"""Property-based tests for discipline registry schema.

Validates:
- Registry exists and is valid JSON
- Each discipline has required fields (id, display_name, category)
- Discipline ids are unique
- Known cross-cutting disciplines are all registered
- No discipline id collides with route id or alias from route-manifest.json
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = ROOT / "schemas" / "discipline-registry.json"
ROUTE_MANIFEST_PATH = ROOT / "schemas" / "route-manifest.json"


def load_registry():
    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_routes():
    with open(ROUTE_MANIFEST_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


# ── Structural tests ──────────────────────────────────────────────────────


def test_registry_exists():
    assert REGISTRY_PATH.exists(), f"{REGISTRY_PATH} does not exist"


def test_registry_valid_json():
    data = load_registry()
    assert isinstance(data, dict)


def test_registry_has_version():
    data = load_registry()
    assert "version" in data, "registry must have a version field"


def test_registry_has_disciplines():
    data = load_registry()
    assert "disciplines" in data
    assert isinstance(data["disciplines"], list)
    assert len(data["disciplines"]) > 0, "registry must have at least one discipline"


def test_each_discipline_has_required_fields():
    data = load_registry()
    required = {"id", "display_name", "category"}
    for d in data["disciplines"]:
        missing = required - set(d.keys())
        assert not missing, f"Discipline {d} missing fields: {missing}"


def test_discipline_ids_are_unique():
    data = load_registry()
    ids = [d["id"] for d in data["disciplines"]]
    duplicates = [i for i in ids if ids.count(i) > 1]
    assert not duplicates, f"Duplicate discipline ids: {set(duplicates)}"


def test_discipline_ids_are_kebab_case():
    data = load_registry()
    for d in data["disciplines"]:
        did = d["id"]
        # Must be lowercase kebab-case (no spaces, no underscores)
        assert " " not in did, f"Discipline id '{did}' contains spaces"
        assert "_" not in did, f"Discipline id '{did}' contains underscores (use hyphens)"
        assert did == did.lower(), f"Discipline id '{did}' must be lowercase"


def test_categories_are_valid():
    data = load_registry()
    valid_categories = {"evidence", "currentness", "quantitative", "decision", "scope", "other"}
    for d in data["disciplines"]:
        assert d["category"] in valid_categories, (
            f"Discipline '{d['id']}' has invalid category '{d['category']}'. "
            f"Valid: {valid_categories}"
        )


# ── Coverage tests ────────────────────────────────────────────────────────


def test_known_cross_cutting_disciplines_registered():
    """All well-known cross-cutting disciplines must be in the registry."""
    data = load_registry()
    ids = {d["id"] for d in data["disciplines"]}
    expected = {
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
    missing = expected - ids
    assert not missing, f"Missing cross-cutting disciplines: {missing}"


def test_discipline_display_names_are_descriptive():
    """Display names should be human-readable and non-empty."""
    data = load_registry()
    for d in data["disciplines"]:
        assert len(d["display_name"]) > 0, f"Empty display_name for {d['id']}"
        assert d["display_name"] != d["id"], (
            f"display_name should be descriptive, not just the id: {d['id']}"
        )


# ── Property: no collision with route ids ─────────────────────────────────


def test_no_discipline_overlaps_route_ids():
    """Property: no discipline id should match a route id."""
    data = load_registry()
    routes = load_routes()
    route_ids = {r["id"] for r in routes["routes"]}

    for d in data["disciplines"]:
        did = d["id"]
        assert did not in route_ids, (
            f"Discipline id '{did}' collides with route id. "
            f"Disciplines and routes must have separate id spaces."
        )


def test_no_discipline_overlaps_route_aliases():
    """Property: no discipline id should match a route alias (normalized)."""
    data = load_registry()
    routes = load_routes()
    route_aliases: set[str] = set()
    for r in routes["routes"]:
        for alias in r.get("aliases", []):
            normalized = alias.lower().replace(" ", "-")
            route_aliases.add(normalized)

    for d in data["disciplines"]:
        did = d["id"]
        assert did not in route_aliases, (
            f"Discipline id '{did}' collides with a route alias. "
            f"Matching aliases: {[a for a in route_aliases if a == did]}"
        )


def test_route_ids_dont_overlap_discipline_ids():
    """Property: reverse check — no route id should match a discipline id."""
    data = load_registry()
    routes = load_routes()
    discipline_ids = {d["id"] for d in data["disciplines"]}

    for r in routes["routes"]:
        rid = r["id"]
        assert rid not in discipline_ids, (
            f"Route id '{rid}' collides with discipline id. "
            f"Routes and disciplines must have separate id spaces."
        )
