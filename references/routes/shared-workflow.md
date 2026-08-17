# Route Card: Shared-workflow (no specialized route selected)

> **Generated view** — do not edit by hand. Canonical source: `schemas/route-manifest.json`. Regenerate with `python3 scripts/generate_route_cards.py`.

- **Route ID**: `shared-workflow`
- **Category**: `shared-workflow`
- **Aliases**: `shared-workflow`, `shared workflow`, `shared-workflow (no specialized route selected)`
- **Full contract**: [`ROUTING-MATRIX.md`](../../ROUTING-MATRIX.md#route-shared-workflow-no-specialized-route-selected)
- **Compact index**: [`references/route-index.md`](../../references/route-index.md)

## Often confused with

- [`constrained-choice`](constrained-choice.md)

## Primary reads

- [`references/route-activation-and-preflight.md`](../route-activation-and-preflight.md)
- [`references/source-traceability-and-claim-citation.md`](../source-traceability-and-claim-citation.md)

## Required audits

- [`workflow-spine-audit`](../../checklists/workflow-spine-audit.md)
- [`final-audit`](../../checklists/final-audit.md)

## Trigger

No specialized route fits and the task has no option universe, ranking, probability, or selection burden; lightweight fact query.

## Do not use when

Task fits a specialized route but it is avoided for convenience (escape-hatch misuse).

## Artifact contract

Workflow spine audit plus final audit; no route-specific artifact contract beyond the shared delivery contract.

## Failure signs (hard-fail keywords)

- `specialized route escape hatch misuse`
- `missing workflow-spine-audit`

## Hard-fail source

`references/route-index.md#shared-workflow`

