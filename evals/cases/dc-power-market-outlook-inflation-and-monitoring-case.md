# Eval: Data Center Power — Market Outlook Register Inflation and Monitoring Actionability Case

## Goal

Test whether a Market Outlook / Industry Evolution report with strong current-state snapshot, drivers/blockers separation, multi-scenario structure, and multi-stakeholder coverage can still **fail strict delivery** when:

- **Source Register inflation exceeds 50%** — 33 register entries, only 16 cited in body, yet claims source-traceability ✅ passed; triggers register inflation hard-fail
- **self-assessment references non-existent section** — audit status block cites "§7.2" for technical secondary verification, but the report has no §7.2; a specific process-artifact failure
- **monitoring signals have structure but lack actionability** — signals listed with threshold/trigger but no cadence, source, or trigger-to-action mapping; fails the monitoring actionability gate added in Round 7 (#224)
- **forward-looking labels in observed-fact context** — IEA forecast placed in `[确认事实]` bullet, "预计2027年翻倍" in `[观察值]` table row; forward-looking numbers not consistently separated from confirmed facts
- **source strength/label mismatch** — Wikipedia, vendor claims (NVIDIA), industry media carrying `[确认事实]` for load-bearing claims
- **secondary Technical Deep-Dive route declared but verification unverifiable** — self-assessment claims verification via non-existent section
- **self-assessment claims all ✅ while inflation, monitoring, labels, and secondary verification all have gaps** — triggers process-integrity hard-fail

This eval is based on a real report: a data center power constraint market outlook memo that correctly activated the market-outlook route, provided a strong current-state snapshot, separated drivers and blockers, built three scenarios with stakeholder coverage, and included counter-evidence — but failed on register inflation severity, monitoring actionability, forward-looking label consistency, and self-assessment accuracy.

## Prompt

Analyze how global data center power constraints affect the AI infrastructure industry chain. Produce a structured market outlook report that:

- provides a current market snapshot (power consumption, share, queue backlog, construction investment, supply chain bottlenecks)
- separates key drivers (AI model scale, inference demand, renewables, policy, liquid cooling) from blockers (grid interconnection, social license, TDP/thermal, SMR timeline, AI bubble)
- builds base case with explicit assumptions and quantified ranges
- provides structured alternative scenarios (optimistic / pessimistic) with trigger conditions
- covers ≥3 stakeholder categories with implications (hyperscalers, chip designers, DC REITs, utilities, policymakers)
- includes actionable monitoring signals with threshold, cadence, source, and trigger-to-action mapping
- uses a complete 7-column Source Register with all entries cited in body — uncited entries >25% is a hard-fail
- labels forward-looking numbers separately from observed facts — IEA forecasts, "预计" statements, and scenario projections must not carry `[确认事实]` or `[观察值]` labels
- if declaring a secondary route (Technical Deep-dive), runs and reports its hard-fail verification in a real section that exists in the report body
- includes a self-assessment block that honestly reflects actual gaps

## What this eval is testing

- whether extreme register inflation (>50%) is caught and blocks source-traceability self-assessment
- whether monitoring signals satisfy the **actionability** dimension (cadence, source, trigger-to-action) — structure alone (signal/threshold/trigger) is insufficient per Round 7 #224
- whether forward-looking numbers in market-outlook are consistently separated from observed facts — forecast projections must not carry confirmed/observed labels
- whether the audit status block references sections that actually exist in the report body
- whether secondary route hard-fail verification is verifiable (documented in a real section)
- whether self-assessment accuracy matches body execution across all market-outlook-specific disciplines

## Pass criteria

A passing answer should:

1. **Maintain register inflation below 25%.** Every registered source cited in body. Uncited entries >25% is a hard-fail; >50% is a severe fail.

2. **Deliver actionable monitoring signals.** Each signal must include: signal name, threshold/trigger value, review cadence, data source, and trigger-to-action mapping (what action to take if signal crosses threshold).

3. **Separate forward-looking numbers from confirmed/observed labels.** IEA forecasts, "预计" statements, scenario projections labeled as forecast / scenario assumption / model output — never as `[确认事实]` or `[观察值]`.

4. **Make self-assessment verifiable.** Every section cited in the audit status block must exist in the report body. No phantom §7.2 references.

5. **Verify secondary route in a real, labeled section.** Technical Deep-dive hard-fail verification must have its own section or sub-section — not a one-line claim in the audit block.

6. **Caveat weak sources.** Wikipedia labeled as crowdsourced compilation, vendor claims labeled as manufacturer statement (not independent verification), industry media labeled as secondary reporting.

## Failure signs

Mark this eval as failed if the answer does any of the following:

- register inflation >25% (hard-fail; >50% severe fail)
- monitoring signals lack cadence, source, or trigger-to-action mapping (monitoring actionability hard-fail)
- forward-looking numbers carry `[确认事实]` or `[观察值]` labels (forward-looking label gate hard-fail)
- audit status block references a non-existent section (process-artifact hard-fail)
- secondary route hard-fail verification is claimed but the verifying section is empty or non-existent
- self-assessment claims all ✅ while inflation, monitoring, labels, or secondary verification have gaps (process-integrity hard-fail)

## Why this eval matters

Market-outlook is a well-covered route. This case adds specific failure modes from the intersection of Round 7 hardening (#222 forward-looking labels, #224 monitoring actionability) and recurring register/self-assessment issues:

| Case | Route | Level | Unique market-outlook failure |
|---|---|---|---|
| DC power forward-looking (#222) | market-outlook | Fail | Forward-looking labels as [确认事实] |
| Humanoid robot self-assessment | market-outlook | Conditional pass | Self-assessment overconfidence |
| AI cost-control full pass | market-outlook | Pass | Benchmark, not a fail case |
| DC power inflation (this) | market-outlook | **Fail** | **>50% register inflation + phantom section reference + monitoring structure without actionability** |

The unique contributions:

- **>50% register inflation as a benchmark** — existing cases test 25-40% inflation. This case sets a severe benchmark: when >50% of registered sources are uncited, the traceability claim is fundamentally broken regardless of register format.
- **Phantom section reference in audit block** — a new failure subtype: the audit status block claims verification from a section number that doesn't exist in the report. This is different from "vague evidence column" or "overconfidence" — it's a specific delivery error where the self-assessment references non-existent content.
- **Monitoring structure without actionability** — the Round 7 #224 hardening added monitoring actionability requirements. This case tests whether having the right shape (signals/thresholds/triggers) but missing the actionability columns (cadence, source, trigger-to-action) is correctly identified as insufficient.
- **Forward-looking label gate in market-outlook** — extends the #222 test from explicit forecast numbers to the subtler case where forecast data is embedded in an observed-fact context (IEA forecast in [确认事实] bullet).

## Current rule verdict

- Register inflation hard-fail: >50% uncited
- Monitoring actionability hard-fail: missing cadence, source, trigger-to-action
- Forward-looking label gate: forecast numbers in confirmed/observed context
- Process-artifact hard-fail: self-assessment references non-existent §7.2
- Secondary route: technical verification claimed via non-existent section
- Process-integrity hard-fail: self-assessment claims all ✅ while multiple gaps exist

## Related evals

- `evals/cases/dc-power-market-outlook-forward-looking-label-gap-case.md` — same topic domain, forward-looking labels as [确认事实]
- `evals/cases/cross-border-ecommerce-market-outlook-self-assessment-case.md` — same route, self-assessment overconfidence
- `evals/cases/humanoid-robot-market-outlook-dual-route-case.md` — same route, dual-route execution
- `evals/cases/bytedance-competitive-positioning-source-mapping-case.md` — same register inflation pattern, different route

## Reviewer checklist

- Is register inflation below 25%? (check cited count vs total registered)
- Do monitoring signals have cadence, source, AND trigger-to-action?
- Are forward-looking numbers labeled separately from confirmed/observed?
- Does every section cited in audit status block exist in the report body?
- Is secondary route verification documented in a real, identifiable section?
- Does self-assessment match actual body execution?

## Suggested scoring

- **Pass**: register inflation <25%, monitoring signals actionable (cadence/source/trigger-to-action), forward-looking labels separated, audit block cites existing sections only, secondary route verified in identifiable section, self-assessment honest
- **Conditional pass**: market-outlook structure strong, scenarios present, stakeholder coverage good, but register inflation 25-40%, or monitoring signals have structure but missing 1 actionability dimension, or forward-looking label separation partial, or self-assessment slightly optimistic — no hard-fail triggered
- **Fail**: register inflation >25% (hard-fail), or monitoring signals lack cadence/source/trigger-to-action (actionability hard-fail), or forward-looking numbers labeled as confirmed/observed (label gate hard-fail), or audit block references non-existent section (process-artifact hard-fail), or self-assessment claims all ✅ while gaps exist (process-integrity hard-fail)
