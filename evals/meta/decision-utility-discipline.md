# Eval: Decision Utility Discipline

Use this meta-eval when a report sounds informed and well-sourced but does not clearly help the reader make a decision, judgment, or next step.

This eval is **not** about scoring a specific report's decision usefulness — use `evals/templates/decision-utility-rubric.md` (6-dimension scoring) for that. This eval is about deciding **which layer of the repo should change** when a decision-utility failure is observed.

## Goal

Distinguish five distinct root causes for a decision-utility failure:

1. **Missing route** — the task was misclassified as informational research when it should have been routed to a decision-focused route (provider selection, market entry, investment memo, etc.)
2. **Route with weak decision contract** — the correct route was selected, but its visible artifact contract does not require decision frame, load-bearing variables, or bottom-line conclusion
3. **Template gap** — the route's supporting template provides structure for facts but not for decision logic (no mandatory "what matters most", "bottom line", or "what would change the view" sections)
4. **Execution failure** — the route, contract, and template all exist, but the final output still reads like an informative overview rather than a decision support memo
5. **Wrong route for decision type** — the task type calls for a particular decision structure (e.g., go/no-go gates for market entry) but was routed to a route that supplies a different structure (e.g., option comparison)

This distinction matters because these five causes require completely different fixes (routing guidance / artifact contract / template structure / checklist hardening / re-routing).

---

## How to use this meta-eval

When you observe a decision-utility failure, walk through these questions in order:

### Step 1: Is it a missing route?
Check: was the task treated as generic research when it should have been routed to a decision-focused route?
- The routing matrix has 7 routes, most with explicit decision or judgment logic
- A task like "should we buy from vendor A or B?" should use provider selection, not generic overview
- If no route was selected → **missing route**

### Step 2: Route with weak decision contract?
Check: the correct route was selected, but does its artifact contract require decision-appropriate output?
- A route with recommendation burden (provider selection, market entry, investment memo) should require clear bottom-line recommendation
- A route with judgment burden (market outlook, competitive positioning) should require route-appropriate bottom line / judgment / scenario implication — not necessarily a hard recommendation
- If the route contract does not mandate decision or judgment elements appropriate to its task type → **weak route contract**

### Step 3: Template gap?
Check: even if the route contract is strong, does the template provide a clear place for decision or judgment output?
- `references/decision-report-template.md` covers most decision elements
- But if a specific route's template does not include mandatory judgment or recommendation output → **template gap**

### Step 4: Execution failure?
Check: all of the above existed, but the report still reads like an overview.
- The route was correct, the template has decision sections, but the output filled them with general description instead of sharp judgment
- → **execution failure** — fix goes in checklist hardening or execution contract

### Step 5: Wrong route for decision type?
Check: the task was routed to a route that supplies the wrong kind of decision structure.
- Example: a "go/no-go market entry" question routed to "constrained choice / shortlist" (option ranking instead of gate decision)
- Example: a market outlook task forced into "provider selection" would produce a false recommendation when the real need is scenario analysis
- If the route's default decision structure differs from what the task actually needs → **wrong route**

---

## Pass criteria for this meta-eval

A good diagnosis using this meta-eval should:

1. **Classify the root cause correctly.**
   - distinguish missing route from weak contract from execution failure
   - avoid defaulting to "execution failure" when the real gap is that the route never mandated decision output

2. **Point to the narrowest correct fix layer.**
   - missing route → routing selection guidance or SKILL routing step
   - weak route contract → update the route's visible artifact contract in `ROUTING-MATRIX.md`
   - template gap → update the route's supporting template in `references/`
   - execution failure → checklist hardening or execution-contract update
   - wrong route → route selection guidance or disambiguation in `ROUTING-MATRIX.md`

3. **Avoid conflating "informative" with "decision-useful".**
   - a report can be factually solid and well-organized yet still fail the decision-utility test
   - distinguish factual adequacy from decision support

---

## Review questions

When applying this meta-eval, ask:

- Was a primary route selected explicitly? If not, fix routing before anything else.
- Does the selected route's artifact contract require route-appropriate decision or judgment output (bottom line, recommendation, scenario implication, or what matters most)? If not, fix the contract.
- Does the route's supporting template provide a mandatory place for decision output? If not, fix the template.
- If route, contract, and template are all present, did the report fill them with decision logic or with general description? If description, fix execution.
- Is the decision gap recurring across multiple reports from the same route? If recurring, escalate from execution fix to structural fix.

---

## Output format for reviewers

When you apply this meta-eval, summarize the result as:

- **Observed decision gap:**
- **Was a route selected?** yes / no
- **Route used:**
- **Does the route contract require decision output?** yes / no
- **Root cause diagnosis:** missing route / weak route contract / template gap / execution failure / wrong route
- **Evidence for diagnosis:**
- **Narrowest correct fix layer:** routing / route contract / template / checklist / re-route
- **Recurring?** yes / no (first observed)
- **Recommended action:**

---

## Relation to the decision-utility rubric

This meta-eval is distinct from `evals/templates/decision-utility-rubric.md`:

- The **rubric** is a reusable scoring template for reviewers to score a specific report across 6 dimensions (0-2 each). It answers "how decision-useful is this specific report?"
- This **meta-eval** is used to determine whether a case or family of cases exposes a systematic decision-utility gap. It answers "what should the repo do about it?"

Use the rubric when scoring a specific report. Use this meta-eval when deciding whether the repo itself needs a structural improvement.

---

## Why this meta-eval exists

The repo has strong discipline for factual correctness (freshness, traceability, evidence weighting) but has been thinner on ensuring the output is actually useful for decision-making. The rubric makes decision-utility measurable; this meta-eval makes it actionable.

This meta-eval exists to prevent decision-utility failures from being treated as "just add more facts" problems when the real fix may be routing, contract, or template structure.
