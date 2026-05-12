# Research Pack Example

## Example task

Choose the most suitable meetup city for a small team traveling from multiple origins and explain what could change the ranking.

## Compact example

## Objective
Select the best meetup city under practical travel and coordination constraints.

## Decision context
The task is a constrained-choice memo, not a travel overview. The answer should support a real choice rather than describe cities broadly.

## Primary route
Constrained choice / shortlist

## Secondary disciplines
- source traceability
- quantitative role labeling
- counter-evidence

## Core subquestions
- Which comparison unit best fits the real choice?
- Which city wins under that comparison unit?
- Which runner-up remains credible?
- What uncertainty could change the ranking?

## Stop condition
Stop when the top choice, runner-up logic, and ranking-change conditions are supported well enough for a practical recommendation.

## Degraded-search log
- Search objective: current transport and logistics sources for candidate meetup cities
- Primary provider attempted: MiniMax web search
- Fallback trigger: low-yield results for practical source discovery
- Fallback provider used: Exa
- Why this fallback fits better: broader discovery of current web sources for schedules and logistics pages
- Candidate-source quality: mixed
- Claims still needing primary-page verification: exact transport timing, current venue constraints
- Live-search status: partially recovered

## Source register
- [S01] Source: transport schedule / route information
  - Supports: travel feasibility and burden comparison
- [S02] Source: venue / city logistics information
  - Supports: practical meetup suitability
- [S03] Source: pricing or timing references
  - Supports: cost and coordination burden

## Claim register
- Claim: City A is the best default meetup choice under current assumptions. [S01][S02]
  - Support: lower coordination burden across origins, stronger schedule fit
  - Confidence: medium
- Claim: City B remains the strongest runner-up. [S01][S03]
  - Support: similar accessibility with weaker logistics fit
  - Confidence: medium

## Uncertainty register
- Uncertainty: actual day-of-travel schedule variation
  - Why it matters: could change the ranking if timing shifts materially
- Uncertainty: venue-side constraints
  - Why it matters: could weaken the current top option

## Counter-evidence log
- Possible weakening factor: schedule changes reduce City A's accessibility advantage
- Possible alternative explanation: the current winner depends too heavily on assumed transfer burden

## Artifact contract
The final memo should visibly show the comparison unit, top choice, runner-up logic, ranking-change conditions, and uncertainty that can move the decision.

## Required audits
- final audit
- quantitative role audit

## Final audit status
Pass
