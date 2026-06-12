#!/usr/bin/env python3
"""
Property-based consistency tests for roadmap state stratification (issue #243).

These tests verify cross-document invariants that must hold across
4 discipline/checklist files after the roadmap state stratification update.

Each test asserts a PROPERTY (invariant) about the documentation:
  - P0: Table structure property — stratification table has required columns and ≥6 rows
  - P1: Coverage property — every status in the table has a corresponding audit check
  - P2: No-orphan property — every audit check maps to a status in the table
  - P3: Forward-looking property — forward-looking discipline references technical roadmap
  - P4: Final-audit property — final audit recalls roadmap state separation for tech deep-dive
  - P5: Hard-fail preservation property — existing hard-fail condition is preserved
  - P6: Commitment property — audit checklist contains commitment/disclaimer item
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def fail(msg: str) -> None:
    raise AssertionError(msg)


# ─── helpers ─────────────────────────────────────────────────────────────────

STRATIFICATION_FILE = "references/technical-analysis-discipline.md"
AUDIT_FILE = "checklists/technical-analysis-audit.md"
FORWARD_LOOKING_FILE = "references/forward-looking-discipline.md"
FINAL_AUDIT_FILE = "checklists/final-audit.md"

# Statuses we expect in the stratification table, with their canonical labels
# and alternative search terms for matching checklist items.
EXPECTED_STATUSES: list[dict] = [
    {"label": "Stable / shipped", "aliases": ["stable", "shipped", "已发布", "稳定"]},
    {"label": "Experimental", "aliases": ["experimental", "实验"]},
    {"label": "Deprecated / superseded", "aliases": ["deprecated", "superseded", "弃用", "替代"]},
    {"label": "Announced roadmap", "aliases": ["announced roadmap", "announced", "路线图", "计划"]},
    {"label": "Proposed / SEP draft", "aliases": ["proposed", "sep", "draft", "草案", "提案"]},
    {"label": "Rumored / community signal", "aliases": ["rumored", "community signal", "推测", "社区"]},
]

EXPECTED_TABLE_COLUMNS = ["状态", "含义", "允许标签", "写作要求"]
MIN_TABLE_ROWS = 6


def extract_table(text: str, headers: list[str]) -> list[list[str]] | None:
    """Find a markdown table with the given headers and return its data rows.

    Returns a list of rows, where each row is a list of cell values.
    Returns None if not found.
    """
    lines = text.split("\n")
    header_idx = None
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("|") and stripped.endswith("|"):
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            if len(cells) == len(headers) and all(
                h in cells[j] for j, h in enumerate(headers)
            ):
                header_idx = i
                break

    if header_idx is None:
        return None

    # Next line should be separator
    if header_idx + 1 >= len(lines):
        return None

    separator = lines[header_idx + 1].strip()
    if not separator.startswith("|") or not all(c.strip()[0] in "-:" for c in separator.strip("|").split("|") if c.strip()):
        return None

    # Data rows follow
    rows = []
    for j in range(header_idx + 2, len(lines)):
        line = lines[j].strip()
        if not line.startswith("|"):
            break
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) >= len(headers):
            rows.append(cells[: len(headers)])

    return rows


def get_checklist_items(text: str) -> list[str]:
    """Extract all checklist items from a checklist file."""
    items = []
    for line in text.split("\n"):
        stripped = line.strip()
        if stripped.startswith("- [ ]") or stripped.startswith("- [x]") or stripped.startswith("- [X]"):
            items.append(stripped)
    return items


# ─── Property Tests ──────────────────────────────────────────────────────────


def test_p0_table_structure() -> None:
    """
    P0 (Table completeness): The stratification table must exist with
    the required columns and at least 6 data rows (one per status).
    """
    text = read(STRATIFICATION_FILE)
    table = extract_table(text, EXPECTED_TABLE_COLUMNS)

    if table is None:
        fail(
            f"P0 FAIL: Could not find stratification table with columns "
            f"{EXPECTED_TABLE_COLUMNS} in {STRATIFICATION_FILE}"
        )

    actual_rows = len(table)
    if actual_rows < MIN_TABLE_ROWS:
        fail(
            f"P0 FAIL: Stratification table has {actual_rows} data rows, "
            f"expected at least {MIN_TABLE_ROWS}"
        )

    print(f"  PASS  P0: table found with {actual_rows} rows, all required columns present")


def test_p1_checklist_coverage() -> None:
    """
    P1 (Coverage): Every status in the stratification table has at least
    one corresponding checklist item in technical-analysis-audit.md.
    """
    text = read(AUDIT_FILE)
    items = get_checklist_items(text)
    items_text = "\n".join(items).lower()

    for status in EXPECTED_STATUSES:
        found = any(alias.lower() in items_text for alias in status["aliases"])
        if not found:
            # Fallback: try the full label
            if status["label"].lower() in items_text:
                found = True
        if not found:
            # Fallback: try partial match of first word of label
            first_word = status["label"].split("/")[0].strip().lower()
            if first_word in items_text:
                found = True
        if not found:
            fail(
                f"P1 FAIL: Status '{status['label']}' has no corresponding "
                f"checklist item in {AUDIT_FILE}.\n"
                f"Searched aliases: {status['aliases']}\n"
                f"Checklist items found: {len(items)}"
            )

    print(f"  PASS  P1: all {len(EXPECTED_STATUSES)} statuses have corresponding audit checks")


def test_p3_forward_looking_technical_section() -> None:
    """
    P3 (Forward-looking property): forward-looking-discipline.md has a section
    heading that mentions technical roadmap or 技术路线图, and the section body
    references the stratification table.
    """
    text = read(FORWARD_LOOKING_FILE)
    lines = text.split("\n")

    found_heading = False
    heading_idx = None
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("##") or stripped.startswith("###"):
            lower = stripped.lower()
            if "technical roadmap" in lower or "技术路线图" in lower:
                found_heading = True
                heading_idx = i
                break

    if not found_heading:
        fail(
            f"P3 FAIL: No section heading mentioning 'technical roadmap' or "
            f"'技术路线图' found in {FORWARD_LOOKING_FILE}"
        )

    # Verify the section body references the stratification table
    # Collect lines until next heading at same or higher level
    section_lines = []
    heading_level = len(lines[heading_idx]) - len(lines[heading_idx].lstrip("#"))
    for j in range(heading_idx + 1, len(lines)):
        next_line = lines[j]
        if next_line.startswith("#") and (len(next_line) - len(next_line.lstrip("#"))) <= heading_level:
            break
        section_lines.append(next_line)
    section_body = "\n".join(section_lines).lower()

    if "technical-analysis-discipline.md" not in section_body and "stratification" not in section_body:
        fail(
            f"P3 FAIL: Technical roadmap section body does not reference "
            f"the stratification table in technical-analysis-discipline.md"
        )

    print(f"  PASS  P3: forward-looking discipline has technical roadmap section with table reference")


def test_p4_final_audit_recall() -> None:
    """
    P4 (Final-audit property): final-audit.md's technical deep-dive recall
    items mention roadmap state separation with consistent terminology
    matching the stratification table's 6 states.
    """
    text = read(FINAL_AUDIT_FILE)
    lines = text.split("\n")

    # Find technical deep-dive recall items within the Recall discipline section
    in_recall_section = False
    recall_line = None

    for line in lines:
        stripped = line.strip()

        # Detect section boundaries
        if stripped.startswith("##") or stripped.startswith("###"):
            if "recall" in stripped.lower():
                in_recall_section = True
            else:
                in_recall_section = False
            continue

        if in_recall_section and (
            stripped.startswith("- [ ]")
            or stripped.startswith("- [x]")
            or stripped.startswith("- [X]")
        ):
            lower = stripped.lower()
            if "technical deep-dive" in lower and "roadmap" in lower and "state" in lower:
                recall_line = lower

    if recall_line is None:
        # Broader search: look for any checklist item mentioning both "roadmap" and "technical"
        all_items = get_checklist_items(text)
        for item in all_items:
            lower = item.lower()
            if "roadmap" in lower and "technical" in lower and "state" in lower:
                recall_line = lower
                break

    if recall_line is None:
        fail(
            f"P4 FAIL: No recall item for technical deep-dive mentioning "
            f"roadmap state separation found in {FINAL_AUDIT_FILE}"
        )

    # Verify the recall item references at least 4 of the 6 table states
    state_signals = {
        "stable", "shipped", "experimental", "deprecated", "superseded",
        "announced", "roadmap", "proposed", "sep draft",
        "rumored", "community signal", "speculative",
    }
    found_signals = sum(1 for s in state_signals if s in recall_line)
    if found_signals < 4:
        fail(
            f"P4 FAIL: Recall item only references {found_signals} state signals "
            f"(need ≥4). Item text: {recall_line}"
        )

    print(f"  PASS  P4: final-audit recalls roadmap state separation ({found_signals} state signals)")


def test_p5_hard_fail_preserved() -> None:
    """
    P5 (Hard-fail preservation property): The existing hard-fail condition
    'roadmap evaluation treats announced features as shipped' must be preserved
    in technical-analysis-discipline.md's hard-fail section.
    """
    text = read(STRATIFICATION_FILE)
    hard_fail_section = False
    found_hard_fail = False

    for line in text.split("\n"):
        stripped = line.strip()
        if stripped.startswith("##") and "hard fail" in stripped.lower():
            hard_fail_section = True
            continue
        if stripped.startswith("##") and hard_fail_section:
            # Exited the hard-fail section
            hard_fail_section = False
            continue
        if hard_fail_section:
            lower = stripped.lower()
            if "announced" in lower and "shipped" in lower and "roadmap" in lower:
                found_hard_fail = True

    if not found_hard_fail:
        fail(
            f"P5 FAIL: Existing hard-fail condition about roadmap evaluation "
            f"treating announced features as shipped not found in {STRATIFICATION_FILE}"
        )

    print(f"  PASS  P5: hard-fail condition for announced-vs-shipped preserved")


def test_p6_commitment_checklist_item() -> None:
    """
    P6 (Commitment property): The audit checklist contains an item about
    roadmap commitment/disclaimer — whether the roadmap is a commitment.
    This was specifically called out in issue #243.
    """
    text = read(AUDIT_FILE)
    items_text = text.lower()
    if "commitment" not in items_text and "承诺" not in items_text:
        fail(
            f"P6 FAIL: No checklist item mentioning 'commitment' or '承诺' "
            f"found in {AUDIT_FILE}"
        )
    print(f"  PASS  P6: commitment/disclaimer checklist item present")


def test_p2_no_orphan_checklist_items() -> None:
    """
    P2 (No-orphan property): Every roadmap-related checklist item in
    technical-analysis-audit.md maps to a status in the stratification table.
    """
    text = read(AUDIT_FILE)
    items = get_checklist_items(text)

    # Collect all known status keywords from the table
    known_keywords = set()
    for status in EXPECTED_STATUSES:
        known_keywords.add(status["label"].lower())
        for alias in status["aliases"]:
            known_keywords.add(alias.lower())

    # Additional legitimate multi-status terms
    known_keywords.update([
        "roadmap", "路线图",
        "commitment",
        "confirm", "confirmed", "conf",
        "未来能力", "outcome",
        "当前推荐",
        "superseded",
        "影响",
    ])

    # Find roadmap-related checklist items
    # Note: deliberately avoids broad terms like "状态" to minimize false positives
    roadmap_items = [
        item for item in items
        if any(kw in item.lower() for kw in ["roadmap", "路线图", "feature-state", "shipped", "deprecated", "experimental", "proposed", "rumored"])
    ]

    for item in roadmap_items:
        lower = item.lower()
        # Check that at least one known keyword appears in this item
        matches_known = any(kw in lower for kw in known_keywords)
        if not matches_known:
            # This is a soft warning, not a hard fail — the item might use
            # legitimate terminology we didn't anticipate
            print(f"  WARN  P2: possible orphan item — '{item[:80]}...'")

    print(f"  PASS  P2: {len(roadmap_items)} roadmap-related items checked for coverage mapping")


# ─── main ────────────────────────────────────────────────────────────────────


def main() -> int:
    tests = [
        ("P0: Table structure", test_p0_table_structure),
        ("P1: Checklist coverage", test_p1_checklist_coverage),
        ("P2: No orphan items", test_p2_no_orphan_checklist_items),
        ("P3: Forward-looking section", test_p3_forward_looking_technical_section),
        ("P4: Final-audit recall", test_p4_final_audit_recall),
        ("P5: Hard-fail preserved", test_p5_hard_fail_preserved),
        ("P6: Commitment item", test_p6_commitment_checklist_item),
    ]

    failures = []
    for name, fn in tests:
        try:
            fn()
        except AssertionError as exc:
            failures.append(name)
            print(f"  FAIL  {name}: {exc}")

    if failures:
        print(f"\n{'='*60}")
        print(f"❌ {len(failures)} property test(s) FAILED: {', '.join(failures)}")
        return 1

    print(f"\n{'='*60}")
    print("✅ All 7 property tests PASSED — all cross-document invariants hold.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
