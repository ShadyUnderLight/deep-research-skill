# Changelog

All notable changes to this project should be recorded here.

This file is intentionally lightweight. Use concise entries that explain:

- what changed
- why it changed
- what capability or failure mode it affects

## Unreleased

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
