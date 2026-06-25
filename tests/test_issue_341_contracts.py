#!/usr/bin/env python3
"""
Property-based contract tests for Issue #341: Source Strength Gate.

Tests validate four new validator checks:
1. Wikipedia ratio in Source Register (100% → hard-fail, >50% → warning)
2. Claims Supported semantics (section-only → hard-fail, partial → warning)
3. CROWDSOURCED + high reliability mismatch → error
4. Enhanced CROWDSOURCED label consistency with reliability calibration

Usage:
    python tests/test_issue_341_contracts.py
    python -m pytest tests/test_issue_341_contracts.py -v

Expected BEFORE implementation: ALL RED (functions don't exist)
Expected AFTER implementation:  ALL GREEN
"""

from __future__ import annotations

import os
import re
import sys
import textwrap

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO_ROOT, "scripts"))


# ═══════════════════════════════════════════════════════════════════════════
# Test fixture builders — construct report markdown with various
# Source Register configurations to exercise the new checks.
# ═══════════════════════════════════════════════════════════════════════════

_FIXTURE_BASE = textwrap.dedent("""\
    # Test Report

    Some body text with citations [S01][S02][S03][S04].

    ## Route and audit status

    | Audit | Status | 证据 |
    |-------|--------|------|
    | source-traceability | ✅ Passed | §1 |

    ## Source Register

""")


def _build_register(source_rows: list[tuple[str, str, str, str]]) -> str:
    """Build a full report from source register rows.

    Each row: (id, source_name, source_type, reliability)
    claims_supported is auto-generated as '§1' unless overridden.
    """
    header = (
        "| ID | Source Name | Source Type | Date | DOI/URL "
        "| Reliability | Claims Supported |\n"
        "|----|-------------|-------------|------|--------"
        "|-------------|-----------------|\n"
    )
    rows = []
    for i, (sid, name, stype, rel) in enumerate(source_rows):
        claims = "§1"  # default: section-only (to test detection)
        rows.append(
            f"| {sid} | {name} | {stype} | 2025-01-01 | https://example.com/{i} "
            f"| {rel} | {claims} |"
        )
    return _FIXTURE_BASE + header + "\n".join(rows) + "\n"


def _report_wiki_100pct() -> str:
    """100% Wikipedia register — should trigger hard-fail."""
    report = textwrap.dedent("""\
        # Test Report

        ## Route and audit status

        **Primary route**: Technical Deep-dive

        | Audit | Status | 证据 |
        |-------|--------|------|
        | source-traceability | ✅ Passed | §Analysis: body has [S01]-[S04] |

        ## Analysis

        Some body text with citations [S01][S02][S03][S04].

        ## Source Register

        | ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
        |----|-------------|-------------|------|---------|-------------|-----------------|
        | S01 | Wikipedia: FIFA World Cup | CROWDSOURCED | 2025-01-01 | https://x.com/1 | high | §Analysis: tournament format rules |
        | S02 | Wikipedia: 2026 FIFA World Cup | Wikipedia | 2025-01-02 | https://x.com/2 | high | §Analysis: scheduling architecture |
        | S03 | Wikipedia: Group stage | wiki | 2025-01-03 | https://x.com/3 | high | §Analysis: third-place ranking criteria |
        | S04 | Wikipedia: Game theory | crowdsourced | 2025-01-04 | https://x.com/4 | high | §Analysis: information set theory |
    """)
    return report


def _report_wiki_50pct_load_bearing() -> str:
    """>50% Wikipedia among cited sources — should trigger warning."""
    return _build_register([
        ("S01", "Wikipedia: FIFA Rules", "CROWDSOURCED", "medium"),
        ("S02", "Wikipedia: World Cup History", "Wikipedia", "medium"),
        ("S03", "FIFA Official Rules PDF", "PRIMARY_INSTITUTION", "high"),
    ])


def _report_wiki_background_only() -> str:
    """Wikipedia used only for uncited background — should pass."""
    return _build_register([
        ("S01", "FIFA Official Rules", "PRIMARY_INSTITUTION", "high"),
        ("S02", "UEFA Press Release", "PRIMARY_INSTITUTION", "high"),
        ("S03", "Wikipedia: Background", "CROWDSOURCED", "medium"),
        # S03 not cited in body (body only has [S01][S02])
    ])


def _report_all_section_only_claims() -> str:
    """All Claims Supported are pure section numbers — should trigger hard-fail."""
    header = (
        "| ID | Source Name | Source Type | Date | DOI/URL "
        "| Reliability | Claims Supported |\n"
        "|----|-------------|-------------|------|--------"
        "|-------------|-----------------|\n"
    )
    rows = [
        "| S01 | FIFA Rules | PRIMARY_INSTITUTION | 2025-01-01 | https://x.com/1 | high | §1.1, §2.1 |",
        "| S02 | UEFA Doc | PRIMARY_INSTITUTION | 2025-01-02 | https://x.com/2 | high | §3.1 |",
        "| S03 | Game Theory Textbook | PRIMARY_FILING | 2025-01-03 | https://x.com/3 | high | §4.1, §4.2 |",
    ]
    return _FIXTURE_BASE + header + "\n".join(rows) + "\n"


def _report_mixed_claims() -> str:
    """Mixed: some claim-level, some section-only — should trigger warning."""
    header = (
        "| ID | Source Name | Source Type | Date | DOI/URL "
        "| Reliability | Claims Supported |\n"
        "|----|-------------|-------------|------|--------"
        "|-------------|-----------------|\n"
    )
    rows = [
        "| S01 | FIFA Rules | PRIMARY_INSTITUTION | 2025-01-01 | https://x.com/1 | high | §1.1: 2026 R32 对阵中 A1/B1 等组第一对阵最佳第三 |",
        "| S02 | UEFA Doc | PRIMARY_INSTITUTION | 2025-01-02 | https://x.com/2 | high | §3.1 |",
        "| S03 | History Stats | SECONDARY_MEDIA | 2025-01-03 | https://x.com/3 | medium | §4.1 |",
    ]
    return _FIXTURE_BASE + header + "\n".join(rows) + "\n"


def _report_claims_with_rich_text() -> str:
    """All claims have claim-level descriptions — should pass."""
    header = (
        "| ID | Source Name | Source Type | Date | DOI/URL "
        "| Reliability | Claims Supported |\n"
        "|----|-------------|-------------|------|--------"
        "|-------------|-----------------|\n"
    )
    rows = [
        "| S01 | FIFA Rules | PRIMARY_INSTITUTION | 2025-01-01 | https://x.com/1 | high | §1.1: 2026 R32 对阵中组第一对阵最佳第三；§2.1: 第三名排名规则 |",
        "| S02 | UEFA Doc | PRIMARY_INSTITUTION | 2025-01-02 | https://x.com/2 | high | §3.1: 欧足联赛程争议分析 |",
    ]
    return _FIXTURE_BASE + header + "\n".join(rows) + "\n"


def _report_crowdsourced_high_reliability() -> str:
    """CROWDSOURCED sources with high reliability — should trigger error."""
    return _build_register([
        ("S01", "Wikipedia: FIFA Rules", "CROWDSOURCED", "high"),
        ("S02", "FIFA Official", "PRIMARY_INSTITUTION", "high"),
    ])


def _report_crowdsourced_valid_reliability() -> str:
    """CROWDSOURCED sources with medium/low reliability — should pass."""
    return _build_register([
        ("S01", "Wikipedia: FIFA Rules", "CROWDSOURCED", "medium"),
        ("S02", "FIFA Official", "PRIMARY_INSTITUTION", "high"),
    ])


def _report_crowdsourced_with_confirmed_label() -> str:
    """CROWDSOURCED source referenced with confirmed label + high reliability."""
    body = textwrap.dedent("""\
        # Test Report

        Some body text [S01]. More text [确认事实][S01].

        ## Route and audit status

        | Audit | Status | 证据 |
        |-------|--------|------|
        | source-traceability | ✅ Passed | §1 |

        ## Source Register

    """)
    header = (
        "| ID | Source Name | Source Type | Date | DOI/URL "
        "| Reliability | Claims Supported |\n"
        "|----|-------------|-------------|------|--------"
        "|-------------|-----------------|\n"
    )
    rows = [
        "| S01 | Wikipedia: Something | CROWDSOURCED | 2025-01-01 | https://x.com/1 | high | §1 |",
    ]
    return body + header + "\n".join(rows) + "\n"


def _report_zero_wikipedia() -> str:
    """Zero Wikipedia sources, proper claims, matching body refs — should pass."""
    report = textwrap.dedent("""\
        # Test Report

        ## Route and audit status

        **Primary route**: Technical Deep-dive

        | Audit | Status | 证据 |
        |-------|--------|------|
        | source-traceability | ✅ Passed | §Analysis: body has [S01]-[S03] |

        ## Analysis

        Body text with citations [S01][S02][S03].

        ## Source Register

        | ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
        |----|-------------|-------------|------|---------|-------------|-----------------|
        | S01 | FIFA Official Rules | PRIMARY_INSTITUTION | 2025-01-01 | https://x.com/1 | high | §Analysis: FIFA tournament regulations |
        | S02 | UEFA Press Release | PRIMARY_INSTITUTION | 2025-01-02 | https://x.com/2 | high | §Analysis: scheduling policy statement |
        | S03 | Game Theory Textbook | PRIMARY_FILING | 2025-01-03 | https://x.com/3 | high | §Analysis: von Neumann theory foundations |
    """)
    return report


# ═══════════════════════════════════════════════════════════════════════════
# Helper: import validator functions (they don't exist yet → RED)
# ═══════════════════════════════════════════════════════════════════════════

def _import_functions():
    """Try to import the 3 new functions. Raise if not found."""
    from validate_report_quality import (
        check_source_register_wikipedia_ratio,
        check_claims_supported_semantics,
        check_source_register_reliability_crowdsourced,
    )
    return (
        check_source_register_wikipedia_ratio,
        check_claims_supported_semantics,
        check_source_register_reliability_crowdsourced,
    )


def _import_label_consistency():
    """Import the enhanced CROWDSOURCED calibration from label consistency."""
    from validate_source_label_consistency import check_source_consistency
    return check_source_consistency


# ═══════════════════════════════════════════════════════════════════════════
# Contract tests: Wikipedia ratio
# ═══════════════════════════════════════════════════════════════════════════

class TestWikipediaRatio:
    """Contract: check_source_register_wikipedia_ratio(cleaned_text)
       -> tuple[list[str], list[str]]  (errors, warnings)"""

    def test_100pct_wikipedia_triggers_blocking_error(self):
        """100% of cited sources are Wikipedia → BLOCKING error in errors list."""
        check, _, _ = _import_functions()
        text = _report_wiki_100pct()
        errors, warnings = check(text)
        assert len(errors) > 0, (
            f"Expected BLOCKING errors for 100% Wikipedia register, got errors={errors}"
        )
        assert len(warnings) == 0, (
            f"100% Wikipedia should be error not warning: warnings={warnings}"
        )
        # At least one error should mention Wikipedia
        wiki_mentioned = any("wikipedia" in e.lower() or "crowdsourced" in e.lower()
                             for e in errors)
        assert wiki_mentioned, (
            f"Errors should mention Wikipedia/CROWDSOURCED: {errors}"
        )

    def test_gt50pct_wikipedia_triggers_warning(self):
        """>50% of cited sources are Wikipedia → warning, not error."""
        check, _, _ = _import_functions()
        text = _report_wiki_50pct_load_bearing()
        errors, warnings = check(text)
        assert len(errors) == 0, (
            f"Expected no errors for 67% Wikipedia, got: {errors}"
        )
        assert len(warnings) > 0, (
            f"Expected warnings for >50% Wikipedia, got: {warnings}"
        )

    def test_zero_wikipedia_passes_cleanly(self):
        """Zero Wikipedia sources → both lists empty."""
        check, _, _ = _import_functions()
        text = _report_zero_wikipedia()
        errors, warnings = check(text)
        assert len(errors) == 0, (
            f"Expected no errors for zero-Wikipedia register, got: {errors}"
        )
        assert len(warnings) == 0, (
            f"Expected no warnings for zero-Wikipedia register, got: {warnings}"
        )

    def test_no_source_register_returns_empty(self):
        """No Source Register section → empty tuple (no crash)."""
        check, _, _ = _import_functions()
        text = "# Just a report\n\nNo register here.\n"
        errors, warnings = check(text)
        assert len(errors) == 0
        assert len(warnings) == 0


# ═══════════════════════════════════════════════════════════════════════════
# Contract tests: Claims Supported semantics
# ═══════════════════════════════════════════════════════════════════════════

class TestClaimsSupportedSemantics:
    """Contract: check_claims_supported_semantics(cleaned_text)
       -> tuple[list[str], list[str]]  (errors, warnings)"""

    def test_all_section_only_triggers_error(self):
        """All Claims Supported are pure section numbers → BLOCKING error."""
        _, check, _ = _import_functions()
        text = _report_all_section_only_claims()
        errors, warnings = check(text)
        assert len(errors) > 0, (
            f"Expected errors for all-section-only, got errors={errors}"
        )
        assert len(warnings) == 0, (
            f"All-section-only should be error not warning: warnings={warnings}"
        )

    def test_all_claim_level_passes_cleanly(self):
        """All Claims Supported have claim descriptions → both lists empty."""
        _, check, _ = _import_functions()
        text = _report_claims_with_rich_text()
        errors, warnings = check(text)
        assert len(errors) == 0, f"Expected no errors: {errors}"
        assert len(warnings) == 0, f"Expected no warnings: {warnings}"

    def test_mixed_claims_triggers_warning(self):
        """Mixed section-only + claim-level → warning, NOT error."""
        _, check, _ = _import_functions()
        text = _report_mixed_claims()
        errors, warnings = check(text)
        assert len(errors) == 0, (
            f"Mixed claims should NOT be blocking errors: {errors}"
        )
        assert len(warnings) > 0, (
            f"Expected warnings for mixed Claims Supported, got: {warnings}"
        )

    def test_no_source_register_returns_empty(self):
        """No Source Register → both lists empty, no crash."""
        _, check, _ = _import_functions()
        text = "# Just a report\n"
        errors, warnings = check(text)
        assert len(errors) == 0
        assert len(warnings) == 0


# ═══════════════════════════════════════════════════════════════════════════
# Contract tests: CROWDSOURCED reliability calibration
# ═══════════════════════════════════════════════════════════════════════════

class TestCrowdsourcedReliability:
    """Contract: check_source_register_reliability_crowdsourced(cleaned_text) -> list[str]"""

    def test_crowdsourced_high_reliability_triggers_error(self):
        """CROWDSOURCED + high reliability → BLOCKING error."""
        _, _, check = _import_functions()
        text = _report_crowdsourced_high_reliability()
        errors = check(text)
        assert len(errors) > 0, (
            f"Expected errors for CROWDSOURCED+high reliability, got: {errors}"
        )
        # Error should mention both CROWDSOURCED and high
        has_crowd = any("crowdsourced" in e.lower() or "wikipedia" in e.lower()
                        for e in errors)
        has_high = any("high" in e.lower() for e in errors)
        assert has_crowd and has_high, (
            f"Error should mention CROWDSOURCED and 'high' reliability: {errors}"
        )

    def test_crowdsourced_valid_reliability_passes(self):
        """CROWDSOURCED + medium/low → passes cleanly."""
        _, _, check = _import_functions()
        text = _report_crowdsourced_valid_reliability()
        errors = check(text)
        assert len(errors) == 0, (
            f"Expected no errors for CROWDSOURCED+medium, got: {errors}"
        )

    def test_no_source_register_returns_empty(self):
        """No register → empty list."""
        _, _, check = _import_functions()
        text = "# No register\n"
        errors = check(text)
        assert len(errors) == 0


# ═══════════════════════════════════════════════════════════════════════════
# Contract tests: Enhanced label consistency (CROWDSOURCED + reliability)
# ═══════════════════════════════════════════════════════════════════════════

class TestCrowdsourcedLabelConsistencyEnhanced:
    """Contract: Cross-function checks for CROWDSOURCED sources."""

    def test_crowdsourced_confirmed_label_still_caught(self):
        """Existing behavior (validate_source_label_consistency):
        CROWDSOURCED + [确认事实] → error."""
        check = _import_label_consistency()
        text = _report_crowdsourced_with_confirmed_label()
        errors = check(text)
        assert len(errors) > 0, (
            f"Expected errors for CROWDSOURCED+confirmed label, got: {errors}"
        )

    def test_crowdsourced_high_reliability_in_register(self):
        """NEW (validate_report_quality): CROWDSOURCED + high reliability → error."""
        _, _, check = _import_functions()
        text = _report_crowdsourced_high_reliability()
        errors = check(text)
        assert len(errors) > 0, (
            f"Expected errors for CROWDSOURCED+high reliability, got: {errors}"
        )


# ═══════════════════════════════════════════════════════════════════════════
# Integration: validate_report_quality wraps new checks
# ═══════════════════════════════════════════════════════════════════════════

class TestIntegrationInValidateReportQuality:
    """The 3 new checks are wired into validate_report_quality's main flow."""

    def test_wikipedia_100pct_causes_quality_failure(self):
        """validate_file on 100% Wikipedia report → exit code 2."""
        from validate_report_quality import validate_file
        from pathlib import Path

        # Write fixture to temp file
        import tempfile
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as f:
            f.write(_report_wiki_100pct())
            tmp_path = Path(f.name)

        try:
            exit_code = validate_file(tmp_path)
            assert exit_code == 2, (
                f"Expected exit code 2 for 100% Wikipedia report, got {exit_code}"
            )
        finally:
            os.unlink(str(tmp_path))

    def test_clean_report_passes(self):
        """validate_file on a clean report → exit code 0."""
        from validate_report_quality import validate_file
        from pathlib import Path

        import tempfile
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as f:
            f.write(_report_zero_wikipedia())
            tmp_path = Path(f.name)

        try:
            exit_code = validate_file(tmp_path)
            assert exit_code == 0, (
                f"Expected exit code 0 for clean report, got {exit_code}"
            )
        finally:
            os.unlink(str(tmp_path))


# ═══════════════════════════════════════════════════════════════════════════
# Property-based invariants (generative contract)
# ═══════════════════════════════════════════════════════════════════════════

class TestPropertyInvariants:
    """Property-based invariants that must hold for all inputs."""

    def test_no_function_crashes_on_malformed_input(self):
        """All 3 functions must handle None-like/malformed input without crashing."""
        check_wiki, check_claims, check_reli = _import_functions()

        # Empty string — wiki and claims return tuple, reli returns list
        result = check_reli("")
        assert isinstance(result, list), f"check_reli('') did not return list"

        errors, warnings = check_wiki("")
        assert isinstance(errors, list) and isinstance(warnings, list)

        errors, warnings = check_claims("")
        assert isinstance(errors, list) and isinstance(warnings, list)

        # Whitespace only
        result = check_reli("   \n\n   ")
        assert isinstance(result, list)

        errors, warnings = check_wiki("   \n\n   ")
        assert isinstance(errors, list) and isinstance(warnings, list)

        errors, warnings = check_claims("   \n\n   ")
        assert isinstance(errors, list) and isinstance(warnings, list)

        # Very long text without register
        long_text = "x" * 100000
        result = check_reli(long_text)
        assert isinstance(result, list)

        errors, warnings = check_wiki(long_text)
        assert isinstance(errors, list) and isinstance(warnings, list)

        errors, warnings = check_claims(long_text)
        assert isinstance(errors, list) and isinstance(warnings, list)

    def test_all_functions_return_list_of_strings(self):
        """Contract: every check function returns list[str] (or tuple of list[str])."""
        check_wiki, check_claims, check_reli = _import_functions()

        # check_reli returns simple list
        result = check_reli(_report_zero_wikipedia())
        assert isinstance(result, list)
        for item in result:
            assert isinstance(item, str)

        # Wikipedia and claims functions return tuples
        for name, fn in [("wikipedia_ratio", check_wiki), ("claims_supported", check_claims)]:
            result = fn(_report_zero_wikipedia())
            assert isinstance(result, tuple), f"{name} returned {type(result)}, expected tuple"
            assert len(result) == 2, f"{name} returned {len(result)}-tuple, expected 2"
            errors, warnings = result
            assert isinstance(errors, list), f"{name} errors not a list: {type(errors)}"
            assert isinstance(warnings, list), f"{name} warnings not a list: {type(warnings)}"

    def test_idempotent(self):
        """Same input → same output (no side effects, no randomness)."""
        check_wiki, check_claims, check_reli = _import_functions()
        text = _report_wiki_100pct()

        # reli returns simple list
        r1 = check_reli(text)
        r2 = check_reli(text)
        assert r1 == r2, f"reliability_crowd not idempotent: {r1} != {r2}"

        # wiki and claims return tuples
        for name, fn in [("wikipedia_ratio", check_wiki), ("claims_supported", check_claims)]:
            e1, w1 = fn(text)
            e2, w2 = fn(text)
            assert e1 == e2, f"{name} errors not idempotent: {e1} != {e2}"
            assert w1 == w2, f"{name} warnings not idempotent: {w1} != {w2}"


# ═══════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-v", "--tb=short"]))
