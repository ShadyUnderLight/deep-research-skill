#!/usr/bin/env python3
"""Issue #438 F4 review: markdown_to_html keeps its public compatibility facade.

The module documents that the public script path and the historical helper
names remain stable for existing callers.  A lint pass must not silently strip
those re-exports, so this test locks the module-level public surface.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import markdown_to_html as m  # noqa: E402

PUBLIC_NAMES = [
    "build_html",
    "convert",
    "process_markdown",
    "style_generated_html",
    "sanitize_html",
    "repair_markdown_tables",
    "maybe_wrap_wide_tables_in_html",
    "extract_cover_meta",
    "normalize_text_for_pdf",
    "atomic_write_text",
    "paths_collide",
    "BASE_CSS",
    "REPORT_THEME_CSS",
]


def test_all_public_names_are_re_exported():
    missing = [name for name in PUBLIC_NAMES if not hasattr(m, name)]
    assert not missing, f"markdown_to_html facade lost public names: {missing}"


def test_all_lists_the_public_names():
    declared = set(getattr(m, "__all__", []))
    missing = [name for name in PUBLIC_NAMES if name not in declared]
    assert not missing, f"__all__ is missing public names: {missing}"


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
