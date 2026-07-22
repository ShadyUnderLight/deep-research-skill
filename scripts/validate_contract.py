#!/usr/bin/env python3
"""
Route activation contract validator.

Validates a contract (extracted from a Markdown report's ```contract fenced block)
against route-manifest.json and discipline-registry.json. Enforces the four-entity
separation: primary route, secondary routes, disciplines, and audits.

Usage:
    python3 scripts/validate_contract.py path/to/report.md [--strict]

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

# ── Paths relative to project root ──────────────────────────────────────────

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ROUTE_MANIFEST_PATH = PROJECT_ROOT / "schemas" / "route-manifest.json"
DISCIPLINE_REGISTRY_PATH = PROJECT_ROOT / "schemas" / "discipline-registry.json"

VALID_AUDIT_STATUSES = {"passed", "skipped", "not_run"}


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


# ── Registry loading ────────────────────────────────────────────────────────


def _load_route_manifest() -> dict:
    with open(ROUTE_MANIFEST_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _load_discipline_registry() -> dict:
    with open(DISCIPLINE_REGISTRY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _get_route_ids() -> set[str]:
    manifest = _load_route_manifest()
    return {r["id"] for r in manifest["routes"]}


def _get_discipline_ids() -> set[str]:
    registry = _load_discipline_registry()
    return {d["id"] for d in registry["disciplines"]}


# ── Contract extraction ─────────────────────────────────────────────────────


def has_contract_block(text: str) -> bool:
    """Check whether a ```contract fenced block exists in the text,
    regardless of whether its content is valid JSON."""
    return bool(re.search(r"```contract\s*\n", text))


def extract_contract_from_markdown(text: str) -> dict | None:
    """Extract a contract from a ```contract fenced code block in Markdown.

    Returns None if no contract block is found or if the JSON is malformed.
    """
    # Match ```contract ... ``` fenced block
    pattern = r"```contract\s*\n(.*?)```"
    match = re.search(pattern, text, re.DOTALL)
    if not match:
        return None

    json_str = match.group(1).strip()
    try:
        contract = json.loads(json_str)
        if not isinstance(contract, dict):
            return None
        return contract
    except (json.JSONDecodeError, ValueError):
        return None


# ── Validation ──────────────────────────────────────────────────────────────


def validate_contract(contract: dict) -> ContractValidationResult:
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
    """
    errors: list[str] = []
    warnings: list[str] = []

    route_ids = _get_route_ids()
    discipline_ids = _get_discipline_ids()

    # 1. Required fields
    required_fields = ["primary_route", "secondary_routes", "disciplines", "audits"]
    for field in required_fields:
        if field not in contract:
            errors.append(f"Missing required field: {field}")

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

    # 6b. Duplicate audit ID detection — only string ids
    audit_id_list_raw = [
        a.get("id", "") for a in audits if isinstance(a, dict)
    ]
    audit_id_list = [aid for aid in audit_id_list_raw if isinstance(aid, str) and aid]
    seen_audit_ids: set[str] = set()
    for aid in audit_id_list:
        if aid in seen_audit_ids:
            warnings.append(f"Duplicate audit id: '{aid}'")
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

    contract = extract_contract_from_markdown(text)
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

    result = validate_contract(contract)
    print(result.format())

    if result.errors:
        return 2
    if args.strict and result.warnings:
        return 2
    if result.warnings:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
