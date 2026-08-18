## Objective

Validate the process artifact paired with a report that omits a required manual audit [S01].

## Decision context

Shared-workflow is used only for a lightweight workflow review. The final audit
must still be declared and executed before the result is called complete.

## Primary route

Shared-workflow

Closest alternative: Technical Deep-dive was rejected because this fixture
tests the shared workflow spine. Switch if a technical judgment becomes the
load-bearing output.

## Secondary disciplines

none

## Core subquestions

Was the workflow spine complete and was the final audit actually run?

## Stop condition

Stop after the visible audit status block is checked.

## Source register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|---|---|---|---|---|---|---|
| S01 | Workflow note | secondary | 2026-08-17 | https://example.com/workflow | medium | workflow context |

## Claim register

| Claim | Source ID |
|---|---|
| The workflow context is available for review | S01 |

## Uncertainty register

| Uncertainty | Why it matters |
|---|---|
| Final audit is absent from the report block | Completion cannot be trusted |

## Artifact id

fixture-shared-workflow-neg

## Artifact contract

The report must show workflow-spine and final-audit execution separately.

## Research status

complete

## Delivery status

md_ready

## Required audits

- workflow-spine-audit — passed — pack-section:Artifact contract
- final-audit — passed — pack-section:Artifact contract

## Final audit status

Pass
