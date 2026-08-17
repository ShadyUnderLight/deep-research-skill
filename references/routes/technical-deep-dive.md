# Route Card: Technical Deep-dive / Architecture Analysis

> **Generated view** — do not edit by hand. Canonical source: `schemas/route-manifest.json`. Regenerate with `python3 scripts/generate_route_cards.py`.

- **Route ID**: `technical-deep-dive`
- **Category**: `specialized`
- **Aliases**: `technical deep-dive`, `architecture analysis`, `technical-deep-dive`
- **Full contract**: [`ROUTING-MATRIX.md`](../../ROUTING-MATRIX.md#route-technical-deep-dive--architecture-analysis)
- **Compact index**: [`references/route-index.md`](../../references/route-index.md)

## Often confused with

- [`equipment-selection`](equipment-selection.md)
- [`constrained-choice`](constrained-choice.md)
- [`market-outlook`](market-outlook.md)

## Primary reads

- [`references/technical-analysis-discipline.md`](../technical-analysis-discipline.md)
- [`references/source-traceability-and-claim-citation.md`](../source-traceability-and-claim-citation.md)
- [`references/forward-looking-discipline.md`](../forward-looking-discipline.md)

## Required disciplines

- `current-state`
- `source-traceability`
- `forward-looking`
- `quantitative-role`

## Required audits

- [`technical-analysis-audit`](../../checklists/technical-analysis-audit.md)
- [`source-traceability`](../../checklists/source-traceability.md)
- [`final-audit`](../../checklists/final-audit.md)

## Trigger

Technical judgment: understanding principles, evaluating feasibility, comparing architectures, assessing technology maturity or roadmaps.

## Do not use when

Task mainly selects a product or vendor (use provider-selection / equipment-selection), describes market evolution (market-outlook), or chooses among defined options (constrained-choice).

## Artifact contract

For principle/architecture/feasibility/roadmap/patent analysis: explicit question framing, dimension-by-dimension comparison or mechanism breakdown, trade-offs with load-bearing dimensions, evidence of viability, conditional recommendation with reversal criteria, announced vs shipped separation.

## Failure signs (hard-fail keywords)

- `technical survey without judgment`
- `compares architectures without dimensions`
- `stale technical state`
- `vendor claims as confirmed facts`
- `feasibility without viability evidence`
- `roadmaps without announced vs shipped separation`

## Hard-fail source

`ROUTING-MATRIX.md#technical-deep-dive-architecture-analysis`

