# Delivery Operator Note

This file describes how the delivery / rendering subsystem works and what common failure patterns to watch for.

It is meant for operators and maintainers who need to understand why a correctly written report may still fail at delivery time, and what to check before marking delivery as clean.

## Pipeline overview

The current delivery pipeline has three stages:

1. **Markdown-to-HTML** — `scripts/markdown_to_html.py` converts the research markdown into styled HTML, with safety sanitization (`nh3`), table repair, CJK spacing normalization, and metadata escaping.
2. **HTML-to-PDF** — `scripts/render_pdf.py` uses Playwright (Chromium) to render the HTML into a PDF with print-oriented CSS. Remote resources are blocked by default.
3. **One-shot pipeline** — `scripts/md_to_pdf.py` chains both stages: markdown → HTML → PDF, forwarding print controls through both stages.

## Pre-delivery checks

Before running the pipeline, verify:

- [ ] no placeholder residues (`TBD`, `TODO`, `XXX`, `[[placeholder]]`, `{citation}`, or similar markers) remain in the markdown
- [ ] no raw markdown syntax leaks that the HTML converter may not handle: check for unclosed code fences, malformed table separators, and unescaped special characters
- [ ] citation artifacts like `[SN]` or `[IN]` labels are intentional reader-facing devices, not debugging residue
- [ ] tables are not extremely wide (20+ columns) — they will degrade badly in PDF; consider restructuring into card/list blocks or splitting into sub-tables
- [ ] the markdown can be read as a standalone document, not as an internal note with rendering dependencies

## Known failure patterns and mitigations

### Table degradation
Very wide or deeply nested tables do not render well in PDF. The pipeline converts multi-column comparison tables into card/list blocks automatically, but extremely dense source tables still need manual simplification before delivery.

Mitigation: keep comparison tables under ~8 columns; move source metadata tables to an appendix with a simpler layout.

### CJK spacing corruption
Spaces between Chinese characters can appear stretched or broken after PDF export, especially around punctuation, brackets, and mixed-script boundaries.

Mitigation: the pipeline runs a pre-parse CJK spacing repair pass (`scripts/markdown_to_html.py`). If artifacts still appear, review the markdown for non-standard spacing around CJK punctuation, especially `%`, `·`, `—`, `…`, and brackets.

### Remote resource blocking
`--allow-remote` is disabled by default. If the report uses remote images, external stylesheets, or web fonts, they will not load unless explicitly allowed.

Mitigation: for local PDF delivery, avoid remote resource dependencies. If remote resources are required (e.g., company logo), use `--allow-remote` and verify the PDF renders correctly.

### Placeholder leakage
Internal generator hints, render-hint text, or template markers can survive into the final HTML if they appear outside of code fences or table structures.

Mitigation: run the final-audit delivery-cleanliness section before the pipeline, not after. Fixing a PDF that already has leaked placeholders requires editing markdown and re-rendering.

## Testing delivery locally

Without running the full pipeline:

1. Render HTML only: `python3 scripts/markdown_to_html.py input.md > output.html`
2. Check the HTML for structural issues: open it in a browser, verify headings, tables, and spacing
3. If PDF quality is critical, render a PDF smoke test: `python3 scripts/md_to_pdf.py input.md test.pdf` and review the output

The pipeline should not be treated as a black box. If the markdown is clean but the PDF is broken, the bug is likely in the rendering layer and should be fixed there rather than by restructuring the research content.

## Relationship to other files

- `checklists/final-audit.md` — the delivery-cleanliness audit section is the delivery-time gate for known failures
- `scripts/markdown_to_html.py` — the conversion entry point; supports `--title` for the document title; cover metadata is inferred from frontmatter-like `title` / `subtitle` / `date` / `type` fields in the markdown input
- `scripts/render_pdf.py` — the PDF renderer; supports `--landscape`, `--media`, `--page-margin`, and `--title` for print control
- `scripts/md_to_pdf.py` — the one-shot pipeline; forwards all print controls
- `references/failure-taxonomy.md` — documents recurring delivery failure families

## When to change the rendering layer

Change `scripts/` when:

- a correctly written report produces a visually broken PDF
- a new markdown pattern (new table shape, new heading structure, new CJK edge case) degrades badly in HTML or PDF
- a security or sanitization gap appears (unsafe HTML, unescaped metadata, remote resource injection)

Do not change `scripts/` when the report content itself is poorly structured, unreadable, or missing required sections. Those are research-discipline problems and should be fixed in the route, reference, or audit layers instead.
