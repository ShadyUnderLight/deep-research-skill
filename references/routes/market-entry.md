# Route Card: Market Entry / Regional Expansion

> **Generated view** — do not edit by hand. Canonical source: `schemas/route-manifest.json`. Regenerate with `python3 scripts/generate_route_cards.py`.

- **Route ID**: `market-entry`
- **Category**: `specialized`
- **Aliases**: `market entry`, `regional expansion`, `market entry / regional expansion`
- **Full contract**: [`ROUTING-MATRIX.md`](../../ROUTING-MATRIX.md#route-market-entry--regional-expansion)
- **Compact index**: [`references/route-index.md`](../../references/route-index.md)

## Often confused with

- [`constrained-choice`](constrained-choice.md)

## Primary reads

- [`references/option-selection-and-shortlist-discipline.md`](../option-selection-and-shortlist-discipline.md)
- [`references/decision-report-template.md`](../decision-report-template.md)
- [`references/source-traceability-and-claim-citation.md`](../source-traceability-and-claim-citation.md)

## Required disciplines

- `current-state`
- `source-traceability`
- `decision-utility`
- `quantitative-role`
- `sensitivity-analysis`

## Required audits

- [`option-selection-final-audit`](../../checklists/option-selection-final-audit.md)
- [`source-traceability`](../../checklists/source-traceability.md)
- [`final-audit`](../../checklists/final-audit.md)

## Trigger

Decide whether to enter a market, where to enter first, when, or how to sequence entry under constrained budget.

## Do not use when

Task is mainly a generic market overview or a simple option comparison without real entry logic.

## Artifact contract

Explicit go / not-now / pilot-only recommendation, country shortlist, hard gates, sequencing, two-level decision funnel (regional screening → country competition → beachhead), country diligence cards, sensitivity/switching table, recommendation-constraint consistency.

## Failure signs (hard-fail keywords)

- `generic market overview`
- `country notes without unified comparison`
- `expansion without hard gates`
- `collapses hub beachhead expansion`
- `skips country-competition stage`
- `inconsistent country diligence`
- `recommendation-constraint mismatch`

## Hard-fail source

`ROUTING-MATRIX.md#market-entry-regional-expansion`

