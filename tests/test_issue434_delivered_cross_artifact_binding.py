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

import copy
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


def _write_real_pass_audit(
    tmp_path: Path, *, pack_extra: str = ""
) -> tuple[Path, Path, Path]:
    """Generate a real audit_report --json Pass bound to copied report/pack."""
    report = tmp_path / "report.md"
    report.write_text(
        (AUDIT_FIXTURES / "market-outlook-pos.md").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    pack = tmp_path / "pack.md"
    pack.write_text(
        (AUDIT_FIXTURES / "research-pack-pos.md").read_text(encoding="utf-8")
        + pack_extra,
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
    tmp_path: Path,
    report: Path,
    pack: Path,
    audit: Path,
    *,
    state_data: dict | None = None,
) -> subprocess.CompletedProcess:
    state = tmp_path / "delivered-state.json"
    payload = (
        state_data
        if state_data is not None
        else json.loads(DELIVERED_STATE.read_text(encoding="utf-8"))
    )
    state.write_text(json.dumps(payload), encoding="utf-8")
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


def _tamper_visible_route(report: Path, replacement: str) -> None:
    report.write_text(
        report.read_text(encoding="utf-8").replace(
            "**Primary route**: Market Outlook",
            f"**Primary route**: {replacement}",
        ),
        encoding="utf-8",
    )


def test_report_status_route_tamper_cannot_support_delivered(tmp_path: Path) -> None:
    report, pack, audit_path = _write_real_pass_audit(tmp_path)
    _tamper_visible_route(report, "Technical Deep Dive")

    proc = _run_delivered(tmp_path, report, pack, audit_path)
    assert proc.returncode == 2, proc.stdout + proc.stderr
    payload = _payload(proc)
    assert any(
        "technical-deep-dive" in error or "route mismatch" in error
        for error in payload["errors"]
    ), payload


def test_unknown_report_status_route_cannot_support_delivered(tmp_path: Path) -> None:
    report, pack, audit_path = _write_real_pass_audit(tmp_path)
    _tamper_visible_route(report, "Bogus Route")

    proc = _run_delivered(tmp_path, report, pack, audit_path)
    assert proc.returncode == 2, proc.stdout + proc.stderr
    payload = _payload(proc)
    assert any("Bogus Route" in error for error in payload["errors"]), payload


def test_duplicate_pack_primary_route_cannot_support_delivered(tmp_path: Path) -> None:
    report, pack, audit_path = _write_real_pass_audit(tmp_path)
    pack.write_text(
        pack.read_text(encoding="utf-8") + "\n## Primary route\n\nShared Workflow\n",
        encoding="utf-8",
    )

    proc = _run_delivered(tmp_path, report, pack, audit_path)
    assert proc.returncode == 2, proc.stdout + proc.stderr
    payload = _payload(proc)
    assert any("Primary route" in error for error in payload["errors"]), payload


def test_duplicate_pack_artifact_id_cannot_support_delivered(tmp_path: Path) -> None:
    report, pack, audit_path = _write_real_pass_audit(tmp_path)
    pack.write_text(
        pack.read_text(encoding="utf-8") + "\n## Artifact id\n\nother-artifact\n",
        encoding="utf-8",
    )

    proc = _run_delivered(tmp_path, report, pack, audit_path)
    assert proc.returncode == 2, proc.stdout + proc.stderr
    payload = _payload(proc)
    assert any("Artifact id" in error for error in payload["errors"]), payload


def test_removed_contract_artifact_id_cannot_support_delivered(tmp_path: Path) -> None:
    report, pack, audit_path = _write_real_pass_audit(tmp_path)
    _edit_contract(report, lambda contract: contract.pop("artifact_id"))

    proc = _run_delivered(tmp_path, report, pack, audit_path)
    assert proc.returncode == 2, proc.stdout + proc.stderr
    payload = _payload(proc)
    assert any("artifact_id" in error for error in payload["errors"]), payload


def test_duplicate_secondary_route_in_contract_cannot_support_delivered(tmp_path: Path) -> None:
    report, pack, audit_path = _write_real_pass_audit(tmp_path)

    def duplicate_secondary(contract: dict) -> None:
        contract["secondary_routes"] = ["regulatory-analysis", "regulatory-analysis"]
        contract["audits"].append(
            {
                "id": "regulatory-analysis-secondary-hard-fail",
                "status": "passed",
                "evidence": "report-section:Findings",
            }
        )

    _edit_contract(report, duplicate_secondary)

    proc = _run_delivered(tmp_path, report, pack, audit_path)
    assert proc.returncode == 2, proc.stdout + proc.stderr
    payload = _payload(proc)
    assert any(
        "Duplicate secondary route" in error or "duplicate secondary" in error
        for error in payload["errors"]
    ), payload


ACTIVATION_SNAPSHOT_SECTION = (
    "\n## Activation snapshot\n"
    "\n"
    "- activation_id: forward-market-outlook-baseline\n"
    "- snapshot_version: 2\n"
    "- decision_tree_version: 1\n"
)


def _state_with_activation_reference(activation_id: str) -> dict:
    state = json.loads(DELIVERED_STATE.read_text(encoding="utf-8"))
    state["activation_reference"] = {
        "activation_id": activation_id,
        "snapshot_version": 2,
        "decision_tree_version": 1,
    }
    return state


def test_matching_pack_activation_snapshot_still_passes(tmp_path: Path) -> None:
    report, pack, audit_path = _write_real_pass_audit(
        tmp_path, pack_extra=ACTIVATION_SNAPSHOT_SECTION
    )
    state = _state_with_activation_reference("forward-market-outlook-baseline")

    proc = _run_delivered(
        tmp_path, report, pack, audit_path, state_data=state
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert _payload(proc)["ok"] is True


def test_tampered_pack_activation_snapshot_cannot_support_delivered(
    tmp_path: Path,
) -> None:
    report, pack, audit_path = _write_real_pass_audit(
        tmp_path, pack_extra=ACTIVATION_SNAPSHOT_SECTION
    )
    state = _state_with_activation_reference("forward-market-outlook-baseline")
    pack.write_text(
        pack.read_text(encoding="utf-8").replace(
            "activation_id: forward-market-outlook-baseline",
            "activation_id: tampered-activation",
        ),
        encoding="utf-8",
    )

    proc = _run_delivered(
        tmp_path, report, pack, audit_path, state_data=state
    )
    assert proc.returncode == 2, proc.stdout + proc.stderr
    payload = _payload(proc)
    assert any("activation" in error.lower() for error in payload["errors"]), payload


def test_run_state_activation_reference_mismatch_cannot_support_delivered(
    tmp_path: Path,
) -> None:
    report, pack, audit_path = _write_real_pass_audit(
        tmp_path, pack_extra=ACTIVATION_SNAPSHOT_SECTION
    )
    state = _state_with_activation_reference("different-activation")

    proc = _run_delivered(
        tmp_path, report, pack, audit_path, state_data=state
    )
    assert proc.returncode == 2, proc.stdout + proc.stderr
    payload = _payload(proc)
    assert any(
        "Run State activation_reference" in error for error in payload["errors"]
    ), payload


def test_removed_report_route_status_section_cannot_support_delivered(
    tmp_path: Path,
) -> None:
    report, pack, audit_path = _write_real_pass_audit(tmp_path)
    text = report.read_text(encoding="utf-8")
    text = re.sub(
        r"## Route and audit status\n.*?(?=\n## )", "", text, flags=re.DOTALL
    )
    report.write_text(text, encoding="utf-8")

    proc = _run_delivered(tmp_path, report, pack, audit_path)
    assert proc.returncode == 2, proc.stdout + proc.stderr
    payload = _payload(proc)
    assert any(
        "Route and audit status" in error for error in payload["errors"]
    ), payload


def test_removed_report_route_declaration_cannot_support_delivered(
    tmp_path: Path,
) -> None:
    report, pack, audit_path = _write_real_pass_audit(tmp_path)
    report.write_text(
        report.read_text(encoding="utf-8").replace(
            "**Primary route**: Market Outlook\n", ""
        ),
        encoding="utf-8",
    )

    proc = _run_delivered(tmp_path, report, pack, audit_path)
    assert proc.returncode == 2, proc.stdout + proc.stderr
    payload = _payload(proc)
    assert any(
        "route declaration" in error.lower() for error in payload["errors"]
    ), payload


def test_duplicate_report_route_status_blocks_cannot_support_delivered(
    tmp_path: Path,
) -> None:
    report, pack, audit_path = _write_real_pass_audit(tmp_path)
    report.write_text(
        report.read_text(encoding="utf-8")
        + "\n## Route and audit status\n\n**Primary route**: Shared Workflow\n",
        encoding="utf-8",
    )

    proc = _run_delivered(tmp_path, report, pack, audit_path)
    assert proc.returncode == 2, proc.stdout + proc.stderr
    payload = _payload(proc)
    assert any(
        "Route and audit status" in error for error in payload["errors"]
    ), payload


def test_removed_pack_artifact_id_section_cannot_support_delivered(
    tmp_path: Path,
) -> None:
    report, pack, audit_path = _write_real_pass_audit(tmp_path)
    text = pack.read_text(encoding="utf-8")
    text = re.sub(r"## Artifact id\n.*?(?=\n## )", "", text, flags=re.DOTALL)
    pack.write_text(text, encoding="utf-8")

    proc = _run_delivered(tmp_path, report, pack, audit_path)
    assert proc.returncode == 2, proc.stdout + proc.stderr
    payload = _payload(proc)
    assert any("Artifact id" in error for error in payload["errors"]), payload


def test_advisory_contract_warnings_do_not_block_delivered(tmp_path: Path) -> None:
    report, pack, audit_path = _write_real_pass_audit(tmp_path)
    secondaries = ["regulatory-analysis", "technical-deep-dive", "startup-evaluation"]

    def add_secondaries(contract: dict) -> None:
        contract["secondary_routes"] = list(secondaries)
        for route in secondaries:
            contract["audits"].append(
                {
                    "id": f"{route}-secondary-hard-fail",
                    "status": "passed",
                    "evidence": "report-section:Monitoring signals",
                }
            )

    _edit_contract(report, add_secondaries)

    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    template = _manual_entry(audit)
    for route in secondaries:
        entry = copy.deepcopy(template)
        entry["audit_id"] = f"{route}-secondary-hard-fail"
        entry["evidence"] = ["report-section:Monitoring signals"]
        entry["evidence_provenance"] = [
            {
                "verified": True,
                "kind": "report_section",
                "locator": "Monitoring signals",
                "execution_source": "manual_checklist_attestation",
            }
        ]
        audit["audits"].append(entry)
    audit_path.write_text(json.dumps(audit, ensure_ascii=False), encoding="utf-8")

    proc = _run_delivered(tmp_path, report, pack, audit_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert _payload(proc)["ok"] is True


def _rerun_producer(report: Path, pack: Path) -> dict:
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
    return json.loads(proc.stdout)


def test_producer_accepted_chinese_route_heading_still_passes_delivered(
    tmp_path: Path,
) -> None:
    """Issue #434 review round 3: producer and delivered must accept the same
    route-status heading forms (H2/H3, English or 附录：路由与审计状态)."""
    report, pack, audit_path = _write_real_pass_audit(tmp_path)
    report.write_text(
        report.read_text(encoding="utf-8").replace(
            "## Route and audit status", "## 附录：路由与审计状态"
        ),
        encoding="utf-8",
    )
    audit = _rerun_producer(report, pack)
    audit_path.write_text(json.dumps(audit, ensure_ascii=False), encoding="utf-8")

    proc = _run_delivered(tmp_path, report, pack, audit_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert _payload(proc)["ok"] is True


def test_producer_accepted_nested_h3_route_heading_still_passes_delivered(
    tmp_path: Path,
) -> None:
    report, pack, audit_path = _write_real_pass_audit(tmp_path)
    report.write_text(
        report.read_text(encoding="utf-8").replace(
            "## Route and audit status",
            "## Appendix\n\n### Route and audit status",
        ),
        encoding="utf-8",
    )
    audit = _rerun_producer(report, pack)
    audit_path.write_text(json.dumps(audit, ensure_ascii=False), encoding="utf-8")

    proc = _run_delivered(tmp_path, report, pack, audit_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert _payload(proc)["ok"] is True


def test_run_state_artifact_id_mismatch_cannot_support_delivered(
    tmp_path: Path,
) -> None:
    report, pack, audit_path = _write_real_pass_audit(tmp_path)
    state = json.loads(DELIVERED_STATE.read_text(encoding="utf-8"))
    state["artifact_id"] = "other-artifact"

    proc = _run_delivered(
        tmp_path, report, pack, audit_path, state_data=state
    )
    assert proc.returncode == 2, proc.stdout + proc.stderr
    payload = _payload(proc)
    assert any("artifact_id" in error for error in payload["errors"]), payload


def test_from_to_delivered_artifact_id_mismatch_cannot_support_delivered(
    tmp_path: Path,
) -> None:
    report, pack, audit_path = _write_real_pass_audit(tmp_path)
    before = json.loads(DELIVERED_STATE.read_text(encoding="utf-8"))
    before.update(
        {
            "phase": "auditing",
            "status": "in_progress",
            "artifact_id": "other-artifact",
        }
    )
    after = json.loads(DELIVERED_STATE.read_text(encoding="utf-8"))
    after["artifact_id"] = "other-artifact"
    before_path = tmp_path / "before.json"
    after_path = tmp_path / "after.json"
    before_path.write_text(json.dumps(before), encoding="utf-8")
    after_path.write_text(json.dumps(after), encoding="utf-8")

    proc = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "validate_research_run_state.py"),
            "--from",
            str(before_path),
            "--to",
            str(after_path),
            "--audit-result",
            str(audit_path),
            "--artifact",
            str(pack),
            "--report",
            str(report),
            "--json",
        ],
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 2, proc.stdout + proc.stderr
    payload = _payload(proc)
    assert any("artifact_id" in error for error in payload["errors"]), payload


def test_activation_reference_mismatch_without_pack_snapshot_cannot_support_delivered(
    tmp_path: Path,
) -> None:
    report, pack, audit_path = _write_real_pass_audit(tmp_path)
    state = json.loads(DELIVERED_STATE.read_text(encoding="utf-8"))
    state["activation_reference"] = {
        "activation_id": "different-activation",
        "snapshot_version": 2,
        "decision_tree_version": 1,
    }

    proc = _run_delivered(
        tmp_path, report, pack, audit_path, state_data=state
    )
    assert proc.returncode == 2, proc.stdout + proc.stderr
    payload = _payload(proc)
    assert any(
        "Run State activation_reference" in error for error in payload["errors"]
    ), payload


def test_matching_contract_activation_reference_without_pack_snapshot_passes(
    tmp_path: Path,
) -> None:
    report, pack, audit_path = _write_real_pass_audit(tmp_path)
    proc = _run_delivered(tmp_path, report, pack, audit_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert _payload(proc)["ok"] is True


def test_malformed_typed_contract_cannot_support_delivered(tmp_path: Path) -> None:
    report, pack, audit_path = _write_real_pass_audit(tmp_path)

    def unhashable_secondary(contract: dict) -> None:
        contract["secondary_routes"] = [{}]
        contract["secondary_route_contracts"] = {}

    _edit_contract(report, unhashable_secondary)

    proc = _run_delivered(tmp_path, report, pack, audit_path)
    assert proc.returncode == 2, proc.stdout + proc.stderr
    payload = _payload(proc)
    assert any(
        "Secondary route" in error or "secondary" in error
        for error in payload["errors"]
    ), payload
    assert "Traceback" not in proc.stderr


def test_invalid_utf8_audit_json_returns_structured_error(tmp_path: Path) -> None:
    report, pack, audit_path = _write_real_pass_audit(tmp_path)
    audit_path.write_bytes(b'{"schema_version": "2", "x": "\xff\xfe"}')

    proc = _run_delivered(tmp_path, report, pack, audit_path)
    assert proc.returncode == 2, proc.stdout + proc.stderr
    payload = _payload(proc)
    assert any("audit result" in error for error in payload["errors"]), payload
    assert "Traceback" not in proc.stderr


def test_invalid_utf8_run_state_returns_structured_error(tmp_path: Path) -> None:
    report, pack, audit_path = _write_real_pass_audit(tmp_path)
    state_path = tmp_path / "bad-state.json"
    state_path.write_bytes(b'{"schema_version": "2", "run_id": "\xff\xfe"}')

    proc = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "validate_research_run_state.py"),
            str(state_path),
            "--audit-result",
            str(audit_path),
            "--artifact",
            str(pack),
            "--report",
            str(report),
            "--json",
        ],
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 2, proc.stdout + proc.stderr
    payload = _payload(proc)
    assert any("run state" in error for error in payload["errors"]), payload
    assert "Traceback" not in proc.stderr


def test_registry_failure_is_structured(monkeypatch) -> None:
    import types

    import registry_loader

    import validate_research_run_state as vrs  # noqa: PLC0415

    class Boom(types.ModuleType):
        def __getattr__(self, name):  # noqa: ANN001
            raise registry_loader.RegistryError("corrupt registry")

    monkeypatch.setitem(sys.modules, "run_forward_evals", Boom("run_forward_evals"))

    errors = vrs.check_audit_result_for_delivered(
        {"schema_version": "2", "overall": "pass", "exit_code": 0, "audits": []},
        {"artifact_id": "x"},
    )
    assert errors
    assert any(
        "registry" in error.lower() or "canonical" in error.lower()
        for error in errors
    ), errors


def test_pack_locator_removed_cannot_support_delivered(tmp_path: Path) -> None:
    report, pack, audit_path = _write_real_pass_audit(tmp_path)
    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    entry = _manual_entry(audit)
    entry["evidence"] = ["pack-section:Artifact contract"]
    entry["evidence_provenance"] = [
        {
            "verified": True,
            "kind": "pack_section",
            "locator": "Artifact contract",
            "execution_source": "manual_checklist_attestation",
        }
    ]
    audit_path.write_text(json.dumps(audit, ensure_ascii=False), encoding="utf-8")

    text = pack.read_text(encoding="utf-8")
    text = re.sub(
        r"## Artifact contract\n.*?(?=\n## )", "", text, flags=re.DOTALL
    )
    pack.write_text(text, encoding="utf-8")

    proc = _run_delivered(tmp_path, report, pack, audit_path)
    assert proc.returncode == 2, proc.stdout + proc.stderr
    payload = _payload(proc)
    assert any(
        "Artifact contract" in error or "visible pack" in error
        for error in payload["errors"]
    ), payload
