# Rule Trigger Rate Audit - 2026-06 Baseline

First baseline run for the periodic audit defined in `evals/meta/rule-trigger-audit.md`.

## Metadata

- Period: 2026-06 baseline
- Audit date: 2026-06-11
- Commit anchor: `fe2f60e`
- Case count: 75 tracked Markdown cases
- Data source: `git ls-files evals/cases/*.md`
- Scope: tracked eval-case Markdown files only; local untracked eval assets are intentionally excluded.

## Methodology

This is a first-pass manual audit from case-level diagnosis text, not a fresh re-grade of every original report artifact.

Status values:

- `N/A`: discipline does not apply to this case or the file is a delivery fixture rather than a research-output eval.
- `Triggered`: the case shows visible activation/execution evidence.
- `Missing trigger`: the discipline should have applied, but the case diagnosis shows little or no activation.
- `Declared only`: the report or audit block named the discipline but did not operationalize it.
- `Failed execution`: the discipline visibly activated, but execution failed materially.

For the aggregate rate below, `Triggered` and `Failed execution` both count as activated. `Failed execution` is separated because it points to execution drift rather than missing trigger.

## Discipline summary

| Discipline | Applicable cases | Triggered | Missing/Declared-only | Failed execution | Rate | Status | Notes |
|---|---:|---:|---:|---:|---|---|---|
| Current-state verification | 59 | 56 | 3 | 19 | 94.9% | Healthy activation / execution drift | Usually attaches, but stale anchors and incomplete snapshots remain common. |
| Source traceability | 65 | 57 | 8 | 29 | 87.7% | Needs attention | Highest combined missing/declared-only burden; zero-citation provider cases are the clearest under-trigger cluster. |
| Forward-looking claims | 57 | 57 | 0 | 38 | 100.0% | Healthy activation / execution drift | Almost always recognized, but probability, source-role, and assumption execution frequently fail. |
| Quantitative role labeling | 57 | 53 | 4 | 39 | 93.0% | Healthy activation / execution drift | Activation is high, but table-level and load-bearing number labels fail often. |
| Scope completeness | 36 | 36 | 0 | 5 | 100.0% | Healthy activation | Scope failures are concentrated in global/industry/academic boundary cases. |
| Decision utility | 60 | 58 | 2 | 24 | 96.7% | Healthy activation / execution drift | Most decision tasks shape a recommendation, but utility leaks when route choice or aggregation logic is weak. |
| Delivery cleanliness | 69 | 69 | 0 | 3 | 100.0% | Healthy activation | Delivery checks are visible; remaining failures are concentrated in PDF/layout residue cases. |
| Target-language coherence | 69 | 69 | 0 | 1 | 100.0% | Healthy activation | Mostly stable after CJK delivery work; one delivery fixture still captures language/output residue risk. |

## Case matrix

| Case | Route | Current-state | Source traceability | Forward-looking | Quant role | Scope completeness | Decision utility | Delivery cleanliness | Target-language | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| `evals/cases/aaeon-listed-company-label-inflation-case.md` | listed-company | Failed execution | Failed execution | Failed execution | Failed execution | N/A | Failed execution | Triggered | Triggered | Snapshot, labels, valuation method, and self-assessment drift. |
| `evals/cases/academic-route-activation-crispr-progress-case.md` | academic-review activation | N/A | Triggered | Triggered | N/A | Triggered | N/A | Triggered | Triggered | Route-activation fixture tests academic contract shape. |
| `evals/cases/academic-route-activation-llm-hallucination-comparison-case.md` | academic-review activation | N/A | Triggered | N/A | N/A | Triggered | N/A | Triggered | Triggered | Route-activation fixture for paper-comparison burden. |
| `evals/cases/academic-route-activation-transformer-origin-case.md` | academic-review activation | N/A | Triggered | Triggered | N/A | Triggered | N/A | Triggered | Triggered | Route-activation fixture with literature-review scope. |
| `evals/cases/adlink-listed-company-anchor-error-case.md` | listed-company | Failed execution | Failed execution | Failed execution | Failed execution | N/A | Failed execution | Triggered | Triggered | Anchor fact and unit errors despite visible structure. |
| `evals/cases/advantech-listed-company-traceability-hard-fail-case.md` | listed-company | Failed execution | Declared only | Failed execution | Failed execution | N/A | Triggered | Triggered | Triggered | Source register claimed as pass with zero body citations. |
| `evals/cases/agent-reach-external-channel-preflight-case.md` | external-channel preflight | Triggered | Failed execution | N/A | N/A | N/A | N/A | Triggered | Triggered | DISCOVERY and WEAK_SIGNAL rules triggered but failed in examples. |
| `evals/cases/ai-startup-hq-constrained-choice-register-compliance-case.md` | constrained-choice | Triggered | Failed execution | N/A | Failed execution | Failed execution | Declared only | Failed execution | Triggered | Register claims 7 columns but delivers 5; aggregation not replicable; false precision in ranking. |
| `evals/cases/ai-agent-market-outlook-stakeholder-and-route-boundary-case.md` | market-outlook | Triggered | Failed execution | Failed execution | Missing trigger | Failed execution | Failed execution | Triggered | Triggered | Stakeholder, route-boundary, traceability, and probability gaps. |
| `evals/cases/ai-coding-agent-market-outlook-probability-case.md` | market-outlook | Triggered | Failed execution | Failed execution | Failed execution | Triggered | Triggered | Triggered | Triggered | Strong route execution, probability and sensitivity gaps. |
| `evals/cases/ai-coding-tools-provider-selection-traceability-fail-case.md` | provider-selection | Missing trigger | Missing trigger | N/A | Missing trigger | N/A | Triggered | Triggered | Triggered | Decision architecture present; evidence/current/numeric disciplines absent. |
| `evals/cases/ai-cost-control-market-outlook-full-pass-benchmark.md` | market-outlook | Triggered | Triggered | Triggered | Triggered | Triggered | Triggered | Triggered | Triggered | Full-pass benchmark with all required audits visible. |
| `evals/cases/ai-saas-market-entry-traceability-case.md` | market-entry | Triggered | Missing trigger | Failed execution | Missing trigger | Triggered | Triggered | Triggered | Triggered | Decision architecture strong; body citations and role labels absent. |
| `evals/cases/ai-traffic-police-technical-deep-dive-traceability-case.md` | technical-deep-dive | Triggered | Triggered | Triggered | Triggered | Triggered | Triggered | Triggered | Triggered | Format-boundary case with functional traceability visible. |
| `evals/cases/ai-video-market-outlook-label-and-probability-gap-case.md` | market-outlook | Triggered | Failed execution | Failed execution | Failed execution | Triggered | Triggered | Triggered | Triggered | Scenario structure visible; labels and probability basis fail. |
| `evals/cases/amat-listed-company-anchor-and-label-execution-case.md` | listed-company | Failed execution | Failed execution | Failed execution | Failed execution | N/A | Failed execution | Triggered | Triggered | Label inflation and stale/incorrect anchor execution. |
| `evals/cases/apple-product-and-valuation-case.md` | product/investment analysis | Failed execution | Failed execution | Failed execution | Failed execution | N/A | Failed execution | Triggered | Triggered | Product roadmap and valuation require current and forward-looking discipline. |
| `evals/cases/apple-product-roadmap-and-investment-case.md` | product-roadmap + investment | Failed execution | Failed execution | Failed execution | Failed execution | N/A | Failed execution | Triggered | Triggered | Roadmap/investment case stresses traceability and forecast labeling. |
| `evals/cases/byd-competitive-positioning-traceability-hard-fail-case.md` | competitive-positioning | Failed execution | Failed execution | N/A | Failed execution | Triggered | Triggered | Failed execution | Triggered | Source traceability not executed; self-assessment completely incorrect; evidence labels over-optimistic; strong exclusivity wording. |
| `evals/cases/byd-report-format-discipline-case.md` | listed-company | Triggered | Failed execution | Failed execution | Failed execution | N/A | Triggered | Triggered | Triggered | Labels understood but applied inconsistently. |
| `evals/cases/cambricon-competitive-positioning-near-pass-case.md` | competitive-positioning | Triggered | Triggered | Failed execution | Failed execution | Triggered | Triggered | Triggered | Triggered | Near-pass; secondary verification and role labels lag. |
| `evals/cases/cambricon-evidence-weighting-and-traceability-case.md` | listed-company / evidence weighting | Triggered | Failed execution | Failed execution | Failed execution | N/A | Failed execution | Triggered | Triggered | Evidence weighting visible but weak around bottom line. |
| `evals/cases/cambricon-first-tier-positioning-case.md` | competitive-positioning | Triggered | Triggered | N/A | Failed execution | Triggered | Triggered | Triggered | Triggered | Scope/metric/timeframe visible; overall-label compression remains. |
| `evals/cases/champions-league-constrained-choice-activation-case.md` | constrained-choice activation | Triggered | Missing trigger | Failed execution | Failed execution | N/A | Missing trigger | Triggered | Triggered | Route activation gap leaves prediction/ranking burden weak. |
| `evals/cases/china-shenhua-listed-company-judgment-and-traceability-case.md` | listed-company judgment memo | Failed execution | Failed execution | Failed execution | Failed execution | N/A | Failed execution | Triggered | Triggered | Judgment memo shape and claim traceability leak. |
| `evals/cases/cjk-pdf-validation-findings-case.md` | pdf-delivery validation | N/A | N/A | N/A | N/A | N/A | N/A | Triggered | Triggered | Delivery validation artifact, not a research-output eval. |
| `evals/cases/cjk-pdf-validation-input-company-case.md` | pdf-delivery fixture | N/A | N/A | Triggered | Triggered | N/A | Triggered | Triggered | Triggered | Fixture used to validate CJK rendering pipeline. |
| `evals/cases/cjk-pdf-validation-input-market-case.md` | pdf-delivery fixture | Triggered | N/A | Triggered | Triggered | Triggered | Triggered | Triggered | Triggered | Fixture used to validate CJK rendering pipeline. |
| `evals/cases/cnooc-judgment-shape-improved-but-freshness-still-leaked-case.md` | listed-company | Failed execution | Triggered | Failed execution | Failed execution | N/A | Triggered | Triggered | Triggered | Judgment shape improved but freshness still leaks. |
| `evals/cases/content-platform-constrained-choice-compounded-fail-case.md` | constrained-choice | Triggered | Failed execution | N/A | Failed execution | Triggered | Triggered | Failed execution | Triggered | Zero [Sxx] inline citations; register exists but disconnected; self-assessment claims full pass with all three gaps. |
| `evals/cases/consensus-and-forward-pe-misuse-case.md` | finance-date discipline | Failed execution | Triggered | Failed execution | Failed execution | N/A | Failed execution | Triggered | Triggered | Consensus and forward PE roles are activated but misused. |
| `evals/cases/cross-border-ecommerce-market-outlook-self-assessment-case.md` | market-outlook | Triggered | Failed execution | Failed execution | Failed execution | Triggered | Triggered | Triggered | Triggered | Self-assessment overclaims while traceability/forward-looking are partial. |
| `evals/cases/dc-power-market-outlook-forward-looking-label-gap-case.md` | market-outlook | Triggered | Failed execution | Failed execution | Failed execution | Triggered | Triggered | Triggered | Triggered | Forward-looking claims labeled as confirmed; source register weak. |
| `evals/cases/deepseek-competitive-positioning-evidence-label-case.md` | competitive-positioning | Triggered | Failed execution | N/A | Failed execution | Triggered | Triggered | Failed execution | Triggered | Evidence labels overstate source strength; numeric role labels absent; self-assessment overclaims. |
| `evals/cases/ecommerce-cs-provider-selection-traceability-case.md` | provider-selection | Missing trigger | Missing trigger | N/A | Missing trigger | N/A | Triggered | Triggered | Triggered | Provider facts and recommendations lack auditable sources/roles. |
| `evals/cases/embodied-ai-market-outlook-register-and-label-gap-case.md` | market-outlook | Triggered | Failed execution | Failed execution | Failed execution | Triggered | Triggered | Triggered | Triggered | Register and label execution gap in market-outlook structure. |
| `evals/cases/eu-dma-regulatory-scenario-probability-and-action-tiering-case.md` | regulatory | Triggered | Declared only | Failed execution | Declared only | Triggered | Failed execution | Failed execution | Triggered | Scenario probabilities lack source basis; direct/indirect impact not separated; action tiering absent. |
| `evals/cases/emc-listed-company-strong-claims-moat-case.md` | listed-company | Triggered | Failed execution | Failed execution | Failed execution | N/A | Failed execution | Triggered | Triggered | Strong moat claims exceed evidence and traceability support. |
| `evals/cases/evergrande-property-listed-company-execution-case.md` | listed-company | Triggered | Failed execution | Failed execution | Failed execution | N/A | Triggered | Triggered | Triggered | Near-pass listed-company execution with traceability formatting issues. |
| `evals/cases/fertility-academic-literature-review-format-boundary-case.md` | academic-review | N/A | Triggered | N/A | N/A | Triggered | N/A | Triggered | Triggered | Academic citation format judged functionally traceable. |
| `evals/cases/finance-and-market-share-cambricon-case.md` | finance / market-share | Triggered | Triggered | Triggered | Triggered | Triggered | Triggered | Triggered | Triggered | Numeric/time/source layering is the pass condition. |
| `evals/cases/freshness-xiaomi-case.md` | current-state / ranking | Triggered | Triggered | Triggered | Triggered | N/A | Triggered | Triggered | Triggered | Freshness and finance-date discipline are explicit pass dimensions. |
| `evals/cases/global-market-scope-completeness-case.md` | scope-completeness | Triggered | Triggered | Triggered | Triggered | Failed execution | Triggered | Triggered | Triggered | Scope discipline is central and partially failing. |
| `evals/cases/hnb-industry-report-table-design-case.md` | industry report / delivery | Triggered | Triggered | Failed execution | Triggered | Triggered | Triggered | Failed execution | Triggered | Report table design and estimate sourcing are visible issues. |
| `evals/cases/humanoid-robot-market-outlook-dual-route-case.md` | market-outlook + secondary listed-company | Failed execution | Failed execution | Failed execution | Failed execution | Triggered | Failed execution | Triggered | Triggered | Dual-route execution, stale anchor, citations, and stakeholder gaps. |
| `evals/cases/humanoid-robot-market-outlook-self-assessment-case.md` | market-outlook | Triggered | Failed execution | Failed execution | Failed execution | Triggered | Failed execution | Triggered | Triggered | Market-outlook scenario and self-assessment drift. |
| `evals/cases/indie-dev-constrained-choice-delivery-fail-case.md` | constrained-choice | Triggered | Failed execution | N/A | Failed execution | Failed execution | Declared only | Failed execution | Triggered | No 7-column register; no weights/worked example; shortlist boundary not justified; hidden burdens incomplete. |
| `evals/cases/indie-game-constrained-choice-quantitative-role-case.md` | constrained-choice | Triggered | Triggered | Failed execution | Failed execution | Triggered | Triggered | Triggered | Triggered | Quantitative role and secondary-route checks lag. |
| `evals/cases/industry-landscape-depth-case.md` | industry landscape | Triggered | Triggered | Triggered | Triggered | Failed execution | Failed execution | Triggered | Triggered | Depth/scope and decision utility are central failure dimensions. |
| `evals/cases/injection-stale-product-data-case.md` | freshness / injection | Failed execution | Triggered | N/A | N/A | N/A | Failed execution | Triggered | Triggered | Stale product data contaminates current-state answer. |
| `evals/cases/innolight-listed-company-execution-case.md` | listed-company | Failed execution | Failed execution | Failed execution | Failed execution | N/A | Failed execution | Triggered | Triggered | Listed-company execution family with snapshot/labels/valuation gaps. |
| `evals/cases/intel-current-state-freshness-case.md` | current-state / listed-company | Failed execution | Triggered | Triggered | Triggered | N/A | Failed execution | Triggered | Triggered | Current-state freshness failure is the target. |
| `evals/cases/lotes-listed-company-moat-snapshot-case.md` | listed-company | Failed execution | Failed execution | Failed execution | Failed execution | N/A | Failed execution | Triggered | Triggered | Market snapshot, moat boundary, valuation, and label gaps. |
| `evals/cases/marvell-listed-company-snapshot-traceability-case.md` | listed-company | Failed execution | Missing trigger | Failed execution | Failed execution | N/A | Failed execution | Triggered | Triggered | Claim-level citations absent; snapshot and valuation incomplete. |
| `evals/cases/memory-academic-review-first-post-fix-case.md` | academic-review | N/A | Triggered | Triggered | N/A | Triggered | N/A | Triggered | Triggered | Post-fix academic-review validation. |
| `evals/cases/minimax-company-report-case.md` | company report | Failed execution | Failed execution | Failed execution | Failed execution | N/A | Failed execution | Triggered | Triggered | Company report distillation case with execution gaps. |
| `evals/cases/minimax-sea-memo-pdf-layout-case.md` | market-entry / delivery | Triggered | Failed execution | Failed execution | Failed execution | Triggered | Failed execution | Failed execution | Failed execution | Decision memo content mixed with PDF/layout failure. |
| `evals/cases/moore-threads-listing-status-case.md` | current-state / listing status | Failed execution | Triggered | Triggered | Triggered | N/A | Triggered | Triggered | Triggered | Listing-state and time-discipline stress case. |
| `evals/cases/nev-parts-europe-market-entry-quantitative-role-case.md` | market-entry | Triggered | Triggered | Failed execution | Failed execution | Triggered | Triggered | Triggered | Triggered | Quantitative role labeling is the main leak. |
| `evals/cases/pdf-delivery-trigger-regression-case.md` | delivery regression | N/A | N/A | N/A | N/A | N/A | N/A | Triggered | Triggered | Delivery-only trigger regression. |
| `evals/cases/pop-mart-listed-company-traceability-hard-fail-case.md` | listed-company | Failed execution | Failed execution | Failed execution | Failed execution | N/A | Failed execution | Triggered | Triggered | Traceability hard-fail plus absolute/inference claim issues. |
| `evals/cases/rag-api-provider-selection-traceability-fail-case.md` | provider-selection | Missing trigger | Missing trigger | N/A | Failed execution | N/A | Failed execution | Triggered | Triggered | Same provider-selection evidence/current-state under-triggering pattern. |
| `evals/cases/ranking-and-current-claims-xiaomi-update-case.md` | ranking/current-claims | Triggered | Triggered | N/A | Triggered | Triggered | Triggered | Triggered | Triggered | Current ranking/source/metric discipline is explicit. |
| `evals/cases/regulatory-analysis-route-activation-case.md` | regulatory-analysis activation | Triggered | Triggered | Triggered | N/A | Triggered | Triggered | Triggered | Triggered | Route activation fixture for regulatory impact tasks. |
| `evals/cases/reporting-period-and-ttm-confusion-case.md` | finance-date discipline | Failed execution | Triggered | Failed execution | Failed execution | N/A | Failed execution | Triggered | Triggered | Time-layer and metric-role confusion are central. |
| `evals/cases/source-traceability-moore-threads-case.md` | source-traceability | Triggered | Triggered | Triggered | Failed execution | N/A | Triggered | Triggered | Triggered | Traceability and inference chain are explicit pass criteria. |
| `evals/cases/startup-evaluation-route-activation-case.md` | startup-evaluation activation | Triggered | Triggered | Triggered | Triggered | Triggered | Triggered | Triggered | Triggered | Route activation fixture for startup evaluation. |
| `evals/cases/storage-chip-listed-company-deep-dive-pass-case.md` | listed-company + technical-deep-dive | Triggered | Triggered | Triggered | Triggered | Triggered | Triggered | Triggered | Triggered | Pass-level dual-route benchmark. |
| `evals/cases/technical-analysis-kubernetes-vs-docker-case.md` | technical-deep-dive activation | N/A | Triggered | Triggered | N/A | Triggered | Triggered | Triggered | Triggered | Technical route activation and artifact-contract fixture. |
| `evals/cases/tiktok-ai-technical-deep-dive-route-inflation-case.md` | technical-deep-dive | Triggered | Failed execution | Failed execution | Failed execution | Failed execution | Failed execution | Triggered | Triggered | Route inflation and secondary-route execution drift. |
| `evals/cases/transformer-academic-review-evidence-matrix-and-secondary-route-case.md` | academic-review + technical-deep-dive | N/A | Failed execution | Triggered | N/A | Failed execution | N/A | Triggered | Triggered | Academic metadata, evidence matrix, secondary-route hard-fail skipped. |
| `evals/cases/unitree-competitive-positioning-secondary-route-case.md` | competitive-positioning | Triggered | Failed execution | Failed execution | Failed execution | Triggered | Triggered | Triggered | Triggered | Secondary route, label, strong-claim, and valuation gaps. |
| `evals/cases/world-cup-constrained-choice-wrong-route-case.md` | constrained-choice / wrong-route | Triggered | Missing trigger | Failed execution | Failed execution | N/A | Missing trigger | Triggered | Triggered | Evidence labels good; wrong route and no inline citations. |
| `evals/cases/xiaohongshu-competitive-positioning-register-gap-case.md` | competitive-positioning | Triggered | Failed execution | N/A | Failed execution | Triggered | Triggered | Failed execution | Triggered | Register completeness and delivery residue issues. |
| `evals/cases/xiaohongshu-startup-evaluation-traceability-benchmark-case.md` | startup-evaluation | Triggered | Failed execution | Failed execution | Failed execution | Triggered | Triggered | Triggered | Triggered | Near-pass with traceability/register and sensitivity gaps. |

## Route-level observations

- Provider-selection and constrained-choice failures cluster around `Missing trigger` for source traceability and current-state verification even when decision architecture is strong.
- Market-outlook cases usually trigger the right route structure, but forward-looking claims and quantitative role labeling frequently fall into `Failed execution`.
- Listed-company cases usually trigger current-state and traceability structures, but stale anchors, incomplete snapshots, valuation-method opacity, and label inflation keep execution unstable.
- Delivery cleanliness is mostly triggered and stable, with PDF/CJK-specific cases showing that delivery gates now have concrete regression coverage.
- Academic-review route activation is visible, but evidence-matrix and source-metadata execution can still drift in full-report cases.

## Root-cause classification

| Root cause | Evidence from baseline | Best next fix type |
|---|---|---|
| Missing trigger | Provider-selection cases with zero inline citations or unverifiable current provider facts. | Route attachment / final-audit recall hardening. |
| Execution drift | Market-outlook and listed-company cases with visible scenarios/registers/snapshots that fail labels, source roles, or method transparency. | Checklist gates and validator coverage. |
| Declared but not executed | Source-traceability self-assessments claiming pass while body citations or register mapping are absent. | Process-integrity and declared-not-executed validator expansion. |
| Validator gap | Delivery and traceability issues now have some scripts; quantitative role and route-boundary checks remain mostly manual. | Add narrow lint only after manual baseline stabilizes. |

## Action items

- Add a provider-selection recall issue: source traceability and current-state verification must be visible before ranking or recommendation.
- Add a quantitative-role validator design issue limited to declared role systems and table-level role columns; do not attempt semantic number classification yet.
- Add a market-outlook forward-looking execution issue for probability weights, source roles, assumptions, and reversal conditions.
- Add a listed-company current-state execution issue focused on anchor accuracy, snapshot completeness, and valuation-method transparency.
- During the next 10-case increment, require new eval cases to include an explicit mini-block listing applicable disciplines and their status.

## Follow-up cadence

Run the next audit after either 10 additional tracked case evals or the next major routing/checklist change, whichever comes first.
