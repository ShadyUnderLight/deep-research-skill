# Evals

## Purpose

This directory exists to improve the skill system, not just to archive interesting outputs.

Evals should help identify:

- what failed
- why it failed
- which layer should change
- whether the result is a new rule, a checklist hardening, a template change, a routing change, a delivery fix, or no action

## Directory structure

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

## What not to put here

Do not use `evals/` for:

- generic brainstorming
- duplicate notes with no new lesson
- report archives with no reusable intervention
- raw thoughts that do not change the repo

## Maintenance note

Keep evals organized by function rather than by recency alone.

If a new eval does not clearly fit an existing subtype, choose the smallest reasonable category instead of creating unnecessary taxonomy.

## Periodic audits

Run `evals/meta/rule-trigger-audit.md` every 10 new eval cases or quarterly to track whether core disciplines are being triggered. When adding a new case eval, note which disciplines were applicable and whether they were triggered — this data feeds the audit.
