# Research Pack Contract

## Purpose

Research Pack exists to preserve the minimum process structure needed to make route, evidence, uncertainty, and audit burden more recoverable than final prose alone.

It is not the user-facing deliverable.
It is the minimum internal artifact that helps make the final deliverable more auditable.

## What a Research Pack contains

A Research Pack is a compact internal record of:

- what the task actually is
- which route was selected
- which supporting disciplines were attached
- which load-bearing claims drive the answer
- what remains uncertain
- what counter-evidence was considered
- what the final artifact is required to show
- how audit readiness was judged

## Minimal required fields

A minimal Research Pack should include:

- objective
- decision context
- primary route
- closest alternative route and boundary judgment
- action burden (from route selection decision tree Step 1)
- weight-bearing object (from route selection decision tree Step 2)
- decision tree path (which steps resolved; "not needed" if per-route clauses sufficed)
- tie-break rationale (only if Step 4 was reached)
- secondary disciplines
- core subquestions
- stop condition
- source register
- claim register
- uncertainty register
- artifact contract
- required audits
- final audit status

Use the following when relevant:

- current-state snapshot
- degraded-search log
- counter-evidence log
- channel availability snapshot

## Field intent

### Objective
What the work is actually trying to answer.

### Decision context
Why the answer matters and what burden the task carries.

### Primary route
Which route determines structure and audit burden. Include the closest
alternative route and boundary judgment — why this route was chosen over the
alternative, what "Do not use" / "Often confused with" clauses were checked,
and what would trigger a route change.

### Action burden
The action category from Step 1 of the route selection decision tree
in `ROUTING-MATRIX.md` (e.g., "Select / rank / predict", "Judge direction
/ scenario"). Records what the user asked the system to *do*, not just
what topic they asked about. Note "not needed" if per-route clauses alone
resolved the route without invoking the decision tree.

### Weight-bearing object
The object from Step 2 of the decision tree that the conclusion rests on
(e.g., "Defined options / teams / ranking", "Market / category trajectory").
Records what the analysis fundamentally depends on. Note "not needed" if
the decision tree was not invoked.

### Decision tree path
A compact record of which decision tree steps produced the route
selection. Format: "Steps 1-2 resolved to `<route-id>`; Step 3 verified;
Step 4 not reached" or "Per-route clauses resolved without decision tree."
If Step 4 was reached, document the exhaustion of Steps 1-3.

### Tie-break rationale
Only required when Step 4 of the decision tree was reached. Documents why
Steps 1-3 were exhausted (two candidate routes were genuinely equivalent
on action burden, weight-bearing object, and per-route boundary clauses)
and how the fixed tie-breaker priority list resolved the selection.

### Secondary disciplines
Which cross-cutting disciplines are required for this task.

### Core subquestions
The smallest set of subquestions needed to support the final answer.

### Stop condition
What would count as enough research to synthesize responsibly.

### Source register
The key sources and what they support.

### Claim register
The load-bearing claims and how they are supported.

### Uncertainty register
What remains unresolved and why it matters.

### Current-state snapshot
What must be verified as current when the task is time-sensitive.

### Degraded-search log
If fallback discovery was needed, record which provider path was attempted, why fallback was triggered, whether the search objective or query shape was tightened before escalating, what fallback path was used, and what remained unverified.

### Counter-evidence log
What could weaken, delay, qualify, or overturn the answer.

### Channel availability snapshot
If the task depends on an external information channel (local Research API, search provider, content fetch service), record preflight results here. See `references/external-channel-preflight.md` for preflight rules and field definitions. Fields include: `api_available`, `api_version`, `checked_at`, `channels_ok`, `channels_total`, `selected_channels`, `degraded_channels`, `impact_on_research`.

This snapshot is distinct from the degraded-search log — it captures channel availability before research begins, while the degraded-search log records provider fallback during research.

### Artifact contract
What the final report must visibly contain.

### Required audits
Which audits should run before delivery. For each audit, record its run
status — one of: passed, skipped (with reason), not-run (with reason), or
partial (with reason for incomplete execution). The run status documents
whether the audit was actually executed, not just listed.

### Final audit status
Whether the report passed, partially passed, or failed audit readiness.
The status must be consistent with the individual audit run statuses in
Required audits: Pass requires all audits to be passed or skipped (with
reason); Partial is for not-run/partial with reason, or validator warnings
without errors; Fail is required when any audit is not-run without reason,
or when strict validation fails.

## Scope

Research Pack is not:

- a full orchestration engine
- a mandatory artifact for every lightweight task
- a verbose research diary
- a replacement for the final report
- proof that good reasoning happened

It exists to preserve enough structure for auditability without forcing a heavy framework.

## When to use it

Research Pack is most useful when the task is:

- route-heavy
- recommendation-heavy
- uncertainty-sensitive
- comparative
- forward-looking
- audit-burdened

If the task is lightweight and carries little route or audit burden, a fully explicit Research Pack may be unnecessary.

## Minimal internal shape

A compact Research Pack may use this shape:

- Objective
- Decision context
- Primary route
- Closest alternative and boundary judgment
- Action burden
- Weight-bearing object
- Decision tree path
- Tie-break rationale (if applicable)
- Secondary disciplines
- Core subquestions
- Stop condition
- Current-state snapshot
- Degraded-search log
- Channel availability snapshot
- Source register
- Claim register
- Uncertainty register
- Counter-evidence log
- Artifact contract
- Required audits
- Final audit status
