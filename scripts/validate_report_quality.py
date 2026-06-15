#!/usr/bin/env python3
"""Validate final report quality against minimum delivery contracts.

Checks whether the final report meets the structural and traceability
requirements defined in references/report-template.md:

- Route and audit status block exists (§8)
- Route declaration present (Primary route or Shared-workflow)
- Audit table passed rows have meaningful evidence (not empty/vague)
- Source Register exists (§9) with 7-column header
- Body contains [Sxx] or functionally equivalent inline citations
- --strict mode adds route-specific warnings
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


EXIT_PASS = 0
EXIT_STRUCTURE = 2

# ── Regex patterns ────────────────────────────────────────────────────────

FENCE_RE = re.compile(r"^[ ]{0,3}(`{3,}|~{3,})")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
TABLE_ROW_RE = re.compile(r"^\s*\|.*\|\s*$")
TABLE_DELIMITER_RE = re.compile(
    r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$"
)

ROUTE_AUDIT_HEADING = re.compile(r"Route\s+and\s+audit\s+status", re.IGNORECASE)
SOURCE_REGISTER_HEADING = re.compile(r"Source\s+Register", re.IGNORECASE)
PRIMARY_ROUTE_RE = re.compile(r"\*\*Primary\s+route\*\*", re.IGNORECASE)
SHARED_WORKFLOW_RE = re.compile(
    r"\*\*Route\*\*.*[Ss]hared[- ]?[Ww]orkflow"
)

AUDIT_PASSED_RE = re.compile(r"(✅\s*)?(Passed|已通过|通过)", re.IGNORECASE)
VAGUE_EVIDENCE_RE = re.compile(
    r"^(通过|已检查|N/A|n/a|ok|OK|已通过|是|yes|Yes|YES)?\s*$"
)

AUDIT_COL_RE = re.compile(r"Audit|审计|检查项", re.IGNORECASE)
STATUS_COL_RE = re.compile(r"Status|状态|结果", re.IGNORECASE)
EVIDENCE_COL_RE = re.compile(r"证据|Evidence|Proof|执行证据", re.IGNORECASE)

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

# ── Placeholder patterns (for Source Register DOI/URL column) ─────────────
# Detects common placeholder values that indicate unresolved entries.
PLACEHOLDER_RE = re.compile(
    r"^[\s\-—–—]*$"         # whitespace-only, dashes, em-dashes, en-dashes
    r"|TBD"                  # TBD (case-sensitive, avoids 'tbd' suffix)
    r"|tbd"                  # lowercase tbd
    r"|T\.B\.D\."            # T.B.D. dotted form
    r"|xxxxx"                # placeholder xxxxx
    r"|arXiv:\d{4}\.xxxxx"   # arXiv placeholder pattern
    r"|—|–"      # HTML entities for em-dash / en-dash
)

# ── Academic 11-column Source Register header patterns ────────────────────
ACADEMIC_EXTRA_COLUMNS = [
    "Publication Type", "Peer-review Status", "Venue", "Venue Prestige",
]

# ── Key section patterns (for section-level citation coverage check) ──────

KEY_SECTION_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"(?:执行\s*摘要|Executive\s*Summary)", re.IGNORECASE),
    re.compile(r"(?:综合\s*结论|^结论$|Conclusion\s*$)", re.IGNORECASE),
    re.compile(r"(?:维度\s*结论|维度\s*评估|Dimension\s+Conclusion)", re.IGNORECASE),
    re.compile(r"(?:推荐\s*排序|推荐\s*建议|Recommendation)", re.IGNORECASE),
]

# Role-label patterns (for quantitative-role self-assessment check)
ROLE_HEADER_RE = re.compile(
    r"(?:数字角色|number role|role|epistemic role)", re.IGNORECASE
)
ROLE_VALUE_RE = re.compile(
    r"(?:\b[OPAM]\b|observed|proxy|assumption|model\s*output|estimate|"
    r"scenario|inferred|illustrative)",
    re.IGNORECASE,
)

ROUTE_IN_BLOCK = re.compile(
    r"\*\*(?:Primary\s+)?route\*\*", re.IGNORECASE
)

# ── Helpers ───────────────────────────────────────────────────────────────


def strip_fenced_code_blocks(text: str) -> str:
    lines = text.splitlines()
    out: list[str] = []
    in_fence = False
    fence_char = ""
    fence_len = 0
    fence_opener: str | None = None  # line content of unclosed fence opener

    for line in lines:
        stripped = line.rstrip()
        if not in_fence:
            m = FENCE_RE.match(stripped)
            if m:
                fence_char = m.group(1)[0]
                fence_len = len(m.group(1))
                in_fence = True
                fence_opener = line
                continue
            out.append(line)
            continue
        # Build closing pattern once per fence block, not per line
        closing_re = re.compile(
            r"^[ ]{0,3}"
            + re.escape(fence_char)
            + "{"
            + str(fence_len)
            + r",}\s*$"
        )
        if closing_re.match(stripped):
            in_fence = False
            fence_opener = None

    # If fence never closed, put the opener back to avoid silent content loss
    if fence_opener is not None:
        out.append(fence_opener)

    return "\n".join(out)


def section_bounds(
    text: str, heading_pattern: re.Pattern[str]
) -> tuple[int, int] | None:
    lines = text.splitlines()
    start = None
    start_level = None
    for i, line in enumerate(lines):
        m = HEADING_RE.match(line.rstrip())
        if m and heading_pattern.search(m.group(2)):
            start = i
            start_level = len(m.group(1))
            break
    if start is None:
        return None
    end = len(lines)
    for i in range(start + 1, len(lines)):
        m = HEADING_RE.match(lines[i].rstrip())
        if m and len(m.group(1)) <= start_level:
            end = i
            break
    return start, end


def section_text(text: str, heading_pattern: re.Pattern[str]) -> str | None:
    bounds = section_bounds(text, heading_pattern)
    if bounds is None:
        return None
    start, end = bounds
    lines = text.splitlines()
    return "\n".join(lines[start:end])


def body_text(text: str) -> str:
    """Return text outside all ## headings."""
    lines = text.splitlines()
    out: list[str] = []
    for line in lines:
        m = HEADING_RE.match(line.rstrip())
        if m and len(m.group(1)) <= 2:
            continue
        out.append(line)
    return "\n".join(out)


def parse_table(text: str) -> list[list[str]] | None:
    """Parse first markdown table from text.

    Returns list of rows (each row = list of cell strings).
    First row is the header.  Returns None if no table found.
    Handles escaped pipes (\\|) inside cells by masking them before splitting.
    """
    lines = text.splitlines()
    rows: list[list[str]] = []
    state = "before_header"
    # Sentinel to protect escaped pipes from splitting
    PIPE_SENTINEL = "\x00PIPE\x00"

    for line in lines:
        stripped = line.rstrip()
        if not TABLE_ROW_RE.match(stripped):
            if state == "after_delimiter" and rows:
                break
            continue
        if TABLE_DELIMITER_RE.match(stripped):
            if state == "before_header":
                # Delimiter before any header — invalid, skip
                continue
            if state == "after_header":
                state = "after_delimiter"
            continue
        # Protect escaped pipes before splitting, restore after
        guarded = stripped.replace("\\|", PIPE_SENTINEL)
        cells = [
            c.strip().replace(PIPE_SENTINEL, "|")
            for c in guarded.strip("|").split("|")
        ]
        if state == "before_header":
            rows.append(cells)
            state = "after_header"
        elif state == "after_delimiter":
            rows.append(cells)
        elif state == "after_header":
            # No delimiter found, treat as another header row
            # (malformed table, but try to continue)
            rows.append(cells)

    if len(rows) < 2:  # need at least header + 1 data row
        return None
    return rows


def find_col_index(header: list[str], patterns: list[re.Pattern[str]]) -> int:
    """Find column index matching any of the patterns, or -1."""
    for i, cell in enumerate(header):
        for pat in patterns:
            if pat.search(cell):
                return i
    return -1


# ── Route and audit status checks ─────────────────────────────────────────


def check_route_audit_block(cleaned: str) -> list[str]:
    """Verify ## Route and audit status block exists."""
    if section_bounds(cleaned, ROUTE_AUDIT_HEADING) is None:
        return ["Missing '## Route and audit status' section"]
    return []


def check_route_declaration(cleaned: str) -> list[str]:
    """Verify route declaration present (Primary route / Shared-workflow)."""
    sec = section_text(cleaned, ROUTE_AUDIT_HEADING)
    if sec is None:
        return []
    if PRIMARY_ROUTE_RE.search(sec) or SHARED_WORKFLOW_RE.search(sec):
        return []
    # Check for any **route** pattern as fallback
    if ROUTE_IN_BLOCK.search(sec):
        return []
    return [
        "No route declaration found: expected '**Primary route**' or "
        "'**Route**: Shared-workflow' in the audit status section"
    ]


def check_audit_evidence(cleaned: str) -> list[str]:
    """Verify passed audit rows have non-vague evidence."""
    sec = section_text(cleaned, ROUTE_AUDIT_HEADING)
    if sec is None:
        return []
    table = parse_table(sec)
    if table is None:
        return ["No table found in Route and audit status section"]

    header = table[0]
    audit_idx = find_col_index(header, [AUDIT_COL_RE])
    status_idx = find_col_index(header, [STATUS_COL_RE])
    evidence_idx = find_col_index(header, [EVIDENCE_COL_RE])

    if any(i == -1 for i in (audit_idx, status_idx)):
        return [
            "Audit table must have at least 'Audit' and 'Status' columns"
        ]
    if evidence_idx == -1:
        return [
            "Audit table must have an evidence column "
            "(证据 / Evidence / Proof)"
        ]

    issues: list[str] = []
    for row in table[1:]:
        if len(row) <= max(audit_idx, status_idx, evidence_idx):
            continue
        status_val = row[status_idx].strip()
        if not AUDIT_PASSED_RE.match(status_val):
            continue
        evidence_val = row[evidence_idx].strip()
        if not evidence_val or VAGUE_EVIDENCE_RE.match(evidence_val):
            audit_name = row[audit_idx].strip().split("\n")[0][:60]
            issues.append(
                f"Passed audit '{audit_name}' has vague evidence: "
                f"'{evidence_val or '(empty)'}'"
            )

    return issues


# ── Source Register checks ────────────────────────────────────────────────


def check_source_register_exists(cleaned: str) -> list[str]:
    """Verify ## Source Register section exists."""
    if section_bounds(cleaned, SOURCE_REGISTER_HEADING) is None:
        return ["Missing '## Source Register' section"]
    return []


def check_source_register_columns(cleaned: str) -> list[str]:
    """Verify Source Register table has 7-column header."""
    sec = section_text(cleaned, SOURCE_REGISTER_HEADING)
    if sec is None:
        return []
    table = parse_table(sec)
    if table is None:
        return ["No table found in Source Register section"]
    header = table[0]
    if len(header) < 7:
        return [
            f"Source Register table has {len(header)} column(s), "
            f"expected at least 7 "
            f"(ID / Source Name / Source Type / Date / DOI/URL / "
            f"Reliability / Claims Supported)"
        ]
    return []


def check_source_register_missing_ids(cleaned: str) -> list[str]:
    """Verify every Source Register entry has a non-empty ID.

    Entries without an ID cannot be body-referenced, breaking traceability.
    Returns error list (non-empty → hard fail).
    """
    sec = section_text(cleaned, SOURCE_REGISTER_HEADING)
    if sec is None:
        return []
    table = parse_table(sec)
    if table is None or len(table) < 2:
        return []

    header = table[0]
    data_rows = table[1:]

    id_col = find_col_index(header, [re.compile(r'\bID\b', re.IGNORECASE)])
    if id_col == -1:
        return []  # No ID column found (caught by column check already)

    missing: list[int] = []
    for i, row in enumerate(data_rows, start=2):  # +2 for 0-index + header + delimiter
        if len(row) <= id_col:
            missing.append(i)
            continue
        id_val = row[id_col].strip()
        if not id_val or id_val == "-":
            missing.append(i)

    if missing:
        line_nums = ", ".join(str(l) for l in missing[:5])
        if len(missing) > 5:
            line_nums += ", ..."
        return [
            f"Source Register has {len(missing)} entry/entries with missing ID "
            f"(table rows {line_nums})"
        ]
    return []


def check_source_register_doi_coverage(cleaned: str) -> list[str]:
    """Warn if >50% of Source Register entries lack DOI/URL.

    Missing DOI/URL reduces verifiability; warn but do not hard-block.
    Returns warning list (non-empty → warning only).
    """
    sec = section_text(cleaned, SOURCE_REGISTER_HEADING)
    if sec is None:
        return []
    table = parse_table(sec)
    if table is None or len(table) < 2:
        return []

    header = table[0]
    data_rows = table[1:]

    doi_col = find_col_index(header, [re.compile(r"DOI\s*/\s*URL", re.IGNORECASE)])
    if doi_col == -1:
        return []

    empty_count = 0
    for row in data_rows:
        if len(row) <= doi_col:
            empty_count += 1
            continue
        doi_val = row[doi_col].strip()
        if not doi_val or doi_val == "-":
            empty_count += 1

    if data_rows and empty_count / len(data_rows) > 0.5:
        return [
            f"Source Register: {empty_count}/{len(data_rows)} entries "
            f"({empty_count/len(data_rows):.0%}) lack DOI/URL"
        ]
    return []


def check_source_register_mapping(cleaned: str) -> list[str]:
    """Cross-compare body [Sxx] IDs against register ID column.

    Body references to IDs not present in the register are mapping errors.
    This catches structural mapping failures where the body cites a source
    ID that does not exist in the Source Register.
    Returns error list (non-empty → hard fail).
    """
    sec = section_text(cleaned, SOURCE_REGISTER_HEADING)
    if sec is None:
        return []
    table = parse_table(sec)
    if table is None or len(table) < 2:
        return []

    header = table[0]
    data_rows = table[1:]

    id_col = find_col_index(header, [re.compile(r"\bID\b", re.IGNORECASE)])
    if id_col == -1:
        return []

    register_ids: set[str] = set()
    for row in data_rows:
        if len(row) > id_col:
            val = row[id_col].strip()
            if val:
                register_ids.add(val)

    body = body_before_source_register(cleaned)
    body_ids = set(BODY_SXX_RE.findall(body))  # e.g. {"[S01]", "[S05]"}
    body_id_values = {ref.strip("[]") for ref in body_ids}

    missing = sorted(body_id_values - register_ids)
    if missing:
        preview = ", ".join(missing[:10])
        if len(missing) > 10:
            preview += ", ..."
        return [
            f"Body references source ID(s) {preview} "
            f"not found in Source Register"
        ]
    return []


def check_source_register_placeholders(cleaned: str) -> list[str]:
    """Detect placeholder values in Source Register DOI/URL column.

    Checks for —, TBD, xxxxx, arXiv:xxxxx, and other patterns that
    indicate unresolved entries.
    Returns warning list (non-empty → warning only).
    """
    sec = section_text(cleaned, SOURCE_REGISTER_HEADING)
    if sec is None:
        return []
    table = parse_table(sec)
    if table is None or len(table) < 2:
        return []

    header = table[0]
    data_rows = table[1:]

    doi_col = find_col_index(header, [re.compile(r"DOI\s*/\s*URL", re.IGNORECASE)])
    if doi_col == -1:
        return []

    found: list[str] = []
    for i, row in enumerate(data_rows, start=2):
        if len(row) <= doi_col:
            continue
        val = row[doi_col].strip()
        if not val:
            continue  # empty handled by DOI coverage check
        if PLACEHOLDER_RE.search(val):
            if len(found) < 5:
                found.append(f"row {i}: '{val}'")
            else:
                found.append("...")
                break

    if not found:
        return []

    return [
        f"Source Register: {len(found)} entry/entries with placeholder "
        f"DOI/URL — {', '.join(found)}. "
        f"Resolve to real DOI/URL or annotate as unavailable."
    ]


def check_source_register_duplicate_ids(cleaned: str) -> list[str]:
    """Check for duplicate IDs in Source Register.

    Duplicate IDs corrupt traceability — a body [Sxx] reference cannot
    unambiguously identify a single source.
    Returns error list (non-empty → hard fail).
    """
    sec = section_text(cleaned, SOURCE_REGISTER_HEADING)
    if sec is None:
        return []
    table = parse_table(sec)
    if table is None or len(table) < 2:
        return []

    header = table[0]
    data_rows = table[1:]

    id_col = find_col_index(header, [re.compile(r"\bID\b", re.IGNORECASE)])
    if id_col == -1:
        return []

    seen: dict[str, int] = {}
    duplicates: list[str] = []
    for i, row in enumerate(data_rows, start=2):
        if len(row) <= id_col:
            continue
        id_val = row[id_col].strip()
        if not id_val or id_val == "-":
            continue
        if id_val in seen:
            duplicates.append(f"'{id_val}' (rows {seen[id_val]} and {i})")
        seen[id_val] = i

    if duplicates:
        preview = "; ".join(duplicates[:5])
        if len(duplicates) > 5:
            preview += "; ..."
        return [
            f"Source Register has duplicate ID(s): {preview}"
        ]
    return []


# ── Body reference checks ────────────────────────────────────────────────


def body_before_source_register(text: str) -> str:
    """Return body text excluding content under ## Source Register.

    Uses body_text() on the portion before the Source Register heading,
    so [Sxx] refs inside Source Register tables are not counted as body refs.
    """
    lines = text.splitlines()
    register_at: int | None = None
    for i, line in enumerate(lines):
        m = HEADING_RE.match(line.rstrip())
        if m and len(m.group(1)) <= 2 and SOURCE_REGISTER_HEADING.search(m.group(2)):
            register_at = i
            break
    if register_at is None:
        return body_text(text)
    # Process only lines before Source Register
    return body_text("\n".join(lines[:register_at]))


def check_body_references(cleaned: str) -> list[str]:
    """Verify body contains [Sxx] or functionally equivalent citations.

    Format equivalence exemptions (per source-traceability-and-claim-citation.md):
    - Author-Year: (Author, Year, Venue)
    - arXiv ID: arXiv:XXXX.XXXXX
    - DOI: doi:10.XXX/... or https://doi.org/10.XXX/...
    - Natural language unique attribution: 据 FY2025 年报, etc.

    NOTE: Source Register table content is excluded from body text so that
    [Sxx] references in the register's "Claims Supported" column do not
    produce false positives for the body-citation requirement.
    """
    body = body_before_source_register(cleaned)

    if BODY_SXX_RE.search(body):
        return []

    # Check format equivalence
    formats_found: list[str] = []
    if AUTHOR_YEAR_RE.search(body):
        formats_found.append("Author-Year")
    if ARXIV_RE.search(body):
        formats_found.append("arXiv ID")
    if DOI_RE.search(body):
        formats_found.append("DOI")
    if NL_ATTR_RE.search(body):
        formats_found.append("natural language attribution")

    if formats_found:
        return []

    return [
        "Body text has no [Sxx] citations or functionally equivalent "
        "format (Author-Year, arXiv ID, DOI, or unique natural language "
        "attribution)"
    ]


def _section_has_citation(text: str) -> bool:
    """Check if a text block has [Sxx] or equivalent inline citations.

    Uses the same format equivalence rules as check_body_references.
    """
    if BODY_SXX_RE.search(text):
        return True
    if AUTHOR_YEAR_RE.search(text):
        return True
    if ARXIV_RE.search(text):
        return True
    if DOI_RE.search(text):
        return True
    if NL_ATTR_RE.search(text):
        return True
    return False


def check_key_section_citation_coverage(cleaned: str) -> list[str]:
    """Check that key sections (exec summary, conclusion, etc.) have citations.

    A key section without any [Sxx] or equivalent inline citation is a
    traceability gap.  This is a hard fail because evidence-based reports
    must be auditable in every key section.

    Only checks sections at heading level <= 2 (## or #).
    Source Register section content is excluded — key sections within
    the register block are not scanned.
    Returns error list (non-empty → hard fail).
    """
    errors: list[str] = []

    # Build section boundaries: list of (heading_text, start_line, level)
    lines = cleaned.splitlines()
    sections: list[tuple[str, int, int]] = []
    for i, line in enumerate(lines):
        m = HEADING_RE.match(line.rstrip())
        if not m:
            continue
        level = len(m.group(1))
        if level > 2:
            continue  # only check major sections (h1/h2)
        heading_text = m.group(2)
        for pattern in KEY_SECTION_PATTERNS:
            if pattern.search(heading_text):
                sections.append((heading_text, i, level))
                break

    if not sections:
        return []  # no key sections found → nothing to check

    # Locate Source Register heading so we can exclude its content
    register_start: int | None = None
    for i, line in enumerate(lines):
        m = HEADING_RE.match(line.rstrip())
        if m and len(m.group(1)) <= 2 and SOURCE_REGISTER_HEADING.search(m.group(2)):
            register_start = i
            break

    for name, start, level in sections:
        # Find section end: next heading at same or higher level
        end = len(lines)
        for j in range(start + 1, len(lines)):
            m = HEADING_RE.match(lines[j].rstrip())
            if m and len(m.group(1)) <= level:
                end = j
                break

        # If section starts before the register, clip to register boundary
        # to avoid scanning register table content for body citations.
        if register_start is not None and start < register_start:
            end = min(end, register_start)

        body = "\n".join(lines[start + 1 : end]).strip()
        if not body:
            continue  # empty section body, skip

        if not _section_has_citation(body):
            errors.append(
                f"Key section '{name}' has no [Sxx] or equivalent "
                f"inline citations"
            )

    return errors


def get_route_name(cleaned: str) -> str | None:
    """Extract the declared route name, if any."""
    sec = section_text(cleaned, ROUTE_AUDIT_HEADING)
    if sec is None:
        return None
    m = re.search(r"\*\*Primary\s+route\*\*[:\s]+(.+)", sec)
    if m:
        return m.group(1).strip()
    m = re.search(r"\*\*Route\*\*[:\s]+(.+)", sec)
    if m:
        return m.group(1).strip()
    return None


def check_strict_warnings(cleaned: str) -> list[str]:
    """Additional warnings for --strict mode."""
    warnings: list[str] = []
    route = get_route_name(cleaned)
    if route:
        route_lower = route.lower()
        body = body_before_source_register(cleaned)

        if "academic" in route_lower or "literature" in route_lower:
            if not AUTHOR_YEAR_RE.search(body) and not BODY_SXX_RE.search(body):
                warnings.append(
                    f"Route '{route}': consider using (Author, Year) "
                    f"citations for academic traceability"
                )
        if "technical" in route_lower or "deep" in route_lower:
            if not ARXIV_RE.search(body) and not DOI_RE.search(body) and not BODY_SXX_RE.search(body):
                warnings.append(
                    f"Route '{route}': consider using arXiv ID or DOI "
                    f"for technical traceability"
                )
        if "listed" in route_lower or "investment" in route_lower or "memo" in route_lower:
            if not NL_ATTR_RE.search(body) and not BODY_SXX_RE.search(body):
                warnings.append(
                    f"Route '{route}': consider using named-source "
                    f"attribution (e.g., '据 FY2025 年报') for traceability"
                )
    return warnings


# ── Audit self-assessment consistency check ───────────────────────────────


def _split_cells(row: str) -> list[str]:
    """Split a markdown table row into individual cells, preserving escaped pipes."""
    guarded = row.replace("\\|", "\x00PIPE\x00")
    return [
        c.strip().replace("\x00PIPE\x00", "|")
        for c in guarded.strip("|").split("|")
    ]


def _body_has_role_labels(scan_text: str) -> bool:
    """Check if body tables have role labels (header column or cell values).

    Detection rules:
    1. Header row matches ROLE_HEADER_RE \u2192 table has role structure (C3: header only)
    2. Multi-word role value (observed/proxy/assumption etc.) in any data cell
    3. Single-letter role value (O/P/A/M) ONLY if in a role-column (C2: avoids 'a' as article)
    """
    lines = scan_text.splitlines()
    i = 0
    while i < len(lines):
        if not TABLE_ROW_RE.match(lines[i]):
            i += 1
            continue

        # Collect all rows of this table
        table_lines: list[str] = []
        while i < len(lines) and (
            TABLE_ROW_RE.match(lines[i]) or TABLE_DELIMITER_RE.match(lines[i])
        ):
            table_lines.append(lines[i])
            i += 1

        if len(table_lines) < 2:
            continue

        # Split into cells, skip delimiter rows
        parsed: list[list[str]] = []
        for line in table_lines:
            if TABLE_DELIMITER_RE.match(line):
                continue
            parsed.append(_split_cells(line))
        if len(parsed) < 2:
            continue

        header = parsed[0]
        data_rows = parsed[1:]

        # (C3) Check header row only for role column name
        header_has_role = any(ROLE_HEADER_RE.search(c) for c in header)
        role_col_indices = [i for i, c in enumerate(header) if ROLE_HEADER_RE.search(c)]

        # Multi-word role values in any column (distinctive enough)
        for row in data_rows:
            for cell in row:
                if re.search(
                    r"observed|proxy|assumption|model\s*output|estimate|"
                    r"scenario|inferred|illustrative",
                    cell,
                    re.IGNORECASE,
                ):
                    return True

        # (C2) Single-letter role values only count in role-column cells
        if role_col_indices:
            for row in data_rows:
                for idx in role_col_indices:
                    if idx < len(row):
                        cell = row[idx].strip()
                        if cell:
                            return True

        # Header with role column name counts as role structure
        if header_has_role:
            return True

    return False


def check_audit_self_assessment_consistency(cleaned: str) -> list[str]:
    """Check that audit block self-assessments match actual body execution.

    Warnings-level: if the audit block claims a discipline passed but the
    body does not meet the corresponding structural requirement, a warning
    is issued. Unknown discipline names are silently skipped.
    """
    sec = section_text(cleaned, ROUTE_AUDIT_HEADING)
    if sec is None:
        return []

    table = parse_table(sec)
    if table is None:
        return []

    header = table[0]
    audit_idx = find_col_index(header, [AUDIT_COL_RE])
    status_idx = find_col_index(header, [STATUS_COL_RE])

    if audit_idx == -1 or status_idx == -1:
        return []

    # Build scan_text once: body text excluding audit status section
    # and Source Register section, to avoid false positives from:
    # - [Sxx] in audit evidence column (C1 fix)
    # - [Sxx] in register "Claims Supported" column
    audit_bounds = section_bounds(cleaned, ROUTE_AUDIT_HEADING)
    register_bounds = section_bounds(cleaned, SOURCE_REGISTER_HEADING)
    raw_lines = cleaned.splitlines()

    if audit_bounds:
        _, audit_end = audit_bounds
        scan_lines = raw_lines[audit_end:]
        if register_bounds:
            reg_start, _ = register_bounds
            # Guard against negative slice (register before audit) — I1 fix
            offset = reg_start - audit_end
            if 0 < offset < len(scan_lines):
                scan_lines = scan_lines[:offset]
    elif register_bounds:
        reg_start, _ = register_bounds
        scan_lines = raw_lines[:reg_start]
    else:
        scan_lines = raw_lines

    scan_text = "\n".join(scan_lines)

    # Precompute role-label status for quantitative-role check
    body_has_role_labels = _body_has_role_labels(scan_text)

    warnings: list[str] = []

    for row in table[1:]:
        if len(row) <= max(audit_idx, status_idx):
            continue
        discipline = row[audit_idx].strip()
        status = row[status_idx].strip()

        if not AUDIT_PASSED_RE.match(status):
            continue

        disc_lower = discipline.lower()

        # source-traceability: body must have [Sxx] or equivalent citations
        if 'source-traceability' in disc_lower or 'source traceability' in disc_lower:
            has_refs = bool(BODY_SXX_RE.search(scan_text))
            if not has_refs:
                has_equiv = bool(
                    AUTHOR_YEAR_RE.search(scan_text)
                    or ARXIV_RE.search(scan_text)
                    or DOI_RE.search(scan_text)
                    or NL_ATTR_RE.search(scan_text)
                )
                if not has_equiv:
                    warnings.append(
                        f"Audit self-assessment mismatch: '{discipline}' is marked "
                        "✅ Passed, but the body has no [Sxx] or equivalent source citations"
                    )

        # quantitative-role: body tables should have role label columns
        if ('quantitative-role' in disc_lower
                or 'quantitative role' in disc_lower
                or '数字角色' in disc_lower):
            if not body_has_role_labels:
                warnings.append(
                    f"Audit self-assessment mismatch: '{discipline}' is marked "
                    "✅ Passed, but no quantitative role labels "
                    "(O/P/A/M or equivalent) found in body tables"
                )

    return warnings


# ── Academic route checks ──────────────────────────────────────────────────


def _is_academic_route(cleaned: str) -> bool:
    """Detect if the report's primary route is academic/literature-review.

    Uses word-boundary matching to avoid false positives like
    "Literature-based Market Research" or "Academic-style Overview".
    """
    route = get_route_name(cleaned)
    if route is None:
        return False
    rl = route.lower()
    if re.search(r"\bacademic\b", rl):
        return True
    if re.search(r"\bliterature[-\s]?review\b", rl):
        return True
    return False


def check_academic_register_columns(cleaned: str) -> list[str]:
    """Verify academic-route reports use 11-column Source Register.

    Academic / Literature Review reports must have the extended 11-column
    Source Register template (7 base + Publication Type, Peer-review Status,
    Venue, Venue Prestige). Returns error list (non-empty → hard fail).
    Only fires when the primary route is detected as academic/literature-review.
    """
    if not _is_academic_route(cleaned):
        return []
    sec = section_text(cleaned, SOURCE_REGISTER_HEADING)
    if sec is None:
        return []  # missing register is caught by existing check
    table = parse_table(sec)
    if table is None:
        return []
    header = table[0]
    if len(header) < 11:
        return [
            f"Academic / Literature Review route requires an 11-column "
            f"Source Register, but found {len(header)} column(s). "
            f"Expected 7 base columns + "
            f"{' / '.join(ACADEMIC_EXTRA_COLUMNS)}."
        ]
    return []


# ── Main ──────────────────────────────────────────────────────────────────


def validate_file(path: Path, strict: bool = False) -> int:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except (OSError, UnicodeError) as exc:
        print(f"{path}: cannot read file — {exc}")
        return EXIT_STRUCTURE
    cleaned = strip_fenced_code_blocks(text)

    errors: list[str] = []
    warnings: list[str] = []

    # 1. Route and audit status
    errors.extend(check_route_audit_block(cleaned))
    errors.extend(check_route_declaration(cleaned))
    errors.extend(check_audit_evidence(cleaned))

    # 2. Source Register
    errors.extend(check_source_register_exists(cleaned))
    errors.extend(check_source_register_columns(cleaned))
    errors.extend(check_source_register_missing_ids(cleaned))
    errors.extend(check_source_register_mapping(cleaned))
    errors.extend(check_source_register_duplicate_ids(cleaned))
    warnings.extend(check_source_register_doi_coverage(cleaned))
    warnings.extend(check_source_register_placeholders(cleaned))

    # 3. Body references
    errors.extend(check_body_references(cleaned))

    # 4. Key section citation coverage (hard fail)
    errors.extend(check_key_section_citation_coverage(cleaned))

    # 5. Audit self-assessment consistency (hard-fail gate)
    errors.extend(check_audit_self_assessment_consistency(cleaned))

    # 6. Academic route checks
    errors.extend(check_academic_register_columns(cleaned))

    # 7. Strict mode warnings
    if strict:
        warnings.extend(check_strict_warnings(cleaned))

    # Print warnings regardless of errors (all issues visible at once)
    if warnings:
        label = "warnings" if errors else "passed with warnings"
        print(f"Report quality validation {label} for {path}:")
        for w in warnings:
            print(f"  ⚠ {w}")

    if errors:
        print(f"Report quality validation failed for {path}:")
        for e in errors:
            print(f"  ✗ {e}")
        return EXIT_STRUCTURE

    if not warnings:
        print(f"Report quality validation passed for {path}.")

    return EXIT_PASS


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate final report quality against minimum delivery contracts."
    )
    parser.add_argument("path", help="Path to the report .md file")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Enable additional route-specific warnings",
    )
    args = parser.parse_args(argv)

    path = Path(args.path)
    if not path.is_file():
        print(f"{path}: not a regular file")
        return EXIT_STRUCTURE

    return validate_file(path, strict=args.strict)


if __name__ == "__main__":
    raise SystemExit(main())
