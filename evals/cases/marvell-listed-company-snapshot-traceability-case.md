# Eval: Marvell Listed-Company Snapshot + Traceability Case

## Goal

Test whether a Listed-Company / Investment-Style report with strong judgment-first opening and structured bull/bear framework can still achieve only Conditional Pass when claim-level source traceability is absent, market snapshot is incomplete (PB, 52-week range missing), and valuation scenario matrix lacks recomputable parameters.

## Real case pattern

A user-provided Marvell Technology (MRVL) deep research report dated **2026-06-04** demonstrates this pattern.

**What was done well:**
- ✅ Judgment-first opening with rerating thesis, valuation concern, customer churn uncertainty
- ✅ Complete research anchor block (FY2026, Q1 FY2027, 2026-06-03 snapshot, CEO state)
- ✅ Structured bull/bear split with uncertainty register
- ✅ Scenario matrix with target price ranges
- ✅ Counter-evidence present (bear case not strawman)
- ✅ Turn-signal triggers (转多/转空 signals)
- ✅ Route activation audit self-reported (§298-307)

**Core issues (conditional pass level):**
- ❌ **Claim-level source traceability absent** — body has no `[Sxx]` inline citations; source register exists but claims not traceable from body
- ❌ **Market snapshot incomplete** — PB, 52-week high/low, forward PE, EV/EBITDA missing (listed-company hard-fail borderline)
- ❌ **Valuation scenario opacity** — target price ranges without recomputable EPS/multiple assumptions or comparable company logic
- ⚠️ **Evidence label over-confidence** — JPM X, PatSnap, market growth reports labeled as `[确认事实]` where `[推断]` or source role label would be appropriate

## Scoring

- **Full Pass**: inline citations present + complete snapshot + transparent valuation
- **Conditional Pass**: strong judgment framework but traceability + snapshot + valuation gaps (this case's level)
- **Fail**: hard-fail triggered

## Related evals

- `evals/cases/tencent-listed-company-label-consistency-case.md` — companion: label consistency gap
- `evals/cases/meituan-listed-company-traceability-gap-case.md` — companion: traceability gap
