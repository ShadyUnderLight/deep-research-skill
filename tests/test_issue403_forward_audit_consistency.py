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
    expected = _expected_for(case)
    # Verify with consumer-computed hash anchor (mandatory path for real pipeline)
    import hashlib
    from pathlib import Path

    report = ROOT / case["fixtures"]["report"]
    rp = ROOT / case["fixtures"]["research_pack"]
    expected_report_sha256 = hashlib.sha256(report.read_bytes()).hexdigest()
    expected_pack_sha256 = hashlib.sha256(rp.read_bytes()).hexdigest()
    assert _audits_ok(
        data,
        expected,
        audited_path=str(report),
        expected_report_sha256=expected_report_sha256,
        research_pack_path=str(rp),
        expected_pack_sha256=expected_pack_sha256,
    ) is True
    # Also passes when called without the external anchor (fallback to non-empty)
    assert _audits_ok(data, expected) is True


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


def test_audits_ok_rejects_automated_masquerading_as_manual() -> None:
    """An automated audit (registry: automated) flipping to manual + a manual
    attestation source must NOT dodge the validator_binding check (issue #403
    P1)."""
    case, data = _real_audit_for(POSITIVE_CASE_ID)
    expected = _expected_for(case)
    tampered = copy.deepcopy(data)
    for a in tampered["audits"]:
        if a["audit_id"] == "source-traceability":  # registry: automated
            a["execution_type"] = "manual"
            a["execution_source"] = "manual_checklist_attestation"
            a["validator_binding"] = "whatever-or-null"
    assert _audits_ok(tampered, expected) is False


def test_audits_ok_rejects_string_provenance() -> None:
    """A list of strings is not a provenance record (issue #403 P1)."""
    case, data = _real_audit_for(POSITIVE_CASE_ID)
    expected = _expected_for(case)
    tampered = copy.deepcopy(data)
    tampered["audits"][0]["evidence_provenance"] = ["hello"]
    assert _audits_ok(tampered, expected) is False


def test_audits_ok_rejects_unverified_provenance() -> None:
    """A provenance record with verified != True must be rejected (issue #403
    P1)."""
    case, data = _real_audit_for(POSITIVE_CASE_ID)
    expected = _expected_for(case)
    tampered = copy.deepcopy(data)
    tampered["audits"][0]["evidence_provenance"] = [
        {"verified": False, "execution_source": "automated_validator"}
    ]
    assert _audits_ok(tampered, expected) is False


def test_audits_ok_rejects_provenance_field_mismatch() -> None:
    """An automated provenance record must match the audit result's
    audit_id / binding / validator_version (issue #403 P1)."""
    case, data = _real_audit_for(POSITIVE_CASE_ID)
    expected = _expected_for(case)
    tampered = copy.deepcopy(data)
    for a in tampered["audits"]:
        if a["audit_id"] == "source-traceability":
            rec = a["evidence_provenance"][0]
            rec["audit_id"] = "not-source-traceability"
            rec["validator_binding"] = "wrong-binding"
            rec["validator_version"] = "audit-registry-v1 (route-manifest-v1)"
    assert _audits_ok(tampered, expected) is False


def test_audits_ok_rejects_provenance_hash_mismatch() -> None:
    """For a report-targeted automated audit, a forged artifact hash in the
    provenance must fail closed (issue #403 P1 / scope 3)."""
    import hashlib
    from pathlib import Path

    case, data = _real_audit_for(POSITIVE_CASE_ID)
    expected = _expected_for(case)
    tampered = copy.deepcopy(data)
    target = None
    report = ROOT / case["fixtures"]["report"]
    expected_report_sha256 = hashlib.sha256(report.read_bytes()).hexdigest()
    for a in tampered["audits"]:
        if a["audit_id"] == "source-traceability":
            target = a["evidence_provenance"][0]["target"]
            a["evidence_provenance"][0]["input_sha256"] = "forged-hash"
    assert target is not None
    assert _audits_ok(
        tampered,
        expected,
        audited_path=target,
        expected_report_sha256=expected_report_sha256,
    ) is False


def test_audits_ok_rejects_provenance_target_swap() -> None:
    """Swapping a report-targeted provenance target to another file must fail
    closed — the hash comparison must not be skippable via target (issue #403
    P1)."""
    import hashlib

    case, data = _real_audit_for(POSITIVE_CASE_ID)
    expected = _expected_for(case)
    tampered = copy.deepcopy(data)
    report = ROOT / case["fixtures"]["report"]
    expected_report_sha256 = hashlib.sha256(report.read_bytes()).hexdigest()
    for a in tampered["audits"]:
        if a["audit_id"] == "source-traceability":
            a["evidence_provenance"][0]["target"] = "some-other-report.md"
            a["evidence_provenance"][0]["input_sha256"] = "anything-non-empty"
    assert _audits_ok(
        tampered,
        expected,
        audited_path=str(report),
        expected_report_sha256=expected_report_sha256,
    ) is False


def test_audits_ok_rejects_research_pack_provenance_wrong_artifact() -> None:
    """The research-pack audit's provenance must bind to the research pack,
    not the report — swapping to the report target/hash must fail closed
    (issue #403 P1)."""
    import hashlib

    case, data = _real_audit_for(POSITIVE_CASE_ID)
    expected = _expected_for(case)
    tampered = copy.deepcopy(data)
    report = ROOT / case["fixtures"]["report"]
    rp = ROOT / case["fixtures"]["research_pack"]
    expected_report_sha256 = hashlib.sha256(report.read_bytes()).hexdigest()
    expected_pack_sha256 = hashlib.sha256(rp.read_bytes()).hexdigest()
    for a in tampered["audits"]:
        if a["audit_id"] == "research-pack":
            a["evidence_provenance"][0]["target"] = str(report)
            a["evidence_provenance"][0]["input_sha256"] = expected_report_sha256
    assert _audits_ok(
        tampered,
        expected,
        audited_path=str(report),
        expected_report_sha256=expected_report_sha256,
        research_pack_path=str(rp),
        expected_pack_sha256=expected_pack_sha256,
    ) is False


def test_audits_ok_rejects_manual_stripped_provenance() -> None:
    """A manual pass audit whose provenance is stripped to bare
    verified+execution_source (no kind/locator) must fail closed — otherwise
    an attacker can fabricate the boolean alongside the JSON (issue #403 P1)."""
    case, data = _real_audit_for(POSITIVE_CASE_ID)
    expected = _expected_for(case)
    tampered = copy.deepcopy(data)
    for a in tampered["audits"]:
        if a["audit_id"] == "option-selection-final-audit":  # registry: manual
            a["evidence_provenance"] = [
                {"verified": True, "execution_source": "manual_checklist_attestation"}
            ]
    assert _audits_ok(tampered, expected) is False


def test_audits_ok_rejects_fake_kind() -> None:
    """A manual provenance with a forged kind must fail closed (issue #403
    re-review)."""
    case, data = _real_audit_for(POSITIVE_CASE_ID)
    expected = _expected_for(case)
    tampered = copy.deepcopy(data)
    for a in tampered["audits"]:
        if a["audit_id"] == "option-selection-final-audit":
            a["evidence_provenance"] = [
                {
                    "verified": True,
                    "execution_source": "manual_checklist_attestation",
                    "kind": "forged_kind",
                    "locator": "whatever",
                }
            ]
    assert _audits_ok(tampered, expected) is False


def test_audits_ok_rejects_locator_mismatch() -> None:
    """A valid-looking kind but locator that does not match evidence must fail
    closed (issue #403 re-review)."""
    case, data = _real_audit_for(POSITIVE_CASE_ID)
    expected = _expected_for(case)
    tampered = copy.deepcopy(data)
    for a in tampered["audits"]:
        if a["audit_id"] == "option-selection-final-audit":
            a["evidence_provenance"] = [
                {
                    "verified": True,
                    "execution_source": "manual_checklist_attestation",
                    "kind": "report_section",
                    "locator": "A Completely Different Section",
                }
            ]
    assert _audits_ok(tampered, expected) is False


def test_audits_ok_rejects_legacy_source_for_pass() -> None:
    """A manual pass with a degraded/legacy execution_source must fail closed
    in strict mode (issue #403 re-review)."""
    case, data = _real_audit_for(POSITIVE_CASE_ID)
    expected = _expected_for(case)
    for forged_source in ("unknown", "legacy_self_attested"):
        tampered = copy.deepcopy(data)
        for a in tampered["audits"]:
            if a["audit_id"] == "option-selection-final-audit":
                a["execution_source"] = forged_source
                # also adjust provenance to stay consistent with the forged source
                a["evidence_provenance"][0]["execution_source"] = forged_source
        assert _audits_ok(tampered, expected) is False, forged_source


def test_audits_ok_rejects_malformed_audits_without_crash() -> None:
    """Non-object audit entries (null / string) must fail closed, not raise
    (issue #403 P2)."""
    expected = ["markdown-delivery", "research-pack"]
    assert _audits_ok({"audits": [None]}, expected) is False
    assert _audits_ok({"audits": ["corrupted"]}, expected) is False
    assert _audits_ok({"audits": [{"audit_id": "markdown-delivery"}]}, expected) is False


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


def test_forward_eval_rejects_simultaneously_forged_hashes(monkeypatch) -> None:
    """Top-level + validator hashes simultaneously forged to the same fake value
    must still fail against the consumer-computed external anchor (issue #403
    P1)."""
    case = _positive_case()
    original = run_forward_evals._run_audit

    def fake_run(report, research_pack, activation_snapshot=None):
        data, err, rc = original(report, research_pack)
        forged = copy.deepcopy(data)
        forged["input_sha256"] = "forged"
        for v in forged["validators"]:
            v["input_sha256"] = "forged"
        return forged, err, rc

    monkeypatch.setattr(run_forward_evals, "_run_audit", fake_run)
    result = _evaluate_case(case, load_registry()["decision_tree_version"])
    assert result["checks"]["validators_ok"] is False
    assert result["passed"] is False


def test_forward_eval_rejects_research_pack_wrong_artifact(monkeypatch) -> None:
    """The research-pack provenance must bind to the research pack, not the
    report — swapping its target/hash to the report must fail closed (issue
    #403 P1)."""
    case = _positive_case()
    original = run_forward_evals._run_audit

    def fake_run(report, research_pack, activation_snapshot=None):
        data, err, rc = original(report, research_pack)
        forged = copy.deepcopy(data)
        for a in forged["audits"]:
            if a["audit_id"] == "research-pack":
                rec = a["evidence_provenance"][0]
                rec["target"] = str(report)
                # also forge hash to report's hash so it would pass a
                # JSON-internal check but fail the consumer's pack anchor
                import hashlib
                from pathlib import Path

                rec["input_sha256"] = hashlib.sha256(Path(report).read_bytes()).hexdigest()
        return forged, err, rc

    monkeypatch.setattr(run_forward_evals, "_run_audit", fake_run)
    result = _evaluate_case(case, load_registry()["decision_tree_version"])
    assert result["checks"]["required_audits_present"] is False
    assert result["passed"] is False


def test_forward_eval_rejects_malformed_audits_without_crash(monkeypatch) -> None:
    """Malformed audits (null / string entries) must fail the positive case
    via the consumer gate, not crash the runner (issue #403 P2)."""
    case = _positive_case()
    original = run_forward_evals._run_audit

    def fake_run(report, research_pack, activation_snapshot=None):
        data, err, rc = original(report, research_pack)
        malformed = copy.deepcopy(data)
        malformed["audits"] = [None, "corrupted", {"audit_id": "markdown-delivery"}]
        return malformed, err, rc

    monkeypatch.setattr(run_forward_evals, "_run_audit", fake_run)
    result = _evaluate_case(case, load_registry()["decision_tree_version"])
    assert result["checks"]["required_audits_present"] is False
    assert result["passed"] is False


def test_forward_eval_rejects_masqueraded_automated_audit(monkeypatch) -> None:
    """Flipping an automated audit to manual + manual source must fail the
    positive case (issue #403 P1)."""
    case = _positive_case()
    original = run_forward_evals._run_audit

    def fake_run(report, research_pack, activation_snapshot=None):
        data, err, rc = original(report, research_pack)
        forged = copy.deepcopy(data)
        for a in forged["audits"]:
            if a["audit_id"] == "source-traceability":
                a["execution_type"] = "manual"
                a["execution_source"] = "manual_checklist_attestation"
                a["validator_binding"] = "whatever"
        return forged, err, rc

    monkeypatch.setattr(run_forward_evals, "_run_audit", fake_run)
    result = _evaluate_case(case, load_registry()["decision_tree_version"])
    assert result["checks"]["required_audits_present"] is False
    assert result["passed"] is False


def test_forward_eval_rejects_false_provenance(monkeypatch) -> None:
    """A pass audit with unverified / non-record provenance must fail the
    positive case (issue #403 P1)."""
    case = _positive_case()
    original = run_forward_evals._run_audit

    def fake_run(report, research_pack, activation_snapshot=None):
        data, err, rc = original(report, research_pack)
        forged = copy.deepcopy(data)
        for a in forged["audits"]:
            if a["audit_id"] == "source-traceability":
                a["evidence_provenance"] = [{"verified": False}]
        return forged, err, rc

    monkeypatch.setattr(run_forward_evals, "_run_audit", fake_run)
    result = _evaluate_case(case, load_registry()["decision_tree_version"])
    assert result["checks"]["required_audits_present"] is False
    assert result["passed"] is False
