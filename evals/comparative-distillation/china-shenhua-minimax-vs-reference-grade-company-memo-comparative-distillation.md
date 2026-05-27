# China Shenhua MiniMax vs Reference-Grade Company Memo Distillation

## Case identity

- **Case name:** China Shenhua listed-company judgment-visibility comparative distillation
- **Date:** 2026-04-16
- **Research question:** What reusable repo changes should be extracted from a user-provided MiniMax China Shenhua report when compared against a reference-grade target artifact shaped by the current deep-research rules?
- **Why this comparison matters:** The MiniMax report is not a bad report. It is strong enough to pass as a polished company brief, which makes it a good stress case for whether the repo can force a true investment-style judgment memo rather than a structured overview.
- **Report A:** User-provided MiniMax PDF report on China Shenhua dated 2026-04-16
- **Report B:** Reference-grade rewrite target based on the current listed-company route, existing templates, and the newly hardened judgment-visibility rules
- **Reference / stronger report (if any):** Report B is not a second model output. It is a rule-conformant target artifact contract that represents what a passing rewrite should look like.
- **Prompt(s):** Research China Shenhua in the style of deep-research; cover business, industry position, customers, competitors, last-two-year financial signals, bull/bear logic, and 1-3 year opportunities / risks; distinguish confirmed facts, inference, and uncertainty; produce a Chinese structured report and PDF.
- **Important scope or timing differences:** This is a quasi-paired comparison. Report B is a reference-grade target rather than a separately generated full report. That means the comparison is useful for repo hardening, but not for model-leaderboard style judgments.

---

## Comparison purpose

Use this comparison to identify which structural disciplines the current MiniMax China Shenhua report still misses even after visible evidence labels and a strong report skeleton are present.

The purpose is not to say "MiniMax is worse." The purpose is to determine whether the remaining gap is:
- a missing rule
- a missing trigger
- or execution drift despite existing rules

This comparison is especially useful because the weaker artifact is already polished enough to hide its own remaining weaknesses.

---

## Dimension 1: Current-state discipline

### Report A
- The report visibly states a coverage range such as `2024 full year + 2025 full year + 2026 Q1 latest data`.
- It signals awareness that freshness matters.
- But the report still feels anchored by a broad company snapshot rather than by a clearly locked current thesis tied to the latest reporting layers.
- The opening does not visibly force the reader to see: latest full-year / latest quarter / latest market snapshot / why those anchors drive the present judgment.

### Report B
- The opening would explicitly lock the research anchors before broad narrative expansion.
- The first page would show the current thesis only after making the time layers visible.
- Older but still useful numbers would be demoted to historical context rather than allowed to carry the opening burden.

### Gap
- Freshness awareness exists in Report A, but freshness execution is still too weakly operationalized in the opening structure.
- The failure is less "stale data everywhere" and more "stale-anchor-like report shape still survives despite partial freshness signaling."

### Candidate action
- Strengthen the listed-company route so the opening must contain a compact research-anchor block and current-thesis block before business-profile expansion.

### Action type
- `TEMPLATE_CHANGE`

---

## Dimension 2: Numerical and date discipline

### Report A
- The report includes many concrete numbers and time references.
- However, several important figures still blur categories such as:
  - reported historical fact
  - current market snapshot
  - projected or scenario-like expectation
  - derived or comparative claim
- A/H share, dividend-yield, industry ranking, and price-level statements risk being read as one unified fact layer.

### Report B
- A passing artifact would make time layering and number-role layering more explicit.
- Load-bearing numbers would visibly show whether they are:
  - filing fact
  - current market snapshot with date
  - analyst or scenario expectation
  - inferred comparison
- Multi-venue numbers such as A-share vs H-share framing would be kept explicitly separated when they affect interpretation.

### Gap
- Report A has many real numbers, but some of the most important numbers still do too much rhetorical work without enough metric-role clarity.

### Candidate action
- Add a listed-company audit rule requiring explicit separation when A-share / H-share / current-yield / historical-distribution / scenario-price statements are used in one memo.

### Action type
- `CHECKLIST_HARDENING`

---

## Dimension 3: Source traceability and evidence weighting

### Report A
- The report uses visible evidence buckets such as confirmed facts / inference / open uncertainty.
- But several load-bearing claims still remain bibliography-level rather than claim-level in auditability.
- Strong-sounding statements about transport-cost advantage, volatility sensitivity, dividend superiority, and growth impact from asset injection do not visibly tell the reader:
  - what source supports the exact claim
  - whether the claim is direct or inferred
  - whether the wording was downgraded when support was indirect

### Report B
- The stronger reference artifact would make the load-bearing claims auditable in the body.
- It would not rely on confidence labels alone.
- At minimum, the body would reveal source role and evidence weight for the specific claims doing the most bottom-line work.

### Gap
- Report A shows confidence-label discipline, but not yet true claim-audit discipline.
- The failure is not absence of sources in the broad sense; it is a lack of visible linkage between key conclusion-bearing claims and the exact evidence role behind them.

### Candidate action
- Promote a stronger claim-traceability rule for listed-company reports: if a claim materially supports the thesis, it must be auditable in the body, not only implied by a source list or section bibliography.

### Action type
- `CHECKLIST_HARDENING`

---

## Dimension 4: Forward-looking claim discipline

### Report A
- The report does not collapse into reckless hype.
- But it still tends to compress these layers too smoothly:
  - confirmed transaction completion
  - likely operating implication
  - medium-term growth implication
  - scenario-like commodity price support
- This creates a "polite certainty inflation" problem rather than an obvious hallucination problem.

### Report B
- A stronger rewrite would force a three-way split whenever corporate action or forward scenario language becomes load-bearing:
  - confirmed facts
  - likely implications
  - unresolved timing / realization / quality uncertainty
- Forward-looking commodity-price or dividend-defense language would carry more explicit source role and downgrade conditions.

### Gap
- Report A is disciplined enough to avoid cartoonish overclaiming, but still too smooth in translating real events into thesis support.

### Candidate action
- Add a reusable corporate-action compression guard covering asset injection, financing completion, restructuring, and similar event-to-thesis jumps.

### Action type
- `NEW_RULE`

---

## Dimension 5: Structural readability and information density

### Report A
- The report is organized and readable.
- It has the look of a serious report.
- But the front page still behaves more like a mixed report opening than a judgment-first memo opening.
- Evidence labels and process visibility compete with thesis visibility.

### Report B
- The stronger target artifact would keep methodology compact and subordinate.
- The first page would make the reader see, within seconds:
  - core thesis
  - key risks
  - key unknowns
  - why the current view is not fully precise
- The layout would feel like a decision memo first, not a report shell with judgment embedded inside it.

### Gap
- The main problem is not ugly formatting or density overload. It is that report readability still serves explanation better than judgment.

### Candidate action
- Tighten the report-template front-page rule so evidence legends and process notes cannot dominate the first scan when the route carries investment-style judgment burden.

### Action type
- `TEMPLATE_CHANGE`

---

## Dimension 6: Decision usefulness

### Report A
- The report is useful as a structured orientation to China Shenhua.
- It identifies many true or plausible factors relevant to an investor-style view.
- But it still underperforms as a current judgment memo because it does not compress clearly enough around:
  - strongest support
  - strongest weakening evidence
  - key unresolved variable
  - downgrade boundary
  - what would change the conclusion

### Report B
- A passing reference artifact would visibly separate:
  - what supports the thesis now
  - what weakens it now
  - what remains unresolved and therefore narrows the conclusion
- Risks would not sit as ornamental caution. They would visibly constrain confidence, timing precision, or valuation precision.

### Gap
- Report A is stronger as a company understanding artifact than as a decision-grade company memo.
- This is now a recurring failure family, not a one-off China Shenhua quirk.

### Candidate action
- Harden the decision-report template and listed-company checklist around a mandatory support / weakening / unresolved split in the early report structure.

### Action type
- `TEMPLATE_CHANGE`

---

## Candidate-action summary

| # | Candidate action | Failure family | Action type | Proposed home |
|---|---|---|---|---|
| 1 | Require research-anchor block before broad company narrative | current-state / opening-shape discipline | `TEMPLATE_CHANGE` | `references/decision-report-template.md` |
| 2 | Separate multi-venue and market-snapshot number roles more explicitly | numerical / date discipline | `CHECKLIST_HARDENING` | `checklists/listed-company-report.md` |
| 3 | Require body-level auditability for thesis-bearing claims | source traceability / evidence weighting | `CHECKLIST_HARDENING` | `checklists/final-audit.md` + `checklists/listed-company-report.md` |
| 4 | Add corporate-action compression guard | forward-looking / event-to-thesis inflation | `NEW_RULE` | `references/decision-report-template.md` or `references/finance-date-discipline.md` |
| 5 | Tighten front-page judgment visibility under investment-style route | output structure / information density | `TEMPLATE_CHANGE` | `references/report-template.md` |
| 6 | Require early support / weakening / unresolved split | decision usefulness / judgment visibility | `TEMPLATE_CHANGE` | `references/decision-report-template.md` + `checklists/listed-company-report.md` |

---

## Triage notes

### Candidate 1
- **Why it matters:** Listed-company reports can appear current while still being structurally anchored on background rather than on the true latest decision-relevant layers.
- **Why it is reusable:** This applies to many equity-style memos, especially when the model already has enough data to sound current.
- **Why this home is best:** The problem is mainly opening-shape execution, so the decision-report template is the right first home.
- **Promotion status:** `PROMOTE_NOW`

### Candidate 2
- **Why it matters:** A/H share, yield, market cap, and current-price framing can quietly blur number roles and venue distinctions in China-listed-company work.
- **Why it is reusable:** This is broader than China Shenhua; it applies to dual-listed and multi-venue company reports generally.
- **Why this home is best:** This belongs in the route-specific checklist because it is a recurrent audit issue, not just phrasing guidance.
- **Promotion status:** `PROMOTE_NOW`

### Candidate 3
- **Why it matters:** A source list is not enough when the bottom-line thesis depends on a handful of strong comparative claims.
- **Why it is reusable:** This is a recurring failure family across Cambricon, AMD-style company reports, and now China Shenhua.
- **Why this home is best:** Final audit + listed-company checklist together catch both general and route-specific forms of the failure.
- **Promotion status:** `PROMOTE_NOW`

### Candidate 4
- **Why it matters:** Corporate actions are especially prone to over-smooth narrative inflation because the facts are real but the implications are only partly known.
- **Why it is reusable:** Applies to M&A, asset injection, financing, restructuring, and strategic investment cases across listed-company research.
- **Why this home is best:** This is fundamentally a reasoning-shape and interpretation rule, so it belongs in the decision template or finance-date discipline rather than only a checklist.
- **Promotion status:** `PROMOTE_NOW`

### Candidate 5
- **Why it matters:** If the thesis is hard to see on the first page, the memo will keep reading as a report-shaped overview even when the logic is decent.
- **Why it is reusable:** Front-page judgment visibility is a cross-case weakness already seen in company and PDF-heavy outputs.
- **Why this home is best:** Report-template front-page discipline is the natural place to keep this pressure always visible.
- **Promotion status:** `PROMOTE_NOW`

### Candidate 6
- **Why it matters:** Decorative caveats do not improve decision usefulness unless they visibly narrow the conclusion.
- **Why it is reusable:** This repeats the broader unknown-to-conclusion linkage problem, but in a more memo-structural listed-company form.
- **Why this home is best:** It needs both template pressure and checklist enforcement.
- **Promotion status:** `PROMOTE_NOW`

---

## Things explicitly rejected

| Observation | Why rejected |
|---|---|
| "The report is already good enough, so no repo change is needed." | Too impressionistic; this case is useful precisely because polished overview quality can hide real memo-grade weaknesses |
| "This should become a separate China coal research route." | Too case-specific; the better abstraction is listed-company judgment visibility, not a sector-specific route |
| "Evidence labels should be removed because they did not solve the problem." | Wrong lesson; the issue is weak execution and weighting, not that evidence labels themselves are useless |
| "This proves MiniMax cannot do company reports." | Not auditable and not repo-useful; the right output is discipline hardening, not model tribalism |

---

## Final judgment

### What the stronger report did better
The reference-grade target does not merely add fresher data or more sources. It changes the artifact shape:
- thesis first
- time anchors early
- support / weakening / unresolved split visible
- claim-level auditability for load-bearing points
- corporate-action facts separated from their uncertain implications

### What should change in the repo now
The repo should harden:
1. early research-anchor visibility for listed-company work
2. multi-venue and number-role separation in listed-company audits
3. body-level auditability for thesis-bearing claims
4. corporate-action compression guard
5. front-page judgment visibility
6. early support / weakening / unresolved split

### What should wait for another confirming case
- a dedicated new sub-route for corporate-action-heavy company memos
- any fully separate dual-listed-company route
- any sector-specific energy / coal research discipline

### Is this mainly a missing rule, missing trigger, or execution problem?
Mainly an **execution problem**, secondarily a **template / checklist hardness problem**, and only weakly a missing-rule problem.

The core rules already existed in rough form, but this case shows they were not yet strong enough to force the right artifact shape.

---

## Minimal quality bar

Before finalizing this file, check:

- [x] the two reports are comparable enough to justify distillation
- [x] the comparison used the six fixed dimensions
- [x] each accepted candidate has an action type
- [x] each accepted candidate has a proposed repo home
- [x] at least one rejected observation is documented when relevant
- [x] the final judgment distinguishes rule gap vs trigger gap vs execution gap

This file is intended as a repo-hardening distillation artifact, not as a benchmark verdict on models.
