# Eval: World Cup Group Winner Path Advantage — Cross-Source Contamination and Simulation Contract Case

## Goal

Test whether a Technical Deep-dive / Architecture Analysis report with correct route selection, a structured path-difficulty comparison framework, and quantitative claims (Monte Carlo simulation, Elo ratings, p-values, confidence intervals) can **fail strict delivery** when:

- **Monte Carlo simulation claims lack execution evidence** — p≪0.01, 85.2% vs 40.1% advance rates, Elo 1574 vs 1754 presented as findings but with zero team list, zero seed, zero iteration parameters, and no evidence the simulation was actually executed (covered by [#342](https://github.com/ShadyUnderLight/deep-research-skill/issues/342) simulation contract / R74-R75)
- **Wikipedia-only sources for load-bearing structural claims** — tournament format, knockout path structure, and historical data all sourced from Wikipedia, which cannot bear claims about official FIFA rules and tournament architecture (covered by [#341](https://github.com/ShadyUnderLight/deep-research-skill/issues/341) source strength)
- **NEW (R77): Cross-source model contamination** — Wikipedia structural data (tournament format, history) and external Elo ratings + Monte Carlo simulation output are presented as a single flat "analysis" without layer separation. The Source Register does not distinguish the reliability tiers: Wikipedia data layer vs Elo model layer vs simulation output layer. Even if each individual source passes [#341](https://github.com/ShadyUnderLight/deep-research-skill/issues/341)'s strength check, mixing fundamentally different data tiers without layer identification is a separate audit failure.

This eval is based on a real paired-report comparison: a GPT deep-research version that claimed Monte Carlo simulation results with statistical significance (p≪0.01) but provided no execution evidence, vs a local deep-research-skill version that honestly restricted itself to Wikipedia-only data and made no false simulation claims. Both fail — GPT on simulation contract, local on source strength — but the new cross-source contamination pattern (R77) is the unique contribution of this eval.

## Prompt

Analyze whether winning the group in a 48-team World Cup format (12 groups × 4 teams, top 2 + 8 best third-placed teams advance to Round of 32) provides a significant knockout-stage path advantage for group winners compared to group runners-up.

Produce a structured technical deep-dive report that:

- explains the 48-team knockout bracket structure and the mapping of group-stage finishing positions to knockout-stage opponents
- analyzes path difficulty: do group winners systematically face weaker Round-of-32 opponents? Does this advantage propagate through subsequent rounds?
- quantifies the path advantage: estimate the difference in knockout-stage advancement probability between group winners and group runners-up
- uses Monte Carlo simulation with team-level Elo ratings to model knockout-stage progression probabilities (specify team list, Elo source, seed, iterations, and provide execution evidence — simulation output file or reproducible script)
- provides historical comparison: how did group winners perform in knockout stages in previous 32-team World Cups? (analogous scenario)
- includes a complete 7-column Source Register with **Claims Supported** (claim-level) mapping
- **separates data layers in the Source Register**: Wikipedia structural data (tournament format/history), external model data (Elo ratings), and simulation output must be in clearly distinct layers with explicit provenance for each
- labels all quantitative claims with observed/proxy/assumption/model-output roles
- documents any simulation-execution status (conceptual / executed with evidence / illustrative)

## What this eval is testing

- whether Monte Carlo simulation claims (p-values, advance rates, Elo scores) are blocked when execution evidence is absent — no team list, no seed, no iteration count, no output file
- whether Wikipedia-only sources are flagged as insufficient for load-bearing structural claims about official tournament rules and knockout architecture
- **whether cross-source model contamination is detected**: when Wikipedia structural data and external Elo/Monte Carlo model data are presented in a single analysis without source-layer separation, the Source Register must show distinct reliability tiers
- whether numeric role labels (observed/proxy/assumption/model-output) are applied to quantitative claims
- whether self-assessment reflects actual audit status when simulation contract, source strength, and cross-source layer separation all have gaps

## Pass criteria

A passing answer should:

1. **Provide simulation execution evidence or declare non-execution.** If the report presents Monte Carlo results (p-values, advance rates, Elo scores), it must include: team list, Elo source and retrieval date, random seed, iteration count, and a reproducible script or output artifact. Without this, the report must explicitly label the simulation as "概念框架，未实际执行" and cannot present numerical results as findings.

2. **Use primary/authoritative sources for load-bearing structural claims.** Official FIFA documents, tournament regulations, or official announcements for tournament format and knockout path architecture — not just Wikipedia.

3. **Separate data layers in the Source Register.** The Source Register must distinguish at minimum: (a) structural/factual layer — tournament format, history, rules (Wikipedia, FIFA docs); (b) model data layer — Elo ratings, team strength proxies (external databases); (c) simulation output layer — Monte Carlo results, p-values, confidence intervals (own execution). Each layer must have explicit provenance. A single flat register that mixes these tiers is insufficient — this is the R77 cross-source contamination check.

4. **Label numeric roles.** All quantitative claims — Elo scores, advance rates, p-values, historical performance stats — must have observed/proxy/assumption/model-output labels.

5. **Maintain honest self-assessment.** The audit must flag simulation-execution gaps and source-layer separation gaps if they exist. Self-assessment claiming all ✅ while these gaps exist triggers process-integrity hard-fail.

## Failure signs

Mark this eval as failed if the answer does any of the following:

- presents Monte Carlo simulation results (p≪0.01, 85.2% advance, Elo 1574 vs 1754) without execution evidence: no team list, no seed, no iteration count, no output artifact
- claims statistical significance ("p≪0.01", "95% CI: [82%, 88%]") without disclosing test statistic, sample size, degrees of freedom, or effect size
- uses Elo ratings as simulation input without disclosing the Elo data source, retrieval date, and team coverage
- all or most load-bearing structural claims rely on Wikipedia/crowdsourced sources
- **Source Register is a single flat table mixing Wikipedia structural data, external Elo ratings, and simulation output without layer separation** — this is the R77 cross-source contamination failure
- quantitative claims lack observed/proxy/assumption/model-output role labels
- self-assessment claims all ✅ while simulation contract, source strength, or cross-source layer separation have gaps

## Why this eval matters

This case adds a **cross-source model contamination dimension** that is not covered by existing simulation-transparency or source-strength evals. Even if each individual source passes [#341](https://github.com/ShadyUnderLight/deep-research-skill/issues/341)'s strength check (Wikipedia is acceptable for structural facts, Elo databases are acceptable for team strength proxies), mixing fundamentally different data reliability tiers in a single flat analysis creates an auditability failure that neither [#341](https://github.com/ShadyUnderLight/deep-research-skill/issues/341) nor [#342](https://github.com/ShadyUnderLight/deep-research-skill/issues/342) alone captures:

| Case | Simulation contract (#342) | Source strength (#341) | **Cross-source layer separation (R77)** |
|---|---|---|---|
| `simulation-pseudocode-as-executed-case` | ✅ Tests: pseudocode + claimed results without execution | — | — |
| `world-cup-info-advantage-technical-deep-dive-source-strength-case` | — | ✅ Tests: 100% Wikipedia, no primary sources | — |
| `dc-power-market-outlook-inflation-and-monitoring-case` | — | ✅ Tests: Wikipedia for structural claims | — |
| **This case (group-winner-path-advantage)** | ✅ Tests: p≪0.01 + Elo + advance rates without execution | ✅ Tests: Wikipedia-only for format/history | ✅ **Tests: Wikipedia + Elo + Simulation mixed in single flat analysis without layer separation** |

The unique contribution:

- **Cross-source model contamination (R77)**: The failure is not that Wikipedia is used for format data or that Elo ratings are used for team strength — individually, each source type can be acceptable. The failure is that the report presents Wikipedia structural facts, external Elo model estimates, and Monte Carlo simulation projections within a single "analysis" without distinguishing their fundamentally different reliability characteristics. A reader who sees "group winner advances 85.2%" receives this as one finding — they cannot audit that this number is the output of a model whose inputs (Elo ratings) come from an external database and whose structural constraints (bracket mapping) come from Wikipedia. Cross-source layer separation is the only way to restore auditability.
- **Layered Source Register requirement**: Extends the 7-column Source Register beyond per-source strength grading (#341) to require that sources be grouped into reliability tiers when they come from fundamentally different data domains (structural facts vs model estimates vs simulation projections).
- **Simulation contract with cross-source dimension**: This eval tests the interaction between simulation execution evidence (#342) and the cross-source contamination pattern — the simulation's missing execution evidence is compounded by the fact that its inputs (Elo ratings) are themselves unverifiable model data mixed with Wikipedia structural data.

## Current rule verdict

- **Simulation contract hard-fail** ([#342](https://github.com/ShadyUnderLight/deep-research-skill/issues/342)): p≪0.01, 85.2% advance, Elo 1574 vs 1754 presented as simulation findings without execution evidence → R74 (status disclosure requirement) and R75 (p-value/CI/Elo/Monte Carlo without execution evidence triggers validator warning). R75 is currently `WAIT_FOR_SECOND_CASE` — this case provides the second confirming instance.
- **Source strength hard-fail** ([#341](https://github.com/ShadyUnderLight/deep-research-skill/issues/341)): load-bearing structural claims on Wikipedia-only sources — per-source strength grading is already covered.
- **NEW (R77): Cross-source model contamination hard-fail**: Wikipedia structural data layer, external Elo model data layer, and Monte Carlo simulation output layer mixed in a single flat analysis without source-layer separation in the Source Register. This is not a per-source strength failure — it is a cross-source organization failure. Proposed home: `checklists/final-audit.md` §source layer separation; `references/report-template.md` §Source Register.
- **Numeric role hard-fail**: quantitative claims missing observed/proxy/assumption/model-output labels.
- **Process-integrity hard-fail**: self-assessment claims all ✅ while simulation contract, source strength, cross-source layer separation, and numeric roles all have gaps.

## Related evals

- `evals/cases/simulation-pseudocode-as-executed-case.md` — same simulation contract discipline (#342 / R74-R75); tests pseudocode-as-executed and example-table + p-value claims
- `evals/cases/world-cup-info-advantage-technical-deep-dive-source-strength-case.md` — same source strength discipline (#341); tests Wikipedia-only source failure and "Claims Supported" vs "支持章节" semantic gap
- `evals/cases/world-cup-constrained-choice-wrong-route-case.md` — same topic domain (World Cup), route selection failure
- `evals/cases/agentic-rag-technical-deep-dive-compounded-case.md` — same compounded-failure pattern (multiple discipline failures in one report)
- `evals/comparative-distillation/world-cup-group-winner-path-advantage-gpt-vs-local-comparative-distillation.md` — source distillation file that produced this eval; documents the GPT-vs-local comparison and R77 identification

## Reviewer checklist

- Are Monte Carlo simulation results (p-values, advance rates, Elo scores) accompanied by execution evidence (team list, seed, iterations, output artifact) or explicitly declared as non-executed?
- Are load-bearing structural claims about tournament format and knockout architecture sourced from primary/authoritative sources, not just Wikipedia?
- **Does the Source Register separate data layers?** Look for distinct tiers: (a) structural/factual layer (Wikipedia, FIFA docs), (b) model data layer (Elo database, team strength proxies), (c) simulation output layer (own execution). A single flat register mixing all three is a hard-fail.
- Do quantitative claims (advance rates, Elo scores, p-values) have observed/proxy/assumption/model-output role labels?
- Does self-assessment honestly reflect gaps in simulation execution, source strength, and cross-source layer separation?

## Suggested scoring

- **Pass**: simulation execution evidence present (team list, seed, iterations, output) OR simulation explicitly declared as non-executed with no numerical findings claimed; load-bearing structural claims on primary/authoritative sources; Source Register separates data layers (structural / model / simulation) with explicit provenance per layer; numeric roles present; self-assessment honest
- **Conditional pass**: simulation declared non-executed but partial structural claims still on Wikipedia (non-load-bearing); or source layers partially separated but some mixing remains; or most numeric roles present but some gaps — no hard-fail triggered
- **Fail**: Monte Carlo results (p≪0.01, 85.2%, Elo) presented as findings without execution evidence (simulation contract hard-fail); or load-bearing structural claims all Wikipedia-sourced (source strength hard-fail); or **Source Register is a single flat table mixing structural, model, and simulation data without layer separation** (R77 cross-source contamination hard-fail); or numeric roles absent; or self-assessment claims all ✅ while gaps exist (process-integrity hard-fail)
