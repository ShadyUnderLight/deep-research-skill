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

REQUIRED_SET = set(REQUIRED_HEADINGS)

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

H2_RE = re.compile(r"^## (.+)$", re.MULTILINE)
ALL_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)
INLINE_FENCE_RE = re.compile(r"^[ ]{0,3}(`{3,}|~{3,})")


def strip_fenced_code_blocks(text: str) -> str:
    lines = text.split("\n")
    out = []
    in_fence = False
    fence_char = None
    fence_len = 0

    for line in lines:
        stripped = line.rstrip()
        if not in_fence:
            m = INLINE_FENCE_RE.match(stripped)
            if m:
                fence_char = m.group(1)[0]
                fence_len = len(m.group(1))
                in_fence = True
                continue
            out.append(line)
        else:
            closing_re = re.compile(
                r"^[ ]{0,3}"
                + re.escape(fence_char)
                + "{"
                + str(fence_len)
                + r",}\s*$"
            )
            if closing_re.match(stripped):
                in_fence = False
                continue

    return "\n".join(out)


def find_missing_headings(cleaned: str) -> list[str]:
    found = set()
    for m in H2_RE.finditer(cleaned):
        title = m.group(1).rstrip()
        full = f"## {title}"
        if full in REQUIRED_SET:
            found.add(full)
    return [h for h in REQUIRED_HEADINGS if h not in found]


def find_empty_sections(cleaned: str) -> list[str]:
    lines = cleaned.split("\n")
    heading_positions: list[tuple[str, int]] = []
    for i, line in enumerate(lines):
        m = re.match(r"^(#{1,6})\s+(.+)$", line.rstrip())
        if m:
            heading_positions.append((line.rstrip(), i))

    empty = []
    for idx, (heading_text, line_num) in enumerate(heading_positions):
        if heading_text not in REQUIRED_SET:
            continue
        next_line = (
            heading_positions[idx + 1][1]
            if idx + 1 < len(heading_positions)
            else len(lines)
        )
        body = lines[line_num + 1 : next_line]
        body_no_heading = [l for l in body if not re.match(r"^#{1,6}\s", l)]
        body_text = "\n".join(body_no_heading).strip()
        if not body_text:
            empty.append(heading_text)

    return empty


def check_artifacts(text: str) -> list[tuple]:
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

    missing = find_missing_headings(cleaned)
    if missing:
        print("Missing required headings:")
        for heading in missing:
            print(f"- {heading}")
        return 2

    empty = find_empty_sections(cleaned)
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
