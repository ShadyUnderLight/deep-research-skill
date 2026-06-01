# Eval: 恒大物业 Listed-Company Execution Near-Pass Case

## Goal

Test whether a listed-company / investment-style deep-research report can achieve near-complete execution of the route contract while still having minor but instructive gaps.

This eval is based on a real "near-pass" case: the report passed most route-contract checks and hard-fail conditions, but had 3 specific gaps. This is valuable as a **benchmark case** — it documents what a good report looks like and where the remaining edge cases are.

## Real case pattern

A user-provided 恒大物业 (Evergrande Property Services Group, 6666.HK) report dated **2026-05-29** demonstrates near-complete execution:

**What was done well:**
- ✅ Research Anchor Block present and complete (FY2025, FY2025 quarterly, 2026-05-29 market snapshot, management state)
- ✅ Judgment-first opening — "核心判断（一页摘要）" as first section, before any background
- ✅ Complete market snapshot (price HK$1.22, market cap HK$13.19B, PE 11.58x-12.32x TTM, PB ~7.7x, PS ~0.90x, 52-week 1.70/0.67)
- ✅ Evidence labeling consistent (Confirmed / Likely inference / Open uncertainty) throughout
- ✅ Support / Weakening / Unresolved split in §10 with a 3-column table
- ✅ Counter-evidence as independent chapter (§7) with 5 sub-risks
- ✅ Uncertainty register (U01-U06) with impact analysis
- ✅ Source register (S01-S11) with structured metadata
- ✅ Corporate-action compression guard (§5.3)
- ✅ Monitoring signals with time windows (§8.4)
- ✅ All 7 hard-fail conditions passed
- ✅ Source traceability with inline [SN]/[IN]/[UN] annotations
- ✅ No "unique/only/irreplaceable" language misuse

**What has minor gaps:**
- ⚠️ FY2022 data missing — report uses FY2023-FY2025 (3-year trend), but FY2022 is absent because the company was suspended/trading halt with delayed annual reports. This limits trend analysis completeness.
- ⚠️ Inline inference format inconsistency — sometimes `[I01]`, sometimes `Likely inference [I01]`, sometimes just prose like "各源略有差异"
- ⚠️ Valuation methodology not fully expanded — PE (11.6x) used as primary anchor but no explicit reasoning for why PE over EV/EBITDA, PS, or PB; PB (~7.7x) and PS (~0.90x) mentioned as calculated figures but their limitations not discussed

## What this eval is testing

### Test Dimension 1: Near-complete route execution is achievable

The primary test is whether the system can produce a listed-company report that:
- passes all hard-fail conditions
- includes all mandatory sections (anchor block, market snapshot, evidence labels, counter-evidence, uncertainty register, source register, bottom line)
- opens as a judgment memo rather than a profile

This case serves as a **regression benchmark** — a standard that future reports should meet.

### Test Dimension 2: Data completeness in edge cases

FY2022 data gap tests whether the system:
- recognizes when a data period is missing rather than filling it with estimates
- explicitly documents gaps as uncertainty items
- assesses whether trend analysis is materially weakened by the gap

### Test Dimension 3: Source traceability formatting discipline

The inline format inconsistency tests:
- whether evidence-label usage is consistent throughout the document
- whether inference annotations follow a single canonical format rather than drifting between variants
- whether all Source Register entries have visible body citations

### Test Dimension 4: Valuation methodology reasoning

The valuation discussion gap tests whether:
- the report explains *why* a chosen valuation metric is appropriate for this company
- alternative metrics are discussed and reasons given for not relying on them
- metric-specific limitations are acknowledged (e.g., PB for post-restructuring equity, PS ignoring margin trends)

## Pass criteria

A good answer should:

1. **Complete route contract** — pass all hard-fail checks, include all mandatory sections
2. **Data gap handling** — when a data period is unavailable, either fill it from available sources or explicitly document the gap as a limitation
3. **Format consistency** — all inline inference annotations use a single canonical format throughout the document
4. **Valuation methodology** — include brief reasoning for chosen primary metric and discussion of alternatives
5. **Opening completeness** — judgment, key variables, and strongest weakening evidence all visible on first screen

## Failure signs

Mark this eval as **partial** rather than full pass if the answer does any of the following:

- misses any mandatory section (research anchor block, market snapshot, counter-evidence chapter, uncertainty register, source register)
- fails any hard-fail condition
- omits discussion of valuation metric choice when the company has unusual risk characteristics (post-restructuring, high leverage,关联风险)
- has inline evidence annotations in inconsistent formats
- fails to document a known data gap as a limitation

## Why this case exists

Existing listed-company evals focus on **failure modes**:

- `evals/cases/amat-listed-company-anchor-and-label-execution-case.md` — anchor block missing, label inflation, background-first opening
- `evals/cases/intel-current-state-freshness-case.md` — stale anchor
- `evals/cases/cnooc-judgment-shape-improved-but-freshness-still-leaked-case.md` — judgment shape with freshness leak
- `evals/cases/china-shenhua-listed-company-judgment-and-traceability-case.md` — judgment visibility and traceability

This case is the first **near-pass benchmark** — it documents what a good report looks like and where the remaining edge cases are. It serves as:

1. A **regression target** — future reports should at minimum match this execution level
2. A **gap classifier** — the 3 gaps form a checklist of what to tighten after the major failure modes are solved
3. A **calibration point** — helps distinguish "must fix for pass" from "nice to have for excellence"

## Suggested intervention target

The gaps found in this near-pass case should push changes at the margin:

- `references/report-template.md` — add guidance for data gap documentation when a fiscal year is unavailable (停牌/延迟发布场景)
- `references/finance-date-discipline.md` — add note about multi-year trend completeness when a year is missing
- `references/valuation-methodology.md` — strengthen guidance on metric selection reasoning, especially for post-restructuring or high-risk companies
- `checklists/listed-company-report.md` — add minor check for annotation format consistency (non-blocker)
- `checklists/final-audit.md` — add non-blocker check for valuation methodology reasoning

These are lower priority than the anchor/label fixes from `evals/cases/amat-listed-company-anchor-and-label-execution-case.md`.

## Reviewer checklist

- Was the research anchor block present and complete?
- Was the market snapshot complete (price, cap, multiples, range, date)?
- Did the opening present judgment before background?
- Were all evidence annotations in a consistent format?
- Was the valuation methodology explained with metric-choice reasoning?
- Were known data gaps explicitly documented as limitations?

## Suggested scoring

- **Full pass**: all route contract items satisfied, valuation methodology explained, annotation format consistent, all data gaps documented
- **Near pass**: route contract satisfied, but minor gaps in valuation reasoning or annotation consistency (this case's level)
- **Fail**: any hard-fail condition triggered, or any mandatory section missing

## Related evals

- `evals/cases/amat-listed-company-anchor-and-label-execution-case.md` — cluster failure (contrast case: what a failing report looks like)
- `evals/cases/intel-current-state-freshness-case.md` — stale-anchor failure
- `evals/meta/listed-company-judgment-memo-execution-family.md` — broader execution family diagnosis
