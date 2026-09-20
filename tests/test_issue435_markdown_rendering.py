"""Issue #435 C2-C4: fence preservation and table DOM/column integrity.

Fenced code must survive the delivery transformation pipeline verbatim, and
table post-processing must keep real tag boundaries, pad ragged rows instead
of truncating them, and report every column it folds.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from delivery.markdown_rows import split_markdown_row  # noqa: E402
from delivery.normalization import normalize_text_for_pdf  # noqa: E402
from delivery.table_repair import repair_markdown_tables  # noqa: E402
from delivery.tables import maybe_wrap_wide_tables_in_html  # noqa: E402
from markdown_to_html import process_markdown  # noqa: E402


FENCED = """# Title

```text
A | B | C
---|---|---

# not a heading
- not a list
> not a quote



inner tail
```

End.
"""

TILDE_FENCED = """# Tilde

~~~python
x = 1  # 中 文



y = 2
~~~
"""

UNCLOSED = """# Unclosed

```
A | B | C
# still code
``` not closed
C | D
"""


def _fence_content(text: str, opener: str) -> str:
    _, rest = text.split(opener + "\n", 1)
    closer = opener[0] * 3
    return rest.split("\n" + closer, 1)[0]


def test_normalize_preserves_backtick_fence_content_verbatim() -> None:
    normalized = normalize_text_for_pdf(FENCED)
    assert _fence_content(normalized, "```text") == _fence_content(FENCED, "```text")


def test_normalize_preserves_tilde_fence_content_verbatim() -> None:
    normalized = normalize_text_for_pdf(TILDE_FENCED)
    assert _fence_content(normalized, "~~~python") == _fence_content(TILDE_FENCED, "~~~python")


def test_convert_reads_crlf_without_universal_newline_translation(
    tmp_path: Path, monkeypatch
) -> None:
    report = tmp_path / "report.md"
    report.write_bytes(b"# R\r\n\r\n```text\r\nline1\r\nline2\r\n```\r\n")
    captured: dict[str, str] = {}

    import markdown_to_html

    real_normalize = markdown_to_html.normalize_text_for_pdf

    def spy(text: str) -> str:
        captured["text"] = text
        return real_normalize(text)

    monkeypatch.setattr(markdown_to_html, "normalize_text_for_pdf", spy)
    output = tmp_path / "out.html"

    markdown_to_html.convert(report, output)

    assert "line1\r\nline2" in captured["text"]
    html = output.read_text(encoding="utf-8")
    assert "line1" in html
    assert "line2" in html


def test_normalize_preserves_fence_unicode_and_line_endings_verbatim() -> None:
    text = "# T\r\n\r\n```text\r\ne\u0301 += 1\r\n\r\ntail\r\n```\r\n"
    normalized = normalize_text_for_pdf(text)
    assert "e\u0301" in normalized
    assert "\r\n" in normalized
    assert normalize_text_for_pdf("e\u0301") == "é"


def test_normalize_preserves_unclosed_fence_tail() -> None:
    normalized = normalize_text_for_pdf(UNCLOSED)
    assert "A | B | C\n# still code\n``` not closed\nC | D" in normalized
    assert "| A | B | C |" not in normalized


def test_repair_ignores_fenced_code() -> None:
    fenced = "```text\nA | B | C\n---|---|---\n```\n"
    assert repair_markdown_tables(fenced) == fenced


def test_repair_still_normalizes_visible_tables() -> None:
    repaired = repair_markdown_tables("| A | B |\n| 1 | 2 |\n")
    assert "| --- | --- |" in repaired


def test_repair_keeps_data_wider_than_header() -> None:
    repaired = repair_markdown_tables("| A | B |\n|---|---|\n| 1 | 2 | 3 |\n")
    assert "3" in repaired
    assert repaired.splitlines()[1].count("---") == 3


def test_process_markdown_keeps_data_wider_than_header() -> None:
    body = process_markdown("| A | B |\n|---|---|\n| 1 | 2 | 3 |\n")
    assert "<td>3</td>" in body
    assert body.count("<th>") == 3


def test_repair_keeps_data_column_before_no_header() -> None:
    md = (
        "|        | No. | Item |\n"
        "|--------|-----|------|\n"
        "| urgent | 1   | A    |\n"
        "| normal | 2   | B    |\n"
    )
    repaired = repair_markdown_tables(md)
    assert "urgent" in repaired
    assert "normal" in repaired


def test_repair_checks_first_data_row_when_separator_missing() -> None:
    md = "|   | Item |\n| urgent | A |\n| - | B |\n"
    repaired = repair_markdown_tables(md)
    assert "urgent" in repaired
    assert "| urgent | A |" in repaired


def test_process_markdown_keeps_first_data_row_when_separator_missing() -> None:
    body = process_markdown("|   | Item |\n| urgent | A |\n| - | B |\n")
    assert "<td>urgent</td>" in body


def test_repair_does_not_turn_escaped_pipe_prose_into_table() -> None:
    md = "a \\| b \\| c\nx \\| y \\| z\n"
    assert repair_markdown_tables(md) == md


def test_fullwidth_pipe_cell_data_is_preserved() -> None:
    md = "| Name | Symbol |\n|---|---|\n| foo | ｜ |\n"
    repaired = repair_markdown_tables(md)
    assert "｜" in repaired
    assert "| foo | ｜ |" in repaired


def test_fullwidth_pipe_inside_inline_code_is_preserved() -> None:
    md = "| Expr | Note |\n|---|---|\n| `a｜b` | keep |\n"
    repaired = repair_markdown_tables(md)
    assert "`a｜b`" in repaired
    assert "a|b" not in repaired


def test_process_markdown_keeps_fullwidth_pipe_cell_data() -> None:
    body = process_markdown("| Name | Symbol |\n|---|---|\n| foo | ｜ |\n")
    assert "｜" in body
    assert "<td>foo</td>" in body


def test_fullwidth_delimiters_still_repair_legacy_tables() -> None:
    repaired = repair_markdown_tables("｜ A ｜ B ｜\n｜ 1 ｜ 2 ｜\n")
    assert "| A | B |" in repaired
    assert "| 1 | 2 |" in repaired


def test_repair_preserves_alignment_separators() -> None:
    repaired = repair_markdown_tables("| A | B |\n|:---|---:|\n| 1 | 2 |\n")
    assert "| :--- | ---: |" in repaired


def test_single_structural_pipe_prose_is_not_promoted_to_table() -> None:
    md = "Alpha | Beta\nGamma | Delta\n"
    assert repair_markdown_tables(md) == md


def test_normalize_does_not_promote_single_pipe_prose() -> None:
    normalized = normalize_text_for_pdf("Alpha | Beta\nGamma | Delta\n")
    assert normalized == "Alpha | Beta\nGamma | Delta"


def test_process_markdown_does_not_promote_single_pipe_prose() -> None:
    body = process_markdown("Alpha | Beta\nGamma | Delta\n")
    assert "<table" not in body
    assert "Alpha | Beta" in body


def test_tokenizer_backslash_before_closing_backtick() -> None:
    cells = split_markdown_row("| `a\\` | keep |")
    assert cells == ["`a\\`", "keep"]


def test_tokenizer_unmatched_backtick_keeps_structural_pipes() -> None:
    cells = split_markdown_row("| `literal | B | C |")
    assert cells == ["`literal", "B", "C"]


def test_tokenizer_different_length_backtick_run_stays_inside_code_span() -> None:
    cells = split_markdown_row("| ``a`b`` | x |")
    assert cells == ["``a`b``", "x"]


def test_process_markdown_unmatched_backtick_keeps_columns() -> None:
    body = process_markdown(
        "| A | B | C |\n|---|---|---|\n| `literal | B | C |\n"
    )
    assert "<td>B</td>" in body
    assert "<td>C</td>" in body
    assert body.count("<td>") == 3


def test_table_attributes_preserve_original_markup() -> None:
    html = (
        '<table id="metrics" class="compact">'
        "<thead><tr><th>A</th><th>B</th></tr></thead>"
        "<tbody><tr><td>1</td><td>2</td></tr></tbody></table>"
    )
    rendered = maybe_wrap_wide_tables_in_html(html)
    assert html in rendered


def test_caption_is_preserved_via_fail_safe() -> None:
    html = (
        "<table><caption>Important title</caption>"
        "<thead><tr><th>A</th><th>B</th></tr></thead>"
        "<tbody><tr><td>1</td><td>2</td></tr></tbody></table>"
    )
    rendered = maybe_wrap_wide_tables_in_html(html)
    assert html in rendered
    assert "Important title" in rendered


def test_colgroup_is_preserved_via_fail_safe() -> None:
    html = (
        "<table><colgroup><col span='1'><col span='1'></colgroup>"
        "<thead><tr><th>A</th><th>B</th></tr></thead>"
        "<tbody><tr><td>1</td><td>2</td></tr></tbody></table>"
    )
    rendered = maybe_wrap_wide_tables_in_html(html)
    assert html in rendered


def test_tfoot_is_preserved_via_fail_safe() -> None:
    html = (
        "<table><thead><tr><th>A</th><th>B</th></tr></thead>"
        "<tfoot><tr><td>f1</td><td>f2</td></tr></tfoot>"
        "<tbody><tr><td>1</td><td>2</td></tr></tbody></table>"
    )
    rendered = maybe_wrap_wide_tables_in_html(html)
    assert html in rendered


def test_malformed_span_value_preserves_original_markup() -> None:
    html = (
        "<table><thead><tr><th>A</th><th>B</th></tr></thead>"
        '<tbody><tr><td colspan="abc">x</td><td>y</td></tr></tbody></table>'
    )
    rendered = maybe_wrap_wide_tables_in_html(html)
    assert html in rendered


def test_duplicate_span_attributes_preserve_original_markup() -> None:
    html = (
        "<table><thead><tr><th>A</th><th>B</th></tr></thead>"
        '<tbody><tr><td colspan="2" colspan="1">x</td><td>y</td></tr></tbody></table>'
    )
    rendered = maybe_wrap_wide_tables_in_html(html)
    assert html in rendered


def test_alignment_styles_are_rebuild_safe() -> None:
    html = (
        '<table><thead><tr><th style="text-align: left;">A</th>'
        '<th style="text-align: right;">B</th></tr></thead>'
        '<tbody><tr><td style="text-align: left;">1</td>'
        '<td style="text-align: right;">2</td></tr></tbody></table>'
    )
    rendered = maybe_wrap_wide_tables_in_html(html)
    assert "<th>A</th>" in rendered
    assert "<td>1</td>" in rendered


def test_other_inline_styles_still_preserve_original_markup() -> None:
    html = (
        '<table><thead><tr><th style="color: red;">A</th><th>B</th></tr></thead>'
        "<tbody><tr><td>1</td><td>2</td></tr></tbody></table>"
    )
    rendered = maybe_wrap_wide_tables_in_html(html)
    assert html in rendered


def test_aligned_markdown_table_keeps_wide_processing() -> None:
    body = process_markdown(
        "| A | B | C | D | E |\n"
        "|:--|--:|:--:|---|---:|\n"
        "| 1 | 2 | 3 | 4 | 5 |\n"
    )
    assert "split-table-group" in body
    assert body.count("<table>") >= 2


def test_cell_attributes_preserve_original_markup() -> None:
    html = (
        "<table><thead><tr><th>A</th><th>B</th></tr></thead>"
        '<tbody><tr><td class="important">1</td><td>2</td></tr></tbody></table>'
    )
    rendered = maybe_wrap_wide_tables_in_html(html)
    assert html in rendered


def test_repair_does_not_turn_inline_code_pipe_prose_into_table() -> None:
    md = "`a|b|c`\n`x|y|z`\n"
    assert repair_markdown_tables(md) == md


def test_repair_reports_dropped_layout_column() -> None:
    warnings: list[str] = []
    repaired = repair_markdown_tables(
        "|   | # | Item |\n"
        "|---|---|---|\n"
        "| - | 1 | A |\n"
        "| * | 2 | B |\n",
        warnings=warnings,
    )
    assert warnings
    assert any("column" in warning for warning in warnings)
    assert "Item" in repaired


def test_normalize_keeps_escaped_pipe_in_one_cell() -> None:
    normalized = normalize_text_for_pdf(
        "| Expr | Note |\n|---|---|\n| a \\| b | keep-me |\n"
    )
    assert "| a \\| b | keep-me |" in normalized


def test_process_markdown_keeps_escaped_pipe_and_last_cell() -> None:
    body = process_markdown("| Expr | Note |\n|---|---|\n| a \\| b | keep-me |\n")
    assert "keep-me" in body
    assert "a | b" in body
    assert body.count("<td>") == 2


def test_process_markdown_keeps_inline_code_pipe_in_one_cell() -> None:
    body = process_markdown("| Expression | Meaning |\n|---|---|\n| `a|b` | union |\n")
    assert "union" in body
    assert "<code>a|b</code>" in body
    assert body.count("<td>") == 2


def test_process_markdown_keeps_fenced_table_like_content_as_code() -> None:
    body = process_markdown("```text\nA | B | C\n---|---|---\n```\n")
    assert "A | B | C\n---|---|---" in body
    assert "<table" not in body


def test_markdown_table_has_no_empty_header_row() -> None:
    body = process_markdown("## Sec\n\n| A | B |\n|---|---|\n| 1 | 2 |\n")
    assert "<thead><tr><th>A</th><th>B</th></tr></thead>" in body
    assert "<thead><tr><th></th></tr>" not in body


RAGGED = (
    "<table><thead><tr><th>A</th><th>B</th><th>C</th></tr></thead>"
    "<tbody><tr><td>1</td></tr><tr><td>1</td><td>2</td><td>3</td></tr></tbody></table>"
)


def test_ragged_rows_pad_instead_of_truncating_columns() -> None:
    rendered = maybe_wrap_wide_tables_in_html(RAGGED)
    assert "<th>A</th>" in rendered
    assert "<th>B</th>" in rendered
    assert "<th>C</th>" in rendered
    assert "<td>2</td>" in rendered
    assert "<td>3</td>" in rendered


def test_short_header_row_does_not_drop_data_columns() -> None:
    html = (
        "<table><thead><tr><th>A</th></tr></thead>"
        "<tbody><tr><td>1</td><td>2</td><td>3</td></tr></tbody></table>"
    )
    rendered = maybe_wrap_wide_tables_in_html(html)
    assert "<td>1</td>" in rendered
    assert "<td>2</td>" in rendered
    assert "<td>3</td>" in rendered
    assert "字段" not in rendered


def test_table_without_th_headers_is_preserved() -> None:
    html = "<table><tbody><tr><td>1</td><td>2</td></tr></tbody></table>"
    rendered = maybe_wrap_wide_tables_in_html(html)
    assert html in rendered


def test_colspan_cells_expand_without_losing_columns() -> None:
    html = (
        '<table><thead><tr><th colspan="2">Group</th><th>B</th></tr></thead>'
        '<tbody><tr><td>1</td><td colspan="2">2</td></tr></tbody></table>'
    )
    rendered = maybe_wrap_wide_tables_in_html(html)
    assert "Group" in rendered
    assert "<th>B</th>" in rendered
    assert "<td>1</td>" in rendered
    assert "<td>2</td>" in rendered
    assert rendered.count("<th>") == 3
    assert rendered.count("<td>") == 3


def test_rowspan_table_is_preserved_without_rebuild() -> None:
    html = (
        '<table><thead><tr><th>A</th><th>B</th></tr></thead>'
        '<tbody><tr><td rowspan="2">x</td><td>1</td></tr><tr><td>2</td></tr></tbody></table>'
    )
    rendered = maybe_wrap_wide_tables_in_html(html)
    assert html in rendered


def test_single_quoted_colspan_expands_columns() -> None:
    html = (
        "<table><thead><tr><th colspan='2'>Group</th><th>B</th></tr></thead>"
        "<tbody><tr><td>1</td><td colspan='2'>2</td></tr></tbody></table>"
    )
    rendered = maybe_wrap_wide_tables_in_html(html)
    assert "Group" in rendered
    assert rendered.count("<th>") == 3
    assert rendered.count("<td>") == 3


def test_single_quoted_rowspan_preserves_original_markup() -> None:
    html = (
        "<table><thead><tr><th>A</th><th>B</th></tr></thead>"
        "<tbody><tr><td rowspan='2'>x</td><td>1</td></tr><tr><td>2</td></tr></tbody></table>"
    )
    rendered = maybe_wrap_wide_tables_in_html(html)
    assert html in rendered


def test_data_colspan_attribute_is_not_treated_as_colspan() -> None:
    html = (
        '<table><thead><tr><th>A</th><th>B</th></tr></thead>'
        '<tbody><tr><td data-colspan="2">x</td><td>y</td></tr></tbody></table>'
    )
    rendered = maybe_wrap_wide_tables_in_html(html)
    # Non-span cell attributes are not rebuildable, so the original markup is
    # preserved verbatim and ``data-colspan`` can never expand a column.
    assert html in rendered
    assert rendered.count("<td") == 2


NESTED_TABLE = (
    "<table><thead><tr><th>A</th><th>B</th></tr></thead>"
    "<tbody><tr><td>1</td>"
    "<td><table><tbody><tr><td>inner</td></tr></tbody></table></td>"
    "</tr></tbody></table>"
)


def test_mismatched_cell_closing_tag_preserves_original_markup() -> None:
    html = (
        "<table><thead><tr><th>A</th><th>B</th></tr></thead>"
        "<tbody><tr><td>1</td><th>2</td></tr></tbody></table>"
    )
    rendered = maybe_wrap_wide_tables_in_html(html)
    assert html in rendered


def test_zero_colspan_preserves_original_markup() -> None:
    html = (
        "<table><thead><tr><th>A</th><th>B</th></tr></thead>"
        "<tbody><tr><td colspan='0'>x</td><td>y</td></tr></tbody></table>"
    )
    rendered = maybe_wrap_wide_tables_in_html(html)
    assert html in rendered


def test_nested_table_is_preserved_intact() -> None:
    rendered = maybe_wrap_wide_tables_in_html(NESTED_TABLE)
    assert NESTED_TABLE in rendered
    assert rendered.count("<table") == 2
    assert rendered.count("</table>") == 2


def test_rowspan_zero_preserves_original_markup() -> None:
    html = (
        '<table><thead><tr><th>A</th><th>B</th></tr></thead>'
        '<tbody><tr><td rowspan="0">x</td><td>1</td></tr>'
        '<tr><td>2</td></tr></tbody></table>'
    )
    rendered = maybe_wrap_wide_tables_in_html(html)
    assert html in rendered


def test_oversized_colspan_preserves_original_markup() -> None:
    html = (
        '<table><thead><tr><th>A</th><th>B</th></tr></thead>'
        '<tbody><tr><td colspan="1000">x</td><td>y</td></tr></tbody></table>'
    )
    rendered = maybe_wrap_wide_tables_in_html(html)
    assert html in rendered


def test_quoted_gt_rowspan_preserves_original_markup() -> None:
    html = (
        '<table><thead><tr><th>A</th><th>B</th></tr></thead>'
        '<tbody><tr><td title="1 > 0" rowspan="2">x</td><td>1</td></tr>'
        '<tr><td>2</td></tr></tbody></table>'
    )
    rendered = maybe_wrap_wide_tables_in_html(html)
    assert html in rendered


def test_quoted_gt_colspan_preserves_original_markup() -> None:
    html = (
        '<table><thead><tr><th>A</th><th>B</th><th>C</th></tr></thead>'
        '<tbody><tr><td title="a > b" colspan="2">x</td><td>y</td></tr></tbody></table>'
    )
    rendered = maybe_wrap_wide_tables_in_html(html)
    # The quoted ``>`` must not hide the colspan or cut the cell content; the
    # cell also carries a non-span attribute, so the table is preserved.
    assert html in rendered
    assert 'colspan="2"' in rendered


def test_semantic_placeholder_values_do_not_delete_columns() -> None:
    html = (
        "<table><thead><tr><th>Metric</th><th></th><th>Notes</th></tr></thead>"
        "<tbody><tr><td>Revenue</td><td>N/A</td><td>ok</td></tr>"
        "<tr><td>Margin</td><td>TBD</td><td>ok</td></tr>"
        "<tr><td>Risk</td><td>#1</td><td>ok</td></tr></tbody></table>"
    )
    rendered = maybe_wrap_wide_tables_in_html(html)
    assert "N/A" in rendered
    assert "TBD" in rendered
    assert "#1" in rendered
    assert rendered.count("<th>") == 3


def test_na_and_tbd_cells_are_not_blanked() -> None:
    body = process_markdown(
        "| Metric | Current |\n"
        "|---|---|\n"
        "| Revenue | N/A |\n"
        "| Margin | TBD |\n"
    )
    assert "N/A" in body
    assert "TBD" in body


METADATA_TABLE = (
    "<table><thead><tr><th>Name</th><th>Source</th><th>Notes</th><th>Type</th></tr></thead>"
    "<tbody><tr><td>A</td><td>https://example.com/a</td><td>ok</td><td>source</td></tr></tbody></table>"
)


def test_metadata_column_fold_requires_explicit_opt_in() -> None:
    warnings: list[str] = []
    rendered = maybe_wrap_wide_tables_in_html(METADATA_TABLE, warnings=warnings)
    assert "<th>Source</th>" in rendered
    assert not any("folded" in warning for warning in warnings)

    opt_in_warnings: list[str] = []
    folded = maybe_wrap_wide_tables_in_html(
        METADATA_TABLE,
        warnings=opt_in_warnings,
        fold_metadata_columns=True,
    )
    assert any("Source" in warning for warning in opt_in_warnings)
    assert "<th>Source</th>" not in folded
    assert "<th>Notes</th>" in folded


def test_process_markdown_keeps_metadata_columns_by_default() -> None:
    warnings: list[str] = []
    body = process_markdown(
        "| Name | Source | Notes | Type |\n"
        "|---|---|---|---|\n"
        "| A | https://example.com/a | ok | source |\n",
        warnings=warnings,
    )
    assert "<th>Source</th>" in body
    assert "example.com" in body
    assert not any("folded" in warning for warning in warnings)


def test_comparison_table_with_url_source_keeps_all_columns() -> None:
    body = process_markdown(
        "| Metric | A | B | Source |\n"
        "|---|---|---|---|\n"
        "| Revenue | 10 | 12 | https://example.com/1 |\n"
        "| Cost | 5 | 6 | https://example.com/2 |\n"
    )
    assert "<th>Source</th>" in body
    assert "example.com" in body


def test_monitoring_table_with_url_source_keeps_all_columns() -> None:
    body = process_markdown(
        "| Indicator | Threshold | Current | Source |\n"
        "|---|---|---|---|\n"
        "| FX rate | < 7.2 | 7.1 | https://example.com/fx |\n"
        "| Spread | < 120bp | 110bp | https://example.com/spread |\n"
    )
    assert "<th>Source</th>" in body
    assert "example.com" in body


def test_scoring_table_with_url_source_keeps_all_columns() -> None:
    body = process_markdown(
        "| Criterion | Weight | Score | Source |\n"
        "|---|---|---|---|\n"
        "| Moat | 30% | 4 | https://example.com/moat |\n"
        "| Growth | 20% | 3 | https://example.com/growth |\n"
    )
    assert "<th>Source</th>" in body
    assert "example.com" in body


SOURCE_REGISTER = (
    "| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |\n"
    "|---|---|---|---|---|---|---|\n"
    "| S01 | Official note | primary | 2026-07-23 | https://example.com/1 | high | §2 |\n"
    "| S02 | Independent analysis | secondary | 2026-07-23 | https://example.com/2 | medium | §3 |\n"
)


def test_source_register_headers_survive_end_to_end() -> None:
    body = process_markdown(SOURCE_REGISTER)
    assert "<thead><tr><th>ID</th>" in body
    for header in ("Source Name", "Source Type", "Date", "DOI/URL", "Reliability", "Claims Supported"):
        assert f"<th>{header}</th>" in body
    assert "<th></th>" not in body
