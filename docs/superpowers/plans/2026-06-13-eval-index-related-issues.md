# Eval Index Related Issues Update — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Update `evals/INDEX.md` related issue column for the Agentic RAG compounded eval from `#268` to `#268, #269, #270, #271, #272` to satisfy issue #273 acceptance criterion #4.

**Architecture:** Single-line change to the INDEX.md table row. Add a contract assertion test that enforces the related-issue reference covers the full range of issues whose rules this eval protects.

**Tech Stack:** Python (contract assertion test), Markdown (INDEX.md)

**Design decision:** Comma-separated individual issue references (`#268, #269, #270, #271, #272`) are preferred over range notation (`#268-#272`) because:
1. Existing table entries use individual references
2. Substring matching in tests is unambiguous
3. No range parsing required by tooling or human readers

**Related issues coverage for `agentic-rag-technical-deep-dive-compounded-case.md`:**
- #268 — Terminology boundary & operational definition block
- #269 — Control-plane / workflow-system architecture add-on
- #270 — Benchmark comparability generalized to technical deep-dive
- #271 — Route-aware audit orchestrator
- #272 — Chinese technical source type mapping

Each of these introduces rules that the compounded eval case tests jointly. The INDEX.md must reference all five.

---

### Task 1: Add contract assertion test for INDEX.md related issue coverage

**Files:**
- Modify: `scripts/test_eval_index.py`
- Test target: `evals/INDEX.md`

- [x] **Step 1: Write the contract assertion test**

The test checks: for the `agentic-rag-technical-deep-dive-compounded-case` row in INDEX.md, the related issue column MUST contain individual references to `#268`, `#269`, `#270`, `#271`, `#272`.

Implementation uses split-based tokenization (comma/semicolon separated) to avoid substring false positives.

- [x] **Step 2: Run test to verify it FAILS before the change**

Run: `python3 scripts/test_eval_index.py`
Expected: FAIL on the new test (related issues column only has `#268`)
Actual: `FAIL  test_agentic_rag_compounded_case_related_issues: Missing #271 in related issues column: '#268'`

- [x] **Step 3: Update `evals/INDEX.md` line 33**

Change `#268` → `#268, #269, #270, #271, #272` in the related issues column.

```diff
- | ... | fail | #268 | Compounded-failure benchmark ...
+ | ... | fail | #268, #269, #270, #271, #272 | Compounded-failure benchmark ...
```

- [x] **Step 4: Run test to verify it PASSES after the change**

Run: `python3 scripts/test_eval_index.py`
Expected: All 7 tests PASS
Actual: All 7 tests PASS

- [x] **Step 5: Run full regression suite**

Run: `python3 scripts/test_eval_index.py && python3 scripts/test_validator_regression.py && python3 scripts/test_doc_eval_sync.py`
Expected: All 46 tests PASS
Actual: 7/7 + 28/28 + 11/11 = 46/46 PASS

- [x] **Step 6: Commit**

```bash
git add evals/INDEX.md scripts/test_eval_index.py docs/superpowers/plans/2026-06-13-eval-index-related-issues.md
git commit -m "test(eval-index): add contract assertion for agentic-rag compounded case related issues (#273)

Update INDEX.md related issue column from #268 to individual
#268, #269, #270, #271, #272 references to reflect the full range
of issues whose rules this eval protects:
terminology boundary (#268), control-plane add-on (#269), benchmark
comparability (#270), route-aware audit wrapper (#271), and source
type mapping (#272)."
```

---
