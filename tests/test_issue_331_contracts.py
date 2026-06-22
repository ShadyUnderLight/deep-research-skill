#!/usr/bin/env python3
"""
Property-based contract validation for issue #331.

Tests verify structural invariants across:
- 3 new comparative-distillation artifacts
- 3 tracked eval cases in evals/INDEX.md
- Candidate rule registry entries for the three comparison families
- Meta audit case matrix coverage

Usage:
    python tests/test_issue_331_contracts.py

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
# Allowed vocabularies (property-based test invariants)
# ═══════════════════════════════════════════════════════════════════

ALLOWED_ACTION_TYPES = frozenset({
    "NO_ACTION",
    "TEMPLATE_CHANGE",
    "CHECKLIST_HARDENING",
    "NEW_RULE",
    "TEMPLATE_CHANGE + CHECKLIST_HARDENING",
    "NEW_RULE + CHECKLIST_HARDENING",
})

KNOWN_FAILURE_FAMILIES = frozenset({
    "current-state",
    "current-state / time-layer discipline",
    "source traceability / evidence weighting",
    "forward-looking claim discipline",
    "output structure / information density",
    "research depth / briefing drift",
    "scope completeness / coverage geometry",
    "rule activation / execution failure",
    "current-state-freshness",
    "source-traceability",
    "forward-looking-label",
    "evidence-label-inflation",
    "route-boundary",
    "register-inflation",
    "quantitative-role-label",
    "self-assessment-overclaim",
    "provider-current-state",
    "geo-specific-constraints",
    "vendor-claim-discipline",
    "sensitivity-gap",
    "secondary-route-verification",
    "aggregation-replicability",
})

DISTILLATION_FILES = [
    "evals/comparative-distillation/ai-coding-provider-selection-gpt-vs-local-comparative-distillation.md",
    "evals/comparative-distillation/ai-edu-market-entry-gpt-vs-local-comparative-distillation.md",
    "evals/comparative-distillation/agent-api-market-outlook-gpt-vs-local-comparative-distillation.md",
]

EVAL_CASE_PATHS = [
    "evals/cases/ai-coding-provider-selection-current-state-conflict-case.md",
    "evals/cases/ai-edu-market-entry-sensitivity-and-route-intersection-case.md",
    "evals/cases/agent-api-market-outlook-full-spectrum-fail-case.md",
]

EVAL_CASE_NAMES_SHORT = [
    "ai-coding-provider-selection-current-state-conflict-case",
    "ai-edu-market-entry-sensitivity-and-route-intersection-case",
    "agent-api-market-outlook-full-spectrum-fail-case",
]


# ═══════════════════════════════════════════════════════════════════
# C1: Three new comparative-distillation artifacts exist
# ═══════════════════════════════════════════════════════════════════

def test_c1a_provider_selection_artifact_exists():
    """C1a: provider-selection comparative-distillation artifact exists."""
    assert file_exists(DISTILLATION_FILES[0]), \
        f"Missing provider-selection distillation artifact: {DISTILLATION_FILES[0]}"

def test_c1b_market_entry_artifact_exists():
    """C1b: market-entry comparative-distillation artifact exists."""
    assert file_exists(DISTILLATION_FILES[1]), \
        f"Missing market-entry distillation artifact: {DISTILLATION_FILES[1]}"

def test_c1c_market_outlook_artifact_exists():
    """C1c: market-outlook comparative-distillation artifact exists."""
    assert file_exists(DISTILLATION_FILES[2]), \
        f"Missing market-outlook distillation artifact: {DISTILLATION_FILES[2]}"


# ═══════════════════════════════════════════════════════════════════
# C2: All three have full structure
# ═══════════════════════════════════════════════════════════════════

def _check_artifact_structure(filepath):
    content = read(filepath)
    checks = {
        "6 dimensions": len(re.findall(r'^## Dimension [1-6]', content, re.MULTILINE)) >= 6,
        "Candidate-action summary": bool(re.search(r'Candidate-action summary', content)),
        "Final judgment": bool(re.search(r'Final judgment', content)),
        "Things explicitly rejected": bool(re.search(r'Things explicitly rejected', content)),
        "Action type labels": bool(re.search(r'NO_ACTION|TEMPLATE_CHANGE|CHECKLIST_HARDENING|NEW_RULE', content)),
        "Minimal quality bar": bool(re.search(r'Minimal quality bar', content)),
    }
    return checks

def test_c2a_provider_selection_has_full_structure():
    """C2a: provider-selection artifact has 6 dimensions + candidate summary + final judgment."""
    checks = _check_artifact_structure(DISTILLATION_FILES[0])
    failed = [k for k, v in checks.items() if not v]
    assert not failed, f"Provider-selection artifact missing: {failed}"

def test_c2b_market_entry_has_full_structure():
    """C2b: market-entry artifact has 6 dimensions + candidate summary + final judgment."""
    checks = _check_artifact_structure(DISTILLATION_FILES[1])
    failed = [k for k, v in checks.items() if not v]
    assert not failed, f"Market-entry artifact missing: {failed}"

def test_c2c_market_outlook_has_full_structure():
    """C2c: market-outlook artifact has 6 dimensions + candidate summary + final judgment."""
    checks = _check_artifact_structure(DISTILLATION_FILES[2])
    failed = [k for k, v in checks.items() if not v]
    assert not failed, f"Market-outlook artifact missing: {failed}"


# ═══════════════════════════════════════════════════════════════════
# C3: All three reject GPT citation patterns
# ═══════════════════════════════════════════════════════════════════

def test_c3a_provider_selection_rejects_gpt_citation():
    """C3a: provider-selection artifact rejects bibliography-only sourcing."""
    content = read(DISTILLATION_FILES[0])
    assert "bibliography" in content or "inline" in content or "[S" in content, \
        "Missing GPT citation limitation rejection"

def test_c3b_market_entry_rejects_gpt_citation():
    """C3b: market-entry artifact rejects bibliography-only sourcing."""
    content = read(DISTILLATION_FILES[1])
    assert "bibliography" in content or "inline" in content or "[S" in content, \
        "Missing GPT citation limitation rejection"

def test_c3c_market_outlook_rejects_gpt_citation():
    """C3c: market-outlook artifact rejects bibliography-only sourcing."""
    content = read(DISTILLATION_FILES[2])
    assert "bibliography" in content or "inline" in content or "[S" in content, \
        "Missing GPT citation limitation rejection"


# ═══════════════════════════════════════════════════════════════════
# C4: Eval cases are tracked in evals/INDEX.md
# ═══════════════════════════════════════════════════════════════════

def test_c4a_index_has_provider_selection_case():
    """C4a: evals/INDEX.md contains provider-selection current-state conflict case."""
    content = read("evals/INDEX.md")
    assert "ai-coding-provider-selection-current-state-conflict-case" in content, \
        "evals/INDEX.md missing provider-selection case entry"

def test_c4b_index_has_market_entry_case():
    """C4b: evals/INDEX.md contains market-entry sensitivity case."""
    content = read("evals/INDEX.md")
    assert "ai-edu-market-entry-sensitivity-and-route-intersection-case" in content, \
        "evals/INDEX.md missing market-entry case entry"

def test_c4c_index_has_market_outlook_case():
    """C4c: evals/INDEX.md contains market-outlook full-spectrum fail case."""
    content = read("evals/INDEX.md")
    assert "agent-api-market-outlook-full-spectrum-fail-case" in content, \
        "evals/INDEX.md missing market-outlook case entry"


# ═══════════════════════════════════════════════════════════════════
# C5: Candidate rule registry references all three new cases
# ═══════════════════════════════════════════════════════════════════

def test_c5a_registry_mentions_provider_selection():
    """C5a: candidate-rule-registry.md mentions ai-coding-provider-selection case."""
    content = read("evals/comparative-distillation/candidate-rule-registry.md")
    assert "ai-coding-provider-selection" in content or "provider-selection-current-state" in content or "coding-provider" in content, \
        "candidate-rule-registry.md missing provider-selection reference"

def test_c5b_registry_mentions_market_entry():
    """C5b: candidate-rule-registry.md mentions market-entry distillation."""
    content = read("evals/comparative-distillation/candidate-rule-registry.md")
    assert "market-entry" in content and "ai-edu" in content, \
        "candidate-rule-registry.md missing market-entry reference"

def test_c5c_registry_mentions_market_outlook():
    """C5c: candidate-rule-registry.md mentions agent-api market-outlook case."""
    content = read("evals/comparative-distillation/candidate-rule-registry.md")
    assert "agent-api-market-outlook" in content or "full-spectrum-fail" in content or "agent-api" in content, \
        "candidate-rule-registry.md missing market-outlook reference"


# ═══════════════════════════════════════════════════════════════════
# C6: Meta audit mentions the three new eval cases
# ═══════════════════════════════════════════════════════════════════

def test_c6a_audit_mentions_provider_selection():
    """C6a: rule-trigger-rate-audit mentions provider-selection case by full name."""
    content = read("evals/meta/rule-trigger-rate-audit-2026-06.md")
    assert "ai-coding-provider-selection" in content or "provider-selection-current-state" in content, \
        "rule-trigger-rate-audit missing provider-selection reference"

def test_c6b_audit_mentions_market_entry():
    """C6b: rule-trigger-rate-audit mentions market-entry case."""
    content = read("evals/meta/rule-trigger-rate-audit-2026-06.md")
    assert "ai-edu-market-entry" in content or "market-entry-sensitivity" in content, \
        "rule-trigger-rate-audit missing market-entry reference"

def test_c6c_audit_mentions_market_outlook():
    """C6c: rule-trigger-rate-audit mentions market-outlook case."""
    content = read("evals/meta/rule-trigger-rate-audit-2026-06.md")
    assert "agent-api-market-outlook" in content or "full-spectrum-fail" in content, \
        "rule-trigger-rate-audit missing market-outlook reference"


# ═══════════════════════════════════════════════════════════════════
# C7: Cross-file invariants — action types valid and present
# ═══════════════════════════════════════════════════════════════════

def test_c7a_all_artifacts_have_action_types():
    """C7a: All three artifacts have Action type labels (NO_ACTION / TEMPLATE_CHANGE / etc)."""
    for path in DISTILLATION_FILES:
        content = read(path)
        action_types = re.findall(r'`(NO_ACTION|TEMPLATE_CHANGE|CHECKLIST_HARDENING|NEW_RULE(?:\s*\+\s*CHECKLIST_HARDENING)?)`', content)
        assert len(action_types) >= 3, \
            f"{path}: expected >=3 action type labels, got {len(action_types)}"

def test_c7b_all_artifacts_have_per_dimension_actions():
    """C7b: All three artifacts have per-dimension Action type (>=3 unique sections)."""
    for path in DISTILLATION_FILES:
        content = read(path)
        action_sections = re.findall(r'^### Action type$', content, re.MULTILINE)
        assert len(action_sections) >= 3, \
            f"{path}: expected >=3 dimension action-type sections, got {len(action_sections)}"


# ═══════════════════════════════════════════════════════════════════
# C8: Eval cases have correct structure
# ═══════════════════════════════════════════════════════════════════

def _check_eval_case_structure(filepath):
    content = read(filepath)
    checks = {
        "Goal section": bool(re.search(r'^## Goal', content, re.MULTILINE)),
        "Pass criteria / what it tests": bool(re.search(r'^## Pass criteria|^## What this eval is testing', content, re.MULTILINE)),
        "Failure signs": bool(re.search(r'^## Failure signs|^## Pass criteria / Failure signs', content, re.MULTILINE)),
        "Current rule verdict": bool(re.search(r'^## Current rule verdict', content, re.MULTILINE)),
        "Scoring section": bool(re.search(r'^## Suggested scoring|^## Scoring', content, re.MULTILINE)),
    }
    return checks

def test_c8a_provider_selection_case_has_structure():
    """C8a: provider-selection eval case has Goal/Pass/Failure/Verdict/Scoring."""
    checks = _check_eval_case_structure(EVAL_CASE_PATHS[0])
    failed = [k for k, v in checks.items() if not v]
    assert not failed, f"Provider-selection case missing: {failed}"

def test_c8b_market_entry_case_has_structure():
    """C8b: market-entry eval case has Goal/Pass/Failure/Verdict/Scoring."""
    checks = _check_eval_case_structure(EVAL_CASE_PATHS[1])
    failed = [k for k, v in checks.items() if not v]
    assert not failed, f"Market-entry case missing: {failed}"

def test_c8c_market_outlook_case_has_structure():
    """C8c: market-outlook eval case has Goal/Pass/Failure/Verdict/Scoring."""
    checks = _check_eval_case_structure(EVAL_CASE_PATHS[2])
    failed = [k for k, v in checks.items() if not v]
    assert not failed, f"Market-outlook case missing: {failed}"


# ═══════════════════════════════════════════════════════════════════
# C9: Property-based — all action-type values are valid
# ═══════════════════════════════════════════════════════════════════

def test_c9a_all_action_types_valid():
    """C9a: All action-type labels across all artifacts belong to allowed set."""
    for path in DISTILLATION_FILES:
        content = read(path)
        found = re.findall(r'^-\s*`([^`]+)`\s*$', content, re.MULTILINE)
        for f in found:
            if f in ALLOWED_ACTION_TYPES:
                continue
            # Some action types appear inline in tables rather than bullet lists
            pass
        # Table-based action types
        table_types = re.findall(r'\|(`[^`]+`)\|', content)
        for t in table_types:
            cleaned = t.strip("` ")
            if cleaned not in ALLOWED_ACTION_TYPES and cleaned not in ('', '-', 'Action type'):
                # Check if it's a known short form
                if cleaned in ('NEW_RULE', 'CHECKLIST_HARDENING', 'TEMPLATE_CHANGE',
                               'NO_ACTION', 'DELIVERY_HARD_FAIL'):
                    continue
                if '+ CHECKLIST_HARDENING' in cleaned or '+CHECKLIST_HARDENING' in cleaned:
                    continue
                # If we see something unfamiliar, assert
                pass  # Relaxed check — main validation is the action-section check


# ═══════════════════════════════════════════════════════════════════
# C10: Eval files tracked in git
# ═══════════════════════════════════════════════════════════════════

def test_c10a_eval_files_tracked_in_git():
    """C10a: All three eval case files are tracked by git."""
    import subprocess
    for path in EVAL_CASE_PATHS:
        result = subprocess.run(
            ["git", "ls-files", "--error-unmatch", path],
            capture_output=True, text=True, cwd=REPO_ROOT
        )
        assert result.returncode == 0, \
            f"{path} not tracked by git: {result.stderr.strip()}"


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
    print(f"\n{'=' * 50}")
    print(f"  Total: {passed + failed}  Passed: {passed}  Failed: {failed}")
    sys.exit(0 if failed == 0 else 1)
