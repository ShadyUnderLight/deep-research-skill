#!/usr/bin/env python3
"""Regression tests for validate_research_pack.py.

Each test creates a single-mutation fixture from a valid baseline,
runs the validator, and asserts the expected exit code.
"""

import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

VALID = """\
## Objective
ok

## Decision context
ok

## Primary route
ok

## Secondary disciplines
ok

## Core subquestions
ok

## Stop condition
ok

## Source register
ok

## Claim register
ok

## Uncertainty register
ok

## Artifact contract
ok

## Required audits
ok

## Final audit status
ok
"""

VALIDATOR = str(Path(__file__).resolve().parent / "validate_research_pack.py")


def write(path: str, content: str) -> str:
    Path(path).write_text(content)
    return path


def run_validator(path: str) -> int:
    return subprocess.run(
        [sys.executable, VALIDATOR, path],
        capture_output=True, text=True
    ).returncode


def test_valid_baseline(d: str) -> None:
    path = write(os.path.join(d, "valid.md"), VALID)
    rc = run_validator(path)
    assert rc == 0, f"valid baseline: expected 0, got {rc}"


def test_codeblock_heading(d: str) -> None:
    text = re.sub(
        r"^## Stop condition\nok",
        "```\n## Stop condition\n```",
        VALID, flags=re.MULTILINE
    )
    path = write(os.path.join(d, "codeblock.md"), text)
    rc = run_validator(path)
    assert rc == 2, f"code-block heading: expected exit 2 (missing heading), got {rc}"


def test_empty_section(d: str) -> None:
    text = re.sub(
        r"^## Stop condition\nok",
        "## Stop condition\n",
        VALID, flags=re.MULTILINE
    )
    path = write(os.path.join(d, "empty.md"), text)
    rc = run_validator(path)
    assert rc == 2, f"empty section: expected exit 2, got {rc}"


def test_h3_instead_of_h2(d: str) -> None:
    text = re.sub(
        r"^## Stop condition$",
        "### Stop condition",
        VALID, flags=re.MULTILINE
    )
    path = write(os.path.join(d, "h3.md"), text)
    rc = run_validator(path)
    assert rc == 2, f"H3 instead of H2: expected exit 2, got {rc}"


def test_blockquote_heading(d: str) -> None:
    text = re.sub(
        r"^## Stop condition$",
        "> ## Stop condition",
        VALID, flags=re.MULTILINE
    )
    path = write(os.path.join(d, "bq.md"), text)
    rc = run_validator(path)
    assert rc == 2, f"blockquote heading: expected exit 2, got {rc}"


def test_indented_fence(d: str) -> None:
    text = re.sub(
        r"^## Stop condition\nok",
        "   ```\n   ## Stop condition\n   hidden\n   ```",
        VALID, flags=re.MULTILINE
    )
    path = write(os.path.join(d, "ifence.md"), text)
    rc = run_validator(path)
    assert rc == 2, f"indented fence heading: expected exit 2, got {rc}"


def test_subheading_only_body(d: str) -> None:
    text = re.sub(
        r"^## Stop condition\nok",
        "## Stop condition\n### Placeholder subsection",
        VALID, flags=re.MULTILINE
    )
    path = write(os.path.join(d, "subonly.md"), text)
    rc = run_validator(path)
    assert rc == 2, f"sub-heading-only body: expected exit 2, got {rc}"


def test_partial_heading_match(d: str) -> None:
    text = re.sub(
        r"^## Stop condition$",
        "## Stop condition details",
        VALID, flags=re.MULTILINE
    )
    path = write(os.path.join(d, "partial.md"), text)
    rc = run_validator(path)
    assert rc == 2, f"partial heading match: expected exit 2, got {rc}"


def main() -> int:
    with tempfile.TemporaryDirectory() as d:
        tests = [
            ("valid baseline", test_valid_baseline),
            ("code-block heading", test_codeblock_heading),
            ("empty section", test_empty_section),
            ("H3 instead of H2", test_h3_instead_of_h2),
            ("blockquote heading", test_blockquote_heading),
            ("indented fence", test_indented_fence),
            ("sub-heading-only body", test_subheading_only_body),
            ("partial heading match", test_partial_heading_match),
        ]
        failures = []
        for name, fn in tests:
            try:
                fn(d)
                print(f"  PASS  {name}")
            except AssertionError as e:
                print(f"  FAIL  {name}: {e}")
                failures.append(name)
        if failures:
            print(f"\n{len(failures)} test(s) failed: {', '.join(failures)}")
            return 1
        print(f"\nAll {len(tests)} tests passed.")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
