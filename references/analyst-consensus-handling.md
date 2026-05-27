# Analyst Consensus Handling

Use this file when the research involves analyst consensus data, including consensus estimates, target prices, ratings, EPS forecasts, revenue forecasts, or any aggregated third-party view.

Do not treat consensus data as confirmed fact. Consensus is a summary of third-party opinions, not a report of company performance.

## Core rule

Consensus data requires metadata to be meaningful. A consensus number without source, date, coverage count, and dispersion context is under-specified.

`Analysts expect EPS of $5.20` is insufficient. `Bloomberg consensus as of 2026-03-15: FY2026E EPS $5.20 (range $4.80–$5.60, 24 analysts)` is properly specified.

## Required metadata

For every consensus data point, capture at minimum:

- **Source / platform** — Bloomberg, FactSet, Refinitiv, Visible Alpha, or other
- **Date** — when the consensus was compiled
- **Coverage count** — number of analysts included
- **Metric basis** — fiscal year, TTM, NTM, or specific quarter

When the data is available, also capture:

- **Range** — high and low estimates
- **Dispersion** — standard deviation, coefficient of variation, or range as percentage of mean
- **Revision direction** — whether consensus has been rising, falling, or stable

## Types of consensus data

Distinguish clearly among:

1. **Consensus estimate** — aggregated EPS, revenue, EBITDA, or other financial metric forecasts
2. **Consensus target price** — aggregated price targets from covering analysts
3. **Consensus rating** — aggregated buy/hold/sell recommendations
4. **Individual analyst estimate** — a single analyst's forecast, not consensus

Do not blur these. A consensus target price is not a consensus EPS estimate. A consensus rating is not a valuation.

## Consensus estimate handling

### Source labeling
Always name the platform. `Consensus EPS is $5.20` is insufficient. `Bloomberg consensus EPS is $5.20` is acceptable.

### Date labeling
Consensus data is time-bound. Always show the compilation date. A consensus from before the latest earnings release may be stale.

### Coverage count
A consensus from 3 analysts carries less weight than one from 30 analysts. Show the count when available.

### Range and dispersion
When available, show the range or dispersion. High dispersion signals uncertainty; low dispersion signals convergence.

Example phrasing:
- `Bloomberg consensus FY2026E EPS: $5.20 (range $4.80–$5.60, 24 analysts, compiled 2026-03-15)`
- `Consensus target price: $180 (range $140–$220, high dispersion suggests divergent views on growth trajectory)`

## Consensus target price handling

Consensus target prices are opinions, not valuations. They reflect analyst methodology and assumptions, not market truth.

### Do not treat as fair value
`The consensus target price is $180, suggesting 20% upside` implies the stock should be worth $180. Better: `The consensus target price is $180 (range $140–$220), which analysts derive from [methodology if known].`

### Show dispersion when material
If target prices range from $100 to $250, the "consensus" of $175 is not a strong signal. High dispersion means analysts disagree substantially on methodology or assumptions.

### Time relevance
Target prices set 6 months ago may not reflect current conditions. Note when target prices were last updated if the data is available.

## Consensus rating handling

Consensus ratings are coarse signals. A "Buy" consensus from 15 analysts with 10 "Strong Buy" and 5 "Hold" is different from 15 "Buy" ratings.

### Show distribution when available
- `Consensus: Buy (15 Buy, 5 Hold, 2 Sell)` is more informative than `Consensus: Buy`
- `Rating distribution skewed toward Buy` is acceptable when exact counts are unavailable

### Do not equate with valuation
A "Buy" rating does not mean the stock is undervalued. It means analysts covering the stock recommend buying it, based on their individual methodologies.

## Post-earnings stale consensus

After an earnings release, consensus estimates may not update immediately. Some platforms show pre-earnings consensus for days or weeks after the report.

### Detection
If the report date is materially after an earnings release, check whether the consensus data reflects the new information.

### Downgrade rule
If consensus data is likely pre-earnings:
- Label it as potentially stale
- Do not use it as the primary basis for forward-looking financial claims
- Prefer the company's own guidance or the most recent individual analyst updates

### Example phrasing
- `Bloomberg consensus FY2026E EPS: $5.20 (compiled 2026-01-15, before Q4 2025 earnings release on 2026-02-01 — may not reflect updated guidance)`
- `Post-earnings consensus has not yet updated; the figure below uses management guidance as the more current source`

## Consensus vs company guidance

When both consensus and company guidance are available:

- Prefer company guidance for the company's own targets
- Use consensus for the market's aggregated expectation
- Show both when they diverge materially

Example phrasing:
- `Management guides FY2026 revenue of $50–52B. Bloomberg consensus expects $53B. The gap may reflect analyst assumptions about [factor].`

## Common failure patterns

### Consensus target price as fair value
`The stock is undervalued because the consensus target is $180 and it trades at $150` conflates analyst opinions with intrinsic value.

### Consensus without metadata
`Analysts expect 20% growth` — which analysts? From when? Based on what reported period?

### Stale consensus used as current
Using pre-earnings consensus to make post-earnings claims without noting the timing gap.

### Consensus rating without distribution
`The stock has a Buy consensus` — how many analysts? How strong is the consensus? Any Hold or Sell?

### Blending consensus types
Using "consensus" to refer ambiguously to either estimates, target prices, or ratings without specifying which.

## Relationship to other discipline files

- `references/finance-date-discipline.md` covers time-layer separation for financial numbers. This file focuses specifically on consensus data handling.
- `references/valuation-methodology.md` covers valuation methodology selection and precision discipline. Consensus target prices are one input, not a valuation method.
- `references/forward-looking-discipline.md` covers forward-looking claims discipline. Consensus estimates are forward-looking and should follow those labeling rules.
