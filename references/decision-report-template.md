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
3. Ranked shortlist or best-fit options
4. Why the top option wins
5. Why the next-best option remains credible
6. Why the other options lose
7. Risks, fallback options, and what would change the ranking
8. Recommended next steps
9. Sources

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
