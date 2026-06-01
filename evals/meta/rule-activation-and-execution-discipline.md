# Eval: Rule Activation and Execution Discipline

Use this eval when a report appears to "know the rules" but still fails to execute them reliably in the final output.

This is a meta-eval. It is not primarily about whether a rule exists in the repo. It is about whether the correct rule was activated and whether its effects are visible in the delivered report.

## Goal

Distinguish three different failure types:

1. **Missing rule** — the repo truly lacks guidance
2. **Missing trigger** — the rule exists, but the task did not route into the right checklist/reference
3. **Execution failure** — the rule was likely triggered, but the final output still violated it

This distinction matters because these three problems require different fixes.

---

## Typical cases where this eval should be used

- listed-company report with no current market snapshot even though listed-company checklist exists
- report includes confidence labels in some sections but drops them around estimates
- report has a source list but still lacks claim-level inline citations
- executive summary uses bullets but still violates one-insight-per-bullet discipline
- forward-looking statements appear without named source even though forward-looking checklist exists

---

## What this eval is testing

### Failure Mode 1: Trigger not activated

The task clearly belongs to a known gate, but the delivered report shows no evidence that the gate ran.

Examples:
- listed company, but no stock-price / market-cap / valuation snapshot
- current product / current ranking question, but no freshness verification
- roadmap / estimate-heavy output, but no forward-looking discipline
- structured or investment memo, but no source-traceability system

### Failure Mode 2: Partial activation, incomplete execution

The report shows signs that the rule was recognized, but execution leaks in key places.

Examples:
- report has a confidence legend, but some forecast language is unlabeled
- report has source register, but body claims still lack citations
- exec summary uses bullets, but each bullet still contains multiple insights

### Failure Mode 3: Cosmetic compliance

The report imitates the shape of compliance without achieving real discipline.

Examples:
- labels exist, but do not change certainty behavior
- sources exist, but reader still cannot audit claims
- risks section exists, but counter-evidence is weak or ceremonial
- "what matters most" section exists, but contains background instead of load-bearing variables

### Failure Mode 4: Misleading execution (label inflation / evidence-label contradiction)

The rule was triggered and execution traces are visible, but the traces are inaccurate or contradict the content they accompany. Unlike partial activation (FM2, where traces are incomplete) or cosmetic compliance (FM3, where structure lacks substance), FM4 describes traces that are actively misleading — they signal a quality that the content does not deliver.

**Key distinction:** FM4 is about the **accuracy** of execution traces, not their completeness (FM2) or authenticity (FM3).

Examples:
- confidence labels exist (Confirmed / Likely / Open), but inferences are labeled as confirmed facts — readers see labels and assume evidence-backed rigor, yet the labels misrepresent the actual evidence strength
- an evidence format (citation style, source register) exists, but load-bearing claims carry citations that do not actually support the attributed claim (citation-content mismatch)
- an explicit evidence grading system is present, but the grade assigned to a claim contradicts the underlying source quality (e.g., a weak secondary source is graded "strong")

Why this is more dangerous than FM2 or FM3: a reader who sees structural markers (labels, citations, grades) assumes a quality guarantee. When those markers are wrong, the trust premium is spent on unreliable signals — the report is harder to evaluate correctly than if no markers existed.

Key diagnostic question: "Are the execution traces factually accurate for the content they accompany, or do they misrepresent the underlying evidence?"

Fix direction: not "add more rules" but "tighten the quality threshold for existing rules" — raise the bar for when a label or grade can be used, add hard-fail conditions for mislabeled claims (label inflation), and verify that citations actually support the claims they are attached to during the final audit.

See also: `evals/cases/amat-listed-company-anchor-and-label-execution-case.md` for a concrete example of label inflation (Confirmed label applied to an inferential claim).

---

## Pass criteria

A good answer should:

1. **Activate the correct gate for the task.**
   - listed company -> listed-company checklist visible in output shape
   - forward-looking task -> assumptions / source basis / failure conditions visible
   - current-state task -> current snapshot visible before broader analysis
   - structured memo -> claim-level traceability visible

2. **Leave visible execution traces.**
   - a reviewer should be able to infer which rules fired from the final report itself
   - compliance should not depend on reading the hidden reasoning

3. **Avoid partial-rule collapse.**
   - do not comply in headers but fail in body claims
   - do not comply in detail sections but fail in exec summary
   - do not comply on some estimates but not others

4. **Avoid cosmetic compliance.**
   - report structure should improve auditability and judgment quality, not just look more formal

---

## Scoring guide

Use a simple 0-2 scale.

### 0 = failed activation
- the relevant rule family should clearly have fired, but there is little or no output evidence that it did

### 1 = partial activation / unstable execution
- some rule traces exist, but important output areas still violate the discipline

### 2 = stable activation and execution
- the correct gates appear to have fired and the final report shows consistent compliance in the places that matter most

---

## Review questions

When using this eval, ask:

- Which checklist/reference should have been triggered by this task?
- What visible artifact would prove that it was triggered?
- Did the final report contain that artifact?
- If partially, where did compliance break: header, summary, body, sources, or bottom line?
- Was there evidence that the route was converted into a section-level execution contract before drafting?
- Did the opening 20-30% of the report already reveal the chosen route, or could it have belonged to a generic overview?
- Is the right fix a new rule, a stronger trigger, a stronger execution contract, or a stronger final-audit gate?
- If execution traces exist, are they factually accurate for the content they accompany, or do they misrepresent the underlying evidence?
- Are labels, citation links, and evidence grades consistent with the actual strength of the evidence they are attached to?

---

## Output format for reviewers

When you apply this eval, summarize the result as:

- **Expected gate(s):**
- **Expected execution contract:**
- **Visible signs of activation:**
- **Where execution held:**
- **Where execution leaked:**
- **Diagnosis:** missing rule / missing trigger / execution failure / misleading execution
- **Best next fix:** reference update / checklist update / SKILL routing update / execution-contract hardening / final-audit update / new eval only

---

## Suggested prompts

- Research Apple as an investment case, including valuation, roadmap, and target-price debate.
- Is Xiaomi currently the leader in China's flagship phone market? Give a current-state view.
- Write a listed-company memo on MiniMax with market snapshot, risks, and evidence labels.
- Compare three public AI companies and include current valuation, ranking claims, and 12-month outlook.

---

## Route activation failures

Common route-activation failures include:

- a specialized route should have been chosen, but the work stayed generic
- a route was selected too late, after the report shape had already drifted
- multiple routes were named, but none actually determined structure or audit burden
- the route was named, but its artifact contract was not visible in the final report
- required secondary disciplines were named but not operationalized

When route execution fails, check in this order:

1. Was a primary route selected explicitly?
2. Was it the route that most strongly determined structure and audit burden?
3. Were required secondary disciplines attached?
4. Was the artifact contract visibly executed?
5. Only then decide whether the route definition itself needs revision.

Do not respond to route misses by endlessly adding more trigger language to `SKILL.md` if the real problem is preflight invisibility or execution drift.

## Why this eval exists

As the repo matures, more failures are no longer caused by missing knowledge. They are caused by weak routing and unstable execution.

This eval exists to prevent the project from solving every new failure by adding more prose rules when the real problem is that the right rule never became a stable delivery-time behavior.
