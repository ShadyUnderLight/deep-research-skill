#!/usr/bin/env python3
"""Regression tests for validate_report_quality.py.

Each test creates a fixture, runs the validator as a subprocess,
and asserts the expected exit code.
"""

import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = str(Path(__file__).resolve().parent / "validate_report_quality.py")

# ── Minimal valid report (all required elements present) ─────────────────

MINIMAL_VALID = """\
## Route and audit status

**Primary route**: Provider / Vendor Selection

| Audit | Status | 证据 |
|-------|--------|------|
| source-traceability | ✅ Passed | §3 正文使用 [S01] 引用 |
| final-audit | ✅ Passed | §2 各关卡可追溯 |

## Findings

Body text with citation [S01].

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Example source | secondary | 2026-01-01 | https://example.com | medium | §2 |
"""

# ── Valid baseline (should pass all checks) ──────────────────────────────

VALID_REPORT = """\
# Test Report

## Route and audit status

**Primary route**: Provider / Vendor Selection

| Audit | Status | 证据 |
|-------|--------|------|
| source-traceability | ✅ Passed | §3-§5 正文使用 [S01] 引用 |
| final-audit | ✅ Passed | §2-§6 各核心关卡可追溯 |

## Market overview

The market is experiencing rapid growth driven by AI adoption [S01].

Companies are investing heavily in R&D to capture market share [S01][S02].

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Example market report | secondary | 2026-01-01 | https://example.com | medium | §3 |
| S02 | Industry filing | primary | 2026-02-01 | https://example.com/filing | high | §3 |
"""

# ── Shared-workflow baseline ─────────────────────────────────────────────

SHARED_WORKFLOW_REPORT = """\
# Test Report

## Route and audit status

**Route**: Shared-workflow (no specialized route selected)

| Audit | Status | 证据 |
|-------|--------|------|
| workflow-spine-audit | ✅ Passed | §2-§6 各工作流关卡在正文可追溯 |
| final-audit | ✅ Passed | 各核心关卡在正文有对应检查标记 |

## Findings

The analysis shows clear patterns [S01].

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Example source | secondary | 2026-01-15 | https://example.com | medium | §2 |
"""

# ── Helpers ──────────────────────────────────────────────────────────────


def run_validator(text: str, *args: str) -> subprocess.CompletedProcess:
    with tempfile.TemporaryDirectory() as d:
        path = Path(d) / "report.md"
        path.write_text(text, encoding="utf-8")
        return subprocess.run(
            [sys.executable, SCRIPT, str(path), *args],
            capture_output=True, text=True,
        )


def expect_pass(name: str, text: str, *args: str) -> None:
    result = run_validator(text, *args)
    assert result.returncode == 0, (
        f"{name}: expected pass (exit 0), got {result.returncode}\n"
        f"stdout: {result.stdout}\nstderr: {result.stderr}"
    )
    print(f"  PASS  {name}")


def expect_fail(name: str, text: str, expected_rc: int = 2, *args: str) -> None:
    result = run_validator(text, *args)
    assert result.returncode == expected_rc, (
        f"{name}: expected exit {expected_rc}, got {result.returncode}\n"
        f"stdout: {result.stdout}\nstderr: {result.stderr}"
    )
    print(f"  PASS  {name}")


# ── Tests ────────────────────────────────────────────────────────────────


def test_valid_report_passes() -> None:
    """Complete report with all required sections should pass."""
    expect_pass("valid report passes", VALID_REPORT)


def test_shared_workflow_passes() -> None:
    """Shared-workflow route format should pass."""
    expect_pass("shared-workflow passes", SHARED_WORKFLOW_REPORT)


def test_missing_route_audit_block_fails() -> None:
    """Report without ## Route and audit status should fail."""
    text = VALID_REPORT.replace("## Route and audit status", "## Missing heading")
    expect_fail("missing route/audit block fails", text)


def test_missing_route_declaration_fails() -> None:
    """Route and audit block without primary route / shared-workflow should fail."""
    text = """\
## Route and audit status

| Audit | Status | 证据 |
|-------|--------|------|
| source-traceability | ✅ Passed | §3 |

## Findings

Body text with citation [S01].

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Example | secondary | 2026-01-01 | https://example.com | medium | §2 |
"""
    expect_fail("missing route declaration fails", text)


def test_passed_row_empty_evidence_fails() -> None:
    """Passed audit row with empty evidence column should fail.
    Uses a fixture with all required elements to isolate the evidence check."""
    text = """\
## Route and audit status

**Primary route**: Provider / Vendor Selection

| Audit | Status | 证据 |
|-------|--------|------|
| source-traceability | ✅ Passed | |
| final-audit | ✅ Passed | §2-§6 各核心关卡可追溯 |

## Findings

Body text with citation [S01].

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Example | secondary | 2026-01-01 | https://example.com | medium | §2 |
"""
    expect_fail("passed row empty evidence fails", text)


def test_passed_row_vague_evidence_fails() -> None:
    """Passed audit row with vague evidence like '通过', '已检查', 'N/A', 'ok' should fail.
    Uses fixtures with all required elements to isolate the evidence check."""
    vague_values = ["通过", "已检查", "N/A", "ok", "OK", "已通过"]
    for vague in vague_values:
        text = f"""\
## Route and audit status

**Primary route**: Provider / Vendor Selection

| Audit | Status | 证据 |
|-------|--------|------|
| source-traceability | ✅ Passed | {vague} |
| final-audit | ✅ Passed | §2-§6 各核心关卡可追溯 |

## Findings

Body text with citation [S01].

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Example | secondary | 2026-01-01 | https://example.com | medium | §2 |
"""
        expect_fail(f"passed row vague evidence '{vague}' fails", text)


def test_missing_source_register_fails() -> None:
    """Report without ## Source Register should fail."""
    text = VALID_REPORT.replace("## Source Register", "## Bibliography")
    expect_fail("missing source register fails", text)


def test_source_register_wrong_columns_fails() -> None:
    """Source Register with fewer than 7 columns should fail."""
    text = VALID_REPORT.replace(
        "| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |",
        "| ID | Source Name | Source Type | Date | URL |",
    ).replace(
        "|----|-------------|-------------|------|---------|-------------|------------------|",
        "|----|-------------|-------------|------|------|",
    )
    expect_fail("source register wrong columns fails", text)


def test_zero_body_refs_fails() -> None:
    """Source Register exists but body has zero [Sxx] references should fail."""
    import re as _re
    text = _re.sub(r"\[S\d{2}\]", "(redacted)", VALID_REPORT)
    expect_fail("zero body refs fails", text)


def test_body_refs_outside_register_only_fails() -> None:
    """[Sxx] in Source Register 'Claims Supported' column must NOT count as body ref.
    This prevents false negatives: body has zero citations but register table includes [Sxx]."""
    text = """\
## Route and audit status

**Primary route**: Provider / Vendor Selection

| Audit | Status | 证据 |
|-------|--------|------|
| source-traceability | ✅ Passed | §2 已验证 |

## Findings

No source references in the actual body text.

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Example | secondary | 2026-01-01 | https://example.com | medium | §2 [S01] |
"""
    expect_fail("body refs in register only (not body) fails", text)


def test_passed_row_with_annotation_fails() -> None:
    """Passed row with parenthetical annotation and empty evidence must fail.
    AUDIT_PASSED_RE should not require $ anchor: '✅ Passed (via #3)' is still Passed."""
    text = """\
## Route and audit status

**Primary route**: Provider / Vendor Selection

| Audit | Status | 证据 |
|-------|--------|------|
| source-traceability | ✅ Passed (via checklist #3) | |
| final-audit | ✅ Passed | §2 各关卡可追溯 |

## Findings

Body text with citation [S01].

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Example | secondary | 2026-01-01 | https://example.com | medium | §2 |
"""
    expect_fail("annotated passed row with empty evidence fails", text)


def test_author_year_ref_passes() -> None:
    """Author-Year inline citation (Academic route) should pass format equivalence."""
    text = """\
## Route and audit status

**Primary route**: Academic / Literature Review

| Audit | Status | 证据 |
|-------|--------|------|
| source-traceability | ✅ Passed | 正文使用 Author-Year 引用 |
| final-audit | ✅ Passed | §2 可追溯 |

## Findings

The transformer architecture revolutionized NLP (Vaswani et al., 2017, NeurIPS).

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Vaswani et al. 2017 | secondary | 2017-06-12 | https://arxiv.org/abs/1706.03762 | high | §2 |
"""
    expect_pass("author-year ref passes", text)


def test_arxiv_id_ref_passes() -> None:
    """arXiv ID inline citation (Technical route) should pass format equivalence."""
    text = """\
## Route and audit status

**Primary route**: Technical Deep-dive

| Audit | Status | 证据 |
|-------|--------|------|
| source-traceability | ✅ Passed | 正文使用 arXiv ID 引用 |
| final-audit | ✅ Passed | §2 可追溯 |

## Findings

The architecture is described in arXiv:1706.03762.

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Attention is All You Need | secondary | 2017-06-12 | https://arxiv.org/abs/1706.03762 | high | §2 |
"""
    expect_pass("arxiv id ref passes", text)


def test_doi_ref_passes() -> None:
    """DOI inline citation should pass format equivalence."""
    text = """\
## Route and audit status

**Primary route**: Technical Deep-dive

| Audit | Status | 证据 |
|-------|--------|------|
| source-traceability | ✅ Passed | 正文使用 DOI 引用 |
| final-audit | ✅ Passed | §2 可追溯 |

## Findings

The findings are documented (doi:10.1038/s41586-023-06747-5).

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Nature paper 2023 | secondary | 2023-11-01 | https://doi.org/10.1038/s41586-023-06747-5 | high | §2 |
"""
    expect_pass("doi ref passes", text)


def test_natural_language_unique_ref_passes() -> None:
    """Natural language attribution that uniquely identifies source should pass."""
    text = """\
## Route and audit status

**Primary route**: Listed Company / Investment Memo

| Audit | Status | 证据 |
|-------|--------|------|
| source-traceability | ✅ Passed | 正文使用自然语言标识引用 |
| final-audit | ✅ Passed | §2 可追溯 |

## Findings

据 FY2025 年报，公司营收同比增长 35%。

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | FY2025 年报 | primary | 2026-03-15 | https://example.com/annual-report | high | §2 |
"""
    expect_pass("natural language unique ref passes", text)


def test_strict_mode_warning_only_no_hard_fail() -> None:
    """--strict mode should produce warnings for route-specific issues but not hard-fail."""
    text = """\
## Route and audit status

**Primary route**: Academic / Literature Review

| Audit | Status | 证据 |
|-------|--------|------|
| source-traceability | ✅ Passed | 正文使用 [S01] 引用 |
| final-audit | ✅ Passed | §2 可追溯 |

## Findings

The key finding is supported by prior work [S01].

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Example academic paper | secondary | 2025-06-01 | https://example.com | high | §2 |
"""
    # Should still pass (exit 0) since warnings are not hard errors
    expect_pass("strict warning only", text, "--strict")


def test_all_checks_together_passes() -> None:
    """All structural checks together on a real-looking report should pass."""
    text = """\
# Provider Selection Report

## Route and audit status

**Primary route**: Provider / Vendor Selection
**Secondary route**: Regulatory / Policy Impact Analysis

| Audit | Status | 证据 |
|-------|--------|------|
| route-activation-audit | ✅ Passed | §3-§5 路由选择正确 |
| option-selection-final-audit | ✅ Passed | §4 短名单已执行 |
| source-traceability | ✅ Passed | 正文使用 [S01]-[S03] 引用 |
| final-audit | ✅ Passed | §2-§6 各关卡可追溯 |
| regulatory secondary hard-fail | ✅ Passed | §6 已验证 |

## Evaluation criteria

Cost efficiency is the primary driver [S01].
Vendor lock-in risk must be considered [S02].
Regulatory compliance is mandatory for all options [S03].

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Vendor pricing analysis | secondary | 2026-01-10 | https://example.com/pricing | medium | §3 |
| S02 | Industry lock-in report | secondary | 2026-01-15 | https://example.com/lock-in | medium | §3 |
| S03 | Regulatory framework 2026 | primary | 2026-01-01 | https://example.com/regs | high | §3 |
"""
    expect_pass("all checks together passes", text)


# ── Audit self-assessment consistency tests ──────────────────────────────


def test_audit_source_traceability_mismatch_warns() -> None:
    """source-traceability marked ✅ Passed but body has zero refs → warn.
    
    The warning is additive: the existing hard error (exit 2) from
    check_body_references still fires, AND the self-assessment warning
    appears. We verify both the warning text AND the exit code.
    """
    text = """\
## Route and audit status

**Primary route**: Provider / Vendor Selection

| Audit | Status | 证据 |
|-------|--------|------|
| source-traceability | ✅ Passed | §3 已验证 |
| final-audit | ✅ Passed | §2 已验证 |

## Findings

No source references in the actual body text.

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Example | secondary | 2026-01-01 | https://example.com | medium | §2 |
"""
    result = run_validator(text)
    # Hard error from check_body_references still fires
    assert result.returncode == 2, (
        f"expected exit 2 (hard error), got {result.returncode}\n"
        f"stdout: {result.stdout}"
    )
    # Self-assessment warning is additive
    assert "self-assessment mismatch" in result.stdout.lower(), (
        f"expected warning about self-assessment mismatch in:\n{result.stdout}"
    )
    print("  PASS  audit source-traceability mismatch warns")


def test_audit_quantitative_role_mismatch_warns() -> None:
    """quantitative-role marked ✅ Passed but tables have no role labels."""
    text = """\
## Route and audit status

**Primary route**: Provider / Vendor Selection

| Audit | Status | 证据 |
|-------|--------|------|
| quantitative-role | ✅ Passed | §4 已验证 |
| source-traceability | ✅ Passed | 正文使用 [S01] 引用 |
| final-audit | ✅ Passed | §2 已验证 |

## Findings

Body text with citation [S01].

| Metric | Base | Upside |
|--------|------|--------|
| Market size | $10B | $15B |
| Adoption | 25% | 35% |

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Example | secondary | 2026-01-01 | https://example.com | medium | §2 |
"""
    result = run_validator(text)
    assert result.returncode == 0, (
        f"expected pass (exit 0), got {result.returncode}\n"
        f"stdout: {result.stdout}"
    )
    assert "self-assessment mismatch" in result.stdout.lower(), (
        f"expected warning about self-assessment mismatch in:\n{result.stdout}"
    )
    print("  PASS  audit quantitative-role mismatch warns")


def test_audit_self_assessment_consistent_no_warn() -> None:
    """Audit claims match body execution → no self-assessment warnings."""
    text = """\
## Route and audit status

**Primary route**: Provider / Vendor Selection

| Audit | Status | 证据 |
|-------|--------|------|
| source-traceability | ✅ Passed | §3-§5 正文使用 [S01] 引用 |
| quantitative-role | ✅ Passed | §4 表格含角色列 |
| final-audit | ✅ Passed | §2 各关卡可追溯 |

## Findings

Body text with citation [S01].

| Metric | Base | Upside | Role |
|--------|------|--------|------|
| Market size | $10B | $15B | A |
| Adoption | 25% | 35% | M |

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Example | secondary | 2026-01-01 | https://example.com | medium | §2 |
"""
    result = run_validator(text)
    assert result.returncode == 0, (
        f"expected pass (exit 0), got {result.returncode}\n"
        f"stdout: {result.stdout}"
    )
    assert "self-assessment mismatch" not in result.stdout.lower(), (
        f"unexpected self-assessment mismatch warning in:\n{result.stdout}"
    )
    print("  PASS  audit self-assessment consistent")


def test_audit_self_assessment_author_year_consistent() -> None:
    """Author-Year citation satisfies source-traceability, no warning."""
    text = """\
## Route and audit status

**Primary route**: Academic / Literature Review

| Audit | Status | 证据 |
|-------|--------|------|
| source-traceability | ✅ Passed | 正文使用 Author-Year 引用 |
| final-audit | ✅ Passed | §2 可追溯 |

## Findings

The transformer architecture revolutionized NLP (Vaswani et al., 2017, NeurIPS).

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Vaswani et al. 2017 | secondary | 2017-06-12 | https://arxiv.org/abs/1706.03762 | high | §2 |
"""
    result = run_validator(text)
    assert result.returncode == 0, (
        f"expected pass (exit 0), got {result.returncode}\n"
        f"stdout: {result.stdout}"
    )
    assert "self-assessment mismatch" not in result.stdout.lower(), (
        f"unexpected warning in:\n{result.stdout}"
    )
    print("  PASS  audit self-assessment author-year consistent")


def test_audit_self_assessment_doi_consistent() -> None:
    """DOI citation satisfies source-traceability, no warning."""
    text = """\
## Route and audit status

**Primary route**: Technical Deep-dive

| Audit | Status | 证据 |
|-------|--------|------|
| source-traceability | ✅ Passed | 正文使用 DOI 引用 |
| final-audit | ✅ Passed | §2 可追溯 |

## Findings

The findings are documented (doi:10.1038/s41586-023-06747-5).

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Nature paper 2023 | secondary | 2023-11-01 | https://doi.org/10.1038/s41586-023-06747-5 | high | §2 |
"""
    result = run_validator(text)
    assert result.returncode == 0, (
        f"expected pass (exit 0), got {result.returncode}\n"
        f"stdout: {result.stdout}"
    )
    assert "self-assessment mismatch" not in result.stdout.lower(), (
        f"unexpected warning in:\n{result.stdout}"
    )
    print("  PASS  audit self-assessment doi consistent")


# ── Main ─────────────────────────────────────────────────────────────────


def main() -> int:
    tests = [
        ("valid report passes", test_valid_report_passes),
        ("shared-workflow passes", test_shared_workflow_passes),
        ("missing route/audit block fails", test_missing_route_audit_block_fails),
        ("missing route declaration fails", test_missing_route_declaration_fails),
        ("passed row empty evidence fails", test_passed_row_empty_evidence_fails),
        ("passed row vague evidence fails", test_passed_row_vague_evidence_fails),
        ("missing source register fails", test_missing_source_register_fails),
        ("source register wrong columns fails", test_source_register_wrong_columns_fails),
        ("zero body refs fails", test_zero_body_refs_fails),
        ("body refs in register table excluded", test_body_refs_outside_register_only_fails),
        ("annotated passed row with empty evidence fails", test_passed_row_with_annotation_fails),
        ("author-year ref passes", test_author_year_ref_passes),
        ("arxiv id ref passes", test_arxiv_id_ref_passes),
        ("doi ref passes", test_doi_ref_passes),
        ("natural language unique ref passes", test_natural_language_unique_ref_passes),
        ("strict mode warning only", test_strict_mode_warning_only_no_hard_fail),
        ("all checks together passes", test_all_checks_together_passes),
        ("audit source-traceability mismatch warns", test_audit_source_traceability_mismatch_warns),
        ("audit quantitative-role mismatch warns", test_audit_quantitative_role_mismatch_warns),
        ("audit self-assessment consistent", test_audit_self_assessment_consistent_no_warn),
        ("audit self-assessment author-year consistent", test_audit_self_assessment_author_year_consistent),
        ("audit self-assessment doi consistent", test_audit_self_assessment_doi_consistent),
    ]
    failures = []
    for name, fn in tests:
        try:
            fn()
        except AssertionError as exc:
            failures.append(name)
            print(f"  FAIL  {name}: {exc}")
        except Exception as exc:
            failures.append(name)
            print(f"  FAIL  {name} (exception): {exc}")

    if failures:
        print(f"\n{len(failures)} test(s) failed: {', '.join(failures)}")
        return 1

    print(f"\nAll {len(tests)} tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
