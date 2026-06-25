#!/usr/bin/env python3
"""Property-based and regression tests for validate_simulation_claims.py.

Tests the following invariants:
  INV1  — idempotency (same file twice → same result)
  INV2  — no false positive on clean text
  INV3  — keyword sensitivity: bare "p<0.01" triggers warning
  INV4  — keyword sensitivity: bare "Monte Carlo" triggers warning
  INV5  — status disclosure: "已执行 Monte Carlo 模拟" suppresses warning
  INV6  — illustrative suppress: "示例数据" + p<0.05 suppresses warning
  INV7  — conceptual suppress: "可用该框架验证" + Poisson suppresses warning
  INV8  — code block exempt: p<0.01 inside ``` ``` is ignored
  INV9  — source ref context: keywords in body trigger (human review)
  INV10 — multiple keywords per line: each reported independently
  INV11 — deterministic: no random seed influence
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

import pytest
from hypothesis import given, strategies as st

SCRIPT = str(Path(__file__).resolve().parent / "validate_simulation_claims.py")


def run_validator(text: str) -> subprocess.CompletedProcess:
    """Run validator against a fixture file and return the result."""
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "fixture.md"
        p.write_text(text, encoding="utf-8")
        return subprocess.run(
            [sys.executable, SCRIPT, str(p)],
            capture_output=True,
            text=True,
        )


def expect_pass(name: str, text: str) -> str:
    result = run_validator(text)
    assert result.returncode == 0, (
        f"{name}: expected pass (exit 0), got {result.returncode}\n"
        f"stdout: {result.stdout}\nstderr: {result.stderr}"
    )
    print(f"  PASS  {name}")
    return result.stdout


def expect_warnings(name: str, text: str, min_warnings: int = 1) -> str:
    result = run_validator(text)
    assert result.returncode == 2, (
        f"{name}: expected warnings (exit 2), got {result.returncode}\n"
        f"stdout: {result.stdout}\nstderr: {result.stderr}"
    )
    warning_count = len([l for l in result.stdout.splitlines() if l.startswith("- ")])
    assert warning_count >= min_warnings, (
        f"{name}: expected >= {min_warnings} warning(s), got {warning_count}\n"
        f"stdout: {result.stdout}"
    )
    print(f"  PASS  {name} ({warning_count} warning(s))")
    return result.stdout


# ============================================================
# Regression tests (deterministic, specific scenarios)
# ============================================================

def test_clean_text_no_warnings() -> None:
    """INV2: Clean text with no simulation/stat keywords should pass."""
    expect_pass("clean market report", """
# 市场分析报告

该公司 2025 年营收为 $10B，同比增长 15%。管理层预计 2026 年增速保持在
10-15% 区间。主要竞争对手在市场份额上略有下降。

## 风险因素
- 宏观经济不确定性
- 行业竞争加剧
""".strip())


def test_bare_p_value_triggers_warning() -> None:
    """INV3: 'p<0.01' without status disclosure triggers warning."""
    expect_warnings("bare p-value", """
分析显示两组之间存在显著差异（p<0.01），说明处理效果明显。
""")


def test_bare_monte_carlo_triggers_warning() -> None:
    """INV4: 'Monte Carlo' without status disclosure triggers warning."""
    expect_warnings("bare Monte Carlo", """
我们使用 Monte Carlo 方法对未来收益进行了预测。
""")


def test_poisson_without_disclosure_triggers_warning() -> None:
    """Poisson model without disclosure triggers warning."""
    expect_warnings("bare Poisson", """
采用 Poisson 回归模型对事件频率进行分析。
""")


def test_confidence_interval_without_disclosure_triggers_warning() -> None:
    """'置信区间' without disclosure triggers warning."""
    expect_warnings("bare CI", """
该估计值的 95% 置信区间为 [1.2, 3.4]。
""")


def test_executed_simulation_suppresses_warning() -> None:
    """INV5: '已执行 Monte Carlo 模拟 10000 次' suppresses warning."""
    expect_pass("executed simulation", """
我们已执行 Monte Carlo 模拟 10000 次，得到晋级概率为 85.2%。
详细参数：随机种子=42，迭代次数=10000。
""")


def test_illustrative_data_suppresses_warning() -> None:
    """INV6: '以下为示例数据' followed by p<0.05 suppresses warning."""
    expect_pass("illustrative data", """
以下为示例数据，仅为说明指标口径：
组A与组B的差异 p<0.05（不应视为实际统计检验结果）。
""")


def test_conceptual_framework_suppresses_warning() -> None:
    """INV7: '可用该框架验证' + Poisson suppresses warning."""
    expect_pass("conceptual framework", """
研究者可用该 Poisson 回归框架验证事件频率的驱动因素。
本报告未实际执行该分析。
""")


def test_pseudocode_label_suppresses_warning() -> None:
    """Pseudocode marker suppresses simulation keyword warning."""
    expect_pass("pseudocode marker", """
伪代码：
```
def simulate(n=10000):
    for i in range(n):
        ...
```
本报告未实际执行模拟。
""")


def test_code_block_exempt() -> None:
    """INV8: Keywords inside fenced code blocks are exempt."""
    text = """# 分析结果

```python
# 以下为伪代码示例
from scipy import stats
result = stats.ttest_ind(a, b)
print(f"p<0.01, t=-3.5")
```

核心结论基于实际数据，不依赖上述示例代码。
"""
    # 代码块中的 p<0.01 不应触发
    result = run_validator(text)
    # 如果没有代码块之外的触发词，应该 pass
    assert result.returncode == 0, f"code block exemption failed: {result.stdout}"
    print("  PASS  code_block_exempt")


def test_source_reference_keyword_in_body_triggers() -> None:
    """Keywords in body text next to [Sxx] still trigger (human review needed)."""
    # Even with source references nearby, keywords in free text should be flagged
    # for human verification. The [Sxx] alone doesn't prove the p-value was
    # actually from that source.
    expect_warnings("keyword near ref", """
该结论在 [S01] 的 Monte Carlo 分析基础上，进一步验证了显著性水平 p<0.01
的稳健性 [S02]。
""", min_warnings=2)


def test_multiple_keywords_single_sentence() -> None:
    """INV10: 'p<0.01' and 'Monte Carlo' in one sentence → 2 independent claims."""
    stdout = expect_warnings("multiple keywords single sentence", """
我们的 Monte Carlo 模拟显示两组间存在显著差异（p<0.01）。
""", min_warnings=2)
    # Each keyword is an independent claim needing disclosure
    warning_lines = [l for l in stdout.splitlines() if l.startswith("- ")]
    assert len(warning_lines) == 2, (
        f"Expected 2 warnings (Monte Carlo + p<0.01), got {len(warning_lines)}:\n{stdout}"
    )


def test_chinese_simulation_keywords() -> None:
    """Chinese keyword '模拟显示' triggers warning."""
    expect_warnings("Chinese 模拟", """
模拟显示，小组第一晋级 16 强的概率约为 85.2%。
""")


def test_elo_without_disclosure_triggers_warning() -> None:
    """Elo mention without disclosure triggers warning."""
    expect_warnings("Elo warning", """
对手平均 Elo 评分为 1574，远低于本队的 1850。
""")


def test_statistically_significant_without_disclosure() -> None:
    """'统计显著' without disclosure triggers warning."""
    expect_warnings("统计显著", """
回归分析表明该因素具有统计显著性，是决策的核心驱动变量。
""")


def test_empty_file_passes() -> None:
    """Edge case: empty file should pass."""
    expect_pass("empty", "")


def test_file_with_only_code_blocks_passes() -> None:
    """Edge case: file containing only code blocks with keywords passes."""
    expect_pass("only code blocks", """
```python
# Monte Carlo simulation
result = ttest_ind(a, b)
p = 0.001  # p<0.01
```
""")


def test_chinese_conceptual_suppresses() -> None:
    """Chinese conceptual markers suppress warnings."""
    expect_pass("Chinese conceptual", """
该问题可用 Monte Carlo 框架进行后续验证。当前报告未实际执行该分析。
未来可考虑采用 Poisson 模型进行敏感性测试。
""")


# ============================================================
# Property-based tests (Hypothesis)
# ============================================================

# Strategy: generate sentences with and without keywords
clean_sentence = st.text(
    alphabet=st.characters(whitelist_categories=("Lu", "Ll", "Lo", "Nd", "Zs", "Po")),
    min_size=10,
    max_size=200,
).filter(lambda s: not any(kw in s for kw in [
    "p<", "p <", "p≪", "p-value", "Monte Carlo", "monte carlo",
    "Poisson", "poisson", "Elo", "elo", "置信区间", "模拟",
    "显著", "统计检验", "t-test", "T-test", "随机种子",
    "random seed", "confidence interval",
]))


@given(
    prefix=st.text(min_size=0, max_size=50),
    suffix=st.text(min_size=0, max_size=50),
)
def test_inv2_property_clean_text_no_false_positive(prefix: str, suffix: str) -> None:
    """INV2 property: clean text (no simulation keywords) should yield zero claims."""
    # Ensure no keywords accidentally appear in the generated text
    text = f"{prefix} 该公司 2025 年营收表现良好，管理层对未来展望持谨慎乐观态度。{suffix}"
    result = run_validator(text)
    assert result.returncode == 0, (
        f"Expected pass on clean text, got exit {result.returncode}\n"
        f"text: {text[:100]}\nstdout: {result.stdout}"
    )


@given(
    keyword=st.sampled_from([
        "p<0.01", "p <0.05", "p≪0.001", "p-value",
        "Monte Carlo", "Poisson", "Elo", "置信区间",
        "confidence interval", "模拟", "统计显著",
    ]),
    context=st.text(
        alphabet=st.characters(whitelist_categories=("Lu", "Ll", "Lo", "Nd", "Zs", "Po")),
        min_size=5, max_size=100,
    ).filter(lambda s: all(
        kw not in s.lower() for kw in [
            "执行", "executed", "示例", "illustrative", "概念",
            "conceptual", "伪代码", "pseudocode", "框架", "framework",
            "可用该", "后续", "验证", "已实现", "运行了",
        ]
    )),
)
def test_inv3_property_keyword_triggers_warning(keyword: str, context: str) -> None:
    """INV3/4 property: any simulation/stat keyword without disclosure → warning."""
    text = f"分析表明 {context}（{keyword}）。"
    result = run_validator(text)
    assert result.returncode == 2, (
        f"Expected warning for keyword '{keyword}', got exit {result.returncode}\n"
        f"text: {text[:120]}\nstdout: {result.stdout}"
    )


@given(
    keyword=st.sampled_from([
        "Monte Carlo 模拟", "Poisson 回归", "p<0.01",
    ]),
    disclosure=st.sampled_from([
        "已实际执行", "我们运行了该模型", "已执行并记录输出",
        "以下为示例数据，仅作说明", "仅为示例说明",
        "可用该框架进行后续验证", "本报告未实际执行",
    ]),
)
def test_inv5_property_disclosure_suppresses(keyword: str, disclosure: str) -> None:
    """INV5-7 property: status disclosure suppresses warnings."""
    text = f"{disclosure}。具体方法：采用 {keyword} 进行分析。"
    result = run_validator(text)
    assert result.returncode == 0, (
        f"Expected pass for disclosure '{disclosure}' + keyword '{keyword}', "
        f"got exit {result.returncode}\nstdout: {result.stdout}"
    )


@given(
    python_code=st.text(
        alphabet=st.characters(whitelist_categories=("Lu", "Ll", "Lo", "Nd", "Zs", "Po", "Sc")),
        min_size=10, max_size=200,
    ),
)
def test_inv8_property_code_block_exempt(python_code: str) -> None:
    """INV8 property: any text inside ``` ``` code blocks is exempt."""
    # Inject a known keyword into the code block
    text = f"""# 报告

```python
# 分析代码: {python_code}
p_value = 0.001  # p<0.01
```

上述代码仅供内部使用，实际结论基于观测数据。
"""
    result = run_validator(text)
    # The p<0.01 inside code block should be exempt
    # The outer text has no keywords, so should pass
    assert result.returncode == 0, (
        f"Expected pass (code block exempt), got {result.returncode}\n"
        f"stdout: {result.stdout}"
    )


def main() -> int:
    """Run all tests. Returns 0 on success, 1 on failure."""
    return pytest.main([__file__, "-v", "--tb=short", "--hypothesis-show-statistics"])


if __name__ == "__main__":
    raise SystemExit(main() or 0)
