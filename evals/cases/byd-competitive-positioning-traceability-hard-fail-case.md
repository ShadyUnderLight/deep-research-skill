# Eval: BYD Competitive Positioning — Source Traceability Hard-Fail and Self-Assessment Integrity Case

## Goal

Test whether a competitive-positioning / first-tier classification report with strong structural elements (opening judgment, dimension framework, counter-evidence, aggregation rules, overall-label gate) can still **fail** when:

- body-level source traceability is essentially not executed — most key claims lack claim-level citations, Source Register is incomplete, and >50% of registered sources are uncited
- evidence labels are systematically over-optimistic — secondary/media/analyst sources carrying `[确认事实]` labels
- self-assessment is completely incorrect — source-traceability, quantitative-role, and final-audit all claimed as passed while body execution has visible gaps → triggers process-integrity and declared-not-executed hard-fails
- quantitative role labels are absent from load-bearing tables
- strong exclusivity wording ("全球独一无二", "汽车工业史上前所未有", "无可争议的全球第一") lacks exclusivity-level evidence
- opening has metadata-first drift — route metadata and evidence legend precede the thesis

This eval is based on a real report: a BYD NEV competitive positioning memo that activated the correct route, defined scope/metric/timeframe, built a dimension framework with counter-evidence, and had an explicit overall-label gate — but failed on fundamental source traceability execution, label calibration, and self-assessment integrity.

## Prompt

Assess whether BYD is a global first-tier player in the NEV industry chain. Produce a structured competitive positioning memo that:

- defines the classification frame (scope, metric, timeframe) before judging
- evaluates at least sales scale, technology depth, supply chain/globalization, financial/profitability, and brand dimensions
- provides dimension-level conclusions
- provides an explicit overall-label aggregation rule and reversal conditions
- uses inline claim-level source traceability with `[Sxx]` or functional equivalent for every load-bearing claim
- includes a complete 7-column Source Register (ID, Source Name, Type, Date, DOI/URL, Claims Supported, Evidence Tier)
- distinguishes confirmed facts (primary/filing), inference (secondary/analyst), and open uncertainty
- includes counter-evidence that adjusts the conclusion
- labels numeric roles (observed / proxy / assumption / model output) for key figures

## What this eval is testing

- whether the model can execute source traceability at the body level, not only in the appendix
- whether evidence labels are calibrated to source type (primary = confirmed, secondary = inference/conditional)
- whether self-assessment (audit status block) accurately reflects actual execution gaps instead of claiming full pass
- whether process-integrity and declared-not-executed hard-fail gates are triggered when execution contradicts self-assessment
- whether quantitative role labels are applied to load-bearing numbers in tables
- whether strong exclusivity wording triggers evidence-match gates
- whether the opening prioritizes thesis/risk/unknown over route metadata

## Pass criteria

A passing answer should:

1. **Execute body-level source traceability.**
   - every load-bearing claim in the executive summary, dimension conclusions, and overall conclusion has a claim-level citation (`[Sxx]` or functional equivalent)
   - Source Register is complete 7 columns including DOI/URL
   - all registered sources are cited in body (no register inflation)
   - the report reads as auditable from any key sentence to a single source

2. **Calibrate evidence labels to source type.**
   - primary documents (filings, official specs, audited financials) → confirmed fact
   - secondary sources (media reports, analyst notes, third-party benchmarks) → inference or conditional
   - do not let secondary sources carry `[确认事实]` labels even if the claim is plausible
   - respect the evidence label ceiling — no source type is upgraded beyond its weight

3. **Keep self-assessment honest.**
   - audit status block must match actual body execution
   - source-traceability cannot claim pass if body citations are missing or register is incomplete
   - quantitative-role cannot claim pass if numeric role labels are absent
   - process-integrity gate must flag any mismatch

4. **Apply quantitative role labels to key numbers.**
   - distinguish observed (audited revenue, disclosed production), proxy (third-party tracker, LinkedIn estimate), assumption (TAM estimate), model output (valuation from multiples)
   - label roles in tables alongside the numbers

5. **Match strong wording to evidence strength.**
   - exclusivity claims ("全球独一无二", "前所未有的", "无可争议的全球第一") require evidence that supports exclusivity
   - if the evidence is secondary or indirect, downgrade the wording

6. **Prioritize thesis in the opening.**
   - the first screen should show the core judgment, key risk, and key unknown — not route metadata or evidence legend
   - metadata/legend belongs after the opening or in footnotes

## Failure signs

Mark this eval as failed if the answer does any of the following:

- most load-bearing claims in exec summary, dimension conclusions, or overall conclusion lack claim-level citations
- Source Register has fewer than 7 columns or DOI/URL is absent
- more than 30% of registered sources are uncited in body (register inflation)
- secondary/media/analyst sources systematically carry confirmed-fact labels for claims that drive the overall positioning
- self-assessment claims full pass on disciplines where body execution has visible gaps (process-integrity hard-fail)
- quantitative role labels are absent from tables with load-bearing numbers
- strong exclusivity wording appears without exclusivity-level evidence support
- opening screen shows route metadata before thesis/judgment

## Why this eval matters

This case captures a distinct failure level within the competitive-positioning route:

The DeepSeek case (`deepseek-competitive-positioning-evidence-label-case.md`) tested **conditional pass** — structure right, evidence labels over-optimistic but partial tagging exists. This case tests **hard fail** — structure partially right, but source traceability fundamentally not executed, evidence labels systematically wrong, and self-assessment completely disconnected from reality.

The key escalation:

- Not "some labels are a bit strong" but "most source traceability infrastructure is missing or ornamental"
- Not "self-assessment could be more precise" but "self-assessment is flatly wrong, triggering two hard-fail gates"
- Not "register has a minor format issue" but "register is incomplete (6 vs 7 columns) and 68% of sources are uncited"

This is the difference between a report that needs label refinement and a report that needs a structural rebuild of its evidence layer before it can be considered delivered.

Without this eval, the skill could produce reports that look structurally competent (opening, dimensions, counter-evidence, audit block) but are fundamentally unauditable at the claim level — the most dangerous failure mode for decision-quality research.

## Current rule verdict

The current rules should catch this as **fail**:

- body-level source traceability hard-fail is triggered — >3 load-bearing claims lack `[Sxx]` or equivalent
- Source Register 7-column hard-fail is triggered — DOI/URL column missing
- register inflation hard-fail is triggered — >50% uncited sources
- process-integrity hard-fail is triggered — self-assessment contradicts body execution
- declared-not-executed hard-fail is triggered — source-traceability and quantitative-role declared passed but not executed

This case guards against **structural competence as a disguise for execution failure**.

## Related evals

- `evals/cases/deepseek-competitive-positioning-evidence-label-case.md` — same route, same label/self-assessment family but conditional-pass level
- `evals/cases/cambricon-first-tier-positioning-case.md` — same route, same overall-label compression risk
- `evals/cases/cambricon-evidence-weighting-and-traceability-case.md` — same evidence-weighting family
- `evals/cases/advantech-listed-company-traceability-hard-fail-case.md` — same hard-fail traceability pattern, different route
- `evals/cases/pop-mart-listed-company-traceability-hard-fail-case.md` — same claim-level traceability collapse
- `evals/cases/emc-listed-company-strong-claims-moat-case.md` — same strong-claim without exclusivity evidence pattern
- `evals/cases/cross-border-ecommerce-market-outlook-self-assessment-case.md` — self-assessment overconfidence pattern

## Reviewer checklist

- Does the answer execute body-level source traceability or only appendix-level?
- Is the Source Register complete (7 columns, DOI/URL present)?
- Are uncited sources below 30% of total registered?
- Are evidence labels calibrated to source type (primary→confirmed, secondary→inference)?
- Does the self-assessment block match actual body execution?
- Are quantitative role labels present in load-bearing tables?
- Are strong exclusivity wording claims supported by exclusivity-level evidence?
- Does the opening prioritize thesis over metadata?

## Suggested scoring

- **Pass**: body-level source traceability executed, Source Register complete with low uncited ratio, evidence labels calibrated to source type, self-assessment honest, quantitative roles visible, strong wording evidence-matched, thesis-first opening
- **Conditional pass**: route activation correct, structural elements present, but traceability is partial (some key claims missing citations), labels are slightly over-optimistic, or self-assessment has minor mismatches — no hard-fail triggered
- **Fail**: source traceability fundamentally not executed (most key claims uncited), register incomplete or heavily inflated, secondary sources systematically carry confirmed-fact labels, self-assessment contradicts body execution triggering process-integrity/declared-not-executed hard-fails, or quantitative roles entirely absent
