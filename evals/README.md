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
- `comparative-distillation/` — paired-report comparisons used to extract reusable repo changes
- `meta/` — cross-case execution, activation, and discipline notes
- `templates/` — reusable eval scaffolds and evaluation templates

## Which type to add

Use `cases/` when a single real task exposes a clear failure family.

Use `comparative-distillation/` when comparing two outputs is the main way to extract reusable changes.

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
