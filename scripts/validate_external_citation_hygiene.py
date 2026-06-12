#!/usr/bin/env python3
"""Validate that a report contains no external deep-research internal citation artifacts.

Scans for three categories of import hygiene violations:

1. sandbox: paths — GPT sandbox file paths, unreachable outside session
2. turn\\d+ references — GPT session turn citations (turn42view0, turn12source1, etc.)
3. \\ue000cite placeholders — GPT-specific citation rendering artifacts
4. file-xxxxxxxxxxxx temp IDs — ephemeral session file identifiers

These patterns bypass the project's source traceability discipline because they
are not resolvable outside the originating session.

Usage:
    python validate_external_citation_hygiene.py report.md

Exit codes:
    0 — pass (no violations found, or only warnings produced)
    2 — structural error (cannot read file)

Output:
    Warnings are printed to stdout if violations are found.
    The script always exits 0 (warnings-only severity).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

EXIT_PASS = 0
EXIT_STRUCTURE = 2

# ── Regex patterns ─────────────────────────────────────────────────────────

# Pattern 1: sandbox: paths (GPT sandbox, unreachable after session ends)
EXTERNAL_CITE_SANDBOX_RE = re.compile(r"sandbox:")

# Pattern 2: turnNviewM / turnNsourceM / turnNsearchM (GPT session turn refs)
# Uses \bturn to avoid matching "return", "turnaround", "turning", etc.
# No trailing \b because the type suffix often has trailing digits (view0, source1).
# The (?:view|source|search) suffix requirement prevents matching legitimate uses
# of turn+N like "turn 12 degrees" or "turn 4 times".
EXTERNAL_CITE_TURN_RE = re.compile(r"\bturn\d+(?:view\d*|source\d*|search\d*)")

# Pattern 3: \ue000cite or \ue001cite (GPT cite rendering artifacts)
# \ue000 and \ue001 are Unicode Private Use Area characters used by GPT
EXTERNAL_CITE_UNICODE_RE = re.compile(r"[\ue000\ue001]cite")

# Pattern 4: file-xxxxxxxxxxxx (temporary file IDs from GPT/claude)
# Matches file- followed by alphanumeric ID of 10+ chars
EXTERNAL_CITE_FILE_ID_RE = re.compile(r"\bfile-[A-Za-z0-9]{10,}\b")

# ── Fence stripping (same pattern as validate_report_quality.py) ───────────

FENCE_RE = re.compile(r"^[ ]{0,3}(`{3,}|~{3,})")


def strip_fenced_code_blocks(text: str) -> str:
    """Remove fenced code blocks so patterns inside code are not scanned."""
    lines = text.splitlines()
    out: list[str] = []
    in_fence = False
    fence_char = ""
    fence_len = 0

    for line in lines:
        stripped = line.rstrip()
        if not in_fence:
            m = FENCE_RE.match(stripped)
            if m:
                fence_char = m.group(1)[0]
                fence_len = len(m.group(1))
                in_fence = True
                continue
            out.append(line)
            continue
        closing_re = re.compile(
            r"^[ ]{0,3}"
            + re.escape(fence_char)
            + "{"
            + str(fence_len)
            + r",}\s*$"
        )
        if closing_re.match(stripped):
            in_fence = False

    return "\n".join(out)


# ── Hygiene check function ────────────────────────────────────────────────


def check_external_citation_hygiene(cleaned: str) -> list[str]:
    """Scan for external deep-research internal citation artifacts.

    Args:
        cleaned: Report body text with fenced code blocks removed.

    Returns:
        List of warning strings (one per unique violation type found).
        Empty list means no violations.
    """
    warnings: list[str] = []

    if EXTERNAL_CITE_SANDBOX_RE.search(cleaned):
        warnings.append(
            "External citation hygiene: body text contains 'sandbox:' path(s) — "
            "these are GPT sandbox paths unreachable outside the session; "
            "convert to local assets or remove before delivery"
        )

    if EXTERNAL_CITE_TURN_RE.search(cleaned):
        warnings.append(
            "External citation hygiene: body text contains 'turnNxxx' reference(s) — "
            "these are GPT session-internal citations not resolvable by readers; "
            "resolve to real URL/DOI or remove before delivery"
        )

    if EXTERNAL_CITE_UNICODE_RE.search(cleaned):
        warnings.append(
            "External citation hygiene: body text contains \\ue000cite placeholder(s) — "
            "these are GPT-specific rendering artifacts; "
            "resolve to real URL/DOI or remove before delivery"
        )

    if EXTERNAL_CITE_FILE_ID_RE.search(cleaned):
        warnings.append(
            "External citation hygiene: body text contains 'file-xxxxxxxxxxxx' temp ID(s) — "
            "these are ephemeral session file identifiers; "
            "resolve to real source references or remove before delivery"
        )

    return warnings


# ── Main ──────────────────────────────────────────────────────────────────


def validate_file(path: Path) -> int:
    """Validate a single report file for external citation hygiene.

    Returns exit code (0 = pass, 2 = structural error).
    """
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except (OSError, UnicodeError) as exc:
        print(f"{path}: cannot read file — {exc}")
        return EXIT_STRUCTURE

    cleaned = strip_fenced_code_blocks(text)
    warnings = check_external_citation_hygiene(cleaned)

    if warnings:
        print(f"External citation hygiene warnings for {path}:")
        for w in warnings:
            print(f"  \u26a0 {w}")
        print("\nNote: these are warnings only — the report is not blocked.")
    else:
        print(f"External citation hygiene passed for {path}.")

    return EXIT_PASS


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate external deep-research citation hygiene."
    )
    parser.add_argument("path", help="Path to the report .md file")
    args = parser.parse_args(argv)

    path = Path(args.path)
    if not path.is_file():
        print(f"{path}: not a regular file")
        return EXIT_STRUCTURE

    return validate_file(path)


if __name__ == "__main__":
    raise SystemExit(main())
