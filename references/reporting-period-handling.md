# Reporting Period Handling

Use this file when the research involves financial reporting periods, fiscal year definitions, quarterly or interim reports, TTM/LTM/NTM calculations, or any claim where the reporting-period definition affects the meaning of a financial number.

Do not assume all companies report on the same calendar or that all financial figures refer to the same period type.

## Core rule

A financial number is only meaningful in context of its reporting period. The same company can have different numbers for "Q1 2026" depending on whether it refers to a fiscal quarter or a calendar quarter.

Always make the reporting-period definition explicit when it affects the claim.

## Fiscal year vs calendar year

Not all companies use the calendar year as their fiscal year.

- **Fiscal year (FY)** — the company's own reporting year, which may start in any month. Example: Apple's FY ends in September; Microsoft's FY ends in June.
- **Calendar year (CY)** — January 1 to December 31.

When using financial data, specify whether the period is FY or CY. `FY2025 revenue` and `CY2025 revenue` can be very different numbers for the same company.

### Example phrasing
- `Apple's FY2025 (ending September 2025) revenue was $X`
- `Calendar year 2025 revenue for [company with December fiscal year-end] was $X`

## Quarterly, interim, and annual reports

Distinguish among:

1. **Annual report** — covers the full fiscal year, typically audited
2. **Interim report** — covers a half-year or nine-month period, typically reviewed but not fully audited
3. **Quarterly report** — covers a three-month period, may be reviewed or unaudited
4. **Earnings release** — preliminary disclosure before the full report, may contain unaudited figures

### Priority when multiple sources exist
If both an earnings release and a full annual/interim report are available, prefer:
1. Full annual report (audited) over interim report
2. Interim report over quarterly report
3. Full report over earnings release (preliminary)

But note: the earnings release may be more current than the last full report. In that case, use the earnings release for the latest quarter while noting it is preliminary.

## TTM / LTM / NTM

These are derived periods, not reported periods. They require explicit calculation or sourcing.

### TTM / LTM (Trailing Twelve Months / Last Twelve Months)

- Refers to the most recent 12-month period, often constructed from the latest quarterly data
- TTM and LTM are generally interchangeable in financial analysis
- Used for valuation metrics like PE when the company's fiscal year does not align with the analysis date

### NTM (Next Twelve Months)

- Refers to the forward 12-month period, typically based on consensus estimates
- Used for forward valuation metrics like forward PE

### Disclosure requirement
When using TTM, LTM, or NTM figures:
- State the construction method: `TTM PE calculated using the most recent four quarters of earnings`
- Or state the source: `TTM PE as reported by Bloomberg as of [date]`
- Do not present TTM figures as if they were reported annual figures

### Common confusion
- TTM is not the same as the latest fiscal year if the fiscal year does not end on the analysis date
- NTM is not the same as the next fiscal year if the fiscal year does not start on the analysis date
- TTM PE and forward PE are different metrics; do not use them interchangeably

## Preliminary, unaudited, and restated

### Preliminary
- Earnings releases or pre-announced figures before the full report
- May be subject to revision
- Label as `preliminary` or `per earnings release`

### Unaudited
- Quarterly or interim figures that have not been fully audited
- Label as `unaudited` or `per interim report`

### Restated
- Financial figures that have been revised by the company after initial publication
- Restated figures supersede earlier published figures
- Always use restated figures when available, and note that they are restated
- Do not use the original figures if restated figures exist, unless analyzing the revision itself

### Example phrasing
- `Q1 2026 revenue (preliminary, per earnings release dated 2026-04-15): $X`
- `FY2025 revenue (audited, per annual report): $X`
- `FY2024 revenue (restated in FY2025 annual report): $X`

## "Latest data" around earnings dates

The definition of "latest available data" changes around earnings releases.

### Before earnings release
- The latest reported period is the previous quarter or interim
- Current market snapshot is the most recent trading data
- Forward estimates are based on pre-release consensus

### After earnings release, before full report
- The latest reported period is the newly released quarter (preliminary)
- Consensus may not yet be updated
- Label the new quarter as preliminary

### After full report
- The latest reported period is the newly reported quarter (from the full report)
- Full report data supersedes the earnings release

### Decision rule
If the report date is materially after an expected earnings release date:
- Check whether a newer period should be available
- If the report uses an older period, explain why (e.g., `the company has not yet released Q1 2026 results`)
- Do not silently use an older period when a newer one should exist

## Post-period events

Events occurring after the reporting period but before the research date may affect the interpretation of financial data.

Examples:
- M&A completed after the reporting period
- New product launch after the reporting period
- Management change after the reporting period
- Capital raise or buyback after the reporting period

When post-period events are relevant:
- State the event and its timing
- Do not treat post-period events as if they were reflected in the reported financials
- Separate the reported data from the post-period event implications

### Example phrasing
- `FY2025 revenue was $X. In January 2026 (post-period), the company completed acquisition of [target], which is not reflected in FY2025 figures.`

## Boundary: this file does not cover

This file focuses on reporting-period definitions and financial-number context. It does not cover:

- **Quiet periods / silent periods** — regulatory restrictions on company communications before earnings
- **Insider trading rules** — legal restrictions on trading by insiders
- **Trading restrictions** — blackout periods or compliance-related trading limitations

These are compliance and trading-behavior topics, not research-output disciplines.

## Common failure patterns

### TTM confused with latest fiscal year
Using FY2025 revenue when the analysis date is March 2026 and TTM revenue would include Q4 2025 + Q1-Q3 2026 (if available).

### Preliminary treated as audited
Using earnings-release figures without noting they are preliminary and may be revised in the full report.

### Restated figures not used
Using original FY2024 figures when the FY2025 annual report contains restated FY2024 figures.

### Fiscal year assumed to be calendar year
Writing `2025 revenue` for a company with a June fiscal year-end, creating ambiguity about whether CY2025 or FY2025 is meant.

### Old period used without explanation
Using Q3 2025 data in a March 2026 report without checking whether Q4 2025 results should be available.

## Relationship to other discipline files

- `references/finance-date-discipline.md` covers the broader time-layer separation (historical vs snapshot vs forward). This file focuses specifically on period definitions and conventions.
- `references/analyst-consensus-handling.md` covers consensus data handling. Consensus estimates have their own period definitions (FY1, FY2, NTM) that should follow the conventions in this file.
- `references/valuation-methodology.md` covers valuation methodology. Many valuation metrics use TTM or NTM figures; the period definition affects the metric meaning.
