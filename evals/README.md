# Evals

## Purpose

This directory exists to improve the skill system, not just to archive interesting outputs.

Evals should help identify:

- what failed
- why it failed
- which layer should change
- whether the result is a new rule, a checklist hardening, a template change, a routing change, a delivery fix, or no action

## Directory structure

- `INDEX.md` — case-level asset index for route, failure-family, discipline, status, and intervention-target scans
- `cases/` — single-case failures, route-specific lessons, or delivery failures tied to one task
- `comparative-distillation/` — paired-report comparisons or single-output distillations used to extract reusable repo changes
- `meta/` — cross-case execution, activation, and discipline notes
- `templates/` — reusable eval scaffolds and evaluation templates

### Naming conventions

Eval subtypes are distinguished by naming rather than by additional subdirectories:

| Directory | Recommended suffix | Example |
|---|---|---|
| `cases/` | `*-case.md` | `freshness-xiaomi-case.md` |
| `comparative-distillation/` | `*-comparative-distillation.md` for paired-output comparisons or comparison-centered distillations; `*-distillation.md` for single-output hardening without a comparison-centered frame | `byd-gpt-vs-minimax-comparative-distillation.md`, `amd-minimax-equity-report-distillation.md` |
| `templates/` | `*-template.md` or `*-rubric.md` | `comparative-distillation-template.md`, `depth-rubric.md` |
| `meta/` | descriptive kebab-case (no fixed suffix) | `current-state-checks.md` |

Rubric-like files may live in `templates/` or inside `evals/meta/`; use `*-rubric.md` when the file is primarily a reusable scoring rubric, while meta discipline checks may keep descriptive names.

## Which type to add

Use `cases/` when a single real task exposes a clear failure family.

Use `comparative-distillation/` for distillation artifacts — either paired-output comparisons or single-output hardening exercises.

Use `meta/` when the issue is not mainly one case but a broader execution, activation, or discipline problem.

Use `templates/` when the file is meant to be reused as an evaluation scaffold rather than stored as a result.

## What an eval should do

A useful eval should not stop at “this was weak”.

It should point toward at least one likely intervention, such as:

- new rule
- checklist hardening
- template change
- routing change
- delivery fix
- no action

## Asset index

Keep `evals/INDEX.md` synchronized with tracked case evals in `evals/cases/`.

The index is the first place to answer:

- which route has active eval coverage
- which failure family a case protects
- which discipline, checklist, validator, or rule is the main intervention target
- whether a case is active, candidate, stale, needs review, or superseded

Status values:

- `active` — normalized case that belongs in the regression/audit asset set
- `candidate` — useful failure material that still needs normalization before it becomes active
- `needs-review` — tracked case whose route, failure family, or current-rule verdict should be rechecked
- `stale` — case expresses an old contract and should be rewritten or retired
- `superseded` — case is covered by a newer, clearer eval

When adding a tracked `evals/cases/*.md` file, add exactly one row to `evals/INDEX.md`. Keep temporary reports, scratch outputs, and unnormalized local material out of the active index until they have a clear eval purpose.

## Executable forward registry

`evals/registry.json` is the canonical machine-readable registry for the small
offline forward-eval subset. It is intentionally separate from the historical
Markdown case index:

- `evals/INDEX.md` catalogs all tracked `evals/cases/*.md` files for human
  coverage scans.
- `evals/registry.json` describes executable user-prompt, activation, process-
  artifact, audit, and delivery-status fixtures.
- `comparative-distillation/candidate-rule-registry.md` tracks candidate rule
  actions and coverage; it is not an execution registry.

Validate and run the forward subset with:

```bash
python3 scripts/validate_eval_registry.py
python3 scripts/run_forward_evals.py --offline --check-baseline
```

The runner routes each case's prompt through a deterministic offline adapter
derived from the route-selection decision tree, then replays local report and
Research Pack snapshots. It does not call a paid model or an external search
provider, and it consumes the structured JSON verdict emitted by
`scripts/audit_report.py` rather than parsing human-readable audit output. The
adapter is a test surface, not a claim that production agent reasoning is a
keyword classifier.

Forward cases retain a concrete `failure_family` and map it to one of four
diagnostic classes: `missing-rule`, `missing-trigger`, `execution-drift`, or
`fixture-reference-drift`. Registry and fixture failures are reported as
`fixture-reference-drift` before any model or audit result is considered.

Metric denominators are explicit: `route_activation_accuracy` is correct
prompt activation over positive cases; `pack_completeness` is complete expected
pack fields over all active cases; `declared_not_executed_rate` is observed
manual/process `not_run`/`partial`/`skipped` cases over all active cases; and
`declared_not_executed_recall` is detection over its negative-case denominator.

## What not to put here

Do not use `evals/` for:

- generic brainstorming
- duplicate notes with no new lesson
- report archives with no reusable intervention
- raw thoughts that do not change the repo

## Maintenance note

Keep evals organized by function rather than by recency alone.

If a new eval does not clearly fit an existing subtype, choose the smallest reasonable category instead of creating unnecessary taxonomy.

When rules evolve, historical evals may keep their original case background, but they must clearly separate historical observations from current acceptance rules. Use short fields when a prior verdict no longer matches the current contract:

- **Historical verdict**: how the case was judged when the eval was created
- **Current rule verdict**: how the same pattern should be judged under the current rule set
- **Current eval target**: what the eval now primarily guards against

## Periodic audits

Run `evals/meta/rule-trigger-audit.md` every 10 new eval cases or quarterly to track whether core disciplines are being triggered. When adding a new case eval, note which disciplines were applicable and whether they were triggered — this data feeds the audit.
