# Research Pack Schema (Minimal)

## Required sections

A minimal Research Pack should contain:

- Objective
- Decision context
- Primary route
- Closest alternative route and boundary judgment
- Action burden (Step 1 of route selection decision tree)
- Weight-bearing object (Step 2 of route selection decision tree)
- Decision tree path (which steps resolved the route; "not needed" if per-route clauses sufficed)
- Tie-break rationale (only if Step 4 was reached)
- Secondary disciplines
- Core subquestions
- Stop condition
- Source register
- Claim register
- Uncertainty register
- Artifact contract
- Required audits
- Final audit status

## Optional sections

Include when the pack is part of a tracked delivery (issue #376):

- `## Artifact id` — stable identifier for this pack, e.g. `research-2026-08-13-001`.
  The final report's contract block should reference the same id via
  `artifact_id`, and the pack's `## Primary route` must match the contract's
  `primary_route` (check with
  `scripts/validate_contract.py report.md --research-pack pack.md`).
- `## Contract reference` — points back to the final report/contract artifact id
  once the report is delivered.

## Conditional sections

Include these when the task requires them:

- Current-state snapshot
- Counter-evidence log
- Channel availability snapshot

### Channel availability snapshot fields

When this section is used, include all 8 fields:

- `api_available` — whether the API responded (true / false / not-checked)
- `api_version` — version string from health response
- `checked_at` — ISO-8601 timestamp of the preflight
- `channels_ok` — count of healthy channels
- `channels_total` — total defined channels
- `selected_channels` — channels selected for the current task
- `degraded_channels` — channels degraded (or `none`)
- `impact_on_research` — how degraded/unavailable channels affect scope or confidence

See `references/external-channel-preflight.md` for preflight rules.

## Field guidance

### Objective
State the real question, not just the topic area.

### Decision context
State why the answer matters and what decision or judgment burden it carries.

### Primary route
State the route that most strongly determines structure and audit burden.
Include the closest alternative route and boundary judgment — why this
route was chosen over the alternative (verify "Do not use" / "Often confused
with" clauses from `references/route-activation-and-preflight.md`).

### Action burden
Record the action category from Step 1 of the route selection decision tree
in `ROUTING-MATRIX.md` (e.g., "Select / rank / predict", "Judge direction /
scenario"). If the decision tree was not needed (per-route clauses sufficed),
note "not needed."

### Weight-bearing object
Record the weight-bearing object from Step 2 of the decision tree (e.g.,
"Defined options / teams / ranking", "Market / category trajectory").
If the decision tree was not needed, note "not needed."

### Decision tree path
Document which steps resolved the route selection. Format: "Steps 1-2
resolved to `<route-id>`; Step 3 verified; Step 4 not reached" or
"Per-route clauses resolved without decision tree." If Step 4 was reached,
document the exhaustion of Steps 1-3 and the tie-breaker result.

### Tie-break rationale
Only required if Step 4 of the decision tree was reached. Explain why
Steps 1-3 were exhausted and which two candidate routes were compared
by the fixed tie-breaker priority list. Document the resolution.

### Secondary disciplines
List only the disciplines that materially matter to the task.

### Core subquestions
Keep these focused on what drives the final answer.

### Stop condition
Make clear what would count as enough evidence to synthesize.

### Source register
List key sources, not every source encountered.

### Claim register
Track load-bearing claims rather than every claim in the report.

### Uncertainty register
Show why each unresolved point matters to the answer.

### Artifact contract
State what the final report must visibly contain.

### Required audits
List the audits that should run before delivery. For each audit, record
its run status — one of: passed, skipped (with reason), not-run (with
reason), or partial (with reason for incomplete execution). A passed audit
must carry a typed evidence reference, for example
`pack-section:Artifact contract` or
`checklist-item:checklists/final-audit.md#FA-001`; free-form text is legacy
self-attestation and cannot pass strict validation. Checklist IDs are stable
markers such as `<!-- audit-item: FA-001 -->` immediately before the item.

The compact Markdown form is:

```md
- final-audit — passed — pack-section:Artifact contract
- route-activation-audit — not-run: no route activation record was created
```

### Final audit status
Mark Pass, Partial, or Fail with a short reason. The status must be
consistent with the individual audit run statuses in Required audits:
Pass requires all audits to have run status "passed" or "skipped" (with
documented reason); Partial is appropriate when some audits are not-run
or partial with reason, or when validator has warnings but no errors;
Fail is required when any audit is not-run without reason or when strict
validation fails.

The same evidence/provenance semantics are used by the report status block
and the JSON verdict. Automated results are labelled
`automated_validator`; manual checklist results are labelled
`manual_checklist_attestation`; process-node results are labelled
`process_node_evidence`; old free-form entries are labelled
`legacy_self_attested` in compatibility mode.

### Research status

Set the research status after collection is complete. One of:

- `complete` — all core subquestions have adequate evidence.
- `partial` — some subquestions have insufficient evidence or relied on
  degraded search.
- `blocked` — external channels or providers were unavailable, preventing
  current-state confirmation.

This field is distinct from Final audit status: it records whether the
research process completed successfully, not whether the delivered content
passes quality checks. A blocked research process can still produce a
content-quality-audit Pass if the available evidence is correctly labeled.

### Delivery status

Set the delivery status after rendering. One of:

- `md_ready` — Markdown artifact satisfies the artifact contract.
- `pdf_ready` — PDF was successfully rendered from the Markdown artifact.
- `pdf_failed` — PDF rendering failed, but Markdown is still available.
- `not_run` — rendering was not attempted (e.g., mid-research artifact).

This field separates delivery concerns from content quality. A `pdf_failed`
result does not imply the Markdown content is invalid — the two statuses
are independent.

## Minimal example shape

```md
## Objective
...

## Decision context
...

## Primary route
...

## Action burden
...

## Weight-bearing object
...

## Decision tree path
...

## Tie-break rationale (if applicable)
...

## Secondary disciplines
...

## Core subquestions
...

## Stop condition
...

## Source register
- Source:
- Supports:

## Claim register
- Claim:
- Support:
- Confidence:

## Uncertainty register
- Uncertainty:
- Why it matters:

## Channel availability snapshot
- api_available:
- api_version:
- checked_at:
- channels_ok:
- channels_total:
- selected_channels:
- degraded_channels:
- impact_on_research:

## Artifact contract
...

## Research status
complete | partial | blocked

## Delivery status
md_ready | pdf_ready | pdf_failed | not_run

## Required audits
- audit name — passed | skipped (reason) | not-run (reason) | partial (reason)
...

## Final audit status
...
```
