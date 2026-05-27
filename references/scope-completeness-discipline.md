# Scope Completeness Discipline

Use this reference when a task claims global, comprehensive, industry-wide, or full-landscape scope. It defines what minimum coverage should look like so "global" is not just a stylistic label.

This is not about scoring a specific report — use `evals/cases/global-market-scope-completeness-case.md` for that. This reference defines the **reusable rule** for what acceptable scope coverage means.

---

## Core rule

When a report claims a scope label, the actual coverage must match the label.

### Global / industry-wide
The report must cover at least:
- **the top 3-5 geographies** by demand, supply, or regulation (whichever most affects the conclusion)
- **regional leaders** that materially shape the competitive landscape, not only global brands
- **binding regulatory regimes** — if a regime affects market access, pricing, or product design, it must be discussed proportionally to its impact

If any of these are missing, the report must:
- state the omission explicitly
- explain why it does not change the conclusion
- or downgrade the scope label (e.g., from "global" to "US + Europe focus")

### Comprehensive / full landscape
The report must not silently skip any major segment, use case, or value-chain layer that could materially change the answer.

- if a segment is excluded, say so
- if coverage is proportional to data availability rather than importance, flag the gap

### Partial scope (acceptable)
A report may have deliberately limited scope — e.g., "US market only", "enterprise segment only". This is fine as long as:
- the scope boundary is stated in the opening
- the label reflects the boundary (not "global" when it covers only one region)
- a reader would not reasonably assume broader coverage than what is delivered

---

## Geography coverage matrix

When a report claims global scope, check:

| Dimension | What to cover | Minimum bar |
|-----------|---------------|-------------|
| Demand centers | Largest revenue / adoption / user markets | Top 3 geographies by market size |
| Supply centers | Key manufacturing / sourcing / talent regions | Regions that would disrupt supply if constrained |
| Regulatory centers | Regimes that control market access or product design | At minimum the most restrictive regime(s) |
| Competitive map | Players that shape each major region | Regional champions not just global brands |

If the report covers fewer than these by default, it must state which regions were prioritized and why.

---

## When to apply this discipline

Apply scope completeness when:
- the task asks for "global", "worldwide", "industry-wide", or "full landscape" coverage
- the report title or scope statement implies breadth that the body may not deliver
- the recommendation or conclusion depends on multi-region comparison
- a market-size, market-share, or competitive-rank claim references multiple geographies

Do **not** apply when:
- the task is explicitly single-region (e.g., "US market only")
- the report's scope is bounded by the user's constraints (e.g., "providers available in China")

---

## Common failure patterns

| Pattern | Symptom | Fix |
|---------|---------|-----|
| Name-only global | Report says "global" but covers US+EU only | Add missing geographies or downgrade scope label |
| Missing load-bearing geography | A top-3 geography is absent or appears in one sentence | Cover it proportionally or state explicit exclusion |
| Flat competitive map | Global names listed but local champions absent | Include region-specific leaders |
| Scope boundary not stated | Partial report reads as if it were comprehensive | State what is excluded in the opening |
| Data-driven exclusion | Poorly documented markets are silently omitted | Flag data gaps rather than ignoring the region |

---

## Visible output in the report

When scope completeness is applied, the final report should contain:

- a scope statement in the opening that matches actual coverage
- for global claims, coverage of the consequential geographies/segments proportional to their importance
- state the exclusion of any load-bearing geography or segment that is not covered (with rationale)
- avoid silently treating data-poor regions as irrelevant

---

## Related files

- `evals/cases/global-market-scope-completeness-case.md` — concrete scoring tool for a specific report
- `evals/meta/scope-completeness-discipline.md` — meta-eval for diagnosing which layer of the repo should change when a scope failure occurs
- `ROUTING-MATRIX.md` — cross-cutting discipline: scope completeness
