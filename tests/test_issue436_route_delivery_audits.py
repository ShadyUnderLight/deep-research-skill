"""Issue #436: route-specific delivery audits must actually execute.

Covers the "rules exist but are not run" gaps:

D1 — the listed-company validator must trust the orchestrator-resolved
     canonical ``listed-company`` id instead of re-guessing from display text;
D2 — research-anchor / market-snapshot time-layers are counted only inside
     their own sections, not from keywords scattered elsewhere;
D3 — monitoring signal cells that hold a placeholder (TBD / N/A / 待补充) do
     not count as fully-defined;
D4 — external citation hygiene (turnNviewN / sandbox: / file-... temp IDs) is
     a global delivery-scope audit that blocks visible internal references.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import validate_listed_company_delivery as vlc  # noqa: E402
import audit_report  # noqa: E402
from validate_external_citation_hygiene import (  # noqa: E402
    check_external_citation_hygiene,
    strip_fenced_code_blocks,
)

VLC_SCRIPT = str(SCRIPTS / "validate_listed_company_delivery.py")


# ── Fixtures ──────────────────────────────────────────────────────────────────


def _route_block(primary: str) -> str:
    return (
        "## Route and audit status\n\n"
        f"**Primary route**: {primary}\n\n"
        "| Audit | Status | 证据 |\n"
        "|-------|--------|------|\n"
        "| source-traceability | ✅ Passed | 正文使用 [S01] |\n"
        "| final-audit | ✅ Passed | §2 可追溯 |\n"
    )


def _anchor_block() -> str:
    return (
        "## 研究锚定块\n\n"
        "- **最新完整财年**: FY2025 (2025-12-31)\n"
        "- **最新季度**: 2026Q1 (2026-03-31)\n"
        "- **快照日期**: 2026-06-01\n"
    )


def _snapshot_table() -> str:
    return (
        "## 市场快照\n\n"
        "| 指标 | 数值 | 数据来源 |\n"
        "|------|------|----------|\n"
        "| 当前股价 | $185.50 | NYSE |\n"
        "| 市值 | $960B | NYSE |\n"
        "| PE (TTM) | 28.5x | filings |\n"
        "| PE (Forward) | 22.1x | consensus |\n"
        "| PB | 7.2x | filings |\n"
        "| PS | 10.8x | filings |\n"
        "| 52周区间 | $120-$210 | NYSE |\n"
        "| 股息率 | 1.5% | filings |\n"
    )


def _source_register() -> str:
    return (
        "## Source Register\n\n"
        "| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |\n"
        "|----|-------------|-------------|------|---------|-------------|------------------|\n"
        "| S01 | TSMC AR | primary | 2026-03-31 | https://example.com | high | §3 |\n"
    )


def _write(tmp: Path, text: str) -> Path:
    p = tmp / "report.md"
    p.write_text(text, encoding="utf-8")
    return p


# ── D1: canonical route injection ────────────────────────────────────────────


def test_canonical_route_id_runs_listed_company_checks(tmp_path: Path) -> None:
    """route_id='listed-company' must run the anchor check (issue #436 D1).

    The report declares the canonical kebab id and has NO anchor block, so the
    validator must report the missing anchor (a hard error) instead of silently
    returning no errors.
    """
    report = (
        "# TSMC\n\n"
        + _route_block("listed-company")
        + "\n"
        + _snapshot_table()
        + "\n## 投资判断\n\nGrowth intact [S01].\n\n"
        + _source_register()
    )
    errors, warnings = vlc.validate_file(_write(tmp_path, report), route_id="listed-company")
    assert errors, "canonical listed-company route must run anchor checks"
    assert any("research-anchor" in e or "anchor" in e for e in errors)


def test_display_name_route_id_runs_checks(tmp_path: Path) -> None:
    """The display form still runs the checks when resolved to canonical."""
    report = (
        "# TSMC\n\n"
        + _route_block("listed-company")  # no anchor block
        + "\n## 投资判断\n\nGrowth intact [S01].\n\n"
        + _source_register()
    )
    errors, _ = vlc.validate_file(_write(tmp_path, report), route_id="listed-company")
    assert errors


def test_non_listed_route_id_skips(tmp_path: Path) -> None:
    """A non-listed route_id must skip all listed-company checks."""
    report = "# TSMC\n\n## Body\n\nNo real content.\n"
    errors, warnings = vlc.validate_file(
        _write(tmp_path, report), route_id="market-outlook"
    )
    assert errors == []
    assert warnings == []


def test_legacy_display_fallback_still_detects(tmp_path: Path) -> None:
    """Without route_id, the legacy display-text adapter still detects the route."""
    report = (
        "# TSMC\n\n"
        + _route_block("Listed Company / Investment-style Research")
        + "\n## 投资判断\n\nGrowth intact [S01].\n\n"
        + _source_register()
    )
    errors, _ = vlc.validate_file(_write(tmp_path, report), route_id=None)
    # no anchor block -> legacy adapter must still trigger the anchor error
    assert errors and any("anchor" in e for e in errors)


def test_cli_canonical_route_runs_checks(tmp_path: Path) -> None:
    """Standalone CLI must resolve the canonical 'listed-company' declaration."""
    report = (
        "# TSMC\n\n"
        + _route_block("listed-company")
        + "\n## 投资判断\n\nGrowth intact [S01].\n\n"
        + _source_register()
    )
    p = _write(tmp_path, report)
    proc = subprocess.run(
        [sys.executable, VLC_SCRIPT, str(p)], capture_output=True, text=True
    )
    assert proc.returncode == 2, proc.stdout


# ── D2: anchor / snapshot block boundaries ───────────────────────────────────


def test_anchor_keywords_in_other_section_do_not_count(tmp_path: Path) -> None:
    """FY/quarter keywords outside the anchor block must not satisfy the gate."""
    report = (
        "# TSMC\n\n"
        + _route_block("listed-company")
        + "\n## 投资判断\n\n"
        "The latest full year FY2025 and 2026Q1 were strong; snapshot date 2026-06-01. [S01]\n\n"
        + _source_register()
    )
    errors, _ = vlc.validate_file(_write(tmp_path, report), route_id="listed-company")
    assert any("no research-anchor block" in e for e in errors), errors


def test_missing_snapshot_section_reported(tmp_path: Path) -> None:
    """A missing market-snapshot section is reported, not papered over."""
    report = (
        "# TSMC\n\n"
        + _route_block("listed-company")
        + "\n"
        + _anchor_block()
        + "\n## 投资判断\n\nGrowth intact [S01].\n\n"
        + _source_register()
    )
    errors, warnings = vlc.validate_file(_write(tmp_path, report), route_id="listed-company")
    combined = errors + warnings
    assert any("market-snapshot" in w for w in combined), combined


# ── D3: monitoring placeholders ────────────────────────────────────────────


def _monitoring_report(rows: list[str]) -> str:
    table = (
        "| Signal | Threshold | Cadence | Source | Trigger-to-action |\n"
        "|---|---|---|---|---|\n"
        + "\n".join(rows)
        + "\n"
    )
    return "# Outlook\n\n## Monitoring\n\n" + table + "\n" + _source_register()


def test_monitoring_placeholders_not_counted(tmp_path: Path) -> None:
    """Three fully placeholder rows must NOT reach the 3-signal gate."""
    rows = [
        "| Margin | TBD | weekly | S01 | cut production |",
        "| Demand | N/A | N/A | S02 | observe |",
        "| Competition | 待补充 | 待填写 | 待补充 | 观察 |",
    ]
    p = _write(tmp_path, _monitoring_report(rows))
    result = audit_report._run_market_outlook_monitoring_actionability(p, strict=True)
    assert result.errors, "three placeholder rows must fail the actionability gate"


def test_monitoring_valid_rows_pass(tmp_path: Path) -> None:
    """Three actionable rows with concrete values must pass."""
    rows = [
        "| Margin | below 30% | weekly | S01 | cut production |",
        "| Demand growth | below 5% | monthly | S02 | reduce headcount |",
        "| PE ratio | above 40x | quarterly | S03 | take profit |",
    ]
    p = _write(tmp_path, _monitoring_report(rows))
    result = audit_report._run_market_outlook_monitoring_actionability(p, strict=True)
    assert not result.errors, result.errors


# ── D4: external citation hygiene as a delivery audit ────────────────────────


def test_external_citation_visible_turn_ref_blocks() -> None:
    text = "The claim was sourced from turn43view0 in the research session."
    assert check_external_citation_hygiene(strip_fenced_code_blocks(text))


def test_external_citation_sandbox_path_blocks() -> None:
    text = "See sandbox:/Users/gpt/work/report for the raw table."
    assert check_external_citation_hygiene(strip_fenced_code_blocks(text))


def test_external_citation_fenced_code_not_flagged() -> None:
    """A turn-ref inside a fenced code block must not pollute the gate."""
    text = (
        "# Report\n\n"
        "Here is a code example:\n\n"
        "```\n"
        "use turn43view0 to render citations\n"
        "```\n"
    )
    assert check_external_citation_hygiene(strip_fenced_code_blocks(text)) == []


def test_external_citation_runner_blocks_visible_ref(tmp_path: Path) -> None:
    report = "# Report\n\nVisible claim citing turn43view0 [S01].\n\n" + _source_register()
    result = audit_report._run_external_citation_hygiene(_write(tmp_path, report))
    assert result.errors, "visible internal citation must be a delivery error"


def test_external_citation_runner_clean_report(tmp_path: Path) -> None:
    report = "# Report\n\nClean body with no internal session refs.\n\n" + _source_register()
    result = audit_report._run_external_citation_hygiene(_write(tmp_path, report))
    assert not result.errors, result.errors


def test_external_citation_is_global_delivery_audit() -> None:
    """The new audit is wired as a global delivery-scope automated audit."""
    audits = audit_report._AUDIT_REGISTRY.global_audit_ids()
    assert "external-citation-hygiene" in audits
    audit = audit_report._AUDIT_REGISTRY.get_audit("external-citation-hygiene")
    assert audit.scope == "delivery"
    assert audit.execution_type == "automated"
    assert audit.validator_binding == "external-citation-hygiene"
    assert "external-citation-hygiene" in audit_report._AUDIT_VALIDATOR_REGISTRY
