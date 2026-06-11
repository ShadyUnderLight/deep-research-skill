#!/usr/bin/env python3
"""Detect report frameworks that are declared but not executed.

This lint is intentionally lightweight and fixture/report scoped. It catches
the concrete Issue #223 patterns where a report declares a discipline such as
O/P/A/M labels, Source Register traceability, or an academic evidence framework
but the body does not visibly apply that discipline.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


EXIT_ISSUES = 2
REGISTER_INFLATION_FAIL_RATIO = 0.25

FENCE_RE = re.compile(r"^[ ]{0,3}(`{3,}|~{3,})")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
TABLE_ROW_RE = re.compile(r"^\s*\|.*\|\s*$")
TABLE_DELIMITER_RE = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$")
NUMBER_RE = re.compile(
    r"(?:[$¥€£]?\s*\d[\d,]*(?:\.\d+)?\s*(?:%|bp|bps|x|X|倍|万|亿|兆|台|GW|GWh|TWh|MW|B|M|bn|mn|months?|月|年)?\+?)",
    re.IGNORECASE,
)

OPAM_DECL_RE = re.compile(
    r"(?:O/P/A/M|O\s*=\s*observed|P\s*=\s*proxy|A\s*=\s*assumption|M\s*=\s*model)",
    re.IGNORECASE,
)
ROLE_HEADER_RE = re.compile(r"(?:数字角色|number role|role|epistemic role)", re.IGNORECASE)
ROLE_VALUE_RE = re.compile(
    r"(?:\b[OPAM]\b|observed|proxy|assumption|model\s*output|estimate|scenario|inferred|illustrative)",
    re.IGNORECASE,
)

SOURCE_REGISTER_HEADING_RE = re.compile(r"^#{1,6}\s+Source Register\s*$", re.IGNORECASE)
SOURCE_ID_RE = re.compile(r"(?<!\w)\[?(S\d{2})\]?(?!\w)")
BODY_SOURCE_REF_RE = re.compile(r"\[S\d{2}\]")
ARXIV_REF_RE = re.compile(
    r"(?:arxiv\s*:\s*|arxiv\.org/(?:abs|pdf)/)(\d{4}\.\d{4,5})(?:v\d+)?",
    re.IGNORECASE,
)
DOI_REF_RE = re.compile(
    r"(?:doi\s*:\s*|https?://(?:dx\.)?doi\.org/)?"
    r"(10\.\d{4,9}/[^\s\]\)\|,;\"'<>]+)",
    re.IGNORECASE,
)
AUTHOR_YEAR_RE = re.compile(
    r"\(([A-Z][A-Za-z'’-]+)(?:\s+et\s+al\.)?,\s*((?:19|20)\d{2})(?:,\s*[^)]{2,80})?\)"
    r"|\b([A-Z][A-Za-z'’-]+)(?:\s+et\s+al\.)?\s+((?:19|20)\d{2})\b"
)
NATURAL_ATTR_RE = re.compile(
    r"(?:据|根据|来自|引用|援引)\s*([^。；;，,\n]{0,60}?"
    r"(?:FY\s*20\d{2}|20\d{2}\s*Q[1-4]|招股书|年报|季报|业绩公告|annual report|prospectus|earnings announcement)"
    r"[^。；;，,\n]{0,60})"
    r"|((?:FY\s*20\d{2}|20\d{2}\s*Q[1-4])[^。；;，,\n]{0,40}?"
    r"(?:年报|季报|业绩公告|annual report|earnings announcement))"
    r"|((?:招股书|prospectus)\s*(?:披露)?)",
    re.IGNORECASE,
)
VAGUE_ATTR_RE = re.compile(r"(?:公开资料|据悉|市场研究|行业研究|公开信息)", re.IGNORECASE)

ACADEMIC_FRAMEWORK_RE = re.compile(
    r"(?:study\s+design\s+quality.{0,80}venue\s+prestige|venue\s+prestige.{0,80}study\s+design\s+quality|研究设计.{0,80}发表场所声誉|发表场所声誉.{0,80}研究设计|双维.{0,40}证据|多级.{0,40}证据)",
    re.IGNORECASE | re.DOTALL,
)
MAPPING_HEADER_RE = re.compile(
    r"\|\s*(?:Source|来源)\s*\|.*(?:Study design|研究设计).*(?:Venue prestige|发表场所声誉|Venue)",
    re.IGNORECASE,
)


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
            r"^[ ]{0,3}" + re.escape(fence_char) + "{" + str(fence_len) + r",}\s*$"
        )
        if closing.match(stripped):
            in_fence = False

    return "\n".join(out)


def section_bounds(lines: list[str], heading_re: re.Pattern[str]) -> tuple[int, int] | None:
    start = None
    start_level = None
    for idx, line in enumerate(lines):
        if heading_re.match(line):
            m = HEADING_RE.match(line)
            start = idx
            start_level = len(m.group(1)) if m else 2
            break
    if start is None:
        return None

    end = len(lines)
    for idx in range(start + 1, len(lines)):
        m = HEADING_RE.match(lines[idx])
        if m and len(m.group(1)) <= start_level:
            end = idx
            break
    return start, end


def remove_section(text: str, heading_re: re.Pattern[str]) -> str:
    lines = text.splitlines()
    bounds = section_bounds(lines, heading_re)
    if not bounds:
        return text
    start, end = bounds
    return "\n".join(lines[:start] + lines[end:])


def table_lines(text: str) -> list[str]:
    rows = []
    for line in text.splitlines():
        if not TABLE_ROW_RE.match(line):
            continue
        if TABLE_DELIMITER_RE.match(line):
            continue
        rows.append(line)
    return rows


def split_markdown_table_row(row: str) -> list[str]:
    stripped = row.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]
    return [cell.strip() for cell in stripped.split("|")]


def normalize_compact(text: str) -> str:
    return re.sub(r"\s+", "", text.lower())


def register_entries(register_text: str) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    for row in table_lines(register_text):
        cells = split_markdown_table_row(row)
        if not cells or cells[0].strip().lower() == "id":
            continue
        source_id = SOURCE_ID_RE.search(cells[0])
        if not source_id:
            continue
        entries.append(
            {
                "id": source_id.group(1),
                "text": " ".join(cells),
                "source_name": cells[1] if len(cells) > 1 else "",
                "doi_url": cells[4] if len(cells) > 4 else "",
            }
        )
    return entries


def normalize_doi(doi: str) -> str:
    cleaned = doi.strip().lower()
    cleaned = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", cleaned)
    cleaned = re.sub(r"^doi\s*:\s*", "", cleaned)
    return cleaned.rstrip(".,;:)")


def equivalent_id_matches(
    body_values: set[str],
    entries: list[dict[str, str]],
    pattern: re.Pattern[str],
    normalizer=lambda value: value.lower(),
) -> set[str]:
    cited: set[str] = set()
    if not body_values:
        return cited

    for entry in entries:
        entry_values = {normalizer(match) for match in pattern.findall(entry["text"])}
        if body_values & entry_values:
            cited.add(entry["id"])
    return cited


def author_year_refs(body_text: str, entries: list[dict[str, str]]) -> set[str]:
    cited: set[str] = set()
    for match in AUTHOR_YEAR_RE.finditer(body_text):
        author = match.group(1) or match.group(3)
        year = match.group(2) or match.group(4)
        if not author or not year:
            continue
        hits = [
            entry["id"]
            for entry in entries
            if author.lower() in entry["text"].lower() and year in entry["text"]
        ]
        if len(hits) == 1:
            cited.add(hits[0])
    return cited


def natural_anchor_tokens(phrase: str) -> list[str]:
    if VAGUE_ATTR_RE.search(phrase):
        return []

    compact = normalize_compact(phrase)
    tokens: list[str] = []
    tokens.extend(re.findall(r"fy20\d{2}", compact))
    tokens.extend(re.findall(r"20\d{2}q[1-4]", compact))

    if "annualreport" in compact or "年报" in compact:
        tokens.append("annual_report")
    if "earningsannouncement" in compact or "业绩公告" in compact:
        tokens.append("earnings")
    if "quarterly" in compact or "季报" in compact:
        tokens.append("quarterly")
    if "prospectus" in compact or "招股书" in compact:
        tokens.append("prospectus")

    return list(dict.fromkeys(tokens))


def entry_matches_natural_tokens(entry: dict[str, str], tokens: list[str]) -> bool:
    compact = normalize_compact(entry["text"])
    for token in tokens:
        if token == "annual_report":
            if "annualreport" not in compact and "年报" not in compact:
                return False
            continue
        if token == "earnings":
            if (
                "earnings" not in compact
                and "results" not in compact
                and "业绩公告" not in compact
            ):
                return False
            continue
        if token == "quarterly":
            if "quarter" not in compact and "季报" not in compact:
                return False
            continue
        if token == "prospectus":
            if "prospectus" not in compact and "招股书" not in compact:
                return False
            continue
        if token not in compact:
            return False
    return True


def natural_language_refs(body_text: str, entries: list[dict[str, str]]) -> set[str]:
    cited: set[str] = set()
    for match in NATURAL_ATTR_RE.finditer(body_text):
        phrase = next((group for group in match.groups() if group), "")
        tokens = natural_anchor_tokens(phrase)
        if not tokens:
            continue
        hits = [
            entry["id"]
            for entry in entries
            if entry_matches_natural_tokens(entry, tokens)
        ]
        if len(hits) == 1:
            cited.add(hits[0])
    return cited


def equivalent_body_source_refs(body_text: str, entries: list[dict[str, str]]) -> set[str]:
    arxiv_values = {match.lower() for match in ARXIV_REF_RE.findall(body_text)}
    doi_values = {normalize_doi(match) for match in DOI_REF_RE.findall(body_text)}

    cited: set[str] = set()
    cited.update(equivalent_id_matches(arxiv_values, entries, ARXIV_REF_RE))
    cited.update(equivalent_id_matches(doi_values, entries, DOI_REF_RE, normalize_doi))
    cited.update(author_year_refs(body_text, entries))
    cited.update(natural_language_refs(body_text, entries))
    return cited


def check_opam_execution(text: str, path: Path) -> list[str]:
    if not OPAM_DECL_RE.search(text):
        return []

    rows = [row for row in table_lines(text) if NUMBER_RE.search(row)]
    if not rows:
        return []

    role_headers = [row for row in table_lines(text) if ROLE_HEADER_RE.search(row)]
    applied = 0
    for row in rows:
        if ROLE_VALUE_RE.search(row):
            applied += 1
            continue
        if role_headers and ROLE_HEADER_RE.search(row):
            applied += 1

    if applied == 0:
        return [
            f"{path}: O/P/A/M or equivalent quantitative role system is declared, "
            "but numeric table rows do not visibly apply role labels"
        ]

    if applied / len(rows) < 0.5:
        return [
            f"{path}: O/P/A/M or equivalent quantitative role system is declared, "
            f"but only {applied}/{len(rows)} numeric table rows visibly apply role labels"
        ]

    return []


def check_source_register_execution(text: str, path: Path) -> list[str]:
    lines = text.splitlines()
    bounds = section_bounds(lines, SOURCE_REGISTER_HEADING_RE)
    if not bounds:
        return []

    start, end = bounds
    register_text = "\n".join(lines[start:end])
    source_ids = set(SOURCE_ID_RE.findall(register_text))
    if not source_ids:
        return []

    body_text = remove_section(text, SOURCE_REGISTER_HEADING_RE)
    body_refs = set(ref.strip("[]") for ref in BODY_SOURCE_REF_RE.findall(body_text))
    body_refs.update(equivalent_body_source_refs(body_text, register_entries(register_text)))
    if not body_refs:
        return [
            f"{path}: Source Register declares {len(source_ids)} source ID(s), "
            "but the body contains no [Sxx] or equivalent citations"
        ]

    uncited_source_ids = sorted(source_ids - body_refs)
    uncited_ratio = len(uncited_source_ids) / len(source_ids)
    if uncited_ratio > REGISTER_INFLATION_FAIL_RATIO:
        uncited_preview = ", ".join(uncited_source_ids[:10])
        if len(uncited_source_ids) > 10:
            uncited_preview += ", ..."
        return [
            f"{path}: Source Register declares {len(source_ids)} source ID(s), "
            f"but {len(uncited_source_ids)} are never cited in the body "
            f"({uncited_ratio:.0%} uncited; register inflation): {uncited_preview}"
        ]

    return []


def check_academic_framework_execution(text: str, path: Path) -> list[str]:
    if not ACADEMIC_FRAMEWORK_RE.search(text):
        return []
    if MAPPING_HEADER_RE.search(text):
        return []
    return [
        f"{path}: academic evidence framework is declared, "
        "but no source-level evidence mapping table is visible"
    ]


def validate_file(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    cleaned = strip_fenced_code_blocks(text)
    errors: list[str] = []
    errors.extend(check_opam_execution(cleaned, path))
    errors.extend(check_source_register_execution(cleaned, path))
    errors.extend(check_academic_framework_execution(cleaned, path))
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Lint declared report frameworks that are not executed."
    )
    parser.add_argument("paths", nargs="+", help="Markdown/text files to validate")
    args = parser.parse_args(argv)

    errors: list[str] = []
    for raw_path in args.paths:
        path = Path(raw_path)
        if not path.exists():
            errors.append(f"{path}: file not found")
            continue
        errors.extend(validate_file(path))

    if errors:
        print("Declared execution lint failed:")
        for error in errors:
            print(f"- {error}")
        return EXIT_ISSUES

    print(f"Declared execution lint passed for {len(args.paths)} file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
