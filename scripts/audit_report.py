#!/usr/bin/env python3
"""
Route-aware audit orchestrator for technical report delivery.

Wraps existing standalone validators into a single route-aware command
that produces a consolidated verdict (blocking / warnings / recommended
audit status) and a single exit code.

Usage:
    python3 scripts/audit_report.py path/to/report.md [--route ROUTE] [--strict]
        [--activation-snapshot path/to/activation.json]

Route auto-detection (from ## Route and audit status block) is the default;
pass --route to override or when no route block is present.

Exit codes:
    0 = all checks pass
    1 = warnings only (conditional pass)
    2 = one or more blocking errors
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass, field
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
    check_audit_evidence_section_refs,
    check_source_register_exists,
    check_source_register_columns,
    check_source_register_missing_ids,
    check_source_register_mapping,
    check_source_register_duplicate_ids,
    check_source_register_doi_coverage,
    check_source_register_placeholders,
    check_body_references,
    check_key_section_citation_coverage,
    check_audit_self_assessment_consistency,
    check_academic_register_columns,
    check_strict_warnings,
    get_route_name,
)

from validate_declared_execution import validate_file as vde_validate_file
from validate_table_role_labels import validate_file as vtr_validate_file
from validate_source_label_consistency import validate_file as vsl_validate_file
from validate_listed_company_delivery import validate_file as vlc_validate_file
from validate_scoring_replicability import validate_file as vsr_validate_file
from validate_contract import (
    extract_contract_blocks,
    extract_contract_from_markdown,
    extract_report_primary_route,
    has_contract_block,
    validate_contract,
)
from validate_contract import (
    _extract_pack_artifact_id as vc_extract_pack_artifact_id,
    _resolve_pack_primary_route as vc_resolve_pack_primary_route,
    _strip_fences as vc_strip_fences,
    count_report_route_blocks as vc_count_report_route_blocks,
    extract_report_route_declaration as vc_extract_report_route_declaration,
    validate_pack_sections as vc_validate_pack_sections,
)

# Validators executed only through required-audit bindings (issue #378).
from validate_markdown_delivery import validate_markdown_delivery as vmd_validate
from validate_forward_looking_labels import validate_file as vfl_validate_file
from validate_research_pack import (
    find_missing_headings as vrp_find_missing_headings,
    run_strict_checks as vrp_run_strict_checks,
    strip_fenced_code_blocks as vrp_strip_fenced_code_blocks,
)
from audit_evidence import validate_evidence_reference
from activation_snapshot import (
    ActivationSnapshotError,
    extract_activation_snapshot_reference,
    load_activation_snapshot,
)

# ── Runtime control-plane registry (issue #374) ─────────────────────────────
# Route identity, aliases and validator dispatch bindings come from
# schemas/route-manifest.json via registry_loader.  Unknown routes and
# unknown bindings fail closed at runtime.  Audit identity and required-audit
# bindings come from schemas/audit-registry.json (issue #378).
import registry_loader
from registry_loader import RegistryError, UnknownRouteError

_ROUTE_REGISTRY = registry_loader.load_route_registry()
_AUDIT_REGISTRY = registry_loader.load_audit_registry()

# Audits executed for every route in addition to route.required_audits.
# These are delivery-scope pipeline validators (markdown-delivery,
# research-pack), registered as first-class entries in
# schemas/audit-registry.json with scope: "delivery" (issue #393).  The
# global audit set is derived from the registry via global_audit_ids() —
# there is no second, hardcoded audit identity in code.  research-pack is
# skipped outside strict mode when no --research-pack is given (and a
# not_run + blocking error under --strict); markdown-delivery always runs
# against the report itself.


# ── Exit codes ──────────────────────────────────────────────────────────────

EXIT_PASS = 0
EXIT_WARNINGS = 1
EXIT_BLOCKING = 2

# Version of the machine-readable audit JSON contract (issue #393).  The
# forward runner pins the same value (EXPECTED_AUDIT_JSON_SCHEMA_VERSION) and
# fails closed when it does not match.  Bump only on breaking JSON field
# changes; additive fields do not require a bump.
AUDIT_JSON_SCHEMA_VERSION = 1


# ── Types ───────────────────────────────────────────────────────────────────


@dataclass
class CheckResult:
    """Structured result from a single validator check."""

    name: str
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


ValidatorFn = Callable[..., CheckResult]


# ── Route name normalization ────────────────────────────────────────────────

# Default route used when auto-detection fails (no route declared in report).
# Unknown routes that are explicitly named but unsupported are now a blocking
# error (exit 2) — they do NOT fall back to this default.
_DEFAULT_ROUTE = "technical-deep-dive"

# The default route must always be a canonical manifest route id.
if _DEFAULT_ROUTE not in _ROUTE_REGISTRY.route_ids():
    raise RegistryError(
        f"_DEFAULT_ROUTE '{_DEFAULT_ROUTE}' is not a canonical route id "
        f"in schemas/route-manifest.json"
    )

# Minimum number of fully-defined monitoring signals required for
# market-outlook reports to pass the actionability gate.
MIN_MONITORING_SIGNALS = 3


def _normalize_route(name: str) -> str:
    """Resolve a display route name to a canonical key.

    Alias resolution now comes from the route manifest via
    registry_loader: lowercase + whitespace collapse, alias lookup,
    parenthetical-note stripping, then a space→hyphen fallback against
    canonical route ids.  Raises UnknownRouteError for unresolvable
    names — callers must treat that as a blocking error.
    """
    return _ROUTE_REGISTRY.resolve_route(name)


# ── Wrapper runners for each validator ─────────────────────────────────────

# Each _run_* function accepts ``**kwargs`` so that the dispatch loop
# can pass shared flags (e.g. ``strict``) uniformly.  Validators that
# do not use a particular flag simply ignore it.


def _run_report_quality(path: Path, **kwargs: bool) -> CheckResult:
    """Run validate_report_quality checks via public check_* functions.

    Accepts ``strict`` keyword (default ``False``) to enable additional
    route-specific warnings.

    Crash isolation: each check_* call is individually wrapped so that
    a crash in one does not silently discard the results of others.
    """
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except (OSError, UnicodeError) as exc:
        return CheckResult(
            name="report-quality",
            errors=[f"{path}: cannot read file — {exc}"],
        )

    cleaned = vc_strip_fences(text)
    errors: list[str] = []
    warnings: list[str] = []

    def _run(func, *a, **kw):  # local helper for crash isolation
        try:
            return func(*a, **kw)
        except Exception as exc:
            return [f"{func.__name__} crashed: {exc}"]

    # 1. Route and audit status
    errors.extend(_run(check_route_audit_block, cleaned))
    errors.extend(_run(check_route_declaration, cleaned))
    errors.extend(_run(check_audit_evidence, cleaned))
    errors.extend(_run(check_audit_evidence_section_refs, cleaned))

    # 2. Source Register
    errors.extend(_run(check_source_register_exists, cleaned))
    errors.extend(_run(check_source_register_columns, cleaned))
    errors.extend(_run(check_source_register_missing_ids, cleaned))
    errors.extend(_run(check_source_register_mapping, cleaned))
    errors.extend(_run(check_source_register_duplicate_ids, cleaned))
    warnings.extend(_run(check_source_register_doi_coverage, cleaned))
    warnings.extend(_run(check_source_register_placeholders, cleaned))

    # 3. Body references
    errors.extend(_run(check_body_references, cleaned))

    # 4. Key section citation coverage (hard fail)
    errors.extend(_run(check_key_section_citation_coverage, cleaned))

    # 5. Audit self-assessment consistency (hard-fail gate)
    errors.extend(_run(check_audit_self_assessment_consistency, cleaned))

    # 6. Academic route checks
    errors.extend(_run(check_academic_register_columns, cleaned))

    # 7. Strict mode warnings
    strict = kwargs.get("strict", False)
    if strict:
        warnings.extend(_run(check_strict_warnings, cleaned))

    return CheckResult(name="report-quality", errors=errors, warnings=warnings)


def _run_declared_execution(path: Path, **kwargs: bool) -> CheckResult:
    """Run validate_declared_execution checks."""
    try:
        errors, warnings = vde_validate_file(path)
    except Exception as exc:
        return CheckResult(
            name="declared-execution",
            errors=[f"declared-execution validator crashed: {exc}"],
        )
    return CheckResult(name="declared-execution", errors=errors, warnings=warnings)


def _run_table_role_labels(path: Path, **kwargs: bool) -> CheckResult:
    """Run validate_table_role_labels checks."""
    try:
        errors = vtr_validate_file(path)
    except Exception as exc:
        return CheckResult(
            name="table-role-labels",
            errors=[f"table-role-labels validator crashed: {exc}"],
        )
    return CheckResult(name="table-role-labels", errors=errors, warnings=[])


def _run_source_label_consistency(path: Path, **kwargs: bool) -> CheckResult:
    """Run validate_source_label_consistency checks."""
    try:
        errors = vsl_validate_file(path)
    except Exception as exc:
        return CheckResult(
            name="source-label-consistency",
            errors=[f"source-label-consistency validator crashed: {exc}"],
        )
    return CheckResult(name="source-label-consistency", errors=errors, warnings=[])


def _run_listed_company_delivery(path: Path, **kwargs: bool) -> CheckResult:
    """Run validate_listed_company_delivery checks."""
    try:
        errors, warnings = vlc_validate_file(path)
    except Exception as exc:
        return CheckResult(
            name="listed-company-delivery",
            errors=[f"listed-company-delivery validator crashed: {exc}"],
        )
    return CheckResult(
        name="listed-company-delivery", errors=errors, warnings=warnings
    )


def _run_scoring_replicability(path: Path, **kwargs: bool) -> CheckResult:
    """Run validate_scoring_replicability checks."""
    try:
        errors = vsr_validate_file(path)
    except Exception as exc:
        return CheckResult(
            name="scoring-replicability",
            errors=[f"scoring-replicability validator crashed: {exc}"],
        )
    return CheckResult(name="scoring-replicability", errors=errors, warnings=[])


def _run_market_outlook_monitoring_actionability(
    path: Path, **kwargs: bool
) -> CheckResult:
    """Validate ≥3 fully-defined monitoring signals with actionability fields.

    Scans monitoring-related sections for tables containing all four
    actionability columns: threshold, cadence, source, and trigger-to-action.
    Each data row with all four fields populated counts as one fully-defined
    signal.  Fewer than 3 such signals is a blocking error.

    Accepts ``strict`` keyword to enable warnings for partially-defined
    signals.
    """
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except (OSError, UnicodeError) as exc:
        return CheckResult(
            name="market-outlook-monitoring",
            errors=[f"{path}: cannot read file — {exc}"],
        )

    # Shared declaration sanitizer: sections inside ```fences or <!-- -->
    # are not rendered content and must not count as monitoring signals
    # (issue #378).
    text = vc_strip_fences(text)

    # ── Split into sections by heading level (## or ###) ──────────────────
    lines = text.split("\n")
    sections: list[tuple[str, list[str]]] = []
    current_heading: str | None = None
    current_body: list[str] = []

    for line in lines:
        m = re.match(r"^#{2,3}\s+(.+)$", line)
        if m:
            if current_heading is not None:
                sections.append((current_heading, current_body))
            current_heading = m.group(1).strip()
            current_body = []
        else:
            current_body.append(line)
    if current_heading is not None:
        sections.append((current_heading, current_body))

    # Find monitoring-related sections
    monitoring_sections = [
        (h, b) for h, b in sections
        if "monitoring" in h.lower() or "监测" in h
    ]

    if not monitoring_sections:
        return CheckResult(
            name="market-outlook-monitoring",
            errors=[
                "No monitoring section found — market-outlook report must "
                "include monitoring signals with actionable fields "
                "(threshold, cadence, source, trigger-to-action)"
            ],
        )

    # ── Actionability field keyword sets ──────────────────────────────────
    FIELD_KEYWORDS: dict[str, set[str]] = {
        "threshold": {"threshold", "阈值"},
        "cadence": {"cadence", "frequency", "频率"},
        "source": {"source", "来源"},
        "trigger_to_action": {"trigger", "action", "应对"},
    }

    def _map_table_header(header_line: str) -> dict[str, int]:
        """Match markdown table header columns to actionability fields.

        Returns a dict {field_name: column_index}.  Columns are matched
        in priority order (threshold → cadence → source → trigger_to_action);
        each column can match at most one field.
        """
        # Split and drop leading/trailing artifacts from | markers
        raw = header_line.split("|")
        cols = [c.strip().lower() for c in raw[1:-1]]
        mapping: dict[str, int] = {}
        used: set[int] = set()

        for field, keywords in FIELD_KEYWORDS.items():
            for i, col in enumerate(cols):
                if i in used:
                    continue
                if any(kw in col for kw in keywords):
                    mapping[field] = i
                    used.add(i)
                    break

        return mapping

    # ── Parse tables within monitoring sections ────────────────────────────
    fully_defined = 0
    partial_signals: list[str] = []

    for _heading, body_lines in monitoring_sections:
        i = 0
        while i < len(body_lines):
            line = body_lines[i].strip()
            if line.startswith("|") and not line.startswith("|--"):
                header_line = line
                i += 1
                # Skip separator row (|--|--|...|)
                if i < len(body_lines) and body_lines[i].strip().startswith("|") and "---" in body_lines[i]:
                    i += 1
                else:
                    continue

                col_map = _map_table_header(header_line)
                if len(col_map) < 4:
                    # Table does not have all 4 actionability columns; skip
                    while i < len(body_lines) and body_lines[i].strip().startswith("|"):
                        i += 1
                    continue

                # Parse data rows
                while i < len(body_lines) and body_lines[i].strip().startswith("|"):
                    row = body_lines[i].strip()
                    # Keep empty cells to preserve column index alignment
                    raw_cells = row.split("|")
                    cells = [c.strip() for c in raw_cells[1:-1]]
                    all_filled = True
                    missing_fields: list[str] = []
                    for field, col_idx in col_map.items():
                        if col_idx >= len(cells) or not cells[col_idx]:
                            all_filled = False
                            missing_fields.append(field)
                    if all_filled:
                        fully_defined += 1
                    else:
                        signal_name = cells[0] if cells else "(unknown)"
                        partial_signals.append(
                            f"Signal '{signal_name}' missing: "
                            f"{', '.join(missing_fields)}"
                        )
                    i += 1
            else:
                i += 1

    # ── Compute verdict ────────────────────────────────────────────────────
    errors: list[str] = []
    warnings: list[str] = []

    if fully_defined < MIN_MONITORING_SIGNALS:
        errors.append(
            f"Only {fully_defined} fully-defined monitoring signal(s) "
            f"found; need ≥{MIN_MONITORING_SIGNALS} with all four "
            f"actionability fields (threshold, cadence, source, "
            f"trigger-to-action)"
        )

    strict = kwargs.get("strict", False)
    if strict and partial_signals:
        warnings.append(
            f"{len(partial_signals)} partially-defined monitoring signal(s):"
        )
        warnings.extend(f"  {s}" for s in partial_signals)

    return CheckResult(
        name="market-outlook-monitoring",
        errors=errors,
        warnings=warnings,
    )


def _run_secondary_route_check(path: Path, **kwargs: bool) -> CheckResult:
    """Check that declared secondary routes are supported.

    Scans the Route and audit status block for secondary/auxiliary route
    declarations.  If an unsupported secondary route is found, produces a
    warning (not blocking).  Silence means either no secondary routes
    declared or all are supported.
    """
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except (OSError, UnicodeError) as exc:
        return CheckResult(
            name="secondary-route-check",
            errors=[f"{path}: cannot read file — {exc}"],
        )
    cleaned = vc_strip_fences(text)

    # Locate the Route and audit status block — use same patterns as
    # validate_report_quality.ROUTE_AUDIT_HEADING for consistency.
    block_start = -1
    lines = cleaned.split("\n")
    for i, line in enumerate(lines):
        if re.match(
            r"^#{2,3}\s+.*(?:Route\s+and\s+audit\s+status|路由与审计状态)",
            line,
            re.IGNORECASE,
        ):
            block_start = i
            break
    if block_start < 0:
        # No route block — nothing to check
        return CheckResult(name="secondary-route-check", errors=[], warnings=[])

    # Extract block text (until next ## heading or end)
    block_lines: list[str] = []
    for line in lines[block_start + 1:]:
        if re.match(r"^#{2,3}\s", line):
            break
        block_lines.append(line)
    block_text = "\n".join(block_lines)

    # Search for secondary route declarations
    secondary_patterns = [
        r"\*\*[Ss]econdary\s+[Rr]outes?\*\*\s*[:\s]+\s*(.+)",
        r"\*\*[Aa]dditional\s+[Rr]outes?\*\*\s*[:\s]+\s*(.+)",
        r"\*\*辅助路由\*\*\s*[:\s]+\s*(.+)",
        r"\*\*次级路由\*\*\s*[:\s]+\s*(.+)",
        r"\*\*次要路由\*\*\s*[:\s]+\s*(.+)",
    ]

    warnings: list[str] = []
    for pattern in secondary_patterns:
        m = re.search(pattern, block_text)
        if m:
            raw_routes = m.group(1).strip().rstrip(".")
            # Split on common delimiters: comma, /, 、,  or "and"
            parts = re.split(r"\s*[,/、，]\s*|\s+and\s+|\s+和\s+|\s+与\s+", raw_routes)
            for part in parts:
                part = part.strip().rstrip(".")
                if not part:
                    continue
                try:
                    canon = _normalize_route(part)
                except UnknownRouteError:
                    warnings.append(
                        f"Declared secondary route '{part}' "
                        f"is not a supported route"
                    )
                    continue
                if canon not in _ROUTE_REGISTRY.route_ids():
                    warnings.append(
                        f"Declared secondary route '{part}' "
                        f"is not a supported route"
                    )
                # Even if supported, note that secondary route hard-fail
                # is not independently verified (per ROUTING-MATRIX.md).
            break  # Only process the first match

    return CheckResult(name="secondary-route-check", errors=[], warnings=warnings)


def _run_contract_check(path: Path, **kwargs: bool) -> CheckResult:
    """Validate route activation contract if present in the report.

    When a ```contract fenced block is found, runs full validation
    (route/discipline separation, boundary judgment, secondary hard-fail
    tracking, audit evidence, registry wiring, status-block route
    consistency, artifact identity).

    When no contract block is present:
    - With require_contract=True → blocking error.
    - With require_contract=False → silent skip (migration opt-out
      for reports that haven't yet adopted the contract format).
    """
    require_contract = kwargs.get("require_contract", False)
    strict = kwargs.get("strict", False)
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except (OSError, UnicodeError) as exc:
        return CheckResult(
            name="contract-check",
            errors=[f"{path}: cannot read file — {exc}"],
        )
    visible_text = vc_strip_fences(text)

    activation_snapshot_path = kwargs.get("activation_snapshot")
    activation_data: dict | None = None
    if activation_snapshot_path is not None:
        try:
            activation_data = load_activation_snapshot(Path(activation_snapshot_path))
        except ActivationSnapshotError as exc:
            return CheckResult(
                name="activation-record-integration",
                errors=[str(exc)],
            )

    # Cardinality checks on user-writable declarations (issue #378): more
    # than one contract block / route status block is structural
    # malformation — a second declaration could carry a conflicting route
    # or a broken payload, so fail closed instead of accepting the first.
    contract_blocks, contract_errors = extract_contract_blocks(text)
    if contract_errors:
        return CheckResult(name="contract-check", errors=contract_errors)
    route_block_count = vc_count_report_route_blocks(text)
    if route_block_count > 1:
        return CheckResult(
            name="contract-check",
            errors=[
                f"multiple 'Route and audit status' blocks found "
                f"({route_block_count}) — exactly one is required "
                "(issue #378)"
            ],
        )

    research_pack = kwargs.get("research_pack")
    pack_activation_snapshot: dict | None = None
    if research_pack is not None:
        pack_section_errors = vc_validate_pack_sections(str(research_pack))
        if pack_section_errors:
            return CheckResult(name="contract-check", errors=pack_section_errors)
        try:
            pack_text = Path(research_pack).read_text(
                encoding="utf-8", errors="replace"
            )
            pack_activation_snapshot, activation_errors = (
                extract_activation_snapshot_reference(
                    vc_strip_fences(pack_text), label="Research Pack"
                )
            )
        except (OSError, UnicodeError) as exc:
            return CheckResult(
                name="activation-record-integration",
                errors=[f"cannot read Research Pack activation snapshot: {exc}"],
            )
        if activation_errors:
            return CheckResult(
                name="activation-record-integration",
                errors=activation_errors,
            )

    report_route, route_malformed = vc_extract_report_route_declaration(text)
    if route_malformed:
        return CheckResult(name="contract-check", errors=route_malformed)

    contract = contract_blocks[0] if contract_blocks else None
    if contract is None:
        if has_contract_block(text):
            # A ```contract fenced block exists but the JSON is malformed
            # or not a dict — this is a broken contract, not a missing one.
            return CheckResult(
                name="contract-check",
                errors=[
                    "Route activation contract block found but JSON is malformed "
                    "or not a valid object. Fix the ```contract fenced block "
                    "or remove it if not needed."
                ],
            )
        # No contract block at all.
        if require_contract or activation_data is not None:
            return CheckResult(
                name="contract-check",
                errors=[
                    "No route activation contract found in report "
                    "(--require-contract is set)."
                ],
            )
        # Migration opt-out: silently skip for reports without contracts.
        return CheckResult(name="contract-check", errors=[], warnings=[])

    result = validate_contract(
        contract,
        report_primary_route=report_route,
        pack_activation_snapshot=pack_activation_snapshot,
        activation_snapshot=activation_data,
        require_activation_snapshot=activation_data is not None,
        strict=strict,
        report_text=visible_text,
        evidence_base_dir=Path(__file__).resolve().parent.parent,
        known_validator_bindings=_registered_validator_bindings(),
    )
    if result.errors:
        return CheckResult(
            name="contract-check",
            errors=[
                f"Route activation contract is invalid ({len(result.errors)} error(s))",
                *(f"  {e}" for e in result.errors[:5]),  # cap at 5 for readability
            ],
            warnings=[w for w in result.warnings],
        )
    # Cross-check the Research Pack against the contract (issue #378 scope 4:
    # report/pack/contract route and artifact identity must agree).  The
    # pack checks run inside the contract validator so the same evidence
    # chain (contract → pack) is verified in one command.
    research_pack = kwargs.get("research_pack")
    if research_pack is not None and (result.is_valid or strict):
        pack_primary = vc_resolve_pack_primary_route(str(research_pack))
        pack_artifact = vc_extract_pack_artifact_id(str(research_pack))
        if pack_primary is None:
            # Matches the standalone validator's fail-closed behavior: a
            # pack whose '## Primary route' cannot be resolved is an error,
            # not a silent skip (issue #378 scope 4).
            return CheckResult(
                name="contract-check",
                errors=[
                    f"Research Pack {research_pack} '## Primary route' "
                    "cannot be resolved to a canonical route — fix the "
                    "pack declaration or drop --research-pack"
                ],
            )
        cross = validate_contract(
            contract,
            pack_primary_route=pack_primary,
            pack_artifact_id=pack_artifact,
            pack_activation_snapshot=pack_activation_snapshot,
            activation_snapshot=activation_data,
            require_activation_snapshot=activation_data is not None,
            research_pack_provided=True,
            strict=strict,
            report_text=visible_text,
            evidence_base_dir=Path(__file__).resolve().parent.parent,
            known_validator_bindings=_registered_validator_bindings(),
        )
        if cross.errors:
            return CheckResult(
                name="contract-check",
                errors=[
                    "Research Pack / contract cross-check failed "
                    f"({len(cross.errors)} error(s))",
                    *(f"  {e}" for e in cross.errors[:5]),
                ],
                warnings=[w for w in cross.warnings],
            )
        if cross.warnings:
            return CheckResult(
                name="contract-check",
                errors=[],
                warnings=[w for w in cross.warnings],
            )
    if result.warnings:
        return CheckResult(
            name="contract-check",
            errors=[],
            warnings=[w for w in result.warnings],
        )
    return CheckResult(name="contract-check", errors=[], warnings=[])


# ── Required-audit validators (issue #378) ───────────────────────────────────
# These wrappers execute audits bound via schemas/audit-registry.json
# validator_binding, not via route validator_bindings.


def _run_markdown_delivery(path: Path, **kwargs: bool) -> CheckResult:
    """Run validate_markdown_delivery structural checks on the report."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except (OSError, UnicodeError) as exc:
        return CheckResult(
            name="markdown-delivery",
            errors=[f"{path}: cannot read file — {exc}"],
        )
    result = vmd_validate(text)
    return CheckResult(
        name="markdown-delivery", errors=list(result.errors), warnings=list(result.warnings)
    )


def _run_forward_looking(path: Path, **kwargs: bool) -> CheckResult:
    """Run validate_forward_looking_labels on the report.

    The validator flags numeric claims that carry a confirmed label; each
    hit is a blocking error (mislabeled forward-looking claim).
    """
    try:
        hits = vfl_validate_file(path)
    except Exception as exc:
        return CheckResult(
            name="forward-looking-claims",
            errors=[f"forward-looking-claims validator crashed: {exc}"],
        )
    return CheckResult(name="forward-looking-claims", errors=list(hits), warnings=[])


def _run_research_pack(pack_path: Path | None, **kwargs: bool) -> CheckResult:
    """Validate a Research Pack file (issue #378).

    Structural headings always run; semantic strict checks run too because
    a pack provided to a strict audit must be deliverable.  Returns a
    CheckResult whose name is the audit id 'research-pack'.
    """
    if pack_path is None:
        return CheckResult(name="research-pack", errors=[], warnings=[])
    try:
        text = pack_path.read_text(encoding="utf-8", errors="replace")
    except (OSError, UnicodeError) as exc:
        return CheckResult(
            name="research-pack",
            errors=[f"{pack_path}: cannot read pack file — {exc}"],
        )
    cleaned = vrp_strip_fenced_code_blocks(text)
    errors: list[str] = []
    missing = vrp_find_missing_headings(cleaned)
    errors.extend(f"pack missing required heading: {h}" for h in missing)
    try:
        report_path = kwargs.get("report_path")
        report_text: str | None = None
        if isinstance(report_path, Path) and report_path.is_file():
            report_text = vc_strip_fences(
                report_path.read_text(encoding="utf-8", errors="replace")
            )
        errors.extend(
            vrp_run_strict_checks(
                cleaned,
                artifact_text=cleaned,
                evidence_base_dir=Path(__file__).resolve().parent.parent,
                report_text=report_text,
                known_validator_bindings=_registered_validator_bindings(),
            )
        )
    except Exception as exc:
        errors.append(f"research-pack strict checks crashed: {exc}")
    return CheckResult(name="research-pack", errors=errors, warnings=[])


# ── Validator registry and dispatch ─────────────────────────────────────────
# Route → validator bindings come from schemas/route-manifest.json
# (validator_bindings per route).  This dict maps stable binding ids to
# the actual validator functions; _dispatch_validators resolves a route
# through the manifest and fails closed on unknown bindings.

_VALIDATOR_REGISTRY: dict[str, ValidatorFn] = {
    "report-quality": _run_report_quality,
    "declared-execution": _run_declared_execution,
    "table-role-labels": _run_table_role_labels,
    "source-label-consistency": _run_source_label_consistency,
    "listed-company-delivery": _run_listed_company_delivery,
    "scoring-replicability": _run_scoring_replicability,
    "market-outlook-monitoring-actionability": _run_market_outlook_monitoring_actionability,
    "secondary-route-check": _run_secondary_route_check,
    "contract-check": _run_contract_check,
}

# The runtime registry must stay in sync with the loader's canonical set —
# otherwise a binding id the manifest is allowed to use has no function here.
_missing_functions = registry_loader.KNOWN_VALIDATOR_IDS - set(_VALIDATOR_REGISTRY)
_unregistered_ids = set(_VALIDATOR_REGISTRY) - registry_loader.KNOWN_VALIDATOR_IDS
if _missing_functions or _unregistered_ids:
    raise RegistryError(
        "_VALIDATOR_REGISTRY and registry_loader.KNOWN_VALIDATOR_IDS are "
        f"out of sync (registry ids without functions: "
        f"{sorted(_missing_functions)}; functions without registry ids: "
        f"{sorted(_unregistered_ids)})"
    )

# ── Audit-level validator registry (issue #378) ─────────────────────────────
# Executes automated audits bound via audit-registry.json validator_binding.
# An audit may also bind to a route validator id (e.g. source-traceability
# → source-label-consistency), which is resolved through _VALIDATOR_REGISTRY.

_AUDIT_VALIDATOR_REGISTRY: dict[str, ValidatorFn] = {
    "markdown-delivery": _run_markdown_delivery,
    "research-pack": _run_research_pack,
    "forward-looking-claims": _run_forward_looking,
}

_missing_audit_fns = registry_loader.AUDIT_VALIDATOR_IDS - set(_AUDIT_VALIDATOR_REGISTRY)
_unregistered_audit_ids = set(_AUDIT_VALIDATOR_REGISTRY) - registry_loader.AUDIT_VALIDATOR_IDS
if _missing_audit_fns or _unregistered_audit_ids:
    raise RegistryError(
        "_AUDIT_VALIDATOR_REGISTRY and registry_loader.AUDIT_VALIDATOR_IDS "
        f"are out of sync (audit validator ids without functions: "
        f"{sorted(_missing_audit_fns)}; functions without audit ids: "
        f"{sorted(_unregistered_audit_ids)})"
    )


def _dispatch_validators(route_id: str) -> list[ValidatorFn]:
    """Resolve manifest validator bindings for a route to functions.

    Raises UnknownRouteError if the route id is not canonical; raises
    RegistryError if the manifest binds a validator id that has no
    registered function (manifest/code drift — must fail closed).
    """
    bindings = _ROUTE_REGISTRY.validators_for(route_id)
    validators: list[ValidatorFn] = []
    for binding in bindings:
        fn = _VALIDATOR_REGISTRY.get(binding)
        if fn is None:
            raise RegistryError(
                f"Route '{route_id}' binds unknown validator '{binding}' — "
                f"schemas/route-manifest.json and audit_report.py "
                f"_VALIDATOR_REGISTRY are out of sync"
            )
        validators.append(fn)
    return validators


def _auto_detect_route(path: Path) -> str | None:
    """Try to extract the raw primary route name from the report's audit block.

    Returns the raw declared name (not normalized) or None when no route is
    declared.  The caller is responsible for resolving/normalizing the name,
    so an unknown declared route flows through the unified blocking path in
    audit_report() instead of raising here.
    """
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except (OSError, UnicodeError):
        return None
    cleaned = vc_strip_fences(text)
    raw = get_route_name(cleaned)
    if raw is None or not raw.strip():
        return None
    return raw.strip()


# ── Verdict computation ────────────────────────────────────────────────────


@dataclass
class AuditResult:
    """Structured result for a single required audit (issue #378).

    status is one of: pass | conditional-pass | fail | not_run | skipped |
    partial.  ``not_run``/``skipped`` mean the audit did not execute and
    must never aggregate to a Pass verdict. execution_source distinguishes
    automated validator output, manual checklist attestation, process-node
    evidence, and legacy self-attestation (issue #390).
    """

    audit_id: str
    execution_type: str  # automated | manual | process
    status: str
    execution_source: str | None = None
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)
    evidence_provenance: list[dict[str, object]] = field(default_factory=list)
    validator_binding: str | None = None
    reason: str | None = None


@dataclass
class ValidatorResult:
    """Structured result for a single route-level validator (issue #393).

    Route-level validators (report-quality, declared-execution, ...) are the
    dispatch chain resolved from schemas/route-manifest.json.  Each must
    appear in the JSON verdict with its own status, evidence and provenance;
    a dispatched validator with no recorded result is ``incomplete`` and must
    never aggregate to a Pass (fail-closed).
    """

    validator_id: str
    status: str  # pass | conditional-pass | fail | incomplete | not_run
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)
    execution_source: str = "automated_validator"
    validator_version: str | None = None
    reason: str | None = None


@dataclass
class AuditVerdict:
    """Consolidated verdict across all validators for a given route."""

    route: str | None
    overall: str  # "pass", "conditional-pass", "fail"
    blocking: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    recommended_audit_status: dict[str, str] = field(default_factory=dict)
    audit_results: list[AuditResult] = field(default_factory=list)
    validator_results: list[ValidatorResult] = field(default_factory=list)
    input_sha256: str | None = None
    validator_version: str | None = None
    delivery: dict[str, object] | None = None

    @property
    def exit_code(self) -> int:
        if self.blocking:
            return EXIT_BLOCKING
        if self.warnings:
            return EXIT_WARNINGS
        return EXIT_PASS


# ── Required-audit execution (issue #378) ────────────────────────────────────


def _sha256(path: Path) -> str | None:
    """Return the sha256 of a file's bytes, or None on read failure."""
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return None


def _load_delivery_result(
    path: Path | None,
    audited_path: Path,
) -> tuple[dict[str, object] | None, list[str]]:
    """Load and verify an optional result emitted by ``md_to_pdf --json``.

    Status strings alone are not provenance. The result must bind to the
    exact audited Markdown input, and ``pdf_ready`` must point to a real,
    non-empty PDF whose size and hash match the declared metadata.
    """

    if path is None:
        return None, []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return None, [f"delivery result cannot be read as JSON: {exc}"]
    if not isinstance(payload, dict):
        return None, ["delivery result must be a JSON object"]

    errors: list[str] = []
    expected_input = audited_path.resolve()
    input_value = payload.get("input_path")
    if not isinstance(input_value, str) or not input_value:
        errors.append("delivery result input_path must be a non-empty string")
    elif not Path(input_value).is_absolute() or Path(input_value).resolve() != expected_input:
        errors.append(
            f"delivery result input_path does not match audited report: {input_value!r}"
        )

    input_hash = payload.get("input_sha256")
    actual_input_hash = _sha256(expected_input)
    if not isinstance(input_hash, str) or not input_hash:
        errors.append("delivery result input_sha256 is required")
    elif actual_input_hash is None or input_hash != actual_input_hash:
        errors.append("delivery result input_sha256 does not match audited report")

    delivery_status = payload.get("delivery_status")
    markdown_status = payload.get("markdown_status")
    valid_delivery = {"md_ready", "pdf_ready", "pdf_failed", "not_run"}
    if delivery_status not in valid_delivery:
        errors.append(f"invalid delivery_status in delivery result: {delivery_status!r}")
    if markdown_status not in {"md_ready", "not_run"}:
        errors.append(f"invalid markdown_status in delivery result: {markdown_status!r}")
    if delivery_status in {"md_ready", "pdf_ready", "pdf_failed"} and markdown_status != "md_ready":
        errors.append(f"{delivery_status} requires markdown_status=md_ready")

    pdf_value = payload.get("pdf_path")
    pdf_path: Path | None = None
    if pdf_value is not None:
        if not isinstance(pdf_value, str) or not pdf_value:
            errors.append("delivery result pdf_path must be a non-empty string when present")
        elif not Path(pdf_value).is_absolute():
            errors.append("delivery result pdf_path must be absolute")
        else:
            pdf_path = Path(pdf_value).resolve()

    if delivery_status == "pdf_ready":
        if pdf_path is None or not pdf_path.is_file():
            errors.append("pdf_ready requires an existing PDF artifact")
        else:
            try:
                actual_size = pdf_path.stat().st_size
                with pdf_path.open("rb") as stream:
                    header = stream.read(4)
            except OSError as exc:
                errors.append(f"cannot inspect pdf_ready artifact: {exc}")
            else:
                declared_size = payload.get("pdf_size_bytes")
                if not isinstance(declared_size, int) or isinstance(declared_size, bool):
                    errors.append("pdf_ready requires integer pdf_size_bytes")
                elif declared_size != actual_size or actual_size <= 0:
                    errors.append("pdf_size_bytes does not match the PDF artifact")
                if header != b"%PDF":
                    errors.append("pdf_ready artifact does not have a PDF header")
                declared_hash = payload.get("pdf_sha256")
                actual_hash = _sha256(pdf_path)
                if not isinstance(declared_hash, str) or not declared_hash:
                    errors.append("pdf_ready requires pdf_sha256")
                elif actual_hash is None or declared_hash != actual_hash:
                    errors.append("pdf_sha256 does not match the PDF artifact")
    elif pdf_path is not None and pdf_path.is_file():
        declared_hash = payload.get("pdf_sha256")
        if declared_hash is not None and declared_hash != _sha256(pdf_path):
            errors.append("pdf_sha256 does not match the optional PDF artifact")

    return (payload, []) if not errors else (None, errors)


def _parse_audit_block_statuses(path: Path) -> tuple[dict[str, dict[str, str]], list[str]]:
    """Parse the report's Route and audit status tables.

    Returns ``(statuses, malformed)`` where statuses maps {audit_id:
    {"status": ..., "evidence": ...}} and malformed lists structural
    errors.  audit_id is the first table column and status is derived from
    the Status column.  Used to record explicit status for manual/process
    audits that cannot be executed by a validator.

    Fail-closed rules (issue #378): more than one Route and audit status
    block is malformed — a second block could hide a '❌ Not run' after a
    '✅ Passed' first block, so callers must treat it as blocking instead
    of parsing only the first occurrence.
    """
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except (OSError, UnicodeError):
        return {}, []
    # Shared declaration sanitizer: strips fences (state machine) and HTML
    # comments so forged blocks inside ```fences or <!-- --> never count
    # as real declarations (issue #378).
    cleaned = vc_strip_fences(text)
    lines = cleaned.split("\n")

    block_heading_re = re.compile(
        r"^#{2,3}\s+.*(?:Route\s+and\s+audit\s+status|路由与审计状态)",
        re.IGNORECASE,
    )
    block_starts = [i for i, line in enumerate(lines) if block_heading_re.match(line)]
    if not block_starts:
        # Zero blocks is also cardinality != 1: the audit status is not
        # declared at all, so the structural reason is reported explicitly
        # instead of relying on other validators (issue #378).
        return {}, [
            "missing 'Route and audit status' block — exactly one is "
            "required (issue #378)"
        ]
    if len(block_starts) > 1:
        return {}, [
            f"multiple 'Route and audit status' blocks found "
            f"({len(block_starts)}) — exactly one is required; a second "
            "block could hide a not_run declaration (issue #378)"
        ]
    block_start = block_starts[0]

    table_lines: list[str] = []
    for line in lines[block_start + 1:]:
        if re.match(r"^#{2,3}\s", line):
            break
        if line.strip().startswith("|") and "---" not in line:
            table_lines.append(line.strip())
    if len(table_lines) < 2:
        return {}, []

    statuses: dict[str, dict[str, str]] = {}
    for row in table_lines[1:]:  # skip header row
        cells = [c.strip() for c in row.strip("|").split("|")]
        if len(cells) < 2 or not cells[0]:
            continue
        audit_id = cells[0].lower()
        status_cell = cells[1].lower()
        evidence = cells[2] if len(cells) > 2 else ""
        if audit_id in statuses:
            # Duplicate declaration is malformed: fail closed instead of
            # last-write-wins, so a trailing '✅ Passed' cannot override an
            # earlier '❌ Not run' (issue #378).
            statuses[audit_id] = {
                "status": "not_run",
                "evidence": "",
                "duplicate": "1",
            }
            continue
        statuses[audit_id] = {
            "status": _parse_status_cell(status_cell),
            "evidence": evidence,
        }
    return statuses, []


def _parse_status_cell(status_cell: str) -> str:
    """Map a report status cell to a canonical manual-audit status.

    Fail-closed rules (issue #378):
    - negative markers (not passed / did not pass / not_passed / unpassed /
      not passing / 未通过 / ❌ / ✗ / fail / pending / blocked) take
      precedence over any positive wording, so '❌ Not passed' can never
      parse as pass;
    - the positive branches are whole-cell matches: the cell must BE a
      canonical token (``Pass``/``Passed``/``✅|✓|✔ Passed``/``已通过``,
      ``skipped``/``已跳过``, ``partial``/``部分``), optionally with an
      emoji marker and surrounding whitespace.  A bare 'pass'/'passed'
      substring inside unknown or caveated wording (``passed-ish``,
      ``conditional-pass``, ``Status: Pass``, ``pass (manual)``) is never
      accepted;
    - anything unrecognized defaults to ``not_run``.
    """
    cell = status_cell.lower()
    if re.search(
        r"not\s*[-_ ]?pass(?:ed|ing)?|unpassed|未通过|✗|✖|❌|"
        r"fail(?:ed)?|pending|in progress|blocked",
        cell,
    ):
        return "not_run"
    if re.fullmatch(r"(?:⚠\ufe0f?)?\s*(?:skipped|已跳过)\s*", cell):
        return "skipped"
    if re.fullmatch(r"(?:partial|部分(?:通过)?)\s*", cell):
        return "partial"
    if re.fullmatch(r"(?:✅|✓|✔)?\s*(?:pass(?:ed)?|已通过)\s*", cell):
        return "pass"
    return "not_run"


def _audit_validator_fn(binding: str) -> ValidatorFn | None:
    """Resolve an audit validator_binding id to a function."""
    fn = _AUDIT_VALIDATOR_REGISTRY.get(binding)
    if fn is None:
        fn = _VALIDATOR_REGISTRY.get(binding)
    return fn


def _execution_source(execution_type: str, *, legacy: bool = False) -> str:
    """Map registry execution type to the public provenance vocabulary."""
    if legacy:
        return "legacy_self_attested"
    if execution_type == "automated":
        return "automated_validator"
    if execution_type == "process":
        return "process_node_evidence"
    return "manual_checklist_attestation"


def _registered_validator_bindings() -> set[str]:
    """Return validator ids with runtime functions in this module."""
    return set(_VALIDATOR_REGISTRY) | set(_AUDIT_VALIDATOR_REGISTRY)


def _execute_required_audits(
    path: Path,
    route_id: str,
    strict: bool,
    research_pack: Path | None,
) -> tuple[list[AuditResult], list[str], list[str]]:
    """Execute all required audits for a route plus global audits.

    Returns (audit_results, blocking_errors, warnings).  Fail-closed rules:
    - required audit id missing from audit registry → blocking;
    - automated audit without a validator binding → blocking;
    - manual/process audit with no declaration in the report → ``not_run``,
      which is blocking in strict mode and a warning otherwise;
    - research-pack without --research-pack → explicit ``skipped`` outside
      strict mode, ``not_run`` + blocking under ``--strict``.
    """
    audit_ids = _ROUTE_REGISTRY.required_audits_for(route_id) + list(
        _AUDIT_REGISTRY.global_audit_ids()
    )
    block_statuses, block_malformed = _parse_audit_block_statuses(path)
    try:
        visible_text = vc_strip_fences(
            path.read_text(encoding="utf-8", errors="replace")
        )
    except (OSError, UnicodeError):
        visible_text = None
    # Artifact binding for strict provenance (issue #401): audit-record must
    # prove it targets the current artifact, not any template.  Compute the
    # input hash once and extract the contract's stable artifact_id up front
    # so validation can fail closed on mismatched bindings.
    expected_artifact_sha256 = _sha256(path) if path.is_file() else None
    contract_data_for_binding: dict | None = None
    try:
        contract_data_for_binding = extract_contract_from_markdown(
            path.read_text(encoding="utf-8", errors="replace")
        )
    except (OSError, UnicodeError):
        contract_data_for_binding = None
    expected_artifact_id: str | None = None
    if isinstance(contract_data_for_binding, dict):
        raw_aid = contract_data_for_binding.get("artifact_id")
        if isinstance(raw_aid, str) and raw_aid.strip():
            expected_artifact_id = raw_aid.strip()
    results: list[AuditResult] = []
    blocking: list[str] = []
    warnings: list[str] = []

    # Multiple Route and audit status blocks are structural malformation
    # (a second block could hide a not_run declaration): blocking in every
    # mode, not only strict (issue #378).
    blocking.extend(f"[audit-block] {e}" for e in block_malformed)

    for audit_id in audit_ids:
        audit = _AUDIT_REGISTRY.get_audit(audit_id)
        if audit is None:
            blocking.append(
                f"Required audit '{audit_id}' has no entry in "
                f"schemas/audit-registry.json — add it or remove it from "
                f"the route's required_audits"
            )
            continue

        if audit is not None and audit.execution_type != "automated":
            # manual / process audit: record explicit status from the report.
            declared = block_statuses.get(audit_id.lower())
            if declared is None:
                status = "not_run"
                reason = "not declared in Route and audit status block"
            elif declared.get("duplicate"):
                status = "not_run"
                reason = (
                    f"audit '{audit_id}' declared multiple times in the "
                    "Route and audit status block — duplicate declarations "
                    "are malformed"
                )
            else:
                status = declared["status"]
                reason = None
            evidence = [declared["evidence"]] if declared and declared["evidence"] else []
            execution_source = _execution_source(audit.execution_type)
            evidence_provenance: list[dict[str, object]] = []
            if status == "pass" and not evidence:
                status = "partial"
                reason = "declared Passed but evidence column is empty"
            elif (
                declared is not None
                and not declared.get("duplicate")
                and status in {"skipped", "not_run", "partial"}
                and not evidence
            ):
                reason = (
                    f"declared status '{status}' requires a reason or evidence "
                    "reference"
                )
            elif status == "pass":
                evidence_result = validate_evidence_reference(
                    evidence[0],
                    artifact_text=visible_text,
                    base_dir=Path(__file__).resolve().parent.parent,
                    strict=strict,
                    artifact_label="report",
                    known_validator_bindings=_registered_validator_bindings(),
                    execution_type=audit.execution_type,
                    expected_audit_id=audit_id,
                    expected_artifact_sha256=expected_artifact_sha256,
                    expected_artifact_id=expected_artifact_id,
                )
                if evidence_result.legacy:
                    execution_source = _execution_source(
                        audit.execution_type, legacy=True
                    )
                if evidence_result.provenance:
                    evidence_provenance.append(
                        {
                            **evidence_result.provenance,
                            "execution_source": execution_source,
                        }
                    )
                if evidence_result.errors:
                    status = "partial"
                    reason = "; ".join(evidence_result.errors)
            result = AuditResult(
                audit_id=audit_id,
                execution_type=audit.execution_type,
                status=status,
                execution_source=execution_source,
                evidence=evidence,
                evidence_provenance=evidence_provenance,
                reason=reason,
            )
            results.append(result)
            if status == "pass":
                continue
            message = (
                f"[{audit_id}] {status} — "
                f"{reason or 'not executed by a validator'}"
            )
            if strict:
                blocking.append(message)
            # Non-strict is the legacy compatibility mode: the status is
            # still recorded explicitly (never aggregated as a Pass) but
            # does not change the exit code.
            continue

        # automated audit (registry-bound; delivery-scope audits are also
        # registry entries with scope: delivery, issue #393)
        binding = audit.validator_binding
        if binding is None:
            blocking.append(
                f"Required audit '{audit_id}' is automated but has no "
                f"validator_binding in schemas/audit-registry.json"
            )
            continue
        fn = _audit_validator_fn(binding)
        if fn is None:
            blocking.append(
                f"Required audit '{audit_id}' binds unknown validator "
                f"'{binding}' — registry and audit_report.py are out "
                f"of sync"
            )
            continue
        if audit_id == "research-pack" and research_pack is None:
            # Issue #378 acceptance: a strict task without a pack fails
            # closed; non-strict records an explicit skip (legacy mode).
            status = "skipped"
            reason = "no --research-pack path provided"
            if strict:
                status = "not_run"
                reason = "no --research-pack path provided (strict mode requires it)"
                blocking.append(f"[research-pack] not_run — {reason}")
            results.append(AuditResult(
                audit_id=audit_id,
                execution_type="automated",
                status=status,
                execution_source="automated_validator",
                validator_binding=binding,
                evidence_provenance=[{
                    "kind": "automated_validator",
                    "locator": binding,
                    "validator_binding": binding,
                    "verified": False,
                }],
                reason=reason,
            ))
            continue
        try:
            target = research_pack if audit_id == "research-pack" else path
            audit_kwargs: dict[str, object] = {"strict": strict}
            if audit_id == "research-pack":
                audit_kwargs["report_path"] = path
            check = fn(target, **audit_kwargs)
        except Exception as exc:
            check = CheckResult(
                name=audit_id,
                errors=[f"{audit_id} validator crashed: {exc}"],
            )
        status = (
            "fail" if check.errors
            else "conditional-pass" if check.warnings
            else "pass"
        )
        # Legacy compatibility: outside strict mode, failures of the
        # delivery-scope global audits (markdown-delivery / research-pack)
        # are recorded in the audit result but do not change the exit code,
        # so pre-contract reports keep their previous behavior.  In strict
        # mode they block.
        advisory = audit.scope == "delivery" and not strict and check.errors
        if check.errors:
            evidence = [str(e)[:200] for e in check.errors[:5]]
        else:
            # Success carries an evidence location (issue #378 acceptance 8).
            evidence = [f"{target}: no violations found by {binding}"]
        evidence_provenance = [{
            "kind": "automated_validator",
            "locator": binding,
            "validator_binding": binding,
            "target": str(target),
            "verified": True,
        }]
        results.append(AuditResult(
            audit_id=audit_id,
            execution_type="automated",
            status=status,
            execution_source="automated_validator",
            errors=list(check.errors),
            warnings=list(check.warnings),
            validator_binding=binding,
            evidence=evidence,
            evidence_provenance=evidence_provenance,
            reason="advisory outside strict mode" if advisory else None,
        ))
        if not advisory:
            blocking.extend(f"[{audit_id}] {e}" for e in check.errors)
            warnings.extend(f"[{audit_id}] {w} (audit)" for w in check.warnings)

    # Secondary-route hard-fail verification must have its own audit result
    # (issue #378 acceptance 6) — primary-route coverage is not enough.  The
    # contract declares secondary routes; each needs an explicit
    # `<secondary>-secondary-hard-fail` entry in the contract audits.
    contract_data: dict | None = None
    try:
        contract_data = extract_contract_from_markdown(
            path.read_text(encoding="utf-8", errors="replace")
        )
    except (OSError, UnicodeError):
        pass
    contract_audits: list[dict] = []
    if isinstance(contract_data, dict):
        contract_audits = contract_data.get("audits", []) or []
    secondary_ids = (
        [str(s) for s in (contract_data.get("secondary_routes", []) or [])]
        if isinstance(contract_data, dict)
        else []
    )
    for sr in secondary_ids:
        derived_id = f"{sr}-secondary-hard-fail"
        entry = next((a for a in contract_audits if a.get("id") == derived_id), None)
        if entry is None:
            status, reason = "not_run", (
                f"secondary route '{sr}' declared but no "
                f"'{derived_id}' entry in the contract audits"
            )
        elif str(entry.get("status", "")).lower() in ("passed", "pass", "已通过"):
            status, reason = "pass", None
        else:
            status, reason = str(entry.get("status", "not_run")).lower(), None
        raw_evidence = entry.get("evidence") if entry else None
        if isinstance(raw_evidence, str) and raw_evidence.strip():
            evidence = [raw_evidence.strip()]
        elif isinstance(raw_evidence, dict):
            evidence = [json.dumps(raw_evidence, ensure_ascii=False, sort_keys=True)]
        else:
            evidence = []
        execution_source = _execution_source("manual")
        evidence_provenance: list[dict[str, object]] = []
        if status == "pass" and not evidence:
            status, reason = "partial", "hard-fail entry declared Passed but evidence empty"
        elif status == "pass":
            evidence_result = validate_evidence_reference(
                raw_evidence,
                artifact_text=visible_text,
                base_dir=Path(__file__).resolve().parent.parent,
                strict=strict,
                artifact_label="report",
                known_validator_bindings=_registered_validator_bindings(),
                execution_type="manual",
                expected_audit_id=derived_id,
                expected_artifact_sha256=expected_artifact_sha256,
                expected_artifact_id=expected_artifact_id,
            )
            if evidence_result.legacy:
                execution_source = _execution_source("manual", legacy=True)
            if evidence_result.provenance:
                evidence_provenance.append(
                    {
                        **evidence_result.provenance,
                        "execution_source": execution_source,
                    }
                )
            if evidence_result.errors:
                status = "partial"
                reason = "; ".join(evidence_result.errors)
        result = AuditResult(
            audit_id=derived_id,
            execution_type="manual",
            status=status,
            execution_source=execution_source,
            evidence=evidence,
            evidence_provenance=evidence_provenance,
            reason=reason,
        )
        results.append(result)
        if status != "pass":
            message = f"[{derived_id}] {status} — {reason or 'not verified'}"
            if strict:
                blocking.append(message)
            # non-strict: recorded only (legacy compatibility)

    return results, blocking, warnings


def _compute_verdict(
    route: str | None,
    results: list[CheckResult],
    audit_results: list[AuditResult] | None = None,
    blocking_extra: list[str] | None = None,
    warnings_extra: list[str] | None = None,
    delivery: dict[str, object] | None = None,
    expected_validators: list[str] | None = None,
    source_path: str | None = None,
) -> AuditVerdict:
    """Aggregate check results into a single consolidated verdict.

    Also records one ValidatorResult per route-level validator so the JSON
    verdict is a complete provenance artifact (issue #393).  Any dispatched
    validator with no recorded result is flagged ``incomplete`` and adds a
    blocking error — a missing validator result must never aggregate to a
    silent Pass.
    """
    blocking: list[str] = []
    warnings: list[str] = []
    status: dict[str, str] = {}
    validator_results: list[ValidatorResult] = []

    for result in results:
        for err in result.errors:
            blocking.append(f"[{result.name}] {err}")
        for warn in result.warnings:
            warnings.append(f"[{result.name}] {warn}")

        if result.errors:
            status[result.name] = "fail"
        elif result.warnings:
            status[result.name] = "conditional-pass"
        else:
            status[result.name] = "pass"

    # Build one ValidatorResult per dispatched validator, keyed by the
    # canonical manifest binding id (issue #393).  Results are appended in
    # dispatch order, so expected_validators[i] pairs with results[i].  A
    # validator whose CheckResult name differs from its binding id (e.g.
    # market-outlook-monitoring vs market-outlook-monitoring-actionability)
    # is still recorded under the canonical id.
    if expected_validators is not None:
        for i, validator_id in enumerate(expected_validators):
            if i < len(results):
                result = results[i]
                evidence = list(result.errors[:5]) or list(result.warnings[:5]) or [
                    f"{source_path or '<report>'}: no violations found by "
                    f"{validator_id}"
                ]
                validator_results.append(ValidatorResult(
                    validator_id=validator_id,
                    status=status.get(result.name, "pass"),
                    errors=list(result.errors),
                    warnings=list(result.warnings),
                    evidence=evidence,
                ))
            else:
                # Fail-closed: a dispatched validator with no recorded result
                # must never be interpreted as a silent Pass (issue #393).
                validator_results.append(ValidatorResult(
                    validator_id=validator_id,
                    status="incomplete",
                    reason="validator result missing — never aggregated as pass",
                ))
                blocking.append(
                    f"[{validator_id}] incomplete — validator result missing "
                    f"(issue #393: missing results must fail closed, not pass)"
                )

    blocking.extend(blocking_extra or [])
    warnings.extend(warnings_extra or [])
    for audit in audit_results or []:
        status[f"audit:{audit.audit_id}"] = audit.status

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
        audit_results=list(audit_results or []),
        validator_results=validator_results,
        delivery=delivery,
    )


# ── Output formatting ──────────────────────────────────────────────────────


def format_verdict(verdict: AuditVerdict) -> str:
    """Render the consolidated verdict to a human-readable string."""
    lines: list[str] = []

    route_str = verdict.route or "(not detected)"
    lines.append(f"Route: {route_str}")
    lines.append(f"Overall: {verdict.overall}")
    if verdict.delivery:
        lines.append(
            f"Delivery: {verdict.delivery.get('delivery_status')} "
            f"(markdown={verdict.delivery.get('markdown_status')})"
        )
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

    if verdict.audit_results:
        lines.append("Required audit results:")
        for audit in verdict.audit_results:
            line = f"- {audit.audit_id}: {audit.status}"
            if audit.reason:
                line += f" ({audit.reason})"
            if audit.validator_binding:
                line += f" [binding: {audit.validator_binding}]"
            lines.append(line)
        lines.append("")

    if verdict.recommended_audit_status:
        lines.append("Recommended audit status:")
        for audit_name, status in sorted(verdict.recommended_audit_status.items()):
            lines.append(f"- {audit_name}: {status}")
        lines.append("")

    return "\n".join(lines)


def _verdict_to_json(verdict: AuditVerdict) -> str:
    """Serialize an AuditVerdict to machine-readable JSON (issue #378).

    The human-readable summary is derived from this structure; consumers
    (CI, forward tests) should read this JSON rather than parse text.
    ``schema_version`` pins the JSON contract so consumers can fail closed
    on unknown shapes instead of assuming Pass (issue #393).  Additive-only
    field evolution keeps old consumers working.
    """
    payload: dict = {
        "schema_version": AUDIT_JSON_SCHEMA_VERSION,
        "route": verdict.route,
        "overall": verdict.overall,
        "exit_code": verdict.exit_code,
        "blocking": verdict.blocking,
        "warnings": verdict.warnings,
        "input_sha256": verdict.input_sha256,
        "validator_version": verdict.validator_version,
        "delivery": verdict.delivery,
        "validators": [
            {
                "validator_id": v.validator_id,
                "status": v.status,
                "errors": v.errors,
                "warnings": v.warnings,
                "evidence": v.evidence,
                "execution_source": v.execution_source,
                "validator_version": v.validator_version,
                "reason": v.reason,
            }
            for v in verdict.validator_results
        ],
        "audits": [
            {
                "audit_id": a.audit_id,
                "execution_type": a.execution_type,
                "execution_source": a.execution_source,
                "status": a.status,
                "errors": a.errors,
                "warnings": a.warnings,
                "evidence": a.evidence,
                "evidence_provenance": a.evidence_provenance,
                "validator_binding": a.validator_binding,
                "reason": a.reason,
            }
            for a in verdict.audit_results
        ],
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


# ── Main ────────────────────────────────────────────────────────────────────


def _audit_report_impl(
    path: Path,
    route: str | None = None,
    strict: bool = False,
    allow_route_fallback: bool = False,
    require_contract: bool = False,
    research_pack: Path | None = None,
    activation_snapshot: Path | None = None,
    delivery_result: Path | None = None,
) -> AuditVerdict:
    """Run route-aware audit on a report and return the consolidated verdict.

    Parameters
    ----------
    path : Path
        Path to the Markdown report file.
    route : str | None
        Route name to select validators. If None, auto-detect from the report.
        Falls back to 'technical-deep-dive' when auto-detection fails (no route
        declared at all).  Unknown routes (declared but unsupported) are a
        blocking error (exit 2), not silently fallen back.
    strict : bool
        Fail-closed mode (issue #378): a missing route declaration and a
        missing contract are blocking, and manual/process audits that were
        not run cannot aggregate to Pass.
    allow_route_fallback : bool
        Legacy opt-in: unknown routes fall back to the default route.
    require_contract : bool
        Require a valid route activation contract. Implied by strict.
    research_pack : Path | None
        Research Pack file to validate as the research-pack required audit.
        None records the audit as ``skipped`` (non-strict) or ``not_run``
        + blocking (strict, issue #378).
    activation_snapshot : Path | None
        Canonical structured activation snapshot. When supplied, strict
        contract validation requires report/pack/contract route and reference
        consistency with this snapshot.

    Returns
    -------
    AuditVerdict
        Consolidated verdict with blocking errors, warnings, and recommended
        audit status.  Provenance (input sha256 / validator version) is
        filled by the public audit_report() wrapper on every path.
    """
    delivery, delivery_errors = _load_delivery_result(delivery_result, path)
    if not path.is_file():
        return AuditVerdict(
            route=route,
            overall="fail",
            blocking=[f"{path}: not a regular file", *delivery_errors],
            delivery=delivery,
        )

    resolved_route: str | None = route

    # Auto-detect route if not specified.  In strict mode a missing route
    # declaration is a blocking error (issue #378) — no silent fallback to
    # technical-deep-dive.  Non-strict keeps the legacy fallback.
    if resolved_route is None:
        detected = _auto_detect_route(path)
        if detected is not None:
            resolved_route = detected
        elif strict:
            return AuditVerdict(
                route=None,
                overall="fail",
                blocking=[*delivery_errors,
                    "No route declaration found in report and --route was "
                    "not given — strict mode requires an explicit route "
                    "(issue #378)"
                ],
                delivery=delivery,
            )
        else:
            resolved_route = _DEFAULT_ROUTE

    # Normalize the route (in case user passed --route with a display name)
    try:
        resolved_route = _normalize_route(resolved_route)
    except UnknownRouteError as exc:
        if allow_route_fallback:
            # Explicit opt-in: fall back to default route (legacy behavior)
            print(
                f"warning: unknown route '{route or '(auto-detected)'}', "
                f"falling back to '{_DEFAULT_ROUTE}' validators "
                f"(--allow-route-fallback enabled)",
                file=sys.stderr,
            )
            resolved_route = _DEFAULT_ROUTE
        else:
            # Unknown route — blocking error, no fallback
            supported = ", ".join(sorted(_ROUTE_REGISTRY.route_ids()))
            return AuditVerdict(
                route=resolved_route,
                overall="fail",
                blocking=[*delivery_errors,
                    f"Unknown route '{resolved_route}'. "
                    f"Supported routes: {supported} — {exc}"
                ],
                delivery=delivery,
            )

    # Look up validators for the resolved route (fail closed on drift)
    try:
        validators = _dispatch_validators(resolved_route)
    except RegistryError as exc:
        return AuditVerdict(
            route=resolved_route,
            overall="fail",
            blocking=[*delivery_errors, str(exc)],
            delivery=delivery,
        )

    # Strict mode implies --require-contract (issue #378): a strict task
    # without a contract fails by definition instead of silently skipping.
    effective_require_contract = require_contract or strict

    # Run each validator with shared flags as keyword arguments
    results: list[CheckResult] = []
    for validator in validators:
        result = validator(
            path,
            strict=strict,
            require_contract=effective_require_contract,
            research_pack=research_pack,
            activation_snapshot=activation_snapshot,
        )
        results.append(result)

    # Execute required audits from the audit registry (issue #378)
    audit_results, audit_blocking, audit_warnings = _execute_required_audits(
        path, resolved_route, strict=strict, research_pack=research_pack
    )

    verdict = _compute_verdict(
        resolved_route,
        results,
        audit_results=audit_results,
        blocking_extra=[*delivery_errors, *audit_blocking],
        warnings_extra=audit_warnings,
        delivery=delivery,
        expected_validators=_ROUTE_REGISTRY.validators_for(resolved_route),
        source_path=str(path),
    )
    return verdict


def _finalize_verdict(verdict: AuditVerdict, path: Path) -> AuditVerdict:
    """Fill provenance (input sha256, validator version) on any verdict.

    Runs on every return path of audit_report() — including early failures
    (missing route declaration, unknown route, registry drift) so JSON
    consumers always get the artifact hash and validator version
    (issue #378 acceptance 8).
    """
    if verdict.input_sha256 is None:
        verdict.input_sha256 = _sha256(path)
    if verdict.validator_version is None:
        verdict.validator_version = (
            f"audit-registry-v{_AUDIT_REGISTRY.version} "
            f"(route-manifest-v{_ROUTE_REGISTRY.version})"
        )
    # Propagate the shared validator version onto each route-level validator
    # result so JSON carries per-validator provenance (issue #393).
    for validator in verdict.validator_results:
        if validator.validator_version is None:
            validator.validator_version = verdict.validator_version
    return verdict


def audit_report(
    path: Path,
    route: str | None = None,
    strict: bool = False,
    allow_route_fallback: bool = False,
    require_contract: bool = False,
    research_pack: Path | None = None,
    activation_snapshot: Path | None = None,
    delivery_result: Path | None = None,
) -> AuditVerdict:
    """Public entry point: run the audit and attach provenance to the verdict.

    See _audit_report_impl for the parameters and the fail-closed rules.
    """
    verdict = _audit_report_impl(
        path,
        route=route,
        strict=strict,
        allow_route_fallback=allow_route_fallback,
        require_contract=require_contract,
        research_pack=research_pack,
        activation_snapshot=activation_snapshot,
        delivery_result=delivery_result,
    )
    return _finalize_verdict(verdict, path)


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
        help=(
            "Fail-closed mode (issue #378): missing route/contract are "
            "blocking, manual audits not run cannot pass."
        ),
    )
    parser.add_argument(
        "--allow-route-fallback",
        action="store_true",
        default=False,
        help=(
            "Allow unknown routes to fall back to 'technical-deep-dive' "
            "validators (legacy behavior). By default, unknown routes are "
            "a blocking error (exit 2)."
        ),
    )
    parser.add_argument(
        "--require-contract",
        action="store_true",
        default=False,
        help=(
            "Require a valid route activation contract in the report. "
            "When set, missing or malformed contract blocks are blocking errors. "
            "Use in CI to enforce contract adoption. Implied by --strict."
        ),
    )
    parser.add_argument(
        "--research-pack",
        type=str,
        default=None,
        help=(
            "Path to the Research Pack .md file. When given, the research-pack "
            "required audit validates it; without it the audit is skipped "
            "(or blocking under --strict, issue #378)."
        ),
    )
    parser.add_argument(
        "--activation-snapshot",
        type=str,
        default=None,
        help=(
            "Path to a canonical activation snapshot JSON. When supplied, "
            "strict mode blocks activation/report/pack/contract mismatches."
        ),
    )
    parser.add_argument(
        "--delivery-result",
        type=str,
        default=None,
        help=(
            "Optional JSON result emitted by md_to_pdf.py --json. "
            "The delivery layer remains separate from content-audit status."
        ),
    )
    parser.add_argument(
        "--json",
        action="store_true",
        default=False,
        help=(
            "Emit a machine-readable JSON verdict on stdout (route, audit id, "
            "status, evidence, input sha256). The human-readable summary is "
            "suppressed on stdout."
        ),
    )
    args = parser.parse_args(argv)

    path = Path(args.path)
    verdict = audit_report(
        path,
        route=args.route,
        strict=args.strict,
        allow_route_fallback=args.allow_route_fallback,
        require_contract=args.require_contract,
        research_pack=Path(args.research_pack) if args.research_pack else None,
        activation_snapshot=(
            Path(args.activation_snapshot) if args.activation_snapshot else None
        ),
        delivery_result=Path(args.delivery_result) if args.delivery_result else None,
    )

    if args.json:
        print(_verdict_to_json(verdict))
    else:
        output = format_verdict(verdict)
        print(output)

    return verdict.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
