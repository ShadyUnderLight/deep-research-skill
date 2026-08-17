# Route Card: Listed Company / Investment-style Research

> **Generated view** — do not edit by hand. Canonical source: `schemas/route-manifest.json`. Regenerate with `python3 scripts/generate_route_cards.py`.

- **Route ID**: `listed-company`
- **Category**: `specialized`
- **Aliases**: `listed company`, `investment-style research`, `listed company / investment-style research`
- **Full contract**: [`ROUTING-MATRIX.md`](../../ROUTING-MATRIX.md#route-listed-company--investment-style-research)
- **Compact index**: [`references/route-index.md`](../../references/route-index.md)

## Often confused with

- [`competitive-positioning`](competitive-positioning.md)

## Primary reads

- [`references/finance-date-discipline.md`](../finance-date-discipline.md)
- [`references/valuation-methodology.md`](../valuation-methodology.md)
- [`references/analyst-consensus-handling.md`](../analyst-consensus-handling.md)
- [`references/reporting-period-handling.md`](../reporting-period-handling.md)
- [`references/forward-looking-discipline.md`](../forward-looking-discipline.md)
- [`references/market-sizing-and-share-discipline.md`](../market-sizing-and-share-discipline.md)
- [`references/source-traceability-and-claim-citation.md`](../source-traceability-and-claim-citation.md)
- [`references/moat-monopoly-screening.md`](../moat-monopoly-screening.md)
- [`references/templates/listed-company-report.md`](../templates/listed-company-report.md)
- [`examples/listed-company-judgment-memo-example.md`](../../examples/listed-company-judgment-memo-example.md)
- [`examples/china-shenhua-reference-grade-rewrite-skeleton.md`](../../examples/china-shenhua-reference-grade-rewrite-skeleton.md)

## Required disciplines

- `current-state`
- `forward-looking`
- `source-traceability`
- `data-conflict`
- `scope-completeness`
- `decision-utility`
- `sensitivity-analysis`
- `quantitative-role`

## Required audits

- [`listed-company-report`](../../checklists/listed-company-report.md)
- [`source-traceability`](../../checklists/source-traceability.md)
- [`final-audit`](../../checklists/final-audit.md)

## Trigger

Listed-company, valuation, public-market, or investment-style memo judgment burden.

## Do not use when

Real question is a definition-sensitive positioning judgment rather than an investment-style memo.

## Artifact contract

Judgment-first opening, research-anchor block locking latest reported periods and market snapshot, dated key numbers, reported vs estimates separation, support/weakening/unresolved split, claim-level traceability, risks and counter-evidence, time-horizon valuation stratification when asked.

## Failure signs (hard-fail keywords)

- `mixed reported and forward estimates`
- `undated financial numbers`
- `missing research anchor`
- `missing market snapshot`
- `market-position without scope`
- `valuation substitutes for business evidence`
- `strong claims without evidence`
- `mixes monopoly moat scarcity`

## Hard-fail source

`ROUTING-MATRIX.md#listed-company-investment-style-research`

