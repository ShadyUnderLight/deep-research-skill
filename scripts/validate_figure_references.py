#!/usr/bin/env python3
"""Validate figure reference completeness in markdown reports.

Checks:
- Every "图X" / "Figure X" reference in body text has a corresponding
  figure definition (caption, Mermaid fence, or image reference)
- No duplicate figure captions
- Warns about uncaptioned Mermaid blocks, figure numbering gaps,
  unreferenced captions, and generic "如下图所示" references without
  a following figure entity
- Mermaid fence state is explicit: closed / mismatched / unclosed /
  invalid info string.  Unclosed or mis-closed (mismatched, shorter
  closer, Unicode-whitespace closer) Mermaid fences are BLOCKING and are
  NOT counted as legal figure entities (issue #394).

Exit codes:
  0 = passed (all clear, or only warnings)
  2 = blocking errors found

Independent advisory check: this validator is NOT part of the unified
`scripts/audit_report.py` audit registry; run it separately when figures
are part of the report (issue #394).

Usage:
    python3 scripts/validate_figure_references.py report.md
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path

# Shared fence semantics (issue #378): validated opener, first info-string
# token, same-character minimum-length closer.
from validate_contract import _fence_close_re, _fence_language, _fence_open_match

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
# Mermaid fence: first info-string token is 'mermaid' (options like
# 'mermaid theme=dark' are allowed; 'mermaid-example' is not) — matches
# the shared sanitizer's tokenization (issue #378).
MERMAID_FENCE_OPEN = re.compile(r'^[ ]{0,3}(?:`{3,}|~{3,})mermaid(?:\s|$)', re.IGNORECASE)
FENCE_CLOSE = re.compile(r'^[ ]{0,3}(`{3,}|~{3,})\s*$')
IMAGE_REF = re.compile(r'!\[.*?\]\(.*?\)')

# Code fence detection
FENCE_OPEN = re.compile(r'^[ ]{0,3}(`{3,}|~{3,})')

# Fence-shaped closer line (backtick/tilde run + whitespace), tolerant of
# Unicode whitespace.  Used only to classify near-miss closers for
# diagnostics (issue #394): the strict closer rule lives in
# validate_contract._fence_close_re.
_FENCE_SHAPE_LOOSE = re.compile(r'^[ ]{0,3}([`~]+)[\t ]*\s*$')

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


@dataclass
class MermaidFence:
    """A detected Mermaid fence block and its explicit state (issue #394).

    ``state`` is one of:
    - "closed": a valid same-character, >= opener-length closer was found
      (the block is a legal figure entity)
    - "mismatched": a bare fence-shaped closer line failed the strict rule
      (different char / shorter length / Unicode whitespace trailing)
    - "unclosed": no valid closer found before the end of the text

    ``end`` is the end-exclusive line index of the closer (None when the
    block is not closed).  ``diagnostic`` is a human-readable blocking
    message for invalid blocks (None for closed blocks).
    """
    start: int
    end: int | None
    state: str
    diagnostic: str | None


# ── Parsing functions ──────────────────────────────────────────────────────


def strip_fenced_code_blocks(text: str) -> str:
    """Blank non-rendered content, keeping mermaid fences.

    Uses the shared single-pass sanitizer (fence-aware HTML handling):
    inside a fence, HTML-looking lines are code and never start an HTML
    block; mermaid fences stay visible (figure entities); line numbers
    are preserved via blank lines (issue #378).
    """
    from validate_contract import _sanitize_visible_lines
    return "\n".join(
        _sanitize_visible_lines(text.splitlines(), keep_mermaid=True, blank=True)
    )
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


def _mermaid_fences(text: str) -> list[MermaidFence]:
    """Mermaid fence blocks with explicit state (issue #394).

    Uses the shared fence semantics (issue #378): validated opener via
    ``_fence_open_match``, first info-string token exactly 'mermaid' via
    ``_fence_language``, and a same-character minimum-length closer via
    ``_fence_close_re``.  A block is ``closed`` only when a valid closer
    is found; otherwise it is ``unclosed`` (no closer at all) or
    ``mismatched`` (a bare fence-shaped closer line that fails the strict
    rule — different character, shorter length, or Unicode whitespace
    trailing).  Invalid blocks are NOT figure entities.

    No rstrip() here: the shared fence regexes only accept spaces/tabs as
    grammar whitespace, so a trailing NBSP keeps a line from being a valid
    closer/opener (issue #378).
    """
    fences: list[MermaidFence] = []
    lines = text.splitlines()
    in_mermaid = False
    start = -1
    char = ""
    length = 0
    near_miss: tuple[int, str] | None = None  # (line index, reason)

    for i, line in enumerate(lines):
        if not in_mermaid:
            fm = _fence_open_match(line)
            if fm is not None and _fence_language(fm) == "mermaid":
                in_mermaid = True
                start = i
                char = fm.group(1)[0]
                length = len(fm.group(1))
                near_miss = None
            continue

        # Inside a mermaid block.
        if _fence_close_re(char, length).match(line):
            fences.append(MermaidFence(
                start=start, end=i + 1, state="closed", diagnostic=None
            ))
            in_mermaid = False
            near_miss = None
            continue

        # A bare fence-shaped closer line that fails the strict closer rule
        # is a near-miss closer (different char / shorter length / Unicode
        # whitespace trailing).  Record the FIRST one for diagnostics.
        if near_miss is None and _FENCE_SHAPE_LOOSE.match(line):
            near_miss = (i, _closer_mismatch_reason(char, length, line))

    if in_mermaid:
        if near_miss is not None:
            idx, reason = near_miss
            state = "mismatched"
            diagnostic = (
                f"Mermaid fence at line {start + 1} is not closed: "
                f"invalid closer at line {idx + 1} — {reason}"
            )
        else:
            state = "unclosed"
            diagnostic = (
                f"Mermaid fence at line {start + 1} is unclosed "
                f"(no valid closing fence of {length} {char}"
                f"{'s' if length > 1 else ''} found)"
            )
        fences.append(MermaidFence(
            start=start, end=None, state=state, diagnostic=diagnostic
        ))

    return fences


def _closer_mismatch_reason(fence_char: str, fence_len: int, line: str) -> str:
    """Explain why a bare fence-shaped line is not a valid closer."""
    m = _FENCE_SHAPE_LOOSE.match(line)
    other_char = m.group(1)[0] if m else ""
    other_len = len(m.group(1)) if m else 0
    if other_char != fence_char:
        return f"closer uses '{other_char}' but the opener uses '{fence_char}'"
    if other_len < fence_len:
        return (
            f"closer has {other_len} chars but the opener requires "
            f"≥ {fence_len}"
        )
    # Same character, same/longer run: only Unicode whitespace (e.g. NBSP)
    # can make a strict closer fail while the loose shape still matches.
    return "closer has non-space/tab trailing whitespace (e.g. NBSP)"


def _blank_fence_region(text: str, fences: list[MermaidFence]) -> str:
    """Blank all lines of invalid (unclosed / mismatched) mermaid fences.

    Invalid mermaid content is not a rendered figure, so figure references
    and captions inside it must not count (issue #394).  Closed fences are
    left visible.  Line numbers are preserved via blank lines.
    """
    lines = text.splitlines()
    out = list(lines)
    for f in fences:
        if f.state == "closed":
            continue
        end = f.end if f.end is not None else len(lines)
        for i in range(f.start, end):
            out[i] = ""
    return "\n".join(out)


def collect_figure_defs(text: str) -> list[FigureDef]:
    """Extract all figure definitions from raw text (fences preserved).

    Only CLOSED mermaid blocks count as figure entities; unclosed or
    mismatched fences are not legal figures (issue #394).
    """
    defs: list[FigureDef] = []
    lines = text.splitlines()
    mermaid_fences = _mermaid_fences(text)

    def in_mermaid_block(i: int) -> bool:
        # Invalid (unclosed/mismatched) fences run to the end of the text;
        # their content is blanked by the caller, so the skip is a safety
        # net rather than the primary mechanism (issue #394).
        return any(
            f.start <= i < (f.end if f.end is not None else len(lines))
            for f in mermaid_fences
        )

    # Phase 1: scan for captions (mermaid block content is the diagram
    # itself, not captions — issue #378)
    for i, line in enumerate(lines):
        if in_mermaid_block(i):
            continue
        for m in CAPTION_CHINESE.finditer(line):
            num = int(m.group(1))
            rest = line[m.end():].strip()
            defs.append(FigureDef(num, i, "caption", rest))

        for m in CAPTION_ENGLISH.finditer(line):
            num = int(m.group(1))
            rest = line[m.end():].strip()
            defs.append(FigureDef(num, i, "caption", rest))

    # Phase 2: mermaid entities (one per CLOSED block) and image references
    for f in mermaid_fences:
        if f.state == "closed":
            defs.append(FigureDef(None, f.start, "mermaid"))
    for i, line in enumerate(lines):
        if in_mermaid_block(i):
            continue
        for m in IMAGE_REF.finditer(line):
            defs.append(FigureDef(None, i, "image"))

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

    Unclosed or mismatched Mermaid fences are blocking errors and are
    NOT counted as figure entities (issue #394): a fence that never
    closes is not a rendered diagram, so it cannot satisfy a 图N/Figure N
    reference and content inside it is not body text.
    """
    # Strip code fences (but keep mermaid fences)
    cleaned = strip_fenced_code_blocks(text)

    # Classify mermaid fence state using the shared fence semantics.
    fences = _mermaid_fences(cleaned)

    # Blank invalid (unclosed / mismatched) mermaid content: it is not a
    # rendered figure, so refs/captions inside it must not count.
    body = _blank_fence_region(cleaned, fences)

    # Collect figure refs from body text (code fences stripped)
    refs = collect_figure_refs(body)

    # Collect figure defs from cleaned text (code fences stripped,
    # closed mermaid fences preserved)
    defs = collect_figure_defs(body)

    # Cross-reference
    errors, warnings = cross_reference(refs, defs)

    # Invalid mermaid fences are blocking: never a legal figure entity.
    for f in fences:
        if f.state != "closed" and f.diagnostic:
            errors.append(f"[line {f.start + 1}] {f.diagnostic}")

    return errors, warnings


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
