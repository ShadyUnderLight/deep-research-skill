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

# Dynamic sys.path setup is intentional for direct script-module tests.
# ruff: noqa: E402

import copy
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from audit_evidence import validate_evidence_reference  # noqa: E402
from validate_contract import (
    sanitize_checklist_visible_markdown,
    sanitize_visible_markdown,
)  # noqa: E402

import run_forward_evals  # noqa: E402
from run_forward_evals import (
    _audit_consistency_details,
    _audit_provenance_details,
    _audits_ok,
    load_registry,
)  # noqa: E402

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
        report_text=sanitized_report,
        pack_text=sanitized_pack,
        expected_route="provider-selection",
    ) is False
    ok, errs = _audit_consistency_details(
        actual,
        expected_ids,
        audited_path="report.md",
        report_text=sanitized_report,
        pack_text=sanitized_pack,
        expected_route="provider-selection",
    )
    assert ok is False
    assert any("not found in the visible report" in e.lower() for e in errs), errs
    assert any(MANUAL_AUDIT_ID in e for e in errs)


def test_consumer_sanitizes_raw_text_at_audits_ok_boundary():
    """The helper must stay fail-closed even when callers pass raw Markdown."""
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
    raw_report = REPORT_WITH_HIDDEN_ONLY
    raw_pack = PACK_WITH_VISIBLE
    assert _audits_ok(
        actual,
        [MANUAL_AUDIT_ID],
        audited_path="report.md",
        research_pack_path="pack.md",
        report_text=raw_report,
        pack_text=raw_pack,
        expected_route="provider-selection",
    ) is False


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
        research_pack_path="pack.md",
        report_text=sanitized_report,
        pack_text=sanitized_pack,
        expected_route="provider-selection",
    )
    assert ok is False
    assert any("not found in the visible pack" in e.lower() for e in errs), errs


def test_consumer_provenance_target_mismatch_still_distinct_diagnostic():
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
    ok, errs = _audit_provenance_details(
        audit,
        MANUAL_AUDIT_ID,
        MANUAL_EXECUTION_TYPE,
        MANUAL_SOURCE,
        expected_target="report.md",
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


def test_checklist_html_comment_inside_raw_html_block_is_invisible(tmp_path: Path):
    checklist = tmp_path / "checklist.md"
    checklist.write_text(
        "<div>\n"
        "<!-- audit-item: FA-999 -->\n"
        "</div>\n\n"
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
    assert "was not found" in "; ".join(result.errors)


def test_checklist_inline_html_comment_marker_is_invisible(tmp_path: Path):
    checklist = tmp_path / "checklist.md"
    checklist.write_text(
        "Some explanation <!-- audit-item: FA-999 --> not a marker.\n",
        encoding="utf-8",
    )
    result = validate_evidence_reference(
        f"checklist-item:{checklist.name}#FA-999",
        artifact_text=None,
        base_dir=tmp_path,
        strict=False,
    )
    assert not result.is_valid


def test_checklist_inline_code_marker_is_invisible(tmp_path: Path):
    checklist = tmp_path / "checklist.md"
    checklist.write_text(
        "`<!-- audit-item: FA-999 -->`\n",
        encoding="utf-8",
    )
    result = validate_evidence_reference(
        f"checklist-item:{checklist.name}#FA-999",
        artifact_text=None,
        base_dir=tmp_path,
        strict=False,
    )
    assert not result.is_valid


def test_checklist_indented_code_marker_is_invisible(tmp_path: Path):
    checklist = tmp_path / "checklist.md"
    checklist.write_text(
        "    <!-- audit-item: FA-999 -->\n",
        encoding="utf-8",
    )
    result = validate_evidence_reference(
        f"checklist-item:{checklist.name}#FA-999",
        artifact_text=None,
        base_dir=tmp_path,
        strict=False,
    )
    assert not result.is_valid


def test_strict_audit_record_rejects_non_top_level_checklist_marker(tmp_path: Path):
    checklist = tmp_path / "checklist.md"
    checklist.write_text(
        "`<!-- audit-item: FA-999 -->`\n",
        encoding="utf-8",
    )
    record = tmp_path / "audit-record.json"
    record.write_text(
        json.dumps(
            {
                "records": [
                    {
                        "record_id": "manual-001",
                        "recorded_at": "2026-08-18T10:00:00Z",
                        "audit_id": "market-outlook-audit",
                        "status": "passed",
                        "artifact_id": "test-artifact-a",
                        "executed_at": "2026-08-18T10:00:00Z",
                        "execution_source": "manual_checklist_attestation",
                        "evidence": "checklist-item:checklist.md#FA-999",
                        "route": "market-outlook",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    result = validate_evidence_reference(
        "audit-record:audit-record.json#manual-001@2026-08-18T10:00:00Z",
        base_dir=tmp_path,
        strict=True,
        expected_audit_id="market-outlook-audit",
        expected_artifact_id="test-artifact-a",
        expected_route="market-outlook",
    )
    assert not result.is_valid
    assert any("checklist item" in error.lower() for error in result.errors)


def test_checklist_sanitizer_removes_raw_html_but_keeps_top_level_marker(tmp_path: Path):
    text = "<!-- audit-item: FA-001 -->\n\n```md\ncode\n```\n\n<div>hi</div>"
    stripped = sanitize_checklist_visible_markdown(text)
    assert "<!-- audit-item: FA-001 -->" in stripped
    assert "<div>hi</div>" not in stripped
    assert "code" not in stripped


# ── producer / consumer parity (issue #426: no byte hashing; visible text only) ──

# ── producer / consumer parity ──────────────────────────────────────────────


def test_producer_consumer_parity_visible():
    # Producer (audit_report) and consumer (run_forward_evals) must share the
    # exact same canonical sanitizer — not two copies.  Verify by exercising
    # both import paths that resolve to the same implementation.
    text = REPORT_WITH_VISIBLE
    # Consumer import path
    from validate_contract import sanitize_visible_markdown as consumer_sanitize

    # Producer import path (audit_report re-exports it as vc_strip_fences)
    from audit_report import vc_strip_fences as producer_sanitize

    sanitized_via_consumer = consumer_sanitize(text)
    sanitized_via_producer = producer_sanitize(text)
    assert sanitized_via_consumer == sanitized_via_producer

    # Both sides must agree on validation outcome via their respective paths
    prod_result = validate_evidence_reference(
        f"report-section:{HIDDEN_HEADING}",
        artifact_text=sanitized_via_producer,
        base_dir=ROOT,
        strict=True,
        artifact_label="report",
    )
    # Consumer validates through _audit_provenance_details (which calls
    # validate_evidence_reference on the sanitized text)
    audit = _pass_audit(
        MANUAL_AUDIT_ID,
        f"report-section:{HIDDEN_HEADING}",
        "report_section",
        HIDDEN_HEADING,
    )
    cons_ok, _ = _audit_provenance_details(
        audit,
        MANUAL_AUDIT_ID,
        MANUAL_EXECUTION_TYPE,
        MANUAL_SOURCE,
        expected_target="report.md",
        report_text=sanitized_via_consumer,
        pack_text=None,
        expected_route="provider-selection",
    )
    assert prod_result.is_valid is True
    assert cons_ok is True


def test_producer_consumer_parity_hidden():
    text = REPORT_WITH_HIDDEN_ONLY
    from validate_contract import sanitize_visible_markdown as consumer_sanitize
    from audit_report import vc_strip_fences as producer_sanitize

    sanitized_cons = consumer_sanitize(text)
    sanitized_prod = producer_sanitize(text)
    assert sanitized_cons == sanitized_prod
    prod_result = validate_evidence_reference(
        f"report-section:{HIDDEN_HEADING}",
        artifact_text=sanitized_prod,
        base_dir=ROOT,
        strict=True,
        artifact_label="report",
    )
    assert not prod_result.is_valid
    assert "not found in the visible report" in "; ".join(prod_result.errors).lower()
    audit = _pass_audit(
        MANUAL_AUDIT_ID,
        f"report-section:{HIDDEN_HEADING}",
        "report_section",
        HIDDEN_HEADING,
    )
    ok, errs = _audit_provenance_details(
        audit,
        MANUAL_AUDIT_ID,
        MANUAL_EXECUTION_TYPE,
        MANUAL_SOURCE,
        expected_target="report.md",
        report_text=sanitized_cons,
        pack_text=None,
        expected_route="provider-selection",
    )
    assert ok is False
    assert any("not found in the visible report" in e.lower() for e in errs)


# ── end-to-end _evaluate_case with real fixtures still passes ───────────────


def test_forward_eval_still_passes_for_genuine_positive():
    registry = load_registry()
    case = next(c for c in registry["cases"] if c["id"] == "forward-provider-selection")
    from run_forward_evals import _evaluate_case

    result = _evaluate_case(case, registry["decision_tree_version"])
    assert result["passed"] is True, result
    assert result["checks"]["audits_consistent"] is True


def test_forward_eval_hidden_evidence_still_fails_when_report_has_no_visible_heading():
    """Lower-level check: a report with only a fenced heading must not be
    accepted via _audit_consistency_details (sanitized text does not contain it)."""
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
        report_text=hidden_sanitized,
        pack_text=None,
        expected_route="provider-selection",
    )
    assert ok is False
    assert any("not found in the visible report" in e.lower() for e in errs)


def test_evaluate_case_wiring_rejects_hidden_report_section_e2e(tmp_path, monkeypatch):
    """True e2e wiring test for #409: _evaluate_case must sanitize the
    on-disk report before re-validating evidence.  A heading that only
    exists inside a fenced code block (and a tilde fence variant) must
    cause the consumer to fail even when evidence+provenance are
    self-consistent.  If the sanitizer wiring in _evaluate_case were
    removed, this test would green-light a forged hidden locator."""
    # Write tmp report with hidden heading only inside fence, and a pack
    report = tmp_path / "report.md"
    report.write_text(REPORT_WITH_HIDDEN_ONLY, encoding="utf-8")
    pack = tmp_path / "pack.md"
    pack.write_text(PACK_WITH_VISIBLE, encoding="utf-8")

    registry = load_registry()
    base_case = next(c for c in registry["cases"] if c["id"] == "forward-provider-selection")
    case = copy.deepcopy(base_case)
    # Absolute tmp paths: ROOT / absolute == absolute, so _evaluate_case will
    # compute hashes from the tmp files and sanitize their contents.
    case["fixtures"]["report"] = str(report)
    case["fixtures"]["research_pack"] = str(pack)

    # Forge an audit JSON that claims the hidden heading is valid
    real_report = ROOT / base_case["fixtures"]["report"]
    real_pack = ROOT / base_case["fixtures"]["research_pack"]
    real_data, _, _ = run_forward_evals._run_audit(real_report, real_pack)
    assert real_data is not None
    tampered = copy.deepcopy(real_data)
    for a in tampered["audits"]:
        if a["audit_id"] == MANUAL_AUDIT_ID:
            a["status"] = "pass"
            a["errors"] = []
            a["warnings"] = []
            a["reason"] = None
            a["evidence"] = [f"report-section:{HIDDEN_HEADING}"]
            a["evidence_provenance"] = [
                {"verified": True, "execution_source": MANUAL_SOURCE, "kind": "report_section", "locator": HIDDEN_HEADING}
            ]
            a["execution_source"] = MANUAL_SOURCE
            a["execution_type"] = "manual"
    tampered["overall"] = "pass"
    # Make validator hashes match the tmp files so validators_ok does not mask
    # the provenance failure (we want to isolate the visible-heading check)
    tmp_report_hash = hashlib.sha256(report.read_bytes()).hexdigest()
    tmp_pack_hash = hashlib.sha256(pack.read_bytes()).hexdigest()
    tampered["input_sha256"] = tmp_report_hash
    for v in tampered.get("validators", []):
        # report-targeted validators should match tmp report hash; pack is not a validator target
        if v.get("target") == str(real_report):
            v["target"] = str(report)
            v["input_sha256"] = tmp_report_hash
            v["validator_version"] = run_forward_evals.EXPECTED_VALIDATOR_VERSION
        elif v.get("target") == str(real_pack):
            v["target"] = str(pack)
            v["input_sha256"] = tmp_pack_hash
    for a in tampered["audits"]:
        if a["audit_id"] == "research-pack":
            for p in a.get("evidence_provenance", []):
                if p.get("target") == str(real_pack):
                    p["target"] = str(pack)
                    p["input_sha256"] = tmp_pack_hash
        elif a["audit_id"] != MANUAL_AUDIT_ID:
            for p in a.get("evidence_provenance", []):
                # automated provenance should bind to tmp report
                if p.get("target") == str(real_report):
                    p["target"] = str(report)
                    p["input_sha256"] = tmp_report_hash

    def fake_run(rp, pp, activation_snapshot=None):
        return tampered, None, 0

    monkeypatch.setattr(run_forward_evals, "_run_audit", fake_run)
    result = run_forward_evals._evaluate_case(case, registry["decision_tree_version"])
    assert result["passed"] is False
    assert result["checks"]["audits_consistent"] is False
    assert any("not found in the visible report" in e.lower() for e in result["checks"]["audit_consistency_errors"]), result["checks"]["audit_consistency_errors"]
    # Hash must stay raw — the computed hash is the raw file hash, not the sanitized one
    assert hashlib.sha256(report.read_bytes()).hexdigest() != hashlib.sha256(sanitize_visible_markdown(REPORT_WITH_HIDDEN_ONLY).encode()).hexdigest()


def test_evaluate_case_wiring_rejects_hidden_tilde_and_html_e2e(tmp_path, monkeypatch):
    """Same wiring test for tilde fence and raw HTML hidden headings — the
    sanitizer must handle both CommonMark fence types and HTML blocks."""
    for hidden_text in (REPORT_WITH_HIDDEN_TILDE, REPORT_WITH_HTML_HIDDEN):
        report = tmp_path / "report.md"
        report.write_text(hidden_text, encoding="utf-8")
        pack = tmp_path / "pack.md"
        pack.write_text(PACK_WITH_VISIBLE, encoding="utf-8")
        registry = load_registry()
        base_case = next(c for c in registry["cases"] if c["id"] == "forward-provider-selection")
        case = copy.deepcopy(base_case)
        case["fixtures"]["report"] = str(report)
        case["fixtures"]["research_pack"] = str(pack)
        real_report = ROOT / base_case["fixtures"]["report"]
        real_pack = ROOT / base_case["fixtures"]["research_pack"]
        real_data, _, _ = run_forward_evals._run_audit(real_report, real_pack)
        tampered = copy.deepcopy(real_data)
        for a in tampered["audits"]:
            if a["audit_id"] == MANUAL_AUDIT_ID:
                a["status"] = "pass"
                a["errors"] = []
                a["warnings"] = []
                a["reason"] = None
                a["evidence"] = [f"report-section:{HIDDEN_HEADING}"]
                a["evidence_provenance"] = [
                    {"verified": True, "execution_source": MANUAL_SOURCE, "kind": "report_section", "locator": HIDDEN_HEADING}
                ]
                a["execution_source"] = MANUAL_SOURCE
                a["execution_type"] = "manual"
        tampered["overall"] = "pass"
        tmp_report_hash = hashlib.sha256(report.read_bytes()).hexdigest()
        tmp_pack_hash = hashlib.sha256(pack.read_bytes()).hexdigest()
        tampered["input_sha256"] = tmp_report_hash
        for v in tampered.get("validators", []):
            if v.get("target") == str(real_report):
                v["target"] = str(report)
                v["input_sha256"] = tmp_report_hash
            elif v.get("target") == str(real_pack):
                v["target"] = str(pack)
                v["input_sha256"] = tmp_pack_hash
        for a in tampered["audits"]:
            if a["audit_id"] == "research-pack":
                for p in a.get("evidence_provenance", []):
                    if p.get("target") == str(real_pack):
                        p["target"] = str(pack)
                        p["input_sha256"] = tmp_pack_hash
            elif a["audit_id"] != MANUAL_AUDIT_ID:
                for p in a.get("evidence_provenance", []):
                    if p.get("target") == str(real_report):
                        p["target"] = str(report)
                        p["input_sha256"] = tmp_report_hash

        def fake_run(rp, pp, activation_snapshot=None, _tampered=tampered):
            return _tampered, None, 0

        monkeypatch.setattr(run_forward_evals, "_run_audit", fake_run)
        result = run_forward_evals._evaluate_case(case, registry["decision_tree_version"])
        assert result["passed"] is False, hidden_text[:50]
        assert any("not found in the visible report" in e.lower() for e in result["checks"]["audit_consistency_errors"]), result["checks"]["audit_consistency_errors"]


def test_checklist_sanitizer_import_failure_is_fail_closed(monkeypatch, tmp_path):
    """P1: if the canonical fence sanitizer cannot be loaded, checklist
    validation must fail closed, not fall back to raw text (which would
    accept a fenced marker)."""
    checklist = tmp_path / "checklist.md"
    checklist.write_text("# Checklist\n\n```markdown\n<!-- audit-item: FA-999 -->\n```\n\nNo visible marker.\n", encoding="utf-8")
    # Force the lazy import to fail
    import builtins

    real_import = builtins.__import__

    def fake_import(name, *args, **kwargs):
        if name == "validate_contract":
            raise ImportError("simulated missing sanitizer")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", fake_import)
    result = validate_evidence_reference(
        f"checklist-item:{checklist.name}#FA-999",
        artifact_text=None,
        base_dir=tmp_path,
        strict=False,
    )
    assert not result.is_valid
    assert "cannot load canonical fence sanitizer" in "; ".join(result.errors).lower()
