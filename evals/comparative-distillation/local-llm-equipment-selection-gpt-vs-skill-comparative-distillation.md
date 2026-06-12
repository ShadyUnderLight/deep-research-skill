# Local LLM equipment selection GPT-vs-skill comparative distillation

## Case

Two independently commissioned reports on the same topic:

- **Report A (skill-generated):** 「本地大模型运行设备选型：Mac Studio vs RTX 5090 主机 vs 云 GPU」  
  Produced via the repo's deep-research skill system with explicit Equipment Selection route activation.
- **Report B (GPT deep research):** 「个人本地大模型运行设备选型研究报告」  
  Produced via GPT's native deep research mode without an explicit discipline system.

**What the comparison reveals:** Neither report could pass the repo's final delivery standard on its own. Report A activates the correct route, builds TCO structure, and includes counter-evidence — but its source traceability is not actually landed, numeric role labels are absent, and the self-assessment overclaims pass status. Report B delivers superior decision-making craft (workload segmentation, benchmark methodology explanation, cost sensitivity, decision tree, build-ready configurations) but its citations are unreproducible `turn...` placeholders with `sandbox:` image references.

This is a **paired complementary failure**: one report has visible structural discipline but fails on evidence execution; the other has superior native judgment but fails on reproducibility.

---

## Triage notes

### Triage outcome
KEEP and DISTILL

### Why this case matters
This case exposes a gap that existing case evals do not cover — the gap between **structural discipline activation** and **sentence-level execution quality**:

- Previous equipment-selection cases (home-NAS, local-AI-lab) tested whether the skill system worked as designed, and found conditional-pass failures at the discipline level.
- This case tests a different scenario: the skill system **fired correctly** (route declared, TCO built, counter-evidence included) but the model still did not execute discipline layers at the source-line level. The discipline *system* worked; the model *execution* did not.
- Meanwhile, a non-skill report (GPT) produced stronger decision-making output — but with delivery flaws that make it unreproducible.

This pair is valuable because it shows that **even when routing succeeds, discipline checklists can pass at the section-present level while failing at the evidence-quality level**. And it shows that **native model judgment can outperform discipline scaffolding on content but remain undeliverable due to citation hygiene**.

The repo's response cannot be "add more checklists" — the checklists already exist. It must be about checklist **hardening at the line level**, not the section level.

---

## Task classification

### Primary route
- Equipment Selection / Procurement / Home-server Planning

### Secondary disciplines
- Technical Deep-dive (benchmark methodology, model quantization)
- Cost analysis (TCO, electricity, residual value)
- Source traceability
- Decision utility (per-persona recommendation)

### Visible artifact contract (what a deliverable report must contain)
- Per-persona recommendation (not one-size-fits-all)
- Route ranked with dominant constraint named
- Budget assumptions explicit (what is included/excluded)
- Hardware ↔ system stack bound into one recommendation
- Benchmark methodology disclosed with comparability caveats
- TCO broken into upfront + recurring with usage sensitivity
- Configurations that are build-ready (not abstract component lists)
- Source traceability via `[Sxx]` inline citations with Source Register
- Numeric role labels on prices, performance, TCO
- Clean delivery: no `turn...` references, no `sandbox:` images, honest audit status
- Unknown/verification gap register

---

## What Report A (skill) did well

### 1. Route activation
Report A correctly selected the Equipment Selection route and declared it explicitly. The report opens with a per-user-type recommendation (student, regular learner, heavy researcher) — this matches the route's visible artifact contract.

### 2. TCO structure
A dedicated TCO comparison section spans all three routes (Mac Studio, RTX 5090 host, cloud GPU) and covers power, noise, maintenance, and privacy. The TCO is operationalized as a load-bearing section, not a decorative table.

### 3. Counter-evidence and reversal conditions
The report includes a reversal conditions table (§290-301 in the source) and explicitly covers drawbacks per option. Reversal conditions are key for the Equipment Selection route's visible artifact contract.

### 4. Rejected options with specific reasoning
Brand new hardware, dual-GPU setups, 16GB Mac variants, AMD GPUs, and overseas cloud providers are rejected with specific operator-reasoning rather than category dismissal.

### 5. Uncertainty and next steps
A 30-day action plan with branching paths (§326-335) and a risks section (§305-322) show forward-looking discipline.

### 6. Judgment-first opening
The report opens with the per-user-type recommendation before broad background — matching the route's requirement for judgment compression.

---

## What Report B (GPT) did well

### 1. Workload segmentation
Report B segments recommendations not by user budget level but by **real workload**: fine-tuning vs inference-heavy vs eval-heavy. This is a more operationally useful segmentation than broad user persona categories. The workload-aware approach produces different route rankings per workload type — which is exactly what the Equipment Selection route demands but rarely achieves.

### 2. Benchmark comparability
Report B explicitly explains why different benchmarks (MMLU, HumanEval, AIME) matter for different use cases, and why benchmark scores from different sources are not directly comparable. This is a best practice that neither the repo's Technical Deep-dive discipline nor the Equipment Selection route currently mandates.

### 3. Cost sensitivity
The report models how cost changes with usage: light vs heavy GPU hours per day, cloud GPU break-even point vs upfront purchase, and how electricity cost flips the ranking between Mac Studio and RTX 5090 at different utilization rates. This is notably more nuanced than Report A's fixed TCO table.

### 4. Decision tree
A visible decision flow branches by: workload type → budget → tolerance for tinkering. This produces 3-4 concrete recommendation paths that a buyer can follow without re-reading the entire report. The Equipment Selection route's visible artifact contract requires recommendation compression — this is an execution example of what that looks like.

### 5. Build-ready configurations
The report provides component-level configurations for each route: specific CPU/GPU/RAM/storage part numbers with estimated prices. While pricing accuracy depends on market recency, the *shape* of the output (buy-ready, not abstract) is what the route contract demands.

### 6. Why-not reasoning per route
Each route includes a "who should NOT choose this" paragraph — e.g., "Mac Studio user should NOT be someone who needs to run Llama 3 70B at full precision." This matches the reversal-condition requirement but is deployed more readably than a separate table.

---

## Core diagnosis

Neither report is independently deliverable. The gap is **complementary and structural**, not model-vs-model:

- Report A has the **discipline scaffolding** right (route declared, sections present, TCO built, counter-evidence included) but fails at **source-line execution** (no `[Sxx]` inline citations, no numeric role labels, audit section self-declares ✅ when body evidence is insufficient).
- Report B has superior **decision-making craft** (workload segmentation, benchmark methodology, build-ready configs, decision tree) but fails at **delivery reproducibility** (`turn...` placeholder citations, `sandbox:` images, no Source Register, no audit discipline at all).

The repo's existing discipline layers **would catch both failures** — source traceability checklist, quantitative role audit, delivery integrity checklist. But the system only applies to skill-produced reports. The most actionable insight is that **the discipline layers exist but the model doesn't execute them at line level even when they're activated**.

This is a **model execution gap, not a system design gap** — which means the fix must be at the checklist-hardening or template level, not the ROUTING-MATRIX or reference level.

---

## Failure families (10 dimensions)

### 1. Route fit
**Report A:** Equipment Selection route correctly selected. Route declaration visible in output. Per-user-type recommendation present. ✅
**Report B:** No route declaration — output is implicitly equipment-selection but without discipline awareness. The content fits the route's artifact contract (workload segmentation, build-ready configs) but without explicit route binding. ⚠️

*Triggered discipline:* ROUTING-MATRIX equipment-selection route — declaration required.

### 2. Workload segmentation
**Report A:** Segments by user persona (student, regular learner, heavy researcher). Reasonable but maps imperfectly to real equipment needs — budget and workload don't always align. ⚠️
**Report B:** Segments by workload type (fine-tuning, inference-heavy, eval-heavy). More operationally useful — the same person with different workloads should get different recommendations. ✅

*Triggered discipline:* decision-report-template — persona-based vs workload-based segmentation.

### 3. Benchmark comparability
**Report A:** Reports benchmarks without explaining comparability constraints. Does not disclose which benchmark settings (precision, quantization, batch size) produced the numbers. ❌
**Report B:** Explicitly explains why benchmark scores are not directly comparable across sources, and maps benchmark families to use-case relevance. ✅

*Triggered discipline:* `references/technical-analysis-discipline.md` — benchmark methodology disclosure.

### 4. Hardware ↔ system stack
**Report A:** Covers hardware and software separately without binding them. Does the recommendation change if the user runs Ollama vs vLLM vs LM Studio? Not addressed. ❌
**Report B:** Configurations include software stack recommendations per hardware route (e.g., "use Ollama + Open WebUI for this config, use vLLM for this one"). Binding is present but shallow. ⚠️

*Triggered discipline:* Equipment Selection hard-fail — "discusses hardware and systems separately without binding."

### 5. Cost sensitivity
**Report A:** Fixed TCO table — a single set of numbers without usage-sensitivity analysis. The table assumes a fixed utilization rate without disclosure. ❌
**Report B:** Models cost as a function of usage hours per day, and provides a break-even chart for cloud vs local. Shows that the ranking between Mac Studio and RTX 5090 flips at different utilization levels. ✅

*Triggered discipline:* `references/quantitative-role-labeling.md` — cost figures need role labels and sensitivity.

### 6. Build-ready configuration
**Report A:** Provides route-level descriptions but not component-level configurations. Not actionable for purchase. ❌
**Report B:** Provides specific part numbers with estimated prices and vendor types (e.g., "RTX 5090, ASUS ROG or MSI SUPRIM, ~¥28,000-32,000"). Actionable for someone ready to buy. ✅

*Triggered discipline:* Equipment Selection visible artifact contract — "minimum viable vs recommended config."

### 7. Source traceability
**Report A:** Source list at end is a loose bibliography without URLs, access dates, source-type ratings, or claims-supported mapping. No `[Sxx]` inline citations in body text. ❌
**Report B:** Citations use `turn...` placeholders — unreproducible references that look like `turn1.tool1.result...` with no URL, no access date, no source name. Also references `sandbox:` images that are not deliverable. ❌

*Both fail here, differently:* A has a source list with no inline binding; B has inline references that are unreproducible placeholders.

*Triggered discipline:* `checklists/source-traceability.md` — hard-fail if inline citations are missing or unreproducible.

### 8. Numeric role labeling
**Report A:** TCO figures, power estimates, failure rates, and residual value claims are presented without distinguishing observed prices from estimates from assumptions from model output. ❌
**Report B:** Prices are listed as estimates (labeled "约" or "预计") but no systematic role labeling. Better than A in practice but still not disciplined. ⚠️

*Triggered discipline:* `checklists/quantitative-role-audit.md` — every load-bearing number needs a role label.

### 9. Delivery cleanliness
**Report A:** The report ends with a self-assessment section claiming `Final Audit ✅ 已通过` and `Source Traceability ✅` — but body evidence does not support this claim. This is the repo's known overconfidence pattern documented in the local-AI-lab and home-NAS cases. ❌
**Report B:** Contains `sandbox:` image references that render as broken content in the delivered report. Citations use internal `turn...` identifiers that are meaningless to the reader. No audit section at all. ❌

*Triggered discipline:* `checklists/final-audit.md` — self-assessment honesty and delivery integrity.

### 10. Target synthesis
An ideal report combining the strengths would:
- Use workload segmentation (from B) as the primary recommendation driver, cross-referenced by user persona (from A).
- Open with a decision tree (from B) and follow with route-level TCO (from A) that varies by utilization.
- Provide build-ready configurations (from B) with minimum-viable vs recommended separation (from A).
- Bind hardware to software stack per route (A and B's partial efforts combined into explicit stack pairs).
- Include reversal conditions per recommendation (from A's table format) and "who should NOT choose this" per route (from B's paragraph format).
- Use `[Sxx]` inline citations (from the repo's source traceability discipline) with a proper Source Register — landing what A attempted.
- Apply numeric role labels to all load-bearing numbers: prices as `[OBSERVED]`, `[ESTIMATE]`, or `[ASSUMPTION]`; benchmark scores with precision/quantization context.
- End with an honest audit section that reflects actual delivery status — not claiming ✅ for undelivered disciplines.

The target synthesis is not a new report — it is a **cross-report discipline graft**: A's structure with B's craft, plus the repo's existing evidence disciplines executed at line level.

---

## Candidate actions

### NEW_RULE (checklist-hardening)
When the Equipment Selection route is activated, the source traceability checklist must verify **inline `[Sxx]` citations in body text**, not just a source list at end. A bibliography without inline binding is a hard fail.

### NEW_RULE (checklist-hardening)
When benchmark scores are reported, the report must disclose: benchmark name, precision/quantization setting, batch size, and model variant. Missing any of these is a hard fail for Technical Deep-dive sections within Equipment Selection.

### NEW_RULE (checklist-hardening)
Cost sensitivity analysis in equipment-selection reports must vary at least one input variable (utilization hours, electricity price, or depreciation period) and show how the ranking changes. A single fixed TCO table without sensitivity is a hard fail.

### CHECKLIST_HARDENING
The final-audit self-assessment check must verify delivery integrity at the **line level**, not the section level:
- Scan for `turn...` patterns (GPT internal references) — flag as delivery blocker
- Scan for `sandbox:`, `/sandbox/`, or local-path references — flag as delivery blocker
- Verify that each discipline declared in the audit section has corresponding body evidence

### DELIVERY_HARD_FAIL
If the report contains unreproducible citation patterns (`turn...`, `sandbox:`, `/sandbox/`, local absolute paths, or internal tool references), the delivery must be rejected regardless of content quality. This applies to both skill-produced and external reports.

### TEMPLATE_HARDENING
Add a "workload vs persona" segmentation option to the Equipment Selection route's visible artifact contract. The current contract specifies per-persona recommendation but does not mention workload-type segmentation, which is often more operationally useful.

---

## Proposed patch targets

### 1. `checklists/final-audit.md`
Add a delivery-integrity gate that scans for unreproducible patterns:
- `turn...` internal references
- `sandbox:` or `/sandbox/` paths
- Local file paths in citations or images
- Self-assessment claims that declare ✅ for disciplines without body evidence

### 2. `references/source-traceability-and-claim-citation.md`
Add an explicit rule: a source list at end without inline `[Sxx]` citations does not satisfy traceability. Equipment Selection and Provider Selection routes must have inline citations in body text for all load-bearing claims.

### 3. `references/equipment-selection-and-procurement-discipline.md` (new or existing)
Add guidance for:
- Workload-type segmentation (fine-tuning vs inference vs eval) alongside user-persona segmentation
- Benchmark methodology disclosure requirements
- Cost sensitivity analysis with at minimum one varied input
- Build-ready configuration format (specific components, not abstract route descriptions)

### 4. `references/technical-analysis-discipline.md`
Add a benchmark comparability section requiring disclosure of precision, quantization, batch size, model variant, and source for every reported benchmark score.

### 5. `ROUTING-MATRIX.md` (equipment-selection route)
Update the visible artifact contract to include:
- Workload segmentation as an option alongside persona segmentation
- Benchmark methodology disclosure
- Cost sensitivity analysis
- Build-ready configuration format

---

## Rejected observations

These are not the main reusable lessons:

- Whether Mac Studio is actually better than RTX 5090 for local LLMs
- Whether one specific quantizer or inference engine was mentioned
- Whether GPU RAM or system RAM is more important for a specific model size
- Whether one report's price for a specific component is closer to current market reality
- Whether B's decision tree is formatted as a flow chart or a text list
- Whether A uses the exact same TCO categories as B

Those are case-level details. The reusable lessons are about:

- The gap between **discipline activation** (route declared, sections present) and **discipline execution** (source traceability at line level, role labels on every load-bearing number)
- The gap between **procedural reproducibility** (skill system checklists) and **decision-making craft** (workload segmentation, cost sensitivity)
- The paired failure pattern where one report has structure but poor evidence, and the other has craft but poor reproducibility — neither is independently deliverable
- The insight that **existing discipline layers work at the section level but not at the line level** — the model activates the right checklist but does not execute it sentence by sentence

---

## Strongest reusable insight

Equipment-selection reports can **simultaneously** activate the correct route AND fail the discipline layers that the route requires. This is different from "route mismatch" (home-server case) or "overconfident labeling" (NAS case). It is a **structural-vs-execution gap**: the macro structure matches the route contract, but the micro evidence doesn't survive audit.

This means the repo's checklist system cannot rely on section-present checks. It needs line-level evidence sampling for:

- Inline `[Sxx]` citations in body text
- Quantitative role labels on numbers
- Benchmark methodology disclosure
- Self-assessment honesty (scanning for ✅ claims without body evidence)

The secondary insight is that GPT deep research can produce superior decision-making output in the **absence** of any discipline system. The repo's skill system adds auditability and reproducibility, but it does not (yet) guarantee better decision-making craft. The best target state is: **skill system for discipline + native judgment for craft**.

---

## Proposed bottom line

This case should be kept and distilled.

It reveals that the repo's discipline layers are **necessary but not sufficient** for deliverable equipment-selection reports:

- Necessary: routing, source traceability, role labeling, audit checklists — these catch failures that would otherwise go undetected
- Not sufficient: the model executes checklists at the section level but not at the line level, resulting in reports that pass structural review but fail evidence audit

The paired failure pattern is unique: Report A shows that "right structure + wrong execution" is not deliverable; Report B shows that "right judgment + wrong reproducibility" is also not deliverable. Together they define the **minimum viable combination**: discipline scaffolding that survives line-level audit + decision-making craft that produces actionable output.

The repo's most urgent patch is not a new route or a new reference document. It is **hardening the existing checklists to require line-level evidence** — inline citations, role labels, benchmark methodology disclosure, self-assessment honesty — rather than section-level presence.

---

## Post-case validation notes

### What this case confirms
The pattern of "model activates discipline structure but does not execute at source-line level" is stable and worth repo-level treatment. It is broader than equipment-selection: any route with source traceability or quantitative role labeling requirements will face the same gap.

### What is newly clarified
Previous equipment-selection cases (NAS, local-AI-lab) tested **whether the skill system worked** and found conditional-pass failures. This case tests **whether the skill system can guarantee delivery quality even when it fires correctly** — and finds that it cannot, because the model does not execute checklists at the evidence level. This shifts the intervention target from "add more rules" to "harden existing rules to require line-level execution."

### Why it is worth repo-level treatment
The gap is not route-specific or model-specific. It sits at the intersection of:
- Checklist design (section-present vs line-level)
- Template design (implicit vs workload segmentation)
- Delivery integrity (unreproducible patterns scanning)
- Self-assessment discipline (honest vs overconfident audit status)

All four are repo-level systems, not equipment-selection specifics.
