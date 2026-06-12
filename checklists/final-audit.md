# Final Audit Checklist

Run through every item before delivering any deep research output.

This is the last gate before the report goes to the user. If any item fails, revise before delivery.

## Core question answered

- [ ] the report answers the user's actual question, not just the general topic
- [ ] the most important 2-3 variables are clearly stated and supported
- [ ] the bottom line is clear and actionable

## Evidence quality

- [ ] no major claim rests on a single weak source
- [ ] evidence hierarchy is visible: confirmed facts, well-supported inferences, and weak claims are not mixed
- [ ] key numbers are sourced and dated
- [ ] load-bearing claims are traceable in the body text, not only recoverable from a source appendix or bibliography
- [ ] strong-sounding comparative or forecast claims have explicit scope and source role, or were visibly downgraded
- [ ] PRIMARY_COMPANY / PRIMARY_PARTNER / 简化类型的 vendor-claim 来源（或 register Notes 列标注"厂商自述"的来源），在正文引用时附加了内联说明 `(来源：厂商自述，非独立验证)`，不得在缺少该限定的情况下标注为 [已确认事实]（见 `references/source-traceability-and-claim-citation.md` §来源标注一致性）
- [ ] SECONDARY_MEDIA / SECONDARY_ANALYST 类型来源（媒体估计、券商研报）未在正文中标注为 [已确认事实]（已使用 [推断] 或具体来源角色替代）；例外（指 register 标为 high reliability 且经审计确认）已在 process log 或审计状态区块中记录理由（见 `references/quantitative-role-labeling.md` §映射表使用规则）
- [ ] 每条正文证据标签不超过 `references/quantitative-role-labeling.md` §来源类型到证据标签的校准规则 中对应来源类型允许的最大标签强度；例外已记录理由

## Counter-evidence

- [ ] the strongest argument against the main conclusion is present
- [ ] competing explanations are noted where relevant
- [ ] limitations and risks are explicit, not buried
- [ ] each high-confidence conclusion has a corresponding structured counter-argument (see `references/counter-evidence.md` template)
- [ ] counter-arguments are based on real evidence or reasonable logic, not strawman
- [ ] if a counter-argument is rated "strong", the conclusion has been visibly adjusted (confidence downgrade, constraints, or reversal condition)

## Uncertainty

- [ ] what could not be verified is stated explicitly
- [ ] confidence levels match evidence quality
- [ ] the report does not claim more certainty than the evidence supports

## Counter-evidence and review integrity

- [ ] the report's load-bearing conclusions are visibly pressure-tested rather than only supported
- [ ] there is visible counter-evidence handling for the main recommendation, ranking, or prioritization
- [ ] the report shows what weakens the conclusion, not just what supports it
- [ ] where uncertainty remains, it changes confidence, timing, ranking, or action in a visible way
- [ ] if alternatives remain credible, the report explains why they did not win now
- [ ] there is visible evidence that the research was narrowed, redirected, or stopped intentionally rather than merely exhausted

## Process-artifact sufficiency

- [ ] there is enough process structure to explain how the final answer was formed
- [ ] the selected route is recoverable from the process artifact rather than only the final prose
- [ ] load-bearing claims are traceable through at least a minimal claim and source structure
- [ ] meaningful uncertainties are recorded rather than only implied
- [ ] where the task warrants it, counter-evidence handling is recoverable from the process artifact
- [ ] required audits are named and statused rather than merely assumed
- [ ] the artifact includes a standardized route-and-audit-status block (via `references/report-template.md` §Route and audit status), with audit run status visible in the artifact itself (not only in a process log)
- [ ] the audit status block matches the actual report body: each self-assessment claiming passage (✅ Passed or equivalent phrasing or emoji) in the block has corresponding visible execution evidence in the artifact body or structure; if the body shows missing citations, incomplete source register entries, missing route-required sections, or other hard-fail conditions, the block must reflect that status rather than claiming full passage （阻断级）

- [ ] Process-integrity gate（阻断级）: self-assessment inconsistency triggers delivery block
  - 触发条件：当第 57 行检查未通过时，此 gate 自动触发——审计状态块中任何 discipline 标为 ✅ 已通过，但正文检查显示该 discipline 未达标（正文缺少 `[SN]` 引用、Source Register 列不完整、缺少路由要求的章节）
  - 即使报告内容质量高，虚假的质量信号本身就是不可交付的状态——触发此 hard-fail gate 时报告视为未通过 final-audit，无论其他所有检查项通过与否
  - 此 gate 独立于其他所有检查项，是 final-audit 的最后防线

- [ ] （阻断级）Declared-not-executed gate: if the report declares a discipline in methodology, metadata, a legend, or an audit block, verify that the discipline is visibly executed in the body where it applies. Methodology declarations do not count as execution.
  - 数字角色标签体系（O/P/A/M or equivalent）→ key tables and load-bearing numbers must apply role labels at row, column, or table-note level. Declared but 0% applied to applicable body numbers → hard-fail. Declared but <50% applied → may not be marked ✅ Passed; conditional-pass ceiling.
  - 证据层级/评估框架（dual-dimension, multi-level, study design × venue prestige, etc.）→ body must include a source-level evidence mapping table covering at least the major or load-bearing sources. Declared but no source-level mapping → hard-fail when systematic; conditional-pass ceiling when partial.
  - Source Register → body must contain matching inline `[Sxx]` references or functionally equivalent claim-level citations. A register appendix with zero body citations → hard-fail. A register with substantial uncited inflation should be marked and cannot be used as proof of source-traceability pass.
  - 判断标准：部分执行 = declared framework with >50% of applicable body locations visibly applying it; 声明未执行 = <50%; 声明零执行 = 0% or no body-level mapping/citations.

- [ ] （Tier-2）每项审计的「证据」列附有与状态对应的具体引用，不可为空：
  - ✅ Passed → 执行证据位置（章节号、检查项编号或 register 条目）
  - ⚠️ Skipped / ❌ Not run → 决定理由在正文中的位置
- [ ] （Tier-2）自称通过项的证据列引用的章节/条目确实存在且满足对应审计要求：引用的章节号/标题在正文中真实存在（非虚构引用）；引用内容与审计要求实质匹配——如 source-traceability ✅ 引用"正文使用 [S01]-[SN] 引用，附录为 7 列 Source Register"，则需验证正文确有 `[SN]` 引用且 register 满足 7 列模板格式

  > Tier-2 说明：深度验证检查，不通过需记录理由但不必然阻断交付。区别于 Tier-1（阻断级，不通过不可交付）和 (非阻塞)（质量信号，不通过属于改进项）。
- [ ] (非阻塞) cross-chapter label consistency: the same data point uses the same evidence label across all chapters; if the uncertainty register lists an item, bull/bear sections that reference it should cross-reference or maintain a consistent confidence level
- [ ] if the task used a specialized route, there is visible evidence that the route was turned into an execution contract before full drafting

## Route execution integrity

- [ ] the selected primary route is inferable from the final artifact without relying on internal notes
- [ ] the report visibly satisfies that route's artifact contract
- [ ] if a close alternative route existed, the chosen route's logic is visible rather than merely asserted
- [ ] the required secondary disciplines for the selected route are visibly executed (note: "secondary disciplines" such as current-state verification differ from "secondary routes" — secondary routes have their own hard-fail verification requirement checked in the Recall discipline section)
- [ ] the report does not collapse back into generic overview mode despite route selection
- [ ] if the route implies recommendation, ranking, gating, or sequencing burden, the report actually carries that burden
- [ ] if scope completeness was required, the report's coverage boundaries are explicit; load-bearing geographies or segments are present; omissions are named rather than silent
- [ ] the opening 20-30% of the report already reflects the chosen route rather than reading like a reusable generic overview
- [ ] the route is visible not only in headers, but also in section order and burden allocation
- [ ] there is a visible bridge from route -> mandatory sections -> bottom-line conclusion
- [ ] if a route-specific section were removed, the report would materially lose decision logic rather than only lose formatting variety
- [ ] generic background, company history, market history, or option blurbs do not occupy the strongest early-report positions unless the route truly requires them

## Route label visibility (non-blocker)

- [ ] route-specific labels or structural markers declared in the route contract appear explicitly in the body text (e.g. "短名单"/"反转条件"/"底限判断"/"情景分析", "shortlist"/"reversal condition"/"floor judgment"/"scenario analysis"), not only implicitly in content
- [ ] this is a non-blocker check: implicit structure without explicit labels is a quality signal, not a hard fail
- [ ] this complements `checklists/route-activation-audit.md`'s Visible label check — route-activation-audit verifies at activation time, this re-verifies at delivery for defense-in-depth

## Company-report judgment audit

- [ ] the report reads like a judgment memo rather than only a strong descriptive overview
- [ ] the main conclusion is visible in the opening section rather than buried after background exposition
- [ ] the opening makes visible not only the thesis, but also the strongest weakening evidence and the key unresolved variable
- [ ] if the first 30-40% of background were removed, the core judgment would still remain clear
- [ ] issuer- or company-sourced claims are not upgraded into confirmed industry facts too easily
- [ ] `leading` / `unique` / market-share / industry-position / strategic-importance claims are independently supported or visibly downgraded
- [ ] the report distinguishes clearly among: company states X / filing states X / third-party evidence supports X / scope remains only partially confirmed
- [ ] for each load-bearing number, time window, sample boundary, denominator, and comparison basis are explicit when relevant
- [ ] each important metric is visibly identified as realized performance / management target / third-party estimate / analyst inference / media-reported figure when the distinction matters
- [ ] for asset injection, financing, restructuring, M&A, or similar corporate actions, the report separates confirmed transaction facts from likely implications and from open uncertainty
- [ ] open uncertainties do not remain cosmetic; they visibly narrow confidence, timing confidence, ranking strength, scenario weighting, or recommendation strength
- [ ] if a key technical, commercial, regulatory, or execution milestone is unresolved, the final judgment is correspondingly narrowed
- [ ] the competition section identifies who actually pressures the thesis, and on what timeline, rather than mostly listing peers and products
- [ ] the distinction between narrative competitors and execution competitors is clear when relevant
- [ ] the final PDF reads as a polished deliverable rather than a text export
- [ ] hierarchy, spacing, tables, and visual anchors support judgment rather than merely displaying information blocks

## Monopoly / moat / listed-proxy boundary audit

- [ ] monopoly, oligopoly, strong moat, market leadership, and listed-proxy scarcity are clearly separated when defensibility language is load-bearing
- [ ] any `唯一` / `only` / `sole` / `永久` / `permanent` / `不可替代` / `irreplaceable` / `无竞争对手` / `>90%` claim is supported by evidence strong enough for that exact wording strength
- [ ] if exact-strength support is missing, the wording is visibly downgraded rather than left in place with cosmetic caveats
- [ ] A-share uniqueness is not used as shorthand for industry exclusivity or supply-side monopoly
- [ ] secondary, aggregator, social, or retail-investor sources are not doing load-bearing work for monopoly-style final claims
- [ ] if the report screens or ranks companies by scarcity / monopoly / irreplaceability, the final ranking shows category boundaries rather than one undifferentiated defensibility scale
- [ ] a skeptical reader would not be able to point to multiple obvious overclaims in the final text
- [ ] （非阻塞）强定性声明（"不可逆"/"永久"/"结构性转变"）指明了时间范围或适用条件
- [ ] （非阻塞）"唯一"/"首家"/"only"声明具有排他性验证或已降级为"领先"/"头部之一"

## Completeness

- [ ] the report does not leave a strong impression while having weak substance
- [ ] every section either adds decision-relevant information or is cut

## Recall discipline

- [ ] current-state verification was run for fast-moving topics
- [ ] listing status and financial snapshot were verified for listed companies
- [ ] source traceability was applied for structured or investment-relevant outputs — 正文 load-bearing claims 有 `[Sxx]` 或功能等效引用（仅 `[CONF]/[INFER]` 等置信标签不满足追溯要求；`[IN]`/`[UN]` 是合规的 traceability 标注，区别于 `[INFER]` 置信标签）；未通过 `checklists/source-traceability.md` hard-fail gate 则视为不可交付
- [ ] scope completeness was checked when the report claims global, comprehensive, or industry-wide scope
- [ ] decision utility was checked when the report carries a recommendation, choice, judgment, or investment-style decision burden
- [ ] if multiple routes are declared (primary + secondary), the hard-fail conditions of each declared route are verified; secondary route hard-fail conditions are not skipped because the route is "secondary"; "covered elsewhere without independent run" does not satisfy this requirement — each condition must be independently verified or its inapplicability documented; if a condition is genuinely inapplicable, the reason is documented rather than skipped silently (see ROUTING-MATRIX.md "Secondary route hard-fail requirement")
- [ ] option-selection final audit was run for shortlist, ranking, or constrained-choice outputs
- [ ] for model/API/provider selection tasks, a current provider snapshot was verified before ranking or recommendation
- [ ] for China-mainland deployment decisions, accessibility, compliance, data residency, and SLA were treated as part of ranking logic when relevant
- [ ] when the report uses Chinese-language sources alongside English-language sources, cross-language conflicts were handled explicitly (see `references/source-quality.md` and `references/data-conflict-resolution.md`)
- [ ] for equipment-selection / procurement / home-server-planning tasks, the report is visibly a procurement memo rather than a broad route overview
- [ ] for equipment-selection / procurement / home-server-planning tasks, top recommendation, credible runner-up, and rejected routes are explicit rather than implied
- [ ] for equipment-selection / procurement / home-server-planning tasks, budget assumptions are explicit, especially drives, UPS, networking upgrades, accessories, and what is excluded
- [ ] for equipment-selection / procurement / home-server-planning tasks, minimum viable configuration vs recommended configuration are separated when that distinction materially affects the answer
- [ ] for equipment-selection / procurement / home-server-planning tasks, hardware route and system choice are visibly bound into one stack recommendation rather than treated as detached sections
- [ ] for equipment-selection / procurement / home-server-planning tasks, power, noise, maintenance burden, backup overhead, and expansion friction are treated as ranking variables when relevant
- [ ] for equipment-selection / procurement / home-server-planning tasks, the report segments recommendation by workload or operator persona when the answer materially differs by use case
- [ ] for equipment-selection / procurement / home-server-planning tasks, the hardware ↔ system fit includes software stack, deployment method, and maintenance mode, not only hardware specification
- [ ] for market-entry / regional-expansion / country-prioritization tasks, priority relative to alternatives, country shortlist, hard gates, and sequencing logic are explicit rather than implied
- [ ] for market-entry / regional-expansion / country-prioritization tasks, regional hub vs first beachhead vs later expansion market are separated when relevant
- [ ] for market-outlook / industry-evolution tasks, a current market snapshot was verified before forward-looking sections
- [ ] for market-outlook / industry-evolution tasks, drivers, blockers, scenarios, and stakeholder implications are explicit rather than implied
- [ ] for market-outlook / industry-evolution tasks, all forward-looking claims have visible source role and time basis; derived, modeled, or load-bearing forecasts also show key assumptions and failure / reversal conditions
- [ ] for market-outlook / industry-evolution tasks, forward-looking numeric claims containing `预计` / `预测` / `预期` / `将达` / `有望` / `expected` / `forecast` / `projected` / `estimated to` / `will reach` / `by 20xx` are not labeled `[确认]`, `[已确认事实]`, `[CONF]`, or `[Confirmed]`; >3 violations or any load-bearing scenario assumption labeled confirmed facts triggers hard-fail
- [ ] for market-outlook / industry-evolution tasks, structured multi-scenario analysis exists (at minimum base case + one alternative) with quantitative ranges on the same load-bearing metric and trigger conditions
- [ ] for market-outlook / industry-evolution tasks, stakeholder implications cover at least 3 distinct stakeholder types, not only investors
- [ ] for market-outlook / industry-evolution tasks, monitoring signals are actionable: at least 3 include threshold, cadence, source, and trigger-to-action mapping rather than only a reversal-condition list
- [ ] for market-outlook / industry-evolution tasks, the task's core output is direction/evolution/trajectory — not ranking, prediction, or selection among defined options
- [ ] for first-tier / top-tier / multidimensional positioning tasks, scope, metric, timeframe, and dimension-level conclusions are visible before any overall label
- [ ] for first-tier / top-tier / multidimensional positioning tasks, the report does not collapse geography, current products, roadmap products, ecosystem strength, traction, and capital-markets signaling into one vague prestige tag without an explicit aggregation rule
- [ ] for technical deep-dive / architecture analysis tasks, the report makes a technical judgment (not just a survey) and the judgment is supported by evidence
- [ ] for technical deep-dive / architecture analysis tasks, comparison dimensions are explicit and the analysis is dimension-by-dimension (not just a feature list)
- [ ] for technical deep-dive / architecture analysis tasks, technical state is current and vendor claims are distinguished from independently verified technical facts
- [ ] for regulatory / policy impact analysis tasks, current regulations are separated from pending/in-progress legislation
- [ ] for regulatory / policy impact analysis tasks, business impact is analyzed (direct vs indirect) and uncertainty is explicitly bounded
- [ ] for regulatory / policy impact analysis tasks, scenario analysis covers optimistic / base / pessimistic outcomes
- [ ] for academic / literature review tasks, evidence is assessed on two dimensions: study design quality AND publication venue prestige
- [ ] for academic / literature review tasks, publication type and peer-review status are labeled for each source
- [ ] for academic / literature review tasks, preprints are explicitly distinguished from peer-reviewed publications
- [ ] for academic / literature review tasks, search strategy is documented (databases, search terms with Boolean operators, inclusion/exclusion criteria, screening counts, search date) — required when the report claims "系统化综述" or "有限范围系统化综述". Methodology transparency must match the claimed review type; see `references/academic-evidence-hierarchy.md` §措辞纪律 (Wording Discipline) for wording requirements.
- [ ] for academic / literature review tasks, publication bias discussion exists (≥2 sentences covering direction judgment and conclusion adjustment)

- [ ] （阻断级）RECALL: 强措辞审计。扫描全文的绝对化措辞（列表参见 `references/moat-monopoly-screening.md` §Strong-claim wording discipline，含中文等价表述及学术语境"系统评述"/"系统综述"/"系统化综述"/"systematic review"）。每个出现位置必须有：a) 措辞已降级为范围化表述，或 b) 同时具备搜索范围/分母说明 AND 否定证据搜索记录。存在系统性多处违规（非偶发、非归因引语）→ 标记为不通过

## Precision and estimate sourcing

- [ ] every "预计 / 估计 / 预期 / 有望" in the report has a named source attribution (who expects this?)
- [ ] bare "预计" or bare "有望" without source = fail; go back and add "[据公司指引/据分析师/据媒体]预计" or "[据行业趋势/据管理层/据第三方]有望"
- [ ] forward-looking numbers are not upgraded to confirmed facts merely because the source is official or reputable; confirm the source event separately from the future outcome
- [ ] exact figures are used when source provides them; "约" only when source itself rounds
- [ ] quantitative outlook numbers are labeled as observed / inferred / scenario assumption / illustrative calculation when the distinction matters
- [ ] for constrained-choice / shortlist reports that use composite scoring, important quantitative inputs are labeled as observed fact / proxy / assumption / model output when the distinction affects trust in the recommendation
- [ ] when evidence buckets are used, the report does not stop at `confirmed / inference / unknown` if important numbers still function as proxy / assumption / planning-model output
- [ ] heuristic timing, cost, payback, or ROI-style claims are not written as if they were directly observed facts when they are closer to assumptions or planning-model outputs
- [ ] （非阻塞）所有比较表、评分表、估算表包含数字角色列（或等效的表头角色行/表注），读者无需回正文即可从表格行判断数字性质（观察值/代理指标/假设/模型输出）。单角色表可以在表注声明；多角色表必须有独立列或表头角色行。见 `references/quantitative-role-labeling.md` §表格中的角色标签

## Metric-scope audit

- [ ] for each load-bearing numeric claim, the report makes visible when relevant: time period, segment boundary, geographic scope, and unit vs revenue vs mix vs run-rate distinction
- [ ] for each load-bearing numeric claim, the report makes clear whether the number comes from a filing fact, management commentary, or an estimate
- [ ] market-share, cumulative-sales, segment-growth, customer-scale, and product-performance claims do not imply more precision or universality than the source supports
- [ ] if metric scope is incomplete or ambiguous, the claim is rewritten or downgraded with visible caveats
- [ ] valuation precision matches data quality and company characteristics: loss-making companies do not get precise PE valuations, cyclical companies do not get valuations based on peak/trough earnings, and forward metrics are labeled as estimate-based

## Valuation inference transparency (non-blocker)

- [ ] if a valuation range or target price is labeled as inference, the report states the multiple range, comparable selection logic, and scenario parameters (optimistic / base / pessimistic) and key assumptions
- [ ] metric selection justification is present when the chosen metric is not the obvious default for the company type
- [ ] these are non-blocker checks: failures indicate areas for improvement but do not block delivery
- [ ] this check complements the metric-scope audit above: metric-scope checks focus on data quality and precision, while this check focuses on methodology transparency

## Bull/bear structural symmetry (non-blocker)

- [ ] when both bull and bear case sections exist, they use the same structural format (same column breakdown, same evidence-label discipline)
- [ ] this is a non-blocker check: asymmetric structure is a quality signal, not a hard fail
- [ ] this check complements the "Risks and counter-evidence" section of the report template: the template requires counter-evidence content, this check requires structural symmetry

## Unknown-to-conclusion linkage

- [ ] for each major unknown or unresolved current-state gap, the report explains whether it limits directional judgment, quantitative precision, valuation confidence, ranking confidence, timing confidence, or recommendation strength
- [ ] caveats do not remain cosmetic; if a load-bearing unknown remains unresolved, the final conclusion narrows accordingly
- [ ] the report distinguishes clearly between a directional judgment that is still justified, a precise quantitative judgment that is not justified, and a valuation-grade or timing-grade judgment that is not justified
- [ ] when the evidence supports direction but not precision, the report explicitly downgrades from precise claim -> directional claim instead of keeping precise language with caveats attached
- [ ] when the evidence supports a shortlist but not a stable winner, the report downgrades to conditional lead / provisional ranking / close-call framing rather than overstating separation
- [ ] when an unresolved variable could realistically flip the recommendation, the report names the reversal condition rather than burying it in generic risk language
- [ ] if unknowns are concentrated in one load-bearing segment, geography, customer type, or time horizon, the report narrows scope rather than leaving the conclusion artificially broad
- [ ] if the report still gives a strong recommendation under unresolved load-bearing unknowns, it makes explicit why low-regret action is still justified despite those gaps

## Market position and ranking claims

- [ ] every market-position claim specifies scope: "中国市场" / "全球" / "按XX口径"
- [ ] every market-position claim includes a conditional clause or explicitly states "no dependencies identified"
- [ ] if the report uses `第一梯队` / `top-tier` / similar prestige labels, it states whether the label is dimension-specific or an overall classification and why that compression is justified
- [ ] "全球最大" / "市场领导者" / loose `第一梯队` language without scope and dependency = fail

## Profit + scale signal pairing

- [ ] when volume/scale growth is reported, profitability and cash flow signals are checked
- [ ] if both positive (scale up) and negative (margin down) signals exist in the same period, they are presented together in one sentence or adjacent bullets — not separated in different sections
- [ ] reader does not have to connect the dots themselves

## Front-page readability

- [ ] the front page mainly helps the reader grasp the report's judgment rather than the process behind it; check for metadata-first drift (evidence grading, audit status, route metadata, or process notes displacing core judgment) (see `references/decision-report-template.md` §Metadata-first drift warning)
- [ ] the thesis, key risks, and key unknowns are easy to identify within 10-15 seconds of scanning
- [ ] methodology detail does not displace judgment visibility on the front page; if the first screen displays evidence grading, audit status, route metadata, or process notes before the thesis, verify that an explicit exception applies (e.g., academic review method statement is the core output)
- [ ] the front page feels like a report opening rather than a process note or metadata dump

## Judgment visibility in layout

- [ ] key judgments are visually visible rather than only embedded in prose
- [ ] major sections include a visible takeaway, judgment, or summary block when the route carries recommendation or decision burden
- [ ] risks, unknowns, and reversal conditions are easy to locate
- [ ] the layout helps the reader scan the report's decision structure without reading every paragraph in order

## Visual hierarchy and scanability

- [ ] major headings and subheadings are clearly distinguished
- [ ] judgment blocks, risks, evidence notes, and unknowns are visually differentiated from body text
- [ ] long stretches of dense text are broken up when scanability would otherwise suffer
- [ ] the report can be skimmed without losing the main logic

## Table usefulness

- [ ] each table has a clear title or immediate interpretive context
- [ ] units, scope, and time basis are visible when relevant
- [ ] tables support a judgment rather than merely display data
- [ ] important tables are followed by a short interpretation of what matters most
- [ ] the reader can tell why a given table matters to the conclusion

## Mixed-script and target-language cleanliness

- [ ] Chinese text spacing is visually normal and not obviously stretched by export
- [ ] mixed Chinese-English text remains readable and stylistically consistent
- [ ] names, product terms, and other proper nouns are spelled consistently
- [ ] punctuation, brackets, dashes, dates, and percentages are stylistically aligned
- [ ] there are no visible formatting artifacts that reduce final-delivery credibility

## Delivery cleanliness

- [ ] no citation artifacts, retrieval syntax, placeholder entities, or rendering residues leak into the final report body
- [ ] markdown / PDF delivery does not expose internal labels, raw template markers, or unfinished placeholders
- [ ] the delivered markdown reads like an intentional report, not a tool dump, export residue, or stitched note bundle
- [ ] the final artifact has been checked specifically for leftover placeholders such as `TBD`, `TODO`, `XXX`, `[[placeholder]]`, `{citation}`, or unresolved bracket markers
- [ ] source notes, evidence labels, and section labels visible to the user are intentional reader-facing devices rather than leaked process scaffolding
- [ ] tables, bullets, spacing, and heading hierarchy improve scanability rather than making the report feel like a raw export
- [ ] presentation credibility leaks such as spelling mistakes, inconsistent naming, awkward table rhythm, orphaned headings, or obvious spacing artifacts are treated as delivery failures rather than cosmetic nits
- [ ] if PDF is delivered, the PDF was reviewed as a deliverable in its own right rather than assumed correct because markdown looked clean
- [ ] if markdown looked acceptable but PDF degraded structure, spacing, or readability, that is treated as a delivery failure rather than a minor rendering quirk

## Quality bar

A report that fails this checklist is not ready for delivery, regardless of length or apparent polish.

CJK spacing degradation or broken-export text rhythm should not be severe enough to reduce professional readability.
