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
- the user’s likely decision or use case
- the required depth
- the time horizon if relevant
- whether the user wants explanation, recommendation, comparison, or diligence

If the user’s wording is broad, anchor on the most decision-relevant interpretation instead of drifting into general background.

Examples:

- “Research AI coding agents” may really mean market entry, competitive positioning, or vendor selection.
- “Research this company” may really mean partnership diligence, investment risk, or product comparison.

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
Read `references/market-sizing-and-share-discipline.md` when the task involves market size, TAM/SAM/SOM, market-share estimates, competitive-position sizing, or any numeric mapping from company data to broader market claims.
Read `references/ranking-and-current-claims-discipline.md` when the task involves rankings, share rankings, category leadership, "No.1" claims, streak claims, current-position claims, or other time-sensitive comparative statements.
Read `references/corporate-status-and-listing-state-discipline.md` when the task involves whether a company is private, filed, approved, registered, listed, trading, delisted, or otherwise in a changing capital-markets state.

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

Read `references/parallel-research.md` when deciding whether to parallelize.
Read `references/subagent-orchestration.md` when spawning sub-agents or merging outputs.
Read `references/evidence-log-template.md` when you want a compact per-track ledger.

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

Before delivering the final report, check:

- Did I answer the user’s real objective?
- Did I rely too much on one narrative or one source chain?
- Did I test my main conclusion against counter-evidence?
- Did I clearly separate confirmed facts, inference, and uncertainty?
- Did I give the user a useful bottom line rather than just a long summary?

If not, revise before answering.
