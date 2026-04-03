# MiniMax SEA Memo PDF Layout Case

## Case identity

- **Task type:** PDF delivery / rendering-layer + information-design review
- **Artifact:** MiniMax-generated PDF for a SEA market-entry decision memo
- **Date:** 2026-04-03
- **Why this case matters:** 该案例同时暴露了 PDF 渲染硬伤与 decision-memo 信息设计不足，适合作为“哪些该归入 pipeline、哪些该归入输出模板”的分流样本。

---

## Observed failure families

### 1. CJK rendering / spacing failure

Visible symptoms:
- Chinese characters appeared visually torn apart or over-spaced
- headings such as `决 策 备 忘录` and `进 ⼊ 东 南 亚 市 场` looked broken
- the PDF felt closer to a damaged export or OCR-like artifact than to a polished memo

Why it matters:
- this is a first-glance trust failure
- readers lose confidence before engaging the reasoning
- even strong content looks unfinished when the base text texture is visibly broken

Likely home:
- `scripts/markdown_to_html.py`
- PDF rendering / CSS / text-normalization pipeline

---

### 2. Weak scan anchors

Visible symptoms:
- section headings existed but did not create strong visual anchors
- the page still felt like continuous explanation rather than decision blocks
- the eye could not quickly isolate recommendation, hard gates, shortlist, and execution path

Why it matters:
- decision memos should support 30-second scan, 2-minute framework read, and 5-10 minute deeper review
- without strong anchors, the memo behaves like a long report even if the headings are technically present

Likely home:
- `references/report-template.md`
- `references/decision-report-template.md`
- secondarily CSS / heading spacing in the PDF pipeline

---

### 3. Country analysis as prose rather than shortlist object

Visible symptoms:
- country sections were readable but still felt like topic exposition
- comparison logic was not visually amplified
- table usage did not clearly outperform plain prose in scan efficiency

Why it matters:
- multi-country entry memos need comparison-first layout, not country-tour layout
- if the page does not make ranking legible, the memo underperforms as decision support

Likely home:
- `references/report-template.md`
- `references/decision-report-template.md`
- `checklists/option-selection-final-audit.md`

---

### 4. Hard gates not visually isolated

Visible symptoms:
- conditions for entry existed in substance, but were not elevated into a clear block
- the reader had to read through prose to understand what would make the answer become `not now`

Why it matters:
- for go/no-go work, gates should not be buried inside analysis
- they should survive skim reading and executive discussion

Likely home:
- `references/report-template.md`
- `references/decision-report-template.md`
- final-audit gates

---

## Distilled conclusion

This case should not be reduced to “the PDF looked ugly.”

It exposed two distinct repair tracks:

1. **Rendering-layer failure**
   - CJK spacing / text texture / page rhythm / weak visual anchors
2. **Information-design failure**
   - recommendation, hard gates, shortlist, and sequencing were not sufficiently elevated into typed memo blocks

The right response is to keep those two tracks separate:
- pipeline fixes should make the PDF look stable and readable
- template/checklist fixes should make the memo behave like a decision artifact instead of a long regional overview

---

## Candidate actions

| # | Candidate action | Failure family | Action type | Proposed home |
|---|---|---|---|---|
| 1 | Improve CJK text rhythm defaults and paragraph/list spacing in PDF rendering | output structure / information density | TEMPLATE_CHANGE | `scripts/markdown_to_html.py` |
| 2 | Add explicit market-entry memo formatting discipline to the default report template | decision utility / output structure | NEW_RULE | `references/report-template.md` |
| 3 | Keep hard gates, shortlist, and phased-entry logic as visible blocks rather than prose | decision utility / execution failure | CHECKLIST_HARDENING | `references/decision-report-template.md` + `checklists/final-audit.md` |

---

## Final judgment

The biggest lesson from this PDF is not “make it prettier.”

It is:
- first, make the PDF stop looking broken
- second, make the page layout serve the decision

A decision memo that looks like a damaged export and reads like a long market explainer is failing both the rendering layer and the decision-support layer.
