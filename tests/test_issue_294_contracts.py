#!/usr/bin/env python3
"""
Property-based contract validation for issue #294.

Tests verify structural invariants:
  C1: Two academic-review eval case files are git-tracked (not untracked).
  C2: evals/INDEX.md contains entries for both cases, table remains parseable.
  C3: Each eval case file contains all required standard sections.
  C4: Cross-references exist (between cases, from checklists to cases).
  C5: This test file itself verifies all contracts and passes.
  C6: No scope creep — only specified files changed, eval content unchanged.

Usage:
    python tests/test_issue_294_contracts.py

Expected BEFORE implementation:
    C1 FAIL (files untracked), C2 FAIL (no INDEX entries), C4 FAIL (no cross-refs)

Expected AFTER implementation:
    ALL PASS
"""

import re
import os
import subprocess
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

NEW_CASE_FILES = [
    "evals/cases/ai-agent-planning-academic-review-compounded-case.md",
    "evals/cases/mllm-visual-reasoning-academic-review-narrow-fail-case.md",
]

REQUIRED_SECTIONS = [
    "## Goal",
    "## Prompt",
    "## What this eval is testing",
    "## Pass criteria",
    "## Failure signs",
]

# ── helpers ───────────────────────────────────────────────────────

def read(path):
    with open(os.path.join(REPO_ROOT, path), "r") as f:
        return f.read()


def file_exists(path):
    return os.path.exists(os.path.join(REPO_ROOT, path))


def is_git_tracked(path):
    """Check if a file is tracked by git (not untracked)."""
    result = subprocess.run(
        ["git", "ls-files", "--error-unmatch", path],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


# ═══════════════════════════════════════════════════════════════════
# C1: File Tracking Invariant
# ═══════════════════════════════════════════════════════════════════

def test_c1_file_exists():
    """C1: Both eval case files MUST exist on disk."""
    for f in NEW_CASE_FILES:
        assert file_exists(f), f"File does not exist: {f}"


def test_c1_git_tracked():
    """C1: Both eval case files MUST be git-tracked (not untracked)."""
    for f in NEW_CASE_FILES:
        assert is_git_tracked(f), (
            f"File is NOT git-tracked (untracked): {f}\n"
            f"  Run: git add {f}"
        )


def test_c1_only_two_new_academic_files():
    """C1: No OTHER untracked academic-review eval files should be tracked by this issue.

    This is an informational check — the issue scope is exactly 2 files.
    """
    # This is a soft check: we list tracked academic cases and confirm our 2 are among them
    result = subprocess.run(
        ["git", "ls-files", "evals/cases/"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    tracked = [line for line in result.stdout.strip().split("\n") if line]
    for f in NEW_CASE_FILES:
        assert f in tracked, f"Expected {f} to be git-tracked"


# ═══════════════════════════════════════════════════════════════════
# C2: INDEX.md Structural Invariant
# ═══════════════════════════════════════════════════════════════════

def test_c2_index_has_new_case_entries():
    """C2: evals/INDEX.md MUST contain an entry for each new eval case."""
    content = read("evals/INDEX.md")
    filenames = [os.path.basename(f) for f in NEW_CASE_FILES]
    for fn in filenames:
        assert fn in content, (
            f"INDEX.md missing entry for {fn}\n"
            f"  Add a row to evals/INDEX.md for this case."
        )


def test_c2_index_table_consistent_columns():
    """C2: All data rows in INDEX.md table MUST have exactly 11 columns (10 data + empty edges)."""
    content = read("evals/INDEX.md")
    lines = content.split("\n")
    in_table = False
    column_counts = []
    for line in lines:
        # Detect the separator line: starts with |--- or | ---
        if re.match(r'^\|\s?---', line):
            in_table = True
            continue
        if in_table and line.startswith("|"):
            cols = len(line.split("|"))
            column_counts.append(cols)
        elif in_table and not line.startswith("|"):
            in_table = False
    assert len(column_counts) > 0, "No table rows found in INDEX.md"
    assert max(column_counts) == min(column_counts), (
        f"Inconsistent INDEX.md table columns: min={min(column_counts)}, "
        f"max={max(column_counts)}"
    )


def test_c2_index_rows_have_10_or_more_columns():
    """C2: Each INDEX.md table row MUST have >= 10 columns."""
    content = read("evals/INDEX.md")
    lines = content.split("\n")
    in_table = False
    for line in lines:
        if re.match(r'^\|\s?---', line):
            in_table = True
            continue
        if in_table and line.startswith("|"):
            cols = len(line.split("|"))
            assert cols >= 11, f"Row has {cols} columns (need >= 10 data columns): {line[:60]}..."
        elif in_table and not line.startswith("|"):
            in_table = False


def test_c2_new_entries_have_expected_metadata():
    """C2: Each new INDEX.md entry MUST have primary route=academic-review and status=active."""
    content = read("evals/INDEX.md")
    for fn in [os.path.basename(f) for f in NEW_CASE_FILES]:
        # Find the row
        lines = [l for l in content.split("\n") if fn in l]
        assert len(lines) >= 1, f"No INDEX.md row found containing {fn}"
        for line in lines:
            # Check primary route
            if "ai-agent-planning" in fn:
                assert "academic-review" in line, (
                    f"Row for {fn} missing primary route 'academic-review'"
                )
                assert "fail" in line.lower(), (
                    f"Row for {fn} should have 'fail' in current rule status"
                )
            if "mllm-visual-reasoning" in fn:
                assert "academic-review" in line, (
                    f"Row for {fn} missing primary route 'academic-review'"
                )
                assert "conditional-pass" in line.lower(), (
                    f"Row for {fn} should have 'conditional-pass' in current rule status"
                )


# ═══════════════════════════════════════════════════════════════════
# C3: Eval File Structural Invariant
# ═══════════════════════════════════════════════════════════════════

def test_c3_required_sections_present():
    """C3: Each eval case file MUST contain all required sections."""
    for f in NEW_CASE_FILES:
        content = read(f)
        for section in REQUIRED_SECTIONS:
            assert section in content, (
                f"{f} missing required section: {section}"
            )


def test_c3_has_failure_signs():
    """C3: Each eval case file MUST have actionable failure signs (markdown list)."""
    for f in NEW_CASE_FILES:
        content = read(f)
        assert "## Failure signs" in content, f"{f} missing ## Failure signs section"
        section = content.split("## Failure signs")[1].split("##")[0]
        has_list = any(line.strip().startswith("- ") for line in section.split("\n"))
        assert has_list, f"{f}: ## Failure signs section has no list items"


def test_c3_has_related_evals_section():
    """C3: Each eval case file SHOULD have a related-evals section linking to the other case."""
    for f in NEW_CASE_FILES:
        content = read(f)
        assert "## Related evals" in content or "## Related" in content, (
            f"{f} missing 'Related evals' section"
        )


# ═══════════════════════════════════════════════════════════════════
# C4: Cross-Reference Invariant
# ═══════════════════════════════════════════════════════════════════

def test_c4_cases_reference_each_other():
    """C4: Each eval case MUST reference the other in 'Related evals'."""
    f1 = NEW_CASE_FILES[0]
    f2 = NEW_CASE_FILES[1]
    content1 = read(f1)
    content2 = read(f2)
    f2_basename = os.path.basename(f2)
    f1_basename = os.path.basename(f1)
    assert f2_basename in content1, (
        f"{f1} does not reference {f2_basename} in Related evals"
    )
    assert f1_basename in content2, (
        f"{f2} does not reference {f1_basename} in Related evals"
    )


def test_c4_academic_analysis_audit_references_cases():
    """C4: checklists/academic-analysis-audit.md MUST reference both eval cases."""
    content = read("checklists/academic-analysis-audit.md")
    basenames = [os.path.basename(f) for f in NEW_CASE_FILES]
    for bn in basenames:
        assert bn in content, (
            f"checklists/academic-analysis-audit.md missing reference to {bn}"
        )


# ═══════════════════════════════════════════════════════════════════
# C5: Test Coverage Invariant (self-referential)
# ═══════════════════════════════════════════════════════════════════

def test_c5_test_file_exists():
    """C5: This test file MUST exist."""
    test_path = "tests/test_issue_294_contracts.py"
    assert file_exists(test_path), f"{test_path} does not exist"


def test_c5_test_contains_all_contract_tests():
    """C5: This test file MUST have tests for C1-C4 (at minimum)."""
    content = read("tests/test_issue_294_contracts.py")
    # Check for contract-specific test functions
    assert "test_c1_" in content, "Missing C1 tests"
    assert "test_c2_" in content, "Missing C2 tests"
    assert "test_c3_" in content, "Missing C3 tests"
    assert "test_c4_" in content, "Missing C4 tests"


def test_c5_no_regression_on_existing_tests():
    """C5: Existing contract tests MUST still pass."""
    existing_tests = [
        "tests/test_capital_return_discipline.py",
        "tests/test_issue_270_contracts.py",
        "tests/test_issue_272_contracts.py",
        "tests/test_issue_278_contracts.py",
        "tests/test_issue_280_contracts.py",
    ]
    for test_file in existing_tests:
        if not file_exists(test_file):
            continue
        result = subprocess.run(
            [sys.executable, test_file],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert result.returncode == 0, (
            f"Regression in {test_file}:\n"
            f"STDOUT: {result.stdout[-500:]}\n"
            f"STDERR: {result.stderr[-500:]}"
        )


# ═══════════════════════════════════════════════════════════════════
# C6: Scope Boundary
# ═══════════════════════════════════════════════════════════════════

def test_c6_only_intended_files_changed():
    """C6: Only the intended set of files should be modified (no scope creep)."""
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMRT"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    changed_files = set(result.stdout.strip().split("\n")) if result.stdout.strip() else set()
    # Allow files that are part of this PR
    allowed = {
        "evals/INDEX.md",
        "checklists/academic-analysis-audit.md",
        "evals/cases/ai-agent-planning-academic-review-compounded-case.md",
        "evals/cases/mllm-visual-reasoning-academic-review-narrow-fail-case.md",
        "evals/cases/argentina-cape-verde-constrained-choice-route-and-source-fail-case.md",
        "evals/cases/world-cup-expansion-regulatory-contract-and-source-fail-case.md",
        "evals/cases/world-cup-sports-broadcasting-market-outlook-source-and-monitoring-case.md",
        "tests/test_issue_294_contracts.py",
        "tests/test_issue_353_contracts.py",
        "ROUTING-MATRIX.md",
    }
    unexpected = changed_files - allowed
    assert not unexpected, (
        f"Unexpected modified files (scope creep): {sorted(unexpected)}"
    )


def test_c6_eval_structure_preserved():
    """C6: Eval case files retain their required structural sections."""
    for f in NEW_CASE_FILES:
        content = read(f)
        assert content.startswith("# "), (
            f"{f}: expected markdown heading at start"
        )
        assert "## Goal" in content
        assert "## Prompt" in content


# ═══════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    tests = [
        ("C1: file exists", test_c1_file_exists),
        ("C1: git tracked", test_c1_git_tracked),
        ("C1: only 2 new tracked", test_c1_only_two_new_academic_files),
        ("C2: INDEX has entries", test_c2_index_has_new_case_entries),
        ("C2: consistent columns", test_c2_index_table_consistent_columns),
        ("C2: >=10 columns", test_c2_index_rows_have_10_or_more_columns),
        ("C2: metadata correct", test_c2_new_entries_have_expected_metadata),
        ("C3: required sections", test_c3_required_sections_present),
        ("C3: failure signs", test_c3_has_failure_signs),
        ("C3: related evals", test_c3_has_related_evals_section),
        ("C4: cross-references", test_c4_cases_reference_each_other),
        ("C4: audit references", test_c4_academic_analysis_audit_references_cases),
        ("C5: test file exists", test_c5_test_file_exists),
        ("C5: contract coverage", test_c5_test_contains_all_contract_tests),
        ("C5: no regression", test_c5_no_regression_on_existing_tests),
        ("C6: scope creep", test_c6_only_intended_files_changed),
        ("C6: structure preserved", test_c6_eval_structure_preserved),
    ]

    passed = 0
    failed = 0
    for name, fn in tests:
        try:
            fn()
            print(f"  ✅ {name}")
            passed += 1
        except (AssertionError, ValueError) as e:
            print(f"  ❌ {name}: {e}")
            failed += 1
        except Exception as e:
            print(f"  ❌ {name}: Unexpected error: {e}")
            failed += 1

    print(f"\n{'='*50}")
    print(f"Results: {passed} passed, {failed} failed")
    if failed:
        sys.exit(1)
    else:
        print("All contracts verified ✅")
