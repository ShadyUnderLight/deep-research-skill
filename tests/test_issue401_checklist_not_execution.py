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
    # Replace the first occurrence (status block) and the contract block's first matching audit
    content = content.replace("report-section:Monitoring signals", evidence_locator, 1)
    # Contract block also contains the same locator for forward-looking etc.; leave other audits untouched
    # For market-outlook-audit only, we replaced one; the contract still references the same locator for that audit
    # Ensure contract's market-outlook-audit evidence is also updated if it still references the old locator
    # The contract audit list includes market-outlook-audit as first entry; we handle both by second replace
    if content.count("report-section:Monitoring signals") >= 1:
        # The remaining occurrences are for other audits (forward-looking, etc.); keep them as-is for positive path
        # But for our negative test we only care about market-outlook-audit, which is the first replacement above
        pass
    # If the evidence_locator is audit-record, also patch contract block to match (so contract validation sees same)
    if evidence_locator.startswith("audit-record:"):
        # contract block's market-outlook-audit evidence is the first audit entry; patch it similarly
        # Do a targeted JSON replace for that specific audit id
        content = content.replace(
            '"id": "market-outlook-audit", "status": "passed", "evidence": "report-section:Monitoring signals"',
            f'"id": "market-outlook-audit", "status": "passed", "evidence": "{evidence_locator}"',
        )
        # Fallback for fixtures where contract formatting differs slightly
        if f'"evidence": "{evidence_locator}"' not in content:
            # Already patched via first replace if contract used same string
            pass
    report = tmp_path / "report.md"
    report.write_text(content, encoding="utf-8")
    # When evidence is audit-record pointing to tmp/test_record.json, we must also ensure the contract's evidence matches,
    # otherwise contract validation will still reference report-section and pass while status block fails. That's intentional
    # for checklist-only negatives where contract still passes but status block fails -> overall still fail.
    return report


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
    # Prepare a record with status=partial and correct artifact binding
    content = POS.read_text(encoding="utf-8")
    report_tmp = tmp_path / "report.md"
    # First write a placeholder report to compute sha/artifact_id
    placeholder = content.replace("report-section:Monitoring signals", "audit-record:tmp/issue401_partial.json#r1@2026-08-18T10:00:00Z", 1)
    report_tmp.write_text(placeholder, encoding="utf-8")
    sha = hashlib.sha256(report_tmp.read_bytes()).hexdigest()
    # Extract artifact_id
    m = re.search(r'"artifact_id"\s*:\s*"([^"]+)"', placeholder)
    aid = m.group(1) if m else "fixture-market-outlook-pos"
    # Write record
    rec_path = ROOT / "tmp" / "issue401_partial.json"
    rec_path.parent.mkdir(parents=True, exist_ok=True)
    rec_path.write_text(json.dumps({"records": [{"record_id": "r1", "recorded_at": "2026-08-18T10:00:00Z", "audit_id": "market-outlook-audit", "status": "partial", "artifact_sha256": sha, "artifact_id": aid, "executed_at": "2026-08-18T10:00:00Z"}]}), encoding="utf-8")
    # Also patch contract block to reference same record
    placeholder = placeholder.replace('"evidence": "report-section:Monitoring signals"', '"evidence": "audit-record:tmp/issue401_partial.json#r1@2026-08-18T10:00:00Z"', 1)
    # Need to recompute sha after contract patch
    report_tmp.write_text(placeholder, encoding="utf-8")
    sha2 = hashlib.sha256(report_tmp.read_bytes()).hexdigest()
    rec_path.write_text(json.dumps({"records": [{"record_id": "r1", "recorded_at": "2026-08-18T10:00:00Z", "audit_id": "market-outlook-audit", "status": "partial", "artifact_sha256": sha2, "artifact_id": aid, "executed_at": "2026-08-18T10:00:00Z"}]}), encoding="utf-8")
    proc = _run_report(report_tmp, "--strict", "--require-contract", "--json")
    # cleanup
    try:
        rec_path.unlink(missing_ok=True)
        try:
            rec_path.parent.rmdir()
        except OSError:
            pass
    except Exception:
        pass
    assert proc.returncode == 2, proc.stdout
    data = json.loads(proc.stdout)
    assert data["overall"] != "pass"
    assert any("status" in b.lower() and "not passed" in b.lower() for b in data["blocking"])


def test_audit_record_wrong_artifact_cannot_pass(tmp_path: Path) -> None:
    content = POS.read_text(encoding="utf-8")
    report_tmp = tmp_path / "report.md"
    placeholder = content.replace("report-section:Monitoring signals", "audit-record:tmp/issue401_wrong_artifact.json#r1@2026-08-18T10:00:00Z", 1)
    placeholder = placeholder.replace('"evidence": "report-section:Monitoring signals"', '"evidence": "audit-record:tmp/issue401_wrong_artifact.json#r1@2026-08-18T10:00:00Z"', 1)
    report_tmp.write_text(placeholder, encoding="utf-8")
    sha = hashlib.sha256(report_tmp.read_bytes()).hexdigest()
    m = re.search(r'"artifact_id"\s*:\s*"([^"]+)"', placeholder)
    aid = m.group(1) if m else "fixture-market-outlook-pos"
    rec_path = ROOT / "tmp" / "issue401_wrong_artifact.json"
    rec_path.parent.mkdir(parents=True, exist_ok=True)
    # Intentionally write a different artifact binding
    rec_path.write_text(json.dumps({"records": [{"record_id": "r1", "recorded_at": "2026-08-18T10:00:00Z", "audit_id": "market-outlook-audit", "status": "passed", "artifact_sha256": "0"*64, "artifact_id": "some-other-artifact", "executed_at": "2026-08-18T10:00:00Z"}]}), encoding="utf-8")
    proc = _run_report(report_tmp, "--strict", "--require-contract", "--json")
    try:
        rec_path.unlink(missing_ok=True)
        try:
            rec_path.parent.rmdir()
        except OSError:
            pass
    except Exception:
        pass
    assert proc.returncode == 2, proc.stdout
    data = json.loads(proc.stdout)
    assert any("artifact" in b.lower() and "mismatch" in b.lower() for b in data["blocking"])


def test_audit_record_wrong_audit_id_cannot_pass(tmp_path: Path) -> None:
    content = POS.read_text(encoding="utf-8")
    report_tmp = tmp_path / "report.md"
    placeholder = content.replace("report-section:Monitoring signals", "audit-record:tmp/issue401_wrong_audit.json#r1@2026-08-18T10:00:00Z", 1)
    placeholder = placeholder.replace('"evidence": "report-section:Monitoring signals"', '"evidence": "audit-record:tmp/issue401_wrong_audit.json#r1@2026-08-18T10:00:00Z"', 1)
    report_tmp.write_text(placeholder, encoding="utf-8")
    sha = hashlib.sha256(report_tmp.read_bytes()).hexdigest()
    m = re.search(r'"artifact_id"\s*:\s*"([^"]+)"', placeholder)
    aid = m.group(1) if m else "fixture-market-outlook-pos"
    rec_path = ROOT / "tmp" / "issue401_wrong_audit.json"
    rec_path.parent.mkdir(parents=True, exist_ok=True)
    rec_path.write_text(json.dumps({"records": [{"record_id": "r1", "recorded_at": "2026-08-18T10:00:00Z", "audit_id": "final-audit", "status": "passed", "artifact_sha256": sha, "artifact_id": aid, "executed_at": "2026-08-18T10:00:00Z"}]}), encoding="utf-8")
    proc = _run_report(report_tmp, "--strict", "--require-contract", "--json")
    try:
        rec_path.unlink(missing_ok=True)
        try:
            rec_path.parent.rmdir()
        except OSError:
            pass
    except Exception:
        pass
    assert proc.returncode == 2, proc.stdout
    blocking = json.loads(proc.stdout)["blocking"]
    assert any("audit" in b.lower() and ("mismatch" in b.lower() or "does not match" in b.lower()) for b in blocking)


def test_valid_audit_record_with_binding_passes(tmp_path: Path) -> None:
    content = POS.read_text(encoding="utf-8")
    report_tmp = tmp_path / "report.md"
    # Use a unique tmp record path under repo tmp so base_dir resolution works
    rec_rel = "tmp/issue401_valid.json"
    placeholder = content.replace("report-section:Monitoring signals", f"audit-record:{rec_rel}#r1@2026-08-18T10:00:00Z", 1)
    # also patch contract
    placeholder = placeholder.replace('"evidence": "report-section:Monitoring signals"', f'"evidence": "audit-record:{rec_rel}#r1@2026-08-18T10:00:00Z"', 1)
    report_tmp.write_text(placeholder, encoding="utf-8")
    sha = hashlib.sha256(report_tmp.read_bytes()).hexdigest()
    m = re.search(r'"artifact_id"\s*:\s*"([^"]+)"', placeholder)
    aid = m.group(1) if m else "fixture-market-outlook-pos"
    rec_path = ROOT / rec_rel
    rec_path.parent.mkdir(parents=True, exist_ok=True)
    rec_path.write_text(json.dumps({"records": [{"record_id": "r1", "recorded_at": "2026-08-18T10:00:00Z", "audit_id": "market-outlook-audit", "status": "passed", "artifact_sha256": sha, "artifact_id": aid, "executed_at": "2026-08-18T10:00:00Z", "execution_source": "manual_checklist_attestation"}]}), encoding="utf-8")
    # Recompute after ensuring report content final (sha already matches)
    proc = _run_report(report_tmp, "--strict", "--require-contract", "--json")
    try:
        rec_path.unlink(missing_ok=True)
        try:
            rec_path.parent.rmdir()
        except OSError:
            pass
    except Exception:
        pass
    assert proc.returncode == 0, proc.stdout
    data = json.loads(proc.stdout)
    assert data["overall"] == "pass"
    audit = next(a for a in data["audits"] if a["audit_id"] == "market-outlook-audit")
    assert audit["status"] == "pass"
    assert audit["execution_source"] == "manual_checklist_attestation"
    assert audit["evidence_provenance"][0]["verified"] is True
    assert audit["evidence_provenance"][0]["kind"] == "audit_record"


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
