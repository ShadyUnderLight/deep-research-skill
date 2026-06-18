# Market Outlook Audit Checklist

Use this checklist when the task is mainly about how a market, category, product class, or industry is likely to evolve over the next 6–24 months.

Examples:
- industry evolution or adoption trajectory
- market direction or structural change
- scenario memo for a changing market
- strategic outlook for buyers / operators / investors

Run this checklist before delivery.

## Route boundary check

- [ ] the task's core output is direction, evolution, or trajectory — not ranking, prediction, or selection among defined options
- [ ] the route's "Do not use" clauses from `ROUTING-MATRIX.md` have been checked against the task
- [ ] if the task mixes market-evolution and selection/ranking questions, the primary burden has been identified and the correct primary route selected

## Current market snapshot

- [ ] the report starts from a verified current baseline before forward-looking sections
- [ ] current baseline market state is separated from scenario logic
- [ ] current leading products / vendors / architectures are identified when relevant
- [ ] current pricing, policy, or packaging changes that alter the near-term outlook are noted
- [ ] evidence date basis is explicit

## Drivers and blockers

- [ ] drivers (forces that accelerate) and blockers / frictions (forces that slow) are clearly separated
- [ ] drivers and blockers are not mixed into a flat trend list
- [ ] each driver or blocker is specific enough to be decision-relevant, not generic

## Value-chain sensitivity coverage

- [ ] if the topic contains 产业链 / value chain / supply chain / infrastructure chain, a value-chain sensitivity map is present
- [ ] each chain layer includes exposure, bottleneck mechanism, beneficiaries/losers, timing, evidence strength, change-condition
- [ ] the map is not a flat description but shows inter-layer transmission logic

## Structured multi-scenario analysis

- [ ] at minimum a base case and one credible alternative scenario exist
- [ ] all scenarios share the same load-bearing metric as their quantitative axis — no mixing different metrics
- [ ] each scenario has explicitly stated key assumptions
- [ ] each scenario has observable trigger conditions that would signal it is becoming more or less likely
- [ ] when uncertainty is material, three scenarios (optimistic / base / pessimistic) are present
- [ ] probability weights are not assigned with false precision — directional labels used when evidence cannot support precise percentages
- [ ] the report does not rest on a single base case with no uncertainty structure

## Stakeholder implications

- [ ] at least 3 distinct stakeholder types are covered (see hard-fail gate below; scope-focused reports targeting a single stakeholder type are exempt with explicit scope declaration)
- [ ] investor-only coverage is not the sole stakeholder lens
- [ ] each covered stakeholder type has a dedicated "what does this mean for them" subsection
- [ ] for each stakeholder type: who should act now, what they should do, what they should avoid overcommitting to, and what they should monitor next
- [ ] stakeholder implications are not collapsed into a single generic paragraph

### Stakeholder coverage hard-fail gate

- [ ] （阻断级）报告覆盖的不同 stakeholder 类型少于 3 类（示例最小三类：买家/用户、供应商/平台、投资者/监管）
- [ ] 本 hard-fail 独立于 ROUTING-MATRIX.md §Market Outlook 中的 stakeholder hard-fail（"covers only investor stakeholder implications"），两者需同时检查

**不触发条件（同时满足）：**
- 报告 scope 已明确声明聚焦单一 stakeholder 群体（标题暗示受众、开头声明 scope 如"面向 X 的决策参考"、"本文旨在为 X 提供参考"）
- 且未以全球/行业全景报告自居（如标题含"市场全景"、"行业分析"、"全球展望"等措辞）

### Stakeholder actionability（enhanced, when implementation burden exists）

- [ ] stakeholder implications use action table format (decision / action / metric / trigger) when the report involves implementation, deployment, or organizational change
- [ ] each action has a concrete, checkable recommendation (not "关注趋势")
- [ ] "Trigger to revise" column includes specific threshold or condition for at least half of entries

## Quantitative role labeling

- [ ] important numbers are labeled as observed current metric / inferred estimate / scenario assumption / illustrative calculation
- [ ] readers can tell which kind of number they are reading without guessing
- [ ] （阻断级）Declared-not-executed check: if the report defines an O/P/A/M or equivalent role system for market-outlook numbers, the body must apply that system to scenario tables, market-size numbers, growth rates, adoption projections, probabilities, and other load-bearing numeric claims. A label legend without body/table application does not satisfy quantitative role labeling.
- [ ] Declared role system but 0% body/table application → hard-fail. Declared role system but <50% application to applicable market-outlook numbers → conditional-pass ceiling and quantitative-role labeling may not be marked ✅ Passed.

## Forward-looking claims

- [ ] every forward-looking claim has a labeled source role
- [ ] `预计` / `expected` / `likely` has named source attribution (who expects this?)
- [ ] forecasts show key assumptions and failure / reversal conditions

### Forward-looking label hard-fail gate

- [ ] （阻断级）扫描所有包含前瞻触发词的数字陈述：`预计`、`预测`、`预期`、`将达`、`有望`、`expected`、`forecast`、`projected`、`estimated to`、`will reach`、`by 20xx`。
- [ ] 前瞻数字不得标为 `[确认]`、`[已确认事实]`、`[CONF]`、`[Confirmed]`，即使来源是权威机构、公司指引或分析师报告；可确认的是“某来源发布了该预测”，不是“未来数值会发生”。
- [ ] 前瞻数字必须使用 estimate / scenario-assumption / analyst estimate / inference / model-output 等来源角色或数字角色标签，并给出归因来源和时间 basis。
- [ ] 例外：已经发生并已被审计、披露或直接观测的 historical / current metric（如“2025 年实际营收”）可标为确认事实；仅描述“Gartner 于 2026-01 发布预测”且不把预测数值当事实时，也不触发。
- [ ] 同一报告中出现 >3 处“前瞻数字标为确认事实”或任一 load-bearing scenario assumption 被标为确认事实 → hard-fail。

## Regional coverage (global scope)

- [ ] if the report title/question contains 全球 / global / 区域 / region, a regional coverage matrix is present
- [ ] each region in the matrix has a Data role column (observed / estimate / forecast / scenario / proxy)
- [ ] each regional key metric has an `[Sxx]` inline citation
- [ ] if the report claims "global" but only covers US/China/EU, a scope completeness warning is present or the report explicitly qualifies its scope

## Monitoring and change conditions

- [ ] the report identifies what would change the conclusion
- [ ] monitoring signals are specific and observable
- [ ] the report does not give a bottom line without explaining what would flip it

### Monitoring signal actionability hard-fail gate

- [ ] （阻断级）If more than 3 monitoring signals are only qualitative reversal-condition items, with no measurable threshold, observation cadence, data source, or trigger-to-action mapping, the monitoring section may not be marked as passed.
- [ ] at least 3 monitoring signals should include all four actionability fields: measurable threshold, observation cadence, data source, and trigger-to-action mapping.
- [ ] Remaining lower-priority signals may be simpler, but each should still name the reversal condition and observation source.
- [ ] A fully qualitative list such as "watch costs, regulation, demand, and capex" is not enough for a market-outlook dashboard, even if it names plausible variables.

## Decision usefulness

- [ ] the report functions as a decision memo about a changing market, not just an industry overview
- [ ] the reader knows what to do next based on the outlook
- [ ] the opening 20–30% already reflects the market-outlook route rather than reading like generic background

## Quality bar

A market-outlook report that fails this checklist may still be informative, but it is not yet a proper decision-useful market memo.
