# deep-research-skill

Decision-oriented deep research skill for OpenClaw-compatible agents.

## Goal

Turn “search and summarize” into a stricter research workflow that:

- clarifies the real objective
- classifies the task type
- verifies current-state facts for fast-moving topics
- compares sources by quality and recency
- actively searches for counter-evidence
- produces decision-oriented final reports

## Core files

Start here:

- `SKILL.md` — shared workflow spine and orchestration rules
- `ROUTING-MATRIX.md` — primary routes, attached disciplines, audits, and visible artifact contracts
- `ARCHITECTURE.md` — layered system view of the repo
- `SYSTEM-MAP.md` — family map for references, checklists, evals, and intervention paths

## Supporting directories

- `references/` — reusable methods, discipline files, and report templates
- `checklists/` — delivery-time audit gates
- `evals/` — real-case evals, rubrics, distillation artifacts, and regression checks
- `scripts/` — delivery/rendering helpers, especially for markdown → PDF output
- `examples/` — example tasks and failure cases

## How the repo fits together

The intended flow is:

1. `SKILL.md` defines the workflow spine
2. `ROUTING-MATRIX.md` selects the active route and attached disciplines
3. `references/` provides reusable methods and templates
4. `checklists/` verify that the final artifact is actually ready
5. `evals/` capture real failures and improvement signals
6. `scripts/` handle delivery artifacts such as PDF

If you want the full layered explanation, read `ARCHITECTURE.md`.
If you want the family/problem-area mapping, read `SYSTEM-MAP.md`.

## How to evolve the repo

Use real tasks and real failures.

- when a repeated task family needs clearer activation, strengthen `ROUTING-MATRIX.md`
- when the task shape is right but the method is weak, improve `references/`
- when the method exists but the final output still leaks failures, harden `checklists/`
- when the report is analytically fine but final delivery mixes target languages in load-bearing labels, treat that as a delivery-coherence failure rather than a translation nit
- when the failure is still unclear, add or refine `evals/`
- when the content is right but the export is broken, fix `scripts/`

Prefer focused changes over grab-bag edits.

## Maintenance

- record meaningful behavior changes in `CHANGELOG.md`
- track likely next work in `ROADMAP.md`
- when fixing a real failure mode, add or update an eval whenever possible
- keep rendering/pipeline fixes separate from research-discipline changes when they address different failure families
