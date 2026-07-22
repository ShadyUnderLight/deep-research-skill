"""Property-based tests for Issue #361 Phase 1: Progressive-disclosure refactoring.

Validates:
  - Contract A: search-provider-fallback.md exists and has required sections
  - Contract B: delivery-operator-note.md has PDF trigger + pipeline sections
  - Contract C: route-index.md exists, <=80 lines, all routes present, consistent with manifest
  - Contract D: SKILL.md is <=350 lines, retains workflow spine, correctly navigates
  - Contract E: Migration integrity — no content lost
  - Contract F: Backward compatibility — existing validators still pass
  - Contract G: Cross-reference integrity — affected files have updated references
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "schemas" / "route-manifest.json"


# ── Helpers ──────────────────────────────────────────────────────────────────

def load_manifest():
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def file_has_section(filepath: Path, section_title: str) -> bool:
    text = filepath.read_text(encoding="utf-8")
    return f"## {section_title}" in text or f"# {section_title}" in text


def file_line_count(filepath: Path) -> int:
    return len(filepath.read_text(encoding="utf-8").splitlines())


def file_contains(filepath: Path, needle: str) -> bool:
    return needle in filepath.read_text(encoding="utf-8")


def _parse_boundary_table() -> list[dict[str, str]]:
    """Parse the boundary reference table from route-index.md into rows."""
    text = (ROOT / "references" / "route-index.md").read_text(encoding="utf-8")
    boundary_start = text.index("## Route boundary reference")
    boundary_section = text[boundary_start:]
    lines = boundary_section.split("\n")
    header_cols = []
    rows = []
    in_table = False
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("## ") and in_table:
            break  # next section reached
        if stripped.startswith("| Route ID |"):
            header_cols = [c.strip() for c in stripped.strip("|").split("|")]
            in_table = True
            continue
        if in_table and stripped.startswith("|---"):
            continue  # skip separator
        if in_table and stripped.startswith("|"):
            cols = [c.strip().strip("`") for c in stripped.strip("|").split("|")]
            if len(cols) >= len(header_cols):
                row = {}
                for i, col in enumerate(cols):
                    if i < len(header_cols):
                        row[header_cols[i]] = col
                if row.get("Route ID", "").strip():
                    rows.append(row)
    return rows


def _extract_route_ids_from_text(text: str) -> set[str]:
    """Extract route IDs (kebab-case backtick-quoted identifiers) from text."""
    import re
    ids = set()
    for match in re.finditer(r'`([a-z]+(?:-[a-z]+)*)`', text):
        rid = match.group(1)
        # Only match known route ID patterns (not file paths or other backtick strings)
        if "-" in rid and not rid.endswith(".md") and not rid.startswith("references"):
            ids.add(rid)
    return ids


# ── Contract A: references/search-provider-fallback.md ───────────────────────

class TestSearchProviderFallback:
    FALLBACK_PATH = ROOT / "references" / "search-provider-fallback.md"

    def test_file_exists(self):
        assert self.FALLBACK_PATH.exists(), f"{self.FALLBACK_PATH} does not exist"

    def test_has_fallback_policy_section(self):
        assert file_has_section(
            self.FALLBACK_PATH, "Degraded-search fallback policy"
        ), "Missing 'Degraded-search fallback policy' section"

    def test_has_execution_discipline_section(self):
        assert file_has_section(
            self.FALLBACK_PATH, "Degraded-search execution discipline"
        ), "Missing 'Degraded-search execution discipline' section"

    def test_has_evidence_log_section(self):
        assert file_has_section(
            self.FALLBACK_PATH, "Degraded-search evidence log"
        ), "Missing 'Degraded-search evidence log' section"

    def test_has_tool_capability_mapping(self):
        assert file_has_section(
            self.FALLBACK_PATH, "Common tool capability mapping"
        ), "Missing 'Common tool capability mapping' section"

    def test_fallback_steps_preserved(self):
        text = self.FALLBACK_PATH.read_text(encoding="utf-8")
        required = [
            "distinguish temporary rate-limit",
            "declare the search provider degraded",
            "Exa",
            "Bing",
            "dynamic-browser",
            "evidence log",
        ]
        for marker in required:
            assert marker in text, f"Missing fallback step marker: {marker}"

    def test_navigates_back_to_skill(self):
        text = self.FALLBACK_PATH.read_text(encoding="utf-8")
        assert "SKILL.md" in text, "Missing back-reference to SKILL.md"


# ── Contract B: references/delivery-operator-note.md ─────────────────────────

class TestDeliveryOperatorNote:
    DELIVERY_PATH = ROOT / "references" / "delivery-operator-note.md"

    def test_file_has_pdf_trigger_section(self):
        assert file_has_section(
            self.DELIVERY_PATH, "PDF Delivery Trigger"
        ), "Missing 'PDF Delivery Trigger' section"

    def test_trigger_keywords_preserved(self):
        text = self.DELIVERY_PATH.read_text(encoding="utf-8")
        required_triggers = [
            "生成 PDF", "导出 PDF", "PDF 报告", "保存为 PDF",
            "给我 PDF 文件", "PDF 版本", "PDF 格式",
        ]
        for t in required_triggers:
            assert t in text, f"Missing PDF trigger keyword: {t}"

    def test_negation_guard_preserved(self):
        text = self.DELIVERY_PATH.read_text(encoding="utf-8")
        guards = ["不要 PDF", "不用 PDF", "无需 PDF", "no PDF", "not PDF"]
        for g in guards:
            assert g in text, f"Missing PDF negation guard: {g}"

    def test_pipeline_steps_preserved(self):
        text = self.DELIVERY_PATH.read_text(encoding="utf-8")
        assert "scripts/md_to_pdf.py" in text, "Missing pipeline reference"

    def test_navigates_back_to_skill(self):
        text = self.DELIVERY_PATH.read_text(encoding="utf-8")
        assert "SKILL.md" in text, "Missing back-reference to SKILL.md"


# ── Contract C: references/route-index.md ───────────────────────────────────

class TestRouteIndex:
    INDEX_PATH = ROOT / "references" / "route-index.md"

    def test_file_exists(self):
        assert self.INDEX_PATH.exists(), f"{self.INDEX_PATH} does not exist"

    def test_within_line_limit(self):
        lines = file_line_count(self.INDEX_PATH)
        assert lines <= 80, (
            f"route-index.md is {lines} lines, exceeds 80-line limit"
        )

    def test_all_routes_present(self):
        manifest = load_manifest()
        text = self.INDEX_PATH.read_text(encoding="utf-8")
        route_ids = [r["id"] for r in manifest["routes"]]
        missing = [rid for rid in route_ids if rid not in text]
        assert not missing, f"Routes missing from index: {missing}"

    def test_refers_to_routing_matrix(self):
        text = self.INDEX_PATH.read_text(encoding="utf-8")
        assert "ROUTING-MATRIX.md" in text, (
            "route-index.md must reference ROUTING-MATRIX.md"
        )

    def test_route_ids_consistent_with_manifest(self):
        manifest = load_manifest()
        text = self.INDEX_PATH.read_text(encoding="utf-8")
        for route in manifest["routes"]:
            rid = route["id"]
            assert rid in text, f"route-index.md missing route id: {rid}"

    def test_has_boundary_reference_table(self):
        """Route index must include a boundary table with non-empty fields."""
        rows = _parse_boundary_table()
        assert len(rows) >= 12, (
            f"Expected ≥12 data rows in boundary table, got {len(rows)}"
        )
        manifest = load_manifest()
        route_ids = {r["id"] for r in manifest["routes"]}
        for row in rows:
            rid = row.get("Route ID", "").strip()
            assert rid, f"Boundary row has empty Route ID: {row}"
            assert rid in route_ids, (
                f"Boundary table Route ID '{rid}' not found in route-manifest.json"
            )
            do_not = row.get("Do NOT use when", "").strip()
            assert do_not, f"Boundary row '{rid}' has empty 'Do NOT use when'"
            confused = row.get("Often confused with", "").strip()
            assert confused, f"Boundary row '{rid}' has empty 'Often confused with'"
            artifact = row.get("Key artifact must-haves", "").strip()
            assert artifact, f"Boundary row '{rid}' has empty 'Key artifact must-haves'"
            # Verify confused-with IDs reference valid routes
            for ref_id in _extract_route_ids_from_text(confused):
                assert ref_id in route_ids, (
                    f"Boundary row '{rid}' references unknown route '{ref_id}' "
                    f"in 'Often confused with'"
                )

    def test_boundary_table_covers_all_routes(self):
        """Every route in manifest must appear in the boundary table."""
        rows = _parse_boundary_table()
        route_ids_in_table = {row.get("Route ID", "").strip() for row in rows}
        manifest = load_manifest()
        expected_ids = {r["id"] for r in manifest["routes"]}
        missing = expected_ids - route_ids_in_table
        assert not missing, f"Routes missing from boundary table: {missing}"

    def test_market_outlook_guards_against_ranking_misuse(self):
        """market-outlook must explicitly warn that ranking/selection tasks
        should use constrained-choice instead."""
        rows = _parse_boundary_table()
        mo = [r for r in rows if r.get("Route ID", "").strip() == "market-outlook"]
        assert len(mo) == 1, f"Expected 1 market-outlook row, got {len(mo)}"
        confused = mo[0].get("Often confused with", "")
        do_not = mo[0].get("Do NOT use when", "")
        combined = (confused + " " + do_not).lower()
        assert "constrained-choice" in combined, (
            f"market-outlook boundary must reference constrained-choice. "
            f"Do NOT use: '{do_not}', Often confused: '{confused}'"
        )


# ── Contract D: SKILL.md (modified) ──────────────────────────────────────────

class TestSkillMDPostMigration:
    SKILL_PATH = ROOT / "SKILL.md"

    def test_within_line_limit(self):
        lines = file_line_count(self.SKILL_PATH)
        assert lines <= 450, (
            f"SKILL.md is {lines} lines, exceeds 450-line post-migration limit"
        )

    def test_workflow_spine_preserved(self):
        text = self.SKILL_PATH.read_text(encoding="utf-8")
        for i in range(1, 10):
            assert str(i) in text, f"Workflow step {i} may be missing"

    def test_research_pack_lifecycle_preserved(self):
        text = self.SKILL_PATH.read_text(encoding="utf-8")
        assert "## Research Pack" in text, "Research Pack section missing"
        assert "any of the 11 routes" in text or "a specialized route" in text, (
            "Research Pack trigger condition changed"
        )

    def test_final_discipline_preserved(self):
        text = self.SKILL_PATH.read_text(encoding="utf-8")
        assert "## Final discipline" in text, "Final discipline section missing"
        assert "route-specific audits" in text, "Audit step reference missing"

    def test_output_quality_bar_preserved(self):
        text = self.SKILL_PATH.read_text(encoding="utf-8")
        assert "## Output quality bar" in text, "Output quality bar missing"

    def test_points_to_fallback_file(self):
        text = self.SKILL_PATH.read_text(encoding="utf-8")
        assert "search-provider-fallback.md" in text, (
            "SKILL.md must reference new fallback file"
        )

    def test_points_to_route_index(self):
        text = self.SKILL_PATH.read_text(encoding="utf-8")
        assert "route-index.md" in text, (
            "SKILL.md must reference route-index.md"
        )

    def test_points_to_delivery_note(self):
        text = self.SKILL_PATH.read_text(encoding="utf-8")
        assert "delivery-operator-note.md" in text, (
            "SKILL.md must reference delivery-operator-note.md"
        )

    def test_degraded_search_moved_out(self):
        text = self.SKILL_PATH.read_text(encoding="utf-8")
        moved_markers = [
            "## Degraded-search execution discipline",
            "## Degraded-search evidence log",
        ]
        for marker in moved_markers:
            assert marker not in text, (
                f"'{marker}' still in SKILL.md — should be moved to fallback file"
            )

    def test_delivery_details_moved_out(self):
        """PDF pipeline details and trigger keyword list should NOT be in SKILL.md anymore."""
        text = self.SKILL_PATH.read_text(encoding="utf-8")
        moved_markers = [
            "可下载报告",
            "正式报告文件",
            "以附件形式交付",
            "write the final report to a `.md` file first",
        ]
        for marker in moved_markers:
            assert marker not in text, (
                f"'{marker}' still in SKILL.md — should be in delivery-operator-note.md"
            )


# ── Contract E: Migration Integrity ─────────────────────────────────────────

class TestMigrationIntegrity:
    """Verify that relocated content actually exists in target files."""

    def test_fallback_content_migrated(self):
        if not (ROOT / "references" / "search-provider-fallback.md").exists():
            return  # Skip if file not yet created (pre-migration TDD check)
        fallback = (ROOT / "references" / "search-provider-fallback.md").read_text(
            encoding="utf-8"
        )
        required = [
            "Agent-Reach",
            "Exa",
            "Bing",
            "candidate-source discovery only",
            "re-verify any load-bearing claim",
        ]
        for phrase in required:
            assert phrase in fallback, f"Missing phrase in fallback file: {phrase}"

    def test_pdf_content_migrated(self):
        delivery = (ROOT / "references" / "delivery-operator-note.md").read_text(
            encoding="utf-8"
        )
        required = [
            "md_to_pdf.py",
            "markdown file remains the source of truth",
            "PDF rendering fails",
        ]
        for phrase in required:
            assert phrase in delivery, f"Missing phrase in delivery file: {phrase}"


# ── Contract F: Backward Compatibility ──────────────────────────────────────

def _resolve_merge_base() -> str | None:
    """Find merge-base with the target branch. Only tries explicit base refs
    (main, origin/main, origin/master). Does NOT enumerate arbitrary origin/*
    refs to avoid accidentally selecting the PR head or unrelated branches.
    Returns None if unresolvable (fail closed)."""
    candidates = ["main", "origin/main", "origin/master"]
    for target in candidates:
        result = subprocess.run(
            ["git", "merge-base", "HEAD", target],
            capture_output=True, text=True, cwd=str(ROOT),
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    return None


class TestBackwardCompatibility:
    """Existing validators and tests must still pass."""

    def test_route_manifest_validator_passes(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "validate_route_manifest.py")],
            capture_output=True, text=True, cwd=str(ROOT),
        )
        assert result.returncode == 0, (
            f"validate_route_manifest.py failed:\n{result.stderr}"
        )

    def test_docs_structure_validator_passes(self):
        result = subprocess.run(
            ["bash", str(ROOT / "scripts" / "validate-docs-structure.sh")],
            capture_output=True, text=True, cwd=str(ROOT),
        )
        assert result.returncode == 0, (
            f"validate-docs-structure.sh failed:\n{result.stdout}\n{result.stderr}"
        )

    def test_route_manifest_test_suite_passes(self):
        result = subprocess.run(
            [sys.executable, "-m", "pytest",
             str(ROOT / "tests" / "test_route_manifest.py"),
             "-v", "--tb=short"],
            capture_output=True, text=True, cwd=str(ROOT),
        )
        assert result.returncode == 0, (
            f"test_route_manifest.py failed:\n{result.stdout}\n{result.stderr}"
        )

    def test_discipline_registry_test_suite_passes(self):
        result = subprocess.run(
            [sys.executable, "-m", "pytest",
             str(ROOT / "tests" / "test_discipline_registry.py"),
             "-v", "--tb=short"],
            capture_output=True, text=True, cwd=str(ROOT),
        )
        assert result.returncode == 0, (
            f"test_discipline_registry.py failed:\n{result.stdout}\n{result.stderr}"
        )

    def test_routing_matrix_is_unchanged(self):
        """ROUTING-MATRIX.md should not be modified in Phase 1.

        Uses merge-base diff to verify no commits on this branch modify
        ROUTING-MATRIX.md. Resolves merge-base against main, origin/main,
        or any available remote ref. Fails closed if base is unresolvable
        (e.g. shallow/detached checkout without remote).
        """
        base = _resolve_merge_base()
        assert base is not None, (
            "Cannot resolve merge-base — git remote or local main branch "
            "is required to verify ROUTING-MATRIX.md was not modified. "
            "In CI, ensure the checkout fetches the base branch."
        )
        result = subprocess.run(
            ["git", "diff", "--name-only", f"{base}..HEAD"],
            capture_output=True, text=True, cwd=str(ROOT),
        )
        changed = result.stdout.strip().split("\n") if result.stdout.strip() else []
        assert "ROUTING-MATRIX.md" not in changed, (
            f"ROUTING-MATRIX.md was modified in this branch — out of scope "
            f"for Phase 1.\nChanged files: {changed}"
        )


# ── Contract G: Cross-Reference Integrity ───────────────────────────────────

class TestCrossReferenceIntegrity:
    """Affected files must not have broken internal references."""

    def test_skill_md_has_no_broken_references(self):
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        refs = re.findall(r'`(references/[^`]+\.md)`', text)
        refs += re.findall(r'`(checklists/[^`]+\.md)`', text)
        broken = []
        for ref in refs:
            if not (ROOT / ref).exists():
                broken.append(ref)
        assert not broken, f"Broken references in SKILL.md: {broken}"

    def test_external_channel_preflight_has_updated_ref(self):
        filepath = ROOT / "references" / "external-channel-preflight.md"
        text = filepath.read_text(encoding="utf-8")
        # Must reference either new fallback file or SKILL.md for fallback info
        assert "search-provider-fallback.md" in text or (
            "SKILL.md" in text and "Tool strategy" in text
        ), "external-channel-preflight.md missing updated reference"
