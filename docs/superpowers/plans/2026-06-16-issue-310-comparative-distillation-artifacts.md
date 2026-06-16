# Issue #310: 将两组 GPT 对照沉淀为 comparative-distillation artifact 与回归 eval

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development

**Goal:** 将世界杯预测和编程语言学习两组 GPT-vs-本地对比报告沉淀为 comparative-distillation 归档资产

**Architecture:** 两个新 artifact 文件使用现有模板 + candidate-rule-registry 更新 + INDEX 索引更新。纯新增，不改已有逻辑。

**Tech Stack:** Markdown (comparative-distillation-template.md)

**类型契约:**
- `WorldCupDistillationArtifact` = `evals/comparative-distillation/world-cup-constrained-choice-gpt-vs-local-comparative-distillation.md` 存在且包含 6 个维度对比 + Candidate-action table + turn... citation 拒绝标注
- `ProgrammingLanguageDistillationArtifact` = `evals/comparative-distillation/programming-language-learning-gpt-vs-local-comparative-distillation.md` 存在且包含相同结构
- `CandidateRegistryEntry` = `candidate-rule-registry.md` 包含这 2 个案例的条目

---

### Task 0: 设置分支 + RED 测试契约

**文件:**
- Create: `tests/test_issue_310_contracts.py`
- Other files: NOT YET

- [ ] **Step 0a: 创建新分支**
```bash
git checkout -b feat/issue-310-comparative-distillation-artifacts
```

- [ ] **Step 0b: 创建 `tests/test_issue_310_contracts.py`**
```python
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
    """C3: World cup artifact MUST reference #306-#309."""
    content = read(WORLD_CUP_ARTIFACT)
    for issue_num in ['306', '307', '308', '309']:
        assert f'#{issue_num}' in content, f"World cup artifact must reference #{issue_num}"


def test_c3_prog_lang_references_issues():
    """C3: Programming language artifact MUST reference #306-#309."""
    content = read(PROG_LANG_ARTIFACT)
    for issue_num in ['306', '307', '308', '309']:
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
    """C7: BOTH artifacts MUST contain Action type labels (NEW_RULE / NO_ACTION etc)."""
    wc = read(WORLD_CUP_ARTIFACT)
    pa = read(PROG_LANG_ARTIFACT)
    for content, name in [(wc, 'world cup'), (pa, 'prog lang')]:
        assert re.search(r'NEW_RULE|CHECKLIST_HARDENING|TEMPLATE_CHANGE|NO_ACTION', content), \
            f"{name} artifact must have Action type labels"


def test_c7_artifacts_have_dimension_action_sections():
    """C7: BOTH artifacts MUST have Dimension N + Candidate action + Action type for each dimension."""
    wc = read(WORLD_CUP_ARTIFACT)
    pa = read(PROG_LANG_ARTIFACT)
    for content, name in [(wc, 'world cup'), (pa, 'prog lang')]:
        # Each dimension should have a candidate action and action type
        candidate_actions = re.findall(r'### Candidate action', content)
        action_types = re.findall(r'### Action type', content)
        assert len(candidate_actions) >= 3, f"{name} has {len(candidate_actions)} candidate actions (need >=3)"
        assert len(action_types) >= 3, f"{name} has {len(action_types)} action types (need >=3)"


def test_c7_registry_entry_format():
    """C7: Registry entries for these cases MUST include Source file(s) and Coverage status."""
    content = read(REGISTRY)
    # The registry table should have rows with coverage status info
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

        # C3: Issue references
        ("C3: world cup references #306-#309", test_c3_world_cup_references_issues),
        ("C3: prog lang references #306-#309", test_c3_prog_lang_references_issues),

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
        ("C7: artifacts dimension actions", test_c7_artifacts_have_dimension_action_sections),
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
```
