# Eval: RAG API Provider Selection Source Traceability Fail Case

## Goal

Test whether a Provider / Vendor Selection report with clear decision architecture (8-dimension comparison, scenario-based recommendations, hybrid architecture) can still fail the provider-selection route when inline citations are absent, current-state verification is un-auditable, and ranking aggregation logic is opaque.

This is the **second consecutive Provider / Vendor Selection Fail case**, confirming a pattern: the route's source traceability and current-state verification requirements are systematically not executed.

## Real case pattern

A user-provided report "企业知识库 RAG 系统大模型 API 选型深度研究报告" dated **2026-06-04** demonstrates this pattern.

**What was done well:**
- ✅ Provider Selection route correctly selected with clear ranking framework
- ✅ 8-dimension comparison criteria with China-specific constraints
- ✅ Ranked recommendation: Qwen #1, Claude #2 supplement, DeepSeek #3 cost alternative
- ✅ Scenario-based recommendations for different team profiles
- ✅ Risk and counter-evidence chapter (§228-255)
- ✅ Source index exists as bibliography (§278-306)
- ✅ Actionable next steps (PoC, A/B testing, hybrid architecture)

**Fail causes:**
- ❌ **Zero inline citations** — no `[S1]` format or equivalent body-level references; source index exists but uncited in body
- ❌ **Current-state verification un-auditable** — pricing, model versions, compliance status, SLA claims have no verification date or source trail
- ❌ **Ranking aggregation logic opaque** — star ratings from 8 dimensions without explaining how they combine into final ranking; annual cost estimates missing formula and embedding cost treatment
- ❌ **Runner-up reversal conditions absent** — DeepSeek/Baidu/Claude scenarios stated but no explicit "what weight change would overtake Qwen" conditions

## Scoring

- **Fail**: source traceability hard-fail + current-state verification un-auditable + aggregation logic opaque
- **Conditional Pass**: one of the above issues fixed

## Related evals

- `evals/cases/ai-coding-tools-provider-selection-traceability-fail-case.md` — companion Fail: same route, same pattern (zero citations + unverifiable facts + missing role labels)
