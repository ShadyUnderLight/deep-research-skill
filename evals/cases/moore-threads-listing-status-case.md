# Eval: Moore Threads Listing-Status Discipline Case

## Goal

Test whether the skill correctly handles a company's current capital-markets status and avoids freezing the report at an earlier IPO-process stage.

This eval is based on a real failure mode: a Moore Threads report relied on IPO-filing / prospectus framing and Pre-IPO language in a way that may have ignored or failed to verify the company's actual current listing status.

## Prompt

Research Moore Threads as of today and produce a deep-research style memo covering:

- company status and current identity
- capital-markets status
- current product/platform positioning
- financial and funding context
- competitive position and investment relevance

## What this eval is testing

- whether the model verifies the company's current listing / IPO-process state before using older financing or filing language
- whether it distinguishes filing, acceptance, review, registration, issuance, listing, and trading status
- whether it avoids stale `Pre-IPO` framing if the company state has advanced
- whether it makes the time basis explicit when citing financing and listing-stage facts

## Pass criteria

A good answer should:

1. Verify current capital-markets status first.
   - determine whether the company is private, filed, accepted, under review, registered, issued, listed, or trading
   - avoid assuming the status from an older filing document alone

2. Separate status layers clearly.
   - distinguish company identity from listing status
   - distinguish historical IPO milestones from current state
   - distinguish financing-stage language from public-market status

3. Apply time discipline.
   - mark older prospectus / filing facts as historical milestones when appropriate
   - not use `Pre-IPO` as current framing if newer status supersedes it

4. Keep market-language aligned with status.
   - if the company is listed, include appropriate trading/status context
   - if still in process, say which step is current and what remains incomplete

5. Handle uncertainty honestly.
   - if the current status cannot be confirmed cleanly, say so and avoid overclaiming

## Failure signs

Mark this eval as failed if the answer does any of the following:

- treats an IPO filing or prospectus as enough to establish current listing status
- uses `Pre-IPO` framing as if it were still current without checking for later changes
- confuses `filed`, `accepted`, `approved`, `registered`, `issued`, and `listed`
- omits trading status / ticker-style context when claiming the company is listed
- presents capital-markets status with strong certainty despite weak time discipline

## Why this eval matters

Corporate status is a load-bearing current-state fact.

If the model gets this wrong, it can distort:

- valuation framing
- disclosure expectations
- financing context
- investment logic
- the interpretation of company milestones

A report can look detailed and still fail if it anchors the company to the wrong capital-markets state.

## Reviewer checklist

- Did it verify current listing/IPO status before deeper analysis?
- Did it clearly separate historical milestones from current state?
- Did it avoid stale `Pre-IPO` language unless still actually current?
- Did it distinguish IPO-process steps precisely?
- Did it calibrate certainty correctly if the status was hard to verify?

## Suggested scoring

- Pass: company status is current, layered, and precisely stated
- Partial: some status distinctions are present, but old filing-stage framing still leaks into the current picture
- Fail: the report materially misstates or blurs the company's current capital-markets status
