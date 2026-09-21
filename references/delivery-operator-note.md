# Delivery Operator Note

This file describes how the delivery / rendering subsystem works and what common failure patterns to watch for.

It is meant for operators and maintainers who need to understand why a correctly written report may still fail at delivery time, and what to check before marking delivery as clean.

## Pipeline overview

The current delivery pipeline has three stages:

1. **Markdown-to-HTML** — `scripts/markdown_to_html.py` is the compatibility CLI facade over independently testable `scripts/delivery/` modules for normalization, table repair/layout, metadata, sanitization, and HTML rendering.
2. **HTML-to-PDF** — `scripts/render_pdf.py` uses Playwright (Chromium) to render the HTML into a PDF with print-oriented CSS. Remote resources are blocked by default.
3. **One-shot pipeline** — `scripts/md_to_pdf.py` calls the structured delivery pipeline: Markdown → temporary HTML → PDF. Intermediate HTML is removed by default; use `--keep-html` to retain it next to the PDF.

The pipeline returns a machine-readable result with `markdown_status`,
`delivery_status`, artifact paths, size, and errors. The canonical
delivery values are `md_ready`, `pdf_ready`, `pdf_failed`, and `not_run`.
Use `--json` to emit this result. Use `--write-status PATH` only when an
explicit Research Pack/report writeback is intended; the input Markdown is
never mutated implicitly.

Path conflicts fail closed before any write: the output must be a `.pdf`
path (case-insensitive), must not resolve to the input Markdown (including
hardlink aliases), and `--keep-html` must not collide with the PDF path.
On Windows and macOS, planned output/status aliases that differ only by case
are also rejected before delivery starts.
Intermediate HTML and the PDF are staged next to the output and validated
(non-empty, `%PDF` header) before atomic replacement, so a rejected or
failed render leaves the input and any existing PDF untouched; replaced
files keep their previous permission mode. Fenced code (backtick or tilde,
closed or not) is never rewritten by normalization or table repair: its
Unicode form, control characters, and line endings pass through those
stages unchanged (the downstream Markdown/HTML serializer renders LF).
Data-bearing table columns are never dropped, including columns holding
`N/A`/`TBD`/`#1` style status values; only strictly empty layout columns
and columns removed by the optional metadata fold are dropped, with
warnings. Nested tables, non-default rowspans, oversized colspans, and table-level
content outside the lossless model (`<caption>`, `<colgroup>`/`<col>`,
`<tfoot>`, stray text between cells) are kept as original markup instead
of being rebuilt, as are tables or cells with attributes beyond spans —
except Python-Markdown's renderer-owned alignment `style="text-align: ..."`,
which stays rebuild-safe so aligned wide tables still get split and cleaned
up. Malformed or duplicate span attributes also fail closed.

## Pre-delivery checks

Before running the pipeline, verify:

- [ ] no placeholder residues (`TBD`, `TODO`, `XXX`, `[[placeholder]]`, `{citation}`, or similar markers) remain in the markdown
- [ ] no raw markdown syntax leaks that the HTML converter may not handle: check for unclosed code fences, malformed table separators, and unescaped special characters
- [ ] citation artifacts like `[SN]` or `[IN]` labels are intentional reader-facing devices, not debugging residue
- [ ] tables are not extremely wide (20+ columns) — they will degrade badly in PDF; consider restructuring into card/list blocks or splitting into sub-tables
- [ ] the markdown can be read as a standalone document, not as an internal note with rendering dependencies

## Known failure patterns and mitigations

### Markdown table repair

Malformed or LLM-produced Markdown tables are repaired to
`max(header width, widest data row)`; a wider data row is never sliced, and
escaped pipes (`\|`) or pipes inside inline code spans stay in one cell —
including when deciding whether a line is a table row at all. A separator-
backed unbordered two-column block may use one structural pipe per row;
an unbordered one-token short row can bridge directly to a following
structural row, while prose-shaped boundaries — including an unbordered
sentence-shaped width expansion with pipes — terminate the block. A
consistent label/number-shaped row such as `North | Sales | Forecast` remains
data even when it is wider than the separator. Lowercase or CJK wide rows in
this ambiguous position fail closed as prose; use outer pipes when they are
intended as data.
Multi-pipe prose without a separator and standalone single-pipe prose are
never promoted to a table. Code spans follow CommonMark rules: backslash is ordinary
inside a span and an unmatched backtick is literal. Fullwidth `｜` is data
inside normal rows and code spans; it is only converted to a delimiter for
legacy rows that have no ASCII structural pipes. Existing alignment
separators (`:---`/`---:`/`:---:`) are preserved. A leading layout-only
column is dropped only when the header and every real data cell are
strictly layout values (also when the separator is missing), and the drop
is reported as a warning; warnings reach `--json` and are printed to
stderr in human mode.

### Table degradation
Very wide or deeply nested tables do not render well in PDF. The pipeline converts multi-column comparison tables into card/list blocks automatically, but extremely dense source tables still need manual simplification before delivery.

Mitigation: keep comparison tables under ~8 columns; move source metadata tables to an appendix with a simpler layout.

### CJK spacing corruption
Spaces between Chinese characters can appear stretched or broken after PDF export, especially around punctuation, brackets, and mixed-script boundaries.

Mitigation: the pipeline runs a pre-parse CJK spacing repair pass (`scripts/markdown_to_html.py`). If artifacts still appear, review the markdown for non-standard spacing around CJK punctuation, especially `%`, `·`, `—`, `…`, and brackets.

### Remote resource blocking
`--allow-remote` is disabled by default. If the report uses remote images, external stylesheets, or web fonts, they will not load unless explicitly allowed.

Mitigation: for local PDF delivery, avoid remote resource dependencies. If remote resources are required (e.g., company logo), use `--allow-remote` and verify the PDF renders correctly.

### Path conflicts and overwrites

A delivery invoked with the input Markdown as its output, a hardlink alias,
or any non-`.pdf` output path (`.md`, `.html`, `.txt`, `.json`, or no
extension) is rejected with an explicit error and `not_run`; `--keep-html`
additionally rejects an HTML path that collides with the PDF, and
`--write-status` rejects a status path that resolves to the input Markdown,
the PDF, or the retained HTML. Nothing is written before these checks, and
staged artifacts are replaced atomically, so a rejected or crashed render
cannot truncate the source or a previously delivered PDF. Output-directory
preparation failures, missing inputs, and missing Markdown-stage
dependencies all return a structured `not_run` result instead of a
traceback or plain text, so `--json` consumers always receive parseable
JSON; `pdf_size_bytes` is recorded only after the PDF commit succeeds, and
status writeback is atomic and mode-preserving. With
`--keep-html`, the HTML is committed before PDF rendering (so a failed
render still leaves a readable HTML) while the previous PDF stays
untouched; `kept_html` is true only after that commit succeeds. Diagnostics
name the conflicting path; fix the command instead of deleting files.

### Placeholder leakage
Internal generator hints, render-hint text, or template markers can survive into the final HTML if they appear outside of code fences or table structures.

Mitigation: run the final-audit delivery-cleanliness section before the pipeline, not after. Fixing a PDF that already has leaked placeholders requires editing markdown and re-rendering.

## Testing delivery locally

Without running the full pipeline:

1. Render HTML only: `python3 scripts/markdown_to_html.py input.md output.html`
2. Check the HTML for structural issues: open it in a browser, verify headings, tables, and spacing
3. If PDF quality is critical, render a PDF smoke test: `python3 scripts/md_to_pdf.py input.md test.pdf --json`
4. Run the deterministic structure/visual smoke set: `python3 scripts/check_pdf_regression.py --artifact-dir /tmp/deep-research-pdf-regression`

The pipeline should not be treated as a black box. If the markdown is clean but the PDF is broken, the bug is likely in the rendering layer and should be fixed there rather than by restructuring the research content.

## Relationship to other files

- `checklists/final-audit.md` — the delivery-cleanliness audit section is the delivery-time gate for known failures
- `scripts/markdown_to_html.py` — the conversion entry point; supports `--title` for the document title; cover metadata is inferred from frontmatter-like `title` / `subtitle` / `date` / `type` fields in the markdown input
- `scripts/render_pdf.py` — the PDF renderer; supports `--landscape`, `--media`, `--margin-top`, `--margin-right`, `--margin-bottom`, `--margin-left`, and `--title` for print control
- `scripts/md_to_pdf.py` — the one-shot pipeline; forwards all print controls
- `scripts/delivery/` — modular delivery stages and the `DeliveryResult`/status contract
- `scripts/check_pdf_regression.py` — offline fixture-based PDF structure and Playwright visual smoke checks; artifacts are explainable HTML/PDF/screenshots, not pixel-equality baselines
- `references/failure-taxonomy.md` — documents recurring delivery failure families
- `references/markdown-delivery-contract.md` — defines the reader-facing
  Markdown shape and its lightweight presentation lint

## When to change the rendering layer

Change `scripts/` when:

- a correctly written report produces a visually broken PDF
- a new markdown pattern (new table shape, new heading structure, new CJK edge case) degrades badly in HTML or PDF
- a security or sanitization gap appears (unsafe HTML, unescaped metadata, remote resource injection)

Do not change `scripts/` when the report content itself is poorly structured, unreadable, or missing required sections. Those are research-discipline problems and should be fixed in the route, reference, or audit layers instead.

---

## PDF Delivery Trigger (from SKILL.md §Delivery rule)

Default delivery stays as text or markdown.

Produce a PDF artifact when the user's request shows explicit file-delivery intent:

- contains `pdf` or `PDF` in a generative/delivery context (e.g. "生成 PDF", "导出 PDF", "PDF 报告", "保存为 PDF", "给我 PDF 文件", "PDF 版本", "PDF 格式")
- includes file-oriented phrases like "报告文件", "可下载报告", "正式报告文件", "给我报告文件", "交付一个文件", "作为附件给我", "以附件形式交付", "输出为附件", "交付成附件"
- the overall request clearly asks for a deliverable file rather than just report content

Do not trigger PDF generation when:

- the user mentions `pdf` / `PDF` only to negate or discuss it: "不要 PDF", "不用 PDF", "无需 PDF", "no PDF", "not PDF", "为什么 PDF 渲染失败", "比较 PDF 和 Markdown", or similar meta-discussion
- the request only uses generic report terminology ("报告", "研究报告", "分析报告", "写成报告格式") that indicates output shape (text/markdown) rather than file format

### Pipeline steps

1. write the final report to a `.md` file first
2. convert it with `scripts/md_to_pdf.py`
3. deliver the PDF when the surface supports files

The markdown file remains the source of truth.

If PDF rendering fails, still deliver the markdown or text report and explicitly say the PDF export failed.

→ **Back to:** `SKILL.md` §Delivery rule (for the delivery trigger activation in the workflow context)
