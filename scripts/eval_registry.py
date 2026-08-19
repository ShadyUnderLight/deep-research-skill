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
        load_decision_tree_registry,
        load_discipline_registry,
        load_route_registry,
    )
except ImportError:  # pragma: no cover - exercised only by package imports
    from .registry_loader import (  # type: ignore[no-redef]
        RegistryError,
        load_audit_registry,
        load_decision_tree_registry,
        load_discipline_registry,
        load_route_registry,
    )
try:
    from route_activation import ALLOWED_PARALLELIZATION
except ImportError:  # pragma: no cover - package import fallback
    from .route_activation import ALLOWED_PARALLELIZATION  # type: ignore[no-redef]


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY_PATH = ROOT / "evals" / "registry.json"
FORWARD_FIXTURE_DIR = ROOT / "tests" / "fixtures" / "forward"

CASE_ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]+$")
ALLOWED_CASE_STATUSES = {"active", "archived"}
ALLOWED_CASE_TYPES = {"positive", "negative"}
ALLOWED_EVALUATION_MODES = {
    "structured-decision-replay",
    "activation-record-integration",
    "agent-prompt",
}
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
FAILURE_FAMILY_TO_STAGE = {
    "route-misclassification": "contract",
    "secondary-route-not-verified": "audit",
    "declared-not-executed": "evidence",
    "audit-failure": "audit",
}

REQUIRED_CASE_FIELDS = {
    "id",
    "type",
    "status",
    "evaluation_mode",
    "input",
    "expected",
    "fixtures",
    "failure_family",
    "related_rule",
    "related_validator",
}
REQUIRED_INPUT_FIELDS = {
    "user_prompt",
    "prompt_sha256",
    "action_burden",
    "weight_bearing_object",
    "secondary_routes",
    "parallelization_decision",
}
REQUIRED_EXPECTED_FIELDS = {
    "primary_route",
    "closest_alternative",
    "secondary_routes",
    "disciplines",
    "required_audits",
    "research_pack_fields",
    "statuses",
    "verdict",
    "parallelization_decision",
}
OPTIONAL_EXPECTED_FIELDS = {"failure_stage"}
REQUIRED_FIXTURE_FIELDS = {"report", "research_pack"}
OPTIONAL_FIXTURE_FIELDS = {"activation_snapshot"}
ALLOWED_STATUS_KEYS = {"research_status", "audit_status", "delivery_status"}
PACK_FIELD_NAMES = {
    "Objective",
    "Decision context",
    "Primary route",
    "Action burden",
    "Weight-bearing object",
    "Decision tree path",
    "Decision tree version",
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


def failure_stage_for_failure_family(failure_family: str | None) -> str | None:
    """Map a concrete failure family to its observable control-plane stage."""
    if not isinstance(failure_family, str):
        return None
    return FAILURE_FAMILY_TO_STAGE.get(failure_family)


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


def _load_control_plane_ids() -> tuple[
    set[str], set[str], set[str], dict[str, list[str]], Any
]:
    """Return canonical ids plus the structured decision-tree registry."""
    try:
        routes = load_route_registry()
        disciplines = load_discipline_registry()
        audits = load_audit_registry()
        decision_tree = load_decision_tree_registry(route_registry=routes)
    except RegistryError as exc:
        raise EvalRegistryError(f"cannot load canonical control-plane registries: {exc}") from exc

    route_ids = routes.route_ids()
    discipline_ids = disciplines.discipline_ids()
    audit_ids = audits.audit_ids()
    required_audits = {route.id: route.required_audits for route in routes.routes}
    return route_ids, discipline_ids, audit_ids, required_audits, decision_tree


def _validate_case(
    case: Any,
    index: int,
    *,
    root: Path,
    route_ids: set[str],
    discipline_ids: set[str],
    audit_ids: set[str],
    required_audits: dict[str, list[str]],
    decision_tree: Any,
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
    evaluation_mode = case["evaluation_mode"]
    if not isinstance(case_type, str) or case_type not in ALLOWED_CASE_TYPES:
        errors.append(f"{prefix}.type must be one of {sorted(ALLOWED_CASE_TYPES)}")
    if not isinstance(case_status, str) or case_status not in ALLOWED_CASE_STATUSES:
        errors.append(f"{prefix}.status must be one of {sorted(ALLOWED_CASE_STATUSES)}")
    if not isinstance(evaluation_mode, str) or evaluation_mode not in ALLOWED_EVALUATION_MODES:
        errors.append(
            f"{prefix}.evaluation_mode must be one of "
            f"{sorted(ALLOWED_EVALUATION_MODES)}"
        )
    elif evaluation_mode == "agent-prompt" and case_status == "active":
        errors.append(
            f"{prefix}.evaluation_mode=agent-prompt cannot be active in the offline runner"
        )
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
        prompt_sha256 = input_data.get("prompt_sha256")
        if not isinstance(prompt_sha256, str) or not re.fullmatch(r"[0-9a-f]{64}", prompt_sha256):
            errors.append(f"{prefix}.input.prompt_sha256 must be a lowercase SHA-256")
        action_burden = input_data.get("action_burden")
        if (
            not isinstance(action_burden, str)
            or action_burden not in decision_tree.action_labels()
        ):
            errors.append(f"{prefix}.input.action_burden is not canonical")
        weight_bearing_object = input_data.get("weight_bearing_object")
        if (
            not isinstance(weight_bearing_object, str)
            or weight_bearing_object not in decision_tree.object_labels()
        ):
            errors.append(f"{prefix}.input.weight_bearing_object is not canonical")
        input_secondary = input_data.get("secondary_routes")
        if not _as_string_list(input_secondary):
            errors.append(f"{prefix}.input.secondary_routes must be a string list")
        elif len(input_secondary) != len(set(input_secondary)):
            errors.append(f"{prefix}.input.secondary_routes must not contain duplicates")

        secondary_contracts = input_data.get("secondary_route_contracts", {})
        if secondary_contracts is None:
            secondary_contracts = {}
        if not isinstance(secondary_contracts, dict):
            errors.append(
                f"{prefix}.input.secondary_route_contracts must be an object"
            )
        else:
            secondary_set = (
                set(input_secondary) if _as_string_list(input_secondary) else set()
            )
            contract_routes = set(secondary_contracts)
            if contract_routes - secondary_set:
                errors.append(
                    f"{prefix}.input.secondary_route_contracts contains an "
                    "undeclared secondary route"
                )
            for route_id, contract in secondary_contracts.items():
                if not isinstance(route_id, str) or route_id not in route_ids:
                    errors.append(
                        f"{prefix}.input.secondary_route_contracts has unknown route: "
                        f"{route_id!r}"
                    )
                if (
                    not isinstance(contract, dict)
                    or set(contract) != {"boundary", "hard_fail_verification"}
                    or not _is_non_empty_string(contract.get("boundary"))
                    or not _is_non_empty_string(contract.get("hard_fail_verification"))
                ):
                    errors.append(
                        f"{prefix}.input.secondary_route_contracts[{route_id!r}] "
                        "must contain non-empty boundary and hard_fail_verification"
                    )

            if (
                isinstance(action_burden, str)
                and action_burden in decision_tree.action_labels()
                and isinstance(weight_bearing_object, str)
                and weight_bearing_object in decision_tree.object_labels()
                and _as_string_list(input_secondary)
            ):
                try:
                    _, derived_secondary = decision_tree.resolve(
                        action_burden, weight_bearing_object
                    )
                except RegistryError as exc:
                    errors.append(f"{prefix}.input decision-tree resolution failed: {exc}")
                else:
                    derived_set = set(derived_secondary)
                    missing_derived = derived_set - secondary_set
                    if missing_derived:
                        errors.append(
                            f"{prefix}.input.secondary_routes omits derived route(s): "
                            f"{', '.join(sorted(missing_derived))}"
                        )
                    manual_set = secondary_set - derived_set
                    if contract_routes != manual_set:
                        errors.append(
                            f"{prefix}.input.secondary_route_contracts must cover "
                            "exactly the manually attached secondary routes"
                        )
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
        unexpected_expected = set(expected) - (
            REQUIRED_EXPECTED_FIELDS | OPTIONAL_EXPECTED_FIELDS
        )
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
    if isinstance(input_data, dict) and _as_string_list(input_data.get("secondary_routes")):
        if set(input_data["secondary_routes"]) != set(secondary):
            errors.append(
                f"{prefix}.input.secondary_routes must match expected.secondary_routes"
            )

    if (
        isinstance(input_data, dict)
        and isinstance(input_data.get("action_burden"), str)
        and isinstance(input_data.get("weight_bearing_object"), str)
        and input_data["action_burden"] in decision_tree.action_labels()
        and input_data["weight_bearing_object"] in decision_tree.object_labels()
    ):
        try:
            resolved_primary, resolved_secondary = decision_tree.resolve(
                input_data["action_burden"], input_data["weight_bearing_object"]
            )
        except RegistryError as exc:
            errors.append(f"{prefix}.input decision-tree resolution failed: {exc}")
        else:
            if primary != resolved_primary:
                errors.append(
                    f"{prefix}.expected.primary_route '{primary}' does not match "
                    f"decision-tree route '{resolved_primary}'"
                )
            missing_derived = set(resolved_secondary) - set(secondary)
            if missing_derived:
                errors.append(
                    f"{prefix}.expected.secondary_routes omits derived route(s): "
                    f"{', '.join(sorted(missing_derived))}"
                )

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
    expected_parallelization = expected.get("parallelization_decision")
    if not isinstance(expected_parallelization, str) or expected_parallelization not in ALLOWED_PARALLELIZATION:
        errors.append(f"{prefix}.expected.parallelization_decision is invalid")
    failure_stage = expected.get("failure_stage")
    if case_type == "negative":
        expected_stage = FAILURE_FAMILY_TO_STAGE.get(failure_family)
        if failure_stage != expected_stage:
            errors.append(
                f"{prefix}.expected.failure_stage must be {expected_stage!r} "
                f"for failure_family {failure_family!r}"
            )
    elif failure_stage is not None:
        errors.append(f"{prefix}.expected.failure_stage is only valid for negative cases")

    fixtures = case["fixtures"]
    if not isinstance(fixtures, dict):
        errors.append(f"{prefix}.fixtures must be an object")
        fixtures = {}
    else:
        missing_fixtures = REQUIRED_FIXTURE_FIELDS - set(fixtures)
        unexpected_fixtures = set(fixtures) - (
            REQUIRED_FIXTURE_FIELDS | OPTIONAL_FIXTURE_FIELDS
        )
        if missing_fixtures:
            errors.append(
                f"{prefix}.fixtures missing field(s): {', '.join(sorted(missing_fixtures))}"
            )
        if unexpected_fixtures:
            errors.append(
                f"{prefix}.fixtures has unexpected field(s): "
                f"{', '.join(sorted(unexpected_fixtures))}"
            )
    fixture_keys = set(REQUIRED_FIXTURE_FIELDS)
    if evaluation_mode == "activation-record-integration":
        if "activation_snapshot" not in fixtures:
            errors.append(
                f"{prefix}.fixtures.activation_snapshot is required for "
                "activation-record-integration"
            )
        else:
            fixture_keys.add("activation_snapshot")
    elif "activation_snapshot" in fixtures:
        errors.append(
            f"{prefix}.fixtures.activation_snapshot is only valid for "
            "activation-record-integration"
        )
    for fixture_key in fixture_keys:
        fixture_value = fixtures.get(fixture_key)
        fixture_path = _repo_relative_path(fixture_value, root) if isinstance(fixture_value, str) else None
        if fixture_path is None:
            errors.append(f"{prefix}.fixtures.{fixture_key} must be a repo-relative path")
            continue
        relative = fixture_path.relative_to(root).as_posix()
        referenced.add(relative)
        if not fixture_path.is_file():
            errors.append(f"{prefix}.fixtures.{fixture_key} does not exist: {relative}")
        elif fixture_key == "activation_snapshot":
            try:
                from activation_snapshot import load_activation_snapshot

                snapshot = load_activation_snapshot(fixture_path)
            except Exception as exc:
                errors.append(
                    f"{prefix}.fixtures.activation_snapshot is invalid: {exc}"
                )
            else:
                if snapshot["activation_id"] != case_id:
                    errors.append(
                        f"{prefix}.fixtures.activation_snapshot activation_id "
                        f"must be {case_id!r}"
                    )
                if snapshot["evaluation_mode"] != evaluation_mode:
                    errors.append(
                        f"{prefix}.fixtures.activation_snapshot evaluation_mode "
                        f"must be {evaluation_mode!r}"
                    )

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

    required_top = {
        "version",
        "decision_tree_version",
        "description",
        "last_reviewed",
        "cases",
    }
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
    if not isinstance(data.get("decision_tree_version"), int) or isinstance(
        data.get("decision_tree_version"), bool
    ):
        errors.append("registry.decision_tree_version must be an integer")
    if not _is_non_empty_string(data.get("description")):
        errors.append("registry.description must be non-empty")
    if not _is_non_empty_string(data.get("last_reviewed")):
        errors.append("registry.last_reviewed must be non-empty")
    if not isinstance(data.get("cases"), list):
        errors.append("registry.cases must be a list")
        return errors

    try:
        (
            route_ids,
            discipline_ids,
            audit_ids,
            required_audits,
            decision_tree,
        ) = _load_control_plane_ids()
    except EvalRegistryError as exc:
        return errors + [str(exc)]
    if data.get("decision_tree_version") != decision_tree.version:
        errors.append(
            "registry.decision_tree_version does not match the canonical decision-tree "
            f"version {decision_tree.version}"
        )

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
            decision_tree=decision_tree,
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
