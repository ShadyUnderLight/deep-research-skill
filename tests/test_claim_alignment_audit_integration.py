#!/usr/bin/env python3
"""Opt-in claim-source-alignment audit integration (issue #419)."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
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
