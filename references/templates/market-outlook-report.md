# Market Outlook / Industry Evolution Report Template (route-specific)

**When to read:** only when the **market-outlook** route is selected (see the
route's card in `references/routes/market-outlook.md`). The core default
structure lives in `references/report-template.md`; this file adds the
market-outlook memo discipline and its category-boundary, demand-segmentation
and commercialization templates.

## Market-outlook memo discipline

When the user asks how a market, category, or industry will evolve over the next 6-12 months, do not default to a generic industry overview.

The report should visibly answer:

- what the current baseline is
- what is changing now
- what the key drivers and blockers are
- what the base case is for the stated time horizon
- what alternative scenarios exist
- who should act now and what they should do
- what to monitor that would change the view

If quantitative outlook numbers appear in such reports, label them clearly as one of:

- observed current metric
- inferred estimate
- scenario assumption
- illustrative calculation

Do not let readers mistake scenario math for reported market fact.

### Category Boundary 模板

当使用 market-outlook 路由时，建议在"当前市场快照"之前或紧接其后加一张类别边界表，明确核心市场范围：

```
| 类别 | 是否纳入核心市场 | 纳入理由 | 不可直接比较项 |
|------|---------------|---------|-------------|
| [类别 A] | 是 / 否 / 邻接 | [为什么纳入/排除] | [如果混用会比较什么] |
| [类别 B] | ... | ... | ... |
```

**规则：**
- 不同类别不得在没有 comparison-unit 说明的情况下直接排名。
- 跨层参与者按最大收入来源所在业务口径纳入。
- 见 `references/market-outlook-and-scenario-discipline.md` §Category Boundary。

### Demand Segmentation 矩阵模板

当市场明显异质时，建议在 stakeholders 分析后用需求细分矩阵说明不同 buyer 群体的差异：

```
| 细分维度 | Segment | Job-to-be-done | 购买者 | 付费意愿 proxy | 部署要求 | 证据强度 |
|---------|---------|---------------|-------|--------------|---------|---------|
| 行业监管强度 | 受监管行业（金融/医疗） | [JTBD] | [决策者身份] | [proxy指标] | SaaS / on-prem / hybrid | observed / estimate |
| 行业监管强度 | 未受监管行业（创意/零售） | [JTBD] | [决策者身份] | [proxy指标] | SaaS / on-prem / hybrid | observed / estimate |
| 企业规模 | 大企业 / SME / 个人开发者 | ... | ... | ... | ... | ... |
```

### Commercialization / Pricing Memo 结构

商业化分析建议使用以下结构代替自由的"商业模式"段落：

```
## 商业化分析

### 谁付费
- 真实 buyer: [角色]，预算归属: [IT/业务线/研发]
- 采购单位: [团队/部门/企业/个人]，决策链: [自下而上/自上而下/个人]

### 定价模式
| 模式 | 适用场景 | 对毛利影响 |
|------|---------|-----------|
| [per query / per token / per seat / annual contract / consumption / freemium] | [场景说明] | [影响说明] |

### Unit Economics 关键变量
- CAC: [获客成本范围]
- ARPU/ACV: [客单价范围]
- Gross margin: [毛利范围及压力来源]
- Retention: [留存率，NRR]
- 规模效应: [边际成本是否下降]

### 验证指标
- ARR / Revenue growth
- Enterprise contract count
- Multi-model / multi-provider usage
- Paid query / token mix

> 所有数字必须标注角色（observed / estimate / assumption / scenario）和 [Sxx] 引用。
```
