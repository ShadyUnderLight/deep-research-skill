# Market-Outlook Routing Validation Analysis

**Date:** 2026-05-27
**Purpose:** Analyze 3 real-case market-outlook task executions against the routing system
**Issue reference:** #94

---

## Methodology

Three research tasks were executed, each representing a distinct domain and decision-maker scenario:

| # | Task | Domain | Decision-maker | Evidence basis |
|---|---|---|---|---|
| 1 | AI Coding Agent market, 18-month outlook | Technology / Developer tools | Enterprise CTO | Live-fetched vendor pages (GitHub Copilot, Cursor) + model knowledge |
| 2 | Humanoid Robot industry, 12-month outlook | Hardware / Robotics | Industry investor | Live-fetched Unitree product page + model knowledge |
| 3 | China E-commerce landscape, 12-18 month outlook | Consumer / Retail | Brand operations director | Model knowledge (no public filing data live-verifiable) |

All three followed the same workflow: route preflight → execution contract → evidence gathering → report writing → route audit check.

---

## Dimension 1: Route Trigger

### Assessment criteria (from ROUTING-MATRIX.md lines 192-245)
- Primary route correctly selected as Market Outlook / Industry Evolution
- Closest alternative route identified
- Route not confused with Provider Selection, Constrained Choice, or generic research

### Results

| Criterion | Task 1 | Task 2 | Task 3 |
|---|---|---|---|
| Correct route selected | ✅ Market Outlook | ✅ Market Outlook | ✅ Market Outlook |
| Closest alternative identified | ✅ Provider/Vendor Selection | ❌ Not explicitly stated | ❌ Not explicitly stated |
| Route activation timing | ✅ Before evidence gathering | ✅ Before evidence gathering | ✅ Before evidence gathering |
| Route confusion risk | ✅ Avoided (not a provider comparison) | ✅ Avoided (not equipment selection) | ✅ Avoided (not a generic overview) |

**Observation:** Tasks 2 and 3 did not explicitly name the closest alternative route in the report body. However, the preflight decision was made correctly. The closest-alternative requirement is primarily an internal discipline rather than a delivery requirement, so this is minor.

**Result: Route trigger works correctly for market-outlook tasks across diverse domains.**

---

## Dimension 2: Reference Discipline Binding

### Assessment criteria (from references/market-outlook-and-scenario-discipline.md)
All sections of the required report logic must be present. Quantitative numbers must be labeled by role.

### Report structure compliance

| Required section (ref doc lines 81-91) | Task 1 | Task 2 | Task 3 |
|---|---|---|---|
| Current market snapshot | ✅ | ✅ | ✅ |
| What matters most | ✅ | ✅ | ✅ |
| Key drivers of change | ✅ | ✅ | ✅ |
| Key blockers / frictions | ✅ | ✅ | ✅ |
| Base case | ✅ | ✅ | ✅ |
| Alternative scenarios | ✅ | ✅ | ✅ |
| Stakeholder implications | ✅ | ✅ | ✅ |
| What would change the conclusion | ✅ | ✅ | ✅ |
| Recommended next steps / monitoring | ✅ | ✅ | ✅ |

### Drivers vs blockers separation (ref doc lines 97-127)

| Criterion | Task 1 | Task 2 | Task 3 |
|---|---|---|---|
| Drivers and blockers in separate sections | ✅ | ✅ | ✅ |
| Drivers are forces, not just trend names | ✅ | ✅ | ✅ |
| Blockers are specific, not generic | ✅ | ✅ | ✅ |

### Quantitative outlook discipline (ref doc lines 130-149)

| Criterion | Task 1 | Task 2 | Task 3 |
|---|---|---|---|
| Numbers labeled by role (observed/inferred/scenario) | ✅ Partial | ⚠️ Some unlabeled | ✅ Partial |
| "Synthetic precision" avoided | ✅ | ✅ | ✅ |
| "Illustrative calculation" labeled where used | ✅ | ✅ | N/A |

### Stakeholder implications (ref doc lines 153-173)

| Criterion | Task 1 | Task 2 | Task 3 |
|---|---|---|---|
| "Who should act now" stated | ✅ | ✅ | ✅ |
| "What to do now" and "what to avoid" separated | ✅ | ✅ | ✅ |
| Monitoring signals included | ✅ | ✅ | ✅ |

### Failure mode avoidance (ref doc lines 177-202)

| Failure mode | Task 1 | Task 2 | Task 3 |
|---|---|---|---|
| Overview drift (failure mode 1) | ✅ Avoided | ✅ Avoided | ✅ Avoided |
| Trend list without scenario logic (mode 2) | ✅ Avoided | ✅ Avoided | ✅ Avoided |
| Synthetic precision (mode 3) | ✅ Avoided | ✅ Avoided | ✅ Avoided |
| Hidden time-layer mixing (mode 4) | ⚠️ Partial risk | ⚠️ Partial risk | ⚠️ Partial risk |
| Action gap (mode 5) | ✅ Avoided | ✅ Avoided | ✅ Avoided |

**Result: The reference discipline binds correctly and produces the right structure. The weakest area is quantitative role labeling (numbers not always labeled) and time-layer mixing (forward-looking claims without source role blend into the narrative).**

---

## Dimension 3: Audit Binding

### Assessment criteria (from ROUTING-MATRIX.md line 221-224 and checklists/)
Required audits:
1. `checklists/forward-looking-claims.md`
2. `checklists/source-traceability.md`
3. `checklists/final-audit.md` (specifically lines 116-117 for market outlook)

### Audit execution

| Required audit | Task 1 | Task 2 | Task 3 |
|---|---|---|---|
| final-audit.md lines 116-117 | ✅ Run (current snapshot + drivers/blockers/scenarios checked) | ✅ Run | ✅ Run |
| forward-looking-claims.md | ⚠️ Consulted but not fully executed | ⚠️ Consulted but not fully executed | ⚠️ Consulted but not fully executed |
| source-traceability.md | ⚠️ Partially executed (evidence basis stated, but not claim-level traceability) | ⚠️ Partially executed | ⚠️ Partially executed |

### Specific audit findings

**final-audit.md line 116** ("a current market snapshot was verified before forward-looking sections"):
- ✅ Passed in all 3 tasks — snapshot always appears in section 1
- ✅ Evidence date basis explicitly noted in all tasks

**final-audit.md line 117** ("drivers, blockers, scenarios, and stakeholder implications are explicit"):
- ✅ Passed in all 3 tasks

**forward-looking-claims.md (key items that failed or were partial):**

| Checklist item | Status across tasks | Notes |
|---|---|---|
| "every forward-looking claim is identified and clearly labeled" | ❌ Failed | Some forward claims not labeled |
| "each prediction has at least one documented key assumption" | ⚠️ Partial | Some have, some don't |
| "each prediction has at least one stated condition under which it would not hold" | ✅ Passed | |
| "predictions are not presented as confirmed facts" | ✅ Passed | |
| "consensus estimates checked against latest data" | ⚠️ Partial | |
| "all predictions listed with confidence label, assumption, failure condition" | ⚠️ Partial | |

**Result: The two final-audit gates (lines 116-117) activate and hold. The forward-looking-claims.md checklist is listed as required but not fully executed at delivery time. This is the primary "binding gap" found.**

---

## Dimension 4: Artifact Contract Satisfaction

### Assessment criteria (from ROUTING-MATRIX.md lines 226-244)

### Visible artifact contract items

| Required visible element | Task 1 | Task 2 | Task 3 |
|---|---|---|---|
| Current market snapshot | ✅ | ✅ | ✅ |
| Key drivers of change | ✅ | ✅ | ✅ |
| Key blockers or friction points | ✅ | ✅ | ✅ |
| Base case | ✅ | ✅ | ✅ |
| Alternative scenarios | ✅ | ✅ | ✅ |
| Stakeholder implications | ✅ | ✅ | ✅ |
| Monitoring signals | ✅ | ✅ | ✅ |
| What would change the conclusion | ✅ | ✅ | ✅ |

### Hard-fail check (ROUTING-MATRIX.md lines 238-244)

| Hard-fail condition | Pass? |
|---|---|
| "Remains an industry overview instead of an outlook memo" | ✅ All passed |
| "Mixes observed facts with scenario assumptions" | ⚠️ Partial risk in forward-looking areas |
| "Gives forecasts without visible scenario structure" | ✅ All passed |
| "Hides stakeholder implications inside generic narrative" | ✅ All passed |

### Hard-fail check: opening section route visibility

| Route visibility | Task 1 | Task 2 | Task 3 |
|---|---|---|---|
| Report opens with current snapshot, not generic background | ✅ | ✅ | ✅ |
| Route inferable from artifact without internal notes | ✅ | ✅ | ✅ |
| Section order and burden allocation match route | ✅ | ✅ | ✅ |

**Result: Artifact contract is well-satisfied for all 3 tasks. The route is visible in the output.**

---

## Cross-Task Patterns

### What works reliably

1. **Route selection** — market outlook was the correct choice for all 3 tasks. No confusion with Provider Selection, Constrained Choice, or generic research
2. **Current snapshot anchoring** — easy to apply; evidence date basis was naturally included
3. **Drivers vs. blockers separation** — straightforward once the framework is known
4. **Scenario structure** — base case + alternative scenarios were easy to construct for all 3 domains
5. **Stakeholder implications** — most actionable when the decision-maker is clearly defined (Task 3 brand director was clearest; Task 1 CTO was also strong; Task 2 "investor" was slightly broader)

### What needs reinforcement

**Gap 1 (HIGH): Forward-looking claims discipline at delivery time**
- The `forward-looking-claims.md` checklist is **specified in ROUTING-MATRIX.md** as a required audit for market outlook
- It is **listed** as consulted in the Route Audit Evidence sections
- But it was **not fully executed** — forward-looking claims in all 3 tasks lack consistent source role and assumption chain labeling
- This is an **execution stability problem**, not a missing-rule problem (as classified in `evals/meta/rule-activation-and-execution-discipline.md`)
- This same gap was identified in the previous comparative distillation (ai-coding-agent-market-outlook-gpt-vs-minimax-comparative-distillation.md, candidate action 1, PROMOTE_NOW) and resulted in the two final-audit gates at lines 116-117

**Gap 2 (MEDIUM): Quantitative role labeling consistency**
- Some numerical claims are labeled (observed/inferred/scenario assumption) but not all
- No systematic method applied across all load-bearing numbers
- This is a execution consistency issue

**Gap 3 (LOW): Closest alternative route naming**
- Tasks 2 and 3 didn't explicitly name the closest alternative route
- Minor — this is a preflight discipline, not a delivery requirement

---

## Implication for Issue #94

### Question: Should we harden wording or add a sub-checklist?

**Recommendation: Smallest meaningful change only.**

The findings show that:
1. **Route definition (ROUTING-MATRIX.md)** — works correctly. No wording changes needed
2. **Reference discipline (market-outlook-and-scenario-discipline.md)** — works correctly. The structure produces good output
3. **Final-audit gates (final-audit.md lines 116-117)** — work correctly. The two gates pass for all tasks
4. **Forward-looking checklist execution** — this is the only real gap. The checklist exists and is specified as required, but doesn't reliably fire at delivery time

**The correct fix is NOT:**
- Adding more prose to ROUTING-MATRIX.md (route definition is adequate)
- Adding more prose to references/market-outlook-and-scenario-discipline.md (reference already covers this)
- Creating a checklists/market-outlook-audit.md (too heavyweight for a single gap; would duplicate existing final-audit)

**The correct fix IS:**
- One additional line in `checklists/final-audit.md` in the market-outlook section, bridging the gap between "forward-looking checklist exists" and "it was actually run":

```
- [ ] for market-outlook / industry-evolution tasks, all forward-looking claims have visible source role and time basis; derived, modeled, or load-bearing forecasts also show key assumptions and failure / reversal conditions
```

This turns the existing forward-looking discipline requirement (which lives in a separate checklist) into a **delivery-time gate** that is harder to skip. It follows the same pattern as the existing two gates (lines 116-117), is consistent with the project's escalation order (checklists before routing/references), and is the smallest possible change to close the observed gap.

### Rationale for not adding a sub-checklist

Adding `checklists/market-outlook-audit.md` would create a new maintenance burden without clear benefit. The existing `final-audit.md` already has route-specific sections for every specialized route. A market-outlook sub-checklist would duplicate the structure of `final-audit.md` lines 116-117 plus the forward-looking checklist items. The more minimal change — one additional final-audit line — achieves the same binding improvement without the overhead.

### ROADMAP alignment

This analysis confirms ROADMAP.md P1 line 16 was correct: the validation found exactly one gap (forward-looking claims execution), and it was wise not to harden wording before validating.

The ROADMAP's instruction "do not solve every new failure with more prose" (failure-taxonomy.md line 302) is directly relevant here. The gap is an execution-stability problem, not a missing-rule problem. One additional checklist gate is the appropriate response.
