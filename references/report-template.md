# Report Template

Use this as the default structure for most deep-research outputs.

Do not force every section if the task does not need it, but keep the report decision-oriented and evidence-aware.

## Default structure

### 1. Executive summary

- answer the real question first
- give the bottom line in 3-6 bullets
- separate what is confirmed, inferred, and uncertain when relevant

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
