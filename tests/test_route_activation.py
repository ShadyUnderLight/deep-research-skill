"""Regression tests for the registry-backed route activation adapter."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from route_activation import RouteActivationError, activate_prompt  # noqa: E402


def _activate(**kwargs):
    prompt = kwargs.pop("prompt", "A stable route activation fixture")
    return activate_prompt(
        prompt,
        "single-track",
        **kwargs,
    )


def test_conflict_pair_is_resolved_from_registry() -> None:
    result = _activate(
        action_category="Judge regulation / policy impact",
        weight_bearing_object="Market / category trajectory",
        secondary_routes=["market-outlook"],
    )
    assert result.primary_route == "regulatory-analysis"
    assert result.derived_secondary_routes == ("market-outlook",)
    assert result.manual_secondary_routes == ()
    assert result.decision_tree_version == 1


def test_unknown_action_fails_closed() -> None:
    with pytest.raises(RouteActivationError, match="unknown structured action"):
        _activate(
            action_category="not-a-canonical-action",
            weight_bearing_object="Market / category trajectory",
            secondary_routes=[],
        )


def test_unknown_object_fails_closed() -> None:
    with pytest.raises(RouteActivationError, match="unknown structured weight"):
        _activate(
            action_category="Judge direction / scenario",
            weight_bearing_object="not-a-canonical-object",
            secondary_routes=[],
        )


def test_missing_derived_secondary_fails_closed() -> None:
    with pytest.raises(RouteActivationError, match="not match"):
        _activate(
            action_category="Judge listed-company value",
            weight_bearing_object="Architecture / mechanism / patent",
            secondary_routes=[],
        )


def test_manual_secondary_requires_boundary_contract() -> None:
    with pytest.raises(RouteActivationError, match="manually attached secondary"):
        _activate(
            action_category="Judge direction / scenario",
            weight_bearing_object="Market / category trajectory",
            secondary_routes=["technical-deep-dive"],
        )


def test_manual_secondary_contract_is_preserved() -> None:
    result = _activate(
        action_category="Judge direction / scenario",
        weight_bearing_object="Market / category trajectory",
        secondary_routes=["technical-deep-dive"],
        secondary_route_contracts={
            "technical-deep-dive": {
                "boundary": "The technical mechanism is explicitly attached as a secondary concern.",
                "hard_fail_verification": "technical-deep-dive-secondary-hard-fail",
            }
        },
    )
    assert result.derived_secondary_routes == ()
    assert result.manual_secondary_routes == ("technical-deep-dive",)


def test_primary_route_cannot_be_secondary() -> None:
    with pytest.raises(RouteActivationError, match="cannot also be a secondary"):
        _activate(
            action_category="Judge direction / scenario",
            weight_bearing_object="Market / category trajectory",
            secondary_routes=["market-outlook"],
            secondary_route_contracts={
                "market-outlook": {
                    "boundary": "Invalid duplicate route fixture.",
                    "hard_fail_verification": "market-outlook-secondary-hard-fail",
                }
            },
        )


def test_duplicate_secondary_route_fails_closed() -> None:
    with pytest.raises(RouteActivationError, match="must not contain duplicates"):
        _activate(
            action_category="Judge direction / scenario",
            weight_bearing_object="Market / category trajectory",
            secondary_routes=["technical-deep-dive", "technical-deep-dive"],
            secondary_route_contracts={
                "technical-deep-dive": {
                    "boundary": "Explicit secondary concern.",
                    "hard_fail_verification": "technical-deep-dive-secondary-hard-fail",
                }
            },
        )
