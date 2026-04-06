# Home-server equipment recommendation comparative distillation

## Case
Prompt topic: deep research report for “building a home server for an ordinary household”  
Required artifact: decision-ready research report with PDF delivery  
Core user need: realistic, budget-clear, long-run-usable equipment and system recommendation

---

## Triage notes

### Triage outcome
KEEP and DISTILL

This case should not be discarded as a shallow one-off miss. It is useful because:
- the task entrance was broadly recognized
- the report achieved visible structural coverage
- the main weaknesses are stable and reusable
- the failure is not “missing one fact” but “wrong artifact shape under the right topic”

### Why this case matters
This is a strong test case for a common failure pattern in technical consumer planning tasks:

- the report looks comprehensive
- many expected sections are present
- recommendation language appears
- but the artifact still fails to become decision-grade

That makes this case valuable for route hardening, template hardening, and audit hardening.

---

## Task classification

This task should not be treated as generic technical research or broad consumer hardware explanation.

### Primary route
- equipment selection / procurement-style decision memo

### Secondary disciplines
- constrained-choice / route ranking
- hardware-software stack fit
- current-market-sensitive technical planning
- household operating cost analysis
- final-delivery rendering integrity

### Visible artifact contract
A strong final artifact should:
- recommend a route, not just explain routes
- rank alternatives under visible constraints
- make budget assumptions explicit
- tie hardware route to software/system fit
- surface long-run household operating tradeoffs
- remain readable as a final PDF when PDF is requested

---

## What MiniMax got right

### 1. Broad task-shape recognition was acceptable
The report recognized the expected top-level sections:
- household use cases
- device-route comparison
- budget bands
- demand-based recommendations
- component analysis
- software/system matching
- pitfalls

This means the task was not misread at the outer structural level.

### 2. Several directional judgments were reasonable
Useful judgments included:
- home servers are not a “peak performance wins” problem
- low power, low noise, stability, and maintainability matter heavily in household use
- beginners often overweight CPU/RAM and underweight drive bays, networking, media capability, and maintenance reality

### 3. It produced a usable orientation artifact
As a first-pass orientation note, the report can still help a user narrow choices.  
Its failure is not “uselessness.” Its failure is “insufficient decision compression.”

---

## Core diagnosis

The report is structurally broad but decision-soft.

It reads more like:
- a structured hardware overview with recommendation drift

than:
- a procurement-grade home server decision memo

The main problem is not missing sections.  
The main problem is failure to compress route comparison, budgets, stack fit, and household operating tradeoffs into a purchase-ready recommendation structure.

---

## Failure families

### 1. Procurement-overview drift
The task should have been executed as a procurement memo, but the report remained closer to a broad route overview.

Signals:
- multiple routes are described
- budget bands are present
- recommendation language appears
- but the artifact still behaves like a guided comparison rather than a ranked buying decision

### 2. Decision compression failure
The report gathers categories but does not compress them into a small set of clear, executable decisions.

Weak or missing:
- top recommendation
- credible runner-up
- rejected routes and why
- dominant constraint behind the ranking
- conditions that would change the recommendation

This produces a report that feels complete while remaining weak as a decision artifact.

### 3. Budget closure failure
The budget sections do not form a real procurement-ready cost structure.

Typical unresolved assumptions include:
- whether hard drives are included
- whether UPS is included
- whether networking upgrades are included
- system disk vs data disk layout
- minimum viable configuration vs recommended configuration
- upfront capex vs recurring power / maintenance / expansion cost

A report can contain budget bands and still fail to become budget-clear.

### 4. Hardware-system fit underbinding
The report covers both hardware and software, but their relationship is not load-bearing enough.

Weak or missing:
- why a given OS or stack fits a given hardware route
- where mismatch risks appear
- which combinations are beginner-unfriendly
- which advanced combinations are intentionally more complex
- why data-first and service-first households often imply different stack choices

This leaves “system choice” as a coverage section instead of a decision driver.

### 5. Household-ops cost underweighting
The report discusses performance and route categories more strongly than long-run household operating friction.

Underweighted dimensions include:
- 24/7 idle and real-world power use
- annual electricity implications
- noise in domestic environments
- maintenance burden
- drive expansion friction
- backup overhead
- failure/replacement risk in used hardware
- whether low upfront cost creates higher long-run annoyance

For home-server planning, these are not side notes. They are ranking variables.

### 6. Number-role ambiguity
Several quantified or semi-quantified claims appear in a way that blurs:
- confirmed fact
- typical estimate
- planning assumption
- heuristic
- recommendation judgment

Claims in this task type that often need explicit role labeling include:
- budget coverage claims
- power-use claims
- value-for-money claims
- stability claims
- long-run suitability claims

Without role labeling, practical heuristics are too easily read as hard facts.

### 7. Final-artifact rendering failure
The PDF showed visibly broken Chinese text spacing and degraded readability.

Because the user explicitly requested a PDF, this should not be treated as a cosmetic flaw.  
It is a final-delivery quality failure.

---

## Candidate actions

### NEW_RULE
When the user asks what hardware, device, or system to buy or build under budget and real-world constraints, route the task as a procurement-style decision memo rather than generic technical research.

### CHECKLIST_HARDENING
Require recommendation compression:
- top recommendation
- runner-up
- rejected route(s)
- dominant constraint
- ranking-change conditions

### CHECKLIST_HARDENING
Require budget closure:
- budget includes/excludes drives
- UPS included/excluded
- networking assumptions explicit
- system disk vs data disk specified
- minimum viable vs recommended config separated
- upfront vs recurring cost separated

### CHECKLIST_HARDENING
Require hardware-system fit reasoning:
- why the stack fits the route
- mismatch risks
- beginner-unfriendly combinations
- advanced tradeoffs made explicit

### CHECKLIST_HARDENING
Require household-ops cost visibility:
- 24/7 suitability
- noise
- power cost
- maintenance burden
- expansion friction
- backup overhead

### DELIVERY_HARD_FAIL
If PDF is requested and the delivered PDF has broken typography, unreadable spacing, malformed tables, or visible export artifacts, treat it as a final-artifact delivery failure.

---

## Proposed patch targets

### 1. ROUTING-MATRIX.md
Add or harden a route/sub-route for:
- equipment selection
- hardware/software stack recommendation
- budgeted configuration memo
- home server / homelab planning

This route should specify:
- trigger
- required secondary disciplines
- visible artifact contract
- hard-fail conditions
- required audits

### 2. references/decision-report-template.md
Add a procurement-specific structure including:
- decision context and dominant constraints
- top recommendation
- runner-up and why not top
- rejected routes and why
- minimum viable configuration
- recommended configuration
- storage/network/UPS assumptions
- long-run cost notes
- upgrade path
- who should not choose the recommendation

### 3. checklists/final-audit.md or route-specific audit
Add gates for:
- recommendation compression
- budget closure
- hardware-system fit binding
- final PDF readability

### 4. New reference candidate
Possible new file:
- `references/equipment-selection-and-procurement-discipline.md`

Possible contents:
- procurement memo vs overview
- how to expose budget assumptions
- household ops friction as a ranking dimension
- hardware↔system fit requirements
- common beginner misreads in home-server planning

---

## Rejected observations

These are not the main reusable lessons:
- whether one specific NAS brand was named
- whether one exact CPU tier was best
- whether one budget boundary should shift by a few hundred yuan
- whether one vendor/model omission occurred

Those are case-level details.  
The reusable lessons are about:
- routing
- artifact shape
- budget closure
- stack fit
- operating-cost weighting
- delivery integrity

---

## Strongest reusable insight

Equipment-selection and homelab-planning tasks can appear comprehensive while still failing to become decision-grade artifacts.

The stable failure pattern is:
- coverage-rich
- recommendation-present
- procurement-weak

The quality bar is not whether the report mentions all expected categories.  
The quality bar is whether it turns route comparison, budgets, stack fit, and household operating tradeoffs into a purchase-ready memo.

---

## Proposed bottom line

This case should be kept and distilled.

It shows that home-server planning tasks need explicit routing to a procurement-style decision memo. Without that route hardening, a model can produce a report that looks comprehensive while remaining weak where it matters most: ranked recommendation, budget closure, hardware-system fit, household operating realism, and final delivery quality.

---

## Post-case validation notes

### What this case confirms
This case reinforces a broader pattern already seen in other comparisons:
- the model may preserve broad structural coverage
- but still fail to produce the right decision artifact
- recommendation language alone is not evidence of decision-grade execution

### What is newly clarified
This case sharpens a task family that deserves clearer handling:
- hardware recommendation
- device procurement
- stack planning for always-on household systems

These tasks should not default to general technical explanation, because the real user need is closer to:
- constrained-choice
- procurement memo
- operating tradeoff memo

### Why it is worth repo-level treatment
The failure is stable enough to justify repo-level hardening because it sits at:
- route selection
- template structure
- checklist enforcement
- final-delivery gate

It is not merely a one-off content miss.
