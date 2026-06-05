# Eval: 小红书 Competitive Positioning Register Incompleteness Case

## Goal

Test whether a Competitive Positioning / First-tier report with strong structural execution (dimension-level conclusions, evidence-strength separation, explicit overall-label gate) can still achieve only Conditional Pass when the Source Register has missing entries (S-B10, S-C09 cited in body but not registered), URL completeness is inconsistent, self-assessment overclaims pass status, and delivery residue remains.

## Real case pattern

A user-provided 小红书 (Xiaohongshu) global content community first-tier positioning report dated **2026-06-05** demonstrates this pattern.

**What was done well:**
- ✅ Competitive Positioning route correctly selected with 5-dimension analysis
- ✅ Explicit overall-label gate with aggregation rules → "中国一线成立、全球一线不成立"
- ✅ Body-level `[Sxx]` citations present throughout (not just bibliography)
- ✅ Structured Source Register (§13) with ID / Source / Type / Date / URL / Reliability / Claims Supported
- ✅ Strong counter-evidence (§8: NYT, arXiv, overseas DAU decline, growth ceiling, valuation)
- ✅ Reversal conditions with monitoring paths (§9-§10)
- ✅ Scope clearly defined (global content community, excluding messaging/e-commerce)
- ✅ Market position claims scoped (中国一线 vs 全球一线 vs 准一线)

**Core issues (conditional pass level):**
- ❌ **Source Register entries missing** — S-B10, S-C09 cited in body but have no entries in §13 Source Register. Breaks the "every S# in body maps to register" contract.
- ❌ **URL completeness inconsistent** — S-A10, S-C13, S-D42 are home-page-level URLs; S29 type is INFERRED but Reliability given as M (should be L without explanation)
- ❌ **Self-assessment overconfident** — §12 claims source-traceability ✅ passed despite missing register entries; claims "47 S#" but actual register has 66 IDs
- ❌ **Delivery residue** —末尾 "报告完毕。下一步：PDF 渲染。" is a process note, not deliverable content; Pinterst/Rdit typo
- ❌ **Body-to-register count mismatch** — claims 47 S# cited but register has 66 IDs; reader cannot reconcile

## Scoring

- **Full Pass**: register complete + honest self-assessment + clean delivery
- **Conditional Pass**: strong structure but register gaps + self-assessment overconfidence (this case's level)
- **Fail**: hard-fail triggered

## Related evals

- `evals/cases/cambricon-competitive-positioning-near-pass-case.md` — companion: same route, self-assessment overconfidence
- `evals/cases/unitree-competitive-positioning-secondary-route-case.md` — companion: CP route secondary verification
