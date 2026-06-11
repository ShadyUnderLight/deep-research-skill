#!/usr/bin/env python3
"""Detect Markdown tables missing numeric role labels.

A "comparison/scoring/estimation" table with 3+ data rows should contain
numeric role labels (e.g., a 数字角色 column, or role keywords in data cells).
Simple key-value or metadata tables are exempt.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


# Role column header keywords — if a header cell contains any of these,
# the table is considered to have a role annotation column.
ROLE_HEADER_KEYWORDS = [
    "数字角色",
    "角色",
    "number role",
    "epistemic role",
    "role",
]

# Role value keywords — if a data cell contains any of these,
# the row is considered to have a role label.
ROLE_VALUE_KEYWORDS = [
    "观察值",
    "代理",
    "假设",
    "模型输出",
    "估算",
    "推断",
    "observed",
    "proxy",
    "assumption",
    "model-output",
    "model output",
    "estimate",
    "scenario",
    "inferred",
    "illustrative",
]

# Key-value table header patterns (first 2 cells, lowered + stripped).
_KEY_VALUE_PATTERNS: set[tuple[str, str]] = {
    ("key", "value"),
    ("属性", "值"),
    ("指标", "数值"),
    ("metric", "value"),
    ("参数", "值"),
    ("项目", "值"),
    ("attribute", "value"),
    ("item", "value"),
    ("属性", "数值"),
    ("指标", "值"),
    ("key", "description"),
    ("指标", "说明"),
    ("参数", "说明"),
    ("item", "description"),
}


def strip_fenced_code_blocks(text: str) -> str:
    """Remove content inside fenced code blocks (`` ``` `` and `` ~~~ ``)."""
    lines = text.splitlines()
    out: list[str] = []
    in_fence = False
    fence_char = ""
    fence_len = 0

    for line in lines:
        stripped = line.rstrip()
        if not in_fence:
            m = re.match(r"^[ ]{0,3}(`{3,}|~{3,})", stripped)
            if m:
                fence_char = m.group(1)[0]
                fence_len = len(m.group(1))
                in_fence = True
                continue
            out.append(line)
            continue

        closing = re.compile(
            r"^[ ]{0,3}" + re.escape(fence_char) + "{" + str(fence_len) + r",}\s*$"
        )
        if closing.match(stripped):
            in_fence = False

    return "\n".join(out)


def get_cells(line: str) -> list[str]:
    """Split a Markdown table row into stripped cell values.

    Handles leading/trailing pipes and trims whitespace per cell.
    """
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return [cell.strip() for cell in s.split("|")]


def is_delimiter_row(cells: list[str]) -> bool:
    """Return True if this row is a Markdown delimiter row (e.g. |---|---|)."""
    if not cells:
        return False
    # A delimiter row has cells that consist entirely of dashes, colons, and spaces.
    return all(re.fullmatch(r":?-{3,}:?\s*", cell) for cell in cells)


def is_key_value_table(header_cells: list[str]) -> bool:
    """Return True if the table has a simple key-value header (e.g. | Key | Value |)."""
    if len(header_cells) != 2:
        return False
    first = header_cells[0].lower().strip()
    second = header_cells[1].lower().strip()
    return (first, second) in _KEY_VALUE_PATTERNS


def has_role_keyword_in_cell(text: str) -> bool:
    """Return True if *text* contains any role keyword (header or value)."""
    lower = text.lower()
    for kw in ROLE_HEADER_KEYWORDS:
        if kw.lower() in lower:
            return True
    for kw in ROLE_VALUE_KEYWORDS:
        if kw.lower() in lower:
            return True
    return False


def find_tables(lines: list[str]) -> list[tuple[int, int]]:
    """Return (start, end) line index spans for each detected Markdown table."""
    tables: list[tuple[int, int]] = []
    in_table = False
    start = 0
    for i, line in enumerate(lines):
        if line.startswith("|"):
            if not in_table:
                in_table = True
                start = i
        else:
            if in_table and i - start >= 2:  # at least header + delimiter
                tables.append((start, i))
            in_table = False
    if in_table and len(lines) - start >= 2:
        tables.append((start, len(lines)))
    return tables


def validate_file(path: Path) -> list[str]:
    """Validate all tables in *path* for role labels. Returns error message list."""
    raw = path.read_text(encoding="utf-8", errors="replace")
    cleaned = strip_fenced_code_blocks(raw)
    lines = cleaned.splitlines()

    errors: list[str] = []

    for start, end in find_tables(lines):
        table_lines = lines[start:end]
        # Parse header (first non-delimiter row)
        header_cells: list[str] = []
        data_rows: list[list[str]] = []
        for line in table_lines:
            cells = get_cells(line)
            if is_delimiter_row(cells):
                continue
            if not header_cells:
                header_cells = cells
            else:
                data_rows.append(cells)

        # Skip tables with too few data rows
        if len(data_rows) < 3:
            continue

        # Skip key-value tables
        if is_key_value_table(header_cells):
            continue

        # Check if any row (header or data) contains role keywords
        role_found = False
        if has_role_keyword_in_cell(" ".join(header_cells)):
            role_found = True
        for row in data_rows:
            if has_role_keyword_in_cell(" ".join(row)):
                role_found = True
                break

        if not role_found:
            line_no = start + 1  # 1-indexed
            # Show header as context
            header_str = " | ".join(header_cells)
            errors.append(
                f"{path}:{line_no}: table with {len(data_rows)} data rows "
                f"lacks numeric role labels\n"
                f"    header: | {header_str} |"
            )

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Lint Markdown tables for missing numeric role labels."
    )
    parser.add_argument("paths", nargs="+", help="Markdown files to validate")
    args = parser.parse_args(argv)

    errors: list[str] = []
    for raw_path in args.paths:
        path = Path(raw_path)
        if not path.exists():
            errors.append(f"{path}: file not found")
            continue
        errors.extend(validate_file(path))

    if errors:
        print("Table role label lint failed:")
        for error in errors:
            print(f"- {error}")
        return 2

    print(f"Table role label lint passed for {len(args.paths)} file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
