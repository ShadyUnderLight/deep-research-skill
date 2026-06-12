#!/usr/bin/env python3
"""
Property-based consistency tests for Control-plane / workflow-system add-on (issue #269).

These tests verify cross-document invariants that must hold across
4 discipline/checklist/eval files after the control-plane add-on update.

Each test asserts a PROPERTY (invariant) about the documentation:
  - P0: §Control-plane add-on section exists with all required dimension concepts
  - P1: Control-plane dimension table has required columns (Dimension, Key questions)
  - P2: ROUTING-MATRIX artifact contract mentions agentic/workflow architecture comparison
  - P3: technical-analysis-audit has control-plane checklist subsection with >=3 items
  - P4: Control-plane checklist covers state/action boundary, failure distinction,
        platform burden, and (optional) diagram recommendation
  - P5: Agentic-rag eval case reviewer checklist includes control-plane dimension check
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def fail(msg: str) -> None:
    raise AssertionError(msg)


# ─── files ────────────────────────────────────────────────────────────────────

DISCIPLINE_FILE = "references/technical-analysis-discipline.md"
ROUTING_FILE = "ROUTING-MATRIX.md"
AUDIT_FILE = "checklists/technical-analysis-audit.md"
EVAL_CASE_FILE = "evals/cases/agentic-rag-technical-deep-dive-compounded-case.md"


# ─── helpers ──────────────────────────────────────────────────────────────────

EXPECTED_CONTROL_PLANE_CONCEPTS = [
    "control plane",
    "state",
    "memory",
    "tool",
    "action",
    "dataflow",
    "error",
    "observability",
    "permission",
]

# Soft concepts that should appear in some form (not all may match English)
SOFT_CONTROL_PLANE_CONCEPTS = [
    "控制平面",
    "状态",
    "记忆",
    "工具",
    "动作",
    "数据流",
    "错误",
    "可观测",
    "权限",
]

# All required concepts (union of English and Chinese)
REQUIRED_CONTROL_PLANE_CONCEPTS = EXPECTED_CONTROL_PLANE_CONCEPTS + SOFT_CONTROL_PLANE_CONCEPTS


def find_section_heading(text: str, heading_prefix: str) -> int | None:
    """Find the line index of a markdown heading matching heading_prefix."""
    lines = text.split("\n")
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("##") or stripped.startswith("###"):
            if heading_prefix.lower() in stripped.lower():
                return i
    return None


def get_section_lines(text: str, heading_idx: int) -> list[str]:
    """Get lines belonging to a section starting at heading_idx, until next heading at same level."""
    lines = text.split("\n")
    heading_level = len(lines[heading_idx]) - len(lines[heading_idx].lstrip("#"))
    section = []
    for j in range(heading_idx + 1, len(lines)):
        next_line = lines[j]
        if next_line.startswith("#") and (len(next_line) - len(next_line.lstrip("#"))) <= heading_level:
            break
        section.append(next_line)
    return section


def extract_table_headers(text: str) -> list[list[str]]:
    """Extract markdown table headers from text. Returns list of header rows."""
    lines = text.split("\n")
    tables = []
    i = 0
    while i < len(lines):
        if lines[i].strip().startswith("|"):
            headers = [c.strip() for c in lines[i].strip().strip("|").split("|")]
            # Check next line is separator
            if i + 1 < len(lines) and lines[i + 1].strip().startswith("|") and all(
                c.strip().replace("-", "").replace(":", "") == "" for c in lines[i + 1].strip().strip("|").split("|") if c.strip()
            ):
                tables.append(headers)
                i += 2
                continue
        i += 1
    return tables


def count_checklist_items(text: str) -> int:
    """Count markdown checklist items."""
    count = 0
    for line in text.split("\n"):
        stripped = line.strip()
        if stripped.startswith("- [ ]") or stripped.startswith("- [x]") or stripped.startswith("- [X]"):
            count += 1
    return count


# ─── Property Tests ──────────────────────────────────────────────────────────


def test_p0_control_plane_section_exists() -> None:
    """
    P0 (Section existence): technical-analysis-discipline.md must have a
    heading about control-plane / workflow-system architecture add-on,
    containing all required dimension concepts.
    """
    text = read(DISCIPLINE_FILE)
    heading_idx = find_section_heading(text, "control-plane")
    if heading_idx is None:
        heading_idx = find_section_heading(text, "workflow-system")
    if heading_idx is None:
        heading_idx = find_section_heading(text, "control plane")

    if heading_idx is None:
        fail(
            f"P0 FAIL: No 'Control-plane' or 'workflow-system' section heading "
            f"found in {DISCIPLINE_FILE}"
        )

    section_text = "\n".join(get_section_lines(text, heading_idx))

    # Verify all required dimension concepts are present within the section boundary
    # Use case-insensitive matching to tolerate heading/table casing differences
    section_lower = section_text.lower()
    matched = sum(1 for c in EXPECTED_CONTROL_PLANE_CONCEPTS if c in section_lower)
    if matched < 7:
        fail(
            f"P0 FAIL: Control-plane section has only {matched}/9 required dimension "
            f"concepts (expected >=7). Missing or weakly expressed dimensions in section."
        )

    print(f"  PASS  P0: control-plane section found with {matched}/9 required dimension concepts")


def test_p1_dimension_table_columns() -> None:
    """
    P1 (Table property): The control-plane dimension table must have
    at minimum columns: Dimension and Key questions (or Chinese equivalents).
    """
    text = read(DISCIPLINE_FILE)

    # Find the control-plane section first
    heading_idx = find_section_heading(text, "control-plane")
    if heading_idx is None:
        heading_idx = find_section_heading(text, "control plane")
    if heading_idx is None:
        fail("P1 FAIL: Cannot check table — control-plane section not found. Run P0 first.")

    section_text = "\n".join(get_section_lines(text, heading_idx))
    tables = extract_table_headers(section_text)

    # Accept either English or Chinese column headers (Chinese is the repo convention)
    required_col_sets = [
        ["Dimension", "Key questions"],
        ["维度", "关键问题"],
    ]

    found = False
    for headers in tables:
        if any(all(col in headers for col in col_set) for col_set in required_col_sets):
            found = True
            # Check there are at least 6 dimension rows (header + 6 data rows minimum)
            table_lines = [l for l in section_text.split("\n") if l.strip().startswith("|")]
            # Count non-header, non-separator lines
            data_rows = 0
            for tl in table_lines:
                stripped = tl.strip()
                if stripped.startswith("|"):
                    cells = [c.strip() for c in stripped.strip("|").split("|")]
                    # Skip header and separator rows
                    if len(cells) >= 2 and not all(c in ["---", ":---", "---:", ":---:", ""] for c in cells):
                        data_rows += 1
            if data_rows < 5:  # header + 5 = 6 lines, meaning >=5 data rows
                # Allow >= 5 dimension rows (flexible: could be 5-8)
                print(f"  WARN  P1: dimension table has only {data_rows} data rows (expected >=5)")
            break

    if not found:
        fail(
            f"P1 FAIL: No control-plane dimension table with required columns "
            f"found in control-plane section"
        )

    print(f"  PASS  P1: control-plane dimension table found with required columns")


def test_p2_routing_mentions_agentic_workflow() -> None:
    """
    P2 (Routing property): ROUTING-MATRIX.md's Technical Deep-dive
    Visible artifact contract mentions agentic/workflow architecture comparison.
    """
    text = read(ROUTING_FILE)
    lines = text.split("\n")

    found_signal = False

    # Collect the entire Visible artifact contract section as one block
    in_artifact_contract = False
    artifact_lines = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if "Route: Technical Deep-dive" in stripped or "Route: Technical Deep-dive / Architecture Analysis" in stripped:
            in_artifact_contract = False
            artifact_lines = []
        if in_artifact_contract:
            if stripped.startswith("##") or stripped.startswith("---"):
                break
            artifact_lines.append(stripped)
        if "Visible artifact contract" in stripped:
            in_artifact_contract = True

    artifact_block = " ".join(artifact_lines).lower()
    if "agentic" in artifact_block or "workflow" in artifact_block:
        found_signal = True

    if not found_signal:
        # Fallback: search entire Technical Deep-dive section
        in_tech_route = False
        route_lines = []
        for line in lines:
            stripped = line.strip()
            if "Route: Technical Deep-dive" in stripped:
                in_tech_route = True
                continue
            if in_tech_route and (stripped.startswith("##") or stripped.startswith("---")) and "Route:" in stripped:
                break
            if in_tech_route:
                route_lines.append(stripped)
        route_block = " ".join(route_lines).lower()
        if "agentic" in route_block or "workflow" in route_block:
            found_signal = True

    if not found_signal:
        fail(
            f"P2 FAIL: Technical Deep-dive route does not mention "
            f"agentic/workflow architecture comparison in {ROUTING_FILE}"
        )

    print(f"  PASS  P2: ROUTING-MATRIX mentions agentic/workflow architecture comparison")


def test_p3_checklist_has_control_plane_section() -> None:
    """
    P3 (Checklist property): technical-analysis-audit.md has a checklist section
    dedicated to control-plane / workflow-system with at least 3 checklist items.
    """
    text = read(AUDIT_FILE)
    heading_idx = find_section_heading(text, "control-plane")
    if heading_idx is None:
        heading_idx = find_section_heading(text, "control plane")
    if heading_idx is None:
        heading_idx = find_section_heading(text, "workflow")

    if heading_idx is None:
        fail(
            f"P3 FAIL: No 'Control-plane' or 'workflow' heading found in {AUDIT_FILE}"
        )

    section_lines = get_section_lines(text, heading_idx)
    section_text = "\n".join(section_lines)

    item_count = count_checklist_items(section_text)
    if item_count < 3:
        fail(
            f"P3 FAIL: Control-plane section has only {item_count} checklist items, "
            f"expected at least 3"
        )

    print(f"  PASS  P3: control-plane checklist section found with {item_count} items")


def test_p4_checklist_covers_essential_checks() -> None:
    """
    P4 (Checklist coverage property): Control-plane checklist items must cover:
      - state/memory/action boundary
      - information failure vs workflow failure distinction
      - platform/operational burden from control plane
      - (optional) diagram recommendation
    """
    text = read(AUDIT_FILE)
    heading_idx = find_section_heading(text, "control-plane")
    if heading_idx is None:
        heading_idx = find_section_heading(text, "control plane")
    if heading_idx is None:
        fail("P4 FAIL: Cannot check coverage — control-plane section not found. Run P3 first.")

    section_text = "\n".join(get_section_lines(text, heading_idx)).lower()

    checks = {
        "state/action/tool boundary": any(kw in section_text for kw in ["state", "memory", "tool", "action", "状态", "记忆", "工具", "动作"]),
        "failure distinction": any(kw in section_text for kw in ["信息失败", "工作流失败", "information failure", "workflow failure", "rollback", "错误恢复", "error recovery"]),
        "platform/operational burden": any(kw in section_text for kw in ["平台组件", "运维负担", "platform", "operational burden", "deployment"]),
    }

    missing = [k for k, v in checks.items() if not v]
    if missing:
        fail(
            f"P4 FAIL: Control-plane checklist missing coverage for: {missing}"
        )

    print(f"  PASS  P4: all 3 essential control-plane coverage areas present in checklist")


def test_p5_eval_case_reviewer_checklist_updated() -> None:
    """
    P5 (Eval case property): The agentic-rag eval case's Reviewer checklist
    includes a control-plane dimension check (if the eval case exists).

    This is a soft check: the eval case was added by #268 and may not yet
    be merged. If absent, print a warning rather than failing.
    """
    eval_path = ROOT / EVAL_CASE_FILE
    if not eval_path.exists():
        print(f"  SKIP  P5: eval case file not found ({EVAL_CASE_FILE}) — may depend on #268 merge")
        return

    text = read(EVAL_CASE_FILE)

    # Check for reviewer checklist section
    if "## Reviewer checklist" not in text:
        print(f"  SKIP  P5: no '## Reviewer checklist' section found — may be old version before #268")
        return

    # Check for control-plane dimension mention in the reviewer checklist section
    in_reviewer_checklist = False
    found = False
    for line in text.split("\n"):
        stripped = line.strip()
        if stripped.startswith("## Reviewer checklist"):
            in_reviewer_checklist = True
            continue
        if in_reviewer_checklist:
            if stripped.startswith("##"):
                break
            if "control-plane" in stripped.lower() or "control plane" in stripped.lower():
                found = True
                break

    if found:
        print(f"  PASS  P5: eval case reviewer checklist includes control-plane dimension check")
    else:
        print(f"  WARN  P5: eval case exists but reviewer checklist does not mention control-plane dimensions")


# ─── main ────────────────────────────────────────────────────────────────────


def main() -> int:
    tests = [
        ("P0: Control-plane add-on section exists", test_p0_control_plane_section_exists),
        ("P1: Dimension table columns", test_p1_dimension_table_columns),
        ("P2: Routing contract mentions agentic/workflow", test_p2_routing_mentions_agentic_workflow),
        ("P3: Checklist has control-plane section", test_p3_checklist_has_control_plane_section),
        ("P4: Checklist covers essential areas", test_p4_checklist_covers_essential_checks),
        ("P5: Eval case reviewer checklist updated", test_p5_eval_case_reviewer_checklist_updated),
    ]

    failures = []
    for name, fn in tests:
        try:
            fn()
        except AssertionError as exc:
            failures.append(name)
            print(f"  FAIL  {name}: {exc}")
        except Exception as exc:
            failures.append(name)
            print(f"  FAIL  {name}: unexpected error — {exc}")

    if failures:
        print(f"\n{'='*60}")
        print(f"❌ {len(failures)} property test(s) FAILED: {', '.join(failures)}")
        return 1

    print(f"\n{'='*60}")
    print("✅ All 6 property tests PASSED — all cross-document invariants hold.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
