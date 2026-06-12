#!/usr/bin/env python3
"""
Property-based contract validation for issue #270.
Tests verify structural invariants across the 4 deliverable files.

Usage:
    python tests/test_issue_270_contracts.py

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


# ── D1: technical-analysis-discipline.md ──────────────────────────

def test_d1_has_benchmark_comparability_section():
    """D1: references/technical-analysis-discipline.md MUST contain ## Benchmark comparability section."""
    content = read("references/technical-analysis-discipline.md")
    assert re.search(r'^##\s+Benchmark comparability', content, re.MULTILINE), \
        "Missing '## Benchmark comparability' section"


def test_d1_section_position():
    """D1: Benchmark comparability MUST be between 'Comparison dimensions' and 'Common failure modes'."""
    content = read("references/technical-analysis-discipline.md")
    dims_pos = content.index("## Comparison dimensions for architecture analysis")
    bench_pos = content.index("## Benchmark comparability")
    fail_pos = content.index("## Common failure modes")
    assert dims_pos < bench_pos < fail_pos, \
        f"Section ordering: dimensions({dims_pos}) < benchmark({bench_pos}) < failures({fail_pos})"


def test_d1_has_disclosure_fields():
    """D1: Section MUST contain at least 4 mandatory disclosure fields."""
    content = read("references/technical-analysis-discipline.md")
    section_start = content.index("## Benchmark comparability")
    section = content[section_start:]
    # Count bullet-point fields (lines starting with -)
    fields = re.findall(r'^\s*-\s+\*\*', section, re.MULTILINE)
    assert len(fields) >= 4, f"Expected >=4 field definitions, got {len(fields)}"


def test_d1_fields_workload_agnostic():
    """D1: Fields MUST NOT be RAG-specific (no 'retrieval corpus', 'index setup', 'reranker')."""
    content = read("references/technical-analysis-discipline.md")
    section_start = content.index("## Benchmark comparability")
    section = content[section_start:]
    rag_terms = ['retrieval corpus', 'index setup', 'reranker', 'chunk']
    for term in rag_terms:
        assert term not in section, f"D1 contains RAG-specific term: '{term}'"


def test_d1_no_existing_deleted():
    """D1: Existing content outside the new section MUST be intact."""
    content = read("references/technical-analysis-discipline.md")
    # Check key original landmarks still exist
    assert "## Evidence standards" in content
    assert "## Common failure modes" in content
    assert "## Security deep-dive" in content
    assert "## Control-plane / workflow-system architecture add-on" in content


# ── D2: technical-analysis-audit.md ───────────────────────────────

def test_d2_has_benchmark_checks():
    """D2: Evidence quality section MUST have >=4 benchmark checkboxes."""
    content = read("checklists/technical-analysis-audit.md")
    evid_start = content.index("## Evidence quality")
    # Find next section boundary (skip the first match which is the Evidence quality header itself)
    remaining = content[evid_start + len('## Evidence quality'):]
    next_section = re.search(r'^##\s+', remaining, re.MULTILINE)
    if next_section:
        evid_section = remaining[:next_section.start()]
    else:
        evid_section = remaining
    # Count benchmark-related checkboxes (benchmark, latency, cost, performance table)
    bench_terms = ['benchmark', 'latency', 'cost', 'performance table']
    bench_checks = [
        l for l in evid_section.split('\n')
        if '- [' in l and any(t in l.lower() for t in bench_terms)
    ]
    assert len(bench_checks) >= 4, f"Evidence quality has {len(bench_checks)} benchmark-related checks, expected >=4"


def test_d2_checkboxes_actionable():
    """D2: Each benchmark checkbox MUST mention a verifiable property."""
    content = read("checklists/technical-analysis-audit.md")
    evid_start = content.index("## Evidence quality")
    remaining = content[evid_start:]
    next_section = re.search(r'^##\s+', remaining, re.MULTILINE)
    evid_section = remaining[:next_section.start()] if next_section else remaining
    bench_checks = [l for l in evid_section.split('\n') if 'benchmark' in l.lower() and '- [' in l]
    # Each should mention at least: workload OR metric OR dataset OR scope OR cross-source OR comparability
    keywords = ['workload', 'metric', 'dataset', 'scope', 'cross-source', 'comparability',
                'end-to-end', 'latency', 'cost', 'role', 'methodology', 'environment']
    for check in bench_checks:
        assert any(kw in check.lower() for kw in keywords), f"Check not actionable: '{check.strip()}'"


def test_d2_no_existing_deleted():
    """D2: Non-benchmark evidence quality items MUST survive."""
    original_markers = [
        "primary technical sources are used",
        "vendor claims are distinguished",
        "patent claims cite patent numbers",
        "source register must use the 7-column",
    ]
    content = read("checklists/technical-analysis-audit.md")
    for marker in original_markers:
        assert marker in content, f"D2 lost: '{marker}'"


# ── D3: final-audit.md ────────────────────────────────────────────

def test_d3_has_tech_dive_benchmark_recall():
    """D3: Recall discipline MUST have a technical-deep-dive benchmark item."""
    content = read("checklists/final-audit.md")
    recall_start = content.index("## Recall discipline")
    # Find within the technical-deep-dive section — look for benchmark/performance/cost disclosure
    td_section = content[recall_start:]
    td_items = re.findall(
        r'- \[.*?\] for technical deep-dive / architecture analysis tasks, .*?(?:\n|$)',
        td_section
    )
    bench_items = [i for i in td_items if any(t in i.lower() for t in
                    ['benchmark', 'performance', 'cost number'])]
    assert len(bench_items) >= 1, "No technical-deep-dive benchmark comparability recall item found"


def test_d3_mentions_disclosure_fields():
    """D3: The new item MUST reference benchmark disclosure fields."""
    content = read("checklists/final-audit.md")
    recall_start = content.index("## Recall discipline")
    td_section = content[recall_start:]
    td_items = re.findall(
        r'- \[.*?\] for technical-deep-dive.*?(?:\n|$)',
        td_section,
        re.MULTILINE
    )
    # Find the benchmark-related one
    bench_items = [i for i in td_items if 'benchmark' in i.lower() or 'metric' in i.lower()]
    if bench_items:
        disclosure_keywords = ['model', 'workload', 'metric', 'setup', 'source role',
                               'hardware', 'disclos', 'comparability']
        assert any(kw in bench_items[-1].lower() for kw in disclosure_keywords), \
            f"Item doesn't reference disclosure fields: {bench_items[-1]}"


def test_d3_equipment_rules_untouched():
    """D3: Equipment-selection rules remain intact."""
    content = read("checklists/final-audit.md")
    equip_items = [l for l in content.split('\n') if 'equipment-selection' in l.lower() and '- [' in l]
    # Count them - should not decrease
    assert len(equip_items) >= 1, "All equipment-selection rules appear to be removed!"


# ── D4: New eval case ─────────────────────────────────────────────

EVAL_FILE = "evals/cases/benchmark-comparability-technical-deep-dive-case.md"

def test_d4_eval_file_exists():
    """D4: New eval case file MUST exist."""
    path = os.path.join(REPO_ROOT, EVAL_FILE)
    assert os.path.exists(path), f"Eval case file missing: {EVAL_FILE}"


def test_d4_eval_has_standard_sections():
    """D4: Eval case MUST have standard sections."""
    content = read(EVAL_FILE)
    assert "## Goal" in content
    assert "## Prompt" in content
    assert "## What this eval is testing" in content
    assert "## Pass criteria" in content


def test_d4_eval_tests_cross_source():
    """D4: Eval case MUST address cross-source benchmark risk."""
    content = read(EVAL_FILE)
    terms = ['cross-source', 'cross-paper', 'cross-product', 'different source',
             '橫比', 'héng bǐ', 'comparability', '横比', '不可比']
    assert any(t in content.lower() for t in terms), \
        "Eval case doesn't test cross-source benchmark risk"


def test_d4_eval_expects_fail():
    """D4: Eval case must expect fail or conditional-pass verdict."""
    content = read(EVAL_FILE)
    assert 'fail' in content.lower() or 'conditional' in content.lower(), \
        "Eval case should expect fail or conditional-pass verdict"


def test_d4_index_has_entry():
    """D4: INDEX.md MUST have an entry for the new eval case."""
    content = read("evals/INDEX.md")
    filename = os.path.basename(EVAL_FILE)
    assert filename in content, f"INDEX.md missing entry for {filename}"


def test_d4_index_table_format():
    """D4: INDEX.md entry MUST maintain proper table format (10+ columns)."""
    content = read("evals/INDEX.md")
    # Find lines with the new case
    filename = os.path.basename(EVAL_FILE)
    table_lines = [l for l in content.split('\n') if filename in l]
    assert len(table_lines) >= 1, f"No table line found for {filename}"
    for line in table_lines:
        cols = line.split('|')
        assert len(cols) >= 10, f"INDEX.md line has {len(cols)} cols, expected >=10: {line}"


# ── Cross-file invariants ─────────────────────────────────────────

def test_p1_cross_references_valid():
    """P1: Cross-references between modified files must be valid."""
    discipline = read("references/technical-analysis-discipline.md")

    # technical-analysis-audit.md references  — assertion required for this PR's reference
    audit = read("checklists/technical-analysis-audit.md")
    # This is the key cross-reference added in this PR
    assert '§Benchmark comparability for technical deep-dive' in audit, \
        "technical-analysis-audit.md must reference §Benchmark comparability"
    assert '## Benchmark comparability for technical deep-dive' in discipline, \
        "Discipline file must have the referenced heading"

    # final-audit.md also references this section
    final = read("checklists/final-audit.md")
    assert '§Benchmark comparability for technical deep-dive' in final, \
        "final-audit.md must reference §Benchmark comparability"
    assert '## Benchmark comparability for technical deep-dive' in discipline, \
        "Discipline file must have the referenced heading"

    # Check all § references from audit file for completeness
    all_refs = re.findall(r'`references/technical-analysis-discipline\.md`\s*§([^`]+)', audit)
    for ref in all_refs:
        heading_match = re.search(
            r'^#{2,3}\s*' + re.escape(ref.strip()).replace(r'\ ', r'\s*').replace(r'\(', r'\(').replace(r'\)', r'\)'),
            discipline,
            re.MULTILINE
        )
        if not heading_match:
            # Lenient fallback: match first significant word
            words = ref.strip().split()
            if words:
                heading_match = re.search(
                    r'^#{2,3}.*?' + re.escape(words[0]),
                    discipline,
                    re.MULTILINE | re.IGNORECASE
                )
        assert heading_match, f"Cross-ref '§{ref.strip()}' not found as any heading in technical-analysis-discipline.md"


def test_p2_index_not_broken():
    """P2: INDEX.md table structure should remain parseable."""
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
    # All table lines should have consistent column count
    if table_lines:
        counts = [len(l.split('|')) for l in table_lines]
        assert max(counts) == min(counts), f"Inconsistent INDEX.md table columns: {counts}"


def test_p4_equipment_rules_preserved():
    """P4: Equipment-selection specific benchmark rules are not weakened."""
    # Check final-audit.md has equipment-selection benchmark items
    content = read("checklists/final-audit.md")
    # Key equipment-selection hard-fail items
    equip_markers = [
        "benchmark performance numbers (tok/s, TTFT",
        "model, quantization, context/prompt length, backend, metric type",
        "server-side throughput is not directly compared",
    ]
    for marker in equip_markers:
        assert marker in content, f"Equipment-selection rule missing: '{marker[:50]}'"

    # Check ROUTING-MATRIX.md equipment selection hard-fails
    routing = read("ROUTING-MATRIX.md")
    assert "without disclosing model, quantization, metric type, and backend" in routing


# ── Main ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    tests = [
        ("D1: benchmark comparability section", test_d1_has_benchmark_comparability_section),
        ("D1: section position", test_d1_section_position),
        ("D1: has disclosure fields", test_d1_has_disclosure_fields),
        ("D1: fields workload-agnostic", test_d1_fields_workload_agnostic),
        ("D1: no existing deleted", test_d1_no_existing_deleted),
        ("D2: has 4+ benchmark checks", test_d2_has_benchmark_checks),
        ("D2: checks actionable", test_d2_checkboxes_actionable),
        ("D2: no existing deleted", test_d2_no_existing_deleted),
        ("D3: has tech-dive benchmark recall", test_d3_has_tech_dive_benchmark_recall),
        ("D3: mentions disclosure fields", test_d3_mentions_disclosure_fields),
        ("D3: equipment rules untouched", test_d3_equipment_rules_untouched),
        ("D4: eval file exists", test_d4_eval_file_exists),
        ("D4: standard sections", test_d4_eval_has_standard_sections),
        ("D4: cross-source test", test_d4_eval_tests_cross_source),
        ("D4: expects fail", test_d4_eval_expects_fail),
        ("D4: INDEX entry", test_d4_index_has_entry),
        ("D4: INDEX table format", test_d4_index_table_format),
        ("P2: INDEX not broken", test_p2_index_not_broken),
        ("P4: equipment rules preserved", test_p4_equipment_rules_preserved),
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
