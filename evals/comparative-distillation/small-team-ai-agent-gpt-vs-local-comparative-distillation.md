# Small Team AI Agent GPT-vs-Local Comparative Distillation

> **目的：** 将 GPT 深度研究版与本地 deep-research-skill 版对小团队 AI Agent 接入的 paired-report 对比固化为回归资产，识别模板级别的结构性差距。

---

## Case identity

- **Case name:** Small-team AI Agent GPT-vs-local comparative distillation
- **Date:** 2026-06-17
- **Research question:** 小团队是否应将客服、运营与数据分析统一接入 AI Agent？
- **Why this comparison matters:**
  - 两组报告面对相同的组织落地类决策问题，但结构质量差异显著。
  - GPT 版在输入边界说明、选项对比与实施路线一体化方面有可借鉴的模板能力。
  - 本地版在源追溯和证据纪律上更严格，但"读者可用结构"有所欠缺。
- **Report A:** GPT 深度研究版 `小团队AI Agent接入决策分析.md`
- **Report B:** 本地 deep-research-skill 版（未留存）
- **Reference / stronger report (if any):** GPT 版（结构面更强），本地版（纪律面更强）
- **Prompt(s):** 小团队是否应将客服、运营与数据分析统一接入 AI Agent？
- **Important scope or timing differences:**
  - 两份报告均基于 2026 年初数据，时间窗口基本一致
  - 对比焦点在结构性差异，而非事实检索能力或结论准确性
  - 本地版未留存报告，对比基于 issue #320 中记录的 GPT 报告特征与当前模板的 gap 分析

---

## Comparison purpose

This comparison is for:

1. 识别 template 层面缺少的输入边界声明机制（Input boundary / 未指定项）
2. 识别 option-selection 结构中缺少的实施路线维度
3. 将 paired-report 基线固化为将来 regression 资产

---

## Dimension 1: Current-state discipline

### Report A (GPT)
- 有专门的「评估边界与现状假设」章节，列出团队规模、角色构成、客服渠道、数据来源等"已明确/未指定"项
- 明确说明结论适用范围而非隐含限制

### Report B (Local)
- 当前模板无 input boundary 声明机制
- Decision Scope block 有「关键未知」但无系统化的"未指定项→assumption→sensitivity"链路

### Gap
- 缺少一个标准化的输入边界表，导致推荐看似普适但实际隐含多个未指定前提
- 未指定项有时被悄悄补全而不是转为显式假设

### Candidate action
- 在 report-template.md 中增加"未指定项与输入边界"小节
- 要求未指定项转为显式假设，若翻转结论则进入 sensitivity 分析

### Action type
`TEMPLATE_CHANGE`

---

## Dimension 2: Numerical and date discipline

### Report A (GPT)
- 成本基线、时间窗口等数字有范围说明但缺少正式数字角色标签
- 未区分 observed / estimate / assumption

### Report B (Local)
- 当前模板有 Quantitative role labeling 纪律和数字角色列要求
- 在数字角色上更严格

### Gap
- GPT 版在数字精度和角色标注上不如本地版
- **这不是本地版需要学习的方向**

### Candidate action
- 无 — 当前系统在数字角色上已优于 GPT

### Action type
`NO_ACTION`

---

## Dimension 3: Source traceability and evidence weighting

### Report A (GPT)
- 引用依赖 `turn...` 或文末 bibliography
- 正文无 `[Sxx]` claim-level traceability
- 数字无 source role 标签（observed / estimate / forecast / scenario）

### Report B (Local)
- 强制 7 列 Source Register + `[Sxx]` 正文引用
- 要求 claim-level evidence label ([CONF] / [INFER] / [UNKN])

### Gap
- GPT 版 sourcing 纪律不可接受
- **本地版不能继承 GPT 的 bibliography-only sourcing 或不可复查的 citation**

### Candidate action
- 在蒸馏 artifact 中明确记录"GPT 版 sourcing 缺陷不可继承"
- 无规则变更

### Action type
`NO_ACTION`（但需在 distilled learning 中注明边界）

---

## Dimension 4: Forward-looking claim discipline

### Report A (GPT)
- 实施了前瞻声明，但来源归属不够精确
- 有些 future 陈述未标明归因

### Report B (Local)
- 要求每个 forward-looking claim 有 named source attribution
- 要求 label source role（analyst estimate / scenario / roadmap 等）
- 对「预计」等触发词有硬性归属要求

### Gap
- 本地版在此维度已更严格，无需向 GPT 学习

### Candidate action
- 无

### Action type
`NO_ACTION`

---

## Dimension 5: Structural readability and information density

### Report A (GPT)
- 选项对比 + 推荐路径 + 实施路线一体化：不接入 / 部分接入 / 全面接入；集中式 Agent / 分布式微代理 / 混合架构
- 有明确的阶段划分：准备阶段 → MVP → 扩展 → 强化 → 稳态
- 按 stakeholder 分层给出行动建议（业务 owner、数据 owner、AI 运营 owner）

### Report B (Local)
- 现有 option-selection 结构有 ranking 和 recommendation 但缺少 implementation roadmap
- Stakeholder implications 已有但停留在方向性描述，未升级为 action table
- 现有模板没有"阶段"或"实施路线"维度

### Gap
- 没有实施路线：读者知道结论但不知道"先做什么、别做什么、什么时候扩大范围"
- Stakeholder 建议不够可执行：缺少决策/行动/指标/触发四要素

### Candidate action
- 在 decision-report-template.md 的 option-selection 结构中增加实施路线模板
- 在 market-outlook-and-scenario-discipline.md 中将 stakeholder implications 升级为 action table

### Action type
`TEMPLATE_CHANGE`

---

## Dimension 6: Decision usefulness

### Report A (GPT)
- 读者不仅知道结论，还知道"先做什么、别做什么、什么时候扩大范围"
- 按角色给出具体行动：业务 owner、数据 owner、AI 运营 owner
- 区分 MVP 与终局，不把终局架构当第一阶段建议

### Report B (Local)
- 结论清晰，但缺少实施维度的决策支持
- 方向性描述有余，可执行性不足

### Gap
- 对于有落地决策负担的报告，缺失实施路线和 stake-holder action table 会降低决策可用性

### Candidate action
- 实施路线模板
- Stakeholder action table

### Action type
`TEMPLATE_CHANGE`

---

## Candidate-action summary

| # | Candidate action | Failure family | Action type | Proposed home |
|---|---|---|---|---|
| 1 | Input boundary / 未指定项 声明块 | output structure / info density | `TEMPLATE_CHANGE` | `references/report-template.md` |
| 2 | Implementation stages integration in option-selection | output structure / info density | `TEMPLATE_CHANGE` | `references/decision-report-template.md` |
| 3 | Stakeholder action table (decision/action/metric/trigger) | scope completeness / coverage geometry | `TEMPLATE_CHANGE` | `references/market-outlook-and-scenario-discipline.md` |

---

## Triage notes

### Candidate 1: Input boundary / 未指定项
- **Why it matters:** 未经明确说明的"未指定项"隐含在结论中，会让读者误以为推荐适用于比实际更宽的场景。
- **Why it is reusable:** 适用于 constrained-choice、provider-selection、market-entry、market-outlook 中涉及组织落地或方案选择的问题。
- **Why this home is best:** report-template.md 是所有报告的默认模板，放在已存在的 Market-entry formatting discipline 之后最合理。
- **Promotion status:** `PROMOTE_NOW`

### Candidate 2: Implementation stages integration
- **Why it matters:** 读者不仅需要知道"选什么"，还需要知道"先做什么、不做什么、什么时候扩大"。
- **Why it is reusable:** 适用于所有有实施/部署/组织变更负担的推荐类报告。
- **Why this home is best:** decision-report-template.md 的 option-selection 结构已经有 ranking 和 recommendation，实施路线是其自然扩展。
- **Promotion status:** `PROMOTE_NOW`

### Candidate 3: Stakeholder action table
- **Why it matters:** 方向性描述（"利好投资者"）不如可执行建议（"投资者应关注XX指标，若YY则调整"）对决策有用。
- **Why it is reusable:** 适用于 market-outlook 和所有涉及多角色决策的报告。
- **Why this home is best:** market-outlook-and-scenario-discipline.md 已有 §Stakeholder implications discipline，action table 是该节的升级。
- **Promotion status:** `PROMOTE_NOW`

---

## Things explicitly rejected

| Observation | Why rejected |
|---|---|
| GPT 版的文末 bibliography 替代正文 `[Sxx]` | 不符合 source traceability 纪律，不接受 |
| GPT 版的 `turn...` 不可复查引用 | 引用不可复核，不接受 |
| GPT 版数字无 role label | 当前 skill 已有 quantitative role labeling 纪律且更严格 |
| GPT 版 vendor/Wikipedia 承载 confirmed fact | 当前 skill 有 source-type 分类纪律阻止此模式 |

---

## Final judgment

### What the stronger report did better
- GPT 版在"读者可用结构"上更强：输入边界声明、选项对比+实施路线一体化、按角色分层行动建议

### What should change in the repo now
- report-template.md 增加输入边界/未指定项小节
- decision-report-template.md 增加实施路线模板
- market-outlook-and-scenario-discipline.md 升级 stakeholder implications 为 action table

### What should wait for another confirming case
- 其他 GPT 报告的结构特征（如区域矩阵、价值链敏感图）需等数据中心电力蒸馏 case 确认后再统一推广

### Is this mainly a missing rule, missing trigger, or execution problem?
- 主要是 **missing template**：输入边界和实施路线是模板层面的缺失，不是已有规则的执行失败

---

## Minimal quality bar

- [x] the two reports are comparable enough to justify distillation
- [x] the comparison used the six fixed dimensions
- [x] each accepted candidate has an action type
- [x] each accepted candidate has a proposed repo home
- [x] at least one rejected observation is documented
- [x] the final judgment distinguishes rule gap vs trigger gap vs execution gap
