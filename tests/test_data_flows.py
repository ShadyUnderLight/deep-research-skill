"""Contract tests for data-flow documentation and drift checks (issue #418)."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_data_flows.py"
REGISTRY_PATH = ROOT / "schemas" / "data-flow-registry.json"

sys.path.insert(0, str(ROOT / "scripts"))
import validate_data_flows as data_flows  # noqa: E402


def test_validate_data_flows_passes_on_repo() -> None:
    result = subprocess.run(
        [sys.executable, str(VALIDATOR)],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_registry_network_touchpoints_documented_in_data_flows() -> None:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    data_flows_text = (ROOT / "docs" / "DATA_FLOWS.md").read_text(encoding="utf-8")
    for item in registry["network_touchpoints"]:
        assert f"`{item['id']}`" in data_flows_text


def test_registry_risk_ids_documented_in_risk_register() -> None:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    risk_register = (ROOT / "docs" / "RISK_REGISTER.md").read_text(encoding="utf-8")
    for risk_id in registry["risk_ids"]:
        assert risk_id in risk_register


def test_undocumented_playwright_file_fails_drift_check(monkeypatch) -> None:
    """A new playwright script not listed in the registry should fail validation."""

    def fake_collect(signal: str) -> set[str]:
        if signal == "async_playwright":
            return {"scripts/rogue_new_playwright.py"}
        return data_flows.collect_signal_files(signal)

    monkeypatch.setattr(data_flows, "collect_signal_files", fake_collect)
    failures = data_flows.run_checks()
    assert any("Undocumented network signal `async_playwright`" in msg for msg in failures)
