# Eval: Agentic RAG vs Traditional RAG — Technical Deep-Dive Compounded Fail Case

## Goal

Test whether a Technical Deep-dive / Architecture Comparison report with strong dimension-by-dimension analysis, explicit trade-off summary, conditional recommendation, and clear counter-evidence can still **fail strict delivery** when all common technical-deep-dive failure patterns compound in a single report:

- **Source Register 6 columns** (missing DOI/URL) — fails 7-column hard requirement
- **Numeric role labels absent** — performance, cost, accuracy, TRL, phase benefit numbers lack observed/proxy/assumption/model-output roles
- **Vendor/secondary claims not distinguished in body** — Pinecone docs, LlamaIndex blogs, industry reports used as `[确认事实]` for performance/accuracy claims without "(厂商文档/技术博客，非独立验证)" caveat
- **Benchmark numbers missing methodology context** — "+42%", "30-40% cost", "80% Agentic 收益" stated without workload, benchmark setup, model/hardware/data boundaries
- **Self-assessment claims all ✅ while register, roles, vendor claims, and benchmark method all have gaps** — triggers process-integrity and declared-not-executed hard-fails
- **Mixed-script delivery cleanliness** — "传统文化RAG更优" mixed Chinese/English in a load-bearing conclusion position

This eval is based on a real report: an Agentic RAG vs Traditional RAG architecture comparison memo that correctly activated the technical-deep-dive route, provided clear comparison dimensions, a conditional recommendation framework with counter-evidence, and actionable next steps — but compounded every common technical-deep-dive failure at once.

## Prompt

Compare Agentic RAG and Traditional RAG system architectures. Produce a structured technical deep-dive report that:

- explains candidate architectures (Traditional RAG pipeline, Agentic RAG loop) with core mechanisms
- provides explicit comparison dimensions (control flow, retrieval strategy, tool integration, robustness, performance, cost, complexity, security)
- includes dimension-by-dimension analysis with judgments, not just feature lists
- provides a trade-off summary linking accuracy gains to latency/cost trade-offs
- gives a conditional recommendation per query type, latency budget, team maturity, and regulatory requirement
- includes counter-evidence (Agentic RAG can be worse, long-context alternatives, framework variance)
- uses claim-level `[Sxx]` inline citations throughout
- includes a complete 7-column Source Register (ID, Source Name, Type, Date, DOI/URL, Reliability, Claims Supported)
- labels all benchmark/performance/cost numbers with observed/proxy/assumption/model-output roles AND methodology context (workload, setup, hardware, model, data boundary)
- distinguishes vendor documentation / technical blogs / industry reports from independently verified facts in body labels
- checks mixed-script delivery — Chinese technical terms should not mix languages mid-phrase without consistent convention

## What this eval is testing

- whether the 7-column Source Register requirement is executed (not just the first 6 columns)
- whether numeric role labels are applied to comparison numbers with methodology context
- whether vendor/secondary sources are distinguished from independently verified facts at the body label level
- whether benchmark numbers include methodology boundaries (workload, setup, hardware)
- whether self-assessment accuracy matches body execution when multiple disciplines fail
- whether mixed-script delivery issues are caught in final-audit

## Pass criteria

A passing answer should:

1. **Deliver a complete 7-column Source Register with DOI/URL.** Abstract concept: 6 of 7 is a hard-fail.

2. **Label numeric roles with methodology boundaries.** Performance/cost/accuracy numbers must list: role (observed / proxy / benchmark-result / vendor-claim / assumption / model-output), workload, setup, hardware, data boundary where applicable.

3. **Distinguish vendor/secondary claims in body labels.** Vendor docs → "(厂商文档，非独立验证)", technical blogs → "(技术博客，非独立验证)", industry reports → "(行业报告)". Do not let them carry `[确认事实]` without caveat.

4. **Keep self-assessment honest.** Audit status must reflect actual gaps in register, roles, vendor claims, and benchmark method.

5. **Maintain delivery cleanliness.** Mixed-script phrases ("传统文化RAG更优") are cleanliness hard-fails.

## Failure signs

Mark this eval as failed if the answer does any of the following:

- Source Register has fewer than 7 columns (DOI/URL missing)
- comparison numbers lack role labels and methodology context
- vendor docs / technical blogs / industry reports labeled as `[确认事实]` without source role caveat
- self-assessment claims full pass while register, roles, or vendor claims have gaps
- mixed-script errors in load-bearing positions

## Why this eval matters

Existing technical-deep-dive cases capture individual failures (vendor claims in CPO, benchmark method in K8s, register format in MCP). This case tests the **compounded scenario** — all common failures in one architecture comparison report:

| Case | Route | Level | Unique issue | Common issues |
|---|---|---|---|---|
| CPO inline citation | tech-dive | Conditional pass | Vendor claims without caveat | Citations absent, roles missing |
| K8s vs Swarm | tech-dive | Conditional pass | Benchmark method missing | Self-assessment, register gaps |
| MCP timeline | tech-dive | Fail | Timeline inconsistency + roadmap | Self-assessment |
| Agentic RAG (this) | tech-dive | **Fail** | **Compounded: register + roles + vendor + benchmark + self-assessment** | All common issues at once |

The unique contribution of this case is testing whether the skill can independently identify each failure layer when they co-occur. A report with structured dimension comparison, trade-off summary, and clear recommendation can mask the fact that the evidence layer (register, roles, vendor claim distinction) is systematically noncompliant.

Mixed-script delivery ("传统文化RAG更优") is a specific technical-deep-dive cleanliness issue: Chinese technical reports with frequent English terms (RAG, token, pipeline, latency) must maintain consistent language boundaries.

## Current rule verdict

- Source Register 7-column hard-fail
- Numeric role hard-fail on comparison tables
- Evidence ceiling violation: vendor/secondary sources as [确认事实]
- Process-integrity hard-fail: self-assessment overclaim
- Delivery cleanliness: mixed-script error

## Related evals

- `evals/cases/cpo-technical-deep-dive-inline-citation-absent-case.md` — same route, vendor claims without caveats
- `evals/cases/k8s-vs-swarm-technical-deep-dive-self-assessment-case.md` — same route, benchmark method missing
- `evals/cases/mcp-technical-deep-dive-timeline-roadmap-case.md` — same route, timeline and roadmap
- `evals/cases/content-platform-constrained-choice-compounded-fail-case.md` — same compounded-fail pattern, different route

## Reviewer checklist

- Is Source Register 7 columns with DOI/URL?
- Do comparison numbers have role labels AND methodology context?
- Are vendor/secondary sources distinguished in body labels?
- Does self-assessment match body execution?
- Are there mixed-script errors in load-bearing positions?
- Are definition-sensitive concepts (术语边界) clarified before architecture comparison (原始定义 vs 工程定义 vs 本文采用定义)?

## Suggested scoring

- **Pass**: 7-column register, numeric roles with method context, vendor claims caveated, self-assessment honest, clean delivery
- **Conditional pass**: architecture comparison strong, trade-offs visible, recommendation actionable, but register format thin (6 columns), or roles exist without method context, or vendor caveats partial — no process-integrity violation
- **Fail**: register <7 columns (hard-fail), or roles absent on comparison numbers, or vendor claims systematically carry [确认事实] without caveat, or self-assessment claims all ✅ while gaps exist (process-integrity)
