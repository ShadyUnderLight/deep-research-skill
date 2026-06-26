# Eval: World Cup Transition Attack vs Possession Control — Method Scaffold with False Statistics Case

## Goal

Test whether a Technical Deep-dive report that correctly builds a method scaffold (defining observable metrics, measurement approaches, analytical framework) in a data-unavailable scenario can still **fail strict delivery** when:

- **example tables are presented as statistical evidence** — the report constructs a metric framework with transition attack efficiency, possession conversion rate, and counter-attack success rate indicators, but then presents example/demonstration tables with p-values and confidence intervals as if they were actual findings from real data
- **current-state staleness** — the report states "2026 World Cup data is not yet generated" when in June 2026, the tournament structure (48 teams, 12 groups, knockout path), draw results, qualified teams, match schedule, and venue assignments are all confirmed and publicly available
- **method scaffold lacks explicit placeholder boundaries** — the report defines metrics but fails to declare placeholder variables (e.g., `Δ_possession_advantage`, `transition_efficiency_gap`) with explicit assumption boundaries (event-count, sample-size, lookback-window, known constraints), leaving readers uncertain about what is framework vs. what is finding (R76 pattern)

This eval is based on a real paired-report comparison: a World Cup tactical mechanism analysis (transition attack vs possession control under the 2026 48-team format) where GPT's deep research version had a polished method scaffold but crossed the line into false statistics and stale factual claims, while the local deep-research-skill version had correct discipline (no false statistics) but a less structured framework.

The comparative distillation that documents the full paired-report comparison is at `evals/comparative-distillation/world-cup-transition-vs-possession-gpt-vs-local-comparative-distillation.md`.

## Prompt

Analyze whether the 2026 World Cup's expanded 48-team format rewards transition attacks more than traditional possession control. Produce a structured technical deep-dive report that:

- defines a tactical analysis framework with observable metrics for transition attack efficiency, possession conversion rate, counter-attack success rate, and defensive recovery speed
- explains how the 2026 format (12 groups of 4, top-2 + 8 best third-place teams advance, expanded knockout path) changes the tactical incentives compared to the 2022 32-team format
- identifies which tactical styles benefit from the new format structure (more group-stage matches, more knockout rounds, different rest schedules)
- uses historical data from prior tournaments (2018, 2022 World Cups + comparable multi-group tournaments) to establish baseline patterns
- clearly distinguishes between (a) confirmed 2026 facts (format rules, qualified teams, draw results, schedule, venues) and (b) analytical framework for future data
- labels all quantitative values with observed/proxy/assumption/model-output roles
- if data is unavailable for certain metrics, uses explicit placeholder variables with stated assumption boundaries — never presents example/demonstration tables as statistical evidence with p-values or confidence intervals
- includes a complete 7-column Source Register with claim-level mapping
- documents the route conflict check: why technical-deep-dive rather than market-outlook or other routes

## What this eval is testing

- whether `validate_simulation_claims.py` catches example tables that are presented with p-values/CI without "illustrative" or "conceptual" markers (simulation contract violation — extends #342)
- whether current-state freshness checks catch stale statements like "data not yet generated" when structural data (format, draw, schedule) already exists — the report must distinguish between "match outcome data not yet generated" (correct) and "all data not yet generated" (incorrect and stale)
- whether the report defines explicit placeholder variables with assumption boundaries when data is genuinely unavailable (R76 candidate rule pattern: data-unavailable method-scaffold)
- whether the method scaffold (metric definitions, analytical framework, placeholder variables) is clearly separated from findings — readers must not confuse framework scaffolding with statistical conclusions
- whether self-assessment accuracy reflects the gap between "has a well-organized framework" and "presented false statistics"

## Pass criteria

A passing answer should:

1. **Maintain clean separation between method scaffold and findings.** The report may define metrics, analytical frameworks, placeholder variables, and assumption boundaries. It must never present example/demonstration tables with p-values, confidence intervals, or statistical significance claims unless the underlying data is real, sourced, and disclosed.

2. **Use accurate current-state statements.** "2026 World Cup match-level data (goals, shots, possession stats, transition metrics per match) is not yet generated" is correct. "2026 World Cup data is not yet generated" is stale and incorrect — format rules, draw results, qualified teams, match schedule, and venue assignments are all confirmed. The report must explicitly list what data categories exist and what doesn't.

3. **Define explicit placeholder variables with assumption boundaries (R76).** When data is unavailable, the report must:
   - Name each placeholder variable (e.g., `transition_efficiency_gap`, `possession_conversion_delta`)
   - Declare its operational definition
   - State the assumption boundaries (event-count range, sample-size constraints, lookback-window, known constraints from tournament format)
   - Label it as `[placeholder — awaiting data]`

4. **Label all quantitative values with numeric roles.** Any number in the report — whether historical baseline, format parameter, or placeholder variable — must carry observed/proxy/assumption/model-output label.

5. **Document what is known vs. unknown about 2026.** A current-state snapshot that lists: confirmed format rules, qualified teams, match schedule, venue assignments (known) vs. team form, tactical setups, match outcomes, transition attack vs possession statistics (not yet generated).

## Failure signs

Mark this eval as failed if the answer does any of the following:

- example/demonstration tables are presented with p-values, confidence intervals, or "statistically significant" claims without explicit illustrative/conceptual markers and without real underlying data
- the report states "2026 data not yet generated" as an undifferentiated blanket claim — failing to distinguish between structural data that exists (format, draw, schedule) and match-level data that doesn't
- placeholder variables are absent or undefined — the method scaffold provides metric names but no explicit placeholder variable definitions, assumption boundaries, or data-availability markers
- quantitative values in tables lack numeric role labels (observed/proxy/assumption/model-output)
- the boundary between "this is a framework for future analysis" and "these are our findings" is ambiguous or unmarked
- self-assessment claims all ✅ while example tables carry p-values or stale current-state claims are present
- the report dismisses the question entirely with "data unavailable, cannot analyze" — this is a correct conservative position but the report should offer a method scaffold as a productive alternative (see R76: the rule is about constructive discipline, not avoidance)

## Why this eval matters

This case adds a **data-unavailable method-scaffold discipline dimension** that is distinct from the existing simulation-contract cases. Previous cases test whether pseudocode is presented as executed simulation (#342), or whether sources are strong enough for claims, or whether probability methods are replicable. This case tests a different edge condition: **when real data genuinely does not exist yet, what is the legitimate scope of a method scaffold before it crosses into false statistics?**

| Case | Failure family | Data exists? | Primary gap | Unique contribution |
|---|---|---|---|---|
| `simulation-pseudocode-as-executed` | simulation-discipline | Framework only (no execution) | Pseudocode → "simulation shows" | Simulation contract: conceptual vs executed status disclosure (R74/R75) |
| `world-cup-info-advantage-source-strength` | source-strength | Data exists (historical rules) | 100% Wikipedia for load-bearing claims | Source strength purity: all sources are crowdsourced compilations |
| `world-cup-prediction-probability-method` | probability-method | Partial (teams known, outcomes unknown) | 60/25/15 as conclusion without method | Probability distribution replicability: evidence → probability mapping |
| **`world-cup-transition-vs-possession-method-scaffold` (this)** | **method-scaffold / current-state-staleness** | **No match-level data exists** | **Example tables → p-values; stale "not yet generated"; no placeholder boundaries** | **Data-unavailable method scaffold boundary: when data is truly absent, the framework must self-identify as scaffolding (R76)** |

The unique contributions:

- **Data-unavailable as a distinct edge condition.** Unlike #342 (simulation was possible but not executed), here the data genuinely does not exist — no 48-team World Cup has ever been played. The method scaffold is the only legitimate output, but it must self-identify as scaffolding. This is a different contract than simulation disclosure.
- **Staleness in "not yet generated" statements.** "2026 data not yet generated" is a stale statement in June 2026 — format rules, draw results, qualified teams, schedules, and venues are all confirmed. The freshness discipline must distinguish between categories of data availability, not accept blanket "data doesn't exist" claims. This extends current-state freshness checks to a new granularity requirement.
- **Placeholder variables vs. false precision.** The report can and should define `Δ_possession_advantage` with assumption boundaries — this is constructive discipline. It cannot present made-up numbers in a polished table with p-values — this is fraud. R76 formalizes this boundary, which neither #342 (simulation disclosure) nor existing freshness rules cover.
- **Method scaffold as a legitimate output mode.** A report that says "here is the analytical framework for evaluating transition-vs-possession under the 2026 format, with placeholder variables and assumption boundaries — match data to be filled when tournament begins" is a valid, useful output. The eval must not penalize method-scaffold itself — only the crossing of the line into false statistics or stale claims.

## Current rule verdict

- **Simulation contract hard-fail (#342, R74/R75):** Example tables with p-values and confidence intervals without illustrative markers trigger `validate_simulation_claims.py` — the p-value/CI detection matches the pattern from `simulation-pseudocode-as-executed-case.md`
- **Current-state freshness hard-fail:** "2026 data not yet generated" as undifferentiated blanket claim is stale — structural data (format, draw, schedule, venues) exists and is confirmed. The freshness check must catch this. Covered by `checklists/final-audit.md` §freshness audit, but this case tests the granularity requirement (distinguishing data categories).
- **R76 candidate rule — data-unavailable method-scaffold:** When event/match data genuinely does not exist, the report must define explicit placeholder variables with assumption boundaries (event-count, sample-size, lookback-window, known constraints), label them as `[placeholder — awaiting data]`, and never present example tables as statistical evidence. This is a new rule candidate from the paired-report comparison.
- **Numeric role labeling:** All quantitative values in the report must carry observed/proxy/assumption/model-output labels. Placeholder variables must be labeled as `[placeholder]`.
- **Process-integrity hard-fail:** Self-assessment claims all ✅ while example tables carry p-values, stale current-state claims are present, or placeholder boundaries are absent.

## Related evals

- `evals/cases/simulation-pseudocode-as-executed-case.md` — same failure family (simulation discipline), covers "pseudocode presented as executed simulation" pattern from #342; this case extends to "example tables as statistical evidence" in data-unavailable context
- `evals/cases/world-cup-info-advantage-technical-deep-dive-source-strength-case.md` — same route (technical-deep-dive), covers source-strength failure with 100% Wikipedia sources; this case covers method-scaffold failure with false statistics
- `evals/cases/world-cup-prediction-constrained-choice-probability-method-case.md` — same topic domain (World Cup), covers probability method replicability in constrained-choice route; this case covers method-scaffold boundary in technical-deep-dive route
- `evals/cases/intel-current-state-freshness-case.md` — same current-state discipline family
- `evals/comparative-distillation/world-cup-transition-vs-possession-gpt-vs-local-comparative-distillation.md` — the paired-report comparison that documents the full GPT-vs-local gap and identifies R76 as the core new candidate rule

## Reviewer checklist

- Are any tables containing p-values, confidence intervals, or "statistically significant" claims actually backed by real, disclosed data — or are they example/demonstration tables masquerading as findings?
- Does the current-state statement distinguish between "structural data exists (format, draw, schedule, venues)" and "match-level data not yet generated" — or is it an undifferentiated "data not yet generated" blanket claim?
- Are placeholder variables explicitly defined with operational definitions and assumption boundaries (event-count, sample-size, lookback-window, known constraints)?
- Is the boundary between "analytical framework / method scaffold" and "findings from actual data" clearly marked?
- Do all quantitative values in tables carry numeric role labels?
- Does self-assessment reflect the gap between framework quality and statistical evidence quality?
- If the report offers a method scaffold without any statistical claims, it should pass (or conditional pass) — the eval tests crossing the line, not the scaffold itself

## Suggested scoring

- **Pass**: method scaffold is cleanly separated from findings, all example/demonstration content is explicitly marked as illustrative/conceptual, current-state statements are granular and accurate (structural data acknowledged, match-level data correctly identified as unavailable), placeholder variables have explicit assumption boundaries, numeric roles are labeled, no false p-values or CIs, self-assessment honest
- **Conditional pass**: method scaffold present and well-structured, no false statistics, but placeholder variables lack explicit assumption boundaries, or current-state snapshot could be more granular, or the scaffold-vs-finding boundary is partially but not fully marked — no hard-fail triggered
- **Fail**: example tables presented with p-values/CI as statistical evidence (simulation contract hard-fail, #342 R74/R75), or undifferentiated "2026 data not yet generated" stale claim (current-state freshness hard-fail), or method scaffold exists but placeholder boundaries completely absent (R76 hard-fail), or self-assessment claims all ✅ while false statistics or stale claims are present (process-integrity hard-fail)
