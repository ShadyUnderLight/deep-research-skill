# Route Card: Provider / Vendor Selection

> **Generated view** — do not edit by hand. Canonical source: `schemas/route-manifest.json`. Regenerate with `python3 scripts/generate_route_cards.py`.

- **Route ID**: `provider-selection`
- **Category**: `specialized`
- **Aliases**: `provider selection`, `vendor selection`, `provider / vendor selection`
- **Full contract**: [`ROUTING-MATRIX.md`](../../ROUTING-MATRIX.md#route-provider--vendor-selection)
- **Compact index**: [`references/route-index.md`](../../references/route-index.md)

## Often confused with

- [`market-outlook`](market-outlook.md)
- [`equipment-selection`](equipment-selection.md)

## Primary reads

- [`references/option-selection-and-shortlist-discipline.md`](../option-selection-and-shortlist-discipline.md)
- [`references/source-traceability-and-claim-citation.md`](../source-traceability-and-claim-citation.md)
- [`references/decision-report-template.md`](../decision-report-template.md)

## Required disciplines

- `current-state`
- `source-traceability`
- `decision-utility`
- `quantitative-role`
- `data-conflict`

## Required audits

- [`option-selection-final-audit`](../../checklists/option-selection-final-audit.md)
- [`source-traceability`](../../checklists/source-traceability.md)
- [`final-audit`](../../checklists/final-audit.md)

## Trigger

Select among model/API suppliers, vendors or platforms and justify why one wins under explicit constraints.

## Do not use when

Task mainly describes the market or industry direction without a real selection burden; physical hardware / device procurement belongs to equipment-selection.

## Artifact contract

Current provider snapshot, decision criteria, ranked shortlist, why top option wins, why runner-up stays credible, why others lose, accessibility/compliance/SLA treatment when relevant.

## Failure signs (hard-fail keywords)

- `stale anchor products`
- `accessibility as side note`
- `vendor overview instead of choice memo`

## Hard-fail source

`ROUTING-MATRIX.md#provider-vendor-selection`

