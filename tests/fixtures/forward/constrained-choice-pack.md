## Objective

Choose one option from a defined option set under a fixed deployment constraint [S01].

## Decision context

The task asks which option should win. Equipment-selection was rejected because
the task has no purchase-ready hardware or build constraint; it would apply if
the question changed to a hardware procurement decision.

## Primary route

Constrained Choice / Shortlist

Closest alternative: Equipment Selection was rejected because the user asks
which defined option to choose rather than what hardware to buy. Switch if the
task gains a purchase-ready hardware and budget burden.

## Action burden

Select / rank / predict

## Weight-bearing object

Defined options / teams / ranking

## Decision tree path

Steps 1-2 resolved to `constrained-choice`; Step 3 verified; Step 4 not reached.

## Secondary disciplines

decision-utility, quantitative-role

## Core subquestions

Which option wins under the stated comparison unit, and what changes the choice?

## Stop condition

Stop when all defined options are compared on the load-bearing dimensions.

## Source register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|---|---|---|---|---|---|---|
| S01 | Option documentation | PRIMARY_DEV | 2026-08-17 | https://example.com/option | medium | option constraints |

## Claim register

| Claim | Source ID |
|---|---|
| Option A fits the deployment constraint | S01 |

## Uncertainty register

| Uncertainty | Why it matters |
|---|---|
| Access terms may change | It could reverse the choice |

## Artifact id

forward-constrained-choice

## Artifact contract

The final artifact must show the option universe, comparison unit, winner,
runner-up, and reversal condition.

## Research status

complete

## Delivery status

md_ready

## Required audits

- option-selection-final-audit — passed: option universe and comparison unit checked
- final-audit — passed: conclusion and reversal condition visible

## Final audit status

Pass
