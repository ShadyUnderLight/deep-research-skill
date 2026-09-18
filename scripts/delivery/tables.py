"""HTML table cleanup and layout decisions for generated reports."""

from __future__ import annotations

import re
from html.parser import HTMLParser

# Both table location (``_TableSpanCollector``) and table structure parsing
# (``_TableStructureParser``) use the stdlib HTML parser: depth-aware spans
# keep nested tables intact, and quoted attribute values can no longer
# truncate a cell or hide a colspan/rowspan (issue #435 review rounds 1-3).


# Rebuilding a table with more than this many columns is never useful for a
# reader-facing PDF and would let a tiny input amplify memory/CPU, so
# oversized spans fail closed to the original markup (issue #435 review
# round 3).
MAX_TABLE_SPAN = 64


def _span_attrs(attributes: dict[str, str | None]) -> dict[str, int] | None:
    """Return normalized colspan/rowspan values, or None when unsupported.

    ``rowspan`` values other than the default ``1`` (including the legal
    ``rowspan="0"``) cannot be represented by the rebuild path, so they are
    kept as spans and make the table unsupported downstream.  A colspan
    beyond :data:`MAX_TABLE_SPAN` is rejected outright.
    """

    spans: dict[str, int] = {}
    for name in ("colspan", "rowspan"):
        raw = attributes.get(name)
        if raw is None:
            continue
        try:
            value = int(raw)
        except (TypeError, ValueError):
            continue
        if name == "rowspan":
            if value != 1:
                spans[name] = value
        elif value > 1:
            if value > MAX_TABLE_SPAN:
                return None
            spans[name] = value
    return spans


class _TableStructureParser(HTMLParser):
    """Parse one table into sections/rows with byte-accurate cell HTML.

    Start tags, attributes, and cell boundaries all come from the stdlib
    parser, so quoted ``>`` values, single/double/unquoted attributes, and
    unclosed cells follow HTML rules instead of a regex (issue #435 review
    round 2).
    """

    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.rows: list[tuple[str | None, list[tuple[str, dict[str, int], str]]]] = []
        self.unsupported = False
        self._line_starts = [0]
        self._section: str | None = None
        self._row: list[tuple[str, dict[str, int], str]] | None = None
        self._cell: tuple[str, dict[str, int], int] | None = None
        self._table_depth = 0

    def feed(self, data: str) -> None:
        self._line_starts = [0]
        for index, char in enumerate(data):
            if char == "\n":
                self._line_starts.append(index + 1)
        super().feed(data)

    def _offset(self) -> int:
        line, column = self.getpos()
        return self._line_starts[line - 1] + column

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self._table_depth += 1
            if self._table_depth > 1:
                self.unsupported = True
            return
        if tag in ("thead", "tbody", "tfoot"):
            self._section = "thead" if tag == "thead" else "tbody"
            return
        if tag == "tr":
            if self._row is not None:
                self.unsupported = True
            self._row = []
            return
        if tag in ("td", "th"):
            if self._row is None or self._cell is not None:
                self.unsupported = True
                return
            spans = _span_attrs(dict(attrs))
            if spans is None:
                self.unsupported = True
                return
            start_tag = self.get_starttag_text() or ""
            self._cell = (tag, spans, self._offset() + len(start_tag))

    def handle_startendtag(self, tag, attrs):
        if tag in ("td", "th"):
            self.unsupported = True

    def handle_endtag(self, tag):
        if tag == "table":
            self._table_depth -= 1
            return
        if tag in ("td", "th"):
            if self._cell is None:
                self.unsupported = True
                return
            cell_tag, spans, content_start = self._cell
            content = self.rawdata[content_start:self._offset()]
            if self._row is None:
                self.unsupported = True
            else:
                self._row.append((cell_tag, spans, content))
            self._cell = None
            return
        if tag == "tr":
            if self._row is None or self._cell is not None:
                self.unsupported = True
            else:
                self.rows.append((self._section, self._row))
            self._row = None
            return
        if tag in ("thead", "tbody", "tfoot"):
            self._section = None


def _parse_table_rows(
    table_html: str,
) -> list[tuple[str | None, list[tuple[str, dict[str, int], str]]]] | None:
    parser = _TableStructureParser()
    try:
        parser.feed(table_html)
        parser.close()
    except Exception:
        return None
    if parser.unsupported or parser._cell is not None or parser._row is not None:
        return None
    return parser.rows


class _TableSpanCollector(HTMLParser):
    """Collect complete top-level ``<table>...</table>`` spans.

    A depth counter keeps nested tables inside the outer span, so the
    replacement never receives a half table cut at an inner ``</table>``
    (issue #435 review round 3).
    """

    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.spans: list[tuple[int, int]] = []
        self._line_starts = [0]
        self._depth = 0
        self._start: int | None = None

    def feed(self, data: str) -> None:
        self._line_starts = [0]
        for index, char in enumerate(data):
            if char == "\n":
                self._line_starts.append(index + 1)
        super().feed(data)

    def _offset(self) -> int:
        line, column = self.getpos()
        return self._line_starts[line - 1] + column

    def handle_starttag(self, tag, attrs):
        if tag != "table":
            return
        if self._depth == 0:
            self._start = self._offset()
        self._depth += 1

    def handle_endtag(self, tag):
        if tag != "table" or self._depth == 0:
            return
        self._depth -= 1
        if self._depth != 0 or self._start is None:
            return
        end = self.rawdata.find(">", self._offset())
        if end != -1:
            self.spans.append((self._start, end + 1))
        self._start = None


def _replace_top_level_tables(html: str, replacement) -> str:
    parser = _TableSpanCollector()
    try:
        parser.feed(html)
        parser.close()
    except Exception:
        return html
    if not parser.spans:
        return html
    pieces: list[str] = []
    last = 0
    for start, end in parser.spans:
        pieces.append(html[last:start])
        pieces.append(replacement(html[start:end]))
        last = end
    pieces.append(html[last:])
    return "".join(pieces)


def _expand_cells(
    cells: list[tuple[str, dict[str, int], str]],
) -> tuple[list[str], list[bool], bool]:
    """Expand colspan slots and flag unsupported rowspan layouts.

    Returns ``(values, synthetic, has_rowspan)``: ``synthetic[i]`` marks a
    slot created by colspan expansion, which later padding also uses, so
    placeholder-column folding can never delete a data-bearing slot.
    """

    values: list[str] = []
    synthetic: list[bool] = []
    has_rowspan = False
    for _, attrs, inner in cells:
        if attrs.get("rowspan", 1) != 1:
            has_rowspan = True
        values.append(inner)
        synthetic.append(False)
        for _ in range(attrs.get("colspan", 1) - 1):
            values.append("")
            synthetic.append(True)
    return values, synthetic, has_rowspan


def extract_table_structure(
    table_html: str,
) -> tuple[list[str], list[bool], list[list[str]]] | None:
    """Extract ``(headers, synthetic_header_slots, body_rows)`` from a table.

    Returns ``None`` when the table cannot be rebuilt without losing
    structure (no ``<th>`` header row, rowspan cells, multi-row headers, or
    no body rows); callers then keep the original markup untouched.
    """

    parsed_rows = _parse_table_rows(table_html)
    if parsed_rows is None:
        return None

    if any(section == "thead" for section, _ in parsed_rows):
        header_rows = [cells for section, cells in parsed_rows if section == "thead"]
        if len(header_rows) != 1:
            return None
        header_cells = header_rows[0]
        body_cell_rows = [cells for section, cells in parsed_rows if section != "thead"]
    else:
        if not parsed_rows:
            return None
        header_cells = parsed_rows[0][1]
        if not any(tag == "th" for tag, _, _ in header_cells):
            return None
        body_cell_rows = [cells for _, cells in parsed_rows[1:]]

    if not header_cells or not body_cell_rows:
        return None

    headers, header_synthetic, header_has_rowspan = _expand_cells(header_cells)
    rows: list[list[str]] = []
    has_rowspan = header_has_rowspan
    for cells in body_cell_rows:
        values, _, row_has_rowspan = _expand_cells(cells)
        has_rowspan = has_rowspan or row_has_rowspan
        if not values:
            return None
        rows.append(values)
    if has_rowspan or not headers:
        return None
    return headers, header_synthetic, rows


def maybe_wrap_wide_tables_in_html(
    html: str,
    *,
    warnings: list[str] | None = None,
    fold_metadata_columns: bool = False,
) -> str:
    """Normalize dense tables and split wide tables into readable chunks.

    Data-bearing columns are never deleted by default: a column is only
    dropped when both its header and every cell are strictly empty layout
    (whitespace or punctuation), never when they hold ``N/A``/``TBD``/``#1``
    style status values.  Metadata/URL columns are folded only when
    ``fold_metadata_columns`` is explicitly enabled, and every drop/fold is
    reported through ``warnings`` (issue #435).
    """

    warning_sink = warnings if warnings is not None else []

    def plain_text(value: str) -> str:
        value = re.sub(r"<br\s*/?>", " / ", value, flags=re.I)
        value = re.sub(r"<[^>]+>", "", value)
        return re.sub(r"\s+", " ", value).strip()

    def is_empty_layout_cell(value: str) -> bool:
        """True only for whitespace and pure layout punctuation.

        Semantic marker values such as ``N/A``, ``TBD``, or ``#1`` are data,
        not emptiness: they must never justify deleting a column or be
        blanked out of a cell (issue #435 review round 2).
        """

        text = plain_text(value)
        return not text or text in {"#", "—", "-", "–", "--", "——", "— —", "/", "｜"}

    def normalize_meta_key(value: str) -> str:
        return re.sub(r"[\s:：\-_]+", "", plain_text(value).lower())

    def is_urlish(value: str) -> bool:
        return bool(re.search(r"(https?://|www\.)", plain_text(value), flags=re.I))

    def is_metadata_header(value: str) -> bool:
        return normalize_meta_key(value) in {
            "来源", "信息来源", "出处", "参考", "参考来源", "source", "sources",
            "citation", "citations", "url", "urls", "link", "links", "参考链接", "链接",
        }

    def soft_wrap_url_text(value: str) -> str:
        value = re.sub(r"(?<=/)(?=[^/])", "<wbr>", value)
        return re.sub(r"([?&=#%])", r"\1<wbr>", value)

    def normalize_cell_html(cell: str) -> str:
        cleaned = cell.strip()

        def anchor_repl(match: re.Match[str]) -> str:
            href = match.group(1)
            attrs = match.group(2) or ""
            text = match.group(3)
            if plain_text(text) == href:
                text = soft_wrap_url_text(text)
            return f'<a href="{href}"{attrs}>{text}</a>'

        cleaned = re.sub(
            r'<a\s+href="([^"]+)"([^>]*)>(.*?)</a>',
            anchor_repl,
            cleaned,
            flags=re.S | re.I,
        )
        if is_urlish(cleaned) and "<a " not in cleaned.lower():
            cleaned = f'<span class="url-soft">{soft_wrap_url_text(cleaned)}</span>'
        return cleaned

    def sanitize_table(
        headers: list[str],
        header_synthetic: list[bool],
        rows: list[list[str]],
    ) -> tuple[list[str], list[list[str]]]:
        if not rows:
            return headers, rows

        min_row_width = min(len(row) for row in rows)
        if (
            len(headers) == min_row_width + 1
            and is_empty_layout_cell(headers[0])
            and not header_synthetic[0]
            and all(is_empty_layout_cell(row[0]) for row in rows)
        ):
            warning_sink.append("table column dropped: leading empty column (no data)")
            headers = headers[1:]
            header_synthetic = header_synthetic[1:]
            rows = [row[1:] for row in rows]

        width = max(len(headers), *(len(row) for row in rows))
        if width > len(headers):
            headers = headers + [""] * (width - len(headers))
            header_synthetic = header_synthetic + [True] * (width - len(header_synthetic))
        rows = [row + [""] * (width - len(row)) for row in rows]
        protected = list(header_synthetic)

        keep: list[int] = []
        metadata_cols: list[int] = []
        for index in range(width):
            header_text = plain_text(headers[index])
            column_values = [plain_text(row[index]) for row in rows]
            if not protected[index]:
                if is_empty_layout_cell(header_text) and all(
                    is_empty_layout_cell(value) for value in column_values
                ):
                    warning_sink.append(
                        f"table column dropped: empty column {index + 1} (no data)"
                    )
                    continue
                if fold_metadata_columns and is_metadata_header(header_text):
                    urlish = [value for value in column_values if is_urlish(value)]
                    if len(urlish) >= max(1, int(len(column_values) * 0.6)):
                        metadata_cols.append(index)
            keep.append(index)

        if metadata_cols:
            non_meta_keep = [index for index in keep if index not in metadata_cols]
            if len(non_meta_keep) >= 2 and len(keep) >= 4:
                for index in metadata_cols:
                    warning_sink.append(
                        f"table column folded: metadata column {plain_text(headers[index])!r}"
                    )
                keep = non_meta_keep
        if not keep:
            keep = list(range(width))

        headers = [headers[index] for index in keep]
        rows = [[row[index] for index in keep] for row in rows]

        cleaned_rows: list[list[str]] = []
        for row in rows:
            cleaned = ["" if is_empty_layout_cell(cell) else normalize_cell_html(cell.strip()) for cell in row]
            if any(plain_text(cell) for cell in cleaned):
                cleaned_rows.append(cleaned)
        return headers, cleaned_rows

    def build_table(headers: list[str], rows: list[list[str]]) -> str:
        parts = ["<table><thead><tr>"]
        parts.extend(f"<th>{header.strip()}</th>" for header in headers)
        parts.append("</tr></thead><tbody>")
        for row in rows:
            parts.append("<tr>")
            parts.extend(f'<td>{cell.strip() or ""}</td>' for cell in row)
            parts.append("</tr>")
        parts.append("</tbody></table>")
        return "".join(parts)

    def split_table(headers: list[str], rows: list[list[str]], max_cols: int = 4) -> list[str]:
        if len(headers) <= max_cols:
            return [build_table(headers, rows)]
        chunks: list[str] = []
        anchor_first = not is_metadata_header(headers[0])
        if anchor_first and max_cols >= 3:
            chunk_size = max_cols - 1
            for start in range(1, len(headers), chunk_size):
                end = min(start + chunk_size, len(headers))
                sub_headers = [headers[0]] + headers[start:end]
                sub_rows = [[row[0]] + row[start:end] for row in rows]
                chunks.append(build_table(sub_headers, sub_rows))
            return chunks
        for start in range(0, len(headers), max_cols):
            end = min(start + max_cols, len(headers))
            chunks.append(build_table(headers[start:end], [row[start:end] for row in rows]))
        return chunks

    def replace_table(table_html: str) -> str:
        structure = extract_table_structure(table_html)
        if structure is None:
            return f'<div class="table-wrap">{table_html}</div>'

        headers, header_synthetic, body_rows = structure
        cell_texts = [cell for row in body_rows for cell in row]
        headers, body_rows = sanitize_table(headers, header_synthetic, body_rows)
        if not headers or not body_rows:
            return f'<div class="table-wrap">{table_html}</div>'

        dense = len(headers) >= 4
        long_cells = any(len(plain_text(cell)) > 36 for cell in cell_texts)
        many_rows = len(body_rows) >= 6
        source_like = sum(1 for header in headers if is_metadata_header(header)) >= max(1, len(headers) // 2)
        source_class = " table-wrap-source" if source_like else ""

        if len(headers) >= 5 or (dense and long_cells) or (dense and many_rows):
            tables = split_table(headers, body_rows)
            wrapped = "".join(f'<div class="split-table">{table}</div>' for table in tables)
            return f'<div class="table-wrap wide-table split-table-group{source_class}">{wrapped}</div>'

        compact_html = build_table(headers, body_rows)
        if dense or long_cells:
            return f'<div class="table-wrap wide-table{source_class}">{compact_html}</div>'
        return f'<div class="table-wrap{source_class}">{compact_html}</div>'

    return _replace_top_level_tables(html, replace_table)
