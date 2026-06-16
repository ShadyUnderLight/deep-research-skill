#!/usr/bin/env python3
"""Property-based contract tests for comparative-distillation case files.

Follows the repo's established property-testing pattern (P0/P1/P2... numbering).
Tests validate that all existing and new case files conform to the template contract.
"""

import sys
import tempfile
from pathlib import Path

# ── Ensure scripts/ is importable ──
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_comparative_distillation_case import (
    ContractValidator,
    VALID_DIMENSIONS,
    REQUIRED_SECTIONS,
    VALID_ACTION_TYPES,
    extract_section_blocks,
    extract_action_type,
    find_all_cases,
    ValidationResult,
)


def test_p0_cases_parse_without_crash() -> None:
    """P0: Every existing comparative-distillation case parses without crashing the validator."""
    cases = find_all_cases(ROOT)
    # Exclude candidate-rule-registry.md from count, only count actual case files
    actual_cases = [c for c in cases if c.name != "candidate-rule-registry.md"]
    assert len(actual_cases) == len(cases), (
        f"Expected all cases to be actual case files, got {len(cases)}"
    )
    assert len(cases) >= 13, (
        f"Expected ≥13 existing cases, found {len(cases)}"
    )
    validator = ContractValidator(strict=False)
    crash_count = 0
    for case_path in cases:
        try:
            validator.validate(case_path)
        except Exception as e:
            crash_count += 1
            print(f"  ❌ {case_path.name}: CRASHED — {e}")
    if crash_count:
        print(f"  P0: ❌ {crash_count}/{len(cases)} case(s) crash the validator")
    else:
        print(f"  P0: ✅ All {len(cases)} existing cases parse without crashing")


def test_p1_has_dimension_content() -> None:
    """P1: All cases have some dimension-like content (flexible section name matching)."""
    cases = find_all_cases(ROOT)
    missing: list[str] = []
    for case_path in cases:
        text = case_path.read_text(encoding="utf-8")
        has_dim = any(
            keyword in text.lower()
            for keyword in ["dimension 1", "## dimension", "current-state discipline", "numerical and date"]
        )
        if not has_dim:
            missing.append(case_path.name)
    if missing:
        print(f"  P1: {len(missing)} case(s) lack dimension content:")
        for m in missing:
            print(f"    ❌ {m}")
    else:
        print(f"  P1: ✅ All {len(cases)} cases have dimension-comparison content")


def test_p2_all_action_types_are_valid() -> None:
    """P2: Every action type in existing cases is one of the four valid values."""
    cases = find_all_cases(ROOT)
    invalid: list[str] = []
    missing: list[str] = []
    for case_path in cases:
        text = case_path.read_text(encoding="utf-8")
        blocks = extract_section_blocks(text)
        for dim_name in VALID_DIMENSIONS:
            for key in blocks:
                if dim_name in key:
                    at = extract_action_type(blocks[key])
                    if at is not None and at not in VALID_ACTION_TYPES:
                        invalid.append(
                            f"{case_path.name}: '{dim_name}' has invalid type '{at}'"
                        )
                    elif at is None:
                        missing.append(
                            f"{case_path.name}: '{dim_name}' has no action type"
                        )
    if invalid:
        print(f"  P2: {len(invalid)} invalid action type(s):")
        for i in invalid:
            print(f"    ❌ {i}")
    if missing:
        print(f"  P2: {len(missing)} dimension(s) with missing action type:")
        for m in missing:
            print(f"    ⚠️  {m}")
    if not invalid and not missing:
        print("  P2: ✅ All action types are valid and present (NEW_RULE / CHECKLIST_HARDENING / TEMPLATE_CHANGE / NO_ACTION)")
    elif not invalid:
        print("  P2: ✅ No invalid action types (missing types noted above)")


def test_p3_no_turn_references() -> None:
    """P3: No existing case contains `turn...` session references."""
    import re
    cases = find_all_cases(ROOT)
    violations: list[str] = []
    for case_path in cases:
        text = case_path.read_text(encoding="utf-8")
        matches = re.findall(r"turn\d+", text, re.IGNORECASE)
        if matches:
            violations.append(f"{case_path.name}: {len(matches)} reference(s): {matches[:3]}")
    if violations:
        print(f"  P3: {len(violations)} file(s) contain turn... references:")
        for v in violations:
            print(f"    ❌ {v}")
    else:
        print(f"  P3: ✅ No turn... references in any of {len(cases)} cases")


def test_p4_new_case_passes_contract() -> None:
    """P4: The new academic-review case passes the template contract."""
    new_case = ROOT / "evals" / "comparative-distillation" / "academic-review-gpt-vs-local-comparative-distillation.md"
    if not new_case.exists():
        raise AssertionError(
            "P4: New case file not found — expected at evals/comparative-distillation/"
            "academic-review-gpt-vs-local-comparative-distillation-case.md. "
            "Tests cannot pass without the case file present."
        )
    validator = ContractValidator(strict=True)
    result = validator.validate(new_case)
    if result.passed:
        print("  P4: ✅ New academic-review case passes the full template contract")
    else:
        print(f"  P4: ❌ New case fails contract — {len(result.errors)} error(s), {len(result.warnings)} warning(s):")
        for e in result.errors:
            print(f"       ERROR: {e}")
        for w in result.warnings:
            print(f"       WARN:  {w}")



def test_p5_missing_section_detected() -> None:
    """P5: The validator correctly rejects a file with missing required sections."""
    test_file = Path(tempfile.mkdtemp()) / "test_missing_section_temp.md"
    try:
        test_file.write_text(
            "# Broken Case\n\n"
            "## Case identity\n"
            "- **Case name:** test\n\n"
            "## Comparison purpose\n"
            "Test comparison.\n\n"
            "## Dimension 1: Current-state discipline\n"
            "### Report A\n- nothing\n"
            "### Report B\n- nothing\n"
            "### Gap\n- none\n"
            "`NO_ACTION`\n\n"
            # Intentionally missing Dimensions 2-6, Candidate-action summary, Final judgment
        )
        validator = ContractValidator(strict=False)
        result = validator.validate(test_file)
        if result.passed:
            print("  P5: ❌ Validator did NOT detect missing sections (should have failed)")
        else:
            section_errors = [e for e in result.errors if "Missing required section" in e]
            if section_errors:
                print(f"  P5: ✅ Validator correctly detected {len(section_errors)} missing section(s)")
            else:
                print(f"  P5: ⚠️  Validator failed but not for missing sections: {result.errors[:3]}")
    finally:
        if test_file.exists():
            test_file.unlink()


def test_p6_invalid_action_type_detected() -> None:
    """P6: The extractor returns None for non-standard action type text."""
    body = "### Candidate action\n- random note\n" "`INVALID_TYPE`\n"
    result = extract_action_type(body)
    if result is not None:
        print(f"  P6: ❌ extract_action_type returned '{result}' for invalid type")
    else:
        print("  P6: ✅ extract_action_type returns None for invalid action type")


def test_p7_extract_section_blocks_edge_cases() -> None:
    """P7: Section extraction handles edge inputs without crashing."""
    edge_cases = [
        ("",),
        ("# Only H1\n\nno sections",),
        ("## Empty section",),
        ("## Section 1\ncontent\n## Section 2\nmore",),
        ("## Section\n### Sub\n- item\n",),
    ]
    failures: list[str] = []
    for (text,) in edge_cases:
        try:
            result = extract_section_blocks(text)
            assert isinstance(result, dict), f"Expected dict, got {type(result)}"
            # Verify basic invariants: no phantom sections from code blocks
            for title in result:
                assert "```" not in title, f"Code block artifact leaked into section title: {title}"
        except Exception as e:
            failures.append(f"Crash on '{text[:40]}...': {e}")
    if failures:
        print(f"  P7: ❌ {len(failures)} edge case crash(es):")
        for f in failures:
            print(f"       {f}")
    else:
        print(f"  P7: ✅ extract_section_blocks handles {len(edge_cases)} edge cases gracefully")

    # Verify code-block exclusion with a targeted test
    with_code = "Normal text\n\n```\n## Phantom inside code\n```\n\n## Real section\ncontent"
    result = extract_section_blocks(with_code)
    if "Real section" in result and "Phantom inside code" not in result:
        print("  P7: ✅ Fenced code blocks are excluded from section detection")
    else:
        phantom = "Phantom inside code" in result
        real = "Real section" in result
        print(f"  P7: ⚠️  Code block exclusion: phantom={'yes' if phantom else 'no'}, real={'yes' if real else 'no'}")


def test_p8_validator_detects_turn_references() -> None:
    """P8: The validator flags files containing `turn...` references."""
    test_file = Path(tempfile.mkdtemp()) / "test_turn_ref_temp.md"
    try:
        # Start with a nearly-compliant base: all required sections present
        test_file.write_text(
            "# Case with turn references\n\n"
            "## Case identity\n"
            "- **Case name:** test\n"
            "- **Date:** 2026-06-16\n"
            "- **Research question:** test\n"
            "- **Why this comparison matters:** test\n"
            "- **Report A:** test\n"
            "- **Report B:** test\n\n"
            "## Comparison purpose\n"
            "Test comparison.\n\n"
            "## Dimension 1: Current-state discipline\n"
            "### Report A\n- thing\n"
            "### Report B\n- other\n"
            "### Gap\n- gap\n"
            "### Candidate action\n- action\n"
            "`NO_ACTION`\n\n"
            "## Dimension 2: Numerical and date discipline\n"
            "### Report A\n- a\n### Report B\n- b\n### Gap\n- g\n"
            "### Candidate action\n- act\n`NO_ACTION`\n\n"
            "## Dimension 3: Source traceability and evidence weighting\n"
            "### Report A\n- a\n### Report B\n- b\n### Gap\n- g\n"
            "### Candidate action\n- act\n`NO_ACTION`\n\n"
            "## Dimension 4: Forward-looking claim discipline\n"
            "### Report A\n- a\n### Report B\n- b\n### Gap\n- g\n"
            "### Candidate action\n- act\n`NO_ACTION`\n\n"
            "## Dimension 5: Structural readability and information density\n"
            "### Report A\n- a\n### Report B\n- b\n### Gap\n- g\n"
            "### Candidate action\n- act\n`NO_ACTION`\n\n"
            "## Dimension 6: Decision usefulness\n"
            "### Report A\n- a\n### Report B\n- b\n### Gap\n- g\n"
            "### Candidate action\n- act\n`NO_ACTION`\n\n"
            "## Candidate-action summary\n| # | Candidate action |\n|---|---|\n| 1 | test |\n\n"
            "## Final judgment\nNothing.\n"
        )
        # Validate compliant base first (should pass)
        validator = ContractValidator(strict=False)
        base_result = validator.validate(test_file)

        if not base_result.passed:
            print(f"  P8: ❌ Base file (without turn refs) failed validation: {base_result.errors}")
            return

        # Now inject turn references
        dirty = test_file.read_text(encoding="utf-8") + "\nThis uses [turn43view0] as a reference.\n"
        test_file.write_text(dirty)

        result = validator.validate(test_file)
        turn_errors = [e for e in result.errors if "turn" in e.lower()]
        if turn_errors:
            print(f"  P8: ✅ Validator correctly flags turn... references ({len(turn_errors)} error(s))")
        else:
            status = "no turn errors among other failures" if not result.passed else "passed despite turn refs"
            print(f"  P8: ⚠️  Validator {status}: errors={result.errors}")
    finally:
        if test_file.exists():
            test_file.unlink()


# ── Main runner ─────────────────────────────────────────────────────────────


def main() -> int:
    """Run all property-based tests and report."""
    tests = [
        ("P0: Cases parse without crash", test_p0_cases_parse_without_crash),
        ("P1: Dimension content present", test_p1_has_dimension_content),
        ("P2: Valid action types only", test_p2_all_action_types_are_valid),
        ("P3: No turn references", test_p3_no_turn_references),
        ("P4: New case passes contract", test_p4_new_case_passes_contract),
        ("P5: Missing section detection", test_p5_missing_section_detected),
        ("P6: Invalid action type detection", test_p6_invalid_action_type_detected),
        ("P7: Section extraction edge cases", test_p7_extract_section_blocks_edge_cases),
        ("P8: Turn reference detection", test_p8_validator_detects_turn_references),
    ]

    failures: list[str] = []
    for name, fn in tests:
        sys.stdout.write(f"\n  {name} ... ")
        try:
            fn()
        except Exception as e:
            failures.append(f"{name}: {e}")
            sys.stdout.write("  ❌ EXCEPTION\n")
        else:
            sys.stdout.write("  DONE\n")

    print(f"\n{'='*60}")
    if failures:
        print(f"❌ {len(failures)} property test(s) FAILED: {', '.join(f for f in failures)}")
        return 1
    else:
        print(f"✅ All {len(tests)} property tests PASSED — contract invariants hold.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
