# Eval: Reporting Period and TTM Confusion Case

## Goal

Test whether the skill handles reporting-period definitions and TTM/LTM calculations with proper discipline, specifically:

1. **TTM confused with latest fiscal year** — whether the model uses TTM figures without noting they are derived, or confuses TTM with the latest annual report.
2. **Preliminary treated as audited** — whether the model uses earnings-release figures without labeling them as preliminary.
3. **Restated figures ignored** — whether the model uses original figures when restated figures are available.

All three can distort financial analysis. A report that mixes TTM and FY, or uses preliminary data as if it were audited, may draw conclusions from misaligned periods.

## Prompt

Research BYD Company Limited (1211.HK / 002594.SZ) as a listed company and produce a deep-research style memo covering:

- current financial performance (most recent reported period)
- current trading status and valuation context
- investment thesis and key risks
- bottom line

## What this eval is testing

### Failure Mode 1: TTM confused with latest fiscal year

BYD's fiscal year ends December 31. The research report is dated March 2026, after Q4 2025 earnings release but before Q1 2026 results.

The report writes:
- `2025 revenue was RMB 600 billion` (using the FY2025 figure from the annual report)
- `The company trades at 25x PE` (but this is TTM PE using the last four quarters, not FY2025 PE)

If the report uses FY2025 revenue but TTM PE without distinguishing the periods, the reader cannot tell which periods the numbers belong to.

**Pass behavior:** The report clearly labels `FY2025 revenue (from annual report)` and `TTM PE (based on Q2 2025 – Q1 2026 earnings, or as reported by Bloomberg as of [date])`, or explicitly states that TTM and FY figures use different period definitions.

### Failure Mode 2: Preliminary treated as audited

BYD releases a preliminary earnings announcement for Q4 2025 in late January 2026, with the full annual report expected in March 2026.

The report uses Q4 2025 / FY2025 figures from the preliminary announcement but does not label them as preliminary.

**Pass behavior:** The report labels the figures as `preliminary, per earnings release dated [date]` and notes that the full annual report may contain revisions.

### Failure Mode 3: Restated figures ignored

BYD restated FY2024 figures in the FY2025 annual report (e.g., due to accounting policy change or correction).

The report uses the original FY2024 figures instead of the restated figures.

**Pass behavior:** The report uses the restated FY2024 figures from the FY2025 annual report and notes that they are restated.

## Pass Criteria

A good answer should:

1. Distinguish TTM from fiscal year
   - label TTM figures as derived from the most recent four quarters
   - do not present TTM figures as if they were reported annual figures
   - state the construction method or source platform

2. Label preliminary data
   - mark earnings-release figures as `preliminary` or `per earnings release`
   - note that the full report may contain revisions
   - prefer the full report when available

3. Use restated figures
   - use restated figures from the latest annual report when available
   - note that the figures are restated
   - do not use original figures when restated figures exist

## Failure Signs

Mark this eval as failed if the answer does any of the following:

### TTM failures
- writes `2025 revenue` and `PE ratio` without distinguishing FY from TTM
- uses `the company trades at Xx PE` when the PE figure is TTM-based without labeling
- does not explain how TTM figures are constructed
- confuses TTM with the latest fiscal year in valuation metrics

### Preliminary failures
- uses earnings-release figures without labeling them as preliminary
- does not note that the full annual report may revise the figures
- treats preliminary data as if it were audited

### Restatement failures
- uses original FY2024 figures when restated figures are available in the FY2025 annual report
- does not check for restatements in the latest annual report
- uses outdated figures without noting the restatement

## Why This Eval Matters

### TTM vs fiscal year
TTM and fiscal year figures are different constructs. A report that uses FY2025 revenue but TTM PE without distinction creates a false impression that all numbers refer to the same period.

### Preliminary vs audited
Earnings releases are preliminary and may be revised. Using them as if they were audited can propagate errors, especially for companies with complex accounting.

### Restated figures
Restated figures supersede original figures. Using outdated figures when restated ones exist is a factual error that can distort trend analysis.

## Reviewer Checklist

- Did it distinguish TTM figures from fiscal year figures?
- Did it label TTM figures as derived?
- Did it label earnings-release figures as preliminary?
- Did it note that the full report may revise preliminary figures?
- Did it use restated figures when available?
- Did it note that figures are restated?

## Suggested Scoring

- **Pass**: all three areas (TTM, preliminary, restatement) handled with proper discipline
- **Partial**: two of three areas handled correctly, one has minor gaps
- **Fail**: any area presents figures without proper period labeling, or uses outdated data when current data is available
