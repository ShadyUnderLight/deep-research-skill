#!/usr/bin/env python3
"""Execute the offline route-sharp forward-eval registry.

The runner deliberately consumes the existing command-line audit surface and
its JSON output. It does not call a paid model, browse the network, or invent a
production prompt classifier. Structured replay cases supply canonical
action/object activation inputs and a prompt hash. Integration cases also pass
a versioned activation snapshot into the production audit command so route
mismatch is a real blocking assertion rather than a runner-only oracle.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

from eval_registry import (
    DEFAULT_REGISTRY_PATH,
    EvalRegistryError,
    active_cases,
    gap_class_for_failure_family,
    failure_stage_for_failure_family,
    load_registry,
)
from validate_contract import extract_contract_from_markdown
from validate_research_pack import (
    extract_declared_statuses,
    find_missing_headings,
    strip_fenced_code_blocks,
)
from route_activation import RouteActivationError, activate_prompt
from activation_snapshot import (
    ActivationSnapshotError,
    activation_reference,
    build_activation_snapshot,
    extract_activation_snapshot_reference,
    load_activation_snapshot,
)


ROOT = Path(__file__).resolve().parents[1]
AUDIT_SCRIPT = ROOT / "scripts" / "audit_report.py"
DEFAULT_BASELINE_PATH = ROOT / "evals" / "forward-metrics-baseline.json"

# The audit JSON verdict schema this runner understands.  A schema_version it
# does not know must fail closed instead of being treated as a Pass
# (issue #393: unknown JSON shape ⇒ incomplete, never pass).
EXPECTED_AUDIT_JSON_SCHEMA_VERSION = 1


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _ratio(numerator: int, denominator: int) -> float:
    return round(numerator / denominator, 4) if denominator else 1.0


def _pack_observation(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8", errors="replace")
    cleaned = strip_fenced_code_blocks(text)
    headings = {
        line.removeprefix("## ").strip()
        for line in cleaned.splitlines()
        if line.startswith("## ")
    }
    statuses = extract_declared_statuses(text)
    version_match = re.search(
        r"^## Decision tree version\s*\n+[ \t]*([0-9]+)[ \t]*$",
        cleaned,
        re.MULTILINE,
    )
    activation_snapshot, activation_snapshot_errors = (
        extract_activation_snapshot_reference(cleaned, label="Research Pack")
    )
    return {
        "fields": sorted(headings),
        "missing_required_fields": find_missing_headings(cleaned),
        "statuses": statuses,
        "decision_tree_version": int(version_match.group(1)) if version_match else None,
        "activation_snapshot": activation_snapshot,
        "activation_snapshot_errors": activation_snapshot_errors,
    }


def _run_audit(
    report: Path,
    research_pack: Path,
    activation_snapshot: Path | None = None,
) -> tuple[dict[str, Any] | None, str | None, int]:
    command = [
        sys.executable,
        str(AUDIT_SCRIPT),
        str(report),
        "--research-pack",
        str(research_pack),
        "--strict",
        "--require-contract",
        "--json",
    ]
    if activation_snapshot is not None:
        command.extend(["--activation-snapshot", str(activation_snapshot)])
    completed = subprocess.run(command, capture_output=True, text=True, cwd=ROOT)
    try:
        data = json.loads(completed.stdout)
    except json.JSONDecodeError:
        detail = (completed.stderr or completed.stdout).strip()
        return None, detail[:500] or "audit_report.py did not emit JSON", completed.returncode
    return data, None, completed.returncode


def _detect_failure_family(case: dict[str, Any], actual: dict[str, Any]) -> str | None:
    expected_family = case.get("failure_family")
    if expected_family == "route-misclassification":
        if (
            actual["activation_route"] != actual["expected_route"]
            or actual["activation_route"] != actual["report_route"]
        ):
            return expected_family
    if expected_family == "secondary-route-not-verified":
        expected_secondary = set(case["expected"].get("secondary_routes", []))
        if set(actual["secondary_routes"]) != expected_secondary:
            return None
        expected_targets = {f"{route}-secondary-hard-fail" for route in expected_secondary}
        secondary_audits = [
            item
            for item in actual.get("audits", [])
            if str(item.get("audit_id", "")) in expected_targets
        ]
        if expected_targets and {
            str(item.get("audit_id")) for item in secondary_audits
        } != expected_targets:
            return expected_family
        if any(item.get("status") != "pass" for item in secondary_audits):
            return expected_family
        if any("secondary route" in str(message).lower() for message in actual.get("blocking", [])):
            return expected_family
    if expected_family == "declared-not-executed":
        if any(
            item.get("execution_type") in {"manual", "process"}
            and item.get("status") in {"not_run", "partial", "skipped"}
            for item in actual.get("audits", [])
        ):
            return expected_family
    if actual.get("overall") == "fail":
        return "audit-failure"
    return None


def _audit_statuses(actual: dict[str, Any]) -> dict[str, str]:
    return {
        str(item.get("audit_id")): str(item.get("status"))
        for item in actual.get("audits", [])
        if item.get("audit_id")
    }


def _validators_ok(actual: dict[str, Any]) -> bool:
    """Consume the structured audit JSON provenance fields (issue #393).

    A verdict is consumable only when:
    - the JSON schema_version is the one this runner understands; an unknown
      shape fails closed (never treated as Pass);
    - route-level validator results are present and none is ``incomplete`` /
      ``not_run`` — a missing validator result must not be interpreted as
      a silent Pass.
    """
    if actual.get("schema_version") != EXPECTED_AUDIT_JSON_SCHEMA_VERSION:
        return False
    validators = actual.get("validators") or []
    if not validators:
        return False
    return all(
        str(item.get("status")) not in {"incomplete", "not_run"}
        for item in validators
    )


def _blocking_ids_are_allowed(actual: dict[str, Any], allowed: set[str]) -> bool:
    for message in actual.get("blocking", []):
        match = re.match(r"\[([^\]]+)\]", str(message))
        if match and match.group(1) not in allowed:
            return False
    return True


def _blocking_ids_are_exact(actual: dict[str, Any], allowed: set[str]) -> bool:
    """Require every blocking message to carry one of the allowed sources."""
    blocking = actual.get("blocking", [])
    if not blocking:
        return False
    return all(
        (match := re.match(r"\[([^\]]+)\]", str(message))) is not None
        and match.group(1) in allowed
        for message in blocking
    )


def _negative_structure_matches(case: dict[str, Any], actual: dict[str, Any], checks: dict[str, bool]) -> bool:
    """Require the intended defect shape, not merely any failing audit."""
    family = case.get("failure_family")
    if family == "route-misclassification":
        # The activation snapshot must be correct while the report artifact
        # deliberately carries the wrong primary route.
        return all(
            [
                checks["activation_route_match"],
                not checks["report_route_match"],
                checks["activation_secondary_routes_match"],
                checks["report_secondary_routes_match"],
                checks["parallelization_match"],
                checks["prompt_identity_match"],
                checks["activation_snapshot_match"],
                checks["statuses_match"],
                _blocking_ids_are_exact(actual, {"contract-check"}),
            ]
        )

    common = [
        checks["activation_route_match"],
        checks["report_route_match"],
        checks["activation_report_consistent"],
        checks["activation_secondary_routes_match"],
        checks["report_secondary_routes_match"],
        checks["disciplines_match"],
        checks["pack_fields_present"],
        checks["parallelization_match"],
        checks["prompt_identity_match"],
        checks["decision_tree_version_match"],
        checks["statuses_match"],
    ]
    statuses = _audit_statuses(actual)
    expected_audits = set(case["expected"].get("required_audits", []))
    if family == "secondary-route-not-verified":
        secondary_targets = {
            f"{route}-secondary-hard-fail"
            for route in case["expected"].get("secondary_routes", [])
        }
        target_present_and_failed = any(
            audit_id in secondary_targets and statuses.get(audit_id) != "pass"
            for audit_id in secondary_targets
        )
        primary_ids = expected_audits - secondary_targets
        failed_ids = {audit_id for audit_id, status in statuses.items() if status != "pass"}
        return (
            all(common)
            and all(audit_id in statuses and statuses[audit_id] == "pass" for audit_id in primary_ids)
            and failed_ids.issubset(secondary_targets)
            and _blocking_ids_are_allowed(actual, {"contract-check", *secondary_targets})
            and target_present_and_failed
        )
    if family == "declared-not-executed":
        target_present_and_unrun = any(
            audit_id in expected_audits and statuses.get(audit_id) in {"not_run", "partial", "skipped"}
            for audit_id in expected_audits
        )
        failed_ids = {audit_id for audit_id, status in statuses.items() if status != "pass"}
        allowed_targets = {
            audit_id
            for audit_id in expected_audits
            if statuses.get(audit_id) in {"not_run", "partial", "skipped"}
        }
        return (
            all(common)
            and failed_ids.issubset(allowed_targets)
            and _blocking_ids_are_allowed(actual, allowed_targets)
            and target_present_and_unrun
        )
    return all(common)


def _evaluate_case(
    case: dict[str, Any], expected_decision_tree_version: int | None = None
) -> dict[str, Any]:
    expected = case["expected"]
    input_data = case["input"]
    fixtures = case["fixtures"]
    evaluation_mode = case.get("evaluation_mode", "structured-decision-replay")
    report = ROOT / fixtures["report"]
    research_pack = ROOT / fixtures["research_pack"]
    pack = _pack_observation(research_pack)

    activation_error: str | None = None
    activation_snapshot_error: str | None = None
    activation_snapshot_data: dict[str, Any] | None = None
    activation_snapshot_path: Path | None = None
    try:
        activation = activate_prompt(
            input_data["user_prompt"],
            input_data["parallelization_decision"],
            action_category=input_data["action_burden"],
            weight_bearing_object=input_data["weight_bearing_object"],
            secondary_routes=input_data["secondary_routes"],
            secondary_route_contracts=input_data.get("secondary_route_contracts", {}),
            expected_prompt_sha256=input_data["prompt_sha256"],
        )
    except RouteActivationError as exc:
        activation = None
        activation_error = str(exc)

    if evaluation_mode == "activation-record-integration":
        activation_snapshot_path = ROOT / fixtures["activation_snapshot"]
        try:
            activation_snapshot_data = load_activation_snapshot(
                activation_snapshot_path
            )
            if activation is None:
                raise ActivationSnapshotError(
                    "structured activation did not produce a snapshot"
                )
            expected_snapshot = build_activation_snapshot(
                case["id"], activation, evaluation_mode=evaluation_mode
            )
            if activation_snapshot_data != expected_snapshot:
                raise ActivationSnapshotError(
                    "fixture activation snapshot does not match the structured "
                    "activation result"
                )
        except (ActivationSnapshotError, OSError, KeyError) as exc:
            activation_snapshot_error = str(exc)

    audit_data, runner_error, returncode = _run_audit(
        report,
        research_pack,
        activation_snapshot=activation_snapshot_path,
    )

    contract: dict[str, Any] = {}
    if report.is_file():
        contract = extract_contract_from_markdown(
            report.read_text(encoding="utf-8", errors="replace")
        ) or {}

    report_route = audit_data.get("route") if audit_data else None
    actual_statuses = {
        "research_status": pack["statuses"].get("research_status"),
        "audit_status": audit_data.get("overall") if audit_data else None,
        "delivery_status": pack["statuses"].get("delivery_status"),
    }
    requires_decision_tree = "Decision tree path" in expected["research_pack_fields"]
    decision_tree_version_match = (
        not requires_decision_tree
        or (
            expected_decision_tree_version is not None
            and activation is not None
            and activation.decision_tree_version == expected_decision_tree_version
            and pack["decision_tree_version"] == expected_decision_tree_version
        )
    )
    actual = {
        "route": report_route,
        "report_route": report_route,
        "activation_route": activation.primary_route if activation else None,
        "activation_secondary_routes": sorted(activation.secondary_routes) if activation else [],
        "activation_action_category": activation.action_category if activation else None,
        "activation_weight_bearing_object": activation.weight_bearing_object if activation else None,
        "activation_parallelization_decision": activation.parallelization_decision if activation else None,
        "activation_prompt_sha256": activation.prompt_sha256 if activation else None,
        "activation_decision_tree_version": (
            activation.decision_tree_version if activation else None
        ),
        "pack_decision_tree_version": pack["decision_tree_version"],
        "activation_error": activation_error,
        "evaluation_mode": evaluation_mode,
        "activation_snapshot_error": activation_snapshot_error,
        "activation_snapshot": (
            activation_reference(activation_snapshot_data)
            if activation_snapshot_data is not None
            else None
        ),
        "contract_activation_snapshot": contract.get("activation_snapshot"),
        "pack_activation_snapshot": pack.get("activation_snapshot"),
        "closest_alternative": contract.get("closest_alternative"),
        "secondary_routes": sorted(contract.get("secondary_routes", []) or []),
        "disciplines": sorted(contract.get("disciplines", []) or []),
        "audit_ids": sorted(
            {str(item.get("audit_id")) for item in (audit_data or {}).get("audits", [])}
        ),
        "audits": (audit_data or {}).get("audits", []),
        "validators": (audit_data or {}).get("validators", []),
        "schema_version": (audit_data or {}).get("schema_version"),
        "overall": (audit_data or {}).get("overall"),
        "blocking": (audit_data or {}).get("blocking", []),
        "statuses": actual_statuses,
        "pack_fields": pack["fields"],
        "pack_missing_required_fields": pack["missing_required_fields"],
        "returncode": returncode,
        "runner_error": runner_error,
        "expected_route": expected["primary_route"],
    }
    actual["failure_family"] = _detect_failure_family(case, actual)
    actual["gap_class"] = gap_class_for_failure_family(actual["failure_family"])
    actual["failure_stage"] = failure_stage_for_failure_family(
        actual["failure_family"]
    )

    expected_pack_fields = set(expected["research_pack_fields"])
    expected_audits = set(expected["required_audits"])
    actual_audits = set(actual["audit_ids"])
    activation_route_match = actual["activation_route"] == expected["primary_route"]
    report_route_match = actual["report_route"] == expected["primary_route"]
    activation_report_consistent = actual["activation_route"] == actual["report_route"]
    alternative_match = actual["closest_alternative"] == expected["closest_alternative"]
    activation_secondary_match = (
        actual["activation_secondary_routes"] == sorted(expected["secondary_routes"])
    )
    report_secondary_match = actual["secondary_routes"] == sorted(expected["secondary_routes"])
    secondary_match = activation_secondary_match and report_secondary_match
    discipline_match = actual["disciplines"] == sorted(expected["disciplines"])
    audit_ids_match = expected_audits.issubset(actual_audits)
    pack_fields_match = expected_pack_fields.issubset(set(actual["pack_fields"]))
    status_match = actual["statuses"] == expected["statuses"]
    parallelization_match = (
        actual["activation_parallelization_decision"]
        == expected["parallelization_decision"]
    )
    prompt_identity_match = actual["activation_prompt_sha256"] == input_data["prompt_sha256"]
    activation_snapshot_match = (
        evaluation_mode != "activation-record-integration"
        or (
            actual["activation_snapshot_error"] is None
            and actual["activation_snapshot"] is not None
            and actual["contract_activation_snapshot"] == actual["activation_snapshot"]
            and actual["pack_activation_snapshot"] == actual["activation_snapshot"]
        )
    )
    expected_returncode = {
        "pass": 0,
        "conditional-pass": 1,
        "fail": 2,
    }.get(expected["statuses"]["audit_status"])

    validators_ok = _validators_ok(actual)
    if expected["verdict"] == "pass":
        case_passed = all(
            [
                activation_route_match,
                report_route_match,
                activation_report_consistent,
                alternative_match,
                secondary_match,
                discipline_match,
                audit_ids_match,
                pack_fields_match,
                status_match,
                parallelization_match,
                prompt_identity_match,
                decision_tree_version_match,
                activation_snapshot_match,
                validators_ok,
                actual["overall"] == expected["statuses"]["audit_status"],
                returncode == expected_returncode,
            ]
        )
    else:
        negative_returncode_ok = (
            returncode == 2
            if evaluation_mode == "activation-record-integration"
            else returncode in {0, 1}
            if case.get("failure_family") == "route-misclassification"
            else returncode == 2
        )
        checks_for_negative = {
            "activation_route_match": activation_route_match,
            "report_route_match": report_route_match,
            "activation_report_consistent": activation_report_consistent,
            "activation_secondary_routes_match": activation_secondary_match,
            "report_secondary_routes_match": report_secondary_match,
            "disciplines_match": discipline_match,
            "pack_fields_present": pack_fields_match,
            "parallelization_match": parallelization_match,
            "prompt_identity_match": prompt_identity_match,
            "decision_tree_version_match": decision_tree_version_match,
            "activation_snapshot_match": activation_snapshot_match,
            "statuses_match": status_match,
        }
        case_passed = all(
            [
                actual["failure_family"] == case["failure_family"],
                _negative_structure_matches(case, actual, checks_for_negative),
                validators_ok,
                actual["overall"] == expected["statuses"]["audit_status"],
                negative_returncode_ok,
            ]
        )

    return {
        "case_id": case["id"],
        "passed": case_passed,
        "expected": {
            "route": expected["primary_route"],
            "closest_alternative": expected["closest_alternative"],
            "secondary_routes": expected["secondary_routes"],
            "statuses": expected["statuses"],
            "verdict": expected["verdict"],
            "failure_family": case["failure_family"],
            "gap_class": gap_class_for_failure_family(case["failure_family"]),
            "evaluation_mode": evaluation_mode,
            "failure_stage": expected.get("failure_stage"),
        },
        "actual": {
            "route": actual["route"],
            "report_route": actual["report_route"],
            "activation_route": actual["activation_route"],
            "activation_secondary_routes": actual["activation_secondary_routes"],
            "activation_action_category": actual["activation_action_category"],
            "activation_weight_bearing_object": actual["activation_weight_bearing_object"],
            "activation_parallelization_decision": actual["activation_parallelization_decision"],
            "activation_prompt_sha256": actual["activation_prompt_sha256"],
            "activation_decision_tree_version": actual["activation_decision_tree_version"],
            "pack_decision_tree_version": actual["pack_decision_tree_version"],
            "activation_error": actual["activation_error"],
            "closest_alternative": actual["closest_alternative"],
            "secondary_routes": actual["secondary_routes"],
            "disciplines": actual["disciplines"],
            "audit_ids": actual["audit_ids"],
            "audits": actual["audits"],
            "validators": actual["validators"],
            "schema_version": actual["schema_version"],
            "blocking": actual["blocking"],
            "statuses": actual["statuses"],
            "overall": actual["overall"],
            "failure_family": actual["failure_family"],
            "gap_class": actual["gap_class"],
            "failure_stage": actual["failure_stage"],
            "evaluation_mode": actual["evaluation_mode"],
            "activation_snapshot_error": actual["activation_snapshot_error"],
            "activation_snapshot": actual["activation_snapshot"],
            "contract_activation_snapshot": actual["contract_activation_snapshot"],
            "pack_activation_snapshot": actual["pack_activation_snapshot"],
            "pack_missing_required_fields": actual["pack_missing_required_fields"],
            "returncode": returncode,
            "runner_error": runner_error,
        },
        "checks": {
            "activation_route_match": activation_route_match,
            "report_route_match": report_route_match,
            "activation_report_consistent": activation_report_consistent,
            "alternative_match": alternative_match,
            "activation_secondary_routes_match": activation_secondary_match,
            "report_secondary_routes_match": report_secondary_match,
            "secondary_routes_match": secondary_match,
            "disciplines_match": discipline_match,
            "required_audits_present": audit_ids_match,
            "pack_fields_present": pack_fields_match,
            "statuses_match": status_match,
            "parallelization_match": parallelization_match,
            "prompt_identity_match": prompt_identity_match,
            "decision_tree_version_match": decision_tree_version_match,
            "activation_snapshot_match": activation_snapshot_match,
            "validators_ok": validators_ok,
        },
    }


def _metrics(cases: list[dict[str, Any]], results: list[dict[str, Any]]) -> dict[str, Any]:
    by_id = {result["case_id"]: result for result in results}
    positives = [case for case in cases if case["type"] == "positive"]
    negatives = [case for case in cases if case["type"] == "negative"]
    structured_positive_cases = [
        case
        for case in positives
        if case.get("evaluation_mode", "structured-decision-replay")
        == "structured-decision-replay"
    ]
    integration_positive_cases = [
        case
        for case in positives
        if case.get("evaluation_mode") == "activation-record-integration"
    ]
    integration_negative_cases = [
        case
        for case in negatives
        if case.get("evaluation_mode") == "activation-record-integration"
    ]
    oracle_mismatch_cases = [
        case
        for case in negatives
        if case.get("failure_family") == "route-misclassification"
    ]
    boundary_cases = [
        case
        for case in positives
        if case["expected"].get("closest_alternative") is not None
    ]
    boundary_resolved = sum(
        by_id[case["id"]]["checks"]["alternative_match"] for case in boundary_cases
    )
    structured_route_correct = sum(
        by_id[case["id"]]["checks"]["activation_route_match"]
        for case in structured_positive_cases
    )
    report_route_consistent = sum(
        by_id[case["id"]]["checks"]["activation_report_consistent"]
        for case in integration_positive_cases
    )
    secondary_cases = [
        case for case in negatives if case.get("failure_family") == "secondary-route-not-verified"
    ]
    secondary_recalled = sum(
        by_id[case["id"]]["actual"]["failure_family"] == "secondary-route-not-verified"
        for case in secondary_cases
    )
    declared_cases = [
        case for case in negatives if case.get("failure_family") == "declared-not-executed"
    ]
    declared_recalled = sum(
        by_id[case["id"]]["actual"]["failure_family"] == "declared-not-executed"
        for case in declared_cases
    )
    pack_complete = sum(
        result["checks"]["pack_fields_present"] for result in results
    )
    declared_not_executed_observed = sum(
        any(
            item.get("execution_type") in {"manual", "process"}
            and item.get("status") in {"not_run", "partial", "skipped"}
            for item in result["actual"].get("audits", [])
        )
        for result in results
    )
    integration_false_passed = sum(
        by_id[case["id"]]["actual"]["overall"] == "pass"
        for case in integration_negative_cases
    )
    oracle_mismatch_detected = sum(
        by_id[case["id"]]["actual"]["failure_family"]
        == "route-misclassification"
        for case in oracle_mismatch_cases
    )
    status_cases = [
        case
        for case in cases
        if case["expected"].get("statuses", {}).get("research_status") in {"blocked", "partial"}
        or case["expected"].get("statuses", {}).get("delivery_status") == "pdf_failed"
    ]
    status_correct = sum(
        by_id[case["id"]]["checks"]["statuses_match"] for case in status_cases
    )
    return {
        "case_count": len(cases),
        "positive_case_count": len(positives),
        "negative_case_count": len(negatives),
        "case_pass_count": sum(result["passed"] for result in results),
        "structured_route_resolution_rate": _ratio(
            structured_route_correct, len(structured_positive_cases)
        ),
        "activation_report_consistency": _ratio(
            report_route_consistent, len(integration_positive_cases)
        ),
        "parallelization_decision_consistency": _ratio(
            sum(result["checks"]["parallelization_match"] for result in results),
            len(results),
        ),
        "boundary_resolution_rate": _ratio(boundary_resolved, len(boundary_cases)),
        "pack_completeness": _ratio(pack_complete, len(results)),
        "secondary_hard_fail_recall": _ratio(secondary_recalled, len(secondary_cases)),
        "declared_not_executed_recall": _ratio(declared_recalled, len(declared_cases)),
        "declared_not_executed_rate": _ratio(declared_not_executed_observed, len(results)),
        "audit_false_pass_rate": _ratio(
            integration_false_passed, len(integration_negative_cases)
        ),
        "oracle_mismatch_detection_rate": _ratio(
            oracle_mismatch_detected, len(oracle_mismatch_cases)
        ),
        "negative_case_contract_pass_rate": _ratio(
            sum(by_id[case["id"]]["passed"] for case in negatives),
            len(negatives),
        ),
        "blocked_partial_and_pdf_failed_status_correctness": _ratio(
            status_correct, len(status_cases)
        ),
    }


def _check_baseline(metrics: dict[str, Any], baseline_path: Path) -> list[str]:
    if not baseline_path.is_file():
        return [f"metrics baseline not found: {baseline_path}"]
    try:
        baseline = _read_json(baseline_path)
    except (OSError, json.JSONDecodeError) as exc:
        return [f"metrics baseline is invalid: {exc}"]
    expected = baseline.get("metrics") if isinstance(baseline, dict) else None
    if not isinstance(expected, dict):
        return ["metrics baseline must contain an object field named 'metrics'"]
    mismatches = []
    for key, value in expected.items():
        if metrics.get(key) != value:
            mismatches.append(f"{key}: expected {value!r}, got {metrics.get(key)!r}")
    return mismatches


def run(registry_path: Path = DEFAULT_REGISTRY_PATH, *, check_baseline: bool = False) -> dict[str, Any]:
    registry = load_registry(registry_path)
    cases = active_cases(registry)
    results = [
        _evaluate_case(case, registry["decision_tree_version"])
        for case in cases
    ]
    metrics = _metrics(cases, results)
    baseline_errors = (
        _check_baseline(metrics, DEFAULT_BASELINE_PATH) if check_baseline else []
    )
    failed_cases = [result for result in results if not result["passed"]]
    return {
        "registry_version": registry["version"],
        "decision_tree_version": registry["decision_tree_version"],
        "offline": True,
        "evaluation_mode": "offline",
        "case_evaluation_modes": {
            mode: sum(
                case.get("evaluation_mode", "structured-decision-replay") == mode
                for case in cases
            )
            for mode in sorted(
                {
                    case.get("evaluation_mode", "structured-decision-replay")
                    for case in cases
                }
            )
        },
        "metrics": metrics,
        "baseline_errors": baseline_errors,
        "passed": not failed_cases and not baseline_errors,
        "failed_cases": failed_cases,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run offline route-sharp forward evals")
    parser.add_argument(
        "--registry",
        type=Path,
        default=DEFAULT_REGISTRY_PATH,
        help="path to the eval registry JSON",
    )
    parser.add_argument(
        "--offline",
        action="store_true",
        help="explicitly document the offline execution mode (the default)",
    )
    parser.add_argument(
        "--check-baseline",
        action="store_true",
        help="compare metrics with evals/forward-metrics-baseline.json",
    )
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = parser.parse_args(argv)

    try:
        report = run(args.registry, check_baseline=args.check_baseline)
    except EvalRegistryError as exc:
        report = {
            "registry_version": None,
            "offline": True,
            "metrics": {},
            "baseline_errors": [],
            "passed": False,
            "failed_cases": [],
            "gap_class": "fixture-reference-drift",
            "registry_error": str(exc),
        }

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        if report.get("registry_error"):
            print(f"Registry validation failed: {report['registry_error']}")
        else:
            status = "PASS" if report["passed"] else "FAIL"
            print(f"{status}: {report['metrics']['case_count']} offline forward cases")
            print(json.dumps(report["metrics"], ensure_ascii=False, indent=2, sort_keys=True))
            for result in report["failed_cases"]:
                print(f"- FAIL {result['case_id']}: {result['actual']}")
            for error in report["baseline_errors"]:
                print(f"- BASELINE {error}")
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
