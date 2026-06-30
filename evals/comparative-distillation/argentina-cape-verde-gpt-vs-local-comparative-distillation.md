# Argentina vs Cape Verde GPT-vs-Local Comparative Distillation

> **目的：** 将 GPT 深度研究版与本地 deep-research-skill 版对 Argentina vs Cape Verde World Cup 淘汰赛 upset path 分析报告的 paired-report 对比固化为回归资产，防止 future constrained-choice 体育 upset 分析报告重复出现 Shared-workflow 逃逸、Wikipedia 虚假可靠性标注、零决策架构等复合失败模式。

---

## Case identity

- **Case name:** Argentina-vs-Cape-Verde constrained-choice GPT-vs-local comparative distillation
- **Date:** 2026-06-29
- **Research question:** Analyze the upset potential for Cape Verde against Argentina in the World Cup knockout stage. What are the realistic upset paths, what probabilities attach to each, and what conditions must be met?
- **Why this comparison matters:**
  - 两份报告回答相同问题，但 GPT 版展示了 strong current-state discipline（market-implied probability 基线、统计对比表、事件场景模拟）和清晰的数据限制声明；本地版则出现了 Shared-workflow 逃逸、零决策架构、100% Wikipedia 虚假可靠性标注、概率发布时承认缺失关键输入等复合失败
  - 该对比是 #306、#307、#309、#341 多项改进的触发之一
  - 本地版暴露了 constrained-choice route 在体育 upset 分析场景中的系统性薄弱环节：route 逃逸（Shared-workflow 作为 catch-all）、source 虚假标注（Wikipedia = high reliability）、决策架构完全缺失
- **Report A:** GPT 深度研究版（Argentina vs Cape Verde upset path 分析）
- **Report B:** 本地 deep-research-skill 版（Argentina vs Cape Verde upset path 分析 memo）
- **Reference / stronger report (if any):** GPT 深度研究版（current-state 纪律更强、统计对比表、事件场景模拟、数据限制文档化更清晰）
- **Prompt(s):** 相同研究问题，两份报告均使用 deep-research style
- **Important scope or timing differences:**
  - 两份报告均基于同一赛前窗口，时间窗口基本一致
  - GPT 版生成于 GPT 深度研究界面，本地版生成于 deep-research-skill pipeline
  - 对比焦点在 route 选择纪律、决策架构完整性、source traceability 与可靠性标注、概率方法透明度等结构性差异

---

## Comparison purpose

This comparison is **not** for deciding which model is "better."

It is for:

1. 识别 constrained-choice route 中体育 upset 分析场景有哪些规则 gap 已被 #306、#307、#309、#341 覆盖
2. 确认哪些 gap 仍有残余风险，特别是 Shared-workflow 逃逸和虚假可靠性标注两个新子模式
3. 将 paired-report 基线固化为将来 regression 资产
4. 记录哪些改进来自"新规则"，哪些来自"执行链触发"

**Because all identified gaps have already been addressed by closed issues, this file serves primarily as a regression audit asset rather than a gap-discovery artifact.**

---

## Dimension 1: Current-state discipline (pre-match snapshot, odds/lineups/weather/injuries verification)

### Report A (GPT)
- Better current-state discipline: odds/market-implied probability used as baseline for all upset path probabilities
- Statistical comparison tables (goals, conceded, possession, shots, xG, set-piece threat) providing factual grounding
- Event scenario simulation (early red card, set-piece goal, weather/fitness, penalties) with explicit condition-to-probability mapping
- Clear signal for decision-making: which early events change upset probability and by how much
- Data limitations and assumptions explicitly documented (sources, reliability boundaries, what is unknown)

### Report B (Local)
- Admitted missing odds, injuries, training status, and weather — **core pre-match prediction inputs, not optional enrichments**
- Published numerical probability judgments (`10-15%`, `25-30%`, `80-85%`) despite admitting these gaps
- No market-implied baseline or odds calibration step
- No team comparison tables (goals, xG, set-piece metrics)
- Wikipedia-only sourcing provided no independent verification of current-state claims

### Gap
- **Critical**: 本地版发布概率时承认缺失赔率/伤病/天气，但在 constrained-choice 概率预测中，这些是 minimum viable input 而非可选丰富化
- GPT 版以市场隐含概率为基线，展示统计对比，本地版完全没有这一层
- 这是 pre-match 预测特有的 current-state 纪律——不是通用信息缺口

### Current status
✅ 已由 #309 修复：
- `references/decision-report-template.md` 新增 Decision Scope 块，强制 pre-match snapshot 包含确认/未确认输入
- 体育预测子类型明确要求赛前快照在前 1 屏内出现，包含赔率/伤病/天气等输入状态
- `checklists/option-selection-final-audit.md` 新增 first-screen clarity 检查

### Eval regression assets
- `evals/cases/argentina-cape-verde-constrained-choice-route-and-source-fail-case.md` — 覆盖 pre-match current-state 缺口

### Action type
`NO_ACTION` — 规则已覆盖，有专用 eval case

---

## Dimension 2: Numerical and date discipline (probability method transparency, numeric role labels)

### Report A (GPT)
- Probability distribution grounded in market-implied odds as baseline → adjusted for upset scenarios
- Statistical comparison table data (goals, xG, shots, possession) with observable match statistics
- Event scenario simulation assigns explicit delta-probability to each scenario
- Numbers carry implied roles (observed stats, market-implied prior, modeled scenario deltas)
- Data limitations section documents what inputs are solid vs estimated

### Report B (Local)
- Core probabilities (`10-15%`, `25-30%`, `80-85%`) presented as conclusions with **zero replicable method**
- Score distributions (`2-0`, `1-0`, `3-0`, `1-1`, `2-1`) similarly without role labels, method reference, or worked example
- **No numeric role labels**: observed/proxy/assumption/model-output entirely absent
- No estimation method disclosed (Poisson? logit? odds calibration? expert judgment?)
- No worked example showing how a stated probability was computed from evidence

### Gap
- **Probability is the core output of this report type** — publishing it without method or role labels is a hard-fail in constrained-choice
- 本地版对比 GPT 版在数值纪律层面的差距比 Argentina vs Algeria 案例更大：该案例连变量到概率的映射架构都没有
- 无模型路径、无基线校准、无复现路径

### Current status
✅ 已由 #307 修复：
- 新增 scoring-replicability validator（`scripts/validate_scoring_replicability.py`）
- 触发条件：胜率/概率分布、加权评分
- 强制要求：维度定义、权重、分数/概率转换规则、至少 1 个 worked example

### Eval regression assets
- `evals/cases/argentina-cape-verde-constrained-choice-route-and-source-fail-case.md` — 覆盖概率方法缺失
- `evals/cases/world-cup-prediction-constrained-choice-probability-method-case.md` — 同体育场景

### Action type
`NO_ACTION` — 规则已覆盖，validator 已接入

---

## Dimension 3: Source traceability and evidence weighting (body citations, Source Register, reliability labels)

### Report A (GPT)
- Body has claim-level citation density though `turn...` format not replicable outside session
- Data limitations explicitly documented with reliability boundaries
- Stronger source diversity (statistics databases, market odds aggregators)
- No 7-column Source Register (format mismatch — not in repo standard)

### Report B (Local)
- **Zero `[Sxx]` inline citations in body** — source-traceability hard-fail
- Source Register is **6-column (missing Claims Supported)** — hard-fail against 7-column requirement
- **100% of sources are Wikipedia** — source-strength gate fail
- **All Wikipedia sources falsely labeled "high reliability"** — actively misrepresenting tertiary crowdsourced sources as authoritative for load-bearing match analysis claims
- Admitted missing odds, injuries, weather but no attempt to source them

### Gap
- 本地版同时触发三项失败：traceability hard-fail（零正文引用）、source-strength gate fail（100% Wikipedia）、false reliability labeling（Wikipedia = high reliability）
- 最后一项（虚假可靠性标注）是此前 eval cases 未覆盖的新子模式：不仅是 source 质量低，而且是 active misrepresentation
- 相比 Argentina vs Algeria 案例，此案例的 source 问题更严重——Argentina vs Algeria 至少 Wikipedia 标注正确（tertiary/crowdsourced），此版本标注错误

### Current status
✅ 已由 #306 和 #341 联合修复：
- #306：constrained-choice route 接入 audit_report 总控，触发 source traceability validator 链；未知 route 不再静默回落到 technical-deep-dive
- #341：source-strength gate 强制 Wikipedia 等聚合源按实际可靠性层级标注（tertiary/crowdsourced），禁止标注为 "high reliability"

### Eval regression assets
- `evals/cases/argentina-cape-verde-constrained-choice-route-and-source-fail-case.md` — 覆盖 100% Wikipedia + false reliability labeling
- `evals/cases/world-cup-constrained-choice-wrong-route-case.md` — 同 route 逃逸模式

### Action type
`NO_ACTION` — 规则已覆盖，validator 链已接入，有专用 eval case

---

## Dimension 4: Forward-looking claim discipline (probability as forecast, scenario logic, uncertainty communication)

### Report A (GPT)
- Probability presented as conditional on current-state assumptions: "if X, then upset probability is Y"
- Event scenario simulation shows how key events (early red card, set-piece goal, weather, penalties) shift upset probability
- Clear signal for decision-making: which early events change upset probability and by how much
- Data limitations and assumptions explicitly documented — reader knows what is solid vs uncertain

### Report B (Local)
- Listed upset paths (set-piece goal, defensive collapse, extra time/penalties, weather, early red card) — structurally similar to GPT
- Assigned probabilities to each path (`10-15%` for set-piece, `25-30%` extra time, etc.)
- No condition-to-probability mapping — probabilities appear as flat estimates
- No sensitivity or scenario simulation
- No uncertainty bands or confidence intervals
- No explicit distinction between core-conviction vs speculative claims

### Gap
- 本地版的 upset path 识别在结构层面与 GPT 版类似，但 forward-looking discipline 弱：
  - 概率以单点范围呈现而无条件标记
  - 没有"如果 X 发生，概率变为 Y"的事件模拟
  - 读者无法判断这些概率在什么条件下成立、什么时候需要更新
- GPT 版的事件场景模拟提供了更具可操作性的决策信号

### Current status
✅ 已由 #307 和 #309 共同覆盖：
- #307：scoring-replicability validator 强制要求概率从 evidence 到 conclusion 的映射，包括权重和至少 1 个 worked example
- #309：Decision Scope 块强制列出改变结论的条件

### Eval regression assets
- `evals/cases/argentina-cape-verde-constrained-choice-route-and-source-fail-case.md` — 覆盖 forward-looking claim 要求

### Action type
`NO_ACTION` — 规则已覆盖

---

## Dimension 5: Structural readability and information density (decision architecture, opening flow)

### Report A (GPT)
- 开头给出条件化结论和 probability baseline
- 方法论路径在正文中清晰分段
- Statistical comparison table 在正文前中部位置，提供 factual grounding
- Event scenario simulation 在结论附近集中展示
- 无 route/audit status 模块（不符合仓库格式要求，但也避免了 metadata-first 漂移）

### Report B (Local)
- **Zero decision architecture** — 没有 Decision Scope、option universe、shortlist construction logic、comparison unit 或 aggregation logic。概率和分析路径呈现为 unstructured expert commentary 而非 structured choice task
- 自述 Shared-workflow（catch-all route），回避了 constrained-choice 应有的结构
- Opening flow 没有 judgment-first — 核心 upset path 分析和概率被埋在中后部

### Gap
- **零决策架构是此案例相比 Argentina vs Algeria 案例的独特严重缺口** — Argentina vs Algeria 案例有 partial architecture（outcome shortlist、variable definition、reversal conditions），此版本完全没有
- Shared-workflow route 逃逸使得 template 中的 Decision Scope、option universe 等块全部不触发

### Current status
✅ 已由 #309 修复：
- `references/decision-report-template.md` 新增 Decision Scope 块，强制 judgment + decision scope 在 route metadata 之前
- 明确要求 constrained-choice 报告必须包含 option universe、shortlist logic、comparison unit
- `checklists/option-selection-final-audit.md` 新增第一屏清晰度检查

### Eval regression assets
- `evals/cases/argentina-cape-verde-constrained-choice-route-and-source-fail-case.md` — 覆盖零决策架构

### Action type
`NO_ACTION` — 规则已覆盖

---

## Dimension 6: Decision usefulness (would the report help someone decide?)

### Report A (GPT)
- Clear signal for decision-making: which early events change upset probability and by how much
- Reader can answer: "what needs to go right for Cape Verde, and how likely is each scenario?"
- Conditional probability structure helps reader know when to update beliefs
- Data limitations documented so reader knows confidence boundaries

### Report B (Local)
- Upset path identification is structurally useful: set-piece, defensive collapse, extra time, weather, early red card
- Probability ranges (`10-15%` etc.) give reader a rough sense of relative likelihood
- But **no replicable method** → reader cannot recompute if they disagree with assumptions
- **No condition-to-probability mapping** → reader cannot tell when probabilities should change
- **Gapped current-state** → reader doesn't know if published probabilities account for latest injuries/weather/odds
- **Untraceable claims** → reader cannot verify any factual assertion
- **Misrepresented source quality** → reader is actively misled about evidence reliability

### Gap
- 本地版的决策有用性被复合失败严重限制：traceability 缺失、概率方法不透明、current-state 缺口、source 虚假标注，四个问题叠加使报告几乎不可用

### Current status
✅ 已由 #306、#307、#309、#341 联合覆盖：
- #306：保证 constrained-choice 路由的所有 validator 稳定触发
- #307：要求概率必须有从 evidence 到结论的可复算通道
- #309：要求 decision scope 明确改变结论的条件
- #341：source-strength gate 禁止虚假可靠性标注

### Action type
`NO_ACTION` — 规则已覆盖

---

## Candidate-action summary

| # | Candidate action | Failure family | Action type | Proposed home |
|---|---|---|---|---|
| 1 | Constrained-choice audit_report 总控接入（Shared-workflow 逃逸检测） | route-wiring / process-integrity | `NO_ACTION` | Already closed by #306 |
| 2 | Scoring-replicability validator for constrained-choice | probability-method / numerical-discipline | `NO_ACTION` | Already closed by #307 |
| 3 | Decision Scope block with forced option universe + shortlist | decision-architecture / opening-flow | `NO_ACTION` | Already closed by #309 |
| 4 | Source-strength gate with false-reliability-labeling guard | source-traceability / evidence-weighting | `NO_ACTION` | Already closed by #341 |
| 5 | Pre-match current-state verification requirement | current-state / domain-discipline | `NO_ACTION` | Already closed by #309 |
| 6 | Self-assessment accuracy gate for constrained-choice | process-integrity | `NO_ACTION` | Already closed by #306 |

**Summary: All 6 candidate actions are `NO_ACTION` (all gaps closed by #306, #307, #309, #341).**

---

## Triage notes

### Why all candidates are NO_ACTION

Each gap identified in this paired-report comparison has been systematically addressed by issues #306, #307, #309, and #341. This distillation exists to:

1. **Document that the loop is closed** — all known gaps from this paired comparison are now covered by rules, checklists, templates, or validator gates
2. **Provide a regression baseline** — if a future constrained-choice sport upset analysis report still exhibits Shared-workflow escape hatch, zero decision architecture, 100% Wikipedia falsely labeled high reliability, or odds/injuries/weather gapped while publishing probabilities, that is a regression
3. **Distinguish rule gaps from execution gaps** — most gaps were missing rules (false reliability labeling, zero decision architecture) or execution/wiring gaps (Shared-workflow catch-all, constrained-choice route not wired to audit_report)

### Action type distribution in this artifact

All six dimensions evaluate to `NO_ACTION` because every identified gap has been addressed by issues #306, #307, #309, and #341. No `NEW_RULE`, `CHECKLIST_HARDENING`, `TEMPLATE_CHANGE`, or `VALIDATOR_OR_TEST` candidates emerged from this paired comparison — the gap-closure work was comprehensive in Phase A/B.

### Unique contributions vs. existing Argentina-vs-Algeria comparative distillation

| Dimension | Argentina vs Algeria (existing) | Argentina vs Cape Verde (this file) |
|---|---|---|
| Route misidentification | market-outlook (wrong specific route) | Shared-workflow (catch-all escape) |
| Decision architecture | Partial: outcome shortlist + variable definitions | **Zero**: no universe, shortlist, comparison unit, aggregation |
| Source diversity | Mixed (Wikipedia + others) | **100% Wikipedia** |
| Reliability labeling | Correct (tertiary/aggregator) | **False**: Wikipedia = "high reliability" |
| Current-state gap | Partial | **Critical**: odds/injuries/weather admitted missing while publishing probabilities |
| Closed issues | #306, #307, #309 | #306, #307, #309, #341 |

---

## Things explicitly rejected

| Observation | Why rejected |
|---|---|
| GPT 版应被作为"体育 upset 分析标准输出格式" | GPT 版使用 `turn...` citation 格式，不满足仓库 Source Register 纪律和 route/audit status 要求 |
| 本地版应被废弃 | 本地版的 upset path 识别有结构价值，只是执行纪律有缺口；该案例促成了 Shared-workflow 逃逸检测和虚假可靠性标注的规则落地 |
| Shared-workflow 逃逸只在体育场景出现 | 已有 eval case 覆盖 regulatory 场景的 Shared-workflow 逃逸；这是 route-level 问题而非 domain-level 问题 |
| 虚假可靠性标注可以视为"标注者诚实错误" | Wikipedia 标注为 "high reliability" 不是诚实错误的范畴——Wikipedia 是已知 tertiary/crowdsourced 源，在 deep-research 上下文中有明确标注规则 |
| 零决策架构是"篇幅限制所致" | 对于 constrained-choice 报告，决策架构不是可选的丰富化内容，而是 route contract 的 core obligation |

---

## Final judgment

### What the stronger report did better
- GPT 版以 market-implied odds 为概率基线，grounding 在可观察市场信号上而非直觉判断
- GPT 版统计对比表（goals, xG, shots, possession, set-piece threat）提供 factual grounding
- GPT 版事件场景模拟（early red card, set-piece, weather, penalties）显示条件变化对概率的 delta 影响
- GPT 版的数据限制文档化使报告可被持续使用（知道什么信息变化需要更新判断）

### What should change in the repo now
- ✅ 全部已通过 #306、#307、#309、#341 落地
- 所有 6 个维度均已覆盖规则或 validator 链
- 本文件作为 Argentina-vs-Cape-Verde 配对报告回归基线

### What should wait for another confirming case
- **Shared-workflow 逃逸检测的 recall** — 当前 route auto-detection 在 `audit_report.py` 中实现，但只有一个 eval case（此案例）的触发记录。如果 future 报告中再次出现 constrained-choice 任务被错误识别为 Shared-workflow，应考虑在 route-selection checklist 中加入显式排除项
- **体育 upset 分析的事件场景模拟要求** — GPT 版的事件模拟提供了更高的决策有用性，但当前规则集不强制要求。如果 future 体育预测报告再次缺少场景模拟，应考虑升级该要求到 checklist 级别

### Is this mainly a missing rule, missing trigger, or execution problem?
- **Shared-workflow escape hatch (route misidentification)**: Mixed — route auto-detection was missing (rule gap), and constrained-choice route wasn't wired to audit_report (execution gap) → both fixed by #306
- **Zero decision architecture**: Missing rule → fixed by #309
- **Probability method opacity / numeric roles**: Missing rule → fixed by #307
- **100% Wikipedia + false reliability labeling**: Missing rule → fixed by #341
- **Current-state gap for pre-match prediction**: Missing rule → fixed by #309
- **Self-assessment overclaim**: Execution problem → fixed by #306

---

## Minimal quality bar

- [x] the two reports are comparable enough to justify distillation
- [x] the comparison used the six fixed dimensions
- [x] each accepted candidate has an action type
- [x] each accepted candidate has a proposed repo home
- [x] at least one rejected observation is documented when relevant
- [x] the final judgment distinguishes rule gap vs trigger gap vs execution gap
