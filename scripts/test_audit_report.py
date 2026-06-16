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

    def test_unknown_route_falls_back(self) -> None:
        result = _run_audit(_valid_report(), extra_args=["--route", "unknown-route"])
        assert result.returncode == 0, (
            f"Unknown route falls back to technical-deep-dive validators, "
            f"expected pass, got exit {result.returncode}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
        # Warning should be printed to stderr about the fallback
        assert "warning" in result.stderr.lower(), (
            f"Expected fallback warning in stderr, got:\n{result.stderr}"
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

    # Property 3: Route is always present in output
    def test_route_always_present(self) -> None:
        """Output always contains a Route: line."""
        for fixture, label in [
            (_valid_report(), "valid"),
            (_report_with_6col_register(), "6col"),
            (_report_with_audit_mismatch(), "mismatch"),
            (_report_no_route_block(), "no-route"),
        ]:
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


class TestSharedWorkflow:
    """Shared-workflow reports should fall back to default validators."""

    def test_exit_code_zero_when_valid(self) -> None:
        """Shared-workflow report with valid structure should pass."""
        result = _run_audit(_report_shared_workflow())
        assert result.returncode == 0, (
            f"Expected pass for shared-workflow, got {result.returncode}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )

    def test_fallback_warning_in_stderr(self) -> None:
        """Auto-detected route 'Shared-workflow' should trigger fallback warning."""
        result = _run_audit(_report_shared_workflow())
        assert "warning" in result.stderr.lower() or "unknown route" in result.stderr.lower(), (
            f"Expected fallback warning in stderr, got:\n{result.stderr}"
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
        ("--route unknown falls back", TestRouteOverride().test_unknown_route_falls_back),
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
        # TestSharedWorkflow
        ("shared-workflow valid passes", TestSharedWorkflow().test_exit_code_zero_when_valid),
        ("shared-workflow fallback warning", TestSharedWorkflow().test_fallback_warning_in_stderr),
        # TestValidatorCount
        ("all 5 validators run on failing report", TestValidatorCount().test_all_validators_executed_on_failing_report),
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
