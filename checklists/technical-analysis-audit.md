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

### Technical opening baseline

These items verify that the report's front page provides a trustworthy temporal and decision anchor:

- [ ] opening 明确默认受众与决策场景，不只是技术主题说明
- [ ] report date / coverage / latest source date 三者不冲突（metadata date 与正文来源时间戳无矛盾）
- [ ] stable baseline 与 forward-looking material 在 front page 或研究范围中分开：source baseline（规范版本、协议版本、当前实现基线）与 roadmap、实验扩展、前瞻分析使用不同的时间标注，避免读者混淆"已可用"与"规划中"

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
- [ ] each comparator's role is visible (direct substitute / complement / lower-level primitive / higher-level runtime / historical ancestor / unsuitable — with exclusion rationale)
- [ ] comparison table is followed by a trade-off interpretation identifying load-bearing dimensions
- [ ] the recommendation explains which dimensions are load-bearing and what conditions would reverse the conclusion
- [ ] if a common comparator was excluded, the exclusion reason is stated
- [ ] （非阻塞）所有比较表、评分表、估算表包含数字角色列（或等效的表头角色行/表注），见 `references/quantitative-role-labeling.md` §表格中的角色标签
- [ ] 定义敏感的技术概念在比较前已明确其定义范围：原始/严格定义、当代工程定义、本文采用定义
- [ ] （非阻塞）如术语不是单篇论文严格定义的标准概念，报告标明其为操作性定义或工程范式归纳
- [ ] 相关但不等价的概念有明确的排除边界，避免读者误以为比较对象在同类概念间进行

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

## Security deep-dive (activate when security risk is the main burden)

这些检查项只对安全风险是主负担的技术 deep-dive 报告启用。如果任务不以安全分析为主线，跳过本小节。

- [ ] 如果报告主要涉及安全风险，是否定义了**核心资产**（用户数据、凭据、本地资源、远程权限等）、**攻击者类型**与**信任边界**
- [ ] 是否给出了**风险优先级**（可能性 × 影响），而不是等权列出所有风险
- [ ] 是否将缓解措施分为**预防 / 检测 / 响应**（或短/中/长期），而不是堆砌原则性建议
- [ ] 是否提供了工程可落地的**检测信号/监控字段**（如监控指标、阈值建议），而不仅说"应加强监控"
- [ ] （非阻塞）是否区分了**协议设计风险、实现漏洞、部署误配置、供应链风险**等不同风险类型

---

## Final sign-off

- [ ] all items above are checked
- [ ] the report visibly satisfies the technical analysis artifact contract
- [ ] the route is evident in the report structure without needing to read hidden notes
