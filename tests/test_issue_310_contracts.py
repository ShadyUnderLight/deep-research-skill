#!/usr/bin/env python3
"""
Property-based contract validation for issue #310.

Tests verify structural invariants for comparative-distillation artifacts:

  C1: world-cup-constrained-choice-gpt-vs-local-comparative-distillation.md exists
  C2: programming-language-learning-gpt-vs-local-comparative-distillation.md exists
  C3: Both artifacts contain 6-dimension comparison framework
  C4: Both artifacts contain Candidate-action summary
  C5: Both artifacts explicitly document turn... citation as rejected
  C6: candidate-rule-registry.md contains entries referencing these two cases
  C7: Cross-file: artifacts use template format correctly

Usage:
    python tests/test_issue_310_contracts.py

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


# ═══════════════════════════════════════════════════════════════════
# File paths
# ═══════════════════════════════════════════════════════════════════

WORLD_CUP_ARTIFACT = "evals/comparative-distillation/world-cup-constrained-choice-gpt-vs-local-comparative-distillation.md"
PROG_LANG_ARTIFACT = "evals/comparative-distillation/programming-language-learning-gpt-vs-local-comparative-distillation.md"
REGISTRY = "evals/comparative-distillation/candidate-rule-registry.md"


# ═══════════════════════════════════════════════════════════════════
# C1: World cup artifact exists and has required structure
# ═══════════════════════════════════════════════════════════════════

def test_c1_world_cup_artifact_exists():
    """C1: World cup distillation artifact MUST exist."""
    assert file_exists(WORLD_CUP_ARTIFACT), f"Missing: {WORLD_CUP_ARTIFACT}"


def test_c1_world_cup_has_six_dimensions():
    """C1: World cup artifact MUST contain 6 dimension headings."""
    content = read(WORLD_CUP_ARTIFACT)
    dimensions = [
        'Current-state discipline',
        'Numerical and date discipline',
        'Source traceability and evidence weighting',
        'Forward-looking claim discipline',
        'Structural readability and information density',
        'Decision usefulness',
    ]
    for dim in dimensions:
        assert dim in content, f"Missing dimension '{dim}' in world cup artifact"


def test_c1_world_cup_has_candidate_summary():
    """C1: World cup artifact MUST contain Candidate-action summary."""
    content = read(WORLD_CUP_ARTIFACT)
    assert 'Candidate-action summary' in content, "Missing Candidate-action summary"


def test_c1_world_cup_documents_turn_citations():
    """C1: World cup artifact MUST document turn... citations as rejected."""
    content = read(WORLD_CUP_ARTIFACT)
    assert re.search(r'turn\d+|turn.*citation|不可交付|不可采纳|rejected', content, re.IGNORECASE), \
        "World cup artifact must document turn... citation as rejected"


# ═══════════════════════════════════════════════════════════════════
# C2: Programming language artifact exists and has required structure
# ═══════════════════════════════════════════════════════════════════

def test_c2_prog_lang_artifact_exists():
    """C2: Programming language distillation artifact MUST exist."""
    assert file_exists(PROG_LANG_ARTIFACT), f"Missing: {PROG_LANG_ARTIFACT}"


def test_c2_prog_lang_has_six_dimensions():
    """C2: Programming language artifact MUST contain 6 dimension headings."""
    content = read(PROG_LANG_ARTIFACT)
    dimensions = [
        'Current-state discipline',
        'Numerical and date discipline',
        'Source traceability and evidence weighting',
        'Forward-looking claim discipline',
        'Structural readability and information density',
        'Decision usefulness',
    ]
    for dim in dimensions:
        assert dim in content, f"Missing dimension '{dim}' in prog lang artifact"


def test_c2_prog_lang_has_candidate_summary():
    """C2: Programming language artifact MUST contain Candidate-action summary."""
    content = read(PROG_LANG_ARTIFACT)
    assert 'Candidate-action summary' in content, "Missing Candidate-action summary"


def test_c2_prog_lang_documents_turn_citations():
    """C2: Programming language artifact MUST document turn... citations as rejected."""
    content = read(PROG_LANG_ARTIFACT)
    assert re.search(r'turn\d+|turn.*citation|不可交付|不可采纳|rejected', content, re.IGNORECASE), \
        "Prog lang artifact must document turn... citation as rejected"


# ═══════════════════════════════════════════════════════════════════
# C3: Both artifacts reference related issues
# ═══════════════════════════════════════════════════════════════════

def test_c3_world_cup_references_issues():
    """C3: World cup artifact MUST reference relevant issues #306, #307, #309."""
    content = read(WORLD_CUP_ARTIFACT)
    for issue_num in ['306', '307', '309']:
        assert f'#{issue_num}' in content, f"World cup artifact must reference #{issue_num}"


def test_c3_prog_lang_references_issues():
    """C3: Programming language artifact MUST reference relevant issues #306, #308, #309."""
    content = read(PROG_LANG_ARTIFACT)
    for issue_num in ['306', '308', '309']:
        assert f'#{issue_num}' in content, f"Prog lang artifact must reference #{issue_num}"


# ═══════════════════════════════════════════════════════════════════
# C4: Both artifacts have Case identity and Triage notes
# ═══════════════════════════════════════════════════════════════════

def test_c4_world_cup_has_case_identity():
    """C4: World cup artifact MUST have Case identity section."""
    content = read(WORLD_CUP_ARTIFACT)
    assert 'Case identity' in content


def test_c4_world_cup_has_triage():
    """C4: World cup artifact MUST have Triage notes."""
    content = read(WORLD_CUP_ARTIFACT)
    assert 'Triage notes' in content or 'Things explicitly rejected' in content


def test_c4_prog_lang_has_case_identity():
    """C4: Programming language artifact MUST have Case identity section."""
    content = read(PROG_LANG_ARTIFACT)
    assert 'Case identity' in content


def test_c4_prog_lang_has_triage():
    """C4: Programming language artifact MUST have Triage notes."""
    content = read(PROG_LANG_ARTIFACT)
    assert 'Triage notes' in content or 'Things explicitly rejected' in content


# ═══════════════════════════════════════════════════════════════════
# C5: Both artifacts have Final judgment section
# ═══════════════════════════════════════════════════════════════════

def test_c5_world_cup_has_final_judgment():
    """C5: World cup artifact MUST have Final judgment section."""
    content = read(WORLD_CUP_ARTIFACT)
    assert 'Final judgment' in content


def test_c5_prog_lang_has_final_judgment():
    """C5: Programming language artifact MUST have Final judgment section."""
    content = read(PROG_LANG_ARTIFACT)
    assert 'Final judgment' in content


# ═══════════════════════════════════════════════════════════════════
# C6: candidate-rule-registry.md entries
# ═══════════════════════════════════════════════════════════════════

def test_c6_registry_mentions_world_cup():
    """C6: Registry MUST mention world cup constrained choice case."""
    content = read(REGISTRY)
    assert 'world-cup' in content or 'world cup' in content.lower() or '世界杯' in content, \
        "Registry must reference world cup case"


def test_c6_registry_mentions_prog_lang():
    """C6: Registry MUST mention programming language learning case."""
    content = read(REGISTRY)
    assert 'programming' in content or '编程语言' in content or 'language learning' in content.lower(), \
        "Registry must reference programming language learning case"


# ═══════════════════════════════════════════════════════════════════
# C7: Cross-file invariants (property-based)
# ═══════════════════════════════════════════════════════════════════

def test_c7_artifacts_have_action_type():
    """C7: BOTH artifacts MUST contain Action type labels."""
    wc = read(WORLD_CUP_ARTIFACT)
    pa = read(PROG_LANG_ARTIFACT)
    for content, name in [(wc, 'world cup'), (pa, 'prog lang')]:
        assert re.search(r'NEW_RULE|CHECKLIST_HARDENING|TEMPLATE_CHANGE|NO_ACTION', content), \
            f"{name} artifact must have Action type labels"


def test_c7_artifacts_have_dimension_action_sections():
    """C7: BOTH artifacts MUST have per-dimension Gap + Action type sections."""
    wc = read(WORLD_CUP_ARTIFACT)
    pa = read(PROG_LANG_ARTIFACT)
    for content, name in [(wc, 'world cup'), (pa, 'prog lang')]:
        # Each dimension should have a per-dimension action type (### Action type)
        action_types = re.findall(r'^### Action type$', content, re.MULTILINE)
        assert len(action_types) >= 3, f"{name} has {len(action_types)} action types (need >=3)"
        # Each dimension should identify the gap
        gaps = re.findall(r'^### Gap$', content, re.MULTILINE)
        assert len(gaps) >= 3, f"{name} has {len(gaps)} gap sections (need >=3)"


def test_c7_registry_entry_format():
    """C7: Registry entries MUST include Source file(s) and Coverage status."""
    content = read(REGISTRY)
    assert '已覆盖' in content or '无覆盖' in content or 'Coverage status' in content, \
        "Registry must contain coverage tracking columns"


if __name__ == '__main__':
    tests = [
        # C1: World cup artifact
        ("C1: world cup exists", test_c1_world_cup_artifact_exists),
        ("C1: world cup 6 dimensions", test_c1_world_cup_has_six_dimensions),
        ("C1: world cup candidate summary", test_c1_world_cup_has_candidate_summary),
        ("C1: world cup turn citations", test_c1_world_cup_documents_turn_citations),

        # C2: Programming language artifact
        ("C2: prog lang exists", test_c2_prog_lang_artifact_exists),
        ("C2: prog lang 6 dimensions", test_c2_prog_lang_has_six_dimensions),
        ("C2: prog lang candidate summary", test_c2_prog_lang_has_candidate_summary),
        ("C2: prog lang turn citations", test_c2_prog_lang_documents_turn_citations),

        # C3: Issue references (per-artifact relevant issues)
        ("C3: world cup references #306 #307 #309", test_c3_world_cup_references_issues),
        ("C3: prog lang references #306 #308 #309", test_c3_prog_lang_references_issues),

        # C4: Case identity and triage
        ("C4: world cup case identity", test_c4_world_cup_has_case_identity),
        ("C4: world cup triage/rejected", test_c4_world_cup_has_triage),
        ("C4: prog lang case identity", test_c4_prog_lang_has_case_identity),
        ("C4: prog lang triage/rejected", test_c4_prog_lang_has_triage),

        # C5: Final judgment
        ("C5: world cup final judgment", test_c5_world_cup_has_final_judgment),
        ("C5: prog lang final judgment", test_c5_prog_lang_has_final_judgment),

        # C6: Registry
        ("C6: registry world cup", test_c6_registry_mentions_world_cup),
        ("C6: registry prog lang", test_c6_registry_mentions_prog_lang),

        # C7: Cross-file invariants
        ("C7: artifacts have action type", test_c7_artifacts_have_action_type),
        ("C7: artifacts gaps+actions", test_c7_artifacts_have_dimension_action_sections),
        ("C7: registry format", test_c7_registry_entry_format),
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
