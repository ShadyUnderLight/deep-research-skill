---
name: deep-research
description: Conduct structured multi-step research for complex questions, decision support, market/company/technical analysis, competitive scans, and fact-checked briefings. Use when the user needs more than a quick answer and the task benefits from explicit planning, source comparison, verification, counter-evidence, uncertainty handling, and a structured final report. Especially use when the goal is to support a decision, compare alternatives, understand a market/company/product, assess feasibility, or produce a source-backed research memo.
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

1. Clarify the real objective.
2. Classify the task type.
3. Produce a short research plan.
4. Define evidence standards and stop conditions.
5. Collect and compare sources.
6. Run a mid-research review.
7. Search for counter-evidence.
8. Synthesize findings into a decision-oriented report.

## Step 1: Clarify the real objective

Before searching, identify:

- the main question
- the user's likely decision or use case
- the required depth
- the time horizon if relevant
- whether the user wants explanation, recommendation, comparison, or diligence

If the user's wording is broad, anchor on the most decision-relevant interpretation instead of drifting into general background.

Examples:

- "Research AI coding agents" may really mean market entry, competitive positioning, or vendor selection.
- "Research this company" may really mean partnership diligence, investment risk, or product comparison.

## Step 2: Classify the task type

Choose the closest task type before collecting sources. If unclear, make a reasonable choice and proceed.

Common task types:

- market or industry research
- company or startup analysis
- product or competitor analysis
- technical feasibility
- regulatory or policy scan
- people or background research
- buy/build/partner decision
- vendor or tool selection

Use the task type to shape subquestions, source priorities, and report structure.

Read `references/task-types.md` when the task needs a domain-specific question set.

## Step 3: Produce a short research plan

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

Prefer a small number of high-value questions over a large list of generic ones.

A strong plan focuses on what would change the final conclusion, not just what is interesting.

## Step 4: Define evidence standards and stop conditions

Set a quality bar before gathering sources.

Before searching deeply, decide which gates must fire for this task. Do not leave this implicit.

At minimum, check for these trigger patterns:

- **Listed company / public equity / valuation / investment memo** -> run listed-company discipline and require a current market snapshot before delivery
- **Current products / latest model / current lineup / pricing / release cycle / rankings / market position** -> run current-state verification before broader analysis
- **Model/API supplier selection / vendor shortlist / provider choice / platform choice under deployment constraints** -> treat as both a current-state-sensitive task and a constrained-choice task; require a current provider snapshot before ranking or recommendation
- **Structured memo / investment case / comparative report / claim-labeled output** -> run source-traceability discipline
- **Forecast / roadmap / guidance / consensus / target price / launch timing / "预计" style claims** -> run forward-looking-claims discipline
- **Market outlook / industry evolution / "未来12个月如何演化" / adoption trajectory / industry memo** -> treat as both a current-state-sensitive task and a decision-memo task; require a current market snapshot, explicit drivers/blockers, scenario structure, and stakeholder action guidance
- **Global market / full landscape / industry-wide scope** -> explicitly test scope completeness across key geographies, segments, and regulatory regimes
- **Recommendation / go-no-go / compare options / what should we do** -> optimize for decision utility, not just depth
- **Market entry / regional expansion / "should we prioritize market X" / country-entry sequencing under limited budget** -> treat as both a constrained-choice task and a decision-memo task; require explicit priority vs alternatives, country shortlist, sequencing, hard gates, and entry-mode logic rather than a market overview

If multiple triggers apply, route into all of them. Do not assume one checklist covers the others.

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
Read `references/finance-date-discipline.md` when the task involves company research, financial performance, valuation, guidance, delivery volumes, or other time-sensitive numeric claims.
Read `checklists/listed-company-report.md` for listed-company research - applies the required fields gate before delivery.

Read `references/market-sizing-and-share-discipline.md` when the task involves market size, TAM/SAM/SOM, market-share estimates, competitive-position sizing, or any numeric mapping from company data to broader market claims.
Read `references/ranking-and-current-claims-discipline.md` when the task involves rankings, share rankings, category leadership, "No.1" claims, streak claims, current-position claims, or other time-sensitive comparative statements.
Read `references/corporate-status-and-listing-state-discipline.md` when the task involves whether a company is private, filed, approved, registered, listed, trading, delisted, or otherwise in a changing capital-markets state.
Read `references/source-traceability-and-claim-citation.md` when the task requires structured claims, investment memos, competitive analysis, or any output where readers need to audit which specific source supports which conclusion. Specifically required when the output includes CONFIRMED / LIKELY / UNCERTAIN labels.
Run `checklists/source-traceability.md` before delivery if the output is a structured or investment-relevant memo.

Read `checklists/forward-looking-claims.md` when the task involves product release timelines, pricing forecasts, forward financial estimates, or any forward-looking statements.
Read `evals/global-market-scope-completeness-case.md` as a coverage discipline check when the task claims global, full-landscape, or industry-wide scope.
Read `evals/decision-utility-rubric.md` when the user needs a recommendation, prioritization, vendor choice, go/no-go, or other action-guiding conclusion.
Read `references/option-selection-and-shortlist-discipline.md` when the task is mainly about choosing among several plausible options under constraints (for example destination selection, vendor shortlist, office/venue choice, multi-origin meetup/location choice, or other comparison tasks where ranking and elimination matter more than background explanation).
Run `checklists/option-selection-final-audit.md` before delivery for shortlist, ranking, destination-selection, or other constrained-choice outputs.
For model/API supplier or provider-selection tasks, explicitly verify a current provider snapshot before broader comparison: current primary model/API family, current pricing unit, current support-region / mainland accessibility reality, current data-control posture, and current SLA / status disclosures when decision-relevant.
For market-entry / regional-expansion / country-prioritization tasks, explicitly verify the decision architecture before broader analysis: what the real choice is, what the priority is relative to alternatives, whether the question is about a regional hub vs first revenue beachhead vs later expansion market, what hard gates exist, and what sequencing logic would make the recommendation operational.
Use `references/decision-report-template.md` with the provider-selection structure when the task is choosing a core model/API supplier under real deployment constraints.
Use `references/decision-report-template.md` with the market-entry structure when the task is deciding whether to prioritize a country or region under real budget, compliance, and localization constraints.
Read `references/comparative-distillation-method.md` when comparing paired reports (for example GPT vs Minimax on the same topic) to distill reusable skill improvements rather than just judge which output is better.
Use `evals/comparative-distillation-template.md` to record each paired-report comparison so every extracted pattern ends in `NEW_RULE`, `CHECKLIST_HARDENING`, `TEMPLATE_CHANGE`, or `NO_ACTION`.

Stop searching when one of these is true:

- the main question is answered with adequate confidence
- new searches mostly repeat prior findings
- remaining uncertainty is due to unavailable data, not lack of effort

Do not keep searching just to make the report longer.

## Step 5: Collect and compare sources

Start lightweight.

- Use `web_search` to discover candidate sources.
- Use `web_fetch` for readable extraction.
- Use `browser` only when a page is dynamic or fetch fails.

Avoid browsing loops with weak information gain.

Prioritize source diversity over source count. A few independent, high-quality sources are better than many repetitive summaries.

When comparing sources, pay attention to:

- independence
- recency
- directness
- measurement vs opinion
- whether a source is repeating another source

For time-sensitive topics, prefer current sources over older authoritative summaries if the newer material changes the picture.

## Current-state verification

When the task involves products, model versions, device lineups, pricing, packaging, regulations, company status, leadership, rankings, release cycles, or any fast-moving topic, verify the current state before forming conclusions.

Do not rely on prior knowledge, stale summaries, or model memory for current-state facts.

Before writing the report, explicitly verify when relevant:

- latest product generation or version
- current product lineup
- current pricing or packaging
- current company positioning
- most recent major announcement or release
- whether newer information supersedes older sources

Prefer current-state checks in this order:

1. official current product or company pages
2. official announcements, press releases, or release notes
3. current docs, changelogs, or support pages
4. reputable reporting only after checking primary sources

For fast-moving topics, search with freshness-first patterns such as:

- `[topic] official`
- `[topic] latest`
- `[topic] current`
- `[topic] current lineup`
- `[topic] release date`
- `[topic] pricing`
- `site:<official-domain> [topic]`

If the current state cannot be verified, say so clearly instead of filling gaps with likely-but-stale knowledge.

For fast-moving company or investment research, produce a short current snapshot before broader analysis. When relevant, verify and separate:

- current product lineup
- current strategic framing
- latest reported financial disclosure
- current market snapshot
- forward-looking targets or estimates

Do not merge reported facts, current market data, and forward-looking numbers into one undifferentiated narrative.

For market-outlook / industry-evolution tasks, the opening snapshot should be visibly tailored to decision use, not just recency. When relevant, verify and separate:

- current market baseline and scope
- current product / pricing / policy changes that alter the next-12-month view
- current adoption bottlenecks or enabling infrastructure
- explicit drivers of change vs blockers of change
- what is observed now vs what is scenario logic for the next 6-12 months

If the task asks how a market will evolve, do not let the report remain a background industry overview. Force a transition from current snapshot -> scenarios -> stakeholder implications.

## Step 6: Run a mid-research review

After the first meaningful batch of evidence, pause and reassess.

Write a short internal review covering:

- current best answer
- strongest evidence so far
- key missing evidence
- which subquestions matter less than expected
- whether the search strategy should change
- whether parallelization is now justified

Use this step to cut low-value branches and sharpen high-value ones.

Do not continue gathering information blindly once the shape of the answer is clear.

## Step 7: Search for counter-evidence

For every high-impact conclusion, actively look for evidence that could weaken or overturn it.

At minimum, do one of:

- look for direct criticism or failure cases
- look for competing explanations
- look for contradictory primary or independent sources
- look for edge cases, legal issues, security issues, user complaints, or failed rollouts
- look for reasons the conclusion may only hold in one market, segment, or timeframe

Read `references/counter-evidence.md` when the topic is contentious, commercial, fast-moving, or high stakes.

Never treat the first plausible story as the final one.

## Step 8: Synthesize into a decision-oriented report

Use the report structure in `references/report-template.md` by default.
Read `references/decision-report-template.md` when the user needs a recommendation, go/no-go view, comparison, or action plan.
For market-outlook / industry-evolution tasks, prefer the decision-report structure over a generic industry overview. These tasks should visibly show: current snapshot, key drivers and blockers, scenario structure, stakeholder implications, and what would change the view.

For most tasks, include:

1. Executive summary
2. What matters most
3. Key findings
4. Detailed analysis
5. Risks and counter-evidence
6. Uncertainty and missing evidence
7. Bottom line
8. Sources

When useful, also include:

- recommendation
- alternatives considered
- what could change the conclusion
- next checks
- near-term outlook

Always make clear:

- what is directly supported
- what is inferred
- what remains unresolved

## Delivery artifact rule

Default delivery stays as text / markdown.

If the user's request includes `pdf`, `PDF`, or `报告`, treat that as a PDF-output request in addition to the normal report delivery.

In that case:

1. write the final report to a `.md` file first
2. convert it with `scripts/md_to_pdf.py` (resolve relative to the skill directory)
3. deliver or attach the generated PDF when the surface supports files

Do not skip the markdown file. The PDF is a rendered artifact, not the source of truth.

If PDF rendering fails, still deliver the markdown/text report and explicitly say the PDF export failed.

## Research depth

This skill defaults to deep research quality.

Do not switch between multiple research modes by default. Instead, keep the research discipline consistent and adapt only:

- the breadth of background detail
- the number of secondary branches explored
- the length of the final report

Even when answering more compactly, keep the core workflow:

- clarify the real objective
- classify the task type
- produce a research plan
- compare sources
- test key conclusions with counter-evidence
- separate fact from inference
- state uncertainty clearly
- deliver a decision-oriented synthesis

If the user explicitly asks for a faster or lighter answer, compress the presentation rather than dropping core research discipline.

## Parallelization

Only parallelize when the topic clearly splits into distinct tracks and each track can be researched independently enough to justify coordination cost.

Good examples:

- market size
- competitors
- technical feasibility
- regulation
- customer demand signals

When parallelizing:

- split into 2-4 tracks
- keep each track narrow
- require structured findings, not polished prose
- require explicit source URLs
- require separation of confirmed facts vs inference
- reserve final synthesis for the parent agent

For each track, define:

- track name
- exact question
- preferred source types
- required outputs


## Tool strategy

Use tools deliberately.

- `web_search`: discover candidate sources and comparison angles
- `web_fetch`: extract readable page content
- `browser`: handle dynamic pages or failed fetches
- `sessions_spawn`: split clearly separable tracks only
- final synthesis: always perform one parent-level reconciliation pass

Avoid unnecessary browsing loops, repetitive searches, or unstructured parallel runs.

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

## Domain adaptation

Adjust source preference by topic:

- companies or startups: official site, filings, product docs, pricing, careers, credible press
- software or tools: docs, repo, changelog, issue tracker, benchmarks, user complaints
- markets: official datasets, regulator or institution reports, strong industry analysis
- regulation: regulator publications, law text, consultation documents, legal analysis
- people or background: primary profiles, official bios, direct publications, reputable reporting

When the topic changes over time, explicitly include the time dimension:

- recent changes
- momentum
- inflection points
- near-term outlook

## Final discipline

Before delivering the final report, run `checklists/final-audit.md`.

Then ask one more question: did the correct gates actually fire for this task?

Use these final trigger checks:

- if this was a listed-company or investment-style report, the output should visibly show listed-company discipline
- if this was a current-state-sensitive task, the output should visibly show a current snapshot or freshness verification
- if this was a model/API supplier or provider-selection task, the output should visibly show a current provider snapshot and should treat accessibility / compliance / SLA / data-control constraints as part of ranking logic when relevant
- if this was a market-entry / regional-expansion / country-prioritization task, the output should visibly show priority vs alternatives, a country shortlist, a distinction between regional hub vs first beachhead vs later expansion market when relevant, hard gates, and sequencing logic rather than a generic market overview
- if this was a structured or claim-heavy memo, the output should visibly show source traceability in the body, not only in a source appendix
- if this included forecasts, roadmap claims, estimates, or target prices, the output should visibly show forward-looking discipline
- if this claimed broad global or full-landscape scope, the output should visibly show scope completeness or clearly state scope limits
- if this was meant to support a decision, the output should visibly help the reader choose, prioritize, or decide what to verify next

If the report appears to know the rule but not execute it reliably, use `evals/rule-activation-and-execution-discipline.md` to diagnose whether the problem is a missing rule, missing trigger, or execution failure.

It checks: real objective answered, evidence quality, counter-evidence, uncertainty honesty, completeness, recall discipline, and whether the right delivery-time gates actually became visible in the report.

A report that fails the final audit checklist is not ready for delivery.
