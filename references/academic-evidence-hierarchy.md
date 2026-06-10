# Academic Evidence Hierarchy

Use this file when the research task involves academic literature, peer-reviewed research, preprints, conference papers, or patent literature.

This discipline applies when the core question is **understanding academic evidence, evaluating research quality, or surveying field progress** — not product selection, vendor comparison, or market sizing.

## When to use

Apply this discipline when the task involves:

- literature review or systematic review (文献综述 / 系统性综述)
- academic field progress analysis (学术领域进展分析)
- paper comparison or methodological evaluation (论文对比分析)
- technology origin tracing through academic publications (技术溯源)
- research quality assessment (研究质量评估)

## When NOT to use

Do not use this discipline when:

- the task is mainly about technology principles or architecture → use **Technical Deep-dive**
- the task is mainly about product or vendor selection → use **Provider / Vendor Selection**
- the task is mainly about market evolution → use **Market Outlook / Industry Evolution**
- the task is about company evaluation → use **Listed Company** or **Private Company**

## Evidence hierarchy

Academic evidence evaluation has two orthogonal dimensions:

1. **Study design quality** — how the research was conducted
2. **Publication venue prestige** — where it was published

Both dimensions matter. A well-designed RCT published in a top journal is stronger than a poorly designed RCT in a predatory journal. A cohort study in Nature is stronger than a cohort study in an obscure journal.

### Dimension 1: Study design quality

Use this hierarchy when evaluating **how the research was conducted**:

| Level | Study design | Description | Typical strength |
|-------|--------------|-------------|------------------|
| 1 | Meta-analysis | Systematic pooling of multiple studies | Strongest for synthesizing evidence |
| 2 | Systematic review | Structured literature search with inclusion/exclusion criteria | Strongest for comprehensive literature survey |
| 3 | Randomized controlled trial (RCT) | Gold standard for causal inference | Strongest for intervention effects |
| 4 | Cohort study | Observational study following a population over time | Good for longitudinal associations |
| 5 | Case-control study | Comparing groups with/without outcome | Moderate for rare outcomes |
| 6 | Cross-sectional study | Snapshot of a population at one time point | Weak for causal claims |
| 7 | Case report / Case series | Single or small number of cases | Weakest for generalizability |

### Dimension 2: Publication venue prestige

Use this hierarchy when evaluating **where the research was published**:

| Level | Venue type | Description | Examples |
|-------|------------|-------------|----------|
| 1 | Top-tier journal | Highest prestige, most rigorous peer review | Nature, Science, NEJM, Lancet, PNAS |
| 2 | Field-specific top journal | Top venue in a specific field | JAMA, Cell, ICML, NeurIPS, CVPR, ACL |
| 3 | Peer-reviewed journal | Standard peer-reviewed publication | Field-specific journals, regional journals |
| 4 | Peer-reviewed conference | Peer-reviewed but typically shorter | Field-specific conferences (CS, engineering) |
| 5 | Preprint | Not yet peer-reviewed, use with caution | arXiv, bioRxiv, medRxiv, SSRN |
| 6 | Working paper | Preliminary version, often in economics | NBER, IZA working papers |
| 7 | Technical report | Institutional publication, variable quality | Company research labs, government agencies |
| 8 | Thesis / Dissertation | Student work, variable quality | Institutional repositories |

### Combined evidence assessment

When evaluating a source, combine both dimensions:

```
[Study design level] × [Venue prestige level] = Evidence strength
```

**Examples**:
- Meta-analysis in Nature → Level 1 × Level 1 = Strongest
- RCT in NEJM → Level 3 × Level 1 = Very strong
- Cohort study in field journal → Level 4 × Level 3 = Moderate
- Preprint of RCT → Level 3 × Level 5 = Moderate (high design, low venue)
- Conference paper of empirical study → Level 4 × Level 4 = Moderate

**Important**: Do not conflate the two dimensions. A preprint of an RCT (high design quality, low venue prestige) is not the same as a published case report (low design quality, moderate venue prestige).

### 双维证据强度评估表（推荐格式）

在评估每个来源时，使用以下表格同时标注两个维度。此表应在报告的「证据质量评估」或「来源分析」章节中呈现。

| 来源 | 研究设计质量 (Level) | 发表场所声誉 (Level) | 综合评估 |
|------|---------------------|---------------------|---------|
| [S1] | Level 3: RCT | Level 1: NEJM | 强 |
| [S2] | Level 4: 队列研究 | Level 3: 同行评议期刊 | 中等 |
| [S3] | Level 6: 横断面研究 | Level 1: 顶级期刊 | 中等 |
| [S4] | Level 3: RCT (预印本) | Level 5: 预印本 | 中等 |
| [S5] | Level 7: 案例报告 | Level 2: 领域顶刊 | 弱 |

**说明**：
- 研究设计质量等级见上文「Dimension 1: Study design quality」表格
- 发表场所声誉等级见上文「Dimension 2: Publication venue prestige」表格
- **综合评估规则**：
  - **强**：研究设计 Level 1-3 **且** 发表场所声誉 Level 1-2（高质量研究在顶级/领域顶级期刊）
  - **弱**：研究设计 Level 7-8 **或** 发表场所声誉 Level 6-8（案例报告/论文/预印本/技术报告，或工作在极低声誉场所发表）
  - **中等**：以上两者之外的其余组合
- 此表格是报告证据分级的一部分，不替代正文中的 `[确认事实]/[推断]` 标签——两者是互补关系：表格展示来源级评估，标签是声明级置信度

### Discipline-specific venue prestige

The venue prestige hierarchy varies by discipline:

#### Computer Science / Engineering
- **Top-tier conferences** (NeurIPS, ICML, CVPR, ACL, SIGCOMM, OSDI) are the primary publication venues
- Conference papers are often more prestigious than journal articles
- Preprints (arXiv) are widely accepted and often cited before peer review
- Journal publications are less common and often extended versions of conference papers

#### Medicine / Biomedical
- **Top-tier journals** (NEJM, Lancet, JAMA, Nature Medicine) are the primary venues
- RCTs and systematic reviews are the gold standard
- Conference abstracts are preliminary; full papers are expected in journals
- Preprints (bioRxiv, medRxiv) should be treated with extra caution

#### Social Sciences / Economics
- **Top-tier journals** (AER, QJE, Econometrica, APSR) are the primary venues
- Working papers (NBER, IZA) are a major venue and often cited
- Conference papers are less formal; journal publications are the standard
- Preprints are less common; working papers serve a similar role

#### Physics / Mathematics
- **Preprints** (arXiv) are the primary venue and widely accepted
- Journal publication is a formality; peer review happens after community validation
- Conference papers are less common; journal articles are the standard
- Venue prestige matters less than community recognition

**When in doubt**: Check the norms of the specific field. A CS conference paper at NeurIPS is not "less rigorous" than a journal article — it's the primary publication venue.

## Source labeling requirements

When citing academic sources, **always label**:

1. **Title**: paper title (e.g., "Attention Is All You Need")
2. **Publication type**: published / preprint / conference / working paper / unpublished
3. **Peer-review Status**: peer-reviewed / not peer-reviewed / unknown
4. **Publication venue**: journal name, conference name, or repository
5. **Publication date**: year (and month if available for fast-moving fields)
6. **DOI/URL**: when available

Example labeling:
```
- [Published, Peer-reviewed] Vaswani et al. (2017). "Attention Is All You Need." NeurIPS 2017. DOI: xxx
- [Preprint, Not peer-reviewed] Smith et al. (2024). "Scaling Laws for LLMs." arXiv:2401.xxxxx
```

### 每个 [S#] 条目必填字段

报告中的每个来源条目（`[S#]`）必须包含以下字段：

| 字段 | 说明 | 示例 |
|------|------|------|
| **标题** | 论文/报告标题 | "Attention Is All You Need" |
| **Publication type** | 原始研究/综述/预印本/工作论文/会议论文/书籍章节/报告 | original research / review / preprint |
| **Peer-review Status** | 同行评审状态 | peer-reviewed / preprint / unknown |
| **Venue** | 期刊名/会议名/出版商 | NeurIPS 2017 / arXiv |
| **DOI/URL** | 永久标识符或可访问链接 | 10.xxxx/xxxxx 或 https://... |
| **Date** | 发表日期（至少年份） | 2017 |

此要求与 `references/source-traceability-and-claim-citation.md` 中的结构化 source register 要求一致，是学术路由来源标注的具体扩展。

### Source Register 扩展模板（Academic 专用）

Academic / Literature Review 路线的 Source Register 必须在 7 列基础模板之上增加 4 列学术附加元数据，形成 11 列扩展模板：

| # | 列名 | 说明 | 示例 |
|---|------|------|------|
| 1 | **ID** | 来源编号 | S01 |
| 2 | **Source Name** | 论文/报告标题 | "Attention Is All You Need" |
| 3 | **Source Type** | 来源类型（5 类简化或 8 类粒度） | primary |
| 4 | **Date** | 发表日期（至少年份） | 2017 |
| 5 | **DOI/URL** | 永久标识符或可访问链接 | 10.xxxx/xxxxx |
| 6 | **Reliability** | 可靠性评级 | high / medium / low |
| 7 | **Claims Supported** | 正文引用章节 | §3.1, §4.3 |
| 8 | **Publication Type** | 研究类型 | original research / survey / benchmark / position paper / review / case report |
| 9 | **Peer-review Status** | 同行评审状态 | peer-reviewed / preprint / working paper / unpublished / unknown |
| 10 | **Venue** | 发表场所 | NeurIPS 2017 / arXiv / Nature |
| 11 | **Venue Prestige** | 场所声誉等级（如适用） | Tier 1 — Tier 7（见上文「Dimension 2: Publication venue prestige」） |

**Register 表格示例：**

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported | Publication Type | Peer-review Status | Venue | Venue Prestige |
|----|-------------|-------------|------|---------|-------------|-----------------|-----------------|-------------------|-------|---------------|
| S01 | Attention Is All You Need | primary | 2017 | 10.xxxx/xxxxx | high | §2.1, §4.3 | original research | peer-reviewed | NeurIPS 2017 | Tier 2 |
| S02 | Scaling Laws for LLMs | primary | 2024 | arXiv:2401.xxxxx | medium | §2.2 | original research | preprint | arXiv | Tier 5 |
| S03 | LLM Safety Survey | secondary | 2025 | 10.xxxx/yyyyy | medium | §3.1 | survey | peer-reviewed | ACM Computing Surveys | Tier 3 |

**规则说明：**
- 此 11 列模板是 7 列基础模板的学术扩展，仅适用于 Academic / Literature Review 路线。非学术路由仍使用 7 列基础模板。
- **Publication Type**（第 8 列）：标注研究设计性质，帮助读者区分原始研究与综述等次级文献。
- **Peer-review Status**（第 9 列）：区分已同行评审发表、预印本、工作论文；预印本必须标注 `preprint`，不得标为 `peer-reviewed`。
- **Venue**（第 10 列）：标注具体期刊/会议/仓库名称，不得仅写 "journal" 或 "conference"。
- **Venue Prestige**（第 11 列）：当报告使用了证据层级框架（双维评估）时必填；否则可填 `N/A`。
- 如果某个来源不适合标注全部 11 列（如灰色文献、技术报告），缺少的列应注明原因（如 "venue prestige: N/A — technical report"），不可直接省略。

## Statistical assessment

When evaluating quantitative research, check:

### Study design
- Sample size: is it adequate for the claimed effect size?
- Control group: is there a proper comparison?
- Randomization: how were participants assigned?
- Blinding: single / double / triple / open-label?

### Statistical claims
- **p-value**: statistical significance (typically p < 0.05)
- **Effect size**: practical significance (Cohen's d, odds ratio, etc.)
- **Confidence interval**: range of plausible values
- **Multiple testing**: were corrections applied? (Bonferroni, FDR)
- **Power analysis**: was the study powered to detect the claimed effect?

### Common statistical pitfalls
- p-hacking: testing many hypotheses without correction
- Cherry-picking: reporting only significant results
- Confounding: correlation ≠ causation
- Selection bias: non-representative samples
- Publication bias: positive results more likely published

## 检索策略文档化

当报告涉及文献检索时（尤其是自称"系统化综述"或"有限范围系统化综述"时），必须按以下要求文档化检索策略。此要求参考 PRISMA 2020 指南（简化版）。

### 必须包含（Mandatory）

- **检索数据库列表**：列出所有检索的数据库（如 PubMed, Web of Science, Google Scholar, Semantic Scholar, arXiv, IEEE Xplore, CNKI, Scopus 等），注明各数据库的覆盖范围和检索时间
- **检索词组合**：包含关键词 + 布尔运算符（AND/OR/NOT），以及所使用的字段标签（title/abstract/keywords）和任何限制条件（如 MeSH terms）
- **纳入/排除标准**：时间范围、语言、研究类型（RCT / 观察性研究 / 系统化综述 / 综述 / 灰色文献）、发表日期范围、样本量阈值（如适用）
- **筛选流程数量**：初筛结果数 → 再审结果数 → 最终纳入数；如适用说明排除原因
- **检索日期**：明确记录检索执行日期

### 推荐但不强制（Recommended）

- **PRISMA 流程图**：适用于系统性综述报告，直观展示筛选流程各阶段的文献数量
- **文献管理工具**：如 Zotero, EndNote, Mendeley，便于追踪筛选过程和管理引用

### 筛选流程完整性

当报告使用"有限范围"限定词时，仍应在能力范围内完整记录检索策略；"有限范围"不应成为跳过检索策略文档化的借口。

### 检索策略模板

当报告涉及文献检索时，请直接填充此模板（参考 PRISMA 2020 简化版）：

```markdown
## 检索方法
- 检索数据库：PubMed / Web of Science / Google Scholar / CNKI / …
- 检索词组合：(keyword1 AND keyword2) OR (keyword3 AND keyword4)
- 检索日期：YYYY-MM-DD
- 纳入标准：语言、时间范围、研究类型
- 排除标准：…
- 筛选流程：初筛 ___ 篇 → 再审 ___ 篇 → 纳入 ___ 篇
```

填充后的检索策略应放在报告正文的「检索方法」或「方法论」章节中。此模板适用于系统化综述和有限范围系统化综述；对于非系统化综述，填写可用的字段即可。

## 措辞纪律 (Wording Discipline)

### 核心规则

在学术文献回顾类报告中，方法学措辞必须与实际执行的检索策略透明度相匹配：

- **"系统评述"/"系统综述"/"系统化综述"/"systematic review"**：暗示检索过程符合结构化标准（如 PRISMA 简化版）。只有报告完整文档化检索方法（数据库列表、检索日期、Boolean query、纳入/排除标准、screening counts）时方可使用。
- **替代措辞**：如果方法学达不到上述标准，应使用与透明度匹配的更精确措辞——

| 实际透明度 | 推荐措辞 |
|-----------|---------|
| 完整检索文档（数据库 + 检索式 + 筛选计数 + 日期） | 系统评述 / 系统综述 / 系统化综述 / systematic review |
| 有检索词和时间范围，但缺筛选计数或部分字段 | 文献回顾 / literature review / narrative review |
| 有明确检索策略但范围有限 | 有限范围系统化综述 / scoping review |
| 通过明确检索词和数据库获取文献 | 系统检索 / systematic search |

### 违规范例

以下情况视为措辞纪律违规：
- ❌ 声称"系统评述"/"系统综述"/"系统化综述"但未列出检索数据库
- ❌ 声称"约80篇文献的系统性回顾"但无筛选流程计数（初筛→再审→纳入）
- ❌ 正文描述"有限范围系统化综述"但无检索日期或纳入标准

### 通过范例

以下情况通过措辞纪律检查：
- ✅ 使用"文献回顾"/"literature review"/"narrative review"措辞且检索步骤透明 → 通过
- ✅ 使用"系统检索"/"systematic search"措辞且列明数据库、检索词、日期 → 通过
- ✅ 符合最低筛选计数标准的"有限范围系统化综述"/"scoping review"且检索文档完整 → 通过

「发表偏倚讨论」的触发条件判断与此措辞纪律无关：即使使用"文献回顾"措辞，只要话题属于争议性或多因素归因类，仍须包含发表偏倚讨论。

## 发表偏倚讨论

### 触发条件

当话题属于以下类别之一时，报告**必须**包含发表偏倚讨论：

- **争议度话题**：学术领域存在明显对立的研究立场或相互矛盾的发现
- **多因素归因研究**：null result（"因素 X 无显著影响"）与 positive result 具有同等信息价值。仅呈现正面结果会产生系统性的发表偏倚

### 最低要求

至少 2-3 句，涵盖：
1. **偏倚方向判断**：本报告所引用的文献集是否更可能包含正面结果？是否存在"抽屉问题"（file drawer problem）的系统性偏差？
2. **结论调整建议**：如果发表偏倚可能存在，报告的结论应如何调整（方向、幅度、置信度）？

### 非争议性话题

对于无明显争议或不存在明显发表偏倚倾向的话题（如成熟的、共识度高的领域），发表偏倚讨论可以简化，但**不能完全跳过**：

- **可接受的替代形式**：注明"本话题发表偏倚风险较低，理由如下：[简要阐述为什么该领域不太受抽屉问题影响]"
- 此简要备注**满足**本研究方法论文档对发表偏倚讨论的最低要求（即可通过 checklist 检查），前提是理由判断合理
- **不推荐完全省略**：即使话题看似无争议，简要记录理由也展示了方法论透明度

### 发表偏倚讨论模板

当话题满足触发条件（见上文「触发条件」）时，请直接填充此模板：

```markdown
**发表偏倚讨论**：本研究涵盖的主题存在[正/负/不确定]方向发表偏倚的可能——[说明偏倚方向及对结论的影响]。因此本报告的核心结论应被视为[方向性/需谨慎]。
```

**填充指引**：
- 如果偏倚方向可以判断（正/负）：在第一个 `[...]` 中说明方向判断的依据，在第二个 `[...]` 中说明该方向偏差对结论的具体影响（夸大效应？低估风险？）
- 如果偏倚方向无法判断（不确定）：在第二个 `[...]` 中写明"现有文献不足以判断偏倚方向，结论应视为方向性而非定量判断"
- 模板中两个 `[...]` 各至少填充一句，总计至少 2 句

对于非争议性话题，可使用上文"可接受的替代形式"的简化说明。

## Hard fail conditions

Fail the report if:

- **Preprints treated as peer-reviewed**: preprints must be explicitly labeled as not peer-reviewed
- **Cherry-picking**: using single papers to support pre-determined conclusions
- **Correlation ≠ causation**: inferring causation from observational studies without proper caveats
- **Ignoring publication bias**: presenting only positive results without noting the "file drawer problem" or without completing the publication bias discussion requirements (see「发表偏倚讨论」section)
- **Stale sources**: using outdated research when newer evidence exists (field-dependent: 2-5 years for fast-moving fields, 10+ years for established methods)
- **Missing venue information**: citing papers without noting where they were published
- **Statistical claims without context**: reporting p-values without effect sizes, or claiming significance without noting sample size limitations

## Output structure

An academic literature review report should visibly show:

### For field progress analysis
- Scope of the review (time period, sub-fields covered)
- Key research themes and trends
- Major breakthroughs and milestones
- Current state of the art
- Open questions and future directions
- Evidence quality assessment

### For paper comparison
- Comparison dimensions (methodology, dataset, results, limitations)
- Paper-by-paper analysis
- Cross-cutting themes
- Methodological strengths and weaknesses
- Recommendations for practitioners

### For technology origin tracing
- Original seminal work(s)
- Key evolutionary steps
- Branching points and divergent approaches
- Current dominant paradigm
- Competing approaches and their evidence bases

## Related references

- `references/source-quality.md` — for general source ranking (academic sources use a separate two-dimensional hierarchy: study design quality + publication venue prestige)
- `references/source-traceability-and-claim-citation.md` — for inline citation requirements
- `references/counter-evidence.md` — for actively seeking contradicting evidence in academic literature
- `references/forward-looking-discipline.md` — when research trends or future directions are discussed
