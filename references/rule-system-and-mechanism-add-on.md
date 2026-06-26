# Rule-system / Tournament-mechanism Add-on

当研究问题涉及**规则系统改变参与者激励、从而改变行为、路径优势或战术选择**时，本 add-on 在现有路由（regulatory / policy impact analysis 或 technical deep-dive / architecture analysis）基础上提供额外的输出结构要求。本 add-on 不替代现有路由的 artifact contract，而是作为附加的输出块纪律层。

> **注意：** 本 add-on 不新建路由。按内容负担选择主路由（regulatory 或 technical deep-dive），再根据本节的启用条件决定是否激活 add-on。

## 启用条件

当研究问题满足以下**任意一条**时启用本 add-on：

- 规则、赛制、政策、排序机制、奖励机制的设计和影响是核心分析对象
- 参与者可根据规则改变行为（激励扭曲、策略选择、博弈均衡偏移）
- 需要解释策略状态分类、路径优势、信息优势、公平性或激励扭曲
- 研究涉及赛制架构比较、规则改革方案评估、机制设计分析

**典型场景（非穷举）：**
- 赛制规则对球队/选手行为的影响分析
- 监管政策如何改变市场主体激励
- 拍卖/排序/配额机制的设计评估
- 激励方案（薪酬、补贴、税收）对参与者行为的影响
- 信息不对称下的策略选择分析

**不启用的情况：**
- 规则仅作为背景上下文（如合规要求清单），不做机制分析
- 纯粹的赛事结果预测（走 constrained choice 路由）
- 纯粹的规则文本解读，不涉及行为影响

## 与现有路由的关系

### 作为 regulatory / policy impact analysis 的 add-on

当核心问题是**规则影响和政策建议**时，主路由为 `regulatory-analysis`。本 add-on 在 regulatory artifact contract 基础上增加：

- **State taxonomy**（§状态分类）：补充 regulatory 现有 scenario analysis，用有限状态描述参与者在规则下的不同处境
- **Intervention matrix**（§干预矩阵）：补充 regulatory 现有 business/industry implications，以表格化格式列出规则调整方案

regulatory route 的以下现有输出块**已经覆盖**本 add-on 的部分目标，无需重复：

| Add-on 目标 | 已由 regulatory route 覆盖 |
|------------|--------------------------|
| Rule snapshot | Current regulatory snapshot + Pending legislation |
| Metric framework | Quantitative role labeling |
| Scenario/sensitivity | Scenario analysis (optimistic/base/pessimistic) |
| Monitoring signals | Monitoring signals: what to watch |
| Decision flow | 部分由 core mechanism analysis 覆盖 |

### 作为 technical deep-dive 的 add-on

当核心问题是**赛制/信息结构/机制原理**时，主路由为 `technical-deep-dive`。本 add-on 在 technical artifact contract 基础上增加：

- **State taxonomy**（§状态分类）：将 technical deep-dive 的 "core mechanism" 细化为参与者状态机
- **Intervention matrix**（§干预矩阵）：将 "comparison with alternatives" 细化为规则调整方案的对照表

technical deep-dive route 的以下现有输出块**已经覆盖**本 add-on 的部分目标：

| Add-on 目标 | 已由 technical deep-dive 覆盖 |
|------------|------------------------------|
| Rule snapshot / current mechanism | Core mechanism + key components |
| Decision flow | Core mechanism + fundamental constraints |
| Metric framework | Quantitative role labeling |
| Scenario/sensitivity | 作为 comparison with alternatives 的一部分 |

## 必备输出块

以下为本 add-on 激活时必须在报告中出现的输出块。标注「新增」的块是现有规则体系未充分覆盖的部分。

### 规则快照 (Rule snapshot) — 由现有路由覆盖

当前规则状态的快照应在主路由的 artifact contract 中满足：

- 对于 regulatory route：已在 "Current regulatory snapshot" 中要求
- 对于 technical deep-dive route：已在 "core mechanism, key components" 中要求

本 add-on 确保快照包含：当前生效规则、待变更/建议规则、官方来源与日期、规则生效时间线。

### 状态分类 (State taxonomy) — **新增**

用有限状态分类参与者处境。不使用泛泛的"有利/不利"，而是可操作的状态标签。

**模板：**

| 状态 | 描述 | 可用策略空间 | 信息条件 | 可选动作 | 典型示例 |
|------|------|-------------|----------|----------|----------|
| STATE_A | 处境定义 | 策略约束 | 信息集描述 | 可选路径 | 具体实例 |
| STATE_B | ... | ... | ... | ... | ... |

**要求：**
- 状态定义必须完整覆盖分析范围内的所有参与者处境
- 每个状态说明：参与者能做什么、不能做什么、知道什么、不知道什么
- 至少区分 3-5 种状态，不宜过少（过于粗糙）也不宜过多（失去分类价值）
- 状态标签应可观测（能用指标/数据验证参与者处于该状态），而非纯主观判断

### 决策流程 (Decision flow) — 由现有路由覆盖

决策流程（规则 → 信息集 → 可选策略 → 结果风险）的呈现由主路由的 artifact contract 覆盖：

- regulatory route：enforcement reality + business impact analysis
- technical deep-dive route：core mechanism + fundamental constraints

本 add-on 建议使用表格或简洁列表呈现，不强制要求 Mermaid 图表（与 issue 的非目标一致：不要求所有 regulatory report 都画 Mermaid）。

### 指标框架 (Metric framework) — 由现有规则覆盖

如何观察行为改变的指标框架已由 `references/quantitative-role-labeling.md` 覆盖。本 add-on 确保：

- 所有可观测指标标记数字角色（observed / proxy / assumption / model-output）
- 指标选择与状态分类中的状态定义对应（每个状态至少有一个可观测指标）
- 不将未执行模拟的假设数据表述为实证结果

### 干预矩阵 (Intervention matrix) — **新增**

列出可选规则调整方案，评估其效果、副作用和实施可行性。这是本 add-on 区别于纯 regulatory analysis（侧重现有规则影响）和纯 technical deep-dive（侧重机制解释）的关键输出块。

**模板：**

| 规则调整 | 预期改善 | 副作用/意外后果 | 实施难度 | 需监测指标 | 反转条件 |
|----------|----------|-----------------|----------|-----------|----------|
| 方案 A | 具体改善 | 可能的负面影响 | 高/中/低 + 原因 | 定量或定性指标 | 什么情况下方案失效 |
| 方案 B | ... | ... | ... | ... | ... |

**要求：**
- 至少列出 2 个可比较的调整方案（不是只有一个选项 + "维持现状"）
- 副作用必须具体，不能只写"可能有意想不到的后果"
- 实施难度需有依据（制度障碍、时间成本、政治可行性等）
- 监测指标必须可落地（threshold / cadence / source / trigger-to-action），见 §监测信号
- 反转条件必须具体可验证

### 情景/敏感性表 (Scenario / sensitivity table) — 由现有路由覆盖

情景分析由主路由覆盖：
- regulatory route：optimistic / base / pessimistic scenarios（已强制要求）
- technical deep-dive route：conditional recommendation with reversal criteria

本 add-on 确保对高敏变量列出 tipping point（阈值），即变量变化到什么程度会导致结论反转。

### 监测信号 (Monitoring signals) — 由现有路由覆盖

监测信号由 regulatory route 的 "Monitoring signals" 要求覆盖。本 add-on 确保信号具备：

| 监测目标 | 指标 | 阈值 | 频率 | 数据来源 | 触发动作 |
|----------|------|------|------|----------|----------|
| 具体监测目标 | 可量化的度量 | 触发数值/区间 | 检查频率 | 数据获取方式 | 触发后的行动 |

**要求：**
- 每个信号必须包含上述 6 个字段
- 不能只写模糊的"关注比赛数据"或"监测市场变化"
- 触发动作必须是可操作的，而非"进一步分析"

## 与 simulation contract 的关系

**关键约束：** 当报告包含模型/模拟结果（如 Monte Carlo、Poisson 模型、Elo 评分、回归分析等）时，必须服从 `references/model-output-and-simulation-discipline.md` 的 model-output contract。本 add-on 中的指标框架和情景分析不能变成伪精确生成器——所有模拟声明必须标注 status（conceptual / executed / illustrative），未执行的模拟不得以实证口吻呈现。

特别地：
- 干预矩阵中的"预期改善"若涉及定量估计，必须标注 estimation method 和 confidence
- 状态分类中的概率/倾向若来源于模拟，必须区分 observed frequency 与 modelled probability
- 不得在本 add-on 的框架下用 Monte Carlo / Elo 等未经执行和验证的模拟结果冒充实证

## 相关 references

- `references/regulatory-analysis-discipline.md` — 当主路由为 regulatory 时（如该文件存在；否则参考 ROUTING-MATRIX.md §Regulatory / Policy Impact Analysis）
- `references/technical-analysis-discipline.md` — 当主路由为 technical deep-dive 时，特别是 §Security deep-dive 和 §Control-plane add-on 的 add-on 激活模式
- `references/model-output-and-simulation-discipline.md` — 所有模拟/模型输出必须服从的合约
- `references/quantitative-role-labeling.md` — 数字角色标注（指标框架的基础纪律）
- `references/source-traceability-and-claim-citation.md` — 来源追溯（规则快照和官方来源必须满足）
- `references/counter-evidence.md` — 在规则影响分析中寻找反证（激励扭曲可能有意想不到的效果）
- `checklists/regulatory-analysis-audit.md` §Rule-system analysis — 本 add-on 的审计检查项
- `checklists/technical-analysis-audit.md` §Rule-system analysis — 技术分析路由下的审计检查项

## 非目标

- 不为足球或任何具体体育项目建立特殊路由
- 不要求所有 regulatory 或 technical deep-dive 报告都画 Mermaid 图表
- 不替代 source-traceability、numeric role labeling、simulation contract 等现有基础纪律
- 不适用于纯赛事结果预测（走 constrained choice 路由）
- 不适用于规则仅作为背景上下文的研究（不激活本 add-on）
