#!/usr/bin/env python3
"""Detect forward-looking numeric claims mislabeled as confirmed facts.

This lightweight lint is intentionally report/fixture scoped. It should be run
on final report text or purpose-built fixtures, not on eval case descriptions
that quote known-bad examples for documentation.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


CONFIRMED_LABEL_RE = re.compile(
    r"\[(?:确认|已确认事实|CONF|Confirmed|confirmed)\]"
)

FORWARD_RE = re.compile(
    r"(?:"
    r"预计|预测|预期|将达|将达到|有望|"
    r"expected|forecast(?:s|ed|ing)?|projected|projection|"
    r"estimated\s+to|will\s+reach|by\s+20\d{2}"
    r")",
    re.IGNORECASE,
)

NUMBER_RE = re.compile(
    r"(?:"
    r"[$¥€£]?\s*\d[\d,]*(?:\.\d+)?\s*(?:%|bp|bps|x|X|倍|万|亿|兆|台|GW|GWh|TWh|MW|B|M|bn|mn)?\+?"
    r"|20\d{2}\s*(?:年|H[12]|Q[1-4])?"
    r")",
    re.IGNORECASE,
)

SOURCE_EVENT_RE = re.compile(
    r"(?:发布|published|released).{0,30}(?:预测报告|forecast report|projection report)",
    re.IGNORECASE,
)

OUTCOME_RE = re.compile(
    r"(?:"
    r"预计|预期|将达|将达到|有望|"
    r"预测.{0,30}(?:到|至|为|达|达到|超过|\d|%)|"
    r"expected|forecast(?:s|ed|ing)?.{0,40}(?:to|reach|grow|increase|decline|\d|[$¥€£])|"
    r"projected|estimated\s+to|will\s+reach|by\s+20\d{2}"
    r")",
    re.IGNORECASE,
)


def strip_fenced_code_blocks(text: str) -> str:
    lines = text.splitlines()
    out: list[str] = []
    in_fence = False
    fence_char = ""
    fence_len = 0

    for line in lines:
        stripped = line.rstrip()
        if not in_fence:
            m = re.match(r"^[ ]{0,3}(`{3,}|~{3,})", stripped)
            if m:
                fence_char = m.group(1)[0]
                fence_len = len(m.group(1))
                in_fence = True
                continue
            out.append(line)
            continue

        closing = re.compile(
            r"^[ ]{0,3}" + re.escape(fence_char) + "{" + str(fence_len) + r",}\s*$"
        )
        if closing.match(stripped):
            in_fence = False

    return "\n".join(out)


def split_sentences(text: str) -> list[tuple[int, str]]:
    results: list[tuple[int, str]] = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        line = line.strip()
        if not line:
            continue
        chunks = re.split(r"(?<=[。！？!?；;])\s+|\s+[•·]\s+", line)
        for chunk in chunks:
            chunk = chunk.strip()
            if chunk:
                results.append((line_no, chunk))
    return results


def find_confirmed_forward_looking_numbers(text: str) -> list[tuple[int, str]]:
    cleaned = strip_fenced_code_blocks(text)
    hits: list[tuple[int, str]] = []
    for line_no, sentence in split_sentences(cleaned):
        if not CONFIRMED_LABEL_RE.search(sentence):
            continue
        if not FORWARD_RE.search(sentence):
            continue
        if not NUMBER_RE.search(sentence):
            continue
        if SOURCE_EVENT_RE.search(sentence) and not OUTCOME_RE.search(sentence):
            continue
        hits.append((line_no, sentence))
    return hits


def validate_file(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    hits = find_confirmed_forward_looking_numbers(text)
    return [
        f"{path}:{line_no}: forward-looking numeric claim uses confirmed label: {sentence}"
        for line_no, sentence in hits
    ]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Lint forward-looking numeric claims mislabeled as confirmed facts."
    )
    parser.add_argument("paths", nargs="+", help="Markdown/text files to validate")
    args = parser.parse_args(argv)

    errors: list[str] = []
    for raw_path in args.paths:
        path = Path(raw_path)
        if not path.exists():
            errors.append(f"{path}: file not found")
            continue
        errors.extend(validate_file(path))

    if errors:
        print("Forward-looking label lint failed:")
        for error in errors:
            print(f"- {error}")
        return 2

    print(f"Forward-looking label lint passed for {len(args.paths)} file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
