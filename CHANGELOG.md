# Changelog

All notable changes to this project should be recorded here.

This file is intentionally lightweight. Use concise entries that explain:

- what changed
- why it changed
- what capability or failure mode it affects

## Unreleased

### Added
- `references/technical-analysis-discipline.md`: new discipline file for technical analysis tasks — covers principle analysis, architecture comparison, patent analysis, feasibility assessment, and roadmap evaluation. Includes comparison dimensions, maturity assessment frameworks (TRL, adoption lifecycle), and common failure modes (#116).
- `checklists/technical-analysis-audit.md`: new checklist for technical deep-dive route — verifies route activation, technical state verification, evidence quality, comparison structure, feasibility assessment, maturity assessment, and judgment quality (#116).
- `evals/cases/technical-analysis-kubernetes-vs-docker-case.md`: new eval case for technical deep-dive routing — tests whether the skill correctly activates the technical deep-dive route for architecture comparison tasks and produces a report that satisfies the artifact contract (#116).
- `ROUTING-MATRIX.md`: added Technical Deep-dive / Architecture Analysis as a first-class route with trigger, artifact contract, hard-fail conditions, and routing priority (#116).
- `SYSTEM-MAP.md`: added technical deep-dive to Family B supported mature routes list (#116).
- `ARCHITECTURE.md`: added technical deep-dive to first-class routes list (#116).
- `ROADMAP.md`: added technical deep-dive route validation task to P1 remaining priorities (#116).

### Changed
- `ROUTING-MATRIX.md`: updated routing priority from 7 to 8 routes — technical deep-dive inserted at position 5 (after first-tier positioning, before equipment selection) (#116).

### Why
- Per issue #116, technical analysis tasks (principle analysis, architecture comparison, patent analysis, feasibility assessment, roadmap evaluation) lacked a dedicated route. These tasks were being routed to generic research or adjacent routes (equipment selection, constrained choice), producing reports with wrong structure. The new technical deep-dive route provides explicit trigger conditions, artifact contract, and hard-fail conditions for technical judgment tasks.

### Added
- `references/data-conflict-resolution.md`: added Chinese-language source mapping table (Tier 1–6) for common Chinese sources (东方财富, Wind, 财新, 36氪, 雪球, etc.) and cross-language conflict trigger in "When to apply" section (#125).
- `references/source-quality.md`: added cross-language conflict rules section — 4 common patterns (filing vs filing, filing vs aggregator, media vs media, specificity priority) with language-neutral credibility guidance (#125).
- `checklists/final-audit.md`: added NON-BLOCKER check item for cross-language source conflict handling when Chinese and English sources coexist (#125).
- `evals/cases/cjk-pdf-validation-input-company-case.md`, `evals/cases/cjk-pdf-validation-input-market-case.md`: Chinese-heavy test markdown files (5,000+ CJK chars each) for PDF rendering validation (#100).
- `evals/cases/cjk-pdf-validation-findings-case.md`: validation findings for Chinese-heavy PDF rendering (#100). Uncovered and fixed two pipeline bugs (see Changed).
- `evals/comparative-distillation/candidate-rule-registry.md`: comprehensive cross-case candidate tracking for all 11 comparative distillation files. Extracts all 60 candidate rules, maps each to existing checklist/reference coverage, and identifies recurring patterns. Finding: zero uncovered PROMOTE_NOW candidates — the existing skill system has already absorbed lessons from all 11 cases. See issue #96 for context.
- `checklists/final-audit.md`: added delivery-time gate for market-outlook forward-looking claims — source role + time basis for all claims; assumption chain + failure condition for derived/modeled/load-bearing forecasts (validated against 3 real cases, see `report/validation-analysis.md`).
- `checklists/workflow-spine-audit.md`: Family A checklist — audits whether the SKILL.md shared workflow spine was actually executed rather than assumed.
- `checklists/route-activation-audit.md`: Family B checklist — audits whether route activation was explicit and whether the route actually shaped the output.
- `references/forward-looking-discipline.md`: Family E reference — dedicated discipline for forecasts, estimates, roadmap statements, announced-vs-rumored separation, and forward-looking assumption chains.
- `references/delivery-operator-note.md`: Family H reference — operator-facing note on the rendering pipeline, known failure patterns, CJK concerns, and pre-delivery checks.
- `references/valuation-methodology.md`: P2 reference — valuation methodology selection, metric choice logic, precision downgrade rules for cyclical/loss-making/high-growth companies, target price discipline.
- `references/analyst-consensus-handling.md`: P2 reference — consensus data handling: source/date/coverage metadata, estimate vs target price vs rating distinction, stale consensus detection.
- `references/reporting-period-handling.md`: P2 reference — reporting-period definitions: FY vs CY, TTM/LTM/NTM, preliminary/unaudited/restated, post-period events.
- `evals/cases/consensus-and-forward-pe-misuse-case.md`: eval testing consensus target price as fair value, forward PE as reported fact, and stale consensus after earnings.
- `evals/cases/reporting-period-and-ttm-confusion-case.md`: eval testing TTM vs fiscal year confusion, preliminary vs audited, and restated figures.
- `evals/meta/scope-completeness-discipline.md`: Family F meta-eval — root-cause diagnosis for scope-completeness failures (missing rule / missing trigger / route misclassification / execution failure / data unavailability).
- `evals/meta/decision-utility-discipline.md`: meta-eval for decision-utility failures — root-cause diagnosis (missing route / weak contract / template gap / execution failure / wrong route). Distinguishable from `evals/templates/decision-utility-rubric.md` (scoring tool) by focus on "which repo layer should change".
- `references/scope-completeness-discipline.md`: reusable minimum-coverage standard for global/comprehensive claims — geography coverage matrix, common failure patterns, acceptable partial scope rules.
- `ROUTING-MATRIX.md`: added scope completeness and decision utility as cross-cutting disciplines with attach triggers, visible signs, and hard-fail conditions.
- `ROUTING-MATRIX.md`: wired scope completeness and decision utility into relevant route `### Attach` lists (provider/vendor selection, market entry, market outlook, first-tier positioning, constrained choice, equipment selection, listed-company).
- `SKILL.md`: added scope completeness and decision utility to core shared disciplines list.
- `checklists/route-activation-audit.md`: added visible-execution checks for scope completeness and decision utility.
- `checklists/final-audit.md`: added recall-discipline entries for scope completeness and decision utility.

### Added — Decision tree / consequence mapping method (#124)
- `references/decision-tree-method.md`: new reference for structured post-decision branch planning. Covers when to use, core 3-branch structure (success / blocked / all-blocked), output format, relationship to existing disciplines (change-the-conclusion, sensitivity analysis, market-outlook scenarios), and common failure modes.
- `references/option-selection-and-shortlist-discipline.md`: added cross-reference to decision-tree-method.md in Step 7 (scenario logic).
- `checklists/option-selection-final-audit.md`: added NON-BLOCKER check for post-decision branch with trigger condition and monitoring signal when execution uncertainty is major.

### Added — Sensitivity analysis enhancement (#119)
- `references/quantitative-role-labeling.md`: enhanced assumption chain template with sensitivity classification (low / medium / high), test amplitude guidance (±20%, ±50%, extreme scenarios), and structured output format for sensitivity tables.
- `checklists/quantitative-role-audit.md`: added sensitivity analysis checklist — BLOCKER checks for high-sensitivity assumption classification and visible sensitivity tables; NON-BLOCKER checks for tipping points and load-bearing variable identification.
- `ROUTING-MATRIX.md`: wired sensitivity analysis into market entry, market outlook, and listed-company routes as an attached discipline when numerical assumptions materially affect the conclusion.
- `SYSTEM-MAP.md`: updated Family D2 (Quantitative role clarity) to include sensitivity analysis failure signs and intervention guidance.

### Changed
- `scripts/markdown_to_html.py`: fixed two CJK normalization bugs found during validation:
  - CJK spacing regexes used `\s+` which matched across newlines, merging headings with body paragraphs. Changed to `[ \t]+` (horizontal whitespace only).
  - `unicodedata.normalize('NFKC', ...)` degraded Chinese fullwidth punctuation (（）→(), ，→,) to ASCII. Changed to `NFC` to preserve CJK punctuation.
- `scripts/test_cjk_pdf_pipeline.py`: added dedicated verification script covering block structure integrity, Chinese punctuation fidelity, and same-line CJK spacing (6 tests).
- `.gitignore`: narrowed PDF/HTML exclusion to `evals/cases/*.pdf` and `evals/cases/*.html` to avoid hiding future non-generated files.
- `ROADMAP.md`: updated P2 CJK validation item — found and fixed two pipeline bugs; not yet marked complete (remaining: more report types, CI gate).
- `evals/cases/cjk-pdf-validation-findings-case.md`: updated to document bugs discovered, fixes applied, and remaining limitations.
- `references/failure-taxonomy.md`:
  - Family E: added decision-utility rubric and meta-eval to existing evals; updated priority direction from "add evaluation" to "checklist-level gate / route activation hardening".
  - Family F: added `references/scope-completeness-discipline.md` and updated coverage status; updated priority direction from "dedicated eval" to "route-trigger consistency / final-audit recall".
  - "What this taxonomy implies should happen next": marked scope-completeness eval and decision-utility rubric as done, with remaining next steps documented.
  - Short classification table: updated Family F and Meta-Rule-Activation status to reflect current coverage.
- `SYSTEM-MAP.md`: mapped `evals/meta/scope-completeness-discipline.md` and `evals/meta/decision-utility-discipline.md` to Family G.
- `ROADMAP.md`: split P1 meta-eval item into completed (scope/decision meta-evals + route discipline) and remaining (checklist gate / market-outlook validation / remaining route hardening).
- `SYSTEM-MAP.md`: filled family-level coverage across all nine families: added missing file references (`mid-research-review.md`, `route-activation-and-preflight.md`), added newly created checklists, split combined Primary references/checklists sections into separate subsections for clarity, and updated Current thin spots to reflect resolved items.
- `SKILL.md`: narrowed PDF delivery trigger — replaced bare keyword matching with an explicit file-delivery intent model: added delivery-phrase list ("生成 PDF", "导出 PDF", "报告文件", "可下载报告", "给我报告文件", "作为附件给我" etc.) and a negation/discussion guardrail (不要 PDF, no PDF, 解释 PDF 渲染失败, etc.). Bare `报告` no longer triggers PDF pipeline.
- `evals/cases/pdf-delivery-trigger-regression-case.md`: added acceptance matrix to prevent trigger-boundary drift.
- `scripts/validate_research_pack.py`: added `## Stop condition` to required headings list; fenced code blocks are stripped via line-by-line state machine (handles up-to-3-space indent, proper closing); heading detection uses exact H2 parsing (rejects `###`, `> ##`, `## extra text`); empty section detection uses any heading as section boundary and excludes sub-heading lines from body content.
- `scripts/test_validator_regression.py`: added dedicated regression test suite (8 tests) for the validator, replacing inline `python3 -c` in CI that broke YAML parsing.
- `schemas/research-pack.md`: added `## Stop condition` to the minimal example shape so it matches the schema's required sections.
- `.github/workflows/ci.yml`: replaced inline Python test fixture generation with `scripts/test_validator_regression.py`.
- `equipment selection / procurement / home-server planning` promoted to first-class route (routing priority #5), with provider-vs-equipment conflict rules and route-conflict examples
- route lists in `ARCHITECTURE.md`, `SYSTEM-MAP.md`, and `README.md` updated from six to seven mature routes
- `scripts/markdown_to_html.py`: hardened metadata HTML escaping and security model — `html.escape()` applied to all frontmatter-derived fields; `cover_meta` lines are escaped individually before joining with `<br>`
- `scripts/markdown_to_html.py`: added `nh3`-based body HTML sanitization — strips `<script>`, `<iframe>`, event handlers, `javascript:` URLs, inline `style` attributes, and `<img src>`; only safe tags and attributes (`class`, `id`, `href`, `colspan`, etc.) are allowed
- `scripts/render_pdf.py`: added `--allow-remote` flag (remote resources blocked by default); route glob fixed to cover all http/https URLs
- `scripts/md_to_pdf.py`: added `--allow-remote` passthrough (remote resources blocked by default)
- `requirements.txt`: added `nh3>=0.2`
- `ROUTING-MATRIX.md`: Listed Company / Investment-style Research route Read list now includes `valuation-methodology.md`, `analyst-consensus-handling.md`, and `reporting-period-handling.md`.
- `checklists/listed-company-report.md`: added `## Valuation methodology` and `## Reporting-period discipline` sections with consensus and period-labeling checks.
- `checklists/forward-looking-claims.md`: added stale consensus check to source-type section.
- `checklists/final-audit.md`: added valuation-precision check to metric-scope audit section.
- `SYSTEM-MAP.md`: mapped new reference and eval files to Family C (valuation methodology, reporting-period handling) and Family E (analyst consensus handling).
- `SKILL.md`: added listed-company synthesis wiring for `valuation-methodology.md`, `analyst-consensus-handling.md`, `reporting-period-handling.md`.
- `references/reporting-period-handling.md`: fixed source priority rule — split into same-period priority (audited over preliminary) and freshness priority (latest period even if preliminary).
- `references/analyst-consensus-handling.md`: softened coverage-count requirement — capture when available, never infer; clarified target price upside is acceptable if attributed.
- `checklists/listed-company-report.md`: softened consensus analyst-count requirement; clarified target price must not be treated as fair value.
- `evals/cases/consensus-and-forward-pe-misuse-case.md`: fixed Tesla earnings date (Jan 28); converted to fixed-scenario prompt with hypothetical bounds; clarified implied upside is acceptable if attributed.
- `evals/cases/reporting-period-and-ttm-confusion-case.md`: fixed TTM example to use only available quarters; converted to fixed-scenario prompt.

### Why
- Per issue #100 and ROADMAP.md P2, the CJK spacing fixes in `markdown_to_html.py` needed validation on Chinese-heavy content. The validation uncovered two pipeline bugs: (1) CJK spacing regexes used `\s+` which merged headings with body paragraphs across `\n`, and (2) `NFKC` normalization degraded Chinese fullwidth punctuation to ASCII. Both were fixed, and a verification script (`test_cjk_pdf_pipeline.py`) was added to prevent regression.
- Per issue #97 (P1), failure-taxonomy families lacked corresponding meta-evals and route-trigger coverage. Added meta-evals for scope completeness and decision utility, wired them into the execution chain (SKILL.md, ROUTING-MATRIX.md route Attach, checklists), and created a reusable reference-level rule for scope completeness that was previously missing.
- Per issue #96 (P1), 11 comparative distillation cases existed but lacked a cross-case candidate rule registry. The registry confirms all PROMOTE_NOW candidates are already covered by existing checklists and references; no new promotion is needed. The main gap has shifted from missing rules to execution/activation discipline.
- Per issue #124 (P2), selection tasks with major execution uncertainty lacked structured post-decision branch planning. The existing scenario logic (Step 7) and change-the-conclusion sections handle pre-decision ranking changes, but do not cover post-decision execution branching (success / blocked / all-blocked paths with trigger conditions and monitoring signals). Added a focused reference file and wired it into option-selection discipline and audit checklist.

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
