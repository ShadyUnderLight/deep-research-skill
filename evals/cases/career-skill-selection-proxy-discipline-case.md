# Eval: Programming Language Learning Value — Career/Skill Selection Proxy Discipline Case

## Goal

Test whether a constrained-choice / option-selection report about programming language learning value correctly handles **proxy indicator discipline** for career/skill-selection data sources. The core challenge is that career/skill-selection reports rely on proxy indicators (job postings, salary surveys, TIOBE ranking, GitHub stars, Stack Overflow survey percentages) that must be labeled by epistemic role rather than treated as directly comparable facts.

This eval is based on the comparative distillation between a local report (`2026年编程语言学习价值深度研究报告.md`) and a GPT reference report on the same question, where the local report exhibited common proxy discipline failures:

- **unlabeled proxy indicators mixed in comparison tables** — TIOBE rank, SO usage %, package count, GitHub stars, US salary range all in one table without role labels
- **no default market or reader scope declaration** — US salary data and global rankings mixed without geographic scope
- **Source Register missing Claims Supported column** — source entries without claim-type attribution
- **composite scores without visible input-role transparency** — A+/B+ scores derived from mixed-proxy inputs without explaining how each proxy was weighted
- **self-assessment overclaim** — audit status claims full pass while evidence discipline gaps exist

## Prompt

A reader needs to decide which programming language to learn in 2026 for career investment. The shortlist is Swift, Kotlin, Rust, and Python. Produce a structured constrained-choice report that:

- declares the default reader persona (experience level, geographic market, decision goal, time window) in a scope block
- builds a replicable comparison framework with weighted variables, scoring rules, and at least 1 worked example
- gives per-persona recommendations (zero-base, 1-3 year, 5+ year) with why each wins and ranking-reversal conditions
- uses claim-level `[Sxx]` inline citations throughout
- includes a complete 7-column Source Register with Claims Supported specifying each source's claim type (job proxy / salary proxy / ecosystem size / official roadmap / community preference)
- labels all job-market, salary, ranking, package-count, star, and survey-percentage numbers with observed/proxy/assumption/model-output roles
- does not present US job-posting or salary data as global demand without explicit scope declaration
- labels learning time estimates with basis note (estimate / assumption / model-output)

## What this eval is testing

- **Default decision scope discipline** — whether the report declares target reader, market, decision goal, and time window upfront
- **Proxy indicator role labeling** — whether TIOBE, SO survey %, GitHub stars, LinkedIn/Indeed job counts, and salary data carry role labels (proxy / observed / assumption) rather than being treated as directly comparable facts
- **Source Register Claims Supported specificity** — whether the Claims Supported column goes beyond generic "supports language ranking" to specify job proxy / salary proxy / ecosystem size / official roadmap / community preference
- **US-vs-global scope boundary** — whether US salary or job data is scoped to US rather than generalized to global demand without declaration
- **Learning time estimate labeling** — whether learning duration claims carry estimate/assumption/model-output labels with basis notes
- **Per-persona recommendation discipline** — whether the report gives separate treatment for different experience levels rather than one generalized ranking
- **Self-assessment honesty** — whether the audit status block matches actual body execution

## Pass criteria

A passing answer should:

1. **Declare default decision scope.**
   - includes a scope block with target reader, market, decision goal, time window
   - scope mentions data geography (e.g., "US salary data, not global")

2. **Label all proxy indicators by role.**
   - TIOBE/RedMonk ranked as `proxy - search/attention`
   - Stack Overflow survey % as `proxy - developer sample`
   - GitHub stars as `proxy - public code activity`
   - LinkedIn/Indeed job counts as `proxy - job keyword`
   - Salary data as `proxy - mixed caliber` or equivalent
   - Role labels visible at row or column level in all comparison tables

3. **Use a complete 7-column Source Register with typed claims.**
   - Claims Supported column specifies claim type (job proxy / salary proxy / ecosystem size / official roadmap / community preference)
   - Every `[Sxx]` body citation maps to a register entry

4. **Scope US data to US market.**
   - US salary not presented as "global" without explicit scope note

5. **Label learning time estimates.**
   - Each learning duration labeled as estimate / assumption / model-output with brief basis
   - Bare "6 months" without basis is not acceptable for load-bearing comparisons

6. **Separate recommendations by persona.**
   - At minimum distinct treatment for zero-base, 1-3 year, and 5+ year readers

7. **Expose composite score input roles.**
   - If composite scoring is used (star ratings, weighted tables, A+/B+ tiers), each input dimension must carry a role label (observed / proxy / assumption / model-output)
   - At least 1 worked example or traceable score path to specific evidence anchors
   - Weights or priority order for each sub-dimension must be visible

8. **Self-assessment matches execution.**
   - If proxy labels are missing, quantitative-role cannot be ✅
   - If scope block is missing, decision-architecture cannot be ✅

## Failure signs

Mark this eval as failed if the answer does any of the following:

- comparison tables mix TIOBE, salary, stars, survey % without role labels (constrained-choice route hard-fail)
- no default scope block AND >3 unlabeled proxy indicators in load-bearing ranking positions (career/skill sub-gate compound hard-fail)
- Source Register lacks Claims Supported column or claims are generic ("supports language ranking") without type
- US salary presented as global demand without scope declaration
- learning time claims used for ranking without basis note
- composite scoring uses hidden weights or unlabeled input dimensions (aggregation not replicable)
- self-assessment claims full pass while scope or proxy labels are missing (process-integrity concern)

Missing scope block alone (without unlabeled proxies) is a conditional pass floor, not a hard-fail.

## Why this eval matters

This case guards against a specific failure mode in career/skill-selection constrained-choice reports: **proxy indicator conflation**. Unlike vendor selection (where pricing is an observed fact) or destination selection (where distance is measured), career/skill reports rely heavily on second-order proxy indicators that look quantitative but carry fundamentally different epistemic weights. A TIOBE ranking, a LinkedIn job count, and a Stack Overflow survey percentage are not comparable data types, but they are routinely placed in the same comparison table without distinction.

This eval extends the constrained-choice route to cover the proxy-heavy career/skill subclass, complementing existing constrained-choice evals that focus on source traceability (content-platform), quantitative role (indie-game), aggregation replicability (world-cup-prediction), and delivery structure (indie-dev).

## Current rule verdict

The current rules (informed by issue #308) should catch this as **conditional pass → fail**:

- `references/option-selection-and-shortlist-discipline.md` §默认决策口径 — Default decision scope requires scope declaration
- `references/option-selection-and-shortlist-discipline.md` §Common proxy indicators for career/skill selection requires role labeling by source type
- `checklists/option-selection-final-audit.md` §Career / skill selection sub-gate enforces scope, proxy roles, US-vs-global boundary
- Missing scope or unlabeled proxies for >3 load-bearing numbers → hard-fail per BLOCKER check

## Related evals

- `evals/cases/content-platform-constrained-choice-compounded-fail-case.md` — same route, compounded fail with body traceability and numeric role gaps
- `evals/cases/indie-dev-constrained-choice-delivery-fail-case.md` — same route, delivery fail with no source register and no numeric roles
- `evals/cases/indie-game-constrained-choice-quantitative-role-case.md` — same route, numeric role labeling gap
- `evals/cases/world-cup-prediction-constrained-choice-probability-method-case.md` — same route, probability method transparency gap
- `evals/comparative-distillation/tsmc-gpt-vs-deep-research-skill-comparative-distillation.md` — same comparative-distillation methodology

## Reviewer checklist

- Does the report have a default scope block (reader, market, goal, window)?
- Are TIOBE, SO survey, GitHub stars, job counts, and salary data labeled with role?
- Is the Source Register 7-column with typed Claims Supported?
- Is US data scoped (not silently presented as global)?
- Are learning time claims labeled with basis?
- Are recommendations separated by reader experience level?
- Does self-assessment match body execution?

## Suggested scoring

- **Pass**: full scope block, all proxy indicators role-labeled, 7-column register with typed claims, US data scoped, learning times labeled, per-persona recommendations, honest self-assessment
- **Conditional pass**: scope block present but incomplete (missing 1 field), proxy labels on most but not all tables, register claims typed but not all entries, US scope mentioned but not consistently, or scope block entirely missing but proxy labels otherwise clean — no hard-fail triggered
- **Fail**: comparison tables mix proxies without role labels (constrained-choice route hard-fail), or no scope block AND >3 unlabeled proxies (compound hard-fail), or register lacks Claims Supported column entirely, or US data presented as global without scope declaration, or self-assessment all ✅ while scope/labels missing (process-integrity concern)
