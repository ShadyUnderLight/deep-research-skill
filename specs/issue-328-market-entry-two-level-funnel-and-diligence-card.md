# Market Entry: Two-Level Funnel & Country Diligence Card Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development. Steps use checkbox (`- [ ]`) syntax.

**Goal:** Add two-level decision funnel (regional screening → country competition → single beachhead), Country Diligence Card, recommendation-constraint consistency check, and sensitivity switching table to the Market Entry / Regional Expansion route.

**Architecture:** Pure markdown documentation changes to existing route definition, checklists, templates, and references plus new property-based contract tests and a regression eval case. No Python code changes except tests.

**Tech Stack:** Python property-based contract tests (`tests/test_issue_328_contracts.py`); markdown documentation.

---

## Design Analysis (CoT)

### Problem Analysis

The current Market Entry route has a single-stage country comparison. A report can select a region (e.g., Southeast Asia), compare a few countries within it, and pick a beachhead — all in one contiguous process. The issue identifies that:

1. **Region screening and country competition are different comparison levels.** Evidence that wins a region (macro TAM, growth rate, cultural distance) is not sufficient to pick a country within that region (localization depth, channel readiness, regulatory licensing, payment infrastructure).
2. **No standardized diligence format.** Each country's assessment is free-form prose; no consistent evidence-role labeling across candidates.
3. **No constraint consistency check.** A report can estimate 18-24 months to entry-ready but also require 6-month revenue verification, without the contradiction being flagged.
4. **Sensitivity analysis has no required format.** The route "attaches" sensitivity analysis but provides no template for what a switching-condition table looks like.

### Solution Architecture

Three independent phases (can be implemented and reviewed separately):

**Phase A — Constraint consistency + sensitivity switching table**
- Add 2 checklist items to `checklists/option-selection-final-audit.md` §Market-entry gate
- Add sensitivity switching table format to `references/decision-report-template.md` §Market-entry

**Phase B — Country Diligence Card**
- Add 10-field Country Diligence Card template to `references/decision-report-template.md` §Market-entry
- Add 2 checklist items to `checklists/option-selection-final-audit.md` §Market-entry gate

**Phase C — Two-level decision funnel**
- Restructure `ROUTING-MATRIX.md` §Market Entry visible artifact contract and hard fails
- Restructure `references/decision-report-template.md` §Market-entry structure to reflect two-stage process
- Add 2 heuristic questions to `references/option-selection-and-shortlist-discipline.md` §Market entry

**Phase D — Regression eval**
- New eval case `evals/cases/market-entry-two-level-funnel-and-diligence-case.md`
- New entry in `evals/INDEX.md`
- Existing evals unchanged (they test different gaps)

### Design Decisions

1. **All three phases share one test file** (`tests/test_issue_328_contracts.py`) for atomic pass/fail visibility.
2. **No changes to `scripts/audit_report.py`** — #325 already wired market-entry, no new routes needed.
3. **No changes to existing evals** — they test different market-entry failure modes (traceability, quantitative roles).
4. **Country Diligence Card added inside `decision-report-template.md`** (not a new file) to keep all market-entry templates in one place.
5. **Two-level funnel is a contract change, not a new route** — it upgrades the existing Market Entry route's artifact contract and hard fails.

---

## Files Changed

| File | Change | Phase |
|------|--------|-------|
| `checklists/option-selection-final-audit.md` | Add 4 new checklist items to market-entry gate | A, B |
| `references/decision-report-template.md` | Add Country Diligence Card sub-template, sensitivity switching table, restructure for two-level funnel | A, B, C |
| `ROUTING-MATRIX.md` | Market Entry section: upgrade artifact contract + hard fail for two-level funnel | C |
| `references/option-selection-and-shortlist-discipline.md` | Add 2 heuristic questions to market entry section | C |
| `tests/test_issue_328_contracts.py` | NEW: property-based contract tests for all phases | A, B, C |
| `evals/cases/market-entry-two-level-funnel-and-diligence-case.md` | NEW: regression eval case | D |
| `evals/INDEX.md` | Add entry for new eval case | D |

---

### Task A: Tests first — write contract tests for all phases

**Files:**
- Create: `tests/test_issue_328_contracts.py`

**Context:** The test file uses the same pattern as `tests/test_issue_327_contracts.py` and `tests/test_issue_308_contracts.py`: helper functions `read(path)`, `file_exists(path)`, `section_after(content, title)`, `re.search(...)`, `re.MULTILINE`. Tests use `assert`, no test framework. Run with `python tests/test_issue_328_contracts.py`.

The tests are property-based structural invariants: they verify that specific headings, table columns, checklist items, and keywords exist in the modified markdown files.

- [ ] **Step 1: Write C1-C7 failing tests**

```python
#!/usr/bin/env python3
"""
Property-based contract validation for issue #328.

Tests verify structural invariants for Market Entry two-level decision funnel,
Country Diligence Card, recommendation-constraint consistency, and sensitivity
switching table.

  C1: checklists/option-selection-final-audit.md
      - Constraint consistency checklist items exist
      - Sensitivity/switching table checklist item exists
      - Country Diligence Card checklist items exist
      - Existing content preserved
  C2: references/decision-report-template.md
      - Country Diligence Card template with 10 fields + evidence role + source
      - Sensitivity switching table format
      - Two-level funnel structure (region screening → country competition)
      - Existing content preserved
  C3: ROUTING-MATRIX.md
      - Two-level funnel in artifact contract
      - New hard fail for missing country competition
      - Existing content preserved
  C4: references/option-selection-and-shortlist-discipline.md
      - Two new heuristic questions for two-level funnel
      - Existing content preserved
  C5: evals/cases/ new file exists
      - File exists with standard eval structure
      - References issue #328
  C6: evals/INDEX.md
      - Entry for new eval case
      - Table format preserved
  C7: Cross-file invariants
      - No regression in existing contract tests
      - INDEX.md table parseable

Usage:
    python tests/test_issue_328_contracts.py

Expected BEFORE implementation (RED):
    ALL FAIL

Expected AFTER implementation (GREEN):
    ALL PASS
"""

import re
import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def read(path):
    with open(os.path.join(REPO_ROOT, path), "r") as f:
        return f.read()


def file_exists(path):
    return os.path.exists(os.path.join(REPO_ROOT, path))


def section_after(content, section_title):
    """Return content starting from a ## section title."""
    match = re.search(
        r'^#{2,3}\s+' + re.escape(section_title) + r'\s*$',
        content,
        re.MULTILINE
    )
    if not match:
        return None
    return content[match.start():]


# ═══════════════════════════════════════════════════════════════════
# C1: checklists/option-selection-final-audit.md
# ═══════════════════════════════════════════════════════════════════

CHECKLIST = "checklists/option-selection-final-audit.md"


def test_c1a_constraint_consistency_check():
    """C1a: Market-entry gate MUST have constraint-consistency check item."""
    content = read(CHECKLIST)
    assert re.search(
        r'recommendation.*constraint.*consistency|'
        r'GO.*budget.*team.*timeframe.*consistent|'
        r'推荐.*约束.*一致',
        content,
        re.IGNORECASE
    ), "Missing constraint-consistency checklist item"


def test_c1b_sensitivity_switching_table():
    """C1a: Market-entry gate MUST have sensitivity/switching table check."""
    content = read(CHECKLIST)
    assert re.search(
        r'sensitivity.*switch|切换.*表|what would change.*beachhead',
        content,
        re.IGNORECASE
    ), "Missing sensitivity/switching table checklist item"


def test_c1c_country_diligence_card():
    """C1c: Market-entry gate MUST have Country Diligence Card check."""
    content = read(CHECKLIST)
    assert re.search(
        r'Country.?Diligence.?Card|diligence.?card|diligence.*template|尽职调查',
        content,
        re.IGNORECASE
    ), "Missing Country Diligence Card checklist item"


def test_c1d_two_level_funnel():
    """C1d: Market-entry gate MUST have two-level funnel check."""
    content = read(CHECKLIST)
    assert re.search(
        r'region.*screen|region.*comparison|两级.*漏斗|区域.*初筛|区域.*复赛|funnel',
        content,
        re.IGNORECASE
    ), "Missing two-level funnel checklist item"


# ═══════════════════════════════════════════════════════════════════
# C2: references/decision-report-template.md
# ═══════════════════════════════════════════════════════════════════

TEMPLATE = "references/decision-report-template.md"


def test_c2a_country_diligence_card_template():
    """C2a: Template MUST contain Country Diligence Card with 10+ fields."""
    content = read(TEMPLATE)
    card_section = section_after(content, "Country Diligence Card")
    assert card_section is not None, "Missing Country Diligence Card section"

    required_fields = [
        "目标客户", "首笔收入", "本地化", "监管", "竞争",
        "渠道", "Entry motion", "成本与周期", "法律", "扩展",
    ]
    for field in required_fields:
        assert field in card_section, (
            f"Country Diligence Card missing field: {field}"
        )


def test_c2b_evidence_role_column():
    """C2b: Country Diligence Card MUST have evidence role column."""
    content = read(TEMPLATE)
    card_section = section_after(content, "Country Diligence Card")
    assert card_section is not None, "Missing Country Diligence Card section"
    assert re.search(
        r'Evidence.?role|observed|proxy|assumption|model.?output',
        card_section,
        re.IGNORECASE
    ), "Country Diligence Card missing evidence role column"


def test_c2c_sensitivity_switching_table_format():
    """C2c: Template MUST contain sensitivity switching table format."""
    content = read(TEMPLATE)
    assert re.search(
        r'sensitivity.*switch|切换|what would change.*beachhead|under what.*would.*switch',
        content,
        re.IGNORECASE
    ), "Missing sensitivity/switching table format"


def test_c2d_two_level_funnel_structure():
    """C2d: Template MUST indicate two-level funnel structure."""
    content = read(TEMPLATE)
    assert re.search(
        r'region.*screen|区域.*初筛|regional.?comparison|country.?competition|国家.*复赛|两级.*漏斗',
        content,
        re.IGNORECASE
    ), "Missing two-level funnel structure in market-entry template"


# ═══════════════════════════════════════════════════════════════════
# C3: ROUTING-MATRIX.md
# ═══════════════════════════════════════════════════════════════════

ROUTING = "ROUTING-MATRIX.md"


def test_c3a_two_level_funnel_contract():
    """C3a: Market Entry artifact contract MUST require two-level funnel."""
    content = read(ROUTING)
    market_entry_section = section_after(content, "Route: Market Entry / Regional Expansion")
    assert market_entry_section is not None, "Market Entry section not found"

    # Find the visible artifact contract subsection
    contract_match = re.search(
        r'### Visible artifact contract',
        market_entry_section
    )
    assert contract_match is not None, "Visible artifact contract not found in Market Entry"

    assert re.search(
        r'region.*screen|区域.*初筛|country.*competition|国家.*复赛|两级.*漏斗',
        market_entry_section[contract_match.start():],
        re.IGNORECASE
    ), "Two-level funnel missing from artifact contract"


def test_c3b_new_hard_fail():
    """C3b: Market Entry hard fail MUST include missing country-competition."""
    content = read(ROUTING)
    market_entry_section = section_after(content, "Route: Market Entry / Regional Expansion")
    assert market_entry_section is not None, "Market Entry section not found"

    hard_fail_match = re.search(
        r'### Hard fail',
        market_entry_section
    )
    assert hard_fail_match is not None, "Hard fail section not found in Market Entry"

    hard_fail_content = market_entry_section[hard_fail_match.start():]
    assert re.search(
        r'region.*screen.*skip|跳过.*区域.*s?c?r?e?e?n|country.*competition.*missing|missing.*country.*shortlist.*within|'
        r'胜出区域.*未.*国家.*复赛',
        hard_fail_content,
        re.IGNORECASE
    ) or re.search(
        r'第[二2]级.*未|未.*第[二2]级',
        hard_fail_content
    ), "Missing hard fail for skipping second-level country competition"


# ═══════════════════════════════════════════════════════════════════
# C4: references/option-selection-and-shortlist-discipline.md
# ═══════════════════════════════════════════════════════════════════

DISCIPLINE = "references/option-selection-and-shortlist-discipline.md"


def test_c4a_two_level_heuristic_questions():
    """C4a: Discipline MUST have region-screening heuristic questions."""
    content = read(DISCIPLINE)
    market_entry_questions = section_after(content, "When the task involves market entry / regional expansion / country prioritization")
    assert market_entry_questions is not None, "Market entry questions section not found"
    assert re.search(
        r'region.*screen|区域.*筛选|funnel.*level|两级.*漏斗',
        market_entry_questions,
        re.IGNORECASE
    ) or re.search(
        r'regional hub.*region|region.*beachhead.*first',
        market_entry_questions,
        re.IGNORECASE
    ), "Missing two-level funnel heuristic questions"


# ═══════════════════════════════════════════════════════════════════
# C5: New eval case
# ═══════════════════════════════════════════════════════════════════

EVAL_CASE = "evals/cases/market-entry-two-level-funnel-and-diligence-case.md"


def test_c5a_eval_case_exists():
    """C5a: Eval case file MUST exist."""
    assert file_exists(EVAL_CASE), f"Missing eval case: {EVAL_CASE}"


def test_c5b_standard_eval_structure():
    """C5b: Eval case MUST have Goal, Pass criteria, Failure signs."""
    content = read(EVAL_CASE)
    assert re.search(r'^##\s+Goal', content, re.MULTILINE), "Missing ## Goal"
    assert re.search(r'^##\s+Pass criteria', content, re.MULTILINE), "Missing ## Pass criteria"
    assert re.search(r'^##\s+Failure signs', content, re.MULTILINE), "Missing ## Failure signs"


def test_c5c_references_issue():
    """C5c: Eval case MUST reference issue #328."""
    content = read(EVAL_CASE)
    assert "#328" in content, "Eval case must reference issue #328"


# ═══════════════════════════════════════════════════════════════════
# C6: evals/INDEX.md
# ═══════════════════════════════════════════════════════════════════

INDEX = "evals/INDEX.md"


def test_c6a_index_entry_exists():
    """C6a: INDEX.md MUST have entry for new eval case."""
    content = read(INDEX)
    assert "market-entry-two-level-funnel-and-diligence-case" in content, \
        "Missing entry in evals/INDEX.md"


def test_c6b_index_table_parseable():
    """C6b: INDEX.md table MUST be parseable (same number of pipes per row)."""
    content = read(INDEX)
    # Find the table section (lines containing |)
    table_lines = [l for l in content.split('\n') if l.strip().startswith('|')]
    if not table_lines:
        return  # No table to check; pass
    pipe_counts = [l.count('|') for l in table_lines]
    header_count = max(pipe_counts[:3])  # header + separator + one data row
    for i, count in enumerate(pipe_counts):
        assert count == header_count or count == 0 or table_lines[i].strip() in ('', '| --- '), (
            f"INDEX.md table row {i+1} has {count} pipes, expected {header_count}. "
            f"Content: {table_lines[i][:80]}"
        )


# ═══════════════════════════════════════════════════════════════════
# C7: Cross-file invariants
# ═══════════════════════════════════════════════════════════════════

def test_c7_existing_contract_tests_still_pass():
    """C7: Existing contract tests MUST still pass (no regression)."""
    # Run a subset of related contract tests to check no regression
    existing_tests = [
        "tests/test_issue_327_contracts.py",
    ]
    for test_file in existing_tests:
        if not file_exists(test_file):
            continue
        result = os.system(
            f"{sys.executable} {os.path.join(REPO_ROOT, test_file)}"
        )
        assert result == 0, (
            f"Regression: {test_file} failed after changes"
        )


def test_c7_checklist_market_entry_section_preserved():
    """C7: Existing market-entry checklist items MUST still be present."""
    content = read(CHECKLIST)
    # Original 6 items must remain
    assert re.search(r'go.*not now.*pilot only|phased entry', content), \
        "Existing checklist item missing: go/not now/pilot only"
    assert re.search(r'regional hub.*first revenue beachhead.*later expansion', content), \
        "Existing checklist item missing: role separation"
    assert re.search(r'comparison unit.*free-form', content), \
        "Existing checklist item missing: comparison unit"
    assert re.search(r'hard gates.*budget.*product.*compliance', content), \
        "Existing checklist item missing: hard gates"


# ═══════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import inspect

    tests = [
        obj for name, obj in globals().items()
        if name.startswith("test_") and inspect.isfunction(obj)
    ]
    tests.sort(key=lambda f: f.__name__)

    passed = 0
    failed = 0

    for test_fn in tests:
        try:
            test_fn()
            print(f"  ✅ {test_fn.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"  ❌ {test_fn.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"  💥 {test_fn.__name__}: {e}")
            failed += 1

    print(f"\n{'=' * 50}")
    print(f"  Total: {passed + failed}  |  Passed: {passed}  |  Failed: {failed}")
    if failed:
        sys.exit(1)
```

---

### Task B: Implement checklist changes (Phase A + B)

**Files:**
- Modify: `checklists/option-selection-final-audit.md` (lines 67-74, after existing market-entry items)

- [ ] **Step 1: Run tests to confirm they fail (RED)**

Run: `python tests/test_issue_328_contracts.py`
Expected: FAIL — tests search for content not yet present

- [ ] **Step 2: Add 4 new checklist items to `checklists/option-selection-final-audit.md`**

Append after line 74 (`- [ ] the report names what would change the entry sequencing or turn `go` into `not now``):

```markdown
- [ ] **[Phase A] recommendation-constraint consistency** — GO / Pilot / Not Now labels are checked against the report's own budget, team, compliance readiness, and timeline estimates; if the report estimates 18–24 months to entry-ready but also requires 6-month revenue verification, the beachhead must not be labelled GO
- [ ] **[Phase A] sensitivity / switching table** — at least one sensitivity table or switching-condition description shows how changes in growth, ARPU, CAC, localization cost, partner deal cycle, or regulatory delay would change the beachhead country
- [ ] **[Phase B] Country Diligence Card** — each shortlisted country is evaluated through a consistent diligence card that includes: target customer/payer, first-revenue path, localization depth, regulatory/data status, competitive landscape, channel/partner readiness, entry motion, cost and timeline, legal/tax/IP, and expansion/exit scenario
- [ ] **[Phase B] two-level decision funnel** — the report explicitly separates regional screening (option universe → region shortlist) from country competition (winning region → country shortlist → single beachhead); winning region must compare at least 2–3 realistic country candidates or explain exclusivity
```

- [ ] **Step 3: Run tests to confirm they pass (GREEN)**

Run: `python tests/test_issue_328_contracts.py`
Expected: C1a, C1b, C1c, C1d, C7 market-entry preservation all PASS

---

### Task C: Implement decision-report-template.md changes (Phase A + B + C)

**Files:**
- Modify: `references/decision-report-template.md` — add Country Diligence Card sub-template, sensitivity switching table, two-level funnel restructuring

- [ ] **Step 1: Run tests to confirm relevant tests fail (RED)**

Run: `python tests/test_issue_328_contracts.py`
Expected: C2a, C2b, C2c, C2d FAIL

- [ ] **Step 2: Add Country Diligence Card sub-template**

Insert after the existing market-entry bullet list (after line 533 `- if the final memo is written in Chinese...`):

```markdown
### Country Diligence Card

Each shortlisted country should be evaluated through a consistent diligence card. This ensures that the comparison is driven by comparable evidence across candidates, not by free-form prose depth that varies by country.

| 字段 | 内容 | Evidence role | Source |
|------|------|--------------|--------|
| 目标客户 / 付费方 | | observed / proxy | [Sxx] |
| 首笔收入路径 | | assumption / model-output | |
| 本地化（语言 / 内容 / 支持） | | estimate | |
| 监管 / 数据合规 | | observed / current | |
| 竞争格局 | | observed / inferred | |
| 渠道 / 伙伴 readiness | | observed / unknown | |
| Entry motion | B2C / B2B / B2G / B2B2C | inference | |
| 成本与周期 | | estimate / assumption | |
| 法律 / 税务 / IP | | current fact | |
| 扩展 / 退出场景 | | scenario | |

Rules:
- Each row must have a non-empty "Evidence role" and "Source" when the Evidence role is observed / current fact.
- If a field cannot be filled, mark it explicitly as `unknown` or `not applicable` rather than leaving it blank.
- The "Source" column uses `[Sxx]` references to the Source Register.

### Sensitivity / Switching Table

When the recommendation depends on load-bearing numerical assumptions (growth rate, ARPU, CAC, localization cost, partner deal cycle, regulatory delay), include at least one sensitivity table that explicitly states which variable changes would switch the beachhead country.

| Variable | Current assumption | Change direction | New beachhead | Trigger threshold |
|----------|-------------------|-----------------|---------------|-------------------|
| Market growth rate | 12% CAGR | drops to 6% | Country B | <8% for 2 quarters |
| ARPU | $8.50 | falls to $5.00 | Country C (pilot) | <$6.00 |
| Localization cost | $150K | rises to $300K | Country D (hub-first) | >2x estimate |
| Partner deal cycle | 4 months | extends to 10 months | Country B (pilot only) | >8 months |

### Two-level decision funnel

For market-entry / regional-expansion tasks, the report structure should explicitly reflect two comparison levels:

1. **Regional screening**: Compare regions on macro dimensions — total addressable market, regulatory posture, execution distance, language/team requirements, business model fit, competitive pressure. Produce a ranked region shortlist.
2. **Country competition**: Within the winning region, compare specific countries on micro dimensions — 6–12 month first-revenue path, channel/partner readiness, localization depth and cost, data/education/industry licensing, payment/contract/tax/entity requirements, CAC/ARPU/payback cycle, pilot testability, exit cost.

**Restructured outline:**

1. Executive summary
2. What is the real decision?
3. Recommendation (at region and country levels)
4. Regional screening
   - Option universe and exclusions
   - Region-level comparison table
   - Ranked region shortlist
   - Winning region justification
5. Country competition (within winning region)
   - Country shortlist with unified comparison unit
   - Country Diligence Cards (one per candidate)
   - Ranked country list
6. Why the top beachhead wins
7. Why the runner-up remains credible
8. Why other countries lose
9. Hard gates and sequencing
10. Sensitivity / switching table
11. Regional hub / later expansion portfolio
12. Risk / what changes the decision
13. Sources
```

- [ ] **Step 3: Run tests to confirm they pass (GREEN)**

Run: `python tests/test_issue_328_contracts.py`
Expected: C2a, C2b, C2c, C2d all PASS

---

### Task D: Implement ROUTING-MATRIX.md changes (Phase C)

**Files:**
- Modify: `ROUTING-MATRIX.md` — Market Entry section artifact contract + hard fail

- [ ] **Step 1: Run tests to confirm C3a, C3b fail (RED)**

Run: `python tests/test_issue_328_contracts.py`
Expected: C3a, C3b FAIL

- [ ] **Step 2: Update artifact contract**

In ROUTING-MATRIX.md lines 210-222, change the Visible artifact contract. Add after line 218 (`- sequencing logic`):

```markdown
- two-level decision funnel: regional screening → country competition → single beachhead
  - winning region must compare at least 2-3 realistic country candidates or explain exclusivity
```

And add to the hub/beachhead block (after line 222 `- later expansion market`):

```markdown
- Country Diligence Cards with consistent evidence-role labeling across candidates
- sensitivity / switching table showing which variable changes would switch the beachhead
- recommendation-constraint consistency (GO labels compatible with report's own budget, timeline, and compliance estimates)
```

- [ ] **Step 3: Update hard fail**

In ROUTING-MATRIX.md lines 224-230, add after line 230 (`- collapses hub / beachhead / later expansion market into one vague "best market"`):

```markdown
- [NEW] skips the country-competition stage, jumping directly from regional winner to beachhead without evaluating 2-3 realistic country candidates within the winning region
- [NEW] country diligence varies inconsistently across candidates (different fields, different depth, no evidence-role labeling)
- [NEW] recommendation-constraint mismatch: the beachhead recommendation label (GO / Pilot Only / Not Now) contradicts the report's own estimated entry timeline, budget, team capacity, or compliance readiness
```

- [ ] **Step 4: Run tests to confirm they pass (GREEN)**

Run: `python tests/test_issue_328_contracts.py`
Expected: C3a, C3b PASS

---

### Task E: Implement option-selection-and-shortlist-discipline.md changes (Phase C)

**Files:**
- Modify: `references/option-selection-and-shortlist-discipline.md` — add 2 heuristic questions

- [ ] **Step 1: Run tests to confirm C4a fails (RED)**

Run: `python tests/test_issue_328_contracts.py`
Expected: C4a FAIL

- [ ] **Step 2: Add 2 heuristic questions**

After line 380 in `references/option-selection-and-shortlist-discipline.md` (after `- Does the report show why the top entry sequence wins and what would reverse that sequence?`), add:

```markdown
- Is the report applying a two-level decision funnel? That is, does it first screen regions at a macro level (TAM, regulatory posture, execution distance) before competing individual countries within the winning region on micro dimensions (localization depth, channel readiness, CAC/ARPU, licensing)?
- Does each shortlisted country have a consistent diligence card with explicit evidence-role labels (observed / proxy / assumption / model-output / current fact / scenario), or are some countries analyzed in free-form prose while others get structured evaluation?
```

- [ ] **Step 3: Run tests to confirm they pass (GREEN)**

Run: `python tests/test_issue_328_contracts.py`
Expected: C4a PASS

---

### Task F: Create regression eval case (Phase D)

**Files:**
- Create: `evals/cases/market-entry-two-level-funnel-and-diligence-case.md`
- Modify: `evals/INDEX.md`

- [ ] **Step 1: Run tests to confirm C5a, C5b, C5c, C6a fail (RED)**

Run: `python tests/test_issue_328_contracts.py`
Expected: C5a, C5b, C5c, C6a FAIL

- [ ] **Step 2: Create eval case**

```markdown
# Eval: Market Entry Two-Level Decision Funnel and Country Diligence Card Case

## Goal

Test whether a Market Entry / Regional Expansion report that correctly separates regional hub / first revenue beachhead / later expansion roles and uses a unified comparison unit can still **fail** when:

- **Two-level decision funnel absent** — the report jumps from regional winner directly to beachhead without evaluating 2-3 realistic country candidates within the winning region
- **Country Diligence Card absent** — countries are evaluated in free-form prose without consistent diligence fields or evidence-role labels
- **Recommendation-constraint mismatch** — the report's own estimates (e.g., 18-24 month entry timeline) contradict the recommendation label (e.g., GO with 6-month revenue requirement)
- **Sensitivity / switching table absent** — the beachhead recommendation depends on load-bearing assumptions (growth, ARPU, localization cost) that are not stress-tested with explicit switching conditions

This eval complements existing market-entry evals:
- `ai-edu-market-entry-sensitivity-and-route-intersection-case.md` — tests sensitivity, traceability, quantitative roles
- `ai-saas-market-entry-traceability-case.md` — tests traceability
- `nev-parts-europe-market-entry-quantitative-role-case.md` — tests quantitative role labeling

## Prompt

A Chinese AI education product company has completed initial market research and identified Southeast Asia as the preferred expansion region. Produce a market-entry decision memo that:

- identifies the specific beachhead country within Southeast Asia
- justifies why this country over other realistic candidates (minimum 2-3 within the region must be evaluated)
- uses a consistent diligence framework across all candidates
- labels GO / Pilot Only / Not Now for each country
- checks that the recommendation is consistent with estimated timeline, budget, and team constraints
- includes a sensitivity/switching table for load-bearing assumptions
- applies role labels (observed / proxy / assumption / model-output) to diligence numbers
- uses `[Sxx]` inline citations
- includes a complete 7-column Source Register

## What this eval is testing

- whether the report applies a two-level funnel: regional screening → country competition
- whether each candidate country uses a Country Diligence Card with consistent fields and evidence roles
- whether the recommendation label (GO/Pilot/Not Now) is checked against the report's own constraint estimates
- whether load-bearing assumptions have sensitivity/switching analysis

## Pass criteria

A passing answer should:

1. **Explicitly separate regional screening from country competition.** The report must show why SEA (not Japan, Middle East, or India) wins at the regional level, and then within SEA compete at least 2-3 specific countries.

2. **Use Country Diligence Card on each candidate.** Each country gets a diligence card with at least these fields: target customer/payer, first-revenue path, localization depth, regulatory/data status, competitive landscape, entry motion, cost and timeline. Each field has an evidence role label.

3. **Check recommendation-constraint consistency.** If the report says "entry requires 12-18 months to set up entity, hire team, localize product, and obtain licenses", a country labelled GO must not require revenue within 6 months. If the budget is $200K and estimated entry cost is $350K, no country can be labelled GO.

4. **Include sensitivity/switching table.** At least 3 variables tested with: current assumption, change direction, new beachhead, trigger threshold.

5. **Label numeric roles.** All key numbers (market size, ARPU, CAC, localization cost, timeline) carry observed/proxy/assumption/model-output labels.

## Failure signs

- ❌ Only one country evaluated within the winning region → hard-fail (two-level funnel absent)
- ❌ Country analysis is free-form prose without consistent diligence fields → hard-fail
- ❌ Recommendation label contradicts report's own estimates (timeline, budget, capacity) → hard-fail
- ❌ No sensitivity/switching table despite load-bearing assumptions → hard-fail
- ❌ Missing role labels on key numbers → hard-fail

## Scoring

- **Full Pass**: two-level funnel + diligence cards + constraint consistency + sensitivity table + role labels + traceability
- **Conditional Pass**: funnel and diligence present but sensitivity or constraint-consistency weak
- **Fail**: any hard-fail triggered

## Related evals

- `evals/cases/ai-edu-market-entry-sensitivity-and-route-intersection-case.md`
- `evals/cases/nev-parts-europe-market-entry-quantitative-role-case.md`
```

- [ ] **Step 3: Add entry to evals/INDEX.md**

Insert before the last line (`| `evals/cases/xiaohongshu-startup-evaluation-traceability-benchmark-case.md`...`):

```markdown
| `evals/cases/market-entry-two-level-funnel-and-diligence-case.md` | market-entry | constrained-choice | structural-completeness | option-selection final audit | active | two-level funnel and diligence card gates | fail | #328 | Guards market-entry reports against missing country-competition stage, absent diligence card, recommendation-constraint mismatch, and missing sensitivity switching. |
```

- [ ] **Step 4: Run full test suite**

Run: `python tests/test_issue_328_contracts.py`
Expected: ALL PASS

Run: `python tests/test_issue_327_contracts.py`
Expected: ALL PASS (no regression)

---

## Self-Review Checklist (Reflexion)

- [ ] All C1-C7 test groups pass
- [ ] Existing market-entry checklist items preserved (C7)
- [ ] Existing contract tests (`test_issue_327_contracts.py`) still pass (C7)
- [ ] Country Diligence Card has 10+ required fields (C2a)
- [ ] Evidence role column exists in diligence card (C2b)
- [ ] Sensitivity switching table format exists (C2c)
- [ ] Two-level funnel structure in template (C2d)
- [ ] Two-level funnel in ROUTING-MATRIX artifact contract (C3a)
- [ ] New hard fail for missing country competition (C3b)
- [ ] Heuristic questions in discipline reference (C4a)
- [ ] Eval case exists with standard structure (C5a, C5b)
- [ ] Eval case references #328 (C5c)
- [ ] INDEX.md entry exists (C6a)
- [ ] INDEX.md table parseable (C6b)
- [ ] No changes to files outside plan scope
- [ ] No changes to `scripts/audit_report.py`
- [ ] No changes to existing evals
