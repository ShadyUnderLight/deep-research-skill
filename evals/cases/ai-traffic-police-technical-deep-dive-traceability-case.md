# Eval: AI Traffic Police Technical Deep-Dive Source Traceability Format-Boundary Case

## Goal

Test whether a Technical Deep-dive / Architecture Analysis report with complete appendix source list (S01-S27) handles non-standard inline citation formats (arXiv IDs, paper names) under the current source-traceability format-equivalence rule.

This eval targets a failure mode where:

- the report has a **complete, well-structured source list** in the appendix
- the body uses **partial inline references** (arXiv IDs, paper names) — which is better than nothing
- **Historical verdict**: this was originally treated as a source-traceability hard-fail because the body did not use the appendix `[SN]` IDs
- **Current rule verdict**: arXiv IDs or DOI references can be a conditional pass if they uniquely map to structured Source Register entries; they fail only when the mapping is absent or ambiguous
- **Current eval target**: distinguish format-boundary conditional pass from true zero-body-traceability failures

This is distinct from previous source-traceability cases:

| Case | Source traceability issue |
|------|--------------------------|
| Moore Threads | No sourcing at all |
| 中际旭创 | Inconsistent inline citations |
| 人形机器人 | Bibliography exists but zero body traceability |
| **This case** | Body has partial citations (arXiv IDs) but not `[SN]` format — conditional pass if those citations map to structured register entries |

## Real case pattern

A user-provided AI Traffic Police report (AI 在交警电子警察违章图片审核中的应用研究报告) dated **2026-05-31** demonstrates this pattern:

**What was done well:**
- ✅ Technical Deep-dive route correctly selected and executed
- ✅ Complete structured source list (S01-S27) with type, date, relevance annotations
- ✅ Inference register (I01-I04) and uncertainty register (U01-U08)
- ✅ Evidence labeling consistent throughout (✅/🔶/❓ icons for Confirmed/Likely/Unknown)
- ✅ All 7 quality gates passed
- ✅ Multi-dimensional comparison tables (7 dimensions for edge vs cloud, 6 dimensions for model comparison)
- ✅ TRL maturity assessment per violation type (§2.1)
- ✅ Counter-evidence chapter (§7.5)
- ✅ Uncertainty summary with 7 data gaps + 5 legal gray zones (§9)
- ✅ Clear multi-timescale judgment (short/medium/long term, §10)
- ✅ Judgment-first opening (6 core conclusions in executive summary, no background-first drift)

**Historical source-traceability concern:**
- ⚠️ **Format-boundary concern** — body uses arXiv IDs (e.g., `arXiv:1911.00927`) and paper names instead of `[S01]`-format structured inline references. Under the current rule, this is not automatically a hard-fail: it is conditional pass if the identifiers uniquely map to Source Register entries, and fail only if the mapping is missing or ambiguous.

**What has minor gaps:**
- ⚠️ **Route planning (announced vs shipped)** — LLM integration cited from FT report (§4.3) describes an announced product integration, but is not explicitly labeled as "announced / not yet deployed at scale"
- ⚠️ **Vendor revenue data freshness** — Hikvision ($13B/2021) and Dahua ($5B/2021) revenue data from Wikipedia is ~5 years old, not annotated with a staleness notice

## What this eval is testing

### Failure Mode 1: Non-standard inline citations as a format boundary

The report uses arXiv IDs and paper names as inline references — this is a legitimate form of citation in academic contexts. The current `source-traceability.md` checklist treats arXiv IDs / DOI references as functionally equivalent inline citations when they uniquely map to structured register entries.

This is a **format-boundary case**: the content is there, the traceability exists in principle, but reviewers must verify that the non-`[SN]` citations map cleanly to the appendix source entries.

The lesson: **having source information in the body (arXiv IDs, paper names) can satisfy the hard-fail gate conditionally, but full pass still requires structured `[SN]` citations or an equally unambiguous register mapping.**

### Failure Mode 2: Announced vs shipped separation in Technical Deep-dive

The Technical Deep-dive route requires separating "announced" from "shipped/delivered" in roadmap/route-planning sections. The LLM integration claim (§4.3, citing a FT report) is an announced product feature, but is not explicitly labeled as such. This is a hard-fail condition for the Technical Deep-dive route.

### Failure Mode 3: Subsidiary content not labeled as subsidiary route

The report covers three route types (Technical Deep-dive primary + Provider Selection + Regulatory as secondary content). The provider analysis (§4) and regulatory analysis (§8) are legitimate given the user's request, but they are not explicitly labeled as sub-sections belonging to different route families.

## Pass criteria

A good answer should:

1. **Structured inline citations in `[SN]` format for full pass** — body text references appendix source IDs (S01-S27), or non-`[SN]` citations uniquely map to register entries for conditional pass
2. **Announced vs shipped separated** — roadmap/route-planning claims explicitly labeled as "announced" vs "shipped/delivered" vs "rumored/speculative"
3. **Data freshness annotations** — data older than 2 years from report date has a staleness notice
4. **Multi-route content labeled** — if non-primary-route content is included (provider analysis, regulatory), it is explicitly labeled as belonging to a different route family

## Failure signs

Mark this eval as failed if the answer:

- has a complete appendix source list (S01-S27) but no body-level source references of any kind
- has arXiv IDs or paper names in the body that cannot be uniquely mapped to structured Source Register entries
- fails to separate announced vs shipped in roadmap/route-planning sections
- uses vendor or market data 2+ years old without a staleness annotation

## Why this case exists

This case adds coverage for a distinct source-traceability failure mode: **non-standard inline citations**. Previous cases covered:

| Case | Issue | Severity |
|------|-------|----------|
| `source-traceability-moore-threads-case.md` | No sourcing at all | 🔴 |
| `innolight-listed-company-execution-case.md` | Inconsistent body citations | 🟡 |
| `humanoid-robot-market-outlook-dual-route-case.md` | Bibliography but zero body traceability | 🔴 |
| `storage-chip-listed-company-deep-dive-pass-case.md` | Pass-level: no inline citations but other quality high | ✅ |
| **This case** | Body has arXiv citations but not `[SN]` format — conditional pass if mapped to structured register entries | ⚠️ |

This case documents a **borderline**: the report's traceability is better than the 人形机器人 case (which had zero body citations), but less structured than a clean `[SN]` implementation. It should now be judged by functional traceability rather than `[SN]` format alone.

The case records why the `[SN]` format requirement was refined to allow non-standard citations when they provide equivalent or better traceability (arXiv IDs are globally unique and permanently resolvable).

## Suggested intervention target

- `references/source-traceability-and-claim-citation.md` — preserve the current format-equivalence rule for arXiv IDs / DOI / paper names with dates, while requiring unique mapping to structured register entries
- `checklists/source-traceability.md` — keep the conditional-pass distinction between equivalent inline formats and true zero-body-traceability failures
- `checklists/technical-analysis-audit.md` — add non-blocker: "announced vs shipped separation for roadmap claims"
- `references/technical-analysis-discipline.md` — add guidance for multi-route labeling when non-primary content is included

## Reviewer checklist

- Does the body use `[SN]`-format inline citations referencing the appendix source list?
- If non-standard citations (arXiv IDs, DOI) are used, are they also indexed in the appendix source list?
- Are announced product features explicitly separated from shipped/delivered ones?
- Is vendor/market data older than 2 years annotated with staleness notice?
- Are non-primary-route content sections labeled as belonging to a different route family?

## Suggested scoring

- **Full pass**: `[SN]` inline citations present, announced vs shipped separated, fresh data, multi-route labeled
- **Conditional pass**: source list exists, body has equivalent citations (arXiv IDs) but not `[SN]` format; announced/shipped mostly separated (this case's level)
- **Fail**: no body-level source references, or equivalent references cannot be mapped to the register

## Related evals

- `evals/cases/humanoid-robot-market-outlook-dual-route-case.md` — bibliography but zero body traceability (worse)
- `evals/cases/storage-chip-listed-company-deep-dive-pass-case.md` — pass-level: evidence labels in body but no `[SN]` cites (better)
- `evals/cases/innolight-listed-company-execution-case.md` — inconsistent body citations
- `evals/cases/source-traceability-moore-threads-case.md` — no sourcing at all (worst)
