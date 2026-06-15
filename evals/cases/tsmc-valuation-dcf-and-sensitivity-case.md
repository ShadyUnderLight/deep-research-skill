# Eval: TSMC Listed-Company — DCF and Sensitivity Matrix Case

## Goal

Test whether a Listed-Company / Investment-Style report that answers a valuation question for a cash-flow-positive, long-operating-history company produces a **DCF or reverse DCF analysis with sensitivity matrix** (or an explicit explanation of non-applicability), rather than relying solely on PE/EPS scenario analysis for its valuation conclusion.

The reference failure is the existing TSMC report (`tmp/tsmc-valuation-report.md`), which has a well-structured listed-company memo with:
- judgment-first opening and clear thesis
- complete research-anchor block and market snapshot
- bull/bear framework with optimistic/base/pessimistic scenarios
- PE/EPS-based valuation ranging

But the core valuation methodology is exclusively PE-multiple + consensus-EPS-based: the report provides PE scenarios under different growth assumptions, but has **no DCF model, no reverse DCF, no explicit FCF-based valuation, and no sensitivity matrix** that would let a reader reconstruct the valuation conclusion from first principles.

This eval tests that the new template rules (DCF trigger + sensitivity matrix) produce outputs that close this gap: a listed-company valuation is not complete if the conclusion rests entirely on multiple-based scenarios without cash-flow-based structural analysis and sensitivity disclosure.

## Prompt

Assess whether TSMC is undervalued or overvalued at current levels (~$180 USD / ~$1,350 TWD as of mid-2026), given its strong free cash flow generation, long operating history (1987–present), dominant market position in advanced semiconductor manufacturing, and significant AI-driven growth prospects. Produce a structured listed-company investment memo that:

- provides a judgment-first opening with clear thesis
- includes a research-anchor block (FY, latest quarter, market snapshot date, management context)
- provides a current financial/market snapshot with clearly dated and cited key numbers
- uses `[Sxx]` or equivalent claim-level inline citations for every load-bearing claim
- includes a complete 7-column Source Register
- **uses DCF or reverse DCF as a structured valuation framework** (or provides an explicit, justified explanation if DCF is deemed inapplicable for TSMC)
- **includes a sensitivity matrix showing valuation changes under different assumptions for at least one high-sensitivity variable** (e.g., WACC, terminal growth rate, long-term revenue CAGR, or sustainable FCF margin)
- **does not rely on PE/EPS scenario analysis as the sole basis for the valuation conclusion**

## What this eval is testing

- whether the DCF/reverse DCF trigger fires when the company is cash-flow-positive with a long operating history and predictable cash flow profile
- whether the report produces a DCF assumptions table (or reverse DCF) OR explicitly explains why DCF was not used
- whether key DCF assumptions have number roles (assumption / model output) and source/method documented
- whether a sensitivity matrix or tipping-point analysis is present for at least one high-sensitivity assumption
- whether multi-variable scenario analysis (optimistic/base/pessimistic) is treated as distinct from single-variable sensitivity analysis — they are complementary, not substitutable
- whether all existing listed-company discipline (research-anchor block, market snapshot, `[Sxx]` traceability, 7-column Source Register) is maintained alongside the new DCF content

## Pass criteria

A passing answer should:

1. **Include DCF or reverse DCF analysis (or explicit non-applicability).**
   - **Forward DCF**: explicit revenue/FCF projections, WACC derivation, terminal value calculation, and resulting fair value per share
   - **Reverse DCF**: calculate the implied growth rate / FCF yield / terminal multiple embedded in the current price, and evaluate whether that implied assumption is reasonable relative to evidence
   - **Explicit non-applicability**: if DCF is deemed not applicable, the report must explain *why* (e.g., "FCF is too volatile to project meaningfully" or "terminal value dominates the result beyond useful bounds") — not simply omit DCF without explanation
   - A passing answer may use either forward DCF or reverse DCF; it does not need to do both

2. **Document DCF assumptions with number roles and source/method.**
   - Each key assumption must carry a role label: `assumption` / `model output` / `observed input`
   - Each assumption must have a source or method note: "based on 5yr historical average," "consensus estimate from [source]," "management guidance," "author estimate supported by [evidence]"
   - Assumptions that should be covered (at minimum): revenue growth trajectory, operating margin / FCF conversion, CapEx intensity (CapEx/Revenue), WACC (cost of equity + capital structure), terminal growth rate, terminal value method (perpetuity vs exit multiple)

3. **Include a sensitivity matrix or tipping-point analysis for at least one high-sensitivity assumption.**
   - Sensitivity matrix: a table showing how valuation changes when one assumption varies across a range (e.g., WACC ±1%, terminal growth ±0.5%, long-term revenue CAGR ±2%), with all other assumptions held constant
   - Tipping-point analysis: identify the value of a key assumption at which the valuation crosses a threshold (e.g., "if WACC exceeds 11%, TSMC is overvalued at current price")
   - The chosen assumption must be plausibly high-sensitivity for a DCF: WACC, terminal growth rate, or long-term revenue growth are preferred; terminal value method is acceptable

4. **Do not substitute multi-variable scenarios for single-variable sensitivity.**
   - Optimistic/base/pessimistic scenarios that vary multiple assumptions simultaneously (e.g., "bull case: high revenue growth + low WACC + high terminal growth") do **not** satisfy the sensitivity requirement
   - The sensitivity matrix must vary one assumption at a time, holding others constant, to isolate the marginal impact of each variable
   - Multi-variable scenarios are complementary and encouraged, but they are not a replacement for single-variable sensitivity

5. **Maintain all existing listed-company discipline.**
   - research-anchor block present and complete (FY, latest quarter, market snapshot date, management context)
   - market snapshot table present and complete
   - body-level `[Sxx]` traceability for every load-bearing claim
   - 7-column Source Register (ID, Source Name, Type, Date, DOI/URL, Reliability, Claims Supported)
   - evidence labels match source strength
   - conclusion is calibrated to evidence strength, not overstated

## Failure signs

Mark this eval as failed if the answer does any of the following:

- valuation conclusion is based solely on PE/EPS scenario analysis without DCF or reverse DCF, and no explanation is given for why DCF was not used — this is the primary hard-fail when the company is clearly cash-flow-positive with long operating history
- DCF (or reverse DCF) is attempted but key assumptions are stated without source/method or role labels — the valuation is non-reconstructable
- sensitivity matrix is absent for high-sensitivity assumptions (WACC, terminal growth, long-term revenue)
- multi-variable scenarios are presented as substitutes for single-variable sensitivity analysis
- the report has the same structure as the existing TSMC report (`tmp/tsmc-valuation-report.md`) with only cosmetic changes — i.e., PE scenarios remain the sole valuation methodology
- DCF is omitted without explanation, or the explanation is a vague justification like "DCF is not needed for this company" without specific reasoning

## Why this eval matters

The existing TSMC report (`tmp/tsmc-valuation-report.md`) demonstrates a clear failure mode: a well-structured listed-company memo with judgment-first opening, complete research anchor, market snapshot, PE-based valuation scenarios under bull/bear frameworks — but the core valuation conclusion is supported **only** by multiple-based analysis (PE range × consensus EPS). There is no DCF, no reverse DCF, no FCF-based structural valuation, and no sensitivity analysis. A reader cannot reconstruct the valuation from first principles or understand which assumption changes would tip the conclusion.

For a company like TSMC — with 35+ years of financial history, predictable cash generation, dominant market position, and clear capex-driven FCF dynamics — the absence of DCF-based analysis is a material gap in the valuation methodology. The conclusion "未充分反映长期价值" is precise-sounding but non-reconstructable without disclosed structural assumptions.

Issue #278 proposes DCF/reverse DCF trigger rules, assumption table templates, and sensitivity matrix requirements to close this gap. This eval validates that those rules actually produce the behavioral change. Without this eval, the trigger rules could be added but never verified to actually fire during report generation.

This eval is distinct from the existing TSMC eval cases:
- `evals/cases/tsmc-valuation-time-horizon-stratification-case.md` focuses on time-horizon stratification of the valuation judgment
- `evals/cases/tsmc-listed-company-aggregator-source-and-moat-case.md` focuses on aggregator source discipline and moat classification
- This case focuses on **valuation methodology completeness**: DCF/sensitivity as structural requirements for any listed-company valuation

## Current rule verdict

- **Without new rules (status quo)**: existing TSMC report passes listed-company checklist (has research anchor, market snapshot, valuation scenarios, bull/bear framework, source register) but produces a PE-only valuation with no DCF or sensitivity matrix — this eval would FAIL.
- **With new rules (after issue #278)**: a compliant report must include DCF or reverse DCF (or explicit non-applicability) and a sensitivity matrix to pass listed-company checklist. A report that meets these requirements should PASS or CONDITIONAL-PASS this eval.

## Relationship to new rules

This eval directly tests the behavioral impact of three new rules proposed in issue #278:

1. `references/valuation-methodology.md` §DCF / reverse DCF trigger rules — defines when a listed-company valuation must use DCF (cash-flow-positive, long operating history) or provide explicit non-applicability explanation
2. `references/report-template.md` §DCF assumption table + sensitivity matrix template — provides a structured template for DCF assumptions (revenue growth, margin, CapEx/Rev, WACC, terminal growth) with role labels and a sensitivity matrix format
3. `checklists/listed-company-report.md` — new checklist items for DCF/sensitivity: "DCF or reverse DCF present or non-applicability explained," "key assumptions labeled with role and source/method," "sensitivity matrix for at least one high-sensitivity assumption," "multi-variable scenarios not replacing single-variable sensitivity"

## Related evals

- `evals/cases/tsmc-valuation-time-horizon-stratification-case.md` — same company, time-horizon stratification focus (issue #277)
- `evals/cases/tsmc-listed-company-aggregator-source-and-moat-case.md` — same company, aggregator source + moat classification focus
- `evals/cases/pop-mart-listed-company-traceability-hard-fail-case.md` — same route, traceability focus
- `evals/cases/xiaohongshu-startup-evaluation-traceability-benchmark-case.md` — sensitivity analysis requirement for load-bearing assumptions (startup route)
- `evals/cases/startup-evaluation-route-activation-case.md` — startup route's DCF avoidance rule (inverse of listed-company DCF requirement)
- `evals/cases/industrial-robot-market-entry-compound-criterion-gap-case.md` — sensitivity analysis gap in market-entry route (related principle: scenario ≠ sensitivity)

## Reviewer checklist

- Does the report include DCF or reverse DCF analysis? If not, is explicit non-applicability explained with specific reasoning?
- If DCF is used, are key assumptions documented with role labels (assumption / model output) and source/method?
- Is a sensitivity matrix present, varying one assumption at a time? Does it cover a plausibly high-sensitivity variable (WACC, terminal growth, long-term revenue)?
- If multi-variable scenarios exist, are they clearly distinguished from single-variable sensitivity, or are they presented as substitutes?
- Does the valuation conclusion remain non-reconstructable even with DCF numbers (e.g., DCF presented but assumptions from unknown sources)?
- Are all existing listed-company discipline items maintained alongside the new DCF content?
- If the report omits DCF for a cash-flow-positive company with long history, is the explanation credible and specific (not a boilerplate justification)?
- Does the report avoid the exact structural failure of the existing TSMC report — PE-only valuation without structural FCF analysis?

## Suggested scoring

- **Pass**: DCF or reverse DCF present with documented assumptions (roles + source/method), sensitivity matrix for at least one high-sensitivity assumption, single-variable sensitivity distinguished from multi-variable scenarios, all existing listed-company discipline maintained, conclusion reconstructable from disclosed assumptions
- **Conditional pass**: DCF or reverse DCF present but sensitivity matrix partially covers only a low-sensitivity variable, or some assumptions lack role labels or source/method, or the existing listed-company discipline has minor gaps (e.g., 1-2 missing source-register columns), but no hard-fail violation — the core DCF trigger fired correctly but execution quality could improve
- **Fail**: no DCF or reverse DCF and no explicit non-applicability explanation (primary hard-fail for cash-flow-positive company with long history), or DCF present but assumption chain incomplete or non-reconstructable, or sensitivity matrix absent for all high-sensitivity assumptions, or multi-variable scenarios substituted for single-variable sensitivity, or PE-only valuation structure replicates the existing TSMC report failure mode
