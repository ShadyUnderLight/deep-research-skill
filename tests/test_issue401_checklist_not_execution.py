"""Issue #401 negatives: checklist definition cannot masquerade as execution evidence.

Covers the acceptance criteria:

- checklist marker alone (even if exists) cannot obtain trusted pass in strict
- forged item id, missing checklist, unchecked template (all strict) -> partial/not_run
- audit-record missing / status != passed / artifact_id mismatch / audit_id mismatch / route mismatch / missing evidence/source -> fail closed
- duplicate record -> fail closed
- valid audit-record with artifact_id binding + evidence + route -> pass
- audit-records carrying removed hash fields -> fail closed
- JSON distinguishes 4 execution sources
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "audit_report.py"
POS = ROOT / "tests" / "fixtures" / "audit" / "market-outlook-pos.md"
PACK = ROOT / "tests" / "fixtures" / "audit" / "research-pack-pos.md"
REMOVED_AUDIT_RECORD_HASH_FIELDS = (
    "input_sha256",
    "artifact_sha256",
    "artifact_hash",
    "sha256",
    "record_artifact_sha256",
    "claim_alignment_bundle_sha256",
)

sys.path.insert(0, str(ROOT / "scripts"))


def _run_report(path: Path, *extra: str, pack: Path = PACK) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), str(path), "--research-pack", str(pack), *extra],
        capture_output=True,
        text=True,
    )


def _write_report_with_evidence(tmp_path: Path, evidence_locator: str) -> Path:
    """Create a market-outlook report where the manual audit evidence is replaced."""
    content = POS.read_text(encoding="utf-8")
    content = content.replace("report-section:Monitoring signals", evidence_locator, 1)
    if content.count("report-section:Monitoring signals") >= 1:
        pass
    if evidence_locator.startswith("audit-record:"):
        content = content.replace(
            '"id": "market-outlook-audit", "status": "passed", "evidence": "report-section:Monitoring signals"',
            f'"id": "market-outlook-audit", "status": "passed", "evidence": "{evidence_locator}"',
        )
        if f'"evidence": "{evidence_locator}"' not in content:
            pass
    report = tmp_path / "report.md"
    report.write_text(content, encoding="utf-8")
    return report


def _make_record_dir() -> Path:
    """Create an isolated directory under ROOT/tmp for audit-record files."""
    base = ROOT / "tmp"
    base.mkdir(parents=True, exist_ok=True)
    tmpdir = Path(tempfile.mkdtemp(dir=base))
    return tmpdir


def _write_record_file(dir_path: Path, filename: str, payload: dict) -> tuple[Path, str]:
    """Write a record JSON under dir_path and return (full_path, relative_locator)."""
    full = dir_path / filename
    full.write_text(json.dumps(payload), encoding="utf-8")
    rel = full.relative_to(ROOT).as_posix()
    return full, rel


def test_checklist_template_marker_cannot_pass_strict(tmp_path: Path) -> None:
    report = _write_report_with_evidence(tmp_path, "checklist-item:checklists/final-audit.md#FA-001")
    proc = _run_report(report, "--strict", "--require-contract", "--json")
    assert proc.returncode == 2, proc.stdout
    data = json.loads(proc.stdout)
    assert data["overall"] != "pass"
    audit = next(a for a in data["audits"] if a["audit_id"] == "market-outlook-audit")
    assert audit["status"] != "pass"
    haystack = " ".join([audit.get("reason") or ""] + data["blocking"])
    assert "definition-only" in haystack or "audit-record" in haystack


def test_forged_checklist_item_cannot_pass_strict(tmp_path: Path) -> None:
    report = _write_report_with_evidence(tmp_path, "checklist-item:checklists/final-audit.md#NO_SUCH_ITEM")
    proc = _run_report(report, "--strict", "--require-contract", "--json")
    assert proc.returncode == 2
    data = json.loads(proc.stdout)
    assert data["overall"] != "pass"


def test_audit_record_missing_file_cannot_pass(tmp_path: Path) -> None:
    report = _write_report_with_evidence(tmp_path, "audit-record:tmp/no-such.json#r1@2026-08-18T10:00:00Z")
    proc = _run_report(report, "--strict", "--require-contract", "--json")
    assert proc.returncode == 2
    data = json.loads(proc.stdout)
    assert any("does not exist" in b or "not found" in b for b in data["blocking"])


def test_audit_record_status_not_passed_cannot_pass(tmp_path: Path) -> None:
    record_dir = _make_record_dir()
    try:
        content = POS.read_text(encoding="utf-8")
        report_tmp = tmp_path / "report.md"
        placeholder = content.replace("report-section:Monitoring signals", "audit-record:tmp/placeholder#r1@2026-08-18T10:00:00Z", 1)
        m = re.search(r'"artifact_id"\s*:\s*"([^"]+)"', placeholder)
        aid = m.group(1) if m else "fixture-market-outlook-pos"
        rec_payload = {"records": [{"record_id": "r1", "recorded_at": "2026-08-18T10:00:00Z", "audit_id": "market-outlook-audit", "status": "partial", "artifact_id": aid, "executed_at": "2026-08-18T10:00:00Z", "execution_source": "manual_checklist_attestation", "evidence": "report-section:Monitoring signals", "route": "market-outlook"}]}
        rec_path, rel = _write_record_file(record_dir, "record.json", rec_payload)
        placeholder = content.replace("report-section:Monitoring signals", f"audit-record:{rel}#r1@2026-08-18T10:00:00Z", 1)
        placeholder = placeholder.replace('"evidence": "report-section:Monitoring signals"', f'"evidence": "audit-record:{rel}#r1@2026-08-18T10:00:00Z"', 1)
        report_tmp.write_text(placeholder, encoding="utf-8")
        rec_path.write_text(json.dumps(rec_payload), encoding="utf-8")
        proc = _run_report(report_tmp, "--strict", "--require-contract", "--json")
        assert proc.returncode == 2, proc.stdout
        data = json.loads(proc.stdout)
        assert data["overall"] != "pass"
        assert any("status" in b.lower() and "not passed" in b.lower() for b in data["blocking"])
    finally:
        shutil.rmtree(record_dir, ignore_errors=True)


def test_audit_record_wrong_artifact_cannot_pass(tmp_path: Path) -> None:
    record_dir = _make_record_dir()
    try:
        content = POS.read_text(encoding="utf-8")
        report_tmp = tmp_path / "report.md"
        rec_payload = {"records": [{"record_id": "r1", "recorded_at": "2026-08-18T10:00:00Z", "audit_id": "market-outlook-audit", "status": "passed", "artifact_id": "some-other-artifact", "executed_at": "2026-08-18T10:00:00Z", "execution_source": "manual_checklist_attestation", "evidence": "report-section:Monitoring signals", "route": "market-outlook"}]}
        rec_path, rel = _write_record_file(record_dir, "record.json", rec_payload)
        placeholder = content.replace("report-section:Monitoring signals", f"audit-record:{rel}#r1@2026-08-18T10:00:00Z", 1)
        placeholder = placeholder.replace('"evidence": "report-section:Monitoring signals"', f'"evidence": "audit-record:{rel}#r1@2026-08-18T10:00:00Z"', 1)
        report_tmp.write_text(placeholder, encoding="utf-8")
        proc = _run_report(report_tmp, "--strict", "--require-contract", "--json")
        assert proc.returncode == 2, proc.stdout
        data = json.loads(proc.stdout)
        assert any("artifact" in b.lower() and ("mismatch" in b.lower() or "does not match" in b.lower()) for b in data["blocking"])
    finally:
        shutil.rmtree(record_dir, ignore_errors=True)


def test_audit_record_wrong_audit_id_cannot_pass(tmp_path: Path) -> None:
    record_dir = _make_record_dir()
    try:
        content = POS.read_text(encoding="utf-8")
        report_tmp = tmp_path / "report.md"
        placeholder = content.replace("report-section:Monitoring signals", "audit-record:tmp/placeholder#r1@2026-08-18T10:00:00Z", 1)
        m = re.search(r'"artifact_id"\s*:\s*"([^"]+)"', placeholder)
        aid = m.group(1) if m else "fixture-market-outlook-pos"
        tmp_placeholder = placeholder.replace("audit-record:tmp/placeholder#r1@2026-08-18T10:00:00Z", "audit-record:tmp/dummy#r1@2026-08-18T10:00:00Z", 1)
        report_tmp.write_text(tmp_placeholder, encoding="utf-8")
        rec_payload = {"records": [{"record_id": "r1", "recorded_at": "2026-08-18T10:00:00Z", "audit_id": "final-audit", "status": "passed", "artifact_id": aid, "executed_at": "2026-08-18T10:00:00Z", "execution_source": "manual_checklist_attestation", "evidence": "report-section:Monitoring signals", "route": "market-outlook"}]}
        rec_path, rel = _write_record_file(record_dir, "record.json", rec_payload)
        placeholder = content.replace("report-section:Monitoring signals", f"audit-record:{rel}#r1@2026-08-18T10:00:00Z", 1)
        placeholder = placeholder.replace('"evidence": "report-section:Monitoring signals"', f'"evidence": "audit-record:{rel}#r1@2026-08-18T10:00:00Z"', 1)
        report_tmp.write_text(placeholder, encoding="utf-8")
        rec_path.write_text(json.dumps(rec_payload), encoding="utf-8")
        proc = _run_report(report_tmp, "--strict", "--require-contract", "--json")
        assert proc.returncode == 2, proc.stdout
        blocking = json.loads(proc.stdout)["blocking"]
        assert any("audit" in b.lower() and ("mismatch" in b.lower() or "does not match" in b.lower()) for b in blocking)
    finally:
        shutil.rmtree(record_dir, ignore_errors=True)


def test_valid_audit_record_with_binding_passes(tmp_path: Path) -> None:
    record_dir = _make_record_dir()
    try:
        content = POS.read_text(encoding="utf-8")
        report_tmp = tmp_path / "report.md"
        rec_payload: dict = {"records": [{"record_id": "r1", "recorded_at": "2026-08-18T10:00:00Z", "audit_id": "market-outlook-audit", "status": "passed", "artifact_id": "fixture-market-outlook-pos", "executed_at": "2026-08-18T10:00:00Z", "execution_source": "manual_checklist_attestation", "evidence": "report-section:Monitoring signals", "route": "market-outlook"}]}
        rec_path, rel = _write_record_file(record_dir, "record.json", rec_payload)
        placeholder = content.replace("report-section:Monitoring signals", f"audit-record:{rel}#r1@2026-08-18T10:00:00Z", 1)
        placeholder = placeholder.replace('"evidence": "report-section:Monitoring signals"', f'"evidence": "audit-record:{rel}#r1@2026-08-18T10:00:00Z"', 1)
        m = re.search(r'"artifact_id"\s*:\s*"([^"]+)"', placeholder)
        aid = m.group(1) if m else "fixture-market-outlook-pos"
        report_tmp.write_text(placeholder, encoding="utf-8")
        rec_payload["records"][0]["artifact_id"] = aid
        rec_path.write_text(json.dumps(rec_payload), encoding="utf-8")
        proc = _run_report(report_tmp, "--strict", "--require-contract", "--json")
        assert proc.returncode == 0, proc.stdout
        data = json.loads(proc.stdout)
        assert data["overall"] == "pass"
        audit = next(a for a in data["audits"] if a["audit_id"] == "market-outlook-audit")
        assert audit["status"] == "pass"
        assert audit["execution_source"] == "manual_checklist_attestation"
        assert audit["evidence_provenance"][0]["verified"] is True
        assert audit["evidence_provenance"][0]["kind"] == "audit_record"
        # nested evidence should be present
        assert audit["evidence_provenance"][0].get("record_evidence") == "report-section:Monitoring signals"
    finally:
        shutil.rmtree(record_dir, ignore_errors=True)



@pytest.mark.parametrize(
    "field",
    REMOVED_AUDIT_RECORD_HASH_FIELDS,
)
def test_audit_record_removed_hash_field_cannot_pass(
    tmp_path: Path, field: str
) -> None:
    """Removed audit-record hash fields must fail closed under the new contract."""
    record_dir = _make_record_dir()
    try:
        content = POS.read_text(encoding="utf-8")
        report_tmp = tmp_path / "report.md"
        rec_payload = {"records": [{
            "record_id": "r1",
            "recorded_at": "2026-08-18T10:00:00Z",
            "audit_id": "market-outlook-audit",
            "status": "passed",
            "artifact_id": "fixture-market-outlook-pos",
            field: "0" * 64,
            "executed_at": "2026-08-18T10:00:00Z",
            "execution_source": "manual_checklist_attestation",
            "evidence": "report-section:Monitoring signals",
            "route": "market-outlook",
        }]}
        rec_path, rel = _write_record_file(record_dir, "record.json", rec_payload)
        placeholder = content.replace(
            "report-section:Monitoring signals",
            f"audit-record:{rel}#r1@2026-08-18T10:00:00Z",
            1,
        )
        placeholder = placeholder.replace(
            '"evidence": "report-section:Monitoring signals"',
            f'"evidence": "audit-record:{rel}#r1@2026-08-18T10:00:00Z"',
            1,
        )
        report_tmp.write_text(placeholder, encoding="utf-8")
        proc = _run_report(report_tmp, "--strict", "--require-contract", "--json")
        assert proc.returncode == 2, proc.stdout
        data = json.loads(proc.stdout)
        assert any("removed hash field" in error for error in data["blocking"])
    finally:
        shutil.rmtree(record_dir, ignore_errors=True)


@pytest.mark.parametrize("field", REMOVED_AUDIT_RECORD_HASH_FIELDS)
def test_audit_record_envelope_removed_hash_field_cannot_pass(
    tmp_path: Path, field: str
) -> None:
    """Removed hash fields on a records envelope must fail closed."""
    record_dir = _make_record_dir()
    try:
        content = POS.read_text(encoding="utf-8")
        report_tmp = tmp_path / "report.md"
        ts = "2026-08-18T10:00:00Z"
        record = {
            "record_id": "r1",
            "recorded_at": ts,
            "audit_id": "market-outlook-audit",
            "status": "passed",
            "artifact_id": "fixture-market-outlook-pos",
            "executed_at": ts,
            "execution_source": "manual_checklist_attestation",
            "evidence": "report-section:Monitoring signals",
            "route": "market-outlook",
        }
        rec_payload = {"records": [record], field: "0" * 64}
        rec_path, rel = _write_record_file(record_dir, "record.json", rec_payload)
        locator = f"audit-record:{rel}#r1@{ts}"
        placeholder = content.replace(
            "report-section:Monitoring signals", locator, 1
        )
        placeholder = placeholder.replace(
            '"evidence": "report-section:Monitoring signals"',
            f'"evidence": "{locator}"',
            1,
        )
        report_tmp.write_text(placeholder, encoding="utf-8")
        proc = _run_report(report_tmp, "--strict", "--require-contract", "--json")
        assert proc.returncode == 2, proc.stdout
        data = json.loads(proc.stdout)
        assert data["overall"] != "pass"
        assert any("removed hash field" in error for error in data["blocking"])
        assert any("envelope" in error for error in data["blocking"])
        assert rec_path.is_file()
    finally:
        shutil.rmtree(record_dir, ignore_errors=True)


def test_audit_record_id_mismatch_cannot_pass(tmp_path: Path) -> None:
    """P1 regression: artifact_id mismatch must still fail."""
    record_dir = _make_record_dir()
    try:
        content = POS.read_text(encoding="utf-8")
        report_tmp = tmp_path / "report.md"
        rec_payload: dict = {"records": [{"record_id": "r1", "recorded_at": "2026-08-18T10:00:00Z", "audit_id": "market-outlook-audit", "status": "passed", "artifact_id": "wrong-id", "executed_at": "2026-08-18T10:00:00Z", "execution_source": "manual_checklist_attestation", "evidence": "report-section:Monitoring signals", "route": "market-outlook"}]}
        rec_path, rel = _write_record_file(record_dir, "record.json", rec_payload)
        placeholder = content.replace("report-section:Monitoring signals", f"audit-record:{rel}#r1@2026-08-18T10:00:00Z", 1)
        placeholder = placeholder.replace('"evidence": "report-section:Monitoring signals"', f'"evidence": "audit-record:{rel}#r1@2026-08-18T10:00:00Z"', 1)
        report_tmp.write_text(placeholder, encoding="utf-8")
        rec_path.write_text(json.dumps(rec_payload), encoding="utf-8")
        proc = _run_report(report_tmp, "--strict", "--require-contract", "--json")
        assert proc.returncode == 2, proc.stdout
        data = json.loads(proc.stdout)
        assert any("artifact_id" in b or "artifact" in b.lower() for b in data["blocking"])
    finally:
        shutil.rmtree(record_dir, ignore_errors=True)


def test_audit_record_execution_source_mismatch_cannot_pass(tmp_path: Path) -> None:
    """P2 regression: manual audit cannot be backed by process record."""
    record_dir = _make_record_dir()
    try:
        content = POS.read_text(encoding="utf-8")
        report_tmp = tmp_path / "report.md"
        rec_payload: dict = {"records": [{"record_id": "r1", "recorded_at": "2026-08-18T10:00:00Z", "audit_id": "market-outlook-audit", "status": "passed", "artifact_id": "placeholder", "executed_at": "2026-08-18T10:00:00Z", "execution_source": "process_node_evidence", "evidence": "report-section:Monitoring signals", "route": "market-outlook"}]}
        rec_path, rel = _write_record_file(record_dir, "record.json", rec_payload)
        placeholder = content.replace("report-section:Monitoring signals", f"audit-record:{rel}#r1@2026-08-18T10:00:00Z", 1)
        placeholder = placeholder.replace('"evidence": "report-section:Monitoring signals"', f'"evidence": "audit-record:{rel}#r1@2026-08-18T10:00:00Z"', 1)
        m = re.search(r'"artifact_id"\s*:\s*"([^"]+)"', placeholder)
        aid = m.group(1) if m else "fixture-market-outlook-pos"
        report_tmp.write_text(placeholder, encoding="utf-8")
        rec_payload["records"][0]["artifact_id"] = aid
        rec_path.write_text(json.dumps(rec_payload), encoding="utf-8")
        proc = _run_report(report_tmp, "--strict", "--require-contract", "--json")
        assert proc.returncode == 2, proc.stdout
        data = json.loads(proc.stdout)
        assert any("execution_source" in b for b in data["blocking"])
    finally:
        shutil.rmtree(record_dir, ignore_errors=True)


def test_audit_record_legacy_source_cannot_pass(tmp_path: Path) -> None:
    """P2 regression: legacy_self_attested record must not be trusted in strict."""
    record_dir = _make_record_dir()
    try:
        content = POS.read_text(encoding="utf-8")
        report_tmp = tmp_path / "report.md"
        rec_payload: dict = {"records": [{"record_id": "r1", "recorded_at": "2026-08-18T10:00:00Z", "audit_id": "market-outlook-audit", "status": "passed", "artifact_id": "placeholder", "executed_at": "2026-08-18T10:00:00Z", "execution_source": "legacy_self_attested", "evidence": "report-section:Monitoring signals", "route": "market-outlook"}]}
        rec_path, rel = _write_record_file(record_dir, "record.json", rec_payload)
        placeholder = content.replace("report-section:Monitoring signals", f"audit-record:{rel}#r1@2026-08-18T10:00:00Z", 1)
        placeholder = placeholder.replace('"evidence": "report-section:Monitoring signals"', f'"evidence": "audit-record:{rel}#r1@2026-08-18T10:00:00Z"', 1)
        m = re.search(r'"artifact_id"\s*:\s*"([^"]+)"', placeholder)
        aid = m.group(1) if m else "fixture-market-outlook-pos"
        report_tmp.write_text(placeholder, encoding="utf-8")
        rec_payload["records"][0]["artifact_id"] = aid
        rec_path.write_text(json.dumps(rec_payload), encoding="utf-8")
        proc = _run_report(report_tmp, "--strict", "--require-contract", "--json")
        assert proc.returncode == 2, proc.stdout
        data = json.loads(proc.stdout)
        assert any("execution_source" in b for b in data["blocking"])
    finally:
        shutil.rmtree(record_dir, ignore_errors=True)


def test_audit_record_missing_execution_source_cannot_pass(tmp_path: Path) -> None:
    """P1-blocker: record without execution_source must not obtain trusted pass and must not be伪造为 manual."""
    record_dir = _make_record_dir()
    try:
        content = POS.read_text(encoding="utf-8")
        report_tmp = tmp_path / "report.md"
        rec_payload: dict = {"records": [{"record_id": "r1", "recorded_at": "2026-08-18T10:00:00Z", "audit_id": "market-outlook-audit", "status": "passed", "artifact_id": "placeholder", "executed_at": "2026-08-18T10:00:00Z", "evidence": "report-section:Monitoring signals", "route": "market-outlook"}]}
        rec_path, rel = _write_record_file(record_dir, "record.json", rec_payload)
        placeholder = content.replace("report-section:Monitoring signals", f"audit-record:{rel}#r1@2026-08-18T10:00:00Z", 1)
        placeholder = placeholder.replace('"evidence": "report-section:Monitoring signals"', f'"evidence": "audit-record:{rel}#r1@2026-08-18T10:00:00Z"', 1)
        m = re.search(r'"artifact_id"\s*:\s*"([^"]+)"', placeholder)
        aid = m.group(1) if m else "fixture-market-outlook-pos"
        report_tmp.write_text(placeholder, encoding="utf-8")
        rec_payload["records"][0]["artifact_id"] = aid
        rec_path.write_text(json.dumps(rec_payload), encoding="utf-8")
        proc = _run_report(report_tmp, "--strict", "--require-contract", "--json")
        assert proc.returncode == 2, proc.stdout
        data = json.loads(proc.stdout)
        assert any("execution_source" in b.lower() and "missing" in b.lower() for b in data["blocking"])
        audit = next(a for a in data["audits"] if a["audit_id"] == "market-outlook-audit")
        assert audit["status"] != "pass"
        # P2: missing source must not be displayed as trusted attestation
        assert audit["execution_source"] != "manual_checklist_attestation", "missing source should not be shown as trusted attestation"
    finally:
        shutil.rmtree(record_dir, ignore_errors=True)


def test_audit_record_missing_evidence_cannot_pass(tmp_path: Path) -> None:
    """P1-blocker: record that only self-declares passed without referencing checklist/section must not pass."""
    record_dir = _make_record_dir()
    try:
        content = POS.read_text(encoding="utf-8")
        report_tmp = tmp_path / "report.md"
        rec_payload: dict = {"records": [{"record_id": "r1", "recorded_at": "2026-08-18T10:00:00Z", "audit_id": "market-outlook-audit", "status": "passed", "artifact_id": "placeholder", "executed_at": "2026-08-18T10:00:00Z", "execution_source": "manual_checklist_attestation", "route": "market-outlook"}]}
        rec_path, rel = _write_record_file(record_dir, "record.json", rec_payload)
        placeholder = content.replace("report-section:Monitoring signals", f"audit-record:{rel}#r1@2026-08-18T10:00:00Z", 1)
        placeholder = placeholder.replace('"evidence": "report-section:Monitoring signals"', f'"evidence": "audit-record:{rel}#r1@2026-08-18T10:00:00Z"', 1)
        m = re.search(r'"artifact_id"\s*:\s*"([^"]+)"', placeholder)
        aid = m.group(1) if m else "fixture-market-outlook-pos"
        report_tmp.write_text(placeholder, encoding="utf-8")
        rec_payload["records"][0]["artifact_id"] = aid
        rec_path.write_text(json.dumps(rec_payload), encoding="utf-8")
        proc = _run_report(report_tmp, "--strict", "--require-contract", "--json")
        assert proc.returncode == 2, proc.stdout
        data = json.loads(proc.stdout)
        assert any("evidence" in b.lower() and "missing" in b.lower() for b in data["blocking"])
    finally:
        shutil.rmtree(record_dir, ignore_errors=True)


def test_audit_record_duplicate_cannot_pass(tmp_path: Path) -> None:
    """P1/P2: duplicate record (same id+timestamp) must fail closed, order-independent."""
    record_dir = _make_record_dir()
    try:
        content = POS.read_text(encoding="utf-8")
        report_tmp = tmp_path / "report.md"
        # Two records with same id+timestamp but different status/evidence - should be ambiguous
        rec_payload = {"records": [
            {"record_id": "r1", "recorded_at": "2026-08-18T10:00:00Z", "audit_id": "market-outlook-audit", "status": "passed", "artifact_id": "placeholder", "executed_at": "2026-08-18T10:00:00Z", "execution_source": "manual_checklist_attestation", "evidence": "report-section:Monitoring signals", "route": "market-outlook"},
            {"record_id": "r1", "recorded_at": "2026-08-18T10:00:00Z", "audit_id": "market-outlook-audit", "status": "partial", "artifact_id": "placeholder", "executed_at": "2026-08-18T10:00:00Z", "execution_source": "manual_checklist_attestation", "evidence": "report-section:Monitoring signals", "route": "market-outlook"},
        ]}
        rec_path, rel = _write_record_file(record_dir, "record.json", rec_payload)
        placeholder = content.replace("report-section:Monitoring signals", f"audit-record:{rel}#r1@2026-08-18T10:00:00Z", 1)
        placeholder = placeholder.replace('"evidence": "report-section:Monitoring signals"', f'"evidence": "audit-record:{rel}#r1@2026-08-18T10:00:00Z"', 1)
        m = re.search(r'"artifact_id"\s*:\s*"([^"]+)"', placeholder)
        aid = m.group(1) if m else "fixture-market-outlook-pos"
        report_tmp.write_text(placeholder, encoding="utf-8")
        for rec in rec_payload["records"]:
            rec["artifact_id"] = aid
        rec_path.write_text(json.dumps(rec_payload), encoding="utf-8")
        proc = _run_report(report_tmp, "--strict", "--require-contract", "--json")
        assert proc.returncode == 2, proc.stdout
        data = json.loads(proc.stdout)
        assert any("ambiguous" in b.lower() or "duplicate" in b.lower() for b in data["blocking"])
        # Also test reverse order (partial first, passed second) must also fail
        rec_payload["records"] = list(reversed(rec_payload["records"]))
        rec_path.write_text(json.dumps(rec_payload), encoding="utf-8")
        proc2 = _run_report(report_tmp, "--strict", "--require-contract", "--json")
        assert proc2.returncode == 2, proc2.stdout
        assert any("ambiguous" in b.lower() or "duplicate" in b.lower() for b in json.loads(proc2.stdout)["blocking"])
    finally:
        shutil.rmtree(record_dir, ignore_errors=True)


def test_audit_record_wrong_route_cannot_pass(tmp_path: Path) -> None:
    """P2: route binding - record for different route must not pass."""
    record_dir = _make_record_dir()
    try:
        content = POS.read_text(encoding="utf-8")
        report_tmp = tmp_path / "report.md"
        rec_payload: dict = {"records": [{"record_id": "r1", "recorded_at": "2026-08-18T10:00:00Z", "audit_id": "market-outlook-audit", "status": "passed", "artifact_id": "placeholder", "executed_at": "2026-08-18T10:00:00Z", "execution_source": "manual_checklist_attestation", "evidence": "report-section:Monitoring signals", "route": "technical-deep-dive"}]}
        rec_path, rel = _write_record_file(record_dir, "record.json", rec_payload)
        placeholder = content.replace("report-section:Monitoring signals", f"audit-record:{rel}#r1@2026-08-18T10:00:00Z", 1)
        placeholder = placeholder.replace('"evidence": "report-section:Monitoring signals"', f'"evidence": "audit-record:{rel}#r1@2026-08-18T10:00:00Z"', 1)
        m = re.search(r'"artifact_id"\s*:\s*"([^"]+)"', placeholder)
        aid = m.group(1) if m else "fixture-market-outlook-pos"
        report_tmp.write_text(placeholder, encoding="utf-8")
        rec_payload["records"][0]["artifact_id"] = aid
        rec_path.write_text(json.dumps(rec_payload), encoding="utf-8")
        proc = _run_report(report_tmp, "--strict", "--require-contract", "--json")
        assert proc.returncode == 2, proc.stdout
        data = json.loads(proc.stdout)
        assert any("route" in b.lower() and ("mismatch" in b.lower() or "does not match" in b.lower()) for b in data["blocking"])
    finally:
        shutil.rmtree(record_dir, ignore_errors=True)


def test_json_distinguishes_execution_sources(tmp_path: Path) -> None:
    # Positive fixture already distinguishes manual vs automated
    proc = subprocess.run([sys.executable, str(SCRIPT), str(POS), "--research-pack", str(PACK), "--strict", "--require-contract", "--json"], capture_output=True, text=True)
    assert proc.returncode == 0
    data = json.loads(proc.stdout)
    sources = {a["execution_source"] for a in data["audits"]}
    assert "manual_checklist_attestation" in sources
    assert "automated_validator" in sources
    # legacy in compatibility mode
    content = POS.read_text().replace("report-section:Monitoring signals", "free-form evidence", 1)
    report = tmp_path / "legacy.md"
    report.write_text(content)
    proc2 = subprocess.run([sys.executable, str(SCRIPT), str(report), "--research-pack", str(PACK), "--json"], capture_output=True, text=True)
    data2 = json.loads(proc2.stdout)
    manual = next(a for a in data2["audits"] if a["audit_id"] == "market-outlook-audit")
    assert manual["execution_source"] == "legacy_self_attested"
    # process_node_evidence presence: mid-research-review-audit via shared-workflow pack
    # Use a direct audit_evidence check for process
    from audit_evidence import validate_evidence_reference
    rec_dir = _make_record_dir()
    try:
        payload = {"records": [{"record_id": "p1", "recorded_at": "2026-08-18T10:00:00Z", "audit_id": "mid-research-review-audit", "status": "passed", "artifact_id": "proc-artifact-1", "executed_at": "2026-08-18T10:00:00Z", "execution_source": "process_node_evidence", "evidence": "report-section:Monitoring signals", "route": "market-outlook"}]}
        rec_path, rel = _write_record_file(rec_dir, "prec.json", payload)
        res = validate_evidence_reference(f"audit-record:{rel}#p1@2026-08-18T10:00:00Z", base_dir=ROOT, strict=True, execution_type="process", expected_audit_id="mid-research-review-audit", expected_route="market-outlook", artifact_text="## Monitoring signals\n\ncontent")
        assert res.is_valid, res.errors
        assert res.provenance and res.provenance["verified"] is True
    finally:
        shutil.rmtree(rec_dir, ignore_errors=True)


def test_nested_report_section_only_in_pack_must_fail(tmp_path: Path) -> None:
    """P1/P2: report-section evidence that exists only in pack must not be verified against report."""
    from audit_evidence import validate_evidence_reference
    rec_dir = _make_record_dir()
    try:
        # Pack has ## Artifact contract, report fixture does not
        pack_text = "## Artifact contract\n\ncontract body\n"
        report_text = "## Monitoring signals\n\nsignals\n"
        payload = {"records": [{"record_id": "r1", "recorded_at": "2026-08-18T10:00:00Z", "audit_id": "market-outlook-audit", "status": "passed", "artifact_id": "test-artifact", "executed_at": "2026-08-18T10:00:00Z", "execution_source": "manual_checklist_attestation", "evidence": "report-section:Artifact contract", "route": "market-outlook"}]}
        rec_path, rel = _write_record_file(rec_dir, "r.json", payload)
        # Validate as report audit: report_text is report_text (without Artifact contract), pack_text is pack_text
        # Inner report-section:Artifact contract should fail because it's not in report_text
        res = validate_evidence_reference(
            f"audit-record:{rel}#r1@2026-08-18T10:00:00Z",
            base_dir=ROOT,
            strict=True,
            execution_type="manual",
            expected_audit_id="market-outlook-audit",
                        expected_artifact_id="test-artifact",
            expected_route="market-outlook",
            artifact_text=report_text,
            report_text=report_text,
            pack_text=pack_text,
        )
        assert not res.is_valid, "report-section that only exists in pack should not verify against report"
        assert any("Artifact contract" in e for e in res.errors)
    finally:
        shutil.rmtree(rec_dir, ignore_errors=True)


def test_nested_pack_section_only_in_report_must_fail(tmp_path: Path) -> None:
    """P1/P2: pack-section evidence that exists only in report must not be verified against pack."""
    from audit_evidence import validate_evidence_reference
    rec_dir = _make_record_dir()
    try:
        # Report has Monitoring signals, pack has Artifact contract only
        pack_text = "## Artifact contract\n\ncontract body\n"
        report_text = "## Monitoring signals\n\nsignals\n"
        payload = {"records": [{"record_id": "r1", "recorded_at": "2026-08-18T10:00:00Z", "audit_id": "market-outlook-audit", "status": "passed", "artifact_id": "test-artifact", "executed_at": "2026-08-18T10:00:00Z", "execution_source": "manual_checklist_attestation", "evidence": "pack-section:Monitoring signals", "route": "market-outlook"}]}
        rec_path, rel = _write_record_file(rec_dir, "r.json", payload)
        # Validate via research_pack context: artifact_text is pack, report_text is report
        # Inner pack-section:Monitoring signals should fail because pack_text doesn't have it
        res = validate_evidence_reference(
            f"audit-record:{rel}#r1@2026-08-18T10:00:00Z",
            base_dir=ROOT,
            strict=True,
            execution_type="manual",
            expected_audit_id="market-outlook-audit",
                        expected_artifact_id="test-artifact",
            expected_route="market-outlook",
            artifact_text=pack_text,
            artifact_label="pack",
            report_text=report_text,
            pack_text=pack_text,
        )
        assert not res.is_valid, "pack-section that only exists in report should not verify against pack"
        assert any("Monitoring signals" in e for e in res.errors)
    finally:
        shutil.rmtree(rec_dir, ignore_errors=True)


def test_report_context_rejects_pack_evidence_without_pack_text(tmp_path: Path) -> None:
    """Report context without pack_text must reject pack-scoped evidence."""
    from audit_evidence import validate_evidence_reference
    rec_dir = _make_record_dir()
    try:
        payload = {"records": [{"record_id": "r1", "recorded_at": "2026-08-18T10:00:00Z", "audit_id": "market-outlook-audit", "status": "passed", "artifact_id": "art", "executed_at": "2026-08-18T10:00:00Z", "execution_source": "manual_checklist_attestation", "evidence": "pack-section:Artifact contract", "route": "market-outlook"}]}
        rec_path, rel = _write_record_file(rec_dir, "r.json", payload)
        # Report-only context: no pack_text
        res = validate_evidence_reference(
            f"audit-record:{rel}#r1@2026-08-18T10:00:00Z",
            base_dir=ROOT,
            strict=True,
            execution_type="manual",
            expected_audit_id="market-outlook-audit",
                        expected_artifact_id="art",
            expected_route="market-outlook",
            artifact_text="## Monitoring signals\n",
            artifact_label="report",
            report_text="## Monitoring signals\n",
            pack_text=None,
        )
        assert not res.is_valid
        assert any("pack" in e.lower() and "not allowed" in e.lower() for e in res.errors)
    finally:
        shutil.rmtree(rec_dir, ignore_errors=True)


def test_report_template_does_not_advertise_direct_checklist_item_as_strict_valid() -> None:
    """Regression: canonical report-template must not teach bare checklist-item as strict Passed evidence."""
    text = (ROOT / "references" / "report-template.md").read_text(encoding="utf-8")
    # Find the evidence row for Passed
    passed_idx = text.find("已通过 (Passed)")
    assert passed_idx != -1, "template must contain Passed evidence description"
    # The next ~500 chars after that header should contain the allowed references
    snippet = text[passed_idx : passed_idx + 800]
    # It must mention audit-record as allowed
    assert "audit-record:" in snippet, "template should advertise audit-record for Passed"
    # It must NOT list checklist-item as a direct allowed Passed evidence without qualification
    # Extract the line that lists the allowed refs (starts with ✅ or contains report-section)
    lines = snippet.split("\n")
    allowed_line = next((l for l in lines if "report-section" in l and "audit-record" in l), "")
    assert allowed_line, "could not find allowed evidence line"
    assert "checklist-item" not in allowed_line, "direct checklist-item must not be listed as standalone Passed evidence"
    # Must contain the clarifying note that checklist-item is definition-only and must be via audit-record
    assert "only identifies a checklist definition" in text
    assert "must be referenced from an artifact-bound" in text
