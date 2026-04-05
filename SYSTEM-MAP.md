# System Map

This file maps the current `references/`, `checklists/`, and `evals/` into practical families.

It exists to answer four maintenance questions quickly:

1. which files belong to the same problem area?
2. when a failure appears, which layer should be changed first?
3. which route families already have strong support?
4. where is the repo still structurally thin?

This is a mapping document, not a directory-reorganization plan.

It should make the current system easier to navigate without forcing premature file moves.

---

## How to use this file

When a new failure, improvement idea, or refactor proposal appears, classify it in this order:

1. which family is it closest to?
2. is the problem mainly routing, discipline, audit, eval coverage, or delivery?
3. which existing files already cover part of it?
4. what is the narrowest layer that should change first?

Default escalation order:

- if the task family is being misidentified -> fix routing
- if the task family is right but method is weak -> fix references/templates
- if the method exists but delivery keeps failing -> harden checklists
- if the failure mode is still unclear -> add or improve eval coverage first
- if the memo is right but export is broken -> fix scripts / rendering layer

---

## Family A — Workflow and orchestration

### Purpose
Defines the shared research process that applies before any route-specific specialization.

### Primary files
- `SKILL.md`
- `references/task-types.md`
- `references/counter-evidence.md`
- `references/source-quality.md`
- `references/claim-matrix.md`
- `references/parallel-research.md`

### Typical questions this family answers
- what is the real objective?
- what task type is this?
- how deep should the research go?
- when should I stop searching?
- when is parallelization justified?

### Typical failure signs
- generic search-and-summarize drift
- poor research planning
- unnecessary browsing loops
- weak counter-evidence search
- parallelism used without enough structure

### First place to change
- `SKILL.md` if the shared workflow itself is weak
- `references/` if the workflow is fine but the reusable method is thin

---

## Family B — Route activation and decision routing

### Purpose
Makes mature task families explicit so the right discipline set and delivery contract activate.

### Primary files
- `ROUTING-MATRIX.md`
- `evals/rule-activation-and-execution-discipline.md`

### Supported mature routes
- provider / vendor selection
- market entry / regional expansion
- market outlook / industry evolution
- first-tier / competitive positioning
- constrained choice / shortlist
- listed-company / investment-style research

### Typical failure signs
- the correct rule exists but does not activate
- the report uses the right vocabulary but the wrong structure
- the route is implicit in reasoning but invisible in the final artifact
- a task drifts from choice memo into overview memo

### First place to change
- `ROUTING-MATRIX.md` when route selection or attached discipline mapping is wrong
- `SKILL.md` only if the shared orchestration rule is genuinely missing
- `evals/` if the failure is observed but not yet clearly classified

---

## Family C — Current-state and time-layer discipline

### Purpose
Protects fast-moving research from stale facts, frozen time layers, and blurred present-vs-forward views.

### Primary references
- `references/current-state-verification.md`
- `references/finance-date-discipline.md`
- `references/corporate-status-and-listing-state-discipline.md`
- `references/ranking-and-current-claims-discipline.md`

### Primary checklists
- `checklists/listed-company-report.md`
- `checklists/final-audit.md`

### Representative evals
- `evals/freshness-xiaomi-case.md`
- `evals/apple-product-and-valuation-case.md`
- `evals/moore-threads-listing-status-case.md`
- `evals/ranking-and-current-claims-xiaomi-update-case.md`
- `evals/finance-and-market-share-cambricon-case.md`
- `evals/minimax-company-report-case.md`

### Typical failure signs
- stale product or model generation presented as current
- listing state frozen at an earlier stage
- present-tense ranking without a time basis
- reported financials, market snapshot, and estimates blended together

### First place to change
- routing layer if current-state-sensitive tasks are not activating the right gates
- references if time-layer method is unclear
- checklists if current snapshot fields exist in theory but still fail in delivery

---

## Family D — Source traceability and evidence weighting

### Purpose
Makes load-bearing claims auditable and separates primary evidence from inference-heavy judgment.

### Primary references
- `references/source-traceability-and-claim-citation.md`
- `references/source-quality.md`
- `references/claim-matrix.md`
- `references/report-template.md`

### Primary checklists
- `checklists/source-traceability.md`
- `checklists/final-audit.md`

### Representative evals
- `evals/source-traceability-moore-threads-case.md`
- `evals/apple-product-roadmap-and-investment-case.md`
- `evals/minimax-company-report-case.md`
- `evals/cambricon-evidence-weighting-and-traceability-case.md`
- `evals/byd-gpt-vs-minimax-comparative-distillation.md`

### Typical failure signs
- bibliography exists but claims are not auditable
- numbers and dates appear without visible support
- direct evidence and inference are blended
- mixed-evidence positioning judgments hide which claims are load-bearing

### First place to change
- references when evidence structure itself is weak
- checklists when traceability exists in theory but not in the report body
- route contracts when certain task families should always attach traceability but do not

---

## Family D2 — Process artifacts and audit binding

### Purpose
Makes route, evidence, uncertainty, and counter-evidence handling more recoverable than final prose alone.

### Primary files
- `references/research-pack-contract.md`
- `schemas/research-pack.md`
- `checklists/final-audit.md`
- `examples/research-pack-example.md`

### Typical failure signs
- final report sounds rigorous but cannot be reconstructed
- route is only implicit
- uncertainty is rhetorical rather than structural
- audit depends entirely on prose interpretation

### First place to change
- process-artifact contract when the internal structure is too thin
- final-audit expectations when the structure exists but is not being checked
- examples when the contract exists but still feels too abstract to use

---

## Family E — Forward-looking and estimate discipline

### Purpose
Controls forecasts, roadmap statements, target dates, and estimate-heavy claims so they do not create false certainty.

### Primary references/checklists
- `checklists/forward-looking-claims.md`
- `references/finance-date-discipline.md`
- `checklists/final-audit.md`

### Representative evals
- `evals/apple-product-roadmap-and-investment-case.md`
- `evals/byd-report-format-discipline-case.md`
- `evals/hnb-industry-report-table-design-case.md`
- `evals/byd-gpt-vs-minimax-comparative-distillation.md`

### Typical failure signs
- `预计` / `expected` / `likely` without source role
- roadmap claims without announced vs rumored separation
- consensus numbers without source or date
- estimate language without assumption chain

### First place to change
- checklists when forecasts leak through at delivery time
- references/templates when the report structure does not expose source role clearly enough
- route contracts when a route should always attach forward-looking discipline but does not

---

## Family F — Decision-routing and constrained-choice discipline

### Purpose
Supports tasks where the output must help choose among options rather than merely describe them.

### Primary references
- `references/option-selection-and-shortlist-discipline.md`
- `references/decision-report-template.md`
- `references/market-outlook-and-scenario-discipline.md`
- `references/ranking-and-current-claims-discipline.md`

### Primary checklists
- `checklists/option-selection-final-audit.md`
- `checklists/final-audit.md`

### Representative evals
- `evals/api-supplier-selection-gpt-vs-minimax-comparative-distillation.md`
- `evals/sea-market-entry-gpt-vs-minimax-comparative-distillation.md`
- `evals/multi-origin-meetup-city-selection-gpt-vs-minimax-comparative-distillation.md`
- `evals/cambricon-first-tier-positioning-case.md`
- `evals/ai-coding-agent-market-outlook-gpt-vs-minimax-comparative-distillation.md`
- `evals/decision-utility-rubric.md`

### Typical failure signs
- provider selection becomes vendor encyclopedia
- market-entry memo becomes regional overview
- outlook memo becomes industry summary
- ranking memo collapses multiple dimensions into prestige language
- shortlist recommendation appears without shortlist-construction logic

### First place to change
- `ROUTING-MATRIX.md` when a mature task family is misrouted or under-specified
- route-supporting references/templates when the task family is right but the memo structure is weak
- option/final audits when visible decision structure is still not appearing at delivery time

---

## Family G — Research depth, scope completeness, and decision utility

### Purpose
Protects against reports that sound smart but still fail as deep, load-bearing decision support.

### Primary references
- `references/research-depth-rubric.md`
- `references/decision-report-template.md`
- `references/task-types.md`
- `references/failure-taxonomy.md`

### Primary checklists/evals
- `checklists/final-audit.md`
- `evals/depth-rubric.md`
- `evals/decision-utility-rubric.md`
- `evals/global-market-scope-completeness-case.md`
- `evals/industry-landscape-depth-case.md`

### Typical failure signs
- broad coverage but weak prioritization
- summary quality is good, decision utility is weak
- global scope claim hides missing geographies/segments
- report answers “what exists” but not “what matters most”

### First place to change
- eval layer first when the failure is felt but still hard to pin down
- references/templates when the repo needs stronger structure around load-bearing variables and what-changes-the-view logic
- final audit when a known depth/scope failure should be a delivery-time gate

---

## Family H — Delivery cleanliness and rendering reliability

### Purpose
Preserves the report’s intended structure and readability when converted into final user-facing artifacts.

### Primary scripts
- `scripts/markdown_to_html.py`
- `scripts/render_pdf.py`
- `scripts/md_to_pdf.py`

### Primary references/checklists
- `checklists/final-audit.md`
- `references/report-template.md`
- `references/failure-taxonomy.md`

### Representative evals
- `evals/minimax-sea-memo-pdf-layout-case.md`
- `evals/hnb-industry-report-table-design-case.md`
- `evals/byd-report-format-discipline-case.md`

### Typical failure signs
- citation artifacts leak into final body
- placeholder residues or render hints survive export
- dense tables degrade badly in PDF
- Chinese-heavy PDFs look broken, torn, or OCR-like
- memo logic is correct but delivery artifact feels corrupted

### First place to change
- scripts/rendering layer if the report logic is sound but the export is broken
- final-audit gates if known delivery failures are not being caught before export
- templates when the information design or target-language labeling contract is unclear
- routing/workflow layer when target-language coherence should have been a visible delivery discipline but did not activate

---

## Family I — Comparative distillation and improvement routing

### Purpose
Turns paired-report comparisons into repeatable repo improvements instead of one-off taste judgments.

### Primary files
- `references/comparative-distillation-method.md`
- `evals/comparative-distillation-template.md`
- `references/failure-taxonomy.md`

### Representative evals
- `evals/api-supplier-selection-gpt-vs-minimax-comparative-distillation.md`
- `evals/ai-coding-agent-market-outlook-gpt-vs-minimax-comparative-distillation.md`
- `evals/sea-market-entry-gpt-vs-minimax-comparative-distillation.md`
- `evals/multi-origin-meetup-city-selection-gpt-vs-minimax-comparative-distillation.md`
- `evals/byd-gpt-vs-minimax-comparative-distillation.md`
- `evals/weekend-seaside-destination-gpt-vs-minimax-comparative-distillation.md`

### Typical questions this family answers
- is the gap a new rule or only an execution miss?
- should the change land in routing, references, checklists, templates, or scripts?
- is this failure recurring enough to promote into a more general discipline?

### First place to change
- eval/distillation files when the pattern is still being understood
- then whichever layer the distillation points to: routing, references, checklists, or scripts

---

## Intervention guide by symptom

Use this quick map when deciding where to change the repo.

### Symptom: wrong task shape
Examples:
- provider choice memo turns into vendor overview
- market-entry memo turns into regional research summary
- top-tier question becomes generic ranking prose

Change first:
- `ROUTING-MATRIX.md`
- then route-supporting templates/references if needed

### Symptom: right task shape, weak evidence discipline
Examples:
- claims are not auditable
- stale facts treated as current
- estimates blur into confirmed facts

Change first:
- relevant `references/`
- then relevant checklist if delivery-time enforcement is weak

### Symptom: right method exists, but output still leaks failures
Examples:
- no visible current snapshot
- no inline evidence weighting in body
- decision memo structure missing in final artifact

Change first:
- `checklists/`
- then `ROUTING-MATRIX.md` if the discipline was not being attached consistently

### Symptom: architecture or docs are unclear
Examples:
- contributors keep adding route logic back into `SKILL.md`
- people cannot tell where a fix belongs

Change first:
- `ARCHITECTURE.md`
- `SYSTEM-MAP.md`
- `README.md`

### Symptom: content is good, export is bad
Examples:
- PDF looks corrupted
- tables break badly
- placeholders or raw syntax leak into output

Change first:
- `scripts/`
- then delivery-related final-audit hardening if needed

---

## Current thin spots

The current system is much clearer than before, but still relatively thin in a few places:

- formal grouping of eval subtypes is still implicit rather than encoded in folder structure
- some families still rely more on representative eval clusters than on explicit map files
- the delivery subsystem is documented architecturally, but not yet documented with its own dedicated operator-facing note
- not every route family yet has a clearly separated supporting reference vs checklist vs eval cluster

These are natural next-step candidates, but they do not need to be solved in the same PR as this map.

---

## Maintenance rule

Do not use this file as an excuse to reorganize everything at once.

Use it to make narrower changes cleaner:

- identify the family
- identify the layer
- change the smallest correct surface
- leave structural relocation for later unless it clearly reduces real confusion
