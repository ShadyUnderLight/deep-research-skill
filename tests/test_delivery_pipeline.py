"""Unit tests for the modular Markdown/PDF delivery contract."""

from __future__ import annotations

import sys
import json
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from delivery.models import DeliveryResult, DeliveryStatus  # noqa: E402
from delivery.normalization import normalize_text_for_pdf  # noqa: E402
from delivery.pipeline import run_delivery  # noqa: E402
from delivery.status import write_delivery_status  # noqa: E402
from delivery.tables import maybe_wrap_wide_tables_in_html  # noqa: E402
from audit_report import _verdict_to_json, audit_report  # noqa: E402
from check_pdf_regression import _safe_artifact_stem  # noqa: E402
from markdown_to_html import process_markdown  # noqa: E402


def test_normalization_and_table_renderer_are_independent() -> None:
    normalized = normalize_text_for_pdf("## 标题\n\n中 文。")
    assert normalized == "## 标题\n\n中文。"

    body = process_markdown(
        "# 标题\n\n"
        "| A | B | C | D | E |\n"
        "|---|---|---|---|---|\n"
        "| 1 | 2 | 3 | 4 | 5 |"
    )
    assert body.count("<table>") == 2
    assert "<script" not in body


def test_table_layout_keeps_remote_url_text_safe() -> None:
    html = (
        "<table><thead><tr><th>Name</th><th>Source</th><th>Notes</th><th>Type</th></tr></thead>"
        "<tbody><tr><td>A</td><td>https://example.com/a?x=1</td><td>ok</td><td>source</td></tr></tbody></table>"
    )
    rendered = maybe_wrap_wide_tables_in_html(html)
    assert "table-wrap" in rendered
    assert "javascript:" not in rendered


def test_special_fixture_artifact_alias_is_upload_safe() -> None:
    safe = _safe_artifact_stem("input#frag?query 中文")
    assert safe == "input-frag-query"
    assert not any(character in safe for character in '"\':<>|*?\r\n')


def test_pdf_failure_keeps_markdown_ready_and_cleans_intermediate_html(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    input_path = tmp_path / "report.md"
    input_path.write_text("# Report\n\nBody.\n", encoding="utf-8")

    def fail_pdf(*args, **kwargs):
        raise RuntimeError("simulated Chromium failure")

    monkeypatch.setattr("delivery.pipeline._render_pdf", fail_pdf)
    result = run_delivery(input_path, tmp_path / "out.pdf")

    assert result.markdown_status is DeliveryStatus.MD_READY
    assert result.delivery_status is DeliveryStatus.PDF_FAILED
    assert any("simulated Chromium failure" in error for error in result.errors)
    assert not (tmp_path / "report.html").exists()


def test_missing_pdf_artifact_cannot_claim_ready(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    input_path = tmp_path / "report.md"
    input_path.write_text("# Report\n\nBody.\n", encoding="utf-8")
    monkeypatch.setattr("delivery.pipeline._render_pdf", lambda *args, **kwargs: None)

    result = run_delivery(input_path, tmp_path / "out.pdf")

    assert result.ok is False
    assert result.delivery_status is DeliveryStatus.PDF_FAILED
    assert result.pdf_size_bytes is None
    assert any("without creating" in error for error in result.errors)


def test_keep_html_is_explicit_and_status_writeback_is_explicit(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    input_path = tmp_path / "report.md"
    input_path.write_text("# Report\n\nBody.\n", encoding="utf-8")
    status_path = tmp_path / "pack.md"
    status_path.write_text(
        "## Artifact contract\n\nvalid\n\n## Delivery status\nmd_ready\n\n## Required audits\n\n- final-audit — passed\n",
        encoding="utf-8",
    )

    def fake_pdf(html_path, pdf_path, **kwargs):
        Path(pdf_path).write_bytes(b"%PDF-1.7\n")

    monkeypatch.setattr("delivery.pipeline._render_pdf", fake_pdf)
    result = run_delivery(
        input_path,
        tmp_path / "out.pdf",
        keep_html=True,
        write_status_to=status_path,
    )

    assert result.delivery_status is DeliveryStatus.PDF_READY
    assert result.markdown_status is DeliveryStatus.MD_READY
    assert result.html_path == tmp_path / "out.html"
    assert result.html_path.is_file()
    assert "## Delivery status\n\npdf_ready" in status_path.read_text(encoding="utf-8")
    assert "markdown_status: md_ready" in status_path.read_text(encoding="utf-8")


def test_status_writer_adds_missing_section_without_duplicate(tmp_path: Path) -> None:
    path = tmp_path / "pack.md"
    path.write_text("## Required audits\n\n- final-audit — passed\n", encoding="utf-8")
    result = DeliveryResult(
        input_path=path,
        delivery_status=DeliveryStatus.PDF_FAILED,
        markdown_status=DeliveryStatus.MD_READY,
        errors=["Chromium unavailable"],
    )

    write_delivery_status(path, result)
    text = path.read_text(encoding="utf-8")
    assert text.count("## Delivery status") == 1
    assert "pdf_failed" in text
    assert "Chromium unavailable" in text


def test_audit_runner_consumes_delivery_result_without_merging_status_layers(
    tmp_path: Path,
) -> None:
    report = ROOT / "tests" / "fixtures" / "audit" / "market-outlook-pos.md"
    delivery_result = tmp_path / "delivery.json"
    delivery_result.write_text(
        json.dumps(
            {
                "input_path": str(report.resolve()),
                "delivery_status": "pdf_failed",
                "markdown_status": "md_ready",
                "pdf_path": str(tmp_path / "missing.pdf"),
                "errors": ["Chromium unavailable"],
            }
        ),
        encoding="utf-8",
    )

    verdict = audit_report(report, route="market-outlook", delivery_result=delivery_result)
    payload = json.loads(_verdict_to_json(verdict))
    assert payload["delivery"]["delivery_status"] == "pdf_failed"
    assert payload["delivery"]["markdown_status"] == "md_ready"
    assert verdict.delivery == payload["delivery"]


def test_audit_accepts_provenance_bound_pdf_ready_result(tmp_path: Path) -> None:
    report = ROOT / "tests" / "fixtures" / "audit" / "market-outlook-pos.md"
    pdf_path = tmp_path / "report.pdf"
    pdf_path.write_bytes(b"%PDF-1.7\nvalid test artifact\n")
    delivery_result = tmp_path / "delivery.json"
    delivery_result.write_text(
        json.dumps(
            {
                "input_path": str(report.resolve()),
                "delivery_status": "pdf_ready",
                "markdown_status": "md_ready",
                "pdf_path": str(pdf_path.resolve()),
                "pdf_size_bytes": pdf_path.stat().st_size,
            }
        ),
        encoding="utf-8",
    )

    verdict = audit_report(report, route="market-outlook", delivery_result=delivery_result)
    assert verdict.exit_code in (0, 1)
    assert verdict.delivery["delivery_status"] == "pdf_ready"


def test_audit_rejects_forged_delivery_provenance(tmp_path: Path) -> None:
    report = ROOT / "tests" / "fixtures" / "audit" / "market-outlook-pos.md"
    delivery_result = tmp_path / "forged.json"
    delivery_result.write_text(
        json.dumps(
            {
                "input_path": str((tmp_path / "wrong.md").resolve()),
                "delivery_status": "pdf_ready",
                "markdown_status": "md_ready",
                "pdf_path": str((tmp_path / "missing.pdf").resolve()),
                "pdf_size_bytes": 1,
            }
        ),
        encoding="utf-8",
    )

    verdict = audit_report(report, route="market-outlook", delivery_result=delivery_result)
    assert verdict.exit_code == 2
    assert verdict.overall == "fail"
    assert any("input_path" in error for error in verdict.blocking)


def test_audit_cli_accepts_delivery_result_json(tmp_path: Path) -> None:
    report = ROOT / "tests" / "fixtures" / "audit" / "market-outlook-pos.md"
    delivery_result = tmp_path / "delivery.json"
    delivery_result.write_text(
        json.dumps({
            "input_path": str(report.resolve()),
            "delivery_status": "pdf_failed",
            "markdown_status": "md_ready",
            "errors": ["boom"],
        }),
        encoding="utf-8",
    )
    completed = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "audit_report.py"),
            str(report),
            "--route",
            "market-outlook",
            "--delivery-result",
            str(delivery_result),
            "--json",
        ],
        capture_output=True,
        text=True,
    )
    assert completed.returncode in (0, 1), completed.stdout + completed.stderr
    payload = json.loads(completed.stdout)
    assert payload["delivery"]["delivery_status"] == "pdf_failed"
