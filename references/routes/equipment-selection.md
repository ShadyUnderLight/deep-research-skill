# Route Card: Equipment Selection / Procurement / Home-server Planning

> **Generated view** — do not edit by hand. Canonical source: `schemas/route-manifest.json`. Regenerate with `python3 scripts/generate_route_cards.py`.

- **Route ID**: `equipment-selection`
- **Category**: `specialized`
- **Aliases**: `equipment selection`, `equipment selection / procurement`, `equipment selection / procurement / home-server planning`, `procurement`, `home-server planning`, `nas`, `nas / home server`, `homelab`
- **Full contract**: [`ROUTING-MATRIX.md`](../../ROUTING-MATRIX.md#route-equipment-selection--procurement--home-server-planning)
- **Compact index**: [`references/route-index.md`](../../references/route-index.md)

## Often confused with

- [`constrained-choice`](constrained-choice.md)
- [`market-outlook`](market-outlook.md)

## Primary reads

- [`references/decision-report-template.md`](../decision-report-template.md)
- [`references/option-selection-and-shortlist-discipline.md`](../option-selection-and-shortlist-discipline.md)
- [`references/source-traceability-and-claim-citation.md`](../source-traceability-and-claim-citation.md)

## Required disciplines

- `current-state`
- `decision-utility`
- `quantitative-role`
- `source-traceability`

## Required audits

- [`option-selection-final-audit`](../../checklists/option-selection-final-audit.md)
- [`final-audit`](../../checklists/final-audit.md)

## Trigger

Produce a purchase-ready or build-ready hardware/device recommendation under visible budget, maintenance, noise, power, storage, networking, or expansion constraints.

## Do not use when

Task mainly explains hardware categories, compares benchmarks abstractly, or teaches general technical concepts without a real procurement burden.

## Artifact contract

Real purchase/build decision, dominant constraints, workload segmentation, top recommendation, credible runner-up, rejected routes, minimum-viable vs recommended config, budget assumptions, hardware-system fit, operating tradeoffs, what would change the recommendation.

## Failure signs (hard-fail keywords)

- `hardware overview instead of procurement`
- `budget without inclusion assumptions`
- `hardware and system not bound`
- `operating costs as side notes`
- `fails to segment workload`
- `benchmark performance without method disclosure`

## Hard-fail source

`ROUTING-MATRIX.md#equipment-selection-procurement-home-server-planning`

