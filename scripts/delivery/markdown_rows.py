"""Shared Markdown table-row tokenizer for delivery transforms.

Normalization and table repair both need to know which ``|`` characters are
structural separators.  Escaped pipes (``\\|``) and pipes inside inline code
spans are cell content, not separators, and splitting them naively corrupts
valid Markdown before the renderer ever sees it (issue #435 review rounds
4-6).

The state machine follows CommonMark code-span rules: backslash escapes do
not apply inside a code span, a backtick run only opens a code span when a
matching same-length run exists later, and an unmatched backtick is literal
text (so the pipes after it stay structural).
"""

from __future__ import annotations

import re


def _backtick_run_length(row: str, start: int) -> int:
    run = 0
    while start + run < len(row) and row[start + run] == "`":
        run += 1
    return run


def _has_closing_backtick_run(row: str, start: int, run_length: int) -> bool:
    """True when a run of exactly *run_length* backticks follows *start*."""

    index = start
    length = len(row)
    while index < length:
        if row[index] == "`":
            run = _backtick_run_length(row, index)
            if run == run_length:
                return True
            index += run
            continue
        index += 1
    return False


def _delimiter_positions(row: str) -> tuple[list[int], list[int]]:
    """Return structural ``(ascii_pipe, fullwidth_pipe)`` character indices.

    Escaped pipes and pipes inside code spans are excluded; an unmatched
    backtick is literal, so the pipes after it stay structural.
    """

    ascii_positions: list[int] = []
    fullwidth_positions: list[int] = []
    code_fence = 0
    index = 0
    length = len(row)
    while index < length:
        char = row[index]
        if code_fence == 0:
            if char == "\\" and index + 1 < length:
                index += 2
                continue
            if char == "`":
                run = _backtick_run_length(row, index)
                if _has_closing_backtick_run(row, index + run, run):
                    code_fence = run
                index += run
                continue
            if char == "|":
                ascii_positions.append(index)
                index += 1
                continue
            if char == "｜":
                fullwidth_positions.append(index)
                index += 1
                continue
            index += 1
            continue
        if char == "`":
            run = _backtick_run_length(row, index)
            index += run
            if run == code_fence:
                code_fence = 0
            continue
        index += 1
    return ascii_positions, fullwidth_positions


def _scan_row(row: str) -> tuple[list[str], int]:
    """Return ``(cells, structural_pipe_count)`` for one table row."""

    ascii_positions, _ = _delimiter_positions(row)
    cells: list[str] = []
    start = 0
    for position in ascii_positions:
        cells.append(row[start:position])
        start = position + 1
    cells.append(row[start:])

    if cells and cells[0].strip() == "":
        cells = cells[1:]
    if cells and cells[-1].strip() == "":
        cells = cells[:-1]
    return [cell.strip() for cell in cells], len(ascii_positions)


def split_markdown_row(row: str) -> list[str]:
    """Split a Markdown table row on structural pipes only.

    Leading/trailing structural pipes are removed and every cell is
    stripped.  Escaped pipes and pipes inside backtick code spans stay in
    the cell text so the downstream Markdown parser can render them
    correctly.
    """

    cells, _ = _scan_row(row)
    return cells


def count_structural_pipes(row: str) -> int:
    """Number of structural ``|`` separators (escapes and code spans excluded).

    Candidate detection uses this instead of the raw pipe count. The
    group-level table gate decides whether a one-pipe row belongs to a
    separator-backed two-column table; escaped pipes and code-span pipes
    never contribute (issue #435 review round 9).
    """

    _, structural_pipes = _scan_row(row)
    return structural_pipes


def is_separator_row(row: str) -> bool:
    """Return True when every cell is a Markdown table separator cell."""

    cells = split_markdown_row(row)
    return bool(cells) and all(
        not cell or re.fullmatch(r":?-+:?", re.sub(r"\s+", "", cell))
        for cell in cells
    )


def has_outer_structural_pipe(row: str) -> bool:
    """Return True when a row has a leading or trailing structural pipe."""

    ascii_positions, _ = _delimiter_positions(row)
    if not ascii_positions:
        return False
    return (
        not row[: ascii_positions[0]].strip()
        or not row[ascii_positions[-1] + 1 :].strip()
    )


def is_repairable_table_group(rows: list[str]) -> bool:
    """Gate repair to a separator-backed or explicitly delimited table block.

    A standard unbordered table may omit outer pipes but must have a separator
    row and at least one data row. Missing-separator repair remains available
    for explicitly pipe-delimited rows, while ordinary multi-pipe prose stays
    prose (issue #435 C2).
    """

    if len(rows) >= 3 and is_separator_row(rows[1]):
        return True
    return len(rows) >= 2 and all(has_outer_structural_pipe(row) for row in rows)


def normalize_fullwidth_table_delimiters(row: str) -> str:
    """Convert fullwidth ``｜`` separators only for legacy delimiter rows.

    A row that already has ASCII structural pipes keeps every ``｜`` as
    data, and code-span ``｜`` is never touched.  Only a row with no ASCII
    structural pipes and at least two structural ``｜`` candidates is
    treated as a legacy fullwidth-delimited table row (issue #435 review
    round 8).
    """

    ascii_positions, fullwidth_positions = _delimiter_positions(row)
    if ascii_positions or len(fullwidth_positions) < 2:
        return row
    characters = list(row)
    for position in fullwidth_positions:
        characters[position] = "|"
    return "".join(characters)
