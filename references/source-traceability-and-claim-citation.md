# Source Traceability and Claim Citation

Use this file when the research involves producing structured claims, investment memos, competitive analysis, or any output where readers need to audit the origin of each key conclusion.

Do not treat a bibliography as the same thing as source traceability. A list of sources at the end of a report does not tell the reader which specific claim came from which source. This file fixes that.

## Core rule

Every important claim needs to be traceable to a specific source and labeled by evidence type. This is not the same as listing sources at the bottom. This is a two-layer system:

- Layer 1: inline claim-level citations in the body text
- Layer 2: a source register at the end mapping each source id to a specific source with type and relevance

**Hard rule: A source list or bibliography appendix does NOT satisfy the traceability requirement.** If the body text has no inline citations but the report has an appendix source list, the traceability discipline is not yet satisfied. The appendix is supplementary; inline citations are mandatory. A report with a bibliography but zero body-level references is a hard-fail. See the format equivalence exemption below for inline citation formats that satisfy this requirement.

## Format equivalence exemption

### Core principle

Traceability > Format consistency. The goal is functional auditability — a human reader must be able to trace every key claim to a specific source. When a non-`[SN]` format provides equivalent or better traceability, it should be accepted.

The hard-fail gate uses a ternary severity (reflected in `checklists/source-traceability.md`):

| Level | Condition | Action |
|-------|-----------|--------|
| 🔴 Hard-fail | 正文无任何形式的行内引用（既无 `[SN]` 也无功能等价格式）| 不可追溯，不交付 |
| 🟡 Conditional pass | 正文有功能等价的非 `[SN]` 格式引用 + 附录有结构化 register | 通过，建议补充 `[SN]` |
| 🟢 Full pass | 正文使用结构化 `[SN]` 行内引用 + 附录有完整 register | 通过 |

**Key distinction:** If the body has zero inline references of any kind — regardless of whether a structured register or bibliography exists in the appendix — it is a hard-fail. A register without body citations does not enable claim-level traceability. The register must be accompanied by body-level references (in any functionally equivalent format) to reach at least conditional pass.

### Route-specific exemptions

#### Academic / Literature Review route
`(Author, Year, Journal/Blog)` format satisfies the inline traceability requirement. This format is the universal standard in academic publishing and is more informative than `[SN]` — a reader can identify the source immediately without cross-referencing an appendix. `[SN]` numbering is recommended for full pass, but functionally equivalent `(Author, Year, Journal)` format alone is sufficient to pass the hard-fail gate (conditional pass; see the ternary severity table above). The source register should still cross-reference these citations with structured entries.

#### Technical Deep-dive route
arXiv ID (e.g., `arXiv:1911.00927`) or DOI (with version) satisfies the inline traceability requirement, provided the appendix source list indexes these IDs under structured entries. These identifiers are globally unique and permanently resolvable.

#### Listed Company / Investment Memo route
Natural language attribution that uniquely identifies a source ("据 FY2025 年报", "招股书披露", "彭博信用卡数据") satisfies the inline traceability requirement, but the source register must still contain structured entries cross-referencing these citations. The natural language text must be specific enough that a reader can locate the exact source entry without ambiguity. To evaluate this: check whether the natural language attribution maps to exactly one register entry. If the register lists multiple annual reports and the body says "据年报" without specifying the year, it is ambiguous and does not qualify. If the register has one annual report and the body says "据 FY2025 年报," it is unambiguous and qualifies.

### What does NOT qualify as equivalent

The following do NOT satisfy the traceability requirement:
- generic section-level bibliography (one source list per section with no per-claim mapping)
- broad attribution ("据市场研究" without naming the specific report or firm)
- bare URLs in the body text without a source register entry
- vague "据公开资料" or "据悉" — these do not enable unique source identification

### Shared-Workflow route coverage

Shared-Workflow reports are not limited to the three route-specific exemptions listed above. The general conditional pass rule applies: any functionally equivalent non-`[SN]` format (Author-Year, arXiv ID, DOI, natural language that uniquely identifies the source) paired with a structured register qualifies for conditional pass. The three route-specific exemptions are explicit examples; Shared-Workflow reports are evaluated against the general functional traceability standard.

### Multi-route reports

When a report declares multiple routes (primary + secondary), a format that matches **any** declared route's exemption qualifies for conditional pass. For example, a report with primary route "Listed Company" and secondary route "Academic / Literature Review" that uses `(Author, Year, Journal)` citations qualifies under the Academic route exemption. A format that does not match any declared route but is still functionally traceable should also be evaluated under the general conditional pass rule.

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

Use a simple `[SN]` format in the body text, where `N` is a source number. (See the [Format equivalence exemption](#format-equivalence-exemption) section above for route-specific alternatives that satisfy the traceability requirement without using `[SN]` numbering.)

Examples:

- `MTT S5000 is positioned as the current flagship AI chip [S01][S03].`
- `The company filed for STAR Market IPO in June 2025 [S01].`
- `Qwen3.5 compatibility was announced via a press release [S04]; GLM-5 compatibility remains unconfirmed at the time of writing [U01].`
- `三星已量产HBM4 [S3]` (body) → `[S3] Samsung Semiconductor, 2026-03-18, Press Release` (appendix)

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

### Structured Source Register Template

Beginning from this version, the source register appendix must use the following 7-column structure. This template makes source traceability part of the writing process rather than a post-audit fix: the author fills the register while drafting, inline `[S#]` references point to register rows, and the `Claims Supported` column links each entry back to the body section.

```
| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|-----------------|
| S01 | [来源名/标题] | primary | YYYY-MM-DD | [URL 或 DOI] | high | § 相关章节 |
```

**Column definitions:**

| Column | Content |
|--------|---------|
| ID | `S#` identifier (S01, S02, …) matching inline `[S#]` body citations |
| Source Name | Source title, document name, or descriptive label |
| Source Type | One of: `primary` (官方/监管文件/公司公告), `secondary` (媒体/分析师/第三方), `inferred` (报告自身推断), `vendor-claim` (厂商自述，非独立验证), `unconfirmed` (无法独立验证) |
| Date | Source publication date or retrieval date in `YYYY-MM-DD` format |
| DOI/URL | Resolvable link where available; for offline sources, note the limitation |
| Reliability | One of: `high` (独立可验证官方源), `medium` (可靠第三方), `low` (厂商自述/推断/未确认) |
| Claims Supported | Body section references (e.g. `§3.2, §4.1`) that this entry supports — establishes reverse traceability from register to body |

**Cross-reference rule:** Body `[S#]` citations point to the ID column; the `Claims Supported` column points back to body sections. A register entry should be removed if none of its listed sections actually cite it, or a body citation should be added.

**Source Type notes:**
- `primary` — official regulatory filings, annual reports, company press releases, government data
- `secondary` — media articles, analyst reports, third-party research
- `inferred` — report's own reasoning chain (must include inference documentation — see §Inference documentation below)
- `vendor-claim` — manufacturer self-reported data without independent verification
- `unconfirmed` — found in one or more sources but cannot be independently verified

If the existing granular classification (`PRIMARY_FILING`, `SECONDARY_MEDIA`, etc. — see §Source type classification below) better suits a specific entry, use it instead; the template can accommodate either level of detail.

## Register completeness

Every source register entry must satisfy two additional rules beyond basic metadata:

1. **Every entry must be cited in the body.** Each `[S#]` in the register must have at least one inline reference in the body text. Uncited entries should be removed or a body reference added. A reader who sees an entry in the register will assume it was cited somewhere; uncited entries create false audit expectations.

2. **Every entry should include a URL or DOI where available.** For primary filings, company disclosures, news articles, and analyst reports, a resolvable link enables readers to independently verify the source. For offline sources (printed books, internal data), note the limitation explicitly. For high-reliability government or academic sources where a specific URL cannot be provided, the entry should include enough retrieval information (institution, publication, date, archive location) for a reader to locate the source.

These rules prevent the "register theatre" problem where a source list looks comprehensive but contains dead or unreferenced entries.

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

## Mixed-evidence weighting for tier / positioning memos

When a report judges whether a company belongs in the `first tier`, `top tier`, or a global lead group, traceability is not enough by itself. The reader also needs to see which parts of the judgment rest on direct evidence and which parts rest on inference.

For load-bearing positioning claims, do not let these evidence types blur together:

- official current specs
- audited or filed financial disclosures
- official current product pages
- independent third-party market data
- self-tested benchmark claims
- customer anecdotes or partner marketing
- media reports about unreleased roadmap products
- model inference or synthesis

If several of these appear in one section, the body text should make the weighting visible rather than only listing sources at the end.

Good pattern:
- `Current revenue inflection is directly supported by the annual report [S01], but the claim that this already proves global first-tier commercial traction is still an inference [I01].`
- `Current-chip specs are directly sourced [S02], while the conclusion that performance is "about A100 level in broad deployment" relies partly on vendor or customer test material and should remain qualified [S05][I02].`

Bad pattern:
- one polished sentence that mixes audited revenue, self-tested performance, partner statements, and roadmap rumors under one confidence label

## Load-bearing claim rule

If a report's bottom-line judgment depends on a small number of crucial claims, each of those claims should be visibly auditable in the body.

For each load-bearing claim, try to make visible:

- source id
- source type
- whether the claim is direct or inferred
- the main limitation if the evidence is indirect

If the report uses confidence labels but hides the source type and inference role for the key judgment, it is still not adequately auditable.

### Thesis-bearing claim guard

Treat a claim as thesis-bearing when weakening or removing it would materially change:
- the bottom line
- the main ranking or recommendation
- the confidence level
- the valuation / timing / upside-downside framing
- the reader's view of the core thesis

Typical thesis-bearing claims in listed-company work include:
- cost advantage vs peers
- current market-position or ranking claims
- dividend superiority or valuation-support claims
- event-to-thesis claims such as asset injection -> growth, financing -> rerating, restructuring -> margin improvement
- commodity-price or market-cycle assumptions that materially support the thesis
- claims that a certain business segment is the key driver of the current view

For these claims, bibliography-level traceability is not enough.

The body text should make visible, at minimum:
- what the claim is
- which source or evidence bucket supports it
- whether it is directly stated or inferred
- what key limitation or dependency still applies if the evidence is indirect

Bad pattern:
- a polished sentence makes a strong comparative or forward-looking claim
- the reader sees confidence labels or a source list
- but cannot tell which exact source does the real work for that sentence

Good pattern:
- `长协占比较高这一事实可由年报经营披露支持 [S03]；但“煤价敏感度仅为行业平均三分之一”仍属于基于同业比较和经营结构的推断 [I02]。`

If a thesis-bearing claim cannot be made auditable in the body without awkwardness, that is usually a sign the claim should be narrowed, split, or downgraded.

## 来源标注一致性 — Register-to-body label consistency

使用 Source Register 时，register 对某个来源的可靠性/角色标注必须 ≥ 正文引用该来源时使用的标签强度。

具体规则：

- 当 register 标注某来源为 **厂商自述 / manufacturer self-reported**（如 `PRIMARY_COMPANY`、`PRIMARY_PARTNER`、或 register Notes 列注明"厂商自述"），正文引用该来源的数据时必须附加内联说明，如 `(来源：厂商自述，非独立验证)`，不得单独使用 `[已确认事实]`
- 当来源为 **媒体估计**（SECONDARY_MEDIA 类型，如彭博、券商研究报告等第三方推断），正文不得标注为 `[已确认事实]`；应使用 `[推断]` 或具体角色如 `[彭博 estimate]`
- 核心原则：**正文标签强度 ≤ register 标签强度**。register 标注弱于正文时视为标签通胀，应修正

> 注：正文标签 `[已确认事实]` 通常对应 register 中的 `PRIMARY_FILING` 或等效高可靠性类型；`[推断]` 对应 `SECONDARY_MEDIA`、`SECONDARY_ANALYST`、`INFERRED`；`[未知]` 对应 `UNCONFIRMED`、`WEAK_SIGNAL`。此映射为经验性参考，具体 case 由审计员根据证据强度判断。

例外：如果 register 本身将某个来源明确标为 `PRIMARY_FILING` 或等效高可靠性类型，且正文标签与之匹配，则无需额外 caveat。

参见 `references/quantitative-role-labeling.md` §厂商声明与媒体估计的特殊标注规则，获取标注时机判断标准。

## Common failure patterns

### Pattern 1: Bibliography theater

The report lists many sources at the bottom but does not use inline citations. Readers cannot determine which specific claim comes from which source.

**Fix:** Use inline `[SN]` citations for every important claim and map them in the source register.

**Ternary severity (see Format equivalence exemption above):**
- **Hard-fail:** bibliography appendix + zero body-level references of any kind → not deliverable
- **Conditional pass:** bibliography + functionally equivalent non-`[SN]` inline format (Author-Year, arXiv ID, natural language) + structured register → pass, recommend adding `[SN]`
- **Full pass:** structured `[SN]` inline citations + complete register

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
- the report has a long sources list but no inline citations in the body of any kind (neither `[SN]` nor functionally equivalent format)
- a current-state claim is sourced to an old filing with no indication of supersession
- the report's most thesis-bearing sentence would become hard to defend if a reviewer asked `which exact source supports this line?`
- a strong comparative claim is visible in the body, but only a generic section bibliography exists beneath it

## Final discipline

Before finalizing, ask:

- Can I trace every key claim to a specific source entry in the body (via `[SN]` id or functionally equivalent format)?
- Does the source register classify each source by type and date?
- Are inferred claims clearly labeled with reasoning chains?
- Are unconfirmable claims flagged in an uncertainty register?
- Does the report look like it has sources, or does it actually support audit trails?

If any of these are weak, add more citations before publishing.
