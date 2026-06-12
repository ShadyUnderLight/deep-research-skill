#!/usr/bin/env python3
"""Contract test for benchmark comparability disclosure discipline on the equipment-selection route."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def assert_contains(path: str, needles: list[str]) -> None:
    text = read(path)
    missing = [needle for needle in needles if needle not in text]
    assert not missing, f"{path} missing: {', '.join(missing)}"


def test_routing_matrix_benchmark_disclosure() -> None:
    assert_contains(
        "ROUTING-MATRIX.md",
        [
            "benchmark performance numbers",
            "metric type",
            "backend",
            # Second hard-fail condition — unique needle
            "single-stream desktop tok/s",
        ],
    )


def test_routing_matrix_attach_section() -> None:
    """Verify the Attach section explicitly includes benchmark numbers."""
    assert_contains(
        "ROUTING-MATRIX.md",
        [
            "scoring, or benchmark performance numbers materially affect",
        ],
    )


def test_final_audit_recalls_benchmark_disclosure() -> None:
    assert_contains(
        "checklists/final-audit.md",
        [
            "benchmark performance numbers",
            "quantization",
            "context",
            "backend",
            # Second half of the rule — unique needle
            "single-stream desktop tok/s",
        ],
    )


def test_quantitative_role_includes_equipment_selection() -> None:
    assert_contains(
        "references/quantitative-role-labeling.md",
        [
            "Equipment selection / procurement / home-server-planning",
            "epistemic role",
            "comparability note",
        ],
    )


def main() -> int:
    tests = [
        test_routing_matrix_benchmark_disclosure,
        test_routing_matrix_attach_section,
        test_final_audit_recalls_benchmark_disclosure,
        test_quantitative_role_includes_equipment_selection,
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
