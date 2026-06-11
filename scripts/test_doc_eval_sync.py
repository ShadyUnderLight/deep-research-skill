#!/usr/bin/env python3
"""Regression tests for doc/eval synchronization after rule evolution."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relpath: str) -> str:
    return (ROOT / relpath).read_text(encoding="utf-8")


def expect(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def test_architecture_reflects_current_route_map() -> None:
    text = read("ARCHITECTURE.md")

    expect(
        "academic / literature review (⚠️ experimental)" not in text,
        "ARCHITECTURE.md still marks academic route as experimental",
    )
    expect(
        "academic / literature review" in text and "hardened" in text,
        "ARCHITECTURE.md should describe academic route as hardened/current",
    )
    expect(
        "a dedicated system-map file for failure families and intervention points" not in text,
        "ARCHITECTURE.md still says the dedicated system-map file is missing",
    )
    expect(
        "\nDo not default to expanding `SKILL.md` unless the change truly belongs to the workflow spine.\nto the workflow spine." not in text,
        "ARCHITECTURE.md still contains the duplicate trailing fragment",
    )


def test_eval_readme_documents_historical_rule_sync() -> None:
    text = read("evals/README.md")

    for phrase in [
        "Historical verdict",
        "Current rule verdict",
        "Current eval target",
    ]:
        expect(
            phrase in text,
            f"evals/README.md should document the {phrase} field for historical evals",
        )


def test_source_traceability_format_boundary_evals_are_current() -> None:
    cases = [
        "evals/cases/ai-traffic-police-technical-deep-dive-traceability-case.md",
        "evals/cases/pop-mart-listed-company-traceability-hard-fail-case.md",
        "evals/cases/fertility-academic-literature-review-format-boundary-case.md",
    ]

    stale_phrases = [
        "appendix source list exists but zero [SN] inline citations in body = undeliverable",
        "source register exists but zero [SN] inline citations in body = undeliverable",
        "Per `checklists/source-traceability.md`, this is a hard-fail",
        "Yet it triggers the project's source-traceability hard-fail because it doesn't use `[SN]` numbering",
    ]

    for case in cases:
        text = read(case)
        for phrase in ["Historical verdict", "Current rule verdict", "Current eval target"]:
            expect(phrase in text, f"{case} should explicitly distinguish {phrase}")
        for phrase in stale_phrases:
            expect(phrase not in text, f"{case} still contains stale rule text: {phrase}")


def test_academic_activation_cases_mark_historical_experimental_status() -> None:
    cases = [
        "evals/cases/academic-route-activation-transformer-origin-case.md",
        "evals/cases/academic-route-activation-crispr-progress-case.md",
        "evals/cases/academic-route-activation-llm-hallucination-comparison-case.md",
    ]

    for case in cases:
        text = read(case)
        expect(
            "Current route status: hardened" in text,
            f"{case} should state the current academic route status",
        )
        expect(
            "Adequate for experimental stage" not in text,
            f"{case} still describes the current route definition as experimental",
        )


def main() -> int:
    tests = [
        test_architecture_reflects_current_route_map,
        test_eval_readme_documents_historical_rule_sync,
        test_source_traceability_format_boundary_evals_are_current,
        test_academic_activation_cases_mark_historical_experimental_status,
    ]
    failures = []
    for test in tests:
        try:
            test()
            print(f"  PASS  {test.__name__}")
        except AssertionError as exc:
            failures.append(test.__name__)
            print(f"  FAIL  {test.__name__}: {exc}")

    if failures:
        print(f"\n{len(failures)} test(s) failed: {', '.join(failures)}")
        return 1

    print(f"\nAll {len(tests)} tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
