#!/usr/bin/env python3
"""Regression tests for declared-not-executed report discipline."""

from pathlib import Path
import subprocess
import sys
import tempfile


SCRIPT = str(Path(__file__).resolve().parent / "validate_declared_execution.py")


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


def test_opam_declared_zero_applied_fails() -> None:
    expect_fail(
        "O/P/A/M declared but not applied",
        """
## Method

This report uses O/P/A/M labels: O = observed metric, P = proxy,
A = assumption, M = model output.

## Scenario table

| Metric | Base | Upside |
|--------|------|--------|
| Market size | $10B | $15B |
| Adoption | 25% | 35% |
| Payback | 18 months | 12 months |
""",
    )


def test_opam_declared_applied_passes() -> None:
    expect_pass(
        "O/P/A/M declared and applied",
        """
## Method

This report uses O/P/A/M labels: O = observed metric, P = proxy,
A = assumption, M = model output.

## Scenario table

| Metric | Base | Upside | Role |
|--------|------|--------|------|
| Market size | $10B | $15B | A |
| Adoption | 25% | 35% | M |
| Payback | 18 months | 12 months | M |
""",
    )


def test_source_register_zero_body_refs_fails() -> None:
    expect_fail(
        "Source Register declared but no body citations",
        """
## Findings

The market is growing quickly and adoption is likely to accelerate.

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Example market report | secondary | 2026-01-01 | https://example.com | medium | § Findings |
| S02 | Example filing | primary | 2026-02-01 | https://example.com/filing | high | § Findings |
""",
    )


def test_academic_framework_no_mapping_fails() -> None:
    expect_fail(
        "academic framework declared without mapping",
        """
## Method

Evidence is evaluated on two dimensions: study design quality × venue prestige.

## Findings

Smith 2025 provides the strongest evidence; Lee 2024 is weaker.
""",
    )


def test_academic_framework_mapping_present_passes() -> None:
    expect_pass(
        "academic framework mapping present",
        """
## Method

Evidence is evaluated on two dimensions: study design quality × venue prestige.

## Evidence mapping table

| Source | Study design quality | Venue prestige | Overall assessment |
|--------|----------------------|----------------|--------------------|
| S01 | RCT | Tier 1 journal | strong |
| S02 | cohort study | Tier 3 journal | medium |
""",
    )


def main() -> int:
    tests = [
        test_opam_declared_zero_applied_fails,
        test_opam_declared_applied_passes,
        test_source_register_zero_body_refs_fails,
        test_academic_framework_no_mapping_fails,
        test_academic_framework_mapping_present_passes,
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
