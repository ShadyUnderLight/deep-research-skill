#!/usr/bin/env python3
"""Detect Source Register label/source type mismatches in Markdown reports.

Two checks:
1. Secondary sources (SECONDARY_MEDIA, SECONDARY_ANALYST, etc.) should not
   be referenced with confirmed labels like [CONF], [确认事实].
2. Primary company sources (PRIMARY_COMPANY, PRIMARY_PARTNER) must include
   a self-reporting caveat (厂商自述) when referenced.

PRIMARY_FILING sources are exempt from both checks.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Confirmed label patterns — these should NOT be used with secondary sources.
CONFIRMED_LABEL_RE = re.compile(
    r"\[(?:确认事实|CONF|Confirmed|确认)\]", re.IGNORECASE
)

# Self-reporting caveat patterns required for primary company sources.
CAVEAT_RE = re.compile(r"(?:来源：厂商自述，非独立验证|厂商自述)")

# Heading patterns for Source Register section.
HEADING_RE = re.compile(
    r"^#{1,6}\s+.*(?:Source Register|来源注册表)", re.IGNORECASE
)

# Secondary source types (granular + simplified). These should NOT use
# confirmed labels.
_SECONDARY_TYPES: frozenset[str] = frozenset({
    "SECONDARY_MEDIA",
    "SECONDARY_ANALYST",
    "SECONDARY_FEED",
    "SECONDARY",
})

# Primary company source types that need a self-reporting caveat.
_PRIMARY_COMPANY_TYPES: frozenset[str] = frozenset({
    "PRIMARY_COMPANY",
    "PRIMARY_PARTNER",
})


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
            r"^[ ]{0,3}"
            + re.escape(fence_char)
            + "{"
            + str(fence_len)
            + r",}\s*$"
        )
        if closing.match(stripped):
            in_fence = False

    return "\n".join(out)


def get_cells(line: str) -> list[str]:
    """Split a Markdown table row into stripped cell values."""
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
    return all(re.fullmatch(r":?-{3,}:?\s*", cell) for cell in cells)


def find_source_register(
    lines: list[str],
) -> tuple[list[tuple[str, str]], int, int] | None:
    """Find the Source Register table.

    Returns (sources, heading_start, table_end_exclusive) where *table_end_exclusive*
    is the line index one past the last table line, or None if not found.
    *sources* may be empty if the register table has no parseable rows.
    """
    # Find heading
    heading_idx = -1
    for i, line in enumerate(lines):
        if HEADING_RE.match(line):
            heading_idx = i
            break

    if heading_idx == -1:
        return None

    # Find the first table line after the heading
    table_start = -1
    for i in range(heading_idx + 1, len(lines)):
        if lines[i].strip().startswith("|"):
            table_start = i
            break

    if table_start == -1:
        return None

    # Collect consecutive table lines
    table_lines: list[str] = []
    for i in range(table_start, len(lines)):
        if not lines[i].strip().startswith("|"):
            break
        table_lines.append(lines[i])

    if not table_lines:
        return None

    sources = _parse_register_table(table_lines)
    # table_end_exclusive is the last table line index + 1
    table_end = table_start + len(table_lines)
    return (sources, heading_idx, table_end)


def _parse_register_table(table_lines: list[str]) -> list[tuple[str, str]]:
    """Parse Source Register table rows into (source_id, source_type) tuples."""
    header_parsed = False
    sources: list[tuple[str, str]] = []

    for line in table_lines:
        cells = get_cells(line)
        if is_delimiter_row(cells):
            continue
        if not header_parsed:
            header_parsed = True
            continue

        if len(cells) < 3:
            continue

        source_id = cells[0].strip()
        source_type = cells[2].strip()

        if not source_id or not source_type:
            continue

        sources.append((source_id, source_type))

    return sources


def _is_secondary_type(source_type: str) -> bool:
    """Check if a source type is secondary (granular or simplified)."""
    upper = source_type.strip().upper()
    return upper in _SECONDARY_TYPES


def _is_primary_company_type(source_type: str) -> bool:
    """Check if a source type is a primary company (needs caveat)."""
    upper = source_type.strip().upper()
    return upper in _PRIMARY_COMPANY_TYPES


def _source_ref_re(source_id: str) -> re.Pattern:
    """Build a regex to find a source ID reference (word-boundary match)."""
    return re.compile(r"\b" + re.escape(source_id) + r"\b")


def _split_sentences(text: str) -> list[str]:
    """Split text into sentence-like chunks for scanning."""
    results: list[str] = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        chunks = re.split(r"(?<=[。！？!?；;])\s+", line)
        for chunk in chunks:
            chunk = chunk.strip()
            if chunk:
                results.append(chunk)
    return results


def check_source_consistency(text: str) -> list[str]:
    """Check label/source type consistency. Returns list of error messages.

    Two checks:
    1. Secondary sources must not be referenced with confirmed labels.
    2. Primary company sources must have a self-reporting caveat nearby.
    """
    cleaned = strip_fenced_code_blocks(text)
    lines = cleaned.splitlines()

    register_info = find_source_register(lines)
    if register_info is None:
        return []  # No Source Register → nothing to check

    sources, heading_start, table_end = register_info
    if not sources:
        return []

    # Build body text excluding the Source Register section itself,
    # so table rows don't trigger false positives.
    body_lines = lines[:heading_start] + lines[table_end:]
    body_text = "\n".join(body_lines)

    sentences = _split_sentences(body_text)
    errors: list[str] = []

    for source_id, source_type in sources:
        if not source_id:
            continue

        ref_re = _source_ref_re(source_id)

        if _is_secondary_type(source_type):
            # Check 1: Secondary source should not have confirmed label nearby.
            for sent in sentences:
                if not ref_re.search(sent):
                    continue
                if CONFIRMED_LABEL_RE.search(sent):
                    errors.append(
                        f"source {source_id} ({source_type}) is secondary "
                        f"but referenced with confirmed label: {sent[:100]}"
                    )

        elif _is_primary_company_type(source_type):
            # Check 2: Primary company source needs self-reporting caveat.
            for sent in sentences:
                if not ref_re.search(sent):
                    continue
                if not CAVEAT_RE.search(sent):
                    errors.append(
                        f"source {source_id} ({source_type}) is a primary "
                        f"company source but lacks self-reporting caveat: "
                        f"{sent[:100]}"
                    )

    return errors


def validate_file(path: Path) -> list[str]:
    """Validate all source label consistency rules in *path*."""
    raw = path.read_text(encoding="utf-8", errors="replace")
    return check_source_consistency(raw)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Lint Source Register label consistency in Markdown reports."
        )
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
        print("Source label consistency lint failed:")
        for error in errors:
            print(f"- {error}")
        return 2

    print(
        f"Source label consistency lint passed for {len(args.paths)} file(s)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
