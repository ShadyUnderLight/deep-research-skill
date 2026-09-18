"""Issue #435 C1: path conflicts and atomic delivery must fail closed.

These tests pin the file-lifecycle contract: delivery must never overwrite
the input Markdown, hardlink aliases, reserved source/intermediate paths, or
a previously delivered PDF, and a crashed renderer must not leave a partial
artifact behind.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from delivery.models import DeliveryStatus  # noqa: E402
from delivery.pipeline import run_delivery  # noqa: E402
from markdown_to_html import convert  # noqa: E402


ORIGINAL = "# Report\n\nBody.\n"


def _write_report(tmp_path: Path) -> Path:
    report = tmp_path / "report.md"
    report.write_text(ORIGINAL, encoding="utf-8")
    return report


def test_run_delivery_rejects_identical_input_and_output(tmp_path: Path) -> None:
    report = _write_report(tmp_path)

    result = run_delivery(report, report)

    assert result.ok is False
    assert result.delivery_status is DeliveryStatus.NOT_RUN
    assert report.read_bytes() == ORIGINAL.encode()
    assert any("overwrite" in error.lower() or "collides" in error.lower() for error in result.errors)


def test_run_delivery_rejects_hardlink_alias_output(tmp_path: Path) -> None:
    report = _write_report(tmp_path)
    alias = tmp_path / "alias.pdf"
    os.link(report, alias)

    result = run_delivery(report, alias)

    assert result.ok is False
    assert alias.read_bytes() == ORIGINAL.encode()
    assert report.read_bytes() == ORIGINAL.encode()


@pytest.mark.parametrize("suffix", [".md", ".markdown", ".html", ".htm"])
def test_run_delivery_rejects_reserved_output_suffixes(tmp_path: Path, suffix: str) -> None:
    report = _write_report(tmp_path)
    output = tmp_path / f"target{suffix}"

    result = run_delivery(report, output)

    assert result.ok is False
    assert not output.exists()
    assert report.read_bytes() == ORIGINAL.encode()


def test_keep_html_rejects_intermediate_collision(tmp_path: Path) -> None:
    report = _write_report(tmp_path)
    output = tmp_path / "target.html"

    result = run_delivery(report, output, keep_html=True)

    assert result.ok is False
    assert not output.exists()
    assert report.read_bytes() == ORIGINAL.encode()


def test_convert_rejects_identical_paths(tmp_path: Path) -> None:
    report = _write_report(tmp_path)

    with pytest.raises(ValueError):
        convert(report, report)

    assert report.read_bytes() == ORIGINAL.encode()


def test_partial_pdf_failure_preserves_existing_artifact(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    report = _write_report(tmp_path)
    pdf = tmp_path / "out.pdf"
    pdf.write_bytes(b"%PDF-1.7\noriginal delivery\n")

    def partial_renderer(html_path, pdf_path, **kwargs):
        Path(pdf_path).write_bytes(b"%PDF-1.7\npartial")
        raise RuntimeError("simulated crash after partial write")

    monkeypatch.setattr("delivery.pipeline._render_pdf", partial_renderer)

    result = run_delivery(report, pdf)

    assert result.delivery_status is DeliveryStatus.PDF_FAILED
    assert pdf.read_bytes() == b"%PDF-1.7\noriginal delivery\n"


def test_failed_first_delivery_leaves_no_pdf(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    report = _write_report(tmp_path)
    pdf = tmp_path / "out.pdf"

    def partial_renderer(html_path, pdf_path, **kwargs):
        Path(pdf_path).write_bytes(b"%PDF-1.7\npartial")
        raise RuntimeError("simulated crash after partial write")

    monkeypatch.setattr("delivery.pipeline._render_pdf", partial_renderer)

    result = run_delivery(report, pdf)

    assert result.delivery_status is DeliveryStatus.PDF_FAILED
    assert not pdf.exists()


def test_delivery_result_surfaces_table_fold_warnings(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    report = tmp_path / "report.md"
    report.write_text(
        "# Report\n\n"
        "| Name | Source | Notes | Type |\n"
        "|---|---|---|---|\n"
        "| A | https://example.com/a | ok | source |\n",
        encoding="utf-8",
    )
    pdf = tmp_path / "out.pdf"

    def fake_renderer(html_path, pdf_path, **kwargs):
        Path(pdf_path).write_bytes(b"%PDF-1.7\nwarned delivery\n")

    monkeypatch.setattr("delivery.pipeline._render_pdf", fake_renderer)

    result = run_delivery(report, pdf)

    assert result.delivery_status is DeliveryStatus.PDF_READY
    assert any("Source" in warning for warning in result.warnings)
    assert "warnings" in result.to_json()


def test_renderer_receives_staged_paths_and_commits_atomically(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    report = _write_report(tmp_path)
    pdf = tmp_path / "out.pdf"
    captured: dict[str, Path] = {}

    def fake_renderer(html_path, pdf_path, **kwargs):
        captured["html"] = Path(html_path)
        captured["pdf"] = Path(pdf_path)
        Path(pdf_path).write_bytes(b"%PDF-1.7\nnew delivery\n")

    monkeypatch.setattr("delivery.pipeline._render_pdf", fake_renderer)

    result = run_delivery(report, pdf, keep_html=True)

    assert result.delivery_status is DeliveryStatus.PDF_READY
    assert result.html_path == tmp_path / "out.html"
    assert result.html_path.is_file()
    assert captured["pdf"] != pdf.resolve()
    assert captured["pdf"].parent.parent == tmp_path
    assert captured["html"] == tmp_path / "out.html"
    assert pdf.read_bytes() == b"%PDF-1.7\nnew delivery\n"
    leftovers = [
        entry.name
        for entry in tmp_path.iterdir()
        if entry.name.startswith(".") and "delivery" in entry.name
    ]
    assert leftovers == []
