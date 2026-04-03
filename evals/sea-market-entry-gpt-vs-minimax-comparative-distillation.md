# SEA Market Entry — GPT vs MiniMax Comparative Distillation

## Case identity

- **Task type:** market entry / regional expansion / go-no-go memo / constrained-choice task
- **User objective:** 判断一家中国 AI SaaS 创业公司是否应优先进入东南亚市场，并明确优先级、进入顺序、进入方式与关键门槛
- **Compared outputs:** GPT report vs MiniMax report on the same topic
- **Research date context:** 2026-04-03
- **Distillation goal:** 提炼可复用、可审计、可执行的结构性差异，并将其归因为 `NEW_RULE` / `CHECKLIST_HARDENING` / `TEMPLATE_CHANGE` / `NO_ACTION`

---

## Prompt shape

This was not a generic Southeast Asia market overview.

It was effectively a **market-entry memo for a resource-constrained Chinese AI SaaS startup** with all of these properties at once:

- constrained-choice
- go/no-go / prioritization
- regional-expansion sequencing
- current-state-sensitive
- compliance-sensitive
- partially quantitative
- action-oriented

That means the output should optimize for:

- decision architecture
- priority relative to alternatives
- country shortlist logic
- hard gates
- sequencing and entry mode
- explicit uncertainty about what would change the recommendation

It should **not** drift into a region overview with a recommendation attached afterward.

---

## Compared outputs at a glance

### GPT output
More clearly behaved like an actual **market-entry decision memo**.

Visible strengths:

- recommendation as an operating path rather than a stance
- explicit phased entry and country sequencing
- hard gates (budget / deployment architecture)
- more visible country-shortlist structure
- KPI / milestone / scenario framing
- stronger sense of priority under resource constraints

Visible weaknesses:

- some evidence / citation artifacts leaked into the final delivery (`entity...` style residue)
- some models and estimates looked more precise than the evidence base warranted unless carefully labeled
- stronger Singapore-first logic may still partially reflect regional-HQ default bias unless tied more clearly to beachhead economics

### MiniMax output
The weaker output in this pair.

Visible strengths:

- recognized that the question was not just whether SEA is interesting, but under what conditions and with what entry logic
- identified real constraints such as localization, regulation, payment systems, and competitive timing
- offered a cautious and plausible high-level judgment rather than naive expansion enthusiasm

Visible weaknesses:

- drifted back toward a structured market overview with recommendation flavor rather than a tightly constrained choice memo
- country analysis was useful but less visibly driven by one comparison unit
- hard gates were present conceptually but not converted into operational go/no-go thresholds
- recommendation was less clearly written as sequencing, operating path, and decision logic

---

## Six-dimension comparison

### 1. Current-state discipline

**Winner: GPT**

GPT more clearly treated current conditions as the base state for a decision: current demand proxies, current infrastructure investment, current regulation posture, and current product/deployment implications all visibly fed the recommendation.

MiniMax included many current facts, but they did not as clearly form the memo skeleton. The output remained closer to a region scan with current facts mixed in.

**Distilled conclusion:**  
For market-entry tasks, current-state discipline must not stop at a few recent facts. It has to anchor the recommendation and the sequencing logic.

**Candidate action:** `CHECKLIST_HARDENING`

---

### 2. Numerical and date discipline

**Winner: GPT**

GPT used TAM / SAM / SOM, scenario framing, quarterly split, CAC / payback / ARR targets, and budget thresholds to make the recommendation operational.

MiniMax used numbers more as support material than as the load-bearing spine of the memo.

This case also reveals a caution: GPT-style planning models can look highly rigorous while still relying on proxies and assumptions. The right lesson is not “use more numbers”; it is “label the role of each number.”

**Distilled conclusion:**  
Market-entry memos need visible labeling for observed metrics, proxies, assumptions, and planning-model outputs.

**Candidate action:** `NEW_RULE`

---

### 3. Source traceability and evidence weighting

**Winner: GPT (but with a new failure)**

GPT more clearly suggested distinct evidence layers: institutional market data, regulatory constraints, adoption surveys, and planning assumptions. But the final delivery leaked citation artifacts, which is a separate hard failure.

MiniMax had the more basic weakness: major claims and numeric ranges often read as if they were equally grounded, even when they were likely a mixture of sourced facts, heuristics, and synthesis.

**Distilled conclusion:**  
For market-entry memos, evidence layering needs to be more visible in-body; and any citation/retrieval artifact leakage should count as a final-delivery failure.

**Candidate action:** `CHECKLIST_HARDENING`

---

### 4. Forward-looking claim discipline

**Winner: GPT**

GPT more clearly answered the actual action question over the next 12 months: what to do first, what to delay, what gates matter, and what targets would count as success.

MiniMax did include a recommendation, but it was less visibly tied to phased execution, milestone logic, or ranking-reversal conditions.

**Distilled conclusion:**  
For market-entry / regional-expansion tasks, the future-facing logic should be written as phased sequencing + gates + change conditions, not only as a cautious recommendation paragraph.

**Candidate action:** `TEMPLATE_CHANGE`

---

### 5. Structural readability and information density

**Winner: GPT**

GPT more clearly grouped the memo into high-utility blocks: recommendation, country order, market sizing, customer profile, competition, compliance, GTM path, milestones, and financial scenarios.

MiniMax was structurally cleaner than a generic article, but its middle sections still read more like topic exposition than shortlist architecture.

**Distilled conclusion:**  
Market-entry reports should use typed decision blocks rather than long country-by-country exposition.

**Candidate action:** `TEMPLATE_CHANGE`

---

### 6. Decision usefulness

**Winner: GPT**

This was the largest gap.

GPT more clearly answered:

- whether to prioritize SEA now
- what the first sequence should be
- what the hard gates are
- how to know if the move is working
- what should happen if the company lacks the needed budget or deployment readiness

MiniMax gave a plausible judgment but remained less operational: informative, but weaker as a resource-allocation memo.

**Distilled conclusion:**  
The central gap in this case is not knowledge coverage. It is stronger **entry-decision architecture**.

**Candidate action:** `NEW_RULE` + `CHECKLIST_HARDENING`

---

## Core distilled findings

### Finding 1
For market-entry tasks, the output must explicitly answer not just whether to enter, but whether the recommendation is:

- `go`
- `not now`
- `pilot only`
- `phased entry`

A vague “有条件进入” is not enough unless the conditions are turned into visible hard gates.

**Action type:** `CHECKLIST_HARDENING`

---

### Finding 2
The report should explicitly distinguish these roles when relevant:

- regional hub
- first revenue beachhead
- later expansion market

Otherwise the phrase “priority country” becomes structurally ambiguous.

**Action type:** `NEW_RULE`

---

### Finding 3
Country analysis should use one visible comparison unit across the shortlist, rather than free-form country notes.

Useful columns or decision variables often include:

- demand / monetization quality
- compliance friction
- sales / channel friction
- localization burden
- suitability as first beachhead
- recommended entry motion

**Action type:** `NEW_RULE`

---

### Finding 4
Hard gates should be explicit and operational, not only qualitative.

Examples:

- minimum 12-month budget
- deployment / data-isolation capability
- compliance package readiness
- channel readiness
- language/localization readiness

**Action type:** `TEMPLATE_CHANGE`

---

### Finding 5
Scenario models, TAM / SAM / SOM, KPI plans, and financial targets improve decision usefulness, but they also create a risk of **professional-looking model drift** unless each number is labeled by evidence role.

**Action type:** `CHECKLIST_HARDENING`

---

### Finding 6
Citation / retrieval / placeholder artifacts in final delivery should be treated as hard fails, even when the underlying analysis is strong.

**Action type:** `CHECKLIST_HARDENING`

---

## Candidate-action summary

| # | Candidate action | Failure family | Action type | Proposed home |
|---|---|---|---|---|
| 1 | Add explicit market-entry trigger routing for go/no-go / regional expansion / country prioritization tasks | rule activation / execution failure | NEW_RULE | `SKILL.md` |
| 2 | Add a dedicated market-entry memo structure with recommendation, hard gates, country shortlist, sequencing, and milestones | decision utility / output structure | TEMPLATE_CHANGE | `references/decision-report-template.md` |
| 3 | Require market-entry reports to distinguish regional hub vs first revenue beachhead vs later expansion market when relevant | constrained-choice / choice architecture | NEW_RULE | `references/decision-report-template.md` + `checklists/option-selection-final-audit.md` |
| 4 | Require one visible comparison unit across countries/markets in a shortlist | constrained-choice / output structure | NEW_RULE | `references/option-selection-and-shortlist-discipline.md` |
| 5 | Require explicit hard gates and priority relative to alternatives in market-entry outputs | decision utility / rule activation | CHECKLIST_HARDENING | `checklists/final-audit.md` + `checklists/option-selection-final-audit.md` |
| 6 | Treat citation/retrieval artifact leakage as a final-delivery failure | source traceability / execution failure | CHECKLIST_HARDENING | `checklists/final-audit.md` |

---

## Triage notes

### Candidate 1
- **Why it matters:** without dedicated routing, reports drift into regional backgrounders even when the real question is entry sequencing under constraints
- **Why it is reusable:** applies to country expansion, cross-border SaaS GTM, regional prioritization, and go/no-go tasks beyond SEA
- **Why this home is best:** this is primarily a trigger / routing problem
- **Promotion status:** `PROMOTE_NOW`

### Candidate 2
- **Why it matters:** this was one of the clearest structural differences in the pair
- **Why it is reusable:** market-entry memos recur and need a stronger skeleton than generic decision memos
- **Why this home is best:** the issue is memo architecture, not source discovery
- **Promotion status:** `PROMOTE_NOW`

### Candidate 3
- **Why it matters:** many regional-expansion memos collapse different market roles into one sloppy “priority country” label
- **Why it is reusable:** the same distinction applies in Europe, LatAm, MENA, and multi-country rollouts generally
- **Why this home is best:** it belongs both in structure and in delivery-time audit
- **Promotion status:** `PROMOTE_NOW`

### Candidate 4
- **Why it matters:** free-form country notes feel rich but often hide weak ranking logic
- **Why it is reusable:** any multi-country market-entry memo benefits from a unified comparison unit
- **Why this home is best:** this is part of constrained-choice methodology, not a SEA-specific patch
- **Promotion status:** `PROMOTE_NOW`

### Candidate 5
- **Why it matters:** a recommendation without explicit gates or priority context is easy to misread as generic growth enthusiasm
- **Why it is reusable:** applies to most international-expansion and market-prioritization work
- **Why this home is best:** this is a final-delivery gate, not just prose advice
- **Promotion status:** `PROMOTE_NOW`

### Candidate 6
- **Why it matters:** artifact leakage makes an otherwise strong memo unshippable
- **Why it is reusable:** the same failure can recur in PDFs, markdown, and claim-rich outputs
- **Why this home is best:** it should fail the final audit regardless of how good the analysis is
- **Promotion status:** `PROMOTE_NOW`

---

## Things explicitly rejected

| Observation | Why rejected |
|---|---|
| GPT sounded more executive-ready | tone preference only unless tied to decision utility |
| New Singapore-first advice should become the default rule | too case-specific; could overfit to one regional-expansion pattern |
| MiniMax was just weaker overall | too vague to become a reusable rule |

---

## Final judgment

The stronger report won mainly because it behaved more like a **resource-allocation memo** and less like a regional market overview.

The most important lesson is not “GPT knew more SEA facts.” It is that a better market-entry output should visibly show:

- the real choice being made
- priority relative to alternatives
- country shortlist logic
- hard gates
- sequencing
- what changes the decision

This case is best understood as a mix of:

- **missing trigger hardness** for market-entry routing
- **template weakness** for expansion-sequencing memo structure
- **execution weakness** when reports drift back into overview mode or leak delivery artifacts
