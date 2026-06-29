#!/usr/bin/env python3
"""
Contract tests for Issue #353: Sports prediction / regulatory / market-outlook
execution closure — Phase A: core loop.

Tests validate:
  C1: ROUTING-MATRIX.md constrained-choice section has sports prediction trigger
      and concrete boundary examples (Shared-workflow escape hatch guard).
  C2: evals/INDEX.md has three new case rows with #353 in Related issue/PR.
  C3: python3 scripts/test_eval_index.py passes (verifies git-tracked + INDEX
      consistency).

Usage:
    python tests/test_issue_353_contracts.py
    python -m pytest tests/test_issue_353_contracts.py -v

Expected BEFORE implementation: ALL FAIL
Expected AFTER implementation:  ALL PASS
"""

from __future__ import annotations

import os
import re
import subprocess
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def read(path: str) -> str:
    with open(os.path.join(REPO_ROOT, path), "r", encoding="utf-8") as f:
        return f.read()


def file_exists(path: str) -> bool:
    return os.path.exists(os.path.join(REPO_ROOT, path))


# ════════════════════════════════════════════════════════════════════════════
# C1: ROUTING-MATRIX.md — constrained-choice sports prediction trigger
# ════════════════════════════════════════════════════════════════════════════

ROUTING_MATRIX = "ROUTING-MATRIX.md"

# Expected keyword groups in the constrained-choice trigger section.
# At least ONE keyword from each group must be present to satisfy the
# sports-prediction catch-all contract.
_SPORTS_KEYWORDS = [
    r"sport",
    r"match\s+(outcome|prediction|result)",
    r"赛果",
    r"predict(?:ing|ion)",
    r"outcome\s+(ranking|probability|distribution)",
    r"upset\s+path",
    r"爆冷",
    r"胜平负",
    r"比分分布",
    r"晋级路径",
]

# Expected concrete boundary example patterns (e.g. "...
# → Constrained Choice")
_BOUNDARY_PATTERNS = [
    r"→\s*Constrained\s+Choice",
    r"Constrained\s+Choice.*(?:sport|match|赛果|爆冷|预测)",
    r"(?:sport|match|赛果|爆冷|预测).*Constrained\s+Choice",
]


# Extract the constrained-choice section from ROUTING-MATRIX.md
def _get_constrained_choice_section() -> str:
    """Return the constrained-choice route section as a single string."""
    content = read(ROUTING_MATRIX)
    # Section starts at "## Route: Constrained Choice"
    match = re.search(
        r"^## Route:\s*Constrained\s+Choice\s*/.*$",
        content,
        re.MULTILINE,
    )
    assert match, "Constrained Choice section not found in ROUTING-MATRIX.md"
    start = match.start()
    # Section ends at next "## Route:" or end-of-file
    next_section = re.search(r"\n## Route:", content[match.end() :])
    end = match.end() + next_section.start() if next_section else len(content)
    return content[start:end]


def test_c1_file_exists() -> None:
    """C1: ROUTING-MATRIX.md must exist."""
    assert file_exists(ROUTING_MATRIX), f"Missing: {ROUTING_MATRIX}"


def test_c1_constrained_choice_section_has_sports_trigger() -> None:
    """C1: constrained-choice trigger section must mention sports prediction."""
    section = _get_constrained_choice_section()
    # At least one sports keyword must match
    assert any(
        re.search(kw, section, re.IGNORECASE) for kw in _SPORTS_KEYWORDS
    ), (
        "Constrained-choice section lacks sports/赛果/prediction trigger keywords.\n"
        f"Checked patterns: {_SPORTS_KEYWORDS}"
    )


def test_c1_has_concrete_boundary_example() -> None:
    """C1: constrained-choice must have concrete boundary example with sports."""
    section = _get_constrained_choice_section()
    assert any(
        re.search(pat, section, re.IGNORECASE) for pat in _BOUNDARY_PATTERNS
    ), (
        "Constrained-choice section lacks concrete boundary example "
        "involving sports prediction (e.g. '... → Constrained Choice').\n"
        f"Checked patterns: {_BOUNDARY_PATTERNS}"
    )


# ════════════════════════════════════════════════════════════════════════════
# C2: evals/INDEX.md — three new cases with #353 in Related issue/PR
# ════════════════════════════════════════════════════════════════════════════

INDEX_FILE = "evals/INDEX.md"

_NEW_CASES = [
    "evals/cases/world-cup-expansion-regulatory-contract-and-source-fail-case.md",
    "evals/cases/world-cup-sports-broadcasting-market-outlook-source-and-monitoring-case.md",
    "evals/cases/argentina-cape-verde-constrained-choice-route-and-source-fail-case.md",
]


def _parse_index_rows() -> list[dict[str, str]]:
    """Parse INDEX.md rows into dicts keyed by column name."""
    text = read(INDEX_FILE)
    # Find the header row to get column names
    lines = text.splitlines()
    header_line = None
    for line in lines:
        if line.startswith("| Path") and "Primary route" in line:
            header_line = line
            break
    assert header_line, "Could not find INDEX.md header row"
    # Count columns from the header
    column_cells = [c.strip() for c in header_line.strip("|").split("|")]
    columns = column_cells  # Ordered column names

    rows = []
    for line in lines:
        if line.startswith("| `evals/cases/") and line.endswith(" |"):
            cells = [c.strip().strip("`") for c in line.strip("|").split("|")]
            assert len(cells) == len(columns), (
                f"INDEX.md row has {len(cells)} cells, "
                f"expected {len(columns)}: {line[:80]}"
            )
            rows.append(dict(zip(columns, cells)))
    return rows


def test_c2_index_file_exists() -> None:
    """C2: evals/INDEX.md must exist."""
    assert file_exists(INDEX_FILE), f"Missing: {INDEX_FILE}"


def test_c2_three_new_cases_have_related_issue_353() -> None:
    """C2: Three new eval cases must reference #353 in Related issue/PR."""
    rows = _parse_index_rows()
    found = {r["Path"]: r["Related issue / PR"] for r in rows}

    for case_file in _NEW_CASES:
        assert case_file in found, (
            f"Case {case_file} not found in INDEX.md rows"
        )
        related = found[case_file]
        assert "#353" in related, (
            f"Case {case_file}: Related issue/PR '{related}' "
            f"does not contain '#353'"
        )


def test_c2_expansion_case_also_refs_341_343() -> None:
    """C2: expansion case must also reference #341 and #343 (regression check)."""
    rows = _parse_index_rows()
    found = {r["Path"]: r["Related issue / PR"] for r in rows}

    expansion = "evals/cases/world-cup-expansion-regulatory-contract-and-source-fail-case.md"
    related = found.get(expansion, "")
    assert "#341" in related, f"Expansion case missing #341 reference: {related}"
    assert "#343" in related, f"Expansion case missing #343 reference: {related}"


# ════════════════════════════════════════════════════════════════════════════
# C3: test_eval_index.py passes
# ════════════════════════════════════════════════════════════════════════════


def test_c3_eval_index_regression_passes() -> None:
    """C3: python3 scripts/test_eval_index.py must pass (exit code 0)."""
    result = subprocess.run(
        [sys.executable, "scripts/test_eval_index.py"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"test_eval_index.py failed with exit code {result.returncode}.\n"
        f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    )


# ════════════════════════════════════════════════════════════════════════════
# Main
# ════════════════════════════════════════════════════════════════════════════


def main() -> int:
    tests = [
        test_c1_file_exists,
        test_c1_constrained_choice_section_has_sports_trigger,
        test_c1_has_concrete_boundary_example,
        test_c2_index_file_exists,
        test_c2_three_new_cases_have_related_issue_353,
        test_c2_expansion_case_also_refs_341_343,
        test_c3_eval_index_regression_passes,
    ]
    failures = []
    for test in tests:
        try:
            test()
            print(f"  PASS  {test.__name__}")
        except (AssertionError, Exception) as exc:
            failures.append(test.__name__)
            print(f"  FAIL  {test.__name__}: {exc}")

    if failures:
        print(f"\n{len(failures)} test(s) failed: {', '.join(failures)}")
        return 1

    print(f"\nAll {len(tests)} tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
