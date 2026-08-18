#!/usr/bin/env python3

import argparse
import re
from collections.abc import Collection
from pathlib import Path

from audit_evidence import validate_evidence_reference, is_typed_reference
from registry_loader import (
    RegistryError,
    load_audit_registry,
    load_decision_tree_registry,
    load_route_registry,
)

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
    "## Decision tree version",
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
    """Reduce *text* to rendered Markdown content (shared sanitizer).

    Delegates to validate_contract.sanitize_visible_markdown so the pack
    validation path applies the same HTML-comment / raw-HTML-block / fence
    stripping as the contract and report declaration parsers (issue #378).
    """
    from validate_contract import sanitize_visible_markdown
    return sanitize_visible_markdown(text)

def _heading_matches(found: set[str], heading: str) -> bool:
    """Check if a heading exists in found set, accepting optional
    suffixes like ' (if applicable)'."""
    if heading in found:
        return True
    # Check for headings that start with the expected prefix
    prefix = heading + " ("
    return any(h.startswith(prefix) for h in found)


def _specialized_route_declared(cleaned: str) -> bool:
    """Return whether the primary route is a canonical specialized route."""
    primary_section = _section_body(cleaned, "Primary route")
    if not primary_section:
        return False

    route_registry = load_route_registry()
    search_ids: set[str] = set()
    for route in route_registry.routes:
        if route.category != "specialized":
            continue
        search_ids.add(route.id.lower())
        search_ids.update(alias.lower() for alias in route.aliases)

    def _strip_md(line: str) -> str:
        s = line.strip()
        s = re.sub(r"^[-*>]+\s+", "", s)
        s = re.sub(r"^\d+[.)]\s+", "", s)
        return re.sub(r"\*{1,2}([^*]+)\*{1,2}", r"\1", s)

    primary_lines = [
        _strip_md(line)
        for line in primary_section.split("\n")
        if _strip_md(line) and not _strip_md(line).lower().startswith("closest")
    ]
    primary_declared = "\n".join(primary_lines[:3]).lower()
    return any(route_id in primary_declared for route_id in search_ids)


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
        # Accept only the exact heading or the documented optional suffix
        if full == "## Tie-break rationale" or full == "## Tie-break rationale (if applicable)":
            found.add("## Tie-break rationale")

    if not _specialized_route_declared(cleaned):
        return []  # Shared-workflow or unknown — decision tree fields not needed

    # Core fields are warned here; version correctness is checked separately.
    core_fields = [
        h for h in DECISION_TREE_HEADINGS
        if h not in {"## Tie-break rationale", "## Decision tree version"}
    ]
    missing = [h for h in core_fields if h not in found]

    # Tie-break rationale: only warn if Decision tree path explicitly says
    # Step 4 was reached (not "Step 4 not reached"). Accept heading with
    # optional suffix like "## Tie-break rationale (if applicable)".
    dt_path_body = _section_body(cleaned, "Decision tree path")
    step4_reached = dt_path_body and re.search(
        r"step 4 (?:was )?reached", dt_path_body.lower()
    ) is not None
    tiebreak_found = _heading_matches(found, "## Tie-break rationale")
    if step4_reached and not tiebreak_found:
        missing.append("## Tie-break rationale")

    return missing


def _check_decision_tree_version(cleaned: str) -> list[str]:
    """Check the specialized pack's decision-tree version against the registry."""
    if not _specialized_route_declared(cleaned):
        return []
    found = {
        f"## {match.group(1).rstrip()}"
        for match in H2_RE.finditer(cleaned)
    }
    decision_tree_used = any(
        heading in found
        for heading in (
            "## Action burden",
            "## Weight-bearing object",
            "## Decision tree path",
        )
    )
    if not decision_tree_used:
        return []
    body = _section_body(cleaned, "Decision tree version")
    if not body or not body.strip():
        return ["Decision tree version is required for specialized routes"]
    match = re.fullmatch(r"\s*([0-9]+)\s*", body)
    if not match:
        return ["Decision tree version must be a single positive integer"]
    try:
        canonical_version = load_decision_tree_registry().version
    except RegistryError as exc:
        return [f"Cannot load canonical decision-tree registry: {exc}"]
    version = int(match.group(1))
    if version != canonical_version:
        return [
            f"Decision tree version {version} does not match canonical version "
            f"{canonical_version}"
        ]
    return []


def find_missing_headings(cleaned: str) -> list[str]:
    found = set()
    for m in H2_RE.finditer(cleaned):
        title = m.group(1).rstrip()
        full = f"## {title}"
        if full in REQUIRED_SET:
            found.add(full)
    return [h for h in REQUIRED_HEADINGS if h not in found]


def extract_declared_statuses(text: str) -> dict[str, str | None]:
    """Extract the optional machine-readable status sections from a pack.

    The Research Pack validator deliberately keeps these sections optional for
    backwards compatibility.  Forward evals need to observe the values without
    reimplementing Markdown heading parsing, so this small helper exposes the
    same visible-content rules used by the validator itself.
    """
    cleaned = strip_fenced_code_blocks(text)
    statuses: dict[str, str | None] = {
        "research_status": None,
        "delivery_status": None,
    }
    for heading, key in (
        ("Research status", "research_status"),
        ("Delivery status", "delivery_status"),
    ):
        body = _section_body(cleaned, heading)
        if not body:
            continue
        first_line = next((line.strip() for line in body.split("\n") if line.strip()), "")
        statuses[key] = first_line.split()[0] if first_line else None
    return statuses


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


def run_strict_checks(
    cleaned: str,
    *,
    artifact_text: str | None = None,
    evidence_base_dir: Path | None = None,
    report_text: str | None = None,
    known_validator_bindings: Collection[str] | None = None,
) -> list[str]:
    errors: list[str] = []
    warnings: list[str] = []
    errors.extend(_check_decision_tree_version(cleaned))

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

    evidence_errors, evidence_warnings = _check_audit_evidence(
        _parse_audit_statuses(cleaned),
        artifact_text=artifact_text if artifact_text is not None else cleaned,
        evidence_base_dir=evidence_base_dir,
        report_text=report_text,
        known_validator_bindings=known_validator_bindings,
    )
    errors.extend(evidence_errors)
    warnings.extend(evidence_warnings)

    # Audit consistency (Pass vs not-run/partial, Partial vs not-run-no-reason, Fail vs all-ok)
    cons_issues = _check_audit_consistency(cleaned)
    for issue in cons_issues:
        if "consider Partial" in issue:
            warnings.append(issue)
        else:
            errors.append(issue)

    # Research status validation (conditional: only validated when present)
    research_issues = _check_research_status(cleaned)
    errors.extend(research_issues)

    # Delivery status validation (conditional: only validated when present)
    delivery_issues = _check_delivery_status(cleaned)
    errors.extend(delivery_issues)

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


# ─── Strict mode: evidence and status consistency ─────────────────────────────


def _check_audit_evidence(
    records: list[dict],
    *,
    artifact_text: str,
    evidence_base_dir: Path | None,
    report_text: str | None,
    known_validator_bindings: Collection[str] | None,
) -> tuple[list[str], list[str]]:
    """Require typed, resolvable evidence for every passed pack audit."""
    errors: list[str] = []
    warnings: list[str] = []
    audit_registry = load_audit_registry()
    route_registry = load_route_registry()
    route_ids = route_registry.route_ids()
    for record in records:
        status = record.get("status")
        if status is None:
            continue
        audit_line = str(record.get("line", ""))[:100]
        audit_id = record.get("audit_id")
        audit_info = audit_registry.get_audit(str(audit_id))
        derived_secondary_id = (
            isinstance(audit_id, str)
            and audit_id.endswith("-secondary-hard-fail")
            and audit_id[: -len("-secondary-hard-fail")] in route_ids
        )
        if audit_info is None and not derived_secondary_id:
            errors.append(
                f"Required audit id {audit_id!r} is not registered in "
                "schemas/audit-registry.json"
            )
        execution_type = (
            audit_info.execution_type
            if audit_info is not None
            else "manual"
            if derived_secondary_id
            else None
        )
        if status in {"passed", "已通过"}:
            evidence = record.get("evidence")
            if not evidence:
                errors.append(
                    f"Required audit marked passed without typed evidence: "
                    f"{audit_line}"
                )
                continue

            target_text = artifact_text
            target_label = "Research Pack"
            if (
                isinstance(evidence, str)
                and evidence.startswith(("report-section:", "report-table:"))
                and report_text is not None
            ):
                target_text = report_text
                target_label = "report"
            result = validate_evidence_reference(
                evidence,
                artifact_text=target_text,
                base_dir=evidence_base_dir,
                strict=True,
                artifact_label=target_label,
                known_validator_bindings=known_validator_bindings,
                execution_type=execution_type,
            )
            errors.extend(
                f"Required audit evidence: {error}"
                for error in result.errors
            )
            warnings.extend(
                f"Required audit evidence: {warning}"
                for warning in result.warnings
            )
        elif status in {
            "skipped", "not-run", "partial", "已跳过", "未运行", "部分通过",
        }:
            if not record.get("has_reason"):
                errors.append(
                    f"Required audit status={status} requires a reason: "
                    f"{audit_line}"
                )
    return errors, warnings


# ─── Structured audit status parsing ────────────────────────────────────────────

# Extract status after em dash separator (standard format: "audit-name — STATUS")
_STATUS_EXTRACT_RE = re.compile(
    r"[–—]\s*(passed|skipped|not-run|partial|已通过|已跳过|未运行|部分通过)\b",
    re.IGNORECASE,
)

# Detect reason after status (colon followed by non-whitespace content)


def _parse_audit_statuses(cleaned: str) -> list[dict]:
    """Parse Required audits into structured status records.

    Each record: {"line": str, "status": str|None, "has_reason": bool,
    "detail": str, "evidence": str|None}.  A typed evidence reference is
    separated from the free-form reason after the status token.
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
        audit_prefix = re.split(r"\s+[–—]\s+", line, maxsplit=1)[0]
        audit_id = re.sub(r"^[-*]\s*", "", audit_prefix).strip().lower()
        audit_id = re.sub(r"\s+", "-", audit_id)
        if not m:
            records.append({
                "line": line,
                "audit_id": audit_id,
                "status": None,
                "has_reason": False,
                "detail": "",
                "evidence": None,
            })
            continue
        status = m.group(1).lower()
        raw_after = line[m.end():]
        # Preserve the existing reason grammar: a reason must be introduced
        # immediately by a colon. An em dash is reserved for the typed
        # evidence separator and must not make distant/punctuation-only text
        # look like a documented skip reason.
        has_reason = bool(re.match(
            r"\s*[:：]\s*[a-zA-Z0-9_\u4e00-\u9fff]", raw_after
        ))
        after = raw_after.strip()
        if after.startswith(("—", "–")):
            after = after[1:].strip()
        if after.startswith((":", "：")):
            after = after[1:].strip()
        evidence = after if is_typed_reference(after) else None
        records.append({
            "line": line,
            "audit_id": audit_id,
            "status": status,
            "has_reason": has_reason,
            "detail": after,
            "evidence": evidence,
        })
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


# ─── Research status and Delivery status validation ──────────────────────────


def _has_h2_section(text: str, heading: str) -> bool:
    """Check if text contains a real H2 section (## heading on its own line).

    Uses line-anchored regex to avoid false matches on body text references
    like `` `## Research status` `` or prose mentions."""
    return bool(re.search(rf"^## {re.escape(heading)}\s*$", text, re.MULTILINE))


def _count_h2_sections(text: str, heading: str) -> int:
    """Count occurrences of a real H2 section heading."""
    return len(re.findall(rf"^## {re.escape(heading)}\s*$", text, re.MULTILINE))


def _check_research_status(cleaned: str) -> list[str]:
    """Validate the ## Research status section if present.

    Conditional: section absence is not an error.
    When present, the first line must be a valid status value.
    Uses word-boundary matching (like _check_audit_status) so
    trailing comments like 'complete — verified' are accepted.

    Rejects duplicate sections — only one Research status section is allowed.
    """
    count = _count_h2_sections(cleaned, "Research status")
    if count == 0:
        return []
    if count > 1:
        return [f"Duplicate section: '## Research status' appears {count} times"]
    body = _section_body(cleaned, "Research status")
    if not body:
        return ["Research status section is present but empty"]
    first_line = body.split("\n")[0].strip()
    if not first_line:
        return ["Research status section is present but empty"]
    m = re.match(r"^(complete|partial|blocked)\b", first_line, re.IGNORECASE)
    if not m:
        return [
            f"Invalid research_status: '{first_line}'. "
            f"Must be one of: complete, partial, blocked"
        ]
    return []


def _check_delivery_status(cleaned: str) -> list[str]:
    """Validate the ## Delivery status section if present.

    Conditional: section absence is not an error.
    When present, the first line must be a valid status value.
    Uses word-boundary matching (like _check_audit_status) so
    trailing comments like 'md_ready — all checks passed' are accepted.

    Rejects duplicate sections — only one Delivery status section is allowed.
    """
    count = _count_h2_sections(cleaned, "Delivery status")
    if count == 0:
        return []
    if count > 1:
        return [f"Duplicate section: '## Delivery status' appears {count} times"]
    body = _section_body(cleaned, "Delivery status")
    if not body:
        return ["Delivery status section is present but empty"]
    first_line = body.split("\n")[0].strip()
    if not first_line:
        return ["Delivery status section is present but empty"]
    m = re.match(r"^(md_ready|pdf_ready|pdf_failed|not_run)\b", first_line, re.IGNORECASE)
    if not m:
        return [
            f"Invalid delivery_status: '{first_line}'. "
            f"Must be one of: md_ready, pdf_ready, pdf_failed, not_run"
        ]
    return []


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

    dt_version_issues = _check_decision_tree_version(cleaned)
    if dt_version_issues:
        print("Warning: Decision tree version check:")
        for issue in dt_version_issues:
            print(f"- {issue}")

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
        strict_issues = run_strict_checks(
            cleaned,
            artifact_text=cleaned,
            evidence_base_dir=Path(__file__).resolve().parent.parent,
        )
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
