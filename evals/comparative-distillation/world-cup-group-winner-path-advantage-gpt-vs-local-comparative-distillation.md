# World Cup Group Winner Path Advantage GPT-vs-Local Comparative Distillation

> **目的：** 将 GPT 深度研究版与本地 deep-research-skill 版对世界杯小组头名路径优势的 paired-report 对比固化为回归资产，暴露并捕获「跨源模型污染」（cross-source model contamination）模式——当 Wikipedia 结构性数据与外部 Elo 评级和 Monte Carlo 仿真输出在无层级分离的情况下合并时产生的问题。

---

## Case identity

- **Case name:** World Cup Group Winner Path Advantage GPT-vs-Local Comparative Distillation
- **Date:** 2026-06-24
- **Research question:** Does winning the group in a 48-team World Cup format provide a significant knockout-stage path advantage?
- **Why this comparison matters:**
  - 暴露「cross-source model contamination」模式：当 Wikipedia 结构性数据（赛制、历史）与外部来源的 Elo 评级和 Monte Carlo 仿真输出在无 source-layer 分离的情况下合并时，读者无法审计哪些主张来自可靠来源、哪些来自不可验证的模型。
  - 该对比验证 [#341](https://github.com/ShadyUnderLight/deep-research-skill/issues/341)（source strength）和 [#342](https://github.com/ShadyUnderLight/deep-research-skill/issues/342)（仿真合约），并识别出一个新的跨源分层问题。
  - GPT 版有正确框架但零执行证据；本地版有诚实限制但无框架。两者均失败——GPT 在仿真合约上，本地在 source strength + numeric roles 上。
- **Report A:** GPT 深度研究版（仿真/Elo/路径难度框架，声称 Monte Carlo 模拟 p≪0.01、Elo 1574 vs 1754，但无球队列表、无种子、无执行证据）
- **Report B:** 本地 deep-research-skill 版（仅 Wikipedia 来源，有部分历史数据，numeric roles 缺失，未尝试仿真）
- **Reference / stronger report (if any):** 两份报告均存在严重缺陷，但本地版的诚实限制（Wikipedia-only、未声称仿真）在 trustworthiness 上略优于 GPT 版的未执行仿真声称
- **Prompt(s):** 相同研究问题，两份报告均使用 deep-research style
- **Important scope or timing differences:**
  - 两份报告均基于同一赛前窗口，2026 年 48 队赛制的数据基础相同
  - GPT 版组合了 Wikipedia 结构数据 + 外部 Elo 评级 + 声称的 Monte Carlo 仿真
  - 本地版仅使用 Wikipedia 作为数据源，无外部模型数据
  - 对比焦点在 source-layer 分离纪律和仿真执行证据，而非事实检索能力

---

## Comparison purpose

This comparison is **not** for deciding which model is "better."

It is for:

1. 识别当结构性数据（Wikipedia）与外部定量模型（Elo、Monte Carlo）合并时，source-layer 分离的必要性——这是 [#341](https://github.com/ShadyUnderLight/deep-research-skill/issues/341) 未覆盖的新 gap
2. 确认 [#342](https://github.com/ShadyUnderLight/deep-research-skill/issues/342) 仿真合约对「声称但未执行」的仿真的拦截力度
3. 验证已在等待中的 R75（p-value/Elo/Monte Carlo 无执行证据触发 validator warning）是否需要升级
4. 将 paired-report 基线固化为将来 regression 资产

---

## Dimension 1: Current-state discipline

### Report A
- GPT 版对 2026 年世界杯的 48 队赛制描述正确（12 组 × 4 队、小组前二 + 8 个最佳第三名晋级）
- 淘汰赛路径结构（32 强 → 16 强 → 四分之一决赛 → 半决赛 → 决赛）描述准确
- 对小组头名 vs 小组第二在淘汰赛中的对阵路径有清晰分析
- 弱点：部分淘汰赛路径细节（如特定小组头名 vs 特定第三名对阵）在赛制尚未完全确定时可能为推测

### Report B
- 本地版对 2026 年世界杯赛制的基本参数描述准确（48 队、12 组）
- 引用了 FIFA 官方赛制公告和 Wikipedia 结构数据
- 弱点：对淘汰赛路径的分析不如 GPT 版精细，缺乏对阵路径的显式映射

### Gap
- 两份报告在 current-state（赛制参数）上表现均可接受
- GPT 版对淘汰赛路径的分析更精细，但部分细节在赛制尚未完全确定时存在推测风险
- 本地版更保守，但覆盖的 depth 不如 GPT 版

### Candidate action
- 无需新增候选：赛制参数的 current-state 纪律在可接受范围内

### Current status
- ✅ 已由现有规则覆盖：`checklists/final-audit.md` §current-state snapshot 要求声明已确认 vs 推测的事实
- 赛制参数类问题在 current-state discipline 上无显著新 gap

### Eval regression assets
- `evals/cases/world-cup-group-winner-simulation-contract-case.md` — 综合 eval 覆盖 current-state 纪律

### Action type
`NO_ACTION`

---

## Dimension 2: Numerical and date discipline

### Report A
- GPT 版声称 Monte Carlo 仿真输出 p≪0.01、Elo 评级 1574 vs 1754——这些数值以统计结论的形式呈现
- **严重问题：零执行证据。** 无球队列表、无仿真种子、无迭代次数、无 Elo 评级来源——这些数值无法复现、无法审计
- 另一个问题：Wikipedia 的结构性数据（赛制）和外部 Elo 评级/仿真输出被混合在同一个「分析」中，缺乏 source-layer 分离

### Report B
- 本地版仅使用 Wikipedia 作为数据源，包含部分历史数据（往届世界杯小组头名 vs 小组第二的淘汰赛表现）
- 弱点是 numeric roles 缺失——历史数据未标注为 observed/proxy，没有定量分析框架
- 没有虚假仿真——因为根本没有尝试仿真，诚实声明了局限性

### Gap
- 核心差距 1（仿真合约）：GPT 版声称 p 值/仿真但无执行证据——这是 [#342](https://github.com/ShadyUnderLight/deep-research-skill/issues/342) 的仿真合约已覆盖的问题，R75 已有 `WAIT_FOR_SECOND_CASE` 状态
- **核心差距 2（跨源模型污染——新发现）：** 当 Wikipedia 结构数据和外部 Elo 评级被呈现在单一的「分析」中且无 source-layer 分离时，读者无法区分哪些主张来自可验证的结构性事实、哪些来自不可验证的外部模型。这是一个 [#341](https://github.com/ShadyUnderLight/deep-research-skill/issues/341) 未覆盖的新 gap——#341 覆盖 per-source 的强度分级，但不覆盖跨源层级分离
- 核心差距 3（numeric roles）：本地版缺失 numeric role 标签——已有规则未触发

### Candidate action
- 新增候选规则 **R77**：当结合众包结构性数据（如 Wikipedia 赛制/历史）与外部来源的定量模型（如 Elo 评级、Monte Carlo 仿真）时，报告必须在 Source Register 中分离数据层，为每层声明显式的 provenance。单一 source-type 的 register 在数据来自根本不同可靠性层级时是不够的
- R75 当前状态为 `WAIT_FOR_SECOND_CASE`——本对比是第二个确认案例，但不在此对比中升级（等 [#342](https://github.com/ShadyUnderLight/deep-research-skill/issues/342) validator 运行更多案例后自然升级）

### Current status
- ⚠️ 新 gap（cross-source model contamination）——未被现有规则覆盖
- [#341](https://github.com/ShadyUnderLight/deep-research-skill/issues/341)（source strength）覆盖 per-source 的强度分级，但不要求跨源层级分离
- [#342](https://github.com/ShadyUnderLight/deep-research-skill/issues/342)（仿真合约）覆盖仿真执行证据，但不覆盖结构性数据与模型数据的混合
- R77 是本次对比的核心新发现

### Eval regression assets
- `evals/cases/world-cup-group-winner-simulation-contract-case.md` — 综合 eval 覆盖 cross-source model contamination + 仿真合约

### Action type
`CHECKLIST_HARDENING`

---

## Dimension 3: Source traceability and evidence weighting

### Report A
- GPT 版正文有度量框架和数值但缺乏 claim-level 来源归属
- 无 7 列 Source Register——外部 Elo 评级和仿真输出没有 provenance
- Wikipedia 结构数据和外部模型数据在正文中混合呈现，无层级区分

### Report B
- 本地版 Wikipedia-only 来源——source traceability 诚实但狭窄
- 部分历史数据有来源（Wikipedia 赛果页面）
- 弱点：Wikipedia-only 限制了 source strength——缺少 primary source（FIFA 官方数据）和 statistical source（Elo 数据库）

### Gap
- GPT 版的核心问题：外部 Elo 评级和 Monte Carlo 仿真的 provenance 缺失
- 本地版的核心问题：source strength 不足（Wikipedia-only）——这已被 [#341](https://github.com/ShadyUnderLight/deep-research-skill/issues/341) 覆盖
- 跨源模型污染（Dimension 2 中已识别）在 source traceability 维度也有体现：Source Register 需要反映数据层级

### Candidate action
- 本地版的 source strength gap 已被 [#341](https://github.com/ShadyUnderLight/deep-research-skill/issues/341) 覆盖——NO_ACTION
- 跨源层级分离的需求已作为 R77 在 Dimension 2 中提出——不在此维度重复

### Current status
- ✅ 部分已覆盖，部分由 R77 处理
- [#341](https://github.com/ShadyUnderLight/deep-research-skill/issues/341) 覆盖 source strength per-source 分级
- R77（Dimension 2）覆盖跨源层级分离

### Eval regression assets
- `evals/cases/world-cup-group-winner-simulation-contract-case.md` — 约束 source traceability 和跨源分层

### Action type
`NO_ACTION`

---

## Dimension 4: Forward-looking claim discipline

### Report A
- GPT 版声称 Monte Carlo 仿真结果（p≪0.01 → 小组头名有显著路径优势）但没有仿真执行证据
- 将未执行的仿真输出呈现为确定性结论，违反了 forward-looking claim 的基本纪律
- Elo 评级（1574 vs 1754）的差异被用作仿真输入，但 Elo 数据的来源和计算方式不可审计

### Report B
- 本地版没有做出无法验证的预测性断言——诚实承认局限性
- 部分历史数据（往届世界杯小组头名 vs 小组第二的淘汰赛表现）可以作为 forward-looking 的参考，但未以预测框架组织
- 弱点：对有数据支持的 forward-looking 分析可以更主动（如基于历史数据的路径优势趋势分析）

### Gap
- GPT 版在 forward-looking claim 上犯了严重错误：将未执行的仿真呈现为已执行的仿真结果
- 这是 [#342](https://github.com/ShadyUnderLight/deep-research-skill/issues/342) 仿真合约直接覆盖的场景——R75 的 WAIT_FOR_SECOND_CASE 状态得到本对比的第二次确认

### Candidate action
- R75 已由本对比得到第二次确认（simulation p-values without execution evidence 触发 validator warning）
- 不在此对比中升级 R75——等 [#342](https://github.com/ShadyUnderLight/deep-research-skill/issues/342) validator 运行更多案例后自然升级

### Current status
- ⚠️ R75 得到了第二个确认案例，但保持 `WAIT_FOR_SECOND_CASE` 状态
- 升级时机由 [#342](https://github.com/ShadyUnderLight/deep-research-skill/issues/342) validator 决定，不在本对比中单独升级

### Eval regression assets
- `evals/cases/world-cup-group-winner-simulation-contract-case.md` — 约束 forward-looking claims（仿真合约纪律）

### Action type
`NO_ACTION`

---

## Dimension 5: Structural readability and information density

### Report A
- GPT 版仿真/Elo/路径难度的分析框架在结构上组织良好
- 淘汰赛路径的映射（小组头名 vs 小组第二 vs 第三名的对阵路径）在结构上清晰
- 弱点：框架的「仿真」属性未声明——读者可能认为 framework = executed analysis

### Report B
- 本地版 Wikipedia-only 来源，结构上缺乏分析框架——报告更像是信息汇总而非分析
- 没有路径难度映射、没有定量比较框架
- 弱点：结构性不足——读者拿到的是数据，而非分析

### Gap
- GPT 版在框架结构上更强，但结构优势被仿真执行证据的缺失所侵蚀
- 本地版在结构上较弱，但这是 conservative approach 的副产品（宁可没有框架也不编造框架）
- 没有需要升级的新结构性 gap

### Candidate action
- 无需新增候选：GPT 版的框架结构不应被采纳为 template（无复算证据）；本地版的结构不足属于 source strength 问题，已由 [#341](https://github.com/ShadyUnderLight/deep-research-skill/issues/341) 覆盖

### Current status
- ℹ️ 观察中：GPT 的框架结构不应被采纳——没有仿真执行证据的框架是空壳
- 本地版的结构不足是「没有足够优质数据就无法构建框架」的正确行为——不应被惩罚

### Eval regression assets
- `evals/cases/world-cup-group-winner-simulation-contract-case.md` — 跟踪结构 vs 执行的权衡

### Action type
`NO_ACTION`

---

## Dimension 6: Decision usefulness

### Report A
- GPT 版声称的仿真结论（小组头名有显著路径优势）如果真实，将非常有决策价值
- 但由于仿真执行证据缺失，结论不可信——读者无法区分这是真实分析还是模型幻觉
- p≪0.01 的呈现方式暗示了虚假的确定性

### Report B
- 本地版诚实限制了报告在决策上的用处——Wikipedia-only 的历史数据不足以支持强有力的路径优势结论
- 但至少读者知道「这里的数据不支持强结论」——这是一个决策上有用的信号
- 弱点：在决策有用性上太保守，可能在数据确实存在时仍然不敢做出结论

### Gap
- 两份报告在决策有用性上都存在重大缺陷
- GPT 版：不可信（仿真无执行证据）→ 不能用于决策
- 本地版：不够有力（数据不足）→ 不足以支持决策
- 本对比确认：当数据不充分时，「诚实的不确定性」优于「虚假的确定性」

### Candidate action
- 无需新增候选：decision usefulness 在数据不足场景下的天然限制已被现有原则覆盖

### Current status
- ✅ 已由现有原则覆盖：`references/report-template.md` §报告可信度优先于可读性
- 本对比验证了该原则在仿真合约和 cross-source contamination 场景下的适用性

### Eval regression assets
- `evals/cases/world-cup-group-winner-simulation-contract-case.md` — 跟踪 decision usefulness 的 trustworthiness 权衡

### Action type
`NO_ACTION`

---

## Candidate-action summary

| # | Candidate action | Failure family | Action type | Proposed home |
|---|---|---|---|---|
| 1 | R77: 当结合众包结构性数据（Wikipedia 赛制/历史）与外部定量模型（Elo、Monte Carlo）时，必须在 Source Register 中分离数据层，为每层声明显式 provenance | source traceability / evidence weighting | `CHECKLIST_HARDENING` | `checklists/final-audit.md` §source layer separation; `references/report-template.md` §Source Register |
| 2 | R75: Simulation p-values/CI/Elo without execution evidence → validator warning | numerical-discipline / simulation contract | `NO_ACTION` | R75 already `WAIT_FOR_SECOND_CASE` via [#342](https://github.com/ShadyUnderLight/deep-research-skill/issues/342); second case confirmed here |
| 3 | Current-state discipline — 赛制参数场景下表现可接受 | current-state / time-layer discipline | `NO_ACTION` | Already covered by `checklists/final-audit.md` §current-state snapshot |
| 4 | Source traceability (Wikipedia-only) — [ #341](https://github.com/ShadyUnderLight/deep-research-skill/issues/341) 覆盖 per-source 强度分级 | source traceability | `NO_ACTION` | Already covered by [ #341](https://github.com/ShadyUnderLight/deep-research-skill/issues/341) |
| 5 | Forward-looking claims — [ #342](https://github.com/ShadyUnderLight/deep-research-skill/issues/342) 仿真合约覆盖 | forward-looking claim discipline | `NO_ACTION` | Already covered by [ #342](https://github.com/ShadyUnderLight/deep-research-skill/issues/342) |
| 6 | Structural framework — GPT 框架不应被采纳 | output structure / information density | `NO_ACTION` | No execution evidence = framework is hollow shell |
| 7 | Decision usefulness — trustworthiness > polish 验证 | decision usefulness | `NO_ACTION` | Already covered by `references/report-template.md` §报告可信度优先于可读性 |

---

## Triage notes

### Candidate 1 (R77)
- **Why it matters:** 当 Wikipedia 的结构数据和外部 Elo 评级被混合在一个「分析」中时，读者收到的是一份「平权」的报告——所有数据看起来同等可靠。但实际上，Wikipedia 赛制参数是高度可验证的结构性事实，而外部 Elo 评级和 Monte Carlo 仿真可能包含未声明的假设、过时的数据或错误的实现。Source-layer 分离是让读者恢复审计能力的唯一方式。
- **Why it is reusable:** 任何涉及「众包结构数据 + 外部定量模型」的场景都会触发同样的困境：体育分析（Wikipedia + Elo）、金融分析（公司基本面 + DCF 模型）、市场研究（行业数据库 + 预测模型）。这不是世界杯特有的问题。
- **Why this home is best:** `checklists/final-audit.md` 的 Source Register 部分已有 per-source 强度检查（来自 [#341](https://github.com/ShadyUnderLight/deep-research-skill/issues/341)），R77 作为跨源层级分离检查自然扩展这个领域。`references/report-template.md` 的 Source Register 格式可以从单层表格升级为支持 source-layer 的多层表格。
- **Promotion status:** `PROMOTE_NOW`

### Candidate 2 (R75)
- **Why it matters:** R75 要求 p 值/CI/Elo/Poisson/Monte Carlo 无执行证据时触发 validator warning。本对比是 R75 的第二个确认案例——GPT 版的 p≪0.01 和 Elo 1574 vs 1754 是 R75 直接覆盖的失败模式。
- **Why it should stay WAIT_FOR_SECOND_CASE:** R75 已经有了第二个案例确认，但升级决策应由 [#342](https://github.com/ShadyUnderLight/deep-research-skill/issues/342) 的 validator 在实际运行后做出——validator 的运行结果比案例数量更重要。
- **Why this home is best:** `scripts/validate_simulation_claims.py`（已由 [#342](https://github.com/ShadyUnderLight/deep-research-skill/issues/342) 创建）
- **Promotion status:** `WAIT_FOR_SECOND_CASE`

---

## Things explicitly rejected

| Observation | Why rejected |
|---|---|
| GPT 的 Elo/Monte Carlo 框架应被采纳为 template | 零复算证据——框架在没有执行证据的情况下是空壳。采纳框架而不要求执行证据会鼓励「仿真空壳」报告 |
| 本地版应被废弃（Wikipedia-only 太弱） | 诚实限制比虚假声称好——Wikipedia-only 至少告诉读者「信息边界在此」。废弃本地版而不修复仿真合约会奖励错误的执行行为 |
| R75 应在本次对比中从 WAIT_FOR_SECOND_CASE 升级 | 本对比是 R75 的第二个案例确认，但升级时机由 [#342](https://github.com/ShadyUnderLight/deep-research-skill/issues/342) validator 的实际运行结果决定 |
| R77 应与 R75 合并为一条规则 | R75 覆盖「声称但未执行的仿真」，R77 覆盖「不同可靠性层级的数据混合在一个分析中」——两者是不同的问题类型，需要不同检查项和不同触发条件 |
| Wikipedia 应被禁止作为世界杯分析的数据源 | Wikipedia 在赛制参数和历史赛果等结构性数据上是适当的数据源——问题不在 Wikipedia，而在于当 Wikipedia 数据与外部模型数据混合时缺乏层级分离 |

---

## Final judgment

### What the stronger report did better
- 两份报告均存在严重缺陷，但本地版的诚实限制在 trustworthiness 上略优于 GPT 版
- GPT 版的分析框架（路径难度映射）在结构上有价值，但被仿真执行证据的缺失所侵蚀
- 本地版对「数据不支持强结论」的诚实声明是 forward-looking claim discipline 的正确行为

### What should change in the repo now
- ✅ R77（cross-source model contamination）应作为 `CHECKLIST_HARDENING` 加入 `checklists/final-audit.md` 和/或 `references/report-template.md` §Source Register
- R75 已获得第二个案例确认，但等待 [#342](https://github.com/ShadyUnderLight/deep-research-skill/issues/342) validator 运行后升级
- 其余 5 个维度 `NO_ACTION`

### What should wait for another confirming case
- R75 的升级——第二个案例已确认，等待 [#342](https://github.com/ShadyUnderLight/deep-research-skill/issues/342) validator 运行后决定
- GPT 版的路径难度映射框架是否值得抽象为 template module——等更多有仿真的案例确认框架复用价值

### Is this mainly a missing rule, missing trigger, or execution problem?
- **Cross-source model contamination (D2, R77):** Missing rule —— source-layer 分离没有显式规则 → 由 R77 修复
- **Simulation contract (D2/D4, R75):** Missing rule（已有，WAIT_FOR_SECOND_CASE）——p 值/Elo/Monte Carlo 无执行证据的检测已经在 [#342](https://github.com/ShadyUnderLight/deep-research-skill/issues/342) 中作为 R75 提出，本对比提供第二次确认
- **Source strength (D3):** Missing rule（已有）——per-source 强度分级已在 [#341](https://github.com/ShadyUnderLight/deep-research-skill/issues/341) 中覆盖
- **Numeric roles (D2):** Execution problem —— 本地版 missing numeric role 标签是已有规则未触发

---

## Minimal quality bar

- [x] the two reports are comparable enough to justify distillation
- [x] the comparison used the six fixed dimensions
- [x] each accepted candidate has an action type
- [x] each accepted candidate has a proposed repo home
- [x] at least one rejected observation is documented when relevant
- [x] the final judgment distinguishes rule gap vs trigger gap vs execution gap
