#!/usr/bin/env python3

import argparse
import json
import re
from pathlib import Path

REQUIRED_HEADINGS = [
    "## Objective",
    "## Decision context",
    "## Primary route",
    "## Secondary disciplines",
    "## Core subquestions",
    "## Stop condition",
    "## Source register",
    "## Claim register",
    "## Uncertainty register",
    "## Artifact contract",
    "## Required audits",
    "## Final audit status",
]

# Decision tree fields: conditionally required when a specialized route
# was selected and the decision tree was used. Not required for shared-
# workflow or lightweight tasks.
DECISION_TREE_HEADINGS = [
    "## Action burden",
    "## Weight-bearing object",
    "## Decision tree path",
    "## Tie-break rationale",
]

REQUIRED_SET = set(REQUIRED_HEADINGS)

ARTIFACT_RED_FLAGS = [
    r"\bTBD\b",
    r"\bTODO\b",
    r"\bXXX\b",
    r"\[\[placeholder\]\]",
    r"\{citation\}",
    r"\{\{[^\n{}]{1,80}\}\}",
    r"<PLACEHOLDER>",
    r"\[SOURCE\]",
    r"\[CITATION NEEDED\]",
    r"\[INSERT [^\]\n]{1,80}\]",
]

H2_RE = re.compile(r"^## (.+)$", re.MULTILINE)
ALL_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)
INLINE_FENCE_RE = re.compile(r"^[ ]{0,3}(`{3,}|~{3,})")

EXIT_USAGE = 1
EXIT_STRUCTURE = 2
EXIT_ARTIFACT = 3
EXIT_STRICT = 4


def strip_fenced_code_blocks(text: str) -> str:
    lines = text.split("\n")
    out = []
    in_fence = False
    fence_char = None
    fence_len = 0

    for line in lines:
        stripped = line.rstrip()
        if not in_fence:
            m = INLINE_FENCE_RE.match(stripped)
            if m:
                fence_char = m.group(1)[0]
                fence_len = len(m.group(1))
                in_fence = True
                continue
            out.append(line)
        else:
            closing_re = re.compile(
                r"^[ ]{0,3}"
                + re.escape(fence_char)
                + "{"
                + str(fence_len)
                + r",}\s*$"
            )
            if closing_re.match(stripped):
                in_fence = False
                continue

    return "\n".join(out)


def _check_decision_tree_headings(cleaned: str) -> list[str]:
    """Check for decision tree fields if a specialized route was selected.

    Only warns — does not fail validation. Decision tree fields are
    recommended but not required for shared-workflow or lightweight tasks."""
    found = set()
    for m in H2_RE.finditer(cleaned):
        title = m.group(1).rstrip()
        full = f"## {title}"
        if full in set(DECISION_TREE_HEADINGS):
            found.add(full)

    # Only warn if a specialized route was declared
    primary_section = _section_body(cleaned, "Primary route")
    if not primary_section:
        return []  # Primary route is already checked as required

    # Check if a specialized route was selected (not shared-workflow).
    # Canonicalize via route-manifest.json aliases so display-name forms
    # like "Constrained Choice / Shortlist" are recognized.
    manifest_path = Path(__file__).resolve().parent.parent / "schemas" / "route-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    search_ids: set[str] = set()
    for route in manifest["routes"]:
        if route["category"] != "specialized":
            continue
        # Canonical id + all aliases
        search_ids.add(route["id"].lower())
        for alias in route.get("aliases", []):
            search_ids.add(alias.lower())

    primary_lower = primary_section.lower()
    has_specialized = any(rid in primary_lower for rid in search_ids)
    if not has_specialized:
        return []  # Shared-workflow or unknown — decision tree fields not needed

    missing = [h for h in DECISION_TREE_HEADINGS if h not in found]
    return missing


def find_missing_headings(cleaned: str) -> list[str]:
    found = set()
    for m in H2_RE.finditer(cleaned):
        title = m.group(1).rstrip()
        full = f"## {title}"
        if full in REQUIRED_SET:
            found.add(full)
    return [h for h in REQUIRED_HEADINGS if h not in found]


def find_empty_sections(cleaned: str) -> list[str]:
    lines = cleaned.split("\n")
    heading_positions: list[tuple[str, int]] = []
    for i, line in enumerate(lines):
        m = re.match(r"^(#{1,6})\s+(.+)$", line.rstrip())
        if m:
            heading_positions.append((line.rstrip(), i))

    empty = []
    for idx, (heading_text, line_num) in enumerate(heading_positions):
        if heading_text not in REQUIRED_SET:
            continue
        next_line = (
            heading_positions[idx + 1][1]
            if idx + 1 < len(heading_positions)
            else len(lines)
        )
        body = lines[line_num + 1 : next_line]
        body_no_heading = [l for l in body if not re.match(r"^#{1,6}\s", l)]
        body_text = "\n".join(body_no_heading).strip()
        if not body_text:
            empty.append(heading_text)

    return empty


def check_artifacts(text: str) -> list[tuple]:
    hits = []
    for pattern in ARTIFACT_RED_FLAGS:
        matches = re.findall(pattern, text)
        if matches:
            hits.append((pattern, matches[:3]))
    return hits


# ─── Strict mode helpers ──────────────────────────────────────────────────────


def _section_body(text: str, heading: str) -> str:
    lines = text.split("\n")
    buf: list[str] = []
    collecting = False
    for line in lines:
        if re.match(rf"^## {re.escape(heading)}\s*$", line):
            collecting = True
            continue
        if collecting:
            if re.match(r"^##\s", line):
                break
            buf.append(line)
    return "\n".join(buf).strip()


def _body_outside_section(text: str, heading: str) -> str:
    lines = text.split("\n")
    out: list[str] = []
    skipping = False
    for line in lines:
        if re.match(rf"^## {re.escape(heading)}\s*$", line):
            skipping = True
            out.append(line)
            continue
        if skipping:
            if re.match(r"^##\s", line):
                skipping = False
                out.append(line)
                continue
            continue
        out.append(line)
    return "\n".join(out)


_BODY_REF_RE = re.compile(r"\[([SIU])(\d{2})\]")

_CLAIM_LINE_RE = re.compile(r"^[-*]\s+Claim:")


def _collect_register_ids(text: str, heading: str) -> tuple[dict[str, str], list[str]]:
    body = _section_body(text, heading)
    if not body:
        return {}, []
    ids: dict[str, str] = {}
    issues: list[str] = []
    seen: dict[str, str] = {}

    for line in body.split("\n"):
        stripped = line.strip()
        if not stripped:
            continue
        for m in re.findall(r"\[([SIU])(\d+)\]", stripped):
            prefix, num = m[0], m[1]
            raw = f"[{prefix}{num}]"
            if len(num) != 2:
                issues.append(
                    f"Malformed ID '{raw}': "
                    f"expected 2 digits, got {len(num)}"
                )
                continue
            sid = f"{prefix}{num}"
            if sid in seen:
                issues.append(f"Duplicate ID '{raw}'")
            else:
                seen[sid] = stripped[:80]
                ids[sid] = stripped[:80]
        rest = re.sub(r"\[[A-Z]\d+\]", "", stripped)
        for m in re.finditer(r"(?<!\w)([SIU])(\d{2})(?!\w)", rest):
            prefix, num = m.group(1), m.group(2)
            sid = f"{prefix}{num}"
            if sid in seen:
                issues.append(f"Duplicate ID '{prefix}{num}' (bare)")
            else:
                seen[sid] = stripped[:80]
                ids[sid] = stripped[:80]
        for m in re.finditer(r"(?<!\w)([SIU])(\d{1,3})(?!\w)", rest):
            prefix, num = m.group(1), m.group(2)
            if len(num) == 2:
                continue
            issues.append(
                f"Malformed ID '{prefix}{num}': "
                f"expected 2 digits, got {len(num)}"
            )

    return ids, issues


def _find_body_references(cleaned: str) -> dict[str, set[str]]:
    rest = _body_outside_section(cleaned, "Source register")
    rest = _body_outside_section(rest, "Uncertainty register")
    refs: dict[str, set[str]] = {"S": set(), "U": set(), "I": set()}
    for m in _BODY_REF_RE.finditer(rest):
        refs[m.group(1)].add(f"{m.group(1)}{m.group(2)}")
    return refs


def _split_claim_blocks(text: str) -> list[str]:
    body = _section_body(text, "Claim register")
    if not body:
        return []
    blocks: list[str] = []
    current: list[str] = []
    for line in body.split("\n"):
        if _CLAIM_LINE_RE.match(line):
            if current:
                blocks.append("\n".join(current))
            current = [line]
        elif current:
            current.append(line)
    if current:
        blocks.append("\n".join(current))
    return blocks


def _check_malformed_refs(cleaned: str) -> list[str]:
    rest = _body_outside_section(cleaned, "Source register")
    rest = _body_outside_section(rest, "Uncertainty register")
    issues: list[str] = []
    for m in re.finditer(r"\[([SIU])(\d+)\]", rest):
        prefix, num = m.group(1), m.group(2)
        if len(num) != 2:
            issues.append(
                f"Malformed reference '[{prefix}{num}]': "
                f"expected 2 digits, got {len(num)}"
            )
    return issues


def run_strict_checks(cleaned: str) -> list[str]:
    errors: list[str] = []
    warnings: list[str] = []

    source_ids, sid_issues = _collect_register_ids(cleaned, "Source register")
    uncertainty_ids, uid_issues = _collect_register_ids(cleaned, "Uncertainty register")
    errors.extend(sid_issues)
    errors.extend(uid_issues)

    # DISCOVERY is not a valid Source Register source type.
    # Scan the Source register body for any DISCOVERY reference.
    source_body = _section_body(cleaned, "Source register")
    if source_body:
        for line in source_body.split("\n"):
            if re.search(r"\bDISCOVERY\b", line, re.IGNORECASE):
                errors.append(
                    f"DISCOVERY in Source register: {line.strip()[:80]}"
                )

    if not source_ids:
        errors.append(
            "No source IDs (Sxx or [Sxx]) found in Source register"
        )

    body_refs = _find_body_references(cleaned)

    undefined_s = body_refs["S"] - set(source_ids.keys())
    if undefined_s:
        errors.append(
            f"Undefined source IDs referenced: "
            f"{', '.join(sorted(undefined_s))}"
        )

    undefined_u = body_refs["U"] - set(uncertainty_ids.keys())
    if undefined_u:
        errors.append(
            f"Undefined uncertainty IDs referenced: "
            f"{', '.join(sorted(undefined_u))}"
        )

    if body_refs["I"]:
        warnings.append(
            f"Inference IDs [{', '.join(sorted(body_refs['I']))}] "
            f"referenced but no Inference register to validate against"
        )

    if source_ids:
        all_refs = body_refs["S"] | body_refs["U"] | body_refs["I"]
        unused = set(source_ids.keys()) - all_refs
        if unused:
            warnings.append(
                f"Unused source IDs (defined but never referenced): "
                f"{', '.join(sorted(unused))}"
            )

    malformed_issues = _check_malformed_refs(cleaned)
    errors.extend(malformed_issues)

    all_valid_ids = {**source_ids, **uncertainty_ids}
    claim_blocks = _split_claim_blocks(cleaned)
    for idx, block in enumerate(claim_blocks, 1):
        refs = set(_BODY_REF_RE.findall(block))
        if not refs:
            first_line = block.split("\n")[0].strip()[:80]
            warnings.append(
                f"Claim #{idx} has no evidence references: {first_line}"
            )
        for prefix, num in refs:
            if prefix == "I":
                continue
            sid = f"{prefix}{num}"
            if sid not in all_valid_ids:
                errors.append(
                    f"Claim #{idx} references undefined '{sid}'"
                )

    audit_issues = _check_audit_status(cleaned)
    for issue in audit_issues:
        if issue.startswith("Final audit status is 'Partial'"):
            warnings.append(issue)
        else:
            errors.append(issue)

    # Closest alternative / boundary judgment
    alt_issues = _check_closest_alternative(cleaned)
    for issue in alt_issues:
        errors.append(issue)

    # Per-audit run statuses
    run_errs, run_warns = _check_audit_run_statuses(cleaned)
    errors.extend(run_errs)
    warnings.extend(run_warns)

    # Audit consistency (Pass vs not-run/partial, Partial vs not-run-no-reason, Fail vs all-ok)
    cons_issues = _check_audit_consistency(cleaned)
    for issue in cons_issues:
        if "consider Partial" in issue:
            warnings.append(issue)
        else:
            errors.append(issue)

    result: list[str] = []
    for e in errors:
        result.append(f"  ✗ {e}")
    for w in warnings:
        result.append(f"  ⚠ {w}")
    return result


def _check_audit_status(text: str) -> list[str]:
    body = _section_body(text, "Final audit status")
    if not body:
        return []
    first_line = body.split("\n")[0].strip()
    m = re.match(r"^(Pass|Partial|Fail)\b", first_line)
    if not m:
        return [
            f"Final audit status must be Pass, Partial, or Fail. "
            f"Got: {first_line[:60]}"
        ]
    status = m.group(1)
    if status == "Fail":
        return [
            "Final audit status is 'Fail' — pack is not ready for delivery"
        ]
    if status == "Partial":
        return [
            "Final audit status is 'Partial' — pack may not be ready for delivery"
        ]
    return []


# ─── Structured audit status parsing ────────────────────────────────────────────

# Extract status after em dash separator (standard format: "audit-name — STATUS")
_STATUS_EXTRACT_RE = re.compile(
    r"[–—]\s*(passed|skipped|not-run|partial|已通过|已跳过|未运行|部分通过)\b",
    re.IGNORECASE,
)

# Detect reason after status (colon followed by non-whitespace content)


def _parse_audit_statuses(cleaned: str) -> list[dict]:
    """Parse Required audits into structured status records.

    Each record: {"line": str, "status": str|None, "has_reason": bool}
    Status is extracted from the first em-dash-separated token.
    has_reason is True when the status is followed by colon with content.
    """
    body = _section_body(cleaned, "Required audits")
    if not body:
        return []
    records: list[dict] = []
    for raw in body.split("\n"):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        m = _STATUS_EXTRACT_RE.search(line)
        if not m:
            records.append({"line": line, "status": None, "has_reason": False})
            continue
        status = m.group(1).lower()
        after = line[m.end():]
        # Reason must immediately follow the status with non-trivial content.
        # Anchored match prevents distant colons (e.g. "skipped — no; note: x").
        # \w + CJK range requires at least one letter/ideograph, not just punctuation.
        has_reason = bool(re.match(
            r"\s*[:：]\s*[a-zA-Z0-9_\u4e00-\u9fff]", after
        ))
        records.append({"line": line, "status": status, "has_reason": has_reason})
    return records


# ─── Strict mode: closest-alternative, per-audit, consistency ──────────────────

_CLOSEST_ALT_RE = re.compile(
    r"\b(?:alternative|closest|boundary|instead of|rather than|chosen over"
    r"|vs\.?|versus|区别于|替代|备选|边界)\b",
    re.IGNORECASE,
)

_AUDIT_STATUS_RE = re.compile(
    r"\b(?:passed|skipped|not-run|partial"
    r"|已通过|已跳过|未运行|部分通过)\b",
    re.IGNORECASE,
)

# Structured status: status must follow an em dash or colon separator.
# The regular hyphen [-] is excluded — it matches list bullets (e.g.
# "passed-source audit" with leading "- " is not a status stamp)
_AUDIT_STATUS_STRUCTURED_RE = re.compile(
    r"[–—:]\s*(?:passed|skipped|not-run|partial"
    r"|已通过|已跳过|未运行|部分通过)\b",
    re.IGNORECASE,
)

# Require exclusion/rejection language in boundary judgment, not just keywords
_CLOSEST_ALT_EXCLUDE_RE = re.compile(
    r"\b(?:rejected|excluded|not applicable|not (?:a |an )?(?:fit|match|suitable)"
    r"|排除|不适用|不适合|排除在外|改用|改为)\b",
    re.IGNORECASE,
)

# Require specific alternative-identity or switching-condition language.
# Checks that the boundary judgment contains more than just "rejected" —
# must explain why or describe when the alternative would apply.
_CLOSEST_ALT_IDENTITY_RE = re.compile(
    r"\b(?:would become|would apply|if\b.*\b(?:then|would|will)\b|"
    r"when\b.*\bchanges?\b|switch to|instead would be|"
    r"改用|转为|切换|如果.*则|当.*时|"
    r"rejected\s*[–—]\s*(?:task|because|since|due|as)\b|"
    r"rejected because|rejected since|rejected as|"
    r"alternative (?:is|would be)|boundary: if)\b",
    re.IGNORECASE,
)


def _check_closest_alternative(cleaned: str) -> list[str]:
    """Check Primary route section contains boundary judgment language."""
    body = _section_body(cleaned, "Primary route")
    if not body:
        return ["Primary route section is empty — missing route declaration"]
    if not _CLOSEST_ALT_RE.search(body):
        return [
            "Primary route section lacks closest-alternative / "
            "boundary judgment language"
        ]
    # Reject trivial hits: need substance beyond the keyword
    stripped = " ".join(body.split())
    if len(stripped) < 60:
        return [
            "Primary route section boundary judgment too brief "
            f"({len(stripped)} chars) — must include route identity, "
            "alternative, and reason for exclusion or switching"
        ]
    # Require exclusion/rejection language, not just boundary keywords
    if not _CLOSEST_ALT_EXCLUDE_RE.search(body):
        return [
            "Primary route section mentions alternative/boundary but "
            "lacks exclusion/rejection language (e.g. rejected, excluded, "
            "not applicable, not a fit, 排除, 不适用) — boundary judgment "
            "must explain why the alternative was not chosen"
        ]
    # Require specific alternative identity (named route or switching condition)
    if not _CLOSEST_ALT_IDENTITY_RE.search(body):
        return [
            "Primary route section has boundary/exclusion language but "
            "lacks specific alternative identity — must name the "
            "alternative route or describe switching condition "
            "(e.g. 'would become', 'if X then Y', '改用', '转为')"
        ]
    return []


def _check_audit_run_statuses(cleaned: str) -> list[str]:
    """Check Required audits section: each line has a status, and
    skipped/partial/not-run statuses have a documented reason.
    Returns (errors, warnings) tuple."""
    records = _parse_audit_statuses(cleaned)
    if not records:
        return (["Required audits section is empty"], [])

    errors: list[str] = []
    warnings: list[str] = []

    NO_REASON_STATUSES = {"skipped", "partial", "not-run",
                          "已跳过", "部分通过", "未运行"}

    for r in records:
        if r["status"] is None:
            errors.append(
                f"Required audit missing run status: {r['line'][:60]}"
            )
        elif r["status"] in NO_REASON_STATUSES and not r["has_reason"]:
            warnings.append(
                f"Required audit has {r['status']} "
                f"without documented reason: {r['line'][:60]}"
            )

    return (errors, warnings)


def _check_audit_consistency(cleaned: str) -> list[str]:
    """Check Final audit status is consistent with per-audit run statuses.
    Uses structured status parsing to avoid false matches on reason text."""
    audit_body = _section_body(cleaned, "Final audit status")
    if not audit_body:
        return []
    first_line = audit_body.split("\n")[0].strip()
    m = re.match(r"^(Pass|Partial|Fail)\b", first_line)
    if not m:
        return []
    declared = m.group(1)

    records = _parse_audit_statuses(cleaned)
    if not records:
        return []

    statuses = [r["status"] for r in records if r["status"] is not None]

    has_partial = "partial" in statuses or "部分通过" in statuses
    has_not_run = "not-run" in statuses or "未运行" in statuses

    def _no_reason(*sts: str) -> bool:
        return any(
            r["status"] in sts and not r["has_reason"]
            for r in records if r["status"]
        )

    has_not_run_no_reason = _no_reason("not-run", "未运行")
    has_skipped_partial_no_reason = _no_reason(
        "skipped", "partial", "已跳过", "部分通过"
    )

    issues: list[str] = []

    if declared == "Pass":
        if has_partial:
            issues.append(
                "Final audit status is 'Pass' but Required audits "
                "contain partial item(s) — Pass requires all audits "
                "fully executed (passed or skipped)"
            )
        if has_not_run:
            issues.append(
                "Final audit status is 'Pass' but Required audits "
                "contain not-run item(s) — Pass requires all audits "
                "to be executed (passed or skipped)"
            )
        if has_skipped_partial_no_reason:
            issues.append(
                "Final audit status is 'Pass' but Required audits "
                "contain skipped/partial item(s) without documented "
                "reason — Pass requires reason for skipped/partial"
            )

    if declared == "Partial":
        if has_not_run_no_reason:
            issues.append(
                "Final audit status is 'Partial' but Required audits "
                "contain not-run item(s) without documented reason — "
                "should be Fail"
            )
        if has_skipped_partial_no_reason:
            issues.append(
                "Final audit status is 'Partial' but Required audits "
                "contain skipped/partial item(s) without documented "
                "reason — Partial requires reason for all non-passed "
                "statuses"
            )

    if declared == "Fail":
        if not has_not_run_no_reason:
            issues.append(
                "Final audit status is 'Fail' but no not-run-without-reason "
                "audit found — verify validator errors exist; otherwise "
                "consider Partial"
            )

    return issues


# ─── Main ─────────────────────────────────────────────────────────────────────


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate a Research Pack markdown file"
    )
    parser.add_argument("path", help="Path to the Research Pack .md file")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Enable semantic checks (source IDs, references, audit status)",
    )
    args = parser.parse_args()

    path = Path(args.path)
    text = path.read_text(encoding="utf-8")
    cleaned = strip_fenced_code_blocks(text)

    missing = find_missing_headings(cleaned)
    if missing:
        print("Missing required headings:")
        for heading in missing:
            print(f"- {heading}")
        return EXIT_STRUCTURE

    # Conditional check: decision tree fields are recommended when
    # a specialized route is selected (not shared-workflow), but
    # are not required for lightweight tasks.
    dt_missing = _check_decision_tree_headings(cleaned)
    if dt_missing:
        print("Note: Decision tree fields recommended (not required):")
        for heading in dt_missing:
            print(f"- {heading}")
        # Warning only — does not fail validation

    empty = find_empty_sections(cleaned)
    if empty:
        print("Empty required sections (no content after heading):")
        for heading in empty:
            print(f"- {heading}")
        return EXIT_STRUCTURE

    artifact_hits = check_artifacts(text)
    if artifact_hits:
        print("Artifact red flags detected:")
        for pattern, matches in artifact_hits:
            preview = ", ".join(repr(m) for m in matches)
            print(f"- pattern {pattern}: {preview}")
        return EXIT_ARTIFACT

    if args.strict:
        strict_issues = run_strict_checks(cleaned)
        if strict_issues:
            print("Strict mode issues:")
            for issue in strict_issues:
                print(issue)
            has_errors = any(issue.startswith("  ✗") for issue in strict_issues)
            return EXIT_STRICT if has_errors else 0

    print("Research Pack structure looks valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
