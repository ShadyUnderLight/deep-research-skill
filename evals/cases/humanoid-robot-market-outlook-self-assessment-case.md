# Eval: Humanoid Robot Market Outlook Self-Assessment Overconfidence Case

## Goal

Test whether a Market Outlook / Industry Evolution report with strong structural execution (three scenarios, stakeholder coverage, reversal signals) can still achieve only Conditional Pass when source traceability self-assessment is overconfident (claims passed but body-level traceability incomplete), scenario probabilities lack calibration method, and forward-looking claims missing source roles.

## Real case pattern

A user-provided report "人形机器人产业链未来 24 个月商业化路径" dated **2026-06-04** demonstrates this pattern.

**What was done well:**
- ✅ Market Outlook route correctly selected with clear commercialization ladder judgment
- ✅ 3 structured scenarios (optimistic/base/pessimistic) with common quantitative axis (global deployment units)
- ✅ 4 stakeholder types (investors, industrial buyers, developers, policymakers)
- ✅ Drivers/blockers separated with specific mechanisms
- ✅ Reversal signals with monitoring conditions (§224-242)
- ✅ Counter-evidence present (§246-279) with per-scenario counter-arguments
- ✅ Route audit status self-reported (§341-350)
- ✅ Body-level `[Sxx]` citations present (partial)
- ✅ Bottom line actionable with per-stakeholder recommendations (§285-303)

**Core issues (conditional pass level):**
- ❌ **Source traceability self-assessment overconfident** — §341-350 claims ✅ passed, but body traceability incomplete; source list (§311-337) lacks DOI/URL, Reliability, Claims Supported columns
- ❌ **Scenario probability precision without calibration** — 20/55/25% given without method explanation (same pattern as AI Coding Agent case)
- ❌ **Forward-looking claims missing source roles** — §127 "固态电池预计", §153 "ISO 预计", §147 "2028年后压力将显著显现" lack named source attribution
- ❌ **Evidence label coverage incomplete** — drivers/blockers analysis, stakeholder recommendations, bottom line conclusions missing per-item `[确认事实]/[推断]/[未知]` labels

## Scoring

- **Full Pass**: complete traceability + calibrated probabilities + complete label coverage
- **Conditional Pass**: strong structure but self-assessment overconfidence + probability gaps (this case's level)
- **Fail**: hard-fail triggered

## Related evals

- `evals/cases/ai-coding-agent-market-outlook-probability-case.md` — companion: same pattern (probability precision + source traceability self-assessment)
