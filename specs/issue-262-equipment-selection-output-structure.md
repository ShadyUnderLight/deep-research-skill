# SDD: Equipment-Selection Cost Sensitivity, Decision Tree, Build-Ready Configuration

## Spec metadata

- Issue: #262
- Route: equipment-selection / procurement / home-server-planning
- Files to modify: `references/decision-report-template.md`, `checklists/final-audit.md`, `checklists/option-selection-final-audit.md`
- Files to add: `scripts/test_equipment_selection_contract.py` (contract tests), then add to CI

## Type Contracts

### Contract 1: `references/decision-report-template.md`

**Postcondition:** The equipment-selection section must contain these three subsections after the existing `Hardware ↔ system fit` content (current line ~315):

```
C1.1: "### Cost sensitivity table" subsection
  - MUST contain a table with columns: Active usage level, Local fixed cost, Local variable cost, Cloud variable cost, Break-even interpretation, Numeric role
  - MUST state that cost sensitivity must show the driving variable (e.g., monthly active GPU hours)
  - MUST state that all cost figures carry numeric role labels

C1.2: "### Decision tree" subsection
  - MUST state that equipment-selection tasks should include a decision tree
  - MUST state decision tree content: branching logic, change conditions, detail reference
  - MUST accept Mermaid or equivalent table format

C1.3: "### Build-ready configuration table" subsection
  - MUST describe a table with columns: Scenario, Recommended stack, Included cost items, Excluded/user-supplied items, Operating burden, Expansion path
  - MUST state minimum fields: hardware, software/OS, included/excluded budget, operating burden, expansion
```

### Contract 2: `checklists/final-audit.md`

**Postcondition:** The equipment-selection recall group (currently lines 148-156) must gain 3 new items:

```
C2.1: Cost sensitivity variables check
  - MUST mention: monthly active GPU hours, daily usage, storage/network/power, depreciation/residual
  - MUST require these drive the break-even analysis

C2.2: Budget inclusion/exclusion hard-fail
  - MUST require explicit what-is-included and what-is-excluded
  - MUST flag bare "约 ¥X" without scope as hard-fail

C2.3: Build-ready configuration table check
  - MUST require a build-ready table when hardware is core output
  - MUST require fields: hardware, software, included/excluded, operating burden, expansion
```

### Contract 3: `checklists/option-selection-final-audit.md`

**Postcondition:** After line 95, gain 1 new item:

```
C3.1: Build-ready friction check
  - MUST trigger when physical hardware or build stack is core output
  - MUST surface hidden friction (power, noise, maintenance, backup)
  - MUST surface build-ready components
```

### Contract 4: `scripts/test_equipment_selection_contract.py` (new file)

Must contain property-based tests that verify:

```
C4.1: Table column count consistency for all equipment-selection template tables
  - For each pipe-delimited table in the equipment-selection section, header column count == data row column count

C4.2: All three new subsections exist in decision-report-template.md
  - "Cost sensitivity table", "Decision tree", "Build-ready configuration table" headers present

C4.3: All new audit items are present in final-audit.md
  - Needles: "cost sensitivity", "budget assumptions", "build-ready configuration table"

C4.4: New option-selection audit item is present
  - Needle: "build-ready"
```

### Contract 5: CI Integration

```
C5.1: .github/workflows/ci.yml must run the new contract test
  - Add `python3 scripts/test_equipment_selection_contract.py` to the quick job
```

## Property-Based Tests

For markdown templates, the following properties must hold:

| Property | Files | Description |
|---|---|---|
| P1. Table column consistency | `decision-report-template.md` | All pipe-delimited tables in the equipment-selection section have matching header/data column counts |
| P2. Section header presence | `decision-report-template.md` | Specific `###` headers exist in the equipment-selection zone |
| P3. Needle presence | `final-audit.md`, `option-selection-final-audit.md` | Required keywords exist in correct file zone |
| P4. No orphan references | All checklist files | Every checklist item referencing a template section has a corresponding section |

## Verification strategy

```
RED:   Run contract tests on current code → all fail (content missing)
GREEN: Implement template/checklist changes
       Run contract tests → all pass
REFACTOR: Run full CI test suite → no regressions
```
