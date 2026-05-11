#!/usr/bin/env python3

import re
import sys
from pathlib import Path

REQUIRED_HEADINGS = [
    "## Objective",
    "## Decision context",
    "## Primary route",
    "## Secondary disciplines",
    "## Core subquestions",
    "## Stop condition",
    "## Source register",
    "## Claim register",
    "## Uncertainty register",
    "## Artifact contract",
    "## Required audits",
    "## Final audit status",
]

ARTIFACT_RED_FLAGS = [
    r"\bTBD\b",
    r"\bTODO\b",
    r"\bXXX\b",
    r"\[\[placeholder\]\]",
    r"\{citation\}",
    r"\{\{[^\n{}]{1,80}\}\}",
    r"<PLACEHOLDER>",
    r"\[SOURCE\]",
    r"\[CITATION NEEDED\]",
    r"\[INSERT [^\]\n]{1,80}\]",
]

FENCED_BLOCK_RE = re.compile(r"^(`{3,}|~{3,})(.*?)\1.*?$", re.MULTILINE | re.DOTALL)
HEADING_RE = re.compile(r"^##\s+\S", re.MULTILINE)


def strip_fenced_code_blocks(text: str) -> str:
    """Remove fenced code blocks so headings inside them don't pollute checks."""
    return FENCED_BLOCK_RE.sub("", text)


def check_empty(cleaned: str, required_headings: list[str]) -> list[str]:
    """Return required headings whose section body is empty (no non-whitespace content).

    A section body is everything between the heading and the next heading or EOF.
    """
    lines = cleaned.split("\n")
    heading_set = set(required_headings)
    empty = []
    current = None
    current_start = None

    # First pass: find all required heading positions
    positions: list[tuple[str, int]] = []
    for i, line in enumerate(lines):
        stripped = line.rstrip()
        if stripped in heading_set:
            positions.append((stripped, i))

    if not positions:
        return []

    for idx, (heading, line_num) in enumerate(positions):
        next_line = positions[idx + 1][1] if idx + 1 < len(positions) else len(lines)
        body = lines[line_num + 1 : next_line]
        body_text = "\n".join(body).strip()
        if not body_text:
            empty.append(heading)

    return empty


def check_artifacts(text: str) -> list[tuple]:
    """Scan for placeholder / artifact red flags in the full text."""
    hits = []
    for pattern in ARTIFACT_RED_FLAGS:
        matches = re.findall(pattern, text)
        if matches:
            hits.append((pattern, matches[:3]))
    return hits


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_research_pack.py <path>")
        return 1

    path = Path(sys.argv[1])
    text = path.read_text(encoding="utf-8")
    cleaned = strip_fenced_code_blocks(text)

    missing = [h for h in REQUIRED_HEADINGS if h not in cleaned]

    if missing:
        print("Missing required headings:")
        for heading in missing:
            print(f"- {heading}")
        return 2

    empty = check_empty(cleaned, REQUIRED_HEADINGS)
    if empty:
        print("Empty required sections (no content after heading):")
        for heading in empty:
            print(f"- {heading}")
        return 2

    artifact_hits = check_artifacts(text)

    if artifact_hits:
        print("Artifact red flags detected:")
        for pattern, matches in artifact_hits:
            preview = ", ".join(repr(m) for m in matches)
            print(f"- pattern {pattern}: {preview}")
        return 3

    print("Research Pack structure looks valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
