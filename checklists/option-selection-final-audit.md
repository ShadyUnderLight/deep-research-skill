# Option Selection Final Audit Checklist

Use this checklist when the task is mainly about choosing, ranking, narrowing, or shortlisting among several plausible options.

Examples:
- destination or city selection
- vendor shortlist
- office / venue / meetup-point choice
- route or location choice
- product/tool/platform shortlist
- any multi-option recommendation task where elimination matters

Run this checklist before delivery.

## Decision frame

- [ ] the report states the actual choice being made, not just the topic being explored
- [ ] hard constraints are explicit
- [ ] soft preferences are explicit or clearly marked as assumed
- [ ] the report distinguishes best overall, best-fit, and fallback option when relevant

## Load-bearing variables

- [ ] the 2-5 variables that actually drive the choice are clearly stated
- [ ] low-value descriptive detail does not crowd out the decision variables
- [ ] the report explains why these variables matter more than the others

## Comparison unit and aggregation logic

- [ ] the primary comparison unit is explicit (for example total access burden, usable leisure time, implementation cost, reliability-adjusted value)
- [ ] [BLOCKER] If the selection criterion is a compound concept ("综合回报" / "最佳价值" / "整体最优" / "composite return" / "best overall value"), the compound criterion must be decomposed into:
  a) sub-dimension definitions
  b) weight or priority for each sub-dimension
  c) trade-off rules (e.g., dimension A is twice as important as dimension B)
  Undefined compound criterion → hard-fail
- [ ] the aggregation logic is visible when multiple people, teams, or regions are involved
- [ ] the report states whether it is optimizing for average outcome, fairness, worst-case burden, weighted priority user, or robustness
- [ ] subgroup views are shown when one average would hide an important outlier or penalty
- [ ] if quantitative or composite scoring is used, the report distinguishes observed facts, proxies, assumptions, and model outputs rather than presenting them as one evidence layer
- [ ] if fairness is load-bearing, the report makes clear whether unfairness is being measured by worst-off participant, dispersion/variance, hidden subgroup penalties, or another explicit rule
- [ ] hidden operational burden layers (for example transfer burden, cross-border friction, checkpoint/visa hassle, fragile first/last-mile routing) are surfaced when they materially affect the ranking
- [ ] aggregation replicability: the ranking method should allow the reader to independently verify the result. At minimum:
  a) per-dimension scoring rules
  b) weights (explicit values or priority order)
  c) at least 1 worked example calculation path
  If scoring tables or star ratings are used, at least 2 exemplar scores should be traceable to specific evidence anchors

## Provider / vendor current-state gate

- [ ] for model, API, vendor, or platform provider tasks, the report verifies the current primary model/API family rather than anchoring on stale flagship generations
- [ ] current pricing, pricing units, and any batch/cache/context-length pricing differences are checked before comparison
- [ ] support regions, mainland-China accessibility, signing/payment reality, data residency, and SLA/status are treated as ranking variables when relevant, not buried as footnotes
- [ ] if a key provider fact could not be confirmed, it is marked unknown rather than filled with likely-but-stale prior knowledge

## Market-entry / regional-expansion gate

- [ ] for market-entry, country-prioritization, or regional-expansion tasks, the report states whether the recommendation is `go`, `not now`, `pilot only`, or phased entry
- [ ] the report makes priority relative to realistic alternatives visible rather than assuming the target market should be first by default
- [ ] the report distinguishes regional hub, first revenue beachhead, and later expansion market when those roles differ
- [ ] countries/markets are compared using one visible comparison unit rather than free-form country notes
- [ ] hard gates (budget, product architecture, compliance readiness, channel readiness, localization burden, or similar) are explicit
- [ ] the report names what would change the entry sequencing or turn `go` into `not now`
- [ ] **[Phase A] recommendation-constraint consistency** — GO / Pilot / Not Now labels are checked against the report's own budget, team, compliance readiness, and timeline estimates; if the report estimates 18–24 months to entry-ready but also requires 6-month revenue verification, the beachhead must not be labelled GO
- [ ] **[Phase A] sensitivity / switching table** — at least one sensitivity table or switching-condition description shows how changes in growth, ARPU, CAC, localization cost, partner deal cycle, or regulatory delay would change the beachhead country
- [ ] **[Phase B] Country Diligence Card** — each shortlisted country is evaluated through a consistent diligence card that includes: target customer/payer, first-revenue path, localization depth, regulatory/data status, competitive landscape, channel/partner readiness, entry motion, cost and timeline, legal/tax/IP, and expansion/exit scenario
- [ ] **[Phase B] two-level decision funnel** — the report explicitly separates regional screening (option universe → region shortlist) from country competition (winning region → country shortlist → single beachhead); winning region must compare at least 2–3 realistic country candidates or explain exclusivity

## Sports prediction / outcome probability gate

This gate activates when the constrained-choice task involves **pre-match prediction, outcome probability estimation, upset-path ranking, or any explicit win/draw/loss probability distribution for a sport match or competitive event**.

### Required current-state inputs

Before producing probability outputs, the report must source or explicitly declare unavailable:

- [ ] **market odds / market-implied probability** — odds from one or more bookmakers or betting exchanges, converted to implied probability as a baseline
- [ ] **injury and suspension status** — current confirmed absences and doubts for both sides
- [ ] **expected lineup / rotation risk** — likely starting XI, key player availability, rotation patterns
- [ ] **weather / venue / travel or surface factors** — forecast conditions, stadium location, travel burden, pitch surface
- [ ] **recent match data / form window** — results, goals scored/conceded, form trend over an appropriate window (e.g. last 5–10 matches)
- [ ] **tactical or statistical data relevant to the prediction** — such as xG, shots, set-piece threat, pressing intensity, defensive block indicators, head-to-head record

### Downgrade rules for missing inputs

If one or more of the above inputs are absent or sourced only from low-reliability sources:

- [ ] **probability output must be downgraded** — do not present precise percentages (`60%`, `25%`, `15%`) if core inputs (especially odds, injuries, lineup) are missing. Acceptable outputs are limited to:
  - **qualitative scenario** — directional descriptions ("more likely to win", "upset possible under specific conditions")
  - **directional probability band** — broad ranges without false precision ("low / medium / high", "unlikely / plausible / as likely as not")
  - **model-output with explicit caveat** — only if the method is disclosed and the missing-input limitation is stated in the same visual context as the output

- [ ] **probability table must include role labels** — every numeric probability, percentage range, or score distribution in a scoring/comparison table must carry one of:
  - `observed market-implied` — derived from actual odds
  - `proxy` — estimated from comparable events or historical baserates
  - `assumption` — author judgment or scenario assumption
  - `model-output` — result of a disclosed quantitative model (Poisson, logit, Monte Carlo, etc.)

### Worked example

For a match-level prediction where odds are available but lineup and weather are not confirmed:

> **Market-implied probability baseline**: odds of 1.50 / 4.00 / 7.00 → implied probabilities 67% / 25% / 14%.
> **Adjustment factors** (assumption): historical upset rate in similar tournament stages (~15%), key defender doubt (assumption: −5% to win probability).
> **Final band**: win probability 55–65% (assumption-adjusted, not confirmed).
> **Role labels**: `observed market-implied` for the 67/25/14 baseline; `assumption` for the −5% adjustment and for missing lineup confirmation.

Without the worked example, the reader cannot see how inputs were combined to produce the final probability.

### Integration with existing rules

- The scoring-replicability validator (`scripts/validate_scoring_replicability.py`) already enforces probability-to-evidence mapping and blocks opaque probability statements. This gate adds domain-specific input requirements that trigger before the replicability check.
- Source-strength gate (#341) enforces source quality for the inputs listed above. Odds from aggregators, injury news from press, and weather from general forecasts must carry appropriate reliability labels.
- Decision Scope block (#309) requires listing what would change the conclusion. This gate adds the pre-match input checklist as the minimum scope baseline for sports prediction tasks.

## Shortlist structure

- [ ] the shortlist or ranking appears before long option-by-option detail
- [ ] [BLOCKER] the shortlist boundary is justified — why these options were selected and what was excluded are explained
- [ ] the top option is named clearly
- [ ] the runner-up or best alternative is named clearly
- [ ] eliminated or weak-fit options are identified when useful
- [ ] the reader can see why one option wins and why the others lose
- [ ] the winning option is not just described positively; the report identifies the few load-bearing reasons it beats the runner-up under the stated constraints
- [ ] the runner-up is not just second by narration; the report states what weighting, scenario, or constraint shift would make it first
- [ ] eliminated options are rejected for specific decision reasons rather than fading out through lower narrative attention

## Evidence layers

- [ ] operational facts are separated from subjective reputation or user-sentiment claims
- [ ] medium-stability attributes are not presented with the same certainty as official hard constraints
- [ ] model synthesis / recommendation is distinguishable from raw source claims
- [ ] strong negative or positive reputation claims are scoped and not treated as hard facts by default
- [ ] source register must use the 7-column template (ID / Source Name / Source Type / Date / DOI or URL / Reliability / Claims Supported) defined in `references/source-traceability-and-claim-citation.md` (§Structured Source Register Template). 来源注册表必须使用该 7 列模板。
- [ ] [BLOCKER] All comparison, scoring, and estimation tables must include a numeric role column (or equivalent header row / table note), per `references/quantitative-role-labeling.md` §表格中的角色标签。所有比较表、评分表、估算表必须包含数字角色列（或等效的表头角色行/表注）。
- [ ] [BLOCKER] If >3 critical numbers in a scoring/ranking system lack role labels (observed / proxy / assumption / model-output) → hard-fail (see ROUTING-MATRIX.md §Constrained Choice hard-fail: `uses numbers without labeling observed fact / proxy / assumption / model output`). "关键数字"定义见 `references/quantitative-role-labeling.md` §What should be labeled（materially affect ranking / recommendation / sequencing / timing / valuation / confidence）。注意：辅助性描述数字（如"约 5 年"、"数万用户"）不受此规则限制。

### Career / skill selection sub-gate

When the constrained-choice task is about learning, career, skill-selection, or personal investment decisions (e.g., "which programming language to learn", "which framework to adopt", "which certificate to pursue"), add these checks:

- [ ] the report includes a default decision scope block (target reader experience level, geographic market, decision goal, time window, indicator roles, non-comparable items) as described in `references/option-selection-and-shortlist-discipline.md` §默认决策口径 — Default decision scope
- [ ] all job-market, salary, ranking, package-count, star, and survey-percentage numbers used for ranking carry role labels (observed / proxy / assumption / model-output) per the table in `references/option-selection-and-shortlist-discipline.md` §Common proxy indicators for career/skill selection
- [ ] Source Register Claims Supported column specifies what type of claim each source supports (job proxy / salary proxy / ecosystem size / official roadmap / community preference) rather than generic "supports language ranking"
- [ ] US job-posting or salary data is not presented as global career demand unless the report explicitly declares US-only scope
- [ ] if learning time estimates are used for ranking or cost comparison, each estimate is labeled as `estimate` / `assumption` / `model-output` with a brief basis note
- [ ] [BLOCKER] a career/skill selection report that lacks a default scope declaration AND uses unlabeled proxy indicators for >3 load-bearing ranking numbers → hard-fail. (Missing scope alone is a conditional pass floor; hard-fail requires the compound condition.)

## Scenario logic and change conditions

- [ ] the report identifies the main fragility points or disruption scenarios
- [ ] fallback options are given when the leading option is fragile
- [ ] the report states what would change the ranking or recommendation
- [ ] uncertainty is tied to the decision, not left as generic caveats
- [ ] if the recommendation depends on one dominant assumption, that dependency is visible near the recommendation rather than buried later
- [ ] if the route involves procurement, deployment, or physical movement, the report surfaces hidden friction in the same decision layer as price / performance / convenience rather than treating it as appendix detail
- [ ] if the route involves physical hardware procurement or build-stack recommendation as core output, the report includes a build-ready configuration table that surfaces hidden friction (power, noise, maintenance, backup) and build-ready components in the same decision layer as price/performance
- [ ] if the route involves multiple stakeholders or geographies, the report shows who is penalized by the winning option and why that penalty is still acceptable or not
- [ ] when the chosen option has major execution uncertainty, the report includes at least one post-decision branch with trigger condition and monitoring signal (see `references/decision-tree-method.md`)

## Decision usefulness

- [ ] the report helps the reader choose, not just learn about the options
- [ ] the recommendation is sharp enough to act on
- [ ] the reader can tell who or what is penalized by the recommended choice
- [ ] the next step is clear
- [ ] narrative weight is not distributed so evenly that the winning option, runner-up, and rejected options all feel equally plausible by reading time alone

## Background-first drift check

- [ ] the executive summary or judgment-first opening flows directly into the decision architecture or comparison framework, not into >5 lines of pure background description (venue context, event history, category overview, or similar)
- [ ] removing background paragraphs that immediately follow the opening judgment would sharpen rather than weaken the report

## Decision Scope visibility

- [ ] the report includes a visible Decision Scope block (target reader, option universe, shortlist boundary, exclusions, reversal conditions) after the executive summary / judgment block and before detailed analysis
- [ ] the Decision Scope block is present before route metadata or background exposition; if the first decision-relevant content after the summary is the decision scope rather than metadata, this check passes

## Quality bar

A selection report that fails this checklist may still be informative, but it is not yet strong decision support.
