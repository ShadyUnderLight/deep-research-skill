"""End-to-end coverage for Issue 391 contract fields."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "scripts" / "audit_report.py"
REPORT = ROOT / "tests" / "fixtures" / "forward" / "company-technical-mixed-report.md"
PACK = ROOT / "tests" / "fixtures" / "forward" / "company-technical-mixed-pack.md"


def _run(report: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(AUDIT),
            str(report),
            "--research-pack",
            str(PACK),
            "--strict",
            "--require-contract",
            "--json",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def test_audit_report_accepts_issue391_contract_fields() -> None:
    result = _run(REPORT)
    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert payload["overall"] == "pass"


def test_audit_report_rejects_stale_decision_tree_version(tmp_path: Path) -> None:
    mutated = tmp_path / "stale-version.md"
    text = REPORT.read_text(encoding="utf-8")
    mutated.write_text(text.replace('"decision_tree_version": 1', '"decision_tree_version": 999', 1), encoding="utf-8")
    result = _run(mutated)
    assert result.returncode == 2, result.stdout + result.stderr
    assert "decision_tree_version" in result.stdout
