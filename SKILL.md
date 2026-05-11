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
5. if live search, source fetching, browser access, or parallel agents may be needed, run tooling preflight to confirm what is available; if a needed capability is missing, note it and adjust the search strategy before starting collection
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

Read `ROUTING-MATRIX.md` to select:

- the primary route
- required secondary disciplines
- required audits
- visible output structure

Before deep collection, explicitly select one primary route.

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
2. use `web_fetch` only after a candidate URL is identified
3. use `browser` only when the page is dynamic or `web_fetch` fails on a confirmed-live URL

If the selected provider path is unavailable, do not silently fall back to another provider without explicit justification. Only add another provider when degradation, low yield, or query-fit mismatch is explicitly identified.

If degraded search is needed, use this fallback policy:
1. first distinguish temporary rate-limit / quota issues from broader provider unavailability
2. if live search is still unavailable, declare the search provider degraded in the evidence log
3. if `agent-reach` Exa search is available in the current environment, use it as the first explicit degraded fallback for discovery and comparison-angle finding
4. current fallback implementation for that path (example for one environment; adjust the command to match your environment):

```bash
mcporter call 'exa.web_search_exa(query: "<search query>", numResults: 5)'
```

5. prefer the Exa fallback when the query is primarily about English-language material, technical documentation, developer tooling, code context, company pages, or broad web discovery
6. Exa is not automatically better for every case; if the task is dominated by Chinese-language news flow, localized platform chatter, or a search intent that clearly needs browser-side localization, note that and move on rather than forcing Exa first
7. treat Exa result pages as candidate-source discovery only, not as evidence for memo claims
8. re-verify any load-bearing claim via `web_fetch` or `browser` on the source page itself, prioritizing official / primary sources
9. if Exa is unavailable, unusable, or evidently low-yield for the query class, use Bing via `browser` as the second explicit discovery-only fallback, preferably with `en-US` parameters when practical
10. expect region bias / localized ranking in the current environment; do not describe Bing as a guaranteed international or neutral search path
11. treat Bing result pages as candidate-source discovery only, not as evidence for memo claims
12. in the evidence log, record which provider path was attempted, why the fallback was triggered, and whether the fallback was used because of provider failure, quota/rate-limit pressure, or query-fit judgment
13. if Bing is also blocked or unusable, declare the live-search step blocked and note which freshness checks or claims could not be verified live
14. continue with offline materials only if the remaining uncertainty is made explicit

## Degraded-search execution discipline

When fallback search is needed, do not switch providers mechanically.

Before changing provider path, make an explicit judgment about the cause:

- tool unavailable in the current environment
- provider failure or temporary outage
- quota / rate-limit pressure
- query-fit mismatch
- low-yield results despite provider availability
- browser-side localization need

Prefer this execution logic:

- use Exa first when the task is discovery-heavy and likely benefits from English-language web coverage, technical docs, company pages, or broad web recall
- do not force Exa first when the task is dominated by Chinese-language news flow, localized search intent, or browser-local ranking behavior
- before escalating again, tighten the search objective or query shape if the current path is returning noisy but not obviously irrelevant material
- move to Bing only when Exa is unavailable, clearly low-yield for the query class, or mismatched to the search intent
- stop degraded-search escalation when the next provider is unlikely to add decision-relevant value rather than escalating just because another provider exists

If fallback search keeps returning noisy or repetitive candidate sources, say so and tighten the live-search objective instead of continuing provider churn.

## Degraded-search evidence log

When degraded fallback is used, keep a compact internal log in this shape:

- search objective:
- primary provider attempted:
- fallback trigger: tool unavailable / provider failure / quota / query-fit / low-yield / localization need
- fallback provider used:
- why this fallback fits better:
- candidate-source quality: strong / mixed / weak
- claims still needing primary-page verification:
- live-search status: recovered / partially recovered / blocked

This log does not need to appear verbatim in the final memo, but its effects should be recoverable in the Research Pack, uncertainty register, or source notes.

Other tools:
- `web_fetch`: extract readable page content after search identifies a candidate source
- `browser`: handle dynamic pages or failed fetches for confirmed-live URLs
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

Produce a PDF artifact when the user's request shows explicit file-delivery intent:

- contains `pdf` or `PDF` in a generative/delivery context (e.g. "生成 PDF", "导出 PDF", "PDF 报告", "保存为 PDF", "给我 PDF 文件", "PDF 版本", "PDF 格式")
- includes file-oriented phrases like "报告文件", "可下载报告", "正式报告文件", "给我报告文件", "交付一个文件", "作为附件给我", "以附件形式交付", "输出为附件", "交付成附件"
- the overall request clearly asks for a deliverable file rather than just report content

Do not trigger PDF generation when:

- the user mentions `pdf` / `PDF` only to negate or discuss it: "不要 PDF", "不用 PDF", "无需 PDF", "no PDF", "not PDF", "为什么 PDF 渲染失败", "比较 PDF 和 Markdown", or similar meta-discussion
- the request only uses generic report terminology ("报告", "研究报告", "分析报告", "写成报告格式") that indicates output shape (text/markdown) rather than file format

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

use `evals/meta/rule-activation-and-execution-discipline.md`.

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
