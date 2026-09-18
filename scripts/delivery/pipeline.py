"""Markdown → HTML → PDF orchestration with explicit artifact lifecycle."""

from __future__ import annotations

import asyncio
import os
import tempfile
from pathlib import Path

from .models import DeliveryResult, DeliveryStatus
from .paths import paths_collide, pdf_output_reason
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

    Path conflicts (same file, hardlink alias) and non-``.pdf`` output
    targets are rejected before any write.  The PDF is staged in a private
    directory next to the output, validated, and only then moved into place,
    so a failed render can never truncate the input or an existing PDF.  With
    ``keep_html``, the intermediate HTML is committed atomically *before*
    PDF rendering so a failed render still leaves a diagnosable HTML, while a
    previously delivered PDF stays untouched (issue #435).  Status writeback
    is opt-in and never mutates the input Markdown implicitly.
    """

    input_path = Path(input_path).resolve()
    if not input_path.is_file():
        return DeliveryResult(
            input_path=input_path,
            errors=[f"Input file not found: {input_path}"],
        )

    pdf_path = Path(output_path).resolve() if output_path else input_path.with_suffix(".pdf")

    if paths_collide(pdf_path, input_path):
        return DeliveryResult(
            input_path=input_path,
            pdf_path=pdf_path,
            errors=[
                "Refusing to overwrite input Markdown: "
                f"output path {pdf_path} resolves to the input file"
            ],
        )
    non_pdf = pdf_output_reason(pdf_path)
    if non_pdf:
        return DeliveryResult(input_path=input_path, pdf_path=pdf_path, errors=[non_pdf])

    final_html_path = pdf_path.with_suffix(".html") if keep_html else None
    if final_html_path is not None:
        if paths_collide(final_html_path, pdf_path):
            return DeliveryResult(
                input_path=input_path,
                pdf_path=pdf_path,
                errors=[
                    "Refusing keep_html: HTML intermediate path collides "
                    f"with the PDF path: {final_html_path}"
                ],
            )
        if paths_collide(final_html_path, input_path):
            return DeliveryResult(
                input_path=input_path,
                pdf_path=pdf_path,
                errors=[
                    "Refusing keep_html: HTML intermediate path collides "
                    f"with the input Markdown: {final_html_path}"
                ],
            )

    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    result = DeliveryResult(
        input_path=input_path,
        pdf_path=pdf_path,
        kept_html=keep_html,
    )

    with tempfile.TemporaryDirectory(
        prefix=f".{pdf_path.stem}-delivery-", dir=pdf_path.parent
    ) as temp_dir:
        staging = Path(temp_dir)
        html_work = staging / f"{input_path.stem}.html"
        pdf_work = staging / "output.pdf"
        try:
            from markdown_to_html import convert

            convert(input_path, html_work, title, warnings=result.warnings)
            _validate_non_empty_file(html_work, "HTML")
            result.markdown_status = DeliveryStatus.MD_READY
            if final_html_path is not None:
                os.replace(html_work, final_html_path)
                result.html_path = final_html_path
        except Exception as exc:
            result.errors.append(f"Markdown to HTML failed: {exc}")
            if write_status_to:
                try:
                    write_delivery_status(Path(write_status_to), result)
                except Exception as exc:
                    result.errors.append(f"Delivery status writeback failed: {exc}")
            return result

        html_for_pdf = final_html_path if final_html_path is not None else html_work
        try:
            _render_pdf(
                html_for_pdf,
                pdf_work,
                title=title,
                landscape=landscape,
                media=media,
                margin_top=margin_top,
                margin_right=margin_right,
                margin_bottom=margin_bottom,
                margin_left=margin_left,
                allow_remote=allow_remote,
            )
            result.pdf_size_bytes = _validate_pdf_artifact(pdf_work)
            os.replace(pdf_work, pdf_path)
            result.delivery_status = DeliveryStatus.PDF_READY
        except Exception as exc:
            result.delivery_status = DeliveryStatus.PDF_FAILED
            result.errors.append(f"HTML to PDF failed (Chromium/PDF renderer): {exc}")

    if write_status_to:
        try:
            write_delivery_status(Path(write_status_to), result)
        except Exception as exc:
            result.errors.append(f"Delivery status writeback failed: {exc}")
    return result
