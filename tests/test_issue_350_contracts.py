#!/usr/bin/env python3
"""Structural contract tests for Issue #350: financial aggregator source taxonomy."""

from __future__ import annotations

import os
import re
import subprocess


REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def read(path: str) -> str:
    with open(os.path.join(REPO_ROOT, path), "r", encoding="utf-8") as f:
        return f.read()


def git_ls_files(pattern: str) -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", pattern],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return [line for line in result.stdout.splitlines() if line]


def tracked_file_exists(path: str) -> bool:
    return path in git_ls_files(path)


def test_source_traceability_mentions_new_financial_aggregator_taxonomy() -> None:
    text = read("references/source-traceability-and-claim-citation.md")
    required = [
        "FILED_DATA_AGGREGATOR",
        "ANALYST_PORTAL_COMPILATION",
        "Reuters LSEG",
        "Bloomberg",
        "Wind",
        "Choice",
        "StockAnalysis",
        "Macrotrends",
        "Finviz",
        "Seeking Alpha",
        "Yahoo Finance",
        "snapshot date",
        "metric basis",
    ]
    missing = [token for token in required if token not in text]
    assert not missing, f"source taxonomy missing tokens: {missing}"


def test_conflict_resolution_distinguishes_filed_aggregators_from_portals() -> None:
    text = read("references/data-conflict-resolution.md")
    assert "FILED_DATA_AGGREGATOR" in text
    assert "ANALYST_PORTAL_COMPILATION" in text
    assert re.search(r"Tier\s*2.*FILED_DATA_AGGREGATOR", text, re.DOTALL), (
        "Tier 2 filed/regulatory aggregators should be mapped explicitly"
    )
    assert re.search(r"Tier\s*5.*ANALYST_PORTAL_COMPILATION", text, re.DOTALL), (
        "Analyst portal compilations should be mapped as secondary-like"
    )


def test_quantitative_role_labeling_requires_aggregator_role_notes() -> None:
    text = read("references/quantitative-role-labeling.md")
    required = [
        "FILED_DATA_AGGREGATOR",
        "aggregated filed data",
        "snapshot date",
        "TTM",
        "metric basis",
        "ANALYST_PORTAL_COMPILATION",
    ]
    missing = [token for token in required if token not in text]
    assert not missing, f"quantitative role labeling missing tokens: {missing}"


def test_listed_company_checklist_mentions_aggregator_guardrails() -> None:
    text = read("checklists/listed-company-report.md")
    required = [
        "FILED_DATA_AGGREGATOR",
        "ANALYST_PORTAL_COMPILATION",
        "snapshot date",
        "metric basis",
        "confirmed",
    ]
    missing = [token for token in required if token not in text]
    assert not missing, f"listed-company checklist missing tokens: {missing}"


def test_no_tracked_markdown_references_missing_tsmc_aggregator_eval() -> None:
    # Build the legacy path from parts so this regression test does not itself
    # contain a literal reference to the missing eval artifact.
    missing_eval = "/".join([
        "evals",
        "cases",
        "tsmc-listed-company-aggregator-source-and-moat-case.md",
    ])
    if tracked_file_exists(missing_eval):
        return

    offenders: list[str] = []
    for path in git_ls_files("*.md") + git_ls_files("**/*.md"):
        full = os.path.join(REPO_ROOT, path)
        if not os.path.exists(full):
            continue
        if missing_eval in read(path):
            offenders.append(path)

    assert not offenders, (
        f"tracked markdown references missing eval {missing_eval}: {offenders}"
    )


def main() -> int:
    tests = [
        test_source_traceability_mentions_new_financial_aggregator_taxonomy,
        test_conflict_resolution_distinguishes_filed_aggregators_from_portals,
        test_quantitative_role_labeling_requires_aggregator_role_notes,
        test_listed_company_checklist_mentions_aggregator_guardrails,
        test_no_tracked_markdown_references_missing_tsmc_aggregator_eval,
    ]
    failures: list[str] = []
    for test in tests:
        try:
            test()
            print(f"  PASS  {test.__name__}")
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
