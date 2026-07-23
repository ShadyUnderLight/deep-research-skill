---
name: deep-research
description: Conduct structured multi-step research for complex questions, decision support, market/company/technical analysis, competitive scans, and fact-checked briefings. Use when the user needs more than a quick answer and the task benefits from explicit planning, source comparison, verification, counter-evidence, uncertainty handling, and a structured final report.
---

# Deep Research

Run research as a staged decision-support workflow, not a search-and-summarize pass.

## Core rule

Research is not just collecting information. First identify what decision, judgment, or understanding the user actually needs. Then gather and test evidence against that goal.

Always distinguish:

- 确认事实
- 推断
- 未知

永远不要将推断呈现为确认事实。

## Workflow

1. clarify the real objective
2. classify the task
3. produce a compact research plan
4. define evidence standards and stop conditions
5. if live search, source fetching, browser access, or parallel agents may be needed, run tooling preflight to confirm what is available; if a needed capability is missing, note it and adjust the search strategy before starting collection. When the environment has a local Research API (e.g. Agent-Reach), read `references/external-channel-preflight.md` for channel-specific preflight rules.
6. collect and compare sources
7. run a mid-research review
   - read `references/mid-research-review.md` once the first meaningful evidence batch is in hand
   - the review must visibly confirm, narrow, redirect, or stop the research path
8. search for counter-evidence
9. synthesize into a decision-oriented report

## Routing rule

Before deep collection, determine:

- the primary route
- the required secondary disciplines
- the visible artifact contract the final report must satisfy

For route selection, first read `references/route-index.md` for a compact trigger table (one short read to locate the candidate route). Then read `ROUTING-MATRIX.md` for the full route contract including:

- the primary route
- required secondary disciplines
- required audits
- visible output structure

Read `references/route-activation-and-preflight.md` when a specialized route is being considered, and complete its preflight steps before finalizing route selection:
- "Do not use" / "Often confused with" clause check
- secondary-route hard-fail verification
- route declaration scale check
- execution contract formation

Before deep collection, explicitly select one primary route. If no mature specialized route applies, treat the task as a shared-workflow task (the delivery-time final discipline handles audit selection: see step 3 and 6 below).

Use one primary route plus only the smallest necessary supporting set.

If multiple routes apply, compare the closest two and choose the one that most strongly determines:

- report structure
- evidence burden
- audit burden

Do not default to generic research just because multiple routes sound partially relevant.

## Core shared disciplines

Apply these when the route requires them:

- current-state verification
- source traceability
- forward-looking claims discipline
- quantitative role labeling
- scope completeness
- decision utility
- delivery cleanliness
- target-language coherence for final delivery when the report is user-facing

Do not assume these are implied. If the route needs them, make them visible in the final output.

## Research plan

Before searching, write a compact internal plan with:

- objective
- decision context
- task type
- core subquestions
- likely source types
- evidence threshold
- likely failure modes
- stop conditions
- what would count as a strong answer

Prefer a small number of high-value questions over a long list of generic ones.

When creating a Research Pack (see below), it absorbs the Research Plan —
do not write a separate plan. For tasks not requiring a Research Pack,
use this lightweight plan as described.

## Research Pack

For tasks that carry significant route, audit, recommendation, or uncertainty burden,
create a Research Pack as a process artifact.
Read `references/research-pack-contract.md` for the contract and `schemas/research-pack.md` for the field schema.

The Research Pack is not the user-facing deliverable. It is a compact internal record that makes
route selection, source decisions, claim support, uncertainty handling, counter-evidence
consideration, and audit readiness more recoverable than final prose alone.

### When to create

Create a Research Pack when the task meets **any** of:
- a specialized route is selected (any of the 11 routes in `ROUTING-MATRIX.md`)
- the task involves recommendation, comparison, or go/no-go judgment
- the task is forward-looking (forecasts, roadmaps, target dates, projections)
- the task is uncertainty-sensitive (high stakes, ambiguous data, conflicting sources)

A Research Pack is optional (but recommended as an internal aid — use
`references/research-pack-contract.md` as a guide) when:
- the task is a lightweight fact query with no route or audit burden
- the task clearly fits shared-workflow with minimal discipline requirements

### Lifecycle

1. **After route selection and before evidence collection** (workflow step 3–4):
   Create the Research Pack as a `.md` file alongside the final report
   (e.g., `<report-name>-research-pack.md`). Write at minimum:
   - Objective, Decision context
   - Primary route, Closest alternative route and boundary judgment
     (why the primary route was chosen over the alternative; verify the alternative's
     "Do not use" / "Often confused with" clauses per
     `references/route-activation-and-preflight.md`)
   - Secondary disciplines
   - Core subquestions, Stop condition
   - Artifact contract, Required audits (as listed in `ROUTING-MATRIX.md` for the selected route)
   - Channel availability snapshot (if API preflight was run — see `references/external-channel-preflight.md`)
   - Leave Source register, Claim register, Uncertainty register, Counter-evidence log blank for now

2. **At mid-research review** (workflow step 7):
   After reading `references/mid-research-review.md`, update the Research Pack with:
   - Current best answer and search decision (confirm / narrow / redirect / stop)
   - If the decision is **redirect**, re-run route preflight:
     check "Do not use" / "Often confused with" clauses in
     `references/route-activation-and-preflight.md`, update Primary route,
     Closest alternative, and Required audits accordingly, and document the
     redirect reason in the Research Pack.
   - Source register (key sources found so far, with what each supports)
   - Degraded-search log (if fallback was used — record provider path, trigger reason, and
     what remains unverified)
   - Populate the Uncertainty register (unresolved items and why they matter)

 3. **Before final audit** (after synthesis, before running the Final discipline audits below):
    Close the remaining registers:
    - Claim register: load-bearing claims with evidence references ([Sxx], [Uxx])
    - Counter-evidence log: what could weaken, delay, qualify, or overturn the answer
    - Final audit status: see below

### Validation

Before delivery (as part of Final discipline, after all registers are closed),
run strict validation that checks source IDs, claim references, and audit status
consistency:
```bash
python3 scripts/validate_research_pack.py <pack-file>.md --strict
```

If strict validation fails, fix the issues before proceeding. A validator-based audit
check takes precedence over prose self-assessment. Do not claim Pass in the final
report's Route and audit status block without validator evidence.

### Final audit status

Set the Final audit status based on **both** validator evidence and audit execution
evidence — not on validator alone:

- **Pass**: strict validation passes AND every Required audit was executed with
  documented evidence (passed / skipped-with-reason).
- **Partial**: strict validation passes but some Required audits were skipped or not run
  with documented reason, OR strict validation has warnings but no errors.
- **Fail**: strict validation fails (structural or semantic errors) OR a Required audit
  was not run without documented reason.

If a Required audit was declared but never executed, do not claim Pass regardless of
validator outcome. Record each Required audit with its run status — passed, skipped
(with reason), or not-run (with reason) — in the Required audits section of the
Research Pack.

### Blocked, partial, and not-run states

Distinguish these status types so tool failures are not misrecorded as evidence failures:

| State type | Where recorded | Format example |
|---|---|---|
| Provider blocked | Degraded-search log | `provider blocked: Agent-Reach API unreachable (connection refused)` |
| Channel degraded | Degraded-search log | `channel degraded: Exa search quota exhausted, fell back to browser-based discovery` |
| Audit not-run | Required audits | `regulatory-analysis-audit — not-run: task completed before audit was available` |
| Audit partial | Required audits | `source-traceability checklist — partial: [S02] source page 404, cannot verify claim C3` |
| Content quality failure | Final audit status | `Fail: 3 undefined source IDs ([S05], [S07], [S09])` |

These states are distinct from "evidence is weak" or "confidence is low" — they record
why a tool, channel, audit, or validation step could not complete, not why the evidence
itself is insufficient.

Two conditional Pack fields add formal layers: **Research status**
(`complete` / `partial` / `blocked`) for process completion, and
**Delivery status** (`md_ready` / `pdf_ready` / `pdf_failed` / `not_run`)
for rendering outcome. Both are independent from content quality
(`Final audit status`). See `schemas/research-pack.md` for the
full schema.

## Evidence standards

For key claims, prefer:

1. official or primary sources
2. direct technical documentation
3. reputable institutional or regulatory reporting
4. strong secondary analysis
5. forum or social discussion only as supplemental context

For every important claim, capture:

- source title
- URL
- source type
- publication date if available
- the exact claim supported
- short evidence note
- confidence
- why it matters

Read `references/source-quality.md` when source ranking is ambiguous.
Read `references/claim-matrix.md` when the task has multiple important conclusions, conflicting evidence, or high stakes.
Read `references/data-conflict-resolution.md` when multiple sources provide contradictory data for the same fact or metric.
Read `references/task-types.md` when the task needs a domain-specific question set.
Read `references/moat-monopoly-screening.md` when the task screens or ranks listed companies using monopoly, irreplaceability, scarcity, strongest moat, or only-listed-proxy language.
Read `references/comparative-distillation-method.md` when comparing paired reports to turn stronger-vs-weaker outputs into reusable changes.
Use `evals/templates/comparative-distillation-template.md` to record paired-report comparisons so extracted patterns land as `NEW_RULE`, `CHECKLIST_HARDENING`, `TEMPLATE_CHANGE`, or `NO_ACTION`.

Stop searching when one of these is true:

- the main question is answered with adequate confidence
- new searches mostly repeat prior findings
- remaining uncertainty is due to unavailable data, not lack of effort

Do not keep searching just to make the report longer.

## Tool strategy

**Do not assume a specific default search provider. Before live search, inspect what search / fetch / browser capabilities are available in the current environment: use formal tooling preflight if it exists, otherwise make the selected provider path explicit in the research plan or evidence log.**

When a research task needs live web search:

1. select one provider path based on expected query fit and use it for discovery and comparison-angle finding
2. use readable content-fetch capability only after a candidate URL is identified (e.g. `web_fetch`, MCP fetch, HTTP fetch when it captures final page content/status and usable source text)
3. use dynamic-browser capability only when the page requires JS rendering or fetch alone fails (e.g. `browser`, Playwright, headless Chrome)

If the selected provider path is unavailable, do not silently fall back to another provider without explicit justification. Only add another provider when degradation, low yield, or query-fit mismatch is explicitly identified.

For the full degraded-search fallback policy (14-step chain), execution discipline, evidence log format, tool capability mapping, and environment-specific invocation, read `references/search-provider-fallback.md`.

For channel-specific preflight rules when a local Research API (Agent-Reach) is available, read `references/external-channel-preflight.md`.

Final synthesis: always perform one parent-level reconciliation pass. Avoid unnecessary browsing loops, repetitive searches, or unstructured parallel runs.

## Current-state verification

When the task is time-sensitive, verify the current state before forming conclusions.

Typical triggers include:

- latest products or versions
- current pricing
- current provider state
- current company status
- current market snapshot
- current rankings or positioning

If current state cannot be verified, say so clearly instead of filling gaps with likely-but-stale knowledge.

For listed-company or investment-style research, treat current-state verification as a hard gate rather than a general reminder.

Before broad company analysis, explicitly confirm:

- latest full-year reported period
- latest quarterly / interim reported period
- latest current market snapshot date
- latest management / leadership state when decision-relevant
- whether the opening section is anchored on those latest periods rather than on an older but easier-to-find snapshot

If the report date is materially later than the supposedly "latest" figures used in the memo, stop and re-check freshness before continuing.

Fail-fast rule for listed-company work:
- if the research-anchor block contains a quarterly / interim period that is materially inconsistent with the report date or likely filing calendar
- or if the agent cannot defend why that period is still the newest reasonably available layer
- do not continue synthesis as if the anchor were acceptable
- stop, re-check, and either fix the anchor or state explicitly that the latest quarter could not be verified

Do not let an older but well-structured company snapshot become the de facto current baseline just because it is easier to retrieve.
Do not let a polished research-anchor block create false trust when one of its time layers is stale or mis-timed.

Route-specific current-state requirements are defined in `ROUTING-MATRIX.md`.

## Mid-research review

After the first meaningful batch of evidence, pause and reassess:

- current best answer
- strongest evidence so far
- key missing evidence
- whether the search strategy should change
- whether low-value branches should be cut

Do not continue gathering information blindly once the shape of the answer is clear.

## Counter-evidence

For every load-bearing conclusion, actively look for evidence that could weaken or overturn it.

At minimum, check for:

- direct criticism or failure cases
- contradictory primary evidence
- competing explanations
- edge cases, legal constraints, operational failures, or user complaints

Read `references/counter-evidence.md` when the topic is contentious, commercial, fast-moving, or high stakes.

Never treat the first plausible story as the final one.

## Synthesis

Use `references/report-template.md` by default.

Use `references/decision-report-template.md` when the task needs:

- recommendation
- go / no-go view
- prioritization
- comparison
- action guidance

For listed-company / investment-style work, also use:
- `examples/listed-company-judgment-memo-example.md` as the default positive memo shape
- `examples/china-shenhua-reference-grade-rewrite-skeleton.md` when a more concrete Chinese listed-company reference skeleton would help keep the opening judgment-first
- `references/valuation-methodology.md` when making valuation judgments or using target prices
- `references/analyst-consensus-handling.md` when consensus data, target prices, or analyst ratings appear
- `references/reporting-period-handling.md` when using reported financials, TTM/NTM, or comparing multiple periods

These three references are complementary to `references/finance-date-discipline.md` — they cover methodology, data handling, and period definitions rather than time-layer labeling.

The report should not just summarize the topic. It should help the user decide, judge, or verify what matters next.

For most tasks, include:

1. executive summary
2. what matters most
3. key findings
4. detailed analysis
5. risks and counter-evidence
6. uncertainty and missing evidence
7. bottom line
8. sources

## Delivery rule

Default delivery stays as text or markdown. Produce a PDF artifact only when the user's request shows explicit file-delivery intent (e.g. "生成 PDF", "导出 PDF", "作为附件给我").

For the complete PDF delivery trigger keywords, negation guard list, and pipeline steps, read `references/delivery-operator-note.md`.

If PDF rendering fails, still deliver the markdown or text report and explicitly say the PDF export failed.

## Parallelization

Only parallelize when the topic clearly splits into distinct tracks and each track can be researched independently enough to justify coordination cost.

Good examples:

- market size
- competitors
- technical feasibility
- regulation
- customer demand signals

When parallelizing:

- split into 2–4 tracks
- keep each track narrow
- require structured findings, not polished prose
- require explicit source URLs
- require separation of confirmed facts vs inference
- reserve final synthesis for the parent agent

Read `references/parallel-research.md` when the task clearly benefits from multi-track work. Keep rate-limit risk in mind and prefer small batches over naive full parallelism.

## Final discipline

Before delivery:

1. run the route-specific audits required by `ROUTING-MATRIX.md`
2. run `checklists/route-activation-audit.md` when a specialized route was selected
3. run `checklists/workflow-spine-audit.md`
3a. if a Research Pack was created for this task, validate it before proceeding:
    ```bash
    python3 scripts/validate_research_pack.py <pack-file>.md --strict
    ```
    if validation fails, fix the Research Pack before continuing; the Final audit
    status in the Research Pack must not claim Pass without passing strict validation
4. run `checklists/final-audit.md`
5. confirm that the required artifact contract is visibly satisfied:
   - if a specialized route was selected, confirm the route's artifact contract is visibly executed in the final artifact
   - if no specialized route applies (shared-workflow path), confirm the shared workflow spine is visibly executed instead
6. verify that all required audits for the task have been executed, with each audit's run status recorded:
   - if a specialized route was selected, list all audits listed in its `### Audit` section in `ROUTING-MATRIX.md`
   - if no specialized route applies (shared-workflow path), list at least `workflow-spine-audit.md` and `final-audit.md`
   - for each listed audit, confirm one of these statuses: **已通过** (passed, with evidence visible in the standardized route-and-audit-status block in the artifact — see `references/report-template.md` §Route and audit status — or in the process log), **已跳过（附理由）** (skipped, with documented reason), or **未运行（附理由）** (not run, with documented reason)
   - if any required audit is missing or not run, run it before proceeding, or document the reason (skipped / not run / not applicable)

A report that sounds informed but does not visibly satisfy its required artifact contract (route-specific or shared-workflow) is not ready.

If the failure seems to be:
- missing rule
- missing trigger
- or execution drift

use `evals/meta/rule-activation-and-execution-discipline.md`.

If no mature specialized route applies, treat the task as a shared-workflow task — the workflow-spine audit (already run in step 3) replaces route-specific checks; skip the route-dependent parts of steps 5 and 6.

## Output quality bar

A strong final answer should:

- answer the actual question, not just summarize the topic
- show how the conclusion was formed
- 区分事实与推断
- surface counter-evidence
- state confidence clearly
- explain what is still missing
- help the user decide what to do next

If confidence is limited, say exactly why.

If a Research Pack should have been created under the trigger conditions but was not,
record this in the internal Research Pack (or in the Final discipline log if no pack exists)
as a noted gap — do not silently omit it.
