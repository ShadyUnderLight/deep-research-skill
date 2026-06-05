# Eval: AI Coding Agent Market Outlook Probability Precision Case

## Goal

Test whether a Market Outlook / Industry Evolution report with strong scenario structure, stakeholder coverage, and route audit status visibility can still achieve only Conditional Pass when scenario probability weights lack calibration method, sensitivity analysis is absent, and a single inferred synthesis source (S27) bears excessive load-bearing claims.

## Real case pattern

A user-provided report "AI Coding Agent 市场未来 18 个月演化" dated **2026-06-04** demonstrates this pattern.

**What was done well:**
- ✅ Market Outlook route correctly selected with 3 complete scenarios
- ✅ Current market snapshot (§35-73) with leading products, pricing, market size
- ✅ 4 stakeholder types (CTO, indie dev, VC, legal/policy) with dedicated subsections
- ✅ Drivers/blockers separated with specific mechanisms (D1-D4, B1-B4)
- ✅ Reversal signals (§229-241) with explicit monitoring conditions
- ✅ Route audit status visible (§259-268) with required audits listed
- ✅ Body-level `[S]` citations present (not just bibliography)
- ✅ Strong bottom line actionable (§245-255)

**Core issues (conditional pass level):**
- ❌ **Scenario probability precision without calibration** — `~25% / ~55% / ~20%` given without explaining how probabilities were derived; no sensitivity analysis or method note
- ❌ **S27 inferred synthesis over-burdened** — single `Research synthesis — inferred` entry supports multiple technical/benchmark key claims without decomposing into traceable sub-sources
- ❌ **Bottom-line judgment labels incomplete** — §245-255 bottom line claims lack per-item evidence labels ([确认事实]/[推断]/[未知]) despite report claiming "all key judgments labeled"
- ❌ **Sensitivity analysis absent** — adoption rate, ARPU, MCP security maturity, copyright events have no ±20%/extreme scenario impact table

## Scoring

- **Full Pass**: probability calibration method + sensitivity analysis + complete label coverage
- **Conditional Pass**: strong structure but probability precision + missing sensitivity + S27 burden (this case's level)
- **Fail**: hard-fail triggered

## Related evals

- `evals/cases/ai-cost-control-market-outlook-full-pass-benchmark.md` — Market Outlook Full Pass benchmark
- `evals/cases/app-vs-agent-market-outlook-register-scenario-case.md` — companion: scenario quantification gaps
