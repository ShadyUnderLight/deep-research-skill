"""Issue #401 negatives: checklist definition cannot masquerade as execution evidence.

Covers the acceptance criteria:

- checklist marker alone (even if exists) cannot obtain trusted pass in strict
- forged item id, missing checklist, unchecked template (all strict) -> partial/not_run
- audit-record missing / status != passed / artifact mismatch / audit_id mismatch -> fail closed
- valid audit-record with artifact binding -> pass
- JSON distinguishes 4 execution sources
"""

from __future__ import annotations

import hashlib
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
    """Create an isolated directory under ROOT/tmp for audit-record files.

    Using a unique subdir under ROOT/tmp keeps the relative locator inside the
    repository root (required by _safe_path) while avoiding collisions and
    allowing safe cleanup without touching the shared tmp/ directory itself.
    """
    base = ROOT / "tmp"
    base.mkdir(parents=True, exist_ok=True)
    # mkdtemp under base gives a unique isolated folder like tmp/tmpxxx
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
        # temporary placeholder to compute aid
        m = re.search(r'"artifact_id"\s*:\s*"([^"]+)"', placeholder)
        aid = m.group(1) if m else "fixture-market-outlook-pos"
        # create isolated record file
        rec_payload = {"records": [{"record_id": "r1", "recorded_at": "2026-08-18T10:00:00Z", "audit_id": "market-outlook-audit", "status": "partial", "artifact_sha256": "x"*64, "artifact_id": aid, "executed_at": "2026-08-18T10:00:00Z"}]}
        rec_path, rel = _write_record_file(record_dir, "record.json", rec_payload)
        # patch placeholder to use real rel
        placeholder = content.replace("report-section:Monitoring signals", f"audit-record:{rel}#r1@2026-08-18T10:00:00Z", 1)
        placeholder = placeholder.replace('"evidence": "report-section:Monitoring signals"', f'"evidence": "audit-record:{rel}#r1@2026-08-18T10:00:00Z"', 1)
        report_tmp.write_text(placeholder, encoding="utf-8")
        sha2 = hashlib.sha256(report_tmp.read_bytes()).hexdigest()
        rec_payload["records"][0]["artifact_sha256"] = sha2
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
        rec_payload = {"records": [{"record_id": "r1", "recorded_at": "2026-08-18T10:00:00Z", "audit_id": "market-outlook-audit", "status": "passed", "artifact_sha256": "0"*64, "artifact_id": "some-other-artifact", "executed_at": "2026-08-18T10:00:00Z"}]}
        rec_path, rel = _write_record_file(record_dir, "record.json", rec_payload)
        placeholder = content.replace("report-section:Monitoring signals", f"audit-record:{rel}#r1@2026-08-18T10:00:00Z", 1)
        placeholder = placeholder.replace('"evidence": "report-section:Monitoring signals"', f'"evidence": "audit-record:{rel}#r1@2026-08-18T10:00:00Z"', 1)
        report_tmp.write_text(placeholder, encoding="utf-8")
        proc = _run_report(report_tmp, "--strict", "--require-contract", "--json")
        assert proc.returncode == 2, proc.stdout
        data = json.loads(proc.stdout)
        # Each provided artifact field is now independently fail-closed (P1)
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
        # pre-write to compute sha
        tmp_placeholder = placeholder.replace("audit-record:tmp/placeholder#r1@2026-08-18T10:00:00Z", "audit-record:tmp/dummy#r1@2026-08-18T10:00:00Z", 1)
        report_tmp.write_text(tmp_placeholder, encoding="utf-8")
        sha_probe = hashlib.sha256(report_tmp.read_bytes()).hexdigest()
        rec_payload = {"records": [{"record_id": "r1", "recorded_at": "2026-08-18T10:00:00Z", "audit_id": "final-audit", "status": "passed", "artifact_sha256": sha_probe, "artifact_id": aid, "executed_at": "2026-08-18T10:00:00Z"}]}
        rec_path, rel = _write_record_file(record_dir, "record.json", rec_payload)
        placeholder = content.replace("report-section:Monitoring signals", f"audit-record:{rel}#r1@2026-08-18T10:00:00Z", 1)
        placeholder = placeholder.replace('"evidence": "report-section:Monitoring signals"', f'"evidence": "audit-record:{rel}#r1@2026-08-18T10:00:00Z"', 1)
        report_tmp.write_text(placeholder, encoding="utf-8")
        sha = hashlib.sha256(report_tmp.read_bytes()).hexdigest()
        rec_payload["records"][0]["artifact_sha256"] = sha
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
        rec_payload: dict = {"records": [{"record_id": "r1", "recorded_at": "2026-08-18T10:00:00Z", "audit_id": "market-outlook-audit", "status": "passed", "artifact_sha256": "placeholder", "artifact_id": "fixture-market-outlook-pos", "executed_at": "2026-08-18T10:00:00Z", "execution_source": "manual_checklist_attestation"}]}
        rec_path, rel = _write_record_file(record_dir, "record.json", rec_payload)
        placeholder = content.replace("report-section:Monitoring signals", f"audit-record:{rel}#r1@2026-08-18T10:00:00Z", 1)
        placeholder = placeholder.replace('"evidence": "report-section:Monitoring signals"', f'"evidence": "audit-record:{rel}#r1@2026-08-18T10:00:00Z"', 1)
        # Extract aid
        m = re.search(r'"artifact_id"\s*:\s*"([^"]+)"', placeholder)
        aid = m.group(1) if m else "fixture-market-outlook-pos"
        report_tmp.write_text(placeholder, encoding="utf-8")
        sha = hashlib.sha256(report_tmp.read_bytes()).hexdigest()
        rec_payload["records"][0]["artifact_sha256"] = sha
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
    finally:
        shutil.rmtree(record_dir, ignore_errors=True)


def test_audit_record_hash_mismatch_even_if_id_matches_cannot_pass(tmp_path: Path) -> None:
    """P1 regression: id correct but hash wrong must still fail (AND semantics)."""
    record_dir = _make_record_dir()
    try:
        content = POS.read_text(encoding="utf-8")
        report_tmp = tmp_path / "report.md"
        rec_payload: dict = {"records": [{"record_id": "r1", "recorded_at": "2026-08-18T10:00:00Z", "audit_id": "market-outlook-audit", "status": "passed", "artifact_sha256": "0"*64, "artifact_id": "fixture-market-outlook-pos", "executed_at": "2026-08-18T10:00:00Z"}]}
        rec_path, rel = _write_record_file(record_dir, "record.json", rec_payload)
        placeholder = content.replace("report-section:Monitoring signals", f"audit-record:{rel}#r1@2026-08-18T10:00:00Z", 1)
        placeholder = placeholder.replace('"evidence": "report-section:Monitoring signals"', f'"evidence": "audit-record:{rel}#r1@2026-08-18T10:00:00Z"', 1)
        m = re.search(r'"artifact_id"\s*:\s*"([^"]+)"', placeholder)
        aid = m.group(1) if m else "fixture-market-outlook-pos"
        placeholder = placeholder.replace("some-other-artifact", aid)  # ensure id will match
        report_tmp.write_text(placeholder, encoding="utf-8")
        sha = hashlib.sha256(report_tmp.read_bytes()).hexdigest()
        # Intentionally keep wrong hash (0*64) but correct id
        rec_payload["records"][0]["artifact_sha256"] = "0"*64
        rec_payload["records"][0]["artifact_id"] = aid
        rec_path.write_text(json.dumps(rec_payload), encoding="utf-8")
        proc = _run_report(report_tmp, "--strict", "--require-contract", "--json")
        assert proc.returncode == 2, proc.stdout
        data = json.loads(proc.stdout)
        # Should fail on sha mismatch even though id matched
        assert any("artifact_sha256" in b or "artifact" in b.lower() for b in data["blocking"])
        assert any("does not match" in b for b in data["blocking"])
    finally:
        shutil.rmtree(record_dir, ignore_errors=True)


def test_audit_record_id_mismatch_even_if_hash_matches_cannot_pass(tmp_path: Path) -> None:
    """P1 regression: hash correct but id wrong must still fail."""
    record_dir = _make_record_dir()
    try:
        content = POS.read_text(encoding="utf-8")
        report_tmp = tmp_path / "report.md"
        # First compute real sha
        rec_payload: dict = {"records": [{"record_id": "r1", "recorded_at": "2026-08-18T10:00:00Z", "audit_id": "market-outlook-audit", "status": "passed", "artifact_sha256": "placeholder", "artifact_id": "wrong-id", "executed_at": "2026-08-18T10:00:00Z"}]}
        rec_path, rel = _write_record_file(record_dir, "record.json", rec_payload)
        placeholder = content.replace("report-section:Monitoring signals", f"audit-record:{rel}#r1@2026-08-18T10:00:00Z", 1)
        placeholder = placeholder.replace('"evidence": "report-section:Monitoring signals"', f'"evidence": "audit-record:{rel}#r1@2026-08-18T10:00:00Z"', 1)
        report_tmp.write_text(placeholder, encoding="utf-8")
        sha = hashlib.sha256(report_tmp.read_bytes()).hexdigest()
        rec_payload["records"][0]["artifact_sha256"] = sha
        rec_payload["records"][0]["artifact_id"] = "wrong-id"
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
        rec_payload: dict = {"records": [{"record_id": "r1", "recorded_at": "2026-08-18T10:00:00Z", "audit_id": "market-outlook-audit", "status": "passed", "artifact_sha256": "placeholder", "artifact_id": "placeholder", "executed_at": "2026-08-18T10:00:00Z", "execution_source": "process_node_evidence"}]}
        rec_path, rel = _write_record_file(record_dir, "record.json", rec_payload)
        placeholder = content.replace("report-section:Monitoring signals", f"audit-record:{rel}#r1@2026-08-18T10:00:00Z", 1)
        placeholder = placeholder.replace('"evidence": "report-section:Monitoring signals"', f'"evidence": "audit-record:{rel}#r1@2026-08-18T10:00:00Z"', 1)
        m = re.search(r'"artifact_id"\s*:\s*"([^"]+)"', placeholder)
        aid = m.group(1) if m else "fixture-market-outlook-pos"
        report_tmp.write_text(placeholder, encoding="utf-8")
        sha = hashlib.sha256(report_tmp.read_bytes()).hexdigest()
        rec_payload["records"][0]["artifact_sha256"] = sha
        rec_payload["records"][0]["artifact_id"] = aid
        # keep process source (mismatch for manual)
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
        rec_payload: dict = {"records": [{"record_id": "r1", "recorded_at": "2026-08-18T10:00:00Z", "audit_id": "market-outlook-audit", "status": "passed", "artifact_sha256": "placeholder", "artifact_id": "placeholder", "executed_at": "2026-08-18T10:00:00Z", "execution_source": "legacy_self_attested"}]}
        rec_path, rel = _write_record_file(record_dir, "record.json", rec_payload)
        placeholder = content.replace("report-section:Monitoring signals", f"audit-record:{rel}#r1@2026-08-18T10:00:00Z", 1)
        placeholder = placeholder.replace('"evidence": "report-section:Monitoring signals"', f'"evidence": "audit-record:{rel}#r1@2026-08-18T10:00:00Z"', 1)
        m = re.search(r'"artifact_id"\s*:\s*"([^"]+)"', placeholder)
        aid = m.group(1) if m else "fixture-market-outlook-pos"
        report_tmp.write_text(placeholder, encoding="utf-8")
        sha = hashlib.sha256(report_tmp.read_bytes()).hexdigest()
        rec_payload["records"][0]["artifact_sha256"] = sha
        rec_payload["records"][0]["artifact_id"] = aid
        rec_path.write_text(json.dumps(rec_payload), encoding="utf-8")
        proc = _run_report(report_tmp, "--strict", "--require-contract", "--json")
        assert proc.returncode == 2, proc.stdout
        data = json.loads(proc.stdout)
        assert any("execution_source" in b for b in data["blocking"])
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
    # Simulate process record validation
    rec_dir = _make_record_dir()
    try:
        payload = {"records": [{"record_id": "p1", "recorded_at": "2026-08-18T10:00:00Z", "audit_id": "mid-research-review-audit", "status": "passed", "artifact_sha256": "b"*64, "executed_at": "2026-08-18T10:00:00Z", "execution_source": "process_node_evidence"}]}
        rec_path, rel = _write_record_file(rec_dir, "prec.json", payload)
        # Validate as process
        res = validate_evidence_reference(f"audit-record:{rel}#p1@2026-08-18T10:00:00Z", base_dir=ROOT, strict=True, execution_type="process", expected_audit_id="mid-research-review-audit", expected_artifact_sha256="b"*64)
        assert res.is_valid, res.errors
        assert res.provenance and res.provenance["verified"] is True
    finally:
        shutil.rmtree(rec_dir, ignore_errors=True)
