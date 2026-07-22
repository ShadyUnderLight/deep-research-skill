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


# ── Behavioral route fixtures ──────────────────────────────────────────────

def _decision_tree_section() -> str:
    """Return the full decision tree section from ROUTING-MATRIX.md."""
    content = read_file(REPO_ROOT / "ROUTING-MATRIX.md")
    return _section_after_heading(content, "## Route selection decision tree")


def _step1_section() -> str:
    """Return the Step 1 subsection."""
    section = _decision_tree_section()
    start = section.find("### Step 1")
    assert start != -1, "Step 1 not found"
    body = section[start:]
    next_h3 = re.search(r"\n### Step 2\b", body)
    if next_h3:
        body = body[:next_h3.start() + 1]
    return body


def _step2_section() -> str:
    """Return the Step 2 subsection."""
    section = _decision_tree_section()
    start = section.find("### Step 2")
    assert start != -1, "Step 2 not found"
    body = section[start:]
    next_h3 = re.search(r"\n### Step 3\b", body)
    if next_h3:
        body = body[:next_h3.start() + 1]
    return body


def _step2_object_routes() -> dict[str, list[str]]:
    """Parse Step 2 table: weight-bearing object → list of route candidate(s)."""
    section = _step2_section()
    mapping: dict[str, list[str]] = {}
    in_table = False
    for line in section.split("\n"):
        stripped = line.strip()
        if stripped.startswith("| Weight-bearing object"):
            in_table = True
            continue
        if not in_table:
            continue
        if stripped.startswith("|---"):
            continue
        if stripped.startswith("|") and "`" in stripped:
            cols = [c.strip() for c in stripped.strip("|").split("|")]
            if len(cols) >= 2:
                object_name = cols[0].strip()
                route_cell = cols[1].strip()
                # Extract all backtick-quoted route IDs
                route_ids = re.findall(r"`([a-z]+(?:-[a-z]+)*)`", route_cell)
                if route_ids and object_name:
                    mapping[object_name] = route_ids
        elif stripped.startswith("|") and not in_table:
            continue
        elif stripped.startswith("When an object matches"):
            break  # end of table
    return mapping


def test_step1_covers_all_action_categories():
    """Step 1 must define exactly the action categories that map to routes."""
    section = _step1_section()
    # Must list all 9 major action categories
    required = [
        "Select",
        "Enter",
        "Judge direction",
        "Judge regulation",
        "Judge listed-company",
        "Judge private-company",
        "Judge technical",
        "Judge academic",
        "Judge positioning",
    ]
    for keyword in required:
        assert keyword in section, f"Step 1 missing action category: {keyword}"


def test_step2_maps_to_known_route_ids():
    """Every route ID in Step 2 must exist in route-manifest.json."""
    import json
    manifest_path = REPO_ROOT / "schemas" / "route-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    valid_ids = {r["id"] for r in manifest["routes"]}

    mapping = _step2_object_routes()
    for obj_name, route_ids in mapping.items():
        for rid in route_ids:
            assert rid in valid_ids, (
                f"Step 2 object '{obj_name}' maps to unknown route '{rid}'"
            )


def test_step2_each_object_has_unique_candidate():
    """Each weight-bearing object row must map to 1-3 unique candidate routes."""
    mapping = _step2_object_routes()
    for obj_name, route_ids in mapping.items():
        assert 1 <= len(route_ids) <= 3, (
            f"Step 2 object '{obj_name}' has {len(route_ids)} candidates, "
            f"expected 1-3"
        )


def test_step2_disambiguation_rule_exists():
    """Step 2 must include a disambiguation rule for multi-match objects."""
    section = _step2_section()
    has_rule = (
        "most specific" in section.lower()
        or "more specific" in section.lower()
    )
    assert has_rule, (
        "Step 2 must include a 'most specific row wins' disambiguation rule "
        "for objects matching multiple rows"
    )


def test_step3_references_boundary_clauses():
    """Step 3 must reference per-route 'Do not use' and boundary resolution."""
    section = _decision_tree_section()
    step3_start = section.find("### Step 3")
    assert step3_start != -1
    step3 = section[step3_start:]
    next_h3 = re.search(r"\n### Step 4\b", step3)
    if next_h3:
        step3 = step3[:next_h3.start() + 1]

    assert "Do not use" in step3, "Step 3 must reference 'Do not use' clauses"
    assert "boundary" in step3.lower(), (
        "Step 3 must reference boundary resolution"
    )


def test_step4_is_explicitly_last_resort():
    """Step 4 tie-breaker must be labeled as last-resort, not default."""
    section = _decision_tree_section()
    step4_start = section.find("### Step 4")
    assert step4_start != -1
    step4 = section[step4_start:]
    next_h3 = re.search(r"\n### ", step4[1:])
    if next_h3:
        step4 = step4[:next_h3.start() + 1]

    # Must emphasize that Step 4 is only for unresolved cases
    keywords = ["only", "don't resolve", "did not produce", "exhausted"]
    found = any(kw in step4.lower() for kw in keywords)
    assert found, (
        "Step 4 must explicitly state it's only for cases Steps 1-3 don't resolve"
    )


def test_sports_prediction_routes_to_constrained_choice():
    """Sports prediction keywords in Step 1 must map to constrained-choice,
    not market-outlook or provider-selection. Regression test for the
    Blocker found in Round 1 cross-review."""
    step1 = _step1_section()
    mapping = _step2_object_routes()

    # Step 1 must have sports-related Chinese example
    assert "哪支球队" in step1 or "predict" in step1.lower(), (
        "Step 1 must include sports prediction example"
    )

    # "Defined options / teams" must map to constrained-choice (single candidate)
    teams_obj = None
    for obj_name in mapping:
        if "team" in obj_name.lower() or "defined options" in obj_name.lower():
            teams_obj = obj_name
            break
    assert teams_obj is not None, (
        "Step 2 must have a 'Defined options / teams' row"
    )
    candidates = mapping[teams_obj]
    assert "constrained-choice" in candidates, (
        f"'Defined options / teams' must map to constrained-choice, got {candidates}"
    )
    # constrained-choice must be the only or highest-specificity candidate for teams
    # (after the Blocker fix, it should be a single candidate row)
    assert len(candidates) == 1, (
        f"'Defined options / teams' should have 1 candidate after Blocker fix, "
        f"got {len(candidates)}: {candidates}"
    )


def test_market_outlook_guards_against_ranking_misuse_in_step1():
    """Step 1 must distinguish 'judge direction' from 'select/rank'.
    Step 2 must not map 'market trajectory' to constrained-choice."""
    step1 = _step1_section()
    mapping = _step2_object_routes()

    # Verify the action categories are distinct
    assert "Select / rank" in step1, "Step 1 must have Select/rank category"
    assert "Judge direction" in step1, "Step 1 must have Judge direction category"

    # Market trajectory must map to market-outlook only
    market_obj = None
    for obj_name in mapping:
        if "market" in obj_name.lower() and "trajectory" in obj_name.lower():
            market_obj = obj_name
            break
    assert market_obj is not None, "Step 2 must have a market trajectory row"
    candidates = mapping[market_obj]
    assert candidates == ["market-outlook"], (
        f"Market trajectory must map only to market-outlook, got {candidates}"
    )


def test_conflict_pairs_exist():
    """At least 5 action-object conflict pairs must be documented in Step 2."""
    section = _step2_section()
    # Count "→" arrows in the conflict examples section
    conflict_start = section.find("Conflict examples")
    assert conflict_start != -1, "Conflict examples section not found"
    conflict_section = section[conflict_start:]
    arrow_count = conflict_section.count("→")
    assert arrow_count >= 5, (
        f"Expected ≥5 conflict pairs, found {arrow_count} '→' arrows"
    )


def test_shared_workflow_not_misused():
    """The decision tree must not recommend shared-workflow as an escape hatch
    for tasks that have a clear action burden and weight-bearing object."""
    section = _decision_tree_section()
    mapping = _step2_object_routes()

    # Every weight-bearing object must map to at least one specialized route
    for obj_name, route_ids in mapping.items():
        for rid in route_ids:
            assert rid != "shared-workflow", (
                f"Step 2 object '{obj_name}' maps to shared-workflow — "
                f"specialized routes must be preferred"
            )


if __name__ == "__main__":
    failures: list[str] = []
    tests = [
        # Structural tests
        ("decision_tree_section_exists", test_decision_tree_section_exists),
        ("old_routing_priority_replaced", test_old_routing_priority_replaced_or_demoted),
        ("decision_tree_has_four_steps", test_decision_tree_has_four_steps),
        ("tie_breaker_retains_all_routes", test_tie_breaker_retains_all_routes),
        ("route_index_tie_breaker_annotation", test_route_index_tie_breaker_annotation),
        ("route_activation_references_decision_tree", test_route_activation_references_decision_tree),
        # Behavioral tests — action/object coverage
        ("step1_covers_all_action_categories", test_step1_covers_all_action_categories),
        ("step2_maps_to_known_route_ids", test_step2_maps_to_known_route_ids),
        ("step2_each_object_has_unique_candidate", test_step2_each_object_has_unique_candidate),
        ("step2_disambiguation_rule_exists", test_step2_disambiguation_rule_exists),
        # Behavioral tests — boundary/guard checks
        ("step3_references_boundary_clauses", test_step3_references_boundary_clauses),
        ("step4_is_explicitly_last_resort", test_step4_is_explicitly_last_resort),
        # Behavioral tests — routing correctness (positive)
        ("sports_prediction_routes_to_constrained_choice", test_sports_prediction_routes_to_constrained_choice),
        ("market_outlook_guards_against_ranking_misuse", test_market_outlook_guards_against_ranking_misuse_in_step1),
        ("conflict_pairs_exist", test_conflict_pairs_exist),
        # Behavioral tests — negative/misuse guard
        ("shared_workflow_not_misused", test_shared_workflow_not_misused),
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
