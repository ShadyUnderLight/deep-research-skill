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


def test_process_markdown_collects_fold_warnings() -> None:
    warnings: list[str] = []
    process_markdown(
        "| Name | Source | Notes | Type |\n"
        "|---|---|---|---|\n"
        "| A | https://example.com/a | ok | source |\n",
        warnings=warnings,
    )
    assert warnings
    assert any("Source" in warning for warning in warnings)


def test_metadata_column_fold_reports_warning() -> None:
    html = (
        "<table><thead><tr><th>Name</th><th>Source</th><th>Notes</th><th>Type</th></tr></thead>"
        "<tbody><tr><td>A</td><td>https://example.com/a</td><td>ok</td><td>source</td></tr></tbody></table>"
    )
    warnings: list[str] = []
    rendered = maybe_wrap_wide_tables_in_html(html, warnings=warnings)
    assert warnings
    assert any("Source" in warning for warning in warnings)
    assert "<th>Notes</th>" in rendered


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
