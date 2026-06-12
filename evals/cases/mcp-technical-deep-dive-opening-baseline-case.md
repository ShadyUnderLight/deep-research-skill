# Eval: MCP Protocol Technical Deep-Dive — Opening Baseline Integrity Case

## Goal

Test whether a Technical Deep-dive / Architecture Analysis report with strong technical content can still **fail delivery** when its front page:

- **lacks audience definition** — the report does not state who it is for (security engineer, protocol designer, platform architect), leaving readers to self-select
- **lacks decision scenario** — the report describes protocol capabilities and risks, but does not frame the analysis as supporting a specific engineering decision (adopt, defer, deploy with controls), leaving the report as a survey rather than a decision-support artifact
- **has an inconsistent technical baseline** — the report's stated coverage/assessment date is not reconciled with the timeline of its referenced sources (e.g., coverage date "2025-06-11" but sources cite spec version 2025-11-25 and roadmap 2026-03-05), making the "current state" anchor ambiguous
- **does not separate stable baseline from forward-looking material** — roadmap items, experimental extensions, and community proposals are discussed alongside current specification capabilities without distinguishing their temporal status

This eval is based on a real failure mode observed in MCP protocol deep-dive reports: technically accurate content undermined by an opening that does not anchor the reader in the report's temporal and decision context.

## Prompt

Analyze the MCP protocol's architecture, core mechanisms, capability boundaries, and security risks. Produce a structured technical deep-dive report that:

- explains core mechanisms (participant model, transport layer, lifecycle, primitive system)
- identifies fundamental constraints and non-goals
- compares the protocol to alternatives (OpenAI Function Calling, Google A2A) with load-bearing comparison dimensions
- evaluates the roadmap with clear separation of shipped / announced / roadmap priority / speculative
- includes counter-evidence (complexity, security model limitations, deprecation risk)
- provides actionable judgments for practitioners
- uses claim-level source traceability with a complete 7-column Source Register
- opens with a clear audience definition, decision scenario, and technical baseline block as described in `references/report-template.md` §Technical deep-dive opening

## What this eval is testing

- whether the report's opening block defines **audience** (who should read this) and **decision scenario** (what decision does this report support) — without these, the report risks being a general technical survey
- whether the report's **technical baseline** is explicit: report date, stable specification version, latest verification date, and forward-looking boundary
- whether the **source timeline** is internally consistent with the stated coverage window — if the coverage date is 2025-06-11 but sources cite a 2025-11-25 spec, the temporal anchor is broken
- whether **stable baseline vs. forward-looking material** are distinguished: current specification features vs. roadmap priorities vs. experimental extensions vs. community proposals
- whether the self-assessment audit block honestly reflects these baseline disciplines

## Pass criteria

A passing answer should:

1. **Define audience and decision scenario in the opening.**
   - explicitly state who the report is for (e.g., security engineers, protocol designers, platform architects)
   - explicitly state what decision the report supports (e.g., adopt MCP, deploy with controls, monitor and wait)
   - these should be visible in the executive summary or front-page block, not buried in a methodology note

2. **Set an explicit technical baseline.**
   - report date: the date the analysis was performed or finalized
   - stable version / current specification: which spec version is treated as "current state"
   - latest verification date: when the sources were last checked
   - forward-looking boundary: which content is roadmap, experimental, or prospective

3. **Maintain source timeline consistency.**
   - the report's coverage date must be consistent with the sources it cites
   - no source dated after the coverage date should be used as a "current state" reference
   - if sources span a date range, the coverage window must be explicit

4. **Separate stable baseline from forward-looking material.**
   - current specification capabilities are clearly identified as "current stable"
   - roadmap items, experimental extensions, and community proposals are labeled with their temporal status
   - the reader can distinguish "available now" from "planned" from "speculative"

5. **Keep self-assessment honest.**
   - audit status must reflect actual gaps in baseline definition, timeline consistency, or forward-looking separation

## Failure signs

Mark this eval as failed if the answer does any of the following:

- the report's front page does not explicitly state the target audience or decision scenario
- the report has no technical baseline block (report date, stable version, forward-looking boundary)
- the coverage date in the report metadata contradicts the source timeline (e.g., coverage date 2025-06-11 but primary source is a spec from 2025-11-25)
- stable baseline capabilities and forward-looking/roadmap content are mixed without temporal labels — the reader cannot tell what is currently available vs. planned vs. speculative
- self-assessment claims full pass on technical-deep-dive disciplines but baseline definition, timeline consistency, or forward-looking labeling have gaps

## Why this eval matters

This case adds a **technical opening baseline** failure mode not yet covered by existing technical-deep-dive cases:

| Case | Route | Level | Core failure |
|------|-------|-------|-------------|
| MCP timeline/roadmap (existing) | technical-deep-dive | Fail | Timeline inconsistency + roadmap state not separated + route conflict check absent |
| CPO inline citation | technical-deep-dive | Conditional pass | Body citations absent, vendor claims lack caveats |
| K8s vs Swarm | technical-deep-dive | Conditional pass | Self-assessment overconfident, benchmark method missing |
| AI Traffic Police | technical-deep-dive | Conditional pass | Non-standard inline citations, announced vs shipped unlabeled |
| **MCP opening baseline (this)** | technical-deep-dive | **Fail** | **Opening lacks audience, decision scenario, and version baseline** |

The existing `mcp-technical-deep-dive-timeline-roadmap-case.md` tests timeline integrity (do the dates match?) and roadmap state separation (are roadmap items commitment-labeled?). This case tests the **opening contract** — the front page's job to frame the report's purpose, audience, and temporal anchor for the reader.

These are distinct failures:
- Timeline integrity: "Is the report's evidence timeline internally consistent?"
- Opening baseline: "Does the report's front page tell the reader who this is for, what decision it supports, and which version/snapshot this analysis is anchored to?"

A technically strong report with good timeline consistency can still fail on opening baseline if it starts with a generic technical survey opening instead of a decision-framed, audience-aware, version-anchored opening.

## Current rule verdict

The current rules should catch this as **fail**:

- technical-analysis audit: opening baseline checks (audience, decision scenario, version baseline)
- technical-analysis discipline: output structure requires audience and baseline definition
- final-audit: front-page readability check requires technical judgment and baseline visibility
- process-integrity hard-fail: self-assessment claims full pass while baseline and audience framing have gaps

This case guards against **opening-frame failures in technical deep-dives** — where technically accurate analysis is delivered without the front-page framing that makes it trustworthy and decision-actionable.

## Related evals

- `evals/cases/mcp-technical-deep-dive-timeline-roadmap-case.md` — same route, timeline integrity and roadmap state separation (complementary: this case tests opening baseline, the existing case tests temporal execution)
- `evals/cases/cpo-technical-deep-dive-inline-citation-absent-case.md` — same route, self-assessment overconfidence
- `evals/cases/k8s-vs-swarm-technical-deep-dive-self-assessment-case.md` — same route, self-assessment and register gaps
- `evals/cases/rag-technical-deep-dive-register-gap-case.md` — same route, register gaps
- `evals/cases/ai-traffic-police-technical-deep-dive-traceability-case.md` — same route, announced vs shipped separation

## Reviewer checklist

- Does the opening block define the target audience explicitly?
- Does the opening block state the decision scenario (what decision does this report support)?
- Is the technical baseline explicit (report date, stable version, verification date, forward-looking boundary)?
- Is the coverage date consistent with the source timeline?
- Are stable baseline capabilities separated from forward-looking/roadmap content?
- Does the self-assessment block match actual body execution on these baseline disciplines?

## Suggested scoring

- **Pass**: audience defined, decision scenario stated, technical baseline explicit, source timeline consistent, stable vs. forward-looking separated, self-assessment honest
- **Conditional pass**: technical analysis strong, core mechanisms explained, but audience/decision scenario present but thin, or baseline block present but minor date framing ambiguity — no process-integrity violation
- **Fail**: opening lacks audience or decision scenario, or no technical baseline block exists, or coverage date contradicts source timeline, or self-assessment claims pass while baseline/audience framing has gaps
