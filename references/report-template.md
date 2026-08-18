# Report Template

Use this as the default structure for most deep-research outputs.

Do not force every section if the task does not need it, but keep the report decision-oriented and evidence-aware.

For the reader-facing format of a Markdown-first delivery, also read
`references/markdown-delivery-contract.md`. This template defines what the
report must contain; the Markdown contract defines how that content should be
ordered and presented for scan reading.

## Front-page discipline

The front page should help the reader grasp the report's main judgment quickly.

For user-facing reports, the front page should usually prioritize:
- title
- report date / coverage period
- one-sentence bottom line or thesis
- 3-5 executive bullets
- **research-anchor block** (for listed-company / investment-style work — see `references/templates/listed-company-report.md`)
- key risks
- key unknowns


## Route-aware template selection

`report-template.md` is the **core (default) report template**. Route-specific
structure lives in `references/templates/` and is read **only when the
selected route requires it** (per the route's card in `references/routes/`):

- **listed-company / investment-style**: `references/templates/listed-company-report.md` — research-anchor block, market snapshot table, customer-concentration risk table, valuation method / DCF / sensitivity-matrix sections.
- **technical-deep-dive**: `references/templates/technical-deep-dive-report.md` — route-aware opening, terminology-boundary table.
- **academic-review**: `references/templates/academic-review-report.md` — researcher / practitioner next-steps recommendations (field-progress style).
- **market-outlook**: `references/templates/market-outlook-report.md` — market-outlook memo discipline, category-boundary / demand-segmentation / commercialization templates.
- **market-entry / go-no-go**: `references/templates/market-entry-report.md` — go-no-go memo formatting discipline. The shared input-boundary table remains in this core template because it also applies to constrained-choice, provider-selection, and market-outlook tasks.

Use `references/decision-report-template.md` when the task needs recommendation,
go/no-go view, prioritization, comparison, or action guidance (it supplements
the core sections below).

## Shared decision-scope add-on

For constrained-choice, provider-selection, market-entry, and market-outlook tasks that involve organizational rollout or solution selection, make the decision scope explicit with an input-boundary table. It distinguishes known inputs, assumptions, and unspecified inputs before the recommendation is generalized beyond the evidence.

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


## Scanability and paragraph discipline

Final reports should support scan reading, not only sequential reading.

Prefer:
- shorter paragraphs
- one main judgment per paragraph
- bullets for risks, unknowns, limits, and counter-evidence
- visible subheadings or callouts for key takeaways

Avoid long stretches of dense prose when a list, takeaway block, or short sub-section would improve readability.

## Table discipline

Use tables when they help the reader compare, prioritize, or interpret evidence.
Tables should not appear as unsupported data dumps.

By default, a useful table should include:
- a clear title
- visible units and time scope
- consistent number formatting
- a short interpretation below the table explaining what the table shows and why it matters

### Number role column in comparison / scoring / estimation tables

When a table carries numbers that affect ranking, recommendation, timing, or confidence — especially in comparison tables, scoring tables, or estimation tables — include a **数字角色 (number role) column** as the last or second-to-last column. This makes the epistemic status of each number visible to the reader without requiring them to cross-reference back to the body text.

Use the last column for the role label by default. Reserve the second-to-last position when the table also has a confidence or source-reference column that should appear after the role column (e.g., [数字角色 → 置信度] or [数字角色 → 来源]).

The role column identifies each number as one of: observed metric, proxy, assumption, model output, or illustrative calculation (see `references/quantitative-role-labeling.md` §Core roles for definitions).

Example template:

```
| 维度 | 国家A | 国家B | 国家C | 数字角色 |
|------|-------|-------|-------|---------|
| 成本 | $100M | $80M | $60M | 代理指标（基于行业报告推算） |
| 市场增速 | 40% | 30% | 20% | 模型输出（基于假设增长率） |
| 补贴比例 | 15%  | 10%  | 5%   | 假设（政策方向已知，具体比例未定） |
| 潜在市场规模 | 500亿 | 300亿 | 200亿 | 说明性计算（基于Top-Down市场拆分） |
```

If a per-row role column makes the table too wide or repetitive, acceptable alternatives include:

- a role **header row** (a row between the column headers and the data that labels each column's epistemic role)
- a **table-level note** stating the role of all numbers in the table (e.g., "本表所有数字均为模型输出，基于公开财务数据的推算，不应视为已确认事实")

What is **not** acceptable:

- A statement in the surrounding prose that "all numbers in this report are estimates" while the table itself carries no role indicator
- A single inline disclaimer in the introduction applied to every table without per-table annotation
- Mixing observed facts and model outputs in the same table without distinguishing them

For the full description of each pattern with examples, see `references/quantitative-role-labeling.md` §表格中的角色标签. The role must be visible at the table level — either per row, per column in a header role row, or in an explicit table note.

## Default structure

### 1. Executive summary

**Format: use bullet points, not paragraphs.** Each bullet should contain one distinct idea. Do NOT write the executive summary as a wall of running text.

- answer the real question first
- give the bottom line in 4–8 short bullet points
- each bullet: one insight, one label (Confirmed / Inference / Uncertainty)
- separate what is confirmed, inferred, and uncertain when relevant
- put the most important conclusion first; less important details later
- when presenting paired signals (e.g., volume growth + margin pressure), use one bullet to pair them — do not separate into different sections

**Good bullet:**
- `[CONF]` 2025年营收638.9亿美元，净利润231.3亿美元（同日历年）

**Bad bullet (wall of text, no label):**
- 博通是全球最大的半导体和基础设施软件公司之一，2025财年营收达638.9亿美元，净利润231.3亿美元，在AI浪潮中跻身"科技七巨头"（Magnificent Seven），公司业务横跨半导体芯片设计与软件基础设施两大板块。

**When writing bullets, ask:** Can a reader extract the key facts without reading every sentence?

### 2. What matters most

- identify the 2-5 variables that most affect the conclusion
- explain why they matter more than the rest

### 3. Key findings

- present the main findings in descending order of importance
- avoid trivia and background overload

### 4. Detailed analysis

Organize by task type. Examples:

- company: products, financials, competition, risks, strategy
- market: size, growth, structure, competition, bottlenecks
- technical: feasibility, constraints, trade-offs, implementation needs. For security-sensitive tasks, consider the threat modeling structure in `references/technical-analysis-discipline.md` §Security deep-dive: threat modeling add-on (assets, trust boundaries, threat actors, risk prioritization, engineering controls, detection signals, short/medium/long-term roadmap).
- policy: rules, scope, timing, compliance impact, edge cases

### 5. Risks and counter-evidence

- include the strongest reasons the main conclusion could be wrong
- include limits, contradictions, or competing explanations

#### Bull/bear structural symmetry

When the report includes both bull (看多) and bear (看空) case sections, they must use the same structural format. Do not give one side a rigorous epistemic breakdown while the other side is loose prose.

Recommended three-column structure for both sides:

| 事实依据 | 推断依据 | 不确定性/限制条件 |
|----------|----------|-------------------|
| 支持该判断的确认事实 | 推断或假设 | 什么会推翻该判断 |

Rules:
- both bull and bear sections use the same column breakdown
- both sides apply the same evidence-label discipline ([CONF] / [INFER] / [UNKN])
- if one side has a table, the other side should have a comparable table
- do not let the bear case become a bullet list of generic risks while the bull case is a structured analysis
- if one side has significantly less evidence than the other, still use the same structure but mark empty cells as "无相关证据" or "暂无数据" rather than omitting the structure
- asymmetric evidence strength is acceptable; asymmetric structure is not

This symmetry matters because asymmetric structure signals to the reader that one side was analyzed more rigorously than the other, even if the substance is equally strong.

### 6. Uncertainty and missing evidence

- if confidence depends on assumptions or modeled numbers, make that dependency visible instead of letting the numbers read like confirmed facts
- say what could not be verified
- say what would most improve confidence

### 7. Bottom line

- give the practical conclusion
- include what to do next when useful
- include what could change the conclusion

### 8. Route and audit status (mandatory)

在来源注册表之前，**必须包含**一个标准化的路由与审计状态区块，让评审者无需查看 process log 即可确认哪些审计已运行。

该区块内的自评状态（✅ Passed / ⚠️ Skipped / ❌ Not run）必须与报告正文的实际检查结果一致。不一致的区块（如声称 "source-traceability ✅ Passed" 但正文缺少 `[SN]` 引用或 Source Register 条目不完整）将被 final-audit 门控拦截。

**格式模板（路由已选择时）：**

```
## Route and audit status

**Primary route**: Provider / Vendor Selection
**Secondary route**: Regulatory / Policy Impact Analysis

| Audit | Status | 证据 |
|-------|--------|------|
| route-activation-audit | ✅ Passed | report-section:Route selection visibility |
| option-selection-final-audit | ✅ Passed | report-section:Comparison |
| source-traceability | ✅ Passed | report-section:Sources |
| final-audit | ✅ Passed | report-section:Bottom line |
| regulatory secondary hard-fail | ✅ Passed | report-section:Regulatory impact |
```

**格式模板（shared-workflow 路径）：**

```
## Route and audit status

**Route**: Shared-workflow (no specialized route selected)

| Audit | Status | 证据 |
|-------|--------|------|
| workflow-spine-audit | ✅ Passed | report-section:Findings |
| final-audit | ✅ Passed | report-section:Bottom line |
```

**规则：**

- 列出该次任务运行或应运行的所有审计，包括：
  - route-specific audits（来自 `ROUTING-MATRIX.md` 各路由的 `### Audit` 节）
  - `route-activation-audit` 的运行状态
  - 如果声明了次级路由（secondary route），次级路由的 hard-fail 验证状态
- 每个 audit 一行，状态三选一：
  - **已通过** — 审计已运行且通过
  - **已跳过（附理由）** — 审计适用但决定跳过，理由需明确
  - **未运行（附理由）** — 审计因故未运行，理由需明确
- 该区块不追求详尽审计记录，只追求评审者可见——证明审计已运行
- **一致性要求**：区块中每个声称已通过的审计（✅ Passed 或等效表达/emoji）必须在正文或交付物结构中有对应的执行证据（如 source-traceability ✅ 需要正文存在 `[SN]` 引用，workflow-spine-audit ✅ 需要交付物有清晰的工作流结构）；无对应执行证据的 ✅ Passed 视为自评不准确，由 final-audit 门控标记为未通过
- **证据列要求**：每项审计的「证据」列必须填写具体的正文引用，不得为空或仅写"是"、"通过"等无明确引用内容：
  - ✅ **已通过 (Passed)** — 使用 typed reference：`report-section:<heading>`、`report-table:<heading>`、`checklist-item:<path>#<id>` 或 `audit-record:<path>#<id>@<ISO-8601>`
    Checklist item IDs are declared by stable markers such as `<!-- audit-item: FA-001 -->` in the referenced checklist.
  - ⚠️ **已跳过 (Skipped)** — 引用正文中说明跳过理由的章节位置，或说明"§X 已在正文覆盖，未独立运行"
  - ❌ **未运行 (Not run)** — 引用正文中说明未运行原因的章节位置
  「证据」列与 Status 列的自评状态共同构成可审计记录——评审者无需全文扫描即可定位每项审计的执行证据或决定理由。裸 `§3`、`§999` 和任意自由文本不属于可验证 evidence。
- 如果路由未选择（shared-workflow 路径），列出 `workflow-spine-audit.md` 和 `final-audit.md` 的运行状态
- **审计状态应由 validator 输出驱动**：技术类报告交付前，应使用 `scripts/audit_report.py`（route-aware 审计编排器）对报告运行一次 consolidated audit。该工具的 verdict 输出应作为最终 Route and Audit Status 区块的客观依据。如果未运行 audit wrapper，不得将任意状态默认为 ✅ Passed；必须标注为 ⚠️ Manual 或 ❌ Not Run，并附理由。

  JSON 中的 `execution_source` 必须区分 `automated_validator`、`manual_checklist_attestation`、`process_node_evidence` 和兼容模式的 `legacy_self_attested`。

#### 类型化实体说明

Status block 中涉及四类实体，使用统一的 canonical id：

| 实体类型 | Canonical ID 来源 | Status Block 中表现 | 示例 |
|---------|-------------------|-------------------|------|
| **Primary Route** | `schemas/route-manifest.json` | `**Primary route**: ...` | `provider-selection` |
| **Secondary Route** | `schemas/route-manifest.json` | `**Secondary route**: ...` + hard-fail 验证行 | `regulatory-analysis` |
| **Discipline** (跨路由方法) | `schemas/discipline-registry.json` | 不直接显示在 status block；通过 audit 间接体现 | `current-state`, `source-traceability` |
| **Audit** (验证动作) | `checklists/*.md` (文件 stem) | 表格行：`\| audit-name \| status \| 证据 \|` | `final-audit` |

**关键区分：**
- Secondary Route ≠ Discipline。Secondary Route 是完整路由（有独立 hard-fail），Discipline 是跨路由复用的方法/规则。
- 不要把 `current-state`、`source-traceability` 等 discipline 误计为 secondary route。
- 如果报告中嵌入了 ` ```contract` fenced block（JSON 格式），可以在交付前用 `scripts/validate_contract.py` 验证实体之间的一致性。

#### Contract block（可选，推荐）

对于需要程序化验证实体分离的场景，报告可在 Route and audit status block 附近嵌入 contract。稳定 ID 字段 `artifact_id`、`contract_version`、`created_at` 用于与 Research Pack 互相关联（issue #376）：报告/contract 与 pack 必须对 primary route 和 artifact 归属保持一致。

   ```contract
    {
      "artifact_id": "research-2026-08-13-001",
      "contract_version": "1",
      "created_at": "2026-08-13",
      "primary_route": "provider-selection",
      "closest_alternative": "market-outlook",
      "boundary_judgment": {
        "checked_conditions": ["treats market direction as the primary question"],
        "why_not_alternative": "Task selects among providers/plans, not market direction",
        "switch_conditions": "If the question shifts to market/category trajectory"
      },
      "secondary_routes": ["regulatory-analysis"],
      "disciplines": ["current-state", "source-traceability", "forward-looking"],
      "audits": [
        {"id": "option-selection-final-audit", "status": "passed", "evidence": "report-section:Comparison"},
        {"id": "source-traceability", "status": "passed", "evidence": "report-section:Sources"},
        {"id": "regulatory-analysis-secondary-hard-fail", "status": "passed", "evidence": "report-section:Regulatory impact"},
        {"id": "final-audit", "status": "passed", "evidence": "report-section:Bottom line"}
      ]
    }
   ```

验证命令：`python3 scripts/validate_contract.py report.md --require-contract`

跨工件校验（可选）：`python3 scripts/validate_contract.py report.md --require-contract --research-pack path/to/research-pack.md`，pack 的 `## Primary route` 与 contract 的 `primary_route` 不一致会失败。

（建议在 CI 和交付前验证中始终使用 `--require-contract`。不带该 flag 时，缺失 contract 的报告会静默跳过以兼容旧报告。）

### 9. Sources

- list the most important sources
- **must** include a structured Source Register appendix using the 7-column template defined in `references/source-traceability-and-claim-citation.md` (§Structured Source Register Template) — a loose bibliography does not satisfy traceability
- a bibliography appendix without body-level `[SN]` inline citations does not satisfy source traceability — see `references/source-traceability-and-claim-citation.md`

#### Inline citation format

Use a three-layer system for every load-bearing claim:

1. **Confidence label** in the body: `[CONF]` / `[INFER]` / `[UNKN]`
2. **Inline source citation** in the body: `[SN]` at the end of the relevant clause
3. **Source register entry** in the appendix: `[SN] source title, date, type`

Body text example:
```
三星已量产HBM4 [CONF][S3]，但良率仍低于美光 [INFER][S5]。
```

Appendix example (7-column structured template):
```
| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|-----------------|
| S01 | Samsung 2025 Annual Report (KRX filing) | primary | 2026-02-15 | https://dart.fss.or.kr/... | high | §3.2, §4.1 |
| S02 | TrendForce HBM4 yield comparison note | secondary | 2026-04 | https://www.trendforce.com/... | medium | §3.2, §5.3 |
| I01 | Analyst inference based on S01 and S02 | inferred | 2026-04-15 | — | low | §4.2 |
```

See `references/source-traceability-and-claim-citation.md` for the full template definition, column rules, and Source Type classification.

For forward-looking claims, the inline citation must also include the source role:
```
据 JEDEC 行业路线图预计2027-2028发布 [S2]。
据摩根大通预计销售额年复合增长率55% [S8]。
```

Do not use bare `预计` without "据XX" attribution. See `references/forward-looking-discipline.md`.

## Final-delivery rule

Treat the final artifact as its own subsystem, not as a passive export of good reasoning.

Before delivery, check separately for:

- placeholder residue
- citation / retrieval syntax leakage
- accidental internal scaffolding visible to the reader
- broken heading hierarchy
- table overflow or unreadable density
- bullet walls or compressed paragraphs that reduce scanability
- markdown that looks acceptable but degrades badly in PDF
- leftover source placeholders such as `[SOURCE]`, `[CITATION NEEDED]`, or unresolved insert markers

A report can be analytically strong and still fail delivery. If the delivered artifact feels like a draft export, stitched note bundle, or parser byproduct, it is not ready.

## Compression rule

If the user wants a shorter answer, shorten:

- background detail
- secondary branches
- repetition

Do not shorten away:

- the real objective
- the core conclusion
- counter-evidence
- uncertainty

## Quality bar

A good report should let the reader quickly answer:

- what is the conclusion?
- why does it hold?
- what could break it?
- what remains uncertain?
- what should be done next?

## Required evidence-tier legend

Include a brief legend defining evidence confidence levels near the top of every report.

If the final report is written in Chinese, keep the legend in Chinese too. Do not mix a Chinese body with accidental English evidence buckets unless bilingual output was explicitly requested.

Placement rule:
- keep the legend compact
- do not let it displace the one-sentence thesis, executive bullets, key risks, or key unknowns from the reader's first screen / first page scan
- if space is tight, place the legend immediately after the executive summary block or at the start of the next page rather than above the thesis

Preferred Chinese format:

```
证据分级：
[确认事实] = 来自监管披露 / 年报 / 官方发布
[推断] = 来自权威机构或媒体，或基于多项证据的合理归纳
[未知] = 行业缺乏统一口径，或公开信息暂时无法验证
```

If the report also needs number-role labeling, add a second compact legend such as:

```
数字角色：
[观察值] = 公开披露或原始材料直接给出的数值
[代理指标] = 因主指标缺失而使用的替代观察量
[假设] = 用于推演的前提条件，并非已观测事实
[规划模型输出] = 基于假设或代理指标计算出的结果
```

This makes your labeling system interpretable to the reader and enforces discipline on the model side.

## Load-bearing evidence note (required for mixed-evidence positioning judgments)

When the report makes a high-level classification from mixed evidence types — especially `first-tier` / `top-tier` / competitive-positioning judgments — add a short note immediately before the final classification or bottom line.

Use a compact pattern like:

> "证据说明：关于[技术/商业化/生态/资本市场]的判断，直接证据主要来自[官方披露/产品页/监管文件]；关于[更强结论]的部分仍依赖[第三方数据/厂商自测/媒体报道/推断]，因此该结论应视为[有条件判断/推断]，不应与确认事实等同。"

This note is not filler. It forces the report to show which part of the conclusion is directly supported and which part is inference-heavy.

## Data calibration paragraph (required when using proxy indicators)

When you use proxy indicators because primary data is unavailable, add a brief note immediately below the relevant section or table:

> "注：公开定期报告对'[指标名称]'披露有限，因此以[代理指标]作为规模与供给能力的代理指标，并注明来源与口径。"

The note must state: (1) what proxy is being used, (2) why the primary data is unavailable, (3) what limitation this introduces. Without this, readers may mistake a proxy for a direct measurement.

## Conditional framing in market-position conclusions

Every market-position or ranking conclusion must include a conditional clause. Never write flat assertions like "X is the market leader" without a scope and a dependency.

- Bad: `"比亚迪是中国最大新能源汽车制造商"`
- Good: `"在中国市场（2025年零售口径），比亚迪销量领先，但全球市场份额取决于海外本地化产能落地节奏"`

Pattern: `[Position claim] + "but depends on [X]" or "this assumes [Y]"`. If no dependencies can be identified, say so explicitly.

## Competitive framing — choose the right unit of comparison

When comparing companies or assessing competitive position, do not default to unit sales or volume. First ask: *what is the correct unit for the question being answered?*

Examples:

- If comparing profitability: use margin, not revenue
- If comparing scale in a price-war context: revenue or margin, not unit volume (volume can grow while margin collapses — the "规模扩张、盈利承压" pattern)
- If comparing battery suppliers: GWh deployed, not number of vehicles

State explicitly which comparison unit you are using and why. Do not let the reader assume unit sales = competitive advantage.

## Volume + profitability signal pairing (financial sections)

When reporting volume or scale growth in a financial or competitive context, always check whether profitability and cash flow signals exist. If both growth and decline signals are present in the same period, use the "规模仍在扩张、盈利承压" structure to make the tension explicit rather than burying it in separate paragraphs.

This is a direct distillation pattern from GPT's BYD report, which consistently paired volume growth with margin and cash flow pressure in the same sentence.

## Table formatting discipline

When building tables with multi-dimensional comparisons (e.g., product category across multiple attributes):

- **Each cell contains one fact.** Do not pack multiple data points into a single cell.
- **Use `<br>` (line break) within a cell when a single attribute has multiple sub-points.** For example, a cell for "发热原理" that needs to list "燃烧烟草 (600-900°C) + 雾化器 + 口腔黏膜" should be written in markdown as one cell using `<br>`: `燃烧烟草 (600-900°C)<br>雾化器加热<br>口腔黏膜吸收`.
- **Avoid using `|` inside cell content** — if a cell requires listing multiple items separated by pipes, use commas or `<br>` instead.
- **Wide tables with many columns are hard to read in PDF.** Consider splitting a wide table into two separate tables grouped by theme (e.g., one table for product attributes, another for commercial metrics).

When in doubt: write for the reader who will skim the table, not for the analyst who already knows the data.
