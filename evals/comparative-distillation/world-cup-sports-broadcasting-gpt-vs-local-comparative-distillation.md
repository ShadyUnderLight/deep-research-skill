# World Cup Sports Broadcasting Market Outlook GPT-vs-Local Comparative Distillation

> **目的：** 将 GPT 深度研究版与本地 deep-research-skill 版对 2026 年世界杯体育转播市场前景同一问题的 paired-report 对比固化为回归资产。这是首个在 market-outlook route 中追踪 citation 格式 vs. source 质量分离的对比案例——本地版具有完整 body `[Sxx]` 内联引用和 7 列 Source Register，但 source pool 以 Wikipedia/众包为主。同时暴露了 "structurally complete, gate-level fail" 模式（结构完美但各 section 的内部执行合约不达标）。所有 gap 已由 Phase A/B 覆盖。

---

## Case identity

- **Case name:** World Cup Sports Broadcasting Market Outlook GPT-vs-Local Comparative Distillation
- **Date:** 2026-06-29
- **Research question:** Can broadcasting rights holders and streaming platforms use the 2026 World Cup to prove that live sports remains a high-value asset?
- **Why this comparison matters:**
  - 本地版拥有完整的 market-outlook 结构（snapshot、drivers/blockers、三个 scenarios、stakeholder 表、monitoring signals、body `[Sxx]` 内联引用），但 source pool 以 Wikipedia/crowdsourced 为主——load-bearing claims（FIFA 营收、平台投资、市场估值）依赖 tertiary sources。
  - 这是 **structurally complete, gate-level fail** 的极限基准：所有 mandatory sections 都存在，但大多数 sections 未满足其内部执行合约（monitoring 无 actionability、scenarios 无 shared axis、forward-looking numbers 无 sourcing、evidence labels 与 source strength 不匹配、self-assessment overclaim）。
  - Scenario axis drift（base=revenue, bull=viewership, bear=platform competition）——这是首个在 market-outlook route 中追踪此失败模式的案例。
  - 对比触发或引用了 Phase A/B 的所有主要 issue：source-strength gate（#341）、route wiring（#340）、Decision Scope（#309）、rule-system add-on（#343）、scenario shared-axis 合约测试（#355 Phase B）。
- **Report A:** GPT 深度研究版（更清晰的 stakeholder 划分、KPI 框架、结构化 case studies：Peacock/Netflix/DAZN/区域版权、分 stakeholder + horizon 的策略建议、更好的 forward-looking horizon 分离）
- **Report B:** 本地 deep-research-skill 版（结构化 market-outlook 报告：快照→驱动/阻碍→三种情景→利益相关者→监测信号→自评；body `[Sxx]` 内联引用、7 列 Source Register、counter-evidence、stakeholder actionability table；但 source pool 以 Wikipedia 为主、monitoring 信号纯定性、scenarios 缺乏 shared axis、forward-looking numbers 缺 sourcing 和 role label、evidence labels 与 source strength 不匹配、self-assessment overclaim）
- **Reference / stronger report (if any):** GPT 深度研究版（stakeholder-specific KPI 框架和 horizon-based 策略规划更强，但 citation 格式不可用于仓库）
- **Prompt(s):** 相同研究问题，两份报告均使用 deep-research style
- **Important scope or timing differences:**
  - 本地版正确选择了 `market-outlook` 路由（内容负担符合 market direction/trajectory）
  - 两份报告完成时间不同，但此对比聚焦结构性差异而非时效性差异
  - 对比焦点：source strength 纯度、monitoring actionability、scenario shared-axis 纪律、forward-looking number 纪律、evidence label 校准、self-assessment 诚实性

---

## Comparison purpose

This comparison is **not** for deciding which model is "better."

It is for:

1. 确认 "structurally complete, gate-level fail" 模式（所有 market-outlook mandatory sections 存在但 section 内部执行合约未满足）是否已被 Phase A/B 的 checklist gates 覆盖
2. 确认 source-strength gate（#341）是否覆盖 load-bearing claims 依赖 Wikipedia/crowdsourced 的问题
3. 确认 monitoring actionability hard-fail gate（`checklists/market-outlook-audit.md` §Monitoring signal actionability hard-fail gate）是否覆盖纯定性 monitoring 问题
4. 确认 scenario shared-axis 规则（`checklists/market-outlook-audit.md` §Structured multi-scenario analysis）和 Phase B 合约测试（#355）是否覆盖 scenarios 跨 metric drift 问题
5. 确认 forward-looking claim 纪律（`checklists/market-outlook-audit.md` §Forward-looking label hard-fail gate）是否覆盖精确百分比无 sourcing/role label 的问题
6. 确认 evidence-label calibration（间接通过 #341 source-strength gate）是否覆盖 confirmed fact tags 在 secondary source 上的误用
7. 将 "body [Sxx] present but source pool Wikipedia-heavy" 作为 market-outlook route 的 traceability-theatre 基准固化为回归资产

**Because all identified gaps have already been addressed by closed issues and checklist gates in Phase A/B, this file serves primarily as a regression audit asset rather than a gap-discovery artifact.**

---

## Dimension 1: Current-state discipline

### Report A (GPT)
- Better stakeholder segmentation: cleanly separates rights holders / streaming platforms / advertisers / fans into distinct analytical units
- Clear KPI framework across stakeholder types: rights cost, concurrency, watch time, CPM, CAC, ARPU, retention, piracy, infrastructure cost
- Structured case studies (Peacock for WWE/EPL, Netflix for NFL Christmas games, DAZN for boxing/global rights, regional rights market snapshots)
- Horizon-aware current-state: distinguishes near-term (2026 buildup) from medium-term (rights cycle renewal) and long-term (structural platform shift)

### Report B (Local)
- ✅ Current snapshot present: market size context (global sports broadcast market, FIFA revenue) with [Sxx] citations
- ✅ Drivers and blockers separately identified (5 drivers, 4 blockers) with role labels
- ✅ Stakeholder types identified: rights holders, streaming platforms, advertisers, fans (4 types, meeting the ≥3 minimum)
- ❌ Current snapshot relies on Wikipedia-sourced market-size numbers for load-bearing claims (FIFA revenue cited from Wikipedia)
- ❌ Stakeholder segmentation has less granularity than GPT—the "streaming platforms" category doesn't distinguish between tech-first (Netflix/Amazon) vs media-first (DAZN/ESPN+) vs carrier-first (Telstra/Sky) business models
- ❌ No explicit KPI framework that maps metrics to stakeholders (e.g., "CPM matters for advertisers, retention for platforms, rights cost for broadcasters")

### Gap
- 两份报告在 current-state discipline 上都有足够的结构，但 GPT 版的 KPI framework 和 stakeholder-specific metric mapping 更精细
- 本地版的缺失不是规则缺口——`checklists/market-outlook-audit.md` §Stakeholder implications 和 §Commercialization/Pricing check 已经覆盖了 stakeholder 分层和指标纪律
- 本地版对 current-state 的执行质量足够通过条件性通过（conditional pass），核心问题在于 source strength 而非 current-state 结构

### Candidate action
- `NO_ACTION` — checklist 已经覆盖 stakeholder segmentation 和 quantitative discipline 要求。GPT 版的 KPI framework 是 domain-specific 执行选择，不是通用规则缺口。本地版的 source strength 问题由 #341 解决。

### Action type
`NO_ACTION`

---

## Dimension 2: Numerical and date discipline

### Report A (GPT)
- KPI framework provides explicit numeric dimensions for each stakeholder (rights cost per match, concurrency peaks, watch time per user, CPM rates, CAC/LTV ratios, ARPU trajectory, retention curves, piracy leak %, infrastructure cost per TB)
- Horizon-based numerical structure: near-term metrics vs medium-term vs long-term structural shifts
- Case studies anchor numbers to real platform experiences (Peacock's WWE concurrent peak, Netflix's NFL Christmas Day viewership)
- Lacks numeric role labels (observed / proxy / assumption / model-output) per warehouse standard

### Report B (Local)
- Body has numerical content: market size (global sports broadcast market ~$XXB), FIFA revenue, platform investment figures, rights fee comparisons
- Scenario probabilities stated precisely: `~60/25/15%` for base/bull/bear
- Revenue thresholds: `>40%`, `<$1B`, `>15%` without estimation method or confidence interval
- ❌ **Numeric role labels missing** — precise-sounding percentages lack observed/proxy/assumption/model-output labels
- ❌ **Estimation method opaque** — `~60%` probability is not self-evident; no exposition of whether this is analyst consensus, model output, or author judgment
- ❌ **Precise thresholds treated as given** — `>40%` rights cost ratio as scenario trigger without explaining how 40% was derived
- ❌ Source weakness compounds numeric weakness: market-size numbers cite Wikipedia, so even if role labels existed, the source strength wouldn't support load-bearing numerical claims

### Gap
- 本地版的核心问题：precision without provenance——精确的百分比和阈值（~60%、>40%、<$1B）看起来像 quantitative discipline，但缺少 estimation method、confidence boundary、role label
- GPT 版虽然没有显式 role labels，但其 numerical claims 通过 case study 和经验锚定（Peacock 的真实并发、Netflix 的实际观看量）提供了隐性 provenance
- `checklists/market-outlook-audit.md` §Quantitative role labeling 和 §Forward-looking label hard-fail gate 已经覆盖此 gap
- Source-strength gate（#341）间接要求：基于低强度 source 的数字必须标注 role 和 uncertainty

### Candidate action
- `NO_ACTION` — #309 的 Decision Scope 块和 `checklists/market-outlook-audit.md` §Quantitative role labeling 的 declared-not-executed hard-fail 已经覆盖角色标签和执行检查。Forward-looking label hard-fail gate 明确禁止精确百分比无 sourcing。本地版的 precision-without-provenance 模式如出现在 future 报告中将被这些 gate 捕获。

### Action type
`NO_ACTION`

---

## Dimension 3: Source traceability and evidence weighting

### Report A (GPT)
- Body has claim-level citations but in GPT-proprietary format (not auditable within repo)
- Stakeholder-specific sourcing: rights costs from financial filings, viewership from platform disclosures or Nielsen, market size from industry analysts
- Sourcing is stronger per-claim than Report B even though format is incompatible—the underlying sources are more authoritative
- No 7-column Source Register, no route/audit status modules

### Report B (Local)
- ✅ Body `[Sxx]` inline citations present (unlike earlier zero-citation market-outlook failures)
- ✅ 7-column Source Register with URL, source type, key claims, evidence strength
- ✅ Zero register inflation (all registered sources cited in body)
- ❌ **Wikipedia/crowdsourced dominant** — load-bearing claims about FIFA revenue, platform financials, and market valuations cite Wikipedia or secondary media aggregators as their primary source
- ❌ **Evidence labels inconsistent with source strength** — secondary/crowdsourced sources tagged as `[CONFIRMED]` or equivalent confirmed-fact labels, inflating evidence weight beyond what the actual source type can bear
- ❌ **No explicit evidence-label calibration rule** — labels exist (confirmed fact / inference / unknown) but their assignment is disconnected from source-type classification

### Gap
- 核心发现：**traceability theatre 扩展到 market-outlook route** — body `[Sxx]` 和 Source Register 格式完整，但 source pool 不足以支撑 load-bearing claims
- 这是首个 market-outlook 案例，同时暴露了两个失败模式：
  1. Citation format vs. source quality separation（以前的 case 测试 citation 缺失，本 case 测试 citation 存在但 source 不合适）
  2. Evidence label inflation 从 listed-company 扩展到 market-outlook（confirmed fact 标签被贴在 crowdsourced 来源上）
- Source-strength gate（#341）直接解决了 source pool 问题：load-bearing claims 需要 primary/authoritative source，Wikipedia 被标记为 crowdsourced 级别

### Candidate action
- `NO_ACTION` — #341 的 source-strength gate 间接要求证据标签反映 source 可靠性（crowdsourced source 不能支持 load-bearing claims，因此也不能标为 confirmed fact）。Process-integrity gate 防止全 ✅ 自评当 source strength 不满足。证据标签问题主要是执行问题而非规则缺口——如果 source strength gate 严格执行，evidence label inflation 自然被预防。

### Action type
`NO_ACTION`

---

## Dimension 4: Forward-looking claim discipline

### Report A (GPT)
- Strategy organized by stakeholder + horizon: short-term (2026 buildup), medium-term (rights cycle 2027–2030), long-term (structural platform shift)
- Case studies anchor forward-looking claims in actual platform trajectories (Peacock from WWE to EPL to broader rights; Netflix from NFL experiment to potential annual sports package)
- Explicit uncertainty communication: "direction is clear, magnitude depends on..."
- Differentiates structural predictions (rule/rights-cycle-driven) vs situational predictions (match-specific, team-specific)

### Report B (Local)
- Three scenarios present: base, bull, bear with narrative descriptions
- Scenario probabilities: `~60/25/15%` — precise but without estimation method, named source, or role labels
- Revenue thresholds: `>40%` rights cost ratio, `<$1B` investment floor, `>15%` growth cut — specified as scenario triggers without derivation explanation
- ❌ **No role labels on forward-looking numbers** — scenario probabilities and revenue thresholds should carry role labels (estimate / scenario-assumption / inference / model-output)
- ❌ **No confidence calibration** — ~60% base case probability implies 60% confidence weight, but no uncertainty band, sensitivity context, or condition-dependent variation

### Gap
- 本地版的核心问题：精确但不透明——`~60/25/15%` 看起来是严肃的情景权重，但读者无法判断这是来自量化模型、分析师共识、还是作者的个人判断
- `checklists/market-outlook-audit.md` §Forward-looking label hard-fail gate 明确要求：前瞻数字必须使用 estimate / scenario-assumption / analyst estimate 等标签，给出来源 attribution 和时间 basis，且同一报告中 >3 处违规即触发 hard-fail
- #309 的 Decision Scope 块要求列出改变结论的条件

### Candidate action
- `NO_ACTION` — checklists 中的 forward-looking label hard-fail gate 和 Decision Scope 块（#309）已经覆盖。% 精度无 sourced 的问题将被 forward-looking gate（阻断级）捕获。

### Action type
`NO_ACTION`

---

## Dimension 5: Structural readability and information density

### Report A (GPT)
- Clear stakeholder-driven structure: segmentation → KPI framework → case studies → horizon-based strategy
- Case studies serve dual purpose: evidence for current-state + anchor for forward-looking claims
- KPI framework creates consistent analytical lens across all sections
- Information density high per section—each paragraph carries specific stakeholder relevance

### Report B (Local)
- ✅ Structural completeness: snapshot → drivers/blockers → three scenarios → stakeholder table → monitoring signals → self-assessment
- ✅ Counter-evidence section present
- ✅ Stakeholder actionability table present with concrete recommendations
- ❌ **Scenarios not bound to shared quantitative axis** — base scenario anchored in revenue metrics, bull in viewership metrics, bear in platform competition narrative. Reader cannot compare scenarios quantitatively.
- ❌ **Monitoring signals purely qualitative** — 7 reversal signals listed but none meet 4-field actionability requirement (threshold + cadence + source + trigger-to-action)
- ❌ **Evidence labels inconsistent** — confirmed fact tags on secondary sources reduce trust in evidence architecture
- ❌ **Self-assessment overclaim** — source-traceability, market-outlook, forward-looking, final-audit all claimed ✅ while source-strength gate fails, monitoring hard-fail triggers, and forward-looking numbers lack sourcing

### Gap
- 本地版暴露了 **"structurally complete, gate-level fail"** 模式：报告拥有所有 market-outlook 的 mandatory sections（这是进步），但不满足各 section 的内部执行合约
- Scenario axis drift 被 checklist 明确禁止（"all scenarios share the same load-bearing metric"）并已通过#355 Phase B 合约测试覆盖
- Monitoring actionability 被 checklist 的 monitoring signal actionability hard-fail gate 覆盖
- Self-assessment overclaim 被 process-integrity gate（#341）覆盖

### Candidate action
- `NO_ACTION` — Phase B 合约测试（#355）和 market-outlook-audit checklist 的所有相关 gate 已覆盖本维度的所有 gap。

### Action type
`NO_ACTION`

---

## Dimension 6: Decision usefulness

### Report A (GPT)
- Stakeholder-specific recommendations: what rights holders should do (bundle/ unbundle/ tier), what streaming platforms should invest in (infra/ exclusive content/ personalization), what advertisers should watch (CPM trends/ demo shift/ piracy impact)
- Horizon-based action framework: near-term anchor plays, medium-term structural bets, long-term position building
- Case studies provide concrete reference points: "Peacock did X, achieved Y" — actionable because replicable
- KPI framework gives decision-makers a measurement lens to evaluate their own position

### Report B (Local)
- ✅ Stakeholder actionability table present with concrete recommendations per type
- ✅ Counter-evidence and reversal conditions enhance decision trust
- ✅ Bottom-line judgment clear and defensible
- ❌ **Decision usefulness undermined by source weakness** — a broadcaster considering a rights bid cannot confidently base their decision on a report whose FIFA revenue figures come from Wikipedia
- ❌ **Monitoring signals not actionable** — decision-maker cannot operationalize "watch platform investment levels" without a measurable threshold, cadence, and trigger-to-action
- ❌ **Scenario axis drift reduces comparative usefulness** — reader cannot decide "which scenario am I in?" if each scenario measures different things

### Gap
- 本地版在分析内容质量上值得 conditional pass，但 source weakness、monitoring non-actionability 和 scenario axis drift 共同降低了决策有用性
- 决策有用性是三个独立缺口的叠加效应，而非单一问题
- GPT 版的 decision usefulness 优势来自两个维度：更好的 source selection（直接来自平台财报）和更好的 scenario anchored metrics
- 所有三个缺口已有规则覆盖：source strength（#341）、monitoring actionability（checklist gate）、scenario shared axis（checklist + Phase B）

### Candidate action
- `NO_ACTION` — 决策有用性缺口是其他维度缺口的症状而非独立问题。Source strength gate、monitoring actionability gate 和 scenario shared-axis 规则同时修复后，决策有用性自然提升。

### Action type
`NO_ACTION`

---

## Candidate-action summary

| # | Candidate action | Failure family | Action type | Proposed home |
|---|---|---|---|---|
| 1 | Source-strength gate for market-outlook | source-traceability / evidence-weighting | `NO_ACTION` | Already closed by #341 |
| 2 | Monitoring signal actionability — 4-field requirement | monitoring / actionability | `NO_ACTION` | Already covered by `checklists/market-outlook-audit.md` |
| 3 | Scenario shared-axis discipline | structural / scenario-discipline | `NO_ACTION` | Already covered by `checklists/market-outlook-audit.md` + Phase B (#355) |
| 4 | Forward-looking number sourcing | forward-looking / claim-discipline | `NO_ACTION` | Already covered by `checklists/market-outlook-audit.md` + #309 |
| 5 | Evidence label calibration | evidence-weighting | `NO_ACTION` | Indirectly covered by #341 source-strength gate |
| 6 | Self-assessment honesty | process-integrity | `NO_ACTION` | Already closed by #341 |

**Summary: All 6 candidate actions are `NO_ACTION` — all gaps identified in this paired comparison are covered by Phase A/B issues or existing checklist gates.**

---

## Triage notes

### Action type distribution in this artifact

All six dimensions evaluate to `NO_ACTION` because every identified gap has been addressed by Phase A/B issues. No `NEW_RULE`, `CHECKLIST_HARDENING`, `TEMPLATE_CHANGE`, or `VALIDATOR_OR_TEST` candidates emerged — the gap-closure work (source-strength gate #341, scenario shared-axis #355, monitoring actionability gate, forward-looking discipline #309) was comprehensive.

### Why all candidates are NO_ACTION

Each gap identified in this paired-report comparison has been systematically addressed by Phase A/B of the #353 workstream. This distillation exists to:

1. **Establish "structurally complete, gate-level fail" as a documented failure pattern** — this is the first market-outlook eval case with all mandatory sections present but multiple section-level execution failures
2. **Document "body [Sxx] + Wikipedia source pool" as traceability-theatre in market-outlook** — extends the traceability-theatre finding from technical-deep-dive to market-outlook route
3. **Provide a regression baseline** — if a future market-outlook report has body [Sxx] citations and 7-col Source Register but all sources are Wikipedia for load-bearing claims, that is a regression
4. **Distinguish rule gaps from execution gaps** — all six dimensions were a mix of missing rules (source-strength, monitoring actionability, scenario axis) and execution gaps (evidence labels, forward-looking roles). All now covered.

---

## Things explicitly rejected

| Observation | Why rejected |
|---|---|
| GPT 版 stakeholder-specific KPI framework 应强制作为 market-outlook template 的一部分 | KPI framework 是 domain-specific 的行业分析工具，不是通用 market-outlook 模板组件。不同市场（如 AI agent 市场、半导体市场、电商市场）需要完全不同的 KPI set。 |
| 本地版应废弃 | 本地版在 content quality 上值得 conditional pass。问题在 section-level gate execution 不在 content quality。当前规则修复后，同样内容负担的报告将同时具备结构纪律和执行纪律。 |
| 应新增 explicit "evidence label ↔ source type calibration" 规则 | Source-strength gate（#341）已间接解决。如 future case 再次出现 source-strength gate 通过但 evidence-label inflation 单独失败的情况，再考虑独立规则。 |
| GPT 版不可审计的 citation 格式说明 GPT 更好 | 仓库规则要求 body `[Sxx]` 和 7-col Source Register。GPT 版格式不兼容。此对比聚焦结构纪律和 gate execution。 |
| Monitoring 信号的 4-field actionability 要求过高 | 对于 market-outlook dashboard，纯定性的 "watchlist" 无法支撑决策。≥3 个信号满足 4-field 不是过度要求。 |

---

## Final judgment

### What the stronger report did better
- **Stakeholder segmentation**: GPT 版更精细地划分了 rights holders / streaming platforms / advertisers / fans，且每个 stakeholder 有专属的 KPI lens
- **Case study anchoring**: Peacock（WWE/EPL）、Netflix（NFL Christmas）、DAZN（boxing/global）等案例使 forward-looking claims 有可参考的锚点
- **Horizon separation**: 短期（2026 前）、中期（2027–2030 版权周期）、长期（结构性平台转型）的分离使策略建议更具体

### What should change in the repo now
- ✅ 全部 gap 已通过 Phase A/B 覆盖：
  - #341: Source-strength gate + process-integrity gate
  - #309: Decision Scope block for forward-looking claims
  - #355 Phase B: Scenario shared-axis contract tests
- `checklists/market-outlook-audit.md` 已包含 monitoring actionability hard-fail gate、forward-looking label hard-fail gate、scenario shared-axis rule
- 本文件作为 regression 基线

### What should wait for another confirming case
- **Evidence-label calibration 显式规则**：当前由 source-strength gate 间接覆盖。如果 future market-outlook 报告通过 source-strength gate 但仍出现 evidence-label inflation，应考虑新增显式规则。
- **KPI framework 作为 market-outlook 的 recommended section**：如果 future market-outlook 报告再次因缺少 stakeholder-specific KPI mapping 而降低决策有用性，应考虑在 market-outlook 模板中增加 optional "KPI framework by stakeholder" 建议。

### Is this mainly a missing rule, missing trigger, or execution problem?
- **Source strength for load-bearing claims**: Missing rule → 已由 #341 新增 source-strength gate
- **Monitoring signal actionability**: Missing rule → 已由 `checklists/market-outlook-audit.md` 新增 monitoring actionability hard-fail gate
- **Scenario shared-axis discipline**: Missing rule → 已由 `checklists/market-outlook-audit.md` + #355 新增
- **Forward-looking number sourcing**: Missing rule → 已由 `checklists/market-outlook-audit.md` + #309 新增
- **Evidence-label calibration**: Execution problem — source-strength gate 已间接覆盖
- **Self-assessment overclaim**: Execution problem — process-integrity gate（#341）已新增

---

## Minimal quality bar

- [x] the two reports are comparable enough to justify distillation
- [x] the comparison used the six fixed dimensions
- [x] each accepted candidate has an action type
- [x] each accepted candidate has a proposed repo home
- [x] at least one rejected observation is documented when relevant
- [x] the final judgment distinguishes rule gap vs trigger gap vs execution gap
