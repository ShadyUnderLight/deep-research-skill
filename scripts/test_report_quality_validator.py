#!/usr/bin/env python3
"""Regression tests for validate_report_quality.py.

Each test creates a fixture, runs the validator as a subprocess,
and asserts the expected exit code.
"""

import subprocess
import sys
import tempfile
from pathlib import Path

# Direct import for get_route_name unit tests
sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_report_quality import get_route_name

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
| S01 | Example source | secondary | 2026-01-01 | https://example.com | medium | §2: documented evidence |
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
| S01 | Example market report | secondary | 2026-01-01 | https://example.com | medium | §3: documented evidence |
| S02 | Industry filing | primary | 2026-02-01 | https://example.com/filing | high | §3: documented evidence |
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
| S01 | Example source | secondary | 2026-01-15 | https://example.com | medium | §2: documented evidence |
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
| source-traceability | ✅ Passed | §3: documented evidence |

## Findings

Body text with citation [S01].

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Example | secondary | 2026-01-01 | https://example.com | medium | §2: documented evidence |
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
| S01 | Example | secondary | 2026-01-01 | https://example.com | medium | §2: documented evidence |
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
| S01 | Example | secondary | 2026-01-01 | https://example.com | medium | §2: documented evidence |
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
| S01 | Example | secondary | 2026-01-01 | https://example.com | medium | §2: documented evidence |
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

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported | Publication Type | Peer-review Status | Venue | Venue Prestige |
|----|-------------|-------------|------|---------|-------------|------------------|-----------------|--------------------|-------|----------------|
| S01 | Vaswani et al. 2017 | secondary | 2017-06-12 | https://arxiv.org/abs/1706.03762 | high | §2: academic evidence | published | peer-reviewed | NeurIPS | top-tier |
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
| S01 | Attention is All You Need | secondary | 2017-06-12 | https://arxiv.org/abs/1706.03762 | high | §2: documented evidence |
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
| S01 | Nature paper 2023 | secondary | 2023-11-01 | https://doi.org/10.1038/s41586-023-06747-5 | high | §2: documented evidence |
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
| S01 | FY2025 年报 | primary | 2026-03-15 | https://example.com/annual-report | high | §2: documented evidence |
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

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported | Publication Type | Peer-review Status | Venue | Venue Prestige |
|----|-------------|-------------|------|---------|-------------|------------------|-----------------|--------------------|-------|----------------|
| S01 | Example academic paper | secondary | 2025-06-01 | https://example.com | high | §2: academic evidence | published | peer-reviewed | NeurIPS | top-tier |
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
| S01 | Vendor pricing analysis | secondary | 2026-01-10 | https://example.com/pricing | medium | §3: documented evidence |
| S02 | Industry lock-in report | secondary | 2026-01-15 | https://example.com/lock-in | medium | §3: documented evidence |
| S03 | Regulatory framework 2026 | primary | 2026-01-01 | https://example.com/regs | high | §3: documented evidence |
"""
    expect_pass("all checks together passes", text)


# ── Audit self-assessment consistency tests ──────────────────────────────


def test_audit_source_traceability_mismatch_fails() -> None:
    """source-traceability marked ✅ Passed but body has zero refs → hard-fail.
    
    Previously warnings-level; now hard error (exit 2).
    The existing hard error from check_body_references also fires.
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
| S01 | Example | secondary | 2026-01-01 | https://example.com | medium | §2: documented evidence |
"""
    result = run_validator(text)
    # Hard error from check_body_references still fires
    assert result.returncode == 2, (
        f"expected exit 2 (hard error), got {result.returncode}\n"
        f"stdout: {result.stdout}"
    )
    # Self-assessment mismatch is now a hard error (was warning)
    assert "self-assessment mismatch" in result.stdout.lower(), (
        f"expected self-assessment mismatch error in:\n{result.stdout}"
    )
    print("  PASS  audit source-traceability mismatch fails")


def test_audit_quantitative_role_mismatch_fails() -> None:
    """quantitative-role marked ✅ Passed but tables have no role labels → hard-fail."""
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
| S01 | Example | secondary | 2026-01-01 | https://example.com | medium | §2: documented evidence |
"""
    result = run_validator(text)
    # Now hard-fail (exit 2) instead of pass with warning (exit 0)
    assert result.returncode == 2, (
        f"expected exit 2 (hard error), got {result.returncode}\n"
        f"stdout: {result.stdout}"
    )
    assert "self-assessment mismatch" in result.stdout.lower(), (
        f"expected self-assessment mismatch error in:\n{result.stdout}"
    )
    print("  PASS  audit quantitative-role mismatch fails")


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
| S01 | Example | secondary | 2026-01-01 | https://example.com | medium | §2: documented evidence |
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

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported | Publication Type | Peer-review Status | Venue | Venue Prestige |
|----|-------------|-------------|------|---------|-------------|------------------|-----------------|--------------------|-------|----------------|
| S01 | Vaswani et al. 2017 | secondary | 2017-06-12 | https://arxiv.org/abs/1706.03762 | high | §2: academic evidence | published | peer-reviewed | NeurIPS | top-tier |
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
| S01 | Nature paper 2023 | secondary | 2023-11-01 | https://doi.org/10.1038/s41586-023-06747-5 | high | §2: documented evidence |
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


# ── Source Register row-level checks ──────────────────────────────────────


def test_register_row_missing_id_fails() -> None:
    """Register entry with empty ID should fail."""
    text = """\
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
| S01 | Example source | secondary | 2026-01-01 | https://example.com | medium | §2: documented evidence |
|  | Empty ID entry | secondary | 2026-02-01 | https://example.com/2 | low | §3: documented evidence |
"""
    expect_fail("register row missing ID fails", text)


def test_register_rows_all_valid_passes() -> None:
    """All register rows have non-empty IDs → pass."""
    text = """\
## Route and audit status

**Primary route**: Provider / Vendor Selection

| Audit | Status | 证据 |
|-------|--------|------|
| source-traceability | ✅ Passed | §3 正文使用 [S01] 引用 |
| final-audit | ✅ Passed | §2 各关卡可追溯 |

## Findings

Body text with citations [S01][S02].

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | First source | secondary | 2026-01-01 | https://example.com/1 | medium | §2: documented evidence |
| S02 | Second source | primary | 2026-02-01 | https://example.com/2 | high | §2: documented evidence |
"""
    expect_pass("register rows all valid pass", text)


def test_register_doi_systematically_missing_warns() -> None:
    """>50% of register rows missing DOI/URL → warning, not hard fail."""
    text = """\
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
| S01 | First source | secondary | 2026-01-01 |  | medium | §2: documented evidence |
| S02 | Second source | primary | 2026-02-01 |  | high | §2: documented evidence |
| S03 | Third source | secondary | 2026-03-01 | https://example.com | medium | §3: documented evidence |
"""
    result = run_validator(text)
    assert result.returncode == 0, (
        f"expected pass with warning (exit 0), got {result.returncode}\n"
        f"stdout: {result.stdout}"
    )
    assert "DOI/URL" in result.stdout, (
        f"expected warning about DOI/URL in:\n{result.stdout}"
    )
    print("  PASS  register DOI systematically missing warns")


# ── Key section citation coverage checks ──────────────────────────────────


def test_exec_summary_no_ref_fails() -> None:
    """Executive summary section without [Sxx] should fail."""
    text = """\
## Route and audit status

**Primary route**: Provider / Vendor Selection

| Audit | Status | 证据 |
|-------|--------|------|
| source-traceability | ✅ Passed | §3 正文使用 [S01] 引用 |
| final-audit | ✅ Passed | §2 各关卡可追溯 |

## 执行摘要

The market is undergoing rapid transformation.
New entrants are disrupting traditional business models.
No source citations in this section.

## Findings

Body text with citation [S01].

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Example source | secondary | 2026-01-01 | https://example.com | medium | §2: documented evidence |
"""
    expect_fail("exec summary no ref fails", text)


def test_all_key_sections_have_refs_passes() -> None:
    """All recognized key sections with [Sxx] should pass without warnings."""
    text = """\
## Route and audit status

**Primary route**: Provider / Vendor Selection

| Audit | Status | 证据 |
|-------|--------|------|
| source-traceability | ✅ Passed | §3 正文使用 [S01] 引用 |
| final-audit | ✅ Passed | §2 各关卡可追溯 |

## 执行摘要

The market is growing [S01].

## Findings

Body text with citation [S01].

## 综合结论

The recommendation is clear [S01].

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Example source | secondary | 2026-01-01 | https://example.com | medium | §2: documented evidence |
"""
    result = run_validator(text)
    assert result.returncode == 0, (
        f"expected pass, got {result.returncode}\n"
        f"stdout: {result.stdout}"
    )
    assert "key section" not in result.stdout.lower(), (
        f"unexpected warning in:\n{result.stdout}"
    )
    print("  PASS  all key sections have refs")


def test_key_section_author_year_instead_of_sxx_passes() -> None:
    """Equivalent format (Author-Year) in key section should satisfy check."""
    text = """\
## Route and audit status

**Primary route**: Academic / Literature Review

| Audit | Status | 证据 |
|-------|--------|------|
| source-traceability | ✅ Passed | §3 正文使用 Author-Year 引用 |
| final-audit | ✅ Passed | §2 各关卡可追溯 |

## Executive Summary

The transformer architecture revolutionized NLP (Vaswani et al., 2017, NeurIPS).

## Findings

Body text with citation [S01].

## Conclusion

This analysis supports continued development [S01].

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported | Publication Type | Peer-review Status | Venue | Venue Prestige |
|----|-------------|-------------|------|---------|-------------|------------------|-----------------|--------------------|-------|----------------|
| S01 | Vaswani et al. 2017 | primary | 2017-06-12 | https://arxiv.org/abs/1706.03762 | high | §2: academic evidence | published | peer-reviewed | NeurIPS | top-tier |
"""
    result = run_validator(text)
    assert result.returncode == 0, (
        f"expected pass, got {result.returncode}\n"
        f"stdout: {result.stdout}"
    )
    assert "key section" not in result.stdout.lower(), (
        f"unexpected warning in:\n{result.stdout}"
    )
    print("  PASS  key section with Author-Year instead of [Sxx]")


def test_no_key_sections_detected_no_warn() -> None:
    """Report without any recognized key section heading should pass."""
    text = """\
## Route and audit status

**Primary route**: Provider / Vendor Selection

| Audit | Status | 证据 |
|-------|--------|------|
| source-traceability | ✅ Passed | §3 正文使用 [S01] 引用 |
| final-audit | ✅ Passed | §2 各关卡可追溯 |

## Custom Analysis Section

Body text with citation [S01].

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Example source | secondary | 2026-01-01 | https://example.com | medium | §2: documented evidence |
"""
    result = run_validator(text)
    assert result.returncode == 0, (
        f"expected pass, got {result.returncode}\n"
        f"stdout: {result.stdout}"
    )
    assert "key section" not in result.stdout.lower(), (
        f"unexpected warning in:\n{result.stdout}"
    )
    print("  PASS  no key sections detected")


def test_body_ref_not_in_register_fails() -> None:
    """Body references [S99] which doesn't exist in register → fail."""
    text = """\
## Route and audit status

**Primary route**: Provider / Vendor Selection

| Audit | Status | 证据 |
|-------|--------|------|
| source-traceability | ✅ Passed | §3 正文使用 [S01][S99] 引用 |
| final-audit | ✅ Passed | §2 各关卡可追溯 |

## Findings

Body text with citation [S01][S99].

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Example source | secondary | 2026-01-01 | https://example.com | medium | §2: documented evidence |
"""
    expect_fail("body ref not in register fails", text)


def test_register_duplicate_id_fails() -> None:
    """Duplicate ID in Source Register should fail."""
    text = """\
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
| S01 | First entry | secondary | 2026-01-01 | https://example.com/1 | medium | §2: documented evidence |
| S01 | Duplicate ID | primary | 2026-02-01 | https://example.com/2 | high | §2: documented evidence |
"""
    expect_fail("register duplicate ID fails", text)


def test_key_section_after_register_still_checked() -> None:
    """Key section after Source Register should still be checked for citations."""
    text = """\
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
| S01 | Example source | secondary | 2026-01-01 | https://example.com | medium | §2: documented evidence |

## 综合结论

No citation in this section.
"""
    expect_fail("key section after register fails", text)


# ── Source Register placeholder detection tests ──────────────────────────


def _make_register_placeholder_fixture(doi_value: str) -> str:
    """Build a minimal valid report + register with a specific DOI/URL value."""
    return f"""\
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
| S01 | Example source | secondary | 2026-01-01 | {doi_value} | medium | §2: documented evidence |
"""


def test_register_placeholder_emdash_warns() -> None:
    """Em-dash (—) in DOI/URL column → warning (not hard error)."""
    text = _make_register_placeholder_fixture("—")
    result = run_validator(text)
    assert result.returncode == 0, (
        f"expected pass with warning (exit 0), got {result.returncode}\n"
        f"stdout: {result.stdout}"
    )
    assert "placeholder" in result.stdout.lower(), (
        f"expected placeholder warning in:\n{result.stdout}"
    )
    print("  PASS  register placeholder em-dash warns")


def test_register_placeholder_tbd_warns() -> None:
    """TBD in DOI/URL column → warning."""
    text = _make_register_placeholder_fixture("TBD")
    result = run_validator(text)
    assert result.returncode == 0, (
        f"expected pass with warning (exit 0), got {result.returncode}\n"
        f"stdout: {result.stdout}"
    )
    assert "placeholder" in result.stdout.lower(), (
        f"expected placeholder warning in:\n{result.stdout}"
    )
    print("  PASS  register placeholder TBD warns")


def test_register_placeholder_arxiv_xxxxx_warns() -> None:
    """arXiv:xxxxx placeholder in DOI/URL column → warning."""
    text = _make_register_placeholder_fixture("arXiv:2402.xxxxx")
    result = run_validator(text)
    assert result.returncode == 0, (
        f"expected pass with warning (exit 0), got {result.returncode}\n"
        f"stdout: {result.stdout}"
    )
    assert "placeholder" in result.stdout.lower(), (
        f"expected placeholder warning in:\n{result.stdout}"
    )
    print("  PASS  register placeholder arXiv:xxxxx warns")


def test_register_placeholder_xxxxx_only_warns() -> None:
    """xxxxx placeholder in DOI/URL column → warning."""
    text = _make_register_placeholder_fixture("xxxxx")
    result = run_validator(text)
    assert result.returncode == 0, (
        f"expected pass with warning (exit 0), got {result.returncode}\n"
        f"stdout: {result.stdout}"
    )
    assert "placeholder" in result.stdout.lower(), (
        f"expected placeholder warning in:\n{result.stdout}"
    )
    print("  PASS  register placeholder xxxxx warns")


def test_register_no_placeholder_passes() -> None:
    """Valid DOI/URL → no placeholder warning."""
    text = _make_register_placeholder_fixture("https://doi.org/10.1038/s41586-023-06747-5")
    result = run_validator(text)
    assert result.returncode == 0, (
        f"expected pass (exit 0), got {result.returncode}\n"
        f"stdout: {result.stdout}"
    )
    assert "placeholder" not in result.stdout.lower(), (
        f"unexpected placeholder warning in:\n{result.stdout}"
    )
    print("  PASS  register no placeholder")


# ── Academic 11-column Source Register tests ─────────────────────────────


def _make_academic_register_fixture(num_cols: int, route: str = "Academic / Literature Review") -> str:
    """Build a report with academic route and an N-column Source Register."""
    if num_cols >= 11:
        header = "| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported | Publication Type | Peer-review Status | Venue | Venue Prestige |"
        sep = "|----|-------------|-------------|------|---------|-------------|------------------|-----------------|--------------------|-------|----------------|"
        data = "| S01 | Vaswani et al. 2017 | secondary | 2017-06-12 | https://arxiv.org/abs/1706.03762 | high | §2: academic evidence | published | peer-reviewed | NeurIPS | top-tier |"
    else:
        header = "| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |"
        sep = "|----|-------------|-------------|------|---------|-------------|------------------|"
        data = "| S01 | Vaswani et al. 2017 | secondary | 2017-06-12 | https://arxiv.org/abs/1706.03762 | high | §2: academic evidence |"
    return f"""\
## Route and audit status

**Primary route**: {route}

| Audit | Status | 证据 |
|-------|--------|------|
| source-traceability | ✅ Passed | §3 正文使用 [S01] 引用 |
| final-audit | ✅ Passed | §2 各关卡可追溯 |

## Findings

Body text with citation [S01].

## Source Register

{header}
{sep}
{data}
"""


def test_academic_register_11_columns_passes() -> None:
    """Academic route with 11-column Source Register → pass."""
    text = _make_academic_register_fixture(11)
    result = run_validator(text)
    assert result.returncode == 0, (
        f"expected pass (exit 0), got {result.returncode}\n"
        f"stdout: {result.stdout}"
    )
    print("  PASS  academic 11-column register passes")


def test_academic_register_7_columns_fails() -> None:
    """Academic route with only 7-column Source Register → hard-fail."""
    text = _make_academic_register_fixture(7)
    result = run_validator(text)
    assert result.returncode == 2, (
        f"expected fail (exit 2), got {result.returncode}\n"
        f"stdout: {result.stdout}"
    )
    assert "academic" in result.stdout.lower() and "column" in result.stdout.lower(), (
        f"expected academic column count error in:\n{result.stdout}"
    )
    print("  PASS  academic 7-column register fails")


def test_academic_register_7_columns_non_academic_route_passes() -> None:
    """Non-academic route with 7-column register → pass (no academic column check)."""
    text = _make_academic_register_fixture(7, route="Technical Deep-dive")
    result = run_validator(text)
    assert result.returncode == 0, (
        f"expected pass (exit 0), got {result.returncode}\n"
        f"stdout: {result.stdout}"
    )
    print("  PASS  non-academic 7-column register passes")


# ── Evidence section reference validation tests ───────────────────────
# These test check_audit_evidence_section_refs functionality.

def test_evidence_subsection_ref_valid_passes() -> None:
    """Audit evidence with §X.Y ref that matches a body heading → pass.
    Report has numbered headings like "## 7.2 Technical Deep-dive"."""
    text = """\
# Test Report

## Route and audit status

**Primary route**: Technical Deep-dive

| Audit | Status | 证据 |
|-------|--------|------|
| source-traceability | ✅ Passed | §7.2 验证 hard-fail 条件 |
| final-audit | ✅ Passed | §2 各关卡可追溯 |

## 1. Introduction

Body text with citation [S01].

## 2. Analysis

### 7.2 Technical Deep-dive

Hard-fail verification content [S01].

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Example source | secondary | 2026-01-01 | https://example.com | medium | §2: documented evidence |
"""
    expect_pass("evidence subsection ref valid passes", text)


def test_evidence_subsection_ref_phantom_fails() -> None:
    """Audit evidence with §X.Y ref that has NO matching heading → blocking.
    Report has numbered headings but no "## 7.2" heading."""
    text = """\
# Test Report

## Route and audit status

**Primary route**: Technical Deep-dive

| Audit | Status | 证据 |
|-------|--------|------|
| source-traceability | ✅ Passed | §7.2 验证 hard-fail 条件 |
| final-audit | ✅ Passed | §2 各关卡可追溯 |

## 1. Introduction

Body text with citation [S01].

## 2. Analysis

### 7.1 Component Analysis

Analysis text [S01].

### 7.3 Integration

Analysis text [S01].

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Example source | secondary | 2026-01-01 | https://example.com | medium | §2: documented evidence |
"""
    expect_fail("evidence subsection ref phantom fails", text)


def test_evidence_appendix_ref_valid_passes() -> None:
    """Audit evidence with Appendix reference that matches a heading → pass."""
    text = """\
# Test Report

## Route and audit status

**Primary route**: Technical Deep-dive

| Audit | Status | 证据 |
|-------|--------|------|
| source-traceability | ✅ Passed | §3 正文使用 [S01] 引用 |
| final-audit | ✅ Passed | Appendix B 补充数据 |

## 1. Introduction

Body text with citation [S01].

## Appendix B

Supplementary data [S01].

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Example source | secondary | 2026-01-01 | https://example.com | medium | §2: documented evidence |
"""
    expect_pass("evidence appendix ref valid passes", text)


def test_evidence_appendix_ref_phantom_fails() -> None:
    """Audit evidence with Appendix reference that has NO matching heading → blocking."""
    text = """\
# Test Report

## Route and audit status

**Primary route**: Technical Deep-dive

| Audit | Status | 证据 |
|-------|--------|------|
| source-traceability | ✅ Passed | §3 正文使用 [S01] 引用 |
| final-audit | ✅ Passed | Appendix B 补充数据 |

## 1. Introduction

Body text with citation [S01].

## Appendix A

Previous data [S01].

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Example source | secondary | 2026-01-01 | https://example.com | medium | §2: documented evidence |
"""
    expect_fail("evidence appendix ref phantom fails", text)


def test_evidence_no_numbered_headings_skips_section_refs() -> None:
    """Report with no numbered headings → §X.Y and §X refs are not checked
    (gate: can't verify what doesn't exist structurally)."""
    text = """\
# Test Report

## Route and audit status

**Primary route**: Technical Deep-dive

| Audit | Status | 证据 |
|-------|--------|------|
| source-traceability | ✅ Passed | §7.2 验证 |
| final-audit | ✅ Passed | 各关卡可追溯 |

## Introduction

Body text with citation [S01].

## Methodology

Methodology content [S01].

## Findings

Key findings [S01].

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Example source | secondary | 2026-01-01 | https://example.com | medium | §2: documented evidence |
"""
    expect_pass("evidence no numbered headings skips section refs", text)


def test_evidence_multiple_phantom_refs_all_reported() -> None:
    """Multiple phantom refs in different rows → all reported, not just the first."""
    text = """\
# Test Report

## Route and audit status

**Primary route**: Technical Deep-dive

| Audit | Status | 证据 |
|-------|--------|------|
| source-traceability | ✅ Passed | §7.2 正文引用 |
| quantitative-role | ✅ Passed | §8.3 表格角色列 |

## 1. Introduction

Body text with citation [S01].

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Example source | secondary | 2026-01-01 | https://example.com | medium | §2: documented evidence |
"""
    expect_fail("evidence multiple phantom refs all reported", text)


def test_evidence_phantom_ref_not_passed_row_skipped() -> None:
    """Phantom ref in a row that is NOT passed → skipped (only passed rows matter)."""
    text = """\
# Test Report

## Route and audit status

**Primary route**: Technical Deep-dive

| Audit | Status | 证据 |
|-------|--------|------|
| source-traceability | ❌ Not run | §7.2 |
| final-audit | ✅ Passed | §2 各关卡可追溯 |

## 1. Introduction

Body text with citation [S01].

## 2. Analysis

Analysis content [S01].

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Example source | secondary | 2026-01-01 | https://example.com | medium | §2: documented evidence |
"""
    expect_pass("evidence phantom ref not passed row skipped", text)


def test_evidence_subsection_ref_no_heading_at_all_but_unnumbered_passes() -> None:
    """§7.2 in evidence column, no numbered headings at all → pass (gate)."""
    text = """\
# Test Report

## Route and audit status

**Primary route**: Technical Deep-dive

| Audit | Status | 证据 |
|-------|--------|------|
| source-traceability | ✅ Passed | §7.2 正文引用 |
| final-audit | ✅ Passed | §2 各关卡可追溯 |

## Introduction

Body text with citation [S01].

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Example source | secondary | 2026-01-01 | https://example.com | medium | §2: documented evidence |
"""
    expect_pass("evidence subsection ref unnumbered doc passes", text)
# These import get_route_name directly for precise unit-level testing.


def test_evidence_spaced_subsection_ref_passes() -> None:
    """§ with space (§ 7.2) matches heading with same number."""
    text = """\
# Test Report

## Route and audit status

**Primary route**: Technical Deep-dive

| Audit | Status | 证据 |
|-------|--------|------|
| source-traceability | ✅ Passed | § 7.2 验证 hard-fail 条件 |
| final-audit | ✅ Passed | §2 各关卡可追溯 |

## 1. Introduction

Body text with citation [S01].

## 2. Analysis

### 7.2 Technical Deep-dive

Hard-fail verification content [S01].

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Example source | secondary | 2026-01-01 | https://example.com | medium | §2: documented evidence |
"""
    expect_pass("evidence spaced subsection ref passes", text)


def test_evidence_chinese_appendix_no_space_passes() -> None:
    """Chinese appendix without space (附录B) matches heading."""
    text = """\
# Test Report

## Route and audit status

**Primary route**: Technical Deep-dive

| Audit | Status | 证据 |
|-------|--------|------|
| source-traceability | ✅ Passed | §3 正文使用 [S01] 引用 |
| final-audit | ✅ Passed | 附录B 补充数据 |

## 1. Introduction

Body text with citation [S01].

## 附录B 补充数据

Supplementary data [S01].

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Example source | secondary | 2026-01-01 | https://example.com | medium | §2: documented evidence |
"""
    expect_pass("evidence chinese appendix no space passes", text)


def test_evidence_subsection_ref_prefix_matches_subsubsection() -> None:
    """§7.2 matches '### 7.2.1 Subsection' (prefix matching — intentional)."""
    text = """\
# Test Report

## Route and audit status

**Primary route**: Technical Deep-dive

| Audit | Status | 证据 |
|-------|--------|------|
| source-traceability | ✅ Passed | §7.2 验证 hard-fail 条件 |
| final-audit | ✅ Passed | §3 各关卡可追溯 |

## 1. Introduction

Body text with citation [S01].

## 2. Analysis

### 7.2.1 Technical Details

Only sub-subsection exists, no §7.2 heading itself.

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Example source | secondary | 2026-01-01 | https://example.com | medium | §2: documented evidence |
"""
    expect_pass("evidence subsection ref prefix matches subsubsection", text)


def test_get_route_name_english_still_works() -> None:
    """Existing English format still works after changes."""
    text = """\
## Route and audit status

**Primary route**: Provider / Vendor Selection
"""
    result = get_route_name(text)
    assert result == "Provider / Vendor Selection", (
        f"Expected 'Provider / Vendor Selection', got {result!r}"
    )
    print("  PASS  get_route_name english still works")


def test_get_route_name_chinese_heading() -> None:
    """Report with Chinese heading and 研究路线 should return route name."""
    text = """\
## 附录：路由与审计状态

研究路线：Constrained Choice / Shortlist
"""
    result = get_route_name(text)
    assert result == "Constrained Choice / Shortlist", (
        f"Expected 'Constrained Choice / Shortlist', got {result!r}"
    )
    print("  PASS  get_route_name chinese heading")


def test_get_route_name_chinese_heading_with_secondary() -> None:
    """Chinese heading with secondary route in parentheses."""
    text = """\
## 附录：路由与审计状态

研究路线：Constrained Choice / Shortlist（主）+ Market Outlook（辅助）
"""
    result = get_route_name(text)
    assert result == "Constrained Choice / Shortlist", (
        f"Expected 'Constrained Choice / Shortlist', got {result!r}"
    )
    print("  PASS  get_route_name chinese heading with secondary")


def test_get_route_name_chinese_primary_route() -> None:
    """Chinese heading with 主路由 declaration."""
    text = """\
## 附录：路由与审计状态

主路由：Constrained Choice / Shortlist
"""
    result = get_route_name(text)
    assert result == "Constrained Choice / Shortlist", (
        f"Expected 'Constrained Choice / Shortlist', got {result!r}"
    )
    print("  PASS  get_route_name chinese primary route")


def test_get_route_name_chinese_table_cell_pipe() -> None:
    """Table cell format with pipe separator: 主路由 | Constrained Choice / Shortlist."""
    text = """\
## 附录：路由与审计状态

| Audit | 路由 | 证据 |
|-------|------|------|
| 主路由 | Constrained Choice / Shortlist / Option Selection | ✅ |
"""
    result = get_route_name(text)
    assert result == "Constrained Choice / Shortlist / Option Selection", (
        f"Expected 'Constrained Choice / Shortlist / Option Selection', got {result!r}"
    )
    print("  PASS  get_route_name chinese table cell pipe")


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
        ("audit source-traceability mismatch fails", test_audit_source_traceability_mismatch_fails),
        ("audit quantitative-role mismatch fails", test_audit_quantitative_role_mismatch_fails),
        ("audit self-assessment consistent", test_audit_self_assessment_consistent_no_warn),
        ("audit self-assessment author-year consistent", test_audit_self_assessment_author_year_consistent),
        ("audit self-assessment doi consistent", test_audit_self_assessment_doi_consistent),
        ("register row missing ID fails", test_register_row_missing_id_fails),
        ("register rows all valid pass", test_register_rows_all_valid_passes),
        ("register DOI systematically missing warns", test_register_doi_systematically_missing_warns),
        ("exec summary no ref fails", test_exec_summary_no_ref_fails),
        ("all key sections have refs passes", test_all_key_sections_have_refs_passes),
        ("key section with Author-Year passes", test_key_section_author_year_instead_of_sxx_passes),
        ("no key sections detected no warn", test_no_key_sections_detected_no_warn),
        ("body ref not in register fails", test_body_ref_not_in_register_fails),
        ("register duplicate ID fails", test_register_duplicate_id_fails),
        ("key section after register fails", test_key_section_after_register_still_checked),
        ("register placeholder em-dash warns", test_register_placeholder_emdash_warns),
        ("register placeholder TBD warns", test_register_placeholder_tbd_warns),
        ("register placeholder arXiv:xxxxx warns", test_register_placeholder_arxiv_xxxxx_warns),
        ("register placeholder xxxxx warns", test_register_placeholder_xxxxx_only_warns),
        ("register no placeholder passes", test_register_no_placeholder_passes),
        ("academic 11-column register passes", test_academic_register_11_columns_passes),
        ("academic 7-column register fails", test_academic_register_7_columns_fails),
        ("non-academic 7-column register passes", test_academic_register_7_columns_non_academic_route_passes),
        # evidence section reference tests
        ("evidence subsection ref valid passes", test_evidence_subsection_ref_valid_passes),
        ("evidence subsection ref phantom fails", test_evidence_subsection_ref_phantom_fails),
        ("evidence appendix ref valid passes", test_evidence_appendix_ref_valid_passes),
        ("evidence appendix ref phantom fails", test_evidence_appendix_ref_phantom_fails),
        ("evidence no numbered headings skips section refs", test_evidence_no_numbered_headings_skips_section_refs),
        ("evidence multiple phantom refs all reported", test_evidence_multiple_phantom_refs_all_reported),
        ("evidence phantom ref not passed row skipped", test_evidence_phantom_ref_not_passed_row_skipped),
        ("evidence subsection ref unnumbered doc passes", test_evidence_subsection_ref_no_heading_at_all_but_unnumbered_passes),
        ("evidence spaced subsection ref passes", test_evidence_spaced_subsection_ref_passes),
        ("evidence chinese appendix no space passes", test_evidence_chinese_appendix_no_space_passes),
        ("evidence subsection ref prefix matches subsubsection", test_evidence_subsection_ref_prefix_matches_subsubsection),
        # get_route_name Chinese heading tests
        ("get_route_name english still works", test_get_route_name_english_still_works),
        ("get_route_name chinese heading", test_get_route_name_chinese_heading),
        ("get_route_name chinese heading with secondary", test_get_route_name_chinese_heading_with_secondary),
        ("get_route_name chinese primary route", test_get_route_name_chinese_primary_route),
        ("get_route_name chinese table cell pipe", test_get_route_name_chinese_table_cell_pipe),
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
