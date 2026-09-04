"""Issue #408: tighten forward audit status & provenance semantics.

Covers:
- not_run / skipped without reason → fail, with evidence → fail, with verified provenance → fail
- conditional-pass must have warnings, no errors, non-empty evidence and same provenance binding as pass
- pass / conditional-pass share strict execution_source and provenance checks
- fail requires locatable errors
- partial requires reason or errors
- overall / returncode must be consistent with audit statuses
- negative can keep not_run/skipped with reason but cannot aggregate to pass
"""

from __future__ import annotations

# Dynamic sys.path setup is intentional for direct script-module tests.
# ruff: noqa: E402

import copy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import run_forward_evals  # noqa: E402
from run_forward_evals import (
    _audits_ok,
    _audit_consistency_details,
    _expected_audit_set,
    _overall_and_returncode_consistent,
    _overall_consistency_details,
    _evaluate_case,
    load_registry,
)  # noqa: E402


def _real_audit(case_id: str):
    reg = load_registry()
    case = next(c for c in reg["cases"] if c["id"] == case_id)
    rep = ROOT / case["fixtures"]["report"]
    rp = ROOT / case["fixtures"]["research_pack"]
    data, err, rc = run_forward_evals._run_audit(rep, rp)
    assert data is not None, err
    return case, data, rep, rp


def _expected(case) -> list[str]:
    return _expected_audit_set(case["expected"]["primary_route"], case["expected"]["secondary_routes"])


# ── helpers for minimal _audits_ok unit tests without real files ──────────────

def _minimal_pass_audit(audit_id="source-traceability", execution_type="automated", binding="source-label-consistency"):
    # Use a known automated audit that exists in registry
    return {
        "audit_id": audit_id,
        "execution_type": execution_type,
        "execution_source": "automated_validator",
        "status": "pass",
        "errors": [],
        "warnings": [],
        "evidence": ["tests/fixtures/forward/provider-selection-report.md: no violations found by source-label-consistency"],
        "evidence_provenance": [
            {
                "kind": "automated_validator",
                "audit_id": audit_id,
                "locator": binding,
                "validator_binding": binding,
                "execution_source": "automated_validator",
                "target": "tests/fixtures/forward/provider-selection-report.md",
                "validator_version": run_forward_evals.EXPECTED_VALIDATOR_VERSION,
                "verified": True,
            }
        ],
        "validator_binding": binding,
        "reason": None,
    }


# ── not_run / skipped ────────────────────────────────────────────────────────


def test_not_run_without_reason_fails() -> None:
    case, data = _real_audit("forward-provider-selection")[:2]
    expected = _expected(case)
    tampered = copy.deepcopy(data)
    for a in tampered["audits"]:
        if a["audit_id"] == "option-selection-final-audit":
            a["status"] = "not_run"
            a["reason"] = None
            a["evidence"] = []
            a["evidence_provenance"] = []
            a["errors"] = []
            a["warnings"] = []
            break
    tampered["overall"] = "fail"
    assert _audits_ok(tampered, expected) is False


def test_skipped_without_reason_fails() -> None:
    case, data = _real_audit("forward-provider-selection")[:2]
    expected = _expected(case)
    tampered = copy.deepcopy(data)
    for a in tampered["audits"]:
        if a["audit_id"] == "option-selection-final-audit":
            a["status"] = "skipped"
            a["reason"] = ""
            a["evidence"] = []
            a["evidence_provenance"] = []
            break
    assert _audits_ok(tampered, expected) is False


def test_not_run_with_reason_and_no_evidence_passes() -> None:
    case, data = _real_audit("forward-declared-not-executed")[:2]
    # Use the real negative data which already has partial/not_run with reasons
    expected = _expected(case)
    # It should pass _audits_ok when overall is fail (negative case)
    # Data already has overall fail, so check directly
    _, data_real, _, _ = _real_audit("forward-declared-not-executed")
    # data_real already validated via _expected
    assert _audits_ok(data_real, expected) is True


def test_not_run_with_evidence_fails() -> None:
    case, data = _real_audit("forward-provider-selection")[:2]
    expected = _expected(case)
    tampered = copy.deepcopy(data)
    for a in tampered["audits"]:
        if a["audit_id"] == "option-selection-final-audit":
            a["status"] = "not_run"
            a["reason"] = "not executed: manual step"
            a["evidence"] = ["report-section:Decision scope"]
            a["evidence_provenance"] = []
            break
    assert _audits_ok(tampered, expected) is False


def test_not_run_with_verified_provenance_fails() -> None:
    case, data = _real_audit("forward-provider-selection")[:2]
    expected = _expected(case)
    tampered = copy.deepcopy(data)
    for a in tampered["audits"]:
        if a["audit_id"] == "option-selection-final-audit":
            a["status"] = "not_run"
            a["reason"] = "not executed"
            a["evidence"] = []
            a["evidence_provenance"] = [
                {"verified": True, "execution_source": "manual_checklist_attestation", "kind": "report_section", "locator": "Decision scope"}
            ]
            break
    assert _audits_ok(tampered, expected) is False


def test_not_run_with_errors_fails() -> None:
    case, data = _real_audit("forward-provider-selection")[:2]
    expected = _expected(case)
    tampered = copy.deepcopy(data)
    for a in tampered["audits"]:
        if a["audit_id"] == "option-selection-final-audit":
            a["status"] = "not_run"
            a["reason"] = "not executed"
            a["errors"] = ["some error"]
            break
    assert _audits_ok(tampered, expected) is False


def test_not_run_not_allowed_in_overall_pass() -> None:
    case, data = _real_audit("forward-provider-selection")[:2]
    expected = _expected(case)
    tampered = copy.deepcopy(data)
    for a in tampered["audits"]:
        if a["audit_id"] == "option-selection-final-audit":
            a["status"] = "not_run"
            a["reason"] = "not executed: reason"
            a["evidence"] = []
            a["evidence_provenance"] = []
            a["errors"] = []
            a["warnings"] = []
            break
    tampered["overall"] = "pass"
    # Even with reason, overall pass must fail because not_run cannot aggregate to pass
    assert _audits_ok(tampered, expected) is False


# ── conditional-pass ────────────────────────────────────────────────────────


def test_conditional_pass_without_warnings_fails() -> None:
    case, data = _real_audit("forward-academic-vs-technical")[:2]
    expected = _expected(case)
    tampered = copy.deepcopy(data)
    for a in tampered["audits"]:
        if a["audit_id"] == "markdown-delivery":
            a["warnings"] = []
            break
    rep = ROOT / case["fixtures"]["report"]
    rp = ROOT / case["fixtures"]["research_pack"]
    rep_text = rep.read_text(encoding="utf-8", errors="replace")
    pack_text = rp.read_text(encoding="utf-8", errors="replace")
    assert _audits_ok(tampered, expected, audited_path=str(rep), research_pack_path=str(rp), report_text=rep_text, pack_text=pack_text, expected_route="academic-review") is False


def test_conditional_pass_with_errors_fails() -> None:
    case, data = _real_audit("forward-academic-vs-technical")[:2]
    expected = _expected(case)
    tampered = copy.deepcopy(data)
    for a in tampered["audits"]:
        if a["audit_id"] == "markdown-delivery":
            a["errors"] = ["some error"]
            break
    rep = ROOT / case["fixtures"]["report"]
    rp = ROOT / case["fixtures"]["research_pack"]
    assert _audits_ok(tampered, expected, audited_path=str(rep), research_pack_path=str(rp),) is False


def test_conditional_pass_without_evidence_fails() -> None:
    case, data = _real_audit("forward-academic-vs-technical")[:2]
    expected = _expected(case)
    tampered = copy.deepcopy(data)
    for a in tampered["audits"]:
        if a["audit_id"] == "markdown-delivery":
            a["evidence"] = []
            break
    assert _audits_ok(tampered, expected) is False


def test_conditional_pass_without_provenance_fails() -> None:
    case, data = _real_audit("forward-academic-vs-technical")[:2]
    expected = _expected(case)
    tampered = copy.deepcopy(data)
    for a in tampered["audits"]:
        if a["audit_id"] == "markdown-delivery":
            a["evidence_provenance"] = []
            break
    rep = ROOT / case["fixtures"]["report"]
    rp = ROOT / case["fixtures"]["research_pack"]
    rep_text = rep.read_text(encoding="utf-8", errors="replace")
    pack_text = rp.read_text(encoding="utf-8", errors="replace")
    assert _audits_ok(tampered, expected, audited_path=str(rep), research_pack_path=str(rp), report_text=rep_text, pack_text=pack_text, expected_route="academic-review") is False


def test_conditional_pass_forged_provenance_fails() -> None:
    case, data = _real_audit("forward-academic-vs-technical")[:2]
    expected = _expected(case)
    tampered = copy.deepcopy(data)
    for a in tampered["audits"]:
        if a["audit_id"] == "markdown-delivery":
            # Only verified:true without binding fields
            a["evidence_provenance"] = [{"verified": True, "execution_source": "automated_validator"}]
            break
    assert _audits_ok(tampered, expected) is False


def test_conditional_pass_cross_audit_provenance_fails() -> None:
    case, data = _real_audit("forward-academic-vs-technical")[:2]
    expected = _expected(case)
    tampered = copy.deepcopy(data)
    for a in tampered["audits"]:
        if a["audit_id"] == "markdown-delivery":
            for p in a["evidence_provenance"]:
                p["audit_id"] = "source-traceability"
            break
    rep = ROOT / case["fixtures"]["report"]
    rp = ROOT / case["fixtures"]["research_pack"]
    rep_text = rep.read_text(encoding="utf-8", errors="replace")
    pack_text = rp.read_text(encoding="utf-8", errors="replace")
    assert _audits_ok(tampered, expected, audited_path=str(rep), research_pack_path=str(rp), report_text=rep_text, pack_text=pack_text, expected_route="academic-review") is False


def test_conditional_pass_cross_artifact_fails() -> None:
    case, data = _real_audit("forward-academic-vs-technical")[:2]
    expected = _expected(case)
    tampered = copy.deepcopy(data)
    rep = ROOT / case["fixtures"]["report"]
    rp = ROOT / case["fixtures"]["research_pack"]
    for a in tampered["audits"]:
        if a["audit_id"] == "markdown-delivery":
            for p in a["evidence_provenance"]:
                p["target"] = str(rp)
            break
    rep_text = rep.read_text(encoding="utf-8", errors="replace")
    pack_text = rp.read_text(encoding="utf-8", errors="replace")
    assert _audits_ok(tampered, expected, audited_path=str(rep), research_pack_path=str(rp), report_text=rep_text, pack_text=pack_text, expected_route="academic-review") is False


def test_conditional_pass_degraded_source_fails() -> None:
    case, data = _real_audit("forward-academic-vs-technical")[:2]
    # This case is automated so not applicable, test manual conditional-pass via synthetic
    # Instead test that a manual conditional-pass with legacy source fails
    # Create minimal manual conditional-pass audit
    # We will mutate a manual audit to conditional-pass with legacy source and check _audits_ok via real data structure
    # Use provider-selection's manual audit as base
    case2, data2 = _real_audit("forward-provider-selection")[:2]
    expected2 = _expected(case2)
    tampered = copy.deepcopy(data2)
    for a in tampered["audits"]:
        if a["audit_id"] == "option-selection-final-audit":
            a["status"] = "conditional-pass"
            a["warnings"] = ["some warning"]
            a["errors"] = []
            a["evidence"] = ["report-section:Decision scope"]
            a["execution_source"] = "legacy_self_attested"
            # provenance must match execution_source
            a["evidence_provenance"] = [
                {"verified": True, "execution_source": "legacy_self_attested", "kind": "report_section", "locator": "Decision scope"}
            ]
            break
    assert _audits_ok(tampered, expected2) is False


def test_conditional_pass_genuine_still_passes() -> None:
    case, data = _real_audit("forward-academic-vs-technical")[:2]
    expected = _expected(case)
    rep = ROOT / case["fixtures"]["report"]
    rp = ROOT / case["fixtures"]["research_pack"]
    rep_text = rep.read_text(encoding="utf-8", errors="replace")
    pack_text = rp.read_text(encoding="utf-8", errors="replace")
    assert _audits_ok(data, expected, audited_path=str(rep), research_pack_path=str(rp), report_text=rep_text, pack_text=pack_text, expected_route="academic-review") is True


# ── pass / fail / partial ──────────────────────────────────────────────────


def test_pass_with_warnings_fails() -> None:
    case, data = _real_audit("forward-provider-selection")[:2]
    expected = _expected(case)
    tampered = copy.deepcopy(data)
    tampered["audits"][0]["warnings"] = ["warn"]
    assert _audits_ok(tampered, expected) is False


def test_pass_without_evidence_fails() -> None:
    case, data = _real_audit("forward-provider-selection")[:2]
    expected = _expected(case)
    tampered = copy.deepcopy(data)
    tampered["audits"][0]["evidence"] = []
    tampered["audits"][0]["evidence_provenance"] = []
    assert _audits_ok(tampered, expected) is False


def test_pass_legacy_source_fails() -> None:
    case, data = _real_audit("forward-provider-selection")[:2]
    expected = _expected(case)
    tampered = copy.deepcopy(data)
    for a in tampered["audits"]:
        if a["audit_id"] == "option-selection-final-audit":
            a["execution_source"] = "legacy_self_attested"
            a["evidence_provenance"][0]["execution_source"] = "legacy_self_attested"
            break
    assert _audits_ok(tampered, expected) is False


def test_fail_without_errors_fails() -> None:
    case, data = _real_audit("forward-provider-selection")[:2]
    expected = _expected(case)
    tampered = copy.deepcopy(data)
    tampered["audits"][0]["status"] = "fail"
    tampered["audits"][0]["errors"] = []
    assert _audits_ok(tampered, expected) is False


def test_fail_with_empty_error_string_fails() -> None:
    case, data = _real_audit("forward-provider-selection")[:2]
    expected = _expected(case)
    tampered = copy.deepcopy(data)
    tampered["audits"][0]["status"] = "fail"
    tampered["audits"][0]["errors"] = [""]
    assert _audits_ok(tampered, expected) is False


def test_partial_without_reason_or_errors_fails() -> None:
    case, data = _real_audit("forward-provider-selection")[:2]
    expected = _expected(case)
    tampered = copy.deepcopy(data)
    for a in tampered["audits"]:
        if a["audit_id"] == "option-selection-final-audit":
            a["status"] = "partial"
            a["reason"] = None
            a["errors"] = []
            a["evidence"] = []
            break
    assert _audits_ok(tampered, expected) is False


def test_partial_with_reason_passes() -> None:
    case, data = _real_audit("forward-provider-selection")[:2]
    expected = _expected(case)
    tampered = copy.deepcopy(data)
    for a in tampered["audits"]:
        if a["audit_id"] == "option-selection-final-audit":
            a["status"] = "partial"
            a["reason"] = "need human review: evidence ambiguous"
            a["errors"] = []
            a["warnings"] = []
            a["evidence"] = []
            a["evidence_provenance"] = []
            break
    tampered["overall"] = "fail"
    # partial is allowed, overall must be fail (not pass)
    assert _audits_ok(tampered, expected) is True


def test_partial_with_errors_passes() -> None:
    case, data = _real_audit("forward-provider-selection")[:2]
    expected = _expected(case)
    tampered = copy.deepcopy(data)
    for a in tampered["audits"]:
        if a["audit_id"] == "option-selection-final-audit":
            a["status"] = "partial"
            a["reason"] = None
            a["errors"] = ["missing evidence: locator not found"]
            break
    tampered["overall"] = "fail"
    assert _audits_ok(tampered, expected) is True


# ── overall / returncode ──────────────────────────────────────────────────


def test_overall_pass_with_conditional_audit_fails() -> None:
    case, data = _real_audit("forward-provider-selection")[:2]
    expected = _expected(case)
    tampered = copy.deepcopy(data)
    for a in tampered["audits"]:
        if a["audit_id"] == "source-traceability":
            a["status"] = "conditional-pass"
            a["warnings"] = ["w"]
            break
    tampered["overall"] = "pass"
    assert _audits_ok(tampered, expected) is False
    assert _overall_and_returncode_consistent(tampered, 0) is False


def test_overall_conditional_with_fail_audit_fails() -> None:
    case, data = _real_audit("forward-academic-vs-technical")[:2]
    tampered = copy.deepcopy(data)
    for a in tampered["audits"]:
        if a["audit_id"] == "source-traceability":
            a["status"] = "fail"
            a["errors"] = ["err"]
            break
    tampered["overall"] = "conditional-pass"
    assert _audits_ok(tampered, _expected(case)) is False
    assert _overall_and_returncode_consistent(tampered, 1) is False


def test_returncode_mismatch_fails() -> None:
    case, data = _real_audit("forward-provider-selection")[:2]
    assert _overall_and_returncode_consistent(data, 2) is False
    assert _overall_and_returncode_consistent(data, 0) is True


def test_overall_fail_requires_locatable_source() -> None:
    # Fail with all audits pass and no blocking should be unlocatable
    actual = {
        "overall": "fail",
        "audits": [{"audit_id": "a", "status": "pass"}],
        "validators": [{"validator_id": "v", "status": "pass"}],
        "blocking": [],
    }
    assert _overall_and_returncode_consistent(actual, 2) is False
    # With blocking it becomes locatable
    actual["blocking"] = ["[a] fail — reason"]
    assert _overall_and_returncode_consistent(actual, 2) is True


# ── integration via _evaluate_case ────────────────────────────────────────


def test_forward_eval_rejects_not_run_without_reason(monkeypatch) -> None:
    reg = load_registry()
    case = next(c for c in reg["cases"] if c["id"] == "forward-provider-selection")
    orig = run_forward_evals._run_audit

    def fake(report, research_pack, activation_snapshot=None):
        data, err, rc = orig(report, research_pack, activation_snapshot)
        tampered = copy.deepcopy(data)
        for a in tampered["audits"]:
            if a["audit_id"] == "option-selection-final-audit":
                a["status"] = "not_run"
                a["reason"] = None
                a["evidence"] = []
                a["evidence_provenance"] = []
                break
        return tampered, err, rc

    monkeypatch.setattr(run_forward_evals, "_run_audit", fake)
    result = _evaluate_case(case, reg["decision_tree_version"])
    assert result["checks"]["audits_consistent"] is False
    assert result["checks"]["required_audits_present"] is False
    assert result["passed"] is False


def test_forward_eval_rejects_conditional_pass_without_provenance(monkeypatch) -> None:
    reg = load_registry()
    case = next(c for c in reg["cases"] if c["id"] == "forward-academic-vs-technical")
    orig = run_forward_evals._run_audit

    def fake(report, research_pack, activation_snapshot=None):
        data, err, rc = orig(report, research_pack, activation_snapshot)
        tampered = copy.deepcopy(data)
        for a in tampered["audits"]:
            if a["audit_id"] == "markdown-delivery":
                a["evidence_provenance"] = []
                break
        return tampered, err, rc

    monkeypatch.setattr(run_forward_evals, "_run_audit", fake)
    result = _evaluate_case(case, reg["decision_tree_version"])
    assert result["checks"]["audits_consistent"] is False
    assert result["passed"] is False


def test_forward_eval_accepts_genuine_conditional_pass() -> None:
    reg = load_registry()
    case = next(c for c in reg["cases"] if c["id"] == "forward-academic-vs-technical")
    result = _evaluate_case(case, reg["decision_tree_version"])
    assert result["passed"] is True
    assert result["checks"]["audits_consistent"] is True


def test_forward_eval_negative_keeps_not_run_with_reason(monkeypatch) -> None:
    reg = load_registry()
    case = next(c for c in reg["cases"] if c["id"] == "forward-declared-not-executed")
    result = _evaluate_case(case, reg["decision_tree_version"])
    assert result["passed"] is True
    # Now without reason should fail even though failure_family is correct
    orig = run_forward_evals._run_audit

    def fake(report, research_pack, activation_snapshot=None):
        data, err, rc = orig(report, research_pack, activation_snapshot)
        tampered = copy.deepcopy(data)
        for a in tampered["audits"]:
            if a["status"] == "not_run":
                a["reason"] = None
                break
        return tampered, err, rc

    monkeypatch.setattr(run_forward_evals, "_run_audit", fake)
    result2 = _evaluate_case(case, reg["decision_tree_version"])
    assert result2["passed"] is False


def test_forward_eval_overall_returncode_mismatch_fails(monkeypatch) -> None:
    reg = load_registry()
    case = next(c for c in reg["cases"] if c["id"] == "forward-provider-selection")
    orig = run_forward_evals._run_audit

    def fake(report, research_pack, activation_snapshot=None):
        data, err, rc = orig(report, research_pack, activation_snapshot)
        tampered = copy.deepcopy(data)
        # overall pass but returncode 2
        return tampered, err, 2

    monkeypatch.setattr(run_forward_evals, "_run_audit", fake)
    result = _evaluate_case(case, reg["decision_tree_version"])
    assert result["passed"] is False
    assert result["checks"]["overall_and_returncode_ok"] is False


# ── P1: locatable errors ──────────────────────────────────────────────────


def test_audit_consistency_errors_contain_audit_id_and_field() -> None:
    case, data = _real_audit("forward-provider-selection")[:2]
    expected = _expected(case)
    tampered = copy.deepcopy(data)
    for a in tampered["audits"]:
        if a["audit_id"] == "option-selection-final-audit":
            a["status"] = "not_run"
            a["reason"] = None
            a["evidence"] = []
            a["evidence_provenance"] = []
            break
    ok, errs = _audit_consistency_details(tampered, expected)
    assert ok is False
    assert any("option-selection-final-audit" in e and "reason" in e.lower() for e in errs), errs


def test_conditional_pass_provenance_error_is_locatable() -> None:
    case, data = _real_audit("forward-academic-vs-technical")[:2]
    expected = _expected(case)
    tampered = copy.deepcopy(data)
    for a in tampered["audits"]:
        if a["audit_id"] == "markdown-delivery":
            a["evidence_provenance"] = []
            break
    ok, errs = _audit_consistency_details(
        tampered, expected,
        audited_path=str(ROOT / case["fixtures"]["report"]),
        research_pack_path=str(ROOT / case["fixtures"]["research_pack"]),
    )
    assert ok is False
    assert any("markdown-delivery" in e and "provenance" in e.lower() for e in errs), errs


def test_overall_consistency_errors_locatable() -> None:
    case, data = _real_audit("forward-provider-selection")[:2]
    tampered = copy.deepcopy(data)
    tampered["overall"] = "pass"
    # keep returncode 2 to trigger returncode mismatch
    ok, errs = _overall_consistency_details(tampered, 2)
    assert ok is False
    assert any("returncode" in e.lower() or "overall" in e.lower() for e in errs), errs


def test_evaluate_case_exposes_audit_and_overall_errors(monkeypatch) -> None:
    reg = load_registry()
    case = next(c for c in reg["cases"] if c["id"] == "forward-provider-selection")
    orig = run_forward_evals._run_audit

    def fake(report, research_pack, activation_snapshot=None):
        data, err, rc = orig(report, research_pack, activation_snapshot)
        tampered = copy.deepcopy(data)
        for a in tampered["audits"]:
            if a["audit_id"] == "option-selection-final-audit":
                a["status"] = "not_run"
                a["reason"] = None
                a["evidence"] = []
                a["evidence_provenance"] = []
                break
        return tampered, err, rc

    monkeypatch.setattr(run_forward_evals, "_run_audit", fake)
    result = _evaluate_case(case, reg["decision_tree_version"])
    assert result["checks"]["audits_consistent"] is False
    assert "audit_consistency_errors" in result["checks"]
    assert any("option-selection-final-audit" in e for e in result["checks"]["audit_consistency_errors"])
    # returncode mismatch variant
    def fake2(report, research_pack, activation_snapshot=None):
        data, err, rc = orig(report, research_pack, activation_snapshot)
        return data, err, 2  # overall pass but rc 2

    monkeypatch.setattr(run_forward_evals, "_run_audit", fake2)
    result2 = _evaluate_case(case, reg["decision_tree_version"])
    assert result2["checks"]["overall_and_returncode_ok"] is False
    assert any("returncode" in e.lower() for e in result2["checks"]["overall_consistency_errors"])


# ── P2: unified non-empty / type checks for fail/partial ──────────────────


def test_fail_with_whitespace_warnings_fails() -> None:
    case, data = _real_audit("forward-provider-selection")[:2]
    expected = _expected(case)
    tampered = copy.deepcopy(data)
    for a in tampered["audits"]:
        if a["audit_id"] == "option-selection-final-audit":
            a["status"] = "fail"
            a["errors"] = ["something failed"]
            a["warnings"] = ["   "]
            break
    ok, errs = _audit_consistency_details(tampered, expected)
    assert ok is False
    assert any("warnings" in e.lower() for e in errs), errs


def test_partial_with_whitespace_warnings_fails() -> None:
    case, data = _real_audit("forward-provider-selection")[:2]
    expected = _expected(case)
    tampered = copy.deepcopy(data)
    for a in tampered["audits"]:
        if a["audit_id"] == "option-selection-final-audit":
            a["status"] = "partial"
            a["reason"] = "needs review"
            a["warnings"] = ["   "]
            break
    ok, errs = _audit_consistency_details(tampered, expected)
    assert ok is False
    assert any("warnings" in e.lower() for e in errs), errs


def test_fail_evidence_provenance_not_list_fails() -> None:
    case, data = _real_audit("forward-provider-selection")[:2]
    expected = _expected(case)
    tampered = copy.deepcopy(data)
    for a in tampered["audits"]:
        if a["audit_id"] == "option-selection-final-audit":
            a["status"] = "fail"
            a["errors"] = ["err"]
            a["evidence_provenance"] = {"verified": True}  # type error
            break
    ok, errs = _audit_consistency_details(tampered, expected)
    assert ok is False
    assert any("evidence_provenance" in e.lower() for e in errs), errs


def test_partial_evidence_provenance_not_list_fails() -> None:
    case, data = _real_audit("forward-provider-selection")[:2]
    expected = _expected(case)
    tampered = copy.deepcopy(data)
    for a in tampered["audits"]:
        if a["audit_id"] == "option-selection-final-audit":
            a["status"] = "partial"
            a["reason"] = "needs review"
            a["evidence_provenance"] = {"verified": True}
            break
    ok, errs = _audit_consistency_details(tampered, expected)
    assert ok is False
    assert any("evidence_provenance" in e.lower() for e in errs), errs


def test_partial_with_reason_and_whitespace_error_fails() -> None:
    case, data = _real_audit("forward-provider-selection")[:2]
    expected = _expected(case)
    tampered = copy.deepcopy(data)
    for a in tampered["audits"]:
        if a["audit_id"] == "option-selection-final-audit":
            a["status"] = "partial"
            a["reason"] = "needs review"
            a["errors"] = ["   "]
            a["warnings"] = []
            a["evidence"] = []
            a["evidence_provenance"] = []
            break
    ok, errs = _audit_consistency_details(tampered, expected)
    assert ok is False
    assert any("errors" in e.lower() and "option-selection-final-audit" in e for e in errs), errs


def test_partial_warnings_empty_string_also_rejected_diagnostically() -> None:
    # Ensures the diagnostic path from P2 is exercised: warnings=["   "] is
    # not silently accepted as internally consistent.
    actual = {
        "overall": "fail",
        "audits": [
            {
                "audit_id": "final-audit",
                "execution_type": "manual",
                "execution_source": "manual_checklist_attestation",
                "status": "partial",
                "reason": "needs review",
                "errors": [],
                "warnings": ["   "],
                "evidence": [],
                "evidence_provenance": [],
            },
            {
                "audit_id": "markdown-delivery",
                "execution_type": "automated",
                "execution_source": "automated_validator",
                "status": "pass",
                "errors": [],
                "warnings": [],
                "evidence": ["x: y"],
                "evidence_provenance": [{"verified": True, "execution_source": "automated_validator", "audit_id": "markdown-delivery", "validator_binding": "markdown-delivery", "validator_version": run_forward_evals.EXPECTED_VALIDATOR_VERSION, "target": "x", "input_sha256": "y"}],
                "validator_binding": "markdown-delivery",
            },
            {
                "audit_id": "research-pack",
                "execution_type": "automated",
                "execution_source": "automated_validator",
                "status": "pass",
                "errors": [],
                "warnings": [],
                "evidence": ["x: y"],
                "evidence_provenance": [{"verified": True, "execution_source": "automated_validator", "audit_id": "research-pack", "validator_binding": "research-pack", "validator_version": run_forward_evals.EXPECTED_VALIDATOR_VERSION, "target": "x", "input_sha256": "y"}],
                "validator_binding": "research-pack",
            },
        ],
        "validators": [],
        "blocking": [],
        "input_sha256": None,
    }
    # Use a minimal expected set that matches the audits above
    expected_ids = ["final-audit", "markdown-delivery", "research-pack"]
    ok, errs = _audit_consistency_details(actual, expected_ids)
    assert ok is False
    assert any("warnings" in e.lower() and "final-audit" in e for e in errs), errs
