# Eval: World Cup Sports Broadcasting — Market Outlook Source Strength and Monitoring Actionability Case

## Goal

Test whether a structurally strong market-outlook report — with complete snapshot, drivers/blockers, three scenarios, stakeholder table, and body-level `[Sxx]` citations — can still **fail hard delivery gates** when:

- **source pool is Wikipedia/crowdsourced-heavy** — body has `[Sxx]` inline citations (unlike zero-citation cases), but the cited sources are predominantly Wikipedia and media secondary sources, not official financial reports, audited statements, or industry data. Load-bearing claims about FIFA revenue, platform investment, and market valuations cite tertiary sources.
- **evidence labeling inconsistent with source strength** — secondary/crowdsourced sources are tagged as confirmed facts, inflating evidence weight above what the actual sources can bear
- **monitoring signals non-actionable** — 7 reversal signals listed qualitatively, but none meet the 4-field actionability requirement (threshold + cadence + source + trigger-to-action)
- **forward-looking numbers without sourcing or role labels** — scenario probabilities `~60/25/15%`, revenue thresholds `>40%`, `<$1B`, `>15%` stated precisely but lack estimation method, named source, or numeric role labels
- **scenarios not bound to shared quantitative axis** — base/bull/bear scenarios exist but drift across different metrics (revenue, viewership, platform competition) rather than being tied to a single load-bearing variable
- **self-assessment overclaim** — source-traceability, market-outlook, forward-looking, and final-audit all claimed ✅ while source-strength gate fails, monitoring hard-fail triggers, and forward-looking numbers lack sourcing

This eval is based on a real report: a 2026 World Cup sports broadcasting market outlook that correctly structured as market-outlook, included strong counter-evidence and stakeholder action table, and achieved body-level `[Sxx]` traceability — but still failed on source quality, monitoring actionability, and forward-looking precision gates. It serves as the **conditional-pass benchmark** for structurally sound market-outlook execution with gate-level failures.

## Prompt

Can broadcasting rights holders and streaming platforms use the 2026 World Cup to prove that live sports remains a high-value asset?

## What this eval is testing

- whether body-level `[Sxx]` citations are sufficient when the underlying source pool is Wikipedia/crowdsourced (traceability present, source strength absent)
- whether evidence labels (confirmed fact / inference / unknown) are correctly calibrated against actual source types — not just present/absent
- whether monitoring signals that are qualitatively correct but lack threshold/cadence/source/trigger-to-action trigger the market-outlook monitoring hard-fail
- whether forward-looking numbers with precise percentages (`~60%`, `>40%`, `<$1B`) without method, role labels, or assumption chains are flagged
- whether scenarios not bound to a shared quantitative axis fail the structured-scenario gate
- whether self-assessment claims all ✅ when monitoring actionability, source strength, and forward-looking precision all fail independently

## Pass criteria

A passing answer should:

1. **Pass source-strength gate.** Load-bearing claims about FIFA revenue, platform financials, and market valuations require primary sources (official financial reports, audited statements, industry data), not Wikipedia or news media. Body `[Sxx]` citations are necessary but not sufficient — the cited sources must be appropriate for their claims.

2. **Calibrate evidence labels to source strength.** Secondary/crowdsourced sources should not be tagged as confirmed facts. Evidence labels must reflect actual source reliability, not just claim confidence.

3. **Execute monitoring signal actionability.** At minimum 3 monitoring signals must include threshold, cadence, source, and trigger-to-action. Qualitative reversal lists without operational fields do not satisfy the market-outlook monitoring contract.

4. **Source forward-looking numbers.** Scenario probabilities, revenue thresholds, and growth rates must include estimation method, named source, or explicit assumption chain. Role labels (observed / estimate / scenario-assumption / model-output) must be applied.

5. **Bind scenarios to shared axis.** Base/bull/bear scenarios must be anchored to the same load-bearing quantitative variable, with each scenario represented as a deviation along that axis.

6. **Keep self-assessment honest.** Audit status must reflect actual gate execution, not structural completeness alone.

## Failure signs

Mark this eval as failed if the answer does any of the following:

- body has `[Sxx]` citations but cited sources are predominantly Wikipedia/crowdsourced for load-bearing claims (source-strength gate fail)
- evidence labels tag secondary/crowdsourced claims as confirmed facts (label-source mismatch)
- monitoring signals are purely qualitative with zero actionable signals meeting 4-field requirement (monitoring hard-fail)
- scenario probabilities are precise percentages without method, role labels, or assumption chain
- scenarios drift across different metrics rather than binding to a shared quantitative axis
- self-assessment claims source-traceability/market-outlook/forward-looking/final-audit all passed when multiple gates fail independently

## Why this eval matters

This case adds a **structurally-sound, gate-level-fail** dimension to the market-outlook eval family:

| Case | Body [Sxx] | Source pool | Monitoring | Scenarios | Self-assessment |
|---|---|---|---|---|---|
| Agent API full-spectrum | ❌ Zero | 5-col register | Zero actionable | No method | ❌ All ✅ |
| DC power inflation | ⚠️ Partial (16/33) | 7-col, >50% inflation | Structure, no action | Present | ❌ Overclaim |
| AI video label gap | ❌ Weak | Present | N/A | No method | ❌ Overclaim |
| **Sports broadcasting (this)** | **✅ Present** | **Heavy Wikipedia** | **Qualitative, no actionability** | **3 scenarios, unanchored** | **❌ Overclaim** |

The unique contributions:

- **Citation format vs. source quality** — this is the first market-outlook case where body `[Sxx]` citations exist but the source pool itself is the problem. Previous cases tested citation absence; this case tests citation presence with inadequate sources. Having `[Sxx]` does not automatically pass source traceability if the `[Sxx]` point to Wikipedia.
- **Evidence label calibration** — the report uses evidence labels (confirmed fact / inference / unknown) but assigns labels inconsistently with actual source types. A claim backed by Wikipedia should not be tagged as confirmed fact. This extends the evidence-label-inflation family to market-outlook, previously concentrated in listed-company and competitive-positioning.
- **Structurally complete, gate-level fail** — the report has all market-outlook mandatory sections (snapshot, drivers, blockers, scenarios, stakeholders, monitoring) correctly structured. It is the best-structured market-outlook in the recent batch. But having the right sections does not mean the sections satisfy their contracts. This tests the gap between structural completeness and gate-level execution.
- **Scenarios without shared axis** — base/bull/bear scenarios exist but each scenario pivots to a different metric (revenue in base, viewership in bull, platform competition in bear). This is a new scenario failure pattern: the scenarios are present but not comparable because they lack a common load-bearing variable.

## Current rule verdict

- **Fail**: monitoring signals do not meet actionability hard-fail (zero signals with threshold/cadence/source/trigger-to-action)
- **Fail**: source-strength gate fail (Wikipedia/crowdsourced dominant for load-bearing claims)
- **Warn**: evidence labels inconsistent with source strength (confirmed fact tags on secondary sources)
- **Warn**: forward-looking numbers lack sourcing and role labels
- **Warn**: scenarios not bound to shared quantitative axis
- **Fail**: self-assessment overclaim triggers declared-not-executed (source, market-outlook, forward-looking all claimed ✅)
- **Conditional pass**: content quality and structure are strong; counter-evidence and stakeholder actionability are above average; the core judgment is clearly stated and defensible

## Related evals

- `evals/cases/agent-api-market-outlook-full-spectrum-fail-case.md` — same route, maximum severity (100% inflation, zero body citations, zero monitoring)
- `evals/cases/dc-power-market-outlook-inflation-and-monitoring-case.md` — same route, monitoring structure without actionability, >50% register inflation
- `evals/cases/ai-video-market-outlook-label-and-probability-gap-case.md` — same route, scenario labels and probabilities without support
- `evals/cases/cross-border-ecommerce-market-outlook-self-assessment-case.md` — same route, self-assessment overclaim pattern
- `evals/cases/aaeon-listed-company-label-inflation-case.md` — different route, same evidence-label-inflation pattern
- `evals/cases/advantech-listed-company-traceability-hard-fail-case.md` — different route, same self-assessment overclaim with traceability gap

## Reviewer checklist

- Does the body have `[Sxx]` citations? (pass/fail: yes)
- Are the cited sources appropriate for their claims? (check: Wikipedia vs. official sources for load-bearing claims)
- Are evidence labels calibrated to actual source types? (check: confirmed fact tags on secondary/crowdsourced sources)
- Do at least 3 monitoring signals have threshold + cadence + source + trigger-to-action?
- Do forward-looking numbers have sourcing, role labels, or assumption chains?
- Are the three scenarios bound to the same quantitative axis?
- Does self-assessment reflect actual gate execution, not just structural completeness?

## Scoring

- **Pass**: source pool appropriate for claims, monitoring signals actionable (≥3 with 4 fields), forward-looking numbers sourced and role-labeled, scenarios bound to shared axis, self-assessment honest
- **Conditional pass**: structurally complete, strong counter-evidence, stakeholder table actionable, body `[Sxx]` present, but 1-2 gates conditional (e.g., monitoring signals qualitative, source pool partially weak) — no process-integrity hard-fail
- **Fail** (this case's level): structurally strong market-outlook execution with body `[Sxx]` present, but source-strength gate fails on load-bearing claims, monitoring hard-fail triggers (zero actionable signals), forward-looking numbers unsourced, and self-assessment overclaims — multiple independent gate failures despite structural completeness
