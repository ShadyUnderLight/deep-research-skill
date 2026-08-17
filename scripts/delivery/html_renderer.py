"""Markdown parser, HTML post-processing, and document renderer."""

from __future__ import annotations

import html
import re

import markdown

from .normalization import normalize_text_for_pdf
from .sanitizer import sanitize_html
from .table_repair import repair_markdown_tables
from .tables import maybe_wrap_wide_tables_in_html


def build_html(
    title: str,
    body_html: str,
    *,
    base_css: str,
    report_theme_css: str,
    cover_title: str = "",
    cover_subtitle: str = "",
    cover_meta: str = "",
    meta_lines: list[str] | None = None,
) -> str:
    """Wrap sanitized body HTML in the complete report document."""

    title = html.escape(title)
    cover_title = html.escape(cover_title)
    cover_subtitle = html.escape(cover_subtitle)
    if meta_lines is not None:
        cover_meta = "<br>".join(html.escape(line) for line in meta_lines)
    elif cover_meta:
        parts = re.split(r"<br\s*/?>", cover_meta, flags=re.I)
        cover_meta = "<br>".join(html.escape(part) for part in parts)

    cover_block = ""
    body_class = "has-cover" if cover_title else ""
    if cover_title:
        cover_block = f"""
<div class="cover">
  <div class="cover-tag">Deep Research Report · 深度研究报告</div>
  <h1>{cover_title}</h1>
  <h2>{cover_subtitle}</h2>
  <div class="cover-line"></div>
  <div class="cover-meta">{cover_meta}</div>
</div>
"""
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<style>{base_css}\n{report_theme_css}</style>
</head>
<body class="{body_class}">
{cover_block}
{body_html}
</body>
</html>"""


def _convert_front_page_summary(html_text: str) -> str:
    thesis_labels = r"(?:Core thesis|Thesis|Bottom line|Bottom-line judgment|Judgment|Recommendation|结论|核心判断|核心结论|建议)"
    html_text = re.sub(
        rf"<p><strong>({thesis_labels})[:：]</strong>\s*(.*?)</p>",
        r'<div class="front-page-summary"><div class="front-page-thesis"><strong>\1:</strong> \2</div></div>',
        html_text,
        flags=re.I | re.S,
    )
    return re.sub(
        r'<div class="front-page-summary">\s*(<div class="front-page-thesis">.*?</div>)\s*</div>\s*(<ul>.*?</ul>)',
        r'<div class="front-page-summary">\1\2</div>',
        html_text,
        flags=re.S,
    )


TAKEAWAY_LABEL_PATTERNS = {
    "section judgment": r"(?:Section judgment|Judgment|本节判断|核心判断|结论判断)",
    "main driver": r"(?:Main driver|Core driver|核心驱动|主要驱动)",
    "main risk": r"(?:Main risk|Core risk|核心风险|主要风险)",
    "key unknown": r"(?:Key unknown|Main unknown|关键未知项|主要未知项|未知项)",
    "what would change this view": r"(?:What would change this view|What would change the conclusion|改变判断的条件|什么会改变这一判断|什么会改变结论)",
}


def _convert_takeaway_cards(html_text: str) -> str:
    pattern = re.compile(r"<p><strong>([^<]{1,80})[:：]</strong>\s*(.*?)</p>", flags=re.I | re.S)
    matches = list(pattern.finditer(html_text))
    if not matches:
        return html_text

    def normalize_label(label: str) -> tuple[str | None, str]:
        raw = re.sub(r"<[^>]+>", "", label).strip()
        for canonical, expression in TAKEAWAY_LABEL_PATTERNS.items():
            if re.fullmatch(expression, raw, flags=re.I):
                return canonical, raw
        return None, raw

    rebuilt: list[str] = []
    last = 0
    index = 0
    while index < len(matches):
        match = matches[index]
        canonical, _ = normalize_label(match.group(1))
        if not canonical:
            index += 1
            continue
        group: list[tuple[re.Match[str], str, str, str]] = []
        end = index
        while end < len(matches):
            candidate = matches[end]
            candidate_canonical, raw = normalize_label(candidate.group(1))
            if not candidate_canonical:
                break
            if end > index and candidate.start() != matches[end - 1].end():
                between = html_text[matches[end - 1].end():candidate.start()]
                if re.sub(r"\s+", "", between):
                    break
            group.append((candidate, candidate_canonical, raw, candidate.group(2).strip()))
            end += 1
            if len(group) >= 5:
                break
        if len(group) < 2:
            index += 1
            continue
        rebuilt.append(html_text[last:group[0][0].start()])
        cards = [
            f'<div class="takeaway-card"><span class="takeaway-card-label">{raw}</span>'
            f'<span class="takeaway-card-value">{value}</span></div>'
            for _, _, raw, value in group
        ]
        rebuilt.append('<div class="takeaway-grid">' + "".join(cards) + "</div>")
        last = group[-1][0].end()
        index = end
    rebuilt.append(html_text[last:])
    return "".join(rebuilt)


def _mark_methods_notes(html_text: str) -> str:
    return re.sub(
        r"<p><strong>((?:Methods note|Method note|方法说明|研究方式|证据分级|数字角色))[:：]</strong>\s*(.*?)</p>",
        r'<div class="methods-note"><strong>\1:</strong> \2</div>',
        html_text,
        flags=re.I | re.S,
    )


def style_generated_html(html_text: str) -> str:
    """Apply report-specific post-processing before sanitization."""

    html_text = re.sub(
        r"<(?:p|li|div)>\s*[^<]*(?:优先拆成主题子表|退化成长卡片列表|该表信息较密)[^<]*</(?:p|li|div)>",
        "",
        html_text,
        flags=re.I,
    )
    html_text = maybe_wrap_wide_tables_in_html(html_text)
    html_text = re.sub(
        r"<li>\s*(<(?:h1|h2|h3|h4)[^>]*>.*?</(?:h1|h2|h3|h4)>)\s*</li>",
        r"\1",
        html_text,
        flags=re.S | re.I,
    )
    html_text = re.sub(
        r'<li>\s*(<div class="callout[^"]*">.*?</div>)\s*</li>',
        r"\1",
        html_text,
        flags=re.S | re.I,
    )
    html_text = re.sub(r"<p>\s*(?:#\d+|[—–-])\s*</p>", "", html_text, flags=re.I)

    cjk = r"\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff"

    def heading_repl(match: re.Match[str]) -> str:
        tag, inner = match.group(1), match.group(2)
        inner = re.sub(rf"([{cjk}])\s+([{cjk}])", r"\1\2", inner)
        inner = re.sub(rf"([{cjk}])\s+([，。！？；：、])", r"\1\2", inner)
        inner = re.sub(r"\s+", " ", inner).strip()
        return f"<{tag}>{inner}</{tag}>"

    html_text = re.sub(r"<(h[1-4])>(.*?)</\1>", heading_repl, html_text, flags=re.S | re.I)

    def quote_repl(match: re.Match[str]) -> str:
        inner = match.group(1).strip()
        plain = re.sub(r"<[^>]+>", "", inner).strip()
        if plain.startswith(("预测:", "预测：", "风险:", "风险：")):
            return f'<div class="callout callout-inference">{inner}</div>'
        return f"<blockquote>{inner}</blockquote>"

    return re.sub(r"<blockquote>\s*(.*?)\s*</blockquote>", quote_repl, html_text, flags=re.S | re.I)


def process_markdown(md_text: str) -> str:
    """Convert normalized Markdown into sanitized, styled body HTML."""

    repaired = repair_markdown_tables(md_text)
    generated = markdown.markdown(
        repaired,
        extensions=["extra", "tables", "fenced_code", "sane_lists", "nl2br"],
        output_format="html5",
    )
    return sanitize_html(style_generated_html(generated))
