# Finance Date Discipline

Use this file when the research involves companies, stocks, valuation, financial performance, guidance, delivery volumes, market share, or any numeric claim whose meaning depends on reporting period or data source.

Do not present financial numbers as if they all have the same certainty or time meaning.

## Core rule

For important financial or valuation claims, make the time basis and source type explicit.

A number without time basis, source type, or reporting status is often misleading even if the number itself is plausible.

## Separate these categories

Always distinguish between:

1. Historical reported facts
2. Current market snapshot
3. Forward-looking targets or estimates
4. Derived or inferred calculations

Do not blur them together.

## 1. Historical reported facts

Examples:

- annual report revenue
- interim report gross margin
- officially disclosed delivery volume
- audited or company-reported R&D spend

When using these, indicate:

- reporting period
- disclosure type
- whether it is audited, reported, or preliminary if known

Example phrasing:

- `According to Xiaomi's FY2024 annual report, ...`
- `In the latest reported interim results, ...`
- `The company disclosed cumulative deliveries of ...`

## 2. Current market snapshot

Examples:

- current market cap
- current share price
- current PE, PB, PS, EV/sales
- live analyst-consensus views shown on market platforms

When using these, indicate:

- snapshot date or time context
- platform/source type
- metric basis when relevant (for example TTM vs forward)

Example phrasing:

- `As of the market snapshot reviewed on 2026-03-30, ...`
- `The reported PE appears to be TTM rather than forward PE.`

### Mandatory for listed companies

**For any listed-company research, a current valuation snapshot is required, not optional.**

At minimum, include:

- approximate current stock price
- approximate market capitalization
- current valuation ratios (PE, PB, PS) with basis (TTM or forward) and date
- 52-week high/low range if relevant

If this data cannot be obtained cleanly, note the limitation explicitly rather than omitting it.

Do not write a listed-company investment memo without current market context. Historical financials alone are insufficient for investment analysis.

### Freshness hard gate for listed-company work

Before broad analysis, explicitly lock three time layers:

1. latest full-year reported period
2. latest quarterly / interim reported period
3. latest current market snapshot date

If the report date is materially later than the period being presented as "latest," stop and re-check whether a newer filing, earnings release, or market snapshot should already exist.

Common failure pattern:
- the report is dated well after a newer quarter should already be available
- an older annual or quarterly snapshot is easier to retrieve
- that older snapshot quietly becomes the opening anchor for the whole memo

Treat that as a freshness failure, not as a minor lag.

### Fail-fast rule: stale anchor invalidates the memo

For listed-company / investment-style work, a stale or mis-timed research anchor is not a cosmetic flaw.
It invalidates the memo until corrected.

If any of the following occurs:
- the report date is materially later than the allegedly latest quarter or interim period
- the research-anchor block names a period that does not plausibly match the filing calendar
- the agent cannot explain why no newer reported layer should reasonably exist

then do not continue writing through the inconsistency.

Required action:
1. stop synthesis
2. re-check the latest quarter / interim layer
3. either fix the anchor or explicitly state that the latest period could not be verified
4. if the latest period cannot be verified, downgrade the memo visibly rather than pretending the anchor is stable

A polished memo shape does not rescue a stale anchor.
In fact, the better the memo looks, the more dangerous a stale anchor becomes because readers are more likely to trust it.

When older numbers remain useful, label them as one of:
- historical background
- prior-cycle comparison
- older market snapshot

Do not let them stand in for current-state anchors.

## 3. Forward-looking targets or estimates

Examples:

- management target
- analyst consensus estimate
- media-reported expectation
- projected delivery volume
- inferred future revenue or margin

When using these, indicate clearly whether the number is:

- company target
- analyst estimate
- market expectation
- reasoned inference

Do not label these as confirmed facts.

Example phrasing:

- `Management has guided to ...`
- `Analyst consensus appears to expect ...`
- `This report infers ... based on ...`

## 4. Derived or inferred calculations

Examples:

- revenue converted between currencies
- valuation multiple calculated from current price and reported earnings
- back-of-envelope market share estimate
- estimated segment contribution inferred from external reports

When using derived numbers, indicate:

- what inputs were used
- whether the result is rough or precise
- what assumptions matter most

If assumptions are weak, lower confidence.

## Source-type labels to use when helpful

For key numeric claims, identify the source type in plain language. Useful labels include:

- annual report
- interim report
- earnings release
- company announcement
- investor presentation
- current market quote
- market-data platform snapshot
- analyst consensus
- media-reported estimate
- inferred calculation

## Common failure modes

Avoid these mistakes:

- writing estimated numbers as confirmed reported facts
- mixing TTM and full-year values without clarification
- presenting a target as if it were achieved performance
- using live valuation ratios without snapshot date
- quoting market-share or shipment numbers without period definition
- blending company disclosures and third-party estimates into one table without labels
- compressing a confirmed corporate action directly into an operating or valuation conclusion without separating what is fact vs implication vs open uncertainty

## Corporate-action compression guard

For listed-company work, treat these as a separate reasoning layer rather than ordinary company facts:

- asset injection
- M&A
- financing completion
- restructuring
- capacity expansion approval or registration
- major strategic partnership with claimed earnings impact

When these events matter to the thesis, split them explicitly into three layers:

1. confirmed transaction or event facts
2. likely operating / financial implications
3. open uncertainty about timing, realization, integration quality, or scenario dependence

Do not compress these three layers into one smooth sentence such as:
- `配套融资完成，打开中期成长空间`
- `资产注入落地，将显著增厚利润`
- `重组完成后成长确定性提升`

Better pattern:
- `已确认事实：公司已完成某项融资 / 注入 / 重组。`
- `可能影响：若按当前披露口径顺利并表或协同兑现，可能带来产能、储量、收入结构或成本结构变化。`
- `未知事项：兑现节奏、协同质量、盈利质量、资本开支压力、整合摩擦仍待后续披露验证。`

This guard matters because corporate actions often create a false sense of precision:
- the transaction fact is real
- but the economic consequence remains only partially known

If the consequence is still conditional, write it as conditional. Do not let transaction finality masquerade as thesis finality.

## Precision discipline (from GPT vs Minimax distillation)

**Use exact figures when the source provides them.** Do not round figures by default.

- Bad: `"约427万辆" when the source gives 4,272,145`
- Good: `"4,272,145辆 (据公司月度产销快报年累计)"`
- `"约" is acceptable only when the source itself provides rounded data` — not as a default style

When source provides an exact number, use it. Preserve significant digits unless rounding is explicitly noted.

## Forward-looking estimates must cite the source

Every estimate, projection, or target figure must attribute the source of the estimate — not just the word "预计."

- Bad: `"2025年海外销量预计超100万辆"`
- Good: `"据路透社引公司业绩沟通指引，预计2025年海外销量超100万辆"`
- `"据[机构/分析师/媒体]预计"` is required; bare "预计" without source attribution is insufficient

This applies to: management guidance, analyst consensus, media-reported targets, implied projections.

## Volume + profitability signal pairing

When reporting volume or scale growth, always check whether profitability and cash flow signals exist — and if they do, present them together.

Example pattern — the "规模扩张、盈利承压" structure:

- Bad (separate): `"2025年销量约460万辆。" "2025年净利润下滑19%。"` — reader must connect the dots
- Good (paired): `"规模仍在扩张（2025年销量约460万辆），但盈利与现金流承压（净利润下滑约19%，经营现金流同比下降约56%）"` — tension is explicit

This pairing is especially important when both positive and negative signals coexist in the same period.

## Date discipline checklist

For any important numeric section, ask:

- What period does this number belong to?
- Is it historical, current-snapshot, or forward-looking?
- Is it reported, estimated, quoted, or inferred?
- Does the source define the metric clearly?
- Would a reader misread this as more certain than it is?

If yes, rewrite.

## Output expectation

For company or investment research, the final answer should make the time layering visible.

A good report should help the reader distinguish:

- what the company has already reported
- what the market currently reflects
- what management or analysts expect next
- what the report itself is inferring

## Confidence discipline

Lower confidence when:

- the latest official disclosure is missing
- current market metrics are not clearly time-stamped
- estimates are being used because reported data is unavailable
- multiple sources disagree on period or metric definition
- the report depends heavily on inferred values
