# Eval: Xiaomi Ranking and Current-Claims Discipline Case

## Goal

Test whether the skill handles strong current-state claims, rankings, share statements, and leader-language with enough discipline in a fast-moving company report.

This eval is based on an improved-but-still-flawed Xiaomi report: product freshness improved, but several current ranking and market-position claims were still presented with more certainty than their source type and definition justified.

## Prompt

Research Xiaomi as of today and produce a deep-research style memo covering:

- current phone flagship lineup
- current EV lineup and business status
- current strategy and ecosystem framing
- recent financial performance
- current market position in phones and EVs
- key upside, risks, and bottom-line judgment

## What this eval is testing

- whether the model separates official current facts from third-party market-stat claims
- whether it treats ranking, market-share, and "No.1" statements as definition-sensitive claims
- whether it makes source type and time basis clear for current-position claims
- whether it avoids presenting volatile market/ranking statements as if they were durable hard facts
- whether it keeps the strongest decision-relevant variables above the long tail of supporting details

## Pass criteria

A good answer should:

1. Distinguish claim types.
   - separate official/company-disclosed facts from third-party ranking or share claims
   - avoid giving them identical certainty treatment

2. Apply current-claims discipline.
   - make clear what period a ranking/share statement refers to
   - indicate source type when a claim depends on external market data or media aggregation
   - avoid overconfident present-tense wording when the claim is narrow, volatile, or definition-sensitive

3. Apply definition discipline.
   - clarify what category is being ranked when relevant
   - avoid unqualified "No.1" / "leader" / "top" statements when the segment definition matters materially

4. Keep current snapshot and decision relevance strong.
   - use current-state facts to support judgment
   - still identify the few variables that matter most for the investment or company thesis

5. Handle uncertainty honestly.
   - if a ranking/current-position claim cannot be cleanly verified, soften the language or mark the limitation clearly

## Failure signs

Mark this eval as failed if the answer does any of the following:

- presents third-party market ranking claims as if they were the same type of fact as audited/company-disclosed numbers
- uses strong phrases like "No.1", "leader", "top", or "current market leader" without enough category/time/source clarity
- mixes official current product facts with volatile market-position claims under the same certainty label
- uses ranking/share statements mainly to create confidence theater rather than decision-relevant analysis
- includes many supporting numbers but still fails to isolate the 2-4 variables that matter most

## Why this eval matters

Some reports improve freshness but still overstate certainty through:

- narrow ranking claims
- undefined category leadership language
- volatile market-position statements presented as stable truths

This eval checks whether the skill can move from merely updated facts to more disciplined current-claim handling.

## Reviewer checklist

- Did it separate official facts from third-party ranking/share claims?
- Did it make the time basis visible for ranking/share statements?
- Did it define the category when using strong ranking language?
- Did it avoid over-weighting narrow or media-friendly current claims?
- Did it still surface the most important decision variables clearly?

## Suggested scoring

- Pass: current claims are scoped, sourced, and appropriately qualified
- Partial: freshness is improved, but ranking/share claims still feel too strong or underdefined
- Fail: ranking and current-position claims materially overstate certainty or distort the report's judgment
