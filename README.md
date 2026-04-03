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

- `SKILL.md` — main workflow spine and orchestration rules
- `ROUTING-MATRIX.md` — task-routing contract: primary routes, attached disciplines, audits, and visible artifact expectations
- `ARCHITECTURE.md` — system-shape note explaining how workflow, routing, references, audits, evals, and scripts fit together
- `SYSTEM-MAP.md` — family map showing how references, checklists, and evals cluster by problem area and where fixes should land first
- `references/` — supporting playbooks and templates
- `checklists/` — execution-time audit checklists (run before delivery)
- `examples/` — example tasks and failure cases
- `evals/` — lightweight regression/evaluation prompts, rubrics, and meta-evals
- `references/failure-taxonomy.md` — recurring eval failure families and structural fix map
- `references/comparative-distillation-method.md` — how to turn stronger paired reports into reusable rules and gates
- `references/option-selection-and-shortlist-discipline.md` — general method for constrained choice, ranking, shortlist design, and provider-selection tasks under real constraints
- `references/market-outlook-and-scenario-discipline.md` — routing and structure discipline for market-outlook / industry-evolution / future-12-month memo tasks
- `checklists/option-selection-final-audit.md` — delivery gate for shortlist, ranking, constrained-choice outputs, provider-selection current-state checks, and market-entry shortlist / sequencing gates
- `evals/api-supplier-selection-gpt-vs-minimax-comparative-distillation.md` — worked comparative-distillation case for model/API supplier selection, current-state drift, and China-mainland deployment constraints
- `evals/ai-coding-agent-market-outlook-gpt-vs-minimax-comparative-distillation.md` — worked comparative-distillation case for market-outlook routing, scenario structure, and stakeholder-action discipline
- `evals/sea-market-entry-gpt-vs-minimax-comparative-distillation.md` — worked comparative-distillation case for market-entry routing, country-shortlist structure, sequencing, hard gates, and delivery-artifact leakage
- `evals/multi-origin-meetup-city-selection-gpt-vs-minimax-comparative-distillation.md` — worked comparative-distillation case for multi-origin meetup-city choice, aggregation visibility, shortlist construction, fairness logic, and ranking-reversal conditions
- `evals/cambricon-first-tier-positioning-case.md` — eval for first-tier / top-tier competitive-positioning discipline, scope-metric-timeframe gating, and prevention of dimension-collapse into prestige labels
- `evals/cambricon-evidence-weighting-and-traceability-case.md` — eval for load-bearing claim traceability, mixed-evidence weighting, and prevention of source-rich but weakly-auditable positioning memos

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
5. Keep rendering/pipeline fixes split from research-discipline changes when they address different failure families.

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
- market-entry / regional-expansion / country-prioritization memos under budget, localization, and compliance constraints
- multi-origin meetup / city-selection / venue-selection memos where fairness, aggregation logic, and shortlist discipline matter
- first-tier / top-tier / multidimensional competitive-positioning judgments
- company diligence
- technical feasibility
- market hype vs reality
