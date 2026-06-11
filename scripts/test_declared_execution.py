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


def test_source_register_uncited_inflation_fails() -> None:
    expect_fail(
        "Source Register inflation fails when most entries are uncited",
        """
## Findings

The market is growing quickly and adoption is likely to accelerate [S01].

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Example market report | secondary | 2026-01-01 | https://example.com/1 | medium | § Findings |
| S02 | Example filing | primary | 2026-02-01 | https://example.com/2 | high | § Findings |
| S03 | Example benchmark | secondary | 2026-03-01 | https://example.com/3 | medium | § Findings |
| S04 | Example interview | secondary | 2026-04-01 | https://example.com/4 | medium | § Findings |
""",
    )


def test_source_register_fully_cited_passes() -> None:
    expect_pass(
        "Source Register entries cited in body pass",
        """
## Findings

The market is growing quickly [S01][S02].
Adoption is likely to accelerate [S03][S04].

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Example market report | secondary | 2026-01-01 | https://example.com/1 | medium | § Findings |
| S02 | Example filing | primary | 2026-02-01 | https://example.com/2 | high | § Findings |
| S03 | Example benchmark | secondary | 2026-03-01 | https://example.com/3 | medium | § Findings |
| S04 | Example interview | secondary | 2026-04-01 | https://example.com/4 | medium | § Findings |
""",
    )


def test_source_register_arxiv_equivalent_refs_pass() -> None:
    expect_pass(
        "Source Register entries cited by arXiv IDs pass",
        """
## Findings

The base detector follows the YOLOv3 formulation (Redmon, 2018, arXiv:1804.02767).
The transformer baseline follows the original attention paper (Vaswani et al. 2017, arXiv:1706.03762).

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | YOLOv3: An Incremental Improvement | primary | 2018-04-08 | https://arxiv.org/abs/1804.02767 | high | § Findings |
| S02 | Attention Is All You Need | primary | 2017-06-12 | https://arxiv.org/abs/1706.03762 | high | § Findings |
""",
    )


def test_source_register_doi_equivalent_refs_pass() -> None:
    expect_pass(
        "Source Register entries cited by DOI pass",
        """
## Findings

The intervention effect is taken from the Nature study doi:10.1038/nature14539.
The follow-up mechanism is described in https://doi.org/10.1145/3366423.3380295.

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Nature intervention study | primary | 2015-05-01 | https://doi.org/10.1038/nature14539 | high | § Findings |
| S02 | Systems follow-up paper | primary | 2020-04-01 | 10.1145/3366423.3380295 | high | § Findings |
""",
    )


def test_source_register_author_year_equivalent_refs_pass() -> None:
    expect_pass(
        "Source Register entries cited by Author-Year pass",
        """
## Findings

The first cohort evidence comes from (Smith, 2025, Nature Medicine).
The robustness check follows Lee et al. 2024.

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Smith 2025 Nature Medicine cohort study | primary | 2025-02-01 | https://doi.org/10.1000/smith2025 | high | § Findings |
| S02 | Lee et al. 2024 robustness analysis | primary | 2024-08-01 | https://doi.org/10.1000/lee2024 | high | § Findings |
""",
    )


def test_source_register_unique_natural_language_refs_pass() -> None:
    expect_pass(
        "Source Register entries cited by unique natural-language attribution pass",
        """
## Findings

据 FY2025 年报，公司海外收入占比继续提升。
2026Q1 业绩公告披露，同店销售恢复到正增长区间。

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | ExampleCo FY2025 Annual Report | primary | 2026-03-31 | https://example.com/fy2025-annual-report | high | § Findings |
| S02 | ExampleCo 2026Q1 Earnings Announcement | primary | 2026-04-30 | https://example.com/2026q1-results | high | § Findings |
""",
    )


def test_source_register_vague_natural_language_refs_fail() -> None:
    expect_fail(
        "vague natural-language attribution does not count as equivalent citation",
        """
## Findings

据公开资料，公司海外收入占比继续提升。

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | ExampleCo FY2025 Annual Report | primary | 2026-03-31 | https://example.com/fy2025-annual-report | high | § Findings |
""",
    )


def test_source_register_ambiguous_natural_language_refs_fail() -> None:
    expect_fail(
        "ambiguous natural-language attribution does not count as equivalent citation",
        """
## Findings

据年报，公司海外收入占比继续提升。

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | ExampleCo FY2024 Annual Report | primary | 2025-03-31 | https://example.com/fy2024-annual-report | high | § Findings |
| S02 | ExampleCo FY2025 Annual Report | primary | 2026-03-31 | https://example.com/fy2025-annual-report | high | § Findings |
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
        test_source_register_uncited_inflation_fails,
        test_source_register_fully_cited_passes,
        test_source_register_arxiv_equivalent_refs_pass,
        test_source_register_doi_equivalent_refs_pass,
        test_source_register_author_year_equivalent_refs_pass,
        test_source_register_unique_natural_language_refs_pass,
        test_source_register_vague_natural_language_refs_fail,
        test_source_register_ambiguous_natural_language_refs_fail,
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
