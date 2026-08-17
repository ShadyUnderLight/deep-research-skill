#!/usr/bin/env python3
"""Run offline HTML/PDF structure and Playwright visual smoke checks.

This intentionally avoids pixel equality. It emits screenshots and PDF text
artifacts that explain a failure while checking stable structural properties.
"""

from __future__ import annotations

import argparse
import asyncio
import re
import shutil
import sys
import tempfile
import unicodedata
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from delivery.pipeline import run_delivery  # noqa: E402


class StructureParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.counts: dict[str, int] = {}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.counts[tag] = self.counts.get(tag, 0) + 1


def _compact_extracted_text(text: str) -> str:
    """Normalize font-mapped glyphs and layout whitespace for marker checks."""

    return re.sub(r"\s+", "", unicodedata.normalize("NFKC", text)).replace("\u00ad", "")


async def _screenshot(html_path: Path, output_path: Path) -> None:
    from playwright.async_api import async_playwright

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        try:
            page = await browser.new_page(viewport={"width": 1280, "height": 900})
            await page.emulate_media(media="print")
            await page.goto(html_path.as_uri(), wait_until="networkidle")
            await page.screenshot(path=str(output_path), full_page=True)
        finally:
            await browser.close()


def _check_case(
    markdown_path: Path,
    artifact_dir: Path,
    *,
    marker: str,
    min_pages: int = 1,
    expected_tags: dict[str, int] | None = None,
) -> list[str]:
    output_pdf = artifact_dir / f"{markdown_path.stem}.pdf"
    result = run_delivery(markdown_path, output_pdf, keep_html=True)
    errors: list[str] = []
    if not result.ok:
        return [f"{markdown_path.name}: delivery failed: {'; '.join(result.errors)}"]
    if not result.html_path or not result.html_path.is_file():
        return [f"{markdown_path.name}: kept HTML artifact is missing"]
    if not result.pdf_path or not result.pdf_path.is_file():
        return [f"{markdown_path.name}: PDF artifact is missing"]

    parser = StructureParser()
    parser.feed(result.html_path.read_text(encoding="utf-8"))
    for tag, minimum in (expected_tags or {}).items():
        if parser.counts.get(tag, 0) < minimum:
            errors.append(
                f"{markdown_path.name}: expected at least {minimum} <{tag}> tags, "
                f"found {parser.counts.get(tag, 0)}"
            )

    from pypdf import PdfReader

    reader = PdfReader(str(result.pdf_path))
    if len(reader.pages) < min_pages:
        errors.append(f"{markdown_path.name}: expected at least {min_pages} PDF pages, found {len(reader.pages)}")
    page_texts = [(page.extract_text() or "").strip() for page in reader.pages]
    blank_pages = [index + 1 for index, text in enumerate(page_texts) if not text]
    if blank_pages:
        errors.append(f"{markdown_path.name}: blank extracted PDF pages: {blank_pages}")
    if _compact_extracted_text(marker) not in _compact_extracted_text("\n".join(page_texts)):
        errors.append(f"{markdown_path.name}: missing extracted marker {marker!r}")

    screenshot_path = artifact_dir / f"{markdown_path.stem}.png"
    asyncio.run(_screenshot(result.html_path, screenshot_path))
    if not screenshot_path.is_file() or screenshot_path.stat().st_size == 0:
        errors.append(f"{markdown_path.name}: visual smoke screenshot is empty")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check delivery HTML/PDF structure and visual smoke")
    parser.add_argument(
        "--artifact-dir",
        type=Path,
        help="Directory for generated PDF/HTML/screenshot artifacts (default: temporary)",
    )
    args = parser.parse_args(argv)

    cases_dir = ROOT / "tests" / "fixtures" / "delivery"
    owned_temp: tempfile.TemporaryDirectory[str] | None = None
    if args.artifact_dir:
        artifact_dir = args.artifact_dir.resolve()
        artifact_dir.mkdir(parents=True, exist_ok=True)
    else:
        owned_temp = tempfile.TemporaryDirectory(prefix="pdf-regression-")
        artifact_dir = Path(owned_temp.name)

    cases = [
        (cases_dir / "cjk-heavy.md", "中文交付回归", 1, {"h1": 1, "h2": 1}),
        (cases_dir / "mixed-language.md", "mixed-language-marker-2026", 1, {"h1": 1}),
        (cases_dir / "long-table.md", "long-table-marker-2026", 1, {"table": 2}),
        (cases_dir / "code-heavy.md", "code-heavy-marker", 1, {"pre": 2}),
        (cases_dir / "multi-page.md", "multi-page-marker-2026", 2, {"h3": 1, "h4": 1}),
    ]
    failures: list[str] = []
    for path, marker, min_pages, expected_tags in cases:
        failures.extend(
            _check_case(
                path,
                artifact_dir,
                marker=marker,
                min_pages=min_pages,
                expected_tags=expected_tags,
            )
        )

    special_dir = artifact_dir / "hash path #frag/query ?q/中文 路径"
    special_dir.mkdir(parents=True, exist_ok=True)
    special_input = special_dir / "input#frag?query 中文.md"
    shutil.copyfile(cases_dir / "mixed-language.md", special_input)
    failures.extend(
        _check_case(
            special_input,
            special_dir,
            marker="mixed-language-marker-2026",
            expected_tags={"h1": 1},
        )
    )

    if failures:
        print("PDF regression failures:")
        for failure in failures:
            print(f"- {failure}")
        print(f"Artifacts: {artifact_dir}")
        return 1
    print(f"PDF structure/visual smoke passed for {len(cases) + 1} fixtures")
    print(f"Artifacts: {artifact_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
