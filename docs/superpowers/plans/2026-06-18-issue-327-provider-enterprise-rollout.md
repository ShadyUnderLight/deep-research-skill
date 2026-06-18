# #327 Provider Selection Enterprise Rollout Blueprint

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add enterprise rollout blueprint (recommendation hierarchy, team-size roadmap, TCO template, migration checklist, unresolved-questions link) to the Provider Selection report structure.

**Architecture:** Extend existing references/decision-report-template.md provider-selection sub-template, ROUTING-MATRIX.md visible artifact contract, checklists/option-selection-final-audit.md, references/option-selection-and-shortlist-discipline.md. Add new eval case. Keep existing discipline intact.

**Type Contracts:**
- `decision-report-template.md:245-320`: New provider-selection sub-template MUST contain: recommendation hierarchy (首选/备选/次选/避免), team-size roadmap, migration checklist table, TCO table with boundary declaration, unresolved-questions-to-reversal link. Each feature MUST be gated behind explicit subtype labels.
- `ROUTING-MATRIX.md:141-151`: Visible artifact contract MUST add enterprise rollout items.
- `option-selection-final-audit.md:48-53`: Provider gate MUST add enterprise rollout checks.
- `option-selection-and-shortlist-discipline.md:356-363`: Provider-selection heuristic questions MUST add rollout/TCO questions.

**Tech Stack:** Markdown templates, Python property-based test contracts, eval case Markdown.

---

### Task 1: Write failing contract tests (TDD)

**Files:**
- Create: `tests/test_issue_327_contracts.py`
- Create: `evals/cases/provider-selection-enterprise-rollout-missing-case.md`

**Steps:**

- [ ] **Step 1: Write contract test file**

```python
# tests/test_issue_327_contracts.py
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


# ═══════════════════════════════════════════════════════════════════
# C1: decision-report-template.md has enterprise rollout sub-template
# ═══════════════════════════════════════════════════════════════════

def test_c1a_has_recommendation_hierarchy():
    """C1a: provider-selection template has 首选/备选/次选/避免 hierarchy."""
    content = read("references/decision-report-template.md")
    assert re.search(r'首选.*备选.*次选.*避免', content), \
        "Missing recommendation hierarchy (首选/备选/次选/避免)"

def test_c1b_has_team_size_roadmap():
    """C1b: provider-selection template has team-size roadmap (小团队/中型/大型)."""
    content = read("references/decision-report-template.md")
    assert re.search(r'小团队|小型团队|中型团队|大型团队|治理成熟度', content), \
        "Missing team-size governance roadmap"

def test_c1c_has_migration_checklist():
    """C1c: provider-selection template has migration checklist with security/identity/CI/training."""
    content = read("references/decision-report-template.md")
    assert re.search(r'inventory|安全|SSO|SCIM|RBAC|审计|培训.*试运行|退出条件', content), \
        "Missing migration checklist items"

def test_c1d_has_tco_template():
    """C1d: provider-selection template has TCO template with direct/network/audit/integration/training/contract/switching."""
    content = read("references/decision-report-template.md")
    assert re.search(r'TCO|总拥有成本|直接费.*网络|seat.*API.*网络.*审计.*培训.*合同.*切换', content), \
        "Missing TCO template"

def test_c1e_tco_has_boundary():
    """C1e: TCO template requires boundary declaration (included/excluded)."""
    content = read("references/decision-report-template.md")
    assert re.search(r'included.*excluded|边界声明|included/excluded boundary', content), \
        "TCO template missing boundary declaration"

def test_c1f_tco_has_cost_role_labels():
    """C1f: TCO template requires cost role labels (observed/estimate/assumption/model-output)."""
    content = read("references/decision-report-template.md")
    assert re.search(r'observed.*estimate.*assumption.*model-output|成本角色|数据角色', content), \
        "TCO template missing cost role labels"

def test_c1g_has_unresolved_questions():
    """C1g: provider-selection template links unresolved questions to recommendation strength."""
    content = read("references/decision-report-template.md")
    assert re.search(r'未决问题.*推荐强度|unresolved.*recommendation|改变推荐.*未确认', content), \
        "Missing unresolved-questions-to-recommendation-strength link"


# ═══════════════════════════════════════════════════════════════════
# C2: ROUTING-MATRIX.md visible artifact contract updated
# ═══════════════════════════════════════════════════════════════════

def test_c2a_routing_has_enterprise_rollout():
    """C2a: ROUTING-MATRIX.md Provider Selection artifact contract mentions enterprise rollout."""
    content = read("ROUTING-MATRIX.md")
    route_section = content[content.find("## Route: Provider / Vendor Selection"):]
    route_section = route_section[:route_section.find("## ")] if "## " in route_section[1:] else route_section
    matches = re.search(r'recommendation hierarchy|首选.*备选|TCO.*边界|迁移.*checklist|企业落地|enterprise rollout', route_section)
    assert matches, \
        "ROUTING-MATRIX.md Provider Selection section missing enterprise rollout in artifact contract"

def test_c2b_routing_has_unresolved_link():
    """C2b: ROUTING-MATRIX.md artifact contract links unresolved questions to ranking."""
    content = read("ROUTING-MATRIX.md")
    route_section = content[content.find("## Route: Provider / Vendor Selection"):]
    route_section = route_section[:route_section.find("## ")] if "## " in route_section[1:] else route_section
    assert re.search(r'unresolved|未决问题|未确认.*排名|unknown.*ranking', route_section), \
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
    assert re.search(r'团队规模|小团队|中型|大型|治理成熟度', content), \
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
    route_section = content[content.find("## Route: Provider / Vendor Selection"):]
    route_section = route_section[:route_section.find("## ")] if "## " in route_section[1:] else route_section
    assert "stale anchor" in route_section, \
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
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python tests/test_issue_327_contracts.py`
Expected: FAIL — all C1, C2, C3, C4, C5 tests fail because content doesn't exist yet

- [ ] **Step 3: Write eval case for missing enterprise rollout**

Write `evals/cases/provider-selection-enterprise-rollout-missing-case.md`:
- Scenario: A provider-selection report that has strong ranking, current-state verification, source traceability and shortlist logic, but completely lacks:
  - Recommendation hierarchy (only ranked list, no 首选/备选/次选/避免)
  - Team-size governance roadmap
  - Migration/rollout checklist
  - TCO with boundary declaration
  - Unresolved questions linked to recommendation strength
- Expected verdict: CONDITIONAL PASS or WARNING — structure exists but enterprise rollout layer missing
- Failure pattern documented: "选型结构强但企业落地缺失"

- [ ] **Step 4: Commit tests as failing (TDD red)**

```bash
git add tests/test_issue_327_contracts.py evals/cases/provider-selection-enterprise-rollout-missing-case.md
git commit -m "test: add failing contract tests for #327 enterprise rollout blueprint"
```

---

### Task 2: Update decision-report-template.md provider-selection sub-template

**Files:**
- Modify: `references/decision-report-template.md:220-250` (insert enterprise rollout sub-template after existing 11-section structure)

**Type contract for this task:**
New provider-selection enterprise rollout block MUST:
1. Start with a header like `### Enterprise rollout blueprint (provider-selection专用)` or similar
2. Contain a recommendation hierarchy table (首选/备选/次选/避免)
3. Contain a team-size governance maturity roadmap (小/中/大)
4. Contain a migration/rollout checklist
5. Contain a TCO template with boundary declaration and cost role labels
6. Contain an unresolved-questions-to-recommendation-strength link
7. Be explicitly scoped as "supplementary to the 11-section structure, not a replacement"

- [ ] **Step 1: Write the enterprise rollout sub-template block**

Insert after line ~239 (after "current SLA / status / enterprise controls when decision-relevant") in `references/decision-report-template.md`.

```markdown

**Provider-selection 企业落地蓝图（当读者需要将推荐转化为采购/实施决策时，在 11 节结构之上附加以下内容）：**

当读者是企业采购者、技术选型负责人或平台治理团队时，纯排名不足以支持落地决策。在完成上述 11 节结构后，附加以下企业落地蓝图。

### 推荐层级

避免只给总分排名。按角色分类：

| 层级 | Provider | 适用条件 | 不适用条件 | 反转条件 |
|------|----------|---------|-----------|---------|
| **首选** Primary | | | | |
| **备选** Secondary | | | | |
| **次选** Tertiary | | | | |
| **避免** Avoid / Excluded | | | | |

规则：
- 首选 = 当前约束下最优；备选 = 首选不可行时的合理替代；次选 = 特定场景下可行但通常不推荐；避免 = 当前约束下有明确缺陷。
- 每个层级必须标注适用条件和不适用条件，避免笼统的"较好/较差"。
- 反转条件说明什么变化会使该 provider 跳到另一层级。

### 团队规模与治理成熟度路线

对同一个推荐结果，不同团队规模需要不同的实施路径：

| 团队/组织类型 | 实施路径 | 重点 | 不宜做的事 |
|-------------|---------|------|-----------|
| **小团队**（1-20 人） | 低治理成本、快速试点；个人账号 + 简单配额 | 工具体验、单价、快速上线 | 不要采购企业合同、不要过早锁 SSO/SCIM |
| **中型团队**（20-200 人） | 统一账号、仓库策略、成本配额；引入基本治理 | 账号管理、权限控制、预算管控 | 不要引入完整 GRC 流程拖慢速度 |
| **大型/受监管团队**（200+ 人） | SSO/SCIM、审计日志、数据保留、合同/SLA、采购和法务流程 | 合规、数据主权、供应商管理 | 不要跳过试点直接全面上线 |

规则：
- 如果推荐结论本身与团队规模无关，说明"推荐结论稳定，但实施路径按以下规模调整"。
- 如果推荐结论随团队规模变化（如小团队免费版够用、大团队需要企业版），必须在推荐层级中体现。

### 迁移与上线 checklist

在选定供应商后，按此 checklist 规划上线：

| 阶段 | 事项 | 完成标准 | 风险/备注 |
|------|------|---------|----------|
| 1. 现状 inventory | 当前工具/仓库/IDE/CI 资产盘点 | 清单完成，了解迁移影响范围 | 遗漏关键依赖导致迁移延期 |
| 2. 网络与访问验证 | 大陆/目标地区可达性、延迟、带宽测试 | 网络条件满足生产使用要求 | 区域性网络限制可能阻断迁移 |
| 3. 安全与合规评估 | 数据使用政策、训练政策、数据驻留、行业合规要求 | 供应商行为符合组织安全基线 | 法律/合规未清可能造成风险 |
| 4. 代表性任务 pilot | 选取 1-3 个真实任务进行 pilot 与基准对比 | pilot 结果达到或超过原有方案基线 | pilot 范围过窄无法暴露真实问题 |
| 5. 账号与身份集成 | 账号创建、SSO/SCIM、RBAC 角色分配、审计日志配置 | 身份治理流程正常运行 | 企业目录变更影响面大 |
| 6. 仓库/CI/IDE 集成 | 代码仓库、CI 流水线、开发环境与供应商工具集成 | 集成后开发流程无中断 | API 兼容性或自定义配置缺失 |
| 7. 培训与规范 | 团队培训、使用规范、人工复核边界、升级路径 | 团队可独立使用并知道升级路径 | 无培训导致采用率低、误用 |
| 8. 试运行与全面上线 | 试运行、退出条件定义、全面上线、老系统关停计划 | 试运行达标后逐步切换 | 确保退出条件事先定义且可执行 |

### 完整 TCO 模板

TCO 必须声明 included / excluded boundary，且每个成本数字标注角色标签（observed / estimate / assumption / model-output）：

| 成本类别 | 估算值 | 角色标签 | 说明 |
|---------|-------|---------|------|
| **seat/API 直接费用** | | | 许可证、API 调用量、席位费 |
| 网络/VPN/专线/代理 | | | 出口带宽、CDN、代理搭建 |
| 企业合同与采购成本 | | | 招标、法务审查、合同管理 |
| 安全合规审计 | | | 渗透测试、合规审查、审计日志存储 |
| 集成与运维人力 | | | 集成开发、日常运维、故障响应 |
| 培训与迁移损耗 | | | 团队培训、迁移期间产能折损 |
| 折扣、最低承诺、超额用量 | | | 承诺消费折扣、超额费率 |
| 退出/切换成本 | | | 数据导出、重新集成、人员再培训 |

**边界声明：** included / excluded boundary 必须在 TCO 表之前明确写出。例如："本 TCO 覆盖 seat 费用和网络成本，不覆盖法务审查和退出成本。"

**规则：**
- 每个数字必须标 `observed` / `estimate` / `assumption` / `model-output`。
- 如果某个成本无法估算，标注 `not estimated` 并说明为什么无法估算。
- 折扣和最低承诺必须标注是公开定价还是协商报价（vendor-claim / observed / assumption）。

### 未决问题与推荐强度

对无法确认的大陆可访问性、合同主体、数据出境、行业许可、本地替代方案等不得用"通常/可能"补全。使用以下结构：

| 未决问题 | 如果为"是" | 如果为"否" | 对推荐层级的影响 | 信息来源尝试 |
|---------|-----------|-----------|----------------|------------|
| 该供应商在大陆是否有可签约主体？ | 首选保持 | 首选→备选或避免 | 大陆无签约主体则推荐降级 | 尝试联系销售（未确认） |

规则：
- 每个未决问题必须说明分别影响哪些层级的推荐。
- 如果未决问题数量 > 3 且涉及推荐层级变化，应在 executive summary 中标注"推荐稳定性：中/低"。
- 不得虚构或猜测未确认信息；信息缺口本身是一类发现。
```

- [ ] **Step 2: Run tests to verify C1 passes**

Run: `python tests/test_issue_327_contracts.py`
Expected: All C1 tests now pass. C2-C5 still fail.

- [ ] **Step 3: Commit**

```bash
git add references/decision-report-template.md
git commit -m "feat(#327): add enterprise rollout blueprint to provider-selection sub-template"
```

---

### Task 3: Update ROUTING-MATRIX.md visible artifact contract

**Files:**
- Modify: `ROUTING-MATRIX.md:141-151` (extend visible artifact contract)

- [ ] **Step 1: Add enterprise rollout items to artifact contract**

In the `### Visible artifact contract` section under `## Route: Provider / Vendor Selection`, add after "accessibility / compliance / data-control / SLA treatment when relevant":

```markdown
- **enterprise rollout layer when the reader is a buyer or governance team:**
  - recommendation hierarchy (首选 / 备选 / 次选 / 避免) rather than only a scored ranking
  - team-size / governance-maturity roadmap (small / medium / large / regulated)
  - migration and rollout checklist covering security, identity, repo/CI, training, trial run, and exit
  - TCO with explicit included/excluded boundary and cost role labels (observed / estimate / assumption / model-output)
  - unresolved questions linked to recommendation-tier strength and reversal conditions
```

Also update the hard-fail section (line 152-156) to add:
```markdown
- presents a scored ranking without recommendation hierarchy when the reader is an enterprise buyer
```

- [ ] **Step 2: Run tests to verify C2 passes**

Run: `python tests/test_issue_327_contracts.py`
Expected: C2a, C2b pass. C3-C5 still fail.

- [ ] **Step 3: Commit**

```bash
git add ROUTING-MATRIX.md
git commit -m "feat(#327): update provider-selection artifact contract with enterprise rollout"
```

---

### Task 4: Update option-selection-final-audit.md with enterprise rollout gate

**Files:**
- Modify: `checklists/option-selection-final-audit.md:48`

- [ ] **Step 1: Add enterprise rollout sub-section to provider gate**

After line 53 (`# Provider / vendor current-state gate`), add a new sub-section:

```markdown
### Enterprise rollout gate

When the reader is an enterprise buyer, governance team, or the provider-selection report will be used for procurement decisions, also run these checks:

- [ ] the report includes a recommendation hierarchy (首选/备选/次选/avoid) rather than only a scored ranking or flat shortlist
- [ ] the report shows how team size or governance maturity changes the implementation path, or explicitly states that the recommendation is stable across team scales
- [ ] the report includes a migration/rollout checklist covering at least: inventory, network verification, security/compliance assessment, pilot, identity/SSO/SCIM, repo/CI integration, training, trial run, and exit conditions
- [ ] the report includes a TCO breakdown with direct fees, network, audit, integration, training, contract, and switching costs, with an explicit included/excluded boundary
- [ ] all TCO line items carry a cost role label (observed / estimate / assumption / model-output); unestimated items are marked `not estimated` with a reason
- [ ] unresolved questions (mainland accessibility, contracting entity, data cross-border, industry licensing, local alternatives) are linked to recommendation-tier strength and reversal conditions
- [ ] if the report lacks these enterprise rollout layers despite being used for procurement, the executive summary calls out this gap explicitly
```

- [ ] **Step 2: Run tests to verify C3 passes**

Run: `python tests/test_issue_327_contracts.py`
Expected: C3a, C3b, C3c pass. C4, C5 still fail.

- [ ] **Step 3: Commit**

```bash
git add checklists/option-selection-final-audit.md
git commit -m "feat(#327): add enterprise rollout gate to option-selection audit"
```

---

### Task 5: Update option-selection-and-shortlist-discipline.md with rollout questions

**Files:**
- Modify: `references/option-selection-and-shortlist-discipline.md:356`

- [ ] **Step 1: Add enterprise rollout heuristic questions**

After line 362 (`Is the output becoming a vendor encyclopedia instead of a ranked provider-choice memo?`), add:

```markdown
When the task involves enterprise provider selection with procurement or rollout decisions, also ask:

- Who is the reader: an individual developer choosing a tool, or an enterprise buyer/governance team managing procurement and rollout?
- Would the recommendation change if the team were 5 people vs 200 people?
- Is a simple cost comparison sufficient, or does the decision require a full TCO with network/audit/training/switching cost?
- Are there unresolved compliance, accessibility, data-residency, or contracting questions that could change the recommendation from primary to avoid?
- Does the reader need a migration and rollout plan, not just a ranking?
- Are cost numbers labeled with their data role (observed / estimate / assumption / vendor-claim / model-output), and is the TCO boundary declared?
```

- [ ] **Step 2: Run tests to verify C4 passes**

Run: `python tests/test_issue_327_contracts.py`
Expected: C4a passes. C5 still fails (eval case not yet committed with code).

- [ ] **Step 3: Commit**

```bash
git add references/option-selection-and-shortlist-discipline.md
git commit -m "feat(#327): add enterprise rollout heuristic questions to provider-selection discipline"
```

---

### Task 6: Write eval case for enterprise rollout

**Files:**
- Create: `evals/cases/provider-selection-enterprise-rollout-missing-case.md`

Note: The eval case was created in TDD Task 1 Step 3. This task ensures it exists and is committed.

- [ ] **Step 1: Verify eval case exists**

Run: `python tests/test_issue_327_contracts.py`
Expected: ALL PASS.

- [ ] **Step 2: Commit eval case if not already committed**

```bash
git add evals/cases/provider-selection-enterprise-rollout-missing-case.md
git commit -m "feat(#327): add eval case for enterprise rollout missing failure pattern"
```

- [ ] **Step 3: Run all tests to confirm final state**

Run: `python tests/test_issue_327_contracts.py`
Expected: ALL PASS.  ✅

---

### Task 7: Final verification and PR

- [ ] **Step 1: Run full test suite**

```bash
python tests/test_issue_327_contracts.py
python scripts/test_audit_report.py
```

- [ ] **Step 2: Verify no regressions on existing tests**

```bash
python -m pytest tests/ -v --tb=short 2>&1 | head -80
```

- [ ] **Step 3: Create PR**
