# Eval: Agent-Reach External Channel Preflight & Evidence Discipline

## Goal

Verify that when a research task uses the Agent-Reach local Research API as an external information channel, the workflow:

1. runs explicit channel preflight before depending on the API
2. records preflight results (channel availability snapshot) in the process artifact
3. treats `POST /search` `DISCOVERY` results as candidate-source discovery only — never as body-citable evidence
4. follows the `DISCOVERY → fetch → reclassify` pipeline before any search result enters the Source Register
5. applies correct evidence downgrade for `WEAK_SIGNAL` sources (social, community, forum)
6. downgrades conclusion strength when load-bearing claims depend on weak signals rather than hard sources

## Real case pattern

A hypothetical but representative research task: *"Evaluate community sentiment and competitive positioning for Company X's new AI coding product in 2026"* using the Agent-Reach local API.

**What is done well:**
- ✅ Channel preflight run before research: `GET /health` and `GET /channels` confirm API available
- ✅ Channel availability snapshot recorded with `api_available: true`, `channels_ok: 5`, `selected_channels: [search, fetch]`
- ✅ `POST /search` used for discovery: returns `DISCOVERY` results — candidate URLs recorded in source intake log

**What must not happen:**
- ❌ `DISCOVERY` results cited as `[Sxx]` in body text
- ❌ Exa search summary treated as evidence for memo claims
- ❌ Social media / community `WEAK_SIGNAL` used as sole support for headline conclusion
- ❌ Channel unavailability silently ignored (API down but search assumed available)
- ❌ `POST /fetch` results used without source-quality classification

## Required demonstration

A passing execution must show:

### 1. Channel preflight

```
- api_available: true
- api_version: 0.1.0
- checked_at: 2026-06-04T10:00:00Z
- channels_ok: 5
- channels_total: 6
- selected_channels: [search, fetch]
- degraded_channels: [rss]  (if applicable)
- impact_on_research: RSS channel degraded; feed-based monitoring unavailable — current-state checks rely on search + fetch
```

### 2. Source intake log (DISCOVERY → fetch → reclassify)

At least one candidate discovered via `POST /search` must trace through the full pipeline:

```
- candidate_url: https://example.com/company-x-ai-product-2026
  discovered_via: agent-reach-search
  discovery_source_type: DISCOVERY
  discovered_at: 2026-06-04T10:05:00Z
  fetch_status: fetched
  reclassified_as: SECONDARY_MEDIA (after fetch — media article with interview quotes)
  register_id: S03
```

### 3. Source Register only contains reclassified entries

No entry in the Source Register may have `DISCOVERY` as its source type. Every Source Register entry must trace back to a fetched and reclassified source.

### 4. WEAK_SIGNAL handled correctly

- If `POST /search` returns social media/community results, they enter the intake log
- After fetch, they may be classified as `WEAK_SIGNAL`
- `WEAK_SIGNAL` entries appear in uncertainty register / counter-evidence log, not as support for headline conclusions
- If a conclusion depends on weak signals, the conclusion strength is explicitly downgraded or supplemented with a hard source

### 5. Channel availability snapshot in Research Pack

The Research Pack should contain a `channel availability snapshot` section (not just degraded-search log) when API preflight was run.

## Scoring

- **Pass**: channel preflight recorded (all 8 fields present) + DISCOVERY → fetch → reclassify pipeline shown + Source Register free of DISCOVERY + WEAK_SIGNAL correctly downgraded + channel snapshot present
- **Conditional Pass**: preflight recorded but intake log incomplete or field coverage partial, or WEAK_SIGNAL handling correct but channel snapshot missing
- **Fail**: DISCOVERY results cited as `[Sxx]` in body, or WEAK_SIGNAL used for headline conclusion without downgrade, or channel unavailability silently ignored

## Review checklist

When applying this eval, check each item:

- [ ] Preflight was run and recorded (api_available, channels, checked_at)
- [ ] Source intake log shows DISCOVERY results with candidate URLs
- [ ] At least one candidate traces `DISCOVERY → fetch → reclassify` pipeline
- [ ] No `[Sxx]` cites a `DISCOVERY` source
- [ ] No `DISCOVERY` type appears in Source Register
- [ ] WEAK_SIGNAL sources (social, community) do not support headline conclusions alone
- [ ] If weak-signal-dependent, conclusion strength is explicitly downgraded
- [ ] Channel availability snapshot appears in Research Pack
- [ ] If API/channel unavailable, impact_on_research is documented and search strategy adjusted
- [ ] API unavailability does not result in silent assumption of search capability

## Related evals

- `evals/meta/degraded-search-execution.md` — evaluates fallback search execution discipline
- `evals/meta/rule-activation-and-execution-discipline.md` — evaluates rule activation (whether preflight rules actually trigger)

## Related references

- `references/external-channel-preflight.md` — preflight rules and source intake log definition
- `references/research-pack-contract.md` — channel availability snapshot field
- `references/source-quality.md` §External API source type mapping — source type mapping and weak-signal guard
- `references/source-traceability-and-claim-citation.md` §Source type classification — DISCOVERY exclusion from Source Register
