#!/usr/bin/env python3
"""
Runtime control-plane registry loader (issue #374).

Loads and validates the three canonical registries — route manifest,
discipline registry and audit registry — as the single executable
fact source for route identity, discipline identity, audit identity
and dispatch bindings.

Previously this knowledge was duplicated across audit_report.py
(_ROUTE_ALIASES / ROUTE_VALIDATORS), validate_route_manifest.py
(regex parsing of Python source) and several docs.  This module is
the replacement runtime entry point: everything loads from the JSON
registries and fails closed on structural errors.

Usage:
    from registry_loader import load_route_registry, load_discipline_registry,
                                load_audit_registry
    registry = load_route_registry()
    route_id = registry.resolve_route("listed company")     # -> "listed-company"
    bindings = registry.validators_for(route_id)            # -> ["report-quality", ...]
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ROUTE_MANIFEST = ROOT / "schemas" / "route-manifest.json"
DEFAULT_DISCIPLINE_REGISTRY = ROOT / "schemas" / "discipline-registry.json"
DEFAULT_AUDIT_REGISTRY = ROOT / "schemas" / "audit-registry.json"

VALID_EXECUTION_TYPES = {"automated", "manual", "process"}

# Canonical validator binding ids.  audit_report.py maps these ids to
# validator functions (_VALIDATOR_REGISTRY); the route manifest must only
# reference ids in this set.  Keeping the set here makes the manifest
# self-validating without regex-parsing audit_report.py source.
KNOWN_VALIDATOR_IDS: frozenset[str] = frozenset({
    "report-quality",
    "declared-execution",
    "table-role-labels",
    "source-label-consistency",
    "listed-company-delivery",
    "scoring-replicability",
    "market-outlook-monitoring-actionability",
    "secondary-route-check",
    "contract-check",
})

ROUTE_REQUIRED_FIELDS = {
    "id", "display_name", "category", "aliases", "required_audits",
    "required_disciplines", "validator_bindings", "primary_reads",
    "trigger", "do_not_use", "often_confused_with", "artifact_contract",
    "hard_fail_keywords", "hard_fail_source",
}
DISCIPLINE_REQUIRED_FIELDS = {
    "id", "display_name", "category", "reference", "description",
}
AUDIT_REQUIRED_FIELDS = {
    "id", "checklist", "execution_type", "description", "automation_reference",
}


class RegistryError(Exception):
    """Raised when a registry file is missing, malformed or structurally invalid."""


class UnknownRouteError(RegistryError):
    """Raised when a route name cannot be resolved to a canonical route id."""


def _normalize_name(name: str) -> str:
    """Lowercase, collapse whitespace, strip trailing parenthetical notes."""
    normalized = " ".join(name.strip().lower().split())
    no_paren = re.sub(r"\s*\([^)]*\)\s*$", "", normalized).strip()
    return no_paren if no_paren else normalized


def _load_json(path: Path, what: str) -> dict:
    """Load a JSON registry file, converting hard failures to RegistryError."""
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise RegistryError(f"{what} not found: {path}")
    except OSError as e:
        raise RegistryError(f"Cannot read {what} {path}: {e}")
    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        raise RegistryError(f"Invalid JSON in {what} {path}: {e}")
    if not isinstance(data, dict):
        raise RegistryError(f"{what} {path} must be a JSON object")
    return data


def _require(obj: dict, fields: set[str], what: str) -> None:
    """Ensure all required fields are present on a registry entry."""
    missing = fields - set(obj.keys())
    if missing:
        raise RegistryError(
            f"{what} missing required field(s): {', '.join(sorted(missing))}"
        )
    unexpected = set(obj.keys()) - fields
    if unexpected:
        raise RegistryError(
            f"{what} has unexpected field(s): {', '.join(sorted(unexpected))}"
        )


def _require_str(obj: dict, key: str, what: str) -> str:
    """Return obj[key] as a non-empty string, raising RegistryError otherwise."""
    value = obj[key]
    if not isinstance(value, str) or not value.strip():
        raise RegistryError(
            f"{what} field '{key}' must be a non-empty string, "
            f"got {type(value).__name__}"
        )
    return value


def _require_str_list(obj: dict, key: str, what: str) -> list[str]:
    """Return obj[key] as a list of strings, raising RegistryError otherwise."""
    value = obj[key]
    if not isinstance(value, list) or not all(
        isinstance(item, str) and item.strip() for item in value
    ):
        raise RegistryError(
            f"{what} field '{key}' must be a list of non-empty strings, "
            f"got {type(value).__name__}"
        )
    return list(value)


def _require_optional_str(obj: dict, key: str, what: str) -> str | None:
    """Return obj[key] as a string or None, raising RegistryError otherwise."""
    value = obj[key]
    if value is not None and not isinstance(value, str):
        raise RegistryError(
            f"{what} field '{key}' must be a string or null, "
            f"got {type(value).__name__}"
        )
    return value


@dataclass(frozen=True)
class RouteInfo:
    """Canonical route definition loaded from route-manifest.json."""

    id: str
    display_name: str
    category: str
    aliases: list[str]
    required_audits: list[str]
    required_disciplines: list[str]
    validator_bindings: list[str]
    primary_reads: list[str]
    trigger: str
    do_not_use: str
    often_confused_with: list[str]
    artifact_contract: str
    hard_fail_keywords: list[str]
    hard_fail_source: str


@dataclass(frozen=True)
class DisciplineInfo:
    """Canonical cross-cutting discipline loaded from discipline-registry.json."""

    id: str
    display_name: str
    category: str
    reference: str
    description: str


@dataclass(frozen=True)
class AuditInfo:
    """Canonical audit definition loaded from audit-registry.json."""

    id: str
    checklist: str
    execution_type: str  # automated | manual | process
    description: str
    automation_reference: str | None


@dataclass
class RouteRegistry:
    """Loaded route manifest with alias resolution and dispatch bindings."""

    version: int
    routes: list[RouteInfo]
    _alias_map: dict[str, str] = field(default_factory=dict, repr=False)
    _ids: set[str] = field(default_factory=set, repr=False)

    def __post_init__(self) -> None:
        self._ids = {r.id for r in self.routes}
        for route in self.routes:
            for alias in route.aliases:
                norm = _normalize_name(alias)
                previous = self._alias_map.get(norm)
                if previous is not None and previous != route.id:
                    raise RegistryError(
                        f"Duplicate alias '{alias}' (normalized '{norm}') "
                        f"claimed by both '{previous}' and '{route.id}'"
                    )
                self._alias_map[norm] = route.id

    def route_ids(self) -> set[str]:
        return set(self._ids)

    def get_route(self, route_id: str) -> RouteInfo | None:
        return next((r for r in self.routes if r.id == route_id), None)

    def resolve_route(self, name: str) -> str:
        """Resolve a display name / alias / kebab-case id to a canonical route id.

        Mirrors the previous _normalize_route behavior in audit_report.py:
        lowercase + whitespace collapse, alias lookup, parenthetical-note
        stripping, then a space→hyphen fallback against known route ids.
        Raises UnknownRouteError when nothing matches.
        """
        normalized = " ".join(name.strip().lower().split())
        canon = self._alias_map.get(normalized)
        if canon is not None:
            return canon
        no_paren = re.sub(r"\s*\([^)]*\)\s*$", "", normalized).strip()
        if no_paren and no_paren != normalized:
            canon = self._alias_map.get(no_paren)
            if canon is not None:
                return canon
            normalized = no_paren
        fallback = normalized.replace(" ", "-")
        if fallback in self._ids:
            return fallback
        raise UnknownRouteError(
            f"Unknown route: '{name}' (resolved to '{fallback}')"
        )

    def validators_for(self, route_id: str) -> list[str]:
        """Return the validator binding ids dispatched for a route."""
        route = self.get_route(route_id)
        if route is None:
            raise UnknownRouteError(f"Unknown route: '{route_id}'")
        return list(route.validator_bindings)


@dataclass
class DisciplineRegistry:
    """Loaded discipline registry."""

    version: int
    disciplines: list[DisciplineInfo]

    def discipline_ids(self) -> set[str]:
        return {d.id for d in self.disciplines}


@dataclass
class AuditRegistry:
    """Loaded audit registry."""

    version: int
    audits: list[AuditInfo]

    def audit_ids(self) -> set[str]:
        return {a.id for a in self.audits}


def load_route_registry(path: Path | None = None) -> RouteRegistry:
    """Load and validate the route manifest."""
    manifest_path = path or DEFAULT_ROUTE_MANIFEST
    data = _load_json(manifest_path, "Route manifest")
    if "version" not in data:
        raise RegistryError(f"Route manifest missing 'version': {manifest_path}")
    if not isinstance(data.get("routes"), list):
        raise RegistryError(f"Route manifest 'routes' must be a list: {manifest_path}")

    routes: list[RouteInfo] = []
    seen_ids: set[str] = set()
    for i, entry in enumerate(data["routes"]):
        if not isinstance(entry, dict):
            raise RegistryError(f"Route manifest routes[{i}] is not an object")
        _require(entry, ROUTE_REQUIRED_FIELDS, f"Route manifest routes[{i}]")
        rid = _require_str(entry, "id", f"Route manifest routes[{i}]")
        if rid in seen_ids:
            raise RegistryError(f"Duplicate route id in manifest: '{rid}'")
        seen_ids.add(rid)
        typed = {
            "id": rid,
            "display_name": _require_str(entry, "display_name", f"Route manifest routes[{i}]"),
            "category": _require_str(entry, "category", f"Route manifest routes[{i}]"),
            "aliases": _require_str_list(entry, "aliases", f"Route manifest routes[{i}]"),
            "required_audits": _require_str_list(entry, "required_audits", f"Route manifest routes[{i}]"),
            "required_disciplines": _require_str_list(entry, "required_disciplines", f"Route manifest routes[{i}]"),
            "validator_bindings": _require_str_list(entry, "validator_bindings", f"Route manifest routes[{i}]"),
            "primary_reads": _require_str_list(entry, "primary_reads", f"Route manifest routes[{i}]"),
            "trigger": _require_str(entry, "trigger", f"Route manifest routes[{i}]"),
            "do_not_use": _require_str(entry, "do_not_use", f"Route manifest routes[{i}]"),
            "often_confused_with": _require_str_list(entry, "often_confused_with", f"Route manifest routes[{i}]"),
            "artifact_contract": _require_str(entry, "artifact_contract", f"Route manifest routes[{i}]"),
            "hard_fail_keywords": _require_str_list(entry, "hard_fail_keywords", f"Route manifest routes[{i}]"),
            "hard_fail_source": _require_str(entry, "hard_fail_source", f"Route manifest routes[{i}]"),
        }
        unknown_bindings = set(typed["validator_bindings"]) - KNOWN_VALIDATOR_IDS
        if unknown_bindings:
            raise RegistryError(
                f"Route '{rid}' binds unknown validator id(s): "
                f"{', '.join(sorted(unknown_bindings))} — must be one of "
                f"{', '.join(sorted(KNOWN_VALIDATOR_IDS))}"
            )
        routes.append(RouteInfo(**typed))

    # Fail closed if any primary read reference is missing on disk.
    for route in routes:
        for ref in route.primary_reads:
            if not (ROOT / ref).is_file():
                raise RegistryError(
                    f"Route '{route.id}' primary read missing: {ref}"
                )

    return RouteRegistry(version=data["version"], routes=routes)


def load_discipline_registry(path: Path | None = None) -> DisciplineRegistry:
    """Load and validate the discipline registry."""
    registry_path = path or DEFAULT_DISCIPLINE_REGISTRY
    data = _load_json(registry_path, "Discipline registry")
    if "version" not in data:
        raise RegistryError(f"Discipline registry missing 'version': {registry_path}")
    if not isinstance(data.get("disciplines"), list):
        raise RegistryError(
            f"Discipline registry 'disciplines' must be a list: {registry_path}"
        )

    disciplines: list[DisciplineInfo] = []
    seen_ids: set[str] = set()
    for i, entry in enumerate(data["disciplines"]):
        if not isinstance(entry, dict):
            raise RegistryError(f"Discipline registry disciplines[{i}] is not an object")
        _require(entry, DISCIPLINE_REQUIRED_FIELDS, f"Discipline registry disciplines[{i}]")
        did = _require_str(entry, "id", f"Discipline registry disciplines[{i}]")
        if did in seen_ids:
            raise RegistryError(f"Duplicate discipline id: '{did}'")
        seen_ids.add(did)
        reference = _require_str(entry, "reference", f"Discipline registry disciplines[{i}]")
        if not (ROOT / reference).is_file():
            raise RegistryError(
                f"Discipline '{did}' reference missing: {reference}"
            )
        disciplines.append(DisciplineInfo(
            id=did,
            display_name=_require_str(entry, "display_name", f"Discipline registry disciplines[{i}]"),
            category=_require_str(entry, "category", f"Discipline registry disciplines[{i}]"),
            reference=reference,
            description=_require_str(entry, "description", f"Discipline registry disciplines[{i}]"),
        ))

    return DisciplineRegistry(version=data["version"], disciplines=disciplines)


def load_audit_registry(path: Path | None = None) -> AuditRegistry:
    """Load and validate the audit registry."""
    registry_path = path or DEFAULT_AUDIT_REGISTRY
    data = _load_json(registry_path, "Audit registry")
    if "version" not in data:
        raise RegistryError(f"Audit registry missing 'version': {registry_path}")
    if not isinstance(data.get("audits"), list):
        raise RegistryError(f"Audit registry 'audits' must be a list: {registry_path}")

    audits: list[AuditInfo] = []
    seen_ids: set[str] = set()
    for i, entry in enumerate(data["audits"]):
        if not isinstance(entry, dict):
            raise RegistryError(f"Audit registry audits[{i}] is not an object")
        _require(entry, AUDIT_REQUIRED_FIELDS, f"Audit registry audits[{i}]")
        aid = _require_str(entry, "id", f"Audit registry audits[{i}]")
        if aid in seen_ids:
            raise RegistryError(f"Duplicate audit id: '{aid}'")
        seen_ids.add(aid)
        execution_type = _require_str(entry, "execution_type", f"Audit registry audits[{i}]")
        if execution_type not in VALID_EXECUTION_TYPES:
            raise RegistryError(
                f"Audit '{aid}' has invalid execution_type "
                f"'{execution_type}' (allowed: "
                f"{', '.join(sorted(VALID_EXECUTION_TYPES))})"
            )
        checklist = _require_str(entry, "checklist", f"Audit registry audits[{i}]")
        if not (ROOT / checklist).is_file():
            raise RegistryError(
                f"Audit '{aid}' checklist missing: {checklist}"
            )
        audits.append(AuditInfo(
            id=aid,
            checklist=checklist,
            execution_type=execution_type,
            description=_require_str(entry, "description", f"Audit registry audits[{i}]"),
            automation_reference=_require_optional_str(
                entry, "automation_reference", f"Audit registry audits[{i}]"
            ),
        ))

    return AuditRegistry(version=data["version"], audits=audits)
