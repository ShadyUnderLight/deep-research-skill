#!/usr/bin/env python3
"""
Universal Markdown → Styled HTML converter for Deep Research reports.
Usage:
    python3 markdown_to_html.py <input.md> [output.html] [--title "Report Title"]
"""
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
  font-family: "PingFang SC", "Hiragino Sans GB", "Source Han Sans SC", "Microsoft YaHei", "Noto Sans CJK SC", Arial, sans-serif;
  font-size: 10.2pt;
  line-height: 1.76;
  color: var(--color-text);
  margin: 0;
  padding: 0;
  font-feature-settings: "kern" 1, "liga" 1;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  hyphens: auto;
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
  margin: 0 0 8pt;
  orphans: 3;
  widows: 3;
}

strong { color: var(--color-title); }
a { color: var(--color-primary); text-decoration: none; }

/* ── Lists ── */
ul, ol {
  margin: 6pt 0 12pt 1.35em;
  padding: 0;
}

li {
  margin: 0 0 4pt;
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

.wide-table table {
  font-size: 8.6pt;
}

.wide-table thead th,
.wide-table tbody td {
  padding: 6pt 7pt;
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
}

thead tr {
  background: #e8f0ff;
  color: var(--color-title);
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
  word-break: break-all;
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
  padding: 7pt 11pt;
  margin: 10pt 0;
  color: var(--color-subtitle);
  font-style: normal;
  border-radius: 0 6pt 6pt 0;
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
    text = re.sub(rf'([{cjk}])\s+([{cjk}])', r'\1\2', text)
    text = re.sub(rf'([{cjk}])\s+([，。！？；：、）】》])', r'\1\2', text)
    text = re.sub(rf'([（【《])\s+([{cjk}])', r'\1\2', text)
    text = re.sub(r'(?m)^[\x00-\x1f\u2022\u25aa\u25cf\uf0b7]\s*', '- ', text)
    text = re.sub(r'(?m)(?<=\S)[ \t]{2,}(?=\S)', ' ', text)
    return text


def build_html(title, body_html, cover_title="", cover_subtitle="", cover_meta=""):
    """Wrap processed body HTML in the full HTML document."""
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
    """Wrap dense tables in helper containers after markdown conversion."""
    def repl(match):
        table_html = match.group(0)
        headers = re.findall(r'<th[^>]*>(.*?)</th>', table_html, flags=re.S|re.I)
        rows = re.findall(r'<tr[^>]*>(.*?)</tr>', table_html, flags=re.S|re.I)
        cell_texts = []
        for row in rows[1:]:
            cell_texts.extend(re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', row, flags=re.S|re.I))
        dense = len(headers) >= 5
        long_cells = any(len(re.sub(r'<[^>]+>', '', c).strip()) > 40 for c in cell_texts)
        if dense or long_cells:
            note = '<div class="table-note">注：该表信息较密，若导出的 PDF 可读性不足，优先拆成两张主题子表而不是继续压缩列宽。</div>'
            return f'<div class="table-wrap wide-table">{note}{table_html}</div>'
        return f'<div class="table-wrap">{table_html}</div>'

    return re.sub(r'<table[\s\S]*?</table>', repl, html, flags=re.I)


def style_generated_html(html):
    """Apply lightweight post-processing to markdown-generated HTML."""
    html = maybe_wrap_wide_tables_in_html(html)

    # Turn simple blockquotes into report callouts when they look like highlights.
    def quote_repl(match):
        inner = match.group(1).strip()
        plain = re.sub(r'<[^>]+>', '', inner).strip()
        if plain.startswith('预测：') or plain.startswith('风险：'):
            return f'<div class="callout callout-inference">{inner}</div>'
        return f'<blockquote>{inner}</blockquote>'

    html = re.sub(r'<blockquote>\s*(.*?)\s*</blockquote>', quote_repl, html, flags=re.S|re.I)
    return html


def process_markdown(md_text):
    """Convert markdown to HTML using a real markdown parser, then post-process for report styling."""
    import markdown

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
    Returns (cover_title, cover_subtitle, cover_meta, cleaned_body)
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

    cover_meta = '<br>'.join(meta_lines) if meta_lines else ''

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

    return title, subtitle, cover_meta, '\n'.join(body_lines)


# ─── Main ─────────────────────────────────────────────────────────────────────

def convert(input_path, output_path=None, title=None):
    md_path = Path(input_path)
    if not md_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    md_text = md_path.read_text(encoding='utf-8', errors='replace')
    md_text = normalize_text_for_pdf(md_text)

    # Extract cover info
    cover_title, cover_subtitle, cover_meta, body_text = extract_cover_meta(md_text)

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
        cover_meta=cover_meta,
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
