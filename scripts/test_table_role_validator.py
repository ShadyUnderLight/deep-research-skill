#!/usr/bin/env python3
"""Tests for validate_table_role_labels.py."""

from pathlib import Path
import subprocess
import sys
import tempfile

SCRIPT = str(Path(__file__).resolve().parent / "validate_table_role_labels.py")


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

def test_table_with_role_column_passes() -> None:
    """Table with explicit 数字角色 column passes."""
    expect_pass(
        "table with 数字角色 column",
        "| 指标 | 数字角色 | 数值 |\n"
        "|------|----------|------|\n"
        "| Revenue | 观察值 | $100M |\n"
        "| Growth | 估算 | 20% |\n"
        "| Profit | 推断 | $50M |\n",
    )


def test_table_without_role_column_fails() -> None:
    """Table with 3+ data rows and no role keywords fails."""
    expect_fail(
        "table without role column",
        "| 公司 | 营收 | 利润 |\n"
        "|------|------|------|\n"
        "| Apple | $100B | $20B |\n"
        "| Google | $80B | $15B |\n"
        "| Microsoft | $60B | $12B |\n",
    )


def test_key_value_table_not_flagged() -> None:
    """Simple key-value tables should not be flagged."""
    expect_pass(
        "key-value table",
        "| Key | Value |\n"
        "|-----|-------|\n"
        "| Name | Apple |\n"
        "| Revenue | $100B |\n"
        "| Growth | 20% |\n",
    )


def test_role_header_row_passes() -> None:
    """Table with a role header row between header and data passes."""
    expect_pass(
        "table with role header row",
        "| | 2023 | 2024 | 2025 |\n"
        "|---|------|------|------|\n"
        "| 数字角色 | 观察值 | 估算 | 预测 |\n"
        "| Revenue | 100M | 120M | 150M |\n"
        "| Growth | 10% | 20% | 25% |\n"
        "| Profit | 50M | 60M | 70M |\n",
    )


def test_role_values_in_data_passes() -> None:
    """Table where data cells contain role keywords passes."""
    expect_pass(
        "table with role values in data",
        "| 指标 | 2023 | 2024 |\n"
        "|------|------|------|\n"
        "| Revenue | 假设 $100M | 估算 $120M |\n"
        "| Growth | 观察值 10% | 假设 15% |\n"
        "| Profit | 模型输出 $50M | 估算 $60M |\n",
    )


def test_small_table_without_role_passes() -> None:
    """Table with fewer than 3 data rows and no role keywords passes (too small to flag)."""
    expect_pass(
        "small table without role",
        "| A | B |\n"
        "|---|---|\n"
        "| 1 | 2 |\n"
        "| 3 | 4 |\n",
    )


def test_table_in_code_block_ignored() -> None:
    """Table inside a fenced code block should be ignored."""
    expect_pass(
        "table inside code block",
        "Some text.\n\n"
        "```\n"
        "| A | B | C |\n"
        "|---|---|---|\n"
        "| 1 | 2 | 3 |\n"
        "| 4 | 5 | 6 |\n"
        "| 7 | 8 | 9 |\n"
        "```\n\n"
        "More text.\n",
    )


def test_english_role_column_passes() -> None:
    """Table with English epistemic role column passes."""
    expect_pass(
        "table with epistemic role column",
        "| Metric | Epistemic Role | Value |\n"
        "|--------|----------------|-------|\n"
        "| Revenue | observed | $100M |\n"
        "| Growth | estimate | 20% |\n"
        "| Profit | inferred | $50M |\n",
    )


def main() -> int:
    tests = [
        test_table_with_role_column_passes,
        test_table_without_role_column_fails,
        test_key_value_table_not_flagged,
        test_role_header_row_passes,
        test_role_values_in_data_passes,
        test_small_table_without_role_passes,
        test_table_in_code_block_ignored,
        test_english_role_column_passes,
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
