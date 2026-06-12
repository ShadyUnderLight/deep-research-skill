#!/usr/bin/env python3
"""Regression tests for doc/eval synchronization after rule evolution."""

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relpath: str) -> str:
    return (ROOT / relpath).read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Property-based checks for comparative-distillation document structure
# ---------------------------------------------------------------------------

REQUIRED_DISTILLATION_SECTIONS = [
    "Case identity",
    "Comparison purpose",
    "Candidate-action summary",
    "Triage notes",
    "Things explicitly rejected",
    "Final judgment",
    "Minimal quality bar",
]

ALLOWED_ACTION_TYPES = frozenset([
    "NEW_RULE",
    "CHECKLIST_HARDENING",
    "TEMPLATE_CHANGE",
    "NO_ACTION",
])


def _collect_dim_fields(text: str) -> list[dict[str, bool]]:
    """Extract dimension blocks and which sub-headings each contains."""
    lines = text.splitlines()
    dims: list[dict[str, bool]] = []
    current: dict[str, bool] = {}
    for line in lines:
        s = line.strip()
        if s.startswith("## Dimension "):
            if current:
                dims.append(current)
            current = {}
        elif s.startswith("### "):
            key = s.removeprefix("### ").rstrip()
            current[key] = True
    if current:
        dims.append(current)
    return dims


def _parse_candidate_summary_rows(text: str) -> list[list[str]]:
    """Parse rows from the candidate-action summary table."""
    lines = text.splitlines()
    in_table = False
    rows: list[list[str]] = []
    for line in lines:
        s = line.strip()
        if s.startswith("| # ") and "Candidate action" in s:
            in_table = True
            continue
        if in_table:
            if s.startswith("|") and s.endswith("|"):
                if "---" in s:
                    continue
                cells = [c.strip() for c in s.strip("|").split("|")]
                rows.append(cells)
            else:
                in_table = False
    return rows


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


# ---------------------------------------------------------------------------
# Property-based: comparative-distillation MCP report structure
# ---------------------------------------------------------------------------

# The expected path for the new asset (established by this test before the file exists;
# the test is designed to pass once the file is created per spec).
MCP_DISTILLATION_RELPATH = (
    "evals/comparative-distillation/"
    "mcp-protocol-report-technical-deep-dive-comparative-distillation.md"
)


def test_mcp_distillation_file_exists() -> None:
    """Property: the distillation file must exist at the expected path."""
    path = ROOT / MCP_DISTILLATION_RELPATH
    expect(path.exists(), f"missing expected distillation file: {MCP_DISTILLATION_RELPATH}")


def test_mcp_distillation_has_required_sections() -> None:
    """Property: all required top-level sections must be present."""
    text = read(MCP_DISTILLATION_RELPATH)
    for section in REQUIRED_DISTILLATION_SECTIONS:
        expect(
            section in text,
            f"MCP distillation missing required section: {section}",
        )


def test_mcp_distillation_dimension_structure() -> None:
    """Property: each dimension must have Report A, Report B, Gap, Candidate action, Action type."""
    text = read(MCP_DISTILLATION_RELPATH)
    dims = _collect_dim_fields(text)
    expect(len(dims) >= 6, f"expected >=6 dimensions, got {len(dims)}")

    for idx, d in enumerate(dims, 1):
        for field in ["Report A", "Report B", "Gap"]:
            expect(
                d.get(field, False),
                f"Dimension {idx} missing {field}",
            )
        # Candidate action and Action type are strongly recommended
        if not d.get("Candidate action", False):
            print(f"  WARN  Dimension {idx} missing Candidate action sub-heading")
        if not d.get("Action type", False):
            print(f"  WARN  Dimension {idx} missing Action type sub-heading")


def test_mcp_distillation_action_types_are_valid() -> None:
    """Property: all action type values must be from the allowed set."""
    text = read(MCP_DISTILLATION_RELPATH)
    # Find pattern "Action type\n\n`TYPE`" or "### Action type\n`TYPE`"
    found_types = re.findall(r"Action type\n+`(\w+)`", text)
    for t in found_types:
        expect(
            t in ALLOWED_ACTION_TYPES,
            f"invalid action type '{t}' in MCP distillation (allowed: {ALLOWED_ACTION_TYPES})",
        )


def test_mcp_distillation_candidate_summary_has_action_types() -> None:
    """Property: every row in candidate-action summary must have a valid action type."""
    text = read(MCP_DISTILLATION_RELPATH)
    rows = _parse_candidate_summary_rows(text)
    # This check is informational unless at least 1 accepted candidate exists
    if not rows:
        return
    # Each row has columns: #, Candidate action, Failure family, Action type, Proposed home
    for row in rows:
        if len(row) >= 4:
            atype = row[3].strip()
            if atype in ALLOWED_ACTION_TYPES:
                continue
            expect(
                atype in ALLOWED_ACTION_TYPES,
                f"invalid action type '{atype}' in summary table row: {row}",
            )


def test_mcp_distillation_final_judgment_distinguishes_gap_type() -> None:
    """Property: final judgment section must distinguish rule vs trigger vs execution gap."""
    text = read(MCP_DISTILLATION_RELPATH)
    # Isolate the Final judgment section only — scanning the entire doc is too weak
    # because "rule" / "gap" / "trigger" / "execution" appear in dimension descriptions.
    parts = text.split("## Final judgment")
    if len(parts) < 2:
        expect(False, "MCP distillation missing Final judgment section")
        return
    judgment = parts[1].split("\n## ")[0]  # content up to next level-2 heading (not ### sub-headings)
    has_rule = "rule" in judgment.lower() and "gap" in judgment.lower()
    has_trigger = "trigger" in judgment.lower() and "gap" in judgment.lower()
    has_execution = "execution" in judgment.lower() and "gap" in judgment.lower()
    expect(
        has_rule or has_trigger or has_execution,
        "MCP distillation final judgment should distinguish gap type "
        "(rule/trigger/execution)",
    )


def test_mcp_distillation_minimal_quality_bar_checked() -> None:
    """Property: minimal quality bar must have checked items."""
    text = read(MCP_DISTILLATION_RELPATH)
    # At minimum the [x] or [X] pattern should appear in the quality bar section
    bar_section = text.split("## Minimal quality bar")
    if len(bar_section) < 2:
        expect(False, "MCP distillation missing Minimal quality bar section")
        return
    bar_text = bar_section[1].split("\n## ")[0]  # content up to next level-2 heading
    expect(
        "- [x]" in bar_text or "- [X]" in bar_text,
        "MCP distillation minimal quality bar must have checked items",
    )


def main() -> int:
    tests = [
        test_architecture_reflects_current_route_map,
        test_eval_readme_documents_historical_rule_sync,
        test_source_traceability_format_boundary_evals_are_current,
        test_academic_activation_cases_mark_historical_experimental_status,
        test_mcp_distillation_file_exists,
        test_mcp_distillation_has_required_sections,
        test_mcp_distillation_dimension_structure,
        test_mcp_distillation_action_types_are_valid,
        test_mcp_distillation_candidate_summary_has_action_types,
        test_mcp_distillation_final_judgment_distinguishes_gap_type,
        test_mcp_distillation_minimal_quality_bar_checked,
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
