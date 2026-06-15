"""
Validation tests for issue #281: TSMC GPT-vs-local comparative-distillation.

These tests verify that the comparative-distillation file exists at the correct
path, follows the template structure, and has valid cross-references.

Run: pytest tests/test_tsmc_comparative_distillation.py -v
"""

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

# ── Constants ─────────────────────────────────────────────────────────────

TARGET_PATH = "evals/comparative-distillation/tsmc-gpt-vs-deep-research-skill-comparative-distillation.md"

# Required sections that must appear in the file (template compliance)
REQUIRED_SECTIONS = [
    "## Case identity",
    "## Comparison purpose",
    "## Dimension 1:",
    "## Dimension 2:",
    "## Dimension 3:",
    "## Dimension 4:",
    "## Dimension 5:",
    "## Dimension 6:",
    "## Candidate-action summary",
    "## Triage notes",
    "## Things explicitly rejected",
    "## Final judgment",
    "## Minimal quality bar",
]

# Sub-sections that each dimension must contain
DIMENSION_SUBSECTIONS = [
    "Report A",
    "Report B",
    "Gap",
    "Current status",
    "Action type",
]

# Valid action types from the template
VALID_ACTION_TYPES = {"NEW_RULE", "CHECKLIST_HARDENING", "TEMPLATE_CHANGE", "NO_ACTION"}

# Existing TSMC eval cases that should be cross-referenced
TSMC_EVAL_CASES = [
    "evals/cases/tsmc-valuation-dcf-and-sensitivity-case.md",
    "evals/cases/tsmc-valuation-time-horizon-stratification-case.md",
    "evals/cases/tsmc-customer-concentration-and-second-source-case.md",
]

# Issues that this distillation consolidates
REFERENCED_ISSUES = ["#276", "#277", "#278", "#279", "#280"]


def read(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


def file_exists(path: str) -> bool:
    return (REPO_ROOT / path).exists()


# ── Property 1: File existence ────────────────────────────────────────────


def test_comparative_distillation_file_exists():
    """Property: The comparative-distillation file must exist and be non-empty."""
    assert file_exists(TARGET_PATH), f"{TARGET_PATH} does not exist"
    content = read(TARGET_PATH)
    assert len(content) > 0, f"{TARGET_PATH} is empty"


# ── Property 2: File references all existing TSMC eval cases ─────────────


def test_references_all_tsmc_eval_cases():
    """
    Property: The distillation file must reference all three existing
    TSMC eval cases (dcf, time-horizon, customer-concentration).
    """
    content = read(TARGET_PATH)
    for case_path in TSMC_EVAL_CASES:
        # The case filename without extension should appear as a cross-reference
        stem = Path(case_path).stem
        assert stem in content, f"Missing cross-reference to {stem} (from {case_path})"


# ── Property 3: Template section coverage ─────────────────────────────────


def test_contains_all_required_sections():
    """Property: The file must contain all required sections from the template."""
    content = read(TARGET_PATH)
    content_lower = content.lower()
    missing = []
    for section in REQUIRED_SECTIONS:
        if section.lower() not in content_lower:
            missing.append(section)
    assert not missing, f"Missing required sections: {missing}"


# ── Property 4: Cross-references to existing eval case files ──────────────


def test_cross_references_to_existing_eval_cases_are_valid():
    """
    Property: Every cross-reference to an evals/cases/ path must point
    to an existing file.
    """
    content = read(TARGET_PATH)
    refs = re.findall(r'`?(evals/cases/[^`\s)]+)`?', content)
    for ref in refs:
        clean_ref = ref.strip("()`")
        assert file_exists(clean_ref), f"Cross-reference target {clean_ref} does not exist"


# ── Property 5: References to related issues ──────────────────────────────


def test_references_issues_276_to_280():
    """Property: The file must reference issues #276-#280 (the related closed issues)."""
    content = read(TARGET_PATH)
    for issue_ref in REFERENCED_ISSUES:
        assert issue_ref in content, f"Missing reference to {issue_ref}"


# ── Property 6: Markdown integrity ────────────────────────────────────────


def test_markdown_code_blocks_balanced():
    """Property: No unclosed triple-backtick code blocks."""
    content = read(TARGET_PATH)
    count = content.count("```")
    assert count % 2 == 0, f"Unbalanced code blocks ({count} backtick fences)"


def test_checklist_syntax_consistent():
    """Property: All checklist items use '- [ ]' or '- [x]' format."""
    content = read(TARGET_PATH)
    lines = content.split("\n")
    bad_lines = []
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("- [") and not stripped.startswith("- [ ]") and not stripped.startswith("- [x]"):
            bad_lines.append(f"  Line {i}: {stripped[:60]}")
    assert not bad_lines, f"Non-standard checklist syntax:\n" + "\n".join(bad_lines)


# ── Property 7: Each dimension has required internal structure ────────────


def test_each_dimension_has_required_subsections():
    """
    Property: Each dimension entry must contain all required subsections:
    Report A, Report B, Gap, Current status, Action type.
    """
    content = read(TARGET_PATH)
    for i in range(1, 7):
        # Find the dimension section boundary
        dim_start = re.search(rf"## Dimension {i}:", content)
        dim_end = re.search(rf"## Dimension {i + 1}:", content) if i < 6 else re.search(r"\n## Candidate-action summary", content)
        assert dim_start, f"Dimension {i} section not found"
        if dim_end:
            dim_text = content[dim_start.end():dim_end.start()]
        else:
            dim_text = content[dim_start.end():]

        missing = []
        for subsection in DIMENSION_SUBSECTIONS:
            # Each subsection should be bolded as heading or strong emphasis
            if subsection not in dim_text:
                missing.append(subsection)
        assert not missing, f"Dimension {i} missing subsections: {missing}"


# ── Property 8: All action types are valid template values ────────────────


def test_all_action_types_are_valid():
    """
    Property: Every 'Action type' value in the file must be one of the
    valid values defined in the comparative-distillation template.
    """
    content = read(TARGET_PATH)
    # Find lines like "- `NO_ACTION`" or "`NO_ACTION`" in action type contexts
    action_type_refs = set()
    for match in re.finditer(r'Action type\s*\n\s*(?:`NO_ACTION`|`NEW_RULE`|`CHECKLIST_HARDENING`|`TEMPLATE_CHANGE`)', content):
        # Extract the action type value (the last backtick-delimited word)
        types_found = re.findall(r'`(NO_ACTION|NEW_RULE|CHECKLIST_HARDENING|TEMPLATE_CHANGE)`', match.group())
        action_type_refs.update(types_found)
    # Also find action types in the candidate-action summary table
    for match in re.finditer(r'`(NO_ACTION|NEW_RULE|CHECKLIST_HARDENING|TEMPLATE_CHANGE)`', content):
        action_type_refs.add(match.group(1))
    assert len(action_type_refs) > 0, "No action type values found"
    for at in action_type_refs:
        assert at in VALID_ACTION_TYPES, f"Invalid action type '{at}'"


# ── Property 9: Gap coverage is complete ──────────────────────────────────


def test_gap_coverage_complete():
    """
    Property: The file must document which issue covers which gap.
    At minimum, must mention all of:
    - DCF/sensitivity (#278)
    - Time horizon stratification (#277)
    - Customer concentration (#280)
    - Capital return / FCF conversion (#279)
    - Source traceability / self-assessment (#276)
    """
    content = read(TARGET_PATH)
    required_keywords = [
        "dcf",
        "sensitivity",
        "time horizon",
        "customer concentration",
        "capital return",
        "source traceability",
        "self-assessment",
    ]
    missing = [kw for kw in required_keywords if kw not in content.lower()]
    assert not missing, f"Missing coverage of key topics: {missing}"


# ── Property 10: Source comparison is present ──────────────────────────────


def test_source_comparison_present():
    """
    Property: The file must compare GPT deep research vs local
    deep-research-skill reports.
    """
    content = read(TARGET_PATH)
    mentions_gpt = "gpt" in content.lower()
    mentions_local = "local" in content.lower() or "deep-research-skill" in content.lower()
    assert mentions_gpt, "File must mention GPT deep research version for comparison"
    assert mentions_local, "File must mention local deep-research-skill version for comparison"


# ── Property 11: Final judgment structure ──────────────────────────────────


def _final_judgment_section(content: str) -> str:
    """Extract the text under '## Final judgment' heading."""
    match = re.search(r'## Final judgment\s*\n(.*?)(?=\n## |\Z)', content, re.DOTALL)
    return match.group(1) if match else ""


def test_final_judgment_contains_key_components():
    """Property: Final judgment must include required subsections from template."""
    content = read(TARGET_PATH)
    fjs = _final_judgment_section(content)
    assert fjs, "Could not find '## Final judgment' section"
    required_items = [
        "stronger report did better",
        "should change",
        "should wait",
        "missing rule",
        "missing trigger",
        "execution",
    ]
    fjs_lower = fjs.lower()
    missing = [item for item in required_items if item not in fjs_lower]
    assert not missing, f"Final judgment section missing: {missing}"
