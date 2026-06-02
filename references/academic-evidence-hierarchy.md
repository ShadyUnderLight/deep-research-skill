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

1. **Publication type**: published / preprint / conference / working paper / unpublished
2. **Peer-review status**: peer-reviewed / not peer-reviewed / unknown
3. **Publication venue**: journal name, conference name, or repository
4. **Publication date**: year (and month if available for fast-moving fields)
5. **DOI or URL**: when available

Example labeling:
```
- [Published, Peer-reviewed] Vaswani et al. (2017). "Attention Is All You Need." NeurIPS 2017. DOI: xxx
- [Preprint, Not peer-reviewed] Smith et al. (2024). "Scaling Laws for LLMs." arXiv:2401.xxxxx
```

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
- **纳入/排除标准**：时间范围、语言、研究类型（RCT / 观察性研究 / 系统综述 / 综述 / 灰色文献）、发表日期范围、样本量阈值（如适用）
- **筛选流程数量**：初筛结果数 → 再审结果数 → 最终纳入数；如适用说明排除原因
- **检索日期**：明确记录检索执行日期

### 推荐但不强制（Recommended）

- **PRISMA 流程图**：适用于系统性综述报告，直观展示筛选流程各阶段的文献数量
- **文献管理工具**：如 Zotero, EndNote, Mendeley，便于追踪筛选过程和管理引用

### 筛选流程完整性

当报告使用"有限范围"限定词时，仍应在能力范围内完整记录检索策略；"有限范围"不应成为跳过检索策略文档化的借口。

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

对于无明显争议或不存在明显发表偏倚倾向的话题（如成熟的、共识度高的领域），可注明"本话题发表偏倚风险较低"，但仍建议简要记录判断理由。

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
