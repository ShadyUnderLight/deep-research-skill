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
EXIT_QUALITY = 3

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

AUDIT_PASSED_RE = re.compile(r"(✅\s*)?(Passed|已通过|通过)\s*$", re.IGNORECASE)
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
    r"据\s*(?:FY?\d{2,4}\s*)?(?:年报|招股书|公告|季报|半年报|官方报告|白皮书|研究)",
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
    """
    lines = text.splitlines()
    rows: list[list[str]] = []
    state = "before_header"

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
        cells = [c.strip() for c in stripped.strip("|").split("|")]
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


# ── Body reference checks ────────────────────────────────────────────────


def check_body_references(cleaned: str) -> list[str]:
    """Verify body contains [Sxx] or functionally equivalent citations.

    Format equivalence exemptions (per source-traceability-and-claim-citation.md):
    - Author-Year: (Author, Year, Venue)
    - arXiv ID: arXiv:XXXX.XXXXX
    - DOI: doi:10.XXX/... or https://doi.org/10.XXX/...
    - Natural language unique attribution: 据 FY2025 年报, etc.
    """
    body = body_text(cleaned)

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
        body = body_text(cleaned)

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


# ── Main ──────────────────────────────────────────────────────────────────


def validate_file(path: Path, strict: bool = False) -> int:
    text = path.read_text(encoding="utf-8", errors="replace")
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

    # 3. Body references
    errors.extend(check_body_references(cleaned))

    # 4. Strict mode warnings
    if strict:
        warnings.extend(check_strict_warnings(cleaned))

    # Report
    if errors:
        print(f"Report quality validation failed for {path}:")
        for e in errors:
            print(f"  ✗ {e}")
        # Determine exit code
        return EXIT_STRUCTURE

    if warnings:
        print(f"Report quality validation passed with warnings for {path}:")
        for w in warnings:
            print(f"  ⚠ {w}")
    else:
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
    if not path.exists():
        print(f"{path}: file not found")
        return EXIT_STRUCTURE

    return validate_file(path, strict=args.strict)


if __name__ == "__main__":
    raise SystemExit(main())
