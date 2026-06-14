#!/usr/bin/env python3
"""Regression tests for validate_listed_company_delivery.py.

Each test creates an inline fixture, runs the validator as a subprocess,
and asserts the expected exit code and output content.

Property-based tests verify invariants:
- Exit 0 iff no errors (warnings may be present)
- Exit 2 iff blocking errors exist
- Route detection always produces consistent results
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = str(Path(__file__).resolve().parent / "validate_listed_company_delivery.py")

# ── Fixture builders ─────────────────────────────────────────────────────────


def _valid_listed_company() -> str:
    """A minimal valid listed-company report with all required elements.

    Requirements satisfied:
    - Research-anchor block: latest FY, latest quarter, snapshot date
    - Market snapshot table: share price, market cap, PE(TTM), PE(Forward),
      PB, PS, 52-week range, dividend yield
    - Body [Sxx] citations present
    - 7-column Source Register
    - Audit block with source-traceability, final-audit passed
    - No strong wording without citation
    - No secondary route declared
    """
    return """\
# TSMC Valuation Report

## Route and audit status

**Primary route**: Listed Company / Investment-style Research

| Audit | Status | 证据 |
|-------|--------|------|
| listed-company-report | ✅ Passed | §1-§6 各检查项已执行 |
| source-traceability | ✅ Passed | 正文使用 [S01] 引用，附录 7 列 Source Register |
| final-audit | ✅ Passed | §2-§6 各核心关卡可追溯 |

## 研究锚定块

- **最新完整财年**: FY2025 (2025-12-31)
- **最新季度**: 2026Q1 (2026-03-31)
- **快照日期**: 2026-06-01
- **管理层**: 魏哲家 (CEO)

## 市场快照

| 指标 | 数值 | 数据来源 |
|------|------|----------|
| 当前股价 | $185.50 | NYSE |
| 市值 | $960B | NYSE |
| PE (TTM) | 28.5x | Company filings |
| PE (Forward) | 22.1x | Analyst consensus |
| PB | 7.2x | Company filings |
| PS | 10.8x | Company filings |
| 52周区间 | $120.40 - $210.80 | NYSE |
| 股息率 | 1.5% | Company filings |

## 投资判断

The company's AI-driven growth trajectory remains intact [S01].
Leading-edge process node advantage is sustainable through N3 and N2 [S01].

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | TSMC 2025 Annual Report | primary | 2026-03-31 | https://example.com/tsmc-2025-ar | high | §3 |
"""


def _missing_anchor_block() -> str:
    """Listed-company report with no research-anchor block → hard-fail."""
    return """\
# TSMC Valuation Report

## Route and audit status

**Primary route**: Listed Company / Investment-style Research

| Audit | Status | 证据 |
|-------|--------|------|
| source-traceability | ✅ Passed | 正文使用 [S01] 引用 |
| final-audit | ✅ Passed | §2 可追溯 |

## 市场快照

| 指标 | 数值 | 数据来源 |
|------|------|----------|
| 当前股价 | $185.50 | NYSE |
| 市值 | $960B | NYSE |
| PE (TTM) | 28.5x | Company filings |
| PE (Forward) | 22.1x | Analyst consensus |
| PB | 7.2x | Company filings |
| PS | 10.8x | Company filings |
| 52周区间 | $120.40 - $210.80 | NYSE |
| 股息率 | 1.5% | Company filings |

## 投资判断

The company's AI-driven growth trajectory remains intact [S01].

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | TSMC 2025 Annual Report | primary | 2026-03-31 | https://example.com/tsmc-2025-ar | high | §3 |
"""


def _incomplete_market_snapshot() -> str:
    """Listed-company report with only 3 snapshot fields → warning."""
    return """\
# TSMC Valuation Report

## Route and audit status

**Primary route**: Listed Company / Investment-style Research

| Audit | Status | 证据 |
|-------|--------|------|
| source-traceability | ✅ Passed | 正文使用 [S01] 引用 |
| final-audit | ✅ Passed | §2 可追溯 |

## 研究锚定块

- **最新完整财年**: FY2025 (2025-12-31)
- **最新季度**: 2026Q1 (2026-03-31)
- **快照日期**: 2026-06-01

## 市场快照

| 指标 | 数值 | 数据来源 |
|------|------|----------|
| 当前股价 | $185.50 | NYSE |
| 市值 | $960B | NYSE |
| PE (TTM) | 28.5x | Company filings |

## 投资判断

The company's AI-driven growth trajectory remains intact [S01].

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | TSMC 2025 Annual Report | primary | 2026-03-31 | https://example.com/tsmc-2025-ar | high | §3 |
"""


def _strong_wording_without_citation_audit_claims_pass() -> str:
    """Strong wording like '唯一' without citation, but audit claims ✅ → error."""
    return """\
# TSMC Valuation Report

## Route and audit status

**Primary route**: Listed Company / Investment-style Research

| Audit | Status | 证据 |
|-------|--------|------|
| source-traceability | ✅ Passed | 正文使用 [S01] 引用 |
| final-audit | ✅ Passed | §2 可追溯 |

## 研究锚定块

- **最新完整财年**: FY2025 (2025-12-31)
- **最新季度**: 2026Q1 (2026-03-31)
- **快照日期**: 2026-06-01

## 市场快照

| 指标 | 数值 | 数据来源 |
|------|------|----------|
| 当前股价 | $185.50 | NYSE |
| 市值 | $960B | NYSE |
| PE (TTM) | 28.5x | Company filings |
| PE (Forward) | 22.1x | Analyst consensus |
| PB | 7.2x | Company filings |
| PS | 10.8x | Company filings |
| 52周区间 | $120.40 - $210.80 | NYSE |
| 股息率 | 1.5% | Company filings |

## 投资判断

TSMC is the **唯一** advanced process foundry with **不可替代** technology leadership.
Its market share exceeds **>90%** in leading-edge logic.

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | TSMC 2025 Annual Report | primary | 2026-03-31 | https://example.com/tsmc-2025-ar | high | §3 |
"""


def _strong_wording_but_cited() -> str:
    """Strong wording present but with [Sxx] citation → acceptable."""
    return """\
# TSMC Valuation Report

## Route and audit status

**Primary route**: Listed Company / Investment-style Research

| Audit | Status | 证据 |
|-------|--------|------|
| source-traceability | ✅ Passed | 正文使用 [S01] 引用 |
| final-audit | ✅ Passed | §2 可追溯 |

## 研究锚定块

- **最新完整财年**: FY2025 (2025-12-31)
- **最新季度**: 2026Q1 (2026-03-31)
- **快照日期**: 2026-06-01

## 市场快照

| 指标 | 数值 | 数据来源 |
|------|------|----------|
| 当前股价 | $185.50 | NYSE |
| 市值 | $960B | NYSE |
| PE (TTM) | 28.5x | Company filings |
| PE (Forward) | 22.1x | Analyst consensus |
| PB | 7.2x | Company filings |
| PS | 10.8x | Company filings |
| 52周区间 | $120.40 - $210.80 | NYSE |
| 股息率 | 1.5% | Company filings |

## 投资判断

TSMC is the **唯一** advanced process foundry with reliable technology [S01].

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | TSMC 2025 Annual Report | primary | 2026-03-31 | https://example.com/tsmc-2025-ar | high | §3 |
"""


def _secondary_route_without_verification() -> str:
    """Declares Market Outlook as secondary route but no hard-fail row."""
    return """\
# TSMC Valuation Report

## Route and audit status

**Primary route**: Listed Company / Investment-style Research
**Secondary route**: Market Outlook / Industry Evolution

| Audit | Status | 证据 |
|-------|--------|------|
| source-traceability | ✅ Passed | 正文使用 [S01] 引用 |
| final-audit | ✅ Passed | §2 可追溯 |

## 研究锚定块

- **最新完整财年**: FY2025 (2025-12-31)
- **最新季度**: 2026Q1 (2026-03-31)
- **快照日期**: 2026-06-01

## 市场快照

| 指标 | 数值 | 数据来源 |
|------|------|----------|
| 当前股价 | $185.50 | NYSE |
| 市值 | $960B | NYSE |
| PE (TTM) | 28.5x | Company filings |
| PE (Forward) | 22.1x | Analyst consensus |
| PB | 7.2x | Company filings |
| PS | 10.8x | Company filings |
| 52周区间 | $120.40 - $210.80 | NYSE |
| 股息率 | 1.5% | Company filings |

## 投资判断

The company's AI-driven growth trajectory remains intact [S01].

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | TSMC 2025 Annual Report | primary | 2026-03-31 | https://example.com/tsmc-2025-ar | high | §3 |
"""


def _secondary_route_with_verification() -> str:
    """Declares Market Outlook secondary and has hard-fail row → ok."""
    return """\
# TSMC Valuation Report

## Route and audit status

**Primary route**: Listed Company / Investment-style Research
**Secondary route**: Market Outlook / Industry Evolution

| Audit | Status | 证据 |
|-------|--------|------|
| source-traceability | ✅ Passed | 正文使用 [S01] 引用 |
| final-audit | ✅ Passed | §2 可追溯 |
| market-outlook-hard-fail | ✅ Passed | §5 市场展望已验证场景结构 |

## 研究锚定块

- **最新完整财年**: FY2025 (2025-12-31)
- **最新季度**: 2026Q1 (2026-03-31)
- **快照日期**: 2026-06-01

## 市场快照

| 指标 | 数值 | 数据来源 |
|------|------|----------|
| 当前股价 | $185.50 | NYSE |
| 市值 | $960B | NYSE |
| PE (TTM) | 28.5x | Company filings |
| PE (Forward) | 22.1x | Analyst consensus |
| PB | 7.2x | Company filings |
| PS | 10.8x | Company filings |
| 52周区间 | $120.40 - $210.80 | NYSE |
| 股息率 | 1.5% | Company filings |

## 投资判断

The company's AI-driven growth trajectory remains intact [S01].

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | TSMC 2025 Annual Report | primary | 2026-03-31 | https://example.com/tsmc-2025-ar | high | §3 |
"""


def _strong_wording_uncited_no_audit_claim() -> str:
    """Strong wording without citation, audit does NOT claim source-traceability ✅
    → warning only, not error."""
    return """\
# TSMC Valuation Report

## Route and audit status

**Primary route**: Listed Company / Investment-style Research

| Audit | Status | 证据 |
|-------|--------|------|
| final-audit | ✅ Passed | §2 可追溯 |

## 研究锚定块

- **最新完整财年**: FY2025 (2025-12-31)
- **最新季度**: 2026Q1 (2026-03-31)
- **快照日期**: 2026-06-01

## 市场快照

| 指标 | 数值 | 数据来源 |
|------|------|----------|
| 当前股价 | $185.50 | NYSE |
| 市值 | $960B | NYSE |
| PE (TTM) | 28.5x | Company filings |
| PE (Forward) | 22.1x | Analyst consensus |
| PB | 7.2x | Company filings |
| PS | 10.8x | Company filings |
| 52周区间 | $120.40 - $210.80 | NYSE |
| 股息率 | 1.5% | Company filings |

## 投资判断

TSMC is the **唯一** advanced process foundry with **不可替代** technology leadership.

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | TSMC 2025 Annual Report | primary | 2026-03-31 | https://example.com/tsmc-2025-ar | high | §3 |
"""


# ── Test helpers ─────────────────────────────────────────────────────────────


def run_validator(text: str, *args: str) -> subprocess.CompletedProcess:
    with tempfile.TemporaryDirectory() as d:
        path = Path(d) / "report.md"
        path.write_text(text, encoding="utf-8")
        return subprocess.run(
            [sys.executable, SCRIPT, str(path), *args],
            capture_output=True,
            text=True,
        )


def expect_pass(name: str, text: str, *args: str) -> None:
    result = run_validator(text, *args)
    assert result.returncode == 0, (
        f"{name}: expected pass (exit 0), got {result.returncode}\n"
        f"stdout: {result.stdout}\nstderr: {result.stderr}"
    )
    print(f"  PASS  {name}")


def expect_fail(name: str, text: str, *args: str) -> None:
    result = run_validator(text, *args)
    assert result.returncode == 2, (
        f"{name}: expected exit 2, got {result.returncode}\n"
        f"stdout: {result.stdout}\nstderr: {result.stderr}"
    )
    print(f"  PASS  {name}")


def expect_warn(name: str, text: str, *args: str) -> None:
    """Expect warning-only (exit 0 with warning output)."""
    result = run_validator(text, *args)
    assert result.returncode == 0, (
        f"{name}: expected warning (exit 0), got {result.returncode}\n"
        f"stdout: {result.stdout}\nstderr: {result.stderr}"
    )
    assert "⚠" in result.stdout or "warning" in result.stdout.lower(), (
        f"{name}: expected warning output, got:\n{result.stdout}"
    )
    print(f"  PASS  {name}")


# ── Tests ────────────────────────────────────────────────────────────────────


def test_valid_listed_company_passes() -> None:
    """Fully valid listed-company report should pass."""
    expect_pass("valid listed-company", _valid_listed_company())


def test_missing_anchor_block_fails() -> None:
    """Missing research-anchor block should hard-fail."""
    expect_fail("missing anchor block", _missing_anchor_block())


def test_incomplete_market_snapshot_warns() -> None:
    """Market snapshot with fewer than 5 required fields should warn."""
    expect_warn("incomplete market snapshot", _incomplete_market_snapshot())


def test_strong_wording_uncited_with_audit_pass_fails() -> None:
    """Strong wording without citation + audit claims ✅ → error."""
    expect_fail(
        "strong wording uncited with audit pass",
        _strong_wording_without_citation_audit_claims_pass(),
    )


def test_strong_wording_cited_passes() -> None:
    """Strong wording with [Sxx] citation → pass."""
    expect_pass("strong wording cited", _strong_wording_but_cited())


def test_strong_wording_uncited_without_audit_claim_warns() -> None:
    """Strong wording uncited + audit doesn't claim source-traceability → warn."""
    expect_warn(
        "strong wording uncited without audit claim",
        _strong_wording_uncited_no_audit_claim(),
    )


def test_secondary_route_without_verification_warns() -> None:
    """Secondary route declared but no hard-fail row → warn."""
    expect_warn(
        "secondary route without verification",
        _secondary_route_without_verification(),
    )


def test_secondary_route_with_verification_passes() -> None:
    """Secondary route declared with hard-fail row → pass."""
    expect_pass(
        "secondary route with verification",
        _secondary_route_with_verification(),
    )


def test_non_listed_company_report_skipped() -> None:
    """Report without listed-company route should skip all checks (pass)."""
    text = """\
# Technical Report

## Route and audit status

**Primary route**: Technical Deep-dive

| Audit | Status | 证据 |
|-------|--------|------|
| source-traceability | ✅ Passed | 正文使用 [S01] 引用 |

## Findings

Analysis shows clear patterns [S01].

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Example | secondary | 2026-01-01 | https://example.com | medium | §2 |
"""
    expect_pass("non-listed-company skipped", text)


def test_strong_wording_english_only_uncited_fails() -> None:
    """English strong wording ('only', 'irreplaceable') without citation → fail
    when audit claims source-traceability ✅."""
    text = """\
# Report

## Route and audit status

**Primary route**: Listed Company / Investment-style Research

| Audit | Status | 证据 |
|-------|--------|------|
| source-traceability | ✅ Passed | 正文使用 [S01] 引用 |

## 研究锚定块

- **最新完整财年**: FY2025
- **最新季度**: 2026Q1
- **快照日期**: 2026-06-01

## 市场快照

| 指标 | 数值 |
|------|------|
| 当前股价 | $185.50 |
| 市值 | $960B |
| PE (TTM) | 28.5x |
| PE (Forward) | 22.1x |
| PB | 7.2x |
| PS | 10.8x |
| 52周区间 | $120-$210 |
| 股息率 | 1.5% |

## Body

This is the **only** company with irreplaceable technology advantages.
"""
    expect_fail("english strong wording uncited", text)


# ── Main ─────────────────────────────────────────────────────────────────────


def main() -> int:
    tests = [
        ("valid listed-company passes", test_valid_listed_company_passes),
        ("missing anchor block fails", test_missing_anchor_block_fails),
        ("incomplete market snapshot warns", test_incomplete_market_snapshot_warns),
        (
            "strong wording uncited with audit pass fails",
            test_strong_wording_uncited_with_audit_pass_fails,
        ),
        ("strong wording cited passes", test_strong_wording_cited_passes),
        (
            "strong wording uncited without audit claim warns",
            test_strong_wording_uncited_without_audit_claim_warns,
        ),
        (
            "secondary route without verification warns",
            test_secondary_route_without_verification_warns,
        ),
        (
            "secondary route with verification passes",
            test_secondary_route_with_verification_passes,
        ),
        ("non-listed-company skipped", test_non_listed_company_report_skipped),
        (
            "english strong wording uncited fails",
            test_strong_wording_english_only_uncited_fails,
        ),
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
