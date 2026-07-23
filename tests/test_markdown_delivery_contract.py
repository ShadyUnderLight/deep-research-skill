from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_markdown_delivery import validate_markdown_delivery  # noqa: E402


VALID_REPORT = """---
title: \"Example\"
date: 2026-07-23
type: decision-report
route: shared-workflow
status: final
---

# Example decision report

> **核心判断**：当前最稳妥的选择是先做小范围验证。
>
> **置信度**：中；关键限制是长期数据不足。

## 执行摘要（Executive summary）

- [确认] 方案 A 已满足当前硬约束。[S01]
- [推断] 方案 A 的实施风险低于方案 B。[S02]
- [未知] 长期维护成本尚未被公开资料充分验证。
- 下一步：先在低风险范围内验证，再决定是否扩大投入。

## 最关键变量（What matters most）

> **本节判断**：可逆性比短期功能差异更重要。
>
> **主要驱动**：迁移成本和验证周期。
>
> **主要风险 / 关键未知**：真实负载下的性能数据。

## 关键发现（Key findings）

方案 A 目前更符合约束。[推断] [S02]

## 详细分析（Detailed analysis）

### 实施约束

先验证低风险场景，再决定是否扩大范围。

## 风险与反证（Risks and counter-evidence）

- 反证：如果维护团队规模不足，结论会变弱。[S03]

## 不确定性与缺失证据（Uncertainty and missing evidence）

- 尚未确认跨区域部署成本。

## 结论（Bottom line）

先做受控试点，再进行全面承诺。

## 建议的下一步（Recommended next steps）

1. 建立试点验收指标。

## 附录：路由与审计状态（Route and audit status）

| Audit | Status | 证据 |
|---|---|---|
| final-audit | ✅ Passed | §1-§8 |

## 附录：来源登记（Source Register）

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|---|---|---|---|---|---|---|
| S01 | Official note | primary | 2026-07-23 | [链接](https://example.com/1) | high | §2 |
| S02 | Independent analysis | secondary | 2026-07-23 | [链接](https://example.com/2) | medium | §3 |
| S03 | Counter-evidence | secondary | 2026-07-23 | [链接](https://example.com/3) | medium | §6 |
"""


def test_valid_reader_facing_report_passes() -> None:
    result = validate_markdown_delivery(VALID_REPORT)
    assert result.errors == []


def test_heading_skip_is_blocking() -> None:
    result = validate_markdown_delivery(
        VALID_REPORT.replace("### 实施约束", "#### 实施约束")
    )
    assert any("heading level skips" in error for error in result.errors)


def test_missing_opening_judgment_is_blocking() -> None:
    without_judgment = VALID_REPORT.replace(
        "> **核心判断**：当前最稳妥的选择是先做小范围验证。\n>\n"
        "> **置信度**：中；关键限制是长期数据不足。\n",
        "",
    )
    result = validate_markdown_delivery(without_judgment)
    assert any("judgment/thesis marker" in error for error in result.errors)


def test_placeholder_residue_is_blocking() -> None:
    result = validate_markdown_delivery(
        VALID_REPORT.replace("受控试点", "受控试点 [TBD]", 1)
    )
    assert any("placeholder residue" in error for error in result.errors)


def test_body_table_width_is_advisory() -> None:
    wide = (
        "| A | B | C | D | E | F | G |\n"
        "|---|---|---|---|---|---|---|\n"
        "| 1 | 2 | 3 | 4 | 5 | 6 | 7 |"
    )
    result = validate_markdown_delivery(
        VALID_REPORT.replace("方案 A 目前更符合约束。[推断] [S02]", wide)
    )
    assert result.errors == []
    assert any("columns" in warning for warning in result.warnings)


def test_skill_wires_markdown_contract() -> None:
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    assert "markdown-delivery-contract.md" in skill
    assert "validate_markdown_delivery.py" in skill
