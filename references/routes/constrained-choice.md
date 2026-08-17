# Route Card: Constrained Choice / Shortlist / Option Selection

> **Generated view** — do not edit by hand. Canonical source: `schemas/route-manifest.json`. Regenerate with `python3 scripts/generate_route_cards.py`.

- **Route ID**: `constrained-choice`
- **Category**: `specialized`
- **Aliases**: `constrained choice`, `constrained choice / shortlist`, `shortlist`, `option selection`, `constrained choice / shortlist / option selection`
- **Full contract**: [`ROUTING-MATRIX.md`](../../ROUTING-MATRIX.md#route-constrained-choice--shortlist--option-selection)
- **Compact index**: [`references/route-index.md`](../../references/route-index.md)

## Often confused with

- [`market-entry`](market-entry.md)
- [`equipment-selection`](equipment-selection.md)

## Primary reads

- [`references/option-selection-and-shortlist-discipline.md`](../option-selection-and-shortlist-discipline.md)
- [`references/decision-report-template.md`](../decision-report-template.md)

## Required disciplines

- `decision-utility`
- `quantitative-role`

## Required audits

- [`option-selection-final-audit`](../../checklists/option-selection-final-audit.md)
- [`final-audit`](../../checklists/final-audit.md)

## Trigger

Choose among defined options using a visible comparison unit, shortlist logic, and ranking-change conditions; includes outcome-ranking / probability-distribution tasks.

## Do not use when

Real task is market-entry gating, expansion sequencing, or broad market scanning.

## Artifact contract

Decision architecture, shortlist construction logic, comparison unit, final ranking, why top option wins, why runner-up stays credible, ranking-reversal conditions, hidden operational burdens when relevant.

## Failure signs (hard-fail keywords)

- `recommendation without shortlist`
- `unlabeled numbers`
- `descriptive blurbs instead of choice memo`
- `background-first drift`

## Hard-fail source

`ROUTING-MATRIX.md#constrained-choice-shortlist-option-selection`

