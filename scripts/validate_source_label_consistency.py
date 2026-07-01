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
CAVEAT_RE = re.compile(
    r"(?:（来源：厂商自述，非独立验证）|\(来源：厂商自述，非独立验证\))"
)

# Filed-data aggregators cited with confirmed labels need both:
# 1) source-role language (aggregated / non-original / filed-data platform), and
# 2) metric or snapshot basis (date, TTM/FY,口径). A bare "TTM" is not enough.
FILED_DATA_AGGREGATOR_ROLE_RE = re.compile(
    r"(?:filed data|filed-data|aggregator|aggregated|聚合数据|非原始披露)",
    re.IGNORECASE,
)
FILED_DATA_AGGREGATOR_BASIS_RE = re.compile(
    r"(?:快照日期|snapshot date|TTM|fiscal year|口径|metric basis)",
    re.IGNORECASE,
)

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

# Financial data platforms that re-present filed/regulatory data. These are not
# primary filings, but may support financial snapshots when cited with an inline
# source-role / metric-basis caveat.
_FILED_DATA_AGGREGATOR_TYPES: frozenset[str] = frozenset({
    "FILED_DATA_AGGREGATOR",
})

# Portals/compilations mixing analyst estimates, market data, news, and/or auto
# aggregation. Treat as secondary-like for confirmed-label checks.
_ANALYST_PORTAL_COMPILATION_TYPES: frozenset[str] = frozenset({
    "ANALYST_PORTAL_COMPILATION",
})

# Primary company source types that need a self-reporting caveat.
_PRIMARY_COMPANY_TYPES: frozenset[str] = frozenset({
    "PRIMARY_COMPANY",
    "PRIMARY_PARTNER",
    "PRIMARY",  # simplified 5-class system
})

# Primary institution / agency / multilateral source types.
# These are authoritative public sources (not company self-report),
# so they do NOT need a vendor self-reporting caveat.
_PRIMARY_INSTITUTION_TYPES: frozenset[str] = frozenset({
    "PRIMARY_INSTITUTION",
})

# Crowdsourced / tertiary source types. These must NOT use confirmed labels.
_CROWDSOURCED_TYPES: frozenset[str] = frozenset({
    "CROWDSOURCED",
})

# Unconfirmed / rumor / leak source types. These must NOT use confirmed labels.
# Note: UNCONFIRMED is already in _KNOWN_OTHER_TYPES; the dedicated frozenset
# allows the elif chain to catch it before _is_unknown_type.
_UNCONFIRMED_TYPES: frozenset[str] = frozenset({
    "UNCONFIRMED",
})

# Free-text source type to canonical type mapping (Chinese + common English aliases).
# Used by _normalize_source_type() to map free-text source types
# (common in technical reports) to the canonical types that the validator checks.
# Parenthetical variants (e.g., "学术综述（arXiv）") are handled by stripping
# parenthetical content before lookup.
#
# The standard canonical types are listed in §Source type classification of
# references/source-traceability-and-claim-citation.md.
_FREETEXT_TYPE_MAP: dict[str, str] = {
    # Academic / literature
    "原始论文": "PRIMARY_FILING",
    "peer-reviewed paper": "PRIMARY_FILING",
    "学术综述": "SECONDARY_MEDIA",
    "arxiv preprint": "SECONDARY_MEDIA",
    # Official / vendor
    "官方技术文档": "PRIMARY_DEV",
    "框架文档": "PRIMARY_DEV",
    "官方文档": "PRIMARY_COMPANY",
    "技术白皮书": "PRIMARY_DEV",
    "白皮书": "PRIMARY_DEV",
    "产品文档": "PRIMARY_COMPANY",
    "API文档": "PRIMARY_DEV",
    "api 文档": "PRIMARY_DEV",
    "公司公告": "PRIMARY_COMPANY",
    "招股书": "PRIMARY_FILING",
    "招股说明书": "PRIMARY_FILING",
    "年报": "PRIMARY_FILING",
    "年度报告": "PRIMARY_FILING",
    # Financial filed-data aggregators
    "reuters lseg filed data": "FILED_DATA_AGGREGATOR",
    "lseg filed data": "FILED_DATA_AGGREGATOR",
    "reuters filed data": "FILED_DATA_AGGREGATOR",
    "bloomberg filed data": "FILED_DATA_AGGREGATOR",
    "wind filed data": "FILED_DATA_AGGREGATOR",
    "choice filed data": "FILED_DATA_AGGREGATOR",
    "东方财富 choice api filed data": "FILED_DATA_AGGREGATOR",
    "stockanalysis filed data": "FILED_DATA_AGGREGATOR",
    "macrotrends filed data": "FILED_DATA_AGGREGATOR",
    "filed data aggregator": "FILED_DATA_AGGREGATOR",
    "聚合数据": "FILED_DATA_AGGREGATOR",
    "财务聚合数据": "FILED_DATA_AGGREGATOR",
    # Analyst/market/news portal compilations
    "finviz": "ANALYST_PORTAL_COMPILATION",
    "seeking alpha": "ANALYST_PORTAL_COMPILATION",
    "yahoo finance": "ANALYST_PORTAL_COMPILATION",
    "analyst portal compilation": "ANALYST_PORTAL_COMPILATION",
    "金融门户": "ANALYST_PORTAL_COMPILATION",
    # Blog / media
    "技术博客": "SECONDARY_MEDIA",
    "官方博客": "PRIMARY_COMPANY",
    "官方技术博客": "PRIMARY_COMPANY",
    "行业研究报告": "SECONDARY_ANALYST",
    "新闻报道": "SECONDARY_MEDIA",
    "新闻": "SECONDARY_MEDIA",
    "券商研报": "SECONDARY_ANALYST",
    "研报": "SECONDARY_ANALYST",
    # Community / weak signal
    "社区技术文章": "WEAK_SIGNAL",
    "博客园": "WEAK_SIGNAL",
    "CSDN": "WEAK_SIGNAL",
    "社区文章": "WEAK_SIGNAL",
    "知乎": "WEAK_SIGNAL",
    "Reddit": "WEAK_SIGNAL",
    "微信公众号": "WEAK_SIGNAL",
    "公众号": "WEAK_SIGNAL",
    # Transcript
    "专家访谈": "TRANSCRIPT",
    "访谈": "TRANSCRIPT",
    "财报电话会": "TRANSCRIPT",
    # Inference
    "技术分析": "INFERRED",
    "多来源综合": "INFERRED",
    # Multilateral / government / agency → PRIMARY_INSTITUTION
    "primary (multilateral)": "PRIMARY_INSTITUTION",
    "primary (multilateral report)": "PRIMARY_INSTITUTION",
    "primary (multilateral analysis)": "PRIMARY_INSTITUTION",
    "primary (us govt agency)": "PRIMARY_INSTITUTION",
    "primary (government agency)": "PRIMARY_INSTITUTION",
    "government agency": "PRIMARY_INSTITUTION",
    "regulator": "PRIMARY_INSTITUTION",
    "public agency": "PRIMARY_INSTITUTION",
    # Vendor claim → PRIMARY_COMPANY (统一处理 caveat)
    "primary (vendor)": "PRIMARY_COMPANY",
    # Crowdsourced / tertiary → CROWDSOURCED
    "secondary (crowdsourced)": "CROWDSOURCED",
    "crowdsourced": "CROWDSOURCED",
    "wikipedia": "CROWDSOURCED",
    "wiki": "CROWDSOURCED",
    # Rumor / leak → UNCONFIRMED
    "rumor": "UNCONFIRMED",
    "leak": "UNCONFIRMED",
    "传闻": "UNCONFIRMED",
    "unconfirmed": "UNCONFIRMED",
}

# Case-insensitive lookup map built from _FREETEXT_TYPE_MAP.
# Keys are lowercased; values are the same canonical types.
_FREETEXT_TYPE_MAP_CI: dict[str, str] = {
    k.lower(): v for k, v in _FREETEXT_TYPE_MAP.items()
}


def strip_fenced_code_blocks(text: str) -> str:
    """Replace content inside fenced code blocks with empty lines.

    Preserves original line count so that any line-number reporting
    in the caller maps back to the original file.
    """
    lines = text.splitlines()
    result = list(lines)  # start with a copy
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


def _is_type_in(source_type: str, type_set: frozenset[str]) -> bool:
    """Check if a normalized source type belongs to a given frozenset."""
    return source_type.strip().upper() in type_set


def _is_secondary_type(source_type: str) -> bool:
    """Check if a source type is secondary (granular or simplified)."""
    return _is_type_in(source_type, _SECONDARY_TYPES)


def _is_primary_company_type(source_type: str) -> bool:
    """Check if a source type is a primary company (needs caveat)."""
    return _is_type_in(source_type, _PRIMARY_COMPANY_TYPES)


def _is_institution_type(source_type: str) -> bool:
    """Check if a source type is a primary institution/agency (no caveat)."""
    return _is_type_in(source_type, _PRIMARY_INSTITUTION_TYPES)


def _is_crowdsourced_type(source_type: str) -> bool:
    """Check if a source type is crowdsourced/tertiary (no confirmed label)."""
    return _is_type_in(source_type, _CROWDSOURCED_TYPES)


def _is_unconfirmed_type(source_type: str) -> bool:
    """Check if a source type is unconfirmed/rumor (no confirmed label)."""
    return _is_type_in(source_type, _UNCONFIRMED_TYPES)


def _is_filed_data_aggregator_type(source_type: str) -> bool:
    """Check if a source type is a filed/regulatory data aggregator."""
    return _is_type_in(source_type, _FILED_DATA_AGGREGATOR_TYPES)


def _is_analyst_portal_compilation_type(source_type: str) -> bool:
    """Check if a source type is an analyst/market/news portal compilation."""
    return _is_type_in(source_type, _ANALYST_PORTAL_COMPILATION_TYPES)


def _has_filed_data_aggregator_caveat(sentence: str) -> bool:
    """Return True when sentence has both source-role and metric-basis notes."""
    return bool(
        FILED_DATA_AGGREGATOR_ROLE_RE.search(sentence)
        and FILED_DATA_AGGREGATOR_BASIS_RE.search(sentence)
    )


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
        chunks = re.split(r"(?<=[。！？!?；;．.])\s+", line)
        for chunk in chunks:
            chunk = chunk.strip()
            if chunk:
                results.append(chunk)
    return results


def _normalize_source_type(source_type: str) -> str:
    """Normalize a source type string for canonical lookup.

    Steps:
    1. Strip leading/trailing whitespace
    2. Case-insensitive lookup in _FREETEXT_TYPE_MAP (complete string,
       including parenthetical content)
    3. If not found, strip parenthetical content: both CJK （arXiv） and
       half-width (arXiv), then try lookup again
    4. If still not found, return the stripped string for canonical type matching
       (e.g. \"PRIMARY\" for the simplified 5-class system)

    The two-pass lookup ensures parenthetical variants like
    \"Primary (multilateral)\" are matched before the parenthetical content
    is stripped (which would leave just \"Primary\", conflating it with
    the simplified 5-class PRIMARY).
    """
    # Pass 1: whole-string lookup (preserves parenthetical context)
    s = source_type.strip()
    lower = s.lower()
    if lower in _FREETEXT_TYPE_MAP_CI:
        return _FREETEXT_TYPE_MAP_CI[lower]

    # Pass 2: strip parenthetical content and retry.
    # Loop to handle potential nested parentheses (e.g. "Primary (multilateral (report))").
    # Each iteration strips one level; stops when no more parentheses remain.
    while True:
        stripped = re.sub(r'[（(][^）)]*[）)]|\([^)]*\)', '', s).strip()
        if stripped == s:
            break
        s = stripped
    lower = s.lower()
    if lower in _FREETEXT_TYPE_MAP_CI:
        return _FREETEXT_TYPE_MAP_CI[lower]

    return s  # Return sanitized string for canonical type matching


def _is_unknown_type(source_type: str) -> bool:
    """Check if a normalized source type is unknown (not in any recognized set).

    Returns True if the type is not secondary, not primary-company, and not a
    recognized exempt type (PRIMARY_FILING, PRIMARY_DEV, INFERRED, UNCONFIRMED,
    WEAK_SIGNAL, TRANSCRIPT, FILED_DATA_AGGREGATOR,
    ANALYST_PORTAL_COMPILATION).

    Note: _is_secondary_type and _is_primary_company_type are checked first
    by the caller (check_source_consistency's elif chain). The checks here
    are defensive redundancy — they guarantee correct behavior even if
    _is_unknown_type were called directly.
    """
    upper = source_type.strip().upper()
    # Known non-company types that don't need additional checks.
    # Note: PRIMARY is not here because it's handled by _is_primary_company_type
    # (it's the simplified 5-class equivalent).
    _KNOWN_OTHER_TYPES: frozenset[str] = frozenset({
        "PRIMARY_FILING", "PRIMARY_DEV", "INFERRED",
        "UNCONFIRMED", "WEAK_SIGNAL", "TRANSCRIPT",
        "PRIMARY_INSTITUTION", "CROWDSOURCED",
        "FILED_DATA_AGGREGATOR", "ANALYST_PORTAL_COMPILATION",
    })
    if _is_secondary_type(source_type):
        return False
    if _is_primary_company_type(source_type):
        return False
    if _is_filed_data_aggregator_type(source_type):
        return False
    if _is_analyst_portal_compilation_type(source_type):
        return False
    if upper in _KNOWN_OTHER_TYPES:
        return False
    return True


def check_source_consistency(text: str, strict: bool = False) -> list[str]:
    """Check label/source type consistency. Returns list of error messages.

    Checks (applied in order):
    1. Secondary sources must not be referenced with confirmed labels.
    2. Primary institution/agency sources pass through (no caveat needed).
    3. Primary company sources must have a self-reporting caveat nearby.
    4. Crowdsourced/tertiary sources must not be referenced with confirmed labels.
    5. Unconfirmed/rumor/leak sources must not be referenced with confirmed labels.
    6. Analyst portal compilations must not be referenced with confirmed labels.
    7. Filed-data aggregators require a same-sentence caveat when referenced
       with confirmed labels.
    8. Unknown source types generate a warning (or error in strict mode).

    When strict=True, unknown source types cause errors (not just warnings).
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

        # Normalize Chinese technical source types to canonical types
        norm_type = _normalize_source_type(source_type)

        ref_re = _source_ref_re(source_id)

        if _is_secondary_type(norm_type):
            # Check 1: Secondary source should not have confirmed label nearby.
            for sent in sentences:
                if not ref_re.search(sent):
                    continue
                if CONFIRMED_LABEL_RE.search(sent):
                    errors.append(
                        f"source {source_id} ({source_type}) is secondary "
                        f"but referenced with confirmed label: {sent[:100]}"
                    )

        elif _is_institution_type(norm_type):
            # Check 2: Primary institution/agency source — pass through.
            # These are authoritative public sources (multilateral, government,
            # regulator, agency). No caveat needed; no confirmed-label restriction.
            pass

        elif _is_primary_company_type(norm_type):
            # Check 3: Primary company source needs self-reporting caveat.
            for sent in sentences:
                if not ref_re.search(sent):
                    continue
                if not CAVEAT_RE.search(sent):
                    errors.append(
                        f"source {source_id} ({source_type}) is a primary "
                        f"company source but lacks self-reporting caveat: "
                        f"{sent[:100]}"
                    )

        elif _is_crowdsourced_type(norm_type):
            # Check 4: Crowdsourced/tertiary source must not use confirmed label.
            for sent in sentences:
                if not ref_re.search(sent):
                    continue
                if CONFIRMED_LABEL_RE.search(sent):
                    errors.append(
                        f"source {source_id} ({source_type}) is crowdsourced "
                        f"but referenced with confirmed label: {sent[:100]}"
                    )

        elif _is_unconfirmed_type(norm_type):
            # Check 5: Unconfirmed/rumor/leak source must not use confirmed label.
            for sent in sentences:
                if not ref_re.search(sent):
                    continue
                if CONFIRMED_LABEL_RE.search(sent):
                    errors.append(
                        f"source {source_id} ({source_type}) is unconfirmed "
                        f"but referenced with confirmed label: {sent[:100]}"
                    )

        elif _is_analyst_portal_compilation_type(norm_type):
            # Check 6: Analyst/market/news portal compilations are secondary-like.
            for sent in sentences:
                if not ref_re.search(sent):
                    continue
                if CONFIRMED_LABEL_RE.search(sent):
                    errors.append(
                        f"source {source_id} ({source_type}) is an analyst "
                        f"portal compilation but referenced with confirmed "
                        f"label: {sent[:100]}"
                    )

        elif _is_filed_data_aggregator_type(norm_type):
            # Check 7: Filed-data aggregators can support confirmed snapshots only
            # when the same sentence marks source role or metric/snapshot basis.
            for sent in sentences:
                if not ref_re.search(sent):
                    continue
                has_confirmed_label = CONFIRMED_LABEL_RE.search(sent)
                if (
                    has_confirmed_label
                    and not _has_filed_data_aggregator_caveat(sent)
                ):
                    errors.append(
                        f"source {source_id} ({source_type}) is a filed-data "
                        f"aggregator with confirmed label but lacks same-sentence "
                        f"filed-data/aggregation/snapshot/metric-basis caveat: "
                        f"{sent[:100]}"
                    )

        elif _is_unknown_type(norm_type):
            # Check 8: Unknown source type detection.
            msg = (
                f"source {source_id} has unrecognized source type "
                f"'{source_type}': map to a canonical type or correct the entry"
            )
            if strict:
                errors.append(msg)
            else:
                print(f"warning: {msg}", file=sys.stderr)

    return errors


def validate_file(path: Path, strict: bool = False) -> list[str]:
    """Validate all source label consistency rules in *path*."""
    raw = path.read_text(encoding="utf-8", errors="replace")
    return check_source_consistency(raw, strict=strict)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Lint Source Register label consistency in Markdown reports."
        )
    )
    parser.add_argument("paths", nargs="+", help="Markdown files to validate")
    parser.add_argument("--strict", action="store_true",
                        help="Fail on unknown source types (default: warn only)")
    args = parser.parse_args(argv)

    errors: list[str] = []
    for raw_path in args.paths:
        path = Path(raw_path)
        if not path.exists():
            errors.append(f"{path}: file not found")
            continue
        errors.extend(validate_file(path, strict=args.strict))

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
