# Eval: EU DMA Regulatory — Scenario Probability Basis and Action Tiering Case

## Goal

Test whether a Regulatory / Policy Impact Analysis report with strong structural execution (regulatory snapshot, business impact, scenarios, monitoring signals, uncertainty register) can still **fail strict delivery** when:

- scenario probabilities are stated as exact percentages (`~25% / ~50% / ~25%`) without any source basis, assumption chain, or method disclosure — the probabilities look precise but are not auditable
- direct vs indirect impact is not explicitly labeled — reader must infer which impacts follow directly from regulation vs mediated through market response
- action implications are not tiered by urgency — no "must comply now / prepare / monitor" structure reduces regulatory actionability
- secondary route (Market Outlook) is declared but its hard-fail conditions are not verified
- self-assessment overclaims pass on source-traceability, final-audit, and secondary hard-fail while body execution has gaps
- `[INFER]` claims lack reasoning chains linking to specific register entries

This eval is based on a real report: an EU Digital Markets Act impact analysis memo that correctly activated the regulatory route, provided a current regulatory snapshot, mapped enforcement reality, built three scenarios with counter-evidence, and had a structured uncertainty register — but failed on scenario probability auditability, impact tiering, secondary route verification, and self-assessment accuracy.

## Prompt

Analyze how the EU Digital Markets Act (DMA) affects large-platform AI feature distribution. Produce a structured regulatory impact analysis report that:

- provides a current regulatory snapshot (articles, enforcement, gatekeeper status)
- separates pending/under-review regulatory items from settled rules
- explicitly labels direct regulatory impacts vs indirect/market-mediated impacts
- defines scenarios with grounded probability ranges and visible assumption chains
- provides action implications tiered by urgency (must comply now / prepare / monitor)
- includes counter-evidence that adjusts the analysis
- uses claim-level source traceability with a complete 7-column Source Register
- distinguishes official regulatory sources from legal analysis, media reporting, and industry inference
- if a secondary route (e.g., Market Outlook) is declared, runs and reports its hard-fail verification
- labels numeric roles (observed / proxy / assumption / model output) for all key figures including probabilities

## What this eval is testing

- whether scenario probabilities are grounded in visible assumptions or source basis — exact percentages without method create false precision
- whether direct vs indirect impacts are explicitly separated — regulatory analysis loses decision value when the reader must disentangle what the regulation directly causes vs what depends on market response
- whether action implications are tiered by urgency — regulatory reports should distinguish "must do now" from "prepare for" from "monitor," not present all implications at the same level
- whether secondary route hard-fail verification is actually executed when declared, not just named
- whether self-assessment accuracy matches body execution for regulatory-specific disciplines
- whether `[INFER]` claims include reasoning chains connecting to specific sources
- whether numeric role labels cover probabilities, compliance costs, fine estimates, and other regulatory-specific numbers

## Pass criteria

A passing answer should:

1. **Ground scenario probabilities in visible assumptions.**
   - if probabilities are assigned (e.g., 25/50/25), state what evidence or reasoning each probability is based on
   - if probabilities cannot be sourced, downgrade to qualitative ranges (low/medium/high) or directional statements
   - do not let exact percentages create false precision

2. **Separate direct vs indirect impact explicitly.**
   - label each major impact as direct (follows from regulatory text or enforcement) or indirect (mediated by market response, platform strategy, or third-party adaptation)
   - reader can trace which regulatory provisions cause which effects
   - do not mix direct and indirect impacts in the same paragraph without separation

3. **Tier action implications by urgency.**
   - must comply now: binding requirements with deadlines
   - prepare: expected changes in the next 6-18 months
   - monitor: uncertainties, appeals, legislative reviews that could change the landscape
   - each tier has specific stakeholder guidance

4. **Execute declared secondary route verification.**
   - if a secondary route (Market Outlook, Technical Deep-dive) is declared, run and report its hard-fail conditions
   - do not simply state "verified" without showing the verification results

5. **Keep self-assessment honest.**
   - audit status block must match actual body execution
   - source-traceability, final-audit, and secondary route status must reflect actual gaps

6. **Provide reasoning chains for `[INFER]` claims.**
   - each `[INFER]` claim must trace to specific source evidence and state the inference logic
   - reader can assess whether the inference is reasonable

## Failure signs

Mark this eval as failed if the answer does any of the following:

- scenario probabilities are stated as exact percentages (e.g., 25/50/25) without any source basis, assumption chain, or method disclosure
- direct vs indirect impacts are mixed without explicit labeling — reader cannot tell which impacts are regulatory-direct vs market-mediated
- action implications are not tiered by urgency — all recommendations at the same level without "now/prepare/monitor" structure
- secondary route hard-fail verification is declared but not actually run
- self-assessment claims pass on disciplines where body execution has visible gaps
- `[INFER]` claims lack reasoning chains linking to specific sources
- numeric role labels are absent from key regulatory numbers (fines, compliance costs, probabilities, timeline estimates)

## Why this eval matters

This case adds a distinct regulatory-route failure mode not yet covered by existing cases:

| Case | Route | Level | Core failure |
|---|---|---|---|
| Eu AI Act | regulatory | Conditional pass | Source type label error + label inconsistency + estimated numbers lack roles |
| US Chip Export | regulatory | Conditional pass | Evidence label over-confidence + register not 7-column |
| China Data Export | regulatory | Conditional pass | Body traceability absent + secondary route unverified |
| EU DMA (this) | regulatory | **Fail (delivery)** | **Scenario probability basis missing + direct/indirect impact not separated + action tiering absent** |

The unique contributions of this case:

- **Scenario probability precision without basis** — a regulatory-specific failure: scenarios exist and probabilities are assigned, but the method is invisible. This is different from "no scenarios" (which existing cases test) — it tests false precision *within* an otherwise well-structured scenario analysis.
- **Direct vs indirect impact separation** — regulatory reports must distinguish what the regulation directly causes vs what depends on market response. Existing cases don't test this distinction.
- **Action tiering by urgency** — regulatory best practice requires "must comply now / prepare / monitor" separation. Without it, stakeholders cannot prioritize.

These three failures are regulatory-route specific and not covered by existing eval cases. They sit between "scenario structure" (present) and "decision utility" (partial) — the gap is in the translation from analysis to action.

## Current rule verdict

The current rules should catch this as **fail**:

- regulatory route scenario discipline: probabilities without source basis or method create false precision
- regulatory route action structure: no urgency tiering reduces decision utility
- secondary route hard-fail: declared but not verified
- process-integrity hard-fail: self-assessment claims pass while body execution has gaps
- source traceability: `[INFER]` claims lack reasoning chains

This case guards against **well-structured regulatory analysis that stops short of decision-ready actionability**.

## Related evals

- `evals/cases/eu-ai-act-regulatory-source-type-case.md` — same route, source type and label discipline
- `evals/cases/us-chip-export-regulatory-evidence-label-case.md` — same route, evidence label over-confidence
- `evals/cases/china-data-export-regulatory-secondary-route-case.md` — same route, secondary route verification
- `evals/cases/ai-startup-hq-constrained-choice-register-compliance-case.md` — same false precision pattern (scores without replicable method), different route

## Reviewer checklist

- Are scenario probabilities grounded in visible assumptions or source basis?
- If probabilities cannot be sourced, are they downgraded to qualitative ranges?
- Are direct vs indirect impacts explicitly labeled and separated?
- Are action implications tiered by urgency (must comply now / prepare / monitor)?
- Is the declared secondary route hard-fail verification actually executed?
- Does self-assessment match actual body execution?
- Do `[INFER]` claims include reasoning chains?
- Are numeric role labels present for key regulatory numbers?

## Suggested scoring

- **Pass**: scenario probabilities grounded in assumptions or downgraded to qualitative ranges, direct/indirect impact explicitly labeled, action tiering by urgency, secondary route verified, self-assessment honest, `[INFER]` claims traced
- **Conditional pass**: regulatory snapshot complete, scenarios present, business impact analysis strong, but scenario probabilities stated as exact percentages without method, or direct/indirect impact partially mixed, or action tiering present but not fully separated, or secondary route declared but verification summary is thin — no process-integrity violation
- **Fail**: scenario probabilities stated as exact percentages without any source basis or method (false precision), or direct/indirect impact not separated at all, or no action tiering (all implications at the same level), or secondary route hard-fail declared but not executed, or process-integrity hard-fail triggered
