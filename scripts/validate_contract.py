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

    primary = contract["primary_route"]
    secondary = contract.get("secondary_routes", [])
    disciplines = contract.get("disciplines", [])
    audits = contract.get("audits", [])

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
        audit_id = audit.get("id", "(unknown)")
        status = audit.get("status", "")
        evidence = audit.get("evidence", "")

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
