# Technical Analysis Audit

Use this checklist before delivery when the primary route is **Technical Deep-dive**.

This checklist verifies that the technical analysis route was executed correctly and the final artifact satisfies its contract.

---

## Route activation

- [ ] the task was explicitly classified as technical analysis (principle, architecture, feasibility, patent, or roadmap)
- [ ] the technical analysis route was selected as the primary route (not as a secondary discipline)
- [ ] the route conflict check was run: confirmed this is not better served by provider selection, equipment selection, constrained choice, or market outlook

## Technical state verification

- [ ] current technical state is verified (versions, capabilities, benchmarks)
- [ ] the report's stated coverage date or assessment window is consistent with the source timeline it cites; if sources span a date range, the coverage window is explicit
- [ ] stale technical claims are flagged and either updated or explicitly marked as historical
- [ ] roadmap / version / feature-state claims 分为 stable / shipped / experimental / deprecated / superseded / announced roadmap / proposed / SEP draft / rumored / community signal
- [ ] roadmap announcement 可标为 confirmed event，但未来能力结果不得标为 confirmed outcome
- [ ] deprecated / superseded feature 没有被当作当前推荐能力
- [ ] 如果报告引用官方 roadmap，必须说明是否 commitment，以及该说明对结论的影响

## Evidence quality

- [ ] primary technical sources are used for load-bearing claims (documentation, specs, papers, patents)
- [ ] vendor claims are distinguished from independently verified technical facts
- [ ] benchmarks cite methodology, environment, and date
- [ ] patent claims cite patent numbers or specific filings, not just counts
- [ ] （非阻塞）厂商自述在正文中明确标注了来源角色（如 `(厂商自述)` 或 `(来源：厂商自述，非独立验证)`），见 `references/source-traceability-and-claim-citation.md` §来源标注一致性
- [ ] （非阻塞）涉及厂商自述的行内引用附加了标准格式 caveat `(来源：厂商自述，非独立验证)` 或等效说明
- [ ] source register must use the 7-column template (ID / Source Name / Source Type / Date / DOI or URL / Reliability / Claims Supported) defined in `references/source-traceability-and-claim-citation.md` (§Structured Source Register Template). 来源注册表必须使用该 7 列模板。

## Comparison structure (for architecture comparison)

- [ ] comparison dimensions are explicit (not just "better" or "worse")
- [ ] each dimension has clear criteria
- [ ] trade-offs are stated, not just advantages
- [ ] the comparison covers at least: performance, cost, maturity, ecosystem (or justified subset)
- [ ] the recommendation explains which dimensions are load-bearing
- [ ] （非阻塞）所有比较表、评分表、估算表包含数字角色列（或等效的表头角色行/表注），见 `references/quantitative-role-labeling.md` §表格中的角色标签

## Feasibility assessment (for technical feasibility)

- [ ] what is being attempted is clearly defined
- [ ] available approaches are listed
- [ ] evidence of viability is cited (not just claims)
- [ ] critical unknowns are identified
- [ ] validation requirements are specified
- [ ] conclusion is explicit: feasible / conditionally feasible / not feasible

## Maturity assessment

- [ ] technology maturity is explicitly assessed (TRL, adoption lifecycle, or equivalent)
- [ ] the assessment distinguishes: proven in production / proven in lab / theoretical / experimental
- [ ] ecosystem maturity is assessed separately from core technology maturity

## Judgment quality

- [ ] the report makes a technical judgment, not just a technical survey
- [ ] the judgment is supported by evidence, not just expert opinion
- [ ] limitations and constraints are stated, not hidden in footnotes
- [ ] the "what would change the conclusion" question is answered

## Hard fail check

Fail if any of these are true:

- [ ] the report is a pure technical survey without judgment
- [ ] comparison lacks explicit dimensions
- [ ] technical state is stale without flagging
- [ ] vendor claims are treated as technical facts
- [ ] feasibility conclusion lacks evidence
- [ ] roadmap evaluation treats announced features as shipped
- [ ] patent analysis is counting without coverage analysis

---

## Final sign-off

- [ ] all items above are checked
- [ ] the report visibly satisfies the technical analysis artifact contract
- [ ] the route is evident in the report structure without needing to read hidden notes
