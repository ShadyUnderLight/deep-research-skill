# PR Notes — strengthen market-outlook routing and scenario discipline

## Summary

This change upgrades `deep-research` so market-outlook / industry-evolution tasks are no longer treated like generic industry overviews.

The skill now routes prompts such as:

- `未来12个月如何演化`
- market outlook
- industry evolution
- adoption trajectory

into a stricter **decision-memo** workflow.

That means reports are now expected to show:

- a current market snapshot
- key drivers and blockers
- base case + alternative scenarios
- stakeholder implications
- what would change the conclusion
- recommended next steps / monitoring signals

## Why

A paired GPT-vs-MiniMax case on the AI coding agent market showed a recurring failure mode:

- reports could look research-heavy and polished
- but still drift into **industry overview mode**
- with weak scenario structure
- weak stakeholder-action structure
- and insufficient separation between current facts, inferred estimates, and scenario math

This change turns that failure into explicit routing, template, checklist, and eval updates.

## What changed

### Routing / protocol
- `SKILL.md`
  - adds explicit trigger routing for market-outlook / industry-evolution tasks
  - treats them as both current-state-sensitive and decision-memo tasks
  - requires current market snapshot + drivers/blockers + scenarios + stakeholder guidance

### Templates / references
- `references/decision-report-template.md`
  - adds a dedicated market-outlook decision structure
- `references/report-template.md`
  - adds market-outlook memo discipline
- `references/market-outlook-and-scenario-discipline.md`
  - new standalone reference for market-outlook routing, scenario logic, stakeholder implications, and quantitative-role labeling

### Checklists / rubrics
- `checklists/final-audit.md`
  - adds market-outlook gates for:
    - current market snapshot
    - explicit drivers/blockers/scenarios/stakeholder implications
    - labeling outlook numbers as observed / inferred / scenario assumption / illustrative calculation
- `evals/decision-utility-rubric.md`
  - now checks drivers-vs-blockers separation, market scenario usefulness, and stakeholder-specific next actions more explicitly

### Eval artifacts / traceability
- `evals/ai-coding-agent-market-outlook-gpt-vs-minimax-comparative-distillation.md`
  - adds a worked comparative-distillation case for market-outlook routing and scenario discipline
- `README.md`
  - now exposes market-outlook routing as a first-class capability
- `CHANGELOG.md`
  - records the new failure family and resulting repo changes
- `ROADMAP.md`
  - adds follow-up validation work for market-outlook routing

## Scope notes

This PR note describes the market-outlook routing / skill-discipline work only.

There are also unrelated local modifications in the repo's PDF scripts (`scripts/markdown_to_html.py`, `scripts/md_to_pdf.py`) from earlier work. Those should be reviewed separately instead of being silently bundled into this change unless intentionally included.

## Suggested commit message

```text
feat: strengthen market-outlook routing and scenario discipline
```

## Suggested PR title

```text
feat: strengthen market-outlook routing and scenario discipline
```

## Suggested reviewer focus

1. Does the new trigger routing correctly capture real market-outlook tasks without overfiring?
2. Is the new market-outlook template specific enough to prevent overview drift?
3. Are the new checklist gates concrete and auditable?
4. Does the comparative-distillation case justify the rule promotion level?
5. Should market-outlook tasks get a dedicated standalone checklist later, or is the current audit integration enough for now?
