# Eval: Scope Completeness Discipline

Use this eval when a report claims broad scope (global / comprehensive / industry-wide / full landscape) but may omit one or more load-bearing markets, geographies, segments, or regulatory regimes.

This is a meta-eval. It is not primarily about whether the report's individual facts are correct. It is about whether the actual coverage matches the implied scope, and whether a scope miss could distort the conclusion.

## Goal

Distinguish four different failure types:

1. **Name-only global coverage** — the report says "global" but effectively covers only the easiest or most visible markets
2. **Missing load-bearing geography** — a geography that materially affects market size, supply chain, competition, or policy risk is missing or dismissed in one sentence
3. **Flat competitive map** — the report lists global players but does not distinguish regional champions, incumbents vs emerging local challengers, or geography-dependent competitive dynamics
4. **Scope boundaries not stated** — the report is actually a partial-scope memo, but it does not say so, creating false confidence in the reader

This distinction matters because these four problems require different fixes (missing data, routing misclassification, template omission, or execution failure).

---

## Typical cases where this eval should be used

- global market report that effectively ignores a top-5 geography
- competitive map missing a major local player set
- regulatory analysis that only covers US/EU but not the most constraining regime
- value-chain report that names all layers but skips the highest-friction or highest-value segment
- industry landscape that looks broad but is concentrated on the most visible areas

---

## What this eval is testing

### Failure Mode 1: Name-only global coverage

The report says "global" but effectively covers only the easiest or most visible markets.

Examples:
- mostly US + Europe with little or no China
- mostly public Western vendors while local leaders in Asia are absent
- regulatory discussion centered on one regime while other binding regimes are ignored

### Failure Mode 2: Missing load-bearing geography

A geography that materially affects market size, supply chain, competition, or policy risk is missing or dismissed in one sentence.

Examples:
- the largest demand pool is barely covered
- the most restrictive regulator is omitted
- a key manufacturing region is absent from the supply-side analysis

### Failure Mode 3: Flat competitive map

The report lists global players but does not distinguish:
- regional champions from global leaders
- incumbents from emerging local challengers
- where the competitive picture changes by geography

### Failure Mode 4: Scope boundaries not stated

The report is actually a partial-scope memo, but it does not say so.

This creates false confidence because the reader assumes comprehensiveness.

---

## Pass criteria

A good answer should:

1. **State the real scope clearly.**
   - if the report is truly global, it should behave globally
   - if it is partial, it should say what is excluded

2. **Cover load-bearing geographies.**
   - include the top markets or most consequential geographies for demand, supply, or regulation
   - do not reduce a key geography to a passing mention

3. **Explain why geography changes the conclusion.**
   - show where market structure, regulation, pricing, or competition differ by region
   - do not treat global market conclusions as geography-free by default

4. **Handle competitive scope honestly.**
   - include regional leaders when they materially shape the market
   - distinguish global leaders from region-specific leaders when needed

5. **Make omissions explicit when evidence is weak.**
   - if some markets are poorly documented, say so
   - do not silently downgrade them into irrelevance

---

## Scoring guide

Use a simple 0-2 scale.

### 0 = scope failure
- one or more load-bearing markets or segments are missing
- or the report is functionally regional while presenting itself as global
- or scope boundaries are unstated, creating false confidence

### 1 = partial scope discipline
- the main geographies are present, but one important region/segment is underdeveloped
- or coverage exists without showing how geography changes the analysis
- or scope boundaries are implied but not explicit

### 2 = strong scope completeness
- the report covers the consequential geographies/segments, states its boundaries honestly, and shows how scope affects conclusions

---

## Review questions

When using this eval, ask:

- What are the top geographies or segments that could materially change the answer?
- Did the report cover them proportionally to their importance?
- Did it distinguish demand centers, supply centers, and regulatory centers?
- Did it include local leaders where they matter?
- If some major geography is thin, did the report explain why?
- Would a different conclusion be possible if a missing geography were included?
- Is the right fix a new rule, a stronger route trigger, a checklist gate, or a new case eval?

---

## Output format for reviewers

When you apply this eval, summarize the result as:

- **Implied scope:**
- **Actual coverage:**
- **Load-bearing omissions:**
- **Scope boundaries stated?**
- **Diagnosis:** name-only global / missing load-bearing geography / flat competitive map / boundaries not stated / no failure
- **Best next fix:** routing update / reference update / checklist update / new case eval only / no action

---

## Suggested prompts

- Research the global HNB market and compare major geographies, players, and regulatory constraints.
- Map the global AI datacenter value chain and explain where value accrues by region.
- Analyze the global EV battery market, including China, Europe, the US, Korea, and Japan.
- Compare global cloud security vendors, noting where regional regulation changes adoption dynamics.

---

## Related files

- `evals/cases/global-market-scope-completeness-case.md` — concrete case example for this family
- `references/failure-taxonomy.md` — Family F: Scope Completeness and Coverage Geometry
- `ROUTING-MATRIX.md` — cross-cutting discipline: scope completeness

---

## Why this eval exists

Several reports can look broad while still being structurally incomplete.

This eval exists to prevent "global" from becoming a stylistic label instead of a real coverage standard, and to ensure that scope completeness is explicitly evaluated as a cross-cutting discipline rather than assumed by default.
