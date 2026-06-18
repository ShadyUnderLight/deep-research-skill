#!/usr/bin/env python3
"""
Property-based contract validation for issue #327.

Tests verify structural invariants across:
- references/decision-report-template.md provider-selection enterprise rollout sub-template
- ROUTING-MATRIX.md visible artifact contract for enterprise rollout
- checklists/option-selection-final-audit.md enterprise rollout gate
- references/option-selection-and-shortlist-discipline.md rollout questions
- evals/cases/ new enterprise-rollout eval case

Usage:
    python tests/test_issue_327_contracts.py

Expected AFTER implementation: ALL PASS
Before implementation (TDD): FAIL for missing content
"""

import re
import sys
import os

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def read(path):
    with open(os.path.join(REPO_ROOT, path), "r") as f:
        return f.read()


def file_exists(path):
    return os.path.isfile(os.path.join(REPO_ROOT, path))


def _route_section(content):
    """Extract the Provider / Vendor Selection section from ROUTING-MATRIX.md."""
    start = content.find("## Route: Provider / Vendor Selection")
    if start == -1:
        return ""
    remainder = content[start + len("## Route: Provider / Vendor Selection"):]
    next_heading = remainder.find("\n## ")
    if next_heading == -1:
        return remainder
    return remainder[:next_heading]


# ═══════════════════════════════════════════════════════════════════
# C1: decision-report-template.md has enterprise rollout sub-template
# ═══════════════════════════════════════════════════════════════════

def test_c1a_has_recommendation_hierarchy():
    """C1a: provider-selection template has 首选/备选/次选/避免 hierarchy."""
    content = read("references/decision-report-template.md")
    assert re.search(r'首选.*备选.*次选.*避免', content), \
        "Missing recommendation hierarchy (首选/备选/次选/避免)"


def test_c1b_has_team_size_roadmap():
    """C1b: provider-selection template has team-size governance roadmap."""
    content = read("references/decision-report-template.md")
    assert re.search(r'小团队|小型团队|中型团队|大型团队|治理成熟度', content), \
        "Missing team-size governance roadmap"


def test_c1c_has_migration_checklist():
    """C1c: provider-selection template has migration checklist with security/identity/CI/training/exit."""
    content = read("references/decision-report-template.md")
    assert re.search(r'inventory|安全|SSO|SCIM|RBAC|审计.*培训|试运行|退出条件', content), \
        "Missing migration checklist items"


def test_c1d_has_tco_template():
    """C1d: provider-selection template has TCO template with comprehensive cost categories."""
    content = read("references/decision-report-template.md")
    assert re.search(r'TCO|总拥有成本', content), \
        "Missing TCO template"
    assert re.search(r'直接费|seat.*API', content), \
        "TCO template missing direct fee category"


def test_c1e_tco_has_boundary():
    """C1e: TCO template requires boundary declaration (included/excluded)."""
    content = read("references/decision-report-template.md")
    assert re.search(r'included.*excluded|边界声明|included/excluded boundary', content), \
        "TCO template missing boundary declaration"


def test_c1f_tco_has_cost_role_labels():
    """C1f: TCO template requires cost role labels (observed/estimate/assumption/model-output)."""
    content = read("references/decision-report-template.md")
    assert re.search(r'observed.*estimate.*assumption.*model-output|角色标签.*observed|成本角色', content), \
        "TCO template missing cost role labels"


def test_c1g_has_unresolved_questions():
    """C1g: provider-selection template links unresolved questions to recommendation strength."""
    content = read("references/decision-report-template.md")
    assert re.search(r'未决问题|unresolved.*recommendation|改变推荐.*未确认', content), \
        "Missing unresolved-questions-to-recommendation-strength link"


# ═══════════════════════════════════════════════════════════════════
# C2: ROUTING-MATRIX.md visible artifact contract updated
# ═══════════════════════════════════════════════════════════════════

def test_c2a_routing_has_enterprise_rollout():
    """C2a: ROUTING-MATRIX.md Provider Selection artifact contract mentions enterprise rollout."""
    content = read("ROUTING-MATRIX.md")
    route_sec = _route_section(content)
    assert re.search(r'recommendation hierarchy|首选.*备选|TCO.*边界|迁移.*checklist|企业落地|enterprise rollout', route_sec), \
        "ROUTING-MATRIX.md Provider Selection section missing enterprise rollout in artifact contract"


def test_c2b_routing_has_unresolved_link():
    """C2b: ROUTING-MATRIX.md artifact contract links unresolved questions to ranking."""
    content = read("ROUTING-MATRIX.md")
    route_sec = _route_section(content)
    assert re.search(r'unresolved|未决问题|未确认.*排名|unknown.*ranking', route_sec), \
        "Missing unresolved-questions-to-ranking link in artifact contract"


# ═══════════════════════════════════════════════════════════════════
# C3: option-selection-final-audit.md has enterprise rollout gate
# ═══════════════════════════════════════════════════════════════════

def test_c3a_audit_has_tco_check():
    """C3a: option-selection-final-audit.md has TCO boundary check."""
    content = read("checklists/option-selection-final-audit.md")
    assert re.search(r'TCO.*边界|直接费.*网络|总拥有成本.*声明', content), \
        "Missing TCO boundary check in audit"


def test_c3b_audit_has_migration_check():
    """C3b: option-selection-final-audit.md has migration/rollout check."""
    content = read("checklists/option-selection-final-audit.md")
    assert re.search(r'迁移.*checklist|安全.*SSO.*培训|inventory.*身份.*CI', content), \
        "Missing migration/rollout check in audit"


def test_c3c_audit_has_team_scale_check():
    """C3c: option-selection-final-audit.md has team-size/governance check."""
    content = read("checklists/option-selection-final-audit.md")
    assert re.search(r'团队规模|小团队|中型|大型团队|治理成熟度', content), \
        "Missing team-size/governance check in audit"


# ═══════════════════════════════════════════════════════════════════
# C4: option-selection-and-shortlist-discipline.md has rollout questions
# ═══════════════════════════════════════════════════════════════════

def test_c4a_discipline_has_rollout_questions():
    """C4a: option-selection-and-shortlist-discipline.md has enterprise rollout heuristic questions."""
    content = read("references/option-selection-and-shortlist-discipline.md")
    assert re.search(r'enterprise rollout|企业落地|迁移.*上线|TCO.*hidden|团队规模.*路线', content), \
        "Missing enterprise rollout heuristic questions"


# ═══════════════════════════════════════════════════════════════════
# C5: New eval case exists
# ═══════════════════════════════════════════════════════════════════

def test_c5a_enterprise_rollout_eval_exists():
    """C5a: provider-selection-enterprise-rollout-missing eval case exists."""
    assert file_exists("evals/cases/provider-selection-enterprise-rollout-missing-case.md"), \
        "Missing enterprise rollout eval case"


# ═══════════════════════════════════════════════════════════════════
# C6: Existing discipline preserved (anti-regression)
# ═══════════════════════════════════════════════════════════════════

def test_c6a_current_state_gate_preserved():
    """C6a: option-selection-final-audit.md still has current-state gate."""
    content = read("checklists/option-selection-final-audit.md")
    assert "current primary model/API family" in content, \
        "Existing current-state gate was removed"


def test_c6b_decision_template_provider_structure_preserved():
    """C6b: decision-report-template.md still has original 11-section provider structure."""
    content = read("references/decision-report-template.md")
    assert "Ranked shortlist" in content, \
        "Existing provider-selection 11-section structure was removed"


def test_c6c_routing_hard_fail_preserved():
    """C6c: ROUTING-MATRIX.md still has hard-fail conditions."""
    content = read("ROUTING-MATRIX.md")
    route_sec = _route_section(content)
    assert "stale anchor" in route_sec, \
        "Existing hard-fail conditions were removed"


# ═══════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import inspect
    this_module = sys.modules[__name__]
    tests = [func for name, func in inspect.getmembers(this_module)
             if name.startswith("test_") and callable(func)]
    passed = 0
    failed = 0
    for test in sorted(tests, key=lambda t: t.__name__):
        try:
            test()
            print(f"  ✅ {test.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"  ❌ {test.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"  ❌ {test.__name__}: {type(e).__name__}: {e}")
            failed += 1

    print(f"\n{'='*50}")
    print(f"  Total: {passed + failed}  |  Passed: {passed}  |  Failed: {failed}")
    if failed:
        sys.exit(1)
