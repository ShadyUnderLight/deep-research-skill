# World Cup Information Advantage GPT-vs-Local Comparative Distillation

> **目的：** 将 GPT 深度研究版与本地 deep-research-skill 版对 2026 世界杯"后赛信息优势"问题的 paired-report 对比固化为回归资产，防止 future 报告出现 traceability theatre（形式可追溯但实质不可审计）——这是 source strength 作为独立审计维度的关键发现。

---

## Case identity

- **Case name:** World Cup Information Advantage GPT-vs-Local Comparative Distillation
- **Date:** 2026-06-24
- **Research question:** Does the World Cup third-place qualification rule give later-playing teams an information advantage?
- **Why this comparison matters:**
  - 本地版报告拥有完整的 traceability infrastructure（body `[Sxx]` 内联引用、7 列 Source Register、零 inflation），但所有 8 个源均为 Wikipedia/众包来源——source strength 无法支撑 load-bearing claims。
  - Source Register 使用"支持章节"（section-level）而非 "Claims Supported"（claim-level）——7 列格式正确但映射粒度过粗。
  - 这是 "traceability theatre" 案例：形式可追溯，但实质不可审计，因为所有来源都是众包编纂。
  - 该对比触发了 [#341](https://github.com/ShadyUnderLight/deep-research-skill/issues/341)（source strength gate + Claims Supported granularity hardening）。
- **Report A:** GPT 深度研究版（mechanism analysis、game theory framework，但 citation 格式不兼容）
- **Report B:** 本地 deep-research-skill 版（正确选择 technical-deep-dive 路由，强机制解释，但 100% Wikipedia、Claims Supported 为 section-level、numeric roles 缺失）
- **Reference / stronger report (if any):** GPT 深度研究版（game theory 框架和不确定性沟通更强，但 citation 格式不适用于仓库）
- **Prompt(s):** 相同研究问题，两份报告均使用 deep-research style
- **Important scope or timing differences:**
  - 本地版正确激活了 technical-deep-dive 路由，机制分析质量高
  - 但 source strength 严重不足——所有 load-bearing claims 依赖 Wikipedia
  - GPT 版对 uncertainty 沟通更诚实，但格式不兼容
  - 对比焦点在 source strength 纯度、Source Register 语义粒度、numeric role labeling 和 route conflict check

---

## Comparison purpose

This comparison is **not** for deciding which model is "better."

It is for:

1. 确认 "traceability theatre"（完整 traceability 基础设施但 source strength 不足）是否已被 [#341](https://github.com/ShadyUnderLight/deep-research-skill/issues/341) 的 source strength gate 覆盖
2. 确认 "Claims Supported" vs "支持章节" 语义 gap 是否已被 [#341](https://github.com/ShadyUnderLight/deep-research-skill/issues/341) 的 granularity hardening 修复
3. 确认 numeric role labels 缺失问题是否已被 [#341](https://github.com/ShadyUnderLight/deep-research-skill/issues/341) 覆盖
4. 确认 route conflict check（technical-deep-dive vs regulatory）缺失是否已被 [#340](https://github.com/ShadyUnderLight/deep-research-skill/issues/340) 的 route boundary 检查覆盖
5. 将 "100% Wikipedia" 作为 traceability theatre 的基准案例固化为回归资产

**Because all identified gaps have already been addressed by closed issues, this file serves primarily as a regression audit asset rather than a gap-discovery artifact.**

---

## Dimension 1: Current-state discipline

### Report A (GPT)
- 建立了清晰的 current-state 描述：当前的 schedule 结构、信息集不对称的形成机制
- 区分了规则层面的 current-state 和赛事实例层面的 current-state
- 识别了 simultaneous kickoff 规则作为关键 current-state constraint

### Report B (Local)
- 正确识别了 current-state 的核心要素：信息集不对称、sequential game structure、threshold calculation
- 对 current rule architecture 的描述准确（third-place qualification mechanics、ranking criteria、match scheduling）
- 机制解释从 current-state 自然展开

### Gap
- 两份报告在 current-state discipline 上均表现充分——都建立了清晰的分析基线
- GPT 版对 game theory 层面的 current-state 描述更精确，本地版对规则细节的描述更完整
- 无结构性 gap

### Current status
✅ 两份报告在 current-state discipline 上均合格。各自从不同角度建立了分析基线。

### Eval regression assets
- `evals/cases/world-cup-info-advantage-technical-deep-dive-source-strength-case.md` — 综合 eval

### Action type
`NO_ACTION` — 两份报告 current-state discipline 均充分，无 gap 需修复

---

## Dimension 2: Numerical and date discipline

### Report A (GPT)
- game theory framework 中隐含数值角色：probabilities、payoffs、equilibrium thresholds
- 数值有清晰的理论来源（sequential game model）但未按仓库标准显式标注 observed/proxy/assumption/model-output
- 对 empirical limitations 有诚实说明（low scoring、bounded rationality、common knowledge 假设）

### Report B (Local)
- 比较表格中包含具体数值（67%、9 groups / 27 matches、12/27 matches、概率估计）
- **数字角色标签缺失**——comparison tables 中的百分比、比赛数、概率值缺乏 observed/proxy/assumption/model-output 角色
- 数值的推导过程未文档化——读者无法判断哪些是事实统计，哪些是模型估算
- 概率估计无 confidence interval 或 sensitivity analysis

### Gap
- 本地版核心问题：数值存在但角色未标注——67% 是 observed count 还是 model output？概率值基于什么假设？
- GPT 版虽然没有显式角色标注，但 game theory 框架给出了数值的理论推导路径
- 该 gap 是 source strength 问题的延伸：如果数值基于 Wikipedia 数据，其角色应该是 proxy/crowdsourced 而非 observed

### Current status
✅ 已由 [#341](https://github.com/ShadyUnderLight/deep-research-skill/issues/341) 覆盖：
- Source strength gate 间接改善数值纪律——当 source 被标记为低强度时，基于该 source 的数值必须标注为 proxy 或 assumption
- Claims Supported 的 claim-level granularity 使数值与来源的映射可审计

### Eval regression assets
- `evals/cases/world-cup-info-advantage-technical-deep-dive-source-strength-case.md` — 综合 eval 覆盖 numeric role discipline

### Action type
`NO_ACTION` — [#341](https://github.com/ShadyUnderLight/deep-research-skill/issues/341) 的 source-strength gate 间接覆盖 numeric role labeling

---

## Dimension 3: Source traceability and evidence weighting

### Report A (GPT)
- 正文有 claim-level 引用但格式为 GPT 专有
- game theory 引用有理论来源但不可复核
- 无 7 列 Source Register

### Report B (Local)
- ✅ body `[Sxx]` 内联引用完整
- ✅ 7 列 Source Register 格式完整
- ✅ 零 inflation（所有注册源均在正文被引用）
- ❌ **100% Wikipedia/crowdsourced** — 全部 8 个 Source Register 条目为 Wikipedia
- ❌ **"支持章节" ≠ "Claims Supported"** — Source Register 映射列使用 section-level granularity 而非 claim-level
- ❌ load-bearing claims（FIFA 官方规则、UEFA 调度决策、教练策略、博弈论概念）依赖众包编纂而非 primary source

### Gap
- 核心发现：**traceability theatre** — traceability 基础设施（body [Sxx]、7 列 register、零 inflation）完整，但 source strength 不足以支撑 load-bearing claims
- "支持章节"（section-level）映射无法让 reviewer 验证 "哪个 source 支持哪个具体 claim"
- 这暴露了一个新的审计维度：traceability 不仅是"有没有引用"，还包括"来源强度是否匹配主张重量"
- 100% Wikipedia 作为极限基准——如果所有 source 都是众包编纂，即便 traceability 格式完美，实质审计也无法进行

### Current status
✅ 已由 [#341](https://github.com/ShadyUnderLight/deep-research-skill/issues/341) 直接修复：
- Source strength gate 新增 source 强度评级要求（primary > official > authoritative > aggregator > crowdsourced）
- "Claims Supported" 列强制 claim-level granularity——不允许 section-level "支持章节"
- Wikipedia 被标记为 crowdsourced 级别，load-bearing claims 不可仅依赖 Wikipedia
- Process-integrity gate 新增 source strength 一致性检查

### Eval regression assets
- `evals/cases/world-cup-info-advantage-technical-deep-dive-source-strength-case.md` — 专门 eval case

### Action type
`NO_ACTION` — [#341](https://github.com/ShadyUnderLight/deep-research-skill/issues/341) 直接解决本维度所有 gap

---

## Dimension 4: Forward-looking claim discipline

### Report A (GPT)
- game theory framework 提供了清晰的 forward-looking 推理路径：给定 current rule structure，后赛队伍的 optimal strategy 是什么
- 显式说明了 game theory 模型的 limiting assumptions（common knowledge、rationality、simultaneous constraint）
- 对 empirical 不确定性有诚实沟通："方向确定，幅度不确定"
- 区分了结构性预测（规则驱动）和情境性预测（队伍特性驱动）

### Report B (Local)
- 提供了条件化的"存在-but-limited"结论：信息优势在理论上存在，但实际影响受多重约束限制
- 识别了 fundamental constraints（simultaneous kickoff、low scoring、bounded rationality、common knowledge）
- 缺少 confidence calibration——未说明在什么条件下该结论的置信度会显著变化

### Gap
- GPT 版在不确定性沟通上更显式和诚实：清楚地说明了 game theory 模型的假设边界和 empirical limitation
- 本地版虽然结论谨慎，但未将不确定性结构化地呈现给读者
- 这不是 source strength 的直接延伸，而是 technical-deep-dive 报告中 uncertainty communication 的纪律问题

### Current status
✅ 已由 [#341](https://github.com/ShadyUnderLight/deep-research-skill/issues/341) 间接覆盖：
- Source strength gate 要求低强度 source 支持的主张必须标注 uncertainty caveat
- 当主要 source 均为 crowdsourced 级别时，forward-looking claims 必须附带 confidence statement
- Decision Scope 块（[#309](https://github.com/ShadyUnderLight/deep-research-skill/issues/309)）要求列出改变结论的条件

### Eval regression assets
- `evals/cases/world-cup-info-advantage-technical-deep-dive-source-strength-case.md` — 综合 eval

### Action type
`NO_ACTION` — [#341](https://github.com/ShadyUnderLight/deep-research-skill/issues/341) 和 [#309](https://github.com/ShadyUnderLight/deep-research-skill/issues/309) 联合覆盖

---

## Dimension 5: Structural readability and information density

### Report A (GPT)
- game theory framework 提供了清晰的 structural backbone：mechanism → game structure → equilibrium analysis → empirical constraints
- 尽管无显式 route metadata，结构自然服务于 technical-deep-dive 的信息流
- 对 alternative architectures 的比较（full group synchronization、revert to top-2、16 groups of 3）清晰组织

### Report B (Local)
- ✅ 正确选择了 technical-deep-dive 路由
- ✅ 机制解释清晰，comparison dimensions 明确，trade-off analysis 完整
- ❌ **route conflict check 缺失**——报告触及 rule reform implications（regulatory 边界），但未文档化为什么 technical-deep-dive 而非 regulatory 作为 primary route
- 结构总体良好，但 route boundary 未显式声明

### Gap
- 本地版核心问题：当 topic 横跨多个 route 边界（technical + regulatory），需要文档化 primary route 选择理由
- 该 gap 在 content quality 高的报告中尤其隐蔽——分析本身质量高，但 route discipline 上的灰色地带未被处理
- GPT 版虽然无 route 概念，但其 game theory focus 自然将范围限制在 technical 维度

### Current status
✅ 已由 [#340](https://github.com/ShadyUnderLight/deep-research-skill/issues/340) 覆盖：
- Route auto-detection 根据内容负担确定 primary route
- Route conflict check 在交付前要求文档化 primary route 选择理由
- Regulatory 相关内容作为 secondary content 被允许，但需要明确 primary route 的边界

### Eval regression assets
- `evals/cases/world-cup-info-advantage-technical-deep-dive-source-strength-case.md` — 专门 eval case
- `evals/cases/world-cup-rule-regulatory-route-mismatch-case.md` — 同 topic 的不同 route 问题

### Action type
`NO_ACTION` — [#340](https://github.com/ShadyUnderLight/deep-research-skill/issues/340) 的 route boundary 检查覆盖

---

## Dimension 6: Decision usefulness

### Report A (GPT)
- game theory framework 提供了结构化的决策推理工具
- alternative architectures 比较帮助决策者理解现有规则设计的 tradeoff
- 不确定性沟通诚实——帮助决策者理解 confidence boundary

### Report B (Local)
- ✅ 机制解释强——读者可以清楚理解信息优势的形成和限制
- ✅ 提供了明确的 bottom-line judgment 和 practitioner recommendations
- ✅ 对 fundamental constraints 的识别有实际价值
- ❌ 但所有 load-bearing claims 基于 Wikipedia——决策者无法确定结论基于 primary evidence 还是 crowd interpretation
- ❌ section-level "支持章节" 使得读者无法追溯"具体哪个主张来自哪个 source 的哪个 claim"

### Gap
- 本地版的决策有用性被 source strength 严重削弱——即使机制分析正确，决策者无法独立验证基础事实
- 这是 "有说服力但不可审计" 的问题：分析逻辑可能是对的，但证据链不满足决策支持标准
- GPT 版虽然 source 格式不兼容，但其 game theory 框架提供了可独立验证的理论推理链

### Current status
✅ 已由 [#341](https://github.com/ShadyUnderLight/deep-research-skill/issues/341) 直接覆盖：
- Source strength gate 要求 load-bearing claims 必须有 primary/authoritative source 支撑
- Claims Supported claim-level granularity 使决策者可以 trace "哪个 source 的哪个具体信息支持哪个具体结论"
- Process-integrity gate 在 source strength 不满足时阻止全 ✅ 自评

### Eval regression assets
- `evals/cases/world-cup-info-advantage-technical-deep-dive-source-strength-case.md` — 综合 eval

### Action type
`NO_ACTION` — [#341](https://github.com/ShadyUnderLight/deep-research-skill/issues/341) 直接解决 source strength 对决策有用性的影响

---

## Candidate-action summary

| # | Candidate action | Failure family | Action type | Proposed home |
|---|---|---|---|---|
| 1 | Source strength gate — Wikipedia/crowdsourced cannot bear load-bearing claims | source-traceability / evidence-weighting | `NO_ACTION` | Already closed by [#341](https://github.com/ShadyUnderLight/deep-research-skill/issues/341) |
| 2 | "Claims Supported" claim-level granularity — 不允许 section-level "支持章节" | source-traceability / Source Register semantics | `NO_ACTION` | Already closed by [#341](https://github.com/ShadyUnderLight/deep-research-skill/issues/341) |
| 3 | Numeric role labeling for comparison/estimate numbers | numerical-discipline | `NO_ACTION` | Already covered by [#341](https://github.com/ShadyUnderLight/deep-research-skill/issues/341) via source-strength gate |
| 4 | Route conflict check — document why technical-deep-dive rather than regulatory | route-wiring / structural | `NO_ACTION` | Already closed by [#340](https://github.com/ShadyUnderLight/deep-research-skill/issues/340) |
| 5 | Source-strength-aware uncertainty communication | forward-looking / claim-discipline | `NO_ACTION` | Already covered by [#341](https://github.com/ShadyUnderLight/deep-research-skill/issues/341) + [#309](https://github.com/ShadyUnderLight/deep-research-skill/issues/309) |
| 6 | Process-integrity gate — 不允许 source strength gaps 时的全 ✅ 自评 | process-integrity | `NO_ACTION` | Already closed by [#341](https://github.com/ShadyUnderLight/deep-research-skill/issues/341) |

**Summary: All 6 candidate actions are `NO_ACTION` (all gaps closed by #341, #340, #309).**

---

## Triage notes

### Why all candidates are NO_ACTION

Each gap identified in the original paired-report comparison has been systematically addressed by issues [#341](https://github.com/ShadyUnderLight/deep-research-skill/issues/341), [#340](https://github.com/ShadyUnderLight/deep-research-skill/issues/340), and [#309](https://github.com/ShadyUnderLight/deep-research-skill/issues/309). This distillation exists to:

1. **Document the "traceability theatre" phenomenon** — this is the first case where full traceability infrastructure (body [Sxx], 7-col register, zero inflation) coexists with fatal source strength weakness (100% Wikipedia)
2. **Establish "100% Wikipedia" as a severity benchmark** — any future report with all or most load-bearing claims on Wikipedia should trigger source strength gate
3. **Distinguish form-traceability from substance-auditability** — "Claims Supported" at claim-level is a different discipline than "支持章节" at section-level
4. **Provide a regression baseline** — if a future technical-deep-dive report has [Sxx] citations and 7-col register but all sources are Wikipedia, that is a regression

### Unique contribution: Source strength as independent audit dimension

Before this case, the eval framework tested traceability at the form level (citation presence, register completeness, inflation). This case demonstrates that form-level traceability can be perfect while substance-level auditability is zero.

The discovery that "100% Wikipedia with full [Sxx] traceability = false sense of auditability" is the key contribution of this distillation. It motivated the creation of source strength as an independent audit dimension in [#341](https://github.com/ShadyUnderLight/deep-research-skill/issues/341).

---

## Things explicitly rejected

| Observation | Why rejected |
|---|---|
| Wikipedia 应被 default 视为 high reliability source | Wikipedia 是众包编纂，不适合作为 load-bearing claims 的 sole source。FIFA 官方规则、UEFA 调度决策、教练策略等主张需要 primary/authoritative source |
| "支持章节" 可以替代 "Claims Supported" | Section-level mapping 无法让 reviewer 验证 "哪个 source 的哪个具体信息支持哪个具体主张"——这是粒度问题，不是格式问题 |
| GPT 版 game theory framework 应直接并入 template | Game theory 是 domain-specific 分析工具，不是通用 template 组件。不同 technical-deep-dive 报告需要不同的分析框架。重点在 source strength discipline，不在 framework 选择 |
| 本地版 traceability 基础设施是多余的（因为 source 弱） | Traceability 基础设施本身有价值——它暴露了 source strength 问题。如果没有 [Sxx] 和 register，我们甚至无法发现 100% Wikipedia 的问题 |
| 该对比应只关注 source strength，不关注 route conflict check | Route conflict check 缺失是独立的交付纪律问题——即便 source strength 修复后，route boundary 未文档化仍然是 gap |

---

## Final judgment

### What the stronger report did better
- GPT 版在 uncertainty communication 上更强：显式声明 game theory 模型的 limiting assumptions 和 empirical boundary
- GPT 版在游戏理论框架上更显式——提供了结构化的推理路径和 equilibrium analysis
- GPT 版在 alternative architectures 比较上更系统

### What should change in the repo now
- ✅ 全部已通过 [#341](https://github.com/ShadyUnderLight/deep-research-skill/issues/341)、[#340](https://github.com/ShadyUnderLight/deep-research-skill/issues/340)、[#309](https://github.com/ShadyUnderLight/deep-research-skill/issues/309) 落地
- Source strength gate 已建立（#341）
- "Claims Supported" claim-level granularity 已强制执行（#341）
- Route conflict check 已接入交付链（#340）
- 本文件作为 regression 基线

### What should wait for another confirming case
- Source strength 评级体系（primary > official > authoritative > aggregator > crowdsourced）的精确定义和 enforcement 力度——当前 [#341](https://github.com/ShadyUnderLight/deep-research-skill/issues/341) 建立了 gate 但具体评级标准可能需要多个案例校准
- "混合 source strength" 场景（如 3 个 primary + 5 个 Wikipedia）的通过标准——当前以 100% Wikipedia 为极限基准，但混合场景的阈值需要更多案例确定
- "traceability theatre" 的自动检测——当前依赖人工 review 发现 source strength 问题，自动化检测（如扫描所有 register 条目的域名/类型）可作为未来的硬门

### Is this mainly a missing rule, missing trigger, or execution problem?
- **Source strength gate**: Missing rule（无 source strength 作为独立审计维度）→ 已由 [#341](https://github.com/ShadyUnderLight/deep-research-skill/issues/341) 新增
- **"Claims Supported" granularity**: Missing rule（无 claim-level mapping 要求）→ 已由 [#341](https://github.com/ShadyUnderLight/deep-research-skill/issues/341) 新增
- **Numeric role labels**: Execution problem（规则存在但未触发）→ 已由 [#341](https://github.com/ShadyUnderLight/deep-research-skill/issues/341) 通过 source-strength gate 间接改善
- **Route conflict check**: Execution/wiring problem（route boundary 检查未触发）→ 已由 [#340](https://github.com/ShadyUnderLight/deep-research-skill/issues/340) 修复

**混合类型：** 该对比暴露了两个核心缺失规则（source strength gate + Claims Supported granularity）和一个触发缺口（route conflict check）。均已修复。

---

## Minimal quality bar

- [x] the two reports are comparable enough to justify distillation
- [x] the comparison used the six fixed dimensions
- [x] each accepted candidate has an action type
- [x] each accepted candidate has a proposed repo home
- [x] at least one rejected observation is documented when relevant
- [x] the final judgment distinguishes rule gap vs trigger gap vs execution gap
