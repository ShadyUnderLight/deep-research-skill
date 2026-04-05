# Eval: Xiaomi Freshness and Date-Discipline Case

## Goal

Test whether the skill verifies current-state facts before broader analysis, especially for a fast-moving company/topic that mixes products, vehicles, strategy, finance, and market data.

This eval is based on a real failure mode: the report looked structured and credible, but mixed stale product-line facts with present-tense analysis.

## Prompt

Research Xiaomi as of today and produce a deep-research style memo covering:

- current phone flagship lineup
- current EV lineup
- current company strategy and ecosystem framing
- latest verifiable financial state
- current valuation context
- key upside, risks, and bottom-line judgment

## What this eval is testing

- whether the model performs a current snapshot before analysis
- whether it verifies current phone generation and lineup from primary sources
- whether it distinguishes historical facts, current-state facts, and forward-looking judgments
- whether it handles financial and valuation date discipline correctly
- whether it avoids using stale but familiar Xiaomi knowledge as if it were current

## Pass criteria

A good answer should:

1. Verify the current snapshot first.
   - make clear what Xiaomi's current flagship phone lineup is
   - make clear what current EV lineup is visible from official/current sources
   - make clear what Xiaomi's current ecosystem/strategy framing is

2. Show source freshness discipline.
   - prefer official current pages, current announcements, or current primary financial disclosures
   - avoid relying mainly on historical summaries or generic review pages
   - make dates visible when they matter

3. Separate time layers clearly.
   - historical reported financials
   - current-state facts
   - forward-looking goals, estimates, or management targets

4. Apply finance date discipline.
   - indicate whether a number comes from annual report, interim report, earnings release, TTM market data, market quote, analyst estimate, or inference
   - avoid presenting estimates or targets as fully confirmed facts

5. Be honest about uncertainty.
   - if the latest product generation, latest financial release, or current valuation basis cannot be verified clearly, say so
   - reduce confidence rather than filling gaps with likely-but-stale knowledge

## Failure signs

Mark this eval as failed if the answer does any of the following:

- states an older Xiaomi flagship generation as the current flagship without clear current verification
- mixes historical and current product states without date separation
- presents a 2025/2026 financial figure as confirmed fact without clarifying whether it is reported, estimated, or inferred
- gives "current valuation" numbers without a visible time basis or source type
- writes a polished narrative that appears current but is actually built from stale facts
- skips current snapshot verification and jumps straight into strategic analysis

## Why this eval matters

This is a high-value regression test because it catches a common deep-research failure mode:

- the structure looks strong
- the prose sounds credible
- the dates in the title look current
- but the factual layer is not actually synchronized to the current state

If the skill cannot pass this eval, it is not yet reliable for fast-moving company research.

## Reviewer checklist

Use this quick checklist after a run:

- Did it verify Xiaomi's current flagship lineup from current/official sources?
- Did it distinguish current EV lineup from future targets?
- Did it separate historical financials from current market/valuation data?
- Did it identify forward-looking claims as forward-looking?
- Did it make uncertainty visible where current-state verification was incomplete?

## Suggested scoring

- Pass: current-state and date discipline are clear and reliable
- Partial: some current-state checks are visible, but financial/date layering is still muddy
- Fail: stale facts or unclear time layering materially weaken the report
