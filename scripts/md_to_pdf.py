#!/usr/bin/env python3
"""Markdown → PDF delivery entry point.

Usage:
    python3 md_to_pdf.py <input.md> [output.pdf] [--title "Title"]
"""

from __future__ import annotations

import argparse
import contextlib
import io
import sys
from pathlib import Path

_REQUIREMENTS_FILE = str(Path(__file__).resolve().parent.parent / "requirements.txt")


def _check_playwright_chromium() -> bool:
    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            browser.close()
        return True
    except Exception as exc:
        if "Executable doesn't exist" in str(exc):
            return False
        print(f"Error: Playwright Chromium found but failed to launch: {exc}", file=sys.stderr)
        raise SystemExit(1)


def _check_runtime_deps() -> None:
    missing: list[str] = []
    for module in ("markdown", "nh3", "playwright"):
        try:
            __import__(module)
        except ImportError:
            missing.append(module)

    if missing:
        print("Error: missing required Python packages: " + ", ".join(missing), file=sys.stderr)
        print(f"Run: {sys.executable} -m pip install -r {_REQUIREMENTS_FILE}", file=sys.stderr)
        raise SystemExit(1)

    if not _check_playwright_chromium():
        print("Error: Playwright Chromium browser is not installed", file=sys.stderr)
        print(f"Run: {sys.executable} -m playwright install chromium", file=sys.stderr)
        raise SystemExit(1)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Markdown → PDF delivery pipeline")
    parser.add_argument("input", help="Input Markdown file")
    parser.add_argument("output", nargs="?", help="Output PDF file (default: same name, .pdf)")
    parser.add_argument("--title", help="Report title (overrides frontmatter)")
    parser.add_argument("--landscape", action="store_true", help="Render in landscape orientation")
    parser.add_argument("--media", choices=["print", "screen"], default="print")
    parser.add_argument("--margin-top", default="2cm")
    parser.add_argument("--margin-right", default="2.5cm")
    parser.add_argument("--margin-bottom", default="2cm")
    parser.add_argument("--margin-left", default="2.5cm")
    parser.add_argument(
        "--allow-remote",
        action="store_true",
        help="Allow HTTP/HTTPS resources during PDF rendering (default: blocked)",
    )
    parser.add_argument(
        "--keep-html",
        action="store_true",
        help="Keep the intermediate HTML next to the requested PDF",
    )
    parser.add_argument(
        "--write-status",
        metavar="PATH",
        help="Explicitly write the delivery status to a Research Pack/report",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit only the structured delivery result as JSON",
    )
    args = parser.parse_args(argv)

    md_path = Path(args.input).resolve()
    if not md_path.exists():
        print(f"File not found: {md_path}")
        return 1

    _check_runtime_deps()

    from delivery.pipeline import run_delivery

    output = Path(args.output).resolve() if args.output else None
    captured = io.StringIO()
    stream = contextlib.redirect_stdout(captured) if args.json else contextlib.nullcontext()
    with stream:
        result = run_delivery(
            md_path,
            output,
            title=args.title,
            keep_html=args.keep_html,
            allow_remote=args.allow_remote,
            landscape=args.landscape,
            media=args.media,
            margin_top=args.margin_top,
            margin_right=args.margin_right,
            margin_bottom=args.margin_bottom,
            margin_left=args.margin_left,
            write_status_to=Path(args.write_status).resolve() if args.write_status else None,
        )

    if args.json:
        print(result.to_json())
    else:
        if result.errors:
            for error in result.errors:
                print(f"❌ {error}", file=sys.stderr)
        if result.ok:
            print(f"\n✅ Complete: {result.pdf_path or result.input_path}")

    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
