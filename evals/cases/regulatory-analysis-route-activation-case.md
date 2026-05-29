# Eval: Regulatory / Policy Impact Analysis — US Export Controls on AI Chips

## Goal

Test whether the skill correctly activates the **regulatory / policy impact analysis** route for a regulatory impact assessment task, and produces a report that satisfies the regulatory analysis artifact contract.

This eval validates the new regulatory / policy impact analysis routing added in response to issue #122.

## Prompt

Analyze the impact of US export controls on AI chips (October 2023 rules and subsequent updates) on Chinese AI companies. Focus on:

- current regulatory state (what controls are in effect)
- pending/in-progress changes (proposed rules, enforcement updates)
- business impact on Chinese AI companies (direct vs indirect)
- timeline of regulatory changes
- uncertainty bounds (enforcement intensity, possible exemptions)
- scenario analysis (optimistic / base / pessimistic)
- implications for Chinese AI industry strategy

## What this eval is testing

- whether the regulatory analysis route is correctly activated (not market outlook or listed-company)
- whether the report separates current regulations from pending legislation
- whether business impact is analyzed at business level (not just described)
- whether uncertainty is explicitly bounded
- whether scenario analysis is provided
- whether the artifact contract is satisfied

## Route activation criteria

The regulatory analysis route should activate because:

- the core question is about **understanding regulatory impact on business/industry**
- the task is not about listed-company investment analysis (regulation is the primary focus, not company valuation)
- the task is not about market outlook (regulatory change is the primary driver, not market evolution)
- the task is not about market entry (regulatory environment is the primary focus, not entry sequencing)

If the report treats regulation as a section within a broader company or market analysis, the wrong route fired.

If the report makes regulatory analysis the primary structure and analyzes business impact systematically, the correct route fired.

## Pass criteria

A good answer should:

### 1. Activate the correct route
- explicitly classify this as regulatory/policy impact analysis
- not default to market outlook or listed-company research

### 2. Separate current vs pending regulations
- clearly distinguish what is currently in effect from what is proposed or in-progress
- date the regulatory snapshot
- source regulatory claims to official documents

### 3. Analyze business impact systematically
- separate direct impact (e.g., cannot sell certain chips) from indirect impact (e.g., supply chain disruption)
- quantify impact where possible with explicit assumptions
- analyze impact at business level (revenue, cost, operations, market access)

### 4. Bound uncertainty explicitly
- state uncertainty around enforcement intensity
- state uncertainty around timing of future changes
- state uncertainty around possible exemptions or workarounds
- do not give false precision on regulatory timing

### 5. Provide scenario analysis
- optimistic scenario (what if controls are relaxed?)
- base scenario (current trajectory continues)
- pessimistic scenario (what if controls tighten?)
- scenarios grounded in evidence, not speculation

### 6. Satisfy the artifact contract
The report should visibly show:
- current regulatory snapshot
- pending legislation / policy
- business impact analysis (direct vs indirect)
- timeline (enacted → transition → future changes)
- uncertainty bounds
- scenario analysis
- business/industry implications
- monitoring signals

## Failure signs

Mark this eval as failed if the answer does any of:

- activates market outlook or listed-company route instead of regulatory route
- lists regulations without analyzing business impact
- confuses regulatory text with media interpretation
- gives false precision on regulatory timing without uncertainty bounds
- ignores enforcement reality (letter-of-law vs actual enforcement)
- treats all jurisdictions as equivalent without prioritizing binding regimes
- presents regulatory risk as binary (yes/no) rather than graduated with scenarios
- produces a generic industry overview without regulatory-specific analysis

## Why this eval matters

This is a high-value regression test because it catches a common routing failure:

- the task sounds like it could be "market outlook" (industry analysis) or "listed-company research" (company impact)
- but the real question is about **understanding regulatory impact systematically**
- if the wrong route fires, the report will treat regulation as a section rather than the primary structure

If the skill cannot pass this eval, the regulatory analysis route is not yet reliable.

## Reviewer checklist

Use this quick checklist after a run:

- Did it activate the regulatory analysis route?
- Did it separate current vs pending regulations?
- Did it analyze business impact at business level?
- Did it bound uncertainty explicitly?
- Did it provide scenario analysis?
- Does the artifact contract sections appear in the report?
- Does the report look like a regulatory impact analysis, not a market overview?

## Suggested scoring

- Pass: route activation correct, impact analyzed systematically, uncertainty bounded, artifact contract satisfied
- Partial: route activation correct but analysis is shallow or uncertainty not bounded
- Fail: wrong route activated, or report treats regulation as a section rather than primary structure

---

## Related evals

- `evals/cases/cjk-pdf-validation-input-market-case.md` — contains regulatory analysis example (AI regulation framework)
- `evals/cases/startup-evaluation-route-activation-case.md` — tests private company routing

## Related references

- `references/current-state-verification.md` — for regulatory snapshot verification
- `references/forward-looking-discipline.md` — for regulatory change predictions
- `references/source-quality.md` — for regulatory source hierarchy
- `checklists/regulatory-analysis-audit.md` — the checklist for this route
- `ROUTING-MATRIX.md` — the route definition
