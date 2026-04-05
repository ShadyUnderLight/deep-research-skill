# Comparative Distillation — Weekend Seaside Destination Selection (GPT vs Minimax)

Use this file as a real paired-report comparative-distillation case focused on **multi-origin destination selection under hard weekend constraints**.

---

## Case identity

- **Case name:** Weekend seaside destination selection for four travelers from Guangzhou + Zhuhai
- **Date:** 2026-04-01
- **Research question:** Four people starting from Guangzhou Nansha, Guangzhou Baiyun, Guangzhou Liwan, and Zhuhai want a seaside city suitable for a two-day weekend trip. Identify the destination that is most transport-convenient and still worthwhile as a short seaside getaway.
- **Why this comparison matters:** This is not a standard company or investment memo. It tests whether the skill can generalize its decision-oriented discipline to a consumer travel-selection problem with multiple origins, hard time constraints, and mixed evidence types (official timetables, weather, operator info, media,攻略/UGC). It is a useful stress test for whether the skill's core research logic transfers beyond finance and company analysis.
- **Report A:** GPT deep research (user-provided PDF)
- **Report B:** Minimax deep research (user-provided PDF)
- **Reference / stronger report (if any):** GPT deep research
- **Prompt(s):** Same prompt provided by user: “我们四个人分别在广州南沙、广州白云、广州荔湾和珠海，帮我们调研一个对我们来说交通便利，适合周末两天度假的海边城市。”
- **Important scope or timing differences:** Both reports were generated from the same prompt. Exact retrieval windows and source selection likely differed. Distillation should focus on stable structural differences rather than one-off source hits.

---

## Comparison purpose

This comparison is **not** about which report feels more polished.

It is for identifying:

- what decision-support behaviors GPT shows that Minimax misses
- which gaps are really about method and structure rather than topic knowledge
- what new rules, checklist hardening, or template changes should be added so the skill handles **destination / city / option selection** tasks more rigorously

---

## Dimension 1: Current-state discipline

### Report A
- Uses current operational constraints more explicitly, including train frequency, late-return risk, ferry disruption, and current weather context
- Treats transport feasibility as a live operational question rather than a static background fact
- Avoids overly strong timeless destination-quality claims and instead emphasizes current trip-fit under the stated weekend constraint

### Report B
- Includes some current transport facts such as high-speed rail times and ferry restoration, but mixes them with broad destination-quality judgments
- Uses compressed destination labels such as "粤东最洁净之一" / "广东顶级" / "性价比最高" without sufficiently current and definition-bound support
- Current-state transport information exists, but quality judgments are less temporally disciplined

### Gap
GPT handles "current state" more as **current trip feasibility under current constraints**, while Minimax partly collapses current transport facts and semi-durable destination reputation into one layer. The stronger difference is not freshness of destination facts alone, but better separation between current operational constraints and broader experiential claims.

### Candidate action
When the task is a short-horizon destination or option selection problem, separate:
1. current operational feasibility,
2. medium-stability destination characteristics,
3. subjective experience or reputation claims.

Do not compress all three into one undifferentiated recommendation layer.

### Action type
`NEW_RULE`

---

## Dimension 2: Numerical and date discipline

### Report A
- Explicitly defines a door-to-door methodology: local transfer -> station buffer -> intercity transport -> last-mile connection
- Separates four-person average, Guangzhou-three average, and Zhuhai-origin travel time so averages do not hide the decision-relevant asymmetry
- Uses indicative time/cost ranges with methodological explanation rather than presenting a single opaque "综合最优" conclusion

### Report B
- Provides many time estimates and practical travel paths, but the aggregation logic behind "综合可达性最优" remains less visible
- Gives approximate times and conclusions, but does not clearly explain whether the comparison is based on average, max traveler burden, fairness across origins, or another rule
- Quantification exists, but the decision metric is partially implicit

### Gap
GPT is better not because it has more numbers, but because it makes the **comparison method legible**. It tells the reader how travel time was constructed and why a single average can be misleading. Minimax provides numbers, but not enough of the scoring logic behind the recommendation.

### Candidate action
For multi-origin travel, commute, meetup, or destination-selection tasks, require an explicit aggregation method:
- define door-to-door components,
- state whether the comparison uses average / max / median / fairness logic,
- explain when one subgroup should be shown separately instead of hidden inside the overall average.

### Action type
`NEW_RULE`

---

## Dimension 3: Source traceability and evidence weighting

### Report A
- Shows stronger source hierarchy awareness in prose: official transport/searchable schedule info first, operator/port info for ferry, weather authority for weather risk
- Makes the method feel more anchored to source classes even though explicit inline citations are absent
- Still does not provide claim-level citations or a structured source register

### Report B
- Provides a visible evidence legend `[CONF] / [LIKELY] / [UNCERTAIN]`
- But strong destination-quality and reputation claims remain hard to audit in the body
- Final source list mixes official schedules, news/media,攻略平台, and UGC-style sources without enough claim-level mapping or source-weight distinction

### Gap
GPT is better at **source hierarchy awareness**, while Minimax is better at **visible confidence-label scaffolding**. Neither report fully satisfies the repo's current claim-level traceability standard. The stronger pattern is to combine GPT's source-order thinking with Minimax's visible labeling system.

### Candidate action
For mixed-evidence comparison tasks (travel, consumer choice, local destination, vendor-lite comparisons), require:
1. a short source-class note at the top,
2. confidence labels or equivalent visible evidence discipline,
3. stronger claim-to-source mapping for any strong recommendation or negative reputation claim.

### Action type
`TEMPLATE_CHANGE`

---

## Dimension 4: Forward-looking claim discipline

### Report A
- Handles forward-looking uncertainty mainly through operational-risk framing: weather changes, late-return disruption, ferry stoppage, rain-plan fallback
- Does not overuse unsupported predictive wording; most uncertainty is presented as scenario risk rather than disguised certainty

### Report B
- Uses some forecast-like language and practical advice, but blends future-trip assumptions with recommendation tone more casually
- Some claims about likely crowding, user-experience risk, or destination suitability rely on compiled攻略/口碑 logic rather than clearly scoped scenario assumptions

### Gap
Neither report is full of finance-style forecasts, but GPT is better at turning uncertainty into **scenario planning** rather than bare predictive phrasing. For travel-selection tasks, the right discipline is less about analyst-style forecasts and more about explicit contingency logic.

### Candidate action
Extend forward-looking discipline for practical planning tasks: when the task is travel or itinerary selection, uncertain future conditions should be expressed as **scenario risks + fallback options**, not as flat predictive statements.

### Action type
`CHECKLIST_HARDENING`

---

## Dimension 5: Structural readability and information density

### Report A
- Starts with the evaluation frame and overall ranking before drilling into city-by-city analysis
- Uses summary comparison tables that are more decision-oriented than scenic-description-oriented
- Keeps the reader focused on how the destination choice is being made

### Report B
- Has a recognizable deep-research skeleton and clear sections
- But often drifts into destination-guide mode: scenic descriptions, restaurant avoidance tips, specific shop suggestions, and qualitative destination language start to occupy more space than the underlying comparison logic
- The report is readable, but not always maximally information-dense for the decision being made

### Gap
The core structural difference is that GPT behaves more like a **choice architecture document**, while Minimax behaves more like a **structured travel guide with recommendation output**. The reader can more quickly reconstruct the reasoning path in GPT.

### Candidate action
For destination/option-selection tasks, prioritize this report order:
1. decision frame,
2. comparison dimensions,
3. ranked shortlist,
4. city-by-city detail.

Do not let scenic detail, local tips, or consumption advice dominate before the selection logic is clear.

### Action type
`TEMPLATE_CHANGE`

---

## Dimension 6: Decision usefulness

### Report A
- Clearly frames the problem as a constrained choice under two-day time limits and unequal origin points
- Identifies the real decision-relevant burden: not just whether a place is nice, but whether four people can reach it fairly and still retain meaningful seaside time
- Introduces change-the-conclusion variables such as weather, late return, ferry risk, and rain fallback
- Makes the recommendation logic sharper: Zhuhai first, Shenzhen second, with explicit reasons tied to the stated constraints

### Report B
- Identifies important variables and gives a usable recommendation
- But the output still leans toward scenic quality and destination charm instead of fully formalizing the selection logic
- Strong recommendation exists, but the decision rule behind it is less explicit
- Some local execution tips are practical, yet they do not substitute for a clearer choice architecture

### Gap
This is the biggest difference in the pair. GPT better understands that the user is not asking "which beach is nicest?" but "which destination best satisfies a four-origin, two-day, low-friction decision problem?" Minimax partially understands this, but still answers like an upgraded攻略 report.

### Candidate action
When the task is destination/city/option selection, the report must optimize for **choice architecture**, not attraction density alone. The output should explicitly answer:
- what decision is being made,
- what the governing constraints are,
- which option wins under those constraints,
- what would change the recommendation.

### Action type
`NEW_RULE`

---

## Candidate-action summary

| # | Candidate action | Failure family | Action type | Proposed home |
|---|---|---|---|---|
| 1 | Separate operational feasibility, stable destination traits, and subjective reputation claims | current-state / time-layer discipline | NEW_RULE | `references/report-template.md` or new option-selection reference |
| 2 | Require explicit aggregation logic for multi-origin destination/transport comparisons | research depth / briefing drift | NEW_RULE | new reference for option-selection / comparison tasks |
| 3 | Combine source-class note + visible evidence labels + stronger mapping for strong travel recommendation claims | source traceability / evidence weighting | TEMPLATE_CHANGE | `references/report-template.md` + `checklists/final-audit.md` |
| 4 | Express travel uncertainty as scenario risks + fallback plans, not flat predictive statements | forward-looking claim discipline | CHECKLIST_HARDENING | `checklists/final-audit.md` or `checklists/forward-looking-claims.md` |
| 5 | For destination-selection tasks, lead with decision frame -> comparison dimensions -> shortlist -> detail | output structure / information density | TEMPLATE_CHANGE | `references/report-template.md` |
| 6 | Optimize destination-selection reports for choice architecture rather than guide-style description | decision utility | NEW_RULE | new reference for decision/selection tasks or `references/decision-report-template.md` |

---

## Triage notes

### Candidate 1
- **Why it matters:** Travel-selection tasks often mix current transport conditions, medium-stability destination features, and highly subjective reputation signals. If these are not separated, confidence calibration collapses.
- **Why it is reusable:** This applies beyond travel — local city comparison, school district choice, neighborhood comparison, venue selection, and many consumer decisions share the same evidence-mixing problem.
- **Why this home is best:** This is a structural reporting discipline best taught near the report template or in a dedicated option-selection reference.
- **Promotion status:** `PROMOTE_NOW`

### Candidate 2
- **Why it matters:** In multi-origin problems, a simple average can hide the real decision burden. The comparison method itself is load-bearing.
- **Why it is reusable:** The same issue appears in commute comparisons, meetup planning, warehouse siting, office selection, airport choice, and other multi-origin optimization questions.
- **Why this home is best:** This deserves its own reusable reference or a substantial addition to an existing decision/report template, because it is a method rule rather than only a formatting tweak.
- **Promotion status:** `PROMOTE_NOW`

### Candidate 3
- **Why it matters:** Travel and consumer-choice tasks frequently rely on mixed evidence types. Without explicit source-class handling, strong recommendation claims become too hard to audit.
- **Why it is reusable:** This is a recurring problem anywhere official operational data and subjective user-report data coexist.
- **Why this home is best:** A template-level note plus final-audit enforcement is the cleanest way to improve reader-visible evidence handling without overloading every travel report with full academic citation apparatus.
- **Promotion status:** `WAIT_FOR_SECOND_CASE`

### Candidate 4
- **Why it matters:** Planning decisions are often broken by future-condition uncertainty rather than by current factual gaps.
- **Why it is reusable:** This fits travel, events, weather-sensitive outings, and any real-world plan with fragile logistics.
- **Why this home is best:** This is fundamentally an execution/audit issue, so a checklist home is better than prose-only explanation.
- **Promotion status:** `WAIT_FOR_SECOND_CASE`

### Candidate 5
- **Why it matters:** If scenic detail arrives before selection logic, the reader gets a nice guide but a weaker decision memo.
- **Why it is reusable:** This applies to destination, city, school, venue, and product shortlist tasks.
- **Why this home is best:** The issue is primarily output design, so `report-template.md` is the best initial home.
- **Promotion status:** `PROMOTE_NOW`

### Candidate 6
- **Why it matters:** The report should help the reader choose under constraints, not merely admire well-described options.
- **Why it is reusable:** This is a general decision-utility principle for all shortlist/comparison tasks.
- **Why this home is best:** This belongs in decision-oriented reporting guidance or a dedicated selection-comparison reference, because it shapes the whole output, not just one section.
- **Promotion status:** `PROMOTE_NOW`

---

## Things explicitly rejected

| Observation | Why rejected |
|---|---|
| GPT chose Zhuhai while Minimax chose Xunliao Bay, therefore GPT is correct and Minimax is wrong | Different recommendations alone do not justify a rule; the reusable signal is in the decision method, not the winning city |
| Minimax should stop giving restaurant or local tips entirely | Too absolute; execution advice can be useful after the choice logic is established |
| GPT is simply more intelligent about travel | Too vague and not auditable |
| Travel reports should always avoid UGC | Too strong; in travel decisions UGC can be useful, but it must be clearly weighted and separated from official operational facts |

---

## Final judgment

### What the stronger report did better
GPT was stronger because it treated the task as a **multi-origin constrained decision problem**, not just a destination recommendation. It made the evaluation frame explicit, showed more method transparency around door-to-door comparison, handled operational uncertainty through scenario logic, and kept the reader closer to the actual choice architecture.

### What should change in the repo now
This case suggests the skill needs stronger support for **option-selection / destination-selection / city-selection** tasks, especially:
- explicit comparison methodology for multi-origin problems
- stronger separation of operational facts vs destination traits vs subjective reputation
- template order that keeps shortlist logic ahead of guide detail
- more explicit choice-architecture discipline for consumer and planning decisions

### What should wait for another confirming case
The exact level of source-traceability needed for travel/consumer-comparison tasks should wait for another case before being hardened too aggressively. Full claim-level citation may be too heavy for some travel outputs, but stronger source-class transparency clearly matters.

### Is this mainly a missing rule, missing trigger, or execution problem?
This case is mainly a **missing-rule** case. The current repo is strong on company/investment-style research discipline but less explicit about how to do **selection problems with multiple origins, practical constraints, and mixed evidence types**. GPT's advantage here is largely methodological, not just executional.

---

## Post-case validation note

After creating the new selection-task artifacts, both reports were re-checked against the new option-selection gate:

- `references/option-selection-and-shortlist-discipline.md`
- `references/decision-report-template.md` (selection-aware adaptation)
- `checklists/option-selection-final-audit.md`

### What the new gate catches well

The new gate correctly captures the most important structural difference between the pair:

- **GPT behaves like a constrained-choice memo**
- **Minimax behaves more like a structured guide/recommendation report**

In particular, the new checklist proved useful for distinguishing:

1. **Aggregation visibility**
   - GPT explicitly exposed door-to-door methodology and subgroup handling
   - Minimax gave many travel-time estimates but left the final aggregation logic too implicit

2. **Choice architecture vs guide drift**
   - GPT kept shortlist logic ahead of long detail
   - Minimax more often drifted into scenic detail, restaurant avoidance, and local tips before fully locking the selection logic

3. **Evidence-layer separation**
   - GPT showed stronger source-hierarchy awareness in prose
   - Minimax had visible labels but still mixed operational facts, reputation signals, and synthesized recommendation too freely

4. **Scenario logic tied to ranking**
   - GPT was stronger at expressing risk as scenario/fallback logic
   - Minimax had risk notes, but they were less tightly connected to when the ranking should change

### What still remains imperfect

The new gate does **not** solve the broader source-traceability gap by itself. Both reports still remained weaker than the repo's ideal standard for claim-level auditability. This means the new selection checklist is useful, but it complements rather than replaces the broader traceability discipline.

### Validation result

This case provides an initial real-world validation that the new selection-task discipline is not abstract documentation: it successfully distinguishes a true constrained-choice report from a more catalog/guide-like report.

This is a positive signal that the new reference + template + checklist stack is worth keeping and testing on more non-finance selection tasks.

---

## Minimal quality bar

- [x] the two reports are comparable enough to justify distillation
- [x] the comparison used the six fixed dimensions
- [x] each accepted candidate has an action type
- [x] each accepted candidate has a proposed repo home
- [x] at least one rejected observation is documented when relevant
- [x] the final judgment distinguishes rule gap vs trigger gap vs execution gap
