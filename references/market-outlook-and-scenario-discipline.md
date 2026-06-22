# Market Outlook and Scenario Discipline

Use this reference when the task asks how a market, category, product class, or industry is likely to evolve over the next 6-24 months.

Typical triggers:

- "未来12个月如何演化"
- "未来一年会怎么变"
- market outlook
- industry evolution
- adoption trajectory
- category forecast
- strategic outlook for buyers / operators / investors

---

## Core rule

Do not answer these tasks as generic industry overviews.

The output should function as a **decision memo about a changing market**.

That means the report must make visible:

- the current baseline
- what is changing now
- what drives change
- what blocks change
- what the base case is
- what alternative scenarios exist
- who should act now
- what to monitor that would change the view

If the report mostly explains the topic but does not help the reader act under a time horizon, it has drifted.

---

## When not to use this route

Market Outlook is for understanding **direction, evolution, and trajectory**. It is not for **choosing, ranking, or recommending**.

Do not use this route when:

- the task's core output is a **recommendation** among defined options → use Constrained Choice / Shortlist
- the task requires **ranking** entities or options → use Constrained Choice / Shortlist
- the task asks **"which one should we pick?"** → use Constrained Choice / Shortlist, Provider Selection, or Equipment Selection depending on domain
- the task asks **"who will win?"** in a competition with defined participants → use Constrained Choice / Shortlist

Boundary examples:

| Task | Correct route | Why |
|------|--------------|-----|
| "人形机器人产业链未来 12 个月如何演化" | → Market Outlook | asks for market direction and trajectory |
| "哪支球队最可能夺冠" | → Constrained Choice | asks for ranking/prediction among defined options |
| "应该选哪个 AI 模型供应商" | → Provider Selection | asks for selection under constraints |
| "世界杯足球产业链的商业前景" | → Market Outlook | asks for market evolution, not team ranking |
| "NAS vs 自建服务器怎么选" | → Equipment Selection | asks for procurement recommendation |

If a task mixes market-evolution questions with selection/ranking questions, identify the **primary burden**. If the primary burden is selection or ranking, do not use Market Outlook as the primary route — use the selection route and attach market-outlook discipline as a secondary discipline if market-evolution context is needed.

Refer to `ROUTING-MATRIX.md` "Do not use" clauses for this route before finalizing route selection.

---

## What these tasks are really asking

A market-outlook question is usually not asking:

- "tell me what this market is"

It is usually asking one of these:

- should we enter now or wait?
- what should we buy / build / prioritize now?
- which actors are likely to gain or lose over the next year?
- what assumptions are safe vs fragile?
- what should we monitor because it would change our plan?

Write toward that real decision use.

---

## Required opening structure

Before broader analysis, build a **current market snapshot**.

At minimum, verify and separate when relevant:

- current baseline market state
- current leading products / vendors / architectures
- current pricing, policy, or packaging changes that alter the near-term outlook
- current adoption bottlenecks or enabling infrastructure
- current regulatory or compliance developments
- current evidence date basis

Do not blur:

- current observed facts
- next-12-month scenario logic
- illustrative management or ROI math

These are different evidence layers and should not appear as one undifferentiated narrative.

---

## Required report logic

A strong market-outlook report should usually flow like this:

1. Current market snapshot
2. What matters most
3. Key drivers of change
4. Key blockers / frictions
5. Base case for the stated time horizon
6. Alternative scenarios
7. Stakeholder implications
8. What would change the conclusion
9. Recommended next steps / monitoring signals

This logic matters more than preserving a generic background section order.

---

## Category Boundary / Market Definition（类别边界与市场定义）

Market-outlook 报告必须先声明**这个市场到底包含谁、价值如何流动、谁付钱**。没有类别边界，不同层的参与者（如芯片厂商和 API 聚合平台）会被混入同一张比较表，导致分析失去统一的比较单位。

### 必含结构

#### 1. Category Boundary Table（类别边界表）

必须声明 core category、adjacent categories、excluded categories、comparison unit。一个参与者跨层时，按其主要收入来源所在的业务口径纳入。

| 类别 | 是否纳入核心市场 | 纳入理由 | 不可直接比较项 |
|------|---------------|---------|-------------|
| Research/Search API | 是 | 提供 Agent 外部检索能力 | 查询质量、覆盖、延迟、成本 |
| Model API aggregator | 邻接 | 聚合模型而非研究数据，是上游供应 | 不可直接用模型数量比较搜索基础设施 |
| Agent framework | 邻接 | 编排和调用层，不直接承载索引/抓取 | 架构选择 vs 数据获取能力不属于同类指标 |
| Hardware / chip vendor | 外部驱动 | 影响本地部署成本和可用性 | 算力指标与搜索/API 层的商业指标没有可比性 |

**规则：**
- 不同类别的参与者**不得在缺少 cross-category 说明的情况下直接排名**或混入同一比较表。
- 如果一个参与者跨越多个层（如同时提供 API 和框架），按其**最大收入来源所在业务口径**纳入。
- 如果 core category 本身有多个子类（如检索 API 分为搜索 API、知识图谱 API、结构化提取 API），报告应说明这些子类之间是否可比较。

#### 2. Comparison Unit Discipline（统一比较单位纪律）

当报告需要跨类别比较时，必须声明：

- 使用什么**统一比较单位**（如：同一 customer segment 下的每 query 成本、同一 workload 下的端到端延迟）
- 为什么这个单位在跨类别时仍然有意义
- 当统一比较单位不存在时，不得进行跨类别直接排名

#### 3. 反例：术语定义存在但分类仍然混乱

下面是一个实际触发 #329 的案例（来自 GPT 对比蒸馏）：

> GPT 版同时包含"Research/Search API"和"Model API Aggregator"两类参与者，但在同一个市场规模表中混用了 OpenRouter（API 聚合）、DMXAPI（搜索基础设施）、Parallel.ai（模型编排），导致芯片厂商和 API 聚合平台之间失去统一比较单位。**仅有术语定义不够，需要 category boundary + comparison unit discipline。**

---

## Structured multi-scenario analysis

Market-outlook reports must not rest on a single base case.

Require at minimum:

- **Base case**: the most likely trajectory with quantitative range, key assumptions, and trigger conditions
- **At least one alternative scenario**: a credible divergent path with its own quantitative range, assumptions, and triggers

When uncertainty is material, produce three scenarios:

| Scenario | Label | What it needs |
|----------|-------|---------------|
| Optimistic | Base+ | quantitative range, key assumptions, trigger conditions that would activate it |
| Base | Base | quantitative range, key assumptions, current evidence basis |
| Pessimistic | Base− | quantitative range, key assumptions, trigger conditions that would activate it |

For each scenario:

- state the quantitative range (market size, adoption rate, price trajectory, or other load-bearing metric)
- state the key assumptions that must hold for this scenario to materialize
- state the observable trigger conditions that would signal this scenario is becoming more or less likely

### Scenario quantitative axis consistency

All scenarios must share the **same load-bearing metric** as their quantitative axis. Do not use different metrics across scenarios — the reader must be able to compare all paths on one dimension.

✅ Correct: base "30-40% penetration" / upside "50-60%" / downside "15-25%"
❌ Incorrect: base "user decline 30-50%" / upside "70%+" / downside no equivalent metric

Probability weight annotation is recommended when evidence supports it, but not required. Do not assign precise probabilities when the evidence base cannot support that precision — use directional labels (most likely / upside / downside) or bounded ranges with explicit uncertainty caveats instead of numerical percentages. Precise probabilities are only justified when backed by robust quantitative models or large-sample statistical evidence.

A market-outlook report with only one scenario is not an outlook memo. It is a forecast with no uncertainty structure.

---

## Drivers vs blockers discipline

Do not write a flat list of trends.

Separate:

### Drivers
Forces that accelerate or strengthen the expected trajectory.

Examples:
- cost compression
- workflow integration
- standardization
- regulation clarity
- infrastructure availability
- distribution advantage

### Blockers / frictions
Forces that slow, distort, or cap adoption.

Examples:
- weak evaluation quality
- security risk
- procurement friction
- unclear ROI
- compliance constraints
- workflow change resistance
- missing enterprise controls

If drivers and blockers are not separated, the scenario logic will be too mushy.

---

### Value-chain sensitivity map（产业链主题建议）

当题目包含「产业链」「value chain」「supply chain」「infrastructure chain」时，建议在 drivers/blockers 分析之后包含一张价值链敏感性地图。

**格式模板**

| 链条层级 | 当前暴露程度 | 瓶颈传导机制 | 受益方/受损方 | 影响时间 | 证据强度 | 改变结论的条件 |
|---------|------------|------------|-------------|---------|---------|-------------|
| 上游：... | observed / estimated | 机制说明 | ... | 短期/中期/长期 | high / medium / low | ... |
| 中游：... | ... | ... | ... | ... | ... | ... |
| 下游：... | ... | ... | ... | ... | ... | ... |

**规则：**
- 链条层级一般分为上游（原材料/基础供应）、中游（制造/建设/运营）、下游（应用/消费/服务），可根据题目调整。
- 每个层级至少包含 exposure、bottleneck mechanism、beneficiaries/losers、timing、evidence strength、change-condition。
- 不同层级之间的传导关系应在文字说明中体现，而非仅靠表格。

### Regional coverage matrix（global scope 主题建议）

当报告标题或问题包含「全球」「global」「区域」「region」时，建议包含一张区域覆盖矩阵。这有助于读者理解"全球"是否真的是全球覆盖，还是主要聚焦部分区域。

**格式模板**

| 区域 | 覆盖的关键指标 | 数据角色 | 来源 `[Sxx]` | 是否覆盖 |
|-----|-------------|---------|-------------|---------|
| 北美 | ... | observed / estimate / forecast / scenario / proxy | [S01], [S02] | ✅ |
| 欧盟 | ... | ... | ... | ✅ |
| 中国 | ... | ... | ... | ✅ |
| 印度 | ... | ... | ... | ❌ 未覆盖 |
| 东南亚 | ... | ... | ... | ❌ 未覆盖 |
| 中东/非洲 | ... | ... | ... | ❌ 未覆盖 |

**规则：**
- 数据角色列必须标注角色的认识论分类（observed / estimate / forecast / scenario / proxy）。
- 区域关键数字必须有 `[Sxx]` 正文引用，不能仅靠文末 bibliography。
- 若只覆盖欧美和中国却声称"全球"，必须触发 scope completeness warning：

  > ⚠️ 本报告声称覆盖全球市场，但实际可验证数据仅覆盖 [北美+欧盟+中国] 三个区域，占全球市场约 [X]%。建议在题目或范围声明中明确限定覆盖区域。

- 区域选择不是固定的——应根据题目涉及的产业链和市场规模合理选择对比区域（例如数据中心电力主题至少覆盖北美、欧盟、中国、东南亚、中东）。

**不触发条件**：报告 scope 已明确声明聚焦特定区域（如"中国市场"、"全球视角偏重欧美"）且标题/问题不含"全球"等全貌措辞。

---

### Participant Value-Chain Map（参与者价值链地图）

当报告涉及多类参与者（聚合平台、Agent 平台、模型提供商、云厂商、硬件、开源社区、搜索 API）及其价值流动时，建议在 drivers/blockers 分析后包含一张参与者价值链地图，补充上述产业链敏感图。

**与 Value-chain sensitivity map 的区别：**
- 产业链敏感图聚焦**供应-制造-交付**的物理/技术链条，适用于"芯片短缺如何影响服务器交付"这类问题。
- 参与者地图聚焦**价值创造-捕获-流动**的经济链条，适用于"API 聚合平台能否从搜索基础设施中独立盈利"这类问题。
- 两者可以共存：产业链主题优先用敏感图，市场结构主题优先用参与者地图。当话题同时涉及两者时，两张图都应包含。

**格式模板**

| 链条层级 | 参与者类别 | Value Capture | Bottleneck | 依赖关系 | 被吸收/取代风险 | 证据强度 |
|---------|-----------|-------------|-----------|---------|--------------|---------|
| 上游：数据/索引/内容权利 | 数据供应商、索引运营商、内容许可方 | 内容许可费、数据订阅 | 高质量数据获取成本 | 下游检索层依赖其索引覆盖 | 被模型训练数据自动化取代 | medium |
| 搜索/抓取/提取与结构化 | 搜索 API、抓取平台、知识图谱 API | 按 query / page / token 收费 | 实时性、反爬、多语言覆盖 | 依赖上游数据权利和索引质量 | 被 model-native knowledge 吸收 | medium |
| API 聚合/路由 | API 网关、聚合平台、负载均衡 | 按 token / query 抽佣或加价 | 模型 API 定价波动、延迟 | 依赖模型层和搜索层 API | 被云厂商内置路由取代 | high |
| Agent 编排与模型层 | Agent 框架、模型 API、微调平台 | Seat 订阅、token 消耗、按结果付费 | 准确率、幻觉控制、企业集成 | 依赖搜索层获取外部知识 | 被模型原生工具调用吸收 | medium |
| 企业分发/集成 | 企业应用市场、SaaS 平台、咨询集成商 | 实施费、年度合同、SaaS 订阅 | 企业采购周期、合规审核 | 依赖下游 Agent 和模型层稳定性 | 被 SaaS 平台内置 Agent 功能取代 | low |
| 客户与付费方 | 企业 buyer、个人开发者、云账户 | 按用量/座位/合同付费 | 付费意愿、预算归属 | 所有上层依赖 customer adoption | — | observed |

**规则：**
- 每层必须标注 value capture 方式（谁收什么费）、bottleneck（约束该层扩张的主要因素）、dependency（依赖哪些下层的稳定性和质量）、absorption risk（该层功能被其他层内置/取代的风险）。
- 层之间的价值传导关系应在正文中说明，而非仅靠表格。
- 所有关键商业数字必须有角色标注和 `[Sxx]` 来源引用。

---

## Quantitative outlook discipline

When using numbers in market-outlook reports, label each important number by role.

Use categories like:

- **Observed current metric**
- **Inferred estimate**
- **Scenario assumption**
- **Illustrative calculation**

This matters because market-outlook reports are especially vulnerable to synthetic precision.

Examples:

- Current paid-seat estimate -> may be inferred from public pricing and adoption evidence
- Next-year ARR path -> usually scenario logic, not reported fact
- ROI example -> usually illustrative calculation, not externally verified realized return

Readers should never have to guess which kind of number they are reading.

---

## Stakeholder implications discipline

Do not stop at "the market will likely do X."

State who that matters for.

Cover **at least 3 distinct stakeholder types**. Investor-only coverage is not sufficient.

Common stakeholder lenses:

- investors / operators / procurement teams
- builders / startups / product teams
- vendors / channels / ecosystem partners
- technology developers / platform teams
- policymakers / regulators
- enterprise buyers / CTOs
- end users / consumers

For each covered stakeholder type, provide a dedicated subsection that answers:

- what does this market change mean for them?
- who should act now, and what should they do?
- what should they avoid overcommitting to?
- what should they monitor next?

Do not collapse all stakeholder implications into a single investor-focused paragraph. Each stakeholder type has different decision horizons, risk exposures, and action requirements.

Without multi-stakeholder coverage, the report may be informative for one audience but fails as a decision-useful market memo.

### 推荐结构：Stakeholder action table

当报告涉及实施决策、成本投入、组织变更时，建议将 stakeholder 影响从"方向性描述"升级为 action table：

| Stakeholder | Decision to make | Recommended action | Required evidence / metric | Trigger to revise |
|---|---|---|---|---|
| [角色] | [需要做的决策] | [推荐行动] | [约束条件 / 关键指标] | [什么假设变化会改变推荐] |

示例：

| Stakeholder | Decision to make | Recommended action | Required evidence / metric | Trigger to revise |
|---|---|---|---|---|
| 业务 Owner | 是否全面接入 AI Agent | 先启动 MVP 试点（1 个团队，3 个月） | 客服响应时间改善 >30% 且成本不增加 >15% | 试点 3 个月后效果未达标 → 回到部分接入方案 |
| 数据/知识 Owner | 数据清洗与知识库优先级 | 优先打通 CRM+BI 系统数据管道 | 数据覆盖率 >80% 的渠道数 | 关键工单系统 API 不可用 → 调整 MVP scope |
| AI 运营 Owner | 选型：集中式 Agent vs 微代理 | 部署分布式微代理 + 人工兜底 | 单 Agent 准确率 >85%，兜底率 <10% | 运维人力需求超预期 → 增加集中管理面板 |

**规则：**
- 每个 stakeholder 的行动建议必须是具体的、可检查的，而不是"关注趋势"。
- "Trigger to revise"列必须包含具体阈值或条件。
- 该表不替代现有"what does this mean for them"描述性段落——可以在描述性段落后附加该表，或直接用表格替代描述。

---

## Demand Segmentation（需求细分）

当市场明显异质（不同 buyer 群体有显著不同的购买动机、使用场景、价格敏感度）时，报告必须显式拆分需求维度，而不是用一个泛化的"市场需求"替代。

### 至少覆盖两个细分维度

常用维度（选择与当前市场最相关的两个或以上）：

| 维度 | 细分类型 | 示例 |
|------|---------|------|
| 行业监管强度 | 受监管 vs 未受监管 | 金融/医疗 vs 创意/零售 |
| 企业规模/技术能力 | 大企业 vs SME vs 个人开发者 | 自建 vs 采购 vs 使用免费工具 |
| 地域/数据主权 | 数据驻留要求强 vs 弱 | 欧盟 GDPR 区域 vs 其他区域 |
| Workload 类型 | 简单搜索 vs 复杂研究 vs 结构化提取 vs 企业知识富化 vs 本地 Agent | 不同 workload 对应不同的 buyer 和技术要求 |

### 每 segment 的输出要求

每个 selected segment 必须回答：

- **Job-to-be-done / 使用场景**：这个 segment 的用户想完成什么任务？
- **购买者身份**：决策者是谁（CTO/业务线/个人开发者）？采购流程多长？
- **付费意愿 proxy**：用什么信号衡量购买意愿（PoC request、RFP 数量、GitHub star、API 调用量增长）？
- **部署要求**：SaaS / on-prem / hybrid / edge / 本地？
- **证据强度**：该 segment 的分析有多少基于 observed data，多少基于推断/假设？

### 通用规则

- 不同 segment 之间不可使用同一套 metrics 直接排名——每个 segment 有独立的成功标准和购买逻辑。
- 如果报告只覆盖一个 segment，必须显式声明 scope 限定，不得以"市场整体"自称。
- 关键商业数字必须有角色标注和 `[Sxx]` 来源引用。

---

## Commercialization / Pricing Layer（商业化与定价层）

市场展望不能只写技术趋势和融资列表。必须说明**价值如何被捕获、谁付钱、商业闭环如何成立**。

### 必含元素

#### 1. Buyer identification（谁付费）

明确谁是真实 buyer（不是受益者，是掏钱的人），包括：
- 预算归属（IT 预算 / 业务线预算 / 研发预算 / 个人账户）
- 采购单位（团队 / 部门 / 企业 / 个人）
- 决策链条（自下而上 vs 自上而下 vs 个人采购）

#### 2. Pricing unit / model（定价单位与模式）

覆盖市场中存在的定价模式：

| 模式 | 适用场景 | 对毛利的影响 |
|------|---------|------------|
| Per query / per token | API、搜索服务 | 低毛利但弹性好，边际成本随用量下降 |
| Per seat / per user | Agent 平台、企业 SaaS | 高毛利但扩散慢，依赖用户增长 |
| Annual contract / enterprise license | 大型企业部署 | 高确定性但销售周期长 |
| Consumption / usage-based | 云市场、按量付费 | 随 adoption 增长，但 unit economics 依赖留存 |
| Freemium / open-core | 开源商业化、开发者工具 | 低转化率但社区扩散快 |

#### 3. Unit economics 的主要变量

至少识别以下变量中的 2-3 个：
- **获客成本**（CAC）：销售团队 vs 自服务 vs 渠道
- **客单价**（ARPU / ACV）：受 segment 和部署模式影响
- **毛利**（Gross margin）：基础设施成本 vs 软件利润率
- **留存/续费**（Retention）：Net Revenue Retention 是独立基础设施的关键指标
- **规模效应**：边际成本是否随规模下降

#### 4. 验证指标（Validation metrics）

声明什么商业指标能验证该独立层成立：

- **ARR / Revenue growth**：收入绝对值和增长率
- **Gross margin**：独立基础设施 vs 模型内置功能的利润比较
- **Enterprise contract count**：企业级合同数量和平均合同额
- **Multi-model / multi-provider usage**：用户使用超过一个供应商的比例（验证聚合层价值）
- **付费 query / token mix**：付费 vs 免费使用比例

#### 数字角色纪律

所有商业化数字必须标注角色（observed / estimate / assumption / scenario / proxy）和 `[Sxx]` 来源引用。

> ✅ 正确："企业 ARR 在 2026 年达到约 $50M（estimate，基于公开收入披露 [S03] 和销售团队规模推断 [S07]）"
> ❌ 错误："企业 ARR 在 2026 年达到 $50M"

---

## Regulatory-to-Business Transmission（监管影响传导）

监管章节必须有实质内容，不能只列法规名称。必须解释**法规变化如何影响具体的商业变量**。

### 必含传导路径

每项识别的监管因素都必须连接至少 2 个以下商业变量：

| 监管因素 | → 影响哪个商业变量 | → 传导机制 | 证据强度 |
|---------|------------------|-----------|---------|
| 数据出境法规 / GDPR / 数据本地化 | 部署模式选择（SaaS vs on-prem vs hybrid） | 数据本地化要求 → 增加本地部署成本 → 影响产品定价和交付策略 | medium |
| AI 责任 / 可解释性要求 | 销售周期长度、企业合同通过率 | 合规审核流程增加 → 延长 PoC 到生产的时间 → 影响收入确认节奏 | low |
| 知识产权 / 训练数据版权 | 内容许可成本、毛利 | 训练数据需要明确授权 → 增加上游成本 → 压缩毛利 | medium |
| 出口管制 / 芯片限制 | 部署区域选择、硬件成本 | 受限区域的客户需替代方案 → 影响市场覆盖和 unit economics | observed |

### 规则

- 不要出现"监管风险是 XX"后直接跳到结论文本——必须展示完整的 **regulatory factor → business variable → mechanism → impact magnitude/range** 链条。
- 如果判断（judgment）涉及监管影响，数字必须标注为 estimate / inference / scenario-assumption，不得标为确认事实。
- 已知法规（已生效）与提案法规（未通过）必须分开处理，不能用同一确定性级别讨论。

---

## Common failure modes

### Failure mode 1: Overview drift
The report explains the market but never becomes a decision memo.

**Fix:** Force current snapshot -> scenarios -> stakeholder implications.

### Failure mode 2: Trend list without scenario logic
The report lists trends but never states a base case, alternative case, or change condition.

**Fix:** Require at least one base case and one credible alternative scenario when uncertainty is material.

### Failure mode 3: Synthetic precision
The report presents precise market numbers without clarifying whether they are observed, inferred, or illustrative.

**Fix:** Label numeric role and evidence status.

### Failure mode 4: Hidden time-layer mixing
Current facts, forecast logic, and illustrative ROI math appear in one paragraph as if they were equally factual.

**Fix:** Separate current snapshot, forecast section, and illustrative calculations.

### Failure mode 5: Action gap
The report gives a smart-sounding bottom line but no stakeholder-specific next steps.

**Fix:** Require actions + monitoring signals.

### Failure mode 6: Single-scenario outlook
The report has only a base case with no structured alternative scenarios. This is a forecast, not an outlook memo.

**Fix:** Require at minimum a base case and one credible alternative scenario with distinct assumptions and trigger conditions.

### Failure mode 7: Investor-only stakeholder coverage
The report covers only investor/operator implications but ignores technology developers, policymakers, enterprise buyers, or end users.

**Fix:** Require at least 3 distinct stakeholder types with dedicated "what does this mean for them" subsections.

### Failure mode 8: Wrong route for ranking task
The report uses Market Outlook for a task whose core output is ranking, prediction, or selection among defined options.

**Fix:** Check the "When not to use this route" section and `ROUTING-MATRIX.md` "Do not use" clauses before committing to this route. Redirect to Constrained Choice / Shortlist when ranking/prediction burden is primary.

### Failure mode 9: Probability precision illusion
The report assigns precise probability percentages (e.g., "15-20%", "23%") to inherently uncertain outcomes where the evidence base cannot support that level of precision.

**Fix:** Use directional labels (most likely / upside / downside) or bounded ranges with explicit uncertainty caveats. Precise probabilities are only justified when backed by robust quantitative models or large-sample statistical evidence.

---

## Final audit questions

Before delivery, ask:

- Does the report start from a verified current baseline?
- Are drivers and blockers clearly separated?
- Is there a visible base case for the stated time horizon?
- Are there structured alternative scenarios (at minimum base + one alternative) with distinct assumptions and trigger conditions?
- Are quantitative outlook numbers labeled by role?
- Does the report cover at least 3 distinct stakeholder types with dedicated implications?
- Does it explain what would change the conclusion?
- Is the task actually a market-outlook task, or does it carry ranking/selection burden that belongs to a different route?

If several of these are missing, the report is probably still an overview rather than a proper market-outlook memo.
