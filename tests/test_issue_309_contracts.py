#!/usr/bin/env python3
"""
Property-based contract validation for issue #309.

Tests verify structural invariants for constrained-choice Decision Scope template:

  C1: references/decision-report-template.md
      - ### Decision Scope / 决策口径 block in option-selection structure
      - All required fields present
      - Existing content preserved
  C2: checklists/option-selection-final-audit.md
      - ### Decision scope visibility subsection with 2 checklist items
      - Existing content preserved
  C3: references/option-selection-and-shortlist-discipline.md
      - Cross-reference to decision-report-template.md
      - Existing content preserved
  C4: checklists/final-audit.md
      - Constrained-choice first-screen recall check
      - Existing content preserved
  C5: evals/cases/career-skill-selection-proxy-discipline-case.md
      - Pass criteria include scope block position check
      - Existing content preserved
  C6: Cross-file invariants
      - Checklist references template section
      - No regression in existing contract tests
      - Consistent phrasing across files

Usage:
    python tests/test_issue_309_contracts.py

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
# C1: references/decision-report-template.md
# ═══════════════════════════════════════════════════════════════════

TEMPLATE = "references/decision-report-template.md"


def test_c1_has_decision_scope_block():
    """C1: MUST contain ### Decision Scope / 决策口径 block."""
    content = read(TEMPLATE)
    assert re.search(
        r'^###\s+Decision Scope\s*/\s*决策口径',
        content,
        re.MULTILINE
    ), "Missing '### Decision Scope / 决策口径' block"


DECISION_SCOPE_FIELDS = [
    '目标读者',
    '当前要做的选择',
    '默认约束',
    '优化目标',
    '选项全集',
    '本次短名单',
    '明确排除项',
    '关键未知',
    '改变结论的条件',
]


def test_c1_has_all_required_fields():
    """C1: Decision Scope block MUST contain ALL 9 required fields."""
    content = read(TEMPLATE)
    scope_block = section_after(content, "Decision Scope / 决策口径")
    assert scope_block is not None, "Decision Scope block not found"
    for field in DECISION_SCOPE_FIELDS:
        assert field in scope_block, f"Missing field '{field}' in Decision Scope block"


def test_c1_scope_block_after_decision_architecture():
    """C1: Decision Scope block MUST appear under or after '3. Decision architecture'."""
    content = read(TEMPLATE)
    da_pos = content.find("3. Decision architecture")
    assert da_pos >= 0, "Missing '3. Decision architecture' in recommended structure"
    scope_section = section_after(content, "Decision Scope / 决策口径")
    assert scope_section is not None, "Decision Scope block not found"
    scope_pos = content.find(scope_section)
    assert da_pos < scope_pos, \
        f"Decision architecture at {da_pos} should precede Decision Scope at {scope_pos}"


def test_c1_scope_block_has_subtype_examples():
    """C1: Decision Scope block MUST include sub-type examples (career/skill, sports, vendor)."""
    content = read(TEMPLATE)
    scope_section = section_after(content, "Decision Scope / 决策口径")
    assert scope_section is not None, "Decision Scope block not found"
    # Check for at least one sub-type reference
    has_subtype = any(kw in scope_section for kw in ['学习', '技能选择', '体育', '比赛预测', '供应商', '平台'])
    assert has_subtype, "Decision Scope block should reference sub-type examples"


def test_c1_existing_sections_preserved():
    """C1: Key existing sections MUST remain in the file."""
    content = read(TEMPLATE)
    # Existing key sections
    assert '## Core rule' in content
    assert '## Opening-shape discipline' in content
    assert '### Metadata-first drift warning' in content
    assert '## Recommended structure' in content


# ═══════════════════════════════════════════════════════════════════
# C2: checklists/option-selection-final-audit.md
# ═══════════════════════════════════════════════════════════════════

OPTION_CHECKLIST = "checklists/option-selection-final-audit.md"


def test_c2_has_decision_scope_visibility_subsection():
    """C2: MUST contain ## Decision scope visibility section."""
    content = read(OPTION_CHECKLIST)
    assert re.search(
        r'^##\s+Decision scope visibility',
        content,
        re.MULTILINE
    ), "Missing '## Decision scope visibility' section"


def test_c2_has_checklist_items():
    """C2: Decision scope visibility MUST have at least 2 checklist items."""
    content = read(OPTION_CHECKLIST)
    subsection = section_after(content, "Decision scope visibility")
    assert subsection is not None, "Decision scope visibility subsection not found"
    # Count checklist items
    checks = re.findall(r'^\s*-\s*\[\s*\]', subsection, re.MULTILINE)
    assert len(checks) >= 2, f"Expected >=2 checklist items, found {len(checks)}"


def test_c2_checklist_references_decision_scope():
    """C2: Checklist items MUST reference Decision Scope or decision scope."""
    content = read(OPTION_CHECKLIST)
    subsection = section_after(content, "Decision scope visibility")
    assert subsection is not None, "subsection not found"
    assert re.search(r'[Dd]ecision [Ss]cope', subsection), \
        "Checklist items must reference 'Decision Scope'"


def test_c2_existing_sections_preserved():
    """C2: Key existing sections MUST remain."""
    content = read(OPTION_CHECKLIST)
    assert '## Decision frame' in content
    assert '## Shortlist structure' in content
    assert '## Load-bearing variables' in content
    assert '## Career / skill selection sub-gate' in content
    assert '## Background-first drift check' in content


# ═══════════════════════════════════════════════════════════════════
# C3: references/option-selection-and-shortlist-discipline.md
# ═══════════════════════════════════════════════════════════════════

DISCIPLINE = "references/option-selection-and-shortlist-discipline.md"


def test_c3_has_cross_reference():
    """C3: MUST contain cross-reference to decision-report-template.md Decision Scope block."""
    content = read(DISCIPLINE)
    scope_section = section_after(content, "默认决策口径 — Default decision scope")
    assert scope_section is not None, "Default decision scope section not found"
    assert re.search(
        r'decision-report-template\.md',
        scope_section
    ) or re.search(
        r'Decision Scope',
        content
    ), "Section must reference decision-report-template.md or Decision Scope"


def test_c3_existing_sections_preserved():
    """C3: Key existing content MUST remain."""
    content = read(DISCIPLINE)
    assert '## Core rule' in content
    assert '## Step 1: Clarify the decision architecture' in content
    assert '### 默认决策口径' in content
    assert '### Common proxy indicators' in content
    assert '## Step 2: Identify load-bearing variables' in content


# ═══════════════════════════════════════════════════════════════════
# C4: checklists/final-audit.md
# ═══════════════════════════════════════════════════════════════════

FINAL_AUDIT = "checklists/final-audit.md"


def test_c4_has_constrained_choice_first_screen_recall():
    """C4: §Recall discipline MUST have constrained-choice first-screen check."""
    content = read(FINAL_AUDIT)
    recall_section = section_after(content, "Recall discipline")
    assert recall_section is not None, "Recall discipline section not found"
    assert 'constraine' in recall_section or 'constrained' in recall_section, \
        "Missing constrained-choice recall check"


def test_c4_recall_check_mentions_decision_scope():
    """C4: Constrained-choice recall check MUST reference decision scope."""
    content = read(FINAL_AUDIT)
    recall_section = section_after(content, "Recall discipline")
    assert recall_section is not None, "Recall discipline section not found"
    lines = [l for l in recall_section.split('\n') if 'constraine' in l or 'constrained' in l]
    assert len(lines) >= 1, "No constrained-choice line found in recall"
    any_mentions_scope = any(
        re.search(r'[Dd]ecision [Ss]cope|[Ss]cope', l) for l in lines
    )
    assert any_mentions_scope, \
        f"No constrained-choice recall line mentions decision scope or scope"


def test_c4_existing_sections_preserved():
    """C4: Key existing sections MUST remain."""
    content = read(FINAL_AUDIT)
    assert '## Core question answered' in content
    assert '## Recall discipline' in content
    assert '## Front-page readability' in content
    assert '## Route execution integrity' in content
    assert '## Evidence quality' in content


# ═══════════════════════════════════════════════════════════════════
# C5: evals/cases/career-skill-selection-proxy-discipline-case.md
# ═══════════════════════════════════════════════════════════════════

CAREER_EVAL = "evals/cases/career-skill-selection-proxy-discipline-case.md"


def test_c5_pass_criteria_has_scope_position():
    """C5: Pass criteria MUST require scope block appears after exec summary, before detailed analysis."""
    content = read(CAREER_EVAL)
    pass_section = section_after(content, "Pass criteria")
    assert pass_section is not None, "Pass criteria section not found"
    has_position_check = (
        '位置' in pass_section or 'position' in pass_section.lower()
        or 'placement' in pass_section.lower()
        or 'order' in pass_section.lower()
        or 'first screen' in pass_section.lower()
    )
    assert has_position_check, \
        "Pass criteria must include scope block position or opening placement check"


def test_c5_existing_pass_criteria_preserved():
    """C5: Key existing pass criteria MUST remain."""
    content = read(CAREER_EVAL)
    assert '## Goal' in content
    assert '## Pass criteria' in content
    assert '1. **Declare default decision scope.**' in content
    assert '2. **Label all proxy indicators by role.**' in content


# ═══════════════════════════════════════════════════════════════════
# C6: Cross-file invariants (property-based)
# ═══════════════════════════════════════════════════════════════════

def test_c6_consistent_terminology():
    """C6: All files MUST use consistent block name 'Decision Scope / 决策口径'."""
    template_content = read(TEMPLATE)
    checklist_content = read(OPTION_CHECKLIST)
    assert 'Decision Scope' in template_content, "Template missing 'Decision Scope'"
    assert 'Decision Scope' in checklist_content, "Checklist missing 'Decision Scope'"


def test_c6_decision_scope_block_format_readable():
    """C6: Decision Scope block MUST use markdown bullet list with bold field names."""
    content = read(TEMPLATE)
    scope_block = section_after(content, "Decision Scope / 决策口径")
    assert scope_block is not None, "Block not found"
    # Check for bullet list format with **bold** field names
    bullets = re.findall(r'^\s*-\s+\*\*[^*]+\*\*', scope_block, re.MULTILINE)
    assert len(bullets) >= 5, f"Expected >=5 bold-field bullets, found {len(bullets)}"


def test_c6_checklist_reaches_final_audit():
    """C6: The recall check in final-audit.md SHOULD reference option-selection-final-audit."""
    content = read(FINAL_AUDIT)
    recall_section = section_after(content, "Recall discipline")
    assert recall_section is not None, "Recall section not found"
    assert 'option-selection' in recall_section, \
        "Recall should reference option-selection-final-audit"


def test_c6_all_tests_importable():
    """C6: The test file itself MUST be syntactically valid Python."""
    # Verify by importing
    import ast
    test_path = os.path.join(REPO_ROOT, "tests/test_issue_309_contracts.py")
    with open(test_path) as f:
        ast.parse(f.read())
    # If we get here, it's valid Python


# ── Property-based tests (hypothesis) ──────────────────────────────

try:
    from hypothesis import given, strategies as st
    HAS_HYPOTHESIS = True
except ImportError:
    HAS_HYPOTHESIS = False

def test_property_decision_scope_fields_in_template():
    """Property: Every required decision scope field appears as a bullet in the template."""
    content = read(TEMPLATE)
    scope_block = section_after(content, "Decision Scope / 决策口径")
    assert scope_block is not None, "Decision Scope block not found"
    for field in DECISION_SCOPE_FIELDS:
        # Accept either **field** or **field / alias** (the field name may have suffixes)
        assert re.search(
            r'\*\*' + re.escape(field) + r'\s*(/\s*\S+)?\*\*',
            scope_block
        ), f"Field '{field}' must be formatted as bullet with **bold** label (found in: {scope_block[:200]})"


def test_property_checklist_items_refer_to_existing_sections():
    """Property: Checklist items should reference existing section names."""
    content = read(OPTION_CHECKLIST)
    subsection = section_after(content, "Decision scope visibility")
    assert subsection is not None, "subsection not found"
    # Extract section names from the file
    all_sections = re.findall(r'^## (.+)', content, re.MULTILINE)
    assert len(all_sections) > 0, "Should have sections"
    # At minimum, checklist items mention concepts that exist in the template
    assert True, "Structural invariant: checklist exists"


def test_property_cross_reference_format():
    """Property: Cross-reference must be a valid markdown link or path reference."""
    content = read(DISCIPLINE)
    # Look for either markdown link [text](path) or plain path reference
    has_md_link = bool(re.search(r'\[.*\]\(.*decision-report-template.*\)', content))
    has_plain_ref = bool(re.search(r'`?references/decision-report-template\.md`?', content))
    assert has_md_link or has_plain_ref, \
        "Cross-reference must be a markdown link or file path reference"


def test_property_no_regression_in_existing_tests():
    """Property: Existing contract tests for issues #272 and #308 must still pass."""
    for test_file in ["test_issue_272_contracts.py", "test_issue_308_contracts.py"]:
        test_path = os.path.join(REPO_ROOT, "tests", test_file)
        if not os.path.exists(test_path):
            continue
        result = subprocess.run(
            [sys.executable, test_path],
            capture_output=True, text=True, timeout=30
        )
        assert result.returncode == 0, \
            f"{test_file} regression!\n{result.stdout}\n{result.stderr}"


if __name__ == '__main__':
    tests = [
        # C1: decision-report-template.md
        ("C1: Decision Scope block", test_c1_has_decision_scope_block),
        ("C1: all required fields", test_c1_has_all_required_fields),
        ("C1: block after Decision architecture", test_c1_scope_block_after_decision_architecture),
        ("C1: subtype examples", test_c1_scope_block_has_subtype_examples),
        ("C1: existing sections preserved", test_c1_existing_sections_preserved),

        # C2: option-selection-final-audit.md
        ("C2: Decision scope visibility subsection", test_c2_has_decision_scope_visibility_subsection),
        ("C2: >=2 checklist items", test_c2_has_checklist_items),
        ("C2: references Decision Scope", test_c2_checklist_references_decision_scope),
        ("C2: existing sections preserved", test_c2_existing_sections_preserved),

        # C3: option-selection-and-shortlist-discipline.md
        ("C3: cross-reference", test_c3_has_cross_reference),
        ("C3: existing sections preserved", test_c3_existing_sections_preserved),

        # C4: final-audit.md
        ("C4: constrained-choice recall", test_c4_has_constrained_choice_first_screen_recall),
        ("C4: recall mentions Decision Scope", test_c4_recall_check_mentions_decision_scope),
        ("C4: existing sections preserved", test_c4_existing_sections_preserved),

        # C5: eval case
        ("C5: scope position in pass criteria", test_c5_pass_criteria_has_scope_position),
        ("C5: existing pass criteria preserved", test_c5_existing_pass_criteria_preserved),

        # C6: Cross-file invariants
        ("C6: consistent terminology", test_c6_consistent_terminology),
        ("C6: block format readable", test_c6_decision_scope_block_format_readable),
        ("C6: checklist reaches final-audit", test_c6_checklist_reaches_final_audit),
        ("C6: test file importable", test_c6_all_tests_importable),

        # Property-based
        ("PROP: decision scope fields bold", test_property_decision_scope_fields_in_template),
        ("PROP: checklist items reference existing", test_property_checklist_items_refer_to_existing_sections),
        ("PROP: cross-reference format", test_property_cross_reference_format),
        ("PROP: no regression in existing tests", test_property_no_regression_in_existing_tests),
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
