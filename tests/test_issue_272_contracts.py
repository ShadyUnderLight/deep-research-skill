#!/usr/bin/env python3
"""
Property-based contract validation for issue #272.
Tests verify Chinese technical source type normalization and unknown type detection.

Usage:
    python tests/test_issue_272_contracts.py

Expected BEFORE implementation: ALL FAIL
Expected AFTER implementation:  ALL PASS
"""

import re
import sys
import os

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO_ROOT, 'scripts'))

from validate_source_label_consistency import (
    _normalize_source_type,
    _FREETEXT_TYPE_MAP,
    _FREETEXT_TYPE_MAP_CI,
    _is_unknown_type,
    _is_secondary_type,
    check_source_consistency,
)


def read(path):
    with open(os.path.join(REPO_ROOT, path), "r") as f:
        return f.read()


# ── D1: New functions exist ────────────────────────────────────────

def test_d1_imports_new_functions():
    """D1: _normalize_source_type, _FREETEXT_TYPE_MAP, _is_unknown_type must be importable."""
    assert callable(_normalize_source_type), "_normalize_source_type must be callable"
    assert isinstance(_FREETEXT_TYPE_MAP, dict), "_FREETEXT_TYPE_MAP must be a dict"
    assert isinstance(_FREETEXT_TYPE_MAP_CI, dict), "_FREETEXT_TYPE_MAP_CI must be a dict"
    assert callable(_is_unknown_type), "_is_unknown_type must be callable"


# ── D2: Normalization behaviour ────────────────────────────────────

def test_d2_normalize_strips_cjk_parens():
    """D2: '学术综述（arXiv）' maps to 'SECONDARY_MEDIA' (strip + lookup)."""
    result = _normalize_source_type("学术综述（arXiv）")
    assert result == "SECONDARY_MEDIA", f"Expected 'SECONDARY_MEDIA', got '{result}'"


def test_d2_normalize_strips_halfwidth_parens():
    """D2: '(foo)' is stripped by normalization, returning 'test' (not original)."""
    result = _normalize_source_type("test (foo)")
    assert result == "test", f"Expected 'test' (parentheses stripped), got '{result}'"


def test_d2_normalize_returns_stripped_if_unmapped():
    """D2: Unknown strings without parens return stripped value unchanged."""
    result = _normalize_source_type("BOOTSTRAP_HEURISTIC")
    assert result == "BOOTSTRAP_HEURISTIC", f"Expected stripped, got '{result}'"


def test_d2_normalize_maps_chinese_secondary():
    """D2: '技术博客' maps to 'SECONDARY_MEDIA'."""
    result = _normalize_source_type("技术博客")
    assert result == "SECONDARY_MEDIA", f"Expected 'SECONDARY_MEDIA', got '{result}'"


def test_d2_normalize_maps_chinese_primary_company():
    """D2: '官方博客' maps to 'PRIMARY_COMPANY'."""
    result = _normalize_source_type("官方博客")
    assert result == "PRIMARY_COMPANY", f"Expected 'PRIMARY_COMPANY', got '{result}'"


# ── D3: Unknown type detection ─────────────────────────────────────

def test_d3_unknown_type_non_strict():
    """D3: Unknown type warns but doesn't error in non-strict mode."""
    content = """## Source Register

| Source ID | Source Name | Source Type |
|-----------|-------------|-------------|
| src-001   | Some Source | BLOG_POST   |

Some text referencing src-001.
"""
    errors = check_source_consistency(content, strict=False)
    assert len(errors) == 0, f"Expected no errors in non-strict mode, got: {errors}"


def test_d3_unknown_type_strict():
    """D3: Unknown type causes error in strict mode."""
    content = """## Source Register

| Source ID | Source Name | Source Type |
|-----------|-------------|-------------|
| src-001   | Some Source | BLOG_POST   |

Some text referencing src-001.
"""
    errors = check_source_consistency(content, strict=True)
    assert len(errors) > 0, "Expected at least one error in strict mode"
    assert "unrecognized source type" in errors[0], f"Unexpected error: {errors[0]}"


def test_d3_known_types_not_unknown():
    """D3: _is_unknown_type returns False for known canonical types."""
    known = ["PRIMARY_FILING", "PRIMARY_DEV", "INFERRED", "UNCONFIRMED",
             "WEAK_SIGNAL", "TRANSCRIPT", "PRIMARY"]
    for t in known:
        assert not _is_unknown_type(t), f"{t} should NOT be unknown"


def test_d3_bogus_type_is_unknown():
    """D3: _is_unknown_type returns True for truly unknown types."""
    assert _is_unknown_type("BOGUS_TYPE"), "BOGUS_TYPE should be unknown"
    assert _is_unknown_type("__MADE_UP__"), "__MADE_UP__ should be unknown"


# ── D4: Chinese type integration ───────────────────────────────────

def test_d4_chinese_secondary_detected():
    """D4: Chinese secondary type (技术博客) + [确认事实] → error."""
    content = """## Source Register

| Source ID | Source Name | Source Type |
|-----------|-------------|-------------|
| src-001   | Tech Blog   | 技术博客    |

This is [确认事实] referencing src-001.
"""
    errors = check_source_consistency(content)
    assert len(errors) > 0, "Expected error for chinese secondary type with confirmed label"
    assert "secondary" in errors[0].lower() or "confirmed" in errors[0].lower(), \
        f"Unexpected error: {errors[0]}"


def test_d4_chinese_primary_company_detected():
    """D4: Chinese primary company type (官方博客) without caveat → error."""
    content = """## Source Register

| Source ID | Source Name | Source Type |
|-----------|-------------|-------------|
| src-001   | Official Blog | 官方博客  |

This is referencing src-001 without a caveat.
"""
    errors = check_source_consistency(content)
    assert len(errors) > 0, "Expected error for chinese primary company type without caveat"
    assert "caveat" in errors[0].lower() or "primary" in errors[0].lower(), \
        f"Unexpected error: {errors[0]}"


def test_d4_chinese_secondary_with_parens_detected():
    """D4: Chinese secondary with parens (学术综述（arXiv）) + [CONF] → error."""
    content = """## Source Register

| Source ID | Source Name | Source Type     |
|-----------|-------------|-----------------|
| src-001   | Survey Paper | 学术综述（arXiv） |

[CONF] referencing src-001 is wrong.
"""
    errors = check_source_consistency(content)
    assert len(errors) > 0, "Expected error for 学术综述 with (arXiv) parens and [CONF]"
    assert "secondary" in errors[0].lower(), f"Unexpected error: {errors[0]}"


# ── D6: Documentation — Chinese type mapping section ───────────────

DOC_FILE = "references/source-traceability-and-claim-citation.md"

def test_d6_has_chinese_type_mapping_section():
    """D6: references/source-traceability-and-claim-citation.md MUST contain ## Technical Chinese source type mapping."""
    content = read(DOC_FILE)
    assert "## Technical Chinese source type mapping" in content, \
        "Missing '## Technical Chinese source type mapping' section"


def test_d6_mapping_table_has_min_rows():
    """D6: Mapping table MUST have at least 5 mapping rows."""
    content = read(DOC_FILE)
    section_start = content.index("## Technical Chinese source type mapping")
    section = content[section_start:]
    # Count rows with Chinese source types (lines starting with | that contain non-ASCII)
    rows = [l for l in section.split('\n') if l.startswith('|') and any(ord(c) > 127 for c in l)]
    assert len(rows) >= 5, f"Mapping table has {len(rows)} Chinese rows, expected >=5"


def test_d6_table_has_required_columns():
    """D6: Mapping table MUST have '报告常见写法', '映射规范类型', and '默认最高正文标签' columns."""
    content = read(DOC_FILE)
    section_start = content.index("## Technical Chinese source type mapping")
    section = content[section_start:]
    # First table row after section
    table_start = -1
    for i, line in enumerate(section.split('\n')):
        if line.strip().startswith('|') and '报告常见写法' in line:
            table_start = i
            break
    assert table_start >= 0, "Could not find mapping table header"
    header_line = section.split('\n')[table_start]
    assert '报告常见写法' in header_line, "Missing '报告常见写法' column"
    assert '映射规范类型' in header_line, "Missing '映射规范类型' column"
    assert '默认最高正文标签' in header_line, "Missing '默认最高正文标签' column"


def test_d6_no_existing_content_deleted():
    """D6: Original content in the doc MUST survive."""
    content = read(DOC_FILE)
    original_markers = [
        "## Source type classification",
        "## Claim classification",
        "PRIMARY_FILING",
        "SECONDARY_MEDIA",
        "WEAK_SIGNAL",
        "DISCOVERY` is not a valid Source Register",  # backtick-quoted in original
    ]
    for marker in original_markers:
        assert marker in content, f"Doc lost original content: '{marker}'"


# ── D7: Eval case exists ───────────────────────────────────────────

EVAL_FILE = "evals/cases/technical-source-type-chinese-mapping-case.md"

def test_d7_eval_file_exists():
    """D7: New eval case file MUST exist."""
    path = os.path.join(REPO_ROOT, EVAL_FILE)
    assert os.path.exists(path), f"Eval case file missing: {EVAL_FILE}"


def test_d7_eval_has_standard_sections():
    """D7: Eval case MUST have standard sections."""
    content = read(EVAL_FILE)
    assert "## Goal" in content
    assert "## Prompt" in content
    assert "## What this eval is testing" in content
    assert "## Pass criteria" in content


def test_d7_eval_tests_chinese_type_mapping():
    """D7: Eval case MUST reference Chinese source type mapping."""
    content = read(EVAL_FILE)
    terms = ['Chinese', 'chinese', '中文', '技术来源', 'source type', 'mapping']
    assert any(t in content for t in terms), \
        "Eval case doesn't test Chinese source type mapping"


def test_d7_eval_expects_fail():
    """D7: Eval case must expect fail or conditional-pass verdict."""
    content = read(EVAL_FILE)
    assert any(t in content.lower() for t in ['fail', 'conditional']), \
        "Eval case should expect fail or conditional-pass verdict"


def test_d7_index_has_entry():
    """D7: evals/INDEX.md MUST have an entry for the new eval case."""
    content = read("evals/INDEX.md")
    filename = os.path.basename(EVAL_FILE)
    assert filename in content, f"INDEX.md missing entry for {filename}"


def test_d7_index_table_format():
    """D7: INDEX.md entry MUST maintain proper table format (10+ columns)."""
    content = read("evals/INDEX.md")
    filename = os.path.basename(EVAL_FILE)
    table_lines = [l for l in content.split('\n') if filename in l]
    assert len(table_lines) >= 1, f"No table line found for {filename}"
    for line in table_lines:
        cols = line.split('|')
        assert len(cols) >= 10, f"INDEX.md line has {len(cols)} cols, expected >=10: {line}"


# ── Property-based tests (hypothesis) ──────────────────────────────

try:
    from hypothesis import given, strategies as st
    HAS_HYPOTHESIS = True
except ImportError:
    HAS_HYPOTHESIS = False


def test_property_normalization_idempotent():
    """Property: Normalizing a freetext type twice gives same result."""
    for raw_type in _FREETEXT_TYPE_MAP:
        once = _normalize_source_type(raw_type)
        twice = _normalize_source_type(once)
        assert once == twice, f"Normalization not idempotent for '{raw_type}': {once} -> {twice}"


def test_property_normalize_with_cjk_parens():
    """Property: Normalizing 'base（content）' strips parens and maps correctly."""
    for base_type in list(_FREETEXT_TYPE_MAP.keys())[:5]:  # test first 5 entries
        for paren_content in ["测试", "arXiv", "2024"]:
            with_parens = f"{base_type}（{paren_content}）"
            result = _normalize_source_type(with_parens)
            assert result == _FREETEXT_TYPE_MAP[base_type], \
                f"Expected {_FREETEXT_TYPE_MAP[base_type]} for '{with_parens}', got '{result}'"


def test_property_normalize_with_halfwidth_parens():
    """Property: Normalizing 'base(content)' strips halfwidth parens correctly."""
    for base_type in list(_FREETEXT_TYPE_MAP.keys())[:5]:
        for paren_content in ["test", "v2", "2024"]:
            with_parens = f"{base_type}({paren_content})"
            result = _normalize_source_type(with_parens)
            assert result == _FREETEXT_TYPE_MAP[base_type], \
                f"Expected {_FREETEXT_TYPE_MAP[base_type]} for '{with_parens}', got '{result}'"


def test_property_normalize_canonical_noop():
    """Property: Normalizing an already-canonical type returns same value."""
    canonical_types = ["PRIMARY_FILING", "SECONDARY_MEDIA", "PRIMARY_COMPANY",
                       "INFERRED", "UNCONFIRMED", "WEAK_SIGNAL", "PRIMARY_DEV"]
    for t in canonical_types:
        assert _normalize_source_type(t) == t, f"Normalization changed canonical type '{t}'"


def test_property_strict_mode_rejects_all_unknown_types():
    """Property: In strict mode, ALL truly unknown types cause errors."""
    unknown_types = ["BLOG_POST", "TWEET", "REDDIT_POST", "SLACK_MESSAGE", "WHATSAPP_CHAT",
                     "GITHUB_DISCUSSION", "HACKER_NEWS", "LINKEDIN_POST", "MEDIUM_ARTICLE"]
    for ut in unknown_types:
        content = f"""## Source Register

| Source ID | Source Name | Source Type |
|-----------|-------------|-------------|
| src-001   | Test Source | {ut}        |

Some text referencing src-001.
"""
        errors = check_source_consistency(content, strict=True)
        assert len(errors) > 0, f"Strict mode should reject '{ut}'"


def test_property_non_strict_mode_warns_unknown_types():
    """Property: In non-strict mode, unknown types produce warnings (not errors)."""
    # We can observe the warning via stderr capture, but for simplicity
    # check that no errors are returned
    unknown_types = ["BLOG_POST", "TWEET", "WHATSAPP_CHAT"]
    for ut in unknown_types:
        content = f"""## Source Register

| Source ID | Source Name | Source Type |
|-----------|-------------|-------------|
| src-001   | Test Source | {ut}        |

Some text referencing src-001.
"""
        errors = check_source_consistency(content, strict=False)
        assert len(errors) == 0, f"Non-strict should return no errors for '{ut}'"


def test_property_mapped_types_produce_correct_check_type():
    """Property: Each mapped freetext type triggers the correct check type."""
    # SECONDARY_MEDIA mappings should trigger confirmed label check
    secondary_chinese = [k for k, v in _FREETEXT_TYPE_MAP.items() if v.startswith("SECONDARY")]
    for ct in secondary_chinese:
        content = f"""## Source Register

| Source ID | Source Name | Source Type |
|-----------|-------------|-------------|
| src-001   | Test Source | {ct}        |

[确认事实] referencing src-001.
"""
        errors = check_source_consistency(content)
        assert len(errors) > 0, f"'{ct}' (-> {_FREETEXT_TYPE_MAP[ct]}) should trigger confirmed label check"
        assert "confirmed label" in errors[0].lower(), f"'{ct}' error should mention 'confirmed label'"

    # PRIMARY_COMPANY mappings should trigger caveat check
    primary_company_chinese = [k for k, v in _FREETEXT_TYPE_MAP.items() if v == "PRIMARY_COMPANY"]
    for ct in primary_company_chinese:
        content = f"""## Source Register

| Source ID | Source Name | Source Type |
|-----------|-------------|-------------|
| src-001   | Test Source | {ct}        |

Referencing src-001 without caveat.
"""
        errors = check_source_consistency(content)
        assert len(errors) > 0, f"'{ct}' (-> PRIMARY_COMPANY) should trigger caveat check"
        assert "self-reporting caveat" in errors[0].lower(), f"'{ct}' error should mention 'self-reporting caveat'"


# ── D8: Edge case tests ────────────────────────────────────────────

import io
import contextlib


def test_d8_exempt_chinese_types_clean():
    """D8: Chinese types mapping to exempt types (PRIMARY_FILING, PRIMARY_DEV, INFERRED, WEAK_SIGNAL) produce no errors."""
    exempt_cases = [
        ("原始论文", "PRIMARY_FILING"),
        ("官方技术文档", "PRIMARY_DEV"),
        ("API文档", "PRIMARY_DEV"),
        ("多来源综合", "INFERRED"),
        ("技术分析", "INFERRED"),
        ("社区技术文章", "WEAK_SIGNAL"),
        ("知乎", "WEAK_SIGNAL"),
        ("专家访谈", "TRANSCRIPT"),
    ]
    for ct, expected_type in exempt_cases:
        content = f"""## Source Register

| Source ID | Source Name | Source Type |
|-----------|-------------|-------------|
| src-001   | Test Source | {ct}        |

Some text referencing src-001 without confirmed label or caveat issues.
"""
        errors = check_source_consistency(content)
        assert len(errors) == 0, f"'{ct}' (-> {expected_type}) should produce no errors, got: {errors}"


def test_d8_case_insensitive_english():
    """D8: Case variations of English freetext entries should still map correctly."""
    cases = [
        ("ARXIV PREPRINT", "SECONDARY_MEDIA"),
        ("Peer-reviewed Paper", "PRIMARY_FILING"),
        ("PEER-REVIEWED PAPER", "PRIMARY_FILING"),
    ]
    for raw, expected in cases:
        result = _normalize_source_type(raw)
        assert result == expected, f"Case-insensitive lookup for '{raw}' should give '{expected}', got '{result}'"


def test_d8_canonical_type_with_parens():
    """D8: Canonical types with parenthetical annotations should still match type checks."""
    # PRIMARY_FILING (annual report) should still be PRIMARY_FILING after normalization
    result = _normalize_source_type("PRIMARY_FILING (annual report)")
    assert result == "PRIMARY_FILING", f"Canonical type with parens should be stripped to 'PRIMARY_FILING', got '{result}'"
    assert not _is_unknown_type(result), "PRIMARY_FILING should not be unknown"

    # SECONDARY_MEDIA with parenthetical should still be detected as secondary
    result = _normalize_source_type("SECONDARY_MEDIA (arXiv)")
    assert result == "SECONDARY_MEDIA", f"SECONDARY_MEDIA with parens should be stripped, got '{result}'"
    assert _is_secondary_type(result), "SECONDARY_MEDIA should be detected as secondary"


def test_d8_new_chinese_types():
    """D8: Newly added Chinese types map correctly."""
    cases = [
        ("招股书", "PRIMARY_FILING"),
        ("年报", "PRIMARY_FILING"),
        ("公司公告", "PRIMARY_COMPANY"),
        ("新闻报道", "SECONDARY_MEDIA"),
        ("券商研报", "SECONDARY_ANALYST"),
        ("知乎", "WEAK_SIGNAL"),
        ("微信公众号", "WEAK_SIGNAL"),
        ("专家访谈", "TRANSCRIPT"),
        ("白皮书", "PRIMARY_DEV"),
    ]
    for raw, expected in cases:
        assert _normalize_source_type(raw) == expected, f"'{raw}' should map to '{expected}'"


def test_d8_non_strict_stderr_warning():
    """D8: Non-strict mode should print warning to stderr for unknown types."""
    content = """## Source Register

| Source ID | Source Name | Source Type |
|-----------|-------------|-------------|
| src-001   | Test Source | MYSTERY_TYPE |

Some text referencing src-001.
"""
    stderr_buf = io.StringIO()
    with contextlib.redirect_stderr(stderr_buf):
        errors = check_source_consistency(content, strict=False)
    assert len(errors) == 0, "Non-strict should return no errors"
    stderr_output = stderr_buf.getvalue()
    assert "warning:" in stderr_output, f"Expected warning on stderr, got: {stderr_output}"


def test_d8_normalize_accounting_for_whitespace():
    """D8: Chinese types with extra whitespace should still be normalized."""
    result = _normalize_source_type("  学术综述  ")
    assert result == "SECONDARY_MEDIA", f"Whitespace-padded '学术综述' should map to SECONDARY_MEDIA"


# ── Cross-file invariants ─────────────────────────────────────────

def test_p1_validator_has_normalize_function():
    """P1: Validator script must have _normalize_source_type defined."""
    content = read("scripts/validate_source_label_consistency.py")
    assert "def _normalize_source_type" in content, "Validator missing _normalize_source_type"


def test_p1_validator_has_strict_flag():
    """P1: Validator script must have --strict argument."""
    content = read("scripts/validate_source_label_consistency.py")
    assert "--strict" in content, "Validator missing --strict flag"


def test_p1_validator_has_chinese_map():
    """P1: Validator script must have _FREETEXT_TYPE_MAP."""
    content = read("scripts/validate_source_label_consistency.py")
    assert "_FREETEXT_TYPE_MAP" in content, "Validator missing _FREETEXT_TYPE_MAP"


def test_p2_index_not_broken():
    """P2: INDEX.md table structure should remain parseable."""
    content = read("evals/INDEX.md")
    table_lines = []
    in_table = False
    for line in content.split('\n'):
        if line.startswith('| ---'):
            in_table = True
            continue
        if in_table and line.startswith('|'):
            table_lines.append(line)
        elif in_table and not line.startswith('|'):
            in_table = False
    if table_lines:
        counts = [len(l.split('|')) for l in table_lines]
        assert max(counts) == min(counts), f"Inconsistent INDEX.md table columns: {counts}"


# ── D5: Known types still work ─────────────────────────────────────

def test_d5_known_types_still_work():
    """D5: PRIMARY_FILING still works correctly (no errors)."""
    content = """## Source Register

| Source ID | Source Name      | Source Type    |
|-----------|------------------|----------------|
| src-001   | Some Paper       | PRIMARY_FILING |

Some text referencing src-001.
"""
    errors = check_source_consistency(content)
    assert len(errors) == 0, f"Expected no errors for PRIMARY_FILING, got: {errors}"


def test_d5_secondary_still_works():
    """D5: SECONDARY_MEDIA + [确认事实] still errors."""
    content = """## Source Register

| Source ID | Source Name | Source Type     |
|-----------|-------------|-----------------|
| src-001   | Media Source | SECONDARY_MEDIA |

This is [确认事实] referencing src-001.
"""
    errors = check_source_consistency(content)
    assert len(errors) > 0, "Existing secondary check should still work"
    assert "secondary" in errors[0].lower(), f"Unexpected error: {errors[0]}"


def test_d5_primary_company_still_works():
    """D5: PRIMARY_COMPANY without caveat still errors."""
    content = """## Source Register

| Source ID | Source Name | Source Type     |
|-----------|-------------|-----------------|
| src-001   | Company Source | PRIMARY_COMPANY |

This is referencing src-001 without a caveat.
"""
    errors = check_source_consistency(content)
    assert len(errors) > 0, "Existing primary company check should still work"
    assert "caveat" in errors[0].lower(), f"Unexpected error: {errors[0]}"


# ── Main ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    tests = [
        ("D1: imports new functions", test_d1_imports_new_functions),
        ("D2: normalize strips CJK parens", test_d2_normalize_strips_cjk_parens),
        ("D2: normalize strips halfwidth parens", test_d2_normalize_strips_halfwidth_parens),
        ("D2: normalize returns stripped if unmapped", test_d2_normalize_returns_stripped_if_unmapped),
        ("D2: normalize maps chinese secondary", test_d2_normalize_maps_chinese_secondary),
        ("D2: normalize maps chinese primary company", test_d2_normalize_maps_chinese_primary_company),
        ("D3: unknown type non-strict", test_d3_unknown_type_non_strict),
        ("D3: unknown type strict", test_d3_unknown_type_strict),
        ("D3: known types not unknown", test_d3_known_types_not_unknown),
        ("D3: bogus type is unknown", test_d3_bogus_type_is_unknown),
        ("D4: chinese secondary detected", test_d4_chinese_secondary_detected),
        ("D4: chinese primary company detected", test_d4_chinese_primary_company_detected),
        ("D4: chinese secondary with parens detected", test_d4_chinese_secondary_with_parens_detected),
        ("D5: known types still work", test_d5_known_types_still_work),
        ("D5: secondary still works", test_d5_secondary_still_works),
        ("D5: primary company still works", test_d5_primary_company_still_works),
        ("D6: has chinese type mapping section", test_d6_has_chinese_type_mapping_section),
        ("D6: mapping table has 5+ rows", test_d6_mapping_table_has_min_rows),
        ("D6: table has required columns", test_d6_table_has_required_columns),
        ("D6: no existing content deleted", test_d6_no_existing_content_deleted),
        ("D7: eval file exists", test_d7_eval_file_exists),
        ("D7: has standard sections", test_d7_eval_has_standard_sections),
        ("D7: tests chinese type mapping", test_d7_eval_tests_chinese_type_mapping),
        ("D7: expects fail", test_d7_eval_expects_fail),
        ("D7: index has entry", test_d7_index_has_entry),
        ("D7: index table format", test_d7_index_table_format),
        ("P1: validator has normalize function", test_p1_validator_has_normalize_function),
        ("P1: validator has --strict flag", test_p1_validator_has_strict_flag),
        ("P1: validator has chinese map", test_p1_validator_has_chinese_map),
        ("P2: index not broken", test_p2_index_not_broken),
        ("PROP: normalization idempotent", test_property_normalization_idempotent),
        ("PROP: normalize CJK parens", test_property_normalize_with_cjk_parens),
        ("PROP: normalize halfwidth parens", test_property_normalize_with_halfwidth_parens),
        ("PROP: canonical noop", test_property_normalize_canonical_noop),
        ("PROP: strict rejects unknowns", test_property_strict_mode_rejects_all_unknown_types),
        ("PROP: non-strict warns unknowns", test_property_non_strict_mode_warns_unknown_types),
        ("PROP: mapped types correct check", test_property_mapped_types_produce_correct_check_type),
        ("D8: exempt chinese types clean", test_d8_exempt_chinese_types_clean),
        ("D8: case insensitive english", test_d8_case_insensitive_english),
        ("D8: canonical type with parens", test_d8_canonical_type_with_parens),
        ("D8: new chinese types", test_d8_new_chinese_types),
        ("D8: non-strict stderr warning", test_d8_non_strict_stderr_warning),
        ("D8: whitespace handling", test_d8_normalize_accounting_for_whitespace),
    ]

    passed = 0
    failed = 0
    for name, fn in tests:
        try:
            fn()
            print(f"  ✅ {name}")
            passed += 1
        except (AssertionError, ValueError) as e:
            print(f"  ❌ {name}: {e}")
            failed += 1
        except Exception as e:
            print(f"  ❌ {name}: Unexpected error: {e}")
            failed += 1

    print(f"\n{'='*50}")
    print(f"Results: {passed} passed, {failed} failed")
    if failed:
        sys.exit(1)
    else:
        print("All contracts verified ✅")
