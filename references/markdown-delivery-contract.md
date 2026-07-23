# Markdown-first Delivery Contract

Use this contract when the reader will primarily consume the final `.md` file.
It is a reader-facing layer, separate from the research/content requirements in
`references/report-template.md` and the HTML/PDF pipeline in
`references/delivery-operator-note.md`.

The goal is not to make every report look identical. The goal is to make the
answer easy to locate, scan, verify, and revisit in plain Markdown, Obsidian,
GitHub, or a similar reader.

## Activation and boundaries

- Markdown/text delivery is the default, so apply this contract before drafting
  the final report.
- If the user explicitly requests PDF, apply this contract first, then run the
  separate PDF/HTML delivery checks. Page breaks, cover pages, and CSS do not
  belong in the Markdown contract.
- `references/report-template.md` still controls research content, evidence,
  route, and audit requirements. This file controls reading order, density,
  heading shape, and reader-visible scaffolding.
- A Research Pack remains a process artifact. Do not paste the complete pack,
  search log, tool trace, or internal deliberation into the reader-facing body.
- Route/audit status and the structured Source Register remain required when
  the applicable validator or route contract requires them; place them after
  the narrative as appendices so they remain discoverable without taking over
  the opening.

## Reader goals

A reader opening the file should be able to answer these questions quickly:

1. What is the current judgment?
2. What are the two to five variables that drive it?
3. Which parts are confirmed, inferred, or still unknown?
4. What evidence supports the judgment, and what could overturn it?
5. What should happen next?

## Document shape

### 1. Metadata and title

Use one H1 and, when the file is stored or indexed in a Markdown vault,
prefer lightweight YAML frontmatter:

```yaml
---
title: "报告标题"
date: 2026-07-23
type: decision-report
route: shared-workflow
status: final
---
```

Keep frontmatter short. Put the actual thesis in the body rather than hiding
it in metadata. Do not add PDF-only cover instructions, page numbers, or CSS
classes to the Markdown.

### 2. Judgment card before background

Immediately after the title, show a compact, portable blockquote. It should
contain no more than four lines:

```markdown
> **核心判断**：一句话回答用户真正要判断的问题。
>
> **置信度**：中；限制来自……
>
> **结论范围**：本判断只适用于……
>
> **改变条件**：如果……，结论将转向……
```

For English reports, use `Core thesis`, `Confidence`, `Scope`, and
`What would change this view`. Keep this block before the first background
paragraph or market/company history section.

### 3. Executive summary

Use a heading that preserves a stable English alias for tooling when useful:

```markdown
## 执行摘要（Executive summary）
```

Use four to eight short bullets. Each bullet should carry one idea and, when
it is load-bearing, one evidence label and source ID:

```markdown
- [确认] 已发生的事实，以及它对判断的直接影响。[S01]
- [推断] 基于两项证据得出的方向性判断。[S02][S04]
- [未知] 公开资料仍无法确认的变量，以及它为什么重要。
```

For English reports, use `[CONF]`, `[INFER]`, and `[UNKN]`. For Chinese
reports, prefer `[确认]`, `[推断]`, and `[未知]`; do not mix the two label
systems within one report. Labels belong on load-bearing claims, not every
sentence.

### 4. Main narrative

Use H2 headings for the major decision path and H3 headings for its parts.
The opening 20–30% should already contain the answer, not only methodology or
background. A normal Markdown-first sequence is:

1. `执行摘要（Executive summary）`
2. `最关键变量（What matters most）`
3. `关键发现（Key findings）`
4. `详细分析（Detailed analysis）`
5. `风险与反证（Risks and counter-evidence）`
6. `不确定性与缺失证据（Uncertainty and missing evidence）`
7. `结论（Bottom line）`
8. `建议的下一步（Recommended next steps）`
9. `附录：路由与审计状态（Route and audit status）`
10. `附录：来源登记（Source Register）`

Adapt or remove sections when the route does not need them, but do not move
background ahead of the judgment merely to fill the template. For reports
longer than roughly six major sections, add a short `阅读导航` block near the
top or rely on the reader's outline view; do not create a manually maintained
table of contents if it is likely to become stale.

### 5. Section takeaway block

For each major H2 section, put the section judgment before the supporting
detail. A compact portable pattern is:

```markdown
> **本节判断**：这一节改变或强化了什么结论？
>
> **主要驱动**：最重要的证据或变量是什么？
>
> **主要风险 / 关键未知**：什么限制了结论？
```

Use this on major sections, not every small H3. Keep it to two or three
sentences/lines so it remains a reading aid rather than another summary layer.

## Markdown readability rules

### Paragraphs and lists

- Keep one main judgment per paragraph; use the first sentence as the point.
- Prefer two to five sentences per paragraph. Break longer reasoning into a
  short judgment, evidence bullets, and a limitation.
- Use bullets for risks, unknowns, counter-evidence, change conditions, and
  next steps. Avoid a single bullet containing a mini-essay.
- Use bold for labels or the key phrase, not for whole paragraphs.
- Leave a blank line around headings, lists, blockquotes, tables, and fenced
  code blocks. Do not use HTML/CSS merely to create visual spacing.

### Tables

Use a table only when the reader needs row/column comparison. For normal body
tables:

- target six columns or fewer; split a wide table by decision dimension;
- put units and time scope in the header or immediately above the table;
- keep one fact or one judgment in each cell;
- after the table, write one or two sentences explaining what matters;
- use bullets or compact cards for narrative evidence, risks, and unknowns;
- keep the seven-column Source Register as the explicit appendix exception.

Do not end a major section with an unexplained data dump. Do not mix observed
numbers, proxies, assumptions, and model outputs without a visible numeric-role
label at row, column, or table level.

### Evidence and links

- Keep the existing `[S01]`-style source IDs so body claims map to the Source
  Register. When a direct source link improves reading, use `[S01](URL)`;
  otherwise keep `[S01]` and make the register entry clickable.
- Put the evidence label next to the claim it qualifies: `[确认] [S01]`,
  `[推断] [S02]`, or `[未知]`.
- Use descriptive Markdown link text in the Source Register instead of long
  raw URLs when the renderer supports it.
- Do not put retrieval traces, tool names, raw search snippets, or internal
  citation placeholders in the final body.

### Appendices and internal scaffolding

Keep the narrative clean while preserving auditability:

```markdown
## 附录：路由与审计状态（Route and audit status）

...标准化审计状态表...

## 附录：来源登记（Source Register）

...七列表格...
```

The stable English aliases in parentheses are intentional: they keep the
reader-friendly Chinese headings compatible with existing validators and
cross-report tooling. Do not rename an audit to a prose description only.

## Delivery acceptance checklist

Before delivering a Markdown report, confirm:

- [ ] exactly one H1; heading levels do not skip from H2 to H4;
- [ ] the first screen contains the title, judgment card, and executive
      summary, before detailed background;
- [ ] the executive summary has four to eight scannable bullets unless the
      task is genuinely too small for that shape;
- [ ] major sections use a visible section judgment before evidence detail;
- [ ] load-bearing claims have an evidence label and `[Sxx]` citation where
      applicable;
- [ ] regular tables are narrow, titled or scoped, and interpreted afterward;
- [ ] route/audit status and Source Register are present in the required
      stable form, usually as appendices;
- [ ] no placeholders, retrieval traces, internal deliberation, or parser
      residue remain in the final body;
- [ ] `python3 scripts/validate_markdown_delivery.py <report>.md` passes;
- [ ] if PDF was requested, the separate PDF pipeline and visual check also
      pass.

## Minimal Markdown-first skeleton

```markdown
---
title: "……"
date: YYYY-MM-DD
type: decision-report
route: …
status: final
---

# ……

> **核心判断**：……
>
> **置信度**：……
>
> **结论范围**：……

## 执行摘要（Executive summary）

- [确认] …… [S01]
- [推断] …… [S02]
- [未知] ……
- 下一步：……

## 最关键变量（What matters most）

> **本节判断**：……
>
> **主要驱动**：……
>
> **主要风险 / 关键未知**：……

## 关键发现（Key findings）

……

## 详细分析（Detailed analysis）

### ……

……

## 风险与反证（Risks and counter-evidence）

- ……

## 不确定性与缺失证据（Uncertainty and missing evidence）

- ……

## 结论（Bottom line）

……

## 建议的下一步（Recommended next steps）

1. ……

## 附录：路由与审计状态（Route and audit status）

……

## 附录：来源登记（Source Register）

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|---|---|---|---|---|---|---|
| S01 | …… | primary | YYYY-MM-DD | [链接](URL) | high | §2 |
```
