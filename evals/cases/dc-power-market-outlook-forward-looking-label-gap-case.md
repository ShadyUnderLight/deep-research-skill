# Eval: 数据中心电力瓶颈 Market Outlook — Forward-Looking Label + Traceability Gap Case (Round 7)

## Goal

Test whether a market-outlook / industry-evolution report with strong scenario analysis, stakeholder coverage, and clear bottom line can still receive a **Fail** rating when:

- **forward-looking claims labeled as `[确认]`** — GPT-5 power estimate, 76% adoption forecast, 16GW capacity prediction all labeled as confirmed facts instead of estimate/assumption
- **body-level source traceability absent** — no `[Sxx]` inline citations; Source Register only 5 columns, missing DOI/URL and Claims Supported
- **process-integrity hard-fail** — audit status claims all `✅ 已通过` but source traceability, forward-looking label, and quantitative role are all noncompliant
- **probability weights without method** — "20%→30%""20%→15%" assigned without estimation basis or named source
- **monitoring signals not actionable** — more like a reversal-condition list than a measurable dashboard with thresholds, review cadence, sources, and trigger-to-action mapping (#224)

This is the **ninth Round 7 case**.

## Real case pattern

A user-provided report "全球数据中心电力瓶颈对 AI 基础设施产业链影响深度研究报告" dated **2026-06-10** demonstrates this pattern. Inferred route: `market-outlook / industry-evolution`.

**What was done well:**
- ✅ Opening carries core judgment — "电力瓶颈取代芯片供应" as binding constraint at line 9
- ✅ Current market snapshot: global power consumption, regional bottlenecks, policy constraints
- ✅ Drivers and blockers clearly separated
- ✅ Three scenarios (base/optimistic/pessimistic) sharing DC power consumption as quantitative axis
- ✅ Stakeholder implications ≥6 types: cloud, chip, DC operators, power equipment, liquid cooling, policymakers
- ✅ Counter-evidence present with 3 structured counter-arguments
- ✅ Uncertainty register explicit
- ✅ Decision usefulness: actionable for AI companies, DC operators, investors

**Core issues (Fail — hard-fail triggered):**
- ❌ **Forward-looking claims labeled as `[确认]`** — §73 "GPT-5 预计需 500+ GWh", §99 "预测到 2026 年底 76%", §111 "2026 年预计新增 16GW" all labeled as `[确认]` when evidence role is analyst estimate or scenario assumption. Triggers Round 5 #191 calibration rule: forecasts must carry estimate/assumption labels.
- ❌ **Body-level source traceability absent** — no `[Sxx]` or equivalent inline citations for load-bearing claims. Source Register (§356-379) has only 5 columns, missing DOI/URL and Claims Supported per Round 4 #182 template.
- ❌ **Process-integrity hard-fail** — §343-352 claims all `✅ 已通过`, but source traceability noncompliant, forward-looking labels misapplied, probability weights lack method.
- ❌ **Probability weights without method** — §270 "20%→30%", §281 "20%→15%" assigned without calibration basis, named source, or scenario context. Bare percentages without derivation.
- ❌ **Monitoring signals not actionable** — §334-339 lists "what would change the conclusion" items but lacks: measurable thresholds, observation frequency, data source, and trigger-to-action mapping. More of a reversal condition list than a monitoring dashboard (#224).

## Why this case exists

Ninth Round 7 case. The failure triad continues across 9 cases × 4 routes. This case adds a clear pattern: **forward-looking claims written as confirmed facts** — the most direct violation of the Round 5 #191 label calibration rule seen so far in this round.

## Round 7 accumulation

| # | Case | Route | Core failure |
|---|------|-------|-------------|
| 1 | Code review agent selection | provider-selection | Triad |
| 2 | Chinese LLM writing | provider-selection | Triad + aggregation |
| 3 | AI image generation | provider-selection | Triad + metadata drift |
| 4 | Tea brand overseas entry | market-entry | Triad |
| 5 | Short drama overseas entry | market-entry | Triad + hub-role + sensitivity |
| 6 | Industrial robot overseas entry | market-entry | Triad + compound criterion |
| 7 | AI video market outlook | market-outlook | Triad + label overuse + ext verification |
| 8 | Embodied AI market outlook | market-outlook | Triad + register inflation |
| 9 | DC power market outlook | market-outlook | Triad + forward-looking as `[确认]` |

## Related evals

- `evals/cases/ai-video-market-outlook-label-and-probability-gap-case.md` — Round 7: `[CONF]` overuse in market-outlook
- `evals/cases/us-chip-export-regulatory-evidence-label-case.md` — Round 5: Round 5 #191 calibration rule
