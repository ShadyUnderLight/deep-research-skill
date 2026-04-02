# Commit Plan — market-outlook routing

## Recommended split

Because the repo currently has unrelated local changes in PDF scripts, do **not** blindly commit everything together.

Prefer a focused commit containing only these files:

- `SKILL.md`
- `README.md`
- `CHANGELOG.md`
- `ROADMAP.md`
- `checklists/final-audit.md`
- `evals/decision-utility-rubric.md`
- `evals/ai-coding-agent-market-outlook-gpt-vs-minimax-comparative-distillation.md`
- `references/decision-report-template.md`
- `references/report-template.md`
- `references/market-outlook-and-scenario-discipline.md`
- `PR_NOTES_market_outlook_routing.md`
- `COMMIT_PLAN_market_outlook_routing.md`

## Suggested staging command

```bash
git add \
  SKILL.md \
  README.md \
  CHANGELOG.md \
  ROADMAP.md \
  checklists/final-audit.md \
  evals/decision-utility-rubric.md \
  evals/ai-coding-agent-market-outlook-gpt-vs-minimax-comparative-distillation.md \
  references/decision-report-template.md \
  references/report-template.md \
  references/market-outlook-and-scenario-discipline.md \
  PR_NOTES_market_outlook_routing.md \
  COMMIT_PLAN_market_outlook_routing.md
```

## Suggested commit message

```bash
git commit -m "feat: strengthen market-outlook routing and scenario discipline"
```

## Suggested follow-up

After this focused commit lands, review the PDF-script changes separately:

- `scripts/markdown_to_html.py`
- `scripts/md_to_pdf.py`

Those changes may deserve their own commit because they solve a different failure family (rendering / PDF structure) from the market-outlook routing work.
