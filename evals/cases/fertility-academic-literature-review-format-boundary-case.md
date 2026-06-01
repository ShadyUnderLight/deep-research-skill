# Eval: 年轻人不生育 Academic / Literature Review Format Boundary Case

## Goal

Test whether an Academic / Literature Review route report using standard academic citation format `(Author, Year, Journal)` — which is functionally superior for academic readers — can still pass the source-traceability hard-fail gate, or whether the `[SN]` format requirement needs an academic-style carve-out.

This eval targets a format boundary failure:

- the report uses **(Author, Year, Journal)** inline citations — the universal standard in academic publishing
- this format is **more informative than `[SN]`** — a reader can immediately identify the source without cross-referencing an appendix
- but it **does not use `[SN]`/`[IN]`/`[UN]`** numbering, triggering the checklist hard-fail for format noncompliance
- the core question: **should the project's `[SN]` requirement override discipline-specific citation standards when the alternative format provides equivalent or better traceability?**

This continues the Round 2 pattern of **source traceability format boundary** cases:

| Case | Attribution format | Functional traceability | Project format compliance |
|------|-------------------|----------------------|--------------------------|
| AI Traffic Police | arXiv IDs | Partial (tech readers) | ❌ Noncompliant |
| 泡泡玛特 | Natural language prose | High (all readers) | ❌ Noncompliant |
| **This case** | **(Author, Year, Journal)** | **Highest (academic readers)** | ❌ Noncompliant |

## Real case pattern

A user-provided report "年轻人不生育多因素归因报告" (Multi-Factor Attribution of declining fertility among young adults) dated **2026-06-01** demonstrates this pattern:

**What was done well:**
- ✅ Academic / Literature Review route correctly selected
- ✅ 4-tier evidence labeling (确认事实/合理推断/推测/待验证) with conditional qualifiers throughout
- ✅ 7-chapter logical chain with 8 tables supporting judgment
- ✅ Counter-evidence present (alternative explanations discussed)
- ✅ Conditional weight quantitative estimation in §7 with scenario breakdown
- ✅ Policy implications clear and actionable
- ✅ Judgment-first opening

**What triggered the format concern:**
- ⚠️ **Source format noncompliant** — uses `(Author, Year, Journal)` inline citations, the universal standard in academic publishing. This is functionally superior to `[SN]` (a reader can immediately identify the source without cross-referencing an appendix). But it is format-noncompliant with the project's `[SN]` numbering requirement.

**What has gaps:**
- ❌ **Search strategy incomplete** — the report calls itself "有限范围系统化综述" (limited-scope systematic review) but lacks: database list, search terms, inclusion/exclusion criteria, screening count. This is a methodology documentation gap for the academic route.
- ❌ **Publication bias discussion insufficient** — methodology appendix mentions it but body text does not discuss the "file drawer problem" (publication bias toward positive results). For a multi-factor attribution topic with mixed evidence, this is a material gap.

## What this eval is testing

### Failure Mode 1: Academic citation format vs project [SN] requirement

The academic standard `(Author, Year, Journal)` is:
- More informative than `[SN]` (reader can identify source immediately)
- Universally recognized across academic disciplines
- Permanently resolvable (unlike arXiv IDs which may change)

Yet it triggers the project's source-traceability hard-fail because it doesn't use `[SN]` numbering.

This case raises the same question as the AI Traffic Police and 泡泡玛特 cases: **should functionally equivalent citation formats be accepted?**

The difference: academic `(Author, Year, Journal)` is arguably **better** than `[SN]` for readability — it eliminates the cross-referencing step entirely. A strict `[SN]`-only requirement would force academic reports to use a format that is **less useful** for their primary audience.

### Failure Mode 2: Search strategy documentation (academic route)

The academic route requires a documented search strategy. The report's "有限范围系统化综述" claim is not backed by:
- database list (PubMed? CNKI? Web of Science?)
- search terms and combinations
- inclusion/exclusion criteria
- screening flow (initial hits → screened → included)

This is a methodology transparency issue specific to the academic route.

### Failure Mode 3: Publication bias discussion

For a multi-factor attribution topic where null results (e.g., "factor X has no significant effect") are as informative as positive results, the absence of a publication bias discussion is a material gap.

## Pass criteria

A good academic literature review should:

1. **Citation format appropriate to discipline** — `(Author, Year, Journal)` is acceptable IF it provides equivalent or better traceability than `[SN]`; the register appendix should still cross-reference these citations structurally
2. **Search strategy documented** — database list, search terms, inclusion/exclusion criteria, screening numbers
3. **Publication bias discussed** — at minimum 2-3 sentences acknowledging file drawer problem and its impact on the evidence base
4. **Evidence tiering consistent** — labels applied to all load-bearing claims

## Failure signs

Mark this eval as **conditional pass** (not fail) if the answer:

- uses standard academic citation format `(Author, Year, Journal)` instead of `[SN]` — format noncompliant but functionally superior
- has incomplete search strategy documentation
- lacks publication bias discussion
- is otherwise a well-structured academic review (this case's level)

Mark as **fail** if the academic route hard-fail conditions are triggered (evidence hierarchy misuse, cherry-picking, preprint treated as peer-reviewed).

## Why this case exists

This case adds the **academic route** to the Round 2 source-traceability format boundary cluster, making it 3 cases across 3 route types:

| Case | Route | Citation format | Functional quality |
|------|-------|----------------|-------------------|
| AI Traffic Police | Technical Deep-dive | arXiv IDs | Medium |
| 泡泡玛特 | Listed Company | Natural language | High |
| **This case** | **Academic / Literature Review** | **(Author, Year, Journal)** | **Highest** |

Together, these 3 cases provide sufficient evidence to refine the `[SN]` hard-fail gate in the next fix cycle.

## Suggested intervention target

- `references/source-traceability-and-claim-citation.md` — add academic citation format carve-out: "(Author, Year, Journal/Blog) format satisfies the traceability requirement for the Academic / Literature Review route; [SN] numbering is recommended but not required for this route. Source register should still cross-reference these citations with structured entries."
- `references/academic-evidence-hierarchy.md` — add: search strategy documentation requirements (database list, search terms, inclusion/exclusion criteria, screening numbers); publication bias discussion requirements
- `checklists/source-traceability.md` — add note: "academic citation formats ((Author, Year)) are acceptable for the Academic route; for other routes, [SN] format is required"
- `evals/meta/rule-activation-and-execution-discipline.md` — add format-equivalence as a consideration in the missing-trigger vs execution-failure diagnosis (if the format is functionally equivalent, it's not an execution failure)

## Reviewer checklist

- Is the citation format appropriate for the route type?
- Does the citation format provide functional traceability (can reader find the source)?
- Is the search strategy documented (database, terms, criteria)?
- Is publication bias discussed?
- Is the evidence tiering consistent?
- Are load-bearing claims auditable?

## Scoring

- **Full pass**: search strategy documented, publication bias discussed, evidence tiering consistent, citations functionally traceable
- **Conditional pass**: strong content but search strategy missing + publication bias not discussed + citation format noncompliant (this case's level)
- **Fail**: academic route hard-fail triggered

## Related evals

- `evals/cases/ai-traffic-police-technical-deep-dive-traceability-case.md` — format boundary: arXiv IDs vs [SN]
- `evals/cases/pop-mart-listed-company-traceability-hard-fail-case.md` — format boundary: natural language vs [SN]
- `evals/cases/academic-route-activation-transformer-origin-case.md` — academic route activation (companion)
