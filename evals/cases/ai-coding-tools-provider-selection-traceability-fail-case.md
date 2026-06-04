# Eval: AI Coding Tools Provider Selection Source Traceability Fail Case

## Goal

Test whether a Provider / Vendor Selection report with strong decision architecture (ranked shortlist, runner-up credibility, reversal conditions) can still fail the provider-selection route's hard-fail conditions when inline source citations are entirely absent, current-state verification is un-auditable, and quantitative indicators lack role labels.

This is the **first Provider / Vendor Selection route Fail case**.

## Real case pattern

A user-provided report "中国团队AI编程工具选型深度研究报告" (China Team AI Coding Tool Selection) dated **2026-06-04** demonstrates this pattern.

**What was done well:**
- ✅ Provider Selection route correctly selected with full decision architecture
- ✅ Ranked shortlist (Cursor #1, Copilot #2, Trae CN #3, Claude Code/Codex not recommended)
- ✅ Why top option wins + why runner-up credible + why others lose — all present
- ✅ Hard constraints + soft preferences + TCO + weights explicitly stated
- ✅ Reversal conditions and monitoring signals (§336-360)
- ✅ Counter-evidence present with reverse scenarios
- ✅ Bottom line actionable with deployment recommendations

**Fail causes:**
- ❌ **Zero inline citations** — entire report has no `[SN]`/`[IN]`/`[UN]` or equivalent body-level references. Sources are a loose bibliography (§405-447), not a structured register
- ❌ **Fast-moving provider facts unverifiable** — pricing, model versions, China accessibility, SLA claims have no verification date or source; reader cannot confirm freshness
- ❌ **Quantitative indicators lack role labels** — market share, DAU, performance percentages, enterprise adoption rates have no observed/proxy/assumption/model-output distinction
- ❌ **Scoring aggregation method unexplained** — star ratings presented without explaining how weights combine into final ranking

## Scoring

- **Fail**: source traceability hard-fail + current-state verification un-auditable + quantitative role labels missing
- **Conditional Pass**: one of the above issues fixed
- **Full Pass**: all three resolved

## Related evals

- `evals/cases/meituan-listed-company-traceability-gap-case.md` — same pattern: near-zero citations + register present but uncited
