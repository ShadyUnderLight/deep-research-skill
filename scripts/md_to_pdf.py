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


def run(cmd, description):
    print(f"\n▶ {description}")
    result = subprocess.run(cmd, shell=True, capture_output=False)
    if result.returncode != 0:
        print(f"❌ Failed: {description}")
        sys.exit(result.returncode)
    print(f"✅ {description}")


def main():
    parser = argparse.ArgumentParser(description='Markdown → PDF pipeline (markdown_to_html + render_pdf)')
    parser.add_argument('input', help='Input markdown file')
    parser.add_argument('output', nargs='?', help='Output PDF file (default: same name, .pdf)')
    parser.add_argument('--title', help='Report title (overrides frontmatter)')
    args = parser.parse()

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

    # Step 1: Markdown → HTML
    title_flag = f'--title "{args.title}"' if args.title else ''
    run(
        f'python3 {__file__.parent}/markdown_to_html.py "{md_path}" "{html_path}" {title_flag}',
        f"Markdown → HTML: {html_path.name}"
    )

    # Step 2: HTML → PDF
    run(
        f'python3 {__file__.parent}/render_pdf.py "{html_path}" "{pdf_path}"',
        f"HTML → PDF: {pdf_path.name}"
    )

    print(f"\n✅ Complete: {pdf_path}")


if __name__ == '__main__':
    main()
