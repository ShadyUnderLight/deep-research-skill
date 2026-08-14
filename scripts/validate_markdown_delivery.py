#!/usr/bin/env python3
"""Validate the reader-facing shape of a Markdown research report.

This is intentionally narrower than ``validate_report_quality.py``. The
existing validator checks evidence, route/audit status, and source
traceability; this validator checks Markdown reading order and density:

* one H1 and a continuous heading hierarchy;
* a judgment/summary opening before detailed analysis;
* stable Route and audit status / Source Register headings;
* obvious placeholder residue;
* overly wide body tables.

Warnings are advisory by default. ``--strict`` promotes warnings to a failing
exit status for delivery gates.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path


FENCE_RE = re.compile(r"^[ ]{0,3}(`{3,}|~{3,})")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
EXECUTIVE_RE = re.compile(r"(?:执行\s*摘要|executive\s+summary)", re.IGNORECASE)
THESIS_RE = re.compile(
    r"(?:\*\*)?(?:核心判断|核心结论|一句话判断|bottom[- ]line|core\s+thesis|"
    r"recommendation|judgment|结论)(?:\*\*)?\s*[:：]",
    re.IGNORECASE,
)
AUDIT_RE = re.compile(
    r"(?:route\s+and\s+audit\s+status|路由与审计状态)", re.IGNORECASE
)
SOURCE_RE = re.compile(r"(?:source\s+register|来源登记)", re.IGNORECASE)
PLACEHOLDER_RE = re.compile(
    r"(?:\[\s*(?:TODO|TBD|XXX|SOURCE|CITATION\s+NEEDED|待填写|待补充)\s*\]"
    r"|\{\{[^\n{}]+\}\})",
    re.IGNORECASE,
)
TABLE_SEPARATOR_RE = re.compile(
    r"^\s*\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)+\|?\s*$"
)


@dataclass
class ValidationResult:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def _without_frontmatter(lines: list[str]) -> list[str]:
    if not lines or lines[0].strip() != "---":
        return lines
    for index in range(1, min(len(lines), 80)):
        if lines[index].strip() == "---":
            return lines[index + 1 :]
    return lines


def _visible_lines(lines: list[str]) -> list[tuple[int, str]]:
    """Return (line number, line) pairs outside fenced code blocks and
    HTML comments (rendered content only, issue #378)."""
    visible: list[tuple[int, str]] = []
    in_fence = False
    in_comment = False
    fence_char = ""
    fence_length = 0
    for number, line in enumerate(lines, start=1):
        stripped = line.rstrip()
        if in_comment:
            if "-->" in stripped:
                in_comment = False
            continue
        if "<!--" in stripped:
            in_comment = True
            head = stripped.split("<!--", 1)[0]
            if head.strip():
                visible.append((number, head))
            if "-->" in stripped.split("<!--", 1)[1]:
                in_comment = False
            continue
        match = FENCE_RE.match(line)
        if not in_fence and match:
            in_fence = True
            fence_char = match.group(1)[0]
            fence_length = len(match.group(1))
            continue
        if in_fence:
            if re.match(
                rf"^[ ]{{0,3}}{re.escape(fence_char)}{{{fence_length},}}\s*$",
                stripped,
            ):
                in_fence = False
            continue
        visible.append((number, line))
    return visible


def _heading_context(visible: list[tuple[int, str]], line_number: int) -> str:
    context = ""
    for number, line in visible:
        if number > line_number:
            break
        match = HEADING_RE.match(line.rstrip())
        if match:
            context = match.group(2)
    return context


def _table_widths(visible: list[tuple[int, str]]) -> list[tuple[int, int, str]]:
    tables: list[tuple[int, int, str]] = []
    index = 0
    while index < len(visible) - 1:
        line_number, line = visible[index]
        _, next_line = visible[index + 1]
        if "|" not in line or not TABLE_SEPARATOR_RE.match(next_line):
            index += 1
            continue
        width = len(line.strip().strip("|").split("|"))
        tables.append((line_number, width, _heading_context(visible, line_number)))
        index += 2
        while index < len(visible):
            candidate = visible[index][1]
            if "|" not in candidate or not candidate.strip():
                break
            index += 1
    return tables


def validate_markdown_delivery(text: str) -> ValidationResult:
    result = ValidationResult()
    # Shared rendered-content sanitizer: fenced code, HTML comments and
    # raw HTML blocks (div/pre/script/...) are not rendered Markdown, so
    # headings hidden inside them must not count as document structure
    # (issue #378).
    from validate_contract import sanitize_visible_markdown
    text = sanitize_visible_markdown(text)
    raw_lines = text.splitlines()
    lines = _without_frontmatter(raw_lines)
    visible = _visible_lines(lines)

    headings: list[tuple[int, int, str]] = []
    for number, line in visible:
        match = HEADING_RE.match(line.rstrip())
        if match:
            headings.append((number, len(match.group(1)), match.group(2).strip()))

    h1s = [item for item in headings if item[1] == 1]
    if len(h1s) != 1:
        result.errors.append(f"expected exactly one H1, found {len(h1s)}")
    if headings and headings[0][1] != 1:
        result.errors.append("the first heading must be H1")
    for previous, current in zip(headings, headings[1:]):
        if current[1] > previous[1] + 1:
            result.errors.append(
                f"heading level skips from H{previous[1]} to H{current[1]} "
                f"near line {current[0]}"
            )

    opening = "\n".join(line for _, line in visible[:45])
    if not THESIS_RE.search(opening):
        result.errors.append(
            "the opening 45 lines must contain a judgment/thesis marker"
        )
    if not any(EXECUTIVE_RE.search(title) for _, _, title in headings):
        result.errors.append("missing Executive summary / 执行摘要 heading")

    audit_heading = next(
        ((number, title) for number, _, title in headings if AUDIT_RE.search(title)),
        None,
    )
    source_heading = next(
        ((number, title) for number, _, title in headings if SOURCE_RE.search(title)),
        None,
    )
    if audit_heading is None:
        result.errors.append("missing Route and audit status / 路由与审计状态 heading")
    if source_heading is None:
        result.errors.append("missing Source Register / 来源登记 heading")
    if audit_heading and source_heading and source_heading[0] < audit_heading[0]:
        result.errors.append("Source Register must appear after Route and audit status")

    body = "\n".join(line for _, line in visible)
    for match in PLACEHOLDER_RE.finditer(body):
        result.errors.append(f"placeholder residue: {match.group(0)!r}")

    for line_number, width, context in _table_widths(visible):
        source_like = bool(SOURCE_RE.search(context))
        limit = 7 if source_like else 6
        if width > limit:
            result.warnings.append(
                f"table near line {line_number} has {width} columns; "
                f"reader-facing body tables should stay at {limit} or fewer"
            )

    # A summary heading without any top-level bullets is usually a prose wall.
    executive_index = next(
        (
            index
            for index, (_, _, title) in enumerate(headings)
            if EXECUTIVE_RE.search(title)
        ),
        None,
    )
    if executive_index is not None:
        start_line = headings[executive_index][0]
        end_line = (
            headings[executive_index + 1][0]
            if executive_index + 1 < len(headings)
            else len(lines) + 1
        )
        bullet_count = sum(
            1
            for number, line in visible
            if start_line < number < end_line and re.match(r"^\s*[-*+]\s+", line)
        )
        if bullet_count == 0:
            result.warnings.append(
                "Executive summary has no bullet list; use bullets unless the task is genuinely small"
            )
        elif bullet_count > 10:
            result.warnings.append(
                f"Executive summary has {bullet_count} bullets; compress to roughly four to eight"
            )

    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate reader-facing Markdown delivery shape"
    )
    parser.add_argument("input", type=Path, help="Markdown report to validate")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="treat advisory readability warnings as failures",
    )
    args = parser.parse_args(argv)

    if not args.input.exists():
        print(f"error: file not found: {args.input}", file=sys.stderr)
        return 2
    result = validate_markdown_delivery(args.input.read_text(encoding="utf-8"))
    for message in result.errors:
        print(f"ERROR: {message}")
    for message in result.warnings:
        print(f"WARNING: {message}")

    if result.errors:
        print(f"Markdown delivery failed: {len(result.errors)} error(s)")
        return 2
    if args.strict and result.warnings:
        print(
            f"Markdown delivery failed in strict mode: {len(result.warnings)} warning(s)"
        )
        return 2
    print("Markdown delivery shape: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
