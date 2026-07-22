#!/usr/bin/env python3

import argparse
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
    run_issues = _check_audit_run_statuses(cleaned)
    for issue in run_issues:
        errors.append(issue)

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

_AUDIT_NOT_RUN_RE = re.compile(
    r"\b(?:not-run|未运行)\b",
    re.IGNORECASE,
)

# Matches "not-run" / "未运行" NOT followed by a reason (colon, parenthesis)
_AUDIT_NOT_RUN_NO_REASON_RE = re.compile(
    r"\b(?:not-run|未运行)\b(?!\s*[:：（(]\s*\S)",
    re.IGNORECASE,
)

# Matches "partial" / "部分通过" — incomplete execution
_AUDIT_PARTIAL_RE = re.compile(
    r"\b(?:partial|部分通过)\b",
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
    # Reject trivial hits: boundary needs substance beyond the keyword
    stripped = " ".join(body.split())
    if len(stripped) < 60:
        return [
            "Primary route section boundary judgment too brief "
            f"({len(stripped)} chars) — must include route identity, "
            "alternative, and reason for exclusion or switching"
        ]
    return []


def _check_audit_run_statuses(cleaned: str) -> list[str]:
    """Check Required audits section lists per-audit run statuses."""
    body = _section_body(cleaned, "Required audits")
    if not body:
        return ["Required audits section is empty"]
    lines = [l.strip() for l in body.split("\n") if l.strip()]

    # Each non-empty, non-subheading line in Required audits should have a status
    audit_lines = [l for l in lines if not l.startswith("#")]
    unstamped: list[str] = []
    for line in audit_lines:
        if not _AUDIT_STATUS_RE.search(line):
            unstamped.append(line[:60])

    issues: list[str] = []
    for u in unstamped:
        issues.append(
            f"Required audit missing run status: {u}"
        )
    return issues


def _check_audit_consistency(cleaned: str) -> list[str]:
    """Check Final audit status is consistent with per-audit run statuses."""
    audit_body = _section_body(cleaned, "Final audit status")
    if not audit_body:
        return []
    first_line = audit_body.split("\n")[0].strip()
    m = re.match(r"^(Pass|Partial|Fail)\b", first_line)
    if not m:
        return []
    declared = m.group(1)

    req_body = _section_body(cleaned, "Required audits")
    issues: list[str] = []

    if not req_body:
        return issues

    has_partial = bool(_AUDIT_PARTIAL_RE.search(req_body))
    has_not_run = bool(_AUDIT_NOT_RUN_RE.search(req_body))
    has_not_run_no_reason = bool(_AUDIT_NOT_RUN_NO_REASON_RE.search(req_body))

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

    if declared == "Partial":
        if has_not_run_no_reason:
            issues.append(
                "Final audit status is 'Partial' but Required audits "
                "contain not-run item(s) without documented reason — "
                "should be Fail"
            )

    if declared == "Fail":
        # Fail is appropriate when validator has errors or audits are
        # not-run without reason. If neither condition is met, suggest
        # Partial instead.
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
