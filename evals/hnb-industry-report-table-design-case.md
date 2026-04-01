# HNB Industry Report — Table Design and Content Structure Eval

**Date:** 2026-04-01
**Model:** Minimax (MiniMax-M2)
**Source:** User-provided PDF from a Minimax-generated deep research report on HNB (加热不燃烧烟草) industry

## Research question
HNB industry deep research report (Chinese, structured format with confidence labels)

---

## What went well

### 1. Evidence tier legend included at report top
The report included an explicit evidence confidence legend at the top:
```
[CONF] = 确认事实
[LIKELY] = 合理推断
[UNCERTAIN] = 公开不确定性
```
This matches the distillation pattern identified from GPT's BYD report and shows the rule was understood and applied. This is a meaningful improvement over earlier reports that had no such legend.

### 2. Market size range with calibration note
> "全球 HNB 市场规模约 360–380 亿美元（2024年，不同机构口径差异较大）"

The report used a range rather than a single false-precision number and explicitly noted that different sources have different figures. This follows the data calibration discipline.

### 3. Competitive position labeled with [LIKELY]
> "PMI 以 IQOS 占据全球 HNB 市场约 55–60% 份额，是绝对领导者 [LIKELY]"

The model correctly applied a confidence label to a market-share claim rather than presenting it as a confirmed fact.

---

## What went wrong

### 1. Super-sized comparison table undermines the entire purpose of tabular structure

**Section 2.2 "HNB 与传统烟草品类的主要区别"** attempts to compare four product categories (传统燃烧香烟 / HNB / 电子雾化烟 / 尼古丁袋) across seven dimensions:

| 维度 | 问题 |
|------|------|
| 发热原理 | 每个单元格 1 个数据点 ✅ |
| 原料形态 | 每个单元格 1 个数据点 ✅ |
| 典型产品 | 每个单元格 2-4 个品牌名 ✅ |
| 风险 | 每格 1 个词（高/低/低/极低） ✅ |
| 监管体系 | 每格 1 个短语 ✅ |
| 主要公司 | 每格 3-5 家公司名，压缩在一格 ✅ |
| **整体** | **6 列 × 7 行 = 42 个数据点，每列都很浅** ❌ |

**The failure mode:** A table with this many dimensions cannot be read effectively. Each column gets at most a brief phrase, and the reader loses the ability to make cross-category comparisons. The information density is too low to support analysis, and the table becomes decorative rather than useful.

**What the model should have done instead:**

- Split into **2-3 thematic sub-tables** grouped by purpose:
  - Table A: Product attributes (发热原理 / 原料形态 / 产生烟雾) — for the reader comparing mechanism
  - Table B: Commercial & regulatory profile (监管体系 / 风险等级 / 主要公司) — for the reader assessing market structure
- Or use a **structured list** if the number of data points per category exceeds what a table cell can hold meaningfully

### 2. China section is substantively absent

The report dedicates significant space to PMI/IQOS, BAT/glo, JTI/Ploom, and KT&G/lil, but gives China's HNB landscape only this sentence:

> "中国烟草体系以 MC（Mudu Cell）等品牌切入海外市场，但国内受政策严格限制。"

This is a significant gap. China is the world's largest tobacco market. Domestic HNB policy is a critical variable: if restrictions loosen, it represents a massive market opportunity or threat. The report's failure to cover China's current domestic HNB status, key players (MC, CRISP, etc.), regulatory status, and potential scenarios means the "global HNB market" analysis is materially incomplete.

**This is a content scope failure**, not a table formatting issue. The model should have asked: "What are the five largest tobacco markets globally, and what is the HNB status in each?"

### 3. "减害" narrative vs regulatory risk not structurally reconciled

The report presents "减害定位" as a core investment logic and separately lists "监管收紧风险高" as a core risk. These two points exist in parallel without being forced into a structured tension analysis.

The model should have asked:
- How strong is the medical evidence for HNB harm reduction?
- What has the FDA's recent posture been toward MRTP (Modified Risk Tobacco Product) designations for HNB?
- In how many markets has HNB been granted tax parity with cigarettes vs. been taxed at comparable rates?

Without this analysis, the report has two parallel narratives that do not touch each other.

### 4. Forward-looking estimate without source attribution (recurring)

> "预计 2025–2030 年维持 8–12% 增速 [LIKELY]"

The [LIKELY] label is present, but there is no named source. Is this from Euromonitor? Mordor Intelligence? Company guidance? An internal inference? This is the same failure mode documented in the BYD GPT vs Minimax distillation case — the skill has the rule, but enforcement is inconsistent.

---

## Failure modes summary

| Failure | Severity | Related skill rule |
|---------|----------|-------------------|
| Super-sized comparison table (6 cols × 7 dims) with low information density per cell | Medium | `report-template.md` — table formatting discipline (new) |
| China HNB landscape substantively absent | High | `current-state-verification.md` — fast-moving market scope check |
| "减害" vs regulatory risk not structurally reconciled | Medium | `counter-evidence.md` — opposing-narratives analysis |
| "预计" without named source attribution | Medium | `finance-date-discipline.md` — estimate sourcing rule |

---

## Lessons

1. **Table width vs. information density is a design decision, not a formatting one.** When building multi-category comparison tables, the question to ask is: "Can a reader extract one meaningful insight from each cell?" If not, split the table. This is a structural decision that no rendering pipeline can fix.

2. **Geographic scope checklist should be mandatory for global industry reports.** A report on a global market should explicitly cover: top 5 markets, their regulatory status, and key local players. "China has a policy restriction" is not equivalent to "China is covered."

3. **This eval complements the HNB table design case as a combined structural + content failure.** The table problem is visible and fixable; the China gap requires more deliberate research scope setting before collection begins.

4. **Eval conclusion:** Add this as a **table design + content scope** case. The evidence tier system shows the model can follow the labeling rules. The execution gaps are in structural design (table layout, scope completeness) rather than knowledge.
