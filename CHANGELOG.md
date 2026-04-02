# Changelog

All notable changes to this project should be recorded here.

This file is intentionally lightweight. Use concise entries that explain:

- what changed
- why it changed
- what capability or failure mode it affects

## Unreleased

### Added
- `references/failure-taxonomy.md`
- `references/comparative-distillation-method.md`
- `references/option-selection-and-shortlist-discipline.md`
- `evals/rule-activation-and-execution-discipline.md`
- `evals/global-market-scope-completeness-case.md`
- `evals/decision-utility-rubric.md`
- `evals/comparative-distillation-template.md`
- `evals/api-supplier-selection-gpt-vs-minimax-comparative-distillation.md`

### Changed
- `SKILL.md` now adds a delivery-artifact rule: if the user's request includes `pdf`, `PDF`, or `报告`, the workflow should still produce the normal markdown report but also write a `.md` file and run `scripts/md_to_pdf.py` to render a PDF artifact when possible.
- Added `scripts/markdown_to_html.py`, `scripts/render_pdf.py`, and `scripts/md_to_pdf.py` to version the PDF rendering pipeline inside the repo instead of relying only on workspace-root helper scripts.
- The PDF renderer styles were substantially upgraded: lighter cover design, cleaner heading hierarchy, improved table spacing/borders, better code/callout/blockquote styling, and proper markdown list rendering for `ul/ol` blocks.
- `scripts/markdown_to_html.py` now performs pre-render text normalization for PDF safety, including control-character cleanup, unicode normalization, and partial repair of spurious CJK spacing artifacts from poor upstream text extraction.
- `scripts/render_pdf.py` now exposes more print-oriented controls (`--landscape`, `--media`, explicit page margins, CSS page-size preference, title override) instead of acting as a minimal one-shot wrapper.
- `scripts/md_to_pdf.py` now forwards those print controls through the one-shot pipeline so the markdown→PDF path can be tuned without patching code.
- The PDF CSS is now split into a base layer plus a report theme layer, making later theme iteration easier without collapsing all print styling into one monolithic block.
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
- `SKILL.md` final discipline now adds a visible-gate check and routes rule-execution failures to `evals/rule-activation-and-execution-discipline.md`.
- `SKILL.md` final trigger checks now require provider-selection outputs to show current provider snapshot + accessibility/compliance/SLA/data-control constraints as ranking logic when relevant.
- `references/option-selection-and-shortlist-discipline.md` now includes provider-selection heuristics for current model/API family, stale-anchor avoidance, and mainland-access / data-residency / SLA-sensitive ranking.
- `references/decision-report-template.md` now explicitly adapts its structure for option-selection and shortlist tasks, including ranked shortlist flow, aggregation visibility, and change-the-ranking conditions.
- `references/decision-report-template.md` now includes a stronger provider-selection structure with decision architecture, current snapshot table, ranked shortlist, and deployment archetypes.
- `checklists/option-selection-final-audit.md` now includes a provider/vendor current-state gate covering current model family, pricing units, accessibility, data residency, and SLA/status checks.
- `checklists/final-audit.md` now requires a provider snapshot and ranking-level treatment of accessibility/compliance/data-residency/SLA for model/API supplier decisions.

### Why
- The eval set has grown enough that recurring patterns now matter more than single-case accumulation.
- A taxonomy makes it easier to decide whether a new report failure needs a new rule, a stronger checklist gate, a trigger-routing fix, or only another case file.
- Current evidence shows that several failures are no longer "missing rule" problems but "rule activation / execution" problems; documenting that distinction is now important.
- Three next-step eval artifacts were added to turn the taxonomy into execution guidance: one for rule activation failures, one for global scope-completeness failures, and one for decision-support quality beyond generic depth.
- Comparative distillation needed to become a repeatable method rather than an ad-hoc discussion, so the repo now includes both a method file and a working template for paired-report comparisons.
- The weekend destination comparison case exposed a broader missing-rule area: the repo needed general guidance for constrained choice, shortlist construction, multi-origin aggregation, and choice architecture beyond travel-specific prompting.
- A new model/API supplier selection case exposed a more specific failure family inside constrained-choice work: stale current-state anchors, provider-encyclopedia drift, and failure to treat mainland accessibility / compliance / SLA as ranking variables.
- The skill itself needed to consume those additions through clearer routing, otherwise the new evals would remain documentation instead of affecting execution.

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
- `evals/finance-and-market-share-cambricon-case.md`
- `evals/ranking-and-current-claims-xiaomi-update-case.md`
- `evals/depth-rubric.md`
- `evals/moore-threads-listing-status-case.md`
- `evals/source-traceability-moore-threads-case.md`
- `evals/apple-product-and-valuation-case.md`
- `evals/apple-product-roadmap-and-investment-case.md`
- `evals/industry-landscape-depth-case.md`
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
- `evals/freshness-xiaomi-case.md`

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
- `evals/current-state-checks.md`

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
3-30

### Added
- Initial project scaffold
- `SKILL.md`
- `README.md`
- `references/` directory
- `examples/` directory
- `evals/` directory
