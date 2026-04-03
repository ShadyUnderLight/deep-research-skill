# Final Audit Checklist

Run through every item before delivering any deep research output.

This is the last gate before the report goes to the user. If any item fails, revise before delivery.

## Core question answered

- [ ] the report answers the user's actual question, not just the general topic
- [ ] the most important 2-3 variables are clearly stated and supported
- [ ] the bottom line is clear and actionable

## Evidence quality

- [ ] no major claim rests on a single weak source
- [ ] evidence hierarchy is visible: confirmed facts, well-supported inferences, and weak claims are not mixed
- [ ] key numbers are sourced and dated

## Counter-evidence

- [ ] the strongest argument against the main conclusion is present
- [ ] competing explanations are noted where relevant
- [ ] limitations and risks are explicit, not buried

## Uncertainty

- [ ] what could not be verified is stated explicitly
- [ ] confidence levels match evidence quality
- [ ] the report does not claim more certainty than the evidence supports

## Completeness

- [ ] the report does not leave a strong impression while having weak substance
- [ ] every section either adds decision-relevant information or is cut

## Recall discipline

- [ ] current-state verification was run for fast-moving topics
- [ ] listing status and financial snapshot were verified for listed companies
- [ ] source traceability was applied for structured or investment-relevant outputs
- [ ] option-selection final audit was run for shortlist, ranking, or constrained-choice outputs
- [ ] for model/API/provider selection tasks, a current provider snapshot was verified before ranking or recommendation
- [ ] for China-mainland deployment decisions, accessibility, compliance, data residency, and SLA were treated as part of ranking logic when relevant
- [ ] for market-entry / regional-expansion / country-prioritization tasks, priority relative to alternatives, country shortlist, hard gates, and sequencing logic are explicit rather than implied
- [ ] for market-entry / regional-expansion / country-prioritization tasks, regional hub vs first beachhead vs later expansion market are separated when relevant
- [ ] for market-outlook / industry-evolution tasks, a current market snapshot was verified before forward-looking sections
- [ ] for market-outlook / industry-evolution tasks, drivers, blockers, scenarios, and stakeholder implications are explicit rather than implied
- [ ] for first-tier / top-tier / multidimensional positioning tasks, scope, metric, timeframe, and dimension-level conclusions are visible before any overall label
- [ ] for first-tier / top-tier / multidimensional positioning tasks, the report does not collapse geography, current products, roadmap products, ecosystem strength, traction, and capital-markets signaling into one vague prestige tag without an explicit aggregation rule

## Precision and estimate sourcing

- [ ] every "预计 / 估计 / 预期" in the report has a named source attribution (who expects this?)
- [ ] bare "预计" without source = fail; go back and add "[据公司指引/据分析师/据媒体]预计"
- [ ] exact figures are used when source provides them; "约" only when source itself rounds
- [ ] quantitative outlook numbers are labeled as observed / inferred / scenario assumption / illustrative calculation when the distinction matters
- [ ] for constrained-choice / shortlist reports that use composite scoring, important quantitative inputs are labeled as observed fact / proxy / assumption / model output when the distinction affects trust in the recommendation
- [ ] when evidence buckets are used, the report does not stop at `confirmed / inference / unknown` if important numbers still function as proxy / assumption / planning-model output
- [ ] heuristic timing, cost, payback, or ROI-style claims are not written as if they were directly observed facts when they are closer to assumptions or planning-model outputs

## Market position and ranking claims

- [ ] every market-position claim specifies scope: "中国市场" / "全球" / "按XX口径"
- [ ] every market-position claim includes a conditional clause or explicitly states "no dependencies identified"
- [ ] if the report uses `第一梯队` / `top-tier` / similar prestige labels, it states whether the label is dimension-specific or an overall classification and why that compression is justified
- [ ] "全球最大" / "市场领导者" / loose `第一梯队` language without scope and dependency = fail

## Profit + scale signal pairing

- [ ] when volume/scale growth is reported, profitability and cash flow signals are checked
- [ ] if both positive (scale up) and negative (margin down) signals exist in the same period, they are presented together in one sentence or adjacent bullets — not separated in different sections
- [ ] reader does not have to connect the dots themselves

## Delivery cleanliness

- [ ] no citation artifacts, retrieval syntax, placeholder entities, or rendering residues leak into the final report body
- [ ] markdown / PDF delivery does not expose internal labels, raw template markers, or unfinished placeholders

## Quality bar

A report that fails this checklist is not ready for delivery, regardless of length or apparent polish.
tput does not show CJK spacing degradation or broken-export text rhythm severe enough to reduce professional readability

## Quality bar

A report that fails this checklist is not ready for delivery, regardless of length or apparent polish.
