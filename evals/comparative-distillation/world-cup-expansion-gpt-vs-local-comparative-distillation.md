# Comparative Distillation: World Cup Expansion (32→48 Teams) — GPT vs Local Deep-Research-Skill

## Case identity

- **Case name:** world-cup-expansion-gpt-vs-local-comparative-distillation
- **Date:** 2026-06-29
- **Research question:** Analyze the impact of the 2026 World Cup expansion from 32 to 48 teams on global fairness and group-stage competitive quality. Include current rules, counter-evidence, and uncertainty.
- **Why this comparison matters:** The same research question produced two reports with divergent execution quality despite the local report correctly identifying the regulatory route and rule-system add-on. This comparison tests whether the Phase A/B declared-not-executed gate and checklists are sufficient to close the gap, or whether residual structural discipline differences remain.
- **Report A:** GPT report — strong regulatory analysis framework with explicit state taxonomy (participant categories with strategy space/information/action paths), qualified intervention matrix (side effects, monitoring indicators, reversal conditions), explicit causal chains (rules → incentives → behavior → indicators), dated data-as-of block, clear source register with institutional sources.
- **Report B:** Local deep-research-skill report — route declared correctly (regulatory) and rule-system add-on declared, but not executed. Wikipedia-heavy source register (8/9 tertiary, S08 only FIFA official). Body uses `[CONF]/[INFER]` as proxy for `[Sxx]` citations. Regulatory contract missing scenarios, enforcement reality, monitoring signals. Add-on produces flat alternatives table instead of intervention matrix. Self-assessment overclaims all disciplines.
- **Reference / stronger report (if any):** Report A (GPT)
- **Prompt(s):** "Analyze the impact of the 2026 World Cup expansion from 32 to 48 teams on global fairness and group-stage competitive quality. Include current rules, counter-evidence, and uncertainty."
- **Important scope or timing differences:** Both reports address the same question in the same timeframe (June 2026). Report A is a single-shot GPT output; Report B is a deep-research-skill pipeline output with self-assessment metadata. Both are comparable in length and scope. No material timing difference.

---

## Comparison purpose

Determine whether the gap between Report A (strong regulatory framework execution) and Report B (route-correct but contract-unexecuted) is already closed by the Phase A/B interventions (PR #354, PR #356), and whether any residual gaps from the paired comparison justify further action.

This artifact serves as a **regression baseline** for Issue #353 Phase C: most expected gaps should already be addressed by Phase A/B gates. The comparison verifies that the loop is closed and documents which interventions covered which failure patterns.

---

## Dimension 1: Current-state discipline

### Report A
- Separates current rules (32-team format, qualification allocation, group-stage mechanics under existing regulations) from pending decisions (48-team format details, confederation slot reallocation, group-size proposals not yet approved by FIFA Council).
- Dated regulatory snapshot with explicit FIFA Council decision chronology (2017: 48-team approved in principle; 2023: 3×16 format favored; 2025: slot allocation still in negotiation).
- Enforcement reality distinguished from letter of law: notes that FIFA decision-making is opaque, confederation politics influence outcomes, and scheduling constraints may override theoretical formats.

### Report B
- Current-state section exists but mixes enacted rules (32-team format, current qualification slots) with speculative future format details (3×16 vs 4×12 vs 8×6 group proposals) without consistent separation flags.
- The boundary between "expansion rules as enacted" and "still-in-flux design choices" is blurred — reader cannot always tell which statements describe current regulations and which describe proposed changes.

### Gap
- Report A has cleaner layer separation (enacted / pending / proposed / speculated). Report B merges these layers, reducing auditability of what is currently in force vs what is under discussion.

### Candidate action
- **No new action needed.** Phase B already addresses this via `checklists/regulatory-analysis-audit.md` (§Regulatory state verification), which requires: "current regulations are clearly separated from pending/in-progress legislation" and "regulatory snapshot is dated and sourced." A report following Phase B checklist would pass this gate. The gap is structural failure at the body level, not a missing rule.

### Action type
`NO_ACTION`

---

## Dimension 2: Numerical and date discipline

### Report A
- All quantitative claims carry explicit date context: "as of FIFA Council meeting March 2025," "per qualification slot allocation published June 2023," "under the current 32-team format (2018–2022 avg)."
- Exact figures used throughout (104→64 match reduction under 3×16 format, 48→80 match increase under 4×12, qualification slots by confederation with year labels).
- Explicit "Data as of: 1 June 2026" block in methodology section anchors all figures.

### Report B
- Numerical data present (32 vs 48 teams, match counts, qualification slots) but date-stamped inconsistently. Some figures from 2017 decisions sit alongside 2025 speculation without date markers.
- No explicit data-as-of anchor. Reader must infer recency from context.
- Qualification slot projections given without year basis or source date.

### Gap
- Report A consistently binds every figure to its temporal context. Report B has weaker date-binding — figures from different decision epochs are presented with uniform weight.

### Candidate action
- **No new action needed.** The repo's date-discipline references (`references/finance-date-discipline.md`, regulatory checklist §Regulatory state verification "regulatory snapshot is dated and sourced") already require explicit date anchors. Phase B market-outlook shared-axis rules also enforce comparable time bases for scenario metrics. Report B's failure is execution against existing gates, not a missing date-discipline rule.

### Action type
`NO_ACTION`

---

## Dimension 3: Source traceability and evidence weighting

### Report A
- Source register includes institutional sources (FIFA Council resolutions, FIFA Statutes, confederation documentation), media analysis (Reuters, BBC Sport, The Athletic), and academic/statistical references (CIES Football Observatory).
- Load-bearing claims carry inline citations. Source types are distinguishable (primary institutional vs secondary media vs expert commentary).
- Reasoning chains are visible: data source → analytical step → conclusion is traceable.

### Report B
- Source register is heavily Wikipedia/crowdsourced: 8/9 entries are Wikipedia or crowdsourced aggregators (source types: `CROWDSOURCED`, `wiki`, `WIKI`). Only S08 (FIFA official) is primary institutional. Load-bearing claims about FIFA Council decisions, qualification slot allocation, and match statistics rely on tertiary sources.
- Body has zero `[Sxx]` claim-level citations. Uses `[CONF]/[INFER]` as body-level annotation, which the repo's `checklists/source-traceability.md` explicitly states does not satisfy traceability requirements.
- Self-assessment claims source-traceability ✅ Passed, triggering declared-not-executed hard-fail.

### Gap
- This is the widest gap in the comparison. Report B fails on three independent axes: (a) no body-level `[Sxx]` citations, (b) `[CONF]/[INFER]` used as false proxy, (c) source pool is Wikipedia-dominated for load-bearing official claims. Self-assessment overclaim compounds the failure.

### Candidate action
- **No new action needed.** Phase B comprehensively addressed this gap via multiple interventions:
  - `checklists/source-traceability.md`: hard-fail gate explicitly rejects `[CONF]/[INFER]` as traceability substitute.
  - `checklists/source-traceability.md`: CROWDSOURCED + high reliability hard-fail.
  - `checklists/source-traceability.md`: source-strength purity gate (100% Wikipedia → hard-fail, >50% → warning).
  - `checklists/final-audit.md`: final audit requires `[Sxx]`, warns that `[CONF]/[INFER]` alone is insufficient.
  - `evals/cases/world-cup-expansion-regulatory-contract-and-source-fail-case.md`: documents all three failure axes as hard-fail patterns.
  - Phase C test `tests/test_issue_353_phase_c_contracts.py` C5: sports-themed source-strength fixtures prove the #341 validators work in sports contexts (100% Wikipedia fails, CROWDSOURCED+high fails, section-only Claims Supported fails, [确认事实] label mismatch fails).
  - No additional rules, checklist hardening, or template change is needed — the existing infrastructure captures this failure pattern at multiple enforcement points.

### Action type
`NO_ACTION`

---

## Dimension 4: Forward-looking claim discipline

### Report A
- Named sources for every forecast: FIFA President statements (source: FIFA.com, dated), Council meeting minutes, confederation proposals (CAF, UEFA, CONMEBOL positions identified by name).
- Distinguishes three status levels explicitly: **announced** (FIFA Council approved decisions), **proposed** (confederation submissions or working group recommendations), **speculated** (media analysis or expert opinion with source named).
- Failure conditions for each scenario clearly stated: "if FIFA cannot reach consensus on slot allocation by Q4 2025, the default 3×16 format becomes effectively locked."

### Report B
- Forward-looking claims intermixed with current-state description without status labels.
- Uncertainty expressed via "may" / "could" without naming the source of the projection.
- Scenarios exist (optimistic/base/pessimistic) but not clearly linked to specific decision-maker timelines or named sources.

### Gap
- Report A explicitly labels the status of every forward-looking claim. Report B treats all forward-looking content as undifferentiated analysis.

### Candidate action
- **No new action needed.** The repo already has `checklists/forward-looking-claims.md` which hard-fails forward-looking claims labeled `[CONF]` or without source attribution. The regulatory checklist requires "scenario analysis covers optimistic / base / pessimistic outcomes" and "monitoring signals are specified." Phase B's add-on reference further requires monitoring signals with threshold/cadence/source/trigger-to-action. Report B's failure is execution-level, not a missing forward-looking-claims gate.

### Action type
`NO_ACTION`

---

## Dimension 5: Structural readability and information density

### Report A
- Clean section progression: regulatory snapshot → state taxonomy (participant categories with strategy space) → intervention matrix (4 format alternatives with mechanism, side effects, monitoring, reversal) → three scenarios (bound to shared variables) → monitoring signals (threshold/cadence/source/trigger-to-action) → stakeholder action guidance.
- Each table serves one analytical purpose. The state taxonomy has 5 rows × 5 columns covering participant groups. The intervention matrix has 4 rows × 6 columns. No table exceeds visual density limits.
- Executive summary bullet points each carry one load-bearing insight.

### Report B
- Flat section structure: introduction → current rules → alternatives comparison (simple pros/cons table) → scenarios → conclusion.
- State taxonomy absent entirely — no participant categories, no strategy-space analysis.
- "Intervention matrix" in Report B is actually a flat alternatives table (48 vs 32 vs hybrid, with pros/cons per option). No mechanism analysis, no side effects beyond casual mention, no monitoring indicators, no reversal conditions.
- Rule-system add-on declared in plan (self-assessment) but not reflected in execution structure.

### Gap
- Report A's structure directly executes the add-on contract (state taxonomy + intervention matrix). Report B declares awareness of the add-on need but the output structure does not reshape to satisfy it. The flat alternatives table is the clearest symptom: it has the format of an intervention matrix (table with alternatives) but lacks the analytical content (mechanism traceability, side effects, monitoring, reversal).

### Candidate action
- `CHECKLIST_HARDENING` to `checklists/regulatory-analysis-audit.md` §Rule-system analysis. While Phase B already added state taxonomy and intervention matrix checks, this paired comparison reveals that the checklist items could be hardened to explicitly distinguish a flat alternatives table (feature comparison) from a qualified intervention matrix (mechanism traceability + side effects + monitoring + reversal). Adding a note like "intervention matrix entries must describe the causal mechanism, not just the expected outcome" would close the gap between formal compliance and substantive execution. This is a genuine improvement revealed by seeing how Report A structured its intervention traceability vs Report B's shallow alternative listing.

> **Note:** This candidate is included as an *observation* from the paired comparison, not a mandatory Phase C deliverable. The issue scope for Phase C explicitly excludes revisiting Phase A/B contracts. If adopted separately, it would be a minor checklist wording change (1–2 lines).

### Action type
`NO_ACTION` (out of Phase C scope — Phase A/B already addressed)

---

## Dimension 6: Decision usefulness

### Report A
- Decision frame made explicit: "FIFA faces a binding trilemma: competitive quality, global representation, and tournament feasibility cannot all be maximized simultaneously."
- Three load-bearing variables identified: competitive balance (measured by group-stage predictability), revenue distribution (per-match value × match count), qualification fairness (access vs merit weighting).
- Trade-offs mapped explicitly: 3×16 format maximizes feasibility but dilutes group-stage drama; 4×12 maximizes match inventory but requires 28-day tournament; 8×6 eliminates group-stage tension entirely.
- Bottom line: 3×16 format is the nearly inevitable outcome given binding scheduling constraints — specific identifiable stakeholder pressures make alternatives unlikely.
- Practical next checks listed: monitor FIFA Council slot-allocation decisions, confederation responses to draft proposals, player union positions on match load.

### Report B
- Trade-offs discussed but not distilled to a decision frame. Reader gets a list of pros and cons per format option but no binding constraint analysis.
- Multiple alternatives presented without prioritization. No "what this means for decision-makers" section.
- Bottom line less sharp — the report concludes expansion is "likely" without identifying the specific constraints that make one outcome more probable than others.
- Monitoring suggestions present but not structured into threshold-based triggers.

### Gap
- Report A provides actionable orientation (this is what FIFA must decide, these are the binding constraints, here is what to watch). Report B stays descriptive (here are the options, here are some pros and cons) without compressing to a decision-relevant bottom line.

### Candidate action
- **No new action needed.** The regulatory-analysis-audit checklist already requires "actionable conclusions for decision-makers" and "monitoring signals specified (what to watch for regulatory changes)." The add-on reference requires intervention matrix entries to include reversal conditions and monitoring indicators with trigger-to-action. Report B's flat descriptive structure is an execution failure against these existing gates, not proof that the gates are insufficient.

### Action type
`NO_ACTION`

---

## Candidate-action summary

| # | Candidate action | Failure family | Action type | Proposed home |
|---|---|---|---|---|
| 1 | Harden intervention matrix checklist item to distinguish flat alternatives table from qualified intervention matrix (mechanism traceability + side effects + monitoring + reversal) | output structure / information density | `NO_ACTION` | Out of Phase C scope — documented for future consideration in `checklists/regulatory-analysis-audit.md` |
| 2 | (Regression baseline only) All other gaps already covered by Phase A/B | — | `NO_ACTION` | eval only |

---

## Triage notes

### Why all candidates are NO_ACTION

Each gap identified in the original paired-report comparison has been systematically addressed by Phase A/B of the #353 workstream. This distillation exists to:

1. **Document that the loop is closed** — all known gaps from this paired comparison are now covered by rules, checklists, templates, or validator gates
2. **Provide a regression baseline** — if a future regulatory analysis report with rule-system add-on passes through the pipeline and still exhibits any of these gaps, that is a regression
3. **Distinguish rule gaps from execution gaps** — most gaps were execution/wiring gaps (rules existed but regulatory route and add-on execution was not verified against the body output), not missing rules

---

## Things explicitly rejected

| Observation | Why rejected |
|---|---|
| GPT report uses a more confident and assertive tone | Tone preference only — the repo guidelines already favor direct, actionable language. Tone differences between models are not a structural discipline gap. |
| GPT report includes a formal "Methodology and Data Limitations" section | Already covered by existing repo infrastructure (`references/quantitative-role-labeling.md`, `references/model-output-and-simulation-discipline.md`). The methodology block is a content decision, not a missing rule. |
| GPT report's state taxonomy labels participant groups differently | The specific taxonomy labels (top-tier federations, developing federations, commercial partners, players' unions) are domain knowledge, not structural discipline. The add-on template's generic format is intentional — domain-specific labels are the report author's responsibility. |
| GPT report uses diagrams for participant flow | The add-on reference explicitly says "不要求所有 regulatory 报告都画图表." Visual preference, not a rule gap. |

---

## Final judgment

### What the stronger report did better

Report A (GPT) executed the regulatory route contract end-to-end: it built a dated regulatory snapshot, constructed a domain-appropriate state taxonomy, produced an intervention matrix with causal mechanism traceability, drafted evidence-grounded scenarios, and defined actionable monitoring signals. The structural discipline translated regulatory **route awareness** into regulatory **artifact output**.

Report B (local deep-research-skill) correctly identified the same route and add-on, but the identification did not translate into body execution. The output stayed at the level of general analysis (alternatives comparison, informal scenarios, pros/cons) rather than regulatory artifact (state taxonomy, qualified intervention matrix, threshold-based monitoring).

### What should change in the repo now

All gaps are closed by Phase A/B gates. No new rules, new checklist items, or new evals are needed from this paired comparison's primary gaps. One minor checklist hardening observation (intervention matrix vs alternatives table distinction) is documented but explicitly marked as out of Phase C scope.

### What should wait for another confirming case

The flat-alternatives-table-as-intervention-matrix pattern. If a second rule-system add-on case (e.g., sports league regulation, auction design, incentive scheme evaluation) confirms the pattern, the checklist hardening should be promoted to `PROMOTE_NOW`.

### Is this mainly a missing rule, missing trigger, or execution problem?

**Execution problem** at the report level.

- Report B's failures (no state taxonomy, flat alternatives table, no `[Sxx]`, Wikipedia-dominated register, self-assessment overclaim) were all covered by existing Phase A/B gates at the time of evaluation. The problem was execution: the pipeline produced a report that formally checked the right route boxes without reshaping the body output to satisfy the route's artifact contract.
- No missing activation triggers identified — the route selection and add-on activation were correct. The failure is between route selection and route execution.

---

## Minimal quality bar

- [x] the two reports are comparable enough to justify distillation (same question, same timeframe, comparable scope)
- [x] the comparison used the six fixed dimensions
- [x] each accepted candidate has an action type
- [x] each accepted candidate has a proposed repo home
- [x] at least one rejected observation is documented when relevant
- [x] the final judgment distinguishes rule gap vs trigger gap vs execution gap
