# Quantitative Role Audit

## Core gate

If load-bearing numbers materially affect the conclusion, their roles should be visible.

## Checklist

- Are the report's load-bearing numbers identifiable?
- Is each load-bearing number distinguishable as observed metric, proxy, assumption, model output, or illustrative calculation?
- Are proxies prevented from masquerading as direct evidence?
- Are model outputs prevented from masquerading as observed facts?
- Where recommendation or ranking depends on scoring or estimation, are the roles of the inputs visible?
- Does uncertainty treatment match the role of the number?
- If assumptions changed, would the conclusion visibly change? If yes, are those assumptions labeled clearly enough?

## Assumption chain checks

- Each high-sensitivity assumption has a complete assumption chain (supporting evidence, dependency conditions, sensitivity, failure signals, confidence). If the chain cannot be fully populated, one of the following must apply: (a) fill the chain from available evidence, (b) downgrade the assumption's sensitivity classification, or (c) restructure the analysis to reduce dependence on that assumption. Do not leave the chain incomplete without an explicit remediation decision.
- The dependency conditions in each assumption chain are reasonable for the context.
- The failure signals in each assumption chain are observable and actionable (not generic disclaimers).

## Sensitivity analysis checks

- [BLOCKER] If the conclusion depends 30% or more on a single numerical assumption, has that assumption been classified by sensitivity level (low / medium / high)?
- [BLOCKER] High-sensitivity assumptions have a visible sensitivity table with at least ±20% and one wider amplitude (±50% or extreme scenario).
- [NON-BLOCKER] Medium-sensitivity assumptions have at least the tipping point documented (the deviation at which the conclusion would change direction).
- [NON-BLOCKER] The report states which assumptions are most load-bearing and what would change the conclusion.

## Hard fail signs

- Numerical precision exceeds source certainty.
- A model output is written as a fact.
- An unlabeled assumption carries the recommendation.
- Numbers from different epistemic roles are mixed without distinction.
