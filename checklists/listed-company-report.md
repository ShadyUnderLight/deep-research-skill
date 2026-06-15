# Listed Company Report Checklist

Use this checklist when the research is about a publicly listed company.

Run through every item before delivering the final report.

## Market snapshot (对照 references/report-template.md §Market snapshot table)

- [ ] 市场快照表已填入完整数据（对照模板必填列：当前股价/快照日期/市值/PE (TTM)/PE (Forward)/PB/PS/52周区间/股息率）
- [ ] 每项指标都标注了具体数据来源和快照日期
- [ ] 数据来源优先使用实时金融数据平台或交易所披露，而非过时或间接来源

## Reporting discipline

- [ ] **research-anchor block is present and complete** — the report includes a visible block before broad analysis that locks: latest full-year reported period (FY), latest quarterly / interim reported period, latest current market snapshot date, and latest management / leadership state when decision-relevant
- [ ] latest full-year financial figures are sourced from annual report, earnings release, or filed disclosure
- [ ] latest quarterly / interim figures are sourced from the newest reported period reasonably available at the report date
- [ ] if the memo date is materially later than the supposedly "latest" figures used, freshness was re-checked before synthesis
- [ ] if the research-anchor block originally contained a stale or mis-timed quarter / interim period, synthesis was stopped and the anchor was corrected or explicitly downgraded before delivery
- [ ] financial figures are labeled by type: audited annual / interim / earnings release / analyst consensus / inferred
- [ ] historical reported facts are separated from current market snapshot
- [ ] forward-looking targets or estimates are clearly labeled as such, not presented as confirmed facts
- [ ] evidence labels do not inflate claim strength — inferred or third-party claims are not labeled as "confirmed facts"; the highest label tier per claim matches the actual source strength; if a claim carries [Confirmed] / confirmed facts label, the source must support that tier (primary filing, company disclosure, or directly observed event); labels that overstate certainty relative to the evidence are downgraded before delivery (see `references/source-quality.md` for source-tier definitions)
- [ ] inline source citation format is consistent throughout the document — all `[SN]`/`[IN]`/`[UN]` tags use the same bracket style and spacing; mixing formats (e.g. `[SN]` in some sections and unformatted references in others) is flagged and aligned before delivery (see `checklists/source-traceability.md` for citation format requirements)
- [ ] older but still useful numbers are visibly labeled as historical background / older snapshot rather than treated as current-state anchors

## Valuation methodology

- [ ] valuation metric selection is justified by company characteristics (PE for stable earnings, PB for asset-heavy, PS for loss-making, EV/EBITDA for levered comparisons)
- [ ] loss-making companies do not force PE-based valuation without explicit justification
- [ ] cyclical companies are not valued at peak or trough earnings without cycle-stage labeling
- [ ] high-growth companies have forward metrics clearly labeled as estimate-based
- [ ] consensus target prices are presented with source, date, and analyst count when available (never inferred); target prices are not treated as fair value
- [ ] consensus data timing is checked against latest earnings releases; stale consensus is noted
- [ ] （非阻塞）估值方法包含倍数区间范围，以及可比公司选择逻辑或估值指标选择理由说明（对照 `references/report-template.md` §Valuation method and scenario analysis）
- [ ] （非阻塞）情景分析包含乐观/基准/悲观三档，每档有明确的 EPS 假设、PE 倍数和触发条件

### Capital return discipline (CapEx-heavy 公司适用)

适用触发条件：公司属于半导体制造、工业制造、能源、电力、数据中心、通信基础设施等资本密集型业务，或 CapEx / 收入长期高于 20%，或核心 thesis 依赖产能扩张/新节点爬坡/海外建厂/重资产投入（完整定义见 `references/valuation-methodology.md` §Capital return discipline for CapEx-heavy companies → 触发条件）。

- [ ] （阻断级）当本纪律触发时，报告不得仅凭收入增长和 PE/PEG 得出估值结论；必须检查 FCF conversion / CapEx burden / D&A / ROIC，并在估值章节而非仅风险章节处理这些变量
- [ ] （非阻塞）如果增长依赖新产能、新地区、新节点或重资产扩张，报告说明了初期 margin 稀释的时间范围与回收周期，而不是只提示"存在稀释风险"
- [ ] （非阻塞）FCF / CapEx / D&A 数字的角色和时间口径在转换表或正文中可见（观察值 vs 假设 vs 模型输出）
- [ ] （非阻塞）若 CapEx 强度、FCF 转换或 ROIC 等资本回收关键变量存在实质性不确定性（±20% 偏差可改变估值结论），最终结论降级为方向性或条件性判断，而非精确目标价

### DCF / 反向 DCF（当适用）

- [ ] （阻断级）当报告判断"长期增长是否已反映 / 是否透支"且公司有较长经营历史和正向自由现金流时，必须包含 DCF、反向 DCF，或明确说明不适用原因 — 缺此项则至多条件性通过（参见 `references/valuation-methodology.md` §DCF / reverse DCF trigger）
- [ ] （非阻塞）DCF / 反向 DCF 的关键假设列了数字角色、来源/方法和时间范围
- [ ] （非阻塞）至少一个高敏感变量有单变量敏感性矩阵或 tipping point（参见 `references/quantitative-role-labeling.md` §Sensitivity classification）
- [ ] （非阻塞）目标价 / 股权价值区间可由披露假设复算
- [ ] （非阻塞）多变量三情景不替代单变量敏感性分析（参见 `references/quantitative-role-labeling.md` §Sensitivity classification，该处已说明"情景分析 ≠ 敏感性分析"）

## Reporting-period discipline

- [ ] TTM / LTM figures are labeled as derived, not confused with reported fiscal year
- [ ] preliminary earnings-release figures are labeled as preliminary
- [ ] restated figures are used when available, with restatement noted
- [ ] fiscal year vs calendar year distinction is explicit when it affects the claim

## Stale-anchor hard-fail gate

- [ ] stale-anchor hard gate: a missing, stale, or mis-timed research-anchor layer — latest full-year, quarterly / interim, or current market snapshot — invalidates the memo unless synthesis was stopped, the anchor was re-checked, and the anchor was corrected or visibly downgraded before continuing — per SKILL.md fail-fast rule
- [ ] this gate applies regardless of whether listed-company is the primary route or a secondary/sub-route (per ROUTING-MATRIX.md "Secondary route hard-fail requirement")
- [ ] （阻断级）追加触发条件（适用于 primary 和 secondary route）— 存在以下任一情况则触发 stale-anchor hard-fail，无论 anchor block 形式是否完整：a) 报告日期晚于交易所/公司官网的公告披露日期，且已发布的年度/半年度/季度报告未被纳入（即使报告声称"未获取"）；b) 报告将已公开的关键财务数据（营收、利润、现金流）当作未知值处理；c) 自上市之日起不足 2 年的公司，最近的已发布业绩公告未纳入

## Current product lineup

- [ ] current flagship product generation verified (not stale)
- [ ] current pricing or price range verified with date
- [ ] latest major announcement or release confirmed
- [ ] product lifecycle stage: announced / pre-order / shipping / discontinued

## Listing status

- [ ] listing exchange and ticker confirmed
- [ ] current trading status: actively trading / suspended / delisted / in process
- [ ] if IPO pending or in process, current stage: filed / accepted / under review / approved / issued

## Key numbers are complete

- [ ] revenue with period and growth rate
- [ ] gross margin or net margin where relevant
- [ ] operating cash flow direction noted
- [ ] segment breakdown if multi-segment business
- [ ] the report makes visible which numbers belong to the latest reported annual period, which belong to the latest reported quarter/interim period, and which belong only to older historical context
- [ ] （非阻塞）所有比较表、评分表、估算表包含数字角色列（或等效的表头角色行/表注），见 `references/quantitative-role-labeling.md` §表格中的角色标签

## Judgment-shape micro-audit

- [ ] the opening section states the current thesis before long background exposition begins
- [ ] the opening page makes the thesis, key risks, and key unknowns easier to see than methodology notes or evidence-label legends
- [ ] the report identifies the few disclosures or variables that most determine the current view, rather than spreading importance evenly across many company facts
- [ ] the 3-5 claims doing the most thesis work are auditable in the body text rather than only indirectly recoverable from a source list
- [ ] the report distinguishes what currently supports the thesis, what currently weakens it, and what remains unresolved
- [ ] support / weakening / unresolved are visible in the opening 20-30% of the report, not only scattered later across sections
- [ ] if one unresolved variable dominates the case, it is named as such rather than diluted inside a general risk list
- [ ] the unresolved variable visibly narrows confidence, timing precision, valuation precision, or recommendation strength rather than remaining a decorative caveat
- [ ] competition is written as actual thesis pressure or threat-window analysis rather than mostly a peer directory
- [ ] valuation, growth, market position, and strategic narrative are not blended into one undifferentiated bullish or bearish mood
- [ ] if the view is positive but not valuation-grade, timing-grade, or precision-grade, the downgrade boundary is explicit
- [ ] asset injection, restructuring, one-off financing, M&A, or other major corporate actions are split into: confirmed transaction facts / likely operating impact / open uncertainty about realization, timing, synergy quality, or dependency on external variables

### Time-horizon valuation stratification (适用于"是否充分反映长期增长"类问题)

- [ ] （阻塞：无分层则至多条件性通过）当任务涉及"是否充分反映长期增长 / 是否便宜 / 是否透支"时，opening 区分了短中期（1-3年 / 3-5年）已定价部分与长期（5-10年）未定价 optionality，而不是只给出一个方向性判断（见 `references/report-template.md` §Time-horizon valuation stratification）
- [ ] （非阻塞）报告明确列出了 3-5 个估值驱动变量（如需求规模、份额捕获、利润率转换、估值透支等），并解释了为什么它们比背景事实更重要；这些变量驱动了报告章节顺序
- [ ] （非阻塞）投资行动含义与时间层次一致：不把"长期可持有"写成"当前明显低估"；如果短期已充分定价但长期仍有上行空间，行动选项反映这种张力

## Monopoly / moat / scarcity discipline

- [ ] monopoly, oligopoly, strong moat, market leadership, and listed-market proxy scarcity are clearly separated when defensibility is central to the task
- [ ] A-share-only listed uniqueness is not used as shorthand for industry exclusivity
- [ ] `唯一` / `only` / `sole` / `永久` / `permanent` / `不可替代` / `irreplaceable` / `无竞争对手` / `>90%` style wording appears only when the source support matches that exact strength
- [ ] if source support is weaker than wording strength, the wording is visibly downgraded
- [ ] load-bearing market-share, ranking, or exclusivity claims include time window, scope, and denominator when relevant
- [ ] issuer-sourced or media-mediated positioning claims are not upgraded into confirmed industry facts too easily
- [ ] if the report screens for scarce or monopolistic companies, category boundaries are visible in the final ranking rather than hidden in caveats
- [ ] （非阻塞）绝对化声明（"唯一"/"首家"/"最大"）标注了范围口径（按收入/按用户/按地域）和验证来源
- [ ] （非阻塞）如果缺少排他性验证，措辞已降级为"领先"/"头部之一"
- [ ] （阻断级）即使 moat/scarcity 框架结构正确，正文措辞仍必须匹配框架；框架正确 ≠ 正文可以使用框架不允许的措辞级别。扫描全文的绝对化措辞（列表参见 `references/moat-monopoly-screening.md` §Strong-claim wording discipline，含中文等价表述）并验证每个的证据基础

## Flags

If any item above is unchecked or uncertain, note the limitation explicitly in the report before delivery.
