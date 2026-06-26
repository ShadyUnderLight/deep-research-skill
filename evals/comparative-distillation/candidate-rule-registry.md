# Candidate Rule Registry

Purpose: cross-case candidate tracking for comparative distillation.
Only promote rules recurring across 2+ real cases.

Reference: `references/comparative-distillation-method.md#step-6`

---

## Summary finding

PROMOTE_NOW candidates from the first 13 distillation cases are **already covered** by existing checklists, SKILL.md, and reference documents. See each entry below for exact coverage location.

Two new distillation cases (issue #320) produced **5 new PROMOTE_NOW candidates (R61-R65)** that were not previously covered. These have been implemented via template/checklist updates in issue #320 — see each entry for the new coverage location.

---

## Candidate-action table

### Legend

| Column | Meaning |
|---|---|
| ID | Unique identifier |
| Candidate rule | Imperative statement of the rule |
| Action type | NEW_RULE / CHECKLIST_HARDENING / TEMPLATE_CHANGE / DELIVERY_HARD_FAIL |
| Source file(s) | Distillation case file(s) that produced this candidate |
| Frequency | Number of cases that independently produced this or a near-identical candidate |
| Original label | PROMOTE_NOW / WAIT_FOR_SECOND_CASE / (unlabeled) |
| Existing coverage | File path and line number(s) where this rule already exists in the skill system |
| Coverage status | 已覆盖 / 部分覆盖 / 无覆盖 / 已延期 |

---

| ID | Candidate rule | Action type | Source file(s) | Frequency | Original label | Existing coverage | Coverage status |
|---|---|---|---|---|---|---|---|
| R01 | Require a current market snapshot before forward-looking sections | CHECKLIST_HARDENING | ai-coding-agent-market-outlook | 1 | PROMOTE_NOW | `checklists/final-audit.md` L119; `references/report-template.md` L230-251 | 已覆盖 |
| R02 | Label outlook numbers as observed / inferred / scenario / illustrative | NEW_RULE | ai-coding-agent-market-outlook, sea-market-entry | 2 | PROMOTE_NOW | `checklists/final-audit.md` L130; `references/report-template.md` L244-249; `references/decision-report-template.md` L109, L161 | 已覆盖 |
| R03 | Add a dedicated market-outlook decision structure | TEMPLATE_CHANGE | ai-coding-agent-market-outlook | 1 | PROMOTE_NOW | `references/decision-report-template.md` L142-162 | 已覆盖 |
| R04 | Force market-outlook reports to include stakeholder implications and monitoring signals | CHECKLIST_HARDENING | ai-coding-agent-market-outlook | 1 | PROMOTE_NOW | `references/report-template.md` L236-241; `references/decision-report-template.md` L149, L153 | 已覆盖 |
| R05 | Use typed memo blocks for scenario-heavy and comparison-heavy sections | TEMPLATE_CHANGE | ai-coding-agent-market-outlook | 1 | PROMOTE_NOW | `references/decision-report-template.md` L142-155 (whole market-outlook structure) | 已覆盖 |
| R06 | Add evidence-tier inflation guard | NEW_RULE | amd-minimax-equity-report, cas-space-minimax-company-report | 2 | PROMOTE_NOW | `checklists/listed-company-report.md` L85-91; `checklists/final-audit.md` L73-74 | 已覆盖 |
| R07 | Add metric-scope audit for load-bearing numeric claims | CHECKLIST_HARDENING | amd-minimax-equity-report, cas-space-minimax-company-report | 2 | PROMOTE_NOW | `checklists/final-audit.md` L137-141; `checklists/listed-company-report.md` L88-89 | 已覆盖 |
| R08 | Add unknown-to-conclusion linkage audit | CHECKLIST_HARDENING | amd-minimax-equity-report, cas-space-minimax-company-report | 2 | PROMOTE_NOW | `checklists/final-audit.md` L145-152; `checklists/listed-company-report.md` L77 | 已覆盖 |
| R09 | Tighten company-report structure around thesis-first flow | TEMPLATE_CHANGE | amd-minimax-equity-report, cas-space-minimax-company-report | 2 | PROMOTE_NOW | `checklists/final-audit.md` L69-83; `checklists/listed-company-report.md` L70-81; `references/decision-report-template.md` L204-268 | 已覆盖 |
| R10 | Add thesis-break / watch-metrics section later | WAIT_FOR_SECOND_CASE | amd-minimax-equity-report | 1 | WAIT_FOR_SECOND_CASE | `checklists/final-audit.md` L150; `checklists/option-selection-final-audit.md` L75-76; `references/decision-report-template.md` L413-431 | 已延期 |
| R11 | Add provider-selection current snapshot gate | NEW_RULE | api-supplier-selection | 1 | (unlabeled) | `checklists/final-audit.md` L109; `checklists/option-selection-final-audit.md` L40-43; `references/decision-report-template.md` L164-183 | 已覆盖 |
| R12 | Harden option-selection final audit for provider tasks | CHECKLIST_HARDENING | api-supplier-selection | 1 | (unlabeled) | `checklists/option-selection-final-audit.md` (entire file); `references/decision-report-template.md` L164-183 | 已覆盖 |
| R13 | Update decision-report template for provider selection | TEMPLATE_CHANGE | api-supplier-selection | 1 | (unlabeled) | `references/decision-report-template.md` L164-183 | 已覆盖 |
| R14 | Strengthen freshness audit for fast-moving vendor/model reports | CHECKLIST_HARDENING | api-supplier-selection | 1 | (unlabeled) | `checklists/option-selection-final-audit.md` L40-43; `checklists/final-audit.md` L103 | 已覆盖 |
| R15 | Market-position conclusions require scope + conditional clause | CHECKLIST_HARDENING | byd | 1 | PROMOTE_NOW | `checklists/final-audit.md` L156-159; `references/report-template.md` L203-210 | 已覆盖 |
| R16 | Use exact figures when source provides exact figures | NEW_RULE | byd | 1 | PROMOTE_NOW | `checklists/final-audit.md` L129 | 已覆盖 |
| R17 | Add data-calibration note when using proxies or approximate mappings | TEMPLATE_CHANGE | byd | 1 | PROMOTE_NOW | `references/report-template.md` L195-201 | 已覆盖 |
| R18 | Add evidence-tier legend at report top | TEMPLATE_CHANGE | byd | 1 | PROMOTE_NOW | `references/report-template.md` L153-183 | 已覆盖 |
| R19 | Every forward-looking figure must name the source of the estimate | CHECKLIST_HARDENING | byd | 1 | PROMOTE_NOW | `checklists/final-audit.md` L127-128; `checklists/forward-looking-claims.md` L32-34 | 已覆盖 |
| R20 | State the right unit of comparison in competitive analysis | NEW_RULE | byd | 1 | PROMOTE_NOW | `references/report-template.md` L212-222; `checklists/option-selection-final-audit.md` L30-33 | 已覆盖 |
| R21 | Pair scale growth with profitability/cash-flow pressure when both exist | NEW_RULE | byd | 1 | PROMOTE_NOW | `checklists/final-audit.md` L163-165; `references/report-template.md` L224-228 | 已覆盖 |
| R22 | Tighten company-report opening into judgment-summary-first structure | TEMPLATE_CHANGE | cas-space-minimax-company-report | 1 | PROMOTE_NOW | `checklists/final-audit.md` L69-71; `checklists/listed-company-report.md` L70-71; `references/decision-report-template.md` L204-220 | 已覆盖 |
| R23 | Add issuer-claim grading guard | NEW_RULE | cas-space-minimax-company-report | 1 | PROMOTE_NOW | `checklists/listed-company-report.md` L85-91; `checklists/final-audit.md` L73-74 | 已覆盖 |
| R24 | Add company-report judgment audit | CHECKLIST_HARDENING | cas-space-minimax-company-report | 1 | PROMOTE_NOW | `checklists/final-audit.md` L69-83 | 已覆盖 |
| R25 | Add stronger metric-scope audit for company-report numbers | CHECKLIST_HARDENING | cas-space-minimax-company-report | 1 | PROMOTE_NOW | `checklists/final-audit.md` L137-141 | 已覆盖 |
| R26 | Add unknown-to-conclusion linkage audit (company reports) | CHECKLIST_HARDENING | cas-space-minimax-company-report | 1 | PROMOTE_NOW | `checklists/final-audit.md` L145-152 | 已覆盖 |
| R27 | Add final PDF delivery gate for company-style reports | CHECKLIST_HARDENING | cas-space-minimax-company-report | 1 | PROMOTE_NOW | `checklists/final-audit.md` L196-214; also L213-214 | 已覆盖 |
| R28 | Require research-anchor block before broad company narrative | TEMPLATE_CHANGE | china-shenhua | 1 | PROMOTE_NOW | `checklists/listed-company-report.md` L6-14, L21, L43-45; `references/decision-report-template.md` L211 | 已覆盖 |
| R29 | Separate multi-venue and market-snapshot number roles | CHECKLIST_HARDENING | china-shenhua | 1 | PROMOTE_NOW | `checklists/listed-company-report.md` L22-24 | 已覆盖 |
| R30 | Require body-level auditability for thesis-bearing claims | CHECKLIST_HARDENING | china-shenhua | 1 | PROMOTE_NOW | `checklists/final-audit.md` L18; `checklists/listed-company-report.md` L73 | 已覆盖 |
| R31 | Add corporate-action compression guard | NEW_RULE | china-shenhua | 1 | PROMOTE_NOW | `checklists/final-audit.md` L78; `checklists/listed-company-report.md` L81; `references/decision-report-template.md` L222-228 | 已覆盖 |
| R32 | Tighten front-page judgment visibility under investment-style route | TEMPLATE_CHANGE | china-shenhua | 1 | PROMOTE_NOW | `checklists/final-audit.md` L169-172; `references/decision-report-template.md` L42-55 | 已覆盖 |
| R33 | Require early support / weakening / unresolved split | TEMPLATE_CHANGE | china-shenhua | 1 | PROMOTE_NOW | `checklists/listed-company-report.md` L74-75; `checklists/final-audit.md` L36-38; `references/decision-report-template.md` L248-253 | 已覆盖 |
| R34 | Route hardware/equipment procurement as procurement-style decision memo | NEW_RULE | home-server-equipment-recommendation | 1 | (unlabeled) | `checklists/final-audit.md` L111 | 已覆盖 |
| R35 | Require recommendation compression (top / runner-up / rejected routes) | CHECKLIST_HARDENING | home-server-equipment-recommendation | 1 | (unlabeled) | `checklists/final-audit.md` L112; `checklists/option-selection-final-audit.md` L56-63; `references/decision-report-template.md` L270-296 | 已覆盖 |
| R36 | Require budget closure (explicit includes/excludes, min vs recommended config) | CHECKLIST_HARDENING | home-server-equipment-recommendation | 1 | (unlabeled) | `checklists/final-audit.md` L113-114; `references/decision-report-template.md` L279-280, L292 | 已覆盖 |
| R37 | Require hardware-system fit reasoning | CHECKLIST_HARDENING | home-server-equipment-recommendation | 1 | (unlabeled) | `checklists/final-audit.md` L115; `references/decision-report-template.md` L281 | 已覆盖 |
| R38 | Require household-ops cost visibility (power, noise, maintenance, etc.) | CHECKLIST_HARDENING | home-server-equipment-recommendation | 1 | (unlabeled) | `checklists/final-audit.md` L116; `references/decision-report-template.md` L283-294 | 已覆盖 |
| R39 | PDF broken typography = delivery hard fail | DELIVERY_HARD_FAIL | home-server-equipment-recommendation | 1 | (unlabeled) | `checklists/final-audit.md` L213-214 | 已覆盖 |
| R40 | Require market-entry outputs to show explicit decision status, hard gates, sequencing, ranking-change logic | CHECKLIST_HARDENING | japan-vs-china-vs-sea-market-entry | 1 | (unlabeled) | `checklists/final-audit.md` L117; `checklists/option-selection-final-audit.md` L47-52; `references/decision-report-template.md` L298-325 | 已覆盖 |
| R41 | Require visible separation between evidence-layer labels and modeling-layer number-role labels | CHECKLIST_HARDENING | japan-vs-china-vs-sea-market-entry | 1 | (unlabeled) | `checklists/final-audit.md` L130-132; `references/report-template.md` L173-181 | 已覆盖 |
| R42 | Add target-language consistency gate for load-bearing structural labels | NEW_RULE + CHECKLIST_HARDENING | japan-vs-china-vs-sea-market-entry | 1 | (unlabeled) | `checklists/final-audit.md` L196-202; `references/report-template.md` L157 | 已覆盖 |
| R43 | Treat mixed-language labels and CJK broken-export as final-delivery failures | CHECKLIST_HARDENING | japan-vs-china-vs-sea-market-entry | 1 | (unlabeled) | `checklists/final-audit.md` L198-200, L213-214 | 已覆盖 |
| R44 | Require role-labeling of key quantitative inputs in constrained-choice memos | CHECKLIST_HARDENING | multi-origin-meetup-city-selection | 1 | PROMOTE_NOW | `checklists/final-audit.md` L131; `checklists/option-selection-final-audit.md` L34 | 已覆盖 |
| R45 | Strengthen fairness/aggregation gate for multi-stakeholder selection | CHECKLIST_HARDENING | multi-origin-meetup-city-selection | 1 | PROMOTE_NOW | `checklists/option-selection-final-audit.md` L35-36 | 已覆盖 |
| R46 | Strengthen option-selection structure to show shortlist-construction logic and loser-specific failures | TEMPLATE_CHANGE | multi-origin-meetup-city-selection | 1 | PROMOTE_NOW | `checklists/option-selection-final-audit.md` L56-63; `references/decision-report-template.md` L122-140 | 已覆盖 |
| R47 | Strengthen option-selection structure with ranking-reversal conditions | TEMPLATE_CHANGE | multi-origin-meetup-city-selection | 1 | PROMOTE_NOW | `checklists/option-selection-final-audit.md` L73-78; `references/decision-report-template.md` L139-140 | 已覆盖 |
| R48 | Add practical-planning heuristic for multi-origin meetup/location choice (hidden friction) | NEW_RULE | multi-origin-meetup-city-selection | 1 | PROMOTE_NOW | `checklists/option-selection-final-audit.md` L36; `references/decision-report-template.md` L294 (household) | 已覆盖 |
| R49 | Add explicit market-entry trigger routing for go/no-go / regional expansion tasks | NEW_RULE | sea-market-entry | 1 | PROMOTE_NOW | `checklists/option-selection-final-audit.md` L47-52; `references/report-template.md` L253-283 | 已覆盖 |
| R50 | Add a dedicated market-entry memo structure | TEMPLATE_CHANGE | sea-market-entry | 1 | PROMOTE_NOW | `references/decision-report-template.md` L298-325 | 已覆盖 |
| R51 | Require distinction of regional hub vs first beachhead vs later expansion | NEW_RULE | sea-market-entry | 1 | PROMOTE_NOW | `checklists/option-selection-final-audit.md` L49; `references/decision-report-template.md` L317 | 已覆盖 |
| R52 | Require one visible comparison unit across countries/markets | NEW_RULE | sea-market-entry | 1 | PROMOTE_NOW | `checklists/option-selection-final-audit.md` L50; `references/decision-report-template.md` L305, L322 | 已覆盖 |
| R53 | Require explicit hard gates and priority relative to alternatives | CHECKLIST_HARDENING | sea-market-entry | 1 | PROMOTE_NOW | `checklists/option-selection-final-audit.md` L48, L51-52 | 已覆盖 |
| R54 | Treat citation/retrieval artifact leakage as final-delivery failure | CHECKLIST_HARDENING | sea-market-entry | 1 | PROMOTE_NOW | `checklists/final-audit.md` L206-208 | 已覆盖 |
| R55 | Separate operational feasibility, stable traits, and subjective reputation claims | NEW_RULE | weekend-seaside-destination | 1 | PROMOTE_NOW | `checklists/option-selection-final-audit.md` L67-69 | 已覆盖 |
| R56 | Require explicit aggregation logic for multi-origin comparisons | NEW_RULE | weekend-seaside-destination | 1 | PROMOTE_NOW | `checklists/option-selection-final-audit.md` L30-33 | 已覆盖 |
| R57 | Combine source-class note + evidence labels + stronger mapping for strong claims | TEMPLATE_CHANGE | weekend-seaside-destination | 1 | WAIT_FOR_SECOND_CASE | `references/report-template.md` L153-183; `checklists/final-audit.md` L15-19 | 已延期 |
| R58 | Express travel uncertainty as scenario risks + fallback plans | CHECKLIST_HARDENING | weekend-seaside-destination | 1 | WAIT_FOR_SECOND_CASE | `checklists/option-selection-final-audit.md` L73-78; `references/decision-report-template.md` L139-140 | 已延期 |
| R59 | For destination-selection tasks, lead with decision frame → comparison → shortlist → detail | TEMPLATE_CHANGE | weekend-seaside-destination | 1 | PROMOTE_NOW | `checklists/option-selection-final-audit.md` L56-57; `references/decision-report-template.md` L122-140 | 已覆盖 |
| R60 | Optimize destination-selection reports for choice architecture rather than guide-style description | NEW_RULE | weekend-seaside-destination | 1 | PROMOTE_NOW | `checklists/option-selection-final-audit.md` L84-88 | 已覆盖 |
| R61 | Add Input boundary / 未指定项 block for constrained-choice / market-entry / market-outlook templates | TEMPLATE_CHANGE | small-team-ai-agent, dc-power | 2 | PROMOTE_NOW | `references/report-template.md` §输入边界与未指定项（#320） | 已覆盖 |
| R62 | Add Value-chain sensitivity map for industry-chain market-outlook | TEMPLATE_CHANGE + CHECKLIST_HARDENING | dc-power | 1 | PROMOTE_NOW | `references/market-outlook-and-scenario-discipline.md` §Value-chain sensitivity map; `checklists/market-outlook-audit.md` §Value-chain sensitivity coverage（#320） | 已覆盖 |
| R63 | Add Regional coverage matrix with source role for global scope | TEMPLATE_CHANGE + CHECKLIST_HARDENING | dc-power | 1 | PROMOTE_NOW | `references/market-outlook-and-scenario-discipline.md` §Regional coverage matrix; `checklists/market-outlook-audit.md` §Regional coverage（#320） | 已覆盖 |
| R64 | Upgrade Stakeholder implications to action table (decision/action/metric/trigger) | TEMPLATE_CHANGE + CHECKLIST_HARDENING | small-team-ai-agent, dc-power | 2 | PROMOTE_NOW | `references/market-outlook-and-scenario-discipline.md` §Stakeholder action table; `checklists/market-outlook-audit.md` §Stakeholder actionability（#320） | 已覆盖 |
| R65 | Add Implementation stages integration in option-selection structure | TEMPLATE_CHANGE | small-team-ai-agent | 1 | PROMOTE_NOW | `references/decision-report-template.md` §实施路线（#320） | 已覆盖 |
| R66 | Add provider current-state external verifiability check (last-verified date, contradiction = hard fail) | CHECKLIST_HARDENING | ai-coding-provider-selection | 1 | PROMOTE_NOW | `checklists/option-selection-final-audit.md` (new) via [#331](https://github.com/ShadyUnderLight/deep-research-skill/issues/331) | 待实现 |
| R67 | Require vendor claim caveat "(厂商文档，非独立验证)" for provider docs in body | CHECKLIST_HARDENING | ai-coding-provider-selection | 1 | PROMOTE_NOW | `checklists/option-selection-final-audit.md` (new) via [#331](https://github.com/ShadyUnderLight/deep-research-skill/issues/331) | 待实现 |
| R68 | Require body-level `[Sxx]` + numeric role labels on market-data estimates in market-entry reports | CHECKLIST_HARDENING | ai-edu-market-entry | 1 | PROMOTE_NOW | `checklists/option-selection-final-audit.md` (new) via [#331](https://github.com/ShadyUnderLight/deep-research-skill/issues/331) | 待实现 |
| R69 | Require sensitivity analysis for load-bearing estimated variables in market-entry (what change would reverse recommendation) | NEW_RULE | ai-edu-market-entry | 1 | PROMOTE_NOW | `checklists/option-selection-final-audit.md` via [#331](https://github.com/ShadyUnderLight/deep-research-skill/issues/331) | 待实现 |
| R70 | Require shortlist boundary justification: list excluded options and rationale | CHECKLIST_HARDENING | ai-edu-market-entry | 1 | PROMOTE_NOW | `references/decision-report-template.md` via [#331](https://github.com/ShadyUnderLight/deep-research-skill/issues/331) | 待实现 |
| R71 | Add inference-register disconnected-from-body detection method | CHECKLIST_HARDENING | agent-api-market-outlook | 1 | PROMOTE_NOW | `checklists/final-audit.md` (new) via [#331](https://github.com/ShadyUnderLight/deep-research-skill/issues/331) | 待实现 |
| R72 | Add monitoring signal actionability 4-field verification (threshold, cadence, source, trigger-to-action) | CHECKLIST_HARDENING | agent-api-market-outlook | 1 | PROMOTE_NOW | `checklists/market-outlook-audit.md` via [#331](https://github.com/ShadyUnderLight/deep-research-skill/issues/331) | 待实现 |
| R73 | Add route-boundary check: market-outlook reports containing competitive-positioning content must document rationale | NEW_RULE | agent-api-market-outlook | 1 | PROMOTE_NOW | `checklists/market-outlook-audit.md` via [#331](https://github.com/ShadyUnderLight/deep-research-skill/issues/331) | 待实现 |
| R74 | Add simulation/model-output status disclosure requirement (conceptual / executed / illustrative) | NEW_RULE | world-cup-constrained-choice | 1 | WAIT_FOR_SECOND_CASE | `references/model-output-and-simulation-discipline.md` via [#342](https://github.com/ShadyUnderLight/deep-research-skill/issues/342); `scripts/validate_simulation_claims.py` | 新规则（观察中） |
| R75 | P-value / CI / Elo / Poisson / Monte Carlo without execution evidence triggers validator warning | NEW_RULE | world-cup-constrained-choice | 1 | WAIT_FOR_SECOND_CASE | `scripts/validate_simulation_claims.py` via [#342](https://github.com/ShadyUnderLight/deep-research-skill/issues/342) | 新规则（观察中） |
| R76 | When tournament/event data does not yet exist, require explicit placeholder variables with assumption boundaries (event-count, sample-size, lookback-window, known constraints) instead of fabricating data or dismissing the question | CHECKLIST_HARDENING | world-cup-transition-vs-possession-gpt-vs-local-comparative-distillation | 1 | PROMOTE_NOW | `checklists/forward-looking-claims.md` via [#344](https://github.com/ShadyUnderLight/deep-research-skill/issues/344) (pending) | 新规则（待实现） |
| R77 | When combining crowd-sourced structural data (Wikipedia format/history) with externally sourced quantitative models (Elo ratings, Monte Carlo), separate data layers with explicit provenance per layer in the Source Register | CHECKLIST_HARDENING | world-cup-group-winner-path-advantage-gpt-vs-local-comparative-distillation | 1 | PROMOTE_NOW | `checklists/final-audit.md` via [#344](https://github.com/ShadyUnderLight/deep-research-skill/issues/344) (pending) | 新规则（待实现） |

---

## Summary statistics

| Metric | Count |
|---|---|---|
| Total candidate rules (all files) | 77 |
| PROMOTE_NOW | 58 |
| WAIT_FOR_SECOND_CASE | 5 |
| (unlabeled, implicitly actionable) | 14 |
| **Covered by existing code** | **62 / 77** (81%) |
| Pending / WAIT_FOR_SECOND_CASE | 5 (R10, R57, R58, R74, R75) |
| Pending / #331 implementation | 8 (R66-R73: new candidates from three GPT-vs-local comparisons) |
| Pending / #344 implementation | 2 (R76-R77: new candidates from four World Cup GPT-vs-local comparisons) |
| **Truly uncovered PROMOTE_NOW** | **10** (R66-R73 from #331 + R76-R77 from #344) — pending checklist/template updates |

---

## Cross-case recurrence analysis

### Rules appearing in ≥2 cases

| Candidate theme | Cases | Current status |
|---|---|---|
| Evidence-tier inflation guard | amd (R06), cas-space (R06) | Already in `checklists/listed-company-report.md` L85-91 |
| Metric-scope audit | amd (R07), cas-space (R07) | Already in `checklists/final-audit.md` L137-141 |
| Unknown-to-conclusion linkage | amd (R08), cas-space (R08) | Already in `checklists/final-audit.md` L145-152 |
| Thesis-first company structure | amd (R09), cas-space (R09) | Already in `checklists/final-audit.md` L69-83 |
| Outlook number role labeling | ai-coding-agent (R02), sea-market-entry (merged) | Already in `checklists/final-audit.md` L130 |
| Career/skill-selection proxy indicator discipline | programming-language-learning (new) | Already in `checklists/option-selection-final-audit.md` via [#308](https://github.com/ShadyUnderLight/deep-research-skill/issues/308) |

All recurring rules are already covered. No new promotion is needed.

### Recent additions (June 2026)

Two new comparative-distillation cases were added as part of issue #310:

- **World Cup constrained-choice** (`world-cup-constrained-choice-gpt-vs-local-comparative-distillation.md`): Identified constrained-choice probability-distribution gaps (probability method opacity, numeric role labeling, route wiring, self-assessment accuracy). All gaps closed by [#306](https://github.com/ShadyUnderLight/deep-research-skill/issues/306), [#307](https://github.com/ShadyUnderLight/deep-research-skill/issues/307), [#309](https://github.com/ShadyUnderLight/deep-research-skill/issues/309).

- **Programming language learning** (`programming-language-learning-gpt-vs-local-comparative-distillation.md`): Identified career/skill-selection proxy discipline gaps (proxy indicator conflation, US-vs-global scope confusion, bare learning time estimates, shortlist boundary leak). All gaps closed by [#306](https://github.com/ShadyUnderLight/deep-research-skill/issues/306), [#308](https://github.com/ShadyUnderLight/deep-research-skill/issues/308), [#309](https://github.com/ShadyUnderLight/deep-research-skill/issues/309).

Both cases have all 6 candidate actions marked `NO_ACTION` — confirming the existing rule coverage is sufficient and the gaps were primarily execution/wiring problems.

Two new comparative-distillation cases were added as part of issue #320:

- **Small-team AI Agent** (`small-team-ai-agent-gpt-vs-local-comparative-distillation.md`): Identified template-level gaps — Input boundary declaration, implementation stages integration, stakeholder action table. All candidates promoted as `TEMPLATE_CHANGE` (R61, R64, R65), implemented in [#320](https://github.com/ShadyUnderLight/deep-research-skill/issues/320).

- **Data center power bottleneck** (`data-center-power-bottleneck-gpt-vs-local-comparative-distillation.md`): Identified template + checklist gaps — Value-chain sensitivity map, Regional coverage matrix, stakeholder action table. All candidates promoted as `TEMPLATE_CHANGE + CHECKLIST_HARDENING` (R62, R63, R64). Cross-case confirmed R61 (input boundary) and R64 (action table) from the AI Agent case.

Three new comparative-distillation cases were added as part of issue #331:

- **AI Coding Agent provider-selection** (`ai-coding-provider-selection-gpt-vs-local-comparative-distillation.md`): Identified execution-level gaps — provider current-state external verifiability, vendor claim caveat for provider docs. Both candidates promoted as `CHECKLIST_HARDENING` (R66, R67). The numeric-role and self-assessment execution gap was determined to be a pure execution problem (existing rules, no new action needed). Confirmed that #325 and #327 already cover the enterprise rollout structure gap.

- **AI Education market-entry** (`ai-edu-market-entry-gpt-vs-local-comparative-distillation.md`): Identified mixed gaps — sensitivity analysis for load-bearing estimated variables (missing rule, R69), market-data traceability/shortlist boundary justification (execution reinforcement, R68, R70), and two-level funnel already covered by #328.

- **Agent API market-outlook** (`agent-api-market-outlook-gpt-vs-local-comparative-distillation.md`): Identified mixed gaps — route boundary for market-outlook + positioning content (missing rule, R73), inference register disconnected-from-body detection and monitoring actionability 4-field verification (execution reinforcement, R71, R72). Structural gaps confirmed covered by #329 and #330.

All three cases track real reports with verified failure patterns. Together they produce **8 new candidates** (R66-R73), of which 6 are `CHECKLIST_HARDENING` and 2 are `NEW_RULE`.

Four new comparative-distillation cases were added as part of issue #344:

- **World Cup best-third-rule** (`world-cup-best-third-rule-gpt-vs-local-comparative-distillation.md`): Route self-declaration mismatch (Shared-workflow vs regulatory-analysis). All 6 candidate actions are `NO_ACTION` — gaps closed by [#340](https://github.com/ShadyUnderLight/deep-research-skill/issues/340) and [#343](https://github.com/ShadyUnderLight/deep-research-skill/issues/343). Serves as regression baseline.

- **World Cup info-advantage** (`world-cup-info-advantage-gpt-vs-local-comparative-distillation.md`): Source strength failure (100% Wikipedia with full traceability infrastructure = traceability theatre). All 6 candidate actions are `NO_ACTION` — gaps closed by [#341](https://github.com/ShadyUnderLight/deep-research-skill/issues/341). Serves as regression baseline.

- **World Cup transition-vs-possession** (`world-cup-transition-vs-possession-gpt-vs-local-comparative-distillation.md`): Method-scaffold with false statistics + stale "data not yet generated" claims. 5 dimensions `NO_ACTION`, 1 dimension `CHECKLIST_HARDENING` → **R76** (data-unavailable method-scaffold pattern). Distinct from #342 simulation contract: covers the case where data genuinely doesn't exist, not where simulation was claimed but not executed.

- **World Cup group-winner path-advantage** (`world-cup-group-winner-path-advantage-gpt-vs-local-comparative-distillation.md`): Simulation claims without execution evidence + Wikipedia-only + cross-source contamination. 5 dimensions `NO_ACTION`, 1 dimension `CHECKLIST_HARDENING` → **R77** (cross-source model contamination pattern). Extends beyond #341 (per-source strength) and #342 (simulation contract): requires layer separation when combining fundamentally different data reliability tiers.

Together they produce **2 new candidates** (R76, R77), both `CHECKLIST_HARDENING`, with companion eval cases at `evals/cases/world-cup-transition-vs-possession-method-scaffold-case.md` and `evals/cases/world-cup-group-winner-simulation-contract-case.md`.

### 链路原因：本地已有但未执行

本轮四组对比暴露出 **规则存在但执行链未触发** 的系统性问题，其根因链路如下：

| # | 链路原因 | 具体表现 | 修复 | 在本轮中的证据 |
|---|---|---|---|---|
| 1 | **总控未覆盖** | `audit_report.py` 的 `ROUTE_VALIDATORS` 未包含 `regulatory-analysis`、`competition-positioning` 等成熟路线；报告选对路线也无法触发对应 checklist/validator | [#340](https://github.com/ShadyUnderLight/deep-research-skill/issues/340) 将所有路线加入总控映射 | 最佳第三名报告：内容属 regulatory 但路线未在总控中 → 无法触发 regulatory contract |
| 2 | **unknown route 静默回退** | 当报告的 route 声明不在 `ROUTE_VALIDATORS` 中时，`audit_report.py` fallback 到 `technical-deep-dive` validators → 错误路线通过错误的审计链 | [#340](https://github.com/ShadyUnderLight/deep-research-skill/issues/340) 禁止静默回退，输出明确的 "unsupported route" error | 最佳第三名报告：若通过旧版总控，Shared-workflow 不在映射中，会 fallback 到 tech-dive，regulatory 缺陷不会被发现 |
| 3 | **自评块未被 validator 约束** | 报告的自评 audit status 声称所有 ✅ 通过，但 body 执行缺 `[Sxx]` 引用、Wikipedia-only 来源、数字角色缺失 → process-integrity hard-fail 未触发 | [#340](https://github.com/ShadyUnderLight/deep-research-skill/issues/340) 路线接入总控后，`check_audit_self_assessment_consistency` 对所有路线强制执行 | 信息优势报告：8/8 Wikipedia 来源标注 high reliability，自评仍声称全部 ✅ |
| 4 | **untracked eval 未进入 CI** | 本轮的两个 eval case 在 issue 创建时为本地草稿，未纳入 `evals/INDEX.md`，因此未进入 `test_eval_index.py` 的回归测试覆盖 | 本 PR ([#344](https://github.com/ShadyUnderLight/deep-research-skill/issues/344)) 将两个已有 eval case + 两个新 eval case 全部纳入 INDEX.md，通过 `test_eval_index.py` 和 `test_issue_344_contracts.py` 验证进入回归链 | `world-cup-rule-regulatory-route-mismatch-case.md` 和 `world-cup-info-advantage-technical-deep-dive-source-strength-case.md` 在 INDEX.md 中已注册为 active/fail，但在本 PR 前缺少 CI 级别的 index coverage 验证 |

**关键教训：** 这四个问题不是独立 bug，而是同一根因链路的四个环节——总控覆盖不完整 → 未知路线静默回退 → 自评不受约束 → 回归资产未 CI。每个环节在本轮四组报告中都有具体证据。修复 [#340](https://github.com/ShadyUnderLight/deep-research-skill/issues/340) 切断了前三个环节的链路，本 PR 切断第四个。

---

## Conclusion for issue #96

All PROMOTE_NOW candidates from the 13 existing distillation cases are already covered by the current skill system. The existing checklists, SKILL.md, and reference documents have absorbed the lessons from all 13 comparisons.

**There is nothing new to promote.** Running 2-3 additional distillation cases is unlikely to produce uncovered rule discoveries; the marginal value would be validating that the current coverage is sufficient.

The remaining gap is **execution/activation discipline** — the model often does not follow rules that already exist in checklists and templates. This is tracked separately in issue #97 and in failure-taxonomy.md.
