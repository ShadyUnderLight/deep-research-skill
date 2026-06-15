#!/usr/bin/env python3
"""Regression checks for the eval asset index."""

from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "evals" / "INDEX.md"
README = ROOT / "evals" / "README.md"

REQUIRED_COLUMNS = [
    "Path",
    "Primary route",
    "Secondary route",
    "Failure family",
    "Primary discipline",
    "Status",
    "Intervention target",
    "Current rule status",
    "Related issue / PR",
    "Notes",
]

ALLOWED_STATUSES = {
    "active",
    "candidate",
    "needs-review",
    "stale",
    "superseded",
}

ALLOWED_RULE_STATUSES = {
    "pass",
    "conditional-pass",
    "fail",
    "warn",
    "manual-review",
}


def tracked_cases() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "evals/cases/*.md"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return sorted(line for line in result.stdout.splitlines() if line.strip())


def parse_index_rows() -> list[dict[str, str]]:
    assert INDEX.exists(), f"missing eval index: {INDEX}"
    text = INDEX.read_text(encoding="utf-8")
    rows = [
        line for line in text.splitlines()
        if line.startswith("| `evals/cases/") and line.endswith(" |")
    ]
    parsed = []
    for row in rows:
        cells = [cell.strip().strip("`") for cell in row.strip("|").split("|")]
        assert len(cells) == len(REQUIRED_COLUMNS), f"unexpected index row shape: {row}"
        parsed.append(dict(zip(REQUIRED_COLUMNS, cells)))
    return parsed


def test_index_file_exists() -> None:
    assert INDEX.exists(), f"missing eval index: {INDEX}"


def test_index_header_has_required_columns() -> None:
    assert INDEX.exists(), f"missing eval index: {INDEX}"
    text = INDEX.read_text(encoding="utf-8")
    expected_header = "| " + " | ".join(REQUIRED_COLUMNS) + " |"
    assert expected_header in text


def test_index_covers_all_tracked_cases_once() -> None:
    indexed_paths = [row["Path"] for row in parse_index_rows()]
    assert indexed_paths == tracked_cases()


def test_index_uses_known_status_values() -> None:
    for row in parse_index_rows():
        assert row["Status"] in ALLOWED_STATUSES, f"unknown status in {row['Path']}: {row['Status']}"
        assert row["Current rule status"] in ALLOWED_RULE_STATUSES, (
            f"unknown current rule status in {row['Path']}: {row['Current rule status']}"
        )


def test_index_rows_are_complete_enough_for_coverage_scans() -> None:
    for row in parse_index_rows():
        path = row["Path"]
        for column in [
            "Primary route",
            "Failure family",
            "Primary discipline",
            "Status",
            "Intervention target",
            "Current rule status",
            "Notes",
        ]:
            assert row[column] and row[column] != "-", f"{path} missing {column}"


def test_eval_readme_links_index_and_status_policy() -> None:
    text = README.read_text(encoding="utf-8")
    assert "`evals/INDEX.md`" in text
    for phrase in [
        "active",
        "candidate",
        "needs-review",
        "stale",
        "superseded",
    ]:
        assert phrase in text, f"README should document {phrase} index status"


def test_agentic_rag_compounded_case_related_issues() -> None:
    """P1: The agentic-rag compounded eval MUST reference #268-#272.

    Contract: the Related issue / PR column value for the
    agentic-rag-technical-deep-dive-compounded-case row MUST contain
    references to all 5 issues whose rules this eval tests:
      - #268 (terminology boundary)
      - #269 (control-plane add-on)
      - #270 (benchmark comparability)
      - #271 (route-aware audit wrapper)
      - #272 (source type mapping)
    """
    rows = parse_index_rows()
    target = None
    for row in rows:
        if "agentic-rag-technical-deep-dive-compounded-case" in row["Path"]:
            target = row
            break

    assert target is not None, (
        "Row for agentic-rag-technical-deep-dive-compounded-case not found in INDEX.md"
    )

    related = target["Related issue / PR"]
    assert related and related != "-", (
        f"Related issue / PR column is empty for agentic-rag compounded case: {related!r}"
    )

    # Split on comma/semicolon to avoid substring false positives (e.g. #268 matching #2680)
    tokens = [t.strip() for t in related.replace(";", ",").split(",")]
    found_issues = {t for t in tokens if t.startswith("#")}

    expected_issues = {"#268", "#269", "#270", "#271", "#272"}
    missing = expected_issues - found_issues
    assert not missing, (
        f"Missing {missing} in related issues column: '{related}' — "
        f"found issues: {found_issues}"
    )


def main() -> int:
    tests = [
        test_index_file_exists,
        test_index_header_has_required_columns,
        test_index_covers_all_tracked_cases_once,
        test_index_uses_known_status_values,
        test_index_rows_are_complete_enough_for_coverage_scans,
        test_eval_readme_links_index_and_status_policy,
        test_agentic_rag_compounded_case_related_issues,
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
