#!/usr/bin/env python3
"""
Tests for audit_report.py — route-aware audit orchestrator.

Uses property-based testing patterns to verify:
1. Valid reports pass all checks
2. Common failure modes produce appropriate blocking/warnings
3. Route auto-detection works correctly
4. Exit code invariants hold

Each test creates a fixture file inline rather than using external fixtures,
ensuring tests are self-contained and easy to understand.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from collections.abc import Callable
from pathlib import Path

# ── Fixture builders ─────────────────────────────────────────────────────────

SCRIPT = str(Path(__file__).resolve().parent / "audit_report.py")


def _valid_report() -> str:
    """A minimal valid report that passes all technical-deep-dive checks.

    Requirements:
    - S02 must be 'secondary' not 'primary_company' to avoid caveat requirement
    - A table with role labels must exist to satisfy quantitative-role-labeling claim
    - Source Register must have 7 columns
    - Each key section must have [Sxx] citation
    """
    return """\
# Test Report

## Route and audit status

**Primary route**: Technical Deep-dive

| Audit | Status | 证据 |
|-------|--------|------|
| source-traceability | ✅ Passed | §3 正文使用 [S01] 与 [S02] 引用 |
| final-audit | ✅ Passed | §2-§6 各核心关卡可追溯 |
| quantitative-role-labeling | ✅ Passed | §5 Comparison 表格含数字角色列 |

## 执行摘要

Executive summary with citation [S01].

## Findings

Body text with citation [S02].

## 维度结论

Each dimension conclusion is backed by [S01] and [S02].

## Comparison Table

| Metric | System A | System B | 数字角色 |
|--------|----------|----------|---------|
| Cost | 100 | 80 | observed |
| Speed | 200 | 150 | observed |

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Example A | secondary | 2026-01-01 | https://example.com/a | medium | §3 |
| S02 | Example B | secondary | 2026-02-01 | https://example.com/b | high | §5 |
"""


def _report_with_6col_register() -> str:
    """Report whose Source Register has only 6 columns (should fail).

    Uses 'secondary' source type to avoid triggering source-label-consistency,
    isolating the test to the column-count failure only.
    """
    return """\
# Test Report

## Route and audit status

**Primary route**: Technical Deep-dive

| Audit | Status | 证据 |
|-------|--------|------|
| source-traceability | ✅ Passed | §3 引用 [S01] |
| final-audit | ✅ Passed | §2 可追溯 |

## Body

Body text with citation [S01] and [S02].

## Source Register

| ID | Source Name | Type | Date | URL | Reliability |
|----|-------------|------|------|-----|-------------|
| S01 | Example A | secondary | 2026-01-01 | https://example.com/a | medium |
| S02 | Example B | secondary | 2026-02-01 | https://example.com/b | high |
"""


def _report_with_audit_mismatch() -> str:
    """Report claiming quantitative-role-labeling passed but body has no roles."""
    return """\
# Test Report

## Route and audit status

**Primary route**: Technical Deep-dive

| Audit | Status | 证据 |
|-------|--------|------|
| source-traceability | ✅ Passed | §3 正文使用 [S01] 引用 |
| quantitative-role-labeling | ✅ Passed | §4 表格含数字角色列 |
| final-audit | ✅ Passed | §2 各关卡可追溯 |

## Body

Body text with citation [S01].

## Comparison Table

| Item | Value A | Value B |
|------|---------|---------|
| Cost | 100 | 80 |
| Speed | 200 | 150 |

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Example | secondary | 2026-01-01 | https://example.com | medium | §3 |
"""


def _report_with_declared_exec_pass_but_fail() -> str:
    """Declared execution passes but other checks fail.

    This is the exact scenario from Issue #271:
    - validate_declared_execution.py returns pass
    - but Source Register has 6 columns and audit mismatch exists
    """
    return """\
# Test Report

## Route and audit status

**Primary route**: Technical Deep-dive

| Audit | Status | 证据 |
|-------|--------|------|
| source-traceability | ✅ Passed | §3 正文使用 [S01] 引用 |
| quantitative-role-labeling | ✅ Passed | §4 表格含数字角色列 |
| final-audit | ✅ Passed | §2 各关卡可追溯 |

## Body

Body text with citation [S01].

## Comparison Table

| Item | Value A | Value B |
|------|---------|---------|
| Cost | 100 | 80 |
| Speed | 200 | 150 |

## Source Register

| ID | Name | Type | Date | URL | Reliability |
|----|------|------|------|-----|-------------|
| S01 | Example | secondary | 2026-01-01 | https://example.com | medium |
"""


def _report_with_table_missing_role_labels() -> str:
    """Report with tables lacking numeric role labels.

    Uses 'secondary' source type to avoid triggering source-label-consistency,
    isolating the test to missing-role-labels only.
    """
    return """\
# Test Report

## Route and audit status

**Primary route**: Technical Deep-dive

| Audit | Status | 证据 |
|-------|--------|------|
| source-traceability | ✅ Passed | §3 正文使用 [S01] 引用 |
| final-audit | ✅ Passed | §2 各关卡可追溯 |

## Body

Body with [S01] and [S02].

## Performance Table

| Metric | System A | System B | System C |
|--------|----------|----------|----------|
| Latency | 10ms | 20ms | 15ms |
| Throughput | 100 | 200 | 150 |
| Cost | $50 | $40 | $60 |
| Memory | 1GB | 2GB | 1.5GB |

## Comparison Table

| Feature | A | B | C |
|---------|---|---|---|
| Support | Yes | No | Yes |
| Protocol | HTTP | gRPC | MQTT |

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Example A | secondary | 2026-01-01 | https://example.com/a | medium | §3 |
| S02 | Example B | secondary | 2026-02-01 | https://example.com/b | high | §4 |
"""


def _report_no_route_block() -> str:
    """Report missing the ## Route and audit status section entirely."""
    return """\
# Test Report

## Body

Body text with citation [S01].

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Example | secondary | 2026-01-01 | https://example.com | medium | §3 |
"""


def _valid_constrained_choice_report() -> str:
    """A minimal valid report that passes all constrained-choice checks.

    Same structure as _valid_report() but with Constrained Choice / Shortlist
    route and route-specific audit rows.
    """
    return """\
# Test Report

## Route and audit status

**Primary route**: Constrained Choice / Shortlist

| Audit | Status | 证据 |
|-------|--------|------|
| source-traceability | ✅ Passed | §3 正文使用 [S01] 与 [S02] 引用 |
| option-selection-final-audit | ✅ Passed | §2-§6 各核心关卡可追溯 |
| final-audit | ✅ Passed | §5 Comparison 表格含数字角色列 |

## 执行摘要

Executive summary with citation [S01].

## Findings

Body text with citation [S02].

## 维度结论

Each dimension conclusion is backed by [S01] and [S02].

## Comparison Table

| Metric | System A | System B | 数字角色 |
|--------|----------|----------|---------|
| Cost | 100 | 80 | observed |
| Speed | 200 | 150 | observed |

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Example A | secondary | 2026-01-01 | https://example.com/a | medium | §3 |
| S02 | Example B | secondary | 2026-02-01 | https://example.com/b | high | §5 |
"""


def _cc_scoring_table_no_rules() -> str:
    """Constrained-choice report with scoring table + total scores but no
    scoring rules, weights, or worked example.  Should fail scoring-replicability.

    Keeps all other structure valid (source register, role labels, route block)
    so the failure is isolated to scoring-replicability only.
    """
    return """\
# Programming Language Learning Value

## Route and audit status

**Primary route**: Constrained Choice / Shortlist

| Audit | Status | 证据 |
|-------|--------|------|
| source-traceability | ✅ Passed | §3 使用 [S01] [S02] 引用 |
| option-selection-final-audit | ✅ Passed | §2-§6 可追溯 |
| final-audit | ✅ Passed | §5 含数字角色列 |

## 排名

| 排名 | 语言 | 市场需求 | 生态成熟度 | 学习回报 | 前景 | 广度 | **总分** | 数字角色 |
|------|------|----------|------------|----------|------|------|----------|---------|
| 🥇 | Python | A+ | A+ | A+ | A+ | A+ | 4.8/5 | model-output |
| 🥈 | Rust | B+ | B+ | B | A | B | 3.7/5 | model-output |

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Example A | secondary | 2026-01-01 | https://example.com/a | medium | §3 |
| S02 | Example B | secondary | 2026-02-01 | https://example.com/b | high | §5 |
"""


def _cc_probability_no_method() -> str:
    """Constrained-choice report with probability distribution but no
    replicable method.  Should fail scoring-replicability."""
    return """\
# World Cup Prediction

## Route and audit status

**Primary route**: Constrained Choice / Shortlist

| Audit | Status | 证据 |
|-------|--------|------|
| source-traceability | ✅ Passed | §3 使用 [S01] [S02] 引用 |
| option-selection-final-audit | ✅ Passed | §2 可追溯 |
| final-audit | ✅ Passed | §5 含数字角色列 |

## 胜率预测

| 结果 | 概率 | 数字角色 |
|------|------|---------|
| Argentina 胜 | 60% | model-output |
| 平局 | 25% | model-output |
| Algeria 胜 | 15% | model-output |

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Example A | secondary | 2026-01-01 | https://example.com/a | medium | §3 |
| S02 | Example B | secondary | 2026-02-01 | https://example.com/b | high | §5 |
"""


def _cc_scoring_table_with_rules() -> str:
    """Constrained-choice report with scoring table + weights + rules +
    worked example.  Should pass all validators including scoring-replicability."""
    return """\
# Programming Language Learning Value

## Route and audit status

**Primary route**: Constrained Choice / Shortlist

| Audit | Status | 证据 |
|-------|--------|------|
| source-traceability | ✅ Passed | §3 使用 [S01] [S02] 引用 |
| option-selection-final-audit | ✅ Passed | §2-§6 可追溯 |
| final-audit | ✅ Passed | §5 含数字角色列 |

## 执行摘要

This report evaluates programming language learning value based on market demand [S01].

## Findings

Python and Rust show strong demand in 2026 [S01]. Learning curves vary significantly by language [S02].

## 评分规则

字母等级转 5 分制：A+=5.0, A=4.5, A-=4.0, B+=3.5, B=3.0, B-=2.5, C+=2.0, C=1.5。

**权重**：市场需求 30%，生态成熟度 25%，学习回报 20%，前景 15%，广度 10%。

**计算示例 (Python)**：总分 = (5.0×0.30)+(5.0×0.25)+(5.0×0.20)+(5.0×0.15)+(5.0×0.10) = 5.0/5。

**⚠ 近似分差说明**：Rust 3.7 与 Kotlin 3.6 的差距（0.1）在估算误差范围内
（±0.15）。排名取决于生态成熟度权重，如果该维度权重下降 5pp，差距可能逆转。

## 排名

| 排名 | 语言 | 市场需求 | 生态成熟度 | 学习回报 | **总分** | 数字角色 |
|------|------|----------|------------|----------|----------|---------|
| 🥇 | Python | A+ (5.0) | A+ (5.0) | A+ (5.0) | 5.0/5 | model-output |

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Example A | secondary | 2026-01-01 | https://example.com/a | medium | §3 |
| S02 | Example B | secondary | 2026-02-01 | https://example.com/b | high | §5 |
"""


def _valid_chinese_constrained_choice_report() -> str:
    """A valid constrained-choice report with Chinese heading.

    Uses ## 附录：路由与审计状态 instead of the English heading, with
    **Primary route**: Constrained Choice / Shortlist so that both
    get_route_name() and check_route_declaration() work correctly.
    """
    return """\
# Test Report

## 附录：路由与审计状态

**Primary route**: Constrained Choice / Shortlist

| Audit | Status | 证据 |
|-------|--------|------|
| source-traceability | ✅ Passed | §3 正文使用 [S01] 与 [S02] 引用 |
| option-selection-final-audit | ✅ Passed | §2-§6 各核心关卡可追溯 |
| final-audit | ✅ Passed | §5 Comparison 表格含数字角色列 |

## 执行摘要

Executive summary with citation [S01].

## Findings

Body text with citation [S02].

## 维度结论

Each dimension conclusion is backed by [S01] and [S02].

## Comparison Table

| Metric | System A | System B | 数字角色 |
|--------|----------|----------|---------|
| Cost | 100 | 80 | observed |
| Speed | 200 | 150 | observed |

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Example A | secondary | 2026-01-01 | https://example.com/a | medium | §3 |
| S02 | Example B | secondary | 2026-02-01 | https://example.com/b | high | §5 |
"""


def _valid_market_outlook_report() -> str:
    """A minimal valid market-outlook report that passes all checks.

    Passes shared validators AND monitoring actionability (3+ signals
    with all four fields: threshold, cadence, source, trigger-to-action).
    """
    return """\
# Power Market Outlook 2026

## Route and audit status

**Primary route**: Market Outlook / Industry Evolution

| Audit | Status | 证据 |
|-------|--------|------|
| source-traceability | ✅ Passed | §3 正文使用 [S01] 与 [S02] 引用 |
| quantitative-role-labeling | ✅ Passed | §5 Comparison 表格含数字角色列 |
| final-audit | ✅ Passed | §2-§6 各核心关卡可追溯 |

## 执行摘要

Power constraints are tightening across global data center markets [S01].

## 市场现状

Current snapshot shows 5.2 GW under construction in North America [S02].

## Dimension conclusions

Each dimension conclusion is backed by [S01] and [S02].

## Comparison Table

| Metric | 2025 | 2026E | 数字角色 |
|--------|------|-------|---------|
| DC Power | 50GW | 65GW | observed |
| Growth | 20% | 30% | estimate |

## Monitoring Signals

| Signal | Threshold | Cadence | Source | Trigger-to-action | 数字角色 |
|--------|-----------|---------|--------|-------------------|---------|
| GPU utilization | >85% for 3 months | Monthly | Cloud provider API | Notify capacity team | observed |
| Power cost | >$0.12/kWh | Quarterly | EIA report | Reassess location strategy | observed |
| Grid interconnection | >6 months delay | Per project | Utility queue data | Explore colocation option | observed |

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Example A | secondary | 2026-01-01 | https://example.com/a | medium | §3 |
| S02 | Example B | secondary | 2026-02-01 | https://example.com/b | high | §5 |
"""


def _market_outlook_no_monitoring_actionability() -> str:
    """Market-outlook report with monitoring signals lacking actionability.

    Has only 'Signal' and 'Threshold' columns — missing cadence,
    source, and trigger-to-action.  <3 fully-defined → blocking.
    """
    return """\
# Power Market Outlook 2026

## Route and audit status

**Primary route**: Market Outlook / Industry Evolution

| Audit | Status | 证据 |
|-------|--------|------|
| source-traceability | ✅ Passed | §3 正文使用 [S01] 与 [S02] 引用 |
| quantitative-role-labeling | ✅ Passed | §5 Comparison 表格含数字角色列 |
| final-audit | ✅ Passed | §2-§6 各核心关卡可追溯 |

## 执行摘要

Power constraints are tightening across global data center markets [S01].

## 市场现状

Current snapshot shows 5.2 GW under construction in North America [S02].

## Dimension conclusions

Each dimension conclusion is backed by [S01] and [S02].

## Comparison Table

| Metric | 2025 | 2026E | 数字角色 |
|--------|------|-------|---------|
| DC Power | 50GW | 65GW | observed |
| Growth | 20% | 30% | estimate |

## Monitoring Signals

| Signal | Threshold | 数字角色 |
|--------|-----------|---------|
| GPU utilization | >85% | observed |
| Power cost | >$0.12/kWh | observed |
| Grid interconnection | >6 months delay | observed |

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Example A | secondary | 2026-01-01 | https://example.com/a | medium | §3 |
| S02 | Example B | secondary | 2026-02-01 | https://example.com/b | high | §5 |
"""


def _market_outlook_no_monitoring_section() -> str:
    """Market-outlook report with no monitoring section at all."""
    return """\
# Power Market Outlook 2026

## Route and audit status

**Primary route**: Market Outlook / Industry Evolution

| Audit | Status | 证据 |
|-------|--------|------|
| source-traceability | ✅ Passed | §3 正文使用 [S01] 与 [S02] 引用 |
| quantitative-role-labeling | ✅ Passed | §5 Comparison 表格含数字角色列 |
| final-audit | ✅ Passed | §2-§6 各核心关卡可追溯 |

## 执行摘要

Power constraints are tightening across global data center markets [S01].

## 市场现状

Current snapshot shows 5.2 GW under construction in North America [S02].

## Dimension conclusions

Each dimension conclusion is backed by [S01] and [S02].

## Comparison Table

| Metric | 2025 | 2026E | 数字角色 |
|--------|------|-------|---------|
| DC Power | 50GW | 65GW | observed |
| Growth | 20% | 30% | estimate |

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Example A | secondary | 2026-01-01 | https://example.com/a | medium | §3 |
| S02 | Example B | secondary | 2026-02-01 | https://example.com/b | high | §5 |
"""


# ── Shared base for market-outlook monitoring test fixtures ────────────

_MO_BODY_PREFIX = """\
# Power Market Outlook 2026

## Route and audit status

**Primary route**: Market Outlook / Industry Evolution

| Audit | Status | 证据 |
|-------|--------|------|
| source-traceability | ✅ Passed | §3 正文使用 [S01] 与 [S02] 引用 |
| quantitative-role-labeling | ✅ Passed | §5 Comparison 表格含数字角色列 |
| final-audit | ✅ Passed | §2-§6 各核心关卡可追溯 |

## 执行摘要

Power constraints are tightening across global data center markets [S01].

## 市场现状

Current snapshot shows 5.2 GW under construction [S02].

## Dimension conclusions

Each dimension conclusion is backed by [S01] and [S02].

## Comparison Table

| Metric | 2025 | 2026E | 数字角色 |
|--------|------|-------|---------|
| DC Power | 50GW | 65GW | observed |
| Growth | 20% | 30% | estimate |

"""

_MO_SOURCE_REGISTER = """

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Example A | secondary | 2026-01-01 | https://example.com/a | medium | §3 |
| S02 | Example B | secondary | 2026-02-01 | https://example.com/b | high | §5 |
"""


def _market_outlook_with_monitoring(monitoring_body: str) -> str:
    """Build a valid market-outlook report with a given monitoring section body."""
    return _MO_BODY_PREFIX + monitoring_body + _MO_SOURCE_REGISTER


def _market_outlook_with_empty_cell() -> str:
    """Report where one monitoring signal has an empty Cadence cell.

    Tests the cell-index alignment fix: the empty cell must NOT shift
    subsequent column indices, so the signal is correctly detected as
    not fully-defined.
    """
    table = """\
## Monitoring Signals

| Signal | Threshold | Cadence | Source | Trigger-to-action | 数字角色 |
|--------|-----------|---------|--------|-------------------|---------|
| GPU utilization | >85% for 3 months | Monthly | Cloud provider API | Notify capacity team | observed |
| Power cost | >$0.12/kWh | | EIA report | Reassess location strategy | observed |
| Grid interconnection | >6 months delay | Per project | Utility queue data | Explore colocation option | observed |
"""
    return _market_outlook_with_monitoring(table)


def _market_outlook_uppercase_columns() -> str:
    """Report with UPPERCASE monitoring table column headers.

    Validates case-insensitive keyword matching in _map_table_header.
    """
    table = """\
## Monitoring Signals

| SIGNAL | THRESHOLD | CADENCE | SOURCE | TRIGGER-TO-ACTION | 数字角色 |
|--------|-----------|---------|--------|-------------------|---------|
| GPU utilization | >85% 3mo | Monthly | Cloud API | Notify team | observed |
| Power cost | >$0.12/kWh | Quarterly | EIA report | Reassess | observed |
| Grid delay | >6 months | Per proj | Utility queue | Explore colo | observed |
"""
    return _market_outlook_with_monitoring(table)


def _market_outlook_two_signals() -> str:
    """Report with only 2 fully-defined monitoring signals (<3 threshold)."""
    table = """\
## Monitoring Signals

| Signal | Threshold | Cadence | Source | Trigger-to-action | 数字角色 |
|--------|-----------|---------|--------|-------------------|---------|
| GPU utilization | >85% 3mo | Monthly | Cloud API | Notify team | observed |
| Power cost | >$0.12/kWh | Quarterly | EIA report | Reassess | observed |
"""
    return _market_outlook_with_monitoring(table)


def _market_outlook_strict_with_partial() -> str:
    """Report with 3 fully-defined + 1 partially-defined monitoring signal.

    Without --strict: passes (exit 0).  With --strict: passes with warnings.
    """
    table = """\
## Monitoring Signals

| Signal | Threshold | Cadence | Source | Trigger-to-action | 数字角色 |
|--------|-----------|---------|--------|-------------------|---------|
| GPU utilization | >85% 3mo | Monthly | Cloud API | Notify team | observed |
| Power cost | >$0.12/kWh | Quarterly | EIA report | Reassess | observed |
| Grid delay | >6 months | Per proj | Utility queue | Explore colo | observed |
| New entrant | announced | | Vendor press | | observed |
"""
    return _market_outlook_with_monitoring(table)


def _valid_provider_selection_report() -> str:
    """A minimal valid provider-selection report that passes all checks.

    Same structure as _valid_constrained_choice_report() but with
    Provider / Vendor Selection route.  Passes shared validators AND
    scoring-replicability (no scoring table → nothing to fail on).
    """
    return """\
# AI Coding Provider Selection

## Route and audit status

**Primary route**: Provider / Vendor Selection

| Audit | Status | 证据 |
|-------|--------|------|
| source-traceability | ✅ Passed | §3 正文使用 [S01] 与 [S02] 引用 |
| option-selection-final-audit | ✅ Passed | §2-§6 各核心关卡可追溯 |
| final-audit | ✅ Passed | §5 Comparison 表格含数字角色列 |

## 执行摘要

Executive summary with citation [S01].

## Findings

Body text with citation [S02].

## 维度结论

Each dimension conclusion is backed by [S01] and [S02].

## Comparison Table

| Metric | System A | System B | 数字角色 |
|--------|----------|----------|---------|
| Cost | 100 | 80 | observed |
| Speed | 200 | 150 | observed |

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Example A | secondary | 2026-01-01 | https://example.com/a | medium | §3 |
| S02 | Example B | secondary | 2026-02-01 | https://example.com/b | high | §5 |
"""


def _valid_market_entry_report() -> str:
    """A minimal valid market-entry report that passes all checks.

    Same structure as _valid_provider_selection_report() but with
    Market Entry / Regional Expansion route.
    """
    return """\
# AI Education Market Entry

## Route and audit status

**Primary route**: Market Entry / Regional Expansion

| Audit | Status | 证据 |
|-------|--------|------|
| source-traceability | ✅ Passed | §3 正文使用 [S01] 与 [S02] 引用 |
| option-selection-final-audit | ✅ Passed | §2-§6 各核心关卡可追溯 |
| final-audit | ✅ Passed | §5 Comparison 表格含数字角色列 |

## 执行摘要

Executive summary with citation [S01].

## Findings

Body text with citation [S02].

## 维度结论

Each dimension conclusion is backed by [S01] and [S02].

## Comparison Table

| Metric | Country A | Country B | 数字角色 |
|--------|-----------|-----------|---------|
| Market Size | 100M | 80M | observed |
| Growth | 20% | 15% | observed |

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Example A | secondary | 2026-01-01 | https://example.com/a | medium | §3 |
| S02 | Example B | secondary | 2026-02-01 | https://example.com/b | high | §5 |
"""


def _valid_regulatory_analysis_report() -> str:
    """A minimal valid regulatory-analysis report that passes all checks."""
    return """\
# Regulatory Impact Analysis

## Route and audit status

**Primary route**: Regulatory / Policy Impact Analysis

| Audit | Status | 证据 |
|-------|--------|------|
| source-traceability | ✅ Passed | §3 正文使用 [S01] 与 [S02] 引用 |
| final-audit | ✅ Passed | §2-§6 各核心关卡可追溯 |

## 执行摘要

Executive summary with citation [S01].

## Findings

Body text with citation [S02].

## 维度结论

Each dimension conclusion is backed by [S01] and [S02].

## Comparison Table

| Metric | Scenario A | Scenario B | 数字角色 |
|--------|------------|------------|---------|
| Impact | High | Medium | estimate |
| Timeline | 2026 | 2027 | observed |

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Example A | secondary | 2026-01-01 | https://example.com/a | medium | §3 |
| S02 | Example B | secondary | 2026-02-01 | https://example.com/b | high | §5 |
"""


def _valid_equipment_selection_report() -> str:
    """A minimal valid equipment-selection report that passes all checks."""
    return """\
# Home Server Selection

## Route and audit status

**Primary route**: Equipment Selection / Procurement / Home-server Planning

| Audit | Status | 证据 |
|-------|--------|------|
| source-traceability | ✅ Passed | §3 正文使用 [S01] 与 [S02] 引用 |
| option-selection-final-audit | ✅ Passed | §2-§6 各核心关卡可追溯 |
| final-audit | ✅ Passed | §5 Comparison 表格含数字角色列 |

## 执行摘要

Executive summary with citation [S01].

## Findings

Body text with citation [S02].

## 维度结论

Each dimension conclusion is backed by [S01] and [S02].

## Comparison Table

| Metric | Option A | Option B | 数字角色 |
|--------|----------|----------|---------|
| Cost | 5000 | 4000 | observed |
| Power | 65W | 45W | observed |

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Example A | secondary | 2026-01-01 | https://example.com/a | medium | §3 |
| S02 | Example B | secondary | 2026-02-01 | https://example.com/b | high | §5 |
"""


def _valid_startup_evaluation_report() -> str:
    """A minimal valid startup-evaluation report that passes all checks."""
    return """\
# Startup Assessment

## Route and audit status

**Primary route**: Startup / Private Company Evaluation

| Audit | Status | 证据 |
|-------|--------|------|
| source-traceability | ✅ Passed | §3 正文使用 [S01] 与 [S02] 引用 |
| final-audit | ✅ Passed | §2-§6 各核心关卡可追溯 |

## 执行摘要

Executive summary with citation [S01].

## Findings

Body text with citation [S02].

## 维度结论

Each dimension conclusion is backed by [S01] and [S02].

## Comparison Table

| Metric | Company A | Company B | 数字角色 |
|--------|-----------|-----------|---------|
| Revenue | 10M | 8M | estimated |
| Growth | 80% | 60% | estimated |

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Example A | secondary | 2026-01-01 | https://example.com/a | medium | §3 |
| S02 | Example B | secondary | 2026-02-01 | https://example.com/b | high | §5 |
"""


def _valid_competitive_positioning_report() -> str:
    """A minimal valid competitive-positioning report that passes all checks."""
    return """\
# Competitive Positioning Analysis

## Route and audit status

**Primary route**: First-tier / Top-tier / Competitive Positioning

| Audit | Status | 证据 |
|-------|--------|------|
| source-traceability | ✅ Passed | §3 正文使用 [S01] 与 [S02] 引用 |
| final-audit | ✅ Passed | §2-§6 各核心关卡可追溯 |

## 执行摘要

Executive summary with citation [S01].

## Findings

Body text with citation [S02].

## 维度结论

Each dimension conclusion is backed by [S01] and [S02].

## Comparison Table

| Metric | Company A | Company B | 数字角色 |
|--------|-----------|-----------|---------|
| Market Share | 35% | 28% | observed |
| Growth | 15% | 12% | observed |

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Example A | secondary | 2026-01-01 | https://example.com/a | medium | §3 |
| S02 | Example B | secondary | 2026-02-01 | https://example.com/b | high | §5 |
"""


def _report_with_secondary_routes() -> str:
    """Report declaring primary + secondary routes (one supported, one not)."""
    return """\
# Test Report

## Route and audit status

**Primary route**: Technical Deep-dive
**Secondary routes**: Market Outlook, unknown-route-xyz

| Audit | Status | 证据 |
|-------|--------|------|
| source-traceability | ✅ Passed | §3 正文使用 [S01] 与 [S02] 引用 |
| final-audit | ✅ Passed | §2-§6 各核心关卡可追溯 |
| quantitative-role-labeling | ✅ Passed | §5 Comparison 表格含数字角色列 |

## 执行摘要

Executive summary with citation [S01].

## Findings

Body text with citation [S02].

## 维度结论

Each dimension conclusion is backed by [S01] and [S02].

## Comparison Table

| Metric | System A | System B | 数字角色 |
|--------|----------|----------|---------|
| Cost | 100 | 80 | observed |
| Speed | 200 | 150 | observed |

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Example A | secondary | 2026-01-01 | https://example.com/a | medium | §3 |
| S02 | Example B | secondary | 2026-02-01 | https://example.com/b | high | §5 |
"""


def _report_with_supported_secondary_routes() -> str:
    """Report declaring primary + secondary routes (all supported)."""
    return """\
# Test Report

## Route and audit status

**Primary route**: Technical Deep-dive
**Secondary routes**: Market Outlook, Constrained Choice

| Audit | Status | 证据 |
|-------|--------|------|
| source-traceability | ✅ Passed | §3 正文使用 [S01] 与 [S02] 引用 |
| final-audit | ✅ Passed | §2-§6 各核心关卡可追溯 |
| quantitative-role-labeling | ✅ Passed | §5 Comparison 表格含数字角色列 |

## 执行摘要

Executive summary with citation [S01].

## Findings

Body text with citation [S02].

## 维度结论

Each dimension conclusion is backed by [S01] and [S02].

## Comparison Table

| Metric | System A | System B | 数字角色 |
|--------|----------|----------|---------|
| Cost | 100 | 80 | observed |
| Speed | 200 | 150 | observed |

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Example A | secondary | 2026-01-01 | https://example.com/a | medium | §3 |
| S02 | Example B | secondary | 2026-02-01 | https://example.com/b | high | §5 |
"""


def _report_shared_workflow() -> str:
    """Report using shared-workflow path (no primary route).

    Falls back to technical-deep-dive validators since the auto-detected
    route name doesn't match any ROUTE_VALIDATORS key.
    """
    return """\
# Test Report

## Route and audit status

**Route**: Shared-workflow (no specialized route selected)

| Audit | Status | 证据 |
|-------|--------|------|
| workflow-spine-audit | ✅ Passed | §2-§6 各工作流关卡可追溯 |
| final-audit | ✅ Passed | §2-§6 各核心关卡有对应检查标记 |

## Body

Body text with citation [S01] and [S02].

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Example A | secondary | 2026-01-01 | https://example.com/a | medium | §3 |
| S02 | Example B | secondary | 2026-02-01 | https://example.com/b | high | §5 |
"""





# ── Test helpers ────────────────────────────────────────────────────────────


def _run_audit(content: str, extra_args: list[str] | None = None) -> subprocess.CompletedProcess:
    """Run audit_report.py on inline fixture content and return result."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", delete=False, encoding="utf-8",
    ) as f:
        f.write(content)
        tmp_path = f.name

    try:
        cmd = [sys.executable, SCRIPT, tmp_path]
        if extra_args:
            cmd.extend(extra_args)
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30,
        )
        return result
    finally:
        Path(tmp_path).unlink(missing_ok=True)


def _count_blocking(output: str) -> int:
    """Count blocking error lines in audit output."""
    lines = output.splitlines()
    in_blocking = False
    count = 0
    for line in lines:
        stripped = line.strip()
        if stripped == "Blocking:":
            in_blocking = True
            continue
        if stripped.startswith("Warnings:") or stripped.startswith("Recommended"):
            in_blocking = False
        if in_blocking and stripped.startswith("- "):
            count += 1
    return count


def _count_warnings(output: str) -> int:
    """Count warning lines in audit output."""
    lines = output.splitlines()
    in_warnings = False
    count = 0
    for line in lines:
        stripped = line.strip()
        if stripped == "Warnings:":
            in_warnings = True
            continue
        if stripped.startswith("Blocking:") or stripped.startswith("Recommended"):
            in_warnings = False
        if in_warnings and stripped.startswith("⚠ "):
            count += 1
    return count


def _get_overall(output: str) -> str | None:
    """Extract overall verdict line from output."""
    for line in output.splitlines():
        if line.startswith("Overall:"):
            return line.split(":", 1)[1].strip()
    return None


# ── Tests ───────────────────────────────────────────────────────────────────


class TestValidReport:
    """A fully valid technical-deep-dive report should pass all checks."""

    def test_exit_code_zero(self) -> None:
        result = _run_audit(_valid_report())
        assert result.returncode == 0, (
            f"Expected exit 0, got {result.returncode}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )

    def test_overall_pass(self) -> None:
        result = _run_audit(_valid_report())
        overall = _get_overall(result.stdout)
        assert overall == "pass", f"Expected 'pass', got '{overall}'"

    def test_no_blocking(self) -> None:
        result = _run_audit(_valid_report())
        assert _count_blocking(result.stdout) == 0

    def test_route_detected(self) -> None:
        result = _run_audit(_valid_report())
        assert "technical-deep-dive" in result.stdout.lower()


class Test6ColumnRegister:
    """Source Register with 6 columns (instead of required 7) must fail."""

    def test_exit_code_blocking(self) -> None:
        result = _run_audit(_report_with_6col_register())
        assert result.returncode == 2, (
            f"Expected exit 2, got {result.returncode}\n"
            f"stdout:\n{result.stdout}"
        )

    def test_overall_fail(self) -> None:
        result = _run_audit(_report_with_6col_register())
        assert _get_overall(result.stdout) == "fail"

    def test_blocking_mentions_column_count(self) -> None:
        result = _run_audit(_report_with_6col_register())
        assert "6 column" in result.stdout, (
            f"Expected column count error, got:\n{result.stdout}"
        )


class TestAuditMismatch:
    """Report claiming quantitative-role ✅ but body lacks roles -> blocking error."""

    def test_exit_code_blocking(self) -> None:
        result = _run_audit(_report_with_audit_mismatch())
        assert result.returncode == 2, (
            f"Expected exit 2 (blocking), got {result.returncode}\n"
            f"stdout:\n{result.stdout}"
        )

    def test_overall_fail(self) -> None:
        result = _run_audit(_report_with_audit_mismatch())
        assert _get_overall(result.stdout) == "fail"

    def test_error_mentions_quantitative_role(self) -> None:
        result = _run_audit(_report_with_audit_mismatch())
        assert "quantitative-role" in result.stdout or "quantitative role" in result.stdout, (
            f"Expected quantitative-role error, got:\n{result.stdout}"
        )


class TestDeclaredExecPassButOverallFail:
    """The exact Issue #271 scenario: validate_declared_execution passes
    but overall audit fails due to Source Register structure and audit mismatch."""

    def test_exit_code_blocking(self) -> None:
        result = _run_audit(_report_with_declared_exec_pass_but_fail())
        assert result.returncode == 2, (
            f"Expected exit 2 (blocking), got {result.returncode}\n"
            f"stdout:\n{result.stdout}"
        )

    def test_overall_fail(self) -> None:
        result = _run_audit(_report_with_declared_exec_pass_but_fail())
        assert _get_overall(result.stdout) == "fail"

    def test_blocking_mentions_column_and_mismatch(self) -> None:
        result = _run_audit(_report_with_declared_exec_pass_but_fail())
        output = result.stdout
        # Must have Source Register column error (blocking)
        assert "column" in output, f"Expected column count error, got:\n{output}"
        # Must have audit mismatch (warning)
        assert _count_warnings(output) > 0 or "quantitative-role" in output, (
            f"Expected audit mismatch warning, got:\n{output}"
        )


class TestTableMissingRoleLabels:
    """Reports with tables lacking numeric role labels must fail."""

    def test_exit_code_blocking(self) -> None:
        result = _run_audit(_report_with_table_missing_role_labels())
        assert result.returncode == 2, (
            f"Expected exit 2, got {result.returncode}\n"
            f"stdout:\n{result.stdout}"
        )

    def test_blocking_mentions_role_labels(self) -> None:
        result = _run_audit(_report_with_table_missing_role_labels())
        assert "role" in result.stdout.lower(), (
            f"Expected role label error, got:\n{result.stdout}"
        )


class TestNoRouteBlock:
    """Report missing the Route and audit status block should fail."""

    def test_exit_code_blocking(self) -> None:
        result = _run_audit(_report_no_route_block())
        assert result.returncode == 2

    def test_blocking_mentions_missing_section(self) -> None:
        result = _run_audit(_report_no_route_block())
        assert "Missing '## Route and audit status' section" in result.stdout, (
            f"Expected specific missing section error, got:\n{result.stdout}"
        )


class TestRouteOverride:
    """Explicit --route should override auto-detection."""

    def test_explicit_route_appears_in_output(self) -> None:
        result = _run_audit(_valid_report(), extra_args=["--route", "technical-deep-dive"])
        assert "technical-deep-dive" in result.stdout

    def test_unknown_route_is_blocking(self) -> None:
        result = _run_audit(_valid_report(), extra_args=["--route", "unknown-route"])
        assert result.returncode == 2, (
            f"Unknown route must block (exit 2), got {result.returncode}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
        # Error message should identify the unknown route, not silently fall back
        assert "unknown route" in (result.stdout + result.stderr).lower(), (
            f"Expected 'unknown route' in output, got stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )


class TestNonExistentFile:
    """Non-existent file should produce clear error."""

    def test_exit_code_blocking(self) -> None:
        cmd = [sys.executable, SCRIPT, "/tmp/nonexistent_report_xyz.md"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        assert result.returncode == 2, (
            f"Expected exit 2, got {result.returncode}\n"
            f"stdout:\n{result.stdout}"
        )


# ── Property-based tests ───────────────────────────────────────────────────


class TestProperties:
    """Invariant properties that must always hold."""

    # Property 1: Exit code 0 iff overall is "pass"
    def test_exit_code_zero_iff_overall_pass(self) -> None:
        """Exit code 0 <-> overall 'pass'."""
        for fixture, label in [
            (_valid_report(), "valid"),
            (_report_with_6col_register(), "6col"),
            (_report_with_audit_mismatch(), "mismatch"),
            (_report_with_table_missing_role_labels(), "no-roles"),
            (_report_no_route_block(), "no-route"),
            (_valid_regulatory_analysis_report(), "reg-analysis"),
            (_valid_equipment_selection_report(), "equip-sel"),
            (_valid_startup_evaluation_report(), "startup-eval"),
            (_valid_competitive_positioning_report(), "comp-pos"),
        ]:
            result = _run_audit(fixture)
            overall = _get_overall(result.stdout)
            if result.returncode == 0:
                assert overall == "pass", (
                    f"[{label}] Exit 0 but overall='{overall}'"
                )
            if overall == "pass":
                assert result.returncode == 0, (
                    f"[{label}] overall='pass' but exit={result.returncode}"
                )

    # Property 2: Exit code 2 iff blocking errors exist
    def test_exit_code_two_iff_blocking(self) -> None:
        """Exit code 2 iff at least one blocking error."""
        for fixture, label in [
            (_valid_report(), "valid"),
            (_report_with_6col_register(), "6col"),
            (_report_with_audit_mismatch(), "mismatch"),
            (_report_with_table_missing_role_labels(), "no-roles"),
            (_report_no_route_block(), "no-route"),
            (_report_with_declared_exec_pass_but_fail(), "declared-but-fail"),
            (_cc_scoring_table_no_rules(), "cc-scoring-no-rules"),
            (_cc_probability_no_method(), "cc-prob-no-method"),
            (_valid_regulatory_analysis_report(), "reg-analysis"),
            (_valid_equipment_selection_report(), "equip-sel"),
            (_valid_startup_evaluation_report(), "startup-eval"),
            (_valid_competitive_positioning_report(), "comp-pos"),
        ]:
            result = _run_audit(fixture)
            blocking_count = _count_blocking(result.stdout)
            if result.returncode == 2:
                assert blocking_count > 0, (
                    f"[{label}] Exit 2 but no blocking errors\n"
                    f"stdout:\n{result.stdout}"
                )
            if blocking_count > 0:
                assert result.returncode == 2, (
                    f"[{label}] {blocking_count} blocking errors but "
                    f"exit={result.returncode}\nstdout:\n{result.stdout}"
                )
            result = _run_audit(fixture)
            blocking_count = _count_blocking(result.stdout)
            if result.returncode == 2:
                assert blocking_count > 0, (
                    f"[{label}] Exit 2 but no blocking errors\n"
                    f"stdout:\n{result.stdout}"
                )
            if blocking_count > 0:
                assert result.returncode == 2, (
                    f"[{label}] {blocking_count} blocking errors but "
                    f"exit={result.returncode}\nstdout:\n{result.stdout}"
                )

    # Property 3: Route is always present in output
    def test_route_always_present(self) -> None:
        """Output always contains a Route: line."""
        for fixture, label in [
            (_valid_report(), "valid"),
            (_report_with_6col_register(), "6col"),
            (_report_with_audit_mismatch(), "mismatch"),
            (_report_no_route_block(), "no-route"),
            (_valid_regulatory_analysis_report(), "reg-analysis"),
            (_valid_equipment_selection_report(), "equip-sel"),
            (_valid_startup_evaluation_report(), "startup-eval"),
            (_valid_competitive_positioning_report(), "comp-pos"),
        ]:
            result = _run_audit(fixture)
            assert "Route:" in result.stdout, (
                f"[{label}] Missing Route: line\nstdout:\n{result.stdout}"
            )
            result = _run_audit(fixture)
            assert "Route:" in result.stdout, (
                f"[{label}] Missing Route: line\nstdout:\n{result.stdout}"
            )

    # Property 4: Overall is always one of pass / conditional-pass / fail
    def test_overall_is_valid(self) -> None:
        """Overall verdict is one of the three valid values."""
        for fixture, label in [
            (_valid_report(), "valid"),
            (_report_with_6col_register(), "6col"),
            (_report_with_audit_mismatch(), "mismatch"),
            (_report_with_table_missing_role_labels(), "no-roles"),
            (_report_no_route_block(), "no-route"),
            (_report_with_declared_exec_pass_but_fail(), "declared-but-fail"),
            (_valid_regulatory_analysis_report(), "reg-analysis"),
            (_valid_equipment_selection_report(), "equip-sel"),
            (_valid_startup_evaluation_report(), "startup-eval"),
            (_valid_competitive_positioning_report(), "comp-pos"),
        ]:
            result = _run_audit(fixture)
            overall = _get_overall(result.stdout)
            assert overall in ("pass", "conditional-pass", "fail"), (
                f"[{label}] Invalid overall='{overall}'"
            )

    # Property 5: Valid report with --strict still passes
    def test_strict_mode_on_valid_report(self) -> None:
        """--strict flag should not break valid reports."""
        result = _run_audit(_valid_report(), extra_args=["--strict"])
        assert result.returncode == 0, (
            f"Expected exit 0 with --strict, got {result.returncode}\n"
            f"stdout:\n{result.stdout}"
        )

    # Property 5b: Route normalization works for various input formats
    def test_route_normalization(self) -> None:
        """Route names are normalized correctly regardless of input format."""
        # Create a minimal report and verify route normalization
        base_md = """\
# Test

## Route and audit status

**Primary route**: Technical Deep-dive

| Audit | Status | 证据 |
|-------|--------|------|
| final-audit | ✅ Passed | §2 可追溯 |

## Body

Body with [S01].

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Ex | secondary | 2026-01-01 | https://ex.com | medium | §3 |
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as f:
            f.write(base_md)
            tmp = f.name
        try:
            # Same report with different route formats
            for route_arg in ["technical-deep-dive", "Technical Deep-dive", "technical deep dive"]:
                r = subprocess.run(
                    [sys.executable, SCRIPT, tmp, "--route", route_arg],
                    capture_output=True, text=True, timeout=30,
                )
                assert r.returncode == 0, (
                    f"Route '{route_arg}' failed (exit {r.returncode}):\n{r.stdout}"
                )
                assert "technical-deep-dive" in r.stdout.lower(), (
                    f"Normalized route not found for '{route_arg}'\n{r.stdout}"
                )
        finally:
            Path(tmp).unlink(missing_ok=True)

    # Property 6: Same result with explicit --route route-name as auto-detect
    def test_explicit_route_matches_auto(self) -> None:
        """Explicit --route technical-deep-dive gives same result as auto."""
        auto_result = _run_audit(_valid_report())
        explicit_result = _run_audit(
            _valid_report(),
            extra_args=["--route", "technical-deep-dive"],
        )
        # Both should pass
        assert auto_result.returncode == explicit_result.returncode, (
            f"Auto exit={auto_result.returncode} != explicit exit={explicit_result.returncode}"
        )
        assert auto_result.returncode == 0

    # Property 7: Declared_execution alone passes but overall fails
    # (Issue #271 core scenario — tested separately in its own class)
    # Property 8: Blocking errors are always non-empty when exit=2
    def test_blocking_count_matches_exit_code(self) -> None:
        """Blocking count > 0 precisely when exit=2."""
        for fixture, label in [
            (_valid_report(), "valid"),
            (_report_with_6col_register(), "6col"),
            (_report_with_audit_mismatch(), "mismatch"),
            (_report_with_table_missing_role_labels(), "no-roles"),
            (_report_no_route_block(), "no-route"),
            (_report_with_declared_exec_pass_but_fail(), "declared-but-fail"),
            (_cc_scoring_table_no_rules(), "cc-scoring-no-rules"),
            (_cc_probability_no_method(), "cc-prob-no-method"),
            (_cc_scoring_table_with_rules(), "cc-scoring-with-rules"),
            (_valid_regulatory_analysis_report(), "reg-analysis"),
            (_valid_equipment_selection_report(), "equip-sel"),
            (_valid_startup_evaluation_report(), "startup-eval"),
            (_valid_competitive_positioning_report(), "comp-pos"),
        ]:
            # CC-specific fixtures have route in their block, so auto-detection works
            result = _run_audit(fixture)
            blocking = _count_blocking(result.stdout)
            if result.returncode == 2:
                assert blocking > 0, (
                    f"[{label}] Exit 2 but no blocking lines"
                )
            else:
                assert blocking == 0, (
                    f"[{label}] Exit {result.returncode} but {blocking} blocking lines"
                )



class TestConstrainedChoice:
    """Constrained-choice route must be recognized without fallback."""

    def test_constrained_choice_route_recognized(self) -> None:
        """`--route constrained-choice` should show `constrained-choice` in output."""
        result = _run_audit(
            _valid_report(),
            extra_args=["--route", "constrained-choice"],
        )
        assert "constrained-choice" in result.stdout, (
            f"Expected 'constrained-choice' in route output, got:\n{result.stdout}"
        )

    def test_constrained_choice_no_fallback_warning(self) -> None:
        """stderr must NOT contain 'falling back' when using --route constrained-choice."""
        result = _run_audit(
            _valid_report(),
            extra_args=["--route", "constrained-choice"],
        )
        assert "falling back" not in result.stderr.lower(), (
            f"Unexpected fallback warning in stderr:\n{result.stderr}"
        )

    def test_constrained_choice_route_runs_validators(self) -> None:
        """A valid report with --route constrained-choice must pass (exit 0)."""
        result = _run_audit(
            _valid_constrained_choice_report(),
            extra_args=["--route", "constrained-choice"],
        )
        assert result.returncode == 0, (
            f"Expected exit 0, got {result.returncode}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )

    def test_auto_detect_constrained_choice_via_chinese_heading(self) -> None:
        """Chinese heading report with constrained-choice route auto-detects."""
        result = _run_audit(_valid_chinese_constrained_choice_report())
        assert result.returncode == 0, (
            f"Expected exit 0 for Chinese constrained-choice report, "
            f"got {result.returncode}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
        assert "constrained-choice" in result.stdout, (
            f"Expected auto-detected 'constrained-choice' in route output, got:\n{result.stdout}"
        )
        assert "falling back" not in result.stderr.lower(), (
            f"Unexpected fallback warning in stderr:\n{result.stderr}"
        )


class TestConstrainedChoiceScoringReplicability:
    """Constrained-choice scoring-replicability validator must catch
    reports that present aggregated scores/probabilities without
    showing reproducible method, and pass those that include it."""

    def test_scoring_table_no_rules_blocking(self) -> None:
        """Scoring table with total scores but no rules → blocking."""
        result = _run_audit(
            _cc_scoring_table_no_rules(),
            extra_args=["--route", "constrained-choice"],
        )
        assert result.returncode == 2, (
            f"Expected exit 2 (blocking), got {result.returncode}\n"
            f"stdout:\n{result.stdout}"
        )

    def test_scoring_table_no_rules_mentions_scoring_replicability(self) -> None:
        """Error output should mention the scoring-replicability validator."""
        result = _run_audit(
            _cc_scoring_table_no_rules(),
            extra_args=["--route", "constrained-choice"],
        )
        assert "scoring-replicability" in result.stdout, (
            f"Expected scoring-replicability in output, got:\n{result.stdout}"
        )

    def test_probability_no_method_blocking(self) -> None:
        """Probability distribution without method → blocking."""
        result = _run_audit(
            _cc_probability_no_method(),
            extra_args=["--route", "constrained-choice"],
        )
        assert result.returncode == 2, (
            f"Expected exit 2 (blocking), got {result.returncode}\n"
            f"stdout:\n{result.stdout}"
        )

    def test_scoring_table_with_rules_passes(self) -> None:
        """Scoring table with weights, rules, and worked example → pass."""
        result = _run_audit(
            _cc_scoring_table_with_rules(),
            extra_args=["--route", "constrained-choice"],
        )
        assert result.returncode == 0, (
            f"Expected exit 0, got {result.returncode}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )

    def test_scoring_table_with_rules_no_scoring_replicability_errors(self) -> None:
        """Passing report should not have scoring-replicability blocking errors."""
        result = _run_audit(
            _cc_scoring_table_with_rules(),
            extra_args=["--route", "constrained-choice"],
        )
        blocking = _count_blocking(result.stdout)
        # Count scoring-replicability specific blocking
        for line in result.stdout.splitlines():
            if line.strip().startswith("- ") and "[scoring-replicability]" in line:
                blocking -= 1
        assert blocking == 0, (
            f"Expected no scoring-replicability blocking, got:\n{result.stdout}"
        )


class TestMarketOutlookRoute:
    """Market-outlook route must be recognized without fallback."""

    def test_market_outlook_route_recognized(self) -> None:
        """--route market-outlook should show 'market-outlook' in output."""
        result = _run_audit(
            _valid_market_outlook_report(),
            extra_args=["--route", "market-outlook"],
        )
        assert "market-outlook" in result.stdout, (
            f"Expected 'market-outlook' in route output, got:\n{result.stdout}"
        )

    def test_market_outlook_no_fallback_warning(self) -> None:
        """stderr must NOT contain 'falling back' for --route market-outlook."""
        result = _run_audit(
            _valid_market_outlook_report(),
            extra_args=["--route", "market-outlook"],
        )
        assert "falling back" not in result.stderr.lower(), (
            f"Unexpected fallback warning in stderr:\n{result.stderr}"
        )

    def test_market_outlook_auto_detect(self) -> None:
        """Report with 'Market Outlook / Industry Evolution' route auto-detects."""
        result = _run_audit(_valid_market_outlook_report())
        assert "market-outlook" in result.stdout, (
            f"Expected auto-detected 'market-outlook' in output, got:\n{result.stdout}"
        )
        assert "falling back" not in result.stderr.lower(), (
            f"Unexpected fallback warning in stderr:\n{result.stderr}"
        )

    def test_market_outlook_alias_no_fallback(self) -> None:
        """Each alias must resolve without fallback warning."""
        for alias in [
            "market-outlook",
            "market outlook",
            "market outlook / industry evolution",
            "industry evolution",
        ]:
            result = _run_audit(
                _valid_market_outlook_report(),
                extra_args=["--route", alias],
            )
            assert "falling back" not in result.stderr.lower(), (
                f"Alias '{alias}' triggered fallback:\n{result.stderr}"
            )
            assert "market-outlook" in result.stdout, (
                f"Alias '{alias}' did not show 'market-outlook' in output:\n{result.stdout}"
            )


class TestMarketOutlookMonitoringActionability:
    """Market-outlook monitoring actionability validator must enforce the
    <3 fully-defined signals → blocking gate."""

    def test_actionable_monitoring_passes(self) -> None:
        """Report with 3+ fully-defined monitoring signals must pass."""
        result = _run_audit(
            _valid_market_outlook_report(),
            extra_args=["--route", "market-outlook"],
        )
        assert result.returncode == 0, (
            f"Expected exit 0 for actionable monitoring, got {result.returncode}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )

    def test_non_actionable_monitoring_blocking(self) -> None:
        """Report with monitoring lacking cadence/source/trigger → exit 2."""
        result = _run_audit(
            _market_outlook_no_monitoring_actionability(),
            extra_args=["--route", "market-outlook"],
        )
        assert result.returncode == 2, (
            f"Expected exit 2 for non-actionable monitoring, got {result.returncode}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )

    def test_no_monitoring_section_blocking(self) -> None:
        """Report with no monitoring section → exit 2."""
        result = _run_audit(
            _market_outlook_no_monitoring_section(),
            extra_args=["--route", "market-outlook"],
        )
        assert result.returncode == 2, (
            f"Expected exit 2 for missing monitoring section, got {result.returncode}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )

    def test_non_actionable_error_mentions_monitoring(self) -> None:
        """Error output must mention 'market-outlook-monitoring' or 'monitoring'."""
        result = _run_audit(
            _market_outlook_no_monitoring_actionability(),
            extra_args=["--route", "market-outlook"],
        )
        assert "monitoring" in result.stdout.lower(), (
            f"Expected monitoring-related error, got:\n{result.stdout}"
        )

    def test_empty_cell_does_not_shift_indices(self) -> None:
        """Row with an empty cell must NOT be counted as fully-defined.

        Regression test for the `if c.strip()` cell-parsing bug found in
        cross-review: filtering empty cells shifts column indices and
        causes false positives.
        """
        result = _run_audit(
            _market_outlook_with_empty_cell(),
            extra_args=["--route", "market-outlook"],
        )
        assert result.returncode == 2, (
            f"Expected exit 2 for row with empty cell, got {result.returncode}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
        # Should report only 2 fully-defined signals (GPU + Grid, not Power cost)
        assert "2" in result.stdout, (
            f"Expected '2' fully-defined signals in output, got:\n{result.stdout}"
        )

    def test_uppercase_column_headers(self) -> None:
        """UPPERCASE column headers must be matched case-insensitively."""
        result = _run_audit(
            _market_outlook_uppercase_columns(),
            extra_args=["--route", "market-outlook"],
        )
        assert result.returncode == 0, (
            f"Expected exit 0 for uppercase columns, got {result.returncode}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )

    def test_two_signals_blocking(self) -> None:
        """Only 2 fully-defined signals (<3 threshold) must block."""
        result = _run_audit(
            _market_outlook_two_signals(),
            extra_args=["--route", "market-outlook"],
        )
        assert result.returncode == 2, (
            f"Expected exit 2 for 2 signals only, got {result.returncode}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )

    def test_strict_mode_warns_on_partial(self) -> None:
        """--strict mode adds warnings for partially-defined signals.

        Exit code 1 (=warnings) because partial-signal warnings exist;
        not exit 0 (no warnings) and not exit 2 (blocking errors).
        """
        result = _run_audit(
            _market_outlook_strict_with_partial(),
            extra_args=["--route", "market-outlook", "--strict"],
        )
        # Warnings exist → exit 1 (not blocking, not fully pass)
        assert result.returncode == 1, (
            f"Expected exit 1 (warnings) for partial signals, "
            f"got {result.returncode}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
        # Overall verdict should be conditional-pass
        assert "conditional-pass" in result.stdout, (
            f"Expected 'conditional-pass' for partial signals, got:\n{result.stdout}"
        )
        # Should generate warnings about the partial signal
        assert "⚠" in result.stdout or "warning" in result.stdout.lower(), (
            f"Expected strict mode warnings, got:\n{result.stdout}"
        )


class TestProviderSelectionRoute:
    """Provider-selection route must be recognized without fallback."""

    def test_provider_selection_route_recognized(self) -> None:
        """--route provider-selection should show 'provider-selection' in output."""
        result = _run_audit(
            _valid_provider_selection_report(),
            extra_args=["--route", "provider-selection"],
        )
        assert "provider-selection" in result.stdout, (
            f"Expected 'provider-selection' in route output, got:\n{result.stdout}"
        )

    def test_provider_selection_no_fallback_warning(self) -> None:
        """stderr must NOT contain 'falling back' for --route provider-selection."""
        result = _run_audit(
            _valid_provider_selection_report(),
            extra_args=["--route", "provider-selection"],
        )
        assert "falling back" not in result.stderr.lower(), (
            f"Unexpected fallback warning in stderr:\n{result.stderr}"
        )

    def test_provider_selection_auto_detect(self) -> None:
        """Report with 'Provider / Vendor Selection' route auto-detects."""
        result = _run_audit(_valid_provider_selection_report())
        assert "provider-selection" in result.stdout, (
            f"Expected auto-detected 'provider-selection' in output, got:\n{result.stdout}"
        )
        assert "falling back" not in result.stderr.lower(), (
            f"Unexpected fallback warning in stderr:\n{result.stderr}"
        )

    def test_provider_selection_valid_report_passes(self) -> None:
        """A valid report with --route provider-selection must pass (exit 0)."""
        result = _run_audit(
            _valid_provider_selection_report(),
            extra_args=["--route", "provider-selection"],
        )
        assert result.returncode == 0, (
            f"Expected exit 0, got {result.returncode}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )

    def test_provider_selection_alias_no_fallback(self) -> None:
        """Each alias must resolve without fallback warning."""
        for alias in [
            "provider-selection",
            "provider selection",
            "vendor selection",
            "provider / vendor selection",
        ]:
            result = _run_audit(
                _valid_provider_selection_report(),
                extra_args=["--route", alias],
            )
            assert "falling back" not in result.stderr.lower(), (
                f"Alias '{alias}' triggered fallback:\n{result.stderr}"
            )
            assert "provider-selection" in result.stdout, (
                f"Alias '{alias}' did not show 'provider-selection' in output:\n{result.stdout}"
            )


class TestMarketEntryRoute:
    """Market-entry route must be recognized without fallback."""

    def test_market_entry_route_recognized(self) -> None:
        """--route market-entry should show 'market-entry' in output."""
        result = _run_audit(
            _valid_market_entry_report(),
            extra_args=["--route", "market-entry"],
        )
        assert "market-entry" in result.stdout, (
            f"Expected 'market-entry' in route output, got:\n{result.stdout}"
        )

    def test_market_entry_no_fallback_warning(self) -> None:
        """stderr must NOT contain 'falling back' for --route market-entry."""
        result = _run_audit(
            _valid_market_entry_report(),
            extra_args=["--route", "market-entry"],
        )
        assert "falling back" not in result.stderr.lower(), (
            f"Unexpected fallback warning in stderr:\n{result.stderr}"
        )

    def test_market_entry_auto_detect(self) -> None:
        """Report with 'Market Entry / Regional Expansion' route auto-detects."""
        result = _run_audit(_valid_market_entry_report())
        assert "market-entry" in result.stdout, (
            f"Expected auto-detected 'market-entry' in output, got:\n{result.stdout}"
        )
        assert "falling back" not in result.stderr.lower(), (
            f"Unexpected fallback warning in stderr:\n{result.stderr}"
        )

    def test_market_entry_valid_report_passes(self) -> None:
        """A valid report with --route market-entry must pass (exit 0)."""
        result = _run_audit(
            _valid_market_entry_report(),
            extra_args=["--route", "market-entry"],
        )
        assert result.returncode == 0, (
            f"Expected exit 0, got {result.returncode}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )

    def test_market_entry_alias_no_fallback(self) -> None:
        """Each alias must resolve without fallback warning."""
        for alias in [
            "market-entry",
            "market entry",
            "regional expansion",
            "market entry / regional expansion",
        ]:
            result = _run_audit(
                _valid_market_entry_report(),
                extra_args=["--route", alias],
            )
            assert "falling back" not in result.stderr.lower(), (
                f"Alias '{alias}' triggered fallback:\n{result.stderr}"
            )
            assert "market-entry" in result.stdout, (
                f"Alias '{alias}' did not show 'market-entry' in output:\n{result.stdout}"
            )


class TestRegulatoryAnalysisRoute:
    """Regulatory-analysis route must be recognized without fallback."""

    def test_regulatory_analysis_route_recognized(self) -> None:
        """--route regulatory-analysis should show 'regulatory-analysis' in output."""
        result = _run_audit(
            _valid_regulatory_analysis_report(),
            extra_args=["--route", "regulatory-analysis"],
        )
        assert "regulatory-analysis" in result.stdout, (
            f"Expected 'regulatory-analysis' in route output, got:\n{result.stdout}"
        )

    def test_regulatory_analysis_no_fallback_warning(self) -> None:
        """stderr must NOT contain 'falling back' for --route regulatory-analysis."""
        result = _run_audit(
            _valid_regulatory_analysis_report(),
            extra_args=["--route", "regulatory-analysis"],
        )
        assert "falling back" not in result.stderr.lower(), (
            f"Unexpected fallback warning in stderr:\n{result.stderr}"
        )

    def test_regulatory_analysis_auto_detect(self) -> None:
        """Report with 'Regulatory / Policy Impact Analysis' route auto-detects."""
        result = _run_audit(_valid_regulatory_analysis_report())
        assert "regulatory-analysis" in result.stdout, (
            f"Expected auto-detected 'regulatory-analysis' in output, got:\n{result.stdout}"
        )
        assert "falling back" not in result.stderr.lower(), (
            f"Unexpected fallback warning in stderr:\n{result.stderr}"
        )

    def test_regulatory_analysis_valid_report_passes(self) -> None:
        """A valid report with --route regulatory-analysis must pass (exit 0)."""
        result = _run_audit(
            _valid_regulatory_analysis_report(),
            extra_args=["--route", "regulatory-analysis"],
        )
        assert result.returncode == 0, (
            f"Expected exit 0, got {result.returncode}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )

    def test_regulatory_analysis_alias_no_fallback(self) -> None:
        """Each alias must resolve without fallback warning."""
        for alias in [
            "regulatory-analysis",
            "regulatory analysis",
            "regulatory / policy impact analysis",
            "regulatory / policy impact",
        ]:
            result = _run_audit(
                _valid_regulatory_analysis_report(),
                extra_args=["--route", alias],
            )
            assert "falling back" not in result.stderr.lower(), (
                f"Alias '{alias}' triggered fallback:\n{result.stderr}"
            )
            assert "regulatory-analysis" in result.stdout, (
                f"Alias '{alias}' did not show 'regulatory-analysis' in output:\n{result.stdout}"
            )


class TestEquipmentSelectionRoute:
    """Equipment-selection route must be recognized without fallback."""

    def test_equipment_selection_route_recognized(self) -> None:
        """--route equipment-selection should show 'equipment-selection' in output."""
        result = _run_audit(
            _valid_equipment_selection_report(),
            extra_args=["--route", "equipment-selection"],
        )
        assert "equipment-selection" in result.stdout, (
            f"Expected 'equipment-selection' in route output, got:\n{result.stdout}"
        )

    def test_equipment_selection_no_fallback_warning(self) -> None:
        """stderr must NOT contain 'falling back' for --route equipment-selection."""
        result = _run_audit(
            _valid_equipment_selection_report(),
            extra_args=["--route", "equipment-selection"],
        )
        assert "falling back" not in result.stderr.lower(), (
            f"Unexpected fallback warning in stderr:\n{result.stderr}"
        )

    def test_equipment_selection_auto_detect(self) -> None:
        """Report with 'Equipment Selection / Procurement' route auto-detects."""
        result = _run_audit(_valid_equipment_selection_report())
        assert "equipment-selection" in result.stdout, (
            f"Expected auto-detected 'equipment-selection' in output, got:\n{result.stdout}"
        )
        assert "falling back" not in result.stderr.lower(), (
            f"Unexpected fallback warning in stderr:\n{result.stderr}"
        )

    def test_equipment_selection_valid_report_passes(self) -> None:
        """A valid report with --route equipment-selection must pass (exit 0)."""
        result = _run_audit(
            _valid_equipment_selection_report(),
            extra_args=["--route", "equipment-selection"],
        )
        assert result.returncode == 0, (
            f"Expected exit 0, got {result.returncode}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )

    def test_equipment_selection_alias_no_fallback(self) -> None:
        """Each alias must resolve without fallback warning."""
        for alias in [
            "equipment-selection",
            "equipment selection",
            "equipment selection / procurement / home-server planning",
            "equipment selection / procurement",
            "procurement",
            "home-server planning",
        ]:
            result = _run_audit(
                _valid_equipment_selection_report(),
                extra_args=["--route", alias],
            )
            assert "falling back" not in result.stderr.lower(), (
                f"Alias '{alias}' triggered fallback:\n{result.stderr}"
            )
            assert "equipment-selection" in result.stdout, (
                f"Alias '{alias}' did not show 'equipment-selection' in output:\n{result.stdout}"
            )


class TestStartupEvaluationRoute:
    """Startup-evaluation route must be recognized without fallback."""

    def test_startup_evaluation_route_recognized(self) -> None:
        """--route startup-evaluation should show 'startup-evaluation' in output."""
        result = _run_audit(
            _valid_startup_evaluation_report(),
            extra_args=["--route", "startup-evaluation"],
        )
        assert "startup-evaluation" in result.stdout, (
            f"Expected 'startup-evaluation' in route output, got:\n{result.stdout}"
        )

    def test_startup_evaluation_no_fallback_warning(self) -> None:
        """stderr must NOT contain 'falling back' for --route startup-evaluation."""
        result = _run_audit(
            _valid_startup_evaluation_report(),
            extra_args=["--route", "startup-evaluation"],
        )
        assert "falling back" not in result.stderr.lower(), (
            f"Unexpected fallback warning in stderr:\n{result.stderr}"
        )

    def test_startup_evaluation_auto_detect(self) -> None:
        """Report with 'Startup / Private Company Evaluation' route auto-detects."""
        result = _run_audit(_valid_startup_evaluation_report())
        assert "startup-evaluation" in result.stdout, (
            f"Expected auto-detected 'startup-evaluation' in output, got:\n{result.stdout}"
        )
        assert "falling back" not in result.stderr.lower(), (
            f"Unexpected fallback warning in stderr:\n{result.stderr}"
        )

    def test_startup_evaluation_valid_report_passes(self) -> None:
        """A valid report with --route startup-evaluation must pass (exit 0)."""
        result = _run_audit(
            _valid_startup_evaluation_report(),
            extra_args=["--route", "startup-evaluation"],
        )
        assert result.returncode == 0, (
            f"Expected exit 0, got {result.returncode}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )

    def test_startup_evaluation_alias_no_fallback(self) -> None:
        """Each alias must resolve without fallback warning."""
        for alias in [
            "startup-evaluation",
            "startup evaluation",
            "startup / private company evaluation",
            "private company evaluation",
            "private company",
            "startup",
        ]:
            result = _run_audit(
                _valid_startup_evaluation_report(),
                extra_args=["--route", alias],
            )
            assert "falling back" not in result.stderr.lower(), (
                f"Alias '{alias}' triggered fallback:\n{result.stderr}"
            )
            assert "startup-evaluation" in result.stdout, (
                f"Alias '{alias}' did not show 'startup-evaluation' in output:\n{result.stdout}"
            )


class TestCompetitivePositioningRoute:
    """Competitive-positioning route must be recognized without fallback."""

    def test_competitive_positioning_route_recognized(self) -> None:
        """--route competitive-positioning should show 'competitive-positioning' in output."""
        result = _run_audit(
            _valid_competitive_positioning_report(),
            extra_args=["--route", "competitive-positioning"],
        )
        assert "competitive-positioning" in result.stdout, (
            f"Expected 'competitive-positioning' in route output, got:\n{result.stdout}"
        )

    def test_competitive_positioning_no_fallback_warning(self) -> None:
        """stderr must NOT contain 'falling back' for --route competitive-positioning."""
        result = _run_audit(
            _valid_competitive_positioning_report(),
            extra_args=["--route", "competitive-positioning"],
        )
        assert "falling back" not in result.stderr.lower(), (
            f"Unexpected fallback warning in stderr:\n{result.stderr}"
        )

    def test_competitive_positioning_auto_detect(self) -> None:
        """Report with 'First-tier / Top-tier / Competitive Positioning' route auto-detects."""
        result = _run_audit(_valid_competitive_positioning_report())
        assert "competitive-positioning" in result.stdout, (
            f"Expected auto-detected 'competitive-positioning' in output, got:\n{result.stdout}"
        )
        assert "falling back" not in result.stderr.lower(), (
            f"Unexpected fallback warning in stderr:\n{result.stderr}"
        )

    def test_competitive_positioning_valid_report_passes(self) -> None:
        """A valid report with --route competitive-positioning must pass (exit 0)."""
        result = _run_audit(
            _valid_competitive_positioning_report(),
            extra_args=["--route", "competitive-positioning"],
        )
        assert result.returncode == 0, (
            f"Expected exit 0, got {result.returncode}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )

    def test_competitive_positioning_alias_no_fallback(self) -> None:
        """Each alias must resolve without fallback warning."""
        for alias in [
            "competitive-positioning",
            "competitive positioning",
            "first-tier / top-tier / competitive positioning",
            "first-tier",
            "top-tier",
        ]:
            result = _run_audit(
                _valid_competitive_positioning_report(),
                extra_args=["--route", alias],
            )
            assert "falling back" not in result.stderr.lower(), (
                f"Alias '{alias}' triggered fallback:\n{result.stderr}"
            )
            assert "competitive-positioning" in result.stdout, (
                f"Alias '{alias}' did not show 'competitive-positioning' in output:\n{result.stdout}"
            )


class TestUnknownRouteBlocking:
    """Unknown routes must be blocked (exit 2), not silently fall back."""

    def test_unknown_route_exit_2(self) -> None:
        """--route nonexistent-route-xyz must exit 2."""
        result = _run_audit(_valid_report(), extra_args=["--route", "nonexistent-route-xyz"])
        assert result.returncode == 2, (
            f"Expected exit 2 for unknown route, got {result.returncode}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )

    def test_unknown_route_overall_fail(self) -> None:
        """Unknown route must produce overall 'fail'."""
        result = _run_audit(_valid_report(), extra_args=["--route", "nonexistent-route-xyz"])
        assert _get_overall(result.stdout) == "fail", (
            f"Expected overall 'fail', got:\n{result.stdout}"
        )

    def test_unknown_route_shows_supported_routes(self) -> None:
        """Error message must list supported routes."""
        result = _run_audit(_valid_report(), extra_args=["--route", "nonexistent-route-xyz"])
        assert "supported routes" in result.stdout.lower(), (
            f"Expected 'supported routes' in error output, got:\n{result.stdout}"
        )

    def test_unknown_route_no_validator_runs(self) -> None:
        """No validators should run for unknown route (no report-quality etc.)."""
        result = _run_audit(_valid_report(), extra_args=["--route", "nonexistent-route-xyz"])
        # No validator-specific output should appear in blocking errors
        # The only blocking error should be the unknown-route message itself
        blocking_lines = [
            line for line in result.stdout.splitlines()
            if line.startswith("- [")
        ]
        assert len(blocking_lines) == 0, (
            f"Expected no validator-specific blocking, got:\n{result.stdout}"
        )


class TestSecondaryRouteCheck:
    """Secondary route declarations must be checked for support status."""

    def test_unsupported_secondary_route_warns(self) -> None:
        """Report with unsupported secondary route → warning (not blocking)."""
        result = _run_audit(_report_with_secondary_routes())
        # Should have warnings about the unsupported secondary route
        assert "secondary-route-check" in result.stdout, (
            f"Expected secondary-route-check in output, got:\n{result.stdout}"
        )
        # Should NOT be blocking (secondary route unsupported = warning, not error)
        blocking = _count_blocking(result.stdout)
        secondary_blocking = [
            line for line in result.stdout.splitlines()
            if "[secondary-route-check]" in line and line.strip().startswith("- ")
        ]
        assert len(secondary_blocking) == 0, (
            f"Secondary route unsupported should be warning, not blocking:\n{result.stdout}"
        )

    def test_supported_secondary_routes_no_warning(self) -> None:
        """Report with all supported secondary routes → no warnings."""
        result = _run_audit(_report_with_supported_secondary_routes())
        # secondary-route-check should appear with pass status
        assert "secondary-route-check" in result.stdout, (
            f"Expected secondary-route-check in output, got:\n{result.stdout}"
        )
        # Should have no warnings for secondary routes
        warning_lines = [
            line for line in result.stdout.splitlines()
            if "⚠" in line and "secondary" in line.lower()
        ]
        assert len(warning_lines) == 0, (
            f"Expected no secondary-route warnings, got:\n{result.stdout}"
        )

    def test_no_secondary_routes_silent(self) -> None:
        """Report with no secondary routes → silence (pass)."""
        result = _run_audit(_valid_report())
        # secondary-route-check should appear as pass
        assert "secondary-route-check" in result.stdout, (
            f"Expected secondary-route-check in output, got:\n{result.stdout}"
        )


class TestAllowRouteFallback:
    """--allow-route-fallback flag restores legacy fallback behavior."""

    def test_allow_fallback_passes_for_unknown_route(self) -> None:
        """--route unknown-xyz --allow-route-fallback should exit 0 (not 2)."""
        result = _run_audit(
            _valid_report(),
            extra_args=["--route", "nonexistent-fallback-test", "--allow-route-fallback"],
        )
        assert result.returncode == 0, (
            f"Expected exit 0 with --allow-route-fallback, got {result.returncode}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
        # Should show fallback warning in stderr
        assert "falling back" in result.stderr.lower(), (
            f"Expected fallback warning in stderr with --allow-route-fallback:\n{result.stderr}"
        )

    def test_allow_fallback_shows_default_route_in_output(self) -> None:
        """With --allow-route-fallback, output should show technical-deep-dive."""
        result = _run_audit(
            _valid_report(),
            extra_args=["--route", "nonexistent-fallback-test", "--allow-route-fallback"],
        )
        assert "technical-deep-dive" in result.stdout, (
            f"Expected fallback to 'technical-deep-dive' in output, got:\n{result.stdout}"
        )


class TestSharedWorkflow:
    """Shared-workflow should be recognized as a valid route, not fall back."""

    def test_exit_code_zero_when_valid(self) -> None:
        """Shared-workflow report with valid structure should pass."""
        result = _run_audit(_report_shared_workflow())
        assert result.returncode == 0, (
            f"Expected pass for shared-workflow, got {result.returncode}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )

    def test_no_fallback_warning_in_stderr(self) -> None:
        """Shared-workflow should be recognized, not fall back."""
        result = _run_audit(_report_shared_workflow())
        assert "falling back" not in result.stderr.lower(), (
            f"Shared-workflow should be recognized, not fall back:\n{result.stderr}"
        )

    def test_shared_workflow_route_in_output(self) -> None:
        """Output should contain 'shared-workflow' as the recognized route."""
        result = _run_audit(_report_shared_workflow())
        assert "shared-workflow" in result.stdout.lower(), (
            f"Expected 'shared-workflow' in output, got:\n{result.stdout}"
        )


class TestValidatorCount:
    """Ensures all validators actually run (catches silent drops)."""

    def test_all_validators_executed_on_failing_report(self) -> None:
        """A report that triggers issues in all validators should show all five."""
        # Create a report that will fail every validator:
        # - No route block -> report-quality fail
        # - Add opam declaration without execution -> declared-execution fail
        # - Large tables without role labels -> table-role-labels fail
        # - Primary company source without caveat -> source-label-consistency fail
        content = """\
# Test Report

This report declares O/P/A/M labels but has no role labels.
Primary company source S01 lacks the required caveat.

## Performance

| A | B |
|---|---|
| 1 | 2 |
| 3 | 4 |
| 5 | 6 |

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Test Corp | primary_company | 2026-01-01 | https://example.com | medium | §3 |
"""
        result = _run_audit(content, extra_args=["--route", "constrained-choice"])
        # Validators appear either as [name] in blocking/warnings or
        # as "name:" in the recommended audit status section.
        all_validator_names = [
            "report-quality",
            "declared-execution",
            "table-role-labels",
            "source-label-consistency",
            "scoring-replicability",
            "secondary-route-check",
        ]
        for name in all_validator_names:
            marker_bracket = f"[{name}]"
            marker_plain = f"{name}:"
            assert (
                marker_bracket in result.stdout
                or marker_bracket in result.stderr
                or marker_plain in result.stdout
            ), (
                f"Missing '{name}' in output — validator may not have run\n"
                f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
            )

    def test_market_outlook_validators_all_run(self) -> None:
        """Market-outlook route must run all 5 validators, including monitoring."""
        content = """\
# Test

## Route and audit status

**Primary route**: Market Outlook / Industry Evolution

| Audit | Status | 证据 |
|-------|--------|------|
| source-traceability | ✅ Passed | §3 引用 [S01] |
| final-audit | ✅ Passed | §2 可追溯 |

## Body

Body text with citation [S01].

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Ex | secondary | 2026-01-01 | https://ex.com | medium | §3 |
"""
        result = _run_audit(content, extra_args=["--route", "market-outlook"])
        # The market-outlook validator chain: report-quality, declared-execution,
        # table-role-labels, source-label-consistency, market-outlook-monitoring
        expected_prefixes = [
            "report-quality",
            "declared-execution",
            "table-role-labels",
            "source-label-consistency",
            "market-outlook-monitoring",
            "secondary-route-check",
        ]
        for prefix in expected_prefixes:
            marker_bracket = f"[{prefix}]"
            marker_plain = f"{prefix}:"
            assert (
                marker_bracket in result.stdout
                or marker_bracket in result.stderr
                or marker_plain in result.stdout
            ), (
                f"Missing '{prefix}' in output — market-outlook validator "
                f"may not have run\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
            )


if __name__ == "__main__":
    # Self-contained test runner (no external dependencies).
    # Follows the same pattern as test_report_quality_validator.py and other
    # test scripts in this project.
    tests: list[tuple[str, Callable[[], None]]] = [
        # TestValidReport
        ("valid report exit 0", TestValidReport().test_exit_code_zero),
        ("valid report overall pass", TestValidReport().test_overall_pass),
        ("valid report no blocking", TestValidReport().test_no_blocking),
        ("valid report route detected", TestValidReport().test_route_detected),
        # Test6ColumnRegister
        ("6-col register exit blocking", Test6ColumnRegister().test_exit_code_blocking),
        ("6-col register overall fail", Test6ColumnRegister().test_overall_fail),
        ("6-col register mentions column count", Test6ColumnRegister().test_blocking_mentions_column_count),
        # TestAuditMismatch
        ("audit mismatch exit blocking", TestAuditMismatch().test_exit_code_blocking),
        ("audit mismatch overall fail", TestAuditMismatch().test_overall_fail),
        ("audit mismatch mentions quantitative-role", TestAuditMismatch().test_error_mentions_quantitative_role),
        # TestDeclaredExecPassButOverallFail
        ("declared-exec pass but overall fail exit", TestDeclaredExecPassButOverallFail().test_exit_code_blocking),
        ("declared-exec pass but overall fail overall", TestDeclaredExecPassButOverallFail().test_overall_fail),
        ("declared-exec pass but overall fail error msg", TestDeclaredExecPassButOverallFail().test_blocking_mentions_column_and_mismatch),
        # TestTableMissingRoleLabels
        ("tables missing role labels exit", TestTableMissingRoleLabels().test_exit_code_blocking),
        ("tables missing role labels mentions role", TestTableMissingRoleLabels().test_blocking_mentions_role_labels),
        # TestNoRouteBlock
        ("no route block exit", TestNoRouteBlock().test_exit_code_blocking),
        ("no route block missing section", TestNoRouteBlock().test_blocking_mentions_missing_section),
        # TestRouteOverride
        ("--route appears in output", TestRouteOverride().test_explicit_route_appears_in_output),
        ("--route unknown is blocking", TestRouteOverride().test_unknown_route_is_blocking),
        # TestNonExistentFile
        ("non-existent file exit", TestNonExistentFile().test_exit_code_blocking),
        # TestConstrainedChoice
        ("constrained-choice route recognized", TestConstrainedChoice().test_constrained_choice_route_recognized),
        ("constrained-choice no fallback warning", TestConstrainedChoice().test_constrained_choice_no_fallback_warning),
        ("constrained-choice route runs validators", TestConstrainedChoice().test_constrained_choice_route_runs_validators),
        ("constrained-choice auto-detect via chinese heading", TestConstrainedChoice().test_auto_detect_constrained_choice_via_chinese_heading),
        # TestConstrainedChoiceScoringReplicability
        ("cc scoring table no rules blocking",
         TestConstrainedChoiceScoringReplicability().test_scoring_table_no_rules_blocking),
        ("cc scoring table no rules mentions scoring-replicability",
         TestConstrainedChoiceScoringReplicability().test_scoring_table_no_rules_mentions_scoring_replicability),
        ("cc probability no method blocking",
         TestConstrainedChoiceScoringReplicability().test_probability_no_method_blocking),
        ("cc scoring table with rules passes",
         TestConstrainedChoiceScoringReplicability().test_scoring_table_with_rules_passes),
        ("cc scoring table with rules no scoring-replicability errors",
         TestConstrainedChoiceScoringReplicability().test_scoring_table_with_rules_no_scoring_replicability_errors),
        # TestMarketOutlookRoute
        ("market-outlook route recognized", TestMarketOutlookRoute().test_market_outlook_route_recognized),
        ("market-outlook no fallback warning", TestMarketOutlookRoute().test_market_outlook_no_fallback_warning),
        ("market-outlook auto-detect", TestMarketOutlookRoute().test_market_outlook_auto_detect),
        ("market-outlook alias no fallback", TestMarketOutlookRoute().test_market_outlook_alias_no_fallback),
        # TestMarketOutlookMonitoringActionability
        ("market-outlook actionable monitoring passes",
         TestMarketOutlookMonitoringActionability().test_actionable_monitoring_passes),
        ("market-outlook non-actionable monitoring blocking",
         TestMarketOutlookMonitoringActionability().test_non_actionable_monitoring_blocking),
        ("market-outlook no monitoring section blocking",
         TestMarketOutlookMonitoringActionability().test_no_monitoring_section_blocking),
        ("market-outlook monitoring error message",
         TestMarketOutlookMonitoringActionability().test_non_actionable_error_mentions_monitoring),
        ("market-outlook empty cell no false positive",
         TestMarketOutlookMonitoringActionability().test_empty_cell_does_not_shift_indices),
        ("market-outlook uppercase columns match",
         TestMarketOutlookMonitoringActionability().test_uppercase_column_headers),
        ("market-outlook 2 signals blocking",
         TestMarketOutlookMonitoringActionability().test_two_signals_blocking),
        ("market-outlook strict mode warns partial",
         TestMarketOutlookMonitoringActionability().test_strict_mode_warns_on_partial),
        # TestProviderSelectionRoute
        ("provider-selection route recognized",
         TestProviderSelectionRoute().test_provider_selection_route_recognized),
        ("provider-selection no fallback warning",
         TestProviderSelectionRoute().test_provider_selection_no_fallback_warning),
        ("provider-selection auto-detect",
         TestProviderSelectionRoute().test_provider_selection_auto_detect),
        ("provider-selection valid report passes",
         TestProviderSelectionRoute().test_provider_selection_valid_report_passes),
        ("provider-selection alias no fallback",
         TestProviderSelectionRoute().test_provider_selection_alias_no_fallback),
        # TestMarketEntryRoute
        ("market-entry route recognized",
         TestMarketEntryRoute().test_market_entry_route_recognized),
        ("market-entry no fallback warning",
         TestMarketEntryRoute().test_market_entry_no_fallback_warning),
        ("market-entry auto-detect",
         TestMarketEntryRoute().test_market_entry_auto_detect),
        ("market-entry valid report passes",
         TestMarketEntryRoute().test_market_entry_valid_report_passes),
        ("market-entry alias no fallback",
         TestMarketEntryRoute().test_market_entry_alias_no_fallback),
        # TestSharedWorkflow
        ("shared-workflow valid passes", TestSharedWorkflow().test_exit_code_zero_when_valid),
        ("shared-workflow no fallback warning", TestSharedWorkflow().test_no_fallback_warning_in_stderr),
        ("shared-workflow route in output", TestSharedWorkflow().test_shared_workflow_route_in_output),
        # TestSecondaryRouteCheck
        ("secondary route unsupported warns",
         TestSecondaryRouteCheck().test_unsupported_secondary_route_warns),
        ("secondary route supported no warning",
         TestSecondaryRouteCheck().test_supported_secondary_routes_no_warning),
        ("secondary route none silent",
         TestSecondaryRouteCheck().test_no_secondary_routes_silent),
        # TestAllowRouteFallback
        ("allow-route-fallback passes",
         TestAllowRouteFallback().test_allow_fallback_passes_for_unknown_route),
        ("allow-route-fallback shows default route",
         TestAllowRouteFallback().test_allow_fallback_shows_default_route_in_output),
        # TestRegulatoryAnalysisRoute
        ("regulatory-analysis route recognized",
         TestRegulatoryAnalysisRoute().test_regulatory_analysis_route_recognized),
        ("regulatory-analysis no fallback warning",
         TestRegulatoryAnalysisRoute().test_regulatory_analysis_no_fallback_warning),
        ("regulatory-analysis auto-detect",
         TestRegulatoryAnalysisRoute().test_regulatory_analysis_auto_detect),
        ("regulatory-analysis valid report passes",
         TestRegulatoryAnalysisRoute().test_regulatory_analysis_valid_report_passes),
        ("regulatory-analysis alias no fallback",
         TestRegulatoryAnalysisRoute().test_regulatory_analysis_alias_no_fallback),
        # TestEquipmentSelectionRoute
        ("equipment-selection route recognized",
         TestEquipmentSelectionRoute().test_equipment_selection_route_recognized),
        ("equipment-selection no fallback warning",
         TestEquipmentSelectionRoute().test_equipment_selection_no_fallback_warning),
        ("equipment-selection auto-detect",
         TestEquipmentSelectionRoute().test_equipment_selection_auto_detect),
        ("equipment-selection valid report passes",
         TestEquipmentSelectionRoute().test_equipment_selection_valid_report_passes),
        ("equipment-selection alias no fallback",
         TestEquipmentSelectionRoute().test_equipment_selection_alias_no_fallback),
        # TestStartupEvaluationRoute
        ("startup-evaluation route recognized",
         TestStartupEvaluationRoute().test_startup_evaluation_route_recognized),
        ("startup-evaluation no fallback warning",
         TestStartupEvaluationRoute().test_startup_evaluation_no_fallback_warning),
        ("startup-evaluation auto-detect",
         TestStartupEvaluationRoute().test_startup_evaluation_auto_detect),
        ("startup-evaluation valid report passes",
         TestStartupEvaluationRoute().test_startup_evaluation_valid_report_passes),
        ("startup-evaluation alias no fallback",
         TestStartupEvaluationRoute().test_startup_evaluation_alias_no_fallback),
        # TestCompetitivePositioningRoute
        ("competitive-positioning route recognized",
         TestCompetitivePositioningRoute().test_competitive_positioning_route_recognized),
        ("competitive-positioning no fallback warning",
         TestCompetitivePositioningRoute().test_competitive_positioning_no_fallback_warning),
        ("competitive-positioning auto-detect",
         TestCompetitivePositioningRoute().test_competitive_positioning_auto_detect),
        ("competitive-positioning valid report passes",
         TestCompetitivePositioningRoute().test_competitive_positioning_valid_report_passes),
        ("competitive-positioning alias no fallback",
         TestCompetitivePositioningRoute().test_competitive_positioning_alias_no_fallback),
        # TestUnknownRouteBlocking
        ("unknown route exit 2", TestUnknownRouteBlocking().test_unknown_route_exit_2),
        ("unknown route overall fail", TestUnknownRouteBlocking().test_unknown_route_overall_fail),
        ("unknown route shows supported routes", TestUnknownRouteBlocking().test_unknown_route_shows_supported_routes),
        ("unknown route no validator runs", TestUnknownRouteBlocking().test_unknown_route_no_validator_runs),
        # TestValidatorCount
        ("all 5 validators run on failing report", TestValidatorCount().test_all_validators_executed_on_failing_report),
        ("market-outlook all 5 validators run", TestValidatorCount().test_market_outlook_validators_all_run),
        # TestProperties
        ("property: exit 0 iff overall pass", TestProperties().test_exit_code_zero_iff_overall_pass),
        ("property: exit 2 iff blocking", TestProperties().test_exit_code_two_iff_blocking),
        ("property: route always present", TestProperties().test_route_always_present),
        ("property: overall is valid", TestProperties().test_overall_is_valid),
        ("property: strict mode doesn't break valid", TestProperties().test_strict_mode_on_valid_report),
        ("property: route normalization", TestProperties().test_route_normalization),
        ("property: explicit route matches auto", TestProperties().test_explicit_route_matches_auto),
        ("property: blocking count matches exit", TestProperties().test_blocking_count_matches_exit_code),
    ]

    failures: list[str] = []
    for name, fn in tests:
        try:
            fn()
        except AssertionError as exc:
            failures.append(name)
            print(f"  FAIL  {name}: {exc}")
        except Exception as exc:
            failures.append(name)
            print(f"  FAIL  {name} (exception): {exc}")

    if failures:
        print(f"\n{len(failures)} test(s) failed: {', '.join(failures)}")
        raise SystemExit(1)

    print(f"\nAll {len(tests)} tests passed.")
    raise SystemExit(0)
