# Model Output and Simulation Discipline

Use this file when a report claims to have used simulation, statistical
modeling, or computational methods — Monte Carlo, Poisson, Elo, regression
with significance testing, p-values, confidence intervals, or similar —
and the claim materially affects a conclusion, ranking, recommendation,
or probability estimate.

## When to use

Apply this discipline when the report body contains any of these signals:

- `Monte Carlo` / `蒙特卡洛`
- `Poisson` / `泊松`
- `Elo` / 评分系统
- `p<` / `p ≪` / `p-value`
- `置信区间` / `confidence interval`
- `回归显著` / `统计显著` / `statistically significant`
- `t-test` / `ANOVA` / `卡方`
- `模拟` / `simulation` / `仿真`
- `随机种子` / `random seed`

## Core rules

### Rule 1: Status disclosure

Every model/simulation/statistical claim must be classified into exactly
one of three statuses. The status must be visible to the reader within
the same paragraph or section as the claim.

| Status | Definition | Allowed wording |
|--------|-----------|----------------|
| **Conceptual / planned** | Method is described but NOT executed. The report suggests it as an approach for future validation. | "可用该框架验证", "建议后续采用", "可为未来分析提供方法", "conceptual framework", "本报告未实际执行", "仅介绍方法" |
| **Executed** | The model/simulation was actually run with specific parameters and produces concrete output. | "已执行 Monte Carlo 模拟 10000 次", "ran with seed=42", "输出见附录表", "executed and recorded output" |
| **Illustrative** | Numbers come from example data, placeholder values, or simplified cases, NOT from real data or actual execution. | "以下为示例数据", "仅为说明指标口径", "illustrative only", "不应视为实际结果", "不代表真实数据" |

**Hard rule**: If none of these statuses is disclosed, the claim is
*unverifiable* and must be treated as a quality signal requiring
reviewer attention.

### Rule 2: Claim permission boundaries

What specific wording is allowed for each status:

| Status | Permitted claims | Forbidden claims |
|--------|-----------------|-----------------|
| Conceptual | "可用该框架验证", "建议后续采用该方法", "conceptual approach" | "模拟显示", "结果表明确实", "我们的分析发现", "数据表明" |
| Illustrative | "示例说明指标口径", "illustrative example", "仅为说明" | p<0.05, 95% CI, "显著差异", "统计检验表明", any conclusion-bearing statistical language |
| Executed | All statistical/quantitative conclusions | Nothing — but must disclose: seed, iterations, parameters, data source, output artifact location |

**Hard rule**: If the report writes pseudocode (actual code blocks or
algorithmic descriptions) but does not disclose execution, the report
may ONLY use "conceptual" language. Pseudocode without explicit execution
is conceptual by default.

### Rule 3: Labeling requirements

Model outputs must carry explicit epistemic role labels:

- `[模型输出]` / `model-output` — NEVER `[确认事实]` / `[CONF]` / `[Confirmed]`
- If labeled `model-output`, the report should also indicate whether it is: conceptual output, executed output, or illustrative output
- Model output cannot replace primary-source verification of current rules, schedules, match conditions, or game states

### Rule 4: Minimum evidence for executed claims

If a claim is classified as "executed", the report must provide at
minimum these evidentiary elements within the body or a nearby appendix:

1. **Data source**: what data was used, with date/coverage
2. **Parameters**: key parameter values (e.g., Elo K-factor, Poisson λ source, strategy adjustment coefficients)
3. **Random seed and iteration count**: for stochastic simulations
4. **Unit of analysis**: match, team, possession chain, event, schedule state, etc.
5. **Output artifact**: summary table, script reference, notebook location, or inline worked example
6. **Sensitivity variables**: at least 2-3 input variables whose plausible variation would change the conclusion

If any of these elements is missing, the report must either:
- downgrade the claim to "conceptual" (methods described, not executed), or
- explicitly state what is missing and adjust confidence accordingly

## Relationship to other discipline files

- `references/quantitative-role-labeling.md` — provides the general model-output role definition. This file adds simulation-specific disclosure requirements.
- `references/forward-looking-discipline.md` — handles forecast/source attribution for forward-looking claims. Simulation/model claims may overlap; both disciplines apply when present.
- `checklists/quantitative-role-audit.md` — hard-fail signs include model-output-as-fact detection. This file extends coverage to simulation-specific failure modes.
- `checklists/final-audit.md` §Precision and estimate sourcing — general estimate sourcing discipline complements this file.
- `scripts/validate_simulation_claims.py` — automated scanner for undisclosed simulation/statistical keywords. Produces conditional warnings; final judgment at audit time.

## Non-goals

This discipline does NOT:
- require all reports to include simulations
- require deep-research-skill to implement any Monte Carlo or Poisson model
- prohibit the use of p-values or confidence intervals (it only requires they have verifiable evidence)
- cover DCF models, ML training claims, or financial modeling (those have their own discipline files)

## Graceful degradation

Reports MAY retain simulation pseudocode or conceptual model descriptions
without execution. They MUST label them as `conceptual framework` or
`future validation` and MUST NOT derive statistical conclusions from them.

Reports that describe a method as "here is how you could verify this" are
acceptable. Reports that describe a method as "here is what we found" are
acceptable only when they actually ran it.
