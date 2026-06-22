#!/usr/bin/env python3
"""Regression + property-based tests for validate_figure_references.py.

Test strategy:
- Contract tests: explicit fixtures with expected pass/fail (subprocess style)
- Property tests: Hypothesis strategies asserting invariants

Usage:
    python scripts/test_figure_reference_validator.py

Expected BEFORE implementation: ALL FAIL (subprocess tests: script not found)
Expected AFTER implementation:  ALL PASS
"""

from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from pathlib import Path

# Hypothesis for property-based testing
from hypothesis import assume, given, strategies as st

# ── Paths ──────────────────────────────────────────────────────────────────

SCRIPT_DIR = Path(__file__).resolve().parent
VALIDATOR = str(SCRIPT_DIR / "validate_figure_references.py")

# ── Helpers ────────────────────────────────────────────────────────────────


def run_validator(text: str) -> subprocess.CompletedProcess:
    """Run the validator as a subprocess, return CompletedProcess."""
    with tempfile.TemporaryDirectory() as d:
        path = Path(d) / "report.md"
        path.write_text(text, encoding="utf-8")
        return subprocess.run(
            [sys.executable, VALIDATOR, str(path)],
            capture_output=True, text=True,
        )


def expect_pass(name: str, text: str) -> None:
    result = run_validator(text)
    assert result.returncode == 0, (
        f"{name}: expected pass (exit 0), got {result.returncode}\n"
        f"stdout: {result.stdout}\nstderr: {result.stderr}"
    )
    print(f"  PASS  {name}")


def expect_fail(name: str, text: str) -> None:
    result = run_validator(text)
    assert result.returncode == 2, (
        f"{name}: expected fail (exit 2), got {result.returncode}\n"
        f"stdout: {result.stdout}\nstderr: {result.stderr}"
    )
    # A real failure should contain an error message
    assert "✗" in result.stdout or "error" in result.stdout.lower() or "Error" in result.stdout, (
        f"{name}: expected error message in stdout:\n{result.stdout}"
    )
    print(f"  PASS  {name}")


# ── Fixtures ───────────────────────────────────────────────────────────────

NO_FIGURES = """\
# Test Report

This report has no figures at all.
No references, no images, no Mermaid.
"""

VALID_FIGURES = """\
# Test Report

As shown in 图1, the architecture is clear.

```mermaid
graph TD
    A-->B
```

图1: System architecture diagram

Further analysis is in 图2.

![Performance chart](./charts/perf.png)

图2: Performance comparison
"""

VALID_ENGLISH = """\
# Report

As shown in Figure 1, the trend is clear.

```mermaid
graph LR
    X-->Y
```

**Figure 1:** Architecture overview

See Figure 2 for details.

![Benchmark](./bench.png)

**Figure 2:** Benchmark results
"""

MISSING_FIGURE_CN = """\
# Report

As shown in 图1, the trend is clear.
See also 图2 for details.

```mermaid
graph TD
    A-->B
```

图1: Architecture diagram

Note: 图2 is referenced but no entity exists for it.
"""

MISSING_FIGURE_EN = """\
# Report

As shown in Figure 1, the trend is clear.
Figure 2 also supports this conclusion.

```mermaid
graph TD
    A-->B
```

**Figure 1:** Architecture diagram

Note: Figure 2 is referenced but no entity exists.
"""

DUPLICATE_CAPTION = """\
# Report

Analysis in 图1.

```mermaid
graph TD
    A-->B
```

图1: First caption
图1: Second duplicate caption
"""

GENERIC_NO_FIGURE = """\
# Report

如下图所示，the trend is clear.

No figure follows this reference.
"""

MERMAID_NO_CAPTION = """\
# Report

Analysis in 图1.

```mermaid
graph TD
    A-->B
```

No caption follows the mermaid block.
"""

FIGURE_GAP = """\
# Report

See 图1 and 图3 for details.

```mermaid
graph TD
    A-->B
```

图1: Architecture

![Chart](./chart.png)

**Figure 3:** Results

Note: 图2 is never defined — there's a gap.
"""

CAPTION_WITH_REFERENCE_IN_CODE_FENCE = """\
# Report

Code example:

```python
# 图1 is inside a code fence, should be ignored
result = process(data)
```

The actual 图1 is below.

```mermaid
graph TD
    A-->B
```

图1: Actual diagram
"""

# ── Property-based test strategies ─────────────────────────────────────────


@st.composite
def figure_reports(draw):
    """Strategy: generate valid markdown reports with consistent figures."""
    num_figures = draw(st.integers(min_value=0, max_value=5))
    lines = ["# Property Test Report\n"]
    
    figure_blocks = []
    for i in range(1, num_figures + 1):
        # Optionally reference the figure in body text first
        if draw(st.booleans()):
            ref_style = draw(st.sampled_from([
                f"图{i}",
                f"图 {i}",
                f"Figure {i}",
                f"Fig. {i}",
                f"见图{i}",
            ]))
            lines.append(f"As shown in {ref_style}, the result is clear.\n")
        
        # Optionally add a Mermaid block or image
        entity_type = draw(st.sampled_from(["mermaid", "image"]))
        if entity_type == "mermaid":
            lines.append("```mermaid\ngraph TD\n    A-->B\n```\n")
        else:
            lines.append(f"![Figure {i}](./fig{i}.png)\n")
        
        # Add caption
        caption_style = draw(st.sampled_from([
            f"图{i}: ",
            f"**Figure {i}:** ",
            f"**Fig. {i}:** ",
        ]))
        lines.append(f"{caption_style}Caption for figure {i}\n")
        
        figure_blocks.append(i)
    
    return "".join(lines)


@given(figure_reports())
def test_property_valid_report_has_no_errors(report):
    """Property: Any valid report generated by the strategy should pass."""
    result = run_validator(report)
    assert result.returncode == 0, (
        f"Expected pass for valid report, got exit {result.returncode}\n"
        f"stdout: {result.stdout}"
    )


@given(st.text())
def test_property_arbitrary_text_does_not_crash(text):
    """Property: The validator must never crash on arbitrary input."""
    result = run_validator(text)
    assert result.returncode in (0, 2), (
        f"Unexpected exit code {result.returncode} for arbitrary text\n"
        f"stderr: {result.stderr}"
    )


@st.composite
def reports_with_missing_figure(draw):
    """Strategy: reports that reference a figure without defining it.
    
    Ensures entity_count < ref_num so the validator produces an error
    (not a warning about missing explicit caption).
    """
    # ref_num must be > entity_count. We'll generate 0 or 1 entities.
    generate_entity = draw(st.booleans())
    entity_count = 1 if generate_entity else 0
    ref_num = draw(st.integers(min_value=entity_count + 1, max_value=5))
    
    # Pick a ref style
    ref = draw(st.sampled_from([
        f"图{ref_num}",
        f"Figure {ref_num}",
        f"Fig. {ref_num}",
    ]))
    
    # Build report
    lines = ["# Test\n"]
    lines.append(f"As shown in {ref}, the result is clear.\n")
    
    # Optionally add a different figure with a number that is < ref_num
    if generate_entity:
        other_num = draw(st.integers(min_value=1, max_value=ref_num - 1))
        lines.append("```mermaid\ngraph TD\n    Z-->W\n```\n")
        lines.append(f"图{other_num}: Other figure\n")
    
    return "".join(lines)


@given(reports_with_missing_figure())
def test_property_missing_figure_detected(report):
    """Property: Reports referencing undefined figures must fail."""
    result = run_validator(report)
    assert result.returncode == 2, (
        f"Expected fail for report with missing figure, got exit {result.returncode}\n"
        f"stdout: {result.stdout}"
    )


# ── Contract tests ─────────────────────────────────────────────────────────


def test_empty_markdown_passes():
    """No figures → no errors."""
    expect_pass("empty markdown", "")


def test_no_figures_passes():
    """Report with zero figure references should pass."""
    expect_pass("no figures", NO_FIGURES)


def test_valid_chinese_figures_passes():
    """Report with consistent Chinese figure references should pass."""
    expect_pass("valid Chinese figures", VALID_FIGURES)


def test_valid_english_figures_passes():
    """Report with consistent English figure references should pass."""
    expect_pass("valid English figures", VALID_ENGLISH)


def test_missing_chinese_figure_fails():
    """Report referencing 图2 but no entity for it should fail."""
    expect_fail("missing Chinese figure", MISSING_FIGURE_CN)


def test_missing_english_figure_fails():
    """Report referencing Figure 2 but no entity for it should fail."""
    expect_fail("missing English figure", MISSING_FIGURE_EN)


def test_duplicate_caption_fails():
    """Two captions claiming the same figure number should fail."""
    expect_fail("duplicate caption", DUPLICATE_CAPTION)


def test_code_fence_excludes_figure_ref():
    """图1 inside a code fence should be ignored; only the real 图1 counts."""
    # This should pass: the only real 图1 reference maps to the caption + mermaid
    expect_pass("code fence excludes ref", CAPTION_WITH_REFERENCE_IN_CODE_FENCE)


def test_generic_ref_no_figure_passes():
    """Generic 如下图所示 without a following figure → warning only (not blocking)."""
    # Warnings do not cause exit code 2
    result = run_validator(GENERIC_NO_FIGURE)
    # Should pass (exit 0) with warnings
    assert result.returncode == 0, (
        f"Generic ref expected pass (exit 0), got {result.returncode}\n"
        f"stdout: {result.stdout}"
    )
    # But should contain warning about missing figure
    assert "warning" in result.stdout.lower(), (
        f"Expected warning in stdout:\n{result.stdout}"
    )
    print("  PASS  generic ref no figure (warning only)")


def test_mermaid_no_caption_passes_with_warning():
    """Mermaid block without caption → warning (not blocking)."""
    result = run_validator(MERMAID_NO_CAPTION)
    assert result.returncode == 0, (
        f"Mermaid no caption expected pass (exit 0), got {result.returncode}\n"
        f"stdout: {result.stdout}"
    )
    assert "warning" in result.stdout.lower() or "mermaid" in result.stdout.lower(), (
        f"Expected warning about mermaid in stdout:\n{result.stdout}"
    )
    print("  PASS  mermaid no caption (warning only)")


def test_figure_gap_passes_with_warning():
    """Figure numbers 1 and 3 only (no 2) → warning (not blocking)."""
    result = run_validator(FIGURE_GAP)
    assert result.returncode == 0, (
        f"Figure gap expected pass (exit 0), got {result.returncode}\n"
        f"stdout: {result.stdout}"
    )
    assert "gap" in result.stdout.lower() or "warning" in result.stdout.lower(), (
        f"Expected warning about gap in stdout:\n{result.stdout}"
    )
    print("  PASS  figure gap (warning only)")


# ── Edge cases ─────────────────────────────────────────────────────────────


def test_only_images_passes():
    """Report with images but no explicit figure number references should pass."""
    text = """\
# Report

Here is a chart:

![Revenue Growth](./revenue.png)

And another:

![Market Share](./market.png)
"""
    expect_pass("only images no refs", text)


def test_image_as_figure_passes():
    """Image referenced as 图1 with caption should pass."""
    text = """\
# Report

图1 shows the trend.

![Trend](./trend.png)

图1: Revenue trend
"""
    expect_pass("image as figure with caption", text)


def test_mermaid_with_explicit_caption_passes():
    """Mermaid block with explicit 图1 caption should pass."""
    text = """\
# Report

图1 shows the workflow.

```mermaid
graph TD
    Start-->End
```

图1: Workflow diagram
"""
    expect_pass("mermaid with explicit caption", text)


def test_no_figure_number_in_body_but_mermaid_exists_passes():
    """Mermaid block exists but body never references it → warning (not blocking)."""
    text = """\
# Report

Lots of text.

```mermaid
graph TD
    A-->B
```

图1: Architecture
"""
    result = run_validator(text)
    # body never says "图1" → unreferenced caption → warning
    assert result.returncode == 0, (
        f"Expected pass (exit 0), got {result.returncode}\n"
        f"stdout: {result.stdout}"
    )
    print("  PASS  mermaid without body reference (warning only)")


# ── Main ───────────────────────────────────────────────────────────────────


def main() -> int:
    tests = [
        # --- Property-based tests ---
        ("property: valid report has no errors", test_property_valid_report_has_no_errors),
        ("property: arbitrary text does not crash", test_property_arbitrary_text_does_not_crash),
        ("property: missing figure detected", test_property_missing_figure_detected),
        # --- Contract tests ---
        ("empty markdown passes", test_empty_markdown_passes),
        ("no figures passes", test_no_figures_passes),
        ("valid Chinese figures passes", test_valid_chinese_figures_passes),
        ("valid English figures passes", test_valid_english_figures_passes),
        ("missing Chinese figure fails", test_missing_chinese_figure_fails),
        ("missing English figure fails", test_missing_english_figure_fails),
        ("duplicate caption fails", test_duplicate_caption_fails),
        ("code fence excludes ref", test_code_fence_excludes_figure_ref),
        ("generic ref no figure (warning only)", test_generic_ref_no_figure_passes),
        ("mermaid no caption (warning only)", test_mermaid_no_caption_passes_with_warning),
        ("figure gap (warning only)", test_figure_gap_passes_with_warning),
        ("only images no refs", test_only_images_passes),
        ("image as figure with caption", test_image_as_figure_passes),
        ("mermaid with explicit caption", test_mermaid_with_explicit_caption_passes),
        ("mermaid without body reference (warning only)", test_no_figure_number_in_body_but_mermaid_exists_passes),
    ]

    passed = 0
    failed = 0
    for name, fn in tests:
        try:
            fn()
            passed += 1
        except AssertionError as e:
            print(f"  ❌ {name}: {e}")
            failed += 1
        except Exception as e:
            print(f"  ❌ {name}: {type(e).__name__}: {e}")
            failed += 1

    print(f"\n{'=' * 50}")
    print(f"Total: {passed + failed} | Passed: {passed} | Failed: {failed}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
