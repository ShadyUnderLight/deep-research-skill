## Objective

Explain the market direction represented by the route-mismatch integration report [S01].

## Decision context

The report fixture deliberately declares Market Outlook while the canonical
activation snapshot resolves the selection burden to Constrained Choice. The
integration audit must block this disagreement.

## Primary route

Market Outlook

Closest alternative: Shared-workflow was rejected because the output requires
scenario structure. Switch if no specialized outlook burden remains.

## Action burden

Judge direction / scenario

## Weight-bearing object

Market / category trajectory

## Decision tree path

Steps 1-2 resolved to `market-outlook`; Step 3 verified; Step 4 not reached.

## Decision tree version

1

## Secondary disciplines

current-state, forward-looking, source-traceability, scope-completeness, quantitative-role, sensitivity-analysis

## Activation snapshot

- activation_id: forward-route-misclassification
- snapshot_sha256: 3bf7ccf7086d1eba693dc753bb633d6a009a13421f6424250bcf98a2c4b89a56
- snapshot_version: 1
- decision_tree_version: 1

## Core subquestions

What direction is supported, and what should be monitored?

## Stop condition

Stop when the current snapshot, scenarios, and monitoring signals are complete.

## Source register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|---|---|---|---|---|---|---|
| S01 | Existing snapshot | secondary | 2026-08-17 | https://example.com/snapshot | medium | current directional context |

## Claim register

| Claim | Source ID |
|---|---|
| The baseline direction is supported by the current snapshot | S01 |

## Uncertainty register

| Uncertainty | Why it matters |
|---|---|
| Scenario inputs may change | Monitoring signals determine when to revise |

## Artifact id

fixture-forward-route-misclassification

## Artifact contract

The artifact must show the current snapshot, scenarios, stakeholder implications,
and actionable monitoring signals.

## Research status

complete

## Delivery status

md_ready

## Required audits

- market-outlook-audit — passed — pack-section:Artifact contract
- forward-looking-claims — passed — pack-section:Artifact contract
- source-traceability — passed — pack-section:Artifact contract
- final-audit — passed — pack-section:Artifact contract

## Final audit status

Pass
