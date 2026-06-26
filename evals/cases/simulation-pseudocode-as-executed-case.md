# Simulation Pseudocode-as-Executed Hard Fail Case

> **目的：** 固化 GPT 深度研究版与本地 deep-research-skill 版对比中发现的 "伪代码写为已执行 simulation" 和 "示例表 + p 值/CI 充实证" 两类失败模式。此 eval 确保 `validate_simulation_claims.py` 能检测到这些 pattern，且 `checklists/quantitative-role-audit.md` 将其设为 hard-fail sign。

---

## Case identity

- **Case name:** simulation-pseudocode-as-executed-case
- **Date:** 2026-06-25
- **Source issues:** [#342](https://github.com/ShadyUnderLight/deep-research-skill/issues/342)
- **Related distillation:** `evals/comparative-distillation/world-cup-constrained-choice-gpt-vs-local-comparative-distillation.md`
- **Failure family:** numerical-discipline / simulation-transparency

---

## Test scenario 1: GPT-style "示例表 + p 值/CI" hard fail

### Description
GPT 深度研究版报告将一个"示例参考"表格接到 T 检验和 p 值结论上，但该表仅为示例数据，并未反映实际统计检验。

### Input
```text
# 比赛分析报告

以下为示例数据，说明各指标计算口径：

| 指标 | 小组第一 | 小组第二 |
|------|---------|---------|
| 平均射门 | 12.3 | 8.1 |
| 平均控球率 | 58% | 42% |

t 检验结果显示两组存在显著差异（p<0.001），说明小组第一优势具有统计学意义。
```

### Expected validator output
- `validate_simulation_claims.py` should detect:
  - `p<0.001` → triggers `[p_value]` warning because the text after the table is
    a statistical claim without disclosure that the numbers come from example data
    (the table says "示例数据" but the t-test claim doesn't carry its own
    illustrative marker)
  - Note: if the validator classifies this as "illustrative" because "示例" 
    is in the context window, that's acceptable — the validator is a helper,
    and the reviewer's judgment at final-audit time is the real gate
- The claim `t 检验结果显示` does NOT trigger because we don't currently scan
  for bare "t 检验" without a p-value component

### Expected human review action
Block — the p<0.001 conclusion should NOT appear without the table explicitly
marked as illustrative AND the p-value being accompanied by actual statistical
output (test statistic, degrees of freedom, sample size, effect size).

---

## Test scenario 2: "伪代码 + 声称模拟显示" hard fail

### Description
GPT 深度研究版给出 Poisson/Monte Carlo 伪代码，但正文却写成"模拟显示
晋级概率有统计学意义提高"，而实际上并未执行模拟。

### Input
```text
# 晋级概率分析

## 方法
我们采用 Poisson 模型对进球数建模，并使用 Monte Carlo 方法进行
10,000 次模拟。伪代码如下：

```python
import numpy as np
from scipy import stats

def simulate_match(team_a_elo, team_b_elo, n_sim=10000):
    results = []
    for i in range(n_sim):
        # ... (conceptual implementation)
        pass
    return results
```

## 结果
Monte Carlo 模拟显示，小组第一晋级 16 强约 85.2%，小组第二约 40.1%
（p<0.01）。数据显示其晋级概率有统计学意义提高（95% CI: [82%, 88%]）。
```

### Expected validator output
- `Monte Carlo` → triggers `[simulation]` warning (no execution disclosure)
- `p<0.01` → triggers `[p_value]` warning (no execution disclosure)
- `95% CI` → triggers `[confidence_interval]` warning (no execution disclosure)
- Total: 3 warnings expected (one for simulation, one for p_value, one for CI)
- Status classification: ALL should be "unknown" because:
  - The pseudocode is presented without "已执行" marker
  - The results are stated as findings without disclosure

### Expected human review action
Hard fail — the report:
1. Presents pseudocode but claims simulation results
2. Uses p<0.01 and 95% CI without seed/iterations/parameters/output artifact
3. Model output is written as if it were confirmed fact
4. Violates Claim Permission boundaries: pseudocode-only → may only write
   conceptual language, not "模拟显示"

---

## Test scenario 3: Properly disclosed (should pass)

### Description
A well-disciplined report that properly labels simulation status.

### Input
```text
# 晋级概率分析

## 方法（概念框架，未实际执行）
本报告提供 Monte Carlo 仿真框架供未来验证使用。具体方法：
采用 Elo 评分作为球队实力代理变量，通过 Poisson 回归对进球数建模。

> 注：本框架尚未实际执行。以下数字均为概念性演示，不应视为实际预测。

参数建议：随机种子=42, 迭代=10000, K-factor=32。
```

### Expected validator output
- `Monte Carlo` → classified as "conceptual" (✓ auto-classified, no warning)
- `Poisson` → classified as "conceptual" (✓ auto-classified, no warning)
- `Elo` → classified as "conceptual" (✓ auto-classified, no warning)
- `随机种子` → detected but classified (seed + context = conceptual, no warning)
- Exit code: 0 (all claims have status disclosure)

---

## Validation

Run against the validator:

```bash
python3 scripts/validate_simulation_claims.py <scenario_file>.md
```

- Scenario 1: expect exit code 2 (warnings)
- Scenario 2: expect exit code 2 (warnings) with >= 3 warnings
- Scenario 3: expect exit code 0 (pass)

---

## Registry

| Rule ID | Candidate rule | Action type | Source |
|---------|---------------|-------------|--------|
| R74 | Simulation/model-output status disclosure requirement (conceptual/executed/illustrative) | NEW_RULE | Issue [#342](https://github.com/ShadyUnderLight/deep-research-skill/issues/342) |
| R75 | P-value/CI/Elo/Poisson without execution evidence triggers validator warning | NEW_RULE | Issue [#342](https://github.com/ShadyUnderLight/deep-research-skill/issues/342) |
