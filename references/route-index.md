# Route Index (Compact)

Quick route selection before deep collection. The trigger/read/audit table below is generated from `schemas/route-manifest.json`; the boundary table and routing guidance remain hand-maintained. Each route has a generated card in `references/routes/`. Specialized routes use `ROUTING-MATRIX.md` for their full contract; `shared-workflow` uses `SKILL.md#routing-rule` because it has no specialized matrix section.

**How to use:** (1) Scan the trigger column. (2) Check the boundary table to confirm the route is correct (or switch to a better fit). (3) Open the route's **Card** for its primary reads, required disciplines, audits and artifact contract. (4) Apply the listed audits before delivery. If no specialized route matches, use `shared-workflow`.

## Trigger table

<!-- BEGIN GENERATED ROUTE INDEX -->
<!-- Source: schemas/route-manifest.json; version: 2 -->
| Route ID | Trigger keywords | Reads | Audits | Card |
|----------|-----------------|-------|--------|------|
| `provider-selection` | Select among model/API suppliers, vendors or platforms and justify why one wins under explicit constraints. | `references/option-selection-and-shortlist-discipline.md`, `references/source-traceability-and-claim-citation.md`, `references/decision-report-template.md`, `references/report-template.md` | `option-selection-final-audit`, `source-traceability`, `final-audit` | [`provider-selection`](routes/provider-selection.md) |
| `market-entry` | Decide whether to enter a market, where to enter first, when, or how to sequence entry under constrained budget. | `references/option-selection-and-shortlist-discipline.md`, `references/decision-report-template.md`, `references/source-traceability-and-claim-citation.md`, `references/templates/market-entry-report.md`, `references/report-template.md` | `option-selection-final-audit`, `source-traceability`, `final-audit` | [`market-entry`](routes/market-entry.md) |
| `market-outlook` | Explain how a market will evolve over the next 6-24 months: direction, adoption trajectory, scenario memo. | `references/market-outlook-and-scenario-discipline.md`, `references/forward-looking-discipline.md`, `references/decision-report-template.md`, `references/source-traceability-and-claim-citation.md`, `references/templates/market-outlook-report.md`, `references/report-template.md` | `market-outlook-audit`, `forward-looking-claims`, `source-traceability`, `final-audit` | [`market-outlook`](routes/market-outlook.md) |
| `competitive-positioning` | Judge whether an entity belongs in a top group, with dimension-level judgment before any overall label. | `references/ranking-and-current-claims-discipline.md`, `references/source-traceability-and-claim-citation.md`, `references/decision-report-template.md` | `source-traceability`, `final-audit` | [`competitive-positioning`](routes/competitive-positioning.md) |
| `constrained-choice` | Choose among defined options using a visible comparison unit, shortlist logic, and ranking-change conditions; includes outcome-ranking / probability-distribution tasks. | `references/option-selection-and-shortlist-discipline.md`, `references/decision-report-template.md`, `references/report-template.md` | `option-selection-final-audit`, `final-audit` | [`constrained-choice`](routes/constrained-choice.md) |
| `regulatory-analysis` | Assess the regulatory environment, policy risk, or compliance impact on a business or industry. | `references/current-state-verification.md`, `references/forward-looking-discipline.md`, `references/source-quality.md`, `references/data-conflict-resolution.md`, `references/rule-system-and-mechanism-add-on.md` | `regulatory-analysis-audit`, `source-traceability`, `final-audit` | [`regulatory-analysis`](routes/regulatory-analysis.md) |
| `equipment-selection` | Produce a purchase-ready or build-ready hardware/device recommendation under visible budget, maintenance, noise, power, storage, networking, or expansion constraints. | `references/decision-report-template.md`, `references/option-selection-and-shortlist-discipline.md`, `references/source-traceability-and-claim-citation.md` | `option-selection-final-audit`, `final-audit` | [`equipment-selection`](routes/equipment-selection.md) |
| `technical-deep-dive` | Technical judgment: understanding principles, evaluating feasibility, comparing architectures, assessing technology maturity or roadmaps. | `references/technical-analysis-discipline.md`, `references/source-traceability-and-claim-citation.md`, `references/forward-looking-discipline.md`, `references/templates/technical-deep-dive-report.md` | `technical-analysis-audit`, `source-traceability`, `final-audit` | [`technical-deep-dive`](routes/technical-deep-dive.md) |
| `listed-company` | Listed-company, valuation, public-market, or investment-style memo judgment burden. | `references/finance-date-discipline.md`, `references/valuation-methodology.md`, `references/analyst-consensus-handling.md`, `references/reporting-period-handling.md`, `references/forward-looking-discipline.md`, `references/market-sizing-and-share-discipline.md`, `references/source-traceability-and-claim-citation.md`, `references/moat-monopoly-screening.md`, `references/templates/listed-company-report.md`, `examples/listed-company-judgment-memo-example.md`, `examples/china-shenhua-reference-grade-rewrite-skeleton.md` | `listed-company-report`, `source-traceability`, `final-audit` | [`listed-company`](routes/listed-company.md) |
| `startup-evaluation` | Evaluate a non-public company's current state, prospects, or investment value: due diligence, PMF, funding round, early-stage assessment. | `references/startup-evaluation-discipline.md`, `references/source-quality.md`, `references/source-traceability-and-claim-citation.md`, `references/forward-looking-discipline.md` | `startup-company-report`, `source-traceability`, `final-audit` | [`startup-evaluation`](routes/startup-evaluation.md) |
| `academic-review` | Understand academic evidence, evaluate research quality, or survey field progress through peer-reviewed literature. | `references/academic-evidence-hierarchy.md`, `references/source-traceability-and-claim-citation.md`, `references/counter-evidence.md`, `references/templates/academic-review-report.md` | `academic-analysis-audit`, `source-traceability`, `final-audit` | [`academic-review`](routes/academic-review.md) |
| `shared-workflow` | No specialized route fits and the task has no option universe, ranking, probability, or selection burden; lightweight fact query. | `references/route-activation-and-preflight.md`, `references/source-traceability-and-claim-citation.md` | `workflow-spine-audit`, `final-audit` | [`shared-workflow`](routes/shared-workflow.md) |
<!-- END GENERATED ROUTE INDEX -->

## Route boundary reference

Before committing to a route, check this table. If the task matches a "Do NOT use" condition, switch routes. If it partially overlaps "Often confused with", read the boundary clauses in the route's card (`references/routes/<id>.md`) or `references/route-activation-and-preflight.md` for boundary resolution.

| Route ID | Do NOT use when | Often confused with | Key artifact must-haves |
|----------|----------------|---------------------|-------------------------|
| `listed-company` | task is definition-sensitive positioning, not investment-style | `competitive-positioning` | research-anchor block, judgment-first opening, market snapshot |
| `startup-evaluation` | company is publicly listed and trading | `listed-company` | source reliability levels, PMF signals, labeled financial data |
| `market-entry` | task is generic market overview or simple option comparison | `constrained-choice` | go/not-now/pilot label, hard gates, sequencing, regional hub vs beachhead |
| `regulatory-analysis` | regulation is only background context | `listed-company`, `market-outlook` | current reg snapshot, pending legislation, enforcement reality, scenarios |
| `provider-selection` | task mainly describes market direction without real selection burden; hardware/physical device procurement | `market-outlook`, `equipment-selection` | decision criteria, ranked shortlist, why top wins, why runner-up credible |
| `competitive-positioning` | task is investment-style analysis, valuation reasoning, or broad company profiling | `listed-company` | scope, metric, timeframe, dimension-level conclusions, explicit overall-label gate |
| `technical-deep-dive` | task is about selecting a product/vendor or market evolution | `equipment-selection`, `constrained-choice`, `market-outlook` | technical judgment (not survey), comparison dimensions, current-state verification |
| `equipment-selection` | task mainly explains hardware categories or compares benchmarks abstractly | `constrained-choice`, `provider-selection` | real purchase decision, dominant constraints, stack recommendation, budget assumptions |
| `market-outlook` | task has ranking, selection, or winner-prediction burden among defined options | `constrained-choice` | base case + alternative scenarios (≥2), 3+ stakeholder types, monitoring signals |
| `constrained-choice` | real task is market-entry gating, expansion sequencing, or broad market scanning | `market-entry` | decision architecture, shortlist logic, comparison unit, ranking-reversal conditions |
| `academic-review` | task can be answered by technical deep-dive; question is about how tech works, not research evidence | `technical-deep-dive` | peer-review status labels, search strategy, evidence hierarchy (dual-dim), publication bias |
| `shared-workflow` | task fits a specialized route but it's avoided for convenience | any specialized route | workflow spine audit, final audit; no route-specific artifact contract |

## Route preflight (before committing)

Read `references/route-activation-and-preflight.md` and complete:
- "Do not use" / "Often confused with" clause check (see boundary table above)
- secondary-route hard-fail verification
- route declaration scale check
- execution contract formation

## Routing tie-breaker (Step 4 only)

When multiple routes could apply, first use the **Route selection decision tree** in `ROUTING-MATRIX.md` (Steps 1-3: action burden → weight-bearing object → boundary hard-fails). This fixed priority list is the **Step 4 tie-breaker** — use it only after Steps 1-3 are exhausted:

`listed-company` > `startup-evaluation` > `market-entry` > `regulatory-analysis` > `provider-selection` > `competitive-positioning` > `technical-deep-dive` > `equipment-selection` > `market-outlook` > `constrained-choice` > `academic-review`.

For full route contracts (hard-fail conditions, micro-audit focus, entity type definitions), read `ROUTING-MATRIX.md`.
