# Risk Register

This document records **operational and evidence risks** for deep-research runs: what can go wrong, which controls already exist, how well those controls are evidenced, and what gaps remain.

It is **not** a security certification, compliance attestation, or complete threat model. Technical deep-dive reports may still use `references/technical-analysis-discipline.md` §Security deep-dive for domain-specific threat modeling.

For where data goes and how to turn channels off, see `docs/DATA_FLOWS.md`.

## How to read an entry

| Field | Meaning |
|---|---|
| `risk_id` | stable identifier |
| `description` | what can go wrong |
| `affected_boundary` | repo script / host Agent / user tool / delivery |
| `existing_controls` | references, validators, or workflow gates already in tree |
| `evidence_status` | `measured` \| `asserted` \| `not_run` \| `unknown` |
| `residual_gap` | what is still unproven or unmanaged |
| `next_validation` | smallest follow-up measurement or eval |
| `owner_layer` | workflow \| route \| reference \| audit \| eval \| delivery |

---

## RISK-001-retrieved-content-prompt-injection

- **description:** Fetched page content or search snippets contain adversarial instructions that steer the Agent away from evidence discipline.
- **affected_boundary:** host Agent + Agent-Reach fetch + browser tools
- **existing_controls:** `references/source-quality.md`; unfetched `DISCOVERY` cannot cite as `[Sxx]`; `references/external-channel-preflight.md` intake log; counter-evidence workflow in `SKILL.md`
- **evidence_status:** asserted
- **residual_gap:** no automated prompt-injection detector on retrieved HTML; host sandboxing unknown
- **next_validation:** add eval case with malicious snippet in fetched fixture; confirm report does not treat it as authoritative
- **owner_layer:** workflow

## RISK-002-sensitive-query-external-channel

- **description:** Unpublished material, credentials, or sensitive queries are sent to external search/fetch channels.
- **affected_boundary:** host Agent + user-invoked third-party tools
- **existing_controls:** operator responsibility called out in `docs/DATA_FLOWS.md` out-of-repository boundary; no repo auto-upload path
- **evidence_status:** unknown
- **residual_gap:** repository cannot observe or block host tool payloads
- **next_validation:** document operator preflight checklist in Research Pack template (optional); never claim repo-enforced redaction
- **owner_layer:** workflow

## RISK-003-provider-outage-quota-fetch-failure

- **description:** Provider outage, quota exhaustion, or fetch failure blocks current-state verification or source retrieval.
- **affected_boundary:** Agent-Reach + host search tools
- **existing_controls:** `references/external-channel-preflight.md` fetch status table; `references/search-provider-fallback.md`; channel availability snapshot fields in Research Pack
- **evidence_status:** asserted
- **residual_gap:** no live integration test against real Agent-Reach in CI
- **next_validation:** extend `evals/cases/agent-reach-external-channel-preflight-case.md` with fetch_failed fixture expectations
- **owner_layer:** reference

## RISK-004-stale-source-cache-current-state

- **description:** Cached or stale sources produce wrong current-state conclusions.
- **affected_boundary:** host tools + user workspace artifacts
- **existing_controls:** `references/current-state-verification.md`; current-state gate discipline; Research Pack uncertainty register
- **evidence_status:** asserted
- **residual_gap:** no repo-level TTL on user artifacts; Agent-Reach cache semantics out of repo scope
- **next_validation:** eval case where stale date in Source Register must fail current-state audit
- **owner_layer:** audit

## RISK-005-locator-forgery-cross-artifact

- **description:** Source/claim/evidence locators are forged or bound to the wrong artifact (pack vs report vs handoff).
- **affected_boundary:** repo validators + user artifacts
- **existing_controls:** `scripts/audit_evidence.py`; `scripts/validate_research_pack.py`; track handoff validator; CommonMark/evidence provenance tests (issues #403/#408/#409)
- **evidence_status:** measured
- **residual_gap:** scoped claim–source alignment audit landed as opt-in (#419); production enablement still requires explicit bundle + calibration review
- **next_validation:** run opt-in audit on a real report bundle after next multi-claim delivery; refresh gold set when new failure modes appear
- **owner_layer:** audit

## RISK-006-validator-fail-open

- **description:** A validator or parser accepts invalid artifacts that should block delivery.
- **affected_boundary:** repo scripts
- **existing_controls:** `scripts/audit_report.py` fail-closed dispatch; `--strict` / `--require-contract`; forward eval offline baseline; pytest regression suites
- **evidence_status:** measured
- **residual_gap:** not every discipline has executable negative fixtures
- **next_validation:** maintain negative fixture set per route in `tests/fixtures/audit/`
- **owner_layer:** eval

## RISK-007-model-tool-version-drift

- **description:** Model or tool version changes alter routing, citation, or audit behavior without repo changes.
- **affected_boundary:** host Agent platform
- **existing_controls:** offline forward eval replays local snapshots; `evals/registry.json`; changelog discipline
- **evidence_status:** not_run
- **residual_gap:** no pinned model matrix in repo; host upgrades can silently shift behavior
- **next_validation:** record host model/tool versions in Research Pack optional metadata
- **owner_layer:** eval

## RISK-008-partial-not-run-misread-as-pass

- **description:** Operator or reader treats `partial` / `not_run` tool or audit states as a clean Pass.
- **affected_boundary:** workflow + delivery
- **existing_controls:** `SKILL.md` §Blocked, partial, and not-run states; separate Research status vs Delivery status vs Final audit status in `schemas/research-pack.md`
- **evidence_status:** asserted
- **residual_gap:** final-audit checklist still relies on human reading of status fields
- **next_validation:** audit_report JSON should surface not-run Required audits as blocking when `--strict`
- **owner_layer:** workflow

## RISK-009-host-platform-transport

- **description:** Prompts, retrieved content, or reports leave the machine through host session transport without repo visibility.
- **affected_boundary:** host Agent platform (out of repository control)
- **existing_controls:** `docs/DATA_FLOWS.md` boundary table; no repo telemetry endpoint
- **evidence_status:** unknown
- **residual_gap:** repository cannot measure or block host uploads
- **next_validation:** none in repo; operator must review host platform data policy
- **owner_layer:** workflow

## RISK-010-pdf-remote-resource-fetch

- **description:** PDF rendering pulls remote images/fonts and leaks report context or breaks air-gapped expectations.
- **affected_boundary:** delivery (`render-pdf-playwright`)
- **existing_controls:** `scripts/render_pdf.py` default `block_remote=True`; `scripts/test_remote_block.py`; `references/delivery-operator-note.md`
- **evidence_status:** measured
- **residual_gap:** `--allow-remote` is operator opt-in without automatic URL allowlist
- **next_validation:** keep `test_remote_block.py` in CI smoke-adjacent checks
- **owner_layer:** delivery

## Related documents

- `docs/DATA_FLOWS.md` — touchpoint and store map
- `references/external-channel-preflight.md` — external channel preflight discipline
- `schemas/data-flow-registry.json` — registry used by `scripts/validate_data_flows.py`
