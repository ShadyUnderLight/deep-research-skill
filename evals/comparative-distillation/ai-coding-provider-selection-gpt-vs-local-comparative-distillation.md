# AI Coding Agent Provider Selection GPT-vs-Local Comparative Distillation

> **目的：** 将 GPT 深度研究版与本地 deep-research-skill 版对中国大陆团队 Coding Agent 选型的 paired-report 对比固化为回归资产，识别 provider-selection 路线中企业落地结构、当前状态纪律和厂商声明治理的差距。

---

## Case identity

- **Case name:** AI Coding Agent provider selection GPT-vs-local comparative distillation
- **Date:** 2026-06-18
- **Research question:** 中国大陆团队如何选择默认 Coding Agent？
- **Why this comparison matters:**
  - 两组报告面对同一地域约束 provider-selection 问题，GPT 版在企业落地结构（推荐层级、团队规模路线、迁移步骤、TCO、未决问题）方面更完整。
  - 本地版在 route activation 和 self-assessment 纪律上更严格，但企业落地结构和当前状态验证存在缺口。
  - 本对比验证 provider-selection 路线在 #325（企业落地蓝图）、#327（provider enterprise rollout）覆盖后是否还有未捕获的结构优势。
- **Report A:** GPT 深度研究版 `中国大陆团队 Coding Agent 选型.md`
- **Report B:** 本地 deep-research-skill 版（同一 prompt，对比报告）
- **Reference / stronger report (if any):** GPT 版（结构面——企业落地部分更强），本地版（纪律面——sourcing 和 self-assessment 更强）
- **Prompt(s):** 中国大陆团队如何选择默认 Coding Agent？需输出结构化 provider-selection 决策备忘录。
- **Important scope or timing differences:**
  - 两份报告均基于 2026 年初数据，时间窗口一致
  - 对比焦点在结构性差异，尤其是企业落地蓝图和当前状态纪律

---

## Comparison purpose

This comparison is for:

1. 识别 provider-selection 路线中企业落地结构的 gap（推荐层级、团队规模路线、迁移步骤、TCO）
2. 验证 #325 和 #327 实施后是否已覆盖 GPT 的结构优势
3. 确认 provider-selection 的当前状态纪律缺口是否是执行问题而非模板缺失
4. 将 paired-report 基线固化为将来 regression 资产

---

## Dimension 1: Current-state discipline

### Report A (GPT)
- 有当前 provider 概览列表（平台、模型、定价、中国大陆可访问性）
- 但依赖厂商文档作为`[确认事实]`，无 source role 标注
- 部分平台支持信息过时（Codex 仅 macOS desktop 与实际 web/CLI/IDE/macOS/Windows 不符）

### Report B (Local)
- 当前状态验证要求已存在于 checklists 但执行不完整
- 对 fast-moving provider 产品缺少 external verification 机制
- 部分 provider claim 源自厂商文档且未标 source role

### Gap
- 本地系统要求 current-state snapshot 但缺少"external verifiability"检查：对 fast-moving provider，如果 claim 可被官方文档证伪应视为硬失败
- 厂商文档在 provider-selection 中承载了过多 load-bearing claim 而没有 system caveat
- 这是执行问题（EXISTING_RULE_NOT_EXECUTED），不是模板缺失

### Candidate action
- 在 provider-selection final audit 中增加 external verifiability check：每个 provider current-state claim 必须标注最后验证日期；如果 claim 可被当前官方文档证伪，触发硬失败

### Action type
- `CHECKLIST_HARDENING`

---

## Dimension 2: Numerical and date discipline

### Report A (GPT)
- 价格、团队规模、上下文窗口等比较数字存在但无 role label
- 多数数字来自厂商定价页或第三方估算，未区分 observed/proxy/estimate

### Report B (Local)
- 数字角色标注规则已在 checklists 中，但 provider-selection 场景中执行较弱
- 评分表、价格对比缺少 observed/proxy/assumption 标注

### Gap
- provider-selection 的数字角色缺口是执行问题：checklists 已有 numeric role labeling 要求但未在评分/价格对比表上贯彻
- 自审声称通过但实际缺失——process-integrity 问题

### Candidate action
- 确保 provider-selection 的评分/价格对比表在执行时触发 numeric role labeling checklist

### Action type
- `NO_ACTION`（规则已存在，需加强执行）

---

## Dimension 3: Source traceability and evidence weighting

### Report A (GPT)
- 文末 bibliography 替代正文 `[Sxx]`，无法逐 claim 追溯
- 厂商文档、行业媒体、Wikipedia 来源未区分 evidence tier
- 37 条 register 条目约 14 条无正文引用（>25% inflation）

### Report B (Local)
- 当前 skill 有严格 source register 和 body citation 纪律
- provider-selection 路线存在 register inflation >25% 的执行缺口

### Gap
- 报告 B register inflation >25% 触发硬失败规则已在 checklists 中，问题是执行失败
- 厂商声明未标注"(厂商文档，非独立验证)"

### Candidate action
- 在 provider-selection final audit 中加入厂商声明 caveat 检查

### Action type
- `CHECKLIST_HARDENING`

---

## Dimension 4: Forward-looking claim discipline

### Report A (GPT)
- 迁移步骤、TCO 估算包含 forward-looking claims
- 无 probabilistic labels 或 sensitivity 说明

### Report B (Local)
- 当前模板有 forward-looking claim audit
- provider-selection 的推荐通常不涉及大量预测，适用度较低

### Gap
- 差距不显著：provider-selection 的 forward-looking 元素较少

### Candidate action
- 无

### Action type
- `NO_ACTION`

---

## Dimension 5: Structural readability and information density

### Report A (GPT)
- 推荐层级清晰：1st tier / 2nd tier / 条件推荐
- 有独立的迁移步骤和建议实施路线
- 有未决问题清单

### Report B (Local)
- #325 和 #327 已增加 enterprise rollout structure（推荐层级、团队规模路线、迁移治理、完整 TCO）
- 当前模板在 recommending structure 方面已覆盖 GPT 的结构优势

### Gap
- 实施后差异缩小：#325、#327 已覆盖 GPT 在此维度的大部分优点
- 剩余差距是执行层面的：模板已更新但 agent 是否按模板执行不确定

### Candidate action
- 验证 #325 和 #327 的模板更新是否在 provider-selection 执行中自动激活

### Action type
- `NO_ACTION`（已通过 issue 覆盖）

---

## Dimension 6: Decision usefulness

### Report A (GPT)
- 推荐结论依赖排名，但未说明排名逆转条件
- TCO 估算无 sensitivity

### Report B (Local)
- 当前 option-selection 模板要求 ranking-reversal conditions、budget closure、shortlist boundary justification
- provider-selection 已有约束条件但执行不完整

### Gap
- 差距主要是执行层面：模板已有要求但 agent 在 provider 场景中激活不充分

### Candidate action
- 强化 provider-selection 场景的 option-selection final audit 激活率

### Action type
- `NO_ACTION`

---

## Candidate-action summary

List each accepted candidate briefly.

| # | Candidate action | Failure family | Action type | Proposed home |
|---|---|---|---|---|
| 1 | provider current-state external verifiability check：每个 claim 标注最后验证日期；可被官方文档证伪时硬失败 | current-state / provider-selection | `CHECKLIST_HARDENING` | `checklists/option-selection-final-audit.md` |
| 2 | 厂商声明 caveat：vendor docs 在正文中必须标注"(厂商文档，非独立验证)" | source traceability / vendor claim | `CHECKLIST_HARDENING` | `checklists/option-selection-final-audit.md` |
| 3 | 强化 provider-selection 场景的数字角色/自审一致性执行 | quantitative-role-label / process-integrity | `CHECKLIST_HARDENING` | `checklists/option-selection-final-audit.md` |

---

## Triage notes

### Candidate 1: provider current-state external verifiability
- **Why it matters:** fast-moving provider 产品的 current-state claim 可被官方文档证伪。现有 current-state 检查只验证"是否标注来源"，不验证"来源是否与当前官方信息一致"。
- **Why it is reusable:** 适用于所有 vendor/provider 类报告，特别是 AI 工具、云服务、API 产品。
- **Why this home is best:** option-selection-final-audit 已经是 provider-selection 路线的最终审核 checklist。
- **Promotion status:** `PROMOTE_NOW`

### Candidate 2: vendor claim discipline
- **Why it matters:** provider-selection 的主题本身就是 vendor 产品，vendor docs 与独立验证的边界尤其模糊。不标注消费者无法区分厂商声称与客观事实。
- **Why it is reusable:** 同样适用于 equipment-selection、market-entry 中引用厂商数据的场景。
- **Why this home is best:** 与现有 source-type 分类纪律并列。
- **Promotion status:** `PROMOTE_NOW`

### Candidate 3: provider-selection execution reinforcement
- **Why it matters:** 模板和 checklists 已覆盖但 agent 未自动激活，导致自审不准确。
- **Why this home is best:** 属于 route-specific trigger rate 改善，不是新规则。
- **Promotion status:** `PROMOTE_NOW`

---

## Things explicitly rejected

| Observation | Why rejected |
|---|---|
| GPT 版的企业落地结构（推荐层级、迁移步骤、TCO）| #325、#327 已覆盖，不重复推广 |
| GPT 版的文末 bibliography 替代正文 `[Sxx]` | 不符合 source traceability 纪律，不接受 |
| GPT 版数字无 role label | 当前 skill 已有 quantitative role labeling 纪律且更严格 |

---

## Final judgment

### What the stronger report did better
- GPT 版在"读者可用结构"上的企业落地部分更强，但 #325、#327 已覆盖这些差距
- GPT 版不像本地版有 register inflation、self-assessment overclaim 等纪律问题

### What should change in the repo now
- option-selection-final-audit.md 增加 provider current-state external verifiability check
- 同上文件增加 vendor claim caveat 检查

### What should wait for another confirming case
- Provider-selection 的结构性改进已由 #325、#327 完成，不需要等更多 case

### Is this mainly a missing rule, missing trigger, or execution problem?
- 主要是 **execution problem**：2/3 的候选动作是对已有规则的执行强化（checklist hardening），不是新规则或新模板。剩余 1/3 是对 fast-moving provider 独有的 external verifiability 检查。

---

## Minimal quality bar

- [x] the two reports are comparable enough to justify distillation
- [x] the comparison used the six fixed dimensions
- [x] each accepted candidate has an action type
- [x] each accepted candidate has a proposed repo home
- [x] at least one rejected observation is documented when relevant
- [x] the final judgment distinguishes rule gap vs trigger gap vs execution gap
