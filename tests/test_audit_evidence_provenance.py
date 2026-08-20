"""Issue #390 tests for typed audit evidence and provenance."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "audit_report.py"
POSITIVE = ROOT / "tests" / "fixtures" / "audit" / "market-outlook-pos.md"
PACK = ROOT / "tests" / "fixtures" / "audit" / "research-pack-pos.md"


def _run_report(
    path: Path,
    *extra: str,
    pack: Path = PACK,
) -> subprocess.CompletedProcess:
    return subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            str(path),
            "--research-pack",
            str(pack),
            *extra,
        ],
        capture_output=True,
        text=True,
    )


def _manual_audit(data: dict) -> dict:
    return next(
        audit for audit in data["audits"]
        if audit["audit_id"] == "market-outlook-audit"
    )


def test_strict_json_distinguishes_manual_and_automated_provenance() -> None:
    result = _run_report(POSITIVE, "--strict", "--require-contract", "--json")
    assert result.returncode == 0, result.stdout
    data = json.loads(result.stdout)
    manual = _manual_audit(data)
    automated = next(
        audit for audit in data["audits"]
        if audit["audit_id"] == "forward-looking-claims"
    )

    assert manual["execution_source"] == "manual_checklist_attestation"
    assert manual["evidence_provenance"][0]["kind"] == "report_section"
    assert manual["evidence_provenance"][0]["verified"] is True
    assert automated["execution_source"] == "automated_validator"
    assert automated["evidence_provenance"][0]["validator_binding"] == (
        "forward-looking-claims"
    )


@pytest.mark.parametrize(
    ("label", "replacement"),
    [
        ("free-text", "not actually checked"),
        ("bare-section", "§3"),
        ("missing-section", "report-section:§999"),
    ],
)
def test_strict_manual_evidence_tampering_cannot_pass(
    tmp_path: Path, label: str, replacement: str
) -> None:
    content = POSITIVE.read_text(encoding="utf-8")
    content = content.replace(
        "report-section:Monitoring signals", replacement, 1
    )
    report = tmp_path / f"{label}.md"
    report.write_text(content, encoding="utf-8")

    result = _run_report(report, "--strict", "--require-contract", "--json")
    assert result.returncode == 2, result.stdout
    data = json.loads(result.stdout)
    assert data["overall"] == "fail"
    assert _manual_audit(data)["status"] != "pass"


def test_strict_contract_evidence_tampering_cannot_pass(tmp_path: Path) -> None:
    content = POSITIVE.read_text(encoding="utf-8")
    content = content.replace(
        '"evidence": "report-section:Monitoring signals"',
        '"evidence": "report-section:§999"',
        1,
    )
    report = tmp_path / "contract-fake-section.md"
    report.write_text(content, encoding="utf-8")

    result = _run_report(report, "--strict", "--require-contract", "--json")
    assert result.returncode == 2, result.stdout
    data = json.loads(result.stdout)
    assert any("evidence" in error.lower() for error in data["blocking"])


def test_unknown_validator_binding_cannot_pass(tmp_path: Path) -> None:
    content = POSITIVE.read_text(encoding="utf-8")
    content = content.replace(
        "report-section:Monitoring signals",
        "validator:not-a-real-binding",
        1,
    )
    report = tmp_path / "unknown-validator.md"
    report.write_text(content, encoding="utf-8")

    result = _run_report(report, "--strict", "--require-contract", "--json")
    assert result.returncode == 2, result.stdout
    data = json.loads(result.stdout)
    assert data["overall"] == "fail"
    assert any("validator" in error.lower() for error in data["blocking"])


def test_validator_reference_checks_registry_for_automated_context() -> None:
    sys.path.insert(0, str(ROOT / "scripts"))
    from audit_evidence import validate_evidence_reference

    unknown = validate_evidence_reference(
        "validator:not-a-real-binding",
        strict=True,
        execution_type="automated",
    )
    assert not unknown.is_valid
    assert any("not registered" in error for error in unknown.errors)

    known = validate_evidence_reference(
        "validator:listed-company-delivery",
        strict=True,
        execution_type="automated",
    )
    assert known.is_valid, known.errors


def test_registered_but_unexecuted_validator_cannot_back_manual_audit(
    tmp_path: Path,
) -> None:
    content = POSITIVE.read_text(encoding="utf-8")
    content = content.replace(
        "report-section:Monitoring signals",
        "validator:listed-company-delivery",
        1,
    )
    report = tmp_path / "wrong-validator-for-manual.md"
    report.write_text(content, encoding="utf-8")

    result = _run_report(report, "--strict", "--require-contract", "--json")
    assert result.returncode == 2, result.stdout
    data = json.loads(result.stdout)
    manual = _manual_audit(data)
    assert manual["status"] != "pass"
    assert any("manual" in error.lower() for error in data["blocking"])


def test_research_pack_manual_validator_reference_is_rejected(tmp_path: Path) -> None:
    content = PACK.read_text(encoding="utf-8").replace(
        "pack-section:Artifact contract",
        "validator:listed-company-delivery",
        1,
    )
    pack = tmp_path / "manual-validator-pack.md"
    pack.write_text(content, encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "validate_research_pack.py"),
            str(pack),
            "--strict",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 4, result.stdout
    assert "manual audits cannot use validator evidence" in result.stdout


def test_unknown_research_pack_audit_id_fails_both_entrypoints(tmp_path: Path) -> None:
    content = PACK.read_text(encoding="utf-8").replace(
        "market-outlook-audit",
        "made-up-audit",
        1,
    )
    pack = tmp_path / "unknown-audit-pack.md"
    pack.write_text(content, encoding="utf-8")

    standalone = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "validate_research_pack.py"),
            str(pack),
            "--strict",
        ],
        capture_output=True,
        text=True,
    )
    assert standalone.returncode == 4, standalone.stdout
    assert "is not registered" in standalone.stdout

    report = _run_report(
        POSITIVE,
        "--strict",
        "--require-contract",
        "--json",
        pack=pack,
    )
    assert report.returncode == 2, report.stdout
    data = json.loads(report.stdout)
    assert any("is not registered" in error for error in data["blocking"])


def test_audit_record_without_matching_content_cannot_pass(tmp_path: Path) -> None:
    content = POSITIVE.read_text(encoding="utf-8")
    content = content.replace(
        "report-section:Monitoring signals",
        "audit-record:README.md#not-a-real-record@2030-01-01T00:00:00Z",
        1,
    )
    report = tmp_path / "unknown-record.md"
    report.write_text(content, encoding="utf-8")

    result = _run_report(report, "--strict", "--require-contract", "--json")
    assert result.returncode == 2, result.stdout
    data = json.loads(result.stdout)
    assert data["overall"] == "fail"
    assert any("audit record file" in error for error in data["blocking"])


def test_legacy_evidence_is_explicit_in_compatibility_json(tmp_path: Path) -> None:
    content = POSITIVE.read_text(encoding="utf-8")
    content = content.replace(
        "report-section:Monitoring signals", "§3", 1
    )
    report = tmp_path / "legacy.md"
    report.write_text(content, encoding="utf-8")

    result = _run_report(report, "--json")
    assert result.returncode in (0, 1), result.stdout
    data = json.loads(result.stdout)
    manual = _manual_audit(data)
    assert manual["execution_source"] == "legacy_self_attested"
    assert manual["evidence_provenance"][0]["verified"] is False


def test_duplicate_evidence_reference_shape_is_rejected() -> None:
    sys.path.insert(0, str(ROOT / "scripts"))
    from audit_evidence import validate_evidence_reference

    result = validate_evidence_reference(
        [
            "report-section:Findings",
            "report-section:Findings",
        ],
        strict=True,
    )
    assert not result.is_valid
    assert any("typed reference" in error for error in result.errors)


def test_forged_checklist_item_is_rejected() -> None:
    sys.path.insert(0, str(ROOT / "scripts"))
    from audit_evidence import validate_evidence_reference

    result = validate_evidence_reference(
        "checklist-item:checklists/final-audit.md#NO_SUCH_ITEM",
        base_dir=ROOT,
        strict=True,
    )
    assert not result.is_valid
    assert any("not found" in error for error in result.errors)


def test_real_checklist_item_is_verified() -> None:
    sys.path.insert(0, str(ROOT / "scripts"))
    from audit_evidence import validate_evidence_reference

    # Strict mode: checklist definition alone is not execution evidence (issue #401)
    strict_result = validate_evidence_reference(
        "checklist-item:checklists/final-audit.md#FA-001",
        base_dir=ROOT,
        strict=True,
    )
    assert not strict_result.is_valid
    assert any("definition-only" in e or "audit-record" in e for e in strict_result.errors)
    assert strict_result.provenance and strict_result.provenance.get("definition_only") is True

    # Compatibility mode: the definition can still be verified as existing
    compat = validate_evidence_reference(
        "checklist-item:checklists/final-audit.md#FA-001",
        base_dir=ROOT,
        strict=False,
    )
    assert compat.is_valid, compat.errors
    assert compat.provenance and compat.provenance["verified"] is True


def test_audit_record_requires_matching_record_content(tmp_path: Path) -> None:
    sys.path.insert(0, str(ROOT / "scripts"))
    from audit_evidence import validate_evidence_reference

    record_file = tmp_path / "audit-record.json"
    # Valid record must include strict provenance fields (issue #401) including evidence
    record_file.write_text(
        json.dumps({
            "records": [
                {
                    "record_id": "manual-001",
                    "recorded_at": "2026-08-18T10:00:00Z",
                    "audit_id": "market-outlook-audit",
                    "status": "passed",
                    "artifact_sha256": "a" * 64,
                    "executed_at": "2026-08-18T10:00:00Z",
                    "execution_source": "manual_checklist_attestation",
                    "evidence": "report-section:Monitoring signals",
                    "route": "market-outlook",
                }
            ]
        }),
        encoding="utf-8",
    )
    valid = validate_evidence_reference(
        "audit-record:audit-record.json#manual-001@2026-08-18T10:00:00Z",
        base_dir=tmp_path,
        strict=True,
        expected_audit_id="market-outlook-audit",
        expected_artifact_sha256="a" * 64,
        expected_route="market-outlook",
        artifact_text="## Monitoring signals\n\ncontent",
    )
    assert valid.is_valid, valid.errors
    assert valid.provenance and valid.provenance["verified"] is True

    forged = validate_evidence_reference(
        "audit-record:audit-record.json#not-real@2030-01-01T00:00:00Z",
        base_dir=tmp_path,
        strict=True,
    )
    assert not forged.is_valid
    assert any("was not found" in error for error in forged.errors)


# ─── Issue #402: validator binding must match the audit's registry binding ──
#
# The registry is the single source of truth for which validator executes an
# automated audit.  A registered-but-wrong binding (e.g. validator:report-quality
# for the forward-looking-claims audit) must fail closed in the contract,
# the Research Pack, and the unified audit report.  execution_source must be
# derived from the registry execution_type, not arbitrarily overridden by the
# report.  Nested evidence objects must match the JSON Schema
# (schemas/route-activation-contract.json): unknown fields and a
# validator_binding field that disagrees with locator are rejected.


def test_registered_but_wrong_validator_binding_cannot_pass(tmp_path: Path) -> None:
    """forward-looking-claims audit evidence = validator:report-quality
    (registered but wrong binding) must fail strict contract validation."""
    content = POSITIVE.read_text(encoding="utf-8")
    content = content.replace(
        '"id": "forward-looking-claims", "status": "passed", '
        '"evidence": "report-section:Monitoring signals"',
        '"id": "forward-looking-claims", "status": "passed", '
        '"evidence": "validator:report-quality"',
        1,
    )
    report = tmp_path / "wrong-binding.md"
    report.write_text(content, encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "validate_contract.py"),
            str(report),
            "--strict",
            "--require-contract",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2, result.stdout
    assert "does not match" in result.stdout or "binding" in result.stdout.lower()


def test_wrong_validator_binding_fails_audit_report(tmp_path: Path) -> None:
    """The unified audit_report --strict path must reject the same forgery."""
    content = POSITIVE.read_text(encoding="utf-8")
    content = content.replace(
        '"id": "forward-looking-claims", "status": "passed", '
        '"evidence": "report-section:Monitoring signals"',
        '"id": "forward-looking-claims", "status": "passed", '
        '"evidence": "validator:report-quality"',
        1,
    )
    report = tmp_path / "wrong-binding.md"
    report.write_text(content, encoding="utf-8")

    result = _run_report(report, "--strict", "--require-contract", "--json")
    assert result.returncode == 2, result.stdout
    data = json.loads(result.stdout)
    assert data["overall"] == "fail"
    assert any("binding" in error.lower() for error in data["blocking"])


def test_wrong_validator_binding_fails_research_pack(tmp_path: Path) -> None:
    """A Research Pack declaring forward-looking-claims with a registered but
    wrong binding must fail the standalone strict pack validator."""
    content = PACK.read_text(encoding="utf-8").replace(
        "- forward-looking-claims — passed — pack-section:Artifact contract",
        "- forward-looking-claims — passed — validator:report-quality",
        1,
    )
    pack = tmp_path / "wrong-binding-pack.md"
    pack.write_text(content, encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "validate_research_pack.py"),
            str(pack),
            "--strict",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 4, result.stdout
    assert "does not match" in result.stdout


def test_correct_validator_binding_passes(tmp_path: Path) -> None:
    """The exact registry binding for forward-looking-claims is accepted
    end-to-end (positive regression guard for #402)."""
    content = POSITIVE.read_text(encoding="utf-8")
    content = content.replace(
        '"id": "forward-looking-claims", "status": "passed", '
        '"evidence": "report-section:Monitoring signals"',
        '"id": "forward-looking-claims", "status": "passed", '
        '"evidence": "validator:forward-looking-claims"',
        1,
    )
    report = tmp_path / "correct-binding.md"
    report.write_text(content, encoding="utf-8")

    result = _run_report(report, "--strict", "--require-contract", "--json")
    assert result.returncode == 0, result.stdout
    data = json.loads(result.stdout)
    assert data["overall"] == "pass"


def test_execution_source_mismatch_is_rejected(tmp_path: Path) -> None:
    """A manual audit declaring execution_source=automated_validator must not
    be accepted: execution_source is derived from the registry execution_type."""
    content = POSITIVE.read_text(encoding="utf-8")
    content = content.replace(
        '"id": "market-outlook-audit", "status": "passed", '
        '"evidence": "report-section:Monitoring signals"',
        '"id": "market-outlook-audit", "status": "passed", '
        '"evidence": "report-section:Monitoring signals", '
        '"execution_source": "automated_validator"',
        1,
    )
    report = tmp_path / "wrong-exec-source.md"
    report.write_text(content, encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "validate_contract.py"),
            str(report),
            "--strict",
            "--require-contract",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2, result.stdout
    assert "execution_source" in result.stdout


def test_evidence_object_unknown_field_is_rejected() -> None:
    """Nested evidence object with an extra field is rejected — the JSON
    Schema (additionalProperties: false) must not be contradicted by runtime."""
    sys.path.insert(0, str(ROOT / "scripts"))
    from audit_evidence import validate_evidence_reference

    result = validate_evidence_reference(
        {
            "kind": "automated_validator",
            "locator": "forward-looking-claims",
            "bogus": 1,
        },
        strict=True,
        execution_type="automated",
        known_validator_bindings={"forward-looking-claims"},
    )
    assert not result.is_valid
    assert any("unknown field" in error for error in result.errors)


def test_evidence_object_wrong_validator_binding_field_is_rejected() -> None:
    """Nested evidence object whose validator_binding field disagrees with its
    locator is rejected (declared support must match the referenced validator)."""
    sys.path.insert(0, str(ROOT / "scripts"))
    from audit_evidence import validate_evidence_reference

    result = validate_evidence_reference(
        {
            "kind": "automated_validator",
            "locator": "forward-looking-claims",
            "validator_binding": "report-quality",
        },
        strict=True,
        execution_type="automated",
        known_validator_bindings={"forward-looking-claims", "report-quality"},
    )
    assert not result.is_valid
    assert any("validator_binding" in error for error in result.errors)


def test_validator_reference_must_match_expected_binding() -> None:
    """A registered-but-wrong validator reference must fail exact-match against
    the audit's registry validator_binding."""
    sys.path.insert(0, str(ROOT / "scripts"))
    from audit_evidence import validate_evidence_reference

    result = validate_evidence_reference(
        "validator:report-quality",
        strict=True,
        execution_type="automated",
        known_validator_bindings={"forward-looking-claims", "report-quality"},
        expected_validator_binding="forward-looking-claims",
    )
    assert not result.is_valid
    assert any("does not match" in error for error in result.errors)


def test_validator_reference_matches_expected_binding() -> None:
    """The exact registry binding satisfies the expected-binding check."""
    sys.path.insert(0, str(ROOT / "scripts"))
    from audit_evidence import validate_evidence_reference

    result = validate_evidence_reference(
        "validator:forward-looking-claims",
        strict=True,
        execution_type="automated",
        known_validator_bindings={"forward-looking-claims"},
        expected_validator_binding="forward-looking-claims",
    )
    assert result.is_valid, result.errors
