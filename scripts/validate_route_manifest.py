#!/usr/bin/env python3
"""
Route manifest drift detector (registry-backed).

Validates that schemas/route-manifest.json is consistent with:
1. schemas/discipline-registry.json  — required_disciplines must be registered
2. schemas/audit-registry.json       — required_audits must be registered
3. checklists/ files                 — no orphan checklists, no missing files
4. ROUTING-MATRIX.md                 — route count, display names, audit lists,
                                       hard-fail keywords
5. references/route-index.md         — route ids, trigger keywords, audits
6. evals/INDEX.md                    — Primary/Secondary route columns

Route/alias/discipline/audit identity now comes from the JSON registries
via registry_loader — this script no longer regex-parses audit_report.py.
Alias resolution itself (including unknown-route blocking) is enforced by
the loader at runtime; duplicate aliases surface here as load errors.

Exit codes:
    0 = manifest is consistent with code/docs
    1 = non-blocking warnings
    2 = blocking drift detected

Usage:
    python3 scripts/validate_route_manifest.py [--manifest schemas/route-manifest.json]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import registry_loader
from registry_loader import RegistryError

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "schemas" / "route-manifest.json"
ROUTING_MATRIX = ROOT / "ROUTING-MATRIX.md"
ROUTE_INDEX = ROOT / "references" / "route-index.md"
ROUTE_CARDS_DIR = ROOT / "references" / "routes"
CHECKLISTS_DIR = ROOT / "checklists"
EVALS_INDEX = ROOT / "evals" / "INDEX.md"
AUDIT_REGISTRY = ROOT / "schemas" / "audit-registry.json"

EXIT_OK = 0
EXIT_WARN = 1
EXIT_FAIL = 2

# ── Non-discipline eval tags seen in evals/INDEX.md Primary column ──────────
# These are eval-asset labels (PDF build, company status, checklist names,
# delivery concerns), not canonical disciplines.  Canonical disciplines come
# from schemas/discipline-registry.json; route ids come from the manifest.
_EVAL_TAG_WHITELIST: set[str] = {
    "adversarial-input",
    "comparative-analysis",
    "company-status",
    "company-status-boundary",
    "corporate-status",
    "delivery-cleanliness",
    "external-channel-preflight",
    "finance",
    "listed-company-report",
    "listing-status",
    "pdf-build",
    "pdf-layout",
    "pdf-rendering",
    "private-company",
    "product-ranking",
    "ranking",
    "reporting-period",
    "valuation-methodology",
}


# ── Parser for ROUTING-MATRIX.md ─────────────────────────────────────────────


def _parse_routing_matrix_headings(text: str) -> list[str]:
    """Extract route heading display names from ROUTING-MATRIX.md."""
    return re.findall(r"^## Route: (.+)$", text, re.M)


def _parse_routing_matrix_route_sections(text: str) -> dict[str, str]:
    """Split ROUTING-MATRIX.md into per-route sections by '## Route: ' headings.

    Returns {normalized_heading: section_text}.
    """
    sections: dict[str, str] = {}
    parts = re.split(r"^## Route: ", text, flags=re.M)
    for part in parts[1:]:  # Skip content before first ## Route:
        heading_end = part.index("\n") if "\n" in part else len(part)
        heading = part[:heading_end].strip()
        body = part[heading_end:]
        sections[registry_loader._normalize_name(heading)] = body
    return sections


def _parse_audits_from_matrix_section(section: str) -> list[str]:
    """Extract audit checklist names from a ROUTING-MATRIX.md route section."""
    audit_match = re.search(
        r"### Audit\n((?:\s*-.*\n?)+)",
        section,
    )
    if not audit_match:
        return []
    audit_lines = audit_match.group(1).strip().split("\n")
    audits: list[str] = []
    for line in audit_lines:
        m = re.search(r"`checklists/([^`]+)\.md`", line)
        if m:
            audits.append(m.group(1).strip())
    return audits


def _parse_matrix_route_name_to_id(
    headings: list[str], manifest_routes: dict[str, dict]
) -> dict[str, str]:
    """Map normalized ROUTING-MATRIX.md headings to manifest route IDs."""
    mapping: dict[str, str] = {}
    for heading in headings:
        norm = registry_loader._normalize_name(heading)
        for route in manifest_routes.values():
            if registry_loader._normalize_name(route["display_name"]) == norm:
                mapping[norm] = route["id"]
                break
    return mapping


# ── Manifest loading ─────────────────────────────────────────────────────────


def _load_manifest(path: Path) -> dict:
    """Load and validate top-level manifest structure."""
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise SystemExit(f"ERROR: Manifest file not found: {path}")
    try:
        manifest = json.loads(text)
    except json.JSONDecodeError as e:
        raise SystemExit(f"ERROR: Invalid JSON in {path}: {e}")

    if not isinstance(manifest, dict):
        raise SystemExit(f"ERROR: Manifest must be a JSON object: {path}")
    if "version" not in manifest:
        raise SystemExit(f"ERROR: Missing 'version' field in {path}")
    if "routes" not in manifest:
        raise SystemExit(f"ERROR: Missing 'routes' field in {path}")
    if not isinstance(manifest["routes"], list):
        raise SystemExit(f"ERROR: 'routes' must be a list in {path}")
    return manifest


# ── evals/INDEX.md parsing ───────────────────────────────────────────────────


def _check_evals_index_line(line: str, known_ids: set[str]) -> list[str]:
    """Validate one evals/INDEX.md data row's route columns.

    Row layout: | Path | Primary route | Secondary route | ... — after
    strip("|") + split("|"), cells[1] is the Primary route column and
    cells[2] the Secondary route column.  Both are checked against
    canonical route ids, discipline ids and the eval-tag whitelist.
    Returns blocking errors for unknown values.
    """
    if not line.startswith("| `evals/cases/"):
        return []
    cells = [c.strip().strip("`") for c in line.strip("|").split("|")]
    if len(cells) < 3:
        return [f"evals/INDEX.md row has too few columns: {line[:60]}..."]
    errors: list[str] = []
    for col_idx, col_name in [(1, "Primary route"), (2, "Secondary route")]:
        val = cells[col_idx]
        if not val or val == "-":
            continue
        if val.startswith("evals/cases/") or val.endswith(".md"):
            continue
        for part in val.split("/"):
            part = part.strip()
            if not part or part == "-":
                continue
            if part not in known_ids:
                errors.append(
                    f"evals/INDEX.md: '{part}' in {col_name} "
                    f"column for {cells[0]} is not a known canonical "
                    f"route, discipline or eval tag"
                )
    return errors


# ── references/route-index.md parsing ───────────────────────────────────────


def _check_route_index(
    text: str,
    manifest_ids: set[str],
    route_audits: dict[str, set[str]],
) -> list[str]:
    """Validate references/route-index.md trigger table against the manifest.

    Trigger table rows: | Route ID | Trigger keywords | Reads | Audits |.
    Checks: route id set matches the manifest bidirectionally, trigger
    keywords are non-empty, and each listed audit is part of that route's
    required_audits in the manifest.  Returns blocking errors.
    """
    errors: list[str] = []
    index_ids: set[str] = set()
    in_trigger_table = False
    for line in text.splitlines():
        if line.startswith("| Route ID | Trigger keywords"):
            in_trigger_table = True
            continue
        if in_trigger_table and line.startswith("## "):
            break
        if not in_trigger_table:
            continue
        if not line.startswith("| `"):
            continue
        cells = [c.strip().strip("`") for c in line.strip("|").split("|")]
        # Row: | Route ID | Trigger keywords | Reads | Audits | → 4 cells
        if len(cells) < 4:
            continue
        rid = cells[0]  # after strip("|"), the Route ID is the first cell
        if rid in {"Route ID", ""} or set(rid) <= {"-"}:
            continue
        index_ids.add(rid)
        if rid not in manifest_ids:
            errors.append(
                f"route-index.md lists route '{rid}' which is not in the manifest"
            )
            continue
        trigger = cells[1]
        if not trigger or trigger == "-":
            errors.append(
                f"route-index.md route '{rid}' has empty trigger keywords"
            )
        for audit in (a.strip() for a in cells[3].split(",")):
            audit = audit.strip("`")
            if not audit or audit == "-":
                continue
            if audit not in route_audits.get(rid, set()):
                errors.append(
                    f"route-index.md route '{rid}' lists audit '{audit}' "
                    f"which is not in the route's manifest required_audits"
                )

    missing = manifest_ids - index_ids
    if missing:
        errors.append(
            f"Manifest routes missing from route-index.md trigger table: "
            f"{', '.join(sorted(missing))}"
        )
    return errors


# ── references/routes/*.md route cards ────────────────────────────────────────


def _check_route_cards(
    cards_dir: Path,
    manifest_routes: dict[str, dict],
    manifest_ids: set[str],
) -> list[str]:
    """Validate generated route cards (references/routes/<id>.md) against the
    manifest (issue #380).

    Route cards are generated views of the manifest — their per-route
    sections (trigger, do-not-use, often-confused, primary reads, required
    disciplines, required audits, artifact contract, failure signs) must
    match the manifest fields.  A card is stale when any section disagrees,
    which means the manifest changed without regenerating the cards.
    """
    errors: list[str] = []

    # 1. Every manifest route must have a card file.
    for rid in sorted(manifest_ids):
        card = cards_dir / f"{rid}.md"
        if not card.is_file():
            errors.append(
                f"Missing route card: references/routes/{rid}.md — "
                f"run `python3 scripts/generate_route_cards.py`"
            )

    # 2. Extra card files (no manifest route) are drift.
    if cards_dir.is_dir():
        for card in sorted(cards_dir.glob("*.md")):
            rid = card.stem
            if rid not in manifest_ids:
                errors.append(
                    f"Orphan route card: references/routes/{rid}.md has no "
                    f"corresponding route in the manifest"
                )

    # 3. Section-level sync: each manifest field must appear in the card.
    #    Card section headings (issue #380 card contract):
    section_for: dict[str, str] = {
        "trigger": "## Trigger",
        "do_not_use": "## Do not use when",
        "often_confused_with": "## Often confused with",
        "primary_reads": "## Primary reads",
        "required_disciplines": "## Required disciplines",
        "required_audits": "## Required audits",
        "artifact_contract": "## Artifact contract",
        "hard_fail_keywords": "## Failure signs (hard-fail keywords)",
        "hard_fail_source": "## Hard-fail source",
    }
    for rid, route in manifest_routes.items():
        card = cards_dir / f"{rid}.md"
        if not card.is_file():
            continue
        text = card.read_text(encoding="utf-8")
        for field, heading in section_for.items():
            value = route.get(field, "")
            if isinstance(value, str):
                if not value:
                    continue
                if value not in text:
                    errors.append(
                        f"Route card '{rid}': field '{field}' value missing "
                        f"from references/routes/{rid}.md"
                    )
            elif isinstance(value, list):
                for item in value:
                    if item and item not in text:
                        errors.append(
                            f"Route card '{rid}': {field} item '{item}' "
                            f"missing from references/routes/{rid}.md"
                        )
    return errors


# ── Validation logic ─────────────────────────────────────────────────────────


def validate(path: Path | None = None) -> int:
    """Run full drift validation. Returns exit code."""
    manifest_path = path or DEFAULT_MANIFEST
    manifest = _load_manifest(manifest_path)
    errors: list[str] = []
    warnings: list[str] = []

    # Route registry load — fail closed on structural errors.  A malformed
    # registry makes every downstream check meaningless, so report the
    # structural error and stop instead of continuing into KeyError land.
    try:
        registry = registry_loader.load_route_registry(manifest_path)
    except RegistryError as e:
        print(f"BLOCKING DRIFT DETECTED (1 issue(s)):\n  ✗ {e}")
        return EXIT_FAIL

    manifest_routes: dict[str, dict] = {}
    manifest_ids: set[str] = set()
    for route in manifest["routes"]:
        rid = route["id"]
        if rid in manifest_routes:
            errors.append(f"Duplicate route ID in manifest: {rid}")
        manifest_routes[rid] = route
        manifest_ids.add(rid)

    # ═══ Check 1: validator bindings are well-formed ═════════════════════════
    # Existence in KNOWN_VALIDATOR_IDS is enforced by the loader already;
    # this check guards non-empty and duplicate bindings with clear messages.
    for rid, route in manifest_routes.items():
        bindings = route.get("validator_bindings", [])
        if not isinstance(bindings, list) or not bindings:
            errors.append(f"Route '{rid}': validator_bindings must be non-empty")
            continue
        if len(bindings) != len(set(bindings)):
            errors.append(f"Route '{rid}': duplicate validator bindings: {bindings}")

    # ═══ Check 2: required_disciplines are registered ════════════════════════
    try:
        discipline_registry = registry_loader.load_discipline_registry()
        known_disciplines = discipline_registry.discipline_ids()
        for rid, route in manifest_routes.items():
            unknown = set(route.get("required_disciplines", [])) - known_disciplines
            if unknown:
                errors.append(
                    f"Route '{rid}': required_disciplines not in "
                    f"discipline-registry.json: {sorted(unknown)}"
                )
    except RegistryError as e:
        errors.append(str(e))
        known_disciplines = set()

    # ═══ Check 3: required_audits are registered and checklist files exist ═══
    try:
        audit_registry = registry_loader.load_audit_registry()
        known_audits = audit_registry.audit_ids()
    except RegistryError as e:
        errors.append(str(e))
        known_audits = set()

    existing_checklists = {p.stem for p in CHECKLISTS_DIR.glob("*.md")}
    for rid, route in manifest_routes.items():
        for audit in route.get("required_audits", []):
            if audit not in known_audits:
                errors.append(
                    f"Route '{rid}' requires audit '{audit}' but it is not "
                    f"registered in schemas/audit-registry.json"
                )
            elif audit not in existing_checklists:
                errors.append(
                    f"Route '{rid}' requires audit '{audit}' but checklist "
                    f"file 'checklists/{audit}.md' does not exist"
                )

    # Check 3b: audit registry and checklists directory must not drift
    if known_audits:
        unregistered = existing_checklists - known_audits
        if unregistered:
            errors.append(
                f"Checklist files without audit-registry entries: "
                f"{', '.join(sorted(unregistered))}"
            )

    # ═══ Check 4: ROUTING-MATRIX.md consistency ══════════════════════════════
    if not ROUTING_MATRIX.is_file():
        errors.append(
            f"ROUTING-MATRIX.md not found at {ROUTING_MATRIX} — "
            f"cannot verify manifest consistency"
        )
    else:
        matrix_text = ROUTING_MATRIX.read_text(encoding="utf-8")
        matrix_headings = _parse_routing_matrix_headings(matrix_text)
        specialized_in_manifest = sum(
            1 for r in manifest["routes"] if r.get("category") == "specialized"
        )

        if len(matrix_headings) != specialized_in_manifest:
            errors.append(
                f"ROUTING-MATRIX.md has {len(matrix_headings)} route sections, "
                f"manifest has {specialized_in_manifest} specialized routes — "
                f"drift detected"
            )
        else:
            # Compare display names (normalized)
            matrix_norms = {
                registry_loader._normalize_name(h): h for h in matrix_headings
            }
            manifest_display_names = [
                r["display_name"] for r in manifest["routes"]
                if r.get("category") == "specialized"
            ]
            manifest_norms = {
                registry_loader._normalize_name(d): d
                for d in manifest_display_names
            }

            missing_in_manifest = set(matrix_norms.keys()) - set(manifest_norms.keys())
            missing_in_matrix = set(manifest_norms.keys()) - set(matrix_norms.keys())

            if missing_in_manifest:
                errors.append(
                    f"ROUTING-MATRIX.md headings not in manifest: "
                    f"{', '.join(sorted(matrix_norms[h] for h in missing_in_manifest))}"
                )
            if missing_in_matrix:
                errors.append(
                    f"Manifest display_names not in ROUTING-MATRIX.md: "
                    f"{', '.join(sorted(manifest_norms[d] for d in missing_in_matrix))}"
                )

        # Check 5b: audit list per route comparison
        matrix_sections = _parse_routing_matrix_route_sections(matrix_text)
        name_to_id = _parse_matrix_route_name_to_id(matrix_headings, manifest_routes)

        for heading_norm, route_id in name_to_id.items():
            section = matrix_sections.get(heading_norm, "")
            matrix_audits = set(_parse_audits_from_matrix_section(section))
            manifest_audits = set(
                manifest_routes[route_id].get("required_audits", [])
            )

            if matrix_audits != manifest_audits:
                missing = manifest_audits - matrix_audits
                extra = matrix_audits - manifest_audits
                parts: list[str] = []
                if missing:
                    parts.append(f"manifest has but matrix missing: {sorted(missing)}")
                if extra:
                    parts.append(f"matrix has but manifest missing: {sorted(extra)}")
                errors.append(
                    f"Route '{route_id}': audit list mismatch between "
                    f"manifest and ROUTING-MATRIX.md — {'; '.join(parts)}"
                )

        # Check 5c: hard_fail_keywords present in matrix section
        for heading_norm, route_id in name_to_id.items():
            section = matrix_sections.get(heading_norm, "")
            hf_match = re.search(
                r"### Hard fail\n(.*?)(?=\n## |\n### |\Z)",
                section,
                re.DOTALL,
            )
            if not hf_match:
                warnings.append(
                    f"Route '{route_id}': no '### Hard fail' section "
                    f"found in ROUTING-MATRIX.md"
                )
                continue
            hf_text = hf_match.group(1).lower()
            keywords = manifest_routes[route_id].get("hard_fail_keywords", [])
            missing_keywords: list[str] = []
            for kw in keywords:
                sig_words = [w for w in kw.lower().split() if len(w) > 3]
                if not sig_words:
                    continue
                matched = sum(1 for w in sig_words if w in hf_text)
                # Require >50% of significant words to match; <50% = probable deletion
                if matched == 0 or (
                    len(sig_words) >= 3 and matched < len(sig_words) / 2
                ):
                    missing_keywords.append(kw)
            if missing_keywords:
                errors.append(
                    f"Route '{route_id}': hard_fail_keywords with insufficient "
                    f"match in ROUTING-MATRIX.md hard-fail section: "
                    f"{missing_keywords}"
                )

    # ═══ Check 6: required fields per route ══════════════════════════════════
    required_fields = {
        "id", "display_name", "category", "aliases",
        "required_audits", "required_disciplines", "validator_bindings",
        "primary_reads", "trigger", "do_not_use", "often_confused_with",
        "artifact_contract", "hard_fail_keywords", "hard_fail_source",
    }
    for route in manifest["routes"]:
        missing_fields = required_fields - set(route.keys())
        if missing_fields:
            errors.append(
                f"Route '{route.get('id', '?')}' missing fields: {missing_fields}"
            )

    # ═══ Check 7: no duplicate hard_fail_keywords across routes ══════════════
    all_keywords: dict[str, str] = {}
    for route in manifest["routes"]:
        for kw in route.get("hard_fail_keywords", []):
            kw_lower = kw.lower().strip()
            if kw_lower in all_keywords and all_keywords[kw_lower] != route["id"]:
                warnings.append(
                    f"Hard-fail keyword '{kw}' claimed by both "
                    f"'{all_keywords[kw_lower]}' and '{route['id']}'"
                )
            all_keywords[kw_lower] = route["id"]

    # ═══ Check 8: evals/INDEX.md Primary/Secondary route columns ═════════════
    # Row layout: | Path | Primary route | Secondary route | ... — after
    # strip("|") + split("|"), cells[1] is the Primary route column and
    # cells[2] the Secondary route column.
    if EVALS_INDEX.is_file():
        index_text = EVALS_INDEX.read_text(encoding="utf-8")
        known_ids = manifest_ids | known_disciplines | _EVAL_TAG_WHITELIST
        for line in index_text.splitlines():
            errors.extend(_check_evals_index_line(line, known_ids))

    # ═══ Check 9: references/route-index.md trigger table ════════════════════
    if ROUTE_INDEX.is_file():
        index_text = ROUTE_INDEX.read_text(encoding="utf-8")
        route_audits = {
            rid: set(route.get("required_audits", []))
            for rid, route in manifest_routes.items()
        }
        errors.extend(_check_route_index(index_text, manifest_ids, route_audits))
    else:
        errors.append(
            f"references/route-index.md not found at {ROUTE_INDEX} — "
            f"cannot verify route-index consistency"
        )

    # ═══ Check 10: references/routes/*.md route cards (issue #380) ═══════════
    errors.extend(
        _check_route_cards(ROUTE_CARDS_DIR, manifest_routes, manifest_ids)
    )

    # ── Output ──────────────────────────────────────────────────────────────
    if errors:
        print(f"BLOCKING DRIFT DETECTED ({len(errors)} issue(s)):")
        for err in errors:
            print(f"  ✗ {err}")
        if warnings:
            print(f"\nWarnings ({len(warnings)}):")
            for warn in warnings:
                print(f"  ⚠ {warn}")
        return EXIT_FAIL

    if warnings:
        print(f"Warnings only ({len(warnings)}):")
        for warn in warnings:
            print(f"  ⚠ {warn}")
        return EXIT_WARN

    print("OK — manifest is consistent with registries, code and docs")
    return EXIT_OK


# ── CLI ──────────────────────────────────────────────────────────────────────


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Route manifest drift detector",
    )
    parser.add_argument(
        "--manifest",
        type=str,
        default=None,
        help=f"Path to route manifest JSON (default: {DEFAULT_MANIFEST})",
    )
    args = parser.parse_args(argv)

    manifest_path = Path(args.manifest) if args.manifest else DEFAULT_MANIFEST
    return validate(manifest_path)


if __name__ == "__main__":
    raise SystemExit(main())
