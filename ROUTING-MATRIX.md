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
- opening-section contract
- non-negotiable sections the final artifact must contain
- route-specific hard-fail conditions to guard against during synthesis

Do not proceed as if generic research were automatically sufficient when a specialized route would materially change structure, evidence burden, or audit burden.

If the route changes the answer shape, do not wait until late-stage writing to apply it. The route should determine the report skeleton before broad evidence accumulation turns into generic prose.

## Global rule

For every task:

1. identify the real decision, judgment, or diligence goal
2. choose one primary route
3. attach the required secondary disciplines
4. translate the route into a visible section-level execution contract before drafting
5. make the route visible in the final artifact
6. run the required audits before delivery
7. ensure target-language coherence in the final artifact when the report is user-facing

If multiple routes apply, choose one primary route and attach the others as secondary disciplines.

Use the smallest complete set:

- one primary route
- up to 2–3 secondary disciplines

Do not activate everything. Activate the smallest set that produces a decision-useful, auditable, current, and clean final artifact.

### Secondary route hard-fail requirement

When a report declares multiple routes (primary + secondary), the hard-fail conditions of **all** declared routes must be verified. A secondary route's hard-fail conditions may not be skipped because it is "secondary." If a hard-fail condition is genuinely inapplicable to the task, document the inapplicability reason rather than skipping the check silently.

### Route boundary resolution requirement

When a report identifies a close alternative route (i.e., one listed in ROUTING-MATRIX.md's "Often confused with" section for the chosen route) but decides to stay in the current route, the report or execution contract must document:

a) which specific hard-fail conditions of the alternative route were checked
b) why those conditions do not apply to this task
c) under what conditions the route should be switched

"It was considered" is not sufficient resolution. If any hard-fail condition of the alternative route is triggered during actual execution, the report **must not** remain in the current route without a documented override reason. A single triggered condition is sufficient to require resolution — the threshold is not cumulative.

This requirement applies whenever a route selection considers and rejects an alternative — whether at preflight time or during delivery review.

### Route inflation warning

Declaring 2+ secondary routes without verifying their hard-fail conditions constitutes **route inflation** — the route list suggests structured methodology, but the unchecked hard-fails create a quality-control blind spot.

Rules to prevent route inflation:

- The declared route list must reflect **actual delivery scope**, not the most comprehensive coverage set. If the output behaves as a shared-workflow survey, declare it as shared-workflow rather than inflating the route list.
- When 2+ secondary routes are declared, the hard-fail check status of each must be explicitly verifiable in the process log or artifact (not assumed covered by the primary route's checks). Absent evidence of per-route verification, the declarations constitute route inflation.
- If the share of body text consumed by secondary-route content (tools, compliance, ROI, market outlook, etc.) exceeds roughly 25% — especially when the primary route requires minimizing those sections (e.g., Technical Deep-dive minimizes tools-overview sections) — consider using Shared-Workflow or simplifying the route declaration set.
- If the total route count (primary + secondary) exceeds 3, re-examine scope focus — the task may be better served by a narrower primary route or a shared-workflow path.

When in doubt, declare fewer routes with verified hard-fails rather than more routes with unchecked assumptions.

> **Note on terms:** "Secondary routes" in this section refers only to specialized routes used as secondary disciplines (e.g., Provider Selection attached to a Market Outlook primary), not to cross-cutting disciplines like source traceability or current-state verification. The distinction is defined in `references/route-activation-and-preflight.md` Step 2.

## Route execution contract

Before synthesis, convert the selected route into a compact execution contract.

That contract should make these items explicit:

- what the opening 20-30% of the report must do
- which sections are mandatory because the route would fail without them
- which tempting generic sections should be minimized or cut
- which visible artifact would prove that the route fired correctly
- which route-specific hard-fail patterns must be checked before delivery

Use a compact format like:

- primary route:
- closest alternative route:
- opening must do:
- mandatory sections:
- minimize / move later:
- visible proof the route fired:
- hard-fail signs to watch:

A route is not fully selected until this contract exists in operational form.

If the report can still be drafted as a generic overview with a recommendation paragraph appended near the end, the route has not yet been operationalized strongly enough.

---

## Route: Provider / Vendor Selection

### Trigger
Use when the task is mainly about:

- model/API supplier selection
- vendor shortlist
- platform choice
- provider comparison under deployment constraints

**Choose this route when:** the task is to select among providers and justify why one wins under explicit constraints.

**Do not use this route when:** the task is mainly to describe the market or explain industry direction without a real selection burden. For physical hardware / device procurement, purchase recommendation, build, or configuration choices (NAS, home server, build-ready stack, office equipment purchasing), use the Equipment Selection / Procurement route instead.

**Often confused with:** market outlook / industry evolution, equipment selection / procurement / home-server planning.

### Read
- `references/option-selection-and-shortlist-discipline.md`
- `references/source-traceability-and-claim-citation.md`
- `references/decision-report-template.md`

### Attach
- current-state verification
- source traceability
- decision utility
- quantitative role labeling when pricing, benchmarks, or scoring matter
- data conflict resolution when pricing, performance metrics, or benchmark data from different sources disagree

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

### Micro-audit focus
For this route, be especially strict about:

- explicit go / not now / pilot only / phased-entry language
- whether hub / beachhead / later expansion roles are separated when relevant
- whether sequencing depends on named hard gates rather than generic optimism
- whether the recommendation appears before country-by-country narrative expands

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
- decision utility
- quantitative role labeling when market size, payback, cost assumptions, sequencing thresholds, or scenario-style numbers materially affect the recommendation — see `checklists/quantitative-role-audit.md` §Route-specific checks (Market Entry)
- sensitivity analysis when the recommendation depends on load-bearing numerical assumptions (growth rates, market size, payback periods)

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
- collapses hub / beachhead / later expansion market into one vague "best market"

---

## Route: Market Outlook / Industry Evolution

### Trigger
Use when the task is mainly about:

- how a market will evolve
- next 6–24 month outlook
- adoption trajectory
- industry evolution
- scenario memo

**Choose this route when:** the task is to explain direction, evolution, trajectory, or structural change rather than pick a winner now.

**Do not use this route when:** the task has a real recommendation, shortlist, or selection burden. Specifically: ranking entities or options, predicting competition outcomes among defined participants, or choosing a provider/supplier. See `references/market-outlook-and-scenario-discipline.md` "When not to use this route" for boundary examples.

Concrete boundary examples:
- "哪支球队最可能夺冠" → Constrained Choice (ranking burden)
- "世界杯足球产业链的商业前景" → Market Outlook (market evolution without ranking)
- "人形机器人产业链未来 12 个月如何演化" → Market Outlook (trajectory question)
- "应该选哪个 AI 模型供应商" → Provider Selection (selection burden)

**Often confused with:** provider selection or constrained choice.

### Read
- `references/market-outlook-and-scenario-discipline.md`
- `references/forward-looking-discipline.md`
- `references/decision-report-template.md`
- `references/source-traceability-and-claim-citation.md`

### Attach
- current-state verification
- forward-looking claims discipline
- source traceability
- scope completeness when the report claims global or broad market scope
- quantitative role labeling when forecasts or scenario math appear — see `checklists/quantitative-role-audit.md` §Route-specific checks (Market Outlook)
- sensitivity analysis when forecasts, market size estimates, or adoption projections materially affect the conclusion

### Audit
- `checklists/market-outlook-audit.md`
- `checklists/forward-looking-claims.md`
- `checklists/source-traceability.md`
- `checklists/final-audit.md`

### Visible artifact contract
The final report should visibly show:

- current market snapshot
- key drivers of change
- key blockers or friction points
- base case
- structured alternative scenarios (at minimum base + one alternative; three scenarios — optimistic / base / pessimistic — when uncertainty is material, which is the default for market-outlook tasks)
- stakeholder implications covering at least 3 distinct stakeholder types
- monitoring signals
- what would change the conclusion

### Hard fail
Fail if the report:

- remains an industry overview instead of an outlook memo
- mixes observed facts with scenario assumptions
- gives forecasts without visible scenario structure, or rests on a single base case with no alternative scenarios
- hides stakeholder implications inside generic narrative
- covers only investor stakeholder implications while ignoring technology developers, policymakers, enterprise buyers, or end users
- uses Market Outlook for a task whose core output carries recommendation, ranking, selection, or winner-prediction burden among defined options — including team ranking, supplier shortlist, investment pick, or any "which one wins" framing (wrong route — use Constrained Choice / Shortlist instead)

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
- scope completeness when the positioning claim is global or multi-region
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

### Micro-audit focus
For this route, be especially strict about:

- whether the winning option beats the runner-up for a few explicit load-bearing reasons rather than diffuse overall narration
- whether the runner-up remains credible in a named scenario instead of serving as a ceremonial second place
- whether rejected options are rejected for actual decision reasons rather than lower narrative attention
- whether hidden operational burdens sit in the ranking logic rather than in cleanup caveats
- whether narrative weight is allocated in proportion to the final decision rather than making all plausible options feel equally alive

### Trigger
Use when the task is mainly about:

- choosing among several plausible options
- ranking or shortlist construction
- destination / venue / city / office / vendor choice
- practical decision memo under constraints

**Choose this route when:** the task is to choose among defined options using a visible comparison unit, shortlist logic, and ranking-change conditions.

**Do not use this route when:** the real task is market-entry gating, expansion sequencing, or broad market scanning.

**Often confused with:** market entry / regional expansion, equipment selection / procurement.

### Read
- `references/option-selection-and-shortlist-discipline.md`
- `references/decision-report-template.md`

### Attach
- decision utility
- quantitative role labeling when scoring, weighting, burden proxies, cost comparisons, or scenario comparisons materially affect ranking or recommendation — see `checklists/quantitative-role-audit.md` §Route-specific checks (Constrained Choice)

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
- exhibits background-first drift — the executive summary or judgment-first opening is immediately followed by >5 lines of pure background description (venue context, event history, category overview, halftime-show information, or similar) before the decision architecture or comparison framework begins

---

## Route: Regulatory / Policy Impact Analysis

### Micro-audit focus
For this route, be especially strict about:

- whether the report separates current regulations from pending/in-progress legislation
- whether regulatory impact is analyzed at business level (direct vs indirect impact)
- whether enforcement reality is distinguished from letter-of-law analysis
- whether uncertainty around regulatory timing and enforcement is explicitly bounded
- whether scenario analysis covers optimistic / base / pessimistic outcomes

### Trigger
Use when the task is mainly about:

- regulatory environment assessment
- policy risk evaluation
- compliance impact analysis
- regulatory change impact on business/industry
- policy-driven investment or strategic decisions

**Choose this route when:** the core question is understanding the regulatory environment, assessing policy risk, or judging compliance impact on a business or industry.

**Do not use this route when:** regulation is background context only (use other routes + attach regulatory discipline). If the task is primarily about listed-company valuation, market entry sequencing, or technical feasibility, use those routes and attach regulatory analysis as a secondary discipline.

**Often confused with:** listed-company / investment-style research (regulation may be one section), market outlook / industry evolution (regulatory changes may be one driver).

**Route-conflict examples:**
- "Analyze the impact of EU AI Act on the European AI market" — this is regulatory analysis if the core question is understanding the regulatory framework and its business impact; it becomes market outlook if the focus is market evolution with regulation as one driver
- "Should we enter the Chinese market given new data localization laws?" — this is market entry if the question is entry sequencing; it becomes regulatory analysis if the question is primarily about understanding and evaluating the regulatory constraint
- "How will US export controls affect our listed company's revenue?" — this is listed-company research if the task is investment judgment; it becomes regulatory analysis if the task is understanding the regulatory impact mechanism

### Read
- `references/current-state-verification.md` (current regulatory snapshot)
- `references/forward-looking-discipline.md` (when predicting regulatory changes)
- `references/source-quality.md` (regulatory sources: official gazette vs news interpretation vs analyst speculation)
- `references/data-conflict-resolution.md` (when regulatory interpretations conflict across sources)

### Attach
- current-state verification (current regulatory state)
- source traceability (regulatory text vs interpretation vs speculation)
- forward-looking claims discipline (regulatory change predictions)
- scope completeness when regulatory analysis claims global or multi-jurisdiction coverage

### Audit
- `checklists/regulatory-analysis-audit.md`
- `checklists/source-traceability.md`
- `checklists/final-audit.md`

### Visible artifact contract
The final report should visibly show:

- **Current regulatory snapshot**: regulations currently in effect
- **Pending legislation / policy**: in-progress bills, draft regulations, public comment periods
- **Business impact analysis**: direct impact vs indirect impact, quantified where possible
- **Timeline**: enacted → transition period → future changes
- **Uncertainty bounds**: enforcement intensity, timing, possible exemptions
- **Scenario analysis**: optimistic / base / pessimistic scenarios
- **Business/industry implications**: actionable conclusions for decision-makers
- **Monitoring signals**: what to watch for regulatory changes

### Hard fail
Fail if the report:

- lists regulations without analyzing business impact
- confuses regulatory text with media interpretation
- gives false precision on regulatory timing ("will pass in month X") without uncertainty bounds
- ignores enforcement reality (letter-of-law vs actual enforcement)
- treats all jurisdictions as equivalent without prioritizing binding regimes
- presents regulatory risk as binary (yes/no) rather than graduated with scenarios

---

## Route: Equipment Selection / Procurement / Home-server Planning

### Micro-audit focus
For this route, be especially strict about:

- whether the recommendation binds hardware route and system choice into one stack decision
- whether minimum viable vs recommended configuration is separated when it changes the answer materially
- whether household operating burdens like noise, power, maintenance, backup, and expansion friction are treated as ranking variables rather than side notes
- whether rejected routes lose for explicit operator constraints rather than broad category descriptions
- whether the report segments recommendation by workload or operator persona when the answer materially differs by use case
- whether benchmark performance numbers that carry a recommendation show test method and comparability boundary

### Trigger
Use when the task is mainly about:

- what hardware or device to buy or build
- home server / NAS / homelab planning
- budgeted configuration recommendation
- hardware + software stack recommendation under household or operator constraints
- route choice such as NAS vs mini PC vs self-build vs used workstation

**Choose this route when:** the user needs a purchase-ready or build-ready recommendation under visible budget, maintenance, noise, power, storage, networking, or expansion constraints.

**Do not use this route when:** the task is mainly to explain hardware categories, compare benchmarks abstractly, or teach general technical concepts without a real procurement burden.

**Often confused with:** constrained choice / shortlist, market outlook / industry evolution.

**Route-conflict examples:**
- NAS vs mini PC vs self-build vs used workstation — this is an equipment selection task even though multiple "vendors" are involved; do not default to provider / vendor selection
- hardware vendor shortlist with build-ready stack recommendation — if the output must include budget, configuration, and operating burden, use equipment selection rather than provider selection
- home-server budget planning — even when framed as a cost comparison, the real decision is a procurement memo, not a market outlook or provider comparison

### Read
- `references/decision-report-template.md`
- `references/option-selection-and-shortlist-discipline.md`
- `references/source-traceability-and-claim-citation.md`

### Attach
- current-state verification when current market pricing, current platforms, or current device availability materially affect the answer
- decision utility
- quantitative role labeling when budgets, power estimates, operating costs, scoring, or benchmark performance numbers materially affect the recommendation
- source traceability when specific hardware, pricing, system constraints, or long-run suitability claims carry the conclusion

### Audit
- `checklists/option-selection-final-audit.md`
- `checklists/final-audit.md`

### Visible artifact contract
The final report should visibly show:

- the real purchase or build decision
- dominant household or operator constraints
- workload or operator persona segmentation when the recommendation differs materially by use case
- top recommendation
- credible runner-up
- rejected routes and why
- minimum viable configuration vs recommended configuration when relevant
- budget assumptions, including what is included or excluded
- hardware ↔ system fit
- long-run operating tradeoffs such as power, noise, maintenance, backup, or expansion friction when relevant
- what would change the recommendation

### Hard fail
Fail if the report:

- becomes a broad hardware overview instead of a procurement memo
- names budget bands without clarifying major inclusion / exclusion assumptions
- discusses hardware and systems separately without binding them into a stack recommendation
- treats household operating costs and maintenance friction as side notes instead of ranking variables
- fails to segment by workload or operator persona when materially different use cases would produce materially different recommendations
- uses benchmark performance numbers to determine a recommendation without disclosing metric type or backend
- compares server-side throughput numbers with single-stream desktop tok/s as if they were the same metric

---

## Route: Technical Deep-dive / Architecture Analysis

### Micro-audit focus
For this route, be especially strict about:

- whether the report makes a technical judgment, not just a technical survey
- whether comparison dimensions are explicit when architectures are compared
- whether technical state is current (versions, capabilities, benchmarks)
- whether vendor claims are distinguished from independently verified technical facts
- whether roadmap claims are separated into announced / rumored / speculative

### Trigger
Use when the task is mainly about:

- understanding how a technology works (技术原理分析)
- comparing technical architectures (架构对比)
- evaluating patent portfolios or trends (专利趋势)
- assessing technical feasibility (技术可行性)
- evaluating technology roadmaps (技术路线评估)

**Choose this route when:** the core question is technical judgment — understanding principles (原理), evaluating feasibility, comparing architectures, or assessing technology maturity.

**Do not use this route when:** the task is mainly about selecting a product or vendor (use provider selection or equipment selection), market evolution (use market outlook), or choosing among defined options (use constrained choice).

**Often confused with:** equipment selection / procurement, constrained choice / shortlist, market outlook / industry evolution.

**Route-conflict examples:**
- "Kubernetes vs Docker Swarm architecture" — this is a technical deep-dive if the question is about architectural principles and trade-offs; it becomes constrained choice if the question is "which should I deploy?"
- "Is Rust suitable for systems programming?" — this is a technical feasibility question
- "What does this patent portfolio cover?" — this is a technical deep-dive, not market analysis
- "Which GPU server should I buy?" — this is equipment selection, not technical deep-dive

### Read
- `references/technical-analysis-discipline.md`
- `references/source-traceability-and-claim-citation.md`
- `references/forward-looking-discipline.md` when roadmap evaluation is involved

### Attach
- current-state verification when versions, capabilities, benchmarks, or maturity levels materially affect the answer
- source traceability for technical claims
- forward-looking claims discipline when roadmap evaluation is involved
- quantitative role labeling when benchmarks, performance metrics, or cost comparisons appear

### Audit
- `checklists/technical-analysis-audit.md`
- `checklists/source-traceability.md`
- `checklists/final-audit.md`

### Visible artifact contract
The final report should visibly show:

- **For principle analysis:** core mechanism, key components, fundamental constraints, comparison with alternatives
- **For architecture comparison:** candidate architectures with comparator roles, explicit comparison dimensions, dimension-by-dimension analysis, trade-off summary with load-bearing dimensions identified, conditional recommendation with reversal criteria
- **For feasibility assessment:** what is being attempted, available approaches, evidence of viability, critical unknowns, validation requirements, explicit conclusion (feasible / conditionally feasible / not feasible)
- **For roadmap evaluation:** current state of the art, announced vs. rumored roadmaps, key milestones and dependencies, risk factors, realistic timeline assessment
- **For patent analysis:** patent landscape, technical coverage areas, freedom-to-operate assessment, filing trends
- **For security-sensitive architecture analysis:** assets, trust boundaries, threat actors, attack paths, risk prioritization, engineering controls, detection signals, short/medium/long-term roadmap — see `references/technical-analysis-discipline.md` §Security deep-dive (threat modeling add-on)

### Hard fail
Fail if the report:

- becomes a pure technical survey without judgment or recommendation
- compares architectures without explicit comparison dimensions
- uses stale technical state without verification
- treats vendor claims as confirmed technical facts
- assesses feasibility without evidence of viability
- evaluates roadmaps without separating announced vs. shipped capabilities
- analyzes patents without understanding technical coverage

---

## Route: Listed Company / Investment-style Research

### Micro-audit focus
For this route, be especially strict about:

- whether the opening states the current thesis before long background expansion
- whether the case is driven by a few current load-bearing variables rather than broad company description
- whether support, weakening evidence, and unresolved variables are separated clearly
- whether competition is written as actual thesis pressure rather than peer-directory filler
- whether valuation, growth, strategic narrative, and market position are kept analytically distinct
- whether moat / monopoly / listed-proxy scarcity claims are explicitly separated when defensibility is central to the task

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
- `references/valuation-methodology.md` — read when the report makes valuation judgments, uses target prices, or claims a stock is cheap/expensive/mispriced
- `references/analyst-consensus-handling.md` when consensus data appears (consensus is almost always present in listed-company work)
- `references/reporting-period-handling.md` — read when the report uses reported financials, TTM/NTM figures, or multi-period comparisons (effectively always for listed-company work)
- `references/forward-looking-discipline.md` when forward-looking claims appear
- `references/market-sizing-and-share-discipline.md` when share/size claims matter
- `references/source-traceability-and-claim-citation.md`
- `references/moat-monopoly-screening.md` when the task involves monopoly, irreplaceability, strongest moat, scarce listed assets, or only-listed-proxy judgments
- `examples/listed-company-judgment-memo-example.md` when the report risks drifting into a company overview instead of a judgment memo
- `examples/china-shenhua-reference-grade-rewrite-skeleton.md` when a concrete Chinese listed-company reference shape would help keep the memo judgment-first

### Attach
- current-state verification
- forward-looking claims discipline when forecasts appear
- source traceability
- data conflict resolution when financial data from multiple platforms or sources disagree
- scope completeness when the report makes global market-position or global competitive claims
- decision utility
- sensitivity analysis when valuation, growth assumptions, or financial projections materially affect the investment thesis
- quantitative role labeling when valuation ranges, industry forecasts, or scenario estimates materially affect the investment thesis — see `checklists/quantitative-role-audit.md` §Route-specific checks (Listed Company)

For this route, current-state verification must explicitly lock:

- latest full-year reported period
- latest quarterly / interim reported period
- latest current market snapshot date
- latest management / leadership state when decision-relevant
- whether the opening thesis is anchored on those latest periods rather than on stale-but-plausible background material

### Audit
- `checklists/listed-company-report.md`
- `checklists/source-traceability.md`
- `checklists/final-audit.md`

### Visible artifact contract
The final report should visibly show:

- a judgment-first opening rather than a background-first company overview
- a compact research-anchor block that locks:
  - latest full-year reported period
  - latest quarterly / interim reported period
  - latest current market snapshot date
  - latest management / leadership state when decision-relevant
- current business snapshot
- current financial or market snapshot
- clearly dated key numbers
- separation of reported facts vs estimates
- visible support / weakening evidence / unresolved-variable split for the current thesis
- claim-level traceability for load-bearing claims in the body, not only a bibliography at the end
- risks and counter-evidence
- uncertainty around forward views
- when moat / monopoly / scarcity is central, a visible distinction among:
  - legal or regulatory exclusivity
  - resource or infrastructure control
  - strong moat but still contestable position
  - listed-market proxy scarcity only
- where wording was downgraded because the strongest claim could not be fully verified

### Hard fail
Fail if the report:

- mixes reported metrics and forward estimates without clear labels
- uses undated financial numbers
- research-anchor block is missing entirely, or names a stale or mis-timed time layer — latest full-year, quarterly / interim period, or current market snapshot — and still proceeds as if the memo were current
- lacks a complete market snapshot — missing at least three of: share price with date, market capitalization, PE (TTM/Forward), PB/PS, 52-week range, snapshot date
- makes market-position claims without scope
- lets valuation narrative substitute for business evidence
- treats A-share uniqueness as supply-side monopoly or industry exclusivity
- uses `唯一` / `only` / `永久` / `permanent` / `不可替代` / `irreplaceable` / `>90%` / `无竞争对手` style wording without evidence strong enough for that exact claim strength
- mixes monopoly, moat, market leadership, and listed-proxy scarcity into one undifferentiated scale

---

## Route: Private Company / Startup Evaluation

### Micro-audit focus
For this route, be especially strict about:

- whether the report avoids listed-company valuation methods (PE, PB, DCF) when the company has no public market data
- whether founder-sourced claims are labeled as issuer-sourced rather than confirmed facts
- whether PMF signals are grounded in available evidence rather than assumed from marketing language
- whether source reliability levels are explicit rather than treating all sources as equal
- whether funding and financial data are labeled by source type (company-disclosed / estimated / inferred)

### Trigger
Use when the task is mainly about:

- private / unlisted company analysis
- startup due diligence
- PMF (Product-Market Fit) evaluation
- funding round analysis
- early-stage company assessment
- founder / team evaluation

**Choose this route when:** the core question is evaluating a non-public company's current state, prospects, or investment value.

**Do not use this route when:** the company is publicly listed and trading (use listed-company route). If the company is filing for IPO but not yet listed, use this route but note IPO status.

**Often confused with:** listed-company / investment-style research, first-tier / competitive positioning.

**Key differences from listed-company route:**

- no mandatory financial disclosures → source hierarchy must be redefined
- founder / team background becomes a primary variable (rarely central in listed-company analysis)
- PMF signals, funding trajectory, metric quality become key
- valuation method differs (comparable transactions / latest round / revenue multiples vs PE / DCF)
- source hierarchy differs (Crunchbase, PitchBook, SEC Form D, founder social media vs SEC filings, exchange disclosures)

### Read
- `references/startup-evaluation-discipline.md`
- `references/source-quality.md`
- `references/source-traceability-and-claim-citation.md`
- `references/forward-looking-discipline.md` when forward-looking claims appear

### Attach
- current-state verification (funding status, product stage, team composition)
- source traceability (especially for unverified founder claims)
- forward-looking claims discipline (PMF signals, growth projections, runway estimates)
- quantitative role labeling when ARR/MRR estimates, valuation multiples, or growth projections materially affect the assessment — see `checklists/quantitative-role-audit.md` §Route-specific checks (Startup)
- decision utility when the task carries investment or partnership judgment

### Audit
- `checklists/startup-company-report.md`
- `checklists/source-traceability.md`
- `checklists/final-audit.md`

### Visible artifact contract
The final report should visibly show:

- company overview and stage positioning (what the company does, what stage it is in)
- team assessment (founders, key hires, relevant background)
- product and PMF signals (what exists, what traction is real vs claimed)
- market and competitive position (who they compete with, what advantages exist)
- funding and financial overview (known funding, revenue if disclosed, burn/runway if known — labeled by source type)
- key strengths and risks (specific to this company, not generic startup risks)
- 12-24 month key milestones (what to watch for)
- judgment and recommendation (if applicable, with explicit uncertainty bounds)

### Hard fail
Fail if the report:

- uses PE / PB / PS / DCF as primary valuation framing for a private company without explicit justification
- treats unverified founder claims as confirmed facts
- presents weak or absent financial data as if it were comparable to audited public-company disclosures
- does not label source reliability levels
- writes the report as a mini listed-company analysis with private company data gaps hidden
- uses `唯一` / `only` / `first` / `领先` wording without evidence strong enough for that claim strength

---

## Route: Academic / Literature Review

> ✅ **Hardened route** (Round 3): This route has been validated against 3 real academic research cases and hardened with fillable templates (search strategy, publication bias, source metadata, dual-dimension evidence matrix) and Tier-1 checklist gate (see #175). Reports should now satisfy the academic route's methodology transparency requirements.

### Micro-audit focus
For this route, be especially strict about:

- whether preprints are explicitly distinguished from peer-reviewed publications
- whether evidence is assessed on two dimensions: study design quality AND publication venue prestige
- whether statistical claims include effect sizes and confidence intervals, not just p-values
- whether publication bias or cherry-picking is acknowledged
- whether the search strategy is documented when the review claims completeness
- whether discipline-specific venue prestige is respected (e.g., CS conferences are top-tier venues)

### Trigger
Use when the task is mainly about:

- academic field progress analysis (学术领域进展分析)
- literature review or systematic review (文献综述 / 系统性综述)
- paper comparison or methodological evaluation (论文对比分析)
- technology origin tracing through academic publications (技术溯源)
- research quality assessment (研究质量评估)

**Choose this route when:** the core question is understanding academic evidence, evaluating research quality, or surveying field progress through peer-reviewed literature.

**Do not use this route when:** the task can be adequately answered using the more mature technical deep-dive route (e.g., comparing software architectures, evaluating product feasibility). If the task involves academic evidence but the decision burden is about product selection, vendor choice, or market entry, use those routes and attach academic evidence discipline as a secondary discipline.

**Often confused with:** technical deep-dive / architecture analysis (when technology origin is involved), market outlook / industry evolution (when research trends are involved).

**Route-conflict examples:**
- "What are the key papers on Transformer architecture?" — this is academic route if the goal is literature survey; it becomes technical deep-dive if the goal is understanding how Transformers work for practical application
- "What is the current state of CRISPR research?" — this is academic route if analyzing research progress; it becomes market outlook if analyzing commercial applications
- "Compare the methodologies of these 5 papers on LLM hallucination" — this is academic route, not technical deep-dive

### Read
- `references/academic-evidence-hierarchy.md`
- `references/source-traceability-and-claim-citation.md`
- `references/counter-evidence.md` when the research area is contentious or has conflicting findings

### Attach
- source traceability with academic-specific labeling (publication type, peer-review status, venue)
- current-state verification when the field is fast-moving (e.g., AI/ML, genomics)
- forward-looking claims discipline when research trends or future directions are discussed
- scope completeness when the review claims to cover a broad field

### Audit
- `checklists/academic-analysis-audit.md`
- `checklists/source-traceability.md`
- `checklists/final-audit.md`

### Visible artifact contract
The final report should visibly show:

**For field progress analysis:**
- scope of the review (time period, sub-fields covered, search strategy)
- key research themes and trends
- major breakthroughs and milestones
- current state of the art
- open questions and future directions
- evidence quality assessment

**For paper comparison:**
- comparison dimensions (methodology, dataset, results, limitations)
- paper-by-paper analysis with venue and peer-review status
- cross-cutting themes
- methodological strengths and weaknesses
- recommendations for practitioners

**For technology origin tracing:**
- original seminal work(s) with full citation
- key evolutionary steps
- branching points and divergent approaches
- current dominant paradigm
- competing approaches and their evidence bases

### Hard fail
Fail if the report:

- treats preprints as peer-reviewed without explicit labeling
- cherry-picks papers to support pre-determined conclusions
- infers causation from observational studies without proper caveats
- reports p-values without effect sizes or confidence intervals
- uses outdated research when newer evidence exists without justification
- cites papers without noting publication venue or peer-review status
- ignores publication bias or the "file drawer problem"
- presents a literature survey without distinguishing evidence tiers

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

Read:
- `references/forward-looking-discipline.md`

Visible sign:
- forward-looking claims are labeled by source role and uncertainty

Fail if:
- `预计` / `expected` / `likely` appears without source role or confidence framing

### Quantitative role labeling
Attach when the task uses proxies, scorecards, market sizing, scenario math, or composite scoring.
See `checklists/quantitative-role-audit.md` §Route-specific checks for route-specific BLOCKER/NON-BLOCKER checks.

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

### Scope completeness
Attach when the task claims broad or global scope (global market / industry-wide / full landscape / comprehensive coverage).

Read:
- `references/scope-completeness-discipline.md`

Visible sign:
- the report states its real scope clearly
- load-bearing geographies, segments, or regulatory regimes are covered proportionally to their importance
- scope boundaries are explicit when coverage is partial

Fail if:
- the report is functionally regional while presenting itself as global
- a top-5 geography, major segment, or binding regulatory regime is missing or barely mentioned
- scope boundaries are unstated, creating false confidence in the reader

### Decision utility
Attach when the task carries a recommendation, choice, judgment, or investment-style decision burden.

Visible sign:
- the decision frame is explicit and drives report structure
- load-bearing variables (3-5) are identified and prioritized
- the bottom line is sharp and actionable
- what could change the conclusion is explained

Fail if:
- the report is informative but leaves the reader unsure what to decide
- the conclusion is soft, buried, or missing
- the report answers "what exists" better than "what matters most"

---

## Routing priority

If multiple primary-looking routes apply, use this order:

1. listed-company / investment-style
2. private company / startup evaluation
3. market entry / regional expansion
4. regulatory / policy impact analysis
5. provider / vendor selection
6. first-tier / competitive positioning
7. technical deep-dive / architecture analysis
8. equipment selection / procurement / home-server planning
9. market outlook / industry evolution
10. constrained choice / shortlist
11. academic / literature review

Choose the route that most strongly determines report structure and audit burden.

**Borderline case — private company filing for IPO:** Use private company route if not yet trading. Use listed-company route if trading has begun. Note IPO status explicitly in either case.

**Borderline case — academic vs technical deep-dive:** Use academic route when the core question is about research evidence, methodology, or field progress through literature. Use technical deep-dive when the core question is about how technology works, comparing architectures, or evaluating feasibility — even if academic papers are used as sources.

---

## Final check

Before delivery:

- run `checklists/route-activation-audit.md` when a specialized route was selected
- run `checklists/workflow-spine-audit.md`
- run `checklists/final-audit.md`
- verify that all required audits for the task have been executed, with each audit's run status recorded in the standardized route-and-audit-status block (see `references/report-template.md` §Route and audit status), and each audit's 「证据」column populated with specific section references or register entries per the template's evidence column rules:
  - if a specialized route was selected: for each audit listed in that route's `### Audit` section, confirm its run status: **已通过** (passed), **已跳过（附理由）** (skipped, with documented reason), or **未运行（附理由）** (not run, with documented reason)
  - if no specialized route applies (shared-workflow path): confirm at least `workflow-spine-audit.md` and `final-audit.md` were run, with run status recorded

Then ask (route-selected only — skip these if no specialized route applies):

1. did the correct route fire?
2. did the required secondary disciplines attach?
3. was the route converted into a section-level execution contract early enough to shape the report?
4. is the route visibly executed in the opening, middle, and bottom line of the final artifact?
5. would a reviewer infer the chosen route from the delivered report itself, without hidden notes?

A route only counts if the final report visibly satisfies its artifact contract.

If the route is implicit in reasoning but not visible in delivery, treat that as an execution failure.

If the opening section could be swapped with a generic industry or company overview without materially changing the report, treat that as strong evidence that route execution drift still occurred.
