"""Issue #403: forward-eval consumer must fail closed on forged / truncated audit provenance.

These tests pin the consumer-side hardening that #401/#402 delivered on the
producer side (audit_report.py): the runner must reject any audit JSON whose
audits[] / validators[] set is incomplete, duplicated, forged, or internally
inconsistent — not silently aggregate a truncated/forged record to Pass.
"""

from __future__ import annotations

import copy
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import run_forward_evals
from run_forward_evals import (
    _audits_ok,
    _evaluate_case,
    _expected_audit_set,
    load_registry,
)

POSITIVE_CASE_ID = "forward-provider-selection"


def _real_audit_for(case_id: str):
    registry = load_registry()
    case = next(c for c in registry["cases"] if c["id"] == case_id)
    report = ROOT / case["fixtures"]["report"]
    pack = ROOT / case["fixtures"]["research_pack"]
    data, err, _ = run_forward_evals._run_audit(report, pack)
    assert data is not None, err
    return case, data


def _expected_for(case) -> list[str]:
    return _expected_audit_set(
        case["expected"]["primary_route"], case["expected"]["secondary_routes"]
    )


# ── _expected_audit_set ──────────────────────────────────────────────────────


def test_expected_audit_set_matches_real_audits() -> None:
    case, data = _real_audit_for(POSITIVE_CASE_ID)
    expected = _expected_for(case)
    assert expected is not None
    assert set(expected) == {a["audit_id"] for a in data["audits"]}
    # global delivery audits are included even though the case YAML does not
    # enumerate them (this is what makes truncation fail closed).
    assert "markdown-delivery" in expected
    assert "research-pack" in expected


def test_expected_audit_set_includes_secondary_hard_fail() -> None:
    registry = load_registry()
    case = next(
        c for c in registry["cases"] if c["id"] == "forward-secondary-route-not-verified"
    )
    expected = _expected_for(case)
    assert expected is not None
    assert any(s.endswith("-secondary-hard-fail") for s in expected)


def test_expected_audit_set_registry_drift_returns_none() -> None:
    real = run_forward_evals._AUDIT_REGISTRY.get_audit
    run_forward_evals._AUDIT_REGISTRY.get_audit = lambda _aid: None
    try:
        assert _expected_audit_set("provider-selection", []) is None
    finally:
        run_forward_evals._AUDIT_REGISTRY.get_audit = real


# ── _audits_ok: genuine data accepted ────────────────────────────────────────


def test_audits_ok_accepts_genuine_audit_json() -> None:
    case, data = _real_audit_for(POSITIVE_CASE_ID)
    assert _audits_ok(data, _expected_for(case)) is True


# ── _audits_ok: fail closed on truncation / forgery ──────────────────────────


def test_audits_ok_rejects_missing_global_audit() -> None:
    case, data = _real_audit_for(POSITIVE_CASE_ID)
    expected = _expected_for(case)
    tampered = copy.deepcopy(data)
    tampered["audits"] = [
        a for a in data["audits"] if a["audit_id"] != "markdown-delivery"
    ]
    assert _audits_ok(tampered, expected) is False


def test_audits_ok_rejects_unknown_forged_audit_id() -> None:
    case, data = _real_audit_for(POSITIVE_CASE_ID)
    expected = _expected_for(case)
    tampered = copy.deepcopy(data)
    tampered["audits"].append(
        {
            "audit_id": "forged-audit",
            "execution_type": "automated",
            "execution_source": "automated_validator",
            "status": "pass",
            "errors": [],
            "warnings": [],
            "evidence": ["report: no violations found"],
            "evidence_provenance": [{}],
            "validator_binding": "forged-audit",
        }
    )
    assert _audits_ok(tampered, expected) is False


def test_audits_ok_rejects_duplicate_audit_id() -> None:
    case, data = _real_audit_for(POSITIVE_CASE_ID)
    expected = _expected_for(case)
    tampered = copy.deepcopy(data)
    tampered["audits"].append(
        next(a for a in data["audits"] if a["audit_id"] == "markdown-delivery")
    )
    assert _audits_ok(tampered, expected) is False


def test_audits_ok_rejects_wrong_validator_binding() -> None:
    case, data = _real_audit_for(POSITIVE_CASE_ID)
    expected = _expected_for(case)
    tampered = copy.deepcopy(data)
    for a in tampered["audits"]:
        if a["audit_id"] == "source-traceability":
            a["validator_binding"] = "not-the-registry-binding"
    assert _audits_ok(tampered, expected) is False


def test_audits_ok_rejects_wrong_execution_source() -> None:
    case, data = _real_audit_for(POSITIVE_CASE_ID)
    expected = _expected_for(case)
    tampered = copy.deepcopy(data)
    tampered["audits"][0]["execution_source"] = "trusted_human"
    assert _audits_ok(tampered, expected) is False


def test_audits_ok_rejects_pass_with_errors() -> None:
    case, data = _real_audit_for(POSITIVE_CASE_ID)
    expected = _expected_for(case)
    tampered = copy.deepcopy(data)
    tampered["audits"][0]["errors"] = ["boom"]
    assert _audits_ok(tampered, expected) is False


def test_audits_ok_rejects_pass_without_evidence() -> None:
    case, data = _real_audit_for(POSITIVE_CASE_ID)
    expected = _expected_for(case)
    tampered = copy.deepcopy(data)
    tampered["audits"][0]["evidence"] = []
    assert _audits_ok(tampered, expected) is False


def test_audits_ok_rejects_pass_without_provenance() -> None:
    case, data = _real_audit_for(POSITIVE_CASE_ID)
    expected = _expected_for(case)
    tampered = copy.deepcopy(data)
    tampered["audits"][0]["evidence_provenance"] = []
    assert _audits_ok(tampered, expected) is False


def test_audits_ok_rejects_fail_without_errors() -> None:
    case, data = _real_audit_for(POSITIVE_CASE_ID)
    expected = _expected_for(case)
    tampered = copy.deepcopy(data)
    tampered["audits"][0]["status"] = "fail"
    tampered["audits"][0]["errors"] = []
    assert _audits_ok(tampered, expected) is False


# ── Full consumer pipeline (via _evaluate_case) fail closed ──────────────────


def _positive_case():
    registry = load_registry()
    return next(c for c in registry["cases"] if c["id"] == POSITIVE_CASE_ID)


def test_forward_eval_rejects_truncated_audit_json(monkeypatch) -> None:
    """Dropping a mandatory global audit must fail the positive case."""
    case = _positive_case()
    original = run_forward_evals._run_audit

    def fake_run(report, research_pack, activation_snapshot=None):
        data, err, rc = original(report, research_pack)
        truncated = copy.deepcopy(data)
        truncated["audits"] = [
            a for a in data["audits"] if a["audit_id"] != "markdown-delivery"
        ]
        return truncated, err, rc

    monkeypatch.setattr(run_forward_evals, "_run_audit", fake_run)
    result = _evaluate_case(case, load_registry()["decision_tree_version"])
    assert result["checks"]["required_audits_present"] is False
    assert result["passed"] is False


def test_forward_eval_rejects_forged_validator_version(monkeypatch) -> None:
    """A forged top-level validator_version must fail the positive case."""
    case = _positive_case()
    original = run_forward_evals._run_audit

    def fake_run(report, research_pack, activation_snapshot=None):
        data, err, rc = original(report, research_pack)
        forged = copy.deepcopy(data)
        forged["validator_version"] = "forged-registry-v9"
        return forged, err, rc

    monkeypatch.setattr(run_forward_evals, "_run_audit", fake_run)
    result = _evaluate_case(case, load_registry()["decision_tree_version"])
    assert result["checks"]["validators_ok"] is False
    assert result["passed"] is False
