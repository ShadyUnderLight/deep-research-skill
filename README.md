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
- `examples/` — example tasks and failure cases
- `evals/` — lightweight regression/evaluation prompts

## Initial references included

- `current-state-verification.md`
- `counter-evidence.md`
- `decision-report-template.md`
- `claim-matrix.md`
- `task-types.md`
- `finance-date-discipline.md`

## Suggested next steps

1. Run real tasks against the skill.
2. Save failures in `examples/` or `evals/`.
3. Tighten references based on observed mistakes.
4. Add scripts only after the protocol is stable.

## Good evaluation targets

- fast-moving products and model versions
- vendor/tool selection
- company diligence
- technical feasibility
- market hype vs reality
