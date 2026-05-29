# Startup / Private Company Evaluation Discipline

Use this file when the research involves evaluating a private, unlisted, or early-stage company.

Do not default to listed-company evaluation methods (PE, PB, DCF, public-market multiples) when the company has no public market data.

## Core rule

Private company evaluation requires a different framework than listed-company analysis. The absence of mandatory financial disclosures, public market pricing, and analyst consensus changes what evidence is available, how it should be sourced, and what conclusions can be drawn.

Do not force listed-company structure onto a private company report.

## Key differences from listed-company evaluation

| Dimension | Listed company | Private company |
|-----------|---------------|-----------------|
| Financial data | Audited filings, quarterly reports | Self-reported, estimated, or absent |
| Valuation | Market price, PE, PB, DCF | Latest round, comparable transactions, revenue multiples |
| Key variables | Revenue growth, margins, guidance | PMF signals, burn rate, runway, founder quality |
| Source quality | SEC filings, exchange disclosures | Company blog, Crunchbase, PitchBook, media |
| Analyst coverage | Broker research, consensus | Sparse, often investor-sourced |
| Time horizon | Quarterly / annual cycles | Funding round to funding round |

## Evaluation framework

### 1. Company stage identification

Before analysis, identify the company's current stage:

- **Pre-seed / Seed**: Idea or early product, minimal revenue, founder-dependent
- **Series A/B**: Product-market fit validation, early revenue, team building
- **Series C+ / Growth**: Scaling, meaningful revenue, operational complexity
- **Pre-IPO**: Preparing for public listing, may have filed or be in process

The stage determines which metrics matter and what evidence burden is appropriate.

### 2. Team and founder assessment

For private companies, team quality is often a primary variable, not a secondary one.

Assess:
- Founder background and track record
- Domain expertise relevance
- Prior exits or scaling experience
- Team composition relative to business model needs
- Advisory board or investor quality as signal

**Evidence discipline:**
- Label founder-sourced claims as issuer-sourced
- Do not treat marketing language ("world-class team", "serial entrepreneur") as confirmed fact
- Prefer third-party validation (investor quality, prior exit outcomes) over self-description

### 3. PMF (Product-Market Fit) signals

PMF is the central question for early-stage companies. Evaluate based on available signals:

**Strong signals (if available):**
- Retention curves (cohort analysis)
- Net Revenue Retention (NRR) for SaaS
- Organic growth vs paid growth ratio
- Customer testimonials or case studies with verifiable outcomes
- Revenue growth rate relative to burn rate

**Weak signals (use with caution):**
- User count without retention context
- Press coverage or social media buzz
- Awards or recognition without revenue validation
- Founder claims about traction

**Evidence discipline:**
- Distinguish user growth from paid growth from revenue growth
- If PMF data is unavailable, state this explicitly rather than inferring from adjacent signals
- Label metrics by source type: company-reported / third-party estimate / inferred

### 4. Funding and valuation

Private company valuation is fundamentally different from public market valuation.

**Preferred valuation anchors:**
1. Most recent funding round valuation (if disclosed)
2. Comparable transaction multiples (revenue, ARR, user base)
3. Secondary market pricing (if available and current)
4. Investor-reported valuations (if credible and recent)

**Do not use as primary framing:**
- PE / PB / PS multiples (no public market price)
- DCF models (too many assumptions for early-stage)
- Public market comparable without explicit adjustment for illiquidity, stage, and disclosure differences

**Evidence discipline:**
- Label valuation as "latest round valuation" not "company value"
- Note whether valuation is primary (investor-confirmed) or secondary (media-reported)
- If valuation is stale (older than 12 months for fast-moving companies), flag this
- Distinguish between pre-money and post-money when relevant

### 5. Financial metrics for private companies

Available financial data varies dramatically by stage. Use what exists, do not fabricate what does not.

**Common metrics (when available):**
- ARR / MRR (Annual / Monthly Recurring Revenue)
- Gross margin
- Burn rate (monthly cash consumption)
- Runway (months of cash remaining)
- CAC (Customer Acquisition Cost)
- LTV (Customer Lifetime Value)
- Churn rate
- Burn Multiple (net burn / net new ARR)

**Evidence discipline:**
- Label all financial figures by source: company-disclosed / investor-reported / estimated / inferred
- If revenue is estimated by third parties (Crunchbase, PitchBook), label as estimate
- Do not present estimated figures with the same confidence as audited public-company financials
- If key metrics are unknown, state this rather than using proxies without labeling

### 6. Competitive positioning

Private companies often compete with both incumbents and other startups.

Assess:
- Direct competitors (same market, similar solution)
- Adjacent competitors (different approach to same problem)
- Incumbent threat (large companies that could enter)
- Resource constraints vs competitive advantages
- Moat durability (network effects, data advantages, switching costs, brand)

**Evidence discipline:**
- Competitive claims should be grounded in verifiable product differences, not marketing
- Market share claims for private companies are often weak or absent; label accordingly
- Do not treat "first mover" or "only player" claims as confirmed without evidence

### 7. Risk assessment

Private company risks differ from public company risks:

**Key risk categories:**
- Funding risk (runway, next round dependency)
- Key-person risk (founder departure impact)
- Market risk (PMF may not scale)
- Regulatory risk (especially for fintech, healthtech, crypto)
- Execution risk (scaling challenges)
- Competitive risk (incumbent response, new entrants)

**Evidence discipline:**
- Risks should be specific to the company, not generic startup risks
- Quantify when possible (runway in months, burn rate trajectory)
- Label risk assessment as judgment, not fact

## Source hierarchy for private companies

Private companies have different source availability than listed companies.

### Preferred order

1. **Company official materials** — blog posts, product documentation, whitepapers, official announcements
2. **Credible third-party databases** — Crunchbase, PitchBook, CB Insights (label as aggregator data)
3. **Regulatory filings** — SEC Form D, state filings, international equivalents (when available)
4. **Investor-sourced information** — investor blogs, portfolio pages, LP letters (label as investor perspective)
5. **Media coverage** — TechCrunch, 36氪, The Information (treat as discovery, verify claims)
6. **Social / community** — founder Twitter/LinkedIn, Reddit, V2EX (minimum weight, supplemental only)

### Source quality rules

- **Crunchbase / PitchBook**: Aggregator data, not primary source. Funding amounts and valuations may be approximate. Label as "per [source], estimated."
- **Media coverage**: Discovery tool, not evidence. Verify load-bearing claims via primary sources when possible.
- **Founder claims**: Issuer-sourced. Do not elevate to confirmed fact without independent validation.
- **Social media**: Weak supplemental signal. Do not use as primary evidence for any load-bearing claim.

## Output structure

A private company report should include:

1. **Company overview and stage positioning** — what the company does, what stage it is in
2. **Team assessment** — founders, key hires, relevant background
3. **Product and PMF signals** — what exists, what traction is real
4. **Market and competitive position** — who they compete with, what advantages exist
5. **Funding and financial overview** — known funding, revenue (if disclosed), burn/runway (if known)
6. **Key strengths and risks** — specific to this company
7. **12-24 month milestones** — what to watch for
8. **Judgment and recommendation** — if applicable, with explicit uncertainty bounds

Do not force listed-company sections (current market snapshot, PE/PB, analyst consensus) into a private company report.

## Hard-fail conditions

Fail if the report:

- uses PE / PB / PS / DCF as primary valuation framing for a private company without explicit justification
- treats unverified founder claims as confirmed facts
- presents weak or absent financial data as if it were comparable to audited public-company disclosures
- does not label source reliability levels
- writes the report as a mini listed-company analysis with private company data gaps hidden
- uses `唯一` / `only` / `first` / `领先` wording without evidence strong enough for that claim strength

## Borderline cases

### Company is filing for IPO but not yet listed

Use the private company route, but note IPO status. The analysis should be forward-looking about what changes post-IPO (access to capital, disclosure requirements, valuation anchoring).

### Recently listed company with mostly pre-IPO data

Use the listed-company route if trading has begun. Note that financial data is primarily from prospectus / pre-IPO disclosures, and current market data should be included as the primary valuation anchor.

### Large private company with extensive public data (e.g., OpenAI, Stripe)

Use the private company route, but note that data availability is unusually high. The evaluation framework still applies, but evidence burden may be easier to meet.
