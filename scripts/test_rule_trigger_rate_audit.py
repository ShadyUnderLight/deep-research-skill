#!/usr/bin/env python3
"""Regression checks for the first rule-trigger-rate audit artifact."""

from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "evals" / "meta" / "rule-trigger-rate-audit-2026-06.md"
ROADMAP = ROOT / "ROADMAP.md"

DISCIPLINES = [
    "Current-state verification",
    "Source traceability",
    "Forward-looking claims",
    "Quantitative role labeling",
    "Scope completeness",
    "Decision utility",
    "Delivery cleanliness",
    "Target-language coherence",
]

STATES = {
    "N/A",
    "Triggered",
    "Missing trigger",
    "Declared only",
    "Failed execution",
}


def tracked_case_count() -> int:
    result = subprocess.run(
        ["git", "ls-files", "evals/cases/*.md"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return len([line for line in result.stdout.splitlines() if line.strip()])


def test_audit_file_exists() -> None:
    assert AUDIT.exists(), f"missing audit artifact: {AUDIT}"


def test_audit_metadata_matches_tracked_cases() -> None:
    text = AUDIT.read_text(encoding="utf-8")
    match = re.search(r"^- Case count: (\d+) tracked Markdown cases$", text, re.MULTILINE)
    assert match, "audit must record tracked Markdown case count"
    assert int(match.group(1)) == tracked_case_count()
    assert re.search(r"^- Commit anchor: `[0-9a-f]{7,40}`$", text, re.MULTILINE)


def test_discipline_summary_covers_all_core_disciplines() -> None:
    text = AUDIT.read_text(encoding="utf-8")
    expected_header = (
        "| Discipline | Applicable cases | Triggered | Missing/Declared-only | "
        "Failed execution | Rate | Status | Notes |"
    )
    assert expected_header in text
    for discipline in DISCIPLINES:
        assert re.search(rf"^\| {re.escape(discipline)} \|", text, re.MULTILINE), (
            f"missing discipline summary row for {discipline}"
        )


def test_case_matrix_has_one_row_per_tracked_case_and_known_states() -> None:
    text = AUDIT.read_text(encoding="utf-8")
    case_rows = [
        line for line in text.splitlines()
        if line.startswith("| `evals/cases/") and line.endswith(" |")
    ]
    assert len(case_rows) == tracked_case_count()

    for row in case_rows:
        cells = [cell.strip().strip("`") for cell in row.strip("|").split("|")]
        assert len(cells) == 11, f"unexpected case-matrix shape: {row}"
        for state in cells[2:10]:
            assert state in STATES, f"unknown audit state {state!r} in row: {row}"


def test_roadmap_marks_first_audit_done() -> None:
    text = ROADMAP.read_text(encoding="utf-8")
    done_section = text.split("### P1 — Remaining", maxsplit=1)[0]
    remaining_section = text.split("### P1 — Remaining", maxsplit=1)[1]

    assert "rule-trigger-rate audit" in done_section
    assert "evals/meta/rule-trigger-rate-audit-2026-06.md" in done_section
    assert "Run first rule-trigger-rate audit" not in remaining_section


def main() -> int:
    tests = [
        test_audit_file_exists,
        test_audit_metadata_matches_tracked_cases,
        test_discipline_summary_covers_all_core_disciplines,
        test_case_matrix_has_one_row_per_tracked_case_and_known_states,
        test_roadmap_marks_first_audit_done,
    ]
    failures = []
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
