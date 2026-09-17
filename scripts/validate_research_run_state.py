#!/usr/bin/env python3
"""Fail-closed validator for the Research Run State contract (issue #417, #426).

Run State records process phase, run overlay, artifact identity, and
checkpoints for long / multi-track / explicit-resume research. It is not a
second interpretation of Research Pack ``research_status``, Final audit
status, or ``delivery_status``. Issue #426: no byte-hash binding; binding is
by run_id / artifact_id / handoff_id / path / route / validator.

Single-track research does not create a Run State and never invokes this
validator unless the user explicitly resumes a previous ``run_id``.

Exit codes:
    0 = snapshot (and optional transition / resume / chain) is valid
    2 = fail closed

Usage:
    python3 scripts/validate_research_run_state.py <run-state.json> [--json]
    python3 scripts/validate_research_run_state.py --from prev.json --to next.json \\
        [--audit-result audit.json] [--artifact pack.md] [--report report.md] [--json]
        # phase=delivered requires --audit-result, --artifact (Pack), and --report
    python3 scripts/validate_research_run_state.py <run-state.json> \\
        --resume --artifact <pack.md> --activation-snapshot snap.json [--json]
    python3 scripts/validate_research_run_state.py --chain \\
        --handoff h1.json [--handoff h2.json ...] --run-state r.json --pack p.md \\
        [--report report.md] [--audit-result a.json] \\
        [--claim-alignment-bundle bundle.json] [--json]
        # --chain requires Pack ## Run state to name the same sidecar file;
        # every listed handoff_refs entry must be supplied via --handoff
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

from activation_snapshot import (
    ActivationSnapshotError,
    extract_activation_snapshot_reference,
    load_activation_snapshot,
    validate_activation_reference,
)

SCHEMA_VERSION = "2"
EXIT_OK = 0
EXIT_FAIL_CLOSED = 2

PHASES = (
    "intake",
    "route_locked",
    "collecting",
    "mid_review",
    "synthesizing",
    "auditing",
    "delivered",
)
STATUSES = (
    "in_progress",
    "paused",
    "partial",
    "blocked",
    "completed",
    "aborted",
)
ENABLED_REASONS = ("parallel", "explicit_resume")
TERMINAL_STATUSES = frozenset({"completed", "aborted"})
MID_REVIEW_DECISIONS = frozenset(
    {"continue", "narrow", "pivot", "stop-and-synthesize"}
)
PENDING_DECISIONS = MID_REVIEW_DECISIONS | {"confirm-boundary", "confirm-delivery"}
HANDOFF_REQUIRED_PHASES = frozenset({"synthesizing", "auditing", "delivered"})
PARTIAL_PHASES = frozenset({"collecting", "synthesizing"})
BLOCKED_PHASES = frozenset({"collecting", "auditing"})

LEGAL_COMBINATIONS = frozenset(
    {
        ("intake", "in_progress"),
        ("intake", "paused"),
        ("intake", "aborted"),
        ("route_locked", "in_progress"),
        ("route_locked", "paused"),
        ("route_locked", "aborted"),
        ("collecting", "in_progress"),
        ("collecting", "paused"),
        ("collecting", "partial"),
        ("collecting", "blocked"),
        ("collecting", "aborted"),
        ("mid_review", "in_progress"),
        ("mid_review", "paused"),
        ("mid_review", "aborted"),
        ("synthesizing", "in_progress"),
        ("synthesizing", "paused"),
        ("synthesizing", "partial"),
        ("synthesizing", "aborted"),
        ("auditing", "in_progress"),
        ("auditing", "paused"),
        ("auditing", "blocked"),
        ("auditing", "aborted"),
        ("delivered", "completed"),
    }
)

REQUIRED_TOP_LEVEL = frozenset(
    {
        "schema_version",
        "run_id",
        "artifact_id",
        "phase",
        "status",
        "activation_reference",
        "pending_decision",
        "last_transition_reason",
        "updated_at",
        "enabled_reason",
    }
)
OPTIONAL_TOP_LEVEL = frozenset(
    {
        "parent_artifact_id",
        "status_reason",
        "recovery_action",
        "next_action",
        "handoff_refs",
    }
)
KNOWN_TOP_LEVEL = REQUIRED_TOP_LEVEL | OPTIONAL_TOP_LEVEL
HANDOFF_REF_REQUIRED = frozenset({"handoff_id"})

_TIMESTAMP_RE = re.compile(
    r"^(\d{4}-\d{2}-\d{2})"
    r"(?:[Tt](\d{2}:\d{2}(?::\d{2}(?:\.\d+)?))([Zz]|[+-]\d{2}:\d{2})?)?$"
)

STABLE_IDENTITY_FIELDS = (
    "run_id",
    "artifact_id",
    "enabled_reason",
    "schema_version",
)


def _is_non_empty_str(value: object) -> bool:
    return isinstance(value, str) and value.strip() != ""


def _is_valid_timestamp(value: object) -> bool:
    if not isinstance(value, str):
        return False
    match = _TIMESTAMP_RE.match(value)
    if not match:
        return False
    date_part, time_part, zone_part = match.groups()
    try:
        if time_part is None:
            date.fromisoformat(date_part)
            return True
        zone = (zone_part or "").replace("z", "Z").replace("Z", "+00:00")
        dt = datetime.fromisoformat(f"{date_part}T{time_part}{zone}")
    except ValueError:
        return False
    return dt.tzinfo is not None


def _phase_index(phase: str) -> int:
    return PHASES.index(phase)


def validate_run_state_data(data: object) -> list[str]:
    """校验单个 Run State 快照。空列表表示通过。"""
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["run state must be a JSON object"]

    unknown = sorted(set(data) - KNOWN_TOP_LEVEL)
    if unknown:
        errors.append(f"unknown additional top-level field(s): {unknown}")

    missing = sorted(REQUIRED_TOP_LEVEL - set(data))
    for field in missing:
        errors.append(f"missing required field '{field}'")

    if data.get("schema_version") != SCHEMA_VERSION:
        errors.append(
            f"schema_version must be {SCHEMA_VERSION!r}, got "
            f"{data.get('schema_version')!r}"
        )

    for field in ("run_id", "artifact_id", "last_transition_reason"):
        if field in data and not _is_non_empty_str(data[field]):
            errors.append(f"'{field}' must be a non-empty string")

    phase = data.get("phase")
    if not isinstance(phase, str) or phase not in PHASES:
        errors.append(f"'phase' must be one of {list(PHASES)}, got {phase!r}")
        phase = None
    status = data.get("status")
    if not isinstance(status, str) or status not in STATUSES:
        errors.append(f"'status' must be one of {list(STATUSES)}, got {status!r}")
        status = None
    if phase is not None and status is not None:
        if (phase, status) not in LEGAL_COMBINATIONS:
            errors.append(
                f"illegal (phase, status) combination: ({phase!r}, {status!r})"
            )

    enabled = data.get("enabled_reason")
    if not isinstance(enabled, str) or enabled not in ENABLED_REASONS:
        errors.append(
            f"'enabled_reason' must be one of {list(ENABLED_REASONS)}, "
            f"got {enabled!r}"
        )

    if "parent_artifact_id" in data and not _is_non_empty_str(
        data.get("parent_artifact_id")
    ):
        errors.append("'parent_artifact_id' must be a non-empty string when present")
    if "next_action" in data and not _is_non_empty_str(data.get("next_action")):
        errors.append("'next_action' must be a non-empty string when present")

    if status in {"partial", "blocked"} and not _is_non_empty_str(
        data.get("status_reason")
    ):
        errors.append(f"'{status}' status requires a non-empty 'status_reason'")
    if status == "blocked" and not _is_non_empty_str(data.get("recovery_action")):
        errors.append("'blocked' status requires a non-empty 'recovery_action'")
    for field in ("status_reason", "recovery_action"):
        if field in data and not _is_non_empty_str(data[field]):
            errors.append(f"'{field}' must be a non-empty string when present")

    if "updated_at" in data and not _is_valid_timestamp(data["updated_at"]):
        errors.append(
            "'updated_at' must be an ISO-8601 date or a timezone-aware "
            f"RFC 3339 timestamp, got {data.get('updated_at')!r}"
        )

    pending = data.get("pending_decision")
    if pending is not None and pending not in PENDING_DECISIONS:
        errors.append(
            f"'pending_decision' must be null or one of {sorted(PENDING_DECISIONS)}, "
            f"got {pending!r}"
        )
    if (
        phase == "mid_review"
        and status in {"in_progress", "paused"}
        and pending not in MID_REVIEW_DECISIONS
    ):
        errors.append(
            "mid_review requires pending_decision in "
            f"{sorted(MID_REVIEW_DECISIONS)}"
        )
    if phase == "delivered" and pending is not None:
        errors.append("delivered requires pending_decision to be null (consumed)")
    if phase == "delivered" and status not in {None, "completed"}:
        errors.append("delivered requires status=completed")

    try:
        validate_activation_reference(
            data.get("activation_reference"),
            label="activation_reference",
        )
    except ActivationSnapshotError as exc:
        errors.append(str(exc))

    handoff_refs = data.get("handoff_refs")
    if "handoff_refs" in data:
        if not isinstance(handoff_refs, list):
            errors.append("'handoff_refs' must be a list")
            handoff_refs = None
        else:
            seen_ids: set[str] = set()
            for index, item in enumerate(handoff_refs):
                if not isinstance(item, dict):
                    errors.append(f"handoff_refs[{index}] must be an object")
                    continue
                extra = sorted(set(item) - HANDOFF_REF_REQUIRED)
                if extra:
                    errors.append(
                        f"unknown additional handoff_refs field(s): {extra}"
                    )
                hid = item.get("handoff_id")
                if not _is_non_empty_str(hid):
                    errors.append(
                        f"handoff_refs[{index}].handoff_id must be a non-empty string"
                    )
                elif hid in seen_ids:
                    errors.append(f"duplicate handoff_id in handoff_refs: {hid!r}")
                else:
                    seen_ids.add(hid)

    if (
        enabled == "parallel"
        and phase in HANDOFF_REQUIRED_PHASES
        and not (isinstance(handoff_refs, list) and handoff_refs)
    ):
        errors.append(
            "enabled_reason=parallel and phase "
            f"{phase!r} require a non-empty handoff_refs list"
        )
    if enabled == "explicit_resume" and handoff_refs:
        errors.append(
            "enabled_reason=explicit_resume must not carry handoff_refs "
            "(single-track creates no Track Handoffs)"
        )

    return errors


def validate_transition(before: object, after: object) -> list[str]:
    """校验一次合法/非法转移。两端都必须先是合法快照。"""
    errors = validate_run_state_data(before)
    errors.extend(
        f"after: {item}" for item in validate_run_state_data(after)
    )
    if errors:
        return errors
    assert isinstance(before, dict) and isinstance(after, dict)

    for field in STABLE_IDENTITY_FIELDS:
        if before.get(field) != after.get(field):
            errors.append(
                f"transition must not change {field}: "
                f"{before.get(field)!r} -> {after.get(field)!r}"
            )
    if before.get("activation_reference") != after.get("activation_reference"):
        errors.append(
            "transition must not change activation_reference; start a new run_id"
        )
    if before.get("parent_artifact_id") != after.get("parent_artifact_id"):
        errors.append("transition must not change parent_artifact_id")

    from_status = before["status"]
    to_status = after["status"]
    from_phase = before["phase"]
    to_phase = after["phase"]
    from_idx = _phase_index(from_phase)
    to_idx = _phase_index(to_phase)

    if from_status in TERMINAL_STATUSES:
        if before != after:
            errors.append(
                f"terminal status {from_status!r} cannot transition "
                f"to ({to_phase!r}, {to_status!r})"
            )
        return errors

    if to_idx == from_idx:
        allowed_same = _allowed_same_phase_status(from_phase, from_status, to_status)
        if not allowed_same:
            errors.append(
                f"illegal same-phase status transfer: "
                f"{from_status!r} -> {to_status!r} at phase {from_phase!r}"
            )
        return errors

    if from_phase == "auditing" and to_phase == "synthesizing":
        if to_status != "in_progress":
            errors.append("audit-fail repair must return to synthesizing/in_progress")
        if from_status not in {"in_progress", "blocked"}:
            errors.append(
                "only in_progress or blocked auditing may return to synthesizing"
            )
        errors.extend(_pending_decision_must_be_consumed(before, after))
        return errors

    if to_idx != from_idx + 1:
        errors.append(
            f"illegal phase skip or regression: {from_phase!r} -> {to_phase!r}"
        )
        return errors

    if from_status == "paused":
        errors.append("paused runs must resume to in_progress before advancing phase")
    if from_status == "blocked":
        errors.append("blocked runs must recover to in_progress before advancing phase")
    if from_status not in {"in_progress", "partial"}:
        errors.append(
            f"cannot advance phase from status {from_status!r}"
        )
    if from_status == "partial" and from_phase not in PARTIAL_PHASES:
        errors.append(f"partial cannot advance from phase {from_phase!r}")

    expected_to_status = "completed" if to_phase == "delivered" else "in_progress"
    if to_status != expected_to_status:
        errors.append(
            f"advancing to {to_phase!r} requires status={expected_to_status!r}, "
            f"got {to_status!r}"
        )
    if to_phase == "delivered" and from_phase != "auditing":
        errors.append("delivered can only be entered from auditing")
    errors.extend(_pending_decision_must_be_consumed(before, after))

    return errors


def _pending_decision_must_be_consumed(before: dict, after: dict) -> list[str]:
    """推进 phase 前必须消费未决 checkpoint，不能把 pending_decision 原样带走。"""
    pending = before.get("pending_decision")
    if pending is None:
        return []
    if after.get("pending_decision") is not None:
        return [
            f"pending_decision {pending!r} must be consumed (set to null) "
            f"before advancing {before['phase']!r} -> {after['phase']!r}"
        ]
    return []


def _allowed_same_phase_status(phase: str, from_status: str, to_status: str) -> bool:
    if from_status == to_status:
        return True
    if to_status == "aborted":
        return from_status not in TERMINAL_STATUSES
    if from_status == "in_progress" and to_status == "paused":
        return True
    if from_status == "paused" and to_status == "in_progress":
        return True
    if from_status == "in_progress" and to_status == "partial":
        return phase in PARTIAL_PHASES
    if from_status == "in_progress" and to_status == "blocked":
        return phase in BLOCKED_PHASES
    if from_status == "partial" and to_status == "in_progress":
        return phase in PARTIAL_PHASES
    if from_status == "blocked" and to_status == "in_progress":
        return phase in BLOCKED_PHASES
    return False


def load_run_state_file(path: Path | str) -> tuple[dict | None, list[str]]:
    path = Path(path)
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return None, [f"cannot read run state file {path}: {exc}"]
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        return None, [f"run state file {path} is not valid JSON: {exc}"]
    errors = validate_run_state_data(data)
    if errors:
        return None, [f"{path}: {item}" for item in errors]
    assert isinstance(data, dict)
    return data, []


def _delivered_forbidden_audit_status(
    audit_id: str,
    status: str,
    reason: str | None = None,
    *,
    require_opt_in_binding: bool = False,
) -> bool:
    """Whether an audit status blocks phase=delivered (#419 default-off exempt only)."""
    if status not in DELIVERED_FORBIDDEN_AUDIT_STATUSES:
        return False
    if status == "not_run":
        try:
            from opt_in_audit_contract import audit_not_run_is_consumer_exempt
            from registry_loader import load_audit_registry

            if audit_not_run_is_consumer_exempt(
                {"audit_id": audit_id, "status": status, "reason": reason},
                load_audit_registry().opt_in_audit_ids(),
                require_opt_in_binding=require_opt_in_binding,
            ):
                return False
        except Exception:
            return True
    return True


PACK_PROVENANCE_KINDS = frozenset({"pack_section", "pack_table"})
DELIVERED_FORBIDDEN_AUDIT_STATUSES = frozenset(
    {"not_run", "skipped", "partial", "fail"}
)
KNOWN_AUDIT_STATUSES = frozenset(
    {"pass", "conditional-pass", "fail", "not_run", "skipped", "partial"}
)


def _canonical_audit_helpers():
    """Lazy-import canonical audit JSON checks; None on ImportError."""
    try:
        from run_forward_evals import (
            EXPECTED_AUDIT_JSON_SCHEMA_VERSION,
            _audit_consistency_details,
            _expected_audit_set,
            _overall_consistency_details,
            _validators_ok,
        )
    except ImportError:
        return 1, None, None, None, None
    return (
        EXPECTED_AUDIT_JSON_SCHEMA_VERSION,
        _overall_consistency_details,
        _audit_consistency_details,
        _expected_audit_set,
        _validators_ok,
    )


def _quiet_resolve_route(name: str | None) -> str | None:
    if not isinstance(name, str) or not name.strip():
        return None
    try:
        from registry_loader import RegistryError, load_route_registry

        return load_route_registry().resolve_route(name.strip())
    except (RegistryError, OSError, ImportError):
        return None


def _registry_error_types() -> tuple[type[BaseException], ...]:
    """Registry / parse failures delivered must surface as structured errors."""
    try:
        from registry_loader import RegistryError
    except ImportError:  # pragma: no cover - standalone import guard
        return (OSError, ValueError)
    return (RegistryError, OSError, ValueError)


def _read_artifact_text(
    path: Path | str,
    label: str,
) -> tuple[str | None, str | None, list[str]]:
    """Read an artifact once: raw text plus canonical visible text.

    The raw text keeps the ```contract fence intact for canonical contract
    extraction; the visible text is the sanitized body used to resolve
    evidence locators (issue #434 B3: fenced/HTML-hidden headings and tables
    must not count as evidence).
    """
    try:
        raw = Path(path).read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return None, None, [f"cannot read {label} {path}: {exc}"]
    try:
        from validate_contract import sanitize_visible_markdown
    except ImportError:
        return raw, None, ["cannot load canonical visible-Markdown sanitizer"]
    return raw, sanitize_visible_markdown(raw), []


def _report_route_declaration(visible_report: str | None) -> tuple[str | None, list[str]]:
    """Issue #434 B1: re-read the visible report route declaration.

    Reuses the canonical producer parser with ``unknown_route_is_error`` so a
    post-audit edit of the ``## Route and audit status`` block cannot disagree
    with the contract, Pack, or audit result route unnoticed.
    """
    if visible_report is None:
        return None, []
    try:
        from validate_contract import extract_report_route_declaration
    except ImportError:
        return None, ["cannot load canonical report route parser"]
    route, malformed = extract_report_route_declaration(
        visible_report, unknown_route_is_error=True
    )
    return route, [f"delivered {item}" for item in malformed]


def _pack_declarations(
    pack_path: Path | str,
    visible_pack: str | None,
) -> tuple[str | None, str | None, dict | None, list[str]]:
    """Issue #434 B1: canonical Pack route / artifact id / activation snapshot.

    Reuses the same parsers as the ``audit_report`` producer: duplicate
    ``## Primary route`` / ``## Artifact id`` sections are structural errors
    (``validate_pack_sections``), an unresolvable route fails closed instead
    of falling back to the first declaration, and the ``## Activation
    snapshot`` reference is re-read from the visible Pack body.
    """
    try:
        from validate_contract import (
            _extract_pack_artifact_id,
            _resolve_pack_primary_route,
            validate_pack_sections,
        )
    except ImportError:
        return None, None, None, ["cannot load canonical Research Pack parsers"]
    section_errors = validate_pack_sections(str(pack_path))
    if section_errors:
        return None, None, None, section_errors
    errors: list[str] = []
    pack_route = _resolve_pack_primary_route(str(pack_path))
    if pack_route is None:
        errors.append(
            f"Research Pack {pack_path} '## Primary route' cannot be resolved "
            "to a canonical route — fix the pack declaration"
        )
    pack_artifact_id = _extract_pack_artifact_id(str(pack_path))
    snapshot = None
    if visible_pack is not None:
        snapshot, snapshot_errors = extract_activation_snapshot_reference(
            visible_pack, label="Research Pack"
        )
        errors.extend(snapshot_errors)
    return pack_route, pack_artifact_id, snapshot, errors


def _activation_reference_errors(run_state: dict, pack_snapshot: dict) -> list[str]:
    """Issue #434: Run State activation_reference must match the Pack snapshot."""
    reference = run_state.get("activation_reference")
    if not isinstance(reference, dict):
        return []
    errors: list[str] = []
    for field in ("activation_id", "snapshot_version", "decision_tree_version"):
        if reference.get(field) != pack_snapshot.get(field):
            errors.append(
                "Run State activation_reference does not match the Research "
                f"Pack activation_snapshot: {field} "
                f"{reference.get(field)!r} != {pack_snapshot.get(field)!r}"
            )
    return errors


def _validated_delivered_contract(
    raw_report: str | None,
    visible_report: str | None,
    *,
    report_supplied: bool,
    pack_provided: bool,
    report_primary_route: str | None,
    pack_artifact_id: str | None,
    pack_activation_snapshot: dict | None,
) -> tuple[dict | None, list[str]]:
    """Issue #434 B1: the report contract must be single, canonical and complete.

    ``extract_contract_from_markdown()`` parsing success is not contract
    validity.  The delivered consumer runs the same canonical
    ``validate_contract()`` boundary the ``audit_report`` producer runs
    (report status route, Pack artifact id, Pack activation snapshot) against
    the visible report body, before any expected audit id is derived.
    ``strict=True`` mirrors ``validate_contract.py --require-contract
    --strict``; the remaining warnings are blocking too, so a post-audit edit
    that drops the contract's stable identity fields cannot pass delivered.
    Route agreement with the Pack/audit result stays in
    ``_derive_expected_audit_ids`` (single locatable error per mismatch).
    """
    if not report_supplied or raw_report is None:
        return None, []
    try:
        from validate_contract import (
            PROJECT_ROOT,
            extract_contract_blocks,
            validate_contract,
        )
    except ImportError:
        return None, ["cannot load canonical contract validator"]
    contracts, contract_errors = extract_contract_blocks(raw_report)
    if contract_errors:
        return None, [f"delivered report contract: {item}" for item in contract_errors]
    if not contracts:
        return None, [
            "phase=delivered requires a route activation contract in --report"
        ]
    contract = contracts[0]
    try:
        result = validate_contract(
            contract,
            report_primary_route=report_primary_route,
            pack_artifact_id=pack_artifact_id,
            pack_activation_snapshot=pack_activation_snapshot,
            research_pack_provided=pack_provided,
            strict=True,
            report_text=visible_report,
            evidence_base_dir=PROJECT_ROOT,
        )
    except _registry_error_types() as exc:
        return contract, [f"delivered report contract validation failed: {exc}"]
    problems = [
        *result.errors,
        *(f"warning: {item}" for item in result.warnings),
    ]
    return contract, [f"delivered report contract: {item}" for item in problems]


def _derive_expected_audit_ids(
    audit: dict,
    *,
    contract: dict | None,
    contract_errors: list[str],
    report_supplied: bool,
    pack_route: str | None,
    expected_set_fn,
) -> tuple[list[str] | None, str | None, list[str]]:
    """从 canonical contract / route registry 外算完整 expected audit set。

    不信任 payload 自己的 audits[] 列表。contract 已经过
    ``_validated_delivered_contract`` 边界（errors 与 warnings 都已阻断），
    这里只消费其 canonical ``primary_route`` / ``secondary_routes``，不重复
    解释 contract 语义（issue #434 review）。顶层 ``route`` 必须存在并与
    报告 contract / Pack 一致。
    """
    errors = list(contract_errors)
    contract_route = None
    secondaries: list[str] = []
    if report_supplied:
        if contract is None or errors:
            return None, None, errors
        raw_primary = contract.get("primary_route")
        if isinstance(raw_primary, str) and raw_primary.strip():
            contract_route = raw_primary.strip()
        else:
            errors.append(
                "delivered report contract requires a non-empty primary_route"
            )
        raw_secondaries = contract.get("secondary_routes")
        if isinstance(raw_secondaries, list):
            secondaries = [
                item.strip()
                for item in raw_secondaries
                if isinstance(item, str) and item.strip()
            ]
        else:
            errors.append(
                "delivered report contract secondary_routes must be an array"
            )
        if errors:
            return None, contract_route, errors

    raw_audit_route = audit.get("route")
    if not isinstance(raw_audit_route, str) or not raw_audit_route.strip():
        errors.append("audit result requires top-level route")
        audit_route = None
    else:
        audit_route = _quiet_resolve_route(raw_audit_route)
        if audit_route is None:
            errors.append(
                f"audit result route {raw_audit_route!r} is not a canonical route"
            )

    route = contract_route or pack_route or audit_route
    if route is None:
        if not errors:
            errors.append(
                "phase=delivered cannot derive the expected audit set: "
                "need a primary route from the report contract or Research Pack"
            )
        return None, None, errors

    for label, other in (
        ("report contract", contract_route),
        ("Research Pack", pack_route),
        ("audit result", audit_route),
    ):
        if other is not None and other != route:
            errors.append(
                f"delivered route mismatch: using {route!r} but {label} "
                f"declares {other!r}"
            )

    if errors:
        return None, route, errors

    if expected_set_fn is None:
        errors.append("cannot load canonical expected audit set helper")
        return None, route, errors
    try:
        expected = expected_set_fn(route, secondaries)
    except _registry_error_types() as exc:
        errors.append(
            f"cannot derive expected audit set for route {route!r}: {exc}"
        )
        return None, route, errors
    if expected is None:
        errors.append(
            f"cannot derive expected audit set for route {route!r} "
            "(registry drift)"
        )
        return None, route, errors
    return expected, route, errors


def _delivered_validator_errors(
    audit: dict,
    *,
    route: str | None,
    report_path: Path | str | None,
    validators_ok_fn,
) -> list[str]:
    """复用 canonical ``_validators_ok``，用外部 route / 报告 path 绑定。"""
    errors: list[str] = []
    validators = audit.get("validators")
    if not isinstance(validators, list) or not validators:
        return ["audit result requires a non-empty validators list"]
    if route is None:
        return ["cannot bind validators[] without a resolved route"]
    try:
        from registry_loader import UnknownRouteError, load_route_registry

        expected = load_route_registry().validators_for(route)
    except (UnknownRouteError, OSError, ImportError) as exc:
        return [f"cannot load canonical validator set for route {route!r}: {exc}"]

    audited_path = str(report_path) if report_path is not None else None
    recorded = [
        str(item.get("validator_id"))
        for item in validators
        if isinstance(item, dict)
    ]
    if recorded != expected:
        errors.append(
            f"validators[] does not match the canonical set for route {route!r}: "
            f"got {recorded}, expected {expected}"
        )
    if validators_ok_fn is None:
        if not errors:
            errors.append("cannot load canonical validators[] helper")
        return errors
    if not validators_ok_fn(
        audit,
        expected,
        audited_path=audited_path,
    ):
        if not errors:
            errors.append(
                "validators[] failed canonical binding (status, provenance, "
                "report path, or validator_version)"
            )
    return errors


def _provenance_binding_errors(entry: dict) -> list[str]:
    """pass / conditional-pass 的 verified provenance 必须携带绑定字段。"""
    status = entry.get("status")
    if status not in {"pass", "conditional-pass"}:
        return []
    audit_id = entry.get("audit_id")
    provenance = entry.get("evidence_provenance")
    if not isinstance(provenance, list) or not provenance:
        return [
            f"audit {audit_id!r} {status} requires verified evidence_provenance"
        ]
    verified = [
        item
        for item in provenance
        if isinstance(item, dict) and item.get("verified") is True
    ]
    if not verified:
        return [
            f"audit {audit_id!r} {status} requires verified evidence_provenance"
        ]
    errors: list[str] = []
    for record in verified:
        if not _is_non_empty_str(record.get("execution_source")):
            errors.append(
                f"audit {audit_id!r} provenance requires execution_source"
            )
    return errors


def _malformed_audit_entry_errors(entry: object) -> list[str]:
    """Fallback 结构校验：在无法导入 canonical helper 时仍 fail closed。"""
    if not isinstance(entry, dict):
        return ["audit result audits entries must be objects"]
    errors: list[str] = []
    audit_id = entry.get("audit_id")
    if not _is_non_empty_str(audit_id):
        errors.append("audit entry requires audit_id")
    status = entry.get("status")
    if not isinstance(status, str) or status not in KNOWN_AUDIT_STATUSES:
        errors.append(
            f"audit {audit_id!r} unknown or missing status {status!r}"
        )
        return errors
    if status == "conditional-pass":
        warnings = entry.get("warnings")
        if not isinstance(warnings, list) or not warnings:
            errors.append(
                f"audit {audit_id!r} conditional-pass requires warnings"
            )
    return errors


def check_audit_result_for_delivered(
    audit: object,
    run_state: dict,
    *,
    report_path: Path | str | None = None,
    pack_path: Path | str | None = None,
    claim_alignment_bundle_path: Path | str | None = None,
    require_opt_in_binding: bool = False,
) -> list[str]:
    """delivered 不能由未执行、空集、畸形或失败的审计支撑。

    Issue #426: 绑定是显式路径/ID/route/validator/状态，不做字节 hash
    比较；报告与 Pack 也只做路径存在与流程门禁，不互相冒充。
    Issue #434: report contract 走 canonical ``validate_contract()`` 边界，
    并重验可见 report route declaration、Pack ``## Primary route`` /
    ``## Artifact id`` 基数与 Pack ``## Activation snapshot``（与
    activation_reference 对齐）；expected audit set 只从 canonical
    route/contract 派生；report/Pack evidence locator 对可见正文重新定位；
    registry/parse 失败返回结构化 delivered 错误而不是 traceback。
    """
    require_opt_in_binding = (
        require_opt_in_binding or claim_alignment_bundle_path is not None
    )
    if not isinstance(audit, dict):
        return ["audit result must be a JSON object"]
    errors: list[str] = []
    (
        schema_version,
        overall_details,
        audit_details,
        expected_set_fn,
        validators_ok_fn,
    ) = _canonical_audit_helpers()

    # Issue #434: read report/Pack once; raw text keeps the contract fence,
    # visible text is what evidence locators must resolve against.
    raw_report = visible_report = None
    if report_path is not None:
        raw_report, visible_report, read_errors = _read_artifact_text(
            report_path, "report"
        )
        errors.extend(read_errors)
    raw_pack = visible_pack = None
    if pack_path is not None:
        raw_pack, visible_pack, read_errors = _read_artifact_text(
            pack_path, "Research Pack"
        )
        errors.extend(read_errors)

    report_route, route_errors = _report_route_declaration(visible_report)
    errors.extend(route_errors)

    pack_route = None
    pack_artifact_id = None
    pack_snapshot = None
    pack_provided = pack_path is not None and raw_pack is not None
    if pack_provided:
        (
            pack_route,
            pack_artifact_id,
            pack_snapshot,
            pack_errors,
        ) = _pack_declarations(pack_path, visible_pack)
        errors.extend(pack_errors)
        if pack_snapshot is not None:
            errors.extend(_activation_reference_errors(run_state, pack_snapshot))

    contract, contract_errors = _validated_delivered_contract(
        raw_report,
        visible_report,
        report_supplied=report_path is not None,
        pack_provided=pack_provided,
        report_primary_route=report_route,
        pack_artifact_id=pack_artifact_id,
        pack_activation_snapshot=pack_snapshot,
    )

    if audit.get("schema_version") != schema_version:
        errors.append(
            f"audit result schema_version must be {schema_version}, "
            f"got {audit.get('schema_version')!r}"
        )
    overall = audit.get("overall")
    if overall == "fail":
        errors.append(
            "audit overall=fail cannot support phase=delivered; "
            "return to synthesizing and re-audit"
        )
    elif overall not in {"pass", "conditional-pass"}:
        errors.append(
            f"audit overall {overall!r} cannot support phase=delivered"
        )

    if "exit_code" not in audit:
        errors.append("audit result requires exit_code")
    elif overall_details is not None:
        _ok, overall_errors = overall_details(
            audit,
            audit.get("exit_code"),
            require_opt_in_binding=require_opt_in_binding,
        )
        errors.extend(overall_errors)
    else:
        expected_rc = {"pass": 0, "conditional-pass": 1, "fail": 2}.get(overall)
        if expected_rc is not None and audit.get("exit_code") != expected_rc:
            errors.append(
                f"exit_code {audit.get('exit_code')!r} does not match overall "
                f"{overall!r} (expected {expected_rc})"
            )

    audits = audit.get("audits")
    if not isinstance(audits, list) or not audits:
        errors.append("audit result requires a non-empty audits list")
        audits = []

    present_ids = [
        str(item.get("audit_id"))
        for item in audits
        if isinstance(item, dict) and item.get("audit_id")
    ]
    expected_ids, route, expected_errors = _derive_expected_audit_ids(
        audit,
        contract=contract,
        contract_errors=contract_errors,
        report_supplied=report_path is not None,
        pack_route=pack_route,
        expected_set_fn=expected_set_fn,
    )
    errors.extend(expected_errors)
    if expected_ids is None:
        expected_ids = []
        if not expected_errors:
            errors.append(
                "phase=delivered cannot derive the expected audit set"
            )
    elif set(present_ids) != set(expected_ids) and audit_details is None:
        missing = sorted(set(expected_ids) - set(present_ids))
        extra = sorted(set(present_ids) - set(expected_ids))
        if missing:
            errors.append(f"missing required audit(s): {', '.join(missing)}")
        if extra:
            errors.append(f"unknown/forged audit(s): {', '.join(extra)}")
    if audit_details is not None:
        _ok, entry_errors = audit_details(
            audit,
            expected_ids,
            audited_path=str(report_path) if report_path is not None else None,
            research_pack_path=str(pack_path) if pack_path is not None else None,
            report_text=visible_report,
            pack_text=visible_pack,
            expected_route=route,
            claim_alignment_bundle_path=(
                str(claim_alignment_bundle_path)
                if claim_alignment_bundle_path is not None
                else None
            ),
            require_opt_in_binding=require_opt_in_binding,
        )
        errors.extend(entry_errors)
    else:
        for entry in audits:
            errors.extend(_malformed_audit_entry_errors(entry))

    errors.extend(
        _delivered_validator_errors(
            audit,
            route=route,
            report_path=report_path,
            validators_ok_fn=validators_ok_fn,
        )
    )

    for entry in audits:
        if not isinstance(entry, dict):
            if audit_details is None:
                errors.append("audit result audits entries must be objects")
            continue
        status = entry.get("status")
        audit_id = entry.get("audit_id")
        if not _is_non_empty_str(audit_id) and audit_details is not None:
            errors.append("audit entry requires audit_id")
        if _delivered_forbidden_audit_status(
            str(audit_id),
            str(status),
            entry.get("reason") if isinstance(entry.get("reason"), str) else None,
            require_opt_in_binding=require_opt_in_binding,
        ):
            errors.append(
                f"audit {audit_id!r} status {status!r} cannot support "
                "phase=delivered"
            )
        errors.extend(_provenance_binding_errors(entry))

    if overall == "conditional-pass" and not _is_non_empty_str(
        run_state.get("last_transition_reason")
    ):
        errors.append(
            "conditional-pass delivery requires last_transition_reason "
            "recording explicit confirmation"
        )
    return errors


def require_delivered_audit(
    state: dict,
    audit_result_path: Path | str | None,
    *,
    artifact_path: Path | str | None = None,
    report_path: Path | str | None = None,
    claim_alignment_bundle_path: Path | str | None = None,
    require_opt_in_binding: bool = False,
) -> list[str]:
    """CLI 进入/保持 delivered 时必须绑定报告审计与 Pack 过程工件。"""
    require_opt_in_binding = (
        require_opt_in_binding or claim_alignment_bundle_path is not None
    )
    if audit_result_path is None:
        return [
            "phase=delivered requires --audit-result; "
            "unexecuted audit cannot enter delivered"
        ]
    if artifact_path is None:
        return [
            "phase=delivered requires --artifact (Research Pack) so "
            "artifact_id binds to the process artifact"
        ]
    if report_path is None:
        return [
            "phase=delivered requires --report so audit "
            "binds to the actual report, not the Pack"
        ]
    audit, errors = _load_json_object(audit_result_path, "audit result")
    if errors:
        return errors
    err = _unreadable_error("artifact", artifact_path)
    if err is not None:
        return [err]
    err = _unreadable_error("report", report_path)
    if err is not None:
        return [err]
    assert audit is not None
    return check_audit_result_for_delivered(
        audit,
        state,
        report_path=report_path,
        pack_path=artifact_path,
        claim_alignment_bundle_path=claim_alignment_bundle_path,
        require_opt_in_binding=require_opt_in_binding,
    )


def _unreadable_error(label: str, path: Path | str) -> str | None:
    """Cheap readability probe: open without loading content.

    Issue #426 review cleanup: resume/delivered only needs to know the
    artifact is readable, so avoid a full-file read of large Packs/reports.
    """
    try:
        with open(path, "rb"):
            pass
    except OSError as exc:
        return f"cannot read {label} {path}: {exc}"
    return None


def _load_json_object(path: Path | str, label: str) -> tuple[dict | None, list[str]]:
    path = Path(path)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        return None, [f"cannot read {label} {path}: {exc}"]
    except json.JSONDecodeError as exc:
        return None, [f"{label} {path} is not valid JSON: {exc}"]
    if not isinstance(data, dict):
        return None, [f"{label} must be a JSON object"]
    return data, []


def check_resume(
    state: dict,
    *,
    artifact_path: Path | str | None = None,
    activation_snapshot_path: Path | str | None = None,
) -> list[str]:
    """恢复时重验 artifact 存在、activation reference、未消费 pending_decision。"""
    errors: list[str] = []
    if artifact_path is not None:
        err = _unreadable_error("resume artifact", artifact_path)
        if err is not None:
            return [err]
    if activation_snapshot_path is not None:
        errors.extend(check_activation_alignment(state, activation_snapshot_path))
    if state["status"] in TERMINAL_STATUSES:
        errors.append(
            f"cannot resume a {state['status']} run; start a new run_id"
        )
    return errors


def check_activation_alignment(
    state: dict, activation_snapshot_path: Path | str
) -> list[str]:
    """核对 activation_reference 与启用门，不把 delivered 当成 resume。"""
    try:
        snapshot = load_activation_snapshot(Path(activation_snapshot_path))
    except (ActivationSnapshotError, OSError) as exc:
        return [f"cannot load activation snapshot: {exc}"]
    errors: list[str] = []
    ref = state["activation_reference"]
    if (
        snapshot.get("activation_id") != ref["activation_id"]
        or snapshot.get("snapshot_version") != ref["snapshot_version"]
        or snapshot.get("decision_tree_version") != ref["decision_tree_version"]
    ):
        errors.append(
            "activation_reference does not match the supplied snapshot"
        )
    decision = snapshot.get("parallelization_decision")
    if state["enabled_reason"] == "parallel" and decision != "parallel":
        errors.append(
            "enabled_reason=parallel requires activation "
            f"parallelization_decision='parallel', got {decision!r}"
        )
    if state["enabled_reason"] == "explicit_resume" and decision == "parallel":
        errors.append(
            "enabled_reason=explicit_resume is for single-track resume; "
            "parallel runs must use enabled_reason=parallel"
        )
    return errors


def bind_handoff_to_run_state(
    handoff: dict,
    run_state: dict,
    *,
    handoff_path: Path | str | None = None,
) -> list[str]:
    """把 Track Handoff 绑到当前 Run State；不改 #416 无 --run-state 时的行为。"""
    if run_state.get("enabled_reason") == "explicit_resume":
        return [
            "enabled_reason=explicit_resume cannot bind a Track Handoff; "
            "single-track resume creates no handoffs"
        ]
    errors: list[str] = []
    artifact_ref = handoff.get("artifact_ref")
    actual_id = (
        artifact_ref.get("artifact_id") if isinstance(artifact_ref, dict) else None
    )
    expected_id = run_state.get("artifact_id")
    if actual_id != expected_id:
        errors.append(
            "artifact binding mismatch under --run-state: expected artifact_id "
            f"{expected_id!r}, got {actual_id!r}"
        )
    hid = handoff.get("handoff_id")
    refs = run_state.get("handoff_refs") or []
    matching = [
        item
        for item in refs
        if isinstance(item, dict) and item.get("handoff_id") == hid
    ]
    if (
        run_state.get("enabled_reason") == "parallel"
        and run_state.get("phase") in HANDOFF_REQUIRED_PHASES
        and not matching
    ):
        errors.append(
            f"handoff_id {hid!r} is not listed in run state handoff_refs"
        )
    if matching and handoff_path is not None:
        err = _unreadable_error("handoff", handoff_path)
        if err is not None:
            errors.append(err)
            return errors
    return errors


def bind_listed_handoffs(
    run_state: dict,
    handoff_paths: list[Path | str],
) -> list[str]:
    """校验 Run State 列出的每一条 handoff，而不是只绑命令行上的第一个文件。"""
    if run_state.get("enabled_reason") == "explicit_resume":
        if handoff_paths:
            return [
                "enabled_reason=explicit_resume cannot bind a Track Handoff; "
                "single-track resume creates no handoffs"
            ]
        return []

    from validate_track_handoff import HandoffIncomplete, load_handoff_for_merge

    errors: list[str] = []
    supplied_ids: set[str] = set()
    for raw in handoff_paths:
        path = Path(raw)
        try:
            handoff = load_handoff_for_merge(path)
        except HandoffIncomplete as exc:
            errors.append(str(exc))
            continue
        hid = handoff.get("handoff_id")
        if isinstance(hid, str) and hid.strip():
            if hid in supplied_ids:
                errors.append(f"duplicate --handoff for handoff_id {hid!r}")
            supplied_ids.add(hid)
        errors.extend(
            bind_handoff_to_run_state(handoff, run_state, handoff_path=path)
        )

    if (
        run_state.get("enabled_reason") == "parallel"
        and run_state.get("phase") in HANDOFF_REQUIRED_PHASES
    ):
        listed = [
            item.get("handoff_id")
            for item in (run_state.get("handoff_refs") or [])
            if isinstance(item, dict) and _is_non_empty_str(item.get("handoff_id"))
        ]
        for hid in listed:
            if hid not in supplied_ids:
                errors.append(
                    f"listed handoff_id {hid!r} was not supplied via --handoff"
                )
    return errors


def parse_pack_run_state_section(cleaned: str) -> tuple[dict | None, list[str]]:
    """解析 Pack 的可选 ``## Run state``。缺省节返回 (None, [])。"""
    heading_re = re.compile(r"^## Run state\s*$", re.MULTILINE)
    count = len(heading_re.findall(cleaned))
    if count == 0:
        return None, []
    if count > 1:
        return None, [f"Duplicate section: '## Run state' appears {count} times"]
    lines = cleaned.split("\n")
    body: list[str] = []
    collecting = False
    for line in lines:
        if re.match(r"^## Run state\s*$", line):
            collecting = True
            continue
        if collecting:
            if re.match(r"^##\s", line):
                break
            body.append(line)
    text = "\n".join(body).strip()
    if not text:
        return None, ["Run state section is present but empty"]
    parsed: dict[str, str] = {}
    for raw in text.split("\n"):
        line = raw.strip()
        line = re.sub(r"^[-*>]+\s+", "", line)
        if not line:
            continue
        if ":" in line:
            key, _, value = line.partition(":")
            parsed[key.strip().lower().replace(" ", "_")] = value.strip()
        elif "run_id" not in parsed:
            parsed["run_id"] = line
    errors: list[str] = []
    if not parsed.get("run_id"):
        errors.append("Run state section missing run_id")
    if not parsed.get("path"):
        errors.append("Run state section missing path to the Run State JSON")
    if errors:
        return None, errors
    return parsed, []


def resolve_declared_run_state_path(
    pack_path: Path | str, cleaned: str | None = None
) -> tuple[dict | None, Path | None, list[str]]:
    """解析 Pack 声明的 sidecar 路径。缺节返回 (None, None, [])。"""
    pack_path = Path(pack_path)
    if cleaned is None:
        try:
            cleaned = pack_path.read_text(encoding="utf-8")
        except OSError as exc:
            return None, None, [f"cannot read Research Pack {pack_path}: {exc}"]
    ref, errors = parse_pack_run_state_section(cleaned)
    if errors:
        return None, None, errors
    if ref is None:
        return None, None, []
    sidecar = Path(ref["path"])
    if not sidecar.is_absolute():
        sidecar = pack_path.parent / sidecar
    return ref, sidecar, []


def check_pack_run_state(pack_path: Path | str, cleaned: str | None = None) -> list[str]:
    """Pack 出现 ``## Run state`` 时 fail-closed；缺省节不增加负担。"""
    pack_path = Path(pack_path)
    try:
        text = pack_path.read_text(encoding="utf-8")
    except OSError as exc:
        return [f"cannot read Research Pack {pack_path}: {exc}"]
    if cleaned is None:
        cleaned = text
    ref, sidecar, errors = resolve_declared_run_state_path(pack_path, cleaned)
    if errors:
        return errors
    if ref is None or sidecar is None:
        return []
    state, load_errors = load_run_state_file(sidecar)
    if load_errors:
        return load_errors
    assert state is not None
    if state["run_id"] != ref["run_id"]:
        errors.append(
            f"Run state run_id mismatch: pack declares {ref['run_id']!r}, "
            f"file has {state['run_id']!r}"
        )
    err = _unreadable_error("Research Pack", pack_path)
    if err is not None:
        return [err]
    pack_artifact = _first_pack_section_line(cleaned, "Artifact id")
    if pack_artifact and pack_artifact != state["artifact_id"]:
        errors.append(
            f"Research Pack artifact id {pack_artifact!r} does not match "
            f"run state artifact_id {state['artifact_id']!r}"
        )
    research_status = _first_pack_section_line(cleaned, "Research status")
    errors.extend(_check_status_mapping(state, research_status=research_status))
    return errors


def load_declared_run_state(pack_path: Path | str) -> dict | None:
    """读取 Pack 声明的 Run State 快照；缺节或无法解析时返回 None。"""
    pack_path = Path(pack_path)
    try:
        cleaned = pack_path.read_text(encoding="utf-8")
    except OSError:
        return None
    ref, errors = parse_pack_run_state_section(cleaned)
    if errors or ref is None:
        return None
    sidecar = Path(ref["path"])
    if not sidecar.is_absolute():
        sidecar = pack_path.parent / sidecar
    state, load_errors = load_run_state_file(sidecar)
    if load_errors or state is None:
        return None
    return state


def _first_pack_section_line(cleaned: str, heading: str) -> str | None:
    match = re.search(
        rf"^## {re.escape(heading)}\s*\n(.+?)(?=\n## |\Z)",
        cleaned,
        re.DOTALL | re.MULTILINE,
    )
    if not match:
        return None
    for line in match.group(1).split("\n"):
        line = line.strip()
        if not line:
            continue
        line = re.sub(r"^[-*>]+\s+", "", line)
        return line
    return None


def _check_status_mapping(state: dict, *, research_status: str | None) -> list[str]:
    """禁止 Run State 与 Pack 结果态互相冒充。不交叉强制三层独立性。"""
    errors: list[str] = []
    phase = state["phase"]
    status = state["status"]
    if research_status:
        token = research_status.split()[0].lower()
        if token in {"complete", "partial", "blocked"}:
            if status == "in_progress" and token == "complete" and phase != "delivered":
                errors.append(
                    "research_status=complete cannot pair with an in-progress "
                    f"run at phase {phase!r}"
                )
            if status == "paused" and token == "complete":
                errors.append(
                    "research_status=complete cannot pair with paused run state"
                )
            if (
                status == "completed"
                and token == "blocked"
                and phase == "delivered"
            ):
                errors.append(
                    "run state completed/delivered cannot pair with "
                    "research_status=blocked without an explicit blocked overlay"
                )
    return errors


def validate_chain(
    *,
    handoff_paths: list[Path | str],
    run_state_path: Path | str,
    pack_path: Path | str,
    audit_result_path: Path | str | None = None,
    report_path: Path | str | None = None,
    claim_alignment_bundle_path: Path | str | None = None,
    require_opt_in_binding: bool = False,
) -> list[str]:
    """端到端：列出的全部 Handoff → Run State → Pack → 可选 audit result。"""
    errors: list[str] = []
    state, state_errors = load_run_state_file(run_state_path)
    errors.extend(state_errors)
    ref, sidecar, ref_errors = resolve_declared_run_state_path(pack_path)
    errors.extend(ref_errors)
    if ref is None and not ref_errors:
        errors.append(
            "--chain requires the Research Pack to declare ## Run state"
        )
    elif sidecar is not None:
        try:
            declared = sidecar.resolve()
            supplied = Path(run_state_path).resolve()
        except OSError as exc:
            errors.append(f"cannot resolve run-state paths: {exc}")
        else:
            if declared != supplied:
                errors.append(
                    "--chain run-state file is not the Pack-declared sidecar: "
                    f"pack declares {declared}, CLI passed {supplied}"
                )
        if (
            state is not None
            and ref is not None
            and state.get("run_id") != ref.get("run_id")
        ):
            errors.append(
                f"--chain run_id mismatch: pack declares {ref.get('run_id')!r}, "
                f"CLI run-state has {state.get('run_id')!r}"
            )
    errors.extend(check_pack_run_state(pack_path))
    if state is not None:
        errors.extend(bind_listed_handoffs(state, handoff_paths))
    if state is not None and state["phase"] == "delivered":
        errors.extend(
            require_delivered_audit(
                state,
                audit_result_path,
                artifact_path=pack_path,
                report_path=report_path,
                claim_alignment_bundle_path=claim_alignment_bundle_path,
                require_opt_in_binding=require_opt_in_binding,
            )
        )
    return errors


def _emit(ok: bool, errors: list[str], *, as_json: bool, extra: dict | None = None) -> int:
    payload = {"ok": ok, "errors": errors}
    if extra:
        payload.update(extra)
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        if ok:
            print("OK — Research Run State is valid")
        else:
            print("Run State validation failed:")
            for item in errors:
                print(f"  - {item}")
    return EXIT_OK if ok else EXIT_FAIL_CLOSED


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Fail-closed validator for Research Run State (issue #417)",
    )
    parser.add_argument("run_state_file", nargs="?", help="Path to the Run State JSON")
    parser.add_argument("--from", dest="from_file", default=None, help="Previous snapshot")
    parser.add_argument("--to", dest="to_file", default=None, help="Next snapshot")
    parser.add_argument("--resume", action="store_true", help="Re-validate for resume")
    parser.add_argument("--artifact", default=None, help="Research Pack process artifact")
    parser.add_argument(
        "--report",
        default=None,
        help="Final report file; binds audit_report (distinct from the Pack)",
    )
    parser.add_argument(
        "--activation-snapshot",
        default=None,
        help="Activation snapshot to re-check on resume",
    )
    parser.add_argument("--audit-result", default=None, help="audit_report --json payload")
    parser.add_argument(
        "--claim-alignment-bundle",
        default=None,
        help=(
            "Exact claim-alignment bundle used by audit_report; required to "
            "verify an enabled alignment audit before delivered"
        ),
    )
    parser.add_argument("--chain", action="store_true", help="Validate the e2e artifact chain")
    parser.add_argument(
        "--handoff",
        action="append",
        default=None,
        help="Track Handoff JSON; repeat for every listed handoff_refs entry",
    )
    parser.add_argument("--run-state", dest="chain_run_state", default=None)
    parser.add_argument("--pack", default=None, help="Research Pack markdown for --chain")
    parser.add_argument("--json", action="store_true", help="Machine-readable JSON output")
    args = parser.parse_args(argv)

    if args.chain:
        if not args.handoff or not (args.chain_run_state or args.run_state_file) or not args.pack:
            return _emit(
                False,
                ["--chain requires --handoff, --pack, and a run-state file"],
                as_json=args.json,
            )
        run_state_path = args.chain_run_state or args.run_state_file
        errors = validate_chain(
            handoff_paths=args.handoff,
            run_state_path=run_state_path,
            pack_path=args.pack,
            audit_result_path=args.audit_result,
            report_path=args.report,
            claim_alignment_bundle_path=args.claim_alignment_bundle,
            require_opt_in_binding=args.claim_alignment_bundle is not None,
        )
        return _emit(not errors, errors, as_json=args.json)

    if (args.from_file is None) ^ (args.to_file is None):
        return _emit(
            False,
            ["--from and --to must be supplied together"],
            as_json=args.json,
        )

    if args.from_file and args.to_file:
        before, before_errors = load_run_state_file(args.from_file)
        after, after_errors = load_run_state_file(args.to_file)
        # load_run_state_file already schema-validates; still run transition
        errors = [*before_errors, *after_errors]
        if before is not None and after is not None:
            errors = validate_transition(before, after)
            if after["phase"] == "delivered":
                errors.extend(
                    require_delivered_audit(
                        after,
                        args.audit_result,
                        artifact_path=args.artifact,
                        report_path=args.report,
                        claim_alignment_bundle_path=args.claim_alignment_bundle,
                        require_opt_in_binding=args.claim_alignment_bundle is not None,
                    )
                )
        extra = None
        if before is not None and after is not None:
            extra = {
                "from_phase": before["phase"],
                "to_phase": after["phase"],
                "from_status": before["status"],
                "to_status": after["status"],
            }
        return _emit(not errors, errors, as_json=args.json, extra=extra)

    if not args.run_state_file:
        return _emit(False, ["run state file is required"], as_json=args.json)

    state, errors = load_run_state_file(args.run_state_file)
    if state is None:
        return _emit(False, errors, as_json=args.json)

    extra = {
        "run_id": state["run_id"],
        "phase": state["phase"],
        "status": state["status"],
        "enabled_reason": state["enabled_reason"],
    }

    if args.resume:
        if args.artifact is None:
            errors.append("--resume requires --artifact to re-check artifact")
        if args.activation_snapshot is None:
            errors.append(
                "--resume requires --activation-snapshot to re-check "
                "activation_reference"
            )
        if args.artifact is None or args.activation_snapshot is None:
            return _emit(not errors, errors, as_json=args.json, extra=extra)
        errors.extend(
            check_resume(
                state,
                artifact_path=args.artifact,
                activation_snapshot_path=args.activation_snapshot,
            )
        )
    elif args.artifact:
        err = _unreadable_error("--artifact", args.artifact)
        if err is not None:
            errors.append(err)

    if args.activation_snapshot and not args.resume:
        errors.extend(
            check_activation_alignment(state, args.activation_snapshot)
        )

    if args.handoff:
        errors.extend(bind_listed_handoffs(state, args.handoff))

    if state["phase"] == "delivered":
        errors.extend(
            require_delivered_audit(
                state,
                args.audit_result,
                artifact_path=args.artifact,
                report_path=args.report,
                claim_alignment_bundle_path=args.claim_alignment_bundle,
                require_opt_in_binding=args.claim_alignment_bundle is not None,
            )
        )

    return _emit(not errors, errors, as_json=args.json, extra=extra)


if __name__ == "__main__":
    raise SystemExit(main())
