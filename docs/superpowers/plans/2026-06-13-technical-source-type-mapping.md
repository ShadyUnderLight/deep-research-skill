# Technical Source Type Mapping Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close the "schema not closed" gap where reports using Chinese free-text source types (e.g., "官方技术文档", "技术博客") bypass `validate_source_label_consistency.py` because the validator only recognizes canonical English type names.

**Architecture:** Add a Chinese→canonical type mapping dict + unknown-type warning in validator; add mapping table to documentation; add eval case and contract tests. All existing check logic stays untouched — only add the mapping layer before existing type checks.

**Tech Stack:** Python 3 (no new dependencies), Markdown

**Contracts (4 deliverables):**
- D1: `scripts/validate_source_label_consistency.py` — add `_TECHNICAL_CHINESE_MAP`, normalization function, `_is_unknown_type` check, `--strict` flag
- D2: `references/source-traceability-and-claim-citation.md` — add `## Technical Chinese source type mapping` section
- D3: `evals/cases/technical-source-type-chinese-mapping-case.md` — new eval case
- D4: `tests/test_issue_272_contracts.py` — contract tests

---

### Task 1: Update validator — Chinese type mapping + unknown type check + --strict

**Files:**
- Modify: `scripts/validate_source_label_consistency.py`
- Test: `tests/test_issue_272_contracts.py` (partially)

**Design (CoT):**

The validator currently has a gap at lines 244-265: after checking `_is_secondary_type()` and `_is_primary_company_type()`, any unrecognized source type silently passes. The fix has 3 parts:

1. **Normalization**: Before type checks, normalize the source_type string. Strip parenthetical content (e.g., "学术综述（arXiv）" → "学术综述"), then look up in `_TECHNICAL_CHINESE_MAP`. If found, use the mapped canonical type.

2. **Unknown type detection**: After normalization + existing checks, if the type still doesn't match any known category, emit a warning (non-strict) or error (strict).

3. **--strict flag**: Add `--strict` to argparse. In strict mode, unknown types cause exit code 2. In non-strict mode, they cause a warning print but exit 0.

Three candidate approaches for unknown type handling:
- **Candidate A (chosen):** Warn always, only fail under --strict. This gives existing reports breathing room while hardening forward.
- **Candidate B:** Always hard-fail on unknown types. Too aggressive — breaks existing reports.
- **Candidate C:** Hard-fail only when the report also has confirmed labels on unknown types. More complex, not worth it.

**Chosen: Candidate A**

- [ ] **Step 1: Install hypothesis for property-based testing**

Run: `pip install hypothesis`

- [ ] **Step 2: Write failing tests for the validator changes**

```python
# In tests/test_issue_272_contracts.py (partial — full file in Task 4)
# Test that the normalize function strips parenthetical content
def test_normalize_strips_parens():
    assert _normalize_source_type("学术综述（arXiv）") == "学术综述"

# Test that Chinese types map correctly
def test_chinese_type_mapping():
    result = check_source_consistency("[S01] 学术综述 [S01] with [确认事实]")
    # Should fail because 学术综述→SECONDARY_MEDIA→can't have confirmed label
    assert len(result) > 0
```

- [ ] **Step 3: Run tests to verify they fail**

Run: `python tests/test_issue_272_contracts.py`
Expected: tests that reference new functions fail with NameError/ImportError

- [ ] **Step 4: Implement validator changes**

```python
# Add to validate_source_label_consistency.py:

_TECHNICAL_CHINESE_MAP: dict[str, str] = {
    "原始论文": "PRIMARY_FILING",
    "peer-reviewed paper": "PRIMARY_FILING",
    "学术综述": "SECONDARY_MEDIA",
    "arxiv preprint": "SECONDARY_MEDIA",
    "arXiv preprint": "SECONDARY_MEDIA",
    "官方技术文档": "PRIMARY_DEV",
    "框架文档": "PRIMARY_DEV",
    "官方文档": "PRIMARY_DEV",
    "技术博客": "SECONDARY_MEDIA",
    "官方博客": "PRIMARY_COMPANY",
    "官方技术博客": "PRIMARY_COMPANY",
    "行业研究报告": "SECONDARY_ANALYST",
    "技术分析（多来源综合）": "INFERRED",
    "技术分析": "INFERRED",
    "多来源综合": "INFERRED",
    "社区技术文章": "WEAK_SIGNAL",
    "博客园": "WEAK_SIGNAL",
    "csdn": "WEAK_SIGNAL",
    "CSDN": "WEAK_SIGNAL",
    "reddit": "WEAK_SIGNAL",
    "Reddit": "WEAK_SIGNAL",
    "社区文章": "WEAK_SIGNAL",
}
```

Add normalization function:
```python
def _normalize_source_type(source_type: str) -> str:
    """Normalize a source type string for canonical lookup.
    
    1. Strip parenthetical content like （arXiv）
    2. Strip whitespace
    3. Look up in Chinese mapping dict
    4. Return canonical type if found, original string if not
    """
    s = source_type.strip()
    # Remove CJK parentheses and content
    s = re.sub(r'[（(][^）)]*[）)]', '', s).strip()
    # Remove half-width parentheses and content
    s = re.sub(r'\([^)]*\)', '', s).strip()
    # Check Chinese mapping
    if s in _TECHNICAL_CHINESE_MAP:
        return _TECHNICAL_CHINESE_MAP[s]
    return source_type  # return original if no mapping found
```

Modify `check_source_consistency()` to use normalization:
```python
# Before the type-check loop, normalize:
normalized_sources = []
for source_id, source_type in sources:
    normalized = _normalize_source_type(source_type)
    normalized_sources.append((source_id, normalized))

# In the loop, use normalized type for checks but track original for error messages
for (source_id, orig_type), (_, norm_type) in zip(sources, normalized_sources):
    # ...existing secondary check on norm_type...
    # ...existing primary_company check on norm_type...
    # NEW: unknown type check
    if not _is_secondary_type(norm_type) and not _is_primary_company_type(norm_type):
        # ...warning/error depending on strict mode
```

Add `--strict` to argparse:
```python
parser.add_argument("--strict", action="store_true",
    help="Fail on unknown source types (default: warn only)")
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `python tests/test_issue_272_contracts.py`
Expected: ALL PASS

- [ ] **Step 6: Run the existing validator against a known-clean file to verify no regression**

Run: `python scripts/validate_source_label_consistency.py evals/cases/source-traceability-moore-threads-case.md`
Expected: exits 0

- [ ] **Step 7: Manual test with a Chinese-type report**

Run: `python scripts/validate_source_label_consistency.py --strict /tmp/test-chinese-source.md` (after creating a test file)
Expected: fails with unknown source type warning

- [ ] **Step 8: Commit**

```bash
git add scripts/validate_source_label_consistency.py
git add tests/test_issue_272_contracts.py
git commit -m "feat(validator): add Chinese technical source type mapping and --strict mode (#272)"
```

---

### Task 2: Add documentation — Chinese source type mapping table

**Files:**
- Modify: `references/source-traceability-and-claim-citation.md`

- [ ] **Step 1: Write failing contract test**

Add to `tests/test_issue_272_contracts.py`:
```python
def test_d2_has_chinese_type_mapping_section():
    content = read("references/source-traceability-and-claim-citation.md")
    assert "## Technical Chinese source type mapping" in content
```

Run: `python tests/test_issue_272_contracts.py`
Expected: test_d2_has_chinese_type_mapping_section FAILS

- [ ] **Step 2: Add the mapping table**

Add after the `## Source type classification` section (after line 268, before `## Claim classification`):

```markdown
## Technical Chinese source type mapping

技术类报告 Source Register 中的常见中文来源类型到规范类型的映射。此映射供 `validate_source_label_consistency.py` 使用，也作为报告编写者的参考。

| 报告常见写法 | 映射规范类型 | 默认最高正文标签 | 说明 |
|---|---|---|---|
| 原始论文 / peer-reviewed paper | PRIMARY_FILING | [确认事实] for paper claims; [推断] for generalization | 只确认论文报告了某实验 |
| arXiv preprint / 学术综述 | SECONDARY_MEDIA | [推断] unless citing paper existence | 预印本状态需说明 |
| 官方技术文档 / 框架文档 | PRIMARY_DEV | [确认事实] for API/docs existence; caveated for performance/adoption | 厂商自述需 caveat |
| 技术博客 / 官方博客 | SECONDARY_MEDIA / PRIMARY_COMPANY | [推断] or caveated | 官方博客可升为 PRIMARY_COMPANY，厂商自述需 caveat |
| 行业研究报告 | SECONDARY_ANALYST | [推断] | 不能无 caveat 标 confirmed |
| 社区技术文章 / 博客园 / CSDN | WEAK_SIGNAL | [推断]/[未知] | 只作补充 |
| 多来源综合 / 技术分析 | INFERRED | [推断] | 必须有推理链 |

**使用说明：**
- 此映射是示例性而非穷举性。新增常见写法应添加到 `scripts/validate_source_label_consistency.py` 的 `_TECHNICAL_CHINESE_MAP` 中。
- 带括号的变体（如"学术综述（arXiv）"）会在查找前剥离括号内容，映射到基础条目。
- 优先使用规范类型（PRIMARY_FILING, SECONDARY_MEDIA 等）而非中文自由文本。中文类型仅为兼容已有报告格式的 fallback。
```

- [ ] **Step 3: Run contracts tests — should pass now**

Run: `python tests/test_issue_272_contracts.py`
Expected: test_d2_has_chinese_type_mapping_section PASSES

- [ ] **Step 4: Commit**

```bash
git add references/source-traceability-and-claim-citation.md
git commit -m "docs: add Technical Chinese source type mapping table (#272)"
```

---

### Task 3: Create eval case for Chinese source type mapping

**Files:**
- Create: `evals/cases/technical-source-type-chinese-mapping-case.md`
- Modify: `evals/INDEX.md`

- [ ] **Step 1: Write failing contract test**

```python
def test_d3_eval_file_exists():
    assert os.path.exists(os.path.join(REPO_ROOT, "evals/cases/technical-source-type-chinese-mapping-case.md"))
```

Run: `python tests/test_issue_272_contracts.py`
Expected: test_d3_eval_file_exists FAILS

- [ ] **Step 2: Create eval case file**

Follow the pattern from `agentic-rag-technical-deep-dive-compounded-case.md`:

```markdown
# Eval: Technical Source Type Chinese Mapping — Uncalibrated Free Text Case

## Goal

Test that the `validate_source_label_consistency.py` validator correctly:
1. Maps common Chinese technical source types (官方文档, 技术博客, 行业研究报告) to canonical types
2. Fails reports that use these types to support [确认事实] without caveats
3. Reports unknown/unmapped source types as warnings (non-strict) or errors (--strict)

## Prompt

Produce a structured technical deep-dive report comparing [two technical topics].
The Source Register must use Chinese free-text source types. The body must label
source claims based on these types.

## What this eval is testing

- Whether the Chinese→canonical type mapping correctly routes 官方技术文档 → PRIMARY_DEV (needs caveat)
- Whether 行业研究报告 → SECONDARY_ANALYST triggers [确认事实] detection
- Whether 学术综述（arXiv）→ SECONDARY_MEDIA triggers [确认事实] detection
- Whether an unmapped Chinese type triggers a warning in non-strict mode and error in --strict mode

## Pass criteria

Validator --strict detects:
- 官方技术文档 supporting [确认事实] without caveat → fail
- 行业研究报告 supporting [确认事实] → fail  
- 学术综述 supporting [确认事实] → fail
- An unmapped Chinese type → error in --strict, warning in non-strict

## Failure signs

- Validator silently passes Chinese free-text source types without mapping
- Validator treats unmapped types as valid (no warning or error)
- Chinese type mapping causes false positives on known clean patterns

## Current rule verdict

- Source type chinese mapping: mandatory
- Unknown type handling: warning (default), error (--strict)
- vendor/secondary docs as [确认事实] without caveat: fail

## Reviewer checklist

- Does Chinese type mapping handle parenthetical variants (学术综述（arXiv）)?
- Does unmapped type produce at least a warning?
- Does --strict mode correctly escalate warnings to errors?
- Are all existing canonical types still working unchanged?
```

- [ ] **Step 3: Run contracts tests**

Run: `python tests/test_issue_272_contracts.py`
Expected: test_d3_eval_file_exists PASSES

- [ ] **Step 4: Update evals/INDEX.md**

Add the new eval entry.

- [ ] **Step 5: Commit both files**

```bash
git add evals/cases/technical-source-type-chinese-mapping-case.md
git add evals/INDEX.md
git commit -m "feat(eval): add Chinese source type mapping eval case (#272)"
```

---

### Task 4: Create contract tests (test_issue_272_contracts.py)

**Files:**
- Create: `tests/test_issue_272_contracts.py`

- [ ] **Step 1: Write the complete contract test file**

Following the pattern of `test_issue_270_contracts.py`. Cover:

D1 checks (validator):
- `test_d1_normalize_strips_parenthetical`: _normalize_source_type("学术综述（arXiv）") == "学术综述"
- `test_d1_normalize_strips_halfwidth_parens`: _normalize_source_type("test (foo)") == "test"  
- `test_d1_chinese_map_correct_types`: Each Chinese type maps to expected canonical type
- `test_d1_unknown_type_non_strict_warns`: Unknown type in non-strict mode warns but exits 0
- `test_d1_unknown_type_strict_fails`: Unknown type in --strict mode exits 2
- `test_d1_secondary_chinese_type_detected`: Chinese secondary type + [确认事实] → error
- `test_d1_primary_company_chinese_type_detected`: Chinese primary company type without caveat → error
- `test_d1_known_types_still_work`: Canonical types (PRIMARY_FILING, SECONDARY_MEDIA) still checked correctly

D2 checks (documentation):
- `test_d2_has_chinese_type_mapping_section`: references/source-traceability-and-claim-citation.md contains the mapping table
- `test_d2_mapping_table_has_required_rows`: Table has ≥5 rows of mappings
- `test_d2_no_existing_content_deleted`: Original content landmarks survive

D3 checks (eval case):
- `test_d3_eval_file_exists`: File exists
- `test_d3_has_standard_sections`: Has Goal, Prompt, What, Pass, Failure sections
- `test_d3_tests_chinese_mapping`: Content references Chinese source type mapping
- `test_d3_index_has_entry`: INDEX.md has entry

Cross-file:
- `test_p1_validator_imports_normalize`: validator script has _normalize_source_type function
- `test_p1_validator_has_strict_flag`: validator script has --strict argument

- [ ] **Step 2: Run the tests — they should all pass since implementation is done**

Run: `python tests/test_issue_272_contracts.py`
Expected: ALL PASS

- [ ] **Step 3: Commit**

```bash
git add tests/test_issue_272_contracts.py
git commit -m "test: add contract tests for Chinese source type mapping (#272)"
```

---

### Task 5: Install hypothesis and add property-based tests

**Files:**
- Modify: `tests/test_issue_272_contracts.py` (add property-based tests section)

- [ ] **Step 1: Install hypothesis**

```bash
pip install hypothesis
```

- [ ] **Step 2: Add property-based tests**

```python
from hypothesis import given, strategies as st

# Property: For any valid Chinese type string (with or without parens),
# normalization should produce the same canonical type
@given(st.sampled_from(list(_TECHNICAL_CHINESE_MAP.keys())))
def test_property_normalization_idempotent(raw_type):
    """Normalizing a Chinese type twice gives same result."""
    once = _normalize_source_type(raw_type)
    twice = _normalize_source_type(once)
    assert once == twice

# Property: Adding random parenthetical content to a Chinese type
# should still normalize to the same canonical type
@given(st.sampled_from(list(_TECHNICAL_CHINESE_MAP.keys())),
       st.text(alphabet="（），。", min_size=0, max_size=20))
def test_property_normalize_with_parens(base_type, paren_content):
    """Normalizing 'type（content）' should strip parens and map correctly."""
    if not paren_content:
        return
    with_parens = f"{base_type}（{paren_content}）"
    result = _normalize_source_type(with_parens)
    assert result == _TECHNICAL_CHINESE_MAP[base_type]

# Property: Normalizing an already-canonical type should be a no-op
@given(st.sampled_from(["PRIMARY_FILING", "SECONDARY_MEDIA", "PRIMARY_COMPANY", "INFERRED"]))
def test_property_normalize_canonical_noop(canonical_type):
    """Normalizing a canonical type returns the same value."""
    assert _normalize_source_type(canonical_type) == canonical_type
```

- [ ] **Step 3: Run property-based tests**

```bash
python -c "from tests.test_issue_272_contracts import *; test_property_normalization_idempotent(); test_property_normalize_with_parens(); test_property_normalize_canonical_noop()"
```

Expected: ALL PASS

- [ ] **Step 4: Commit**

```bash
git add tests/test_issue_272_contracts.py
git commit -m "test: add property-based tests for Chinese type normalization (#272)"
```

---

### Verification

After all tasks:

```bash
# Full contract test suite
python tests/test_issue_272_contracts.py

# Regression: existing validator on known files
python scripts/validate_source_label_consistency.py evals/cases/source-traceability-moore-threads-case.md

# Manual smoke test with Chinese types
python scripts/validate_source_label_consistency.py --strict evals/cases/technical-source-type-chinese-mapping-case.md
```

Expected: All pass or reasonable output.

