#!/usr/bin/env python3
"""
Property-based and negative tests for route manifest drift detection.

Tests that schemas/route-manifest.json is consistent with:
1. _ROUTE_ALIASES canonical targets in scripts/audit_report.py
2. ROUTE_VALIDATORS keys in scripts/audit_report.py
3. Required audit checklist files in checklists/
4. ROUTING-MATRIX.md route count

Includes negative tests that deliberately create inconsistency to verify
the validator catches drift.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "schemas" / "route-manifest.json"
VALIDATOR_PATH = ROOT / "scripts" / "validate_route_manifest.py"


# ── Canonical route data extracted from audit_report.py (source of truth) ────
EXPECTED_CANONICAL_IDS = {
    "academic-review",
    "competitive-positioning",
    "constrained-choice",
    "equipment-selection",
    "listed-company",
    "market-entry",
    "market-outlook",
    "provider-selection",
    "regulatory-analysis",
    "shared-workflow",
    "startup-evaluation",
    "technical-deep-dive",
}

REQUIRED_MANIFEST_FIELDS = {
    "id",
    "display_name",
    "category",
    "aliases",
    "required_audits",
    "hard_fail_keywords",
}

ALLOWED_CATEGORIES = {"specialized", "shared-workflow"}


# ── Helpers ──────────────────────────────────────────────────────────────────

def _load_manifest(path: Path) -> dict:
    """Load and validate top-level structure of a manifest file."""
    text = path.read_text(encoding="utf-8")
    manifest = json.loads(text)
    assert "version" in manifest, "Missing 'version' field"
    assert "routes" in manifest, "Missing 'routes' field"
    assert isinstance(manifest["routes"], list), "'routes' must be a list"
    return manifest


def _make_temp_manifest(routes: list[dict]) -> Path:
    """Create a temporary manifest file for testing."""
    content = json.dumps({"version": 1, "routes": routes}, indent=2)
    f = tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False, encoding="utf-8",
    )
    f.write(content)
    f.close()
    return Path(f.name)


def _run_validator(
    manifest_path: Path | None = None,
    extra_args: list[str] | None = None,
) -> subprocess.CompletedProcess:
    """Run validate_route_manifest.py on the given manifest path."""
    cmd = [sys.executable, str(VALIDATOR_PATH)]
    if manifest_path is not None:
        cmd.extend(["--manifest", str(manifest_path)])
    if extra_args:
        cmd.extend(extra_args)
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=30,
        cwd=str(ROOT),
    )


# ── Tests ────────────────────────────────────────────────────────────────────


class TestManifestExistsAndIsValid:
    """The real manifest file must exist, be parseable, and have valid structure."""

    def test_manifest_file_exists(self) -> None:
        assert MANIFEST_PATH.is_file(), f"Missing: {MANIFEST_PATH}"

    def test_manifest_is_valid_json(self) -> None:
        manifest = _load_manifest(MANIFEST_PATH)
        assert manifest["version"] >= 1

    def test_manifest_has_all_12_routes(self) -> None:
        manifest = _load_manifest(MANIFEST_PATH)
        route_ids = {r["id"] for r in manifest["routes"]}
        missing = EXPECTED_CANONICAL_IDS - route_ids
        extra = route_ids - EXPECTED_CANONICAL_IDS
        assert not missing, f"Manifest missing routes: {missing}"
        assert not extra, f"Manifest has unexpected routes: {extra}"

    def test_every_route_has_required_fields(self) -> None:
        manifest = _load_manifest(MANIFEST_PATH)
        for route in manifest["routes"]:
            missing_fields = REQUIRED_MANIFEST_FIELDS - set(route.keys())
            assert not missing_fields, (
                f"Route '{route.get('id', '?')}' missing fields: {missing_fields}"
            )

    def test_all_route_ids_are_valid_format(self) -> None:
        """Route IDs must be lowercase-hyphenated, no spaces."""
        manifest = _load_manifest(MANIFEST_PATH)
        for route in manifest["routes"]:
            rid = route["id"]
            assert rid == rid.lower(), f"Route ID not lowercase: {rid}"
            assert " " not in rid, f"Route ID contains space: {rid}"
            assert rid.isascii(), f"Route ID not ASCII: {rid}"

    def test_all_categories_are_valid(self) -> None:
        manifest = _load_manifest(MANIFEST_PATH)
        for route in manifest["routes"]:
            assert route["category"] in ALLOWED_CATEGORIES, (
                f"Route '{route['id']}' has invalid category: {route['category']}"
            )

    def test_no_duplicate_route_ids(self) -> None:
        manifest = _load_manifest(MANIFEST_PATH)
        ids = [r["id"] for r in manifest["routes"]]
        assert len(ids) == len(set(ids)), f"Duplicate route IDs: {ids}"

    def test_every_route_has_non_empty_display_name(self) -> None:
        manifest = _load_manifest(MANIFEST_PATH)
        for route in manifest["routes"]:
            assert route["display_name"].strip(), (
                f"Route '{route['id']}' has empty display_name"
            )

    def test_every_route_has_at_least_one_alias(self) -> None:
        manifest = _load_manifest(MANIFEST_PATH)
        for route in manifest["routes"]:
            assert len(route["aliases"]) >= 1, (
                f"Route '{route['id']}' has no aliases"
            )


class TestValidatorAgainstRealManifest:
    """The validator must pass against the real manifest."""

    def test_validator_exit_zero_on_real_manifest(self) -> None:
        result = _run_validator(MANIFEST_PATH)
        assert result.returncode == 0, (
            f"Validator exited {result.returncode} on real manifest\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )

    def test_validator_output_contains_ok(self) -> None:
        result = _run_validator(MANIFEST_PATH)
        output = result.stdout + result.stderr
        assert "OK" in output or "pass" in output.lower(), (
            f"Expected 'OK' or 'pass' in output, got:\n{output}"
        )


class TestValidatorRejectsDrift:
    """Negative tests: validator must detect inconsistency."""

    def test_missing_route_is_detected(self) -> None:
        """A manifest missing a canonical route should fail."""
        routes = [
            {"id": rid, "display_name": rid, "category": "specialized",
             "aliases": [rid], "required_audits": ["final-audit"],
             "hard_fail_keywords": ["test"]}
            for rid in sorted(EXPECTED_CANONICAL_IDS - {"shared-workflow"})
        ]
        tmp = _make_temp_manifest(routes)
        try:
            result = _run_validator(tmp)
            assert result.returncode != 0, (
                f"Should fail (missing route), got exit {result.returncode}\n"
                f"stdout:\n{result.stdout}"
            )
        finally:
            tmp.unlink(missing_ok=True)

    def test_extra_unknown_route_is_detected(self) -> None:
        """A manifest with an unknown route ID should fail."""
        routes = [
            {"id": rid, "display_name": rid, "category": "specialized",
             "aliases": [rid], "required_audits": ["final-audit"],
             "hard_fail_keywords": ["test"]}
            for rid in sorted(EXPECTED_CANONICAL_IDS)
        ] + [
            {"id": "unknown-fake-route", "display_name": "Fake Route",
             "category": "specialized", "aliases": ["fake"],
             "required_audits": ["final-audit"],
             "hard_fail_keywords": ["test"]}
        ]
        tmp = _make_temp_manifest(routes)
        try:
            result = _run_validator(tmp)
            assert result.returncode != 0, (
                f"Should fail (extra route), got exit {result.returncode}\n"
                f"stdout:\n{result.stdout}"
            )
        finally:
            tmp.unlink(missing_ok=True)

    def test_wrong_audit_list_is_detected(self) -> None:
        """A manifest with wrong required_audits should fail."""
        real = _load_manifest(MANIFEST_PATH)
        routes = []
        for r in real["routes"]:
            r_copy = dict(r)
            if r_copy["id"] == "technical-deep-dive":
                r_copy["required_audits"] = ["wrong-audit-name"]
            routes.append(r_copy)
        tmp = _make_temp_manifest(routes)
        try:
            result = _run_validator(tmp)
            assert result.returncode != 0, (
                f"Should fail (wrong audit), got exit {result.returncode}\n"
                f"stdout:\n{result.stdout}"
            )
        finally:
            tmp.unlink(missing_ok=True)

    def test_duplicate_alias_is_detected(self) -> None:
        """A manifest where two routes share an alias should fail."""
        routes = [
            {
                "id": "technical-deep-dive",
                "display_name": "TD",
                "category": "specialized",
                "aliases": ["shared-alias", "tech"],
                "required_audits": ["final-audit"],
                "hard_fail_keywords": ["test"],
            },
            {
                "id": "constrained-choice",
                "display_name": "CC",
                "category": "specialized",
                "aliases": ["shared-alias", "choice"],
                "required_audits": ["final-audit"],
                "hard_fail_keywords": ["test"],
            },
        ]
        tmp = _make_temp_manifest(routes)
        try:
            result = _run_validator(tmp)
            assert result.returncode != 0, (
                f"Should fail (duplicate alias), got exit {result.returncode}\n"
                f"stdout:\n{result.stdout}"
            )
        finally:
            tmp.unlink(missing_ok=True)

    def test_alias_not_in_route_aliases_is_detected(self) -> None:
        """N3: Manifest alias that cannot be resolved via _ROUTE_ALIASES.

        This is the exact B1/B2 scenario from the code review: a manifest
        declares an alias that has no corresponding entry in _ROUTE_ALIASES
        and cannot be resolved via space→hyphen fallback to the correct ID.
        """
        routes = [
            {
                "id": "technical-deep-dive",
                "display_name": "TD",
                "category": "specialized",
                "aliases": ["technical deep-dive", "nonexistent-alias-xyz"],
                "required_audits": ["technical-analysis-audit",
                                    "source-traceability", "final-audit"],
                "hard_fail_keywords": ["test"],
            },
        ]
        tmp = _make_temp_manifest(routes)
        try:
            result = _run_validator(tmp)
            output = result.stdout + result.stderr
            assert result.returncode != 0, (
                f"Should fail (unresolvable alias), got exit {result.returncode}\n"
                f"output:\n{output}"
            )
        finally:
            tmp.unlink(missing_ok=True)


class TestValidatorReturnsCorrectExitCodes:
    """Validator exit codes must be well-defined."""

    def test_exit_0_for_consistent_manifest(self) -> None:
        result = _run_validator(MANIFEST_PATH)
        assert result.returncode == 0

    def test_exit_nonzero_for_missing_file(self) -> None:
        result = _run_validator(Path("/nonexistent/manifest.json"))
        assert result.returncode != 0, (
            f"Should fail on missing file, got exit {result.returncode}"
        )

    def test_exit_nonzero_for_invalid_json(self) -> None:
        f = tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8",
        )
        f.write("not valid json {{{")
        f.close()
        tmp = Path(f.name)
        try:
            result = _run_validator(tmp)
            assert result.returncode != 0, (
                f"Should fail on invalid JSON, got exit {result.returncode}"
            )
        finally:
            tmp.unlink(missing_ok=True)

    def test_exit_nonzero_for_missing_version(self) -> None:
        tmp = _make_temp_manifest([{"id": "test", "display_name": "T",
                                    "category": "specialized",
                                    "aliases": ["t"], "required_audits": [],
                                    "hard_fail_keywords": []}])
        content = json.dumps({"routes": [{"id": "test"}]})
        tmp.write_text(content)
        try:
            result = _run_validator(tmp)
            assert result.returncode != 0, (
                f"Should fail on missing version, got exit {result.returncode}"
            )
        finally:
            tmp.unlink(missing_ok=True)


if __name__ == "__main__":
    passed = 0
    failed = 0
    test_classes = [
        TestManifestExistsAndIsValid,
        TestValidatorAgainstRealManifest,
        TestValidatorRejectsDrift,
        TestValidatorReturnsCorrectExitCodes,
    ]
    for cls in test_classes:
        instance = cls()
        for name in dir(instance):
            if name.startswith("test_"):
                try:
                    getattr(instance, name)()
                    print(f"  PASS  {cls.__name__}.{name}")
                    passed += 1
                except AssertionError as e:
                    print(f"  FAIL  {cls.__name__}.{name}: {e}")
                    failed += 1
                except Exception as e:
                    print(f"  ERROR {cls.__name__}.{name}: {e}")
                    failed += 1

    print(f"\n{passed} passed, {failed} failed")
    sys.exit(0 if failed == 0 else 1)
