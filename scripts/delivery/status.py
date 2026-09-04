"""Explicit, conservative delivery-status writeback for Research Packs."""

from __future__ import annotations

import re
from pathlib import Path

from .models import DeliveryResult


STATUS_HEADING = "## Delivery status"
H2_RE = re.compile(r"^##\s+(.+?)\s*$")
FENCE_RE = re.compile(r"^[ ]{0,3}(`{3,}|~{3,})")


def _section_bounds(lines: list[str]) -> tuple[int, int] | None:
    """Find the real Delivery status section, ignoring fenced examples."""

    in_fence = False
    fence_char = ""
    fence_length = 0
    start: int | None = None
    for index, line in enumerate(lines):
        match = FENCE_RE.match(line)
        if match and not in_fence:
            in_fence = True
            fence_char = match.group(1)[0]
            fence_length = len(match.group(1))
            continue
        if in_fence:
            if re.match(rf"^[ ]{{0,3}}{re.escape(fence_char)}{{{fence_length},}}\s*$", line):
                in_fence = False
            continue
        if line.strip() == STATUS_HEADING:
            start = index
            break
    if start is None:
        return None

    end = len(lines)
    in_fence = False
    for index in range(start + 1, len(lines)):
        match = FENCE_RE.match(lines[index])
        if match and not in_fence:
            in_fence = True
            fence_char = match.group(1)[0]
            fence_length = len(match.group(1))
            continue
        if in_fence:
            if re.match(rf"^[ ]{{0,3}}{re.escape(fence_char)}{{{fence_length},}}\s*$", lines[index]):
                in_fence = False
            continue
        heading = H2_RE.match(lines[index])
        if heading:
            end = index
            break
    return start, end


def _status_lines(result: DeliveryResult) -> list[str]:
    lines = [STATUS_HEADING, "", result.delivery_status.value]
    lines.extend([
        "",
        f"- markdown_status: {result.markdown_status.value}",
    ])
    if result.pdf_path:
        lines.append(f"- pdf_path: {result.pdf_path}")
    if result.errors:
        lines.append(f"- error: {result.errors[0]}")
    return lines


def write_delivery_status(path: Path, result: DeliveryResult) -> Path:
    """Update exactly one status section, adding it before Required audits.

    This function is only called through an explicit CLI option. The normal
    pipeline never mutates the input Markdown or Research Pack implicitly.
    """

    path = Path(path)
    lines = path.read_text(encoding="utf-8").splitlines()
    replacement = _status_lines(result)
    bounds = _section_bounds(lines)
    if bounds:
        start, end = bounds
        lines[start:end] = replacement
    else:
        insert_at = len(lines)
        for index, line in enumerate(lines):
            if line.strip() == "## Required audits":
                insert_at = index
                break
        prefix = [] if insert_at == 0 or not lines[insert_at - 1].strip() else [""]
        lines[insert_at:insert_at] = prefix + replacement + [""]
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return path
