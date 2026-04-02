# deep-research-skill

Decision-oriented deep research skill for OpenClaw-compatible agents.

## Goal

Turn "search and summarize" into a stricter research workflow that:

- clarifies the real objective
- classifies the task type
- verifies current-state facts for fast-moving topics
- compares sources by quality and recency
- actively searches for counter-evidence
- organizes important conclusions as claims
- produces decision-oriented final reports

## Current structure

- `SKILL.md` — main skill protocol
- `references/` — supporting playbooks and templates
- `checklists/` — execution-time audit checklists (run before delivery)
- `examples/` — example tasks and failure cases
- `evals/` — lightweight regression/evaluation prompts, rubrics, and meta-evals
- `references/failure-taxonomy.md` — recurring eval failure families and structural fix map
- `references/comparative-distillation-method.md` — how to turn stronger paired reports into reusable rules and gates
- `references/option-selection-and-shortlist-discipline.md` — general method for constrained choice, ranking, shortlist design, and provider-selection tasks under real constraints
- `checklists/option-selection-final-audit.md` — delivery gate for shortlist, ranking, constrained-choice outputs, and provider-selection current-state checks
- `evals/api-supplier-selection-gpt-vs-minimax-comparative-distillation.md` — worked comparative-distillation case for model/API supplier selection, current-state drift, and China-mainland deployment constraints

## Initial references included

- `current-state-verification.md`
- `counter-evidence.md`
- `decision-report-template.md`
- `claim-matrix.md`
- `task-types.md`
- `finance-date-discipline.md`
- `source-quality.md`
- `report-template.md`
- `market-sizing-and-share-discipline.md`
- `ranking-and-current-claims-discipline.md`
- `research-depth-rubric.md`
- `corporate-status-and-listing-state-discipline.md`
- `source-traceability-and-claim-citation.md`

## Suggested next steps

1. Run real tasks against the skill.
2. Save failures in `examples/` or `evals/`.
3. Tighten references based on observed mistakes.
4. Continue refining `scripts/` only when repeated delivery artifacts or render failures justify it.

## Maintenance and traceability

This repo should be maintained like a real project rather than a loose prompt folder.

- Record meaningful changes in `CHANGELOG.md`.
- Track likely next work in `ROADMAP.md`.
- Use the GitHub issue templates for failures and feature requests.
- Use the PR template for larger changes.
- When fixing a real failure mode, add or update an eval whenever possible.

## Good evaluation targets

- fast-moving products and model versions
- vendor/tool selection
- model/API supplier selection under deployment, compliance, and mainland-access constraints
- company diligence
- technical feasibility
- market hype vs reality
