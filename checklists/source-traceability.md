# Source Traceability Checklist

Use this checklist when the output includes confidence labels (confirmed / likely / uncertain) or is structured as a research memo.

Run through every item before delivering the final report.

## Inline citations

- [ ] every important claim in the body text has a source id in `[SN]` format (or functionally equivalent non-`[SN]` format — see format equivalence exemption in `references/source-traceability-and-claim-citation.md`)
- [ ] each `[SN]` maps to a single specific source, not a generic "multiple sources"
- [ ] inferred claims use `[IN]` with a documented reasoning chain in the register
- [ ] unconfirmable claims use `[UN]` and are listed in the uncertainty register

- [ ] **hard-fail gate（阻断级）**: 正文关键主张缺少内联来源引用，满足以下任一条件即**不可交付**：
  - 零正文内联引用——文末有来源列表但正文没有任何 `[Sxx]` 或功能等价格式
  - >3 个 load-bearing claims 在正文中没有 `[Sxx]` 或等效引用；仅使用 `[CONF]/[INFER]` 等置信/角色标签不满足追溯要求（注：`[IN]` / `[UN]` 是 traceability 标注，附有 register 推理链，与 `[INFER]` 置信标签不同，是合规格式）——读者无法从主张追踪到具体来源
  - 例外：等效格式（Author-Year / arXiv ID / DOI / 自然语言唯一标识引用 + 完整 Source Register）通过 conditional pass 等级
  - 另见 `references/source-traceability-and-claim-citation.md` §Source ID format consistency
  - (外部报告导入卫生) 正文存在不可解析的外部深度研究报告引用——`turn\d+` 会话引用、`\ue000cite` / `\ue001cite` 占位符、`sandbox:` 图片路径或临时 `file-` 路径——且未转换为可复核来源或本地资产；注意：等效格式豁免不适用于此规则（`turn43view0` 无论搭配何种 register 格式都不是可追溯引用）→ 任一违规 **不可交付**（参见 `references/source-traceability-and-claim-citation.md` §External research output / Imported report hygiene）

- [ ] **conditional pass**: functionally equivalent non-`[SN]` inline format (Author-Year / arXiv ID / DOI / natural language uniquely identifying the source) + structured register exists → pass with recommendation to add `[SN]` references
- [ ] **full pass**: structured `[SN]` inline citations + complete register

## Source register

- [ ] **hard-fail gate（阻断级）**: Source Register 必须使用 7 列模板（ID / Source Name / Source Type / Date / DOI/URL / Reliability / Claims Supported），定义见 `references/source-traceability-and-claim-citation.md`（§Structured Source Register Template）。缺失 7 列中的任意 1 列 → **不可交付**
- [ ] source register is present and structured (not a loose bibliography)
- [ ] source register uses the 7-column template: ID / Source Name / Source Type / Date / DOI/URL / Reliability / Claims Supported
- [ ] every register entry has a DOI/URL where available; for offline sources, the limitation is noted explicitly
- [ ] every register entry has a `Claims Supported` column with § section references that match body citations
- [ ] Source Type is one of the simplified 5-class system (`primary` / `secondary` / `inferred` / `vendor-claim` / `unconfirmed`) or a compatible granular type (see `references/source-traceability-and-claim-citation.md`)
- [ ] Reliability consistency: if Source Type is `vendor-claim`, `inferred`, or `unconfirmed`, Reliability must be `low`
- [ ] no source id is listed but never cited in the body
- [ ] **register inflation gate**: compare Source Register IDs against body `[Sxx]` references (or functionally equivalent claim-level citations). `<10%` uncited register entries can pass as normal auxiliary sourcing; `10-25%` uncited entries must be flagged for cleanup and may not be used as evidence of strong traceability; `>25%` uncited entries = register inflation and source-traceability may not be marked ✅ Passed.
- [ ] **hard-fail escalation**: uncited register entries that also lack DOI/URL, clear Source Type, or a plausible `Claims Supported` mapping are not valid auxiliary sources; if they are material or numerous, the report is not deliverable until the register is cleaned up or moved to an explicit extra-reading appendix.
- [ ] **CROWDSOURCED reliability gate**: CROWDSOURCED sources (Wikipedia, crowdsourced compilations) must not be rated `high` reliability. The maximum allowed is `medium`. Default: `medium` for stable factual articles, `low` for controversial or rapidly-edited topics. Entries with `CROWDSOURCED + high` are a hard-fail. (See `references/source-traceability-and-claim-citation.md` §Reliability consistency rule)
- [ ] **Claims Supported semantic gate**: every Claims Supported entry must include at least a brief claim description beyond section numbers. Acceptable: `§1.1: 2026 R32 对阵…`; Unacceptable: `§1.1, §2.1` (section-only). A register where all entries are section-only is a hard-fail. (See `references/source-traceability-and-claim-citation.md` §Structured Source Register Template)
- [ ] **source-strength purity gate** (阻断级): check ratio of Wikipedia/crowdsourced sources among cited register entries. `100%` of cited sources are Wikipedia/crowdsourced → hard-fail (source-traceability may not be marked ✅ Passed). `>50%` → warning. Only counts cited entries (body-referenced); uncited Wikipedia background entries are not flagged. (See `references/source-traceability-and-claim-citation.md` §Source-strength purity gate)

## Source type discipline

- [ ] primary sources (official filings, company disclosures, primary documents) are distinguished from secondary (media, analyst reports)
- [ ] [BLOCKER] `SECONDARY_MEDIA` / `SECONDARY_ANALYST` / `SECONDARY_FEED` sources must not be labeled `[确认事实]` / `[CONF]` / `[Confirmed]` in the body. The upper bound for secondary-source labels is `[推断]` / `[INFER]`, per the source-type-to-label mapping table in `references/quantitative-role-labeling.md` (§来源类型到证据标签的校准规则). Exceptions for multi-source cross-validated claims must be explicitly documented.
- [ ] [BLOCKER] `PRIMARY_COMPANY` / `PRIMARY_PARTNER` sources (company self-reports, partner announcements) must carry an inline caveat `(来源：厂商自述，非独立验证)` — they cannot be silently labeled `[确认事实]` without the caveat.
- [ ] inferred claims are labeled `[IN]` and not presented as confirmed facts
- [ ] no source is given higher weight than its type warrants
- [ ] for load-bearing tier / positioning judgments, the body text makes visible which key claims are direct-evidence-backed vs inference-heavy rather than hiding the weighting inside a bibliography or source register
- [ ] self-tests, partner/customer marketing, roadmap reporting, and valuation signals are not allowed to silently carry the same weight as current primary evidence in the final classification

## Completeness

- [ ] no key claim is left without a traceable source
- [ ] the report reads as auditable — a reader can follow any claim back to a specific source entry
- [ ] if a reviewer highlighted the 3-5 sentences doing the most thesis work, each of those sentences would still be defendable without additional hidden notes

## Flags

If any item above is not satisfied, revise the report before delivery. A report without traceability is not a sufficient output of this skill.
