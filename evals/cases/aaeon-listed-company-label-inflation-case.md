# Eval: 研扬科技 Listed-Company Label Inflation Case

## Goal

Test whether a Listed-Company report with complete anchor block, structured bull/bear, and clear uncertainty register can still achieve only Conditional Pass when evidence labels are inflated (secondary/aggregator sources labeled as `[CONF]`), market snapshot lacks PB/PS, valuation lacks scenario framework, and uncertainty register does not narrow the final conclusion.

## Real case pattern

A user-provided 研扬科技 (6579.TW) deep research report dated **2026-06-04** demonstrates this pattern.

**What was done well:**
- ✅ Complete research anchor block (FY2025, 2026Q1, 2026-05-22 snapshot, mgmt)
- ✅ Body-level `[Sxx]` citations present (not just bibliography)
- ✅ Structured bull/bear with uncertainty register U01-U05
- ✅ Counter-evidence strong and symmetric with bull case
- ✅ Market-position claims scoped ("台湾 IPC 第 5 名")
- ✅ Judgment-first opening with clear thesis
- ✅ Monitoring signals useful and actionable

**Core issues (conditional pass level):**
- ❌ **Evidence label inflation** — S01/S02/S06/S11/S13 are news/aggregator/secondary sources labeled as `primary` or `[CONF]`; evidence tier higher than source quality warrants
- ❌ **Market snapshot incomplete** — PB, PS missing; market cap not in anchor block
- ❌ **Valuation lacks method** — PE used but no PB/PS/EV justification; Forward PE is Q1 annualized without scenario framework or multiple basis
- ❌ **Uncertainty does not narrow conclusion** — U01-U05 listed but conclusion not visibly reduced in confidence or precision
- ❌ **Self-assessment overconfident** — claims `final-audit 7/7` but actual checklist has far more than 7 items and several are partial

## Scoring

- **Full Pass**: honest label calibration + complete snapshot + recomputable valuation + uncertainty flows into conclusion
- **Conditional Pass**: strong structure but label inflation + snapshot + valuation gaps (this case's level)
- **Fail**: hard-fail triggered

## Related evals

- `evals/cases/advantech-listed-company-traceability-hard-fail-case.md` — companion: same-day listed-company
- `evals/cases/lotes-listed-company-moat-snapshot-case.md` — companion: snapshot incomplete + label inflation
