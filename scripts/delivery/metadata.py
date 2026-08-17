"""Frontmatter-like metadata extraction for delivery cover pages."""

from __future__ import annotations


def extract_cover_meta(md_text: str) -> tuple[str, str, list[str], str]:
    """Return cover title, subtitle, metadata lines, and cleaned body."""

    lines = md_text.split("\n")
    title = ""
    subtitle = ""
    meta_lines: list[str] = []

    for line in lines[:15]:
        lower = line.lower()
        if line.startswith("title:") or line.startswith("# title:"):
            title = line.split(":", 1)[1].strip().strip("\"'")
        elif "subtitle:" in lower or line.startswith("## subtitle:"):
            subtitle = line.split(":", 1)[1].strip().strip("\"'")
        elif line.startswith("date:") or lower.startswith("research date:"):
            meta_lines.append(f"研究日期：{line.split(':', 1)[1].strip()}")
        elif line.startswith("type:") or lower.startswith("research type:"):
            meta_lines.append(f"研究类型：{line.split(':', 1)[1].strip()}")

    body_lines = lines
    if lines and lines[0].strip() == "---":
        end = next(
            (index for index in range(1, min(20, len(lines))) if lines[index].strip() == "---"),
            None,
        )
        if end is not None:
            body_lines = lines[end + 1 :]
    return title, subtitle, meta_lines, "\n".join(body_lines)
