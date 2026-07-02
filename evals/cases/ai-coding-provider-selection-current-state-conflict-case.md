# Eval: AI Coding Agent Provider Selection — Geo-Specific Current-State Conflict Case

## Goal

Test whether a Provider / Vendor Selection report with clear ranked shortlist, geo-specific decision criteria (Chinese mainland accessibility/compliance), runner-up credibility, and conditional recommendations can still **fail strict delivery** when:

- **current-state verification is externally contradicted** — Codex capabilities described as "only macOS desktop" while current official docs show web/CLI/IDE/macOS/Windows support; a verifiably stale provider snapshot
- **register inflation exceeds 25%** — 37 entries, ~14 uncited in body
- **numeric role labels absent** — star ratings, prices, team sizes, context windows, adoption rates lack observed/proxy/assumption/model-output roles; triggers provider-selection blocker
- **vendor claims not distinguished from independent verification** — provider docs used without "(厂商文档，非独立验证)" caveat
- **route boundary not fully justified** — why provider-selection beats constrained-choice as primary route not explained
- **strong wording without scope** — "最强", "唯一", "完全封锁", "大多数科技公司标准配置" without source IDs or scope qualification
- **self-assessment claims all ✅ while current-state, traceability, numeric roles, and vendor claims all have gaps** — triggers process-integrity hard-fail

This eval is based on a real report: an AI Coding Agent provider selection memo for Chinese mainland teams that correctly activated the provider-selection route, used geo-specific constraints (GFW, compliance, VPN dependency, team governance) as load-bearing variables, provided a clear ranked shortlist with conditional recommendations — but failed on current-state verification that was externally verifiable as stale, register inflation, numeric role labeling, vendor claim discipline, and self-assessment accuracy.

## Prompt

A Chinese mainland team needs to select a primary AI Coding Agent. Produce a structured provider-selection memo that:

- defines the team profile and geo-specific constraints (mainland accessibility, compliance, team governance, pricing in RMB)
- provides a current provider snapshot with dated, sourced, and verifiable facts for each provider (supported platforms, models, pricing, accessibility, compliance status)
- includes a ranked shortlist with why top option wins, why runner-up is credible, and why each other option loses
- provides ranking-reversal conditions and a phased adoption plan
- uses `[Sxx]` inline citations for every load-bearing claim
- includes a complete 7-column Source Register with all entries cited in body
- distinguishes vendor documentation (manufacturer claims) from independent verification in body labels
- labels all comparison/price/score numbers with observed/proxy/assumption/model-output roles
- documents the route boundary: why provider-selection rather than constrained-choice or other alternatives
- qualifies strong wording ("最强", "唯一", "完全封锁") with source ID and scope

## What this eval is testing

- whether current-state verification for fast-moving provider products is externally verifiable — claims about current platform support, pricing, and model availability must match official docs
- whether provider-selection with geo-specific constraints (Chinese mainland) correctly raises accessibility/compliance to load-bearing variable status
- whether register inflation is kept below 25%
- whether vendor documentation is distinguished from independent verification in body-level labels
- whether route boundary is documented (provider-selection vs constrained-choice)
- whether strong wording is qualified with source and scope
- whether self-assessment accuracy matches body execution

## Pass criteria

A passing answer should:

1. **Deliver externally verifiable current-state snapshot.** Every provider claim (supported platforms, pricing tier, model version, China accessibility) must be sourced from current official docs with access date. If a claim cannot be verified from current docs, mark it as "unverifiable at [date]."

2. **Maintain register inflation below 25%.** No more than 25% of registered sources uncited in body.

3. **Distinguish vendor claims in body labels.** Vendor pricing pages, documentation, and feature lists must carry "(厂商文档)" or equivalent caveat — not `[确认事实]` or `[官方数据]` without source-role annotation.

4. **Document route boundary.** Explain why provider-selection rather than constrained-choice. The key difference: constrained-choice picks between abstract options; provider-selection evaluates specific vendor offerings with current-state verification.

5. **Qualify strong wording.** "最强", "唯一", "完全封锁", "大多数科技公司标准配置" must include a source ID and scope boundary.

6. **Label numeric roles.** All comparison/price/score numbers with observed/proxy/assumption/model-output labels.

## Failure signs

Mark this eval as failed if the answer does any of the following:

- provider current-state claims are verifiably stale (contradicted by current official docs)
- register inflation >25%
- vendor documentation used as `[确认事实]` without source-role caveat
- route boundary not documented (why not constrained-choice)
- strong wording without source ID or scope
- numeric role labels absent from comparison/price/score tables
- self-assessment claims all ✅ while current-state, traceability, or vendor labels have gaps

## Why this eval matters

This case adds a **verified stale-data failure** to the provider-selection route — not just "can't verify freshness" but "external check proves the data is wrong":

| Case | Route | Current-state | Register | Numeric roles | Verified stale? |
|---|---|---|---|---|---|
| AI Coding Tools (old) | provider-selection | Unverifiable | Bibliography | Missing | No |
| AI Coding Agent (this) | provider-selection | **Externally contradicted** | 37/14 uncited (>25%) | Missing | **Yes — verified via official docs** |

The unique contributions:

- **Externally verified stale data** — the reviewer checked current official Provider documentation and found platform support, model, and pricing claims that were incorrect. This is more severe than "unverifiable freshness" (existing case) because it proves the report's current-state snapshot is wrong.
- **Geo-specific provider selection** — Chinese mainland accessibility/GFW/compliance as primary ranking variable adds a dimension not present in existing provider-selection cases (which test general tool selection without geo-constraint weighting).
- **Vendor claim discipline for provider-selection** — when the report's subject IS a vendor product, the line between "vendor documentation as source" and "independent verification" is especially blurry. This case tests whether vendor docs are systemically caveated as manufacturer claims.

## Current rule verdict

- Current-state hard-fail: verified stale (externally contradicted)
- Register inflation hard-fail: >25% uncited
- Numeric role hard-fail: absent from comparison/price tables
- Vendor claim discipline: vendor docs not distinguished from independent verification
- Process-integrity hard-fail: self-assessment overclaim

## Related evals

- `evals/cases/ai-coding-tools-provider-selection-traceability-fail-case.md` — same route/topic, unverifiable freshness (vs verified stale)
- `evals/cases/rag-api-provider-selection-traceability-fail-case.md` — same route, traceability fail
- `evals/cases/aaeon-listed-company-label-inflation-case.md` — same label-inflation discipline, different route
- `evals/cases/dc-power-market-outlook-inflation-and-monitoring-case.md` — same register inflation severity, different route

## Reviewer checklist

- Is every provider current-state claim externally verifiable from current official docs?
- Is register inflation below 25%?
- Are vendor documentation sources distinguished from independent verification in body labels?
- Is the route boundary documented (provider-selection vs constrained-choice)?
- Are strong wording claims ("最强", "唯一", "完全封锁") sourced and scoped?
- Do comparison/price/score tables have numeric role labels?
- Does self-assessment match body execution?

## Suggested scoring

- **Pass**: all provider claims verifiably current, register inflation <25%, vendor claims caveated, route boundary documented, strong wording qualified, numeric roles present, self-assessment honest
- **Conditional pass**: provider-selection structure strong, ranking clear, geo-specific constraints load-bearing, but current-state verification unverifiable (not yet proven wrong), or register inflation 25-40%, or vendor caveats partial, or numeric roles exist but incomplete — no hard-fail triggered
- **Fail**: provider current-state claims verifiably stale (externally contradicted), or register inflation >25% (hard-fail), or vendor docs carry `[确认事实]` without caveat, or route boundary not documented, or self-assessment claims all ✅ while gaps exist (process-integrity hard-fail)
