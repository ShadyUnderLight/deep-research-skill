"""Contract tests for issue #380: generated route cards (references/routes/).

Validates:
  - Contract A: generator produces deterministic output (idempotent --check)
  - Contract B: every manifest route has a card; every card has a manifest route
  - Contract C: card sections mirror manifest fields (trigger, do-not-use,
    often-confused, primary reads, required disciplines, required audits,
    artifact contract, failure signs)
  - Contract D: validate_route_manifest.py detects stale / missing / orphan cards
  - Contract E: route-index.md links to the route cards
"""

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "schemas" / "route-manifest.json"
CARDS_DIR = ROOT / "references" / "routes"
INDEX_PATH = ROOT / "references" / "route-index.md"
GENERATOR = ROOT / "scripts" / "generate_route_cards.py"
VALIDATOR = ROOT / "scripts" / "validate_route_manifest.py"


def _load_manifest() -> dict:
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        return json.load(f)


def _card_text(route_id: str) -> str:
    path = CARDS_DIR / f"{route_id}.md"
    assert path.is_file(), f"Missing route card: {path}"
    return path.read_text(encoding="utf-8")


def _github_anchor(heading: str) -> str:
    """Approximate GitHub's anchor slug for the headings used by cards."""
    lowered = heading.lower().strip()
    kept = "".join(c for c in lowered if c.isalnum() or c in " -")
    return kept.replace(" ", "-")


# ── Contract A: deterministic generation ────────────────────────────────────


class TestGeneratorDeterminism:
    def test_check_passes_on_committed_cards(self):
        result = subprocess.run(
            [sys.executable, str(GENERATOR), "--check"],
            capture_output=True, text=True, cwd=str(ROOT),
        )
        assert result.returncode == 0, (
            f"generate_route_cards.py --check failed:\n{result.stdout}\n{result.stderr}"
        )

    def test_regenerate_is_idempotent(self):
        """Re-running the generator must not change committed cards."""
        before = {p.name: p.read_text(encoding="utf-8") for p in CARDS_DIR.glob("*.md")}
        result = subprocess.run(
            [sys.executable, str(GENERATOR)],
            capture_output=True, text=True, cwd=str(ROOT),
        )
        assert result.returncode == 0, result.stdout + result.stderr
        after = {p.name: p.read_text(encoding="utf-8") for p in CARDS_DIR.glob("*.md")}
        assert before == after, "Generator is not idempotent — card content changed"
        # Restore determinism even if the generator wrote files
        for name, content in before.items():
            (CARDS_DIR / name).write_text(content, encoding="utf-8")


# ── Contract B: one card per manifest route, no orphans ─────────────────────


class TestCardCoverage:
    def test_every_manifest_route_has_card(self):
        manifest = _load_manifest()
        missing = [
            r["id"] for r in manifest["routes"]
            if not (CARDS_DIR / f"{r['id']}.md").is_file()
        ]
        assert not missing, f"Routes missing cards: {missing}"

    def test_no_orphan_cards(self):
        manifest = _load_manifest()
        manifest_ids = {r["id"] for r in manifest["routes"]}
        orphans = [p.stem for p in CARDS_DIR.glob("*.md") if p.stem not in manifest_ids]
        assert not orphans, f"Orphan route cards: {orphans}"

    def test_card_declares_generated_status(self):
        for route in _load_manifest()["routes"]:
            text = _card_text(route["id"])
            assert "Generated view" in text, (
                f"Card '{route['id']}' missing generated-view declaration"
            )
            assert "route-manifest.json" in text, (
                f"Card '{route['id']}' missing canonical-source declaration"
            )


# ── Contract C: card sections mirror manifest fields ────────────────────────


class TestCardContentSync:
    def test_trigger_do_not_use_artifact_contract(self):
        manifest = _load_manifest()
        for route in manifest["routes"]:
            text = _card_text(route["id"])
            assert route["trigger"] in text, (
                f"Card '{route['id']}' missing trigger"
            )
            assert route["do_not_use"] in text, (
                f"Card '{route['id']}' missing do-not-use"
            )
            assert route["artifact_contract"] in text, (
                f"Card '{route['id']}' missing artifact contract"
            )

    def test_audits_and_disciplines_present(self):
        manifest = _load_manifest()
        for route in manifest["routes"]:
            text = _card_text(route["id"])
            for audit in route["required_audits"]:
                assert audit in text, (
                    f"Card '{route['id']}' missing audit '{audit}'"
                )
            for discipline in route["required_disciplines"]:
                assert discipline in text, (
                    f"Card '{route['id']}' missing discipline '{discipline}'"
                )

    def test_failure_signs_and_hard_fail_source_present(self):
        manifest = _load_manifest()
        for route in manifest["routes"]:
            text = _card_text(route["id"])
            for keyword in route["hard_fail_keywords"]:
                assert keyword in text, (
                    f"Card '{route['id']}' missing failure sign '{keyword}'"
                )
            assert route["hard_fail_source"] in text, (
                f"Card '{route['id']}' missing hard-fail source"
            )

    def test_often_confused_links_to_sibling_cards(self):
        manifest = _load_manifest()
        manifest_ids = {r["id"] for r in manifest["routes"]}
        for route in manifest["routes"]:
            text = _card_text(route["id"])
            for other_id in route["often_confused_with"]:
                if other_id not in manifest_ids:
                    continue
                assert f"({other_id}.md)" in text, (
                    f"Card '{route['id']}' missing link to sibling card "
                    f"'{other_id}'"
                )

    def test_primary_reads_present(self):
        manifest = _load_manifest()
        for route in manifest["routes"]:
            text = _card_text(route["id"])
            for ref in route["primary_reads"]:
                assert ref in text, (
                    f"Card '{route['id']}' missing primary read '{ref}'"
                )

    def test_route_specific_templates_are_primary_reads(self):
        expected = {
            "listed-company": "references/templates/listed-company-report.md",
            "technical-deep-dive": "references/templates/technical-deep-dive-report.md",
            "academic-review": "references/templates/academic-review-report.md",
            "market-outlook": "references/templates/market-outlook-report.md",
            "market-entry": "references/templates/market-entry-report.md",
        }
        manifest = {route["id"]: route for route in _load_manifest()["routes"]}
        for route_id, template in expected.items():
            assert template in manifest[route_id]["primary_reads"], (
                f"Manifest route '{route_id}' does not expose its route-specific "
                f"template as a primary read"
            )
            assert template in _card_text(route_id), (
                f"Card '{route_id}' does not expose its route-specific template"
            )

    def test_card_links_are_valid(self):
        """All local markdown links inside cards must resolve to files."""
        manifest = _load_manifest()
        for route in manifest["routes"]:
            text = _card_text(route["id"])
            for target in re.findall(r"\]\(([^)]+)\)", text):
                if target.startswith(("http://", "https://", "#")):
                    continue
                path = target.split("#", 1)[0]
                if not path.endswith(".md"):
                    continue
                resolved = (CARDS_DIR / path).resolve()
                assert resolved.is_file(), (
                    f"Card '{route['id']}' has broken file link: {target} "
                    f"(resolved to {resolved})"
                )

    def test_card_link_fragments_are_valid(self):
        """Markdown links with fragments must target real headings."""
        for route in _load_manifest()["routes"]:
            text = _card_text(route["id"])
            for target in re.findall(r"\]\(([^)]+)\)", text):
                if target.startswith(("http://", "https://")) or "#" not in target:
                    continue
                path, fragment = target.split("#", 1)
                resolved = (CARDS_DIR / path).resolve()
                assert resolved.is_file(), (
                    f"Card '{route['id']}' has broken fragment file: {target}"
                )
                headings = re.findall(
                    r"^#{1,6}\s+(.+?)\s*$",
                    resolved.read_text(encoding="utf-8"),
                    re.MULTILINE,
                )
                assert fragment in {_github_anchor(h) for h in headings}, (
                    f"Card '{route['id']}' has broken fragment: {target}"
                )


# ── Contract D: drift detection blocks stale / missing / orphan cards ───────


class TestDriftDetection:
    def test_validator_passes_on_committed_state(self):
        result = subprocess.run(
            [sys.executable, str(VALIDATOR)],
            capture_output=True, text=True, cwd=str(ROOT),
        )
        assert result.returncode == 0, (
            f"validate_route_manifest.py failed:\n{result.stdout}\n{result.stderr}"
        )

    def test_missing_card_is_blocked(self):
        """Deleting a card must be detected as blocking drift."""
        target = CARDS_DIR / "market-outlook.md"
        assert target.is_file()
        backup = target.read_text(encoding="utf-8")
        target.unlink()
        try:
            result = subprocess.run(
                [sys.executable, str(VALIDATOR)],
                capture_output=True, text=True, cwd=str(ROOT),
            )
            assert result.returncode == 2, (
                f"Expected blocking drift (exit 2), got {result.returncode}\n"
                f"{result.stdout}"
            )
            assert "Missing route card" in result.stdout
        finally:
            target.write_text(backup, encoding="utf-8")

    def test_stale_card_is_blocked(self):
        """Editing a card away from its manifest fields must be blocked."""
        target = CARDS_DIR / "market-outlook.md"
        backup = target.read_text(encoding="utf-8")
        target.write_text(backup.replace(
            "Explain how a market will evolve",
            "STALE content injected by test",
        ), encoding="utf-8")
        try:
            result = subprocess.run(
                [sys.executable, str(VALIDATOR)],
                capture_output=True, text=True, cwd=str(ROOT),
            )
            assert result.returncode == 2, (
                f"Expected blocking drift (exit 2), got {result.returncode}\n"
                f"{result.stdout}"
            )
        finally:
            target.write_text(backup, encoding="utf-8")


# ── Contract E: route-index.md links to the cards ───────────────────────────


class TestRouteIndexLinksToCards:
    def test_trigger_table_has_card_column(self):
        text = INDEX_PATH.read_text(encoding="utf-8")
        assert "| Route ID | Trigger keywords | Reads | Audits | Card |" in text, (
            "route-index.md trigger table must have a Card column"
        )

    def test_every_route_links_to_its_card(self):
        rows = {}
        in_trigger_table = False
        for line in INDEX_PATH.read_text(encoding="utf-8").splitlines():
            if line.startswith("| Route ID | Trigger keywords"):
                in_trigger_table = True
                continue
            if in_trigger_table and line.startswith("## "):
                break
            if in_trigger_table and line.startswith("| `"):
                rid = line.split("|", 2)[1].strip().strip("`")
                rows[rid] = line
        manifest = _load_manifest()
        for route in manifest["routes"]:
            rid = route["id"]
            assert rid in rows, f"route-index.md missing row for '{rid}'"
            assert f"](routes/{rid}.md)" in rows[rid], (
                f"route-index.md Card column does not point to '{rid}'"
            )

    def test_card_column_drift_is_blocked(self):
        target = INDEX_PATH
        backup = target.read_text(encoding="utf-8")
        target.write_text(
            backup.replace(
                "| [`listed-company`](routes/listed-company.md)",
                "| [`listed-company`](routes/market-outlook.md)",
                1,
            ),
            encoding="utf-8",
        )
        try:
            result = subprocess.run(
                [sys.executable, str(VALIDATOR)],
                capture_output=True,
                text=True,
                cwd=str(ROOT),
            )
            assert result.returncode == 2, (
                f"Expected Card-column drift to be blocking, got {result.returncode}\n"
                f"{result.stdout}"
            )
            assert "Card link points to" in result.stdout
        finally:
            target.write_text(backup, encoding="utf-8")
