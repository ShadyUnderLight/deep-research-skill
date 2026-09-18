"""Shared Markdown table-row tokenizer for delivery transforms.

Normalization and table repair both need to know which ``|`` characters are
structural separators.  Escaped pipes (``\\|``) and pipes inside inline code
spans are cell content, not separators, and splitting them naively corrupts
valid Markdown before the renderer ever sees it (issue #435 review round 4).
"""

from __future__ import annotations


def split_markdown_row(row: str) -> list[str]:
    """Split a Markdown table row on structural pipes only.

    Leading/trailing structural pipes are removed and every cell is
    stripped.  Escaped pipes and pipes inside backtick code spans stay in
    the cell text so the downstream Markdown parser can render them
    correctly.
    """

    cells: list[str] = []
    current: list[str] = []
    code_fence = 0
    index = 0
    length = len(row)
    while index < length:
        char = row[index]
        if char == "\\" and index + 1 < length:
            current.append(char)
            current.append(row[index + 1])
            index += 2
            continue
        if char == "`":
            run = 1
            while index + run < length and row[index + run] == "`":
                run += 1
            if code_fence == 0:
                code_fence = run
            elif code_fence == run:
                code_fence = 0
            current.append("`" * run)
            index += run
            continue
        if char == "|" and code_fence == 0:
            cells.append("".join(current))
            current = []
            index += 1
            continue
        current.append(char)
        index += 1
    cells.append("".join(current))

    if cells and cells[0].strip() == "":
        cells = cells[1:]
    if cells and cells[-1].strip() == "":
        cells = cells[:-1]
    return [cell.strip() for cell in cells]
