# Decision Report Template

Use this template when the research should support a judgment, recommendation, comparison, prioritization, or next action.

## Core rule

The report should answer:

- What is the best current judgment?
- Why is that the best current judgment?
- How confident is it?
- What could change it?
- What should the user do next?

When the task is a constrained choice among several plausible options, also read `references/option-selection-and-shortlist-discipline.md`.
In those cases, the report is not just a recommendation memo — it must show the choice architecture clearly enough that the reader can see why option A beats option B under the stated constraints.

## Recommended structure

### Load-bearing numbers and their role

If recommendation, ranking, sequencing, or valuation materially depends on numbers, show which are observed metrics, proxies, assumptions, or model outputs.

1. Executive summary
2. What matters most
3. Bottom-line judgment or recommendation
4. Key findings
5. Detailed analysis
6. Risks and counter-evidence
7. Uncertainty and missing evidence
8. What would change the conclusion
9. Recommended next steps
10. Sources

For option-selection / shortlist tasks, adapt the middle of the structure like this:

1. Executive summary
2. What matters most
3. Decision architecture
4. Ranked shortlist or best-fit options
5. Why the top option wins
6. Why the next-best option remains credible
7. Why the other options lose
8. Risks, fallback options, and what would change the ranking
9. Recommended next steps
10. Sources

In these option-selection / shortlist cases:
- make the shortlist-construction logic visible rather than jumping straight to the final ranking
- if multiple stakeholders, origins, or user groups are involved, show how fairness enters the recommendation instead of only saying that fairness matters
- if quantitative scoring or composite comparison is used, label what is an observed fact, what is a proxy, what is an assumption, and what is a model output
- do not let "runner-up" become just a second-place description; explain what weighting or scenario would make it first
- express uncertainty as change-the-ranking or ranking-reversal conditions when possible, not only as generic caveats

For market-outlook / industry-evolution / "未来12个月如何演化" tasks, prefer this stronger structure:

1. Executive summary
2. Decision architecture
3. Current market snapshot
4. What matters most
5. Key drivers of change
6. Key blockers or friction points
7. Base case for the next 6-12 months
8. Alternative scenarios and what shifts them
9. Stakeholder implications (for example buyers / builders / investors / operators)
10. What would change the conclusion
11. Recommended next steps
12. Sources

In these market-outlook cases:
- do not let the report remain a background industry overview
- make the time horizon visible in section headers and claims
- separate observed current state from scenario logic and illustrative estimates
- if quantitative outlook numbers are used, label them as observed / inferred / scenario assumption / illustrative calculation
- ensure the report answers who should act now, how, and what to monitor

For model/API supplier or provider-selection tasks, prefer this stronger structure:

1. Executive summary
2. Decision architecture
3. What matters most
4. Current snapshot table
5. Ranked shortlist
6. Why the top option wins
7. Why the runner-up remains credible
8. Why the other options lose
9. Recommended deployment archetypes
10. Risks / what changes the ranking
11. Sources

In these provider-selection cases, the report should explicitly show current-state load-bearing variables such as:
- current primary model/API family
- current pricing unit and pricing caveats
- current support-region / mainland accessibility reality
- current data-control / retention posture
- current SLA / status / enterprise controls when decision-relevant

For first-tier / top-tier / multidimensional positioning tasks, prefer this stronger structure:

1. Executive summary
2. Scope / metric / timeframe
3. Decision architecture for the tier judgment
4. Dimension-by-dimension conclusions
5. Where direct evidence is strong vs where inference carries the argument
6. Whether an overall tier label is justified
7. Why the strongest rival classification remains credible
8. Open uncertainty / what could move the classification
9. Sources

In these multidimensional-positioning cases:
- do not treat `first-tier` as a loose compliment; define what dimensions are load-bearing before judging
- separate geography, product scope, and time basis before comparing players
- keep dimension-level judgments visible when evidence strength differs across dimensions
- do not let roadmap products, self-tests, valuation signals, or regional leadership silently substitute for current global product/commercial leadership
- if an overall label is still used, show the rule that permits collapsing multiple dimensions into one classification

## Company / equity-style decision reports

When the task is primarily about evaluating a company, competitive position, or investment-style thesis, do not default to a background-first company overview.

Prefer this front structure:

1. Core thesis
2. What matters most now
3. Main evidence supporting the thesis
4. Main evidence weakening the thesis
5. Key unknowns and why they matter
6. What to watch next
7. Only then: business background, segment detail, products, roadmap, customers, and competitors

Background, segment description, roadmap detail, and customer examples should appear only insofar as they sharpen the current thesis, not as default report ballast.

Under "What matters most now", prefer to surface:
- which business line or driver most shapes the current view
- which 2-4 disclosures or metrics matter most next
- which facts would most strengthen or weaken the thesis

For equipment-selection / procurement / home-server-planning tasks, prefer this stronger structure:

1. Executive summary
2. What is the real purchase or build decision?
3. Dominant constraints
4. Top recommendation
5. Credible runner-up and why it did not win
6. Rejected routes and why
7. Minimum viable configuration
8. Recommended configuration
9. Budget assumptions and what is included or excluded
10. Hardware ↔ system fit
11. Long-run operating costs and friction
12. Upgrade path or when to split workloads
13. What would change the recommendation
14. Sources

In these equipment-selection / procurement cases:
- do not let the report become a route overview with a recommendation attached at the end
- make the dominant constraint visible, such as budget, quiet operation, storage density, data safety, media capability, low maintenance, or virtualization flexibility
- show why the top route wins, why the runner-up remains credible, and why rejected routes lose under the stated constraints
- separate minimum viable configuration from recommended configuration when budget or complexity materially changes the answer
- make budget assumptions explicit, especially drives, UPS, networking upgrades, accessories, and whether long-run power or maintenance costs are included
- bind hardware route to system choice rather than listing operating systems as a detached appendix
- treat power, noise, maintenance burden, backup overhead, and expansion friction as ranking variables when the task is household or always-on planning
- if power, cost, payback, storage growth, or scoring numbers are used, label observed values vs estimates vs assumptions vs planning-model outputs
- if the report is in Chinese, keep load-bearing labels in Chinese and ensure PDF readability is not degraded by broken export spacing

For market-entry / regional-expansion / country-prioritization tasks, prefer this stronger structure:

1. Executive summary
2. What is the real decision?
3. Recommendation
4. Why now / why not now
5. Hard gates
6. Country shortlist with unified comparison unit
7. Recommended sequencing
8. Recommended entry archetypes
9. Why the top option wins
10. Why the runner-up remains credible
11. Why the other options lose
12. Risks / what changes the decision
13. 0-12 month milestones or KPIs
14. Sources

In these market-entry cases:
- do not let the report become a regional market overview with a recommendation attached at the end
- explicitly separate regional hub, first revenue beachhead, and later expansion market when those roles differ
- make priority relative to alternatives visible (for example domestic market vs SEA, or SEA vs other expansion regions)
- show the few hard gates that could turn `go` into `not now` or `pilot only`
- show why the top option wins, why the runner-up remains credible, and what would change the ranking
- make KPI / milestone triggers visible when they are part of the operating path
- use one comparison unit across countries or candidate markets rather than free-form prose by country
- if TAM / SAM / SOM, scenario models, or KPI plans are used, label observed numbers vs proxies vs assumptions vs planning-model outputs
- if the final memo is written in Chinese, keep load-bearing labels in Chinese too rather than leaking English evidence buckets into the body

Do not give every option equal narrative weight if the user's real need is to choose.

## Executive summary

State:

- the main answer in plain language
- the strongest reasons behind it
- the confidence level
- the biggest caveat

## What matters most

Highlight the few variables that actually drive the conclusion.

Examples:

- distribution matters more than feature parity
- time-to-market matters more than technical elegance
- regulatory timing matters more than category excitement

For option-selection tasks, explicitly separate:

- the primary comparison unit
- the aggregation logic (average / median / max burden / fairness / weighted user)
- any subgroup that should not be hidden inside one blended score

If the report says one option is "best" but does not reveal how the comparison was aggregated, the decision logic is still too opaque.

## Bottom-line judgment

State the conclusion clearly.

Useful patterns:

- `The best current conclusion is:`
- `The best-fit option is:`
- `The recommendation is to buy / build / partner because:`
- `The approach appears feasible / conditionally feasible / not yet viable because:`

## Key findings

For each major finding, include:

- the finding
- why it matters
- confidence
- strongest evidence
- whether it is confirmed fact or inference

## Risks and counter-evidence

Include:

- strongest counter-evidence
- strongest alternative explanation
- hidden costs or trade-offs
- where the conclusion may not generalize

## Uncertainty and missing evidence

State:

- main unresolved questions
- confidence limits
- most important missing evidence
- what public sources do not clearly show

## What would change the conclusion

Spell out what future evidence would materially change the judgment.

For option-selection tasks, include concrete change conditions such as:

- one stakeholder or subgroup becoming more important than the others
- a budget ceiling tightening or loosening
- a key operational step becoming fragile (for example transport, availability, regulation, weather, or integration)
- the fallback option becoming preferable under disruption

A strong selection report should not only say what wins now; it should also say when the ranking would change.

## Recommended next steps

Give concrete, low-regret next actions tied to the decision context.

## Confidence scale

Use a simple label when useful:

- High
- Medium
- Low

Do not use high confidence casually on fast-moving topics.
