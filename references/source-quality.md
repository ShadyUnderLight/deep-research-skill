# Source Quality

Use this file when source ranking is ambiguous or when multiple sources conflict in credibility, recency, directness, or independence.

## Core rule

Prefer the source that is most direct, current enough for the task, and least dependent on repetition from another source.

Do not confuse:

- authority with recency
- recency with reliability
- repetition with independent confirmation
- detail with truth

## Ranking dimensions

Judge source quality on these dimensions:

1. **Directness** — does it directly support the claim, or summarize another source?
2. **Authority** — is it primary, official, technical, regulatory, or institutionally credible?
3. **Recency** — is it current enough for the claim being made?
4. **Independence** — is it genuinely separate, or just repeating the same original source?
5. **Specificity** — does it support the exact claim, or only a nearby generalization?

## Preferred order by default

For most claims, prefer:

1. official primary source
2. direct technical or regulatory document
3. reputable institutional dataset or report
4. strong independent secondary analysis
5. media summary
6. social or forum discussion only as weak supplemental signal

## Tie-break rules

When choosing between two sources:

- prefer the more direct one over the more elegant summary
- prefer the more current one for fast-moving topics
- prefer the more authoritative one for stable facts
- prefer two independent moderate sources over many repetitions of one chain
- prefer the source that supports the exact claim wording you want to use

## Fast-moving topics

For product lineups, pricing, rankings, company status, releases, leadership, packaging, and regulation changes:

- recency matters more than older summaries
- old authoritative sources may become misleading
- a current official page often beats a respected but outdated article

## Stable topics

For audited financials, legal text, filings, architecture docs, and official disclosures:

- authority matters more than media interpretation
- primary source should anchor the claim whenever available

## Private company sources

For private, unlisted, or early-stage companies, source availability differs from listed companies. Adjust source hierarchy accordingly.

Preferred order for private companies:

1. **Company official materials** — blog posts, product documentation, whitepapers, official announcements
2. **Credible third-party databases** — Crunchbase, PitchBook, CB Insights (label as aggregator data, not primary source)
3. **Regulatory filings** — SEC Form D, state filings, international equivalents (when available)
4. **Investor-sourced information** — investor blogs, portfolio pages, LP letters (label as investor perspective)
5. **Media coverage** — TechCrunch, 36氪, The Information (treat as discovery, verify claims independently)
6. **Social / community** — founder Twitter/LinkedIn, Reddit, V2EX (minimum weight, supplemental only)

Key rules for private company sources:

- **Crunchbase / PitchBook**: Aggregator data, not primary source. Funding amounts and valuations may be approximate. Label as "per [source], estimated."
- **Media coverage**: Discovery tool, not evidence. Verify load-bearing claims via primary sources when possible.
- **Founder claims**: Issuer-sourced. Do not elevate to confirmed fact without independent validation.
- **Social media**: Weak supplemental signal. Do not use as primary evidence for any load-bearing claim.

For detailed private company evaluation methodology, read `references/startup-evaluation-discipline.md`.

## Regulatory sources

For regulatory and policy analysis, source hierarchy differs from corporate or market research. The key distinction is between regulatory text itself and interpretations of it.

Preferred order for regulatory claims:

1. **Official gazette / regulatory text** — the actual law, regulation, rule, or order as published (Federal Register, 国务院公报, EU Official Journal, agency rule text)
2. **Regulatory filings and disclosures** — formal compliance filings, license applications, enforcement actions, consent orders
3. **Government publications** — regulatory agency guidance, consultation papers, impact assessments, press releases from regulators
4. **Institutional analysis** — law firm memos, policy think-tank reports, official impact studies (label as expert interpretation, not regulatory text)
5. **Media coverage** — news reporting on regulatory developments (treat as discovery, verify against primary sources; enforcement actions are often reported before official documents are published)
6. **Social / analyst commentary** — analyst notes, forum discussion, social media speculation (minimum weight, supplemental only)

Key rules for regulatory sources:

- **Official gazette vs news**: Do not cite a news article's summary of a regulation as if it were the regulation itself. Always verify the actual text for load-bearing claims.
- **Enforcement vs letter-of-law**: Distinguish between what the regulation says and how it is actually enforced. Both matter, but they are not the same source.
- **Draft vs enacted**: Clearly distinguish draft regulations, consultation papers, and proposed rules from enacted law. Do not present a draft as if it were final.
- **Cross-jurisdiction**: When comparing regulatory regimes across jurisdictions, ensure each regime's sources are at the same tier (do not compare official gazette text of one jurisdiction with media coverage of another).

When sources conflict:

1. identify whether the disagreement is about time, scope, metric, or interpretation
2. prefer the source closest to the underlying event or measurement
3. if conflict remains unresolved, state the conflict instead of forcing certainty

For structured conflict classification, resolution steps, and output templates, read `references/data-conflict-resolution.md`.

## Cross-language conflict rules

When researching Chinese-listed companies, Chinese-market topics, or cross-border comparisons, Chinese-language and English-language sources often coexist. Language itself is not a credibility signal — apply the same source-quality dimensions (directness, authority, recency, independence, specificity) regardless of language.

This section covers conflict-handling patterns for cross-language scenarios. For static tier mapping of common Chinese-language sources (东方财富, Wind, 财新, 36氪, 雪球, etc.), read `references/data-conflict-resolution.md`.

Common cross-language conflict patterns:

1. **Chinese filing vs English filing** — same company, same period, different language versions. Differences are usually accounting-scope, translation, or disclosure-level differences, not factual contradictions. Identify the scope difference and use the version most relevant to the research objective.

2. **Chinese filing vs English aggregator (Reuters / Yahoo Finance)** — the filing is the primary source; the aggregator is secondary. If the aggregator number differs from the filing, check whether the aggregator uses a different scope (e.g., consolidated vs parent, GAAP vs non-GAAP, RMB vs USD conversion date).

3. **Chinese media vs English media** — both are secondary. Prefer the source that is more specific (has dates, numbers, direct citations) and more independent (not republishing the same original article). If neither is clearly superior, present both with explicit tension.

4. **One source is more specific** — when one source provides exact dates, numbers, or direct citations and the other provides only a summary or paraphrase, prefer the more specific source regardless of language.

## Output expectation

For important claims, be able to explain in one sentence why that source was chosen over others.

Source discipline does not end at evidence labeling. If the best available evidence remains partial, indirect, stale, or scope-limited, the final conclusion should narrow with it. Weak evidence should not merely produce softer source notes while the headline judgment stays equally strong.

## Red flags

Downgrade confidence when:

- many sources point back to one original article
- the source is old for a fast-moving claim
- the source supports only a broader adjacent claim
- the source uses promotional or marketing wording without direct evidence
- the report wants to use a strong claim that the best source supports only weakly

## Evidence-tier inflation guard

Do not upgrade a claim to confirmed fact merely because it appears specific, technical, or official-adjacent.

Treat these source types with care:
- keynote remarks
- earnings-call commentary
- company blog posts
- press-release framing
- media paraphrases of company statements
- secondary analyst estimates

Distinguish clearly among:
- audited or regulatory disclosure
- official company statement
- management commentary
- secondary estimate
- media-mediated interpretation

For high-risk claim types such as:
- market share
- customer adoption or deployment
- performance leadership
- cumulative sales
- product wins
- roadmap-linked commercial expectations

do not present the claim as confirmed fact unless the underlying evidence is strong enough for that grade.

If source hardness, metric scope, or verification completeness remains unclear:
- downgrade to inference
- or label the claim as management-stated rather than confirmed fact
- and narrow the conclusion that depends on that claim if it remains load-bearing

Evidence labels should reflect source hardness and verification completeness, not just how plausible or specific the sentence sounds.

If a claim stays unresolved in a load-bearing way, do not stop at relabeling the evidence. Also downgrade one or more of the following in the final memo:
- scope of the conclusion
- precision of the conclusion
- confidence of the conclusion
- strength of the recommendation
- stability of the ranking
- timing confidence behind the action

## Load-bearing claims in listed-company monopoly / moat research

For claims about monopoly status, licensing exclusivity, permanent protection, sole-provider status, or extreme market-share dominance:

- prefer primary evidence first
- treat reposts, social discussion, retail-investor commentary, and news aggregation as discovery only
- do not label such claims as confirmed fact unless supported by company filings, regulator documents, or other primary institutional material
- broker research may support interpretation, but should not alone carry `sole` / `only` / `permanent` / `>90%` wording

If source strength does not justify wording strength, downgrade the wording.

When the wording contains `唯一` / `only` / `sole` / `exclusive` / `永久` / `permanent` / `不可替代` / `irreplaceable` / `无竞争对手` / `>90%`, check explicitly:
- exact claim wording
- source class
- year and market scope
- whether the source supports the exact strength or only a weaker adjacent claim

If that check fails, downgrade the conclusion rather than merely softening the source note.

## Issuer-sourced competitive and positioning claims

Treat issuer-sourced claims with extra caution, especially when they involve:
- market share
- ranking
- uniqueness
- leadership
- strategic importance
- cost advantage
- execution superiority
- `first` / `only` / `largest` type statements

Do not treat these as fully confirmed industry facts merely because they appear in:
- company websites
- prospectuses
- investor materials
- official press releases
- company-linked media coverage

Separate such claims into three layers:

1. **Confirmed issuer statement**
   The company or filing explicitly makes the claim.

2. **Independent support or partial support**
   Third-party reporting, public data, or cross-source comparison supports some part of the claim.

3. **Open scope or comparability uncertainty**
   Market definition, denominator, sample boundary, time window, or peer set still limits conclusion strength.

When in doubt, downgrade the certainty of the competitive conclusion rather than inflate the certainty of the evidence.

If a competitive claim depends on a number, make the number's role explicit:
- official reported figure
- management target
- internal estimate
- reconstructed inference
- third-party estimate

Do not let precise quantitative wording create false evidentiary precision.

## External API source type mapping

When consuming results from a local Research API (e.g. Agent-Reach), map the API's returned `source_type` to deep-research source quality rules as follows. This mapping only applies **after** a candidate URL has been fetched and its content evaluated — raw discovery results (e.g. Exa search summaries or `POST /search` output) must never directly support body claims.

| API source_type | deep-research quality tier | Supports load-bearing claim? | Notes |
|---|---|---|---|
| `PRIMARY_COMPANY` / `PRIMARY_DOCS` | Tier 1 (official primary) | Yes, after verifying URL, date, and claim specificity | Register as `PRIMARY_COMPANY` (company docs, product docs, whitepapers) or `PRIMARY_DEV` (API docs, developer guides, changelogs) depending on content type |
| `PRIMARY_DEV` (GitHub, docs) | Tier 1–2 (primary technical) | Yes, for code, project status, release/version claims | Register as `PRIMARY_DEV` |
| `TRANSCRIPT` (interview, earnings call, press conference, podcast, tutorial) | Tier 1–2 (if verbatim); Tier 4 (if summarized) | Conditionally; must annotate transcript source and limitations | Register as `TRANSCRIPT`; Tier depends on whether original speech is captured verbatim or reconstructed |
| `SECONDARY_MEDIA` / `SECONDARY_FEED` | Tier 5 (media summary) | No for load-bearing; yes for context/background | Register as `SECONDARY_MEDIA` or `SECONDARY_FEED` |
| `WEAK_SIGNAL` | Tier 6 (weak) | No — supplemental only | Register as `WEAK_SIGNAL`; enters uncertainty / counter-evidence sections |
| `UNKNOWN` | Low confidence | No — requires manual judgment | Register as `UNCONFIRMED` or `WEAK_SIGNAL` per judgment |

> **Hard rule:** Search-level `DISCOVERY` results (unfetched search summaries) are not a valid source type for the Source Register. They live in the source intake log (see `references/external-channel-preflight.md`) and only enter the Source Register after content fetch and reclassification.

**Weak-signal guard:** Social media, community discussion, and search discovery consensus must not be presented as evidence for headline conclusions. If a conclusion depends on weak signals, either downgrade the conclusion strength or supplement with a hard source (official, regulatory, primary documentation). See also `references/source-traceability-and-claim-citation.md` §Source type classification for `WEAK_SIGNAL` handling.

## Tertiary encyclopedic sources (Wikipedia, Baidu Baike, etc.)

Wikipedia, Baidu Baike, and similar crowd-sourced or collaboratively edited encyclopedias are **tertiary sources** — they aggregate, summarize, and interpret primary and secondary sources. They are **never** primary evidence.

### Classification rules

- **Not valid as `PRIMARY_COMPANY`, `PRIMARY_FILING`, or `PRIMARY_DEV`.** These types require official, direct-from-source documentation. Wikipedia is a tertiary aggregation with variable quality per article, editorial lag, and no institutional accountability.
- **Recommended type:** `SECONDARY_MEDIA` for well-cited articles with stable consensus; `WEAK_SIGNAL` for controversial, poorly cited, or frequently edited topics.
- **De facto fallback:** If a claim depends on a Wikipedia article as its best available source, the claim's evidence strength is inherently weak. Downgrade the conclusion strength rather than treating the citation as solid evidence.
- **Load-bearing prohibition:** Wikipedia alone may not support any load-bearing claim (thesis-bearing, ranking, quantitative, or strong positioning). Use Wikipedia for background, discovery, and consensus summaries only. Every load-bearing claim must have a direct primary or secondary source as its evidentiary anchor.

### Usage guidance

- Wikipedia is useful for: discovery of primary sources (via the reference list at the bottom of each article), factual consensus on well-established topics (e.g., founding dates, historical events), and background context.
- Wikipedia should not be used for: current financial data, current competitive positioning, product specifics, regulatory interpretation, or any claim where precision or timeliness matters.
- When citing Wikipedia in the Source Register, include the URL of the specific page and the retrieval date. A generic "Wikipedia" entry without a page URL does not satisfy traceability.
- If a more authoritative source is available (official document, regulatory filing, primary interview), prefer it over Wikipedia even if Wikipedia is more convenient.
