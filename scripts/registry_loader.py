#!/usr/bin/env python3
"""
Runtime control-plane registry loader (issue #374).

Loads and validates the canonical registries — route manifest, discipline
registry, audit registry and structured route-decision tree — as executable
fact sources for route identity, discipline identity, audit identity,
dispatch bindings and route activation semantics.

Previously this knowledge was duplicated across audit_report.py
(_ROUTE_ALIASES / ROUTE_VALIDATORS), validate_route_manifest.py
(regex parsing of Python source) and several docs.  This module is
the replacement runtime entry point: everything loads from the JSON
registries and fails closed on structural errors.

Usage:
    from registry_loader import load_route_registry, load_discipline_registry,
                                load_audit_registry, load_decision_tree_registry
    registry = load_route_registry()
    route_id = registry.resolve_route("listed company")     # -> "listed-company"
    bindings = registry.validators_for(route_id)            # -> ["report-quality", ...]
    tree = load_decision_tree_registry()
    primary, secondary = tree.resolve(action_label, object_label)
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
DEFAULT_DECISION_TREE = ROOT / "schemas" / "route-decision-tree.json"

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

# Validator ids that exist only to execute automated audits (issue #378).
# They are NOT route validator bindings: they are bound via each audit's
# ``validator_binding`` in schemas/audit-registry.json.  audit_report.py
# maps these ids to functions in _AUDIT_VALIDATOR_REGISTRY; keeping the
# set here makes the registry self-validating without regex-parsing code.
AUDIT_VALIDATOR_IDS: frozenset[str] = frozenset({
    "markdown-delivery",
    "research-pack",
    "forward-looking-claims",
})

# All ids an audit's validator_binding may reference.
AUDIT_BINDING_IDS: frozenset[str] = KNOWN_VALIDATOR_IDS | AUDIT_VALIDATOR_IDS

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
    "validator_binding",
}

# Optional audit-registry entry fields. ``scope`` distinguishes checklist-backed
# audits (``checklist``, the default) from delivery-scope / virtual audits that
# are executed by pipeline validators and carry no human checklist file
# (issue #393): ``delivery`` audits must declare ``checklist: null``.
AUDIT_OPTIONAL_FIELDS = {"scope"}

# Valid values for an audit entry's ``scope`` field.
VALID_AUDIT_SCOPES = {"checklist", "delivery"}


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


# Top-level fields shared by all three registry documents.
_TOP_LEVEL_FIELDS = {"version", "description", "last_reviewed"}


def _validate_top_level(data: dict, what: str, entries_key: str) -> None:
    """Strictly validate the top-level registry document shape.

    Enforces: version present and an integer (not bool), the entries key
    present and a list, and no unexpected top-level fields.  Anything else
    raises RegistryError instead of being silently accepted.
    """
    if "version" not in data:
        raise RegistryError(f"{what} missing top-level 'version'")
    if entries_key not in data:
        raise RegistryError(f"{what} missing top-level '{entries_key}'")
    unexpected = set(data) - _TOP_LEVEL_FIELDS - {entries_key}
    if unexpected:
        raise RegistryError(
            f"{what} has unexpected top-level field(s): "
            f"{', '.join(sorted(unexpected))}"
        )
    version = data["version"]
    if not isinstance(version, int) or isinstance(version, bool):
        raise RegistryError(
            f"{what} 'version' must be an integer, got {type(version).__name__}"
        )
    if not isinstance(data[entries_key], list):
        raise RegistryError(
            f"{what} '{entries_key}' must be a list, "
            f"got {type(data[entries_key]).__name__}"
        )


def _require(
    obj: dict,
    fields: set[str],
    what: str,
    optional: set[str] | None = None,
) -> None:
    """Ensure all required fields are present on a registry entry.

    ``optional`` names fields that may appear but are not required; any other
    unexpected field is rejected (fail-closed registry schema).
    """
    missing = fields - set(obj.keys())
    if missing:
        raise RegistryError(
            f"{what} missing required field(s): {', '.join(sorted(missing))}"
        )
    allowed = fields | (optional or set())
    unexpected = set(obj.keys()) - allowed
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
    """Canonical audit definition loaded from audit-registry.json.

    scope is ``checklist`` (default) for audits backed by a human checklist
    file, or ``delivery`` for delivery-scope / virtual pipeline audits that
    have no checklist file and are executed by a validator (issue #393).
    """

    id: str
    checklist: str | None
    execution_type: str  # automated | manual | process
    description: str
    automation_reference: str | None
    validator_binding: str | None
    scope: str = "checklist"


@dataclass(frozen=True)
class DecisionAction:
    """Canonical action-burden category from route-decision-tree.json."""

    id: str
    label: str


@dataclass(frozen=True)
class DecisionObject:
    """Canonical weight-bearing object and its route candidates."""

    id: str
    label: str
    candidate_routes: list[str]


@dataclass(frozen=True)
class DecisionConflict:
    """Explicit action/object override and derived secondary routes."""

    action: str
    object: str
    primary_route: str
    derived_secondary_routes: list[str]


@dataclass
class DecisionTreeRegistry:
    """Structured route-selection semantics loaded from JSON."""

    version: int
    route_manifest_version: int
    actions: list[DecisionAction]
    objects: list[DecisionObject]
    conflicts: list[DecisionConflict]
    _actions_by_label: dict[str, DecisionAction] = field(default_factory=dict, repr=False)
    _objects_by_label: dict[str, DecisionObject] = field(default_factory=dict, repr=False)
    _conflicts: dict[tuple[str, str], DecisionConflict] = field(default_factory=dict, repr=False)

    def __post_init__(self) -> None:
        self._actions_by_label = {action.label: action for action in self.actions}
        self._objects_by_label = {obj.label: obj for obj in self.objects}
        self._conflicts = {
            (conflict.action, conflict.object): conflict
            for conflict in self.conflicts
        }

    def action_labels(self) -> set[str]:
        return set(self._actions_by_label)

    def object_labels(self) -> set[str]:
        return set(self._objects_by_label)

    def resolve(
        self, action_label: str, object_label: str
    ) -> tuple[str, tuple[str, ...]]:
        """Resolve exact canonical labels without consulting Markdown."""
        action = self._actions_by_label.get(action_label)
        if action is None:
            raise RegistryError(f"Unknown decision-tree action category: {action_label!r}")
        obj = self._objects_by_label.get(object_label)
        if obj is None:
            raise RegistryError(f"Unknown decision-tree object category: {object_label!r}")
        if (action.id == "shared-workflow") != (obj.id == "shared-workflow"):
            raise RegistryError(
                "shared-workflow activation requires both action and object "
                "categories to be shared-workflow"
            )
        conflict = self._conflicts.get((action.id, obj.id))
        if conflict is not None:
            return conflict.primary_route, tuple(conflict.derived_secondary_routes)
        if not obj.candidate_routes:
            raise RegistryError(
                f"Decision-tree object '{object_label}' has no route candidate"
            )
        return obj.candidate_routes[0], ()


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

    def required_audits_for(self, route_id: str) -> list[str]:
        """Return the required audit ids declared for a route."""
        route = self.get_route(route_id)
        if route is None:
            raise UnknownRouteError(f"Unknown route: '{route_id}'")
        return list(route.required_audits)


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

    def get_audit(self, audit_id: str) -> AuditInfo | None:
        return next((a for a in self.audits if a.id == audit_id), None)

    def global_audit_ids(self) -> list[str]:
        """Delivery-scope audits that run for every route (issue #393).

        These are the pipeline validators (markdown-delivery, research-pack)
        previously hardcoded as GLOBAL_AUDITS in audit_report.py.  They are
        now first-class registry entries; callers must derive the global
        audit set from the registry, not from code.
        """
        return [a.id for a in self.audits if a.scope == "delivery"]


def load_route_registry(path: Path | None = None) -> RouteRegistry:
    """Load and validate the route manifest."""
    manifest_path = path or DEFAULT_ROUTE_MANIFEST
    data = _load_json(manifest_path, "Route manifest")
    _validate_top_level(data, "Route manifest", "routes")

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
    _validate_top_level(data, "Discipline registry", "disciplines")

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
    _validate_top_level(data, "Audit registry", "audits")

    audits: list[AuditInfo] = []
    seen_ids: set[str] = set()
    for i, entry in enumerate(data["audits"]):
        if not isinstance(entry, dict):
            raise RegistryError(f"Audit registry audits[{i}] is not an object")
        _require(
            entry,
            AUDIT_REQUIRED_FIELDS,
            f"Audit registry audits[{i}]",
            optional=AUDIT_OPTIONAL_FIELDS,
        )
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
        # scope: delivery-scope / virtual audits are executed by pipeline
        # validators and carry no human checklist file (issue #393).
        scope = entry.get("scope", "checklist")
        if scope not in VALID_AUDIT_SCOPES:
            raise RegistryError(
                f"Audit '{aid}' has invalid scope '{scope}' (allowed: "
                f"{', '.join(sorted(VALID_AUDIT_SCOPES))})"
            )
        checklist_value = entry.get("checklist")
        if scope == "delivery":
            if checklist_value is not None:
                raise RegistryError(
                    f"Delivery-scope audit '{aid}' must declare "
                    f"checklist: null (it has no human checklist file)"
                )
            checklist: str | None = None
        else:
            checklist = _require_str(entry, "checklist", f"Audit registry audits[{i}]")
            if not (ROOT / checklist).is_file():
                raise RegistryError(
                    f"Audit '{aid}' checklist missing: {checklist}"
                )
        validator_binding = _require_optional_str(
            entry, "validator_binding", f"Audit registry audits[{i}]"
        )
        if execution_type == "automated":
            if validator_binding is None:
                raise RegistryError(
                    f"Automated audit '{aid}' has no validator_binding — "
                    f"every automated audit must declare which validator "
                    f"executes it (issue #378)"
                )
            if validator_binding not in AUDIT_BINDING_IDS:
                raise RegistryError(
                    f"Automated audit '{aid}' binds unknown validator id "
                    f"'{validator_binding}' — must be one of "
                    f"{', '.join(sorted(AUDIT_BINDING_IDS))}"
                )
        elif validator_binding is not None:
            raise RegistryError(
                f"{execution_type} audit '{aid}' must not declare a "
                f"validator_binding (only automated audits execute a "
                f"validator)"
            )
        audits.append(AuditInfo(
            id=aid,
            checklist=checklist,
            execution_type=execution_type,
            description=_require_str(entry, "description", f"Audit registry audits[{i}]"),
            automation_reference=_require_optional_str(
                entry, "automation_reference", f"Audit registry audits[{i}]"
            ),
            validator_binding=validator_binding,
            scope=scope,
        ))

    return AuditRegistry(version=data["version"], audits=audits)


def load_decision_tree_registry(
    path: Path | None = None,
    *,
    route_registry: RouteRegistry | None = None,
) -> DecisionTreeRegistry:
    """Load and validate structured route-activation semantics.

    The decision tree is a separate canonical registry because action/object
    categories are not route metadata.  Its route references and declared
    manifest version are checked against the route registry before callers can
    use it.
    """
    registry_path = path or DEFAULT_DECISION_TREE
    data = _load_json(registry_path, "Route decision-tree registry")
    expected_top = {
        "version",
        "route_manifest_version",
        "description",
        "last_reviewed",
        "actions",
        "objects",
        "required_conflict_pairs",
        "conflicts",
    }
    missing = expected_top - set(data)
    unexpected = set(data) - expected_top
    if missing:
        raise RegistryError(
            "Route decision-tree registry missing top-level field(s): "
            f"{', '.join(sorted(missing))}"
        )
    if unexpected:
        raise RegistryError(
            "Route decision-tree registry has unexpected top-level field(s): "
            f"{', '.join(sorted(unexpected))}"
        )
    for key in ("version", "route_manifest_version"):
        value = data[key]
        if not isinstance(value, int) or isinstance(value, bool):
            raise RegistryError(
                f"Route decision-tree registry '{key}' must be an integer, "
                f"got {type(value).__name__}"
            )
    for key in ("actions", "objects", "required_conflict_pairs", "conflicts"):
        if not isinstance(data[key], list):
            raise RegistryError(
                f"Route decision-tree registry '{key}' must be a list, "
                f"got {type(data[key]).__name__}"
            )

    routes = route_registry or load_route_registry()
    if data["route_manifest_version"] != routes.version:
        raise RegistryError(
            "Route decision-tree registry targets route manifest version "
            f"{data['route_manifest_version']}, but loaded manifest is version "
            f"{routes.version}"
        )
    known_routes = routes.route_ids()

    actions: list[DecisionAction] = []
    action_ids: set[str] = set()
    action_labels: set[str] = set()
    for i, entry in enumerate(data["actions"]):
        if not isinstance(entry, dict):
            raise RegistryError(f"Decision-tree actions[{i}] is not an object")
        _require(entry, {"id", "label"}, f"Decision-tree actions[{i}]")
        action_id = _require_str(entry, "id", f"Decision-tree actions[{i}]")
        label = _require_str(entry, "label", f"Decision-tree actions[{i}]")
        if action_id in action_ids:
            raise RegistryError(f"Duplicate decision-tree action id: '{action_id}'")
        if label in action_labels:
            raise RegistryError(f"Duplicate decision-tree action label: '{label}'")
        action_ids.add(action_id)
        action_labels.add(label)
        actions.append(DecisionAction(id=action_id, label=label))

    objects: list[DecisionObject] = []
    object_ids: set[str] = set()
    object_labels: set[str] = set()
    for i, entry in enumerate(data["objects"]):
        if not isinstance(entry, dict):
            raise RegistryError(f"Decision-tree objects[{i}] is not an object")
        _require(
            entry,
            {"id", "label", "candidate_routes"},
            f"Decision-tree objects[{i}]",
        )
        object_id = _require_str(entry, "id", f"Decision-tree objects[{i}]")
        label = _require_str(entry, "label", f"Decision-tree objects[{i}]")
        candidates = _require_str_list(
            entry, "candidate_routes", f"Decision-tree objects[{i}]"
        )
        if object_id in object_ids:
            raise RegistryError(f"Duplicate decision-tree object id: '{object_id}'")
        if label in object_labels:
            raise RegistryError(f"Duplicate decision-tree object label: '{label}'")
        unknown = set(candidates) - known_routes
        if unknown:
            raise RegistryError(
                f"Decision-tree object '{object_id}' has unknown route candidate(s): "
                f"{', '.join(sorted(unknown))}"
            )
        if len(candidates) != len(set(candidates)):
            raise RegistryError(
                f"Decision-tree object '{object_id}' has duplicate route candidates"
            )
        object_ids.add(object_id)
        object_labels.add(label)
        objects.append(
            DecisionObject(id=object_id, label=label, candidate_routes=candidates)
        )

    required_conflict_keys: set[tuple[str, str]] = set()
    for i, pair in enumerate(data["required_conflict_pairs"]):
        if (
            not isinstance(pair, list)
            or len(pair) != 2
            or not all(isinstance(value, str) and value.strip() for value in pair)
        ):
            raise RegistryError(
                "Decision-tree required_conflict_pairs[{}] must be a "
                "two-item list of non-empty action/object ids".format(i)
            )
        key = (pair[0], pair[1])
        if key in required_conflict_keys:
            raise RegistryError(
                f"Duplicate decision-tree required conflict pair: '{pair[0]}/{pair[1]}'"
            )
        if pair[0] not in action_ids or pair[1] not in object_ids:
            raise RegistryError(
                f"Decision-tree required conflict pair references unknown "
                f"action/object: '{pair[0]}/{pair[1]}'"
            )
        required_conflict_keys.add(key)

    conflicts: list[DecisionConflict] = []
    conflict_keys: set[tuple[str, str]] = set()
    for i, entry in enumerate(data["conflicts"]):
        if not isinstance(entry, dict):
            raise RegistryError(f"Decision-tree conflicts[{i}] is not an object")
        _require(
            entry,
            {"action", "object", "primary_route", "derived_secondary_routes"},
            f"Decision-tree conflicts[{i}]",
        )
        action_id = _require_str(entry, "action", f"Decision-tree conflicts[{i}]")
        object_id = _require_str(entry, "object", f"Decision-tree conflicts[{i}]")
        primary_route = _require_str(
            entry, "primary_route", f"Decision-tree conflicts[{i}]"
        )
        secondary = _require_str_list(
            entry,
            "derived_secondary_routes",
            f"Decision-tree conflicts[{i}]",
        )
        if action_id not in action_ids:
            raise RegistryError(
                f"Decision-tree conflict references unknown action '{action_id}'"
            )
        if object_id not in object_ids:
            raise RegistryError(
                f"Decision-tree conflict references unknown object '{object_id}'"
            )
        if primary_route not in known_routes:
            raise RegistryError(
                f"Decision-tree conflict references unknown primary route '{primary_route}'"
            )
        unknown_secondary = set(secondary) - known_routes
        if unknown_secondary:
            raise RegistryError(
                f"Decision-tree conflict '{action_id}/{object_id}' references "
                f"unknown secondary route(s): {', '.join(sorted(unknown_secondary))}"
            )
        if primary_route in secondary:
            raise RegistryError(
                f"Decision-tree conflict '{action_id}/{object_id}' repeats its "
                "primary route as a secondary route"
            )
        if len(secondary) != len(set(secondary)):
            raise RegistryError(
                f"Decision-tree conflict '{action_id}/{object_id}' has duplicate "
                "derived secondary routes"
            )
        key = (action_id, object_id)
        if key in conflict_keys:
            raise RegistryError(
                f"Duplicate decision-tree conflict pair: '{action_id}/{object_id}'"
            )
        conflict_keys.add(key)
        conflicts.append(
            DecisionConflict(
                action=action_id,
                object=object_id,
                primary_route=primary_route,
                derived_secondary_routes=secondary,
            )
        )

    actual_conflict_keys = set(conflict_keys)
    if actual_conflict_keys != required_conflict_keys:
        missing = sorted(required_conflict_keys - actual_conflict_keys)
        extra = sorted(actual_conflict_keys - required_conflict_keys)
        raise RegistryError(
            "Decision-tree conflict coverage mismatch "
            f"(missing={missing}, extra={extra})"
        )

    return DecisionTreeRegistry(
        version=data["version"],
        route_manifest_version=data["route_manifest_version"],
        actions=actions,
        objects=objects,
        conflicts=conflicts,
    )
