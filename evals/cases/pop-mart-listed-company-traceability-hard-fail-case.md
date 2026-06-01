# Eval: 泡泡玛特 Listed-Company Source Traceability Hard-Fail + Absolute Claim Case

## Goal

Test whether a listed-company / investment-style report with a complete 30-entry source register and natural-language source attribution can still trigger the source-traceability hard-fail gate by using prose-based attribution instead of structured `[SN]` inline citations.

This eval targets a failure mode where:

- the report has a **complete, well-structured source register** (30 `[S#]` entries)
- the body uses **natural language attribution** ("据 FY2025 年报", "招股书披露") — which is human-readable and functionally traceable
- but these do **not use `[SN]` inline citations**, triggering the hard-fail gate: "source register exists but zero [SN] inline citations in body = undeliverable"
- additionally, an **absolute claim** ("中国唯一") is used without exclusivity verification

This is a companion to the AI Traffic Police case (`ai-traffic-police-technical-deep-dive-traceability-case.md`), which had the same source-traceability pattern but with arXiv IDs instead of natural language. Together, these cases suggest the `[SN]` hard-fail gate may need to carve out exceptions for functionally equivalent attribution formats.

## Real case pattern

A user-provided 泡泡玛特 (Pop Mart, 9992.HK) deep research report dated **2026-06-01** demonstrates this pattern:

**What was done well:**
- ✅ Complete research anchor block (FY2025, 2026Q1, 2026-06-01 market snapshot)
- ✅ Support / Weakening / Unresolved 3-way split with 6 independent counter-evidence items (strongest seen)
- ✅ Comprehensive valuation coverage: PE/PB/PS/DCF + 8-broker target price comparison + cycle positioning
- ✅ All hard-fail conditions passed except source-traceability
- ✅ Evidence labels consistent ([确认事实]/[推断]/[未知])
- ✅ Judgment-first opening with clear thesis
- ✅ Data freshness: all anchor points labeled [确认事实]
- ✅ Report redundancy at "slightly compressible" not "severely off-track"

**What triggered the hard-fail:**
- ❌ **Source traceability hard-fail triggered** — 30 `[S#]` entries in the source register, but zero `[SN]` inline citations in the body text. Body uses natural language attribution ("来自 FY2025 年报", "招股书披露", "彭博信用卡数据") which is human-readable but does not follow the `[SN]` format. Per `checklists/source-traceability.md`, this is a hard-fail.

**What has minor gaps:**
- ❌ **Absolute claim "中国唯一" without exclusivity verification** — Section 2 uses "中国唯一" (China's only) for a market positioning claim. This is the strongest absolute claim in the report, but no exclusivity verification is provided. It also violates the report's own §18.2 guidance against overclaimed language.
- ❌ **Section 12.3 entirely [推断] without derivation** — 4 proxy indicators (inventory turnover, per-store revenue, etc.) are labeled [推断] but no calculation formula is shown in the body or appendix. The reader cannot verify the inference.
- ⚠️ **Natural language attribution is functionally traceable but format-noncompliant** — unlike the AI Traffic Police case (which used arXiv IDs for partial traceability), this report uses readable prose like "据 FY2025 年报" which any human reader can follow. The format violation is purely procedural, not functional.

## What this eval is testing

### Failure Mode 1: Natural language attribution vs [SN] format compliance

The report uses natural language source attribution ("据 FY2025 年报") throughout the body — this is functionally traceable (a human reader can find the source), but does not follow the `[SN]` inline citation format required by the source-traceability checklist.

This raises the same question as the AI Traffic Police case: **should the `[SN]` hard-fail gate be strictly format-enforced, or should functionally equivalent attribution (natural language, arXiv IDs, DOIs) be accepted?**

The difference between the three cases:

| Case | Body attribution | Traceability | Hard-fail |
|------|-----------------|-------------|-----------|
| AI Traffic Police | arXiv IDs, paper names | Partial (tech readers can resolve) | ❌ Triggered |
| 泡泡玛特 | Natural language prose ("据FY2025年报") | High (any reader can follow) | ❌ Triggered |
| 人形机器人 | Zero body attribution | None | ❌ Triggered |

The 泡泡玛特 case has the **strongest functional traceability** of all three, yet still triggers the hard-fail because the format doesn't match. This suggests the hard-fail gate needs refinement.

### Failure Mode 2: Absolute claim "唯一" without exclusivity gate

"中国唯一" is the strongest possible market positioning claim. The report uses it without:
- explicit scope definition (唯一 in what dimension? revenue? brand recognition? market share?)
- exclusivity verification evidence
- caveat or conditionality

This is a hard-fail condition per the listed-company route contract, even though it's a single word in one sentence.

### Failure Mode 3: Inference without derivation formula

Section 12.3 labels 4 proxy indicators entirely as [推断] but provides no calculation formula. The reader cannot distinguish between:
- educated guess with a specific formula
- directional estimate based on industry benchmarks
- interpolation from adjacent data points

Without the derivation formula, the inference label is accurate but not transparent.

## Pass criteria

A good answer should:

1. **Structured inline citations (`[SN]`)** — even if natural language attribution is also present, every load-bearing claim must also have a `[SN]` inline reference pointing to the source register
2. **Exclusivity verification for absolute claims** — "唯一", "only", "first" claims must include explicit scope definition + verification evidence or be downgraded to "leading" / "top"
3. **Inference derivation transparency** — each [推断] that involves a calculation or proxy must include the formula, assumptions, and data sources; if proprietary, state the limitation explicitly
4. **Fresh anchor block** (already present in this case — maintain)

## Failure signs

Mark this eval as failed if the answer:

- has a complete source register but zero `[SN]` inline citations in body text
- uses "唯一"/"only"/"first"/"only" without scope definition and exclusivity verification
- labels indicators as [推断] without showing the derivation formula in body or appendix
- has functional traceability via natural language but not `[SN]` format (this case's pattern)

## Why this case exists

This case adds to the growing group of source-traceability borderline cases in Round 2:

| Case | Attribution style | Functional traceability | Format compliance |
|------|-----------------|----------------------|-------------------|
| AI Traffic Police | arXiv IDs + paper names | Partial (tech readers) | ❌ Noncompliant |
| 泡泡玛特 (this case) | Natural language prose | High (all readers) | ❌ Noncompliant |
| TikTok AI | [SN] inline citations | Full | ✅ **Compliant** |

Together, these three cases form a spectrum that should inform the `[SN]` hard-fail gate's refinement in the next fix cycle.

| Gap | Existing coverage | This case adds |
|-----|-------------------|----------------|
| **Natural language attribution vs [SN]** | AI Traffic Police covers arXiv IDs | Natural language prose — functionally best, format noncompliant |
| **Absolute claim "唯一"** | Not explicitly covered | Exclusivity verification gap |
| **Inference without derivation** | Not explicitly covered | Section-level inference transparency gap |

## Suggested intervention target

- `references/source-traceability-and-claim-citation.md` — refine the `[SN]` hard-fail gate to allow functionally equivalent attribution formats (natural language that uniquely identifies the source) while still requiring structured register entries; distinguish between "format noncompliant but traceable" vs "format noncompliant and untraceable"
- `checklists/source-traceability.md` — add a graduated severity scale: (1) no attribution at all = hard-fail, (2) natural language but traceable = conditional pass with format fix recommended, (3) structured `[SN]` = full pass
- `checklists/listed-company-report.md` — add: "unique/only/first claims have explicit scope and exclusivity verification"
- `checklists/final-audit.md` — add non-blocker: "each [推断] with a calculation or proxy includes the derivation formula or explicitly states the limitation"

(**Note**: the source-traceability gate refinement question is shared across 3 Round 2 cases — AI Traffic Police, TikTok AI, and 泡泡玛特. A batch fix should address this pattern rather than individual fixes.)

## Reviewer checklist

- Are `[SN]` inline citations present in the body text (not just natural language)?
- If natural language attribution is used, is it uniquely traceable to a specific source?
- Are "唯一"/"only"/"first" claims verified with scope and exclusivity evidence?
- Are [推断] indicators with calculations accompanied by derivation formulas?
- Is the research anchor block present and fresh?

## Suggested scoring

- **Full pass**: structured `[SN]` citations, no absolute claims without verification, inference formulas present
- **Conditional pass**: natural language attribution (traceable but noncompliant), minor absolute claim, inference labeled but formula absent (this case's level)
- **Fail**: source traceability hard-fail AND no functional traceability; or unverified absolute claims AND other quality issues

## Related evals

- `evals/cases/ai-traffic-police-technical-deep-dive-traceability-case.md` — companion case: same source-traceability hard-fail pattern (arXiv IDs vs natural language)
- `evals/cases/tiktok-ai-technical-deep-dive-route-inflation-case.md` — companion case: Round 2 technical-deep-dive route inflation
- `evals/cases/storage-chip-listed-company-deep-dive-pass-case.md` — pass-level listed-company benchmark (contrast)
- `evals/cases/evergrande-property-listed-company-execution-case.md` — near-pass listed-company benchmark
