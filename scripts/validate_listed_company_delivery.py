#!/usr/bin/env python3
"""Listed-Company delivery-time validator.

Detects "rules exist but not executed" gaps specific to the Listed-Company /
Investment-style Research route, complementing the route-agnostic checks in
validate_report_quality.py and validate_declared_execution.py.

Checks:
1. Research-anchor block presence (FY, latest quarter, snapshot date)
2. Market snapshot table completeness (at least 5 of 8 required fields)
3. Strong wording (唯一/不可替代/>90%/垄断/only/irreplaceable/sole/monopoly
   etc.) has matching [Sxx] or equivalent inline citation — error when audit
   claims source-traceability:heavy_check_mark:, warning otherwise
4. Declared secondary routes have explicit hard-fail verification in the
   audit status block

Usage:
    python3 validate_listed_company_delivery.py report.md

Exit codes:
    0 — pass (no errors; warnings may be present)
    2 — blocking errors found
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Reuse shared helpers from validate_report_quality
from validate_report_quality import (
    strip_fenced_code_blocks,
    section_bounds,
    section_text,
    parse_table,
    find_col_index,
)

EXIT_PASS = 0
EXIT_ISSUES = 2

# ── Patterns ─────────────────────────────────────────────────────────────────

# Route detection
LISTED_COMPANY_ROUTE_RE = re.compile(
    r"(?:Listed\s*Company|Investment[\s-]*style|上市|投资研判)",
    re.IGNORECASE,
)

# Research-anchor block patterns
ANCHOR_FY_RE = re.compile(
    r"(?:最新完整财年|latest\s+FY|latest\s+full[-\s]year|FY\d{4})",
    re.IGNORECASE,
)
ANCHOR_QUARTER_RE = re.compile(
    r"(?:最新季度|最新[半]?年[度报]|latest\s+quarter|Q[1-4]\s*\d{4}|interim)",
    re.IGNORECASE,
)
ANCHOR_SNAPSHOT_RE = re.compile(
    r"(?:快照日期|snapshot\s+date|market\s+snapshot\s+date|当前股价|share\s+price)",
    re.IGNORECASE,
)

# Market snapshot table field patterns
SNAPSHOT_FIELD_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"(?:当前股价|share price|股价)", re.IGNORECASE),
    re.compile(r"(?:市值|market cap|market capitalization)", re.IGNORECASE),
    re.compile(r"PE\s*\(TTM\)", re.IGNORECASE),
    re.compile(r"PE\s*\(Forward\)|PE\s*\(Fwd\)|forward\s+PE", re.IGNORECASE),
    re.compile(r"PB\b", re.IGNORECASE),
    re.compile(r"PS\b", re.IGNORECASE),
    re.compile(r"(?:52周|52[-\s]week|52W)", re.IGNORECASE),
    re.compile(r"(?:股息率|dividend yield)", re.IGNORECASE),
]

REQUIRED_SNAPSHOT_FIELDS = 5

# Strong wording patterns — words that require explicit evidence
# Covers both Chinese and English, per ROUTING-MATRIX.md Listed Company hard-fail
STRONG_WORDING_RE = re.compile(
    r"(?:"
    r"唯一|only(?:\s+(?:company|firm|provider|supplier|player|vendor|option|source))?"
    r"|sole(?:\s+(?:provider|supplier|source|option))?"
    r"|不可替代|irreplaceable"
    r"|>90%(?!\})|超过\s*90%"
    r"|最宽护城河|strongest\s+moat|widest\s+moat"
    r"|垄断|monopoly|monopolistic"
    r"|无竞争对手|no\s+competitor"
    r"|permanent|永不|永远|永续"
    r")",
    re.IGNORECASE,
)

# Inline citation patterns (same equivalence rules as validate_report_quality)
BODY_SXX_RE = re.compile(r"\[S\d{2}\]")
AUTHOR_YEAR_RE = re.compile(
    r"\([A-Z][a-z]+(?:\s+et\s+al\.?)?,\s*\d{4}(?:,\s*[A-Za-z .]+)?\)"
)
ARXIV_RE = re.compile(r"arXiv:\d{4}\.\d{4,5}(?:v\d+)?", re.IGNORECASE)
DOI_RE = re.compile(
    r"(?:doi|DOI):\s*10\.\d{4,}/|https://doi\.org/10\.\d{4,}/"
)
NL_ATTR_RE = re.compile(
    r"据\s*(?:FY?\d{2,4}\s*)?(?:年报|招股书|公告|季报|半年报|官方报告|白皮书|研究|财报|研报|行业报告|调查报告)",
    re.IGNORECASE,
)

# Secondary route detection
SECONDARY_ROUTE_RE = re.compile(
    r"\*\*Secondary\s+route\*\*[:\s]+(.+)",
    re.IGNORECASE,
)

# Audit table patterns (same as validate_report_quality)
ROUTE_AUDIT_HEADING = re.compile(r"Route\s+and\s+audit\s+status", re.IGNORECASE)
AUDIT_COL_RE = re.compile(r"Audit|审计|检查项", re.IGNORECASE)
STATUS_COL_RE = re.compile(r"Status|状态|结果", re.IGNORECASE)
AUDIT_PASSED_RE = re.compile(r"(✅\s*)?(Passed|已通过|通过)", re.IGNORECASE)

# Source-traceability audit discipline name
SOURCE_TRACEABILITY_RE = re.compile(
    r"source[-\s]traceability", re.IGNORECASE
)

PRIMARY_ROUTE_RE = re.compile(r"\*\*Primary\s+route\*\*", re.IGNORECASE)


# ── Check functions ──────────────────────────────────────────────────────────


def _is_listed_company(text: str) -> bool:
    """Check whether the report declares a Listed-Company Primary route.

    Only checks the Primary route line (not Secondary route or fallback),
    to avoid false positives when Listed Company is a secondary attachment
    to a different primary route.
    """
    sec = section_text(text, ROUTE_AUDIT_HEADING)
    if sec is None:
        return False
    # Only search within the Primary route declaration line
    for line in sec.splitlines():
        if PRIMARY_ROUTE_RE.search(line) and LISTED_COMPANY_ROUTE_RE.search(line):
            return True
    return False


def _audit_pass_for_source_traceability(text: str) -> bool | None:
    """Return True if source-traceability audit claims :heavy_check_mark:,
    False if not passed, None if no audit table found or discipline not listed.
    """
    sec = section_text(text, ROUTE_AUDIT_HEADING)
    if sec is None:
        return None
    table = parse_table(sec)
    if table is None:
        return None

    header = table[0]
    audit_idx = find_col_index(header, [AUDIT_COL_RE])
    status_idx = find_col_index(header, [STATUS_COL_RE])
    if audit_idx == -1 or status_idx == -1:
        return None

    for row in table[1:]:
        if len(row) <= max(audit_idx, status_idx):
            continue
        discipline = row[audit_idx].strip()
        status = row[status_idx].strip()
        if SOURCE_TRACEABILITY_RE.search(discipline):
            return bool(AUDIT_PASSED_RE.match(status))

    return None  # source-traceability not listed in audit table


def _secondary_routes(text: str) -> list[str]:
    """Extract declared secondary route names from the audit status block."""
    sec = section_text(text, ROUTE_AUDIT_HEADING)
    if sec is None:
        return []
    # Match all occurrences of **Secondary route**: <name>
    matches = SECONDARY_ROUTE_RE.findall(sec)
    return [m.strip() for m in matches if m.strip()]


def _audit_discipline_names(text: str) -> list[str]:
    """Return all discipline names from the audit status table."""
    sec = section_text(text, ROUTE_AUDIT_HEADING)
    if sec is None:
        return []
    table = parse_table(sec)
    if table is None or len(table) < 2:
        return []

    header = table[0]
    audit_idx = find_col_index(header, [AUDIT_COL_RE])
    if audit_idx == -1:
        return []

    return [row[audit_idx].strip() for row in table[1:] if len(row) > audit_idx]


def _has_inline_citation(text_block: str) -> bool:
    """Check if text has [Sxx] or equivalent inline citation."""
    if BODY_SXX_RE.search(text_block):
        return True
    if AUTHOR_YEAR_RE.search(text_block):
        return True
    if ARXIV_RE.search(text_block):
        return True
    if DOI_RE.search(text_block):
        return True
    if NL_ATTR_RE.search(text_block):
        return True
    return False


def check_research_anchor_block(text: str, path: Path) -> list[str]:
    """Check that a Listed-Company report has a visible research-anchor block.

    Required: at least 2 of {FY reference, latest quarter, snapshot date/market
    data reference}.  The anchor block is the current-state lock that prevents
    stale-anchor drift (see ROUTING-MATRIX.md Listed Company hard-fail).
    """
    hits = 0
    if ANCHOR_FY_RE.search(text):
        hits += 1
    if ANCHOR_QUARTER_RE.search(text):
        hits += 1
    if ANCHOR_SNAPSHOT_RE.search(text):
        hits += 1

    if hits < 2:
        return [
            f"{path}: Listed-Company report lacks a complete research-anchor block "
            f"(found {hits}/3 required time-layer references: latest FY, "
            f"latest quarter/interim, current market snapshot date)"
        ]
    return []


def check_market_snapshot(text: str, path: Path) -> list[str]:
    """Check that a Listed-Company report's market snapshot has >=5 of 8 fields.

    The 8 fields correspond to the listed-company-report checklist template:
    share price, market cap, PE(TTM), PE(Forward), PB, PS, 52-week range,
    dividend yield.

    Returns errors (warning-level: missing 2-4 fields; no error for 0-1)
    since the ROUTING-MATRIX.md hard-fail requires a complete snapshot.
    We use a warning threshold at <5 fields because some reports split
    the snapshot across sections.
    """
    # Find the market snapshot section — look for heading patterns
    # and scan the surrounding text for field indicators
    snapshot_heading = re.compile(
        r"(?:市场快照|market snapshot|financial snapshot|关键指标|key metrics)",
        re.IGNORECASE,
    )
    bounds = section_bounds(text, snapshot_heading)
    scan_region = text  # fallback: scan entire document
    if bounds is not None:
        start, end = bounds
        lines = text.splitlines()
        scan_region = "\n".join(lines[start : min(end, start + 60)])

    # Count matched field patterns
    matched = sum(1 for pat in SNAPSHOT_FIELD_PATTERNS if pat.search(scan_region))
    if matched < REQUIRED_SNAPSHOT_FIELDS:
        return [
            f"{path}: Listed-Company market snapshot has only {matched}/8 "
            f"required fields (expected >= {REQUIRED_SNAPSHOT_FIELDS}: "
            f"share price, market cap, PE(TTM), PE(Forward), PB, PS, "
            f"52-week range, dividend yield)"
        ]
    return []


def check_strong_wording(text: str, path: Path) -> tuple[list[str], list[str]]:
    """Check strong wording for matching inline citations.

    Strategy: find all strong-word matches, then for each, check whether the
    surrounding sentence/paragraph has an [Sxx] or equivalent citation.
    Absent citations are:
    - errors if the audit block claims source-traceability :heavy_check_mark:
    - warnings otherwise

    Returns (errors, warnings).
    """
    errors: list[str] = []
    warnings: list[str] = []

    aucit = _audit_pass_for_source_traceability(text)

    # Split text into sentences (approximate) for context window
    sentences = re.split(r"(?<=[。！？.!?\n])\s*", text)
    uncited_words: list[str] = []

    for sentence in sentences:
        words_in_sentence = STRONG_WORDING_RE.findall(sentence)
        if not words_in_sentence:
            continue
        # Check if this sentence (or adjacent context) has a citation
        if not _has_inline_citation(sentence):
            # Record the first unique strong word found
            word = words_in_sentence[0] if isinstance(words_in_sentence[0], str) else words_in_sentence[0][0]
            preview = word.strip()[:30]
            uncited_words.append(preview)

    if not uncited_words:
        return [], []

    msg = (
        f"{path}: {len(uncited_words)} instance(s) of strong wording "
        f"({', '.join(uncited_words[:5])}) without matching inline citation"
    )
    if len(uncited_words) > 5:
        msg += f", plus {len(uncited_words) - 5} more"

    if aucit is True:
        # Report claims source-traceability passed but strong wording uncited
        errors.append(
            f"{msg}; source-traceability is marked :heavy_check_mark: "
            f"but these claims lack body-level evidence"
        )
    else:
        warnings.append(f"{msg}; consider adding [Sxx] or equivalent citation")

    return errors, warnings


def check_secondary_route_hard_fail(text: str, path: Path) -> list[str]:
    """Check that declared secondary routes have explicit hard-fail rows.

    Per ROUTING-MATRIX.md "Secondary route hard-fail requirement", every
    declared secondary route must have its hard-fail conditions independently
    verified.  We check that the audit table contains a discipline row whose
    name overlaps with each declared secondary route.

    Returns warnings (non-blocking because the route-specific validator
    may not cover every secondary route with a dedicated row name).
    """
    routes = _secondary_routes(text)
    if not routes:
        return []

    disciplines = _audit_discipline_names(text)
    warnings: list[str] = []

    for route in routes:
        # Normalize route name for loose matching
        route_keywords = route.lower().split()
        has_resolution = False
        for discipline in disciplines:
            disc_lower = discipline.lower()
            # Check if any keyword from the route appears in the discipline name
            if any(kw in disc_lower for kw in route_keywords if len(kw) > 3):
                has_resolution = True
                break
            # Also check for generic patterns like "secondary hard-fail"
            if "hard" in disc_lower and "fail" in disc_lower:
                has_resolution = True
                break

        if not has_resolution:
            route_preview = route[:60]
            warnings.append(
                f"{path}: secondary route '{route_preview}' is declared "
                f"but no corresponding hard-fail verification row found "
                f"in the audit status table"
            )

    return warnings


# ── Main validate function ───────────────────────────────────────────────────


def validate_file(path: Path) -> tuple[list[str], list[str]]:
    """Run all Listed-Company delivery checks on a report file.

    Returns (errors, warnings):
    - errors — blocking; must be fixed before delivery
    - warnings — non-blocking; quality signals
    """
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except (OSError, UnicodeError) as exc:
        return [f"{path}: cannot read file — {exc}"], []

    cleaned = strip_fenced_code_blocks(text)

    # Only run Listed-Company-specific checks if the report declares
    # this route.  Non-listed-company reports pass through silently.
    if not _is_listed_company(cleaned):
        return [], []

    errors: list[str] = []
    warnings: list[str] = []

    # 1. Research-anchor block
    errors.extend(check_research_anchor_block(cleaned, path))

    # 2. Market snapshot completeness
    warnings.extend(check_market_snapshot(cleaned, path))

    # 3. Strong wording scan
    e, w = check_strong_wording(cleaned, path)
    errors.extend(e)
    warnings.extend(w)

    # 4. Secondary route hard-fail verification
    warnings.extend(check_secondary_route_hard_fail(cleaned, path))

    return errors, warnings


# ── CLI entry point ──────────────────────────────────────────────────────────


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Listed-Company delivery-time validator.",
    )
    parser.add_argument("paths", nargs="+", help="Markdown report file(s) to validate")
    args = parser.parse_args(argv)

    all_errors: list[str] = []
    all_warnings: list[str] = []
    for raw_path in args.paths:
        path = Path(raw_path)
        if not path.is_file():
            all_errors.append(f"{path}: not a regular file")
            continue
        errors, warnings = validate_file(path)
        all_errors.extend(errors)
        all_warnings.extend(warnings)

    if all_warnings:
        print("Listed-Company delivery validation warnings:")
        for w in all_warnings:
            print(f"  :warning: {w}")

    if all_errors:
        print("Listed-Company delivery validation failed:")
        for e in all_errors:
            print(f"  - {e}")
        return EXIT_ISSUES

    if not all_warnings:
        print("Listed-Company delivery validation passed.")
    return EXIT_PASS


if __name__ == "__main__":
    raise SystemExit(main())
