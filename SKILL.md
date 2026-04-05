---
name: deep-research
description: Conduct structured multi-step research for complex questions, decision support, market/company/technical analysis, competitive scans, and fact-checked briefings. Use when the user needs more than a quick answer and the task benefits from explicit planning, source comparison, verification, counter-evidence, uncertainty handling, and a structured final report.
---

# Deep Research

Run research as a staged decision-support workflow, not a search-and-summarize pass.

## Core rule

Research is not just collecting information. First identify what decision, judgment, or understanding the user actually needs. Then gather and test evidence against that goal.

Always distinguish:

- confirmed facts
- likely inference
- open uncertainty

Never present inference as confirmed fact.

## Workflow

1. clarify the real objective
2. classify the task
3. produce a compact research plan
4. define evidence standards and stop conditions
5. collect and compare sources
6. run a mid-research review
   - read `references/mid-research-review.md` once the first meaningful evidence batch is in hand
   - the review must visibly confirm, narrow, redirect, or stop the research path
7. search for counter-evidence
8. synthesize into a decision-oriented report

## Routing rule

Before deep collection, determine:

- the primary route
- the required secondary disciplines
- the visible artifact contract the final report must satisfy

Read `ROUTING-MATRIX.md` to select:

- the primary route
- required secondary disciplines
- required audits
- visible output structure

Use one primary route plus only the smallest necessary supporting set.

If multiple routes apply, choose the route that most strongly determines:

- report structure
- evidence burden
- audit burden

## Core shared disciplines

Apply these when the route requires them:

- current-state verification
- source traceability
- forward-looking claims discipline
- quantitative role labeling
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
Read `references/task-types.md` when the task needs a domain-specific question set.
Read `references/comparative-distillation-method.md` when comparing paired reports to turn stronger-vs-weaker outputs into reusable changes.
Use `evals/comparative-distillation-template.md` to record paired-report comparisons so extracted patterns land as `NEW_RULE`, `CHECKLIST_HARDENING`, `TEMPLATE_CHANGE`, or `NO_ACTION`.

Stop searching when one of these is true:

- the main question is answered with adequate confidence
- new searches mostly repeat prior findings
- remaining uncertainty is due to unavailable data, not lack of effort

Do not keep searching just to make the report longer.

## Tool strategy

Use tools deliberately.

- `web_search`: discover candidate sources and comparison angles
- `web_fetch`: extract readable page content
- `browser`: handle dynamic pages or failed fetches
- `sessions_spawn`: split clearly separable tracks only
- final synthesis: always perform one parent-level reconciliation pass

Avoid unnecessary browsing loops, repetitive searches, or unstructured parallel runs.

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

Default delivery stays as text or markdown.

If the user's request includes `pdf`, `PDF`, or `报告`, also produce a PDF artifact:

1. write the final report to a `.md` file first
2. convert it with `scripts/md_to_pdf.py`
3. deliver the PDF when the surface supports files

The markdown file remains the source of truth.

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
2. run `checklists/final-audit.md`
3. confirm that the selected route is visibly executed in the final artifact

A report that sounds informed but does not visibly satisfy the selected route’s artifact contract is not ready.

If the failure seems to be:
- missing rule
- missing trigger
- or execution drift

use `evals/rule-activation-and-execution-discipline.md`.

## Output quality bar

A strong final answer should:

- answer the actual question, not just summarize the topic
- show how the conclusion was formed
- separate fact from inference
- surface counter-evidence
- state confidence clearly
- explain what is still missing
- help the user decide what to do next

If confidence is limited, say exactly why.
