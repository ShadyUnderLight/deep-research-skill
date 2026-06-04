# Eval: E-Commerce CS Provider Selection Source Traceability Case

## Goal

Test whether a Provider / Vendor Selection report with strong scenario-based recommendations, weighted scoring, and a self-declared audit summary can still achieve a Conditional Pass when body-level inline citations are absent (bibliography exists but uncited in body) and scoring evidence layers are opaque.

This is the **third consecutive Provider / Vendor Selection case in Round 4**, but the first to achieve **Conditional Pass** (previous two both Failed), showing improvement in the route's structural execution.

## Real case pattern

A user-provided report "中小电商客服自动化平台选型深度研究报告" dated **2026-06-04** demonstrates this pattern.

**What was done well:**
- ✅ Provider Selection route correctly selected with explicit audit trail (§ appendix A)
- ✅ Scenario-based recommendations (国内/跨境/小微/合规/Zendesk迁移) with clear winner per scenario
- ✅ 6-dimension weighted scoring with explicit weights
- ✅ Current-state verification for international platforms (Zendesk/Intercom pricing checked)
- ✅ Hard constraints explicit (<50 seats, China market)
- ✅ Counter-evidence and reversal conditions present (§461-472)
- ✅ Self-declared audit summary with required audits listed (§553-557)
- ✅ Actionable next steps (trial, KB testing, WeChat integration, TCO model)

**Core issues (conditional pass level):**
- ❌ **Body-level inline citations absent** — bibliography exists (§476-524) but zero `[SN]` body references; load-bearing claims (pricing, market share, resolution rate, compliance claims) untraceable from body text
- ⚠️ **Scoring evidence layers opaque** — 1-5 scores without per-dimension calibration rules or per-cell source attribution
- ⚠️ **Strong claims missing scope/source** — "电商份额第一", "50-70% cost savings", "90%+ WeChat interactions" without source, date window, or metric definition
- ⚠️ **Audit summary overclaims** — §553-557 marks source-traceability as ✅ passed, but bibliography-only without inline citations should not pass

## Scoring

- **Full Pass**: inline citations present + scoring evidence layers transparent + scope on all strong claims
- **Conditional Pass**: strong structure + scenario-based recommendations but traceability gaps (this case's level)
- **Fail**: source traceability hard-fail + no counter-evidence

## Related evals

- `evals/cases/ai-coding-tools-provider-selection-traceability-fail-case.md` — Failed: same route, zero citations + no register
- `evals/cases/rag-api-provider-selection-traceability-fail-case.md` — Failed: same route, same pattern
