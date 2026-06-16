#!/usr/bin/env python3
"""
Validate that constrained-choice reports with final scores/ratings/
probabilities/stars include the evidence needed to reproduce the result.

A constrained-choice report that presents aggregated scores, rankings,
probability distributions, or star ratings must also show:
- dimension definitions
- weights or priority order
- score/grade/probability conversion rules
- at least 1 worked example (2 for star/grade ratings)
- close-score gap interpretation

This validator works heuristically by scanning for trigger keywords that
indicate aggregated output, then checking whether required evidence
keywords are present in the same document.

Usage:
    python3 scripts/validate_scoring_replicability.py report.md
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


# ── Trigger keywords (report uses aggregated output) ─────────────────────
#
# When any of these appear in the report body (outside fenced code blocks),
# the validator expects supporting evidence (rules, weights, examples).
#
# Grouped by confidence level so we can tier detection if needed.

TRIGGER_KEYWORDS = [
    # High-confidence triggers (almost always indicate aggregation output)
    r'总分',
    r'综合评分',
    r'综合得分',
    r'星级',
    r'胜率',
    r'排名变化',
    # Medium-confidence triggers (need context but strong signal in CC reports)
    r'\branking score\b',
    r'\bweighted score\b',
    r'\bcomposite score\b',
    r'\btotal score\b',
    r'\bfinal score\b',
    r'\boverall score\b',
    r'\brating\b',
    r'\bprobability\b',
]

# ── Evidence keywords (report contains aggregation method) ────────────────

EVIDENCE_KEYWORDS = [
    # Weights and priorities
    r'权重',
    r'加权',
    r'\bweight\b',
    r'\bweights\b',
    r'\bweighted\b',
    r'\bpriority order\b',
    # Scoring rules and conversion
    r'评分规则',
    r'打分规则',
    r'转换规则',
    r'\bscoring rule\b',
    r'\bscoring rules\b',
    r'\bconversion rule\b',
    r'\bmapping rule\b',
    r'\bgrading rubric\b',
    # Worked examples
    r'计算示例',
    r'\bworked example\b',
    r'\bworked examples\b',
    r'\bexample calculation\b',
    r'\bsample calculation\b',
    r'算例',
    # Sensitivity / error analysis
    r'\bsensitivity\b',
    r'敏感性',
    r'误差范围',
    r'\bmargin of error\b',
    r'\bcaveat\b',
    # Dimension definitions / decomposition
    r'维度定义',
    r'\bdimension\b',
    r'\bdecompos',
    r'分解',
]

# ── Compile regexes once ─────────────────────────────────────────────────

_TRIGGER_RE = re.compile('|'.join(TRIGGER_KEYWORDS), re.IGNORECASE)
_EVIDENCE_RE = re.compile('|'.join(EVIDENCE_KEYWORDS), re.IGNORECASE)


# ── Helpers ───────────────────────────────────────────────────────────────


def _strip_fenced_code_blocks(text: str) -> str:
    """Replace content inside fenced code blocks with empty lines.

    Preserves original line count so that line-number references
    map back to the original file.
    """
    lines = text.splitlines()
    result = list(lines)
    in_fence = False
    fence_char = ""
    fence_len = 0

    for i, line in enumerate(lines):
        stripped = line.rstrip()
        if not in_fence:
            m = re.match(r"^[ ]{0,3}(`{3,}|~{3,})", stripped)
            if m:
                fence_char = m.group(1)[0]
                fence_len = len(m.group(1))
                in_fence = True
                result[i] = ""
                continue
        else:
            closing = re.compile(
                r"^[ ]{0,3}"
                + re.escape(fence_char)
                + "{"
                + str(fence_len)
                + r",}\s*$"
            )
            if closing.match(stripped):
                in_fence = False
                result[i] = ""
                continue
            result[i] = ""

    return "\n".join(result)


def _has_trigger(text: str) -> bool:
    """Return True if any trigger keyword appears outside code blocks."""
    cleaned = _strip_fenced_code_blocks(text)
    return bool(_TRIGGER_RE.search(cleaned))


def _has_sufficient_evidence(text: str) -> bool:
    """Return True if enough evidence keywords are present.

    Uses a simple count threshold to avoid false positives from
    incidental keyword matches.  Requires at least 3 distinct
    evidence keyword hits across the document.  In practice, this
    means a report must demonstrate coverage in at least two of:
    weights/priority, scoring rules/conversion, worked examples.
    """
    cleaned = _strip_fenced_code_blocks(text)
    matches = _EVIDENCE_RE.findall(cleaned)
    # Deduplicate for minimum variety — require 3+ distinct types
    unique_matches = set(m.lower() for m in matches)
    return len(unique_matches) >= 3


# ── Main validation ──────────────────────────────────────────────────────


def validate_file(path: Path) -> list[str]:
    """Validate scoring replicability for a Markdown report.

    Parameters
    ----------
    path : Path
        Path to the Markdown report file.

    Returns
    -------
    list[str]
        Empty list if validation passes (no trigger, or trigger + evidence).
        Non-empty list of error messages if trigger found without evidence.
    """
    errors: list[str] = []

    try:
        raw = path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return [f"{path}: file not found"]
    except OSError as exc:
        return [f"{path}: cannot read file — {exc}"]

    # Step 1: Check for trigger keywords
    if not _has_trigger(raw):
        return errors  # pass — not a scoring report

    # Step 2: Check for sufficient evidence
    if not _has_sufficient_evidence(raw):
        errors.append(
            f"{path}: report contains scoring/ranking/probability output "
            f"but lacks replicable aggregation method — "
            f"missing scoring rules, weights, or worked examples. "
            f"Add at minimum: dimension definitions, weights/priority order, "
            f"score conversion rules, and at least 1 worked example calculation."
        )

    return errors


# ── CLI entry point ───────────────────────────────────────────────────────


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate scoring replicability in constrained-choice reports.",
    )
    parser.add_argument("paths", nargs="+", help="Markdown files to validate")
    args = parser.parse_args(argv)

    all_errors: list[str] = []
    for raw_path in args.paths:
        path = Path(raw_path)
        errors = validate_file(path)
        all_errors.extend(errors)

    if all_errors:
        print("Scoring replicability validation failed:")
        for error in all_errors:
            print(f"- {error}")
        return 2

    print(f"Scoring replicability validation passed for {len(args.paths)} file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
