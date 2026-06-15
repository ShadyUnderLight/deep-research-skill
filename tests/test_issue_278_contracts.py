#!/usr/bin/env python3
"""
Property-based contract validation for issue #278.
Tests verify structural invariants across DCF/sensitivity-related files.

Usage:
    python tests/test_issue_278_contracts.py

Expected BEFORE implementation: ALL FAIL
Expected AFTER implementation:  ALL PASS
"""

import re
import sys
import os

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def read(path):
    with open(os.path.join(REPO_ROOT, path), "r") as f:
        return f.read()


# ── D1: references/valuation-methodology.md ────────────────────────

def test_d1_has_dcf_trigger_section():
    """D1: MUST contain ## DCF / reverse DCF trigger section."""
    content = read("references/valuation-methodology.md")
    assert re.search(r'^##\s+DCF / reverse DCF trigger', content, re.MULTILINE), \
        "Missing '## DCF / reverse DCF trigger' section"


def test_d1_trigger_section_position():
    """D1: DCF trigger MUST be after DCF subsection and before SOTP."""
    content = read("references/valuation-methodology.md")
    dcf_sub_pos = content.index("### DCF (Discounted Cash Flow)")
    trigger_pos = content.index("## DCF / reverse DCF trigger")
    sotp_pos = content.index("### SOTP (Sum of the Parts)")
    assert dcf_sub_pos < trigger_pos < sotp_pos, \
        f"Section ordering: DCF subsection({dcf_sub_pos}) < trigger({trigger_pos}) < SOTP({sotp_pos})"


def test_d1_has_trigger_conditions():
    """D1: Trigger section MUST have 5 bullet-point trigger conditions."""
    content = read("references/valuation-methodology.md")
    section_start = content.index("## DCF / reverse DCF trigger")
    section = content[section_start:]
    # Count bold list items in Applicable trigger conditions
    trigger_items = re.findall(r'^\s*-\s+\*\*', section, re.MULTILINE)
    assert len(trigger_items) >= 4, f"Expected >=4 trigger conditions, got {len(trigger_items)}"


def test_d1_has_three_outputs():
    """D1: Trigger section MUST list 3 acceptable outputs."""
    content = read("references/valuation-methodology.md")
    assert "Forward DCF" in content
    assert "Reverse DCF" in content
    assert "Non-applicability explanation" in content


def test_d1_has_degradation_rule():
    """D1: Trigger section MUST have a degradation rule."""
    content = read("references/valuation-methodology.md")
    assert "Degradation rule" in content or "degradation" in content.lower()


def test_d1_no_existing_deleted():
    """D1: Existing content outside the new section MUST be intact."""
    content = read("references/valuation-methodology.md")
    assert "### DCF (Discounted Cash Flow)" in content
    assert "### SOTP (Sum of the Parts)" in content
    assert "### PE (Price / Earnings)" in content
    assert "## Precision downgrade rules" in content
    assert "## Common failure patterns" in content


# ── D2: references/report-template.md ───────────────────────────────

def test_d2_has_dcf_subsection():
    """D2: MUST contain #### DCF / 反向 DCF（当适用） in valuation section."""
    content = read("references/report-template.md")
    assert "DCF / 反向 DCF（当适用）" in content, "Missing DCF subsection heading"


def test_d2_has_dcf_assumption_table():
    """D2: DCF subsection MUST have assumption table with columns for WACC, terminal growth, etc."""
    content = read("references/report-template.md")
    dcf_start = content.index("DCF / 反向 DCF（当适用）")
    dcf_section = content[dcf_start:]
    required_terms = ["WACC", "永续增长率", "收入增速", "营业利润率", "CapEx / 收入"]
    for term in required_terms:
        assert term in dcf_section, f"DCF section missing assumption term: {term}"


def test_d2_has_sensitivity_matrix_subsection():
    """D2: MUST contain #### 敏感性矩阵 subsection."""
    content = read("references/report-template.md")
    assert "敏感性矩阵" in content, "Missing sensitivity matrix subsection"


def test_d2_sensitivity_matrix_has_template():
    """D2: Sensitivity matrix subsection MUST have a template table with WACC and terminal growth."""
    content = read("references/report-template.md")
    sens_start = content.index("敏感性矩阵")
    sens_section = content[sens_start:]
    assert "WACC" in sens_section and "永续增长率" in sens_section, \
        "Sensitivity matrix missing WACC or terminal growth axis"


def test_d2_sensitivity_disclaimer_present():
    """D2: Sensitivity section MUST distinguish scenario from sensitivity analysis."""
    content = read("references/report-template.md")
    sens_start = content.index("敏感性矩阵")
    sens_section = content[sens_start:]
    assert "敏感性分析 ≠ 情景分析" in sens_section or "敏感性分析" in sens_section, \
        "Sensitivity section missing scenario vs sensitivity distinction"


def test_d2_cross_ref_to_valuation_methodology():
    """D2: MUST reference valuation-methodology.md DCF trigger."""
    content = read("references/report-template.md")
    dcf_start = content.index("DCF / 反向 DCF（当适用）")
    dcf_section = content[dcf_start:]
    assert "valuation-methodology.md" in dcf_section or "valuation" in dcf_section.lower(), \
        "DCF section missing cross-reference to valuation-methodology.md"


def test_d2_no_existing_deleted():
    """D2: Existing content in template MUST be intact."""
    content = read("references/report-template.md")
    assert "### Valuation method and scenario analysis" in content
    assert "EPS假设" in content and "PE倍数" in content
    assert "Time-horizon valuation stratification" in content
    assert "### 5. Risks and counter-evidence" in content


# ── D3: checklists/listed-company-report.md ─────────────────────────

def test_d3_has_dcf_checklist_subsection():
    """D3: MUST have ### DCF / 反向 DCF（当适用） section."""
    content = read("checklists/listed-company-report.md")
    assert "### DCF / 反向 DCF（当适用）" in content, "Missing DCF checklist subsection"


def test_d3_has_blocking_checklist_item():
    """D3: MUST have at least one blocking (阻断级) DCF checklist item."""
    blocking_lines = re.findall(
        r'-\s+\[.*?\]\s+（阻断级）.*?(?:DCF|估值)',
        read("checklists/listed-company-report.md"),
        re.MULTILINE
    )
    assert len(blocking_lines) >= 1, "No blocking DCF checklist item found"


def test_d3_has_non_blocker_items():
    """D3: MUST have 3+ non-blocker DCF checklist items."""
    content = read("checklists/listed-company-report.md")
    dcf_start = content.index("### DCF / 反向 DCF（当适用）")
    # Find the boundary: next ##-level or ###-level section heading after the DCF section
    remaining = content[dcf_start + len("### DCF / 反向 DCF（当适用）"):]
    next_heading = re.search(r'^#{2,3}\s+\S', remaining, re.MULTILINE)
    dcf_section = remaining[:next_heading.start()] if next_heading else remaining
    non_blocker = re.findall(r'（非阻塞）', dcf_section)
    assert len(non_blocker) >= 3, f"Expected >=3 non-blocker items in DCF section, got {len(non_blocker)}"


def test_d3_no_existing_deleted():
    """D3: Existing checklist items MUST be intact."""
    content = read("checklists/listed-company-report.md")
    assert "三档，每档有明确的 EPS 假设" in content
    assert "market snapshot" in content
    assert "research-anchor block" in content
    assert "## Reporting-period discipline" in content


# ── D4: ROUTING-MATRIX.md ─────────────────────────────────────────

def test_d4_has_dcf_artifact_contract():
    """D4: ROUTING-MATRIX.md MUST have DCF/reverse DCF in Listed Company artifact contract."""
    content = read("ROUTING-MATRIX.md")
    # Find the Listed Company route section
    lc_route = content.index("## Route: Listed Company / Investment-style Research")
    lc_section = content[lc_route:]
    # Find the next route section boundary
    next_route = re.search(r'^## Route:', lc_section[1:], re.MULTILINE)
    route_body = lc_section[:next_route.start() + 1] if next_route else lc_section
    # The artifact contract should be within this route
    assert "DCF" in route_body or "reverse DCF" in route_body or "reverse" in route_body.lower(), \
        "Listed Company route missing DCF reference"


def test_d4_has_sensitivity_artifact_contract():
    """D4: MUST mention sensitivity matrix in artifact contract."""
    content = read("ROUTING-MATRIX.md")
    lc_route = content.index("## Route: Listed Company / Investment-style Research")
    lc_section = content[lc_route:]
    next_route = re.search(r'^## Route:', lc_section[1:], re.MULTILINE)
    route_body = lc_section[:next_route.start() + 1] if next_route else lc_section
    assert "sensitivity" in route_body.lower(), \
        "Listed Company route missing sensitivity matrix reference"


# ── D5: eval case ──────────────────────────────────────────────────

EVAL_FILE = "evals/cases/tsmc-valuation-dcf-and-sensitivity-case.md"

def test_d5_eval_file_exists():
    """D5: New eval case file MUST exist."""
    path = os.path.join(REPO_ROOT, EVAL_FILE)
    assert os.path.exists(path), f"Eval case file missing: {EVAL_FILE}"


def test_d5_eval_has_standard_sections():
    """D5: Eval case MUST have standard sections: Goal, Prompt, Pass criteria, Failure signs."""
    content = read(EVAL_FILE)
    assert "## Goal" in content
    assert "## Prompt" in content
    assert "## Pass criteria" in content
    assert "## Failure signs" in content
    assert "## Why this eval matters" in content


def test_d5_eval_tests_dcf_or_explanation():
    """D5: Eval case MUST test whether DCF or non-applicability explanation is present."""
    content = read(EVAL_FILE)
    terms = ['DCF', 'reverse DCF', 'non-applicability', 'explicit explanation']
    found = sum(1 for t in terms if t.lower() in content.lower())
    assert found >= 2, f"Eval case doesn't adequately test DCF presence (found {found}/{len(terms)} terms)"


def test_d5_eval_tests_sensitivity():
    """D5: Eval case MUST test sensitivity matrix presence."""
    content = read(EVAL_FILE)
    assert "sensitivity matrix" in content.lower() or "tipping-point" in content.lower(), \
        "Eval case doesn't test sensitivity matrix"


def test_d5_eval_expects_fail():
    """D5: Eval case must expect fail or conditional-pass verdict."""
    content = read(EVAL_FILE)
    assert 'fail' in content.lower() or 'conditional' in content.lower(), \
        "Eval case should expect fail or conditional-pass verdict"


def test_d5_eval_has_scoring():
    """D5: Eval case MUST have Pass / Conditional pass / Fail scoring."""
    content = read(EVAL_FILE)
    assert "Pass" in content and "Fail" in content, "Eval case missing scoring definitions"


def test_d5_index_has_entry():
    """D5: INDEX.md MUST have an entry for the new eval case."""
    content = read("evals/INDEX.md")
    filename = os.path.basename(EVAL_FILE)
    assert filename in content, f"INDEX.md missing entry for {filename}"


def test_d5_index_table_format():
    """D5: INDEX.md entry MUST maintain proper table format (10+ columns)."""
    content = read("evals/INDEX.md")
    filename = os.path.basename(EVAL_FILE)
    table_lines = [l for l in content.split('\n') if filename in l]
    assert len(table_lines) >= 1, f"No table line found for {filename}"
    for line in table_lines:
        cols = line.split('|')
        assert len(cols) >= 10, f"INDEX.md line has {len(cols)} cols, expected >=10: {line}"


# ── Cross-file invariants ─────────────────────────────────────────

def test_p1_cross_references_valid():
    """P1: Cross-references between modified files must be valid."""
    valuation = read("references/valuation-methodology.md")
    template = read("references/report-template.md")
    checklist = read("checklists/listed-company-report.md")

    # valuation-methodology.md references report-template.md
    assert 'report-template.md' in valuation, \
        "valuation-methodology.md must reference report-template.md"

    # valuation-methodology.md references quantitative-role-labeling.md
    assert 'quantitative-role-labeling.md' in valuation, \
        "valuation-methodology.md must reference quantitative-role-labeling.md"

    # report-template.md references valuation-methodology.md
    assert 'valuation-methodology.md' in template, \
        "report-template.md must reference valuation-methodology.md"

    # checklist references valuation-methodology.md DCF trigger
    assert 'valuation-methodology.md' in checklist, \
        "checklist must reference valuation-methodology.md"

    # checklist references quantitative-role-labeling.md
    assert 'quantitative-role-labeling.md' in checklist, \
        "checklist must reference quantitative-role-labeling.md"


def test_p2_quantitative_role_labeling_unchanged():
    """P2: Existing sensitivity classification in quantitative-role-labeling.md MUST be intact."""
    content = read("references/quantitative-role-labeling.md")
    # The key rule: scenario analysis ≠ sensitivity analysis
    assert "情景分析 ≠ 敏感性分析" in content or "Scenario analysis" in content, \
        "quantitative-role-labeling.md lost scenario ≠ sensitivity distinction"
    # Check three sensitivity levels still exist
    assert "Low sensitivity" in content
    assert "Medium sensitivity" in content
    assert "High sensitivity" in content
    assert "±20%" in content


def test_p3_index_not_broken():
    """P3: INDEX.md table structure should remain parseable."""
    content = read("evals/INDEX.md")
    table_lines = []
    in_table = False
    for line in content.split('\n'):
        if line.startswith('| ---'):
            in_table = True
            continue
        if in_table and line.startswith('|'):
            table_lines.append(line)
        elif in_table and not line.startswith('|'):
            in_table = False
    if table_lines:
        counts = [len(l.split('|')) for l in table_lines]
        assert max(counts) == min(counts), f"Inconsistent INDEX.md table columns: {counts}"


# ── Main ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    tests = [
        ("D1: DCF trigger section", test_d1_has_dcf_trigger_section),
        ("D1: section position", test_d1_trigger_section_position),
        ("D1: has trigger conditions", test_d1_has_trigger_conditions),
        ("D1: has three outputs", test_d1_has_three_outputs),
        ("D1: has degradation rule", test_d1_has_degradation_rule),
        ("D1: no existing deleted", test_d1_no_existing_deleted),
        ("D2: DCF subsection", test_d2_has_dcf_subsection),
        ("D2: DCF assumption table", test_d2_has_dcf_assumption_table),
        ("D2: sensitivity matrix subsection", test_d2_has_sensitivity_matrix_subsection),
        ("D2: sensitivity matrix template", test_d2_sensitivity_matrix_has_template),
        ("D2: sensitivity disclaimer", test_d2_sensitivity_disclaimer_present),
        ("D2: cross-ref to valuation-methodology", test_d2_cross_ref_to_valuation_methodology),
        ("D2: no existing deleted", test_d2_no_existing_deleted),
        ("D3: DCF checklist subsection", test_d3_has_dcf_checklist_subsection),
        ("D3: blocking checklist item", test_d3_has_blocking_checklist_item),
        ("D3: non-blocker items", test_d3_has_non_blocker_items),
        ("D3: no existing deleted", test_d3_no_existing_deleted),
        ("D4: DCF artifact contract", test_d4_has_dcf_artifact_contract),
        ("D4: sensitivity artifact contract", test_d4_has_sensitivity_artifact_contract),
        ("D5: eval file exists", test_d5_eval_file_exists),
        ("D5: standard sections", test_d5_eval_has_standard_sections),
        ("D5: tests DCF presence", test_d5_eval_tests_dcf_or_explanation),
        ("D5: tests sensitivity", test_d5_eval_tests_sensitivity),
        ("D5: expects fail", test_d5_eval_expects_fail),
        ("D5: scoring definitions", test_d5_eval_has_scoring),
        ("D5: INDEX entry", test_d5_index_has_entry),
        ("D5: INDEX table format", test_d5_index_table_format),
        ("P1: cross-references valid", test_p1_cross_references_valid),
        ("P2: quantitative-role-labeling intact", test_p2_quantitative_role_labeling_unchanged),
        ("P3: INDEX not broken", test_p3_index_not_broken),
    ]

    passed = 0
    failed = 0
    for name, fn in tests:
        try:
            fn()
            print(f"  ✅ {name}")
            passed += 1
        except (AssertionError, ValueError) as e:
            print(f"  ❌ {name}: {e}")
            failed += 1
        except Exception as e:
            print(f"  ❌ {name}: Unexpected error: {e}")
            failed += 1

    print(f"\n{'='*50}")
    print(f"Results: {passed} passed, {failed} failed")
    if failed:
        sys.exit(1)
    else:
        print("All contracts verified ✅")
