# Eval: Indie Game Studio Constrained Choice Quantitative Role Case

## Goal

Test whether a Constrained Choice / Shortlist report with strong decision architecture (ranking, runner-up credibility, reversal conditions, phased execution gates) can still fail the route's hard-fail condition when quantitative indicators lack observed/proxy/assumption/model-output role labels and body-level claim-level citations are absent.

## Real case pattern

A user-provided report "独立游戏工作室出海路径决策报告" (Indie Game Studio Overseas Path Selection) dated **2026-06-04** demonstrates this pattern.

**What was done well:**
- ✅ Constrained Choice route correctly selected with clear ranking (Steam > Switch > 日本线下)
- ✅ Decision architecture with hard constraints, soft preferences, comparison unit defined
- ✅ Why top option wins + runner-up credibility + why others lose — all structured
- ✅ Ranking-reversal conditions with 3 scenarios (§202-206)
- ✅ Hidden operational burdens surfaced (certification, hardware optimization, cross-cultural legal, inventory risk)
- ✅ Phased execution gates with go/no-go checkpoints (§155-186)
- ✅ Low/medium/high regret action plan (§220-238)
- ✅ Counter-evidence and unknowns present

**Hard-fail triggered:**
- ❌ **Quantitative role labels missing** — §57-62, §88-99, §129-130, §180-186 have numbers (typical revenue, success probability, break-even, sales range) without observed/proxy/assumption/model-output distinction. Route hard-fail "uses numbers without labeling their epistemic role" triggered.
- ❌ **Comparison unit declared but not calculated** — "每投入1美元的期望可回收收入" (§45-47) stated as comparison metric but never actually computed or modeled in the report
- ❌ **Body-level citations absent** — source list exists as bibliography but no `[SN]` inline citations in body
- ❌ **Secondary market-entry route hard-fails unchecked** — declared as secondary discipline but no verification status recorded

## Scoring

- **Full Pass**: quantitative role labels present + comparison unit calculated + inline citations + secondary route verified
- **Conditional Pass**: strong structure + actionable but quantitative role labels missing (this case's level)
- **Fail**: hard-fail triggered + no counter-evidence

## Related evals

- `evals/cases/champions-league-constrained-choice-activation-case.md` — constrained-choice route not activated
