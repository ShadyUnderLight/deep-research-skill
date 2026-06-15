#!/usr/bin/env python3
"""
Property-based contract validation for issue #280.
Tests verify structural invariants for customer concentration / second-source discipline.

Usage:
    python tests/test_issue_280_contracts.py

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


# ── D1: checklists/listed-company-report.md ─────────────────────────

CHECKLIST = "checklists/listed-company-report.md"

def test_d1_has_customer_concentration_section():
    """D1: MUST contain ## Customer concentration / second-source discipline section."""
    content = read(CHECKLIST)
    assert re.search(r'^##\s+Customer concentration', content, re.MULTILINE), \
        "Missing '## Customer concentration / second-source discipline' section"


def test_d1_section_position():
    """D1: Section MUST be between Judgment-shape and Monopoly sections."""
    content = read(CHECKLIST)
    judgment_pos = content.index("## Judgment-shape micro-audit")
    moat_pos = content.index("## Monopoly / moat / scarcity discipline")
    cc_pos = content.index("## Customer concentration")
    assert judgment_pos < cc_pos < moat_pos, \
        f"Section ordering: Judgment({judgment_pos}) < CustConc({cc_pos}) < Moat({moat_pos})"


def test_d1_has_minimum_checklist_items():
    """D1: MUST have >=3 checklist items in the customer concentration section."""
    content = read(CHECKLIST)
    cc_start = content.index("## Customer concentration")
    remaining = content[cc_start + 1:]
    next_heading = re.search(r'^##\s+\S', remaining, re.MULTILINE)
    cc_section = remaining[:next_heading.start()] if next_heading else remaining
    # Count [ ] checklist items
    items = re.findall(r'-\s+\[[ x]\]', cc_section)
    assert len(items) >= 3, f"Expected >=3 checklist items, got {len(items)}"


def test_d1_mentions_second_source():
    """D1: MUST mention second-source or dual-source in checklist items."""
    content = read(CHECKLIST)
    cc_start = content.index("## Customer concentration")
    cc_section = content[cc_start:]
    next_heading = re.search(r'^##\s+\S', cc_section[1:], re.MULTILINE)
    body = cc_section[:next_heading.start() + 1] if next_heading else cc_section
    assert any(term in body for term in ['second-source', 'second source', '第二来源', 'dual-source', '双供应', '供应源']), \
        "Customer concentration section missing second-source reference"


def test_d1_mentions_valuation_implication():
    """D1: MUST mention valuation impact or 估值 in checklist items."""
    content = read(CHECKLIST)
    cc_start = content.index("## Customer concentration")
    cc_section = content[cc_start:]
    next_heading = re.search(r'^##\s+\S', cc_section[1:], re.MULTILINE)
    body = cc_section[:next_heading.start() + 1] if next_heading else cc_section
    assert any(term in body for term in ['估值', 'valuation', '倍数', 'multiple', 'margin', '议价']), \
        "Customer concentration section missing valuation implication reference"


def test_d1_no_existing_deleted():
    """D1: Existing checklist items MUST be intact."""
    content = read(CHECKLIST)
    assert "competition is written as actual thesis pressure" in content
    assert "research-anchor block is present and complete" in content
    assert "monopoly, oligopoly, strong moat" in content
    assert "TTM / LTM figures" in content
    assert "## Reporting-period discipline" in content
    assert "## Market snapshot" in content


# ── D2: references/report-template.md ───────────────────────────────

TEMPLATE = "references/report-template.md"

def test_d2_has_customer_concentration_section():
    """D2: MUST contain customer concentration optional section/table."""
    content = read(TEMPLATE)
    assert "客户集中度" in content or "Customer concentration" in content, \
        "Missing customer concentration section"


def test_d2_table_has_required_columns():
    """D2: Customer concentration table MUST have required metric columns."""
    content = read(TEMPLATE)
    cc_start = content.index("客户集中度") if "客户集中度" in content else content.index("Customer concentration")
    cc_section = content[cc_start:]
    required = ["前十大客户收入占比", "第一大客户占比", "第二大客户占比", "second-source", "估值含义"]
    found = [term for term in required if term in cc_section]
    assert len(found) == len(required), f"Customer concentration table missing required columns. Found {len(found)}/{len(required)}: missing {set(required) - set(found)}"


def test_d2_table_has_conclusion_row():
    """D2: Customer concentration table MUST have a conclusion row with 净影响."""
    content = read(TEMPLATE)
    cc_start = content.index("客户集中度") if "客户集中度" in content else content.index("Customer concentration")
    cc_section = content[cc_start:]
    assert "净影响" in cc_section, \
        "Customer concentration table missing conclusion row with '净影响'"


def test_d2_section_is_optional():
    """D2: Customer concentration section MUST be marked as optional (如适用)."""
    content = read(TEMPLATE)
    cc_start = content.index("客户集中度") if "客户集中度" in content else content.index("Customer concentration")
    context_before = content[max(0, cc_start - 200):cc_start]
    context_start = content[cc_start:cc_start + 200]
    context = context_before + context_start
    assert "如适用" in context or "optional" in context.lower(), \
        "Customer concentration section not marked as optional"


def test_d2_no_existing_deleted():
    """D2: Existing template content MUST be intact."""
    content = read(TEMPLATE)
    assert "### Valuation method and scenario analysis" in content
    assert "EPS假设" in content and "PE倍数" in content
    assert "Time-horizon valuation stratification" in content
    assert "### 5. Risks and counter-evidence" in content
    assert "Research-anchor block" in content
    assert "Market snapshot table" in content
    assert "#### DCF / 反向 DCF（当适用）" in content, "Lost DCF subsection from #278"


# ── D3: references/moat-monopoly-screening.md ───────────────────────

MOAT = "references/moat-monopoly-screening.md"

def test_d3_has_second_source_check():
    """D3: MUST mention second-source/de-risking check with customer-lock-in wording."""
    content = read(MOAT)
    assert any(term in content for term in ['second-source', 'second source', '第二来源', 'supplier de-risking', 'de-risking', 'dual-source', '双供应', '供应源']), \
        "Moat reference missing second-source check"


def test_d3_links_to_checklist():
    """D3: MUST reference listed-company checklist for customer concentration."""
    content = read(MOAT)
    assert "customer concentration" in content.lower() or "客户集中度" in content or "listed-company" in content.lower(), \
        "Moat reference missing link to customer concentration discipline"


def test_d3_no_existing_deleted():
    """D3: Existing moat content MUST be intact."""
    content = read(MOAT)
    assert "## Core rule" in content
    assert "## Required distinctions" in content
    assert "## Strong-claim wording discipline" in content
    assert "unique / only / sole" in content
    assert "## Mandatory downgrade rules" in content
    assert "## Concept-boundary traps" in content
    assert "## Hard fail" in content


# ── D4: eval case ──────────────────────────────────────────────────

EVAL_FILE = "evals/cases/tsmc-customer-concentration-and-second-source-case.md"

def test_d4_eval_file_exists():
    """D4: New eval case file MUST exist."""
    path = os.path.join(REPO_ROOT, EVAL_FILE)
    assert os.path.exists(path), f"Eval case file missing: {EVAL_FILE}"


def test_d4_eval_has_standard_sections():
    """D4: Eval case MUST have standard sections: Goal, Prompt, Pass criteria, Failure signs."""
    content = read(EVAL_FILE)
    assert "## Goal" in content
    assert "## Prompt" in content
    assert "## Pass criteria" in content
    assert "## Failure signs" in content
    assert "## Why this eval matters" in content


def test_d4_eval_tests_customer_concentration():
    """D4: Eval case MUST test customer concentration as valuation variable."""
    content = read(EVAL_FILE)
    terms = ['客户集中度', 'customer concentration', 'second-source', '第二来源', '供应源']
    found = sum(1 for t in terms if t.lower() in content.lower())
    assert found >= 2, f"Eval doesn't adequately test customer concentration (found {found}/{len(terms)} terms)"


def test_d4_eval_tests_valuation_link():
    """D4: Eval case MUST test valuation implication of customer concentration."""
    content = read(EVAL_FILE)
    assert any(term in content for term in ['估值', 'valuation', '倍数', 'multiple', 'margin', '收入可见度', '议价']), \
        "Eval case missing valuation implication test"


def test_d4_eval_expects_conditional_or_fail():
    """D4: Eval case must expect conditional-pass or fail when customer concentration ignored."""
    content = read(EVAL_FILE)
    assert 'conditional' in content.lower() or ('Fail' in content), \
        "Eval case should expect fail or conditional-pass verdict"


def test_d4_eval_has_scoring():
    """D4: Eval case MUST have Pass / Conditional pass / Fail scoring."""
    content = read(EVAL_FILE)
    assert "Pass" in content and "Fail" in content, "Eval case missing scoring definitions"


def test_d4_eval_references_issue_280():
    """D4: Eval case MUST reference issue #280."""
    content = read(EVAL_FILE)
    assert "280" in content, "Eval case missing issue #280 reference"


# ── D5: evals/INDEX.md ─────────────────────────────────────────────

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
    """P1: Cross-references between modified files MUST be valid."""
    checklist = read(CHECKLIST)
    template = read(TEMPLATE)
    moat = read(MOAT)

    # checklist references report-template.md
    assert 'report-template.md' in checklist, \
        "checklist must reference report-template.md"

    # template references checklist
    assert 'listed-company-report.md' in template or 'checklists/' in template, \
        "template must reference the checklist"

    # moat references checklist or template
    assert 'listed-company-report' in moat or 'report-template' in moat or '客户集中度' in moat, \
        "moat reference must link to customer concentration rules"


def test_p2_no_false_broad_deletions():
    """P2: Cross-file references from prior issues MUST still be intact."""
    valuation = read("references/valuation-methodology.md")
    checklist = read(CHECKLIST)
    template = read(TEMPLATE)

    # Previous cross-refs from #278 must remain
    assert 'valuation-methodology.md' in template, \
        "#278 cross-ref (valuation-methodology.md in template) broken"
    assert 'valuation-methodology.md' in checklist, \
        "#278 cross-ref (valuation-methodology.md in checklist) broken"
    assert 'report-template.md' in valuation, \
        "#278 cross-ref (report-template.md in valuation-methodology) broken"


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
        ("D1: customer concentration section", test_d1_has_customer_concentration_section),
        ("D1: section position", test_d1_section_position),
        ("D1: minimum checklist items", test_d1_has_minimum_checklist_items),
        ("D1: mentions second-source", test_d1_mentions_second_source),
        ("D1: mentions valuation implication", test_d1_mentions_valuation_implication),
        ("D1: no existing deleted", test_d1_no_existing_deleted),
        ("D2: customer concentration section", test_d2_has_customer_concentration_section),
        ("D2: table required columns", test_d2_table_has_required_columns),
        ("D2: table conclusion row", test_d2_table_has_conclusion_row),
        ("D2: section is optional", test_d2_section_is_optional),
        ("D2: no existing deleted", test_d2_no_existing_deleted),
        ("D3: second-source check", test_d3_has_second_source_check),
        ("D3: links to checklist", test_d3_links_to_checklist),
        ("D3: no existing deleted", test_d3_no_existing_deleted),
        ("D4: eval file exists", test_d4_eval_file_exists),
        ("D4: standard sections", test_d4_eval_has_standard_sections),
        ("D4: tests customer concentration", test_d4_eval_tests_customer_concentration),
        ("D4: tests valuation link", test_d4_eval_tests_valuation_link),
        ("D4: expects conditional or fail", test_d4_eval_expects_conditional_or_fail),
        ("D4: has scoring", test_d4_eval_has_scoring),
        ("D4: references issue 280", test_d4_eval_references_issue_280),
        ("D5: INDEX entry", test_d5_index_has_entry),
        ("D5: INDEX table format", test_d5_index_table_format),
        ("P1: cross-references valid", test_p1_cross_references_valid),
        ("P2: no false deletions from prior issues", test_p2_no_false_broad_deletions),
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
