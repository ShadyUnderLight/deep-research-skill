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
- [ ] the aggregation logic is visible when multiple people, teams, or regions are involved
- [ ] the report states whether it is optimizing for average outcome, fairness, worst-case burden, weighted priority user, or robustness
- [ ] subgroup views are shown when one average would hide an important outlier or penalty
- [ ] if quantitative or composite scoring is used, the report distinguishes observed facts, proxies, assumptions, and model outputs rather than presenting them as one evidence layer
- [ ] if fairness is load-bearing, the report makes clear whether unfairness is being measured by worst-off participant, dispersion/variance, hidden subgroup penalties, or another explicit rule
- [ ] hidden operational burden layers (for example transfer burden, cross-border friction, checkpoint/visa hassle, fragile first/last-mile routing) are surfaced when they materially affect the ranking

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

## Shortlist structure

- [ ] the shortlist or ranking appears before long option-by-option detail
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

## Scenario logic and change conditions

- [ ] the report identifies the main fragility points or disruption scenarios
- [ ] fallback options are given when the leading option is fragile
- [ ] the report states what would change the ranking or recommendation
- [ ] uncertainty is tied to the decision, not left as generic caveats
- [ ] if the recommendation depends on one dominant assumption, that dependency is visible near the recommendation rather than buried later
- [ ] if the route involves procurement, deployment, or physical movement, the report surfaces hidden friction in the same decision layer as price / performance / convenience rather than treating it as appendix detail
- [ ] if the route involves multiple stakeholders or geographies, the report shows who is penalized by the winning option and why that penalty is still acceptable or not

## Decision usefulness

- [ ] the report helps the reader choose, not just learn about the options
- [ ] the recommendation is sharp enough to act on
- [ ] the reader can tell who or what is penalized by the recommended choice
- [ ] the next step is clear

## Quality bar

A selection report that fails this checklist may still be informative, but it is not yet strong decision support.
