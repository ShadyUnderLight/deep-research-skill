"""Reference-integrity tests for the route activation contract (issue #376).

Covers the contract-side wiring that main (#365/#374) did not yet connect:

1. Audit ids must belong to the audit registry (or be derived
   `<secondary>-secondary-hard-fail` entries).
2. `closest_alternative` must belong to the primary route's
   `often_confused_with` set from route-manifest.json.
3. The primary route's `required_audits` must all be declared, without
   duplicates.
4. Stable artifact identity fields (`artifact_id`, `contract_version`,
   `created_at`) are recommended (warn) by default and required under
   `--strict`.
5. Cross-check: pack primary route vs contract primary route must agree
   (via `--research-pack PATH`).
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from validate_contract import (
    validate_contract,
    extract_contract_from_markdown,
)

MANIFEST = json.loads((ROOT / "schemas" / "route-manifest.json").read_text(encoding="utf-8"))
AUDIT_REGISTRY = json.loads((ROOT / "schemas" / "audit-registry.json").read_text(encoding="utf-8"))

AUDIT_IDS = {a["id"] for a in AUDIT_REGISTRY["audits"]}
REQUIRED_AUDITS = {r["id"]: r["required_audits"] for r in MANIFEST["routes"]}
OFTEN_CONFUSED = {r["id"]: r["often_confused_with"] for r in MANIFEST["routes"]}


def build_contract(primary="listed-company", audits=None, **overrides):
    """Build a contract that satisfies all pre-existing rules by default."""
    audits = audits if audits is not None else [
        {"id": aid, "status": "passed", "evidence": "§2"}
        for aid in REQUIRED_AUDITS[primary]
    ]
    contract = {
        "primary_route": primary,
        "secondary_routes": [],
        "disciplines": [],
        "audits": audits,
    }
    contract.update(overrides)
    return contract


def make_report(contract_text: str) -> Path:
    """Write a small markdown report with an embedded contract block."""
    import tempfile

    f = tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", delete=False, encoding="utf-8"
    )
    f.write(f"# Test report\n\n```contract\n{contract_text}\n```\n")
    f.close()
    return Path(f.name)


# ── Audit id registry wiring ──────────────────────────────────────────────


def test_audit_id_not_in_registry_fails():
    contract = build_contract(
        audits=[
            {"id": "not-a-real-audit", "status": "passed", "evidence": "§2"},
            {"id": "final-audit", "status": "passed", "evidence": "§2"},
        ]
    )
    result = validate_contract(contract)
    assert not result.is_valid
    assert any("not-a-real-audit" in e and "registry" in e for e in result.errors)


def test_all_registry_audit_ids_accepted():
    """Every canonical audit id from the registry passes the id gate."""
    for aid in sorted(AUDIT_IDS):
        if aid == "final-audit":
            audits = [{"id": aid, "status": "passed", "evidence": "§2"}]
        else:
            audits = [
                {"id": aid, "status": "skipped", "evidence": ""},
                {"id": "final-audit", "status": "passed", "evidence": "§2"},
            ]
        # Only keep ids that do not already satisfy listed-company's required set
        required_extra = [
            r for r in REQUIRED_AUDITS["listed-company"]
            if r not in {aid, "final-audit"}
        ]
        audits += [
            {"id": r, "status": "passed", "evidence": "§2"} for r in required_extra
        ]
        contract = build_contract(audits=audits)
        result = validate_contract(contract)
        assert result.is_valid, f"audit '{aid}' should be accepted: {result.errors}"


def test_secondary_hard_fail_derived_audit_id_accepted():
    """Derived `<secondary>-secondary-hard-fail` ids stay legal (issue #376 范围 2)."""
    contract = build_contract(
        primary="market-outlook",
        secondary_routes=["regulatory-analysis"],
        audits=[
            {"id": "market-outlook-audit", "status": "passed", "evidence": "§3"},
            {"id": "forward-looking-claims", "status": "passed", "evidence": "§4"},
            {"id": "source-traceability", "status": "passed", "evidence": "[S01]-[S12]"},
            {"id": "final-audit", "status": "passed", "evidence": "§2-§8"},
            {"id": "regulatory-analysis-secondary-hard-fail", "status": "passed",
             "evidence": "§6 verified 4 hard-fail conditions"},
        ],
    )
    result = validate_contract(contract)
    assert result.is_valid, f"Errors: {result.errors}"


def test_derived_hard_fail_id_without_matching_secondary_fails():
    """A `-secondary-hard-fail` id whose prefix is not a declared secondary route fails."""
    contract = build_contract(
        audits=[
            {"id": "market-outlook-secondary-hard-fail", "status": "passed", "evidence": "§2"},
            {"id": "final-audit", "status": "passed", "evidence": "§2"},
        ]
    )
    result = validate_contract(contract)
    assert not result.is_valid
    assert any("market-outlook-secondary-hard-fail" in e for e in result.errors)


# ── closest_alternative ∈ often_confused_with ─────────────────────────────


def test_closest_alternative_not_in_often_confused_fails():
    contract = build_contract(
        primary="listed-company",
        closest_alternative="academic-review",
        boundary_judgment={
            "checked_conditions": ["x"],
            "why_not_alternative": "not an academic review task",
            "switch_conditions": "if it becomes one",
        },
    )
    result = validate_contract(contract)
    assert not result.is_valid
    assert any("often-confused" in e or "often_confused" in e for e in result.errors)


def test_closest_alternative_in_often_confused_ok():
    contract = build_contract(
        primary="listed-company",
        closest_alternative="competitive-positioning",
        boundary_judgment={
            "checked_conditions": ["uses prestige labels loosely"],
            "why_not_alternative": "Task requires investment judgment with valuation",
            "switch_conditions": "if task shifts to pure positioning",
        },
    )
    result = validate_contract(contract)
    assert result.is_valid, f"Errors: {result.errors}"


# ── required_audits enforcement ───────────────────────────────────────────


def test_missing_required_audit_fails():
    contract = build_contract(audits=[
        {"id": "final-audit", "status": "passed", "evidence": "§2"},
    ])
    result = validate_contract(contract)
    assert not result.is_valid
    assert any("not declared" in e for e in result.errors)
    assert any("listed-company-report" in e for e in result.errors)
    assert any("source-traceability" in e for e in result.errors)


def test_duplicate_audit_id_is_error():
    contract = build_contract(audits=[
        {"id": "final-audit", "status": "passed", "evidence": "§2"},
        {"id": "final-audit", "status": "passed", "evidence": "§3"},
    ])
    result = validate_contract(contract)
    assert not result.is_valid
    assert any("duplicate" in e.lower() for e in result.errors)


def test_shared_workflow_required_audits_enforced():
    contract = build_contract(primary="shared-workflow", audits=[
        {"id": "final-audit", "status": "passed", "evidence": "§2"},
    ])
    result = validate_contract(contract)
    assert not result.is_valid
    assert any("workflow-spine-audit" in e for e in result.errors)


# ── Stable artifact identity fields ───────────────────────────────────────


def test_missing_artifact_meta_warns_by_default():
    result = validate_contract(build_contract())
    assert result.is_valid
    assert any("artifact_id" in w for w in result.warnings)
    assert any("contract_version" in w for w in result.warnings)


def test_artifact_meta_present_no_warnings():
    contract = build_contract(
        artifact_id="research-2026-08-13-001",
        contract_version="1",
        created_at="2026-08-13",
    )
    result = validate_contract(contract)
    assert result.is_valid
    assert not any("artifact_id" in w for w in result.warnings)


# ── Unknown fields fail closed (issue #376 范围 3) ─────────────────────────


def test_unknown_top_level_field_fails():
    contract = build_contract(totally_unknown_field="surprise")
    result = validate_contract(contract)
    assert not result.is_valid
    assert any("unknown" in e.lower() for e in result.errors)
    assert any("totally_unknown_field" in e for e in result.errors)


def test_unknown_audit_field_fails():
    contract = build_contract(audits=[
        {"id": "final-audit", "status": "passed", "evidence": "§2",
         "tampered_evidence_flag": True},
    ])
    result = validate_contract(contract)
    assert not result.is_valid
    assert any("unknown field" in e.lower() for e in result.errors)


# ── Report-level cross-checks ─────────────────────────────────────────────


def test_pack_contract_route_mismatch_fails(monkeypatch):
    from validate_contract import main as vc_main

    contract = build_contract(primary="listed-company")
    report = make_report(json.dumps(contract))
    # Pack declares a different primary route
    pack = ROOT / "examples" / "research-pack-example.md"
    assert pack.exists()
    code = vc_main([str(report), "--research-pack", str(pack), "--require-contract"])
    assert code == 2, "pack/contract route mismatch must fail with exit 2"
    report.unlink(missing_ok=True)


def test_pack_contract_route_match_passes(monkeypatch):
    from validate_contract import main as vc_main

    # The example pack declares constrained-choice; build a matching contract.
    contract = build_contract(
        primary="constrained-choice",
        artifact_id="research-2026-08-13-pack-cross-check",
        contract_version="1",
        created_at="2026-08-13",
        audits=[
            {"id": "option-selection-final-audit", "status": "passed", "evidence": "§2"},
            {"id": "final-audit", "status": "passed", "evidence": "§2"},
        ],
    )
    report = make_report(json.dumps(contract))
    pack = ROOT / "examples" / "research-pack-example.md"
    code = vc_main([str(report), "--research-pack", str(pack), "--require-contract"])
    assert code == 0, "matching pack/contract routes must pass"
    report.unlink(missing_ok=True)


def test_contract_embedded_in_report_extracted_ok():
    contract = build_contract()
    report = make_report(json.dumps(contract))
    text = report.read_text(encoding="utf-8")
    extracted = extract_contract_from_markdown(text)
    assert extracted is not None
    assert extracted["primary_route"] == "listed-company"
    report.unlink(missing_ok=True)
