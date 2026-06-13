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
    """Report claiming quantitative-role ✅ but body lacks roles -> warning."""

    def test_exit_code_warnings(self) -> None:
        result = _run_audit(_report_with_audit_mismatch())
        assert result.returncode == 1, (
            f"Expected exit 1 (warnings), got {result.returncode}\n"
            f"stdout:\n{result.stdout}"
        )

    def test_overall_conditional_pass(self) -> None:
        result = _run_audit(_report_with_audit_mismatch())
        assert _get_overall(result.stdout) == "conditional-pass"

    def test_warning_mentions_quantitative_role(self) -> None:
        result = _run_audit(_report_with_audit_mismatch())
        assert "quantitative-role" in result.stdout or "quantitative role" in result.stdout, (
            f"Expected quantitative-role warning, got:\n{result.stdout}"
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
        import tempfile
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
        ]:
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

    def test_all_four_validators_executed_on_failing_report(self) -> None:
        """A report that triggers issues in all validators should show all four."""
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
        result = _run_audit(content)
        expected_markers = [
            "[report-quality]",
            "[declared-execution]",
            "[table-role-labels]",
            "[source-label-consistency]",
        ]
        for marker in expected_markers:
            assert marker in result.stdout or marker in result.stderr, (
                f"Missing '{marker}' in output — validator may not have run\n"
                f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
            )


if __name__ == "__main__":
    import pytest
    raise SystemExit(pytest.main([__file__, "-v"]))
