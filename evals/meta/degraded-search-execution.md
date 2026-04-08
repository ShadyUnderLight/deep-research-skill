# Eval: Degraded Search Execution

Use this eval when live-search fallback was needed and you need to judge whether degraded discovery was handled explicitly and intelligently rather than mechanically.

## Goal

Distinguish between:

1. fallback policy exists on paper
2. fallback execution actually improved the research path

A skill can have a reasonable fallback ladder and still execute it poorly through provider churn, weak query-fit judgment, or poor logging.

---

## Typical failure patterns

- provider fallback happens, but the trigger is not recorded clearly
- Exa is used even when the query obviously needs localized browser-side discovery
- Bing is used only because it is next in sequence, not because it is a better fit
- fallback search returns noisy candidates, but the search objective is not tightened
- degraded-search path is used, but the evidence log does not preserve what was tried and what remained unverified
- result pages are implicitly treated as evidence instead of discovery-only candidate lists

---

## What this eval is testing

### Failure Mode 1: Mechanical fallback

The workflow changes provider because a ladder exists, not because the switch was justified.

Examples:
- Exa -> Bing -> more Bing-like browsing without explaining why the search intent changed
- switching provider after weak results without identifying whether the problem was query-fit, low-yield, or provider failure
- escalating providers when the better next move would have been to tighten the objective or query shape first

### Failure Mode 2: Query-fit misfire

The chosen fallback does not match the search objective.

Examples:
- technical-doc query forced into browser-localized search first
- localized Chinese news-flow task forced through Exa as if it were the default best path
- dynamic page need misdiagnosed as search-provider weakness

### Failure Mode 3: Weak degraded-search logging

Fallback may have been reasonable, but the research state no longer preserves what happened.

Examples:
- no record of which provider path was attempted
- no distinction between provider failure, rate-limit pressure, and low-yield results
- no note of what still required primary-page verification

---

## Pass criteria

A good degraded-search workflow should:

1. record why fallback was triggered
2. choose fallback path based on query-fit, not only sequence order
3. keep result pages in the discovery layer rather than treating them as memo evidence
4. stop escalation when additional provider churn is unlikely to add decision-relevant value
5. preserve degraded-search state in a compact log or recoverable process artifact

---

## Scoring guide

Use a simple 0-2 scale.

### 0 = poor degraded-search execution
- fallback path was mechanical, noisy, or poorly logged

### 1 = partially disciplined fallback
- fallback choice was somewhat justified, but query-fit or logging discipline remains weak

### 2 = strong degraded-search execution
- fallback was explicitly triggered, fit-matched, efficiently bounded, and recoverably logged

---

## Review questions

When using this eval, ask:

- Why was the primary provider insufficient: failure, quota, query-fit, or low-yield?
- Did the chosen fallback actually match the search objective better?
- Were result pages kept as discovery-only rather than treated as evidence?
- Should the workflow have stopped, tightened the query, or switched tools instead of escalating providers?
- Is the degraded-search state recoverable from notes, logs, or the Research Pack?

---

## Output format for reviewers

When you apply this eval, summarize the result as:

- **Search objective:**
- **Primary provider outcome:**
- **Fallback trigger:**
- **Fallback path used:**
- **Why that path was or was not a good fit:**
- **What remained unverified after fallback:**
- **Diagnosis:** mechanical fallback / query-fit misfire / weak degraded-search logging / strong degraded-search execution
- **Best next fix:** SKILL fallback hardening / log-shape hardening / query-fit guidance / stop-condition hardening

---

## Why this eval exists

As fallback policy becomes clearer, the next failure mode is no longer missing policy but weak execution. This eval exists to pressure-test whether degraded search actually improves the research path or just makes the process look more sophisticated.
