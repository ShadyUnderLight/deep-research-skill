# Academic Analysis Audit

Use this checklist before delivery when the primary route is **Academic / Literature Review**.

This checklist verifies that the academic route was executed correctly and the final artifact satisfies its contract.

---

## Route activation

- [ ] the task was explicitly classified as academic literature review, field progress analysis, or paper comparison
- [ ] the academic route was selected as the primary route (not as a secondary discipline)
- [ ] the route conflict check was run: confirmed this is not better served by technical deep-dive, market outlook, or generic research
- [ ] 子风格选择已确认：使用标准 survey-style 还是 field-progress-analysis sub-style；若使用 field-progress，确认触发条件匹配（见 `ROUTING-MATRIX.md`「子风格选择指引」）

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

## Current-state discipline

Current-state verification for academic reviews has different semantics than product/company current-state checks. The core contract: academic reviews have an inherently time-bound "current state" — the coverage window determines what the report can legitimately claim as current.

- [ ] coverage window 显式声明：报告正文（非仅方法论段落）必须声明 literature coverage window（如"本综述覆盖截至 YYYY 年末的文献"）。若报告日期距最新 verified source 超过 12 个月，不得声称 current SOTA / latest debate / 当前前沿 / 最新进展。可选项：a) 执行 current-state refresh 更新覆盖窗口，或 b) 将报告降级为 historical snapshot 并在标题、opening、结论中同步降级
- [ ] 结论绑定 coverage window：结论区的措辞必须与 coverage window 一致。若覆盖到 2024 年末，结论应写"截至 2024 年末的学术分析"，不得写成"当前学术争议全景"或"最新进展综述"。若近期论文（报告日期 3 个月内）的 peer-review 状态未确认，结论不得以高置信度使用这些论文支撑核心论点
- [ ] （Tier-1）近期来源 peer-review 验证：对报告日期前 3 个月内的来源，若 Source Register 中标注为 peer-reviewed 或同等状态，必须包含可见核验证据（proceedings link / OpenReview / publisher page / official accepted list）。仅有 arXiv URL 且无其他验证证据 → 状态应降级为 preprint / accepted-pending / under review。此规则防止 preprint → peer-reviewed 的 evidence level 过度上调

## Benchmark comparability

此章节适用于报告中涉及多模型 AI benchmark 比较、benchmark 分数支撑能力声称、或讨论 benchmark 有效性争议的场景。若不满足触发条件，可跳过此章节。

- [ ] 触发条件检查：报告是否包含多模型 benchmark 对比、能力领先声称、benchmark 分数支撑推理能力声称、或 leakage / contamination / no-image baseline 讨论；若不属于任一类，此章节可跳过
- [ ] each load-bearing benchmark comparison includes: Benchmark / Task, Capability claim, Model / version, Dataset split / version, Prompt / eval protocol, Metric, Baseline / no-input control, Source role, and Comparability caveat — per `references/academic-evidence-hierarchy.md` §Benchmark comparability for academic reviews
- [ ] no-image / text-only baseline 被视为重要反证：当模型在视觉推理任务上显著领先时，若缺少 no-image baseline 或 text-only baseline，不可排除语言捷径（language shortcut）作为竞争解释；缺少 baseline 的领先声称应降级
- [ ] cross-source benchmark numbers 不直接横比而不注明 comparability caveat：不同 prompt 设定、不同数据集切分、不同评估实现的分数不可直接并列比较而无限制说明
- [ ] （Tier-1）当 benchmark comparability schema 在 load-bearing comparison 中严重缺失（3+ 字段不可用，或无 dataset/protocol 信息），report 结论被降级为方向性判断而非强排名；若结论未做对应降级 → hard-fail。此规则防止 schema 不完整时结论过度声称
- [ ] （non-blocking / 可读性检查）当报告中涉及 3+ benchmark 或 3+ 模型比较时，建议使用结构化对比表（见 `references/academic-evidence-hierarchy.md` §Benchmark comparison table template）而非 prose 段落，以提高信息密度和可扫描性

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

### For standard academic survey (文献综述，默认)
- [ ] scope of review (time period, sub-fields covered, search strategy)
- [ ] key research themes and trends
- [ ] major breakthroughs and milestones
- [ ] current state of the art
- [ ] open questions and future directions
- [ ] evidence quality assessment

### For field-progress analysis (子风格)
- [ ] opening verdict: thesis-first judgment in opening 10-15% (progress confirmed, main limits, evidence that overstates/understates, applicability boundary)
- [ ] scope and search strategy (same as survey-style)
- [ ] mechanism or benchmark ladder: at least one of mechanism map / benchmark ladder / evidence ladder
- [ ] representative failure cases: 3-5 specific cases with task, ground truth, failure mode, mechanism link, source citation
- [ ] conditions that would change the conclusion: what evidence would increase confidence, what would reverse judgment
- [ ] evidence quality assessment
- [ ] research/practice next steps (recommended, non-blocking)

### For paper comparison
- [ ] comparison dimensions, paper-by-paper analysis, cross-cutting themes, strengths/weaknesses, recommendations for practitioners

### For technology origin tracing
- [ ] seminal work, evolutionary steps, current paradigm, evidence quality

## Hard fail check

- [ ] no preprints treated as peer-reviewed without explicit labeling
- [ ] no cherry-picking to support pre-determined conclusions
- [ ] no correlation ≠ causation errors
- [ ] no missing venue information for cited papers
- [ ] no conflation of study design and venue prestige dimensions
- [ ] no ignoring publication bias or the "file drawer problem" — 发表偏倚讨论已按规定完成（至少 2-3 句，涵盖偏倚方向判断和结论调整建议；参见 `references/academic-evidence-hierarchy.md`「发表偏倚讨论」节）
- [ ] （Tier-1）no secondary route hard-fail verification skipped without itemization: when a secondary route is declared, its hard-fail verification must be itemized per condition (which were checked, which passed/failed, and evidence for each); "covered elsewhere without independent run" constitutes a hard-fail — see ROUTING-MATRIX.md "Secondary route hard-fail requirement"

## Eval regression cases

The following eval cases guard academic-review delivery discipline against real failure patterns. Run or review them as part of the regression set when modifying academic route rules, checklists, or validators:

- `evals/cases/ai-agent-planning-academic-review-compounded-case.md` — compounded academic fail: search strategy incomplete + stale current-state + source register placeholder + evidence matrix not executed + self-assessment overclaim. Expected verdict: **Fail**.
- `evals/cases/mllm-visual-reasoning-academic-review-narrow-fail-case.md` — narrow fail: body traceability absent (zero `[S##]`) while all other academic disciplines pass. Expected verdict: **Conditional Pass**.
