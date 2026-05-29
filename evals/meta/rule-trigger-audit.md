# Rule Trigger Rate Audit

Periodic audit of whether core disciplines are actually being triggered and executed across eval cases.

## Purpose

Track activation rates for the 8 core shared disciplines defined in `SKILL.md`. Identify disciplines that exist in the repo but are systematically ignored or under-triggered in practice.

## When to run this audit

- Every 10 new eval cases, or quarterly — whichever comes first
- After a major routing or checklist change
- When a discipline is suspected of being under-triggered

## Core disciplines tracked

| # | Discipline | Reference file | Checklist gate |
|---|-----------|----------------|----------------|
| 1 | Current-state verification | `references/current-state-verification.md` | `checklists/listed-company-report.md` |
| 2 | Source traceability | `references/source-traceability-and-claim-citation.md` | `checklists/source-traceability.md` |
| 3 | Forward-looking claims | `references/forward-looking-discipline.md` | `checklists/forward-looking-claims.md` |
| 4 | Quantitative role labeling | `references/quantitative-role-labeling.md` | `checklists/quantitative-role-audit.md` |
| 5 | Scope completeness | `references/scope-completeness-discipline.md` | `checklists/final-audit.md` |
| 6 | Decision utility | `references/decision-report-template.md` | `checklists/final-audit.md` |
| 7 | Delivery cleanliness | `checklists/final-audit.md` | `checklists/final-audit.md` |
| 8 | Target-language coherence | `checklists/final-audit.md` | `checklists/final-audit.md` |

## Audit template

```markdown
## Period: YYYY-MM to YYYY-MM (N cases reviewed)

### Rule activation rates

| Discipline | Applicable cases | Triggered | Rate | Status |
|-----------|------------------|-----------|------|--------|
| Current-state verification | / | / | % | |
| Source traceability | / | / | % | |
| Forward-looking claims | / | / | % | |
| Quantitative role labeling | / | / | % | |
| Scope completeness | / | / | % | |
| Decision utility | / | / | % | |
| Delivery cleanliness | / | / | % | |
| Target-language coherence | / | / | % | |

### Notes
- [Any context on why certain disciplines were under-triggered]

### Action items
- [ ] [Specific hardening or investigation needed]
```

## How to count

### Applicable cases

Count only cases where the discipline **should** have been triggered based on the task type:

- Current-state verification → listed-company, current-position, ranking, fast-moving product tasks
- Source traceability → all cases
- Forward-looking claims → cases with forecasts, estimates, roadmaps, target prices
- Quantitative role labeling → cases with load-bearing numeric claims
- Scope completeness → global, comprehensive, industry-wide scope claims
- Decision utility → cases with recommendation, selection, or judgment burden
- Delivery cleanliness → all cases
- Target-language coherence → all user-facing cases

### Triggered

A discipline is counted as "triggered" if:

1. The case eval's diagnosis shows the discipline was activated (even if execution was partial)
2. The final artifact shows visible evidence of the discipline
3. The route-activation audit confirms the discipline was attached and executed

A discipline is **not** triggered if:

1. The case eval identifies it as a missing trigger or missing rule
2. The final artifact shows no visible compliance
3. The discipline was named but not operationalized (cosmetic compliance)

## Trigger rate thresholds

| Rate | Status | Action |
|------|--------|--------|
| > 90% | ✅ Healthy | Maintain |
| 70–90% | ⚠️ Needs attention | Investigate: is the rule unclear, or is execution drifting? |
| 50–70% | 🔴 Insufficient | Consider hardening: stronger checklist gate, route attachment, or execution contract |
| < 50% | 🚫 Ineffective | Rule may be poorly defined or not actionable — redesign trigger or scope |

## Data sources

- `evals/cases/*-case.md` — case-level failure diagnoses
- `evals/comparative-distillation/*-distillation.md` — distillation findings
- `evals/meta/rule-activation-and-execution-discipline.md` — activation failure analysis
- `evals/comparative-distillation/candidate-rule-registry.md` — rule coverage status

## Related files

- `evals/meta/rule-activation-and-execution-discipline.md` — distinguishes missing rule / missing trigger / execution failure
- `evals/comparative-distillation/candidate-rule-registry.md` — tracks candidate rules and coverage
- `references/failure-taxonomy.md` — cross-family meta-failure: rule activation vs rule existence
- `checklists/route-activation-audit.md` — route-level activation checklist

## Why this audit exists

The repo has accumulated 60+ candidate rules across 11 distillation cases and 32+ case evals. Most rules are already covered by existing checklists and references (95% coverage per candidate-rule-registry.md).

The remaining gap is **execution/activation discipline** — rules exist but are not consistently triggered. This audit provides a lightweight, periodic check on whether that gap is widening or narrowing.

Without this audit, under-triggered disciplines can silently degrade report quality without anyone noticing until a major failure surfaces.
