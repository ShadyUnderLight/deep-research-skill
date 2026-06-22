# Eval: AI Education Market Entry — Sensitivity Analysis and Route Intersection Case

## Goal

Test whether a Market Entry / Beachhead report with clear `GO / Pilot Only / Not Now` ranking, hard gates, sequencing logic, and explicit comparison framework can still **fail strict delivery** when:

- **sensitivity analysis absent** — the recommendation (SE Asia GO) depends on load-bearing assumptions (growth rate, ARPU, budget, localization cost, PMF threshold) that are not stress-tested; no "what would change this recommendation" quantification
- **body-level source traceability absent** — zero `[Sxx]` inline citations; source list is loose bibliography, not 7-column Source Register
- **declared secondary route (Constrained Choice) hard-fail not verified** — the report uses scoring/comparison as its ranking method, triggering constrained-choice numeric role requirements that are not satisfied
- **numeric role labels absent** — market size, CAGR, ARPU, K-12 population, budget, localization cost, PMF thresholds, composite scores lack observed/proxy/assumption/model-output roles
- **shortlist boundary not justified** — why these 4 markets (SE Asia, Japan, Middle East, Korea) and not EU, Latin America, India
- **aggregation not replicable** — star ratings and composite scores without scoring rules, weights, or worked examples
- **self-assessment claims all ✅ while traceability, numeric roles, sensitivity, and aggregation all have gaps** — triggers process-integrity hard-fail

This eval is based on a real report: an AI education product market entry memo that correctly activated the market-entry route, provided a clear GO/Pilot/Not Now framework with hard gates, sequencing logic, and actionable recommendations — but failed on sensitivity analysis, body traceability, numeric role labeling, secondary route verification, and self-assessment accuracy.

## Prompt

A Chinese AI education product company needs to select its first overseas market. Produce a structured market-entry decision memo that:

- defines the company profile (product type, stage, team size, budget)
- provides a country shortlist with justification — why these markets and not others
- rates each market as GO / Pilot Only / Not Now with explicit criteria
- provides a unified comparison framework with weighted variables, scoring rules, and at least 1 worked example
- identifies hard gates per market and sequencing logic
- distinguishes regional hub, first beachhead, and later expansion roles
- includes sensitivity analysis — which assumption changes would alter the recommendation
- uses `[Sxx]` inline citations throughout
- includes a complete 7-column Source Register with all entries cited in body
- labels all comparison/estimate numbers (market size, CAGR, ARPU, budget, localization cost, PMF thresholds) with observed/proxy/assumption/model-output roles
- if using scoring as part of the ranking method, independently verifies the Constrained Choice secondary hard-fail (numeric role labels)
- provides an honest self-assessment block

## What this eval is testing

- whether sensitivity analysis is executed for load-bearing assumptions — recommendations that depend on estimated variables must test which changes would reverse the ranking
- whether market-entry reports that use scoring/comparison as part of the ranking method satisfy the constrained-choice secondary route's numeric role requirements
- whether body-level source traceability is executed
- whether numeric role labels cover all key market/estimate numbers
- whether shortlist boundary is justified for market entry
- whether aggregation is replicable (scoring rules, weights, worked examples)
- whether self-assessment accuracy matches body execution

## Pass criteria

A passing answer should:

1. **Include sensitivity analysis for load-bearing assumptions.** For each key variable (growth rate, ARPU, budget, localization cost, PMF threshold), state the current assumption and the change that would alter the ranking. At minimum: "if X changes by Y%, the recommendation shifts from SE Asia to Japan/Middle East."

2. **Verify constrained-choice secondary route independently if scoring is used.** If the ranking uses weighted scores, star ratings, or composite indices, numeric role labels must be present on all comparison/estimate numbers.

3. **Execute body-level `[Sxx]` traceability.** Every key claim in exec summary, comparison table, market analysis, risk matrix, and action plan has an inline citation.

4. **Justify the shortlist boundary.** Explain why these specific markets were selected and what was excluded (EU, Latin America, India, etc.) and why.

5. **Label numeric roles on all market/estimate numbers.** Market size, CAGR, ARPU, K-12 population, budget, localization cost, PMF thresholds — all labeled as observed/proxy/assumption/model-output.

6. **Make aggregation replicable.** Scoring rules, weights, and at least 1 worked example tracing a market's composite score.

## Failure signs

Mark this eval as failed if the answer does any of the following:

- recommendation depends on estimated variables but no sensitivity analysis exists
- secondary constrained-choice hard-fail not verified when scoring/comparison is used for ranking
- body has zero `[Sxx]` inline citations (traceability hard-fail)
- numeric role labels absent from comparison/estimate numbers
- shortlist boundary not justified
- aggregation not replicable (no scoring rules or worked examples)
- self-assessment claims all ✅ while sensitivity, traceability, roles, or aggregation have gaps

## Why this eval matters

This case adds a **market-entry-specific sensitivity requirement** to the eval collection. Market-entry recommendations depend on multiple estimated variables (market growth, ARPU, regulatory timeline, localization cost). When these estimates are not stress-tested, the recommendation's robustness is unknown:

| Case | Route | Level | Sensitivity | Traceability | Numeric roles |
|---|---|---|---|---|---|
| NEV parts EU | market-entry | Conditional pass | Not tested | Partial | Missing |
| Sea market entry | market-entry | Conditional pass | Not tested | Partial | Missing |
| Short drama hub | market-entry | Conditional pass | Not tested | Partial | Missing |
| AI edu (this) | market-entry | **Fail** | **❌ Absent** | **❌ Zero [Sxx]** | **❌ Missing** |

The unique contributions:

- **Sensitivity analysis as a decision-utility requirement** — a market-entry recommendation that depends on growth rate, ARPU, and cost assumptions without testing what changes would reverse the ranking is decision-incomplete. This is different from "uncertainty register" (which lists what's unknown) — sensitivity analysis tests how hard the recommendation is before the unknown resolves.
- **Route intersection: market-entry × constrained-choice** — when market-entry scoring uses comparison/ranking methodology, the constrained-choice secondary route's numeric role requirements activate. This is a cross-route discipline intersection not yet tested.
- **Shortlist boundary for market entry** — market-entry shortlists are inherently about geographic options, and failing to justify why certain regions were excluded creates an un-auditable recommendation scope.

## Current rule verdict

- Market-entry hard-fail: sensitivity analysis absent for load-bearing assumptions
- Source traceability hard-fail: zero body `[Sxx]`
- Numeric role hard-fail: absent from comparison/estimate numbers
- Secondary route hard-fail: constrained-choice not verified
- Process-integrity hard-fail: self-assessment overclaim

## Related evals

- `evals/cases/short-drama-market-entry-hub-role-and-sensitivity-gap-case.md` — same route, hub role and sensitivity
- `evals/cases/ai-startup-hq-constrained-choice-register-compliance-case.md` — same aggregation replicability gap, different route
- `evals/cases/small-team-agent-constrained-choice-tech-dive-secondary-case.md` — same route intersection pattern, different route combination
- `evals/cases/indie-dev-constrained-choice-delivery-fail-case.md` — same traceability + numeric roles fail, different route

## Reviewer checklist

- Does the recommendation include sensitivity analysis for load-bearing assumptions?
- Is the declared secondary constrained-choice hard-fail verified (numeric roles)?
- Does the body have `[Sxx]` inline citations?
- Do comparison/estimate numbers have numeric role labels?
- Is the shortlist boundary justified (why these markets, what was excluded)?
- Is aggregation replicable (scoring rules, worked examples)?
- Does self-assessment match body execution?

## Suggested scoring

- **Pass**: sensitivity analysis present, secondary route verified, body `[Sxx]` present, numeric roles on all numbers, shortlist boundary justified, aggregation replicable, self-assessment honest
- **Conditional pass**: market-entry structure strong, GO/Pilot/Not Now clear, hard gates visible, sequencing logic present, but sensitivity analysis thin or absent, or traceability partial, or numeric roles on most but not all key numbers, or secondary route verification incomplete — no hard-fail triggered
- **Fail**: sensitivity analysis absent for load-bearing assumptions (decision-incomplete), or body zero `[Sxx]` (traceability hard-fail), or numeric role labels absent (hard-fail), or secondary route not verified, or self-assessment claims all ✅ while gaps exist (process-integrity hard-fail)
