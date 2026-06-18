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
