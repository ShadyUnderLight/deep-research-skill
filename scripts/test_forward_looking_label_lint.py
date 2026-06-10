#!/usr/bin/env python3
"""Regression tests for validate_forward_looking_labels.py."""

from pathlib import Path
import subprocess
import sys
import tempfile


SCRIPT = str(Path(__file__).resolve().parent / "validate_forward_looking_labels.py")


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


def test_forward_chinese_confirmed_fails() -> None:
    expect_fail(
        "Chinese forward-looking confirmed label",
        "[确认] GPT-5 预计需 500+ GWh 电力。",
    )


def test_forward_english_confirmed_fails() -> None:
    expect_fail(
        "English forecast confirmed label",
        "[CONF] The market is forecast to reach $50B by 2028.",
    )


def test_future_by_year_confirmed_fails() -> None:
    expect_fail(
        "by-year future confirmed label",
        "[Confirmed] AI video revenue by 2028 will reach $17-20B.",
    )


def test_analyst_estimate_passes() -> None:
    expect_pass(
        "analyst estimate role passes",
        "[ANALYST_EST] 据 Gartner 2026-01 预计，2028 年市场规模达 $50B [S01]。",
    )


def test_mixed_confirmed_and_estimate_fails() -> None:
    expect_fail(
        "mixed confirmed and estimate labels fails",
        "[CONF][ANALYST_EST] 据 Gartner 2026-01 预计，2028 年市场规模达 $50B。",
    )


def test_scenario_assumption_passes() -> None:
    expect_pass(
        "scenario assumption role passes",
        "[SCENARIO] 假设推理成本继续下降，2028 年市场规模将达 $17-20B。",
    )


def test_observed_historical_confirmed_passes() -> None:
    expect_pass(
        "observed historical confirmed fact passes",
        "[确认] 2025 年实际营收为 $10B，来自已审计年报。",
    )


def test_source_event_without_forecast_number_passes() -> None:
    expect_pass(
        "forecast publication event passes",
        "[确认] Gartner 于 2026-01 发布了 AI 市场预测报告。",
    )


def main() -> int:
    tests = [
        test_forward_chinese_confirmed_fails,
        test_forward_english_confirmed_fails,
        test_future_by_year_confirmed_fails,
        test_analyst_estimate_passes,
        test_mixed_confirmed_and_estimate_fails,
        test_scenario_assumption_passes,
        test_observed_historical_confirmed_passes,
        test_source_event_without_forecast_number_passes,
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
