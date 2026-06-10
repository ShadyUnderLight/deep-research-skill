# Eval: AI 视频生成 Market Outlook — Label Overuse + Probability Precision Gap Case (Round 7)

## Goal

Test whether a market-outlook / industry-evolution report with strong route-contract execution (drivers/blockers, three scenarios, stakeholder coverage, monitoring signals) can still receive a **Fail** rating when:

- **`[CONF]` label overuse** — secondary media/analyst/market-report sources labeled as confirmed facts; vendor claims lack "厂商自述" caveat
- **forward-looking claims lack source role** — probability weights (`~60%`, `20-25%`, `15-20%`) and market size estimates (`$17-20B by 2028`) without calibration method or named source
- **process-integrity hard-fail** — audit status claims `Forward-looking ✅`, `Source Traceability ✅`, `Final Audit ✅` but body evidence contradicts
- **internal inconsistency** — Sora cost `$1500万/day` (exec summary) vs `$100万/day` (body) without reconciliation
- **external verification failure** — Sora discontinuation date wrong (report says March 2026, actual web/app April 2026, API September 2026)
- **vendor claims without caveat labels** — Runway revenue "超 $3 亿" without independent verification note
- **monitoring signals not actionable** — signal categories are named, but threshold, cadence, source, and trigger-to-action mapping are not sufficient for a reusable monitoring dashboard (#224)

This is the **seventh Round 7 case**, adding the **market-outlook route** with **label overuse** as the primary failure pattern.

## Real case pattern

A user-provided report "AI 视频生成市场未来 24 个月演化展望" dated **2026-06-10** demonstrates this pattern. Inferred route: `market-outlook / industry-evolution`.

**What was done well:**
- ✅ Opening carries core judgment — base case scenario, probability, market size, core variables within first 10 lines
- ✅ Current market snapshot: product matrix, pricing, adoption landscape
- ✅ Drivers and blockers separated with clear structure
- ✅ Three scenarios (optimistic/base/pessimistic) sharing market size as quantitative axis
- ✅ Stakeholder implications ≥3 types: creators, enterprise buyers, investors/policymakers
- ✅ Monitoring variables named: inference cost, copyright rulings, user growth, capital markets, tech rankings
- ✅ Counter-evidence present: pessimistic scenario, copyright crisis, cost bottleneck
- ✅ Body has `[Sxx]` traceable citations (incomplete but present)
- ✅ Uncertainty register with U01-U05 items

**Core issues (Fail — hard-fail triggered):**
- ❌ **`[CONF]` label overuse** — secondary media/analyst/market-report sources (marketing team adoption rates, enterprise adoption rates, North America market share) labeled as `[CONF]` without source-role downgrade. Vendor claims (Runway revenue "$3亿+") lack `(厂商自述，非独立验证)` caveat. Triggers Round 5 #191 calibration rule.
- ❌ **Forward-looking claims lack source role** — probability weights `~60%`, `20-25%`, `15-20%` assigned without calibration method, comparable basis, or named source. Market size "$17-20B by 2028" stated without attribution to specific forecast model or institution. Internal inconsistency: Sora cost `$1500万/day` (exec summary) vs `$100万/day` (body) unreconciled.
- ❌ **Process-integrity hard-fail** — audit status claims `Forward-looking ✅`, `Source Traceability ✅`, `Final Audit ✅`, but label overuse, forward-looking attribution gaps, and internal inconsistency all present.
- ❌ **External verification failure** — Sora discontinuation date: report states "2026 年 3 月关停", but OpenAI Help Center shows web/app discontinued April 2026 and API September 2026. Report error not caught by current-state verification.
- ❌ **Probability precision false** — `~60%`, `20-25%`, `15-20%` imply precision without documented derivation. Per forward-looking discipline, probabilities without calibration basis should use directional ranges.
- ❌ **Monitoring signals not actionable** — the report names plausible things to watch, but does not turn at least 3 of them into a dashboard with threshold, review cadence, data source, and trigger-to-action mapping (#224).

## Why this case exists

Seventh Round 7 case. First market-outlook case in this round. The failure triad is confirmed again — the pattern is route-independent. New dimensions added: external verification failure (Sora date) and internal inconsistency (cost figures), both of which are delivery-cleanliness issues.

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

## Related evals

- `evals/cases/ai-agent-market-outlook-stakeholder-and-route-boundary-case.md` — Round 6: market-outlook stakeholder + route boundary
- `evals/cases/cross-border-ecommerce-market-outlook-self-assessment-case.md` — Round 5: market-outlook self-assessment overconfidence
- `evals/cases/us-chip-export-regulatory-evidence-label-case.md` — Round 5: `[CONF]` label overuse
