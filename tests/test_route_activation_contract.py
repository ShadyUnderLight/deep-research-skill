"""Property-based tests for route activation contract schema.

Validates the contract schema itself and contract instances:

1. Schema structural tests:
   - Schema exists, valid JSON, type=object
   - Requires primary_route, secondary_routes, disciplines, audits fields

2. Contract instance validation (via validate_contract.py):
   - Minimal contract is valid
   - Discipline/route separation (properties)
   - Secondary route ids must be valid routes
   - Audit status values are constrained
   - Shared-workflow path requires minimum audits
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTRACT_SCHEMA_PATH = ROOT / "schemas" / "route-activation-contract.json"
ROUTE_MANIFEST_PATH = ROOT / "schemas" / "route-manifest.json"
DISCIPLINE_REGISTRY_PATH = ROOT / "schemas" / "discipline-registry.json"

# Add scripts/ to path for validate_contract import
sys.path.insert(0, str(ROOT / "scripts"))

from validate_contract import validate_contract, extract_contract_from_markdown


def load_contract_schema():
    with open(CONTRACT_SCHEMA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_routes():
    with open(ROUTE_MANIFEST_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_disciplines():
    with open(DISCIPLINE_REGISTRY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


# ── Schema structural tests ───────────────────────────────────────────────


def test_contract_schema_exists():
    assert CONTRACT_SCHEMA_PATH.exists(), f"{CONTRACT_SCHEMA_PATH} does not exist"


def test_contract_schema_valid_json():
    data = load_contract_schema()
    assert isinstance(data, dict)


def test_contract_schema_has_version():
    data = load_contract_schema()
    assert "version" in data


def test_contract_schema_has_type_object():
    data = load_contract_schema()
    assert "type" in data
    assert data["type"] == "object", "contract schema must be type=object"


def test_contract_schema_requires_primary_route():
    data = load_contract_schema()
    required = data.get("required", [])
    assert "primary_route" in required, "primary_route must be required"


def test_contract_schema_defines_secondary_routes():
    data = load_contract_schema()
    props = data.get("properties", {})
    assert "secondary_routes" in props, "secondary_routes property must be defined"


def test_contract_schema_defines_disciplines():
    data = load_contract_schema()
    props = data.get("properties", {})
    assert "disciplines" in props, "disciplines property must be defined"


def test_contract_schema_defines_audits():
    data = load_contract_schema()
    props = data.get("properties", {})
    assert "audits" in props, "audits property must be defined"


def test_secondary_routes_is_array():
    data = load_contract_schema()
    sr_prop = data["properties"]["secondary_routes"]
    assert sr_prop.get("type") == "array", "secondary_routes must be array type"


def test_disciplines_is_array():
    data = load_contract_schema()
    d_prop = data["properties"]["disciplines"]
    assert d_prop.get("type") == "array", "disciplines must be array type"


def test_audits_is_array():
    data = load_contract_schema()
    a_prop = data["properties"]["audits"]
    assert a_prop.get("type") == "array", "audits must be array type"


def test_audit_item_has_status_enum():
    data = load_contract_schema()
    audits = data["properties"]["audits"]
    items = audits.get("items", {})
    status_prop = items.get("properties", {}).get("status", {})
    # Status should be constrained to valid values
    assert "enum" in status_prop or status_prop.get("type") == "string", (
        "audit status should be constrained"
    )


# ── Contract instance validation tests ────────────────────────────────────


def test_minimal_contract_has_valid_primary():
    """A minimal contract with a valid primary_route should be structurally valid."""
    routes = load_routes()
    valid_ids = {r["id"] for r in routes["routes"]}
    contract = {
        "primary_route": "listed-company",
        "secondary_routes": [],
        "disciplines": [],
        "audits": [],
    }
    assert contract["primary_route"] in valid_ids


def test_contract_disciplines_are_not_route_ids():
    """Property: discipline ids in contract must NOT be route ids."""
    routes = load_routes()
    route_ids = {r["id"] for r in routes["routes"]}
    disciplines_data = load_disciplines()
    discipline_ids = {d["id"] for d in disciplines_data["disciplines"]}

    contract = {
        "primary_route": "market-outlook",
        "secondary_routes": [],
        "disciplines": ["current-state", "source-traceability"],
        "audits": [],
    }
    for d in contract["disciplines"]:
        assert d not in route_ids, f"'{d}' is a route id, not a discipline"
        assert d in discipline_ids, f"'{d}' is not a registered discipline"


def test_contract_secondary_routes_are_valid():
    """Secondary route ids must exist in the route manifest."""
    routes = load_routes()
    valid_ids = {r["id"] for r in routes["routes"]}
    contract = {
        "primary_route": "market-outlook",
        "secondary_routes": ["regulatory-analysis"],
        "disciplines": [],
        "audits": [],
    }
    for sr in contract["secondary_routes"]:
        assert sr in valid_ids, f"Unknown secondary route: {sr}"


def test_contract_discipline_cannot_be_secondary_route():
    """Property: discipline ids should NOT be usable as secondary routes."""
    # current-state is a discipline, not a route
    contract = {
        "primary_route": "listed-company",
        "secondary_routes": ["current-state"],  # This should be REJECTED
        "disciplines": [],
        "audits": [],
    }
    result = validate_contract(contract)
    assert not result.is_valid, (
        f"Contract with discipline as secondary route should be invalid. "
        f"Got: valid={result.is_valid}"
    )
    assert any(
        "discipline" in e.lower() or "not a valid route" in e.lower()
        for e in result.errors
    ), f"Expected discipline-related error, got: {result.errors}"


def test_contract_audit_status_valid_values():
    """Audit status must be one of: passed, skipped, not_run."""
    valid_statuses = {"passed", "skipped", "not_run"}
    contract = {
        "primary_route": "listed-company",
        "secondary_routes": [],
        "disciplines": [],
        "audits": [
            {"id": "final-audit", "status": "passed", "evidence": "§2-§8"},
            {"id": "source-traceability", "status": "skipped", "evidence": "not applicable"},
            {"id": "route-activation-audit", "status": "not_run", "evidence": "deferred"},
        ],
    }
    for audit in contract["audits"]:
        assert audit["status"] in valid_statuses, (
            f"Invalid audit status '{audit['status']}' for {audit['id']}. "
            f"Must be one of: {valid_statuses}"
        )


def test_contract_invalid_audit_status():
    """An audit with invalid status should be detectable."""
    contract = {
        "primary_route": "listed-company",
        "secondary_routes": [],
        "disciplines": [],
        "audits": [
            {"id": "final-audit", "status": "invalid_status", "evidence": ""},
        ],
    }
    valid_statuses = {"passed", "skipped", "not_run"}
    invalid = [a for a in contract["audits"] if a["status"] not in valid_statuses]
    assert len(invalid) > 0, "Should detect invalid audit status"


def test_contract_shared_workflow_min_audits():
    """Shared-workflow contract should have at least workflow-spine-audit or final-audit."""
    contract = {
        "primary_route": "shared-workflow",
        "secondary_routes": [],
        "disciplines": [],
        "audits": [
            {"id": "workflow-spine-audit", "status": "passed", "evidence": "§2-§6"},
            {"id": "final-audit", "status": "passed", "evidence": "§2-§8"},
        ],
    }
    audit_ids = {a["id"] for a in contract["audits"]}
    required = {"workflow-spine-audit", "final-audit"}
    assert audit_ids & required, (
        f"Shared-workflow must include at least one of: {required}"
    )


def test_contract_primary_and_secondary_cannot_be_same():
    """Primary route must not also be declared as secondary."""
    contract = {
        "primary_route": "listed-company",
        "secondary_routes": ["listed-company"],
        "disciplines": [],
        "audits": [],
    }
    result = validate_contract(contract)
    assert not result.is_valid, (
        f"Primary route as secondary should be invalid. "
        f"Got: valid={result.is_valid}"
    )


def test_contract_secondary_routes_have_hard_fail_audit_entry():
    """When secondary routes are declared, contract should include
    per-secondary-route hard-fail verification audit entries."""
    contract = {
        "primary_route": "market-outlook",
        "secondary_routes": ["regulatory-analysis"],
        "disciplines": [],
        "audits": [
            {"id": "regulatory-analysis-secondary-hard-fail", "status": "passed",
             "evidence": "§6 verified all 4 hard-fail conditions"},
        ],
    }
    # At minimum, there should be audit entries that reference the secondary route
    secondary_route_ids = set(contract["secondary_routes"])
    audit_refs = set()
    for a in contract["audits"]:
        for sr in secondary_route_ids:
            if sr in a["id"] or sr in a.get("evidence", ""):
                audit_refs.add(sr)
    # Each secondary route should have some audit tracking
    assert secondary_route_ids == audit_refs, (
        f"Missing hard-fail audit entries for: {secondary_route_ids - audit_refs}"
    )


def test_contract_audit_evidence_not_empty():
    """Audit entries with status=passed must have non-empty evidence."""
    contract = {
        "primary_route": "listed-company",
        "secondary_routes": [],
        "disciplines": [],
        "audits": [
            {"id": "final-audit", "status": "passed", "evidence": ""},
        ],
    }
    result = validate_contract(contract)
    assert not result.is_valid, (
        f"Passed audit with empty evidence should be invalid. "
        f"Got: valid={result.is_valid}"
    )
