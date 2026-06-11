# Eval: Content Platform Selection — Constrained Choice Compounded Fail Case

## Goal

Test whether a constrained-choice / option-selection report with strong decision architecture (ranking by team type, 5-variable framework, scenario reversal conditions, phased action plan) can still **fail strict delivery** when all three common fail conditions compound simultaneously:

- **body-level source traceability absent** — zero `[Sxx]` inline citations across the entire report body; source register exists but is completely disconnected from body claims
- **numeric role labels entirely absent** — MAU/DAU, GMV, production costs, cold-start traffic, star weights, revenue thresholds all lack observed/proxy/assumption/model-output roles; triggers constrained-choice hard-fail
- **self-assessment claims full pass while body execution has all three gaps** — audit status block reports source-traceability, quantitative-role, final-audit all ✅ despite zero body citations, noncompliant register, and absent numeric roles → process-integrity and declared-not-executed hard-fails triggered
- **front-page metadata-first drift** — audit status block and route metadata placed before the core judgment, crowding the first-screen decision signal
- **strong wording in platform comparison** — "最高/最大/最强/最成熟/最友好" used without claim-level source or qualification

This eval is based on a real report: a content creation platform selection memo (小红书 vs 视频号 vs 抖音 vs B站) that correctly activated the constrained-choice route, built team-type-specific rankings, defined 5 load-bearing variables, provided scenario reversal conditions with a 0-13 week action plan — but compounded every common delivery fail condition at once.

## Prompt

A content creation team needs to choose a primary platform. Produce a structured decision memo that:

- defines the team profile (size, budget, content type, monetization goal, compliance tolerance)
- states hard constraints and soft preferences
- builds a shortlist with 3-5 platforms and justifies why each was included
- provides a replicable comparison framework with weighted variables, scoring rules, and at least 1 worked example
- gives clear per-team-type rankings with why top option wins, why runner-up is credible, and why each rejected platform fails
- identifies ranking-reversal conditions and hidden operational burdens (audit risk, algorithm change, monetization threshold, content saturation)
- uses claim-level `[Sxx]` inline citations in every section (exec summary, variable table, ranking rationale, scenarios, action plan)
- includes a complete 7-column Source Register with DOI/URL
- labels all comparison numbers with observed/proxy/assumption/model-output roles
- places the core judgment before route metadata on the front page
- qualifies strong comparison wording with scope and source

## What this eval is testing

- whether body-level source traceability is executed at all — zero `[Sxx]` across the entire body is a hard-fail regardless of register existence
- whether numeric role labels are applied to every comparison table — constrained-choice hard-fail when absent
- whether self-assessment accurately reflects execution when multiple disciplines fail simultaneously — compounded failures make self-assessment errors more visible
- whether front-page metadata placement respects judgment-first design — audit status before thesis creates metadata-first drift
- whether strong comparison wording ("最高/最大/最强") is qualified with scope and source in a competitive ranking context
- whether aggregation is replicable when weights and variables are declared but scoring rules are invisible

## Pass criteria

A passing answer should:

1. **Execute body-level `[Sxx]` traceability throughout.**
   - every section (exec summary, variable table, ranking, scenarios, action plan) has inline `[Sxx]` or equivalent
   - source register has 7 columns including DOI/URL
   - every registered source is citable and cited

2. **Label numeric roles in all comparison tables.**
   - MAU/DAU, GMV, production cost, cold-start traffic, revenue thresholds, star weights all labeled as observed/proxy/assumption/model-output
   - no comparison table without row or column-level role labels

3. **Match self-assessment to body execution.**
   - audit status block must reflect actual gaps
   - if body has zero `[Sxx]`, source-traceability cannot be ✅
   - if comparison tables lack numeric roles, quantitative-role cannot be ✅
   - if both fail, final-audit cannot be ✅

4. **Place judgment before metadata.**
   - core conclusion should appear before route metadata and audit status on the front page
   - metadata belongs after the opening or in footnotes

5. **Qualify strong comparison wording.**
   - "最高/最大/最强/最成熟/最友好" must have scope qualifications and source references
   - exclusivity claims in a comparison context must be evidentiary, not rhetorical

## Failure signs

Mark this eval as failed if the answer does any of the following:

- body has zero `[Sxx]` or equivalent inline citations (source traceability hard-fail)
- comparison tables entirely lack numeric role labels (constrained-choice hard-fail)
- self-assessment claims full pass while source traceability and numeric roles are both absent (process-integrity hard-fail)
- audit status block or route metadata appears before the core judgment on the front page
- strong comparison wording ("最高/最大/最强") is used without scope qualification or source

## Why this eval matters

This case tests the **compounded failure** scenario — not just one discipline missing, but all three (traceability, numeric roles, self-assessment) failing simultaneously in the same report.

| Case | Route | Level | Body `[Sxx]` | Num roles | Register | Self-assessment |
|---|---|---|---|---|---|---|
| indie-dev | constrained-choice | Fail | None | None | No register | Overclaim |
| hq-city | constrained-choice | Cond→Fail | Partial | Partial | 5 of 7 cols | Overclaim |
| content (this) | constrained-choice | **Fail** | **Zero** | **None** | **6 of 7 cols, no body wiring** | **All ✅ while three disciplines fail** |

This is the most severe constrained-choice delivery fail in the eval set. It compounds every common failure mode into a single report, testing whether the skill catches each layer independently even when they co-occur.

The unique contributions:
- **Zero body `[Sxx]` with register existing but completely disconnected** — a source register that cannot be traced from any body claim. Compared to indie-dev (no register at all) and hq-city (register partially compliant), this tests a different failure: register exists as infrastructure but is non-functional.
- **Three disciplines fail simultaneously** — source traceability, numeric roles, AND self-assessment. Tests whether process-integrity gates fire when multiple failures compound.
- **Front-page metadata-first drift in constrained-choice** — extends the pattern from competitive-positioning cases.
- **Strong wording in platform comparison** — "最高/最大/最强" in a ranking context has different failure characteristics than "唯一/全球第一" in competitive-positioning (less about exclusivity, more about unqualified superlatives).

## Current rule verdict

The current rules should catch this as **fail**:

- body-level source traceability hard-fail: zero `[Sxx]` across entire body
- constrained-choice numeric role hard-fail: no role labels on any comparison table
- source register 7-column hard-fail: DOI/URL missing
- process-integrity hard-fail: self-assessment ✅ while body has multiple gaps
- declared-not-executed hard-fail: source-traceability and quantitative-role declared but not executed

This case guards against **compounded failure masking** — when multiple disciplines fail simultaneously, each individual gap might look small, but their intersection creates a non-deliverable artifact.

## Related evals

- `evals/cases/indie-dev-constrained-choice-delivery-fail-case.md` — same route, fail level with no source register and no numeric roles
- `evals/cases/ai-startup-hq-constrained-choice-register-compliance-case.md` — same route, partial compliance with format gaps
- `evals/cases/pkm-constrained-choice-quantitative-role-gap-case.md` — same route, conditional pass with quantitative role and register gaps
- `evals/cases/byd-competitive-positioning-traceability-hard-fail-case.md` — same body traceability absence pattern, different route
- `evals/cases/bytedance-competitive-positioning-source-mapping-case.md` — same source register disconnected from body, different route

## Reviewer checklist

- Does the body have any `[Sxx]` or equivalent inline citations? (zero = immediate hard-fail)
- Do comparison tables have numeric role labels? (none = immediate hard-fail)
- Does self-assessment match body execution? (all ✅ with gaps = process-integrity hard-fail)
- Is the core judgment visible before route metadata on the front page?
- Are strong comparison words ("最高/最大/最强") qualified with scope and source?
- Is the aggregation method replicable (scoring rules, worked example)?

## Suggested scoring

- **Pass**: body-level `[Sxx]` throughout, numeric roles on all tables, self-assessment honest, judgment-first front page, strong wording qualified, aggregation replicable
- **Conditional pass**: decision architecture correct, ranking clear, reversal conditions present, but body `[Sxx]` partial (not every section), numeric roles exist but not at row/column level, self-assessment slightly optimistic — no hard-fail triggered
- **Fail**: zero body `[Sxx]` (hard-fail), or no numeric role labels (hard-fail), or self-assessment claims all ✅ while execution has gaps (process-integrity hard-fail), or all three compounding
