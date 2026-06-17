#!/usr/bin/env python3
"""Tests for validate_source_label_consistency.py."""

from pathlib import Path
import subprocess
import sys
import tempfile

from hypothesis import given, strategies as st

SCRIPT = str(
    Path(__file__).resolve().parent / "validate_source_label_consistency.py"
)


def run_lint(text: str) -> subprocess.CompletedProcess:
    with tempfile.TemporaryDirectory() as d:
        path = Path(d) / "fixture.md"
        path.write_text(text, encoding="utf-8")
        return subprocess.run(
            [sys.executable, SCRIPT, str(path)],
            capture_output=True,
            text=True,
        )


def expect_pass(name: str, text: str) -> None:
    result = run_lint(text)
    assert result.returncode == 0, (
        f"{name}: expected pass, got {result.returncode}\n"
        f"stdout: {result.stdout}\nstderr: {result.stderr}"
    )
    print(f"  PASS  {name}")


def expect_fail(name: str, text: str) -> None:
    result = run_lint(text)
    assert result.returncode == 2, (
        f"{name}: expected lint failure, got {result.returncode}\n"
        f"stdout: {result.stdout}\nstderr: {result.stderr}"
    )
    print(f"  PASS  {name}")


# --- Tests ---


def test_secondary_source_with_confirmed_label_fails() -> None:
    """SECONDARY_MEDIA source referenced with [CONF] in body fails."""
    expect_fail(
        "secondary source with confirmed label",
        "## Source Register\n\n"
        "| ID | Source Name | Source Type | Date | DOI/URL | Reliability | "
        "Claims Supported |\n"
        "|----|-------------|-------------|------|---------|-------------|-"
        "-----------------|\n"
        "| S01 | Analyst Report | SECONDARY_MEDIA | 2025-01 | https://x.com "
        "| Medium | Market forecast |\n\n"
        "[CONF] According to S01, the market will reach $50B by 2028.\n",
    )


def test_secondary_source_with_infer_label_passes() -> None:
    """SECONDARY source referenced with [推断] in body passes."""
    expect_pass(
        "secondary source with infer label",
        "## Source Register\n\n"
        "| ID | Source Name | Source Type | Date | DOI/URL | Reliability | "
        "Claims Supported |\n"
        "|----|-------------|-------------|------|---------|-------------|-"
        "-----------------|\n"
        "| S01 | Analyst Note | SECONDARY_ANALYST | 2025-03 | https://x.com "
        "| Medium | Market estimate |\n\n"
        "[推断] According to S01, the market might reach $50B by 2028.\n",
    )


def test_primary_company_without_caveat_fails() -> None:
    """PRIMARY_COMPANY source referenced without inline caveat fails."""
    expect_fail(
        "primary company without caveat",
        "## Source Register\n\n"
        "| ID | Source Name | Source Type | Date | DOI/URL | Reliability | "
        "Claims Supported |\n"
        "|----|-------------|-------------|------|---------|-------------|-"
        "-----------------|\n"
        "| S01 | Company PR | PRIMARY_COMPANY | 2025-06 | https://company.com "
        "| High | Product launch |\n\n"
        "[CONF] According to S01, the company plans to invest $10B in R&D.\n",
    )


def test_primary_company_with_caveat_passes() -> None:
    """PRIMARY_COMPANY source with inline caveat passes."""
    expect_pass(
        "primary company with caveat",
        "## Source Register\n\n"
        "| ID | Source Name | Source Type | Date | DOI/URL | Reliability | "
        "Claims Supported |\n"
        "|----|-------------|-------------|------|---------|-------------|-"
        "-----------------|\n"
        "| S01 | Company PR | PRIMARY_COMPANY | 2025-06 | https://company.com "
        "| High | Product launch |\n\n"
        "[CONF] According to S01（来源：厂商自述，非独立验证）, the company "
        "plans to invest $10B in R&D.\n",
    )


def test_no_register_passes() -> None:
    """File without Source Register passes (no data to check)."""
    expect_pass(
        "no source register",
        "# Just a random document\n\n"
        "Some content here without any source register table.\n",
    )


def test_label_in_code_block_ignored() -> None:
    """Confirmed label inside code block is not flagged."""
    expect_pass(
        "label in code block ignored",
        "## Source Register\n\n"
        "| ID | Source Name | Source Type | Date | DOI/URL | Reliability | "
        "Claims Supported |\n"
        "|----|-------------|-------------|------|---------|-------------|-"
        "-----------------|\n"
        "| S01 | Analyst Report | SECONDARY_MEDIA | 2025-01 | https://x.com "
        "| Medium | Market forecast |\n\n"
        "Some text.\n\n"
        "```\n"
        "[CONF] According to S01, the market will reach $50B by 2028.\n"
        "```\n\n"
        "More text.\n",
    )


def test_simplified_secondary_type_fails() -> None:
    """Source type 'secondary' (simplified) with [CONF] also fails."""
    expect_fail(
        "simplified secondary type",
        "## Source Register\n\n"
        "| ID | Source Name | Source Type | Date | DOI/URL | Reliability | "
        "Claims Supported |\n"
        "|----|-------------|-------------|------|---------|-------------|-"
        "-----------------|\n"
        "| S01 | Quick Note | secondary | 2025-01 | https://x.com "
        "| Low | Quick thought |\n\n"
        "[CONF] According to S01, this is a growing trend.\n",
    )


def test_primary_filing_with_confirmed_passes() -> None:
    """PRIMARY_FILING source with [CONF] is allowed (not a self-report)."""
    expect_pass(
        "primary filing with confirmed",
        "## Source Register\n\n"
        "| ID | Source Name | Source Type | Date | DOI/URL | Reliability | "
        "Claims Supported |\n"
        "|----|-------------|-------------|------|---------|-------------|-"
        "-----------------|\n"
        "| S01 | SEC Filing | PRIMARY_FILING | 2025-04 | https://sec.gov "
        "| High | Financial results |\n\n"
        "[CONF] According to S01, the revenue was $10B in Q1 2025.\n",
    )


def test_primary_partner_without_caveat_fails() -> None:
    """PRIMARY_PARTNER source referenced without inline caveat fails."""
    expect_fail(
        "primary partner without caveat",
        "## Source Register\n\n"
        "| ID | Source Name | Source Type | Date | DOI/URL | Reliability | "
        "Claims Supported |\n"
        "|----|-------------|-------------|------|---------|-------------|-"
        "-----------------|\n"
        "| S01 | Partner Blog | PRIMARY_PARTNER | 2025-06 | https://partner.com "
        "| Medium | Integration announcement |\n\n"
        "[CONF] According to S01, the integration is complete.\n",
    )


def test_primary_partner_with_caveat_passes() -> None:
    """PRIMARY_PARTNER source with inline caveat passes."""
    expect_pass(
        "primary partner with caveat",
        "## Source Register\n\n"
        "| ID | Source Name | Source Type | Date | DOI/URL | Reliability | "
        "Claims Supported |\n"
        "|----|-------------|-------------|------|---------|-------------|-"
        "-----------------|\n"
        "| S01 | Partner Blog | PRIMARY_PARTNER | 2025-06 | https://partner.com "
        "| Medium | Integration announcement |\n\n"
        "[CONF] According to S01（来源：厂商自述，非独立验证），the integration "
        "is complete.\n",
    )


def test_infer_label_on_secondary_passes() -> None:
    """[INFER] label on SECONDARY source passes."""
    expect_pass(
        "INFER label on secondary source",
        "## Source Register\n\n"
        "| ID | Source Name | Source Type | Date | DOI/URL | Reliability | "
        "Claims Supported |\n"
        "|----|-------------|-------------|------|---------|-------------|-"
        "-----------------|\n"
        "| S01 | Analyst Note | SECONDARY_ANALYST | 2025-03 | https://x.com "
        "| Medium | Market estimate |\n\n"
        "[INFER] According to S01, the market might reach $50B by 2028.\n",
    )


def test_secondary_source_in_english_sentence_passes() -> None:
    """SECONDARY source and [CONF] in different English sentences passes.

    Regression test for the '.' sentence-splitter fix.
    """
    expect_pass(
        "secondary source in different English sentence",
        "## Source Register\n\n"
        "| ID | Source Name | Source Type | Date | DOI/URL | Reliability | "
        "Claims Supported |\n"
        "|----|-------------|-------------|------|---------|-------------|-"
        "-----------------|\n"
        "| S01 | Analyst Report | SECONDARY_MEDIA | 2025-01 | https://x.com "
        "| Medium | Market forecast |\n\n"
        "A separate claim that is confirmed. "
        "S01 provides a different estimate.\n",
    )


# ---------------------------------------------------------------------------
# Issue #317: 机构来源不应触发 vendor caveat；弱源不得承载 [确认事实]
# ---------------------------------------------------------------------------


def test_multilateral_source_without_caveat_passes() -> None:
    """Primary (multilateral) 来源即使无 caveat 也应通过（非厂商自述）。"""
    expect_pass(
        "multilateral source without caveat",
        "## Source Register\n\n"
        "| ID | Source Name | Source Type | Date | DOI/URL | Reliability | "
        "Claims Supported |\n"
        "|----|-------------|-------------|------|---------|-------------|-"
        "-----------------|\n"
        "| S01 | IEA Report | Primary (multilateral) | 2026-01 | https://iea.org "
        "| High | §3 |\n\n"
        "[CONF] According to S01, data center energy will reach 500 TWh.\n",
    )


def test_government_agency_source_without_caveat_passes() -> None:
    """Primary (US govt agency) 来源不应触发 vendor caveat 检查。"""
    expect_pass(
        "government agency source without caveat",
        "## Source Register\n\n"
        "| ID | Source Name | Source Type | Date | DOI/URL | Reliability | "
        "Claims Supported |\n"
        "|----|-------------|-------------|------|---------|-------------|-"
        "-----------------|\n"
        "| S01 | DOE Report | Primary (US govt agency) | 2026-02 | https://energy.gov "
        "| High | §2 |\n\n"
        "[CONF] According to S01, electricity demand is rising.\n",
    )


def test_crowdsourced_source_with_confirmed_label_fails() -> None:
    """Secondary (crowdsourced) 使用 [CONF] 应报错。"""
    expect_fail(
        "crowdsourced source with confirmed label",
        "## Source Register\n\n"
        "| ID | Source Name | Source Type | Date | DOI/URL | Reliability | "
        "Claims Supported |\n"
        "|----|-------------|-------------|------|---------|-------------|-"
        "-----------------|\n"
        "| S01 | Wiki Compilation | Secondary (crowdsourced) | 2026-01 | "
        "https://wiki.example.com | Low | §2 |\n\n"
        "[CONF] According to S01, the specification is confirmed.\n",
    )


def test_wikipedia_source_with_confirmed_label_fails() -> None:
    """Wikipedia 来源使用 [确认事实] 应报错。"""
    expect_fail(
        "Wikipedia source with confirmed label",
        "## Source Register\n\n"
        "| ID | Source Name | Source Type | Date | DOI/URL | Reliability | "
        "Claims Supported |\n"
        "|----|-------------|-------------|------|---------|-------------|-"
        "-----------------|\n"
        "| S01 | Wikipedia Article | Wikipedia | 2026-01 | https://en.wikipedia.org "
        "| Low | §3 |\n\n"
        "[确认事实] S01 报告称市场规模达 500 亿美元。\n",
    )


def test_rumor_source_with_confirmed_label_fails() -> None:
    """rumor 来源使用 [CONF] 应报错。"""
    expect_fail(
        "rumor source with confirmed label",
        "## Source Register\n\n"
        "| ID | Source Name | Source Type | Date | DOI/URL | Reliability | "
        "Claims Supported |\n"
        "|----|-------------|-------------|------|---------|-------------|-"
        "-----------------|\n"
        "| S01 | Leak Source | rumor | 2026-03 | https://leak.example.com "
        "| Low | §4 |\n\n"
        "[CONF] According to S01, the product will launch in Q3.\n",
    )


def test_crowdsourced_source_with_infer_label_passes() -> None:
    """crowdsourced 来源使用 [推断] 应通过。"""
    expect_pass(
        "crowdsourced source with infer label",
        "## Source Register\n\n"
        "| ID | Source Name | Source Type | Date | DOI/URL | Reliability | "
        "Claims Supported |\n"
        "|----|-------------|-------------|------|---------|-------------|-"
        "-----------------|\n"
        "| S01 | Forum Post | crowdsourced | 2026-01 | "
        "https://forum.example.com | Low | §5 |\n\n"
        "[推断] S01 推测市场可能增长。\n",
    )


def test_primary_vendor_without_caveat_still_fails() -> None:
    """Primary (vendor) 无 caveat 应继续报错（回归）。"""
    expect_fail(
        "primary vendor without caveat still fails",
        "## Source Register\n\n"
        "| ID | Source Name | Source Type | Date | DOI/URL | Reliability | "
        "Claims Supported |\n"
        "|----|-------------|-------------|------|---------|-------------|-"
        "-----------------|\n"
        "| S01 | NVIDIA Blog | Primary (vendor) | 2026-01 | https://nvidia.com "
        "| Medium | Performance claim |\n\n"
        "[CONF] According to S01, the chip is 25x faster.\n",
    )


def test_multilateral_source_with_confirmed_passes() -> None:
    """PRIMARY_INSTITUTION 规范类型使用 [CONF] 应通过（回归）。"""
    expect_pass(
        "PRIMARY_INSTITUTION with confirmed label",
        "## Source Register\n\n"
        "| ID | Source Name | Source Type | Date | DOI/URL | Reliability | "
        "Claims Supported |\n"
        "|----|-------------|-------------|------|---------|-------------|-"
        "-----------------|\n"
        "| S01 | IEA Report | PRIMARY_INSTITUTION | 2026-01 | https://iea.org "
        "| High | §3 |\n\n"
        "[CONF] According to S01, data center energy will reach 500 TWh.\n",
    )


def test_crowdsourced_canonical_type_with_confirmed_fails() -> None:
    """CROWDSOURCED 规范类型使用 [CONF] 应报错。"""
    expect_fail(
        "CROWDSOURCED canonical with confirmed label",
        "## Source Register\n\n"
        "| ID | Source Name | Source Type | Date | DOI/URL | Reliability | "
        "Claims Supported |\n"
        "|----|-------------|-------------|------|---------|-------------|-"
        "-----------------|\n"
        "| S01 | Wiki | CROWDSOURCED | 2026-01 | https://wiki.example.com "
        "| Low | §2 |\n\n"
        "[CONF] According to S01.\n",
    )


def test_unconfirmed_canonical_type_with_confirmed_fails() -> None:
    """UNCONFIRMED 规范类型使用 [CONF] 应报错。"""
    expect_fail(
        "UNCONFIRMED canonical with confirmed label",
        "## Source Register\n\n"
        "| ID | Source Name | Source Type | Date | DOI/URL | Reliability | "
        "Claims Supported |\n"
        "|----|-------------|-------------|------|---------|-------------|-"
        "-----------------|\n"
        "| S01 | Rumor | UNCONFIRMED | 2026-01 | https://example.com "
        "| Low | §2 |\n\n"
        "[CONF] According to S01.\n",
    )


# ---------------------------------------------------------------------------
# Property-based test: _normalize_source_type idempotency and roundtrip
# ---------------------------------------------------------------------------

# All valid canonical types used in the system.
_VALID_CANONICAL_TYPES: frozenset[str] = frozenset({
    "PRIMARY_FILING", "PRIMARY_COMPANY", "PRIMARY_PARTNER",
    "PRIMARY_INSTITUTION", "PRIMARY_DEV", "SECONDARY_MEDIA",
    "SECONDARY_ANALYST", "SECONDARY_FEED", "SECONDARY",
    "TRANSCRIPT", "INFERRED", "UNCONFIRMED", "WEAK_SIGNAL",
    "CROWDSOURCED", "PRIMARY",
})


@given(st.sampled_from([
    "Primary (multilateral)",
    "Primary (multilateral report)",
    "Primary (multilateral analysis)",
    "Primary (US govt agency)",
    "Primary (government agency)",
    "government agency",
    "regulator",
    "public agency",
    "Secondary (crowdsourced)",
    "crowdsourced",
    "Wikipedia",
    "wiki",
    "rumor",
    "leak",
    "传闻",
    "unconfirmed",
    "Primary (vendor)",  # 仍为 PRIMARY_COMPANY
    "PRIMARY_INSTITUTION",
    "CROWDSOURCED",
    "PRIMARY_COMPANY",
    "SECONDARY_MEDIA",
]))
def test_normalize_source_type_property(source_type: str) -> None:
    """Property: normalized canonical type is idempotent and valid.

    For all known free-text and canonical source types, _normalize_source_type
    returns a stable value, running it twice is idempotent, and the output
    is one of the valid canonical types.
    """
    from validate_source_label_consistency import _normalize_source_type

    first = _normalize_source_type(source_type)
    second = _normalize_source_type(first)

    # Idempotent: second application should not change value
    assert first == second, (
        f"normalize_source_type not idempotent for {source_type!r}: "
        f"{first!r} -> {second!r}"
    )
    # Result is not empty
    assert first.strip(), f"normalize_source_type returned empty for {source_type!r}"
    # Result is a valid canonical type
    assert first.upper() in _VALID_CANONICAL_TYPES, (
        f"normalize_source_type returned unexpected canonical type "
        f"{first!r} for {source_type!r}"
    )


def main() -> int:
    tests = [
        test_secondary_source_with_confirmed_label_fails,
        test_secondary_source_with_infer_label_passes,
        test_primary_company_without_caveat_fails,
        test_primary_company_with_caveat_passes,
        test_no_register_passes,
        test_label_in_code_block_ignored,
        test_simplified_secondary_type_fails,
        test_primary_filing_with_confirmed_passes,
        test_primary_partner_without_caveat_fails,
        test_primary_partner_with_caveat_passes,
        test_infer_label_on_secondary_passes,
        test_secondary_source_in_english_sentence_passes,
        # Issue #317 tests
        test_multilateral_source_without_caveat_passes,
        test_government_agency_source_without_caveat_passes,
        test_crowdsourced_source_with_confirmed_label_fails,
        test_wikipedia_source_with_confirmed_label_fails,
        test_rumor_source_with_confirmed_label_fails,
        test_crowdsourced_source_with_infer_label_passes,
        test_primary_vendor_without_caveat_still_fails,
        test_multilateral_source_with_confirmed_passes,
        test_crowdsourced_canonical_type_with_confirmed_fails,
        test_unconfirmed_canonical_type_with_confirmed_fails,
        test_normalize_source_type_property,
    ]
    failures = []
    for test in tests:
        try:
            test()
        except AssertionError as exc:
            failures.append(test.__name__)
            print(f"  FAIL  {test.__name__}: {exc}")

    if failures:
        print(f"\n{len(failures)} test(s) failed: {', '.join(failures)}")
        return 1

    print(f"\nAll {len(tests)} tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
