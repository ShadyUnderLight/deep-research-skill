# World Cup Best Third-Place Rule GPT-vs-Local Comparative Distillation

> **目的：** 将 GPT 深度研究版与本地 deep-research-skill 版对 2026 世界杯最佳小组第三晋级规则行为影响的 paired-report 对比固化为回归资产，防止 future regulatory/policy impact analysis 类报告重复出现 route self-declaration mismatch 和 regulatory contract 缺失。

---

## Case identity

- **Case name:** World Cup Best Third-Place Rule GPT-vs-Local Comparative Distillation
- **Date:** 2026-06-24
- **Research question:** Does the 2026 World Cup "best third-place" qualification rule make final group matches more conservative or more aggressive?
- **Why this comparison matters:**
  - 本地版报告声明 `Shared-workflow` 路由，但实际内容是 regulatory/policy impact analysis（分析规则组合如何改变行为激励）——路由自声明与实际内容负担不匹配。
  - 即便按正确路由（regulatory）审视，regulatory contract（snapshot、enforcement、impact separation、scenarios、monitoring）也未执行。
  - 该对比触发了 [#340](https://github.com/ShadyUnderLight/deep-research-skill/issues/340)（route wiring 修复）和 [#343](https://github.com/ShadyUnderLight/deep-research-skill/issues/343)（rule-system add-on）。
  - GPT 版具有更强的 metric framework 和 state taxonomy，但格式不兼容。
- **Report A:** GPT 深度研究版（metric framework: shots, xG, possession, cards, goal diff; state taxonomy: draw-to-qualify, must-win-on-goal-diff, already-qualified 等）
- **Report B:** 本地 deep-research-skill 版（多学科证据，nuanced "more polarized" 结论，但自声明错误路由）
- **Reference / stronger report (if any):** GPT 深度研究版（metric framework 和 state taxonomy 更强，但 citation 格式不适用于仓库）
- **Prompt(s):** 相同研究问题，两份报告均使用 deep-research style
- **Important scope or timing differences:**
  - 本地版声明 `Shared-workflow` 路由，但内容负担的自然路由是 `regulatory/policy impact analysis`
  - GPT 版以 regulatory analysis 框架组织内容（即便无显式路由元数据）
  - 对比焦点在路由准确性、regulatory contract 执行、metric framework 和 state taxonomy 等结构性差异

---

## Comparison purpose

This comparison is **not** for deciding which model is "better."

It is for:

1. 识别 route self-declaration mismatch（声明 Shared-workflow，实际 regulatory）是否已被 [#340](https://github.com/ShadyUnderLight/deep-research-skill/issues/340) 修复
2. 确认 GPT 版 metric framework 和 state taxonomy 是否需要作为新规则纳入仓库
3. 确认 regulatory contract 执行缺口是否已被 [#343](https://github.com/ShadyUnderLight/deep-research-skill/issues/343) 的 rule-system add-on 覆盖
4. 将 paired-report 基线固化为将来 regression 资产

**Because all identified gaps have already been addressed by closed issues, this file serves primarily as a regression audit asset rather than a gap-discovery artifact.**

---

## Dimension 1: Current-state discipline

### Report A (GPT)
- 显式记录 regulatory snapshot：当前 third-place 规则组合、比赛调度结构、simultaneous kickoff 约束
- 区分了 current regulation 与 pending/unknown policy（如 VAR 介入、纪律处分）
- 以 state taxonomy（draw-to-qualify, must-win-on-goal-diff, already-qualified 等）组织 current-state 分析
- 将 enforcement reality（FIFA 监督、同时开球纪律）纳入当前状态框架

### Report B (Local)
- 分析了规则对行为的影响，但未正式建立 regulatory snapshot 作为分析基线
- 规则内容散见于分析段落，未作为独立 current-state 快照呈现
- 缺少 enforcement reality 的显式说明（simultaneous kickoff 的约束力、FIFA 纪律机制）
- 未区分 "当前已制定规则" 与 "pending/unknown policy"

### Gap
- 本地版缺失 regulatory snapshot——分析了规则效应但未将当前规则组合作为 regulatory baseline 正式文档化
- GPT 版的 state taxonomy 提供了一种将 current-state 结构化为可分析维度的方式
- 核心问题：报告在分析规则效应，但没有先建立"当前规则是什么"的快照

### Current status
- 本地版缺失 enforcement reality 显式说明

### Eval regression assets
- `evals/cases/world-cup-rule-regulatory-route-mismatch-case.md` — 综合 eval 覆盖 current-state snapshot 要求

### Action type
`NO_ACTION` — [#343](https://github.com/ShadyUnderLight/deep-research-skill/issues/343) 的 rule-system add-on 覆盖 regulatory snapshot 纪律

---

## Dimension 2: Numerical and date discipline

### Report A (GPT)
- 建立了可观测 metric framework：shots、xG、possession、cards、goal difference
- 每个 metric 有明确的角色：哪些是行为变化的观测指标，哪些是机制约束
- metrics 与 state taxonomy 联动——不同 state 下预期的 metric pattern 不同
- 数字角色隐含可识别（观测 vs 推断），但未按仓库标准显式标注

### Report B (Local)
- 以定性分析为主，缺少将行为变化映射到可观测指标的框架
- 讨论了"更保守/更激进"的定性判断，但没有对应的定量观测维度
- 多学科证据（历史、博弈论、统计）丰富了论证但未形成 metric framework

### Gap
- 本地版仅有定性分析，GPT 版使用可观测 metrics 将行为变化锚定到量化指标
- 这是 regulatory analysis 中"如何验证规则效应"的关键维度
- GPT 版的 metric framework 和 state taxonomy 联动是 regulator 评估规则效果的标准方法

### Current status
- 本地版缺少将行为变化映射到可观测指标的 metric framework

### Eval regression assets
- `evals/cases/world-cup-rule-regulatory-route-mismatch-case.md` — 综合 eval 覆盖 quantitative discipline 要求

### Action type
`NO_ACTION` — [#343](https://github.com/ShadyUnderLight/deep-research-skill/issues/343) 的 rule-system add-on 覆盖 regulatory 报告的量化纪律

---

## Dimension 3: Source traceability and evidence weighting

### Report A (GPT)
- 正文有 claim-level 引用密度但格式为 GPT 专有（不可复核）
- 无 7 列 Source Register
- 无 route/audit status 模块

### Report B (Local)
- 正文缺 `[Sxx]` claim-level 内联引用——仅有来源列表但正文未逐条标注
- Source Register 格式不完整（非标准 7 列）
- 自评声明路由/审计状态与实际执行不一致

### Gap
- 本地版核心问题：body-level traceability 缺失——来源存在但未在正文中逐条连接到具体主张
- GPT 版虽然有 claim-level 密度，但格式不可复核
- 该 gap 是路由错误（声明 Shared-workflow 而非 regulatory）的衍生后果——错误路由未能触发对应的 traceability validator

### Current status
✅ 已由 [#340](https://github.com/ShadyUnderLight/deep-research-skill/issues/340) 修复：
- Route auto-detection 扩展支持中文/混合格式路由声明
- 未知 route 不再静默回落到 fallback 路由
- Regulatory route 激活时强制触发 source traceability validator
- Process-integrity gate 在交付前强制检查自评与执行的一致性

### Eval regression assets
- `evals/cases/world-cup-rule-regulatory-route-mismatch-case.md` — 综合 eval

### Action type
`NO_ACTION` — [#340](https://github.com/ShadyUnderLight/deep-research-skill/issues/340) 通过 route wiring 修复覆盖

---

## Dimension 4: Forward-looking claim discipline

### Report A (GPT)
- 显式说明 pre-match 信息变化如何调整不同 strategic state 的概率分布
- 区分了"规则结构决定的行为方向"与"特定赛事条件决定的行为幅度"
- 不确定性沟通更诚实——指出哪些行为预测是结构性的（规则驱动），哪些是情境性的（队伍特性驱动）

### Report B (Local)
- 给出了"more polarized"的整体结论，但未展示在不同条件下（如不同组的实力分布、不同赛程安排）该结论如何变化
- 缺少 scenario 结构——读者无法知道"如果 X 条件改变，结论是否仍成立"
- reversal conditions 存在但不完整

### Gap
- GPT 版对 forward-looking 的条件化表达更显式——帮助读者理解结论的适用范围和条件依赖
- 本地版的 single-point "more polarized" 结论缺少情境敏感性分析
- 这是 regulatory analysis 的核心纪律：政策效应必须在不同 scenario 下测试

### Current status
✅ 已由 [#309](https://github.com/ShadyUnderLight/deep-research-skill/issues/309) 覆盖：
- Decision Scope 块强制列出改变结论的条件
- `checklists/option-selection-final-audit.md` 新增 first-screen clarity 检查
- `references/decision-report-template.md` 新增 Decision Scope 块要求

### Eval regression assets
- `evals/cases/world-cup-rule-regulatory-route-mismatch-case.md` — 约束 forward-looking claim discipline

### Action type
`NO_ACTION` — [#309](https://github.com/ShadyUnderLight/deep-research-skill/issues/309) 的 Decision Scope 已覆盖

---

## Dimension 5: Structural readability and information density

### Report A (GPT)
- 以 regulatory analysis 框架组织内容：snapshot → mechanism → scenarios → monitoring
- 尽管无显式 route metadata，但结构自然匹配 regulatory contract 的信息流
- state taxonomy 提供了清晰的 section 组织方式

### Report B (Local)
- 自声明 `Shared-workflow`，但该路由与内容负担不匹配
- 内容实质是 regulatory/policy impact analysis，但结构未遵循 regulatory contract
- 路由声明错误导致缺失 sections（snapshot、enforcement、impact separation、scenarios、monitoring）
- 多学科证据有价值，但被错误的路由结构削弱了可用性

### Gap
- 本地版核心问题是 route self-declaration mismatch——声明了不适合内容负担的路由
- Shared-workflow 是跨领域流程任务的路由，不是领域特定的政策分析路由
- 路由错误导致 artifact contract 整体不匹配——即便内容质量高，结构不满足交付要求

### Current status
✅ 已由 [#340](https://github.com/ShadyUnderLight/deep-research-skill/issues/340) 修复：
- Route auto-detection 现在根据内容负担选择路由，而非仅依赖自声明
- 规则分析类内容 → regulatory/policy impact analysis 路由
- Route declaration mismatch gate 在交付前检查自声明与内容的一致性

### Eval regression assets
- `evals/cases/world-cup-rule-regulatory-route-mismatch-case.md` — 本 eval 的专门案例

### Action type
`NO_ACTION` — [#340](https://github.com/ShadyUnderLight/deep-research-skill/issues/340) 的 route wiring 修复覆盖

---

## Dimension 6: Decision usefulness

### Report A (GPT)
- 提供了可用于未来赛事分析的 metric framework
- state taxonomy 帮助决策者快速识别不同情境下的行为预期
- 量化指标使规则效应可被观测和验证

### Report B (Local)
- 多学科证据（历史、博弈论、统计、专家评论、反证）提供了 nuanced 的 "more polarized" 结论
- 对政策制定者理解规则效应的复杂性有价值——不是简单的"更保守"或"更激进"
- reversal conditions 和 counter-evidence 增强了分析的平衡性

### Gap
- 两份报告在不同维度上有用：GPT 版在可操作性和可验证性上更强，本地版在分析深度和 nuance 上更强
- 理想场景是将两者的优势结合：GPT 的 metric framework + 本地版的多学科证据 depth
- 但这不是 structural gap 而是 feature spectrum——两份报告服务于不同的使用场景

### Current status
✅ 两份报告的 strengths 互补而非互斥。路由修复（[#340](https://github.com/ShadyUnderLight/deep-research-skill/issues/340)）和 rule-system add-on（[#343](https://github.com/ShadyUnderLight/deep-research-skill/issues/343)）将使未来版本的本地报告同时具备结构性纪律和分析深度。

### Eval regression assets
- `evals/cases/world-cup-rule-regulatory-route-mismatch-case.md` — 综合 eval

### Action type
`NO_ACTION` — 两份报告互补，gap 已通过路由修复和规则补齐覆盖

---

## Candidate-action summary

| # | Candidate action | Failure family | Action type | Proposed home |
|---|---|---|---|---|
| 1 | Route self-declaration mismatch gate (Shared-workflow vs regulatory) | route-wiring / rule-activation | `NO_ACTION` | Already closed by [#340](https://github.com/ShadyUnderLight/deep-research-skill/issues/340) |
| 2 | Regulatory contract execution (snapshot, enforcement, impact separation, scenarios, monitoring) | current-state / structural | `NO_ACTION` | Already closed by [#343](https://github.com/ShadyUnderLight/deep-research-skill/issues/343) |
| 3 | Body-level [Sxx] traceability for regulatory route | source-traceability / evidence-weighting | `NO_ACTION` | Already closed by [#340](https://github.com/ShadyUnderLight/deep-research-skill/issues/340) via validator chain |
| 4 | Decision Scope block for forward-looking claims in regulatory analysis | forward-looking / scenario-discipline | `NO_ACTION` | Already closed by [#309](https://github.com/ShadyUnderLight/deep-research-skill/issues/309) |
| 5 | Metric framework as rule-system add-on for regulatory reports | numerical-discipline | `NO_ACTION` | Already closed by [#343](https://github.com/ShadyUnderLight/deep-research-skill/issues/343) |
| 6 | Process-integrity gate for route declaration accuracy | process-integrity | `NO_ACTION` | Already closed by [#340](https://github.com/ShadyUnderLight/deep-research-skill/issues/340) |

**Summary: All 6 candidate actions are `NO_ACTION` (all gaps closed by #340, #343, #309).**

---

## Triage notes

### Why all candidates are NO_ACTION

Each gap identified in the original paired-report comparison has been systematically addressed by issues [#340](https://github.com/ShadyUnderLight/deep-research-skill/issues/340), [#343](https://github.com/ShadyUnderLight/deep-research-skill/issues/343), and [#309](https://github.com/ShadyUnderLight/deep-research-skill/issues/309). This distillation exists to:

1. **Document that the loop is closed** — all known gaps from this paired comparison are now covered by rules, checklists, templates, or validator gates
2. **Provide a regression baseline** — if a future regulatory/policy impact analysis report passes through the pipeline and still exhibits route self-declaration mismatch or missing regulatory contract, that is a regression
3. **Distinguish rule gaps from execution gaps** — the core gap was route self-declaration mismatch (execution/wiring: regulatory route not triggered), and the secondary gap was missing rule-system discipline (addressed by #343)

### Relative to constrained-choice World Cup comparative distillation

This file is the third World Cup comparative distillation (following constrained-choice and info-advantage). The constrained-choice case addressed probability-distribution gaps. This case addresses route self-declaration accuracy and regulatory contract execution. Both share a common thread: route wiring failures where validators existed but were not triggered due to incorrect route selection.

---

## Things explicitly rejected

| Observation | Why rejected |
|---|---|
| GPT 的 metric framework（shots, xG, possession 等）应直接并入 template | [#343](https://github.com/ShadyUnderLight/deep-research-skill/issues/343) 已通过 rule-system add-on 机制处理，而非硬编码到 template——不同领域的 regulatory analysis 需要不同的 metric set |
| 本地版应废弃（因为路由错误） | 本地版的多学科证据（历史、博弈论、统计、counter-evidence）和对行为 "more polarized" 的 nuanced 结论仍有价值——问题在路由和结构，不在分析质量 |
| 应把 `Shared-workflow` 作为 route 分析的 catch-all | Shared-workflow 有明确的适用边界（跨领域流程任务），不应被用作"不确定时回退"的兜底路由。这会导致 regulatory 内容被 Shared-workflow 的 artifact contract 错误约束 |
| GPT 版 state taxonomy 应直接作为 regulatory template 的标准 section | State taxonomy 是 GPT 版对特定问题的 domain-specific 分析工具，不是通用 regulatory template 组件。未来其他 regulatory 分析可能需要不同的 taxonomy |
| 本对比应放在 `evals/cases/` 下 | `evals/README.md` 明确定义 comparative-distillation 应放在 `evals/comparative-distillation/`，使用 `*-comparative-distillation.md` 命名 |

---

## Final judgment

### What the stronger report did better
- GPT 版在 current-state discipline 上更强：显式建立了 regulatory snapshot 和 state taxonomy
- GPT 版在 numerical discipline 上更强：建立了可观测 metric framework 将行为变化锚定到量化指标
- GPT 版在 forward-looking discipline 上更强：条件化表达结论的适用范围和情境依赖
- GPT 版在 structural 上更匹配内容负担：自然使用了 regulatory analysis 框架（即便无显式路由声明）

### What should change in the repo now
- ✅ 全部已通过 [#340](https://github.com/ShadyUnderLight/deep-research-skill/issues/340)、[#343](https://github.com/ShadyUnderLight/deep-research-skill/issues/343)、[#309](https://github.com/ShadyUnderLight/deep-research-skill/issues/309) 落地
- 所有 6 个维度均已覆盖规则或 validator 链
- 本文件作为 regression 基线

### What should wait for another confirming case
- GPT 版 state taxonomy 作为 regulatory 报告的 optional 结构工具——当前 [#343](https://github.com/ShadyUnderLight/deep-research-skill/issues/343) 的 rule-system add-on 提供了框架但不强制特定 taxonomy。如果 future regulatory 报告再次出现无结构化 state 分类的问题，应考虑升级为 recommended section。
- "Shared-workflow catch-all" 问题——当前仅由 route auto-detection 和 mismatch gate 间接防止。如果 future 报告再次出现不匹配的 Shared-workflow 声明，应新增 explicit "route declaration justification" block。

### Is this mainly a missing rule, missing trigger, or execution problem?
- **Route self-declaration mismatch**: Execution/wiring problem（规则分析内容未触发 regulatory 路由）→ 已由 [#340](https://github.com/ShadyUnderLight/deep-research-skill/issues/340) 修复
- **Regulatory contract not executed**: Missing rule（regulatory 路由的 artifact contract 缺少 rule-system discipline）→ 已由 [#343](https://github.com/ShadyUnderLight/deep-research-skill/issues/343) 修复
- **Body-level traceability**: Execution problem（regulatory 路由的 validator 未触发）→ 已由 [#340](https://github.com/ShadyUnderLight/deep-research-skill/issues/340) 修复
- **Forward-looking scenario structure**: Missing template（Decision Scope 块未强制 scenario 结构）→ 已由 [#309](https://github.com/ShadyUnderLight/deep-research-skill/issues/309) 修复

**混合类型：** 该对比暴露了路由触发缺口（route auto-detection）、规则缺口（rule-system discipline）和模板缺口（Decision Scope）。均已按场景修复。

---

## Minimal quality bar

- [x] the two reports are comparable enough to justify distillation
- [x] the comparison used the six fixed dimensions
- [x] each accepted candidate has an action type
- [x] each accepted candidate has a proposed repo home
- [x] at least one rejected observation is documented when relevant
- [x] the final judgment distinguishes rule gap vs trigger gap vs execution gap
