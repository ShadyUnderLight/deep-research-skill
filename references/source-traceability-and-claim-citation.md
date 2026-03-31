# Source Traceability and Claim Citation

Use this file when the research involves producing structured claims, investment memos, competitive analysis, or any output where readers need to audit the origin of each key conclusion.

Do not treat a bibliography as the same thing as source traceability. A list of sources at the end of a report does not tell the reader which specific claim came from which source. This file fixes that.

## Core rule

Every important claim needs to be traceable to a specific source and labeled by evidence type. This is not the same as listing sources at the bottom. This is a two-layer system:

- Layer 1: inline claim-level citations in the body text
- Layer 2: a source register at the end mapping each source id to a specific source with type and relevance

## Why this matters

Without claim-level traceability:

- readers cannot verify specific conclusions
- the model cannot be audited for accuracy
- high-quality and low-quality evidence get mixed
- strong-sounding claims can obscure weak sourcing
- it becomes easy to hide inference behind a bibliography

With proper traceability:

- each key claim has a source id
- the source register classifies each source by type and reliability
- the model's reasoning is auditable
- readers can challenge specific claims, not the whole report

## The two-layer system

### Layer 1: Inline claim citations

Use a simple `[SN]` format in the body text, where `N` is a source number.

Examples:

- `MTT S5000 is positioned as the current flagship AI chip [S01][S03].`
- `The company filed for STAR Market IPO in June 2025 [S01].`
- `Qwen3.5 compatibility was announced via a press release [S04]; GLM-5 compatibility remains unconfirmed at the time of writing [U01].`

Guidelines for inline citations:

- add the citation at the end of the relevant clause or sentence
- when a claim draws from multiple sources, use multiple ids: `[S01][S03]`
- when a claim is inferred and not directly stated in a source, flag it: `[I01]` and explain the inference chain in the source register
- when a claim cannot be confirmed, use `[U01]` and note it in the uncertainty register
- do not cite the same source twice for the same claim in close proximity; one citation per major claim is sufficient
- avoid citing a broad source (e.g., an entire prospectus) without specifying what part of it supports the claim

### Layer 2: Source register

At the end of the report, include a structured source register with at minimum:

- source id
- source title or description
- source type
- date or version
- relevance to the report
- any notes on reliability or limitations

Example format:

```
## Source Register

| ID  | Source | Type | Date | Relevance | Notes |
|-----|--------|------|------|-----------|-------|
| S01 | 上交所科创板招股书（摩尔线程），2025-06 | Primary regulatory filing | 2025-06 | Company fundamentals, financials, products | Most authoritative source for historical facts |
| S02 | 摩尔线程官网产品页 | Primary company | Current | Current product lineup and positioning | May reflect marketing language |
| S03 | SCMP article: "Moore Threads launches..." | Secondary media | 2025-03 | Flagship product claims | journalist synthesis; not primary |
| S04 | 阿里云官方博客：与摩尔线程合作公告 | Primary partner | 2025-04 | Partnership and compatibility claims | Partner self-reporting |
| I01 | Analyst inference based on S01 and S02 | Inferred | 2026-03-31 | Assessment of core business model | Explicit reasoning documented |
| U01 | Unconfirmed; no primary source found | Unconfirmed | 2026-03-31 | GLM-5 compatibility claim | Requires further verification |
```

## Source type classification

Classify every source in the register by type. Use these types consistently:

- `PRIMARY_FILING` — official regulatory filing (招股书, 年报, 季报, 交易所公告)
- `PRIMARY_COMPANY` — official company website, press release, official social media, product documentation
- `PRIMARY_PARTNER` — official statement from a named partner or customer
- `SECONDARY_MEDIA` — news article, industry report, analyst commentary
- `SECONDARY_ANALYST` — analyst report, investment bank research
- `INFERRED` — model inference with explicit reasoning chain documented
- `UNCONFIRMED` — claim found in one or more sources but not independently verified
- `WEAK_SIGNAL` — anecdotal, social media, unnamed sources

## Claim classification

In the source register, classify the nature of each claim:

- `FACT` — directly stated in the source with low ambiguity
- `QUALIFIED` — stated with conditions or caveats in the source
- `INFERRED` — not directly stated; model reasoned from available evidence
- `SPECULATION` — model-generated hypothesis not directly supported by any source
- `UNCONFIRMED` — mentioned in sources but cannot be independently verified

## Inference documentation

When a claim is inferred (not directly stated in any source), document the reasoning chain:

```
I01 | INFERRED | Analyst inference on core business model
  | Evidence: S01 (R&D spend as % of revenue), S02 (product descriptions)
  | Reasoning: High R&D intensity combined with fabless model suggests chip design is 
               the core capability; manufacturing is outsourced.
  | Confidence: Moderate — based on pattern common in fabless semiconductor companies.
  | Limitation: Without detailed cost breakdown in S01, the split between design 
                and manufacturing cost cannot be precisely determined.
```

This makes inference auditable and distinguishes it from sourced facts.

## Uncertainty register

For claims that cannot be confirmed or are highly time-sensitive, include a brief uncertainty register:

```
## Uncertainty Register

| ID  | Claim | Problem | Impact if Wrong |
|-----|-------|---------|------------------|
| U01 | GLM-5 full-stack adaptation completed | No primary source confirmed; only inferred from secondary reporting | Would overstate ecosystem breadth |
| U02 | MTT S5000 shipping volume | Company has not disclosed shipment numbers; third-party estimates unavailable | Affects market position assessment |
| U03 | Next-generation desktop GPU launch timeline | Based on Tom's Hardware speculation; company has not officially confirmed | Timeline uncertainty affects near-term revenue outlook |
```

## Common failure patterns

### Pattern 1: Bibliography theater

The report lists many sources at the bottom but does not use inline citations. Readers cannot determine which specific claim comes from which source.

**Fix:** Use inline `[SN]` citations for every important claim and map them in the source register.

### Pattern 2: Source-type blur

All sources are listed with equal weight regardless of type. A prospectus and a news article get the same visual treatment.

**Fix:** Use source-type classification in the register and weight claims accordingly in the body.

### Pattern 3: Inference presented as fact

Inferred claims are presented without any indication they are inferences. Readers treat them as equally reliable as filed facts.

**Fix:** Use `[I01]` notation for inferred claims and require an explicit reasoning chain in the register.

### Pattern 4: Over-citation

Every sentence ends with multiple source ids, obscuring which source is actually primary and which is supporting.

**Fix:** Cite only the primary or most important source per claim. Use multiple ids only when a claim genuinely draws from multiple distinct sources.

### Pattern 5: Stale source used as current fact

An old filing or news article is cited for a claim about the current state without noting that newer information may supersede it.

**Fix:** For current-state claims, verify that the source is still the most recent authoritative evidence. Flag outdated sources explicitly.

## Good citation patterns

Prefer:

- `MTT S5000 is described as the current flagship AI chip [S01][S03].`
- `The company reported revenue of 7.02 billion RMB for H1 2025 [S01, p.XX].`
- `A partnership with Alibaba Cloud was announced in April 2025 [S04]; GLM-5 compatibility remains unconfirmed as of the research date [U01].`
- `Revenue trajectory 2022–2024: 0.46B → 4.38B [S01]; analyst estimate for 2025 full-year ~15B [I01].`

Avoid:

- `The company has strong partnerships. [S02][S03][S04]` (vague claim, over-cited)
- `The GPU market is growing rapidly. [S05]` (weak claim, stale source)
- `The company is the only domestic full-function GPU firm. [S02]` (strong claim, single source, definition-dependent)

## Integration with confidence labels

Source traceability and the confidence labeling system (confirmed / likely / uncertain) work together:

- `CONFIRMED FACT` claims should map to `PRIMARY_FILING`, `PRIMARY_COMPANY`, or `PRIMARY_PARTNER` sources with `[SN]` citation
- `LIKELY INFERENCE` claims should include `[IN]` with documented reasoning chain in the inference register
- `UNCERTAIN` claims should include `[UN]` with the uncertainty register explaining what would be needed to verify

## Output expectation

A well-traced report should allow a reader to:

1. pick any key claim in the body
2. find its inline citation
3. look up the source in the register
4. understand the source type, date, and reliability
5. if inferred, read the documented reasoning chain
6. if unconfirmed, see the uncertainty register entry

If the report does not support this audit trail, the source traceability discipline is not yet satisfied.

## Red flags

Slow down and add more traceability when:

- a paragraph makes multiple claims but has only one source citation
- a strong conclusion does not have a corresponding primary source in the register
- an inferred claim is presented without `[IN]` notation or reasoning chain
- a source is listed but never actually cited in the body
- the report has a long sources list but no inline citations
- a current-state claim is sourced to an old filing with no indication of supersession

## Final discipline

Before finalizing, ask:

- Can I trace every key claim to a specific source id in the body?
- Does the source register classify each source by type and date?
- Are inferred claims clearly labeled with reasoning chains?
- Are unconfirmable claims flagged in an uncertainty register?
- Does the report look like it has sources, or does it actually support audit trails?

If any of these are weak, add more citations before publishing.
