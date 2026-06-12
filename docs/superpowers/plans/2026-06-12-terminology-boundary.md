# Terminology Boundary & Operational Definition Block Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add terminology-boundary / operational-definition requirements to Technical Deep-dive route, addressing Issue #268

**Architecture:** All changes are documentation-only (markdown files). No code changes. Each file has a clear structural contract verified by a validation script.

**Tech Stack:** Markdown, with `scripts/validate-docs-structure.sh` for property-based structural validation.

**Spec Source:** Issue #268 — https://github.com/ShadyUnderLight/deep-research-skill/issues/268

---

## Type Contracts (文件结构契约)

Each modified file MUST satisfy:

### Contract A: `references/technical-analysis-discipline.md`
- §Core questions MUST have a new sub-section "### 6. Definition-sensitive concepts（定义敏感概念）" with ≥3 bullet questions
- Each bullet MUST be a full question (not a fragment)

### Contract B: `references/report-template.md`
- §Technical deep-dive opening section MUST contain a terminology-boundary template table
- Table MUST have 5 columns: 概念 / 原始/严格定义 / 当代工程定义 / 本报告采用定义 / 排除边界
- MUST include a short note explaining the table is optional but recommended for definition-sensitive topics
- MUST include an "操作性定义" line template

### Contract C: `checklists/technical-analysis-audit.md`
- MUST add ≥2 new checklist items in the Comparison structure section
- One item MUST check: definition-sensitive concepts have scope/definition clarified
- One item MUST check: operational definition vs strict definition distinguished
- Each item MUST use `- [ ]` format

### Contract D: `evals/cases/agentic-rag-technical-deep-dive-compounded-case.md`
- MUST add 1-2 lines in Reviewer checklist section checking terminology boundary
- MUST NOT modify pass/fail criteria (this is forward-looking, not blocking)

---

## Task 1: `references/technical-analysis-discipline.md` — Core questions

**Files:**
- Modify: `references/technical-analysis-discipline.md` (after line 64, before "### 3. Patent analysis")

- [ ] **Step 1: SDD — Write structural contract test**

Write property-based validation: `scripts/validate-docs-structure.sh` must check:
- `technical-analysis-discipline.md` contains "### 6. Definition-sensitive concepts"

- [ ] **Step 2: CoT — Design analysis**

The new section needs to ask:
1. Is the core concept definition-sensitive? (multiple competing/academic vs engineering definitions?)
2. Does the author need to distinguish original academic definition from current engineering usage?
3. Could the chosen definition affect the comparison conclusions?
4. What concepts are commonly confused with the target concept but should not be conflated?

These questions should appear as a new numbered subsection #6 in the Core questions, following the existing pattern.

- [ ] **Step 3: TDD — Run validation, verify it fails**

```bash
bash scripts/validate-docs-structure.sh
```
Expected: FAIL — "technical-analysis-discipline.md" missing "### 6. Definition-sensitive concepts"

- [ ] **Step 4: Code — Implement the change**

Edit `references/technical-analysis-discipline.md`:
- Insert new §6 "Definition-sensitive concepts" after the "### 5. Technology roadmap evaluation" section (after line 63)
- Add 4 bullet questions following the same formatting pattern as existing sections

- [ ] **Step 5: Reflexion — Run validation, verify passes**

```bash
bash scripts/validate-docs-structure.sh
```
Expected: PASS for contract A

- [ ] **Step 6: Manual review**

Read the diff. Confirm:
- Questions are genuinely useful, not filler
- Formatting matches existing sections (same indentation, dash style, spacing)
- No typos or broken markdown

---

## Task 2: `references/report-template.md` — Template table

**Files:**
- Modify: `references/report-template.md` (after line ~182, in the default structure, after "### 4. Detailed analysis")

- [ ] **Step 1: SDD — Write structural contract test**

Add to `scripts/validate-docs-structure.sh`:
- `report-template.md` contains "| 概念 | 原始/严格定义 | 当代工程定义 | 本报告采用定义 | 排除边界 |"

- [ ] **Step 2: CoT — Design analysis**

The template table placement:
- Should appear in the Technical deep-dive opening section, NOT in the generic default structure
- Best placement: after line 171 (end of "### 4. Detailed analysis" → "Technical deep-dive: terminology boundary") alternative section
- Actually, better: add as a new visible block under "### 4. Detailed analysis" subsection for technical work, or create a dedicated "术语边界" section before detailed analysis for technical-deep-dive cases

Looking at the current template structure:
- §4 Detailed analysis says "Organize by task type. Examples: ... technical: feasibility, constraints, trade-offs, implementation needs"
- The best place is after line 159, adding a note: "For definition-sensitive technical topics, include a terminology boundary block before detailed analysis:"

- [ ] **Step 3: TDD — Run validation, verify it fails

```bash
bash scripts/validate-docs-structure.sh
```
Expected: FAIL — "report-template.md" missing the table header with 5 columns

- [ ] **Step 4: Code — Implement the change**

Edit `references/report-template.md`:
- After line 159 (end of bullet list in "### 4. Detailed analysis"), add:
  - A sub-note about definition-sensitive topics
  - The template table
  - The operational definition line template

- [ ] **Step 5: Reflexion — Run validation, verify passes

```bash
bash scripts/validate-docs-structure.sh
```
Expected: PASS for contract B

- [ ] **Step 6: Manual review**

Confirm table format renders correctly (no pipe alignment issues), note text is clear

---

## Task 3: `checklists/technical-analysis-audit.md` — Checklist items

**Files:**
- Modify: `checklists/technical-analysis-audit.md` (Comparison structure section, after line ~39)

- [ ] **Step 1: SDD — Write structural contract test

Add to `scripts/validate-docs-structure.sh`:
- `technical-analysis-audit.md` contains "definition-sensitive concepts" and "operational definition"

- [ ] **Step 2: CoT — Design analysis**

New checklist items:
1. `[ ]` definition-sensitive concepts are clarified before comparison (原始定义 vs 工程定义 vs 本文采用定义)
2. `[ ]` if a concept is not a strict single-paper definition, the report labels it as operational definition or engineering paradigm synthesis
3. `[ ]` （非阻塞）related but distinct concepts have explicit exclusion boundaries or comparator roles

Item 3 should be non-blocking (marked 非阻塞) following existing pattern.

- [ ] **Step 3: TDD — Run validation, verify it fails

```bash
bash scripts/validate-docs-structure.sh
```
Expected: FAIL — audit file missing required items

- [ ] **Step 4: Code — Implement the change

Insert 3 new items in the Comparison structure section (after line 39)

- [ ] **Step 5: Reflexion — Run validation, verify passes

Expected: PASS for contract C

- [ ] **Step 6: Manual review**

Confirm items don't duplicate existing items, format matches

---

## Task 4: `evals/cases/agentic-rag-technical-deep-dive-compounded-case.md` — Eval update

**Files:**
- Modify: `evals/cases/agentic-rag-technical-deep-dive-compounded-case.md` (Reviewer checklist section)

- [ ] **Step 1: SDD — Write structural contract test

Add to `scripts/validate-docs-structure.sh`:
- `agentic-rag-technical-deep-dive-compounded-case.md` contains "terminology" or "definition" in reviewer checklist

- [ ] **Step 2: CoT — Design analysis

The eval already tests compounded failures (register, roles, vendor claims, benchmark, self-assessment). Adding terminology boundary as a forward-looking check in reviewer checklist is appropriate; it should NOT be a pass/fail criterion for this eval since the original report didn't have this requirement.

- [ ] **Step 3: TDD — Run validation, verify it fails

```bash
bash scripts/validate-docs-structure.sh
```
Expected: FAIL — eval file missing terminology check

- [ ] **Step 4: Code — Implement the change

Add 1 line in Reviewer checklist: "- Are definition-sensitive concepts clarified before architecture comparison (原始定义 vs 工程定义 vs 本文采用定义)?"

- [ ] **Step 5: Reflexion — Run validation, verify passes

Expected: PASS for contract D

- [ ] **Step 6: Manual review

Confirm no pass/fail criteria were modified

---

## Cross-Reference Verification

After all tasks:

- [ ] All `references/` cross-references are valid (no broken links to nonexistent sections)
- [ ] `ROUTING-MATRIX.md` was NOT modified (out of scope)
- [ ] No other routes' checklists were modified (out of scope)
- [ ] All new items use the same formatting conventions as existing content
- [ ] No self-assessment / audit logic was changed (out of scope)

---

## Verification

- [ ] `bash scripts/validate-docs-structure.sh` passes all 4 contracts
- [ ] `git diff --stat` shows exactly 4 files modified (or 4 + 1 new script)
- [ ] No unintended files changed
