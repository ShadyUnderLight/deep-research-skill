# Eval: Apple Product Freshness and Valuation Snapshot Case

## Goal

Test two separate but related failure modes in a single Apple deep-research report:

1. **Product current-state freshness**: whether the model uses stale product generations as if they were current flagships when newer products already exist.
2. **Valuation snapshot completeness**: whether the model omits current-market valuation metrics (price, market cap, PE, PB, PS, 52-week range) when studying a listed company.

Both are serious in a listed-company research context. A report on Apple without current valuation data is incomplete for investment analysis. A report listing iPhone 16 as current when iPhone 17 has shipped is factually wrong.

## Prompt

Research Apple Inc. as of today and produce a deep-research style memo covering:

- current flagship product lineup (iPhone, Mac, iPad, Apple Watch, etc.)
- current financial performance (most recent fiscal year)
- current trading status and valuation context
- competitive position
- investment thesis and key risks
- bottom line

## What this eval is testing

### Failure Mode 1: Product Current-State

The Apple report listed iPhone 16 series, M4 chips, and Apple Watch Series 10 as current flagships when:

- iPhone 17 series has already been released and is the current flagship
- M5 chips have shipped in current Mac models
- Apple Watch Series 11 / Ultra 3 are the current models

This is a direct freshness failure. The model used stale product knowledge instead of verifying what is actually current.

### Failure Mode 2: Valuation Snapshot Missing

For a listed-company research report, omitting current valuation metrics is a significant gap. Investors need to know:

- current stock price
- market capitalization
- PE ratio (TTM or forward)
- PB ratio
- PS ratio
- 52-week high/low range

The report had financial data but no current trading/valuation snapshot.

## Pass Criteria

A good answer should:

1. Verify the current product lineup before writing product sections.
   - confirm which iPhone generation is currently shipping
   - confirm which Mac chip generation is current
   - confirm which Apple Watch generation is current
   - do not use last generation as if it is still current

2. For a listed company, include a current valuation snapshot.
   - at minimum: current approximate stock price and market cap
   - if valuation ratios are included, specify the basis (TTM / forward / fiscal year)
   - specify the date of the snapshot
   - note the source

3. Apply consistent freshness discipline to all fast-moving product categories.
   - consumer electronics: phone, PC, tablet, wearable
   - chips: new generations ship frequently; verify before stating
   - product lifecycle stage: current shipping vs. previous generation vs. announced but not yet shipping

4. When product generations are ambiguous, apply appropriate caveats.
   - if the exact current lineup is uncertain, say so
   - if a new product was just announced but not yet widely available, note the stage

## Failure Signs

Mark this eval as failed if the answer does any of the following:

### Product freshness failures
- lists iPhone 16 series as current flagship when iPhone 17 series has shipped
- uses M4 as the current Mac chip when M5 has shipped
- lists Apple Watch Series 10 as current when Series 11 / Ultra 3 have been announced or released
- any major product category is materially stale without a caveat

### Valuation completeness failures
- no current stock price or market cap for a listed company
- no valuation ratios when these are normally available and relevant
- valuation data is present but has no date, source, or basis specified
- the report is framed as investment-relevant but omits the most basic current-market context

## Why This Eval Matters

### Product freshness
Apple product generations are some of the most frequently updated in consumer electronics. A research report that anchors on the wrong generation is not just slightly stale — it misrepresents what the company is currently selling and at what price points.

### Valuation completeness
For any listed-company investment memo, current valuation is a fundamental data point. A report that covers historical financials but omits current market context is incomplete by a serious margin for investment-decision purposes.

Both are covered by existing references (current-state verification, finance-date discipline) but this eval tests whether they are actually applied together in a real report run.

## Reviewer Checklist

- Did it verify the current iPhone generation before writing iPhone sections?
- Did it verify the current Mac chip generation?
- Did it verify the current Apple Watch generation?
- Did it include current stock price and market cap?
- Did it include valuation ratios with date and basis specified?
- If any product data was stale, did it apply appropriate caveats?

## Suggested Scoring

- Pass: both current product lineup and current valuation snapshot are present and correctly dated
- Partial: product lineup is mostly current but some categories are stale; OR valuation data is present but incomplete or undated
- Fail: multiple major product categories are materially stale AND/OR valuation snapshot is entirely absent for a listed company
