# Eval: 中际旭创 Listed-Company Execution Near-Pass Case

## Goal

Test whether a listed-company / investment-style deep-research report on a fast-growing, AI-driven company can achieve near-complete route-contract execution while still having minor traceability and structure gaps.

This eval is based on a real "near-pass" case covering 中际旭创 (Zhongji Innolight, 300308.SZ), a high-growth optical module maker deeply tied to the AI infrastructure cycle. It passed most route-contract checks and all hard-fail conditions, but had 3 specific gaps that are instructive for the listed-company route.

## Real case pattern

A user-provided 中际旭创 report dated **2026-05-29** demonstrates near-complete execution:

**What was done well:**
- ✅ Research Anchor Block present and complete (FY2025, 2026Q1, 2026-05-29 market snapshot)
- ✅ Judgment-first opening — "核心结论" appears at line 5 with investment thesis and risk caveat
- ✅ All hard-fail conditions passed (7/7)
- ✅ Comprehensive financial data (2023-2026Q1) with source dates
- ✅ Bull/Bear logic separated (§6 看多逻辑, §7 看空逻辑)
- ✅ Valuation analysis with historical PE/PB comparison
- ✅ Analyst consensus summary with source attribution
- ✅ Evidence labeling (Confirmed / Likely inference / Open uncertainty) throughout
- ✅ Monitoring signals and investment advice in bottom line
- ✅ No "unique/only/irreplaceable" language misuse
- ✅ Scope-qualified market share claims ("全球市占率40-51%")
- ✅ Counter-evidence chapter present (§7 看空逻辑)
- ✅ Uncertainty register (§8.3 Open Uncertainty)
- ✅ Source list at end of document

**What has minor gaps:**
- ⚠️ **Claim-level traceability incomplete** — many load-bearing claims have confidence labels but lack inline source citations. For example, "800G光模块全球市占率超40%" appears without a direct `[Sxx]` or source reference in the body. The source list exists in the appendix but body-level traceability is inconsistent.
- ⚠️ **Counter-evidence structural asymmetry** — bull case (§6) has a structured "事实依据/推断依据/不确定性" 3-column table, but bear case (§7) does not match this structure. The bear case section lists risks without the same epistemic-layer breakdown, making it feel less rigorous even though the content is valid.
- ⚠️ **Valuation-range inference basis unclear** — the valuation range "保守区间560-620元" (§估値分析) is labeled as "Likely Inference" but the inference basis (PE multiple assumptions, comparable company selection logic) is not explicitly stated. The reader cannot reconstruct the valuation range from the stated assumptions.

## What this eval is testing

### Test Dimension 1: Claim-level traceability for high-growth listed companies

This case tests whether the system provides body-level inline citations for load-bearing claims, not just a source list in the appendix. For a fast-growing company like 中际旭创 where market share and growth rate claims are thesis-critical, lack of body traceability weakens auditability.

### Test Dimension 2: Counter-evidence structural symmetry

This case tests whether the bear/bull case sections are structurally symmetric. If one side has a 3-column epistemic breakdown (fact basis / inference basis / uncertainty) and the other side is unstructured prose, the asymmetry can make the report feel imbalanced to the reader even if both sides are substantively covered.

### Test Dimension 3: Valuation inference transparency

This case tests whether valuation ranges labeled as "Likely Inference" include enough methodological basis (multiple assumptions, comparable selection, scenario parameters) for the reader to reconstruct or challenge the range.

## Pass criteria

A good answer should:

1. **Body-level claim traceability** — all load-bearing claims (market share, growth rate, margin trajectory) have inline source citations, not just appendix references
2. **Symmetric counter-evidence structure** — bull and bear case sections use the same structural format (same column breakdown, same epistemic rigor)
3. **Transparent valuation inference** — valuation ranges labeled as inference include: PE multiple range, basis for multiple selection, comparable company logic if applicable, and scenario parameters
4. **All hard-fail conditions passed** (same baseline as other listed-company evals)
5. **Complete route contract** — research anchor block, market snapshot, evidence labels, uncertainty register, source register, bottom line

## Failure signs

Mark this eval as **partial** rather than full pass if the answer does any of the following:

- lacks body-level inline citations for 3+ load-bearing claims
- has structurally asymmetric bull/bear case sections (one side has epistemic breakdown, the other does not)
- labels a valuation range as "inference" without stating the multiple assumptions or parameters
- misses any hard-fail condition or mandatory section

## Why this case exists

This case adds coverage for three subtle gaps that existing evals do not fully address:

| Gap | Existing coverage | This case adds |
|-----|-------------------|----------------|
| **Body-level traceability** | `source-traceability-moore-threads-case.md` covers complete absence of source list | Covers case where source list exists but body citations are inconsistent |
| **Counter-evidence symmetry** | `cnooc-judgment-shape-case.md` covers weak counter-evidence | Covers case where counter-evidence exists but structural format is asymmetric |
| **Valuation transparency** | `consensus-and-forward-pe-misuse-case.md` covers forward PE misuse | Covers case where valuation range inference basis is implicit rather than explicit |

Together with `evals/cases/evergrande-property-listed-company-execution-case.md`, it forms a "near-pass benchmark" cluster that documents what minor gaps remain after major route-contract execution is achieved.

## Suggested intervention target

The gaps in this near-pass case suggest marginal improvements:

- `references/source-traceability-and-claim-citation.md` — add guidance for body-level inline citations even when a source list appendix exists
- `references/report-template.md` — add structural symmetry requirement for bull/bear case sections (same column format for both)
- `references/valuation-methodology.md` — add guidance for documenting valuation inference basis (multiple assumptions, comparable selection, scenario parameters)
- `checklists/final-audit.md` — add non-blocker checks: (1) bull/bear structural symmetry, (2) valuation inference includes explicit parameter documentation

These are lower priority than the anchor/label fixes suggested by `evals/cases/amat-listed-company-anchor-and-label-execution-case.md`.

## Reviewer checklist

- Are load-bearing claims traceable in the body (not just in the appendix source list)?
- Are bull and bear case sections structurally symmetric?
- Is the valuation range inference basis explicitly documented (multiples, comparables, parameters)?
- Are all hard-fail conditions passed?
- Is the research anchor block present and timely?

## Suggested scoring

- **Full pass**: body traceability present, bull/bear symmetry, transparent valuation inference
- **Near pass**: route contract satisfied but minor gaps in any of the above (this case's level)
- **Fail**: any hard-fail condition triggered or mandatory section missing

## Related evals

- `evals/cases/evergrande-property-listed-company-execution-case.md` — companion near-pass benchmark (恒大物业)
- `evals/cases/amat-listed-company-anchor-and-label-execution-case.md` — cluster failure (contrast case)
- `evals/cases/source-traceability-moore-threads-case.md` — source traceability failure
- `evals/cases/consensus-and-forward-pe-misuse-case.md` — forward PE/valuation misuse
