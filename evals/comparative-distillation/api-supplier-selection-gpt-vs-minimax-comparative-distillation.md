# API Supplier Selection — GPT vs MiniMax Comparative Distillation

## Case identity

- **Task type:** vendor / provider selection under constraints
- **User objective:** 为一个做中文 AI Agent 产品的小团队，研究并比较潜在核心模型/API 供应商，形成可执行的选型备忘录
- **Compared outputs:** GPT report vs MiniMax report on the same prompt
- **Research date context:** around 2026-04-01
- **Distillation goal:** 不是判断哪份报告“更聪明”，而是提炼可复用、可审计、可执行的结构性差异，并将其归因为 `NEW_RULE` / `CHECKLIST_HARDENING` / `TEMPLATE_CHANGE` / `NO_ACTION`

---

## Prompt shape

The task was not a generic market overview. It was a constrained provider-selection memo for a Chinese AI Agent team.

That means the output should optimize for:

- provider choice under real deployment constraints
- shortlist / ranking usefulness
- current-state accuracy
- compliance / accessibility / pricing relevance
- decision-ready architecture, not vendor encyclopedia coverage

---

## Compared outputs at a glance

### GPT output
More clearly framed the task as a **decision memo** for a Chinese AI Agent team operating under cost, compliance, deployment, and product constraints.

Visible strengths:

- explicit decision framing
- clearer comparison dimensions
- stronger treatment of mainland-China accessibility / compliance / SLA / data controls
- more decision-useful recommendation structure
- more current-state-aware organization

### MiniMax output
Looked more like a **structured supplier overview** with recommendation tendencies, but less like a constrained-choice memo.

Visible weaknesses:

- drift toward vendor-by-vendor overview
- weaker comparison-unit discipline
- weaker aggregation logic
- clear signs of stale current-state anchoring
- evidence labels present, but not yet translated into claim-level traceability

---

## Six-dimension comparison

### 1. Current-state discipline

**Winner: GPT**

GPT treated the task as current-state-sensitive and organized the memo around current model families, current API structure, current pricing pages, current support-region constraints, and current enterprise controls.

MiniMax showed visible freshness failures. The clearest example was continuing to anchor OpenAI comparison around **GPT-4o**, rather than structuring the vendor section around the current primary API/model family. Similar issues appeared in how some provider positioning, pricing, and commercial availability claims felt like prior-state snapshots rather than explicitly verified current-state findings.

This matters because API supplier selection is inherently a **current-state-sensitive task**. If the report uses stale anchors, the comparison frame itself becomes distorted before ranking even begins.

**Distilled conclusion:**  
This is not just a factual miss. It is a **current-state verification failure** in a task where freshness should shape the report skeleton.

**Candidate action:** `NEW_RULE` + `CHECKLIST_HARDENING`

---

### 2. Numerical / pricing discipline

**Winner: GPT**

GPT handled pricing more like a decision variable and less like a fact dump. It more clearly surfaced:

- pricing unit differences
- currency differences
- batch discounts
- cache read/write implications
- segmented pricing by context/input length
- why a quoted price may or may not be comparable across providers

MiniMax included many price points, but the output leaned more toward enumerating representative model prices than building a comparable pricing frame for the actual buyer.

The result is that GPT was closer to answering:  
**“What will matter to this team’s actual cost structure?”**  
while MiniMax more often answered:  
**“What prices exist in public materials?”**

**Distilled conclusion:**  
The failure is not lack of numbers, but lack of a sufficiently explicit **comparison unit** and **decision-relevant pricing normalization**.

**Candidate action:** `CHECKLIST_HARDENING`

---

### 3. Source traceability / evidence weighting

**Winner: GPT**

GPT more clearly separated evidence layers:

- official model/pricing/docs pages
- SLA / status / privacy / data-control documentation
- benchmark or leaderboard material
- model cards and technical disclosures
- inferred deployment conclusions

MiniMax used `[CONF] / [LIKELY] / [UNCERTAIN]`, which is directionally correct and valuable. However, many claims still operated at the level of **source-bucket labeling**, not true **claim-level traceability**. Readers could often tell the general evidence tier, but not always which specific source anchored which comparative conclusion.

This was especially noticeable for positioning claims such as strength, maturity, or relative tier judgments.

**Distilled conclusion:**  
Evidence labels alone are not enough. For comparative memos, the skill must convert evidence tiering into **claim-to-source auditable support**.

**Candidate action:** `CHECKLIST_HARDENING`

---

### 4. Forward-looking claim discipline

**Winner: GPT (slight)**

Neither report’s biggest difference sat in forecasting quality, but GPT was more restrained. It tended to separate current constraints from deployment recommendations more cleanly.

MiniMax was more likely to let ecosystem maturity, product trajectory, or substitution recommendations blur into present-tense supplier reality. The issue was not outright fabrication, but weaker separation between:

- what is currently true
- what is likely to improve
- what is an operational recommendation

**Distilled conclusion:**  
This is a secondary difference, but it still supports the broader pattern: GPT preserved evidence-layer separation more reliably.

**Candidate action:** `NO_ACTION` or fold into existing forward-looking discipline

---

### 5. Structural readability / information density

**Winner: GPT**

GPT’s structure was visibly more aligned with constrained choice:

- executive summary
- scenario framing
- comparable dimensions
- cost / accessibility / privacy / customization
- recommendation logic

MiniMax’s structure still drifted toward a supplier-by-supplier overview. That is not inherently wrong, but in a provider-selection task it creates a familiar failure mode: the report becomes a **structured overview with recommendations attached**, instead of a **selection memo whose sections exist to support ranking and elimination**.

This is a classic **guide drift** problem: the output keeps informational structure, but loses choice architecture.

**Distilled conclusion:**  
For provider selection, the report must prioritize shortlist logic, elimination logic, and ranking reversibility over equal-weight vendor description.

**Candidate action:** `TEMPLATE_CHANGE`

---

### 6. Decision usefulness

**Winner: GPT**

This was the largest gap.

GPT more clearly helped the user decide what to do by providing:

- a China-relevant decision frame
- deployment assumptions
- multiple realistic strategy archetypes
- a “domestic core + optional overseas premium layer” type architecture logic
- a clearer mapping from constraints to recommendation

MiniMax had recommendation tendencies, but still behaved more like a report that helps the reader “understand the supplier set” than one that helps the reader “choose the operating architecture.”

The key distinction is:

- **GPT:** choice architecture
- **MiniMax:** vendor overview with recommendation drift

**Distilled conclusion:**  
The most important difference in this case is not broader knowledge coverage, but stronger **decision architecture under constraints**.

**Candidate action:** `CHECKLIST_HARDENING` + `TEMPLATE_CHANGE`

---

## Core distilled findings

### Finding 1
For provider-selection tasks, if the report does not explicitly define the **decision architecture** first, it will often drift into supplier encyclopedia mode.

- GPT framed the task as a constrained choice problem
- MiniMax framed it more like a structured comparative overview

**Action type:** `CHECKLIST_HARDENING`

---

### Finding 2
Model/API supplier comparison is inherently **current-state-sensitive**. Without an explicit current snapshot gate, stale anchors can distort the entire comparison.

Representative symptom in this case:

- continued reliance on **GPT-4o** as the main OpenAI comparison anchor rather than a current primary API/model-family framing

This is not a small naming issue. It signals that the memo may be comparing vendors through a partially outdated state model.

**Action type:** `NEW_RULE` + `CHECKLIST_HARDENING`

---

### Finding 3
For China-based teams, support regions, mainland accessibility, payment/signing reality, data residency, and SLA are not side risks. They are part of the **ranking architecture**.

- GPT treated these as decision-shaping variables
- MiniMax treated them more like cautionary notes

**Action type:** `TEMPLATE_CHANGE`

---

### Finding 4
Evidence labels such as `CONFIRMED / LIKELY / UNCERTAIN` are helpful, but not sufficient. Comparative memos still need claim-level traceability.

Without this, the output sounds disciplined while remaining hard to audit.

**Action type:** `CHECKLIST_HARDENING`

---

## Candidate actions

### Action A — Add a provider-selection current snapshot gate
**Type:** `NEW_RULE`

**Proposed rule:**

For model/API supplier selection tasks, produce a mandatory current snapshot before broader comparison. At minimum verify:

- current primary model/API family
- current pricing page and pricing unit
- current context window and key capability availability
- current support regions / mainland-China accessibility
- current data retention / training / enterprise control policy
- current SLA / status / service availability disclosures

If a key dimension cannot be verified, mark it as unknown rather than filling with likely-but-stale prior knowledge.

---

### Action B — Harden option-selection final audit for provider tasks
**Type:** `CHECKLIST_HARDENING`

Add provider-selection-specific checks:

- Is the decision frame explicit?
- Is the comparison unit explicit?
- Are 2–5 load-bearing variables explicitly named?
- Is there visible shortlist / elimination logic?
- Does the memo show what could change the ranking?
- Does it distinguish:
  - best overall
  - best fit for mainland-China team
  - best fallback
  - best cost-performance option

---

### Action C — Update decision-report template for provider selection
**Type:** `TEMPLATE_CHANGE`

Recommended structure:

1. Executive summary  
2. Decision architecture  
3. What matters most  
4. Current snapshot table  
5. Ranked shortlist  
6. Why top option wins  
7. Why runner-up remains credible  
8. Why other options lose  
9. Recommended deployment archetypes  
10. Risks / what changes the ranking  
11. Sources  

This reduces vendor-encyclopedia drift and increases choice usefulness.

---

### Action D — Strengthen freshness audit for fast-moving vendor/model reports
**Type:** `CHECKLIST_HARDENING`

Add explicit checks:

- Is the report still using visibly stale flagship anchors?
- Are old pricing/model snapshots being treated as current?
- Does the report separate current facts from historical background?
- Does it build from current official pages rather than remembered prior-state knowledge?

---

## Triage notes

### Was this a missing rule, missing trigger, or execution failure?

**Diagnosis:** mostly **missing trigger + execution failure**, not pure missing rule.

Why:

- The skill already contains current-state verification discipline
- The skill already contains option-selection and decision-usefulness discipline
- The skill already contains source-traceability expectations

But this case shows that those rules are not yet firing strongly enough for **model/API supplier selection** as a task family.

The most likely breakdown is:

1. **Missing trigger**
   - provider-selection should explicitly trigger:
     - current-state-sensitive task discipline
     - constrained-choice discipline
     - compliance-sensitive architecture choice discipline

2. **Execution failure**
   - even when the right rules conceptually exist, the output can still:
     - anchor on stale model generations
     - drift into vendor overview mode
     - relegate compliance/accessibility constraints to footnotes instead of ranking logic

### Final diagnosis
This case is best understood as:

- not mainly a missing knowledge issue
- not mainly a missing source-count issue
- but a failure to reliably convert existing discipline into visible report architecture

---

## Rejected observations

### Rejected observation 1
**“GPT is better mainly because it knows more facts.”**

Rejected because this is too shallow. The stronger difference is that GPT framed the task as a constrained provider-choice problem and then organized evidence around that frame.

---

### Rejected observation 2
**“MiniMax mainly needs more sources.”**

Rejected because the issue was not primarily source count. The issue was that evidence was not sufficiently transformed into selection structure.

---

### Rejected observation 3
**“This can be fixed by updating a few model names.”**

Rejected because the deeper requirement is a **current snapshot gate**, not a patch for one outdated model anchor.

---

## Bottom line

This comparison should not be distilled into “GPT had newer facts than MiniMax.”

The reusable lesson is stronger:

1. **Provider selection must begin with a current snapshot**
2. **Mainland accessibility / compliance / SLA must enter ranking architecture**
3. **Selection outputs must resist drifting into vendor encyclopedia mode**
4. **Evidence labeling must become claim-level traceability**

If only one lesson is promoted into a hard gate, it should be this:

> For model/API supplier selection tasks, current-state verification is not an extra check at the end. It is part of the report skeleton.
