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


# ─── Inline Markdown Processing ───────────────────────────────────────────────

def process_inline(text):
    """
    Process inline markdown: bold, italic, code, links.
    Order matters: code first (to avoid processing inside code),
    then bold/italic, then links.
    """
    # Inline code: `code`
    text = re.sub(r'`([^`\n]+)`', r'<code>\1</code>', text)
    # Bold + italic: ***text***
    text = re.sub(r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>', text)
    # Bold: **text**
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Italic: *text*
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    # Links: [text](url)
    text = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', text)
    return text


def escape_html(text):
    """Escape HTML special characters (for pre/code blocks)."""
    return (text
        .replace('&', '&amp;')
        .replace('<', '&lt;')
        .replace('>', '&gt;')
        .replace('"', '&quot;'))


def normalize_text_for_pdf(text):
    """Clean obvious PDF-breaking artifacts before markdown parsing.

    Goals:
    - remove control chars like NUL
    - normalize odd unicode spacing/forms
    - collapse spurious spaces between adjacent CJK chars
    - collapse repeated internal whitespace without destroying markdown structure
    """
    if not text:
        return text

    text = unicodedata.normalize('NFKC', text)

    # Remove control chars except tab/newline/carriage return.
    text = ''.join(
        ch for ch in text
        if ch in ('\n', '\r', '\t') or ord(ch) >= 32
    )

    # Normalize line endings.
    text = text.replace('\r\n', '\n').replace('\r', '\n')

    # Remove trailing spaces and tabs at line ends.
    text = re.sub(r'[ \t]+\n', '\n', text)

    # Collapse 3+ blank lines.
    text = re.sub(r'\n{3,}', '\n\n', text)

    # Remove accidental spaces between adjacent Chinese/Japanese/Korean chars.
    cjk = r'\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff'
    text = re.sub(rf'([{cjk}])\s+([{cjk}])', r'\1\2', text)

    # Remove accidental spaces between CJK and Chinese punctuation.
    text = re.sub(rf'([{cjk}])\s+([，。！？；：、）】》])', r'\1\2', text)
    text = re.sub(rf'([（【《])\s+([{cjk}])', r'\1\2', text)

    # Normalize bullet-like garbage chars at line starts.
    text = re.sub(r'(?m)^[\x00-\x1f\u2022\u25aa\u25cf\uf0b7]\s*', '- ', text)

    # Collapse runs of spaces inside lines, but keep indentation at line start.
    text = re.sub(r'(?m)(?<=\S)[ \t]{2,}(?=\S)', ' ', text)

    return text


def maybe_wrap_wide_table(html, header_cells, body_rows):
    """Add a wrapper and note for wide / dense tables to improve PDF readability."""
    dense = len(header_cells) >= 5
    long_cells = any(len(cell) > 40 for row in body_rows for cell in row)
    if dense or long_cells:
        note = '<div class="table-note">注：该表信息较密，若导出的 PDF 可读性不足，优先拆成两张主题子表而不是继续压缩列宽。</div>'
        return f'<div class="table-wrap wide-table">{note}{html}</div>'
    return f'<div class="table-wrap">{html}</div>'


# ─── Table Parsing ────────────────────────────────────────────────────────────

def is_separator_line(line):
    """Return True if line is a markdown table separator: |---|:---|:---:|"""
    cells = line.strip().strip('|').split('|')
    return all(
        re.match(r'^[\-: ]+$', cell.strip()) or cell.strip() == ''
        for cell in cells
    )


def split_table_row(line):
    r"""
    Split a markdown table row into cells, handling:
      - Leading/trailing pipes: | cell1 | cell2 |
      - Escaped pipes inside cells: cell \| with space
      - Pipes inside parentheses or brackets are NOT column separators
    Strategy: scan character by character; only treat '|' as a separator when
    we are not inside () [] {} <> or inside a quoted string.
    """
    stripped = line.strip().strip('|')
    cells = []
    current = []
    depth = 0  # parenthesis/bracket depth
    in_backtick = False
    i = 0

    while i < len(stripped):
        ch = stripped[i]

        # Toggle backtick-quote state
        if ch == '`' and not in_backtick:
            in_backtick = True
        elif ch == '`' and in_backtick:
            in_backtick = False
        elif ch == '\\' and i + 1 < len(stripped) and stripped[i+1] == '|':
            # Escaped pipe: keep the literal | character, skip the backslash
            current.append('|')
            i += 2
            continue

        # Track bracket depth (only outside backticks)
        if not in_backtick:
            if ch in '([':
                depth += 1
            elif ch in ')]':
                depth -= 1

        # Separator: only split when at zero depth and not in backtick
        if ch == '|' and depth == 0 and not in_backtick:
            cells.append(''.join(current).strip())
            current = []
        else:
            current.append(ch)

        i += 1

    # Last cell
    if current:
        cells.append(''.join(current).strip())

    return [c.replace('\\|', '|') for c in cells]


def render_table_row(cells, is_header=False):
    """Render a list of markdown cells into an HTML <tr>."""
    tag = 'th' if is_header else 'td'
    html = '<tr>'
    for cell in cells:
        # Convert literal newlines inside cells to <br> for multi-line cells
        cell_content = process_inline(cell.replace('\n', '<br>'))
        html += f'<{tag}>{cell_content}</{tag}>'
    html += '</tr>'
    return html


def parse_table(rows):
    """
    Parse a list of markdown table row strings (including separator row).
    Returns HTML <table> string with inline processing applied per cell.
    """
    if len(rows) < 2:
        return ''
    header_cells = split_table_row(rows[0])
    body_rows = []
    html = '<table><thead>'
    html += render_table_row(header_cells, is_header=True)
    html += '</thead><tbody>'
    for row in rows[2:]:
        if row.strip() and is_separator_line(row):
            continue
        body_cells = split_table_row(row)
        body_rows.append(body_cells)
        html += render_table_row(body_cells, is_header=False)
    html += '</tbody></table>'
    return maybe_wrap_wide_table(html, header_cells, body_rows)


# ─── Markdown Processing ─────────────────────────────────────────────────────

def is_pagebreak(line):
    """Return True if line is a pagebreak marker."""
    stripped = line.strip()
    return stripped in ('---', '***', '****', '## pagebreak ##', '<!-- pagebreak -->', '***')


def flush_list(result, list_type, items):
    if not items:
        return None, []
    tag = 'ol' if list_type == 'ol' else 'ul'
    html = [f'<{tag}>']
    for item in items:
        html.append(f'<li>{process_inline(item)}</li>')
    html.append(f'</{tag}>')
    result.append(''.join(html))
    return None, []


def process_markdown(md_text):
    """
    Convert markdown to HTML with custom extensions for deep-research reports.
    """
    lines = md_text.split('\n')
    result = []
    i = 0

    in_code_block = False
    in_table_rows = []  # accumulate table rows until separator resolved
    list_type = None
    list_items = []

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # ── Code block ──
        if stripped.startswith('```'):
            if in_table_rows:
                result.append(parse_table(in_table_rows))
                in_table_rows = []
            list_type, list_items = flush_list(result, list_type, list_items)
            if not in_code_block:
                in_code_block = True
                result.append('<pre><code>')
            else:
                result.append('</code></pre>')
            in_code_block = not in_code_block
            i += 1
            continue
        if in_code_block:
            result.append(escape_html(line))
            i += 1
            continue

        # ── Blank line ──
        if not stripped:
            if in_table_rows:
                result.append(parse_table(in_table_rows))
                in_table_rows = []
            list_type, list_items = flush_list(result, list_type, list_items)
            i += 1
            continue

        # ── Page break ──
        if is_pagebreak(stripped):
            if in_table_rows:
                result.append(parse_table(in_table_rows))
                in_table_rows = []
            list_type, list_items = flush_list(result, list_type, list_items)
            result.append('<div class="pb"></div>')
            i += 1
            continue

        # ── Callout block: :::callout-NAME ... ::: ──
        if stripped.startswith(':::callout'):
            if in_table_rows:
                result.append(parse_table(in_table_rows))
                in_table_rows = []
            list_type, list_items = flush_list(result, list_type, list_items)
            callout_type = stripped.split(':::callout')[1].strip()
            callout_content_lines = []
            i += 1
            while i < len(lines) and lines[i].strip() != ':::':
                callout_content_lines.append(lines[i])
                i += 1
            callout_body = process_inline('<br>'.join([l for l in callout_content_lines if l.strip()]))
            result.append(f'<div class="callout callout-{callout_type}">{callout_body}</div>')
            i += 1  # skip the closing :::
            continue

        # ── Table row ──
        if '|' in stripped and stripped.startswith('|'):
            list_type, list_items = flush_list(result, list_type, list_items)
            in_table_rows.append(line)

            if len(in_table_rows) == 1:
                j = i + 1
                while j < len(lines) and not lines[j].strip():
                    j += 1
                if j < len(lines) and is_separator_line(lines[j].strip()):
                    in_table_rows.append(lines[j])
                    i = j + 1
                    continue
                elif len(in_table_rows) == 1 and not (j < len(lines) and '|' in lines[j].strip()):
                    result.append(line_to_html(stripped))
                    in_table_rows = []
                    i += 1
                    continue
            elif len(in_table_rows) == 2 and is_separator_line(in_table_rows[1]):
                i += 1
                continue
            else:
                i += 1
                continue
            i += 1
            continue
        else:
            if in_table_rows:
                result.append(parse_table(in_table_rows))
                in_table_rows = []

        # ── List items ──
        unordered_match = re.match(r'^[-*]\s+(.+)$', stripped)
        ordered_match = re.match(r'^\d+\.\s+(.+)$', stripped)
        if unordered_match:
            if list_type not in (None, 'ul'):
                list_type, list_items = flush_list(result, list_type, list_items)
            list_type = 'ul'
            list_items.append(unordered_match.group(1))
            i += 1
            continue
        if ordered_match:
            if list_type not in (None, 'ol'):
                list_type, list_items = flush_list(result, list_type, list_items)
            list_type = 'ol'
            list_items.append(ordered_match.group(1))
            i += 1
            continue
        else:
            list_type, list_items = flush_list(result, list_type, list_items)

        # ── Regular line ──
        result.append(line_to_html(stripped))
        i += 1

    if in_table_rows:
        result.append(parse_table(in_table_rows))
    list_type, list_items = flush_list(result, list_type, list_items)

    return '\n'.join(result)


def line_to_html(line):
    """Convert a single non-special markdown line to HTML."""
    if not line:
        return ''

    # Heading
    if line.startswith('#### '):
        return f'<h4>{process_inline(line[5:])}</h4>'
    if line.startswith('### '):
        return f'<h3>{process_inline(line[4:])}</h3>'
    if line.startswith('## '):
        return f'<h2>{process_inline(line[3:])}</h2>'
    if line.startswith('# '):
        return f'<h1>{process_inline(line[2:])}</h1>'

    # HR
    if line in ('---', '***'):
        return '<hr>'

    # Blockquote / source attribution
    if line.startswith('>'):
        content = line.lstrip('>').strip()
        return f'<blockquote>{process_inline(content)}</blockquote>'

    # Unordered list item
    if line.startswith('- ') or line.startswith('* '):
        return f'<p>{process_inline(line[2:])}</p>'

    # Paragraph
    return f'<p>{process_inline(line)}</p>'


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
