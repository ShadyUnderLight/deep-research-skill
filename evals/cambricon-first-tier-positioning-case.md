# Eval: Cambricon First-Tier Positioning Discipline Case

## Goal

Test whether the skill handles `first-tier` / `top-tier` / competitive-positioning questions with enough definition discipline when the company has mixed evidence across technology, commercial traction, ecosystem maturity, and capital-markets signaling.

This eval is based on a real failure mode: the report looked rigorous because it defined multiple dimensions and used labels like confirmed fact / inference / open uncertainty, but it still collapsed uneven evidence into a polished overall tier conclusion that was not fully auditable.

## Prompt

Assess whether Cambricon can reasonably be considered a global first-tier AI-chip player.

Method requirements:
- do not use `first-tier` loosely
- define the judgment dimensions separately
- at minimum evaluate:
  - technical capability
  - product adoption / commercial traction
  - ecosystem strength
  - capital-markets or financing position when relevant
- before any ranking-style conclusion, define scope, metric, and timeframe
- do not collapse multiple dimensions into one fuzzy total label
- if evidence strength differs by dimension, make that visible
- distinguish direct evidence from inference
- distinguish confirmed facts, inference, and open uncertainty
- attach sources

## What this eval is testing

- whether the model treats `first-tier` as a definition-sensitive classification rather than a prestige adjective
- whether it makes scope / metric / timeframe load-bearing instead of decorative
- whether it keeps dimension-level judgments visible when evidence strength differs
- whether it prevents valuation, regional strength, roadmap signals, or self-tested performance claims from silently standing in for current global commercial/technical leadership
- whether it avoids compressing mixed evidence into a clean but weakly justified overall label

## Pass criteria

A good answer should:

1. Define the classification frame before judging.
   - specify geography, product scope, and time basis
   - state what dimensions matter and why
   - explain whether an overall label is even appropriate

2. Keep dimensions separate.
   - give distinct conclusions for technical capability, traction, ecosystem, and capital-markets position
   - avoid blending `strong in one dimension` into `overall first-tier` without a visible rule

3. Weight evidence types honestly.
   - separate official specs, company financials, third-party market data, self-tests, customer anecdotes, media reporting, and inference
   - reduce certainty when critical claims rely on inference or indirect evidence

4. Avoid false globality.
   - distinguish China-market leadership or strategic importance from global first-tier status
   - separate current in-production products from roadmap / next-generation products

5. Make uncertainty decision-relevant.
   - identify what missing evidence would change the classification
   - if overall tier language is retained, state why the compression is still justified despite uneven evidence

## Failure signs

Mark this eval as failed if the answer does any of the following:

- says `global first-tier` or similar without a visible rule for what that means
- defines dimensions up front but still collapses them into one prestige label without showing the aggregation logic
- treats regional strength, valuation, or financing ability as if they directly prove current global product/ecosystem standing
- relies heavily on self-tested benchmarks, media-reported roadmap claims, or inferred performance ranges while still sounding highly certain
- compares players with different scopes or market roles under one blended tier label without narrowing the comparison unit

## Why this eval matters

This catches a specific failure family that sits between ordinary ranking drift and generic company-analysis weakness.

A report can look structured and still fail because:

- it uses `first-tier` as a vague umbrella term
- it mixes global and domestic frames
- it mixes current products and future roadmap
- it mixes direct evidence and inference with too little weighting discipline
- it creates confidence theater by presenting a neat overall classification that the evidence does not fully support

If the skill cannot pass this eval, it is still too vulnerable to polished but weakly-auditable positioning memos.

## Reviewer checklist

- Did it define scope, metric, and timeframe before using tier language?
- Did it keep dimension-level judgments visible?
- Did it separate direct evidence from inference in the load-bearing claims?
- Did it distinguish China-market strength from global first-tier status?
- Did it avoid letting roadmap, valuation, or self-tests do too much work in the final classification?

## Suggested scoring

- Pass: the classification is definition-driven, dimension-specific, and honest about evidence role
- Partial: some discipline is visible, but overall-label compression still feels too easy
- Fail: the answer materially overstates confidence in a `first-tier` / `top-tier` classification
