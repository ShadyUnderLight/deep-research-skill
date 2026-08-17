"""Repair common LLM-produced Markdown table failures before parsing."""

from __future__ import annotations

import re


def repair_markdown_tables(md_text: str) -> str:
    def normalize_table_candidate(line: str) -> str:
        line = line.strip().replace("｜", "|")
        return re.sub(r"^[-*+]\s+(?=\|)", "", line)

    def parse_cells(row: str) -> list[str]:
        return [cell.strip() for cell in row.strip("|").split("|")]

    def is_separator_row(row: str) -> bool:
        cells = parse_cells(row)
        return bool(cells) and all(
            not cell or re.fullmatch(r":?-+:?", re.sub(r"\s+", "", cell))
            for cell in cells
        )

    def is_bullet_placeholder(value: str) -> bool:
        return value.strip().lower() in {"", "-", "*", "+", "•", "●", "▪", "◦"}

    lines = md_text.split("\n")
    repaired: list[str] = []
    index = 0
    while index < len(lines):
        stripped = normalize_table_candidate(lines[index])
        if "|" not in stripped or stripped.count("|") < 2:
            repaired.append(lines[index])
            index += 1
            continue

        group = [stripped]
        end = index + 1
        while end < len(lines):
            candidate = normalize_table_candidate(lines[end])
            if candidate and "|" in candidate and candidate.count("|") >= 2:
                group.append(candidate)
                end += 1
                continue
            break

        if len(group) < 2:
            repaired.append(lines[index])
            index += 1
            continue

        parsed_rows = [parse_cells(row) for row in group]
        if len(parsed_rows[0]) >= 2 and is_bullet_placeholder(parsed_rows[0][0]):
            first_col_values = [row[0] if row else "" for row in parsed_rows[2:]]
            second_header = parsed_rows[0][1].strip().lower()
            if (
                first_col_values
                and all(is_bullet_placeholder(value) for value in first_col_values)
            ) or second_header in {"#", "no", "no.", "序号", "编号"}:
                parsed_rows = [row[1:] if len(row) > 1 else [""] for row in parsed_rows]

        first_cells = parsed_rows[0]
        if not is_separator_row(group[1]):
            parsed_rows.insert(1, ["---"] * len(first_cells))
        else:
            parsed_rows[1] = ["---"] * len(first_cells)

        normalized_group: list[str] = []
        for cells in parsed_rows:
            cells = cells[: len(first_cells)] + [""] * max(0, len(first_cells) - len(cells))
            normalized_group.append("| " + " | ".join(cells) + " |")

        if repaired and repaired[-1] != "":
            repaired.append("")
        repaired.extend(normalized_group)
        repaired.append("")
        index = end

    return "\n".join(repaired)
