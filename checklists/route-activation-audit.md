# Route Activation Audit

Use this checklist when a route-specialized report still reads like generic research, or when the final artifact does not visibly match the chosen route's required structure.

It audits whether route activation was explicit and whether the route actually shaped the output.

## Preflight

- [ ] the primary route was consciously chosen before deep collection began, not retrofitted during writing
- [ ] the closest alternative route was identified and a reason exists for why the chosen route wins
- [ ] the selected route's "Do not use" / "Often confused with" clauses from `ROUTING-MATRIX.md` were checked before finalizing; if the task matched a disqualifying condition, the route was reconsidered or the boundary judgment was documented
- [ ] if a secondary route is declared, its hard-fail conditions from `ROUTING-MATRIX.md` were verified at selection time (not deferred to delivery); if a condition is inapplicable, the reason is documented
- [ ] when 2+ secondary routes are declared, each secondary route's hard-fail check status is explicitly listed (not assumed covered by the primary route's checks)
- [ ] the total route count (primary + secondary) was reviewed: if it exceeds 3, scope focus was re-examined and the decision to keep the current route set is documented
- [ ] secondary body-text share is reasonable (secondary-route content does not exceed roughly 25% of body text when the primary route requires minimizing those sections; if it does, consider shared-workflow declaration or route simplification)
- [ ] a compact execution contract exists before synthesis: opening mandate, mandatory sections, hard-fail conditions, minimize / move later
- [ ] all required audits for this route (from `ROUTING-MATRIX.md` `### Audit` section) are identified and each has an explicit run status: **已通过** (passed, with evidence visible in the artifact via the standardized 「证据」column — see `references/report-template.md` §Route and audit status), **已跳过（附理由）** (skipped, with documented reason), or **未运行（附理由）** (not run, with documented reason); if any required audit is missing, it is run before the report is considered ready

## Route selection visibility

- [ ] the primary route is inferable from the final artifact without reading internal notes
- [ ] the report satisfies its route's visible artifact contract
- [ ] a reviewer would not guess a different primary route from the report's structure and burden allocation

## Route-to-contract conversion

- [ ] the execution contract was specific enough to determine report structure, not just topic
- [ ] mandatory sections from the contract are present and carry the expected burden
- [ ] sections that should be minimized are visibly shorter or placed later than the primary decision logic
- [ ] the opening 20-30% already reflects the route rather than reading like reusable background

## Required secondary disciplines

- [ ] every secondary discipline attached by the route is visibly executed in the final artifact
- [ ] attached discipline files were read and applied, not only named
- [ ] if current-state verification was required, the report shows a verifiably current snapshot
- [ ] if source traceability was required, load-bearing claims are auditable in the body
- [ ] if forward-looking claims discipline was required, forecasts and estimates have visible source role and time basis
- [ ] if quantitative role labeling was required, important numbers are labeled as observed fact / proxy / assumption / model output
- [ ] if scope completeness was required, the report states its actual coverage boundaries and covers load-bearing geographies, segments, or regulatory regimes proportionally to their importance
- [ ] if decision utility was required, the decision frame is explicit and drives report structure, with a clear route-appropriate bottom line

## Route execution integrity

- [ ] the report does not fall back into generic overview mode despite route selection
- [ ] generic background, market history, or option blurbs do not occupy the strongest positions unless the route genuinely requires them
- [ ] the route is visible not only in section headers, but also in the burden each section carries
- [ ] if a route-specific section were removed, the report would materially lose decision logic

## Hard-fail check

Preflight hard-fail verification (above) identifies conditions at selection time. This delivery-time check re-verifies them — the task context or evidence may have changed during research.

- [ ] route-specific hard-fail conditions from the routing matrix were checked before delivery
- [ ] the report does not exhibit any of the named hard-fail patterns for its primary route
- [ ] if multiple routes are declared (primary + secondary), the hard-fail conditions of **all** declared routes are verified; a secondary route's hard-fail conditions are not skipped because it is "secondary"; if a condition is genuinely inapplicable, the reason is documented rather than skipped silently

## Contract item-by-item verification

The route execution contract (from `ROUTING-MATRIX.md`) defines what the final artifact must visibly deliver. Run this block to verify that each contract dimension is satisfied in the delivered output, not only in the research plan.

This block complements the sections above — it checks contract‑specific tests that operate at item level rather than structural level. If a contract dimension does not exist for the chosen route (e.g. the route defines no mandatory sections, or has no explicit labels), mark that item as N/A.

### Opening drift check
- [ ] the opening could NOT be swapped into a different route type without sounding unnatural (pass: opening is route-specific; fail: opening is generic enough to carry across routes — swap test from `ROUTING-MATRIX.md` line 649)
- [ ] removing background paragraphs from the opening would sharpen rather than weaken the report (fail: background-first drift — the opening is route-agnostic background, not route-executing judgment)

### Mandatory section quality
- [ ] each mandatory section from the contract is decision‑useful (it changes the reader's view) rather than descriptive filler (it adds completeness without changing the view)

### Visible label check
- [ ] route‑specific labels or structural markers from the contract appear explicitly in the final artifact (e.g. "go / not now / pilot only", "ranked shortlist", "base case vs scenarios", "hub / beachhead / expansion"; for structure-prescribed routes like first-tier positioning: dimension-level conclusions, evidence-strength separation)

## Quality bar

A report that fails this checklist may have the right route selected, but the route was not operationalized strongly enough to shape the output. Treat this as an execution failure, not a routing failure.
