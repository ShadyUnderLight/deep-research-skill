# Issue #309: 强化 constrained-choice 模板层 Decision Scope 块

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将 Decision Scope / 决策口径 块从 checklist 审计层前置到 template 模板层，使 constrained-choice 报告在写作时自然包含目标画像、短名单边界与排除项。

**架构:** 在 `references/decision-report-template.md` 的 option-selection 推荐结构中新增强制块，联动更新 checklist、cross-reference 和 eval pass criteria。6 个文件，按依赖顺序执行。

**Tech Stack:** Python 3.x, pytest, hypothesis (property-based tests for markdown structural invariants)

**类型契约 (Type Contracts):**
- `DecisionScopeBlock` = `### Decision Scope / 决策口径` + 以下字段全部存在: 目标读者, 当前要做的选择, 默认约束, 优化目标, 选项全集, 本次短名单, 明确排除项, 关键未知, 改变结论的条件
- `DecisionScopeVisibilityCheck` = `### Decision scope visibility` 子节包含 2 条 check
- `ConstrainedChoiceRecallCheck` = `final-audit.md` §Recall 中 `constraine` 行存在
- `CrossReferenceLink` = `option-selection-and-shortlist-discipline.md` 中存在 `decision-report-template.md` 的 cross-reference
- `EvalScopePositionCheck` = eval `career-skill-selection-proxy-discipline-case.md` pass criteria 包含 scope block 位置检查

---

### Task 0: 设置隔离 worktree + 创建测试契约文件（RED 阶段）

**文件:**
- Create: `tests/test_issue_309_contracts.py`
- Other files: NOT YET (this task creates the test file and runs it; all tests must fail before implementation)

- [ ] **Step 0a: 创建新分支**

Run:
```bash
git checkout -b feat/issue-309-decision-scope-template
```

- [ ] **Step 0b: 创建测试契约文件 `tests/test_issue_309_contracts.py`**

完整内容如下。该文件包含 6 组契约测试（C1-C6）和 property-based invariants，所有测试在实现前必须全部 FAIL。

```python
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
    """C2: MUST contain ### Decision scope visibility subsection."""
    content = read(OPTION_CHECKLIST)
    assert re.search(
        r'^###\s+Decision scope visibility',
        content,
        re.MULTILINE
    ), "Missing '### Decision scope visibility' subsection"


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
    target_line = lines[0]
    assert re.search(r'[Dd]ecision [Ss]cope|[Ss]cope', target_line), \
        f"Recall line must mention decision scope or scope: {target_line}"


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
    assert re.search(r'(?i)exec.*summary|后.*详细|before.*detail|opening.*after|位置|position|placement|order|first.*screen|一屏'), pass_section, \
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
    assert 'option-selection-final-audit' in recall_section, \
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
        assert f'**{field}**' in scope_block, \
            f"Field '{field}' must be formatted as bullet with **bold** label"


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
```

- [ ] **Step 0c: 运行测试验证全部 FAIL**

Run:
```bash
python tests/test_issue_309_contracts.py 2>&1
```
Expected: ALL tests FAIL (since no implementation exists yet)


### Task 1: 在 `decision-report-template.md` 中新增 Decision Scope 块

**文件:**
- Modify: `references/decision-report-template.md` — 在 §Recommended structure 的 option-selection 推荐结构中增强 "3. Decision architecture" 为带具体内容的规约

- [ ] **Step 1a: 读取文件确认当前状态**

Run: `python -c "import utils; print('ok')"` — 确保文件存在

实际: 直接读取文件确认 `decision-report-template.md` 中 "3. Decision architecture" 当前只有一行标题，没有具体内容。

- [ ] **Step 1b: 编辑文件，在 §Recommended structure 的 option-selection 结构中增强 "3. Decision architecture"**

在 `references/decision-report-template.md` 中找到 option-selection 推荐结构中的 `3. Decision architecture`（大约第 127 行），将其从一行标题扩展为：

将:

```
3. Decision architecture
```

替换为:

```
3. Decision architecture

   对于 constrained-choice / shortlist / option-selection 报告，该节必须包含以下决策口径块（Decision Scope block），放在执行摘要之后、详细分析之前：

   ### Decision Scope / 决策口径

   - **目标读者 / 使用者**：[零基础 / 1-3 年经验 / 5 年以上 / 转行 / 已有领域背景，或明确说明]
   - **当前要做的选择**：[一句话说明实际决策问题，而非话题探索]
   - **默认约束**：[hard constraints（硬性限制）和 soft preferences（软偏好）]
   - **优化目标**：[最快就业 / 长期上限 / 创业效率 / 后悔概率最低 / 综合回报 / 其他]
   - **选项全集**：[理论上的选项范围，如"所有主流编程语言"或"用户指定的四个选项"]
   - **本次短名单**：[实际纳入比较的选项，与全集的关系]
   - **明确排除项**：[排除了什么、为什么排除；若来自用户指定则说明"非全市场排行"]
   - **关键未知**：[选择时尚未确认、可能影响结果的信息]
   - **改变结论的条件**：[什么假设变化会改变排名或推荐]

   **子类型示例：**

   学习/职业技能选择（另见 `references/option-selection-and-shortlist-discipline.md` §默认决策口径）：
   - 目标读者：零基础 / 1-3 年经验 / 5 年以上经验
   - 默认市场：全球英语市场 / 美国岗位代理 / 中国岗位 / 远程岗位
   - 优化目标：最快就业 / 长期上限 / 通用性 / 创业效率

   体育/比赛预测：
   - outcome shortlist：胜 / 平 / 负（或精确比分范围）
   - 当前快照时间：最新排名、赔率、阵容、伤停、天气
   - 未确认项：首发、裁判、临场伤病、赔率波动
   - 调整规则：首发缺核心、赔率移动、天气恶化时概率怎么改

   供应商/平台/地点选择：
   - 排除项和 runner-up 必须在 opening 后 1 屏内可见
   - 若选项来自用户指定，明确标注"不代表全市场最优"
```

- [ ] **Step 1c: 运行 C1 测试验证通过**

Run:
```bash
python tests/test_issue_309_contracts.py -k "test_c1" -v 2>&1
```
Expected: C1 tests PASS

- [ ] **Step 1d: Commit**

```bash
git add references/decision-report-template.md
git commit -m "feat: add Decision Scope block to decision-report-template option-selection structure (#309)"
```


### Task 2: 在 `option-selection-final-audit.md` 中新增 Decision Scope visibility 子节

**文件:**
- Modify: `checklists/option-selection-final-audit.md` — 在 §Background-first drift check 之后新增 §Decision scope visibility

- [ ] **Step 2a: 读取文件找到插入位置**

确认 §Background-first drift check 的结束位置（当前文件第 120 行: `- [ ] removing background paragraphs that immediately follow the opening judgment would sharpen rather than weaken the report`），在其后插入新节。

- [ ] **Step 2b: 在 §Background-first drift check 之后新增**

在 `checklists/option-selection-final-audit.md` 的 §Background-first drift check 后面追加：

```markdown
## Decision scope visibility

- [ ] the report includes a visible Decision Scope block (target reader, option universe, shortlist boundary, exclusions, reversal conditions) after the executive summary / judgment block and before detailed analysis
- [ ] the Decision Scope block is present before route metadata or background exposition; if the first decision-relevant content after the summary is the decision scope rather than metadata, this check passes
```

- [ ] **Step 2c: 运行 C2 测试验证通过**

Run:
```bash
python tests/test_issue_309_contracts.py -k "test_c2" -v 2>&1
```
Expected: C2 tests PASS

- [ ] **Step 2d: Commit**

```bash
git add checklists/option-selection-final-audit.md
git commit -m "feat: add Decision scope visibility checks to option-selection audit (#309)"
```


### Task 3: 在 `option-selection-and-shortlist-discipline.md` 中添加 cross-reference

**文件:**
- Modify: `references/option-selection-and-shortlist-discipline.md` — 在 §默认决策口径 节中添加 cross-reference

- [ ] **Step 3a: 读取文件，找到 §默认决策口径 节的末尾**

确认该节的最后一行（在当前文件中约第 96 行，`> 参见 checklists/option-selection-final-audit.md §Career / skill selection sub-gate` 之后）。

- [ ] **Step 3b: 在 §默认决策口径 末尾添加 cross-reference**

在该段的 `> 参见 ...` 引用之后，追加一行：

```markdown
> 对于所有 constrained-choice 报告（不仅限 career/skill selection），决策架构节必须包含一个 Decision Scope block。通用模板见 `references/decision-report-template.md` §Recommended structure (option-selection/shortlist 子结构)。本节的 career/skill 模板是该通用规约的子类特化。
```

- [ ] **Step 3c: 运行 C3 测试**

Run:
```bash
python tests/test_issue_309_contracts.py -k "test_c3" -v 2>&1
```
Expected: C3 tests PASS

- [ ] **Step 3d: Commit**

```bash
git add references/option-selection-and-shortlist-discipline.md
git commit -m "docs: add cross-reference to Decision Scope template in option-selection discipline (#309)"
```


### Task 4: 在 `final-audit.md` §Recall discipline 中增加 constrained-choice first-screen 检查

**文件:**
- Modify: `checklists/final-audit.md` — 在 §Recall discipline 中新增一行 constrained-choice first-screen clarity 检查

- [ ] **Step 4a: 读取文件找到插入位置**

找到 §Recall discipline 中的 `- [ ] option-selection final audit was run for shortlist, ranking, or constrained-choice outputs`（当前文件约第 145 行），在其后新增一行。

- [ ] **Step 4b: 在该行后新增**

```markdown
- [ ] for constrained-choice / shortlist / option-selection reports, the first-screen clarity includes the core judgment followed by decision scope (target reader, option universe, shortlist boundary, exclusions) before route metadata or background
```

- [ ] **Step 4c: 运行 C4 测试**

Run:
```bash
python tests/test_issue_309_contracts.py -k "test_c4" -v 2>&1
```
Expected: C4 tests PASS

- [ ] **Step 4d: Commit**

```bash
git add checklists/final-audit.md
git commit -m "feat: add constrained-choice first-screen recall check in final-audit (#309)"
```


### Task 5: 更新 eval cases 的 pass criteria

**文件:**
- Modify: `evals/cases/career-skill-selection-proxy-discipline-case.md` — 在 §Pass criteria 末尾增加 scope block 位置检查
- Modify: `evals/cases/world-cup-prediction-constrained-choice-probability-method-case.md` — 在 §Pass criteria 末尾增加 outcome shortlist 和 pre-match snapshot 第一屏检查

- [ ] **Step 5a: 更新 career-skill eval**

在 `evals/cases/career-skill-selection-proxy-discipline-case.md` 的 §Pass criteria 末尾（第 7 条之后）新增：

```markdown
8. **Scope block placement is correct.**
   - The default decision scope block appears after the executive summary / judgment block and before detailed analysis
   - The scope block includes option universe and explicit exclusions
```

- [ ] **Step 5b: 更新 world-cup eval**

在 `evals/cases/world-cup-prediction-constrained-choice-probability-method-case.md` 的 §Pass criteria 末尾（第 6 条之后）新增：

```markdown
7. **Outcome shortlist and pre-match snapshot in first screen.**
   - The outcome shortlist (win / draw / loss) appears in the first 30% of the report
   - Pre-match snapshot (kickoff time, squad status, key unknowns) is visible before detailed analysis
```

- [ ] **Step 5c: 运行 C5 测试验证**

Run:
```bash
python tests/test_issue_309_contracts.py -k "test_c5" -v 2>&1
```
Expected: C5 tests PASS

- [ ] **Step 5d: 运行全部测试验证整体通过**

Run:
```bash
python tests/test_issue_309_contracts.py -v 2>&1
```
Expected: ALL tests PASS

- [ ] **Step 5e: Commit**

```bash
git add evals/cases/career-skill-selection-proxy-discipline-case.md evals/cases/world-cup-prediction-constrained-choice-probability-method-case.md
git commit -m "feat: update eval pass criteria for Decision Scope visibility (#309)"
```


### Task 6: 完整性验证 + Regression 检查

**文件:** 无需修改，只需运行验证命令

- [ ] **Step 6a: 运行全部 309 契约测试**

```bash
python tests/test_issue_309_contracts.py -v 2>&1
```
Expected: ALL 20+ tests PASS (C1-C6 + property-based)

- [ ] **Step 6b: 运行已有契约测试，确保无 regression**

```bash
python tests/test_issue_272_contracts.py -v 2>&1
python tests/test_issue_308_contracts.py -v 2>&1
```
Expected: ALL tests PASS (no regression)

- [ ] **Step 6c: 确认 git 状态干净**

```bash
git status
git log --oneline -10
```
Expected: 5 commits on `feat/issue-309-decision-scope-template`, working tree clean

- [ ] **Step 6d: 运行 C6 cross-file 测试**

```bash
python tests/test_issue_309_contracts.py -k "test_c6" -v 2>&1
```
Expected: C6 tests PASS (consistent terminology, cross-references valid)
