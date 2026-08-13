#!/usr/bin/env python3
"""
Tests for scripts/registry_loader.py — the runtime control-plane loader.

Verifies that route / discipline / audit registries can be loaded and
validated as a single runtime fact source (issue #374), and that
route resolution (alias → canonical id) works without duplicating
_ROUTE_ALIASES in audit_report.py.
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys_path_ready = False
if not sys_path_ready:
    import sys

    SCRIPTS_DIR = ROOT / "scripts"
    if str(SCRIPTS_DIR) not in sys.path:
        sys.path.insert(0, str(SCRIPTS_DIR))
    sys_path_ready = True

import registry_loader  # noqa: E402
from registry_loader import (  # noqa: E402
    RegistryError,
    UnknownRouteError,
    load_audit_registry,
    load_discipline_registry,
    load_route_registry,
)

EXPECTED_ROUTE_IDS = {
    "academic-review",
    "competitive-positioning",
    "constrained-choice",
    "equipment-selection",
    "listed-company",
    "market-entry",
    "market-outlook",
    "provider-selection",
    "regulatory-analysis",
    "shared-workflow",
    "startup-evaluation",
    "technical-deep-dive",
}

EXPECTED_DISCIPLINE_IDS = {
    "current-state",
    "source-traceability",
    "forward-looking",
    "decision-utility",
    "quantitative-role",
    "scope-completeness",
    "data-conflict",
    "counter-evidence",
    "sensitivity-analysis",
}

EXPECTED_VALIDATOR_IDS = {
    "report-quality",
    "declared-execution",
    "table-role-labels",
    "source-label-consistency",
    "listed-company-delivery",
    "scoring-replicability",
    "market-outlook-monitoring-actionability",
    "secondary-route-check",
    "contract-check",
}


class TestKnownValidatorIds:
    """KNOWN_VALIDATOR_IDS is the shared contract for binding validity."""

    def test_known_validator_ids_match_expectation(self) -> None:
        assert set(registry_loader.KNOWN_VALIDATOR_IDS) == EXPECTED_VALIDATOR_IDS

    def test_unknown_binding_rejected_by_route_registry(self) -> None:
        """A manifest binding outside KNOWN_VALIDATOR_IDS must fail loading."""
        f = tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8",
        )
        json.dump(
            {"version": 1, "routes": [
                _minimal_route({"validator_bindings": ["typo-validator"]})
            ]},
            f,
        )
        f.close()
        tmp = Path(f.name)
        try:
            with pytest.raises(RegistryError, match="typo-validator"):
                load_route_registry(tmp)
        finally:
            tmp.unlink(missing_ok=True)


class TestTopLevelRegistryValidation:
    """Top-level registry document shape must be strictly validated:
    version must be an integer, unexpected top-level keys must be
    rejected — for all three registries (P2)."""

    @staticmethod
    def _tmp(data: dict) -> Path:
        f = tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8",
        )
        json.dump(data, f)
        f.close()
        return Path(f.name)

    @staticmethod
    def _minimal_routes_doc(**overrides) -> dict:
        doc = {"version": 2, "routes": [_minimal_route({})]}
        doc.update(overrides)
        return doc

    @staticmethod
    def _minimal_disciplines_doc(**overrides) -> dict:
        doc = {"version": 1, "disciplines": []}
        doc.update(overrides)
        return doc

    @staticmethod
    def _minimal_audits_doc(**overrides) -> dict:
        doc = {"version": 1, "audits": []}
        doc.update(overrides)
        return doc

    def test_string_version_raises(self) -> None:
        for loader, doc in [
            (load_route_registry, self._minimal_routes_doc(version="2")),
            (load_discipline_registry, self._minimal_disciplines_doc(version="1")),
            (load_audit_registry, self._minimal_audits_doc(version="1")),
        ]:
            tmp = self._tmp(doc)
            try:
                with pytest.raises(RegistryError, match="version"):
                    loader(tmp)
            finally:
                tmp.unlink(missing_ok=True)

    def test_unexpected_top_level_field_raises(self) -> None:
        for loader, doc in [
            (load_route_registry, self._minimal_routes_doc(unexpected=True)),
            (load_discipline_registry, self._minimal_disciplines_doc(unexpected=True)),
            (load_audit_registry, self._minimal_audits_doc(unexpected=True)),
        ]:
            tmp = self._tmp(doc)
            try:
                with pytest.raises(RegistryError, match="unexpected"):
                    loader(tmp)
            finally:
                tmp.unlink(missing_ok=True)

    def test_bool_version_raises(self) -> None:
        tmp = self._tmp(self._minimal_routes_doc(version=True))
        try:
            with pytest.raises(RegistryError, match="version"):
                load_route_registry(tmp)
        finally:
            tmp.unlink(missing_ok=True)

    def test_entries_key_must_be_list(self) -> None:
        tmp = self._tmp(self._minimal_routes_doc(routes="not-a-list"))
        try:
            with pytest.raises(RegistryError, match="routes"):
                load_route_registry(tmp)
        finally:
            tmp.unlink(missing_ok=True)


class TestRouteRegistryLoads:
    def test_loads_real_manifest(self) -> None:
        registry = load_route_registry()
        assert {r.id for r in registry.routes} == EXPECTED_ROUTE_IDS

    def test_every_route_has_required_fields(self) -> None:
        registry = load_route_registry()
        required = {
            "id", "display_name", "category", "aliases", "required_audits",
            "hard_fail_keywords", "trigger", "do_not_use",
            "often_confused_with", "primary_reads", "required_disciplines",
            "artifact_contract", "validator_bindings", "hard_fail_source",
        }
        for route in registry.routes:
            missing = required - {f for f in route.__dataclass_fields__}
            assert not missing, f"RouteInfo missing fields: {missing}"

    def test_every_route_has_validator_bindings(self) -> None:
        registry = load_route_registry()
        for route in registry.routes:
            assert route.validator_bindings, (
                f"Route '{route.id}' has empty validator_bindings"
            )
            unknown = set(route.validator_bindings) - EXPECTED_VALIDATOR_IDS
            assert not unknown, (
                f"Route '{route.id}' has unknown validator bindings: {unknown}"
            )

    def test_every_route_has_required_disciplines(self) -> None:
        registry = load_route_registry()
        discipline_registry = load_discipline_registry()
        known = {d.id for d in discipline_registry.disciplines}
        for route in registry.routes:
            unknown = set(route.required_disciplines) - known
            assert not unknown, (
                f"Route '{route.id}' references unknown disciplines: {unknown}"
            )

    def test_every_route_primary_reads_exist(self) -> None:
        registry = load_route_registry()
        for route in registry.routes:
            for ref in route.primary_reads:
                assert (ROOT / ref).is_file(), (
                    f"Route '{route.id}' primary read missing: {ref}"
                )

    def test_route_ids_are_unique(self) -> None:
        registry = load_route_registry()
        ids = [r.id for r in registry.routes]
        assert len(ids) == len(set(ids)), f"Duplicate route ids: {ids}"

    def test_no_duplicate_aliases_across_routes(self) -> None:
        registry = load_route_registry()
        seen: dict[str, str] = {}
        for route in registry.routes:
            for alias in route.aliases:
                norm = registry_loader._normalize_name(alias)
                assert norm not in seen or seen[norm] == route.id, (
                    f"Alias '{alias}' claimed by both '{seen.get(norm)}' "
                    f"and '{route.id}'"
                )
                seen[norm] = route.id


class TestRouteResolution:
    """resolve_route must handle display names, aliases and kebab-case ids."""

    @staticmethod
    def _registry() -> registry_loader.RouteRegistry:
        return load_route_registry()

    def test_resolves_alias_with_different_casing(self) -> None:
        assert self._registry().resolve_route("Listed Company") == "listed-company"

    def test_resolves_compound_alias(self) -> None:
        assert (
            self._registry().resolve_route("market entry / regional expansion")
            == "market-entry"
        )

    def test_resolves_paren_annotated_name(self) -> None:
        assert (
            self._registry().resolve_route(
                "shared-workflow (no specialized route selected)"
            )
            == "shared-workflow"
        )

    def test_resolves_kebab_id_directly(self) -> None:
        assert (
            self._registry().resolve_route("technical-deep-dive")
            == "technical-deep-dive"
        )

    def test_resolves_space_separated_display_name(self) -> None:
        assert (
            self._registry().resolve_route("Technical Deep-dive")
            == "technical-deep-dive"
        )

    def test_unknown_route_raises(self) -> None:
        with pytest.raises(UnknownRouteError):
            self._registry().resolve_route("nonexistent-route-xyz")

    def test_validators_for_returns_bindings(self) -> None:
        bindings = self._registry().validators_for("technical-deep-dive")
        assert bindings == [
            "report-quality",
            "declared-execution",
            "table-role-labels",
            "source-label-consistency",
            "secondary-route-check",
            "contract-check",
        ]

    def test_validators_for_unknown_route_raises(self) -> None:
        with pytest.raises(UnknownRouteError):
            self._registry().validators_for("no-such-route")


def _minimal_route(overrides: dict) -> dict:
    """A structurally complete route entry for type-validation tests."""
    route = {
        "id": "test-route",
        "display_name": "Test Route",
        "category": "specialized",
        "aliases": ["test"],
        "required_audits": ["final-audit"],
        "required_disciplines": [],
        "validator_bindings": ["report-quality"],
        "primary_reads": ["references/decision-report-template.md"],
        "trigger": "trigger",
        "do_not_use": "do not use",
        "often_confused_with": ["constrained-choice"],
        "artifact_contract": "artifact",
        "hard_fail_keywords": ["test"],
        "hard_fail_source": "ROUTING-MATRIX.md#test",
    }
    route.update(overrides)
    return route


class TestRegistryValidation:
    def test_malformed_json_raises_registry_error(self) -> None:
        f = tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8",
        )
        f.write("{not valid json")
        f.close()
        tmp = Path(f.name)
        try:
            with pytest.raises(RegistryError):
                load_route_registry(tmp)
        finally:
            tmp.unlink(missing_ok=True)

    def test_missing_version_raises_registry_error(self) -> None:
        f = tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8",
        )
        json.dump({"routes": []}, f)
        f.close()
        tmp = Path(f.name)
        try:
            with pytest.raises(RegistryError):
                load_route_registry(tmp)
        finally:
            tmp.unlink(missing_ok=True)

    def test_missing_file_raises_registry_error(self) -> None:
        with pytest.raises(RegistryError):
            load_route_registry(Path("/nonexistent/route-manifest.json"))

    def test_route_missing_required_field_raises(self) -> None:
        f = tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8",
        )
        json.dump(
            {"version": 1, "routes": [{"id": "only-id"}]}, f,
        )
        f.close()
        tmp = Path(f.name)
        try:
            with pytest.raises(RegistryError):
                load_route_registry(tmp)
        finally:
            tmp.unlink(missing_ok=True)

    def test_non_list_field_raises_registry_error(self) -> None:
        """A list-typed field with a non-list value must raise RegistryError,
        not a raw TypeError."""
        f = tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8",
        )
        json.dump(
            {"version": 1, "routes": [_minimal_route({"aliases": None})]}, f,
        )
        f.close()
        tmp = Path(f.name)
        try:
            with pytest.raises(RegistryError, match="aliases"):
                load_route_registry(tmp)
        finally:
            tmp.unlink(missing_ok=True)

    def test_non_string_field_raises_registry_error(self) -> None:
        f = tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8",
        )
        json.dump(
            {"version": 1, "routes": [_minimal_route({"display_name": 42})]}, f,
        )
        f.close()
        tmp = Path(f.name)
        try:
            with pytest.raises(RegistryError, match="display_name"):
                load_route_registry(tmp)
        finally:
            tmp.unlink(missing_ok=True)

    def test_unexpected_field_raises_registry_error(self) -> None:
        """Extra fields on a registry entry must be rejected explicitly,
        not surface as a TypeError from the dataclass constructor."""
        f = tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8",
        )
        json.dump(
            {"version": 1, "routes": [_minimal_route({"surprise_field": 1})]}, f,
        )
        f.close()
        tmp = Path(f.name)
        try:
            with pytest.raises(RegistryError, match="surprise_field"):
                load_route_registry(tmp)
        finally:
            tmp.unlink(missing_ok=True)


class TestDisciplineRegistryLoads:
    def test_loads_real_registry(self) -> None:
        registry = load_discipline_registry()
        assert {d.id for d in registry.disciplines} == EXPECTED_DISCIPLINE_IDS

    def test_every_discipline_has_required_fields(self) -> None:
        registry = load_discipline_registry()
        required = {"id", "display_name", "category", "reference", "description"}
        for d in registry.disciplines:
            missing = required - {f for f in d.__dataclass_fields__}
            assert not missing, f"DisciplineInfo missing fields: {missing}"

    def test_discipline_references_exist(self) -> None:
        registry = load_discipline_registry()
        for d in registry.disciplines:
            assert (ROOT / d.reference).is_file(), (
                f"Discipline '{d.id}' reference missing: {d.reference}"
            )


class TestAuditRegistryLoads:
    def test_loads_real_registry(self) -> None:
        registry = load_audit_registry()
        assert len(registry.audits) >= 14

    def test_audit_ids_are_unique(self) -> None:
        registry = load_audit_registry()
        ids = [a.id for a in registry.audits]
        assert len(ids) == len(set(ids)), f"Duplicate audit ids: {ids}"

    def test_execution_types_are_valid(self) -> None:
        registry = load_audit_registry()
        allowed = {"automated", "manual", "process"}
        for a in registry.audits:
            assert a.execution_type in allowed, (
                f"Audit '{a.id}' has invalid execution_type: {a.execution_type}"
            )

    def test_checklist_paths_exist(self) -> None:
        registry = load_audit_registry()
        for a in registry.audits:
            assert (ROOT / a.checklist).is_file(), (
                f"Audit '{a.id}' checklist missing: {a.checklist}"
            )


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
