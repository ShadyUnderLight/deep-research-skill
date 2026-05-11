# PDF Delivery Trigger Regression Case

## Case identity

- **Task type:** PDF delivery trigger rule boundary test
- **Artifact:** `SKILL.md` Delivery rule — natural language trigger for PDF pipeline
- **Date:** 2026-05-11
- **Why this case matters:** 中文场景中"报告"是高频词，过宽的 PDF 触发规则会导致不必要的 Playwright 渲染，增加失败面和交付延迟。这个 case 把 issue #69 的验收标准沉淀为可复现的回归矩阵，防止后续 prose 修改漂移触发边界。

---

## Acceptance matrix

Each row is a user request fragment. The agent should decide whether to produce a PDF artifact in addition to the default markdown/text.

| Input | Expected PDF | Why |
|---|---|---|
| 写一份报告 | No | generic report terminology, no file intent |
| 写成研究报告格式 | No | format instruction only, not file request |
| 这个报告帮我改一下 | No | editing request, not delivery request |
| 给我一份研究报告 | No | report content request, no file format specified |
| 生成 PDF 报告 | Yes | explicit "生成 PDF" |
| 导出 PDF | Yes | explicit "导出 PDF" |
| 保存为 PDF | Yes | explicit "保存为 PDF" |
| 给我 PDF 文件 | Yes | explicit file + PDF |
| 给我报告文件 | Yes | explicit file-delivery intent |
| 可下载报告 | Yes | downloadable file intent |
| 正式报告文件 | Yes | formal file deliverable |
| 交付一个文件 | Yes | explicit file deliverable |
| 附件是报告 | Yes | attachment = file deliverable |
| 不要生成 PDF，只要 markdown | No | negation of PDF |
| 解释一下 PDF 渲染为什么失败 | No | meta-discussion, not a request |
| 比较 PDF 和 Markdown 的优缺点 | No | comparison/discussion, not delivery |
| 为什么上次 PDF 输出格式乱了 | No | debugging question, not a request |
| 生成财务报表 PDF | Yes | explicit "生成" + "PDF" |
| 给我一份可下载的 PDF 版本 | Yes | downloadable file + PDF |

## Regression rules

1. PDF trigger must not fire on generic "报告" without file-delivery intent
2. PDF trigger must not fire on negated or discussion-context `pdf`/`PDF` mentions
3. PDF trigger must fire on explicit file-delivery phrases even without the literal string "PDF"
4. `pdf` / `PDF` substrings alone are sufficient only when the surrounding context is generative or delivery-oriented, not meta-discussion

## Related

- Issue #69
- `SKILL.md` Delivery rule
