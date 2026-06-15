# TSMC GPT vs Deep-Research-Skill Comparative Distillation

> **目的：** 将 GPT 深度研究版与本地 deep-research-skill 版对台积电的 paired-report 对比固化为回归资产，防止 future listed-company reports 重复出现同样的复合失败。

---

## Case identity

- **Case name:** TSMC listed-company GPT-vs-local comparative distillation
- **Date:** 2026-06-15
- **Research question:** 台积电当前估值是否充分反映 AI 半导体长期增长？
- **Why this comparison matters:**
  - 两份报告回答同一问题，但结构质量、执行纪律、方法论完整性差异显著。
  - 该对比是 [#276](https://github.com/ShadyUnderLight/deep-research-skill/issues/276) ~ [#280](https://github.com/ShadyUnderLight/deep-research-skill/issues/280) 所有改进的原始动机来源。
  - 本地版暴露了多个 listed-company route 的系统性薄弱环节，跨越 traceability、valuation methodology、capital return 和 customer concentration。
- **Report A:** GPT 深度研究版 `台积电估值是否已充分反映AI半导体长期增长.md`
- **Report B:** 本地 deep-research-skill 版 `2026-06-12-台积电估值是否充分反映AI半导体长期增长-深度研究报告.md`
- **Reference / stronger report (if any):** GPT 深度研究版（valuation 骨架更强，但在仓库格式纪律上有 gap）
- **Prompt(s):** 相同研究问题，两份报告均使用 deep-research style
- **Important scope or timing differences:**
  - 两份报告均基于 mid-2026 数据，时间窗口基本一致
  - GPT 版生成于 GPT 深度研究界面，本地版生成于 deep-research-skill pipeline
  - 对比焦点在结构性差异，而非事实检索能力

---

## Comparison purpose

This comparison is **not** for deciding which model is "better."

It is for:

1. 识别 listed-company route 中哪些规则 gap 已被 [#276](https://github.com/ShadyUnderLight/deep-research-skill/issues/276) ~ [#280](https://github.com/ShadyUnderLight/deep-research-skill/issues/280) 覆盖
2. 确认哪些 gap 仍有残余风险
3. 将 paired-report 基线固化为将来 regression 资产
4. 记录哪些改进来自"新规则"，哪些来自"执行链触发"

**Because all identified gaps have already been addressed by closed issues, this file serves primarily as a regression audit asset rather than a gap-discovery artifact.**

---

## Dimension 1: Source traceability and evidence weighting

### Report A (GPT)
- 正文有 claim-level 引用但格式为 `turn...` 不可复核
- 无 7 列 Source Register
- 引用离开原会话不可回溯

### Report B (Local)
- 有 Source Register 但非 7 列模板（列数不足、格式不一致）
- 正文缺 claim-level `[Sxx]` 引用
- 声称 source-traceability / final-audit 已通过，与正文事实不一致
- 将部分推断标记为 [CONF]（过度自信）

### Gap
- 本地版核心问题：**规则存在但执行链未触发**。Source traceability 和 final-audit 纪律已有文档，但报告生成时 validator 链未强制执行。
- GPT 版核心问题：**格式不符合仓库标准**，引用离源不可复核。

### Current status
✅ 已由 [#276](https://github.com/ShadyUnderLight/deep-research-skill/issues/276) 修复：
- Listed-company delivery-time validator chain 已接入
- Process-integrity gate 阻止 declared-not-executed 和 self-assessment 不一致
- `checklists/listed-company-report.md` 已强化 traceability 检查项

### Eval regression assets
- `evals/cases/advantech-listed-company-traceability-hard-fail-case.md` — traceability hard-fail 基准
- `evals/cases/pop-mart-listed-company-traceability-hard-fail-case.md` — traceability hard-fail 基准
- `evals/cases/content-platform-constrained-choice-compounded-fail-case.md` — self-assessment + traceability + quantitative-role 复合失败

### Action type
`NO_ACTION` — 规则已覆盖，validator 链已接入

---

## Dimension 2: Valuation methodology — DCF / sensitivity matrix

### Report A (GPT)
- 有完整 DCF 假设表、三情景股权价值、WACC/永续增长敏感性矩阵
- DCF 假设有来源标注
- 但假设的数字角色未正式标记（assumption / model output）

### Report B (Local)
- PE/PEG/同业倍数估值框架
- 有乐观/基准/悲观三情景
- **无 DCF / reverse DCF / 敏感性矩阵**
- 估值结论不可从第一原理重建
- CapEx、折旧、海外厂、新节点毛利率稀释未进入估值模型

### Gap
- 对于现金流可预测、运营历史 35+ 年的公司，无 DCF 是方法论上的重大缺失
- 多变量情景不能替代单变量敏感性分析

### Current status
✅ 已由 [#278](https://github.com/ShadyUnderLight/deep-research-skill/issues/278) 修复：
- `references/valuation-methodology.md` 新增 DCF/reverse DCF 触发规则
- `references/report-template.md` 新增 DCF 假设表 + 敏感性矩阵模板
- `checklists/listed-company-report.md` 新增 DCF/sensitivity 检查项

### Eval regression assets
- `evals/cases/tsmc-valuation-dcf-and-sensitivity-case.md` [#278] — DCF/敏感性 gap 基准

### Action type
`NO_ACTION` — 规则已覆盖，有专用 eval case

---

## Dimension 3: Valuation judgment — time horizon stratification

### Report A (GPT)
- 时间分层判断：3-5 年已较充分定价，10 年上行可选性未完全定价
- 四变量拆解：需求规模、份额捕获、AI mix/利润率、当前估值是否透支
- 投资行动与时间视野一致

### Report B (Local)
- 结论为单一方向："未充分反映长期价值"
- 未区分哪段 horizon 已定价、哪段存在可选性
- 缺少四变量显式拆解

### Gap
- 单一方向结论没有为不同投资期限提供可操作信号
- "长期可持有" 不能折叠为 "当前明显低估"

### Current status
✅ 已由 [#277](https://github.com/ShadyUnderLight/deep-research-skill/issues/277) 修复：
- `references/report-template.md` 新增时间分层段落
- `references/report-template.md` 新增四变量拆解
- `checklists/listed-company-report.md` 新增 horizon consistency 检查

### Eval regression assets
- `evals/cases/tsmc-valuation-time-horizon-stratification-case.md` [#277] — 时间分层 gap 基准

### Action type
`NO_ACTION` — 规则已覆盖，有专用 eval case

---

## Dimension 4: Capital return / FCF conversion

### Report A (GPT)
- CapEx / 折旧 / 海外厂和新节点 margin dilution 被写成资本回收约束
- 增长叙事与 FCF 生成能力之间有关联分析

### Report B (Local)
- 有现金流方向的关键数据
- **没有增长到 FCF / ROIC 的转换链条**
- CapEx 强度、海外厂投资回报周期未进入估值模型
- 资本配置纪律未作为估值变量

### Gap
- Key numbers 要求现金流方向，但未要求将增长叙事转换为现金回报预测
- 对于 CapEx-heavy 公司，资本回收轨迹是核心估值变量

### Current status
✅ 已由 [#279](https://github.com/ShadyUnderLight/deep-research-skill/issues/279) 修复：
- `references/valuation-methodology.md` 新增资本回收纪律
- `references/report-template.md` 新增 growth-to-cash-flow conversion table
- `checklists/listed-company-report.md` 新增资本回收检查项
- `checklists/final-audit.md` 新增 capital-return recall discipline

### Eval regression assets
⚠️ **此维度缺少独立 eval case**（相对于 #277/#278/#280 各有专用 TSMC eval case，资本回收纪律是唯一没有独立 eval case 的改进）。

### Action type
`NO_ACTION` — 规则已存在。资本回收纪律是唯一没有独立 eval case 的维度（其余 #277/#278/#280 各有专用 TSMC eval case）。

---

## Dimension 5: Customer concentration and second-source risk

### Report A (GPT)
- 展示 top-10 客户份额变化趋势
- 区分正效应（收入可见性）和负效应（定价权侵蚀）
- 分析主要客户的 second-source 信号（Google → Samsung/Intel）
- 将客户集中度写为估值变量：终端倍数调整、收入置信度

### Report B (Local)
- 提及"客户锁定效应强"
- 将客户集中度作为护城河描述词而非估值变量
- 无 top-10 / top-1 / top-2 时间序列数据
- 无 second-source 威胁窗口分析

### Gap
- 客户集中度被写成 moat booster 而非估值影响变量
- 未区分正/负效应，未做 second-source 检查

### Current status
✅ 已由 [#280](https://github.com/ShadyUnderLight/deep-research-skill/issues/280) 修复：
- `references/report-template.md` 新增客户集中度表格
- `references/moat-monopoly-screening.md` 新增 second-source 检查规则
- `checklists/listed-company-report.md` 新增 5 个客户集中度检查项

### Eval regression assets
- `evals/cases/tsmc-customer-concentration-and-second-source-case.md` [#280]

### Action type
`NO_ACTION` — 规则已覆盖，有专用 eval case

---

## Dimension 6: Self-assessment accuracy and process integrity

### Report A (GPT)
- 无自评审计模块（不符合仓库格式要求）
- 无 route/audit status 声明

### Report B (Local)
- 有声明的 audit status block
- **声称 source-traceability / final-audit 已通过，但实际上文缺 `[Sxx]`**
- **声称 source-register 合规，但非 7 列模板**
- 自评与正文执行不一致 — process-integrity 硬失败

### Gap
- 报告可以看起来结构完整，但 source/audit 硬门槛不执行
- 这是 process-integrity 失败而非内容失败

### Current status
✅ 已由 [#276](https://github.com/ShadyUnderLight/deep-research-skill/issues/276) 修复：
- Validator chain 在交付前强制检查自评与执行的一致性
- Process-integrity gate 定义为 hard-fail

### Eval regression assets
- `evals/cases/advantech-listed-company-traceability-hard-fail-case.md`
- `evals/cases/content-platform-constrained-choice-compounded-fail-case.md`
- `evals/cases/agentic-rag-technical-deep-dive-compounded-case.md`

### Action type
`NO_ACTION` — 规则已覆盖，validator 链已接入

---

## Candidate-action summary

| # | Candidate action | Failure family | Action type | Proposed home |
|---|---|---|---|---|
| 1 | Source traceability validator chain | source-traceability / self-assessment | `NO_ACTION` | Already closed by #276 |
| 2 | DCF/reverse DCF trigger and sensitivity matrix | valuation-methodology | `NO_ACTION` | Already closed by #278 |
| 3 | Time-horizon stratification and four-variable decomposition | valuation-judgment | `NO_ACTION` | Already closed by #277 |
| 4 | Capital return / FCF conversion discipline | capital-return | `NO_ACTION` | Already closed by #279 |
| 5 | Customer concentration as valuation variable | customer-concentration | `NO_ACTION` | Already closed by #280 |
| 6 | Capital return eval case gap noted | capital-return | `NO_ACTION` | Already closed by #279; no dedicated eval case yet |

**Summary: All 6 candidate actions are `NO_ACTION` (all gaps closed). Capital return (#279) is the only dimension without a dedicated eval case.**

---

## Triage notes

### Why most candidates are NO_ACTION

Each gap identified in the original paired-report comparison has been systematically addressed by issues #276-#280. This distillation exists to:

1. **Document that the loop is closed** — all known gaps from this paired comparison are now covered by rules, checklists, templates, or validator gates
2. **Provide a regression baseline** — if a future listed-company report passes through the pipeline and still exhibits any of these gaps, that is a regression
3. **Distinguish rule gaps from execution gaps** — most gaps were execution gaps (rules existed but triggers didn't fire), not missing rules

### Candidate 6: Capital return eval case gap

Capital return (#279) is the only dimension without a dedicated eval case. All others have TSMC-named eval cases. A future eval case should be created when another capital-return issue surfaces.

---

## Things explicitly rejected

| Observation | Why rejected |
|---|---|
| GPT 版应当被作为"标准输出格式" | GPT 版格式不符合仓库 Source Register 纪律和 route/audit status 要求——不是可接受交付物 |
| 本地版应被废弃 | 本地版的结构（research-anchor、market snapshot、情景估值）依然有价值，只是执行纪律有缺口 |
| 需要新增"GPT compatibility mode" | 仓库已有自己的格式纪律，不需要反向适配 |
| 这个 comparative-distillation 应放在 `evals/cases/` 下 | `evals/README.md` 明确定义 comparative-distillation 应放在 `evals/comparative-distillation/`，使用 `*-comparative-distillation.md` 命名 |

---

## Final judgment

### What the stronger report did better
- GPT 版在估值方法论（DCF、敏感性矩阵、时间分层）上明显更强
- GPT 版将客户集中度写为估值变量而非护城河描述
- GPT 版将增长叙事与资本回收约束关联

### What should change in the repo now
- ✅ 全部已通过 #276-#280 落地
- 所有 6 个维度均已覆盖规则或 validator 链
- 本文件作为 regression 基线

### What should wait for another confirming case
- Capital return eval case — 资本回收纪律缺少独立 eval case，可在另一个资本回收相关的 listed-company 报告出现时创建，遵循现有 TSMC eval case 的命名惯例

### Is this mainly a missing rule, missing trigger, or execution problem?
- **Source traceability / self-assessment**: Execution problem（规则存在，trigger 未触发）→ 已由 #276 修复
- **DCF/sensitivity**: Missing rule（模板偏 PE/EPS）→ 已由 #278 修复
- **Time horizon**: Missing trigger（模板不强制分层）→ 已由 #277 修复
- **Capital return**: Missing rule（无增长到现金转换链条）→ 已由 #279 修复
- **Customer concentration**: Missing rule（无 second-source 检查规则）→ 已由 #280 修复

**混合类型：** 该对比暴露了规则缺口、触发缺口和执行缺口。已分别按场景修复：
- Traceability / self-assessment 是执行缺口（规则存在但 trigger 未触发）
- DCF 和 capital return / customer concentration 是规则缺口（模板或检查规则不存在）
- Time horizon 是触发缺口（模板不强制分层输出）

---

## Minimal quality bar

- [x] the two reports are comparable enough to justify distillation
- [x] the comparison used the six fixed dimensions
- [x] each accepted candidate has an action type
- [x] each accepted candidate has a proposed repo home
- [x] at least one rejected observation is documented when relevant
- [x] the final judgment distinguishes rule gap vs trigger gap vs execution gap
