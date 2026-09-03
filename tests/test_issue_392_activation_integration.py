"""Production audit integration coverage for Issue 392."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "scripts" / "audit_report.py"
VALIDATE_CONTRACT = ROOT / "scripts" / "validate_contract.py"
POSITIVE_REPORT = ROOT / "tests" / "fixtures" / "audit" / "market-outlook-pos.md"
POSITIVE_PACK = ROOT / "tests" / "fixtures" / "forward" / "market-outlook-baseline-pack.md"
POSITIVE_SNAPSHOT = ROOT / "tests" / "fixtures" / "forward" / "forward-market-outlook-baseline-activation.json"
MISMATCH_REPORT = ROOT / "tests" / "fixtures" / "forward" / "forward-route-misclassification-report.md"
MISMATCH_PACK = ROOT / "tests" / "fixtures" / "forward" / "forward-route-misclassification-pack.md"
MISMATCH_SNAPSHOT = ROOT / "tests" / "fixtures" / "forward" / "forward-route-misclassification-activation.json"


def _run(
    report: Path,
    pack: Path,
    snapshot: Path,
) -> tuple[subprocess.CompletedProcess[str], dict]:
    result = subprocess.run(
        [
            sys.executable,
            str(AUDIT),
            str(report),
            "--research-pack",
            str(pack),
            "--activation-snapshot",
            str(snapshot),
            "--strict",
            "--require-contract",
            "--json",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    return result, json.loads(result.stdout)


def test_matching_activation_report_pack_contract_passes() -> None:
    result, payload = _run(POSITIVE_REPORT, POSITIVE_PACK, POSITIVE_SNAPSHOT)
    assert result.returncode == 0, result.stdout + result.stderr
    assert payload["overall"] == "pass"
    assert payload["blocking"] == []


def test_route_mismatch_is_a_blocking_production_audit_failure() -> None:
    result, payload = _run(MISMATCH_REPORT, MISMATCH_PACK, MISMATCH_SNAPSHOT)
    assert result.returncode == 2
    assert payload["overall"] == "fail"
    assert any("mismatch" in item.lower() for item in payload["blocking"])


def test_tampered_snapshot_route_fails_closed(tmp_path: Path) -> None:
    tampered = tmp_path / "tampered-activation.json"
    data = json.loads(POSITIVE_SNAPSHOT.read_text(encoding="utf-8"))
    data["primary_route"] = "regulatory-analysis"
    tampered.write_text(json.dumps(data), encoding="utf-8")

    result, payload = _run(POSITIVE_REPORT, POSITIVE_PACK, tampered)
    assert result.returncode == 2
    assert payload["overall"] == "fail"
    assert any("mismatch" in item.lower() or "canonical" in item.lower() for item in payload["blocking"])


def test_legacy_hash_bearing_snapshot_is_rejected(tmp_path: Path) -> None:
    legacy = tmp_path / "legacy-activation.json"
    data = json.loads(POSITIVE_SNAPSHOT.read_text(encoding="utf-8"))
    data["snapshot_version"] = 1
    data["prompt_sha256"] = "0" * 64
    data["snapshot_sha256"] = "0" * 64
    legacy.write_text(json.dumps(data), encoding="utf-8")

    result, payload = _run(POSITIVE_REPORT, POSITIVE_PACK, legacy)
    assert result.returncode == 2
    assert payload["overall"] == "fail"


def test_tampered_pack_snapshot_reference_fails_closed(tmp_path: Path) -> None:
    tampered = tmp_path / "tampered-pack.md"
    text = POSITIVE_PACK.read_text(encoding="utf-8")
    tampered.write_text(
        text.replace(
            "activation_id: forward-market-outlook-baseline",
            "activation_id: forged-activation",
            1,
        ),
        encoding="utf-8",
    )

    result, payload = _run(POSITIVE_REPORT, tampered, POSITIVE_SNAPSHOT)
    assert result.returncode == 2
    assert payload["overall"] == "fail"
    assert any("activation_snapshot" in item for item in payload["blocking"])


def test_v2_contract_with_v1_contract_version_fails_closed(tmp_path: Path) -> None:
    downgraded = tmp_path / "downgraded-report.md"
    text = POSITIVE_REPORT.read_text(encoding="utf-8")
    downgraded.write_text(
        text.replace('"contract_version": "2.0.0"', '"contract_version": "1.0.0"', 1),
        encoding="utf-8",
    )

    result, payload = _run(downgraded, POSITIVE_PACK, POSITIVE_SNAPSHOT)
    assert result.returncode == 2
    assert payload["overall"] == "fail"
    assert any("contract_version" in item for item in payload["blocking"])


def test_activation_snapshot_implies_contract_requirement(tmp_path: Path) -> None:
    report = tmp_path / "without-contract.md"
    report.write_text("# Report without a contract\n", encoding="utf-8")
    result = subprocess.run(
        [
            sys.executable,
            str(VALIDATE_CONTRACT),
            str(report),
            "--activation-snapshot",
            str(POSITIVE_SNAPSHOT),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 2
    assert "requires a contract" in result.stdout


def test_duplicate_visible_pack_activation_snapshot_fails_closed(
    tmp_path: Path,
) -> None:
    duplicate = tmp_path / "duplicate-pack.md"
    duplicate.write_text(
        POSITIVE_PACK.read_text(encoding="utf-8")
        + "\n## Activation snapshot\n\n"
        + "- activation_id: conflicting-activation\n"
        + "- snapshot_version: 2\n- decision_tree_version: 1\n",
        encoding="utf-8",
    )
    result, payload = _run(POSITIVE_REPORT, duplicate, POSITIVE_SNAPSHOT)
    assert result.returncode == 2
    assert payload["overall"] == "fail"
    assert any("multiple" in item.lower() for item in payload["blocking"])
