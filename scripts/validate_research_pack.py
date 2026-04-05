#!/usr/bin/env python3

import sys
from pathlib import Path

REQUIRED_HEADINGS = [
    "## Objective",
    "## Decision context",
    "## Primary route",
    "## Secondary disciplines",
    "## Core subquestions",
    "## Source register",
    "## Claim register",
    "## Uncertainty register",
    "## Artifact contract",
    "## Required audits",
    "## Final audit status",
]


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_research_pack.py <path>")
        return 1

    path = Path(sys.argv[1])
    text = path.read_text(encoding="utf-8")
    missing = [heading for heading in REQUIRED_HEADINGS if heading not in text]

    if missing:
        print("Missing required headings:")
        for heading in missing:
            print(f"- {heading}")
        return 2

    print("Research Pack structure looks valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
