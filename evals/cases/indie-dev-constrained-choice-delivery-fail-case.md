# Eval: Indie Developer Product Form — Constrained Choice Delivery Fail Case

## Goal

Test whether a constrained-choice / option-selection report with near-conditional-pass decision quality (clear ranking, decision architecture, reversal conditions, action plan) can still **fail delivery** when:

- numeric role labels are entirely absent from comparison/score/estimate tables — triggers constrained-choice hard-fail per ROUTING-MATRIX.md
- no 7-column Source Register exists — body has `[1]`-style references but no structured source table with type/date/URL/claims-supported
- declared source-traceability and quantitative-role disciplines not executed in body (process-integrity violation)
- shortlist construction boundary not justified — "why these three forms and not others" has no visible reasoning
- hidden operational burdens incomplete — payment processing, support overhead, privacy/permissions review, Chrome Web Store takedown risk not surfaced in the same decision layer
- aggregation logic (star ratings from 5-variable framework) not replicable — no weights, no worked example, reader cannot verify ranking derivation

This eval is based on a real report: an indie developer product form selection memo (browser extension vs mobile app vs SaaS tool) that reached near-conditional-pass decision quality but failed on delivery packaging, source infrastructure, numeric role labeling, and process-integrity.

## Prompt

A budget-constrained indie developer needs to choose a product form: browser extension, mobile app, or SaaS tool. Produce a structured decision memo that:

- defines hard constraints and soft preferences
- justifies why these three forms are the shortlist (and what was excluded)
- provides a replicable comparison framework with weighted variables
- gives a clear ranking with why top option wins, why runner-up is credible, and why each other option loses
- identifies ranking-reversal conditions and hidden operational burdens
- uses claim-level source traceability with a complete 7-column Source Register
- labels all load-bearing numbers with observed/proxy/assumption/model-output roles
- includes an honest self-assessment block matching actual execution

## What this eval is testing

- whether numeric role labeling is applied to constrained-choice comparison/score/estimate tables (the route's defining hard-fail condition)
- whether a complete 7-column Source Register is present with claim-level body mappings
- whether declared source-traceability and quantitative-role disciplines are actually executed in body, not just declared in metadata
- whether the shortlist boundary is justified — constrained-choice requires explaining why these options were selected and what was excluded
- whether hidden operational burdens are comprehensive (platform risk, payment, support, compliance, takedown risk), not just the most obvious ones
- whether the aggregation/ranking method is replicable — reader should be able to verify why scores produce this exact order

## Pass criteria

A passing answer should:

1. **Label numeric roles in all comparison/score/estimate tables.**
   - every key number has an observed/proxy/assumption/model-output role label
   - star ratings and ranking scores are labeled as model output
   - pricing, revenue, cost estimates are labeled as observed (if disclosed), proxy (if third-party tracked), or assumption (if modeled)

2. **Provide a complete 7-column Source Register.**
   - ID, Source Name, Type, Date, DOI/URL, Claims Supported, Evidence Tier
   - every body claim with a `[Sxx]` maps to a register entry
   - register inflation below 25%

3. **Execute declared disciplines in body.**
   - source-traceability, quantitative-role, final-audit actually visible in body execution
   - self-assessment block matches actual execution, not aspirational

4. **Justify the shortlist boundary.**
   - explain why these three forms and not others (e.g., web app, desktop app, API, no-code, physical product)
   - show the exclusion logic

5. **Surface comprehensive hidden burdens.**
   - at minimum: platform risk (store takedown, policy change), payment processing friction, support overhead, privacy/permissions compliance, ongoing maintenance cost, distribution dependency
   - not just the most obvious 1-2 risks

6. **Make aggregation replicable.**
   - show how variables are weighted and combined into ranking
   - provide at least one worked example
   - reader can verify why scores produce this exact ranking order

## Failure signs

Mark this eval as failed if the answer does any of the following:

- comparison/score/estimate tables have no numeric role labels (constrained-choice hard-fail triggered)
- no 7-column Source Register exists (body references without structured register)
- declared source-traceability or quantitative-role disciplines are not executed in body (process-integrity violation)
- shortlist boundary is not justified — reader cannot tell why these three forms were chosen
- hidden operational burdens omit major real-world categories (payment, support, platform risk, compliance)
- aggregation logic is not replicable — reader cannot verify ranking derivation

## Why this eval matters

This case captures a distinct failure level for the constrained-choice route that is not yet covered by existing cases:

| Case | Route | Level | Core failure |
|---|---|---|---|
| indie-game | constrained-choice | Conditional pass | Quant role missing + body citations absent |
| pkm | constrained-choice | Conditional pass | Quant role + source register + aggregation gaps |
| indie-dev (this) | constrained-choice | **Fail** | Quant role missing + no source register + **shortlist boundary unjustified + hidden burdens incomplete + declared disciplines not executed** |

The key escalation from the existing conditional-pass cases:

- Not just "quant role labels are missing in some tables" but **no role labels in any comparison/estimate table**
- Not just "source register has format gaps" but **no structured source register at all** — only `[1]` bibliography
- Not just "aggregation could be clearer" but **no justification for why these three forms were even compared**
- **Declared disciplines not executed** — the route/audit block declares source-traceability and quantitative-role as present, but body execution has neither

This is a **packaging/process-integrity fail** rather than a content fail. The decision quality is near-conditional-pass, but the delivery infrastructure (source register, numeric roles, self-assessment honesty, shortlist boundary) is insufficient for a deliverable research artifact.

Without this eval, the skill could produce reports with good decision reasoning that fail delivery hygiene — a failure mode that becomes increasingly important as the skill strengthens on content quality.

## Current rule verdict

The current rules should catch this as **fail**:

- constrained-choice hard-fail triggered: numeric role labels absent from comparison/score tables
- process-integrity hard-fail triggered: declared source-traceability and quantitative-role not executed in body
- source traceability hard-fail triggered: no 7-column Source Register, body citations not claim-level
- option-selection audit: shortlist boundary not justified, aggregation not replicable

This case guards against **good decision reasoning that cannot pass delivery hygiene**.

## Related evals

- `evals/cases/indie-game-constrained-choice-quantitative-role-case.md` — same route, same numeric role hard-fail, conditional-pass level
- `evals/cases/pkm-constrained-choice-quantitative-role-gap-case.md` — same route, same quantitative role + source register gaps, conditional-pass level
- `evals/cases/creator-platform-constrained-choice-aggregation-logic-gap-case.md` — same route, aggregation not replicable
- `evals/cases/deepseek-competitive-positioning-evidence-label-case.md` — same process-integrity pattern (declared not executed), different route
- `evals/cases/cross-border-ecommerce-market-outlook-self-assessment-case.md` — same self-assessment overconfidence pattern

## Reviewer checklist

- Are numeric role labels present in every comparison/score/estimate table?
- Does a 7-column Source Register exist with body-to-register mappings?
- Are declared disciplines (source-traceability, quantitative-role) actually executed in body?
- Is the shortlist boundary justified (why these three, what was excluded)?
- Are hidden operational burdens comprehensive beyond the obvious 1-2 items?
- Is the aggregation/ranking method replicable (weights, worked example)?
- Does the self-assessment block match actual execution?

## Suggested scoring

- **Pass**: numeric role labels on all tables, complete 7-column Source Register, declared disciplines executed in body, shortlist boundary justified, hidden burdens comprehensive, aggregation replicable, self-assessment honest
- **Conditional pass**: decision architecture correct, ranking clear, reversal conditions present, but numeric role labels partial, source register has format gaps, aggregation described but not fully replicable, or self-assessment slightly off — no process-integrity violation
- **Fail**: numeric role labels entirely absent (hard-fail), no structured source register, declared disciplines not executed in body (process-integrity violation), shortlist boundary not justified, hidden burdens incomplete, or aggregation not replicable
