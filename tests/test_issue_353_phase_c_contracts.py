#!/usr/bin/env python3
"""
Contract tests for Issue #353 Phase C: comparative distillation artifacts,
sports prediction current-state gate, and sports source-strength regression.

Phase A (PR #354) — ROUTING-MATRIX sports trigger + 3 eval cases + INDEX rows.
Phase B (PR #356) — market-outlook scenario shared-axis, regulatory rule-system
                    declared-not-executed, target-gate integration.
Phase C (this file) — closes the #353 loop:

  C1: Three comparative-distillation artifacts exist at the specified paths.
  C2: Each artifact contains action-type classifications
      (NEW_RULE / CHECKLIST_HARDENING / TEMPLATE_CHANGE / NO_ACTION).
  C3: checklists/option-selection-final-audit.md has a sports prediction
      current-state gate defining 6 required inputs.
  C4: The sports prediction gate includes downgrade rules for missing
      inputs and requires probability-table role labels.
  C5: Sports/World Cup source-strength fixtures hit existing #341
      validator functions, proving the gate works in sports contexts.

Usage:
    python tests/test_issue_353_phase_c_contracts.py
    python -m pytest tests/test_issue_353_phase_c_contracts.py -v

Expected BEFORE implementation: C1–C4 FAIL, C5 PASS (functions already exist)
Expected AFTER implementation:  ALL PASS
"""

from __future__ import annotations

import os
import re
import sys
import textwrap

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ═══════════════════════════════════════════════════════════════════════════════
# Shared helpers
# ═══════════════════════════════════════════════════════════════════════════════


def read(path: str) -> str:
    with open(os.path.join(REPO_ROOT, path), "r", encoding="utf-8") as f:
        return f.read()


def file_exists(path: str) -> bool:
    return os.path.exists(os.path.join(REPO_ROOT, path))


def text_contains_any(text: str, keywords: list[str], case_sensitive: bool = False) -> bool:
    if case_sensitive:
        return any(kw in text for kw in keywords)
    t_lower = text.lower()
    return any(kw.lower() in t_lower for kw in keywords)


# ═══════════════════════════════════════════════════════════════════════════════
# C1: Three comparative-distillation artifacts exist
# ═══════════════════════════════════════════════════════════════════════════════

_DISTILLATION_DIR = "evals/comparative-distillation"

DISTILLATION_ARTIFACTS = [
    f"{_DISTILLATION_DIR}/world-cup-expansion-gpt-vs-local-comparative-distillation.md",
    f"{_DISTILLATION_DIR}/world-cup-sports-broadcasting-gpt-vs-local-comparative-distillation.md",
    f"{_DISTILLATION_DIR}/argentina-cape-verde-gpt-vs-local-comparative-distillation.md",
]

_ACTION_TYPES = [
    "NEW_RULE",
    "CHECKLIST_HARDENING",
    "TEMPLATE_CHANGE",
    "VALIDATOR_OR_TEST",
    "NO_ACTION",
]


def _count_action_types(content: str) -> int:
    """Count distinct action-type labels present in the artifact."""
    found = set()
    for at in _ACTION_TYPES:
        # Match as a code-like token (backtick or plain) in context
        if re.search(rf"(?:`?){re.escape(at)}(?:`?)", content):
            found.add(at)
    return len(found)


# ═══════════════════════════════════════════════════════════════════════════════
# C3/C4: Sports prediction gate in option-selection-final-audit.md
# ═══════════════════════════════════════════════════════════════════════════════

OPTION_SELECTION_CHECKLIST = "checklists/option-selection-final-audit.md"

# The 6 required inputs for the sports prediction gate.
_SPORTS_GATE_INPUT_KEYWORDS = [
    "market odds",
    "赔率",
    "odds",
    "injury",
    "伤停",
    "suspension",
    "lineup",
    "首发",
    "rotation",
    "weather",
    "天气",
    "venue",
    "recent match data",
    "近期",
    "form",
    "tactical",
    "战术",
    "statistical",
    "xG",
]

# Downgrade / role-label keywords.
_GATE_DOWNGRADE_KEYWORDS = [
    "downgrade",
    "降级",
    "qualitative scenario",
    "定性",
    "directional probability band",
    "probability band",
    "role",
    "observed",
    "market-implied",
    "proxy",
    "assumption",
    "model-output",
    "model output",
    "worked example",
    "示例",
]


def _section_after_heading(text: str, heading_pattern: str) -> str | None:
    """Return text after a ## (level-2) heading matching heading_pattern.

    Only stops at the next ## heading (NOT ###) so that the extracted
    section includes all ### subheadings and their content.
    """
    pat = re.compile(
        r"^##\s+.*(?:" + heading_pattern + r").*$",
        re.MULTILINE | re.IGNORECASE,
    )
    m = pat.search(text)
    if not m:
        return None
    start = m.end()
    remaining = text[start:]
    # Only match ## (not ###) as the next section boundary
    end_match = re.search(r"^##\s+(?!#)", remaining, re.MULTILINE)
    if end_match:
        return remaining[: end_match.start()].strip()
    return remaining.strip()


# ═══════════════════════════════════════════════════════════════════════════════
# C5: Sports source-strength fixtures — World Cup / sports themed markdown
# that exercises the existing #341 validator functions.
# ═══════════════════════════════════════════════════════════════════════════════

_SPORTS_FIXTURE_BASE = textwrap.dedent("""\
    # World Cup Match Prediction: Argentina vs France

    Based on recent form and head-to-head record [S01][S02][S03][S04].

    ## Route and audit status

    **Primary route:** Constrained Choice / Option Selection

    | Audit | Status | 证据 |
    |-------|--------|------|
    | source-traceability | ✅ Passed | §Analysis: body has [S01]-[S04] |

    ## Source Register

""")


def _sports_register_rows(
    rows: list[tuple[str, str, str, str]],
) -> str:
    """Build full sports fixture from register rows.
    Each row: (id, source_name, source_type, reliability)
    claims_supported defaults to section-only §1 to test detection.
    """
    header = (
        "| ID | Source Name | Source Type | Date | DOI/URL "
        "| Reliability | Claims Supported |\n"
        "|----|-------------|-------------|------|--------"
        "|-------------|-----------------|\n"
    )
    body_rows = []
    for i, (sid, name, stype, rel) in enumerate(rows):
        body_rows.append(
            f"| {sid} | {name} | {stype} | 2026-06-01 | https://example.com/{i} "
            f"| {rel} | §1 |"
        )
    return _SPORTS_FIXTURE_BASE + header + "\n".join(body_rows) + "\n"


def _sports_fixture_wiki_100pct() -> str:
    """100% Wikipedia/CROWDSOURCED sources with body references — should fail."""
    return _sports_register_rows([
        ("S01", "Wikipedia: FIFA World Cup history", "CROWDSOURCED", "high"),
        ("S02", "Wikipedia: Argentina national team", "Wikipedia", "high"),
        ("S03", "Wikipedia: France national team", "CROWDSOURCED", "high"),
        ("S04", "Wikipedia: Match statistics", "wiki", "high"),
    ])


def _sports_fixture_crowdsourced_high() -> str:
    """CROWDSOURCED source with high reliability — should fail."""
    return _sports_register_rows([
        ("S01", "Wikipedia: World Cup data", "CROWDSOURCED", "high"),
        ("S02", "FIFA Official Match Report", "PRIMARY_INSTITUTION", "high"),
    ])


def _sports_fixture_section_only_claims() -> str:
    """All Claims Supported are pure section numbers — should fail."""
    header = (
        "| ID | Source Name | Source Type | Date | DOI/URL "
        "| Reliability | Claims Supported |\n"
        "|----|-------------|-------------|------|--------"
        "|-------------|-----------------|\n"
    )
    rows = [
        "| S01 | FIFA Stats | PRIMARY_INSTITUTION | 2026-06-01 | https://x.com/1 | high | §1.1, §2.1 |",
        "| S02 | UEFA Analysis | SECONDARY_MEDIA | 2026-06-01 | https://x.com/2 | medium | §3.1 |",
        "| S03 | Opta Data | PRIMARY_FILING | 2026-06-01 | https://x.com/3 | high | §4.1, §4.2 |",
    ]
    return _SPORTS_FIXTURE_BASE + header + "\n".join(rows) + "\n"


def _sports_fixture_confirmed_label_mismatch() -> str:
    """CROWDSOURCED source referenced with [确认事实] label — should fail."""
    body = textwrap.dedent("""\
        # World Cup Match Prediction

        Argentina is the favorite [确认事实][S01].

        ## Route and audit status

        | Audit | Status | 证据 |
        |-------|--------|------|
        | source-traceability | ✅ Passed | §1 |

        ## Source Register

    """)
    header = (
        "| ID | Source Name | Source Type | Date | DOI/URL "
        "| Reliability | Claims Supported |\n"
        "|----|-------------|-------------|------|--------"
        "|-------------|-----------------|\n"
    )
    rows = [
        "| S01 | Wikipedia: Argentina squad | CROWDSOURCED | 2026-06-01 | https://x.com/1 | high | §1 |",
    ]
    return body + header + "\n".join(rows) + "\n"


# ═══════════════════════════════════════════════════════════════════════════════
# Tests: C1 — Distillation artifacts exist
# ═══════════════════════════════════════════════════════════════════════════════


class TestC1DistillationArtifactsExist:
    """C1: Three comparative-distillation files exist at specified paths."""

    def test_c1_expansion_artifact_exists(self) -> None:
        assert file_exists(DISTILLATION_ARTIFACTS[0]), (
            f"Missing: {DISTILLATION_ARTIFACTS[0]}"
        )

    def test_c1_broadcasting_artifact_exists(self) -> None:
        assert file_exists(DISTILLATION_ARTIFACTS[1]), (
            f"Missing: {DISTILLATION_ARTIFACTS[1]}"
        )

    def test_c1_argentina_cv_artifact_exists(self) -> None:
        assert file_exists(DISTILLATION_ARTIFACTS[2]), (
            f"Missing: {DISTILLATION_ARTIFACTS[2]}"
        )


# ═══════════════════════════════════════════════════════════════════════════════
# Tests: C2 — Each artifact has action-type classifications
# ═══════════════════════════════════════════════════════════════════════════════


class TestC2ArtifactsHaveActionTypes:
    """C2: Each artifact contains at least 2 distinct action-type labels."""

    def _check_artifact(self, path: str) -> None:
        assert file_exists(path), f"Artifact {path} missing — cannot check action types"
        content = read(path)
        count = _count_action_types(content)
        assert count >= 2, (
            f"Artifact {path} has only {count} distinct action-type "
            f"label(s) (need >= 2). Found labels: {_ACTION_TYPES}"
        )

    def test_c2_expansion_has_action_types(self) -> None:
        self._check_artifact(DISTILLATION_ARTIFACTS[0])

    def test_c2_broadcasting_has_action_types(self) -> None:
        self._check_artifact(DISTILLATION_ARTIFACTS[1])

    def test_c2_argentina_cv_has_action_types(self) -> None:
        self._check_artifact(DISTILLATION_ARTIFACTS[2])


# ═══════════════════════════════════════════════════════════════════════════════
# Tests: C3 — Checklist has sports prediction gate with 6 inputs
# ═══════════════════════════════════════════════════════════════════════════════


class TestC3ChecklistHasSportsGate:
    """C3: option-selection-final-audit.md has sports prediction gate."""

    def test_c3_file_exists(self) -> None:
        assert file_exists(OPTION_SELECTION_CHECKLIST), (
            f"Missing: {OPTION_SELECTION_CHECKLIST}"
        )

    def test_c3_has_sports_gate_section(self) -> None:
        """A ##-level section about sports prediction or outcome-probability exists."""
        content = read(OPTION_SELECTION_CHECKLIST)
        sec = _section_after_heading(content, "Sports prediction|体育预测|outcome.probability|赛前预测")
        assert sec is not None, (
            "option-selection-final-audit.md lacks a sports prediction / "
            "赛前预测 section"
        )

    def test_c3_gate_has_six_inputs(self) -> None:
        """The sports gate defines at least 6 required input checkboxes."""
        content = read(OPTION_SELECTION_CHECKLIST)
        sec = _section_after_heading(content, "Sports prediction|体育预测|outcome.probability|赛前预测")
        assert sec is not None, "Missing sports gate section"
        # Count keyword matches for the 6 input categories
        match_count = sum(
            1 for kw in _SPORTS_GATE_INPUT_KEYWORDS if re.search(kw, sec, re.IGNORECASE)
        )
        assert match_count >= 6, (
            f"Sports gate section has only {match_count} of 6+ required input "
            f"keyword matches. Checked: {_SPORTS_GATE_INPUT_KEYWORDS}"
        )


# ═══════════════════════════════════════════════════════════════════════════════
# Tests: C4 — Gate includes downgrade rules and role labels
# ═══════════════════════════════════════════════════════════════════════════════


class TestC4GateHasDowngradeRules:
    """C4: sports prediction gate includes downgrade rules + role labels."""

    def test_c4_has_downgrade_rules(self) -> None:
        content = read(OPTION_SELECTION_CHECKLIST)
        sec = _section_after_heading(content, "Sports prediction|体育预测|outcome.probability|赛前预测")
        assert sec is not None, "Missing sports gate section"
        match_count = sum(
            1 for kw in _GATE_DOWNGRADE_KEYWORDS if re.search(kw, sec, re.IGNORECASE)
        )
        assert match_count >= 3, (
            f"Sports gate section has only {match_count} of 3+ downgrade/role-label "
            f"keyword matches. Checked: {_GATE_DOWNGRADE_KEYWORDS}"
        )


# ═══════════════════════════════════════════════════════════════════════════════
# Tests: C5 — Sports source-strength fixtures against #341 validators
# ═══════════════════════════════════════════════════════════════════════════════


class TestC5SportsSourceStrengthRegression:
    """C5: Sports-themed fixtures trigger existing #341 validator rules."""

    @staticmethod
    def _import_wikipedia_ratio():
        from validate_report_quality import check_source_register_wikipedia_ratio
        return check_source_register_wikipedia_ratio

    @staticmethod
    def _import_reliability_crowd():
        from validate_report_quality import check_source_register_reliability_crowdsourced
        return check_source_register_reliability_crowdsourced

    @staticmethod
    def _import_claims_supported():
        from validate_report_quality import check_claims_supported_semantics
        return check_claims_supported_semantics

    @staticmethod
    def _import_label_consistency():
        from validate_source_label_consistency import check_source_consistency
        return check_source_consistency

    # ── Fixture 1: 100% Wikipedia/CROWDSOURCED ───────────────────────

    def test_c5_sports_wiki_100pct_fails(self) -> None:
        """Sports fixture with 100% Wikipedia/CROWDSOURCED → errors."""
        check = self._import_wikipedia_ratio()
        text = _sports_fixture_wiki_100pct()
        errors, warnings = check(text)
        assert len(errors) > 0, (
            f"100% Wikipedia sports fixture should produce errors, "
            f"got errors={errors}, warnings={warnings}"
        )

    # ── Fixture 2: CROWDSOURCED + high reliability ───────────────────

    def test_c5_sports_crowdsourced_high_reliability_fails(self) -> None:
        """Sports fixture with CROWDSOURCED + high reliability → errors."""
        check = self._import_reliability_crowd()
        text = _sports_fixture_crowdsourced_high()
        errors = check(text)
        assert len(errors) > 0, (
            "CROWDSOURCED+high reliability sports fixture should produce errors, "
            f"got: {errors}"
        )

    # ── Fixture 3: Section-only Claims Supported ─────────────────────

    def test_c5_sports_section_only_claims_fails(self) -> None:
        """Sports fixture with pure-section Claims Supported → errors."""
        check = self._import_claims_supported()
        text = _sports_fixture_section_only_claims()
        errors, warnings = check(text)
        assert len(errors) > 0, (
            f"Section-only Claims Supported sports fixture should produce errors, "
            f"got errors={errors}, warnings={warnings}"
        )

    # ── Fixture 4: [确认事实] label mismatch ─────────────────────────

    def test_c5_sports_confirmed_label_mismatch_fails(self) -> None:
        """Sports fixture with [确认事实] on CROWDSOURCED source → errors."""
        check = self._import_label_consistency()
        text = _sports_fixture_confirmed_label_mismatch()
        errors = check(text)
        assert len(errors) > 0, (
            "[确认事实] label on CROWDSOURCED source in sports fixture "
            f"should produce errors, got: {errors}"
        )


# ═══════════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════════

ALL_TEST_CLASSES: list[tuple[str, type]] = [
    ("C1: Distillation artifacts exist", TestC1DistillationArtifactsExist),
    ("C2: Artifacts have action types", TestC2ArtifactsHaveActionTypes),
    ("C3: Checklist sports gate exists", TestC3ChecklistHasSportsGate),
    ("C4: Gate has downgrade rules", TestC4GateHasDowngradeRules),
    ("C5: Sports source-strength regression", TestC5SportsSourceStrengthRegression),
]


def _run_test_method(test_class: type, method_name: str) -> str | None:
    try:
        getattr(test_class(), method_name)()
        return None
    except (AssertionError, Exception) as exc:
        return str(exc)


def main() -> int:
    total = 0
    passed = 0
    failures: list[str] = []

    print("=" * 70)
    print("Issue #353 Phase C — Contract Tests")
    print("=" * 70)

    sys.path.insert(0, os.path.join(REPO_ROOT, "scripts"))

    for group_name, test_class in ALL_TEST_CLASSES:
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
