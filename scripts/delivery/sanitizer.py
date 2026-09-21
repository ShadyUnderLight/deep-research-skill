"""HTML safety boundary for generated report body content."""

from __future__ import annotations


def sanitize_html(html_text: str) -> str:
    """Strip dangerous tags, attributes, and URL schemes from body HTML."""

    import nh3

    return nh3.clean(
        html_text,
        tags={
            "p", "br", "hr", "h1", "h2", "h3", "h4", "h5", "h6",
            "ul", "ol", "li", "table", "caption", "colgroup", "col",
            "thead", "tbody", "tfoot", "tr", "th", "td",
            "a", "strong", "em", "b", "i", "u", "s", "code", "pre", "blockquote",
            "div", "span", "dl", "dt", "dd", "abbr", "cite", "wbr",
        },
        attributes={
            "a": {"href", "title"},
            "*": {"class", "id"},
            "colgroup": {"span"},
            "col": {"span"},
            "td": {"colspan", "rowspan"},
            "th": {"colspan", "rowspan", "scope"},
        },
        url_schemes={"http", "https", "mailto"},
    )
