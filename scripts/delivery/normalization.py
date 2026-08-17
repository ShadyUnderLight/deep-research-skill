"""Markdown normalization kept independent from HTML and PDF rendering."""

from __future__ import annotations

import re
import unicodedata


def normalize_text_for_pdf(text: str) -> str:
    """Clean common Markdown artifacts without crossing block boundaries."""

    if not text:
        return text

    text = unicodedata.normalize("NFC", text)
    text = "".join(ch for ch in text if ch in ("\n", "\r", "\t") or ord(ch) >= 32)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
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

    lines: list[str] = []
    in_table = False
    pending_blank = False

    def flush_blank() -> None:
        nonlocal pending_blank
        if pending_blank and (not lines or lines[-1] != ""):
            lines.append("")
        pending_blank = False

    for raw in text.split("\n"):
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

        if "|" in stripped and stripped.count("|") >= 2:
            cells = [cell.strip() for cell in stripped.strip("|").split("|")]
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
    return re.sub(r"\n{3,}", "\n\n", "\n".join(lines))
