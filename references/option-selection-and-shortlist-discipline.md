# Option Selection and Shortlist Discipline

Use this file when the user is not primarily asking for background knowledge, but for help choosing between options under real constraints.

Typical tasks:

- destination or city selection
- vendor shortlist
- tool or platform choice
- office, warehouse, or venue selection
- meetup-point or route selection
- school, neighborhood, or region comparison
- buy / build / partner style option comparison
- any task where several plausible options must be narrowed into a ranked shortlist

This file is intentionally general. Do not treat it as travel-only guidance.

---

## Core rule

An option-selection report is not a catalog.

It should help the reader answer:

- What decision is actually being made?
- What constraints matter most?
- Which 2-5 variables truly drive the choice?
- Which option is best under those constraints?
- What would change the recommendation?

Do not produce a long tour of options and hope the conclusion emerges on its own.

---

## Step 1: Clarify the decision architecture

Before comparing options, identify:

- the actual choice being made
- the user's hard constraints
- the user's soft preferences
- whether the task is about best overall option, best-fit option, or robust fallback option
- whether fairness across stakeholders matters

Examples:

- "Which seaside city should four people pick for a weekend trip?" is not a beach-ranking task. It is a **multi-origin, time-constrained destination selection** task.
- "Which vendor should we choose?" is not a feature tour. It is a **requirements, trade-offs, and risk** task.
- "Where should we place the office?" is not just a rent comparison. It is a **multi-origin commute fairness + business constraint** task.

If the decision architecture is unclear, the rest of the report will drift into background or guide-like description.

---

## Step 2: Identify load-bearing variables

List the 2-5 variables that actually determine the decision.

These are not all facts about the options. They are the few variables that most change the final recommendation.

Examples:

- total door-to-door time
- cost range
- integration difficulty
- reliability / uptime risk
- local transport after arrival
- stakeholder fairness
- weather or regulatory fragility
- fallback quality if the main plan breaks

Do not give equal weight to every variable just because it is easy to describe.

---

## Step 3: Choose the comparison unit explicitly

Before comparing options, define what unit of comparison the task really needs.

Examples:

- venue selection -> total access burden, not only rent
- vendor selection -> implementation + lock-in cost, not only sticker price
- destination selection -> door-to-door usable leisure time, not only distance on a map
- office selection -> median commute and worst-case commute, not only average commute

If the wrong unit is chosen, the report may look quantitative but still mislead.

---

## Step 4: Make the aggregation logic visible

When multiple people, regions, teams, or user groups are involved, do not hide the comparison logic inside one opaque average.

State explicitly whether the judgment is based on:

- average burden
- median burden
- max burden / worst-off participant
- weighted priority user
- fairness across participants
- robustness under disruption

Use subgroup views when needed.

Examples:

- show overall average and also the outlier subgroup
- separate "three users are well served, one is heavily penalized" from "all users are reasonably served"
- explain whether the recommendation optimizes for efficiency or fairness

A simple average is often not enough for real selection problems.

---

## Step 5: Separate evidence layers

In option-selection tasks, different claim types often get mixed together. Separate them.

At minimum, distinguish:

1. **Operational facts**
   - schedules, pricing, capacity, location, formal policy, documented compatibility
2. **Medium-stability attributes**
   - neighborhood character, product maturity, hotel supply, service breadth, platform ecosystem
3. **Subjective or reputation-based signals**
   - user complaints, local reputation, community sentiment,攻略/UGC patterns
4. **Model synthesis / recommendation**
   - the report's integrated judgment

Do not let subjective reputation claims silently inherit the confidence of official operational facts.

---

## Step 6: Build the shortlist before the deep dive

For selection tasks, the report should usually move in this order:

1. decision frame
2. what matters most
3. shortlist or ranked options
4. why the top option wins
5. why the runner-up remains credible
6. why other options lose
7. detailed profiles only after the shortlist logic is clear

Do not spend most of the report describing each option equally if the user needs a choice.

A shortlist report should feel like a narrowing process, not an encyclopedia.

---

## Step 7: Handle uncertainty as scenario logic

For practical planning tasks, uncertainty is often about what could go wrong in execution.

Prefer:

- scenario risks
- fallback paths
- fragility points
- change-the-conclusion variables

Examples:

- if weather disrupts ferries, fallback to rail-access option
- if one stakeholder's commute weight becomes dominant, recommendation changes
- if peak-season congestion matters more than average access time, ranking changes
- if the budget ceiling tightens, the second-best option may become first

Do not express these only as vague warnings. Tie them to the recommendation.

---

## Step 8: Distinguish best overall, best fit, and best fallback

These are not the same.

When useful, explicitly separate:

- **Best overall** — strongest option under the stated objective
- **Best fit for a specific preference** — e.g. quieter, cheaper, lower-risk, more premium
- **Best fallback** — next best option when a key assumption breaks

This often improves the usefulness of the report more than adding extra background detail.

---

## Good output pattern

A strong selection report often includes:

### Executive summary
- top recommendation
- runner-up
- key reason each stands where it does
- biggest caveat

### What matters most
- the 2-5 variables driving the choice

### Ranked shortlist
- option 1
- option 2
- option 3
- optional eliminate/do-not-recommend row

### Comparison table
Include only columns that matter to the decision.

Good columns may include:
- primary comparison unit
- cost
- risk / fragility
- local convenience after arrival
- fallback quality
- why it wins / loses

### Change-the-conclusion section
- what assumption changes would alter the ranking

### Sources
- especially for operational facts and hard constraints

---

## Common failure modes

### Failure mode 1: Catalog drift
The report describes all options at length but never sharpens into a real choice.

**Fix:** force a shortlist early.

### Failure mode 2: Opaque scoring
The report says one option is best, but the comparison method is hidden.

**Fix:** state the unit of comparison and aggregation logic.

### Failure mode 3: Average-value trap
Averages hide one badly served stakeholder or one fragile segment.

**Fix:** show subgroup or worst-case burden explicitly.

### Failure mode 4: Mixed evidence collapse
Official facts, reputation, and inference are blended together.

**Fix:** separate evidence layers and confidence levels.

### Failure mode 5: Guide-mode takeover
Detailed tips, local highlights, or surface features crowd out the selection logic.

**Fix:** move detail below the shortlist and keep it subordinate to the choice.

### Failure mode 6: Weak change conditions
The report gives a recommendation but does not say what would overturn it.

**Fix:** add scenario triggers and fallback options.

---

## Practical heuristics

When the task involves multiple origins or stakeholders, ask:

- Who is worst served by this option?
- Is that penalty acceptable?
- Is fairness more important than absolute efficiency?
- Would a different option win if one origin/user had double weight?
- Is there a hidden burden layer beyond headline time/cost, such as cross-border friction, transfers, visa or checkpoint burden, schedule fragility, or awkward first/last-mile logistics?
- Should that hidden burden be modeled as a separate penalty or risk factor instead of being silently folded into one blended average?

When the task involves practical planning, ask:

- What is the single most fragile step in the plan?
- What is the fallback if that step fails?
- Does the recommendation still hold under common disruption scenarios?

When the task involves destination or city choice, ask:

- Are we optimizing for travel burden, usable time after arrival, activity density, budget, or experience purity?
- Which of these actually matters most for this user?

When the task involves tool/vendor/platform choice, ask:

- Are we optimizing for deployment speed, feature depth, reliability, TCO, lock-in, or team fit?
- Which one dominates under the user's real constraint set?

When the task involves model/API provider selection, also ask:

- What is the current primary model/API family for each provider right now, not one generation ago?
- Which facts are current-state load-bearing variables rather than background detail?
- Do support regions, mainland accessibility, payment/signing reality, data residency, and SLA change the shortlist itself?
- Is the report comparing providers using a current snapshot, or using stale flagship anchors?
- Is the output becoming a vendor encyclopedia instead of a ranked provider-choice memo?

When the task involves market entry / regional expansion / country prioritization, also ask:

- Is the real choice whether to enter now, delay, pilot, or sequence entry over phases?
- What is the realistic alternative to this market or region, and is the report comparing against it explicitly?
- Are regional hub, first revenue beachhead, and later expansion market being confused into one vague "priority market" label?
- Is one visible comparison unit being used across candidate countries, or has the report drifted into free-form country notes?
- Which hard gates would actually block entry: budget, data/deployment architecture, compliance readiness, channel readiness, language / localization readiness, or something else?
- Does the report show why the top entry sequence wins and what would reverse that sequence?

---

## Output discipline

A good option-selection report should let the reader quickly answer:

- What is the top recommendation?
- Why does it win?
- Who or what is penalized by that choice?
- What is the best alternative?
- What would change the recommendation?

If the report cannot answer these cleanly, it is probably still doing description, not decision support.

---

## Best home for related fixes

When a new selection-case failure appears:

- use `references/failure-taxonomy.md` to classify the failure family
- use `evals/decision-utility-rubric.md` if the report feels informative but not decisional
- use `evals/rule-activation-and-execution-discipline.md` if the report knows the structure but fails to execute it
- use `references/report-template.md` for presentation/layout fixes
- use this file for the core logic of comparison, shortlist construction, and selection methodology

---

## Bottom line

Selection work is a special kind of research.

The job is not to describe options well.
The job is to help the user choose well.
