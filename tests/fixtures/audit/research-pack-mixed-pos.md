## Objective

Determine X, grounded on [S01].

## Decision context

Context with boundary judgment: chosen over alternative Y, rejected because
scope mismatch; would become relevant if market conditions change.

## Primary route

Market Outlook

Market Outlook selected as primary route. The closest alternative,
shared-workflow, was rejected because this task needs scenario structure.
Boundary: if monitoring signals are not required, shared-workflow would apply.

## Secondary disciplines

- none

## Core subquestions

- Q1

## Stop condition

Stop when evidence saturated.

## Source register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Example A | secondary | 2026-01-01 | https://example.com/a | medium | §3 |

## Claim register

| Claim | Source ID |
|-------|-----------|
| C1 | S01 |

## Uncertainty register

| Uncertainty | Source ID |
|-------------|-----------|
| U01 | S01 |

## Artifact id

fixture-market-outlook-mixed-pos

## Artifact contract

| Field | Value |
|-------|-------|
| artifact_id | fixture-market-outlook-mixed-pos |

## Required audits

- market-outlook-audit — passed: executed by author
- forward-looking-claims — passed: no mislabeled claims
- source-traceability — passed: register complete
- final-audit — passed: all gates verified

## Final audit status

Pass
