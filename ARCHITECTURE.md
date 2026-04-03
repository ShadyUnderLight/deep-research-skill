# Architecture

This file describes the current system shape of the `deep-research` skill.

It exists to make the repo easier to maintain as a layered research system rather than a growing pile of prompts, references, and scripts.

The goal is not to freeze the design too early. The goal is to make current responsibilities explicit so future changes can land in the right layer.

---

## High-level model

`deep-research` now has six practical layers:

1. workflow spine
2. routing layer
3. method / discipline layer
4. audit layer
5. eval / regression layer
6. delivery / rendering layer

These layers are intentionally separate.

- the workflow spine defines how research proceeds
- the routing layer decides which mature task family is active
- the method layer provides reusable discipline files and templates
- the audit layer acts as delivery-time gates
- the eval layer captures real failures, regressions, and distillation artifacts
- the delivery layer turns reports into user-facing artifacts such as PDF

---

## Layer 1: workflow spine

**Primary file:** `SKILL.md`

This is the top-level orchestration file.

Its job is to define the shared workflow that applies across research tasks:

- clarify the real objective
- classify the task
- plan the work
- set evidence standards
- collect and compare sources
- run a mid-research review
- search for counter-evidence
- synthesize a decision-oriented report
- run final discipline before delivery

`SKILL.md` should stay focused on workflow and shared execution discipline.

It should not keep absorbing every mature route-specific rule.

---

## Layer 2: routing layer

**Primary file:** `ROUTING-MATRIX.md`

This layer answers:

- what kind of task is this?
- which route should be primary?
- which secondary disciplines should attach?
- which audits must run?
- what must be visibly present in the final artifact?

The routing layer exists to reduce two failure modes:

1. the right rule exists but does not activate
2. the route is implicitly present in reasoning but not visibly executed in the output

The current first-class routes are:

- provider / vendor selection
- market entry / regional expansion
- market outlook / industry evolution
- first-tier / competitive positioning
- constrained choice / shortlist
- listed-company / investment-style research

As a rule:

- `SKILL.md` should call into the routing layer
- route-specific execution details should prefer `ROUTING-MATRIX.md` over further growth inside `SKILL.md`

---

## Layer 3: method / discipline layer

**Primary directories/files:** `references/`, report templates, reusable guidance files

This layer contains the reusable discipline files that routes attach when needed.

Typical roles in this layer include:

- source quality and evidence structure
- current-state verification
- counter-evidence method
- task-type framing
- market-sizing discipline
- ranking / current-claims discipline
- source-traceability discipline
- comparative-distillation method
- report templates and decision templates
- route-specific supporting references such as market-outlook and shortlist discipline

This layer should answer:

- how should this kind of evidence be handled?
- what structure should this kind of report use?
- what recurring failure discipline applies here?

This layer is reusable across routes.

A route may require multiple discipline files from this layer.

---

## Layer 4: audit layer

**Primary directory:** `checklists/`

This layer acts as the delivery-time gate.

Its job is not to explain the method in full, but to catch execution failures before a report is considered ready.

Current audit files include:

- `checklists/final-audit.md`
- `checklists/source-traceability.md`
- `checklists/forward-looking-claims.md`
- `checklists/listed-company-report.md`
- `checklists/option-selection-final-audit.md`

This layer should answer:

- did the right discipline actually show up in the final report?
- are route-specific gates visible in the artifact?
- are major delivery failures still leaking through?

If a rule exists in `references/` but is not being enforced at delivery time, the right place to harden it is often the audit layer.

---

## Layer 5: eval / regression layer

**Primary directory:** `evals/`

This layer records real failures, comparative-distillation artifacts, and regression checks.

It provides the evidence base for deciding whether the system needs:

- a new rule
- stronger routing
- a harder audit gate
- a template change
- or only a delivery-layer fix

This layer includes multiple practical eval types already, even if the folder is not yet subdivided:

- worked case evals
- comparative-distillation cases
- rubrics
- meta-evals
- rule-activation diagnostics

This layer should answer:

- what failed in reality?
- was it a missing rule, a missing trigger, or execution drift?
- what kind of repo change should follow from that failure?

The eval layer should stay tightly connected to real failures rather than drifting into hypothetical benchmark clutter.

---

## Layer 6: delivery / rendering layer

**Primary directory:** `scripts/`

This layer turns research output into delivery artifacts.

Current responsibilities include:

- markdown normalization before rendering
- markdown to HTML conversion
- layout routing for comparison-heavy structures
- table handling and placeholder cleanup
- PDF rendering
- print styling and CJK readability adjustments

This layer should be treated as a delivery subsystem, not as part of core research reasoning.

It exists because a correct memo can still fail at delivery time if rendering, layout, or parser hygiene is poor.

This layer should answer:

- can the report be delivered cleanly?
- does the final artifact preserve the intended structure?
- are rendering artifacts, placeholders, and citation leakage blocked?

---

## How the layers connect

The intended flow is:

1. `SKILL.md` defines the workflow spine
2. `ROUTING-MATRIX.md` selects the primary route and attached disciplines
3. `references/` provides the method and template files used by that route
4. `checklists/` verifies the route and disciplines were actually executed
5. `evals/` records what failed and why when the system misfires
6. `scripts/` handle delivery artifacts such as PDF

In short:

- workflow decides how the work proceeds
- routing decides which task family is active
- references explain how to do the work correctly
- checklists decide whether the output is ready
- evals explain what to improve next
- scripts decide whether delivery is clean

---

## Current design intent

The current architecture is aiming for these properties:

### 1. route clarity
The task family should be explicit rather than buried in `SKILL.md` prose.

### 2. composable disciplines
A route should be able to attach multiple reusable disciplines without copying their logic into the main skill file.

### 3. visible execution
A route only counts as successfully executed if the final artifact visibly shows its required structure.

### 4. delivery separation
Rendering and PDF issues should be fixable without pretending they are research-method problems.

### 5. real-failure-driven evolution
Evals should continue to drive changes, rather than abstract architecture changes drifting away from lived failure modes.

---

## What is intentionally not done yet

This architecture is still early-stage. It does **not** yet do all of the following:

- formal family grouping across all `references/`, `checklists/`, and `evals`
- a dedicated system-map file for failure families and intervention points
- a fully independent delivery subsystem with separate top-level docs
- subfolder formalization for eval types such as `case`, `rubric`, `distillation`, and `meta-eval`

Those are possible later steps, but they are not required for the current layered design to be useful.

---

## Near-term maintenance rule

When making future changes, prefer this order of questions:

1. is this a workflow-spine change?
2. is this a routing change?
3. is this a reusable discipline/reference change?
4. is this an audit hardening change?
5. is this an eval/regression addition?
6. is this a delivery/rendering change?

Place the change in the narrowest layer that fully explains the problem.

Do not default to expanding `SKILL.md` unless the change truly belongs to the workflow spine.
