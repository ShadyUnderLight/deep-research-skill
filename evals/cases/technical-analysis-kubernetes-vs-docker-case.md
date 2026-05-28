# Eval: Technical Deep-dive — Kubernetes vs Docker Swarm Architecture Comparison

## Goal

Test whether the skill correctly activates the **technical deep-dive** route for an architecture comparison task, and produces a report that satisfies the technical analysis artifact contract.

This eval validates the new technical deep-dive routing added in response to issue #116.

## Prompt

Compare the architectures of Kubernetes and Docker Swarm for container orchestration. Focus on:

- core architectural differences
- scaling characteristics
- operational complexity
- ecosystem maturity
- when to choose one over the other

## What this eval is testing

- whether the technical deep-dive route is correctly activated (not constrained choice or equipment selection)
- whether the report uses explicit comparison dimensions
- whether the comparison is dimension-by-dimension, not just a feature list
- whether the report makes a judgment, not just a survey
- whether technical state is current (versions, capabilities)
- whether trade-offs are stated, not just advantages

## Route activation criteria

The technical deep-dive route should activate because:

- the core question is about **architectural principles and trade-offs**
- the task is not about selecting a product to deploy (that would be constrained choice)
- the task is not about purchasing hardware (that would be equipment selection)
- the task is not about market evolution (that would be market outlook)

If the report structure looks like a "choice memo" recommending one option, the wrong route fired.

If the report structure looks like a "technical comparison with judgment," the correct route fired.

## Pass criteria

A good answer should:

### 1. Activate the correct route
- explicitly classify this as a technical architecture comparison
- not default to constrained choice or generic research

### 2. Use explicit comparison dimensions
- define comparison dimensions upfront (e.g., architecture, scaling, operations, ecosystem, flexibility)
- each dimension has clear criteria
- the report covers at least 4 dimensions

### 3. Provide dimension-by-dimension analysis
- each dimension gets its own analysis section
- both architectures are compared within each dimension
- trade-offs are stated, not just "Kubernetes is better at X"

### 4. Make a technical judgment
- the report recommends when to choose one over the other
- the recommendation is conditional (under what constraints each wins)
- the report does not just list features

### 5. Use current technical state
- current versions are cited
- current ecosystem state is described
- deprecated or superseded features are not presented as current

### 6. Satisfy the artifact contract
The report should visibly show:
- candidate architectures (Kubernetes, Docker Swarm)
- explicit comparison dimensions
- dimension-by-dimension analysis
- trade-off summary
- conditional recommendation (when to choose which)

## Failure signs

Mark this eval as failed if the answer does any of the following:

- activates constrained choice or equipment selection instead of technical deep-dive
- compares architectures without explicit dimensions
- provides a feature list instead of dimension-by-dimension analysis
- makes an unconditional recommendation without stating trade-offs
- uses stale technical state (old versions, deprecated features)
- treats vendor claims as confirmed technical facts
- produces a pure survey without judgment
- looks like a "choice memo" rather than a "technical comparison"

## Why this eval matters

This is a high-value regression test because it catches a common routing failure:

- the task sounds like it could be "constrained choice" (choosing between two options)
- but the real question is about **understanding architectural trade-offs**, not selecting a product
- if the wrong route fires, the report structure will be wrong (recommendation-first vs. analysis-first)

If the skill cannot pass this eval, the technical deep-dive route is not yet reliable.

## Reviewer checklist

Use this quick checklist after a run:

- Did it activate the technical deep-dive route?
- Did it define explicit comparison dimensions?
- Did it analyze each dimension separately?
- Did it state trade-offs, not just advantages?
- Did it make a conditional recommendation?
- Did it use current technical state?
- Does the report look like a technical comparison, not a choice memo?

## Suggested scoring

- Pass: route activation correct, dimensions explicit, analysis dimension-by-dimension, judgment conditional
- Partial: route activation correct but analysis is shallow or dimensions are implicit
- Fail: wrong route activated, or report is a feature list without judgment

---

## Related evals

- `evals/comparative-distillation/api-supplier-selection-gpt-vs-minimax-comparative-distillation.md` — tests provider selection routing
- `evals/comparative-distillation/multi-origin-meetup-city-selection-gpt-vs-minimax-comparative-distillation.md` — tests constrained choice routing

## Related references

- `references/technical-analysis-discipline.md` — the discipline file for this route
- `ROUTING-MATRIX.md` — the route definition
