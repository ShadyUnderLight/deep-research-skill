# Technical Analysis Discipline

Use this file when the research task is mainly about understanding, comparing, or evaluating technology — its technical principles, architecture, feasibility, maturity, or technology roadmap (原理、架构、可行性、成熟度、技术路线).

This discipline applies when the core question is **technical judgment**, not product selection, vendor comparison, or market sizing.

## When to use

Apply this discipline when the task involves:

- understanding how a technology works (原理分析)
- comparing technical architectures (架构对比)
- evaluating patent portfolios or trends (专利趋势)
- assessing technical feasibility (技术可行性)
- evaluating technology roadmaps (技术路线评估)

## When NOT to use

Do not use this discipline when:

- the task is mainly about selecting a product or vendor → use **Provider / Vendor Selection** or **Equipment Selection**
- the task is mainly about market evolution → use **Market Outlook / Industry Evolution**
- the task is mainly about competitive positioning → use **First-tier / Competitive Positioning**
- the task is about choosing among defined options → use **Constrained Choice / Shortlist**

## Core questions

### 1. Technical principle analysis (技术原理分析)

- What is the core mechanism or principle?
- What are the key components and how do they interact?
- What are the fundamental constraints or limitations?
- What makes this approach different from alternatives?

### 2. Architecture comparison (架构对比)

- What are the candidate architectures?
- What are the comparison dimensions? (performance, cost, maturity, ecosystem, scalability, complexity)
- What are the trade-offs for each dimension?
- Which architecture wins under which constraints?

### 3. Patent analysis (专利趋势)

- What is the patent landscape? (filings, grants, key assignees)
- What technical areas are covered?
- What is the freedom-to-operate situation?
- What trends emerge from filing patterns?

### 4. Technical feasibility (技术可行性)

- What exactly is being attempted?
- What approaches are available?
- What evidence exists that this works in practice?
- What are the critical unknowns or risks?
- What validation would matter next?

### 5. Technology roadmap evaluation (技术路线评估)

- What is the current state of the art?
- What are the announced or rumored roadmaps?
- What are the key milestones and dependencies?
- What could derail the roadmap?
- What is the realistic timeline vs. optimistic claims?

### Roadmap/feature state stratification

When evaluating a technology roadmap, classify each claim into exactly one of these states.
Do not mix multiple states in the same claim.

| 状态 | 含义 | 允许标签 | 写作要求 |
|------|------|----------|----------|
| Stable / shipped | 当前稳定规范或已发布实现支持 | [CONF] | 标明版本和验证日期 |
| Experimental | 规范/扩展标明 experimental | [CONF] for status, [INFER] for maturity | 不得写成生产稳定能力 |
| Deprecated / superseded | 已弃用或被替代 | [CONF] for status | 必须说明迁移或风险 |
| Announced roadmap | 官方 roadmap / WG priority | [CONF] for announcement, not outcome | 必须写明不是已交付能力 |
| Proposed / SEP draft | 提案、草案、PR | [INFER] or scoped [CONF] for proposal existence | 不得当成 adopted spec |
| Rumored / community signal | 媒体、社区、issue、论坛 | [INFER]/[UNKN] | 必须标低置信或 discovery |

## Evidence standards

For technical claims, prioritize:

1. **Primary technical sources**: official documentation, technical papers, specifications, patents
2. **Engineering evidence**: benchmarks, implementation reports, production deployments
3. **Expert analysis**: reputable technical analysis, peer-reviewed research
4. **Community signals**: developer forums, issue trackers, conference talks (as supplemental)

Do not treat marketing materials, blog posts, or press releases as primary technical evidence.

## Maturity assessment frameworks

When evaluating technology maturity, consider using:

### Technology Readiness Levels (TRL)

| Level | Description |
|-------|-------------|
| TRL 1-3 | Basic research to proof-of-concept |
| TRL 4-6 | Lab to prototype validation |
| TRL 7-9 | Production to deployment-proven |

### Adoption lifecycle

- **Innovator**: experimental, high risk
- **Early adopter**: proven in niche, growing ecosystem
- **Early majority**: production-ready, expanding use cases
- **Late majority**: mainstream, standardized
- **Laggard**: legacy, being replaced

## Comparison dimensions for architecture analysis

When comparing technical architectures, use these dimensions:

| Dimension | Key questions |
|-----------|---------------|
| Performance | throughput, latency, scalability limits |
| Cost | infrastructure, operational, development |
| Maturity | production readiness, ecosystem stability |
| Ecosystem | tooling, community, vendor support |
| Scalability | horizontal/vertical scaling characteristics |
| Complexity | operational burden, learning curve |
| Flexibility | extensibility, adaptability to new requirements |
| Risk | technical debt, vendor lock-in, obsolescence risk |

## Common failure modes

Watch for these failure patterns:

1. **Pure technical survey without judgment**: describes technology but does not evaluate or recommend
2. **Missing comparison dimensions**: compares on only 1-2 dimensions when 4-5 are decision-relevant
3. **Stale technical state**: uses outdated version numbers, deprecated features, or superseded benchmarks
4. **Vendor claims treated as technical facts**: marketing specs mixed with engineering evidence
5. **Roadmap optimism**: treats announced features as shipped capabilities, or mixes stable/shipped, experimental, deprecated, announced, proposed, and rumored states into one undifferentiated layer
6. **Ignoring operational burden**: focuses on capabilities while ignoring deployment, maintenance, and scaling costs
7. **Patent counting without analysis**: lists patents without understanding technical coverage or freedom-to-operate

## Output structure

A technical analysis report should visibly show:

### For principle analysis
- Core mechanism explanation
- Key components and interactions
- Fundamental constraints
- Comparison with alternatives

### For architecture comparison
- Candidate architectures
- Comparison dimensions with explicit criteria
- Dimension-by-dimension analysis
- Trade-off summary
- Recommendation with conditions

### For feasibility assessment
- What is being attempted
- Available approaches
- Evidence of viability
- Critical unknowns
- Validation requirements
- Conclusion: feasible / conditionally feasible / not feasible

### For roadmap evaluation
- Current state of the art
- Announced roadmaps
- Key milestones and dependencies
- Risk factors
- Realistic timeline assessment

## Hard fail conditions

Fail the report if:

- it becomes a pure technical survey without judgment or recommendation
- it compares architectures without explicit comparison dimensions
- it uses stale technical state without verification
- it treats vendor claims as confirmed technical facts
- it assesses feasibility without evidence of viability
- it evaluates roadmaps without separating announced vs. shipped capabilities
- it analyzes patents without understanding technical coverage

## Related references

- `references/forward-looking-discipline.md` — for forecasts, roadmap statements, announced-vs-rumored separation, forward-looking assumption chains, and technical roadmap adaptation. Use when the task involves technology roadmap evaluation. See also §Roadmap/feature state stratification above for state-level classification.
- `references/source-traceability-and-claim-citation.md` — for source type classification and inline citation. Use for all technical claims.
- `references/source-quality.md` — for source ranking dimensions and tie-break rules. Use when source credibility is ambiguous.
- `references/counter-evidence.md` — for actively seeking contradicting evidence. Use when the technical claim is contentious or high-stakes.
