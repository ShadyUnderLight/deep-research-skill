#!/usr/bin/env python3
"""
Dispatch consistency tests for audit_report.py (issue #374).

Verifies the runtime dispatch contract:
1. Every manifest validator_bindings id maps to a real validator function.
2. The validator registry and manifest bindings are bidirectionally in sync.
3. Tampering with a binding (unknown id in the manifest) fails closed.
4. Unknown route names are blocking, and _DEFAULT_ROUTE stays registered.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import audit_report  # noqa: E402
import registry_loader  # noqa: E402
from registry_loader import RegistryError, UnknownRouteError  # noqa: E402


def _manifest_bindings() -> dict[str, list[str]]:
    """route id → validator binding ids from the manifest."""
    registry = registry_loader.load_route_registry()
    return {r.id: r.validator_bindings for r in registry.routes}


class TestDispatchConsistency:
    def test_every_binding_id_maps_to_validator_function(self) -> None:
        """All binding ids used in the manifest must exist in _VALIDATOR_REGISTRY."""
        for route_id, bindings in _manifest_bindings().items():
            for binding in bindings:
                assert binding in audit_report._VALIDATOR_REGISTRY, (
                    f"Route '{route_id}' binds unknown validator '{binding}' "
                    f"— manifest and audit_report.py are out of sync"
                )

    def test_validator_registry_and_manifest_bindings_are_bidirectionally_synced(self) -> None:
        """No registered validator is unused; no binding id is unregistered."""
        manifest_union = {
            b for bindings in _manifest_bindings().values() for b in bindings
        }
        assert set(audit_report._VALIDATOR_REGISTRY.keys()) == manifest_union, (
            f"Registry/union mismatch: registry-only="
            f"{sorted(set(audit_report._VALIDATOR_REGISTRY) - manifest_union)}, "
            f"manifest-only={sorted(manifest_union - set(audit_report._VALIDATOR_REGISTRY))}"
        )

    def test_dispatch_resolves_every_route(self) -> None:
        """_dispatch_validators must resolve every manifest route to functions."""
        for route_id in _manifest_bindings():
            validators = audit_report._dispatch_validators(route_id)
            assert len(validators) == len(_manifest_bindings()[route_id]), (
                f"Route '{route_id}' dispatched {len(validators)} validators, "
                f"manifest declares {len(_manifest_bindings()[route_id])}"
            )

    def test_unknown_binding_fails_closed(self, monkeypatch) -> None:
        """A tampered manifest binding (unknown id) must raise, not silently skip."""

        class FakeRegistry:
            def validators_for(self, route_id: str) -> list[str]:
                return ["report-quality", "does-not-exist-validator"]

            def resolve_route(self, name: str) -> str:
                return "technical-deep-dive"

            def route_ids(self) -> set[str]:
                return {"technical-deep-dive"}

        monkeypatch.setattr(audit_report, "_ROUTE_REGISTRY", FakeRegistry())
        with pytest.raises(RegistryError):
            audit_report._dispatch_validators("technical-deep-dive")


class TestRouteResolutionAtRuntime:
    def test_default_route_is_registered(self) -> None:
        """_DEFAULT_ROUTE must be a canonical manifest route id."""
        registry = registry_loader.load_route_registry()
        assert audit_report._DEFAULT_ROUTE in registry.route_ids(), (
            f"_DEFAULT_ROUTE '{audit_report._DEFAULT_ROUTE}' is not in the manifest"
        )

    def test_unknown_route_raises(self) -> None:
        with pytest.raises(UnknownRouteError):
            audit_report._normalize_route("no-such-route")

    def test_display_name_resolves(self) -> None:
        assert (
            audit_report._normalize_route("Listed Company / Investment-style Research")
            == "listed-company"
        )


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
