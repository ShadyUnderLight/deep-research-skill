# Report Template

Use this as the default structure for most deep-research outputs.

Do not force every section if the task does not need it, but keep the report decision-oriented and evidence-aware.

## Default structure

### 1. Executive summary

**Format: use bullet points, not paragraphs.** Each bullet should contain one distinct idea. Do NOT write the executive summary as a wall of running text.

- answer the real question first
- give the bottom line in 4–8 short bullet points
- each bullet: one insight, one label (Confirmed / Inference / Uncertainty)
- separate what is confirmed, inferred, and uncertain when relevant
- put the most important conclusion first; less important details later
- when presenting paired signals (e.g., volume growth + margin pressure), use one bullet to pair them — do not separate into different sections

**Good bullet:**
- `[CONF]` 2025年营收638.9亿美元，净利润231.3亿美元（同日历年）

**Bad bullet (wall of text, no label):**
- 博通是全球最大的半导体和基础设施软件公司之一，2025财年营收达638.9亿美元，净利润231.3亿美元，在AI浪潮中跻身"科技七巨头"（Magnificent Seven），公司业务横跨半导体芯片设计与软件基础设施两大板块。

**When writing bullets, ask:** Can a reader extract the key facts without reading every sentence?

### 2. What matters most

- identify the 2-5 variables that most affect the conclusion
- explain why they matter more than the rest

### 3. Key findings

- present the main findings in descending order of importance
- avoid trivia and background overload

### 4. Detailed analysis

Organize by task type. Examples:

- company: products, financials, competition, risks, strategy
- market: size, growth, structure, competition, bottlenecks
- technical: feasibility, constraints, trade-offs, implementation needs
- policy: rules, scope, timing, compliance impact, edge cases

### 5. Risks and counter-evidence

- include the strongest reasons the main conclusion could be wrong
- include limits, contradictions, or competing explanations

### 6. Uncertainty and missing evidence

- say what could not be verified
- say what would most improve confidence

### 7. Bottom line

- give the practical conclusion
- include what to do next when useful
- include what could change the conclusion

### 8. Sources

- list the most important sources
- when applicable, use a structured source register rather than a loose bibliography

## Compression rule

If the user wants a shorter answer, shorten:

- background detail
- secondary branches
- repetition

Do not shorten away:

- the real objective
- the core conclusion
- counter-evidence
- uncertainty

## Quality bar

A good report should let the reader quickly answer:

- what is the conclusion?
- why does it hold?
- what could break it?
- what remains uncertain?
- what should be done next?

## Required evidence-tier legend

At the top of every report, include a brief legend defining evidence confidence levels. Use this format:

```
证据分级：
[CONF] = 来自监管披露/年报/官方发布
[LIKELY] = 来自权威机构或媒体（可能为二手）
[UNCERTAIN] = 行业认知缺乏统一口径或无法验证
```

This makes your labeling system interpretable to the reader and enforces discipline on the model side.

## Data calibration paragraph (required when using proxy indicators)

When you use proxy indicators because primary data is unavailable, add a brief note immediately below the relevant section or table:

> "注：公开定期报告对'[指标名称]'披露有限，因此以[代理指标]作为规模与供给能力的代理指标，并注明来源与口径。"

The note must state: (1) what proxy is being used, (2) why the primary data is unavailable, (3) what limitation this introduces. Without this, readers may mistake a proxy for a direct measurement.

## Conditional framing in market-position conclusions

Every market-position or ranking conclusion must include a conditional clause. Never write flat assertions like "X is the market leader" without a scope and a dependency.

- Bad: `"比亚迪是中国最大新能源汽车制造商"`
- Good: `"在中国市场（2025年零售口径），比亚迪销量领先，但全球市场份额取决于海外本地化产能落地节奏"`

Pattern: `[Position claim] + "but depends on [X]" or "this assumes [Y]"`. If no dependencies can be identified, say so explicitly.

## Competitive framing — choose the right unit of comparison

When comparing companies or assessing competitive position, do not default to unit sales or volume. First ask: *what is the correct unit for the question being answered?*

Examples:

- If comparing profitability: use margin, not revenue
- If comparing scale in a price-war context: revenue or margin, not unit volume (volume can grow while margin collapses — the "规模扩张、盈利承压" pattern)
- If comparing battery suppliers: GWh deployed, not number of vehicles

State explicitly which comparison unit you are using and why. Do not let the reader assume unit sales = competitive advantage.

## Volume + profitability signal pairing (financial sections)

When reporting volume or scale growth in a financial or competitive context, always check whether profitability and cash flow signals exist. If both growth and decline signals are present in the same period, use the "规模仍在扩张、盈利承压" structure to make the tension explicit rather than burying it in separate paragraphs.

This is a direct distillation pattern from GPT's BYD report, which consistently paired volume growth with margin and cash flow pressure in the same sentence.

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

## Market-entry / go-no-go memo formatting discipline

When the task is about market entry, regional expansion, country prioritization, or go/no-go judgment, do not format the report like a long regional backgrounder.

The page should help a decision-maker scan in this order:

1. recommendation
2. hard gates
3. shortlist / priority order
4. why the top path wins
5. what would change the decision

Formatting discipline for these cases:

- **Do not open with a dense paragraph summary.** Use short bullets or compact decision blocks.
- **Pull hard gates into their own block.** Do not bury budget, deployment, compliance, or localization gates inside long prose.
- **Use one visible comparison unit across countries.** Avoid free-form country notes as the primary structure.
- **Separate market roles visually when relevant:** regional hub, first revenue beachhead, later expansion market.
- **Keep country notes subordinate to the shortlist logic.** The report should feel like narrowing, not touring.
- **If milestones / KPIs / phased rollout are included, present them as a sequence block, not scattered commentary.**

Bad pattern:
- a long "市场分析" section followed by a recommendation paragraph at the end

Better pattern:
- recommendation block
- hard-gate block
- country shortlist table
- phased entry path
- change-the-decision conditions

## Table formatting discipline

When building tables with multi-dimensional comparisons (e.g., product category across multiple attributes):

- **Each cell contains one fact.** Do not pack multiple data points into a single cell.
- **Use `<br>` (line break) within a cell when a single attribute has multiple sub-points.** For example, a cell for "发热原理" that needs to list "燃烧烟草 (600-900°C) + 雾化器 + 口腔黏膜" should be written in markdown as one cell using `<br>`: `燃烧烟草 (600-900°C)<br>雾化器加热<br>口腔黏膜吸收`.
- **Avoid using `|` inside cell content** — if a cell requires listing multiple items separated by pipes, use commas or `<br>` instead.
- **Wide tables with many columns are hard to read in PDF.** Consider splitting a wide table into two separate tables grouped by theme (e.g., one table for product attributes, another for commercial metrics).

When in doubt: write for the reader who will skim the table, not for the analyst who already knows the data.
