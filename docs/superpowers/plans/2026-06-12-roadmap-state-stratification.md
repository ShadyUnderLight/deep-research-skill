# Technical Roadmap State Stratification Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use subagent-driven-development to implement this plan task-by-task.

**Goal:** Strengthen technical deep-dive roadmap state stratification — prevent reports from mixing stable/shipped, announced roadmap, experimental, deprecated, proposed, and rumored directions into one undifferentiated layer.

**Architecture:** Pure documentation changes to 4 discipline/checklist files, plus a property-based test suite that verifies cross-document consistency invariants.

**Tech Stack:** Python (property-based tests with hypothesis), Markdown

---

### Task 0: Write property-based test suite (TDD anchor)

**Files:**
- Create: `scripts/test_roadmap_state_stratification.py`

This test suite verifies cross-document consistency invariants that must hold after ALL 4 tasks complete. It runs as a standalone script (project convention, no pytest needed).

Invariants to test:

- **P0 (Table completeness)**: `references/technical-analysis-discipline.md` must contain a markdown table with column headers: `状态`, `含义`, `允许标签`, `写作要求`. The table must have ≥ 6 data rows.

- **P1 (Checklist coverage)**: For each status in the stratification table (extracted from technical-analysis-discipline.md), there is at least one corresponding checklist item in `checklists/technical-analysis-audit.md` that mentions that status (or its equivalent term).

- **P2 (No orphan checklist items)**: Every roadmap-related checklist item in technical-analysis-audit.md maps to a status in the stratification table.

- **P3 (Forward-looking technical section)**: `references/forward-looking-discipline.md` contains a section heading that mentions "technical roadmap" or "技术路线图".

- **P4 (Final-audit recall)**: `checklists/final-audit.md` has a recall item for technical deep-dive that mentions "roadmap" and "state" or "状态" and "stable shipped".

- **P5 (Hard-fail preservation)**: The existing hard-fail condition "roadmap evaluation treats announced features as shipped" in `technical-analysis-discipline.md` §Hard fail conditions is preserved.

- [ ] **Step 0.1: Install hypothesis** if not available

```bash
pip install hypothesis
```

- [ ] **Step 0.2: Write failing test suite**

Write the full test suite. The tests will fail now because the documents haven't been updated yet.

- [ ] **Step 0.3: Verify tests fail**

```bash
python scripts/test_roadmap_state_stratification.py
```
Expected: multiple failures (since docs haven't been updated yet).

- [ ] **Step 0.4: Commit**

```bash
git add scripts/test_roadmap_state_stratification.py
git commit -m "test: add property-based consistency tests for roadmap state stratification"
```

---

### Task 1: Update `references/technical-analysis-discipline.md`

**Files:**
- Modify: `references/technical-analysis-discipline.md` (§5 Technology roadmap evaluation)

- [ ] **Step 1.1: Add status stratification table**

After the 5 questions in §5 "Technology roadmap evaluation", append a new subsection with the status stratification table:

````md
### Roadmap/feature state stratification

When evaluating a technology roadmap, classify each claim into exactly one of these states.
Do not mix multiple states in the same claim.

| 状态 | 含义 | 允许标签 | 写作要求 |
|------|------|----------|----------|
| Stable / shipped | 当前稳定规范或已发布实现支持 | [CONF] | 标明版本和验证日期 |
| Experimental | 规范/扩展标明 experimental | [CONF] for status, [INFER] for maturity | 不得写成生产稳定能力 |
| Deprecated / superseded | 已弃用或被替代 | [CONF] for status | 必须说明迁移或风险 |
| Announced roadmap | 官方 roadmap / WG priority | [CONF] for announcement, not outcome | 必须写明不是已交付能力 |
| Proposed / SEP draft | 提案、草案、PR | [INFER] or scoped [CONF] for proposal existence | 不得当成 adopted spec |
| Rumored / community signal | 媒体、社区、issue、论坛 | [INFER]/[UNKN] | 必须标低置信或 discovery |
````

- [ ] **Step 1.2: Update Common failure modes**

Update failure mode 5 "Roadmap optimism" to also mention state mixing:

Old: `5. **Roadmap optimism**: treats announced features as shipped capabilities`

New: `5. **Roadmap optimism**: treats announced features as shipped capabilities, or mixes stable/shipped, experimental, deprecated, announced, proposed, and rumored states into one undifferentiated layer`

- [ ] **Step 1.3: Update Related references**

Add a cross-reference to the new stratification section from the forward-looking discipline reference line.

- [ ] **Step 1.4: Commit**

```bash
git add references/technical-analysis-discipline.md
git commit -m "docs(technical-analysis): add roadmap/feature state stratification table"
```

---

### Task 2: Update `checklists/technical-analysis-audit.md`

**Files:**
- Modify: `checklists/technical-analysis-audit.md`

- [ ] **Step 2.1: Expand roadmap checks**

Replace the existing single roadmap check (line 20) with granular checks:

Old:
```
- [ ] roadmap claims are separated into: announced / rumored / speculative
```

New:
```
- [ ] roadmap / version / feature-state claims 分为 stable shipped / experimental / deprecated / announced roadmap / proposed / rumored
- [ ] roadmap announcement 可标为 confirmed event，但未来能力结果不得标为 confirmed outcome
- [ ] deprecated / superseded feature 没有被当作当前推荐能力
- [ ] 如果报告引用官方 roadmap，必须说明是否 commitment，以及该说明对结论的影响
```

- [ ] **Step 2.2: Commit**

```bash
git add checklists/technical-analysis-audit.md
git commit -m "docs(audit): expand roadmap state checks from 3 to 6 categories"
```

---

### Task 3: Update `references/forward-looking-discipline.md`

**Files:**
- Modify: `references/forward-looking-discipline.md`

- [ ] **Step 3.1: Add technical roadmap adaptation section**

After the "Confidence framing" section (line 55), before "Assumption chains" (line 57), add:

```md
## Technical roadmap adaptation

The categories above (announced / estimated / inferred) are designed for financial forecasts and corporate guidance. Technology roadmaps require additional dimensions:

- **Feature lifecycle stage**: is the capability stable / experimental / deprecated / proposed?
- **Specification status**: is the spec adopted / draft / SEP / archived?
- **Implementation status**: is there a production implementation / reference implementation / proof-of-concept / none?

Apply these rules when writing about technical roadmaps:

1. **Confirmation scope is narrower for roadmap claims.** You can confirm that "the organization published a roadmap item," but you cannot confirm that "the roadmap outcome will be delivered." The former is an observed event; the latter is a forward-looking claim.
2. **Do not mix lifecycle stages.** A deprecated feature is not "available but older" — it is explicitly superseded. An experimental extension is not "early production" — it is not yet stable.
3. **Official roadmaps can confirm intent, not delivery.** Even when the source is the specification body itself, roadmap priority is not a commitment. Label accordingly.
4. **When in doubt, use the stratification table in `references/technical-analysis-discipline.md` §Roadmap/feature state stratification.**
```

- [ ] **Step 3.2: Update Relationship section**

In the "Relationship to other discipline files" section, add a reference:

Old:
```
- `checklists/final-audit.md` includes forward-looking gates for precision and estimate sourcing.
```

New:
```
- `references/technical-analysis-discipline.md` §Roadmap/feature state stratification provides a state classification table specific to technical roadmap claims.
- `checklists/final-audit.md` includes forward-looking gates for precision and estimate sourcing.
```

- [ ] **Step 3.3: Commit**

```bash
git add references/forward-looking-discipline.md
git commit -m "docs(forward-looking): add technical roadmap adaptation section"
```

---

### Task 4: Update `checklists/final-audit.md`

**Files:**
- Modify: `checklists/final-audit.md`

- [ ] **Step 4.1: Add roadmap state separation recall item**

In the Recall discipline section, after the existing technical deep-dive items (line 168), add:

```
- [ ] for technical deep-dive / architecture analysis tasks, roadmap / feature-state claims separate stable shipped capability from announced roadmap, experimental extension, deprecated feature, and speculative direction
```

- [ ] **Step 4.2: Commit**

```bash
git add checklists/final-audit.md
git commit -m "docs(final-audit): add roadmap state separation recall for technical deep-dive"
```

---

### Task 5: Run tests and self-review (Reflexion)

**Files:**
- Run: `scripts/test_roadmap_state_stratification.py`

- [ ] **Step 5.1: Run the property-based test suite**

```bash
python scripts/test_roadmap_state_stratification.py
```

Expected: ALL PASS

- [ ] **Step 5.2: Run existing tests**

```bash
python scripts/test_doc_eval_sync.py
```

Expected: ALL PASS (regression check)

- [ ] **Step 5.3: Final review**

Check:
- All 4 discipline files updated correctly
- Property-based tests cover all new content
- Existing test suite not broken
- Cross-references between files are consistent

- [ ] **Step 5.4: Final commit if needed**

```bash
git add -A
git commit -m "fixup: address self-review findings"
```
