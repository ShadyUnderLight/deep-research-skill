#!/usr/bin/env python3
"""
Contract tests for Issue #353 Phase B: scenario shared-axis, rule-system
declared-not-executed, and target-gate integration.

Phase A (PR #354) added three eval cases, INDEX rows, and ROUTING-MATRIX
sports-prediction trigger.  Phase B adds contract-level tests that verify:

  B1: Market-outlook scenario shared-axis rule is testable —
      the checklist defines it, the reference documents it, and the
      eval case records axis-drift as a failure pattern.

  B2: Regulatory rule-system add-on declared-not-executed is testable —
      the checklist requires state taxonomy + intervention matrix, the
      add-on reference defines templates, and the eval case records
      declared-not-executed as a failure pattern.

  B3: Target-gate integration — the eval cases have full Route/Audit
      and Source Register structure but still fail on target-specific
      gates, not just generic missing-block failures.

Usage:
    python tests/test_issue_353_phase_b_contracts.py
    python -m pytest tests/test_issue_353_phase_b_contracts.py -v

Expected state: ALL PASS (checklists + eval cases already contain the
required content — these tests assert the current contract state).

Related:
    * Issue #353 (Phase A + B)
    * Issue #355 (Phase B tracking)
    * PR #354 (Phase A implementation)
"""

from __future__ import annotations

import os
import re
import subprocess
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ═══════════════════════════════════════════════════════════════════════════
# Shared helpers
# ═══════════════════════════════════════════════════════════════════════════


def read(path: str) -> str:
    with open(os.path.join(REPO_ROOT, path), "r", encoding="utf-8") as f:
        return f.read()


def file_exists(path: str) -> bool:
    return os.path.exists(os.path.join(REPO_ROOT, path))


def text_contains_any(text: str, keywords: list[str]) -> bool:
    """Return True if at least one keyword appears (case-insensitive)."""
    return any(kw.lower() in text.lower() for kw in keywords)


def section_text(text: str, heading_pattern: str) -> str | None:
    """Extract text under a ## or ### heading matching heading_pattern.

    Returns the section body (excluding heading line), or None if not found.

    NOTE: heading_pattern is wrapped in (?:...) for proper | alternation
    grouping, so callers can pass patterns like ``"Failure signs|Failure"``
    without unintended captures.
    """
    pat = re.compile(
        r"^#{2,3}\s+.*(?:"
        + heading_pattern
        + r").*$",
        re.MULTILINE | re.IGNORECASE,
    )
    m = pat.search(text)
    if not m:
        return None
    start = m.end()  # Start after the heading line
    # End at next heading of same or higher level (## or ###).
    # Use #{2,3} (not #{1,3}) to avoid matching level-1 (#) titles
    # that may appear between sections.
    remaining = text[start:]
    end_match = re.search(r"^#{2,3}\s+", remaining, re.MULTILINE)
    if end_match:
        return remaining[: end_match.start()].strip()
    return remaining.strip()


# ═══════════════════════════════════════════════════════════════════════════
# B1: Market-outlook scenario shared-axis
# ═══════════════════════════════════════════════════════════════════════════

MARKET_OUTLOOK_CHECKLIST = "checklists/market-outlook-audit.md"
SPORTS_BROADCASTING_EVAL = (
    "evals/cases/world-cup-sports-broadcasting-market-outlook-source-and-monitoring-case.md"
)
MARKET_OUTLOOK_REFERENCE = "references/market-outlook-and-scenario-discipline.md"


class TestMarketOutlookScenarioSharedAxis:
    """B1: Contract tests for scenario shared-axis / axis-drift."""

    # ── Checklist level ──────────────────────────────────────────────

    def test_checklist_has_shared_axis_rule(self) -> None:
        """market-outlook-audit.md §Structured multi-scenario: shared-axis rule exists."""
        content = read(MARKET_OUTLOOK_CHECKLIST)
        sec = section_text(content, "Structured multi-scenario")
        assert sec is not None, (
            "Missing §Structured multi-scenario section in market-outlook checklist"
        )
        # The rule must mention "same load-bearing metric" + "axis" + "no mixing"
        assert re.search(
            r"same\s+load-bearing\s+metric", sec, re.IGNORECASE
        ), "Missing 'same load-bearing metric' constraint in §Structured multi-scenario"
        assert text_contains_any(sec, [
            "quantitative axis",
            "定量主轴",
            "定量轴",
        ]), "Missing 'quantitative axis' reference in §Structured multi-scenario"
        assert text_contains_any(sec, [
            "no mixing different metrics",
            "no mixing different",
            "不混合",
            "不同指标",
        ]), "Missing 'no mixing different metrics' constraint"

    # ── Reference level ──────────────────────────────────────────────

    def test_reference_documents_scenario_axis_discipline(self) -> None:
        """market-outlook-and-scenario-discipline.md references shared-axis constraint."""
        content = read(MARKET_OUTLOOK_REFERENCE)
        # The reference should mention scenario axis discipline
        assert text_contains_any(content, [
            "load-bearing",
            "shared axis",
            "scenario axis",
            "comparable axis",
            "统一比较",
            "common metric",
        ]), (
            "market-outlook-and-scenario-discipline.md lacks shared-axis / "
            "load-bearing variable discipline reference"
        )

    # ── Eval case level ──────────────────────────────────────────────

    def test_eval_documents_axis_drift_failure(self) -> None:
        """Sports broadcasting eval case records axis drift as a failure sign."""
        assert file_exists(SPORTS_BROADCASTING_EVAL), (
            f"Missing eval case: {SPORTS_BROADCASTING_EVAL}"
        )
        content = read(SPORTS_BROADCASTING_EVAL)
        # The failure signs or pass criteria must mention axis drift
        axis_drift_indicators = [
            "scenarios drift across different metrics",
            "scenarios not bound",
            "not bound to a shared quantitative",
            "not bound to shared",
            "shared quantitative axis",
            "not comparable because they lack a common",
            "drift across different",
            "unanchored",
        ]
        assert any(
            re.search(pat, content, re.IGNORECASE)
            for pat in axis_drift_indicators
        ), (
            "Sports broadcasting eval case does not document scenario "
            "axis drift as a failure pattern. "
            f"Checked patterns: {axis_drift_indicators}"
        )

    def test_eval_current_rule_status_includes_axis_warning(self) -> None:
        """Sports broadcasting eval case's Current rule verdict flags axis drift."""
        content = read(SPORTS_BROADCASTING_EVAL)
        sec = section_text(content, "Current rule verdict|Current rule")
        assert sec is not None, "Missing Current rule verdict section"
        # Must have a warn/fail about scenarios/axis
        assert text_contains_any(sec, [
            "axis",
            "scenario",
            "shared",
            "load-bearing",
        ]), "Current rule verdict does not reference scenario/axis issues"


# ═══════════════════════════════════════════════════════════════════════════
# B2: Regulatory / rule-system declared-not-executed
# ═══════════════════════════════════════════════════════════════════════════

REGULATORY_CHECKLIST = "checklists/regulatory-analysis-audit.md"
ADDON_REFERENCE = "references/rule-system-and-mechanism-add-on.md"
EXPANSION_EVAL = (
    "evals/cases/world-cup-expansion-regulatory-contract-and-source-fail-case.md"
)
RULE_SYSTEM_EVAL = "evals/cases/rule-system-add-on-activation-case.md"


class TestDeclaredNotExecutedForRuleSystem:
    """B2: Contract tests for rule-system add-on declared-not-executed."""

    # ── Checklist level ──────────────────────────────────────────────

    def test_checklist_has_state_taxonomy_check(self) -> None:
        """regulatory-analysis-audit.md §Rule-system analysis includes state taxonomy check."""
        content = read(REGULATORY_CHECKLIST)
        sec = section_text(content, "Rule.system|规则系统")
        assert sec is not None, (
            "Missing §Rule-system analysis section in regulatory checklist"
        )
        assert text_contains_any(sec, [
            "state taxonomy",
            "状态分类",
            "state classification",
            "participant states",
        ]), (
            "Missing state taxonomy check in §Rule-system analysis"
        )

    def test_checklist_has_intervention_matrix_check(self) -> None:
        """regulatory-analysis-audit.md §Rule-system includes intervention matrix check."""
        content = read(REGULATORY_CHECKLIST)
        sec = section_text(content, "Rule.system|规则系统")
        assert sec is not None, "Missing §Rule-system section"
        assert text_contains_any(sec, [
            "intervention matrix",
            "干预矩阵",
            "intervention",
            "rule adjustment",
            "规则调整",
        ]), "Missing intervention matrix check in §Rule-system analysis"

    def test_checklist_has_declared_not_executed_gate(self) -> None:
        """regulatory-analysis-audit.md §Rule-system analysis has actionable
        items + §Final sign-off requiring all checked — catches declared-not-executed
        structurally (checklist items unchecked = add-on not executed)."""
        content = read(REGULATORY_CHECKLIST)
        # The rule-system section must have actionable checklist items
        # for state taxonomy and intervention matrix (the items that a
        # declared-but-not-executed report would leave unchecked).
        rs_sec = section_text(content, "Rule.system|规则系统")
        assert rs_sec is not None, (
            "Missing §Rule-system analysis section — needed for "
            "declared-not-executed gate"
        )
        # Must have at least 3 checklist items
        checkbox_count = len(re.findall(r"- \[ \]", rs_sec))
        assert checkbox_count >= 3, (
            f"§Rule-system analysis has only {checkbox_count} checklist "
            f"items, expected >=3 to serve as declared-not-executed gate"
        )
        # §Final sign-off must require checking all items
        assert text_contains_any(content, [
            "all items above are checked",
            "全部",
            "above are checked",
        ]), "§Final sign-off must require all checklist items are checked"

    # ── Add-on reference level ──────────────────────────────────────

    def test_addon_documents_state_taxonomy(self) -> None:
        """rule-system-and-mechanism-add-on.md documents state taxonomy template."""
        assert file_exists(ADDON_REFERENCE), f"Missing: {ADDON_REFERENCE}"
        content = read(ADDON_REFERENCE)
        assert text_contains_any(content, [
            "state taxonomy",
            "状态分类",
            "State taxonomy",
        ]), "Add-on reference missing state taxonomy section"
        # Must contain a template or definition, not just a header
        sec = section_text(content, "state taxonomy|状态分类")
        if sec:
            # The section should have substantive content (template, columns, or description)
            assert len(sec.strip()) > 100, (
                "State taxonomy section appears empty or underspecified"
            )

    def test_addon_documents_intervention_matrix(self) -> None:
        """rule-system-and-mechanism-add-on.md documents intervention matrix template."""
        content = read(ADDON_REFERENCE)
        matrix_sec = section_text(content, "Intervention matrix|干预矩阵")
        assert matrix_sec is not None, (
            "Add-on reference missing intervention matrix section"
        )
        # The section must contain a markdown table (pipe-separated rows
        # with delimiter line) — not just section prose.
        has_table = bool(
            re.search(r"\|.*\|.*\n\|[-| :]+\|", matrix_sec)
        )
        assert has_table, (
            "Add-on reference intervention matrix section must include "
            "a markdown table template"
        )

    # ── Eval case level ──────────────────────────────────────────────

    def test_eval_documents_declared_not_executed_failure(self) -> None:
        """Expansion eval case records add-on declared-not-executed as failure."""
        assert file_exists(EXPANSION_EVAL), f"Missing: {EXPANSION_EVAL}"
        content = read(EXPANSION_EVAL)
        assert text_contains_any(content, [
            "declared but not executed",
            "declared-not-executed",
            "declared not executed",
            "add-on declared",
            "add.on declared",
            "declared.*add.on",
        ]), (
            "World Cup expansion eval case does not document "
            "declared-not-executed failure pattern"
        )

    def test_eval_verdict_includes_add_on_gaps(self) -> None:
        """Expansion eval case Current rule verdict flags add-on not executed."""
        content = read(EXPANSION_EVAL)
        sec = section_text(content, "Current rule verdict|Current rule")
        assert sec is not None, "Missing Current rule verdict section"
        # Verdict must mention add-on, state taxonomy, or intervention matrix
        assert text_contains_any(sec, [
            "add-on",
            "state taxonomy",
            "intervention matrix",
            "状态分类",
            "干预矩阵",
            "add.on",
            "not executed",
        ]), "Current rule verdict does not reference add-on execution gaps"

    def test_rule_system_activation_eval_requires_add_on_blocks(self) -> None:
        """Rule-system add-on activation eval verifies state taxonomy + intervention matrix."""
        assert file_exists(RULE_SYSTEM_EVAL), f"Missing: {RULE_SYSTEM_EVAL}"
        content = read(RULE_SYSTEM_EVAL)
        # Pass criteria / failure signs must reference both blocks
        assert text_contains_any(content, [
            "state taxonomy",
            "状态分类",
        ]), "Rule-system activation eval missing state taxonomy reference"
        assert text_contains_any(content, [
            "intervention matrix",
            "干预矩阵",
        ]), "Rule-system activation eval missing intervention matrix reference"


# ═══════════════════════════════════════════════════════════════════════════
# B3: Target-gate integration — not just generic blocks
# ═══════════════════════════════════════════════════════════════════════════


class TestTargetGateIntegrationNotGeneric:
    """B3: Verify eval cases have full structure but fail on target gates."""

    # ── Sports broadcasting eval (market-outlook) ────────────────────

    def test_eval_has_route_and_source_structure(self) -> None:
        """Sports broadcasting eval case has Route/Audit Status + Source Register."""
        content = read(SPORTS_BROADCASTING_EVAL)
        # Must document Route (market-outlook) and Source traceability expectations
        route_indicators = [
            "market-outlook",
            "market outlook",
        ]
        source_indicators = [
            "Source Register",
            "source register",
            "source-traceability",
            "source traceability",
            "[Sxx]",
        ]
        assert any(
            r in content for r in route_indicators
        ), f"Eval case missing route structure. Checked: {route_indicators}"
        assert any(
            r in content for r in source_indicators
        ), f"Eval case missing source structure. Checked: {source_indicators}"

    def test_eval_fails_on_target_not_generic(self) -> None:
        """Eval case failure signs are NOT just generic 'Missing Route/Missing Register'."""
        content = read(SPORTS_BROADCASTING_EVAL)
        sec = section_text(content, "Failure signs|Failure")
        assert sec is not None, "Missing Failure signs section"

        generic_patterns = [
            r"Missing\s+Route\s+and\s+audit\s+status",
            r"Missing\s+Source\s+Register",
            r"no\s+\[Sxx\]",
            r"missing\s+monitoring\s+section",
        ]
        target_patterns = [
            r"source.?strength",
            r"monitoring",
            r"actionability",
            r"scenario",
            r"axis",
            r"shared",
            r"label.?source",
            r"evidence.?label",
            r"forward.?looking",
            r"self.?assessment",
            r"overclaim",
        ]

        generic_matches = sum(
            1 for pat in generic_patterns if re.search(pat, sec, re.IGNORECASE)
        )
        target_specific_matches = sum(
            1 for pat in target_patterns if re.search(pat, sec, re.IGNORECASE)
        )

        assert target_specific_matches >= 2, (
            f"Failure signs section has only {target_specific_matches} target-specific "
            f"patterns (needs >=2). The eval may depend on generic failures: "
            f"found {generic_matches} generic patterns."
        )

    # ── Expansion eval (regulatory) ─────────────────────────────────

    def test_second_eval_has_route_and_source_structure(self) -> None:
        """Expansion eval case has Route/Audit Status + Source Register structure."""
        content = read(EXPANSION_EVAL)
        route_indicators = [
            "regulatory",
            "regulatory-analysis",
        ]
        source_indicators = [
            "Source Register",
            "source register",
            "source-traceability",
            "source traceability",
            "[Sxx]",
        ]
        assert any(
            r in content for r in route_indicators
        ), f"Expansion eval missing route structure. Checked: {route_indicators}"
        assert any(
            r in content for r in source_indicators
        ), f"Expansion eval missing source structure. Checked: {source_indicators}"

    def test_second_eval_fails_on_target_not_generic(self) -> None:
        """Expansion eval case failure signs target add-on + regulatory contract, not just generic."""
        content = read(EXPANSION_EVAL)
        sec = section_text(content, "Failure signs|Failure")
        assert sec is not None, "Missing Failure signs section"

        generic_patterns = [
            r"Missing\s+Route\s+and\s+audit\s+status",
            r"Missing\s+Source\s+Register",
            r"no\s+\[Sxx\]",
        ]
        target_patterns = [
            r"regulatory.*contract",
            r"rule.?system",
            r"add.?on",
            r"state.?taxonomy",
            r"intervention.?matrix",
            r"declared",
            r"not.*executed",
            r"source.?strength",
            r"self.?assessment",
            r"overclaim",
            r"process.?integrity",
        ]

        generic_matches = sum(
            1 for pat in generic_patterns if re.search(pat, sec, re.IGNORECASE)
        )
        target_matches = sum(
            1 for pat in target_patterns if re.search(pat, sec, re.IGNORECASE)
        )

        assert target_matches >= 3, (
            f"Expansion eval failure signs section has only {target_matches} "
            f"target-specific patterns (needs >=3). "
            f"Generic matches: {generic_matches}"
        )


# ═══════════════════════════════════════════════════════════════════════════
# Regression: existing tests must still pass
# ═══════════════════════════════════════════════════════════════════════════


class TestPhaseBRegression:
    """Regression: existing Phase A + all-contracts tests remain green."""

    def test_phase_a_contracts_still_pass(self) -> None:
        """test_issue_353_contracts.py (Phase A) must still pass."""
        result = subprocess.run(
            [sys.executable, "tests/test_issue_353_contracts.py"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert result.returncode == 0, (
            f"Phase A contract tests failed:\n"
            f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )

    def test_eval_index_regression_passes(self) -> None:
        """scripts/test_eval_index.py must still pass (eval index integrity)."""
        result = subprocess.run(
            [sys.executable, "scripts/test_eval_index.py"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert result.returncode == 0, (
            f"test_eval_index.py failed:\n"
            f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )


# ═══════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════

ALL_TESTS: list[tuple[str, type]] = [
    ("B1: Market-outlook scenario shared-axis", TestMarketOutlookScenarioSharedAxis),
    ("B2: Rule-system declared-not-executed", TestDeclaredNotExecutedForRuleSystem),
    ("B3: Target-gate integration", TestTargetGateIntegrationNotGeneric),
    ("Regression", TestPhaseBRegression),
]


def _run_test_method(test_case: type, method_name: str) -> str | None:
    """Run a single test method. Returns error message on failure, None on pass."""
    try:
        getattr(test_case(), method_name)()
        return None
    except (AssertionError, Exception) as exc:
        return str(exc)


def main() -> int:
    total = 0
    passed = 0
    failures: list[str] = []

    print("=" * 70)
    print("Issue #353 Phase B — Contract Tests")
    print("=" * 70)

    for group_name, test_class in ALL_TESTS:
        print(f"\n── {group_name} ──")
        methods = [
            m for m in dir(test_class)
            if m.startswith("test_") and callable(getattr(test_class, m))
        ]
        for method_name in methods:
            total += 1
            err = _run_test_method(test_class, method_name)
            if err is None:
                print(f"  PASS  {method_name}")
                passed += 1
            else:
                print(f"  FAIL  {method_name}: {err}")
                failures.append(f"{group_name} > {method_name}: {err}")

    print(f"\n{'=' * 70}")
    print(f"Results: {passed}/{total} passed", end="")
    if failures:
        print(f", {len(failures)} failure(s)")
        print("\nFAILURES:")
        for f in failures:
            print(f"  - {f}")
    else:
        print(" — ALL PASS")

    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
