# Changelog

All notable changes to this project should be recorded here.

This file is intentionally lightweight. Use concise entries that explain:

- what changed
- why it changed
- what capability or failure mode it affects

## Unreleased

### Changed
- `equipment selection / procurement / home-server planning` promoted to first-class route (routing priority #5), with provider-vs-equipment conflict rules and route-conflict examples
- route lists in `ARCHITECTURE.md`, `SYSTEM-MAP.md`, and `README.md` updated from six to seven mature routes

### Added
- `references/mid-research-review.md`
- `checklists/mid-research-review-audit.md`
- `references/quantitative-role-labeling.md`
- `checklists/quantitative-role-audit.md`
- `references/research-pack-contract.md`
- `schemas/research-pack.md`
- `examples/research-pack-example.md`
- `scripts/validate_research_pack.py`
- `ARCHITECTURE.md`
- `SYSTEM-MAP.md`
- `ROUTING-MATRIX.md`
- `references/failure-taxonomy.md`
- `references/comparative-distillation-method.md`
- `references/option-selection-and-shortlist-discipline.md`
- `references/market-outlook-and-scenario-discipline.md`
- `evals/meta/rule-activation-and-execution-discipline.md`
- `evals/cases/global-market-scope-completeness-case.md`
- `evals/templates/decision-utility-rubric.md`
- `evals/templates/comparative-distillation-template.md`
- `evals/comparative-distillation/api-supplier-selection-gpt-vs-minimax-comparative-distillation.md`
- `evals/comparative-distillation/ai-coding-agent-market-outlook-gpt-vs-minimax-comparative-distillation.md`
- `evals/comparative-distillation/sea-market-entry-gpt-vs-minimax-comparative-distillation.md`
- `evals/comparative-distillation/multi-origin-meetup-city-selection-gpt-vs-minimax-comparative-distillation.md`
- `evals/cases/cambricon-first-tier-positioning-case.md`
- `evals/cases/cambricon-evidence-weighting-and-traceability-case.md`

### Changed
- Added explicit mid-research review discipline so early evidence batches must visibly narrow, redirect, continue, or stop the search path.
- Strengthened counter-evidence discipline by tying it to load-bearing conclusions rather than generic end-of-report risk language.
- Hardened final-audit expectations around weakening logic and intentional stopping behavior.
- Separated quantitative role labeling into an explicit shared discipline for load-bearing numbers.
- Added route-level attachment guidance where numeric claims materially shape recommendation, ranking, timing, valuation, or confidence.
- Hardened report templates so modeled, assumed, and proxied numbers are less likely to read as confirmed facts.
- Introduced a minimal Research Pack contract as lightweight process-artifact support for auditability.
- Clarified that final delivery alone is not always sufficient for route-heavy or high-burden tasks.
- Added a compact bridge between workflow discipline and future execution-layer binding.
- Organized `evals/` by subtype for easier navigation and maintenance.
- Added compact examples showing expected execution shape for major memo families.
- Clarified that examples are execution references rather than report archives.
- Added explicit route preflight discipline so route selection becomes an auditable entry-layer step rather than an implicit judgment.
- Strengthened routing language so final artifacts must visibly execute the selected route rather than merely name it.
- Clarified route-execution failure signs and route-activation intervention order.
- `scripts/markdown_to_html.py` table routing now keeps comparison-heavy blocks in compact tables (including anchor-column split sub-tables) instead of leaking toward vertical card-like degradation; it also strips internal render-hint text from final HTML.
- `scripts/markdown_to_html.py` pre-parse table repair now strips accidental list-prefix injection before headings/table rows (e.g. `- ##` / `- | ...`), normalizes malformed separator rows, and removes stray leading bullet-placeholder columns (e.g. `| - | # | ...`) before markdown parsing.
- `scripts/markdown_to_html.py` table sanitization now more aggressively removes placeholder headers/columns and URL-heavy split-off metadata columns when they reduce comparison readability.
- PDF table CSS now improves pagination and scan quality for source/info tables: header rows are repeated as table headers across page breaks, row splitting is reduced, and long URLs use softer wrap behavior to avoid severe character fragmentation.
- `ARCHITECTURE.md` now describes the repo as a layered system: workflow spine, routing layer, method/discipline layer, audit layer, eval/regression layer, and delivery/rendering layer.
- `SYSTEM-MAP.md` now groups the current references, checklists, and evals into practical families and explains which layer should usually change first when a failure appears.
- `README.md` now acts more clearly as a lightweight navigation page: core entry files, supporting directories, how the repo fits together, and how changes should land, rather than a long mixed catalog of representative assets.
- `SKILL.md` now acts more clearly as the workflow spine and orchestration layer rather than the single file that carries every mature route-specific trigger; task-family routing is now centralized in `ROUTING-MATRIX.md`.
- `ROUTING-MATRIX.md` now defines the six most mature task families (provider selection, market entry, market outlook, first-tier positioning, constrained choice, listed-company research), their required attached disciplines, their required audits, and the visible artifact contracts that final reports must satisfy.
- `SKILL.md` now adds a delivery-artifact rule: if the user's request includes `pdf`, `PDF`, or `报告`, the workflow should still produce the normal markdown report but also write a `.md` file and run `scripts/md_to_pdf.py` to render a PDF artifact when possible.
- Added `scripts/markdown_to_html.py`, `scripts/render_pdf.py`, and `scripts/md_to_pdf.py` to version the PDF rendering pipeline inside the repo instead of relying only on workspace-root helper scripts.
- The PDF renderer styles were substantially upgraded: lighter cover design, cleaner heading hierarchy, improved table spacing/borders, better code/callout/blockquote styling, and proper markdown list rendering for `ul/ol` blocks.
- `scripts/markdown_to_html.py` now performs pre-render text normalization for PDF safety, including control-character cleanup, unicode normalization, and partial repair of spurious CJK spacing artifacts from poor upstream text extraction.
- `scripts/render_pdf.py` now exposes more print-oriented controls (`--landscape`, `--media`, explicit page margins, CSS page-size preference, title override) instead of acting as a minimal one-shot wrapper.
- `scripts/md_to_pdf.py` now forwards those print controls through the one-shot pipeline so the markdown→PDF path can be tuned without patching code.
- The PDF CSS is now split into a base layer plus a report theme layer, making later theme iteration easier without collapsing all print styling into one monolithic block.
- `scripts/markdown_to_html.py` no longer relies primarily on a hand-rolled block parser for headings/lists/tables/quotes; it now uses the installed `python-markdown` library for core markdown→HTML conversion, then applies report-specific post-processing. This fixes the major failure mode where raw markdown syntax (`##`, `---`, `|`, `>`) leaked into generated PDFs.
- Added a stronger pre-parse normalization and repair pass for messy LLM markdown: block-safe normalization around headings / horizontal rules / quotes / tables / lists, stronger CJK spacing repair for headings and metadata-like lines, and a markdown-table repair pass that inserts or normalizes separator rows and aligns column counts before handing content to the parser.
- Very dense multi-column tables are now transformed into PDF-friendly card/list blocks instead of always being rendered as literal HTML tables. This trades spreadsheet fidelity for readability in report PDFs, especially for market-structure and catalyst/risk sections.
- The print CSS now uses a more opinionated CJK-oriented font stack and stricter line-breaking / spacing defaults to reduce the “characters visually torn apart” look in Chinese-heavy report PDFs.
- `README.md` now points to the failure-taxonomy document so the current eval set can be interpreted as recurring failure families rather than a flat list of isolated cases.
- `README.md` now describes `evals/` as containing case evals, rubrics, and meta-evals rather than only lightweight prompts.
- `README.md` now points to the comparative-distillation method as the standard way to turn paired-report comparisons into reusable improvements.
- `README.md` now points to a general option-selection and shortlist-discipline reference for constrained choice tasks.
- `README.md` now also calls out provider-selection/current-state work as a first-class evaluation target.
- `ROADMAP.md` now calls out possible formalization of eval subtypes (`case`, `rubric`, `distillation`, `meta-eval`).
- `ROADMAP.md` now calls for 2-3 more real comparative-distillation cases before promoting candidate rules too aggressively.
- `SKILL.md` now includes explicit trigger routing for listed-company, current-state, source-traceability, forward-looking, global-scope, decision-utility, and option-selection/shortlist cases instead of leaving those gates implicit.
- `SKILL.md` now routes paired-report comparison work to the comparative-distillation method and template so stronger-vs-weaker report comparisons produce explicit action types.
- `SKILL.md` now explicitly treats model/API supplier selection as both a current-state-sensitive task and a constrained-choice task, requiring a current provider snapshot before ranking.
- `SKILL.md` now explicitly routes market-entry / regional-expansion / country-prioritization tasks as constrained-choice + decision-memo work, requiring priority-vs-alternatives, country shortlist, sequencing, and hard-gate logic rather than a market overview.
- `SKILL.md` final discipline now adds a visible-gate check and routes rule-execution failures to `evals/meta/rule-activation-and-execution-discipline.md`.
- `SKILL.md` final trigger checks now require provider-selection outputs to show current provider snapshot + accessibility/compliance/SLA/data-control constraints as ranking logic when relevant.
- `SKILL.md` final trigger checks now also require market-entry outputs to show priority-vs-alternatives, country shortlist, hub vs beachhead vs later-expansion distinctions when relevant, hard gates, and sequencing logic.
- `SKILL.md` now explicitly routes first-tier / top-tier / multidimensional competitive-positioning tasks as definition-sensitive constrained judgments rather than loose ranking language.
- `references/ranking-and-current-claims-discipline.md` now adds multi-dimensional tiering discipline, dimension-collapse warnings, an overall-label gate, and stronger weighting guidance for direct evidence vs inference.
- `references/decision-report-template.md` now includes a stronger structure for first-tier / top-tier / multidimensional positioning memos.
- `checklists/final-audit.md` now adds first-tier / top-tier delivery gates so reports must show scope / metric / timeframe / dimension-level conclusions before any overall prestige label.
- `SKILL.md` now also routes mixed-evidence dimension-by-dimension judgments into source-traceability discipline with explicit evidence-weight separation for load-bearing claims.
- `references/source-traceability-and-claim-citation.md` now adds a mixed-evidence weighting section for tier / positioning memos so traceability does not stop at bibliography theater.
- `checklists/source-traceability.md` now requires load-bearing positioning judgments to show direct-evidence-vs-inference weighting in the body and prevents self-tests / roadmap reporting / valuation signals from silently carrying primary-evidence weight.
- `references/report-template.md` now adds a required load-bearing evidence note for mixed-evidence positioning judgments.
- `scripts/markdown_to_html.py` now uses stricter CJK-friendly line-breaking defaults (`word-break: keep-all`, `overflow-wrap: normal`, `text-autospace: no-autospace`) for body text and comparison blocks to reduce the broken-export / torn-character feel in Chinese PDFs.
- `scripts/markdown_to_html.py` text normalization now more aggressively repairs broken CJK spacing around punctuation and separators (including `%`, `·`, `—`, `…`) before markdown parsing.
- `references/option-selection-and-shortlist-discipline.md` now includes provider-selection heuristics for current model/API family, stale-anchor avoidance, and mainland-access / data-residency / SLA-sensitive ranking.
- `references/decision-report-template.md` now explicitly adapts its structure for option-selection and shortlist tasks, including ranked shortlist flow, aggregation visibility, and change-the-ranking conditions.
- `references/decision-report-template.md` now includes a stronger provider-selection structure with decision architecture, current snapshot table, ranked shortlist, and deployment archetypes.
- `references/decision-report-template.md` now includes a dedicated market-entry structure with recommendation, why-now/why-not-now, hard gates, country shortlist, sequencing, entry archetypes, and 0-12 month milestones/KPIs.
- `references/decision-report-template.md` now strengthens option-selection structure with explicit decision architecture, shortlist-construction visibility, quantitative-role labeling, runner-up credibility, and ranking-reversal conditions.
- `checklists/option-selection-final-audit.md` now includes a provider/vendor current-state gate covering current model family, pricing units, accessibility, data residency, and SLA/status checks.
- `checklists/option-selection-final-audit.md` now includes a market-entry / regional-expansion gate for explicit go/not-now/phased-entry calls, country comparison units, hard gates, and sequencing-change conditions.
- `checklists/option-selection-final-audit.md` now also requires role-labeling of quantitative inputs (observed fact / proxy / assumption / model output), explicit fairness-measure visibility, and surfacing of hidden operational burden layers when they affect constrained-choice rankings.
- `checklists/final-audit.md` now requires a provider snapshot and ranking-level treatment of accessibility/compliance/data-residency/SLA for model/API supplier decisions.
- `checklists/final-audit.md` now adds market-entry gates for priority-vs-alternatives, shortlist/sequencing logic, and hub-vs-beachhead separation when relevant.
- `checklists/final-audit.md` now adds market-outlook gates for current market snapshot, drivers/blockers/scenarios/stakeholder implications, and explicit labeling of outlook numbers when evidence role matters.
- `checklists/final-audit.md` now also requires constrained-choice reports with composite scoring to label key quantitative inputs by evidence role when that distinction affects trust in the recommendation.
- `checklists/final-audit.md` now hardens market-entry audit gates around explicit `go` / `not now` / `pilot only` / `phased entry` resolution, visible why-this-option-wins logic, KPI/milestone triggers, and ranking-change conditions.
- `checklists/final-audit.md` now explicitly treats mixed evidence-layer vs modeling-layer labeling as an audit issue, so reports do not stop at `confirmed / inference / unknown` when important numbers are really proxies, assumptions, or planning-model outputs.
- `checklists/final-audit.md` now adds a target-language coherence gate: Chinese final reports should use Chinese load-bearing structural labels unless bilingual output was explicitly requested, and mixed-language evidence buckets count as a delivery failure.

### Why
- A real MiniMax SEA memo PDF failure showed five delivery-layer issues that must be handled in rendering: comparison tables degrading in structure, source tables breaking poorly across pages, internal generator hints leaking into final output, placeholder/header residues, and poor horizontal-space usage.
- A new AI coding agent market-outlook comparative case showed that market/industry-evolution tasks were still too prone to overview drift; the repo needed explicit market-outlook routing, scenario discipline, and stakeholder-action structure.
- Repeated PDF export failures also showed a separate rendering failure family: comparison-heavy sections were degrading into tall vertical card stacks, placeholder fields like `#1 / —` could leak into the final PDF, and list/callout semantics were still bleeding into each other in the generated HTML.
- The eval set has grown enough that recurring patterns now matter more than single-case accumulation.
- A taxonomy makes it easier to decide whether a new report failure needs a new rule, a stronger checklist gate, a trigger-routing fix, or only another case file.
- Current evidence shows that several failures are no longer "missing rule" problems but "rule activation / execution" problems; documenting that distinction is now important.
- Three next-step eval artifacts were added to turn the taxonomy into execution guidance: one for rule activation failures, one for global scope-completeness failures, and one for decision-support quality beyond generic depth.
- Comparative distillation needed to become a repeatable method rather than an ad-hoc discussion, so the repo now includes both a method file and a working template for paired-report comparisons.
- The weekend destination comparison case exposed a broader missing-rule area: the repo needed general guidance for constrained choice, shortlist construction, multi-origin aggregation, and choice architecture beyond travel-specific prompting.
- A new model/API supplier selection case exposed a more specific failure family inside constrained-choice work: stale current-state anchors, provider-encyclopedia drift, and failure to treat mainland accessibility / compliance / SLA as ranking variables.
- A new SEA market-entry paired case exposed another constrained-choice failure family: expansion memos can still drift into regional overviews unless the skill forces priority-vs-alternatives, country-shortlist logic, sequencing, and hard gates.
- The GPT side of that SEA case also exposed a delivery-layer failure: citation / retrieval artifacts can leak into an otherwise strong memo, so final-delivery cleanliness must be treated as a hard gate rather than a cosmetic issue.
- A new multi-origin meetup-city paired case exposed a different constrained-choice execution gap: reports can know they are doing selection work yet still hide quantitative-role labeling, fairness measurement, shortlist-construction logic, and ranking-reversal conditions.
- A new Cambricon first-tier positioning case exposed another ranking failure family: reports can define multiple dimensions and still collapse them into a polished but weakly-auditable prestige label, especially when global vs domestic scope, current vs roadmap products, and direct evidence vs inference are mixed.
- The same Cambricon case also exposed an auditability gap: even when reports label confirmed facts, inference, and uncertainty, they may still fail to show which load-bearing claims are direct-evidence-backed versus inference-heavy, creating source-rich but weakly-auditable conclusions.
- Repeated MiniMax PDF samples still showed a broken-export feeling in Chinese text texture, so the rendering layer needed another narrow CJK-spacing pass separate from research-discipline changes.
- The skill itself needed to consume those additions through clearer routing, otherwise the new evals would remain documentation instead of affecting execution.
- The routing surface had become too diffuse inside `SKILL.md`; a dedicated routing contract was needed so mature task families could be activated, reviewed, and audited more explicitly.
- After the routing layer was separated, the repo also needed a lightweight architecture note so future changes can land in the right layer instead of expanding `SKILL.md` again by default.

## 0.4.0 - 2026-03-31

### Added
- `references/parallel-research.md`

### Changed
- `references/parallel-research.md` now includes a **Batch parallelism (rate-limit safe)** section with a max-2-concurrent rule to prevent MiniMax API 429 errors during parallel track execution.

### Why
- During a real deep-research session, running 3-4 parallel sub-agent tracks simultaneously caused multiple concurrent `web_search` calls that exceeded MiniMax's search API concurrency limit, resulting in 429 errors and track failures.
- The fix uses batch parallelism: at most 2 tracks run concurrently; remaining tracks wait for the current batch to finish before spawning. This keeps total research time near-optimal (~2× single-track) without hitting rate limits.
- 4 tracks → two batches (2+2); 3 tracks → two batches (2+1); 1 track → direct run.

### Process
- Fix was identified from a real production failure during a live Minimax research session.
- Changelog entry and branch/PR workflow followed the repo's agreed-upon maintenance discipline.

### Added
- `references/market-sizing-and-share-discipline.md`
- `references/ranking-and-current-claims-discipline.md`
- `references/research-depth-rubric.md`
- `references/corporate-status-and-listing-state-discipline.md`
- `references/source-traceability-and-claim-citation.md`
- `evals/cases/finance-and-market-share-cambricon-case.md`
- `evals/cases/ranking-and-current-claims-xiaomi-update-case.md`
- `evals/templates/depth-rubric.md`
- `evals/cases/moore-threads-listing-status-case.md`
- `evals/cases/source-traceability-moore-threads-case.md`
- `evals/cases/apple-product-and-valuation-case.md`
- `evals/cases/apple-product-roadmap-and-investment-case.md`
- `evals/cases/industry-landscape-depth-case.md`
- `checklists/listed-company-report.md`
- `checklists/source-traceability.md`
- `checklists/forward-looking-claims.md`
- `checklists/final-audit.md`

### Changed
- `SKILL.md` now routes market-size and market-share style work to dedicated sizing/share-discipline guidance.
- `SKILL.md` now routes ranking, category-leadership, and current-position claims to dedicated ranking/current-claims discipline guidance.
- `SKILL.md` now routes changing company capital-markets status questions to dedicated listing-state discipline guidance.
- `SKILL.md` now routes structured claim reports and investment memo outputs to source-traceability guidance.
- `SKILL.md` no longer contains dangling references to missing parallel-research, subagent-orchestration, and evidence-log-template files.

### Why
- A real Cambricon report example exposed pseudo-precision around market-share estimates, weak mapping between company data and market-size claims, and insufficient numeric discipline in company/sector research.
- An updated Xiaomi report showed improved freshness but still over-assertive ranking/current-position claims that needed stronger time/source/category discipline.
- Real-case iteration showed that factual checking alone is not enough; the repo also needs a reusable way to score research depth and breadth.
- A Moore Threads report exposed another failure mode: freezing a company's capital-markets state at IPO-filing / Pre-IPO language instead of verifying the actual current listing status.
- A later Moore Threads report showed the model had improved source awareness but still lacked claim-level traceability — sources appeared at the end but no inline citations existed, making conclusions unauditable.
- An Apple report exposed two additional failure modes: (1) using stale product generations as current when iPhone 17, M5, and Apple Watch 11 have all shipped, and (2) omitting current valuation snapshot entirely for a listed-company investment memo.
- A later Apple product roadmap + investment analysis report showed source traceability was still missing, forward-looking claims lacked reasoning chains, marketing language was not separated from facts, and product analysis was mixed with investment advice without proper boundaries.
- An AI industry value-chain report exposed a different depth failure mode: broad coverage and plausible synthesis, but still more like a high-quality landscape briefing than true deep research with prioritized variables, value-accrual analysis, and counter-evidence.
- After systematic review, the skill had grown to the point where key execution rules (listed-company fields, source traceability, forward-looking claims, final audit) were buried in prose and not reliably enforced. Four execution-time checklists were added as a lightweight anti-forgetting structure: each replaces prose guidance with a concrete run-before-delivery checklist.

### Process
- Future meaningful repo changes should include:
  - a focused commit
  - a changelog update for notable behavior changes
  - an eval addition/update when fixing a real failure mode

## 0.3.0 - 2026-03-30

### Added
- `references/finance-date-discipline.md`
- `evals/cases/freshness-xiaomi-case.md`

### Changed
- `SKILL.md` now routes company/investment-style work to finance/date-discipline guidance.
- `SKILL.md` now requires a clearer current snapshot split for fast-moving company or investment research.

### Why
- A real Xiaomi report example exposed stale product-line facts and weak time-layering between historical, current, and forward-looking numbers.

## 0.2.0 - 2026-03-30

### Added
- `references/current-state-verification.md`
- `references/counter-evidence.md`
- `references/decision-report-template.md`
- `references/claim-matrix.md`
- `references/task-types.md`
- `examples/freshness-failure-cases.md`
- `evals/meta/current-state-checks.md`

### Changed
- `SKILL.md` was upgraded to a deep-only protocol with explicit current-state verification and decision-oriented synthesis.

### Why
- The project moved from a generic research workflow toward a more structured deep-research protocol with stronger freshness, uncertainty, and decision-support discipline.

## 0.1.0 - 2026-03-30

### Added
- Initial project scaffold
- `SKILL.md`
- `README.md`
- `references/` directory
- `examples/` directory
- `evals/` directory
