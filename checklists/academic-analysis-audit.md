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

## Search strategy documentation

- [ ] databases searched are listed (Google Scholar, Semantic Scholar, arXiv, PubMed, etc.)
- [ ] search terms are documented
- [ ] date range is specified
- [ ] inclusion/exclusion criteria are stated
- [ ] search completeness is noted (number of results screened, number included)
- [ ] （Tier-1）检索策略已文档化：search strategy is fully documented (database list, search terms with Boolean operators, inclusion/exclusion criteria, screening counts, search date) — required when the report claims "系统化综述" or "有限范围系统化综述"; for non-systematic reviews, document what is feasible
- [ ] if the report claims "系统化综述" or "有限范围系统化综述", the search flow follows PRISMA simplified standards (at minimum: screening counts from initial hits to final inclusion)

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

## Source labeling

- [ ] （Tier-1）来源表逐项包含：title + publication type + peer-review status + venue + DOI/URL + date — per-source academic metadata is complete (see `references/academic-evidence-hierarchy.md`「每个 [S#] 条目必填字段」)
- [ ] all sources have venue information
- [ ] （Tier-1）预印本/工作论文标注 "未同行评审"：preprints are explicitly labeled as "not peer-reviewed"
- [ ] the report does not conflate study design quality with publication venue prestige
- [ ] the report distinguishes between original research and secondary sources
- [ ] Source Register uses the 7-column template (ID / Source Name / Source Type / Date / DOI or URL / Reliability / Claims Supported) defined in `references/source-traceability-and-claim-citation.md` (§Structured Source Register Template). 来源注册表必须使用该 7 列模板。

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
