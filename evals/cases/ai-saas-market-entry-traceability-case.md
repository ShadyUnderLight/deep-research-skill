# Eval: AI SaaS Market Entry Source Traceability Case

## Goal

Test whether a Market Entry / Regional Expansion report with strong decision architecture (`Go / Pilot Only / Not Now`, phased roadmap, hard gates, reversal conditions) can still achieve Conditional Pass when body-level source traceability fails and quantitative estimates lack role labeling.

## Real case pattern

A user-provided report "中国 AI SaaS 公司出海第一站：日本 vs 东南亚 vs 中东" dated **2026-06-04** demonstrates this pattern.

**What was done well:**
- ✅ Market Entry route correctly selected with clear ranking (东南亚 > 中东 > 日本)
- ✅ `Go / Pilot Only / Not Now` labels per market
- ✅ Hard gates per market (§176-206) with sequencing logic (0-24 month roadmap)
- ✅ Unified comparison framework (§31-55) with consistent dimensions
- ✅ Counter-evidence per market (§210-230)
- ✅ Uncertainty and reassessment conditions (§234-243)
- ✅ Actionable next steps (0-180 day plan, §247-267)
- ✅ Evidence labels ([确认事实]/[推断]/[未知]) used throughout

**Core issues (conditional pass level):**
- ❌ **Body-level inline citations absent** — source list exists (§288-341) but zero `[SN]` body references; market size, cost, revenue cycle, CAGR claims untraceable
- ❌ **Quantitative estimates lack role labels** — weights, investment costs, revenue timelines, star ratings mix observed facts, inferences, and model outputs without distinction
- ❌ **Regulatory secondary route incomplete** — declared as secondary discipline but has no explicit current/pending/enforcement framework or optimistic/base/pessimistic scenarios

## Scoring

- **Full Pass**: inline citations present + quantitative role labels + regulatory framework complete
- **Conditional Pass**: strong decision architecture but traceability gaps (this case's level)
- **Fail**: decision architecture missing or hard gates absent

## Related evals

- `evals/cases/rag-api-provider-selection-traceability-fail-case.md` — same traceability pattern, different route
