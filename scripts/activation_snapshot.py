#!/usr/bin/env python3
"""Typed activation snapshots shared by forward evals and audit integration.

An activation snapshot is a deterministic, versioned record of the structured
route decision.  It is deliberately not a prompt classifier or a model output:
the canonical action/object decision tree still owns route semantics.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Mapping

from registry_loader import (
    RegistryError,
    load_decision_tree_registry,
    load_route_registry,
)
from route_activation import ALLOWED_PARALLELIZATION, ActivationResult


SNAPSHOT_VERSION = 1
SNAPSHOT_MODES = {
    "structured-decision-replay",
    "activation-record-integration",
}
ACTIVATION_REF_FIELDS = {
    "activation_id",
    "snapshot_sha256",
    "snapshot_version",
    "decision_tree_version",
}
SNAPSHOT_REQUIRED_FIELDS = ACTIVATION_REF_FIELDS | {
    "evaluation_mode",
    "prompt_sha256",
    "action_burden",
    "weight_bearing_object",
    "primary_route",
    "secondary_routes",
    "derived_secondary_routes",
    "manual_secondary_routes",
    "parallelization_decision",
}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class ActivationSnapshotError(ValueError):
    """Raised when an activation snapshot or reference is malformed."""


def _canonical_payload(snapshot: Mapping[str, Any]) -> dict[str, Any]:
    """Return the hash payload, excluding the self-referential digest."""
    return {
        key: snapshot[key]
        for key in sorted(snapshot)
        if key != "snapshot_sha256"
    }


def compute_snapshot_sha256(snapshot: Mapping[str, Any]) -> str:
    """Hash a snapshot using stable JSON serialization."""
    encoded = json.dumps(
        _canonical_payload(snapshot),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def activation_reference(snapshot: Mapping[str, Any]) -> dict[str, Any]:
    """Extract the stable cross-artifact reference from a snapshot."""
    return {field: snapshot[field] for field in sorted(ACTIVATION_REF_FIELDS)}


def _require_non_empty_string(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ActivationSnapshotError(f"{field} must be a non-empty string")
    return value


def _require_sha256(value: Any, field: str) -> str:
    if not isinstance(value, str) or not SHA256_RE.fullmatch(value):
        raise ActivationSnapshotError(
            f"{field} must be a 64-character lowercase SHA-256"
        )
    return value


def _require_positive_int(value: Any, field: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise ActivationSnapshotError(f"{field} must be a positive integer")
    return value


def _require_string_list(value: Any, field: str) -> list[str]:
    if not isinstance(value, list) or not all(
        isinstance(item, str) and item.strip() for item in value
    ):
        raise ActivationSnapshotError(f"{field} must be a list of non-empty strings")
    if value != sorted(value):
        raise ActivationSnapshotError(f"{field} must be sorted canonically")
    if len(value) != len(set(value)):
        raise ActivationSnapshotError(f"{field} must not contain duplicates")
    return list(value)


def validate_activation_reference(
    reference: Any,
    *,
    label: str = "activation_snapshot",
) -> dict[str, Any]:
    """Validate the stable reference embedded in a report or Research Pack."""
    if not isinstance(reference, dict):
        raise ActivationSnapshotError(f"{label} must be an object")
    missing = ACTIVATION_REF_FIELDS - set(reference)
    unexpected = set(reference) - ACTIVATION_REF_FIELDS
    if missing:
        raise ActivationSnapshotError(
            f"{label} missing field(s): {', '.join(sorted(missing))}"
        )
    if unexpected:
        raise ActivationSnapshotError(
            f"{label} has unexpected field(s): {', '.join(sorted(unexpected))}"
        )
    activation_id = _require_non_empty_string(reference["activation_id"], f"{label}.activation_id")
    digest = _require_sha256(reference["snapshot_sha256"], f"{label}.snapshot_sha256")
    snapshot_version = _require_positive_int(
        reference["snapshot_version"], f"{label}.snapshot_version"
    )
    decision_tree_version = _require_positive_int(
        reference["decision_tree_version"], f"{label}.decision_tree_version"
    )
    return {
        "activation_id": activation_id,
        "snapshot_sha256": digest,
        "snapshot_version": snapshot_version,
        "decision_tree_version": decision_tree_version,
    }


def validate_snapshot(
    snapshot: Any,
    *,
    expected_reference: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Validate a complete snapshot against the canonical decision tree."""
    if not isinstance(snapshot, dict):
        raise ActivationSnapshotError("activation snapshot must be a JSON object")
    missing = SNAPSHOT_REQUIRED_FIELDS - set(snapshot)
    unexpected = set(snapshot) - SNAPSHOT_REQUIRED_FIELDS
    if missing:
        raise ActivationSnapshotError(
            "activation snapshot missing field(s): "
            + ", ".join(sorted(missing))
        )
    if unexpected:
        raise ActivationSnapshotError(
            "activation snapshot has unexpected field(s): "
            + ", ".join(sorted(unexpected))
        )

    normalized = dict(snapshot)
    normalized["activation_id"] = _require_non_empty_string(
        snapshot["activation_id"], "activation_id"
    )
    normalized["snapshot_version"] = _require_positive_int(
        snapshot["snapshot_version"], "snapshot_version"
    )
    if normalized["snapshot_version"] != SNAPSHOT_VERSION:
        raise ActivationSnapshotError(
            f"snapshot_version {normalized['snapshot_version']} does not match "
            f"supported version {SNAPSHOT_VERSION}"
        )
    normalized["evaluation_mode"] = _require_non_empty_string(
        snapshot["evaluation_mode"], "evaluation_mode"
    )
    if normalized["evaluation_mode"] not in SNAPSHOT_MODES:
        raise ActivationSnapshotError(
            f"evaluation_mode must be one of {sorted(SNAPSHOT_MODES)}"
        )
    normalized["decision_tree_version"] = _require_positive_int(
        snapshot["decision_tree_version"], "decision_tree_version"
    )
    normalized["prompt_sha256"] = _require_sha256(
        snapshot["prompt_sha256"], "prompt_sha256"
    )
    normalized["action_burden"] = _require_non_empty_string(
        snapshot["action_burden"], "action_burden"
    )
    normalized["weight_bearing_object"] = _require_non_empty_string(
        snapshot["weight_bearing_object"], "weight_bearing_object"
    )
    normalized["primary_route"] = _require_non_empty_string(
        snapshot["primary_route"], "primary_route"
    )
    normalized["secondary_routes"] = _require_string_list(
        snapshot["secondary_routes"], "secondary_routes"
    )
    normalized["derived_secondary_routes"] = _require_string_list(
        snapshot["derived_secondary_routes"], "derived_secondary_routes"
    )
    normalized["manual_secondary_routes"] = _require_string_list(
        snapshot["manual_secondary_routes"], "manual_secondary_routes"
    )
    normalized["parallelization_decision"] = _require_non_empty_string(
        snapshot["parallelization_decision"], "parallelization_decision"
    )
    if normalized["parallelization_decision"] not in ALLOWED_PARALLELIZATION:
        raise ActivationSnapshotError(
            "parallelization_decision must be one of "
            f"{sorted(ALLOWED_PARALLELIZATION)}"
        )
    normalized["snapshot_sha256"] = _require_sha256(
        snapshot["snapshot_sha256"], "snapshot_sha256"
    )

    try:
        route_registry = load_route_registry()
        decision_tree = load_decision_tree_registry(route_registry=route_registry)
        resolved_primary, resolved_derived = decision_tree.resolve(
            normalized["action_burden"], normalized["weight_bearing_object"]
        )
    except (RegistryError, KeyError) as exc:
        raise ActivationSnapshotError(f"canonical activation resolution failed: {exc}") from exc

    if normalized["decision_tree_version"] != decision_tree.version:
        raise ActivationSnapshotError(
            f"decision_tree_version {normalized['decision_tree_version']} does not "
            f"match canonical version {decision_tree.version}"
        )
    if normalized["primary_route"] not in route_registry.route_ids():
        raise ActivationSnapshotError(
            f"primary_route '{normalized['primary_route']}' is not canonical"
        )
    if normalized["primary_route"] != resolved_primary:
        raise ActivationSnapshotError(
            f"primary_route '{normalized['primary_route']}' does not match "
            f"canonical decision-tree route '{resolved_primary}'"
        )
    secondary = set(normalized["secondary_routes"])
    if not secondary.issubset(route_registry.route_ids()):
        unknown = sorted(secondary - route_registry.route_ids())
        raise ActivationSnapshotError(
            f"secondary_routes contains unknown route(s): {unknown}"
        )
    derived = set(normalized["derived_secondary_routes"])
    manual = set(normalized["manual_secondary_routes"])
    if derived != set(resolved_derived):
        raise ActivationSnapshotError(
            "derived_secondary_routes does not match canonical decision-tree result"
        )
    if derived | manual != secondary or derived & manual:
        raise ActivationSnapshotError(
            "secondary_routes must equal the disjoint derived/manual route sets"
        )
    if normalized["primary_route"] in secondary:
        raise ActivationSnapshotError("primary_route cannot also be a secondary route")
    expected_digest = compute_snapshot_sha256(normalized)
    if normalized["snapshot_sha256"] != expected_digest:
        raise ActivationSnapshotError(
            "snapshot_sha256 does not match the canonical snapshot payload"
        )

    if expected_reference is not None:
        reference = validate_activation_reference(expected_reference, label="expected activation reference")
        actual_reference = activation_reference(normalized)
        if actual_reference != reference:
            raise ActivationSnapshotError(
                "activation snapshot reference does not match the supplied artifact: "
                f"expected {reference}, got {actual_reference}"
            )
    return normalized


def load_activation_snapshot(path: Path) -> dict[str, Any]:
    """Read and validate a snapshot JSON file."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ActivationSnapshotError(f"activation snapshot not found: {path}") from exc
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ActivationSnapshotError(
            f"activation snapshot cannot be read as JSON: {exc}"
        ) from exc
    return validate_snapshot(data)


def build_activation_snapshot(
    activation_id: str,
    activation: ActivationResult,
    *,
    evaluation_mode: str,
) -> dict[str, Any]:
    """Serialize a canonical ActivationResult and attach its stable hash."""
    payload: dict[str, Any] = {
        "activation_id": activation_id,
        "snapshot_version": SNAPSHOT_VERSION,
        "evaluation_mode": evaluation_mode,
        "decision_tree_version": activation.decision_tree_version,
        "prompt_sha256": activation.prompt_sha256,
        "action_burden": activation.action_category,
        "weight_bearing_object": activation.weight_bearing_object,
        "primary_route": activation.primary_route,
        "secondary_routes": sorted(activation.secondary_routes),
        "derived_secondary_routes": sorted(activation.derived_secondary_routes),
        "manual_secondary_routes": sorted(activation.manual_secondary_routes),
        "parallelization_decision": activation.parallelization_decision,
    }
    payload["snapshot_sha256"] = compute_snapshot_sha256(payload)
    return validate_snapshot(payload)


def extract_activation_snapshot_reference(
    text: str,
    *,
    label: str = "Research Pack",
) -> tuple[dict[str, Any] | None, list[str]]:
    """Extract a visible ``## Activation snapshot`` reference from Markdown."""
    match = re.search(
        r"^## Activation snapshot\s*$\n(.*?)(?=^##\s|\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    if not match:
        return None, []

    values: dict[str, Any] = {}
    errors: list[str] = []
    allowed = ACTIVATION_REF_FIELDS
    for raw_line in match.group(1).splitlines():
        line = raw_line.strip()
        if not line:
            continue
        line = re.sub(r"^[-*]\s+", "", line)
        field_match = re.fullmatch(
            r"(activation_id|snapshot_sha256|snapshot_version|decision_tree_version)\s*:\s*(.+)",
            line,
        )
        if not field_match:
            errors.append(f"{label} activation snapshot has malformed line: {raw_line.strip()}")
            continue
        field, raw_value = field_match.groups()
        if field not in allowed:
            errors.append(f"{label} activation snapshot has unknown field '{field}'")
            continue
        if field in {"snapshot_version", "decision_tree_version"}:
            if not re.fullmatch(r"[0-9]+", raw_value.strip()):
                errors.append(f"{label} activation snapshot field '{field}' must be an integer")
                continue
            value: Any = int(raw_value.strip())
        else:
            value = raw_value.strip()
        if field in values:
            errors.append(f"{label} activation snapshot repeats field '{field}'")
        values[field] = value

    if errors:
        return None, errors
    try:
        return validate_activation_reference(values, label=f"{label} activation_snapshot"), []
    except ActivationSnapshotError as exc:
        return None, [str(exc)]
