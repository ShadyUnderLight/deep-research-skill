# Eval: World Cup Best Third-Place Rule — Regulatory Route Self-Declaration Mismatch Case

## Goal

Test whether a report whose actual content is regulatory/policy impact analysis (analyzing how a rule combination changes behavioral incentives) can **fail strict delivery** when:

- **route self-declaration mismatches actual content** — report declares `Shared-workflow` but the core burden is regulatory/policy impact analysis of tournament rules; the declared route does not match the artifact's natural reading
- **correct route (regulatory) contract is not satisfied** — missing: current regulatory snapshot, pending policy/enforcement reality, direct vs indirect impact separation, three-scenario structure, monitoring signals
- **body-level source traceability absent** — no `[Sxx]` inline citations; source list is not 7-column Source Register
- **self-assessment overconfident** — claims workflow/final audit ✅ while body execution has no claim-level citations and route contract is incomplete
- **process-integrity and declared-not-executed hard-fails triggered**

This eval is based on a real report: a World Cup 2026 best third-place rule behavioral impact analysis that correctly identified the core question ("will teams be more conservative or more aggressive?"), used multi-disciplinary evidence (history, game theory, statistics, expert commentary, counter-evidence), and delivered a nuanced conclusion — but self-declared as Shared-workflow when the natural route is regulatory/policy impact analysis, and satisfied neither the declared nor the correct route's artifact contract.

## Prompt

Analyze how the 2026 World Cup "best third-place" qualification rule affects team behavior in the final group stage matches.

## What this eval is testing

- whether the model selects the correct route by content burden rather than topic domain — analyzing how a rule system changes behavior is regulatory/policy impact analysis, not shared-workflow
- whether the regulatory route contract is executed when the report is regulatory in nature (current snapshot, enforcement reality, impact separation, scenarios, monitoring)
- whether body-level source traceability is present
- whether self-assessment accuracy reflects route selection quality and contract execution completeness
- whether process-integrity and declared-not-executed gates fire when route selection is incorrect and body execution is incomplete

## Pass criteria

A passing answer should:

1. **Select the correct route by content burden.** Analyze tournament rules → regulatory/policy impact analysis. Not shared-workflow, not academic-review (even if academic evidence is used), not market-outlook.

2. **Satisfy the regulatory route artifact contract.** Must include: current regulatory snapshot (the rule combination as enacted), pending/not-applicable policy declaration, enforcement reality (FIFA/judgment, simultaneous kickoff constraints, discipline), direct impact (rule → behavior) vs indirect impact (tactical evolution, spectator experience), structured scenarios (at minimum baseline and variation), and monitoring signals for future tournaments.

3. **Execute body-level `[Sxx]` traceability.** Every load-bearing factual claim and quantitative estimate must have an inline citation.

4. **Keep self-assessment honest.** Audit status must reflect route accuracy and contract completion.

## Failure signs

Mark this eval as failed if the answer does any of the following:

- declares a route that does not match the content burden (e.g., Shared-workflow for regulatory analysis)
- fails to satisfy the correct route's artifact contract (regulatory: missing snapshot, enforcement, impact separation, scenarios, monitoring)
- body has no `[Sxx]` inline citations (source traceability hard-fail)
- self-assessment claims all ✅ while route selection is incorrect AND body execution is incomplete (process-integrity hard-fail)
- declared-not-executed gate fires on claimed disciplines

## Why this eval matters

This case adds a **route self-declaration accuracy** dimension not yet covered by existing cases. Previous route activation cases test whether the report matches the declared route. This case tests the reverse: whether the report's burden matches what it should have declared.

| Case | Issue | Direction |
|---|---|---|
| Tiktok AI route inflation | Declared tech-dive, drifts into market-outlook | Declared route vs actual burden drift |
| World Cup wrong route | Declared market-outlook, actual constrained-choice | Wrong primary route |
| World Cup rule (this) | **Declares Shared-workflow, actual regulatory** | **Route self-declaration mismatch** |

The unique contributions:

- **Route self-declaration mismatch** — the report declares `Shared-workflow` when the core burden (analyzing how a rule combination changes behavioral incentives) fits `regulatory/policy impact analysis`. This is a meta-level failure: the model chose a generic catch-all route instead of recognizing the specific route that matches the content burden. Shared-workflow is for cross-cutting process tasks, not for domain-specific policy analysis.
- **Correct route contract not satisfied as a secondary failure** — even if the route declaration could be corrected, the regulatory contract (snapshot, enforcement, scenarios, monitoring) is not executed. The report has strong content but wrong artifact shape.

Without this eval, the skill could produce analytically strong reports that fail on route accuracy — a failure that affects every downstream discipline (checklist activation, audit block structure, required sections).

## Current rule verdict

- Route activation hard-fail: self-declared route does not match content burden
- Regulatory contract hard-fail: missing snapshot, enforcement, impact separation, scenarios, monitoring
- Source traceability hard-fail: no body `[Sxx]`
- Process-integrity hard-fail: self-assessment overclaim with route mismatch

## Related evals

- `evals/cases/tiktok-ai-technical-deep-dive-route-inflation-case.md` — declared route vs actual burden drift
- `evals/cases/world-cup-constrained-choice-wrong-route-case.md` — wrong primary route selection
- `evals/cases/eu-dma-regulatory-scenario-probability-and-action-tiering-case.md` — same regulatory route, different failure pattern

## Reviewer checklist

- Does the self-declared route match the content burden? (regulatory/policy analysis ≠ shared-workflow)
- Is the correct route's artifact contract satisfied?
- Does the body have `[Sxx]` inline citations?
- Does self-assessment reflect route accuracy?
- Does the audit block truthfully assess route contract execution?

## Suggested scoring

- **Pass**: route self-declaration matches content burden, artifact contract satisfied, body `[Sxx]` present, self-assessment honest
- **Conditional pass**: content analysis strong, nuanced conclusion, counter-evidence present, but route selection inaccurate but close (declares a sibling route), or contract partially satisfied, or traceability thin — no process-integrity hard-fail
- **Fail**: route self-declaration significantly mismatches content burden (e.g., Shared-workflow for regulatory analysis), AND correct route contract not satisfied, AND body traceability absent, AND self-assessment overclaims
