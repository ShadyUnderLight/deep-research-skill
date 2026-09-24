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



# ── Review round 1: anchor single-line form / vague monitoring / CLI fail-closed ──


def test_single_line_anchor_form_passes(tmp_path: Path) -> None:
    """The template's heading-less single-line anchor must satisfy the gate.

    The report template (references/templates/listed-company-report.md) allows a
    one-line form: 研究锚定：最新FY：FY2025｜最新季度：2026Q1｜市场快照：…
    The checker must not demand a '## 研究锚定块' heading (review P1).
    """
    report = (
        "# TSMC\n\n"
        + _route_block("listed-company")
        + "\n\n研究锚定：最新FY：FY2025｜最新季度：2026Q1｜市场快照：2026-05-29\n\n"
        + _snapshot_table()
        + "\n## 投资判断\n\nGrowth intact [S01].\n\n"
        + _source_register()
    )
    errors, _ = vlc.validate_file(_write(tmp_path, report), route_id="listed-company")
    assert not any("anchor" in e for e in errors), errors


def test_vague_monitoring_values_not_counted(tmp_path: Path) -> None:
    """Meaningless non-empty cells must not count (review P1).

    threshold=foo / cadence=later / source=maybe / action=observe are non-empty
    but carry no executable info; three such rows must fail the gate.
    """
    rows = [
        "| Margin | foo | later | maybe | observe |",
        "| Demand | bar | soon | perhaps | watch |",
        "| PE | test | later | unknown | monitor |",
    ]
    p = _write(tmp_path, _monitoring_report(rows))
    result = audit_report._run_market_outlook_monitoring_actionability(p, strict=True)
    assert result.errors, "vague monitoring values must not reach the signal gate"


def test_cli_missing_route_declaration_fails(tmp_path: Path) -> None:
    """No declared primary route is a blocking failure, not a silent pass (P2)."""
    report = "# TSMC\n\n## 投资判断\n\nGrowth intact [S01].\n\n" + _source_register()
    proc = subprocess.run(
        [sys.executable, VLC_SCRIPT, str(_write(tmp_path, report))],
        capture_output=True, text=True,
    )
    assert proc.returncode == 2, proc.stdout
    assert "route" in proc.stdout.lower(), proc.stdout


def test_cli_unknown_route_declaration_fails(tmp_path: Path) -> None:
    """An unresolvable declared route is a blocking failure, not a silent pass."""
    report = (
        "# TSMC\n\n"
        + _route_block("Totally Bogus Route Name")
        + "\n## 投资判断\n\nGrowth intact [S01].\n\n"
        + _source_register()
    )
    proc = subprocess.run(
        [sys.executable, VLC_SCRIPT, str(_write(tmp_path, report))],
        capture_output=True, text=True,
    )
    assert proc.returncode == 2, proc.stdout
    assert "route" in proc.stdout.lower(), proc.stdout



# ── Review round 2: snapshot hard-fail / bare-operator threshold / placeholder anchor ──


def test_market_snapshot_missing_is_error(tmp_path: Path) -> None:
    """No market-snapshot section must be a blocking error, not conditional-pass."""
    report = (
        "# TSMC\n\n"
        + _route_block("listed-company")
        + "\n"
        + _anchor_block()
        + "\n## 投资判断\n\nGrowth intact [S01].\n\n"
        + _source_register()
    )
    errors, warnings = vlc.validate_file(_write(tmp_path, report), route_id="listed-company")
    assert any("market-snapshot" in e for e in errors), (errors, warnings)


def test_bare_comparison_threshold_not_counted(tmp_path: Path) -> None:
    """A bare '≥' with no number is not a judgeable threshold."""
    rows = [
        "| Margin | ≥ | weekly | S01 | cut production |",
        "| Demand | > | monthly | S02 | reduce headcount |",
        "| PE | ~ | quarterly | S03 | take profit |",
    ]
    p = _write(tmp_path, _monitoring_report(rows))
    result = audit_report._run_market_outlook_monitoring_actionability(p, strict=True)
    assert result.errors, "bare comparison operators must not count as thresholds"


def test_vague_cadence_phrase_not_counted(tmp_path: Path) -> None:
    """'later this year' / 'soon' cadence phrases are not real frequencies."""
    rows = [
        "| Margin | below 30% | later this year | S01 | cut production |",
        "| Demand | below 5% | soon | S02 | reduce headcount |",
        "| PE | above 40x | asap | S03 | take profit |",
    ]
    p = _write(tmp_path, _monitoring_report(rows))
    result = audit_report._run_market_outlook_monitoring_actionability(p, strict=True)
    assert result.errors, "vague cadence phrases must not count"


def test_placeholder_anchor_snapshot_label_not_a_layer(tmp_path: Path) -> None:
    """'市场快照：待补充' must not count as a locked snapshot time layer."""
    anchor = "研究锚定：最新FY：FY2025｜市场快照：待补充\n"
    report = (
        "# TSMC\n\n"
        + _route_block("listed-company")
        + "\n\n" + anchor + "\n"
        + _snapshot_table()
        + "\n## 投资判断\n\nGrowth intact [S01].\n\n"
        + _source_register()
    )
    errors, _ = vlc.validate_file(_write(tmp_path, report), route_id="listed-company")
    assert any("anchor" in e for e in errors), (
        "FY + placeholder snapshot only locks 1/3 layers; must fail", errors
    )



# ── Review round 3: snapshot placeholder values / multi-word fillers / quarter value / cadence positive ──


def test_snapshot_table_labels_with_placeholder_values_fail(tmp_path: Path) -> None:
    """All 8 labels present but template placeholder values must not pass."""
    snapshot = (
        "## 市场快照\n\n"
        "| 指标 | 值 | 来源 |\n|------|-----|------|\n"
        "| 当前股价 | $__ | [数据源](URL) |\n"
        "| 快照日期 | YYYY-MM-DD | — |\n"
        "| 市值 | $__ | [数据源](URL) |\n"
        "| PE (TTM) | __x | [数据源](URL) |\n"
        "| PE (Forward) | __x | [数据源](URL) |\n"
        "| PB | __x | [数据源](URL) |\n"
        "| PS | __x | [数据源](URL) |\n"
        "| 52周区间 | $__ - $__ | [数据源](URL) |\n"
        "| 股息率 | __% | [数据源](URL) |\n"
    )
    report = (
        "# TSMC\n\n" + _route_block("listed-company") + "\n" + _anchor_block()
        + "\n" + snapshot + "\n## 投资判断\n\nGrowth intact [S01].\n\n"
        + _source_register()
    )
    errors, _ = vlc.validate_file(_write(tmp_path, report), route_id="listed-company")
    assert any("market snapshot" in e or "market-snapshot" in e for e in errors), errors


def test_multiword_placeholder_phrases_not_counted(tmp_path: Path) -> None:
    """'TBD Q3' / 'maybe EIA report' / 'observe weekly' still count as fillers."""
    rows = [
        "| Margin | TBD Q3 | weekly | S01 | cut production |",
        "| Demand | below 5% | monthly | maybe EIA report | reduce headcount |",
        "| PE | above 40x | quarterly | S03 | observe weekly |",
    ]
    p = _write(tmp_path, _monitoring_report(rows))
    result = audit_report._run_market_outlook_monitoring_actionability(p, strict=True)
    assert result.errors, "multi-word placeholder fillers must not count"


def test_quarter_label_with_placeholder_value_not_a_layer(tmp_path: Path) -> None:
    """'最新季度：待补充' must not count as a quarter time layer."""
    anchor = "研究锚定：最新完整财年：FY2025｜最新季度：待补充\n"
    report = (
        "# TSMC\n\n" + _route_block("listed-company") + "\n\n" + anchor + "\n"
        + _snapshot_table() + "\n## 投资判断\n\nGrowth intact [S01].\n\n"
        + _source_register()
    )
    errors, _ = vlc.validate_file(_write(tmp_path, report), route_id="listed-company")
    assert any("anchor" in e for e in errors), (
        "FY only + placeholder quarter locks 1/3; must fail", errors
    )


def test_cadence_with_explicit_frequency_and_this_year_passes(tmp_path: Path) -> None:
    """'monthly through this year' has an explicit frequency → valid cadence."""
    rows = [
        "| Margin | below 30% | monthly through this year | S01 | cut production |",
        "| Demand | below 5% | weekly | S02 | reduce headcount |",
        "| PE | above 40x | quarterly | S03 | take profit |",
    ]
    p = _write(tmp_path, _monitoring_report(rows))
    result = audit_report._run_market_outlook_monitoring_actionability(p, strict=True)
    assert not result.errors, result.errors



# ── Review round 4: value-cell parsing / review action / segment isolation / cadence frequency ──


def test_snapshot_source_id_not_counted_as_value(tmp_path: Path) -> None:
    """A placeholder value next to a [S01] source id must not count."""
    snapshot = (
        "## 市场快照\n\n| 指标 | 值 | 来源 |\n|------|-----|------|\n"
        "| 当前股价 | __x | [S01] |\n"
        "| 市值 | __x | [S02] |\n"
        "| PE (TTM) | __x | [S03] |\n"
        "| PB | __x | [S01] |\n"
        "| 52周区间 | __x | [S02] |\n"
    )
    report = (
        "# TSMC\n\n" + _route_block("listed-company") + "\n" + _anchor_block()
        + "\n" + snapshot + "\n## 投资判断\n\nGrowth intact [S01].\n\n"
        + _source_register()
    )
    errors, _ = vlc.validate_file(_write(tmp_path, report), route_id="listed-company")
    assert any("market snapshot" in e or "market-snapshot" in e for e in errors), errors


def test_vague_action_review_not_counted(tmp_path: Path) -> None:
    """trigger-to-action = 'review' is not a concrete action."""
    rows = [
        "| Margin | below 30% | weekly | S01 | review |",
        "| Demand | below 5% | monthly | S02 | 看情况 |",
        "| PE | above 40x | quarterly | S03 | 视情况 |",
    ]
    p = _write(tmp_path, _monitoring_report(rows))
    result = audit_report._run_market_outlook_monitoring_actionability(p, strict=True)
    assert result.errors, "review/看情况/视情况 actions must not count"


def test_fy_value_does_not_leak_from_quarter_segment(tmp_path: Path) -> None:
    """FY segment must not borrow the quarter report date as its value."""
    anchor = "研究锚定：最新完整财年：待补充｜最新季度：2026Q1（2026-03-31）｜市场快照：待补充\n"
    report = (
        "# TSMC\n\n" + _route_block("listed-company") + "\n\n" + anchor + "\n"
        + _snapshot_table() + "\n## 投资判断\n\nGrowth intact [S01].\n\n"
        + _source_register()
    )
    errors, _ = vlc.validate_file(_write(tmp_path, report), route_id="listed-company")
    assert any("anchor" in e for e in errors), (
        "FY value placeholder + quarter only = 1 layer; must fail", errors
    )


def test_cadence_with_frequency_and_vague_phrase_passes(tmp_path: Path) -> None:
    """'weekly later this year' has an explicit frequency → valid cadence."""
    rows = [
        "| Margin | below 30% | weekly later this year | S01 | cut production |",
        "| Demand | below 5% | monthly | S02 | reduce headcount |",
        "| PE | above 40x | quarterly | S03 | take profit |",
    ]
    p = _write(tmp_path, _monitoring_report(rows))
    result = audit_report._run_market_outlook_monitoring_actionability(p, strict=True)
    assert not result.errors, result.errors



def test_cadence_hard_placeholder_with_frequency_not_counted(tmp_path: Path) -> None:
    """'TBD weekly' must not pass just because it contains a frequency word."""
    rows = [
        "| Margin | below 30% | TBD weekly | S01 | cut production |",
        "| Demand | below 5% | N/A monthly | S02 | reduce headcount |",
        "| PE | above 40x | unknown quarterly | S03 | take profit |",
    ]
    p = _write(tmp_path, _monitoring_report(rows))
    result = audit_report._run_market_outlook_monitoring_actionability(p, strict=True)
    assert result.errors, "TBD weekly / N/A monthly must not count"



def test_cadence_weekly_review_is_valid(tmp_path: Path) -> None:
    """'weekly review' names a real frequency and must not be rejected."""
    rows = [
        "| Margin | below 30% | weekly review | S01 | cut production |",
        "| Demand | below 5% | monthly | S02 | reduce headcount |",
        "| PE | above 40x | quarterly | S03 | take profit |",
    ]
    p = _write(tmp_path, _monitoring_report(rows))
    result = audit_report._run_market_outlook_monitoring_actionability(p, strict=True)
    assert not result.errors, result.errors



def test_none_provided_source_not_counted(tmp_path: Path) -> None:
    """'source = none provided' must be blocked as a multi-word placeholder."""
    rows = [
        "| Margin | below 30% | weekly | none provided | cut production |",
        "| Demand | below 5% | monthly | EIA report | reduce headcount |",
        "| PE | above 40x | quarterly | S03 | take profit |",
    ]
    p = _write(tmp_path, _monitoring_report(rows))
    result = audit_report._run_market_outlook_monitoring_actionability(p, strict=True)
    assert result.errors, "none provided source must not count"



# ── Review round 6: no untethered FY/quarter, concrete action override, missing-source phrases ──


def test_historical_fy_quarter_refs_do_not_count_as_current_layers(tmp_path: Path) -> None:
    """Historical FY/quarter prose must not satisfy the current-time-layer gate."""
    anchor = (
        "## 研究锚定块\n\n"
        "- **最新完整财年**: 待补充\n"
        "- **最新季度**: 待补充\n"
        "- **快照日期**: 待补充\n\n"
        "历史对比采用 FY2025 与 2025Q4 的基数。\n"
    )
    report = (
        "# TSMC\n\n" + _route_block("listed-company") + "\n" + anchor
        + "\n" + _snapshot_table() + "\n## 投资判断\n\nGrowth intact [S01].\n\n"
        + _source_register()
    )
    errors, _ = vlc.validate_file(_write(tmp_path, report), route_id="listed-company")
    assert any("anchor" in e for e in errors), (
        "historical FY2025/2025Q4 must not count; must fail", errors
    )


def test_bare_review_action_fails_but_concrete_monitoring_action_passes(tmp_path: Path) -> None:
    """Bare 'review' fails; 'monitor ... and cut ... if ...' passes."""
    (tmp_path / "bare").mkdir()
    bare = _write(tmp_path / "bare", _monitoring_report([
        "| Margin | below 30% | weekly | S01 | review |",
        "| Demand | below 5% | monthly | S02 | observe |",
        "| PE | above 40x | quarterly | S03 | 关注 |",
    ]))
    r1 = audit_report._run_market_outlook_monitoring_actionability(bare, strict=True)
    assert r1.errors, "bare vague actions must fail"

    (tmp_path / "concrete").mkdir()
    concrete = _write(tmp_path / "concrete", _monitoring_report([
        "| Margin | below 30% | weekly | S01 | monitor margin and cut production if below 30% |",
        "| Demand | below 5% | monthly | S02 | reduce headcount |",
        "| PE | above 40x | quarterly | S03 | take profit |",
    ]))
    r2 = audit_report._run_market_outlook_monitoring_actionability(concrete, strict=True)
    assert not r2.errors, r2.errors


def test_missing_source_phrases_not_counted(tmp_path: Path) -> None:
    """not provided / no source / 无来源 must not count as a source."""
    rows = [
        "| Margin | below 30% | weekly | not provided | cut production |",
        "| Demand | below 5% | monthly | no source | reduce headcount |",
        "| PE | above 40x | quarterly | 无来源 | take profit |",
    ]
    p = _write(tmp_path, _monitoring_report(rows))
    result = audit_report._run_market_outlook_monitoring_actionability(p, strict=True)
    assert result.errors, "missing-source phrases must not count"



# ── Review round 7: quarter needs year, concrete-action without arbitrary digit ──


def test_bare_q1_without_year_not_a_layer(tmp_path: Path) -> None:
    """'最新季度：Q1' (no year) must not count as a quarter layer."""
    anchor = "研究锚定：最新FY：待补充｜最新季度：Q1｜市场快照：2026-09-24\n"
    report = (
        "# TSMC\n\n" + _route_block("listed-company") + "\n\n" + anchor + "\n"
        + _snapshot_table() + "\n## 投资判断\n\nGrowth intact [S01].\n\n"
        + _source_register()
    )
    errors, _ = vlc.validate_file(_write(tmp_path, report), route_id="listed-company")
    assert any("anchor" in e for e in errors), errors


def test_yearly_interim_h1_counts(tmp_path: Path) -> None:
    """'最新半年报：2026H1' with a year counts as the quarter/interim layer."""
    anchor = (
        "## 研究锚定块\n\n"
        "- **最新完整财年**: FY2025\n"
        "- **最新半年报**: 2026H1\n"
        "- **快照日期**: 2026-09-24\n"
    )
    report = (
        "# TSMC\n\n" + _route_block("listed-company") + "\n" + anchor
        + "\n" + _snapshot_table() + "\n## 投资判断\n\nGrowth intact [S01].\n\n"
        + _source_register()
    )
    errors, _ = vlc.validate_file(_write(tmp_path, report), route_id="listed-company")
    assert not any("anchor" in e for e in errors), errors


def test_review_with_source_id_still_fails(tmp_path: Path) -> None:
    """'review [S01]' has no concrete measure and must fail."""
    rows = [
        "| Margin | below 30% | weekly | S01 | review [S01] |",
        "| Demand | below 5% | monthly | S02 | observe [S02] |",
        "| PE | above 40x | quarterly | S03 | 关注 |",
    ]
    p = _write(tmp_path, _monitoring_report(rows))
    result = audit_report._run_market_outlook_monitoring_actionability(p, strict=True)
    assert result.errors, "review [S01] must not count"


def test_conditional_action_with_concrete_measure_passes(tmp_path: Path) -> None:
    """'review if ... then cut production' is a concrete action."""
    rows = [
        "| Margin | below 30% | weekly | S01 | review if revenue falls below 30%, then cut production |",
        "| Demand | below 5% | monthly | S02 | reduce headcount |",
        "| PE | above 40x | quarterly | S03 | take profit |",
    ]
    p = _write(tmp_path, _monitoring_report(rows))
    result = audit_report._run_market_outlook_monitoring_actionability(p, strict=True)
    assert not result.errors, result.errors



# ── Review round 8: Chinese quarter format, word-boundary action verbs ──


def test_chinese_quarter_format_counts(tmp_path: Path) -> None:
    """'最新季度：2026年一季报' (doc-allowed format) counts as the quarter layer."""
    anchor = (
        "## 研究锚定块\n\n"
        "- **最新完整财年**: FY2025\n"
        "- **最新季度**: 2026年一季报\n"
        "- **快照日期**: 2026-09-24\n"
    )
    report = (
        "# TSMC\n\n" + _route_block("listed-company") + "\n" + anchor
        + "\n" + _snapshot_table() + "\n## 投资判断\n\nGrowth intact [S01].\n\n"
        + _source_register()
    )
    errors, _ = vlc.validate_file(_write(tmp_path, report), route_id="listed-company")
    assert not any("anchor" in e for e in errors), errors


def test_review_execution_plan_fails(tmp_path: Path) -> None:
    """'review execution plan' has no concrete measure (cut inside execution)."""
    rows = [
        "| Margin | below 30% | weekly | S01 | review execution plan |",
        "| Demand | below 5% | monthly | S02 | observe |",
        "| PE | above 40x | quarterly | S03 | 关注 |",
    ]
    p = _write(tmp_path, _monitoring_report(rows))
    result = audit_report._run_market_outlook_monitoring_actionability(p, strict=True)
    assert result.errors, "review execution plan must not count"



def test_quarter_reversed_year_order_q1_2026_isolated(tmp_path: Path) -> None:
    """Isolated: FY empty, quarter='Q1 2026', snapshot valid → passes via quarter layer."""
    anchor = (
        "## 研究锚定块\n\n"
        "- **最新完整财年**: 待补充\n"
        "- **最新季度**: Q1 2026\n"
        "- **快照日期**: 2026-09-24\n"
    )
    report = (
        "# TSMC\n\n" + _route_block("listed-company") + "\n" + anchor
        + "\n" + _snapshot_table() + "\n## 投资判断\n\nGrowth intact [S01].\n\n"
        + _source_register()
    )
    errors, _ = vlc.validate_file(_write(tmp_path, report), route_id="listed-company")
    assert not any("anchor" in e for e in errors), errors


def test_anchor_placeholder_annotations_do_not_count_periods(tmp_path: Path) -> None:
    """Dates in notes beside placeholder values must not fill anchor fields."""
    anchor = (
        "## 研究锚定块\n\n"
        "- **最新完整财年**: 待补充（历史对照 FY2025）\n"
        "- **最新季度**: 待补充（历史期间 2025Q4）\n"
        "- **快照日期**: 待补充（历史快照 2026-09-24）\n"
    )
    report = (
        "# TSMC\n\n" + _route_block("listed-company") + "\n" + anchor
        + "\n" + _snapshot_table() + "\n## 投资判断\n\nGrowth intact [S01].\n\n"
        + _source_register()
    )
    errors, _ = vlc.validate_file(_write(tmp_path, report), route_id="listed-company")
    assert any("anchor" in e.lower() for e in errors), errors


def test_invalid_calendar_date_does_not_fill_snapshot_anchor(tmp_path: Path) -> None:
    """A date-shaped but impossible snapshot date is not an anchor layer."""
    anchor = (
        "## 研究锚定块\n\n"
        "- **最新完整财年**: FY2025\n"
        "- **最新季度**: 待补充\n"
        "- **快照日期**: 2026-02-30\n"
    )
    report = (
        "# TSMC\n\n" + _route_block("listed-company") + "\n" + anchor
        + "\n" + _snapshot_table() + "\n## 投资判断\n\nGrowth intact [S01].\n\n"
        + _source_register()
    )
    errors, _ = vlc.validate_file(_write(tmp_path, report), route_id="listed-company")
    assert any("anchor" in e.lower() for e in errors), errors


def test_anchor_labels_inside_notes_do_not_count_as_fields(tmp_path: Path) -> None:
    """Anchor labels embedded in prose are not parsed as declared field values."""
    anchor = (
        "## 研究锚定块\n\n"
        "- 历史注释：最新完整财年：FY2025；最新季度：2026Q1；"
        "快照日期：2026-09-24\n"
    )
    report = (
        "# TSMC\n\n" + _route_block("listed-company") + "\n" + anchor
        + "\n" + _snapshot_table() + "\n## 投资判断\n\nGrowth intact [S01].\n\n"
        + _source_register()
    )
    errors, _ = vlc.validate_file(_write(tmp_path, report), route_id="listed-company")
    assert any("anchor" in e.lower() for e in errors), errors


def test_snapshot_dates_in_placeholder_values_do_not_count(tmp_path: Path) -> None:
    """A date annotation cannot make a placeholder metric look numeric."""
    snapshot = (
        "## 市场快照\n\n| 指标 | 值 | 来源 |\n|------|-----|------|\n"
        "| 当前股价 | 待补充（截至 2026-09-24） | [S01] |\n"
        "| 市值 | 待补充（截至 2026-09-24） | [S01] |\n"
        "| PE (TTM) | 待补充（截至 2026-09-24） | [S01] |\n"
        "| PB | 待补充（截至 2026-09-24） | [S01] |\n"
        "| PS | 待补充（截至 2026-09-24） | [S01] |\n"
    )
    report = (
        "# TSMC\n\n" + _route_block("listed-company") + "\n" + _anchor_block()
        + "\n" + snapshot + "\n## 投资判断\n\nGrowth intact [S01].\n\n"
        + _source_register()
    )
    errors, _ = vlc.validate_file(_write(tmp_path, report), route_id="listed-company")
    assert any("market snapshot" in e.lower() for e in errors), errors


def test_snapshot_metrics_reject_wrong_numeric_formats(tmp_path: Path) -> None:
    """A number or date only counts when it has the metric's value format."""
    snapshot = (
        "## 市场快照\n\n| 指标 | 值 | 来源 |\n|------|-----|------|\n"
        "| 当前股价 | 2026Q1 | [S01] |\n"
        "| 市值 | 10 | [S01] |\n"
        "| PE (TTM) | 2026-09-24 | [S01] |\n"
        "| PE (Forward) | FY2025 | [S01] |\n"
        "| PB | maybe 3 | [S01] |\n"
        "| PS | N/A 5 | [S01] |\n"
        "| 52周区间 | 2026-2027 | [S01] |\n"
        "| 股息率 | 5x | [S01] |\n"
    )
    errors = vlc.check_market_snapshot(snapshot, tmp_path / "snapshot.md")
    assert errors and "only 0/8" in errors[0], errors


def test_snapshot_values_marked_unverified_do_not_count(tmp_path: Path) -> None:
    """A numeric value remains incomplete when its note says it needs review."""
    snapshot = (
        "## 市场快照\n\n| 指标 | 值 | 来源 |\n|------|-----|------|\n"
        "| 当前股价 | 185.5（待核实） | [S01] |\n"
        "| 市值 | $960B（待更新） | [S01] |\n"
        "| PE (TTM) | 28x（待核实） | [S01] |\n"
        "| PE (Forward) | 20x（待更新） | [S01] |\n"
        "| PB | 3x（待核实） | [S01] |\n"
    )
    errors = vlc.check_market_snapshot(snapshot, tmp_path / "snapshot.md")
    assert errors and "only 0/8" in errors[0], errors


def test_eps_row_does_not_fill_missing_ps_snapshot_metric(tmp_path: Path) -> None:
    """EPS is not the price-to-sales ratio and cannot make the fifth field."""
    snapshot = (
        "## 市场快照\n\n| 指标 | 值 | 来源 |\n|------|-----|------|\n"
        "| 当前股价 | $185.50 | [S01] |\n"
        "| 市值 | $960B | [S01] |\n"
        "| PE (TTM) | 28.5x | [S01] |\n"
        "| PB | 7.2x | [S01] |\n"
        "| EPS | 5.2 | [S01] |\n"
    )
    errors = vlc.check_market_snapshot(snapshot, tmp_path / "snapshot.md")
    assert errors and "only 4/8" in errors[0], errors


def test_period_and_source_ids_do_not_satisfy_threshold(tmp_path: Path) -> None:
    """Years, quarters and source ids are not numeric monitoring thresholds."""
    rows = [
        "| Margin | FY2025 | weekly | EIA report | cut production |",
        "| Demand | Q1 2026 | monthly | S02 | reduce headcount |",
        "| PE | S01 | quarterly | S03 | take profit |",
    ]
    p = _write(tmp_path, _monitoring_report(rows))
    result = audit_report._run_market_outlook_monitoring_actionability(p, strict=True)
    assert result.errors, "periods and source IDs must not count as thresholds"
    assert not audit_report._monitoring_field_actionable("threshold", "revisit in 2027")


def test_unspecified_source_and_revisit_plan_are_partial(tmp_path: Path) -> None:
    """Generic source/action prose must not count as fully-defined signals."""
    rows = [
        "| Margin | below 30% | weekly | some source | cut production |",
        "| Demand | below 5% | monthly | EIA report | revisit plan |",
        "| PE | above 40x | quarterly | S03 | take profit |",
    ]
    p = _write(tmp_path, _monitoring_report(rows))
    result = audit_report._run_market_outlook_monitoring_actionability(p, strict=True)
    assert result.errors, "unspecified source/action text must remain partial"
    assert not audit_report._monitoring_field_actionable(
        "trigger_to_action", "take another look"
    )


def test_generic_report_and_data_are_not_monitoring_sources(tmp_path: Path) -> None:
    """Generic capitalized nouns do not identify a monitoring data source."""
    rows = [
        "| Margin | below 30% | weekly | Report | cut production |",
        "| Demand | below 5% | monthly | 行业报告 | reduce headcount |",
        "| PE | above 40x | quarterly | 政府报告 | take profit |",
    ]
    p = _write(tmp_path, _monitoring_report(rows))
    result = audit_report._run_market_outlook_monitoring_actionability(p, strict=True)
    assert result.errors, "generic source labels must leave the rows partial"
    assert not audit_report._monitoring_field_actionable("source", "Report")
    assert not audit_report._monitoring_field_actionable("source", "Data")
    assert not audit_report._monitoring_field_actionable("source", "Public Data")
    assert not audit_report._monitoring_field_actionable("source", "Public Data Report")
    assert not audit_report._monitoring_field_actionable("source", "行业数据")
    assert not audit_report._monitoring_field_actionable("source", "行业报告")
    assert not audit_report._monitoring_field_actionable("source", "政府报告")
    assert not audit_report._monitoring_field_actionable("source", "Industry data")


def test_chinese_monitoring_values_are_actionable(tmp_path: Path) -> None:
    """Chinese comparisons, named sources, cadences and actions remain valid."""
    report = (
        "# 市场展望\n\n## 监测信号\n\n"
        "| 指标 | 阈值 | 频率 | 来源 | 触发动作 |\n"
        "|------|------|------|------|----------|\n"
        "| 毛利率 | 低于30% | 每月 | 国家统计局月报 | 暂停扩产 |\n"
        "| 电价 | 不超过0.12 | 每季度 | 国家能源局公告 | 削减产能 |\n"
        "| 估值 | 高于40倍 | 每周 | 新华社 | 推迟投资 |\n"
    )
    p = _write(tmp_path, report)
    result = audit_report._run_market_outlook_monitoring_actionability(p, strict=True)
    assert not result.errors, result.errors


def test_stress_test_is_not_a_placeholder_token(tmp_path: Path) -> None:
    """A domain term containing 'test' remains usable in an actionable row."""
    rows = [
        "| Margin | below 30% | weekly | Stress-test report | stress-test downside |",
        "| Demand | below 5% | monthly | EIA report | reduce headcount |",
        "| PE | above 40x | quarterly | S03 | take profit |",
    ]
    p = _write(tmp_path, _monitoring_report(rows))
    result = audit_report._run_market_outlook_monitoring_actionability(p, strict=True)
    assert not result.errors, result.errors


def test_inline_code_route_name_resolves_to_canonical_id(tmp_path: Path) -> None:
    """Backticks around a declared route do not change route identity."""
    assert audit_report._normalize_route("`listed-company`") == "listed-company"
    report = (
        "# TSMC\n\n" + _route_block("`listed-company`")
        + "\n## 投资判断\n\nGrowth intact [S01].\n\n" + _source_register()
    )
    p = _write(tmp_path, report)
    proc = subprocess.run(
        [sys.executable, VLC_SCRIPT, str(p)], capture_output=True, text=True
    )
    assert proc.returncode == 2, proc.stdout
    assert "research-anchor" in proc.stdout.lower(), proc.stdout
    assert "cannot be resolved" not in proc.stdout.lower(), proc.stdout


def test_route_registry_error_is_a_blocking_cli_resolution_error(
    tmp_path: Path, monkeypatch
) -> None:
    """Registry corruption is reported as a route error, not an uncaught crash."""
    report = _write(tmp_path, _route_block("listed-company"))

    def broken_registry():
        raise vlc.registry_loader.RegistryError("invalid test registry")

    monkeypatch.setattr(vlc.registry_loader, "load_route_registry", broken_registry)
    route_id, error = vlc._resolve_route_id(report)
    assert route_id is None
    assert error is not None and "route registry is invalid" in error
