# Eval: Intel Listed-Company Freshness Hard Gate Case

## Goal

Test whether a listed-company deep-research report dated in 2026 can still silently anchor itself on 2024 and 2025 Q1 material as if those were the current baseline.

This eval targets a recurring failure mode:

- the report looks structured and evidence-aware
- many numbers are real
- but the opening thesis is anchored on stale reporting periods and stale market snapshots rather than the newest reasonably available reported periods at the report date

## Real failure pattern

A user-provided Intel report dated **2026-04-13** still described **2025 Q1** as the "latest financial" period and relied heavily on older 2024 / early-2025 snapshots for:

- financial performance anchors
- market-share context
- target-price / consensus framing
- foundry scale framing
- product / roadmap state

The problem was not total fabrication. The problem was that older but plausible data became the memo's de facto current-state anchor.

## What this eval is testing

### Failure Mode 1: stale reporting-period anchor

The report date is materially later than the supposedly latest figures used.

For example:
- report dated 2026-04
- memo still treats 2025 Q1 as "latest financial"

This should trigger a hard freshness re-check before synthesis.

### Failure Mode 2: older market snapshots presented as current state

Older figures such as:
- old market share snapshots
- old analyst target-price snapshots
- old valuation or ownership snapshots
- old product or roadmap milestone wording

may still be useful as background, but they must not silently function as the current-state baseline.

### Failure Mode 3: broad company analysis starts before current-state lock

The model begins writing business, competition, and thesis sections before explicitly locking:
- latest full-year reported period
- latest quarterly / interim reported period
- latest current market snapshot date
- latest leadership / management state when decision-relevant

## Pass criteria

A good answer should:

1. lock the current time layers before broad synthesis
   - latest full-year reported period
   - latest quarterly / interim reported period
   - latest current market snapshot date

2. treat stale-but-plausible anchors as a hard failure condition
   - if the memo date is materially later than the allegedly latest period, re-check first
   - do not continue as if the old anchor were acceptable

3. downgrade older but useful data visibly
   - historical background
   - prior-cycle comparison
   - older market snapshot

4. make the opening section reflect the newest verified reporting layer rather than an easier older snapshot

## Failure signs

Mark this eval as failed if the answer does any of the following:

- calls an older quarter or fiscal year the "latest" when newer reported periods should already exist
- uses older market-share, target-price, or analyst-snapshot data as if it were the current baseline
- lets a stale opening snapshot determine the whole memo's framing
- includes many real numbers but still mis-times the company state overall

## Why this eval matters

This is a listed-company execution problem, not just a generic freshness problem.

In investment-style research, a stale anchor distorts:
- the opening thesis
- the weight assigned to risks vs catalysts
- whether management guidance is still current
- how valuation context is interpreted
- what counts as unresolved vs already updated

A report can therefore look numerically rich while still failing the real current-state contract.

## Suggested intervention target

This case should push changes at multiple layers:

- `SKILL.md` current-state verification for listed-company work
- `ROUTING-MATRIX.md` listed-company hard-fail rules
- `references/finance-date-discipline.md`
- `checklists/listed-company-report.md`

## Reviewer checklist

- Did the report lock the latest annual period before broad analysis?
- Did the report lock the latest quarterly / interim period before broad analysis?
- Did the report include a clearly dated current market snapshot?
- Were older market snapshots visibly downgraded to historical context?
- Could the opening section still be true if a newer reported period already existed?

If yes, the freshness hard gate failed.
