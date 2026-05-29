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

- `references/source-quality.md` — for general source ranking (academic sources use a separate two-dimensional hierarchy: study design quality + publication venue prestige)
- `references/source-traceability-and-claim-citation.md` — for inline citation requirements
- `references/counter-evidence.md` — for actively seeking contradicting evidence in academic literature
- `references/forward-looking-discipline.md` — when research trends or future directions are discussed
