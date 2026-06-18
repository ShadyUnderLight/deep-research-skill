# Data Center Power Bottleneck GPT-vs-Local Comparative Distillation

> **目的：** 将 GPT 深度研究版与本地 deep-research-skill 版对全球数据中心电力瓶颈的 paired-report 对比固化为回归资产，识别行业的产业链敏感图、区域覆盖率、行动建议门槛等模板层面的结构性差距。

---

## Case identity

- **Case name:** Data center power bottleneck GPT-vs-local comparative distillation
- **Date:** 2026-06-17
- **Research question:** 全球数据中心电力瓶颈会如何影响 AI 基础设施产业链？
- **Why this comparison matters:**
  - 两份报告面对同一产业链主题，GPT 版在产业链分层、区域矩阵和 stakeholder-specific 行动建议上有可借鉴的模板能力。
  - 本地版在 sourcing 纪律和数字角色标注上更严格，但缺少产业链敏感图和区域覆盖门槛。
- **Report A:** GPT 深度研究版 `全球数据中心电力瓶颈对AI基础设施产业链影响分析.md`
- **Report B:** 本地 deep-research-skill 版（未留存）
- **Reference / stronger report (if any):** GPT 版（结构面更强），本地版（纪律面更强）
- **Prompt(s):** 全球数据中心电力瓶颈会如何影响 AI 基础设施产业链？
- **Important scope or timing differences:**
  - 两份报告均基于 2025-2026 数据，时间窗口基本一致
  - 对比焦点在结构性差异，特别是产业链分析和区域 coverage
  - 本地版未留存报告，对比基于 issue #320 中记录的 GPT 报告特征与当前模板的 gap 分析

---

## Comparison purpose

This comparison is for:

1. 识别 market-outlook 模板中缺少的 Value-chain sensitivity map 机制
2. 识别 global scope 报告中缺少的 Regional coverage matrix 门槛
3. 验证 small-team AI Agent 蒸馏 case 中的 stakeholder action table 建议是否在本 case 中有独立复现
4. 将 paired-report 基线固化为将来 regression 资产

---

## Dimension 1: Current-state discipline

### Report A (GPT)
- 有清晰的产业链分层：上游（电力供应与电网）、中游（数据中心建设与运营）、下游（AI 硬件制造与云服务）
- 每个层级描述了当前 state、瓶颈机制、影响时间

### Report B (Local)
- 当前模板有 market snapshot 要求，但无自动的产业链分层默认结构
- 当前系统在约束少时可能产生平铺式产业描述而非分层敏感分析

### Gap
- 当题目含"产业链"、"value chain"、"supply chain"、"infrastructure chain"时，当前模板没有要求 Value-chain sensitivity map
- 同一瓶颈在不同链条位置产生不同影响（电网排队 vs 园区选址 vs 液冷功率）的分析结构没有标准化

### Candidate action
- 在 market-outlook-and-scenario-discipline.md 中增加 Value-chain sensitivity map 小节
- 在 market-outlook-audit.md 中增加对应的 checklist 项

### Action type
`TEMPLATE_CHANGE` + `CHECKLIST_HARDENING`

---

## Dimension 2: Numerical and date discipline

### Report A (GPT)
- 按区域列出了 TWh、PUE、可再生能源占比、电价等数据
- 但数字的文末 reference 列表缺乏正文 `[Sxx]` 追溯
- 数字没有 source role 标签（observed / estimate / forecast / scenario）

### Report B (Local)
- 强制 `[Sxx]` 正文引用 + 数字角色标签
- 在数字纪律上更严格

### Gap
- 区域矩阵本身是好结构，但 GPT 版缺少 role labeling 和 inline citation
- 应吸收区域矩阵结构，同时附加本 skill 的数据纪律

### Candidate action
- 增加 Regional coverage matrix 模板，要求每个数字有 `[Sxx]` 引用和 Data role 列
- 对声称"全球"但只覆盖欧美+中国的报告触发 scope completeness warning

### Action type
`TEMPLATE_CHANGE` + `CHECKLIST_HARDENING`

---

## Dimension 3: Source traceability and evidence weighting

### Report A (GPT)
- 文末列了参考来源，但正文无 `[Sxx]` claim-level traceability
- 部分数字来自 industry media / vendor 但没有 source-type 分级

### Report B (Local)
- 强制 7 列 Source Register + `[Sxx]` 正文引用
- Source-type 分类（primary / secondary / inferred / vendor / Wikipedia 等）

### Gap
- GPT 版 sourcing 纪律不可接受
- **本地版不能继承 GPT 的 bibliography-only sourcing 或不可复查的 citation**

### Candidate action
- 在蒸馏 artifact 中明确记录"GPT 版区域矩阵数据缺乏 inline 引用和 role labeling — 我们吸收结构但不继承纪律缺陷"
- 无规则变更

### Action type
`NO_ACTION`（但需在 distilled learning 中注明边界）

---

## Dimension 4: Forward-looking claim discipline

### Report A (GPT)
- 有前瞻性预测但 source 角色不够精确
- 预测数字没有区分 analyst estimate / scenario / model output

### Report B (Local)
- 要求每个 forward-looking claim 有 named source attribution
- 对「预计」等触发词有硬性归属要求
- 前瞻数字不得标为 [CONF]

### Gap
- 本地版在此维度已更严格

### Candidate action
- 无

### Action type
`NO_ACTION`

---

## Dimension 5: Structural readability and information density

### Report A (GPT)
- 产业链分层清晰：上游/中游/下游
- 区域对比表：北美、欧盟、中国、印度、东南亚、中东/非洲
- 每个区域列 TWh、PUE、可再生能源、电价、主要运营商
- 行动建议按 stakeholder 分层：投资者、云/数据中心运营商、AI 硬件厂商、政策制定者

### Report B (Local)
- Stakholder implications 已要求覆盖 ≥3 类型
- 但缺少产业链敏感图标准模板
- 缺少区域覆盖矩阵
- Stakeholder 建议停留在方向性描述而非 action table

### Gap
- Value-chain sensitivity map：产业链结构描述优于平铺式分析
- Regional coverage matrix：全球主题不能只用单一区域数据
- Stakeholder action：从"利好/利空"升级为"决策/行动/指标/触发"

### Candidate action
- Value-chain sensitivity map → references + checklist
- Regional coverage matrix → references + checklist
- Stakeholder action table → references + checklist
- 三个候选均从本 case 独立产生，确认了与 small-team AI Agent case 的交叉验证

### Action type
`TEMPLATE_CHANGE` + `CHECKLIST_HARDENING`

---

## Dimension 6: Decision usefulness

### Report A (GPT)
- 行动建议写给不同角色（投资者、运营商、硬件厂商、政策制定者）
- 每个角色有具体行动而非方向性描述

### Report B (Local)
- 当前 stakeholder 覆盖已要求 ≥3 类
- 但建议停留在"what does this mean for them"的描述性层面
- 缺少触发条件和阈值

### Gap
- Action table 让建议比描述性段落更可执行

### Candidate action
- Stakeholder action table（decision / action / metric / trigger）
- 与 small-team AI Agent 蒸馏 case 的候选 3 一致 — cross-case 确认

### Action type
`TEMPLATE_CHANGE` + `CHECKLIST_HARDENING`

---

## Candidate-action summary

| # | Candidate action | Failure family | Action type | Proposed home |
|---|---|---|---|---|
| 1 | Value-chain sensitivity map for industry-chain market-outlook | scope completeness / coverage geometry | `TEMPLATE_CHANGE` + `CHECKLIST_HARDENING` | `references/market-outlook-and-scenario-discipline.md` + `checklists/market-outlook-audit.md` |
| 2 | Regional coverage matrix with source role for global scope | scope completeness / coverage geometry | `TEMPLATE_CHANGE` + `CHECKLIST_HARDENING` | `references/market-outlook-and-scenario-discipline.md` + `checklists/market-outlook-audit.md` |
| 3 | Stakeholder action table (decision/action/metric/trigger) | output structure / info density | `TEMPLATE_CHANGE` + `CHECKLIST_HARDENING` | `references/market-outlook-and-scenario-discipline.md` + `checklists/market-outlook-audit.md` |
| 4 | Input boundary / 未指定项 声明块（交叉验证自 small-team case） | output structure / info density | `TEMPLATE_CHANGE` | `references/report-template.md` |

---

## Triage notes

### Candidate 1: Value-chain sensitivity map
- **Why it matters:** 产业链主题的瓶颈传导机制在不同链条位置产生不同影响，平铺式产业描述无法呈现这种分层影响。
- **Why it is reusable:** 适用于所有含"产业链"、"value chain"、"supply chain"、"infrastructure chain"的 market-outlook 报告。
- **Why this home is best:** market-outlook-and-scenario-discipline.md 是市场展望类报告的方法文档，产业链敏感图是其自然扩展；market-outlook-audit.md 需要对应的检查项。
- **Promotion status:** `PROMOTE_NOW`（本 case 独立产出 + 与已有行业分析逻辑一致）

### Candidate 2: Regional coverage matrix
- **Why it matters:** "全球"不是单一区域事实。缺乏区域覆盖矩阵时，报告可能用欧美+中国数据声称全球结论。
- **Why it is reusable:** 适用于所有标题含"全球"、"global"、"区域"、"region"的 market-outlook 报告。
- **Why this home is best:** market-outlook-and-scenario-discipline.md 包含 scope completeness 和 stakeholder coverage，区域矩阵是其覆盖维度扩展。
- **Promotion status:** `PROMOTE_NOW`

### Candidate 3: Stakeholder action table
- **Why it matters:** 方向性描述（"利好投资者"）不如可执行建议（"投资者应关注XX指标，若YY则调整"）对决策有用。
- **Why it is reusable:** 本 case 独立产出该候选，与 small-team AI Agent case 交叉验证。
- **Why this home is best:** market-outlook-and-scenario-discipline.md 已有 §Stakeholder implications discipline，action table 是该节的升级。
- **Promotion status:** `PROMOTE_NOW`（cross-case 确认）

### Candidate 4: Input boundary / 未指定项（交叉验证）
- **Why it matters:** 数据中心能源主题同样涉及隐式假设（地理位置、电力结构、政策环境），输入边界声明同样适用。
- **Why it is reusable:** 与 small-team case 的候选 1 指向同一规则，cross-case 确认。
- **Why this home is best:** 同上 small-team case 分析。
- **Promotion status:** `PROMOTE_NOW`（cross-case 确认）

---

## Things explicitly rejected

| Observation | Why rejected |
|---|---|
| GPT 版的文末 bibliography 替代正文 `[Sxx]` | 不符合 source traceability 纪律，不接受 |
| GPT 版区域数字无 `[Sxx]` inline citation | 引用不可复核，不接受 |
| GPT 版将 industry media 数字当 confirmed fact | 当前 skill 有 source-type 分类纪律阻止 |
| GPT 版预测无 source role 区分 | 当前 skill 有 forward-looking label 纪律且更严格 |

---

## Final judgment

### What the stronger report did better
- GPT 版在产业链分析结构（上游/中游/下游分层）、区域覆盖矩阵（6 区域对比）、stakeholder-specific 行动建议上更强
- 这些结构适合 market-outlook / industry-evolution 模板吸收

### What should change in the repo now
- market-outlook-and-scenario-discipline.md 增加 Value-chain sensitivity map 小节
- 同上文件增加 Regional coverage matrix 小节
- 同上文件升级 Stakeholder implications 为 action table
- market-outlook-audit.md 增加对应 checklist 项目

### What should wait for another confirming case
- Input boundary 已被 small-team case 独立确认，不需等更多 case
- 其他结构性特征当前未发现

### Is this mainly a missing rule, missing trigger, or execution problem?
- 主要是 **missing template**：value-chain sensitivity map、regional coverage matrix 和 action table 当前在系统中不存在，不是执行失败

---

## Minimal quality bar

- [x] the two reports are comparable enough to justify distillation
- [x] the comparison used the six fixed dimensions
- [x] each accepted candidate has an action type
- [x] each accepted candidate has a proposed repo home
- [x] at least one rejected observation is documented
- [x] the final judgment distinguishes rule gap vs trigger gap vs execution gap
