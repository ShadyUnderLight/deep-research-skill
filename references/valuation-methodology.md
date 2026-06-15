# Valuation Methodology

Use this file when the research involves valuation judgments, target prices, valuation multiples, or any claim about whether a company is cheap, expensive, fairly valued, or mispriced.

Do not confuse a valuation snapshot with a valuation judgment.

## Core rule

A valuation snapshot is a data point. A valuation judgment is a conclusion that requires methodology, assumptions, and evidence quality assessment.

Presenting a PE ratio without methodology context is reporting. Concluding that a stock is "undervalued" or "overpriced" is a judgment that carries a higher evidence burden.

## Snapshot vs judgment

Always separate:

1. **Valuation snapshot** — current market data: stock price, market cap, PE, PB, PS, EV/EBITDA, dividend yield, 52-week range. This is observed fact from a market platform.
2. **Valuation judgment** — whether the current pricing is justified, stretched, or discounted relative to fundamentals, peers, or intrinsic value. This requires methodology and assumptions.

Do not let a snapshot masquerade as a judgment. `The stock trades at 15x TTM PE` is a snapshot. `The stock appears cheap relative to its historical range` is a judgment that needs supporting evidence.

## Metric selection logic

Choose valuation metrics based on company characteristics, not habit.

### PE (Price / Earnings)

Use when:
- earnings are positive and reasonably stable
- the company is not highly cyclical at a trough or peak
- the business model is not undergoing structural transition

Do not use when:
- the company is loss-making or has volatile earnings
- the industry is at a cyclical extreme (peak or trough)
- one-time gains or losses distort reported earnings

### PB (Price / Book)

Use when:
- asset values are meaningful (banks, insurance, real estate, industrials)
- earnings are volatile but book value is more stable
- the company has significant tangible assets

Do not use when:
- the company is asset-light (software, services, platform businesses)
- intangible assets dominate but are not reflected in book value
- book value is negative or distorted by accumulated losses

### PS (Price / Sales)

Use when:
- the company is loss-making or margin structure is unstable
- revenue is more reliable than earnings for the business model
- the company is early-stage but has meaningful revenue

Do not use when:
- margin structure is stable and well-understood (use PE instead)
- revenue quality is questionable (related-party, one-time, unsustainable)

### EV/EBITDA

Use when:
- capital structure differences matter (comparing levered vs unlevered companies)
- depreciation policies distort earnings comparisons
- the industry standard uses this metric (telecom, media, infrastructure)

Do not use when:
- working capital or capex intensity varies dramatically without adjustment
- the company has significant operating leases not reflected in EBITDA

### DCF (Discounted Cash Flow)

Use when:
- cash flows are predictable enough to model
- the company has a long operating history
- terminal value assumptions can be reasonably bounded

Do not use when:
- cash flows are too volatile or uncertain for meaningful projection
- the company is pre-revenue or pre-profit with no clear path
- the model would depend on speculative assumptions about distant future

> **Forward reference**: For when DCF is **required** rather than merely available — including trigger conditions, acceptable outputs, and degradation rules — see §DCF / reverse DCF trigger below.

### SOTP (Sum of the Parts)

Use when:
- the company has distinct business segments with different valuation logics
- conglomerate discount or premium is material
- segment-level data is sufficient for independent valuation

Do not use when:
- segment data is insufficient or unreliable
- inter-segment dependencies make separation artificial

## DCF / reverse DCF trigger

DCF is listed above as one of several valuation methods. This section defines when DCF is **required** rather than merely available.

### Applicable trigger conditions

A listed-company valuation must include DCF or reverse DCF (or an explicit explanation of non-applicability) when ALL of the following are true:

- **Operating history**: The company has a sufficiently long operating history (typically 10+ years of reported financials).
- **Cash flow predictability**: The company has positive and reasonably predictable free cash flow.
- **Long-term growth dependency**: The report's core valuation question is whether long-term growth (5+ years) is already reflected in the current price, and/or the valuation conclusion depends on assumptions about revenue growth, margin structure, CapEx intensity, or FCF conversion extending 5+ years into the future.
- **PE/PEG insufficiency**: PE or PEG ratios alone cannot adequately capture the long-term growth realization path, or the company's growth profile makes pure multiple-based valuation misleading.

### Acceptable outputs (choose one)

1. **Forward DCF**: Explicit projections of revenue, operating margin, D&A, CapEx, tax rate, WACC, and terminal value, producing a per-share fair value range. Key assumptions must be labeled with number roles (assumption / model output / observed input) and source/method.

2. **Reverse DCF**: Starting from the current market price, calculate the implied revenue growth, FCF margin, terminal growth rate, or WACC embedded in the current valuation, then evaluate whether those implied assumptions are reasonable relative to available evidence.

3. **Non-applicability explanation**: If DCF is deemed not applicable (despite meeting the trigger conditions superficially), the report must explain specifically why — e.g., "FCF is too volatile for meaningful projection due to [reason]" or "terminal value would dominate unreasonably because [reason]." Vague justifications such as "DCF is not needed" without specific reasoning do not satisfy this requirement.

### Degradation rule

If DCF is determined to be not applicable after the above assessment:

- The report must still satisfy the existing methodology requirements (metric selection logic, target price discipline, and precision downgrade rules).
- The valuation conclusion must be visibly downgraded — "directional" or "range-based" rather than "precise" — because the absence of a cash-flow-based structural model reduces the precision ceiling.
- The non-applicability reasoning must be visible in the valuation section, not buried in a footnote or appendix.

### Relationship to other rules

- `references/report-template.md` §Valuation method and scenario analysis contains the DCF assumption table template and sensitivity matrix template.
- `references/quantitative-role-labeling.md` §Sensitivity classification defines the sensitivity analysis framework that applies to DCF assumptions.
- `checklists/listed-company-report.md` §DCF / 反向 DCF contains the enforcement checklist.

## Precision downgrade rules

Downgrade valuation precision when the company or data quality does not support precise conclusions.

### Cyclical companies

- Do not use peak or trough earnings as the base for PE valuation without explicit cycle-stage labeling
- Prefer mid-cycle earnings normalization or PB when cycle position is uncertain
- Label the valuation as "cycle-dependent" rather than presenting a single-point PE

### Loss-making companies

- Do not force a PE-based valuation
- Use PS, EV/Revenue, or EV/EBITDA if margins are expected to normalize
- If no reasonable metric applies, state that valuation cannot be meaningfully assessed with available data
- Do not invent a "forward PE" based on speculative profitability timeline

### High-growth companies

- Forward PE or EV/Revenue may be more relevant than TTM PE
- But label clearly: "based on consensus estimates" or "based on management guidance"
- Do not present forward metrics as if they were reported facts
- Acknowledge that growth assumptions drive the valuation heavily

### Companies with major corporate actions

- If M&A, restructuring, asset injection, or spin-off is pending or recent, valuation may be distorted
- Split the valuation into pre-action and post-action scenarios when relevant
- Do not compress transaction certainty into valuation certainty

### DCF-triggered-but-declined

When all DCF trigger conditions are met but DCF is deemed not applicable (see §DCF / reverse DCF trigger → Non-applicability explanation):

- The valuation precision ceiling is **directional or range-based**, not precise.
- A single-point target price should not be given; prefer a valuation range with explicit assumptions or a directional judgment.
- The non-applicability reasoning must be visible in the valuation section (not buried in a footnote), so the reader can assess whether the DCF avoidance is justified.

## Target price discipline

Do not give a target price unless:
- sufficient data exists to support a methodology
- the assumptions are explicit and defensible
- the time horizon is stated
- the confidence level is honest

When target price cannot be supported, prefer:
- directional judgment (looks stretched / appears reasonable / seems discounted)
- valuation range with explicit assumptions
- "insufficient data for a target price" as a valid conclusion

## Valuation inference documentation

When presenting a valuation range, target price, or fair value estimate labeled as inference, the reader must be able to reconstruct the reasoning chain. Do not present a valuation conclusion without visible methodology.

### Required elements for valuation inference

Every valuation inference must include:

1. **Multiple assumption range** — state the PE (or other metric) range used, not just the final number. Example: "基于2026年预期PE 25-30x" rather than "目标价600元"
2. **Comparable selection logic** — if comparables are used, state why these companies were chosen and what they share with the target. Do not assume the reader knows why Company X is a valid comp
3. **Scenario parameters** — if the valuation uses optimistic/base/pessimistic scenarios, state the key variable that differs across scenarios (e.g., margin assumption, growth rate, market share)
4. **Limitation disclosure** — state what the valuation does not capture or where the methodology is weakest

### Metric selection justification

When the report uses one metric as the primary valuation anchor, briefly state why. This is especially important when:

- the company has characteristics that could support multiple metrics (e.g., positive earnings AND significant assets)
- the chosen metric is not the industry default
- the company is in a transitional state (post-restructuring, cyclical trough, high-growth phase)
- the company has significant related-party transaction exposure or concentrated ownership that could distort earnings quality

Example patterns:
- "选用PE而非EV/EBITDA作为主要估值锚，因为[公司]资本结构简单、折旧政策稳定，PE更能反映股东视角的回报预期"
- "选用EV/EBITDA而非PE作为主要估值锚，因为[公司]关联方交易占比高，PE可能受非经常性损益影响较大，EV/EBITDA更能反映经营层面的真实估值水平"

For loss-making or cyclical companies, see the precision downgrade rules above. If no metric applies cleanly, say so.

### Common failure patterns

- Presenting a target price without stating the multiple or methodology
- Using "保守区间" or "合理估值" without showing the assumptions behind the range
- Choosing comparables without explaining the selection logic
- Stating a PE range without explaining why that range is appropriate for this company's growth/risk profile

## Common failure patterns

### Using TTM PE for cyclical stocks
A cyclical company at peak earnings will show a low PE that suggests "cheapness." This is misleading if earnings are about to mean-revert.

### Forcing PE on loss-making companies
Presenting a "negative PE" or ignoring the loss-making status to maintain a PE-based framework is a methodology failure.

### Treating SOTP as a precision tool without segment data
If segment-level financials are unavailable or unreliable, SOTP creates false precision. The result looks analytical but is assumption-driven.

### Presenting forward metrics as reported facts
`The stock trades at 12x forward PE` is acceptable. `The stock has a PE of 12` when the 12x is forward-based is misleading.

### Conflating snapshot with thesis
`The stock is cheap because it trades at 10x PE` is not a valuation thesis. It is a snapshot with an unsupported conclusion. A proper thesis would explain why 10x is cheap relative to what benchmark and why.

## Capital return discipline for CapEx-heavy companies (重资产公司的资本回收纪律)

当分析资本密集型上市公司的估值时，仅使用收入增长和 PE/PEG 框架可能掩盖最关键的财务问题：增长是否以足够高的回报率沉淀为自由现金流和股东价值。

### 触发条件

以下**任一**条件满足时，必须启动本纪律：

- **行业属性**：公司属于半导体制造、工业制造、能源、电力、数据中心、通信基础设施、矿业/金属、化工/石化等资本密集型业务。
- **CapEx 强度**：CapEx / 收入长期高于 20%，或显著影响自由现金流。
- **Thesis 依赖**：报告核心 thesis 依赖产能扩张、新节点爬坡、海外建厂、重资产投入。
- **增长模式**：收入增长主要来自增加产能/固定资产而非价格/产品 mix 改善。

### 必须回答的六个问题

当本纪律触发时，报告必须在估值章节（或紧邻的四变量分解段）中回答以下问题，而非仅将 CapEx 风险列在风险段落：

1. **增长来源**：收入增长来自价格、出货量、产品 mix，还是一次性周期因素？区分可持续增长与周期波动。
2. **再投资负担**：实现增长需要多少 CapEx、营运资本（ΔWC）和 D&A？收入扩张期间的应收账款和库存积累对 FCF 的实际消耗是多少？CapEx / 收入比率和 ΔWC / 收入比率是否高于同行业可比公司，如果是，原因是什么？
3. **利润率稀释**：新产能、新地区、新节点或学习曲线是否短期压低 margin？具体影响幅度和时间范围是什么？
4. **FCF 转换**：净利润增长是否确实转化为自由现金流增长？D&A 和 CapEx 的差额（即 reinvestment gap）对 FCF 的实际影响是什么？
5. **ROIC 与回收周期**：增量资本回报率（推荐使用 incremental ROIC：ΔNOPAT / ΔInvested Capital，更直接反映新投入的产出效率）是否高于 WACC？回收周期是否在投资人可接受范围内？增长是否在扩大收入规模但并未提高股东回报？
6. **估值影响**：如果 CapEx 强度持续高于假设，或 FCF 转换低于预期，估值结论如何变化？PE/PEG 框架能否单独支撑结论，还是需要 DCF 或 ROIC 分析？

### 常见失败模式

- **增长故事代替资本回报分析**：报告强调 TAM 和收入增长，但未检查增长的资本成本。读者无法判断增长是否创造价值。
- **风险清单代替估值输入**：CapEx 和 FCF 风险列在风险章节，但估值结论（目标价、PE 倍数判断）沿用 PE/PEG 框架，未纳入这些风险。
- **轻资产模板套用到重资产公司**：用标准的"收入增长 + PE 倍数收缩/扩张"模板分析半导体制造或数据中心公司，忽略了 FCF 转换的关键问题。
- **忽视 margin 稀释的阶段差异**：新节点/新产区初期爬坡的 margin 稀释是暂时性的，但如果不量化阶段和回收期，容易将过渡期问题误判为结构性缺陷，或反过来忽视其量化影响。

### 与现有规则的关系

- 本纪律的四变量关联：六个问题中的问题 1-4 对应四变量分解的变量 3（利润率与现金流转换），问题 5-6 对应变量 4（估值透支程度）。本纪律为四变量分解中 CapEx-heavy 场景提供更详细的执行指导。
- 本纪律与 `references/report-template.md` §增长到现金流转换表 配合使用：该表提供定量框架，本纪律提供分析问题集。
- 本纪律不替代 DCF 触发条件：如果满足 DCF 触发条件（见 §DCF / reverse DCF trigger），DCF 仍然必须执行。本纪律在 DCF 不适用时提供最低限度的资本回收分析框架。

## Relationship to other discipline files

- `references/finance-date-discipline.md` covers time-layer separation and source-type labeling for financial numbers. This file focuses on methodology selection and precision discipline.
- `references/analyst-consensus-handling.md` covers how to handle consensus estimates and target prices from third parties.
- `references/reporting-period-handling.md` covers reporting-period definitions and TTM/LTM/NTM conventions.
