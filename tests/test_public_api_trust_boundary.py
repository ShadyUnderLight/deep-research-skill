"""Public API trust boundary — external caller cannot mint trusted evidence.

This target deliberately imports ONLY the public API (no ``_validate_*`` internals,
no ``@testable`` equivalent).  It verifies that ``validate_evidence_reference``
— the public constructor analog to ``SnapshotSectionCoverage.init`` — never
produces ``verified=True`` for a locator that only exists inside a fenced code
block or raw HTML container, even when the caller passes the *raw* Markdown
text directly.  Internal trusted paths (audit_report's already-sanitized
``visible_text`` and load-time revalidation via audit-record) remain the only
ways to obtain trusted provenance.

Analog to the Swift fix:
  public SnapshotSectionCoverage(...)  // never .trusted
  internal SnapshotSectionCoverage.moduleIssued(...)  // .trusted
  internal SnapshotSectionCoverage.revalidated(...)    // .trusted (load-time)

Here:
  public  validate_evidence_reference(artifact_text=raw)  // always sanitizes -> pending
  internal audit_report._execute_required_audits(visible_text) // already sanitized
  internal run_forward_evals._audit_provenance_details(sanitized) // double-checked
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

# Public API only — this is the intentional trust boundary.
from audit_evidence import EvidenceValidation, validate_evidence_reference
from validate_contract import sanitize_visible_markdown

HIDDEN = "Hidden claim"

REPORT_FENCE_BACKTICK = f"""# Report

```markdown
## {HIDDEN}
Inside backtick fence
```

No visible heading.
"""

REPORT_FENCE_TILDE = f"""# Report

~~~markdown
## {HIDDEN}
Inside tilde fence
~~~

No visible heading.
"""

REPORT_UNCLOSED = f"""# Report

```markdown
## {HIDDEN}
Unclosed fence — rest of file is code.
Still inside.
"""

REPORT_HTML = f"""# Report

<div>
## {HIDDEN}
Inside raw HTML block
</div>

No visible heading.
"""

REPORT_NESTED = f"""# Report

````markdown
```markdown
## {HIDDEN}
Inner should not close outer
```
Still inside outer.
````

No visible heading.
"""

REPORT_VISIBLE = f"""# Report

## {HIDDEN}

Visible content.

| h | v |
|---|---|
| a | b |
"""

REPORT_TABLE_HIDDEN = f"""# Report

```markdown
## {HIDDEN}

| h1 | h2 |
|---|---|
| v1 | v2 |
```
"""

REPORT_TABLE_VISIBLE = f"""# Report

## {HIDDEN}

| h1 | h2 |
|---|---|
| v1 | v2 |
"""

PACK_FENCE = f"""# Pack

```markdown
## {HIDDEN}
Hidden pack
```

No visible pack heading.
"""

PACK_VISIBLE = f"""# Pack

## {HIDDEN}

| h1 | h2 |
|---|---|
| v1 | v2 |
"""


# ── Public API must reject hidden locators even when given raw text ──────────


def test_public_raw_backtick_hidden_fails():
    # External module passes raw Markdown that contains the heading only inside a fence.
    # Public validate_evidence_reference must internally sanitize and return not valid.
    result = validate_evidence_reference(
        f"report-section:{HIDDEN}",
        artifact_text=REPORT_FENCE_BACKTICK,
        strict=True,
        artifact_label="report",
    )
    assert not result.is_valid
    assert "not found in the visible report" in "; ".join(result.errors).lower()


def test_public_raw_tilde_hidden_fails():
    result = validate_evidence_reference(
        f"report-section:{HIDDEN}",
        artifact_text=REPORT_FENCE_TILDE,
        strict=True,
        artifact_label="report",
    )
    assert not result.is_valid
    assert "not found in the visible report" in "; ".join(result.errors).lower()


def test_public_raw_unclosed_fence_hidden_fails():
    result = validate_evidence_reference(
        f"report-section:{HIDDEN}",
        artifact_text=REPORT_UNCLOSED,
        strict=True,
        artifact_label="report",
    )
    assert not result.is_valid


def test_public_raw_html_hidden_fails():
    result = validate_evidence_reference(
        f"report-section:{HIDDEN}",
        artifact_text=REPORT_HTML,
        strict=True,
        artifact_label="report",
    )
    assert not result.is_valid
    assert "not found in the visible report" in "; ".join(result.errors).lower()


def test_public_raw_nested_fence_hidden_fails():
    result = validate_evidence_reference(
        f"report-section:{HIDDEN}",
        artifact_text=REPORT_NESTED,
        strict=True,
        artifact_label="report",
    )
    assert not result.is_valid


def test_public_raw_table_hidden_fails():
    result = validate_evidence_reference(
        f"report-table:{HIDDEN}",
        artifact_text=REPORT_TABLE_HIDDEN,
        strict=True,
        artifact_label="report",
    )
    assert not result.is_valid
    # Either heading not found or not a visible table
    err = "; ".join(result.errors).lower()
    assert "not found in the visible report" in err or "does not point to a visible markdown table" in err


def test_public_raw_visible_passes():
    # A truly visible heading must still pass when raw text is supplied —
    # public API sanitizes but visible content survives.
    result = validate_evidence_reference(
        f"report-section:{HIDDEN}",
        artifact_text=REPORT_VISIBLE,
        strict=True,
        artifact_label="report",
    )
    assert result.is_valid, result.errors
    assert result.provenance and result.provenance.get("verified") is True


def test_public_raw_visible_table_passes():
    result = validate_evidence_reference(
        f"report-table:{HIDDEN}",
        artifact_text=REPORT_TABLE_VISIBLE,
        strict=True,
        artifact_label="report",
    )
    assert result.is_valid, result.errors


def test_public_pack_raw_hidden_fails():
    result = validate_evidence_reference(
        f"pack-section:{HIDDEN}",
        artifact_text=PACK_FENCE,
        strict=True,
        artifact_label="pack",
    )
    assert not result.is_valid
    assert "not found in the visible pack" in "; ".join(result.errors).lower()


def test_public_pack_raw_visible_passes():
    result = validate_evidence_reference(
        f"pack-section:{HIDDEN}",
        artifact_text=PACK_VISIBLE,
        strict=True,
        artifact_label="pack",
    )
    assert result.is_valid, result.errors


def test_public_sanitized_input_also_passes():
    # Internal callers that already sanitize must not be broken by double-sanitization.
    sanitized = sanitize_visible_markdown(REPORT_VISIBLE)
    result = validate_evidence_reference(
        f"report-section:{HIDDEN}",
        artifact_text=sanitized,
        strict=True,
        artifact_label="report",
    )
    assert result.is_valid, result.errors


def test_public_sanitized_hidden_still_fails():
    sanitized = sanitize_visible_markdown(REPORT_FENCE_BACKTICK)
    result = validate_evidence_reference(
        f"report-section:{HIDDEN}",
        artifact_text=sanitized,
        strict=True,
        artifact_label="report",
    )
    assert not result.is_valid


# ── Direct EvidenceValidation construction cannot mint trust ─────────────────


def test_direct_evidence_validation_construction_not_trusted():
    # An external caller cannot simply construct EvidenceValidation(verified=True)
    # and have it accepted as trusted — the consumer re-validates via
    # validate_evidence_reference, not via object identity.  This test ensures
    # that direct construction doesn't bypass the visible check when re-validated.
    forged = EvidenceValidation(
        provenance={"kind": "report_section", "locator": HIDDEN, "verified": True},
        errors=(),
    )
    assert forged.is_valid  # the forged object itself looks valid
    # But the public validator, when given the raw hidden text, still fails:
    revalidated = validate_evidence_reference(
        f"report-section:{HIDDEN}",
        artifact_text=REPORT_FENCE_BACKTICK,
        strict=True,
        artifact_label="report",
    )
    assert not revalidated.is_valid
    assert forged.provenance != revalidated.provenance


# ── Audit-record nested evidence also respects visible boundary ──────────────


def test_public_audit_record_nested_hidden_report_fails(tmp_path: Path):
    # External caller tries to forge an audit-record whose nested evidence is a
    # hidden report-section. Strict audit-record validation must re-validate
    # the nested locator against visible report text and fail.
    report_path = tmp_path / "report.md"
    report_path.write_text(REPORT_FENCE_BACKTICK, encoding="utf-8")
    sha = "a" * 64
    record_file = tmp_path / "record.json"
    record_file.write_text(
        json.dumps(
            {
                "records": [
                    {
                        "record_id": "rec-001",
                        "recorded_at": "2026-08-14T00:00:00Z",
                        "audit_id": "option-selection-final-audit",
                        "status": "passed",
                        "artifact_sha256": sha,
                        "artifact_id": "test-artifact",
                        "executed_at": "2026-08-14T00:00:00Z",
                        "execution_source": "manual_checklist_attestation",
                        "evidence": f"report-section:{HIDDEN}",
                        "route": "provider-selection",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    locator = f"{record_file.name}#rec-001@2026-08-14T00:00:00Z"
    result = validate_evidence_reference(
        f"audit-record:{locator}",
        base_dir=tmp_path,
        strict=True,
        expected_audit_id="option-selection-final-audit",
        expected_artifact_sha256=sha,
        expected_route="provider-selection",
        execution_type="manual",
        artifact_text=REPORT_FENCE_BACKTICK,
        artifact_label="report",
        report_text=REPORT_FENCE_BACKTICK,
        pack_text=None,
    )
    assert not result.is_valid
    err = "; ".join(result.errors).lower()
    assert "not found in the visible report" in err or "not verifiable in report" in err


def test_public_audit_record_nested_visible_report_passes(tmp_path: Path):
    report_path = tmp_path / "report.md"
    report_path.write_text(REPORT_VISIBLE, encoding="utf-8")
    sha = "b" * 64
    record_file = tmp_path / "record.json"
    record_file.write_text(
        json.dumps(
            {
                "records": [
                    {
                        "record_id": "rec-002",
                        "recorded_at": "2026-08-14T01:00:00Z",
                        "audit_id": "option-selection-final-audit",
                        "status": "passed",
                        "artifact_sha256": sha,
                        "artifact_id": "test-artifact",
                        "executed_at": "2026-08-14T01:00:00Z",
                        "execution_source": "manual_checklist_attestation",
                        "evidence": f"report-section:{HIDDEN}",
                        "route": "provider-selection",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    locator = f"{record_file.name}#rec-002@2026-08-14T01:00:00Z"
    result = validate_evidence_reference(
        f"audit-record:{locator}",
        base_dir=tmp_path,
        strict=True,
        expected_audit_id="option-selection-final-audit",
        expected_artifact_sha256=sha,
        expected_route="provider-selection",
        execution_type="manual",
        artifact_text=REPORT_VISIBLE,
        artifact_label="report",
        report_text=REPORT_VISIBLE,
        pack_text=None,
    )
    assert result.is_valid, result.errors
    assert result.provenance and result.provenance.get("verified") is True


# ── Public API surface check — no runtimeTrust-like sink ─────────────────────


def test_public_api_has_no_runtime_trust_sink():
    # The public validate_evidence_reference must not expose a parameter that
    # directly mints trusted provenance (analogous to runtimeTrust: .trusted).
    # This is a compile-time / API-surface assertion: the function signature
    # must not contain a param that allows bypassing sanitization.
    import inspect

    sig = inspect.signature(validate_evidence_reference)
    forbidden = {"runtime_trust", "runtimeTrust", "verified", "trusted", "force_verified"}
    assert not (set(sig.parameters) & forbidden), f"public API must not expose trust sink: {set(sig.parameters) & forbidden}"
