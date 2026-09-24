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
from datetime import date
from pathlib import Path

# Reuse shared helpers from validate_report_quality
from validate_report_quality import (
    section_bounds,
    section_text,
    parse_table,
    find_col_index,
    get_route_name,
)
from validate_contract import sanitize_visible_markdown

import registry_loader
from registry_loader import RegistryError, UnknownRouteError

EXIT_PASS = 0
EXIT_ISSUES = 2

# ── Patterns ─────────────────────────────────────────────────────────────────

# Route detection
LISTED_COMPANY_ROUTE_RE = re.compile(
    r"(?:Listed\s*Company|Investment[\s-]*style|上市|投资研判)",
    re.IGNORECASE,
)

# Research-anchor fields are parsed as labeled values, rather than searching
# the whole field segment: a period/date in a note after "待补充" must not
# masquerade as the current anchor (review P1).
ANCHOR_FY_LABEL_RE = re.compile(
    r"(?:最新完整财年|最新FY|最新财年|latest\s+FY|latest\s+full[-\s]year)\s*[:：]\s*(.*)$",
    re.IGNORECASE,
)
ANCHOR_QUARTER_LABEL_RE = re.compile(
    r"(?:最新季度|最新半年报|latest\s+quarter|interim)\s*[:：]\s*(.*)$",
    re.IGNORECASE,
)
ANCHOR_SNAPSHOT_LABEL_RE = re.compile(
    r"(?:快照日期|市场快照|snapshot\s+date|market\s+snapshot\s+date)\s*[:：]\s*(.*)$",
    re.IGNORECASE,
)
ANCHOR_VALUE_PLACEHOLDER_RE = re.compile(
    r"\b(?:tbd|n/?a|none|unknown|pending|maybe|perhaps|not provided|"
    r"not available|unavailable)\b"
    r"|待补充|待填写|待定|待确认|待核实|待更新|暂无",
    re.IGNORECASE,
)
ANCHOR_FY_VALUE_RE = re.compile(
    r"^(?:FY\s*20\d{2}|20\d{2}(?:年(?:年报|报|年度|年)?)?)(?=$|[\s（(,，。；;])",
    re.IGNORECASE,
)
ANCHOR_QUARTER_VALUE_RE = re.compile(
    r"^(?:20\d{2}\s*[Qq][1-4]|[Qq][1-4]\s*20\d{2}|"
    r"20\d{2}\s*[Hh][12]|[Hh][12]\s*20\d{2}|"
    r"20\d{2}年[一二三四]季(?:报|度)?)(?=$|[\s（(,，。；;])",
    re.IGNORECASE,
)
ANCHOR_SNAPSHOT_VALUE_RE = re.compile(
    r"^(?:(?:as\s+of|截至|截至日期)\s*)?"
    r"\d{4}[-/]\d{1,2}[-/]\d{1,2}(?=$|[\sTt（(,，。；;])",
    re.IGNORECASE,
)

# The visible research-anchor block heading.  Anchor time-layers must be found
# inside this section — keywords in other sections, the Source Register or body
# prose do not count (issue #436 D2).
ANCHOR_BLOCK_RE = re.compile(
    r"研究锚定|research[\s-]*anchor|current[\s-]*state[\s-]*anchor",
    re.IGNORECASE,
)

# Heading-less single-line anchor form allowed by the report template:
#   研究锚定：最新FY：FY2025｜最新季度：2026Q1｜市场快照：2026-05-29
ANCHOR_LINE_RE = re.compile(
    r"^\s*(?:研究锚定|research\s*anchor)\s*[:：]", re.IGNORECASE
)

REQUIRED_SNAPSHOT_FIELDS = 5
_SNAPSHOT_NUMBER = r"\d+(?:,\d{3})*(?:\.\d+)?"
_SNAPSHOT_CURRENCY = (
    r"(?:(?:USD|EUR|GBP|JPY|CNY|NTD|TWD|HKD|CAD|AUD|RMB)\s*|"
    r"(?:US|NT|HK|CN)\s*[$€£¥￥]\s*|[$€£¥￥]\s*)?"
)
_SNAPSHOT_APPROX = r"(?:~|≈|约)?\s*"
_SNAPSHOT_VALUE_END = (
    r"(?=\s*(?:$|[（(\[,，；;]|"
    r"(?:USD|EUR|GBP|JPY|CNY|NTD|TWD|HKD|CAD|AUD|RMB)\b|"
    r"元|美元|台币|新台币))"
)
SNAPSHOT_PRICE_RE = re.compile(
    r"^\s*" + _SNAPSHOT_APPROX + _SNAPSHOT_CURRENCY
    + _SNAPSHOT_NUMBER + _SNAPSHOT_VALUE_END,
    re.IGNORECASE,
)
SNAPSHOT_MARKET_CAP_RE = re.compile(
    r"^\s*" + _SNAPSHOT_APPROX + _SNAPSHOT_CURRENCY + r"(?:"
    + _SNAPSHOT_NUMBER
    + r"\s*(?:[KMBT](?:n)?\b|thousand\b|million\b|billion\b|"
    r"trillion\b|万|亿|兆)"
    + r"|(?:\d{1,3}(?:,\d{3}){2,}|\d{7,})"
    + r")"
    + _SNAPSHOT_VALUE_END,
    re.IGNORECASE,
)
SNAPSHOT_RATIO_RE = re.compile(
    r"^\s*" + _SNAPSHOT_APPROX + _SNAPSHOT_NUMBER
    + r"\s*(?:x|倍)?" + _SNAPSHOT_VALUE_END,
    re.IGNORECASE,
)
SNAPSHOT_PERCENT_RE = re.compile(
    r"^\s*" + _SNAPSHOT_APPROX + _SNAPSHOT_NUMBER
    + r"\s*(?:%|percent|百分比)"
    + _SNAPSHOT_VALUE_END,
    re.IGNORECASE,
)
SNAPSHOT_DATE_PREFIX_RE = re.compile(
    r"^\s*\d{4}[-/]\d{1,2}[-/]\d{1,2}(?=\s|$|[Tt]|[（(,，；;])"
)
SNAPSHOT_CURRENCY_MARKER_RE = re.compile(
    r"[$€£¥￥]|\b(?:USD|EUR|GBP|JPY|CNY|NTD|TWD|HKD|CAD|AUD|RMB)\b|"
    r"元|美元|台币|新台币",
    re.IGNORECASE,
)
SNAPSHOT_PLACEHOLDER_RE = re.compile(
    r"\b(?:tbd|n/?a|none|unknown|pending|maybe|perhaps|not provided|"
    r"not available|unavailable)\b"
    r"|待补充|待填写|待定|待确认|待核实|待更新|暂无|__",
    re.IGNORECASE,
)
SNAPSHOT_RANGE_RE = re.compile(
    r"^\s*" + _SNAPSHOT_APPROX + _SNAPSHOT_CURRENCY + _SNAPSHOT_NUMBER
    + r"\s*(?:-|–|—|~|至|到|to)\s*"
    + _SNAPSHOT_CURRENCY + _SNAPSHOT_NUMBER + _SNAPSHOT_VALUE_END,
    re.IGNORECASE,
)
SNAPSHOT_FIELD_RULES: tuple[
    tuple[re.Pattern[str], re.Pattern[str], bool], ...
] = (
    (re.compile(r"(?:当前股价|share price|股价)", re.IGNORECASE), SNAPSHOT_PRICE_RE, False),
    (
        re.compile(r"(?:市值|market cap|market capitalization)", re.IGNORECASE),
        SNAPSHOT_MARKET_CAP_RE,
        False,
    ),
    (re.compile(r"PE\s*\(TTM\)", re.IGNORECASE), SNAPSHOT_RATIO_RE, False),
    (
        re.compile(r"PE\s*\(Forward\)|PE\s*\(Fwd\)|forward\s+PE", re.IGNORECASE),
        SNAPSHOT_RATIO_RE,
        False,
    ),
    (re.compile(r"PB\b", re.IGNORECASE), SNAPSHOT_RATIO_RE, False),
    (re.compile(r"PS\b", re.IGNORECASE), SNAPSHOT_RATIO_RE, False),
    (
        re.compile(r"(?:52周|52[-\s]week|52W)", re.IGNORECASE),
        SNAPSHOT_RANGE_RE,
        True,
    ),
    (
        re.compile(r"(?:股息率|dividend yield)", re.IGNORECASE),
        SNAPSHOT_PERCENT_RE,
        False,
    ),
)

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
    """Legacy display-text adapter: does the report declare Listed-Company?

    Only used when the caller has NOT supplied an orchestrator-resolved
    canonical ``route_id``.  When the orchestrator runs this validator it
    already resolved the route (issue #436 D1) and passes the canonical id,
    so this display-text guess must never be allowed to silently skip the
    dedicated checks.
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


def _anchor_block_text(text: str) -> str | None:
    """Locate the visible research-anchor block.

    Returns the anchor section text whether the report uses a ``## 研究锚定块``
    heading or the template's heading-less single-line ``研究锚定：…`` form.
    Returns ``None`` when neither form is present.
    """
    section = section_text(text, ANCHOR_BLOCK_RE)
    if section is not None:
        return section
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if ANCHOR_LINE_RE.match(line):
            # Collect the label line plus immediately following continuation
            # lines (bullet sub-fields) until a blank line or new heading.
            collected = [line]
            j = i + 1
            while j < len(lines):
                nxt = lines[j]
                if not nxt.strip() or nxt.lstrip().startswith("#"):
                    break
                collected.append(nxt)
                j += 1
            return "\n".join(collected)
    return None


def _anchor_field_value(
    block: str, label_pattern: re.Pattern[str]
) -> str | None:
    """Return the value immediately attached to one anchor label.

    The compact template uses fullwidth separators; the detailed form uses one
    labeled field per line. Splitting before matching keeps a neighboring field
    or an unrelated note from supplying this field's value.
    """
    for line in block.splitlines():
        for segment in re.split(r"[｜|]", line):
            visible = re.sub(r"[`*_~]", "", segment).strip()
            visible = re.sub(r"^\s*(?:[-+]|\d+[.)])\s+", "", visible)
            visible = re.sub(
                r"^(?:研究锚定|research\s*anchor)\s*[:：]\s*",
                "",
                visible,
                flags=re.IGNORECASE,
            )
            match = label_pattern.match(visible)
            if match:
                return match.group(1).strip()
    return None


def _anchor_value_is_valid(
    value: str | None,
    value_pattern: re.Pattern[str],
    *,
    calendar_date: bool = False,
) -> bool:
    """Validate the leading value of an anchor field, not dates in annotations."""
    if value is None:
        return False
    visible = re.sub(r"[`*_~]", "", value).strip()
    if not visible or ANCHOR_VALUE_PLACEHOLDER_RE.search(visible):
        return False
    match = value_pattern.match(visible)
    if match is None:
        return False
    if calendar_date:
        date_match = re.search(r"\d{4}[-/]\d{1,2}[-/]\d{1,2}", match.group())
        if date_match is None:
            return False
        year, month, day = map(int, re.split(r"[-/]", date_match.group()))
        try:
            date(year, month, day)
        except ValueError:
            return False
    return True


def check_research_anchor_block(text: str, path: Path) -> list[str]:
    """Check that a Listed-Company report has a visible research-anchor block.

    Required: at least 2 of {FY reference, latest quarter, snapshot date/market
    data reference}.  The anchor block is the current-state lock that prevents
    stale-anchor drift (see ROUTING-MATRIX.md Listed Company hard-fail).

    Time-layer references are counted ONLY inside the visible anchor block.
    The anchor block may be either a heading section (``## 研究锚定块`` /
    ``Research anchor``) or the heading-less single-line form allowed by the
    report template (``研究锚定：最新FY：…｜最新季度：…｜市场快照：…``).  Keywords
    that only appear in other sections, the Source Register or body prose do
    not satisfy the gate (issue #436 D2).
    """
    block = _anchor_block_text(text)
    if block is None:
        return [
            f"{path}: Listed-Company report has no research-anchor block "
            "(expected a visible '## 研究锚定块' section or a single-line "
            "'研究锚定：…' anchor locking latest FY, latest quarter/interim and "
            "current market snapshot date)"
        ]

    field_rules = (
        (ANCHOR_FY_LABEL_RE, ANCHOR_FY_VALUE_RE, False),
        (ANCHOR_QUARTER_LABEL_RE, ANCHOR_QUARTER_VALUE_RE, False),
        (ANCHOR_SNAPSHOT_LABEL_RE, ANCHOR_SNAPSHOT_VALUE_RE, True),
    )
    hits = sum(
        _anchor_value_is_valid(
            _anchor_field_value(block, label), value, calendar_date=is_date
        )
        for label, value, is_date in field_rules
    )

    if hits < 2:
        return [
            f"{path}: research-anchor block only locks {hits}/3 required "
            "time-layer references (latest FY, latest quarter/interim, "
            "current market snapshot date); keywords outside the anchor block "
            "do not count"
        ]
    return []


def check_market_snapshot(text: str, path: Path) -> list[str]:
    """Check that a Listed-Company report's market snapshot has >=5 of 8 fields.

    The 8 fields correspond to the listed-company-report checklist template:
    share price, market cap, PE(TTM), PE(Forward), PB, PS, 52-week range,
    dividend yield.

    Returns errors (blocking): a missing market-snapshot section or fewer than
    5 filled fields is a delivery failure (issue #436), not a warning.  Only
    the value cell of each labeled field is counted; labels and source-column
    ids do not count as a filled value.
    """
    # Find the market snapshot section — look for heading patterns and scan
    # ONLY within that section.  The previous whole-document fallback let
    # reports satisfy the field count from keywords scattered elsewhere, so it
    # is removed (issue #436 D2): a missing snapshot section is reported
    # instead of being silently papered over.
    snapshot_heading = re.compile(
        r"(?:市场快照|market snapshot|financial snapshot|关键指标|key metrics)",
        re.IGNORECASE,
    )
    bounds = section_bounds(text, snapshot_heading)
    if bounds is None:
        return [
            f"{path}: Listed-Company report has no market-snapshot section "
            "(expected a visible section such as '## 市场快照' / "
            "'Market snapshot' with share price, market cap, PE(TTM/Forward), "
            "PB, PS, 52-week range, dividend yield)"
        ]
    start, end = bounds
    lines = text.splitlines()
    scan_lines = lines[start:end]

    # A field counts only when its *value cell* matches that metric's value
    # format. Parsing cells prevents the label itself (e.g. "52周区间" contains
    # digits) and the source column (e.g. "[S01]") from filling the metric.
    def _field_filled(
        label_pattern: re.Pattern[str],
        value_pattern: re.Pattern[str],
        require_currency: bool,
    ) -> bool:
        for ln in scan_lines:
            if "|" not in ln:
                continue
            cells = [c.strip() for c in ln.split("|")]
            for i, cell in enumerate(cells):
                if label_pattern.search(cell) and i + 1 < len(cells):
                    value = re.sub(r"[`*_~]", "", cells[i + 1]).strip()
                    if (
                        not value
                        or SNAPSHOT_PLACEHOLDER_RE.search(value)
                        or SNAPSHOT_DATE_PREFIX_RE.match(value)
                    ):
                        continue
                    if value_pattern.match(value) and (
                        not require_currency or SNAPSHOT_CURRENCY_MARKER_RE.search(value)
                    ):
                        return True
        return False

    matched = sum(
        _field_filled(label_pattern, value_pattern, require_currency)
        for label_pattern, value_pattern, require_currency in SNAPSHOT_FIELD_RULES
    )
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


def validate_file(
    path: Path, route_id: str | None = None
) -> tuple[list[str], list[str]]:
    """Run all Listed-Company delivery checks on a report file.

    Args:
        path: report markdown file.
        route_id: canonical route id already resolved by the orchestrator
            (e.g. ``"listed-company"``).  When supplied, the listed-company
            checks run iff this is the listed-company canonical id; the
            display-text re-guess is NOT used to decide whether to run
            (issue #436 D1).  When ``None`` (legacy/standalone callers that do
            not resolve the route), fall back to the display-text adapter.

    Returns (errors, warnings):
    - errors — blocking; must be fixed before delivery
    - warnings — non-blocking; quality signals
    """
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except (OSError, UnicodeError) as exc:
        return [f"{path}: cannot read file — {exc}"], []

    cleaned = sanitize_visible_markdown(text)

    # Route dispatch: trust the orchestrator-resolved canonical id.  Only when
    # no route id is supplied do we fall back to the legacy display-text guess.
    if route_id is None:
        route_id = "listed-company" if _is_listed_company(cleaned) else None
    if route_id != "listed-company":
        return [], []

    errors: list[str] = []
    warnings: list[str] = []

    # 1. Research-anchor block
    errors.extend(check_research_anchor_block(cleaned, path))

    # 2. Market snapshot completeness — a missing section or insufficient
    # fields is a hard failure (issue #436), not a warning that collapses to
    # conditional-pass.
    errors.extend(check_market_snapshot(cleaned, path))

    # 3. Strong wording scan
    e, w = check_strong_wording(cleaned, path)
    errors.extend(e)
    warnings.extend(w)

    # 4. Secondary route hard-fail verification
    warnings.extend(check_secondary_route_hard_fail(cleaned, path))

    return errors, warnings


# ── CLI entry point ──────────────────────────────────────────────────────────


def _resolve_route_id(path: Path) -> tuple[str | None, str | None]:
    """Resolve the report's declared primary route to a canonical route id.

    Standalone CLI adapter (issue #436 D1): extract the declared primary route
    name and resolve it through the route manifest, so that canonical forms such
    as ``listed-company`` are trusted instead of re-guessed from display text.

    Returns ``(canonical_id, error)``:
    - ``(None, "…")`` when no primary route is declared or it cannot be
      resolved — the CLI must fail closed instead of silently passing;
    - ``(canon, None)`` on success (canon may be a non-listed route, in which
      case ``validate_file`` skips the listed-company checks).
    """
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except (OSError, UnicodeError) as exc:
        return None, f"cannot read file — {exc}"
    cleaned = sanitize_visible_markdown(text)
    raw = get_route_name(cleaned)
    if not raw:
        return None, "no primary route declared in the report"
    try:
        canonical = registry_loader.load_route_registry().resolve_route(raw)
    except UnknownRouteError as exc:
        return None, f"declared primary route '{raw}' cannot be resolved — {exc}"
    except RegistryError as exc:
        return None, f"route registry is invalid — {exc}"
    return canonical, None


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
        # Resolve the declared route once so canonical 'listed-company' runs the
        # dedicated checks instead of being silently skipped.  A missing or
        # unresolvable route is a blocking failure, not a silent pass
        # (issue #436 D1).
        route_id, route_err = _resolve_route_id(path)
        if route_err is not None:
            all_errors.append(f"{path}: {route_err}")
            continue
        errors, warnings = validate_file(path, route_id=route_id)
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
