#!/usr/bin/env python3
"""
Route activation contract validator.

Validates a contract (extracted from a Markdown report's ```contract fenced block)
against route-manifest.json, discipline-registry.json and audit-registry.json.
Enforces the four-entity separation: primary route, secondary routes, disciplines,
and audits, plus reference integrity (issue #376):

- audit ids must belong to audit-registry.json (or be derived
  `<secondary>-secondary-hard-fail` entries),
- `closest_alternative` must belong to the primary route's `often_confused_with`
  set in route-manifest.json,
- the primary route's `required_audits` must all be declared, without duplicates,
- stable artifact identity fields (`artifact_id`, `contract_version`,
  `created_at`) are recommended by default and required under `--strict`,
- with `--research-pack PATH`, the pack's primary route must match the
  contract's primary route.

Usage:
    python3 scripts/validate_contract.py path/to/report.md [--strict] [--research-pack path/to/pack.md]

Exit codes:
    0 = contract is valid (or no contract found)
    1 = warnings only
    2 = errors found (contract invalid)
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

from registry_loader import (
    UnknownRouteError,
    load_audit_registry,
    load_discipline_registry,
    load_route_registry,
)

# ── Paths relative to project root ──────────────────────────────────────────

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ROUTE_MANIFEST_PATH = PROJECT_ROOT / "schemas" / "route-manifest.json"
DISCIPLINE_REGISTRY_PATH = PROJECT_ROOT / "schemas" / "discipline-registry.json"
AUDIT_REGISTRY_PATH = PROJECT_ROOT / "schemas" / "audit-registry.json"

VALID_AUDIT_STATUSES = {"passed", "skipped", "not_run"}

# Recommended stable artifact identity fields (issue #376 范围 1).
ARTIFACT_META_FIELDS = ("artifact_id", "contract_version", "created_at")


# ── Data types ──────────────────────────────────────────────────────────────


@dataclass
class ContractValidationResult:
    """Result of validating a route activation contract."""

    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return len(self.errors) == 0

    def format(self) -> str:
        lines: list[str] = []
        if self.errors:
            lines.append(f"{len(self.errors)} error(s):")
            for e in self.errors:
                lines.append(f"  ✗ {e}")
        if self.warnings:
            lines.append(f"{len(self.warnings)} warning(s):")
            for w in self.warnings:
                lines.append(f"  ⚠ {w}")
        if not self.errors and not self.warnings:
            lines.append("Contract is valid.")
        return "\n".join(lines)


class ContractError(Exception):
    """Raised when a contract cannot be processed at all."""
    pass


# ── Contract extraction ─────────────────────────────────────────────────────

# Fence opener: at most 3 leading spaces (CommonMark), backtick or tilde,
# followed by an info string that MAY contain spaces (```markdown example).
# The info string's first whitespace-separated token is the language.
_FENCE_OPEN_RE = re.compile(r"^[ ]{0,3}(`{3,}|~{3,})([^\n]*)$")


def _fence_language(open_m: re.Match[str]) -> str:
    """First space/tab-separated token of a fence info string, lowercased.

    CommonMark whitespace is space/tab only: NBSP or other Unicode
    whitespace inside the info string is part of the token, so
    '```mermaid\\u00a0' has language 'mermaid\\u00a0', NOT 'mermaid'
    (issue #378).
    """
    info = open_m.group(2)
    m = re.match(r"^[ \t]*([^ \t]*)", info)
    return m.group(1).lower() if m.group(1) else ""


def _fence_open_match(line: str) -> re.Match[str] | None:
    """Match a valid fence opener.

    CommonMark: a backtick fence's info string must not contain backticks
    (a tilde fence's info string may); at most 3 leading spaces
    (issue #378).
    """
    m = _FENCE_OPEN_RE.match(line)
    if m is None:
        return None
    if m.group(1)[0] == "`" and "`" in m.group(2):
        return None
    return m


def _fence_close_re(fence_char: str, fence_len: int) -> re.Pattern[str]:
    """Closing fence: same char, >= opener length, at most 3 leading
    spaces, trailing spaces/tabs only (CommonMark fenced-code rules —
    Python \\s would also accept NBSP etc., issue #378)."""
    return re.compile(
        rf"^[ ]{{0,3}}{re.escape(fence_char)}{{{fence_len},}}[\t ]*$"
    )


def _top_level_fenced_content(text: str, language_keyword: str) -> list[str]:
    """Collect the content of every *top-level* fenced block whose opening
    fence carries *language_keyword*.

    Uses a fence state machine instead of a bare regex: a ```contract
    example nested inside another fence (e.g. inside a `````markdown
    block) is content of the outer fence, not a real declaration
    (issue #378).  An unclosed fence is NOT collected — a contract block
    must be explicitly closed to count.
    """
    blocks: list[str] = []
    lines = text.split("\n")
    i = 0
    while i < len(lines):
        open_m = _fence_open_match(lines[i])
        if not open_m:
            i += 1
            continue
        fence_char = open_m.group(1)[0]
        fence_len = len(open_m.group(1))
        language = _fence_language(open_m)
        content: list[str] = []
        j = i + 1
        close_re = _fence_close_re(fence_char, fence_len)
        while j < len(lines):
            if close_re.match(lines[j]):
                break
            content.append(lines[j])
            j += 1
        if j < len(lines) and language == language_keyword:
            blocks.append("\n".join(content))
        i = j + 1 if j < len(lines) else len(lines)
    return blocks


def has_contract_block(text: str) -> bool:
    """Check whether a top-level ```contract fenced block exists in the
    text, regardless of whether its content is valid JSON.  Nested
    examples inside other fences, declarations inside HTML comments and
    raw HTML blocks (div/pre/script/style/...) do not count (issue #378)."""
    return bool(_top_level_fenced_content(_strip_non_fence_containers(text), "contract"))


def extract_contract_blocks(text: str) -> tuple[list[dict], list[str]]:
    """Collect every top-level ```contract fenced block in *text*.

    Returns ``(contracts, errors)``.  Cardinality rule (issue #378): more
    than one contract block is structural malformation — a second block
    could carry a different route or a broken payload — so callers must
    treat ``errors`` as blocking instead of accepting the first block.
    A single malformed-JSON block is also reported as an error.  Fences
    nested inside other fences (```contract examples inside `````markdown)
    and declarations inside HTML comments / raw HTML blocks are ignored:
    only top-level contract fences count.
    """
    matches = _top_level_fenced_content(_strip_non_fence_containers(text), "contract")
    if not matches:
        return [], []
    if len(matches) > 1:
        return [], [
            f"multiple contract blocks found ({len(matches)}) — exactly "
            "one ```contract block is required (issue #378)"
        ]
    return _parse_contract_json(matches[0])


def _reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict:
    """json object_pairs_hook: duplicate object keys are malformed
    (last-write-wins would let a trailing good value hide a broken
    declaration, issue #378)."""
    result: dict = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate contract key: '{key}'")
        result[key] = value
    return result


def _parse_contract_json(json_str: str) -> tuple[list[dict], list[str]]:
    """Parse one contract JSON payload, rejecting duplicate keys."""
    try:
        contract = json.loads(json_str.strip(), object_pairs_hook=_reject_duplicate_keys)
        if not isinstance(contract, dict):
            return [], [
                "contract block JSON is not a valid object — fix the "
                "```contract fenced block"
            ]
        return [contract], []
    except (json.JSONDecodeError, ValueError) as exc:
        return [], [
            f"contract block JSON is invalid: {exc} — fix the "
            "```contract fenced block"
        ]


def extract_contract_from_markdown(text: str) -> dict | None:
    """Extract a contract from a ```contract fenced code block in Markdown.

    Returns None if no top-level contract block is found or if the JSON is
    malformed.  Duplicate blocks are handled by :func:`extract_contract_blocks`;
    this legacy accessor returns the first block for compatibility.
    """
    contracts, _ = extract_contract_blocks(text)
    return contracts[0] if contracts else None


# ── Validation ──────────────────────────────────────────────────────────────


def validate_contract(
    contract: dict,
    pack_primary_route: str | None = None,
    report_primary_route: str | None = None,
    pack_artifact_id: str | None = None,
    research_pack_provided: bool = False,
    strict: bool = False,
) -> ContractValidationResult:
    """Validate a route activation contract against the manifest and registry.

    Checks:
    1. Required top-level fields exist
    2. primary_route is a valid route id
    3. secondary_routes are valid route ids (not discipline ids)
    4. primary_route is not also in secondary_routes
    5. disciplines are valid discipline ids (not route ids)
    6. audits have valid status values
    7. passed audits have non-empty evidence
    8. shared-workflow has minimum required audits
    9. audit ids belong to audit-registry.json (or are derived
       `<secondary>-secondary-hard-fail` entries)
    10. closest_alternative belongs to the primary route's often_confused_with
    11. the primary route's required_audits are all declared, without duplicates
    12. stable artifact identity fields are present (warning; error under strict)
    13. pack primary route matches contract primary route (when provided)
    14. report status block primary route matches contract primary route
        (when provided)
    15. pack artifact id matches contract artifact_id (when both provided)

    Args:
        contract: parsed contract object.
        pack_primary_route: canonical route id declared by the Research Pack
            (resolved by the CLI). When provided and different from the
            contract's primary_route, validation fails.
        report_primary_route: canonical route id declared in the report's
            '## Route and audit status' block (resolved by the CLI). When
            provided and different from the contract's primary_route,
            validation fails.
        pack_artifact_id: stable id declared in the pack's '## Artifact id'
            section. When both this and contract['artifact_id'] are set and
            differ, validation fails; when only one side is set (and
            research_pack_provided), a warning is emitted.
        research_pack_provided: True when the CLI was given --research-pack.
            Single-side artifact id warnings are only emitted in that case
            (without --research-pack there is no pack to trace to).
        strict: when True, missing artifact identity fields are errors
            instead of warnings.
    """
    errors: list[str] = []
    warnings: list[str] = []

    route_registry = load_route_registry(ROUTE_MANIFEST_PATH)
    audit_registry = load_audit_registry(AUDIT_REGISTRY_PATH)
    route_ids = route_registry.route_ids()
    discipline_ids = load_discipline_registry(DISCIPLINE_REGISTRY_PATH).discipline_ids()
    audit_ids = audit_registry.audit_ids()

    # 1. Required fields
    required_fields = ["primary_route", "secondary_routes", "disciplines", "audits"]
    for field in required_fields:
        if field not in contract:
            errors.append(f"Missing required field: {field}")

    # 1a. Unknown top-level fields fail closed (issue #376 范围 3).
    known_fields = {
        "primary_route", "secondary_routes", "disciplines", "audits",
        "closest_alternative", "boundary_judgment",
        "artifact_id", "contract_version", "created_at",
    }
    for field in contract:
        if field not in known_fields:
            errors.append(
                f"Unknown contract field: '{field}'. "
                f"Known fields: {sorted(known_fields)}"
            )

    # If we can't validate further due to missing fields, return early
    if "primary_route" not in contract:
        return ContractValidationResult(errors=errors, warnings=warnings)

    # Guard against null values in fields that should be arrays
    secondary = contract.get("secondary_routes")
    disciplines = contract.get("disciplines")
    audits = contract.get("audits")

    if secondary is None:
        errors.append("secondary_routes is null — must be an array (use [] if empty)")
        secondary = []
    if disciplines is None:
        errors.append("disciplines is null — must be an array (use [] if empty)")
        disciplines = []
    if audits is None:
        errors.append("audits is null — must be an array (use [] if empty)")
        audits = []

    if not isinstance(secondary, list):
        errors.append(f"secondary_routes must be an array, got {type(secondary).__name__}")
        secondary = []
    if not isinstance(disciplines, list):
        errors.append(f"disciplines must be an array, got {type(disciplines).__name__}")
        disciplines = []
    if not isinstance(audits, list):
        errors.append(f"audits must be an array, got {type(audits).__name__}")
        audits = []

    primary = contract["primary_route"]

    # 1b. Primary route must be a string
    if not isinstance(primary, str):
        errors.append(
            f"primary_route must be a string, got {type(primary).__name__}: {primary!r}"
        )
        return ContractValidationResult(errors=errors, warnings=warnings)

    # 2. Primary route must be a valid route id
    if primary not in route_ids:
        errors.append(
            f"Unknown primary route '{primary}'. "
            f"Valid routes: {sorted(route_ids)}"
        )

    # 3. Secondary routes — must be valid route ids, not discipline ids
    for sr in secondary:
        if not isinstance(sr, str):
            errors.append(f"Secondary route entry is not a string: {sr}")
            continue
        if sr in discipline_ids and sr not in route_ids:
            errors.append(
                f"Secondary route '{sr}' is a discipline id, not a route id. "
                f"Disciplines belong in the 'disciplines' array."
            )
        elif sr not in route_ids:
            errors.append(
                f"Unknown secondary route '{sr}'. "
                f"Valid routes: {sorted(route_ids)}"
            )

    # 4. Primary route must not also be a secondary route
    if primary in secondary:
        errors.append(
            f"Primary route '{primary}' is also listed as a secondary route. "
            f"A route cannot be both primary and secondary in the same contract."
        )

    # 4b. Closest alternative route validation
    closest = contract.get("closest_alternative")
    if closest is not None:
        if not isinstance(closest, str):
            errors.append(
                f"closest_alternative must be a string, got {type(closest).__name__}"
            )
        elif closest not in route_ids:
            errors.append(
                f"closest_alternative '{closest}' is not a valid route id. "
                f"Valid routes: {sorted(route_ids)}"
            )
        elif closest == primary:
            errors.append(
                f"closest_alternative '{closest}' is the same as primary_route. "
                f"Closest alternative must be a different route."
            )
        elif primary in route_ids:
            # 4b2. Closest alternative must belong to the primary route's
            # often-confused boundary (issue #376 验收标准 3).
            often_confused = route_registry.get_route(primary).often_confused_with
            if closest not in often_confused:
                errors.append(
                    f"closest_alternative '{closest}' is not in route '{primary}'s "
                    f"often-confused set {sorted(often_confused)}. "
                    f"A closest alternative must be a route the primary is actually "
                    f"confused with (see route-manifest.json often_confused_with)."
                )

    # 4c. Boundary judgment — required when closest_alternative is set
    boundary = contract.get("boundary_judgment")
    if closest is not None and isinstance(closest, str) and closest in route_ids and closest != primary:
        if boundary is None:
            errors.append(
                "boundary_judgment is required when closest_alternative is set. "
                "Must include: checked_conditions (array), why_not_alternative (string), "
                "switch_conditions (string)."
            )
        elif not isinstance(boundary, dict):
            errors.append(
                f"boundary_judgment must be an object, got {type(boundary).__name__}"
            )
        else:
            # Validate each sub-field with proper type checks
            checked = boundary.get("checked_conditions")
            if not isinstance(checked, list):
                errors.append(
                    f"boundary_judgment.checked_conditions must be an array, "
                    f"got {type(checked).__name__}"
                )
            elif len(checked) == 0:
                errors.append(
                    "boundary_judgment.checked_conditions is empty. "
                    "Must list which hard-fail conditions of the alternative were checked."
                )

            why_not = boundary.get("why_not_alternative")
            if not isinstance(why_not, str):
                errors.append(
                    f"boundary_judgment.why_not_alternative must be a string, "
                    f"got {type(why_not).__name__}"
                )
            elif not why_not.strip():
                errors.append(
                    "boundary_judgment.why_not_alternative is empty. "
                    "Must explain why the alternative route's conditions don't apply."
                )

            switch = boundary.get("switch_conditions")
            if not isinstance(switch, str):
                errors.append(
                    f"boundary_judgment.switch_conditions must be a string, "
                    f"got {type(switch).__name__}"
                )
            elif not switch.strip():
                errors.append(
                    "boundary_judgment.switch_conditions is empty. "
                    "Must state under what conditions the route should be switched."
                )

    # 4c. Duplicate secondary routes detection
    seen_secondary: set[str] = set()
    for sr in secondary:
        if not isinstance(sr, str):
            continue
        if sr in seen_secondary:
            warnings.append(f"Duplicate secondary route: '{sr}'")
        seen_secondary.add(sr)

    # 5. Disciplines — must be valid discipline ids, not route ids
    for d in disciplines:
        if not isinstance(d, str):
            errors.append(f"Discipline entry is not a string: {d}")
            continue
        if d in route_ids and d not in discipline_ids:
            errors.append(
                f"Discipline '{d}' is a route id, not a discipline id. "
                f"Routes belong in 'primary_route' or 'secondary_routes'."
            )
        elif d not in discipline_ids:
            errors.append(
                f"Unknown discipline '{d}'. "
                f"Valid disciplines: {sorted(discipline_ids)}"
            )

    # 6. Audits — validate status and evidence
    for audit in audits:
        if not isinstance(audit, dict):
            errors.append(f"Audit entry is not an object: {audit}")
            continue

        # Guard against missing/malformed audit fields
        audit_id = audit.get("id")
        if not audit_id or not isinstance(audit_id, str):
            errors.append(
                f"Audit entry is missing a valid string 'id': {audit!r}"
            )
            continue

        # 6a0. Unknown audit fields fail closed (issue #376 范围 3).
        known_audit_fields = {"id", "status", "evidence"}
        for afield in audit:
            if afield not in known_audit_fields:
                errors.append(
                    f"Audit '{audit_id}' has unknown field '{afield}'. "
                    f"Known audit fields: {sorted(known_audit_fields)}"
                )

        # 6a. Audit id must belong to the audit registry, or be a derived
        # `<secondary>-secondary-hard-fail` entry for a declared secondary
        # route (issue #376 验收标准 2).
        derived_prefixes = {
            sr for sr in secondary if isinstance(sr, str)
        }
        is_derived_hard_fail = (
            audit_id.endswith("-secondary-hard-fail")
            and audit_id[: -len("-secondary-hard-fail")] in derived_prefixes
        )
        if audit_id not in audit_ids and not is_derived_hard_fail:
            errors.append(
                f"Audit '{audit_id}' is not in the audit registry "
                f"(schemas/audit-registry.json). Valid audit ids: "
                f"{sorted(audit_ids)}"
            )

        status = audit.get("status", "")
        if not isinstance(status, str):
            status = ""

        evidence = audit.get("evidence", "")
        if not isinstance(evidence, str):
            errors.append(
                f"Audit '{audit_id}' evidence must be a string, "
                f"got {type(evidence).__name__}"
            )
            evidence = ""

        if status not in VALID_AUDIT_STATUSES:
            errors.append(
                f"Audit '{audit_id}' has invalid status '{status}'. "
                f"Must be one of: {sorted(VALID_AUDIT_STATUSES)}"
            )

        # Passed audits must have non-empty evidence
        if status == "passed" and (not evidence or not evidence.strip()):
            errors.append(
                f"Audit '{audit_id}' is marked 'passed' but has empty evidence. "
                f"Evidence must reference a concrete location in the artifact."
            )

    # 6b. Duplicate audit ID detection — duplicate ids are an error
    # (issue #376 验收标准 4).
    audit_id_list_raw = [
        a.get("id", "") for a in audits if isinstance(a, dict)
    ]
    audit_id_list = [aid for aid in audit_id_list_raw if isinstance(aid, str) and aid]
    seen_audit_ids: set[str] = set()
    for aid in audit_id_list:
        if aid in seen_audit_ids:
            errors.append(f"Duplicate audit id: '{aid}'")
        seen_audit_ids.add(aid)

    # 6c. Secondary route hard-fail audit enforcement
    # Each declared secondary route must have a corresponding audit entry
    # with status="passed" whose id contains the secondary route name.
    # (e.g., "regulatory-analysis-secondary-hard-fail")
    if secondary:
        # Build map: audit_id -> status for all valid audit entries
        audit_status_map: dict[str, str] = {}
        for a in audits:
            if not isinstance(a, dict):
                continue
            aid = a.get("id", "")
            if isinstance(aid, str) and aid:
                st = a.get("status", "")
                audit_status_map[aid] = st if isinstance(st, str) else ""

        for sr in secondary:
            if not isinstance(sr, str):
                continue
            # Find audits whose id contains the secondary route name
            matching = [
                (aid, st) for aid, st in audit_status_map.items()
                if sr in aid
            ]
            passed = [(aid, st) for aid, st in matching if st == "passed"]
            not_passed = [(aid, st) for aid, st in matching if st != "passed"]

            if not passed:
                if not_passed:
                    errors.append(
                        f"Secondary route '{sr}' has audit tracking but none with "
                        f"status='passed' (found: {[aid for aid, _ in not_passed]} "
                        f"with statuses {[st for _, st in not_passed]}). "
                        f"Hard-fail verification must be independently executed."
                    )
                else:
                    errors.append(
                        f"Secondary route '{sr}' has no hard-fail audit tracking. "
                        f"Add an audit entry with status='passed' whose id contains "
                        f"'{sr}' (e.g., '{sr}-secondary-hard-fail')."
                    )
            elif not_passed:
                warnings.append(
                    f"Secondary route '{sr}' has passed tracking "
                    f"({[aid for aid, _ in passed]}) but also non-passed "
                    f"entries ({[aid for aid, _ in not_passed]}). "
                    f"All hard-fail tracking entries should be 'passed'."
                )

    # 7. Shared-workflow must have at least workflow-spine-audit or final-audit
    if primary == "shared-workflow":
        audit_ids = {a.get("id", "") for a in audits if isinstance(a, dict)}
        required = {"workflow-spine-audit", "final-audit"}
        if not (audit_ids & required):
            errors.append(
                f"Shared-workflow contract must include at least one of: {sorted(required)}. "
                f"Found audits: {sorted(audit_ids)}"
            )
        elif audit_ids & required and len(audit_ids) > 3:
            warnings.append(
                f"Shared-workflow has {len(audit_ids)} audits (unusually many). "
                f"Consider if a specialized route is more appropriate."
            )

    # 8. Structure warnings (non-blocking)
    if len(secondary) > 2:
        warnings.append(
            f"Contract has {len(secondary)} secondary routes. "
            f"Consider reducing to ≤2 for clearer scope focus."
        )

    if not audits:
        warnings.append("Contract has no audits. This is unusual — most tasks "
                        "should run at least final-audit.")

    # 9. Primary route's required_audits must all be declared
    # (issue #376 验收标准 4). Missing required audits are errors.
    if primary in route_ids:
        required_for_route = route_registry.get_route(primary).required_audits
        declared = {aid for aid in audit_id_list}
        missing_required = [aid for aid in required_for_route if aid not in declared]
        if missing_required:
            errors.append(
                f"Primary route '{primary}' requires audits "
                f"{sorted(required_for_route)} but these are not declared: "
                f"{sorted(missing_required)}"
            )

    # 10. Stable artifact identity fields (issue #376 范围 1).
    # Non-string values are always errors; missing/empty values are
    # warnings by default and errors under strict.
    for meta_field in ARTIFACT_META_FIELDS:
        value = contract.get(meta_field)
        if value is not None and not isinstance(value, str):
            errors.append(
                f"Contract field '{meta_field}' must be a string, "
                f"got {type(value).__name__}"
            )
    missing_meta = [f for f in ARTIFACT_META_FIELDS if not contract.get(f)]
    if missing_meta:
        message = (
            "Contract lacks stable artifact identity fields: "
            f"{', '.join(sorted(missing_meta))}. "
            "Add artifact_id, contract_version and created_at so the report "
            "can be referenced by the Research Pack and future audit runs "
            "(required under --strict)."
        )
        if strict:
            errors.append(message)
        else:
            warnings.append(message)

    # 11. Pack primary route must match contract primary route
    # (issue #376 验收标准 5).
    if pack_primary_route is not None and pack_primary_route != primary:
        errors.append(
            f"Primary route mismatch: Research Pack declares "
            f"'{pack_primary_route}' but contract declares '{primary}'. "
            f"Pack and contract must agree on the canonical route."
        )

    # 12. Report status block route must match contract primary route
    # (issue #376 验收标准 5 — route declared in the report body).
    if report_primary_route is not None and report_primary_route != primary:
        errors.append(
            f"Primary route mismatch: report 'Route and audit status' block "
            f"declares '{report_primary_route}' but contract declares "
            f"'{primary}'. Status block and contract must agree on the "
            f"canonical route."
        )

    # 13. Pack artifact id must match contract artifact_id when both are set
    # (issue #376 验收标准 1 — 报告/pack 互指). Single-side warnings only
    # when --research-pack was explicitly provided.
    contract_artifact_id = contract.get("artifact_id")
    if not research_pack_provided:
        pass
    elif pack_artifact_id is not None and contract_artifact_id:
        if pack_artifact_id != contract_artifact_id:
            errors.append(
                f"Artifact id mismatch: Research Pack declares "
                f"'{pack_artifact_id}' but contract declares "
                f"'{contract_artifact_id}'. Pack and contract must reference "
                f"the same artifact."
            )
    elif pack_artifact_id is not None and not contract_artifact_id:
        warnings.append(
            f"Research Pack declares artifact id '{pack_artifact_id}' but "
            "contract has no artifact_id — the report cannot be traced back "
            "to the pack."
        )
    elif contract_artifact_id and pack_artifact_id is None:
        warnings.append(
            f"Contract declares artifact id '{contract_artifact_id}' but the "
            "Research Pack has no '## Artifact id' section — the pack cannot "
            "be traced to the report."
        )

    return ContractValidationResult(errors=errors, warnings=warnings)


# ── CLI ─────────────────────────────────────────────────────────────────────


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate route activation contract in a Markdown report.",
    )
    parser.add_argument(
        "path",
        type=str,
        help="Path to the Markdown report file",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as errors (exit code 2)",
    )
    parser.add_argument(
        "--require-contract",
        action="store_true",
        help="Treat missing contract block as an error (exit code 2). "
             "Use in CI to enforce contract presence.",
    )
    parser.add_argument(
        "--research-pack",
        type=str,
        default=None,
        metavar="PATH",
        help="Path to a Research Pack .md file. Cross-checks that the pack's "
             "primary route matches the contract's primary route (exit code 2 "
             "on mismatch).",
    )
    args = parser.parse_args(argv)

    path = Path(args.path)
    if not path.is_file():
        print(f"Error: {path} is not a file", file=sys.stderr)
        return 2

    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except (OSError, UnicodeError) as exc:
        print(f"Error: cannot read {path}: {exc}", file=sys.stderr)
        return 2

    contract_blocks, contract_errors = extract_contract_blocks(text)
    if contract_errors:
        for err in contract_errors:
            print(f"Error: {err}", file=sys.stderr)
        return 2
    contract = contract_blocks[0] if contract_blocks else None
    if contract is None:
        if has_contract_block(text):
            # A ```contract block exists but JSON is malformed — always an error.
            # A declared contract that can't be parsed is a broken contract,
            # not a missing one. Fail-closed.
            print(
                f"Error: Contract block found in {path} but JSON is malformed "
                f"or not a valid object. Fix the ```contract fenced block."
            )
            return 2
        if args.require_contract:
            print(f"Error: No contract block found in {path} (--require-contract set).")
            return 2
        print(f"No contract block found in {path}. Skipping validation.")
        return 0

    pack_primary_route: str | None = None
    pack_artifact_id: str | None = None
    if args.research_pack:
        pack_section_errors = validate_pack_sections(args.research_pack)
        if pack_section_errors:
            for err in pack_section_errors:
                print(f"Error: {err}", file=sys.stderr)
            return 2
        pack_primary_route = _resolve_pack_primary_route(args.research_pack)
        if pack_primary_route is None:
            return 2
        pack_artifact_id = _extract_pack_artifact_id(args.research_pack)

    # Report status block route (issue #376 验收标准 5 — 三方一致性).
    report_primary_route, route_malformed = extract_report_route_declaration(text)
    if route_malformed:
        for err in route_malformed:
            print(f"Error: {err}", file=sys.stderr)
        return 2

    result = validate_contract(
        contract,
        pack_primary_route=pack_primary_route,
        report_primary_route=report_primary_route,
        pack_artifact_id=pack_artifact_id,
        research_pack_provided=args.research_pack is not None,
        strict=args.strict,
    )
    print(result.format())

    if result.errors:
        return 2
    if args.strict and result.warnings:
        return 2
    if result.warnings:
        return 1
    return 0


def _count_pack_sections(text: str, heading: str) -> int:
    """Number of visible (non-fenced) occurrences of a pack heading."""
    cleaned = _strip_fences(text)
    return len(re.findall(
        rf"^##\s+{re.escape(heading)}\s*$", cleaned, re.MULTILINE
    ))


def validate_pack_sections(pack_path: str) -> list[str]:
    """Cardinality check for pack declarations (issue #378).

    '## Primary route' and '## Artifact id' must each appear at most once;
    a second conflicting declaration would silently bypass the
    pack/contract cross-check if only the first section were read.
    Returns structural errors (empty list when well-formed).
    """
    try:
        text = Path(pack_path).read_text(encoding="utf-8", errors="replace")
    except (OSError, UnicodeError) as exc:
        return [f"cannot read pack {pack_path}: {exc}"]
    errors: list[str] = []
    for heading in ("Primary route", "Artifact id"):
        count = _count_pack_sections(text, heading)
        if count > 1:
            errors.append(
                f"Research Pack {pack_path} declares '## {heading}' "
                f"{count} times — exactly one is required (issue #378)"
            )
    return errors


def _resolve_pack_primary_route(pack_path: str) -> str | None:
    """Resolve the canonical route id declared in a Research Pack's
    '## Primary route' section. Returns None (after reporting) when the
    pack cannot be read or the route cannot be resolved."""
    pack = Path(pack_path)
    if not pack.is_file():
        print(f"Error: --research-pack file not found: {pack_path}", file=sys.stderr)
        return None

    try:
        text = pack.read_text(encoding="utf-8", errors="replace")
    except (OSError, UnicodeError) as exc:
        print(f"Error: cannot read --research-pack {pack_path}: {exc}", file=sys.stderr)
        return None

    # Fenced declarations (e.g. a route inside ~~~markdown) do not count
    # as visible pack sections (issue #378).
    text = _strip_fences(text)

    match = re.search(
        r"## Primary route\s*\n(.*?)(?=\n## |\Z)", text, re.DOTALL
    )
    if not match:
        print(
            f"Error: Research Pack {pack_path} has no '## Primary route' section.",
            file=sys.stderr,
        )
        return None

    # First non-empty line that is not "Closest alternative:" prose.
    lines = [
        l.strip() for l in match.group(1).split("\n")
        if l.strip() and not l.strip().lower().startswith("closest")
    ]
    if not lines:
        print(
            f"Error: Research Pack {pack_path} '## Primary route' section is empty.",
            file=sys.stderr,
        )
        return None

    raw = lines[0]
    # Strip list markers / bold / italic so display-name forms resolve.
    raw = re.sub(r"^[-*>]+\s+", "", raw)
    raw = re.sub(r"^\d+[.)]\s+", "", raw)
    raw = re.sub(r"\*{1,2}([^*]+)\*{1,2}", r"\1", raw)

    try:
        return load_route_registry(ROUTE_MANIFEST_PATH).resolve_route(raw)
    except UnknownRouteError as exc:
        print(f"Error: cannot resolve pack primary route: {exc}", file=sys.stderr)
        return None


_HTML_COMMENT_RE = re.compile(r"<!--.*?(?:-->|\Z)", re.DOTALL)

# CommonMark type-6 block tag list (spec 0.31.2).  Note: source/template
# are NOT in the spec list and must not be treated as block tags.
_HTML_BLOCK_TAGS = (
    "address", "article", "aside", "base", "basefont", "blockquote",
    "body", "caption", "center", "col", "colgroup", "dd", "details",
    "dialog", "dir", "div", "dl", "dt", "fieldset", "figcaption",
    "figure", "footer", "form", "frame", "frameset",
    "h1", "h2", "h3", "h4", "h5", "h6",
    "head", "header", "hr", "html", "iframe", "legend", "li", "link",
    "main", "menu", "menuitem", "nav", "noframes", "ol", "optgroup",
    "option", "p", "param", "search", "section", "summary",
    "table", "tbody", "td", "tfoot", "th", "thead", "title", "tr",
    "track", "ul",
)

# CommonMark type-1 block tags: the block runs until the matching closing
# tag line — blank lines do NOT terminate it (issue #378).
_HTML_TYPE1_TAGS = ("script", "pre", "style", "textarea")

# Tag boundary: after the tag name only space/tab, '>', the complete
# '/>' pair or EOL are allowed.  A lone '/' (as in '<div/foo' or
# '<div/ foo') is NOT a valid suffix — only the full '/>' sequence
# (spec 0.31.2, issue #378).
_TAG_BOUNDARY = r"(?=/>|[\t >]|$)"

_HTML_TYPE1_OPEN_RE = re.compile(
    rf"^[ ]{{0,3}}<({'|'.join(_HTML_TYPE1_TAGS)}){_TAG_BOUNDARY}", re.IGNORECASE
)
_HTML_BLOCK_OPEN_RE = re.compile(
    rf"^[ ]{{0,3}}<({'|'.join(_HTML_BLOCK_TAGS)}){_TAG_BOUNDARY}", re.IGNORECASE
)
# Matches an incomplete allowlist opener too ('<search' without '>'):
# type-6 start condition is conservative so forged declarations after an
# unclosed tag opener fail closed (issue #378).
_HTML_BLOCK_OPEN_ANY_RE = re.compile(
    rf"^[ ]{{0,3}}<({'|'.join(_HTML_BLOCK_TAGS)}){_TAG_BOUNDARY}", re.IGNORECASE
)
# Type-6 closing tag: '</tag' followed by space/tab, '>' or EOL (an
# incomplete closing tag also starts the block, spec 0.31.2).
_HTML_BLOCK_CLOSE_RE = re.compile(
    rf"^[ ]{{0,3}}</({'|'.join(_HTML_BLOCK_TAGS)}){_TAG_BOUNDARY}", re.IGNORECASE
)


def _match_complete_open_tag(line: str) -> re.Match[str] | None:
    """Match a complete open tag at line start (type-7 start condition).

    Quote-aware: a '>' inside a quoted attribute value is part of the
    attribute.  After the closing '>' only spaces/tabs may follow to the
    end of the line (spec 0.31.2, issue #378).
    """
    m = re.match(rf"^[ ]{{0,3}}<([a-zA-Z][a-zA-Z0-9-]*){_TAG_BOUNDARY}", line)
    if m is None:
        return None
    i = m.end()
    quote: str | None = None
    while i < len(line):
        ch = line[i]
        if quote is not None:
            if ch == quote:
                quote = None
        elif ch in "\"'":
            quote = ch
        elif ch == ">":
            if re.match(r"^[\t ]*$", line[i + 1:]):
                return m
            return None
        i += 1
    return None


def _continues_paragraph(line: str) -> bool:
    """True if a top-level line continues an open paragraph.

    Used for the CommonMark type-7 start condition: type-7 HTML blocks
    cannot interrupt an open paragraph.  Block starts — blank lines,
    headings, lists, blockquotes, fences, thematic breaks / setext
    underlines, indented code — end the paragraph; everything else
    (including inline HTML tags like <span>) continues it (issue #378).
    Takes the RAW line (leading spaces matter for indented code).
    """
    stripped = line.strip()
    if not stripped:
        return False
    if re.match(
        r"^(#{1,6}[\t ]|>|[-+*][\t ]|\d+[.)][\t ]|`{3,}|~{3,})",
        stripped,
    ):
        return False
    # Thematic break / setext underline (---, ***, ___, - - -, ===).
    if re.match(r"^[-*_](?:[\t ]*[-*_]){2,}[\t ]*$", stripped):
        return False
    if re.match(r"^=+[\t ]*$", stripped):
        return False
    # Indented code (4+ leading spaces): starts a block.  (In a real
    # CommonMark parser an indented line after a paragraph is a lazy
    # continuation, but treating it as a block boundary is the
    # fail-closed direction for the type-7 gate — issue #378.)
    if re.match(r"^[ ]{4,}\S", line):
        return False
    # HTML tag line: block tags (types 1/6) interrupt the paragraph;
    # inline tags (<span>, </span>, <a href=...>) continue it.
    m = re.match(r"^</?([a-zA-Z][a-zA-Z0-9-]*)", stripped)
    if m is not None:
        tag = m.group(1).lower()
        return tag not in _HTML_TYPE1_TAGS and tag not in _HTML_BLOCK_TAGS
    return True


def _sanitize_visible_lines(
    lines: list[str],
    *,
    keep_mermaid: bool = False,
    blank: bool = False,
    keep_fences: bool = False,
) -> list[str]:
    """Single-pass rendered-content sanitizer state machine.

    Fences, HTML comments and raw HTML blocks (CommonMark types
    1/3/4/5/6/7) are recognized in ONE pass: inside a fence, HTML-looking
    lines are code content and never start an HTML block (fenced-code
    rules, issue #378).

    Modes:
    - blank=False (default): non-visible content is dropped.
    - blank=True: non-visible content becomes empty lines (line numbers
      preserved; used by validators that report original line numbers).
    - keep_mermaid=True: mermaid fences and their content are kept
      (figure entities, used by the figure-reference validator).
    - keep_fences=True: all fenced content is kept (used before contract
      extraction so the ```contract fence itself survives).
    """
    out: list[str] = []
    state: str | None = None  # fence/comment/t1:<tag>/raw/cdata/pi/decl
    fence_char = ""
    fence_len = 0
    t1_tag = ""
    mermaid = False
    in_paragraph = False

    def emit(line: str, visible: bool) -> None:
        if visible or not blank:
            out.append(line if visible else "")
        elif blank:
            out.append("")

    for line in lines:
        stripped = line.strip()
        if state == "fence":
            if _fence_close_re(fence_char, fence_len).match(line):
                state = None
            if keep_fences or (keep_mermaid and mermaid):
                out.append(line)
            elif blank:
                out.append("")
            continue
        if state == "comment":
            if "-->" in stripped:
                state = None
            if blank:
                out.append("")
            continue
        if state is not None and state.startswith("t1:"):
            tag = state[3:]
            if re.search(rf"</{tag}\s*>", stripped, re.IGNORECASE):
                state = None
            if blank:
                out.append("")
            continue
        if state in ("cdata", "pi", "decl", "raw"):
            if state == "cdata" and "]]>" in stripped:
                state = None
            elif state == "pi" and "?>" in stripped:
                state = None
            elif state == "decl" and ">" in stripped:
                state = None
            elif state == "raw" and line.strip(" \t") == "":
                # Blank line (spaces/tabs only) ends a type-6/7 block;
                # NBSP etc. is content, not blankness (issue #378).
                state = None
                if blank:
                    out.append(line)
                continue
            if blank:
                out.append("")
            continue
        # ── top level ────────────────────────────────────────────────
        fm = _fence_open_match(line)
        if fm:
            fence_char = fm.group(1)[0]
            fence_len = len(fm.group(1))
            lang = _fence_language(fm)
            mermaid = keep_mermaid and lang == "mermaid"
            state = "fence"
            in_paragraph = False  # a fence interrupts an open paragraph
            if keep_fences or (keep_mermaid and mermaid):
                out.append(line)
            elif blank:
                out.append("")
            continue
        # ── HTML containers (≤3 leading spaces; 4-space indented content
        #    is an indented code block, not raw HTML, issue #378) ──
        if re.match(r"^[ ]{0,3}<!--", line):
            if "-->" in stripped:
                continue
            state = "comment"
            in_paragraph = False
            if blank:
                out.append("")
            continue
        if re.match(r"^[ ]{0,3}<!\[CDATA\[", line):
            if "]]>" in stripped:
                continue
            state = "cdata"
            in_paragraph = False
            if blank:
                out.append("")
            continue
        if re.match(r"^[ ]{0,3}<\?", line):
            if "?>" in stripped:
                continue
            state = "pi"
            in_paragraph = False
            if blank:
                out.append("")
            continue
        if re.match(r"^[ ]{0,3}<![A-Za-z]", line):
            # Type 4: '<!' must be followed by an ASCII letter.
            if ">" in stripped:
                continue
            state = "decl"
            in_paragraph = False
            if blank:
                out.append("")
            continue
        m1 = _HTML_TYPE1_OPEN_RE.match(line)
        if m1:
            tag = m1.group(1).lower()
            if re.search(rf"</{tag}\s*>", stripped, re.IGNORECASE):
                continue  # same-line close ends the type-1 block
            state = "t1:" + tag
            in_paragraph = False
            if blank:
                out.append("")
            continue
        if _HTML_BLOCK_OPEN_ANY_RE.match(line):
            state = "raw"
            in_paragraph = False
            if blank:
                out.append("")
            continue
        if _HTML_BLOCK_CLOSE_RE.match(line):
            # Type-6 closing tag (may be incomplete: '</div' + EOL).
            state = "raw"
            in_paragraph = False
            if blank:
                out.append("")
            continue
        # Type 7 cannot interrupt an open paragraph (CommonMark).
        if not in_paragraph:
            if _match_complete_open_tag(line) is not None:
                state = "raw"
                in_paragraph = False
                if blank:
                    out.append("")
                continue
            if re.match(r"^[ ]{0,3}</([a-zA-Z][a-zA-Z0-9-]*)\s*>(?:[\t ]*$)", line):
                # Type 7 closing tag: complete tag followed only by
                # spaces/tabs to the end of the line.
                state = "raw"
                in_paragraph = False
                if blank:
                    out.append("")
                continue
        out.append(line)
        # Track paragraph context (type-7 start condition).
        in_paragraph = _continues_paragraph(line)
    return out


def sanitize_visible_markdown(text: str) -> str:
    """Reduce *text* to rendered Markdown content.

    Single-pass sanitizer: HTML comments, raw HTML blocks and fenced code
    blocks are removed; inside a fence, HTML-looking lines are code and
    never start an HTML block.  Whatever remains is what a CommonMark
    renderer would parse as Markdown structure (issue #378).  Shared by
    the contract/report/pack declaration parsers and validators.
    """
    return "\n".join(_sanitize_visible_lines(text.split("\n")))


def _strip_non_fence_containers(text: str) -> str:
    """Strip HTML comments and raw HTML blocks but keep fenced code.

    Used before contract extraction: the ```contract fence itself must
    survive for parsing, while declarations inside <div> or <!-- --> must
    not count (issue #378).
    """
    return "\n".join(
        _sanitize_visible_lines(text.split("\n"), keep_fences=True)
    )


def _strip_fences(text: str) -> str:
    """Legacy alias for :func:`sanitize_visible_markdown`."""
    return sanitize_visible_markdown(text)
def count_report_route_blocks(text: str) -> int:
    """Number of visible (non-fenced) '## Route and audit status' blocks."""
    cleaned = _strip_fences(text)
    return len(re.findall(
        r"^#{2,3}\s+.*(?:Route\s+and\s+audit\s+status|路由与审计状态)",
        cleaned,
        re.MULTILINE | re.IGNORECASE,
    ))


def extract_report_route_declaration(text: str) -> tuple[str | None, list[str]]:
    """Resolve the canonical route declared in the report's
    '## Route and audit status' block (e.g. '**Primary route**: Market
    Outlook' or '**Route**: Shared-workflow').

    Returns ``(route, malformed)``.  Cardinality rule (issue #378): more
    than one route declaration line in the block is structural
    malformation — the first declaration must not win.  Fenced code blocks
    are stripped first so a fake declaration inside a ```markdown block
    can never override the visible status block.
    """
    cleaned = _strip_fences(text)
    match = re.search(
        r"## Route and audit status\s*\n(.*?)(?=\n## |\Z)", cleaned, re.DOTALL
    )
    if not match:
        return None, []
    block = match.group(1)

    declarations: list[str] = []
    for line in block.split("\n"):
        m = re.match(
            r"\*\*Primary\s+route\*\*\s*[:：]\s*(.+)$", line.strip(), re.IGNORECASE
        )
        if m:
            declarations.append(m.group(1).strip())
            continue
        m = re.match(r"\*\*Route\*\*\s*[:：]\s*(.+)$", line.strip(), re.IGNORECASE)
        if m:
            declarations.append(m.group(1).strip())

    if not declarations:
        return None, []
    if len(declarations) > 1:
        return None, [
            f"multiple route declarations found in the 'Route and audit "
            f"status' block ({len(declarations)}) — exactly one is "
            "required (issue #378)"
        ]
    raw = declarations[0]

    # Strip trailing parenthetical notes, list markers, bold/italic.
    raw = re.sub(r"\s*\([^)]*\)\s*$", "", raw)
    raw = re.sub(r"^[-*>]+\s+", "", raw)
    raw = re.sub(r"\*{1,2}([^*]+)\*{1,2}", r"\1", raw)
    try:
        return load_route_registry(ROUTE_MANIFEST_PATH).resolve_route(raw), []
    except UnknownRouteError:
        # Unknown status-block routes are reported by other validators
        # (audit_report route detection); don't fail the contract check.
        return None, []


def extract_report_primary_route(text: str) -> str | None:
    """Legacy accessor for the report's declared primary route.

    See :func:`extract_report_route_declaration` for the cardinality-aware
    version with structured malformed errors.
    """
    route, _ = extract_report_route_declaration(text)
    return route


def _extract_pack_artifact_id(pack_path: str) -> str | None:
    """Extract the first line of the pack's '## Artifact id' section.
    Returns None when the section is absent (single-side tracing → warning).
    Fenced declarations do not count (issue #378)."""
    try:
        text = Path(pack_path).read_text(encoding="utf-8", errors="replace")
    except (OSError, UnicodeError):
        return None
    text = _strip_fences(text)
    match = re.search(
        r"## Artifact id\s*\n(.+?)(?=\n## |\Z)", text, re.DOTALL
    )
    if not match:
        return None
    for line in match.group(1).split("\n"):
        line = line.strip()
        if not line:
            continue
        line = re.sub(r"^[-*>]+\s+", "", line)
        line = re.sub(r"\*{1,2}([^*]+)\*{1,2}", r"\1", line)
        return line or None
    return None


if __name__ == "__main__":
    raise SystemExit(main())
