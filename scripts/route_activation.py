#!/usr/bin/env python3
"""Fail-closed offline adapter for the route-selection decision tree.

Forward evals provide canonical action/object classifications explicitly.  This
module resolves those structured values against the route-decision registry and
keeps the original user prompt as an identity-checked input.  It intentionally
does not guess from arbitrary prose or fall back to ``shared-workflow``.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass

try:
    from registry_loader import (
        RegistryError,
        load_decision_tree_registry,
        load_route_registry,
    )
except ImportError:  # pragma: no cover - package import fallback
    from .registry_loader import (  # type: ignore[no-redef]
        RegistryError,
        load_decision_tree_registry,
        load_route_registry,
    )


ALLOWED_PARALLELIZATION = {"single-track", "parallel", "not-needed"}


class RouteActivationError(ValueError):
    """Raised when a structured activation input is incomplete or invalid."""


@dataclass(frozen=True)
class ActivationResult:
    primary_route: str
    secondary_routes: tuple[str, ...]
    action_category: str
    weight_bearing_object: str
    parallelization_decision: str
    prompt_sha256: str
    decision_tree_version: int
    derived_secondary_routes: tuple[str, ...] = ()
    manual_secondary_routes: tuple[str, ...] = ()
    mode: str = "offline-decision-tree-structured"


def _load_decision_tree():
    """Load the canonical decision tree and translate loader failures."""
    try:
        return load_decision_tree_registry()
    except RegistryError as exc:
        raise RouteActivationError(f"invalid route decision-tree registry: {exc}") from exc


def _resolve_route(action_category: str, weight_bearing_object: str) -> tuple[str, tuple[str, ...]]:
    decision_tree = _load_decision_tree()
    try:
        return decision_tree.resolve(action_category, weight_bearing_object)
    except RegistryError as exc:
        raise RouteActivationError(str(exc)) from exc


def _validate_secondary_contracts(
    secondary_routes: tuple[str, ...],
    derived_secondary_routes: tuple[str, ...],
    contracts: object,
) -> tuple[str, ...]:
    """Require a boundary/hard-fail contract for manual secondary routes."""
    if contracts is None:
        contracts = {}
    if not isinstance(contracts, dict):
        raise RouteActivationError(
            "input.secondary_route_contracts must be an object keyed by route id"
        )
    manual = set(secondary_routes) - set(derived_secondary_routes)
    contract_routes = set(contracts)
    if contract_routes - set(secondary_routes):
        raise RouteActivationError(
            "input.secondary_route_contracts contains a route that is not "
            "declared in input.secondary_routes"
        )
    if contract_routes & set(derived_secondary_routes):
        raise RouteActivationError(
            "derived secondary routes must not be represented as manual contracts"
        )
    if contract_routes != manual:
        missing = sorted(manual - contract_routes)
        extra = sorted(contract_routes - manual)
        raise RouteActivationError(
            "every manually attached secondary route requires a boundary and "
            f"hard-fail contract (missing={missing}, extra={extra})"
        )
    for route_id, contract in contracts.items():
        if not isinstance(route_id, str) or not route_id.strip():
            raise RouteActivationError(
                "input.secondary_route_contracts keys must be non-empty route ids"
            )
        if not isinstance(contract, dict):
            raise RouteActivationError(
                f"manual secondary route '{route_id}' contract must be an object"
            )
        if set(contract) != {"boundary", "hard_fail_verification"}:
            raise RouteActivationError(
                f"manual secondary route '{route_id}' contract must contain only "
                "boundary and hard_fail_verification"
            )
        for field in ("boundary", "hard_fail_verification"):
            if not isinstance(contract[field], str) or not contract[field].strip():
                raise RouteActivationError(
                    f"manual secondary route '{route_id}' contract field "
                    f"'{field}' must be non-empty"
                )
    return tuple(sorted(manual))


def activate_prompt(
    prompt: str,
    parallelization_decision: str,
    *,
    action_category: str | None = None,
    weight_bearing_object: str | None = None,
    secondary_routes: list[str] | tuple[str, ...] | None = None,
    secondary_route_contracts: dict[str, dict[str, str]] | None = None,
    expected_prompt_sha256: str | None = None,
) -> ActivationResult:
    """Resolve structured activation input and verify prompt identity.

    The prompt hash prevents a case from silently changing its natural-language
    input while retaining the old expected activation.  Route selection itself
    is based only on canonical action/object fields; an absent or unknown field
    is a hard error instead of an escape-hatch fallback.
    """
    if not isinstance(prompt, str) or not prompt.strip():
        raise RouteActivationError("input.user_prompt must be a non-empty string")
    if parallelization_decision not in ALLOWED_PARALLELIZATION:
        raise RouteActivationError(
            "input.parallelization_decision must be one of "
            f"{sorted(ALLOWED_PARALLELIZATION)}"
        )
    decision_tree = _load_decision_tree()
    if (
        not isinstance(action_category, str)
        or action_category not in decision_tree.action_labels()
    ):
        raise RouteActivationError(f"unknown structured action_burden: {action_category!r}")
    if (
        not isinstance(weight_bearing_object, str)
        or weight_bearing_object not in decision_tree.object_labels()
    ):
        raise RouteActivationError(
            f"unknown structured weight_bearing_object: {weight_bearing_object!r}"
        )
    if not isinstance(expected_prompt_sha256, str) or not re.fullmatch(r"[0-9a-f]{64}", expected_prompt_sha256):
        raise RouteActivationError("input.prompt_sha256 must be a 64-character lowercase SHA-256")
    prompt_sha256 = hashlib.sha256(prompt.encode("utf-8")).hexdigest()
    if prompt_sha256 != expected_prompt_sha256:
        raise RouteActivationError(
            "input.user_prompt does not match input.prompt_sha256; refusing stale activation"
        )
    if not isinstance(secondary_routes, (list, tuple)) or not all(
        isinstance(route, str) and route.strip() for route in secondary_routes
    ):
        raise RouteActivationError("input.secondary_routes must be a string list")
    if len(secondary_routes) != len(set(secondary_routes)):
        raise RouteActivationError("input.secondary_routes must not contain duplicates")
    route_ids = load_route_registry().route_ids()
    secondary = tuple(sorted(set(secondary_routes)))
    unknown_secondary = set(secondary) - route_ids
    if unknown_secondary:
        raise RouteActivationError(
            f"input.secondary_routes contains unknown route(s): {sorted(unknown_secondary)}"
        )

    if action_category == "shared-workflow" or weight_bearing_object == "shared-workflow":
        if action_category != "shared-workflow" or weight_bearing_object != "shared-workflow":
            raise RouteActivationError(
                "shared-workflow activation requires both action_burden and "
                "weight_bearing_object to be shared-workflow"
            )
        primary = "shared-workflow"
        derived_secondary: tuple[str, ...] = ()
    else:
        try:
            primary, derived_secondary = decision_tree.resolve(
                action_category, weight_bearing_object
            )
        except RegistryError as exc:
            raise RouteActivationError(str(exc)) from exc
    if not set(derived_secondary).issubset(set(secondary)):
        raise RouteActivationError(
            "structured secondary routes do not match the route decision-tree conflict pair: "
            f"expected {sorted(derived_secondary)}, got {sorted(secondary)}"
        )
    if primary in secondary:
        raise RouteActivationError(
            f"primary route '{primary}' cannot also be a secondary route"
        )
    manual_secondary = _validate_secondary_contracts(
        secondary, derived_secondary, secondary_route_contracts
    )
    return ActivationResult(
        primary_route=primary,
        secondary_routes=secondary,
        action_category=action_category,
        weight_bearing_object=weight_bearing_object,
        parallelization_decision=parallelization_decision,
        prompt_sha256=prompt_sha256,
        decision_tree_version=decision_tree.version,
        derived_secondary_routes=tuple(sorted(derived_secondary)),
        manual_secondary_routes=manual_secondary,
    )
