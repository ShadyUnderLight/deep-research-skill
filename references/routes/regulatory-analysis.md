# Route Card: Regulatory / Policy Impact Analysis

> **Generated view** — do not edit by hand. Canonical source: `schemas/route-manifest.json`. Regenerate with `python3 scripts/generate_route_cards.py`.

- **Route ID**: `regulatory-analysis`
- **Category**: `specialized`
- **Aliases**: `regulatory analysis`, `regulatory / policy impact`, `regulatory / policy impact analysis`
- **Full contract**: [`ROUTING-MATRIX.md`](../../ROUTING-MATRIX.md#route-regulatory--policy-impact-analysis)
- **Compact index**: [`references/route-index.md`](../../references/route-index.md)

## Often confused with

- [`listed-company`](listed-company.md)
- [`market-outlook`](market-outlook.md)

## Primary reads

- [`references/current-state-verification.md`](../current-state-verification.md)
- [`references/forward-looking-discipline.md`](../forward-looking-discipline.md)
- [`references/source-quality.md`](../source-quality.md)
- [`references/data-conflict-resolution.md`](../data-conflict-resolution.md)
- [`references/rule-system-and-mechanism-add-on.md`](../rule-system-and-mechanism-add-on.md)

## Required disciplines

- `current-state`
- `source-traceability`
- `forward-looking`
- `scope-completeness`

## Required audits

- [`regulatory-analysis-audit`](../../checklists/regulatory-analysis-audit.md)
- [`source-traceability`](../../checklists/source-traceability.md)
- [`final-audit`](../../checklists/final-audit.md)

## Trigger

Assess the regulatory environment, policy risk, or compliance impact on a business or industry.

## Do not use when

Regulation is background context only; or the primary burden is listed-company valuation, market-entry sequencing, or technical feasibility (attach regulatory analysis as secondary discipline instead).

## Artifact contract

Current regulatory snapshot, pending legislation, business impact analysis, timeline, uncertainty bounds, scenario analysis, monitoring signals, actionable implications.

## Failure signs (hard-fail keywords)

- `regulations without business impact`
- `regulatory text confused with media`
- `false precision on timing`
- `ignored enforcement reality`
- `jurisdictions treated as equivalent`
- `binary risk instead of graduated`

## Hard-fail source

`ROUTING-MATRIX.md#regulatory-policy-impact-analysis`

