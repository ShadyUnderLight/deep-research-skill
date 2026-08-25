#!/usr/bin/env python3
"""Validate claim–source alignment bundles and emit structured verdicts (issue #419).

Usage:
    python3 scripts/validate_claim_alignment.py <bundle.json> [--json]
    python3 scripts/validate_claim_alignment.py --calibrate <bundle.json> <gold.json>

Exit codes:
    0 = alignment pass (or calibration meets threshold)
    1 = conditional pass / calibration below threshold
    2 = structural failure or blocking alignment errors
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from claim_alignment import (
    VALIDATOR_VERSION,
    load_and_run_bundle,
    report_to_dict,
    run_calibration,
)


def validate_bundle(path: Path, *, json_output: bool = False) -> int:
    report = load_and_run_bundle(path)
    payload = report_to_dict(report)
    payload["validator_version"] = VALIDATOR_VERSION
    if json_output:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"bundle_id: {report.bundle_id}")
        print(f"aggregate_verdict: {report.aggregate_verdict}")
        print(f"counts: {report.counts}")
        if report.structural_errors:
            print("structural_errors:")
            for err in report.structural_errors:
                print(f"  - {err}")
        for judgment in report.judgments:
            print(f"  {judgment.claim_id}: {judgment.verdict}")
            for err in judgment.errors:
                print(f"    error: {err}")

    if report.structural_errors or report.blocking_errors:
        return 2
    if report.aggregate_verdict in {"fail"}:
        return 2
    if report.aggregate_verdict == "conditional-pass":
        return 1
    if report.aggregate_verdict == "not_run":
        return 1
    return 0


def calibrate(bundle_path: Path, gold_path: Path, threshold: float, json_output: bool) -> int:
    try:
        result = run_calibration(bundle_path, gold_path, threshold=threshold)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    payload = {
        "fixture_version": result.fixture_version,
        "threshold": result.threshold,
        "aggregate_accuracy": result.aggregate_accuracy,
        "positive_samples": result.positive_samples,
        "negative_samples": result.negative_samples,
        "per_class": result.per_class,
        "mismatches": result.mismatches,
        "validator_version": VALIDATOR_VERSION,
    }
    if json_output:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"fixture_version: {result.fixture_version}")
        print(f"aggregate_accuracy: {result.aggregate_accuracy:.4f}")
        print(f"threshold: {result.threshold}")
        print(f"positive_samples: {result.positive_samples}")
        print(f"negative_samples: {result.negative_samples}")
        for verdict, bucket in sorted(result.per_class.items()):
            print(
                f"  {verdict}: support={bucket['support']} "
                f"fnr={bucket.get('fnr', 0):.3f} fpr={bucket.get('fpr', 0):.3f}"
            )
        if result.mismatches:
            print("mismatches:")
            for line in result.mismatches:
                print(f"  - {line}")

    if result.mismatches and result.aggregate_accuracy < threshold:
        return 2
    if result.aggregate_accuracy < threshold:
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Claim–source alignment validator")
    parser.add_argument("bundle", type=str, help="Path to alignment bundle JSON")
    parser.add_argument(
        "--calibrate",
        type=str,
        default=None,
        metavar="GOLD",
        help="Run calibration against an isolated gold-key JSON file",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.85,
        help="Minimum aggregate accuracy for calibration pass (default 0.85)",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON on stdout")
    args = parser.parse_args(argv)

    bundle_path = Path(args.bundle)
    if not bundle_path.is_file():
        print(f"{bundle_path}: not a regular file", file=sys.stderr)
        return 2

    if args.calibrate:
        gold_path = Path(args.calibrate)
        if not gold_path.is_file():
            print(f"{gold_path}: not a regular file", file=sys.stderr)
            return 2
        return calibrate(bundle_path, gold_path, args.threshold, args.json)

    return validate_bundle(bundle_path, json_output=args.json)


if __name__ == "__main__":
    raise SystemExit(main())
