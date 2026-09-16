"""Issue #433 A4: report-table / pack-table evidence must be a real,
continuous Markdown table.

Before the fix ``_validate_artifact_table`` accepted any section containing
one line with ``|`` and one line with ``---``, so prose such as
``This is prose | with a pipe`` followed by ``--- | ---`` counted as a
verified table.  The parser now requires an adjacent header/delimiter pair,
canonical delimiter cells, and consistent column counts.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from audit_evidence import _validate_artifact_table  # noqa: E402


def _check(text: str, locator: str = "T", kind: str = "report_table"):
    return _validate_artifact_table(kind, locator, text, "report")


FAKE_TABLE = (
    "## T\n\n"
    "This is prose | with a pipe\n\n"
    "--- | ---\n"
)

VALID_TABLE = (
    "## T\n\n"
    "| Metric | Value |\n"
    "|--------|-------|\n"
    "| Cost | 100 |\n"
    "| Speed | 200 |\n"
)

VALID_TABLE_NO_OUTER_PIPES = (
    "## T\n\n"
    "Metric | Value\n"
    "-------|------\n"
    "Cost | 100\n"
)

VALID_TABLE_ALIGNMENT = (
    "## T\n\n"
    "| Metric | Value |\n"
    "|:-------|------:|\n"
    "| Cost | 100 |\n"
)

VALID_TABLE_NO_BLANK_LINE = (
    "## T\n"
    "| A | B |\n"
    "| --- | --- |\n"
    "| 1 | 2 |\n"
)


def test_prose_pipe_plus_dashed_line_is_not_a_table() -> None:
    result = _check(FAKE_TABLE)
    assert result.errors, result


def test_prose_pipe_without_delimiter_is_not_a_table() -> None:
    result = _check("## T\n\nThis is prose | with a pipe\n")
    assert result.errors, result


def test_single_pipe_line_is_not_a_table() -> None:
    result = _check("## T\n\n| only |\n")
    assert result.errors, result


def test_header_delimiter_must_be_adjacent() -> None:
    text = "## T\n\n| A | B |\n\n| --- | --- |\n| 1 | 2 |\n"
    result = _check(text)
    assert result.errors, result


def test_column_count_mismatch_fails() -> None:
    text = "## T\n\n| A | B |\n| --- | --- |\n| 1 | 2 | 3 |\n"
    result = _check(text)
    assert result.errors, result


def test_valid_table_passes() -> None:
    result = _check(VALID_TABLE)
    assert not result.errors, result


def test_valid_table_without_outer_pipes_passes() -> None:
    result = _check(VALID_TABLE_NO_OUTER_PIPES)
    assert not result.errors, result


def test_valid_table_with_alignment_passes() -> None:
    result = _check(VALID_TABLE_ALIGNMENT)
    assert not result.errors, result


def test_valid_table_directly_after_heading_passes() -> None:
    result = _check(VALID_TABLE_NO_BLANK_LINE)
    assert not result.errors, result


def test_single_column_table_is_rejected() -> None:
    """Documented fail-closed rule: a table needs at least two columns, so a
    single pipe-delimited line cannot satisfy report-table evidence."""
    result = _check("## T\n\n| Metric |\n| --- |\n| 1 |\n")
    assert result.errors, result


def test_pack_table_uses_same_parser() -> None:
    fake = _validate_artifact_table("pack_table", "T", FAKE_TABLE, "pack")
    assert fake.errors, fake
    valid = _validate_artifact_table("pack_table", "T", VALID_TABLE, "pack")
    assert not valid.errors, valid


def test_missing_heading_still_fails() -> None:
    result = _check("## Other\n\n| A | B |\n| --- | --- |\n| 1 | 2 |\n")
    assert result.errors, result


def test_duplicate_heading_still_fails() -> None:
    text = (
        "## T\n\n| A | B |\n| --- | --- |\n| 1 | 2 |\n\n"
        "## T\n\n| C | D |\n| --- | --- |\n| 3 | 4 |\n"
    )
    result = _check(text)
    assert result.errors, result
