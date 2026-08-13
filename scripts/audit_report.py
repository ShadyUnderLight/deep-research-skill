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
    strip_fenced_code_blocks,
)

from validate_declared_execution import validate_file as vde_validate_file
from validate_table_role_labels import validate_file as vtr_validate_file
from validate_source_label_consistency import validate_file as vsl_validate_file
from validate_listed_company_delivery import validate_file as vlc_validate_file
from validate_scoring_replicability import validate_file as vsr_validate_file
from validate_contract import (
    extract_contract_from_markdown,
    extract_report_primary_route,
    has_contract_block,
    validate_contract,
)
from validate_contract import (
    _extract_pack_artifact_id as vc_extract_pack_artifact_id,
    _resolve_pack_primary_route as vc_resolve_pack_primary_route,
)

# Validators executed only through required-audit bindings (issue #378).
from validate_markdown_delivery import validate_markdown_delivery as vmd_validate
from validate_forward_looking_labels import validate_file as vfl_validate_file
from validate_research_pack import (
    find_missing_headings as vrp_find_missing_headings,
    run_strict_checks as vrp_run_strict_checks,
    strip_fenced_code_blocks as vrp_strip_fenced_code_blocks,
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
# These are delivery-pipeline validators rather than checklist audits, so
# they live in code (not in audit-registry.json which requires a checklist
# file per audit): audit id → validator binding id.  research-pack is
# skipped outside strict mode when no --research-pack is given (and a
# not_run + blocking error under --strict); markdown-delivery always runs
# against the report itself.
GLOBAL_AUDITS: dict[str, str] = {
    "markdown-delivery": "markdown-delivery",
    "research-pack": "research-pack",
}


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

    cleaned = strip_fenced_code_blocks(text)
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
    cleaned = strip_fenced_code_blocks(text)

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

    contract = extract_contract_from_markdown(text)
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
        if require_contract:
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
        report_primary_route=extract_report_primary_route(text),
        strict=strict,
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
            research_pack_provided=True,
            strict=strict,
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
        errors.extend(vrp_run_strict_checks(cleaned))
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
    cleaned = strip_fenced_code_blocks(text)
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
    must never aggregate to a Pass verdict.
    """

    audit_id: str
    execution_type: str  # automated | manual | process
    status: str
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)
    validator_binding: str | None = None
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
    input_sha256: str | None = None
    validator_version: str | None = None

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


def _parse_audit_block_statuses(path: Path) -> dict[str, dict[str, str]]:
    """Parse the report's Route and audit status table.

    Returns {audit_id: {"status": ..., "evidence": ...}} where audit_id is
    the first table column and status is derived from the Status column
    (passed/已通过 → pass, skipped/已跳过 → skipped, otherwise not_run).
    Used to record explicit status for manual/process audits that cannot be
    executed by a validator.
    """
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except (OSError, UnicodeError):
        return {}
    cleaned = strip_fenced_code_blocks(text)
    lines = cleaned.split("\n")
    block_start = -1
    for i, line in enumerate(lines):
        if re.match(
            r"^#{2,3}\s+.*(?:Route\s+and\s+audit\s+status|路由与审计状态)",
            line,
            re.IGNORECASE,
        ):
            block_start = i
            break
    if block_start < 0:
        return {}

    table_lines: list[str] = []
    for line in lines[block_start + 1:]:
        if re.match(r"^#{2,3}\s", line):
            break
        if line.strip().startswith("|") and "---" not in line:
            table_lines.append(line.strip())
    if len(table_lines) < 2:
        return {}

    statuses: dict[str, dict[str, str]] = {}
    for row in table_lines[1:]:  # skip header row
        cells = [c.strip() for c in row.strip("|").split("|")]
        if len(cells) < 2 or not cells[0]:
            continue
        audit_id = cells[0].lower()
        status_cell = cells[1].lower()
        evidence = cells[2] if len(cells) > 2 else ""
        statuses[audit_id] = {
            "status": _parse_status_cell(status_cell),
            "evidence": evidence,
        }
    return statuses


def _parse_status_cell(status_cell: str) -> str:
    """Map a report status cell to a canonical manual-audit status.

    Fail-closed rules (issue #378): negative markers (not passed / did not
    pass / not_passed / unpassed / not passing / 未通过 / ❌ / ✗ / fail /
    pending / blocked) take precedence over any positive wording, so
    '❌ Not passed' can never parse as pass.  The positive branch only
    matches canonical tokens at word boundaries (``\bpass(?:ed)?\b`` or
    ✅/✓/✔/已通过) — a bare 'pass'/'passed' substring inside unknown or
    negative wording is never accepted.  Anything unrecognized defaults to
    ``not_run``.
    """
    cell = status_cell.lower()
    if re.search(
        r"not\s*[-_ ]?pass(?:ed|ing)?|unpassed|未通过|✗|✖|❌|"
        r"fail(?:ed)?|pending|in progress|blocked",
        cell,
    ):
        return "not_run"
    if re.search(r"skipped|已跳过", cell):
        return "skipped"
    if re.search(r"partial|部分", cell):
        return "partial"
    if re.search(r"(?:✅|✓|✔)|\bpass(?:ed)?\b|已通过", cell):
        return "pass"
    return "not_run"


def _audit_validator_fn(binding: str) -> ValidatorFn | None:
    """Resolve an audit validator_binding id to a function."""
    fn = _AUDIT_VALIDATOR_REGISTRY.get(binding)
    if fn is None:
        fn = _VALIDATOR_REGISTRY.get(binding)
    return fn


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
    audit_ids = _ROUTE_REGISTRY.required_audits_for(route_id) + list(GLOBAL_AUDITS)
    block_statuses = _parse_audit_block_statuses(path)
    results: list[AuditResult] = []
    blocking: list[str] = []
    warnings: list[str] = []

    for audit_id in audit_ids:
        audit = _AUDIT_REGISTRY.get_audit(audit_id)
        global_binding = GLOBAL_AUDITS.get(audit_id)
        if audit is None and global_binding is None:
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
            else:
                status = declared["status"]
                reason = None
            evidence = [declared["evidence"]] if declared and declared["evidence"] else []
            if status == "pass" and not evidence:
                status = "partial"
                reason = "declared Passed but evidence column is empty"
            result = AuditResult(
                audit_id=audit_id,
                execution_type=audit.execution_type,
                status=status,
                evidence=evidence,
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

        # automated audit (either registry-bound or global delivery audit)
        binding = audit.validator_binding if audit is not None else global_binding
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
                validator_binding=binding,
                reason=reason,
            ))
            continue
        try:
            target = research_pack if audit_id == "research-pack" else path
            check = fn(target, strict=strict)
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
        # Legacy compatibility: outside strict mode, failures of the global
        # delivery audits (markdown-delivery / research-pack) are recorded in
        # the audit result but do not change the exit code, so pre-contract
        # reports keep their previous behavior.  In strict mode they block.
        advisory = audit is None and not strict and check.errors
        if check.errors:
            evidence = [str(e)[:200] for e in check.errors[:5]]
        else:
            # Success carries an evidence location (issue #378 acceptance 8).
            evidence = [f"{target}: no violations found by {binding}"]
        results.append(AuditResult(
            audit_id=audit_id,
            execution_type="automated",
            status=status,
            errors=list(check.errors),
            warnings=list(check.warnings),
            validator_binding=binding,
            evidence=evidence,
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
        evidence = [str(entry.get("evidence", "")).strip()] if entry and entry.get("evidence") else []
        if status == "pass" and not evidence:
            status, reason = "partial", "hard-fail entry declared Passed but evidence empty"
        result = AuditResult(
            audit_id=derived_id,
            execution_type="manual",
            status=status,
            evidence=evidence,
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

        if result.errors:
            status[result.name] = "fail"
        elif result.warnings:
            status[result.name] = "conditional-pass"
        else:
            status[result.name] = "pass"

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
    """
    payload: dict = {
        "route": verdict.route,
        "overall": verdict.overall,
        "exit_code": verdict.exit_code,
        "blocking": verdict.blocking,
        "warnings": verdict.warnings,
        "input_sha256": verdict.input_sha256,
        "validator_version": verdict.validator_version,
        "audits": [
            {
                "audit_id": a.audit_id,
                "execution_type": a.execution_type,
                "status": a.status,
                "errors": a.errors,
                "warnings": a.warnings,
                "evidence": a.evidence,
                "validator_binding": a.validator_binding,
                "reason": a.reason,
            }
            for a in verdict.audit_results
        ],
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


# ── Main ────────────────────────────────────────────────────────────────────


def audit_report(
    path: Path,
    route: str | None = None,
    strict: bool = False,
    allow_route_fallback: bool = False,
    require_contract: bool = False,
    research_pack: Path | None = None,
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
                blocking=[
                    "No route declaration found in report and --route was "
                    "not given — strict mode requires an explicit route "
                    "(issue #378)"
                ],
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
                blocking=[
                    f"Unknown route '{resolved_route}'. "
                    f"Supported routes: {supported} — {exc}"
                ],
            )

    # Look up validators for the resolved route (fail closed on drift)
    try:
        validators = _dispatch_validators(resolved_route)
    except RegistryError as exc:
        return AuditVerdict(
            route=resolved_route,
            overall="fail",
            blocking=[str(exc)],
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
        blocking_extra=audit_blocking,
        warnings_extra=audit_warnings,
    )
    verdict.input_sha256 = _sha256(path)
    verdict.validator_version = (
        f"audit-registry-v{_AUDIT_REGISTRY.version} "
        f"(route-manifest-v{_ROUTE_REGISTRY.version})"
    )
    return verdict


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
    )

    if args.json:
        print(_verdict_to_json(verdict))
    else:
        output = format_verdict(verdict)
        print(output)

    return verdict.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
