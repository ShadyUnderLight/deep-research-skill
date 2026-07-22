# Search Provider Fallback

This file contains the degraded-search fallback policy, execution discipline, evidence log format, and tool capability mapping. It was extracted from `SKILL.md` §Tool strategy to reduce context load on every deep-research invocation.

→ **Back to:** `SKILL.md` §Tool strategy (for the provider-neutral search principle and preflight rules)

## Local Research API (first-class channel)

If the environment has a local Research API (e.g. Agent-Reach running on `127.0.0.1:8765`), it may be available as a non-degraded first-class channel providing:
- channel preflight (`GET /health`, `GET /channels`)
- discovery search (`POST /search`)
- content fetch (`POST /fetch`)

Run preflight (see `references/external-channel-preflight.md`) before treating it as an available channel. When the API is available, prefer it over degraded-search fallbacks for the capabilities it provides.

## Degraded-search fallback policy

If degraded search is needed, use this fallback policy:

1. first distinguish temporary rate-limit / quota issues from broader provider unavailability
2. if live search is still unavailable, declare the search provider degraded in the evidence log
3. if `agent-reach` Exa search is available in the current environment, use it as the first explicit degraded fallback for discovery and comparison-angle finding

4. fallback invocation varies by environment; use your environment's tool calling convention

5. prefer the Exa fallback when the query is primarily about English-language material, technical documentation, developer tooling, code context, company pages, or broad web discovery
6. Exa is not automatically better for every case; if the task is dominated by Chinese-language news flow, localized platform chatter, or a search intent that clearly needs browser-side localization, note that and move on rather than forcing Exa first
7. treat Exa result pages as candidate-source discovery only, not as evidence for memo claims
8. re-verify any load-bearing claim via content-fetch or dynamic-browser capability on the source page itself, prioritizing official / primary sources
9. if Exa is unavailable, unusable, or evidently low-yield for the query class, use Bing via dynamic-browser capability as the second explicit discovery-only fallback, preferably with `en-US` parameters when practical
10. expect region bias / localized ranking in the current environment; do not describe Bing as a guaranteed international or neutral search path
11. treat Bing result pages as candidate-source discovery only, not as evidence for memo claims
12. in the evidence log, record which provider path was attempted, why the fallback was triggered, and whether the fallback was used because of provider failure, quota/rate-limit pressure, or query-fit judgment
13. if Bing is also blocked or unusable, declare the live-search step blocked and note which freshness checks or claims could not be verified live
14. continue with offline materials only if the remaining uncertainty is made explicit

Environment-specific example (one environment only; adjust tool calling convention to match your environment):

```bash
mcporter call 'exa.web_search_exa(query: "<search query>", numResults: 5)'
```

## Degraded-search execution discipline

When fallback search is needed, do not switch providers mechanically.

Before changing provider path, make an explicit judgment about the cause:

- tool unavailable in the current environment
- provider failure or temporary outage
- quota / rate-limit pressure
- query-fit mismatch
- low-yield results despite provider availability
- browser-side localization need

Prefer this execution logic:

- use Exa first when the task is discovery-heavy and likely benefits from English-language web coverage, technical docs, company pages, or broad web recall
- do not force Exa first when the task is dominated by Chinese-language news flow, localized search intent, or browser-local ranking behavior
- before escalating again, tighten the search objective or query shape if the current path is returning noisy but not obviously irrelevant material
- move to Bing only when Exa is unavailable, clearly low-yield for the query class, or mismatched to the search intent
- stop degraded-search escalation when the next provider is unlikely to add decision-relevant value rather than escalating just because another provider exists

If fallback search keeps returning noisy or repetitive candidate sources, say so and tighten the live-search objective instead of continuing provider churn.

## Degraded-search evidence log

When degraded fallback is used, keep a compact internal log in this shape:

- search objective:
- primary provider attempted:
- fallback trigger: tool unavailable / provider failure / quota / query-fit / low-yield / localization need
- fallback provider used:
- why this fallback fits better:
- candidate-source quality: strong / mixed / weak
- claims still needing primary-page verification:
- live-search status: recovered / partially recovered / blocked

This log does not need to appear verbatim in the final memo, but its effects should be recoverable in the Research Pack, uncertainty register, or source notes.

## Common tool capability mapping

Different environments expose different tool names for the same capabilities. Map your environment's available tools to the capabilities expected below:

| Capability | Typical tool names | Notes |
|---|---|---|
| Discovery search | `web_search`, `web_search_exa`, search API, Agent-Reach `POST /search` | |
| Readable content fetch | `web_fetch`, MCP fetch, HTTP fetch, Agent-Reach `POST /fetch` | Must return usable source text, not raw HTML/redirect page |
| Channel preflight | Agent-Reach `GET /health`, `GET /channels` | Only when a local Research API is available; see `references/external-channel-preflight.md` |
| Dynamic browser | `browser`, Playwright, headless Chrome | |
| Parallel agent spawn | `spawn_agent`, `sessions_spawn`, agent/session spawn API | Generic parallel tool-call wrappers do not count — must create independent sub-agent/session per track |

Final synthesis: always perform one parent-level reconciliation pass.
