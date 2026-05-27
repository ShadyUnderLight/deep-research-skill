# Eval: Decision Utility Discipline

Use this eval when a report sounds informed and well-sourced but does not clearly help the reader make a decision, judgment, or next step.

This is a meta-eval. It is not about whether the report's facts are correct. It is about whether the report is structured for decision support rather than informative summary — and whether the route correctly activated decision-utility disciplines at the right level.

## Goal

Distinguish three different failure types:

1. **Missing decision frame** — the report never identifies what judgment or choice the reader faces
2. **Weak load-bearing variable selection** — the report covers many dimensions without identifying 3-5 factors that actually determine the answer
3. **Soft conclusion** — the report stays noncommittal or buries the bottom line even when evidence could support a judgment

This distinction matters because these three problems require different fixes (route selection, template structure, execution contract, or checklist hardening).

---

## Typical cases where this eval should be used

- provider comparison that reads like a vendor catalog instead of a choice memo
- market outlook that summarizes trends but does not recommend a position or scenario
- company report that profiles the business but does not state an investment judgment
- option analysis that lists pros and cons without a clear recommendation
- shortlist memo where narrative weight is spread evenly across all options

---

## What this eval is testing

### Failure Mode 1: Missing decision frame

The report explains the topic well, but never clarifies what the reader should decide.

Examples:
- the practical question is unclear
- decision context is absent or buried
- criteria that would change the final answer are unnamed

### Failure Mode 2: Weak load-bearing variable selection

Many facts are presented, but the report does not prioritize the few variables that matter most.

Examples:
- too many dimensions feel equally weighted
- the report answers "what exists" better than "what matters most"
- supporting detail is not subordinated to the primary drivers

### Failure Mode 3: Soft or buried conclusion

The report generates useful analysis but does not convert it into a bottom line.

Examples:
- the report stays noncommittal when evidence supports a judgment
- the conclusion exists but is soft, buried, or not operationally useful
- "what could change the conclusion" is absent even when uncertainty is material

---

## Pass criteria

A good answer should:

1. **Make the decision frame explicit.**
   - state the practical question clearly
   - show decision context rather than topic summary
   - name criteria that would change the final answer

2. **Identify load-bearing variables.**
   - prioritize 3-5 major variables that determine the conclusion
   - explain why those matter more than the rest
   - subordinate supporting detail to those variables

3. **Deliver a sharp conclusion.**
   - give an explicit bottom line
   - include a recommendation, ranking, or directional judgment when appropriate
   - state what could change the conclusion

4. **Avoid informative-but-useless shape.**
   - do not let generic description substitute for decision support
   - do not leave the reader to infer the bottom line from scattered details

---

## Scoring guide

Use a simple 0-2 scale.

### 0 = decision-utility failure
- the report is informative but leaves the reader unsure what to decide
- no decision frame, no load-bearing variable selection, or no conclusion

### 1 = partial decision usefulness
- some decision frame exists, but connection to body is weak
- or load-bearing variables are named but not consistently used
- or a conclusion exists but is soft or buried

### 2 = strong decision usefulness
- the decision frame is explicit and drives report structure
- load-bearing variables are clearly identified and prioritized
- the bottom line is sharp and actionable
- what could change the conclusion is explained

---

## Review questions

When using this eval, ask:

- Does the report identify what judgment or decision the reader faces?
- Does it identify what matters most, or does it treat all facts as equally important?
- Does it help the reader choose, prioritize, approve, reject, or investigate further?
- Does it give a clear bottom line?
- Does it explain what could change the conclusion?
- Would a busy decision-maker get value from the first page alone?
- Is the right fix a route change, a template update, an execution-contract improvement, or a new checklist gate?

---

## Output format for reviewers

When you apply this eval, summarize the result as:

- **Expected decision frame:**
- **Load-bearing variables identified:**
- **Conclusion sharpness:**
- **Change-the-conclusion clarity:**
- **Diagnosis:** missing decision frame / weak variable selection / soft conclusion / no failure
- **Best next fix:** routing update / template update / execution-contract hardening / checklist update / new case eval only

---

## Suggested prompts

- Should we partner with this company, buy from it, or wait six months?
- Which of these three vendors is best for a mid-market deployment, and why?
- Is this market attractive enough for entry in the next 12 months?
- Should an investor treat this stock as a growth opportunity, a hold, or an avoid-for-now case?

---

## Relation to the decision-utility rubric

This meta-eval is distinct from `evals/templates/decision-utility-rubric.md`:

- The **rubric** is a reusable scoring template for reviewers to score a specific report across 6 dimensions (0-2 each).
- This **meta-eval** is used to determine whether a case or family of cases exposes a systematic decision-utility gap, and to decide which layer of the repo should change in response.

Use the rubric when scoring a specific report. Use this meta-eval when deciding whether the repo itself needs a structural improvement in how it handles decision usefulness.

---

## Why this eval exists

The repo has strong discipline for factual correctness (freshness, traceability, evidence weighting) but has been thinner on ensuring the output is actually useful for decision-making.

This eval exists to prevent the system from producing reports that are factually solid but decisionally weak — and to ensure that decision-utility failures are recognized as a distinct family requiring targeted structural fixes, not just more facts or better wording.
