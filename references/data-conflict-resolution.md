# Data Conflict Resolution

Use this file when multiple sources provide contradictory data for the same fact, metric, or claim.

Do not silently pick one source. When data conflicts, apply a structured resolution protocol and make the conflict visible in the final report.

## Core rule

When sources disagree, the conflict must be identified, classified, resolved with explicit reasoning, and recorded. Suppressing or ignoring data conflicts produces false confidence.

## Conflict levels

Classify each conflict by severity:

| Level | Name | Definition | Example |
|-------|------|------------|---------|
| **Level 1** | Scope / definition difference | Same fact, different metric definitions or measurement scopes | GAAP vs Non-GAAP revenue; shipment vs sell-through volume; fiscal year vs calendar year |
| **Level 2** | Directional inconsistency | Different sources trend in opposite directions or give incompatible qualitative assessments | One source says market growing, another says declining; one analyst upgrades, another downgrades |
| **Level 3** | Factual contradiction | Same metric, same period, numbers that cannot be reconciled | $0.24M vs $25.6M revenue for the same fiscal year; two "official" figures that disagree |

### Level-specific response

- **Level 1**: Identify the definition difference. Use the definition most relevant to the research objective. State which definition was used and why.
- **Level 2**: Compare source quality (see `references/source-quality.md`). Prefer the source with better directness, authority, and recency. If both remain credible, present both with explicit tension.
- **Level 3**: Treat as a research blocker until resolved. Escalate to primary sources (filings, regulatory disclosures). If resolution is not possible, downgrade confidence on all claims that depend on this number.

### Multi-level conflicts

When a conflict spans multiple levels, classify at the highest severity level that applies. For example, a scope difference (Level 1) that also produces directional inconsistency (Level 2) should be treated as Level 2.

## Source credibility hierarchy for conflict resolution

This tier hierarchy is a specialized refinement for financial and market data conflicts. For general source quality dimensions (directness, authority, recency, independence, specificity), see `references/source-quality.md`.

When sources conflict, use this hierarchy to determine which source takes precedence:

| Tier | Source type | Description | When to prefer |
|------|------------|-------------|----------------|
| **1** | Official filing | SEC 10-K/10-Q, CSRC/HKEX filings, audited annual/interim reports | Historical financials, regulatory disclosures, restated figures |
| **2** | Exchange / regulatory aggregator | Reuters LSEG, Bloomberg filed data, Wind/Choice API filed data | When primary filing is not directly accessible but data is sourced from filings |
| **3** | Company disclosure (unaudited) | Earnings releases, investor presentations, press releases, management commentary | Latest quarter before full report; forward guidance |
| **4** | Reputable third-party dataset | IDC, Counterpoint, Canalys, Gartner (when methodology is transparent) | Market size, market share, industry benchmarks |
| **5** | Secondary media / analyst | Seeking Alpha, Reuters news, broker research, industry media | News flow, interpretation, synthesis |
| **6** | Social / forum | Retail investor forums, social media, anonymous commentary | Discovery only; never as sole evidence for load-bearing claims |

### Chinese-language source mapping

When researching Chinese-listed companies, Chinese-market topics, or cross-border comparisons, use this mapping to classify common Chinese-language sources into the tier hierarchy above.

| Tier | Chinese-language source | Mainland accessibility | Mapping rationale |
|------|------------------------|----------------------|-------------------|
| **1** | 上交所/深交所/港交所 official filings (年报、半年报、季报) | ✅ | Official regulatory filing, equivalent to SEC 10-K/10-Q |
| **2** | 东方财富 Choice API (filed data), Wind (filed data), 巨潮资讯网 | ✅ | Exchange/regulatory aggregator when data is sourced from filings |
| **3** | 公司官网公告、投资者互动平台、业绩说明会 | ✅ | Company disclosure (unaudited), same as earnings releases / investor presentations |
| **4** | 财新、证券时报、21 经济、第一财经 | ✅ (财新部分内容需付费) | Reputable financial media with editorial standards; stronger than general industry media |
| **5** | 36 氪、动点科技、半导体行业观察、新浪财经、同花顺 | ✅ | Industry media / news aggregation; useful for news flow and discovery |
| **6** | 雪球、知乎、微博、东方财富股吧 | ✅ | Social / forum; discovery only, never as sole evidence for load-bearing claims |

When a Chinese-language source provides data that conflicts with an English-language source for the same fact, apply the standard conflict-resolution protocol below. Language is not a credibility signal — tier and directness are.

### Tie-break rules

When two sources are at the same tier, apply these rules in order. These rules are consistent with `references/source-quality.md`; this file adds the independence check as a formal tie-break step:

1. **Prefer the more direct source** — a filing summary beats a media paraphrase of the same filing
2. **Prefer the more current source** — for fast-moving data, newer is better unless the older source is audited and the newer is preliminary
3. **Prefer the more specific source** — a source covering the exact metric beats one covering an adjacent metric
4. **Check independence** — if two sources trace back to the same original data point, they count as one source, not two

### Cross-tier conflicts

When a lower-tier source contradicts a higher-tier source:

- Default: trust the higher-tier source
- Exception: if the lower-tier source is more recent AND the higher-tier source is known to be stale (e.g., old annual report vs. new earnings release), prefer the newer source but label it as preliminary
- Never downgrade a Tier 1 filing based on Tier 5–6 media/forum claims alone

## Resolution steps

Follow this sequence when a conflict is identified:

### Step 1: Identify the exact conflict

Pinpoint:
- Which specific claim or number is in conflict?
- Which sources provide which values?
- Is this a Level 1, 2, or 3 conflict?

### Step 2: Classify each source

For each conflicting source, identify:
- Source tier (1–6 per the hierarchy above)
- Source type (see `references/source-traceability-and-claim-citation.md` for type labels)
- Directness: does it directly report the fact, or summarize another source?
- Recency: when was the data published or filed?
- Independence: is this an original source, or a repetition of another source?

### Step 3: Apply resolution logic

- If sources are at different tiers → prefer the higher-tier source
- If sources are at the same tier → apply tie-break rules
- If the conflict is Level 1 (scope/definition) → use the definition most relevant to the research objective
- If the conflict is Level 3 and involves Tier 1–2 sources → escalate: check for restated figures, amended filings, or updated disclosures

### Step 4: Record the conflict

Even after resolution, record the conflict in the report. Use the output template below.

### Step 5: Adjust confidence

If the conflict cannot be fully resolved:
- Downgrade the confidence of claims that depend on the conflicted data
- Narrow the scope of conclusions that assume a specific value
- State the remaining uncertainty explicitly

## Output template

When a data conflict is identified and resolved, include a conflict record in the report. Place it near the relevant claim or in a dedicated section.

### Inline pattern (lightweight)

For Level 1 conflicts that are easily resolved:

```
FY2025 revenue was $25.6M (per annual report [S01]); an earlier media report cited $0.24M [S05], which appears to reflect a different segment scope. The annual report figure is used here as the authoritative source.
```

### Structured conflict record (for Level 2–3 or when conflict is load-bearing)

```
### ⚠️ Data Conflict Record

- **Conflicted field**: [Revenue FY2025]
- **Source A**: [Reuters LSEG — $0.24M] (Tier 2, exchange aggregator, filed data)
- **Source B**: [Seeking Alpha — $25.6M] (Tier 5, media, news article headline)
- **Conflict level**: [Level 3 — factual contradiction]
- **Resolution**: [Source A adopted]
- **Reasoning**: [Reuters LSEG reflects filed data from regulatory disclosure; Seeking Alpha headline likely contains an error or refers to a different metric]
- **Residual uncertainty**: [Low — the discrepancy most likely stems from SA headline error; filing data is authoritative]
- **Impact on conclusion**: [None — revenue figure is not load-bearing for the current thesis] / [Moderate — revenue figure affects valuation range; confidence downgraded]
```

### Unresolved conflict (when resolution is not possible)

```
### ⚠️ Unresolved Data Conflict

- **Conflicted field**: [Market share Q3 2025]
- **Source A**: [IDC — 18.2%] (Tier 4, third-party dataset)
- **Source B**: [Counterpoint — 12.7%] (Tier 4, third-party dataset)
- **Conflict level**: [Level 3 — factual contradiction]
- **Resolution**: [Not resolved — both sources are same-tier with different methodologies]
- **Reasoning**: [IDC and Counterpoint use different market definitions and sample boundaries; neither can be preferred without methodology comparison]
- **Residual uncertainty**: [High — market share is materially uncertain]
- **Impact on conclusion**: [Market-share-dependent claims downgraded; conclusion narrowed to directional trend rather than precise positioning]
```

## Integration with existing disciplines

This file works alongside:

- `references/source-quality.md` — for source ranking dimensions, tie-break rules, and cross-language conflict handling patterns (this file adds the tier hierarchy, conflict-specific protocol, and Chinese-language source mapping)
- `references/counter-evidence.md` — for actively seeking contradicting evidence (this file adds structured handling once conflict is found)
- `references/claim-matrix.md` — for tracking claim-level evidence and counter-evidence (this file adds conflict-specific resolution logic)
- `references/source-traceability-and-claim-citation.md` — for source type classification and inline citation (this file adds conflict records)

Do not duplicate content from these files. Reference them when the reader needs deeper guidance on source quality, counter-evidence search, or claim tracking.

## When to apply this protocol

Run the conflict-resolution check when:

- researching financial data from multiple platforms (Reuters vs Bloomberg vs Yahoo Finance vs Wind)
- comparing market-share data from different research firms (IDC vs Counterpoint vs Canalys)
- cross-referencing company disclosures with third-party estimates
- finding contradictory analyst consensus or target prices
- encountering headline-level claims that contradict filed data
- comparing data across jurisdictions (SEC vs CSRC vs HKEX filings for the same company)
- cross-verifying Chinese-language and English-language sources for the same claim (e.g., 中文年报 vs English Reuters summary; 东方财富 vs Yahoo Finance)

Do not apply this protocol for:
- expected noise in forward estimates (that is estimate uncertainty, not data conflict)
- normal variance in analyst opinions (that is opinion dispersion, not factual conflict)
- historical vs forward-looking data (that is time-layer separation, handled by `references/finance-date-discipline.md`)

### Distinguishing opinion dispersion from factual conflict

When analyst estimates for the same metric and period diverge, determine whether this is normal dispersion or a factual conflict:

- **Opinion dispersion**: Estimates differ by a typical margin for the metric's volatility, agree on direction, and use similar methodologies. Treat as normal variance.
- **Factual conflict**: Estimates contradict directionally, differ by an unusual margin, or use incompatible data sources. Treat as a data conflict and apply this protocol.

The threshold depends on the metric's typical volatility. For example, a 10% gap in revenue estimates for a stable utility is significant; the same gap for a high-growth startup may be normal.

## Common failure patterns

### Pattern 1: Silent selection

The report uses one source's number without acknowledging that other sources provide different numbers.

**Fix**: State which source was used and note that other sources exist with different values.

### Pattern 2: False precision from cherry-picking

The report picks the source that gives the most impressive (or most conservative) number without explaining why.

**Fix**: Apply the tier hierarchy and tie-break rules. Document the reasoning.

### Pattern 3: Bibliography without conflict resolution

The report lists multiple sources that disagree, but does not explain which was used or why.

**Fix**: For each conflicting data point, state the resolution and reasoning inline or in a conflict record.

### Pattern 4: Treating all sources as equal

The report gives equal weight to a filing and a media headline.

**Fix**: Use the source credibility hierarchy. Tier differences should be visible in the conflict record.

### Pattern 5: Conflict found but no confidence adjustment

The report acknowledges a conflict but proceeds with full confidence as if it were resolved.

**Fix**: If the conflict is not fully resolved, downgrade confidence on dependent claims.
