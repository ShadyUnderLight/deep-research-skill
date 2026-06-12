# Comparative Distillation — MCP Protocol Technical Deep-Dive: deep-research-skill vs GPT-4o

## Case identity

- **Case name:** MCP protocol technical report comparative distillation
- **Date:** 2026-06-12
- **Research question:** Produce a structured technical deep-dive report on the MCP (Model Context Protocol) protocol — covering architecture, core mechanisms, capability boundaries, security risks, roadmap evaluation, and practitioner recommendations — using claim-level source traceability with a 7-column Source Register and Route-and-audit-status block.
- **Why this comparison matters:** Two reports on the same topic exposed complementary strengths and weakness that collectively define the quality target for technical-deep-dive reports. Neither alone satisfies all dimensions of the skill's delivery contract. The comparison reveals which gaps have been closed by recent rule changes (issues #242–#245) and which structural tensions remain.
- **Report A:** deep-research-skill output (post-review against the existing technical-deep-dive discipline, refined through issues #242–#245)
- **Report B:** GPT-4o deep research output (user-provided external comparison, same topic, no Source Register / Route-and-audit-status constraints)
- **Reference / stronger report (if any):** Neither is strictly stronger — each excels in complementary dimensions. The target state is a synthesis of both.
- **Prompt(s):** Same technical deep-dive task on MCP protocol. Report A used the deep-research-skill pipeline with route-specific discipline files and checklists. Report B used a general GPT-4o deep research session without the skill's structural constraints.
- **Important scope or timing differences:** Both reports analyze roughly the same protocol version window (2024Q4–2025H1). Report A was processed through the skill's audit pipeline and refined per #242–#245 rule changes. Report B is a one-shot GPT-4o output without post-processing. The comparison focuses on structural and disciplinary differences rather than factual accuracy.

---

## Comparison purpose

This comparison is **not** for ranking models or declaring a winner.

It is for:

- documenting which dimensions each report handled well, as a benchmark for the target state
- verifying that the rule changes from issues #242–#245 collectively close the gaps that the GPT comparison exposed
- identifying any remaining failure modes that are not yet covered by existing checklists or rules
- providing a historical record so future maintainers understand why the four MCP eval cases exist

> **INDEX.md note:** This file lives in `evals/comparative-distillation/` and is not added to `evals/INDEX.md`. Per `evals/README.md`, the index is synchronized with tracked case evals in `evals/cases/`. Comparative-distillation assets are tracked by the file listing alone, consistent with the 12 existing files in this directory.

---

## Dimension 1: Source Register / source traceability

### Report A
- Full 7-column Source Register (ID / Source Name / Source Type / Date / DOI or URL / Reliability / Claims Supported)
- Body uses `[Sxx]` inline citations for load-bearing claims
- Source types distinguished (spec, WG discussion, community implementation, blog, security advisory)

### Report B
- No structured Source Register — sources are mentioned inline where relevant
- No standardized citation format (some URLs embedded in text, some mentioned without verifiable links)
- Source roles not systematically distinguished; reader must infer credibility from context

### Gap
Report A satisfies the skill's source-traceability contract. Report B has better narrative flow but fails the auditability requirement: a reviewer cannot quickly verify which claim relies on which source, and some claims have no visible source at all.

### Candidate action
No new action needed. The existing source-traceability discipline (`checklists/source-traceability.md`, `references/source-traceability-and-claim-citation.md`) already requires 7-column Source Register + `[Sxx]` inline citations. The `technical-analysis-audit.md` checklist enforces this for the technical-deep-dive route.

### Action type
`NO_ACTION`

---

## Dimension 2: Route and audit status / self-assessment consistency

### Report A
- Explicit Route and audit status block with per-discipline statuses (route activation, source traceability, current-state verification, forward-looking claims, technical analysis, final audit)
- Each discipline's audit run status is visible with evidence column
- Self-assessment is generally consistent with body execution

### Report B
- No Route and audit status block
- No explicit self-assessment against the skill's discipline taxonomy
- Reader cannot tell which quality gates were (or were not) applied

### Gap
Report B lacks any auditability structure. This is the core difference: Report A makes its quality gates visible, Report B relies on the reader's trust. The existing `final-audit.md` process-integrity gate (§Process-artifact sufficiency, item "Process-integrity gate") and the Route and audit status template already enforce this for Report A. Report B fails any delivery gate that requires audit visibility.

A subtler gap that the comparison reveals: **cross-dimensional self-assessment consistency**. A report could pass each individual dimension check but have its audit block show all "passed" while the actual body evidence is thin or internally contradictory (e.g., timeline integrity claims pass while using inconsistent dates between dimensions). The existing individual dimension checks might not catch this gestalt pattern.

### Candidate action
The existing process-integrity gate (§Process-artifact sufficiency in `final-audit.md`) already requires each "passed" claim to have visible body evidence. This covers the multi-dimensional case because each claimed pass must independently show evidence. However, an explicit cross-DIMENSION consistency reminder would strengthen the gate: when 3+ audit dimensions all claim "passed", verify that their evidence bases are mutually consistent (not contradictory dates, overlapping source bases that tell different stories, etc.).

### Action type
`CHECKLIST_HARDENING` — add a (non-blocking) reminder in `final-audit.md` §Process-artifact sufficiency near the existing process-integrity gate: when 3+ audit dimensions claim passed, spot-check cross-dimensional evidence consistency.

---

## Dimension 3: Technical audience / decision scenario

### Report A
- Opening baseline block (per `references/report-template.md` §Technical deep-dive opening) includes target audience and decision scenario
- Reader knows who the report is for and what decision it supports

### Report B
- No explicit audience definition — the report starts directly with technical description
- No decision scenario — the report reads as a comprehensive survey rather than a decision-support artifact
- Reader must infer their own use case

### Gap
Report B provides more actionable practitioner guidance overall, but without framing the audience and decision scenario, the reader cannot calibrate which parts of the analysis are most relevant to their role. Report A's opening block (mandated by issue #242) solves this at the structural level.

### Candidate action
No new action needed. Issue #242 already added the opening baseline requirement to `references/report-template.md` and `checklists/technical-analysis-audit.md`.

### Action type
`NO_ACTION`

---

## Dimension 4: Version baseline / temporal consistency

### Report A
- Explicit report date, stable specification version, latest verification date, forward-looking boundary
- Coverage date is internally consistent with source timeline
- Stable baseline capabilities are separated from roadmap/experimental content

### Report B
- No explicit version baseline block — the temporal anchor must be inferred from context
- Current-state analysis, roadmap discussion, and speculative ideas are mixed in the same narrative flow
- Stronger on individual technical judgments, but the reader cannot distinguish "available now" from "planned" without cross-referencing external sources

### Gap
Report B has stronger engineering judgment per claim, but the lack of temporal anchoring makes it harder to use as a decision document. The reader cannot quickly tell whether "MCP supports X" is a current specification capability or a roadmap goal.

### Candidate action
No new action needed. Issue #242 (opening baseline) and #243 (roadmap state stratification) already enforce this separation through the `technical-analysis-audit.md` checklist.

### Action type
`NO_ACTION`

---

## Dimension 5: Roadmap state stratification

### Report A
- Roadmap items separated by commitment state (shipped / announced / roadmap priority / speculative / non-commitment)
- Each roadmap claim labeled with its temporal status and confidence
- Route conflict check documented

### Report B
- Roadmap discussion is more detailed and better connected to technical analysis
- But roadmap items are not systematically separated by commitment state
- "MCP plans to support X" and "the community is discussing Y" appear alongside stable capabilities without reader-visible state labels

### Gap
Report B's roadmap analysis is richer in technical detail, but Report A's stratification discipline makes the reliability of each roadmap claim auditable. Issue #243's rules require the stratification that Report A implements. Report B would fail the `technical-analysis-audit.md` checklist item on roadmap state separation.

### Candidate action
No new action needed. Issue #243 already added roadmap state stratification to `checklists/technical-analysis-audit.md` and `references/technical-analysis-discipline.md`.

### Action type
`NO_ACTION`

---

## Dimension 6: Threat model / security architecture

### Report A
- Security analysis organized as risk item descriptions with individual explanations
- Uses the technical-analysis discipline's security deep-dive checklist (per issue #244)
- Includes assets, trust boundaries, threat actors, risk priority matrix, engineering controls tiering, detection signals

### Report B
- Security section structured as an engineering-review-ready threat model
- Assets, trust boundaries, and threat actors are explicitly defined
- Risks are prioritized (likelihood × impact) with engineering controls (prevent/detect/respond)
- Detection signals are concrete (metrics, thresholds, data sources)
- Risk types differentiated (protocol design vs. implementation vs. deployment vs. supply chain)

### Gap
Report B's security analysis is more actionable for a security engineer audience, because the output structure itself reveals the threat model architecture rather than just explaining risks individually. Issue #244 added the security deep-dive checklist to `technical-analysis-audit.md` that requires the threat model structure Report B demonstrates.

### Candidate action
No new action needed. Issue #244 already added the security deep-dive checklist (`checklists/technical-analysis-audit.md` §Security deep-dive) that requires assets, trust boundaries, risk prioritization, control tiering, and detection signals.

### Action type
`NO_ACTION`

---

## Dimension 7: Architecture comparison role / load-bearing trade-offs

### Report A
- Comparison dimensions are explicit and dimension-by-dimension
- Each comparator's role is visible (substitute / complement / ancestor / excluded)
- After-table trade-off interpretation identifies load-bearing dimensions
- Reversal conditions stated

### Report B
- Comparison is richer in technical insight per dimension
- But comparator roles are implicit — reader must infer whether MCP, A2A, and Function Calling are substitutes, complements, or incomparable
- No systematic trade-off interpretation block after the comparison table
- Recommendation is strong but does not explicitly state reversal conditions

### Gap
Report B has stronger individual comparison insights, but the comparison structure is less auditable. Issue #245's comparator role requirement ensures the reader understands the relationship between alternatives, not just their feature differences. Report A's structured comparison (per issue #245 rules) makes the architecture analysis transparent.

### Candidate action
No new action needed. Issue #245 already added comparator role and load-bearing trade-off requirements to `checklists/technical-analysis-audit.md` §Comparison structure and `references/technical-analysis-discipline.md`.

### Action type
`NO_ACTION`

---

## Dimension 8: Engineering control actionability

### Report A
- Security controls are listed with prevent/detect/response tiering
- Each control's availability is noted (readily available / requires customization / conceptual)
- Detection signals include concrete metrics and thresholds
- Short/medium/long-term roadmap for security improvements

### Report B
- Engineering recommendations are more specific and action-oriented
- Better at connecting technical risks to concrete operational recommendations
- But lacks the systematic tiering structure that Report A's security deep-dive checklist enforces

### Gap
Report B's individual recommendations are stronger, but Report A's systematic structure makes the controls auditable and complete. Issue #244's security deep-dive checklist ensures no control type is systematically missing. The ideal is Report B's specificity within Report A's structural framework.

### Candidate action
No new action needed. Issue #244's security deep-dive checklist already requires prevent/detect/response tiering and concrete detection signals.

### Action type
`NO_ACTION`

---

## Candidate-action summary

| # | Candidate action | Failure family | Action type | Proposed home |
|---|---|---|---|---|
| 1 | Source Register 7-column template + `[Sxx]` body citations for technical-deep-dive | source-traceability | NO_ACTION | already in `checklists/source-traceability.md`, `checklists/technical-analysis-audit.md` |
| 2 | Opening baseline (audience, decision scenario, version baseline) | technical-deep-dive artifact contract | NO_ACTION | already in `references/report-template.md`, `checklists/technical-analysis-audit.md` (#242) |
| 3 | Roadmap state stratification (shipped/announced/speculative) | forward-looking / roadmap discipline | NO_ACTION | already in `checklists/technical-analysis-audit.md`, `references/technical-analysis-discipline.md` (#243) |
| 4 | Security deep-dive: threat model with assets, trust boundaries, risk matrix, control tiering, detection signals | security deep-dive | NO_ACTION | already in `checklists/technical-analysis-audit.md` §Security deep-dive (#244) |
| 5 | Architecture comparison: comparator roles, load-bearing trade-offs, reversal conditions | architecture comparison | NO_ACTION | already in `checklists/technical-analysis-audit.md` §Comparison structure (#245) |
| 6 | Cross-dimensional self-assessment consistency check when 3+ audit dimensions claim passed | self-assessment consistency | CHECKLIST_HARDENING | `checklists/final-audit.md` §Process-artifact sufficiency (near existing process-integrity gate) |

---

## Triage notes

### Candidate 1–5
- **Why they are NO_ACTION:** Each gap identified by the MCP report comparison corresponds to a rule change already made in issues #242–#245. The existing checklists, references, and templates already enforce the required behaviors. This comparative distillation serves as validation evidence that the rule set is sufficient.
- **Promotion status:** `ALREADY_PROMOTED` (via #242–#245)

### Candidate 6
- **Why it matters:** The comparison revealed that while individual dimension checks are robust, a report could theoretically pass each check independently while having audit claims that are mutually inconsistent (e.g., timeline integrity claims passed with one date anchor, opening baseline claims passed with a different date anchor). This is an edge case but represents a real integration-level failure mode that none of the existing checks explicitly target.
- **Why it is reusable:** Cross-dimensional consistency applies to any report with 3+ audit dimensions claiming passed status — which includes most technical-deep-dive and listed-company reports.
- **Why this home is best:** The existing process-integrity gate in `final-audit.md` §Process-artifact sufficiency is the natural home for this reminder. It would be a (non-blocking) amplification of the existing "each claimed pass must have visible body evidence" rule, adding a cross-referencing step.
- **Promotion status:** `WAIT_FOR_SECOND_CASE` — this is a genuine gap but has not yet caused a real delivery failure. Promote if a second similar case surfaces.

---

## Things explicitly rejected

| Observation | Why rejected |
|---|---|
| GPT reports are "better" overall | Not actionable — the comparison is about complementary strengths, not a single ranking |
| Report B should adopt Report A's exact Source Register format | The format is already mandated; no new rule needed |
| Report A should copy Report B's writing style for engineering recommendations | Style preference, not a structural rule |
| The comparison proves the skill is now complete | No single comparison proves completeness across all routes and failure families |
| Add an automated cross-dimensional consistency validator | Premature—only one known pattern (the MCP case), no repeated failure data; too speculative for automation |

---

## Final judgment

### What the stronger report did better for each dimension
- **Report A** was stronger on: Source Register discipline, Route and audit status transparency, opening baseline framing, temporal consistency, roadmap state stratification, comparison structure transparency, security control tiering structure, self-assessment honesty.
- **Report B** was stronger on: engineering judgment specificity per dimension, threat model depth, architecture insight quality, recommendation actionability, detection signal concreteness.
- **The target state** is Report A's structural discipline + Report B's engineering judgment depth. Issues #242–#245 have closed the structural gaps; the remaining work is execution quality within that structure.

### What should change in the repo now
- Nothing new. The rule changes from #242–#245 (opening baseline, roadmap stratification, security threat model, architecture comparison roles) collectively cover the gaps that this comparison exposed. This file serves as the validation record.

### What should wait for another confirming case
- **Candidate 6** (cross-dimensional self-assessment consistency reminder in `final-audit.md`) should wait for a second real case before promoting from `WAIT_FOR_SECOND_CASE`.
- Any automation (scripts) for cross-dimensional consistency checking should wait for repeated failure data.

### Is this mainly a missing rule, missing trigger, or execution problem?
This is primarily a **validation and documentation** case. The rules were not missing — they were added through #242–#245. The MCP report comparison validates that the rule set is complete enough to block the failure modes identified by the GPT comparison. The one remaining gap (cross-dimensional self-assessment consistency) is a minor `CHECKLIST_HARDENING` opportunity rather than a missing rule.

---

## Minimal quality bar

- [x] the two reports are comparable enough to justify distillation (same MCP protocol deep-dive task)
- [x] the comparison used eight custom dimensions covering source traceability, self-assessment consistency, audience framing, temporal consistency, roadmap stratification, threat model architecture, comparison structure, and engineering control actionability — adapted from the template's six-dimension framework to fit technical-deep-dive route specifics
- [x] each accepted candidate has an action type (NO_ACTION or CHECKLIST_HARDENING)
- [x] each accepted candidate has a proposed repo home
- [x] at least one rejected observation is documented
- [x] the final judgment distinguishes rule gap vs trigger gap vs execution gap
- [x] the document explicitly maps each dimension to its corresponding issue #242–#245 rule change
- [x] no GPT report text is copied into the repository
