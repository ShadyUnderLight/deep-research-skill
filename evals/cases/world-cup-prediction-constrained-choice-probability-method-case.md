# Eval: World Cup Match Prediction — Constrained Choice Probability Method Case

## Goal

Test whether a Constrained Choice / Shortlist report with clear outcome ranking (win/draw/loss), load-bearing variables, scenario logic, and reversal conditions can still **fail strict delivery** when:

- **probability distribution is presented as conclusion without replicable method** — 60%/25%/15% outcome probabilities stated without showing how evidence (team strength, form, head-to-head, situational factors) maps to probability numbers
- **numeric role labels absent** — odds, probabilities, percentage impacts lack observed/proxy/assumption/model-output roles; triggers constrained-choice hard-fail
- **body-level source traceability weak** — only section-level source attribution, no `[Sxx]` claim-level citations
- **aggregator sources (Wikipedia, Transfermarkt) carry `[确认事实]`** — without caveat for crowdsourced compilation risk
- **Source Register has uncited entries** — S10/S11 registered but not referenced in body
- **self-assessment claims all ✅ while probability method, numeric roles, and body traceability have gaps** — triggers process-integrity hard-fail
- **metadata-first drift on front page** — evidence grading and audit status before core judgment

This eval is based on a real report: an Argentina vs Algeria World Cup match prediction memo that correctly activated the constrained-choice route, defined 5 load-bearing variables, listed reversal conditions with pre-match signals, and included counter-evidence — but failed on probability method transparency, numeric role labeling, body traceability, and self-assessment accuracy.

## Prompt

Predict the outcome of a specific World Cup match (Argentina vs Algeria). Produce a structured decision memo that:

- defines the outcome shortlist (win / draw / loss) and states why these are the exhaustive options
- lists 3-5 load-bearing variables with their evidence basis
- provides a probability distribution over outcomes with a replicable method — show how variable scores combine into probabilities, not just the final percentages
- labels all key numbers (probabilities, odds, performance percentages, impact estimates) with observed/proxy/assumption/model-output roles
- uses `[Sxx]` inline citations for every load-bearing claim in every section
- includes a complete 7-column Source Register with all entries cited in body
- distinguishes official sources (FIFA, team announcements, match centre) from aggregator sources (Wikipedia, Transfermarkt) with appropriate caveats
- includes counter-evidence (historical upsets, situational risks) that adjust the probabilities
- places the core judgment (prediction summary) before evidence grading / audit status metadata on the front page
- provides pre-match monitoring signals with specific thresholds for probability adjustment

## What this eval is testing

- whether probability distributions in constrained-choice reports have a replicable method — 60/25/15 as conclusion without method creates false precision
- whether numeric role labels are applied to probability/odds/impact numbers in sports prediction context
- whether body-level `[Sxx]` traceability is executed
- whether aggregator sources (Wikipedia, Transfermarkt) are caveated appropriately for crowdsourced compilation risk
- whether Source Register entries are all body-cited
- whether self-assessment accuracy matches body execution
- whether the front page places judgment before metadata

## Pass criteria

A passing answer should:

1. **Show the aggregation method from evidence to probabilities.** State how each variable (form, squad value, head-to-head, situational factors) is scored and combined into the final 60/25/15 distribution. At minimum: weight per variable, score per outcome per variable, and combination rule.

2. **Label numeric roles for all probability/odds/impact numbers.**
   - outcome probabilities → model output
   - bookmaker odds → observed (if current and sourced) or proxy (if dated)
   - performance percentages → observed (if from verified match stats) or proxy (if from aggregator)
   - do not let any key number stand without role

3. **Execute body-level `[Sxx]` traceability.** Every key claim in exec summary, variable table, risk section, scenario section, and monitoring signals has an inline citation.

4. **Caveat aggregator sources.** Wikipedia and Transfermarkt entries must carry "(众包聚合源，非官方验证)" or equivalent — not `[确认事实]`.

5. **Cite all registered sources in body.** No registered source should be uncited. Remove or cite S10/S11.

6. **Place judgment before metadata.** Prediction summary should appear before evidence grading legend and audit status on the front page.

7. **Outcome shortlist and pre-match snapshot in first screen.**
   - The outcome shortlist (win / draw / loss) appears in the first 30% of the report
   - Pre-match snapshot (kickoff time, squad status, key unknowns) is visible before detailed analysis

## Failure signs

Mark this eval as failed if the answer does any of the following:

- outcome probabilities (60/25/15 etc.) presented without replicable method
- numeric role labels absent from probability/odds/impact numbers (constrained-choice hard-fail)
- body has no `[Sxx]` inline citations (source traceability hard-fail)
- Wikipedia/Transfermarkt sources carry `[确认事实]` without aggregator caveat
- registered sources exist that are not body-cited
- self-assessment claims all ✅ while method, roles, or traceability have gaps
- audit status / evidence legend precedes core judgment on the front page

## Why this eval matters

This case extends the constrained-choice route to a **probability-distribution-as-ranking** domain — the "ranking" is not "choose X over Y" but "assign likelihood to each outcome." The existing constrained-choice cases test qualitative ranking/product/platform selection. This case tests whether the probability method from evidence to ranking is replicable:

| Case | Domain | Ranking type | Method gap |
|---|---|---|---|
| Indie-dev product form | Product selection | Qualitative | No shortlist boundary |
| Content platform | Platform selection | Qualitative + star ratings | No aggregation replicability |
| AI startup HQ | City selection | Weighted scores (8.8 vs 8.5) | No scoring rules or worked example |
| World Cup prediction (this) | **Sports prediction** | **Probability distribution (60/25/15)** | **No method from evidence to probabilities** |

The unique contributions:

- **Probability as ranking** — the "choice" is not picking one option but distributing probability across options. The method gap is different: with qualitative ranking, the failure is "why A > B." With probability distribution, the failure is "how does evidence → 60% vs 25% vs 15%." This is a different aggregation replicability problem.
- **Sports prediction current-state velocity** — match prediction has the fastest current-state refresh cycle in this eval set. Injuries, lineups, odds, and form can change within hours. The current-state verification contract is correspondingly tighter.
- **Aggregator sources in sports context** — Wikipedia/Transfermarkt serve as backbone sources for squad value, head-to-head, and player data. Their reliability ceiling in a sports context differs from financial aggregators (Macrotrends) or academic databases.

## Current rule verdict

- Constrained-choice hard-fail: probability numbers lack role labels
- **Scoring replicability hard-fail**: probability distribution (60/25/15) presented without replicable aggregation method — caught by `scripts/validate_scoring_replicability.py` (scoring-replicability validator, registered in `audit_report.py` for constrained-choice route)
- Source traceability hard-fail: no body `[Sxx]`, uncited register entries
- Process-integrity hard-fail: self-assessment claims all ✅ while gaps exist
- Aggregator source caveat: Wikipedia/Transfermarkt as [确认事实] without caveat
- Delivery: metadata-first drift on front page

## Related evals

- `evals/cases/content-platform-constrained-choice-compounded-fail-case.md` — same route, compounded fail with body traceability and numeric roles
- `evals/cases/indie-dev-constrained-choice-delivery-fail-case.md` — same route, delivery fail with no source register and no roles
- `evals/cases/world-cup-constrained-choice-wrong-route-case.md` — same topic domain, different failure (wrong route entirely)
- `evals/cases/tsmc-listed-company-aggregator-source-and-moat-case.md` — same aggregator source discipline pattern, different route

## Reviewer checklist

- Is the probability aggregation method from evidence to 60/25/15 replicable?
- Do probability/odds/impact numbers have role labels (observed/proxy/assumption/model-output)?
- Does the body have `[Sxx]` inline citations?
- Are Wikipedia/Transfermarkt sources caveated as aggregator sources?
- Are all registered sources cited in body?
- Does self-assessment match body execution?
- Is the core judgment before metadata on the front page?

## Suggested scoring

- **Pass**: probability method replicable, numeric roles on all key numbers, body `[Sxx]` present, aggregator sources caveated, all register entries cited, self-assessment honest, judgment-first front page
- **Conditional pass**: constrained-choice structure strong, variables clear, reversal conditions present, but probability method described directionally without replicability, or numeric roles on most but not all key numbers, or traceability partial, or metadata placement suboptimal — no hard-fail triggered
- **Fail**: probability distribution presented without method (60/25/15 as unsubstantiated conclusion), or numeric roles absent (constrained-choice hard-fail), or body has no `[Sxx]` (traceability hard-fail), or self-assessment claims all ✅ while gaps exist (process-integrity hard-fail)
