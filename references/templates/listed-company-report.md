# Listed Company / Investment-style Report Template (route-specific)

**When to read:** only when the **listed-company** route is selected (see the
route's card in `references/routes/listed-company.md`). The core default
structure lives in `references/report-template.md`; this file adds the
route-specific sections that the listed-company artifact contract requires.

### Research-anchor block (mandatory for listed-company work)

For listed-company / investment-style reports, a **research-anchor block** is mandatory. It must appear on the front page, after the one-sentence thesis and executive bullets, but before methodology notes or evidence-grading legends.

This block locks the time layers that govern the entire memo:
- latest full-year reported period (FY)
- latest quarterly / interim reported period
- latest current market snapshot date
- latest management / leadership state (when decision-relevant)

**Placement rule:** The research-anchor block goes **before** the evidence-tier legend, not after it. This prevents the first screen from being occupied by methodology notes instead of judgment.

> This placement rule was updated to resolve a conflict between the existing template (which placed anchor block before thesis) and the metadata-first drift discipline introduced in Round 6 P2 (#211). The thesis must now come first; anchor block follows. See `references/decision-report-template.md` §Metadata-first drift warning.

**Format example:**

```
研究锚定：最新FY：FY2025｜最新季度：2026Q1｜市场快照：2026-05-29｜管理层：[CEO Name]
```

For full definition and failure modes, see `references/finance-date-discipline.md` → "Research Anchor Block" section.

### Time-horizon valuation stratification (mandatory when the task asks "是否充分反映长期增长")

当报告要回答"当前估值是否充分反映了[长期增长/长期价值/长期不确定性]"时，opening 的 thesis 必须按以下结构做时间分层，而不仅给出一个方向性判断（如"未充分反映" / "合理偏低"）：

```
一句话结论：
- 短中期（1-3年 或 3-5年，选择最符合该行业周期的子范围）：[已充分反映 / 部分反映 / 未充分反映]，原因是 [估值倍数 / 共识 EPS / 管理层指引]
- 长期（5-10年）：[仍有上行可选性 / 已大体反映 / 难以判断]，原因是 [TAM / 护城河 / 资本回收 / 竞争格局]
- 行动含义：[可持有 / 等待回撤 / 仅适合高风险资金 / 不具备安全边际] — 必须与时间层次一致，不把"长期可持有"写成"当前明显低估"
```

**分类选择指引**：三个选项之间没有严格的定量阈值，但有优先选择规则：
- **已充分反映**：当前估值倍数已显著高于历史均值，或与共识 EPS 对应的 PEG > 2x，或 DCF 反向计算隐含的增长假设已超过最乐观的 TAM 预测
- **未充分反映**：当前估值倍数低于历史均值且增长趋势确认，或与同业相比有明显折价但基本面差异不足以解释该折价
- **部分反映**：当难以判断"已充分反映"还是"未充分反映"时，优先选择"部分反映"，并用证据量化剩余空间的幅度

**为什么要时间分层？**

GPT 深度研究的 TSMC 报告展示了更强的判断结构：不是把问题压缩到"低估/不低估"二元结论，而是拆成"近 3-5 年增长已较充分定价、10 年维度上行可选性尚未完全定价"。这让读者能判断：

- 市场到底定价了哪一段增长？
- 哪一段仍有分歧？
- 新增资金和长期持有者的结论是否应该不同？

如果 opening 只有一个方向性估值判断而没有时间分层，则该报告应视为**条件性通过（conditional pass）**而非全通过。

**证据分层要求**：当使用时间分层时，support / weakening / unresolved 的分离应在每个时间维度内执行，而不是全局笼统地做。也就是说，对于短中期和长期应分别列出支持证据、削弱证据和未解变量。这防止了"短期有风险但长期看好"这样的定性判断背后缺乏分层的证据支撑。

This stratification rule was added via issue #277 to distinguish flat valuation judgments from time-aware ones.

### Four-variable decomposition (recommended for long-term growth valuation tasks)

对于"估值是否充分反映长期增长"类任务，opening 或第二节应明确拆解为以下四个变量，并使后续章节顺序与之对齐：

1. **需求规模**：长期 TAM / 行业增长是否足够大，来源和假设是什么。
2. **份额捕获**：公司是否能持续拿到足够份额，护城河和竞争证据是什么。
3. **利润率与现金流转换**：增长是否改善 margin / FCF / ROIC，还是被 CapEx、折旧、海外扩张吞掉。
4. **估值透支程度**：当前 PE/Forward PE/DCF 是否已经资本化前述增长。

这四个变量应成为后续章节的组织骨架，而不是散落在财务、市场、风险段落中。如果没有明确采用四变量结构，报告中的 3-5 个估值驱动变量仍应显式列出，并用它们驱动报告结构。

This decomposition is recommended when the task involves "has the market priced in long-term growth" — it prevents the report from treating valuation as a single PE comparison and forces explicit handling of the growth→value conversion chain.

### 增长到现金流转换表（CapEx-heavy 公司强制）

当本报告涉及 CapEx-heavy 公司（见 `references/valuation-methodology.md` §Capital return discipline for CapEx-heavy companies 触发条件）时，估值部分必须包含以下转换表。该表将 CapEx、D&A、FCF、ROIC 等变量从风险清单升格为估值模型输入。

| 变量 | 当前状态 | 基准假设 | 压力情景 | 对估值影响 | 数字角色 |
|---|---|---|---|---|---|
| CapEx / 收入 | | | | | observed / assumption |
| D&A / 收入 | | | | | assumption |
| FCF margin | | | | | model output |
| ROIC / 回收期 | | | | | model output |
| 新产能/新地区 margin 稀释 | | | | | estimate / assumption |

**填写规则**：
- 「当前状态」列填写最近报告期的实际可观测数据（如 FY2025 CapEx/收入 = 35%）。该列数值为 **observed**（观察值）。
- 「基准假设」列填写报告采用的分析假设（如未来 3 年 CapEx/收入逐步降至 28%）。该列数值为 **assumption**（假设）。
- 「压力情景」列填写当关键假设不成立时的替代值（如 ASML 设备交付延迟，CapEx/收入维持 35%+）。该列数值为 **assumption**（假设）。
- 「对估值影响」列简述该变量偏离对 PE 倍数调整、目标价变动或结论方向的量化/方向性影响。
- 「数字角色」列标注各行数字的主要认识论角色。由于同一行内「当前状态」（observed）与「基准假设/压力情景」（assumption）分属不同角色，各行数字角色列标注的是该行**核心角色范围**。例如 CapEx/收入 = `observed / assumption` 表示当前值为观察值、未来值为假设。见 `references/quantitative-role-labeling.md`。
- FCF margin 和 ROIC 的「当前状态」格基于实际财务报表计算，角色为 **model output（基于观察值）**；「基准假设/压力情景」格角色为 **model output（基于假设）**。

> 本表不替代 DCF（当 DCF 触发条件满足时 DCF 仍必须执行），而是在 DCF 不适用或作为 DCF 假设的补充可见框架时，确保 CapEx-heavy 公司的资本回收变量不被忽略。

This table requirement was added via issue #279 to ensure CapEx-heavy company reports do not skip the growth-to-cash-flow conversion analysis.

Do not default to using the front page as the main location for:
- full evidence-label explanations
- full numeric-role explanations
- long methodology notes

Method transparency should remain visible, but detailed label explanations and process notes should usually move to a later methods note, page-2 opening block, or appendix.


## Market snapshot table (mandatory for listed-company work)

For listed-company reports, a completed market snapshot table is mandatory. It must appear on the front page, immediately after the research-anchor block and thesis/executive bullets.

| 指标 | 值 | 来源 |
|------|-----|------|
| 当前股价 | $__ | [数据源](URL) |
| 快照日期 | YYYY-MM-DD | — |
| 市值 | $__ | [数据源](URL) |
| PE (TTM) | __x | [数据源](URL) |
| PE (Forward) | __x | [数据源](URL) |
| PB | __x | [数据源](URL) |
| PS | __x | [数据源](URL) |
| 52周区间 | $__ - $__ | [数据源](URL) |
| 股息率 | __% | [数据源](URL) |

> 注：PB 须注明净资产所属报告期，PS 须注明营收口径（TTM / FY2025 等）。

### 客户集中度与第二供应源风险（如适用）

当客户集中度 materially 影响 thesis 时（参见 `checklists/listed-company-report.md` §Customer concentration / second-source discipline），报告应包含以下分析结构：

| 指标 | 最近期间 | 前期对比 | 证据角色 | 估值含义 |
|---|---:|---:|---|---|
| 前十大客户收入占比 | | | observed / estimate | |
| 第一大客户占比 | | | observed / estimate | |
| 第二大客户占比 | | | observed / estimate | |
| second-source 信号 | | | media-reported / inferred | |

结论：客户集中度对 thesis 的净影响是 [增强/削弱/双向]，主要通过 [收入可见度/议价权/替代风险/估值倍数] 影响估值。

> **双面性要求**：上表和分析必须同时呈现客户集中度的正面和负面含义，避免仅列举风险。正面含义包括收入可见度、共同研发深度、客户锁定效应；负面含义包括议价权削弱、单客户波动风险、第二供应源替代威胁。如果报告使用"客户锁定""深度绑定"等措辞，必须检查 second-source / supplier de-risking 信号（参见 `references/moat-monopoly-screening.md` §Concept-boundary traps）。

### Valuation method and scenario analysis (mandatory for listed-company work)

For listed-company reports, a **valuation method and scenario analysis** section is mandatory. It must appear in or immediately after the financial analysis portion of the report, with enough detail for a reviewer to recompute the target prices from the disclosed assumptions.

**估值方法**
- 主要估值指标：__（理由：__）
- 补充指标：PB（说明：__）, PS（说明：__）, EV/EBITDA（说明：__）
- 其他指标：__（说明：__）
- 可比公司：__（选择逻辑：__）
- 倍数区间历史范围：__x - __x

**情景分析**
| 情景 | EPS假设 | PE倍数 | 目标价 | 触发条件 |
|------|---------|--------|--------|---------|
| 乐观 | $__ | __x | $__ | __ |
| 基准 | $__ | __x | $__ | __ |
| 悲观 | $__ | __x | $__ | __ |

> **时间分层关联**：当估值问题涉及"是否充分反映长期增长"时，本节的情景分析应反映时间分层（见前文 §Time-horizon valuation stratification），各情景的时间范围和触发条件应与短中期/长期维度明确绑定。乐观/悲观情景不应仅在幅度上不同，还应在"哪段增长被定价了"上做差异化假设。
>
> **四变量关联**：以下情景的 EPS 假设和 PE 倍数选择应反映前文 §Four-variable decomposition 中确定的估值驱动因素。例如，乐观情景通常假设"需求规模"和"份额捕获"加速、"利润率转换"改善；悲观情景则假设"需求规模"受限或"估值透支"程度较高。本节是四变量从定性分析到价格假设的转换层。

#### DCF / 反向 DCF（当适用）

当报告的估值结论符合 `references/valuation-methodology.md` §DCF / reverse DCF trigger 的适用条件时，估值部分必须包含以下内容之一。如果 DCF 不适用，必须提供具体的不可用原因说明。

**DCF 关键假设表**
| 假设 | [近期年份]E | [中期年份]E | [远期年份]E | 数字角色 | 来源 / 方法 |
|---|---:|---:|---:|---|---|
| 收入增速 | | | | assumption / model output | |
| 营业利润率 | | | | assumption | |
| CapEx / 收入 | | | | assumption | |
| D&A / 收入 | | | | assumption | |
| 税率 | | | | assumption | |
| WACC | | | | assumption | |
| 永续增长率 | | | | assumption | |

**三情景股权价值**
| 情景 | 股权价值 | 较当前市值 | 关键触发条件 | 数字角色 |
|---|---:|---:|---|---|
| 乐观 | | | | model output |
| 基准 | | | | model output |
| 悲观 | | | | model output |

#### 敏感性矩阵

当 DCF / 反向 DCF 用于估值时，必须对至少一个高敏感性假设提供单变量敏感性分析。

> **敏感性分析 ≠ 情景分析**：情景分析同时变动多个假设（如乐观/基准/悲观三情景），读者无法看到单一关键假设变化对结论的独立影响。敏感性分析每次只变一个假设（如 WACC ±0.5% 或永续增长率 ±0.25%），保持其他假设不变，以隔离每个变量的边际影响。当报告提供多情景分析时，仍需对高敏感性假设提供独立敏感性表。两者互补而非替代。参见 `references/quantitative-role-labeling.md` §Sensitivity classification。

模板格式：

```
| [变量A] \\ [变量B] | [低值] | [基准值] | [高值] |
|---|---:|---:|---:|
| [低值] | | | |
| [基准值] | | | |
| [高值] | | | |
```

> 矩阵 axes 的选择应反映该公司最敏感的估值假设。WACC × 永续增长率是常见组合；对于增长型公司，收入 CAGR × 终端利润率可能更说明问题。

结论：估值最敏感变量是 [变量]；若 [变量] 低于/高于 [阈值]，结论从 [低估/合理] 翻转为 [高估/不具安全边际]。

> **DCF 关联**：上述 DCF 假设和敏感性矩阵应与前文 §Four-variable decomposition 中确定的估值驱动因素一致。DCF 是"估值透支程度"变量的定量实现层。敏感性矩阵揭示哪个四变量因素对结论影响最大。
