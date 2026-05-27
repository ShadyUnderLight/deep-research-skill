# Eval: Consensus Target Price and Forward PE Misuse Case

## Goal

Test whether the skill handles consensus data and forward valuation metrics with proper discipline, specifically:

1. **Consensus target price treated as fair value** — whether the model presents analyst target prices as if they were intrinsic value or "correct" pricing.
2. **Forward PE presented as reported fact** — whether the model uses forward PE without labeling it as estimate-based.
3. **Stale consensus after earnings** — whether the model uses pre-earnings consensus data without noting it may be stale.

All three are common in listed-company research. A report that treats consensus target prices as fair value or forward PE as fact misleads the reader about certainty.

## Prompt (fixed scenario)

You are conducting research as of February 10, 2026. Research Tesla Inc. (TSLA) as a listed company and produce a deep-research style memo covering:

- current financial performance (latest reported period: Q4 2025, released January 28, 2026)
- current trading status and valuation context
- analyst consensus view on target price and earnings estimates
- investment thesis and key risks
- bottom line

Use the following scenario facts for evaluating the skill's handling (these are hypothetical bounds for grading, not test-day data):
- Tesla reported Q4 2025 earnings on January 28, 2026
- Before earnings, Bloomberg consensus FY2025E EPS was $2.50 (24 analysts, range $2.20–$2.80)
- After earnings, some analysts have updated but broad consensus has not fully refreshed yet
- Consensus target price range is $180–$400, median $250

## What this eval is testing

### Failure Mode 1: Consensus target price as fair value

The report says something like:
- `The consensus target price is $250, suggesting 30% upside from the current price of $190`
- `Analysts believe the stock is worth $250`
- `Based on the consensus target, the stock appears undervalued`

This treats analyst opinions as if they were a valuation conclusion. Consensus target prices are aggregated third-party views, not intrinsic value assessments.

**Pass behavior:** The report presents the consensus target price with source, date, coverage count, and notes that it reflects analyst methodology rather than market-determined fair value.

### Failure Mode 2: Forward PE as reported fact

The report says something like:
- `Tesla trades at 45x PE`
- `The PE ratio is 45x, which is high relative to peers`

But the 45x is actually forward PE based on consensus estimates, not TTM PE from reported earnings.

**Pass behavior:** The report clearly labels forward PE as `forward PE (based on consensus estimates)` or `45x FY2026E PE`, distinguishing it from TTM PE.

### Failure Mode 3: Stale consensus after earnings

Tesla reported Q4 2025 earnings on January 28, 2026. The research report is dated February 2026 but uses consensus EPS estimates compiled in January 2026 (before earnings).

The report does not note that the consensus data may not reflect Q4 results or updated guidance.

**Pass behavior:** The report either uses post-earnings consensus or explicitly notes that the consensus data predates the latest earnings release.

## Pass Criteria

A good answer should:

1. Present consensus target prices with proper attribution
   - source platform (Bloomberg, FactSet, etc.)
   - compilation date
   - number of analysts
   - range if available
   - explicit note that target prices are analyst opinions, not fair value

2. Distinguish forward PE from TTM PE
   - label forward PE as estimate-based
   - state which fiscal year or period the forward estimate uses
   - do not present forward PE as `the PE ratio`

3. Handle consensus timing
   - check whether consensus data predates the latest earnings release
   - if stale, note the timing gap
   - prefer more current sources when available

## Failure Signs

Mark this eval as failed if the answer does any of the following:

### Consensus target price failures
- presents consensus target price without source, date, or analyst count
- equates consensus target price with fair value or intrinsic value; it is acceptable to report analyst-implied upside if clearly attributed
- uses `undervalued` based solely on consensus target vs current price without attribution
- does not note that target prices are analyst opinions

### Forward PE failures
- writes `PE ratio` or `trades at Xx PE` when the figure is forward PE
- does not label forward PE as estimate-based
- uses forward PE in valuation comparisons without noting it is not a reported metric

### Stale consensus failures
- uses consensus data compiled before the latest earnings release without noting the timing
- does not check whether consensus has been updated post-earnings
- uses pre-earnings consensus as the basis for post-earnings financial claims

## Why This Eval Matters

### Consensus target price
Readers often interpret consensus target prices as "where the stock should be." This conflates analyst methodology with market truth. A disciplined report should present target prices as one input, not a valuation conclusion.

### Forward PE
Forward PE is widely used but often unlabeled. Readers may assume it is a reported metric. Making the estimate basis explicit is a basic discipline for investment-style research.

### Stale consensus
After earnings, consensus data may lag. Using stale consensus without noting it creates a false impression of current market expectations.

## Reviewer Checklist

- Did it present consensus target price with source, date, and analyst count?
- Did it note that target prices are analyst opinions, not fair value?
- Did it distinguish forward PE from TTM PE?
- Did it label forward PE as estimate-based?
- Did it check whether consensus data predates the latest earnings release?
- If consensus was stale, did it note the timing gap?

## Suggested Scoring

- **Pass**: all three areas (target price, forward PE, stale consensus) handled with proper discipline
- **Partial**: two of three areas handled correctly, one has minor gaps
- **Fail**: any area presents consensus data as fact without proper attribution or timing awareness
