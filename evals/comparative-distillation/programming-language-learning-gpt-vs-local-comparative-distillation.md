# Programming Language Learning GPT-vs-Local Comparative Distillation

> **Purpose:** Compare GPT deep research and local deep-research-skill reports on which programming language (Swift, Kotlin, Rust, Python) to systematically learn in 2026 — to identify and close proxy indicator discipline, scope declaration, and evidence traceability gaps in career/skill-selection constrained-choice reports.

---

## Case identity

- **Case name:** Programming language learning GPT-vs-local comparative distillation
- **Date:** 2026-06-16
- **Research question:** Which programming language (Swift, Kotlin, Rust, Python) should an individual learner systematically study in 2026?
- **Why this comparison matters:**
  - Career/skill-selection reports rely heavily on **second-order proxy indicators** (job postings, salary surveys, TIOBE ranking, GitHub stars, Stack Overflow survey percentages) that look quantitative but carry fundamentally different epistemic weights.
  - The local report exhibited a cluster of related proxy discipline failures — unlabeled proxy indicators in comparison tables, missing scope declaration for US-vs-global data, bare learning time estimates, and self-assessment overclaim — that together define a distinctive failure mode for career/skill-selection constrained-choice reports.
  - This comparison is the original motivation for [#308](https://github.com/ShadyUnderLight/deep-research-skill/issues/308) (career/skill-selection proxy evidence discipline) and provides the evidential basis for the eval case at `evals/cases/career-skill-selection-proxy-discipline-case.md`.
- **Report A (GPT):** GPT deep research report on programming language learning value (Swift / Kotlin / Rust / Python)
- **Report B (Local):** `2026年编程语言学习价值深度研究报告.md` — local deep-research-skill report on the same question
- **Reference / stronger report (if any):** GPT for market scope declaration, proxy variable labeling, keyword bias explanation, and segmented recommendations; Local for route/audit structure and persona breakdown
- **Prompt(s):** Same research question, independently generated
- **Important scope or timing differences:**
  - Both reports cover the same 2026-timeframe question with comparable source windows
  - GPT report was generated via GPT deep research interface; local report via deep-research-skill pipeline
  - Comparison focuses on structural discipline (scope declaration, proxy labeling, source traceability, decision architecture), not factual retrieval accuracy

---

## Comparison purpose

This comparison is **not** for deciding which system is "better."

It is for:

1. Identifying which GPT structural patterns (market scope declaration, proxy indicator labeling, keyword bias explanation, learning-time basis notes) are worth absorbing into the career/skill-selection constrained-choice route.
2. Verifying that all identified gaps are now covered by [#306](https://github.com/ShadyUnderLight/deep-research-skill/issues/306), [#308](https://github.com/ShadyUnderLight/deep-research-skill/issues/308), and [#309](https://github.com/ShadyUnderLight/deep-research-skill/issues/309).
3. Determining whether each gap was a **missing rule**, **missing trigger**, or **execution failure**.
4. Registering this pair as a regression asset for future career/skill-selection constrained-choice improvements.

**Because all identified gaps have already been addressed by closed issues, this file serves primarily as a regression audit asset rather than a gap-discovery artifact.**

---

## Dimension 1: Current-state discipline (market scope, reader persona, time window)

### Report A (GPT)
- **Explicit market scope declared first** — opens with a clear statement that the analysis prioritizes the US/global English-speaking market and acknowledges geographic bias
- Job numbers, salary data, and ecosystem size metrics are handled as **proxy variables** with explicit limitations stated (keyword mismatch, self-selection bias in surveys, geographic concentration of certain roles)
- **Keyword bias acknowledged** — notes that job posting counts for "Python" conflate software engineer, data scientist, ML engineer, and DevOps roles under one keyword
- **Incomparable metrics explained** — warns that TIOBE rank, Stack Overflow usage %, GitHub PR count, and job posting volume measure different things and should not be directly compared
- Recommendations are **segmented by experience level** (zero-base, 1-3 year, 3-5 year, 5+ year)
- Learning time estimates are labeled as **decision-type estimates** (not precise predictions)
- Weakness: uses `turn...` citation format; no 7-column Source Register; no formal route/audit status block; no claim-level audit trail

### Report B (Local)
- Has a **route/audit/status structure** — route declaration, evidence matrix, audit status block are all present
- **Persona breakdown** — identifies distinct reader profiles (beginner, mid-career switcher, experienced engineer looking for second language)
- **Ranking with reversal conditions** — per-persona rankings are given with explicit conditions under which the recommendation would change
- **Structured opening** — follows template structure, opens with route metadata and scope
- Weakness: **missing market scope declaration** — US salary data mixed as if global without geographic scope note; no "this analysis prioritizes market X" upfront
- Weakness: no explicit **time window** for the analysis (is this "learn now for jobs in 2026" or "learn now for career in 2027-2030"?)

### Gap
- GPT is stronger at **front-loading market scope** — the reader immediately knows which market is being analyzed and what data limitations apply
- Local report has the structural components (route, audit, persona) that GPT lacks, but omits the **basic scope declaration** that would prevent a reader from mistaking US salary data for global
- The gap is a **missing template block** — the report template for career/skill-selection tasks did not require an explicit market/scope declaration at the time

### Current status
✅ 已由 [#309](https://github.com/ShadyUnderLight/deep-research-skill/issues/309) 修复：
- `references/decision-report-template.md` 新增 Decision Scope 块，强制前置 target reader, market, decision goal, time window
- `checklists/option-selection-final-audit.md` 新增 career/skill-selection sub-gate，检查 scope 声明完整性
- 要求 scope 中明确数据地理范围（如 "US salary data, not global"）

### Eval regression assets
- `evals/cases/career-skill-selection-proxy-discipline-case.md` — 综合 eval 覆盖 Decision Scope 块要求

### Action type
`NO_ACTION` — 规则已覆盖，有专用 eval case

---

## Dimension 2: Numerical and date discipline (proxy indicator labeling, salary scope, learning time estimates)

### Report A (GPT)
- **Proxy indicators explicitly labeled by role** — TIOBE ranked as "search/attention proxy," job postings as "keyword-based demand proxy," salary surveys as "self-selected sample proxy"
- **Salary scope declared** — US Bureau of Labor Statistics and Levels.fyi data explicitly scoped to US market; notes that non-US salaries are systematically lower
- **Learning time estimates labeled with basis** — "6-12 months to job-ready (estimate based on average bootcamp-to-employment trajectories, with wide variance by prior experience and daily study hours)"
- **Keyword bias and incomparable metrics explained** — each proxy type comes with a brief limitation note

### Report B (Local)
- **Source Register missing Claims Supported column** — register entries exist but don't specify whether a source is used for job proxy, salary proxy, ecosystem size, official roadmap, or community preference
- **Numeric/role labels missing from comparison tables** — TIOBE rank, SO usage %, package count, GitHub stars, US salary range all in one table without role labels (observed/proxy/assumption/model-output)
- **US salary data mixed as if global** — US-specific salary figures presented alongside global rankings without scope declaration
- **Learning time estimates bare without basis** — "6 months" or "1-2 years" stated without explanation of what the estimate is based on or what variance to expect
- **Composite scores (A+/B+) without input-role transparency** — aggregated scores derived from mixed-proxy inputs without showing how each proxy was weighted

### Gap
- Core gap: **proxy indicator conflation** — the local report placed fundamentally different data types (TIOBE ranking = search attention signal; LinkedIn job count = keyword-based demand proxy; Levels.fyi salary = US self-selected sample) into the same comparison table without role labels
- Learning time estimates were presented as bare durations, creating an illusion of precision without traceable basis
- US-vs-global scope confusion made the salary comparison misleading
- This is the classic career/skill-selection failure mode that [#308](https://github.com/ShadyUnderLight/deep-research-skill/issues/308) was designed to catch

### Current status
✅ 已由 [#308](https://github.com/ShadyUnderLight/deep-research-skill/issues/308) 修复：
- `references/option-selection-and-shortlist-discipline.md` 新增 §Common proxy indicators for career/skill selection，要求按来源类型做 role labeling
- `checklists/option-selection-final-audit.md` 新增 career / skill selection sub-gate，强制执行 scope、proxy roles、US-vs-global boundary
- 缺少 scope 或超过 3 个 load-bearing 数字未标 proxy role 时触发 BLOCKER
- `references/source-register.md` 已规范 Claims Supported 列，要求按 claim type 分类

### Eval regression assets
- `evals/cases/career-skill-selection-proxy-discipline-case.md` — 核心 eval case，覆盖 proxy indicator role labeling

### Action type
`NO_ACTION` — 规则已覆盖，有专用 eval case

---

## Dimension 3: Source traceability and evidence weighting (Source Register, body citations, self-assessment)

### Report A (GPT)
- Uses `turn...` session-internal citation handles — **unreachable outside the originating GPT session**
- No 7-column Source Register
- No formal route/audit status block
- Claim-level attribution density is high (each key claim has a citation), but citations are non-reproducible
- **Undeliverable** under the repo's final-audit hygiene rules

### Report B (Local)
- **Has route/audit/status structure** — route declaration, evidence matrix, audit status block with check marks
- **Source Register exists but incomplete** — registered sources but missing Claims Supported column; cannot tell which sources back which claim types
- **Body-level `[Sxx]` citations absent** — body text lacks claim-level citations; sources are registered but not connected to specific claims in the body
- **Self-assessment claimed all ✅ while gaps existed** — audit status claimed full pass on proxy labels, scope declaration, and body traceability even though:
  - comparison tables mixed proxy indicators without role labels
  - US salary data was not scoped
  - learning time estimates were bare
  - body lacked `[Sxx]` citations
  - This constitutes a **process-integrity hard-fail**

### Gap
- Local report has the **structural advantage** of having route/audit/status infrastructure at all (GPT has none of this)
- But local report's self-assessment is **inaccurate** — claims full pass while clear gaps exist
- Body-level `[Sxx]` citations missing means individual claims cannot be traced to specific sources
- Source Register Claims Supported column missing means the register is structured but not informative about evidence roles
- This is a **wiring/execution gap** — rules for self-assessment accuracy and body-level citations existed but the constrained-choice route wasn't wired to enforce them for career/skill-selection reports

### Current status
✅ 已由 [#306](https://github.com/ShadyUnderLight/deep-research-skill/issues/306) 修复：
- `scripts/audit_report.py` 新增 constrained-choice / option-selection / shortlist route mapping
- Career/skill-selection 子类型被识别为 constrained-choice route 子类，触发所有相关 validator
- Process-integrity gate 在交付前强制检查自评与执行的一致性
- 7 列 Source Register 含 Claims Supported 列为必填

### Eval regression assets
- `evals/cases/career-skill-selection-proxy-discipline-case.md` — 综合 eval 覆盖 source traceability + self-assessment accuracy

### Action type
`NO_ACTION` — 规则已覆盖，validator 链已接入，有专用 eval case

---

## Dimension 4: Forward-looking claim discipline (learning outcome claims, career predictions)

### Report A (GPT)
- **Learning outcomes labeled as estimates** — "6-12 months to job-ready (estimate, wide variance)" with explicit variance acknowledgment
- **Career predictions qualified** — "If current growth rate continues, Rust roles may grow 20-30% over 2 years but from a small base" — includes both direction and base-rate caveat
- **Explicitly separates current-state from forward-looking** — what we know now vs. what depends on future industry conditions
- **Reversal conditions implicit** — conditions under which the recommendation changes are embedded in the narrative but not structured as a standalone list

### Report B (Local)
- **Ranking with reversal conditions** — per-persona rankings explicitly state conditions under which recommendation would change (e.g., "if Rust ecosystem maturity improves within 2 years, it overtakes Kotlin for backend roles")
- **Forward-looking section bound to evidence** — career predictions cite specific trends (market reports, OSS activity, major employer adoption)
- **Counter-evidence section** — acknowledges arguments for and against each language
- Weakness: **learning time estimates bare** — "6 months for Python" without basis or variance
- Weakness: **career projections lack base-rate caveat** — "Rust is growing fast" without noting it is growing from a small base
- Weakness: **persona table introduced TypeScript/Go as external options** without explaining why they are outside the shortlist (shortlist boundary leak)

### Gap
- Local report's reversal conditions are a structural strength that GPT lacks
- But bare learning time estimates and missing base-rate caveats are a **calibration gap** — the local report gives stronger-seeming predictions than the evidence supports
- Shortlist boundary leak (TypeScript/Go introduced without explanation) is a **shortlist discipline gap** — if they are valid options, they should be in the shortlist; if not, they shouldn't appear as unlabeled alternatives

### Current status
✅ 已由 [#308](https://github.com/ShadyUnderLight/deep-research-skill/issues/308) 和 [#309](https://github.com/ShadyUnderLight/deep-research-skill/issues/309) 共同覆盖：
- [#308](https://github.com/ShadyUnderLight/deep-research-skill/issues/308)：career/skill-selection proxy discipline 要求学习时间估算必须有 basis note
- [#309](https://github.com/ShadyUnderLight/deep-research-skill/issues/309)：Decision Scope 块定义 option universe + explicit exclusions，防止 shortlist boundary leak

### Eval regression assets
- `evals/cases/career-skill-selection-proxy-discipline-case.md` — 约束 forward-looking claim discipline

### Action type
`NO_ACTION` — 规则已覆盖

---

## Dimension 5: Structural readability and information density (route/audit status, opening structure, shortlist boundary)

### Report A (GPT)
- Opens with **judgment + scope** — "this analysis covers the US/global market for 2026-2028 career investment; here is what the data shows"
- **Proxy variable explanation before comparison** — explains what each metric means and its limitations before presenting any numbers
- **Recommendation tables with role labels** — tables include column headers that identify what each metric represents
- No route/audit/status block — structurally simpler but skips a layer of metadata that the repo requires
- Weakness: no route/audit status section (repo requirement), no formal decision scope block

### Report B (Local)
- **Route/audit/status structure** — has the full route metadata block required by the repo
- **Persona breakdown table** — clearly identifies three reader profiles
- **Ranking with reversal conditions** — explicitly structured
- Weakness: **metadata-first drift** — route metadata and audit status appear before the judgment
- Weakness: **shortlist boundary leak** — TypeScript and Go appear in the persona table as external options without explanation of why they are outside the shortlist
- Weakness: **comparison tables lack numeric/role labels** — proxies mixed in one table without distinguishing markers

### Gap
- GPT has better **judgment-first opening** (reader knows the answer before the methodology)
- Local has better **structured metadata** (route, audit, persona breakdown) but presents it at the expense of the first-screen judgment
- Shortlist boundary leak is a **constrained-choice discipline gap** — if TypeScript/Go are mentioned as alternates, the reader should be told why they were excluded
- Comparison tables without role labels make it hard for the reader to differentiate data types

### Current status
✅ 已由 [#306](https://github.com/ShadyUnderLight/deep-research-skill/issues/306) 和 [#309](https://github.com/ShadyUnderLight/deep-research-skill/issues/309) 修复：
- [#309](https://github.com/ShadyUnderLight/deep-research-skill/issues/309)：强制 judgment + Decision Scope 在 route metadata 之前
- [#306](https://github.com/ShadyUnderLight/deep-research-skill/issues/306)：route wiring 确保 constrained-choice 规则（含 shortlist 范围、table role labels）对所有子类型触发

### Eval regression assets
- `evals/cases/career-skill-selection-proxy-discipline-case.md` — 约束 first-screen clarity + scope block placement

### Action type
`NO_ACTION` — 规则已覆盖

---

## Dimension 6: Decision usefulness (per-persona recommendation, ranking logic, reversal conditions)

### Report A (GPT)
- **Recommendations segmented by experience level** — zero-base, 1-3 years, 3-5 years, 5+ years each get a different recommendation
- **Each recommendation explains why** — not just "Python for beginners" but "Python for beginners because: lowest time-to-productivity, largest learning ecosystem, most forgiving error model, widest initial job market"
- **Trade-offs explicit** — "Rust pays more but takes longer to reach job-ready proficiency; Python pays less initially but has faster ramp to employability"
- Weakness: **ranking logic implicit** — the weighting criteria are described in prose rather than a replicable scoring framework

### Report B (Local)
- **Per-persona recommendations** — distinct recommendations for beginner, mid-career switcher, experienced engineer
- **Ranking with reversal conditions** — explicitly states when one recommendation would overtake another
- **Comparison framework present but opaque** — variables are defined but the mapping from variables to ranking is not transparent
- Weakness: **composite scores (A+/B+) lack transparency** — reader cannot see how individual proxy indicators map to the overall score
- Weakness: **learning time estimates used comparatively without basis** — "Python 6 months vs Rust 18 months" suggests precision that doesn't exist
- Weakness: **TypeScript/Go in persona table without explanation** — confuses the decision frame

### Gap
- GPT is better at **explaining why one option wins** for each persona because it connects the recommendation to specific learner-relevant factors
- Local's reversal conditions are a structural strength, but the composite scores and bare learning estimates undermine the reader's ability to independently evaluate the recommendation
- The fundamental gap is **scoring transparency** — the reader can see the conclusion but not how the report got from evidence to ranking
- GPT's recommendation structure (per-persona + why + trade-off) is a strong pattern for career/skill-selection decision memos

### Current status
✅ 已由 [#306](https://github.com/ShadyUnderLight/deep-research-skill/issues/306)、[#308](https://github.com/ShadyUnderLight/deep-research-skill/issues/308)、[#309](https://github.com/ShadyUnderLight/deep-research-skill/issues/309) 联合覆盖：
- [#306](https://github.com/ShadyUnderLight/deep-research-skill/issues/306)：route wiring 确保 constrained-choice 的所有 validator 稳定触发，包括 scoring replicability
- [#308](https://github.com/ShadyUnderLight/deep-research-skill/issues/308)：proxy indicator discipline 要求每个 proxy 维度标注角色和约束，使读者可以独立判断权重
- [#309](https://github.com/ShadyUnderLight/deep-research-skill/issues/309)：Decision Scope 块强制列出 option universe 和 exclusion 原因

### Eval regression assets
- `evals/cases/career-skill-selection-proxy-discipline-case.md` — 综合 eval 覆盖决策有用性的所有方面

### Action type
`NO_ACTION` — 规则已覆盖

---

## Candidate-action summary

| # | Candidate action | Failure family | Action type | Proposed home |
|---|---|---|---|---|
| 1 | Constrained-choice audit_report total control | route-wiring / process-integrity | `NO_ACTION` | Already closed by [#306](https://github.com/ShadyUnderLight/deep-research-skill/issues/306) |
| 2 | Career/skill-selection proxy evidence discipline (checklist sub-gate + scope declaration + proxy indicator table) | numerical-discipline / proxy-conflation | `NO_ACTION` | Already closed by [#308](https://github.com/ShadyUnderLight/deep-research-skill/issues/308) |
| 3 | Decision Scope block in template (target reader, option universe, exclusions, time window) | current-state / opening-flow | `NO_ACTION` | Already closed by [#309](https://github.com/ShadyUnderLight/deep-research-skill/issues/309) |
| 4 | Self-assessment accuracy gate for constrained-choice | process-integrity | `NO_ACTION` | Already closed by [#306](https://github.com/ShadyUnderLight/deep-research-skill/issues/306) |
| 5 | Source Register Claims Supported column requirement | source-traceability | `NO_ACTION` | Already covered by [#306](https://github.com/ShadyUnderLight/deep-research-skill/issues/306) via validator chain |
| 6 | Body-level `[Sxx]` citation requirement for constrained-choice reports | source-traceability | `NO_ACTION` | Already covered by [#306](https://github.com/ShadyUnderLight/deep-research-skill/issues/306) via validator chain |

**Summary: All 6 candidate actions are `NO_ACTION` (all gaps closed by #306, #308, #309).**

---

## Triage notes

### Why all candidates are NO_ACTION

Each gap identified in the original paired-report comparison has been systematically addressed by issues [#306](https://github.com/ShadyUnderLight/deep-research-skill/issues/306), [#308](https://github.com/ShadyUnderLight/deep-research-skill/issues/308), and [#309](https://github.com/ShadyUnderLight/deep-research-skill/issues/309). This distillation exists to:

1. **Document that the loop is closed** — all known gaps from this paired comparison are now covered by rules, checklists, templates, or validator gates
2. **Provide a regression baseline** — if a future career/skill-selection constrained-choice report passes through the pipeline and still exhibits any of these gaps, that is a regression
3. **Distinguish rule gaps from execution gaps** — most gaps were execution/wiring gaps (rules existed but constrained-choice route wasn't wired to audit_report for career/skill-selection sub-type), not missing rules

### Career/skill-selection as a distinct constrained-choice subclass

This case identifies **career/skill-selection reports** as a distinct subclass within the constrained-choice route, with specific failure modes not fully covered by the general constrained-choice rules:

| Failure mode | What the general rules missed | How fixed |
|---|---|---|
| Proxy indicator conflation | General constrained-choice rules assume direct-comparable metrics | [#308](https://github.com/ShadyUnderLight/deep-research-skill/issues/308) added career/skill-selection sub-gate with proxy indicator table |
| US-vs-global scope confusion | General rules don't flag geographic scope for salary/job data | [#308](https://github.com/ShadyUnderLight/deep-research-skill/issues/308): explicit scope requirements |
| Learning time estimate basis | No rule existed for estimate basis notes | [#308](https://github.com/ShadyUnderLight/deep-research-skill/issues/308): learning time basis requirement |
| Shortlist boundary leak | General rules assume shortlist is self-evident | [#309](https://github.com/ShadyUnderLight/deep-research-skill/issues/309): Decision Scope with exclusions |

### Relative to TSMC and World Cup comparative distillations

The TSMC case addressed listed-company route gaps (DCF, capital return, customer concentration). The World Cup case addressed constrained-choice probability-distribution gaps (probability method, scoring replicability). This case addresses **career/skill-selection constrained-choice** gaps (proxy discipline, scope declaration, learning time labeling, shortlist boundary).

All three share a common structural weakness: **route-specific validators were not wired into audit_report's total control, causing existing quality gates to silently not fire for certain sub-types.** TSMC triggered listed-company wiring (#276); World Cup triggered constrained-choice wiring (#306); this case triggered career/skill-selection sub-type wiring within constrained-choice (#308 + #306).

---

## Things explicitly rejected

| Observation | Why rejected |
|---|---|
| GPT 版的 `turn...` citation 格式可以采纳 | 格式在 GPT 会话外不可复核，违反仓库 Source Register 纪律 |
| 本地版应被废弃 | 本地版的 constrained-choice 结构（route/audit status、persona breakdown、reversal conditions）依然有价值，只是 proxy discipline 和 scope 纪律有缺口 |
| TIOBE/薪资/GitHub stars 在同一表格中混合不需要标注角色 | 这是 career/skill-selection 报告的核心失败模式。三种指标测量完全不同的东西，不标角色就是 false comparability |
| 学习时间估算不需要 basis note "因为是常识" | Python "6个月" 和 Rust "18个月" 这样的对比如果无 basis，读者无法判断这是个人估计、项目报告数据、还是平均值。需要 basis+方差 |
| 本地版引入 TypeScript/Go 不需要说明排除理由 | 如果 TypeScript/Go 是有效选项就应该在 shortlist 中，如果不是就应该说明排除理由。不说明就是 shortlist discipline 失败 |
| 这个 comparative-distillation 应放在 `evals/cases/` 下 | 符合 `evals/README.md` 定义的命名约定 `*-comparative-distillation.md`，放在 `evals/comparative-distillation/` 下 |

### Turn... citation format — explicitly rejected

GPT 版使用形如 `turn...` 的 citation artifact 提供正文引用来源。该格式在 GPT 深度研究界面内可点击回溯，但在仓库中 **不可复核、不可检查、不可持久化**。

- 该格式提供的信息（来源、置信度、上下文）在复制到本地后全部丢失
- 该格式不能映射到仓库的 7 列 Source Register 体系
- 该格式不允许 reviewer 独立验证来源

**结论：** `turn...` 格式是 GPT 的专有输出 artifact，不在本仓库采纳范围内。GPT 版在 claim-level attribution density 上的优势（每个关键论断都有来源标注）是值得学习的写作文本习惯，但具体 format 不可采用。

---

## Final judgment

### What the stronger report did better
- GPT 版在 **市场范围声明、代理指标角色标注、关键词偏差说明、学习时间估算 basis** 方面更强
- GPT 版更有效地防止读者将不可比指标（TIOBE、薪资、GitHub stars）视为同一类数据
- GPT 版的按经验水平分段推荐模式（zero-base / 1-3yr / 3-5yr / 5+yr）更精细，每个推荐附带 why + trade-off

**Local report's structural strengths**（非规则 gap，但值得记录）：
- Route/audit/status 结构 — GPT 完全缺失仓库要求的 route metadata
- Persona breakdown + reversal conditions — 按用户画像分推荐+反转条件是本地版的核心结构优势
- Counter-evidence section — 更诚实地展示了反对意见

### What should change in the repo now
- ✅ 全部已通过 [#306](https://github.com/ShadyUnderLight/deep-research-skill/issues/306)、[#308](https://github.com/ShadyUnderLight/deep-research-skill/issues/308)、[#309](https://github.com/ShadyUnderLight/deep-research-skill/issues/309) 落地
- 所有 6 个维度均已覆盖规则、checklist 或 validator 链
- 本文件作为 regression 基线

### What should wait for another confirming case
- Career/skill-selection 报告中的 **composite scoring transparency** — 当前 proxy discipline 规则要求标注每个 proxy 的角色和约束，但对 composite score（如 A+/B+ tier 评分）的输入权重透明度尚未作为硬性 blocking gate。如果 future report 再次出现权重隐藏问题，应考虑升级到 blocking 级别。

### Is this mainly a missing rule, missing trigger, or execution problem?
- **Proxy indicator conflation (unlabeled roles, mixed table)**: Missing rule → 已由 [#308](https://github.com/ShadyUnderLight/deep-research-skill/issues/308) 修复（新增 career/skill-selection proxy evidence discipline checklist sub-gate）
- **Self-assessment overclaim (claimed ✅ while gaps existed)**: Execution problem（constrained-choice route 未接入 audit_report process-integrity gate）→ 已由 [#306](https://github.com/ShadyUnderLight/deep-research-skill/issues/306) 修复
- **Missing scope declaration (US data as global, no market scope upfront)**: Missing template → 已由 [#309](https://github.com/ShadyUnderLight/deep-research-skill/issues/309) 修复（Decision Scope block）
- **Shortlist boundary leak (TypeScript/Go without exclusion rationale)**: Missing template → 已由 [#309](https://github.com/ShadyUnderLight/deep-research-skill/issues/309) 修复（Decision Scope 含 exclusion 原因）

**混合类型：** 该对比暴露了规则缺口（proxy discipline）、执行缺口（route wiring）和模板缺口（scope block, shortlist boundary）。均已按场景修复。

---

## Minimal quality bar

- [x] the two reports are comparable enough to justify distillation (same question, similar timeframe, same route subclass)
- [x] the comparison used the six fixed dimensions
- [x] each accepted candidate has an action type
- [x] each accepted candidate has a proposed repo home
- [x] turn... citations explicitly documented as rejected (see "Things explicitly rejected" section)
- [x] the final judgment distinguishes rule gap vs trigger gap vs execution gap (mixed: rules, execution, and template gaps all present)
