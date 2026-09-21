"""Repair common LLM-produced Markdown table failures before parsing."""

from __future__ import annotations

import re

from .fences import iter_fence_aware_lines
from .markdown_rows import (
    can_bridge_short_data_row,
    count_structural_pipes,
    is_repairable_table_group,
    is_simple_short_data_row,
    is_separator_row,
    normalize_fullwidth_table_delimiters,
    is_textual_unbordered_wide_row,
    split_markdown_row,
)

# Values that carry no information in a leading layout column.  Status
# values such as ``N/A``/``TBD`` and numbering such as ``#1`` are data and
# must never justify dropping a column (issue #435 review round 4).
LAYOUT_ONLY_VALUES = frozenset(
    {"", "#", "-", "*", "+", "•", "●", "▪", "◦", "—", "–", "--", "——", "/"}
)


def repair_markdown_tables(md_text: str, *, warnings: list[str] | None = None) -> str:
    """Normalize table rows without ever truncating data columns.

    The repaired width is ``max(header width, widest data row)``; short rows
    and short headers are padded with empty cells.  A leading layout-only
    column is dropped only when the header and every data cell in that
    column are strictly layout values, and the drop is reported through
    ``warnings`` (issue #435 review round 4).
    """

    warning_sink = warnings if warnings is not None else []

    def normalize_table_candidate(line: str) -> str:
        line = normalize_fullwidth_table_delimiters(line.strip())
        return re.sub(r"^[-*+]\s+(?=\|)", "", line)

    def parse_cells(row: str) -> list[str]:
        return split_markdown_row(row)

    def is_layout_only(value: str) -> bool:
        return value.strip() in LAYOUT_ONLY_VALUES

    def table_candidate(line: str) -> str | None:
        """Return the normalized line when it has at least one structural pipe.

        The group-level gate below decides whether a one-pipe row belongs to
        a separator-backed two-column table; escaped pipes and code-span pipes
        remain excluded from this count (issue #435 review round 9).
        """

        candidate = normalize_table_candidate(line)
        if count_structural_pipes(candidate) < 1:
            return None
        return candidate

    lines = md_text.split("\n")
    fence_flags = [in_fence for _, in_fence in iter_fence_aware_lines(md_text)]
    repaired: list[str] = []
    index = 0
    while index < len(lines):
        if fence_flags[index]:
            repaired.append(lines[index])
            index += 1
            continue

        stripped = table_candidate(lines[index])
        if stripped is None:
            repaired.append(lines[index])
            index += 1
            continue

        group = [stripped]
        end = index + 1
        separator_backed = False
        expected_width = 0
        if end < len(lines) and not fence_flags[end]:
            second = table_candidate(lines[end])
            if second is not None:
                group.append(second)
                end += 1
                separator_backed = is_separator_row(second)
                if separator_backed:
                    expected_width = len(parse_cells(second))
        while end < len(lines) and not fence_flags[end]:
            candidate = table_candidate(lines[end])
            if candidate is not None:
                if (
                    separator_backed
                    and group
                    and is_simple_short_data_row(group[-1])
                    and is_textual_unbordered_wide_row(candidate, expected_width)
                ):
                    break
                group.append(candidate)
                end += 1
                continue
            if (
                separator_backed
                and is_simple_short_data_row(lines[end])
                and end == index + 2
            ):
                group.append(lines[end].strip())
                end += 1
                continue
            if (
                separator_backed
                and end + 1 < len(lines)
                and not fence_flags[end + 1]
                and can_bridge_short_data_row(lines[end], lines[end + 1], expected_width)
            ):
                group.append(lines[end].strip())
                end += 1
                continue
            break

        if not is_repairable_table_group(group):
            repaired.append(lines[index])
            index += 1
            continue

        parsed_rows = [parse_cells(row) for row in group]
        has_separator = is_separator_row(group[1])
        if len(parsed_rows[0]) >= 2 and is_layout_only(parsed_rows[0][0]):
            data_rows = parsed_rows[2:] if has_separator else parsed_rows[1:]
            first_col_values = [row[0] if row else "" for row in data_rows]
            if first_col_values and all(
                is_layout_only(value) for value in first_col_values
            ):
                warning_sink.append(
                    "table repair dropped a leading layout-only column (no data)"
                )
                parsed_rows = [
                    row[1:] if len(row) > 1 else [""] for row in parsed_rows
                ]

        if not has_separator:
            parsed_rows.insert(1, [])
        width = max((len(row) for row in parsed_rows), default=1)
        width = max(width, 1)
        parsed_rows = [row + [""] * (width - len(row)) for row in parsed_rows]
        separator: list[str] = []
        for cell in parsed_rows[1]:
            cleaned = cell.strip()
            separator.append(cleaned if re.fullmatch(r":?-+:?", cleaned) else "---")
        parsed_rows[1] = separator + ["---"] * (width - len(separator))

        normalized_group = [
            "| " + " | ".join(cells) + " |" for cells in parsed_rows
        ]

        if repaired and repaired[-1] != "":
            repaired.append("")
        repaired.extend(normalized_group)
        repaired.append("")
        index = end

    return "\n".join(repaired)
