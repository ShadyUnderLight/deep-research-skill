# Eval: Private Company / Startup Evaluation — Anthropic Company Assessment

## Goal

Test whether the skill correctly activates the **private company / startup evaluation** route for a startup company assessment task, and produces a report that satisfies the private company artifact contract.

This eval validates the new private company / startup evaluation routing added in response to issue #121.

## Prompt

Analyze Anthropic as a private company. Focus on:

- company overview and current stage
- founding team and key leadership
- product and PMF signals (Claude, API business)
- funding history and valuation trajectory
- competitive positioning vs OpenAI, Google, Meta
- key strengths and risks
- 12-24 month outlook

## What this eval is testing

- whether the private company route is correctly activated (not listed-company or first-tier positioning)
- whether the report avoids listed-company valuation methods (PE, PB, DCF)
- whether founder-sourced claims are labeled as issuer-sourced
- whether PMF signals are grounded in available evidence
- whether source reliability levels are explicit
- whether the artifact contract is satisfied

## Route activation criteria

The private company route should activate because:

- Anthropic is a **private, unlisted company**
- the core question is about **evaluating a non-public company's state and prospects**
- the task is not about listed-company investment analysis (no public market data)
- the task is not about competitive positioning ranking (that would be first-tier / competitive positioning)

If the report uses PE/PB/PS/DCF as primary valuation framing, the wrong route fired.

If the report uses funding round valuation and comparable transactions, the correct route fired.

## Pass criteria

A good answer should:

### 1. Activate the correct route
- explicitly classify this as a private company evaluation
- not default to listed-company or generic research

### 2. Avoid listed-company valuation methods
- does not use PE, PB, PS, or DCF as primary framing
- uses latest round valuation, comparable transactions, or revenue multiples
- labels valuation as "latest round valuation" not "company value"

### 3. Label source reliability
- founder-sourced claims labeled as issuer-sourced
- Crunchbase/PitchBook data labeled as aggregator estimates
- media coverage treated as discovery, not evidence
- social media labeled as weak supplemental signal

### 4. Assess PMF signals with evidence
- distinguishes user growth from paid growth from revenue growth
- labels metrics by source type (company-reported / estimated / inferred)
- states explicitly when PMF data is unavailable

### 5. Evaluate team as primary variable
- founders and key leadership identified with background
- track record noted (prior exits, domain experience)
- claims about team quality sourced, not promotional

### 6. Satisfy the artifact contract
The report should visibly show:
- company overview and stage positioning
- team assessment
- product and PMF signals
- market and competitive position
- funding and financial overview (labeled by source type)
- key strengths and risks (specific to this company)
- 12-24 month milestones
- judgment and recommendation (with explicit uncertainty bounds)

## Failure signs

Mark this eval as failed if the answer does any of the following:

- activates listed-company route instead of private company route
- uses PE/PB/PS/DCF as primary valuation framing
- treats unverified founder claims as confirmed facts
- does not label source reliability levels
- presents weak or absent financial data as if comparable to audited public-company disclosures
- writes as a mini listed-company analysis with data gaps hidden
- uses `唯一` / `only` / `first` / `领先` wording without evidence
- produces a generic company overview without private-company-specific assessment

## Why this eval matters

This is a high-value regression test because it catches a common routing failure:

- the task sounds like it could be "listed-company investment research" (company analysis)
- but the real question is about **evaluating a private company with different evidence constraints**
- if the wrong route fires, the report will try to find non-existent public market data and use inappropriate valuation methods

If the skill cannot pass this eval, the private company route is not yet reliable.

## Reviewer checklist

Use this quick checklist after a run:

- Did it activate the private company route?
- Did it avoid PE/PB/PS/DCF as primary framing?
- Did it label source reliability levels?
- Did it assess PMF signals with evidence?
- Did it evaluate team as a primary variable?
- Does the artifact contract sections appear in the report?
- Does the report look like a startup evaluation, not a listed-company memo?

## Suggested scoring

- Pass: route activation correct, valuation appropriate, sources labeled, artifact contract satisfied
- Partial: route activation correct but analysis is shallow or sources not labeled
- Fail: wrong route activated, or report uses listed-company methods for private company

---

## Related evals

- `evals/cases/minimax-company-report-case.md` — tests listed-company routing for a recently-IPO'd company
- `evals/cases/moore-threads-listing-status-case.md` — tests listing-state awareness

## Related references

- `references/startup-evaluation-discipline.md` — the discipline file for this route
- `checklists/startup-company-report.md` — the checklist for this route
- `ROUTING-MATRIX.md` — the route definition
