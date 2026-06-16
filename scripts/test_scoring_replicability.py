#!/usr/bin/env python3
"""
Tests for validate_scoring_replicability.py — scoring/ranking/probability
reproducibility validator for constrained-choice reports.

Pattern matches other test_*.py files in this project: inline fixtures,
self-contained test runner, no external dependencies.
"""

from __future__ import annotations

import sys
import tempfile
from collections.abc import Callable
from pathlib import Path

# ── The validator under test ──────────────────────────────────────────────

SCRIPT = str(Path(__file__).resolve().parent / "validate_scoring_replicability.py")

# We import validate_file directly for unit-level tests.
# Subprocess calls test the CLI entry point.
from validate_scoring_replicability import validate_file

# ── Fixture builders ──────────────────────────────────────────────────────


def _scoring_table_no_rules() -> str:
    """Report with a multi-dimension scoring table + final score but no
    scoring rules, no weights, no worked example.  Should fail."""
    return """\
# Programming Language Learning Value

## Route and audit status

**Primary route**: Constrained Choice / Shortlist

## 排名

| 排名 | 语言 | 市场需求 | 生态成熟度 | 学习回报 | 前景 | 广度 | **总分** |
|------|------|----------|------------|----------|------|------|----------|
| 🥇 | Python | A+ | A+ | A+ | A+ | A+ | 4.8/5 |
| 🥈 | Rust | B+ | B+ | B | A | B | 3.7/5 |
| 🥉 | Kotlin | B+ | B+ | A- | B+ | B+ | 3.6/5 |
| 4 | Swift | C+ | C+ | B- | C+ | C | 2.8/5 |
"""


def _probability_no_method() -> str:
    """Report with outcome probabilities but no method showing how evidence
    maps to those probabilities.  Should fail."""
    return """\
# Argentina vs Algeria World Cup Prediction

## Route and audit status

**Primary route**: Constrained Choice / Shortlist

## 胜率预测

| 结果 | 概率 |
|------|------|
| Argentina 胜 | 60% |
| 平局 | 25% |
| Algeria 胜 | 15% |

## 分析

Argentina 整体实力占优，近期状态良好。
"""


def _scoring_table_with_rules() -> str:
    """Report with scoring table + explicit rules + worked example.
    Should pass."""
    return """\
# Programming Language Learning Value

## Route and audit status

**Primary route**: Constrained Choice / Shortlist

## 评分规则

每个维度按以下规则映射到 5 分制：
- A+ = 5.0, A = 4.5, A- = 4.0
- B+ = 3.5, B = 3.0, B- = 2.5
- C+ = 2.0, C = 1.5, C- = 1.0
- D = 0.5

**权重**：市场需求 30%，生态成熟度 25%，学习回报 20%，前景 15%，广度 10%
(市场需求权重最高，因为直接影响就业机会)

**计算示例 (Python)**：
总分 = (5.0 × 0.30) + (5.0 × 0.25) + (5.0 × 0.20) + (5.0 × 0.15) + (5.0 × 0.10)
     = 1.50 + 1.25 + 1.00 + 0.75 + 0.50
     = 5.0 / 5

| 排名 | 语言 | 市场需求 | 生态成熟度 | 学习回报 | 前景 | 广度 | **总分** | 数字角色 |
|------|------|----------|------------|----------|------|------|----------|---------|
| 🥇 | Python | A+ (5.0) | A+ (5.0) | A+ (5.0) | A+ (5.0) | A+ (5.0) | 5.0/5 | model-output |
| 🥈 | Rust | B+ (3.5) | B+ (3.5) | B (3.0) | A (4.5) | B (3.0) | 3.5/5 | model-output |
"""


def _no_trigger_report() -> str:
    """Report with no scoring/ranking/probability trigger keywords.
    Should pass (skip)."""
    return """\
# Test Report

## Route and audit status

**Primary route**: Technical Deep-dive

## Findings

Python is a popular language [S01].
Rust is gaining traction in systems programming [S02].

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Example A | secondary | 2026-01-01 | https://example.com/a | medium | §3 |
"""


# ── Test helpers ──────────────────────────────────────────────────────────


def _run_validator(content: str) -> list[str]:
    """Run validate_file on inline fixture content and return errors."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", delete=False, encoding="utf-8",
    ) as f:
        f.write(content)
        tmp_path = f.name
    try:
        return validate_file(Path(tmp_path))
    finally:
        Path(tmp_path).unlink(missing_ok=True)


# ── Tests ─────────────────────────────────────────────────────────────────


class TestScoringTableNoRules:
    """A report with a scoring table and total scores but no rules must fail."""

    def test_returns_errors(self) -> None:
        errors = _run_validator(_scoring_table_no_rules())
        assert len(errors) > 0, (
            f"Expected blocking errors for scoring table without rules, "
            f"got empty list"
        )

    def test_error_mentions_replicability(self) -> None:
        errors = _run_validator(_scoring_table_no_rules())
        combined = " ".join(errors).lower()
        keywords = ["总分", "replicab", "scoring", "规则", "权重", "weight"]
        assert any(kw in combined for kw in keywords), (
            f"Error should mention replicability/scoring/rules/weights, "
            f"got:\n{errors}"
        )


class TestProbabilityNoMethod:
    """A report with outcome probabilities but no aggregation method must fail."""

    def test_returns_errors(self) -> None:
        errors = _run_validator(_probability_no_method())
        assert len(errors) > 0, (
            f"Expected blocking errors for probability without method, "
            f"got empty list"
        )

    def test_error_mentions_probability(self) -> None:
        errors = _run_validator(_probability_no_method())
        combined = " ".join(errors).lower()
        keywords = ["概率", "probab", "方法", "method", "复算", "reproduc"]
        assert any(kw in combined for kw in keywords), (
            f"Error should mention probability/method/reproducibility, "
            f"got:\n{errors}"
        )


class TestScoringTableWithRules:
    """A report with scoring table + rules + worked example must pass."""

    def test_returns_no_errors(self) -> None:
        errors = _run_validator(_scoring_table_with_rules())
        assert len(errors) == 0, (
            f"Expected no errors for scoring table with rules, "
            f"got:\n{errors}"
        )


class TestNoTriggerReport:
    """A report with no scoring/ranking/probability triggers must pass (skip)."""

    def test_returns_no_errors(self) -> None:
        errors = _run_validator(_no_trigger_report())
        assert len(errors) == 0, (
            f"Expected no errors for report without triggers, "
            f"got:\n{errors}"
        )


# ── Property-based tests ──────────────────────────────────────────────────


class TestProperties:
    """Invariant properties that must always hold."""

    # Property 1: validate_file always returns a list (never None)
    def test_always_returns_list(self) -> None:
        for fixture, label in [
            (_scoring_table_no_rules(), "no-rules"),
            (_probability_no_method(), "no-method"),
            (_scoring_table_with_rules(), "with-rules"),
            (_no_trigger_report(), "no-trigger"),
        ]:
            result = _run_validator(fixture)
            assert isinstance(result, list), (
                f"[{label}] Expected list, got {type(result).__name__}"
            )

    # Property 2: No false positives on non-scoring reports
    def test_no_false_positive_on_null_report(self) -> None:
        """A report with only narrative text must not trigger."""
        content = """\
# Just a Narrative

This is a plain description of various topics.
No tables, no scores, no rankings, no probabilities.
"""
        errors = _run_validator(content)
        assert len(errors) == 0, (
            f"Expected no errors on plain narrative, got:\n{errors}"
        )

    # Property 3: Missing file produces clear error
    def test_missing_file_error(self) -> None:
        from validate_scoring_replicability import validate_file as vf
        errors = vf(Path("/tmp/nonexistent_scoring_test_file.md"))
        assert len(errors) > 0, "Expected error for missing file"
        assert any("not found" in e.lower() or "exist" in e.lower() or "no such" in e.lower()
                   for e in errors), (
            f"Error should mention file not found, got:\n{errors}"
        )


# ── Self-contained runner ────────────────────────────────────────────────


if __name__ == "__main__":
    tests: list[tuple[str, Callable[[], None]]] = [
        # TestScoringTableNoRules
        ("scoring table no rules returns errors",
         TestScoringTableNoRules().test_returns_errors),
        ("scoring table no rules error mentions replicability",
         TestScoringTableNoRules().test_error_mentions_replicability),
        # TestProbabilityNoMethod
        ("probability no method returns errors",
         TestProbabilityNoMethod().test_returns_errors),
        ("probability no method error mentions probability",
         TestProbabilityNoMethod().test_error_mentions_probability),
        # TestScoringTableWithRules
        ("scoring table with rules returns no errors",
         TestScoringTableWithRules().test_returns_no_errors),
        # TestNoTriggerReport
        ("no trigger report returns no errors",
         TestNoTriggerReport().test_returns_no_errors),
        # TestProperties
        ("property: always returns list",
         TestProperties().test_always_returns_list),
        ("property: no false positive on null report",
         TestProperties().test_no_false_positive_on_null_report),
        ("property: missing file error",
         TestProperties().test_missing_file_error),
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
