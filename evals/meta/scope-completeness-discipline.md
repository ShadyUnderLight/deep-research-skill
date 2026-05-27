# Eval: Scope Completeness Discipline

Use this meta-eval when a report claims broad scope (global / comprehensive / industry-wide / full landscape) but you suspect the actual coverage may not match the implied scope.

This eval is **not** about scoring a specific report's scope completeness — use `evals/cases/global-market-scope-completeness-case.md` (pass criteria + scoring guide) for that. This eval is about deciding **which layer of the repo should change** when a scope-completeness failure is observed.

## Goal

Distinguish five distinct root causes for a scope-completeness failure:

1. **Missing rule** — the repo truly lacks guidance on what "global" / "comprehensive" should mean
2. **Missing route trigger** — the task was not routed into a checklist or reference that checks scope boundaries
3. **Route misclassification** — the task was routed to a route whose discipline set does not include scope checking (e.g., a global market report routed as "provider selection")
4. **Execution failure** — the route was correct and the checklists exist, but the final output still omitted load-bearing geographies or segments
5. **Data unavailability** — the omitted geography/segment genuinely lacks accessible sources, but the report did not state this omission

This distinction matters because these five causes require completely different fixes (reference prose / routing matrix / route attachment / checklist hardening / disclosure requirement).

---

## How to use this meta-eval

When you observe a scope-completeness failure, walk through these questions in order:

### Step 1: Is it a missing rule?
Check: does the repo have any document that defines what "global scope" must include?
- Reference: `references/failure-taxonomy.md` — Family F (records the gap but does not define a standard)
- Reference: `evals/cases/global-market-scope-completeness-case.md` (defines the evaluation but not a reusable rule)
- If no document defines the minimum coverage for a global claim → **missing rule**

### Step 2: Is it a missing route trigger?
Check: does `ROUTING-MATRIX.md` or any existing route attach a scope-completeness discipline for this task type?
- Cross-cutting discipline "scope completeness" now exists in `ROUTING-MATRIX.md`
- If the task type is global/industry-wide but the route selected does not reference this discipline → **missing route trigger**

### Step 3: Is it route misclassification?
Check: was the task routed to a specialized route that does not naturally require scope checking?
- For example: a global AI market report routed as "provider / vendor selection" would miss scope-completeness entirely
- If the chosen route's visible artifact contract and secondary disciplines do not include scope → **route misclassification**

### Step 4: Is it execution failure?
Check: all of the above existed, but the report still shows scope gaps.
- The route was correct, the discipline was attached, but the output omitted key geographies
- The report says "global" but effectively covers only the most visible regions
- → **execution failure** — fix goes in checklist hardening or execution contract

### Step 5: Is it data unavailability?
Check: the omitted geography/segment may genuinely be poorly documented.
- If so, the report should state the omission explicitly rather than silently excluding it
- If it did not state the omission → still an execution failure (disclosure requirement not met)

---

## Pass criteria for this meta-eval

A good diagnosis using this meta-eval should:

1. **Classify the root cause correctly.**
   - distinguish missing rule from missing trigger from execution failure
   - avoid defaulting to "missing rule" when the real gap is route misclassification or execution drift

2. **Point to the narrowest correct fix layer.**
   - missing rule → `references/` or a new reference
   - missing route trigger → `ROUTING-MATRIX.md` or route attachment update
   - route misclassification → route selection guidance or route contract
   - execution failure → checklist hardening or execution-contract update
   - data unavailability → disclosure requirement (update case eval or reference)

3. **Avoid treating every scope failure as a new rule problem.**
   - most scope failures in a maturing repo will be route or execution failures, not missing rules

---

## Review questions

When applying this meta-eval, ask:

- Does a scope-completeness discipline exist in the routing matrix? If not, that is the first fix.
- If it exists, was it attached for this task type? If not, the route attachment is the fix.
- If it was attached, does the report show evidence of scope checking (explicit coverage boundaries, omitted-region disclosure)? If not, execution failed.
- Is this the first observed scope-completeness failure, or is it recurring? If recurring, escalate from execution fix to structural fix.
- Would a different route selection have naturally triggered scope checking? If yes, fix route selection guidance.

---

## Output format for reviewers

When you apply this meta-eval, summarize the result as:

- **Observed scope gap:**
- **Root cause diagnosis:** missing rule / missing route trigger / route misclassification / execution failure / data unavailability
- **Evidence for diagnosis:**
- **Narrowest correct fix layer:** references / routing matrix / route attachment / checklist / case eval only
- **Recurring?** yes / no (first observed)
- **Recommended action:**

---

## Related files

- `evals/cases/global-market-scope-completeness-case.md` — concrete scoring tool for a specific report
- `references/failure-taxonomy.md` — Family F: Scope Completeness and Coverage Geometry
- `ROUTING-MATRIX.md` — cross-cutting discipline: scope completeness

---

## Why this meta-eval exists

The case eval (`global-market-scope-completeness-case.md`) can tell you whether a specific report has a scope problem. This meta-eval exists to answer the next question: **what should the repo do about it?**

Without this distinction, every scope failure risks being treated as a missing-rule problem, leading to more prose when the real fix may be routing, attachment, or execution hardening.
