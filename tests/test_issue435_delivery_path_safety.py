"""Issue #435 C1: path conflicts and atomic delivery must fail closed.

These tests pin the file-lifecycle contract: delivery must never overwrite
the input Markdown, hardlink aliases, reserved source/intermediate paths, or
a previously delivered PDF, and a crashed renderer must not leave a partial
artifact behind.
"""

from __future__ import annotations

import json
import os
import stat
import subprocess
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


@pytest.mark.parametrize(
    "name", ["target.md", "target.markdown", "target.html", "target.htm", "target.txt", "target.json", "target"]
)
def test_run_delivery_rejects_non_pdf_output_targets(tmp_path: Path, name: str) -> None:
    report = _write_report(tmp_path)
    output = tmp_path / name

    result = run_delivery(report, output)

    assert result.ok is False
    assert not output.exists()
    assert report.read_bytes() == ORIGINAL.encode()


def test_run_delivery_accepts_uppercase_pdf_suffix(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    report = _write_report(tmp_path)
    output = tmp_path / "target.PDF"

    def fake_renderer(html_path, pdf_path, **kwargs):
        Path(pdf_path).write_bytes(b"%PDF-1.7\nuppercase\n")

    monkeypatch.setattr("delivery.pipeline._render_pdf", fake_renderer)

    result = run_delivery(report, output)

    assert result.delivery_status is DeliveryStatus.PDF_READY
    assert output.read_bytes() == b"%PDF-1.7\nuppercase\n"


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


@pytest.mark.skipif(os.name != "posix", reason="POSIX permission semantics")
def test_atomic_html_write_preserves_existing_mode(tmp_path: Path) -> None:
    report = _write_report(tmp_path)
    target = tmp_path / "existing.html"
    target.write_text("old", encoding="utf-8")
    os.chmod(target, 0o640)

    convert(report, target)

    assert stat.S_IMODE(target.stat().st_mode) == 0o640


@pytest.mark.skipif(os.name != "posix", reason="POSIX permission semantics")
def test_atomic_html_write_uses_umask_default_for_new_files(tmp_path: Path) -> None:
    report = _write_report(tmp_path)
    target = tmp_path / "new.html"
    current_umask = os.umask(0)
    os.umask(current_umask)

    convert(report, target)

    assert stat.S_IMODE(target.stat().st_mode) == 0o666 & ~current_umask


@pytest.mark.skipif(os.name != "posix", reason="POSIX permission semantics")
def test_keep_html_commit_preserves_existing_html_mode(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    report = _write_report(tmp_path)
    pdf = tmp_path / "out.pdf"
    html = tmp_path / "out.html"
    html.write_text("old html", encoding="utf-8")
    os.chmod(html, 0o640)

    def fake_renderer(html_path, pdf_path, **kwargs):
        Path(pdf_path).write_bytes(b"%PDF-1.7\nok\n")

    monkeypatch.setattr("delivery.pipeline._render_pdf", fake_renderer)

    result = run_delivery(report, pdf, keep_html=True)

    assert result.delivery_status is DeliveryStatus.PDF_READY
    assert stat.S_IMODE(html.stat().st_mode) == 0o640


@pytest.mark.skipif(os.name != "posix", reason="POSIX permission semantics")
def test_pdf_commit_preserves_existing_pdf_mode(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    report = _write_report(tmp_path)
    pdf = tmp_path / "out.pdf"
    pdf.write_bytes(b"%PDF-1.7\nold\n")
    os.chmod(pdf, 0o600)

    def fake_renderer(html_path, pdf_path, **kwargs):
        Path(pdf_path).write_bytes(b"%PDF-1.7\nnew\n")

    monkeypatch.setattr("delivery.pipeline._render_pdf", fake_renderer)

    result = run_delivery(report, pdf)

    assert result.delivery_status is DeliveryStatus.PDF_READY
    assert stat.S_IMODE(pdf.stat().st_mode) == 0o600


def test_atomic_html_write_does_not_mutate_process_umask(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    report = _write_report(tmp_path)
    target = tmp_path / "out.html"
    umask_calls: list[int] = []
    real_umask = os.umask

    def spy(mask: int) -> int:
        umask_calls.append(mask)
        return real_umask(mask)

    monkeypatch.setattr(os, "umask", spy)

    convert(report, target)

    assert umask_calls == []
    assert target.is_file()


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


def test_delivery_keeps_metadata_columns_and_emits_no_fold_warning(
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
        Path(pdf_path).write_bytes(b"%PDF-1.7\nkept delivery\n")

    monkeypatch.setattr("delivery.pipeline._render_pdf", fake_renderer)

    result = run_delivery(report, pdf, keep_html=True)

    assert result.delivery_status is DeliveryStatus.PDF_READY
    assert not any("folded" in warning for warning in result.warnings)
    assert result.html_path is not None
    html_text = result.html_path.read_text(encoding="utf-8")
    assert "<th>Source</th>" in html_text
    assert "example.com" in html_text


def test_write_status_rejects_input_collision(tmp_path: Path) -> None:
    report = _write_report(tmp_path)

    result = run_delivery(report, tmp_path / "out.pdf", write_status_to=report)

    assert result.ok is False
    assert report.read_bytes() == ORIGINAL.encode()
    assert any("status" in error.lower() for error in result.errors)


def test_write_status_rejects_hardlink_alias(tmp_path: Path) -> None:
    report = _write_report(tmp_path)
    alias = tmp_path / "alias.md"
    os.link(report, alias)

    result = run_delivery(report, tmp_path / "out.pdf", write_status_to=alias)

    assert result.ok is False
    assert alias.read_bytes() == ORIGINAL.encode()
    assert report.read_bytes() == ORIGINAL.encode()


def test_write_status_rejects_pdf_collision(tmp_path: Path) -> None:
    report = _write_report(tmp_path)
    pdf = tmp_path / "out.pdf"

    result = run_delivery(report, pdf, write_status_to=pdf)

    assert result.ok is False
    assert not pdf.exists()


def test_write_status_rejects_kept_html_collision(tmp_path: Path) -> None:
    report = _write_report(tmp_path)
    html = tmp_path / "out.html"

    result = run_delivery(
        report,
        tmp_path / "out.pdf",
        keep_html=True,
        write_status_to=html,
    )

    assert result.ok is False
    assert not html.exists()


def test_output_dir_preparation_failure_returns_structured_result(tmp_path: Path) -> None:
    report = _write_report(tmp_path)
    blocker = tmp_path / "blocker"
    blocker.write_text("not a directory", encoding="utf-8")

    result = run_delivery(report, blocker / "out.pdf")

    assert result.ok is False
    assert result.delivery_status is DeliveryStatus.NOT_RUN
    assert any("output directory" in error.lower() for error in result.errors)


@pytest.mark.skipif(
    os.name != "posix" or os.geteuid() == 0,
    reason="POSIX permission semantics, non-root only",
)
def test_unwritable_output_dir_returns_structured_result(tmp_path: Path) -> None:
    report = _write_report(tmp_path)
    readonly = tmp_path / "readonly"
    readonly.mkdir()
    os.chmod(readonly, 0o500)
    try:
        result = run_delivery(report, readonly / "out.pdf")
    finally:
        os.chmod(readonly, 0o700)

    assert result.ok is False
    assert any("output directory" in error.lower() for error in result.errors)


def test_cli_json_survives_output_dir_failure(tmp_path: Path) -> None:
    report = _write_report(tmp_path)
    blocker = tmp_path / "blocker"
    blocker.write_text("not a directory", encoding="utf-8")

    completed = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "md_to_pdf.py"),
            str(report),
            str(blocker / "out.pdf"),
            "--json",
        ],
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 1, completed.stdout + completed.stderr
    payload = json.loads(completed.stdout)
    assert payload["delivery_status"] == "not_run"
    assert any("output directory" in error.lower() for error in payload["errors"])


def test_kept_html_reflects_actual_commit(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    report = _write_report(tmp_path)

    def failing_convert(*args, **kwargs):
        raise RuntimeError("simulated markdown failure")

    monkeypatch.setattr("markdown_to_html.convert", failing_convert)

    result = run_delivery(report, tmp_path / "out.pdf", keep_html=True)

    assert result.kept_html is False
    assert result.html_path is None


def test_delivery_keeps_data_wider_than_header_in_kept_html(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    report = tmp_path / "report.md"
    report.write_text(
        "# Report\n\n| A | B |\n|---|---|\n| 1 | 2 | 3 |\n",
        encoding="utf-8",
    )
    pdf = tmp_path / "out.pdf"

    def fake_renderer(html_path, pdf_path, **kwargs):
        Path(pdf_path).write_bytes(b"%PDF-1.7\nwide row\n")

    monkeypatch.setattr("delivery.pipeline._render_pdf", fake_renderer)

    result = run_delivery(report, pdf, keep_html=True)

    assert result.delivery_status is DeliveryStatus.PDF_READY
    assert result.kept_html is True
    assert result.html_path is not None
    assert "<td>3</td>" in result.html_path.read_text(encoding="utf-8")


def test_keep_html_failure_updates_html_but_preserves_previous_pdf(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    report = _write_report(tmp_path)
    pdf = tmp_path / "out.pdf"
    pdf.write_bytes(b"%PDF-1.7\nprevious pdf\n")
    html = tmp_path / "out.html"
    html.write_text("previous html", encoding="utf-8")

    def partial_renderer(html_path, pdf_path, **kwargs):
        Path(pdf_path).write_bytes(b"%PDF-1.7\npartial")
        raise RuntimeError("simulated crash after partial write")

    monkeypatch.setattr("delivery.pipeline._render_pdf", partial_renderer)

    result = run_delivery(report, pdf, keep_html=True)

    assert result.delivery_status is DeliveryStatus.PDF_FAILED
    assert pdf.read_bytes() == b"%PDF-1.7\nprevious pdf\n"
    assert html.read_text(encoding="utf-8").lstrip().startswith("<!DOCTYPE")


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
