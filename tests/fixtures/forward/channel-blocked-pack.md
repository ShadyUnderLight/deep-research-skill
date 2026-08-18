## Objective

Assess the provider category with a degraded external channel and preserve the
impact on the research conclusion [S01].

## Decision context

Market Outlook was chosen over shared-workflow because the task needs scenario
structure. The external channel is blocked, so the research status is blocked
even though the available artifact can still be audited.

## Primary route

Market Outlook

Closest alternative: Shared-workflow was rejected because the task has a market
trajectory burden. Switch if no specialized outlook structure is required.

## Action burden

Judge direction / scenario

## Weight-bearing object

Market / category trajectory

## Decision tree path

Steps 1-2 resolved to `market-outlook`; Step 3 verified; Step 4 not reached.

## Secondary disciplines

current-state, forward-looking, source-traceability, scope-completeness, quantitative-role, sensitivity-analysis

## Core subquestions

What direction is supported by the available evidence, and what remains unverified?

## Stop condition

Stop after recording the channel limitation and its effect on confidence.

## Source register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|---|---|---|---|---|---|---|
| S01 | Existing snapshot | secondary | 2026-08-17 | https://example.com/snapshot | medium | current directional context |

## Claim register

| Claim | Source ID |
|---|---|
| Directional evidence remains usable | S01 |

## Uncertainty register

| Uncertainty | Why it matters |
|---|---|
| External channel unavailable | Current-state confirmation is incomplete |

## Channel availability snapshot

- api_available: false
- api_version: not-available
- checked_at: 2026-08-17T10:00:00+08:00
- channels_ok: 0
- channels_total: 2
- selected_channels: [search, fetch]
- degraded_channels: [search, fetch]
- impact_on_research: Current-state confirmation is blocked; conclusions remain directional.

## Artifact id

fixture-market-outlook-pos

## Artifact contract

The artifact must disclose the blocked channel and avoid upgrading unavailable
current-state facts into confirmed claims.

## Research status

blocked

## Delivery status

md_ready

## Required audits

- market-outlook-audit — passed — pack-section:Artifact contract
- forward-looking-claims — passed — pack-section:Artifact contract
- source-traceability — passed — pack-section:Artifact contract
- final-audit — passed — pack-section:Artifact contract

## Final audit status

Pass
