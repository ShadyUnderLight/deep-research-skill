# Eval: MLLM Visual Reasoning Academic Review — Body Traceability Narrow-Fail Case

## Goal

Test whether an Academic Review / Literature Review report with strong search strategy documentation, current-state coverage (2023-2026), dual-dimension evidence matrix, substantive counter-evidence, publication bias analysis, and actionable recommendations can still achieve only **Conditional Pass** when:

- **body-level `[S##]` inline citations are entirely absent** — all 32 register sources are uncited in body, making claim-level traceability impossible despite a well-structured register; triggers source-traceability hard-fail
- **self-assessment claims source-traceability ✅** while body has zero `[S##]` — triggers process-integrity risk
- **Source Register has DOI/URL gaps** — 4 entries with `—` placeholder, not "unavailable" annotations
- **peer-review status potentially over-upgraded** — two 2026-06 papers labeled as ICML 2026 peer-reviewed without verification that proceedings/OpenReview confirmation exists at review date

This eval is based on a real report: an MLLM visual reasoning literature review that correctly activated the academic-review route, provided transparent search strategy (databases, search terms, date, inclusion criteria, screening counts), covered 2023-2026 literature with 2026 papers, built a dual-dimension evidence matrix, provided Track D counter-evidence, discussed publication bias with direction and conclusion adjustment, and gave actionable practitioner guidance — but failed on the single most load-bearing academic discipline: body-level claim traceability.

## Prompt

Review the academic literature on multimodal large language model visual reasoning capabilities and limitations. Produce a structured academic literature review that:

- defines the search strategy transparently (databases, Boolean query, search date, inclusion/exclusion criteria, screening counts)
- maps key themes (benchmarks, architecture analysis, failure modes, language shortcuts, data contamination)
- provides a current-state assessment with 2023-2026 coverage
- uses `[S##]` inline citations for every load-bearing claim in every section
- includes a complete academic Source Register with ID, Source Name, Type, Date, Venue, DOI/URL, Peer-Review Status, Publication Type, Reliability, Claims Supported — no placeholder DOIs/URLs
- provides a dual-dimension evidence matrix (study design quality × source role) for load-bearing claims
- includes counter-evidence with structured pressure-testing of common conclusions
- discusses publication bias direction and how it adjusts conclusions
- documents the route boundary: why academic-review rather than technical-deep-dive or provider-selection

## What this eval is testing

- whether body-level `[S##]` traceability is the **narrow gate** that determines academic-review delivery status — when everything else passes but body traceability fails, the verdict should be conditional pass, not fail
- whether self-assessment honesty about body traceability is accurate even when the rest of the report is strong
- whether DOI/URL completeness in the Source Register is maintained (no `—` placeholders)
- whether peer-review status for very recent papers (weeks before review date) is verified or appropriately downgraded

## Pass criteria

A passing answer should:

1. **Execute body-level `[S##]` traceability in every section.** Every load-bearing claim in all substantive sections (opening findings, theme discussions, counter-evidence, actionability) must have an `[S##]` inline citation. Zero `[S##]` across the body = hard-fail regardless of register quality.

2. **Keep self-assessment honest about body traceability.** If body has zero `[S##]`, source-traceability must not claim ✅.

3. **Maintain Source Register completeness.** Every entry must have a real DOI/URL or explicit "unavailable" annotation. No `—` placeholders.

4. **Verify or downgrade peer-review status for recent papers.** Papers from the same month/year as the review date must show verification evidence (proceedings link, OpenReview, acceptance notification) or be labeled as preprint / under review / accepted-pending.

5. **Document the route boundary.** Explain why academic-review rather than technical-deep-dive (architecture analysis would be a different primary burden) or provider-selection (not comparing vendor solutions).

## Failure signs

Mark this eval as failed if the answer does any of the following:

- body has zero `[S##]` inline citations (source traceability hard-fail)
- self-assessment claims source-traceability ✅ while body has zero `[S##]` (process-integrity)
- Source Register has placeholder DOIs/URLs
- recent papers (<3 months before review date) labeled as peer-reviewed without verification evidence
- route boundary not documented

## Why this eval matters

Existing academic-review cases in this collection all fail at **Fail** level with multiple compounded discipline gaps. This case is the first at **Conditional Pass** level for the academic route — it demonstrates what a nearly-passing academic review looks like and isolates the narrow gate that remains:

| Case | Level | Search strategy | Body `[S##]` | Evidence matrix | Counter-evidence | Current-state |
|---|---|---|---|---|---|---|
| Fertility | Fail | ❌ Missing | ❌ Zero | ❌ Missing | ✅ Strong | ⚠️ Partial |
| Transformer | Fail | ✅ Strong | ✅ Present | ❌ Not executed | ⚠️ Partial | ✅ Good |
| AI Agent planning | Fail | ❌ Missing | ❌ Zero | ❌ Not executed | ✅ Strong | ❌ >18mo old |
| MLLM (this) | **Conditional pass** | **✅ Strong** | **❌ Zero** | **✅ Executed** | **✅ Strong** | **✅ 2023-2026** |

The unique contributions:

- **Single-failure isolation** — this case tests whether the delivery system correctly identifies that *only* body traceability is failing while all other disciplines pass. A report with strong search strategy, evidence matrix, counter-evidence, publication bias analysis, and current-state coverage should not fail overall — but it also cannot pass source-traceability without body `[S##]`.
- **Peer-review status calibration for recent papers** — academic reviews that include very recent publications (<3 months old) must either verify acceptance or use tentative labeling (preprint / under review / accepted-pending). This is an academic metadata discipline not yet tested by existing cases.
- **Route boundary documentation for academic-review** — when an academic review includes architecture analysis and model selection recommendations (as this MLLM report does), it must document why the route is academic-review rather than technical-deep-dive or provider-selection. Most existing academic cases don't include this kind of cross-route overlap.

Without this eval, the skill could produce academic reviews that pass search strategy, evidence matrix, and counter-evidence disciplines but fail the *single most load-bearing discipline* (body traceability) — and the conditional-pass verdict would be missed.

## Current rule verdict

- Source traceability hard-fail: body has zero `[S##]` inline citations
- Process-integrity risk: self-assessment claims ✅ while body citations absent
- Source Register: 4 entries with placeholder DOIs
- Peer-review status: recent papers need verification or downgrade — triggers `checklists/academic-analysis-audit.md` §Current-state discipline (Tier-1 recent-paper peer-review verification)

Current rules correctly rate this as **Conditional Pass** — the structure and execution are strong, and the single hard-fail (body traceability) can be fixed with a focused intervention.

## Related evals

- `evals/cases/ai-agent-planning-academic-review-compounded-case.md` — same route, fail level with compounded academic gaps
- `evals/cases/fertility-three-factor-academic-review-search-strategy-gap-case.md` — same route, search strategy as primary failure
- `evals/cases/transformer-academic-review-evidence-matrix-and-secondary-route-case.md` — same route, evidence matrix not executed
- `evals/cases/ai-startup-hq-constrained-choice-register-compliance-case.md` — same "narrow gate" conditional-pass pattern, different route

## Reviewer checklist

- Does the body have `[S##]` inline citations in every section? (zero = immediate issue)
- Does self-assessment reflect body traceability status honestly?
- Does the Source Register have real DOIs/URLs for all entries?
- Are very recent papers (<3 months) labeled with verified peer-review status or downgraded?
- Is the route boundary documented (why not technical-deep-dive or provider-selection)?

## Suggested scoring

- **Pass**: body `[S##]` in all sections, self-assessment honest, register clean, recent papers properly labeled, route boundary documented
- **Conditional Pass** (this case's level): search strategy strong, evidence matrix executed, counter-evidence substantive, counter-evidence present, publication bias analyzed, current-state coverage current — BUT body `[S##]` absent (single discipline gap), self-assessment slightly optimistic, register has minor completeness issues — no compounding
- **Fail**: body traceability absent AND self-assessment claims full pass (process-integrity), OR multiple disciplines fail simultaneously (search strategy + evidence matrix + current-state + traceability), OR Source Register has placeholder entries
