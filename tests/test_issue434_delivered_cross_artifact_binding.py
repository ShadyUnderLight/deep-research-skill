"""Issue #434: delivered Run State must not trust a self-consistent audit JSON.

The delivered consumer cross-checks the report contract, the Research Pack and
the audit result.  These tests pin the fail-closed boundary:

- the report contract must be a single, parseable, canonically valid contract;
- contract primary/secondary routes and the Pack primary route must be
  canonical and agree with the audit result route;
- report/Pack evidence locators must resolve against the visible artifact
  body, not just be internally consistent inside the JSON;
- registry/contract failures must surface as structured delivered errors
  (exit code 2 with a JSON payload), never as an unhandled traceback.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
FIXTURES = ROOT / "tests" / "fixtures"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

AUDIT_FIXTURES = FIXTURES / "audit"
DELIVERED_STATE = FIXTURES / "research-run-state" / "valid-delivered.json"


def _write_real_pass_audit(tmp_path: Path) -> tuple[Path, Path, Path]:
    """Generate a real audit_report --json Pass bound to copied report/pack."""
    report = tmp_path / "report.md"
    report.write_text(
        (AUDIT_FIXTURES / "market-outlook-pos.md").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    pack = tmp_path / "pack.md"
    pack.write_text(
        (AUDIT_FIXTURES / "research-pack-pos.md").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    proc = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "audit_report.py"),
            str(report),
            "--research-pack",
            str(pack),
            "--strict",
            "--require-contract",
            "--json",
        ],
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    audit_path = tmp_path / "audit.json"
    audit_path.write_text(proc.stdout, encoding="utf-8")
    return report, pack, audit_path


def _edit_contract(path: Path, mutate) -> None:
    text = path.read_text(encoding="utf-8")
    match = re.search(r"```contract\n(.*?)\n```", text, re.DOTALL)
    assert match is not None, "contract block missing"
    contract = json.loads(match.group(1))
    mutate(contract)
    replacement = "```contract\n" + json.dumps(contract, ensure_ascii=False) + "\n```"
    path.write_text(text.replace(match.group(0), replacement), encoding="utf-8")


def _manual_entry(audit: dict) -> dict:
    return next(
        entry
        for entry in audit["audits"]
        if entry.get("execution_type") == "manual"
        and entry.get("evidence_provenance")
    )


def _run_delivered(
    tmp_path: Path, report: Path, pack: Path, audit: Path
) -> subprocess.CompletedProcess:
    state = tmp_path / "delivered-state.json"
    state.write_text(DELIVERED_STATE.read_text(encoding="utf-8"), encoding="utf-8")
    return subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "validate_research_run_state.py"),
            str(state),
            "--audit-result",
            str(audit),
            "--artifact",
            str(pack),
            "--report",
            str(report),
            "--json",
        ],
        capture_output=True,
        text=True,
    )


def _payload(proc: subprocess.CompletedProcess) -> dict:
    assert proc.stdout.strip().startswith("{"), proc.stdout + proc.stderr
    return json.loads(proc.stdout)


def test_valid_delivered_fixture_still_passes(tmp_path: Path) -> None:
    report, pack, audit = _write_real_pass_audit(tmp_path)
    proc = _run_delivered(tmp_path, report, pack, audit)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    payload = _payload(proc)
    assert payload["ok"] is True
    assert payload["errors"] == []


def test_forged_secondary_route_cannot_support_delivered(tmp_path: Path) -> None:
    report, pack, audit_path = _write_real_pass_audit(tmp_path)
    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    forged = dict(_manual_entry(audit))
    forged["audit_id"] = "bogus-route-secondary-hard-fail"
    forged["evidence"] = ["report-section:Monitoring signals"]
    forged["evidence_provenance"] = [
        {
            "verified": True,
            "kind": "report_section",
            "locator": "Monitoring signals",
            "execution_source": "manual_checklist_attestation",
        }
    ]
    audit["audits"].append(forged)
    audit_path.write_text(json.dumps(audit, ensure_ascii=False), encoding="utf-8")

    _edit_contract(report, lambda contract: contract["secondary_routes"].append("bogus-route"))

    proc = _run_delivered(tmp_path, report, pack, audit_path)
    assert proc.returncode == 2, proc.stdout + proc.stderr
    payload = _payload(proc)
    assert any("bogus-route" in error for error in payload["errors"]), payload
    assert "Traceback" not in proc.stderr


def test_unknown_primary_route_returns_structured_error(tmp_path: Path) -> None:
    report, pack, audit_path = _write_real_pass_audit(tmp_path)
    _edit_contract(report, lambda contract: contract.__setitem__("primary_route", "bogus-route"))

    proc = _run_delivered(tmp_path, report, pack, audit_path)
    assert proc.returncode == 2, proc.stdout + proc.stderr
    payload = _payload(proc)
    assert any("bogus-route" in error for error in payload["errors"]), payload
    assert "Traceback" not in proc.stderr

    import validate_research_run_state as vrs  # noqa: PLC0415

    state = json.loads(DELIVERED_STATE.read_text(encoding="utf-8"))
    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    errors = vrs.check_audit_result_for_delivered(
        audit, state, report_path=report, pack_path=pack
    )
    assert errors
    assert any("bogus-route" in error for error in errors), errors


def test_phantom_report_locator_cannot_support_delivered(tmp_path: Path) -> None:
    report, pack, audit_path = _write_real_pass_audit(tmp_path)
    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    entry = _manual_entry(audit)
    entry["evidence"] = ["report-section:No such visible section"]
    for record in entry["evidence_provenance"]:
        if record.get("kind") == "report_section":
            record["locator"] = "No such visible section"
    audit_path.write_text(json.dumps(audit, ensure_ascii=False), encoding="utf-8")

    proc = _run_delivered(tmp_path, report, pack, audit_path)
    assert proc.returncode == 2, proc.stdout + proc.stderr
    payload = _payload(proc)
    assert any("No such visible section" in error for error in payload["errors"]), payload


def test_fenced_heading_locator_cannot_support_delivered(tmp_path: Path) -> None:
    report, pack, audit_path = _write_real_pass_audit(tmp_path)
    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    entry = _manual_entry(audit)
    entry["evidence"] = ["report-section:Ghost section"]
    for record in entry["evidence_provenance"]:
        if record.get("kind") == "report_section":
            record["locator"] = "Ghost section"
    audit_path.write_text(json.dumps(audit, ensure_ascii=False), encoding="utf-8")

    report.write_text(
        report.read_text(encoding="utf-8") + "\n```\n## Ghost section\n\nhidden\n```\n",
        encoding="utf-8",
    )

    proc = _run_delivered(tmp_path, report, pack, audit_path)
    assert proc.returncode == 2, proc.stdout + proc.stderr
    payload = _payload(proc)
    assert any("Ghost section" in error for error in payload["errors"]), payload


def test_unresolvable_pack_primary_route_cannot_support_delivered(tmp_path: Path) -> None:
    report, pack, audit_path = _write_real_pass_audit(tmp_path)
    pack.write_text(
        pack.read_text(encoding="utf-8").replace(
            "## Primary route\n\nMarket Outlook",
            "## Primary route\n\nBogus Route",
        ),
        encoding="utf-8",
    )

    proc = _run_delivered(tmp_path, report, pack, audit_path)
    assert proc.returncode == 2, proc.stdout + proc.stderr
    payload = _payload(proc)
    assert any(
        "Bogus Route" in error or "Primary route" in error
        for error in payload["errors"]
    ), payload


def test_missing_pack_primary_route_section_cannot_support_delivered(tmp_path: Path) -> None:
    report, pack, audit_path = _write_real_pass_audit(tmp_path)
    text = pack.read_text(encoding="utf-8")
    text = re.sub(r"## Primary route\n.*?(?=\n## )", "", text, flags=re.DOTALL)
    pack.write_text(text, encoding="utf-8")

    proc = _run_delivered(tmp_path, report, pack, audit_path)
    assert proc.returncode == 2, proc.stdout + proc.stderr
    payload = _payload(proc)
    assert any("Primary route" in error for error in payload["errors"]), payload


def test_duplicate_contract_blocks_cannot_support_delivered(tmp_path: Path) -> None:
    report, pack, audit_path = _write_real_pass_audit(tmp_path)
    text = report.read_text(encoding="utf-8")
    match = re.search(r"```contract\n.*?\n```", text, re.DOTALL)
    assert match is not None, "contract block missing"
    report.write_text(text + "\n" + match.group(0) + "\n", encoding="utf-8")

    proc = _run_delivered(tmp_path, report, pack, audit_path)
    assert proc.returncode == 2, proc.stdout + proc.stderr
    payload = _payload(proc)
    assert any("contract" in error.lower() for error in payload["errors"]), payload


def test_malformed_contract_json_cannot_support_delivered(tmp_path: Path) -> None:
    report, pack, audit_path = _write_real_pass_audit(tmp_path)
    text = report.read_text(encoding="utf-8")
    report.write_text(
        text.replace('"primary_route": "market-outlook"', '"primary_route": '),
        encoding="utf-8",
    )

    proc = _run_delivered(tmp_path, report, pack, audit_path)
    assert proc.returncode == 2, proc.stdout + proc.stderr
    payload = _payload(proc)
    assert any("contract" in error.lower() for error in payload["errors"]), payload


def test_forged_derived_audit_without_contract_declaration_is_rejected(tmp_path: Path) -> None:
    report, pack, audit_path = _write_real_pass_audit(tmp_path)
    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    forged = dict(_manual_entry(audit))
    forged["audit_id"] = "bogus-route-secondary-hard-fail"
    forged["evidence"] = ["report-section:Monitoring signals"]
    forged["evidence_provenance"] = [
        {
            "verified": True,
            "kind": "report_section",
            "locator": "Monitoring signals",
            "execution_source": "manual_checklist_attestation",
        }
    ]
    audit["audits"].append(forged)
    audit_path.write_text(json.dumps(audit, ensure_ascii=False), encoding="utf-8")

    proc = _run_delivered(tmp_path, report, pack, audit_path)
    assert proc.returncode == 2, proc.stdout + proc.stderr
    payload = _payload(proc)
    assert any(
        "forged" in error or "bogus-route-secondary-hard-fail" in error
        for error in payload["errors"]
    ), payload


def test_audit_route_mismatch_cannot_support_delivered(tmp_path: Path) -> None:
    report, pack, audit_path = _write_real_pass_audit(tmp_path)
    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    audit["route"] = "technical-deep-dive"
    audit_path.write_text(json.dumps(audit, ensure_ascii=False), encoding="utf-8")

    proc = _run_delivered(tmp_path, report, pack, audit_path)
    assert proc.returncode == 2, proc.stdout + proc.stderr
    payload = _payload(proc)
    assert any("route mismatch" in error for error in payload["errors"]), payload
