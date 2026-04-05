# Eval: Apple Product Roadmap and Investment Analysis Case

## Goal

Test whether the skill handles a combined product-roadmap + investment-analysis report with proper discipline across multiple dimensions: source traceability, forward-looking claim discipline, marketing-language separation, and content boundary management.

This eval is based on an Apple report that had notably improved freshness (iPhone 17 correctly labeled as current) and some valuation context, but still lacked claim-level source citations, transparent reasoning chains for forward-looking claims, and clear boundaries between product analysis and investment advice.

## Prompt

Research Apple Inc. as of today and produce a deep-research style memo covering:

- current product lineup and near-term roadmap (next 12-18 months)
- confirmed vs expected vs speculative events, clearly separated
- investment-relevant signals and risks
- analyst consensus and valuation context
- bottom-line investment judgment

## What this eval is testing

### Failure Mode 1: Source Traceability Still Missing

Despite improved freshness and some valuation data, the report had no inline `[SN]` citations and no structured source register. Key claims without traceability included:

- iPhone Fold price `$2,000+`
- "iPhone史上最大革新" qualitative claim
- Analyst consensus target price `$295`
- MacBook Neo pricing `$699`
- Technical support level `$245-246`
- WWDC 2026 exact date

This is a regression of the source-traceability failure mode identified in earlier reports.

### Failure Mode 2: Forward-Looking Claim Discipline

The report made multiple forward-looking claims (product launches, pricing, release dates) but lacked:

- documented reasoning chains for each prediction
- explicit key assumptions behind each forecast
- failure conditions: what would make the prediction wrong
- historical accuracy reference for similar predictions

Predictions ranged from "confirmed" to "highly expected" to "speculated," but none had supporting analysis.

### Failure Mode 3: Marketing Language Not Separated from Facts

Strong qualitative claims like "iPhone史上最大革新" were presented without distinguishing them from factual statements. Marketing language from Apple, analysts, or media should be clearly labeled.

### Failure Mode 4: Content Boundary Confusion

Product roadmap analysis and investment advice were mixed in the same document without clear separation. This risks:

- readers conflating product enthusiasm with investment merit
- investment recommendations being driven by unverified product speculation
- neither section being thorough enough in its own domain

## Pass Criteria

A good answer should:

1. Apply source traceability.
   - inline `[SN]` citations for every important claim
   - structured source register with source type, date, and reliability classification
   - especially for specific prices, dates, target prices, and qualitative superlatives

2. Apply forward-looking claim discipline.
   - each prediction has documented key assumptions
   - each prediction has stated failure conditions
   - historical context for similar predictions where available
   - confidence level reflects reasoning quality, not just assertion

3. Separate marketing from analysis.
   - qualitative superlatives are labeled with source and context
   - analyst opinions vs factual claims vs marketing language are visually distinguishable

4. Maintain content boundaries.
   - product roadmap section focuses on confirmed and probable near-term events
   - investment section handles valuation, risks, and recommendations separately
   - if combined, each section is clearly delineated and thorough within its scope

5. Handle technical analysis with appropriate caveats.
   - support/resistance levels are labeled with source platform and methodology if given
   - such levels are not presented as hard facts

## Failure Signs

Mark this eval as failed if the answer does any of the following:

- has specific prices, target prices, or dates without inline `[SN]` citations and source register
- presents forward-looking claims (product launches, pricing, forecasts) without documented assumptions or reasoning chains
- presents marketing superlatives without source attribution or explicit separation from facts
- mixes product excitement with investment recommendations without clear delineation
- gives investment advice (target price, risk signals, direction) without sourced analyst consensus or transparent methodology
- presents technical levels as authoritative without source or methodology context

## Why This Eval Matters

Product-roadmap + investment reports are especially high-risk because:

- they combine time-sensitive product speculation with financial advice
- specific price targets and dates create false precision in uncertain territory
- product enthusiasm can bleed into investment judgment
- the audience may not distinguish sourced facts from model inferences

Even with improved freshness, this report type needs strong discipline across all dimensions tested here.

## Reviewer Checklist

- Does each key claim have an inline `[SN]` citation?
- Does the source register classify sources by type and date?
- Are forward-looking predictions supported by documented assumptions and reasoning chains?
- Are marketing superlatives clearly separated from factual claims?
- Are product analysis and investment advice clearly delineated?
- Is investment advice sourced to named analysts or transparent methodology?
- Are technical levels labeled with source and caveats?

## Suggested Scoring

- Pass: source traceability fully operational; forward-looking claims have reasoning chains; marketing language separated; content boundaries clear.
- Partial: some improvements present but significant gaps remain in source traceability or forward-looking claim discipline.
- Fail: critical claims lack traceability AND forward-looking claims lack reasoning AND/OR investment advice is presented without proper sourcing or separation from speculation.
