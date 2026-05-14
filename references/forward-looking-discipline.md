# Forward-Looking Claims Discipline

Use this file when the research involves forecasts, estimates, targets, roadmap claims, outlook projections, expected timelines, or any statement about what may happen in the future.

Do not present forward-looking claims as if they have the same certainty as observed facts.

## Core rule

Every forward-looking claim needs a visible source role and time basis.

A single unlabeled `预计` / `expected` / `likely` in a load-bearing position is enough to reduce the report's credibility. Multiple unlabeled forward claims without source role or confidence framing mean the report is not yet disciplined enough for delivery.

## Separate these categories

Always distinguish among these three categories in the final output:

1. **Announced / guided** — the company, provider, or issuer publicly stated this target or timeline. Examples: earnings guidance, product launch announcement, official roadmap.
2. **Estimated / projected** — an external third party (analyst, research firm, media) produced this forecast. The source and methodology should be named.
3. **Inferred / modeled** — the report itself derived this number from assumptions, proxies, or scenario math. This must be labeled as model output, not presented as a finding.

Do not collapse these categories into one undifferentiated `预计` or `expected` layer.

## Announced vs rumored separation

For product roadmaps, technology timelines, and corporate plans:

- **Announced**: the company itself made a public, attributable statement with a named time window or trigger condition
- **Rumored / media-reported**: the information comes from supply-chain leaks, analyst notes, media speculation, or unnamed sources
- **Inferred**: the timeline is derived from historical patterns, patent filings, hiring signals, or similar indirect evidence

Keep these separate in the report body. Do not mix announced and rumored claims in the same sentence or bullet without distinguishing their source role.

## Time basis

Every forward-looking claim must have a visible time reference:

- "expected in H2 2026" not "expected soon"
- "guided for FY2026" not "guided higher"
- "media reports suggest a 2027 launch" not "reportedly launching"

If the time basis is uncertain, say so: "media reports suggest a 2027 launch, though the timeline has not been confirmed by the company."

## Confidence framing

When multiple forward-looking claims appear, signal their relative confidence:

- higher confidence: officially guided or contractually committed, with named trigger conditions
- medium confidence: announced with caveats, or estimated by multiple credible third parties with converging methodologies
- lower confidence: rumored, single-source, inferred from weak signals, or derived from untested assumptions

The report should not mix high-confidence and low-confidence forward claims in one undifferentiated outlook section.

## Assumption chains

When the report derives a forward-looking number (revenue projection, market size forecast, adoption timeline), make the assumption chain visible:

- what is the base assumption?
- what would change if that assumption is wrong?
- is the number a scenario illustration or a central forecast?

Example: "Assuming 15% annual growth (in line with industry consensus), the market would reach $X by 2028. If growth slows to 10%, the market would reach $Y. This is an illustrative scenario, not a forecast."

## Common failure patterns

### Pattern 1: unlabeled `预计`
`预计该公司的收入将在2026年增长20%` — who expects this? The company? An analyst? The model?

Fix: `[公司]预计2026年收入增长20%（公司2025年报指引）` or `[分析师Name]预计2026年收入增长20%（来源: [SN]）`.

### Pattern 2: roadmap claims without announced vs rumored separation
`Apple 将在2026年发布M5芯片` — is this announced or media-reported?

Fix: `据媒体报道，Apple 将于2026年发布M5芯片（来源: [SN]，该信息尚未经 Apple 官方确认）`.

### Pattern 3: consensus numbers without source or date
`分析师普遍预计2026年EPS为$X` — which analysts? Based on what reported period?

Fix: `截至2026年3月，彭博一致预期2026年EPS为$X（范围: $Y-$Z, N位分析师）`.

### Pattern 4: estimate language without assumption chain
`到2030年，市场规模将达到$X` — what growth rate does this assume? What adoption curve?

Fix: `假设年均增长率15%（基于[来源]的行业预测），到2030年市场规模将达到$X。若增长率为10%，则为$Y`. Then label as scenario illustration.

## Relationship to other discipline files

- `references/finance-date-discipline.md` covers the broader time-layer separation for financial numbers, including historical reported facts and current market snapshots. This file focuses specifically on the forward-looking subset.
- `checklists/forward-looking-claims.md` is the delivery-time gate: run it to catch unlabeled forward claims before the report goes out.
- `checklists/final-audit.md` includes forward-looking gates for precision and estimate sourcing.

## Quality bar

The report should not contain a sentence where a forward-looking claim has no visible source role, no time basis, and no confidence signal. One such sentence in a load-bearing position means the report is not yet ready for delivery.
