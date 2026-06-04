# Eval: NEV Parts Europe Market Entry Quantitative Role Fail Case

## Goal

Test whether a Market Entry / Regional Expansion report with strong decision architecture (regional hub/beachhead/expansion distinction, hard gates, reversal conditions, phased roadmap) can still fail when the secondary Constrained Choice route's quantitative role labeling hard-fail is triggered (scores, weights, cost multiples without observed/proxy/assumption/model-output labels).

## Real case pattern

A user-provided report "中国新能源汽车零部件公司欧洲第一落点决策报告" dated **2026-06-04** demonstrates this pattern.

**What was done well:**
- ✅ Market Entry primary route correctly selected with A/B/C entry modes
- ✅ Regional Hub / First Revenue Beachhead / Later Expansion Market cleanly distinguished (§195-201)
- ✅ Unified scoring framework across 3 countries with 6+ dimensions (§73-191)
- ✅ Hard gates HG1-HG6 (§205-214) with phased M0-M36 roadmap (§256-292)
- ✅ Reversal conditions R1-R5 (§218-248)
- ✅ Strong decision usefulness: next steps with owner and timeline (§341-351)
- ✅ Hub/beachhead/expansion not conflated into one "best market"

**Hard-fail triggered:**
- ❌ **Constrained Choice secondary route hard-fail triggered** — §85, §99, §114, §128, §142, §157, §172, §180-189: scores, weights, cost multiples, subsidy ratios lack observed/proxy/assumption/model-output labels
- ❌ **Body-level source traceability absent** — §355-396 is loose bibliography, not structured Source Register; no `[SN]` inline citations
- ❌ **Audit status invisible** — primary + secondary routes declared but required audits and secondary hard-fail verification status not recorded
- ❌ **Aggregation logic opaque** — §180-189 weights labeled "模式B基准" but source, sensitivity, and calculation method not explained

## Scoring

- **Full Pass**: quantitative role labels present + inline citations + audit status visible
- **Fail**: secondary route hard-fail triggered + traceability absent (this case's level)

## Related evals

- `evals/cases/ai-saas-market-entry-traceability-case.md` — Market Entry route companion: same traceability gap, different secondary route
- `evals/cases/indie-game-constrained-choice-quantitative-role-case.md` — same quantitative role labeling hard-fail pattern
