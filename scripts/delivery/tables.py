"""HTML table cleanup and layout decisions for generated reports."""

from __future__ import annotations

import re


def maybe_wrap_wide_tables_in_html(html: str) -> str:
    """Normalize dense tables and split wide tables into readable chunks."""

    def plain_text(value: str) -> str:
        value = re.sub(r"<br\s*/?>", " / ", value, flags=re.I)
        value = re.sub(r"<[^>]+>", "", value)
        return re.sub(r"\s+", " ", value).strip()

    def is_placeholder(value: str) -> bool:
        text = plain_text(value)
        return not text or text in {
            "#", "—", "-", "–", "--", "——", "— —", "N/A", "n/a", "NA",
            "TBD", "tbd", "/", "｜",
        } or bool(re.fullmatch(r"#\d+", text))

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

    def sanitize_table(headers: list[str], rows: list[list[str]]) -> tuple[list[str], list[list[str]]]:
        min_row_width = min((len(row) for row in rows), default=len(headers))
        if rows and len(headers) == min_row_width + 1 and is_placeholder(headers[0]):
            headers = headers[1:]
        width = min(len(headers), min((len(row) for row in rows), default=len(headers)))
        headers = headers[:width]
        rows = [row[:width] for row in rows]
        keep: list[int] = []
        metadata_cols: list[int] = []
        for index in range(width):
            header_text = plain_text(headers[index])
            column_values = [plain_text(row[index]) for row in rows if index < len(row)]
            if is_placeholder(header_text) and all(is_placeholder(value) for value in column_values):
                continue
            if is_metadata_header(header_text):
                urlish = [value for value in column_values if is_urlish(value)]
                if len(urlish) >= max(1, int(len(column_values) * 0.6)):
                    metadata_cols.append(index)
            keep.append(index)

        non_meta_keep = [index for index in keep if index not in metadata_cols]
        if len(non_meta_keep) >= 2 and len(keep) >= 4:
            keep = non_meta_keep
        if not keep:
            keep = list(range(width))

        headers = [headers[index] for index in keep]
        rows = [[row[index] for index in keep] for row in rows]
        placeholder_headers = [index for index, header in enumerate(headers) if is_placeholder(header)]
        if placeholder_headers and len(headers) > 1:
            keep = [index for index in range(len(headers)) if index not in placeholder_headers]
            headers = [headers[index] for index in keep]
            rows = [[row[index] for index in keep] for row in rows]

        cleaned_rows: list[list[str]] = []
        for row in rows:
            cleaned = ["" if is_placeholder(cell) else normalize_cell_html(cell.strip()) for cell in row]
            if any(plain_text(cell) for cell in cleaned):
                cleaned_rows.append(cleaned)
        return headers, cleaned_rows

    def build_table(headers: list[str], rows: list[list[str]]) -> str:
        parts = ["<table><thead><tr>"]
        parts.extend(f"<th>{header.strip() or '字段'}</th>" for header in headers)
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

    def replace_table(match: re.Match[str]) -> str:
        table_html = match.group(0)
        headers = re.findall(r"<th[^>]*>(.*?)</th>", table_html, flags=re.S | re.I)
        row_chunks = re.findall(r"<tr[^>]*>(.*?)</tr>", table_html, flags=re.S | re.I)
        body_rows: list[list[str]] = []
        cell_texts: list[str] = []
        for row in row_chunks[1:]:
            cells = re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", row, flags=re.S | re.I)
            if cells:
                body_rows.append(cells)
                cell_texts.extend(cells)
        if not headers or not body_rows:
            return f'<div class="table-wrap">{table_html}</div>'

        headers, body_rows = sanitize_table(headers, body_rows)
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

    return re.sub(r"<table[\s\S]*?</table>", replace_table, html, flags=re.I)
