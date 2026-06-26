# Regulatory Analysis Audit

Use this checklist before delivery when the primary route is **Regulatory / Policy Impact Analysis**.

This checklist verifies that the regulatory analysis route was executed correctly and the final artifact satisfies its contract.

---

## Route activation

- [ ] the task was explicitly classified as regulatory/policy impact analysis
- [ ] the regulatory analysis route was selected as the primary route (not as a secondary discipline)
- [ ] the route conflict check was run: confirmed this is not better served by listed-company, market entry, or market outlook routes

## Regulatory state verification

- [ ] current regulations are clearly separated from pending/in-progress legislation
- [ ] the regulatory snapshot is dated and sourced
- [ ] multiple jurisdictions are prioritized by binding impact (not treated as equivalent)
- [ ] enforcement reality is distinguished from letter-of-law analysis

## Evidence quality

- [ ] primary regulatory sources are used for load-bearing claims (official gazette, regulatory filings, government publications)
- [ ] media interpretation is distinguished from regulatory text
- [ ] analyst speculation is labeled as such, not presented as regulatory fact
- [ ] conflicting regulatory interpretations are handled explicitly
- [ ] source register must use the 7-column template (ID / Source Name / Source Type / Date / DOI or URL / Reliability / Claims Supported) defined in `references/source-traceability-and-claim-citation.md` (§Structured Source Register Template). 来源注册表必须使用该 7 列模板。

## Business impact analysis

- [ ] direct impact vs indirect impact is clearly separated
- [ ] impact is analyzed at business level (revenue, cost, operations, market access)
- [ ] quantified impact is provided where possible, with explicit assumptions
- [ ] impact timeline is stated (when will the regulation take effect?)
- [ ] （非阻塞）所有比较表、评分表、估算表包含数字角色列（或等效的表头角色行/表注），见 `references/quantitative-role-labeling.md` §表格中的角色标签

## Uncertainty and scenarios

- [ ] uncertainty bounds are explicitly stated (enforcement intensity, timing, possible exemptions)
- [ ] scenario analysis covers optimistic / base / pessimistic outcomes
- [ ] scenarios are grounded in evidence, not just speculation
- [ ] the report does not give false precision on regulatory timing
- [ ] [NON-BLOCKER] Scenario probabilities (e.g., `~25%`, `~50%`, `~25%`) must include the estimation method, assumptions, or source basis. If such justification cannot be provided, use qualitative directional labels (low / medium / high) instead of precise percentages. See also `checklists/market-outlook-audit.md` (§结构化多情景分析) and `checklists/quantitative-role-audit.md` (§Market Outlook) for related hard-fail gates.

## Business/industry implications

- [ ] actionable conclusions are provided for decision-makers
- [ ] monitoring signals are specified (what to watch for regulatory changes)
- [ ] the report distinguishes between "must comply now" and "prepare for possible future compliance"
- [ ] competitive implications are analyzed (how does this affect relative positioning?)

## Hard fail check

Fail if any of these are true:

- [ ] regulations are listed without business impact analysis
- [ ] regulatory text is confused with media interpretation
- [ ] false precision is given on regulatory timing without uncertainty bounds
- [ ] enforcement reality is ignored (letter-of-law vs actual enforcement)
- [ ] all jurisdictions are treated as equivalent without prioritizing binding regimes
- [ ] regulatory risk is presented as binary (yes/no) rather than graduated with scenarios

---

## Rule-system analysis (activate when rule/incentive/mechanism is the main burden)

这些检查项只对**规则系统改变参与者激励、策略空间或路径优势**是主负担的 regulatory 报告启用。如果任务以传统合规/政策影响分析为主（不涉及策略博弈或机制设计评估），跳过本小节。（激活条件与 `references/rule-system-and-mechanism-add-on.md` §启用条件一致。）

- [ ] 如果规则/赛制/激励机制是核心分析对象，报告是否包含了**状态分类**（state taxonomy）——用有限状态描述参与者在规则下的不同处境，而非泛泛的"有利/不利"
- [ ] 状态分类的每个状态是否说明了：参与者可用的策略空间、信息条件、可选动作路径
- [ ] 是否包含了**干预矩阵**（intervention matrix）——列出至少 2 个可比较的规则调整方案，每个方案包含：预期改善、副作用/意外后果、实施难度、需监测指标、反转条件
- [ ] 干预矩阵的每个方案是否具有可验证的反转条件（而非"可能需要进一步研究"）
- [ ] （非阻塞）如果干预矩阵中涉及定量估计，是否标注了 estimation method 和 confidence

## Final sign-off

- [ ] all items above are checked
- [ ] the report visibly satisfies the regulatory analysis artifact contract
- [ ] the route is evident in the report structure without needing to read hidden notes
