# External Channel Preflight

## Purpose

When a research task depends on external information channels — live search, content fetch, current-state verification, weak-signal scan, or RSS monitoring — the agent should verify channel availability before committing to a search strategy that assumes those channels exist.

This file defines how to preflight a local Research API (e.g. Agent-Reach) and how to record channel availability in a way that preserves evidence discipline.

## Scope

This file covers:

- when to check external channel availability
- default preflight endpoint and expected shape
- fields to record in the process artifact
- degraded / unavailable handling
- source intake log: how discovery results enter the evidence pipeline

It does **not** cover:

- how to run the Research API itself (that belongs in the external service's own documentation)
- how to vendor or import the Research API runtime into this repo
- how to make any specific external channel a hard dependency

## When to preflight

Preflight the local Research API when the task needs any of these:

- **live web search** — discovery of current sources, comparison-angle finding
- **current-state verification** — confirming product versions, pricing, company status, market snapshot
- **weak-signal scan** — social media, community discussion, sentiment signals
- **content fetch** — retrieving readable content from a candidate URL
- **RSS / feed scan** — monitoring for recent updates from known sources

If the task can be answered entirely from existing knowledge or offline materials, preflight is optional.

## Default preflight endpoints

When the local Research API follows the Agent-Reach convention, these endpoints are used:

| Endpoint | Method | Purpose |
|---|---|---|
| `http://127.0.0.1:8765/health` | GET | API availability and version |
| `http://127.0.0.1:8765/channels` | GET | Available channel list and status |

Adjust the host and port to match your environment if the API runs elsewhere.

## Preflight fields to record

When preflight is run, record these fields in the channel availability snapshot (see `references/research-pack-contract.md`):

- `api_available` — whether the API responded
- `api_version` — version string from health response
- `checked_at` — ISO-8601 timestamp
- `channels_ok` — count of channels reporting OK status
- `channels_total` — total channels defined
- `selected_channels` — list of channels selected for the current task
- `degraded_channels` — list of channels reporting degraded status
- `impact_on_research` — what effect degraded/unavailable channels have on the research scope or confidence

If preflight is not run explicitly, record `api_available: not-checked` and the reason.

## Degraded / unavailable handling

If the local Research API is unavailable or reports degraded channel status:

1. **Record explicitly** — note `api_available: false` or `degraded_channels: [...]` in the channel availability snapshot
2. **Adjust search strategy** — return to the environment's existing search, fetch, and browser capabilities (see `SKILL.md` §Tool strategy)
3. **Do not silently assume** — never proceed as if Agent-Reach is available when it is not
4. **Update the evidence log** — record which channel was expected, what the status was, and what impact on research scope or confidence results

If the API is available but certain channels are degraded (e.g. `search` OK but `fetch` degraded), still attempt the task with the available channels and document the limitation.

## Source intake log: DISCOVERY → fetch → reclassify

Agent-Reach `POST /search` returns results with `source_type: DISCOVERY`. These are candidate sources, not evidence.

The correct pipeline is:

```
POST /search
  → DISCOVERY results recorded in source intake log (NOT Source Register)
  → candidate URL selected
  → POST /fetch (or other content-fetch capability) retrieves readable page content
  → page content classified into one of the real source types:
      PRIMARY_FILING, PRIMARY_COMPANY, PRIMARY_PARTNER, PRIMARY_DEV,
      SECONDARY_MEDIA, SECONDARY_ANALYST, SECONDARY_FEED,
      TRANSCRIPT, INFERRED, UNCONFIRMED, WEAK_SIGNAL
  → reclassified source enters the Source Register (with original DISCOVERY ref retained)
```

> **Hard rule:** `DISCOVERY` results must never appear as `[Sxx]` body citations. They live in the source intake log (part of the degraded-search log or an independent research-process artifact). Only after fetch and reclassification does a candidate become a registerable source.

### Source intake log shape

A compact source intake log entry looks like this. Note that discovery and fetch have separate timestamps to make the pipeline auditable:

```
- candidate_url: https://example.com/article
  channel: agent-reach-search
  operation: search
  discovered_at: 2026-06-04T10:30:00Z       # when POST /search returned this URL
  discovery_source_type: DISCOVERY
  raw_ref: https://example.com/article       # the candidate URL itself
  fetch_status: fetched                      # fetched / fetch_failed / skipped / fetch_unreadable
  retrieved_at: 2026-06-04T10:31:15Z         # when POST /fetch completed
  reclassified_as: SECONDARY_MEDIA           # after content evaluation
  register_id: S04                           # linked after reclassification
  confidence: medium                         # source-quality confidence after fetch
  notes: Media article with interview quotes from CEO; load-bearing claims need primary filing verification
```

Fields:
- `channel` — which API channel produced this candidate (agent-reach-search, agent-reach-fetch, etc.)
- `operation` — which operation (search, fetch, rss-scan, etc.)
- `discovered_at` / `retrieved_at` — separate timestamps for discovery vs content fetch
- `raw_ref` — the candidate URL or API ref
- `confidence` — source-quality confidence after fetch evaluation (high / medium / low)
- `notes` — any caveat, limitation, or cross-reference for this candidate

This log preserves the audit trail from discovery to evidence without letting raw search results enter the body citation chain.

### Fetch status handling

| Status | Meaning | Next step |
|---|---|---|
| `fetched` | Content retrieved successfully | Reclassify into a real source type and enter Source Register |
| `fetch_failed` | HTTP error, timeout, or connection refused | Retain the intake log entry with the error; do not reclassify. Optionally select a different candidate URL for the same research need |
| `fetch_unreadable` | HTTP 200 but content is a login wall, CAPTCHA, binary file (PDF/image), or redirect loop | Record the obstacle in the intake log notes; do not reclassify. The URL may still be useful as a reference for human verification if the content is important |
| `skipped` | Candidate not fetched (e.g. enough sources already) | Retain the entry for audit trail; no reclassification needed |

### Empty result set handling

If `POST /search` returns zero candidate URLs:
1. Declare the discovery phase complete for that query
2. Record `impact_on_research` noting that no candidates were found
3. Optionally retry with a refined search query
4. Do not fabricate or infer candidate URLs from search metadata

### Fetch failure handling for load-bearing gaps

If a candidate URL is the only known source for a load-bearing claim and fetch fails:
1. Note the gap in the uncertainty register
2. Do not present the unfetched DISCOVERY result as evidence
3. If the claim is thesis-bearing, downgrade the conclusion or find an alternative source

## Source type mapping (Agent-Reach API → deep-research)

After a candidate URL is fetched and its content evaluated, the source type from the Agent-Reach API maps to deep-research types as follows:

| Agent-Reach source_type | deep-research handling | Register as |
|---|---|---|
| `PRIMARY_COMPANY` / `PRIMARY_DOCS` | Strong source candidate; verify URL, date, and specific claim before use | `PRIMARY_COMPANY` or equivalent |
| `PRIMARY_DEV` (GitHub repo, issue, PR, release) | Supports code, project status, release/current-state claims | `PRIMARY_DEV` |
| `SECONDARY_MEDIA` / `SECONDARY_FEED` | Supports media/current-state context; load-bearing claim needs primary source | `SECONDARY_MEDIA` or `SECONDARY_FEED` |
| `TRANSCRIPT` (interview,发布会, tutorial, podcast) | Input for interview/podcast/tutorial content; must annotate transcript source and limitations | `TRANSCRIPT` |
| `WEAK_SIGNAL` (social media, community, forum) | Weak signal only; supports sentiment/community/口碑 leads; cannot independently support core judgment | `WEAK_SIGNAL` |
| `UNKNOWN` | Default low confidence; requires manual or source-quality judgment | `UNCONFIRMED` or `WEAK_SIGNAL` per judgment |

The `DISCOVERY` type from `POST /search` does **not** appear in this table because it never enters the Source Register — see the source intake log rules above.

## Relationship to other references

- `SKILL.md` §Tool strategy — preflight is part of the tooling preflight step (step 5); this file provides the reference for Agent-Reach-aware environments
- `references/research-pack-contract.md` — channel availability snapshot records the preflight output
- `references/source-quality.md` — source quality rules apply after a candidate is fetched and reclassified
- `references/source-traceability-and-claim-citation.md` — DISCOVERY is not a valid Source Register source type; only reclassified entries qualify
- `evals/meta/degraded-search-execution.md` — evaluates whether fallback search handling is disciplined
