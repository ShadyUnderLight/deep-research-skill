# Eval: AI Agent API Market Outlook — Full-Spectrum Fail Case

## Goal

Test whether a Market Outlook / Industry Evolution report with complete structural elements (current snapshot, drivers/blockers, multi-scenario, stakeholder coverage) can still **fail every market-outlook discipline simultaneously** at maximum severity:

- **zero body citations** — 34 Source Register entries, 0% cited in body (100% inflation)
- **Source Register only 5 columns** — missing Reliability, Claims Supported; fails 7-column hard requirement
- **inference register exists but body disconnected** — I01-I04 defined but body never uses `[Ixx]`, making the register non-functional
- **monitoring signals non-actionable** — zero signals meeting the 4-field actionability requirement (threshold, cadence, source, trigger-to-action)
- **scenario probabilities 55%/25%/20% without method** — stated as "directional" but precise percentages create false precision
- **numeric role labels absent** — funding, stars, request volume, latency, market share, probability, ARR thresholds all lack observed/proxy/assumption/model-output roles
- **player ranking without route boundary** — contains competitive-positioning rankings ("best bet") but does not document why the route is market-outlook rather than competitive-positioning
- **metadata-first drift** — audit status block precedes core judgment on the front page
- **self-assessment claims all ✅ while zero citations, 5-column register, zero monitoring actionability, and no numeric roles all exist** — triggers process-integrity and declared-not-executed hard-fails

This eval is based on a real report: an AI Agent Research API aggregation market outlook that included a current snapshot, drivers/blockers, three scenarios, six stakeholder categories, and monitoring signals — but failed every sellable market-outlook delivery criterion. It serves as the **severity benchmark** for market-outlook failures.

## Prompt

Produce an 18-month outlook for the local AI Agent / Research API aggregation market. Include current snapshot, key drivers, blockers, at least three scenarios with quantified axes, stakeholder implications across ≥3 stakeholder types, and actionable monitoring signals. This eval exists to test whether the delivery system correctly identifies when all market-outlook disciplines fail simultaneously at maximum severity.

## What this eval is testing

- whether 100% register inflation is caught (not just >25% or >50%)
- whether a Source Register that exists but has 0% body citation rate is correctly identified as functionally absent
- whether an inference register defined in infrastructure but never used in body is flagged as disconnected
- whether monitoring signals with zero actionable signals (missing cadence, source, trigger-to-action) are correctly assessed as non-compliant
- whether scenario probabilities stated as precise percentages without method are flagged regardless of "directional" disclaimers
- whether player ranking content triggers a route boundary check (market-outlook vs competitive-positioning)
- whether metadata-first drift on the front page is flagged

## Pass criteria / Failure signs

This eval has **no pass criteria** in the traditional sense — it exists as a severity benchmark. Mark the answer as failed if **any** of the following apply, which they will:

- body citations per register entry = 0% (100% inflation)
- Source Register has fewer than 7 columns
- inference register entries are never referenced via `[Ixx]` in body
- monitoring signals lack threshold, cadence, source, OR trigger-to-action for all listed signals
- scenario probabilities are precise percentages (e.g., 55/25/20) without method or assumption chain
- comparison/estimate/ranking numbers lack numeric role labels
- player ranking or "best bet" claims appear without route boundary documentation (why not competitive-positioning)
- self-assessment claims all ✅ while every discipline above is noncompliant

## Why this eval matters

This case adds a **severity benchmark** for the market-outlook route — the maximum fail configuration:

| Case | Inflation | Register cols | Body [Sxx] | Monitoring | Num roles | Route boundary | Self-assessment |
|---|---|---|---|---|---|---|---|
| DC power (Round 9) | >50% | 7 | 16/33 cited | Structure, no actionability | Table-level only | ⚠️ Partial | ❌ Overclaim |
| Agent API (this) | **100%** | **5** | **0/34 cited** | **Zero actionable** | **Absent** | **❌ Not documented** | **❌ Overclaim** |

The unique contributions:

- **100% register inflation as a severity benchmark** — the eval set previously tested 25% (threshold) and >50% (severe). 100% is a third tier: every single registered source is unused. The Source Register exists as pure infrastructure theater.
- **Inference register disconnected from body** — the report defines I01-I04 in the inference register but never uses `[Ixx]` in body text. This is analogous to Source Register inflation but for the inference chain: infrastructure exists but is functionally non-functional because the body never activates it.
- **Player ranking without route boundary** — market-outlook reports that include competitive-positioning rankings ("best bet", "strongest player", "winner") must document why the route is market-outlook rather than competitive-positioning. This extends the route boundary pattern to a new intersection.

## Current rule verdict

100% fail: all market-outlook disciplines trigger hard-fails simultaneously.

## Related evals

- `evals/cases/dc-power-market-outlook-inflation-and-monitoring-case.md` — same route, >50% inflation and monitoring structure without actionability
- `evals/cases/bytedance-competitive-positioning-source-mapping-case.md` — same false auditability (infrastructure present but disconnected), different route
- `evals/cases/tiktok-ai-technical-deep-dive-route-inflation-case.md` — same route boundary violation (primary route does not match burden)

## Scoring

- **Pass**: not applicable for this severity benchmark
- **Conditional pass**: not applicable
- **Fail** (this case's level): 100% register inflation + zero body citations + nonfunctional inference register + zero monitoring actionability + no numeric roles + no route boundary + overconfident self-assessment
