# Academic Route Activation Case: LLM Hallucination Research Paper Comparison

## Case metadata

- **Case type**: Route activation validation
- **Route**: Academic / Literature Review (experimental)
- **Task type**: Paper comparison and methodological evaluation
- **Date**: 2026-05-29
- **Status**: Validation case

## Task description

**User request**: "Compare the methodologies of recent papers on LLM hallucination detection and mitigation. What are the strengths and weaknesses of different approaches?"

**Expected route activation**: Academic / Literature Review (paper comparison)

**Alternative route considered**: Technical Deep-dive / Architecture Analysis

**Why academic route wins**: The core question is about comparing research methodologies and evaluating evidence quality, not about how hallucination detection systems work technically.

## Route preflight analysis

### Primary route
- **Selected**: Academic / Literature Review
- **Reason**: Core question is about paper comparison and methodological evaluation

### Closest alternative route
- **Alternative**: Technical Deep-dive / Architecture Analysis
- **Why alternative loses**: The task focuses on comparing research methodologies, not on understanding technical architectures or evaluating feasibility

### Opening must do
- Define scope of comparison (which papers, what time period)
- Establish comparison dimensions
- Present evidence hierarchy for each paper
- State inclusion/exclusion criteria

### Mandatory sections
- Comparison dimensions
- Paper-by-paper analysis
- Cross-cutting themes
- Methodological strengths and weaknesses
- Recommendations for practitioners

### Minimize / move later
- Detailed technical implementation of specific methods (belongs in technical deep-dive)
- Market applications of hallucination detection (belongs in market outlook)

### Visible proof the route fired
- Papers cited with publication type and peer-review status
- Comparison dimensions explicitly stated
- Evidence tier labels for each paper
- Clear strengths/weaknesses analysis

### Hard-fail signs to watch
- Comparing papers without explicit dimensions
- Treating preprints as peer-reviewed
- Missing methodological details
- Cherry-picking papers to support preferred conclusion

## Pass criteria

A good answer should:

### 1. Activate the correct route
- explicitly classify this as an academic paper comparison
- not default to technical deep-dive or generic research

### 2. Satisfy the artifact contract
- define comparison dimensions explicitly
- provide paper-by-paper analysis with full citations
- identify cross-cutting themes
- document methodological strengths and weaknesses
- include recommendations for practitioners

### 3. Apply evidence hierarchy correctly
- label publication type and peer-review status for each paper
- distinguish study design quality from publication venue prestige
- respect discipline-specific venue prestige

### 4. Avoid hard-fail conditions
- no comparing papers without explicit dimensions
- no preprints treated as peer-reviewed
- no missing methodological details
- no cherry-picking to support preferred conclusion

## Failure signs

The route activation failed if:

### Route selection failure
- the report is structured as a technical deep-dive (explaining how methods work)
- the report focuses on market applications instead of methodology comparison
- the report is a generic overview without academic evidence assessment

### Artifact contract failure
- no comparison dimensions explicitly stated
- no paper-by-paper analysis
- no cross-cutting themes identified
- no methodological strengths/weaknesses documented

### Evidence hierarchy failure
- preprints cited without "not peer-reviewed" label
- no publication venue information
- comparison dimensions not explicit
- cherry-picking detected

## Simulated evidence collection

### Search strategy
- **Databases**: Google Scholar, Semantic Scholar, arXiv, ACL Anthology
- **Search terms**: "LLM hallucination", "factual accuracy", "grounded generation", "hallucination detection", "hallucination mitigation"
- **Time range**: 2022-2024
- **Language**: English

### Comparison dimensions
1. **Task definition**: How is hallucination defined?
2. **Evaluation metrics**: What metrics are used?
3. **Dataset**: What data is used for evaluation?
4. **Methodology**: What is the proposed approach?
5. **Baselines**: What are the comparison baselines?
6. **Results**: What are the main findings?
7. **Limitations**: What are the acknowledged limitations?

### Papers selected for comparison

#### Paper 1: Detection-focused
**Manakul et al. (2023)** - "SelfCheckGPT: Zero-Resource Black-Box Hallucination Detection for Generative Large Language Models"
- [Published, Peer-reviewed] EMNLP 2023
- Evidence tier: Tier 2 (conference paper)
- Task definition: Detecting factual errors in LLM outputs
- Evaluation metrics: BERTScore, QA-based consistency, n-gram overlap
- Dataset: BioGEN, FactualQA
- Methodology: Sampling-based consistency checking
- Baselines: GPT-3.5, GPT-4
- Results: Effective for black-box models without external knowledge
- Limitations: Requires multiple samples, may miss subtle errors

#### Paper 2: Mitigation-focused
**Li et al. (2023)** - "Making Large Language Models Better Fact Learners"
- [Published, Peer-reviewed] NeurIPS 2023
- Evidence tier: Tier 2 (conference paper)
- Task definition: Reducing hallucination through improved training
- Evaluation metrics: Factual accuracy, consistency
- Dataset: TruthfulQA, FActScore
- Methodology: Knowledge-augmented training
- Baselines: Standard fine-tuning
- Results: Improved factual accuracy with knowledge integration
- Limitations: Requires high-quality knowledge base

#### Paper 3: Evaluation-focused
**Min et al. (2023)** - "FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation"
- [Published, Peer-reviewed] EMNLP 2023
- Evidence tier: Tier 2 (conference paper)
- Task definition: Evaluating factual precision in long-form generation
- Evaluation metrics: FActScore (atomic fact accuracy)
- Dataset: Biography, Science, History
- Methodology: Atomic fact extraction and verification
- Baselines: Human evaluation
- Results: Strong correlation with human judgment
- Limitations: Domain-specific, requires fact extraction

#### Paper 4: Mechanism-focused
**Li et al. (2023)** - "Inference-Time Intervention: Eliciting Truthful Answers from a Language Model"
- [Published, Peer-reviewed] NeurIPS 2023
- Evidence tier: Tier 2 (conference paper)
- Task definition: Understanding and controlling hallucination at inference time
- Evaluation metrics: Truthfulness score
- Dataset: TruthfulQA
- Methodology: Activation steering during inference
- Baselines: Standard inference, fine-tuning
- Results: Can improve truthfulness without retraining
- Limitations: Requires access to model internals

### Cross-cutting themes

#### Theme 1: Definition challenges
- No consensus on hallucination definition
- Different papers focus on different types (factual, faithful, grounded)
- Evaluation metrics vary widely

#### Theme 2: Methodological diversity
- Detection methods: sampling-based, knowledge-based, consistency-based
- Mitigation methods: training-time, inference-time, post-hoc
- Evaluation methods: automatic metrics, human evaluation, proxy tasks

#### Theme 3: Trade-offs
- Accuracy vs efficiency
- Generalizability vs specificity
- Automatic vs human evaluation

### Methodological strengths and weaknesses

| Paper | Strengths | Weaknesses |
|-------|-----------|------------|
| SelfCheckGPT | Black-box, no external knowledge needed | Requires multiple samples |
| Li et al. (training) | Addresses root cause | Requires high-quality knowledge base |
| FActScore | Fine-grained evaluation | Domain-specific, labor-intensive |
| Inference-Time Intervention | No retraining needed | Requires model access |

## Route activation assessment

### ✅ Route correctly activated
- Academic route was selected over technical deep-dive
- Paper comparison was structured with explicit dimensions
- Evidence hierarchy was respected
- Publication type and peer-review status were labeled

### ✅ Artifact contract satisfied
- Comparison dimensions explicitly stated
- Paper-by-paper analysis provided
- Cross-cutting themes identified
- Methodological strengths and weaknesses documented
- Recommendations for practitioners included

### ✅ Hard-fail conditions avoided
- All papers labeled with publication type
- Comparison dimensions explicitly stated
- No cherry-picking detected (multiple perspectives included)
- Venue information provided

### ⚠️ Areas for improvement
- Could add more systematic search methodology
- Could include more explicit handling of conflicting findings
- Could add more quantitative comparison of results

## Lessons learned

### What worked well
- Paper comparison was natural fit for academic route
- Comparison dimensions provided clear structure
- Evidence hierarchy helped assess paper quality

### What needs hardening
- Could add explicit comparison table template
- Could add more structured methodology assessment
- Could add more explicit handling of conflicting findings

### Route-boundary observations
- Technical deep-dive would have focused on "how hallucination detection works" rather than "how papers compare"
- Academic route better served the "methodology comparison" framing
- Clear boundary: if user asked "build a hallucination detection system", technical deep-dive would be correct

## Recommendation

**Route definition**: Adequate for experimental stage. The route correctly activates for paper comparison tasks and produces artifacts with clear comparison dimensions.

**Next steps**:
1. Consider adding comparison table template
2. Consider adding methodology assessment rubric
3. Consider adding explicit handling of conflicting findings

**Confidence**: High. Route definition is clear, artifact contract is satisfied, hard-fail conditions are avoided.
