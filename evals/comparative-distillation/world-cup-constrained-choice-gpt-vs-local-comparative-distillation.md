# World Cup Constrained-Choice GPT vs Local Comparative Distillation

> **目的：** 将 GPT 深度研究版与本地 deep-research-skill 版对 World Cup 预测（constrained-choice / probability distribution）的 paired-report 对比固化为回归资产，防止 future constrained-choice probability reports 重复出现同样的复合失败。

---

## Case identity

- **Case name:** World Cup constrained-choice GPT-vs-local comparative distillation
- **Date:** 2026-06-16
- **Research question:** Predict outcome of Argentina vs Algeria World Cup match (constrained-choice / probability distribution)
- **Why this comparison matters:**
  - 两份报告回答同一问题，但概率方法透明度、数字角色纪律、source traceability 和 metadata 布局差异显著。
  - 该对比是 [#306](https://github.com/ShadyUnderLight/deep-research-skill/issues/306)、[#307](https://github.com/ShadyUnderLight/deep-research-skill/issues/307)、[#309](https://github.com/ShadyUnderLight/deep-research-skill/issues/309) 所有改进的原始动机来源之一。
  - 本地版暴露了 constrained-choice route 概率分布类报告的系统性薄弱环节，跨越 probability method opacity、numeric role labeling、body-level traceability 和 self-assessment accuracy。
- **Report A:** GPT 深度研究版（World Cup 预测报告）
- **Report B:** 本地 deep-research-skill 版（Argentina vs Algeria 预测 memo）
- **Reference / stronger report (if any):** GPT 深度研究版（概率模型路径更强，current-state 纪律更好，但 citation 格式不适用于仓库）
- **Prompt(s):** 相同研究问题，两份报告均使用 deep-research style
- **Important scope or timing differences:**
  - 两份报告均基于同一赛前窗口，时间窗口基本一致
  - GPT 版生成于 GPT 深度研究界面，本地版生成于 deep-research-skill pipeline
  - 对比焦点在概率方法透明度、数字角色、traceability 等结构性差异，而非事实检索能力

---

## Comparison purpose

This comparison is **not** for deciding which model is "better."

It is for:

1. 识别 constrained-choice route 中概率分布类报告有哪些规则 gap 已被 [#306](https://github.com/ShadyUnderLight/deep-research-skill/issues/306)、[#307](https://github.com/ShadyUnderLight/deep-research-skill/issues/307)、[#309](https://github.com/ShadyUnderLight/deep-research-skill/issues/309) 覆盖
2. 确认哪些 gap 仍有残余风险
3. 将 paired-report 基线固化为将来 regression 资产
4. 记录哪些改进来自"新规则"，哪些来自"执行链触发"

**Because all identified gaps have already been addressed by closed issues, this file serves primarily as a regression audit asset rather than a gap-discovery artifact.**

---

## Dimension 1: Current-state discipline (pre-match snapshot timing, squad/referee/weather unknowns)

### Report A (GPT)
- 显式记录 pre-match snapshot：比赛时间、地点、天气
- 明确列出模型路径（logit sanity check → Poisson → Monte Carlo）
- 区分高置信度核心结果（core results）与低置信度事件级假设（event-level assumptions）
- 说明 pre-match 信息变化（如首发缺核心、赔率移动）会如何调整概率
- 弱点：使用 `turn...` citation 格式，离开会话不可复核

### Report B (Local)
- 正确定义了 outcome shortlist（win / draw / loss）和为什么穷尽
- 定义了 5 个 load-bearing variables（球队实力、近期状态、历史交锋、情境因素等）
- 列出了 reversal conditions 和 pre-match 监控信号
- 包含 counter-evidence 部分（历史冷门、情境风险）
- 弱点：概率分布（60/25/15）以不透明方法呈现，pre-match snapshot 不如 GPT 完整（缺少天气、裁判确认状态等）

### Gap
- 本地版在 pre-match 快照完整性上有 gap：GPT 版更精确地标注了哪些信息（首发、裁判、更新赔率）**尚未确认**
- 本地版的结构变量强，但 current-state 纪律不如 GPT 版显式

### Current status
✅ 已由 [#309](https://github.com/ShadyUnderLight/deep-research-skill/issues/309) 修复：
- `references/decision-report-template.md` 新增 Decision Scope 块，强制前置 outcome shortlist + pre-match snapshot
- 体育比赛预测子类型明确要求 outcome shortlist 与赛前快照在前 1 屏内出现
- `checklists/option-selection-final-audit.md` 新增 first-screen clarity 检查

### Eval regression assets
- `evals/cases/world-cup-prediction-constrained-choice-probability-method-case.md` — 综合 eval 覆盖 current-state snapshot 要求

### Action type
`NO_ACTION` — 规则已覆盖，有专用 eval case

---

## Dimension 2: Numerical and date discipline (probability method transparency, numeric role labels)

### Report A (GPT)
- 显式的方法论路径：logit sanity check 作为基准，转移到 Poisson 模型（含 xG/xA 分解），用 Monte Carlo 模拟 10,000 次
- 敏感性测试：关键输入变化后概率如何移动
- 数字角色隐含可识别（模型输出、假设、观察值），但未按仓库标准标注 observed/proxy/assumption/model-output

### Report B (Local)
- **概率分布（60/25/15）呈现为结论，无复现方法** — 未展示 evidence（球队评分、变量权重、组合规则）如何映射为概率
- **数字角色标签缺失** — odds、probabilities、percentage impacts 缺乏 observed/proxy/assumption/model-output 角色
- 5 个 load-bearing variables 的定义有结构价值，但与最终概率没有连接通道

### Gap
- 核心差距：**概率是 constrained-choice 的排名输出，没有可复现方法就是 false precision**
- 数字角色缺失触发 constrained-choice hard-fail
- GPT 版虽然有模型路径，但格式/角色纪律不满足仓库要求

### Current status
✅ 已由 [#307](https://github.com/ShadyUnderLight/deep-research-skill/issues/307) 修复：
- 新增 scoring-replicability validator（`scripts/validate_scoring_replicability.py`）
- 触发条件：总分、星级、A+/B+ 等级评分表、胜率/概率分布、加权评分
- 强制要求：维度定义、权重、分数/概率转换规则、至少 1 个 worked example、close-score caveat
- 已注册到 `scripts/audit_report.py` 的 constrained-choice route validator
- 世界杯 eval case 直接引用该 validator

### Eval regression assets
- `evals/cases/world-cup-prediction-constrained-choice-probability-method-case.md` — 核心 eval case
- `evals/cases/content-platform-constrained-choice-compounded-fail-case.md` — 同 route 复合失败

### Action type
`NO_ACTION` — 规则已覆盖，validator 已接入

---

## Dimension 3: Source traceability and evidence weighting (body-level citation, source register, self-assessment accuracy)

### Report A (GPT)
- 正文有 claim-level 引用密度但格式为 `turn...` 不可复核
- 无 7 列 Source Register
- 无 route/audit status 模块（不符合仓库格式要求）

### Report B (Local)
- 正文缺 `[Sxx]` claim-level 引用 — 只有章节级来源归属，不足以追溯单条结论
- Source Register 有注册源（S10/S11）但正文未引用
- aggregator 源（Wikipedia、Transfermarkt）标注为 `[确认事实]` 而非带众包风险说明
- **自评声明所有 ✅ 已通过，但概率方法、数字角色、正文 traceability 存在实际缺口** — process-integrity hard-fail

### Gap
- 本地版核心问题：**规则存在但执行链未触发**。Traceability 和 process-integrity 纪律已有文档，但 constrained-choice route 未接入 audit_report 总控，导致 validator 链未强制执行。
- GPT 版核心问题：**格式不符合仓库标准**，引用离源不可复核。

### Current status
✅ 已由 [#306](https://github.com/ShadyUnderLight/deep-research-skill/issues/306) 修复：
- `scripts/audit_report.py` 新增 constrained-choice / option-selection / shortlist route mapping
- Route auto-detection 扩展支持中文/混合格式路由声明
- Constrained-choice route 激活 source traceability、declared-execution、table role labels、source label consistency 等现有 validator
- 未知 route 不再静默回落到 technical-deep-dive
- Process-integrity gate 在交付前强制检查自评与执行的一致性

### Eval regression assets
- `evals/cases/world-cup-prediction-constrained-choice-probability-method-case.md` — 综合 eval 覆盖
- `evals/cases/content-platform-constrained-choice-compounded-fail-case.md` — 同 route 复合失败基准
- `evals/cases/indie-dev-constrained-choice-delivery-fail-case.md` — 同 route delivery fail 基准

### Action type
`NO_ACTION` — 规则已覆盖，validator 链已接入，有专用 eval case

---

## Dimension 4: Forward-looking claim discipline (probability as forecast, scenario logic)

### Report A (GPT)
- 显式区分高置信度核心结果与低置信度事件级假设
- 说明 pre-match 信息变化（首发、赔率移动、天气恶化）如何调整概率
- 敏感性测试展示了在关键输入变化时概率移动范围
- 概率呈现为"在当前已知条件下的条件预测"，未过度承诺

### Report B (Local)
- 列出 reversal conditions 和 pre-match 监控信号
- 包含 counter-evidence 部分（历史冷门、情境风险）
- 概率分布（60/25/15）以单点估计呈现，无置信区间或敏感性
- 未明确区分"核心确信"与"推测性较强"的部分

### Gap
- 本地版 forward-looking discipline 在结构层面有（reversal conditions、counter-evidence），但在概率表达上过于单点化
- 60/25/15 没有告诉用户在什么置信度下预测，也没有展示在关键变量变化后概率如何移动
- GPT 版对不确定性沟通更显式和诚实

### Current status
✅ 已由 [#307](https://github.com/ShadyUnderLight/deep-research-skill/issues/307) 和 [#309](https://github.com/ShadyUnderLight/deep-research-skill/issues/309) 共同覆盖：
- [#307](https://github.com/ShadyUnderLight/deep-research-skill/issues/307)：scoring-replicability validator 强制要求概率必须有从 evidence 到 probability 的映射，包括权重、转换规则、至少 1 个 worked example
- [#309](https://github.com/ShadyUnderLight/deep-research-skill/issues/309)：Decision Scope 块强制列出改变结论的条件，对应 GPT 版的 "how pre-match info changes adjust probabilities"

### Eval regression assets
- `evals/cases/world-cup-prediction-constrained-choice-probability-method-case.md` — 约束 forward-looking claim discipline

### Action type
`NO_ACTION` — 规则已覆盖

---

## Dimension 5: Structural readability and information density (front-page judgment vs metadata, opening flow)

### Report A (GPT)
- 开头先给条件化结论：在特定条件下（首发完整、市场预期）概率分布是多少
- 方法论路径在正文开头或早分段给出
- 无 route/audit status 模块（不符合仓库要求，但也避免了 metadata-first 漂移）

### Report B (Local)
- **metadata-first drift on front page** — evidence grading 图例和 audit status 出现在核心结论之前
- Outcome shortlist 和 pre-match snapshot 不在第一屏
- 自评审计区块的位置更像是"给 reviewer 看"而非"给决策者看"

### Gap
- 本地版的结构受 template 驱动但 template 未规定 judgment-first 布局
- 决策支持报告的开头应该优先回答"结论是什么"，而非"审计状态是什么"

### Current status
✅ 已由 [#309](https://github.com/ShadyUnderLight/deep-research-skill/issues/309) 修复：
- `references/decision-report-template.md` 新增 Decision Scope 块，强制 judgment + decision scope 在 route metadata 之前
- `checklists/option-selection-final-audit.md` 新增 first-screen clarity 检查：selection reports 的第一屏必须优先展示 judgment + decision scope，而不是 route metadata
- 对体育预测子类型给出明确例子：outcome shortlist 和赛前快照必须在前 1 屏内
- `checklists/final-audit.md` 增加 recall：constrained-choice 报告 opening 应先呈现结论范围

### Eval regression assets
- `evals/cases/world-cup-prediction-constrained-choice-probability-method-case.md` — 约束 judgment-first 布局
- `evals/cases/indie-dev-constrained-choice-delivery-fail-case.md` — 同类 opening 问题

### Action type
`NO_ACTION` — 规则已覆盖

---

## Dimension 6: Decision usefulness (would the memo help someone decide?)

### Report A (GPT)
- 提供条件化结论帮助读者理解特定情景下的概率
- 敏感性测试帮助读者判断概率对输入变化的敏感度
- 区分 core results 和 event-level assumptions，帮助读者理解哪部分可信，哪部分存疑
- 写了如果 pre-match 信息如何调整概率，帮助读者持续使用决策 memo

### Report B (Local)
- 5 个 load-bearing variables 定义明确，有结构价值
- reversal conditions 和 pre-match monitoring signals 帮助读者知道何时应改变预测
- counter-evidence 部分帮助读者看到概率的另一面
- 但是概率方法不透明 → 读者无法自己推算如果某个变量变化，概率应如何变化

### Gap
- 本地版的决策有用性受 probability method opacity 严重限制
- 读者可以看到"变量 A、B、C"，但不知道它们以怎样的权重和规则变成 60/25/15
- 如果读者想调整某个变量的评估（例如"我觉得这支球队近期状态更好"），没有复算通道

### Current status
✅ 已由 [#306](https://github.com/ShadyUnderLight/deep-research-skill/issues/306)、[#307](https://github.com/ShadyUnderLight/deep-research-skill/issues/307)、[#309](https://github.com/ShadyUnderLight/deep-research-skill/issues/309) 联合覆盖：
- [#307](https://github.com/ShadyUnderLight/deep-research-skill/issues/307)：要求 probability / score ranking 必须有从 evidence 到结论的可复算通道
- [#309](https://github.com/ShadyUnderLight/deep-research-skill/issues/309)：要求 decision scope 明确改变结论的条件
- [#306](https://github.com/ShadyUnderLight/deep-research-skill/issues/306)：保证 constrained-choice 路由的所有 validator 稳定触发

### Eval regression assets
- `evals/cases/world-cup-prediction-constrained-choice-probability-method-case.md` — 综合 eval

### Action type
`NO_ACTION` — 规则已覆盖

---

## Candidate-action summary

| # | Candidate action | Failure family | Action type | Proposed home |
|---|---|---|---|---|
| 1 | Constrained-choice audit_report 总控接入 | route-wiring / process-integrity | `NO_ACTION` | Already closed by [#306](https://github.com/ShadyUnderLight/deep-research-skill/issues/306) |
| 2 | Scoring-replicability validator for constrained-choice | probability-method / numerical-discipline | `NO_ACTION` | Already closed by [#307](https://github.com/ShadyUnderLight/deep-research-skill/issues/307) |
| 3 | Decision Scope block with pre-match snapshot forced | current-state / opening-flow | `NO_ACTION` | Already closed by [#309](https://github.com/ShadyUnderLight/deep-research-skill/issues/309) |
| 4 | Self-assessment accuracy gate for constrained-choice | process-integrity | `NO_ACTION` | Already closed by [#306](https://github.com/ShadyUnderLight/deep-research-skill/issues/306) |
| 5 | Judgment-first front page layout | structural-readability | `NO_ACTION` | Already closed by [#309](https://github.com/ShadyUnderLight/deep-research-skill/issues/309) |
| 6 | Aggregator source caveat for Wikipedia/Transfermarkt | source-traceability | `NO_ACTION` | Already covered by [#306](https://github.com/ShadyUnderLight/deep-research-skill/issues/306) via validator chain |

**Summary: All 6 candidate actions are `NO_ACTION` (all gaps closed by #306, #307, #309).**

---

## Triage notes

### Why all candidates are NO_ACTION

Each gap identified in the original paired-report comparison has been systematically addressed by issues [#306](https://github.com/ShadyUnderLight/deep-research-skill/issues/306), [#307](https://github.com/ShadyUnderLight/deep-research-skill/issues/307), and [#309](https://github.com/ShadyUnderLight/deep-research-skill/issues/309). This distillation exists to:

1. **Document that the loop is closed** — all known gaps from this paired comparison are now covered by rules, checklists, templates, or validator gates
2. **Provide a regression baseline** — if a future constrained-choice probability report passes through the pipeline and still exhibits any of these gaps, that is a regression
3. **Distinguish rule gaps from execution gaps** — most gaps were execution/wiring gaps (rules existed but constrained-choice route wasn't wired to audit_report), not missing rules

### Relative to TSMC comparative distillation

This file is the second controlled comparative distillation (following TSMC GPT-vs-local). The TSMC case addressed listed-company route gaps (DCF, capital return, customer concentration). This case addresses constrained-choice probability-distribution gaps (probability method, scoring replicability, decision scope, route wiring).

The two distillations share a common structural weakness in the local pipeline: **route-specific validators were not wired into audit_report's total control, causing existing quality gates to silently not fire for certain routes.** Both TSMC and World Cup comparisons triggered route-wiring fixes (#276 for listed-company, #306 for constrained-choice).

---

## Things explicitly rejected

| Observation | Why rejected |
|---|---|
| GPT 版应被作为"概率方法标准输出格式" | GPT 版使用 `turn...` citation 格式，不满足仓库 Source Register 纪律和 route/audit status 要求——不是可接受交付物 |
| 本地版应被废弃 | 本地版的 constrained-choice 结构（variable definition、reversal conditions、counter-evidence）依然有价值，只是执行纪律有缺口 |
| 需要新增"GPT probability model compatibility mode" | 仓库已有自己的概率方法复制性要求和 scoring-replicability validator，不需要反向适配 |
| `turn...` citation 格式可以部分采纳 | 这种引用格式在 GPT 会话外不可复核——不可采用的 artifact。见下方专门说明。 |
| 这个 comparative-distillation 应放在 `evals/cases/` 下 | `evals/README.md` 明确定义 comparative-distillation 应放在 `evals/comparative-distillation/`，使用 `*-comparative-distillation.md` 命名 |

### Turn... citation format — explicitly rejected

GPT 版使用形如 `turn...` 的 citation artifact 提供正文引用来源。该格式在 GPT 深度研究界面内可点击回溯，但在仓库中 **不可复核、不可检查、不可持久化**。

- 该格式提供的信息（来源、置信度、上下文）在复制到本地后全部丢失
- 该格式不能映射到仓库的 7 列 Source Register 体系
- 该格式不允许 reviewer 独立验证来源

**结论：** `turn...` 格式是 GPT 的专有输出 artifact，不在本仓库采纳范围内。GPT 版在 claim-level attribution density 上的优势（每个关键论断都有来源标注）是值得学习的写作文本习惯，但具体 format 不可采用。

---

## Final judgment

### What the stronger report did better
- GPT 版在概率方法论透明度（logit → Poisson → Monte Carlo 路径）上更强
- GPT 版对 pre-match 未知项的纪律更显式（首发、裁判、天气未确认标注）
- GPT 版更好地区分了高置信度 core results 和低置信度 event-level assumptions
- GPT 版的条件化结论方式（"在特定条件下"）降低了 over-promise 风险

### What should change in the repo now
- ✅ 全部已通过 [#306](https://github.com/ShadyUnderLight/deep-research-skill/issues/306)、[#307](https://github.com/ShadyUnderLight/deep-research-skill/issues/307)、[#309](https://github.com/ShadyUnderLight/deep-research-skill/issues/309) 落地
- 所有 6 个维度均已覆盖规则或 validator 链
- 本文件作为 regression 基线

### What should wait for another confirming case
- 概率分布类 constrained-choice 报告的 sensitivity 要求 — 当前 scoring-replicability validator 强制要求 from-evidence-to-probability mapping，但对 sensitivity matrix（不同输入条件下概率移动范围）尚未作为硬门。如果 future constrained-choice 概率报告再次出现单点概率无敏感性展示，应考虑升级该要求到 blocking 级别。

### Is this mainly a missing rule, missing trigger, or execution problem?
- **Probability method opacity / numeric roles**: Missing rule（无概率方法可复现检查）→ 已由 [#307](https://github.com/ShadyUnderLight/deep-research-skill/issues/307) 修复
- **Route wiring (source traceability, self-assessment)**: Execution problem（constrained-choice route 未接入 audit_report）→ 已由 [#306](https://github.com/ShadyUnderLight/deep-research-skill/issues/306) 修复
- **Metadata-first drift / pre-match snapshot**: Missing template（模板未规定 judgment-first 布局和 Decision Scope）→ 已由 [#309](https://github.com/ShadyUnderLight/deep-research-skill/issues/309) 修复
- **Aggregator source caveat**: Missing execution（validator 存在但 constrained-choice 路由不触发）→ 已由 [#306](https://github.com/ShadyUnderLight/deep-research-skill/issues/306) 修复

**混合类型：** 该对比暴露了规则缺口（概率方法）、触发缺口（constrained-choice 路由未接入总控）和模板缺口（无 Decision Scope 块）。均已按场景修复。

---

## Minimal quality bar

- [x] the two reports are comparable enough to justify distillation
- [x] the comparison used the six fixed dimensions
- [x] each accepted candidate has an action type
- [x] each accepted candidate has a proposed repo home
- [x] at least one rejected observation is documented when relevant
- [x] the final judgment distinguishes rule gap vs trigger gap vs execution gap
