# Route Index (Compact)

Quick route selection before deep collection. Each route maps to a full contract in `ROUTING-MATRIX.md`.

**How to use:** (1) Scan the trigger column. (2) Check the boundary table to confirm the route is correct (or switch to a better fit). (3) Read the `reads` files. (4) Apply the listed audits before delivery. If no specialized route matches, use `shared-workflow`.

## Trigger table

| Route ID | Trigger keywords | Reads | Audits |
|----------|-----------------|-------|--------|
| `listed-company` | listed company, valuation, market cap, growth, investment memo | `references/finance-date-discipline.md`, `references/valuation-methodology.md` | `listed-company-report`, `source-traceability`, `final-audit` |
| `startup-evaluation` | private company, startup, PMF, funding round, founder evaluation | `references/startup-evaluation-discipline.md`, `references/source-quality.md` | `startup-company-report`, `source-traceability`, `final-audit` |
| `market-entry` | enter a market, country priority, expansion sequencing, go/no-go entry | `references/option-selection-and-shortlist-discipline.md`, `references/decision-report-template.md` | `option-selection-final-audit`, `source-traceability`, `final-audit` |
| `regulatory-analysis` | regulatory environment, policy risk, compliance impact, regulatory change | `references/current-state-verification.md`, `references/forward-looking-discipline.md` | `regulatory-analysis-audit`, `source-traceability`, `final-audit` |
| `provider-selection` | model/API supplier, vendor shortlist, platform choice, provider comparison | `references/option-selection-and-shortlist-discipline.md`, `references/source-traceability-and-claim-citation.md` | `option-selection-final-audit`, `source-traceability`, `final-audit` |
| `competitive-positioning` | first-tier, top-tier, global standing, prestige label, positioning | `references/ranking-and-current-claims-discipline.md`, `references/source-traceability-and-claim-citation.md` | `source-traceability`, `final-audit` |
| `technical-deep-dive` | technology principles, architecture comparison, patent portfolio, feasibility, roadmap | `references/technical-analysis-discipline.md`, `references/source-traceability-and-claim-citation.md` | `technical-analysis-audit`, `source-traceability`, `final-audit` |
| `equipment-selection` | hardware purchase, NAS, home server, homelab, build-ready stack, budget | `references/decision-report-template.md`, `references/option-selection-and-shortlist-discipline.md` | `option-selection-final-audit`, `final-audit` |
| `market-outlook` | market evolution, adoption trajectory, industry evolution, 6-24 month outlook | `references/market-outlook-and-scenario-discipline.md`, `references/forward-looking-discipline.md` | `market-outlook-audit`, `forward-looking-claims`, `source-traceability`, `final-audit` |
| `constrained-choice` | choose among options, ranking, shortlist, venue/vendor choice, sports prediction | `references/option-selection-and-shortlist-discipline.md`, `references/decision-report-template.md` | `option-selection-final-audit`, `final-audit` |
| `academic-review` | academic field progress, literature review, paper comparison, technology origin | `references/academic-evidence-hierarchy.md`, `references/source-traceability-and-claim-citation.md` | `academic-analysis-audit`, `source-traceability`, `final-audit` |
| `shared-workflow` | no specialized route fits; lightweight fact query without route/audit burden | (workflow spine — see `SKILL.md`) | `workflow-spine-audit`, `final-audit` |

## Route boundary reference

Before committing to a route, check this table. If the task matches a "Do NOT use" condition, switch routes. If it partially overlaps "Often confused with", read `references/route-activation-and-preflight.md` for boundary resolution.

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

## Routing priority

If multiple routes could apply: `listed-company` > `startup-evaluation` > `market-entry` > `regulatory-analysis` > `provider-selection` > `competitive-positioning` > `technical-deep-dive` > `equipment-selection` > `market-outlook` > `constrained-choice` > `academic-review`.

For full route contracts (hard-fail conditions, micro-audit focus, entity type definitions), read `ROUTING-MATRIX.md`.
