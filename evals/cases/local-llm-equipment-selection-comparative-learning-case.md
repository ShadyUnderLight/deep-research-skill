# Eval: Local LLM Equipment Selection Comparative Learning Case

## Goal

Test whether **two independently produced reports on the same topic** — one skill-generated (Report A), one from GPT deep research (Report B) — can each survive the repo's delivery standard when neither independently passes. This is a **comparative learning case**: the repo's most actionable insight comes from examining them as a pair, not from either report in isolation.

What this case tests:
- **Route activation without execution discipline** — Report A fires the Equipment Selection route correctly (TCO, reversal conditions, per-user recommendation) but skips inline `[Sxx]` citations, numeric role labels, and honest self-assessment. This is a new failure family: the **"route-execution gap"** where correct route is selected but discipline layers are not executed at line level.
- **External report import with unreproducible delivery** — Report B demonstrates superior decision-making craft (workload segmentation, benchmark methodology, cost sensitivity) but uses `turn...` placeholder citations and `sandbox:` image references that are unreproducible in any deliverable format.
- **Neither report compensates for the other's gaps** — Report A's visible structure does not guarantee evidence quality; Report B's judgment does not compensate for citation hygiene.

The case reveals that the repo's discipline layers pass at the **section-presence level** but fail at the **evidence-quality level** — a pattern that applies beyond equipment-selection to any route with source traceability or role-labeling requirements.

## Real case pattern

Two reports commissioned independently on the same topic (local LLM equipment selection: Mac Studio vs RTX 5090 host vs cloud GPU):

- **Report A (skill-generated):** 「本地大模型运行设备选型：Mac Studio vs RTX 5090 主机 vs 云 GPU」 — produced via the repo's deep-research skill system with explicit Equipment Selection route activation.
- **Report B (GPT deep research):** 「个人本地大模型运行设备选型研究报告」 — produced via GPT's native deep research mode without an explicit discipline system.

**What was done well (combined across both reports):**
- ✅ Equipment Selection route correctly activated (Report A) — per-user-type recommendation, reversal conditions, rejected options with specific reasoning
- ✅ Decision-making craft (Report B) — workload segmentation (fine-tuning vs inference vs eval-heavy), benchmark comparability explanation, cost sensitivity with utilization-dependent TCO
- ✅ Decision tree and build-ready configurations (Report B) — actionable per-persona recommendation paths and component-level part numbers
- ✅ TCO structure with power, noise, maintenance, privacy (Report A) — load-bearing comparison section
- ✅ Counter-evidence and "who should NOT choose this" per route (both reports) — in Report A's reversal table and Report B's per-route caution paragraphs

**Core issues (7 failure modes across both reports):**

The common thread is a **route-execution gap**: the correct route fires but production-code discipline (inline citations, role labels, honest assessment, delivery hygiene) does not follow at the sentence level. This pattern applies beyond equipment-selection to any route with source traceability or role-labeling requirements.

*Report A — skill-generated (discipline scaffolding present, line-level execution absent):*
- ❌ **Budget assumptions missing include/exclude details** — upfront and recurring costs are presented without listing what is covered (e.g., peripherals, cable management, tax, shipping) or explicitly excluded. The repo's Equipment Selection discipline requires explicit inclusion/exclusion declarations.
- ❌ **Performance table has tok/s but missing benchmark methodology** — tokens-per-second figures are reported without disclosing precision, quantization setting, batch size, model variant, or inference engine (Ollama vs vLLM vs LM Studio). The numbers are not reproducible.
- ❌ **Prices/TCO/breakeven present but no numeric role labels** — all load-bearing numbers (hardware prices, power estimates, failure rates, residual value) are stated without distinguishing `[OBSERVED]` from `[ESTIMATE]` from `[ASSUMPTION]` from `[MODEL_OUTPUT]`.
- ❌ **Source list is loose bibliography without inline binding** — source entries at end lack URLs, access dates, source-type ratings, and claims-supported mapping. No `[Sxx]` inline citations in body text. This fails the repo's source traceability discipline.
- ❌ **Audit status self-claims all ✅ passed but body didn't execute** — the self-assessment section declares `Source Traceability ✅` and `Final Audit ✅ 已通过` when body evidence contains no inline citations and no role labels. Overconfidence pattern consistent with existing equipment-selection cases.
- ❌ **Secondary provider-selection declared but hard-fail not independently verified** — the report activates a secondary Provider Selection concern (cloud GPU pricing) but the hard-fail gate for Provider Selection (price table with per-provider cost, SLA, exit cost) is not independently executed. The claim is structurally present but not substantiated.

*Report B — GPT deep research (strong judgment, unreproducible delivery):*
- ❌ **Citations are unreproducible `turn...` placeholders with `sandbox:` images** — inline references use GPT internal identifiers (`turn1.tool1.result...`) that are meaningless to readers. The report references `sandbox:` images that do not survive delivery. No Source Register, no access dates, no source names. This is a delivery blocker regardless of content quality.

## Scoring

- **Full Pass**: inline `[Sxx]` citations in body text + quantitative role labels on all load-bearing numbers + honest self-assessment (no false ✅) + reproducible sources (no `turn...`, no `sandbox:`) + delivery free of external system artifacts
- **Conditional Pass**: strong structure for skill report (A) or strong judgment for external report (B) but traceability + role labels + self-assessment + delivery hygiene gaps (this case's level — both reports)
- **Fail**: hard-fail triggered — unreproducible citations (`turn...`, `sandbox:`), false audit claims, or missing inline binding that blocks delivery

## Related evals

- `evals/comparative-distillation/local-llm-equipment-selection-gpt-vs-skill-comparative-distillation.md` — full comparative distillation (companion: detailed 10-dimension analysis, triage notes, patch targets)
- `evals/cases/local-ai-lab-equipment-selection-traceability-case.md` — same Equipment Selection route, same traceability gap pattern
- `evals/cases/home-nas-equipment-selection-label-case.md` — same route, label + budget consistency gaps
- `evals/cases/small-studio-video-storage-equipment-selection-case.md` — same route, hard-fail adjacent (inline citations absent, self-assessment overclaim)
