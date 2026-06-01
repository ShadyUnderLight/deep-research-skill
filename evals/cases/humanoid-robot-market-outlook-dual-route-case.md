# Eval: 人形机器人 Market Outlook Dual-Route Execution Case

## Goal

Test whether a dual-route report (Market Outlook primary + Listed Company secondary) can execute both route contracts simultaneously without one route's gaps leaking through the other.

This eval targets a failure mode where:

- the primary route (Market Outlook) is mostly executed correctly
- the secondary route (Listed Company) is attached but not fully executed — its hard-fail conditions (fresh anchor, inline source citations) are violated
- the reader sees a polished industry report, but the investment-grade portions contain stale anchors and untraceable claims

## Real case pattern

A user-provided 人形机器人产业链深度投资研究报告 (Humanoid Robot Industry Chain Deep Investment Research Report, dated **2026-05-29**) demonstrates this dual-route pattern:

**What was done well:**
- ✅ Market Outlook route explicitly selected in design document
- ✅ Judgment-first opening (Section 1 with 7 judgment statements tagged [Confirmed]/[Inference])
- ✅ Evidence labeling consistent throughout (Confirmed / Inference / Manufacturer-claim / Unknown)
- ✅ Market size baseline with assumptions ($10-30B by 2030, cost decline 15-20%/yr)
- ✅ Monitoring signals (Section 12 with 5 signals)
- ✅ Multi-source comparison (Goldman Sachs vs other estimates)
- ✅ 8 research dimensions all covered as requested
- ✅ Base case explicit with quantitative range
- ✅ Forward-looking claims labeled and sourced

**What was missing or wrong:**
- ❌ **Stale anchor on listed-company sub-route** — 优必选 (UBTECH) financial data anchored on FY2023 annual report, which is 2+ years old from the report date (2026-05-29). No freshness re-check was performed. This triggers the listed-company route hard-fail condition.
- ❌ **No inline source citations** — Section 13 is a loose bibliography without [SN]-format inline references. Load-bearing claims cannot be traced to specific sources in the body text.
- ❌ **Missing alternative scenarios chapter** — Market Outlook route requires structured multi-scenario analysis. The report only has a single base case ($10-30B) with one mention of a pessimistic reference ($3-8B), not a full scenario framework.
- ❌ **Stakeholder coverage limited to investors** — Market Outlook route requires multi-stakeholder implications (tech developers, policymakers, enterprises, end users), but the report only covers investor perspectives.
- ⚠️ **Background-first drift** — Sections 2-4 (~200 lines, 37% of report) are descriptive industry overview. Core outlook/judgment content starts at Section 5.
- ⚠️ **Duplicate row error** — 汇川技术 appears twice in the target-company table (Section 8.1).

## What this eval is testing

### Failure Mode 1: Dual-route execution gap

The primary route (Market Outlook) was explicitly selected and mostly executed. The secondary route (Listed Company) was attached but its hard-fail conditions were not checked before delivery.

This is distinct from:
- **Pure listed-company cases** (AMAT, Intel) where listed-company is the primary route — here it's secondary, and the stale anchor failure happened because the route was attached but not audited
- **Pure market-outlook cases** where the route contract is fully checked

The lesson: **attaching a secondary route requires running that route's hard-fail checks too**, not just the primary route's.

### Failure Mode 2: Stale anchor on a secondary-route company

优必选's FY2023 data (2+ years old) was used as the current financial anchor without:
- freshness re-check
- notation that data may be outdated
- attempt to find FY2024 or FY2025 data

This is similar to `evals/cases/intel-current-state-freshness-case.md` but differs in that:
- Intel was the primary subject of a listed-company report
- 优必选 is one of several companies in a market-outlook report with an attached listed-company sub-route

This suggests the stale-anchor problem is **cross-route** — it can appear whenever listed-company data is used, even in non-primary routes.

### Failure Mode 3: No inline source citations despite bibliography

Section 13 has a bibliography, but load-bearing claims in the body have no `[SN]` inline references. This is a source-traceability hard-fail.

This differs from `evals/cases/source-traceability-moore-threads-case.md` (complete absence of sourcing) and `evals/cases/innolight-listed-company-execution-case.md` (inconsistent inline citations). Here the issue is: **bibliography exists but body-text traceability is zero**.

### Failure Mode 4: Missing alternative scenarios in Market Outlook

The Market Outlook route requires structured multi-scenario analysis. The report has a base case and mentions one pessimistic reference, but lacks:
- a dedicated scenarios chapter
- optimistic / base / pessimistic with distinct assumptions
- scenario-specific probability weights or confidence levels

### Failure Mode 5: Stakeholder coverage limited to investors

Market Outlook requires implications for multiple stakeholder types. The report covers only investment implications.

## Pass criteria

A good dual-route answer should:

1. **Primary route contract fully satisfied** — market snapshot, drivers/blockers, base case, alternative scenarios, stakeholder implications, monitoring signals
2. **Secondary route hard-fail conditions checked** — if a listed-company sub-route is attached, its hard-fail conditions (fresh anchor, market snapshot, traceability) must be checked before delivery, not assumed
3. **Stale-anchor gate for all company data** — any company financial data used as a current anchor must be fresh-tested regardless of whether the company is the primary subject or one of many
4. **Inline source citations** — load-bearing claims have body-level `[SN]` references, not just a bibliography appendix
5. **Multi-stakeholder implications** — Market Outlook covers implications for tech developers, enterprises, policymakers, end users, not just investors

## Failure signs

Mark this eval as failed if the answer does any of the following:

- attaches a secondary route (listed-company) but does not check its hard-fail conditions before delivery
- uses company financial data 2+ years old as a current anchor without freshness notice
- has load-bearing claims in the body with no inline source citation format
- has a bibliography appendix but zero inline `[SN]` references in the body
- lacks a structured alternative-scenarios chapter for a Market Outlook task
- covers only investor stakeholder implications for a Market Outlook task

## Why this case exists

This case adds coverage for:

| Gap | Existing coverage | This case adds |
|-----|-------------------|----------------|
| **Dual-route execution** | No existing eval covers multi-route report failures | Secondary route hard-fail conditions not checked |
| **Stale anchor in non-primary context** | Intel case covers stale anchor in primary listed-company report | Stale anchor can happen when listed-company is a sub-route |
| **Bibliography without inline citations** | Moore Threads: no sourcing at all; Innolight: inconsistent citations | Bibliography exists but body traceability is zero |
| **Missing alternative scenarios** | No Market Outlook eval in cases/ directory | First Market Outlook route eval covering scenario completeness |
| **Limited stakeholder implications** | No eval covers this Market Outlook requirement | Stakeholder coverage too narrow |

## Suggested intervention target

This case suggests changes at multiple layers:

- `checklists/route-activation-audit.md` — add check: "if a secondary route is attached, its hard-fail conditions are checked before delivery, not just assumed"
- `ROUTING-MATRIX.md` — add explicit note: "secondary route hard-fail checks are not optional; each attached route's fail-fast conditions must be verified"
- `checklists/listed-company-report.md` — already covers stale anchor, but needs cross-reference: "this check applies even when listed-company is a sub-route, not just primary route"
- `references/source-traceability-and-claim-citation.md` — strengthen: "a bibliography appendix without body-level inline citations is not sufficient; every load-bearing claim must have a visible source link in the body"
- `references/market-outlook-and-scenario-discipline.md` — add: "stakeholder implications must cover at least 3 stakeholder types; investor-only is not sufficient"
- `checklists/final-audit.md` — add non-blocker: "secondary route hard-fail conditions verified before delivery"

## Reviewer checklist

- Was the primary route correctly identified and executed?
- If a secondary route was attached, were its hard-fail conditions checked?
- Are all company financial anchors fresh (not 2+ years old)?
- Do load-bearing claims have inline source citations, not just a bibliography appendix?
- Does the report have structured alternative scenarios (optimistic/base/pessimistic)?
- Do stakeholder implications cover more than just investors?

## Suggested scoring

- **Full pass**: primary route fully satisfied, secondary route hard-fail conditions checked, inline citations present, alternative scenarios structured, multi-stakeholder coverage
- **Partial pass**: primary route mostly satisfied but secondary route gaps present (this case's level)
- **Fail**: primary route hard-fail triggered, or secondary route has blocker-level violations without acknowledgment

## Related evals

- `evals/cases/intel-current-state-freshness-case.md` — stale anchor in primary listed-company report
- `evals/cases/innolight-listed-company-execution-case.md` — inconsistent inline citations
- `evals/cases/amat-listed-company-anchor-and-label-execution-case.md` — cluster failure in listed-company route
- `evals/meta/rule-activation-and-execution-discipline.md` — distinguishes missing-rule vs missing-trigger vs execution-failure (this case: execution-failure on secondary route hard-fail checks)
