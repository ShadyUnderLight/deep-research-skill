#!/usr/bin/env python3
"""Validate that ROUTING-MATRIX.md contains the route selection decision tree,
and the old fixed-priority-only section has been replaced.

Property-based structural test suite.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def read_file(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _section_after_heading(content: str, heading: str) -> str:
    """Extract the section body following a ## heading, up to the next ## heading."""
    start = content.find(heading)
    if start == -1:
        return ""
    section = content[start:]
    # Skip the heading line itself
    rest = section[section.index("\n") + 1:]
    next_heading = re.search(r"\n## ", rest)
    if next_heading:
        rest = rest[:next_heading.start() + 1]
    return rest


def test_decision_tree_section_exists():
    """ROUTING-MATRIX.md MUST contain '## Route selection decision tree' section."""
    content = read_file(REPO_ROOT / "ROUTING-MATRIX.md")
    assert "## Route selection decision tree" in content, (
        "Missing '## Route selection decision tree' section in ROUTING-MATRIX.md"
    )
    _ = _section_after_heading(content, "## Route selection decision tree")


def test_old_routing_priority_replaced_or_demoted():
    """The old '## Routing priority' standalone section MUST be gone.

    It may only appear as a subsection heading (### Routing tie-breaker) or not at all."""
    content = read_file(REPO_ROOT / "ROUTING-MATRIX.md")
    # Count occurrences of '## Routing priority' as a standalone H2 heading
    # This matches only the old-style section header, not '### Routing ...' subsections
    count = len(re.findall(r"^## Routing priority$", content, re.MULTILINE))
    assert count == 0, (
        f"'## Routing priority' H2 section found {count} time(s) in ROUTING-MATRIX.md. "
        "It must be replaced with '## Route selection decision tree'."
    )


def test_decision_tree_has_four_steps():
    """The decision tree section MUST contain Step 1-4 markers."""
    content = read_file(REPO_ROOT / "ROUTING-MATRIX.md")
    section = _section_after_heading(content, "## Route selection decision tree")
    assert section, "Decision tree section not found (empty section body)"

    for step_num in range(1, 5):
        # Match patterns: "### Step 1", "**Step 1**", "Step 1 —", "Step 1:"
        pattern = rf"(?:###\s+|\\*\\*)?Step {step_num}\b"
        assert re.search(pattern, section), (
            f"Step {step_num} not found in decision tree section"
        )


def test_tie_breaker_retains_all_routes():
    """The tie-breaker table (step 4) MUST list all 11 specialized routes
    in the original priority order, within the Step 4 subsection only."""
    content = read_file(REPO_ROOT / "ROUTING-MATRIX.md")
    section = _section_after_heading(content, "## Route selection decision tree")
    assert section, "Decision tree section not found"

    # Narrow to the Step 4 subsection only
    step4_start = section.find("### Step 4")
    assert step4_start != -1, "Step 4 subsection not found in decision tree"
    step4_section = section[step4_start:]
    # Cut at next ### heading if any
    next_h3 = re.search(r"\n### ", step4_section[1:])
    if next_h3:
        step4_section = step4_section[:next_h3.start() + 1]

    expected_routes = [
        "listed-company",
        "startup-evaluation",
        "market-entry",
        "regulatory-analysis",
        "provider-selection",
        "competitive-positioning",
        "technical-deep-dive",
        "equipment-selection",
        "market-outlook",
        "constrained-choice",
        "academic-review",
    ]

    positions = {}
    for route_id in expected_routes:
        pos = step4_section.find(route_id)
        if pos != -1:
            positions[route_id] = pos

    sorted_by_pos = sorted(positions.items(), key=lambda x: x[1])
    found_ordered = [rid for rid, _ in sorted_by_pos]

    missing = set(expected_routes) - set(found_ordered)
    assert not missing, (
        f"Tie-breaker table missing routes: {missing}"
    )
    assert found_ordered == expected_routes, (
        f"Tie-breaker routes not in correct order.\n"
        f"Expected: {expected_routes}\n"
        f"Found:    {found_ordered}"
    )


def test_route_index_tie_breaker_annotation():
    """references/route-index.md MUST annotate priority as tie-breaker only."""
    content = read_file(REPO_ROOT / "references/route-index.md")

    has_tie_breaker = (
        "tie-break" in content.lower()
        or "tie break" in content.lower()
        or "decision tree" in content.lower()
    )
    assert has_tie_breaker, (
        "references/route-index.md must annotate the priority list as tie-breaker only "
        "or reference the decision tree"
    )

    # Must still contain the full priority line (as the tie-breaker list)
    assert "listed-company" in content, "listed-company missing from route-index.md"
    assert "academic-review" in content, "academic-review missing from route-index.md"


def test_route_activation_references_decision_tree():
    """references/route-activation-and-preflight.md MUST reference
    the decision tree (in any section — Preflight Step 1 is the expected location)."""
    content = read_file(REPO_ROOT / "references/route-activation-and-preflight.md")

    # Decision tree reference may be in Preflight Step 1 (after the "Do not use"
    # clause check), not necessarily in "How to choose the primary route" section.
    # Search the entire file.
    has_reference = (
        "decision tree" in content.lower()
        or "route selection decision tree" in content.lower()
    )
    assert has_reference, (
        "route-activation-and-preflight.md must reference the decision tree"
    )

    # Also verify ROUTING-MATRIX.md is mentioned (the decision tree lives there)
    assert "ROUTING-MATRIX.md" in content, (
        "route-activation-and-preflight.md must reference ROUTING-MATRIX.md"
    )


if __name__ == "__main__":
    failures: list[str] = []
    tests = [
        ("decision_tree_section_exists", test_decision_tree_section_exists),
        ("old_routing_priority_replaced", test_old_routing_priority_replaced_or_demoted),
        ("decision_tree_has_four_steps", test_decision_tree_has_four_steps),
        ("tie_breaker_retains_all_routes", test_tie_breaker_retains_all_routes),
        ("route_index_tie_breaker_annotation", test_route_index_tie_breaker_annotation),
        ("route_activation_references_decision_tree", test_route_activation_references_decision_tree),
    ]

    for name, fn in tests:
        try:
            fn()
            print(f"  PASS  {name}")
        except AssertionError as e:
            print(f"  FAIL  {name}: {e}")
            failures.append(name)

    if failures:
        print(f"\n{failures} test(s) failed")
        sys.exit(1)
    else:
        print("\nAll tests passed.")
        sys.exit(0)
