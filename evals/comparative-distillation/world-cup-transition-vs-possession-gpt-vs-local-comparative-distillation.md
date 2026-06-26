# World Cup Transition Attack vs Possession Control GPT-vs-Local Comparative Distillation

> **目的：** 将 GPT 深度研究版与本地 deep-research-skill 版对世界杯战术问题（transition vs possession）的 paired-report 对比固化为回归资产，暴露并捕获「数据不可得时的方法脚手架」模式——这是与 [#342](https://github.com/ShadyUnderLight/deep-research-skill/issues/342) 仿真合约不同的独立边缘场景。

---

## Case identity

- **Case name:** World Cup Transition Attack vs Possession Control GPT-vs-Local Comparative Distillation
- **Date:** 2026-06-24
- **Research question:** Does the 2026 World Cup format reward transition attacks more than traditional possession control?
- **Why this comparison matters:**
  - 暴露「data-unavailable method-scaffold」模式：当赛事数据确实尚不存在时，报告应该怎么做？GPT 版有虚假统计（示例表格 → p 值）和「2026 data not yet generated」这类已失效的陈旧断言。本地版有方法脚手架但没有虚假声明。
  - 该对比验证 [#342](https://github.com/ShadyUnderLight/deep-research-skill/issues/342) 的仿真合约，并识别出一个新的「data-unavailable」边缘场景。
  - GPT 版的「method scaffold」思路正确，但执行（虚假统计、陈旧事实）错误。本地版的保守做法正确，但不够有雄心。
- **Report A:** GPT 深度研究版（有度量框架，但示例表格被呈现为统计证据，含「2026 data not yet generated」陈旧断言）
- **Report B:** 本地 deep-research-skill 版（方法脚手架含占位变量，无虚假统计，但框架不如 GPT 版精细）
- **Reference / stronger report (if any):** 本地 deep-research-skill 版（保守但正确比大胆但错误好，trustworthiness 优先于 polish）
- **Prompt(s):** 相同研究问题，两份报告均使用 deep-research style
- **Important scope or timing differences:**
  - 两份报告均基于同一赛前窗口，2026 年世界杯尚未开赛
  - GPT 版生成于 GPT 深度研究界面，本地版生成于 deep-research-skill pipeline
  - 对比焦点在数据不可得时的报告纪律，而非事实检索能力

---

## Comparison purpose

This comparison is **not** for deciding which model is "better."

It is for:

1. 识别当赛事/事件数据确实不存在时，报告的正当行为边界是什么
2. 将「data-unavailable method-scaffold」模式与 [#342](https://github.com/ShadyUnderLight/deep-research-skill/issues/342) 已有的仿真合约区分开来（仿真合约覆盖「声称但未执行」的仿真；本对比覆盖「数据确实不存在」的独立场景）
3. 提取候选规则升级（R76：data-unavailable method-scaffold）
4. 将 paired-report 基线固化为将来 regression 资产

---

## Dimension 1: Current-state discipline

### Report A
- GPT 版包含「2026 data not yet generated」的陈旧断言——在 2026 年 6 月背景下，该陈述已失效（2026 年世界杯虽然尚未开赛，但抽签、赛程、场馆、资格赛结果均已确定）
- 示例表格（过渡进攻 vs 控球数据）在缺乏数据的情况下呈现为演示性内容，但过渡不清晰
- 缺乏对哪些信息已确定（赛制、参赛队、分组）和哪些确实不可得的显式区分

### Report B
- 本地版正确识别了 2026 年世界杯的赛制参数（48 队、12 组、淘汰赛路径）
- 声明了数据的实际不可得性（无 48 队赛制的历史比赛数据）
- 未做出超越已知事实的断言
- 弱点：对已确定事实（赛制规则、历史类比窗口）的显式 current-state snapshot 不如预期完整

### Gap
- GPT 版的核心问题：「2026 data not yet generated」这类陈述在 current-state 纪律上是错误的——它把「数据尚未产生」当成一个正在进行的事实来陈述，而实际上在 2026 年 6 月，大量结构性数据已经存在
- 本地版在 current-state 上保守但正确，没有做出虚假的时间层断言

### Candidate action
- 当前 current-state 检查已要求 freshness 纪律（`checklists/final-audit.md`），该 gap 属于已有规则未触发（GPT 报告不在本地 pipeline 中），而非规则缺失
- 无需新增候选：current-state freshness 纪律已覆盖

### Current status
- ✅ 已由现有 checklist 覆盖：`checklists/final-audit.md` §freshness audit 要求所有时间敏感断言具有可验证的时间基准
- GPT 版不在本地 pipeline 中运行，但其失败模式（陈旧断言未被 freshness 检查拦截）验证了该检查的必要性

### Eval regression assets
- `evals/cases/world-cup-transition-vs-possession-method-scaffold-case.md` — 综合 eval 覆盖 current-state freshness 检查

### Action type
`NO_ACTION`

---

## Dimension 2: Numerical and date discipline

### Report A
- GPT 版构建了一个度量框架（过渡进攻效率、控球转化率、反击成功率等指标），这种「方法脚手架」的思路在数据不可得时是正确的
- **严重问题：** 示例表格被呈现为统计证据——包含数值和 p 值，但数据源不存在
- 将演示性的框架误用为事实性输出，跨越了「方法说明」和「虚假统计」的界限

### Report B
- 本地版声明了占位变量（如 `Δ_possession_advantage`、`transition_efficiency_gap`）和方法论框架
- 没有虚假统计——所有数值都被显式标记为占位符
- 弱点：框架的组织不够系统化（缺少结构化的「assumption boundary」声明），但对于「数据不可得」场景而言，这是正确的保守策略

### Gap
- 核心差距：当数据确实不存在时，GPT 版选择了正确的思路（方法脚手架）但执行错误（虚假统计）——它需要一个显式的规则来约束方法脚手架的边界
- 本地版展示了正确行为但缺乏结构化指导——它需要一个显式的规则来帮助方法脚手架更有条理
- 这不是 [#342](https://github.com/ShadyUnderLight/deep-research-skill/issues/342) 的仿真合约场景（仿真合约覆盖「声称但未执行仿真」），而是「数据确实不存在，应采用方法脚手架」的独立场景

### Candidate action
- 新增候选规则 **R76**：当赛事/事件数据确实不存在时，报告必须定义显式的占位变量及假设边界（event-count、sample-size、lookback-window、known constraints），而非编造数据或 dismiss 问题
- 这超越了 [#342](https://github.com/ShadyUnderLight/deep-research-skill/issues/342) 的仿真合约（覆盖「声称但未执行」的仿真），它覆盖了「数据确实不存在，方法脚手架是纪律性方案」的独立场景

### Current status
- ⚠️ 新 gap——尚未被现有规则覆盖
- [#342](https://github.com/ShadyUnderLight/deep-research-skill/issues/342) 覆盖仿真合约（conceptual / executed / illustrative status），但「数据不存在时的方法脚手架」是不同的问题
- R76 是本次对比的核心新发现

### Eval regression assets
- `evals/cases/world-cup-transition-vs-possession-method-scaffold-case.md` — 综合 eval 覆盖 data-unavailable method-scaffold 纪律

### Action type
`CHECKLIST_HARDENING`

---

## Dimension 3: Source traceability and evidence weighting

### Report A
- GPT 版度量框架的概念来源可追溯（足球分析文献中的过渡进攻概念）
- 正文引用使用不可复核的专有格式
- 无 7 列 Source Register

### Report B
- 本地版 Source Register 注册了赛制参数的来源（FIFA 官方文档、Wikipedia）
- 对数据不可得性有显式声明
- 占位变量没有 claim-level 来源归属（因为确实没有数据来源）

### Gap
- 两份报告的 source traceability 在当前约束下（数据不可得）都是可接受的
- 本地版对数据不可得的诚实声明比 GPT 版的虚假来源归属好
- 无显著新 gap

### Candidate action
- 无需新增候选：source traceability 在数据不可得场景下表现可接受

### Current status
- ✅ 已由现有 source register 纪律覆盖：`references/report-template.md` §Source Register 要求声明数据可得性状态
- 数据不可得时的诚实声明（「无可用数据」）优于编造来源

### Eval regression assets
- `evals/cases/world-cup-transition-vs-possession-method-scaffold-case.md` — 约束 source traceability 在 data-unavailable 场景的表现

### Action type
`NO_ACTION`

---

## Dimension 4: Forward-looking claim discipline

### Report A
- GPT 版的「示例表格 + p 值」从方法脚手架滑向了虚假的确定性断言
- 将不应该有统计显著性的场景强行赋予了统计显著性
- 对「2026 data not yet generated」的陈旧断言削弱了 forward-looking 的可信度

### Report B
- 本地版使用了适当的 hedging 语言（「在数据不可得的情况下，本报告仅提供分析框架」）
- 没有做出无法验证的预测性断言
- 占位变量明确标注为「待数据填入」
- 弱点：hedging 可以更结构化（如 scenario-based hedging）

### Gap
- GPT 版犯了 forward-looking claim 的典型错误：在数据不支持时过度承诺
- 本地版在 forward-looking claim 纪律上表现正确——对「我们不知道什么」的透明度优于虚假的确定性
- [#342](https://github.com/ShadyUnderLight/deep-research-skill/issues/342) 的仿真合约部分覆盖（区分 conceptual vs executed），但本处的核心问题更基础：在数据不存在时，根本不应该产生带 p 值的 forward-looking claim

### Candidate action
- 无需新增候选：forward-looking claim 纪律已由现有规则覆盖，且 [#342](https://github.com/ShadyUnderLight/deep-research-skill/issues/342) 的仿真合约提供 model-output disclosure 保护

### Current status
- ✅ 已由现有规则覆盖：`checklists/forward-looking-claims.md` §forecast boundaries 要求声明数据支持水平
- [#342](https://github.com/ShadyUnderLight/deep-research-skill/issues/342) 的仿真合约阻止未执行的仿真被呈现为已执行

### Eval regression assets
- `evals/cases/world-cup-transition-vs-possession-method-scaffold-case.md` — 约束 forward-looking claims 在 data-unavailable 场景的边界

### Action type
`NO_ACTION`

---

## Dimension 5: Structural readability and information density

### Report A
- GPT 版度量框架的结构组织良好：过渡进攻效率、控球转化率、反击成功率、防守反击效率——四个维度构成了完整的分析框架
- 指标定义清晰（每个指标都有 operational definition）
- 弱点：框架的「脚手架」属性未声明，读者可能误认为 framework = findings

### Report B
- 本地版方法脚手架存在但组织不够系统化
- 占位变量分散在不同的分析段落中，缺乏统一的框架表格
- 弱点：可读性不如 GPT 版——读者需要自己拼凑分析框架

### Gap
- GPT 版的框架组织在结构上更强，但需要伴以显式的「scaffold status」声明
- 本地版的框架可以更结构化，但不应该以牺牲正确性为代价
- 这是一个「nice to have」的结构改进，而非跨 session 信号

### Candidate action
- 无需新增候选：结构性改进属于风格偏好，不足以构成规则升级
- 如果将来更多 data-unavailable 场景出现，可考虑 TEMPLATE_CHANGE 新增「method-scaffold 模块」

### Current status
- ℹ️ 观察中，不升级：当前模板没有 method-scaffold 专用模块，但该需求仅在一个案例中出现，不足以触发模板变更

### Eval regression assets
- `evals/cases/world-cup-transition-vs-possession-method-scaffold-case.md` — 跟踪 method-scaffold 结构的演进

### Action type
`NO_ACTION`

---

## Dimension 6: Decision usefulness

### Report A
- GPT 版的 polish 更高：度量框架完整、指标定义清晰、分析逻辑连贯
- 但由于虚假统计（p 值）和失效断言（data not yet generated），报告的整体可信度受损
- 一个包含虚假统计的报告是不值得决策者信赖的

### Report B
- 本地版的 polish 更低，但 trustworthiness 更高
- 占位变量的透明度让决策者清楚知道「哪些是已知的，哪些是未知的」
- 方法脚手架（虽然不够美化）让决策者可以在数据到来时自行填入
- 弱点：如果决策者期望的是即时可用的结论而非框架，报告可能令人失望

### Gap
- 在决策有用性上，本对比揭示了一个基本权衡：**trustworthiness > polish**
- 一个可信但粗糙的报告比一个美化但包含虚假统计的报告更有用
- 本地版在这个维度上胜出不是因为更强，而是因为更诚实

### Candidate action
- 无需新增候选：trustworthiness > polish 是已有原则（`references/report-template.md` §报告可信度优先于可读性）

### Current status
- ✅ 已由现有原则覆盖：`references/report-template.md` §报告可信度优先于可读性
- 本对比验证了该原则在 data-unavailable 场景的适用性

### Eval regression assets
- `evals/cases/world-cup-transition-vs-possession-method-scaffold-case.md` — 跟踪 decision usefulness 在 data-unavailable 场景的权衡

### Action type
`NO_ACTION`

---

## Candidate-action summary

| # | Candidate action | Failure family | Action type | Proposed home |
|---|---|---|---|---|
| 1 | R76: 当赛事/事件数据确实不存在时，报告必须定义显式的占位变量及假设边界（event-count、sample-size、lookback-window、known constraints），而非编造数据或 dismiss 问题 | numerical-discipline / data-availability | `CHECKLIST_HARDENING` | `checklists/final-audit.md` §data-unavailable method-scaffold; `checklists/numerical-discipline.md` |
| 2 | Current-state freshness — GPT 版的陈旧断言验证现有 freshness 检查的必要性 | current-state / time-layer discipline | `NO_ACTION` | Already covered by `checklists/final-audit.md` §freshness audit |
| 3 | Source traceability — 数据不可得场景下表现可接受 | source traceability | `NO_ACTION` | Already covered by `references/report-template.md` §Source Register |
| 4 | Forward-looking claim discipline — [ #342](https://github.com/ShadyUnderLight/deep-research-skill/issues/342) 仿真合约提供保护 | forward-looking claim discipline | `NO_ACTION` | Already covered by [ #342](https://github.com/ShadyUnderLight/deep-research-skill/issues/342) + `checklists/forward-looking-claims.md` |
| 5 | Framework structure — 风格偏好，不足触发模板变更 | output structure / information density | `NO_ACTION` | Observe for second case before TEMPLATE_CHANGE |
| 6 | Decision usefulness — trustworthiness > polish 验证已有原则 | decision usefulness | `NO_ACTION` | Already covered by `references/report-template.md` §报告可信度优先于可读性 |

---

## Triage notes

### Candidate 1 (R76)
- **Why it matters:** 当数据不存在时，GPT 的合理直觉（方法脚手架）在执行层崩溃为虚假统计。需要一个显式规则告诉「数据不可得」的报告可以做什么（定义占位变量和假设边界）和不可以做什么（编造数据、dismiss 问题、呈现示例表格为统计证据）。
- **Why it is reusable:** 任何「赛事尚未发生」「数据尚未发布」「疫情后数据不可比」等场景都会触发同样的困境。data-unavailable 不是世界杯特有的问题——它存在于金融预测、市场报告、技术趋势分析等多个领域。
- **Why this home is best:** `checklists/final-audit.md` 的 numerical-discipline 部分已经包含相关检查（如 R07 metric-scope audit），R76 作为一个新的检查项自然扩展这个领域。同时 `checklists/numerical-discipline.md` 是一个更专门化的落脚点。
- **Promotion status:** `PROMOTE_NOW`

---

## Things explicitly rejected

| Observation | Why rejected |
|---|---|
| GPT 的 metric framework 应被直接并入 template | 度量框架在没有配套数据的情况下并入模板会导致「空框架」漂移——模板应该引导内容生成，而非成为空壳 |
| 「2026 data not yet generated」这类 statement 需要新的 freshness 规则 | 该陈述已被 current-state freshness 检查拦截（`checklists/final-audit.md`）——不需要新规则，GPT 版不在本地 pipeline 中运行所以才漏过 |
| 本地版应被批评为「less sophisticated」并加以提升 | 保守但正确比大胆但错误好——在数据不可得场景下，trustworthiness 优先于框架复杂度。本地版不需要被改造为「更像 GPT 版」 |
| R76 应与 R75 合并为一条规则 | R75（仿真合约）覆盖「声称但未执行的仿真」，R76 覆盖「数据确实不存在时的方法脚手架」——两者是不同的问题类型，需要不同的检查项和触发条件 |

---

## Final judgment

### What the stronger report did better
- 本地版在数据不可得场景下的纪律优于 GPT 版——没有虚假统计、没有失效断言、对「不知道什么」诚实透明
- GPT 版的度量框架组织在结构上更强，但执行层错误（虚假统计）侵蚀了结构优势

### What should change in the repo now
- ✅ R76（data-unavailable method-scaffold）应作为 `CHECKLIST_HARDENING` 加入 `checklists/final-audit.md` 和/或 `checklists/numerical-discipline.md`
- 5 个维度 `NO_ACTION`——已有规则已覆盖

### What should wait for another confirming case
- 是否需要为 method-scaffold 场景新增 template 模块（TEMPLATE_CHANGE）——等第二个 data-unavailable 案例确认后升级

### Is this mainly a missing rule, missing trigger, or execution problem?
- **Data-unavailable method-scaffold (D2):** Missing rule —— 数据不可得时的方法脚手架纪律没有显式规则 → 由 R76 修复
- **Current-state freshness (D1):** Execution problem —— freshness 规则存在但 GPT 版不在本地 pipeline 中运行，无法触发
- **Forward-looking claim (D4):** 已有规则保护——[#342](https://github.com/ShadyUnderLight/deep-research-skill/issues/342) 的仿真合约部分覆盖，基础纪律已有 forward-looking claims checklist 覆盖

---

## Minimal quality bar

- [x] the two reports are comparable enough to justify distillation
- [x] the comparison used the six fixed dimensions
- [x] each accepted candidate has an action type
- [x] each accepted candidate has a proposed repo home
- [x] at least one rejected observation is documented when relevant
- [x] the final judgment distinguishes rule gap vs trigger gap vs execution gap
