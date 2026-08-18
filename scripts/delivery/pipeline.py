"""Markdown → HTML → PDF orchestration with explicit artifact lifecycle."""

from __future__ import annotations

import asyncio
import tempfile
from pathlib import Path

from .models import DeliveryResult, DeliveryStatus, sha256_file
from .status import write_delivery_status


def _validate_non_empty_file(path: Path, label: str) -> int:
    if not path.is_file():
        raise RuntimeError(f"{label} renderer returned without creating {path}")
    size = path.stat().st_size
    if size <= 0:
        raise RuntimeError(f"{label} artifact is empty: {path}")
    return size


def _validate_pdf_artifact(path: Path) -> int:
    size = _validate_non_empty_file(path, "PDF")
    with path.open("rb") as stream:
        header = stream.read(4)
    if header != b"%PDF":
        raise RuntimeError(f"PDF artifact has invalid header {header!r}: {path}")
    return size


def _render_pdf(
    html_path: Path,
    pdf_path: Path,
    *,
    title: str | None,
    landscape: bool,
    media: str,
    margin_top: str,
    margin_right: str,
    margin_bottom: str,
    margin_left: str,
    allow_remote: bool,
) -> None:
    from render_pdf import html_to_pdf

    asyncio.run(
        html_to_pdf(
            html_path,
            pdf_path,
            title=title,
            landscape=landscape,
            media=media,
            margin_top=margin_top,
            margin_right=margin_right,
            margin_bottom=margin_bottom,
            margin_left=margin_left,
            block_remote=not allow_remote,
        )
    )


def run_delivery(
    input_path: Path,
    output_path: Path | None = None,
    *,
    title: str | None = None,
    keep_html: bool = False,
    allow_remote: bool = False,
    landscape: bool = False,
    media: str = "print",
    margin_top: str = "2cm",
    margin_right: str = "2.5cm",
    margin_bottom: str = "2cm",
    margin_left: str = "2.5cm",
    write_status_to: Path | None = None,
) -> DeliveryResult:
    """Run the delivery pipeline and return a structured, auditable result.

    Intermediate HTML lives in a private temporary directory by default.
    ``keep_html`` is an explicit opt-in and places it next to the requested
    PDF output.  Status writeback is also opt-in and never mutates the input
    Markdown implicitly.
    """

    input_path = Path(input_path).resolve()
    if not input_path.is_file():
        return DeliveryResult(
            input_path=input_path,
            errors=[f"Input file not found: {input_path}"],
        )

    pdf_path = Path(output_path).resolve() if output_path else input_path.with_suffix(".pdf")
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    result = DeliveryResult(
        input_path=input_path,
        input_sha256=sha256_file(input_path),
        pdf_path=pdf_path,
        kept_html=keep_html,
    )

    with tempfile.TemporaryDirectory(prefix="deep-research-delivery-") as temp_dir:
        html_path = pdf_path.with_suffix(".html") if keep_html else Path(temp_dir) / f"{input_path.stem}.html"
        try:
            from markdown_to_html import convert

            convert(input_path, html_path, title)
            _validate_non_empty_file(html_path, "HTML")
            result.markdown_status = DeliveryStatus.MD_READY
            result.html_sha256 = sha256_file(html_path)
            if keep_html:
                result.html_path = html_path
        except Exception as exc:
            result.errors.append(f"Markdown to HTML failed: {exc}")
            if write_status_to:
                try:
                    write_delivery_status(Path(write_status_to), result)
                except Exception as exc:
                    result.errors.append(f"Delivery status writeback failed: {exc}")
            return result

        try:
            _render_pdf(
                html_path,
                pdf_path,
                title=title,
                landscape=landscape,
                media=media,
                margin_top=margin_top,
                margin_right=margin_right,
                margin_bottom=margin_bottom,
                margin_left=margin_left,
                allow_remote=allow_remote,
            )
            result.pdf_size_bytes = _validate_pdf_artifact(pdf_path)
            result.delivery_status = DeliveryStatus.PDF_READY
            result.pdf_sha256 = sha256_file(pdf_path)
        except Exception as exc:
            result.delivery_status = DeliveryStatus.PDF_FAILED
            result.errors.append(f"HTML to PDF failed (Chromium/PDF renderer): {exc}")

    if write_status_to:
        try:
            write_delivery_status(Path(write_status_to), result)
        except Exception as exc:
            result.errors.append(f"Delivery status writeback failed: {exc}")
    return result
