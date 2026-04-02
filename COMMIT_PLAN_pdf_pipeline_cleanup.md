# Commit Plan — PDF pipeline cleanup

## Recommended scope

Stage only the rendering-layer files and their traceability docs:

- `scripts/markdown_to_html.py`
- `scripts/md_to_pdf.py`
- `README.md`
- `CHANGELOG.md`
- `ROADMAP.md`
- `PR_NOTES_pdf_pipeline_cleanup.md`
- `COMMIT_PLAN_pdf_pipeline_cleanup.md`

## Suggested staging command

```bash
git add \
  scripts/markdown_to_html.py \
  scripts/md_to_pdf.py \
  README.md \
  CHANGELOG.md \
  ROADMAP.md \
  PR_NOTES_pdf_pipeline_cleanup.md \
  COMMIT_PLAN_pdf_pipeline_cleanup.md
```

## Suggested commit message

```bash
git commit -m "fix: clean up pdf table routing and placeholder leakage"
```

## Notes

- Do **not** bundle the market-outlook routing docs/evals into this commit if they have not already been committed separately.
- `scripts/render_pdf.py` is currently untouched in the diff and does not need to be staged for this package.
- This commit should represent the rendering/HTML-structure failure family only.
