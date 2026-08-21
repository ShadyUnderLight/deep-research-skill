"""Issue #407: negative cases must share the same fail-closed audit-set gate as positives.

Reproduces the bypass described in #407: before the fix a duplicated or
truncated ``audits[]`` still yielded ``passed=True`` for negatives with
``checks.required_audits_present=False``.  After the fix the audit-set gate
(``audit_set_exact`` + ``audits_consistent`` + ``required_audits_present``)
is a joint condition for both verdicts and duplicates are detected before set
conversion.
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
from run_forward_evals import _evaluate_case, _expected_audit_set, load_registry

POSITIVE_CASE_ID = "forward-provider-selection"
NEGATIVE_DECLARED = "forward-declared-not-executed"
NEGATIVE_ROUTE_MIS = "forward-route-misclassification"
NEGATIVE_SECONDARY = "forward-secondary-route-not-verified"


def _case(case_id: str):
    registry = load_registry()
    return next(c for c in registry["cases"] if c["id"] == case_id), registry["decision_tree_version"]


def _fake_missing(missing_id: str):
    original = run_forward_evals._run_audit

    def _run(report, research_pack, activation_snapshot=None):
        data, err, rc = original(report, research_pack, activation_snapshot)
        tampered = copy.deepcopy(data)
        tampered["audits"] = [a for a in data["audits"] if a.get("audit_id") != missing_id]
        return tampered, err, rc

    return _run


def _fake_duplicate(dup_id: str = "markdown-delivery"):
    original = run_forward_evals._run_audit

    def _run(report, research_pack, activation_snapshot=None):
        data, err, rc = original(report, research_pack, activation_snapshot)
        tampered = copy.deepcopy(data)
        src = next(a for a in data["audits"] if a.get("audit_id") == dup_id)
        tampered["audits"].append(copy.deepcopy(src))
        return tampered, err, rc

    return _run


def _fake_forged_unknown():
    original = run_forward_evals._run_audit

    def _run(report, research_pack, activation_snapshot=None):
        data, err, rc = original(report, research_pack, activation_snapshot)
        tampered = copy.deepcopy(data)
        tampered["audits"].append(
            {
                "audit_id": "forged-unknown-audit",
                "execution_type": "manual",
                "execution_source": "manual_checklist_attestation",
                "status": "pass",
                "errors": [],
                "warnings": [],
                "evidence": ["report-section:Decision scope"],
                "evidence_provenance": [
                    {
                        "verified": True,
                        "execution_source": "manual_checklist_attestation",
                        "kind": "report_section",
                        "locator": "Decision scope",
                    }
                ],
            }
        )
        return tampered, err, rc

    return _run


# ── positive baseline: genuine still passes with new checks ────────────────


def test_positive_genuine_still_passes_with_audit_set_checks() -> None:
    case, dt_version = _case(POSITIVE_CASE_ID)
    result = _evaluate_case(case, dt_version)
    assert result["passed"] is True
    assert result["checks"]["required_audits_present"] is True
    assert result["checks"]["audit_set_exact"] is True
    assert result["checks"]["audits_consistent"] is True


# ── negative genuine still passes ──────────────────────────────────────────


@pytest.mark.parametrize("case_id", [NEGATIVE_DECLARED, NEGATIVE_ROUTE_MIS, NEGATIVE_SECONDARY])
def test_negative_genuine_still_passes(case_id: str) -> None:
    case, dt_version = _case(case_id)
    result = _evaluate_case(case, dt_version)
    assert result["passed"] is True
    assert result["checks"]["required_audits_present"] is True
    assert result["checks"]["audit_set_exact"] is True
    assert result["checks"]["audits_consistent"] is True


# ── missing audit: positive and both negative families must fail ────────────


def test_missing_global_audit_fails_positive(monkeypatch) -> None:
    case, dt_version = _case(POSITIVE_CASE_ID)
    monkeypatch.setattr(run_forward_evals, "_run_audit", _fake_missing("markdown-delivery"))
    result = _evaluate_case(case, dt_version)
    assert result["checks"]["audit_set_exact"] is False
    assert result["checks"]["required_audits_present"] is False
    assert result["passed"] is False


@pytest.mark.parametrize("case_id", [NEGATIVE_DECLARED, NEGATIVE_ROUTE_MIS])
def test_missing_global_audit_fails_negative(case_id: str, monkeypatch) -> None:
    """Deleting any required/global audit must fail negatives as well as positives."""
    case, dt_version = _case(case_id)
    monkeypatch.setattr(run_forward_evals, "_run_audit", _fake_missing("markdown-delivery"))
    result = _evaluate_case(case, dt_version)
    assert result["checks"]["audit_set_exact"] is False
    assert result["checks"]["required_audits_present"] is False
    assert result["passed"] is False


@pytest.mark.parametrize("case_id", [NEGATIVE_DECLARED, NEGATIVE_SECONDARY])
def test_missing_research_pack_fails_negative(case_id: str, monkeypatch) -> None:
    case, dt_version = _case(case_id)
    monkeypatch.setattr(run_forward_evals, "_run_audit", _fake_missing("research-pack"))
    result = _evaluate_case(case, dt_version)
    assert result["checks"]["required_audits_present"] is False
    assert result["passed"] is False


def test_missing_secondary_hard_fail_fails_negative(monkeypatch) -> None:
    case, dt_version = _case(NEGATIVE_SECONDARY)
    # secondary hard-fail is the defect audit itself; removing it must not pass via structure match
    monkeypatch.setattr(
        run_forward_evals, "_run_audit", _fake_missing("constrained-choice-secondary-hard-fail")
    )
    result = _evaluate_case(case, dt_version)
    assert result["checks"]["required_audits_present"] is False
    assert result["passed"] is False


# ── duplicate audit: must fail and be observable via audit_set_exact ──────


def test_duplicate_audit_fails_positive(monkeypatch) -> None:
    case, dt_version = _case(POSITIVE_CASE_ID)
    monkeypatch.setattr(run_forward_evals, "_run_audit", _fake_duplicate("markdown-delivery"))
    result = _evaluate_case(case, dt_version)
    assert result["checks"]["audit_set_exact"] is False
    assert result["checks"]["audits_consistent"] is False
    assert result["checks"]["required_audits_present"] is False
    assert result["passed"] is False


@pytest.mark.parametrize("case_id", [NEGATIVE_DECLARED, NEGATIVE_ROUTE_MIS])
def test_duplicate_audit_fails_negative(case_id: str, monkeypatch) -> None:
    """Reproduces the #407 bypass: duplicate record must fail negatives and be locatable."""
    case, dt_version = _case(case_id)
    monkeypatch.setattr(run_forward_evals, "_run_audit", _fake_duplicate("markdown-delivery"))
    result = _evaluate_case(case, dt_version)
    # duplicate is caught both by pre-set length check (audit_set_exact) and by _audits_ok
    assert result["checks"]["audit_set_exact"] is False
    assert result["checks"]["audits_consistent"] is False
    assert result["checks"]["required_audits_present"] is False
    assert result["passed"] is False


# ── forged / unknown audit id ──────────────────────────────────────────────


def test_forged_unknown_audit_fails_positive(monkeypatch) -> None:
    case, dt_version = _case(POSITIVE_CASE_ID)
    monkeypatch.setattr(run_forward_evals, "_run_audit", _fake_forged_unknown())
    result = _evaluate_case(case, dt_version)
    assert result["checks"]["required_audits_present"] is False
    assert result["passed"] is False


@pytest.mark.parametrize("case_id", [NEGATIVE_DECLARED, NEGATIVE_ROUTE_MIS])
def test_forged_unknown_audit_fails_negative(case_id: str, monkeypatch) -> None:
    case, dt_version = _case(case_id)
    monkeypatch.setattr(run_forward_evals, "_run_audit", _fake_forged_unknown())
    result = _evaluate_case(case, dt_version)
    assert result["checks"]["required_audits_present"] is False
    assert result["passed"] is False


def test_unknown_report_route_fails_closed_for_route_misclassification(monkeypatch) -> None:
    """Forged unknown report route must fail closed, not raise UnknownRouteError (review P1)."""
    case, dt_version = _case(NEGATIVE_ROUTE_MIS)

    original = run_forward_evals._run_audit

    def _run(report, research_pack, activation_snapshot=None):
        data, err, rc = original(report, research_pack, activation_snapshot)
        tampered = copy.deepcopy(data)
        tampered["route"] = "forged-unknown-route"
        # keep audits consistent with original (market-outlook) so only the route is forged
        return tampered, err, rc

    monkeypatch.setattr(run_forward_evals, "_run_audit", _run)
    # must not raise
    result = _evaluate_case(case, dt_version)
    assert result["passed"] is False
    assert result["checks"]["required_audits_present"] is False
    assert result["checks"]["audit_set_exact"] is False
    assert result["checks"]["audits_consistent"] is False


# ── mixed defects: correct failure_family alone must not rescue a truncated set ─


@pytest.mark.parametrize("case_id", [NEGATIVE_DECLARED, NEGATIVE_ROUTE_MIS])
def test_mixed_missing_plus_correct_failure_family_still_fails(case_id: str, monkeypatch) -> None:
    """Truncation + valid business failure must not pass due to structure match."""
    case, dt_version = _case(case_id)
    # missing global audit, but the structural negative signal is still correct
    monkeypatch.setattr(run_forward_evals, "_run_audit", _fake_missing("markdown-delivery"))
    result = _evaluate_case(case, dt_version)
    # failure_family is still correct, yet overall must fail because audit set is incomplete
    assert result["actual"]["failure_family"] == case["failure_family"]
    assert result["checks"]["required_audits_present"] is False
    assert result["passed"] is False


@pytest.mark.parametrize("case_id", [NEGATIVE_DECLARED, NEGATIVE_SECONDARY])
def test_mixed_duplicate_plus_correct_failure_family_still_fails(case_id: str, monkeypatch) -> None:
    case, dt_version = _case(case_id)
    monkeypatch.setattr(run_forward_evals, "_run_audit", _fake_duplicate("research-pack"))
    result = _evaluate_case(case, dt_version)
    assert result["actual"]["failure_family"] == case["failure_family"]
    assert result["passed"] is False


def test_mixed_unknown_plus_correct_failure_family_still_fails(monkeypatch) -> None:
    case, dt_version = _case(NEGATIVE_DECLARED)
    monkeypatch.setattr(run_forward_evals, "_run_audit", _fake_forged_unknown())
    result = _evaluate_case(case, dt_version)
    assert result["actual"]["failure_family"] == "declared-not-executed"
    assert result["passed"] is False


# ── regression: 11 active cases still 11/11 when not tampered ──────────────


def test_all_active_cases_still_pass_when_not_tampered() -> None:
    registry = load_registry()
    dt_version = registry["decision_tree_version"]
    active = [c for c in registry["cases"] if c["status"] == "active"]
    assert len(active) == 11
    for case in active:
        result = _evaluate_case(case, dt_version)
        assert result["passed"] is True, f"{case['id']} should still pass"
