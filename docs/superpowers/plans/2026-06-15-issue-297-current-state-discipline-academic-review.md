# Spec: Academic-Review Current-State & Peer-Review Status Verification Discipline

## Type Contract

| Field | Value |
|-------|-------|
| Issue | #297 |
| Type | CHECKLIST_HARDENING + DOCUMENTATION |
| Route | Academic / Literature Review |
| Effort | Small (2 files, ~10 new checklist items) |
| Risk | Low (pure additions, no existing rule changed) |

## Scope

### In scope

1. **`checklists/academic-analysis-audit.md`**
   - Add `## Current-state discipline` section with:
     - Coverage window declaration requirement
     - Conclusion-binding requirement (window → conclusion alignment)
     - (Tier-1) Recent-paper peer-review verification requirement
   - Update `## Source labeling` section with recent-paper annotation note
   - Update `## Hard fail check` to reference new coverage window discipline

2. **`checklists/final-audit.md`**
   - Add recall discipline entry for coverage window and recent-paper verification in the academic review section (around line 186)

3. **Eval case updates (optional, low priority)**
   - Update `ai-agent-planning-academic-review-compounded-case.md` to reference new checklist items
   - Update `mllm-visual-reasoning-academic-review-narrow-fail-case.md` to reference new checklist items

### Not in scope

- No Python code changes (no lint/validator)
- No `ROUTING-MATRIX.md` changes (already requires current-state verification at L844)
- No `references/current-state-verification.md` changes (general-purpose, leave as-is for now)
- No `references/academic-evidence-hierarchy.md` changes (already has source labeling requirements)
- No new eval case files (existing eval cases already cover these patterns)
- No CI config changes

## Delivery Contract

### Must have

1. `academic-analysis-audit.md` contains 3+ new checklist items covering:
   - Coverage window declaration
   - Conclusion-binding to coverage window
   - (Tier-1) Recent-paper peer-review verification
2. `final-audit.md` recall discipline includes the new items
3. All existing tests pass unchanged
4. New checklist items match existing formatting conventions (Tier-1 / (非阻塞) / etc.)
5. Chinese/English bilingual consistency matches existing style

### Must NOT have

1. No breaking changes to existing rules
2. No markdown formatting errors
3. No duplication with existing rules
4. No scope creep into non-academic routes
5. No lint/validator changes

## Property-Based Invariants

1. **Structural completeness**: Every new checklist item is at the correct nesting level under its section heading
2. **Format consistency**: Each item uses `- [ ] ` prefix (normal) or `- [ ] （Tier-1）` prefix (blocking)
3. **No orphan references**: Every reference to another file/section resolves correctly
4. **Bilingual balance**: Chinese descriptions have English equivalents where meaning would otherwise be ambiguous
5. **No hard-fail conflict**: New items don't contradict existing hard-fail conditions
6. **Unique identifiers**: No two items request the same behavior under different names

## Acceptance Criteria

- [ ] `checklists/academic-analysis-audit.md` has a `## Current-state discipline` section
- [ ] Coverage window item exists and is specific (>12 months → either refresh or downgrade)
- [ ] Conclusion-binding item exists and requires explicit temporal qualifiers
- [ ] (Tier-1) recent-paper verification item exists and requires verification evidence
- [ ] `final-audit.md` recall list includes coverage window + recent-paper verification
- [ ] All existing tests pass: `python scripts/test_doc_eval_sync.py`
- [ ] All existing tests pass: `pytest scripts/ -x` for Python validator tests
- [ ] PR description accurately describes the change
