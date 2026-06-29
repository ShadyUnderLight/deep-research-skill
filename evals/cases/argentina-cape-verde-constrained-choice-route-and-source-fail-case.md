# Eval: Argentina vs Cape Verde — Constrained-Choice Route Activation and Source Traceability Fail Case

## Goal

Test whether a sport match prediction report with strong analytic reasoning, clear probability judgments, and explicit counter-evidence can still **fail hard** when:

- **route self-declared as Shared-workflow, actual burden is constrained-choice** — predicting match outcomes, ranking upset paths, assigning probability distributions is a structured choice task, not a generic shared workflow
- **decision architecture entirely missing** — no Decision Scope, option universe, shortlist construction logic, comparison unit, or aggregation logic; probability judgments and score distributions are stated without showing how they were derived or how options were narrowed
- **numbers without roles or methods** — core probabilities (`10-15%`, `25-30%`, `80-85%`, `8-10%`, `2-3%`) and score distributions lack observed/proxy/assumption/model-output labels, estimation method, model reference (Poisson/logit/odds calibration), or worked example
- **source traceability hard-fail** — body has zero `[Sxx]` inline citations; Source Register is 6-column (missing Claims Supported); ALL 100% of sources are Wikipedia
- **source-strength gate fail with false reliability labeling** — all Wikipedia sources are labeled "high reliability", actively misrepresenting tertiary sources as authoritative for load-bearing match analysis claims
- **current-state gap critical for domain** — report admits missing odds, injuries, training status, and weather; for pre-match prediction, these are core inputs, not optional enrichments
- **self-assessment overclaim** — claims workflow/final-audit passed when route is misidentified, no `[Sxx]` exists, numeric roles are absent, and current-state is incomplete

This eval is based on a real report: an Argentina vs Cape Verde knockout match upset path analysis that correctly identified the core question ("can Cape Verde upset, how, and with what probability?"), used multi-dimensional analysis (tactical, historical, counter-evidence), and delivered a clear bottom-line judgment — but self-declared as Shared-workflow, built no choice architecture, and provided zero auditable evidence for its core numbers.

## Prompt

Analyze the upset potential for Cape Verde against Argentina in the World Cup knockout stage. What are the realistic upset paths, what probabilities attach to each, and what conditions must be met?

## What this eval is testing

- whether sport match outcome prediction with probability distributions and path ranking is correctly identified as constrained-choice rather than Shared-workflow
- whether probability judgments stated without method, role labels, or worked example trigger the numeric-role hard-fail in constrained-choice
- whether 100% Wikipedia sourcing with false "high reliability" labels triggers both source-traceability hard-fail and source-strength gate fail simultaneously
- whether a 6-column Source Register (missing Claims Supported) is correctly identified as non-compliant with the 7-column hard requirement
- whether admitting current-state gaps (odds, injuries, weather) while still publishing probability judgments constitutes a current-state verification failure for pre-match prediction
- whether self-assessment claiming workflow/final-audit passed while route is wrong, traceability is absent, and numeric roles are missing triggers process-integrity hard-fail

## Pass criteria

A passing answer should:

1. **Select the correct route.** Sport match outcome prediction with probability distributions, path ranking, and conditional scenarios is constrained-choice. Not Shared-workflow, not market-outlook, not technical-deep-dive.

2. **Build decision architecture.** Must include: Decision Scope (who is deciding what, at what time), option universe (all possible outcomes), shortlist construction logic (why these paths, why not others), comparison unit (single metric for ranking), and aggregation logic (how probabilities are derived).

3. **Execute numeric role discipline.** Every probability, percentage, and score distribution must carry an observed/proxy/assumption/model-output label. Estimation method must be disclosed (e.g., Poisson model, odds calibration, historical baserate, expert judgment). At least one worked example must demonstrate how a stated probability was computed.

4. **Execute source traceability.** Body must have `[Sxx]` inline citations for all load-bearing factual claims. Source Register must have 7 columns including Claims Supported. Sources must include primary/official sources for match data, not only Wikipedia.

5. **Pass source-strength gate with honest reliability labels.** Wikipedia sources must be labeled with their actual reliability tier (tertiary, crowdsourced), not falsely marked as high reliability.

6. **Verify current-state inputs.** Odds, injuries, lineups, weather, and training status must be sourced from current data, not left as admitted gaps while still publishing probability judgments.

7. **Keep self-assessment honest.** Audit status must reflect actual gate execution. Route, source, and quantitative role must not be claimed passed when unexecuted.

## Failure signs

Mark this eval as failed if the answer does any of the following:

- self-declares Shared-workflow for a task whose core burden is probability-based outcome ranking (route misidentification)
- states probabilities and score distributions without numeric role labels, estimation method, or worked example (numeric-role hard-fail)
- body has zero `[Sxx]` inline citations (source-traceability hard-fail)
- Source Register is 6 columns (missing Claims Supported) and/or 100% Wikipedia (source-strength gate fail)
- labels Wikipedia sources as "high reliability" (false reliability labeling)
- admits missing current-state inputs (odds, injuries, weather) but still publishes numerical probability judgments
- self-assessment claims all disciplines passed when route, source, and numeric roles are unexecuted

## Why this eval matters

This case adds a **sport-domain constrained-choice + false reliability labeling** pattern not covered by existing cases:

| Existing constrained-choice case | This case |
|---|---|
| `world-cup-constrained-choice-wrong-route` — declared market-outlook for ranking task | Declares **Shared-workflow** for constrained-choice task — different wrong-route pair |
| `world-cup-prediction-probability-method` — probabilities without replicable method | Same probability gap, PLUS 100% Wikipedia + false "high reliability" labeling |
| `small-team-agent-tech-dive-secondary` — zero [Sxx], missing numeric roles | Same gaps, but add: missing entire decision architecture (no option universe, no shortlist, no comparison unit) |
| `content-platform-compounded-fail` — table role-label and scoring-aggregation gates | Same aggregation gap, different route misidentification pattern |

The unique contributions:

- **Shared-workflow as constrained-choice escape hatch** — the report correctly identified the task as having no matching route in the 11-route matrix (sport match prediction is indeed not in the commercial/investment/tech route set), but instead of recognizing constrained-choice as the closest contract (structured ranking with probability), it defaulted to Shared-workflow — the catch-all route. This extends route misidentification testing from "wrong specific route" to "refusal to pick a route."
- **False reliability labeling as a new source-strength sub-pattern** — previous cases tested Wikipedia dominance, but this case adds active mislabeling: all Wikipedia sources are marked "high reliability." This is worse than just using Wikipedia — it's actively deceiving the reader about source quality. Combined with 100% Wikipedia composition, this is a double failure: wrong sources + wrong labels.
- **Current-state gap in pre-match prediction** — admitting missing odds, injuries, and weather while publishing numerical probabilities is a domain-specific failure. For pre-match prediction, these are not optional enrichments — they are the minimum viable inputs. Publishing numbers without these inputs is like publishing a listed-company report without financial data.
- **Missing entire decision architecture** — unlike previous constrained-choice cases that had partial architecture (some shortlist logic, some ranking), this case has zero architecture: no option universe, no shortlist boundary, no comparison unit, no aggregation logic. Probabilities appear as if from nowhere.

## Current rule verdict

- **Fail**: route misidentification (declared Shared-workflow, actual constrained-choice) — route-activation hard-fail
- **Fail**: numeric-role hard-fail — probabilities and score distributions without role labels, method, or worked example
- **Fail**: source-traceability hard-fail — zero body `[Sxx]`, 6-column register, 100% Wikipedia, Claims Supported missing
- **Fail**: source-strength gate fail with false reliability labeling — 100% Wikipedia labeled as "high reliability"
- **Fail**: current-state hard-fail — core pre-match inputs (odds, injuries, weather) admitted missing while probabilities published
- **Fail**: process-integrity hard-fail — self-assessment claims passed while route, source, and numeric roles all unexecuted

## Related evals

- `evals/cases/world-cup-constrained-choice-wrong-route-case.md` — same route misidentification pattern, different wrong-route pair (declared market-outlook vs. declared Shared-workflow)
- `evals/cases/world-cup-prediction-constrained-choice-probability-method-case.md` — same sport-domain constrained-choice, same probability-method gap
- `evals/cases/world-cup-rule-regulatory-route-mismatch-case.md` — same Shared-workflow escape hatch pattern, different correct route (regulatory vs. constrained-choice)
- `evals/cases/small-team-agent-constrained-choice-tech-dive-secondary-case.md` — same route, same source and numeric-role gaps
- `evals/cases/content-platform-constrained-choice-compounded-fail-case.md` — same route, same aggregation and role-label gaps
- `evals/cases/advantech-listed-company-traceability-hard-fail-case.md` — different route, same source-traceability hard-fail + self-assessment overclaim

## Reviewer checklist

- Is the self-declared route correct? (constrained-choice, not Shared-workflow)
- Is decision architecture present? (Decision Scope, option universe, shortlist, comparison unit, aggregation logic)
- Do all probabilities and score distributions have numeric role labels and disclosed estimation method?
- Does the body have `[Sxx]` inline citations?
- Is the Source Register 7-column with Claims Supported?
- Are source types appropriate for claims? (not 100% Wikipedia for match analysis)
- Are source reliability labels honest? (Wikipedia != high reliability)
- Are current-state inputs verified? (odds, injuries, weather sourced, not gapped)
- Does self-assessment reflect actual execution?

## Scoring

- **Pass**: correct route, decision architecture present, numeric roles and methods for all probabilities, body `[Sxx]` with appropriate sources, honest reliability labels, current-state verified, honest self-assessment
- **Conditional pass**: correct route declared, partial decision architecture, probabilities disclosed as expert judgment with caveats, source pool mixed but main claims traceable to non-Wikipedia sources, current-state partially gapped but acknowledged as limitation
- **Fail** (this case's level): wrong route (Shared-workflow escape hatch), zero decision architecture, probabilities without roles or methods, zero body [Sxx], 100% Wikipedia falsely labeled as high reliability, current-state inputs admitted missing while publishing numbers, self-assessment overclaim
