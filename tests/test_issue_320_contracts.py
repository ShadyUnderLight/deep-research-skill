#!/usr/bin/env python3
"""
Property-based contract validation for issue #320.

Tests verify structural invariants across:
- 2 new comparative-distillation artifacts
- references/report-template.md input boundary section
- references/decision-report-template.md implementation stages
- references/market-outlook-and-scenario-discipline.md value-chain, regional, action table
- checklists/market-outlook-audit.md value-chain, regional, actionability checks
- evals/templates/decision-utility-rubric.md enhanced checks

Usage:
    python tests/test_issue_320_contracts.py

Expected AFTER implementation: ALL PASS
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


# ═══════════════════════════════════════════════════════════════════
# C1: Two comparative distillation artifacts exist
# ═══════════════════════════════════════════════════════════════════

def test_c1a_small_team_artifact_exists():
    """C1a: small-team-ai-agent comparative-distillation artifact exists."""
    assert file_exists("evals/comparative-distillation/small-team-ai-agent-gpt-vs-local-comparative-distillation.md"), \
        "Missing small-team-ai-agent distillation artifact"

def test_c1b_dc_power_artifact_exists():
    """C1b: data-center-power comparative-distillation artifact exists."""
    assert file_exists("evals/comparative-distillation/data-center-power-bottleneck-gpt-vs-local-comparative-distillation.md"), \
        "Missing data-center-power distillation artifact"


# ═══════════════════════════════════════════════════════════════════
# C2: Both artifacts contain 6-dimension framework, Candidate-action
# summary, Final judgment
# ═══════════════════════════════════════════════════════════════════

def _check_artifact_structure(filepath):
    content = read(filepath)
    checks = {
        "6 dimensions": len(re.findall(r'^## Dimension [1-6]', content, re.MULTILINE)) >= 6,
        "Candidate-action summary": bool(re.search(r'Candidate-action summary', content)),
        "Final judgment": bool(re.search(r'Final judgment', content)),
        "Things explicitly rejected": bool(re.search(r'Things explicitly rejected', content)),
        "Action type labels": bool(re.search(r'NO_ACTION|TEMPLATE_CHANGE|CHECKLIST_HARDENING|NEW_RULE', content)),
    }
    return checks

def test_c2a_small_team_has_full_structure():
    """C2a: small-team artifact has 6 dimensions + candidate summary + final judgment."""
    checks = _check_artifact_structure(
        "evals/comparative-distillation/small-team-ai-agent-gpt-vs-local-comparative-distillation.md")
    failed = [k for k, v in checks.items() if not v]
    assert not failed, f"Small-team artifact missing: {failed}"

def test_c2b_dc_power_has_full_structure():
    """C2b: dc-power artifact has 6 dimensions + candidate summary + final judgment."""
    checks = _check_artifact_structure(
        "evals/comparative-distillation/data-center-power-bottleneck-gpt-vs-local-comparative-distillation.md")
    failed = [k for k, v in checks.items() if not v]
    assert not failed, f"DC-power artifact missing: {failed}"


# ═══════════════════════════════════════════════════════════════════
# C3: Both artifacts document GPT citation limitations as rejected
# ═══════════════════════════════════════════════════════════════════

def test_c3a_small_team_rejects_gpt_citation():
    """C3a: small-team artifact rejects bibliography-only sourcing."""
    content = read("evals/comparative-distillation/small-team-ai-agent-gpt-vs-local-comparative-distillation.md")
    assert "bibliography" in content or "turn..." in content, \
        "Missing GPT citation limitation rejection"

def test_c3b_dc_power_rejects_gpt_citation():
    """C3b: dc-power artifact rejects bibliography-only sourcing."""
    content = read("evals/comparative-distillation/data-center-power-bottleneck-gpt-vs-local-comparative-distillation.md")
    assert "bibliography" in content or "turn..." in content, \
        "Missing GPT citation limitation rejection"


# ═══════════════════════════════════════════════════════════════════
# C4: Template updates exist
# ═══════════════════════════════════════════════════════════════════

def test_c4a_report_template_has_input_boundary():
    """C4a: report-template.md contains '输入边界' or '未指定项'."""
    content = read("references/report-template.md")
    assert re.search(r'输入边界|未指定项', content), \
        "report-template.md missing input boundary section"

def test_c4b_decision_template_has_implementation_stages():
    """C4b: decision-report-template.md contains '实施路线' or implementation stages structure."""
    content = read("references/decision-report-template.md")
    assert re.search(r'实施路线|\|\s*准备/MVP\s*\|', content), \
        "decision-report-template.md missing implementation stages"

def test_c4c_market_outlook_has_value_chain():
    """C4c: market-outlook-and-scenario-discipline.md contains 'Value-chain sensitivity map'."""
    content = read("references/market-outlook-and-scenario-discipline.md")
    assert "Value-chain sensitivity map" in content, \
        "market-outlook-and-scenario-discipline.md missing value-chain sensitivity map"

def test_c4d_market_outlook_has_regional_matrix():
    """C4d: market-outlook-and-scenario-discipline.md contains 'Regional coverage matrix'."""
    content = read("references/market-outlook-and-scenario-discipline.md")
    assert "Regional coverage matrix" in content, \
        "market-outlook-and-scenario-discipline.md missing regional coverage matrix"

def test_c4e_market_outlook_has_action_table():
    """C4e: market-outlook-and-scenario-discipline.md contains action table template."""
    content = read("references/market-outlook-and-scenario-discipline.md")
    assert re.search(r'Stakeholder.*action table|Decision to make.*Recommended action.*Trigger to revise', content), \
        "market-outlook-and-scenario-discipline.md missing stakeholder action table"


# ═══════════════════════════════════════════════════════════════════
# C5: Checklist updates exist
# ═══════════════════════════════════════════════════════════════════

def test_c5a_checklist_has_value_chain():
    """C5a: market-outlook-audit.md contains value-chain sensitivity check."""
    content = read("checklists/market-outlook-audit.md")
    assert "value-chain sensitivity" in content, \
        "market-outlook-audit.md missing value-chain sensitivity check"

def test_c5b_checklist_has_regional_coverage():
    """C5b: market-outlook-audit.md contains regional coverage check."""
    content = read("checklists/market-outlook-audit.md")
    assert "regional coverage" in content.lower(), \
        "market-outlook-audit.md missing regional coverage check"

def test_c5c_checklist_has_action_table():
    """C5c: market-outlook-audit.md contains action table or actionability check."""
    content = read("checklists/market-outlook-audit.md")
    assert re.search(r'action table|actionability', content), \
        "market-outlook-audit.md missing actionability check"


# ═══════════════════════════════════════════════════════════════════
# C6: candidate-rule-registry.md references both new distillation cases
# ═══════════════════════════════════════════════════════════════════

def test_c6a_registry_mentions_small_team():
    """C6a: candidate-rule-registry.md mentions small-team-ai-agent."""
    content = read("evals/comparative-distillation/candidate-rule-registry.md")
    assert "small-team-ai-agent" in content, \
        "candidate-rule-registry.md missing small-team-ai-agent reference"

def test_c6b_registry_mentions_dc_power():
    """C6b: candidate-rule-registry.md mentions data-center-power."""
    content = read("evals/comparative-distillation/candidate-rule-registry.md")
    assert "dc-power" in content or "data-center-power" in content, \
        "candidate-rule-registry.md missing data-center-power reference"


# ═══════════════════════════════════════════════════════════════════
# C7: Cross-file invariants
# ═══════════════════════════════════════════════════════════════════

def test_c7a_both_artifacts_have_action_types():
    """C7a: Both artifacts have Action type labels (NO_ACTION / TEMPLATE_CHANGE / etc)."""
    for path in [
        "evals/comparative-distillation/small-team-ai-agent-gpt-vs-local-comparative-distillation.md",
        "evals/comparative-distillation/data-center-power-bottleneck-gpt-vs-local-comparative-distillation.md",
    ]:
        content = read(path)
        action_types = re.findall(r'`(NO_ACTION|TEMPLATE_CHANGE|CHECKLIST_HARDENING|NEW_RULE)`', content)
        assert len(action_types) >= 3, \
            f"{path}: expected >=3 action type labels, got {len(action_types)}"

def test_c7b_both_artifacts_have_per_dimension_actions():
    """C7b: Both artifacts have per-dimension Action type (>=3 unique action-type blocks)."""
    for path in [
        "evals/comparative-distillation/small-team-ai-agent-gpt-vs-local-comparative-distillation.md",
        "evals/comparative-distillation/data-center-power-bottleneck-gpt-vs-local-comparative-distillation.md",
    ]:
        content = read(path)
        # Count lines that are "### Action type" sections
        action_sections = re.findall(r'^### Action type$', content, re.MULTILINE)
        assert len(action_sections) >= 3, \
            f"{path}: expected >=3 dimension action-type sections, got {len(action_sections)}"


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
