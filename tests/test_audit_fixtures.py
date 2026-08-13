#!/usr/bin/env python3
"""
End-to-end fixture tests for issue #378.

Each fixture exercises the full audit_report.py command with
--strict --require-contract, proving that required audits actually
trigger (positive = exit 0, negative = exit 2 with the expected audit).
Covers: market-outlook, shared-workflow, a mixed route (primary +
secondary with independent hard-fail audit), and a research pack.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "audit"
SCRIPT = str(ROOT / "scripts" / "audit_report.py")


def _run(*fixture_names: str, extra: list[str] | None = None) -> subprocess.CompletedProcess:
    args = [sys.executable, SCRIPT, str(FIXTURES / fixture_names[0])]
    for f in fixture_names[1:]:
        args += ["--research-pack", str(FIXTURES / f)]
    args += extra or []
    return subprocess.run(args, capture_output=True, text=True)


class TestPositiveFixtures:
    def test_market_outlook_pos(self) -> None:
        result = _run("market-outlook-pos.md", extra=["--strict", "--require-contract"])
        assert result.returncode == 0, result.stdout

    def test_shared_workflow_pos(self) -> None:
        result = _run("shared-workflow-pos.md", extra=["--strict", "--require-contract"])
        assert result.returncode == 0, result.stdout

    def test_mixed_route_pos(self) -> None:
        """Secondary hard-fail has its own audit result and passes."""
        result = _run("market-outlook-mixed-pos.md", extra=["--strict", "--require-contract"])
        assert result.returncode == 0, result.stdout

    def test_mixed_route_pos_json_contains_secondary_audit(self) -> None:
        result = _run("market-outlook-mixed-pos.md", extra=["--strict", "--require-contract", "--json"])
        data = json.loads(result.stdout)
        ids = {a["audit_id"]: a for a in data["audits"]}
        assert ids["constrained-choice-secondary-hard-fail"]["status"] == "pass"

    def test_market_outlook_pos_with_pack(self) -> None:
        """Markdown delivery + Research Pack + contract in one command."""
        result = _run(
            "market-outlook-pos.md", "research-pack-pos.md",
            extra=["--strict", "--require-contract"],
        )
        assert result.returncode == 0, result.stdout


class TestNegativeFixtures:
    def test_market_outlook_neg_forward_looking(self) -> None:
        """Mislabeled forward-looking claim must block (automated audit)."""
        result = _run("market-outlook-neg.md", extra=["--strict", "--require-contract"])
        assert result.returncode == 2, result.stdout
        assert "forward-looking-claims" in result.stdout

    def test_shared_workflow_neg_not_run_manual_audit(self) -> None:
        """Undeclared manual audit must block as not_run in strict mode."""
        result = _run("shared-workflow-neg.md", extra=["--strict", "--require-contract"])
        assert result.returncode == 2, result.stdout
        assert "final-audit" in result.stdout
        assert "not_run" in result.stdout or "not run" in result.stdout

    def test_mixed_route_neg_missing_secondary_hard_fail(self) -> None:
        """Secondary declared without hard-fail audit must block."""
        result = _run("market-outlook-mixed-neg.md", extra=["--strict", "--require-contract"])
        assert result.returncode == 2, result.stdout
        assert "constrained-choice-secondary-hard-fail" in result.stdout


class TestJsonConsumability:
    def test_json_has_evidence_and_hash(self) -> None:
        result = _run("market-outlook-pos.md", extra=["--strict", "--require-contract", "--json"])
        data = json.loads(result.stdout)
        assert data["overall"] == "pass"
        assert data["exit_code"] == 0
        assert data["input_sha256"]
        assert data["validator_version"]
        # evidence locations present for executed audits
        forward = next(a for a in data["audits"] if a["audit_id"] == "forward-looking-claims")
        assert forward["validator_binding"] == "forward-looking-claims"
