# Quantitative Role Audit

## Core gate

If load-bearing numbers materially affect the conclusion, their roles should be visible.

## Checklist

- Are the report's load-bearing numbers identifiable?
- Is each load-bearing number distinguishable as observed metric, proxy, assumption, model output, or illustrative calculation?
- Are proxies prevented from masquerading as direct evidence?
- Are model outputs prevented from masquerading as observed facts?
- Where recommendation or ranking depends on scoring or estimation, are the roles of the inputs visible?
- Does uncertainty treatment match the role of the number?
- If assumptions changed, would the conclusion visibly change? If yes, are those assumptions labeled clearly enough?

## Assumption chain checks

- Each high-sensitivity assumption has a complete assumption chain (supporting evidence, dependency conditions, sensitivity, failure signals, confidence). If the chain cannot be fully populated, one of the following must apply: (a) fill the chain from available evidence, (b) downgrade the assumption's sensitivity classification, or (c) restructure the analysis to reduce dependence on that assumption. Do not leave the chain incomplete without an explicit remediation decision.
- The dependency conditions in each assumption chain are reasonable for the context.
- The failure signals in each assumption chain are observable and actionable (not generic disclaimers).

## Route-specific checks

> **例外说明（所有路线）**：辅助性描述数字（如"约 5 年"、"数万用户"、"少量"、"~3-5 人"）不强制要求逐项标注角色标签。如果已标注角色标签（如 ASSUMPTION）则正常通过。此例外不适用于评分/排名表格中直接影响排序的 load-bearing 数字。"关键数字"定义参见 `references/quantitative-role-labeling.md` §What should be labeled（materially affect recommendation / ranking / shortlist / sequencing / timing / valuation / confidence）。

### Constrained Choice / Shortlist / Option Selection

- [BLOCKER] Key numbers in scoring/ranking systems (star ratings, weight scores, cost estimates, growth rates, plugin/ecosystem counts) must carry role labels (observed / proxy / assumption / model-output).
- [BLOCKER] If >3 critical scoring/ranking numbers lack role labels ("critical" per `references/quantitative-role-labeling.md` §What should be labeled) → hard-fail (see ROUTING-MATRIX.md §Constrained Choice hard-fail).
- [NON-BLOCKER] Composite score breakdown — which dimensions are observed vs. modeled — should be visible in the table or a note.

### Market Outlook / Industry Evolution

- [BLOCKER] Load-bearing numbers (market size, growth rates, scenario probabilities, adoption projections) must carry role labels (observed / estimate / scenario-assumption / model-output).
- [NON-BLOCKER] Scenario probabilities (e.g., "20-25%") should include estimation method or source basis, not bare qualitative judgment.
- [NON-BLOCKER] This route already has a "mixes observed facts with scenario assumptions" hard-fail (ROUTING-MATRIX.md §Market Outlook, enforced by `checklists/market-outlook-audit.md`). These role-label checks serve as defense-in-depth.

### Listed Company / Investment-style Research

- [NON-BLOCKER] Forward-looking numbers (industry forecasts, market-share probabilities, "提升 X%" claims) should carry source-role labels (analyst estimate / model-output / assumption / company-guidance).
- [NON-BLOCKER] Valuation multiples, PE historical midpoints, industry-average PE — if no explicit source role, at least distinguish observed (annual-report / filing) vs. inferred (calculation / estimate).
- [NON-BLOCKER] Input parameters in valuation sensitivity analysis should carry role labels.

### Startup / Private Company Evaluation

- [NON-BLOCKER] ARR/MRR source type must be explicit: company-reported / estimated / inferred (see `checklists/startup-company-report.md` §Funding and financials). This is complementary to the core role labels (observed / proxy / assumption / model-output) — use both.
- [NON-BLOCKER] Valuation multiples (e.g., PS 100x) require boundary conditions: private-company premium context and comparable-transaction range source role.
- [NON-BLOCKER] "预计 X" / "估测 Y" / "约 Z" claims must include method note or source role — bare hedge wording insufficient.

### Market Entry / Regional Expansion

- [NON-BLOCKER] Scoring/weighting matrices used for country or site ranking must label per-score role (observed / proxy / model-output).
- [NON-BLOCKER] Load-bearing numbers (market size, payback period, localization cost, sequencing thresholds) must carry role labels (observed / estimate / assumption / model-output).
- [NON-BLOCKER] When a secondary Constrained Choice route is declared, the CC route's quantitative role BLOCKER checks apply (see `ROUTING-MATRIX.md` §Secondary route hard-fail requirement).

## Sensitivity analysis checks

- [BLOCKER] Has each load-bearing numerical assumption been classified by sensitivity level (low / medium / high) per `references/quantitative-role-labeling.md`?
- [BLOCKER] High-sensitivity assumptions have a visible sensitivity table with at least ±20% and one wider amplitude (±50% or extreme scenario).
- [NON-BLOCKER] If the report includes scenario analysis (optimistic / base / pessimistic), verify that key assumptions also have independent sensitivity tables. Multi-variable scenario changes do not satisfy the sensitivity table requirement — scenario analysis and sensitivity analysis are complementary, not substitutes.
- [NON-BLOCKER] Medium-sensitivity assumptions have at least the tipping point documented (the deviation at which the conclusion would change direction).
- [NON-BLOCKER] The report states which assumptions are most load-bearing and what would change the conclusion.

## Route-specific checks

### Constrained Choice / Shortlist / Option Selection

- [ ] [BLOCKER] 评分/排名系统中的关键数字（星级评分、权重分数、成本估算、增长率）必须标注角色标签（observed/proxy/assumption/model-output）。
- [ ] [BLOCKER] 若 >3 个关键评分/排名数缺少角色标签 → hard-fail（参见 ROUTING-MATRIX.md Constrained Choice hard-fail）。
- [ ] [NON-BLOCKER] 聚合评分（composite score）的来源——哪些维度是观察值、哪些是模型输出——在表格或附注中可见。

### Market Outlook / Industry Evolution

- [ ] 市场规模、增长率、情景概率等 load-bearing 数字必须标注角色标签（observed / estimate / scenario-assumption / model-output）。
- [ ] 情景概率（如"20-25%"）需说明估计方法或来源依据，不能仅靠定性判断。
- [ ] 该路线已有 "mixes observed facts with scenario assumptions" hard-fail（ROUTING-MATRIX.md），本 check 作为 defense-in-depth。

### Listed Company / Investment-style Research

- [ ] 行业预测、市场份额概率、"提升 X%"等前瞻性数字需注明来源角色（分析师 estimate / 模型 output / 假设 assumption）。
- [ ] 估值倍数、PE 历史中枢、行业平均 PE 等如无明确来源角色标注，至少要区分 observed（年报/披露）vs inferred（推算/估计）。
- [ ] [NON-BLOCKER] 估值敏感性分析中的输入参数需标注角色。

### Startup / Private Company Evaluation

- [ ] ARR/MRR 来源类型必须明确：company-reported / estimated / inferred（参见 `checklists/startup-company-report.md` §Funding and financials）。
- [ ] 估值倍数（如 PS 100x）需说明估值边界条件（private company premium / 可比交易区间来源角色）。
- [ ] "预计 X"、"估测 Y"、"约 Z"等用语需附方法说明或来源角色，不得单独以模糊表述出现。

## Hard fail signs

- Numerical precision exceeds source certainty.
- A model output is written as a fact.
- An unlabeled assumption carries the recommendation.
- Numbers from different epistemic roles are mixed without distinction.
