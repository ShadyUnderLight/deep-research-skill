# Failure Taxonomy for `evals/`

This document groups the current eval set into recurring failure families.

The goal is not to replace case-specific evals. The goal is to make it easier to:

- see which failures are truly recurring
- decide whether a new issue needs a new rule, a new checklist gate, or only a new case
- avoid treating every new report failure as an isolated incident
- identify when the next improvement should be structural rather than prose-only

---

## How to use this taxonomy

When a new failure appears, classify it in this order:

1. **Which family is it?**
2. **Is it a missing rule, a missing trigger, or an execution failure?**
3. **Should the fix land in `references/`, `checklists/`, `SKILL.md`, or a new meta-eval?**
4. **Does the new case add a genuinely new failure mode, or only another instance of an existing family?**

Use this taxonomy to prevent overfitting the skill to one report.

---

## Family A — Current-State and Time-Layer Discipline

### Core failure pattern
The report does not cleanly separate:

- historical facts
- current verified state
- forward-looking expectations

Typical symptom: the model uses stale but familiar knowledge as if it were current, or mixes current position with older milestones.

### Why this matters
This is one of the highest-severity failure families because it directly breaks trust in company, product, and market research.

### Typical failure forms
- stale product generation presented as current
- IPO filing / pre-IPO language frozen as current status
- ranking or market-position claim written in present tense without time basis
- valuation snapshot missing in listed-company research
- reported financials, market snapshot, and estimates blended into one narrative

### Existing evals in this family
- `evals/cases/freshness-xiaomi-case.md`
- `evals/cases/apple-product-and-valuation-case.md`
- `evals/cases/moore-threads-listing-status-case.md`
- `evals/cases/ranking-and-current-claims-xiaomi-update-case.md`
- `evals/cases/finance-and-market-share-cambricon-case.md` (partial overlap)
- `evals/cases/minimax-company-report-case.md` (partial overlap)

### Existing rule/checklist coverage
- `references/current-state-verification.md`
- `references/finance-date-discipline.md`
- `references/ranking-and-current-claims-discipline.md`
- `references/corporate-status-and-listing-state-discipline.md`
- `checklists/listed-company-report.md`

### What this family suggests structurally
The repo already has rules for this family. The remaining problem is often not missing guidance but **failure to trigger the correct gate**.

### Priority improvement direction
- strengthen trigger routing for listed-company, current-position, ranking, and fast-moving product tasks
- make required current-snapshot fields more visible in delivery-time audit
- add meta-evals for whether the right checklist was actually activated

---

## Family B — Source Traceability and Evidence Weighting

### Core failure pattern
The report has sources, but the reader still cannot audit which source supports which claim.

Typical symptom: a source list exists, yet key prices, dates, rankings, analyst targets, and strong qualitative claims have no claim-level traceability.

### Why this matters
Once research becomes decision-relevant, bibliography-only sourcing is not enough. The reader must be able to trace major claims to specific evidence and distinguish primary facts from inference.

### Typical failure forms
- no inline source ids for important claims
- source list exists, but no structured source register
- specific numbers or dates appear without visible support
- primary, secondary, inferred, and unconfirmed claims treated with equal weight
- inferred claims appear without reasoning chain
- current-state claim supported only by stale secondary reporting

### Existing evals in this family
- `evals/cases/source-traceability-moore-threads-case.md`
- `evals/cases/apple-product-roadmap-and-investment-case.md`
- `evals/cases/minimax-company-report-case.md`
- `evals/comparative-distillation/byd-gpt-vs-minimax-comparative-distillation.md` (distillation signal)

### Existing rule/checklist coverage
- `references/source-traceability-and-claim-citation.md`
- `references/source-quality.md`
- `references/claim-matrix.md`
- `checklists/source-traceability.md`
- `checklists/final-audit.md`

### What this family suggests structurally
The main gap is shifting from "source awareness" to **auditable claim-level evidence mapping**.

### Priority improvement direction
- enforce inline citation discipline more explicitly in report templates and checklists
- add execution checks that confirm traceability exists in the body, not just the appendix
- create clearer rules for when an inferred claim needs a reasoning chain vs. when it should remain unresolved

---

## Family C — Forward-Looking Claim Discipline

### Core failure pattern
The report makes predictions, estimates, or roadmap statements without enough structure around assumptions, source basis, and failure conditions.

Typical symptom: words like "预计", "target", "likely", "consensus", or launch-timeline claims appear, but the report does not make clear whether they come from company guidance, analyst expectations, media speculation, or internal inference.

### Why this matters
Forward-looking claims are easy to write and easy to overstate. They create false confidence if source type and assumption chain are hidden.

### Typical failure forms
- prediction without named source
- forecast with no assumption chain
- consensus number with no source or date
- roadmap claim that does not distinguish announced vs shipped vs rumored
- target price or support/resistance claim without method
- uncertain forward statement not visibly labeled as uncertain

### Existing evals in this family
- `evals/cases/apple-product-roadmap-and-investment-case.md`
- `evals/cases/byd-report-format-discipline-case.md`
- `evals/cases/hnb-industry-report-table-design-case.md`
- `evals/comparative-distillation/byd-gpt-vs-minimax-comparative-distillation.md` (distillation signal)

### Existing rule/checklist coverage
- `checklists/forward-looking-claims.md`
- `references/finance-date-discipline.md`
- `checklists/final-audit.md`

### What this family suggests structurally
The rule exists, but forward-looking discipline still leaks at output time. This is a classic **execution-stability** problem.

### Priority improvement direction
- add stronger delivery-time checks for every forecast word or estimate phrase
- explicitly distinguish guidance / consensus / media speculation / model inference in templates
- consider a dedicated eval family tag for roadmap and estimate-heavy tasks

---

## Family D — Output Structure and Information Density

### Core failure pattern
The report looks organized, but the structure does not help the reader absorb or use the analysis efficiently.

Typical symptom: bullet walls, table walls, overstuffed summary bullets, or cells that contain several loosely related ideas instead of one clear fact.

### Why this matters
This family does not always create factual errors, but it reduces report usability and hides the most important conclusions.

### Typical failure forms
- exec summary bullet contains multiple insights and too many numbers
- table is too wide to read or too shallow to justify width
- one cell contains multiple sub-points without clear separation
- markdown structure works poorly with PDF rendering constraints
- report has headings and formatting, but not effective reading flow

### Existing evals in this family
- `evals/cases/byd-report-format-discipline-case.md`
- `evals/cases/hnb-industry-report-table-design-case.md`
- `evals/cases/minimax-company-report-case.md` (partial overlap due to structural incompleteness)

### Existing rule/checklist coverage
- `references/report-template.md`
- `checklists/final-audit.md`

### What this family suggests structurally
The repo has started to move from general style guidance toward **render-aware structural discipline**. That should continue.

### Priority improvement direction
- keep moving formatting rules out of prose and into explicit final-audit checks
- add measurable heuristics where possible (one insight per bullet, avoid over-wide comparison tables, prefer split tables)
- treat readability as a quality gate, not only a presentation preference

---

## Family E — Research Depth vs. Briefing Drift

### Core failure pattern
The report sounds intelligent and plausible but stays at the level of a high-quality overview rather than load-bearing deep research.

Typical symptom: broad coverage, many reasonable statements, little prioritization of what actually determines the conclusion.

### Why this matters
This is the most subtle failure family. It produces reports that feel good on first read but are weak as decision support.

### Typical failure forms
- industry-common-sense summary instead of evidence-backed deep analysis
- many dimensions covered, but no prioritization of 3-5 load-bearing variables
- category map without value-accrual analysis
- counter-evidence present only weakly or ceremonially
- report answers "what exists" better than "what matters most"

### Existing evals in this family
- `evals/cases/industry-landscape-depth-case.md`
- `evals/templates/depth-rubric.md`
- `evals/cases/hnb-industry-report-table-design-case.md` (partial overlap)

### Existing rule/checklist coverage
- `references/research-depth-rubric.md`
- `references/counter-evidence.md`
- `references/decision-report-template.md`
- `checklists/final-audit.md`

### What this family suggests structurally
Depth is already recognized as a target, but the current repo still has stronger discipline for factual hygiene than for decision usefulness.

### Priority improvement direction
- add explicit decision-utility evaluation, not just depth evaluation
- identify whether the report names and tests the load-bearing variables
- make "what would change the conclusion" a stronger required field

---

## Family F — Scope Completeness and Coverage Geometry

### Core failure pattern
The report nominally covers a broad company, market, or industry scope, but omits one or more load-bearing geographies, segments, or regulatory regimes.

Typical symptom: a report labeled global or comprehensive is actually concentrated on only the easiest or most visible areas.

### Why this matters
A scope miss can distort the final conclusion even when individual facts are correct.

### Typical failure forms
- global market report that effectively ignores a top-5 geography
- competitive map missing a major local player set
- regulatory analysis that only covers US/EU but not the most constraining regime
- value-chain report that names all layers but skips the highest-friction or highest-value segment

### Existing evals in this family
- `evals/cases/hnb-industry-report-table-design-case.md`
- `evals/cases/industry-landscape-depth-case.md` (partial overlap)

### Existing rule/checklist coverage
- partially covered by `references/current-state-verification.md`
- partially covered by `references/task-types.md`
- partially covered by `checklists/final-audit.md`

### What this family suggests structurally
This family is not yet fully formalized in the repo. It appears repeatedly enough that it likely deserves its own dedicated eval and possibly a checklist gate for global/industry reports.

### Priority improvement direction
- add a dedicated eval for global-market scope completeness
- add explicit checks for top geographies, top segments, and omitted load-bearing scope
- require the report to state its actual coverage boundaries when it is not truly comprehensive

---

## Cross-family meta-failure — Rule Activation vs. Rule Existence

### Core pattern
A rule exists in the repo, the model appears to understand it, but the final output still violates it.

This is different from a missing-rule problem.

### Current signs of this meta-failure
- listed-company market snapshot rule known, but omitted in delivery
- confidence labels known, but not applied consistently to estimates
- traceability concept known, but body-level citations still missing
- bullet discipline known, but exec summary still collapses into dense walls

### Existing eval signals
- `evals/cases/minimax-company-report-case.md`
- `evals/cases/byd-report-format-discipline-case.md`
- `evals/cases/apple-product-roadmap-and-investment-case.md`

### Structural implication
The next phase of repo evolution should focus more on:

- trigger routing
- checklist activation
- delivery-time audit enforcement
- meta-evals that test whether the correct rule fired

This is the main reason not to solve every new failure with more prose.

---

## Distillation-type artifacts vs. normal evals

Not every file in `evals/` plays the same role.

### Case evals
These document a concrete real-world failure or regression.

Examples:
- `freshness-xiaomi-case.md`
- `moore-threads-listing-status-case.md`
- `hnb-industry-report-table-design-case.md`

### Rubrics
These score a general capability dimension.

Examples:
- `depth-rubric.md`
- `current-state-checks.md`

### Distillation artifacts
These compare two outputs to extract reusable skill improvements.

Example:
- `byd-gpt-vs-minimax-comparative-distillation.md`

### Suggested implication
The repo should gradually treat these as distinct eval subtypes, even if they stay in one folder.

---

## What this taxonomy implies should happen next

If the current eval set keeps growing without taxonomy, the repo will become a long list of cases with weak structural reuse.

The current evidence suggests the next improvements should focus on:

1. **Rule activation / checklist routing**
   - especially for listed companies, fast-moving current-state tasks, ranking claims, and forward-looking claims

2. **A dedicated scope-completeness eval**
   - to capture omitted load-bearing geographies or market segments

3. **A decision-utility rubric**
   - to complement depth scoring with actual decision support quality

4. **A formal distinction between case evals, rubrics, and distillation artifacts**
   - so new additions are easier to classify and maintain

---

## Short classification table

| Family | Main question | Existing strength | Main gap |
|---|---|---|---|
| A. Current-state / time-layer discipline | Is the report temporally correct? | Strong rule coverage | Triggering/execution drift |
| B. Source traceability / evidence weighting | Can the reader audit the claims? | Good rule coverage | Claim-level enforcement |
| C. Forward-looking claim discipline | Are predictions structured and sourced? | Checklist exists | Output-time leakage |
| D. Output structure / information density | Is the report readable and decision-efficient? | Improving template discipline | Measurable enforcement still weak |
| E. Research depth / briefing drift | Is this deep research or polished summary? | Rubric exists | Decision-utility layer still thin |
| F. Scope completeness / coverage geometry | Did the report miss a load-bearing part of the scope? | Weakly covered | Needs dedicated eval/gate |
| Meta: Rule activation | Did the correct rule fire at all? | Recognized implicitly | Needs explicit eval/gate |

---

## Bottom line

The repo is no longer short on failure examples.

The next step is to make the eval set easier to reason about as a system:

- fewer isolated lessons
- clearer failure families
- stronger distinction between missing rules and failed rule activation
- more deliberate routing from observed failure -> structural fix
