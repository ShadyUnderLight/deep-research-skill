# Eval: 具身智能商业化路径 Market Outlook — Source Register + Label Overuse Case (Round 7)

## Goal

Test whether a market-outlook / industry-evolution report with strong scenario structure, stakeholder coverage, and monitoring signals can still receive a **Fail** rating when:

- **Source Register noncompliant** — 5 columns only (claims 6, actual is 5), missing DOI/URL and Claims Supported; S01-S60 listed but only 16 actually cited in body — register inflation without body mapping
- **process-integrity hard-fail** — audit status claims `Source Traceability ✅`, `Forward-looking ✅`, `Final Audit ✅` but Register noncompliant, forward-looking claims bare, labels overused
- **`[CONF]` label overuse** — secondary/media/analyst sources supporting deployment numbers, competitive position estimates labeled as confirmed facts
- **forward-looking claims without source role** — "预计淘汰率 50%+""预计 >100 台" without named source or method; audit claims all forward-looking tagged but body contradicts
- **quantitative role labels defined but not executed** — §18-25 defines O/P/A/M labels but body tables lack per-number role annotations
- **metadata-first drift** — evidence grading and numeric role instructions occupy front page (§3-25) before judgment

This is the **eighth Round 7 case**.

## Real case pattern

A user-provided report "具身智能创业公司商业化路径分化研究报告" dated **2026-06-10** demonstrates this pattern. Inferred route: `market-outlook / industry-evolution`.

**What was done well:**
- ✅ Opening carries core judgment — "三轨分化" at line 31
- ✅ Current market snapshot: shipments, sales, competitor tiers
- ✅ Drivers and blockers separated
- ✅ Three scenarios (base/optimistic/pessimistic)
- ✅ Stakeholder implications ≥4 types: founders, investors, enterprise buyers, policymakers
- ✅ Monitoring signals specific and actionable
- ✅ Counter-evidence strong (§312-329)
- ✅ Uncertainty register explicit
- ✅ Decision usefulness: actionable for founders, investors, enterprise buyers

**Core issues (Fail — hard-fail triggered):**
- ❌ **Source Register noncompliant** — has 5 columns (ID / Source Name / Type / Date / Reliability), missing DOI/URL and Claims Supported per Round 4 #182 template. Lists S01-S60 but only 16 are actually cited in body — register inflation without claim-level mapping. Audit claims "6列" but actual is 5 columns.
- ❌ **Process-integrity hard-fail** — §389-394 claims `Source Traceability ✅`, `Forward-looking ✅`, `Final Audit ✅`, but Register is noncompliant (5 columns), forward-looking claims are bare ("预计淘汰率 50%+" without source), and `[CONF]` labels overused.
- ❌ **`[CONF]` label overuse** — secondary/media/analyst sources supporting deployment numbers (生产部署不足 500 台), competitive position ("压倒性优势"), market share estimates labeled as `[CONF]` without source-role downgrade per Round 5 #191.
- ❌ **Forward-looking claims without source role** — "预计淘汰率 50%+""预计工业/物流行业看到 >100 台" stated without named source, method, or confidence interval. Audit claims all forward-looking tagged but body evidence contradicts.
- ❌ **Quantitative role labels defined not executed** — §18-25 defines O/P/A/M label system but body tables and key numbers lack per-number role annotations. Framework declared, labels not applied.
- ❌ **Metadata-first drift** — §3-25 front page occupied by research method, evidence grading, numeric role instructions before core judgment at line 31.

## Why this case exists

Eighth Round 7 case. The same failure triad confirmed across 8 cases and 4 routes. Adds two notable patterns: (1) register inflation (60 entries, 44 uncited), and (2) labels defined but not executed — a variant of the "declared not executed" pattern seen in Round 6 academic cases.

## Round 7 accumulation

| # | Case | Route | Core failure |
|---|------|-------|-------------|
| 1 | Code review agent selection | provider-selection | Triad |
| 2 | Chinese LLM writing | provider-selection | Triad + aggregation |
| 3 | AI image generation | provider-selection | Triad + metadata drift |
| 4 | Tea brand overseas entry | market-entry | Triad |
| 5 | Short drama overseas entry | market-entry | Triad + hub-role + sensitivity |
| 6 | Industrial robot overseas entry | market-entry | Triad + compound criterion |
| 7 | AI video market outlook | market-outlook | Triad + label overuse + ext verification |
| 8 | Embodied AI market outlook | market-outlook | Triad + register inflation + labels declared not executed |

## Related evals

- `evals/cases/ai-video-market-outlook-label-and-probability-gap-case.md` — Round 7: market-outlook label overuse
- `evals/cases/llm-hallucination-academic-review-source-register-gap-case.md` — Round 6: evidence framework declared not executed
