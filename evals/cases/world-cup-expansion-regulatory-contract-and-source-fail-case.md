# Eval: World Cup Expansion — Regulatory Contract Execution and Source Traceability Fail Case

## Goal

Test whether a report that **correctly self-declares its route** (regulatory/policy impact analysis + rule-system add-on) can still fail hard when:

- **regulatory route contract is not executed** — missing pending/current separation, enforcement reality, three scenarios, actionable monitoring signals despite correct route declaration
- **rule-system add-on declared but not executed** — state taxonomy absent, intervention matrix is a flat alternatives table without side effects/monitoring indicators/reversal conditions
- **source traceability hard-fail** — body has zero `[Sxx]` claim-level citations; `[CONF]/[INFER]` used as proxy for source traceability
- **source-strength gate fail** — 8/9 appendix sources are Wikipedia/crowdsourced, only S08 is FIFA official; load-bearing claims about FIFA rules, qualification slots, and statistical data rely on tertiary sources
- **self-assessment overclaim triggers process-integrity hard-fail** — claims all disciplines (workflow, route, regulatory, source traceability, final audit) passed while body execution contradicts every one
- **declared-not-executed hard-fail** — source-traceability, regulatory-contract, and add-on disciplines claimed ✅ but zero body execution evidence

This eval is based on a real report: a 2026 World Cup expansion analysis that correctly identified the core question (fairness vs match quality trade-off), used strong opening judgment, included counter-evidence, and declared the correct route — but satisfied neither the route's artifact contract nor the add-on's requirements, while claiming all disciplines passed.

## Prompt

Analyze the impact of the 2026 World Cup expansion from 32 to 48 teams on global fairness and group-stage competitive quality. Include current rules, counter-evidence, and uncertainty.

## What this eval is testing

- whether correct route self-declaration is sufficient when the route's artifact contract is not executed
- whether `[CONF]/[INFER]` confidence/inference tags are correctly rejected as substitutes for claim-level `[Sxx]` source citations
- whether Wikipedia-dominated source registers (8/9 tertiary, 1/9 official) trigger source-strength gate failure independent of citation format
- whether rule-system add-on declaration without state taxonomy and qualified intervention matrix triggers add-on execution hard-fail
- whether self-assessment claiming all ✅ when regulatory contract, source traceability, and add-on are all unexecuted triggers process-integrity and declared-not-executed hard-fails
- whether metadata-first self-assessment (checkmark parade without body evidence) is caught

## Pass criteria

A passing answer should:

1. **Execute the regulatory route contract.** Must include: current regulatory snapshot (expansion rules as enacted), pending/not-applicable policy declaration, enforcement reality (FIFA decision-making, scheduling constraints, supervision), direct vs indirect impact separation, at minimum three scenarios (optimistic/base/pessimistic), monitoring signals with threshold/cadence/source/trigger-to-action, and stakeholder action guidance.

2. **Execute the rule-system add-on contract.** Must include: state taxonomy (classification of rule elements and their interaction types), qualified intervention matrix (alternative → mechanism → side effects → monitoring indicators → reversal conditions).

3. **Execute body-level `[Sxx]` traceability.** Every load-bearing factual claim must have an inline citation. `[CONF]/[INFER]` tags are not valid substitutes.

4. **Pass source-strength gate.** Load-bearing claims about FIFA rules, qualification slots, and statistical data require primary/official sources, not Wikipedia or crowdsourced aggregators. A Source Register dominated by tertiary sources fails independent of citation format.

5. **Keep self-assessment honest.** Audit status must reflect actual contract execution, not route declaration correctness alone.

## Failure signs

Mark this eval as failed if the answer does any of the following:

- declares the correct regulatory route but fails to execute its contract (missing scenarios, enforcement reality, monitoring signals, pending/current separation)
- declares rule-system add-on but produces a flat alternatives table without state taxonomy or qualified intervention matrix
- body has no `[Sxx]` claim-level citations while self-assessment claims source-traceability pass
- uses `[CONF]/[INFER]` as body-level traceability and claims this satisfies source-traceability requirements
- Source Register is heavily Wikipedia/crowdsourced (≥80% tertiary sources) for load-bearing claims requiring official sources
- self-assessment claims regulatory/rule-system/source-traceability all passed when none are executed at body level
- declared-not-executed gate fires on claimed disciplines

## Why this eval matters

This case adds a **route-declaration-correct, contract-execution-absent** dimension not covered by existing regulatory cases:

| Case | Route declaration | Contract execution | Add-on |
|---|---|---|---|
| World Cup rule route mismatch | ❌ Wrong (Shared-workflow) | ❌ Regulatory not executed | N/A |
| EU DMA scenario gaps | ✅ Regulatory | ⚠️ Partial (scenarios weak) | N/A |
| Rule-system add-on activation | N/A | N/A | ✅ Tests activation trigger |
| **World Cup expansion (this)** | **✅ Correct (regulatory + add-on)** | **❌ Not executed** | **❌ Declared, not executed** |

The unique contributions:

- **Route declaration correctness is not a shield** — the report correctly identified regulatory as the natural route and declared it, but this correct identification did not translate into contract execution. Previous route cases test misidentification; this case tests identification-without-execution.
- **`[CONF]/[INFER]` as false traceability** — the report uses confidence/inference tags as body-level annotations and treats them as equivalent to source citations. This is a new variant of traceability theatre: the body has annotation infrastructure, but the infrastructure traces to confidence levels and inference chains, not to sources.
- **Add-on declaration without execution** — the report declares rule-system add-on (correct for tournament mechanism analysis) but the "intervention matrix" is a flat alternatives evaluation table without state taxonomy, side effects, monitoring indicators, or reversal conditions. This tests the gap between add-on activation awareness and add-on contract execution.
- **Wikipedia dominance as independent hard-fail** — even if `[Sxx]` citations were added, the source pool itself (8/9 tertiary) would fail source-strength gate for load-bearing claims about official FIFA rules. This tests source-strength as a dimension independent of citation format.

## Current rule verdict

- **Fail**: regulatory route contract not executed (hard-fail on scenarios, enforcement reality, monitoring signals)
- **Fail**: rule-system add-on not executed (hard-fail on state taxonomy, intervention matrix)
- **Fail**: source traceability hard-fail (zero `[Sxx]`, `[CONF]/[INFER]` used as proxy)
- **Fail**: source-strength gate fail (8/9 Wikipedia/crowdsourced for load-bearing official claims)
- **Fail**: process-integrity hard-fail (self-assessment overclaim with multiple unexecuted disciplines)
- **Fail**: declared-not-executed hard-fail (source-traceability, regulatory-contract, add-on all claimed ✅, zero body execution)

## Related evals

- `evals/cases/world-cup-rule-regulatory-route-mismatch-case.md` — same topic domain, different failure: route declaration mismatch (declared Shared-workflow, actual regulatory) vs. this case (declared correct route, contract not executed)
- `evals/cases/agent-api-market-outlook-full-spectrum-fail-case.md` — same pattern of 100% register inflation + self-assessment overclaim, different route
- `evals/cases/rule-system-add-on-activation-case.md` — tests add-on activation trigger; this case tests add-on declared-but-not-executed
- `evals/cases/dc-power-market-outlook-inflation-and-monitoring-case.md` — same monitoring non-actionability pattern, different route
- `evals/cases/advantech-listed-company-traceability-hard-fail-case.md` — same source-traceability hard-fail + self-assessment overclaim pattern, different route

## Reviewer checklist

- Is the regulatory route contract executed (snapshot, pending/current, enforcement, scenarios, monitoring)?
- Is the rule-system add-on contract executed (state taxonomy, qualified intervention matrix)?
- Does the body have `[Sxx]` claim-level citations (not `[CONF]/[INFER]` as proxy)?
- Is the source pool appropriate for load-bearing claims (official sources for FIFA rules, not Wikipedia)?
- Does self-assessment match actual body execution (not just route declaration correctness)?

## Scoring

- **Pass**: regulatory contract fully executed, add-on contract satisfied, body `[Sxx]` present, source pool meets strength requirements, self-assessment honest
- **Conditional pass**: content analysis strong, correct route declared, but contract partially executed (e.g., scenarios exist but monitoring signals lack full actionability), traceability present but thin — no process-integrity hard-fail
- **Fail** (this case's level): correct route declared but contract not executed, add-on declared but not executed, zero body `[Sxx]`, Wikipedia-dominated sources, self-assessment overclaim triggers hard-fails
