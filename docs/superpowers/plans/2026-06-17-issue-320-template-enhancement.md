# Issue #320 Template Enhancement Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Absorb structural strengths from two GPT comparison reports into report templates, checklists, and evals per issue #320.

**Architecture:** Three phases: (0) comparative distillation artifacts, (1) template/checklist updates based on validated patterns, (2) test contracts + PR + cross-review.

**Tech Stack:** Python (contract tests), Markdown (templates/distillations)

---

## SDD: Specification

### Files to Create
| File | Purpose |
|------|---------|
| `evals/comparative-distillation/small-team-ai-agent-gpt-vs-local-comparative-distillation.md` | Comparative distillation #1: small team AI Agent report patterns |
| `evals/comparative-distillation/data-center-power-bottleneck-gpt-vs-local-comparative-distillation.md` | Comparative distillation #2: data center power bottleneck report patterns |
| `tests/test_issue_320_contracts.py` | Property-based contract tests for all issue #320 acceptance criteria |

### Files to Modify
| File | Change |
|------|--------|
| `evals/comparative-distillation/candidate-rule-registry.md` | Add registry entries for new candidates from two new distillation cases |
| `references/report-template.md` | Add Input boundary / 未指定项 section for constrained-choice reports |
| `references/decision-report-template.md` | Enhance Decision Scope block; add option+stages integration structure |
| `references/market-outlook-and-scenario-discipline.md` | Add value-chain sensitivity map, regional coverage matrix, stakeholder action table |
| `checklists/market-outlook-audit.md` | Add checklist items for value-chain, regional coverage, action table |
| `evals/templates/decision-utility-rubric.md` | Optional: add action table quality dimension |

---

## CoT: Design Analysis

### Learning Point 1: Input boundary / 未指定项
**Where it lands:** `references/report-template.md`, in or after the existing **Market-entry / go-no-go memo formatting discipline** section.
**Why there:** The existing template has a Decision Scope block in `decision-report-template.md` but `report-template.md` (the generic template) does not.
**What to add:** A new subsection `未指定项与输入边界` that:
- Shows a compact table for unstated inputs
- Requires unstated inputs to be converted to explicit assumptions
- Establishes linkage: if an assumption change would flip the conclusion → enter uncertainty/sensitivity section
- Trigger: constrained-choice / provider-selection / market-entry / market-outlook with organizational-landing burden

### Learning Point 2: Option comparison + stages integration
**Where it lands:** `references/decision-report-template.md`, inside the **Decision-table discipline** section or the **Decision architecture** subsection.
**Why there:** The market-outlook and option-selection structures in `decision-report-template.md` already have ranking and recommendation. What's missing is the **implementation roadmap** dimension.
**What to add:** Expand the option-selection structure template to include:
- `Implementation stages` (MVP → expansion → steady-state)
- `Owner / operating model` (who owns what)
- `Cost / organizational impact` dimension in comparison
- Trigger: tasks with implementation/rollout burden

### Learning Point 3: Value-chain sensitivity map
**Where it lands:** `references/market-outlook-and-scenario-discipline.md`, as a new subsection after **Drivers vs blockers discipline**.
**What to add:** A template for Value-chain sensitivity map:
- Trigger: topic contains 产业链 / value chain / supply chain / infrastructure chain
- Format: table with Chain layer, Current exposure, Bottleneck mechanism, Beneficiaries/losers, Timing, Evidence strength, What would change conclusion

### Learning Point 4: Regional coverage matrix
**Where it lands:** `references/market-outlook-and-scenario-discipline.md`, as a new subsection after Value-chain sensitivity map.
**What to add:** A template for Regional coverage matrix:
- Trigger: report title/question contains 全球 / global / 区域 / region
- Format: table with Region, Key metrics, Data role (observed/estimate/forecast/scenario/proxy), Source `[Sxx]`, Scope completeness warning if only covering US/China but claiming global

### Learning Point 5: Stakeholder action table
**Where it lands:** `references/market-outlook-and-scenario-discipline.md`, replacing/upgrading the existing **Stakeholder implications discipline** section.
Also lands in: `checklists/market-outlook-audit.md` and `references/decision-report-template.md`.
**What to add:** Upgrade from description-based stakeholder implications to action-table format:
| Stakeholder | Decision to make | Recommended action | Required evidence / metric | Trigger to revise |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |

---

## Phase 0: Comparative Distillation

### Task 0.1: Create small-team AI Agent distillation artifact

**Files:**
- Create: `evals/comparative-distillation/small-team-ai-agent-gpt-vs-local-comparative-distillation.md`

- [ ] **Step 1: Write the distillation file** following `evals/templates/comparative-distillation-template.md`

Content should cover:
- Case identity: research question = "小团队是否应将客服、运营与数据分析统一接入 AI Agent"
- All 6 fixed dimensions
- Key gap: GPT has Input boundary scope table; local template lacks it
- Key gap: GPT has option comparison + stages + owner model; local template has ranking but no implementation roadmap
- Action type per dimension: TEMPLATE_CHANGE for input boundary + value-chain + regional matrix + action table
- Things explicitly rejected: GPT's bibliography-only sourcing, turn... citations, no claim-level `[Sxx]`

- [ ] **Step 2: Verify format matches template**

### Task 0.2: Create data center power bottleneck distillation artifact

**Files:**
- Create: `evals/comparative-distillation/data-center-power-bottleneck-gpt-vs-local-comparative-distillation.md`

- [ ] **Step 1: Write the distillation file** following template

Content should cover:
- Case identity: research question = "全球数据中心电力瓶颈会如何影响 AI 基础设施产业链"
- All 6 fixed dimensions
- Key gap: GPT has value-chain sensitivity map (upstream/midstream/downstream); local template lacks this
- Key gap: GPT has regional comparison table (NA/EU/China/India/SEA/ME/Africa); local template has no regional coverage discipline
- Key gap: GPT has stakeholder-specific action recommendations; local template has generic stakeholder impacts
- Things explicitly rejected: GPT's lack of `[Sxx]` inline citations, no data role labeling for regional numbers

- [ ] **Step 2: Verify format matches template**

### Task 0.3: Update candidate-rule-registry.md

**Files:**
- Modify: `evals/comparative-distillation/candidate-rule-registry.md`

- [ ] **Step 1: Add new entries** for the candidate rules found in both distillation cases:
  1. Rxx: Input boundary / 未指定项 block for constrained-choice templates → TEMPLATE_CHANGE
  2. Rxx: Value-chain sensitivity map for industry-chain market-outlook → TEMPLATE_CHANGE
  3. Rxx: Regional coverage matrix with source role for global scope → TEMPLATE_CHANGE
  4. Rxx: Stakeholder action table (decision/action/metric/trigger) → TEMPLATE_CHANGE
  5. Rxx: Implementation stages integration in option-selection structure → TEMPLATE_CHANGE

---

## Phase 1: Template Updates

### Task 1.1: Update references/report-template.md

**Files:**
- Modify: `references/report-template.md`

- [ ] **Step 1: Add `未指定项与输入边界` subsection**

Add after the existing `Market-entry / go-no-go memo formatting discipline` section (around line 677):

```markdown
### 输入边界与未指定项（constrained-choice / market-entry / market-outlook 建议）

对于 constrained-choice、provider-selection、market-entry、market-outlook 中涉及组织落地或方案选择的问题，建议在决策口径块（或等价位置）中包含以下输入边界表，明确哪些输入是已知的、哪些是假设的、哪些是未指定的。

**为什么需要：** 未经明确说明的"未指定项"如果隐含在结论中，会让读者误以为推荐适用于比实际更宽的场景。

| 边界维度 | 当前指定状态 | 说明 / 假设 / 未指定 |
|---------|-------------|---------------------|
| 组织规模/范围 | 已指定 / 未指定 | |
| 角色构成 | 已指定 / 未指定 | |
| 技术栈现状 | 已指定 / 未指定 | |
| 时间窗口 | 已指定 / 未指定 | |
| 合规/地域约束 | 已指定 / 未指定 | |
| 成本/预算基线 | 已指定 / 未指定 | |
| 优化目标 | 已指定 / 未指定 | |

**规则：**
- 未指定项必须转为显式假设（assumption），而非悄悄补全。
- 若未指定项的任何合理取值会导致结论翻转，该变量必须进入 uncertainty / sensitivity 分析。
- 该表不替代 Decision Scope 块中的排除项，而是补充说明"作者知道在省略什么"。
```

### Task 1.2: Update references/decision-report-template.md

**Files:**
- Modify: `references/decision-report-template.md`

- [ ] **Step 1: Enhance Decision Scope block to emphasize input boundary**

In the `### Decision architecture` section (around line 128), enhance the "关键未知" field description to include input-boundary linkage:

```
    - **关键未知**：[选择时尚未确认、可能影响结果的信息] 若未指定项改变结论，应在此标注并进入 sensitivity 分析。
```

Add a new field:
```
    - **输入边界 / 未指定项**：[可选，参考 `references/report-template.md` §输入边界与未指定项]
```

- [ ] **Step 2: Add `实施路线` integration to option-selection structure**

In the market-outlook section (around line 142), add after or within the existing structure:

```
**实施路线（当有落地决策负担时建议包含）：**

当推荐涉及实施、部署或组织变更时，在推荐路径之后补充实施路线：

| 阶段 | 要做什么 | 不做什么 | 关键里程碑 | Owner / 运营模型 |
|-----|---------|---------|-----------|-----------------|
| 准备/MVP | ... | ... | ... | ... |
| 扩展 | ... | ... | ... | ... |
| 强化 | ... | ... | ... | ... |
| 稳态 | ... | ... | ... | ... |

规则：
- 区分 MVP 形态与长期终局，不把终局架构当第一阶段建议。
- 每个阶段必须说明"什么情况下加速下一阶段、什么情况下暂停"。
- 对组织类报告，明确 Owner / 运营模型的归属变化。
```

### Task 1.3: Update references/market-outlook-and-scenario-discipline.md

**Files:**
- Modify: `references/market-outlook-and-scenario-discipline.md`

- [ ] **Step 1: Add Value-chain sensitivity map subsection**

Add after the `Drivers vs blockers discipline` section (around line 192):

```markdown
### Value-chain sensitivity map（产业链主题建议）

当题目包含「产业链」「value chain」「supply chain」「infrastructure chain」时，建议在 drivers/blockers 分析之后包含一张价值链敏感性地图。

**格式模板**

| 链条层级 | 当前暴露程度 | 瓶颈传导机制 | 受益方/受损方 | 影响时间 | 证据强度 | 改变结论的条件 |
|---------|------------|------------|-------------|---------|---------|-------------|
| 上游：... | observed / estimated | 机制说明 | ... | 短期/中期/长期 | high / medium / low | ... |
| 中游：... | ... | ... | ... | ... | ... | ... |
| 下游：... | ... | ... | ... | ... | ... | ... |

**规则：**
- 链条层级一般分为上游（原材料/基础供应）、中游（制造/建设/运营）、下游（应用/消费/服务），可根据题目调整。
- 每个层级至少包含 exposure、bottleneck mechanism、beneficiaries/losers、timing、evidence strength、change-condition。
- 不同层级之间的传导关系应在文字说明中体现，而非仅靠表格。
```

- [ ] **Step 2: Add Regional coverage matrix subsection**

Add after the value-chain sensitivity map:

```markdown
### Regional coverage matrix（global scope 主题建议）

当报告标题或问题包含「全球」「global」「区域」「region」时，建议包含一张区域覆盖矩阵。这有助于读者理解"全球"是否真的是全球覆盖，还是主要聚焦部分区域。

**格式模板**

| 区域 | 覆盖的关键指标 | 数据角色 | 来源 `[Sxx]` | 是否覆盖 |
|-----|-------------|---------|-------------|---------|
| 北美 | ... | observed / estimate / forecast / scenario / proxy | [S01], [S02] | ✅ |
| 欧盟 | ... | ... | ... | ✅ |
| 中国 | ... | ... | ... | ✅ |
| 印度 | ... | ... | ... | ❌ 未覆盖 |
| 东南亚 | ... | ... | ... | ❌ 未覆盖 |
| 中东/非洲 | ... | ... | ... | ❌ 未覆盖 |

**规则：**
- 数据角色列必须标注角色的认识论分类（observed / estimate / forecast / scenario / proxy）。
- 区域关键数字必须有 `[Sxx]` 正文引用，不能仅靠文末 bibliography。
- 若只覆盖欧美和中国却声称"全球"，必须触发 scope completeness warning：

  > ⚠️ 本报告声称覆盖全球市场，但实际可验证数据仅覆盖 [北美+欧盟+中国] 三个区域，占全球市场约 [X]%。建议在题目或范围声明中明确限定覆盖区域。

- 区域选择不是固定的——应根据题目涉及的产业链和市场规模合理选择对比区域（例如数据中心电力主题至少覆盖北美、欧盟、中国、东南亚、中东）。

**不触发条件**：报告 scope 已明确声明聚焦特定区域（如"中国市场"、"全球视角偏重欧美"）且标题/问题不含"全球"等全貌措辞。
```

- [ ] **Step 3: Upgrade Stakeholder implications section to action table**

Replace the current stakeholder section (from `### Stakeholder implications discipline` line 217) with upgraded version. Keep the existing introductory text but add the action table template as the recommended format:

```markdown
## Stakeholder implications discipline

Do not stop at "the market will likely do X."

State who that matters for.

Cover **at least 3 distinct stakeholder types**. Investor-only coverage is not sufficient.

Common stakeholder lenses:
[...keep existing list...]

For each covered stakeholder type, provide a dedicated subsection that answers:
[...keep existing questions...]

### 推荐结构：Stakeholder action table

当报告涉及实施决策、成本投入、组织变更时，建议将 stakeholder 影响从"方向性描述"升级为 action table：

| Stakeholder | Decision to make | Recommended action | Required evidence / metric | Trigger to revise |
|---|---|---|---|---|
| [角色] | [需要做的决策] | [推荐行动] | [约束条件 / 关键指标] | [什么假设变化会改变推荐] |

示例：

| Stakeholder | Decision to make | Recommended action | Required evidence / metric | Trigger to revise |
|---|---|---|---|---|
| 业务 Owner | 是否全面接入 AI Agent | 先启动 MVP 试点（1 个团队，3 个月） | 客服响应时间改善 >30% 且成本不增加 >15% | 试点 3 个月后效果未达标 → 回到部分接入方案 |
| 数据/知识 Owner | 数据清洗与知识库优先级 | 优先打通 CRM+BI 系统数据管道 | 数据覆盖率 >80% 的渠道数 | 关键工单系统 API 不可用 → 调整 MVP scope |
| AI 运营 Owner | 选型：集中式 Agent vs 微代理 | 部署分布式微代理 + 人工兜底 | 单 Agent 准确率 >85%，兜底率 <10% | 运维人力需求超预期 → 增加集中管理面板 |

**规则：**
- 每个 stakeholder 的行动建议必须是具体的、可检查的，而不是"关注趋势"。
- "Trigger to revise"列必须包含具体阈值或条件。
- 该表不替代现有"what does this mean for them"描述性段落——可以在描述性段落后附加该表，或直接用表格替代描述。
```

### Task 1.4: Update checklists/market-outlook-audit.md

**Files:**
- Modify: `checklists/market-outlook-audit.md`

- [ ] **Step 1: Add value-chain sensitivity map check** (after drivers/blockers section)

```markdown
## Value-chain sensitivity coverage

- [ ] if the topic contains 产业链 / value chain / supply chain / infrastructure chain, a value-chain sensitivity map is present
- [ ] each chain layer includes exposure, bottleneck mechanism, beneficiaries/losers, timing, evidence strength, change-condition
- [ ] the map is not a flat description but shows inter-layer transmission logic
```

- [ ] **Step 2: Add regional coverage matrix check** (after quantitative role labeling section)

```markdown
## Regional coverage (global scope)

- [ ] if the report title/question contains 全球 / global / 区域 / region, a regional coverage matrix is present
- [ ] each region in the matrix has a Data role column (observed / estimate / forecast / scenario / proxy)
- [ ] each regional key metric has an `[Sxx]` inline citation
- [ ] if the report claims "global" but only covers US/China/EU, a scope completeness warning is present
```

- [ ] **Step 3: Add stakeholder action table check** (after stakeholder implications section)

```markdown
## Stakeholder actionability (enhanced)

- [ ] stakeholder implications use action table format (decision / action / metric / trigger) when implementation burden exists
- [ ] each action has a concrete, checkable recommendation (not "关注趋势")
- [ ] "Trigger to revise" column includes specific threshold or condition for at least half of entries
```

### Task 1.5: Update evals/templates/decision-utility-rubric.md (optional)

**Files:**
- Modify: `evals/templates/decision-utility-rubric.md`

- [ ] **Step 1: Add stakeholder actionability dimension** or upgrade existing Dimension 6

In Dimension 6 (Actionability of next steps), add a check for action-table format:

```
**Enhanced checks for implementation-heavy reports:**

When the report involves implementation, deployment, or organizational change:
- is there an action table mapping stakeholder → decision → action → metric → trigger?
- are the actions concrete and checkable rather than aspirational?
- does each action have a defined revision trigger?
```

---

## Phase 2: Contract Tests

### Task 2.1: Write and run test_issue_320_contracts.py

**Files:**
- Create: `tests/test_issue_320_contracts.py`

- [ ] **Step 1: Write test file** with the following contracts:

**C1:** Two comparative distillation artifacts exist
- C1a: small-team-ai-agent-gpt-vs-local-comparative-distillation.md exists
- C1b: data-center-power-bottleneck-gpt-vs-local-comparative-distillation.md exists

**C2:** Both artifacts contain 6-dimension framework, Candidate-action summary, Final judgment
- C2a: 6 dimensions headings present
- C2b: Candidate-action summary present
- C2c: Final judgment present
- C2d: Things explicitly rejected section present

**C3:** Both artifacts document GPT citation limitations as rejected
- C3a: contains turn... citation, bibliography-only, or equivalent rejection

**C4:** Template updates exist
- C4a: report-template.md contains "输入边界" or "未指定项"
- C4b: decision-report-template.md contains "实施路线" or implementation stages structure
- C4c: market-outlook-and-scenario-discipline.md contains "Value-chain sensitivity map"
- C4d: market-outlook-and-scenario-discipline.md contains "Regional coverage matrix"
- C4e: market-outlook-and-scenario-discipline.md contains "Stakeholder action table" or action table template

**C5:** Checklist updates exist
- C5a: market-outlook-audit.md contains "value-chain sensitivity" check
- C5b: market-outlook-audit.md contains "regional coverage" check
- C5c: market-outlook-audit.md contains "action table" or actionability check

**C6:** candidate-rule-registry.md references both new distillation cases
- C6a: registry mentions "small-team-ai-agent"
- C6b: registry mentions "data-center-power"

**C7:** Cross-file invariants
- C7a: Both artifacts have Action type labels (NEW_RULE / CHECKLIST_HARDENING / TEMPLATE_CHANGE / NO_ACTION)
- C7b: Each dimension has per-dimension Action type (>=3 action types per artifact)

- [ ] **Step 2: Run tests to confirm RED**

Run: `python tests/test_issue_320_contracts.py`
Expected: ALL FAIL (artifacts and template changes don't exist yet)

- [ ] **Step 3: Commit RED tests**

```bash
git add tests/test_issue_320_contracts.py
git commit -m "test: add contract tests for issue #320 (RED)"
```

### Task 2.2: Implement Phase 0 artifacts

- [ ] Execute Task 0.1 (small-team AI Agent distillation)
- [ ] Execute Task 0.2 (data center power bottleneck distillation)
- [ ] Execute Task 0.3 (candidate-rule-registry update)

- [ ] **Run tests to check progress**

Run: `python tests/test_issue_320_contracts.py`
Expected: C1-C3 pass (artifacts exist), C4-C5 fail (templates not updated yet)

- [ ] Commit Phase 0

### Task 2.3: Implement Phase 1 template changes

- [ ] Execute Task 1.1 (report-template.md)
- [ ] Execute Task 1.2 (decision-report-template.md)
- [ ] Execute Task 1.3 (market-outlook-and-scenario-discipline.md)
- [ ] Execute Task 1.4 (market-outlook-audit.md)
- [ ] Execute Task 1.5 (decision-utility-rubric.md optional)

- [ ] **Run tests to confirm GREEN**

Run: `python tests/test_issue_320_contracts.py`
Expected: ALL PASS

- [ ] Commit Phase 1

### Task 2.4: Run full test suite

- [ ] Run: `python tests/test_issue_320_contracts.py`
- [ ] Run all existing contract tests:
```bash
for f in tests/*.py; do echo "=== $f ===" && python "$f"; done
```
- [ ] Verify no regressions

---

## Reflexion: Self-Review

### Task 3.1: Quality checks

- [ ] **Template consistency check:** Do the new additions in report-template.md, decision-report-template.md, and market-outlook-and-scenario-discipline.md reference each other correctly?
- [ ] **No false-hard-fail:** Are the new checklist items in market-outlook-audit.md appropriately gated (not automated hard-fails without clear trigger)?
- [ ] **No 自夸/自我引用:** Do the artifacts avoid referencing marketing language about the skill's quality?
- [ ] **Scope boundary:** Are all changes limited to the issue #320 scope? No unrelated refactoring?
- [ ] **Existing links preserved:** Check that pre-existing cross-references in modified files are still intact

### Task 3.2: Final pass

- [ ] Re-read all modified files for markdown correctness
- [ ] Check for any `turn...` pattern leakage in new artifacts
- [ ] Verify each acceptance criterion from issue #320 is met:
  - [ ] AC1: Input boundary / 未指定项 小节 → report-template.md
  - [ ] AC2: Value-chain sensitivity map → market-outlook-and-scenario-discipline.md
  - [ ] AC3: Regional coverage matrix with source role → market-outlook-and-scenario-discipline.md
  - [ ] AC4: Stakeholder action table (decision/action/metric/trigger) → market-outlook-and-scenario-discipline.md + checklist
  - [ ] AC5: Documentation of GPT-learnable vs not-learnable → both distillation artifacts
  - [ ] AC6: At least one eval/comparative-distillation artifact → 2 artifacts created

---

## PR and Cross-Review

### Task 4.1: Create PR

- [ ] `git add . && git commit -m "feat: implement issue #320 — absorb GPT structural strengths into templates, checklists, and evals"`
- [ ] `gh pr create`

### Task 4.2: Launch two independent subagent cross-reviews

- [ ] Subagent A: Review all template changes for internal consistency, completeness, and scope boundaries
- [ ] Subagent B: Review distillation artifacts and checklist changes for methodological rigor
- [ ] Address findings
- [ ] Loop until 100% confidence
