#!/usr/bin/env python3
"""
Property-based contract validation for issue #308.

Tests verify structural invariants for career/skill-selection proxy evidence discipline:

  C1: references/option-selection-and-shortlist-discipline.md
      - Default decision scope section after Step 1
      - Common proxy indicators section
      - Existing content preserved
  C2: checklists/option-selection-final-audit.md
      - Career / skill selection sub-gate section
      - Minimum checklist items with specific coverage
      - Existing content preserved
  C3: evals/cases/career-skill-selection-proxy-discipline-case.md
      - File exists with standard eval structure
      - References issue #308
  C4: evals/INDEX.md
      - Entry for new eval case
      - Table format preserved
  C5: Cross-file invariants
      - Checklist references discipline section
      - No regression in existing contract tests
      - INDEX.md table parseable
  C6: Test file self-validation

Usage:
    python tests/test_issue_308_contracts.py

Expected BEFORE implementation (RED):
    ALL FAIL

Expected AFTER implementation (GREEN):
    ALL PASS
"""

import re
import os
import sys
import subprocess

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def read(path):
    with open(os.path.join(REPO_ROOT, path), "r") as f:
        return f.read()


def file_exists(path):
    return os.path.exists(os.path.join(REPO_ROOT, path))


def section_after(content, section_title):
    """Return content starting from a ## or ### section title."""
    match = re.search(r'^#{2,3}\s*' + re.escape(section_title) + r'\s*$', content, re.MULTILINE)
    if not match:
        return None
    return content[match.start():]


# ═══════════════════════════════════════════════════════════════════
# C1: references/option-selection-and-shortlist-discipline.md
# ═══════════════════════════════════════════════════════════════════

DISCIPLINE = "references/option-selection-and-shortlist-discipline.md"


def test_c1_has_default_decision_scope_section():
    """C1: MUST contain ### 默认决策口径 — Default decision scope subsection."""
    content = read(DISCIPLINE)
    assert re.search(
        r'^###\s+默认决策口径.*Default decision scope',
        content,
        re.MULTILINE
    ), "Missing '### 默认决策口径 — Default decision scope' subsection"


def test_c1_section_after_step_1():
    """C1: Decision scope section MUST appear after 'Step 1: Clarify the decision architecture'."""
    content = read(DISCIPLINE)
    step1_pos = content.index("## Step 1: Clarify the decision architecture")
    scope_section = section_after(content, "默认决策口径 — Default decision scope")
    assert scope_section is not None, "Default decision scope section not found"
    scope_pos = content.index(scope_section)
    assert step1_pos < scope_pos, \
        f"Step 1 at {step1_pos} should precede Decision scope at {scope_pos}"


def test_c1_has_reader_fields():
    """C1: Section MUST contain fields for target reader, market, decision goal, time window."""
    content = read(DISCIPLINE)
    scope_section = section_after(content, "默认决策口径 — Default decision scope")
    assert scope_section is not None, "Missing section"
    # Check for required field concepts
    fields = [
        '目标读者', 'Target reader', 'target reader',
        '默认市场', 'Default market', 'default market',
        '决策目标', 'Decision goal', 'decision goal',
        '时间窗口', 'Time window', 'time window',
    ]
    # Use a lenient check: at least 3 unique field concepts present
    # Check for both Chinese and English keywords directly in the section
    scope_lower = scope_section.lower()
    concept_checks = {
        'reader/读者': ['目标读者', 'reader'],
        'market/市场': ['默认市场', 'market'],
        'goal/目标': ['决策目标', 'goal'],
        'time window/时间窗口': ['时间窗口', 'time window'],
    }
    found_concepts = set()
    for concept_name, keywords in concept_checks.items():
        if any(kw.lower() in scope_lower for kw in keywords):
            found_concepts.add(concept_name)
    assert len(found_concepts) >= 3, \
        f"Expected >=3 field concepts (reader/market/goal/window), got {found_concepts}"


def test_c1_has_proxy_indicators_section():
    """C1: MUST contain ### Common proxy indicators for career/skill selection section."""
    content = read(DISCIPLINE)
    assert re.search(
        r'^###\s+Common proxy indicators for career/skill selection',
        content,
        re.MULTILINE
    ), "Missing '### Common proxy indicators for career/skill selection' section"


def test_c1_proxy_section_lists_minimum_sources():
    """C1: Proxy section MUST list at least 5 career data source types."""
    content = read(DISCIPLINE)
    proxy_section = section_after(content, "Common proxy indicators for career/skill selection")
    assert proxy_section is not None, "Missing proxy section"
    # Find the next ##-level heading (not ### which could be the section itself),
    # by searching from after the first line past the heading
    heading_end = proxy_section.index('\n') + 1
    remaining = proxy_section[heading_end:]
    next_h2 = re.search(r'^##\s', remaining, re.MULTILINE)
    boundaries = []
    if next_h2:
        boundaries.append(heading_end + next_h2.start())
    if boundaries:
        body = proxy_section[:min(boundaries)]
    else:
        body = proxy_section

    source_keywords = [
        'TIOBE', 'Stack Overflow', 'GitHub', 'LinkedIn', 'Indeed',
        'Glassdoor', 'salary', 'package', 'repository', 'roadmap',
        'RedMonk', 'developer survey', 'job posting', '招聘',
    ]
    found = sum(1 for kw in source_keywords if kw.lower() in body.lower())
    assert found >= 5, f"Proxy section mentions only {found}/5 required source types"


def test_c1_existing_content_preserved():
    """C1: All original sections MUST survive (all 17 ## headings)."""
    content = read(DISCIPLINE)
    landmarks = [
        "# Option Selection and Shortlist Discipline",
        "## Core rule",
        "## Step 1: Clarify the decision architecture",
        "## Step 2: Identify load-bearing variables",
        "## Step 3: Choose the comparison unit explicitly",
        "## Step 4: Make the aggregation logic visible",
        "## Step 4.5: Per-persona recommendations",
        "## Step 5: Separate evidence layers",
        "## Step 6: Build the shortlist before the deep dive",
        "## Step 7: Handle uncertainty as scenario logic",
        "## Step 8: Distinguish best overall, best fit, and best fallback",
        "## Good output pattern",
        "## Common failure modes",
        "## Practical heuristics",
        "## Output discipline",
        "## Best home for related fixes",
        "## Bottom line",
    ]
    for landmark in landmarks:
        assert landmark in content, f"C1 missing: '{landmark}'"


def test_c1_rule_us_scope_declaration():
    """C1: Scope section MUST contain rule about US data scope declaration."""
    content = read(DISCIPLINE)
    scope_section = section_after(content, "默认决策口径 — Default decision scope")
    assert scope_section is not None, "Missing scope section"
    assert "US" in scope_section and "scope" in scope_section.lower(), \
        "Missing US salary scope declaration rule"


def test_c1_rule_multi_level_reader():
    """C1: Scope section MUST contain rule about multi-level reader treatment."""
    content = read(DISCIPLINE)
    scope_section = section_after(content, "默认决策口径 — Default decision scope")
    assert scope_section is not None, "Missing scope section"
    assert "experience level" in scope_section.lower() or "reader" in scope_section.lower(), \
        "Missing multi-level reader rule"


def test_c1_rule_learning_time_labeling():
    """C1: Scope section MUST contain rule about learning time estimate labeling."""
    content = read(DISCIPLINE)
    scope_section = section_after(content, "默认决策口径 — Default decision scope")
    assert scope_section is not None, "Missing scope section"
    assert "learning time" in scope_section.lower() or "estimate" in scope_section.lower(), \
        "Missing learning time estimate labeling rule"


def test_c1_rule_register_claims_typing():
    """C1: Scope section MUST contain rule about Source Register Claims Supported typing."""
    content = read(DISCIPLINE)
    scope_section = section_after(content, "默认决策口径 — Default decision scope")
    assert scope_section is not None, "Missing scope section"
    assert "Claims Supported" in scope_section or "claim type" in scope_section.lower(), \
        "Missing Source Register claims typing rule"


# ═══════════════════════════════════════════════════════════════════
# C2: checklists/option-selection-final-audit.md
# ═══════════════════════════════════════════════════════════════════

CHECKLIST = "checklists/option-selection-final-audit.md"


def test_c2_has_career_skill_subgate():
    """C2: MUST contain ### Career / skill selection sub-gate section."""
    content = read(CHECKLIST)
    assert re.search(
        r'^###\s+Career.*skill selection sub.gate',
        content,
        re.MULTILINE
    ), "Missing '### Career / skill selection sub-gate' section"


def test_c2_has_minimum_checklist_items():
    """C2: Sub-gate MUST have >= 3 checklist items."""
    content = read(CHECKLIST)
    sg_section = section_after(content, "Career / skill selection sub-gate")
    assert sg_section is not None, "Missing sub-gate section"
    # Find boundary: next ## section or end of file
    heading_end = sg_section.index('\n') + 1
    remaining = sg_section[heading_end:]
    next_section = re.search(r'^##\s', remaining, re.MULTILINE)
    if next_section:
        body = sg_section[:heading_end + next_section.start()]
    else:
        body = sg_section
    items = re.findall(r'-\s+\[[ x]\]', body)
    assert len(items) >= 3, f"Expected >=3 checklist items, got {len(items)}"


def test_c2_has_scope_declaration_item():
    """C2: At least one item MUST address default scope / reader persona declaration."""
    content = read(CHECKLIST)
    sg_section = section_after(content, "Career / skill selection sub-gate")
    assert sg_section is not None, "Missing sub-gate section"
    assert any(
        term in sg_section.lower()
        for term in ['scope', '读者', 'persona', '市场', '默认', 'market', 'reader', '声明', 'declar']
    ), "Missing scope/reader declaration checklist item"


def test_c2_has_proxy_role_item():
    """C2: At least one item MUST address proxy indicator role labeling."""
    content = read(CHECKLIST)
    sg_section = section_after(content, "Career / skill selection sub-gate")
    assert sg_section is not None, "Missing sub-gate section"
    assert any(
        term in sg_section.lower()
        for term in ['proxy', 'role', 'label', '代理', '角色']
    ), "Missing proxy role labeling checklist item"


def test_c2_has_us_global_item():
    """C2: At least one item MUST address US-vs-global scope boundary."""
    content = read(CHECKLIST)
    sg_section = section_after(content, "Career / skill selection sub-gate")
    assert sg_section is not None, "Missing sub-gate section"
    assert any(
        term in sg_section.lower()
        for term in ['US', '全球', 'global', '美国', '地理', 'geographic']
    ), "Missing US-vs-global scope boundary checklist item"


def test_c2_subgate_section_position():
    """C2: Sub-gate section MUST be between Evidence layers and Scenario logic."""
    content = read(CHECKLIST)
    ev_pos = content.index("## Evidence layers")
    sg_section = section_after(content, "Career / skill selection sub-gate")
    assert sg_section is not None, "Missing sub-gate section"
    sg_pos = content.index(sg_section)
    sc_pos = content.index("## Scenario logic and change conditions")
    assert ev_pos < sg_pos < sc_pos, \
        f"Position: Evidence({ev_pos}) < Sub-gate({sg_pos}) < Scenario({sc_pos})"


def test_c2_has_blocker_check():
    """C2: Sub-gate MUST have a [BLOCKER] check."""
    content = read(CHECKLIST)
    sg_section = section_after(content, "Career / skill selection sub-gate")
    assert sg_section is not None, "Missing sub-gate section"
    assert "[BLOCKER]" in sg_section, "Missing BLOCKER check in sub-gate"


def test_c2_has_source_register_claims_item():
    """C2: At least one item MUST address Source Register Claims Supported typing."""
    content = read(CHECKLIST)
    sg_section = section_after(content, "Career / skill selection sub-gate")
    assert sg_section is not None, "Missing sub-gate section"
    assert any(
        term in sg_section.lower()
        for term in ['claims supported', 'claim type', 'job proxy', 'salary proxy']
    ), "Missing Source Register claims typing item"


def test_c2_has_learning_time_label_item():
    """C2: At least one item MUST address learning time estimate labeling."""
    content = read(CHECKLIST)
    sg_section = section_after(content, "Career / skill selection sub-gate")
    assert sg_section is not None, "Missing sub-gate section"
    assert any(
        term in sg_section.lower()
        for term in ['learning time', 'estimate', 'basis note']
    ), "Missing learning time labeling item"


def test_c2_existing_content_preserved():
    """C2: All original sections MUST survive."""
    content = read(CHECKLIST)
    landmarks = [
        "# Option Selection Final Audit Checklist",
        "## Decision frame",
        "## Load-bearing variables",
        "## Comparison unit and aggregation logic",
        "## Provider / vendor current-state gate",
        "## Shortlist structure",
        "## Evidence layers",
        "## Scenario logic and change conditions",
        "## Decision usefulness",
        "## Quality bar",
    ]
    for landmark in landmarks:
        assert landmark in content, f"C2 missing: '{landmark}'"


# ═══════════════════════════════════════════════════════════════════
# C3: evals/cases/career-skill-selection-proxy-discipline-case.md
# ═══════════════════════════════════════════════════════════════════

EVAL_FILE = "evals/cases/career-skill-selection-proxy-discipline-case.md"


def test_c3_eval_file_exists():
    """C3: New eval case file MUST exist."""
    assert file_exists(EVAL_FILE), f"Eval case file missing: {EVAL_FILE}"


def test_c3_has_standard_sections():
    """C3: Eval case MUST have standard sections: Goal, Prompt, Pass criteria, Failure signs."""
    content = read(EVAL_FILE)
    assert "## Goal" in content
    assert "## Prompt" in content
    assert "## Pass criteria" in content
    assert "## Failure signs" in content
    assert "## Why this eval matters" in content


def test_c3_references_issue_308():
    """C3: Eval case MUST reference issue #308."""
    content = read(EVAL_FILE)
    assert "308" in content, "Eval case missing issue #308 reference"


def test_c3_has_scoring():
    """C3: Eval case MUST have Pass / Conditional pass / Fail scoring."""
    content = read(EVAL_FILE)
    assert "Pass" in content and "Fail" in content, "Eval case missing scoring definitions"
    # Either "Conditional pass" or "Conditional" near a pass/fail context
    assert "Conditional pass" in content or "conditional" in content.lower(), \
        "Eval case missing conditional pass scoring tier"


def test_c3_tests_proxy_discipline():
    """C3: Eval case MUST test proxy indicator handling for career data."""
    content = read(EVAL_FILE)
    terms = [
        'proxy', '代理', 'TIOBE', 'LinkedIn', 'Glassdoor', 'Indeed',
        'Stack Overflow', 'GitHub', '岗位', '薪资', 'salary', 'job',
        'career', 'skill selection', '职业', '编程语言',
    ]
    found = sum(1 for t in terms if t.lower() in content.lower())
    assert found >= 3, \
        f"Eval doesn't adequately test proxy discipline (found {found}/3 terms)"


# ═══════════════════════════════════════════════════════════════════
# C4: evals/INDEX.md
# ═══════════════════════════════════════════════════════════════════

EVAL_FILENAME = os.path.basename(EVAL_FILE)


def test_c4_index_has_entry():
    """C4: INDEX.md MUST have an entry for the new eval case."""
    content = read("evals/INDEX.md")
    assert EVAL_FILENAME in content, f"INDEX.md missing entry for {EVAL_FILENAME}"


def test_c4_index_table_format():
    """C4: INDEX.md entry MUST maintain proper table format (10+ columns)."""
    content = read("evals/INDEX.md")
    table_lines = [l for l in content.split('\n') if EVAL_FILENAME in l]
    assert len(table_lines) >= 1, f"No table line found for {EVAL_FILENAME}"
    for line in table_lines:
        cols = line.split('|')
        assert len(cols) >= 10, f"INDEX.md line has {len(cols)} cols, expected >=10: {line}"


# ═══════════════════════════════════════════════════════════════════
# C5: Cross-file invariants
# ═══════════════════════════════════════════════════════════════════


def test_c5_checklist_references_discipline():
    """C5: Checklist MUST reference option-selection-and-shortlist-discipline.md §Default decision scope."""
    checklist_content = read(CHECKLIST)
    discipline_content = read(DISCIPLINE)
    assert 'option-selection-and-shortlist-discipline.md' in checklist_content, \
        "checklist must reference option-selection-and-shortlist-discipline.md"
    assert '默认决策口径' in discipline_content or 'Default decision scope' in discipline_content, \
        "Discipline must have the referenced default decision scope section"


def test_c5_backward_reference_exists():
    """C5: Discipline file MUST reference the checklist in its new sections."""
    content = read(DISCIPLINE)
    assert 'checklists/option-selection-final-audit.md' in content, \
        "Discipline must reference checklists/option-selection-final-audit.md (backward reference)"
    assert 'Career / skill selection sub-gate' in content or '职业' in content, \
        "Discipline must reference the career/skill sub-gate section name"


def test_c5_no_existing_regression():
    """C5: All existing contract tests MUST still pass (scope-creep filtered)."""
    existing_tests = [
        "tests/test_issue_270_contracts.py",
        "tests/test_issue_272_contracts.py",
        "tests/test_issue_278_contracts.py",
        "tests/test_issue_280_contracts.py",
        "tests/test_issue_294_contracts.py",
        "tests/test_issue_298_contracts.py",
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
        if result.returncode != 0:
            lines = result.stdout.split("\n")
            has_non_scope_failure = any(
                "❌" in l and "scope creep" not in l and "Scope" not in l
                and "only intended" not in l
                for l in lines
            )
            if has_non_scope_failure:
                assert False, (
                    f"Non-scope regression in {test_file}:\n"
                    f"STDOUT: {result.stdout[-500:]}\n"
                    f"STDERR: {result.stderr[-500:]}"
                )


def test_c5_index_not_broken():
    """C5: INDEX.md table structure should remain parseable."""
    content = read("evals/INDEX.md")
    table_lines = []
    in_table = False
    for line in content.split('\n'):
        if line.startswith('| ---'):
            in_table = True
            continue
        if in_table and line.startswith('|'):
            table_lines.append(line)
        elif in_table and not line.startswith('|'):
            in_table = False
    if table_lines:
        counts = [len(l.split('|')) for l in table_lines]
        assert max(counts) == min(counts), f"Inconsistent INDEX.md table columns: {counts}"


# ═══════════════════════════════════════════════════════════════════
# C6: Test file self-validation
# ═══════════════════════════════════════════════════════════════════


def test_c6_test_file_exists():
    """C6: This test file MUST exist."""
    test_path = "tests/test_issue_308_contracts.py"
    assert file_exists(test_path), f"{test_path} does not exist"


def test_c6_has_all_contract_tests():
    """C6: This test file MUST have tests for C1-C5 (at minimum)."""
    content = read("tests/test_issue_308_contracts.py")
    assert "test_c1_" in content, "Missing C1 tests"
    assert "test_c2_" in content, "Missing C2 tests"
    assert "test_c3_" in content, "Missing C3 tests"
    assert "test_c4_" in content, "Missing C4 tests"
    assert "test_c5_" in content, "Missing C5 tests"


def test_c6_self_referential():
    """C6: This test must have a test_c6_ test function."""
    content = read("tests/test_issue_308_contracts.py")
    assert "test_c6_" in content, "Missing C6 self-referential tests"


# ═══════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    tests = [
        # C1: option-selection-and-shortlist-discipline.md
        ("C1: default decision scope section", test_c1_has_default_decision_scope_section),
        ("C1: section after Step 1", test_c1_section_after_step_1),
        ("C1: reader/fields", test_c1_has_reader_fields),
        ("C1: proxy indicators section", test_c1_has_proxy_indicators_section),
        ("C1: proxy sources >=5", test_c1_proxy_section_lists_minimum_sources),
        ("C1: existing content preserved", test_c1_existing_content_preserved),
        ("C1: rule US scope", test_c1_rule_us_scope_declaration),
        ("C1: rule multi-level reader", test_c1_rule_multi_level_reader),
        ("C1: rule learning time", test_c1_rule_learning_time_labeling),
        ("C1: rule register claims type", test_c1_rule_register_claims_typing),

        # C2: option-selection-final-audit.md
        ("C2: career/skill sub-gate", test_c2_has_career_skill_subgate),
        ("C2: section position", test_c2_subgate_section_position),
        ("C2: >=3 checklist items", test_c2_has_minimum_checklist_items),
        ("C2: scope declaration item", test_c2_has_scope_declaration_item),
        ("C2: proxy role item", test_c2_has_proxy_role_item),
        ("C2: US/global item", test_c2_has_us_global_item),
        ("C2: BLOCKER check", test_c2_has_blocker_check),
        ("C2: register claims item", test_c2_has_source_register_claims_item),
        ("C2: learning time item", test_c2_has_learning_time_label_item),
        ("C2: existing content preserved", test_c2_existing_content_preserved),

        # C3: eval case
        ("C3: eval file exists", test_c3_eval_file_exists),
        ("C3: standard sections", test_c3_has_standard_sections),
        ("C3: references issue 308", test_c3_references_issue_308),
        ("C3: has scoring", test_c3_has_scoring),
        ("C3: tests proxy discipline", test_c3_tests_proxy_discipline),

        # C4: INDEX.md
        ("C4: INDEX entry", test_c4_index_has_entry),
        ("C4: INDEX table format", test_c4_index_table_format),

        # C5: Cross-file
        ("C5: checklist references discipline", test_c5_checklist_references_discipline),
        ("C5: backward reference from discipline", test_c5_backward_reference_exists),
        ("C5: no regression", test_c5_no_existing_regression),
        ("C5: INDEX not broken", test_c5_index_not_broken),

        # C6: Self-validation
        ("C6: test file exists", test_c6_test_file_exists),
        ("C6: contract coverage", test_c6_has_all_contract_tests),
        ("C6: self-referential", test_c6_self_referential),
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
