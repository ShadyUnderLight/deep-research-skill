# CJK PDF Rendering Validation Findings

**Date:** 2026-05-28
**Issue reference:** #100
**ROADMAP reference:** P2 — "Validate whether recent CJK text-rhythm tweaks actually reduce the 'broken export / OCR-like spacing' feel in Chinese-heavy PDFs"

---

## What this validation found

The CJK validation exercise was itself a success: it uncovered **two real bugs** in `scripts/markdown_to_html.py` that would have degraded Chinese-heavy PDF output.

| # | Bug | Severity | Fix | Impact if unfixed |
|---|-----|----------|-----|-------------------|
| 1 | CJK spacing regexes used `\s+` which matches `\n`. When a heading ended with CJK and the next line started with CJK, they merged across the paragraph break. | **High** — structural | Changed all CJK regex `\s+` → `[ \t]+` (horizontal whitespace only) | Headings would be merged with following paragraph; PDF output would lose block structure (verified: `<h2>` wrapping entire section) |
| 2 | `unicodedata.normalize('NFKC', ...)` degrades Chinese fullwidth punctuation to ASCII: `（`→`(`, `，`→`,`, `：`→`:`. | **Medium** — typographic | Changed `NFKC` → `NFC` (canonical composition only, preserves fullwidth punct) | PDFs would show ASCII parentheses and commas in Chinese text (e.g. `2025 年营收 218.6 亿元(同比 +62.3%),归母净利润`) |

Both fixes were validated against the test reports and existing unit tests.

---

## Methodology

Two Chinese-heavy markdown files (each 5,000+ CJK characters) were created covering distinct report types:

| Test file | CJK chars | Total chars | Report type |
|-----------|-----------|-------------|-------------|
| `cjk-pdf-validation-input-company-case.md` | 5,141 | 12,755 | Listed-company deep research (中际旭创) |
| `cjk-pdf-validation-input-market-case.md` | 5,168 | 11,304 | Market outlook / industry analysis (AI 大模型) |

Both files were processed through the standard delivery pipeline:
1. `scripts/markdown_to_html.py` — Markdown → HTML (with CJK normalization)
2. `scripts/render_pdf.py` — HTML → PDF via Playwright Chromium

### Verification script

A dedicated verification script (`scripts/test_cjk_pdf_pipeline.py`) was added that checks:

- **Block structure integrity**: heading counts, list item counts match between source markdown and generated HTML
- **No cross-paragraph merging**: heading content length < 100 chars (no merged body text)
- **Chinese punctuation fidelity**: no ASCII `(`,`,`, `;`, `:` appearing after CJK characters in non-code, non-URL contexts
- **Same-line CJK spacing**: no `CJK+space+CJK` within single text lines in headings, paragraphs, list items, or table cells

The script passes on both test reports.

---

## Content coverage

- ✅ Multi-level headings (h1–h4) with mixed CJK/Latin
- ✅ Long paragraphs of continuous Chinese text
- ✅ Tables with CJK content (12 source tables in company → 16 HTML tables after auto-split; 9 in market → 14 HTML)
- ✅ Mixed CJK + Latin/numbers (company names, metrics, codes)
- ✅ CJK punctuation (brackets、quotes、dashes — ellipsis… percent% 、、 ；）
- ✅ Ordered and unordered lists
- ✅ Fenced code blocks with Chinese comments
- ✅ Markdown links with Chinese anchor text
- ✅ Bold/strong inline Chinese text
- ✅ Callout blocks
- ✅ Cover page with Chinese metadata
- ✅ Wide CJK table cells with mixed content

---

## Results (after fixes)

### Block structure integrity

| Check | Company report | Market report |
|-------|---------------|---------------|
| H1 count matches source | ✅ | ✅ |
| H2 count matches source | ✅ | ✅ |
| H3 count matches source | ✅ | ✅ |
| List items preserved | ✅ | ✅ |
| No heading-text merging | ✅ 0 issues | ✅ 0 issues |

### Chinese punctuation fidelity

| Check | Company report | Market report |
|-------|---------------|---------------|
| No ASCII `(` or `,` after CJK (non-code, non-URL) | ✅ 0 issues | ✅ 0 issues |
| Fullwidth `（）` preserved | ✅ | ✅ |
| Fullwidth `，` preserved | ✅ | ✅ |
| Fullwidth `：；` preserved | ✅ | ✅ |

### CJK spacing integrity

| Check | Company report | Market report |
|-------|---------------|---------------|
| Headings — same-line CJK spacing | ✅ 0 issues | ✅ 0 issues |
| Table cells — same-line CJK spacing | ✅ 0 issues | ✅ 0 issues |
| Paragraphs — same-line CJK spacing | ✅ 0 issues | ✅ 0 issues |
| List items — CJK spacing | ✅ 0 issues | ✅ 0 issues |
| Fenced code blocks | ✅ 1 code block, clean | ✅ 1 code block, clean |

### PDF generation

| Metric | Company report | Market report |
|--------|---------------|---------------|
| HTML size | ~920 lines | ~900 lines |
| PDF size | 1,741 KB | 1,729 KB |
| Pipeline status | ✅ Generated successfully | ✅ Generated successfully |
| Pipeline warnings | 0 | 0 |

---

## Baseline comparison

Previous eval cases documented specific CJK rendering failures:

| Case | Previously observed symptom | Current status |
|------|---------------------------|----------------|
| `minimax-sea-memo-pdf-layout-case.md` | "Chinese characters appeared visually torn apart or over-spaced" — headings like `决 策 备 忘录` looked broken | ✅ Not reproduced. All headings, paragraphs, and tables show intact CJK spacing |
| `japan-vs-china-vs-sea-market-entry-comparative-distillation.md` (R43) | "CJK broken-export PDF texture" — mixed-language labels showed spacing degradation | ✅ Not reproduced. Mixed CJK/Latin text renders correctly with fullwidth punctuation |
| `home-server-equipment-recommendation-minimax-comparative-distillation.md` | "PDF showed visibly broken Chinese text spacing and degraded readability" | ✅ Not reproduced. Both test PDFs show natural CJK text rhythm |

---

## Bugs discovered and fixed

### Bug 1: `\s+` in CJK regex merges across paragraphs

**File:** `scripts/markdown_to_html.py`, lines 681–686
**Root cause:** All CJK spacing regexes used `\s+` (which includes `\n`, `\r`). When a line ending in CJK (e.g. `摘要`) was followed by a blank line and then another CJK-starting line (e.g. `中际旭创`), the `\s+` matched the `\n\n` and merged them.
**Fix:** Changed `\s+` → `[ \t]+` and `\s*` → `[ \t]*` in all CJK spacing patterns, making them line-local.
**Verified:** A heading + paragraph test case (`## 1. 执行摘要\n\n中际旭创...`) now preserves the paragraph break.

### Bug 2: NFKC degrades Chinese punctuation

**File:** `scripts/markdown_to_html.py`, line 669
**Root cause:** `unicodedata.normalize('NFKC', text)` applies compatibility decomposition, which converts fullwidth CJK punctuation to ASCII (e.g. `（` U+FF08 → `(` U+0028, `，` U+FF0C → `,` U+002C).
**Fix:** Changed `NFKC` → `NFC` (canonical composition only). NFC preserves all CJK characters and punctuation unchanged.
**Verified:** Chinese punctuation in test reports (`（2025 年），公司` → `（2025 年），公司`) remains intact.

### Verification gap

The initial validation only checked `CJK+space+CJK` patterns within single text lines. This missed:
- Cross-paragraph merging (the `\n` between paragraphs wasn't flagged)
- Punctuation degradation (NFKC doesn't introduce CJK+space+CJK, it changes fullwidth to ASCII)

The verification script (`scripts/test_cjk_pdf_pipeline.py`) now explicitly checks all three dimensions.

---

## Verification script

`scripts/test_cjk_pdf_pipeline.py` provides 6 test cases:

| Test | What it checks |
|------|---------------|
| `normalize preserves structure` | Block-level elements survive normalization |
| `no heading merge` | CJK heading + CJK paragraph remain separated by `\n\n` |
| `Chinese punctuation preserved` | `（） ，：；。` survive NFC |
| `full pipeline block integrity` | Complete markdown→HTML pipeline preserves heading/list counts |
| `file pipeline (company)` | Real company report: structural integrity, no punct degradation, no spacing issues |
| `file pipeline (market)` | Real market report: same checks |

Run with: `python3 scripts/test_cjk_pdf_pipeline.py`

---

## Remaining risks

1. **Content type coverage:** Validated on 2 report types (listed-company research, market outlook). Not tested on code-heavy technical docs or academic citation-heavy reports.
2. **Character scope:** Validates Chinese (CJK Unified Ideographs) only. Japanese and Korean characters were not tested.
3. **Rendering engine:** Playwright Chromium only. No other PDF engines (wkhtmltopdf, weasyprint) were tested.
4. **No pixel-level regression testing:** The validation relies on text extraction from HTML and programmatic checks, not automated visual comparison.
5. **No CI gate:** The verification script exists but is not wired into CI. Adding it requires a Playwright-enabled runner.
6. **CJK regex only covers same-line spacing:** The `[ \t]+` regexes fix same-line CJK spacing but cannot handle alternating `CJK-space-CJK-space-CJK` patterns where every CJK is separated by a space (non-overlapping match limitation). This is a pre-existing limitation and not a regression.

---

## Verdict

**After fixes, the CJK spacing repair and normalization logic works correctly for Chinese-heavy PDFs.** Two real bugs were discovered and fixed during the validation process. A dedicated verification script now guards against regression in the three key dimensions: block structure integrity, Chinese punctuation fidelity, and same-line CJK spacing.

The fixes do not change behavior for English-only reports (no CJK characters, no fullwidth punctuation to degrade).

---

## Artifacts produced

| File | Description |
|------|-------------|
| `evals/cases/cjk-pdf-validation-input-company-case.md` | Test markdown — listed-company research (5,141 CJK chars) |
| `evals/cases/cjk-pdf-validation-input-market-case.md` | Test markdown — market outlook (5,168 CJK chars) |
| `evals/cases/cjk-pdf-validation-output-company.pdf` | Generated PDF output (not committed) |
| `evals/cases/cjk-pdf-validation-output-market.pdf` | Generated PDF output (not committed) |
| `evals/cases/cjk-pdf-validation-findings-case.md` | This findings document |
| `scripts/test_cjk_pdf_pipeline.py` | Verification script (6 tests, all passing) |

---

## ROADMAP

This validation uncovered pipeline bugs that were fixed as part of the process. The ROADMAP P2 item is updated to reflect the current state. Remaining work: testing against more report types and adding a CI gate for rendering regression.
