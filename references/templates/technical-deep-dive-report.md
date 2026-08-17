# Technical Deep-dive Report Template (route-specific)

**When to read:** only when the **technical-deep-dive** route is selected (see
the route's card in `references/routes/technical-deep-dive.md`). The core
default structure lives in `references/report-template.md`; this file adds the
route-aware opening and terminology-boundary table.

### Technical deep-dive opening (route-aware)

For Technical Deep-dive / Architecture Analysis reports, the front page should include a structured opening block that defines the report's audience, decision scenario, and temporal baseline before entering technical analysis.

Suggested template:

```
## 执行摘要

**适用读者**：安全工程师 / 协议设计者 / 平台架构师 / 产品技术负责人（按任务选择）

**决策场景**：本报告用于判断 [技术/协议/架构] 是否适合 [采用/部署/迁移/集成/继续投入]，以及需要补哪些工程控制。

**技术基线**：
- 报告日期：YYYY-MM-DD
- 稳定版本 / 当前规范：...
- 最新验证日期：YYYY-MM-DD
- 前瞻内容边界：路线图、实验扩展、社区提案不计入当前稳定能力

**一句话判断**：...
```

When the report uses sources with different temporal statuses (current spec vs. roadmap vs. experimental), the baseline block should make the role of each source type visible. This prevents the "coverage date in metadata conflicts with source timeline" failure mode — a common issue in protocol deep-dives where the report claims a coverage date but cites sources from a later specification version or roadmap announcement.


#### Terminology boundary (for definition-sensitive technical topics)

For technical deep-dive topics where key concepts carry multiple or contested definitions (e.g., "Agentic RAG" as academic term vs. engineering paradigm vs. vendor label), include a terminology-boundary table before the detailed comparison. This helps the reader understand which definition the report adopts and what is excluded from scope.

| 概念 | 原始/严格定义 | 当代工程定义 | 本报告采用定义 | 排除边界 |
|---|---|---|---|---|
| [概念 A] | [原始论文/出处定义] | [当前工程/行业用法] | [本文采用的定义] | [明确排除的范围] |
| [概念 B] | [原始论文/出处定义] | [当前工程/行业用法] | [本文采用的定义] | [明确排除的范围] |

**操作性定义**：本文将 [概念 X] 归入 [分类 Y]；将 [情形 Z] 排除在外，理由是 [理由]。

This table is optional but strongly recommended when the topic involves concepts with multiple competing definitions. It does not replace the 7-column Source Register.
