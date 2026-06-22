# AI Agent API Market Outlook GPT-vs-Local Comparative Distillation

> **目的：** 将 GPT 深度研究版与本地 deep-research-skill 版对 AI Agent / Research API 聚合市场 18 个月展望的 paired-report 对比固化为回归资产，识别 market-outlook 路线中 register 纪律、monitoring actionability 和路线边界的最大失败模式。

---

## Case identity

- **Case name:** Agent API market outlook GPT-vs-local comparative distillation
- **Date:** 2026-06-18
- **Research question:** 本地 AI Agent / Research API 聚合市场 18 个月展望
- **Why this comparison matters:**
  - 两组报告面对同一 market-outlook 题目，GPT 版在术语/市场边界定义、参与者地图、客户细分、商业化闭环方面有更清晰的模板结构。
  - 本地版在整体结构（snapshot、drivers/blockers、scenarios、stakeholder coverage）上完整，但 register 和 monitoring 执行有严重缺口。
  - 本对比验证 #329（类别边界、参与者地图、商业化闭环）和 #330（图表语义完整性）是否充分覆盖了结构差距，同时暴露了本地版的 execution-level 问题。
- **Report A:** GPT 深度研究版 `AI Agent / Research API 聚合市场 18 个月展望.md`
- **Report B:** 本地 deep-research-skill 版（同一 prompt，对比报告）
- **Reference / stronger report (if any):** 各有所长：GPT 版在结构完整性和图表辅助上更强，本地版在 self-assessment 和 trajectory 诚实性上更严谨
- **Prompt(s):** 本地 AI Agent / Research API 聚合市场 18 个月展望，需输出结构化市场展望备忘录。
- **Important scope or timing differences:**
  - 两份报告均基于 2026 年初数据，时间窗口一致
  - 对比焦点在结构性差异和纪律执行，特别是 register inflation 和 monitoring actionability

---

## Comparison purpose

This comparison is for:

1. 识别 market-outlook 路线中 register 纪律的 severity benchmark（100% inflation）
2. 验证 #329 的类别边界、参与者地图、商业化模板是否已覆盖 GPT 的结构优势
3. 暴露 monitoring actionability 和路线边界文档的缺口
4. 将 paired-report 基线固化为将来 regression 资产

---

## Dimension 1: Current-state discipline

### Report A (GPT)
- 有专门的市场定义和边界章节（"术语说明/市场边界"、"参与者地图"）
- 明确列出覆盖范围（只限 API 聚合层，不含底层模型训练或应用层）
- 市场大小和增长率为 estimate 但无 role label 或 access date

### Report B (Local)
- 有 market snapshot 和 current-state 章节
- 当前状态数字有时缺少 source role 标注
- 市场定义/boundary 声明不如 GPT 版明确

### Gap
- 市场边界声明在本地版中执行不一致：有时隐含"整个市场"但实际只覆盖部分
- #329 已增加 category boundary 和 participant map 模板应覆盖此问题

### Candidate action
- 验证 #329 的 category boundary 和 participant map 模板是否在 market-outlook 执行中自动激活

### Action type
- `NO_ACTION`（#329 已覆盖）

---

## Dimension 2: Numerical and date discipline

### Report A (GPT)
- funding、stars、request volume、latency、market share 等数字密集
- 无 role label：读者无法区分 observed / proxy / estimate / scenario
- 部分数字从公开来源提取但无 `[Sxx]`

### Report B (Local)
- 定量角色规则已存在于 checklists 但 agent 执行不完整
- 5 列 Source Register（缺 Reliability 和 Claims Supported）→ register 格式违规

### Gap
- 本地版的 register 列数违规（5 列而非 7 列）和 body citation 缺失（34 条注册，0% 正文引用）是执行问题而非规则缺失
- 规则要求 7 列和 >25% inflation 即触发硬失败

### Candidate action
- 无新规则；确保 market-outlook route 在最终审核中严格执行 register 格式和 body citation 率检查

### Action type
- `NO_ACTION`

---

## Dimension 3: Source traceability and evidence weighting

### Report A (GPT)
- 文末 bibliography 替代正文 `[Sxx]`
- claim 不可追溯
- 行业媒体承载 confirmed fact（证据权重混淆）

### Report B (Local)
- 34 条 register 条目，0% 在正文中被引用 → 100% inflation
- Source Register 仅 5 列（缺 Reliability 和 Claims Supported）
- 推理寄存器（I01-I04）已定义但正文从未使用 `[Ixx]` → 基础设施存在但功能失效

### Gap
- 100% register inflation 是项目 eval 集中最严重水平的 severity benchmark
- 推理寄存器 disconnected from body 是新的失败模式：register 存在但功能性缺失
- 这是执行问题（规则已存在 trigger 条件），不是规则缺失

### Candidate action
- 将 100% register inflation 作为 market-outlook severity benchmark 记录到 eval 集（已通过 eval case 覆盖）
- 推理寄存器 disconnected from body 的 detection 方法需文档化

### Action type
- `CHECKLIST_HARDENING`

---

## Dimension 4: Forward-looking claim discipline

### Report A (GPT)
- Mermaid Gantt 图绘制了假设性并购时间线（2026-09 云厂商收购聚合平台等）
- 这些 scenario assumption 被呈现为确定日期路线图，无 scenario 标签
- 场景概率 55%/25%/20% 无方法说明

### Report B (Local)
- 当前 forward-looking claims checklist 要求概率标签和 method basis
- 场景概率精确百分比若无 method 会触发 warning
- #330 已增加图表语义完整性校验

### Gap
- GPT 版的问题（假设事件画成 roadmap、概率无方法）已被 #330 识别
- 本地版的主要问题是 monitoring 信号不满足 4 字段 actionability 要求（threshold、cadence、source、trigger-to-action）

### Candidate action
- 在 market-outlook-audit.md 中增加 monitoring signal actionability 的 4 字段验证强化

### Action type
- `CHECKLIST_HARDENING`

---

## Dimension 5: Structural readability and information density

### Report A (GPT)
- 清晰的章节结构：市场边界→参与者→客户细分→竞争→商业化→监管传导→季度路线图
- Mermaid 图辅助表达（Gantt、pie、quadrant）
- 但部分图表语义不准确（pie 称为"概率分布"但实际是权重）

### Report B (Local)
- #329 已增加：类别边界（term/boundary）、参与者地图（participant map）、客户细分（demand segmentation）、商业化（commercialization）、监管传导（regulatory-to-business）
- #330 已增加图表语义完整性校验
- 结构面差距已被跟踪 issue 覆盖

### Gap
- #329 和 #330 覆盖后结构面差距已消除
- 需要验证这些模板和校验器是否在 agent 执行中激活

### Candidate action
- 无新规则；#329、#330 的 implementation 已验证，剩余是执行监控

### Action type
- `NO_ACTION`

---

## Dimension 6: Decision usefulness

### Report A (GPT)
- 有 stakeholder-specific 建议（投资者、运营商、硬件厂商、政策制定者）
- 但无 decision/action/metric/trigger 结构化行动表
- "最佳的 bet"等 ranking 式声明无路线边界文档

### Report B (Local)
- 当前模板有 stakeholder implications 但有时不满足 action table 要求
- 报告包含 player ranking/competitive positioning 内容但未文档说明为什么路由是 market-outlook 而非 competitive-positioning

### Gap
- 路线边界文档缺失：当报告包含"最佳选择"、"最强玩家"等 competitive-positioning 内容时，未解释为什么主路由不是 competitive-positioning
- Stakeholder action table 升级（#320）存在但执行可见性不足
- Monitoring 信号不满足 actionability 要求

### Candidate action
- 在 market-outlook 模板或 audit 中增加 route boundary 检查：如果输出含 competitive-positioning 内容但 route 声明为 market-outlook，要求文档说明理由

### Action type
- `NEW_RULE`

---

## Candidate-action summary

| # | Candidate action | Failure family | Action type | Proposed home |
|---|---|---|---|---|
| 1 | 推理寄存器 disconnected from body：register 存在但功能性缺失的 detection 方法文档化 | source-traceability / register-disconnected | `CHECKLIST_HARDENING` | `checklists/final-audit.md` |
| 2 | monitoring signal actionability 4 字段（threshold、cadence、source、trigger-to-action）验证强化 | forward-looking / monitoring-actionability | `CHECKLIST_HARDENING` | `checklists/market-outlook-audit.md` |
| 3 | route boundary 检查：market-outlook 含 competitive-positioning 内容时要求文档说明理由 | route-boundary / route-inflation | `NEW_RULE` | `checklists/market-outlook-audit.md` |

---

## Triage notes

### Candidate 1: inference register disconnected from body
- **Why it matters:** 推理寄存器与正文断连是新的失败模式：基础设施存在但功能失效。这比"完全缺失"更难 detection 因为 register 本身看起来完整。
- **Why it is reusable:** 适用于所有使用推理寄存器的报告类型。
- **Why this home is best:** final-audit.md 是跨路线审核点，适合加入跨线路的 register functionality 检查。
- **Promotion status:** `PROMOTE_NOW`

### Candidate 2: monitoring actionability 4-field verification
- **Why it matters:** monitoring 信号是 market-outlook 的核心决策工具，不满足 4 字段 actionability 时信号无实际操作价值。
- **Why it is reusable:** 仅限 market-outlook 路线。
- **Why this home is best:** market-outlook-audit.md 已是路线专用 checklist。
- **Promotion status:** `PROMOTE_NOW`

### Candidate 3: route boundary for market-outlook with positioning content
- **Why it matters:** 当前路线边界检查主要检查"是否选错路由"，但不检查"主路由正确但输出包含了其他路线内容而未文档化"。
- **Why it is reusable:** 适用于所有可能产生路线交叉的报告类型。
- **Why this home is best:** market-outlook-audit.md 是路线专用审核点。
- **Promotion status:** `PROMOTE_NOW`

---

## Things explicitly rejected

| Observation | Why rejected |
|---|---|
| GPT 版的市场边界定义和参与者地图 | #329 已覆盖，不重复推广 |
| GPT 版的商业化闭环和监管传导分析 | #329 已覆盖，不重复推广 |
| GPT 版的 Mermaid Gantt/pie/quadrant | #330 已覆盖图表语义完整性校验 |
| GPT 版精确场景概率（55/25/20）| 已有 forward-looking label 纪律覆盖 |
| GPT 版文末 bibliography 替代正文 `[Sxx]` | 不符合 source traceability 纪律，不接受 |

---

## Final judgment

### What the stronger report did better
- GPT 版在市场边界/术语定义、参与者地图、客户细分和商业化结构上更完整（#329、#330 已覆盖）
- 图表辅助增强了信息密度（#330 已覆盖校验）

### What should change in the repo now
- checklists/market-outlook-audit.md 增加 monitoring signal actionability 4 字段验证
- checklists/final-audit.md 增加推理寄存器断连检测方法
- checklists/market-outlook-audit.md 增加 route boundary 检查（market-outlook + positioning）

### What should wait for another confirming case
- 推理寄存器断连检测需先在 eval 集中验证再推广到其他路线

### Is this mainly a missing rule, missing trigger, or execution problem?
- 混合型：
  - Monitoring actionability 和推理寄存器断连是 **execution problem**：规则存在但未激活
  - Route boundary（market-outlook + positioning）是 **missing rule**：现有规则只检查"是否选错路由"，不检查选了正确路由但包含了未文档的其他路线内容
  - 结构面差距已被 #329、#330 覆盖

---

## Minimal quality bar

- [x] the two reports are comparable enough to justify distillation
- [x] the comparison used the six fixed dimensions
- [x] each accepted candidate has an action type
- [x] each accepted candidate has a proposed repo home
- [x] at least one rejected observation is documented when relevant
- [x] the final judgment distinguishes rule gap vs trigger gap vs execution gap
