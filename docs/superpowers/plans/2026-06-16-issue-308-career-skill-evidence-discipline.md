# Issue #308 — Career/Skill Selection Proxy Evidence Discipline

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement this plan task-by-task. Steps use checkbox (`- [ ]`) for tracking.

**Goal:** Add evidence discipline for career/skill-selection constrained-choice reports, requiring default market/reader scope declaration, proxy indicator role labeling for common career data sources (TIOBE, LinkedIn, Glassdoor, etc.), and stronger source register claims typing.

**Architecture:** Three-layer change following the project's 6-layer architecture (method → audit → eval). Add content to `references/option-selection-and-shortlist-discipline.md` (method layer), update `checklists/option-selection-final-audit.md` (audit layer), create eval case (eval layer). All changes are extensions to existing constrained-choice framework — no new routes, no new reference files.

**Tech Stack:** Python property-based contract tests (following `tests/test_issue_NNN_contracts.py` pattern), Markdown reference/checklist/eval files.

**Contracts (Property-based invariants):**

C1: `references/option-selection-and-shortlist-discipline.md`
- MUST have a `### Default decision scope` subsection after `### Step 1: Clarify the decision architecture`
- MUST contain fields for: target reader, default market, decision goal, time window
- MUST contain a `### Common proxy indicators for career/skill selection` section after the decision scope section
- MUST list at least 5 proxy source types (TIOBE, Stack Overflow Survey, GitHub, LinkedIn/Indeed, salary pages)
- All existing sections MUST be preserved

C2: `checklists/option-selection-final-audit.md`
- MUST have a `### Career / skill selection sub-gate` section
- Section MUST have >= 3 checklist items
- Items MUST address: default scope declaration, proxy role labels, US-vs-global scope
- All existing sections MUST be preserved

C3: `evals/cases/career-skill-selection-proxy-discipline-case.md`
- File MUST exist
- MUST have standard sections: Goal, Prompt, Pass criteria, Failure signs
- MUST reference issue #308
- MUST have Pass / Conditional pass / Fail scoring

C4: `evals/INDEX.md`
- MUST have an entry for the new eval case
- Table format MUST be preserved (>10 columns)

C5: Cross-file invariants
- Checklist MUST reference `option-selection-and-shortlist-discipline.md` §Default decision scope
- All existing contract tests MUST still pass
- INDEX.md table structure must remain parseable

C6: Self-referential
- Test file MUST exist at `tests/test_issue_308_contracts.py`
- Must have tests for C1-C5

---

### Task 0: Write property-based contract tests (TDD RED phase)

**Files:**
- Create: `tests/test_issue_308_contracts.py`

Write the full contract test file with all C1-C6 tests. Run it — ALL MUST FAIL before any implementation.

### Task 1: Update references/option-selection-and-shortlist-discipline.md

**Files:**
- Modify: `references/option-selection-and-shortlist-discipline.md`

Add after `### Step 1: Clarify the decision architecture` (after line ~52):

1. `### 默认决策口径 — Default decision scope` — a new step-like section requiring reports to declare reader persona, geographic market, decision goal, and time window. Include a template block.
2. `### Common proxy indicators for career/skill selection` — document common proxy source types (TIOBE, SO Survey, GitHub, LinkedIn/Indeed, salary pages, package repos, official roadmaps) with their epistemic roles.

### Task 2: Update checklists/option-selection-final-audit.md

**Files:**
- Modify: `checklists/option-selection-final-audit.md`

Add new section `### Career / skill selection sub-gate` with >= 3 checklist items:
- Default reader persona and market scope declaration exists
- All proxy indicators have role labels
- US data not generalized to global without scope declaration

### Task 3: Create eval case

**Files:**
- Create: `evals/cases/career-skill-selection-proxy-discipline-case.md`

Standard eval case structure testing whether a learning-value constrained-choice report correctly handles proxy indicators for career/skill data.

### Task 4: Register eval in INDEX.md

**Files:**
- Modify: `evals/INDEX.md`

Add entry for the new eval case in alphabetical position.

### Task 5: Verify GREEN — All tests pass

Run `python tests/test_issue_308_contracts.py` — ALL MUST PASS.

### Task 6: Reflexion — self-review all changes

Verify:
- No existing content deleted in modified files
- Cross-references are valid in both directions
- Eval case follows project conventions
- All 5 tasks completed correctly
