# Eval: AI Agent Planning Academic Review — Compounded Fail Case

## Goal

Test whether an Academic Review / Literature Review report with strong opening judgment, structured theme coverage (benchmarks, human evaluation, theoretical frameworks, core debates), and clear publication bias discussion can still **fail strict delivery** when multiple academic-specific failures compound:

- **search strategy transparency insufficient** — no database list, Boolean query, search date, screening counts, or exclusion criteria documented
- **current-state verification failure** — June 2026 report using "~2024末" as SOTA, with self-aware admission of the gap but no corrective action (not re-verified, not downgraded to historical snapshot)
- **Source Register contains placeholder** — `arXiv:2402.xxxxx` unresolved — delivery cleanliness hard-fail
- **evidence matrix declared but not fully executed** — has venue prestige and reliability but no dual-dimension study-design-quality × source-role mapping
- **self-assessment claims all ✅ while search strategy, current-state verification, evidence matrix, and placeholder all have gaps** — triggers process-integrity hard-fail
- **cherry-picking risk not fully addressed** — has pro/con coverage but no exclusion rationale documentation

This eval is based on a real report: an AI Agent planning ability evaluation literature review that correctly activated the academic-review route, organized key themes, discussed publication bias, and identified open questions — but compounded search methodology, current-state verification, source register cleanliness, evidence matrix, and self-assessment failures.

## Prompt

Review the academic literature on AI Agent planning ability evaluation methods. Produce a structured academic literature review that:

- defines the search strategy (databases, Boolean query, search date, inclusion/exclusion criteria, screening counts)
- maps key research themes (benchmarks, human evaluation, adversarial evaluation, theoretical frameworks, core debates)
- provides a current-state assessment with explicit coverage window — if latest verified sources are from ~2024, state that the review covers through that date and does not claim 2025-2026 SOTA
- includes a complete academic Source Register with ID, Source Name, Type, Date, Venue, DOI/URL, Peer-Review Status, Publication Type, Reliability, Claims Supported — no placeholder entries
- builds a dual-dimension evidence matrix (study design quality × source role) for load-bearing claims
- addresses cherry-picking risk by documenting what was excluded and why
- distinguishes preprints from peer-reviewed publications in body labels
- discusses publication bias direction and how it affects conclusions

## What this eval is testing

- whether search strategy transparency is documented to academic-review minimum standards
- whether current-state verification is honest about coverage windows — "as of ~2024" is acceptable if explicit, but "current SOTA" with 2024 data is not
- whether Source Register entries are complete and real (no placeholder DOIs/URLs)
- whether evidence matrix is executed as a dual-dimension mapping, not just a single-dimension source table
- whether cherry-picking is addressed with exclusion rationale, not just pro/con presence
- whether self-assessment accuracy matches body execution across academic-specific disciplines

## Pass criteria

A passing answer should:

1. **Document search strategy transparently.** State databases, Boolean query, search date, inclusion/exclusion criteria, initial screening count, and final included count. If the search was informal, use "structured literature review" wording — do not claim systematic review.

2. **Set honest current-state boundaries.** If latest verified sources are from 2024, state coverage window explicitly. Do not claim "current SOTA" for information that is 18+ months old. Either re-verify or downgrade to "as of [date]."

3. **Deliver a clean Source Register with no placeholders.** Every DOI/URL must be real and resolvable (not `arXiv:2402.xxxxx` or similar). Entries without accessible identifiers must state "unavailable" explicitly.

4. **Execute the evidence matrix as dual-dimension.** Each load-bearing source should map study design quality (RCT / controlled study / case series / expert opinion / theoretical) against source role (primary evidence / secondary analysis / background).

5. **Document exclusion rationale.** Name excluded works or categories and explain why exclusion does not change the review's conclusions.

6. **Keep self-assessment honest.** Audit status must reflect actual execution gaps in search strategy, current-state verification, source register, and evidence matrix.

## Failure signs

Mark this eval as failed if the answer does any of the following:

- search strategy lacks databases, search date, or screening counts (academic hard-fail)
- claims "current SOTA" or similar for information >12 months old without explicit coverage window
- Source Register contains unresolved placeholders (e.g., `arXiv:2402.xxxxx`)
- evidence matrix claimed but not executed as dual-dimension mapping
- cherry-picking not addressed with exclusion rationale
- self-assessment claims all ✅ while search, current-state, register, or evidence matrix have gaps

## Why this eval matters

Existing academic-review cases each isolate specific failures. This case tests the **compounded scenario** where all academic-specific discipline gaps hit simultaneously:

| Case | Route | Level | Primary failure | Secondary gap |
|---|---|---|---|---|
| Fertility search strategy | academic-review | Fail | Search strategy incomplete | Source register columns, wording |
| Transformer evidence matrix | academic-review | Fail | Evidence matrix not executed | Secondary route, cherry-picking |
| AI Agent planning (this) | academic-review | **Fail** | **Compounded + current-state + placeholder** | Search, evidence matrix, cherry-picking, self-assessment |

The unique contributions:

- **Academic current-state verification** — academic reviews have a "current state" contract that is inherently time-bound. A 2026-06 report using "~2024末" SOTA must either re-verify or explicitly downgrade. This is different from "stale data" in listed-company/market-outlook routes because the failure is self-aware: the report knows it's out of date but does not adjust its claims or self-assessment.
- **Source Register placeholder** — `arXiv:2402.xxxxx` is a delivery cleanliness failure specific to academic metadata. It signals that the source item was queued but never resolved — distinct from "missing DOI/URL" (which is a format issue) because the entry *looks* like it has an identifier but it's non-functional.
- **Compounded academic failures** — tests whether each academic discipline is independently checked when they all fail simultaneously.

## Current rule verdict

- Academic methodology hard-fail: search strategy incomplete
- Current-state verification: coverage window >18 months old not explicitly declared — violates `checklists/academic-analysis-audit.md` §Current-state discipline (coverage window declaration)
- Delivery cleanliness: unresolved placeholder in Source Register
- Evidence matrix: declared but not executed as dual-dimension
- Process-integrity hard-fail: self-assessment overclaim

## Related evals

- `evals/cases/content-platform-constrained-choice-compounded-fail-case.md` — same compounded-fail pattern, different route
- `evals/cases/fertility-three-factor-academic-review-search-strategy-gap-case.md` — same route, search strategy as primary failure
- `evals/cases/llm-hallucination-academic-review-source-register-gap-case.md` — same route, source register template gap
- `evals/cases/mcp-technical-deep-dive-timeline-roadmap-case.md` — same current-state timeline integrity pattern
- `evals/cases/mllm-visual-reasoning-academic-review-narrow-fail-case.md` — same route, narrow-fail: body traceability absent while other disciplines pass
- `evals/cases/transformer-academic-review-evidence-matrix-and-secondary-route-case.md` — same route, evidence matrix not executed

## Reviewer checklist

- Is search strategy transparent (databases, query, date, screening counts)?
- Is the coverage window honest about current-state limitations?
- Does the Source Register have any unresolved placeholders?
- Is the evidence matrix a dual-dimension mapping (not just source list)?
- Is cherry-picking addressed with exclusion rationale?
- Does self-assessment match body execution?

## Suggested scoring

- **Pass**: search strategy transparent, coverage window honest, Source Register clean, evidence matrix executed, cherry-picking addressed, self-assessment honest
- **Conditional pass**: academic-review structure strong, themes organized, publication bias discussed, but search strategy partially documented (has databases and date, no screening counts), or evidence matrix declared but thin, or self-assessment slightly optimistic — no hard-fail triggered
- **Fail**: search strategy lacks databases/search date/screening counts, or "current SOTA" claimed for data >12 months old without window, or Source Register has placeholder entries, or evidence matrix claimed but not executed, or self-assessment claims all ✅ while gaps exist
