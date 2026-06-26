# Eval: Rule-system add-on activation — missing state taxonomy and intervention matrix fail case

## Goal

Test whether a report that analyzes how a rule system changes participant incentives (e.g., tournament rules, regulatory mechanism, incentive design) — but delivers only a general policy summary without state taxonomy or intervention matrix — is correctly flagged as incomplete under the rule-system / tournament-mechanism add-on.

This eval verifies that the add-on described in `references/rule-system-and-mechanism-add-on.md` is practically enforceable: a report analyzing incentive effects of rules cannot full-pass if it omits state taxonomy and intervention matrix.

## Prompt

Analyze how the 2026 World Cup "best third-place" qualification rule affects team behavior in the final group stage matches. Produce a structured regulatory analysis report that:

- explains the current rule mechanism (how best third-place teams are determined)
- discusses whether teams become more conservative or more aggressive in final matches
- provides historical examples (1986, 1990, 1994 World Cups with similar rules)
- discusses policy implications for FIFA (fairness, spectator experience)
- includes a scenario analysis (if Group A plays before Group B, etc.)
- cites official FIFA regulations and historical match data

**Do NOT** include:
- a state taxonomy classifying team situations (must-win, draw-enough, already-qualified, already-eliminated, information-advantage)
- an intervention matrix comparing rule alternatives (e.g., simultaneous kickoff enforcement, revert to top-2, 16 groups of 3, cross-group synchronization)
- decision flow diagrams showing how information sets translate into strategy choices

## What this eval is testing

1. Whether the rule-system add-on activates when a report's core burden is "how rules change participant incentives"
2. Whether missing state taxonomy is correctly identified as a gap
3. Whether missing intervention matrix is correctly identified as a gap
4. Whether the report can still be graded as "conditional pass" if the policy analysis is strong but lacks the add-on output blocks
5. Whether the audit correctly distinguishes between an adequate regulatory analysis (general compliance/policy report) and an inadequate one (rule-system analysis missing the add-on blocks)

## Pass criteria

A passing answer should:

1. **Activate the rule-system add-on.** Recognize that "analyzing how tournament rules change team behavior" triggers the add-on's enablement criteria (rule system changes participant incentives).
2. **Identify missing state taxonomy.** Flag that the report lacks a classification of team situations (must-win, draw-enough, already-qualified, already-eliminated, information-advantage) with strategy space and information conditions for each state.
3. **Identify missing intervention matrix.** Flag that the report lacks a structured comparison of rule alternatives with expected improvement, side effects, implementation difficulty, monitoring metrics, and reversal conditions.
4. **Apply the correct verdict.** The report should receive at minimum a conditional-pass (not full-pass) due to the add-on output block gaps, even if the regulatory analysis is otherwise solid.
5. **Reference the add-on document.** Cite `references/rule-system-and-mechanism-add-on.md` as the authority for the missing output blocks.

## Failure signs

Mark this eval as failed if the answer:

- passes the report as fully compliant without flagging the missing state taxonomy or intervention matrix
- treats the regulatory route's general artifact contract as sufficient for a rule-system/incentive analysis
- does not activate the rule-system add-on despite the core burden being "rule → incentive → behavior change"
- accepts "scenario analysis" as a substitute for state taxonomy (scenarios describe outcomes under different assumptions; state taxonomy classifies participant positions within the rule system)
- accepts "policy implications" as a substitute for intervention matrix (implications describe what might happen; intervention matrix compares what rule changes could achieve)
- does not reference the rule-system add-on document

## Why this eval matters

This eval validates that the rule-system add-on is not just documentation — it changes audit behavior. Without this eval, the add-on exists in theory but isn't tested for enforcement.

The rule-system add-on fills a gap not covered by existing evals:

| Eval | Add-on tested | What it guards |
|------|-------------|----------------|
| `control-plane-add-on-activation-case.md` | Control-plane add-on | Missing state/action/error/observability dimensions in agentic architecture comparison |
| `mcp-security-risk-list-vs-threat-model-case.md` | Security deep-dive add-on | Risk list without threat model structure (assets, trust boundaries, attack trees) |
| **This eval** | Rule-system add-on | Missing state taxonomy and intervention matrix in rule/incentive analysis |

The unique contribution: **add-on activation enforcement for a non-security, non-agentic domain**. This demonstrates the add-on pattern is generalizable beyond the technical-deep-dive route.

## Reviewer checklist

- Does the answer activate the rule-system add-on when reviewing a rule-system/incentive analysis?
- Does the answer correctly identify the missing state taxonomy?
- Does the answer correctly identify the missing intervention matrix?
- Does the answer reference `references/rule-system-and-mechanism-add-on.md` as the authority?
- Does the answer apply the correct verdict (conditional-pass or fail, not full-pass)?
- Does the answer distinguish between adequate regulatory analysis and adequate rule-system analysis?

## Suggested scoring

- **Pass**: add-on activated, state taxonomy and intervention matrix gaps identified, correct verdict applied, add-on document referenced
- **Conditional pass**: add-on referenced but only one of the two gaps identified, or verdict is conditional-pass with clear justification
- **Fail**: report accepted as fully compliant without flagging add-on gaps, or add-on never activated despite core burden being "rule → incentive → behavior"
