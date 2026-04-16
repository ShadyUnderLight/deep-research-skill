# Eval: China Shenhua Listed-Company Judgment and Traceability Case

## Goal

Test whether a listed-company deep-research report can avoid looking polished while still failing the real investment-style burden.

This eval is based on a real user-provided report about **China Shenhua (601088 / 01088.HK)** dated **2026-04-16**.

The report looked structured and evidence-aware. It used confidence-style labels such as:
- confirmed facts
- inference
- open uncertainty

But the report still exposed a more specific failure family:
- the opening behaved more like a company-profile snapshot than a judgment memo
- several load-bearing claims sounded stronger than their visible sourcing justified
- key thesis-supporting claims were not auditable at the body-claim level
- front-page methodology / evidence labeling occupied too much attention relative to the actual thesis, risks, and unknowns
- corporate-action upside language compressed confirmed transaction facts, likely operating implications, and open uncertainty into one smooth narrative

## Prompt

Use deep-research to produce a Chinese listed-company / investment-style report on China Shenhua.

The report should cover at least:
- business and products
- industry position
- customers and use cases
- key competitors
- the last two years of operating and financial signals
- bullish logic
- bearish logic
- main opportunities and risks over the next 1-3 years

Requirements:
- use multiple sources and cross-check important claims
- clearly distinguish confirmed facts, likely inference, and open uncertainty
- if PDF is produced, keep the front page readable and judgment-first
- make load-bearing claims auditable in the body, not only by listing sources at the end
- when discussing asset injection, financing, or restructuring, separate:
  - confirmed transaction facts
  - likely operating / financial implications
  - open uncertainty about timing, realization, or synergy quality

## What this eval is testing

### Failure Mode 1: company overview shape substitutes for judgment memo shape

The report may look rich and organized, but the opening still behaves like:
- a company overview
- a background summary
- a cleaned-up profile card

instead of a current judgment memo.

The opening should make visible:
- the current thesis
- the strongest confirmed support
- the key unresolved variable
- the main risks and unknowns
- the time anchors supporting the judgment

If the first page can be skimmed without revealing the real current thesis, the route execution is still too weak.

### Failure Mode 2: confidence-label theater without claim-level auditability

The report may use labels such as confirmed / inference / uncertainty, yet still leave important claims unauditable.

Typical examples include strong-sounding claims about:
- transport-cost advantage
- volatility sensitivity vs peers
- asset-injection growth impact
- dividend superiority
- future coal-price center or scenario range

These may be directionally plausible, but the report fails if the reader cannot tell:
- which source supports the exact claim
- whether the claim is directly stated vs inferred
- whether the wording strength was downgraded when support was indirect

### Failure Mode 3: front-page process visibility displaces judgment visibility

A report can technically include an evidence legend and still fail the front page.

This eval checks whether:
- the thesis is easier to spot than the methodology note
- executive bullets carry judgment rather than metadata
- key risks and key unknowns are visually easier to find than process framing

The evidence legend should stay compact and should not dominate the reader's first scan.

### Failure Mode 4: corporate-action compression

For China Shenhua-style reports, major corporate actions such as:
- asset injection
- financing completion
- restructuring
- production-capacity expansion implications

must not be compressed into one smooth bullish line.

The report should separate:
1. what is confirmed transaction fact
2. what is likely operating or financial implication
3. what remains unresolved about realization, timing, or synergy quality

If these are blended together, the report overstates certainty while sounding disciplined.

### Failure Mode 5: support / weakening / unresolved split is not visible

A listed-company report should not only present positive logic plus a generic risk list.

It should visibly separate:
- what currently supports the thesis
- what currently weakens it
- what remains unresolved and therefore limits confidence, timing precision, valuation precision, or recommendation strength

If the report has a bullish mood with decorative caveats, mark this eval as failed.

## Pass criteria

A good answer should:

1. start with a judgment-first opening
   - thesis first
   - latest time anchors visible early
   - risks and unknowns scannable on the front page

2. make load-bearing claims auditable in the body
   - not only in a bibliography
   - with visible source role and scope when needed

3. separate evidence weight honestly
   - confirmed facts vs likely inference vs open uncertainty
   - direct evidence vs indirect evidence when the claim matters to the bottom line

4. keep strong wording proportional to support
   - if support is weaker than the wording strength, downgrade the wording visibly

5. split major corporate actions into fact / implication / uncertainty
   - do not let asset-injection or financing language function as hidden certainty inflation

6. keep the listed-company route visible
   - the report should read like an investment-style judgment memo, not a polished company brief

## Failure signs

Mark this eval as failed if the answer does any of the following:

- the front page is dominated by methodology, label explanation, or metadata while the thesis remains hard to see
- the opening reads like a business summary instead of a current judgment memo
- key bullish claims sound precise or comparative but are not claim-traceable in the body
- asset injection / financing / restructuring facts are blended directly into growth or valuation upside without an uncertainty split
- competition appears mainly as a peer directory rather than thesis pressure
- the report uses confidence labels but still leaves the main bottom line weakly auditable
- risks exist but do not visibly weaken or narrow the final judgment

## Why this eval matters

This case catches a failure family that can survive even after:
- freshness hardening
- source-list additions
- visible evidence labels

The report can still fail because:
- route execution is too background-first
- traceability remains bibliography-level rather than claim-level
- front-page judgment visibility is too weak
- positive corporate-action storytelling is not separated from confirmed facts and open uncertainty

If the skill cannot pass this eval, it remains vulnerable to reports that look disciplined but still overstate the reliability of their own conclusion.

## Likely intervention targets

This case should push changes in:
- `ROUTING-MATRIX.md` listed-company visible artifact contract and hard fails
- `checklists/listed-company-report.md`
- `checklists/final-audit.md`
- `references/report-template.md`
- `references/decision-report-template.md`

## Reviewer checklist

- Can a reader identify the thesis, key risks, and key unknowns within the first page scan?
- Does the report visibly lock latest annual / latest quarter / latest market snapshot before broad narrative expansion?
- Are load-bearing claims auditable in the body rather than only by a source list at the end?
- Are strong comparative or forecast claims visibly scoped, sourced, or downgraded?
- Are corporate actions split into confirmed facts / likely implications / open uncertainty?
- Does the report visibly show what supports the thesis, what weakens it, and what remains unresolved?
- If the background section were shortened by 30-40%, would the core judgment remain intact?

## Suggested scoring

- Pass: judgment-first, claim-auditable, route-visible, and uncertainty-constraining
- Partial: structured and sourced, but still too background-first or too bibliography-level in traceability
- Fail: polished report shape with weak judgment visibility or inflated certainty behind key claims
