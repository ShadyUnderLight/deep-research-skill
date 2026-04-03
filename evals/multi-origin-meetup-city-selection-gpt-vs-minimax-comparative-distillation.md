# Multi-Origin Meetup City Selection — GPT vs MiniMax Comparative Distillation

## Case identity

- **Task type:** location-selection / multi-origin meetup-city choice / constrained-choice memo
- **User objective:** 为分别位于上海、深圳、香港的三人团队选择一个适合周末线下见面的城市，并显式说明 comparison unit、aggregation logic、shortlist、最终推荐、落选原因与排序逆转条件
- **Compared outputs:** GPT report vs MiniMax report on the same topic
- **Research date context:** 2026-04-03
- **Distillation goal:** 提炼这类 multi-origin selection memo 的稳定结构差异，并归因为 `NEW_RULE` / `CHECKLIST_HARDENING` / `TEMPLATE_CHANGE` / `NO_ACTION`

---

## Prompt shape

This was not a travel-guide prompt.

It was a **multi-origin, fairness-sensitive, budget-constrained location-selection memo** with these properties:

- constrained-choice
- shortlist-first
- aggregation-visible
- fairness-sensitive
- partially quantitative
- practical-planning oriented
- evidence-layer sensitive

That means the output should optimize for:

- explicit comparison unit
- visible aggregation logic
- shortlist construction and elimination logic
- fairness vs efficiency trade-off handling
- runner-up credibility
- ranking-reversal conditions
- clear separation of confirmed facts, inference, and open uncertainty

It should **not** drift into a destination recommendation article or a city-profile comparison with a recommendation attached later.

---

## Compared outputs at a glance

### GPT output
More clearly behaved like an actual **constrained-choice location-selection memo**.

Visible strengths:

- explicitly framed the task as location-selection under constraints
- defined a calculable comparison unit (`GC`) rather than only naming time/cost as factors
- made aggregation logic visible with explicit weights
- built a more transparent shortlist with entry reasons and pre-labeled risk points
- treated runner-up credibility and ranking-reversal conditions more like real decision logic
- separated many evidence roles more explicitly (`confirmed facts` / `inference` / `open uncertainty`)

Visible weaknesses:

- relied heavily on proxies and modeling choices (VOT, metro-length mapping, attraction-score mapping), which can create professional-looking overprecision if not tightly labeled
- some "confirmed" vs "derived" layers could still be separated more cleanly
- the winning recommendation depended materially on modeling assumptions, so sensitivity discipline remained load-bearing

### MiniMax output
The weaker output in this pair.

Visible strengths:

- recognized the task as option-selection rather than pure destination description
- named a comparison unit and a fairness-first aggregation idea
- produced a shortlist and a final ranking
- used at least some transportation sourcing and practical constraints rather than pure travel-writing language

Visible weaknesses:

- comparison unit was only partially operationalized; "experience" remained influential but not clearly modeled
- aggregation logic was declared but not fully made visible, especially around cost role, fairness measurement, and cross-border friction handling
- shortlist construction and elimination logic were too opaque
- claim-level separation of confirmed facts, inference, and uncertainty was weak in the body
- ranking-reversal conditions were underdeveloped; uncertainty appeared more as caveats than as decision-change logic
- the report remained closer to a recommendation-flavored destination memo than a fully auditable choice memo

---

## Six-dimension comparison

### 1. Current-state discipline

**Winner: GPT (slightly)**

This case was less about fast-moving product state and more about current travel-execution facts. GPT did the stronger job of anchoring the memo in a dated data snapshot and clearly labeling what came from platform data versus what was a modeling assumption.

MiniMax did use current schedules and prices, but the current data did not organize the whole decision model as clearly.

**Distilled conclusion:**  
For practical location-selection tasks, current operational facts should anchor the decision frame, but they are only one layer; what matters more is whether those facts are visibly transformed into an auditable choice model.

**Candidate action:** `NO_ACTION`

---

### 2. Numerical and date discipline

**Winner: GPT**

GPT more clearly distinguished:

- observed transport times/prices
- proxy variables
- assumptions like VOT and local-transport budget
- derived model outputs like GC and composite ranking

MiniMax used numbers, but the report still read more like quantified support for a recommendation than a visible model with role-labeled inputs.

**Distilled conclusion:**  
For location-selection / meetup-city memos, numbers should be visibly role-labeled as observed facts, proxies, assumptions, or aggregation outputs. Otherwise reports can look rigorous while hiding modeling choices.

**Candidate action:** `CHECKLIST_HARDENING`

---

### 3. Source traceability and evidence weighting

**Winner: GPT**

GPT was stronger at distinguishing which inputs were direct platform facts and which were synthesized proxies. It also surfaced some uncertainty around Hong Kong pricing/reference conflicts.

MiniMax cited transport sources, but several high-impact claims such as city practicality, experience quality, and "cost-performance" read as if they had the same evidentiary status as the timetable data.

**Distilled conclusion:**  
In selection memos, claim-level evidence separation matters as much as source presence. Schedules, prices, hotel averages, city-function proxies, and final synthesis should not visually collapse into one evidence layer.

**Candidate action:** `CHECKLIST_HARDENING`

---

### 4. Forward-looking claim discipline

**Winner: GPT**

GPT more clearly converted uncertainty into ranking-change logic: when higher time value, stricter budget, or different preference weights would cause Changsha or another city to move.

MiniMax acknowledged uncertainty, but mostly as background caveats or travel variability notes rather than explicit ranking-reversal conditions.

**Distilled conclusion:**  
For shortlist / location-selection work, uncertainty should usually be expressed as change-the-ranking conditions rather than generic caveats.

**Candidate action:** `TEMPLATE_CHANGE`

---

### 5. Structural readability and information density

**Winner: GPT**

GPT more clearly separated:

- decision model
- shortlist generation
- quantified comparison table
- why first place wins
- why second place still works
- why others lose

MiniMax had the right headings but weaker execution: the structure looked like a decision memo, yet the logic inside remained less auditable.

**Distilled conclusion:**  
For constrained-choice city-selection tasks, the report should visibly show shortlist-construction logic and loser-specific failure modes, not just final rank ordering.

**Candidate action:** `TEMPLATE_CHANGE`

---

### 6. Decision usefulness

**Winner: GPT**

This was the largest gap.

GPT more clearly answered:

- what the real decision was
- what unit the comparison used
- how fairness entered the decision
- why the top option won
- why the runner-up remained credible
- what assumptions would reverse the ranking

MiniMax produced a ranking but left more of the actual choice architecture implicit.

**Distilled conclusion:**  
The central gap here is not lack of city knowledge. It is weaker **aggregation visibility + shortlist discipline + ranking-reversal logic**.

**Candidate action:** `CHECKLIST_HARDENING` + `TEMPLATE_CHANGE`

---

## Core distilled findings

### Finding 1
For multi-origin meetup/location-selection tasks, the report should explicitly define not just a comparison unit but also the role of each numerical layer:

- observed fact
- proxy
- assumption
- model output

Otherwise the memo can create **professional-looking model drift**.

**Action type:** `CHECKLIST_HARDENING`

---

### Finding 2
When fairness matters, aggregation visibility must go beyond "fairness-first" prose. The memo should show whether fairness is being measured by:

- worst-off participant
- burden dispersion / variance
- average burden
- robustness under disruption
- cross-border or operational friction penalties

**Action type:** `CHECKLIST_HARDENING`

---

### Finding 3
Shortlist logic should be visibly constructed rather than implied. A strong report should show:

- why each shortlisted option was included
- why near-candidates were excluded
- which failure mode caused each loser to drop

**Action type:** `TEMPLATE_CHANGE`

---

### Finding 4
For practical selection tasks, uncertainty should be written as ranking-reversal logic, not just as travel caveats or generic volatility.

Examples:

- higher time value -> time-fair city rises
- tighter budget ceiling -> lower-cost city rises
- greater weight on destination experience -> experience-led city rises
- stronger aversion to cross-border friction -> different shortlist survives

**Action type:** `TEMPLATE_CHANGE`

---

### Finding 5
The report should make runner-up credibility explicit, not just list a second place. The reader should see under what alternative weighting or scenario the runner-up becomes first.

**Action type:** `TEMPLATE_CHANGE`

---

### Finding 6
The most important failure mode in the weaker report is not "missing recommendation" but **execution drift**: it knows the memo shape, yet does not fully execute comparison-unit visibility, aggregation transparency, and ranking-change logic.

**Action type:** `NO_ACTION`

---

## Candidate-action summary

| # | Candidate action | Failure family | Action type | Proposed home |
|---|---|---|---|---|
| 1 | Require role-labeling of key quantitative inputs in constrained-choice memos: observed fact vs proxy vs assumption vs model output | numerical discipline / professional-looking model drift | CHECKLIST_HARDENING | `checklists/option-selection-final-audit.md` + `checklists/final-audit.md` |
| 2 | Strengthen fairness/aggregation gate to require visibility on worst-off participant, dispersion, and hidden subgroup penalties when relevant | aggregation visibility / average-value trap | CHECKLIST_HARDENING | `checklists/option-selection-final-audit.md` |
| 3 | Strengthen option-selection structure to show shortlist-construction logic and loser-specific failure modes | shortlist discipline / decision utility | TEMPLATE_CHANGE | `references/decision-report-template.md` |
| 4 | Strengthen option-selection structure so uncertainty is expressed as ranking-reversal conditions | scenario logic / change conditions | TEMPLATE_CHANGE | `references/decision-report-template.md` |
| 5 | Add a practical-planning heuristic for multi-origin meetup/location choice: cross-border / transfer / operational friction can be a separate burden layer, not just folded into ticket price | constrained-choice methodology / hidden friction | NEW_RULE | `references/option-selection-and-shortlist-discipline.md` |

---

## Triage notes

### Candidate 1
- **Why it matters:** selection reports can sound quantitative while hiding which numbers are observed and which are modeling choices
- **Why it is reusable:** applies to destination choice, office choice, venue choice, vendor choice, and provider selection whenever composite scoring appears
- **Why this home is best:** this is mainly a delivery-time audit problem rather than a routing problem
- **Promotion status:** `PROMOTE_NOW`

### Candidate 2
- **Why it matters:** saying "fairness matters" is not enough if the memo hides who is worst served or how uneven the burden spread is
- **Why it is reusable:** applies to any multi-user, multi-origin, or subgroup-sensitive choice task
- **Why this home is best:** this belongs in the constrained-choice audit gate
- **Promotion status:** `PROMOTE_NOW`

### Candidate 3
- **Why it matters:** many weak shortlist memos reveal only the final ranking and not the narrowing logic
- **Why it is reusable:** applies broadly across option-selection work, not only city choice
- **Why this home is best:** the gap is structural memo architecture
- **Promotion status:** `PROMOTE_NOW`

### Candidate 4
- **Why it matters:** uncertainty becomes decision-useful only when tied to ranking reversals or fallback conditions
- **Why it is reusable:** this is a general shortlist/reporting pattern for constrained-choice tasks
- **Why this home is best:** the fix belongs in memo structure guidance
- **Promotion status:** `PROMOTE_NOW`

### Candidate 5
- **Why it matters:** transfer burden, border friction, and operational hassle are often load-bearing but easy to hide in one blended time/cost number
- **Why it is reusable:** applies to cross-border meetings, airport/hub choice, region comparisons, and other practical planning tasks
- **Why this home is best:** this is a methodology rule inside option-selection discipline
- **Promotion status:** `PROMOTE_NOW`

---

## Things explicitly rejected

| Observation | Why rejected |
|---|---|
| South-China cities should always dominate cross-border meetup choices | too case-specific |
| GPT should always use a generalized-cost formula | too implementation-specific; explicit comparison unit matters more than one exact formula |
| MiniMax just needs more sources | too shallow; the larger problem is choice architecture execution |

---

## Final judgment

The stronger report won mainly because it behaved more like an **auditable choice memo** and less like a quantified destination recommendation.

The main lesson is not that one model knew more travel facts. It is that a stronger location-selection report should visibly show:

- comparison-unit design
- quantitative-role labeling
- fairness / aggregation logic
- shortlist-construction logic
- why first wins
- why second still works
- what reverses the ranking

This case is best understood mainly as an **execution problem** inside a rule area the repo already partly knows:

- the repo already had option-selection routing
- but the new case shows the delivery-time gates and template wording should push harder on aggregation visibility, role-labeled quantitative inputs, shortlist logic, and ranking-reversal conditions
