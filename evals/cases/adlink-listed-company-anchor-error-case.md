# Eval: 凌华科技 Listed-Company Anchor Error + Label Inflation Case

## Goal

Test whether a Listed-Company report with complete market snapshot (PE/PB/PS/52-week), structured bull/bear, and clear bottom line can still achieve only Conditional Pass when the research anchor contains a verifiable factual error (April revenue growth rate wrong), evidence labels are inflated, and a clear financial unit error undermines delivery cleanliness.

## Real case pattern

A user-provided 凌华科技 (6166.TW) investment research memo dated **2026-06-05** demonstrates this pattern.

**What was done well:**
- ✅ Complete market snapshot (price, market cap, PE, PB, PS, 52-week range)
- ✅ Complete research anchor block with FY2025, latest month, mgmt state
- ✅ Structured bull/bear with uncertainty register
- ✅ Counter-evidence strong (valuation, scale, cash flow, customer concentration, China risk)
- ✅ Valuation scenarios with target price table (though method thin)
- ✅ Judgment-first opening with clear thesis
- ✅ Body-level `[S#]` citations present
- ✅ Bottom line actionable (hold, don't chase, wait for Q2/H2 validation)

**Core issues (conditional pass level):**
- ❌ **Research anchor factual error** — April 2026 monthly revenue growth misstated (37.6% claimed vs 63.16% single-month / 37.59% YTD cumulative per external verification). Undermines the listed-company route's most critical current-state anchor.
- ❌ **Financial unit error** — §313 "H1 营收 NT$56.02B" contradicts FY2025 full year NT$11.8B; obvious unit or decimal error
- ❌ **Evidence label inflation** — §116 "Edge Vision growth is 'direct evidence' of NVIDIA platform commercialization", §126 "较为罕见、议价能力" labeled as [确认事实] where [推断] or company-narrative label would be appropriate
- ❌ **Strong positioning claims lack sourcing** — "最高级伙伴", "第一梯队", "更早、更聚焦" need independent source or downgrade
- ❌ **Self-assessment overconfident** — §472-485 claims all ✅ passed despite anchor error and label inflation

## Scoring

- **Full Pass**: accurate anchor + honest labels + unit correctness
- **Conditional Pass**: strong structure but anchor error + label inflation + unit error (this case's level)
- **Fail**: hard-fail triggered

## Related evals

- `evals/cases/emc-listed-company-strong-claims-moat-case.md` — companion: label inflation + strong claims
- `evals/cases/advantech-listed-company-traceability-hard-fail-case.md` — companion: self-assessment overconfidence
