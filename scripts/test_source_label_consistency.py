#!/usr/bin/env python3
"""Tests for validate_source_label_consistency.py."""

from pathlib import Path
import subprocess
import sys
import tempfile

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
