"""Tests for validate_contract.py — the route activation contract validator.

Tests validate_contract() and extract_contract_from_markdown() across:
- Valid contracts (various route/discipline/audit combinations)
- Invalid contracts (missing primary, unknown routes, discipline-as-route)
- Markdown extraction (fenced contract block)
- Edge cases (empty contracts, malformed JSON, missing registries)
"""
import json
import sys
from pathlib import Path

# Add scripts/ to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

import pytest
from validate_contract import (
    validate_contract,
    extract_contract_from_markdown,
    ContractValidationResult,
    ContractError,
)


# ── Fixtures ────────────────────────────────────────────────────────────────


SAMPLE_CONTRACT_MD = """# Test Report

## Route and audit status

**Primary route**: Listed Company / Investment-style Research
**Secondary route**: Regulatory / Policy Impact Analysis

```contract
{
  "primary_route": "listed-company",
  "secondary_routes": ["regulatory-analysis"],
  "disciplines": ["current-state", "source-traceability"],
  "audits": [
    {"id": "listed-company-report", "status": "passed", "evidence": "\\u00a73"},
    {"id": "final-audit", "status": "passed", "evidence": "\\u00a72-\\u00a78"}
  ]
}
```
"""

NO_CONTRACT_MD = """# No contract here

Just some text without any contract block.
"""

MALFORMED_CONTRACT_MD = """# Report

```contract
{this is not valid json}
```
"""


# ── extract_contract_from_markdown tests ────────────────────────────────────


def test_extract_valid_contract():
    contract = extract_contract_from_markdown(SAMPLE_CONTRACT_MD)
    assert contract is not None
    assert contract["primary_route"] == "listed-company"
    assert "regulatory-analysis" in contract["secondary_routes"]
    assert "current-state" in contract["disciplines"]


def test_extract_no_contract():
    result = extract_contract_from_markdown(NO_CONTRACT_MD)
    assert result is None


def test_extract_malformed_contract():
    result = extract_contract_from_markdown(MALFORMED_CONTRACT_MD)
    assert result is None


def test_extract_contract_preserves_all_fields():
    contract = extract_contract_from_markdown(SAMPLE_CONTRACT_MD)
    assert "primary_route" in contract
    assert "secondary_routes" in contract
    assert "disciplines" in contract
    assert "audits" in contract


# ── validate_contract tests — valid contracts ──────────────────────────────


def test_validate_minimal_valid_contract():
    contract = {
        "primary_route": "listed-company",
        "secondary_routes": [],
        "disciplines": [],
        "audits": [
            {"id": "final-audit", "status": "passed", "evidence": "§2"},
        ],
    }
    result = validate_contract(contract)
    assert result.is_valid, f"Errors: {result.errors}"


def test_validate_full_contract():
    contract = {
        "primary_route": "market-outlook",
        "secondary_routes": ["regulatory-analysis"],
        "disciplines": ["current-state", "source-traceability", "forward-looking"],
        "audits": [
            {"id": "market-outlook-audit", "status": "passed", "evidence": "§3"},
            {"id": "source-traceability", "status": "passed", "evidence": "[S01]-[S12]"},
            {"id": "final-audit", "status": "passed", "evidence": "§2-§8"},
        ],
    }
    result = validate_contract(contract)
    assert result.is_valid, f"Errors: {result.errors}"


def test_validate_shared_workflow_valid():
    contract = {
        "primary_route": "shared-workflow",
        "secondary_routes": [],
        "disciplines": [],
        "audits": [
            {"id": "workflow-spine-audit", "status": "passed", "evidence": "§2-§6"},
            {"id": "final-audit", "status": "passed", "evidence": "§2-§8"},
        ],
    }
    result = validate_contract(contract)
    assert result.is_valid, f"Errors: {result.errors}"


def test_validate_all_route_ids_work():
    """Every canonical route id should be usable as primary_route."""
    with open(Path(__file__).resolve().parent.parent / "schemas" / "route-manifest.json", "r") as f:
        manifest = json.load(f)

    for route in manifest["routes"]:
        contract = {
            "primary_route": route["id"],
            "secondary_routes": [],
            "disciplines": [],
            "audits": [{"id": "final-audit", "status": "passed", "evidence": "§2"}],
        }
        result = validate_contract(contract)
        assert result.is_valid, (
            f"Route '{route['id']}' should be valid. Errors: {result.errors}"
        )


def test_validate_skipped_audit_no_evidence_ok():
    """Audits with status=skipped don't need evidence."""
    contract = {
        "primary_route": "listed-company",
        "secondary_routes": [],
        "disciplines": [],
        "audits": [
            {"id": "source-traceability", "status": "skipped", "evidence": ""},
            {"id": "final-audit", "status": "passed", "evidence": "§2"},
        ],
    }
    result = validate_contract(contract)
    assert result.is_valid, f"Errors: {result.errors}"


def test_validate_not_run_audit_no_evidence_ok():
    """Audits with status=not_run don't need evidence."""
    contract = {
        "primary_route": "listed-company",
        "secondary_routes": [],
        "disciplines": [],
        "audits": [
            {"id": "route-activation-audit", "status": "not_run", "evidence": ""},
            {"id": "final-audit", "status": "passed", "evidence": "§2"},
        ],
    }
    result = validate_contract(contract)
    assert result.is_valid, f"Errors: {result.errors}"


# ── validate_contract tests — invalid contracts ────────────────────────────


def test_validate_missing_primary():
    contract = {"secondary_routes": [], "disciplines": [], "audits": []}
    result = validate_contract(contract)
    assert not result.is_valid
    assert any("primary_route" in e.lower() for e in result.errors)


def test_validate_unknown_primary_route():
    contract = {
        "primary_route": "nonexistent-zzz-route",
        "secondary_routes": [],
        "disciplines": [],
        "audits": [],
    }
    result = validate_contract(contract)
    assert not result.is_valid


def test_validate_unknown_secondary_route():
    contract = {
        "primary_route": "listed-company",
        "secondary_routes": ["nonexistent-zzz"],
        "disciplines": [],
        "audits": [{"id": "final-audit", "status": "passed", "evidence": "§2"}],
    }
    result = validate_contract(contract)
    assert not result.is_valid
    assert any("secondary" in e.lower() for e in result.errors)


def test_validate_discipline_as_secondary_route():
    """Property: discipline ids should NOT be accepted as secondary routes."""
    contract = {
        "primary_route": "listed-company",
        "secondary_routes": ["current-state"],  # discipline, not route
        "disciplines": [],
        "audits": [{"id": "final-audit", "status": "passed", "evidence": "§2"}],
    }
    result = validate_contract(contract)
    assert not result.is_valid
    assert any(
        "discipline" in e.lower() or "not a valid route" in e.lower()
        for e in result.errors
    )


def test_validate_unknown_discipline():
    contract = {
        "primary_route": "listed-company",
        "secondary_routes": [],
        "disciplines": ["nonexistent-discipline"],
        "audits": [{"id": "final-audit", "status": "passed", "evidence": "§2"}],
    }
    result = validate_contract(contract)
    assert not result.is_valid


def test_validate_invalid_audit_status():
    contract = {
        "primary_route": "listed-company",
        "secondary_routes": [],
        "disciplines": [],
        "audits": [
            {"id": "final-audit", "status": "INVALID_STATUS", "evidence": ""},
        ],
    }
    result = validate_contract(contract)
    assert not result.is_valid
    assert any("status" in e.lower() for e in result.errors)


def test_validate_passed_audit_empty_evidence():
    contract = {
        "primary_route": "listed-company",
        "secondary_routes": [],
        "disciplines": [],
        "audits": [
            {"id": "final-audit", "status": "passed", "evidence": ""},
        ],
    }
    result = validate_contract(contract)
    assert not result.is_valid
    assert any("evidence" in e.lower() or "empty" in e.lower() for e in result.errors)


def test_validate_primary_equals_secondary():
    """Property: primary route cannot be a secondary route."""
    contract = {
        "primary_route": "listed-company",
        "secondary_routes": ["listed-company"],
        "disciplines": [],
        "audits": [{"id": "final-audit", "status": "passed", "evidence": "§2"}],
    }
    result = validate_contract(contract)
    assert not result.is_valid
    assert any("same" in e.lower() or "duplicate" in e.lower() or "primary" in e.lower()
               for e in result.errors)


def test_validate_shared_workflow_missing_audits():
    contract = {
        "primary_route": "shared-workflow",
        "secondary_routes": [],
        "disciplines": [],
        "audits": [],
    }
    result = validate_contract(contract)
    assert not result.is_valid


def test_validate_route_as_discipline():
    """Property: route ids should NOT be accepted as disciplines."""
    contract = {
        "primary_route": "listed-company",
        "secondary_routes": [],
        "disciplines": ["market-outlook"],  # this is a route id!
        "audits": [{"id": "final-audit", "status": "passed", "evidence": "§2"}],
    }
    result = validate_contract(contract)
    assert not result.is_valid
    assert any("route" in e.lower() for e in result.errors)


def test_validate_missing_required_fields():
    """Contract must have all required top-level fields."""
    contract = {
        "primary_route": "listed-company",
        # missing secondary_routes, disciplines, audits
    }
    result = validate_contract(contract)
    assert not result.is_valid


def test_validate_contract_roundtrip():
    """Extract + validate should work end-to-end."""
    contract = extract_contract_from_markdown(SAMPLE_CONTRACT_MD)
    assert contract is not None
    result = validate_contract(contract)
    assert result.is_valid, f"Errors: {result.errors}"


def test_validate_warnings_not_errors():
    """Some conditions should produce warnings, not errors."""
    # Shared-workflow with extra audits is a warning, not an error
    contract = {
        "primary_route": "shared-workflow",
        "secondary_routes": [],
        "disciplines": [],
        "audits": [
            {"id": "workflow-spine-audit", "status": "passed", "evidence": "§2"},
            {"id": "final-audit", "status": "passed", "evidence": "§2"},
            {"id": "extra-audit", "status": "passed", "evidence": "§3"},
        ],
    }
    result = validate_contract(contract)
    # It should be valid (has required audits), but may have a warning about extras
    assert result.is_valid or len(result.warnings) > 0


# ── ContractValidationResult tests ─────────────────────────────────────────


def test_contract_validation_result_is_valid():
    result = ContractValidationResult(errors=[], warnings=[])
    assert result.is_valid

    result = ContractValidationResult(errors=["error"], warnings=[])
    assert not result.is_valid

    result = ContractValidationResult(errors=[], warnings=["warning"])
    assert result.is_valid  # warnings don't invalidate


def test_contract_validation_result_format():
    result = ContractValidationResult(
        errors=["Missing primary_route"],
        warnings=["Extra audits detected"],
    )
    output = result.format()
    assert "Missing primary_route" in output
    assert "Extra audits" in output
