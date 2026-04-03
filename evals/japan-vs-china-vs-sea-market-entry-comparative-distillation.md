# Japan vs China Focus vs Southeast Asia Expansion — Comparative Distillation

## Case identity

- **Task type:** market entry / regional expansion / constrained-choice memo / prioritization under resource constraints
- **User objective:** 判断一家资源有限的中国 AI Agent 创业公司在未来 12 个月内，是否应该优先进入日本市场，而不是继续深耕中国或优先进入东南亚
- **Observed output:** MiniMax-generated Chinese PDF memo
- **Research date context:** 2026-04-03
- **Distillation goal:** 提炼这类 market-entry 输出在 decision utility、evidence-role labeling、delivery-language consistency、以及 PDF cleanliness 上的可复用规则

---

## Why this case matters

This case matters because the output did **not** fail in the most basic way.

The model did not completely misunderstand the task. It recognized that this was a prioritization problem, compared China / Southeast Asia / Japan, and produced an explicit ranking.

That makes the case more valuable than a trivial failure. The real question is why a recommendation-shaped market-entry report can still fall short of a truly auditable operating memo.

This case also exposed a separate final-delivery issue: a Chinese report can still leak load-bearing English labels such as `Confirmed Facts`, `Likely Inference`, and `Unknown`, even when the rest of the memo is in Chinese.

---

## Core judgment

MiniMax partially routed the task correctly: the report behaved more like a prioritization memo than a single-country overview.

However, the final output still remained closer to a **structured regional analysis with recommendation** than to a **hard operating decision memo**.

The most important gap was not whether it had a conclusion, but whether it translated that conclusion into:

- visible resource-allocation logic
- explicit hard gates
- sequencing and milestone logic
- ranking-change conditions
- final-delivery coherence in the target language

---

## What the output got right

### 1. It recognized the task as a comparative prioritization problem
The report did not only analyze Japan. It compared Japan against continued China focus and Southeast Asia pilot expansion.

### 2. It produced an explicit ranking
The report clearly stated a current ranking: China first, Southeast Asia second, Japan third.

### 3. It used a visible comparison frame
Demand, compliance, localization, sales motion, deployment constraints, and payback speed were all treated as comparison dimensions.

### 4. It attempted evidence bucketing
The report tried to distinguish stronger evidence from inference and unknowns, which is better than writing every claim in one flat register.

---

## Main failure modes

### 1. Decision-memo under-specification
The recommendation existed, but it was still too soft as an operating memo.

Missing or weak elements included:
- explicit hard gates
- milestone-triggered re-evaluation
- ranking-reversal conditions
- more concrete 0-12 month operating path

### 2. Choice-architecture softness
The ranking was visible, but not fully auditable.

The report did not clearly show:
- why Southeast Asia beats Japan now
- what conditions would move Japan upward
- how to distinguish first revenue beachhead, regional hub, and later expansion market

### 3. Number-role ambiguity
Some time / cost / ROI-like claims read as if they were observed facts, but likely function more as heuristics, assumptions, or planning-model outputs.

This creates a professional-looking memo that can still overstate certainty.

### 4. Delivery-language inconsistency
The final report was written in Chinese, but still used load-bearing English evidence labels such as:
- `Confirmed Facts`
- `Likely Inference`
- `Unknown`

This should be treated as a delivery-quality failure, not a cosmetic preference.

### 5. PDF rendering / CJK broken-export failure
The final PDF still showed obvious CJK spacing degradation and broken-export text rhythm. This remains a final-delivery hard fail.

---

## Distilled lessons

### Lesson 1 — market-entry outputs must show operating-path logic, not only recommendation flavor
For market-entry / regional-expansion tasks, a visible recommendation is not enough. The memo should explicitly show:

- `go` / `not now` / `pilot only` / `phased entry`
- priority relative to alternatives
- why the top option wins
- why the runner-up remains credible
- hard gates
- sequencing
- KPI / milestone triggers
- what changes the ranking

**Candidate action:** `CHECKLIST_HARDENING`

---

### Lesson 2 — evidence-layer labeling and planning-layer labeling should be separate
This case shows that reports can partially distinguish facts from inference while still failing to show the role of important numbers.

The output should distinguish:

**Evidence layer**
- 已确认事实
- 推断
- 未知事项

**Modeling layer**
- 观察值
- 代理指标
- 假设
- 规划模型输出

**Candidate action:** `CHECKLIST_HARDENING`

---

### Lesson 3 — target-language coherence needs to be audited explicitly
If the final report is in Chinese, section anchors, evidence buckets, callout labels, and other load-bearing structural labels should default to Chinese unless bilingual output is explicitly requested.

Preferred labels for Chinese reports include:
- 已确认事实
- 推断
- 未知事项
- 观察值
- 代理指标
- 假设
- 规划模型输出

**Candidate action:** `NEW_RULE` + `CHECKLIST_HARDENING`

---

### Lesson 4 — PDF cleanliness and language consistency belong to the same final-delivery layer
This case confirms that mixed-language structural labels and broken CJK PDF texture should both be treated as final-artifact coherence failures.

They are not separate from delivery quality; they are delivery quality.

**Candidate action:** `CHECKLIST_HARDENING`

---

## Candidate-action summary

| # | Candidate action | Failure family | Action type | Proposed home |
|---|---|---|---|---|
| 1 | Require market-entry outputs to show explicit decision status, hard gates, sequencing, and ranking-change logic | decision utility / operating-path under-specification | CHECKLIST_HARDENING | `checklists/final-audit.md` |
| 2 | Require visible separation between evidence-layer labels and modeling-layer number-role labels | evidence weighting / planning-model traceability | CHECKLIST_HARDENING | `checklists/final-audit.md` |
| 3 | Add target-language consistency gate for load-bearing structural labels in final reports | delivery-language coherence | NEW_RULE + CHECKLIST_HARDENING | `references/report-template.md` + `checklists/final-audit.md` |
| 4 | Treat mixed-language structural labels and CJK broken-export texture as final-delivery coherence failures | delivery cleanliness / final artifact quality | CHECKLIST_HARDENING | `checklists/final-audit.md` |

---

## Things explicitly rejected

| Observation | Why rejected |
|---|---|
| MiniMax understood the task, so no routing change is needed | partial success still left major execution and delivery failures |
| English evidence labels are harmless if the report is mostly Chinese | the labels are load-bearing structure, so language inconsistency weakens final-artifact coherence |
| This is only a PDF rendering problem | the case also exposed decision-utility softness and language-layer inconsistency |

---

## Final judgment

This case is useful because it exposed a more advanced failure family than generic overview drift.

The model can now produce a recommendation-shaped market-entry report, but still often stops short of a fully auditable operating memo. It also showed that a report can partially improve in structure while still failing final delivery through:

- number-role ambiguity
- mixed-language structural labeling
- CJK broken-export PDF texture

The right response is not only to harden market-entry decision architecture, but also to add an explicit audit rule for **target-language coherence in final delivery**.
