## Objective

Validate the process artifact paired with a report that omits secondary-route verification [S01].

## Decision context

Market Outlook is primary. The secondary constrained-choice route is relevant
and must have an independent hard-fail audit entry.

## Primary route

Market Outlook

Closest alternative: Shared-workflow was rejected because the task has an
outlook burden. The secondary constrained-choice check is recorded separately.

## Action burden

Judge direction / scenario

## Weight-bearing object

Market / category trajectory

## Decision tree path

Steps 1-2 resolved to `market-outlook`; Step 3 verified; Step 4 not reached.

## Secondary disciplines

current-state, forward-looking, source-traceability, scope-completeness, quantitative-role, sensitivity-analysis

## Core subquestions

What does the market outlook show, and was every declared route independently checked?

## Stop condition

Stop after the route and audit declarations are inspected.

## Source register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|---|---|---|---|---|---|---|
| S01 | Existing snapshot | secondary | 2026-08-17 | https://example.com/snapshot | medium | current directional context |

## Claim register

| Claim | Source ID |
|---|---|
| The process artifact is complete enough to inspect | S01 |

## Uncertainty register

| Uncertainty | Why it matters |
|---|---|
| Secondary audit entry is absent in the report contract | The secondary route may be falsely treated as verified |

## Artifact id

fixture-market-outlook-mixed-neg

## Artifact contract

The artifact must expose the missing secondary hard-fail verification.

## Research status

complete

## Delivery status

md_ready

## Required audits

- market-outlook-audit — passed: primary route structure inspected
- forward-looking-claims — passed: labels inspected
- source-traceability — passed: claims map to the register
- final-audit — passed: process artifact reviewed

## Final audit status

Pass
