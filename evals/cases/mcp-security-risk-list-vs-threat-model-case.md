# Eval: MCP Protocol Security Analysis — Risk List vs. Threat Model Case

## Goal

Test whether a security-sensitive Technical Deep-dive report can be distinguished by output structure:

- **Negative example:** outputs a risk list — each risk explained individually (what it is, how it works, why it matters) but no cross-risk prioritization, no asset/attacker/trust-boundary framing, no engineering controls tiering, no detection signals.
- **Positive example:** outputs a threat model with assets, trust boundaries, threat actors, attack tree, risk priority matrix (likelihood × impact), engineering controls (prevent/detect/respond), detection signals, and short/medium/long-term roadmap.

The core question: does the report structure resemble a **security architecture review** or a **risk explanation glossary**?

This eval is motivated by comparative analysis showing that GPT's MCP deep-dive report organized its security section as an engineering-review-ready threat model, while the default technical-analysis discipline produces well-explained risks without transforming them into decision-support materials.

## Prompt

Analyze the MCP (Model Context Protocol) protocol's security architecture. Produce a structured technical deep-dive report that covers:

- protocol-level security mechanisms (transport security, authentication, authorization, session management)
- known vulnerability classes (Confused Deputy, Token Passthrough, SSRF, Session Hijacking, local server compromise)
- trust model between Host, Client, Server, and remote endpoints
- current security limitations and non-goals
- recommendations for practitioners deploying MCP

Use the technical deep-dive route. Label all claims with [CONF] / [INFER] / [UNKN]. Use claim-level source traceability with a complete 7-column Source Register.

## What this eval is testing

- whether the report distinguishes **risk list** (item-by-item explanation) from **threat model** (assets, trust boundaries, threat actors, risk prioritization, engineering controls, detection signals)
- whether risks are **prioritized** (likelihood × impact) rather than equal-weighted
- whether engineering controls are **tiered** (prevent / detect / respond or short / medium / long-term)
- whether **detection/monitoring signals** are specified (concrete metrics, thresholds, data sources) rather than "should monitor"
- whether the report differentiates **protocol design risks, implementation vulnerabilities, deployment misconfigurations, and supply chain risks**

## Pass criteria

A passing answer should:

1. **Define assets and trust boundaries.**
   - Identify what is being protected (credentials, tokens, session state, local resources, remote APIs)
   - Draw trust boundaries (host-client, client-server, local process, remote HTTP, registry)
   - Explain the trust assumptions that underlie the security model

2. **Prioritize risks, not just list them.**
   - Use a risk priority matrix with likelihood, impact, and priority columns
   - Explain the judgment basis for each priority rating
   - Identify which risks are urgent vs. acceptable vs. monitored

3. **Tier engineering controls.**
   - Separate controls into prevention, detection, and response (or short/medium/long-term)
   - For each control, state whether it is readily available, requires customization, or is conceptual
   - Mention limitations of each control

4. **Specify detection signals.**
   - Recommend concrete monitoring metrics, data sources, and thresholds
   - Not just "monitor for anomalies" — specify what to monitor, where, and at what cadence

5. **Differentiate risk types.**
   - Distinguish protocol design risks (inherent) from implementation vulnerabilities (fixable), deployment misconfigurations (operational), and supply chain risks (third-party)

## Failure signs

Mark this eval as failed if the answer does any of the following:

- the security section is organized as a flat list of risks with equal-weight treatment
- no risk priority matrix or equivalent prioritization (likelihood × impact or similar) is present
- engineering controls are listed without tiering (all controls presented at the same level)
- no detection/monitoring signals are specified (only generic "should monitor" language)
- the report does not differentiate among protocol design risks, implementation bugs, deployment issues, and supply chain risks
- no assets or trust boundaries are defined

## Why this eval matters

This case adds a **security-specific output structure** failure mode not yet covered by existing technical-deep-dive evals:

| Case | Route | Core failure |
|------|-------|-------------|
| CPO inline citation | technical-deep-dive | Body citations absent |
| K8s vs Swarm | technical-deep-dive | Self-assessment, register gaps |
| MCP timeline/roadmap | technical-deep-dive | Timeline inconsistency + roadmap state |
| **MCP security (this)** | technical-deep-dive | **Risk list vs. threat model gap** |

Without this eval, the skill could produce technically accurate risk descriptions that fail to transform into engineering-review-ready threat model output — the very gap identified in the GPT comparative analysis.

## Current rule verdict

The current rules (after issue #244) should catch this as **fail** when the security deep-dive checklist (`checklists/technical-analysis-audit.md` §Security deep-dive) is activated:

- checklist: assets/trust boundaries not defined → fail
- checklist: no risk prioritization (equal-weight list) → fail
- checklist: no preventive/detection/response tiering → fail
- checklist: no detection signals specified → fail
- checklist (non-blocking): no risk-type differentiation → warn

## Related evals

- `evals/cases/mcp-technical-deep-dive-timeline-roadmap-case.md` — same protocol, different failure mode (timeline + roadmap state)
- `evals/cases/cpo-technical-deep-dive-inline-citation-absent-case.md` — same route, self-assessment overconfidence
- `evals/cases/k8s-vs-swarm-technical-deep-dive-self-assessment-case.md` — same route, self-assessment and register gaps

## Reviewer checklist

- Does the report define assets and trust boundaries?
- Are risks prioritized (likelihood × impact), not equal-weighted?
- Are controls tiered (prevent/detect/respond or short/medium/long)?
- Are detection signals concrete (metrics, thresholds, data sources)?
- Are risk types differentiated (protocol design vs implement vs deploy vs supply chain)?
- Would a security engineer find this report useful as an architecture review input?

## Suggested scoring

- **Pass**: assets + trust boundaries defined, risk priority matrix present, controls tiered, detection signals concrete, risk types differentiated
- **Conditional pass**: assets/boundaries present, risk prioritization partial (e.g., prioritized list without matrix), controls tiered but thin, detection signals generic, risk type differentiation incomplete
- **Fail**: flat risk list, no assets or trust boundaries, no prioritization, no control tiering, no detection signals, no risk-type differentiation
