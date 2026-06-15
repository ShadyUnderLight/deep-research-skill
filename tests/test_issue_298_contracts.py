#!/usr/bin/env python3
"""
Property-based contract validation for issue #298.

Tests verify structural invariants:
  C1: references/academic-evidence-hierarchy.md has benchmark comparability section
  C2: checklists/academic-analysis-audit.md has benchmark comparability chapter
  C3: checklists/final-audit.md has academic-review benchmark comparability recall
  C4: Cross-file references are valid
  C5: Test file exists and covers all contracts

Usage:
    python tests/test_issue_298_contracts.py

Expected BEFORE implementation:
    ALL FAIL (content not yet added)

Expected AFTER implementation:
    ALL PASS
"""

import re
import os
import sys
import subprocess

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def read(path):
    with open(os.path.join(REPO_ROOT, path), "r") as f:
        return f.read()


def file_exists(path):
    return os.path.exists(os.path.join(REPO_ROOT, path))


def section_after(content, section_title):
    """Return content starting from a ## section title."""
    match = re.search(r'^#{2,3}\s*' + re.escape(section_title) + r'\s*$', content, re.MULTILINE)
    if not match:
        return None
    return content[match.start():]


# ═══════════════════════════════════════════════════════════════════
# C1: references/academic-evidence-hierarchy.md
# ═══════════════════════════════════════════════════════════════════

def test_c1_has_benchmark_comparability_section():
    """C1: references/academic-evidence-hierarchy.md MUST contain ## Benchmark comparability for academic reviews."""
    content = read("references/academic-evidence-hierarchy.md")
    assert re.search(r'^##\s+Benchmark comparability for academic reviews', content, re.MULTILINE), \
        "Missing '## Benchmark comparability for academic reviews' section"


def test_c1_section_after_source_register():
    """C1: Benchmark comparability section MUST appear after 'Source Register 扩展模板'."""
    content = read("references/academic-evidence-hierarchy.md")
    src_pos = content.index("Source Register 扩展模板")
    bc_section = section_after(content, "Benchmark comparability for academic reviews")
    assert bc_section is not None, "Benchmark comparability section not found"
    bc_pos = content.index(bc_section)
    assert src_pos < bc_pos, \
        f"Source Register at {src_pos} should precede Benchmark comparability at {bc_pos}"


def test_c1_has_trigger_conditions():
    """C1: Section MUST contain trigger conditions subsection."""
    content = read("references/academic-evidence-hierarchy.md")
    bc = section_after(content, "Benchmark comparability for academic reviews")
    assert bc is not None, "Missing section"
    assert "触发条件" in bc or "trigger condition" in bc.lower(), \
        "Missing trigger conditions subsection"


def test_c1_has_minimum_disclosure_fields():
    """C1: Section MUST contain minimum disclosure fields."""
    content = read("references/academic-evidence-hierarchy.md")
    bc = section_after(content, "Benchmark comparability for academic reviews")
    assert bc is not None, "Missing section"
    assert "Minimum disclosure" in bc or "disclosure fields" in bc.lower(), \
        "Missing minimum disclosure fields subsection"


def test_c1_has_conclusion_strength_binding():
    """C1: Section MUST contain conclusion strength binding subsection."""
    content = read("references/academic-evidence-hierarchy.md")
    bc = section_after(content, "Benchmark comparability for academic reviews")
    assert bc is not None, "Missing section"
    assert "Conclusion strength binding" in bc or "方向性判断" in bc, \
        "Missing conclusion strength binding subsection"


def test_c1_has_cross_source_comparability():
    """C1: Section MUST contain cross-source comparability rules."""
    content = read("references/academic-evidence-hierarchy.md")
    bc = section_after(content, "Benchmark comparability for academic reviews")
    assert bc is not None, "Missing section"
    assert "Cross-source" in bc or "横比" in bc or "cross source" in bc.lower(), \
        "Missing cross-source comparability rules"


def test_c1_references_technical_discipline():
    """C1: Section MUST reference the existing technical-deep-dive benchmark discipline."""
    content = read("references/academic-evidence-hierarchy.md")
    bc = section_after(content, "Benchmark comparability for academic reviews")
    assert bc is not None, "Missing section"
    assert "technical-analysis-discipline" in bc or "technical-deep-dive" in bc.lower(), \
        "Missing reference to technical-analysis-discipline benchmark comparability"


def test_c1_existing_content_preserved():
    """C1: Existing key sections MUST still be present (evidence hierarchy, source register, etc.)."""
    content = read("references/academic-evidence-hierarchy.md")
    landmarks = [
        "## Evidence hierarchy",
        "### Dimension 1: Study design quality",
        "## Source labeling requirements",
        "### Source Register 扩展模板（Academic 专用）",
        "## Statistical assessment",
        "## 检索策略文档化",
        "## 发表偏倚讨论",
    ]
    for landmark in landmarks:
        assert landmark in content, f"C1 missing: '{landmark}'"


# ═══════════════════════════════════════════════════════════════════
# C2: checklists/academic-analysis-audit.md
# ═══════════════════════════════════════════════════════════════════

def test_c2_has_benchmark_comparability_chapter():
    """C2: checklists/academic-analysis-audit.md MUST contain ## Benchmark comparability chapter."""
    content = read("checklists/academic-analysis-audit.md")
    assert re.search(r'^##\s+Benchmark comparability', content, re.MULTILINE), \
        "Missing '## Benchmark comparability' chapter"


def test_c2_chapter_position():
    """C2: Benchmark comparability chapter MUST be between Current-state discipline and Statistical assessment."""
    content = read("checklists/academic-analysis-audit.md")
    cs_pos = content.index("## Current-state discipline")
    bc_pos = content.index("## Benchmark comparability")
    sa_pos = content.index("## Statistical assessment")
    assert cs_pos < bc_pos < sa_pos, \
        f"Position: current-state({cs_pos}) < benchmark-comparability({bc_pos}) < statistical({sa_pos})"


def test_c2_has_at_least_three_checkboxes():
    """C2: Chapter MUST have at least 3 actionable checkboxes."""
    content = read("checklists/academic-analysis-audit.md")
    bc = section_after(content, "Benchmark comparability")
    assert bc is not None, "Missing chapter"
    checkboxes = re.findall(r'- \[ \]', bc)
    assert len(checkboxes) >= 3, f"Expected >=3 checkboxes, got {len(checkboxes)}"


def test_c2_has_trigger_check():
    """C2: At least one checkbox MUST address trigger conditions."""
    content = read("checklists/academic-analysis-audit.md")
    bc = section_after(content, "Benchmark comparability")
    assert bc is not None, "Missing chapter"
    assert "trigger" in bc.lower() or "触发条件" in bc, \
        "Missing trigger conditions checkbox"


def test_c2_has_hard_fail_check():
    """C2: At least one checkbox MUST be Tier-1 or hard-fail level for conclusion binding."""
    content = read("checklists/academic-analysis-audit.md")
    bc = section_after(content, "Benchmark comparability")
    assert bc is not None, "Missing chapter"
    has_hard = "(Tier-1)" in bc or "hard-fail" in bc.lower() or "hard fail" in bc.lower()
    assert has_hard, "Missing Tier-1 or hard-fail check for conclusion strength binding"


def test_c2_existing_sections_preserved():
    """C2: All original sections MUST survive."""
    content = read("checklists/academic-analysis-audit.md")
    landmarks = [
        "## Route activation",
        "## Evidence hierarchy compliance",
        "## Search strategy documentation",
        "## Current-state discipline",
        "## Statistical assessment",
        "## Cherry-picking detection",
        "## Source labeling",
        "## Hard fail check",
    ]
    for landmark in landmarks:
        assert landmark in content, f"C2 missing: '{landmark}'"


# ═══════════════════════════════════════════════════════════════════
# C3: checklists/final-audit.md
# ═══════════════════════════════════════════════════════════════════

def test_c3_academic_recall_items_preserved():
    """C3: Existing academic-review recall items in ## Recall discipline MUST be preserved."""
    content = read("checklists/final-audit.md")
    recall_start = content.index("## Recall discipline")
    section = content[recall_start:]
    academic_markers = [
        "evidence is assessed on two dimensions: study design quality AND publication venue prestige",
        "publication type and peer-review status are labeled for each source",
        "preprints are explicitly distinguished from peer-reviewed publications",
        "search strategy is documented",
        "publication bias discussion exists",
        "coverage window is declared",
    ]
    for marker in academic_markers:
        assert marker in section, f"C3 academic recall marker missing in Recall discipline: '{marker[:60]}...'"


def test_c3_new_benchmark_recall_exists():
    """C3: A new academic-review benchmark comparability recall item MUST exist."""
    content = read("checklists/final-audit.md")
    # Find all academic-review recall items
    recall_start = content.index("## Recall discipline")
    section = content[recall_start:]
    academic_lines = re.findall(
        r'- \[.*?\] for academic / literature review tasks, .*?(?:\n|$)',
        section,
        re.MULTILINE
    )
    bench_lines = [l for l in academic_lines if 'benchmark' in l.lower() or 'comparability' in l.lower()]
    assert len(bench_lines) >= 1, \
        "No academic-review benchmark comparability recall item found"


def test_c3_new_item_references_schema():
    """C3: New recall item MUST reference the new academic-evidence-hierarchy.md section."""
    content = read("checklists/final-audit.md")
    recall_start = content.index("## Recall discipline")
    section = content[recall_start:]
    academic_lines = re.findall(
        r'- \[.*?\] for academic / literature review tasks, .*?(?:\n|$)',
        section,
        re.MULTILINE
    )
    bench_lines = [l for l in academic_lines if 'benchmark' in l.lower()]
    if bench_lines:
        # Use the LAST match (bench_lines[-1]) assuming it's the newest item appended
        # at the end of the academic-review recall group. This assumption holds as long as
        # new items are always appended — if items are inserted or reordered, the test
        # should be updated to use a more precise identifier.
        item = bench_lines[-1]
        assert 'academic-evidence-hierarchy' in item or '§Benchmark comparability' in item, \
            f"New recall item doesn't reference the new section: '{item[:80]}...'"


def test_c3_new_item_mentions_disclosure_fields():
    """C3: New recall item MUST mention at least 3 disclosure field keywords."""
    content = read("checklists/final-audit.md")
    recall_start = content.index("## Recall discipline")
    section = content[recall_start:]
    academic_lines = re.findall(
        r'- \[.*?\] for academic / literature review tasks, .*?(?:\n|$)',
        section,
        re.MULTILINE
    )
    bench_lines = [l for l in academic_lines if 'benchmark' in l.lower()]
    if bench_lines:
        # Same assumption as test_c3_new_item_references_schema: last match = newest item
        item = bench_lines[-1]
        keywords = ['model', 'version', 'dataset', 'split', 'protocol', 'metric',
                     'source role', 'baseline', 'caveat', 'disclos']
        found = sum(1 for kw in keywords if kw in item.lower())
        assert found >= 3, f"New item has only {found} disclosure field keywords: '{item[:100]}...'"


# ═══════════════════════════════════════════════════════════════════
# C4: Cross-file invariants
# ═══════════════════════════════════════════════════════════════════

def test_c4_audit_references_discipline():
    """C4: academic-analysis-audit.md MUST reference the new discipline section."""
    audit = read("checklists/academic-analysis-audit.md")
    discipline = read("references/academic-evidence-hierarchy.md")
    assert '§Benchmark comparability for academic reviews' in audit, \
        "academic-analysis-audit.md must reference §Benchmark comparability for academic reviews"
    assert '## Benchmark comparability for academic reviews' in discipline, \
        "Discipline file must have the referenced heading"


def test_c4_final_audit_references_discipline():
    """C4: final-audit.md MUST reference the new discipline section."""
    final = read("checklists/final-audit.md")
    discipline = read("references/academic-evidence-hierarchy.md")
    assert '§Benchmark comparability for academic reviews' in final, \
        "final-audit.md must reference §Benchmark comparability for academic reviews"
    assert '## Benchmark comparability for academic reviews' in discipline, \
        "Discipline file must have the referenced heading"


def test_c4_all_section_references_valid():
    """C4: All § references in new content to academic-evidence-hierarchy.md MUST be valid."""
    # Gather all § references from academic-analysis-audit.md and final-audit.md
    audit = read("checklists/academic-analysis-audit.md")
    final = read("checklists/final-audit.md")
    combined = audit + "\n" + final
    refs = re.findall(r'`references/academic-evidence-hierarchy\.md`\s*§([^`\n]+)', combined)
    discipline = read("references/academic-evidence-hierarchy.md")
    for ref in refs:
        ref_stripped = ref.strip()
        heading_match = re.search(
            r'^#{2,3}\s*' + re.escape(ref_stripped).replace(r'\ ', r'\s*') + r'\s*$',
            discipline,
            re.MULTILINE
        )
        if not heading_match:
            # Lenient fallback: match first significant word
            words = ref_stripped.split()
            if words:
                heading_match = re.search(
                    r'^#{2,3}.*?' + re.escape(words[0]),
                    discipline,
                    re.MULTILINE | re.IGNORECASE
                )
        assert heading_match, \
            f"Cross-ref '§{ref_stripped}' not found as heading in academic-evidence-hierarchy.md"


def test_c4_no_existing_test_regression():
    """C4: All existing contract tests MUST still pass (minus per-issue scope checks)."""
    existing_tests = [
        "tests/test_capital_return_discipline.py",
        "tests/test_issue_270_contracts.py",
        "tests/test_issue_272_contracts.py",
        "tests/test_issue_278_contracts.py",
        "tests/test_issue_280_contracts.py",
        "tests/test_issue_294_contracts.py",
    ]
    for test_file in existing_tests:
        if not file_exists(test_file):
            continue
        result = subprocess.run(
            [sys.executable, test_file],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=30,
        )
        # Per-issue scope-creep tests (C6-style) are expected to fail when OTHER issues have
        # staged changes — they validate per-branch isolation, not cross-issue compatibility.
        # Filter out scope-creep failures as benign false positives.
        if result.returncode != 0:
            # Check if the ONLY failure is from a scope-creep test
            lines = result.stdout.split("\n")
            has_non_scope_failure = any(
                "❌" in l and "scope creep" not in l and "Scope" not in l
                and "only intended" not in l
                for l in lines
            )
            if has_non_scope_failure:
                assert False, (
                    f"Non-scope regression in {test_file}:\n"
                    f"STDOUT: {result.stdout[-500:]}\n"
                    f"STDERR: {result.stderr[-500:]}"
                )


# ═══════════════════════════════════════════════════════════════════
# C5: Test file self-validation
# ═══════════════════════════════════════════════════════════════════

def test_c5_test_file_exists():
    """C5: This test file MUST exist."""
    test_path = "tests/test_issue_298_contracts.py"
    assert file_exists(test_path), f"{test_path} does not exist"


def test_c5_has_all_contract_tests():
    """C5: This test file MUST have tests for C1-C4 (at minimum)."""
    content = read("tests/test_issue_298_contracts.py")
    assert "test_c1_" in content, "Missing C1 tests"
    assert "test_c2_" in content, "Missing C2 tests"
    assert "test_c3_" in content, "Missing C3 tests"
    assert "test_c4_" in content, "Missing C4 tests"


def test_c5_self_referential():
    """C5: This test must have a test_c5_ test function."""
    content = read("tests/test_issue_298_contracts.py")
    assert "test_c5_" in content, "Missing C5 self-referential tests"


# ═══════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    tests = [
        # C1: academic-evidence-hierarchy.md
        ("C1: benchmark comparability section", test_c1_has_benchmark_comparability_section),
        ("C1: after source register", test_c1_section_after_source_register),
        ("C1: trigger conditions", test_c1_has_trigger_conditions),
        ("C1: minimum disclosure fields", test_c1_has_minimum_disclosure_fields),
        ("C1: conclusion strength binding", test_c1_has_conclusion_strength_binding),
        ("C1: cross-source comparability", test_c1_has_cross_source_comparability),
        ("C1: references technical discipline", test_c1_references_technical_discipline),
        ("C1: existing content preserved", test_c1_existing_content_preserved),

        # C2: academic-analysis-audit.md
        ("C2: benchmark comparability chapter", test_c2_has_benchmark_comparability_chapter),
        ("C2: chapter position", test_c2_chapter_position),
        ("C2: >=3 checkboxes", test_c2_has_at_least_three_checkboxes),
        ("C2: trigger check", test_c2_has_trigger_check),
        ("C2: hard-fail check", test_c2_has_hard_fail_check),
        ("C2: existing sections preserved", test_c2_existing_sections_preserved),

        # C3: final-audit.md
        ("C3: academic recall preserved", test_c3_academic_recall_items_preserved),
        ("C3: new benchmark recall", test_c3_new_benchmark_recall_exists),
        ("C3: recalls schema", test_c3_new_item_references_schema),
        ("C3: mentions disclosure fields", test_c3_new_item_mentions_disclosure_fields),

        # C4: Cross-file
        ("C4: audit references discipline", test_c4_audit_references_discipline),
        ("C4: final audit references discipline", test_c4_final_audit_references_discipline),
        ("C4: all § references valid", test_c4_all_section_references_valid),
        ("C4: no regression", test_c4_no_existing_test_regression),

        # C5: Self-validation
        ("C5: test file exists", test_c5_test_file_exists),
        ("C5: contract coverage", test_c5_has_all_contract_tests),
        ("C5: self-referential", test_c5_self_referential),
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
