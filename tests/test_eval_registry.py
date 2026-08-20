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
import run_forward_evals  # noqa: E402
from run_forward_evals import _evaluate_case, run  # noqa: E402
from route_activation import RouteActivationError, activate_prompt  # noqa: E402


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


def test_registry_rejects_unhashable_case_id_without_crashing() -> None:
    registry = load_registry()
    tampered = copy.deepcopy(registry)
    tampered["cases"][0]["id"] = []
    errors = validate_registry(tampered)
    assert any("kebab-case" in error for error in errors)


def test_registry_rejects_unknown_route() -> None:
    registry = load_registry()
    tampered = copy.deepcopy(registry)
    tampered["cases"][0]["expected"]["primary_route"] = "not-a-route"
    errors = validate_registry(tampered)
    assert any("unknown" in error and "primary_route" in error for error in errors)


def test_registry_rejects_decision_tree_route_mismatch() -> None:
    registry = load_registry()
    tampered = copy.deepcopy(registry)
    case = next(
        item for item in tampered["cases"] if item["id"] == "forward-provider-selection"
    )
    case["expected"]["primary_route"] = "market-outlook"
    errors = validate_registry(tampered)
    assert any("decision-tree route" in error for error in errors)


def test_registry_rejects_decision_tree_version_mismatch() -> None:
    registry = load_registry()
    tampered = copy.deepcopy(registry)
    tampered["decision_tree_version"] = 999
    errors = validate_registry(tampered)
    assert any("decision_tree_version" in error for error in errors)


def test_registry_requires_contract_for_manual_secondary_route() -> None:
    registry = load_registry()
    tampered = copy.deepcopy(registry)
    case = next(
        item
        for item in tampered["cases"]
        if item["id"] == "forward-company-technical-mixed"
    )
    case["input"].pop("secondary_route_contracts")
    errors = validate_registry(tampered)
    assert any("secondary_route_contracts" in error for error in errors)


def test_registry_rejects_missing_fixture() -> None:
    registry = load_registry()
    tampered = copy.deepcopy(registry)
    tampered["cases"][0]["fixtures"]["report"] = "tests/fixtures/forward/missing.md"
    errors = validate_registry(tampered)
    assert any("does not exist" in error for error in errors)


def test_prompt_mutation_cannot_pass_a_forward_case() -> None:
    case = copy.deepcopy(next(
        item for item in load_registry()["cases"]
        if item["id"] == "forward-provider-selection"
    ))
    case["input"]["user_prompt"] = "写一篇关于古典音乐历史的简短说明。"
    result = _evaluate_case(case)
    assert result["passed"] is False
    assert result["checks"]["activation_route_match"] is False


def test_unstructured_prompt_activation_fails_closed() -> None:
    with pytest.raises(RouteActivationError, match="structured action_burden"):
        activate_prompt("不要做排名，只分析未来趋势。", "single-track")


def test_parallelization_decision_is_consumed() -> None:
    case = copy.deepcopy(next(
        item for item in load_registry()["cases"]
        if item["id"] == "forward-provider-selection"
    ))
    case["input"]["parallelization_decision"] = "parallel"
    result = _evaluate_case(case)
    assert result["passed"] is False
    assert result["checks"]["parallelization_match"] is False


def test_negative_oracle_requires_the_declared_secondary_route() -> None:
    case = copy.deepcopy(next(
        item for item in load_registry()["cases"]
        if item["id"] == "forward-secondary-route-not-verified"
    ))
    case["expected"]["secondary_routes"] = ["listed-company"]
    result = _evaluate_case(case)
    assert result["passed"] is False
    assert result["actual"]["failure_family"] is None


def test_negative_oracle_requires_complete_status_shape() -> None:
    case = copy.deepcopy(next(
        item for item in load_registry()["cases"]
        if item["id"] == "forward-secondary-route-not-verified"
    ))
    case["expected"]["statuses"]["delivery_status"] = "pdf_failed"
    result = _evaluate_case(case)
    assert result["passed"] is False
    assert result["checks"]["statuses_match"] is False


def test_offline_forward_runner_passes_and_reports_metrics() -> None:
    report = run(check_baseline=True)
    assert report["passed"] is True
    assert report["failed_cases"] == []
    assert report["offline"] is True
    assert report["evaluation_mode"] == "offline"
    assert report["case_evaluation_modes"] == {
        "activation-record-integration": 2,
        "structured-decision-replay": 9,
    }
    assert report["decision_tree_version"] == 1
    metrics = report["metrics"]
    assert metrics["case_count"] >= 8
    assert metrics["structured_route_resolution_rate"] == 1.0
    assert metrics["activation_report_consistency"] == 1.0
    assert metrics["audit_false_pass_rate"] == 0.0
    assert metrics["oracle_mismatch_detection_rate"] == 1.0
    assert metrics["negative_case_contract_pass_rate"] == 1.0
    assert metrics["blocked_partial_and_pdf_failed_status_correctness"] == 1.0


def test_route_misclassification_is_blocked_by_production_integration_gate() -> None:
    case = next(
        item
        for item in load_registry()["cases"]
        if item["id"] == "forward-route-misclassification"
    )
    result = _evaluate_case(case, 1)
    assert result["passed"] is True
    assert result["actual"]["evaluation_mode"] == "activation-record-integration"
    assert result["actual"]["activation_route"] == "constrained-choice"
    assert result["actual"]["report_route"] == "market-outlook"
    assert result["actual"]["overall"] == "fail"
    assert result["actual"]["returncode"] == 2
    assert result["actual"]["failure_stage"] == "contract"
    assert result["checks"]["activation_snapshot_match"] is True


def test_route_misclassification_does_not_mask_unrelated_report_failure(
    tmp_path: Path,
) -> None:
    case = copy.deepcopy(next(
        item
        for item in load_registry()["cases"]
        if item["id"] == "forward-route-misclassification"
    ))
    original = ROOT / case["fixtures"]["report"]
    tampered = tmp_path / "mixed-route-mismatch.md"
    tampered.write_text(
        original.read_text(encoding="utf-8").replace(
            "Body text with citations [S01], [S02] and [S03].",
            "Body text with citations [S01], [S99] and [S03].",
        ),
        encoding="utf-8",
    )
    case["fixtures"]["report"] = str(tampered)

    result = _evaluate_case(case, 1)
    assert result["passed"] is False
    assert result["actual"]["failure_family"] == "route-misclassification"
    assert any(item.startswith("[report-quality]") for item in result["actual"]["blocking"])


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


def test_cli_malformed_registry_returns_structured_fixture_drift(tmp_path: Path) -> None:
    data = copy.deepcopy(load_registry())
    data["cases"][0]["id"] = []
    path = tmp_path / "malformed.json"
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    completed = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "validate_eval_registry.py"),
            "--registry",
            str(path),
            "--json",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 2
    result = json.loads(completed.stdout)
    assert result["valid"] is False
    assert result["gap_class"] == "fixture-reference-drift"
    assert "kebab-case" in result["error"]


def test_forward_runner_records_audit_json_provenance() -> None:
    """The forward runner must consume schema_version and validators[] so CI
    reads structured fields instead of exit code / stdout only (#393)."""
    import run_forward_evals

    case = load_registry()["cases"][0]
    result = _evaluate_case(case, 1)
    actual = result["actual"]
    assert actual["schema_version"] == 1, actual
    assert actual["validators"], "runner must record route validator results"
    for entry in actual["validators"]:
        assert entry["validator_id"], entry
        assert entry["status"], entry
    assert result["checks"]["validators_ok"] is True, result["checks"]


def _validator_entry(status="pass", **overrides) -> dict:
    """A structurally valid route-validator JSON entry."""
    entry = {
        "validator_id": "report-quality",
        "status": status,
        "errors": [],
        "warnings": [],
        "evidence": ["report: no violations found by report-quality"],
        "execution_source": "automated_validator",
        "validator_version": run_forward_evals.EXPECTED_VALIDATOR_VERSION,
    }
    entry.update(overrides)
    return entry


def test_validators_ok_requires_complete_binding_set() -> None:
    """The runner must fail closed on missing / forged / partial validator
    results, not just on an empty array (issue #393 forged-path negative)."""
    import run_forward_evals

    ok = {
        "schema_version": 1,
        "validator_version": run_forward_evals.EXPECTED_VALIDATOR_VERSION,
        "validators": [_validator_entry()],
    }
    assert run_forward_evals._validators_ok(
        {"schema_version": 1, "validator_version": "forged-top",
         "validators": [_validator_entry()]},
        ["report-quality"], audited_path="report",
    ) is False, "forged top-level validator_version must fail closed"
    assert run_forward_evals._validators_ok(
        ok, ["report-quality"], audited_path="report"
    ) is True
    assert run_forward_evals._validators_ok(
        {"schema_version": 999, "validators": [_validator_entry()]},
        ["report-quality"], audited_path="report",
    ) is False, "unknown schema_version must fail closed"
    assert run_forward_evals._validators_ok(
        {"validators": [_validator_entry()]},
        ["report-quality"], audited_path="report",
    ) is False, "missing schema_version must fail closed"
    assert run_forward_evals._validators_ok(
        {"schema_version": 1, "validators": []},
        ["report-quality"], audited_path="report",
    ) is False, "missing validator results must fail closed"
    assert run_forward_evals._validators_ok(
        {"schema_version": 1, "validators": [_validator_entry(status="incomplete")]},
        ["report-quality"], audited_path="report",
    ) is False, "incomplete validator must fail closed"
    assert run_forward_evals._validators_ok(
        {"schema_version": 1, "validators": [_validator_entry(validator_id="forged")]},
        ["report-quality"], audited_path="report",
    ) is False, "forged validator id must fail closed"
    assert run_forward_evals._validators_ok(
        {"schema_version": 1, "validators": [_validator_entry(validator_id="other")]},
        ["report-quality", "other"], audited_path="report",
    ) is False, "missing an expected validator must fail closed"
    assert run_forward_evals._validators_ok(
        {"schema_version": 1, "validators": [_validator_entry(evidence=[])]},
        ["report-quality"], audited_path="report",
    ) is False, "missing evidence must fail closed"
    assert run_forward_evals._validators_ok(
        {"schema_version": 1, "validators": [_validator_entry(evidence="not-a-list")]},
        ["report-quality"], audited_path="report",
    ) is False, "non-list evidence must fail closed"
    assert run_forward_evals._validators_ok(
        {"schema_version": 1, "validators": [_validator_entry(
            evidence=["/does/not/exist: no violations found by report-quality"])]},
        ["report-quality"], audited_path="report",
    ) is False, "evidence locator must reference the audited report"
    assert run_forward_evals._validators_ok(
        {"schema_version": 1, "validators": [_validator_entry(
            evidence=["report.evil: no violations found by report-quality"])]},
        ["report-quality"], audited_path="report",
    ) is False, "prefix-bypass evidence (report.evil) must fail closed"
    assert run_forward_evals._validators_ok(
        {"schema_version": 1, "validators": [_validator_entry(
            execution_source="")]},
        ["report-quality"], audited_path="report",
    ) is False, "empty execution_source must fail closed"
    assert run_forward_evals._validators_ok(
        {"schema_version": 1, "validators": [_validator_entry(
            validator_version="")]},
        ["report-quality"], audited_path="report",
    ) is False, "empty validator_version must fail closed"
    assert run_forward_evals._validators_ok(
        {"schema_version": 1, "validators": ["not-a-dict"]},
        ["report-quality"], audited_path="report",
    ) is False, "non-object validator entry must fail closed"
    assert run_forward_evals._validators_ok(
        {"schema_version": 1, "validators": [_validator_entry(validator_version=None)]},
        ["report-quality"], audited_path="report",
    ) is False, "missing validator_version must fail closed"
    assert run_forward_evals._validators_ok(
        {"schema_version": 1, "validators": [_validator_entry(
            errors=["boom"], warnings=[])]},
        ["report-quality"], audited_path="report",
    ) is False, "status=pass with errors must fail closed"
    assert run_forward_evals._validators_ok(
        {"schema_version": 1, "validators": [_validator_entry(
            status="conditional-pass", warnings=[], evidence=["report: no violations found by report-quality"])]},
        ["report-quality"], audited_path="report",
    ) is False, "conditional-pass without warnings must fail closed"
    assert run_forward_evals._validators_ok(
        {"schema_version": 1, "validators": [_validator_entry(
            status="fail", errors=[], evidence=["report: no violations found by report-quality"])]},
        ["report-quality"], audited_path="report",
    ) is False, "fail without errors must fail closed"
    assert run_forward_evals._validators_ok(
        {"schema_version": 1, "validators": [
            _validator_entry(),
            _validator_entry(),  # duplicate validator_id
        ]},
        ["report-quality"], audited_path="report",
    ) is False, "duplicate validator entry must fail closed"
    assert run_forward_evals._validators_ok(
        {"schema_version": 1, "validators": [_validator_entry()]},
        ["report-quality"], audited_path=None,
    ) is False, "unverifiable pass evidence must fail closed"


def test_forward_runner_rejects_forged_validators(monkeypatch) -> None:
    """Replacing the real validator results with a forged single entry must
    make the forward runner fail closed, not pass (issue #393)."""
    import run_forward_evals

    case = load_registry()["cases"][0]
    fixtures = case["fixtures"]
    report = ROOT / fixtures["report"]
    pack = ROOT / fixtures["research_pack"]
    real_data, _, _ = run_forward_evals._run_audit(report, pack)
    forged = {
        **real_data,
        "validators": [_validator_entry(validator_id="forged")],
    }

    def fake_run(report, research_pack, activation_snapshot=None):
        return forged, None, 0

    monkeypatch.setattr(run_forward_evals, "_run_audit", fake_run)
    result = _evaluate_case(case, 1)
    assert result["checks"]["validators_ok"] is False, result["checks"]
    assert result["passed"] is False


def test_audit_json_schema_version_contract() -> None:
    """The runner's pinned schema version must match audit_report's constant
    so a JSON contract bump cannot silently drift past the runner (#393)."""
    import audit_report
    import run_forward_evals

    assert audit_report.AUDIT_JSON_SCHEMA_VERSION == (
        run_forward_evals.EXPECTED_AUDIT_JSON_SCHEMA_VERSION
    )
