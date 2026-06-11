# Eval: DeepSeek Competitive Positioning — Evidence Label and Self-Assessment Gap Case

## Goal

Test whether a competitive-positioning / first-tier classification report with strong structural discipline (opening, dimension framework, aggregation rules, counter-evidence) can still pass when evidence labels overstate source strength, numeric role labels are absent, and self-assessment claims full pass despite gaps.

This eval is based on a real report: a DeepSeek competitive positioning memo that correctly activated the competitive-positioning route (scope/metric/timeframe defined, dimension-level conclusions, explicit overall-label gate) but leaked on label calibration, numeric role visibility, and self-assessment honesty.

## Prompt

Assess whether DeepSeek has entered the global first-tier of large-model companies. Produce a structured competitive positioning memo that:

- defines the classification frame (scope, metric, timeframe) before judging
- evaluates at least technology capability, product adoption, ecosystem strength, talent, and capital-markets position
- provides dimension-level conclusions
- provides an explicit overall-label aggregation rule
- uses inline claim-level source traceability
- distinguishes confirmed facts, inference, and open uncertainty
- includes counter-evidence and uncertainty that could change the classification

## What this eval is testing

- whether the model can keep evidence labels honest when the report structure is already strong
- whether source type discipline is maintained — secondary/media/aggregator sources do not silently carry `[CONF]` labels
- whether quantitative role labeling exists for key numbers (valuation, ARR, GPU count, team size, revenue estimates)
- whether self-assessment (audit status block) accurately reflects actual gaps rather than claiming full pass
- whether inferred claims include a visible reasoning chain, not just an `[INFER]` tag
- whether strong exclusivity wording ("唯一", "最大", "市场定义者", "全球第一") triggers evidence-match gates

## Pass criteria

A passing answer should:

1. **Label evidence by source type, not by how strong the claim sounds.**
   - primary documents (filings, official specs, audited financials) → confirmed fact
   - secondary sources (media reports, analyst notes, third-party benchmarks) → inference or conditional
   - aggregator rankings, Wikipedia, comparable-company estimates → proxy or model output, not confirmed
   - do not let secondary sources carry `[CONF]` just because the claim is plausible

2. **Label numeric roles for load-bearing numbers.**
   - distinguish observed (audited revenue, disclosed headcount), proxy (LinkedIn-based estimate, third-party tracker), assumption (total addressable market estimate), model output (valuation derived from comparable multiples)
   - do not mix numbers with different roles in one cell without separating them

3. **Keep self-assessment honest.**
   - audit status block must reflect actual gaps
   - source-traceability should not claim full pass if secondary sources carry `[CONF]`
   - quantitative-role should not claim full pass if numeric role labels are absent

4. **Provide reasoning chains for inferred claims.**
   - do not just tag `[INFER]` — show what evidence the inference rests on and what would change it
   - for claims that cannot be confirmed, enter the uncertainty register

5. **Match strong wording to evidence strength.**
   - exclusivity claims ("唯一认证", "最大", "市场定义者", "全球第一梯队") require evidence that supports exclusivity
   - if the evidence is secondary or indirect, downgrade the wording

## Failure signs

Mark this eval as failed if the answer does any of the following:

- uses secondary/media/aggregator sources as `[CONF]` for claims that drive the overall positioning conclusion
- has no numeric role labels for key financial, headcount, or scale figures
- self-assessment claims full pass on disciplines where the actual execution has visible gaps
- uses `[INFER]` without a reasoning chain connecting it to concrete evidence
- uses strong exclusivity wording ("唯一", "最大", "绝对领先") with only secondary/indirect support

## Why this eval matters

This catches a failure family that has become more visible as the skill strengthens route activation:

Now that opening quality, scope/metric/timeframe discipline, dimension-level conclusions, and counter-evidence structure are mostly stable, the remaining gap is **execution precision inside strong structure**.

A report can activate the right route, define dimensions, add source IDs, add counter-evidence, and an audit status block — and still leak because:

- evidence labels track plausibility instead of source type
- numbers lack role labels so the reader cannot audit what each figure means
- self-assessment claims pass without matching actual execution quality
- inferred claims are tagged but not traced

This is the difference between structural compliance and execution integrity. The gap is especially dangerous for competitive-positioning / first-tier reports because the overall label compression naturally tempts the model to let strong structure substitute for careful evidence weighting.

## Current rule verdict

The current rules should catch this as **warn**:

- source-traceability checklist requires claim-level traceability and source-type discipline — labels are too optimistic but partial tagging exists
- quantitative-role audit requires role separation for load-bearing numbers — labels are absent, which should trigger a non-blocker
- process-integrity hard-fail gate catches self-assessment vs evidence match — should block "all pass" claims if evidence has gaps
- strong-claim evidence-match rules exist but execution on exclusivity wording is inconsistent

This case guards against **structural compliance masking execution gaps** — the hardest failure mode to catch because the report does not look broken.

## Related evals

- `evals/cases/cambricon-first-tier-positioning-case.md` — same route, same overall-label compression risk
- `evals/cases/cambricon-evidence-weighting-and-traceability-case.md` — same evidence-weighting family
- `evals/cases/emc-listed-company-strong-claims-moat-case.md` — same conditional-pass / self-assessment gap pattern
- `evals/cases/cross-border-ecommerce-market-outlook-self-assessment-case.md` — self-assessment overconfidence pattern

## Reviewer checklist

- Does the answer route correctly to competitive-positioning / first-tier classification?
- Are evidence labels calibrated to source type, not claim strength?
- Do load-bearing numbers have visible role labels (observed/proxy/assumption/model output)?
- Does the self-assessment block match actual execution quality?
- Are inferred claims traced with reasoning chains, not just tagged?
- Are strong exclusivity wording claims supported by exclusivity-level evidence?

## Suggested scoring

- **Pass**: evidence labels match source type, numeric roles visible, self-assessment honest, inferred claims traced, strong wording evidence-matched
- **Conditional pass**: strong structure, route activation correct, counter-evidence present, but evidence labels over-optimistic (secondary sources as [CONF]), numeric roles absent, or self-assessment overclaims — with visible gaps
- **Fail**: structural compliance only; evidence weighting, numeric roles, and self-assessment all lack discipline; or key positioning claims are unauditable
