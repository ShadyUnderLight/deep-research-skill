# Eval: 研华 Listed-Company Source Traceability Hard-Fail Case

## Goal

Test whether a Listed-Company report with strong business analysis, structured bull/bear, and clear uncertainty register can still receive a **Fail** rating when body-level source citations are entirely absent (hard-fail), market snapshot lacks PB/PS/52-week, valuation lacks recomputable method, and the self-declared audit status falsely claims source-traceability passed.

## Real case pattern

A user-provided 研华 (2395.TW) deep research report dated **2026-06-05** demonstrates this pattern.

**What was done well:**
- ✅ Complete research anchor block (FY2025, 2026Q1, 2026-06-03 snapshot, mgmt)
- ✅ Strong business analysis with competitive positioning
- ✅ Structured bull/bear with uncertainty register
- ✅ Counter-evidence present (bear case, risks, unresolved questions)
- ✅ Uncertainty explicitly weakens buy recommendation
- ✅ Financial data complete (revenue, margin, cash flow, segment growth)
- ✅ Judgment-first opening with clear thesis

**Fail causes:**
- ❌ **Source traceability hard-fail** — body has zero `[Sxx]` inline citations; source register exists (§215-233) but not referenced from body
- ❌ **Self-assessment falsely claims pass** — §201-211 claims source-traceability ✅ passed ("正文包含[SN]引用标记"), directly contradicted by the report body
- ❌ **Market snapshot incomplete** — PB, PS, 52-week high/low missing; PE not labeled TTM/Forward
- ❌ **Valuation lacks method** — "38-40x is historical mid-high / upside limited" stated without historical range, comparable company logic, or scenario framework
- ❌ **Strong position claims without sourcing** — "全球最大的工业物联网", "全球工业PC市场份额第一", "连续20+年" lack body-level source, scope, or downgrade notation

## Scoring

- **Full Pass**: inline citations present + complete snapshot + recomputable valuation + honest self-assessment
- **Fail**: source traceability hard-fail + self-assessment contradiction (this case's level)

## Related evals

- `evals/cases/meituan-listed-company-traceability-gap-case.md` — companion: zero inline citations, self-assessment overconfidence
- `evals/cases/emc-listed-company-strong-claims-moat-case.md` — companion: strong claims evidence mismatch
