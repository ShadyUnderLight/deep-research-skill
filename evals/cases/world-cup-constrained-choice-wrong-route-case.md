# Eval: 美加墨世界杯 Constrained-Choice Wrong-Route Case

## Goal

Test whether the routing system correctly distinguishes between Market Outlook and Constrained Choice routes, especially when a task involves ranking/prediction burden (which disqualifies Market Outlook per ROUTING-MATRIX.md).

This eval targets a failure mode where:

- the report **declares a route** (Market Outlook)
- but the declared route is **wrong** for the task
- the task's core output (team ranking, winner prediction) has selection/recommendation burden, which is explicitly excluded from Market Outlook by the routing matrix
- the correct route (Constrained Choice) would have triggered different mandatory sections and hard-fail conditions

This is distinct from previous cases:

| Case | Route problem |
|------|--------------|
| AMAT / 恒大物业 / 中际旭创 | Route correct but execution incomplete |
| 欧冠决赛 | Route was **not activated** (shared-workflow mode) |
| 人形机器人 | Dual-route: primary correct, secondary unchecked |
| **This case** | Route was **actively declared but wrong** |

## Real case pattern

A user-provided 2026 美加墨世界杯夺冠前景深度研究报告 (World Cup 2026 Champion Prediction) dated **2026-05-29** demonstrates this pattern:

**What was done well:**
- ✅ Evidence grading excellent — [Confirmed]/[Inference]/[Unknown] consistently used throughout
- ✅ Counter-evidence excellent — Section 8 has 4 structured counter-arguments per team, far beyond simple disclaimers
- ✅ Conditional conclusions — all core predictions have explicit dependency conditions
- ✅ Multi-dimensional comparison — team-by-team analysis with strengths, weaknesses, routes to victory
- ✅ All quality gates passed

**What was wrong:**
- ❌ **Wrong route declared** — report declares "Market Outlook / Industry Evolution" (line 7), but ROUTING-MATRIX.md states Market Outlook does not apply to tasks with recommendation/ranking/selection burden. The core output (team ranking, winner prediction) carries selection burden, so Constrained Choice / Shortlist is the correct route.
- ❌ **2 hard-fail conditions triggered as a result** — because Market Outlook was declared, its "remains an industry overview instead of an outlook memo" hard-fail applies, and the constrained-choice specific hard-fails (shortlist construction, decision architecture) were not checked.
- ❌ **Probability precision illusion** — "15-20%" probability estimates imply precision that the underlying evidence cannot support. Directional ranking ("较高/中等/较低") would be more honest.
- ❌ **No inline source citations** — load-bearing claims lack [SN] inline references.

## What this eval is testing

### Failure Mode 1: Wrong route declaration

The report explicitly declares a route (Market Outlook), but this is incorrect for the task type. The routing matrix defines specific triggers for each route, and Market Outlook explicitly excludes ranking/recommendation tasks.

This is different from:
- **No route activation** (欧冠决赛) — route was not selected at all
- **Wrong secondary route** (人形机器人) — primary route was correct, secondary was attached but unchecked
- **Correct route with partial execution** (AMAT, 恒大物业, 中际旭创) — route was right, execution was incomplete

Here the **primary route itself is misidentified**. This is the most fundamental route-level failure.

### Failure Mode 2: Probability precision illusion

The report uses precise percentages ("15-20%") for inherently uncertain predictions (World Cup outcomes). This creates a false sense of precision. For tasks where the evidence base cannot support precise probabilities, directional classification ("higher / medium / lower") or ranges with explicit caveats should be used instead.

### Failure Mode 3: Missing constrained-choice structure

Because the wrong route was selected, the report lacks:
- explicit shortlist construction logic (why these 8 teams and not others?)
- decision architecture section
- ranking-reversal conditions labeled as such
- runner-up credibility analysis structured per constrained-choice template

These elements exist implicitly in the team-by-team analysis but are not structured as a decision framework.

## Pass criteria

A good answer should:

1. **Select the correct route** — for a task with ranking/prediction burden, Constrained Choice / Shortlist must be selected, not Market Outlook
2. **Route declaration matches ROUTING-MATRIX.md trigger conditions** — check the route's "Do not use" / "Often confused with" clauses before finalizing
3. **Probability honest with evidence** — use directional ranking or bounded ranges instead of precise percentages when the evidence base is inherently uncertain
4. **Constrained-choice structure present** — shortlist construction logic, decision architecture, ranking-reversal conditions, runner-up credibility analysis
5. **All hard-fail conditions of the correct route checked** — not just the declared route's

## Failure signs

Mark this eval as failed if the answer does any of the following:

- declares a route that is explicitly excluded for ranking/recommendation tasks per ROUTING-MATRIX.md
- uses precise probability percentages (e.g., "15-20%", "23%") for inherently uncertain predictions without justifying the precision
- lacks explicit shortlist construction logic for a task involving team/option ranking
- has hard-fail conditions triggered as a side effect of wrong route selection

## Why this case exists

This case adds coverage for a fundamental gap: **wrong route selection**. The routing matrix has clear "Do not use" clauses for each route, but the system does not always check them before declaring a route. This is a routing-layer failure distinct from execution-layer failures.

| Gap | Existing coverage | This case adds |
|-----|-------------------|----------------|
| **Wrong route declared** | No existing eval covers this | Actively choosing the wrong route despite declarable routing matrix clauses |
| **Probability precision** | `consensus-and-forward-pe-misuse-case.md` covers forward PE misuse | Over-precise probability for inherently uncertain predictions |
| **Market Outlook vs Constrained Choice confusion** | No eval tests this boundary | Routing matrix "Do not use" clause violation |

## Suggested intervention target

This case suggests changes at:

- `ROUTING-MATRIX.md` — strengthen the Market Outlook "Do not use" / "Often confused with" section with explicit examples (team ranking, tournament prediction) and add a hard-fail for wrong route declaration
- `references/route-activation-and-preflight.md` — add a step: "before finalizing route selection, check the route's 'Do not use' and 'Often confused with' clauses against the task"
- `SKILL.md` — strengthen the routing step to cross-check "Do not use" clauses before committing
- `references/market-outlook-and-scenario-discipline.md` — add guidance on when NOT to use this route (ranking/recommendation tasks)
- `checklists/route-activation-audit.md` — add: "verify the selected route is not in its own 'Do not use' clauses for this task type"

## Reviewer checklist

- Is the declared route correct for the task type per ROUTING-MATRIX.md triggers?
- Does the route's "Do not use" clause exclude this task?
- Are probability estimates appropriate to the evidence base, not over-precise?
- Does the report have the structure of the correct route (not just the declared route)?
- Are all hard-fail conditions of the correct route checked?

## Suggested scoring

- **Full pass**: correct route selected, all hard-fail conditions passed, probability honest with evidence
- **Pass with route fix**: content quality high but route wrongly declared (this case's level — fix routing declaration and structure)
- **Fail**: wrong route AND content quality issues

## Related evals

- `evals/cases/champions-league-constrained-choice-activation-case.md` — constrained-choice route not activated (route not selected at all, vs wrong route selected)
- `evals/cases/humanoid-robot-market-outlook-dual-route-case.md` — dual-route execution gap (primary route correct, secondary unchecked)
- `evals/cases/amat-listed-company-anchor-and-label-execution-case.md` — correct route but execution incomplete
- `evals/meta/rule-activation-and-execution-discipline.md` — missing-rule vs missing-trigger vs execution-failure diagnosis
