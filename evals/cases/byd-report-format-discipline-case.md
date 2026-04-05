# BYD Report — Output Format & Structural Discipline Eval

**Date:** 2026-04-01
**Model:** Minimax (MiniMax-M2)
**Source:** User-provided PDF from a Minimax-generated deep research report on BYD (比亚迪)

## Research question
BYD company deep research report (Chinese, structured format with confidence labels)

## What went well

### 1. Structured confidence label system
The report introduced and consistently applied `[CONF]` / `[LIKELY]` / `[UNCERTAIN]` inline tags directly before each claim in the text. This is a meaningful structural improvement over reports that only use block-level callouts. It makes the confidence level traceable to the individual claim level, not just the section level.

### 2. Evidence-level labels in Exec Summary
Even in the brief Exec Summary bullets, each item carried a `[CONF]` or `[LIKELY]` tag — showing the model understood the labeling requirement applied at the most critical summary level too.

### 3. Multi-source disclosure in header
The report header explicitly listed data sources (Wikipedia, CnEVPost, Bloomberg, Reuters, SCMP) and defined the confidence label scheme — this follows the source-quality and transparency expectations.

---

## What went wrong

### 1. Exec Summary bullets are paragraph walls — one insight per bullet rule violated

**Rule (from `references/report-template.md`):** Each bullet should contain one distinct idea. A reader should be able to extract key facts without reading every sentence.

**Actual behavior in this report:**

> • **[CONF]** 比亚迪是全球最大的新能源汽车制造商之一，2025年全年新能源汽车销量约460万辆，营收规模约5300亿元人民币（约770亿美元），净利润因国内价格战同比下滑19%至326.2亿元。

This is a single bullet containing approximately 5–6 distinct facts (manufacturer rank, unit sales, revenue, net profit direction, price war factor, percentage). A reader scanning the Exec Summary cannot extract individual facts without reading the full bullet.

**Contrast with the MiniMax report** — that report had the opposite problem (Exec Summary as pure prose paragraph), but the BYD report, while using bullet structure, still defeats the purpose of bullets by stuffing them full of content.

**Severity:** Medium — the structural form is present but its function is defeated.

### 2. "预计" (estimated) language lacks [UNCERTAIN] label

**Rule (from SKILL.md + `references/finance-date-discipline.md`):** Forward-looking or estimated figures must be labeled with their source type (company target / analyst estimate / inferred calculation) and confidence level.

**Actual behavior:**
> "2025年海外销量预计超100万辆，2026年目标150万辆"

The word "预计" indicates this is an estimate or projection, not a confirmed fact. Yet there is no `[UNCERTAIN]` tag. The model used the estimate word but did not apply the corresponding confidence label — a pattern of inconsistent inference labeling.

**Severity:** Medium — the report acknowledges uncertainty in language but does not translate that linguistic hedge into the formal label system.

### 3. Ranking claims without calibration

**Rule (from `references/ranking-and-current-claims-discipline.md`):** Claims about leadership, market position, or rankings must specify the source, metric, time period, and geographic scope. Vague superlatives are not acceptable.

**Actual behavior:**
> "比亚迪是全球最大的新能源汽车制造商之一"
> "中国市场绝对领导者：2025年国内新能源乘用车市场份额约35-40%"

The first claim ("全球最大") has no source, no metric definition, and no time boundary. The second ("绝对领导者") lacks geographic scope (全球? 中国?) and is stated as fact despite being an inference.

**Severity:** Medium — the content is directionally defensible, but the framing violates the ranking claims discipline.

### 4. PDF formatting / render quality

The markdown-to-HTML pipeline difficulty is partially upstream of the model, but the model's markdown source also did not consistently use bullet list syntax for what were clearly list-of-facts items. This made the rendering pipeline's table detection and bullet detection less reliable.

---

## Failure modes summary

| Failure | Severity | Related skill rule |
|---------|----------|---------------------|
| Exec Summary bullets stuffed with multiple facts, violating one-insight-per-bullet | Medium | `report-template.md` exec summary section |
| "预计" language without [UNCERTAIN] label | Medium | `SKILL.md` inference labeling; `finance-date-discipline.md` |
| Ranking claims ("全球最大") without scope/metric/period | Medium | `ranking-and-current-claims-discipline.md` |
| Markdown source not optimized for render pipeline (contributing to formatting issues) | Low | N/A — pipeline issue |

---

## Lessons

1. **Label system exists and is understood — execution discipline is the gap.** The model correctly identified the label scheme and applied it consistently in some places but dropped it in others. This is a known compaction/execution risk: the rule is in the skill, but enforcement is not automatic. The fix direction is to move enforcement to checklist level (`final-audit.md` already exists as a delivery gate).

2. **Bullet stuffing is more common than full prose.** After seeing pure paragraph Exec Summary (MiniMax) and bullet-wall Exec Summary (BYD), the actual lesson is that the model needs a structural enforcement mechanism — not just "use bullets" or "don't use paragraphs" but a concrete size/complexity limit per bullet. Consider adding a bullet length check to `final-audit.md`.

3. **Linguistic hedge ≠ formal label.** The model recognized the word "预计" as carrying uncertainty, but did not translate that to `[UNCERTAIN]`. This suggests the model processes uncertainty at the vocabulary level but not at the formal metadata level. Adding a cross-check in the audit: "Does every instance of 预计/估计/预期 have a corresponding [UNCERTAIN] tag?" would close this gap.

4. **Eval conclusion:** Add this as a **format-and-discipline failure case** rather than a content accuracy case. The model's biggest gaps here are execution consistency and structural discipline, not knowledge or reasoning.
