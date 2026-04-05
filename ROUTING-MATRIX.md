# Routing Matrix

Use this file to route deep-research tasks into the correct research disciplines, audits, and visible report structures.

This file exists to reduce two failure modes:

1. the right rule exists but does not activate
2. the report seems informed by the rule but does not visibly execute it

## Route preflight

Before deep collection, explicitly decide:

- primary route
- closest alternative route
- why the chosen route wins
- required secondary disciplines
- required audits
- visible artifact contract

Do not proceed as if generic research were automatically sufficient when a specialized route would materially change structure, evidence burden, or audit burden.

## Global rule

For every task:

1. identify the real decision, judgment, or diligence goal
2. choose one primary route
3. attach the required secondary disciplines
4. make the route visible in the final artifact
5. run the required audits before delivery
6. ensure target-language coherence in the final artifact when the report is user-facing

If multiple routes apply, choose one primary route and attach the others as secondary disciplines.

Use the smallest complete set:

- one primary route
- up to 2–3 secondary disciplines

Do not activate everything. Activate the smallest set that produces a decision-useful, auditable, current, and clean final artifact.

---

## Route: Provider / Vendor Selection

### Trigger
Use when the task is mainly about:

- model/API supplier selection
- vendor shortlist
- platform choice
- provider comparison under deployment constraints

**Choose this route when:** the task is to select among providers and justify why one wins under explicit constraints.

**Do not use this route when:** the task is mainly to describe the market or explain industry direction without a real selection burden.

**Often confused with:** market outlook / industry evolution.

### Read
- `references/option-selection-and-shortlist-discipline.md`
- `references/source-traceability-and-claim-citation.md`
- `references/decision-report-template.md`

### Attach
- current-state verification
- source traceability
- quantitative role labeling when pricing, benchmarks, or scoring matter

### Audit
- `checklists/option-selection-final-audit.md`
- `checklists/source-traceability.md`
- `checklists/final-audit.md`

### Visible artifact contract
The final report should visibly show:

- current provider snapshot
- decision criteria / ranking logic
- ranked shortlist
- why the top option wins
- why the runner-up remains credible
- why other options lose
- accessibility / compliance / data-control / SLA treatment when relevant

### Hard fail
Fail if the report:

- compares stale anchor products or models without current verification
- treats mainland accessibility / compliance / SLA as side notes instead of ranking logic
- becomes a vendor overview instead of a choice memo

---

## Route: Market Entry / Regional Expansion

### Trigger
Use when the task is mainly about:

- whether to enter a market
- whether to prioritize a country or region
- market-entry sequencing
- regional expansion under constrained budget
- go / no-go / pilot-only expansion decisions

**Choose this route when:** the task is really about whether to enter, where to enter first, when to enter, or how to sequence entry.

**Do not use this route when:** the task is mainly a generic market overview or a simple option comparison without real entry logic.

**Often confused with:** constrained choice / shortlist.

### Read
- `references/option-selection-and-shortlist-discipline.md`
- `references/decision-report-template.md`
- `references/source-traceability-and-claim-citation.md`

### Attach
- current-state verification
- source traceability
- quantitative role labeling when market size, payback, cost assumptions, sequencing thresholds, or scenario-style numbers materially affect the recommendation

### Audit
- `checklists/option-selection-final-audit.md`
- `checklists/source-traceability.md`
- `checklists/final-audit.md`

### Visible artifact contract
The final report should visibly show:

- explicit recommendation: `go` / `not now` / `pilot only` / phased entry
- priority relative to alternatives
- country shortlist
- hard gates
- sequencing logic
- recommended entry motion
- distinction between:
  - regional hub
  - first revenue beachhead
  - later expansion market

### Hard fail
Fail if the report:

- drifts into a generic market overview
- gives country notes without a unified comparison unit
- recommends expansion without hard gates or sequencing logic
- collapses hub / beachhead / later expansion market into one vague “best market”

---

## Route: Market Outlook / Industry Evolution

### Trigger
Use when the task is mainly about:

- how a market will evolve
- next 6–12 month outlook
- adoption trajectory
- industry evolution
- scenario memo

**Choose this route when:** the task is to explain direction, evolution, trajectory, or structural change rather than pick a winner now.

**Do not use this route when:** the task has a real recommendation, shortlist, or selection burden.

**Often confused with:** provider selection or constrained choice.

### Read
- `references/market-outlook-and-scenario-discipline.md`
- `references/decision-report-template.md`
- `references/source-traceability-and-claim-citation.md`

### Attach
- current-state verification
- forward-looking claims discipline
- source traceability
- quantitative role labeling when forecasts or scenario math appear

### Audit
- `checklists/forward-looking-claims.md`
- `checklists/source-traceability.md`
- `checklists/final-audit.md`

### Visible artifact contract
The final report should visibly show:

- current market snapshot
- key drivers of change
- key blockers or friction points
- base case
- alternative scenarios
- stakeholder implications
- monitoring signals
- what would change the conclusion

### Hard fail
Fail if the report:

- remains an industry overview instead of an outlook memo
- mixes observed facts with scenario assumptions
- gives forecasts without visible scenario structure
- hides stakeholder implications inside generic narrative

---

## Route: First-tier / Top-tier / Competitive Positioning

### Trigger
Use when the task is mainly about:

- whether a company belongs in the top tier / first tier
- global-vs-domestic standing
- multidimensional competitive positioning
- prestige-label justification

**Choose this route when:** the real question is whether an entity reasonably belongs in a top group and the answer depends on dimension-level judgment before any overall label.

**Do not use this route when:** the task is mainly investment-style company analysis, valuation reasoning, or broad company profiling.

**Often confused with:** listed-company / investment-style research.

### Read
- `references/ranking-and-current-claims-discipline.md`
- `references/source-traceability-and-claim-citation.md`
- `references/decision-report-template.md`

### Attach
- current-state verification
- source traceability
- evidence-weight separation
- quantitative role labeling when numbers materially affect the positioning judgment

### Audit
- `checklists/source-traceability.md`
- `checklists/final-audit.md`

### Visible artifact contract
The final report should visibly show:

- scope
- metric
- timeframe
- dimension-level conclusions
- evidence-strength separation
- explicit overall-label gate

### Hard fail
Fail if the report:

- uses `第一梯队` / `top-tier` loosely
- collapses multiple dimensions into a prestige label without aggregation logic
- treats direct evidence, roadmap claims, valuation signals, and ecosystem anecdotes as equally strong

---

## Route: Constrained Choice / Shortlist / Option Selection

### Trigger
Use when the task is mainly about:

- choosing among several plausible options
- ranking or shortlist construction
- destination / venue / city / office / vendor choice
- practical decision memo under constraints

**Choose this route when:** the task is to choose among defined options using a visible comparison unit, shortlist logic, and ranking-change conditions.

**Do not use this route when:** the real task is market-entry gating, expansion sequencing, or broad market scanning.

**Often confused with:** market entry / regional expansion.

### Read
- `references/option-selection-and-shortlist-discipline.md`
- `references/decision-report-template.md`

### Attach
- quantitative role labeling when scoring, weighting, burden proxies, cost comparisons, or scenario comparisons materially affect ranking or recommendation

### Audit
- `checklists/option-selection-final-audit.md`
- `checklists/final-audit.md`

### Visible artifact contract
The final report should visibly show:

- decision architecture
- shortlist construction logic
- comparison unit
- final ranking or selection
- why the top option wins
- why the runner-up remains credible
- ranking-reversal conditions
- hidden operational burdens when relevant

### Hard fail
Fail if the report:

- gives a recommendation without showing how the shortlist was built
- uses numbers without labeling observed fact / proxy / assumption / model output
- turns the task into descriptive option blurbs instead of a true choice memo

---

## Route: Listed Company / Investment-style Research

### Trigger
Use when the task is mainly about:

- listed companies
- valuation / market cap / growth / guidance
- investment memo style judgments
- equity-style diligence

**Choose this route when:** the task carries listed-company, valuation, public-market, or investment-style judgment burden.

**Do not use this route when:** the real question is a definition-sensitive positioning judgment rather than an investment-style memo.

**Often confused with:** first-tier / competitive positioning.

### Read
- `references/finance-date-discipline.md`
- `references/market-sizing-and-share-discipline.md` when share/size claims matter
- `references/source-traceability-and-claim-citation.md`

### Attach
- current-state verification
- forward-looking claims discipline when forecasts appear
- source traceability

### Audit
- `checklists/listed-company-report.md`
- `checklists/source-traceability.md`
- `checklists/final-audit.md`

### Visible artifact contract
The final report should visibly show:

- current business snapshot
- current financial or market snapshot
- clearly dated key numbers
- separation of reported facts vs estimates
- risks and counter-evidence
- uncertainty around forward views

### Hard fail
Fail if the report:

- mixes reported metrics and forward estimates without clear labels
- uses undated financial numbers
- makes market-position claims without scope
- lets valuation narrative substitute for business evidence

---

## Cross-cutting disciplines

### Current-state verification
Attach when the task involves current products, pricing, versions, company status, provider state, rankings, or other fast-moving facts.

Visible sign:
- a clearly current snapshot or freshness check

Fail if:
- likely-but-stale knowledge substitutes for verification

### Source traceability
Attach when the task is structured, claim-heavy, investment-relevant, or recommendation-heavy.

Visible sign:
- major claims are auditable in the body, not only in the source appendix

Fail if:
- key conclusions cannot be traced to identifiable evidence

### Forward-looking claims discipline
Attach when the task includes forecasts, roadmap claims, target dates, expected pricing, or expected market evolution.

Visible sign:
- forward-looking claims are labeled by source role and uncertainty

Fail if:
- `预计` / `expected` / `likely` appears without source role or confidence framing

### Quantitative role labeling
Attach when the task uses proxies, scorecards, market sizing, scenario math, or composite scoring.

Visible sign:
- important numbers are labeled as observed fact / proxy / assumption / model output / illustrative calculation

Fail if:
- internally generated estimates appear as if they were observed facts

### Delivery cleanliness
Attach when the output is intended for user-facing delivery, especially PDF.

Visible sign:
- no citation artifacts
- no placeholder residue
- no template markers
- no rendering leakage

Fail if:
- the report body exposes internal syntax, parser debris, or generator hints

---

## Routing priority

If multiple primary-looking routes apply, use this order:

1. listed-company / investment-style
2. market entry / regional expansion
3. provider / vendor selection
4. first-tier / competitive positioning
5. market outlook / industry evolution
6. constrained choice / shortlist

Choose the route that most strongly determines report structure and audit burden.

---

## Final check

Before delivery, ask:

1. did the correct route fire?
2. did the required secondary disciplines attach?
3. is the route visibly executed in the final artifact?

A route only counts if the final report visibly satisfies its artifact contract.

If the route is implicit in reasoning but not visible in delivery, treat that as an execution failure.
