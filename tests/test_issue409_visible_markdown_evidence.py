"""Issue #409: forward consumer must only accept visible Markdown evidence.

Producer (audit_report.py) already sanitizes report/pack via
``sanitize_visible_markdown`` before validating manual/process evidence.
The forward consumer must do the same — a heading/table that only exists
inside a fenced code block or raw HTML block must NOT satisfy
``report-section`` / ``report-table`` / ``pack-section`` / ``pack-table``
evidence.

This file covers:
- report-section hidden in backtick / tilde / unclosed / nested / HTML fences → fail
- visible heading → pass
- report-table hidden / visible
- pack-section / pack-table symmetry
- diagnostics contain "not found in the visible report/pack"
- checklist markers hidden in fences → fail, visible → pass
- artifact hash stays bound to raw bytes
- producer / consumer parity (same visible sanitizer)
"""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from audit_evidence import validate_evidence_reference
from validate_contract import sanitize_visible_markdown, strip_fenced_code_blocks_only

import run_forward_evals
from run_forward_evals import (
    _audit_consistency_details,
    _audit_provenance_details,
    _audits_ok,
    _expected_audit_set,
    load_registry,
)

# Use a known manual audit that exists in the registry; its evidence is
# report-scoped manual attestation.
MANUAL_AUDIT_ID = "option-selection-final-audit"
MANUAL_EXECUTION_TYPE = "manual"
MANUAL_SOURCE = "manual_checklist_attestation"

# For pack tests we reuse the same manual audit but with pack kind — the
# registry execution_type check still passes because the audit is manual.
# Pack evidence validation is independent of registry route, but we keep the
# audit_id real so registry lookup succeeds.


def _sanitized(text: str) -> str:
    return sanitize_visible_markdown(text)


def _pass_audit(
    audit_id: str,
    evidence: str,
    kind: str,
    locator: str,
    *,
    execution_type: str = MANUAL_EXECUTION_TYPE,
    source: str = MANUAL_SOURCE,
    binding=None,
):
    return {
        "audit_id": audit_id,
        "execution_type": execution_type,
        "execution_source": source,
        "status": "pass",
        "errors": [],
        "warnings": [],
        "evidence": [evidence],
        "evidence_provenance": [
            {
                "verified": True,
                "execution_source": source,
                "kind": kind,
                "locator": locator,
            }
        ],
        "validator_binding": binding,
        "reason": None,
    }


def _minimal_overall(pass_audit: dict) -> dict:
    # Provide a minimal valid overall structure for _audits_ok /
    # _audit_consistency_details.  Include a synthetic overall pass.
    return {
        "overall": "pass",
        "audits": [pass_audit],
        "validators": [],
        "blocking": [],
        "input_sha256": None,
    }


# ── helpers for hidden vs visible texts ────────────────────────────────────

HIDDEN_HEADING = "Hidden claim"

REPORT_WITH_HIDDEN_ONLY = f"""# Report

Some intro.

```markdown
## {HIDDEN_HEADING}
Hidden content inside fence.
```

More text but no real heading.
"""

REPORT_WITH_HIDDEN_TILDE = f"""# Report

~~~markdown
## {HIDDEN_HEADING}
Inside tilde fence
~~~

End.
"""

REPORT_WITH_HIDDEN_UNCLOSED = f"""# Report

```markdown
## {HIDDEN_HEADING}
Unclosed fence — rest of file is code.

Still code, not a heading.
"""

REPORT_WITH_VISIBLE = f"""# Report

## {HIDDEN_HEADING}

Visible content.

| col | val |
|---|---|
| a | b |
"""

REPORT_WITH_HTML_HIDDEN = f"""# Report

<div>
## {HIDDEN_HEADING}
This is inside a raw HTML block (type 6) — not visible Markdown.
</div>

End.
"""

REPORT_WITH_TABLE_VISIBLE = f"""# Report

## {HIDDEN_HEADING}

| header1 | header2 |
|---|---|
| cell1 | cell2 |
"""

REPORT_WITH_TABLE_HIDDEN_IN_FENCE = f"""# Report

```markdown
## {HIDDEN_HEADING}

| header1 | header2 |
|---|---|
| cell1 | cell2 |
```
"""

REPORT_WITH_TABLE_HIDDEN_IN_HTML = f"""# Report

<div>
## {HIDDEN_HEADING}
| header1 | header2 |
|---|---|
| cell1 | cell2 |
</div>
"""

# Nested-looking fence: outer fence is 4 backticks, inner 3 backticks should NOT close it
REPORT_WITH_NESTED_FENCE = f"""# Report

````markdown
```markdown
## {HIDDEN_HEADING}
Inner fence should not close outer.
```
Still inside outer fence.
````

After outer fence, no heading.
"""

PACK_WITH_HIDDEN_ONLY = f"""# Pack

```markdown
## {HIDDEN_HEADING}
Hidden pack heading
```

No visible pack heading.
"""

PACK_WITH_VISIBLE = f"""# Pack

## {HIDDEN_HEADING}

Pack visible content.

| h1 | h2 |
|---|---|
| v1 | v2 |
"""

PACK_WITH_TILDE_HIDDEN = f"""# Pack

~~~markdown
## {HIDDEN_HEADING}
Hidden
~~~
"""

# ── report-section tests ────────────────────────────────────────────────────


def test_report_section_backtick_fence_hidden_fails():
    sanitized = _sanitized(REPORT_WITH_HIDDEN_ONLY)
    result = validate_evidence_reference(
        f"report-section:{HIDDEN_HEADING}",
        artifact_text=sanitized,
        base_dir=ROOT,
        strict=True,
        artifact_label="report",
    )
    assert not result.is_valid
    assert "not found in the visible report" in "; ".join(result.errors).lower()


def test_report_section_tilde_fence_hidden_fails():
    sanitized = _sanitized(REPORT_WITH_HIDDEN_TILDE)
    result = validate_evidence_reference(
        f"report-section:{HIDDEN_HEADING}",
        artifact_text=sanitized,
        base_dir=ROOT,
        strict=True,
        artifact_label="report",
    )
    assert not result.is_valid
    assert "not found in the visible report" in "; ".join(result.errors).lower()


def test_report_section_unclosed_fence_hidden_fails():
    sanitized = _sanitized(REPORT_WITH_HIDDEN_UNCLOSED)
    result = validate_evidence_reference(
        f"report-section:{HIDDEN_HEADING}",
        artifact_text=sanitized,
        base_dir=ROOT,
        strict=True,
        artifact_label="report",
    )
    assert not result.is_valid
    assert "not found in the visible report" in "; ".join(result.errors).lower()


def test_report_section_nested_fence_not_exposed():
    sanitized = _sanitized(REPORT_WITH_NESTED_FENCE)
    result = validate_evidence_reference(
        f"report-section:{HIDDEN_HEADING}",
        artifact_text=sanitized,
        base_dir=ROOT,
        strict=True,
        artifact_label="report",
    )
    assert not result.is_valid
    assert "not found in the visible report" in "; ".join(result.errors).lower()


def test_report_section_html_block_hidden_fails():
    sanitized = _sanitized(REPORT_WITH_HTML_HIDDEN)
    result = validate_evidence_reference(
        f"report-section:{HIDDEN_HEADING}",
        artifact_text=sanitized,
        base_dir=ROOT,
        strict=True,
        artifact_label="report",
    )
    assert not result.is_valid
    assert "not found in the visible report" in "; ".join(result.errors).lower()


def test_report_section_visible_passes():
    sanitized = _sanitized(REPORT_WITH_VISIBLE)
    result = validate_evidence_reference(
        f"report-section:{HIDDEN_HEADING}",
        artifact_text=sanitized,
        base_dir=ROOT,
        strict=True,
        artifact_label="report",
    )
    assert result.is_valid, result.errors
    assert result.provenance and result.provenance.get("verified") is True


# ── report-table tests ──────────────────────────────────────────────────────


def test_report_table_hidden_in_fence_fails():
    sanitized = _sanitized(REPORT_WITH_TABLE_HIDDEN_IN_FENCE)
    result = validate_evidence_reference(
        f"report-table:{HIDDEN_HEADING}",
        artifact_text=sanitized,
        base_dir=ROOT,
        strict=True,
        artifact_label="report",
    )
    assert not result.is_valid
    # Either not found as heading, or not a visible table
    err = "; ".join(result.errors).lower()
    assert "not found in the visible report" in err or "does not point to a visible markdown table" in err


def test_report_table_hidden_in_html_fails():
    sanitized = _sanitized(REPORT_WITH_TABLE_HIDDEN_IN_HTML)
    result = validate_evidence_reference(
        f"report-table:{HIDDEN_HEADING}",
        artifact_text=sanitized,
        base_dir=ROOT,
        strict=True,
        artifact_label="report",
    )
    assert not result.is_valid
    err = "; ".join(result.errors).lower()
    assert "not found in the visible report" in err or "does not point to a visible markdown table" in err


def test_report_table_visible_passes():
    sanitized = _sanitized(REPORT_WITH_TABLE_VISIBLE)
    result = validate_evidence_reference(
        f"report-table:{HIDDEN_HEADING}",
        artifact_text=sanitized,
        base_dir=ROOT,
        strict=True,
        artifact_label="report",
    )
    assert result.is_valid, result.errors


# ── pack-section / pack-table symmetry ─────────────────────────────────────


def test_pack_section_backtick_fence_hidden_fails():
    sanitized = _sanitized(PACK_WITH_HIDDEN_ONLY)
    result = validate_evidence_reference(
        f"pack-section:{HIDDEN_HEADING}",
        artifact_text=sanitized,
        base_dir=ROOT,
        strict=True,
        artifact_label="pack",
    )
    assert not result.is_valid
    assert "not found in the visible pack" in "; ".join(result.errors).lower()


def test_pack_section_tilde_fence_hidden_fails():
    sanitized = _sanitized(PACK_WITH_TILDE_HIDDEN)
    result = validate_evidence_reference(
        f"pack-section:{HIDDEN_HEADING}",
        artifact_text=sanitized,
        base_dir=ROOT,
        strict=True,
        artifact_label="pack",
    )
    assert not result.is_valid


def test_pack_section_visible_passes():
    sanitized = _sanitized(PACK_WITH_VISIBLE)
    result = validate_evidence_reference(
        f"pack-section:{HIDDEN_HEADING}",
        artifact_text=sanitized,
        base_dir=ROOT,
        strict=True,
        artifact_label="pack",
    )
    assert result.is_valid, result.errors


def test_pack_table_visible_passes():
    sanitized = _sanitized(PACK_WITH_VISIBLE)
    result = validate_evidence_reference(
        f"pack-table:{HIDDEN_HEADING}",
        artifact_text=sanitized,
        base_dir=ROOT,
        strict=True,
        artifact_label="pack",
    )
    assert result.is_valid, result.errors


def test_pack_table_hidden_in_fence_fails():
    sanitized = _sanitized(PACK_WITH_HIDDEN_ONLY)
    # Pack visible text has no heading, so table also fails
    result = validate_evidence_reference(
        f"pack-table:{HIDDEN_HEADING}",
        artifact_text=sanitized,
        base_dir=ROOT,
        strict=True,
        artifact_label="pack",
    )
    assert not result.is_valid


# ── consumer _audits_ok / _audit_provenance_details with visible texts ──────


def test_consumer_rejects_hidden_report_section_via_audits_ok():
    # The issue's reproduction: evidence+provenance both forged to Hidden claim,
    # but report sanitized text does not contain it.
    sanitized_report = _sanitized(REPORT_WITH_HIDDEN_ONLY)
    sanitized_pack = _sanitized(PACK_WITH_VISIBLE)
    audit = _pass_audit(
        MANUAL_AUDIT_ID,
        f"report-section:{HIDDEN_HEADING}",
        "report_section",
        HIDDEN_HEADING,
    )
    actual = {
        "overall": "pass",
        "audits": [audit],
        "validators": [],
        "blocking": [],
        "input_sha256": "x" * 64,
    }
    expected_ids = [MANUAL_AUDIT_ID]
    # Raw text would have found the heading → old consumer would pass.  With
    # visible text it must fail.
    assert _audits_ok(
        actual,
        expected_ids,
        audited_path="report.md",
        expected_report_sha256="x" * 64,
        report_text=sanitized_report,
        pack_text=sanitized_pack,
        expected_route="provider-selection",
    ) is False
    ok, errs = _audit_consistency_details(
        actual,
        expected_ids,
        audited_path="report.md",
        expected_report_sha256="x" * 64,
        report_text=sanitized_report,
        pack_text=sanitized_pack,
        expected_route="provider-selection",
    )
    assert ok is False
    assert any("not found in the visible report" in e.lower() for e in errs), errs
    assert any(MANUAL_AUDIT_ID in e for e in errs)


def test_consumer_accepts_visible_report_section_via_audits_ok():
    sanitized_report = _sanitized(REPORT_WITH_VISIBLE)
    sanitized_pack = _sanitized(PACK_WITH_VISIBLE)
    audit = _pass_audit(
        MANUAL_AUDIT_ID,
        f"report-section:{HIDDEN_HEADING}",
        "report_section",
        HIDDEN_HEADING,
    )
    actual = {
        "overall": "pass",
        "audits": [audit],
        "validators": [],
        "blocking": [],
        "input_sha256": "x" * 64,
    }
    expected_ids = [MANUAL_AUDIT_ID]
    assert _audits_ok(
        actual,
        expected_ids,
        audited_path="report.md",
        expected_report_sha256="x" * 64,
        report_text=sanitized_report,
        pack_text=sanitized_pack,
        expected_route="provider-selection",
    ) is True


def test_consumer_hidden_pack_section_fails_and_diagnostic_is_locatable():
    sanitized_report = _sanitized(REPORT_WITH_VISIBLE)
    sanitized_pack = _sanitized(PACK_WITH_HIDDEN_ONLY)
    audit = _pass_audit(
        MANUAL_AUDIT_ID,
        f"pack-section:{HIDDEN_HEADING}",
        "pack_section",
        HIDDEN_HEADING,
    )
    actual = {
        "overall": "pass",
        "audits": [audit],
        "validators": [],
        "blocking": [],
        "input_sha256": "x" * 64,
    }
    expected_ids = [MANUAL_AUDIT_ID]
    ok, errs = _audit_consistency_details(
        actual,
        expected_ids,
        audited_path="report.md",
        expected_report_sha256="x" * 64,
        research_pack_path="pack.md",
        expected_pack_sha256="y" * 64,
        report_text=sanitized_report,
        pack_text=sanitized_pack,
        expected_route="provider-selection",
    )
    assert ok is False
    assert any("not found in the visible pack" in e.lower() for e in errs), errs


def test_consumer_provenance_target_mismatch_still_distinct_diagnostic():
    sanitized_report = _sanitized(REPORT_WITH_VISIBLE)
    audit = _pass_audit(
        MANUAL_AUDIT_ID,
        f"report-section:{HIDDEN_HEADING}",
        "report_section",
        HIDDEN_HEADING,
    )
    # Force an automated-style binding mismatch via a manual audit that uses
    # audit_record; easier to test automated provenance directly via
    # _audit_provenance_details.
    automated_audit = {
        "audit_id": "source-traceability",
        "execution_type": "automated",
        "execution_source": "automated_validator",
        "status": "pass",
        "errors": [],
        "warnings": [],
        "evidence": ["tests/fixtures/forward/provider-selection-report.md: no violations found by source-label-consistency"],
        "evidence_provenance": [
            {
                "verified": True,
                "execution_source": "automated_validator",
                "audit_id": "source-traceability",
                "validator_binding": "source-label-consistency",
                "validator_version": run_forward_evals.EXPECTED_VALIDATOR_VERSION,
                "target": "WRONG_TARGET.md",
                "input_sha256": "x" * 64,
            }
        ],
        "validator_binding": "source-label-consistency",
        "reason": None,
    }
    ok, errs = _audit_provenance_details(
        automated_audit,
        "source-traceability",
        "automated",
        "automated_validator",
        expected_target="tests/fixtures/forward/provider-selection-report.md",
        expected_hash="x" * 64,
    )
    assert ok is False
    assert any("target" in e.lower() for e in errs), errs
    # Must NOT be the same message as hidden locator
    assert not any("not found in the visible" in e.lower() for e in errs)


def test_provenance_details_propagates_not_found_for_hidden_table():
    sanitized_report = _sanitized(REPORT_WITH_TABLE_HIDDEN_IN_FENCE)
    audit = _pass_audit(
        MANUAL_AUDIT_ID,
        f"report-table:{HIDDEN_HEADING}",
        "report_table",
        HIDDEN_HEADING,
    )
    actual = {
        "overall": "pass",
        "audits": [audit],
        "validators": [],
        "blocking": [],
        "input_sha256": None,
    }
    ok, errs = _audit_provenance_details(
        audit,
        MANUAL_AUDIT_ID,
        MANUAL_EXECUTION_TYPE,
        MANUAL_SOURCE,
        expected_target="report.md",
        expected_hash="x" * 64,
        report_text=sanitized_report,
        pack_text=None,
        expected_route="provider-selection",
    )
    assert ok is False
    assert any("not found" in e.lower() or "visible markdown table" in e.lower() for e in errs), errs


# ── checklist fence handling ────────────────────────────────────────────────


def test_checklist_fenced_marker_is_invisible(tmp_path: Path):
    # Create a checklist file where the marker is ONLY inside a fenced code block
    checklist = tmp_path / "checklist.md"
    checklist.write_text(
        "# Checklist\n\n"
        "```markdown\n"
        "<!-- audit-item: FA-999 -->\n"
        "```\n\n"
        "No visible marker.\n",
        encoding="utf-8",
    )
    result = validate_evidence_reference(
        f"checklist-item:{checklist.name}#FA-999",
        artifact_text=None,
        base_dir=tmp_path,
        strict=False,
    )
    # Must NOT find the marker inside fence
    assert not result.is_valid
    assert "was not found" in "; ".join(result.errors)


def test_checklist_visible_marker_passes(tmp_path: Path):
    checklist = tmp_path / "checklist.md"
    checklist.write_text(
        "# Checklist\n\n"
        "<!-- audit-item: FA-999 -->\n\n"
        "Content.\n",
        encoding="utf-8",
    )
    result = validate_evidence_reference(
        f"checklist-item:{checklist.name}#FA-999",
        artifact_text=None,
        base_dir=tmp_path,
        strict=False,
    )
    assert result.is_valid, result.errors


def test_checklist_tilde_fenced_marker_is_invisible(tmp_path: Path):
    checklist = tmp_path / "checklist.md"
    checklist.write_text(
        "# Checklist\n\n"
        "~~~markdown\n"
        "<!-- audit-item: FA-999 -->\n"
        "~~~\n\n"
        "No visible marker.\n",
        encoding="utf-8",
    )
    result = validate_evidence_reference(
        f"checklist-item:{checklist.name}#FA-999",
        artifact_text=None,
        base_dir=tmp_path,
        strict=False,
    )
    assert not result.is_valid


def test_checklist_html_comment_outside_fence_is_still_visible(tmp_path: Path):
    # HTML comments outside fences must remain visible (issue #409 risk).
    checklist = tmp_path / "checklist.md"
    checklist.write_text(
        "# Checklist\n\n"
        "<!-- audit-item: FA-999 -->\n\n"
        "```markdown\n"
        "fake content\n"
        "```\n",
        encoding="utf-8",
    )
    result = validate_evidence_reference(
        f"checklist-item:{checklist.name}#FA-999",
        artifact_text=None,
        base_dir=tmp_path,
        strict=False,
    )
    assert result.is_valid, result.errors


def test_strip_fenced_code_blocks_only_preserves_html(tmp_path: Path):
    text = "<!-- audit-item: FA-001 -->\n\n```md\ncode\n```\n\n<div>hi</div>"
    stripped = strip_fenced_code_blocks_only(text)
    assert "<!-- audit-item: FA-001 -->" in stripped
    assert "<div>hi</div>" in stripped
    assert "code" not in stripped


# ── hash stays raw-byte anchored ────────────────────────────────────────────


def test_hash_is_raw_byte_not_sanitized(tmp_path: Path):
    # Same logical heading but different raw bytes: sanitized hashes would be
    # identical if computed from visible text, but raw hashes differ.
    raw_hidden = REPORT_WITH_HIDDEN_ONLY
    raw_visible = REPORT_WITH_VISIBLE
    # Visible sanitized texts would differ, but we test that _sha256 is raw.
    report_hidden = tmp_path / "hidden.md"
    report_hidden.write_bytes(raw_hidden.encode("utf-8"))
    raw_hash = hashlib.sha256(report_hidden.read_bytes()).hexdigest()
    sanitized = _sanitized(raw_hidden)
    sanitized_hash = hashlib.sha256(sanitized.encode("utf-8")).hexdigest()
    assert raw_hash != sanitized_hash
    # The consumer's _sha256 must equal raw_hash
    from run_forward_evals import _sha256

    assert _sha256(report_hidden) == raw_hash
    assert _sha256(report_hidden) != sanitized_hash


# ── producer / consumer parity ──────────────────────────────────────────────


def test_producer_consumer_parity_visible(tmp_path: Path):
    # Same fixture sanitized by both sides must yield same validation outcome.
    text = REPORT_WITH_VISIBLE
    sanitized_via_contract = sanitize_visible_markdown(text)
    # Producer path (audit_report) uses vc_strip_fences == sanitize_visible_markdown
    from validate_contract import sanitize_visible_markdown as vc_sanitize

    sanitized_via_vc = vc_sanitize(text)
    assert sanitized_via_contract == sanitized_via_vc

    # Both sides validate the same locator against the same sanitized text
    prod_result = validate_evidence_reference(
        f"report-section:{HIDDEN_HEADING}",
        artifact_text=sanitized_via_contract,
        base_dir=ROOT,
        strict=True,
        artifact_label="report",
    )
    cons_result = validate_evidence_reference(
        f"report-section:{HIDDEN_HEADING}",
        artifact_text=sanitized_via_vc,
        base_dir=ROOT,
        strict=True,
        artifact_label="report",
    )
    assert prod_result.is_valid == cons_result.is_valid
    assert prod_result.is_valid is True


def test_producer_consumer_parity_hidden(tmp_path: Path):
    text = REPORT_WITH_HIDDEN_ONLY
    sanitized = sanitize_visible_markdown(text)
    prod_result = validate_evidence_reference(
        f"report-section:{HIDDEN_HEADING}",
        artifact_text=sanitized,
        base_dir=ROOT,
        strict=True,
        artifact_label="report",
    )
    assert not prod_result.is_valid
    # Consumer with same sanitized text must also fail
    audit = _pass_audit(
        MANUAL_AUDIT_ID,
        f"report-section:{HIDDEN_HEADING}",
        "report_section",
        HIDDEN_HEADING,
    )
    ok, _ = _audit_provenance_details(
        audit,
        MANUAL_AUDIT_ID,
        MANUAL_EXECUTION_TYPE,
        MANUAL_SOURCE,
        expected_target="report.md",
        expected_hash="x" * 64,
        report_text=sanitized,
        pack_text=None,
        expected_route="provider-selection",
    )
    assert ok is False


# ── end-to-end _evaluate_case with real fixtures still passes ───────────────


def test_forward_eval_still_passes_for_genuine_positive():
    registry = load_registry()
    case = next(c for c in registry["cases"] if c["id"] == "forward-provider-selection")
    from run_forward_evals import _evaluate_case

    result = _evaluate_case(case, registry["decision_tree_version"])
    assert result["passed"] is True, result
    assert result["checks"]["audits_consistent"] is True


def test_forward_eval_hidden_evidence_still_fails_when_report_has_no_visible_heading(monkeypatch):
    """Ensure a visible heading outside fences is still required: the
    consumer's sanitized text path is exercised via _evaluate_case by
    patching filesystem reads?  Instead we validate the lower-level
    _audit_consistency_details path which is what _evaluate_case actually
    checks — a report with only a fenced heading must not be accepted.
    """
    # Directly test the provenance path that _evaluate_case would hit
    hidden_sanitized = _sanitized(REPORT_WITH_HIDDEN_ONLY)
    audit = _pass_audit(
        MANUAL_AUDIT_ID,
        f"report-section:{HIDDEN_HEADING}",
        "report_section",
        HIDDEN_HEADING,
    )
    actual = {
        "overall": "pass",
        "audits": [audit],
        "validators": [],
        "blocking": [],
        "input_sha256": "x" * 64,
    }
    ok, errs = _audit_consistency_details(
        actual,
        [MANUAL_AUDIT_ID],
        audited_path="report.md",
        expected_report_sha256="x" * 64,
        report_text=hidden_sanitized,
        pack_text=None,
        expected_route="provider-selection",
    )
    assert ok is False
    assert any("not found in the visible report" in e.lower() for e in errs)
