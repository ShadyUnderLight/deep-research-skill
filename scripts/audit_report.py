#!/usr/bin/env python3
"""
Route-aware audit orchestrator for technical report delivery.

Wraps existing standalone validators into a single route-aware command
that produces a consolidated verdict (blocking / warnings / recommended
audit status) and a single exit code.

Usage:
    python3 scripts/audit_report.py path/to/report.md [--route ROUTE] [--strict]

Route auto-detection (from ## Route and audit status block) is the default;
pass --route to override or when no route block is present.

Exit codes:
    0 = all checks pass
    1 = warnings only (conditional pass)
    2 = one or more blocking errors
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass, field
from functools import partial
from pathlib import Path
from typing import Callable

# ── Import existing validators ──────────────────────────────────────────────

# validate_report_quality exposes public check_* functions that return
# structured list[str] errors/warnings — we use these directly rather than
# calling validate_file() which prints to stdout and returns only an exit code.
from validate_report_quality import (
    check_route_audit_block,
    check_route_declaration,
    check_audit_evidence,
    check_source_register_exists,
    check_source_register_columns,
    check_source_register_missing_ids,
    check_source_register_mapping,
    check_source_register_duplicate_ids,
    check_body_references,
    check_key_section_citation_coverage,
    check_audit_self_assessment_consistency,
    check_source_register_doi_coverage,
    check_strict_warnings,
    get_route_name,
    strip_fenced_code_blocks,
    ROUTE_AUDIT_HEADING,
)

from validate_declared_execution import validate_file as vde_validate_file
from validate_table_role_labels import validate_file as vtr_validate_file
from validate_source_label_consistency import validate_file as vsl_validate_file


# ── Exit codes ──────────────────────────────────────────────────────────────

EXIT_PASS = 0
EXIT_WARNINGS = 1
EXIT_BLOCKING = 2


# ── Types ───────────────────────────────────────────────────────────────────


@dataclass
class CheckResult:
    """Structured result from a single validator check."""

    name: str
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


ValidatorFn = Callable[..., CheckResult]


# ── Wrapper runners for each validator ─────────────────────────────────────


def _run_report_quality(path: Path, strict: bool = False) -> CheckResult:
    """Run validate_report_quality checks via public check_* functions."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except (OSError, UnicodeError) as exc:
        return CheckResult(
            name="report-quality",
            errors=[f"{path}: cannot read file — {exc}"],
        )

    cleaned = strip_fenced_code_blocks(text)
    errors: list[str] = []
    warnings: list[str] = []

    # 1. Route and audit status
    errors.extend(check_route_audit_block(cleaned))
    errors.extend(check_route_declaration(cleaned))
    errors.extend(check_audit_evidence(cleaned))

    # 2. Source Register
    errors.extend(check_source_register_exists(cleaned))
    errors.extend(check_source_register_columns(cleaned))
    errors.extend(check_source_register_missing_ids(cleaned))
    errors.extend(check_source_register_mapping(cleaned))
    errors.extend(check_source_register_duplicate_ids(cleaned))
    warnings.extend(check_source_register_doi_coverage(cleaned))

    # 3. Body references
    errors.extend(check_body_references(cleaned))

    # 4. Key section citation coverage (hard fail)
    errors.extend(check_key_section_citation_coverage(cleaned))

    # 5. Audit self-assessment consistency (warnings only)
    warnings.extend(check_audit_self_assessment_consistency(cleaned))

    # 6. Strict mode warnings
    if strict:
        warnings.extend(check_strict_warnings(cleaned))

    return CheckResult(name="report-quality", errors=errors, warnings=warnings)


def _run_declared_execution(path: Path) -> CheckResult:
    """Run validate_declared_execution checks."""
    try:
        errors, warnings = vde_validate_file(path)
    except Exception as exc:
        return CheckResult(
            name="declared-execution",
            errors=[f"declared-execution validator crashed: {exc}"],
        )
    return CheckResult(name="declared-execution", errors=errors, warnings=warnings)


def _run_table_role_labels(path: Path) -> CheckResult:
    """Run validate_table_role_labels checks."""
    try:
        errors = vtr_validate_file(path)
    except Exception as exc:
        return CheckResult(
            name="table-role-labels",
            errors=[f"table-role-labels validator crashed: {exc}"],
        )
    return CheckResult(name="table-role-labels", errors=errors, warnings=[])


def _run_source_label_consistency(path: Path) -> CheckResult:
    """Run validate_source_label_consistency checks."""
    try:
        errors = vsl_validate_file(path)
    except Exception as exc:
        return CheckResult(
            name="source-label-consistency",
            errors=[f"source-label-consistency validator crashed: {exc}"],
        )
    return CheckResult(name="source-label-consistency", errors=errors, warnings=[])


# ── Route → validator mapping ──────────────────────────────────────────────

ROUTE_VALIDATORS: dict[str, list[ValidatorFn]] = {
    "technical-deep-dive": [
        _run_report_quality,
        _run_declared_execution,
        _run_table_role_labels,
        _run_source_label_consistency,
    ],
}


def _auto_detect_route(path: Path) -> str | None:
    """Try to extract the primary route name from the report's audit block."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except (OSError, UnicodeError):
        return None
    cleaned = strip_fenced_code_blocks(text)
    return get_route_name(cleaned)


# ── Verdict computation ────────────────────────────────────────────────────


@dataclass
class AuditVerdict:
    """Consolidated verdict across all validators for a given route."""

    route: str | None
    overall: str  # "pass", "conditional-pass", "fail"
    blocking: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    recommended_audit_status: dict[str, str] = field(default_factory=dict)

    @property
    def exit_code(self) -> int:
        if self.blocking:
            return EXIT_BLOCKING
        if self.warnings:
            return EXIT_WARNINGS
        return EXIT_PASS


def _compute_verdict(
    route: str | None,
    results: list[CheckResult],
) -> AuditVerdict:
    """Aggregate check results into a single consolidated verdict."""
    blocking: list[str] = []
    warnings: list[str] = []
    status: dict[str, str] = {}

    for result in results:
        for err in result.errors:
            blocking.append(f"[{result.name}] {err}")
        for warn in result.warnings:
            warnings.append(f"[{result.name}] {warn}")

        # Determine per-validator status for recommended audit status
        if result.errors:
            status[result.name] = "fail"
        elif result.warnings:
            status[result.name] = "conditional-pass"
        else:
            status[result.name] = "pass"

    if blocking:
        overall = "fail"
    elif warnings:
        overall = "conditional-pass"
    else:
        overall = "pass"

    return AuditVerdict(
        route=route,
        overall=overall,
        blocking=blocking,
        warnings=warnings,
        recommended_audit_status=status,
    )


# ── Output formatting ──────────────────────────────────────────────────────


def format_verdict(verdict: AuditVerdict) -> str:
    """Render the consolidated verdict to a human-readable string."""
    lines: list[str] = []

    route_str = verdict.route or "(not detected)"
    lines.append(f"Route: {route_str}")
    lines.append(f"Overall: {verdict.overall}")
    lines.append("")

    if verdict.blocking:
        lines.append("Blocking:")
        for err in verdict.blocking:
            lines.append(f"- {err}")
        lines.append("")

    if verdict.warnings:
        lines.append("Warnings:")
        for warn in verdict.warnings:
            lines.append(f"  ⚠ {warn}")
        lines.append("")

    if verdict.recommended_audit_status:
        lines.append("Recommended audit status:")
        for audit_name, status in sorted(verdict.recommended_audit_status.items()):
            lines.append(f"- {audit_name}: {status}")
        lines.append("")

    return "\n".join(lines)


# ── Main ────────────────────────────────────────────────────────────────────


def audit_report(
    path: Path,
    route: str | None = None,
    strict: bool = False,
) -> AuditVerdict:
    """Run route-aware audit on a report and return the consolidated verdict.

    Parameters
    ----------
    path : Path
        Path to the Markdown report file.
    route : str | None
        Route name to select validators. If None, auto-detect from the report.
        Falls back to 'technical-deep-dive' when auto-detection fails and no
        route is specified.
    strict : bool
        Enable strict mode warnings (additional route-specific checks).

    Returns
    -------
    AuditVerdict
        Consolidated verdict with blocking errors, warnings, and recommended
        audit status.
    """
    if not path.is_file():
        return AuditVerdict(
            route=route,
            overall="fail",
            blocking=[f"{path}: not a regular file"],
        )

    # Auto-detect route if not specified
    resolved_route = route
    if resolved_route is None:
        detected = _auto_detect_route(path)
        if detected is not None:
            resolved_route = detected
        else:
            # Fall back to technical-deep-dive when no route detected
            resolved_route = "technical-deep-dive"

    # Look up validators for the resolved route
    validators = ROUTE_VALIDATORS.get(resolved_route)
    if validators is None:
        # Unknown route — fall back to technical-deep-dive validators
        validators = ROUTE_VALIDATORS.get("technical-deep-dive", [])

    # Run each validator
    results: list[CheckResult] = []
    for validator in validators:
        if validator is _run_report_quality:
            result = _run_report_quality(path, strict=strict)
        else:
            result = validator(path)
        results.append(result)

    return _compute_verdict(resolved_route, results)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Route-aware audit orchestrator for technical reports.",
    )
    parser.add_argument("path", type=str, help="Path to the Markdown report file")
    parser.add_argument(
        "--route",
        type=str,
        default=None,
        help=(
            "Route name (e.g., technical-deep-dive). "
            "Auto-detected from report if omitted."
        ),
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Enable strict mode warnings",
    )
    args = parser.parse_args(argv)

    path = Path(args.path)
    verdict = audit_report(path, route=args.route, strict=args.strict)

    output = format_verdict(verdict)
    print(output)

    return verdict.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
