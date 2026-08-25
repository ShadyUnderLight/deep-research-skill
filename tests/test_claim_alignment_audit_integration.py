#!/usr/bin/env python3
"""Opt-in claim-source-alignment audit integration (issue #419)."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
FIXTURES = ROOT / "tests" / "fixtures"
AUDIT_SCRIPT = ROOT / "scripts" / "audit_report.py"


def _run_audit(*extra: str) -> subprocess.CompletedProcess:
    cmd = [
        sys.executable,
        str(AUDIT_SCRIPT),
        str(FIXTURES / "audit" / "market-outlook-pos.md"),
        "--research-pack",
        str(FIXTURES / "audit" / "research-pack-pos.md"),
        "--strict",
        "--require-contract",
        "--json",
        *extra,
    ]
    return subprocess.run(cmd, capture_output=True, text=True)


def test_default_audit_report_records_claim_alignment_not_run() -> None:
    result = _run_audit()
    assert result.returncode == 0, result.stdout + result.stderr
    data = json.loads(result.stdout)
    by_id = {a["audit_id"]: a for a in data["audits"]}
    assert by_id["claim-source-alignment"]["status"] == "not_run"
    assert by_id["claim-source-alignment"]["reason"]


def test_enable_claim_alignment_with_bound_valid_bundle() -> None:
    result = _run_audit(
        "--enable-claim-alignment",
        "--claim-alignment-bundle",
        str(FIXTURES / "claim-alignment" / "valid.json"),
    )
    assert result.returncode == 0, result.stdout + result.stderr
    data = json.loads(result.stdout)
    by_id = {a["audit_id"]: a for a in data["audits"]}
    assert by_id["claim-source-alignment"]["status"] == "pass"


def test_enable_without_bundle_blocks() -> None:
    result = _run_audit("--enable-claim-alignment")
    assert result.returncode == 2, result.stdout + result.stderr
    data = json.loads(result.stdout)
    by_id = {a["audit_id"]: a for a in data["audits"]}
    assert by_id["claim-source-alignment"]["status"] == "not_run"


def test_enabled_claim_alignment_passes_consumer_provenance() -> None:
    result = _run_audit(
        "--enable-claim-alignment",
        "--claim-alignment-bundle",
        str(FIXTURES / "claim-alignment" / "valid.json"),
    )
    assert result.returncode == 0, result.stdout + result.stderr
    data = json.loads(result.stdout)
    report_path = FIXTURES / "audit" / "market-outlook-pos.md"
    if str(SCRIPTS) not in sys.path:
        sys.path.insert(0, str(SCRIPTS))
    from run_forward_evals import _audit_consistency_details, _expected_audit_set  # noqa: E402

    report_sha = __import__("hashlib").sha256(report_path.read_bytes()).hexdigest()
    expected_ids = _expected_audit_set("market-outlook", [])
    ok, errors = _audit_consistency_details(
        data,
        expected_ids,
        audited_path=str(report_path),
        expected_report_sha256=report_sha,
        research_pack_path=str(FIXTURES / "audit" / "research-pack-pos.md"),
        expected_pack_sha256=__import__("hashlib").sha256(
            (FIXTURES / "audit" / "research-pack-pos.md").read_bytes()
        ).hexdigest(),
        expected_route="market-outlook",
    )
    assert ok, errors


def test_tampered_opt_in_reason_not_exempt_from_consumer_checks() -> None:
    if str(SCRIPTS) not in sys.path:
        sys.path.insert(0, str(SCRIPTS))
    from opt_in_audit_contract import OPT_IN_DEFAULT_OFF_REASON  # noqa: E402
    from run_forward_evals import _audit_status_is_fail_like  # noqa: E402

    assert not _audit_status_is_fail_like(
        "claim-source-alignment",
        "not_run",
        OPT_IN_DEFAULT_OFF_REASON,
    )
    assert _audit_status_is_fail_like(
        "claim-source-alignment",
        "not_run",
        "opt-in audit enabled but no --claim-alignment-bundle provided",
    )


def test_route_mismatch_bundle_blocks_alignment_pass() -> None:
    result = _run_audit(
        "--enable-claim-alignment",
        "--claim-alignment-bundle",
        str(FIXTURES / "claim-alignment" / "route-mismatch.json"),
    )
    assert result.returncode == 2, result.stdout + result.stderr
    data = json.loads(result.stdout)
    by_id = {a["audit_id"]: a for a in data["audits"]}
    assert by_id["claim-source-alignment"]["status"] == "fail"
