"""Embedded CSS theme for generated Markdown/PDF reports."""

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
