# Eval: AI Startup HQ City Selection — Constrained Choice Register Compliance and False Precision Case

## Goal

Test whether a constrained-choice / option-selection report with clear ranking, decision architecture, weights, and actionable recommendations can still be rated **conditional pass leaning toward fail** when:

- source register claims 7-column compliance but delivers only 5 columns (missing Reliability, Claims Supported) — format declared but not executed
- multiple source register entries lack IDs and cannot be body-referenced — nonexistent body-to-register wiring
- numeric role labels are absent from key comparison/score/estimate tables — scores, costs, salaries, talent counts, funding amounts lack observed/proxy/assumption/model-output roles
- aggregation/ranking method is not replicable — weights and scores exist but no scoring rules or worked examples for any dimension
- shortlist boundary is not justified — "why these 4 cities" has no visible exclusion logic
- final ranking precision is misleading — scores like 8.8 vs 8.5 presented as precise differentials without acknowledging estimation noise or the gap is within margin of error
- self-assessment claims source-traceability passed with "7-column template," but actual register is only 5 columns — triggers process-integrity and declared-not-executed hard-fails

This eval is based on a real report: an AI startup headquarters city selection memo that correctly activated the constrained-choice route, built a weighted 5-dimension framework, provided a clear ranking with reversal conditions and action steps — but failed on source register format compliance, numeric role labeling depth, aggregation replicability, and self-assessment accuracy.

## Prompt

An AI startup founder needs to choose a headquarters city among Chinese tech hubs. Produce a structured decision memo that:

- defines the company profile (stage, funding, team size, go-to-market strategy)
- states hard constraints and soft preferences
- justifies the shortlist boundary — why these cities and not others
- provides a replicable comparison framework with weighted variables, scoring rules, and at least 2 worked examples
- gives a clear ranking with why top option wins, why runner-up is credible, and why each rejected option fails
- identifies ranking-reversal conditions and hidden operational burdens
- uses claim-level source traceability with a complete 7-column Source Register (ID, Source Name, Type, Date, DOI/URL, Reliability, Claims Supported)
- ensures every registered source has an ID and is citable via body `[Sxx]`
- labels all load-bearing numbers with observed/proxy/assumption/model-output roles
- states ranking confidence and acknowledges when score differentials are within estimation noise

## What this eval is testing

- whether source register format compliance is executed at the detail level, not just declared in metadata — "7 columns" must actually be 7 columns
- whether every registered source has an ID that enables body-to-register wiring
- whether numeric role labels cover all key comparison/score/estimate tables at row or column level, not just a total table footnote
- whether the aggregation/ranking method is replicable — scoring rules (how each city scores on each dimension) must be visible, not just the final weighted scores
- whether the shortlist boundary is justified — constrained-choice requires explaining why these options were selected and what was excluded
- whether false precision is avoided — scores like 8.8 vs 8.5 must acknowledge whether the gap is within estimation noise or meaningful
- whether process-integrity and declared-not-executed gates trigger when format compliance or role labeling is incomplete

## Pass criteria

A passing answer should:

1. **Deliver a format-compliant 7-column Source Register.**
   - exactly 7 columns: ID, Source Name, Type, Date, DOI/URL, Reliability, Claims Supported
   - every entry has a unique ID that can be referenced via `[Sxx]` in body
   - register inflation below 25%

2. **Label numeric roles at the row/column level in all comparison/score/estimate tables.**
   - scores are labeled as model output
   - costs, salaries, funding amounts labeled as observed (if disclosed), proxy (if third-party tracked), or assumption (if modeled)
   - not just a single table footnote — each key number or column must have a role label

3. **Make aggregation replicable.**
   - show scoring rules for each dimension (how a city gets a 7 vs 9 on policy support)
   - provide at least 2 worked examples tracing one city's score through the method
   - reader can independently verify the ranking

4. **Justify the shortlist boundary.**
   - explain why these particular cities were selected
   - name excluded alternatives and the exclusion criteria
   - the reader can assess whether the shortlist is complete

5. **Avoid false precision in final ranking.**
   - if scores are close (e.g., <0.5 apart on a 10-point scale), acknowledge the gap is within estimation noise
   - describe ranking as conditional rather than absolute when the margin is small
   - do not let precise-looking scores create unwarranted confidence

6. **Keep self-assessment honest.**
   - audit status block must match actual execution
   - source-traceability cannot claim pass if register is noncompliant
   - declared-not-executed gate must flag any gap between declared discipline and body execution

## Failure signs

Mark this eval as failed if the answer does any of the following:

- source register claims 7 columns but delivers fewer (format compliance failure)
- any registered source lacks an ID or cannot be body-referenced
- numeric role labels are absent from any key comparison/score/estimate table
- aggregation method is not replicable — no scoring rules or worked examples
- shortlist boundary is not justified — reader cannot tell why these options were selected
- final ranking presents close scores as precise differentials without acknowledging estimation noise
- self-assessment claims pass on source-traceability while register is noncompliant (process-integrity hard-fail)
- declared numeric-role or source-traceability discipline is not executed in body (declared-not-executed hard-fail)

## Why this eval matters

This case captures a distinct failure level within the constrained-choice route that is different from the existing cases:

| Case | Route | Level | Core failure |
|---|---|---|---|
| indie-game | constrained-choice | Conditional pass | Quant role missing + body citations absent |
| pkm | constrained-choice | Conditional pass | Quant role + source register + aggregation gaps |
| indie-dev | constrained-choice | Fail | No source register + no numeric roles + shortlist boundary missing |
| hq-city (this) | constrained-choice | **Conditional pass → fail** | **Register claims compliance but fails format + entries lack IDs + false precision + aggregation not replicable** |

The unique contributions of this case:

- **Source register format theater** — the register exists and looks structured (5 columns), but claims 7-column compliance. This is harder to catch than "no register at all" because the infrastructure is partially present. The failure is in the gap between declaration and execution.
- **Source entries without IDs** — a source register that has entries that cannot be body-referenced. This is a novel failure: the register exists but part of it is structurally uncitable.
- **False precision in ranking scores** — 8.8 vs 8.5 implies a precision that the underlying evidence cannot support. This is a decision-utility hazard: precise-looking scores from a non-replicable method create pseudo-confidence.
- **Rating straddles the boundary** — "条件通过偏不通过" makes this a useful calibration case between conditional-pass and fail levels.

Without this eval, the skill could produce reports with partially compliant infrastructure that looks good on metadata review but fails on execution detail — the hardest failure mode to catch in automated or checklist-based review.

## Current rule verdict

The current rules should catch this as **fail**:

- source register 7-column hard-fail: register has 5 columns, not 7
- source traceability hard-fail: entries without IDs cannot be body-referenced
- constrained-choice numeric role hard-fail: key comparison/estimate tables lack role labels
- process-integrity hard-fail: self-assessment claims compliant register while actual format is noncompliant
- declared-not-executed hard-fail: numeric roles and source-traceability declared but not fully executed

This case guards against **compliance theater at the infrastructure level** — partially present infrastructure that looks compliant on metadata but fails on detail.

## Related evals

- `evals/cases/indie-dev-constrained-choice-delivery-fail-case.md` — same route, fail level with no source register and no numeric roles
- `evals/cases/pkm-constrained-choice-quantitative-role-gap-case.md` — same route, conditional pass with source register format gaps
- `evals/cases/indie-game-constrained-choice-quantitative-role-case.md` — same route, same numeric role hard-fail
- `evals/cases/creator-platform-constrained-choice-aggregation-logic-gap-case.md` — same route, aggregation not replicable
- `evals/cases/bytedance-competitive-positioning-source-mapping-case.md` — same compliance-theater pattern (infrastructure present but incorrectly wired), different route

## Reviewer checklist

- Does the Source Register actually have 7 columns (not fewer)?
- Does every registered entry have a unique ID usable as body `[Sxx]`?
- Are numeric role labels present at row/column level in all comparison/score/estimate tables?
- Is the aggregation method replicable (scoring rules + worked examples)?
- Is the shortlist boundary justified (why these options, what was excluded)?
- Does the final ranking acknowledge estimation noise for close scores?
- Does self-assessment match actual body execution?

## Suggested scoring

- **Pass**: 7-column compliant register with all entries ID'd, numeric role labels at row/column level, aggregation replicable with worked examples, shortlist boundary justified, false precision avoided, self-assessment honest
- **Conditional pass**: decision architecture correct, ranking clear, reversal conditions present, but register format has minor gaps (6 instead of 7 columns, or some entries lack IDs), or numeric role labels exist but not at row/column level, or aggregation described but not fully replicable — no process-integrity violation
- **Fail**: register claims 7-column compliance but delivers fewer (format theater), or entries without IDs making body wiring impossible, or numeric role labels entirely absent from key tables (hard-fail), or aggregation not replicable, or false precision in final ranking, or process-integrity/declared-not-executed hard-fail triggered
