# Academic Review GPT-vs-Local Comparative Distillation

> **Purpose:** Compare GPT deep research reports against local deep-research-skill reports on two matched academic-review topics (AI Agent planning evaluation and MLLM visual reasoning) to identify structural differences that could improve the academic route's output pattern — without weakening source traceability or evidence discipline.

---

## Case identity

- **Case name:** Academic review GPT-vs-local comparative distillation
- **Date:** 2026-06-16
- **Research question:** Two paired comparisons:
  1. What is the current state and key controversies in AI Agent planning ability evaluation?
  2. What are the real progress and limitations in multimodal LLM visual reasoning?
- **Why this comparison matters:**
  - GPT reports on these topics expose structural patterns (benchmark ladder, mechanism map, failure-case table, practitioner implication) that local reports often deliver in flatter prose.
  - But GPT reports use `turn...` citations that are unreachable outside the original session, making them undeliverable under the repo's source-traceability contract.
  - This pair tests whether the repo can absorb GPT-style structural capability while enforcing its own evidence discipline.
  - Unlike the existing 14 comparative-distillation cases (all non-academic routes), this is the first academic-review route distillation.
- **Report A (GPT):** GPT deep research: "AI Agent 规划能力评测方法与学术争议" + "多模态大模型视觉推理真实进展与局限"
- **Report B (Local):** deep-research-skill reports on the same topics, generated through the local pipeline
- **Reference / stronger report (if any):** GPT for structural readability and decision-framework design; Local for traceability, evidence discipline, and route contract execution
- **Prompt(s):** Overlapping research questions but not identical prompts — GPT reports were generated in GPT deep research interface; local reports used deep-research-skill pipeline
- **Important scope or timing differences:**
  - Both report pairs cover ~2023–2026 literature, broadly comparable time windows
  - Reports were generated independently, not as competing runs on identical prompts
  - Comparison focuses on structural discipline differences, not factual retrieval accuracy

---

## Comparison purpose

This comparison is **not** for deciding which system is "better."

It is for:

1. Identifying which GPT structural patterns (benchmark ladder, mechanism map, failure-case table, opening thesis) are worth absorbing into the academic-review route output template.
2. Verifying that all GPT structural patterns can be rebuilt with the repo's Source Register + evidence hierarchy + audit discipline rather than copied as `turn...` references.
3. Determining whether the gap is a **missing rule** (no rule exists for this pattern), **missing trigger** (rule exists but wasn't activated), or **execution failure** (rule triggered but not executed properly).
4. Registering this pair as a regression asset for future academic-review improvements.

---

## Dimension 1: Current-state discipline

### Report A
- AI Agent report: Opens with clear **evaluation stack layering** — synthetic tasks, interactive environments, human evaluation, theoretical/mechanistic debates. Each layer is described with concrete benchmark examples and known limitations.
- MLLM report: Opens with a clear **thesis judgment** — models have improved significantly on OCR/charts/documents/templated VQA, but spatial/temporal/abstract/multi-step visual reasoning remain unstable. Immediately distinguishes what works from what doesn't.
- Both reports state the literature coverage window implicitly through cited paper dates, but neither has an explicit "coverage window" declaration in the opening.

### Report B
- AI Agent report: Follows the academic route contract — has coverage window, search strategy documentation, evidence hierarchy mapping. But the opening is more procedural (describing route and method) than judgment-first.
- MLLM report: Similar pattern — route-compliant opening, evidence matrix declared, but the "here is the state of the field" thesis is delivered later than in the GPT version.

### Gap
- GPT is stronger at **front-loading the thesis** — the reader knows within the first 10–15% what the report judges about the field. Local reports front-load the methodology and route metadata, deferring the thesis.
- GPT's coverage window is **implicit** (stated through paper dates) while Local's is **explicit** (declared in method sections). The repo's discipline on explicit windows is correct, but GPT's approach of thesis-before-methodology is worth adopting.

### Candidate action
- Academic-review template should open with the thesis judgment, then present route/methodology metadata in a secondary position (exception: when the methodology IS the core output, such as a methodological review).

### Action type
`TEMPLATE_CHANGE` — academic route opening should prioritize thesis over methodology as default, with an explicit exemption when methodology is the core output. This is not ambiguous: the repo already documents metadata-first drift as a failure pattern (final-audit.md L169-172) with an academic-method exception (L171). This candidate simply tightens the exception's trigger conditions.

---

## Dimension 2: Numerical and date discipline

### Report A
- AI Agent report: Uses **ladder-style benchmark comparison** (synthetic → interactive → human eval → theoretical), with approximate performance ranges and known limitations per benchmark.
- MLLM report: Uses a **model/data asset × architecture/training × result × limitation** table to organize significant progress points. Has a separate **benchmark/failure-case** table connecting MathVista, MMMU, MMStar, ClockQA, CalendarQA to specific mechanism failures.
- Both reports use approximate ranges rather than exact numbers, consistent with academic review conventions where exact numbers are less common than direction and magnitude.

### Report B
- Uses the repo's evidence labeling system (`[Sxx]` citations, confidence tags).
- Has benchmark comparability schema per `references/academic-evidence-hierarchy.md`.
- Tends to present benchmark information in prose paragraphs rather than structured comparison tables.

### Gap
- GPT's **benchmark ladder** and **failure-case table** are more information-dense and scannable than Local's prose paragraphs for the same content.
- Local's benchmark comparability discipline (disclosing prompt/eval protocol, dataset split, metric, baseline, source role) is more rigorous but can be hidden in prose rather than made visually scannable.
- The gap is **template/format**, not missing rules — the benchmark comparability schema already requires all the fields.

### Candidate action
- Add a recommended table format for benchmark comparison in academic-review reports: `| Benchmark/Task | Capability claim | Model | Metric | Limitation | Source |` — matches the existing schema but makes it visually scannable.

### Action type
`CHECKLIST_HARDENING` — existing comparability schema is correct; add a table template reference.

---

## Dimension 3: Source traceability and evidence weighting

### Report A
- Uses `turn...` session-internal citation handles — **unreachable outside the originating GPT session**.
- No Source Register (7-column or 11-column academic extension).
- No claim-level evidence hierarchy mapping — citations are per-paragraph or per-claim, but evidence strength is expressed through narrative framing rather than structured labels.
- **Undeliverable** under the repo's final-audit hygiene rules (final-audit.md L295, source-traceability.md L19).

### Report B
- Uses `[Sxx]` or Author-Year format with Source Register (7-column base for general, 11-column extension for academic).
- Has evidence hierarchy (dual-dimension: study design × venue prestige) per `references/academic-evidence-hierarchy.md`.
- Has benchmark comparability schema for AI benchmark comparisons.
- Stronger on **auditability** — a reviewer can trace claims back to sources.

### Gap
- This is the repo's **strongest advantage** over GPT. The import hygiene rules (#263) already forbid `turn...` references.
- GPT's structural patterns (benchmark ladder, mechanism map, failure-case table) can be absorbed only if each claim is rebuilt with local Source Register entries.
- No new rule is needed — the existing discipline is correct and sufficient.

### Candidate action
- When importing structural patterns from external reports, document which structures were inspired by external sources in the report's process-notes section (not as a source citation, but as a discovery-input disclosure).

### Action type
`NO_ACTION` — existing import hygiene (source-traceability.md §External research output / Imported report hygiene) already covers this pattern.

---

## Dimension 4: Forward-looking claim discipline

### Report A
- AI Agent report: Gives **researcher next-step recommendations**: combined evaluation, process evidence, task perturbation, long-horizon planning failure modes. Labels these as recommendations, not predictions.
- MLLM report: Gives **engineering recommendations**: visual evidence parsing, question verification, answer generation, external validator, perturbation testing, no-image baseline. Also labeled as recommendations.
- Both reports maintain good separation between current-state analysis and forward-looking suggestions.

### Report B
- Follows the repo's forward-looking discipline (named source, assumptions, reversal conditions).
- The forward-looking section tends to be more cautious and bound to evidence, but less structured (fewer bullet-graded recommendations).

### Gap
- GPT's forward-looking sections are **more actionable** because they are organized as concrete recommendations with implied priority (list order).
- Local's forward-looking discipline is stronger on calibration but weaker on structuring recommendations for the reader to act on.
- The gap is not about claims discipline (both are responsible) but about **output format** — structuring recommendations with implied priority or effort estimates.

### Candidate action
- Academic-review reports should consider adding a "practitioner implications" or "researcher action items" section that distills forward-looking observations into concrete recommendations with implied priority.

### Action type
`TEMPLATE_CHANGE` — add an optional recommendations section to the academic review template.

---

## Dimension 5: Structural readability and information density

### Report A
- AI Agent report: **Layered evaluation stack** as organizing principle — synthetic → interactive → human → theoretical. Each layer has its own sub-structure with benchmark examples, known problems, open debates.
- MLLM report: **Mechanism map** using Mermaid diagram — decomposes failures into visual encoding → token compression/alignment → LLM reasoning → output format. Uses **benchmark/failure-case table** to connect benchmark names to specific mechanism failures.
- Both reports use tables, section structure, and hierarchical bullets to increase information density.

### Report B
- Follows the repo's academic route structure: coverage window, search strategy, evidence matrix, open questions.
- Content is well-organized but tends toward **sequential prose** — fewer structured tables, less use of mechanism diagrams, more reliance on paragraph-level exposition.

### Gap
- GPT's structural reading aids (mechanism map, benchmark ladder, failure-case table, opening thesis) are **format innovations** that increase scanability without sacrificing substance.
- Local's prose-first approach is safer (less risk of oversimplification) but makes it harder for the reader to quickly grasp the field's structure.
- These patterns are **content-agnostic** — they can be implemented in the local system without importing any GPT- specific content.

### Candidate action
- Add optional structure prompts to the academic review SKILL.md section or report template: "Consider adding a mechanism diagram (Mermaid), a benchmark-comparison table, and a failure-case table when the review covers multiple models or benchmarks."
- These structures must still comply with the existing Source Register and evidence discipline.

### Action type
`CHECKLIST_HARDENING` — add a non-blocking readability item to the academic analysis audit: "If the review covers 3+ benchmarks or models, consider using a structured comparison table."

---

## Dimension 6: Decision usefulness

### Report A
- AI Agent report: Concludes with **what researchers should do next** — concrete next-step directions for evaluation methodology.
- MLLM report: Concludes with **what engineers/practitioners should do** — concrete data-collection, validation, and testing recommendations.
- Both reports make the **reader's next action** explicit.

### Report B
- Concludes with **what the evidence shows** — synthesis of findings, open questions, limitations.
- Stronger on uncertainty communication but weaker on actionable implications.

### Gap
- The academic-review route's article contract currently prioritizes evidence synthesis over action recommendations.
- This is appropriate for some academic review types (pure literature survey) but less useful for field-progress analyses where practitioners need direction.
- The decision-usefulness frame in the comparative-distillation method assumes a decision-oriented task. For academic reviews, "decision usefulness" means **research direction usefulness** or **practitioner implication clarity**.

### Candidate action
- Distinguish two sub-styles within academic-review route:
  - **Survey-style**: evidence synthesis, open questions, limitations (current default).
  - **Field-progress analysis**: thesis-first opening, benchmark ladder, mechanism map, researcher/practitioner recommendations (GPT-inspired).
- Both sub-styles must maintain full Source Register, evidence hierarchy, and audit discipline.

### Action type
`TEMPLATE_CHANGE` — document the field-progress-analysis sub-style as an optional variant of the academic route output contract.

---

## Candidate-action summary

| # | Candidate action | Failure family | Action type | Proposed home |
|---|---|---|---|---|
| 1 | Academic review opening should put thesis before methodology | output structure / information density | `TEMPLATE_CHANGE` | `references/academic-evidence-hierarchy.md` (academic route opening structure) |
| 2 | Add benchmark comparison table template to academic route | source traceability / evidence weighting | `CHECKLIST_HARDENING` | `checklists/academic-analysis-audit.md` |
| 3 | Document external-report structural inspiration disclosure in process notes | source traceability / import hygiene | `NO_ACTION` | Already covered by source-traceability.md |
| 4 | Add optional practitioner/researcher recommendations section | decision usefulness | `TEMPLATE_CHANGE` | `references/report-template.md` (optional academic review recommendations block) |
| 5 | Add non-blocking structured table check to academic audit | output structure / information density | `CHECKLIST_HARDENING` | `checklists/academic-analysis-audit.md` |
| 6 | Document field-progress-analysis sub-style in academic route | route activation | `TEMPLATE_CHANGE` | `ROUTING-MATRIX.md` academic route section |

---

## Triage notes

### Candidate 1 — Thesis-before-methodology opening
- **Why it matters:** Academic reviews that open with methodology/route metadata before the thesis create a 15-20% delay before the reader understands the report's judgment. This is the "metadata-first drift" pattern documented in final-audit.md L169-172.
- **Why it is reusable:** Any academic-review report benefits from thesis-first structure, not just field-progress analyses. The fix is a template ordering change, not a judgment call.
- **Why this home is best:** `references/academic-evidence-hierarchy.md` is the academic route's primary discipline reference. Adding an opening structure guideline there is more discoverable than burying it in the general report-template.md.
- **Promotion status:** `WAIT_FOR_SECOND_CASE` — the current case only demonstrates the gap via GPT comparison. A real local academic-review report written with this structure is needed to validate the template change.

### Candidate 2 — Benchmark comparison table template
- **Why it matters:** The benchmark comparability schema (references/academic-evidence-hierarchy.md §Benchmark comparability) already defines disclosure fields. Adding a recommended table format makes the schema actionable rather than just a checklist.
- **Why it is reusable:** Any academic review covering 3+ benchmarks or models benefits from structured comparison tables.
- **Why this home is best:** `checklists/academic-analysis-audit.md` is the execution gate for academic route discipline. A non-blocking checklist item prompts the model to use the table format without blocking delivery.
- **Promotion status:** `WAIT_FOR_SECOND_CASE` — validate against one real academic review before adding to the checklist.

### Candidate 3 — External report structural inspiration disclosure
- **Why it matters:** When a report explicitly acknowledges "this structure was inspired by external deep research reports," the audit should verify that no `turn...` references leaked through.
- **Why it is reusable:** Cross-system structural inspiration will become more common as multi-system workflows evolve.
- **Why this home is best:** Already covered by `references/source-traceability-and-claim-citation.md` §External research output / Imported report hygiene. No new rule needed.
- **Promotion status:** `NO_ACTION` — existing rules are sufficient.

### Candidate 4 — Practitioner/researcher recommendations section
- **Why it matters:** Academic reviews currently prioritize evidence synthesis over actionable implications. Field-progress analyses benefit from explicit researcher or practitioner next steps.
- **Why it is reusable:** The pattern (opening thesis → benchmark ladder → mechanism map → failure-case table → practitioner recommendations) is content-agnostic and applies to any field-progress review.
- **Why this home is best:** `references/report-template.md` already contains optional structural blocks. An optional "academic review recommendations" block fits the existing template pattern.
- **Promotion status:** `WAIT_FOR_SECOND_CASE` — the GPT pattern is aspirational. A real local academic review that uses recommendations needs to confirm this doesn't dilute evidence discipline.

### Candidate 5 — Non-blocking structured table audit item
- **Why it matters:** The checklist currently has no item prompting structured comparison tables for multi-benchmark reviews.
- **Why it is reusable:** Applies to any academic review covering multiple benchmarks, models, or papers.
- **Why this home is best:** `checklists/academic-analysis-audit.md` is the natural home for non-blocking quality items.
- **Promotion status:** `WAIT_FOR_SECOND_CASE` — add only after Candidate 2 table template is validated.

### Candidate 6 — Field-progress-analysis sub-style
- **Why it matters:** The current academic route has one artifact contract. A field-progress-analysis variant would have different output expectations (thesis-first, benchmark tables, mechanism maps, recommendations).
- **Why it is reusable:** Many academic-review tasks are implicitly field-progress analyses rather than pure surveys.
- **Why this home is best:** `ROUTING-MATRIX.md` academic route section already documents the artifact contract. A sub-style variant would extend this section.
- **Promotion status:** `WAIT_FOR_SECOND_CASE` — requires validation against a real local report written in this style before adding to ROUTING-MATRIX.md.

---

## Things explicitly rejected

| Observation | Why rejected |
|---|---|
| GPT's `turn...` citation format should be tolerated because it's convenient | Violates the repo's core auditability contract. Import hygiene rules (#263) correctly reject it. |
| GPT's Mermaid diagrams should be copied into local reports | Diagrams express the structure authors chose for that specific content. The pattern (mechanism decomposition) is learnable; the specific diagram is not reusable without re-analysis. |
| Academic reviews don't need decision usefulness because they're not decision memos | Partially true for survey-style reviews, but field-progress analyses clearly benefit from actionable implications. The two sub-styles should coexist. |
| New rules are needed because local reports lack GPT's structural readability | The gap is template/trigger/format, not missing rules. The existing benchmark comparability schema, evidence hierarchy, and route contract are sufficient once the output template suggests structured formats. |

---

## Final judgment

### What the stronger report did better
GPT reports are stronger on **structural readability and front-loaded thesis judgment** — they organize academic content into scannable frameworks (benchmark ladders, mechanism maps, failure-case tables, actionable recommendations) that make complex field assessments accessible. Local reports are stronger on **traceability, evidence discipline, and auditability** — they have structured Source Registers, explicit evidence hierarchies, documented search strategies, and claim-level citations that make every assertion verifiable.

### What should change in the repo now
1. The academic route's output contract should document two sub-styles: **survey-style** (current default, strong on evidence synthesis) and **field-progress-analysis** (GPT-inspired, adds thesis-first opening, benchmark tables, mechanism maps, practitioner recommendations).
2. `checklists/academic-analysis-audit.md` should add a non-blocking readability item suggesting structured comparison tables for multi-benchmark or multi-model reviews.
3. `references/academic-evidence-hierarchy.md` should include an optional benchmark comparison table template as a practical example of the comparability schema.

### What should wait for another confirming case
The field-progress-analysis sub-style should be validated against a real academic review task before adding it to ROUTING-MATRIX.md as a documented variant. Currently there is no local report that was intentionally written in this style — the GPT patterns are aspirational, not validated.

### Is this mainly a missing rule, missing trigger, or execution problem?
**Missing trigger + output format gap.** The existing rules (import hygiene, evidence hierarchy, benchmark comparability, source register) are sufficient. What's missing is:
- A trigger that recognizes when an academic review task would benefit from field-progress-analysis structure.
- An output format/template that suggests structured tables and thesis-first opening for that sub-style.
- The candidate-rule-registry finding is confirmed: 57/60 candidates already covered; this case's 6 candidates follow the same pattern — no uncovered rules needed.

---

## Quality checklist

- [x] the two report pairs are comparable enough to justify distillation (same topic, similar time window, same route)
- [x] the comparison used the six fixed dimensions
- [x] each accepted candidate has an action type
- [x] each accepted candidate has a proposed repo home
- [x] at least one rejected observation is documented (4 documented)
- [x] the final judgment distinguishes rule gap vs trigger gap vs execution gap (trigger + output format gap)

