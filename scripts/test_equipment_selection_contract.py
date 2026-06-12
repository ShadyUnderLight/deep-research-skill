#!/usr/bin/env python3
"""
Contract tests for Issue #262 — equipment-selection cost sensitivity, decision tree, and build-ready configuration.

Tests two layers:
  1. property-based: table column consistency, section hierarchy integrity
  2. content-based: required keywords/subsections present in template and checklists

Following the pattern from test_benchmark_comparability_contract.py
and test_market_outlook_monitoring_contract.py.
"""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def assert_contains(path: str, needles: list[str]) -> None:
    text = read(path)
    missing = [needle for needle in needles if needle not in text]
    assert not missing, f"{path} missing: {', '.join(missing)}"


def lines_with(text: str, pattern: str) -> list[str]:
    """Return lines that contain the given regex pattern."""
    return [ln for ln in text.split("\n") if re.search(pattern, ln)]


# ---------------------------------------------------------------------------
# Property-based: every pipe-delimited table in the equipment-selection
# section must have consistent column counts (header == data rows).
# ---------------------------------------------------------------------------

def _extract_tables(markdown: str) -> list[list[list[str]]]:
    """
    Naive pipe-table extractor.

    Returns a list of tables, each table being a list of rows,
    each row being a list of cell strings (stripped).

    Only captures tables where the header row is followed by a separator row
    (|---|...|). Assumes no blank lines inside a table.
    """
    tables: list[list[list[str]]] = []
    lines = markdown.split("\n")
    i = 0
    while i < len(lines):
        ln = lines[i]
        # Detect header row: starts with '|'
        if ln.lstrip().startswith("|") and "---" not in ln:
            # Check next line is a separator
            if i + 1 < len(lines) and "---" in lines[i + 1]:
                table_rows = [ln]
                i += 2  # skip separator
                while i < len(lines) and lines[i].lstrip().startswith("|"):
                    table_rows.append(lines[i])
                    i += 1
                parsed = [[c.strip() for c in row.strip().split("|")[1:-1]]
                          for row in table_rows]
                tables.append(parsed)
                continue
        i += 1
    return tables


def test_property_table_column_consistency() -> None:
    """
    Property: every pipe-delimited table in the equipment-selection section
    has the same number of columns in the header and each data row.
    """
    text = read("references/decision-report-template.md")

    # Isolate the equipment-selection section:
    # starts at "For equipment-selection / procurement / home-server-planning tasks"
    # ends at the next section header "For market-entry" or end of file.
    start_marker = "For equipment-selection / procurement / home-server-planning tasks, prefer this stronger structure"
    end_marker = "\n## "
    # Find start
    start_idx = text.find(start_marker)
    assert start_idx != -1, "Could not find equipment-selection section start"

    # Find next top-level section (##) after start
    # Actually, let's find the start of the equipment section more precisely
    # The section starts with "### Equipment selection…" header
    # Use the ### header directly

    eq_header = "### Cost sensitivity table"
    # Actually, this test will run BEFORE implementation, so the section doesn't exist yet.
    # Let's scope the test to run only if the section exists.
    # If it doesn't exist yet (RED phase), we just skip the property test.
    if eq_header not in text:
        # In RED phase, this test has nothing to validate yet
        return

    # Find equipment-selection subsections area
    eq_start = text.find(eq_header)
    # Find next top-level section after it (next "## ")
    # Search from eq_start
    rest = text[eq_start + len(eq_header):]
    # Find next "## " at line start
    next_section = re.search(r"^## ", rest, re.MULTILINE)
    if next_section:
        zone = text[eq_start:eq_start + len(eq_header) + next_section.start()]
    else:
        zone = text[eq_start:]

    tables = _extract_tables(zone)
    violations = []
    for ti, table in enumerate(tables):
        if len(table) < 2:
            continue  # header only, nothing to check
        ncols = len(table[0])
        for ri, row in enumerate(table[1:], start=1):
            if len(row) != ncols:
                violations.append(
                    f"  Table #{ti}, row #{ri}: {len(row)} cols, expected {ncols}"
                )
    assert not violations, (
        f"Column count inconsistency in equipment-selection zone:\n"
        + "\n".join(violations)
    )


def test_property_table_has_minimum_two_rows() -> None:
    """
    Property: every table (header + separator + ≥1 data row).
    A table with only a header is degenerate.
    """
    text = read("references/decision-report-template.md")
    eq_header = "### Cost sensitivity table"
    if eq_header not in text:
        return  # RED phase — not yet implemented
    eq_start = text.find(eq_header)
    rest = text[eq_start:]
    next_section = re.search(r"^## ", rest, re.MULTILINE)
    if next_section:
        zone = rest[:next_section.start()]
    else:
        zone = rest

    tables = _extract_tables(zone)
    degenerate = [ti for ti, tbl in enumerate(tables) if len(tbl) < 2]
    assert not degenerate, f"Tables with <2 rows (no data): indices {degenerate}"


# ---------------------------------------------------------------------------
# Content-based: required subsections in decision-report-template.md
# ---------------------------------------------------------------------------

def test_cost_sensitivity_table_section_present() -> None:
    """C1.1: Cost sensitivity table subsection exists."""
    assert_contains(
        "references/decision-report-template.md",
        [
            "### Cost sensitivity table",
        ],
    )


def test_cost_sensitivity_table_columns() -> None:
    """C1.1: Cost sensitivity table has required columns."""
    assert_contains(
        "references/decision-report-template.md",
        [
            "Active usage level",
            "Local fixed cost",
            "Local variable cost",
            "Cloud variable cost",
            "Break-even interpretation",
            "Numeric role",
        ],
    )


def test_cost_sensitivity_shows_driving_variable() -> None:
    """C1.1: States that cost sensitivity must show the driving variable."""
    assert_contains(
        "references/decision-report-template.md",
        [
            "monthly active GPU hours",
        ],
    )


def test_cost_sensitivity_numeric_role_labeling() -> None:
    """C1.1: All cost figures must carry numeric role labels."""
    assert_contains(
        "references/decision-report-template.md",
        [
            "numeric role",
        ],
    )


def test_decision_tree_subsection_present() -> None:
    """C1.2: Decision tree subsection exists."""
    assert_contains(
        "references/decision-report-template.md",
        [
            "### Decision tree",
        ],
    )


def test_decision_tree_content() -> None:
    """C1.2: Decision tree has required content."""
    assert_contains(
        "references/decision-report-template.md",
        [
            "branching logic",
            "Mermaid",
        ],
    )


def test_build_ready_config_subsection_present() -> None:
    """C1.3: Build-ready configuration table subsection exists."""
    assert_contains(
        "references/decision-report-template.md",
        [
            "### Build-ready configuration table",
        ],
    )


def test_build_ready_config_columns() -> None:
    """C1.3: Build-ready table has required columns."""
    assert_contains(
        "references/decision-report-template.md",
        [
            "Scenario",
            "Recommended stack",
            "Included cost items",
            "Excluded",
            "Operating burden",
            "Expansion path",
        ],
    )


def test_build_ready_minimum_fields() -> None:
    """C1.3: Build-ready table states minimum fields."""
    assert_contains(
        "references/decision-report-template.md",
        [
            "hardware components",
            "software",
        ],
    )


# ---------------------------------------------------------------------------
# Content-based: new audit items in final-audit.md
# ---------------------------------------------------------------------------

def test_final_audit_cost_sensitivity_check() -> None:
    """C2.1: Cost sensitivity audit item exists."""
    assert_contains(
        "checklists/final-audit.md",
        [
            "cost sensitivity variables",
            "monthly active GPU hours",
            "break-even analysis",
        ],
    )


def test_final_audit_budget_inclusion_exclusion_hard_fail() -> None:
    """C2.2: Budget inclusion/exclusion hard-fail audit item exists."""
    assert_contains(
        "checklists/final-audit.md",
        [
            "budget assumptions declare what is included and",
            "hard-fail",
        ],
    )


def test_final_audit_build_ready_config_check() -> None:
    """C2.3: Build-ready configuration table audit item exists."""
    assert_contains(
        "checklists/final-audit.md",
        [
            "build-ready configuration table",
            "operating burden",
            "expansion path",
        ],
    )


# ---------------------------------------------------------------------------
# Content-based: new audit item in option-selection-final-audit.md
# ---------------------------------------------------------------------------

def test_option_selection_build_ready_friction() -> None:
    """C3.1: Build-ready friction check exists in option-selection audit."""
    assert_contains(
        "checklists/option-selection-final-audit.md",
        [
            "physical hardware",
            "build-ready",
            "hidden friction",
        ],
    )


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def main() -> int:
    all_tests = [
        # Property-based
        test_property_table_column_consistency,
        test_property_table_has_minimum_two_rows,
        # decision-report-template.md
        test_cost_sensitivity_table_section_present,
        test_cost_sensitivity_table_columns,
        test_cost_sensitivity_shows_driving_variable,
        test_cost_sensitivity_numeric_role_labeling,
        test_decision_tree_subsection_present,
        test_decision_tree_content,
        test_build_ready_config_subsection_present,
        test_build_ready_config_columns,
        test_build_ready_minimum_fields,
        # final-audit.md
        test_final_audit_cost_sensitivity_check,
        test_final_audit_budget_inclusion_exclusion_hard_fail,
        test_final_audit_build_ready_config_check,
        # option-selection-final-audit.md
        test_option_selection_build_ready_friction,
    ]

    failures = []
    for test in all_tests:
        try:
            test()
            print(f"  PASS  {test.__name__}")
        except AssertionError as exc:
            print(f"  FAIL  {test.__name__}: {exc}")
            failures.append(test.__name__)

    if failures:
        print(f"\n{len(failures)} test(s) failed: {', '.join(failures)}")
        return 1

    print(f"\nAll {len(all_tests)} tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
