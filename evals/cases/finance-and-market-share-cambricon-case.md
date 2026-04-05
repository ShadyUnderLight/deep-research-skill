# Eval: Cambricon Finance and Market-Share Discipline Case

## Goal

Test whether the skill handles company/investment-style numeric claims with enough discipline, especially when a report mixes product analysis, financial performance, valuation, market sizing, and estimated market share.

This eval is based on a real failure mode: the report looked analytical and well-structured, but some financial, valuation, and market-share claims were presented with more precision and certainty than the underlying evidence justified.

## Prompt

Research Cambricon as of today and produce a deep-research style memo covering:

- current company/product positioning
- current and recent product lines relevant to AI chips
- latest verifiable financial state
- current valuation context
- China AI-chip market context
- Cambricon's likely competitive position and share
- key upside, risks, and bottom-line judgment

## What this eval is testing

- whether the model separates reported financials, current market snapshot, and forward-looking numbers
- whether it handles market-sizing and market-share estimates conservatively
- whether it avoids presenting heuristic share ranges as if they were audited facts
- whether it distinguishes current products from historical representative products
- whether it avoids pseudo-precision in tables and summaries

## Pass criteria

A good answer should:

1. Apply finance/date discipline.
   - identify whether important numbers come from annual report, interim report, earnings release, market-data snapshot, analyst estimate, or inference
   - avoid presenting estimated or inferred numbers as fully confirmed facts
   - make the time basis visible for valuation metrics

2. Apply market-sizing/share discipline.
   - define the market before using market-size data
   - explain whether company revenue can actually map to that market definition
   - use market-share estimates only as rough directional judgments when auditable data is unavailable
   - keep caveats visible

3. Avoid pseudo-precision.
   - do not present thinly supported percentages or narrow numeric ranges as if they were established facts
   - prefer directional language when evidence is weak

4. Handle product-line time layering.
   - separate current promoted/current relevant products from historical representative products or older generations

5. Make uncertainty explicit.
   - call out where data is estimated, inferred, poorly auditable, or dependent on rough assumptions

## Failure signs

Mark this eval as failed if the answer does any of the following:

- presents yearly financial figures as confirmed facts without clarifying reporting/disclosure status
- gives current valuation ratios without visible time basis or metric basis
- uses market-size data without defining the market clearly enough to support share inference
- presents market-share ranges with strong visual precision but weak evidentiary basis
- blends current products and historical product generations without time labeling
- produces a polished investment narrative that hides weak numeric foundations

## Why this eval matters

This catches a different failure mode from simple freshness problems.

A report can be current enough on dates and still be weak because:

- it mixes reported numbers, inferred numbers, and live market data
- it treats rough industry heuristics like hard statistics
- it creates false confidence through detailed-looking numeric tables

If the skill cannot pass this eval, it is not yet reliable for serious company, sector, or investment-style research.

## Reviewer checklist

- Did it label the source type and time basis of key financial numbers?
- Did it distinguish current valuation snapshot from historical reported data?
- Did it define the market before inferring market share?
- Did it avoid overconfident share percentages or narrow ranges?
- Did it keep current vs historical product lines separate?

## Suggested scoring

- Pass: numeric claims are disciplined, scoped, and clearly layered by time/source type
- Partial: some caveats exist, but pseudo-precision or market-share overreach remains
- Fail: the report materially overstates certainty in finance, valuation, or market-share claims
