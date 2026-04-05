# Comparative Distillation Method

Use this method when you have two reports on the same or near-identical research question and want to extract **reusable skill improvements** from their differences.

This method is especially useful when one report is a stronger reference output and the other is a weaker execution of the same task.

The goal is **not** to copy content from the stronger report.

The goal is to identify:

- structural discipline differences
- evidence-handling differences
- output-design differences
- calibration differences
- which of those differences deserve to become reusable rules, checklist gates, template changes, or evals

---

## Core rule

Do not ask: **"Which model is better?"**

Ask instead:

1. What does the stronger report do that is systematically more useful or reliable?
2. Is that difference about content knowledge, or about research and reporting discipline?
3. Can that difference be turned into a reusable, auditable rule?
4. Should the fix land in `references/`, `checklists/`, `report-template`, `SKILL.md`, or only in an eval artifact?

If the answer is still "this one just feels better," the distillation is not ready.

---

## What comparative distillation is for

Use this method to extract improvements from paired reports when you want to improve the skill's execution quality.

Good use cases:

- GPT report vs Minimax report on the same company
- stronger vs weaker report from different runs on the same prompt
- earlier vs later version of the same model's output when one shows a meaningful improvement
- two reports with similar factual inputs but different quality of traceability, calibration, structure, or decision usefulness

Do **not** use this method mainly to compare raw knowledge coverage unless the comparison reveals a stable process difference.

---

## Preconditions

Before comparing, control the inputs as much as possible.

A good comparative-distillation case should have:

- the **same research question** or nearly identical question
- roughly the **same time window**
- broadly comparable public information environment
- outputs that are similar enough in scope to compare
- preserved artifacts when possible: markdown, PDF, source register, prompt

If the two reports differ too much in scope, format, or timing, say so and reduce confidence in the distillation.

---

## What to compare

Compare reports across these fixed dimensions.

### 1. Current-state discipline

Look for:
- current snapshot before analysis
- separation of historical / current / forward-looking layers
- correct handling of latest products, listings, rankings, pricing, or current positioning
- avoidance of stale but familiar knowledge

### 2. Numerical and date discipline

Look for:
- exact figures vs default rounding
- explicit date basis
- explicit valuation basis (TTM / forward / fiscal year)
- use of ranges only when uncertainty or source disagreement justifies them
- visible handling of proxy indicators and their limitations

### 3. Source traceability and evidence weighting

Look for:
- claim-level citations, not just bibliography
- structured source register
- separation of primary, secondary, inferred, and unconfirmed claims
- reasoning chain for inferred claims
- reader ability to audit the report

### 4. Forward-looking claim discipline

Look for:
- named source for forecasts, guidance, targets, or roadmap statements
- assumptions and failure conditions
- distinction between announced, expected, rumored, and shipped
- uncertainty expressed through both labels and sourcing

### 5. Structural readability and information density

Look for:
- one insight per exec-summary bullet
- table width appropriate to information density
- no bullet walls or table walls
- structure that helps the reader absorb the report quickly
- formatting choices that improve auditability, not just appearance

### 6. Decision usefulness

Look for:
- decision frame made explicit
- 3-5 load-bearing variables identified
- trade-offs and scenario implications made clear
- bottom line sharp enough to act on
- what could change the conclusion
- practical next checks

These six dimensions are the default comparison frame. Add other dimensions only if the task truly needs them.

---

## Distillation workflow

### Step 1: Record the case

For each comparative case, capture:

- research question
- report A and report B
- which report is the stronger reference, if any
- date
- prompt(s)
- notable differences in scope or timing

### Step 2: Compare by dimension

For each of the six dimensions:

- identify what report A does
- identify what report B does
- explain the gap in plain language
- decide whether the gap is real, stable, and actionable

### Step 3: Separate knowledge gaps from discipline gaps

This is the most important filter.

Prefer extracting differences that reflect:

- better current-state verification behavior
- better calibration and uncertainty handling
- better source attribution
- better structure and output design
- better decision orientation

Be cautious about extracting differences that may just reflect:

- one report happened to find a better source
- one model knew a fresher fact by chance
- one report had a narrower scope and therefore looked cleaner

If the gap is mainly a knowledge-hit accident, do not harden it into a rule.

### Step 4: Generate rule candidates

For each meaningful gap, write a candidate in imperative form.

Good candidate:
- "Use exact figures when the source provides exact figures; do not round by default."

Weak candidate:
- "Sound more natural."

Every candidate should be:

- reusable
- auditable
- not tied to one company only
- expressible as a rule, checklist item, template change, or eval target

### Step 5: Triage each candidate into one of four actions

Every candidate must end in exactly one of these buckets:

#### A. New rule
Use when the repo truly lacks the discipline.

#### B. Checklist hardening
Use when the rule already exists but is being forgotten or weakly enforced.

#### C. Template change
Use when the main issue is output structure, readability, or presentation discipline.

#### D. No action
Use when the pattern is too subjective, too unstable, or too case-specific.

Do not leave findings floating as vague observations.

### Step 6: Decide whether the candidate is mature enough to promote

Do not immediately promote every candidate to the main skill.

Prefer promoting only when at least two of these are true:

- it appears across **2 or more real cases**
- it can be written as a concrete and testable instruction
- it can be absorbed by a checklist, template, or audit step
- it does not obviously overfit to one industry or one report format

If not mature enough, keep it in the comparative-distillation artifact and wait for another confirming case.

---

## Output standard for a comparative-distillation artifact

A strong comparative-distillation file should contain:

1. the case identity
2. the purpose of the comparison
3. comparison by fixed dimensions
4. the actionable gap per dimension
5. the proposed action type per gap
6. a short final summary of what should change in the repo

If the output does not lead to clear candidate actions, it is commentary, not distillation.

---

## What not to distill

Avoid promoting differences that are mainly:

- tone preference
- writing style preference without decision impact
- one-off elegance or phrasing
- hidden-chain-of-thought speculation
- raw knowledge advantage without process evidence

Examples of weak candidates:
- "Use a more confident tone"
- "Write like GPT"
- "Make it feel smoother"

Examples of strong candidates:
- "Every market-position claim must include scope and a conditional clause."
- "Every forward-looking estimate must cite the named source of the estimate."
- "When primary data is unavailable and a proxy is used, include a short data-calibration note explaining the proxy and its limitation."

---

## Common failure modes in comparative distillation

### Failure mode 1: Content mimicry
Copying the stronger report's wording or structure without identifying the underlying rule.

**Fix:** Always rewrite the observation as a reusable instruction.

### Failure mode 2: Overfitting
Turning one nice pattern from one case into a permanent rule too quickly.

**Fix:** Use the candidate -> promotion discipline. Wait for recurrence.

### Failure mode 3: Knowledge confusion
Treating a fresher fact or lucky source hit as evidence of a better workflow.

**Fix:** Distill process, not lucky retrieval.

### Failure mode 4: Vague actionability
Ending with "report A is more nuanced" without specifying what should change in the skill.

**Fix:** Force every candidate into new rule / checklist hardening / template change / no action.

### Failure mode 5: Rule accumulation without routing
Adding new rules but not deciding when they should trigger.

**Fix:** When promoting a candidate, also decide whether the fix belongs in `SKILL.md`, a checklist gate, or final-audit enforcement.

---

## Integration with the rest of the repo

Comparative distillation should connect to the repo's broader quality system:

- `references/failure-taxonomy.md` — classify the gap into a failure family
- `evals/meta/rule-activation-and-execution-discipline.md` — decide if the problem is missing rule, missing trigger, or execution failure
- `evals/templates/decision-utility-rubric.md` — use when the stronger report is better mainly because it is more decision-useful
- `evals/cases/global-market-scope-completeness-case.md` — use when the gap is really about global coverage geometry
- `checklists/*.md` — use when the pattern should become a hard delivery gate
- `references/report-template.md` — use when the pattern is structural or readability-related

Comparative distillation is not a side note. It is a pipeline for converting better examples into stable skill behavior.

---

## Promotion rule

When a comparative-distillation artifact produces a good candidate, ask:

- Which failure family does it belong to?
- Is it new rule, stronger trigger, stronger checklist, or template fix?
- Is it recurring enough to promote now?
- If promoted, where is the single best home for it?

Prefer one clean home over duplicating the same instruction everywhere.

---

## Bottom line

The purpose of comparative distillation is to turn:

- stronger outputs
- repeated quality gaps
- concrete report differences

into:

- reusable rules
- stronger gates
- better templates
- more targeted evals

If a comparison does not produce one of those, it has not yet done enough work.
