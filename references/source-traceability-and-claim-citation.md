# Source Traceability and Claim Citation

Use this file when the research involves producing structured claims, investment memos, competitive analysis, or any output where readers need to audit the origin of each key conclusion.

Do not treat a bibliography as the same thing as source traceability. A list of sources at the end of a report does not tell the reader which specific claim came from which source. This file fixes that.

## Core rule

Every important claim needs to be traceable to a specific source and labeled by evidence type. This is not the same as listing sources at the bottom. This is a two-layer system:

- Layer 1: inline claim-level citations in the body text
- Layer 2: a source register at the end mapping each source id to a specific source with type and relevance

**Hard rule: A source list or bibliography appendix does NOT satisfy the traceability requirement.** If the body text has no inline citations but the report has an appendix source list, the traceability discipline is not yet satisfied. The appendix is supplementary; inline citations are mandatory. A report with a bibliography but zero body-level references is a hard-fail. See the format equivalence exemption below for inline citation formats that satisfy this requirement.

## Source ID format consistency

正文引用 ID 与 Source Register ID 必须完全一致。此规则适用于所有来源 ID 类型——包括 `S`（来源）、`I`/`IN`（推断主张）、`U`/`UN`（未确认主张）。

- `[S1]`（正文方括号无前导零）和 `S01`（Register 前导零无方括号）是**不同格式**。选择一种并在全文中保持统一。
- 同一规则适用于 `[I1]`/`I01` 和 `[U1]`/`U01`：选择一种格式并全文统一。
- 交叉出现两种格式（如正文 `[S1]`、Register `S01`；正文 `[U01]`、Register `U1`）构成格式不一致，即使内容正确也被视为 traceability 纪律的瑕疵。审计时应标记为格式不一致并要求修正。
- 推荐：正文用 `[S01]`、`[I01]`、`[U01]`，Register 用 `S01`、`I01`、`U01`（前导零 + 无方括号）。
- 同一报告内，来源 ID 后缀（数字部分）在 body 和 register 间必须一一对应：register 中的 `S01` 对应 body 中的 `[S01]`，不允许 `S01` ↔ `[S1]` 的跨格式映射。

此规则独立于格式等值豁免：即使使用 Author-Year 等豁免格式，`[SN]`/`[IN]`/`[UN]` 引用（如果存在）与 register ID 的格式也必须一致。

## Format equivalence exemption

### Core principle

Traceability > Format consistency. The goal is functional auditability — a human reader must be able to trace every key claim to a specific source. When a non-`[SN]` format provides equivalent or better traceability, it should be accepted.

The hard-fail gate uses a ternary severity (reflected in `checklists/source-traceability.md`):

| Level | Condition | Action |
|-------|-----------|--------|
| 🔴 Hard-fail | **条件 A：** 正文无任何形式的行内引用（既无 `[SN]` 也无功能等价格式）<br>**或 条件 B：** >3 个 load-bearing claims 在正文中没有 `[Sxx]` 或等效引用；仅使用 `[CONF]/[INFER]` 等角色标签不满足追溯要求——读者无法从主张追踪到具体来源 | 不可追溯，不交付 |
| 🟡 Conditional pass | 正文有功能等价的非 `[SN]` 格式引用（Author-Year / arXiv ID / DOI / 自然语言唯一标识引用）+ 附录有结构化 register | 通过，建议补充 `[SN]` |
| 🟢 Full pass | 正文使用结构化 `[SN]` 行内引用 + 附录有完整 register | 通过 |

**Key distinction:**
- 条件 A：正文零内联引用，无论附录是否有 register 或书目，均为 hard-fail。仅有 register 而无正文引用不满足 claim-level traceability。
- 条件 B：正文有 `[CONF]/[INFER]/[UNKNOWN]` 等置信/角色标签，但 load-bearing claims 缺少 `[Sxx]` 或功能等价的来源级引用，同样为 hard-fail。注意：`[INFER]` 在此指 report-template 中的置信标签体系（`[CONF]/[INFER]/[UNKNOWN]`），**不是** traceability 中的推断标注 `[IN]`（后者附有 register 推理链，是合规的追溯格式）。`[INFER][Sxx]` 组合（置信标签 + 来源引用）为合格。

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

## External research output / Imported report hygiene

When importing or adapting output from external deep-research systems (GPT Deep Research, Claude, Gemini, etc.) as input material, the following hygiene rules apply.

### Citation hygiene

External deep-research systems often use internal citation handles that are not resolvable outside the originating session:

- `turn...` IDs (`turn43view0`, `turn12source1`) are session-internal references — readers cannot open them
- `\ue000cite...` / `\ue001cite` placeholders are GPT-specific rendering artifacts with no meaning outside the chat
- Temporary file IDs (`file-xxxxxxxxxxxx`) are session-scoped and expire

**Rule:** These are NOT valid final-report citations. Before delivery, every external citation handle must be:
1. Resolved into a real URL / DOI / file path and entered into the Source Register, OR
2. Removed from the claim

Example:

- ❌ `MTT S5000 is the current flagship [\ue000cite\turn43view0]`
- ✅ `MTT S5000 is positioned as the current flagship AI chip [S01]` (with S01 in Source Register)

### Asset hygiene

External deep-research outputs may embed chart images from temporary sandbox paths:

- `sandbox:/mnt/data/...` — GPT sandbox path, unreachable after session ends
- `file-service://...` or similar ephemeral URIs

**Rule:** Temporary sandbox image paths are NOT valid final-report assets. Charts or images must be:
1. Regenerated into repository/vault-accessible files with source attribution, OR
2. Replaced with the underlying data table and generation instructions

### What IS allowed

External deep-research outputs may be used as comparison material, structural inspiration, or discovery input. Specifically allowed without restriction:

- analytical structure and judgment framework
- dimension design and evaluation criteria
- choice of comparison scope and methodology
- real, independently accessible URLs or DOIs that the external report references — these are valid candidate sources and should be treated like any other source in the Source Register

Only the internal citation handles and ephemeral asset paths listed above are excluded.

### Relationship to existing rules

These hygiene rules supplement the existing traceability discipline:
- Source Register requirements (see §Structured Source Register Template) still apply
- Format equivalence exemptions (see §Format equivalence exemption) still apply — `(Author, Year)` or `据 FY2025 年报` are valid even in imported content
- The `DISCOVERY` source type restriction (see §Source type classification) still applies: search-level output is not a register entry

> **Automated scanning:** A standalone validator `scripts/validate_external_citation_hygiene.py` can check any report for these hygiene violations. Run `python scripts/validate_external_citation_hygiene.py <report.md>`. Warnings are advisory (exit 0); the script does not block delivery.

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
- `三星已量产HBM4 [S03]` (body) → `S03 Samsung Semiconductor, 2026-03-18, Press Release` (appendix)

Guidelines for inline citations:

- add the citation at the end of the relevant clause or sentence
- when a claim draws from multiple sources, use multiple ids: `[S01][S03]`
- when a claim is inferred and not directly stated in a source, flag it: `[I01]` and explain the inference chain in the source register
- when a claim cannot be confirmed, use `[U01]` and note it in the uncertainty register
- do not cite the same source twice for the same claim in close proximity; one citation per major claim is sufficient
- avoid citing a broad source (e.g., an entire prospectus) without specifying what part of it supports the claim

### Layer 2: Source register

At the end of the report, include a structured source register with at minimum (see the Structured Source Register Template below for the required 7-column format):

- source id matching inline `[S#]` body citations
- source name or title
- source type (simplified 5-class or granular 8-class)
- date in `YYYY-MM-DD` format
- DOI or URL (when available)
- reliability rating (`high` / `medium` / `low`)
- claims supported (§ section references for reverse traceability)

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

The source register appendix must use the following 7-column structure. This template makes source traceability part of the writing process rather than a post-audit fix: the author fills the register while drafting, inline `[S#]` references point to register rows, and the `Claims Supported` column links each entry back to the body section.

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
| Claims Supported | Body section references + brief claim summaries (e.g. `§3.2: 2026 R32 对阵中 A1/B1 等组第一对阵最佳第三；§2.1: 第三名排名规则`). Must include at least a brief description of what each section reference supports — pure section numbers (`§3.2, §4.1`) without claim summaries are insufficient and will be flagged by the validator. |

**Cross-reference rule:** Body `[S#]` citations point to the ID column; the `Claims Supported` column points back to body sections. This creates bidirectional traceability between register entries and body claims.

**Claims Supported semantic requirement:** Each entry in the Claims Supported column must include at least a brief claim-level description beyond section numbers. Acceptable: `§1.1: 2026 R32 对阵中 A1/B1 等组第一对阵最佳第三`。Unacceptable: `§1.1, §2.1` (section-only, no claim summary). A register where all Claims Supported entries are section-only is a hard-fail; a register where some are section-only triggers a warning.

**Source Type notes:**
- `primary` — official regulatory filings, annual reports, company press releases, government data
- `secondary` — media articles, analyst reports, third-party research
- `inferred` — report's own reasoning chain (must include inference documentation — see §Inference documentation below)
- `vendor-claim` — manufacturer self-reported data without independent verification
- `unconfirmed` — found in one or more sources but cannot be independently verified

**Reliability consistency rule:** If Source Type is `vendor-claim`, `inferred`, or `unconfirmed`, Reliability must be `low`. These source types are inherently non-independent or unverified; marking them `medium` or `high` would misrepresent the evidence strength.

**CROWDSOURCED reliability calibration:** CROWDSOURCED sources (Wikipedia, crowdsourced compilations, tertiary sources) must not be rated `high` reliability. The maximum allowed reliability for CROWDSOURCED is `medium`. Default: `medium` for stable/factual consensus articles or `low` for controversial or rapidly-edited topics. A register entry with Source Type = CROWDSOURCED and Reliability = `high` is a hard-fail.

If the existing granular classification (`PRIMARY_FILING`, `SECONDARY_MEDIA`, etc. — see §Source type classification below) better suits a specific entry, use it instead; the template can accommodate either level of detail.

## Register completeness

Every source register entry must satisfy two additional rules beyond basic metadata:

1. **Every entry must be cited in the body.** Each `[S#]` in the register must have at least one inline reference in the body text. Uncited entries should be removed or a body reference added. A reader who sees an entry in the register will assume it was cited somewhere; uncited entries create false audit expectations.

2. **Every entry should include a URL or DOI where available.** For primary filings, company disclosures, news articles, and analyst reports, a resolvable link enables readers to independently verify the source. For offline sources (printed books, internal data), note the limitation explicitly. For high-reliability government or academic sources where a specific URL cannot be provided, the entry should include enough retrieval information (institution, publication, date, archive location) for a reader to locate the source.

These rules prevent the "register theatre" problem where a source list looks comprehensive but contains dead or unreferenced entries.

### Source-strength purity gate

The Source Register is not only about format completeness and body coverage — it must also ensure that sources are strong enough for the claims they support. A report can pass all format checks (7 columns, body [Sxx] references, zero inflation) but still fail audit if the sources themselves are too weak.

**Severity scale for Wikipedia/crowdsourced concentration:**

| Ratio of cited sources that are CROWDSOURCED | Severity | Action |
|----------------------------------------------|----------|--------|
| 100% | 🔴 Hard-fail | Source-traceability may not be marked ✅ Passed. Load-bearing claims must have primary/secondary anchors; Wikipedia is tertiary and cannot serve as the sole source for official rules, current statistics, or strong claims. |
| >50% | 🟡 Warning | More than half of load-bearing claims rely on tertiary sources. Review register: can weak sources be replaced with primary/secondary anchors? |
| ≤50% | 🟢 Pass | Acceptable as long as load-bearing claims are anchored in non-tertiary sources. |

**Counting rules:**
- Only count cited entries (entries whose ID appears as a body `[Sxx]` reference). Uncited Wikipedia entries used for background are not flagged.
- "CROWDSOURCED" is determined by matching the Source Type column against the canonical `CROWDSOURCED` type and its free-text aliases (`Wikipedia`, `wiki`, `crowdsourced`, etc.).

This gate prevents "traceability theatre" — reports where every claim has a citation and every citation has a register entry, but the underlying evidence is too weak to be auditable.

### Register discipline and inflation

The Source Register is not a bibliography-size contest. Each register entry should serve at least one load-bearing body claim, and the body should make that link visible through `[Sxx]` or a functionally equivalent claim-level citation.

Use this severity scale when auditing a register against body citations:

| Uncited register entries | Severity | Action |
|--------------------------|----------|--------|
| `<10%` | Pass | Accept as normal auxiliary sourcing, but remove entries that do not help the report. |
| `10-25%` | Flag | Mark for cleanup; source-traceability can be conditional but should not be described as strong. |
| `>25%` | Register inflation | Source-traceability may not be marked ✅ Passed. Remove unused entries, add real body citations, or move them to a separate extra-reading appendix. |

Uncited entries are especially problematic when they also lack DOI/URL, a clear Source Type, or a plausible `Claims Supported` mapping. In that case, treat them as non-auditable decoration rather than auxiliary evidence; if the pattern is material or numerous, it is a hard-fail for source traceability.

If a report genuinely needs background or extra-reading sources that do not support specific body claims, put them under a separate `Extra Reading` / `Extended Bibliography` heading. Do not count those entries as proof that Source Register traceability passed. A good drafting workflow is: write the body claim with its citation first, then fill the register row that maps back to that claim.

## Source type classification

Classify every source in the register by type. Use these types consistently:

- `PRIMARY_FILING` — official regulatory filing (招股书, 年报, 季报, 交易所公告)
- `PRIMARY_COMPANY` — official company website, press release, official social media, product documentation
- `PRIMARY_PARTNER` — official statement from a named partner or customer
- `PRIMARY_INSTITUTION` — official multilateral, government agency, regulator, or public institution source (not company self-report; no vendor caveat required)
- `PRIMARY_DEV` — official developer material: GitHub repository, issue, PR, release, API docs, changelog, commit log
- `SECONDARY_MEDIA` — news article, industry report, analyst commentary
- `SECONDARY_ANALYST` — analyst report, investment bank research
- `SECONDARY_FEED` — RSS feed, newsletter, curated content stream
- `FILED_DATA_AGGREGATOR` — financial data platform re-presenting filed/regulatory data (Reuters LSEG filed data, Bloomberg filed data, Wind filed data, Choice filed data, StockAnalysis/Macrotrends filed data). Not a primary filing; may support a financial snapshot only when the body marks both (1) source role/caveat such as aggregated filed data or non-original disclosure, and (2) snapshot / metric basis such as snapshot date, fiscal year/TTM, or metric basis.
- `ANALYST_PORTAL_COMPILATION` — portal/compilation mixing analyst estimates, market data, news, or auto aggregation (Finviz, Seeking Alpha, Yahoo Finance when not specifically filed-data). Treat as secondary-like; do not use confirmed labels for claims sourced only to these portals.
- `TRANSCRIPT` — verbatim or near-verbatim transcript of an interview, press conference, earnings call, podcast, tutorial, or presentation
- `INFERRED` — model inference with explicit reasoning chain documented
- `CROWDSOURCED` — Wikipedia, crowdsourced compilation, tertiary sources (must not carry confirmed labels)
- `UNCONFIRMED` — claim found in one or more sources but not independently verified; also covers rumor, leak, unconfirmed attribution (must not carry confirmed labels)
- `WEAK_SIGNAL` — anecdotal, social media, unnamed sources, community forum speculation

**`DISCOVERY` is not a valid Source Register source type.** Search-level discovery results (Exa search summaries, Agent-Reach `POST /search` output) are candidate sources only. They must be recorded in the source intake log (see `references/external-channel-preflight.md`) and may only enter the Source Register after content fetch and reclassification into one of the types above. Body citations of the form `[Sxx]` must never reference raw discovery output.

## Technical Chinese source type mapping

技术类报告 Source Register 中的常见中文来源类型到规范类型的映射。此映射供 `scripts/validate_source_label_consistency.py` 使用，也作为报告编写者的参考。带括号的变体（如"学术综述（arXiv）"）会在查找前剥离括号内容，映射到基础条目。优先使用规范类型而非中文自由文本；中文类型仅为兼容已有报告格式的 fallback。

| 报告常见写法 | 映射规范类型 | 默认最高正文标签 | 说明 |
|---|---|---|---|
| 原始论文 / peer-reviewed paper | PRIMARY_FILING | [确认事实] for paper claims; [推断] for generalization | 只确认论文报告了某实验 |
| arXiv preprint / 学术综述 | SECONDARY_MEDIA | [推断] unless citing paper existence | 预印本状态需说明 |
| 招股书 / 招股说明书 / 年报 / 年度报告 | PRIMARY_FILING | [确认事实] | 监管披露文件 |
| 官方技术文档 / 框架文档 / API 文档 / 技术白皮书 | PRIMARY_DEV | [确认事实] for API/docs existence; caveated for performance/adoption | 厂商自述需 caveat；官方文档映射为 PRIMARY_COMPANY |
| 官方文档 | PRIMARY_COMPANY | [确认事实] + caveat | 产品手册、用户文档等公司发布材料，需内联 caveat |
| 公司公告 | PRIMARY_COMPANY | [确认事实] + caveat | 公司发布的非监管类公告，需 caveat |
| 官方博客 / 官方技术博客 | PRIMARY_COMPANY | [确认事实] + caveat | 厂商自述需 caveat |
| 技术博客 | SECONDARY_MEDIA | [推断] or caveated | 不直接承载 benchmark fact |
| 新闻报道 / 新闻 | SECONDARY_MEDIA | [推断] | 必须标注来源 |
| 行业研究报告 / 券商研报 / 研报 | SECONDARY_ANALYST | [推断] | 不能无 caveat 标 confirmed |
| 社区技术文章 / 博客园 / CSDN / 知乎 | WEAK_SIGNAL | [推断]/[未知] | 只作补充 |
| 微信公众号 / 公众号 | WEAK_SIGNAL | [推断]/[未知] | 只作补充 |
| 多来源综合 / 技术分析 | INFERRED | [推断] | 必须有推理链 |
| 专家访谈 / 访谈 / 财报电话会 | TRANSCRIPT | [确认事实] or [推断] | verbatim → confirmed; summary → inferred |
| Primary (multilateral) / Primary (US govt agency) / government agency / regulator / public agency | PRIMARY_INSTITUTION | [确认事实] | 机构/政府来源，非厂商自述，不需 caveat |
| Primary (vendor) | PRIMARY_COMPANY | [确认事实] + caveat | 厂商自述需 caveat，同其他公司来源处理 |
| Reuters LSEG filed data / Bloomberg filed data / Wind filed data / Choice filed data / StockAnalysis filed data / Macrotrends filed data | FILED_DATA_AGGREGATOR | [确认事实] only with role + basis note | 非 primary filing；可用于 financial snapshot，但正文同句必须同时标明 filed data / aggregated / 非原始披露等来源角色，以及 snapshot date / TTM / fiscal year / metric basis 等口径 |
| Finviz / Seeking Alpha / Yahoo Finance | ANALYST_PORTAL_COMPILATION | [推断]/[未知] | 混合 analyst estimates、market data、news 或 auto aggregation；不得承载 confirmed labels，除非另行证明为 filed-data 口径并改列 FILED_DATA_AGGREGATOR |
| Secondary (crowdsourced) / crowdsourced / Wikipedia / wiki | CROWDSOURCED | [推断]/[未知] | 不可承载 [确认事实] |
| rumor / leak / 传闻 / unconfirmed | UNCONFIRMED | [未知]/[推断] | 不可承载 [确认事实] |

**使用说明：**
- 此映射是示例性而非穷举性。新增常见写法应添加到 `scripts/validate_source_label_consistency.py` 的 `_FREETEXT_TYPE_MAP` 中。
- 带括号的变体（如 `学术综述（arXiv）`）会在查找前剥离括号内容，映射到基础条目。
- 优先使用规范类型（PRIMARY_FILING, SECONDARY_MEDIA 等）而非中文自由文本。中文类型仅为兼容已有报告格式的 fallback。

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

- 当 register 标注某来源为 **厂商自述 / manufacturer self-reported**（如 `PRIMARY_COMPANY`、`PRIMARY_PARTNER`、简化类型的 `vendor-claim`、或 register Notes 列注明"厂商自述"），正文引用该来源的数据时必须附加内联说明，如 `(来源：厂商自述，非独立验证)`，不得单独使用 `[已确认事实]`
- 当来源为 **媒体估计**（SECONDARY_MEDIA 类型，如彭博、券商研究报告等第三方推断），正文不得标注为 `[已确认事实]`；应使用 `[推断]` 或具体角色如 `[彭博 estimate]`
- 当来源为 `ANALYST_PORTAL_COMPILATION`（Finviz、Seeking Alpha、Yahoo Finance 等混合门户/自动聚合），正文不得使用 `[CONF]` / `[确认事实]` / `[Confirmed]` / `[确认]` 等 confirmed labels。
- 当来源为 `FILED_DATA_AGGREGATOR`（Reuters LSEG filed data、Bloomberg filed data、Wind/Choice filed data、StockAnalysis/Macrotrends filed data），它不是 primary filing；若正文使用 confirmed labels，只能确认“该平台 re-presented filed/regulatory data”，且同句必须同时说明两类信息：source role / caveat（如 `filed data`、`aggregated`、`聚合数据`、`非原始披露`）和 snapshot / metric basis（如 `snapshot date`、`TTM`、`fiscal year`、`口径`、`metric basis`）。
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

### Pattern 6: Source ID format mismatch between body and register

正文引用 ID 格式与 Source Register ID 格式不一致。最常见的形式：正文使用 `[S1]`（方括号无前导零），Register 使用 `S01`（前导零无方括号）。当两篇无关报告（月之暗面、MiniMax）出现完全相同的格式不一致时，说明系统缺乏格式一致性约束。

**Fix:** 正文引用 ID 与 Register ID 必须使用相同的数字格式（前导零一致）。推荐格式：正文 `[S01]`，Register `S01`。参见 §Source ID format consistency。

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
