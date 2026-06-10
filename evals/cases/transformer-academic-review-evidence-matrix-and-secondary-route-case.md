# Eval: Transformer 论文脉络 Academic Review — Evidence Matrix + Secondary Route Gap Case (Round 6)

## Goal

Test whether an academic-review / paper-lineage report with strong scope, milestones, and current-paradigm analysis can still receive a **Fail** rating when:

- **Source Register meets 7-column format but fails academic metadata requirements** — no publication type, peer-review status, or venue columns per academic route contract
- **dual-dimension evidence matrix declared but not executed** — same pattern as the LLM hallucination case
- **secondary route hard-fail skipped** — declares `technical-deep-dive` as secondary but explicitly skips its hard-fail verification
- **strong claims over-labeled as `[确认事实]`** — "所有现代 LLM 标准组件""Mamba 首次实质性挑战" should be scoped inferences
- **cherry-picking risk unaddressed** — excluded architectures (T5, XLNet, Performer) listed but no explanation of why exclusion doesn't affect conclusions
- **self-assessment claims full pass** while academic hard-fail is triggered and secondary route verification is skipped

This is the **eighth Round 6 case**, adding academic-review with **secondary route hard-fail skipping**.

## Real case pattern

A user-provided report "Transformer 架构关键论文脉络" dated **2026-06-10** demonstrates this pattern. Inferred route: `academic-review` with `technical-deep-dive` secondary.

**What was done well:**
- ✅ Opening carries core judgment — 4 families, key fork points, trend judgment upfront
- ✅ Scope/review methodology explicit — databases, search terms, date, inclusion criteria, screening flow
- ✅ Key themes and trends — Encoder-only, Decoder-only, efficiency innovation, cross-modal clearly structured
- ✅ Major breakthroughs/milestones table (§4.2 fork points) useful
- ✅ Preprints distinguished from published in body text
- ✅ Publication bias discussed (acknowledges high-impact paper bias)
- ✅ Route-specific labels visible: search method, publication bias, Source Register
- ✅ Source Register uses 7-column template per Round 4 #182

**Core issues (Fail — hard-fail triggered):**
- ❌ **Source Register fails academic metadata requirements** — 7-column format present but missing: publication type (original research / survey / benchmark / position paper), peer-review status (peer-reviewed / preprint / tech report / unknown), venue (NeurIPS / arXiv / blog). Only `Type=primary/secondary` and `Reliability=high/medium` present, which are not academic evidence taxonomy.
- ❌ **Dual-dimension evidence matrix declared not executed** — §1.4 describes evidence level system, but no source-level mapping table exists per study design quality × venue prestige. Same pattern as the LLM hallucination case.
- ❌ **Secondary route hard-fail skipped** — declares `technical-deep-dive` as secondary route but explicitly writes "§3 covered, no independent run needed" (§8). Per final-audit discipline, secondary route hard-fail must be verified.
- ❌ **Strong claims labeled `[确认事实]`** — "所有现代 LLM 的标准组件""Mamba 首次实质性挑战了 Transformer 范式" are labeled as confirmed facts but evidence role is closer to "high-consensus inference" or "mainstream observation". Need scoped inference labels per Round 5 #191.
- ❌ **Cherry-picking not justified** — excluded architectures (T5, XLNet, Performer, Nyströmformer) listed in §8 but no explanation of why they were excluded and whether inclusion would change conclusions.
- ❌ **Self-assessment claims full pass** — audit status block claims `academic-analysis-audit ✅`, `source-traceability ✅`, `final-audit ✅`, but academic hard-fail is triggered (evidence matrix missing, source metadata incomplete, secondary route skipped).

## Why this case exists

This is the eighth Round 6 case. It adds:

1. **Secondary route hard-fail skipping** — a pattern not yet covered in Round 6. Previous cases either had secondary routes with issues or lacked secondary routes entirely. This case explicitly acknowledges a secondary route and then explicitly skips its verification.
2. **Academic Source Register gap subtype** — unlike the LLM hallucination case (which failed the 7-column template entirely), this case passes the 7-column format but fails the **additional academic metadata** requirements. A different gap in the same family.
3. **Cherry-picking without justification** — a variant of scope completeness failure specific to academic reviews: excluded works are listed but their exclusion rationale is absent.

## Relationship to existing Transformer eval

The existing `academic-route-activation-transformer-origin-case.md` is a route activation validation case (Round 3/4). This case tests deliverable quality of a full paper-lineage report. No overlap.

## Suggested intervention

- `checklists/academic-analysis-audit.md` — add hard-fail: "if a secondary route is declared, its hard-fail verification must be itemized; 'covered elsewhere without independent run' is a hard-fail"
- `references/academic-evidence-hierarchy.md` — add explicit Source Register columns for academic route: publication type, peer-review status, venue; the Round 4 #182 7-column template is necessary but insufficient for academic review
- `references/source-traceability-and-claim-citation.md` — add guidance: "excluded works in a literature review must include rationale; listing exclusions without justification is not scope completeness"

> **Round 6 P2 update (#209):** `checklists/academic-analysis-audit.md` 已追加副路由 hard-fail 验证 Tier-1 检查项。`checklists/route-activation-audit.md` 已追加副路由 hard-fail 跳过阻断级检查。`ROUTING-MATRIX.md` 已追加 Do-not-use 条款解决要求。

## Related evals

- `evals/cases/llm-hallucination-academic-review-source-register-gap-case.md` — Round 6 companion: same evidence matrix declared-not-executed pattern
- `evals/cases/academic-route-activation-transformer-origin-case.md` — route activation baseline (different focus)
- `evals/cases/rag-technical-deep-dive-register-gap-case.md` — Round 5: Source Register template compliance
