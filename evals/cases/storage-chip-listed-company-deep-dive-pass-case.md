# Eval: 存储芯片 Listed-Company + Technical Deep-Dive Pass Case

## Goal

Test whether a dual-route report (Listed Company primary + Technical Deep-dive secondary) can achieve a clean pass-level rating with a well-executed evidence system and route contract, while still having minor but instructive gaps in source attribution discipline.

This eval is a **pass-level benchmark case**. Unlike other cases in this directory that document failure modes, this case documents what a good report looks like and where even a good report can have small gaps.

## Real case pattern

A user-provided 存储芯片产业链深度投资研究报告 (Storage Chip Industry Chain Deep Investment Research Report) dated **2026-05-29** demonstrates pass-level execution.

**What was done exceptionally well:**
- ✅ **Evidence system design** — 3-tier evidence labels ([Confirmed]/[Inference]/[Unknown]) + 4-tier number role labels ([Observed]/[Inferred]/[Model Output]/[Manufacturer Claim]) used consistently throughout the full report
- ✅ **Judgment-first opening** — 8 labeled judgment bullets in the executive summary, thesis + key data + risk signals with no background preamble
- ✅ **All 12 mandatory sections present and decision-useful**
- ✅ **All hard-fail conditions passed** — both primary (Listed Company) and secondary (Technical Deep-dive) route hard-fails clean
- ✅ **Dual-route execution** — primary route (listed-company: valuation table, investment ranking, target recommendations) + secondary route (technical deep-dive: HBM4E latest data, 3D NAND comparison table, technology bottleneck analysis) both visible
- ✅ **Counter-evidence present** — sections 10 (geopolitics) and 11 (risks) dedicated to counter-arguments
- ✅ **Scope-limited claims** — all market share claims specify scope ("global storage chip", "DRAM three oligarchs", "China market")
- ✅ **No "unique/only/irreplaceable" language**
- ✅ **Cross-source data conflict awareness** — TrendForce ($225B) vs WSTS-derived (~$160-180B) discrepancy noted
- ✅ **Freshness appropriate** — latest data as of 2026Q1 and 2026/05, consistent with report date

**What has minor gaps:**
- ⚠️ **Bare "预计" without source** — at least 5 instances of "预计...发布" / "商用预计..." without stating who expects this. This violates `references/forward-looking-discipline.md` Pattern 1 (bare forecast).
- ⚠️ **Research anchor not compact** — latest FY/quarter/market snapshot data is split between sections 4 (financials) and 9 (valuation), not centralized as a compact anchor block.
- ⚠️ **No inline `[SN]` citations** — evidence labels are visible in the body, but there are no numbered inline references pointing to section 13's source list. Readers can infer source attribution but cannot precisely trace each claim.

## What this eval is testing

### Test Dimension 1: Pass-level dual-route execution

This case tests whether a report can simultaneously satisfy two route contracts (Listed Company + Technical Deep-dive). The primary test is whether all hard-fail conditions of both routes are checked, and whether both routes' mandatory sections are visibly present.

### Test Dimension 2: Evidence system quality

The report's evidence system (3-tier labels + 4-tier number role labels) is the strongest seen across all eval cases. This case serves as a benchmark for what good evidence labeling looks like.

### Test Dimension 3: Source attribution discipline (even in a good report)

The 3 gaps in this case all relate to source attribution:
- bare "预计" is a forward-looking discipline failure
- research anchor compaction is a structural clarity issue
- missing inline `[SN]` citations is a traceability issue

These gaps are minor enough that the report still passes, but they are instructive: even the best reports in the current system have source attribution gaps.

## Pass criteria

A pass-level report should:

1. **All hard-fail conditions passed** for both primary and secondary routes
2. **All mandatory sections present and decision-useful**
3. **Evidence system consistent** — labels used for all load-bearing claims
4. **Source attribution disciplined** — every "预计" has a named source; no bare forecasts
5. **Research anchor compact** — latest FY, latest quarter, market snapshot date centralized in one visible block
6. **Inline traceability** — load-bearing claims have body-level source references or at minimum the evidence tier is sufficient for the claim

## Failure signs

Mark this eval as **partial pass** (not fail) if the report:

- has bare "预计" without source attribution (5+ instances = blocker for full pass)
- splits research anchor data across sections instead of compacting it
- lacks inline `[SN]` citations for load-bearing claims
- still passes all hard-fail conditions and quality gates

Mark this eval as **fail** if any hard-fail condition is triggered.

## Why this case exists

This is the first **pass-level benchmark** in the cases/ directory. Existing cases document failure modes:

| Case | Type | Rating |
|------|------|--------|
| `evergrande-property-listed-company-execution-case.md` | Near-pass benchmark | 🟡 Near-pass |
| `innolight-listed-company-execution-case.md` | Near-pass benchmark | 🟡 Near-pass |
| **This case** | **Pass benchmark** | ✅ **Pass** |

This case serves as:
1. A **quality target** — future reports should match this execution level
2. A **threshold calibrator** — helps distinguish "pass" from "near-pass" from "fail"
3. A **gap minimizer** — even at pass level, 3 source-attribution gaps remain, showing where the next improvement iteration should focus

## Suggested intervention target

The gaps in this pass-level report suggest marginal improvements:

- `references/forward-looking-discipline.md` — strengthen the bare-forecast detection pattern with explicit checklist language
- `references/report-template.md` — add "Research Anchor" as a compact mandatory block (not split across sections)
- `checklists/final-audit.md` — add non-blocker: "all '预计' instances have a named source" (even in pass-level reports, bare forecasts should be flagged)
- `checklists/listed-company-report.md` — add non-blocker: "research anchor compact — all time-layer data in one visible block"

These are lowest priority compared to the blocker-level fixes suggested by `evals/cases/amat-listed-company-anchor-and-label-execution-case.md`.

## Reviewer checklist

- Are all hard-fail conditions for all declared routes passed?
- Is the evidence system consistent throughout?
- Are all "预计" instances attributed to a named source?
- Is the research anchor compact (FY, quarter, snapshot date in one block)?
- Are load-bearing claims traceable in the body?

## Suggested scoring

- **Full pass**: all hard-fails passed, all mandatory sections present, evidence system consistent, source attribution clean, research anchor compact
- **Pass with minor gaps**: all hard-fails passed, evidence system good, but bare forecasts or non-compact anchor exist (this case's level)
- **Near-pass**: some hard-fails borderline, or evidence system inconsistent
- **Fail**: hard-fail triggered, or quality gates not met

## Related evals

- `evals/cases/evergrande-property-listed-company-execution-case.md` — near-pass benchmark (恒大物业)
- `evals/cases/innolight-listed-company-execution-case.md` — near-pass benchmark (中际旭创)
- `evals/cases/humanoid-robot-market-outlook-dual-route-case.md` — dual-route failure (人形机器人)
- `evals/cases/amat-listed-company-anchor-and-label-execution-case.md` — listed-company cluster failure (AMAT)
- `evals/comparative-distillation/byd-gpt-vs-minimax-comparative-distillation.md` — numerical discipline patterns
