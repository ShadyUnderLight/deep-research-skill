# Eval: TSMC Listed-Company — Customer Concentration and Second-Source Risk Case

## Goal

Test whether a Listed-Company / Investment-Style report for a B2B manufacturing company with strong customer lock-in language produces a **customer concentration analysis written as a valuation variable** (affecting revenue visibility, pricing power, margin, and terminal multiple) rather than as a flat risk-list item.

The reference pattern is GPT's deep research version of the TSMC report, which:
- goes beyond "客户锁定强 / 与 NVIDIA、Apple 深度绑定"
- further analyzes: customer structure changes over time, top-10 revenue share trend, second-source de-risking signals by major customers (Google → Samsung/Intel), dual-oligopoly customer structure
- treats customer concentration as a **valuation input** (revenue visibility, gross margin / ASP implications, terminal assumption adjustment) not just a moat description

The reference failure is a TSMC report that has customer lock-in paragraphs but:
- stops at "客户锁定效应强" without analyzing top-10 customer concentration time series
- does not distinguish positive (visibility, co-development) vs negative (pricing power, single-customer volatility) effects
- ignores second-source / dual-source / supplier de-risking signals by major customers
- treats customer concentration as a moat-bolstering fact without connecting it to valuation assumptions

## Prompt

Assess TSMC's competitive position, customer dependence structure, and investment thesis, focusing on customer concentration and supply-chain dynamics. Produce a structured listed-company investment memo that:

- provides a judgment-first opening with clear thesis
- includes a research-anchor block (FY, latest quarter, market snapshot date, management context)
- provides a current financial/market snapshot with clearly dated and cited key numbers
- uses `[Sxx]` or equivalent claim-level inline citations for every load-bearing claim
- includes a complete 7-column Source Register
- **analyzes customer concentration as a valuation variable, not just a risk-list item**
- **distinguishes positive effects (revenue visibility, co-development depth, customer lock-in) from negative effects (pricing power erosion, single-customer volatility risk, second-source substitution)**
- **checks for second-source / dual-source / supplier de-risking signals by major customers and characterizes them as: short-term marginal diversification, long-term structural substitution risk, or supply-chain resilience arrangement**
- **connects customer concentration findings to valuation assumptions (revenue visibility scenarios, gross margin / ASP trajectory, terminal multiple range)**

## What this eval is testing

- whether the report goes beyond "客户锁定强" to include customer concentration time-series data (top-10 share, top-1 share, top-2 share) with time windows and data roles
- whether the report separates positive and negative implications of customer concentration rather than treating it as purely a moat signal or purely a risk
- whether second-source / supplier de-risking signals (e.g., Google exploring Samsung/Intel, Apple diversifying modem suppliers) are analyzed as thesis pressure or threat-window rather than buried in a generic risk list
- whether customer concentration analysis is connected to valuation methodology (revenue visibility confidence, margin/ASP assumptions, terminal multiple adjustments) rather than remaining in a standalone "risk" section
- whether all existing listed-company discipline (research-anchor block, market snapshot, `[Sxx]` traceability, 7-column Source Register) is maintained alongside the new customer concentration content

## Pass criteria

A passing answer should:

1. **Include customer concentration time-series data.**
   - Top-10 customer revenue share (most recent period + prior period for trend)
   - Top-1 customer share and trend
   - Top-2 customer share and trend (to assess dual-oligopoly structure)
   - All data labeled with evidence role: `observed` (from annual report / filing) or `estimate` (from analyst reports / inferred)

2. **Separate positive and negative implications.**
   - Positive: revenue visibility, co-development alignment, high switching costs, long-term contract stability
   - Negative: customer bargaining power, ASP/margin pressure from concentrated buyers, single-customer demand volatility
   - The report must explicitly state whether the net effect on the thesis is positive, negative, or mixed — not just list both sides

3. **Analyze second-source / supplier de-risking signals as thesis pressure.**
   - Identify which major customers have publicly signaled or initiated second-source exploration (e.g., Google with Samsung/Intel, Apple with modem diversification)
   - Characterize each signal: short-term marginal diversification, long-term structural substitution risk, or supply-chain resilience arrangement
   - Frame the analysis as thesis pressure or threat-window (consistent with the competition = thesis pressure rule), not as a generic risk item
   - If multiple signals exist, rank them by materiality to the TSMC thesis

4. **Connect customer concentration to valuation assumptions.**
   - Revenue visibility: does customer concentration increase or decrease confidence in revenue forecasts?
   - Margin/ASP: does concentration affect gross margin trajectory or ASP assumptions?
   - Terminal multiple: should customer concentration or second-source risk adjust the terminal growth rate or PE multiple range?
   - At minimum, state the direction and magnitude of the valuation impact (e.g., "customer concentration reduces terminal multiple by 1-2x" or "dual-oligopoly structure supports revenue visibility, but second-source risk caps margin expansion assumptions")

5. **Maintain all existing listed-company discipline.**
   - research-anchor block present and complete (FY, latest quarter, market snapshot date, management context)
   - market snapshot table present and complete
   - body-level `[Sxx]` traceability for every load-bearing claim
   - 7-column Source Register (ID, Source Name, Type, Date, DOI/URL, Reliability, Claims Supported)
   - evidence labels match source strength
   - conclusion is calibrated to evidence strength, not overstated

## Failure signs

Mark this eval as failed if the answer does any of the following:

- mentions "客户锁定" or "customer lock-in" without providing customer concentration time-series data — the strongest wording requires the strongest evidence, and "客户锁定" without disclosed concentration data is an unsupported claim
- treats customer concentration as purely a moat signal (positive) without acknowledging the negative implications on pricing power, single-customer volatility, or substitution risk
- ignores second-source / dual-source / supplier de-risking signals when analyzing a company with disclosed major-customer exploration of alternative suppliers
- mentions second-source activity but characterizes it only as "risk" without distinguishing between marginal diversification, structural substitution, and resilience arrangement
- discusses customer concentration in a standalone "Risks" section without connecting it to valuation assumptions (revenue visibility, margin, terminal multiple)
- has the same structure as the existing TSMC report — customer concentration appears only as a positive moat point ("客户锁定") and a brief risk mention, without valuation linkage
- uses strong customer-lock-in wording ("深度绑定," "不可替代," "唯一供应商") but does not check for second-source signals (violation of the blocking checklist item in the customer concentration discipline)

## Why this eval matters

The TSMC report from GPT's deep research demonstrates a clear capability gap that the existing local report shares: both have customer lock-in paragraphs, but the local version treats it as a moat descriptor while the GPT version makes it a valuation variable. Specifically:

- GPT version shows top-10 customer share *increasing*, top-1 share *decreasing*, and top-2 share *increasing* — suggesting a dual-oligopoly structure with different implications for revenue visibility (good), pricing power (neutral-to-negative), and second-source risk (emerging)
- Local version mentions "客户锁定效应强" without supporting time-series data, without separating positive/negative effects, and without valuation linkage

Issue #280 proposes checklist items, template table, and moat linkage rules to close this gap. This eval validates that those rules actually produce reports that treat customer concentration as a valuation variable rather than as a risk item or a moat descriptor.

This eval is distinct from existing TSMC eval cases:
- `tsmc-valuation-dcf-and-sensitivity-case.md` — focuses on DCF/reverse DCF and sensitivity matrix
- `tsmc-valuation-time-horizon-stratification-case.md` — focuses on time-stratified valuation judgment
- `tsmc-listed-company-aggregator-source-and-moat-case.md` — focuses on aggregator source discipline
- This case focuses on **customer concentration as an independent valuation variable**

## Current rule verdict

- **Without new rules (status quo)**: existing TSMC report mentions customer lock-in as a moat point and customer concentration as a risk, but does not:
  - provide concentration time-series data
  - distinguish positive vs negative effects
  - analyze second-source signals as thesis pressure
  - connect concentration findings to valuation assumptions
  → This eval would FAIL or CONDITIONAL-PASS (no hard-fail violation but material analytical gap)

- **With new rules (after issue #280)**: a compliant report must analyze customer concentration as a valuation variable with time-series data, positive/negative separation, second-source threat-window analysis, and valuation linkage. → SHOULD PASS

## Relationship to new rules

This eval directly tests the behavioral impact of the rules proposed in issue #280:

1. `checklists/listed-company-report.md` §Customer concentration / second-source discipline — 5 new checklist items covering concentration data, positive/negative separation, second-source analysis, valuation linkage, and blocking-level wording-second-source cross-check
2. `references/report-template.md` §客户集中度与第二供应源风险（如适用） — optional customer concentration table with required columns (top-10 share, top-1 share, top-2 share, second-source signals, valuation implications) and dual-sided analysis requirement
3. `references/moat-monopoly-screening.md` — new strong-claim wording note requiring second-source check when customer-lock-in wording is used, and new concept-boundary trap for "customer lock-in → no substitution risk"

## Related evals

- `evals/cases/tsmc-valuation-dcf-and-sensitivity-case.md` — same company, DCF/sensitivity focus (issue #278)
- `evals/cases/tsmc-valuation-time-horizon-stratification-case.md` — same company, time-horizon stratification focus (issue #277)
- `evals/cases/tsmc-listed-company-aggregator-source-and-moat-case.md` — same company, aggregator source + moat classification focus
- `evals/cases/emc-listed-company-strong-claims-moat-case.md` — moat-style claims evidence gates
- `evals/cases/lotes-listed-company-moat-snapshot-case.md` — moat boundary discipline

## Reviewer checklist

- Are customer concentration time-series data provided (top-10, top-1, top-2 shares) with evidence roles and time windows?
- Are positive and negative implications of customer concentration explicitly separated, with a net-effect conclusion?
- Are second-source / supplier de-risking signals identified and characterized (marginal vs structural vs resilience)?
- Is second-source analysis written as thesis pressure or threat-window (consistent with competition = thesis pressure rule)?
- Are customer concentration findings connected to valuation assumptions (revenue visibility, margin/ASP, terminal multiple)?
- If the report uses customer-lock-in strong wording ("深度绑定," "不可替代"), does it check for second-source signals?
- Does the report avoid the existing TSMC report failure mode — customer concentration as moat description + risk list without valuation linkage?

## Suggested scoring

- **Pass**: customer concentration time-series data provided with evidence roles; positive/negative effects separated with net-effect conclusion; second-source signals identified and characterized as thesis pressure; concentration findings connected to valuation assumptions (revenue visibility, margin, terminal multiple); blocking-level wording-second-source cross-check satisfied; all existing listed-company discipline maintained
- **Conditional pass**: customer concentration section present with time-series data and positive/negative separation, but second-source analysis is partial (signals identified but not characterized by materiality) or valuation linkage is directional without magnitude (says "affects margin assumptions" but not how much); or existing listed-company discipline has minor gaps — no hard-fail violation, but execution quality gap remains
- **Fail**: no customer concentration time-series data despite using customer-lock-in wording (primary hard-fail: strongest wording without strongest evidence); or positive/negative separation absent (treats concentration as purely moat or purely risk); or second-source signals ignored despite known major-customer de-risking activity; or valuation linkage absent (concentration remains in a standalone risk section without valuation connection); or blocking-level wording-second-source cross-check violated (customer-lock-in wording used without checking second-source signals)
