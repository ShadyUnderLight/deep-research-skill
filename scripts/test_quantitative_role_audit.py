#!/usr/bin/env python3
"""Regression tests for checklists/quantitative-role-audit.md structure.

Checks:
1. Exactly one "## Route-specific checks" section (no duplicate sections).
2. Every route-specific checklist item carries a [BLOCKER] or [NON-BLOCKER] severity label.
3. All 5 expected route subsections are present.
"""

from pathlib import Path
import re

CHECKLIST = str(
    Path(__file__).resolve().parent.parent
    / "checklists"
    / "quantitative-role-audit.md"
)

CHECKLIST_PATH = Path(CHECKLIST)

EXPECTED_ROUTES = [
    "Constrained Choice",
    "Market Outlook",
    "Listed Company",
    "Startup",
    "Market Entry",
]

EXPECTED_EXCEPTION_NOTE = "例外说明"


def test_no_duplicate_route_specific_sections() -> None:
    """There must be exactly one '## Route-specific checks' heading."""
    text = CHECKLIST_PATH.read_text(encoding="utf-8")
    # Use \s*$ to tolerate trailing whitespace on the heading line
    count = len(re.findall(r"^## Route-specific checks\s*$", text, re.MULTILINE))
    assert count == 1, (
        f"Expected 1 '## Route-specific checks' section, found {count}. "
        "Remove the duplicate section."
    )
    print("  PASS  no duplicate Route-specific checks section")


def test_all_route_items_have_severity() -> None:
    """Every checklist item under route-specific subsections must carry [BLOCKER] or [NON-BLOCKER].

    Matches lines like '- [BLOCKER] ...' or '- [NON-BLOCKER] ...'
    (including checkbox variants like '- [ ] [BLOCKER] ...').

    Fails if any item line lacks a severity tag.
    """
    text = CHECKLIST_PATH.read_text(encoding="utf-8")
    lines = text.splitlines()

    in_route_section = False
    in_route_subsection = False
    failures: list[str] = []

    for i, line in enumerate(lines, start=1):
        stripped = line.strip()

        # Track section boundaries
        if stripped.startswith("## ") and "Route-specific checks" in stripped:
            in_route_section = True
            continue
        if stripped.startswith("## ") and "Route-specific checks" not in stripped:
            in_route_section = False
            in_route_subsection = False
            continue

        if not in_route_section:
            continue

        # Track subsection boundaries (###)
        if stripped.startswith("### "):
            in_route_subsection = True
            continue
        if stripped.startswith("## "):
            in_route_subsection = False
            continue

        if not in_route_subsection:
            continue

        # Skip blank lines and blockquote lines
        if not stripped or stripped.startswith(">"):
            continue

        # This is a checklist item line — check it has severity
        # Handle all checkbox variants: - [ ], - [x], - [X]
        if re.match(r"- \[[ xX]\]", stripped):
            # Checkbox without severity: "- [ ] text" (no BLOCKER/NON-BLOCKER after the checkbox)
            if not re.search(r"\[BLOCKER\]|\[NON-BLOCKER\]", stripped):
                failures.append(f"  L{i}: missing severity tag — {stripped[:80]}")
            continue

        if stripped.startswith("- "):
            # Plain bullet: must start with [BLOCKER] or [NON-BLOCKER]
            if not re.match(r"- \[(BLOCKER|NON-BLOCKER)\]", stripped):
                failures.append(f"  L{i}: missing severity tag — {stripped[:80]}")
            continue

    assert not failures, (
        f"Found {len(failures)} route-specific items without severity labels:\n"
        + "\n".join(failures)
    )
    print("  PASS  all route-specific items have severity labels")


def test_all_expected_routes_present() -> None:
    """All 5 expected route subsections must appear under the Route-specific checks block."""
    text = CHECKLIST_PATH.read_text(encoding="utf-8")
    lines = text.splitlines()

    in_route_section = False
    found_routes: list[str] = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("## ") and "Route-specific checks" in stripped:
            in_route_section = True
            continue
        if stripped.startswith("## ") and "Route-specific checks" not in stripped:
            in_route_section = False
            continue
        if in_route_section and stripped.startswith("### "):
            found_routes.append(stripped)

    # Match against the exact ### heading prefix pattern
    # e.g. "### Constrained Choice / Shortlist / Option Selection"
    found_names = []
    for route_line in found_routes:
        for expected in EXPECTED_ROUTES:
            # Use more precise match: expect the route name at the start of the heading text
            if route_line.startswith(f"### {expected}") and expected not in found_names:
                found_names.append(expected)

    missing = [r for r in EXPECTED_ROUTES if r not in found_names]
    assert not missing, (
        f"Missing route subsection(s) under Route-specific checks: {missing}. "
        f"Found subsections: {found_routes}"
    )
    print("  PASS  all expected route subsections present")


def test_exception_note_present() -> None:
    """The exception note blockquote must exist under the Route-specific checks section."""
    text = CHECKLIST_PATH.read_text(encoding="utf-8")
    lines = text.splitlines()

    in_route_section = False
    found_note = False

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("## ") and "Route-specific checks" in stripped:
            in_route_section = True
            continue
        if stripped.startswith("## ") and "Route-specific checks" not in stripped:
            in_route_section = False
            continue
        if in_route_section and EXPECTED_EXCEPTION_NOTE in stripped:
            found_note = True
            break

    assert found_note, (
        f"Expected exception note containing '{EXPECTED_EXCEPTION_NOTE}' "
        "under Route-specific checks section."
    )
    print("  PASS  exception note present")


def main() -> int:
    tests = [
        test_no_duplicate_route_specific_sections,
        test_all_route_items_have_severity,
        test_all_expected_routes_present,
        test_exception_note_present,
    ]
    failures: list[str] = []
    for test in tests:
        try:
            test()
        except AssertionError as exc:
            failures.append(test.__name__)
            print(f"  FAIL  {test.__name__}: {exc}")
        except Exception as exc:
            failures.append(test.__name__)
            print(f"  ERROR {test.__name__}: {exc}")

    if failures:
        print(f"\n✗ {len(failures)} test(s) failed: {', '.join(failures)}")
        return 1

    print(f"\n✓ all {len(tests)} tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
