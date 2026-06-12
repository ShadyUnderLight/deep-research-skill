# CoT: Equipment-Selection Cost Sensitivity, Decision Tree, Build-Ready Config

## Design Decisions

### D1. Placement in decision-report-template.md

The current equipment-selection section occupies lines 277-316. The document then continues with a market-entry section at line 318.

**Decision:** Insert three new subsections right after line 316 (after the `In these equipment-selection / procurement cases:` bullet block, before "For market-entry / regional-expansion...").

**Rationale:**
- Keeps all equipment-selection content contiguous
- Preserves the document's route-by-route ordering
- No need to renumber existing sections (the doc uses ### headers, not numbers)

### D2. Table column design

**Cost sensitivity table:**
- Use 6 columns matching the issue's design: `Active usage level | Local fixed cost | Local variable cost | Cloud variable cost | Break-even interpretation | Numeric role`
- The "Numeric role" column is part of the table spec, not a footnote — this forces explicit labeling per row
- The example rows show 3 utilization levels (40/120/240 GPU h/month) to demonstrate the pattern
- The description text clarifies the independent variable (e.g., monthly active GPU hours) can be adapted

**Build-ready configuration table:**
- Use 6 columns: `Scenario | Recommended stack | Included cost items | Excluded / user-supplied items | Operating burden | Expansion path`
- The description clarifies minimum fields: hardware components, software/OS, included/excluded budget, operating burden, expansion
- The example row shows the RTX 5090 scenario as a concrete illustration

### D3. Decision tree format

- Include a Mermaid flowchart example (as suggested in the issue)
- Accept alternative formats ("Mermaid 或等价表格")
- The description clarifies that decision trees should show: branching logic, change conditions, and detail reference
- Cross-link to `references/decision-tree-method.md` for detailed methodology

### D4. Audit item design for final-audit.md

The existing equipment-selection recall items (lines 148-156) follow this template:
```
- [ ] for equipment-selection / procurement / home-server-planning tasks, [specific behavior required]
```

New items will follow the same pattern, appended after the last existing equipment-selection item (line 156).

Item 1: Cost sensitivity variables are explicitly shown and drive break-even analysis
Item 2: Budget assumptions declare inclusion/exclusion (hard-fail for bare totals without scope)
Item 3: Build-ready configuration table is present with required fields

### D5. Audit item design for option-selection-final-audit.md

The existing item at line 93 covers hidden friction in procurement. The new item (line 94) extends this to require build-ready components.

### D6. Cross-references

- decision-report-template.md: link to `references/decision-tree-method.md` in the decision tree subsection
- final-audit.md: implicit reference to the template's cost sensitivity table spec
- No changes needed to ROUTING-MATRIX.md, decision-tree-method.md, or quantitative-role-labeling.md

### D7. Style consistency

- Use `[查看 references/decision-tree-method.md]` format for cross-references (matching existing pattern)
- Table examples use `...` placeholders (matching existing template style)
- Description text uses imperative tone ("Include", "Do not", "State")
- All new content is in English, matching the existing document language
