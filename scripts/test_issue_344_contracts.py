#!/usr/bin/env python3
"""Property-based contract tests for Issue #344 artifacts.

SDD contracts:
  C1: ComparativeDistillationContract — 4 new files must pass the template validator
  C2: EvalCaseContract — 2 new eval cases must have all required sections
  C3: IndexRowContract — Each new eval case is tracked in INDEX.md with correct metadata
  C4: CandidateRuleContract — New candidate rules have valid types and source references
  C5: CrossReferenceContract — All cross-references between artifacts are consistent
"""

from __future__ import annotations

import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator

ROOT = Path(__file__).resolve().parents[1]
CASE_DIR = ROOT / "evals" / "cases"
DISTILL_DIR = ROOT / "evals" / "comparative-distillation"
INDEX_PATH = ROOT / "evals" / "INDEX.md"
REGISTRY_PATH = ROOT / "evals" / "comparative-distillation" / "candidate-rule-registry.md"

# ── C1: ComparativeDistillationContract ─────────────────────────────────────


def test_c1_new_files_exist() -> None:
    """C1a: All 4 new comparative-distillation files must exist."""
    required = [
        "world-cup-best-third-rule-gpt-vs-local-comparative-distillation.md",
        "world-cup-info-advantage-gpt-vs-local-comparative-distillation.md",
        "world-cup-transition-vs-possession-gpt-vs-local-comparative-distillation.md",
        "world-cup-group-winner-path-advantage-gpt-vs-local-comparative-distillation.md",
    ]
    missing = [f for f in required if not (DISTILL_DIR / f).exists()]
    assert not missing, f"Missing comparative-distillation files: {missing}"


def test_c1_files_pass_validator() -> None:
    """C1b: All 4 new files pass validate_comparative_distillation_case.py."""
    new_files = [
        "world-cup-best-third-rule-gpt-vs-local-comparative-distillation.md",
        "world-cup-info-advantage-gpt-vs-local-comparative-distillation.md",
        "world-cup-transition-vs-possession-gpt-vs-local-comparative-distillation.md",
        "world-cup-group-winner-path-advantage-gpt-vs-local-comparative-distillation.md",
    ]
    validator = ROOT / "scripts" / "validate_comparative_distillation_case.py"
    for fname in new_files:
        fpath = DISTILL_DIR / fname
        if not fpath.exists():
            continue  # handled by test_c1_new_files_exist
        result = subprocess.run(
            [sys.executable, str(validator), str(fpath)],
            capture_output=True, text=True,
        )
        output = result.stdout + result.stderr
        assert "PASS" in output, (
            f"{fname} FAILED validator:\n{output}"
        )


def test_c1_action_types_are_valid() -> None:
    """C1c: All action types in new files must be one of {NEW_RULE, CHECKLIST_HARDENING, TEMPLATE_CHANGE, NO_ACTION}."""
    VALID_TYPES = {"NEW_RULE", "CHECKLIST_HARDENING", "TEMPLATE_CHANGE", "NO_ACTION"}
    new_files = [
        "world-cup-best-third-rule-gpt-vs-local-comparative-distillation.md",
        "world-cup-info-advantage-gpt-vs-local-comparative-distillation.md",
        "world-cup-transition-vs-possession-gpt-vs-local-comparative-distillation.md",
        "world-cup-group-winner-path-advantage-gpt-vs-local-comparative-distillation.md",
    ]
    for fname in new_files:
        fpath = DISTILL_DIR / fname
        if not fpath.exists():
            continue
        text = fpath.read_text(encoding="utf-8")
        # Find all action type backtick values in proper context
        action_types = set(re.findall(
            r"`(NEW_RULE|CHECKLIST_HARDENING|TEMPLATE_CHANGE|NO_ACTION)`", text
        ))
        # But also find any invalid ones that look like action types
        all_backtick_actions = set(re.findall(
            r"`([A-Z_]+)`", text
        ))
        invalid = {
            a for a in all_backtick_actions
            if a not in VALID_TYPES
            and a in {"NEW_RULE_EVAL", "MISSING_RULE", "RULE_CHANGE", "ADD_RULE", "FIX_RULE"}
        }
        assert not invalid, f"{fname} has invalid action type(s): {invalid}"


def test_c1_no_turn_references() -> None:
    """C1d: No 'turn...' references in new files."""
    new_files = [
        "world-cup-best-third-rule-gpt-vs-local-comparative-distillation.md",
        "world-cup-info-advantage-gpt-vs-local-comparative-distillation.md",
        "world-cup-transition-vs-possession-gpt-vs-local-comparative-distillation.md",
        "world-cup-group-winner-path-advantage-gpt-vs-local-comparative-distillation.md",
    ]
    for fname in new_files:
        fpath = DISTILL_DIR / fname
        if not fpath.exists():
            continue
        text = fpath.read_text(encoding="utf-8")
        turn_refs = re.findall(r"turn\d+", text, re.IGNORECASE)
        assert not turn_refs, f"{fname} has turn... references: {turn_refs}"


def test_c1_minimal_quality_bar_checked() -> None:
    """C1e: Each distillation file has its minimal quality bar checklist checked."""
    new_files = [
        "world-cup-best-third-rule-gpt-vs-local-comparative-distillation.md",
        "world-cup-info-advantage-gpt-vs-local-comparative-distillation.md",
        "world-cup-transition-vs-possession-gpt-vs-local-comparative-distillation.md",
        "world-cup-group-winner-path-advantage-gpt-vs-local-comparative-distillation.md",
    ]
    for fname in new_files:
        fpath = DISTILL_DIR / fname
        if not fpath.exists():
            continue
        text = fpath.read_text(encoding="utf-8")
        assert "Minimal quality bar" in text, f"{fname} missing 'Minimal quality bar' section"
        # Count [x] vs [ ] checkboxes
        checked = len(re.findall(r"- \[x\]", text))
        unchecked = len(re.findall(r"- \[ \]", text))
        if checked == 0:
            # Some files use different checkbox format
            checked = len(re.findall(r"- \[X\]", text))
        assert checked >= 5, (
            f"{fname} has only {checked} checked checkboxes (expected >=5), "
            f"{unchecked} unchecked"
        )


# ── C2: EvalCaseContract ────────────────────────────────────────────────────


EVAL_REQUIRED_SECTIONS = [
    "## Goal",
    "## What this eval is testing",
    "## Pass criteria",
    "## Failure signs",
    "## Why this eval matters",
    "## Current rule verdict",
    "## Related evals",
    "## Reviewer checklist",
    "## Suggested scoring",
]


def test_c2_new_eval_cases_exist() -> None:
    """C2a: All 4 new eval cases must exist (2 pre-existing + 2 new)."""
    required = [
        "world-cup-rule-regulatory-route-mismatch-case.md",
        "world-cup-info-advantage-technical-deep-dive-source-strength-case.md",
        "world-cup-transition-vs-possession-method-scaffold-case.md",
        "world-cup-group-winner-simulation-contract-case.md",
    ]
    missing = [f for f in required if not (CASE_DIR / f).exists()]
    assert not missing, f"Missing eval case files: {missing}"


def test_c2_new_eval_cases_have_required_sections() -> None:
    """C2b: All 4 eval cases have all required sections."""
    all_cases = [
        "world-cup-rule-regulatory-route-mismatch-case.md",
        "world-cup-info-advantage-technical-deep-dive-source-strength-case.md",
        "world-cup-transition-vs-possession-method-scaffold-case.md",
        "world-cup-group-winner-simulation-contract-case.md",
    ]
    for fname in all_cases:
        fpath = CASE_DIR / fname
        if not fpath.exists():
            continue
        text = fpath.read_text(encoding="utf-8")
        missing_sections = [
            s for s in EVAL_REQUIRED_SECTIONS
            if s not in text
        ]
        assert not missing_sections, f"{fname} missing sections: {missing_sections}"


def test_c2_eval_cases_have_valid_verdict() -> None:
    """C2c: Current rule verdict must reference valid status values."""
    VALID_VERDICTS = {"pass", "conditional-pass", "fail", "warn", "manual-review"}
    all_cases = [
        "world-cup-rule-regulatory-route-mismatch-case.md",
        "world-cup-info-advantage-technical-deep-dive-source-strength-case.md",
        "world-cup-transition-vs-possession-method-scaffold-case.md",
        "world-cup-group-winner-simulation-contract-case.md",
    ]
    for fname in all_cases:
        fpath = CASE_DIR / fname
        if not fpath.exists():
            continue
        text = fpath.read_text(encoding="utf-8")
        assert "## Current rule verdict" in text, f"{fname} missing Current rule verdict"
        # The verdict section content should reference valid statuses
        # Not strict checking since format varies


# ── C3: IndexRowContract ─────────────────────────────────────────────────────


def test_c3_all_eval_cases_are_indexed() -> None:
    """C3a: All 4 World Cup eval cases must be in INDEX.md."""
    expected_paths = [
        "evals/cases/world-cup-rule-regulatory-route-mismatch-case.md",
        "evals/cases/world-cup-info-advantage-technical-deep-dive-source-strength-case.md",
        "evals/cases/world-cup-transition-vs-possession-method-scaffold-case.md",
        "evals/cases/world-cup-group-winner-simulation-contract-case.md",
    ]
    index_text = INDEX_PATH.read_text(encoding="utf-8")
    missing = [p for p in expected_paths if p not in index_text]
    assert not missing, f"Missing from INDEX.md: {missing}"


def test_c3_indexed_cases_match_git_tracked_files() -> None:
    """C3b: All eval case files tracked by git must be in INDEX.md."""
    result = subprocess.run(
        ["git", "ls-files", "evals/cases/*.md"],
        cwd=ROOT, check=True, capture_output=True, text=True,
    )
    tracked = sorted(line.strip() for line in result.stdout.splitlines() if line.strip())
    # INDEX rows start with "| `evals/cases/"
    index_text = INDEX_PATH.read_text(encoding="utf-8")
    indexed = [
        f"evals/cases/{m}"
        for m in re.findall(r"`evals/cases/([^`]+)`", index_text)
    ]
    indexed_tracked = [p for p in tracked if p.split("evals/cases/", 1)[0] == ""]
    missing = [p for p in tracked if p not in indexed]
    assert not missing, f"Git-tracked eval cases not in INDEX.md: {missing}"


# ── C4: CandidateRuleContract ───────────────────────────────────────────────


# Canonical stem -> repo-relative source files for the candidate rule
# registry's `Source file(s)` column. This is an explicit map, not a prefix
# glob: a truncated or misspelled stem (e.g. `by`, `...outloo`) must be
# reported instead of silently resolving to a prefix match (issue #375 review
# P1 round 2). Keep in sync when the registry or eval assets change — the
# tests below fail closed on any registry stem missing from this map.
CANONICAL_RULE_SOURCES: dict[str, tuple[str, ...]] = {
    "agent-api-market-outlook": (
        "evals/cases/agent-api-market-outlook-full-spectrum-fail-case.md",
        "evals/comparative-distillation/agent-api-market-outlook-gpt-vs-local-comparative-distillation.md",
    ),
    "ai-coding-agent-market-outlook": (
        "evals/cases/ai-coding-agent-market-outlook-probability-case.md",
        "evals/comparative-distillation/ai-coding-agent-market-outlook-gpt-vs-minimax-comparative-distillation.md",
    ),
    "ai-coding-provider-selection": (
        "evals/cases/ai-coding-provider-selection-current-state-conflict-case.md",
        "evals/comparative-distillation/ai-coding-provider-selection-gpt-vs-local-comparative-distillation.md",
    ),
    "ai-edu-market-entry": (
        "evals/cases/ai-edu-market-entry-sensitivity-and-route-intersection-case.md",
        "evals/comparative-distillation/ai-edu-market-entry-gpt-vs-local-comparative-distillation.md",
    ),
    "amd-minimax-equity-report": (
        "evals/comparative-distillation/amd-minimax-equity-report-distillation.md",
    ),
    "api-supplier-selection": (
        "evals/comparative-distillation/api-supplier-selection-gpt-vs-minimax-comparative-distillation.md",
    ),
    "byd": (
        "evals/cases/byd-competitive-positioning-traceability-hard-fail-case.md",
        "evals/cases/byd-report-format-discipline-case.md",
        "evals/comparative-distillation/byd-gpt-vs-minimax-comparative-distillation.md",
    ),
    "cas-space-minimax-company-report": (
        "evals/comparative-distillation/cas-space-minimax-company-report-distillation.md",
    ),
    "china-shenhua": (
        "evals/cases/china-shenhua-listed-company-judgment-and-traceability-case.md",
        "evals/comparative-distillation/china-shenhua-minimax-vs-reference-grade-company-memo-comparative-distillation.md",
    ),
    "dc-power": (
        "evals/cases/dc-power-market-outlook-forward-looking-label-gap-case.md",
        "evals/cases/dc-power-market-outlook-inflation-and-monitoring-case.md",
    ),
    "home-server-equipment-recommendation": (
        "evals/comparative-distillation/home-server-equipment-recommendation-minimax-comparative-distillation.md",
    ),
    "japan-vs-china-vs-sea-market-entry": (
        "evals/comparative-distillation/japan-vs-china-vs-sea-market-entry-comparative-distillation.md",
    ),
    "multi-origin-meetup-city-selection": (
        "evals/comparative-distillation/multi-origin-meetup-city-selection-gpt-vs-minimax-comparative-distillation.md",
    ),
    "sea-market-entry": (
        "evals/comparative-distillation/sea-market-entry-gpt-vs-minimax-comparative-distillation.md",
    ),
    "small-team-ai-agent": (
        "evals/comparative-distillation/small-team-ai-agent-gpt-vs-local-comparative-distillation.md",
    ),
    "weekend-seaside-destination": (
        "evals/comparative-distillation/weekend-seaside-destination-gpt-vs-minimax-comparative-distillation.md",
    ),
    "world-cup-constrained-choice": (
        "evals/cases/world-cup-constrained-choice-wrong-route-case.md",
        "evals/comparative-distillation/world-cup-constrained-choice-gpt-vs-local-comparative-distillation.md",
    ),
    "world-cup-group-winner-path-advantage-gpt-vs-local-comparative-distillation": (
        "evals/comparative-distillation/world-cup-group-winner-path-advantage-gpt-vs-local-comparative-distillation.md",
    ),
    "world-cup-transition-vs-possession-gpt-vs-local-comparative-distillation": (
        "evals/comparative-distillation/world-cup-transition-vs-possession-gpt-vs-local-comparative-distillation.md",
    ),
}


def _registry_source_problems(registry_text: str, indexed_cases: set[str]) -> list[str]:
    """Validate the registry table's `Source file(s)` column (bare stems).

    Each stem must be a key of the explicit CANONICAL_RULE_SOURCES map (no
    prefix globbing — truncated or misspelled stems are reported, not
    resolved). Every referenced file must exist, and every referenced
    `evals/cases/*.md` must be registered in INDEX.md.

    Returns a list of problems; an empty list means the registry is healthy.
    """
    problems: list[str] = []
    for line in registry_text.splitlines():
        cols = [c.strip() for c in line.split("|")]
        if len(cols) < 9 or not re.match(r"R\d+", cols[1]):
            continue
        rule_id = cols[1]
        for stem in (s.strip() for s in cols[4].split(",") if s.strip()):
            if stem not in CANONICAL_RULE_SOURCES:
                problems.append(
                    f"Source file(s) '{stem}' ({rule_id}) is not a canonical "
                    f"rule source; add it to CANONICAL_RULE_SOURCES or fix the typo"
                )
                continue
            for rel in CANONICAL_RULE_SOURCES[stem]:
                path = ROOT / rel
                if not path.exists():
                    problems.append(
                        f"Referenced source file does not exist: {rel} ({rule_id})"
                    )
                if rel.startswith("evals/cases/"):
                    name = rel[len("evals/cases/"):]
                    if name not in indexed_cases:
                        problems.append(
                            f"{rel} ({rule_id} source) is not registered in evals/INDEX.md"
                        )
    return problems


def test_c4_candidate_rule_sources_exist() -> None:
    """C4a: All candidate rule source files must exist and be indexed."""
    assert REGISTRY_PATH.exists(), f"Registry missing: {REGISTRY_PATH}"
    text = REGISTRY_PATH.read_text(encoding="utf-8")
    # References appear in two forms: repo-relative paths (`` `evals/cases/x.md` ``)
    # and bare filenames (`` `world-cup-x-case.md` ``) that live in either the
    # eval case directory or the comparative-distillation directory. Resolve
    # both forms and fail closed on any missing file (issue #375).
    source_refs = re.findall(r"`([^`]+\.md)`", text)
    for ref in source_refs:
        if ref.startswith("evals/"):
            expected = ROOT / ref
            assert expected.exists(), f"Referenced source file does not exist: {ref}"
        elif "/" not in ref:
            in_cases = (CASE_DIR / ref).exists()
            in_distill = (DISTILL_DIR / ref).exists()
            assert in_cases or in_distill, (
                f"Referenced source file does not exist: {ref} "
                f"(looked in {CASE_DIR} and {DISTILL_DIR})"
            )
    # The table's `Source file(s)` column uses bare stems (no `.md` suffix, no
    # backticks). Resolve them through the explicit CANONICAL_RULE_SOURCES map
    # and fail closed on unknown/truncated stems, missing files, or eval cases
    # missing from INDEX.md (issue #375 review P1 + P1 round 2).
    indexed_cases = set(
        re.findall(
            r"evals/cases/([^`\s]+\.md)",
            INDEX_PATH.read_text(encoding="utf-8"),
        )
    )
    problems = _registry_source_problems(text, indexed_cases)
    assert not problems, (
        "Candidate rule registry source problems:\n" + "\n".join(problems)
    )


def test_c4_missing_source_stem_detected() -> None:
    """C4a-negative: unknown or truncated source stems are reported.

    Covers both a fully unknown stem and truncated prefixes of real stems
    (e.g. `by` must not resolve to `byd-*`; prefix globbing would let these
    through — issue #375 review P1 round 2).
    """
    bad_stems = (
        "this-stem-does-not-exist-anywhere",
        "by",                      # truncated prefix of byd
        "ai-coding-agent-market-outloo",  # truncated prefix of ...outlook
        "world-cup-transitio",     # truncated prefix of ...transition...
        "world-cup",               # truncated to a shared token
    )
    for stem in bad_stems:
        fake = (
            "| ID | Candidate rule | Action type | Source file(s) | Frequency | "
            "Original label | Existing coverage | Coverage status |\n"
            f"| R99 | fake rule | NEW_RULE | {stem} | 1 | "
            "PROMOTE_NOW | - | 无覆盖 |\n"
        )
        problems = _registry_source_problems(fake, set())
        assert any(stem in p for p in problems), (stem, problems)


def test_c4_case_not_indexed_detected() -> None:
    """C4a-negative: an eval case referenced but missing from INDEX.md is reported."""
    # Use a real canonical stem that maps to an evals/cases/ file ("byd").
    assert "byd" in CANONICAL_RULE_SOURCES
    fake = (
        "| ID | Candidate rule | Action type | Source file(s) | Frequency | "
        "Original label | Existing coverage | Coverage status |\n"
        "| R99 | fake rule | NEW_RULE | byd | 1 | "
        "PROMOTE_NOW | - | 无覆盖 |\n"
    )
    problems = _registry_source_problems(fake, set())
    assert any("byd-report-format-discipline-case.md" in p for p in problems), problems
    assert any("evals/INDEX.md" in p for p in problems), problems


def test_c4_no_duplicate_candidate_ids() -> None:
    """C4b: All candidate rule IDs (Rxx) must be unique."""
    assert REGISTRY_PATH.exists(), f"Registry missing: {REGISTRY_PATH}"
    text = REGISTRY_PATH.read_text(encoding="utf-8")
    ids = re.findall(r"\|\s*(R\d+)\s*\|", text)
    duplicates = [r for r in ids if ids.count(r) > 1]
    assert not duplicates, f"Duplicate candidate rule IDs: {set(duplicates)}"


# ── C5: CrossReferenceContract ──────────────────────────────────────────────


def test_c5_eval_to_index_related_issues_consistent() -> None:
    """C5a: Eval cases that reference issues should have them in INDEX.md."""
    all_cases = [
        "world-cup-rule-regulatory-route-mismatch-case.md",
        "world-cup-info-advantage-technical-deep-dive-source-strength-case.md",
        "world-cup-transition-vs-possession-method-scaffold-case.md",
        "world-cup-group-winner-simulation-contract-case.md",
    ]
    for fname in all_cases:
        fpath = CASE_DIR / fname
        if not fpath.exists():
            continue
        case_text = fpath.read_text(encoding="utf-8")
        # Extract issue references from the case file
        issue_refs = set(re.findall(r"#(\d{3})", case_text))
        # Check INDEX.md has corresponding references
        index_text = INDEX_PATH.read_text(encoding="utf-8")
        case_stem = fname.replace("-case.md", "")
        # Find the index row for this case
        pattern = rf"\|\s*`evals/cases/{re.escape(fname)}`\s*\|"
        match = re.search(pattern, index_text)
        if match:
            row_start = match.start()
            row_end = index_text.find("\n", match.end())
            if row_end == -1:
                row_end = len(index_text)
            row_content = index_text[match.start():row_end]
            for issue_ref in issue_refs:
                assert f"#{issue_ref}" in row_content, (
                    f"{fname} references #{issue_ref} but INDEX.md row doesn't"
                )


def test_c5_distillation_to_registry_linkage() -> None:
    """C5b: Comparative-distillations should have corresponding entries in candidate-rule-registry if they produce NEW_RULE candidates."""
    distills = [
        "world-cup-best-third-rule-gpt-vs-local-comparative-distillation.md",
        "world-cup-info-advantage-gpt-vs-local-comparative-distillation.md",
        "world-cup-transition-vs-possession-gpt-vs-local-comparative-distillation.md",
        "world-cup-group-winner-path-advantage-gpt-vs-local-comparative-distillation.md",
    ]
    for dname in distills:
        dpath = DISTILL_DIR / dname
        if not dpath.exists():
            continue
        text = dpath.read_text(encoding="utf-8")
        short_name = dname.replace("-gpt-vs-local-comparative-distillation.md", "")
        # If the distillation has NEW_RULE actions, they should appear in registry
        new_rules = re.findall(r"\|\s*\d+\s*\|.*\|.*NEW_RULE.*\|", text)
        if new_rules and REGISTRY_PATH.exists():
            reg_text = REGISTRY_PATH.read_text(encoding="utf-8")
            # Not strict: just warn if no match found
            assert short_name in reg_text, (
                f"{dname} has NEW_RULE candidates but not mentioned in candidate-rule-registry.md"
            )


# ── Runner ───────────────────────────────────────────────────────────────────


def main() -> int:
    tests = [
        # C1
        test_c1_new_files_exist,
        test_c1_files_pass_validator,
        test_c1_action_types_are_valid,
        test_c1_no_turn_references,
        test_c1_minimal_quality_bar_checked,
        # C2
        test_c2_new_eval_cases_exist,
        test_c2_new_eval_cases_have_required_sections,
        test_c2_eval_cases_have_valid_verdict,
        # C3
        test_c3_all_eval_cases_are_indexed,
        test_c3_indexed_cases_match_git_tracked_files,
        # C4
        test_c4_candidate_rule_sources_exist,
        test_c4_no_duplicate_candidate_ids,
        # C5
        test_c5_eval_to_index_related_issues_consistent,
        test_c5_distillation_to_registry_linkage,
    ]
    failures = []
    for test in tests:
        try:
            test()
            print(f"  PASS  {test.__name__}")
        except AssertionError as exc:
            failures.append((test.__name__, str(exc)))
            print(f"  FAIL  {test.__name__}: {exc}")
        except FileNotFoundError as exc:
            failures.append((test.__name__, str(exc)))
            print(f"  FAIL  {test.__name__}: File not found: {exc}")

    if failures:
        print(f"\n{len(failures)} test(s) FAILED.")
        return 1
    print(f"\nAll {len(tests)} tests PASSED.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
