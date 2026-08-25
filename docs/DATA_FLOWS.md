# Data Flows

This document is the **single user-facing map** of where research-related data goes, what persists locally, how channels can be turned off, and what degraded states mean.

It complements — but does not replace — discipline references such as `references/external-channel-preflight.md` and `references/search-provider-fallback.md`. Those files define research evidence rules; this file answers operational boundary questions.

## Scope

**In scope**

- network touchpoints that affect a research or delivery run
- local stores that may retain prompts, source metadata, reports, or process artifacts
- off-switch behavior and degraded / blocked / partial / not-run semantics
- whether each control is `measured`, `asserted`, `not_run`, or `unknown`

**Out of scope**

- privacy, compliance, or legal guarantees
- a complete threat model (see `docs/RISK_REGISTER.md`)
- copying every reference document into this map

## Out-of-repository control boundary

The following paths are **not enforced by this repository**. The skill documents expected discipline, but cannot block, audit, or guarantee host-platform transport:

| Boundary | What moves | Who controls it |
|---|---|---|
| Host Agent session transport | user prompts, tool arguments, retrieved page bytes, model context | Cursor / host Agent platform and configured MCP tools |
| User-invoked third-party CLIs | search, fetch, browser, social APIs when the operator explicitly runs them | operator environment (Agent-Reach, `gh`, browser MCP, etc.) |
| Remote model inference | prompt and context sent to the configured model provider | host platform billing / model routing |

Repository scripts and validators run **locally** on files the operator points at. They do not substitute for host-platform data handling.

As of commit `fb5bac2` on `main`, **no repository-owned research script performs live web search or content fetch during normal research execution**. Live search and fetch happen through the host Agent tool surface documented below.

## Network touchpoints

| component | trigger | data_class | destination | credential_role | persistence | off_switch | degraded_state | verification_status |
|---|---|---|---|---|---|---|---|---|
| `agent-reach-local-api` | Agent step 5 preflight or live search/fetch when Agent-Reach is installed locally | prompt fragments, search queries, candidate URLs, fetched page bytes, channel metadata | local Agent-Reach service (`127.0.0.1:8765` by convention) | optional local API session; no repo-stored secrets | none in repo; Agent-Reach may cache per its own docs | skip preflight; do not call `/search` or `/fetch`; use offline materials or host search tools | `api_available: false` or `degraded_channels` → adjust strategy per `references/external-channel-preflight.md`; discovery-only results stay in intake log | asserted |
| `host-agent-search-fetch-browser` | Agent uses WebSearch, browser MCP, Exa fallback, or other host tools during collection | prompts, queries, URLs, retrieved content, screenshots | host platform + third-party services chosen by the operator | provider/API keys held by host environment, not this repo | none in repo by default; host may retain session history | choose offline-only research; avoid live-search steps; declare `live-search status: blocked` in degraded-search log | provider blocked / channel degraded / partial recovery per `references/search-provider-fallback.md` | unknown |
| `render-pdf-playwright` | operator runs `scripts/md_to_pdf.py` or `scripts/render_pdf.py` for PDF delivery | local markdown/HTML bytes; optional remote image/font URLs only if `--allow-remote` | local Chromium via Playwright; remote HTTP/S only when explicitly allowed | none | temporary HTML unless `--keep-html`; PDF written to operator-specified path | skip PDF pipeline (`delivery_status: not_run`) | default `block_remote=True` blocks remote fetches; PDF may be incomplete if remote assets required and not allowed | measured |
| `gh-issue-pr-acceptance` | maintainer runs `scripts/validate_issue_pr_acceptance.py ISSUE PR` | issue/PR metadata, changed file paths (no user research content) | `api.github.com` via authenticated `gh` CLI | `gh auth login` role in maintainer environment | none | do not run the script | script exits 0 with advisory warning when `gh` unavailable | asserted |

### Notes on `render-pdf-playwright`

- Default path loads `file://` HTML only and aborts `http://` / `https://` resource requests.
- `--allow-remote` is opt-in. See `references/delivery-operator-note.md`.
- Regression coverage: `scripts/test_remote_block.py`.

### Notes on `agent-reach-local-api`

- Preflight endpoints documented in `references/external-channel-preflight.md`.
- `DISCOVERY` results must not enter the Source Register until fetch + reclassify completes.

## Local stores

| component | trigger | data_class | destination | credential_role | persistence | off_switch | degraded_state | verification_status |
|---|---|---|---|---|---|---|---|---|
| `user-research-artifacts` | operator or Agent writes Research Pack, report, handoff, or run-state files | prompts, source metadata, claim/evidence registers, reports | user workspace paths (e.g. `research-output/`, `report/`, `*-research-pack.md`) | none | until operator deletes; not managed by repo | do not write artifacts; keep research in-session only | missing artifact blocks strict audit / handoff validation | asserted |
| `md-to-pdf-temp-html` | `scripts/md_to_pdf.py` without `--keep-html` | intermediate HTML | system temp dir (`tempfile.TemporaryDirectory`); with `--keep-html`, retained next to output PDF | none | deleted after PDF render unless `--keep-html` | skip PDF pipeline | `pdf_failed` with error in JSON status | asserted |
| `delivery-status-writeback` | explicit `--write-status PATH` on delivery CLI | delivery status markdown snippet | operator-specified file | none | until operator deletes | omit `--write-status` | `not_run` delivery fields in pack | asserted |
| `generated-route-cards` | maintainer runs `scripts/generate_route_cards.py` | route metadata view | `references/routes/*.md`, `references/route-index.md` | none | committed or regenerated on demand | use manifest JSON directly | `generate_route_cards.py --check` fails when drifted | measured |
| `forward-eval-offline-fixtures` | `scripts/run_forward_evals.py --offline` | fixture reports/packs, activation snapshots | `evals/` registry cases and `tests/fixtures/forward/` snapshot inputs | none | versioned in repo | do not run forward eval | offline runner never calls network (module docstring) | measured |
| `validator-temp-artifacts` | validator subprocess fixtures (e.g. channel preflight behavior checks) | synthetic Research Pack markdown | ephemeral temp file via `tempfile.NamedTemporaryFile` | none | deleted when validator exits | do not run the validator | validator exits non-zero on failure | asserted |
| `ci-test-temp-dirs` | pytest / validator regression tests | synthetic markdown/json fixtures | `tempfile` / `/tmp` during CI | none | ephemeral per test run | N/A (test-only) | test failure if cleanup breaks | measured |

## Off-switch and degraded-state summary

| User intent | Off switch | Expected status |
|---|---|---|
| No live search | skip Agent-Reach + host search tools; use offline materials | `live-search status: blocked` or `api_available: not-checked` with reason |
| No PDF delivery | do not run `md_to_pdf.py` | `delivery_status: not_run` |
| No remote assets in PDF | default delivery (no `--allow-remote`) | local-only render; remote images blocked |
| No maintainer GitHub check | do not run `validate_issue_pr_acceptance.py` | N/A |
| Channel partially available | use available channels; record `degraded_channels` | `partial` research or audit states per `SKILL.md` |

## Related documents

- `docs/RISK_REGISTER.md` — risk → control → evidence status → residual gap
- `references/external-channel-preflight.md` — Agent-Reach preflight and source intake log
- `references/search-provider-fallback.md` — degraded-search policy
- `references/delivery-operator-note.md` — PDF pipeline operator notes
- `schemas/data-flow-registry.json` — machine-readable component registry for network/write-signal drift checks (`signal_files` is the bidirectional source of truth; `source_files` may include indirect participants). Automatic scanning is limited to `scripts/**/*.py`.
