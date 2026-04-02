# PR Notes — clean up PDF pipeline table routing and placeholder leakage

## Summary

This change packages the current PDF-pipeline fixes into a focused rendering-layer update.

The main goal is to stop comparison-heavy sections from degrading into poor PDF structures such as:

- tall vertical card stacks for wide tables
- leaked placeholder fields like `#1` / `—`
- list/callout/heading blocks inheriting the wrong list semantics
- wrapper-path failures in the one-shot markdown-to-PDF script

## Why

Recent real exports exposed a separate failure family from the research-discipline work:

- wide comparison tables were being pushed into awkward vertical card layouts
- all-placeholder columns and rows could leak into final PDFs
- some generated HTML still let headings or callouts sit inside list items
- the wrapper script had fragile sibling-script path resolution

These are rendering / structure failures, not research-routing failures, so they should be tracked and reviewed separately.

## What changed

### `scripts/markdown_to_html.py`
- adds CSS support for split-table groups
- replaces the old dense-table fallback logic with a cleaner pipeline:
  - sanitize table headers/rows
  - drop all-placeholder columns
  - drop placeholder-only rows
  - preserve compact tables when possible
  - split dense wide tables into multiple sub-tables instead of degrading into long card stacks
- adds HTML post-processing to:
  - unwrap headings from stray list items
  - unwrap callout blocks from stray list items
  - remove orphan placeholder paragraphs such as `#1` and `—`

### `scripts/md_to_pdf.py`
- fixes sibling-script path resolution by using `Path(__file__).parent`
- avoids invalid `__file__.parent` attribute access in wrapper command construction

## Scope notes

This PR note covers rendering-layer changes only.

The separate market-outlook / decision-memo routing work should stay in its own commit because it solves a different failure family.

## Suggested commit message

```text
fix: clean up pdf table routing and placeholder leakage
```

## Suggested PR title

```text
fix: clean up pdf table routing and placeholder leakage
```

## Suggested reviewer focus

1. Does dense-table sanitization drop only true placeholder fields?
2. Is split-table fallback preferable to the previous vertical-card fallback across real exports?
3. Do the HTML cleanup regexes risk stripping legitimate content?
4. Is the `Path(__file__).parent` wrapper fix sufficient and low-risk?
