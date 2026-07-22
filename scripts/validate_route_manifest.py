#!/usr/bin/env python3
"""
Route manifest drift detector.

Validates that schemas/route-manifest.json is consistent with:
1. _ROUTE_ALIASES canonical targets in scripts/audit_report.py
2. ROUTE_VALIDATORS keys + non-empty validator lists in scripts/audit_report.py
3. Required audit checklist files in checklists/
4. ROUTING-MATRIX.md route headings (count, display name, audit lists, hard-fail keywords)
5. All manifest aliases are resolvable via _normalize_route logic
6. evals/INDEX.md Primary/Secondary route column values

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


def _parse_routing_matrix_route_sections(text: str) -> dict[str, str]:
    """Split ROUTING-MATRIX.md into per-route sections by '## Route: ' headings.

    Returns {normalized_heading: section_text}.  Normalized keys use
    _normalize_alias so they can be joined against manifest display_names.
    """
    sections: dict[str, str] = {}
    parts = re.split(r"^## Route: ", text, flags=re.M)
    for part in parts[1:]:  # Skip content before first ## Route:
        heading_end = part.index("\n") if "\n" in part else len(part)
        heading = part[:heading_end].strip()
        body = part[heading_end:]
        sections[_normalize_alias(heading)] = body
    return sections


def _parse_audits_from_matrix_section(section: str) -> list[str]:
    """Extract audit checklist names from a ROUTING-MATRIX.md route section.

    Looks for the ### Audit block and extracts `checklists/xxx.md` references.
    """
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


def _parse_matrix_route_name_to_id(headings: list[str], manifest_routes: dict[str, dict]) -> dict[str, str]:
    """Map normalized ROUTING-MATRIX.md headings to manifest route IDs."""
    mapping: dict[str, str] = {}
    for heading in headings:
        norm = _normalize_alias(heading)
        for route in manifest_routes.values():
            if _normalize_alias(route["display_name"]) == norm:
                mapping[norm] = route["id"]
                break
    return mapping


# ── Known cross-cutting discipline names (from evals/INDEX.md) ───────────────

_CROSS_CUTTING_DISCIPLINES: set[str] = {
    "source-traceability", "current-state", "forward-looking",
    "delivery-cleanliness", "decision-utility", "scope-completeness",
    "quantitative-role", "finance", "product-ranking", "ranking",
    "adversarial-input", "pdf-rendering", "pdf-build", "pdf-layout",
    "listing-status", "company-status", "company-status-boundary",
    "corporate-status", "valuation-methodology", "reporting-period",
    "comparative-analysis", "external-channel-preflight",
    "private-company", "listed-company-report",
}


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
    # P1-2a fix: require ROUTING-MATRIX.md, error if missing
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
                errors.append(
                    f"ROUTING-MATRIX.md headings not in manifest: "
                    f"{', '.join(sorted(matrix_norms[h] for h in missing_in_manifest))}"
                )
            if missing_in_matrix:
                errors.append(
                    f"Manifest display_names not in ROUTING-MATRIX.md: "
                    f"{', '.join(sorted(manifest_norms[h] for h in missing_in_matrix))}"
                )

        # ═══ Check 7b (P1-2b): Audit list per route comparison ═══════════════
        matrix_sections = _parse_routing_matrix_route_sections(matrix_text)
        name_to_id = _parse_matrix_route_name_to_id(matrix_headings, manifest_routes)

        for heading_norm, route_id in name_to_id.items():
            section = matrix_sections.get(heading_norm, "")
            matrix_audits = set(_parse_audits_from_matrix_section(section))
            manifest_audits = set(manifest_routes[route_id].get("required_audits", []))

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

        # ═══ Check 7c (P1-2c): hard_fail_keywords present in matrix section ══
        for heading_norm, route_id in name_to_id.items():
            section = matrix_sections.get(heading_norm, "")
            # Find the Hard fail subsection — capture from "### Hard fail"
            # to the next "## " or "### " or end of section
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
                if not any(w in hf_text for w in sig_words):
                    missing_keywords.append(kw)
            if missing_keywords:
                warnings.append(
                    f"Route '{route_id}': hard_fail_keywords not found in "
                    f"ROUTING-MATRIX.md hard-fail section: {missing_keywords}"
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

    # ═══ Check 10 (P2-1): evals/INDEX.md Primary/Secondary route columns ═════
    EVALS_INDEX = ROOT / "evals" / "INDEX.md"
    if EVALS_INDEX.is_file():
        index_text = EVALS_INDEX.read_text(encoding="utf-8")
        known_disciplines = _CROSS_CUTTING_DISCIPLINES | manifest_ids
        for line in index_text.splitlines():
            if not line.startswith("| `evals/cases/"):
                continue
            cells = [c.strip().strip("`") for c in line.strip("|").split("|")]
            if len(cells) >= 3:
                # cells[0] = Path, cells[1] = Primary route, cells[2] = Secondary route
                for col_idx, col_name in [(1, "Primary"), (2, "Secondary")]:
                    val = cells[col_idx] if col_idx < len(cells) else ""
                    if not val or val == "-":
                        continue
                    # The value may be a case file path or a discipline name
                    if "/" in val or val.endswith(".md"):
                        continue  # file path, not a route name
                    if val not in known_disciplines:
                        warnings.append(
                            f"evals/INDEX.md: '{val}' in {col_name} route column "
                            f"for {cells[0]} is not a known canonical route or "
                            f"cross-cutting discipline"
                        )

    # ═══ Check 11 (P2-2): ROUTE_VALIDATORS entries must be non-empty ═════════
    # Parse the validator lists to verify each has at least one entry
    vblock_match = re.search(
        r"ROUTE_VALIDATORS\s*:\s*dict\[str,\s*list\[ValidatorFn\]\]\s*=\s*\{(.+?)\n\s*\}",
        audit_source,
        re.DOTALL,
    )
    if vblock_match:
        vblock = vblock_match.group(1)
        empty_routes: list[str] = []
        for route_key in validator_keys:
            # Each entry looks like: "route-key": [\n  validator_fn,\n],
            # Check that the list between [ and ] contains at least one entry
            pattern = rf'"{re.escape(route_key)}"\s*:\s*\[(.*?)\]'
            m = re.search(pattern, vblock, re.DOTALL)
            if m:
                list_body = m.group(1).strip()
                if not list_body or list_body == "":
                    empty_routes.append(route_key)
        if empty_routes:
            errors.append(
                f"ROUTE_VALIDATORS entries are empty for: "
                f"{', '.join(sorted(empty_routes))}"
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
