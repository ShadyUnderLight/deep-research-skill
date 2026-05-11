#!/usr/bin/env python3
"""
Universal HTML → PDF renderer using Playwright.
Usage:
    python3 render_pdf.py <input.html> [output.pdf]
"""
import argparse
import asyncio
import os
from pathlib import Path


async def html_to_pdf(html_path, pdf_path=None, format="A4",
                       margin_top="2cm", margin_bottom="2cm",
                       margin_left="2.5cm", margin_right="2.5cm",
                       print_background=True, landscape=False,
                       prefer_css_page_size=True,
                       media="print",
                       title=None,
                       block_remote=True):
    """
    Render HTML file to PDF via Playwright Chromium.
    """
    from playwright.async_api import async_playwright

    html_path = Path(html_path).resolve()
    if not html_path.exists():
        raise FileNotFoundError(f"HTML file not found: {html_path}")

    # Default PDF path: same name, .pdf
    if pdf_path is None:
        pdf_path = html_path.with_suffix('.pdf')
    pdf_path = Path(pdf_path)

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        if block_remote:
            await page.route("**/*", lambda route: route.abort() if route.request.url.startswith(("http://", "https://")) else route.continue_())

        file_url = f"file://{html_path}"
        await page.goto(file_url, wait_until="networkidle")
        await page.emulate_media(media=media)

        pdf_kwargs = {
            "path": str(pdf_path),
            "format": format,
            "margin": {
                "top": margin_top,
                "bottom": margin_bottom,
                "left": margin_left,
                "right": margin_right,
            },
            "print_background": print_background,
            "landscape": landscape,
            "prefer_css_page_size": prefer_css_page_size,
            "tagged": True,
        }
        if title:
            await page.evaluate("(t) => { document.title = t; }", title)

        await page.pdf(**pdf_kwargs)
        await browser.close()

    size = os.path.getsize(pdf_path)
    print(f"PDF generated: {pdf_path}")
    print(f"File size: {size:,} bytes ({size / 1024:.1f} KB)")
    return str(pdf_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Render HTML to PDF via Playwright')
    parser.add_argument('input', help='Input HTML file')
    parser.add_argument('output', nargs='?', help='Output PDF file (default: same name, .pdf)')
    parser.add_argument('--format', default='A4', help='Page format (default: A4)')
    parser.add_argument('--title', help='PDF title / document title override')
    parser.add_argument('--landscape', action='store_true', help='Render in landscape orientation')
    parser.add_argument('--margin-top', default='2cm')
    parser.add_argument('--margin-right', default='2.5cm')
    parser.add_argument('--margin-bottom', default='2cm')
    parser.add_argument('--margin-left', default='2.5cm')
    parser.add_argument('--media', choices=['print', 'screen'], default='print', help='Emulated media type')
    parser.add_argument('--no-bg', action='store_true', help='Disable background graphics')
    parser.add_argument('--no-prefer-css-page-size', action='store_true', help='Ignore CSS @page size when rendering')
    parser.add_argument('--allow-remote', action='store_true', help='Allow HTTP/HTTPS resource requests during PDF rendering (default: blocked)')
    args = parser.parse_args()

    asyncio.run(html_to_pdf(
        args.input,
        args.output,
        format=args.format,
        margin_top=args.margin_top,
        margin_right=args.margin_right,
        margin_bottom=args.margin_bottom,
        margin_left=args.margin_left,
        landscape=args.landscape,
        prefer_css_page_size=not args.no_prefer_css_page_size,
        media=args.media,
        print_background=not args.no_bg,
        title=args.title,
        block_remote=not args.allow_remote,
    ))
