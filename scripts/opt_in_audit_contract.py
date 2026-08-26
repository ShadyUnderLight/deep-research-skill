"""Shared opt-in audit consumer contract (issue #419)."""

from __future__ import annotations

from typing import Any

OPT_IN_DEFAULT_OFF_REASON = "opt-in audit not enabled (default off)"
OPT_IN_AGGREGATE_NOT_RUN_REASON = "aggregate NOT_RUN"


def is_opt_in_default_off_not_run(
    audit_id: str,
    status: str,
    reason: str | None,
    opt_in_audit_ids: frozenset[str] | set[str],
) -> bool:
    """True when an opt-in audit is explicitly default-off (consumers may exempt)."""
    if status != "not_run":
        return False
    if audit_id not in opt_in_audit_ids:
        return False
    return reason == OPT_IN_DEFAULT_OFF_REASON


def is_opt_in_aggregate_not_run_exempt(
    audit_id: str,
    status: str,
    reason: str | None,
    opt_in_audit_ids: frozenset[str] | set[str],
) -> bool:
    if status != "not_run":
        return False
    if audit_id not in opt_in_audit_ids:
        return False
    return reason == OPT_IN_AGGREGATE_NOT_RUN_REASON


def audit_not_run_is_consumer_exempt(
    audit: dict[str, Any],
    opt_in_audit_ids: frozenset[str] | set[str],
    *,
    require_opt_in_binding: bool = False,
) -> bool:
    audit_id = str(audit.get("audit_id") or "")
    status = str(audit.get("status") or "")
    reason = audit.get("reason")
    reason_str = reason if isinstance(reason, str) else None
    if require_opt_in_binding and audit_id in opt_in_audit_ids:
        # A caller-supplied opt-in input is the trust anchor.  A payload that
        # downgrades the same audit to default-off is contradictory and must
        # not regain the exemption by changing its reason string.
        return False
    # Only an audit that was never enabled may be omitted from a clean Pass.
    # An explicitly enabled audit whose population is entirely NOT_RUN must
    # remain visible as a non-Pass result.
    return is_opt_in_default_off_not_run(
        audit_id, status, reason_str, opt_in_audit_ids
    )


def audit_not_run_is_conditional_consumer_exempt(
    audit: dict[str, Any],
    opt_in_audit_ids: frozenset[str] | set[str],
    *,
    require_opt_in_binding: bool = False,
) -> bool:
    """Allow opt-in NOT_RUN in conditional-pass, never in overall Pass."""
    audit_id = str(audit.get("audit_id") or "")
    status = str(audit.get("status") or "")
    reason = audit.get("reason")
    reason_str = reason if isinstance(reason, str) else None
    return (
        audit_not_run_is_consumer_exempt(
            audit,
            opt_in_audit_ids,
            require_opt_in_binding=require_opt_in_binding,
        )
        or is_opt_in_aggregate_not_run_exempt(
            audit_id, status, reason_str, opt_in_audit_ids
        )
    )
