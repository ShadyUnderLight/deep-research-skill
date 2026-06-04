# Research Pack Schema (Minimal)

## Required sections

A minimal Research Pack should contain:

- Objective
- Decision context
- Primary route
- Secondary disciplines
- Core subquestions
- Stop condition
- Source register
- Claim register
- Uncertainty register
- Artifact contract
- Required audits
- Final audit status

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
List the audits that should run before delivery.

### Final audit status
Mark pass, partial, or fail with a short reason.

## Minimal example shape

```md
## Objective
...

## Decision context
...

## Primary route
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

## Required audits
...

## Final audit status
...
```
