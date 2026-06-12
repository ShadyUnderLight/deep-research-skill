# Eval: Local LLM Equipment Selection — Budget Boundary and Secondary Provider Route Case

## Goal

Test whether an Equipment Selection / Procurement report with strong conditional recommendation (cloud-first, verify for 1-3 months), per-profile guidance, TCO comparison, and clear reversal conditions can still **fail strict delivery** when:

- **budget/TCO inclusion/exclusion boundary is incomplete** — upfront cost, electricity, monthly fees, residual value listed but no mention of tax, storage, network, UPS, cooling, warranty, cloud storage/bandwidth — reader cannot assess whether quoted prices are "all-in" — triggers equipment-selection hard-fail
- **secondary provider route (Vendor Selection) declared but hard-fail not verified** — cloud GPU providers (RunPod, Vast, AutoDL) listed for comparison but no independent audit of provider accessibility, SLA, compliance, data control, or ranking logic
- **body-level source traceability absent** — zero `[Sxx]` inline citations across the entire report; source list is loose bibliography, not 7-column Source Register
- **numeric role labels absent from all comparison/estimate tables** — TCO, performance, power, breakeven, residual value lack observed/proxy/assumption/model-output labels
- **self-assessment claims all ✅ while multiple disciplines have execution gaps** — process-integrity and declared-not-executed hard-fails triggered
- **shortlist boundary not justified** — Mac Studio / RTX 5090 / Cloud GPU is reasonable but no exclusion logic for used workstation, dual 4090, A100 local, managed bare metal
- **strong wording in equipment context** — "唯一" (compatibility), "无限" (VRAM scalability) without exclusivity evidence or qualification

This eval is based on a real report: a local LLM hardware selection memo (Mac Studio vs RTX 5090 host vs cloud GPU) that correctly activated the equipment-selection route, provided per-profile conditional recommendations, structured TCO comparison, strong counter-evidence, and actionable next steps — but failed on budget boundary completeness, secondary route verification, and the now-common traceability/labeling/self-assessment triad.

## Prompt

A developer needs to choose a local LLM hardware setup. Produce a structured equipment selection memo that:

- states the actual decision (buy Mac Studio / build RTX 5090 host / use cloud GPU — or a phased combination)
- defines hard constraints (model size, VRAM, daily usage intensity, speed needs, noise tolerance, privacy requirements)
- defines soft preferences (low maintenance, quiet, upgradeability, ecosystem fit)
- provides a top recommendation with credible runner-up and rejected-option reasons
- includes a complete TCO table covering all major cost categories with explicit inclusion/exclusion items
- states budget boundaries clearly: what's included (hardware, power, cooling, storage, network, warranty, cloud costs) and what's excluded (tax, UPS, extra peripherals)
- justifies the shortlist boundary — why these three options and not used workstation, dual 4090, A100 local, managed bare metal
- if declaring a secondary route (e.g., Provider/Vendor Selection for cloud GPU), runs and reports its hard-fail verification (accessibility, SLA, compliance, data control, ranking logic)
- uses claim-level `[Sxx]` inline citations throughout
- includes a complete 7-column Source Register
- labels all key numbers with observed/proxy/assumption/model-output roles
- qualifies strong wording: "唯一" must specify in what context, "无限" must specify actual limits

## What this eval is testing

- whether budget/TCO inclusion/exclusion boundaries are explicitly declared — equipment-selection hard-fail if missing
- whether a declared secondary provider route has independent hard-fail verification
- whether body-level source traceability is executed (not just appendix-level)
- whether numeric role labels cover all comparison/estimate tables
- whether self-assessment matches actual body execution
- whether shortlist boundary is justified for equipment selection
- whether strong wording in equipment context ("唯一", "无限") is properly qualified

## Pass criteria

A passing answer should:

1. **Declare budget/TCO boundaries explicitly.**
   - state what cost categories are included (hardware, power, cooling, storage, network, cloud compute/bandwidth, warranty)
   - state what cost categories are excluded (tax, UPS, peripherals, setup labor)
   - reader can assess whether the quoted TCO is comparable across options
   - do not let "约 ¥X" or "总成本 ¥Y" stand without scope

2. **Execute declared secondary provider route verification.**
   - if cloud GPU providers are compared, run Provider/Vendor Selection hard-fail items: accessibility, SLA/uptime, compliance (data residency, export control), data control (privacy, persistence), ranking logic with current pricing snapshot
   - do not simply state "verified" without showing results

3. **Provide body-level `[Sxx]` traceability.**
   - exec summary, TCO table, comparison dimension conclusions, reversal conditions all have inline `[Sxx]`
   - source register is 7 columns with all entries ID'd and cited

4. **Label numeric roles on all comparison/estimate tables.**
   - TCO figures labeled as observed (if quoted), estimate (if from third-party tracking), assumption (if modeled)
   - benchmark performance figures labeled by epistemic role (observed-benchmark, vendor-claim, proxy-benchmark, model-output, or assumption) and disclose model, quantization, context/prompt length, backend, metric type, and batch/concurrency per the benchmark comparability discipline (see ROUTING-MATRIX.md §Equipment Selection Hard Fail)
   - breakeven/residual value labeled as model output

5. **Justify the shortlist boundary.**
   - explain why these options and not others (used, dual-GPU, A100, bare metal)
   - exclusion logic visible

6. **Qualify strong wording.**
   - "唯一" must state: unique in what dimension, based on what evidence
   - "无限" must state: what the practical limit is

## Failure signs

Mark this eval as failed if the answer does any of the following:

- TCO/budget table presents figures without stating inclusion/exclusion boundaries (equipment-selection hard-fail)
- declared secondary provider route has no independent hard-fail verification
- body has zero `[Sxx]` inline citations
- comparison/estimate tables entirely lack numeric role labels
- self-assessment claims full pass while traceability, numeric roles, or budget boundary have gaps
- shortlist boundary is not justified
- "唯一" or "无限" used without qualification

## Why this eval matters

This case adds an equipment-selection-specific failure mode not yet covered by existing cases, plus continues the cross-cutting patterns from the current batch:

| Case | Route | Level | Core failure |
|---|---|---|---|
| Home NAS | equipment-selection | Conditional pass | Labels over-strong, TCO inconsistent, quant roles missing |
| Local AI Lab | equipment-selection | Conditional pass | Body traceability absent, quant roles missing, self-assessment |
| Local LLM (this) | equipment-selection | **Fail** | **Budget boundary incomplete (hard-fail) + provider route unverified + traceability/roles/self-assessment triad** |

The unique contributions:

- **Budget boundary completeness** — existing cases test TCO accuracy and consistency (are the numbers self-consistent?), but this case tests scope completeness (does the reader know what's included?). An equipment selection TCO table without inclusion/exclusion boundaries is like a source register without a DOI/URL column: the infrastructure exists but lacks the column that makes it auditable.
- **Secondary provider route in equipment context** — when cloud GPU providers are compared as part of equipment selection, the Provider/Vendor Selection hard-fail must be independently verified. This extends the secondary route verification pattern (previously seen in regulatory and competitive-positioning) to equipment-selection.
- **Equipment-specific strong wording** — "唯一" in equipment selection means something different than in competitive positioning. It's about technical compatibility or feature uniqueness, not market leadership. The qualification standard is different.
- **Escalation to Fail level** — existing equipment-selection cases are conditional pass. This case tests the transition to fail: structure is still strong, but the combination of budget boundary + secondary route + traceability/roles creates a non-deliverable artifact.

Without this eval, the skill could produce equipment-selection reports with well-structured TCO tables that are un-auditable because the reader doesn't know what costs are included — a failure mode that existing conditional-pass cases don't capture.

## Current rule verdict

The current rules should catch this as **fail**:

- equipment-selection hard-fail: budget/TCO inclusion/exclusion boundaries not declared
- secondary route hard-fail: provider route declared but not verified
- source traceability hard-fail: body has zero `[Sxx]`
- numeric role hard-fail: comparison/estimate tables lack role labels
- process-integrity hard-fail: self-assessment claims all ✅ while gaps exist

This case guards against **equipment selection reports with TCO theater** — numbers that look comparable but hide cost scope assumptions.

## Related evals

- `evals/cases/home-nas-equipment-selection-label-case.md` — same route, conditional pass with TCO inconsistency and label gaps
- `evals/cases/local-ai-lab-equipment-selection-traceability-case.md` — same route, conditional pass with body traceability and role gaps
- `evals/cases/indie-dev-constrained-choice-delivery-fail-case.md` — same process-integrity and delivery fail pattern, sibling route
- `evals/cases/china-data-export-regulatory-secondary-route-case.md` — same secondary route verification pattern, different route
- `evals/cases/bytedance-competitive-positioning-source-mapping-case.md` — same source traceability disconnect, different route

## Reviewer checklist

- Does the TCO/budget table state inclusion and exclusion boundaries?
- If cloud GPU providers are compared, is the vendor-selection hard-fail independently verified?
- Does the body have `[Sxx]` inline citations in all key sections?
- Do comparison/estimate tables have numeric role labels?
- Does self-assessment match actual body execution?
- Is the shortlist boundary justified (why these options, what was excluded)?
- Are strong wording claims ("唯一", "无限") qualified?

## Suggested scoring

- **Pass**: budget boundaries declared, secondary route verified if declared, body-level `[Sxx]` present, numeric roles on tables, self-assessment honest, shortlist boundary justified, strong wording qualified
- **Conditional pass**: equipment selection structure strong, per-profile recommendations present, TCO comparison exists, but budget boundaries partially declared (some categories missing), or secondary route verification thin, or traceability/roles partially absent — no hard-fail triggered
- **Fail**: budget/TCO inclusion/exclusion boundaries absent (equipment hard-fail), or secondary provider route declared but not verified, or body has zero `[Sxx]`, or comparison tables lack numeric roles, or self-assessment claims all ✅ while multiple gaps exist
