# Eval: Market Entry Two-Level Decision Funnel and Country Diligence Card Case

**Related issue:** #328

## Goal

Test whether a Market Entry / Regional Expansion report that correctly separates regional hub / first revenue beachhead / later expansion roles and uses a unified comparison unit can still **fail** when:

- **Two-level decision funnel absent** — the report jumps from regional winner directly to beachhead without evaluating 2-3 realistic country candidates within the winning region
- **Country Diligence Card absent** — countries are evaluated in free-form prose without consistent diligence fields or evidence-role labels
- **Recommendation-constraint mismatch** — the report's own estimates (e.g., 18-24 month entry timeline) contradict the recommendation label (e.g., GO with 6-month revenue requirement)
- **Sensitivity / switching table absent** — the beachhead recommendation depends on load-bearing assumptions (growth, ARPU, localization cost) that are not stress-tested with explicit switching conditions

This eval complements existing market-entry evals:
- `evals/cases/ai-edu-market-entry-sensitivity-and-route-intersection-case.md` — tests sensitivity, traceability, quantitative roles
- `evals/cases/ai-saas-market-entry-traceability-case.md` — tests traceability
- `evals/cases/nev-parts-europe-market-entry-quantitative-role-case.md` — tests quantitative role labeling

## Prompt

A Chinese AI education product company has completed initial market research and identified Southeast Asia as the preferred expansion region. Produce a market-entry decision memo that:

- identifies the specific beachhead country within Southeast Asia
- justifies why this country over other realistic candidates (minimum 2-3 within the region must be evaluated)
- uses a consistent diligence framework across all candidates
- labels GO / Pilot Only / Not Now for each country
- checks that the recommendation is consistent with estimated timeline, budget, and team constraints
- includes a sensitivity/switching table for load-bearing assumptions
- applies role labels (observed / proxy / assumption / model-output) to diligence numbers
- uses `[Sxx]` inline citations
- includes a complete 7-column Source Register

## What this eval is testing

- whether the report applies a two-level funnel: regional screening → country competition
- whether each candidate country uses a Country Diligence Card with consistent fields and evidence roles
- whether the recommendation label (GO/Pilot/Not Now) is checked against the report's own constraint estimates
- whether load-bearing assumptions have sensitivity/switching analysis

## Pass criteria

A passing answer should:

1. **Explicitly separate regional screening from country competition.** The report must show why SEA (not Japan, Middle East, or India) wins at the regional level, and then within SEA compete at least 2-3 specific countries.

2. **Use Country Diligence Card on each candidate.** Each country gets a diligence card with at least these fields: target customer/payer, first-revenue path, localization depth, regulatory/data status, competitive landscape, entry motion, cost and timeline. Each field has an evidence role label.

3. **Check recommendation-constraint consistency.** If the report says "entry requires 12-18 months to set up entity, hire team, localize product, and obtain licenses", a country labelled GO must not require revenue within 6 months. If the budget is $200K and estimated entry cost is $350K, no country can be labelled GO.

4. **Include sensitivity/switching table.** At least 3 variables tested with: current assumption, change direction, new beachhead, trigger threshold.

5. **Label numeric roles.** All key numbers (market size, ARPU, CAC, localization cost, timeline) carry observed/proxy/assumption/model-output labels.

## Failure signs

- ❌ Only one country evaluated within the winning region → hard-fail (two-level funnel absent)
- ❌ Country analysis is free-form prose without consistent diligence fields → hard-fail
- ❌ Recommendation label contradicts report's own estimates (timeline, budget, capacity) → hard-fail
- ❌ No sensitivity/switching table despite load-bearing assumptions → hard-fail
- ❌ Missing role labels on key numbers → hard-fail

## Scoring

- **Full Pass**: two-level funnel + diligence cards + constraint consistency + sensitivity table + role labels + traceability
- **Conditional Pass**: funnel and diligence present but sensitivity or constraint-consistency weak
- **Fail**: any hard-fail triggered

## Related evals

- `evals/cases/ai-edu-market-entry-sensitivity-and-route-intersection-case.md`
- `evals/cases/ai-saas-market-entry-traceability-case.md`
- `evals/cases/nev-parts-europe-market-entry-quantitative-role-case.md`
