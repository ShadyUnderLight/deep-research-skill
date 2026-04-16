# Eval: CNOOC Judgment Shape Improved but Freshness Still Leaked Case

## Goal

Test whether a listed-company / investment-style report can visibly improve its judgment-memo shape and still fail because the freshness hard gate remains unstable.

This eval is based on a real user-provided report about **CNOOC / China National Offshore Oil Corporation (600938.SH / 00883.HK)** dated **2026-04-16**.

The report is valuable because it is **not** a simple repeat of older failure patterns.

Unlike weaker earlier cases, this report already showed meaningful progress:
- research-anchor block present
- one-sentence thesis present
- support / weakening / unresolved structure present
- key risks and key unknowns visible early
- output shape much closer to a judgment memo than to a company overview

But despite that progress, the report still leaked on a critical front-end burden:
- the research-anchor block listed **Q1 2025** as the "latest quarterly period" in a report dated **2026-04-16**

That means the report improved at the judgment-shape layer while still failing at the freshness hard-gate layer.

This makes the case especially useful because it captures a more advanced failure mode:

> **the report is no longer broadly route-wrong, but a stale anchor still breaks memo integrity after route execution has already improved**

---

## Prompt context

The underlying task was to use deep-research in a listed-company / investment-style judgment-memo style and produce a short Chinese memo-shaped report rather than a broad company overview.

The intended validation burden included:
- research-anchor block
- one-sentence thesis
- strongest support
- strongest weakening evidence
- key unresolved variable
- what would change the conclusion
- body-level auditability for thesis-bearing claims
- early support / weakening / unresolved visibility

This eval is therefore not testing whether the route was selected at all.
It is testing whether a partly successful route execution can still be invalidated by stale current-state control.

---

## Real failure pattern

The report did several things better than older listed-company failures:
- it opened with a judgment-oriented shape
- it made support / weakening / unresolved visible early
- it identified a real load-bearing unresolved variable around FCF, capex, payout, and oil-price range
- it did not collapse entirely into a company profile

But the report still contained a critical time-anchor inconsistency:
- report date: **2026-04-16**
- latest full-year period: **FY2025**
- latest quarterly period stated: **Q1 2025**

That quarterly anchor is very likely stale or mis-timed for the stated report date.

This matters because the problem is not only factual sloppiness. It changes the memo burden itself:
- a report that looks current and judgment-oriented may still be carrying an outdated quarterly layer
- the user may trust the memo more precisely because the structure now looks more disciplined
- stale-anchor errors become more dangerous, not less, once the artifact shape becomes more convincing

---

## What this eval is testing

### Failure Mode 1: route execution improved, freshness gate still unstable

The report visibly carries more of the listed-company judgment burden than earlier weak outputs.

But the current-state gate still leaks at the research-anchor layer.

This should be treated as a distinct failure pattern from:
- generic company-overview drift
- total route miss
- broad source weakness

The route is partly right. The gate still fails.

### Failure Mode 2: stale anchor inside an otherwise improved memo shape

This case is stronger than a generic stale-data case because the stale anchor appears inside a report that already looks much closer to the desired output form.

That means the failure is no longer:
- `the report never became a judgment memo`

It is now:
- `the report became more memo-like, but the memo is still not safe to trust because the opening anchor is unstable`

### Failure Mode 3: execution-family upgrade without stability upgrade

This case checks whether repo hardening is improving only the visible artifact shape or also the underlying execution stability.

A report can improve on:
- opening structure
- triad visibility
- thesis compression
- uncertainty framing

while still failing the harder question:
- are the latest time layers truly governing the memo?

### Failure Mode 4: stronger shape can hide freshness failure better

When a report is obviously weak, stale anchors are easier to distrust.

When a report looks disciplined, the same stale anchor becomes easier for both the model and the reader to miss.

This means freshness hard-gate failures become higher priority once judgment-memo shape begins to improve.

---

## What the report handled well

The report deserves credit for visible progress in several areas:

### 1. Judgment-first opening improved

The opening contained:
- research-anchor block
- one-sentence thesis
- executive summary
- key risks
- key unknowns
- what matters most now

This is meaningfully better than a business-background-first opening.

### 2. Support / weakening / unresolved structure visibly activated

The report included:
- main evidence supporting the thesis
- main evidence weakening the thesis
- key unresolved variable

This is direct progress on the listed-company judgment-memo burden.

### 3. Unknowns were more load-bearing than in weaker past reports

The unresolved variable focused on whether free cash flow in a moderate oil-price band could simultaneously support:
- high capex
- production growth
- 45% payout ratio

That is a real judgment-limiting unknown, not decorative uncertainty.

### 4. The thesis was more calibrated than a generic positive company summary

The report did not simply frame CNOOC as a clean growth story.
It attempted to place the company as a:
- low-cost
- high-dividend
- production-growth-assisted defensive asset

with explicit oil-price and cash-flow constraints.

These strengths matter because they prove the route is no longer failing at the most obvious level.

---

## What still failed

### 1. Research-anchor integrity failed at the quarterly layer

The most important visible failure was the quarterly anchor:
- report date: 2026-04-16
- latest quarter stated: Q1 2025

For a listed-company memo, this should trigger a hard freshness re-check before synthesis continues.

### 2. Current-state control was present in form, but not stable in execution

The report showed the artifact of current-state discipline:
- a research-anchor block exists

But the content inside that block was not stable enough.

This means the problem is not only:
- missing shape

It is:
- unstable execution of an already-correct shape

### 3. Thesis-bearing claims still remained only partly auditable

Even though the report improved in structure, several high-burden claims still sounded stronger than their body-level auditability fully justified.

Examples include:
- first-tier global cost competitiveness
- A-share market pricing having already priced in `defense + repair + energy-security premium`
- oil-price sensitivity framing
- FCF stress conclusions under lower oil-price bands

These may be directionally plausible, but the case still shows that a better opening does not automatically solve thesis-bearing claim auditability.

### 4. Conclusion-constraint improved, but not all the way to full stability

The unresolved variable did visibly constrain the memo more than in weaker earlier reports.

But the report still leaned toward:
- a relatively strong defensive-asset frame

without fully forcing the reader to downgrade:
- valuation confidence
- pricing confidence
- or recommendation strength

as sharply as the unresolved oil-price / FCF / payout interaction arguably required.

---

## Why this eval matters

This case is important because it prevents a common false conclusion:

> `the listed-company problem is now basically solved because the opening shape looks much better`

That is too optimistic.

This case shows a more realistic state of progress:
- judgment-memo shape has improved
- early triad structure has improved
- route visibility has improved
- but freshness hard-gate stability is still not reliable enough

In other words:
- the project has likely improved **artifact shape** faster than **execution stability**

That is exactly the kind of distinction a mature eval system should capture.

---

## Pass criteria

A good answer should:

1. preserve the improved judgment-memo opening
   - research anchors
   - one-sentence thesis
   - support / weakening / unresolved early

2. make the freshness gate truly binding
   - if the report date materially post-dates the allegedly latest quarter, stop and re-check
   - do not continue with a stale quarter inside the anchor block

3. keep the improved memo shape without letting that shape mask stale current-state control

4. make thesis-bearing claims auditable enough that stronger shape does not create false trust

5. let the key unresolved variable visibly narrow conclusion strength rather than merely sounding prudent

---

## Failure signs

Mark this eval as failed if the answer does several of the following:

- the opening looks materially better than older reports, but the anchor block still contains stale or mis-timed periods
- the report appears current because it has a research-anchor section, but the time layers are not actually trustworthy
- the memo shape improves, but the model still writes through a freshness inconsistency instead of stopping
- better structure makes it easier to miss that the memo is anchored incorrectly
- thesis-bearing claims remain only partly body-auditable even though the report looks more disciplined overall

---

## Suggested diagnosis

The primary diagnosis for this case is:

- **Anchor-governance failure** inside an otherwise improved listed-company judgment-memo execution

Secondary diagnoses may include:
- **Thesis-audit failure**
- **Conclusion-constraint failure**

But the defining lesson is that this is **not mainly a judgment-shape miss**.

That is what makes it a useful second-stage case.

---

## Suggested intervention targets

This case should push attention toward:

- `checklists/listed-company-report.md`
- `checklists/final-audit.md`
- `references/finance-date-discipline.md`
- `SKILL.md` listed-company current-state gate wording
- route-execution contracts that explicitly state: stale research anchors invalidate the memo even if the structure is otherwise good

This case should **not** be treated as evidence that the route hardening failed entirely.
Instead, it shows the next bottleneck after route-shape improvement.

---

## Reviewer checklist

- Did the report improve its opening shape relative to older weak company reports?
- Did the report visibly show support / weakening / unresolved early?
- Did the research-anchor block contain a stale or mis-timed quarter relative to the report date?
- If yes, did the memo still continue as if the anchor were acceptable?
- Did the improved structure make the stale anchor easier to overlook?
- Are the most thesis-bearing claims fully body-auditable, or only more convincing in tone?
- Does the unresolved variable actually narrow the conclusion enough?

---

## Suggested scoring

- **Pass:** improved judgment-memo shape with stable current-state anchor control
- **Partial:** judgment shape improved, but freshness or thesis-audit stability still leaks
- **Fail:** polished memo-looking artifact still anchored on stale time layers or unstable current-state control

---

## Why this case belongs in the repo

This case captures a project transition point.

Earlier listed-company cases mostly showed:
- route-family under-execution
- background-first drift
- weak judgment compression

This case shows a newer, more mature problem:
- the report is closer to the right shape
- the route is more visible
- but the execution is still not stable enough to trust the memo fully

That is exactly the kind of case a stronger repo should preserve, because it marks where the next real bottleneck now lives.
