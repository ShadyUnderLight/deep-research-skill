#!/usr/bin/env python3
"""Property-based regression tests for validate_external_citation_hygiene.py.

Each test creates a fixture, runs the validator as a subprocess,
and asserts the expected exit code and warning output.

Properties verified:
  - Empty text → no warnings (exit 0)
  - Clean text → no warnings (exit 0)
  - Common words like "turnaround" → no false positives
  - Each prohibited pattern → warning produced (exit 0, warning in stdout)
  - Multiple patterns → multiple distinct warnings
"""

import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = str(Path(__file__).resolve().parent / "validate_external_citation_hygiene.py")

# ── Baseline valid report (clean, no external citation artifacts) ──────

CLEAN_REPORT = """\
# Test Report

## Findings

The company reported revenue of 7.02 billion RMB for H1 2025 [S01].

据 FY2025 年报，公司营收同比增长 35%。

The transformer architecture revolutionized NLP (Vaswani et al., 2017, NeurIPS).

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Annual Report FY2025 | primary | 2026-03-15 | https://example.com | high | §2 |
"""


def run_validator(text: str) -> subprocess.CompletedProcess:
    with tempfile.TemporaryDirectory() as d:
        path = Path(d) / "report.md"
        path.write_text(text, encoding="utf-8")
        return subprocess.run(
            [sys.executable, SCRIPT, str(path)],
            capture_output=True, text=True,
        )


def expect_pass(name: str, text: str, warning_substring: str | None = None) -> None:
    """Assert validator exits 0 (pass). If warning_substring given, assert it appears in stdout."""
    result = run_validator(text)
    assert result.returncode == 0, (
        f"{name}: expected pass (exit 0), got {result.returncode}\n"
        f"stdout: {result.stdout}\nstderr: {result.stderr}"
    )
    if warning_substring:
        assert warning_substring.lower() in result.stdout.lower(), (
            f"{name}: expected warning containing '{warning_substring}' in:\n{result.stdout}"
        )
    print(f"  PASS  {name}")


def expect_fail(name: str, text: str) -> None:
    """Assert validator exits non-zero (fail)."""
    result = run_validator(text)
    assert result.returncode != 0, (
        f"{name}: expected fail (non-zero), got {result.returncode}\n"
        f"stdout: {result.stdout}"
    )
    print(f"  PASS  {name}")


# ── Property-based tests ──────────────────────────────────────────────

# Property 1: Empty text → no warnings


def test_empty_text_passes() -> None:
    """Empty report should pass without warnings."""
    text = ""
    result = run_validator(text)
    assert result.returncode == 0, f"expected pass, got {result.returncode}"
    assert "passed" in result.stdout.lower(), (
        f"expected 'passed' message in:\n{result.stdout}"
    )
    assert "⚠" not in result.stdout, (
        f"unexpected warning symbol in:\n{result.stdout}"
    )
    print("  PASS  empty text passes, no warnings")


# Property 2: Clean text → no warnings


def test_clean_report_passes() -> None:
    """Report with [Sxx] and equivalent citations should pass without warnings."""
    result = run_validator(CLEAN_REPORT)
    assert result.returncode == 0, (
        f"expected pass, got {result.returncode}\nstdout: {result.stdout}"
    )
    assert "passed" in result.stdout.lower(), (
        f"expected 'passed' message in:\n{result.stdout}"
    )
    assert "⚠" not in result.stdout, (
        f"unexpected warning symbol in:\n{result.stdout}"
    )
    print("  PASS  clean report passes, no warnings")


# Property 3: Common English words like "turnaround" → no false positives


def test_turnaround_word_no_false_positive() -> None:
    """'turnaround' is legitimate English — must not trigger."""
    text = CLEAN_REPORT.replace(
        "The company reported revenue",
        "The company turnaround strategy succeeded; revenue",
    )
    result = run_validator(text)
    assert result.returncode == 0, (
        f"expected pass, got {result.returncode}\nstdout: {result.stdout}"
    )
    assert "⚠" not in result.stdout, (
        f"unexpected warning about 'turnaround' in:\n{result.stdout}"
    )
    print("  PASS  'turnaround' no false positive")


def test_turning_word_no_false_positive() -> None:
    """'turning' is legitimate English — must not trigger."""
    text = CLEAN_REPORT.replace(
        "The company reported revenue",
        "The market is turning towards AI adoption",
    )
    result = run_validator(text)
    assert result.returncode == 0, (
        f"expected pass, got {result.returncode}\nstdout: {result.stdout}"
    )
    assert "⚠" not in result.stdout, (
        f"unexpected warning about 'turning' in:\n{result.stdout}"
    )
    print("  PASS  'turning' no false positive")


# Property 4: sandbox: path → 1+ warnings


def test_sandbox_path_warns() -> None:
    """sandbox:/mnt/data/... should produce a warning (not hard-fail)."""
    text = CLEAN_REPORT.replace(
        "## Source Register",
        "![revenue](sandbox:/mnt/data/revenue.png)\n\n## Source Register",
    )
    result = run_validator(text)
    assert result.returncode == 0, (
        f"expected pass (warning only), got {result.returncode}\nstdout: {result.stdout}"
    )
    assert "sandbox" in result.stdout.lower(), (
        f"expected warning about sandbox in:\n{result.stdout}"
    )
    print("  PASS  sandbox path warns")


# Property 5: turn reference → 1+ warnings


def test_turn_ref_warns() -> None:
    """turnNview reference should produce a warning (not hard-fail)."""
    text = CLEAN_REPORT.replace(
        "## Source Register",
        "Revenue grew 35% [turn43view0].\n\n## Source Register",
    )
    result = run_validator(text)
    assert result.returncode == 0, (
        f"expected pass (warning only), got {result.returncode}\nstdout: {result.stdout}"
    )
    assert "turnNxxx" in result.stdout, (
        f"expected warning about turn reference in:\n{result.stdout}"
    )
    print("  PASS  turn ref warns")


def test_turn_source_ref_warns() -> None:
    """turnNsource reference should be detected."""
    text = CLEAN_REPORT.replace(
        "## Source Register",
        "Based on [turn12source1].\n\n## Source Register",
    )
    result = run_validator(text)
    assert result.returncode == 0, (
        f"expected pass (warning only), got {result.returncode}\nstdout: {result.stdout}"
    )
    assert "turnNxxx" in result.stdout, (
        f"expected warning about turn reference in:\n{result.stdout}"
    )
    print("  PASS  turn source ref warns")


# Property 6: \ue000cite placeholder → 1+ warnings


def test_cite_placeholder_warns() -> None:
    """\ue000cite placeholder should produce a warning (not hard-fail)."""
    text = CLEAN_REPORT.replace(
        "## Source Register",
        "Result \ue000cite\turn43view0.\n\n## Source Register",
    )
    result = run_validator(text)
    assert result.returncode == 0, (
        f"expected pass (warning only), got {result.returncode}\nstdout: {result.stdout}"
    )
    assert "placeholder" in result.stdout.lower(), (
        f"expected warning about cite placeholder in:\n{result.stdout}"
    )
    print("  PASS  cite placeholder warns")


# Property 7: Multiple pattern types → multiple distinct warnings


def test_multiple_patterns_multiple_warnings() -> None:
    """Multiple distinct violation types produce multiple warnings."""
    text = CLEAN_REPORT.replace(
        "## Source Register",
        "Sandbox chart: ![x](sandbox:/tmp/x.png)\n"
        "Turn ref [turn99view0]\n"
        "\ue000cite\n\n## Source Register",
    )
    result = run_validator(text)
    assert result.returncode == 0, (
        f"expected pass (warning only), got {result.returncode}\nstdout: {result.stdout}"
    )
    # Should mention sandbox AND turn AND cite
    stdout_lower = result.stdout.lower()
    has_sandbox = "sandbox" in stdout_lower
    has_turn = "turn" in stdout_lower
    has_placeholder = "placeholder" in stdout_lower
    # At least 2 of 3 pattern types should produce distinct warnings
    distinct_count = sum([has_sandbox, has_turn, has_placeholder])
    assert distinct_count >= 2, (
        f"expected at least 2 distinct warnings, got {distinct_count}\n"
        f"stdout: {result.stdout}"
    )
    print(f"  PASS  multiple patterns produce {distinct_count} distinct warnings")


# Property 8: Text that passes legitimate uses of "turn" (return to, turn to)


def test_legitimate_turn_usages_no_false_positive() -> None:
    """'return to growth', 'turn to AI' should not trigger."""
    text = CLEAN_REPORT.replace(
        "The company reported revenue",
        "The company saw a return to growth.\n"
        "They turn to AI for innovation.\n"
        "A downtown office location was chosen.",
    )
    result = run_validator(text)
    assert result.returncode == 0, (
        f"expected pass, got {result.returncode}\nstdout: {result.stdout}"
    )
    assert "⚠" not in result.stdout, (
        f"unexpected warning in:\n{result.stdout}"
    )
    print("  PASS  legitimate turn usages no false positive")


# Property 9: file- temp ID should warn


def test_file_id_warns() -> None:
    """Temporary file-xxxxxxxxxxxx ID should produce a warning."""
    text = CLEAN_REPORT.replace(
        "## Source Register",
        "See [file-Db3F2kF0dXHhVd7z5CkRjX].\n\n## Source Register",
    )
    result = run_validator(text)
    assert result.returncode == 0, (
        f"expected pass (warning only), got {result.returncode}\nstdout: {result.stdout}"
    )
    stdout_lower = result.stdout.lower()
    assert "file-" in stdout_lower and "external" in stdout_lower, (
        f"expected warning about file- ID in:\n{result.stdout}"
    )
    print("  PASS  file- ID warns")


# ── Main ──────────────────────────────────────────────────────────────


def main() -> int:
    tests = [
        ("empty text passes, no warnings", test_empty_text_passes),
        ("clean report passes, no warnings", test_clean_report_passes),
        ("'turnaround' no false positive", test_turnaround_word_no_false_positive),
        ("'turning' no false positive", test_turning_word_no_false_positive),
        ("sandbox path warns", test_sandbox_path_warns),
        ("turn ref warns", test_turn_ref_warns),
        ("turn source ref warns", test_turn_source_ref_warns),
        ("cite placeholder warns", test_cite_placeholder_warns),
        ("multiple patterns → multiple warnings", test_multiple_patterns_multiple_warnings),
        ("legitimate turn usages no false positive", test_legitimate_turn_usages_no_false_positive),
        ("file- ID warns", test_file_id_warns),
    ]
    failures = []
    for name, fn in tests:
        try:
            fn()
        except AssertionError as exc:
            failures.append(name)
            print(f"  FAIL  {name}: {exc}")
        except Exception as exc:
            failures.append(name)
            print(f"  FAIL  {name} (exception): {exc}")

    if failures:
        print(f"\n{len(failures)} test(s) failed: {', '.join(failures)}")
        return 1

    print(f"\nAll {len(tests)} tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
