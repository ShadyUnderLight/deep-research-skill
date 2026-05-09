#!/usr/bin/env python3
"""
Markdown → PDF one-shot pipeline.
Usage:
    python3 md_to_pdf.py <input.md> [output.pdf] [--title "Title"]
"""
import argparse
import subprocess
import sys
import os
from pathlib import Path


def run(args_list, description):
    print(f"\n▶ {description}")
    result = subprocess.run(args_list, shell=False, capture_output=False)
    if result.returncode != 0:
        print(f"❌ Failed: {description}")
        sys.exit(result.returncode)
    print(f"✅ {description}")


def main():
    parser = argparse.ArgumentParser(description='Markdown → PDF pipeline (markdown_to_html + render_pdf)')
    parser.add_argument('input', help='Input markdown file')
    parser.add_argument('output', nargs='?', help='Output PDF file (default: same name, .pdf)')
    parser.add_argument('--title', help='Report title (overrides frontmatter)')
    parser.add_argument('--landscape', action='store_true', help='Render in landscape orientation')
    parser.add_argument('--media', choices=['print', 'screen'], default='print')
    parser.add_argument('--margin-top', default='2cm')
    parser.add_argument('--margin-right', default='2.5cm')
    parser.add_argument('--margin-bottom', default='2cm')
    parser.add_argument('--margin-left', default='2.5cm')
    args = parser.parse_args()

    md_path = Path(args.input).resolve()
    if not md_path.exists():
        print(f"File not found: {md_path}")
        sys.exit(1)

    # Determine output PDF path
    if args.output:
        pdf_path = Path(args.output).resolve()
    else:
        pdf_path = md_path.with_suffix('.pdf')

    html_path = md_path.with_suffix('.html')
    scripts_dir = Path(__file__).parent.resolve()

    # Step 1: Markdown → HTML
    cmd = [sys.executable, str(scripts_dir / 'markdown_to_html.py'), str(md_path), str(html_path)]
    if args.title:
        cmd += ['--title', args.title]
    run(cmd, f"Markdown → HTML: {html_path.name}")

    # Step 2: HTML → PDF
    cmd = [sys.executable, str(scripts_dir / 'render_pdf.py'), str(html_path), str(pdf_path)]
    if args.title:
        cmd += ['--title', args.title]
    if args.landscape:
        cmd.append('--landscape')
    cmd += [
        '--media', args.media,
        '--margin-top', args.margin_top,
        '--margin-right', args.margin_right,
        '--margin-bottom', args.margin_bottom,
        '--margin-left', args.margin_left,
    ]
    run(cmd, f"HTML → PDF: {pdf_path.name}")

    print(f"\n✅ Complete: {pdf_path}")


if __name__ == '__main__':
    main()
