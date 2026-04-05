# Comparative Distillation — BYD Report (GPT vs Minimax)

Use this file as a worked example of the comparative-distillation method.

---

## Case identity

- **Case name:** BYD company report comparative distillation
- **Date:** 2026-04-01
- **Research question:** Produce a deep-research report on BYD with company, financial, competitive, and investment-relevant analysis
- **Why this comparison matters:** The two reports cover the same company and broadly similar public facts, but differ materially in calibration, structure, and research-discipline execution. This makes the pair useful for extracting reusable skill improvements.
- **Report A:** GPT deep research (user-provided PDF)
- **Report B:** Minimax deep research (user-provided PDF)
- **Reference / stronger report (if any):** GPT deep research
- **Prompt(s):** Same topic / same company; exact prompt text not preserved in this file
- **Important scope or timing differences:** Both outputs were treated as same-topic paired reports. Exact prompt wording and source windows may differ slightly, so conclusions should focus on stable structural differences rather than one-off factual retrieval.

---

## Comparison purpose

This comparison is **not** for deciding which model is "better."

It is for identifying:

- which structural and disciplinary behaviors the stronger report shows
- whether the weaker report's gaps are missing-rule, missing-trigger, or execution problems
- which gaps deserve promotion into rules, checklist gates, or template changes

---

## Dimension 1: Current-state discipline

### Report A
- Treated market-position conclusions with visible conditionality rather than as flat timeless facts
- Did a better job separating reported/current observations from conclusions that depend on future execution

### Report B
- Used stronger flat market-position framing such as "中国市场绝对领导者：2025年国内新能源乘用车市场份额约35-40%"
- Scope boundary was partly implied, but dependencies and conditionality were not made visible enough

### Gap
The main difference is not raw knowledge. It is that GPT carries uncertainty and dependency structure into the conclusion, while Minimax tends to collapse current-position claims into flatter present-tense statements.

### Candidate action
Require every market-position or ranking conclusion to include both explicit scope and a conditional clause, or explicitly state that no major dependency was identified.

### Action type
`CHECKLIST_HARDENING`

---

## Dimension 2: Numerical and date discipline

### Report A
- Used precise figures when the source provided them: **4,272,145** / **4,602,436** vehicles, **194.705 GWh** / **285.634 GWh**, and exact financial figures rather than broad rounding
- Added explicit limitation notes when proxy indicators or approximate mappings were used

### Report B
- Used rounded figures such as "约460万辆" and "约5300亿元人民币"
- Rounded even in places like the executive summary, where exactness matters most
- Did not explain whether rounding was source-driven or just default smoothing

### Gap
GPT shows stronger numerical discipline in two ways: it preserves exactness when the source allows it, and it signals the limits of approximation when exact direct data is unavailable. Minimax tends to default to rounded presentation without enough justification.

### Candidate action
1. Use exact figures when the source provides exact figures; do not round by default.
2. When proxy indicators or approximate mappings are used, add a brief data-calibration note explaining the proxy and its limitation.

### Action type
`NEW_RULE`

---

## Dimension 3: Source traceability and evidence weighting

### Report A
- Did not use Minimax-style `[CONF] / [LIKELY] / [UNCERTAIN]` labels consistently, but often made source type visible through attribution and evidence-strength framing
- Included an explicit evidence-strength hierarchy and used it to help the reader understand what kinds of evidence supported key conclusions

### Report B
- Used `[CONF] / [LIKELY] / [UNCERTAIN]` labels, which is structurally useful
- But labels were dropped in some places and were not paired with a reader-facing evidence-tier definition
- Strong claims still lacked enough visible evidence-weight explanation

### Gap
GPT was better at teaching the reader how to interpret evidence quality; Minimax had a useful label system but weaker explanatory scaffolding and weaker consistency.

### Candidate action
Combine the existing Minimax label system with a required evidence-tier legend at the top of the report so labels are interpretable and evidence weight is reader-visible.

### Action type
`TEMPLATE_CHANGE`

---

## Dimension 4: Forward-looking claim discipline

### Report A
- Forward-looking statements were usually attributed to a named source, such as company guidance cited via Reuters
- Even without an explicit uncertainty tag, the sourcing made the confidence structure more legible
- Forecast-like language often carried implicit limitation signals

### Report B
- Used bare forward-looking wording such as "2025年海外销量预计超100万辆"
- Did not attribute the estimate to a named source
- Did not consistently label the statement as uncertain in a way visible to the reader

### Gap
The key difference is not just that GPT sounds more careful. It explicitly anchors forward-looking statements to a named source, while Minimax often uses forecast language as if the word "预计" itself were enough.

### Candidate action
Require every forward-looking figure, roadmap statement, or target-style claim to name the source of the estimate — for example, company guidance, analyst estimate, media-reported target, or model inference.

### Action type
`CHECKLIST_HARDENING`

---

## Dimension 5: Structural readability and information density

### Report A
- Used explicit meta-level notes such as "数据口径说明" to orient the reader before they hit ambiguity
- Presented some tensions and limitations in reader-friendly explanatory form rather than burying them later
- Generally made the structure easier to interpret as an analytical document rather than a data dump

### Report B
- Had the beginnings of useful structure through confidence labels
- But still showed a tendency toward denser summary formulations and less explicit framing around what was estimated, proxied, or scope-sensitive
- Reader interpretation relied too much on inference rather than on visible scaffolding

### Gap
GPT improved readability not through prettier prose, but through explicit structural aids that reduced reader ambiguity. The strongest reusable pattern here is not tone; it is the use of short interpretive framing elements that make the report easier to audit.

### Candidate action
When proxy indicators, approximate mappings, or scope-sensitive metrics are used, require a short data-calibration paragraph near the relevant section instead of leaving limitations implicit.

### Action type
`TEMPLATE_CHANGE`

---

## Dimension 6: Decision usefulness

### Report A
- Framed competition using the right unit of comparison rather than defaulting to unit volume
- Paired scale growth with profitability and cash-flow pressure in a single conclusion, e.g. the "规模仍在扩张、盈利与现金回收承压" pattern
- Helped the reader think about what actually matters in an investment-relevant interpretation

### Report B
- Reported competition and scale reasonably, but did not consistently reframe the competitive question around the best comparison unit
- Reported positive and negative signals, but often in separate places rather than as a single load-bearing tension
- Made it harder for the reader to extract the real decision-relevant takeaway quickly

### Gap
GPT was more useful not because it had more facts, but because it surfaced the governing tension and comparison logic. This is a decision-utility difference that can be made teachable.

### Candidate action
1. Require competitive comparisons to state the right unit of comparison for the question being answered.
2. When scale growth and profitability/cash-flow pressure coexist, present them together as one tension rather than separating them into different sections.

### Action type
`NEW_RULE`

---

## Candidate-action summary

| # | Candidate action | Failure family | Action type | Proposed home |
|---|---|---|---|---|
| 1 | Market-position conclusions require scope + conditional clause | current-state / time-layer discipline | CHECKLIST_HARDENING | `checklists/final-audit.md` |
| 2 | Use exact figures when source provides exact figures | current-state / time-layer discipline | NEW_RULE | `references/finance-date-discipline.md` |
| 3 | Add data-calibration note when using proxies or approximate mappings | output structure / information density | TEMPLATE_CHANGE | `references/report-template.md` |
| 4 | Add evidence-tier legend at report top | source traceability / evidence weighting | TEMPLATE_CHANGE | `references/report-template.md` |
| 5 | Every forward-looking figure must name the source of the estimate | forward-looking claim discipline | CHECKLIST_HARDENING | `checklists/final-audit.md` + `checklists/forward-looking-claims.md` |
| 6 | State the right unit of comparison in competitive analysis | research depth / briefing drift | NEW_RULE | `references/report-template.md` |
| 7 | Pair scale growth with profitability/cash-flow pressure when both exist | decision utility | NEW_RULE | `references/report-template.md` + `checklists/final-audit.md` |

---

## Triage notes

### Candidate 1
- **Why it matters:** Flat ranking or leadership claims easily overstate certainty in fast-moving or definition-sensitive markets.
- **Why it is reusable:** This problem recurs across company and market reports, not just BYD.
- **Why this home is best:** This is primarily an enforcement problem at delivery time, so final-audit checklist hardening is the right home.
- **Promotion status:** `PROMOTE_NOW`

### Candidate 2
- **Why it matters:** Default rounding degrades analytical precision and can hide whether a number is sourced or loosely recalled.
- **Why it is reusable:** Exact-vs-rounded numeric discipline applies broadly across company, industry, and investment reports.
- **Why this home is best:** `finance-date-discipline.md` is already the repo's home for numeric and time-sensitive claim discipline.
- **Promotion status:** `PROMOTE_NOW`

### Candidate 3
- **Why it matters:** Readers often misread proxy measures as direct observations unless limitations are made explicit.
- **Why it is reusable:** Proxy indicators recur in market-share, capacity, deployment, and industry-sizing work.
- **Why this home is best:** This is mainly a presentation and report-structure aid, so `report-template.md` is the best home.
- **Promotion status:** `PROMOTE_NOW`

### Candidate 4
- **Why it matters:** Confidence labels without a visible legend make the system less interpretable to the reader.
- **Why it is reusable:** The same problem will recur whenever structured confidence labels are used.
- **Why this home is best:** This is a required report-header design decision, so it belongs in the report template.
- **Promotion status:** `PROMOTE_NOW`

### Candidate 5
- **Why it matters:** Bare forecast language creates false confidence and weak auditability.
- **Why it is reusable:** This issue recurs in roadmaps, pricing, estimates, guidance, and target-price style writing.
- **Why this home is best:** This is both a forward-looking discipline issue and a final delivery gate issue.
- **Promotion status:** `PROMOTE_NOW`

### Candidate 6
- **Why it matters:** Competitive analysis becomes shallow when the comparison unit is wrong.
- **Why it is reusable:** The same logic applies across vehicles, semiconductors, software, batteries, and many other industries.
- **Why this home is best:** This is an analytical pattern best taught in the default report template.
- **Promotion status:** `PROMOTE_NOW`

### Candidate 7
- **Why it matters:** Separating positive scale signals from negative profit signals weakens decision usefulness and hides the core tension.
- **Why it is reusable:** This pattern recurs across growth-company and industry reports.
- **Why this home is best:** The reporting pattern belongs in the template, while enforcement belongs in final audit.
- **Promotion status:** `PROMOTE_NOW`

---

## Things explicitly rejected

| Observation | Why rejected |
|---|---|
| GPT is simply "better" overall | Too vague; not an actionable skill improvement |
| GPT sounds more natural | Tone preference only; not a reliable or auditable rule |
| Minimax should copy GPT's exact prose style | Content mimicry, not reusable discipline |
| GPT had more evidence labels than Minimax | Not true in a stable structural sense; the better lesson is evidence-tier interpretability, not raw label count |

---

## Final judgment

### What the stronger report did better
GPT showed stronger **disciplinary scaffolding around knowledge expression**. The main advantages were not raw knowledge differences but better numeric precision, explicit limitation handling, better evidence interpretability, more disciplined estimate sourcing, stronger comparison framing, and clearer tension reporting.

### What should change in the repo now
The repo should promote the accepted candidates into:
- stronger numeric discipline
- explicit proxy/data-calibration notes
- evidence-tier legend in the report header
- named-source requirement for forward-looking claims
- explicit unit-of-comparison discipline
- paired presentation of scale and profitability/cash-flow signals
- stronger final-audit enforcement for ranking and estimate claims

### What should wait for another confirming case
No additional style-level findings should be promoted without another case. In particular, broad judgments about tone, fluency, or "report feel" should wait unless they can be rewritten as structural rules.

### Is this mainly a missing rule, missing trigger, or execution problem?
This case is mostly a **missing-rule + checklist-hardening** case. Several strong patterns were not yet formalized clearly enough in the repo at the time of comparison, while some others needed stronger delivery-time enforcement rather than more prose explanation.

---

## Minimal quality bar

- [x] the two reports are comparable enough to justify distillation
- [x] the comparison used the six fixed dimensions
- [x] each accepted candidate has an action type
- [x] each accepted candidate has a proposed repo home
- [x] at least one rejected observation is documented when relevant
- [x] the final judgment distinguishes rule gap vs trigger gap vs execution gap
