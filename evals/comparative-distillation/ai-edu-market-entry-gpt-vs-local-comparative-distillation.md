# AI Education Market Entry GPT-vs-Local Comparative Distillation

> **目的：** 将 GPT 深度研究版与本地 deep-research-skill 版对中国 AI 教育产品出海第一站选择的 paired-report 对比固化为回归资产，识别 market-entry 路线中敏感性分析、短名单边界和路线交叉纪律的差距。

---

## Case identity

- **Case name:** AI education market entry GPT-vs-local comparative distillation
- **Date:** 2026-06-18
- **Research question:** 中国 AI 教育产品出海第一站选哪里？
- **Why this comparison matters:**
  - 两组报告面对同一 market-entry 决策问题，GPT 版在区域→国家两级漏斗、国家尽调卡、出海水域法律/税务/IP 方面有结构优势。
  - 本地版在 route activation 和 sourcing 纪律上更严格，但在敏感性分析、secondary constrained-choice 验证和短名单边界方面有缺口。
  - 本对比验证 #328（两级漏斗与国家尽调卡）和现有 template 是否已充分吸收 GPT 结构优势。
- **Report A:** GPT 深度研究版 `中国 AI 教育产品出海第一站选择.md`
- **Report B:** 本地 deep-research-skill 版（同一 prompt，对比报告）
- **Reference / stronger report (if any):** GPT 版（结构面——地区漏斗和尽调卡更强），本地版（纪律面——sourcing 和 route activation 更强）
- **Prompt(s):** 中国 AI 教育产品公司出海第一站选哪个国家？需输出结构化 market-entry 决策备忘录。
- **Important scope or timing differences:**
  - 两份报告均基于 2026 年初数据，时间窗口一致
  - 对比焦点在结构性差异，尤其是决策框架的完整性和纪律执行

---

## Comparison purpose

This comparison is for:

1. 识别 market-entry 路线中敏感性分析和短名单边界纪律的 gap
2. 验证 #328 实施后是否已覆盖 GPT 的区域→国家两级漏斗和尽调卡结构
3. 确认 market-entry × constrained-choice 路线交叉的纪律要求是否被独立验证
4. 将 paired-report 基线固化为将来 regression 资产

---

## Dimension 1: Current-state discipline

### Report A (GPT)
- 给出了区域→国家列表和市场基础数据（人口、GDP、教育市场大小、互联网渗透率）
- 引用来源主要为 industry report 和新闻媒体，正文无 `[Sxx]`
- 数据无 role label，读者无法区分 observed vs estimate

### Report B (Local)
- 当前 template 要求 market snapshot 和 source register
- 但 body-level 引用有时缺失，尤其在市场估算部分
- 部分市场数据源未标注 access date

### Gap
- 差距主要是执行问题：当前规则要求 source register 和 body citation，但 agent 在市场数据密集型报告中执行不完整
- GPT 版同有此类问题但更严重

### Candidate action
- 强化 market-entry 报告中市场估算数据的 body-level `${[Sxx]}` 执行
- 要求每个市场估算数字标注 source role（observed/proxy/estimate）

### Action type
- `CHECKLIST_HARDENING`

---

## Dimension 2: Numerical and date discipline

### Report A (GPT)
- 市场大小、CAGR、ARPU、教育人口等数字密集
- 无 role label，读者无法区分 observed vs estimate vs assumption
- 部分数字无来源或来源不可追

### Report B (Local)
- 当前定量角色规则要求 numeric role labeling 但 market-entry 场景执行较弱
- 评分表和加权比较缺少 role 列

### Gap
- 执行问题：规则已存在但 agent 未在 market-entry 比较表上激活数字角色标签
- 同时存在 self-assessment 声称通过但实际缺失的情况

### Candidate action
- 无新规则。确保 market-entry route 自动触发 numeric role labeling checklist

### Action type
- `NO_ACTION`

---

## Dimension 3: Source traceability and evidence weighting

### Report A (GPT)
- 正文零 `[Sxx]`，仅文末 bibliography
- Industry report 和政府数据未与新闻媒体区分证据权重

### Report B (Local)
- 有 source register 结构但执行不完整
- 部分 claim 无正文引用

### Gap
- 差距同 Dimension 1：执行问题而非规则缺失

### Candidate action
- 无新规则

### Action type
- `NO_ACTION`

---

## Dimension 4: Forward-looking claim discipline

### Report A (GPT)
- 市场预测（增长率、渗透率）数字精确但无概率或 scenario 绑定
- "2027 年达到 X 亿"等 forward-looking 数字未区 observed/scenario/estimate

### Report B (Local)
- 当前 forward-looking claims checklist 要求概率/场景标签
- market-entry 预测通常偏 short-to-medium term，敏感性要求比 market-outlook 更急迫

### Gap
- market-entry 推荐依赖多个预测变量（增长率、ARPU、监管时间线、本地化成本），但这些未经敏感性测试
- 如果某个前提不成立，推荐是否会变？GPT 版也未做

### Candidate action
- 在 market-entry final audit 中增加 sensitivity 检查：每个 load-bearing estimated variable 应测试"如果变化 X%，推荐是否改变"

### Action type
- `NEW_RULE`

---

## Dimension 5: Structural readability and information density

### Report A (GPT)
- 区域→国家两级漏斗：先选区域（SE Asia / Japan / Middle East / Korea），再评国家
- 有国家 diligence card（教育市场、语言/文化、监管/合规、本地化竞争、合作伙伴可用性）
- 同时涉及法律、税务、IP 和扩展/退出策略

### Report B (Local)
- #328 已增加 two-level decision funnel、Country Diligence Card、constraint-consistency 结构
- 这些更新已覆盖 GPT 的区域→国家漏斗和 diligence card 优点

### Gap
- #328 覆盖后结构面差距已大幅缩小
- 剩余差距为：短名单边界未论证（why these 4 markets and not EU/LATAM/India）

### Candidate action
- 在 market-entry 模板中增加短名单边界论证要求：列出被排除市场和排除理由

### Action type
- `CHECKLIST_HARDENING`

---

## Dimension 6: Decision usefulness

### Report A (GPT)
- 推荐结论清晰但无排名逆转条件
- 法律/税务/IP 部分实质是约束条件而非决策变量

### Report B (Local)
- 当前 option-selection 模板要求 ranking-reversal conditions、评分规则、worked examples
- market-entry 执行可见 GO/Pilot/Not Now 框架和排序

### Gap
- 评分/加权方法不透明：star rating 和 composite score 无评分规则、权重或 worked example
- 这是执行问题——规则已存在但未在 market-entry 场景贯彻

### Candidate action
- 无新规则；强化 market-entry 场景的评分透明性执行

### Action type
- `NO_ACTION`

---

## Candidate-action summary

| # | Candidate action | Failure family | Action type | Proposed home |
|---|---|---|---|---|
| 1 | 强化 market-entry 市场估算数字的 body-level `${[Sxx]}` 和 role label | current-state / source-traceability | `CHECKLIST_HARDENING` | `checklists/option-selection-final-audit.md` |
| 2 | 增加 sensitivity 检查：load-bearing estimated variable 应测试逆转条件 | decision-utility / sensitivity-gap | `NEW_RULE` | `checklists/option-selection-final-audit.md` |
| 3 | 增加短名单边界论证：列出排除市场和理由 | scope-completeness | `CHECKLIST_HARDENING` | `references/decision-report-template.md` |

---

## Triage notes

### Candidate 1: market-entry data traceability
- **Why it matters:** market-entry 报告依赖大量估算数据（市场大小、CAGR、ARPU），无 role label 时读者无法判断哪些是 observed 事实、哪些是 estimate。
- **Why it is reusable:** 适用于所有含市场估算的报告类型（market-outlook、provider-selection）。
- **Why this home is best:** option-selection-final-audit 已包含市场数据检查，追加 role label 要求自然。
- **Promotion status:** `PROMOTE_NOW`

### Candidate 2: sensitivity analysis for market-entry
- **Why it matters:** market-entry 推荐依赖多个预测变量。不测试"哪个假设变化会改变推荐"则决策不完整。
- **Why it is reusable:** 适用于所有含 estimated variable 的决策报告。
- **Why this home is best:** option-selection-final-audit 是决策报告的最终审核点。
- **Promotion status:** `PROMOTE_NOW`

### Candidate 3: shortlist boundary justification
- **Why it matters:** 不说明为什么选这些市场、排除哪些，推荐范围无法审计。
- **Why it is reusable:** 适用于所有 constrained-choice / market-entry 场景。
- **Why this home is best:** decision-report-template 是模板层面的改动。
- **Promotion status:** `PROMOTE_NOW`

---

## Things explicitly rejected

| Observation | Why rejected |
|---|---|
| GPT 版的两级区域→国家漏斗 | #328 已覆盖，不重复推广 |
| GPT 版的 Country Diligence Card | #328 已覆盖，不重复推广 |
| GPT 版的法律/税务/IP 部分 | 属于国家尽调卡自然内容，不需要独立规则 |
| GPT 版的文末 bibliography 替代正文 `[Sxx]` | 不符合 source traceability 纪律，不接受 |

---

## Final judgment

### What the stronger report did better
- GPT 版在区域→国家两级漏斗和国家 diligence card 上更强（#328 已吸收）
- 在出海水域的法律/税务/IP 覆盖更全面（属 diligence card 内容）

### What should change in the repo now
- option-selection-final-audit.md 增加敏感性检查（load-bearing estimated variable 逆转条件）
- 同上文件增加市场估算数字 traceability + role label 强化
- decision-report-template.md 增加短名单边界论证要求

### What should wait for another confirming case
- Sensitivity analysis 作为 market-entry 决策完整性要求已足够独立确认，不需要再等

### Is this mainly a missing rule, missing trigger, or execution problem?
- 混合型：
  - Sensitivity analysis 是 **missing rule**（当前系统没有要求 load-bearing estimate 的逆转条件测试）
  - Data traceability 和 shortlist boundary 是 **execution problem**（规则已存在但执行不完整）
  - 两级漏斗和 diligence card 已被 #328 覆盖

---

## Minimal quality bar

- [x] the two reports are comparable enough to justify distillation
- [x] the comparison used the six fixed dimensions
- [x] each accepted candidate has an action type
- [x] each accepted candidate has a proposed repo home
- [x] at least one rejected observation is documented when relevant
- [x] the final judgment distinguishes rule gap vs trigger gap vs execution gap
