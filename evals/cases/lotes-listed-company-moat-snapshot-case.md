# Eval: 嘉澤 Listed-Company Moat Boundary + Snapshot Case

## Goal

Test whether a Listed-Company / Investment-Style report with strong business analysis, structured bull/bear, and complete financials can still achieve only Conditional Pass when market snapshot is incomplete (PS, 52-week range missing), moat boundary discipline is not clean, valuation lacks recomputable method, and evidence label calibration over-weights secondary sources as `[CONF]`.

## Real case pattern

A user-provided 嘉澤端子 (3533.TW) deep research report dated **2026-06-04** demonstrates this pattern.

**What was done well:**
- ✅ Complete research anchor block (FY2025, 2026Q1, 2026-06-03 snapshot, mgmt)
- ✅ Strong business analysis with product/customer/application coverage
- ✅ Structured bull/bear with uncertainty register
- ✅ Body-level `[Sxx]` citations present (not just bibliography)
- ✅ Financial data complete (revenue, gross margin, EPS, segment breakdown, cash/debt)
- ✅ Signal dashboard with positive/negative signals separated
- ✅ Counter-evidence present (margin, valuation, AI purity, FX risk)
- ✅ Judgment-first opening with clear thesis

**Core issues (conditional pass level):**
- ❌ **Market snapshot incomplete** — PS and 52-week high/low missing
- ❌ **Moat boundary discipline not clean** — strong moat language ("双寡头", "极高转换成本", "全球第二") without explicit boundary between legal exclusivity / resource control / competitive moat / listed-proxy scarcity; no downgrade notation where evidence insufficient
- ❌ **Evidence label over-confidence** — secondary media/analyst sources supporting market position, customer growth, target prices labeled as `[CONF]` where `[INFER]` or source role label would be appropriate
- ❌ **Valuation not recomputable** — PE/PB comparison listed but no scenario framework, multiple range, comparable selection logic, or reversal conditions
- ❌ **No explicit action tier** — final judgment lacks clear "buy / hold / wait for Q2 / avoid" action level

## Scoring

- **Full Pass**: complete snapshot + clean moat boundary + recomputable valuation + honest labels
- **Conditional Pass**: strong business analysis but moat + snapshot + valuation gaps (this case's level)
- **Fail**: hard-fail triggered

## Related evals

- `evals/cases/emc-listed-company-strong-claims-moat-case.md` — companion: strong claims + moat discipline
- `evals/cases/marvell-listed-company-snapshot-traceability-case.md` — companion: snapshot incomplete
