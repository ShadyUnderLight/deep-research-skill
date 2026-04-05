# MiniMax Company Report Eval

**Date:** 2026-03-31
**Model:** Minimax (MiniMax-M2)
**Source:** User-provided PDF from a Minimax-generated deep research report on MiniMax

## Research question
MiniMax company deep research report (Chinese, structured format)

## What went well

### 1. Active listing-state awareness (positive behavior change)
The report explicitly flagged in its research note:
> "⚠ 因 MiniMax 已于 2026 年 1 月 9 日港交所上市（代号 00100）"

This is a meaningful improvement over earlier listed-company cases (Moore Threads). The model recognized the listing event and called it out in the research scope section — unlike Moore Threads reports which froze at Pre-IPO language.

### 2. Research scope statement
The opening research note included data-source disclosure (招股书、港交所公告、多方媒体报道) and a datafreshness caveat. This is consistent with the source-quality discipline.

### 3. Inference label used in competitive pressure section
Section 4.4 used "Likely Inference + Risk Factor" label when discussing DeepSeek's impact on the "六小虎" group. This matches the skill's inference-labeling requirement.

### 4. Time layering in financing table
The financing table separated rounds by date and gave specific amounts, matching the finance-date discipline for historical milestone separation.

---

## What went wrong

### 1. Report is structurally incomplete (戛然而止)
The report terminates mid-sentence at section "5.2 主要应用场景" with no:
- Chapter 6: Financial depth (post-IPO audited or interim results)
- Chapter 7: Risk analysis
- Chapter 8: Bull/Bear logic

This is a structural failure — a listed-company deep research report without financial analysis or bull/bear framing is incomplete by the skill's own output standards.

### 2. Listed-company current market snapshot missing (rule existed but not followed)
`references/finance-date-discipline.md` already mandates: "For any listed-company research, a current valuation snapshot is required, not optional." The report is about a listed company (MiniMax, HK00100, listed 2026-01-09) but has no current stock price, market cap, or post-IPO trading data anywhere.

This means the existing rule was either:
- not triggered (compaction didn't retain it), or
- not followed despite being in the skill

The report relied entirely on pre-IPO prospectus data for financial figures.

### 3. Source citation at generic level, not claim-level
All claims cited sources like "招股书披露" or "MiniMax官网" without:
- specific section/chapter or page number
- direct URL
- publication date

Readers cannot verify any individual claim. This is the same failure mode documented in `source-traceability-moore-threads-case.md` — the model improved source awareness but not citation granularity.

### 4. Ranking claims without evidence chain
The report stated:
- "全球唯一四"进入第一梯队的大模型公司之一
- "第一梯队"是谁/什么机构划分的？没有任何证据

These are marketing-level ranking assertions. The skill's `references/ranking-and-current-claims-discipline.md` and the Xiaomi update case (`ranking-and-current-claims-xiaomi-update-case.md`) both address this failure mode. It is present here again.

### 5. Competitive positioning lacks quantitative backing
Section 4.2 describes differentiation qualitatively ("多模态先驱者"、"出海成绩突出") but provides no specific metrics:
- No user growth trend for Starfield/Talkie vs competitors
- No market share data for video generation
- No revenue breakdown by segment

---

## Failure modes summary

| Failure | Severity | Related skill rule or prior eval |
|---------|----------|----------------------------------|
| Listed company report with no current market snapshot | High | `finance-date-discipline.md` — rule existed |
| Source citation at document level, not claim level | Medium | `source-traceability-moore-threads-case.md` |
| Ranking claims ("全球唯一四") lack evidence | Medium | `ranking-and-current-claims-xiaomi-update-case.md` |
| Report structurally incomplete (no financial, risk, bull/bear) | High | SKILL.md output standards |
| Report戛然而止 at section 5.2 | Medium | — possibly upload artifact issue |

---

## Lessons

1. **Listing-state awareness improved**: The model correctly identified the listing event. This is a genuine behavior improvement over the Moore Threads case. The awareness exists; enforcement is the gap.

2. **Knowing a rule ≠ following it**: The current market snapshot rule was in the skill but not triggered. This suggests compaction or execution routing dropped it. The fix should be structural (checklist-level enforcement), not just adding more prose rules.

3. **Incomplete reports**: If the report generation was interrupted (API error) rather than an artifact upload issue, the skill's stop conditions may need review. If it was allowed to terminate at "5.2" without hitting a stop condition, the completion gate needs tightening.

4. **Eval conclusion**: Add this as a mixed-behavior case — positive on listing-state awareness, negative on execution follow-through. The listing-state awareness improvement is worth codifying as a behavior the skill should reinforce.
