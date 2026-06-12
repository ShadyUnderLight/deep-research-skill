# Architecture Comparison: Comparator Roles & Load-Bearing Trade-offs Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add comparator role classification, enriched comparison table template, and load-bearing trade-off interpretation requirements to technical-deep-dive architecture comparison rules.

**Architecture:** Four independent but sequential changes: (1) eval case first (TDD — spec as test), (2) `technical-analysis-discipline.md` — add comparator roles + table template + output structure, (3) `technical-analysis-audit.md` — add checklist items, (4) `ROUTING-MATRIX.md` — update visible artifact contract. Then update `evals/INDEX.md` and Reflexion review.

**Tech Stack:** Markdown documentation only.

---

### Task 1: Write the Eval Case (TDD — test-first)

**Files:**
- Create: `evals/cases/mcp-technical-deep-dive-architecture-comparison-role-case.md`

- [ ] **Step 1: Create eval case file with full spec**

Write MCP architecture comparison eval case that tests:

1. **Negative example** (should fail): MCP vs A2A vs Function Calling as flat feature list, no comparator roles, no load-bearing interpretation
2. **Positive example** (should pass): MCP vs LSP vs A2A vs OpenAPI organized by comparator roles (design ancestor / complement / alternative tool-description approach), with load-bearing trade-off interpretation table

Eval should verify:
- [ ] each comparator has a visible role
- [ ] comparison table includes role column
- [ ] after-table interpretation identifies load-bearing dimensions
- [ ] exclusion reason for common but irrelevant comparators
- [ ] recommendation states reversal conditions

- [ ] **Step 2: Validate eval case structure**

Read the file, confirm it follows existing eval case conventions (Goal, Prompt, Pass criteria, Failure signs, Route activation criteria, Reviewer checklist, Related evals sections).

---

### Task 2: Update `technical-analysis-discipline.md`

**Files:**
- Modify: `references/technical-analysis-discipline.md`

- [ ] **Step 1: Add comparator role requirement to §Architecture comparison (lines 36-41)**

Insert between "What are the candidate architectures?" and "What are the comparison dimensions?":
```md
- What is each candidate's role in the comparison? (direct substitute / complement / lower-level primitive / higher-level runtime or platform / historical or design ancestor / unsuitable comparator with exclusion rationale)
```

Insert after "Which architecture wins under which constraints?":
```md
- Which comparison dimensions are load-bearing vs background information?
- Under what conditions would the recommendation reverse?
```

- [ ] **Step 2: Add enriched comparison table template after §Comparison dimensions table (line 124)**

Append new section after the dimensions table:

````md
### Architecture comparison table template

When presenting an architecture comparison table, use this enriched template that distinguishes comparator roles:

```md
| 方案 | 比较角色 | 解决的问题 | 成熟度 | 关键优势 | 关键代价 | 最适合场景 | 不适合场景 | 核心权衡维度 |
|------|----------|------------|--------|----------|----------|------------|------------|--------------|
```

The table should be followed by a short interpretation:

- **Load-bearing dimensions:** which dimensions drive the final recommendation (and why the others are background)
- **Reversal conditions:** what specific change (ecosystem maturity, performance threshold, cost constraint) would change the recommendation
````

- [ ] **Step 3: Update §Output structure — For architecture comparison (lines 151-156)**

Append to the architecture comparison bullet list:
```md
- Comparator roles with rationale for each candidate's inclusion
- Load-bearing trade-off interpretation after the comparison table
```

---

### Task 3: Update `technical-analysis-audit.md`

**Files:**
- Modify: `checklists/technical-analysis-audit.md`

- [ ] **Step 1: Enhance §Comparison structure (lines 43-50)**

Add checklist items after existing items:

```md
- [ ] each comparator's role is visible (substitute / complement / ancestor / excluded with reason)
- [ ] comparison table is followed by a trade-off interpretation identifying load-bearing dimensions
- [ ] if a common comparator was excluded, the exclusion reason is stated
```

Modify existing item "the recommendation explains which dimensions are load-bearing":
```md
- [ ] the recommendation explains which dimensions are load-bearing and what conditions would reverse the conclusion
```

---

### Task 4: Update `ROUTING-MATRIX.md`

**Files:**
- Modify: `ROUTING-MATRIX.md`

- [ ] **Step 1: Update Visible artifact contract for architecture comparison (line 597)**

Add a sentence to the architecture comparison bullet in the contract:

```md
- **For architecture comparison:** candidate architectures with comparator roles, explicit comparison dimensions, dimension-by-dimension analysis, trade-off summary, conditional recommendation; architecture comparison should show comparator roles and identify load-bearing trade-offs, not only feature differences
```

---

### Task 5: Update `evals/INDEX.md`

**Files:**
- Modify: `evals/INDEX.md`

- [ ] **Step 1: Add new eval case entry**

Insert a row in the eval index table for the new case:
```md
| `evals/cases/mcp-technical-deep-dive-architecture-comparison-role-case.md` | technical-deep-dive | source-traceability | architecture-comparison-role | technical-analysis audit | active | comparator role and load-bearing trade-off gates | manual-review | issue #245 | Guards architecture comparison against flat feature-list output without comparator roles or load-bearing interpretation. |
```

---

### Task 6: Reflexion — Self-Review & Regression Check

- [ ] **Step 1: Verify all changes are coherent**

Read all modified files and confirm:
- Comparator role concept is consistently named across all files
- New checklist items match what the discipline file requires
- Eval case pass/fail criteria match the discipline requirements
- No existing eval cases are broken by new rules (they shouldn't be — rules are additive)

- [ ] **Step 2: Verify no files were accidentally changed**

Run `git diff --stat` and confirm only the intended files were modified.

- [ ] **Step 3: Commit and prepare for PR**

```bash
git add docs/superpowers/plans/2026-06-12-architecture-comparison-roles.md
git add evals/cases/mcp-technical-deep-dive-architecture-comparison-role-case.md
git add references/technical-analysis-discipline.md
git add checklists/technical-analysis-audit.md
git add ROUTING-MATRIX.md
git add evals/INDEX.md
git commit -m "feat(architecture-comparison): add comparator roles and load-bearing trade-off requirements (#245)"
```
