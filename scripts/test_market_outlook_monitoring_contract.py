#!/usr/bin/env python3
"""Regression tests for market-outlook monitoring signal actionability."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def assert_contains(path: str, needles: list[str]) -> None:
    text = read(path)
    missing = [needle for needle in needles if needle not in text]
    assert not missing, f"{path} missing: {', '.join(missing)}"


def test_market_outlook_checklist_defines_actionable_monitoring() -> None:
    assert_contains(
        "checklists/market-outlook-audit.md",
        [
            "Monitoring signal actionability hard-fail gate",
            "measurable threshold",
            "observation cadence",
            "data source",
            "trigger-to-action mapping",
            "at least 3 monitoring signals",
        ],
    )


def test_final_audit_recalls_actionable_monitoring() -> None:
    assert_contains(
        "checklists/final-audit.md",
        [
            "for market-outlook / industry-evolution tasks, monitoring signals are actionable",
            "threshold",
            "cadence",
            "source",
            "trigger-to-action",
        ],
    )


def test_decision_template_includes_monitoring_dashboard() -> None:
    assert_contains(
        "references/decision-report-template.md",
        [
            "| Monitoring signal | Current value | Threshold | Source | Review cadence | Triggered action |",
            "not just a reversal-condition list",
        ],
    )


def main() -> int:
    tests = [
        test_market_outlook_checklist_defines_actionable_monitoring,
        test_final_audit_recalls_actionable_monitoring,
        test_decision_template_includes_monitoring_dashboard,
    ]
    failures = []
    for test in tests:
        try:
            test()
            print(f"  PASS  {test.__name__}")
        except AssertionError as exc:
            print(f"  FAIL  {test.__name__}: {exc}")
            failures.append(test.__name__)

    if failures:
        print(f"\n{len(failures)} test(s) failed: {', '.join(failures)}")
        return 1

    print(f"\nAll {len(tests)} tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
