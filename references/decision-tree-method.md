# Decision Tree / Consequence Mapping Method

Use this reference when a selection task involves major execution uncertainty that requires structured post-decision branch planning.

This file is not needed for every selection task. It activates only when the chosen option has distinct success, partial-failure, and total-failure paths that need explicit planning.

---

## When to use

Apply this method when **all three** conditions hold:

1. the selection involves a high-switching-cost commitment (for example vendor lock-in, market entry, major procurement, multi-year partnership)
2. the execution outcome is genuinely uncertain (for example unproven integration, regulatory risk, dependent on external conditions)
3. the user needs to plan monitoring signals and exit conditions before committing

Do not apply when:

- the selection is low-stakes or easily reversible
- the options are similar enough that switching is trivial
- the user only needs a ranking, not a post-decision plan
- the existing "what would change the conclusion" section in the report already covers the uncertainty adequately

---

## Core rule

A decision tree answers a different question than option-selection ranking.

- **Option-selection** answers: "Which option is best now?"
- **Decision-tree** answers: "After choosing, how do I monitor, branch, and exit if things go wrong?"

Do not confuse these. The decision tree does not replace the ranking. It extends the ranking into execution planning.

---

## Core structure

For each key decision point with major uncertainty, expand 2-3 branches:

### Branch 1: Primary path succeeds

- **Trigger conditions**: what must hold for this branch to activate (for example POC passes threshold, SLA met, cost within budget)
- **Expected outcome**: what success looks like concretely
- **Monitoring signals**: what metrics or events to track continuously
- **Next milestone**: what the next decision gate is

### Branch 2: Primary path blocked, fallback activated

- **Trigger conditions**: what signals indicate the primary path is failing (for example POC fails, SLA breach, cost overrun exceeds threshold)
- **Fallback action**: what the fallback option is and how to activate it
- **Switching cost**: time, money, or capability lost in the switch
- **Exit signal**: conditions under which the fallback should also be abandoned

### Branch 3: All paths blocked, reassessment required

- **Trigger conditions**: what indicates both primary and fallback have failed
- **Reassessment scope**: what to re-evaluate (for example requirements, timeline, build-vs-buy, defer)
- **Lessons learned**: what the failure reveals about the original decision assumptions

Not every decision point needs three branches. Two branches (success / failure) are sufficient when the fallback is obvious or the switching cost is low.

---

## Output format

Use a compact block per decision point. Do not write a separate report section for the decision tree unless the task is unusually complex.

### Minimal format

```
### Decision point: [choice description]

**If primary succeeds:**
- Trigger: [condition]
- Monitor: [signal]
- Next gate: [milestone]

**If primary fails:**
- Trigger: [condition]
- Fallback: [action]
- Switch cost: [estimate]
- Exit if: [abandonment condition]

**If all blocked:**
- Trigger: [condition]
- Reassess: [scope]
```

### Full format (for complex decisions)

Use the three-branch structure from the Core structure section above, with explicit monitoring signals and next milestones for each branch.

---

## Relationship to existing disciplines

### vs "What would change the conclusion"

- **Change-the-conclusion** asks: "What assumption change would make a different option rank first?" (pre-decision)
- **Decision tree** asks: "After choosing option A, what execution branches exist and when do I switch?" (post-decision)

These are complementary. A strong selection report may include both.

### vs Sensitivity analysis

- **Sensitivity analysis** asks: "If a key assumption shifts by X%, does the conclusion change?" (assumption testing)
- **Decision tree** asks: "If execution path Y materializes, what do I do?" (execution planning)

Sensitivity tests assumptions. Decision trees plan actions.

### vs Market-outlook scenarios

- **Market-outlook scenarios** ask: "How will the market evolve under different conditions?" (external environment)
- **Decision tree** asks: "How does my chosen option perform under different execution paths?" (internal commitment)

Market outlook is about the world. Decision trees are about your choice.

---

## Common failure modes

### Failure mode 1: Too many branches

More than 3 branches per decision point creates analysis paralysis.

**Fix:** limit to 2-3 branches. Merge low-probability paths into the "all blocked" branch.

### Failure mode 2: No trigger conditions

Branches without measurable triggers are just wishful thinking.

**Fix:** each branch must name a specific, observable condition (for example "uptime drops below 99.5% for 3 consecutive days", not "if things go wrong").

### Failure mode 3: No monitoring signals

Without monitoring signals, the decision tree is a static document, not an execution tool.

**Fix:** each branch must name at least one signal to watch.

### Failure mode 4: Confusion with ranking logic

Using the decision tree to justify the ranking instead of planning execution.

**Fix:** the decision tree should appear **after** the ranking is established, not as part of the ranking logic.

### Failure mode 5: Applied to low-stakes choices

Adding decision trees to trivial or easily reversible choices bloats the report.

**Fix:** enforce the "When to use" conditions strictly.

---

## Practical heuristics

When building a decision tree, ask:

- What is the single most fragile step in the chosen option's execution?
- What observable signal would tell me that step is failing?
- What is the realistic fallback, and how long does switching take?
- If both primary and fallback fail, what does that reveal about my original assumptions?
- Am I planning actions, or just describing risks?

When deciding whether to include a decision tree at all, ask:

- Is the switching cost high enough to justify pre-planning?
- Is the execution uncertainty genuine, or already well-understood?
- Would the user actually monitor signals and act on them, or is this theoretical?
- Does the existing "what would change the conclusion" section already cover this adequately?

---

## Bottom line

A decision tree turns a selection recommendation into an execution plan.

The job is not to add branches for completeness. The job is to help the user know what to watch, when to act, and when to exit.
