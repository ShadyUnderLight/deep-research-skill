#!/usr/bin/env python3
"""Validate figure reference completeness in markdown reports.

Checks:
- Every "图X" / "Figure X" reference in body text has a corresponding
  figure definition (caption, Mermaid fence, or image reference)
- No duplicate figure captions
- Warns about uncaptioned Mermaid blocks, figure numbering gaps,
  unreferenced captions, and generic "如下图所示" references without
  a following figure entity

Exit codes:
  0 = passed (all clear, or only warnings)
  2 = blocking errors found

Usage:
    python3 scripts/validate_figure_references.py report.md
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# ── Regex patterns ─────────────────────────────────────────────────────────

# Figure REFERENCES in body text (not inside code fences, not captions)
REF_CHINESE = re.compile(r'(?<![\d:：])(?:[见图]|如图)\s*(\d+)(?![\d:：])')
REF_ENGLISH = re.compile(r'(?<!\d)(?:[Ff]igure|[Ff]ig\.?)\s*(\d+)(?![\d:：])')
REF_GENERIC = re.compile(r'(?:如下图|如下图所示|见下图|如下图的|上图|如上图|如上图所示)')

# Figure DEFINITIONS (captions)
CAPTION_CHINESE = re.compile(r'(?:^|(?<=\n))\s*图\s*(\d+)\s*[：:]')
CAPTION_ENGLISH = re.compile(
    r'(?:^|(?<=\n))\s*\*{0,2}(?:[Ff]igure|[Ff]ig\.?)\s*(\d+)\s*[：:]\s*\*{0,2}'
)

# Figure ENTITIES (Mermaid fences, images)
MERMAID_FENCE_OPEN = re.compile(r'^[ ]{0,3}`{3,}mermaid\s*$', re.IGNORECASE)
FENCE_CLOSE = re.compile(r'^[ ]{0,3}(`{3,}|~{3,})\s*$')
IMAGE_REF = re.compile(r'!\[.*?\]\(.*?\)')

# Code fence detection
FENCE_OPEN = re.compile(r'^[ ]{0,3}(`{3,}|~{3,})')

# ── Data structures ────────────────────────────────────────────────────────


class FigureRef:
    """A reference to a figure in body text."""
    __slots__ = ('num', 'line', 'raw')

    def __init__(self, num: int | None, line: int, raw: str) -> None:
        self.num = num      # None for generic refs (见下图)
        self.line = line    # 0-indexed line number
        self.raw = raw      # original matched text

    def __repr__(self) -> str:
        return f"FigureRef(num={self.num}, line={self.line}, raw={self.raw!r})"


class FigureDef:
    """A figure definition (caption, Mermaid block, or image reference)."""
    __slots__ = ('num', 'line', 'kind', 'caption_text')

    def __init__(self, num: int | None, line: int, kind: str,
                 caption_text: str | None = None) -> None:
        self.num = num            # None for uncaptioned entities
        self.line = line          # 0-indexed line number
        self.kind = kind          # "caption", "mermaid", "image"
        self.caption_text = caption_text

    def __repr__(self) -> str:
        return f"FigureDef(num={self.num}, line={self.line}, kind={self.kind})"


# ── Parsing functions ──────────────────────────────────────────────────────


def strip_fenced_code_blocks(text: str) -> str:
    """Replace content inside fenced code blocks with empty lines.
    
    Preserves line count so error line numbers map to original file.
    Excludes mermaid fences (they are figure entities, not code blocks).
    """
    lines = text.splitlines()
    result = list(lines)  # copy
    in_fence = False
    fence_char = ""
    fence_len = 0
    is_mermaid = False
    opener_line = -1

    for i, line in enumerate(lines):
        stripped = line.rstrip()

        if not in_fence:
            m = FENCE_OPEN.match(stripped)
            if m:
                fence_char = m.group(1)[0]
                fence_len = len(m.group(1))
                # Check if this is a mermaid fence
                rest = stripped[fence_len:].strip()
                is_mermaid = rest.lower().startswith('mermaid')
                if is_mermaid:
                    # Keep mermaid fences visible (don't blank them)
                    continue
                in_fence = True
                opener_line = i
                result[i] = ""
                continue
        else:
            closing = re.compile(
                r'^[ ]{0,3}'
                + re.escape(fence_char)
                + '{' + str(fence_len) + r',}\s*$'
            )
            if closing.match(stripped):
                in_fence = False
                result[i] = ""
                is_mermaid = False
                continue
            result[i] = ""

    return "\n".join(result)


def collect_figure_refs(cleaned: str) -> list[FigureRef]:
    """Extract all figure references from body text (outside code fences)."""
    refs: list[FigureRef] = []
    lines = cleaned.splitlines()

    for i, line in enumerate(lines):
        # Chinese number refs
        for m in REF_CHINESE.finditer(line):
            num = int(m.group(1))
            refs.append(FigureRef(num, i, m.group()))

        # English number refs
        for m in REF_ENGLISH.finditer(line):
            num = int(m.group(1))
            refs.append(FigureRef(num, i, m.group()))

        # Generic refs (见下图, 如下图所示)
        for m in REF_GENERIC.finditer(line):
            refs.append(FigureRef(None, i, m.group()))

    return refs


def collect_figure_defs(text: str) -> list[FigureDef]:
    """Extract all figure definitions from raw text (fences preserved)."""
    defs: list[FigureDef] = []
    lines = text.splitlines()

    # Phase 1: scan for captions
    for i, line in enumerate(lines):
        for m in CAPTION_CHINESE.finditer(line):
            num = int(m.group(1))
            rest = line[m.end():].strip()
            defs.append(FigureDef(num, i, "caption", rest))

        for m in CAPTION_ENGLISH.finditer(line):
            num = int(m.group(1))
            rest = line[m.end():].strip()
            defs.append(FigureDef(num, i, "caption", rest))

    # Phase 2: scan for Mermaid fences and image references
    in_mermaid = False
    mermaid_start = -1
    for i, line in enumerate(lines):
        stripped = line.rstrip()

        # Mermaid fence detection
        if not in_mermaid:
            if MERMAID_FENCE_OPEN.match(stripped):
                in_mermaid = True
                mermaid_start = i
                continue
        else:
            closing = re.compile(
                r'^[ ]{0,3}(`{3,}|~{3,})\s*$'
            )
            if closing.match(stripped):
                in_mermaid = False
                # Check if this mermaid block already has a caption
                has_num_caption = any(
                    d.num is not None and d.kind == "caption"
                    and abs(d.line - mermaid_start) < 5
                    for d in defs
                )
                defs.append(
                    FigureDef(None if not has_num_caption else None,
                              mermaid_start, "mermaid")
                )
                mermaid_start = -1
                continue

        # Image references (outside mermaid blocks)
        if not in_mermaid:
            for m in IMAGE_REF.finditer(line):
                defs.append(FigureDef(None, i, "image"))

    # Handle unclosed mermaid fence
    if in_mermaid:
        defs.append(FigureDef(None, mermaid_start, "mermaid"))

    return defs


def _next_entity_line(defs: list[FigureDef], after_line: int) -> int | None:
    """Find the next figure entity (mermaid/image) after a given line."""
    candidates = [
        d.line for d in defs
        if d.kind in ("mermaid", "image") and d.line > after_line
    ]
    return min(candidates) if candidates else None


# ── Cross-reference logic ──────────────────────────────────────────────────


def cross_reference(
    refs: list[FigureRef],
    defs: list[FigureDef],
) -> tuple[list[str], list[str]]:
    """Cross-reference figure refs against definitions.
    
    Returns (errors, warnings).
    """
    errors: list[str] = []
    warnings: list[str] = []

    # Build lookup from explicit figure numbers
    defs_by_num: dict[int, list[FigureDef]] = {}
    for d in defs:
        if d.num is not None:
            defs_by_num.setdefault(d.num, []).append(d)

    # Collect entity line numbers (for sequential matching)
    entity_lines = sorted([
        d.line for d in defs if d.kind in ("mermaid", "image")
    ])
    entity_count = len(entity_lines)

    # Track which numbers have been referenced
    refd_numbers: set[int] = set()
    caption_numbers: set[int] = set()

    # Check numeric refs against definitions
    for ref in refs:
        if ref.num is None:
            continue  # generic refs handled separately

        refd_numbers.add(ref.num)

        if ref.num in defs_by_num:
            # Has an explicit caption — OK
            continue

        # No explicit caption — check if enough entities exist
        if entity_count >= ref.num:
            warnings.append(
                f"[line {ref.line + 1}] 图{ref.num} is referenced but "
                f"has no explicit caption (found {entity_count} figure "
                f"entities, may be entity #{ref.num})"
            )
        else:
            errors.append(
                f"[line {ref.line + 1}] 图{ref.num} is referenced in text "
                f"but no corresponding figure definition exists "
                f"(found {entity_count} figure entities, need at least {ref.num})"
            )

    # Track which numbers are defined by captions
    for d in defs:
        if d.num is not None and d.kind == "caption":
            caption_numbers.add(d.num)

    # Check for duplicate captions
    for num, dlist in defs_by_num.items():
        caption_list = [d for d in dlist if d.kind == "caption"]
        if len(caption_list) > 1:
            lines_str = ", ".join(str(d.line + 1) for d in caption_list)
            errors.append(
                f"图{num} has {len(caption_list)} captions "
                f"(lines {lines_str})"
            )

    # Check for figure numbering gaps (only captions + referenced)
    all_numbers = sorted(caption_numbers | refd_numbers)
    if len(all_numbers) >= 2:
        for i in range(len(all_numbers) - 1):
            expected = all_numbers[i] + 1
            if expected < all_numbers[i + 1]:
                warnings.append(
                    f"Figure number gap: 图{all_numbers[i]} → "
                    f"图{all_numbers[i + 1]} "
                    f"(missing 图{expected})"
                )

    # Check for captions never referenced in body
    for num in sorted(caption_numbers):
        if num not in refd_numbers:
            warnings.append(
                f"图{num} caption defined but never referenced in body text"
            )

    # Check for uncaptioned Mermaid blocks
    for d in defs:
        if d.kind == "mermaid":
            # Check if there's a caption nearby (within 5 lines)
            has_nearby_caption = any(
                df.num is not None and df.kind == "caption"
                and abs(df.line - d.line) <= 5
                for df in defs
            )
            if not has_nearby_caption:
                warnings.append(
                    f"[line {d.line + 1}] Mermaid diagram has no adjacent "
                    f"caption (add a 图N: or Figure N: caption nearby)"
                )

    # Check generic refs (见下图) — need at least one entity after them
    for ref in refs:
        if ref.num is not None:
            continue
        # Generic ref — check if any entity follows
        next_entity = _next_entity_line(defs, ref.line)
        if next_entity is None:
            warnings.append(
                f"[line {ref.line + 1}] \"{ref.raw}\" references a figure "
                f"but no figure entity (Mermaid/image) follows"
            )

    return errors, warnings


def validate_figure_references(text: str) -> tuple[list[str], list[str]]:
    """Main validation function.
    
    Returns (errors, warnings) where errors are blocking (exit code 2)
    and warnings are advisory (exit code 0).
    """
    # Strip code fences (but keep mermaid fences)
    cleaned = strip_fenced_code_blocks(text)

    # Collect figure refs from body text (code fences stripped)
    refs = collect_figure_refs(cleaned)

    # Collect figure defs from raw text (includes mermaid fences)
    defs = collect_figure_defs(text)

    # Cross-reference
    return cross_reference(refs, defs)


# ── CLI ────────────────────────────────────────────────────────────────────


def validate_file(path: Path) -> int:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except (OSError, UnicodeError) as exc:
        print(f"{path}: cannot read file — {exc}")
        return 2

    errors, warnings = validate_figure_references(text)

    if warnings:
        label = "warnings" if errors else "passed with warnings"
        print(f"Figure reference validation {label} for {path}:")
        for w in warnings:
            print(f"  ⚠ {w}")

    if errors:
        print(f"Figure reference validation failed for {path}:")
        for e in errors:
            print(f"  ✗ {e}")
        return 2

    if not warnings:
        print(f"Figure reference validation passed for {path}.")

    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate figure reference completeness in markdown reports."
    )
    parser.add_argument("path", help="Path to the report .md file")
    args = parser.parse_args(argv)

    path = Path(args.path)
    if not path.is_file():
        print(f"{path}: not a regular file")
        return 2

    return validate_file(path)


if __name__ == "__main__":
    raise SystemExit(main())
