# Quantitative Role Labeling

## Purpose

Quantitative role labeling exists to prevent precise-looking numbers from overstating certainty.

In deep research and decision-oriented reports, load-bearing numbers often mix:

- observed metrics
- proxies
- assumptions
- model outputs
- illustrative calculations

If their role is unclear, a report can look rigorous while quietly presenting planning logic as fact.

## Core rule

Never present proxy, assumption, or model output as if it were an observed or directly reported fact.

If a number materially affects ranking, recommendation, timing, sequencing, confidence, or valuation, its role should be visible.

## Core roles

### Observed metric
A number directly observed, officially reported, or clearly measured by the cited source.

### Proxy
A number used to indirectly support a conclusion about something else.

### Assumption
A number introduced as an input to reasoning, estimation, or scenario construction.

### Model output
A number produced from assumptions, proxies, or selected parameters.

### Illustrative calculation
A number used to clarify logic rather than claim a formal estimate.

## What should be labeled

Quantitative role labeling should be visible when a number materially affects:

- recommendation
- ranking
- shortlist construction
- go / not now / pilot only judgment
- sequencing
- timing
- valuation
- confidence

If removing the number would materially weaken the argument, its role is probably load-bearing and should be visible.

## Common failure modes

Common failures include:

- proxy presented as direct evidence
- assumption presented as observed fact
- model output presented as externally verified reality
- composite score shown without clarifying the role of its inputs
- precise-looking numbers carrying more certainty than the evidence supports

## 假设链 — Assumption chain documentation

Labeling a number as "assumption" is a necessary first step. It tells the reader what epistemic role the number plays. But it does not explain why that particular value was chosen or what would change if it turned out wrong.

An assumption chain makes the reasoning behind a load-bearing assumption visible, auditable, and testable.

### When to document an assumption chain

Not every assumption needs a full chain. Apply this scope rule:

- **Required** — assumptions whose deviation would materially affect the conclusion (high sensitivity). If a ±10% change in the assumption would alter the recommendation, shift the ranking, or change valuation by more than ±15%, the assumption chain is mandatory.
- **Optional** — assumptions whose impact on the conclusion is estimated at under ±10% (or under ±15% for valuation only). A lightweight note is sufficient. If the impact falls in the 10–15% range for valuation, analyst judgment applies; err on the side of documenting.
- **Not needed** — directly observed or officially reported facts (observed metrics). Facts do not become assumptions by being inconvenient.

### Remediation when a chain cannot be completed

If a high-sensitivity assumption cannot support a complete assumption chain, apply one of:

1. **Fill the chain** — search for the missing evidence from available sources. If only partial information exists, document what is known and what remains uncertain, then downgrade confidence accordingly.
2. **Downgrade sensitivity** — reclassify the assumption as lower-sensitivity if the chain gap reveals the assumption is less load-bearing than initially assessed.
3. **Restructure the analysis** — reduce dependence on the assumption, or replace it with a more directly verifiable input or a range-based scenario.

Do not leave a high-sensitivity assumption's chain incomplete without an explicit remediation decision and rationale.

### Assumption chain template

For each key assumption, document the following fields. Not every field must be populated; mark genuinely inapplicable fields as `N/A`.

```
### 假设: [具体假设陈述]

- 类型: [假设 / proxy / 估算 / 模型输出]
- 支持证据:
  - 来源 A: [具体依据]
  - 来源 B: [具体依据]
- 依赖条件（假设成立的前提）:
  - 宏观环境: [如不衰退、利率稳定]
  - 竞争格局: [如无颠覆性对手出现]
  - 技术路线: [如主流方案不变化]
- 敏感度:
  - 假设偏差 ±10% → 结论变化 X%
  - 假设偏差 ±50% → 结论变化 Y%
- 失效信号（可观察的事件/数字）:
  - [如 Q1 增速低于 X%，则假设需调整]
  - [如核心客户转向竞品，则假设需放弃]
- 置信度: [高/中/低]
```

### Sensitivity classification

Classify each key assumption by its impact on the conclusion. This determines the required depth of sensitivity testing.

| Classification | Definition | Test amplitudes | Required treatment |
|----------------|------------|-----------------|-------------------|
| **Low sensitivity** | Conclusion unchanged within ±20% deviation | ±20% | Conclusion is robust; label the sensitive variable |
| **Medium sensitivity** | Conclusion direction unchanged but strength changes within ±20% | ±20%, ±50% | Conclusion holds conditionally; label the tipping point |
| **High sensitivity** | Conclusion reverses within ±20% deviation | ±20%, ±50%, extreme scenario | Conclusion is assumption-dependent; reduce confidence or provide scenario analysis |

**Test amplitude selection**:

- **Routine assumptions** (e.g., market growth rate, cost assumptions): test ±20% and ±50%
- **Load-bearing assumptions** (e.g., valuation multiples, core revenue growth): test ±20%, ±50%, and at least one extreme scenario
- **Structural assumptions** (e.g., technology roadmap, regulatory environment): test reversal scenarios (what happens if the assumption fails entirely)

**Output format**:

```
### 敏感性分析: [假设名称]

| 变量 | 基准值 | -50% | -20% | +20% | +50% | 对结论影响 |
|------|--------|------|------|------|------|-----------|
| 市场增速 | 15% YoY | 7.5% | 12% | 18% | 22.5% | ±X% to 核心结论 |

- 敏感度等级: [低/中/高]
- 临界点: [结论翻转的阈值]
- 建议: [降低 confidence / 提供情景分析 / 维持现有结论]
```

**When to apply this classification**:

- **Required** — assumptions classified as high sensitivity. Full sensitivity table and scenario analysis are mandatory.
- **Recommended** — assumptions classified as medium sensitivity. At minimum, document the tipping point.
- **Optional** — assumptions classified as low sensitivity. A brief note is sufficient.

### Template example

```
### 假设: 该公司年增速在未来 3 年保持 15%

- 类型: 假设（基于行业平均增速推测）
- 支持证据:
  - 公司过去 3 年 CAGR 为 14–18%（年报披露）
  - 行业第三方预测未来 3 年增速 12–16%（IDC 报告 [S01]）
- 依赖条件:
  - 宏观环境: 目标市场不出现衰退
  - 竞争格局: 无新进入者以显著更低价格抢份额
  - 技术路线: 现有产品路线不被替代方案颠覆
- 敏感度:
  - 偏差 ±10%（13.5% 或 16.5%）→ 估值变化约 ±15%
  - 偏差 ±50%（7.5% 或 22.5%）→ 估值变化约 ±70%，推荐强度需重新评估
- 失效信号:
  - Q1 营收增速低于 10% → 假设需下调
  - 核心产品 ASP 连续两季下降 → 增速假设可能偏乐观
- 置信度: 中（依赖宏观条件，且竞争格局有不确定性）
```

### Common failure patterns

#### Pattern 1: Proxy used as assumption without justification

A proxy (e.g., patent count as proxy for innovation capability) is silently treated as a valid assumption without explaining why the proxy is reasonable.

**Fix**: State why this proxy is reasonable for the specific context, or downgrade the claim strength.

#### Pattern 2: Assumption chain omitted for high-sensitivity numbers

A number that drives the recommendation has no visible assumption chain — the reader cannot tell what would change the conclusion.

**Fix**: Add the assumption chain. If the assumption is simple, a compact inline version is sufficient.

#### Pattern 3: Assumption stated but dependency conditions missing

The assumption is named ("assume 15% growth"), but the conditions that must hold for it to be valid are not documented.

**Fix**: Add dependency conditions. At minimum, name the 1–2 external conditions most likely to break the assumption.

### Relationship to other discipline files

- `references/forward-looking-discipline.md` has an "Assumption chains" section for forward-looking numbers (revenue projections, market size forecasts, adoption timelines). The template here is the general-purpose version. For forward-looking claims, that file's lighter pattern may be sufficient; for complex or high-sensitivity assumptions, the full template here applies.

## Route-specific notes

### Market entry / regional expansion
Market size, payback, localization cost, and sequencing thresholds are often assumptions or model outputs rather than direct facts.

### Constrained choice / shortlist
Weighted scores, burden proxies, and comparison totals often depend on proxies, assumptions, or model outputs.

### Market outlook / industry evolution
Growth ranges, projected adoption, and scenario paths should not read like observed current-state facts.

### Listed-company / investment-style research
Valuation ranges, scenario cases, and estimated financial outcomes often require explicit model-status visibility.

## Minimal display patterns

Quantitative role may be shown through:

- inline labels
- table columns
- note-style evidence tags

The format may vary.
Role visibility may not.

## Hard fail signs

- A load-bearing number has no visible role.
- A proxy is treated as direct evidence.
- A model output is written as if it were observed fact.
- A recommendation materially depends on unlabeled assumptions.
