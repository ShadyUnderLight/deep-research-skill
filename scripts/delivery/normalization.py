"""Markdown normalization kept independent from HTML and PDF rendering."""

from __future__ import annotations

import re
import unicodedata

from .fences import fence_aware_runs, iter_fence_aware_lines
from .markdown_rows import (
    can_bridge_short_data_row,
    count_structural_pipes,
    is_repairable_table_group,
    is_simple_short_data_row,
    is_separator_row,
    is_ambiguous_unbordered_wide_row,
    is_short_table_data_row,
    split_markdown_row,
)


def _format_plain_markdown(text: str) -> str:
    """Apply the non-structural formatting passes to fence-free text."""

    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    cjk = r"\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff"
    text = re.sub(rf"([{cjk}])[ \t]+([{cjk}])", r"\1\2", text)
    text = re.sub(rf"([{cjk}])[ \t]+([，。！？；：、）】》％%])", r"\1\2", text)
    text = re.sub(rf"([（【《])[ \t]+([{cjk}])", r"\1\2", text)
    text = re.sub(rf"([{cjk}])[ \t]+([·—…])[ \t]*([{cjk}])", r"\1\2\3", text)
    text = re.sub(rf"([{cjk}])[ \t]+([A-Za-z0-9])", r"\1 \2", text)
    text = re.sub(rf"([A-Za-z0-9])[ \t]+([{cjk}])", r"\1 \2", text)
    text = re.sub(
        r"(?m)^((?:[A-Z][A-Za-z\-]+\s*[:：]\s*)+)(.+)$",
        lambda match: re.sub(r"\s{2,}", " ", match.group(1)).strip()
        + " "
        + match.group(2).strip(),
        text,
    )
    text = re.sub(r"(?m)^[\x00-\x08\x0b\x0c\x0e-\x1f\u2022\u25aa\u25cf\uf0b7]\s*", "- ", text)
    text = re.sub(r"(?m)^[•●▪◦]\s*", "- ", text)
    text = re.sub(r"(?m)(?<=\S)[ \t]{2,}(?=\S)", " ", text)
    return text


def normalize_text_for_pdf(text: str) -> str:
    """Clean common Markdown artifacts without crossing block boundaries.

    Fenced code (backtick or tilde, closed or not) is copied byte-for-byte,
    including its Unicode normalization form, control characters, and line
    endings.  NFC/control-character cleanup and the Markdown/CJK formatting
    passes only ever run on fence-free runs (issue #435).
    """

    if not text:
        return text

    processed: list[str] = []
    for run_lines, in_fence in fence_aware_runs(text):
        if in_fence:
            processed.extend(run_lines)
            continue
        joined = "\n".join(run_lines)
        joined = unicodedata.normalize("NFC", joined)
        joined = "".join(ch for ch in joined if ch in ("\n", "\r", "\t") or ord(ch) >= 32)
        joined = joined.replace("\r\n", "\n").replace("\r", "\n")
        processed.extend(_format_plain_markdown(joined).split("\n"))
    text = "\n".join(processed)

    source_lines = text.split("\n")
    fence_flags = [in_fence for _, in_fence in iter_fence_aware_lines(text)]
    table_lines: set[int] = set()

    def table_candidate(line: str) -> str | None:
        candidate = line.strip()
        candidate = re.sub(r"^[-*+]\s+(?=\|)", "", candidate)
        return candidate if count_structural_pipes(candidate) >= 1 else None

    index = 0
    while index < len(source_lines):
        if fence_flags[index]:
            index += 1
            continue
        candidate = table_candidate(source_lines[index])
        if candidate is None:
            index += 1
            continue
        group = [candidate]
        end = index + 1
        separator_backed = False
        expected_width = 0
        short_row_bridged = False
        if end < len(source_lines) and not fence_flags[end]:
            second = table_candidate(source_lines[end])
            if second is not None:
                group.append(second)
                end += 1
                separator_backed = is_separator_row(second)
                if separator_backed:
                    expected_width = len(split_markdown_row(second))
        while end < len(source_lines) and not fence_flags[end]:
            next_candidate = table_candidate(source_lines[end])
            if next_candidate is not None:
                if (
                    separator_backed
                    and group
                    and is_simple_short_data_row(group[-1])
                    and is_ambiguous_unbordered_wide_row(next_candidate, expected_width)
                ):
                    break
                group.append(next_candidate)
                end += 1
                if (
                    separator_backed
                    and not short_row_bridged
                    and is_short_table_data_row(next_candidate, expected_width)
                ):
                    short_row_bridged = True
                continue
            if (
                separator_backed
                and not short_row_bridged
                and is_simple_short_data_row(source_lines[end])
                and end == index + 2
            ):
                group.append(source_lines[end].strip())
                end += 1
                short_row_bridged = True
                continue
            if (
                separator_backed
                and not short_row_bridged
                and end + 1 < len(source_lines)
                and not fence_flags[end + 1]
                and can_bridge_short_data_row(
                    source_lines[end], source_lines[end + 1], expected_width
                )
            ):
                group.append(source_lines[end].strip())
                end += 1
                short_row_bridged = True
                continue
            break
        if is_repairable_table_group(group):
            table_lines.update(range(index, end))
        index = end

    lines: list[str] = []
    in_table = False
    pending_blank = False

    def flush_blank() -> None:
        nonlocal pending_blank
        if pending_blank and (not lines or lines[-1] != ""):
            lines.append("")
        pending_blank = False

    for line_index, raw in enumerate(source_lines):
        in_fence = fence_flags[line_index]
        if in_fence:
            if in_table and lines and lines[-1] != "":
                lines.append("")
            in_table = False
            flush_blank()
            lines.append(raw)
            continue

        line = raw.rstrip()
        stripped = line.strip()
        if not stripped:
            pending_blank = True
            in_table = False
            continue

        stripped = re.sub(r"^[-*+]\s+(?=(?:#{1,6}\s|\|))", "", stripped)
        heading_match = re.match(r"^(#{1,6})\s*(.+?)\s*$", stripped)
        if heading_match:
            if lines and lines[-1] != "":
                lines.append("")
            lines.append(f"{heading_match.group(1)} {heading_match.group(2)}")
            lines.append("")
            pending_blank = False
            in_table = False
            continue

        if re.fullmatch(r"[-*_]{3,}", stripped.replace(" ", "")):
            if lines and lines[-1] != "":
                lines.append("")
            lines.extend(["---", ""])
            pending_blank = False
            in_table = False
            continue

        if stripped.startswith(">"):
            flush_blank()
            lines.append("> " + stripped.lstrip("> ").strip())
            in_table = False
            continue

        if line_index in table_lines:
            cells = split_markdown_row(stripped)
            if not in_table and lines and lines[-1] != "":
                lines.append("")
            lines.append("| " + " | ".join(cells) + " |")
            in_table = True
            pending_blank = False
            continue
        if in_table:
            lines.append("")
            in_table = False

        if re.match(r"^[-*+]\s+.+$", stripped) or re.match(r"^\d+\.\s+.+$", stripped):
            flush_blank()
            lines.append(stripped)
            continue

        flush_blank()
        lines.append(stripped)

    if in_table and lines and lines[-1] != "":
        lines.append("")

    return "\n".join(
        "\n".join(run_lines)
        if in_fence
        else re.sub(r"\n{3,}", "\n\n", "\n".join(run_lines))
        for run_lines, in_fence in fence_aware_runs("\n".join(lines))
    )
