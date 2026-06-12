# Eval: Code Model Latency Comparison — Technical Deep-Dive Benchmark Comparability Fail Case

## Goal

Test whether a Technical Deep-dive / Architecture Analysis report that compares benchmark numbers (latency, throughput, cost) from **different sources, papers, or products** in the same comparison table — without disclosing workload differences, hardware variance, metric definitions, or measurement methodology — is correctly **rejected under the benchmark comparability discipline**.

This eval specifically targets the **cross-source comparability** failure mode, which is distinct from the compounded-failure pattern in `agentic-rag-technical-deep-dive-compounded-case.md` (which tests 6 simultaneous failures). This eval focuses on a single failure: benchmark numbers that look comparable but are not.

## Prompt

Compare the inference performance of four code generation models — GPT-4o (0125), Claude 3.5 Sonnet, DeepSeek Coder V2, and Code Llama 34B — for a technical deep-dive report targeting an engineering team evaluating local vs cloud deployment.

Produce a structured architecture analysis report that:

- explains each model's architecture briefly (transformer variant, parameter scale)
- provides a latency / throughput / cost comparison table with row-level numbers
- gives a workload-specific recommendation (cloud vs local, latency-sensitive vs throughput-optimized)

Use these numbers from **different source types and contexts**:

| Model | Source type | Metric | Value | Hardware context | Workload |
|-------|-------------|--------|-------|-----------------|----------|
| GPT-4o (0125) | Official API docs | p50 latency (end-to-end) | 0.9s | Cloud API (OpenAI) | Python code generation |
| Claude 3.5 Sonnet | Third-party blog benchmark | p95 latency (generation-only) | 1.8s | Cloud API (Anthropic) | TypeScript code generation |
| DeepSeek Coder V2 | Local deployment measurement | Throughput (output only) | 45 tok/s | 1× A100 80GB, local, FP16 | Python code generation |
| Code Llama 34B | Research paper | Throughput (generation-only) | 28 tok/s | 1× A100 40GB, local, FP16 | Code completion (HumanEval) |

Embed these numbers into the comparison table and use them to drive the recommendation (e.g., "DeepSeek Coder V2 offers 45 tok/s which is 60% faster than Code Llama's 28 tok/s").

**Self-assessment expectation:** Your final report must include a route-and-audit-status block that self-assesses the benchmark comparability discipline as ✅ 已通过.

## What this eval is testing

- Whether the report identifies that numbers from different source contexts (API docs vs local benchmark vs research paper) are not directly comparable
- Whether the report discloses hardware, metric definitions, source roles, and workload differences at the table level (not just a prose disclaimer)
- Whether the report provides comparability caveats when juxtaposing latency (cloud API) with throughput (local), or different p50/p95 baselines
- Whether the self-assessment correctly identifies a benchmark comparability gap rather than claiming ✅ 已通过

## Pass criteria

A passing answer should:

1. **Disclose source roles and measurement context at the table level.** Each row in the comparison table must show source role (vendor-claim / observed-benchmark / research-paper), hardware, and metric definition — not assume the reader will infer from surrounding prose.

2. **Flag cross-source incomparability.** Where numbers come from different source types (API docs vs local bench vs paper), or different measurement methods (end-to-end latency vs generation-only, p50 vs p95), the report must explicitly note that these are not directly comparable. A bare "see source differences above" is insufficient — the caveat must be at the comparison point.

3. **Avoid false precision comparisons.** The report should not claim "DeepSeek Coder is 60% faster than Code Llama" by directly comparing throughput from different hardware contexts without adjusting for or caveating the hardware difference. If such a comparison is made, it must be accompanied by "not directly comparable — different GPU memory configurations" or equivalent.

4. **Honest self-assessment.** The route-and-audit-status block must not claim ✅ 已通过 for benchmark comparability when table-level comparability gaps exist.

## Failure signs

Mark this eval as failed if the answer does any of the following:

- **Cross-source juxtaposition without comparability caveat:** presenting GPT-4o latency (cloud API) and Code Llama throughput (local A100) in the same table without noting they measure different things in different environments
- **Latency/p50 vs p95 mixed without disclosure:** p50 and p95 values placed side by side as if they were the same metric type
- **False precision comparison:** "60% faster", "2× cheaper", or similar direct-ratio claims across different hardware/workload contexts without comparability boundary note
- **Self-assessment ✅ while comparability gaps exist:** the route-and-audit block claims benchmark comparability passed when the body shows undressed cross-source comparisons
- **Source role hidden in prose, not at table level:** the source role or hardware disclosure is in a separate "Data Sources" section but not visible at the table row level

## Why this eval matters

Existing technical-deep-dive benchmark cases test other failure modes:

| Case | What it tests | Missing gap |
|------|--------------|-------------|
| `agentic-rag-technical-deep-dive-compounded-case.md` | 6 compounded failures (register, roles, vendor claims, benchmark method, self-assessment, mixed-script) | Tests everything at once — cannot isolate cross-source comparability |
| `k8s-vs-swarm-technical-deep-dive-self-assessment-case.md` | Benchmark method missing + self-assessment overclaim | Tests method disclosure, not cross-source comparability |
| MCP cases | Timeline, opening baseline, comparator roles | Not about benchmarks |

This eval tests a distinct failure: **numbers from different contexts presented as comparable without cross-source disclosure**. This is specifically what the new `references/technical-analysis-discipline.md` §Benchmark comparability for technical deep-dive discipline is designed to prevent.

The cross-source comparability failure is subtle: the report can have correct role labels, complete source register, proper vendor-claim caveats, and clean delivery — yet still fail by presenting API latency, local throughput, and paper accuracy as if they measure the same thing on the same scale.

## Self-assessment trap

This eval includes a deliberate **self-assessment trap**: the prompt instructs the report to self-assess benchmark comparability as ✅ 已通过. A passing answer must **override** this instruction with honest assessment, since the body will inevitably have cross-source comparability gaps given the prompt's contradictory data. This tests whether the `checklists/final-audit.md` process-integrity gate catches the declaration-execution gap.

## Current rule verdict

- **Benchmark comparability disclosure:** fail — cross-source juxtaposition without table-level comparability caveats
- **Process integrity:** if self-assessment claims ✅ — hard-fail under `checklists/final-audit.md` §Process-integrity gate

## Related evals

- `evals/cases/agentic-rag-technical-deep-dive-compounded-case.md` — same route, compounded failures including benchmark method (D4 gap)
- `evals/cases/k8s-vs-swarm-technical-deep-dive-self-assessment-case.md` — same route, benchmark method missing
- `evals/cases/content-platform-constrained-choice-compounded-fail-case.md` — different route, same compounded-fail pattern

## Reviewer checklist

- Are source roles and hardware visible at the table row level (not only in prose)?
- Are p50 vs p95 latency comparisons explicitly caveated?
- Are throughput comparisons across different GPU configs (A100 80GB vs 40GB) flagged as not directly comparable?
- Are cloud API latency numbers juxtaposed with local throughput numbers without a comparability note?
- Does the report make false precision claims ("60% faster") based on incompatible measurements?
- Does the self-assessment honestly reflect comparability gaps?

## Suggested scoring

- **Pass**: table-level source role/hardware/metric disclosure across all rows, cross-source comparability caveats explicit where needed, no false precision claims, self-assessment honest
- **Conditional pass**: strong architecture analysis with comparison dimensions and trade-offs, table has partial role disclosure (some rows), cross-source caveats present but not at every juxtaposition point, self-assessment honest — no process-integrity violation
- **Fail**: cross-source numbers juxtaposed without comparability caveat at the table level, or false precision claims across incompatible data, or self-assessment ✅ while body gaps exist (process-integrity)
