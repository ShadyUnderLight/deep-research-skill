#!/usr/bin/env python3
"""
Route manifest drift detector.

Validates that schemas/route-manifest.json is consistent with:
1. _ROUTE_ALIASES canonical targets in scripts/audit_report.py
2. ROUTE_VALIDATORS keys in scripts/audit_report.py
3. Required audit checklist files in checklists/
4. ROUTING-MATRIX.md route headings (count + display name comparison)
5. All manifest aliases are resolvable via _normalize_route logic

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

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "schemas" / "route-manifest.json"
AUDIT_REPORT = ROOT / "scripts" / "audit_report.py"
ROUTING_MATRIX = ROOT / "ROUTING-MATRIX.md"
CHECKLISTS_DIR = ROOT / "checklists"

EXIT_OK = 0
EXIT_WARN = 1
EXIT_FAIL = 2


# ── Normalization helpers ─────────────────────────────────────────────────────


def _normalize_alias(name: str) -> str:
    """Normalize a display name or alias for comparison.

    Lowercase, collapse whitespace, strip trailing parenthetical notes.
    Mirrors the behavior of _normalize_route in audit_report.py.
    """
    normalized = " ".join(name.strip().lower().split())
    no_paren = re.sub(r"\s*\([^)]*\)\s*$", "", normalized).strip()
    return no_paren if no_paren else normalized


def _resolve_via_routing(
    name: str,
    alias_map: dict[str, str],
    canonical_ids: set[str],
) -> tuple[str | None, bool]:
    """Simulate _normalize_route behavior from audit_report.py.

    Returns (canonical_id, used_fallback).
    - canonical_id is None if the name cannot resolve to a known canonical ID.
    - used_fallback is True if the name resolved via space→hyphen fallback
      (not via explicit _ROUTE_ALIASES entry).
    """
    normalized = _normalize_alias(name)

    # 1. Direct alias lookup (exact match in _ROUTE_ALIASES keys)
    if normalized in alias_map:
        return alias_map[normalized], False

    # 2. Strip parenthetical notes and retry
    no_paren = re.sub(r"\s*\([^)]*\)\s*$", "", normalized).strip()
    if no_paren and no_paren != normalized:
        if no_paren in alias_map:
            return alias_map[no_paren], False
        normalized = no_paren

    # 3. Space→hyphen fallback heuristic
    fallback = normalized.replace(" ", "-")
    if fallback in canonical_ids:
        return fallback, True

    return None, False


# ── Parser for audit_report.py source ────────────────────────────────────────


def _parse_route_aliases(source: str) -> dict[str, str]:
    """Extract _ROUTE_ALIASES dict from audit_report.py source.

    Returns {display_name: canonical_id}. Assumes all keys and values are
    simple string literals (no nested braces in values).
    """
    match = re.search(
        r"_ROUTE_ALIASES\s*:\s*dict\[str,\s*str\]\s*=\s*\{(.+?)\n\s*\}",
        source,
        re.DOTALL,
    )
    if not match:
        raise SystemExit(f"ERROR: Cannot find _ROUTE_ALIASES in {AUDIT_REPORT}")

    block = match.group(1)
    pairs = re.findall(
        r'"([^"]+)"\s*:\s*"([^"]+)"',
        block,
    )
    if not pairs:
        raise SystemExit(f"ERROR: No entries found in _ROUTE_ALIASES")
    return {k.strip(): v.strip() for k, v in pairs}


def _parse_route_validator_keys(source: str) -> set[str]:
    """Extract ROUTE_VALIDATORS keys from audit_report.py source."""
    match = re.search(
        r"ROUTE_VALIDATORS\s*:\s*dict\[str,\s*list\[ValidatorFn\]\]\s*=\s*\{(.+?)\n\s*\}",
        source,
        re.DOTALL,
    )
    if not match:
        raise SystemExit(f"ERROR: Cannot find ROUTE_VALIDATORS in {AUDIT_REPORT}")

    block = match.group(1)
    keys = re.findall(r'"([a-z][a-z-]*[a-z])"', block)
    # Exclude short non-route strings that might accidentally match
    return {k for k in keys if len(k) > 4}


def _parse_routing_matrix_headings(text: str) -> list[str]:
    """Extract route heading display names from ROUTING-MATRIX.md."""
    return re.findall(r"^## Route: (.+)$", text, re.M)


# ── Validation logic ─────────────────────────────────────────────────────────


def _load_manifest(path: Path) -> dict:
    """Load and validate top-level manifest structure."""
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"ERROR: Manifest file not found: {path}")
    except json.JSONDecodeError as e:
        raise SystemExit(f"ERROR: Invalid JSON in {path}: {e}")

    if "version" not in manifest:
        raise SystemExit(f"ERROR: Missing 'version' field in {path}")
    if "routes" not in manifest:
        raise SystemExit(f"ERROR: Missing 'routes' field in {path}")
    if not isinstance(manifest["routes"], list):
        raise SystemExit(f"ERROR: 'routes' must be a list in {path}")
    return manifest


def validate(path: Path | None = None) -> int:
    """Run full drift validation. Returns exit code."""
    manifest_path = path or DEFAULT_MANIFEST
    manifest = _load_manifest(manifest_path)

    if not AUDIT_REPORT.is_file():
        raise SystemExit(f"ERROR: {AUDIT_REPORT} not found")

    audit_source = AUDIT_REPORT.read_text(encoding="utf-8")
    alias_map = _parse_route_aliases(audit_source)
    validator_keys = _parse_route_validator_keys(audit_source)

    errors: list[str] = []
    warnings: list[str] = []

    # Extract manifest data
    manifest_routes: dict[str, dict] = {}
    manifest_ids: set[str] = set()
    for route in manifest["routes"]:
        rid = route["id"]
        if rid in manifest_routes:
            errors.append(f"Duplicate route ID in manifest: {rid}")
        manifest_routes[rid] = route
        manifest_ids.add(rid)

    # ═══ Check 1: ROUTE_VALIDATORS ↔ manifest bidirectional ═════════════════
    missing_from_manifest = validator_keys - manifest_ids
    if missing_from_manifest:
        errors.append(
            f"Routes in ROUTE_VALIDATORS but NOT in manifest: "
            f"{', '.join(sorted(missing_from_manifest))}"
        )

    missing_from_validators = manifest_ids - validator_keys
    if missing_from_validators:
        errors.append(
            f"Routes in manifest but NOT in ROUTE_VALIDATORS: "
            f"{', '.join(sorted(missing_from_validators))}"
        )

    # ═══ Check 2: _ROUTE_ALIASES canonical targets all in manifest ═══════════
    alias_targets = set(alias_map.values())
    missing_targets = alias_targets - manifest_ids
    if missing_targets:
        errors.append(
            f"_ROUTE_ALIASES canonical targets not in manifest: "
            f"{', '.join(sorted(missing_targets))}"
        )

    # ═══ Check 3: Manifest aliases — no duplicates across routes ═════════════
    all_aliases_norm: dict[str, str] = {}  # normalized alias → route_id
    for route in manifest["routes"]:
        for alias in route.get("aliases", []):
            norm = _normalize_alias(alias)
            if norm in all_aliases_norm and all_aliases_norm[norm] != route["id"]:
                errors.append(
                    f"Duplicate alias '{alias}' (normalized: '{norm}') "
                    f"claimed by both '{all_aliases_norm[norm]}' and '{route['id']}'"
                )
            all_aliases_norm[norm] = route["id"]

    # ═══ Check 4: Every manifest alias must resolve correctly ════════════════
    # (This is the strengthened check — catches B1/B2 from code review)
    for route in manifest["routes"]:
        route_id = route["id"]
        has_explicit_match = False
        for alias in route.get("aliases", []):
            resolved, used_fallback = _resolve_via_routing(
                alias, alias_map, manifest_ids
            )
            if resolved is None:
                errors.append(
                    f"Manifest alias '{alias}' for route '{route_id}' "
                    f"cannot be resolved via _normalize_route"
                )
            elif resolved != route_id:
                errors.append(
                    f"Manifest alias '{alias}' for route '{route_id}' "
                    f"resolves to '{resolved}' — target mismatch"
                )
            elif not used_fallback:
                has_explicit_match = True
        if not has_explicit_match and route_id != "shared-workflow":
            warnings.append(
                f"Route '{route_id}' has no explicit alias in _ROUTE_ALIASES; "
                f"all aliases rely on space→hyphen fallback"
            )

    # ═══ Check 5: All _ROUTE_ALIASES keys represented in manifest ════════════
    manifest_alias_norms: dict[str, str] = {}  # normalized → route_id
    for route in manifest["routes"]:
        for alias in route.get("aliases", []):
            manifest_alias_norms[_normalize_alias(alias)] = route["id"]

    for alias_key, target in alias_map.items():
        norm = _normalize_alias(alias_key)
        if norm not in manifest_alias_norms:
            warnings.append(
                f"_ROUTE_ALIASES key '{alias_key}' (→{target}) "
                f"has no corresponding alias in manifest"
            )
        elif manifest_alias_norms[norm] != target:
            warnings.append(
                f"_ROUTE_ALIASES key '{alias_key}' maps to '{target}' "
                f"but manifest alias maps to '{manifest_alias_norms[norm]}'"
            )

    # ═══ Check 6: Required audits reference existing checklist files ═════════
    existing_checklists = {p.stem for p in CHECKLISTS_DIR.glob("*.md")}
    for route in manifest["routes"]:
        for audit in route.get("required_audits", []):
            if audit not in existing_checklists:
                errors.append(
                    f"Route '{route['id']}' requires audit '{audit}' "
                    f"but checklist file 'checklists/{audit}.md' does not exist"
                )

    # ═══ Check 7: ROUTING-MATRIX.md route count + display name comparison ════
    if ROUTING_MATRIX.is_file():
        matrix_text = ROUTING_MATRIX.read_text(encoding="utf-8")
        matrix_headings = _parse_routing_matrix_headings(matrix_text)
        specialized_in_manifest = sum(
            1 for r in manifest["routes"] if r.get("category") == "specialized"
        )

        if len(matrix_headings) != specialized_in_manifest:
            errors.append(
                f"ROUTING-MATRIX.md has {len(matrix_headings)} route sections, "
                f"manifest has {specialized_in_manifest} specialized routes — drift detected"
            )
        else:
            # Compare display names (normalized)
            matrix_norms = {_normalize_alias(h): h for h in matrix_headings}
            manifest_display_names = [
                r["display_name"] for r in manifest["routes"]
                if r.get("category") == "specialized"
            ]
            manifest_norms = {_normalize_alias(d): d for d in manifest_display_names}

            missing_in_manifest = set(matrix_norms.keys()) - set(manifest_norms.keys())
            missing_in_matrix = set(manifest_norms.keys()) - set(matrix_norms.keys())

            if missing_in_manifest:
                warnings.append(
                    f"ROUTING-MATRIX.md headings not in manifest: "
                    f"{', '.join(sorted(matrix_norms[h] for h in missing_in_manifest))}"
                )
            if missing_in_matrix:
                warnings.append(
                    f"Manifest display_names not in ROUTING-MATRIX.md: "
                    f"{', '.join(sorted(manifest_norms[h] for h in missing_in_matrix))}"
                )

    # ═══ Check 8: Manifest required fields per route ══════════════════════════
    required_fields = {
        "id", "display_name", "category", "aliases",
        "required_audits", "hard_fail_keywords",
    }
    for route in manifest["routes"]:
        missing_fields = required_fields - set(route.keys())
        if missing_fields:
            errors.append(
                f"Route '{route.get('id', '?')}' missing fields: {missing_fields}"
            )

    # ═══ Check 9: No duplicate hard_fail_keywords across routes ══════════════
    all_keywords: dict[str, str] = {}  # lowercase keyword → route_id
    for route in manifest["routes"]:
        for kw in route.get("hard_fail_keywords", []):
            kw_lower = kw.lower().strip()
            if kw_lower in all_keywords and all_keywords[kw_lower] != route["id"]:
                warnings.append(
                    f"Hard-fail keyword '{kw}' claimed by both "
                    f"'{all_keywords[kw_lower]}' and '{route['id']}'"
                )
            all_keywords[kw_lower] = route["id"]

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

    print("OK — manifest is consistent with code and docs")
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
