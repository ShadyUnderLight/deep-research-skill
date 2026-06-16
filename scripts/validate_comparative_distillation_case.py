#!/usr/bin/env python3
"""Contract model and validator for comparative-distillation case files.

Defines the data model for a comparative-distillation case and provides
validation functions that check any .md file in evals/comparative-distillation/
against the template contract defined in evals/templates/comparative-distillation-template.md.

Usage:
    python scripts/validate_comparative_distillation_case.py <path_to_case.md>
    python scripts/validate_comparative_distillation_case.py --all  # validate all cases
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator, Literal

# ── Type contracts ──────────────────────────────────────────────────────────

ActionType = Literal["NEW_RULE", "CHECKLIST_HARDENING", "TEMPLATE_CHANGE", "NO_ACTION"]
VALID_ACTION_TYPES: tuple[str, ...] = ("NEW_RULE", "CHECKLIST_HARDENING", "TEMPLATE_CHANGE", "NO_ACTION")

VALID_DIMENSIONS: tuple[str, ...] = (
    "Current-state discipline",
    "Numerical and date discipline",
    "Source traceability and evidence weighting",
    "Forward-looking claim discipline",
    "Structural readability and information density",
    "Decision usefulness",
)

# Required sections in the standard order
REQUIRED_SECTIONS: tuple[str, ...] = (
    "Case identity",
    "Comparison purpose",
    "Dimension 1: Current-state discipline",
    "Dimension 2: Numerical and date discipline",
    "Dimension 3: Source traceability and evidence weighting",
    "Dimension 4: Forward-looking claim discipline",
    "Dimension 5: Structural readability and information density",
    "Dimension 6: Decision usefulness",
)


# ── Data model ──────────────────────────────────────────────────────────────


@dataclass
class CaseIdentity:
    """Case identity block fields."""
    case_name: str
    date: str
    research_question: str
    why_matters: str
    report_a: str
    report_b: str
    stronger_report: str | None = None
    prompt: str | None = None
    scope_diff: str | None = None


@dataclass
class DimensionComparison:
    """One dimension in the comparison."""
    dimension_name: str
    report_a: list[str] = field(default_factory=list)
    report_b: list[str] = field(default_factory=list)
    gap: list[str] = field(default_factory=list)
    candidate_action: list[str] = field(default_factory=list)
    action_type: ActionType | str | None = None


@dataclass
class ComparativeDistillationCase:
    """Full model for a comparative-distillation case file."""
    title: str
    identity: CaseIdentity
    comparison_purpose: str
    dimensions: list[DimensionComparison]
    candidate_summary: list[dict[str, str]] = field(default_factory=list)
    triage_notes: list[dict[str, str]] = field(default_factory=list)
    rejected_observations: list[dict[str, str]] = field(default_factory=list)
    final_judgment: list[str] = field(default_factory=list)
    quality_checklist: dict[str, bool] = field(default_factory=dict)

    # Path tracking for validation context
    source_path: Path | None = None


# ── Section extraction helpers ──────────────────────────────────────────────


def _strip_fenced_code(text: str) -> str:
    """Remove fenced code blocks (```...```) to avoid matching inside them."""
    return re.sub(r"```.*?```", "", text, flags=re.DOTALL)


def extract_section_blocks(text: str) -> dict[str, str]:
    """Extract top-level ## sections from markdown text.

    Returns dict of {section_title: section_body}.
    Fenced code blocks (```...```) are excluded to avoid phantom section headers.
    """
    clean = _strip_fenced_code(text)
    blocks: dict[str, str] = {}
    # Match ##-level headers (not ### or ####) on the code-stripped text
    pattern = re.compile(r"^## (.+)$", re.MULTILINE)
    matches = list(pattern.finditer(clean))
    for i, match in enumerate(matches):
        title = match.group(1).strip()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(clean)
        body = clean[start:end].strip()
        blocks[title] = body
    return blocks


def extract_list_items(section_body: str, sub_header: str) -> list[str]:
    """Extract bullet items under a given ### sub-header within a section body."""
    # Find the sub-header
    pattern = re.compile(rf"^### {re.escape(sub_header)}\s*$", re.MULTILINE)
    match = pattern.search(section_body)
    if not match:
        return []
    # Collect lines after the header until next ### or end
    after = section_body[match.end():]
    next_header = re.search(r"^### ", after, re.MULTILINE)
    if next_header:
        after = after[:next_header.start()]
    # Extract bullet items
    items = re.findall(r"^- (.+)", after, re.MULTILINE)
    return [item.strip() for item in items]


def extract_action_type(section_body: str) -> str | None:
    """Extract the action-type backtick value (e.g. `NO_ACTION`).

    Searches for the action type within the ### Candidate action and
    ### Action type subsections, preferring ### Action type if present.
    This avoids matching action-type tokens in narrative text elsewhere
    (e.g. in dimension comparison prose).
    """
    # Strategy: find the text spanning from ### Candidate action through
    # the immediately following ### Action type (if present), up to the
    # next ### or end of section. Search for the backtick value there.
    ca_match = re.search(r"^### Candidate action\s*$", section_body, re.MULTILINE)
    if not ca_match:
        return None
    after_ca = section_body[ca_match.end():]
    # Extend through any ### Action type subsection
    at_match = re.search(r"^### Action type\s*$", after_ca, re.MULTILINE)
    if at_match:
        # Start from content after ### Action type heading
        scope = after_ca[at_match.end():]
    else:
        scope = after_ca
    # Limit to until next ### or end
    next_header = re.search(r"^### ", scope, re.MULTILINE)
    if next_header:
        scope = scope[:next_header.start()]
    m = re.search(r"`(NEW_RULE|CHECKLIST_HARDENING|TEMPLATE_CHANGE|NO_ACTION)`", scope)
    return m.group(1) if m else None


# ── Validation ──────────────────────────────────────────────────────────────


@dataclass
class ValidationResult:
    """Result of validating one case file."""
    path: str
    passed: bool = True
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


class ContractValidator:
    """Validates a comparative-distillation case file against the template contract."""

    def __init__(self, strict: bool = False) -> None:
        self.strict = strict

    def validate(self, filepath: Path) -> ValidationResult:
        """Run all contract checks on a case file."""
        result = ValidationResult(path=str(filepath))
        try:
            text = filepath.read_text(encoding="utf-8")
        except Exception as e:
            result.passed = False
            result.errors.append(f"Cannot read file: {e}")
            return result

        blocks = extract_section_blocks(text)

        # ── P0: Title ──
        first_line = text.splitlines()[0] if text.splitlines() else ""
        if not first_line.startswith("# "):
            result.warnings.append("P0: File does not start with a level-1 heading (# Title)")

        # ── P1: Required sections present ──
        for section in REQUIRED_SECTIONS:
            if section not in blocks:
                result.errors.append(f"P1: Missing required section '## {section}'")

        # ── P2: Section ordering ──
        section_order = [s for s in blocks if s.startswith(("Dimension ", "Case identity", "Comparison purpose"))]
        expected_prefix_order = [
            "Case identity",
            "Comparison purpose",
            "Dimension 1", "Dimension 2", "Dimension 3",
            "Dimension 4", "Dimension 5", "Dimension 6",
        ]
        actual_prefixes = [s.split(":")[0].strip() if ":" in s else s for s in section_order]
        for i, expected in enumerate(expected_prefix_order):
            if i >= len(actual_prefixes):
                result.errors.append(f"P2: Section order broken — expected '{expected}' at position {i+1}, got end of sections")
                break
            if not actual_prefixes[i].startswith(expected.split(":")[0] if ":" in expected else expected):
                result.errors.append(f"P2: Section order — position {i+1} expected '{expected}', got '{actual_prefixes[i]}'")
                break

        # ── P3: Each dimension has required sub-sections ──
        for dim_name in VALID_DIMENSIONS:
            dim_key = None
            for key in blocks:
                if dim_name in key:
                    dim_key = key
                    break
            if dim_key is None:
                result.warnings.append(f"P3: Could not find dimension section containing '{dim_name}'")
                continue
            body = blocks[dim_key]
            for sub in ("Report A", "Report B", "Gap"):
                items = extract_list_items(body, sub)
                if not items:
                    result.warnings.append(f"P3: Dimension '{dim_name}' is missing bullet items under '### {sub}'")

            # Action type
            action_type = extract_action_type(body)
            if action_type is None:
                result.warnings.append(f"P3: Dimension '{dim_name}' has no action type (`NEW_RULE`/etc.)")
            elif self.strict and action_type not in VALID_ACTION_TYPES:
                result.errors.append(f"P3: Dimension '{dim_name}' has invalid action type '{action_type}'")

        # ── P4: Candidate-action summary table ──
        if "Candidate-action summary" in blocks:
            body = blocks["Candidate-action summary"]
            if "| # | Candidate action" not in body:
                result.warnings.append("P4: Candidate-action summary table missing header row")
        else:
            result.warnings.append("P4: Missing '## Candidate-action summary' section")

        # ── P5: Final judgment section ──
        has_judgment = any("Final judgment" in key for key in blocks)
        if not has_judgment:
            result.warnings.append("P5: Missing '## Final judgment' section")

        # ── P6: No `turn...` references ──
        turn_refs = re.findall(r"turn\d+", text, re.IGNORECASE)
        if turn_refs:
            result.errors.append(f"P6: File contains {len(turn_refs)} `turn...` reference(s): {turn_refs[:5]}")

        # ── P7: No raw \ue000 placeholders ──
        if re.search(r"[\ue000\ue001]", text):
            result.errors.append("P7: File contains raw \\ue000/\\ue001 placeholder characters")

        result.passed = len(result.errors) == 0
        return result


# ── Batch validation ────────────────────────────────────────────────────────


def find_all_cases(root: Path) -> list[Path]:
    """Find all comparative-distillation case files in the repo."""
    pattern = "evals/comparative-distillation/*.md"
    # Exclude known non-case files
    excluded = {"candidate-rule-registry.md"}
    paths = sorted(root.glob(pattern))
    return [p for p in paths if p.name not in excluded]


def validate_all(validator: ContractValidator | None = None) -> list[ValidationResult]:
    """Validate all comparative-distillation cases in the repo."""
    root = Path(__file__).resolve().parents[1]
    if validator is None:
        validator = ContractValidator(strict=False)
    results: list[ValidationResult] = []
    for path in find_all_cases(root):
        results.append(validator.validate(path))
    return results


# ── CLI entry point ─────────────────────────────────────────────────────────


def _argv_without_flags() -> list[str]:
    """Return positional args, stripping --flag options."""
    return [a for a in sys.argv[1:] if not a.startswith("--")]


def main() -> int:
    """Run validation and print results."""
    validator = ContractValidator(strict="--strict" in sys.argv)
    has_positional = bool(_argv_without_flags())

    if "--help" in sys.argv:
        print("Usage:")
        print("  python scripts/validate_comparative_distillation_case.py [--strict] <path>")
        print("  python scripts/validate_comparative_distillation_case.py [--strict] --all")
        return 0

    if "--all" in sys.argv:
        results = validate_all(validator)
    elif has_positional:
        path = Path(_argv_without_flags()[0])
        if not path.exists():
            print(f"ERROR: File not found: {path}")
            return 1
        results = [validator.validate(path)]
    else:
        print("Usage:")
        print("  python scripts/validate_comparative_distillation_case.py [--strict] <path>")
        print("  python scripts/validate_comparative_distillation_case.py [--strict] --all")
        return 1

    exit_code = 0
    for r in results:
        status = "✅ PASS" if r.passed else "❌ FAIL"
        print(f"{status}  {r.path}")
        for e in r.errors:
            print(f"  ERROR:   {e}")
        for w in r.warnings:
            print(f"  WARNING: {w}")
        if not r.passed:
            exit_code = 1

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
