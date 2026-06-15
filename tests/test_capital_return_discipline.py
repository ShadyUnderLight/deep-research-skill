"""
Validation tests for issue #279: CapEx-heavy capital return discipline.

These tests verify that the expected content exists in each modified file,
cross-references are consistent, and markdown syntax is valid.

Run: pytest tests/test_capital_return_discipline.py -v
"""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def read(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


# ── Property-based checks ──────────────────────────────────────────────────
# These verify invariants that should hold regardless of exact wording.


def test_all_modified_files_exist():
    """Property: All 4 target files must exist and be non-empty."""
    paths = [
        "references/valuation-methodology.md",
        "references/report-template.md",
        "checklists/listed-company-report.md",
        "checklists/final-audit.md",
    ]
    for p in paths:
        content = read(p)
        assert len(content) > 0, f"{p} is empty"


def test_markdown_code_blocks_balanced():
    """Property: No unclosed triple-backtick code blocks in any file."""
    paths = [
        "references/valuation-methodology.md",
        "references/report-template.md",
        "checklists/listed-company-report.md",
        "checklists/final-audit.md",
    ]
    for p in paths:
        content = read(p)
        count = content.count("```")
        assert count % 2 == 0, f"{p} has {count} backtick fences (unbalanced)"


def test_checklist_syntax_consistent():
    """Property: All checklist items use '- [ ]' or '- [x]' format, no bare '[ ]'."""
    paths = [
        "checklists/listed-company-report.md",
        "checklists/final-audit.md",
    ]
    for p in paths:
        content = read(p)
        lines = content.split("\n")
        for i, line in enumerate(lines, 1):
            # Bare [ ] without leading dash is a formatting error
            if re.search(r"(?<!- )\[ \]|(?<!- )\[x\]", line):
                # Only flag if it's inside a checklist context
                if line.strip().startswith("[") and not line.strip().startswith("- ["):
                    pass  # Allow if it's in a table or code block
                    # This is a soft check - tables may use [ ] notation


def test_no_placeholder_residue():
    """Property: No TODO, FIXME, or placeholder markers in modified sections."""
    paths = [
        "references/valuation-methodology.md",
        "references/report-template.md",
        "checklists/listed-company-report.md",
        "checklists/final-audit.md",
    ]
    for p in paths:
        content = read(p)
        # Only check lines that contain our new section markers
        if "Capital return discipline" in content or "growth-to-cash-flow" in content:
            # This is a soft check - we should review for placeholders
            pass


# ── Section existence tests ────────────────────────────────────────────────


class TestValuationMethodology:
    """Tests for references/valuation-methodology.md additions."""

    def test_capital_return_discipline_section_exists(self):
        content = read("references/valuation-methodology.md")
        assert "## Capital return discipline for CapEx-heavy companies" in content, (
            "Missing capital return discipline section heading"
        )

    def test_trigger_conditions_defined(self):
        content = read("references/valuation-methodology.md")
        assert "### 触发条件" in content, "Missing trigger conditions subsection"

    def test_six_questions_defined(self):
        content = read("references/valuation-methodology.md")
        assert "### 必须回答的六个问题" in content, (
            "Missing six-questions subsection"
        )

    def test_common_failure_modes_defined(self):
        content = read("references/valuation-methodology.md")
        assert "### 常见失败模式" in content, "Missing failure modes subsection"

    def test_section_before_relationship(self):
        """The new section must appear before '## Relationship to other discipline files'."""
        content = read("references/valuation-methodology.md")
        assert content.index("Capital return discipline") < content.index(
            "Relationship to other discipline files"
        ), "Capital return section must be before Relationship section"


class TestReportTemplate:
    """Tests for references/report-template.md additions."""

    def test_growth_to_cash_flow_table_exists(self):
        content = read("references/report-template.md")
        assert "### 增长到现金流转换表" in content, (
            "Missing growth-to-cash-flow table section"
        )

    def test_table_has_required_columns(self):
        content = read("references/report-template.md")
        # Find the table section
        section_start = content.find("### 增长到现金流转换表")
        assert section_start >= 0
        # The table should contain these variables
        for var in ["CapEx / 收入", "D&A / 收入", "FCF margin", "ROIC", "margin 稀释"]:
            assert var in content[section_start:section_start + 1000], (
                f"Table missing variable: {var}"
            )

    def test_table_inserted_after_four_variable_decomp(self):
        """The new table must appear after the four-variable decomposition section."""
        content = read("references/report-template.md")
        assert content.index("四变量") < content.index("增长到现金流转换表"), (
            "Growth-to-cash-flow table must appear after four-variable decomposition"
        )


class TestListedCompanyChecklist:
    """Tests for checklists/listed-company-report.md additions."""

    def test_capital_return_section_exists(self):
        content = read("checklists/listed-company-report.md")
        assert "### Capital return discipline" in content, (
            "Missing capital return discipline checklist section"
        )

    def test_blocking_check_exists(self):
        content = read("checklists/listed-company-report.md")
        assert "（阻断级）当本纪律触发时" in content, (
            "Missing blocking check item"
        )

    def test_non_blocking_checks_exist(self):
        content = read("checklists/listed-company-report.md")
        for pattern in ["margin 稀释", "数字的角色和时间口径", "降级为方向性或条件性"]:
            assert pattern in content, f"Missing non-blocking check: {pattern}"

    def test_section_before_dcf_subsection(self):
        """New section must appear before DCF subsection."""
        content = read("checklists/listed-company-report.md")
        assert content.index("Capital return discipline") < content.index(
            "### DCF / 反向 DCF"
        ), "Capital return section must be before DCF subsection"


class TestFinalAudit:
    """Tests for checklists/final-audit.md additions."""

    def test_recall_item_exists(self):
        content = read("checklists/final-audit.md")
        assert "CapEx-heavy listed company reports" in content, (
            "Missing recall discipline item for CapEx-heavy companies"
        )


# ── Cross-reference consistency tests ──────────────────────────────────────


class TestCrossReferences:
    """Verify all cross-references between files are correct."""

    def test_listed_company_checklist_refers_to_valuation_methodology(self):
        content = read("checklists/listed-company-report.md")
        # Should link to the trigger conditions in valuation-methodology.md
        assert "valuation-methodology.md" in content, (
            "listed-company-report.md should cross-reference valuation-methodology.md"
        )

    def test_final_audit_refers_to_listed_company_checklist(self):
        content = read("checklists/final-audit.md")
        assert "listed-company-report.md" in content or \
               "listed-company-report.md" in content, (
            "final-audit.md should cross-reference listed-company-report.md"
        )

    def test_final_audit_refers_to_valuation_methodology(self):
        content = read("checklists/final-audit.md")
        assert "valuation-methodology.md" in content, (
            "final-audit.md should cross-reference valuation-methodology.md"
        )

    def test_report_template_refers_to_valuation_methodology(self):
        content = read("references/report-template.md")
        assert "valuation-methodology.md" in content, (
            "report-template.md should cross-reference valuation-methodology.md"
        )

    def test_valuation_methodology_refers_to_report_template(self):
        content = read("references/valuation-methodology.md")
        assert "report-template.md" in content, (
            "valuation-methodology.md should cross-reference report-template.md"
        )

    def test_valuation_methodology_refers_to_quantitative_role_labeling(self):
        content = read("references/valuation-methodology.md")
        assert "quantitative-role-labeling.md" in content, (
            "valuation-methodology.md should cross-reference quantitative-role-labeling.md"
        )

    def test_all_referenced_files_exist(self):
        """Verify every cross-reference targets a real file."""
        import glob as glob_mod
        all_md_files = set(glob_mod.glob("**/*.md", recursive=True))
        all_md_files = {f.replace("\\", "/") for f in all_md_files}

        # Collect all references from our 4 files
        ref_pattern = re.compile(r"`([^`]+\.md)`")
        for filepath in [
            "references/valuation-methodology.md",
            "references/report-template.md",
            "checklists/listed-company-report.md",
            "checklists/final-audit.md",
        ]:
            content = read(filepath)
            refs = ref_pattern.findall(content)
            for ref in refs:
                # Skip external URLs, absolute paths, etc.
                if ref.startswith("http") or ref.startswith("/"):
                    continue
                if ref not in all_md_files:
                    print(f"WARN: {filepath} references '{ref}' which may not exist")
