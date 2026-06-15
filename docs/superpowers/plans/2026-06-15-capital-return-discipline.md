# CapEx-heavy 上市公司资本回收纪律 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add capital return discipline for CapEx-heavy listed companies in the deep-research skill, ensuring reports don't conclude "undervalued" based on PE/PEG/growth alone without checking FCF conversion, CapEx burden, and ROIC.

**Architecture:** Four file modifications to existing documentation: (1) new section in `references/valuation-methodology.md` defining trigger conditions and required analysis, (2) new checklist items in `checklists/listed-company-report.md`, (3) new table template in `references/report-template.md` for growth-to-cash-flow conversion, (4) new recall discipline item in `checklists/final-audit.md`. All changes are additive — no existing content is modified or removed.

**Tech Stack:** Pure Markdown documentation, no code changes. Validation via existing markdown linters and cross-reference checks.

---

### Task 1: Add capital return discipline section to valuation-methodology.md

**Files:**
- Modify: `references/valuation-methodology.md` — append new section before `## Relationship to other discipline files`

- [ ] **Step 1: Read the exact insertion point**

Read `references/valuation-methodology.md` lines 230-239 to confirm the insertion point before `## Relationship to other discipline files`.

- [ ] **Step 2: Insert new section**

Insert a new section `## Capital return discipline for CapEx-heavy companies (重资产公司的资本回收纪律)` at the end of the Common failure patterns section (after line 233), before `## Relationship to other discipline files`.

Content to insert:

```markdown
## Capital return discipline for CapEx-heavy companies (重资产公司的资本回收纪律)

当分析资本密集型上市公司的估值时，仅使用收入增长和 PE/PEG 框架可能掩盖最关键的财务问题：增长是否以足够高的回报率沉淀为自由现金流和股东价值。

### 触发条件

以下**任一**条件满足时，必须启动本纪律：

- **行业属性**：公司属于半导体制造、工业制造、能源、电力、数据中心、通信基础设施等资本密集型业务。
- **CapEx 强度**：CapEx / 收入长期高于 20%，或显著影响自由现金流。
- **Thesis 依赖**：报告核心 thesis 依赖产能扩张、新节点爬坡、海外建厂、重资产投入。
- **增长模式**：收入增长主要来自增加产能/固定资产而非价格/产品 mix 改善。

### 必须回答的六个问题

当本纪律触发时，报告必须在估值章节（或紧邻的四变量分解段）中回答以下问题，而非仅将 CapEx 风险列在风险段落：

1. **增长来源**：收入增长来自价格、出货量、产品 mix，还是一次性周期因素？区分可持续增长与周期波动。
2. **再投资负担**：实现增长需要多少 CapEx / working capital / D&A？CapEx / 收入比率是否高于同行业可比公司，如果是，原因是什么？
3. **利润率稀释**：新产能、新地区、新节点或学习曲线是否短期压低 margin？具体影响幅度和时间范围是什么？
4. **FCF 转换**：净利润增长是否确实转化为自由现金流增长？D&A 和 CapEx 的差额（即 reinvestment gap）对 FCF 的实际影响是什么？
5. **ROIC 与回收周期**：增量资本回报率（ROIC）是否高于 WACC？回收周期是否在投资人可接受范围内？增长是否在扩大收入规模但并未提高股东回报？
6. **估值影响**：如果 CapEx 强度持续高于假设，或 FCF 转换低于预期，估值结论如何变化？PE/PEG 框架能否单独支撑结论，还是需要 DCF 或 ROIC 分析？

### 常见失败模式

- **增长故事代替资本回报分析**：报告强调 TAM 和收入增长，但未检查增长的资本成本。读者无法判断增长是否创造价值。
- **风险清单代替估值输入**：CapEx 和 FCF 风险列在风险章节，但估值结论（目标价、PE 倍数判断）沿用 PE/PEG 框架，未纳入这些风险。
- **轻资产模板套用到重资产公司**：用标准的"收入增长 + PE 倍数收缩/扩张"模板分析半导体制造或数据中心公司，忽略了 FCF 转换的关键问题。
- **忽视 margin 稀释的阶段差异**：新节点/新产区初期爬坡的 margin 稀释是暂时性的，但如果不量化阶段和回收期，容易将过渡期问题误判为结构性缺陷，或反过来忽视其量化影响。

### 与现有规则的关系

- 本纪律的四变量关联：六个问题中的问题 1-3 对应四变量分解的变量 3（利润率与现金流转换），问题 5-6 对应变量 4（估值透支程度）。本纪律为四变量分解中 CapEx-heavy 场景提供更详细的执行指导。
- 本纪律与 `references/report-template.md` §增长到现金流转换表 配合使用：该表提供定量框架，本纪律提供分析问题集。
- 本纪律不替代 DCF 触发条件：如果满足 DCF 触发条件（见 §DCF / reverse DCF trigger），DCF 仍然必须执行。本纪律在 DCF 不适用时提供最低限度的资本回收分析框架。
```

- [ ] **Step 3: Verify the insertion**

Run: `grep -n "Capital return discipline" references/valuation-methodology.md`
Expected: Shows the new section heading with line number, appearing before "Relationship to other discipline files".

- [ ] **Step 4: Commit**

```bash
git add references/valuation-methodology.md
git commit -m "feat(valuation): add capital return discipline for CapEx-heavy companies

Add new section to valuation-methodology.md defining trigger conditions,
six required analysis questions, and common failure patterns for
capital-intensive listed-company analysis.

Toward #279"
```

---

### Task 2: Add growth-to-cash-flow conversion table to report-template.md

**Files:**
- Modify: `references/report-template.md` — insert after the Four-variable decomposition section (after line 83), before the next section starting "Do not default to using the front page"

- [ ] **Step 1: Read the exact insertion point**

Read `references/report-template.md` lines 72-87 to confirm insertion point after the four-variable decomposition block and its existing note.

- [ ] **Step 2: Insert growth-to-cash-flow conversion block after the four-variable decomposition note**

Content to insert after "growth→value conversion chain." paragraph (after line 83):

```markdown
### 增长到现金流转换表（CapEx-heavy 公司强制）

当本报告涉及 CapEx-heavy 公司（见 `references/valuation-methodology.md` §Capital return discipline for CapEx-heavy companies 触发条件）时，估值部分必须包含以下转换表。该表将 CapEx、D&A、FCF、ROIC 等变量从风险清单升格为估值模型输入。

| 变量 | 当前状态 | 基准假设 | 压力情景 | 对估值影响 | 数字角色 |
|---|---|---|---|---|---|
| CapEx / 收入 | | | | | observed / assumption |
| D&A / 收入 | | | | | assumption |
| FCF margin | | | | | model output |
| ROIC / 回收期 | | | | | model output |
| 新产能/新地区 margin 稀释 | | | | | estimate / assumption |

**填写规则**：
- 「当前状态」列填写最近报告期的实际可观测数据（如 FY2025 CapEx/收入 = 35%）。
- 「基准假设」列填写报告采用的分析假设（如未来 3 年 CapEx/收入逐步降至 28%）。
- 「压力情景」列填写当关键假设不成立时的替代值（如 ASML 设备交付延迟，CapEx/收入维持 35%+）。
- 「对估值影响」列简述该变量偏离对 PE 倍数调整、目标价变动或结论方向的量化/方向性影响。
- 「数字角色」列标识每个数值的认识论角色（观察值 / 假设 / 模型输出 / 估算），见 `references/quantitative-role-labeling.md`。

> 本表不替代 DCF（当 DCF 触发条件满足时 DCF 仍必须执行），而是在 DCF 不适用或作为 DCF 假设的补充可见框架时，确保 CapEx-heavy 公司的资本回收变量不被忽略。

This table requirement was added via issue #279 to ensure CapEx-heavy company reports do not skip the growth-to-cash-flow conversion analysis.
```

- [ ] **Step 3: Verify the insertion and section continuity**

Read the surrounding lines to ensure the insertion points and section structure are clean.

- [ ] **Step 4: Commit**

```bash
git add references/report-template.md
git commit -m "feat(template): add growth-to-cash-flow conversion table for CapEx-heavy companies

Insert mandatory table template after the four-variable decomposition
section, ensuring CapEx/Revenue, D&A/Revenue, FCF margin, ROIC, and
margin dilution are treated as valuation inputs rather than risk-list items.

Toward #279"
```

---

### Task 3: Add checklist items to listed-company-report.md

**Files:**
- Modify: `checklists/listed-company-report.md` — add items to the `## Valuation methodology` section after line 36 (after the existing (非阻塞) scenario analysis item)

- [ ] **Step 1: Read the exact insertion point**

Read `checklists/listed-company-report.md` lines 27-45 to confirm the insertion point within the Valuation methodology section, after the scenario analysis items and before `### DCF / 反向 DCF`.

- [ ] **Step 2: Add capital return checklist items after scenario analysis, before DCF subsection**

Content to insert (before `### DCF / 反向 DCF（当适用）`):

```markdown
### Capital return discipline (CapEx-heavy 公司适用)

适用触发条件：公司属于半导体制造、工业制造、能源、电力、数据中心、通信基础设施等资本密集型业务，或 CapEx / 收入长期高于 20%，或核心 thesis 依赖产能扩张/新节点爬坡/海外建厂/重资产投入（完整定义见 `references/valuation-methodology.md` §Capital return discipline for CapEx-heavy companies → 触发条件）。

- [ ] （阻断级）当本纪律触发时，报告不得仅凭收入增长和 PE/PEG 得出估值结论；必须检查 FCF conversion / CapEx burden / D&A / ROIC，并在估值章节而非仅风险章节处理这些变量
- [ ] （非阻塞）如果增长依赖新产能、新地区、新节点或重资产扩张，报告说明了初期 margin 稀释的时间范围与回收周期，而不是只提示"存在稀释风险"
- [ ] （非阻塞）FCF / CapEx / D&A 数字的角色和时间口径在转换表或正文中可见（观察值 vs 假设 vs 模型输出）
- [ ] （非阻塞）若 CapEx 强度、FCF 转换或 ROIC 等资本回收关键变量存在实质性不确定性（±20% 偏差可改变估值结论），最终结论降级为方向性或条件性判断，而非精确目标价
```

- [ ] **Step 3: Verify the insertion**

Run: `grep -n "Capital return discipline" checklists/listed-company-report.md`
Expected: Shows the new section heading.

- [ ] **Step 4: Commit**

```bash
git add checklists/listed-company-report.md
git commit -m "feat(checklist): add capital return discipline checklist for CapEx-heavy companies

Add new subsection under Valuation methodology with 1 blocking and 3
non-blocking checks: blocking check prevents PE/PEG-only valuation
conclusions for CapEx-heavy companies; non-blocking checks cover margin
dilution timeline, number role visibility, and conclusion downgrade rules.

Toward #279"
```

---

### Task 4: Add recall discipline item to final-audit.md

**Files:**
- Modify: `checklists/final-audit.md` — add item to the `## Recall discipline` section

- [ ] **Step 1: Read the exact insertion point**

Read `checklists/final-audit.md` lines 137-168 to find the appropriate location within the Recall discipline section, between existing listed-company items.

- [ ] **Step 2: Add recall item for capital-heavy company growth→FCF check**

Insert after line 139 (after "listing status and financial snapshot were verified for listed companies"), before the scope completeness item:

```markdown
- [ ] for CapEx-heavy listed company reports (trigger conditions defined in `references/valuation-methodology.md` §Capital return discipline for CapEx-heavy companies), the valuation conclusion does not rest on revenue growth and PE/PEG alone without explicitly checking FCF conversion, CapEx burden, D&A, and ROIC; the capital return variables are treated as valuation inputs rather than only risk-list items (see `checklists/listed-company-report.md` §Capital return discipline)
```

- [ ] **Step 3: Verify the insertion**

Run: `grep -n "CapEx-heavy listed company reports" checklists/final-audit.md`
Expected: Shows the new line.

- [ ] **Step 4: Commit**

```bash
git add checklists/final-audit.md
git commit -m "feat(audit): add capital-return recall discipline to final-audit

Add recall check for CapEx-heavy company reports: valuation conclusion
must check FCF/CapEx/D&A/ROIC, not just revenue growth and PE/PEG.

Toward #279"
```

---

### Task 5: Run validation and cross-reference integrity check

- [ ] **Step 1: Verify all cross-references are correct**

Run cross-reference checks:
```bash
# Check that each file's references to other files are correct
grep -n "valuation-methodology.md" checklists/listed-company-report.md | head -5
grep -n "valuation-methodology.md" checklists/final-audit.md | head -5
grep -n "report-template.md" references/valuation-methodology.md | head -5
grep -n "listed-company-report.md" checklists/final-audit.md | head -5
```

- [ ] **Step 2: Verify markdown structure**

Verify files are valid markdown (no broken syntax):
```bash
python3 -c "
import os, re
files = ['references/valuation-methodology.md', 'references/report-template.md',
         'checklists/listed-company-report.md', 'checklists/final-audit.md']
for f in files:
    content = open(f).read()
    # Check no unclosed code blocks
    if content.count('\`\`\`') % 2 != 0:
        print(f'WARN: {f} has unclosed code blocks')
    # Check checklist syntax: [ ] should be - [ ] or - [x]
    lines = content.split('\n')
    for i, line in enumerate(lines, 1):
        if re.search(r'(?<!- )\[ \]', line):
            print(f'WARN: {f}:{i} unformatted empty checkbox: {line.strip()}')
    print(f'OK: {f} ({len(lines)} lines)')
"
```

- [ ] **Step 3: Verify git state**

```bash
git status --short
git log --oneline -5
```

- [ ] **Step 4: Commit any remaining touch-ups**

```bash
git add -A
git commit -m "fixup: cross-reference consistency and markdown integrity

Toward #279"
```
