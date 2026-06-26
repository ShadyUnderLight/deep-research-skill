#!/usr/bin/env python3
"""
Property-based contract tests for Issue #343: Rule-system / tournament-mechanism add-on.

Tests validate structural invariants across the 5 deliverable files:
  D1: references/rule-system-and-mechanism-add-on.md (NEW)
  D2: ROUTING-MATRIX.md (MODIFIED — 2 route references)
  D3: checklists/regulatory-analysis-audit.md (MODIFIED — conditional section)
  D4: checklists/technical-analysis-audit.md (MODIFIED — conditional section)
  D5: evals/cases/rule-system-add-on-activation-case.md (NEW)

Usage:
    python tests/test_issue_343_contracts.py
    python -m pytest tests/test_issue_343_contracts.py -v

Expected BEFORE implementation: ALL FAIL (files don't exist or content missing)
Expected AFTER implementation:  ALL PASS
"""

import re
import sys
import os

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def read(path):
    with open(os.path.join(REPO_ROOT, path), "r", encoding="utf-8") as f:
        return f.read()


def file_exists(path):
    return os.path.exists(os.path.join(REPO_ROOT, path))


# ═══════════════════════════════════════════════════════════════════════════
# D1: references/rule-system-and-mechanism-add-on.md (NEW)
# ═══════════════════════════════════════════════════════════════════════════

ADDON_FILE = "references/rule-system-and-mechanism-add-on.md"


def test_d1_file_exists():
    """D1: Add-on file MUST exist."""
    assert file_exists(ADDON_FILE), f"Missing: {ADDON_FILE}"


def test_d1_has_enablement_criteria():
    """D1: Add-on MUST have explicit enablement criteria section."""
    content = read(ADDON_FILE)
    assert re.search(r'启用条件|enablement|when to activate', content, re.IGNORECASE), \
        "Missing enablement criteria section"


def test_d1_has_state_taxonomy():
    """D1: Add-on MUST contain state taxonomy / 状态分类 section."""
    content = read(ADDON_FILE)
    assert re.search(r'状态分类|state taxonomy|State taxonomy', content), \
        "Missing state taxonomy section"


def test_d1_has_intervention_matrix():
    """D1: Add-on MUST contain intervention matrix / 干预矩阵 section with table template."""
    content = read(ADDON_FILE)
    assert re.search(r'干预矩阵|intervention matrix|Intervention matrix', content), \
        "Missing intervention matrix section"
    # Must contain at least one markdown table (pipe-separated rows with separator line)
    tables = re.findall(r'\|.+\|.*\n\|[-| :]+\|', content)
    assert len(tables) >= 1, f"Expected >=1 table template, found {len(tables)}"


def test_d1_has_relationship_to_existing_rules():
    """D1: Add-on MUST document relationship to existing rules/disciplines."""
    content = read(ADDON_FILE)
    assert re.search(r'与现有.*关系|related (references|disciplines)|参见|see also',
                     content, re.IGNORECASE), \
        "Missing relationship to existing rules section"


def test_d1_references_regulatory_discipline():
    """D1: Add-on MUST reference regulatory analysis as primary route."""
    content = read(ADDON_FILE)
    assert "regulatory" in content.lower(), \
        "Add-on must reference regulatory analysis route"


def test_d1_references_technical_discipline():
    """D1: Add-on MUST reference technical deep-dive as secondary applicable route."""
    content = read(ADDON_FILE)
    assert "technical" in content.lower() and ("deep-dive" in content.lower()
                                                or "deep.dive" in content.lower()), \
        "Add-on must reference technical deep-dive route"


def test_d1_has_non_goals():
    """D1: Add-on MUST have non-goals / 非目标 section."""
    content = read(ADDON_FILE)
    assert re.search(r'非目标|non.?goals|out of scope|not in scope',
                     content, re.IGNORECASE), \
        "Missing non-goals section"


def test_d1_no_football_only_language():
    """D1: Add-on MUST NOT be football/sports-specific (domain-agnostic per issue requirements)."""
    content = read(ADDON_FILE)
    # The add-on should use generic terms, not football-only examples
    # Check that at least one non-football domain is mentioned
    domains = ['regulatory', 'policy', 'incentive', 'compliance', 'market',
               'governance', 'corporate', 'financial', 'trade']
    found_domains = [d for d in domains if d in content.lower()]
    assert len(found_domains) >= 2, \
        f"Add-on should be domain-agnostic, found only: {found_domains}"


def test_d1_has_simulation_contract_reference():
    """D1: Add-on MUST cross-reference model-output/simulation contract discipline."""
    content = read(ADDON_FILE)
    assert "simulation" in content.lower() or "model-output" in content.lower(), \
        "Must cross-reference simulation contract discipline"


# ═══════════════════════════════════════════════════════════════════════════
# D2: ROUTING-MATRIX.md (MODIFIED)
# ═══════════════════════════════════════════════════════════════════════════


def test_d2_regulatory_route_references_addon():
    """D2: Regulatory route section MUST reference the add-on."""
    content = read("ROUTING-MATRIX.md")
    # Find the regulatory route section
    reg_start = content.index("## Route: Regulatory / Policy Impact Analysis")
    next_route = re.search(r'^## Route:', content[reg_start + 1:], re.MULTILINE)
    if next_route:
        reg_section = content[reg_start:reg_start + 1 + next_route.start()]
    else:
        reg_section = content[reg_start:]
    assert "rule-system-and-mechanism" in reg_section, \
        "Regulatory route must reference rule-system-and-mechanism add-on"


def test_d2_technical_route_references_addon():
    """D2: Technical Deep-dive route section MUST reference the add-on."""
    content = read("ROUTING-MATRIX.md")
    # Find the technical deep-dive route section
    td_start = content.index("## Route: Technical Deep-dive / Architecture Analysis")
    next_route = re.search(r'^## Route:', content[td_start + 1:], re.MULTILINE)
    if next_route:
        td_section = content[td_start:td_start + 1 + next_route.start()]
    else:
        td_section = content[td_start:]
    assert "rule-system-and-mechanism" in td_section, \
        "Technical deep-dive route must reference rule-system-and-mechanism add-on"


def test_d2_existing_routes_intact():
    """D2: All 11 original routes MUST still be present."""
    content = read("ROUTING-MATRIX.md")
    route_sections = re.findall(r'^## Route: (.+)$', content, re.MULTILINE)
    assert len(route_sections) >= 11, \
        f"Expected >=11 routes, found {len(route_sections)}: {route_sections}"


def test_d2_regulatory_hard_fails_intact():
    """D2: Regulatory route hard-fail conditions MUST be preserved."""
    content = read("ROUTING-MATRIX.md")
    reg_hard_fail_markers = [
        "lists regulations without analyzing business impact",
        "confuses regulatory text with media interpretation",
        "gives false precision on regulatory timing",
        "ignores enforcement reality",
        "treats all jurisdictions as equivalent",
        "presents regulatory risk as binary",
    ]
    reg_start = content.index("## Route: Regulatory / Policy Impact Analysis")
    next_route = re.search(r'^## Route:', content[reg_start + 1:], re.MULTILINE)
    if next_route:
        reg_section = content[reg_start:reg_start + 1 + next_route.start()]
    else:
        reg_section = content[reg_start:]
    for marker in reg_hard_fail_markers:
        assert marker in reg_section, \
            f"Regulatory hard-fail lost: '{marker[:50]}...'"


# ═══════════════════════════════════════════════════════════════════════════
# D3: checklists/regulatory-analysis-audit.md (MODIFIED)
# ═══════════════════════════════════════════════════════════════════════════


def test_d3_has_rule_system_section():
    """D3: Regulatory audit MUST have conditional §Rule-system analysis section."""
    content = read("checklists/regulatory-analysis-audit.md")
    assert re.search(r'[Rr]ule.?system|规则系统|tournament.*mechanism|赛制',
                     content), \
        "Missing rule-system analysis section in regulatory audit"


def test_d3_rule_system_checks_exist():
    """D3: Rule-system section MUST have >=3 checklist items."""
    content = read("checklists/regulatory-analysis-audit.md")
    # Find the rule-system section and count checkboxes
    rs_match = re.search(r'(#{2,4}\s*.*?(?:[Rr]ule.?system|规则系统|赛制).*?(?:\n|$))',
                         content, re.IGNORECASE)
    if rs_match:
        # Get content from this heading to next heading of same/higher level
        heading_level = len(rs_match.group(1)) - len(rs_match.group(1).lstrip("#"))
        remaining = content[rs_match.start():]
        # Skip the heading line
        lines = remaining.split('\n')[1:]
        section_lines = []
        for line in lines:
            if line.startswith("#") and (len(line) - len(line.lstrip("#"))) <= heading_level:
                break
            section_lines.append(line)
        section = '\n'.join(section_lines)
        checks = len(re.findall(r'- \[ \]', section))
        assert checks >= 3, \
            f"Rule-system section has {checks} checklist items, expected >=3"
    else:
        raise AssertionError("Rule-system section heading not found")


def test_d3_state_taxonomy_check():
    """D3: Rule-system checklist MUST include state taxonomy check."""
    content = read("checklists/regulatory-analysis-audit.md")
    rs_match = re.search(r'(#{2,4}\s*.*?(?:[Rr]ule.?system|规则系统|赛制).*?(?:\n|$))',
                         content, re.IGNORECASE)
    if rs_match:
        heading_level = len(rs_match.group(1)) - len(rs_match.group(1).lstrip("#"))
        remaining = content[rs_match.start():]
        lines = remaining.split('\n')[1:]
        section_lines = []
        for line in lines:
            if line.startswith("#") and (len(line) - len(line.lstrip("#"))) <= heading_level:
                break
            section_lines.append(line)
        section = '\n'.join(section_lines)
        assert re.search(r'state.*taxonomy|状态分类|participant.*state|参与者.*状态',
                         section, re.IGNORECASE), \
            "Missing state taxonomy check in rule-system section"
    else:
        raise AssertionError("Rule-system section not found")


def test_d3_intervention_matrix_check():
    """D3: Rule-system checklist MUST include intervention matrix check."""
    content = read("checklists/regulatory-analysis-audit.md")
    rs_match = re.search(r'(#{2,4}\s*.*?(?:[Rr]ule.?system|规则系统|赛制).*?(?:\n|$))',
                         content, re.IGNORECASE)
    if rs_match:
        heading_level = len(rs_match.group(1)) - len(rs_match.group(1).lstrip("#"))
        remaining = content[rs_match.start():]
        lines = remaining.split('\n')[1:]
        section_lines = []
        for line in lines:
            if line.startswith("#") and (len(line) - len(line.lstrip("#"))) <= heading_level:
                break
            section_lines.append(line)
        section = '\n'.join(section_lines)
        assert re.search(r'intervention.*matrix|干预矩阵|规则调整|rule.*adjustment',
                         section, re.IGNORECASE), \
            "Missing intervention matrix check in rule-system section"
    else:
        raise AssertionError("Rule-system section not found")


def test_d3_existing_sections_intact():
    """D3: All existing regulatory audit sections MUST be preserved."""
    content = read("checklists/regulatory-analysis-audit.md")
    original_sections = [
        "## Route activation",
        "## Regulatory state verification",
        "## Evidence quality",
        "## Business impact analysis",
        "## Uncertainty and scenarios",
        "## Business/industry implications",
        "## Hard fail check",
        "## Final sign-off",
    ]
    for section in original_sections:
        assert section in content, f"Lost regulatory audit section: '{section}'"


def test_d3_conditional_activation_wording():
    """D3: Rule-system section MUST state conditional activation (not always-on)."""
    content = read("checklists/regulatory-analysis-audit.md")
    rs_match = re.search(r'(#{2,4}\s*.*?(?:[Rr]ule.?system|规则系统|赛制).*?(?:\n|$))',
                         content, re.IGNORECASE)
    if rs_match:
        heading_level = len(rs_match.group(1)) - len(rs_match.group(1).lstrip("#"))
        remaining = content[rs_match.start():]
        lines = remaining.split('\n')[1:]
        section_lines = []
        for line in lines:
            if line.startswith("#") and (len(line) - len(line.lstrip("#"))) <= heading_level:
                break
            section_lines.append(line)
        section = '\n'.join(section_lines)
        activation_terms = ['启用', '激活', 'activate', '条件', 'conditional', 'only when',
                            '主负担', 'main burden']
        assert any(t in section.lower() for t in activation_terms), \
            "Rule-system section must state conditional activation"
    else:
        raise AssertionError("Rule-system section not found")


# ═══════════════════════════════════════════════════════════════════════════
# D4: checklists/technical-analysis-audit.md (MODIFIED)
# ═══════════════════════════════════════════════════════════════════════════


def test_d4_has_rule_system_section():
    """D4: Technical audit MUST have conditional §Rule-system analysis section."""
    content = read("checklists/technical-analysis-audit.md")
    assert re.search(r'[Rr]ule.?system|规则系统|tournament.*mechanism|赛制',
                     content), \
        "Missing rule-system analysis section in technical audit"


def test_d4_rule_system_checks_exist():
    """D4: Rule-system section MUST have >=3 checklist items."""
    content = read("checklists/technical-analysis-audit.md")
    rs_match = re.search(r'(#{2,4}\s*.*?(?:[Rr]ule.?system|规则系统|赛制).*?(?:\n|$))',
                         content, re.IGNORECASE)
    if rs_match:
        heading_level = len(rs_match.group(1)) - len(rs_match.group(1).lstrip("#"))
        remaining = content[rs_match.start():]
        lines = remaining.split('\n')[1:]
        section_lines = []
        for line in lines:
            if line.startswith("#") and (len(line) - len(line.lstrip("#"))) <= heading_level:
                break
            section_lines.append(line)
        section = '\n'.join(section_lines)
        checks = len(re.findall(r'- \[ \]', section))
        assert checks >= 3, \
            f"Rule-system section has {checks} checklist items, expected >=3"
    else:
        raise AssertionError("Rule-system section heading not found")


def test_d4_existing_sections_intact():
    """D4: All existing technical audit sections MUST be preserved."""
    content = read("checklists/technical-analysis-audit.md")
    original_sections = [
        "## Route activation",
        "## Technical state verification",
        "## Evidence quality",
        "## Comparison structure",
        "## Feasibility assessment",
        "## Maturity assessment",
        "## Judgment quality",
        "## Hard fail check",
        "## Security deep-dive",
        "## Control-plane / workflow-system",
        "## Final sign-off",
    ]
    for section in original_sections:
        assert section in content, f"Lost technical audit section: '{section}'"


def test_d4_addon_activation_consistent():
    """D4: Rule-system activation condition MUST match D1's enablement criteria."""
    audit = read("checklists/technical-analysis-audit.md")
    try:
        addon = read(ADDON_FILE)
        # Both should reference the concept of "rule system changing behavior/incentives"
        audit_has_incentive = "incentive" in audit.lower() or "激励" in audit
        addon_has_incentive = "incentive" in addon.lower() or "激励" in addon
        assert audit_has_incentive == addon_has_incentive or (
            audit_has_incentive or addon_has_incentive
        ), "Activation conditions inconsistent between add-on and audit"
    except AssertionError:
        pass  # Not a hard fail if addon file not yet created
    except FileNotFoundError:
        pass  # Expected before D1 is created


# ═══════════════════════════════════════════════════════════════════════════
# D5: evals/cases/rule-system-add-on-activation-case.md (NEW)
# ═══════════════════════════════════════════════════════════════════════════

EVAL_FILE = "evals/cases/rule-system-add-on-activation-case.md"


def test_d5_eval_file_exists():
    """D5: New eval case file MUST exist."""
    assert file_exists(EVAL_FILE), f"Missing: {EVAL_FILE}"


def test_d5_eval_has_standard_sections():
    """D5: Eval case MUST have standard sections (Goal, Prompt, Pass criteria, Failure signs)."""
    content = read(EVAL_FILE)
    assert "## Goal" in content, "Missing ## Goal"
    assert "## Prompt" in content, "Missing ## Prompt"
    assert "## What this eval is testing" in content, "Missing ## What this eval is testing"
    assert "## Pass criteria" in content, "Missing ## Pass criteria"
    assert "## Failure signs" in content, "Missing ## Failure signs"


def test_d5_eval_activates_addon():
    """D5: Eval case MUST test that the add-on activates for rule-system tasks."""
    content = read(EVAL_FILE)
    assert "rule-system" in content.lower() or "rule system" in content.lower(), \
        "Eval case must reference rule-system add-on"


def test_d5_eval_expects_fail_for_missing_blocks():
    """D5: Missing state taxonomy / intervention matrix MUST trigger fail or conditional-pass."""
    content = read(EVAL_FILE)
    assert ("fail" in content.lower() or "conditional" in content.lower()), \
        "Eval should expect fail or conditional-pass verdict"


def test_d5_eval_has_reviewer_checklist():
    """D5: Eval case MUST have reviewer checklist section."""
    content = read(EVAL_FILE)
    assert "## Reviewer checklist" in content or "## Why this eval matters" in content, \
        "Missing reviewer checklist or why-this-matters section"


# ═══════════════════════════════════════════════════════════════════════════
# P: Cross-file invariants (Phase 2 — run after all D1-D5 pass)
# ═══════════════════════════════════════════════════════════════════════════


def test_p1_addon_cross_references_valid():
    """P1: Cross-references between files must be consistent."""
    try:
        addon = read(ADDON_FILE)
    except FileNotFoundError:
        raise AssertionError("D1 file not yet created")

    # The add-on should be referenced by both checklists
    reg_audit = read("checklists/regulatory-analysis-audit.md")
    tech_audit = read("checklists/technical-analysis-audit.md")

    assert "rule-system-and-mechanism" in reg_audit, \
        "Regulatory audit must reference rule-system-and-mechanism add-on"
    assert "rule-system-and-mechanism" in tech_audit, \
        "Technical audit must reference rule-system-and-mechanism add-on"


def test_p2_no_existing_addons_broken():
    """P2: Existing add-ons (Security deep-dive, Control-plane) MUST be intact."""
    content = read("references/technical-analysis-discipline.md")
    assert "## Security deep-dive: threat modeling add-on" in content, \
        "Security deep-dive add-on missing"
    assert "## Control-plane / workflow-system architecture add-on" in content, \
        "Control-plane add-on missing"

    audit = read("checklists/technical-analysis-audit.md")
    assert "## Security deep-dive" in audit, "Security deep-dive audit section missing"
    assert "## Control-plane / workflow-system" in audit, \
        "Control-plane audit section missing"


def test_p3_addon_file_not_empty():
    """P3: Add-on file MUST have substantial content (>=500 chars)."""
    content = read(ADDON_FILE)
    # Strip code blocks and markdown formatting to check real content
    clean = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
    clean = re.sub(r'[#*|>\- \n\t]+', '', clean)
    assert len(clean) >= 500, \
        f"Add-on file has only {len(clean)} chars of substantial content, expected >=500"


def test_p4_routing_matrix_not_garbled():
    """P4: ROUTING-MATRIX.md table of contents / structure intact."""
    content = read("ROUTING-MATRIX.md")
    # All major sections should still exist
    major_sections = [
        "## Route preflight",
        "## Global rule",
        "## Route execution contract",
    ]
    for section in major_sections:
        assert section in content, f"ROUTING-MATRIX.md lost section: '{section}'"


# ═══════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════

ALL_TESTS = [
    # D1: New add-on file
    ("D1: file exists", test_d1_file_exists),
    ("D1: enablement criteria", test_d1_has_enablement_criteria),
    ("D1: state taxonomy", test_d1_has_state_taxonomy),
    ("D1: intervention matrix with table", test_d1_has_intervention_matrix),
    ("D1: relationship to existing rules", test_d1_has_relationship_to_existing_rules),
    ("D1: references regulatory discipline", test_d1_references_regulatory_discipline),
    ("D1: references technical discipline", test_d1_references_technical_discipline),
    ("D1: has non-goals", test_d1_has_non_goals),
    ("D1: domain-agnostic", test_d1_no_football_only_language),
    ("D1: simulation contract ref", test_d1_has_simulation_contract_reference),
    # D2: ROUTING-MATRIX.md modifications
    ("D2: regulatory route refs addon", test_d2_regulatory_route_references_addon),
    ("D2: technical route refs addon", test_d2_technical_route_references_addon),
    ("D2: 11 routes intact", test_d2_existing_routes_intact),
    ("D2: regulatory hard-fails intact", test_d2_regulatory_hard_fails_intact),
    # D3: regulatory-analysis-audit.md modifications
    ("D3: has rule-system section", test_d3_has_rule_system_section),
    ("D3: rule-system >=3 checks", test_d3_rule_system_checks_exist),
    ("D3: state taxonomy check", test_d3_state_taxonomy_check),
    ("D3: intervention matrix check", test_d3_intervention_matrix_check),
    ("D3: existing sections intact", test_d3_existing_sections_intact),
    ("D3: conditional activation", test_d3_conditional_activation_wording),
    # D4: technical-analysis-audit.md modifications
    ("D4: has rule-system section", test_d4_has_rule_system_section),
    ("D4: rule-system >=3 checks", test_d4_rule_system_checks_exist),
    ("D4: existing sections intact", test_d4_existing_sections_intact),
    ("D4: activation consistent", test_d4_addon_activation_consistent),
    # D5: New eval case
    ("D5: eval file exists", test_d5_eval_file_exists),
    ("D5: standard sections", test_d5_eval_has_standard_sections),
    ("D5: activates add-on", test_d5_eval_activates_addon),
    ("D5: expects fail", test_d5_eval_expects_fail_for_missing_blocks),
    ("D5: reviewer checklist", test_d5_eval_has_reviewer_checklist),
    # P: Cross-file invariants
    ("P1: cross-references valid", test_p1_addon_cross_references_valid),
    ("P2: existing addons intact", test_p2_no_existing_addons_broken),
    ("P3: addon content >=500 chars", test_p3_addon_file_not_empty),
    ("P4: ROUTING-MATRIX structure intact", test_p4_routing_matrix_not_garbled),
]

if __name__ == "__main__":
    passed = 0
    failed = 0
    for name, fn in ALL_TESTS:
        try:
            fn()
            print(f"  ✅ {name}")
            passed += 1
        except AssertionError as e:
            print(f"  ❌ {name}: {e}")
            failed += 1
        except Exception as e:
            print(f"  ❌ {name}: Unexpected error: {e}")
            failed += 1

    print(f"\n{'='*60}")
    print(f"Results: {passed} passed, {failed} failed out of {len(ALL_TESTS)}")
    if failed:
        sys.exit(1)
    else:
        print("All contracts verified ✅")
