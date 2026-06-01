# Eval: Champions League Final Constrained-Choice Activation Case

## Goal

Test whether a constrained-choice / shortlist / option-selection task can be properly route-activated before execution, rather than being produced in shared-workflow mode with the correct structure emerging by coincidence.

This eval targets a failure mode where:

- the report's content and structure **happen to match** a mature route (constrained-choice)
- but the route was **never explicitly activated** — no pre-collection route selection, no execution contract, no checklist audit
- the report passes most quality checks but has avoidable structural defects that a route contract would have caught early

This is distinct from previous cases where the route was activated but execution was incomplete. Here the route structure emerged **by accident** rather than by design.

## Real case pattern

A user-provided Champions League Final analysis report (PSG vs Arsenal, dated **2026-05-29**) demonstrates this pattern:

**What was done correctly (by instinct):**
- ✅ Judgment-first summary appears early (executive summary at §0)
- ✅ Comparative table with 10 dimensions (§5.1)
- ✅ Winner prediction with confidence (PSG, 60-65%, §6.1)
- ✅ Why the top option wins — 6 reasoning chains (§6.2)
- ✅ Why the runner-up remains credible — full dedicated chapter (§7) with 3 scenarios
- ✅ Ranking-reversal conditions — 4 specific conditions (§6.3)
- ✅ Counter-evidence chapter with real evidence, not strawman (§7)
- ✅ Uncertainty register (§8.1) — lineup, injuries, referee, weather marked as [unknown]
- ✅ All 7 quality gates passed
- ✅ All hard-fail conditions passed

**What was missing (route activation):**
- ❌ No explicit route selection before collection — produced in shared-workflow mode
- ❌ No execution contract existed — mandatory sections were not pre-committed
- ❌ No checklist audit was run — defects were not caught
- ❌ Background-first drift (§1) — 20 lines of pure background (including The Killers halftime show info) immediately after the executive summary, breaking the judgment flow
- ❌ No route-specific labels — "shortlist", "decision architecture", "reversal conditions" are implicit in the content but not named as structural tags
- ❌ No explicit shortlist construction logic — the two options are a natural binary (Champions League Final), but the report never states "these are the only two options because..."
- ❌ Source granularity inconsistent — some key inferences lack specific source attribution (e.g., "法甲竞争力不足使PSG可以轮换" without citing specific matches or data)

## What this eval is testing

### Failure Mode 1: Route activation gap (not execution gap)

The primary failure is that the route was never selected. Unlike previous cases where:

- AMAT: route declared but execution incomplete
- 恒大物业/中际旭创: route executed with minor gaps

This case: **route structure emerged by coincidence, not by design**.

This matters because:
- without a route contract, background-first drift (§1) was not caught before delivery
- without pre-committed mandatory sections, the report could have easily drifted into generic overview
- the quality depends on the model's instinct rather than systematic process

### Failure Mode 2: Background-first drift in a constrained-choice task

Even though the executive summary is judgment-first, §1 immediately follows with 20 lines of pure background (match info, venue, historical context, halftime show entertainment). This breaks the judgment flow that the executive summary established.

In a constrained-choice task, background should be minimized and placed after the decision architecture.

### Failure Mode 3: Implicit route structure without explicit labels

The report's structure happens to match constrained-choice requirements, but:
- "shortlist construction" is implicit (the two finalists are obvious, but never stated as a deliberate choice)
- "reversal conditions" exist in content but are not labeled as such
- "decision architecture" is not a named concept in the report

This makes the report harder for a reader to navigate as a decision document.

## Pass criteria

A good answer should:

1. **Explicit route selection** — the constrained-choice route is selected and declared before evidence collection begins
2. **Execution contract exists** — mandatory sections, opening requirements, and minimize/move-later items are pre-committed
3. **Judgment flow is uninterrupted** — once judgment is presented (§0 or equivalent), background does not immediately break the flow; background is compressed, labeled as "Background", or placed after the decision architecture
4. **Route-specific labels are visible** — "shortlist", "decision architecture", "comparison framework", "reversal conditions" are named as structural elements, not just implicit in content
5. **Shortlist construction is explicit** — even when options are obvious (binary final), the report states the selection boundary and confirms no other options are credible
6. **Source granularity is consistent** — each key inference has a specific source (match, statistic, report), not just a vague attribution

## Failure signs

Mark this eval as failed if the answer does any of the following:

- produced the report without explicit route selection (shared-workflow mode with coincidental structure match)
- has background-first drift where a background section breaks the judgment flow immediately after the executive summary
- does not name route-specific structural elements (shortlist, comparison framework, reversal conditions)
- has key inferences without specific source attribution
- does not explicitly state why the option set is complete (even when obvious)

## Why this case exists

Existing constrained-choice evals cover:

- `evals/comparative-distillation/api-supplier-selection-gpt-vs-minimax-comparative-distillation.md` — provider selection quality
- `evals/comparative-distillation/sea-market-entry-gpt-vs-minimax-comparative-distillation.md` — market entry as constrained choice
- `evals/templates/decision-utility-rubric.md` — decision utility scoring

None of these cover:

- **Route not activated at all** (structure emerges by coincidence, not design)
- **Background-first drift in a constrained-choice task** (judgment flow broken immediately after summary)
- **Implicit structure without explicit route labels** (route terms not used as structural markers)

This case is also the first **non-listed-company** eval in the cases/ directory, expanding coverage to the constrained-choice route family.

## Suggested intervention target

This case should push changes primarily at:

- `SKILL.md` — strengthen the routing step to require explicit route selection before evidence collection; "proceed without route selection" should be a flagged exception, not the default
- `ROUTING-MATRIX.md` — add a constrained-choice route hard-fail condition: "executive summary followed by background section before decision architecture" (background-first drift)
- `references/option-selection-and-shortlist-discipline.md` — add guidance for implicit-binary cases where the shortlist is obvious but should still be explicitly stated
- `checklists/option-selection-final-audit.md` — add check: "background-first drift: any background section immediately after judgment that breaks the decision flow"
- `checklists/final-audit.md` — add non-blocker: "route-specific labels are visible as structural elements, not just implicit in content"

These are medium priority — the core quality of the report is high, but the process gap (route not activated) is a structural risk for future reports.

## Reviewer checklist

- Was the route explicitly selected before evidence collection?
- Did the executive summary flow directly into decision architecture, or was it interrupted by background?
- Are route-specific labels (shortlist, comparison framework, reversal conditions) visible as structural markers?
- Is the shortlist construction explicit, even for obvious binary choices?
- Are all key inferences attributed to specific sources?

## Suggested scoring

- **Full pass**: route explicitly activated, execution contract committed, no background-first drift, explicit shortlist, consistent source granularity
- **Partial**: structure matches constrained-choice but route was not explicitly activated; some background-first drift; labels implicit rather than explicit (this case's level)
- **Fail**: structure does not match constrained-choice; no prediction or ranking; hard-fail triggered

## Related evals

- `evals/templates/decision-utility-rubric.md` — decision utility scoring framework
- `evals/comparative-distillation/api-supplier-selection-gpt-vs-minimax-comparative-distillation.md` — provider selection as constrained choice
- `evals/meta/rule-activation-and-execution-discipline.md` — distinguishes missing-rule vs missing-trigger vs execution-failure (this case: missing-trigger, the route existed but was never activated)
