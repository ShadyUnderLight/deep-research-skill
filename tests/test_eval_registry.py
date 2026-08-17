"""Contract tests for the executable Issue 379 forward-eval registry."""

from __future__ import annotations

import copy
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from eval_registry import (  # noqa: E402
    EvalRegistryError,
    gap_class_for_failure_family,
    load_registry,
    validate_registry,
)
from run_forward_evals import run  # noqa: E402


def test_registry_has_eight_active_forward_cases() -> None:
    registry = load_registry()
    active = [case for case in registry["cases"] if case["status"] == "active"]
    assert len(active) >= 8
    assert sum(case["type"] == "negative" for case in active) >= 2


def test_registry_covers_required_failure_families() -> None:
    registry = load_registry()
    families = {case["failure_family"] for case in registry["cases"]}
    assert "secondary-route-not-verified" in families
    assert "route-misclassification" in families
    assert "declared-not-executed" in families


@pytest.mark.parametrize(
    ("failure_family", "gap_class"),
    [
        ("missing-rule", "missing-rule"),
        ("missing-trigger", "missing-trigger"),
        ("route-misclassification", "missing-trigger"),
        ("execution-drift", "execution-drift"),
        ("declared-not-executed", "execution-drift"),
        ("fixture-reference-drift", "fixture-reference-drift"),
    ],
)
def test_failure_families_map_to_diagnostic_gap_classes(
    failure_family: str, gap_class: str
) -> None:
    assert gap_class_for_failure_family(failure_family) == gap_class


def test_registry_rejects_duplicate_case_ids() -> None:
    registry = load_registry()
    tampered = copy.deepcopy(registry)
    tampered["cases"][1]["id"] = tampered["cases"][0]["id"]
    errors = validate_registry(tampered)
    assert any("duplicated" in error for error in errors)


def test_registry_rejects_unknown_route() -> None:
    registry = load_registry()
    tampered = copy.deepcopy(registry)
    tampered["cases"][0]["expected"]["primary_route"] = "not-a-route"
    errors = validate_registry(tampered)
    assert any("unknown" in error and "primary_route" in error for error in errors)


def test_registry_rejects_missing_fixture() -> None:
    registry = load_registry()
    tampered = copy.deepcopy(registry)
    tampered["cases"][0]["fixtures"]["report"] = "tests/fixtures/forward/missing.md"
    errors = validate_registry(tampered)
    assert any("does not exist" in error for error in errors)


def test_offline_forward_runner_passes_and_reports_metrics() -> None:
    report = run(check_baseline=True)
    assert report["passed"] is True
    assert report["failed_cases"] == []
    assert report["offline"] is True
    metrics = report["metrics"]
    assert metrics["case_count"] >= 8
    assert metrics["negative_detection_rate"] == 1.0
    assert metrics["false_passed_rate"] == 0.0
    assert metrics["blocked_partial_and_pdf_failed_status_correctness"] == 1.0


def test_cli_output_is_machine_readable() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "run_forward_evals.py"),
            "--offline",
            "--check-baseline",
            "--json",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    data = json.loads(completed.stdout)
    assert data["passed"] is True
    assert data["metrics"]["case_pass_count"] == data["metrics"]["case_count"]


def test_invalid_registry_raises_explicit_error(tmp_path: Path) -> None:
    path = tmp_path / "invalid.json"
    path.write_text("{\"version\": 1}", encoding="utf-8")
    with pytest.raises(EvalRegistryError, match="missing top-level"):
        load_registry(path)
