# Eval: TikTok AI Technical Deep-Dive Route Inflation Case

## Goal

Test whether a Technical Deep-dive / Architecture Analysis report can resist **route declaration inflation** — the tendency to declare multiple secondary routes (market outlook, provider comparison, compliance) without checking their hard-fail conditions, resulting in an output that behaves like a shared-workflow comprehensive survey rather than a focused technical analysis.

This eval targets a failure mode where:

- the primary route (Technical Deep-dive) is correctly identified and mostly executed
- 3+ secondary routes are declared but **none of their hard-fail conditions are checked**
- the combined scope of secondary routes exceeds the primary route's "minimize" allowance (tool comparison + compliance + ROI = ~35% of body text)
- the result reads as a comprehensive industry survey rather than a focused technical deep-dive

This is distinct from previous route-level failures:

| Case | Route problem |
|------|--------------|
| 欧冠决赛 | Route **not activated** (shared-workflow mode) |
| 世界杯 | Route **wrongly selected** (Market Outlook → Constrained Choice) |
| 人形机器人 | Dual-route: primary correct, **secondary unchecked** |
| **This case** | Route **declaration inflation**: 4 routes declared, output = shared-workflow survey |

## Real case pattern

A user-provided report "AI 在 TikTok 直播自动化中控中的应用" dated **2026-06-01** demonstrates this pattern:

**What was done well:**
- ✅ **Strongest source traceability seen across all evals** — 42 `[SN]` inline citations, structured source register with 6 columns (type/date/relevance/notes), consistently used in body text. Validates the #145 fix is working.
- ✅ Technical deep-dive core sections strong (六层架构 + 算法拆解 + TTS/NeRF/NLP deep dives)
- ✅ Evidence labeling consistent ([确认事实]/[推断]/[未知]) throughout
- ✅ Judgment-first opening with 7 evidence-tagged bullets
- ✅ All quality gates passed
- ✅ Multi-dimensional comparison tables with explicit dimensions
- ✅ TRL-like maturity model (三代数字人 + L0-L4 stages)
- ✅ Counter-evidence present (§9 牛熊对称分析)
- ✅ Actionable recommendations by GMV segment (§11.2)

**What was wrong:**
- ❌ **Route declaration inflation** — declared 4 routes (Technical Deep-dive primary + Market Outlook + Provider Comparison + Compliance Analysis secondary), but actual output is a comprehensive industry survey. All 3 secondary routes' hard-fail conditions were unchecked.
- ❌ **Provider Selection hard-fail triggered** — §4 (工具对比) behaves as vendor overview rather than choice memo; no ranked shortlist, no selection criteria explicated.
- ❌ **Feasibility assessment missing conclusion** — Technical Deep-dive artifact contract requires a clear "feasible / conditionally feasible / not feasible" conclusion sentence. The report documents constraints (§7) but never syntheses them into a yes/no answer.
- ❌ **Vendor claim labeling inconsistency** — S19 (YY 开播 "峰值稳定性提升58%") and S40 (阿里云 "成本降70%") are tagged as "厂商自述" in the Source Register but as [确认事实] or [推断] in the body text. The reader sees a stronger confidence level than the register supports.
- ❌ **Forward-looking claims missing assumptions** — L0-L4 stages (§8.3) predict timelines ("L3预计2026H2-2027") without stating the dependency conditions ("if model X reaches capability Y by date Z") or failure triggers.

## What this eval is testing

### Failure Mode 1: Route declaration inflation

Declaring multiple routes without checking each one's hard-fail conditions creates a "false precision" problem: the report appears to be executing a structured methodology, but the actual quality control is only running for the primary route. The secondary routes' hard-fails leak through undetected.

The specific pattern: **the report declares 4 routes but delivers 1 shared-workflow survey**. The most honest declaration would be shared-workflow with technical-analysis emphasis.

### Failure Mode 2: Feasibility conclusion omission

The Technical Deep-dive artifact contract requires a clear feasibility conclusion ("feasible / conditionally feasible / not feasible"). The report provides extensive constraint documentation but never closes the loop with a summary judgment. This is a mandatory-section gap.

### Failure Mode 3: Vendor claim labeling inconsistency

Same pattern as the AI Traffic Police case (Round 2 case #1): Source Register labels a claim as "manufacturer self-reported" but the body text uses a higher confidence label ([确认事实] or [推断] without the "self-reported" caveat). The reader cannot see the register's qualification. This is a recurring pattern in Round 2.

### Failure Mode 4: Forward-looking claims without dependency conditions

The L0-L4 roadmap predicts timelines without stating what must be true for each stage to materialize. This is a forward-looking discipline gap.

## Pass criteria

A good answer should:

1. **Route declaration discipline** — if declaring 4 routes, verify each route's hard-fail conditions; if the output is a comprehensive survey, declare as shared-workflow rather than inflating the route list
2. **Feasibility conclusion present** — technical deep-dive must end with a clear "feasible / conditionally feasible / not feasible" summary
3. **Vendor claim labeling consistent** — if Source Register says "manufacturer self-reported", body text must also say so (inline caveat, not just register metadata)
4. **Forward-looking dependency conditions** — each predicted timeline must state the assumption ("if X reaches Y") and the failure trigger ("if Z does not happen by date W")
5. **Minimize discipline** — secondary-route content (tools, compliance, ROI) does not exceed 20% of body text when primary route is Technical Deep-dive

## Failure signs

Mark this eval as **partial pass** (not fail) if the answer:

- declares 3+ secondary routes without checking any of their hard-fail conditions (route inflation)
- has source register labeling "manufacturer self-reported" but body text does not repeat the caveat
- misses the feasibility conclusion for a technical deep-dive
- has forward-looking timelines without dependency conditions
- still has strong source traceability and evidence labeling

Mark as **fail** if the primary route itself is misidentified or its hard-fail conditions are triggered.

## Why this case exists

This case adds coverage for **route declaration inflation**, a pattern not previously documented. It also shows that the #145 source traceability fix is working (this case has the best `[SN]` discipline seen so far), confirming the Round 1 batch fix had real impact.

| Gap | Existing coverage | This case adds |
|-----|-------------------|----------------|
| **Route declaration inflation** | Not covered | Declaring 4 routes but delivering shared-workflow survey |
| **Vendor claim labeling** | AI traffic police case has same issue | Recurring pattern: register vs body inconsistency |
| **Feasibility conclusion** | Not explicitly covered | Mandatory section omission in technical deep-dive |

## Suggested intervention target

- `ROUTING-MATRIX.md` — add a hard-fail or strong warning: "if declaring 2+ secondary routes, each must have its hard-fail conditions checked before delivery; unchecked secondary routes constitute route inflation"
- `references/route-activation-and-preflight.md` — add "route inflation check" step: count declared secondary routes; if >2, verify that total scope is still focused; consider shared-workflow declaration instead
- `checklists/technical-analysis-audit.md` — add mandatory check: "feasibility assessment includes a clear conclusion sentence (feasible / conditionally feasible / not feasible)"
- `checklists/final-audit.md` — add non-blocker: "Source Register labeling and body text labeling are consistent for manufacturer-claimed data points"
- `references/source-traceability-and-claim-citation.md` — add: "when a source is labeled 'manufacturer self-reported' in the register, the body text must include an inline caveat"

(**Note**: the vendor claim labeling issue is a shared pattern with `evals/cases/ai-traffic-police-technical-deep-dive-traceability-case.md` — these two cases together make a stronger case for fixing the register-to-body labeling pipeline.)

## Reviewer checklist

- Is the declared route list appropriate for the actual output, or inflated?
- If secondary routes are declared, are their hard-fail conditions checked?
- Does the technical deep-dive have a clear feasibility conclusion?
- Are vendor claims labeled consistently between Source Register and body text?
- Do forward-looking claims have dependency conditions and failure triggers?

## Suggested scoring

- **Full pass**: route list matches output, all hard-fails checked, feasibility conclusion present, consistent labeling
- **Conditional pass**: strong content but route inflation + feasibility conclusion missing (this case's level)
- **Fail**: primary route hard-fail triggered

## Related evals

- `evals/cases/ai-traffic-police-technical-deep-dive-traceability-case.md` — companion case: same route family (Technical Deep-dive), same vendor claim labeling issue
- `evals/cases/humanoid-robot-market-outlook-dual-route-case.md` — dual-route with secondary unchecked (similar pattern, different route family)
- `evals/cases/champions-league-constrained-choice-activation-case.md` — route not activated (contrast: inflation vs non-activation)
