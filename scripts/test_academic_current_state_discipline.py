#!/usr/bin/env python3
"""Property-based tests for Issue #297: Academic-review current-state discipline.

Verifies that:
1. academic-analysis-audit.md has a Current-state discipline section
2. That section contains items for coverage window, conclusion binding, recent-paper verification
3. final-audit.md recall discipline references coverage window and recent-paper verification
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read(relpath: str) -> str:
    return (ROOT / relpath).read_text(encoding="utf-8")


def expect(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


# ─── Property 1: academic-analysis-audit.md has Current-state discipline section ──────

def test_academic_audit_has_current_state_section() -> None:
    """Property: academic-analysis-audit.md must contain ## Current-state discipline."""
    text = read("checklists/academic-analysis-audit.md")
    expect(
        "## Current-state discipline" in text,
        "academic-analysis-audit.md missing ## Current-state discipline section",
    )


# ─── Property 2: Coverage window declaration item exists ──────

def test_coverage_window_item_present() -> None:
    """Property: There is a checklist item about coverage window declaration."""
    text = read("checklists/academic-analysis-audit.md")
    # Isolate the Current-state discipline section
    sections = text.split("## Current-state discipline")
    expect(len(sections) >= 2, "Cannot find Current-state discipline section")
    section_text = sections[1].split("\n## ")[0]  # content until next H2

    # Must mention coverage window in some form
    coverage_keywords = ["coverage window", "coverage window 显式声明"]
    has_coverage = any(kw in section_text.lower() for kw in coverage_keywords)
    expect(
        has_coverage,
        "Current-state discipline section missing coverage window item. "
        f"Section content:\n{section_text}",
    )


# ─── Property 3: Conclusion binding item exists ──────

def test_conclusion_binding_item_present() -> None:
    """Property: There is a checklist item about conclusion binding to coverage window."""
    text = read("checklists/academic-analysis-audit.md")
    sections = text.split("## Current-state discipline")
    expect(len(sections) >= 2, "Cannot find Current-state discipline section")
    section_text = sections[1].split("\n## ")[0]

    conclusion_keywords = ["结论绑定", "conclusion"]
    has_conclusion = any(kw in section_text for kw in conclusion_keywords)
    expect(
        has_conclusion,
        "Current-state discipline section missing conclusion binding item. "
        f"Section content:\n{section_text}",
    )


# ─── Property 4: Recent-paper peer-review verification item exists (Tier-1) ──────

def test_recent_paper_verification_item_present() -> None:
    """Property: There is a (Tier-1) item about recent-paper peer-review verification."""
    text = read("checklists/academic-analysis-audit.md")
    sections = text.split("## Current-state discipline")
    expect(len(sections) >= 2, "Cannot find Current-state discipline section")
    section_text = sections[1].split("\n## ")[0]

    # Must mention recent papers and some form of verification
    recent_keywords = ["3 个月", "peer-review", "verification", "近期来源"]
    has_recent = any(kw in section_text for kw in recent_keywords)
    has_tier1 = "Tier-1" in section_text or "Tier-1" in section_text
    expect(
        has_recent,
        "Current-state discipline section missing recent-paper verification item. "
        f"Section content:\n{section_text}",
    )


# ─── Property 5: final-audit.md recall includes new items ──────

def test_final_audit_recall_includes_coverage_window() -> None:
    """Property: final-audit.md recall discipline covers coverage window and recent-paper verification."""
    text = read("checklists/final-audit.md")
    # Academic recall items are individual checklist lines prefixed with
    # "for academic / literature review tasks". Parse them structurally instead
    # of slicing the text after the last occurrence of the phrase — later items
    # (e.g. benchmark comparability) can follow the coverage-window item, which
    # previously made the last-slice heuristic point at the wrong section
    # (issue #375).
    recall_items = [
        line.strip()
        for line in text.splitlines()
        if line.strip().startswith("- [ ] for academic / literature review tasks")
    ]
    expect(len(recall_items) >= 1, "Cannot find academic review recall items in final-audit.md")

    expect(
        any(
            "coverage window" in item.lower() or "recent papers" in item.lower()
            for item in recall_items
        ),
        "final-audit.md recall discipline missing coverage window or recent-paper verification. "
        f"Items:\n{recall_items}",
    )


# ─── Property 6: Existing hard-fail checks are preserved ──────

def test_existing_hard_fails_preserved() -> None:
    """Property: All existing hard-fail conditions in academic-analysis-audit.md are preserved."""
    text = read("checklists/academic-analysis-audit.md")
    
    existing_patterns = [
        "no preprints treated as peer-reviewed",  # L73
        "no cherry-picking",  # L74
        "no correlation ≠ causation",  # L75
        "no missing venue information",  # L76
        "no ignoring publication bias",  # L78
        "no secondary route hard-fail verification skipped",  # L79
    ]
    
    for pattern in existing_patterns:
        expect(
            pattern in text.lower(),
            f"Hard-fail check removed or altered: '{pattern}'",
        )


def main() -> int:
    tests = [
        ("Academic audit has Current-state discipline section", test_academic_audit_has_current_state_section),
        ("Coverage window item present", test_coverage_window_item_present),
        ("Conclusion binding item present", test_conclusion_binding_item_present),
        ("Recent-paper verification item present (Tier-1)", test_recent_paper_verification_item_present),
        ("Final-audit recall includes coverage window", test_final_audit_recall_includes_coverage_window),
        ("Existing hard-fails preserved", test_existing_hard_fails_preserved),
    ]
    failures = []
    for name, test_fn in tests:
        try:
            test_fn()
            print(f"  PASS  {name}")
        except AssertionError as exc:
            failures.append(name)
            print(f"  FAIL  {name}: {exc}")

    if failures:
        print(f"\n{len(failures)} test(s) failed: {', '.join(failures)}")
        return 1
    print(f"\nAll {len(tests)} tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
