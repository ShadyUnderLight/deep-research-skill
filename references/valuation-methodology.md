# Valuation Methodology

Use this file when the research involves valuation judgments, target prices, valuation multiples, or any claim about whether a company is cheap, expensive, fairly valued, or mispriced.

Do not confuse a valuation snapshot with a valuation judgment.

## Core rule

A valuation snapshot is a data point. A valuation judgment is a conclusion that requires methodology, assumptions, and evidence quality assessment.

Presenting a PE ratio without methodology context is reporting. Concluding that a stock is "undervalued" or "overpriced" is a judgment that carries a higher evidence burden.

## Snapshot vs judgment

Always separate:

1. **Valuation snapshot** — current market data: stock price, market cap, PE, PB, PS, EV/EBITDA, dividend yield, 52-week range. This is observed fact from a market platform.
2. **Valuation judgment** — whether the current pricing is justified, stretched, or discounted relative to fundamentals, peers, or intrinsic value. This requires methodology and assumptions.

Do not let a snapshot masquerade as a judgment. `The stock trades at 15x TTM PE` is a snapshot. `The stock appears cheap relative to its historical range` is a judgment that needs supporting evidence.

## Metric selection logic

Choose valuation metrics based on company characteristics, not habit.

### PE (Price / Earnings)

Use when:
- earnings are positive and reasonably stable
- the company is not highly cyclical at a trough or peak
- the business model is not undergoing structural transition

Do not use when:
- the company is loss-making or has volatile earnings
- the industry is at a cyclical extreme (peak or trough)
- one-time gains or losses distort reported earnings

### PB (Price / Book)

Use when:
- asset values are meaningful (banks, insurance, real estate, industrials)
- earnings are volatile but book value is more stable
- the company has significant tangible assets

Do not use when:
- the company is asset-light (software, services, platform businesses)
- intangible assets dominate but are not reflected in book value
- book value is negative or distorted by accumulated losses

### PS (Price / Sales)

Use when:
- the company is loss-making or margin structure is unstable
- revenue is more reliable than earnings for the business model
- the company is early-stage but has meaningful revenue

Do not use when:
- margin structure is stable and well-understood (use PE instead)
- revenue quality is questionable (related-party, one-time, unsustainable)

### EV/EBITDA

Use when:
- capital structure differences matter (comparing levered vs unlevered companies)
- depreciation policies distort earnings comparisons
- the industry standard uses this metric (telecom, media, infrastructure)

Do not use when:
- working capital or capex intensity varies dramatically without adjustment
- the company has significant operating leases not reflected in EBITDA

### DCF (Discounted Cash Flow)

Use when:
- cash flows are predictable enough to model
- the company has a long operating history
- terminal value assumptions can be reasonably bounded

Do not use when:
- cash flows are too volatile or uncertain for meaningful projection
- the company is pre-revenue or pre-profit with no clear path
- the model would depend on speculative assumptions about distant future

### SOTP (Sum of the Parts)

Use when:
- the company has distinct business segments with different valuation logics
- conglomerate discount or premium is material
- segment-level data is sufficient for independent valuation

Do not use when:
- segment data is insufficient or unreliable
- inter-segment dependencies make separation artificial

## Precision downgrade rules

Downgrade valuation precision when the company or data quality does not support precise conclusions.

### Cyclical companies

- Do not use peak or trough earnings as the base for PE valuation without explicit cycle-stage labeling
- Prefer mid-cycle earnings normalization or PB when cycle position is uncertain
- Label the valuation as "cycle-dependent" rather than presenting a single-point PE

### Loss-making companies

- Do not force a PE-based valuation
- Use PS, EV/Revenue, or EV/EBITDA if margins are expected to normalize
- If no reasonable metric applies, state that valuation cannot be meaningfully assessed with available data
- Do not invent a "forward PE" based on speculative profitability timeline

### High-growth companies

- Forward PE or EV/Revenue may be more relevant than TTM PE
- But label clearly: "based on consensus estimates" or "based on management guidance"
- Do not present forward metrics as if they were reported facts
- Acknowledge that growth assumptions drive the valuation heavily

### Companies with major corporate actions

- If M&A, restructuring, asset injection, or spin-off is pending or recent, valuation may be distorted
- Split the valuation into pre-action and post-action scenarios when relevant
- Do not compress transaction certainty into valuation certainty

## Target price discipline

Do not give a target price unless:
- sufficient data exists to support a methodology
- the assumptions are explicit and defensible
- the time horizon is stated
- the confidence level is honest

When target price cannot be supported, prefer:
- directional judgment (looks stretched / appears reasonable / seems discounted)
- valuation range with explicit assumptions
- "insufficient data for a target price" as a valid conclusion

## Valuation inference documentation

When presenting a valuation range, target price, or fair value estimate labeled as inference, the reader must be able to reconstruct the reasoning chain. Do not present a valuation conclusion without visible methodology.

### Required elements for valuation inference

Every valuation inference must include:

1. **Multiple assumption range** — state the PE (or other metric) range used, not just the final number. Example: "基于2026年预期PE 25-30x" rather than "目标价600元"
2. **Comparable selection logic** — if comparables are used, state why these companies were chosen and what they share with the target. Do not assume the reader knows why Company X is a valid comp
3. **Scenario parameters** — if the valuation uses optimistic/base/pessimistic scenarios, state the key variable that differs across scenarios (e.g., margin assumption, growth rate, market share)
4. **Limitation disclosure** — state what the valuation does not capture or where the methodology is weakest

### Metric selection justification

When the report uses one metric as the primary valuation anchor, briefly state why. This is especially important when:

- the company has characteristics that could support multiple metrics (e.g., positive earnings AND significant assets)
- the chosen metric is not the industry default
- the company is in a transitional state (post-restructuring, cyclical trough, high-growth phase)

Example pattern: "选用PE而非EV/EBITDA作为主要估值锚，因为[公司]资本结构简单、折旧政策稳定，PE更能反映股东视角的回报预期"

For loss-making or cyclical companies, see the precision downgrade rules above. If no metric applies cleanly, say so.

### Common failure patterns

- Presenting a target price without stating the multiple or methodology
- Using "保守区间" or "合理估值" without showing the assumptions behind the range
- Choosing comparables without explaining the selection logic
- Stating a PE range without explaining why that range is appropriate for this company's growth/risk profile

## Common failure patterns

### Using TTM PE for cyclical stocks
A cyclical company at peak earnings will show a low PE that suggests "cheapness." This is misleading if earnings are about to mean-revert.

### Forcing PE on loss-making companies
Presenting a "negative PE" or ignoring the loss-making status to maintain a PE-based framework is a methodology failure.

### Treating SOTP as a precision tool without segment data
If segment-level financials are unavailable or unreliable, SOTP creates false precision. The result looks analytical but is assumption-driven.

### Presenting forward metrics as reported facts
`The stock trades at 12x forward PE` is acceptable. `The stock has a PE of 12` when the 12x is forward-based is misleading.

### Conflating snapshot with thesis
`The stock is cheap because it trades at 10x PE` is not a valuation thesis. It is a snapshot with an unsupported conclusion. A proper thesis would explain why 10x is cheap relative to what benchmark and why.

## Relationship to other discipline files

- `references/finance-date-discipline.md` covers time-layer separation and source-type labeling for financial numbers. This file focuses on methodology selection and precision discipline.
- `references/analyst-consensus-handling.md` covers how to handle consensus estimates and target prices from third parties.
- `references/reporting-period-handling.md` covers reporting-period definitions and TTM/LTM/NTM conventions.
