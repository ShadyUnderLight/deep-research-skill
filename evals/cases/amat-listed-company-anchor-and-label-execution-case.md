# Eval: AMAT Listed-Company Anchor and Evidence-Label Execution Case

## Goal

Test whether a listed-company / investment-style deep-research report can simultaneously:

- miss the required **research anchor block** (explicit time-layer locking before broad analysis)
- miss the **market snapshot** hard gate (no complete current valuation snapshot)
- overuse **"confirmed fact" evidence labels** for claims that are actually inferences or third-party assertions
- default to **background-first opening** (evidence grading explanation occupies first-screen position instead of judgment)

This eval targets a recurring cluster failure: a report that looks structured (route declaration, evidence labels, organized sections) but still fails the listed-company route's core artifact contract.

## Real failure pattern

A user-provided AMAT report dated **2026-05-29** (Applied Materials deep research) demonstrates this cluster:

**What was present:**
- explicit route declaration ("研究路线：上市公司/投资风格研究")
- evidence grading labels (确认事实 / 合理推断 / 未知)
- organized chapters (business, financials, competition, risks, outlook)
- many real financial figures
- readable formatting

**What was missing:**
- **Research anchor block** — no explicit lock of latest full-year, latest quarter, latest market snapshot date, latest management state. The reader cannot verify whether financial numbers are anchored on the newest reporting layers.
- **Market snapshot** — no share price, market cap, PE TTM/Forward, PB, PS, 52-week range, or snapshot date. This is a listed-company route hard-fail condition.
- **Judgment-first opening** — the first visible content is an evidence-grading explanation block, not the core thesis. The reader must scroll past grading boilerplate before reaching any judgment.

**What was incorrect:**
- **"Confirmed fact" label overuse** — market-position claims such as "全球最大的半导体设备制造商" (world's largest semiconductor equipment manufacturer) were labeled as confirmed facts, when they are actually third-party-asserted rankings. Other inferred statements were similarly over-labeled.
- **Market position claims without scope** — "领导者", "最广泛" appeared without specifying metric, time window, or source basis.

**Why this cluster matters:**
Each of these failures individually would be moderate. Together they reveal that the report's execution contract is not being reliably followed even when the route is explicitly declared.

## What this eval is testing

### Failure Mode 1: Missing research anchor block

The report proceeds into business description, competitive analysis, and financial review without first explicitly locking:

- latest full-year reported period
- latest quarterly / interim reported period
- latest current market snapshot date (price, valuation)
- latest management / leadership state when decision-relevant

This is different from the stale-anchor failure in `evals/cases/intel-current-state-freshness-case.md`. In that case, the anchor existed but was stale. In this case, the anchor is simply **absent** — the report never declares what its time layers are.

### Failure Mode 2: Missing market snapshot hard gate

The listed-company route in ROUTING-MATRIX.md requires a current market snapshot. The report lacks:

- current share price and date
- market capitalization
- PE (TTM and/or Forward)
- PB, PS or other relevant multiples
- 52-week price range
- snapshot date visible at the valuation reference point

This is a route-specific hard-fail condition.

### Failure Mode 3: Evidence-label overuse (inflation)

The report uses a three-tier evidence label system (确认事实 / 合理推断 / 未知). But:

- market position claims labeled as "确认事实" are actually inferences or third-party synthesized rankings
- the strongest label ("confirmed fact") is applied to claims that should be downgraded to "合理推断" or labeled with explicit scope caveats
- the label system creates false confidence because the reader trusts the label but cannot verify the underlying evidence

This is a distinct failure from "no evidence labels" (covered elsewhere) or "missing labels on estimates" (covered in forward-looking evals). It is **label inflation** — the system exists but is applied with insufficient strictness.

### Failure Mode 4: Background-first opening

The opening screen position is occupied by:

- an evidence-grading explanation block
- methodology notes
- boilerplate scope statements

rather than:

- the core judgment (buy / sell / hold thesis)
- the key unresolved variable
- the strongest weakening evidence

This violates the "judgment-first opening" principle. Unlike the overview-shape persistence documented in `evals/meta/listed-company-judgment-memo-execution-family.md`, this case is more specific: it is not that the opening is generic background, but that **a structural requirement (evidence grading)** displaced the judgment in the first-screen real estate.

### Failure Mode 5: Market position claims without scope

"全球最大", "行业领导者", "最广泛的产品组合" appear without:

- explicit metric (revenue, market share %, unit volume, R&D spend?)
- explicit time window (FY2025 calendar year? trailing 12 months?)
- explicit source attribution
- conditional clause (e.g., "按收入计" / "据Gartner 2026年3月数据" / "在XX细分领域")

## Pass criteria

A good answer should:

1. **Include a research anchor block** early in the report (before or as part of the opening) that explicitly states:
   - latest full-year reported period
   - latest quarterly / interim reported period
   - latest market snapshot date and key valuation metrics
   - latest management/leadership state when decision-relevant

2. **Include a complete market snapshot** as part of the listed-company execution contract:
   - current share price with date
   - market capitalization
   - PE (TTM and Forward)
   - additional multiples as relevant (PB, PS, EV/EBITDA)
   - 52-week range
   - snapshot date visible

3. **Open with judgment, not boilerplate**:
   - core thesis visible in first 10-15 seconds of reading
   - evidence grading, methodology, or scope notes placed after the judgment, not before it
   - the first screen real estate is occupied by what changes the reader's view

4. **Apply evidence labels accurately**:
   - "confirmed fact" only for directly verifiable primary-source claims
   - market position rankings labeled as "inference" or "third-party assertion" with scope caveats
   - no label inflation that creates false confidence

5. **Scope every market-position claim**:
   - each "largest", "leader", "best", "most" specifies metric, time window, and source
   - each strong claim includes a conditional clause or explicit dependency

## Failure signs

Mark this eval as failed if the answer does **any** of the following:

- proceeds into business/strategy/financial analysis without an explicit research anchor block
- lacks a complete current market snapshot (price, market cap, multiples, date)
- places evidence-grading explanation or methodology notes before the core judgment on first screen
- labels market-position inferences or third-party ranking claims as "confirmed fact"
- uses "largest", "leader", "most" without specifying scope (metric, time, source)
- includes "confirmed fact" labels for claims that are clearly inferences or secondary-sourced rankings

## Why this case exists

Existing listed-company evals cover:

- **stale anchors** (`intel-current-state-freshness-case.md`) — anchor exists but is stale
- **freshness of individual facts** (`freshness-xiaomi-case.md`) — stale facts presented as current
- **judgment-shape failure** (`cnooc-judgment-shape-improved-but-freshness-still-leaked-case.md`) — overview shape persists
- **judgment-memo execution family** (`evals/meta/listed-company-judgment-memo-execution-family.md`) — the broader family

This case adds coverage for:

- **missing anchor** (not stale, just absent) — a different failure mode from stale-anchor
- **evidence-label inflation** — labels exist but are applied too confidently
- **background-first displacement by structural requirement** — not just overview drift, but a mandatory feature (grading labels) accidentally competing with judgment-first opening

These are gaps in the current eval coverage that affect real report quality.

## Suggested intervention target

This case should push changes at multiple layers:

- `references/report-template.md` — add research anchor block as a mandatory opening element before evidence labels
- `checklists/listed-company-report.md` — add explicit check for "evidence labels not inflating claim strength" and "research anchor block present before business analysis"
- `checklists/final-audit.md` — add first-screen real-estate audit (is judgment visible before boilerplate/notes?)
- `ROUTING-MATRIX.md` — verify that listed-company route hard-fail conditions explicitly include "market snapshot present and dated"
- `evals/meta/rule-activation-and-execution-discipline.md` — this case may show a new sub-pattern: "partial activation with label inflation" where the rule fires (labels used) but execution is worse than no labels because the labels create false confidence

## Reviewer checklist

- Did the report include an explicit research anchor block (FY, quarter, snapshot date, mgmt state)?
- Was the market snapshot complete (price, cap, multiples, range, date)?
- Did judgment appear on first screen before evidence grading or methodology notes?
- Were "confirmed fact" labels used accurately, or inflated for third-party/inferred claims?
- Did every "largest"/"leader"/"most" claim specify metric, time window, and source?
- Could a skeptical reviewer trust the evidence labels without re-verifying each claim?

## Suggested scoring

- **Pass**: research anchor block present, market snapshot present, judgment-first opening, labels accurate, all strong claims scoped
- **Partial**: some anchor or snapshot present but incomplete; labels mostly accurate but one or two inflated; judgment visible but not on first screen
- **Fail**: missing anchor block OR missing market snapshot OR label inflation materially misleads OR judgment displaced by boilerplate on first screen

## Related evals

- `evals/cases/intel-current-state-freshness-case.md` — stale-anchor failure (this case: missing anchor, not stale anchor)
- `evals/cases/freshness-xiaomi-case.md` — freshness and date discipline
- `evals/cases/cnooc-judgment-shape-improved-but-freshness-still-leaked-case.md` — judgment-shape persistence
- `evals/meta/listed-company-judgment-memo-execution-family.md` — broader execution family diagnosis
- `evals/meta/rule-activation-and-execution-discipline.md` — rule activation diagnostic (labels exist but inflated = partial activation with negative execution quality)
