# Eval: Global Market Scope Completeness Case

Use this eval for industry, market, or landscape reports that claim broad scope (global / comprehensive / industry-wide / full landscape) but may omit one or more load-bearing markets, geographies, or segments.

## Goal

Test whether the report's actual coverage matches its implied scope.

A report can have many correct facts and still be misleading if it omits a geography, segment, or regulatory regime that materially changes the conclusion.

---

## Prompt

Research the global [industry/market] landscape and explain:

- market size and growth drivers
- key geographies
- major competitors
- regulatory or policy constraints
- what matters most over the next 12-24 months

Write the report for a reader who needs a decision-useful global view, not a regional summary disguised as a global report.

---

## What this eval is testing

### Failure Mode 1: Name-only global coverage

The report says "global" but effectively covers only the easiest or most visible markets.

Typical examples:
- mostly US + Europe with little or no China
- mostly public Western vendors while local leaders in Asia are absent
- regulatory discussion centered on one regime while other binding regimes are ignored

### Failure Mode 2: Missing load-bearing geography

A geography that materially affects market size, supply chain, competition, or policy risk is missing or dismissed in one sentence.

Typical examples:
- the largest demand pool is barely covered
- the most restrictive regulator is omitted
- a key manufacturing region is absent from the supply-side analysis

### Failure Mode 3: Flat competitive map

The report lists global players but does not distinguish:

- regional champions
- incumbents vs emerging local challengers
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

Use a 0-2 scale.

### 0 = scope failure
- one or more load-bearing markets or segments are missing
- or the report is functionally regional while presenting itself as global

### 1 = partial scope discipline
- the main geographies are present, but one important region/segment is underdeveloped
- or coverage exists without showing how geography changes the analysis

### 2 = strong scope completeness
- the report covers the consequential geographies/segments, states its boundaries honestly, and shows how scope affects conclusions

---

## Review questions

- What are the top geographies or segments that could materially change the answer?
- Did the report cover them proportionally to their importance?
- Did it distinguish demand centers, supply centers, and regulatory centers?
- Did it include local leaders where they matter?
- If some major geography is thin, did the report explain why?

---

## Suggested prompts

- Research the global HNB market and compare major geographies, players, and regulatory constraints.
- Map the global AI datacenter value chain and explain where value accrues by region.
- Analyze the global EV battery market, including China, Europe, the US, Korea, and Japan.
- Compare global cloud security vendors, noting where regional regulation changes adoption dynamics.

---

## Why this eval exists

Several reports can look broad while still being structurally incomplete.

This eval exists to prevent "global" from becoming a stylistic label instead of a real coverage standard.
