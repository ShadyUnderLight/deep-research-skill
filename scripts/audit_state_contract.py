"""Shared audit aggregation/state contract (issue #433 A1).

The producer (``audit_report.py``) records one status per required audit and
resolves the overall verdict; the canonical consumers
(``run_forward_evals.py``, also reused by ``validate_research_run_state.py``)
must accept exactly the verdicts the producer can legitimately emit.  Before
issue #433 the two sides maintained separate status sets, so non-strict
required-audit degradation resolved to ``conditional-pass`` while consumers
still classified those statuses as fail-like.

Aggregation table (single source of truth):

- ``pass``: clean; may aggregate into every overall verdict.
- ``conditional-pass``: audit-level warnings; never aggregates into a clean
  ``pass`` and is itself a conditional cause.
- ``not_run`` / ``skipped`` / ``partial``: degraded required-audit statuses.
  The producer keeps them visible in ``audits[]`` and (outside ``--strict``)
  resolves the verdict to ``conditional-pass`` with a warning; they are the
  conditional causes consumers must accept, and must never aggregate into a
  clean ``pass``.  The only exception is a default-off opt-in audit recorded
  as ``not_run`` (issue #419) — exempt in every context.
- ``fail``: blocks in every mode; never aggregates into ``pass`` or
  ``conditional-pass``.

Consumers of this module must pass the opt-in audit id set from the audit
registry (``_AUDIT_REGISTRY.opt_in_audit_ids()``); the opt-in exemption
reason logic stays in ``opt_in_audit_contract.py``.
"""

from __future__ import annotations

from opt_in_audit_contract import (
    audit_not_run_is_conditional_consumer_exempt,
    audit_not_run_is_consumer_exempt,
    is_opt_in_default_off_not_run,
)

PASS_STATUS = "pass"
CONDITIONAL_PASS_STATUS = "conditional-pass"
FAIL_STATUS = "fail"
NOT_RUN_STATUS = "not_run"

# Statuses that can never be aggregated into a clean overall=pass verdict
# (an exempt default-off opt-in not_run is handled separately, issue #419).
FAIL_LIKE_AUDIT_STATUSES = frozenset({FAIL_STATUS, "partial", "skipped"})

# Degraded required-audit statuses (issue #433 A1): recorded when a required
# manual/process audit did not execute (or only partially executed) and the
# non-strict verdict resolves to conditional-pass.
DEGRADED_AUDIT_STATUSES = frozenset({NOT_RUN_STATUS, "skipped", "partial"})


def audit_status_blocks_clean_pass(
    audit_id: str,
    status: str,
    reason: str | None,
    opt_in_audit_ids: frozenset[str] | set[str],
    *,
    require_opt_in_binding: bool = False,
) -> bool:
    """True when *status* must never be aggregated into ``overall=pass``.

    Every non-pass status blocks a clean pass; the only exception is a
    default-off opt-in ``not_run`` (issue #419), which is explicitly
    disallowed when ``require_opt_in_binding`` marks the caller's opt-in
    input as the trust anchor.
    """
    if status == PASS_STATUS:
        return False
    if status == NOT_RUN_STATUS:
        return not audit_not_run_is_consumer_exempt(
            {"audit_id": audit_id, "status": status, "reason": reason},
            opt_in_audit_ids,
            require_opt_in_binding=require_opt_in_binding,
        )
    return True


def audit_status_is_fail_like(
    audit_id: str,
    status: str,
    reason: str | None,
    opt_in_audit_ids: frozenset[str] | set[str],
    *,
    require_opt_in_binding: bool = False,
) -> bool:
    """Legacy classification: statuses that cannot aggregate to ``pass``.

    ``fail`` / ``partial`` / ``skipped`` are always fail-like; ``not_run`` is
    fail-like unless it is an exempt opt-in record (default-off or aggregate
    NOT_RUN, issue #419).  Kept for callers that distinguish fail-like audits
    from conditional causes (e.g. secondary-hard-fail replay expectations).
    """
    if status in FAIL_LIKE_AUDIT_STATUSES:
        return True
    if status == NOT_RUN_STATUS:
        return not audit_not_run_is_conditional_consumer_exempt(
            {"audit_id": audit_id, "status": status, "reason": reason},
            opt_in_audit_ids,
            require_opt_in_binding=require_opt_in_binding,
        )
    return False


def audit_status_blocks_conditional_pass(status: str) -> bool:
    """True when *status* must never be aggregated into ``conditional-pass``.

    Only an outright ``fail`` escalates past conditional-pass.  Degraded
    required-audit statuses (``not_run`` / ``skipped`` / ``partial``) are the
    issue #433 A1 causes of conditional-pass, not offenders.
    """
    return status == FAIL_STATUS


def audit_status_is_conditional_cause(
    audit_id: str,
    status: str,
    reason: str | None,
    opt_in_audit_ids: frozenset[str] | set[str],
) -> bool:
    """True when *status* alone justifies ``overall=conditional-pass``.

    A ``conditional-pass`` audit or validator is a direct cause; a required
    audit recorded with a degraded status is the non-strict A1 cause.  A
    default-off opt-in ``not_run`` is clean rather than a cause; an enabled
    opt-in default ``not_run`` (aggregate NOT_RUN) is a cause because the
    producer resolves that state to conditional-pass.
    """
    if status == CONDITIONAL_PASS_STATUS:
        return True
    if status in DEGRADED_AUDIT_STATUSES:
        return not is_opt_in_default_off_not_run(
            audit_id, status, reason, opt_in_audit_ids
        )
    return False
