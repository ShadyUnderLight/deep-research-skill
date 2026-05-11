#!/usr/bin/env python3
"""
Universal Markdown → Styled HTML converter for Deep Research reports.

Security model: this script is designed for processing agent-authored
Deep Research reports. It escapes frontmatter-derived metadata fields
(title, cover_title, cover_subtitle, cover_meta) to prevent HTML injection.
Body HTML is produced by Python-Markdown with the 'extra' extension,
which preserves raw HTML in the markdown source. Do not pass untrusted
content to this script without sanitizing first.

Usage:
    python3 markdown_to_html.py <input.md> [output.html] [--title "Report Title"]
"""
import html
import sys
import re
import os
import argparse
import unicodedata
from pathlib import Path

# ─── HTML Template ────────────────────────────────────────────────────────────

BASE_CSS = """
@page {
  size: A4;
  margin: 1.9cm 2.1cm 2cm 2.1cm;
  @bottom-center {
    content: counter(page) " / " counter(pages);
    font-size: 8pt;
    color: #94a3b8;
  }
}

* { box-sizing: border-box; }

:root {
  --color-text: #1f2937;
  --color-title: #0f172a;
  --color-subtitle: #475569;
  --color-primary: #2563eb;
  --color-primary-soft: #eff6ff;
  --color-primary-border: #bfdbfe;
  --color-muted: #64748b;
  --color-line: #dbe4f0;
  --color-table-alt: #f8fbff;
  --color-cover-bg-top: #f8fbff;
  --color-cover-bg-bottom: #eef4ff;
}

html {
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}

body {
  font-family: "PingFang SC", "Hiragino Sans GB", "STHeiti", "Heiti SC", "Microsoft YaHei", "Noto Sans CJK SC", Arial, sans-serif;
  font-size: 10.2pt;
  line-height: 1.82;
  color: var(--color-text);
  margin: 0;
  padding: 0;
  font-feature-settings: "kern" 1, "liga" 1;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  -webkit-text-size-adjust: 100%;
  hyphens: none;
  letter-spacing: 0;
  word-spacing: 0;
  word-break: normal;
  overflow-wrap: normal;
  line-break: strict;
  text-spacing: none;
  text-autospace: no-autospace;
  text-rendering: optimizeLegibility;
}

p, li, blockquote, td, th, h1, h2, h3, h4, .table-card-value, .exec-box, .callout {
  word-break: keep-all;
  overflow-wrap: normal;
}

/* ── Cover ── */
.cover {
  page-break-after: always;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  background: linear-gradient(180deg, var(--color-table-alt) 0%, var(--color-cover-bg-bottom) 100%);
  color: var(--color-title);
  text-align: left;
  padding: 56pt 52pt;
  border-top: 10pt solid #1d4ed8;
}
.cover-tag {
  font-size: 8.5pt;
  letter-spacing: 1.1pt;
  text-transform: uppercase;
  color: var(--color-primary);
  margin-bottom: 18pt;
  font-weight: 700;
}
.cover h1 {
  font-size: 26pt;
  font-weight: 800;
  line-height: 1.22;
  margin: 0 0 10pt 0;
  color: var(--color-title);
  background: none;
  padding: 0;
}
.cover h2 {
  font-size: 13pt;
  font-weight: 500;
  color: var(--color-subtitle);
  margin: 0 0 24pt;
  border: none;
  padding: 0;
}
.cover-line {
  width: 64pt;
  height: 3pt;
  background: var(--color-primary);
  border-radius: 999px;
  margin: 0 0 24pt;
}
.cover-meta {
  font-size: 9.4pt;
  color: var(--color-muted);
  line-height: 1.95;
}
.cover-badge {
  display: inline-block;
  margin-top: 24pt;
  background: #dbeafe;
  border: 1px solid #93c5fd;
  border-radius: 999px;
  padding: 5pt 14pt;
  font-size: 8pt;
  color: #1d4ed8;
  letter-spacing: 0.7pt;
  font-weight: 700;
}

/* ── Headings ── */
h1, h2, h3, h4 {
  page-break-after: avoid;
  page-break-inside: avoid;
}

h1 {
  font-size: 16pt;
  font-weight: 800;
  color: var(--color-title);
  background: var(--color-primary-soft);
  border: 1px solid var(--color-primary-border);
  border-left: 6pt solid var(--color-primary);
  border-radius: 6pt;
  padding: 10pt 13pt;
  margin: 24pt 0 12pt;
}

h2 {
  font-size: 12.2pt;
  font-weight: 700;
  color: #1e3a8a;
  border-left: 4pt solid #3b82f6;
  padding-left: 9pt;
  margin: 18pt 0 8pt;
}

h3 {
  font-size: 10.8pt;
  font-weight: 700;
  color: #111827;
  margin: 12pt 0 5pt;
}

h4 {
  font-size: 10pt;
  font-weight: 700;
  color: #334155;
  margin: 10pt 0 4pt;
}

/* ── Paragraphs / text rhythm ── */
p {
  margin: 0 0 9pt;
  orphans: 3;
  widows: 3;
}

p + p {
  margin-top: 1pt;
}

strong { color: var(--color-title); }
a { color: var(--color-primary); text-decoration: none; }

/* ── Lists ── */
ul, ol {
  margin: 7pt 0 13pt 1.35em;
  padding: 0;
}

li {
  margin: 0 0 5pt;
  padding-left: 1pt;
}

li > p {
  margin: 0;
}

/* ── Tables ── */
.table-wrap {
  margin: 10pt 0 16pt;
}

.table-note {
  font-size: 7.8pt;
  color: var(--color-muted);
  margin: 0 0 5pt;
  line-height: 1.5;
}

.table-card-list {
  display: block;
  margin: 8pt 0 16pt;
}

.table-card {
  border: 1px solid var(--color-line);
  border-radius: 8pt;
  background: #fff;
  margin: 0 0 10pt;
  overflow: hidden;
  page-break-inside: avoid;
}

.table-card-index {
  background: #eef4ff;
  color: #1e3a8a;
  font-size: 8pt;
  font-weight: 700;
  padding: 5pt 9pt;
  border-bottom: 1px solid #d9e5f7;
}

.table-card-row {
  display: block;
  padding: 7pt 9pt;
  border-bottom: 1px solid #edf2f7;
}

.table-card-row:last-child {
  border-bottom: none;
}

.table-card-label {
  display: block;
  font-size: 7.8pt;
  color: var(--color-muted);
  margin-bottom: 2pt;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.2pt;
}

.table-card-value {
  display: block;
  color: var(--color-text);
  line-height: 1.58;
}

.wide-table table {
  font-size: 8.6pt;
}

.wide-table thead th,
.wide-table tbody td {
  padding: 6pt 7pt;
}

.split-table-group {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 9pt 10pt;
  align-items: start;
  page-break-inside: auto;
}

.split-table {
  margin: 0 0 12pt;
  break-inside: avoid;
  page-break-inside: avoid;
}

.split-table:last-child {
  margin-bottom: 0;
}

table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  margin: 10pt 0 16pt;
  font-size: 9.1pt;
  line-height: 1.58;
  table-layout: fixed;
  border: 1px solid var(--color-line);
  border-radius: 8pt;
  overflow: hidden;
  page-break-inside: auto;
}

thead tr {
  background: #e8f0ff;
  color: var(--color-title);
}

thead {
  display: table-header-group;
}

thead th {
  padding: 8pt 9pt;
  text-align: left;
  font-weight: 700;
  font-size: 8.6pt;
  border-bottom: 1px solid #cdd9ee;
  vertical-align: top;
}

tbody tr:nth-child(even) {
  background: var(--color-table-alt);
}

tbody tr {
  break-inside: avoid;
  page-break-inside: avoid;
}

tbody td {
  padding: 7pt 9pt;
  vertical-align: top;
  border-bottom: 1px solid #e5edf7;
  border-right: 1px solid #edf2f7;
  word-wrap: break-word;
  overflow-wrap: break-word;
}

tbody tr:last-child td {
  border-bottom: none;
}

tbody td:last-child,
thead th:last-child {
  border-right: none;
}

td:first-child {
  font-weight: 600;
  color: #1e3a8a;
}

/* ── Callouts ── */
.callout {
  border-radius: 8pt;
  padding: 10pt 13pt;
  margin: 10pt 0 12pt;
  font-size: 9.5pt;
  line-height: 1.66;
  page-break-inside: avoid;
  border: 1px solid transparent;
}
.callout-confirmed  { background: #f0fdf4; border-color: #bbf7d0; border-left: 4pt solid #16a34a; color: #14532d; }
.callout-inference  { background: #fffbeb; border-color: #fde68a; border-left: 4pt solid #d97706; color: #78350f; }
.callout-uncertainty{ background: #fef2f2; border-color: #fecaca; border-left: 4pt solid #dc2626; color: #7f1d1d; }
.callout-bull       { background: #f0fdf4; border-color: #bbf7d0; border-left: 4pt solid #16a34a; color: #14532d; }
.callout-bear       { background: #fef2f2; border-color: #fecaca; border-left: 4pt solid #dc2626; color: #7f1d1d; }

/* ── Badges ── */
.badge {
  display: inline-block;
  font-size: 7pt;
  font-weight: 800;
  letter-spacing: 0.45pt;
  text-transform: uppercase;
  padding: 2pt 6pt;
  border-radius: 999px;
  vertical-align: middle;
  margin-right: 5pt;
}
.badge-confirmed   { background: #dcfce7; color: #166534; }
.badge-inference   { background: #fef3c7; color: #92400e; }
.badge-uncertainty { background: #fee2e2; color: #991b1b; }
.badge-bull        { background: #dcfce7; color: #166534; }
.badge-bear        { background: #fee2e2; color: #991b1b; }

/* ── Sources ── */
.source {
  font-size: 7.8pt;
  color: var(--color-muted);
  margin: 4pt 0 0;
  line-height: 1.55;
}
.source a {
  color: var(--color-primary);
  word-break: normal;
  overflow-wrap: anywhere;
}

.url-soft {
  word-break: normal;
  overflow-wrap: anywhere;
}

.table-wrap-source {
  page-break-inside: auto;
}

.table-wrap-source table {
  page-break-inside: auto;
}

.table-wrap-source td:first-child {
  color: var(--color-text);
  font-weight: 500;
}

/* ── Exec Summary Box ── */
.exec-box {
  background: linear-gradient(180deg, var(--color-title) 0%, #172554 100%);
  color: #e2e8f8;
  border-radius: 10pt;
  padding: 16pt 18pt;
  margin: 12pt 0 18pt;
  font-size: 10pt;
  line-height: 1.8;
}
.exec-box strong { color: #93c5fd; }

/* ── HR / Page Break ── */
.pb { page-break-before: always; }
hr { border: none; border-top: 1pt solid var(--color-line); margin: 16pt 0; }

/* ── Code / Quote ── */
code {
  font-size: 8.4pt;
  background: #f1f5f9;
  padding: 1pt 4pt;
  border-radius: 4pt;
  font-family: "SFMono-Regular", "Menlo", "Courier New", monospace;
}

pre {
  background: var(--color-title);
  color: #e2e8f0;
  padding: 11pt 12pt;
  border-radius: 8pt;
  overflow-x: auto;
  font-size: 8.3pt;
  line-height: 1.55;
  margin: 10pt 0 12pt;
  white-space: pre-wrap;
  word-break: break-word;
}

pre code {
  background: transparent;
  color: inherit;
  padding: 0;
}

blockquote {
  border-left: 3pt solid #93c5fd;
  background: #f8fafc;
  padding: 9pt 11pt;
  margin: 11pt 0 13pt;
  color: var(--color-subtitle);
  font-style: normal;
  border-radius: 0 6pt 6pt 0;
}

.decision-strip {
  display: block;
  margin: 10pt 0 14pt;
  padding: 10pt 12pt;
  border-radius: 8pt;
  border: 1px solid #dbe4f0;
  background: #f8fbff;
  page-break-inside: avoid;
}

.front-page-note {
  margin: 8pt 0 14pt;
  padding: 9pt 11pt;
  border-left: 3pt solid #93c5fd;
  background: #f8fbff;
  color: var(--color-subtitle);
  border-radius: 0 6pt 6pt 0;
  font-size: 8.8pt;
  line-height: 1.6;
}

.takeaway-block {
  margin: 10pt 0 14pt;
  padding: 10pt 12pt;
  border-radius: 8pt;
  border: 1px solid #cfe0ff;
  border-left: 4pt solid var(--color-primary);
  background: linear-gradient(180deg, #f8fbff 0%, #f1f7ff 100%);
  page-break-inside: avoid;
}

.takeaway-block strong {
  color: #1e3a8a;
}

.interpretation-note {
  margin: -6pt 0 14pt;
  padding: 7pt 10pt;
  border-radius: 6pt;
  background: #f8fafc;
  color: var(--color-subtitle);
  font-size: 8.6pt;
  line-height: 1.58;
}

.front-page-summary {
  display: block;
  margin: 8pt 0 16pt;
  padding: 14pt 16pt;
  border-radius: 10pt;
  background: linear-gradient(180deg, #f8fbff 0%, #eef4ff 100%);
  border: 1px solid #d9e6fb;
  page-break-inside: avoid;
}

.front-page-thesis {
  display: block;
  margin: 0 0 10pt;
  padding-left: 10pt;
  border-left: 4pt solid #2563eb;
  color: #0f172a;
  font-weight: 700;
  font-size: 10.4pt;
  line-height: 1.7;
}

.takeaway-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 8pt 10pt;
  margin: 10pt 0 16pt;
  page-break-inside: avoid;
}

.takeaway-card {
  border: 1px solid #dbe4f0;
  border-radius: 8pt;
  background: #f8fbff;
  padding: 9pt 10pt;
  min-height: 100%;
}

.takeaway-card-label {
  display: block;
  margin: 0 0 4pt;
  font-size: 7.6pt;
  line-height: 1.3;
  text-transform: uppercase;
  letter-spacing: 0.35pt;
  color: #475569;
  font-weight: 800;
}

.takeaway-card-value {
  display: block;
  font-size: 9.2pt;
  line-height: 1.58;
  color: #0f172a;
}

.methods-note {
  margin: 8pt 0 14pt;
  padding: 8pt 10pt;
  border-radius: 8pt;
  background: #f8fafc;
  border: 1px dashed #cbd5e1;
  color: #475569;
  font-size: 8.4pt;
  line-height: 1.6;
  page-break-inside: avoid;
}

@media print {
  .takeaway-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}
"""

REPORT_THEME_CSS = """
:root {
  --color-text: #1f2937;
  --color-title: #0f172a;
  --color-subtitle: #475569;
  --color-primary: #2563eb;
  --color-primary-soft: #eff6ff;
  --color-primary-border: #bfdbfe;
  --color-muted: #64748b;
  --color-line: #dbe4f0;
  --color-table-alt: #f8fbff;
  --color-cover-bg-top: #f8fbff;
  --color-cover-bg-bottom: #eef4ff;
}

.cover {
  padding: 50pt 46pt;
}

.cover-meta:empty,
.cover h2:empty {
  display: none;
}

.cover-badge {
  display: none;
}

body.has-cover .report-disclaimer {
  display: none;
}

.report-disclaimer {
  font-size: 7.8pt;
  color: #94a3b8;
  margin: 0 0 10pt;
}

h1 {
  margin-top: 20pt;
}

h1:first-of-type {
  margin-top: 4pt;
}

h2 + p strong,
h3 + p strong {
  color: var(--color-title);
}
"""


def normalize_text_for_pdf(text):
    """Clean obvious PDF-breaking artifacts before markdown parsing."""
    if not text:
        return text

    text = unicodedata.normalize('NFKC', text)
    text = ''.join(
        ch for ch in text
        if ch in ('\n', '\r', '\t') or ord(ch) >= 32
    )
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    text = re.sub(r'[ \t]+\n', '\n', text)
    text = re.sub(r'\n{3,}', '\n\n', text)

    cjk = r'\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff'

    # Stronger CJK spacing repair, especially for broken headings/metadata lines.
    text = re.sub(rf'([{cjk}])\s+([{cjk}])', r'\1\2', text)
    text = re.sub(rf'([{cjk}])\s+([，。！？；：、）】》％%])', r'\1\2', text)
    text = re.sub(rf'([（【《])\s+([{cjk}])', r'\1\2', text)
    text = re.sub(rf'([{cjk}])\s+([·—…])\s*([{cjk}])', r'\1\2\3', text)
    text = re.sub(rf'([{cjk}])\s+([A-Za-z0-9])', r'\1 \2', text)
    text = re.sub(rf'([A-Za-z0-9])\s+([{cjk}])', r'\1 \2', text)
    text = re.sub(r'(?m)^((?:[A-Z][A-Za-z\-]+\s*[:：]\s*)+)(.+)$', lambda m: re.sub(r'\s{2,}', ' ', m.group(1)).strip() + ' ' + m.group(2).strip(), text)

    # Normalize bullets/odd line starts that often confuse markdown parsers.
    text = re.sub(r'(?m)^[\x00-\x08\x0b\x0c\x0e-\x1f\u2022\u25aa\u25cf\uf0b7]\s*', '- ', text)
    text = re.sub(r'(?m)^[•●▪◦]\s*', '- ', text)

    # Collapse repeated internal whitespace without touching indentation.
    text = re.sub(r'(?m)(?<=\S)[ \t]{2,}(?=\S)', ' ', text)

    # Block-safe normalization: force clean boundaries around headings / hr / quotes / tables.
    lines = text.split('\n')
    out = []
    in_table = False
    pending_blank = False

    def flush_blank():
        nonlocal pending_blank
        if pending_blank and (not out or out[-1] != ''):
            out.append('')
        pending_blank = False

    for raw in lines:
        line = raw.rstrip()
        stripped = line.strip()

        if not stripped:
            pending_blank = True
            in_table = False
            continue

        # Undo accidental list prefixes before headings/tables (e.g. "- | ...", "- ## ...").
        stripped = re.sub(r'^[-*+]\s+(?=(?:#{1,6}\s|\|))', '', stripped)

        # Normalize ATX headings even if they have extra spacing after #.
        heading_match = re.match(r'^(#{1,6})\s*(.+?)\s*$', stripped)
        if heading_match:
            if out and out[-1] != '':
                out.append('')
            out.append(f"{heading_match.group(1)} {heading_match.group(2)}")
            out.append('')
            pending_blank = False
            in_table = False
            continue

        # Normalize horizontal rules.
        if re.fullmatch(r'[-*_]{3,}', stripped.replace(' ', '')):
            if out and out[-1] != '':
                out.append('')
            out.append('---')
            out.append('')
            pending_blank = False
            in_table = False
            continue

        # Normalize blockquotes and keep them out of list context.
        if stripped.startswith('>'):
            flush_blank()
            out.append('> ' + stripped.lstrip('> ').strip())
            in_table = False
            continue

        # Normalize table rows / separators and force surrounding blank lines.
        if '|' in stripped and stripped.count('|') >= 2:
            cells = [c.strip() for c in stripped.strip('|').split('|')]
            normalized = '| ' + ' | '.join(cells) + ' |'
            if not in_table:
                if out and out[-1] != '':
                    out.append('')
            out.append(normalized)
            in_table = True
            pending_blank = False
            continue
        elif in_table:
            out.append('')
            in_table = False

        # Ensure lists and following paragraphs don't fuse into one mega-list.
        if re.match(r'^[-*+]\s+.+$', stripped) or re.match(r'^\d+\.\s+.+$', stripped):
            flush_blank()
            out.append(stripped)
            continue

        flush_blank()
        out.append(stripped)

    if in_table and out and out[-1] != '':
        out.append('')

    text = '\n'.join(out)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text


def build_html(title, body_html, cover_title="", cover_subtitle="", cover_meta="", meta_lines=None):
    """Wrap processed body HTML in the full HTML document."""
    title = html.escape(title)
    cover_title = html.escape(cover_title)
    cover_subtitle = html.escape(cover_subtitle)
    if meta_lines is not None:
        cover_meta = '<br>'.join(html.escape(line) for line in meta_lines)
    elif cover_meta:
        parts = re.split(r'<br\s*/?>', cover_meta, flags=re.I)
        cover_meta = '<br>'.join(html.escape(part) for part in parts)
    cover_block = ""
    body_class = "has-cover" if cover_title else ""
    if cover_title:
        cover_block = f"""
<div class="cover">
  <div class="cover-tag">Deep Research Report · 深度研究报告</div>
  <h1>{cover_title}</h1>
  <h2>{cover_subtitle}</h2>
  <div class="cover-line"></div>
  <div class="cover-meta">{cover_meta}</div>
</div>
"""
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<style>{BASE_CSS}\n{REPORT_THEME_CSS}</style>
</head>
<body class="{body_class}">
{cover_block}
{body_html}
</body>
</html>"""


# ─── Markdown Processing ─────────────────────────────────────────────────────

def maybe_wrap_wide_tables_in_html(html):
    """Sanitize dense tables and prefer compact split tables over long vertical cards."""

    def plain_text(value):
        value = re.sub(r'<br\s*/?>', ' / ', value, flags=re.I)
        value = re.sub(r'<[^>]+>', '', value)
        value = re.sub(r'\s+', ' ', value).strip()
        return value

    def is_placeholder(value):
        text = plain_text(value)
        if not text:
            return True
        if text == '#':
            return True
        if re.fullmatch(r'#\d+', text):
            return True
        if text in {'—', '-', '–', '--', '——', '— —', 'N/A', 'n/a', 'NA', 'TBD', 'tbd', '/', '｜'}:
            return True
        return False

    def normalize_meta_key(value):
        text = plain_text(value).lower()
        text = re.sub(r'[\s:：\-_]+', '', text)
        return text

    def is_urlish(value):
        text = plain_text(value)
        return bool(re.search(r'(https?://|www\.)', text, flags=re.I))

    def is_metadata_header(value):
        key = normalize_meta_key(value)
        return key in {
            '来源', '信息来源', '出处', '参考', '参考来源',
            'source', 'sources', 'citation', 'citations',
            'url', 'urls', 'link', 'links', '参考链接', '链接'
        }

    def soft_wrap_url_text(value):
        value = re.sub(r'(?<=/)(?=[^/])', '<wbr>', value)
        value = re.sub(r'([?&=#%])', r'\1<wbr>', value)
        return value

    def normalize_cell_html(cell):
        cleaned = cell.strip()

        def anchor_repl(match):
            href = match.group(1)
            attrs = match.group(2) or ''
            text = match.group(3)
            plain = plain_text(text)
            if plain and plain == href:
                text = soft_wrap_url_text(text)
            return f'<a href="{href}"{attrs}>{text}</a>'

        cleaned = re.sub(
            r'<a\s+href="([^"]+)"([^>]*)>(.*?)</a>',
            anchor_repl,
            cleaned,
            flags=re.S | re.I,
        )

        if is_urlish(cleaned) and '<a ' not in cleaned.lower():
            cleaned = f'<span class="url-soft">{soft_wrap_url_text(cleaned)}</span>'
        return cleaned

    def sanitize_table(headers, rows):
        min_row_width = min((len(r) for r in rows), default=len(headers))
        if rows and len(headers) == min_row_width + 1 and is_placeholder(headers[0]):
            headers = headers[1:]
        width = min(len(headers), min((len(r) for r in rows), default=len(headers)))
        headers = headers[:width]
        rows = [r[:width] for r in rows]
        keep = []
        metadata_cols = []
        for idx in range(width):
            header_text = plain_text(headers[idx])
            column_values = [plain_text(r[idx]) for r in rows if idx < len(r)]
            if is_placeholder(header_text) and all(is_placeholder(v) for v in column_values):
                continue
            if is_metadata_header(header_text):
                urlish = [v for v in column_values if is_urlish(v)]
                if len(urlish) >= max(1, int(len(column_values) * 0.6)):
                    metadata_cols.append(idx)
            keep.append(idx)

        if keep:
            non_meta_keep = [i for i in keep if i not in metadata_cols]
            if len(non_meta_keep) >= 2 and len(keep) >= 4:
                keep = non_meta_keep

        if not keep:
            keep = list(range(width))

        headers = [headers[i] for i in keep]
        rows = [[row[i] for i in keep] for row in rows]

        placeholder_headers = [i for i, h in enumerate(headers) if is_placeholder(h)]
        if placeholder_headers and len(headers) > 1:
            keep2 = [i for i in range(len(headers)) if i not in placeholder_headers]
            headers = [headers[i] for i in keep2]
            rows = [[row[i] for i in keep2] for row in rows]

        cleaned_rows = []
        for row in rows:
            cleaned = []
            for cell in row:
                cell = cell.strip()
                cell = '' if is_placeholder(cell) else normalize_cell_html(cell)
                cleaned.append(cell)
            if any(plain_text(c) for c in cleaned):
                cleaned_rows.append(cleaned)
        return headers, cleaned_rows

    def build_table(headers, rows):
        parts = ['<table><thead><tr>']
        for h in headers:
            label = h.strip() or '字段'
            parts.append(f'<th>{label}</th>')
        parts.append('</tr></thead><tbody>')
        for row in rows:
            parts.append('<tr>')
            for cell in row:
                parts.append(f'<td>{cell.strip() or ""}</td>')
            parts.append('</tr>')
        parts.append('</tbody></table>')
        return ''.join(parts)

    def split_table(headers, rows, max_cols=4):
        if len(headers) <= max_cols:
            return [build_table(headers, rows)]
        chunks = []
        anchor_first = not is_metadata_header(headers[0])
        if anchor_first and max_cols >= 3:
            chunk_size = max_cols - 1
            start = 1
            while start < len(headers):
                end = min(start + chunk_size, len(headers))
                sub_headers = [headers[0]] + headers[start:end]
                sub_rows = [[row[0]] + row[start:end] for row in rows]
                chunks.append(build_table(sub_headers, sub_rows))
                start = end
            return chunks
        start = 0
        while start < len(headers):
            end = min(start + max_cols, len(headers))
            sub_headers = headers[start:end]
            sub_rows = [row[start:end] for row in rows]
            chunks.append(build_table(sub_headers, sub_rows))
            start = end
        return chunks

    def repl(match):
        table_html = match.group(0)
        headers = re.findall(r'<th[^>]*>(.*?)</th>', table_html, flags=re.S|re.I)
        row_chunks = re.findall(r'<tr[^>]*>(.*?)</tr>', table_html, flags=re.S|re.I)
        body_rows = []
        cell_texts = []
        for row in row_chunks[1:]:
            cells = re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', row, flags=re.S|re.I)
            if cells:
                body_rows.append(cells)
                cell_texts.extend(cells)

        if not headers or not body_rows:
            return f'<div class="table-wrap">{table_html}</div>'

        headers, body_rows = sanitize_table(headers, body_rows)
        dense = len(headers) >= 4
        long_cells = any(len(plain_text(c)) > 36 for c in cell_texts)
        many_rows = len(body_rows) >= 6
        source_like = sum(1 for h in headers if is_metadata_header(h)) >= max(1, len(headers) // 2)

        if len(headers) >= 5 or (dense and long_cells) or (dense and many_rows):
            tables = split_table(headers, body_rows, max_cols=4)
            wrapped = ''.join(f'<div class="split-table">{t}</div>' for t in tables)
            source_class = ' table-wrap-source' if source_like else ''
            return f'<div class="table-wrap wide-table split-table-group{source_class}">{wrapped}</div>'

        compact_html = build_table(headers, body_rows)
        source_class = ' table-wrap-source' if source_like else ''
        if dense or long_cells:
            return f'<div class="table-wrap wide-table{source_class}">{compact_html}</div>'
        return f'<div class="table-wrap{source_class}">{compact_html}</div>'

    return re.sub(r'<table[\s\S]*?</table>', repl, html, flags=re.I)


def _convert_front_page_summary(html):
    thesis_labels = r'(?:Core thesis|Thesis|Bottom line|Bottom-line judgment|Judgment|Recommendation|结论|核心判断|核心结论|建议)'
    html = re.sub(
        rf'<p><strong>({thesis_labels})[:：]</strong>\s*(.*?)</p>',
        r'<div class="front-page-summary"><div class="front-page-thesis"><strong>\1:</strong> \2</div></div>',
        html,
        flags=re.I | re.S,
    )

    html = re.sub(
        r'<div class="front-page-summary">\s*(<div class="front-page-thesis">.*?</div>)\s*</div>\s*(<ul>.*?</ul>)',
        r'<div class="front-page-summary">\1\2</div>',
        html,
        flags=re.S,
    )
    return html


TAKEAWAY_LABEL_PATTERNS = {
    'section judgment': r'(?:Section judgment|Judgment|本节判断|核心判断|结论判断)',
    'main driver': r'(?:Main driver|Core driver|核心驱动|主要驱动)',
    'main risk': r'(?:Main risk|Core risk|核心风险|主要风险)',
    'key unknown': r'(?:Key unknown|Main unknown|关键未知项|主要未知项|未知项)',
    'what would change this view': r'(?:What would change this view|What would change the conclusion|改变判断的条件|什么会改变这一判断|什么会改变结论)',
}


def _convert_takeaway_cards(html):
    paragraph_pattern = re.compile(r'<p><strong>([^<]{1,80})[:：]</strong>\s*(.*?)</p>', flags=re.I | re.S)
    matches = list(paragraph_pattern.finditer(html))
    if not matches:
        return html

    def normalize_label(label):
        raw = re.sub(r'<[^>]+>', '', label).strip()
        for canon, pattern in TAKEAWAY_LABEL_PATTERNS.items():
            if re.fullmatch(pattern, raw, flags=re.I):
                return canon, raw
        return None, raw

    rebuilt = []
    last = 0
    i = 0
    while i < len(matches):
        m = matches[i]
        canon, raw = normalize_label(m.group(1))
        if not canon:
            i += 1
            continue
        group = []
        j = i
        while j < len(matches):
            mj = matches[j]
            cj, rawj = normalize_label(mj.group(1))
            if not cj:
                break
            if j > i and mj.start() != matches[j-1].end():
                between = html[matches[j-1].end():mj.start()]
                if re.sub(r'\s+', '', between):
                    break
            group.append((mj, cj, rawj, mj.group(2).strip()))
            j += 1
            if len(group) >= 5:
                break

        if len(group) >= 2:
            rebuilt.append(html[last:group[0][0].start()])
            cards = []
            for _, _, rawj, value in group:
                cards.append(
                    f'<div class="takeaway-card"><span class="takeaway-card-label">{rawj}</span>'
                    f'<span class="takeaway-card-value">{value}</span></div>'
                )
            rebuilt.append('<div class="takeaway-grid">' + ''.join(cards) + '</div>')
            last = group[-1][0].end()
            i = j
        else:
            i += 1

    rebuilt.append(html[last:])
    return ''.join(rebuilt)



def _mark_methods_notes(html):
    return re.sub(
        r'<p><strong>((?:Methods note|Method note|方法说明|研究方式|证据分级|数字角色))[:：]</strong>\s*(.*?)</p>',
        r'<div class="methods-note"><strong>\1:</strong> \2</div>',
        html,
        flags=re.I | re.S,
    )


def style_generated_html(html):
    """Apply lightweight post-processing to markdown-generated HTML."""
    # Strip internal render hints; these should never leak into final delivery output.
    html = re.sub(
        r'<(?:p|li|div)>\s*[^<]*(?:优先拆成主题子表|退化成长卡片列表|该表信息较密)[^<]*</(?:p|li|div)>',
        '',
        html,
        flags=re.I,
    )
    html = maybe_wrap_wide_tables_in_html(html)
    html = re.sub(r'<li>\s*(<(?:h1|h2|h3|h4)[^>]*>.*?</(?:h1|h2|h3|h4)>)\s*</li>', r'\1', html, flags=re.S|re.I)
    html = re.sub(r'<li>\s*(<div class="callout[^"]*">.*?</div>)\s*</li>', r'\1', html, flags=re.S|re.I)
    html = re.sub(r'<p>\s*(?:#\d+|[—–-])\s*</p>', '', html, flags=re.I)

    # Tighten broken spacing inside headings generated from noisy upstream markdown.
    cjk = r'\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff'
    def heading_repl(match):
        tag = match.group(1)
        inner = match.group(2)
        inner = re.sub(rf'([{cjk}])\s+([{cjk}])', r'\1\2', inner)
        inner = re.sub(rf'([{cjk}])\s+([，。！？；：、])', r'\1\2', inner)
        inner = re.sub(r'\s+', ' ', inner).strip()
        return f'<{tag}>{inner}</{tag}>'
    html = re.sub(r'<(h[1-4])>(.*?)</\1>', heading_repl, html, flags=re.S|re.I)

    # Turn simple blockquotes into report callouts when they look like highlights.
    def quote_repl(match):
        inner = match.group(1).strip()
        plain = re.sub(r'<[^>]+>', '', inner).strip()
        if plain.startswith('预测:') or plain.startswith('预测：') or plain.startswith('风险:') or plain.startswith('风险：'):
            return f'<div class="callout callout-inference">{inner}</div>'
        return f'<blockquote>{inner}</blockquote>'

    html = re.sub(r'<blockquote>\s*(.*?)\s*</blockquote>', quote_repl, html, flags=re.S|re.I)
    return html


def repair_markdown_tables(md_text):
    """Repair common LLM-produced markdown table failures before parsing."""
    def normalize_table_candidate(line):
        line = line.strip()
        line = line.replace('｜', '|')
        line = re.sub(r'^[-*+]\s+(?=\|)', '', line)
        return line

    def parse_cells(row):
        return [c.strip() for c in row.strip('|').split('|')]

    def is_separator_row(row):
        cells = parse_cells(row)
        if not cells:
            return False
        for cell in cells:
            token = re.sub(r'\s+', '', cell)
            if not token:
                continue
            if not re.fullmatch(r':?-+:?', token):
                return False
        return True

    def is_bullet_placeholder(value):
        token = value.strip().lower()
        return token in {'', '-', '*', '+', '•', '●', '▪', '◦'}

    lines = md_text.split('\n')
    repaired = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = normalize_table_candidate(line)

        if '|' in stripped and stripped.count('|') >= 2:
            group = [stripped]
            j = i + 1
            while j < len(lines):
                nxt = normalize_table_candidate(lines[j])
                if nxt and '|' in nxt and nxt.count('|') >= 2:
                    group.append(nxt)
                    j += 1
                    continue
                break

            if len(group) >= 2:
                parsed_rows = [parse_cells(row) for row in group]

                if len(parsed_rows[0]) >= 2 and is_bullet_placeholder(parsed_rows[0][0]):
                    first_col_values = [row[0] if row else '' for row in parsed_rows[2:]]
                    second_header = parsed_rows[0][1].strip().lower()
                    if (
                        (first_col_values and all(is_bullet_placeholder(v) for v in first_col_values))
                        or second_header in {'#', 'no', 'no.', '序号', '编号'}
                    ):
                        parsed_rows = [row[1:] if len(row) > 1 else [''] for row in parsed_rows]

                first_cells = parsed_rows[0]
                if not is_separator_row(group[1]):
                    parsed_rows.insert(1, ['---'] * len(first_cells))
                else:
                    parsed_rows[1] = ['---'] * len(first_cells)

                normalized_group = []
                for cells in parsed_rows:
                    if len(cells) < len(first_cells):
                        cells.extend([''] * (len(first_cells) - len(cells)))
                    elif len(cells) > len(first_cells):
                        cells = cells[:len(first_cells)]
                    normalized_group.append('| ' + ' | '.join(cells) + ' |')

                if repaired and repaired[-1] != '':
                    repaired.append('')
                repaired.extend(normalized_group)
                repaired.append('')
                i = j
                continue

        repaired.append(line)
        i += 1

    return '\n'.join(repaired)


def process_markdown(md_text):
    """Convert markdown to HTML using a real markdown parser, then post-process for report styling."""
    import markdown

    md_text = repair_markdown_tables(md_text)

    extensions = [
        'extra',
        'tables',
        'fenced_code',
        'sane_lists',
        'nl2br',
    ]
    html = markdown.markdown(md_text, extensions=extensions, output_format='html5')
    return style_generated_html(html)


# ─── Cover / Meta extraction ─────────────────────────────────────────────────

def extract_cover_meta(md_text):
    """
    Try to extract cover fields from markdown frontmatter or first few lines.
    Returns (cover_title, cover_subtitle, meta_lines, cleaned_body)
    where meta_lines is a list of raw metadata strings (unjoined, unescaped).
    """
    lines = md_text.split('\n')

    title = ""
    subtitle = ""
    meta_lines = []

    # Look for YAML-style fields in first 15 lines
    for j, line in enumerate(lines[:15]):
        lower = line.lower()
        if line.startswith('title:') or line.startswith('# title:'):
            title = line.split(':', 1)[1].strip().strip('"\'')
        elif 'subtitle:' in lower or line.startswith('## subtitle:'):
            subtitle = line.split(':', 1)[1].strip().strip('"\'')
        elif line.startswith('date:') or lower.startswith('research date:'):
            meta_lines.append(f"研究日期：{line.split(':', 1)[1].strip()}")
        elif line.startswith('type:') or lower.startswith('research type:'):
            meta_lines.append(f"研究类型：{line.split(':', 1)[1].strip()}")

    # Strip frontmatter (--- ... ---)
    body_lines = lines
    if lines and lines[0].strip() == '---':
        end = None
        for k in range(1, min(20, len(lines))):
            if lines[k].strip() == '---':
                end = k
                break
        if end is not None:
            body_lines = lines[end+1:]

    return title, subtitle, meta_lines, '\n'.join(body_lines)


# ─── Main ─────────────────────────────────────────────────────────────────────

def convert(input_path, output_path=None, title=None):
    md_path = Path(input_path)
    if not md_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    md_text = md_path.read_text(encoding='utf-8', errors='replace')
    md_text = normalize_text_for_pdf(md_text)

    # Extract cover info
    cover_title, cover_subtitle, meta_lines, body_text = extract_cover_meta(md_text)

    # Use provided title or fall back
    report_title = title or cover_title or md_path.stem

    # Process markdown to HTML body
    body_html = process_markdown(body_text)

    # Build full HTML
    full_html = build_html(
        title=report_title,
        body_html=body_html,
        cover_title=cover_title,
        cover_subtitle=cover_subtitle,
        meta_lines=meta_lines,
    )

    # Output
    if output_path is None:
        output_path = md_path.with_suffix('.html')
    out_path = Path(output_path)
    out_path.write_text(full_html, encoding='utf-8')
    print(f"HTML written: {out_path}")
    return str(out_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert Deep Research markdown report to styled HTML')
    parser.add_argument('input', help='Input markdown file')
    parser.add_argument('output', nargs='?', help='Output HTML file (default: same name, .html)')
    parser.add_argument('--title', help='Report title (overrides frontmatter)')
    args = parser.parse_args()
    convert(args.input, args.output, args.title)
