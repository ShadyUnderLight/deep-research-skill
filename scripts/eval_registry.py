#!/usr/bin/env python3
"""Load and validate the executable forward-eval registry.

The historical Markdown index in ``evals/INDEX.md`` remains the human-facing
catalogue for all case files.  This module owns the smaller, structured set of
offline forward cases that can be executed end to end.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

try:  # Support both ``python scripts/foo.py`` and package-style imports.
    from registry_loader import (
        RegistryError,
        load_audit_registry,
        load_discipline_registry,
        load_route_registry,
    )
except ImportError:  # pragma: no cover - exercised only by package imports
    from .registry_loader import (  # type: ignore[no-redef]
        RegistryError,
        load_audit_registry,
        load_discipline_registry,
        load_route_registry,
    )


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY_PATH = ROOT / "evals" / "registry.json"
FORWARD_FIXTURE_DIR = ROOT / "tests" / "fixtures" / "forward"

CASE_ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]+$")
ALLOWED_CASE_STATUSES = {"active", "archived"}
ALLOWED_CASE_TYPES = {"positive", "negative"}
ALLOWED_PARALLELIZATION = {"single-track", "parallel", "not-needed"}
ALLOWED_RESEARCH_STATUSES = {"complete", "partial", "blocked"}
ALLOWED_AUDIT_STATUSES = {
    "pass",
    "conditional-pass",
    "fail",
    "partial",
    "skipped",
    "not_run",
}
ALLOWED_DELIVERY_STATUSES = {"md_ready", "pdf_ready", "pdf_failed", "not_run"}
ALLOWED_CASE_VERDICTS = {"pass", "fail"}
GAP_CLASSES = {
    "missing-rule",
    "missing-trigger",
    "execution-drift",
    "fixture-reference-drift",
}
FAILURE_FAMILY_TO_GAP_CLASS = {
    "missing-rule": "missing-rule",
    "missing-trigger": "missing-trigger",
    "route-misclassification": "missing-trigger",
    "execution-drift": "execution-drift",
    "secondary-route-not-verified": "execution-drift",
    "declared-not-executed": "execution-drift",
    "fixture-reference-drift": "fixture-reference-drift",
    "orphan-fixture": "fixture-reference-drift",
}

REQUIRED_CASE_FIELDS = {
    "id",
    "type",
    "status",
    "input",
    "expected",
    "fixtures",
    "failure_family",
    "related_rule",
    "related_validator",
}
REQUIRED_INPUT_FIELDS = {"user_prompt", "parallelization_decision"}
REQUIRED_EXPECTED_FIELDS = {
    "primary_route",
    "closest_alternative",
    "secondary_routes",
    "disciplines",
    "required_audits",
    "research_pack_fields",
    "statuses",
    "verdict",
}
REQUIRED_FIXTURE_FIELDS = {"report", "research_pack"}
ALLOWED_STATUS_KEYS = {"research_status", "audit_status", "delivery_status"}
PACK_FIELD_NAMES = {
    "Objective",
    "Decision context",
    "Primary route",
    "Action burden",
    "Weight-bearing object",
    "Decision tree path",
    "Tie-break rationale",
    "Secondary disciplines",
    "Core subquestions",
    "Stop condition",
    "Source register",
    "Claim register",
    "Uncertainty register",
    "Channel availability snapshot",
    "Artifact id",
    "Artifact contract",
    "Research status",
    "Delivery status",
    "Required audits",
    "Final audit status",
}


class EvalRegistryError(ValueError):
    """Raised when the forward-eval registry is malformed."""


def gap_class_for_failure_family(failure_family: str | None) -> str | None:
    """Map a concrete case failure family to the four diagnostic classes."""
    if not isinstance(failure_family, str):
        return None
    mapped = FAILURE_FAMILY_TO_GAP_CLASS.get(failure_family)
    return mapped if mapped in GAP_CLASSES else None


def _is_non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _as_string_list(value: Any) -> bool:
    return isinstance(value, list) and all(_is_non_empty_string(item) for item in value)


def _repo_relative_path(value: str, root: Path) -> Path | None:
    """Resolve a registry path and reject absolute paths or path traversal."""
    if not _is_non_empty_string(value):
        return None
    candidate = Path(value)
    if candidate.is_absolute():
        return None
    resolved = (root / candidate).resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError:
        return None
    return resolved


def _load_control_plane_ids() -> tuple[set[str], set[str], set[str], dict[str, list[str]]]:
    """Return canonical route, discipline, audit and route-audit IDs."""
    try:
        routes = load_route_registry()
        disciplines = load_discipline_registry()
        audits = load_audit_registry()
    except RegistryError as exc:
        raise EvalRegistryError(f"cannot load canonical control-plane registries: {exc}") from exc

    route_ids = routes.route_ids()
    discipline_ids = disciplines.discipline_ids()
    audit_ids = audits.audit_ids()
    required_audits = {route.id: route.required_audits for route in routes.routes}
    return route_ids, discipline_ids, audit_ids, required_audits


def _validate_case(
    case: Any,
    index: int,
    *,
    root: Path,
    route_ids: set[str],
    discipline_ids: set[str],
    audit_ids: set[str],
    required_audits: dict[str, list[str]],
) -> tuple[list[str], set[str]]:
    errors: list[str] = []
    referenced: set[str] = set()
    prefix = f"cases[{index}]"

    if not isinstance(case, dict):
        return [f"{prefix} must be an object"], referenced

    missing = REQUIRED_CASE_FIELDS - set(case)
    unexpected = set(case) - REQUIRED_CASE_FIELDS
    if missing:
        errors.append(f"{prefix} missing field(s): {', '.join(sorted(missing))}")
    if unexpected:
        errors.append(f"{prefix} has unexpected field(s): {', '.join(sorted(unexpected))}")
    if missing:
        return errors, referenced

    case_id = case["id"]
    if not isinstance(case_id, str) or not CASE_ID_RE.fullmatch(case_id):
        errors.append(f"{prefix}.id must be kebab-case, got {case_id!r}")

    case_type = case["type"]
    case_status = case["status"]
    if not isinstance(case_type, str) or case_type not in ALLOWED_CASE_TYPES:
        errors.append(f"{prefix}.type must be one of {sorted(ALLOWED_CASE_TYPES)}")
    if not isinstance(case_status, str) or case_status not in ALLOWED_CASE_STATUSES:
        errors.append(f"{prefix}.status must be one of {sorted(ALLOWED_CASE_STATUSES)}")
    failure_family = case["failure_family"]
    if case_type == "negative" and not _is_non_empty_string(failure_family):
        errors.append(f"{prefix}.failure_family is required for negative cases")
    if case_type == "positive" and failure_family is not None:
        errors.append(f"{prefix}.failure_family must be null for positive cases")
    if case_type == "negative" and gap_class_for_failure_family(failure_family) is None:
        errors.append(
            f"{prefix}.failure_family is not mapped to a diagnostic gap class: "
            f"{failure_family!r}"
        )

    input_data = case["input"]
    if not isinstance(input_data, dict):
        errors.append(f"{prefix}.input must be an object")
    else:
        missing_input = REQUIRED_INPUT_FIELDS - set(input_data)
        if missing_input:
            errors.append(
                f"{prefix}.input missing field(s): {', '.join(sorted(missing_input))}"
            )
        if not _is_non_empty_string(input_data.get("user_prompt")):
            errors.append(f"{prefix}.input.user_prompt must be non-empty")
        parallelization = input_data.get("parallelization_decision")
        if not isinstance(parallelization, str) or parallelization not in ALLOWED_PARALLELIZATION:
            errors.append(
                f"{prefix}.input.parallelization_decision must be one of "
                f"{sorted(ALLOWED_PARALLELIZATION)}"
            )

    expected = case["expected"]
    if not isinstance(expected, dict):
        errors.append(f"{prefix}.expected must be an object")
        expected = {}
    else:
        missing_expected = REQUIRED_EXPECTED_FIELDS - set(expected)
        unexpected_expected = set(expected) - REQUIRED_EXPECTED_FIELDS
        if missing_expected:
            errors.append(
                f"{prefix}.expected missing field(s): {', '.join(sorted(missing_expected))}"
            )
        if unexpected_expected:
            errors.append(
                f"{prefix}.expected has unexpected field(s): "
                f"{', '.join(sorted(unexpected_expected))}"
            )

    primary = expected.get("primary_route")
    if not isinstance(primary, str) or primary not in route_ids:
        errors.append(f"{prefix}.expected.primary_route is unknown: {primary!r}")
    closest = expected.get("closest_alternative")
    if closest is not None:
        if not isinstance(closest, str) or closest not in route_ids:
            errors.append(f"{prefix}.expected.closest_alternative is unknown: {closest!r}")
        elif isinstance(primary, str) and primary in route_ids:
            route_info = next(r for r in load_route_registry().routes if r.id == primary)
            if closest not in route_info.often_confused_with:
                errors.append(
                    f"{prefix}.expected.closest_alternative '{closest}' is not in "
                    f"route '{primary}' often_confused_with"
                )

    secondary = expected.get("secondary_routes")
    if not _as_string_list(secondary):
        errors.append(f"{prefix}.expected.secondary_routes must be a string list")
        secondary = []
    for route_id in secondary:
        if route_id not in route_ids:
            errors.append(f"{prefix}.expected.secondary_routes has unknown route: {route_id}")

    disciplines = expected.get("disciplines")
    if not _as_string_list(disciplines):
        errors.append(f"{prefix}.expected.disciplines must be a string list")
        disciplines = []
    for discipline_id in disciplines:
        if discipline_id not in discipline_ids:
            errors.append(
                f"{prefix}.expected.disciplines has unknown discipline: {discipline_id}"
            )

    expected_audits = expected.get("required_audits")
    if not _as_string_list(expected_audits):
        errors.append(f"{prefix}.expected.required_audits must be a string list")
        expected_audits = []
    derived_audits = {f"{route_id}-secondary-hard-fail" for route_id in secondary}
    for audit_id in expected_audits:
        if audit_id not in audit_ids and audit_id not in derived_audits:
            errors.append(f"{prefix}.expected.required_audits has unknown audit: {audit_id}")
    if isinstance(primary, str) and primary in required_audits:
        missing_required = set(required_audits[primary]) - set(expected_audits)
        if missing_required:
            errors.append(
                f"{prefix}.expected.required_audits omits primary route audit(s): "
                f"{', '.join(sorted(missing_required))}"
            )
    missing_secondary = derived_audits - set(expected_audits)
    if missing_secondary:
        errors.append(
            f"{prefix}.expected.required_audits omits secondary audit(s): "
            f"{', '.join(sorted(missing_secondary))}"
        )

    pack_fields = expected.get("research_pack_fields")
    if not _as_string_list(pack_fields):
        errors.append(f"{prefix}.expected.research_pack_fields must be a string list")
        pack_fields = []
    for field_name in pack_fields:
        if field_name not in PACK_FIELD_NAMES:
            errors.append(f"{prefix}.expected.research_pack_fields has unknown field: {field_name}")

    statuses = expected.get("statuses")
    if not isinstance(statuses, dict) or set(statuses) != ALLOWED_STATUS_KEYS:
        errors.append(
            f"{prefix}.expected.statuses must contain exactly "
            f"{sorted(ALLOWED_STATUS_KEYS)}"
        )
        statuses = {}
    if not isinstance(statuses.get("research_status"), str) or statuses.get("research_status") not in ALLOWED_RESEARCH_STATUSES:
        errors.append(f"{prefix}.expected.statuses.research_status is invalid")
    if not isinstance(statuses.get("audit_status"), str) or statuses.get("audit_status") not in ALLOWED_AUDIT_STATUSES:
        errors.append(f"{prefix}.expected.statuses.audit_status is invalid")
    if not isinstance(statuses.get("delivery_status"), str) or statuses.get("delivery_status") not in ALLOWED_DELIVERY_STATUSES:
        errors.append(f"{prefix}.expected.statuses.delivery_status is invalid")

    verdict = expected.get("verdict")
    if not isinstance(verdict, str) or verdict not in ALLOWED_CASE_VERDICTS:
        errors.append(f"{prefix}.expected.verdict must be one of {sorted(ALLOWED_CASE_VERDICTS)}")
    if case_type == "positive" and verdict != "pass":
        errors.append(f"{prefix} positive cases must expect verdict=pass")
    if case_type == "negative" and verdict != "fail":
        errors.append(f"{prefix} negative cases must expect verdict=fail")

    fixtures = case["fixtures"]
    if not isinstance(fixtures, dict):
        errors.append(f"{prefix}.fixtures must be an object")
        fixtures = {}
    else:
        missing_fixtures = REQUIRED_FIXTURE_FIELDS - set(fixtures)
        unexpected_fixtures = set(fixtures) - REQUIRED_FIXTURE_FIELDS
        if missing_fixtures:
            errors.append(
                f"{prefix}.fixtures missing field(s): {', '.join(sorted(missing_fixtures))}"
            )
        if unexpected_fixtures:
            errors.append(
                f"{prefix}.fixtures has unexpected field(s): "
                f"{', '.join(sorted(unexpected_fixtures))}"
            )
    for fixture_key in REQUIRED_FIXTURE_FIELDS:
        fixture_value = fixtures.get(fixture_key)
        fixture_path = _repo_relative_path(fixture_value, root) if isinstance(fixture_value, str) else None
        if fixture_path is None:
            errors.append(f"{prefix}.fixtures.{fixture_key} must be a repo-relative path")
            continue
        relative = fixture_path.relative_to(root).as_posix()
        referenced.add(relative)
        if not fixture_path.is_file():
            errors.append(f"{prefix}.fixtures.{fixture_key} does not exist: {relative}")

    for field in ("related_rule", "related_validator"):
        if not _as_string_list(case[field]):
            errors.append(f"{prefix}.{field} must be a non-empty string list")
        elif not case[field]:
            errors.append(f"{prefix}.{field} must not be empty")
        else:
            for reference in case[field]:
                reference_path = reference.split("#", 1)[0]
                if "/" in reference_path and reference_path.endswith((".md", ".py", ".sh", ".json")):
                    resolved_reference = _repo_relative_path(reference_path, root)
                    if resolved_reference is None or not resolved_reference.is_file():
                        errors.append(
                            f"{prefix}.{field} references missing file: {reference_path}"
                        )

    return errors, referenced


def validate_registry(data: Any, *, root: Path = ROOT) -> list[str]:
    """Return all structural and reference errors in a registry document."""
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["registry must be a JSON object"]

    required_top = {"version", "description", "last_reviewed", "cases"}
    missing_top = required_top - set(data)
    unexpected_top = set(data) - required_top
    if missing_top:
        errors.append(f"registry missing top-level field(s): {', '.join(sorted(missing_top))}")
    if unexpected_top:
        errors.append(
            f"registry has unexpected top-level field(s): {', '.join(sorted(unexpected_top))}"
        )
    if not isinstance(data.get("version"), int) or isinstance(data.get("version"), bool):
        errors.append("registry.version must be an integer")
    if not _is_non_empty_string(data.get("description")):
        errors.append("registry.description must be non-empty")
    if not _is_non_empty_string(data.get("last_reviewed")):
        errors.append("registry.last_reviewed must be non-empty")
    if not isinstance(data.get("cases"), list):
        errors.append("registry.cases must be a list")
        return errors

    try:
        route_ids, discipline_ids, audit_ids, required_audits = _load_control_plane_ids()
    except EvalRegistryError as exc:
        return errors + [str(exc)]

    seen_ids: set[str] = set()
    referenced: set[str] = set()
    for index, case in enumerate(data["cases"]):
        case_id = case.get("id") if isinstance(case, dict) else None
        if isinstance(case_id, str) and case_id in seen_ids:
            errors.append(f"cases[{index}].id is duplicated: {case_id}")
        if isinstance(case_id, str):
            seen_ids.add(case_id)
        case_errors, case_refs = _validate_case(
            case,
            index,
            root=root,
            route_ids=route_ids,
            discipline_ids=discipline_ids,
            audit_ids=audit_ids,
            required_audits=required_audits,
        )
        errors.extend(case_errors)
        referenced.update(case_refs)

    forward_dir = (root / FORWARD_FIXTURE_DIR.relative_to(ROOT)).resolve()
    if forward_dir.is_dir():
        for path in sorted(forward_dir.glob("*.md")):
            relative = path.relative_to(root.resolve()).as_posix()
            if relative not in referenced:
                errors.append(f"orphan forward fixture is not indexed: {relative}")
    return errors


def load_registry(path: Path | None = None, *, root: Path = ROOT) -> dict[str, Any]:
    """Load and strictly validate the canonical registry."""
    registry_path = path or DEFAULT_REGISTRY_PATH
    try:
        data = json.loads(registry_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise EvalRegistryError(f"registry not found: {registry_path}") from exc
    except json.JSONDecodeError as exc:
        raise EvalRegistryError(f"registry is not valid JSON: {exc}") from exc
    errors = validate_registry(data, root=root)
    if errors:
        raise EvalRegistryError("; ".join(errors))
    return data


def active_cases(registry: dict[str, Any]) -> list[dict[str, Any]]:
    """Return active cases in registry order."""
    return [case for case in registry["cases"] if case["status"] == "active"]
