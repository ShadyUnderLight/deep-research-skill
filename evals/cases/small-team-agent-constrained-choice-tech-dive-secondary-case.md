# Eval: Small Team AI Agent Decision — Constrained Choice with Technical Deep-Dive Secondary Case

## Goal

Test whether a Constrained Choice / Shortlist report with clear ranking (unified > hybrid > separate), decision architecture, reversal conditions, and runner-up credibility can still **fail strict delivery** when:

- **Technical Deep-Dive declared as secondary route without independent hard-fail verification** — platform capability/price comparisons (the secondary route's subject) lack current-state snapshot, vendor claim caveats, and benchmark methodology
- **body-level source traceability absent** — zero `[Sxx]` inline citations; source list is not a 7-column Source Register
- **numeric role labels absent** — star ratings, Token multiples, monthly costs, FTE savings, implementation timelines lack observed/proxy/assumption/model-output roles; triggers constrained-choice hard-fail
- **aggregation logic not replicable** — 5 variables listed without weights, scoring rules, or worked example
- **self-assessment claims all ✅ while traceability, numeric roles, secondary route, and aggregation all have gaps** — triggers process-integrity and declared-not-executed hard-fails
- **platform/price data lacks current-state snapshot** — AI Agent platform capabilities and pricing change rapidly; the comparison has no dated snapshot or verification method

This eval is based on a real report: a small-team AI Agent unification decision memo that correctly activated the constrained-choice route, provided a clear three-option ranking (unified > hybrid > separate) with decision architecture, load-bearing variables, reversal conditions, and actionable next steps — but failed on the intersection of constrained-choice delivery requirements (numeric roles, traceability, replicable method) AND the declared Technical Deep-Dive secondary route (current-state snapshot, vendor claims, benchmark methodology).

## Prompt

A small team needs to decide whether to unify customer service, operations, and data analysis into a single AI Agent, keep them separate, or use a hybrid approach. Produce a structured decision memo that:

- defines the decision frame (team size, budget, technical capability, compliance requirements)
- states the shortlist (unified / hybrid / separate) with justification — why these three and what was excluded
- provides a replicable comparison framework with weighted variables, scoring rules, and at least 1 worked example
- gives a clear ranking with why top option wins, why runner-up is credible, and why rejected option fails
- identifies ranking-reversal conditions and hidden operational burdens
- includes platform capability/price comparisons with a **current-state snapshot** (dated, sourced, with refresh date) — do not use undated price/feature claims
- if declaring Technical Deep-Dive as secondary route (for platform capability analysis), runs and reports its hard-fail verification: current-state verification, vendor/manufacturer claim caveats, benchmark methodology, and comparison dimension load-bearing labels
- uses `[Sxx]` inline citations throughout
- includes a complete 7-column Source Register
- labels all comparison/estimate numbers with observed/proxy/assumption/model-output roles

## What this eval is testing

- whether Technical Deep-Dive secondary route hard-fail is independently verified when declared from a constrained-choice primary — vendor claims, current-state snapshot, benchmark methodology
- whether constrained-choice numeric role hard-fail is applied to decision numbers (costs, token estimates, FTE savings, timelines)
- whether body-level source traceability is executed
- whether aggregation logic is replicable (weights, scoring rules, worked example)
- whether platform/price data has a current-state snapshot with refresh date — rapidly changing data without a temporal anchor creates stale-decision risk
- whether self-assessment accuracy reflects gaps across both primary and secondary routes

## Pass criteria

A passing answer should:

1. **Verify declared Technical Deep-Dive secondary route independently.** List and satisfy: current-state snapshot (dated platform/price table with refresh date), vendor/manufacturer claim caveats (platform docs ≠ independent verification), benchmark methodology (performance/cost claims with workload, setup, date), and load-bearing comparison dimensions (state which dimensions drive the capability assessment).

2. **Execute body-level `[Sxx]` traceability.** Every key claim in exec summary, variable table, ranking, platform comparison, reversal conditions, and action plan has an inline citation.

3. **Label numeric roles on all comparison/estimate numbers.** Costs, token multiples, FTE savings, implementation timelines, star ratings — all labeled as observed/proxy/assumption/model-output.

4. **Make aggregation replicable.** Show how variable scores combine into ranking — weights, scoring rules, at least 1 worked example.

5. **Provide current-state snapshot for quickly-changing data.** Platform pricing, capability, and API cost data must have a snapshot date and expected refresh cadence.

6. **Keep self-assessment honest.** Audit status must reflect gaps across primary route (constrained-choice) and secondary route (technical-deep-dive).

## Failure signs

Mark this eval as failed if the answer does any of the following:

- Technical Deep-Dive secondary route declared but its hard-fail items are not independently verified
- body has zero `[Sxx]` inline citations (source traceability hard-fail)
- comparison/estimate numbers lack numeric role labels (constrained-choice hard-fail)
- aggregation method is not replicable (no weights, rules, or worked example)
- platform/price data has no current-state snapshot date
- self-assessment claims all ✅ while primary or secondary route gaps exist (process-integrity hard-fail)

## Why this eval matters

Constrained-choice cases with technical-content secondary routes create a **dual-discipline delivery requirement**. The primary route demands numeric role labels, traceability, and replicable aggregation. The secondary Technical Deep-Dive route demands current-state snapshots, vendor claim caveats, and benchmark methodology. A report that satisfies neither fails two delivery contracts at once:

| Case | Primary route | Secondary route | Method gap |
|---|---|---|---|
| Programming language | constrained-choice | Market Outlook (unnecessary) | Secondary route unnecessary, not verified |
| World Cup prediction | constrained-choice | None | Probability method |
| Small team agent (this) | **constrained-choice** | **Technical Deep-Dive** | **Both: constrained-choice roles/aggregation + tech-dive current-state/vendor claims** |

The unique contributions:

- **Dual-discipline intersection** — the technical-deep-dive secondary route requires a current-state snapshot for rapidly-changing platform data (pricing, API costs, capability updates). This is a specific delivery requirement when constrained-choice reports include technology platform comparisons.
- **Technical Deep-Dive as secondary from constrained-choice primary** — this is the first case testing this specific route combination. The secondary route hard-fail items differ from Market Outlook or Provider Selection.
- **Platform data temporal anchor** — AI Agent platform pricing/capability is fast-moving. An undated comparison creates stale-decision risk.

## Current rule verdict

- Constrained-choice hard-fail: numeric role labels absent, aggregation not replicable
- Source traceability hard-fail: zero body `[Sxx]`
- Secondary route hard-fail: Technical Deep-Dive declared but not verified
- Process-integrity hard-fail: self-assessment claims all ✅ while gaps exist
- Current-state: platform/price data lacks snapshot date

## Related evals

- `evals/cases/programming-language-constrained-choice-shortlist-contradiction-case.md` — same route, unnecessary secondary route (Market Outlook)
- `evals/cases/world-cup-prediction-constrained-choice-probability-method-case.md` — same route, probability method empty
- `evals/cases/indie-dev-constrained-choice-delivery-fail-case.md` — same route, delivery fail
- `evals/cases/agentic-rag-technical-deep-dive-compounded-case.md` — same technical-deep-dive vendor claim pattern, different primary route
- `evals/cases/china-data-export-regulatory-secondary-route-case.md` — same secondary route verification pattern, different routes

## Reviewer checklist

- Is the declared Technical Deep-Dive secondary route independently verified?
- Does the body have `[Sxx]` inline citations?
- Do comparison/estimate numbers have numeric role labels?
- Is aggregation replicable (weights, scoring rules, worked example)?
- Does platform/price data have a current-state snapshot date?
- Does self-assessment match body execution?

## Suggested scoring

- **Pass**: secondary route verified, body `[Sxx]` present, numeric roles on all numbers, aggregation replicable, platform data dated, self-assessment honest
- **Conditional pass**: constrained-choice structure strong, ranking clear, reversal conditions present, but secondary route verification thin, or numeric roles on most but not all key numbers, or aggregation described directionally, or self-assessment slightly optimistic — no hard-fail triggered
- **Fail**: secondary route declared but not verified (hard-fail), or body zero `[Sxx]` (traceability hard-fail), or numeric roles absent (constrained-choice hard-fail), or aggregation not replicable, or platform data lacks snapshot date, or self-assessment claims all ✅ while gaps exist (process-integrity hard-fail)
