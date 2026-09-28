#!/usr/bin/env python3
"""Issue #438 F6: data-flow doc parser must respect visible-Markdown boundaries.

A heading that only appears inside a fenced code block, an HTML comment/block,
ordinary prose, or at the wrong heading level (### vs ##) must NOT satisfy a
real document section.  Only a real, visible heading line counts.

Reuses the shared visible-Markdown parser (sanitize_visible_markdown, issues
#433/#435) rather than introducing a separate Markdown AST dependency.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import validate_data_flows as df  # noqa: E402


def test_fenced_heading_is_not_a_real_section() -> None:
    text = (
        "# Title\n\n"
        "## Real Section\n\n"
        "visible content\n\n"
        "```markdown\n"
        "## Hidden Section\n"
        "this is code, not a heading\n"
        "```\n"
    )
    assert df.extract_section(text, "## Hidden Section") == ""
    assert df.check_required_sections(text, ["## Hidden Section"], "X") != []


def test_html_comment_heading_is_not_a_real_section() -> None:
    text = (
        "# Title\n\n"
        "<!--\n## Hidden Section\n-->\n\n"
        "## Real Section\n\n"
        "content\n"
    )
    assert df.extract_section(text, "## Hidden Section") == ""
    assert df.check_required_sections(text, ["## Hidden Section"], "X") != []


def test_prose_mention_is_not_a_real_section() -> None:
    text = (
        "# Title\n\n"
        "## Real Section\n\n"
        "see ## Hidden Section above for details\n\n"
        "## Another\n\n"
        "x\n"
    )
    # The same string appears in prose, not as a heading line.
    assert df.extract_section(text, "## Hidden Section") == ""
    assert df.check_required_sections(text, ["## Hidden Section"], "X") != []


def test_wrong_hierarchy_is_not_matched_as_h2() -> None:
    text = "# Title\n\n### Subsection\n\ncontent\n"
    # A ### subsection must not satisfy a required ## heading.
    assert df.check_required_sections(text, ["## Subsection"], "X") != []


def test_visible_heading_is_a_real_section() -> None:
    text = "# Title\n\n## Real Section\n\ncontent\n"
    body = df.extract_section(text, "## Real Section")
    assert "content" in body
    assert df.check_required_sections(text, ["## Real Section"], "X") == []


def test_duplicate_visible_sections_resolves_first() -> None:
    text = "# Title\n\n## Dup\n\nfirst\n\n## Dup\n\nsecond\n"
    body = df.extract_section(text, "## Dup")
    assert "first" in body
    assert "second" not in body


def test_body_includes_h3_subheadings_until_next_h2() -> None:
    text = (
        "# Title\n\n"
        "## Section\n\n"
        "intro\n\n"
        "### Sub\n\nsub body\n\n"
        "## Next\n\n"
        "tail\n"
    )
    body = df.extract_section(text, "## Section")
    assert "intro" in body
    assert "sub body" in body
    assert "tail" not in body


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
