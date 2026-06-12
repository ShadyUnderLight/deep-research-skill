# Process-Integrity Self-Assessment Cross-Check Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add automation for the process-integrity gate: verify that audit block self-assessment ("✅ Passed") matches actual body execution.

**Architecture:** New function `check_audit_self_assessment_consistency()` in `validate_report_quality.py`. Parses the audit table from the Route and audit status section, maps each claimed-discipline to a structural check on the body text, emits warnings (not errors) on mismatch. Tests added to `test_report_quality_validator.py`.

**Tech Stack:** Python 3, regex-based Markdown parsing (same pattern as existing validators)

**Constraints:**
- New checks emit WARN only (no hard-fail), preserving existing exit code behavior
- Unknown discipline names in audit table → skip silently (no false positives)
- Do not import from `validate_declared_execution.py` — use local pattern definitions
- Do not change existing validator behavior or exit codes

---

### Task 1: Write failing test for source-traceability self-assessment mismatch

**Files:**
- Modify: `scripts/test_report_quality_validator.py`

- [ ] **Step 1: Add fixture and test for source-traceability claimed ✅ but body has zero refs**

```python
def test_audit_source_traceability_mismatch_warns() -> None:
    """source-traceability marked ✅ Passed but body has zero [Sxx] refs → warn."""
    text = """\
## Route and audit status

**Primary route**: Provider / Vendor Selection

| Audit | Status | 证据 |
|-------|--------|------|
| source-traceability | ✅ Passed | §3 已验证 |
| final-audit | ✅ Passed | §2 已验证 |

## Findings

No source references in the actual body text.

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Example | secondary | 2026-01-01 | https://example.com | medium | §2 |
"""
    result = run_validator(text)
    # Must still pass (exit 0) since this is a WARN check
    assert result.returncode == 0, (
        f"expected pass (exit 0), got {result.returncode}\n"
        f"stdout: {result.stdout}"
    )
    # But must contain the warning
    assert "self-assessment mismatch" in result.stdout.lower(), (
        f"expected warning about self-assessment mismatch in:\n{result.stdout}"
    )
    print("  PASS  audit source-traceability mismatch warns")
```

- [ ] **Step 2: Run test to verify it fails (or passes without warning)**

```bash
python3 scripts/test_report_quality_validator.py
```

Expected: Test fails — either because the warning is not produced, or because the test function isn't registered in `main()`.

---

### Task 2: Implement `check_audit_self_assessment_consistency()` for source-traceability

**Files:**
- Modify: `scripts/validate_report_quality.py`

- [ ] **Step 1: Add the new function before the main section**

```python
def check_audit_self_assessment_consistency(cleaned: str) -> list[str]:
    """Check that audit block self-assessments match actual body execution.
    
    Warnings-level: if the audit block claims a discipline passed but the
    body does not meet the corresponding structural requirement, a warning
    is issued. Unknown discipline names are silently skipped.
    """
    sec = section_text(cleaned, ROUTE_AUDIT_HEADING)
    if sec is None:
        return []
    
    table = parse_table(sec)
    if table is None:
        return []
    
    header = table[0]
    audit_idx = find_col_index(header, [AUDIT_COL_RE])
    status_idx = find_col_index(header, [STATUS_COL_RE])
    
    if audit_idx == -1 or status_idx == -1:
        return []
    
    warnings: list[str] = []
    body = body_before_source_register(cleaned)
    
    for row in table[1:]:
        if len(row) <= max(audit_idx, status_idx):
            continue
        discipline = row[audit_idx].strip()
        status = row[status_idx].strip()
        
        if not AUDIT_PASSED_RE.match(status):
            continue
        
        disc_lower = discipline.lower()
        
        # source-traceability: body must have [Sxx] or equivalent citations
        if 'source-traceability' in disc_lower or 'source traceability' in disc_lower:
            has_refs = bool(BODY_SXX_RE.search(body))
            if not has_refs:
                has_equiv = bool(AUTHOR_YEAR_RE.search(body) or ARXIV_RE.search(body) or DOI_RE.search(body) or NL_ATTR_RE.search(body))
                if not has_equiv:
                    warnings.append(
                        f"Audit self-assessment mismatch: '{discipline}' is marked "
                        "✅ Passed, but the body has no [Sxx] or equivalent source citations"
                    )
    
    return warnings
```

- [ ] **Step 2: Wire it into `validate_file()` — add after existing checks, emit as warnings**

In `validate_file()`, after the existing checks block (lines 425-438), add:

```python
    # 4. Audit self-assessment consistency (warnings only)
    warnings.extend(check_audit_self_assessment_consistency(cleaned))
```

- [ ] **Step 3: Run test to verify it passes**

```bash
python3 scripts/test_report_quality_validator.py
```

Expected: Test passes, warning appears in stdout for the mismatch case.

---

### Task 3: Write failing test for quantitative-role self-assessment mismatch

**Files:**
- Modify: `scripts/test_report_quality_validator.py`

- [ ] **Step 1: Add fixture and test for quantitative-role claimed ✅ but no role labels**

```python
def test_audit_quantitative_role_mismatch_warns() -> None:
    """quantitative-role marked ✅ Passed but body tables have no O/P/A/M labels."""
    text = """\
## Route and audit status

**Primary route**: Provider / Vendor Selection

| Audit | Status | 证据 |
|-------|--------|------|
| quantitative-role | ✅ Passed | §4 已验证 |
| source-traceability | ✅ Passed | 正文使用 [S01] 引用 |
| final-audit | ✅ Passed | §2 已验证 |

## Findings

Body text with citation [S01].

| Metric | Base | Upside |
|--------|------|--------|
| Market size | $10B | $15B |
| Adoption | 25% | 35% |

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Example | secondary | 2026-01-01 | https://example.com | medium | §2 |
"""
    result = run_validator(text)
    assert result.returncode == 0, (
        f"expected pass (exit 0), got {result.returncode}\n"
        f"stdout: {result.stdout}"
    )
    assert "self-assessment mismatch" in result.stdout.lower(), (
        f"expected warning about self-assessment mismatch in:\n{result.stdout}"
    )
    print("  PASS  audit quantitative-role mismatch warns")
```

- [ ] **Step 2: Run test to verify it fails**

```bash
python3 scripts/test_report_quality_validator.py
```

Expected: Test fails — the quantitative-role check is not yet implemented.

---

### Task 4: Add quantitative-role check to implementation

**Files:**
- Modify: `scripts/validate_report_quality.py`

- [ ] **Step 1: Add role-label patterns near other regex patterns (after line 59)**

```python
ROLE_HEADER_RE = re.compile(r"(?:数字角色|number role|role|epistemic role)", re.IGNORECASE)
ROLE_VALUE_RE = re.compile(
    r"(?:\b[OPAM]\b|observed|proxy|assumption|model\s*output|estimate|scenario|inferred|illustrative)",
    re.IGNORECASE,
)
TABLE_ROW_RE_CHECK = re.compile(r"^\s*\|.*\|\s*$")  # reuses existing
```

- [ ] **Step 2: Add quantitative-role branch to `check_audit_self_assessment_consistency()`**

After the source-traceability block in the function, add:

```python
        # quantitative-role: numeric table rows should have role label column
        if 'quantitative-role' in disc_lower or 'quantitative role' in disc_lower or '数字角色' in disc_lower:
            # Check if any table rows with numbers also have role labels
            lines = cleaned.splitlines()
            table_rows = [l for l in lines if TABLE_ROW_RE.match(l) and not TABLE_DELIMITER_RE.match(l)]
            numeric_rows = [r for r in table_rows if re.search(r'\d', r)]
            role_rows = [r for r in table_rows if ROLE_VALUE_RE.search(r) or ROLE_HEADER_RE.search(r)]
            if numeric_rows and not role_rows:
                warnings.append(
                    f"Audit self-assessment mismatch: '{discipline}' is marked "
                    "✅ Passed, but no quantitative role labels (O/P/A/M or equivalent) "
                    "found in body tables"
                )
```

- [ ] **Step 3: Run test to verify it passes**

```bash
python3 scripts/test_report_quality_validator.py
```

Expected: Test passes.

---

### Task 5: Write failing test for consistent (no mismatch) passes

**Files:**
- Modify: `scripts/test_report_quality_validator.py`

- [ ] **Step 1: Add fixture and test where all audit claims are consistent**

```python
def test_audit_self_assessment_consistent_no_warn() -> None:
    """Audit claims match body execution → no self-assessment warnings."""
    text = """\
## Route and audit status

**Primary route**: Provider / Vendor Selection

| Audit | Status | 证据 |
|-------|--------|------|
| source-traceability | ✅ Passed | §3-§5 正文使用 [S01] 引用 |
| quantitative-role | ✅ Passed | §4 表格含角色列 |
| final-audit | ✅ Passed | §2 各关卡可追溯 |

## Findings

The market is growing [S01].

| Metric | Base | Upside | Role |
|--------|------|--------|------|
| Market size | $10B | $15B | A |
| Adoption | 25% | 35% | M |

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Example | secondary | 2026-01-01 | https://example.com | medium | §2 |
"""
    result = run_validator(text)
    assert result.returncode == 0, (
        f"expected pass (exit 0), got {result.returncode}\n"
        f"stdout: {result.stdout}"
    )
    assert "self-assessment mismatch" not in result.stdout.lower(), (
        f"unexpected self-assessment mismatch warning in:\n{result.stdout}"
    )
    print("  PASS  audit self-assessment consistent")
```

- [ ] **Step 2: Run test to verify it fails (or passes incorrectly)**

```bash
python3 scripts/test_report_quality_validator.py
```

Expected: Test may pass or fail depending on whether role detection is working correctly. If it thinks the Role header counts as a value, this could produce a false positive. We may need to tune.

- [ ] **Step 3: Tune implementation to avoid false positives**

If the test produces a false-positive warning, adjust the role detection to only count data rows (not header rows) as evidence of role application:

```python
            # Count only data rows (after header+delimiter) with role values
            role_data_rows = [r for r in rows_after_header if ROLE_VALUE_RE.search(r)]
            if numeric_data_rows and not role_data_rows:
                # warn
```

---

### Task 6: Run all tests and verify no regressions

**Files:** none (run commands)

- [ ] **Step 1: Run both test suites**

```bash
python3 scripts/test_report_quality_validator.py
python3 scripts/test_declared_execution.py
```

Expected: All tests pass. No regressions.

- [ ] **Step 2: Verify warning messages look right**

Check the stdout of the mismatch tests to ensure the warning messages are clear and actionable.

---

### Task 7: Commit and open PR

**Files:** none (git operations)

- [ ] **Step 1: Check git status**

```bash
git status
git diff
```

- [ ] **Step 2: Commit**

```bash
git add scripts/validate_report_quality.py scripts/test_report_quality_validator.py
git commit -m "feat: add audit self-assessment consistency check (process-integrity gate)

Add check_audit_self_assessment_consistency() to validate_report_quality.py
that cross-references audit block self-assessment status against actual
body execution:

- source-traceability ✅ → body must have [Sxx] or equivalent citations
- quantitative-role ✅ → numeric table rows must have role labels

Warnings-level only (non-blocking), preserving existing exit codes.

Implements the automated core of the process-integrity gate defined
in checklists/final-audit.md §57-62.

Closes #247"
```

- [ ] **Step 3: Push and open PR**

```bash
git push origin HEAD
gh pr create --fill
```
