#!/usr/bin/env python3
"""Execute the offline route-sharp forward-eval registry.

The runner deliberately consumes the existing command-line audit surface and
its JSON output.  It does not call a paid model, browse the network, or invent
a production prompt classifier.  A case's user prompt and expected activation
are recorded in the registry; the report and Research Pack fixtures represent
the deterministic activation/output snapshot that is replayed offline.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from eval_registry import (
    DEFAULT_REGISTRY_PATH,
    EvalRegistryError,
    active_cases,
    gap_class_for_failure_family,
    load_registry,
)
from validate_contract import extract_contract_from_markdown
from validate_research_pack import (
    extract_declared_statuses,
    find_missing_headings,
    strip_fenced_code_blocks,
)


ROOT = Path(__file__).resolve().parents[1]
AUDIT_SCRIPT = ROOT / "scripts" / "audit_report.py"
DEFAULT_BASELINE_PATH = ROOT / "evals" / "forward-metrics-baseline.json"


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
    return {
        "fields": sorted(headings),
        "missing_required_fields": find_missing_headings(cleaned),
        "statuses": statuses,
    }


def _run_audit(report: Path, research_pack: Path) -> tuple[dict[str, Any] | None, str | None, int]:
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
        if actual["route"] != actual["expected_route"]:
            return expected_family
    if expected_family == "secondary-route-not-verified":
        secondary_audits = [
            item
            for item in actual.get("audits", [])
            if str(item.get("audit_id", "")).endswith("-secondary-hard-fail")
        ]
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


def _evaluate_case(case: dict[str, Any]) -> dict[str, Any]:
    expected = case["expected"]
    fixtures = case["fixtures"]
    report = ROOT / fixtures["report"]
    research_pack = ROOT / fixtures["research_pack"]
    pack = _pack_observation(research_pack)
    audit_data, runner_error, returncode = _run_audit(report, research_pack)

    contract: dict[str, Any] = {}
    if report.is_file():
        contract = extract_contract_from_markdown(
            report.read_text(encoding="utf-8", errors="replace")
        ) or {}

    actual_route = audit_data.get("route") if audit_data else None
    actual_statuses = {
        "research_status": pack["statuses"].get("research_status"),
        "audit_status": audit_data.get("overall") if audit_data else None,
        "delivery_status": pack["statuses"].get("delivery_status"),
    }
    actual = {
        "route": actual_route,
        "closest_alternative": contract.get("closest_alternative"),
        "secondary_routes": sorted(contract.get("secondary_routes", []) or []),
        "disciplines": sorted(contract.get("disciplines", []) or []),
        "audit_ids": sorted(
            {str(item.get("audit_id")) for item in (audit_data or {}).get("audits", [])}
        ),
        "audits": (audit_data or {}).get("audits", []),
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

    expected_pack_fields = set(expected["research_pack_fields"])
    expected_audits = set(expected["required_audits"])
    actual_audits = set(actual["audit_ids"])
    route_match = actual["route"] == expected["primary_route"]
    alternative_match = actual["closest_alternative"] == expected["closest_alternative"]
    secondary_match = actual["secondary_routes"] == sorted(expected["secondary_routes"])
    discipline_match = actual["disciplines"] == sorted(expected["disciplines"])
    audit_ids_match = expected_audits.issubset(actual_audits)
    pack_fields_match = expected_pack_fields.issubset(set(actual["pack_fields"]))
    status_match = actual["statuses"] == expected["statuses"]
    expected_returncode = {
        "pass": 0,
        "conditional-pass": 1,
        "fail": 2,
    }.get(expected["statuses"]["audit_status"])

    if expected["verdict"] == "pass":
        case_passed = all(
            [
                route_match,
                alternative_match,
                secondary_match,
                discipline_match,
                audit_ids_match,
                pack_fields_match,
                status_match,
                actual["overall"] == expected["statuses"]["audit_status"],
                returncode == expected_returncode,
            ]
        )
    else:
        negative_returncode_ok = (
            returncode in {0, 1}
            if case.get("failure_family") == "route-misclassification"
            else returncode == 2
        )
        case_passed = all(
            [
                actual["failure_family"] == case["failure_family"],
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
        },
        "actual": {
            "route": actual["route"],
            "closest_alternative": actual["closest_alternative"],
            "secondary_routes": actual["secondary_routes"],
            "disciplines": actual["disciplines"],
            "audit_ids": actual["audit_ids"],
            "statuses": actual["statuses"],
            "overall": actual["overall"],
            "failure_family": actual["failure_family"],
            "gap_class": actual["gap_class"],
            "pack_missing_required_fields": actual["pack_missing_required_fields"],
            "returncode": returncode,
            "runner_error": runner_error,
        },
        "checks": {
            "route_match": route_match,
            "alternative_match": alternative_match,
            "secondary_routes_match": secondary_match,
            "disciplines_match": discipline_match,
            "required_audits_present": audit_ids_match,
            "pack_fields_present": pack_fields_match,
            "statuses_match": status_match,
        },
    }


def _metrics(cases: list[dict[str, Any]], results: list[dict[str, Any]]) -> dict[str, Any]:
    by_id = {result["case_id"]: result for result in results}
    positives = [case for case in cases if case["type"] == "positive"]
    negatives = [case for case in cases if case["type"] == "negative"]
    boundary_cases = [
        case
        for case in positives
        if case["expected"].get("closest_alternative") is not None
    ]
    boundary_resolved = sum(
        by_id[case["id"]]["checks"]["alternative_match"] for case in boundary_cases
    )
    route_correct = sum(
        by_id[case["id"]]["checks"]["route_match"] for case in positives
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
    raw_audit_false_passed = sum(
        by_id[case["id"]]["actual"]["overall"] == "pass" for case in negatives
    )
    false_passed = sum(
        not by_id[case["id"]]["passed"] for case in negatives
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
        "route_activation_accuracy": _ratio(route_correct, len(positives)),
        "boundary_resolution_rate": _ratio(boundary_resolved, len(boundary_cases)),
        "secondary_hard_fail_recall": _ratio(secondary_recalled, len(secondary_cases)),
        "declared_not_executed_recall": _ratio(declared_recalled, len(declared_cases)),
        "false_passed_rate": _ratio(false_passed, len(negatives)),
        "raw_audit_false_passed_rate": _ratio(raw_audit_false_passed, len(negatives)),
        "negative_detection_rate": _ratio(
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
    results = [_evaluate_case(case) for case in cases]
    metrics = _metrics(cases, results)
    baseline_errors = (
        _check_baseline(metrics, DEFAULT_BASELINE_PATH) if check_baseline else []
    )
    failed_cases = [result for result in results if not result["passed"]]
    return {
        "registry_version": registry["version"],
        "offline": True,
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
