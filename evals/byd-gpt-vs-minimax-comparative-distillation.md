# BYD Report — GPT vs Minimax Comparative Distillation

**Date:** 2026-04-01
**Models compared:**
- GPT deep research (source: user-provided PDF)
- Minimax deep research (source: user-provided PDF — same topic, same company)

## Purpose

This eval is not about which model "knows more" — both have access to similar public information. It is about **what structural and disciplinary patterns GPT exhibits that Minimax systematically misses**, and what rules or checklists in the skill need to change to close the gap.

---

## 1. Data Exactness vs Rounding

### GPT
- Uses precise figures: **4,272,145 辆** / **4,602,436 辆** (not "约427万辆")
- Discloses exact GWh: **194.705 GWh** / **285.634 GWh** (not "约194GWh")
- Revenue and profit figures to the decimal: **727.32亿元** / **2,241.24亿元**

### Minimax
- Uses rounded figures: "约460万辆"、"约5300亿元人民币"
- Rounds even in Exec Summary where precision matters most
- No indication of whether rounding is intentional or lazy

### distillation target
**Rule:** When the source provides exact figures, use them. Rounding should be intentional and noted ("约" is acceptable when source only provides rounded data, not as a default). Add to `finance-date-discipline.md`.

---

## 2. Explicit Limitation Acknowledgment

### GPT
> "注：公开定期报告对'名义产能（如 GWh/年、台/年）'披露有限，因此以销量、装机量、分部收入等可核验数据作为规模与供给能力的代理指标，并明确注明来源与口径。"

> "这一估算的局限在于：单月受季节性与促销影响较大，且'批发'不等同'终端零售'；但在无更细官方披露的情况下，可作为'头部集中度与相对份额'的近似观察点。"

**This is meta-level self-awareness:** the model explicitly states what it is approximating, why, and what the limitation is — before the reader has to ask.

### Minimax
No equivalent meta-level limitation statement anywhere in the report. The model presents estimates alongside confirmed facts without distinguishing them in the Exec Summary.

### distillation target
**New rule in `report-template.md`:** After the Exec Summary, add a brief "数据口径说明" paragraph when:
- You used proxy indicators because primary data is unavailable
- A figure is an estimate or inference (not confirmed fact)
- The geographic/scope definition of a metric may differ from standard definitions

---

## 3. Evidence Strength Tiering

### GPT
> "证据强度：高=来自定期报告/审计财务/官方发布；中=权威行业机构或主流媒体但可能为二手；低=行业通行认知且缺乏同一口径数据支持"

The report explicitly defines its evidence hierarchy and applies it consistently in tables.

### Minimax
Uses `[CONF]` / `[LIKELY]` / `[UNCERTAIN]` labels (which GPT does not explicitly do), but:
- Drops labels in some places
- Has no explicit evidence-tiering vocabulary
- Does not explain to the reader what each tier means

### distillation target
**Combine the best of both.** The Minimax label system should be supplemented with an explicit evidence-tiering definition at the top of each report — something like:

> "证据分级：[CONF]=来自监管披露/年报/官方发布；[LIKELY]=来自权威机构或媒体但可能为二手；[UNCERTAIN]=行业认知缺乏统一口径或无法验证"

Add to SKILL.md or `report-template.md` as a required header element.

---

## 4. Uncertainty Propagated into Conclusions

### GPT
> "全球市场份额的弹性更大，取决于海外渠道、合规/贸易壁垒与本地化产能落地节奏。"

Even when stating a view, GPT layers the conditionality into the conclusion.

### Minimax
> "中国市场绝对领导者：2025年国内新能源乘用车市场份额约35-40%"

No uncertainty qualifier, no conditional framing, no scope boundary ("中国市场" scope is implied but not stated).

### distillation target
**Rule in `report-template.md`:** Every market-position or ranking conclusion must include a conditional clause: "but depends on [X]" or "this view assumes [Y]." If no dependencies can be identified, say so explicitly.

---

## 5. Competitive Framing — Aligned, Not Absolute

### GPT
> "投资对比应避免单一指标（如销量）直接横向比较，而应对齐'利润池与约束条件'（监管、渠道、资本开支、回款周期）。"

The model tells the reader *how to think about competition*, not just *who wins*.

### Minimax
Competition section lists competitors but does not reframe the competitive question. It accepts "全球最大" framing without interrogating it.

### distillation target
**New reference or checklist item:** "Competitive framing discipline" — when analyzing competitors, always answer: *what is the right unit of comparison for this question?* (e.g., volume vs revenue vs profit vs margin, not just unit sales).

---

## 6. Cash Flow and Profitability Signal Pairing

### GPT
> "规模仍在扩张、盈利与现金回收承压"

This single sentence pairs scale growth with the two profit signals (profit decline + cash flow decline) — explicitly showing the tension, not just reporting the numbers.

### Minimax
Reports revenue and net profit separately but does not pair them to highlight the structural tension (volume up, profitability down).

### distillation target
**Rule in `report-template.md` financial section:** When reporting volume/scale growth, always pair with profitability and cash flow signals if both exist. "规模仍在扩张、盈利承压" is a model pattern to teach.

---

## 7. Inference Without Label — The "预计" Problem (Shared Failure)

### GPT
> "路透社报道其在业绩沟通中提出2026年海外销量目标，并提及欧洲与印尼等地工厂计划在2026年春季附近启动量产"

No "[UNCERTAIN]" tag, but: (a) it attributes "预计" explicitly to company guidance, (b) the word "计划" implies forward-looking, and (c) the phrase "附近" signals imprecision. The source type makes the confidence self-evident.

### Minimax
> "2025年海外销量预计超100万辆"

Uses "预计" but does not attribute it to a source, nor does it label it [UNCERTAIN].

### distillation target
The key difference: **GPT attributes the estimate to a named source (路透社 quoting company guidance), making the confidence implicit in the sourcing.** Minimax uses "预计" as a bare word. The fix is not just adding a label — it is requiring source attribution for all forward-looking statements: *"据[公司/分析师/媒体]预计"* is better than just "预计".

Add to `finance-date-discipline.md`: "Forward-looking figures must cite the source of the estimate, not just the estimate itself."

---

## Comparative Summary

| Dimension | GPT (reference) | Minimax (evaluated) | Gap |
|-----------|-----------------|---------------------|-----|
| Numerals | Exact (4,272,145) | Rounded (约427万) | Precision discipline |
| Limitation acknowledgment | Explicit meta-statement | None | Self-audit transparency |
| Evidence tiering | Defined + applied | [CONF]/[LIKELY] labels, inconsistent | Systematic labeling |
| Uncertainty in conclusions | Conditional framing | Flat assertions | Inference discipline |
| Competitive framing | Right unit of comparison | Absolute rankings | Analytical depth |
| Profit+scale pairing | "规模扩张、盈利承压" | Separated | Signal pairing |
| Estimate sourcing | Named source + guidance | Bare "预计" | Source attribution |

---

## Key distillation outputs

These seven gaps should generate:

1. **`finance-date-discipline.md` additions:**
   - Exact figures from source = use exact; "约" only when source rounds
   - Forward-looking figures must cite source of estimate
   - Volume growth always paired with profitability + cash flow signals

2. **`report-template.md` additions:**
   - "数据口径说明" paragraph when using proxy indicators
   - Evidence-tier legend required at report top
   - Conditional framing in market-position conclusions
   - "规模扩张、盈利承压" pattern as model for tension reporting

3. **`checklist: final-audit.md` additions:**
   - Every "预计/估计/预期" has a named source attribution
   - Market position claim has scope + conditional clause
   - Profit and scale signals are presented together, not separately

## Eval conclusion

GPT does not have better knowledge — it has better **disciplinary scaffolding around its knowledge expression**. The seven gaps above are not knowledge gaps; they are structural and procedural. Closing them requires rule additions and checklist enforcement, not model retraining. This makes them ideal skill-improvement targets.
