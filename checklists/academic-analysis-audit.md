# Academic Analysis Audit

Use this checklist before delivery when the primary route is **Academic / Literature Review**.

This checklist verifies that the academic route was executed correctly and the final artifact satisfies its contract.

---

## Route activation

- [ ] the task was explicitly classified as academic literature review, field progress analysis, or paper comparison
- [ ] the academic route was selected as the primary route (not as a secondary discipline)
- [ ] the route conflict check was run: confirmed this is not better served by technical deep-dive, market outlook, or generic research

## Evidence hierarchy compliance

- [ ] （Tier-1）证据分级同时评估研究设计质量和发表场所声誉（双维）：evidence is assessed on two dimensions — study design quality AND publication venue prestige
- [ ] publication type is labeled for each source (published / preprint / conference / working paper / unpublished)
- [ ] peer-review status is labeled for each source (peer-reviewed / not peer-reviewed / unknown)
- [ ] publication venue is specified for each source (journal name, conference name, or repository)
- [ ] discipline-specific venue prestige is respected (e.g., CS conferences are top-tier venues)
- [ ] （Tier-1）证据框架执行检查：如果方法论中声明了双维/多级证据评估框架（如研究设计质量 × 发表场所声誉），正文必须包含逐 source 的 evidence mapping table（至少覆盖主要来源或负载结论的核心来源）。方法论描述了框架但正文未逐 source 落地 → 条件通过上限不可标 ✅；系统性缺失（多数来源无 mapping）→ hard-fail。

## Search strategy documentation

- [ ] databases searched are listed (Google Scholar, Semantic Scholar, arXiv, PubMed, etc.)
- [ ] search terms are documented
- [ ] date range is specified
- [ ] inclusion/exclusion criteria are stated
- [ ] search completeness is noted (number of results screened, number included)
- [ ] （Tier-1）检索策略已文档化：search strategy is fully documented (database list, search terms with Boolean operators, inclusion/exclusion criteria, screening counts, search date) — required when the report claims "系统化综述" or "有限范围系统化综述"; for non-systematic reviews, document what is feasible
- [ ] if the report claims "系统化综述" or "有限范围系统化综述", the search flow follows PRISMA simplified standards (at minimum: screening counts from initial hits to final inclusion)
- [ ] （Tier-1）检索策略措辞纪律：如果报告使用"系统评述"/"系统综述"/"系统化综述"/"systematic review"或类似措辞（含"系统性回顾"/"系统性文献综述"），必须列明完整检索方法（数据库列表、检索日期、Boolean query、纳入/排除标准、screening counts）；缺少任一 → hard-fail。方法学达不到此标准时，应使用"文献回顾"/"literature review"/"narrative review"/"系统检索"/"有限范围系统化综述"/"scoping review"等与透明度匹配的替代措辞。

## Publication bias discussion (发表偏倚)

- [ ] （Tier-1）发表偏倚讨论存在（≥2 句，说明偏倚方向与结论调整）：publication bias is discussed (at least 2-3 sentences covering: direction judgment — whether the evidence set skews toward positive results; conclusion adjustment — how conclusions should be modified if publication bias is likely)

## Statistical assessment (if applicable)

- [ ] statistical claims include effect sizes, not just p-values
- [ ] confidence intervals are provided where relevant
- [ ] sample size adequacy is discussed
- [ ] multiple testing corrections are noted if applicable
- [ ] common statistical pitfalls are acknowledged (p-hacking, cherry-picking, confounding)

## Cherry-picking detection

- [ ] negative or conflicting findings are included alongside positive results
- [ ] the report does not selectively cite papers to support a pre-determined conclusion
- [ ] both supporting and contradicting evidence is presented
- [ ] publication bias is discussed (see「Publication bias discussion (发表偏倚)」section above for detailed requirements)
- [ ] 排除论文正当化：文献综述/论文脉络类报告如果列出了被排除的论文、架构或方法，必须简要说明排除理由及排除是否影响主线结论。仅排列名称不作解释 → cherry-picking 风险未解除标记。不要求 exhaustive justification，但不可仅列名称不说明逻辑。

## Source labeling

- [ ] （Tier-1）来源表逐项包含：title + publication type + peer-review status + venue + DOI/URL + date — per-source academic metadata is complete (see `references/academic-evidence-hierarchy.md`「每个 [S#] 条目必填字段」)
- [ ] all sources have venue information
- [ ] （Tier-1）预印本/工作论文标注 "未同行评审"：preprints are explicitly labeled as "not peer-reviewed"
- [ ] the report does not conflate study design quality with publication venue prestige
- [ ] the report distinguishes between original research and secondary sources
- [ ] source register must use the 7-column template (ID / Source Name / Source Type / Date / DOI/URL / Reliability / Claims Supported) defined in `references/source-traceability-and-claim-citation.md` (§Structured Source Register Template). 来源注册表必须使用该 7 列模板。
- [ ] （Academic）Academic / Literature Review 路线的 Source Register 必须使用 11 列学术扩展模板（7 列基础 + Publication Type / Peer-review Status / Venue / Venue Prestige），定义见 `references/academic-evidence-hierarchy.md`（§Source Register 扩展模板（Academic 专用））——仅限 primary route 为 academic 或 literature review 的报告

## Artifact contract verification

- [ ] for field progress analysis: search strategy, key breakthroughs, current state, open questions, evidence quality
- [ ] for paper comparison: comparison dimensions, paper-by-paper analysis, cross-cutting themes, strengths/weaknesses
- [ ] for technology origin tracing: seminal work, evolutionary steps, current paradigm, evidence quality

## Hard fail check

- [ ] no preprints treated as peer-reviewed without explicit labeling
- [ ] no cherry-picking to support pre-determined conclusions
- [ ] no correlation ≠ causation errors
- [ ] no missing venue information for cited papers
- [ ] no conflation of study design and venue prestige dimensions
- [ ] no ignoring publication bias or the "file drawer problem" — 发表偏倚讨论已按规定完成（至少 2-3 句，涵盖偏倚方向判断和结论调整建议；参见 `references/academic-evidence-hierarchy.md`「发表偏倚讨论」节）
- [ ] （Tier-1）if a secondary route is declared, its hard-fail verification must be itemized (which conditions were checked, which passed/failed, and evidence for each); "covered elsewhere without independent run" constitutes a hard-fail — see ROUTING-MATRIX.md "Secondary route hard-fail requirement"
