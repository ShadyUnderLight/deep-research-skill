# Eval: TSMC Listed-Company — Time-Horizon Valuation Stratification Case

## Goal

Test whether a Listed-Company / Investment-Style report that answers "是否充分反映长期增长" produces a **time-stratified valuation judgment** rather than a flat "under-valued / fairly-valued / over-valued" conclusion.

The reference failure is the existing TSMC report (`tmp/tsmc-valuation-report.md`), which has a judgment-first opening, complete research-anchor block, and clear bottom-line — but the conclusion is a single-directional "当前估值部分反映了 AI 增长，但未充分反映长期价值" without distinguishing:

- which growth horizon (3yr / 5yr / 10yr) the market has already priced
- where optionality remains unpriced
- whether the action implication (buy/hold/wait) differs by investment horizon

This eval tests that the new template rules (time-horizon stratification + four-variable decomposition) produce outputs that avoid this failure mode.

## Prompt

Assess whether TSMC's current valuation reflects long-term AI semiconductor growth. Produce a structured listed-company investment memo that:

- provides a judgment-first opening with clear thesis
- includes a research-anchor block (FY, latest quarter, market snapshot date, management context)
- provides a current financial/market snapshot with clearly dated and cited key numbers
- uses `[Sxx]` or equivalent claim-level inline citations for every load-bearing claim
- includes a complete 7-column Source Register
- **when answering "是否充分反映长期增长", stratifies the valuation judgment by time horizon: short-to-medium term (1-3yr / 3-5yr) priced-in status vs long-term (5-10yr) optionality**
- **makes investment action implications horizon-consistent: does not write "长期可持有" as "当前明显低估"**
- **labels the 3-5 valuation-driving variables explicitly (demand TAM, share capture, margin/FCF conversion, valuation pull-ahead)**

## What this eval is testing

- whether the report produces a time-stratified valuation judgment (short-to-medium vs long-term) instead of a flat directional conclusion
- whether investment action implications are tied to specific time horizons rather than being generic
- whether the 3-5 valuation-driving variables are explicitly identified and used to structure the report sections
- whether the opening thesis reflects the stratification before entering detailed analysis
- whether absence of time-horizon stratification is treated as a conditional-pass ceiling (not full pass)

## Pass criteria

A passing answer should:

1. **Stratify valuation judgment by time horizon in the opening.**
   - short-to-medium term (1-3yr / 3-5yr): states whether growth is already priced in, with evidence (PE/Forward PE/consensus EPS)
   - long term (5-10yr): states whether remaining optionality exists, with evidence (TAM, moat, capital回收, competition)
   - action implication is horizon-consistent: e.g., "可持有" not written as "当前明显低估"; if long-term upside exists but short-term is fully priced, the action reflects that tension

2. **Identify 3-5 valuation-driving variables explicitly.**
   - at minimum covers: demand TAM / share capture / margin & FCF conversion / valuation pull-ahead
   - these variables visibly drive report section ordering (not scattered across financial, market, risk sections)
   - each variable has a label: confirmed / inferred / unknown

3. **Separate support / weakening / unresolved for each time horizon.**
   - what supports the short-to-medium thesis
   - what weakens the long-term thesis
   - what remains unresolved for each horizon

4. **Make the investment action horizon-consistent.**
   - "新增买入" vs "继续持有" vs "等待回撤" are tied to specific time horizons
   - does not collapse "长期可持有" into "当前明显低估"

5. **Maintain all existing listed-company discipline.**
   - research-anchor block present and complete
   - market snapshot table present and complete
   - body-level `[Sxx]` traceability
   - 7-column Source Register
   - evidence labels match source strength

## Failure signs

Mark this eval as failed if the answer does any of the following:

- valuation judgment is a single directional statement (e.g., "未充分反映" / "合理偏低") without time-horizon stratification — this is the primary hard-fail
- opening thesis does not distinguish short-to-medium term from long-term pricing status
- action implication is "当前明显低估" when the evidence only supports "长期可持有"
- 3-5 valuation-driving variables are not identified or are scattered without driving report structure
- evidence supports "long-term optionality" but the conclusion reads as "unambiguously cheap"
- the report has the same structure as the existing TSMC report (`tmp/tsmc-valuation-report.md`) with only cosmetic changes

## Why this eval matters

The existing TSMC report demonstrated a clear failure mode: a well-structured listed-company memo with judgment-first opening, complete research anchor, market snapshot, valuation scenarios, and bull/bear framework — but the core valuation judgment was a single directional conclusion ("未充分反映"). This is the gap that GPT's deep research version does not have.

Issue #277 proposes template rules to close this gap. This eval validates that those rules actually produce the behavioral change. Without this eval, the new template rules could be added but never verified to actually fire during report generation.

This eval is distinct from related listed-company cases such as `evals/cases/reporting-period-and-ttm-confusion-case.md`, which focuses on reporting-period and snapshot discipline. This case focuses on valuation judgment structure.

## Current rule verdict

- Without new rules (status quo): existing TSMC report passes listed-company checklist but produces a flat valuation judgment — this eval would FAIL.
- With new rules (after issue #277): a compliant report should PASS or CONDITIONAL-PASS this eval.

## Relationship to new rules

This eval directly tests the behavioral impact of three new rules proposed in issue #277:

1. `references/report-template.md` §Time-horizon valuation stratification — forces opening to stratify by time horizon
2. `references/report-template.md` §Four-variable decomposition — forces identification of 3-5 valuation-driving variables
3. `checklists/listed-company-report.md` — new checklist items for horizon consistency

## Related evals

- `evals/cases/reporting-period-and-ttm-confusion-case.md` — listed-company reporting-period discipline
- `evals/cases/pop-mart-listed-company-traceability-hard-fail-case.md` — same route, traceability focus
- `evals/cases/consensus-and-forward-pe-misuse-case.md` — same route, forward-PE discipline
- `evals/comparative-distillation/byd-gpt-vs-minimax-comparative-distillation.md` — comparative distillation showing GPT's stronger calibration, which this rule closes

## Reviewer checklist

- Is the valuation judgment stratified by time horizon (short-to-medium vs long-term)?
- Are investment action implications horizon-consistent?
- Are 3-5 valuation-driving variables explicitly identified and driving report structure?
- Does the opening thesis reflect the stratification before detailed analysis?
- If the report has a single-directional conclusion without stratification, is it treated as conditional pass only?

## Suggested scoring

- **Pass**: time-horizon stratification present in opening, action implications horizon-consistent, 3-5 variables identified and driving structure, all existing listed-company discipline maintained
- **Conditional pass**: listed-company structure strong, valuation scenarios present, but time-horizon stratification is partial (e.g., mentioned in body but not in opening) or action implications are partially horizon-consistent — no hard-fail violation
- **Fail**: single-directional valuation judgment without time-horizon stratification (primary hard-fail), or action implications contradict the evidence (says "明显低估" when evidence only supports "长期可持有"), or 3-5 variables not identified
