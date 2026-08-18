#!/usr/bin/env python3
"""
Universal Markdown → Styled HTML converter for Deep Research reports.

Security model: this script is designed for processing agent-authored
Deep Research reports. It escapes frontmatter-derived metadata fields
(title, cover_title, cover_subtitle, cover_meta) and sanitizes body
HTML via nh3 to strip dangerous tags, event handlers, and javascript:
URLs. Only safe tags (p, div, table, a, code, pre, etc.) and
attributes (class, id, href, colspan, etc.) are allowed.
Inline style attributes, img tags, script, iframe, and event
handlers are removed. Remote HTTP/HTTPS resources are blocked by
default during PDF rendering (controlled via --allow-remote).

Usage:
    python3 markdown_to_html.py <input.md> [output.html] [--title "Report Title"]
"""
import argparse
import sys
from pathlib import Path

# ── Compatibility facade ────────────────────────────────────────────────────
#
# The public script path and the historical helper names remain stable for
# existing callers, while the implementation now lives in independently
# testable delivery modules.  The CSS theme is a separate module so renderer
# tests can receive it explicitly without coupling to the CLI entry point.
from delivery.theme import BASE_CSS, REPORT_THEME_CSS  # noqa: E402
from delivery.html_renderer import (  # noqa: E402
    build_html as _render_build_html,
    process_markdown,
    style_generated_html,
)
from delivery.metadata import extract_cover_meta  # noqa: E402
from delivery.normalization import normalize_text_for_pdf  # noqa: E402
from delivery.sanitizer import sanitize_html  # noqa: E402
from delivery.table_repair import repair_markdown_tables  # noqa: E402
from delivery.tables import maybe_wrap_wide_tables_in_html  # noqa: E402


def build_html(title, body_html, cover_title="", cover_subtitle="", cover_meta="", meta_lines=None):
    """Backward-compatible wrapper around the modular HTML renderer."""

    return _render_build_html(
        title,
        body_html,
        base_css=BASE_CSS,
        report_theme_css=REPORT_THEME_CSS,
        cover_title=cover_title,
        cover_subtitle=cover_subtitle,
        cover_meta=cover_meta,
        meta_lines=meta_lines,
    )


def convert(input_path, output_path=None, title=None):
    """Convert Markdown to HTML through the modular delivery stages."""

    md_path = Path(input_path)
    if not md_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    md_text = normalize_text_for_pdf(md_path.read_text(encoding="utf-8", errors="replace"))
    cover_title, cover_subtitle, meta_lines, body_text = extract_cover_meta(md_text)
    report_title = title or cover_title or md_path.stem
    full_html = build_html(
        title=report_title,
        body_html=process_markdown(body_text),
        cover_title=cover_title,
        cover_subtitle=cover_subtitle,
        meta_lines=meta_lines,
    )
    out_path = Path(output_path) if output_path is not None else md_path.with_suffix(".html")
    out_path.write_text(full_html, encoding="utf-8")
    print(f"HTML written: {out_path}")
    return str(out_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert Deep Research markdown report to styled HTML')
    parser.add_argument('input', help='Input markdown file')
    parser.add_argument('output', nargs='?', help='Output HTML file (default: same name, .html)')
    parser.add_argument('--title', help='Report title (overrides frontmatter)')
    args = parser.parse_args()
    convert(args.input, args.output, args.title)
