"""Unit tests for the shared audit aggregation state contract (issue #433 A1).

The producer (``audit_report.py``) and the canonical consumers
(``run_forward_evals.py``, reused by Run State validation) must classify
audit statuses identically.  These tests pin the single aggregation table so
the two sides cannot drift apart again — the issue #433 re-review found the
producer resolving non-strict degraded audits to ``conditional-pass`` while
consumers still treated ``partial`` / ``skipped`` / required ``not_run`` as
fail-like.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from audit_state_contract import (  # noqa: E402
    DEGRADED_AUDIT_STATUSES,
    audit_status_blocks_clean_pass,
    audit_status_blocks_conditional_pass,
    audit_status_is_conditional_cause,
    audit_status_is_fail_like,
)
from opt_in_audit_contract import (  # noqa: E402
    OPT_IN_AGGREGATE_NOT_RUN_REASON,
    OPT_IN_DEFAULT_OFF_REASON,
)

OPT_IN_IDS = frozenset({"claim-source-alignment"})
REQUIRED_AUDIT = "market-outlook-audit"
OPT_IN_AUDIT = "claim-source-alignment"


def test_pass_never_blocks_clean_pass() -> None:
    assert audit_status_blocks_clean_pass(REQUIRED_AUDIT, "pass", None, OPT_IN_IDS) is False


def test_every_non_pass_status_blocks_clean_pass_except_default_off_not_run() -> None:
    for status in ("conditional-pass", "fail", "partial", "skipped"):
        assert audit_status_blocks_clean_pass(
            REQUIRED_AUDIT, status, None, OPT_IN_IDS
        ) is True, status
    # A required not_run blocks a clean pass ...
    assert audit_status_blocks_clean_pass(
        REQUIRED_AUDIT, "not_run", "not declared", OPT_IN_IDS
    ) is True
    # ... an enabled opt-in aggregate NOT_RUN does too ...
    assert audit_status_blocks_clean_pass(
        OPT_IN_AUDIT, "not_run", OPT_IN_AGGREGATE_NOT_RUN_REASON, OPT_IN_IDS
    ) is True
    # ... only the default-off opt-in exemption is clean (issue #419).
    assert audit_status_blocks_clean_pass(
        OPT_IN_AUDIT, "not_run", OPT_IN_DEFAULT_OFF_REASON, OPT_IN_IDS
    ) is False


def test_require_opt_in_binding_disables_default_off_exemption() -> None:
    assert audit_status_blocks_clean_pass(
        OPT_IN_AUDIT,
        "not_run",
        OPT_IN_DEFAULT_OFF_REASON,
        OPT_IN_IDS,
        require_opt_in_binding=True,
    ) is True


def test_only_fail_blocks_conditional_pass() -> None:
    for status in ("pass", "conditional-pass", "not_run", "skipped", "partial"):
        assert audit_status_blocks_conditional_pass(status) is False, status
    assert audit_status_blocks_conditional_pass("fail") is True


def test_conditional_causes_cover_conditional_pass_and_degraded_required() -> None:
    assert audit_status_is_conditional_cause(
        REQUIRED_AUDIT, "conditional-pass", None, OPT_IN_IDS
    ) is True
    assert audit_status_is_conditional_cause(
        REQUIRED_AUDIT, "not_run", "not declared", OPT_IN_IDS
    ) is True
    assert audit_status_is_conditional_cause(
        REQUIRED_AUDIT, "skipped", "no --research-pack path provided", OPT_IN_IDS
    ) is True
    assert audit_status_is_conditional_cause(
        REQUIRED_AUDIT, "partial", "evidence incomplete", OPT_IN_IDS
    ) is True
    # A default-off opt-in not_run is clean, not a conditional cause.
    assert audit_status_is_conditional_cause(
        OPT_IN_AUDIT, "not_run", OPT_IN_DEFAULT_OFF_REASON, OPT_IN_IDS
    ) is False
    # An enabled opt-in with an aggregate NOT_RUN resolves to conditional-pass.
    assert audit_status_is_conditional_cause(
        OPT_IN_AUDIT, "not_run", OPT_IN_AGGREGATE_NOT_RUN_REASON, OPT_IN_IDS
    ) is True
    # pass and fail never justify conditional-pass.
    assert audit_status_is_conditional_cause(
        REQUIRED_AUDIT, "pass", None, OPT_IN_IDS
    ) is False
    assert audit_status_is_conditional_cause(
        REQUIRED_AUDIT, "fail", None, OPT_IN_IDS
    ) is False


def test_fail_like_keeps_legacy_replay_semantics() -> None:
    assert audit_status_is_fail_like(REQUIRED_AUDIT, "fail", None, OPT_IN_IDS) is True
    assert audit_status_is_fail_like(REQUIRED_AUDIT, "partial", None, OPT_IN_IDS) is True
    assert audit_status_is_fail_like(REQUIRED_AUDIT, "skipped", None, OPT_IN_IDS) is True
    assert audit_status_is_fail_like(
        REQUIRED_AUDIT, "not_run", "not declared", OPT_IN_IDS
    ) is True
    assert audit_status_is_fail_like(
        OPT_IN_AUDIT, "not_run", OPT_IN_DEFAULT_OFF_REASON, OPT_IN_IDS
    ) is False
    assert audit_status_is_fail_like(
        OPT_IN_AUDIT, "not_run", OPT_IN_AGGREGATE_NOT_RUN_REASON, OPT_IN_IDS
    ) is False
    assert audit_status_is_fail_like(REQUIRED_AUDIT, "pass", None, OPT_IN_IDS) is False
    assert audit_status_is_fail_like(
        REQUIRED_AUDIT, "conditional-pass", None, OPT_IN_IDS
    ) is False


def test_degraded_set_is_the_a1_conditional_cause_set() -> None:
    assert DEGRADED_AUDIT_STATUSES == frozenset({"not_run", "skipped", "partial"})
