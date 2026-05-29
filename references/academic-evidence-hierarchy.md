# Academic Evidence Hierarchy

Use this file when the research task involves academic literature, peer-reviewed research, preprints, conference papers, or patent literature.

This discipline applies when the core question is **understanding academic evidence, evaluating research quality, or surveying field progress** — not product selection, vendor comparison, or market sizing.

## When to use

Apply this discipline when the task involves:

- literature review or systematic review (文献综述 / 系统性综述)
- academic field progress analysis (学术领域进展分析)
- paper comparison or methodological evaluation (论文对比分析)
- technology origin tracing through academic publications (技术 origin 追溯)
- research quality assessment (研究质量评估)

## When NOT to use

Do not use this discipline when:

- the task is mainly about technology principles or architecture → use **Technical Deep-dive**
- the task is mainly about product or vendor selection → use **Provider / Vendor Selection**
- the task is mainly about market evolution → use **Market Outlook / Industry Evolution**
- the task is about company evaluation → use **Listed Company** or **Private Company**

## Evidence hierarchy

Academic evidence has a different hierarchy from business/technical evidence:

### Tier 1 — Strongest evidence

| Type | Description | Example sources |
|------|-------------|-----------------|
| Meta-analysis | Systematic pooling of multiple studies | Cochrane Reviews, meta-analyses in top journals |
| Systematic review | Structured literature search with inclusion/exclusion criteria | PRISMA-compliant reviews |
| Randomized controlled trial (RCT) | Gold standard for causal inference | Clinical trials, A/B tests with proper randomization |

### Tier 2 — Strong evidence

| Type | Description | Example sources |
|------|-------------|-----------------|
| Peer-reviewed journal article | Original research published after peer review | Nature, Science, PNAS, field-specific top journals |
| Cohort study | Observational study following a population over time | Longitudinal studies, prospective studies |
| Case-control study | Comparing groups with/without outcome | Retrospective studies |

### Tier 3 — Moderate evidence

| Type | Description | Example sources |
|------|-------------|-----------------|
| Conference paper | Peer-reviewed but typically shorter, less rigorous | NeurIPS, ICML, ACL, CVPR, field-specific conferences |
| Preprint | Not yet peer-reviewed, use with caution | arXiv, bioRxiv, medRxiv, SSRN |
| Working paper | Preliminary version, often in economics/social sciences | NBER, IZA working papers |
| Technical report | Institutional publication, variable quality | Company research labs, government agencies |

### Tier 4 — Weak evidence

| Type | Description | Example sources |
|------|-------------|-----------------|
| Case report | Single or small number of cases | Medical case reports |
| Editorial / Opinion | Expert opinion, not original research | Journal editorials, commentaries |
| Thesis / Dissertation | Student work, variable quality | Institutional repositories |
| News / Blog / Social media | Secondary reporting, not peer-reviewed | Science journalism, researcher blogs |

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

## Literature search methodology

When conducting literature search, document:

### Search strategy
- Databases searched: Google Scholar, Semantic Scholar, arXiv, PubMed, IEEE Xplore, etc.
- Search terms: exact queries used
- Date range: publication years covered
- Language: English only / multilingual

### Inclusion/exclusion criteria
- Publication type: journal / conference / preprint / all
- Study design: RCT / observational / all
- Sample size: minimum threshold if relevant
- Recency: how recent must the sources be?

### Search completeness
- Number of results screened
- Number included in final analysis
- PRISMA flow diagram if systematic review

## Hard fail conditions

Fail the report if:

- **Preprints treated as peer-reviewed**: preprints must be explicitly labeled as not peer-reviewed
- **Cherry-picking**: using single papers to support pre-determined conclusions
- **Correlation ≠ causation**: inferring causation from observational studies without proper caveats
- **Ignoring publication bias**: presenting only positive results without noting the "file drawer problem"
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

- `references/source-quality.md` — for general source ranking (academic sources add venue prestige and peer-review status as additional dimensions)
- `references/source-traceability-and-claim-citation.md` — for inline citation requirements
- `references/counter-evidence.md` — for actively seeking contradicting evidence in academic literature
- `references/forward-looking-discipline.md` — when research trends or future directions are discussed
