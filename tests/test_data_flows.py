"""Contract tests for data-flow documentation and drift checks (issue #418)."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_data_flows.py"
REGISTRY_PATH = ROOT / "schemas" / "data-flow-registry.json"
DATA_FLOWS_PATH = ROOT / "docs" / "DATA_FLOWS.md"

sys.path.insert(0, str(ROOT / "scripts"))
import validate_data_flows as data_flows  # noqa: E402

_ORIGINAL_COLLECT = data_flows.collect_signal_files


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
    data_flows_text = DATA_FLOWS_PATH.read_text(encoding="utf-8")
    for item in registry["network_touchpoints"]:
        assert f"`{item['id']}`" in data_flows_text


def test_registry_risk_ids_documented_in_risk_register() -> None:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    risk_register = (ROOT / "docs" / "RISK_REGISTER.md").read_text(encoding="utf-8")
    for risk_id in registry["risk_ids"]:
        assert risk_id in risk_register


def test_undocumented_playwright_file_fails_drift_check(monkeypatch) -> None:
    """A new playwright script not listed in the registry should fail validation."""

    def fake_collect(signal: str, patterns, *, include_tests: bool, tests_only: bool = False) -> set[str]:
        if signal == "async_playwright":
            return {"scripts/rogue_new_playwright.py"}
        return _ORIGINAL_COLLECT(
            signal, patterns, include_tests=include_tests, tests_only=tests_only
        )

    monkeypatch.setattr(data_flows, "collect_signal_files", fake_collect)
    failures = data_flows.run_checks()
    assert any("Undocumented signal `async_playwright`" in msg for msg in failures)


def test_undocumented_gh_cli_file_fails_drift_check(monkeypatch) -> None:
    """A new gh CLI script not listed in the registry should fail validation."""

    def fake_collect(signal: str, patterns, *, include_tests: bool, tests_only: bool = False) -> set[str]:
        if signal == "gh_cli":
            return {"scripts/rogue_new_gh_tool.py"}
        return _ORIGINAL_COLLECT(
            signal, patterns, include_tests=include_tests, tests_only=tests_only
        )

    monkeypatch.setattr(data_flows, "collect_signal_files", fake_collect)
    failures = data_flows.run_checks()
    assert any("Undocumented signal `gh_cli`" in msg for msg in failures)


def test_verification_status_must_be_last_column() -> None:
    row = (
        "| `delivery-status-writeback` | explicit `--write-status PATH` on delivery CLI | "
        "delivery status markdown snippet | operator-specified file | none | until operator deletes | "
        "omit `--write-status` | `not_run` delivery fields in pack |"
    )
    failures = data_flows.check_verification_status_tokens(row)
    assert failures
    assert any(
        "expected 9" in msg or "invalid verification_status" in msg for msg in failures
    )


def test_verification_status_accepts_not_run_in_degraded_state_column() -> None:
    row = (
        "| `delivery-status-writeback` | explicit `--write-status PATH` on delivery CLI | "
        "delivery status markdown snippet | operator-specified file | none | until operator deletes | "
        "omit `--write-status` | `not_run` delivery fields in pack | asserted |"
    )
    failures = data_flows.check_verification_status_tokens(row)
    assert not failures


def test_undocumented_delivery_temp_dir_fails_drift_check(monkeypatch) -> None:
    """A new delivery temp-dir write path not listed in the registry should fail."""

    def fake_collect(signal: str, patterns, *, include_tests: bool, tests_only: bool = False) -> set[str]:
        if signal == "delivery_temp_dir":
            return {"scripts/rogue_delivery_cache.py"}
        return _ORIGINAL_COLLECT(
            signal, patterns, include_tests=include_tests, tests_only=tests_only
        )

    monkeypatch.setattr(data_flows, "collect_signal_files", fake_collect)
    failures = data_flows.run_checks()
    assert any("Undocumented signal `delivery_temp_dir`" in msg for msg in failures)


def test_removed_gh_cli_signal_fails_drift_check(monkeypatch) -> None:
    """Removing gh calls from a registered file should fail validation."""

    def fake_collect(signal: str, patterns, *, include_tests: bool, tests_only: bool = False) -> set[str]:
        if signal == "gh_cli":
            return set()
        return _ORIGINAL_COLLECT(
            signal, patterns, include_tests=include_tests, tests_only=tests_only
        )

    monkeypatch.setattr(data_flows, "collect_signal_files", fake_collect)
    failures = data_flows.run_checks()
    assert any(
        "Registered signal `gh_cli` no longer present in" in msg for msg in failures
    )


def test_removed_delivery_temp_dir_signal_fails_drift_check(monkeypatch) -> None:
    """Removing delivery temp-dir writes from a registered file should fail validation."""

    def fake_collect(signal: str, patterns, *, include_tests: bool, tests_only: bool = False) -> set[str]:
        if signal == "delivery_temp_dir":
            return set()
        return _ORIGINAL_COLLECT(
            signal, patterns, include_tests=include_tests, tests_only=tests_only
        )

    monkeypatch.setattr(data_flows, "collect_signal_files", fake_collect)
    failures = data_flows.run_checks()
    assert any(
        "Registered signal `delivery_temp_dir` no longer present in" in msg
        for msg in failures
    )
