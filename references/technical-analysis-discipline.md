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
- What is each candidate's role in the comparison? (direct substitute / complement / lower-level primitive / higher-level runtime or platform / historical or design ancestor / unsuitable comparator — with exclusion rationale)
- What are the comparison dimensions? (performance, cost, maturity, ecosystem, scalability, complexity)
- What are the trade-offs for each dimension?
- Which comparison dimensions are load-bearing vs background information?
- Under what conditions would the recommendation reverse?
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

### 6. Roadmap/feature state stratification

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

### 7. Definition-sensitive concepts (定义敏感概念)

- Is the core concept definition-sensitive — does it carry multiple competing definitions (academic definition vs. engineering definition vs. vendor-specific definition)?
- Does the report need to distinguish the original academic/strict definition from current engineering or industry usage?
- Could the chosen definition materially change the comparison conclusions or recommendation?
- What concepts are commonly conflated with the target concept but should remain analytically distinct?
- What is this report's operational definition (操作性定义), and what is deliberately excluded from scope?

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

### Architecture comparison table template

When presenting an architecture comparison table, use this enriched template that distinguishes comparator roles:

```md
| 方案 | 比较角色 | 解决的问题 | 成熟度 | 关键优势 | 关键代价 | 最适合场景 | 不适合场景 | 核心权衡维度 |
|------|----------|------------|--------|----------|----------|------------|------------|--------------|
```

The table should be followed by a short interpretation:

- **Load-bearing dimensions:** which dimensions drive the final recommendation (and why the others are background)
- **Reversal conditions:** what specific change (ecosystem maturity, performance threshold, cost constraint, etc.) would change the recommendation

## Benchmark comparability for technical deep-dive

When a technical deep-dive report's conclusions depend on benchmark numbers — latency, throughput, accuracy, cost, token-level metrics, or similar quantitative claims — the report must disclose sufficient methodology context for the reader to assess comparability.

### Minimum disclosure fields

For each load-bearing benchmark number, the report must disclose the following. Not every field is applicable to every benchmark; mark genuinely inapplicable fields as `N/A` rather than omitting them silently.

- **Model / system version**: which model, software version, or system configuration was benchmarked. For AI/ML benchmarks, include parameter scale, quantization level, and framework version where relevant.
- **Workload / dataset / task type**: what specific task, query type, dataset, or workload was used in the measurement. If the workload is proprietary or described only in a referenced paper, state the reference.
- **Hardware / environment**: inference or testing hardware (CPU/GPU/TPU, memory), whether local or cloud, and any environment details that affect runtime characteristics.
- **Metric definition**: what exactly was measured — p50/p95 latency, generation-only latency, end-to-end latency, throughput (tokens/s or requests/s), accuracy (F1, Exact Match, human eval), groundedness, citation precision, cost per token or per query. Do not use bare terms like "latency" or "accuracy" without specifying the operational definition.
- **Measurement scope**: what is included in the measurement — whether retrieval, preprocessing, re-ranking, tool calls, post-processing, or other pipeline stages are part of the timing or cost, or whether only the core generation/inference phase is measured.
- **Concurrency / batch / context**: batch size, concurrency level, context length, or other load parameters that materially affect the metric.
- **Source role**: whether the number is an observed benchmark result from a controlled experiment, a vendor-reported claim, a proxy derived from related work, an analytical assumption, or a model output from estimation. For observed benchmarks, state how the measurement was conducted (internal experiment, published paper, third-party evaluation provider).

### Cross-source comparability

When numbers from different sources, papers, or products appear in the same analysis or comparison, the report must explicitly note comparability boundaries — different hardware backends, different metric types (e.g., single-stream decode vs. server throughput), different workload patterns, or different measurement methodologies. Silently juxtaposing numbers from incompatible contexts creates a false appearance of comparability.

### Graceful degradation

If a required field cannot be populated because the original source did not report it, the report should:
1. note the gap explicitly (e.g., "the source does not disclose hardware"),
2. assess whether the missing information could materially change the conclusion, and
3. adjust confidence or claim strength accordingly.

### Relationship to route-specific rules

- For **Technical Deep-dive** reports, the general disclosure fields above apply.
- For **Equipment Selection / Procurement** reports, additional route-specific benchmark comparability rules apply — see `ROUTING-MATRIX.md` §Equipment Selection Hard Fail and `checklists/final-audit.md` §Recall discipline (equipment-selection items).

## Common failure modes

Watch for these failure patterns:

1. **Pure technical survey without judgment**: describes technology but does not evaluate or recommend
2. **Missing comparison dimensions**: compares on only 1-2 dimensions when 4-5 are decision-relevant
3. **Stale technical state**: uses outdated version numbers, deprecated features, or superseded benchmarks
4. **Vendor claims treated as technical facts**: marketing specs mixed with engineering evidence
5. **Roadmap optimism**: treats announced features as shipped capabilities, or mixes stable/shipped, experimental, deprecated, announced, proposed, and rumored states into one undifferentiated layer
6. **Ignoring operational burden**: focuses on capabilities while ignoring deployment, maintenance, and scaling costs
7. **Patent counting without analysis**: lists patents without understanding technical coverage or freedom-to-operate
8. **Missing audience and decision scene**: technical analysis opening lacks audience definition, decision scenario, or version baseline — reader cannot tell who the report is for or what decision it supports
9. **Baseline-date-source conflict**: the report's stated coverage date, technical version, or current-state anchor is inconsistent with its source timeline — the "current state" baseline is temporally broken

## Output structure

A technical analysis report should visibly show:

- **Opening structure**: the report's front page must define the target audience, decision scenario, and technical baseline (version, date anchor, stable vs. forward-looking boundary) before entering detailed analysis. See `references/report-template.md` §Technical deep-dive opening for the template.

### For principle analysis
- Core mechanism explanation
- Key components and interactions
- Fundamental constraints
- Comparison with alternatives

### For architecture comparison
- Candidate architectures with comparator roles (direct substitute / complement / lower-level primitive / higher-level runtime or platform / historical or design ancestor / unsuitable comparator — with exclusion rationale)
- Comparison dimensions with explicit criteria
- Dimension-by-dimension analysis
- Trade-off summary with load-bearing dimensions identified
- Recommendation with conditions and reversal criteria

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

## Security deep-dive: threat modeling add-on

当技术分析任务的主要负担是**安全风险**时（如协议安全评审、工具/架构安全分析、攻击面评估），报告不应只输出"风险清单并逐项解释"，还应输出类似安全架构评审的材料。本小节提供可选但强推荐的威胁模型 + 工程控制输出模板。

> **启用条件：** 仅当安全风险是报告的主负担时使用。如果技术分析只涉及少量安全注意点（如作为技术原理的一部分简要提及），无需启用本小节。

### 资产 (Assets)

明确列出需要保护的核心资产。资产应具体到可操作粒度，而非泛泛的"用户数据"。

| 资产类别 | 示例 | 关键属性 |
|----------|------|----------|
| 用户数据 | 个人身份信息、凭据、密钥、会话令牌 | 机密性、完整性 |
| 本地资源 | 文件系统、进程内存、本地服务 | 访问控制边界 |
| 远程权限 | API token、OAuth 凭据、服务账户 | 授权范围 |
| 会话状态 | 登录状态、操作上下文、临时数据 | 时效性与隔离 |
| 模型上下文 | Agent 记忆、工具调用链、推理状态 | 跨会话污染风险 |
| 供应链组件 | 依赖库、扩展包、容器镜像 | 来源与更新机制 |

### 攻击者 (Threat Actors)

描述可能攻击系统的角色及其能力假设。避免只写"攻击者"而不区分能力等级。

| 攻击者类型 | 能力假设 | 典型入口 |
|------------|----------|----------|
| 恶意 server | 控制协议端点，可发送任意响应 | 网络通信信道 |
| 恶意网页/客户端 | 控制用户交互层，可注入任意输入 | 用户输入接口 |
| 受污染 registry | 在包/扩展分发渠道中植入恶意内容 | 安装/更新流程 |
| 被入侵参考实现 | 官方或社区实现包含后门/漏洞 | 代码依赖 |
| 带漏洞 SDK | 第三方库或工具链存在已知但未修复的漏洞 | 编译/运行时依赖 |
| 内部误配置 | 运维人员配置错误导致权限或网络暴露 | 部署与监控层 |

### 信任边界 (Trust Boundaries)

定义系统中哪些组件/环境是可信的，哪些是不可信的，以及信任传递的条件。

要点：
- **host-client 边界：** 本地主机与客户端进程之间的信任关系
- **client-server 边界：** 客户端与服务端之间的网络通信信任
- **local process 边界：** 同一主机上不同进程之间的隔离程度
- **remote HTTP 边界：** 远程 API 调用的身份验证与传输安全
- **OAuth discovery 边界：** OAuth 端点发现流程中的信任假设
- **registry 边界：** 包/扩展注册表的验证机制与信任基础
- **model context 边界：** 跨会话上下文共享的安全假设

每条信任边界应说明：
- 跨边界的认证/授权机制是什么
- 边界被突破的后果是什么
- 是否有降级或旁路路径

### 攻击树 (Attack Tree)

用分层列表或 mermaid 表达主要攻击路径。攻击树应展示攻击者如何从入口逐步达成目标。

示例（分层列表格式）：
```text
攻击目标：获取远程 API 权限
├─ 1. 窃取有效 token
│  ├─ 1a. 网络嗅探（如果传输未加密）
│  ├─ 1b. 本地文件读取（如果 token 存储在未保护文件）
│  └─ 1c. 会话劫持（如果 token 绑定不充分）
├─ 2. 绕过认证
│  ├─ 2a. OAuth 端点欺骗
│  └─ 2b. 降级攻击（强制使用弱认证协议）
└─ 3. 权限提升
   ├─ 3a. 利用 API 授权校验缺失
   └─ 3b. token 作用域扩展漏洞
```

如果使用 mermaid，确保在纯文本环境中也可读。

### 风险优先级矩阵 (Risk Priority Matrix)

将风险项按可能性和影响分级，而不是等权列出。矩阵应明确优先级判断依据。

| 风险项 | 可能性 | 影响 | 优先级 | 依据与判断 | 首要缓解 |
|--------|--------|------|--------|------------|----------|
| Confused Deputy 攻击 | 中 | 高 | **高** | 协议设计未强制请求来源校验 | 引入来源绑定机制 |
| Token Passthrough 泄露 | 高 | 高 | **高** | 默认 token 传递机制无作用域收窄 | 实现最小权限 token |
| Session Hijacking | 中 | 中 | **中** | 依赖传输层安全，但本地进程可窃取 | 绑定 session 到客户端标识 |
| SSRF 攻击 | 低 | 高 | **中** | 需要特定网络条件，但成功则影响大 | 出站请求白名单 |
| 本地 Server 入侵 | 低 | 高 | **中** | 需要攻击者已有本地代码执行权限 | 进程隔离与最小权限原则 |

优先级分级建议：**高**（必须立即缓解）/ **中**（应规划缓解）/ **低**（接受或监控）。

### 缓解措施与工程控制 (Engineering Controls)

将缓解措施按**预防 / 检测 / 响应**分层，而非堆砌建议。

| 控制类型 | 措施 | 目标风险 |
|----------|------|----------|
| 预防 | 请求来源校验（origin/domain 验证） | Confused Deputy |
| 预防 | 最小权限 token（scope 收窄、短期有效） | Token 泄露 |
| 预防 | Session 绑定（绑定到客户端证书或 fingerprint） | Session Hijacking |
| 检测 | 异常 token 使用模式监控（IP/地理突变） | Token 窃取 |
| 检测 | 未授权出站连接告警 | SSRF |
| 响应 | 自动 token 吊销机制（检测到泄露时） | Token 泄露 |
| 响应 | 进程隔离与自动重启（server 进程崩溃/入侵后） | Server 入侵 |

对于每个控制措施，说明：
- 它是**现成**（已有标准/实现）、**需定制开发**、还是**概念性**
- 它的局限性（什么场景下会失效）

### 检测与监控建议 (Detection Signals)

明确需要记录哪些信号以检测安全事件或攻击行为。检测信号应是工程可落地的，而非原则性建议。

| 检测目标 | 信号 | 数据来源 | 建议阈值/频率 |
|----------|------|----------|---------------|
| 异常 API 调用模式 | 调用频率 / 端点分布突变 | API gateway 日志 | 基线 ±3σ |
| Token 滥用 | 同一 token 多 IP 来源 | 认证中间件日志 | 同一 token >2 源 |
| 未授权资源访问 | 403/401 频率上升 | 应用日志 | >5 次/分钟 |
| 供应链变更 | 依赖哈希变更 / 新版本发布 | 包管理锁文件 | 每次 CI 运行 |

### 短中长期推进路径 (Short/Medium/Long-term Roadmap)

| 时间范围 | 目标 | 具体措施 | 成功标准 |
|----------|------|----------|----------|
| 短期 (0-3 月) | 解决高优先级风险 | 实施来源校验、最小权限 token、session 绑定 | 高优先级风险均有关闭计划或已关闭 |
| 中期 (3-12 月) | 建立检测与响应体系 | 部署异常监控、自动化 token 吊销、定期渗透测试 | 检测覆盖率 >80% 已知攻击路径 |
| 长期 (12+ 月) | 安全架构内置化 | 威胁建模纳入设计流程、安全 review 门禁、供应链安全自动化 | 新功能上线前自动安全 gate 通过率 >95% |

## Control-plane / workflow-system architecture add-on

当被比较对象包含 agent、orchestrator、planner、tool loop、workflow engine、multi-step execution 或 stateful runtime 时，除通用比较维度外，必须从 control-plane 视角评估架构。本 add-on 提供 agentic/workflow 系统的专门维度。

> 本 add-on 不替代 §Security deep-dive：安全威胁建模是另一层附加纪律，control-plane add-on 是架构比较基本盘。两者可同时启用。

| 维度 | 关键问题 |
|------|----------|
| Control plane | 谁决定下一步？是否有 planner / router / evaluator / loop controller 决定动作序列？ |
| State & memory | 哪些状态是一等对象（conversation / task / checkpoint / knowledge memory）？如何持久化、隔离、清理？ |
| Tool & action surface | 系统能调用哪些工具/函数/API？每次调用是否有副作用？如何管理工具注册与权限？ |
| Dataflow & API | 数据流是同步流水线还是事件驱动/异步 workflow？接口是 request/response 还是 event stream？ |
| Error recovery | 失败后 retry、abstain、checkpoint、rollback、compensation 各如何处理？是否区分信息失败与工作流失败？ |
| Observability & permission | 能否追踪子步骤、工具调用、成本和证据来源？工具权限、知识源权限、memory write policy 如何控制？ |

引入 control plane 后，报告中还应评估新增的平台组件与运维负担（orchestrator、queue、state store、trace store、tool gateway 等）。

## Related references

- `references/forward-looking-discipline.md` — for forecasts, roadmap statements, announced-vs-rumored separation, forward-looking assumption chains, and technical roadmap adaptation. Use when the task involves technology roadmap evaluation. See also §Roadmap/feature state stratification above for state-level classification.
- `references/source-traceability-and-claim-citation.md` — for source type classification and inline citation. Use for all technical claims.
- `references/source-quality.md` — for source ranking dimensions and tie-break rules. Use when source credibility is ambiguous.
- `references/counter-evidence.md` — for actively seeking contradicting evidence. Use when the technical claim is contentious or high-stakes.
