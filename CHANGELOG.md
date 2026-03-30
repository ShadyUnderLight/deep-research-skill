# Changelog

All notable changes to this project should be recorded here.

This file is intentionally lightweight. Use concise entries that explain:

- what changed
- why it changed
- what capability or failure mode it affects

## Unreleased

### Added
- `references/market-sizing-and-share-discipline.md`
- `evals/finance-and-market-share-cambricon-case.md`

### Changed
- `SKILL.md` now routes market-size and market-share style work to dedicated sizing/share-discipline guidance.

### Why
- A real Cambricon report example exposed pseudo-precision around market-share estimates, weak mapping between company data and market-size claims, and insufficient numeric discipline in company/sector research.

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
