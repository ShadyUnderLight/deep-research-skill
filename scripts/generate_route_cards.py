#!/usr/bin/env python3
"""
Route card generator (issue #380).

Generates per-route short cards under references/routes/<route-id>.md from
schemas/route-manifest.json (the canonical route registry).  Each card is a
generated view — the manifest is the single source of truth for route
identity, triggers, boundaries, reads, disciplines, audits, artifact
contract and hard-fail keywords.  Do not edit generated cards by hand;
edit the manifest and regenerate.

Canonical / generated relationship (issue #380):
    schemas/route-manifest.json   → canonical (single source of truth)
    references/route-index.md     → hand-maintained compact trigger table
                                    (drift-checked against the manifest by
                                    validate_route_manifest.py)
    references/routes/<id>.md     → GENERATED route cards (this script)
    ROUTING-MATRIX.md             → human-readable full contract overview
                                    (drift-checked against the manifest)

Usage:
    python3 scripts/generate_route_cards.py            # (re)generate all cards
    python3 scripts/generate_route_cards.py --check    # fail if any card is stale

Exit codes:
    0 = OK (or nothing to regenerate in --check)
    1 = generation / write error
    2 = --check found stale cards (drift)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "schemas" / "route-manifest.json"
CARDS_DIR = ROOT / "references" / "routes"
ROUTE_INDEX_PATH = ROOT / "references" / "route-index.md"
ROUTING_MATRIX_PATH = ROOT / "ROUTING-MATRIX.md"

GENERATED_HEADER = (
    "> **Generated view** — do not edit by hand. "
    "Canonical source: `schemas/route-manifest.json`. "
    "Regenerate with `python3 scripts/generate_route_cards.py`."
)

EXIT_OK = 0
EXIT_ERROR = 1
EXIT_DRIFT = 2

# Card fields that must be present for every route.  Keyed by manifest field
# name → (markdown heading, empty-allowed).
CARD_SECTIONS: list[tuple[str, str, bool]] = [
    ("trigger", "## Trigger", False),
    ("do_not_use", "## Do not use when", False),
    ("often_confused_with", "## Often confused with", True),
    ("primary_reads", "## Primary reads", True),
    ("required_disciplines", "## Required disciplines", True),
    ("required_audits", "## Required audits", False),
    ("artifact_contract", "## Artifact contract", False),
    ("hard_fail_keywords", "## Failure signs (hard-fail keywords)", True),
    ("hard_fail_source", "## Hard-fail source", False),
]


def _load_manifest() -> dict:
    import json
    with MANIFEST_PATH.open(encoding="utf-8") as f:
        return json.load(f)


def _anchor_link(text: str) -> str:
    """Build a GitHub-style anchor link from a heading-like string."""
    lowered = text.lower().strip()
    # Keep only alphanumerics, spaces, and hyphens; drop punctuation
    kept = "".join(c for c in lowered if c.isalnum() or c in " -")
    return kept.replace(" ", "-")


def _audit_display(audit_id: str) -> str:
    """Format an audit id as a checklist link when the file exists.

    Checklists live at the repo root (checklists/x.md); from a card in
    references/routes/ the link is ../../checklists/x.md.
    """
    checklist = ROOT / "checklists" / f"{audit_id}.md"
    if checklist.is_file():
        return f"[`{audit_id}`](../../checklists/{audit_id}.md)"
    return f"`{audit_id}`"


def _card_relative(ref: str) -> str:
    """Convert a repo-root-relative path to one relative to references/routes/.

    Cards live at references/routes/<id>.md:
      - ``references/foo.md`` → ``../foo.md`` (sibling in references/)
      - ``examples/foo.md``   → ``../../examples/foo.md`` (repo root)
      - ``checklists/foo.md`` → ``../../checklists/foo.md`` (repo root)
      - ``ROUTING-MATRIX.md`` → ``../../ROUTING-MATRIX.md`` (repo root)
    """
    if ref.startswith("references/"):
        return f"../{ref[len('references/'):]}"
    return f"../../{ref}"


def _primary_read_display(ref: str) -> str:
    """Format a primary read as a link relative to references/routes/."""
    if not (ROOT / ref).is_file():
        return f"`{ref}`"
    return f"[`{ref}`]({_card_relative(ref)})"


def render_card(route: dict, known_route_ids: set[str]) -> str:
    """Render a single route card from a manifest route entry.

    ``known_route_ids`` is the full set of canonical route ids from the
    manifest; sibling-card links are decided from this set (not from
    on-disk file existence) so rendering is deterministic regardless of
    generation order.
    """
    rid = route["id"]
    display = route["display_name"]
    category = route.get("category", "specialized")
    aliases = route.get("aliases", [])

    lines: list[str] = [
        f"# Route Card: {display}",
        "",
        GENERATED_HEADER,
        "",
        f"- **Route ID**: `{rid}`",
        f"- **Category**: `{category}`",
        f"- **Aliases**: {', '.join(f'`{a}`' for a in aliases) if aliases else '—'}",
        f"- **Full contract**: [`ROUTING-MATRIX.md`](../../ROUTING-MATRIX.md#{_anchor_link('Route: ' + display)})",
        f"- **Compact index**: [`references/route-index.md`](../../references/route-index.md)",
        "",
    ]

    # Often-confused-with links to sibling route cards
    often_confused = route.get("often_confused_with", [])
    if often_confused:
        confused_links = []
        for other_id in often_confused:
            if other_id in known_route_ids:
                confused_links.append(f"[`{other_id}`]({other_id}.md)")
            else:
                confused_links.append(f"`{other_id}`")
        lines.append("## Often confused with")
        lines.append("")
        lines.append("- " + "\n- ".join(confused_links))
        lines.append("")

    # Primary reads as links
    primary_reads = route.get("primary_reads", [])
    if primary_reads:
        lines.append("## Primary reads")
        lines.append("")
        for ref in primary_reads:
            lines.append(f"- {_primary_read_display(ref)}")
        lines.append("")

    # Required disciplines
    disciplines = route.get("required_disciplines", [])
    if disciplines:
        lines.append("## Required disciplines")
        lines.append("")
        for d in disciplines:
            lines.append(f"- `{d}`")
        lines.append("")

    # Required audits
    audits = route.get("required_audits", [])
    lines.append("## Required audits")
    lines.append("")
    for a in audits:
        lines.append(f"- {_audit_display(a)}")
    lines.append("")

    # Trigger
    lines.append("## Trigger")
    lines.append("")
    lines.append(route.get("trigger", ""))
    lines.append("")

    # Do not use
    lines.append("## Do not use when")
    lines.append("")
    lines.append(route.get("do_not_use", ""))
    lines.append("")

    # Artifact contract
    lines.append("## Artifact contract")
    lines.append("")
    lines.append(route.get("artifact_contract", ""))
    lines.append("")

    # Hard-fail keywords (failure signs)
    hard_fail = route.get("hard_fail_keywords", [])
    lines.append("## Failure signs (hard-fail keywords)")
    lines.append("")
    if hard_fail:
        for kw in hard_fail:
            lines.append(f"- `{kw}`")
    else:
        lines.append("- (none)")
    lines.append("")

    # Hard-fail source
    lines.append("## Hard-fail source")
    lines.append("")
    lines.append(f"`{route.get('hard_fail_source', '')}`")
    lines.append("")

    return "\n".join(lines) + "\n"


def generate_cards() -> list[Path]:
    """Generate all route cards. Returns the list of written paths."""
    manifest = _load_manifest()
    known_route_ids = {r["id"] for r in manifest["routes"]}
    CARDS_DIR.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for route in manifest["routes"]:
        rid = route["id"]
        target = CARDS_DIR / f"{rid}.md"
        content = render_card(route, known_route_ids)
        target.write_text(content, encoding="utf-8")
        written.append(target)
    return written


def check_drift() -> int:
    """Regenerate in memory and compare with on-disk cards. Returns exit code."""
    manifest = _load_manifest()
    known_route_ids = {r["id"] for r in manifest["routes"]}
    stale: list[str] = []
    missing: list[str] = []
    for route in manifest["routes"]:
        rid = route["id"]
        target = CARDS_DIR / f"{rid}.md"
        expected = render_card(route, known_route_ids)
        if not target.is_file():
            missing.append(rid)
        elif target.read_text(encoding="utf-8") != expected:
            stale.append(rid)

    if missing or stale:
        print("ROUTE CARD DRIFT DETECTED:")
        if missing:
            print(f"  ✗ Missing cards: {', '.join(missing)}")
        if stale:
            print(f"  ✗ Stale cards: {', '.join(stale)}")
        print("  Run `python3 scripts/generate_route_cards.py` and commit the result.")
        return EXIT_DRIFT
    print("OK — route cards are in sync with schemas/route-manifest.json")
    return EXIT_OK


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate route cards from schemas/route-manifest.json"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify committed cards match the manifest without writing",
    )
    args = parser.parse_args(argv)

    if args.check:
        return check_drift()

    written = generate_cards()
    print(f"Generated {len(written)} route cards in {CARDS_DIR.relative_to(ROOT)}")
    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())