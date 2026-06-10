# Quantitative Role Labeling

## Purpose

Quantitative role labeling exists to prevent precise-looking numbers from overstating certainty.

In deep research and decision-oriented reports, load-bearing numbers often mix:

- observed metrics
- proxies
- assumptions
- model outputs
- illustrative calculations

If their role is unclear, a report can look rigorous while quietly presenting planning logic as fact.

## Core rule

Never present proxy, assumption, or model output as if it were an observed or directly reported fact.

If a number materially affects ranking, recommendation, timing, sequencing, confidence, or valuation, its role should be visible.

## Core roles

### Observed metric
A number directly observed, officially reported, or clearly measured by the cited source.

### Proxy
A number used to indirectly support a conclusion about something else.

### Assumption
A number introduced as an input to reasoning, estimation, or scenario construction.

### Model output
A number produced from assumptions, proxies, or selected parameters.

### Illustrative calculation
A number used to clarify logic rather than claim a formal estimate.

## What should be labeled

Quantitative role labeling should be visible when a number materially affects:

- recommendation
- ranking
- shortlist construction
- go / not now / pilot only judgment
- sequencing
- timing
- valuation
- confidence

If removing the number would materially weaken the argument, its role is probably load-bearing and should be visible.

When a number is classified as a medium- or high-sensitivity assumption, sensitivity analysis should also be visible. See "Sensitivity classification" below.

## Common failure modes

Common failures include:

- proxy presented as direct evidence
- assumption presented as observed fact
- model output presented as externally verified reality
- composite score shown without clarifying the role of its inputs
- precise-looking numbers carrying more certainty than the evidence supports

## 假设链 — Assumption chain documentation

Labeling a number as "assumption" is a necessary first step. It tells the reader what epistemic role the number plays. But it does not explain why that particular value was chosen or what would change if it turned out wrong.

An assumption chain makes the reasoning behind a load-bearing assumption visible, auditable, and testable.

### When to document an assumption chain

Not every assumption needs a full chain. Apply this scope rule:

- **Required** — assumptions whose deviation would materially affect the conclusion (high sensitivity). If a ±20% change in the assumption would alter the recommendation, shift the ranking, or change valuation by more than ±15%, the assumption chain is mandatory. See also "Sensitivity classification" below for the full classification framework.
- **Optional** — assumptions whose impact on the conclusion is estimated at under ±20% (or under ±15% for valuation only). A lightweight note is sufficient. If the impact falls in the 15–20% range for non-valuation conclusions, analyst judgment applies; err on the side of documenting.
- **Not needed** — directly observed or officially reported facts (observed metrics). Facts do not become assumptions by being inconvenient.

### Remediation when a chain cannot be completed

If a high-sensitivity assumption cannot support a complete assumption chain, apply one of:

1. **Fill the chain** — search for the missing evidence from available sources. If only partial information exists, document what is known and what remains uncertain, then downgrade confidence accordingly.
2. **Downgrade sensitivity** — reclassify the assumption as lower-sensitivity if the chain gap reveals the assumption is less load-bearing than initially assessed.
3. **Restructure the analysis** — reduce dependence on the assumption, or replace it with a more directly verifiable input or a range-based scenario.

Do not leave a high-sensitivity assumption's chain incomplete without an explicit remediation decision and rationale.

### Assumption chain template

For each key assumption, document the following fields. Not every field must be populated; mark genuinely inapplicable fields as `N/A`.

```
### 假设: [具体假设陈述]

- 类型: [假设 / proxy / 估算 / 模型输出]
- 支持证据:
  - 来源 A: [具体依据]
  - 来源 B: [具体依据]
- 依赖条件（假设成立的前提）:
  - 宏观环境: [如不衰退、利率稳定]
  - 竞争格局: [如无颠覆性对手出现]
  - 技术路线: [如主流方案不变化]
- 敏感度:
  - 假设偏差 ±10% → 结论变化 X%
  - 假设偏差 ±50% → 结论变化 Y%
- 失效信号（可观察的事件/数字）:
  - [如 Q1 增速低于 X%，则假设需调整]
  - [如核心客户转向竞品，则假设需放弃]
- 置信度: [高/中/低]
```

### Sensitivity classification

Classify each key assumption by its impact on the conclusion. This determines the required depth of sensitivity testing.

| Classification | Definition | Test amplitudes | Required treatment |
|----------------|------------|-----------------|-------------------|
| **Low sensitivity** | Conclusion unchanged within ±20% deviation | ±20% | Conclusion is robust; label the sensitive variable |
| **Medium sensitivity** | Conclusion direction unchanged but strength changes within ±20% | ±20%, ±50% | Conclusion holds conditionally; label the tipping point |
| **High sensitivity** | Conclusion reverses within ±20% deviation | ±20%, ±50%, extreme scenario | Conclusion is assumption-dependent; reduce confidence. Both sensitivity table and scenario analysis required. |

**情景分析 ≠ 敏感性分析**：情景分析同时变动多个假设（如乐观/基准/悲观三情景），读者无法看到单一关键假设变化对结论的独立影响。敏感性分析每次只变一个假设，揭示哪个变量是结论的转折点。当报告提供多情景分析时，仍需对高敏感性假设提供独立敏感性表（±20%、±50%）。两者互补而非替代。

**Test amplitude selection**:

- **Routine assumptions** (e.g., market growth rate, cost assumptions): test ±20% and ±50%
- **Load-bearing assumptions** (e.g., valuation multiples, core revenue growth): test ±20%, ±50%, and at least one extreme scenario
- **Structural assumptions** (e.g., technology roadmap, regulatory environment): test reversal scenarios (what happens if the assumption fails entirely)

**Output format**:

```
### 敏感性分析: [假设名称]

| 变量 | 基准值 | -50% | -20% | +20% | +50% | 对结论影响 |
|------|--------|------|------|------|------|-----------|
| 市场增速 | 15% YoY | 7.5% | 12% | 18% | 22.5% | ±X% to 核心结论 |

- 敏感度等级: [低/中/高]
- 临界点: [结论翻转的阈值]
- 建议: [降低 confidence / 补充敏感性分析 / 维持现有结论]
```

**When to apply this classification**:

- **Required** — assumptions classified as high sensitivity. Full sensitivity table and scenario analysis are mandatory.
- **Recommended** — assumptions classified as medium sensitivity. At minimum, document the tipping point.
- **Optional** — assumptions classified as low sensitivity. A brief note is sufficient.

### Template example

```
### 假设: 该公司年增速在未来 3 年保持 15%

- 类型: 假设（基于行业平均增速推测）
- 支持证据:
  - 公司过去 3 年 CAGR 为 14–18%（年报披露）
  - 行业第三方预测未来 3 年增速 12–16%（IDC 报告 [S01]）
- 依赖条件:
  - 宏观环境: 目标市场不出现衰退
  - 竞争格局: 无新进入者以显著更低价格抢份额
  - 技术路线: 现有产品路线不被替代方案颠覆
- 敏感度:
  - 偏差 ±10%（13.5% 或 16.5%）→ 估值变化约 ±15%
  - 偏差 ±50%（7.5% 或 22.5%）→ 估值变化约 ±70%，推荐强度需重新评估
- 失效信号:
  - Q1 营收增速低于 10% → 假设需下调
  - 核心产品 ASP 连续两季下降 → 增速假设可能偏乐观
- 置信度: 中（依赖宏观条件，且竞争格局有不确定性）
```

### Common failure patterns

#### Pattern 1: Proxy used as assumption without justification

A proxy (e.g., patent count as proxy for innovation capability) is silently treated as a valid assumption without explaining why the proxy is reasonable.

**Fix**: State why this proxy is reasonable for the specific context, or downgrade the claim strength.

#### Pattern 2: Assumption chain omitted for high-sensitivity numbers

A number that drives the recommendation has no visible assumption chain — the reader cannot tell what would change the conclusion.

**Fix**: Add the assumption chain. If the assumption is simple, a compact inline version is sufficient.

#### Pattern 3: Assumption stated but dependency conditions missing

The assumption is named ("assume 15% growth"), but the conditions that must hold for it to be valid are not documented.

**Fix**: Add dependency conditions. At minimum, name the 1–2 external conditions most likely to break the assumption.

### Relationship to other discipline files

- `references/forward-looking-discipline.md` has an "Assumption chains" section for forward-looking numbers (revenue projections, market size forecasts, adoption timelines). The template here is the general-purpose version. For forward-looking claims, that file's lighter pattern may be sufficient; for complex or high-sensitivity assumptions, the full template here applies.

## 厂商声明与媒体估计的特殊标注规则

当数据的来源属于以下两类时，必须在正文中显式标注其角色，不能仅依赖 Source Register 的 metadata：

### 厂商自述（manufacturer self-reported）

数据来自公司官网、新闻稿、官方社交媒体、合作伙伴声明等未经过独立第三方验证的来源。

- 正文引用时必须附加内联说明，如 `(来源：厂商自述，非独立验证)`
- 不得单独标注为 `[已确认事实]`

### 媒体估计（media estimate）

数据来自彭博、券商研究报告等第三方推断性来源（register 类型 `SECONDARY_MEDIA`、`SECONDARY_ANALYST`）。

- 不得标注为 `[已确认事实]`
- 应使用 `[推断]` 或具体来源角色如 `[彭博 estimate]`

### 何时需要标注

判断标准：如果删除这行内说明后，读者无法区分"独立验证的事实"和"来源主动声称但未独立验证的数字"，就需要标注。

### 与 Source Register 的关系

参见 `references/source-traceability-and-claim-citation.md` 的「来源标注一致性」章节，其中定义了 register 与正文标签强度的一致性原则。

## 来源类型到证据标签的校准规则

### 核心原则

**标签强度 ≤ 来源类型允许的最大强度。** 二级/推断性来源承载的主张不可仅标注 `[已确认事实]` 而不附加来源角色说明。例外必须记录理由到 process log 或审计状态区块。

### 来源类型 → 允许标签映射表

| 来源类型（granular） | 可标注的最高标签 | 必须附加的说明 |
|---|---|---|
| `PRIMARY_FILING`（监管/年报/交易所公告） | `[已确认事实]` | 无需额外说明，但需标注期间 |
| `PRIMARY_COMPANY`（官网/新闻稿/股东信） | `[已确认事实]` + 来源角色 | 必须附加内联说明 `(来源：厂商自述，非独立验证)`（见 `references/source-traceability-and-claim-citation.md` §来源标注一致性）；可补充来源角色如"（据公司官网）" |
| `PRIMARY_PARTNER`（合作伙伴公告） | `[已确认事实]` + 来源角色 | 必须附加内联说明 `(来源：厂商自述，非独立验证)`（见 `references/source-traceability-and-claim-citation.md` §来源标注一致性）；可补充来源角色如"（据[合作伙伴]声明）" |
| `PRIMARY_DEV`（GitHub 仓库/API 文档/changelog） | `[已确认事实]` | 需标注版本号或 commit ref。Pre-merge PR 默认使用 `[推断]`，除非审计员确认可升级 |
| `SECONDARY_MEDIA`（媒体/行业报告） | `[推断]` | 必须标注"（据XX报道）"如 `[推断]（据路透社报道）` |
| `SECONDARY_ANALYST`（券商研报） | `[推断]` | 必须标注"（据XX分析师）"如 `[推断]（据高盛分析师）` |
| `SECONDARY_FEED`（RSS 摘要/聚合内容流） | `[推断]` | 必须标注来源名称 |
| `TRANSCRIPT`（转录/访谈/电话会） | `[已确认事实]` 或 `[推断]` | verbatim（逐字记录，经录音核对）→ `[已确认事实]`；summary/paraphrase → `[推断]`。无论哪种情况，必须标注来源场景（"据公司年报电话会"） |
| `INFERRED`（报告自身推断） | `[推断]` | 必须附推理链（见 `references/source-traceability-and-claim-citation.md` §Inference documentation） |
| `UNCONFIRMED`（无法独立验证） | `[未知]` | 必须标注"未经独立验证" |
| `WEAK_SIGNAL`（社交/论坛/匿名来源） | `[未知]` | 仅用于补充上下文，不得承载 load-bearing claim |

### 映射表使用规则

1. **register 优先**：上述映射适用于 register 中已正确分类的来源。如果 register 本身的类型标注错误，先修正 register 再应用映射规则。
2. **例外机制**：当 register 将某个 `SECONDARY_MEDIA` 或 `SECONDARY_ANALYST` 来源明确标为 `high` reliability（例如权威第三方基准测试报告），且来源质量经审计员确认，可酌情升级至 `[已确认事实]`。此例外不适用于 `SECONDARY_FEED`。例外必须记录理由。
3. **简化类型兼容**：使用简化 5 类（primary / secondary / vendor-claim / inferred / unconfirmed）时，`vendor-claim` 的规则同 `PRIMARY_COMPANY`/`PRIMARY_PARTNER`；`secondary` 的规则同 `SECONDARY_MEDIA`/`SECONDARY_ANALYST`/`SECONDARY_FEED`。
4. **标签强度一致性**：本映射表与 `references/source-traceability-and-claim-citation.md` §来源标注一致性 的关系——该章节定义 register 与正文间的标签强度约束（register ≥ body）；本映射表定义给定 register 类型时正文的**上限**。两者互补：register ≥ body 且 body ≤ 本表上限。

### 与现有规则的关系

本映射表不替代 `references/source-traceability-and-claim-citation.md` §来源标注一致性 中的双边一致性规则（register 标签 ≥ 正文标签），而是在 register 到正文的映射方向提供更精确的上限约束。

本映射表与 §厂商声明与媒体估计的特殊标注规则 的关系——该节（`quantitative-role-labeling.md` §厂商声明与媒体估计的特殊标注规则）定义了厂商自述和媒体估计这两类来源的特殊标注要求（不得单独标为 `[已确认事实]`）；本映射表将同一原则扩展为对所有 11 种 granular 来源类型的系统性覆盖，并提供统一的例外机制。两者在重叠区域语义一致：本映射表表中 `PRIMARY_COMPANY`/`PRIMARY_PARTNER` 的注释要求与 §厂商声明中的"不得单独标注为 `[已确认事实]`"一致，`SECONDARY_MEDIA`/`SECONDARY_ANALYST` 的注释要求与 §媒体估计中的"不得标注为 `[已确认事实]`"一致。

## Route-specific notes

### Market entry / regional expansion
Market size, payback, localization cost, and sequencing thresholds are often assumptions or model outputs rather than direct facts. Scoring/weighting matrices used for country ranking must label per-score role (observed / proxy / model-output).

### Constrained choice / shortlist
Weighted scores, burden proxies, and comparison totals often depend on proxies, assumptions, or model outputs. Star ratings, price comparisons, plugin/ecosystem counts, and growth rates must carry role labels. Composite scoring must disclose which dimensions are observed vs. modeled.

This route has a hard-fail in ROUTING-MATRIX.md: `uses numbers without labeling observed fact / proxy / assumption / model output` — the option-selection final audit (`checklists/option-selection-final-audit.md`) enforces this with a BLOCKER check.

### Market outlook / industry evolution
Growth ranges, projected adoption, and scenario paths should not read like observed current-state facts. Scenario probabilities (e.g., "20-25%") must be accompanied by estimation method or source basis, not bare qualitative judgment. Scenario assumptions must be visibly separated from current-state observations.

### Listed-company / investment-style research
Valuation ranges, scenario cases, and estimated financial outcomes often require explicit model-status visibility. Industry forecasts, market-share probabilities, and "提升 X%" claims should be labeled as estimate / analyst-inference / model-output / assumption rather than presented as established facts.

### Startup / private company evaluation
ARR/MRR figures must be labeled by source type (company-reported / estimated / inferred). Valuation multiples (e.g., PS 100x) require explicit boundary conditions (private-company premium context, comparable transaction range). "预计" / "估测" / "约" claims must include method note or source role — bare hedge wording is insufficient.

## Minimal display patterns

Quantitative role may be shown through:

- inline labels
- table columns
- note-style evidence tags

The format may vary.
Role visibility may not.

## 表格中的角色标签

When numbers appear in comparison tables, scoring tables, or estimation tables, the role label must be visible **at the table level** — not only in the surrounding prose.

### Correct: role column as part of table structure

Include a dedicated column that labels each row's number role. This is the recommended pattern:

```
| 维度 | 方案A | 方案B | 方案C | 数字角色 |
|------|-------|-------|-------|---------|
| 年营收 | $50M | $30M | $20M | 观察值（年报披露） |
| 市场增长率 | 15% | 12% | 10% | 代理指标（基于第三方行业预测推算） |
| 实施成本 | $5M | $3M | $2M | 模型输出（基于项目规模和同类产品定价） |
| ROI | 3.2x | 2.5x | 1.8x | 模型输出（基于前述成本和营收假设） |
```

Placement note: put the role column as the last or second-to-last column in the table. Use the last position by default; reserve the second-to-last spot when a confidence indicator or source-reference column logically follows the role column.

### Acceptable alternative: role header row

When the same role applies to all values in a column, a header row between column headers and data rows can be used:

```
| 维度 | 方案A | 方案B | 方案C |
|------|-------|-------|-------|
| 角色 | 观察值 | 代理指标 | 模型输出 |
| 年营收 | $50M | $30M | $20M |
| 市场份额 | 25% | 15% | 10% |
```

### Acceptable alternative: table-level note

If all numbers in a table share the same epistemic role, a single table note suffices:

```
> 注：本表所有数字均为模型输出，基于行业公开数据和所述假设计算，不应视为已确认事实。
```

### What is not acceptable

- A statement in the surrounding prose that "all numbers in this report are estimated" without a role indicator at the table level
- A single inline disclaimer in the introduction applied to every table without per-table annotation
- Mixing observed facts and model outputs in the same table without distinguishing them

The rule is: **the reader should not need to leave the table to determine the epistemic role of the numbers inside it.**

## Hard fail signs

- A load-bearing number has no visible role.
- A proxy is treated as direct evidence.
- A model output is written as if it were observed fact.
- A recommendation materially depends on unlabeled assumptions.
