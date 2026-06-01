# Eval: 小红书 Private Company / Startup Evaluation Near-Pass Case

## Goal

Test whether a private company / startup evaluation report with strong source traceability (66 `[SN]` inline citations) and transparent evidence tiering (T1/T2/T3) can still have minor but instructive gaps in source citation completeness, label accuracy, and sensitivity analysis.

This eval targets a failure mode where:

- the report achieves **near-perfect source traceability** (66 `[SN]` citations, structured register, T1/T2/T3 tiering)
- but has a **registry vs body mismatch** (S21 listed in appendix but never cited in body)
- has a **label inflation instance** (2025E $3B revenue labeled as [确认事实] when source is Bloomberg/T2 media estimate)
- is missing **sensitivity analysis** (quantitative-role-audit BLOCKER)
- misses a **formal research-anchor block** (private company context)

This case is the **strongest source traceability benchmark** so far — better than the Round 2 TikTok AI case (42 `[SN]`) and far better than Round 1 cases. It validates that the #145 fix (source traceability hardening) is producing measurable improvements.

## Real case pattern

A user-provided 小红书 (Xiaohongshu / RED) deep investment research report dated **2026-06-01** demonstrates this near-pass pattern:

**What was done exceptionally well:**
- ✅ **66 `[SN]` inline citations** — highest density across all 11 eval cases; validates #145 PR effectiveness
- ✅ **T1/T2/T3 evidence tiering** — transparent source quality stratification throughout
- ✅ **`is_estimated` / `[代理指标]` / `[模型输出]` labels** — full quantitative role labeling coverage
- ✅ **Dual-route execution (startup-evaluation primary + listed-company secondary)** — both routes' mandatory sections present
- ✅ **Judgment-first opening with 10 evidence-tagged bullets**
- ✅ **Counter-evidence: 11 bear-case items** (§7.2)
- ✅ **Uncertainty register: 6 items (§9.2) + 5 limitations (Appendix B)**
- ✅ **Data conflict explicit presentation** — no artificial smoothing
- ✅ **All 6 startup-evaluation hard-fail conditions passed**
- ✅ **Four-perspective recommendation table** (§10.2: 一级市场/二级市场/战略/竞品)
- ✅ **12-24 month milestone roadmap** (§8)

**What has minor gaps:**
- ⚠️ **S21 registered but never cited** — Appendix A lists S21 (晚点 LatePost "小红书 2024 财务关键数据") but body text has no `[S21]` reference. Violates the "no uncited sources" discipline.
- ⚠️ **2025E $3B labeled [确认事实] instead of [推断]** — line 45 and 165-166 label 2025E revenue $3B as [确认事实][S1], but S1 is Bloomberg/T2 media estimate, not company disclosure. This is a label inflation instance.
- ❌ **Sensitivity analysis missing (BLOCKER)** — quantitative-role-audit requires sensitivity tables (±20%, ±50%) for load-bearing assumptions. The report has three scenarios (§7.3: 乐观/基准/悲观) but no formal sensitivity table with explicit assumption variation.
- ⚠️ **No formal research-anchor block** — for the listed-company secondary route, the report lacks a compact "FY / quarter / snapshot date" anchor block. While partly justifiable (private company has no quarterly filings), the exception was not documented.
- ⚠️ **[IN]/[UN] format deviation** — uses [推断]/[未知] (Chinese) instead of [IN]/[UN] (English). Semantically equivalent but format-noncompliant per SKILL.md convention.

## What this eval is testing

### Test Dimension 1: Source registry completeness discipline

S21 is listed in the appendix with full metadata but never referenced in the body. This is a "dead entry" — it wastes reader trust because the reader who sees S21 in the appendix will assume it was cited somewhere and may search for it. The discipline is: **every register entry must have at least one body citation; every body citation must point to a register entry.**

### Test Dimension 2: Label accuracy for media-estimated numbers

2025E $3B revenue is from Bloomberg/T2 media, not company disclosure. Labeling it as [确认事实] overstates the certainty. The correct label would be [推断] or a more specific role like [彭博 estimate]. This is the same pattern as the 泡泡玛特 case's "2025E label inflation" — both involve forward-looking estimates being labeled as confirmed facts.

### Test Dimension 3: Sensitivity analysis completeness

The report has scenario analysis (optimistic/base/pessimistic with 30/50/20% probabilities) but lacks formal sensitivity tables. The quantitative-role-audit checklist requires explicit sensitivity grading (low/medium/high) with ±20% and ±50% variation tables for load-bearing assumptions. This is a BLOCKER.

### Test Dimension 4: Dual-route private company execution

The report successfully executes both startup-evaluation (primary) and listed-company (secondary) routes — a rare pattern that the 人形机器人 case failed at. The key difference: here the secondary route's hard-fail conditions were mostly checked, with the anchor-block gap being a minor exception rather than a systemic failure.

## Pass criteria

A good answer should:

1. **No uncited source register entries** — every `[S#]` in the appendix has at least one body reference
2. **Label accuracy** — media estimates are not labeled as [确认事实]; use [推断] or specific source role labels
3. **Sensitivity analysis present** — load-bearing assumptions have ±20% and ±50% sensitivity tables or explicit sensitivity grading
4. **Secondary route hard-fails documented** — if a secondary route's hard-fail condition is not applicable (e.g., no market snapshot for private company), the exception is explicitly recorded
5. **Inline citation format consistent** — all inference/uncertainty labels use the same format throughout

## Failure signs

Mark this eval as **near-pass** (not fail) if the answer:

- has 60+ strong `[SN]` inline citations but 1 uncited register entry
- has 1-2 label inflation instances (media estimate as [确认事实])
- lacks sensitivity analysis despite having scenario analysis
- is otherwise a high-quality private company report (this case's level)

Mark as **fail** if source traceability hard-fail is triggered (zero [SN] in body), or if startup-evaluation hard-fail conditions are triggered.

## Why this case exists

This case is the **strongest source traceability benchmark** across all 11 eval cases. It validates that the Round 1 batch fix (especially #145) produced measurable improvement.

| Metric | Pre-Round-1 worst | TikTok AI (Round 2) | 小红书 (Round 2) |
|--------|-------------------|---------------------|------------------|
| `[SN]` inline citations | 0 (人形机器人) | 42 | **66** |
| Source register entries | 0 (Moore Threads) | 20+ | **21** |
| Evidence tiering | None | None | **T1/T2/T3** |
| Quantitative role labels | None | partial | **Full (`is_estimated`, `[代理指标]`, `[模型输出]`)** |

The gaps that remain (uncited S21, 1 label inflation instance, missing sensitivity table) are the **marginal improvements** for the next fix cycle.

| Gap | Existing coverage | This case adds |
|-----|-------------------|----------------|
| **Uncited register entry** | Not covered | Registry completeness: every S# must have body citation |
| **Label inflation for media estimates** | 泡泡玛特: 2025E label inflation | Confirms recurring pattern: forward-looking estimates labeled as confirmed fact |
| **Sensitivity analysis missing** | Not explicitly covered | BLOCKER in quantitative-role-audit: scenario analysis ≠ sensitivity analysis |
| **Dual-route private company execution** | 人形机器人: dual-route failure | Successful dual-route with minor gaps (contrast) |

## Suggested intervention target

- `references/source-traceability-and-claim-citation.md` — add: "every source register entry must have at least one body-text `[SN]` reference; uncited entries should be removed or a body reference added"
- `checklists/source-traceability.md` — add non-blocker: "all register entries are cited at least once in body text"
- `references/quantitative-role-labeling.md` — strengthen: "scenario analysis without sensitivity tables is not sufficient for load-bearing assumptions; ±20% and ±50% variation tables are required for high-sensitivity assumptions"
- `checklists/quantitative-role-audit.md` — clarify: "scenario analysis (optimistic/base/pessimistic) does not replace sensitivity analysis (vary one assumption at a time)"
- `checklists/startup-company-report.md` — add: "if listed-company is a secondary route, document which hard-fail conditions are not applicable and why" (anchor block waiver for private companies)

(**Note**: the label inflation for media estimates is a recurring pattern across Round 2 — AI Traffic Police (vendor claims), 泡泡玛特 (2025E), 小红书 (2025E). This should be addressed as a batch fix.)

## Reviewer checklist

- Are all source register entries cited at least once in the body text?
- Are media estimates / third-party data clearly labeled as [推断] or specific source role, not [确认事实]?
- Is sensitivity analysis present for load-bearing assumptions (not just scenario analysis)?
- If listed-company is a secondary route for a private company, are inapplicable hard-fail conditions documented?
- Are inline citation formats consistent throughout?

## Suggested scoring

- **Full pass**: all register entries cited, labels accurate, sensitivity analysis present, secondary route hard-fails documented
- **Near-pass**: 60+ strong citations but 1 uncited entry + 1 label inflation + missing sensitivity analysis (this case's level)
- **Fail**: source traceability hard-fail, or startup-evaluation hard-fail triggered

## Related evals

- `evals/cases/pop-mart-listed-company-traceability-hard-fail-case.md` — companion case: label inflation for 2025E estimate
- `evals/cases/ai-traffic-police-technical-deep-dive-traceability-case.md` — companion case: vendor claim label inconsistency
- `evals/cases/tiktok-ai-technical-deep-dive-route-inflation-case.md` — companion case: dual-route execution with unchecked secondary
- `evals/cases/humanoid-robot-market-outlook-dual-route-case.md` — dual-route failure (contrast: this case succeeds with minor gaps)
