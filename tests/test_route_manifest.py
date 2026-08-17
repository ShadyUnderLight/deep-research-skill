#!/usr/bin/env python3
"""
Property-based and negative tests for route manifest drift detection.

Tests that schemas/route-manifest.json is consistent with:
1. schemas/discipline-registry.json — required_disciplines
2. schemas/audit-registry.json — required_audits
3. Required audit checklist files in checklists/
4. ROUTING-MATRIX.md route count / display names / audit lists / hard-fail
5. scripts/registry_loader.py runtime loading and alias resolution

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
    "required_disciplines",
    "validator_bindings",
    "primary_reads",
    "trigger",
    "do_not_use",
    "often_confused_with",
    "artifact_contract",
    "hard_fail_keywords",
    "hard_fail_source",
}

KNOWN_VALIDATOR_IDS = {
    "report-quality",
    "declared-execution",
    "table-role-labels",
    "source-label-consistency",
    "listed-company-delivery",
    "scoring-replicability",
    "market-outlook-monitoring-actionability",
    "secondary-route-check",
    "contract-check",
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
    content = json.dumps({"version": 2, "routes": routes}, indent=2)
    f = tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False, encoding="utf-8",
    )
    f.write(content)
    f.close()
    return Path(f.name)


def _real_routes_with(mutate) -> list[dict]:
    """Copy the real manifest routes and apply a mutation to one route.

    Negative tests must start from a structurally complete manifest so
    they fail on the *target* drift, not on missing control-plane fields.
    """
    manifest = _load_manifest(MANIFEST_PATH)
    routes = []
    for r in manifest["routes"]:
        r_copy = dict(r)
        r_copy["aliases"] = list(r["aliases"])
        r_copy["required_audits"] = list(r["required_audits"])
        r_copy["hard_fail_keywords"] = list(r["hard_fail_keywords"])
        r_copy["required_disciplines"] = list(r["required_disciplines"])
        r_copy["validator_bindings"] = list(r["validator_bindings"])
        r_copy["primary_reads"] = list(r["primary_reads"])
        r_copy["often_confused_with"] = list(r["often_confused_with"])
        mutate(r_copy)
        routes.append(r_copy)
    return routes


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

    def test_every_route_has_validator_bindings(self) -> None:
        """Each route must dispatch to a non-empty, known validator set."""
        manifest = _load_manifest(MANIFEST_PATH)
        for route in manifest["routes"]:
            bindings = route["validator_bindings"]
            assert bindings, f"Route '{route['id']}' has empty validator_bindings"
            unknown = set(bindings) - KNOWN_VALIDATOR_IDS
            assert not unknown, (
                f"Route '{route['id']}' unknown validator bindings: {unknown}"
            )

    def test_every_route_has_required_disciplines(self) -> None:
        """required_disciplines must be non-empty for specialized routes and
        reference discipline ids registered in schemas/discipline-registry.json."""
        manifest = _load_manifest(MANIFEST_PATH)
        registry_path = ROOT / "schemas" / "discipline-registry.json"
        known = {d["id"] for d in json.loads(registry_path.read_text())["disciplines"]}
        for route in manifest["routes"]:
            if route["category"] == "specialized":
                assert route["required_disciplines"], (
                    f"Specialized route '{route['id']}' has no required_disciplines"
                )
            unknown = set(route["required_disciplines"]) - known
            assert not unknown, (
                f"Route '{route['id']}' unknown disciplines: {unknown}"
            )

    def test_every_route_has_primary_reads(self) -> None:
        """primary_reads must reference files that exist on disk."""
        manifest = _load_manifest(MANIFEST_PATH)
        for route in manifest["routes"]:
            assert route["primary_reads"], (
                f"Route '{route['id']}' has empty primary_reads"
            )
            for ref in route["primary_reads"]:
                assert (ROOT / ref).is_file(), (
                    f"Route '{route['id']}' primary read missing: {ref}"
                )

    def test_every_route_has_trigger_and_boundary_fields(self) -> None:
        manifest = _load_manifest(MANIFEST_PATH)
        for route in manifest["routes"]:
            assert route["trigger"].strip(), f"Route '{route['id']}' empty trigger"
            assert route["do_not_use"].strip(), (
                f"Route '{route['id']}' empty do_not_use"
            )
            assert route["often_confused_with"], (
                f"Route '{route['id']}' empty often_confused_with"
            )
            assert route["artifact_contract"].strip(), (
                f"Route '{route['id']}' empty artifact_contract"
            )
            assert route["hard_fail_source"].strip(), (
                f"Route '{route['id']}' empty hard_fail_source"
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
        """A manifest missing a canonical route should fail.

        The manifest is the single fact source now, so a missing route
        surfaces as a ROUTING-MATRIX.md count drift (matrix still lists it).
        """
        routes = [
            r for r in _real_routes_with(lambda r: None)
            if r["id"] != "academic-review"
        ]
        tmp = _make_temp_manifest(routes)
        try:
            result = _run_validator(tmp)
            output = result.stdout + result.stderr
            assert result.returncode != 0, (
                f"Should fail (missing route), got exit {result.returncode}\n"
                f"output:\n{output}"
            )
            assert "drift" in output.lower(), (
                f"Expected drift message, got:\n{output}"
            )
        finally:
            tmp.unlink(missing_ok=True)

    def test_extra_unknown_route_is_detected(self) -> None:
        """A manifest with an unknown route ID should fail.

        Extra specialized route surfaces as ROUTING-MATRIX.md count drift.
        """
        routes = _real_routes_with(lambda r: None) + [{
            "id": "unknown-fake-route",
            "display_name": "Fake Route",
            "category": "specialized",
            "aliases": ["fake"],
            "required_audits": ["final-audit"],
            "required_disciplines": [],
            "validator_bindings": ["report-quality"],
            "primary_reads": ["references/decision-report-template.md"],
            "trigger": "trigger",
            "do_not_use": "do not use",
            "often_confused_with": ["constrained-choice"],
            "artifact_contract": "artifact",
            "hard_fail_keywords": ["test"],
            "hard_fail_source": "ROUTING-MATRIX.md#fake",
        }]
        tmp = _make_temp_manifest(routes)
        try:
            result = _run_validator(tmp)
            output = result.stdout + result.stderr
            assert result.returncode != 0, (
                f"Should fail (extra route), got exit {result.returncode}\n"
                f"output:\n{output}"
            )
            assert "drift" in output.lower(), (
                f"Expected drift message, got:\n{output}"
            )
        finally:
            tmp.unlink(missing_ok=True)

    def test_wrong_audit_list_is_detected(self) -> None:
        """A manifest with wrong required_audits should fail."""
        routes = _real_routes_with(
            lambda r: r.update(required_audits=["wrong-audit-name"])
            if r["id"] == "technical-deep-dive" else None
        )
        tmp = _make_temp_manifest(routes)
        try:
            result = _run_validator(tmp)
            output = result.stdout + result.stderr
            assert result.returncode != 0, (
                f"Should fail (wrong audit), got exit {result.returncode}\n"
                f"output:\n{output}"
            )
            assert "audit" in output.lower(), (
                f"Expected audit message, got:\n{output}"
            )
        finally:
            tmp.unlink(missing_ok=True)

    def test_duplicate_alias_is_detected(self) -> None:
        """A manifest where two routes share an alias should fail."""
        routes = _real_routes_with(lambda r: None)
        routes[0]["aliases"].append("duplicated-alias-name")
        routes[1]["aliases"].append("duplicated-alias-name")
        tmp = _make_temp_manifest(routes)
        try:
            result = _run_validator(tmp)
            output = result.stdout + result.stderr
            assert result.returncode != 0, (
                f"Should fail (duplicate alias), got exit {result.returncode}\n"
                f"output:\n{output}"
            )
            assert "duplicate alias" in output.lower(), (
                f"Expected duplicate alias message, got:\n{output}"
            )
        finally:
            tmp.unlink(missing_ok=True)

    def test_audit_list_drift_is_detected(self) -> None:
        """P1-2b: Manifest audit list not matching ROUTING-MATRIX.md.

        Uses the real manifest but modifies a route's required_audits
        to differ from what's in ROUTING-MATRIX.md.
        """
        routes = _real_routes_with(
            lambda r: r.update(required_audits=[
                "market-outlook-audit", "source-traceability", "final-audit",
            ])
            if r["id"] == "market-outlook" else None
        )
        tmp = _make_temp_manifest(routes)
        try:
            result = _run_validator(tmp)
            output = result.stdout + result.stderr
            assert result.returncode != 0, (
                f"Should fail (audit drift), got exit {result.returncode}\n"
                f"output:\n{output}"
            )
            assert "audit list mismatch" in output.lower(), (
                f"Expected audit mismatch message, got:\n{output}"
            )
        finally:
            tmp.unlink(missing_ok=True)

    def test_empty_validator_bindings_is_detected(self) -> None:
        """A manifest route with no validator bindings must fail."""
        routes = _real_routes_with(
            lambda r: r.update(validator_bindings=[])
            if r["id"] == "market-entry" else None
        )
        tmp = _make_temp_manifest(routes)
        try:
            result = _run_validator(tmp)
            output = result.stdout + result.stderr
            assert result.returncode != 0, (
                f"Should fail (empty validator bindings), "
                f"got exit {result.returncode}\noutput:\n{output}"
            )
            assert "validator_bindings" in output.lower(), (
                f"Expected validator_bindings message, got:\n{output}"
            )
        finally:
            tmp.unlink(missing_ok=True)

    def test_unknown_discipline_is_detected(self) -> None:
        """A route referencing an unregistered discipline must fail."""
        routes = _real_routes_with(
            lambda r: r.update(required_disciplines=["fake-discipline-xyz"])
            if r["id"] == "constrained-choice" else None
        )
        tmp = _make_temp_manifest(routes)
        try:
            result = _run_validator(tmp)
            output = result.stdout + result.stderr
            assert result.returncode != 0, (
                f"Should fail (unknown discipline), "
                f"got exit {result.returncode}\noutput:\n{output}"
            )
            assert "discipline" in output.lower(), (
                f"Expected discipline message, got:\n{output}"
            )
        finally:
            tmp.unlink(missing_ok=True)

    def test_evals_index_check_no_false_positive(self) -> None:
        """P2-1: evals/INDEX.md check against real manifest must not crash."""
        result = _run_validator(MANIFEST_PATH)
        output = result.stdout
        assert "OK" in output, (
            f"Validator should pass on real manifest+index:\n{output}"
        )


class TestEvalsIndexColumns:
    """evals/INDEX.md route columns must be checked against canonical ids.

    Row layout is | Path | Primary route | Secondary route | ... — after
    strip("|") + split("|"), cells[1] is Primary, cells[2] is Secondary.
    """

    @staticmethod
    def _known() -> set[str]:
        return {"technical-deep-dive", "listed-company", "current-state",
                "source-traceability", "pdf-rendering"}

    @staticmethod
    def _row(primary: str, secondary: str) -> str:
        return (
            f"| `evals/cases/some-case.md` | {primary} | {secondary} | "
            f"some-failure-family |"
        )

    def test_unknown_primary_route_is_detected(self) -> None:
        sys.path.insert(0, str(ROOT / "scripts"))
        import validate_route_manifest as v
        errors = v._check_evals_index_line(
            self._row("fake-unknown-primary", "source-traceability"),
            self._known(),
        )
        assert errors, "Unknown Primary route must be detected"
        assert "Primary route" in errors[0]
        assert "fake-unknown-primary" in errors[0]

    def test_unknown_secondary_route_is_detected(self) -> None:
        sys.path.insert(0, str(ROOT / "scripts"))
        import validate_route_manifest as v
        errors = v._check_evals_index_line(
            self._row("listed-company", "fake-unknown-secondary"),
            self._known(),
        )
        assert errors, "Unknown Secondary route must be detected"
        assert "Secondary route" in errors[0]

    def test_known_values_pass(self) -> None:
        sys.path.insert(0, str(ROOT / "scripts"))
        import validate_route_manifest as v
        errors = v._check_evals_index_line(
            self._row("listed-company", "source-traceability"),
            self._known(),
        )
        assert errors == []

    def test_slash_joined_disciplines_are_split(self) -> None:
        sys.path.insert(0, str(ROOT / "scripts"))
        import validate_route_manifest as v
        errors = v._check_evals_index_line(
            self._row("current-state/source-traceability", "-"),
            self._known(),
        )
        assert errors == []

    def test_dash_and_empty_secondary_pass(self) -> None:
        sys.path.insert(0, str(ROOT / "scripts"))
        import validate_route_manifest as v
        errors = v._check_evals_index_line(
            self._row("technical-deep-dive", "-"),
            self._known(),
        )
        assert errors == []

    def test_non_data_rows_are_ignored(self) -> None:
        sys.path.insert(0, str(ROOT / "scripts"))
        import validate_route_manifest as v
        errors = v._check_evals_index_line("| Path | Primary route |", self._known())
        assert errors == []


class TestRouteIndexConsistency:
    """references/route-index.md must stay in sync with the manifest
    (#374 acceptance: route count / trigger / audits without drift)."""

    @staticmethod
    def _index_with_rows(rows: list[str]) -> str:
        header = (
            "| Route ID | Trigger keywords | Reads | Audits | Card |\n"
            "|----------|-----------------|-------|--------|------|\n"
        )
        return header + "\n".join(rows)

    @staticmethod
    def _manifest() -> dict:
        return _load_manifest(MANIFEST_PATH)

    def test_real_route_index_is_consistent(self) -> None:
        sys.path.insert(0, str(ROOT / "scripts"))
        import validate_route_manifest as v
        manifest = self._manifest()
        manifest_ids = {r["id"] for r in manifest["routes"]}
        route_audits = {r["id"]: set(r["required_audits"]) for r in manifest["routes"]}
        text = (ROOT / "references" / "route-index.md").read_text(encoding="utf-8")
        errors = v._check_route_index(text, manifest_ids, route_audits)
        assert errors == [], f"route-index.md drift: {errors}"

    def test_missing_route_in_index_is_detected(self) -> None:
        sys.path.insert(0, str(ROOT / "scripts"))
        import validate_route_manifest as v
        manifest_ids = {r["id"] for r in self._manifest()["routes"]}
        route_audits = {r["id"]: set(r["required_audits"]) for r in self._manifest()["routes"]}
        rows = [
            "| `listed-company` | lc trigger | `references/a.md` | `final-audit` | [`listed-company`](routes/listed-company.md) |",
        ]
        errors = v._check_route_index(
            self._index_with_rows(rows), manifest_ids, route_audits
        )
        assert errors, "Missing routes in route-index must be detected"
        assert any("missing from route-index" in e for e in errors)

    def test_unknown_route_in_index_is_detected(self) -> None:
        sys.path.insert(0, str(ROOT / "scripts"))
        import validate_route_manifest as v
        manifest = self._manifest()
        manifest_ids = {r["id"] for r in manifest["routes"]}
        route_audits = {r["id"]: set(r["required_audits"]) for r in manifest["routes"]}
        rows = [
            "| `fake-route` | trigger | `references/a.md` | `final-audit` | [`fake-route`](routes/fake-route.md) |",
        ]
        errors = v._check_route_index(
            self._index_with_rows(rows), manifest_ids, route_audits
        )
        assert any("not in the manifest" in e for e in errors)

    def test_empty_trigger_is_detected(self) -> None:
        sys.path.insert(0, str(ROOT / "scripts"))
        import validate_route_manifest as v
        manifest = self._manifest()
        manifest_ids = {r["id"] for r in manifest["routes"]}
        route_audits = {r["id"]: set(r["required_audits"]) for r in manifest["routes"]}
        rows = [
            "| `listed-company` |  | `references/a.md` | `final-audit` | [`listed-company`](routes/listed-company.md) |",
        ]
        errors = v._check_route_index(
            self._index_with_rows(rows), manifest_ids, route_audits
        )
        assert any("trigger" in e.lower() for e in errors)

    def test_audit_not_in_route_required_audits_is_detected(self) -> None:
        sys.path.insert(0, str(ROOT / "scripts"))
        import validate_route_manifest as v
        manifest = self._manifest()
        manifest_ids = {r["id"] for r in manifest["routes"]}
        route_audits = {r["id"]: set(r["required_audits"]) for r in manifest["routes"]}
        rows = [
            "| `listed-company` | trigger | `references/a.md` | "
            "`academic-analysis-audit` | [`listed-company`](routes/listed-company.md) |",
        ]
        errors = v._check_route_index(
            self._index_with_rows(rows), manifest_ids, route_audits
        )
        assert any("academic-analysis-audit" in e for e in errors)


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
