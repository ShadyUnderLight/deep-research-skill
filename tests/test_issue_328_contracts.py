#!/usr/bin/env python3
"""
Property-based contract validation for issue #328.

Tests verify structural invariants for Market Entry two-level decision funnel,
Country Diligence Card, recommendation-constraint consistency, and sensitivity
switching table.

  C1: checklists/option-selection-final-audit.md
      - Constraint consistency checklist items exist
      - Sensitivity/switching table checklist item exists
      - Country Diligence Card checklist items exist
      - Existing content preserved
  C2: references/decision-report-template.md
      - Country Diligence Card template with 10 fields + evidence role + source
      - Sensitivity switching table format
      - Two-level funnel structure (region screening → country competition)
      - Existing content preserved
  C3: ROUTING-MATRIX.md
      - Two-level funnel in artifact contract
      - New hard fail for missing country competition
      - Existing content preserved
  C4: references/option-selection-and-shortlist-discipline.md
      - Two new heuristic questions for two-level funnel
      - Existing content preserved
  C5: evals/cases/ new file exists
      - File exists with standard eval structure
      - References issue #328
  C6: evals/INDEX.md
      - Entry for new eval case
      - Table format preserved
  C7: Cross-file invariants
      - No regression in existing contract tests
      - INDEX.md table parseable

Usage:
    python tests/test_issue_328_contracts.py

Expected BEFORE implementation (RED):
    ALL FAIL

Expected AFTER implementation (GREEN):
    ALL PASS
"""

import re
import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def read(path):
    with open(os.path.join(REPO_ROOT, path), "r") as f:
        return f.read()


def file_exists(path):
    return os.path.exists(os.path.join(REPO_ROOT, path))


def section_after(content, section_title):
    """Return content starting from a ## section title."""
    match = re.search(
        r'^#{2,3}\s+' + re.escape(section_title) + r'\s*$',
        content,
        re.MULTILINE
    )
    if not match:
        return None
    return content[match.start():]


# ═══════════════════════════════════════════════════════════════════
# C1: checklists/option-selection-final-audit.md
# ═══════════════════════════════════════════════════════════════════

CHECKLIST = "checklists/option-selection-final-audit.md"


def test_c1a_constraint_consistency_check():
    """C1a: Market-entry gate MUST have constraint-consistency check item."""
    content = read(CHECKLIST)
    assert re.search(
        r'recommendation.*constraint.*consistency|'
        r'GO.*budget.*team.*timeframe.*consistent|'
        r'推荐.*约束.*一致',
        content,
        re.IGNORECASE
    ), "Missing constraint-consistency checklist item"


def test_c1b_sensitivity_switching_table():
    """C1b: Market-entry gate MUST have sensitivity/switching table check."""
    content = read(CHECKLIST)
    assert re.search(
        r'sensitivity.*switch|切换.*表|what would change.*beachhead',
        content,
        re.IGNORECASE
    ), "Missing sensitivity/switching table checklist item"


def test_c1c_country_diligence_card():
    """C1c: Market-entry gate MUST have Country Diligence Card check."""
    content = read(CHECKLIST)
    assert re.search(
        r'Country.?Diligence.?Card|diligence.?card|diligence.*template|尽职调查',
        content,
        re.IGNORECASE
    ), "Missing Country Diligence Card checklist item"


def test_c1d_two_level_funnel():
    """C1d: Market-entry gate MUST have two-level funnel check."""
    content = read(CHECKLIST)
    assert re.search(
        r'region.*screen|region.*comparison|两级.*漏斗|区域.*初筛|区域.*复赛|funnel',
        content,
        re.IGNORECASE
    ), "Missing two-level funnel checklist item"


# ═══════════════════════════════════════════════════════════════════
# C2: references/decision-report-template.md
# ═══════════════════════════════════════════════════════════════════

TEMPLATE = "references/decision-report-template.md"


def test_c2a_country_diligence_card_template():
    """C2a: Template MUST contain Country Diligence Card with 10+ fields."""
    content = read(TEMPLATE)
    card_section = section_after(content, "Country Diligence Card")
    assert card_section is not None, "Missing Country Diligence Card section"

    required_fields = [
        "目标客户", "首笔收入", "本地化", "监管", "竞争",
        "渠道", "Entry motion", "成本与周期", "法律", "扩展",
    ]
    for field in required_fields:
        assert field in card_section, (
            f"Country Diligence Card missing field: {field}"
        )


def test_c2b_evidence_role_column():
    """C2b: Country Diligence Card MUST have evidence role column."""
    content = read(TEMPLATE)
    card_section = section_after(content, "Country Diligence Card")
    assert card_section is not None, "Missing Country Diligence Card section"
    assert re.search(
        r'Evidence.?role|observed|proxy|assumption|model.?output',
        card_section,
        re.IGNORECASE
    ), "Country Diligence Card missing evidence role column"


def test_c2c_sensitivity_switching_table_format():
    """C2c: Template MUST contain sensitivity switching table format."""
    content = read(TEMPLATE)
    assert re.search(
        r'sensitivity.*switch|切换|what would change.*beachhead|under what.*would.*switch',
        content,
        re.IGNORECASE
    ), "Missing sensitivity/switching table format"


def test_c2d_two_level_funnel_structure():
    """C2d: Template MUST indicate two-level funnel structure."""
    content = read(TEMPLATE)
    assert re.search(
        r'region.*screen|区域.*初筛|regional.?comparison|country.?competition|国家.*复赛|两级.*漏斗',
        content,
        re.IGNORECASE
    ), "Missing two-level funnel structure in market-entry template"


# ═══════════════════════════════════════════════════════════════════
# C3: ROUTING-MATRIX.md
# ═══════════════════════════════════════════════════════════════════

ROUTING = "ROUTING-MATRIX.md"


def test_c3a_two_level_funnel_contract():
    """C3a: Market Entry artifact contract MUST require two-level funnel."""
    content = read(ROUTING)
    market_entry_section = section_after(content, "Route: Market Entry / Regional Expansion")
    assert market_entry_section is not None, "Market Entry section not found"

    contract_match = re.search(
        r'### Visible artifact contract',
        market_entry_section
    )
    assert contract_match is not None, "Visible artifact contract not found in Market Entry"

    contract_content = market_entry_section[contract_match.start():]
    assert re.search(
        r'region.*screen|区域.*初筛|country.*competition|国家.*复赛|两级.*漏斗|two.level.*funnel',
        contract_content,
        re.IGNORECASE
    ), "Two-level funnel missing from artifact contract"


def test_c3b_new_hard_fail():
    """C3b: Market Entry hard fail MUST include missing country-competition."""
    content = read(ROUTING)
    market_entry_section = section_after(content, "Route: Market Entry / Regional Expansion")
    assert market_entry_section is not None, "Market Entry section not found"

    hard_fail_match = re.search(
        r'### Hard fail',
        market_entry_section
    )
    assert hard_fail_match is not None, "Hard fail section not found in Market Entry"

    hard_fail_content = market_entry_section[hard_fail_match.start():]
    assert re.search(
        r'skips.*country.*competition|country.?competition.*missing|'
        r'jump.*directly.*regional.*winner|missing.*country.?shortlist.*within|'
        r'胜出区域.*未.*国家.*复赛|跳过.*区域.*筛选|第二级.*未',
        hard_fail_content,
        re.IGNORECASE
    ), "Missing hard fail for skipping second-level country competition"


# ═══════════════════════════════════════════════════════════════════
# C4: references/option-selection-and-shortlist-discipline.md
# ═══════════════════════════════════════════════════════════════════

DISCIPLINE = "references/option-selection-and-shortlist-discipline.md"


def test_c4a_two_level_heuristic_questions():
    """C4a: Discipline MUST have region-screening heuristic questions."""
    content = read(DISCIPLINE)
    # The heuristic questions are in a paragraph under "When the task involves market entry..."
    # Search the entire file since this is not a markdown heading
    assert re.search(
        r'market entry.*regional expansion.*country prioritization',
        content,
        re.IGNORECASE
    ), "Market entry questions section not found"
    assert re.search(
        r'two.level.*funnel|region.*screen|funnel.*level|'
        r'diligence.?card|evidence-role labels|尽职调查',
        content,
        re.IGNORECASE
    ), "Missing two-level funnel or diligence card heuristic questions"


# ═══════════════════════════════════════════════════════════════════
# C5: New eval case
# ═══════════════════════════════════════════════════════════════════

EVAL_CASE = "evals/cases/market-entry-two-level-funnel-and-diligence-case.md"


def test_c5a_eval_case_exists():
    """C5a: Eval case file MUST exist."""
    assert file_exists(EVAL_CASE), f"Missing eval case: {EVAL_CASE}"


def test_c5b_standard_eval_structure():
    """C5b: Eval case MUST have Goal, Pass criteria, Failure signs."""
    content = read(EVAL_CASE)
    assert re.search(r'^##\s+Goal', content, re.MULTILINE), "Missing ## Goal"
    assert re.search(r'^##\s+Pass criteria', content, re.MULTILINE), "Missing ## Pass criteria"
    assert re.search(r'^##\s+Failure signs', content, re.MULTILINE), "Missing ## Failure signs"


def test_c5c_references_issue():
    """C5c: Eval case MUST reference issue #328."""
    content = read(EVAL_CASE)
    assert "#328" in content, "Eval case must reference issue #328"


# ═══════════════════════════════════════════════════════════════════
# C6: evals/INDEX.md
# ═══════════════════════════════════════════════════════════════════

INDEX = "evals/INDEX.md"


def test_c6a_index_entry_exists():
    """C6a: INDEX.md MUST have entry for new eval case."""
    content = read(INDEX)
    assert "market-entry-two-level-funnel-and-diligence-case" in content, \
        "Missing entry in evals/INDEX.md"


def test_c6b_index_table_parseable():
    """C6b: INDEX.md table MUST be parseable (same number of pipes per row)."""
    content = read(INDEX)
    table_lines = [l for l in content.split('\n') if l.strip().startswith('|')]
    if not table_lines:
        return
    pipe_counts = [l.count('|') for l in table_lines]
    header_count = max(pipe_counts[:3])
    for i, count in enumerate(pipe_counts):
        assert count == header_count or count == 0 or table_lines[i].strip() in ('', '| --- '), (
            f"INDEX.md table row {i+1} has {count} pipes, expected {header_count}. "
            f"Content: {table_lines[i][:80]}"
        )


# ═══════════════════════════════════════════════════════════════════
# C7: Cross-file invariants
# ═══════════════════════════════════════════════════════════════════

def test_c7_existing_contract_tests_still_pass():
    """C7: Existing contract tests MUST still pass (no regression)."""
    import subprocess
    # Use test files that exist on the current branch (not pending-PR files)
    existing_tests = [
        "tests/test_issue_308_contracts.py",
        "tests/test_issue_320_contracts.py",
    ]
    for test_file in existing_tests:
        assert file_exists(test_file), (
            f"Required regression test not found: {test_file}"
        )
        result = subprocess.run(
            [sys.executable, os.path.join(REPO_ROOT, test_file)],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
        )
        assert result.returncode == 0, (
            f"Regression: {test_file} failed after changes.\n"
            f"stdout: {result.stdout[-500:]}\n"
            f"stderr: {result.stderr[-500:]}"
        )


def test_c7_checklist_market_entry_section_preserved():
    """C7: Existing market-entry checklist items MUST still be present."""
    content = read(CHECKLIST)
    assert re.search(r'go.*not now.*pilot only|phased entry', content), \
        "Existing checklist item missing: go/not now/pilot only"
    assert re.search(r'regional hub.*first revenue beachhead.*later expansion', content), \
        "Existing checklist item missing: role separation"
    assert re.search(r'comparison unit.*free-form', content), \
        "Existing checklist item missing: comparison unit"
    assert re.search(r'hard gates.*budget.*product.*compliance', content), \
        "Existing checklist item missing: hard gates"


# ═══════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import inspect

    tests = [
        obj for name, obj in globals().items()
        if name.startswith("test_") and inspect.isfunction(obj)
    ]
    tests.sort(key=lambda f: f.__name__)

    passed = 0
    failed = 0

    for test_fn in tests:
        try:
            test_fn()
            print(f"  ✅ {test_fn.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"  ❌ {test_fn.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"  💥 {test_fn.__name__}: {e}")
            failed += 1

    print(f"\n{'=' * 50}")
    print(f"  Total: {passed + failed}  |  Passed: {passed}  |  Failed: {failed}")
    if failed:
        sys.exit(1)
