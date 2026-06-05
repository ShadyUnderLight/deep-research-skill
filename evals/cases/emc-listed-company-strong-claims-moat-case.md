# Eval: 台光電 Listed-Company Strong Claims + Moat Discipline Case

## Goal

Test whether a Listed-Company / Investment-Style report with complete anchor block, market snapshot, and structured bull/bear framework can achieve only Conditional Pass when strong exclusivity claims ("唯一/100%/>90%") lack evidence strength matching, source register has missing entries, valuation lacks recomputable method, and self-assessment overclaims pass status.

## Real case pattern

A user-provided 台光電 (2383.TW) deep research report dated **2026-06-04** demonstrates this pattern.

**What was done well:**
- ✅ Complete research anchor block (FY2025, 2026Q1, 2026-05-29 snapshot, mgmt)
- ✅ Complete market snapshot (price, market cap, TTM PE, 2025 PE, PB, 52-week range)
- ✅ Structured bull/bear with risk register (§323-331)
- ✅ Judgment-first opening with clear thesis
- ✅ Counter-evidence present (valuation, inventory depreciation, competition, AI capex slowdown)
- ✅ Monitoring signals (§269-279) actionable
- ✅ Route audit status self-reported (§335-342)

**Core issues (conditional pass level):**
- ❌ **[S23] missing from source register** — body §212 cites [S23] but register §299-321 has no S23 entry; delivery cleanliness error
- ❌ **Strong exclusivity claims evidence strength mismatch** — "唯一认证", "100%", ">90%" (§53, §92, §104, §112, §137, §197) carried by secondary media/analyst sources; listed-company hard-fail partially triggered
- ❌ **Evidence label over-confidence** — traditional media and Yahoo Finance labeled as `PRIMARY_FILING` or `[已确认事实]` where `[推断]` or source role downgrade would be appropriate
- ❌ **Valuation lacks recomputable method** — PE called expensive but no scenario valuation framework, comparable company logic, or reversal conditions
- ❌ **Self-assessment overconfident** — §335-342 claims all ✅ passed, but source-traceability (S23 missing + wrong source type labels) and monopoly/moat discipline not clean

## Scoring

- **Full Pass**: strong claims evidence-matched + complete source register + recomputable valuation
- **Conditional Pass**: strong structure but exclusivity claims + register gaps + self-assessment overconfidence (this case's level)
- **Fail**: hard-fail triggered

## Related evals

- `evals/cases/pop-mart-listed-company-traceability-hard-fail-case.md` — "唯一" absolute claim pattern
- `evals/cases/cross-border-ecommerce-market-outlook-self-assessment-case.md` — self-assessment overconfidence pattern
