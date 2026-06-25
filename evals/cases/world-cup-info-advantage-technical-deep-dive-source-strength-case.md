# Eval: World Cup Information Advantage — Technical Deep-Dive Source Strength Failure Case

## Goal

Test whether a Technical Deep-dive / Architecture Analysis report with strong mechanism explanation, correct route selection, explicit comparison dimensions, trade-off analysis, and clear bottom-line judgment can still **fail strict delivery** when:

- **100% of sources are Wikipedia/crowdsourced** — all 8 register entries are Wikipedia; load-bearing claims about FIFA official rules, UEFA scheduling decisions, coach strategies, and game theory concepts cannot be supported by crowdsourced compilations alone
- **Source Register column semantic mismatch** — uses "支持章节" (section-level) instead of "Claims Supported" (claim-level); meets 7-column format but the mapping column is at the wrong granularity
- **numeric role labels absent** — comparison tables (67%, 9 groups/27 matches, 12/27 matches, probabilities) lack observed/proxy/assumption/model-output roles
- **route conflict check absent** — the report touches on rule reform with regulatory implications but does not document why technical-deep-dive beats regulatory as the primary route
- **self-assessment claims all ✅ while source strength, column semantics, and numeric roles all have gaps** — triggers process-integrity hard-fail

This eval is based on a real report: a World Cup information advantage mechanism analysis that correctly activated the technical-deep-dive route, explained information set asymmetry, sequential game theory foundations, empirical limitations, and alternative tournament architectures — but relied entirely on Wikipedia for all load-bearing factual claims, failed to distinguish section-level from claim-level source mapping, and overclaimed self-assessment status.

## Prompt

Analyze whether the World Cup "best third-place" qualification rule gives later-playing teams an information advantage. Produce a structured technical deep-dive report that:

- explains the core mechanism (information set differences, sequential games, threshold calculation)
- identifies key components (ranking rules, match scheduling architecture, tiebreakers)
- identifies fundamental constraints (simultaneous kickoff rules, low scoring, bounded rationality, common knowledge)
- compares alternative architectures (full group synchronization, revert to top-2, 16 groups of 3)
- provides a conditional conclusion with practitioner recommendations
- uses primary technical sources (FIFA/UEFA official rules, schedule PDFs, official press releases, game theory textbooks) — not just Wikipedia — for load-bearing claims
- includes a complete 7-column Source Register with **Claims Supported** (claim-level) not "支持章节" (section-level)
- labels all comparison/estimate numbers with observed/proxy/assumption/model-output roles
- documents the route conflict check: why technical-deep-dive rather than regulatory/policy impact analysis

## What this eval is testing

- whether source strength is audited at the claim level — crowdsourced compilations (Wikipedia) cannot bear load-bearing claims about official rules, organizational decisions, or expert statements
- whether Source Register columns map at the right granularity — "支持章节" (section-level) is insufficient when the column contract is "Claims Supported" (claim-level)
- whether numeric role labels are applied to comparison/estimate numbers
- whether route conflict is documented when the topic touches multiple route boundaries (technical + regulatory)
- whether self-assessment accuracy reflects source strength and column semantics

## Pass criteria

A passing answer should:

1. **Source load-bearing claims from primary or authoritative sources.** Official FIFA/UEFA rules, schedule PDFs, official press releases, verified interviews, and academic game theory sources for claims about rules, scheduling decisions, and expert statements. Wikipedia can supplement background but cannot be the sole source for load-bearing claims.

2. **Use "Claims Supported" at claim-level granularity.** The Source Register column must list specific claims supported by each source (e.g., "S01: 1986/1990/1994 third-place rule formats; ranking criteria A-B-C"), not section names.

3. **Label numeric roles on comparison tables.** Percentages, match counts, probabilities, threshold values must have observed/proxy/assumption/model-output labels.

4. **Document route conflict check.** Explain why technical-deep-dive rather than regulatory — the mechanism analysis makes it technical, even though rule reform implications carry regulatory secondary content.

## Failure signs

Mark this eval as failed if the answer does any of the following:

- all or most load-bearing claims rely on Wikipedia/crowdsourced sources
- Source Register uses "支持章节" (section-level) instead of "Claims Supported" (claim-level)
- comparison/estimate numbers lack numeric role labels
- route conflict check absent (why not regulatory)
- self-assessment claims all ✅ while source strength, column semantics, or numeric roles have gaps

## Why this eval matters

This case adds a **source strength purity dimension** to the technical-deep-dive route. Previous cases test whether sources exist and are cited (register format, body coverage, inflation). This case tests whether the sources used are *strong enough* for the claims they support:

| Case | Body [Sxx] | Register format | Inflation | **Source strength** |
|---|---|---|---|---|
| CPO inline citation | ❌ Zero | 7 cols | N/A | Vendor docs without caveat |
| MCP timeline | ✅ Present | 7 cols | <25% | Mix of official + secondary |
| Agentic RAG | ✅ Present | 6 cols (no DOI) | <25% | Vendor docs + blogs |
| Info advantage (this) | **✅ Present** | **7 cols (wrong semantic)** | **0% (all cited)** | **100% Wikipedia** |

The unique contributions:

- **100% Wikipedia sourcing as a severity benchmark** — every single source is a crowdsourced compilation. The report has the traceability infrastructure (body [Sxx], register mapping, zero inflation) but the source strength cannot support the load-bearing claim weight. This is different from "missing citations" or "register gaps" — it's a *source quality* failure in a fully traced report.
- **"Claims Supported" vs "支持章节" semantic gap** — the register has 7 columns but the mapping column maps to sections, not specific claims. This is a granularity failure: the reader knows which section a source contributes to but not which specific claim it supports. This is a new type of Source Register noncompliance.
- **Route conflict check for technical + regulatory boundary** — a report that analyzes tournament mechanisms AND touches on rule reform implications must document why technical-deep-dive rather than regulatory as the primary route.

## Current rule verdict

- Source strength hard-fail: all load-bearing claims on Wikipedia sources
- Source Register semantics: "支持章节" ≠ "Claims Supported" at claim level
- Numeric role hard-fail: absent from comparison tables
- Route activation: conflict check not documented
- Process-integrity hard-fail: self-assessment claims all ✅ while source strength, register semantics, and numeric roles have gaps

## Related evals

- `evals/cases/mcp-technical-deep-dive-timeline-roadmap-case.md` — same route, timeline and roadmap discipline
- `evals/cases/agentic-rag-technical-deep-dive-compounded-case.md` — same route, compounded vendor/source fail
- `evals/cases/world-cup-rule-regulatory-route-mismatch-case.md` — same topic domain, route self-declaration error
- `evals/cases/tsmc-listed-company-aggregator-source-and-moat-case.md` — same aggregator/source strength issue, different route
- `evals/cases/dc-power-market-outlook-inflation-and-monitoring-case.md` — same Wikipedia source strength issue

## Reviewer checklist

- Are load-bearing claims sourced from primary/authoritative sources, not just Wikipedia?
- Does the Source Register use "Claims Supported" at claim-level granularity (not section-level)?
- Do comparison tables have numeric role labels?
- Is the route conflict check documented (why technical-deep-dive and not regulatory)?
- Does self-assessment reflect source strength accurately?

## Suggested scoring

- **Pass**: load-bearing claims on primary/authoritative sources, "Claims Supported" at claim-level, numeric roles present, route conflict documented, self-assessment honest
- **Conditional pass**: technical analysis strong, mechanism explained, comparison dimensions clear, but Wikipedia used for supplementary claims (not load-bearing), or "Claims Supported" partially at claim-level, or numeric roles exist but incomplete — no hard-fail
- **Fail**: all or most load-bearing claims on Wikipedia/crowdsourced (source strength hard-fail), or register uses section-level instead of claim-level mapping, or numeric roles absent, or route conflict not documented, or self-assessment claims all ✅ while gaps exist
