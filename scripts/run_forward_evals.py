#!/usr/bin/env python3
"""Execute the offline route-sharp forward-eval registry.

The runner deliberately consumes the existing command-line audit surface and
its JSON output. It does not call a paid model, browse the network, or invent a
production prompt classifier. Structured replay cases supply canonical
action/object activation inputs and a prompt hash. Integration cases also pass
a versioned activation snapshot into the production audit command so route
mismatch is a real blocking assertion rather than a runner-only oracle.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

from eval_registry import (
    DEFAULT_REGISTRY_PATH,
    EvalRegistryError,
    active_cases,
    gap_class_for_failure_family,
    failure_stage_for_failure_family,
    load_registry,
)
from validate_contract import extract_contract_from_markdown, sanitize_visible_markdown
from validate_research_pack import (
    extract_declared_statuses,
    find_missing_headings,
    strip_fenced_code_blocks,
)
from route_activation import RouteActivationError, activate_prompt
from activation_snapshot import (
    ActivationSnapshotError,
    activation_reference,
    build_activation_snapshot,
    extract_activation_snapshot_reference,
    load_activation_snapshot,
)
import registry_loader  # noqa: E402
from audit_evidence import validate_evidence_reference  # noqa: E402 — re-validate manual/process evidence against real artifact (issue #403 re-review)
from opt_in_audit_contract import (  # noqa: E402
    OPT_IN_AGGREGATE_NOT_RUN_REASON,
    audit_not_run_is_conditional_consumer_exempt,
    audit_not_run_is_consumer_exempt,
)

# Canonical route → validator binding set.  The runner uses it to verify the
# audit JSON validators[] is a complete, un-forged binding set (issue #393).
_ROUTE_REGISTRY = registry_loader.load_route_registry()

# Canonical audit registry.  Used to derive the complete expected audit set
# (route required audits + delivery-scope global audits + secondary hard-fail
# audits) and to verify each automated audit's validator_binding against the
# registry (issue #403: consumer fail-closed on missing/forged audit results).
_AUDIT_REGISTRY = registry_loader.load_audit_registry()


ROOT = Path(__file__).resolve().parents[1]
AUDIT_SCRIPT = ROOT / "scripts" / "audit_report.py"
DEFAULT_BASELINE_PATH = ROOT / "evals" / "forward-metrics-baseline.json"

# The audit JSON verdict schema this runner understands.  A schema_version it
# does not know must fail closed instead of being treated as a Pass
# (issue #393: unknown JSON shape ⇒ incomplete, never pass).
EXPECTED_AUDIT_JSON_SCHEMA_VERSION = 1

# The canonical provenance version string every audit JSON must carry.  Mirrors
# audit_report._registry_version() so the runner rejects any JSON whose
# validator_version was forged or drifted (issue #403).  Schema version and
# registry version are independent concepts — the JSON carries both.
EXPECTED_VALIDATOR_VERSION = (
    f"audit-registry-v{_AUDIT_REGISTRY.version} "
    f"(route-manifest-v{_ROUTE_REGISTRY.version})"
)

# Route-level validators are always automated; any other execution_source is a
# forged record and must fail closed (issue #403).
ALLOWED_VALIDATOR_EXECUTION_SOURCES = {"automated_validator"}

# Allowed execution_source vocabulary per audit execution_type.  A value
# outside the type's allowlist (e.g. a forged "trusted_human") must fail
# closed (issue #403).  "unknown" is permitted only as a degraded manual/process
# attestation when strict evidence validation could not recover a source.
AUDIT_EXECUTION_SOURCE_BY_TYPE = {
    "automated": {"automated_validator"},
    "manual": {"manual_checklist_attestation", "legacy_self_attested", "unknown"},
    "process": {"process_node_evidence"},
}

# Unified audit result statuses the runner accepts.  Anything else is a forged
# or malformed status and must fail closed (issue #403).
ALLOWED_AUDIT_STATUSES = {
    "pass",
    "conditional-pass",
    "fail",
    "not_run",
    "skipped",
    "partial",
}


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _ratio(numerator: int, denominator: int) -> float:
    return round(numerator / denominator, 4) if denominator else 1.0


def _pack_observation(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8", errors="replace")
    cleaned = strip_fenced_code_blocks(text)
    headings = {
        line.removeprefix("## ").strip()
        for line in cleaned.splitlines()
        if line.startswith("## ")
    }
    statuses = extract_declared_statuses(text)
    version_match = re.search(
        r"^## Decision tree version\s*\n+[ \t]*([0-9]+)[ \t]*$",
        cleaned,
        re.MULTILINE,
    )
    activation_snapshot, activation_snapshot_errors = (
        extract_activation_snapshot_reference(cleaned, label="Research Pack")
    )
    return {
        "fields": sorted(headings),
        "missing_required_fields": find_missing_headings(cleaned),
        "statuses": statuses,
        "decision_tree_version": int(version_match.group(1)) if version_match else None,
        "activation_snapshot": activation_snapshot,
        "activation_snapshot_errors": activation_snapshot_errors,
    }


def _run_audit(
    report: Path,
    research_pack: Path,
    activation_snapshot: Path | None = None,
) -> tuple[dict[str, Any] | None, str | None, int]:
    command = [
        sys.executable,
        str(AUDIT_SCRIPT),
        str(report),
        "--research-pack",
        str(research_pack),
        "--strict",
        "--require-contract",
        "--json",
    ]
    if activation_snapshot is not None:
        command.extend(["--activation-snapshot", str(activation_snapshot)])
    completed = subprocess.run(command, capture_output=True, text=True, cwd=ROOT)
    try:
        data = json.loads(completed.stdout)
    except json.JSONDecodeError:
        detail = (completed.stderr or completed.stdout).strip()
        return None, detail[:500] or "audit_report.py did not emit JSON", completed.returncode
    return data, None, completed.returncode


def _detect_failure_family(case: dict[str, Any], actual: dict[str, Any]) -> str | None:
    expected_family = case.get("failure_family")
    if expected_family == "route-misclassification":
        if (
            actual["activation_route"] != actual["expected_route"]
            or actual["activation_route"] != actual["report_route"]
        ):
            return expected_family
    if expected_family == "secondary-route-not-verified":
        expected_secondary = set(case["expected"].get("secondary_routes", []))
        if set(actual["secondary_routes"]) != expected_secondary:
            return None
        expected_targets = {f"{route}-secondary-hard-fail" for route in expected_secondary}
        secondary_audits = [
            item
            for item in actual.get("audits", [])
            if isinstance(item, dict)
            and str(item.get("audit_id", "")) in expected_targets
        ]
        if expected_targets and {
            str(item.get("audit_id")) for item in secondary_audits
        } != expected_targets:
            return expected_family
        if any(item.get("status") != "pass" for item in secondary_audits):
            return expected_family
        if any("secondary route" in str(message).lower() for message in actual.get("blocking", [])):
            return expected_family
    if expected_family == "declared-not-executed":
        if any(
            isinstance(item, dict)
            and item.get("execution_type") in {"manual", "process"}
            and item.get("status") in {"not_run", "partial", "skipped"}
            for item in actual.get("audits", [])
        ):
            return expected_family
    if actual.get("overall") == "fail":
        return "audit-failure"
    return None


def _audit_statuses(actual: dict[str, Any]) -> dict[str, str]:
    return {
        str(item.get("audit_id")): str(item.get("status"))
        for item in actual.get("audits", [])
        if isinstance(item, dict) and item.get("audit_id")
    }


# Valid statuses a route-level validator result may carry.  ``incomplete`` /
# ``not_run`` mean the validator did not execute and must never be accepted.
VALID_VALIDATOR_STATUSES = {"pass", "conditional-pass", "fail"}


def _validators_ok(
    actual: dict[str, Any],
    expected_validators: list[str],
    audited_path: str | None = None,
    expected_input_sha256: str | None = None,
) -> bool:
    """Consume the structured audit JSON provenance fields (issue #393).

    A verdict is consumable only when:
    - the JSON schema_version is the one this runner understands; an unknown
      shape fails closed (never treated as Pass);
    - the top-level validator_version matches the canonical registry version
      (EXPECTED_VALIDATOR_VERSION); a forged or drifted version fails closed;
    - the validators[] ids are exactly the canonical binding set for the
      resolved route, one-to-one (same length, same order, no duplicates, no
      forged extra id);
    - every entry carries its required provenance fields (validator_id,
      status, errors/warnings, evidence, execution_source, validator_version)
      and a legal status;
    - status is consistent with errors/warnings: ``pass`` carries neither,
      ``conditional-pass`` carries warnings and no errors, ``fail`` carries
      errors;
    - pass evidence is a verifiable locator against the audited report — an
      unverifiable locator blocks instead of being treated as a Pass.
    """
    if actual.get("schema_version") != EXPECTED_AUDIT_JSON_SCHEMA_VERSION:
        return False
    if actual.get("validator_version") != EXPECTED_VALIDATOR_VERSION:
        return False
    # External trust anchor: the verdict's audited-file hash must equal the hash
    # the consumer computes from the report on disk — a missing / forged
    # top-level hash (or one that merely matches another JSON field) fails
    # closed (issue #403 P1).
    if (
        expected_input_sha256 is not None
        and actual.get("input_sha256") != expected_input_sha256
    ):
        return False
    validators = actual.get("validators") or []
    if not validators:
        return False
    # Strict one-to-one binding-set check: same length, same ids, same order.
    # Set comparison would hide duplicate entries and forged extras (#393).
    # Non-object entries are dropped so a malformed list fails the length
    # match instead of crashing on item.get().
    recorded_ids = [
        str(item.get("validator_id"))
        for item in validators
        if isinstance(item, dict)
    ]
    if recorded_ids != expected_validators:
        return False
    for item in validators:
        if not isinstance(item, dict):
            return False
        status = str(item.get("status"))
        if status not in VALID_VALIDATOR_STATUSES:
            return False
        if not item.get("validator_id"):
            return False
        errors = item.get("errors")
        warnings = item.get("warnings")
        if not isinstance(errors, list) or not isinstance(warnings, list):
            return False
        if status == "pass" and (errors or warnings):
            return False
        if status == "conditional-pass" and (not warnings or errors):
            return False
        if status == "fail" and not errors:
            return False
        evidence = item.get("evidence")
        if not isinstance(evidence, list) or not evidence:
            return False
        if not all(isinstance(e, str) and e.strip() for e in evidence):
            return False
        # pass evidence is a "no violations found" locator claim against the
        # audited report.  Prefix matching would accept "<path>.evil: ...", so
        # require the exact "<audited_path>:" prefix; unverifiable blocks.
        if status == "pass" and (
            audited_path is None or not evidence[0].startswith(f"{audited_path}:")
        ):
            return False
        execution_source = item.get("execution_source")
        if execution_source not in ALLOWED_VALIDATOR_EXECUTION_SOURCES:
            return False
        validator_version = item.get("validator_version")
        if validator_version != EXPECTED_VALIDATOR_VERSION:
            return False
        # Bind the validator result to the audited file.  When an external
        # trust anchor is available (the consumer-computed report hash) it is
        # mandatory: target must equal audited_path and artifact hash must
        # equal the consumer-computed hash — a missing / forged hash (even
        # when top-level and item agree) fails closed (issue #403 P1).  Without
        # an external anchor (simple unit tests) fall back to requiring the
        # fields to be present and internally consistent.
        if audited_path is not None:
            if not isinstance(item.get("target"), str) or not item.get("target").strip():
                return False
            if item.get("target") != audited_path:
                return False
            if (
                not isinstance(item.get("input_sha256"), str)
                or not item.get("input_sha256").strip()
            ):
                return False
        if expected_input_sha256 is not None:
            if item.get("input_sha256") != expected_input_sha256:
                return False
        elif actual.get("input_sha256") is not None:
            if item.get("input_sha256") != actual.get("input_sha256"):
                return False
    return True


def _expected_audit_set(
    route: str,
    secondary_routes: list[str],
) -> list[str] | None:
    """Derive the canonical complete expected audit set for a route (issue #403).

    Composes, in order:
    - the route's required audits (``_ROUTE_REGISTRY.required_audits_for``);
    - the delivery-scope global audits (``_AUDIT_REGISTRY.global_audit_ids``);
    - each declared secondary route's ``<secondary>-secondary-hard-fail`` audit.

    Returns a sorted, de-duplicated id list.  Returns ``None`` when a required
    or global audit id has no entry in the audit registry — registry drift must
    fail closed rather than produce a silently incomplete expected set.  The
    ``<secondary>-secondary-hard-fail`` ids are contract-derived and are
    intentionally not required to exist in the audit registry.
    """
    required_and_global = list(_ROUTE_REGISTRY.required_audits_for(route)) + list(
        _AUDIT_REGISTRY.global_audit_ids()
    )
    for audit_id in required_and_global:
        if _AUDIT_REGISTRY.get_audit(audit_id) is None:
            return None
    secondary_ids = [f"{sr}-secondary-hard-fail" for sr in secondary_routes]
    opt_in_ids = list(_AUDIT_REGISTRY.opt_in_audit_ids())
    all_ids = required_and_global + secondary_ids + opt_in_ids
    seen: set[str] = set()
    ordered: list[str] = []
    for audit_id in all_ids:
        if audit_id not in seen:
            seen.add(audit_id)
            ordered.append(audit_id)
    return sorted(ordered)


def _sha256(path: object) -> str | None:
    """SHA-256 of a file's bytes, or ``None`` on read failure.

    The consumer computes this itself so audit provenance is anchored to the
    real on-disk artifact rather than to a hash that travelled inside the audit
    JSON (issue #403 P1: a forged/missing JSON hash must not be trusted).
    """
    try:
        return hashlib.sha256(Path(path).read_bytes()).hexdigest()
    except (OSError, ValueError, UnicodeError):
        return None


def _claim_alignment_bundle_binding_errors(
    item: dict[str, Any],
    expected_path: str | None,
) -> list[str]:
    """Verify the opt-in alignment bundle used by an automated audit.

    The report hash alone is insufficient: the alignment bundle is a separate
    input and may change while the report and Research Pack remain identical.
    Delivered/forward consumers therefore require the caller to supply the
    exact bundle path and re-hash it.
    """
    if expected_path is None:
        return [
            "claim-source-alignment requires the exact "
            "--claim-alignment-bundle path for consumer verification"
        ]
    expected = Path(expected_path).resolve()
    actual_hash = _sha256(expected)
    if actual_hash is None:
        return [f"cannot read claim-alignment bundle {expected}"]

    provenance = item.get("evidence_provenance")
    verified = [
        record
        for record in provenance or []
        if isinstance(record, dict) and record.get("verified") is True
    ]
    if not verified:
        return ["claim-source-alignment has no verified provenance record"]

    errors: list[str] = []
    for record in verified:
        declared_path = record.get("claim_alignment_bundle")
        if not isinstance(declared_path, str) or not declared_path.strip():
            errors.append(
                "verified provenance is missing claim_alignment_bundle"
            )
        else:
            try:
                declared = Path(declared_path).resolve()
            except OSError as exc:
                errors.append(f"claim_alignment_bundle path cannot resolve: {exc}")
            else:
                if declared != expected:
                    errors.append(
                        "claim_alignment_bundle path does not match the supplied "
                        f"path ({declared} != {expected})"
                    )
        declared_hash = record.get("claim_alignment_bundle_sha256")
        if declared_hash != actual_hash:
            errors.append(
                "claim_alignment_bundle_sha256 does not match the supplied "
                f"bundle ({declared_hash!r} != {actual_hash})"
            )
    return errors


def _audit_consistency_details(
    actual: dict[str, Any],
    expected_audit_ids: list[str],
    audited_path: str | None = None,
    expected_report_sha256: str | None = None,
    research_pack_path: str | None = None,
    expected_pack_sha256: str | None = None,
    report_text: str | None = None,
    pack_text: str | None = None,
    expected_route: str | None = None,
    claim_alignment_bundle_path: str | None = None,
) -> tuple[bool, list[str]]:
    """Detailed audit-set validation that returns locatable errors (issue #408).

    Returns ``(ok, errors)`` where ``errors`` contains one entry per violated
    invariant, each prefixed with the offending ``audit_id`` when applicable
    (e.g. ``audit option-selection-final-audit: not_run requires non-empty
    reason``).  ``ok`` is ``True`` iff ``errors`` is empty.  This is the
    single source of truth for audit status semantics; ``_audits_ok`` is a
    boolean wrapper for backwards compatibility.
    """
    errors: list[str] = []
    audits = actual.get("audits")
    if not isinstance(audits, list):
        return False, ["audits is not a list"]
    actual_ids = [
        str(item.get("audit_id")) for item in audits if isinstance(item, dict)
    ]
    if len(actual_ids) != len(set(actual_ids)):
        dup = next((x for x in actual_ids if actual_ids.count(x) > 1), actual_ids[0] if actual_ids else "unknown")
        errors.append(f"duplicate audit_id '{dup}'")
    if set(actual_ids) != set(expected_audit_ids):
        missing = sorted(set(expected_audit_ids) - set(actual_ids))
        extra = sorted(set(actual_ids) - set(expected_audit_ids))
        if missing:
            errors.append(f"missing required audit(s): {', '.join(missing)}")
        if extra:
            errors.append(f"unknown/forged audit(s): {', '.join(extra)}")
    # External trust anchor
    if (
        expected_report_sha256 is not None
        and actual.get("input_sha256") != expected_report_sha256
    ):
        errors.append(
            f"top-level input_sha256 does not match consumer-computed report hash ({actual.get('input_sha256')!r} != {expected_report_sha256!r})"
        )

    for item in audits:
        if not isinstance(item, dict):
            errors.append("audit entry is not an object")
            continue
        audit_id = str(item.get("audit_id") or "<missing>")
        status = str(item.get("status") or "")
        prefix = f"audit {audit_id}:"
        if status not in ALLOWED_AUDIT_STATUSES:
            errors.append(f"{prefix} unknown status '{status}'")
            continue
        execution_type = item.get("execution_type")
        execution_source = item.get("execution_source")
        if not isinstance(execution_source, str) or not execution_source.strip():
            errors.append(f"{prefix} execution_source must be non-empty string")
            continue

        registry_audit = _AUDIT_REGISTRY.get_audit(audit_id)
        if registry_audit is not None:
            if execution_type != registry_audit.execution_type:
                errors.append(
                    f"{prefix} execution_type '{execution_type}' does not match registry '{registry_audit.execution_type}'"
                )
                continue
        elif not (
            audit_id.endswith("-secondary-hard-fail") and execution_type == "manual"
        ):
            errors.append(f"{prefix} unknown audit_id and not a secondary-hard-fail manual audit")
            continue

        allowed_sources = AUDIT_EXECUTION_SOURCE_BY_TYPE.get(execution_type, set())
        if execution_source not in allowed_sources:
            errors.append(
                f"{prefix} execution_source '{execution_source}' not allowed for execution_type '{execution_type}'"
            )
            continue

        if execution_type == "automated":
            if item.get("validator_binding") != registry_audit.validator_binding:
                errors.append(
                    f"{prefix} validator_binding {item.get('validator_binding')!r} does not match registry {registry_audit.validator_binding!r}"
                )
                continue

        # Structural type checks
        raw_errors = item.get("errors")
        raw_warnings = item.get("warnings")
        raw_evidence = item.get("evidence")
        reason = item.get("reason")
        raw_provenance = item.get("evidence_provenance")

        if raw_errors is None:
            errs: list[Any] = []
        elif isinstance(raw_errors, list):
            errs = raw_errors
        else:
            errors.append(f"{prefix} errors must be list")
            continue
        if raw_warnings is None:
            warns: list[Any] = []
        elif isinstance(raw_warnings, list):
            warns = raw_warnings
        else:
            errors.append(f"{prefix} warnings must be list")
            continue
        if raw_evidence is None:
            evids: list[Any] = []
        elif isinstance(raw_evidence, list):
            evids = raw_evidence
        else:
            errors.append(f"{prefix} evidence must be list")
            continue
        if reason is not None and not isinstance(reason, str):
            errors.append(f"{prefix} reason must be string or null")
            continue
        # Unified element-type and non-empty checks for present collections (P2)
        # Every present element must be a non-empty string; a whitespace-only
        # string is never a locatable error/warning/evidence (closes
        # partial+reason+whitespace-errors bypass, see re-review P2).
        if any(not isinstance(e, str) for e in errs):
            errors.append(f"{prefix} errors must be list of strings")
            continue
        if errs and any(not e.strip() for e in errs):
            errors.append(f"{prefix} errors must be non-empty strings")
            continue
        if any(not isinstance(w, str) for w in warns):
            errors.append(f"{prefix} warnings must be list of strings")
            continue
        if warns and any(not w.strip() for w in warns):
            errors.append(f"{prefix} warnings must be non-empty strings")
            continue
        if any(not isinstance(e, str) for e in evids):
            errors.append(f"{prefix} evidence must be list of strings")
            continue
        if evids and any(not e.strip() for e in evids):
            errors.append(f"{prefix} evidence must be non-empty strings")
            continue
        # evidence_provenance structural check for all statuses (P2)
        if raw_provenance is not None and not isinstance(raw_provenance, list):
            errors.append(f"{prefix} evidence_provenance must be list")
            continue
        if isinstance(raw_provenance, list):
            for idx, p in enumerate(raw_provenance):
                if not isinstance(p, dict):
                    errors.append(f"{prefix} evidence_provenance[{idx}] must be object")
                    break
        # Per-status semantics
        if status == "pass":
            if errs or warns:
                errors.append(f"{prefix} pass must have no errors/warnings (got errors={errs!r} warnings={warns!r})")
                continue
            if reason is not None and reason.strip():
                errors.append(f"{prefix} pass must not have reason")
                continue
            if not evids or not all(isinstance(e, str) and e.strip() for e in evids):
                errors.append(f"{prefix} pass requires non-empty evidence")
                continue
            if execution_type == "manual" and execution_source != "manual_checklist_attestation":
                errors.append(f"{prefix} pass with execution_type manual requires execution_source manual_checklist_attestation (got {execution_source!r})")
                continue
            if execution_type == "process" and execution_source != "process_node_evidence":
                errors.append(f"{prefix} pass with execution_type process requires execution_source process_node_evidence (got {execution_source!r})")
                continue
            if audit_id == "research-pack":
                expected_target = str(research_pack_path) if research_pack_path else None
                expected_hash = expected_pack_sha256
            else:
                expected_target = audited_path
                expected_hash = expected_report_sha256
            prov_ok, prov_errors = _audit_provenance_details(
                item, audit_id, execution_type, execution_source,
                expected_target, expected_hash,
                report_text=report_text, pack_text=pack_text, expected_route=expected_route,
            )
            if not prov_ok:
                # Surface the underlying locator / binding diagnostic so a hidden
                # heading inside a fence / HTML block is distinguishable from a
                # generic provenance mismatch (issue #409).
                detail = f" ({'; '.join(prov_errors)})" if prov_errors else ""
                errors.append(f"{prefix} pass provenance failed (missing/unverified or artifact binding mismatch){detail}")
                continue
        elif status == "conditional-pass":
            if not warns or errs:
                errors.append(f"{prefix} conditional-pass requires warnings and no errors (got warnings={warns!r} errors={errs!r})")
                continue
            if not all(isinstance(w, str) and w.strip() for w in warns):
                errors.append(f"{prefix} conditional-pass warnings must be non-empty strings")
                continue
            if reason is not None and reason.strip():
                errors.append(f"{prefix} conditional-pass must not have reason")
                continue
            if not evids or not all(isinstance(e, str) and e.strip() for e in evids):
                errors.append(f"{prefix} conditional-pass requires non-empty evidence")
                continue
            if execution_type == "manual" and execution_source != "manual_checklist_attestation":
                errors.append(f"{prefix} conditional-pass with execution_type manual requires execution_source manual_checklist_attestation")
                continue
            if execution_type == "process" and execution_source != "process_node_evidence":
                errors.append(f"{prefix} conditional-pass with execution_type process requires execution_source process_node_evidence")
                continue
            if audit_id == "research-pack":
                expected_target = str(research_pack_path) if research_pack_path else None
                expected_hash = expected_pack_sha256
            else:
                expected_target = audited_path
                expected_hash = expected_report_sha256
            prov_ok, prov_errors = _audit_provenance_details(
                item, audit_id, execution_type, execution_source,
                expected_target, expected_hash,
                report_text=report_text, pack_text=pack_text, expected_route=expected_route,
            )
            if not prov_ok:
                detail = f" ({'; '.join(prov_errors)})" if prov_errors else ""
                errors.append(f"{prefix} conditional-pass provenance failed (same binding as pass required){detail}")
                continue
        elif status == "fail":
            if not errs or not any(isinstance(e, str) and e.strip() for e in errs):
                errors.append(f"{prefix} fail requires non-empty errors")
                continue
            if not all(isinstance(e, str) and e.strip() for e in errs):
                errors.append(f"{prefix} fail errors must be non-empty strings")
                continue
            if evids and not all(isinstance(e, str) and e.strip() for e in evids):
                errors.append(f"{prefix} fail evidence must be non-empty strings when present")
                continue
            if warns and not all(isinstance(w, str) and w.strip() for w in warns):
                errors.append(f"{prefix} fail warnings must be non-empty strings when present")
                continue
            if reason is not None and isinstance(reason, str) and reason.strip() == "":
                errors.append(f"{prefix} fail reason must be non-empty when present")
                continue
            # evidence_provenance already structurally checked above; no
            # verified provenance required for fail
        elif status == "partial":
            has_reason = isinstance(reason, str) and reason.strip()
            has_errors = bool(errs) and any(isinstance(e, str) and e.strip() for e in errs)
            if not (has_reason or has_errors):
                errors.append(f"{prefix} partial requires non-empty reason or non-empty errors")
                continue
            if has_errors and not all(isinstance(e, str) and e.strip() for e in errs):
                errors.append(f"{prefix} partial errors must be non-empty strings")
                continue
            if evids and not all(isinstance(e, str) and e.strip() for e in evids):
                errors.append(f"{prefix} partial evidence must be non-empty strings when present")
                continue
            if warns and not all(isinstance(w, str) and w.strip() for w in warns):
                errors.append(f"{prefix} partial warnings must be non-empty strings when present")
                continue
            if reason is not None and not has_reason and not has_errors:
                errors.append(f"{prefix} partial reason must be non-empty when errors empty")
                continue
        elif status in {"not_run", "skipped"}:
            if not isinstance(reason, str) or not reason.strip():
                errors.append(f"{prefix} {status} requires non-empty reason")
                continue
            if evids:
                errors.append(f"{prefix} {status} must not carry evidence (got {evids!r})")
                continue
            if errs or warns:
                errors.append(f"{prefix} {status} must not carry errors/warnings (got errors={errs!r} warnings={warns!r})")
                continue
            if isinstance(raw_provenance, list) and raw_provenance:
                if any(isinstance(p, dict) and p.get("verified") is True for p in raw_provenance):
                    errors.append(f"{prefix} {status} must not carry verified provenance")
                    continue
                errors.append(f"{prefix} {status} must not carry evidence_provenance (got {raw_provenance!r})")
                continue
        else:
            errors.append(f"{prefix} unknown status '{status}'")
            continue

        if (
            audit_id == "claim-source-alignment"
            and status in {"pass", "conditional-pass"}
        ):
            errors.extend(
                f"{prefix} claim-alignment bundle binding failed: {error}"
                for error in _claim_alignment_bundle_binding_errors(
                    item, claim_alignment_bundle_path
                )
            )

    # Top-level overall aggregation check
    overall = actual.get("overall")
    if isinstance(overall, str):
        opt_in_ids = set(_AUDIT_REGISTRY.opt_in_audit_ids())
        audit_statuses = [
            (str(a.get("audit_id")), str(a.get("status")))
            for a in audits
            if isinstance(a, dict) and a.get("status")
        ]
        if overall == "pass":
            offending = [
                f"{a.get('audit_id')}:{a.get('status')}"
                for a in audits
                if isinstance(a, dict)
                and a.get("status") != "pass"
                and not audit_not_run_is_consumer_exempt(a, opt_in_ids)
            ]
            if offending:
                errors.append(
                    f"overall pass aggregates non-pass audit(s): {', '.join(offending)}"
                )
        if overall == "conditional-pass":
            offending = [
                f"{a.get('audit_id')}:{a.get('status')}"
                for a in audits
                if isinstance(a, dict)
                and a.get("status") in {"fail", "partial", "not_run", "skipped"}
                and not audit_not_run_is_conditional_consumer_exempt(a, opt_in_ids)
            ]
            if offending:
                errors.append(
                    f"overall conditional-pass aggregates fail-like audit(s): {', '.join(offending)}"
                )

    return (len(errors) == 0, errors)


def _audits_ok(
    actual: dict[str, Any],
    expected_audit_ids: list[str],
    audited_path: str | None = None,
    expected_report_sha256: str | None = None,
    research_pack_path: str | None = None,
    expected_pack_sha256: str | None = None,
    report_text: str | None = None,
    pack_text: str | None = None,
    expected_route: str | None = None,
    claim_alignment_bundle_path: str | None = None,
) -> bool:
    """Boolean wrapper around :func:`_audit_consistency_details` for backwards compat.

    New code should call ``_audit_consistency_details`` to obtain locatable
    error messages (issue #408 P1).
    """
    ok, _ = _audit_consistency_details(
        actual, expected_audit_ids, audited_path, expected_report_sha256,
        research_pack_path, expected_pack_sha256, report_text, pack_text,
        expected_route, claim_alignment_bundle_path,
    )
    return ok


def _audit_provenance_details(
    item: dict[str, Any],
    audit_id: str,
    execution_type: str,
    execution_source: str,
    expected_target: str | None,
    expected_hash: str | None,
    report_text: str | None = None,
    pack_text: str | None = None,
    expected_route: str | None = None,
) -> tuple[bool, list[str]]:
    """Detailed provenance verification that returns locatable errors (issue #409).

    Same semantics as :func:`_audit_provenance_ok` but returns ``(ok, errors)``
    where ``errors`` contains specific diagnostics (e.g. ``not found in the
    visible report`` or ``target mismatch``) so callers can surface them
    instead of a generic ``pass provenance failed``.  This mirrors the
    ``_audit_consistency_details`` pattern introduced in #408.
    """
    errors: list[str] = []
    # Enforce the visible-artifact contract at this helper boundary too.  The
    # normal _evaluate_case path already supplies sanitized text, but callers
    # of this compatibility/helper API must not be able to pass raw Markdown
    # and re-enable fenced/HTML hidden evidence (issue #409 follow-up).
    visible_report_text = (
        sanitize_visible_markdown(report_text) if report_text is not None else None
    )
    visible_pack_text = (
        sanitize_visible_markdown(pack_text) if pack_text is not None else None
    )
    provenance = item.get("evidence_provenance")
    if not isinstance(provenance, list) or not provenance:
        return False, ["evidence_provenance must be a non-empty list"]
    if not any(isinstance(p, dict) for p in provenance):
        return False, ["evidence_provenance must contain at least one object"]
    verified_records = [
        p for p in provenance if isinstance(p, dict) and p.get("verified") is True
    ]
    if not verified_records:
        return False, ["evidence_provenance has no verified record"]
    for record in verified_records:
        if record.get("execution_source") != execution_source:
            return False, [
                f"provenance execution_source {record.get('execution_source')!r} != expected {execution_source!r}"
            ]
        if execution_type == "automated":
            if record.get("audit_id") != audit_id:
                return False, [
                    f"provenance audit_id {record.get('audit_id')!r} != expected {audit_id!r}"
                ]
            if record.get("validator_binding") != item.get("validator_binding"):
                return False, [
                    f"provenance validator_binding {record.get('validator_binding')!r} != expected {item.get('validator_binding')!r}"
                ]
            if record.get("validator_version") != EXPECTED_VALIDATOR_VERSION:
                return False, [
                    f"provenance validator_version {record.get('validator_version')!r} != expected {EXPECTED_VALIDATOR_VERSION!r}"
                ]
            if expected_target is not None:
                if record.get("target") != expected_target:
                    return False, [
                        f"provenance target {record.get('target')!r} != expected {expected_target!r}"
                    ]
            elif (
                not isinstance(record.get("target"), str)
                or not record.get("target").strip()
            ):
                return False, ["provenance target must be a non-empty string"]
            prov_input = record.get("input_sha256")
            if expected_hash is not None:
                if not isinstance(prov_input, str) or prov_input != expected_hash:
                    return False, [
                        f"provenance input_sha256 {prov_input!r} != expected {expected_hash!r}"
                    ]
            elif not isinstance(prov_input, str) or not prov_input:
                return False, ["provenance input_sha256 must be a non-empty string"]
        else:
            kind = record.get("kind")
            locator = record.get("locator")
            if not isinstance(kind, str) or not kind.strip():
                return False, ["provenance kind must be a non-empty string"]
            if not isinstance(locator, str) or not locator.strip():
                return False, ["provenance locator must be a non-empty string"]
            allowed_kinds = {
                "report_section": "report-section",
                "report_table": "report-table",
                "pack_section": "pack-section",
                "pack_table": "pack-table",
                "checklist_item": "checklist-item",
                "audit_record": "audit-record",
            }
            prefix = allowed_kinds.get(kind)
            if prefix is None:
                return False, [f"provenance kind {kind!r} is not allowed"]
            canonical = f"{prefix}:{locator.strip()}"
            evidence = item.get("evidence", [])
            if canonical not in evidence:
                return False, [
                    f"provenance locator {locator!r} (kind {kind}) not in evidence {evidence!r}"
                ]
            if report_text is not None or pack_text is not None:
                if kind in ("report_section", "report_table"):
                    artifact_text = visible_report_text
                    artifact_label = "report"
                elif kind in ("pack_section", "pack_table"):
                    artifact_text = visible_pack_text
                    artifact_label = "pack"
                else:
                    artifact_text = visible_report_text
                    artifact_label = "report"
                result = validate_evidence_reference(
                    canonical,
                    artifact_text=artifact_text,
                    base_dir=ROOT,
                    strict=True,
                    artifact_label=artifact_label,
                    execution_type=execution_type,
                    expected_audit_id=audit_id,
                    expected_artifact_sha256=expected_hash,
                    expected_route=expected_route,
                    report_text=visible_report_text,
                    pack_text=visible_pack_text,
                )
                if not result.is_valid:
                    # Propagate the underlying validator's diagnostic, which
                    # already contains "not found in the visible report/pack"
                    # for hidden locators (issue #409).
                    for err in result.errors:
                        errors.append(err)
                    return False, errors
                if not result.provenance or not result.provenance.get("verified"):
                    return False, [
                        f"provenance locator {locator!r} was not verified against visible {artifact_label}"
                    ]
    return True, []


def _audit_provenance_ok(
    item: dict[str, Any],
    audit_id: str,
    execution_type: str,
    execution_source: str,
    expected_target: str | None,
    expected_hash: str | None,
    report_text: str | None = None,
    pack_text: str | None = None,
    expected_route: str | None = None,
) -> bool:
    """Boolean wrapper around :func:`_audit_provenance_details` for backwards compat."""
    ok, _ = _audit_provenance_details(
        item, audit_id, execution_type, execution_source,
        expected_target, expected_hash,
        report_text=report_text, pack_text=pack_text, expected_route=expected_route,
    )
    return ok


def _audit_status_is_fail_like(audit_id: str, status: str, reason: str | None = None) -> bool:
    """Fail-like audit statuses, excluding default-off opt-in not_run (#419)."""
    if status in {"fail", "partial", "skipped"}:
        return True
    if status == "not_run":
        opt_in_ids = set(_AUDIT_REGISTRY.opt_in_audit_ids())
        if audit_not_run_is_conditional_consumer_exempt(
            {"audit_id": audit_id, "status": status, "reason": reason},
            opt_in_ids,
        ):
            return False
        return True
    return False


def _overall_consistency_details(
    actual: dict[str, Any], returncode: int | None
) -> tuple[bool, list[str]]:
    """Detailed overall/returncode validation with locatable errors (issue #408 P1).

    Returns ``(ok, errors)``.  Errors are prefixed with ``overall`` or
    ``returncode`` so they are directly locatable in CI output.
    """
    errors: list[str] = []
    overall = actual.get("overall")
    if overall not in {"pass", "conditional-pass", "fail"}:
        errors.append(f"overall unknown status '{overall}' (expected pass/conditional-pass/fail)")
        return False, errors
    if returncode is not None:
        expected_rc = {"pass": 0, "conditional-pass": 1, "fail": 2}.get(overall)
        if expected_rc is not None and returncode != expected_rc:
            errors.append(f"returncode {returncode} does not match overall '{overall}' (expected {expected_rc})")
    audits = actual.get("audits") or []
    validators = actual.get("validators") or []
    blocking = actual.get("blocking") or []
    audit_statuses = [
        str(a.get("status"))
        for a in audits
        if isinstance(a, dict) and a.get("status")
    ]
    validator_statuses = [
        str(v.get("status"))
        for v in validators
        if isinstance(v, dict) and v.get("status")
    ]
    has_fail_like = any(
        _audit_status_is_fail_like(
            str(a.get("audit_id") or ""),
            str(a.get("status") or ""),
            a.get("reason") if isinstance(a.get("reason"), str) else None,
        )
        for a in audits
        if isinstance(a, dict) and a.get("status")
    )
    has_conditional = any(s == "conditional-pass" for s in audit_statuses)
    has_conditional_not_run = any(
        isinstance(a, dict)
        and a.get("status") == "not_run"
        and isinstance(a.get("reason"), str)
        and a.get("reason") == OPT_IN_AGGREGATE_NOT_RUN_REASON
        for a in audits
    )
    has_validator_fail = any(s in {"fail", "incomplete"} for s in validator_statuses)
    has_validator_conditional = any(s == "conditional-pass" for s in validator_statuses)
    if overall == "pass":
        if has_fail_like:
            offending = [
                f"{a.get('audit_id')}:{a.get('status')}"
                for a in audits
                if isinstance(a, dict)
                and _audit_status_is_fail_like(
                    str(a.get("audit_id") or ""),
                    str(a.get("status") or ""),
                    a.get("reason") if isinstance(a.get("reason"), str) else None,
                )
            ]
            errors.append(f"overall pass aggregates fail-like audit(s): {', '.join(offending)}")
        non_exempt_not_run = [
            f"{a.get('audit_id')}:{a.get('status')}"
            for a in audits
            if isinstance(a, dict)
            and a.get("status") == "not_run"
            and not audit_not_run_is_consumer_exempt(
                a, set(_AUDIT_REGISTRY.opt_in_audit_ids())
            )
        ]
        if non_exempt_not_run:
            errors.append(
                "overall pass aggregates NOT_RUN audit(s): "
                f"{', '.join(non_exempt_not_run)}"
            )
        if has_conditional:
            offending = [f"{a.get('audit_id')}:{a.get('status')}" for a in audits if isinstance(a, dict) and a.get("status") == "conditional-pass"]
            errors.append(f"overall pass aggregates conditional-pass audit(s): {', '.join(offending)}")
        if has_validator_fail:
            offending = [f"{v.get('validator_id')}:{v.get('status')}" for v in validators if isinstance(v, dict) and v.get("status") in {"fail", "incomplete"}]
            errors.append(f"overall pass aggregates validator fail(s): {', '.join(offending)}")
        if has_validator_conditional:
            offending = [f"{v.get('validator_id')}:{v.get('status')}" for v in validators if isinstance(v, dict) and v.get("status") == "conditional-pass"]
            errors.append(f"overall pass aggregates validator conditional-pass: {', '.join(offending)}")
        if blocking:
            errors.append(f"overall pass must have no blocking (got {blocking[:2]!r})")
    elif overall == "conditional-pass":
        if has_fail_like:
            offending = [
                f"{a.get('audit_id')}:{a.get('status')}"
                for a in audits
                if isinstance(a, dict)
                and _audit_status_is_fail_like(
                    str(a.get("audit_id") or ""),
                    str(a.get("status") or ""),
                    a.get("reason") if isinstance(a.get("reason"), str) else None,
                )
            ]
            errors.append(f"overall conditional-pass aggregates fail-like audit(s): {', '.join(offending)}")
        if has_validator_fail:
            offending = [f"{v.get('validator_id')}:{v.get('status')}" for v in validators if isinstance(v, dict) and v.get("status") in {"fail", "incomplete"}]
            errors.append(f"overall conditional-pass aggregates validator fail(s): {', '.join(offending)}")
        if not (
            has_conditional
            or has_conditional_not_run
            or has_validator_conditional
        ):
            errors.append("overall conditional-pass requires at least one conditional-pass audit or validator")
        if blocking:
            errors.append(f"overall conditional-pass must have no blocking (got {blocking[:2]!r})")
    elif overall == "fail":
        if not (has_fail_like or has_validator_fail or blocking):
            errors.append("overall fail is unlocatable: no fail-like audit, no validator fail, and no blocking message")
    return (len(errors) == 0, errors)


def _overall_and_returncode_consistent(
    actual: dict[str, Any], returncode: int | None
) -> bool:
    """Boolean wrapper around :func:`_overall_consistency_details` for backwards compat."""
    ok, _ = _overall_consistency_details(actual, returncode)
    return ok


def _blocking_ids_are_allowed(actual: dict[str, Any], allowed: set[str]) -> bool:
    for message in actual.get("blocking", []):
        match = re.match(r"\[([^\]]+)\]", str(message))
        if match and match.group(1) not in allowed:
            return False
    return True


def _blocking_ids_are_exact(actual: dict[str, Any], allowed: set[str]) -> bool:
    """Require every blocking message to carry one of the allowed sources."""
    blocking = actual.get("blocking", [])
    if not blocking:
        return False
    return all(
        (match := re.match(r"\[([^\]]+)\]", str(message))) is not None
        and match.group(1) in allowed
        for message in blocking
    )


def _negative_structure_matches(case: dict[str, Any], actual: dict[str, Any], checks: dict[str, bool]) -> bool:
    """Require the intended defect shape, not merely any failing audit."""
    family = case.get("failure_family")
    if family == "route-misclassification":
        # The activation snapshot must be correct while the report artifact
        # deliberately carries the wrong primary route.
        return all(
            [
                checks["activation_route_match"],
                not checks["report_route_match"],
                checks["activation_secondary_routes_match"],
                checks["report_secondary_routes_match"],
                checks["parallelization_match"],
                checks["prompt_identity_match"],
                checks["activation_snapshot_match"],
                checks["statuses_match"],
                _blocking_ids_are_exact(actual, {"contract-check"}),
            ]
        )

    common = [
        checks["activation_route_match"],
        checks["report_route_match"],
        checks["activation_report_consistent"],
        checks["activation_secondary_routes_match"],
        checks["report_secondary_routes_match"],
        checks["disciplines_match"],
        checks["pack_fields_present"],
        checks["parallelization_match"],
        checks["prompt_identity_match"],
        checks["decision_tree_version_match"],
        checks["statuses_match"],
    ]
    statuses = _audit_statuses(actual)
    audit_reasons = {
        str(item.get("audit_id")): item.get("reason")
        for item in actual.get("audits", [])
        if isinstance(item, dict) and item.get("audit_id")
    }

    def _is_fail_like(audit_id: str, status: str) -> bool:
        reason = audit_reasons.get(audit_id)
        reason_str = reason if isinstance(reason, str) else None
        return _audit_status_is_fail_like(audit_id, status, reason_str)

    expected_audits = set(case["expected"].get("required_audits", []))
    if family == "secondary-route-not-verified":
        secondary_targets = {
            f"{route}-secondary-hard-fail"
            for route in case["expected"].get("secondary_routes", [])
        }
        target_present_and_failed = any(
            audit_id in secondary_targets and _is_fail_like(audit_id, statuses.get(audit_id, ""))
            for audit_id in secondary_targets
        )
        primary_ids = expected_audits - secondary_targets
        failed_ids = {
            audit_id for audit_id, status in statuses.items()
            if _is_fail_like(audit_id, status)
        }
        return (
            all(common)
            and all(audit_id in statuses and statuses[audit_id] == "pass" for audit_id in primary_ids)
            and failed_ids.issubset(secondary_targets)
            and _blocking_ids_are_allowed(actual, {"contract-check", *secondary_targets})
            and target_present_and_failed
        )
    if family == "declared-not-executed":
        target_present_and_unrun = any(
            audit_id in expected_audits and statuses.get(audit_id) in {"not_run", "partial", "skipped"}
            for audit_id in expected_audits
        )
        failed_ids = {
            audit_id for audit_id, status in statuses.items()
            if _is_fail_like(audit_id, status)
        }
        allowed_targets = {
            audit_id
            for audit_id in expected_audits
            if statuses.get(audit_id) in {"not_run", "partial", "skipped"}
        }
        return (
            all(common)
            and failed_ids.issubset(allowed_targets)
            and _blocking_ids_are_allowed(actual, allowed_targets)
            and target_present_and_unrun
        )
    return all(common)


def _evaluate_case(
    case: dict[str, Any], expected_decision_tree_version: int | None = None
) -> dict[str, Any]:
    expected = case["expected"]
    input_data = case["input"]
    fixtures = case["fixtures"]
    evaluation_mode = case.get("evaluation_mode", "structured-decision-replay")
    report = ROOT / fixtures["report"]
    research_pack = ROOT / fixtures["research_pack"]
    pack = _pack_observation(research_pack)
    # External trust anchor: compute the artifact hashes ourselves rather than
    # trusting any hash embedded in the audit JSON (issue #403 P1).  A None here
    # (unreadable file) fails the downstream bindings closed.
    expected_report_sha256 = _sha256(report)
    expected_pack_sha256 = _sha256(research_pack)
    # Visible texts for evidence re-validation (manual/process provenance must
    # be anchored to a real heading/table/checklist item, not just a JSON-
    # self-consistent evidence+provenance pair).  Hashes above remain raw-byte
    # anchored; only the locator lookup uses the canonical visible sanitizer
    # (issue #409: fences / raw HTML must not contribute heading/table evidence).
    try:
        raw_report_text = report.read_text(encoding="utf-8", errors="replace")
        report_text_for_provenance = sanitize_visible_markdown(raw_report_text)
    except OSError:
        report_text_for_provenance = None
    try:
        raw_pack_text = research_pack.read_text(encoding="utf-8", errors="replace")
        pack_text_for_provenance = sanitize_visible_markdown(raw_pack_text)
    except OSError:
        pack_text_for_provenance = None

    activation_error: str | None = None
    activation_snapshot_error: str | None = None
    activation_snapshot_data: dict[str, Any] | None = None
    activation_snapshot_path: Path | None = None
    try:
        activation = activate_prompt(
            input_data["user_prompt"],
            input_data["parallelization_decision"],
            action_category=input_data["action_burden"],
            weight_bearing_object=input_data["weight_bearing_object"],
            secondary_routes=input_data["secondary_routes"],
            secondary_route_contracts=input_data.get("secondary_route_contracts", {}),
            expected_prompt_sha256=input_data["prompt_sha256"],
        )
    except RouteActivationError as exc:
        activation = None
        activation_error = str(exc)

    if evaluation_mode == "activation-record-integration":
        activation_snapshot_path = ROOT / fixtures["activation_snapshot"]
        try:
            activation_snapshot_data = load_activation_snapshot(
                activation_snapshot_path
            )
            if activation is None:
                raise ActivationSnapshotError(
                    "structured activation did not produce a snapshot"
                )
            expected_snapshot = build_activation_snapshot(
                case["id"], activation, evaluation_mode=evaluation_mode
            )
            if activation_snapshot_data != expected_snapshot:
                raise ActivationSnapshotError(
                    "fixture activation snapshot does not match the structured "
                    "activation result"
                )
        except (ActivationSnapshotError, OSError, KeyError) as exc:
            activation_snapshot_error = str(exc)

    audit_data, runner_error, returncode = _run_audit(
        report,
        research_pack,
        activation_snapshot=activation_snapshot_path,
    )

    contract: dict[str, Any] = {}
    if report.is_file():
        contract = extract_contract_from_markdown(
            report.read_text(encoding="utf-8", errors="replace")
        ) or {}

    report_route = audit_data.get("route") if audit_data else None
    actual_statuses = {
        "research_status": pack["statuses"].get("research_status"),
        "audit_status": audit_data.get("overall") if audit_data else None,
        "delivery_status": pack["statuses"].get("delivery_status"),
    }
    requires_decision_tree = "Decision tree path" in expected["research_pack_fields"]
    decision_tree_version_match = (
        not requires_decision_tree
        or (
            expected_decision_tree_version is not None
            and activation is not None
            and activation.decision_tree_version == expected_decision_tree_version
            and pack["decision_tree_version"] == expected_decision_tree_version
        )
    )
    actual = {
        "route": report_route,
        "report_route": report_route,
        "activation_route": activation.primary_route if activation else None,
        "activation_secondary_routes": sorted(activation.secondary_routes) if activation else [],
        "activation_action_category": activation.action_category if activation else None,
        "activation_weight_bearing_object": activation.weight_bearing_object if activation else None,
        "activation_parallelization_decision": activation.parallelization_decision if activation else None,
        "activation_prompt_sha256": activation.prompt_sha256 if activation else None,
        "activation_decision_tree_version": (
            activation.decision_tree_version if activation else None
        ),
        "pack_decision_tree_version": pack["decision_tree_version"],
        "activation_error": activation_error,
        "evaluation_mode": evaluation_mode,
        "activation_snapshot_error": activation_snapshot_error,
        "activation_snapshot": (
            activation_reference(activation_snapshot_data)
            if activation_snapshot_data is not None
            else None
        ),
        "contract_activation_snapshot": contract.get("activation_snapshot"),
        "pack_activation_snapshot": pack.get("activation_snapshot"),
        "closest_alternative": contract.get("closest_alternative"),
        "secondary_routes": sorted(contract.get("secondary_routes", []) or []),
        "disciplines": sorted(contract.get("disciplines", []) or []),
        "audit_ids": sorted(
            {
                str(item["audit_id"])
                for item in (audit_data or {}).get("audits", [])
                if isinstance(item, dict) and item.get("audit_id")
            }
        ),
        "audits": (audit_data or {}).get("audits", []),
        "validators": (audit_data or {}).get("validators", []),
        "schema_version": (audit_data or {}).get("schema_version"),
        "validator_version": (audit_data or {}).get("validator_version"),
        "input_sha256": (audit_data or {}).get("input_sha256"),
        "overall": (audit_data or {}).get("overall"),
        "blocking": (audit_data or {}).get("blocking", []),
        "statuses": actual_statuses,
        "pack_fields": pack["fields"],
        "pack_missing_required_fields": pack["missing_required_fields"],
        "returncode": returncode,
        "runner_error": runner_error,
        "expected_route": expected["primary_route"],
    }
    actual["failure_family"] = _detect_failure_family(case, actual)
    actual["gap_class"] = gap_class_for_failure_family(actual["failure_family"])
    actual["failure_stage"] = failure_stage_for_failure_family(
        actual["failure_family"]
    )

    expected_pack_fields = set(expected["research_pack_fields"])
    # Issue #403: derive the canonical expected audit set from the registries
    # (route required audits + delivery-scope global audits + secondary
    # hard-fail audits) instead of trusting the case's declared required_audits
    # subset, and require the executed audit results to match it exactly — no
    # missing, duplicate, unknown, or forged-extra result — and to be internally
    # consistent (status/errors/warnings/evidence/provenance/binding).
    # Issue #407: negative cases must share the same fail-closed audit-set gate
    # as positives.  Duplicate detection is performed on the raw list before
    # set conversion so a forged duplicate is not hidden by de-duplication.
    # For route-misclassification the report's actual route differs from the
    # expected activation route; the audit set must be verified against the
    # report's declared route (the artifact under test), otherwise the genuine
    # negative would always fail its audit-set check and baseline 11/11 would
    # be impossible.
    if case.get("failure_family") == "route-misclassification" and actual.get("report_route"):
        audit_route_for_set = actual["report_route"]
        audit_secondary_for_set = actual.get("secondary_routes") or expected["secondary_routes"]
        audit_expected_route = actual["report_route"]
    else:
        audit_route_for_set = expected["primary_route"]
        audit_secondary_for_set = expected["secondary_routes"]
        audit_expected_route = expected["primary_route"]
    try:
        expected_audit_ids = _expected_audit_set(
            audit_route_for_set, audit_secondary_for_set
        )
    except registry_loader.UnknownRouteError:
        expected_audit_ids = None
    raw_audit_ids = [
        str(item.get("audit_id"))
        for item in actual.get("audits", [])
        if isinstance(item, dict) and item.get("audit_id")
    ]
    has_no_duplicates = len(raw_audit_ids) == len(set(raw_audit_ids))
    if expected_audit_ids is None:
        audit_set_exact = False
        audits_consistent = False
        audit_consistency_errors: list[str] = ["unknown route for expected audit set (registry drift)"]
        audit_set_ok = False  # registry drift → fail closed
    else:
        audit_set_exact = has_no_duplicates and sorted(actual["audit_ids"]) == expected_audit_ids
        audits_consistent, audit_consistency_errors = _audit_consistency_details(
            actual,
            expected_audit_ids,
            audited_path=str(report),
            expected_report_sha256=expected_report_sha256,
            research_pack_path=str(research_pack),
            expected_pack_sha256=expected_pack_sha256,
            report_text=report_text_for_provenance,
            pack_text=pack_text_for_provenance,
            expected_route=audit_expected_route,
        )
        # Duplicate audit_ids are already reported via _audit_consistency_details,
        # but audit_set_exact gives a fast pre-check for the common truncation case.
        if not has_no_duplicates:
            audit_consistency_errors = [f"duplicate audit_id '{next(x for x in raw_audit_ids if raw_audit_ids.count(x) > 1)}'"] + audit_consistency_errors
        if sorted(actual["audit_ids"]) != expected_audit_ids:
            # _audit_consistency_details already reports missing/extra, keep both for
            # backwards compat but avoid duplicate noise in the final list
            pass
        audit_set_ok = audit_set_exact and audits_consistent
    activation_route_match = actual["activation_route"] == expected["primary_route"]
    report_route_match = actual["report_route"] == expected["primary_route"]
    activation_report_consistent = actual["activation_route"] == actual["report_route"]
    alternative_match = actual["closest_alternative"] == expected["closest_alternative"]
    activation_secondary_match = (
        actual["activation_secondary_routes"] == sorted(expected["secondary_routes"])
    )
    report_secondary_match = actual["secondary_routes"] == sorted(expected["secondary_routes"])
    secondary_match = activation_secondary_match and report_secondary_match
    discipline_match = actual["disciplines"] == sorted(expected["disciplines"])
    audit_ids_match = audit_set_ok
    pack_fields_match = expected_pack_fields.issubset(set(actual["pack_fields"]))
    status_match = actual["statuses"] == expected["statuses"]
    parallelization_match = (
        actual["activation_parallelization_decision"]
        == expected["parallelization_decision"]
    )
    prompt_identity_match = actual["activation_prompt_sha256"] == input_data["prompt_sha256"]
    activation_snapshot_match = (
        evaluation_mode != "activation-record-integration"
        or (
            actual["activation_snapshot_error"] is None
            and actual["activation_snapshot"] is not None
            and actual["contract_activation_snapshot"] == actual["activation_snapshot"]
            and actual["pack_activation_snapshot"] == actual["activation_snapshot"]
        )
    )
    expected_returncode = {
        "pass": 0,
        "conditional-pass": 1,
        "fail": 2,
    }.get(expected["statuses"]["audit_status"])

    # The audit must have dispatched exactly the resolved route's canonical
    # validator binding set; the runner fails closed on missing / forged ids.
    expected_validators: list[str] = []
    if actual["route"]:
        try:
            expected_validators = _ROUTE_REGISTRY.validators_for(actual["route"])
        except registry_loader.UnknownRouteError:
            expected_validators = []
    validators_ok = _validators_ok(
        actual,
        expected_validators,
        audited_path=str(report),
        expected_input_sha256=expected_report_sha256,
    )
    overall_and_returncode_ok, overall_consistency_errors = _overall_consistency_details(actual, returncode)
    if expected["verdict"] == "pass":
        case_passed = all(
            [
                activation_route_match,
                report_route_match,
                activation_report_consistent,
                alternative_match,
                secondary_match,
                discipline_match,
                audit_ids_match,
                pack_fields_match,
                status_match,
                parallelization_match,
                prompt_identity_match,
                decision_tree_version_match,
                activation_snapshot_match,
                validators_ok,
                overall_and_returncode_ok,
                actual["overall"] == expected["statuses"]["audit_status"],
                returncode == expected_returncode,
            ]
        )
    else:
        negative_returncode_ok = (
            returncode == 2
            if evaluation_mode == "activation-record-integration"
            else returncode in {0, 1}
            if case.get("failure_family") == "route-misclassification"
            else returncode == 2
        )
        checks_for_negative = {
            "activation_route_match": activation_route_match,
            "report_route_match": report_route_match,
            "activation_report_consistent": activation_report_consistent,
            "activation_secondary_routes_match": activation_secondary_match,
            "report_secondary_routes_match": report_secondary_match,
            "disciplines_match": discipline_match,
            "pack_fields_present": pack_fields_match,
            "parallelization_match": parallelization_match,
            "prompt_identity_match": prompt_identity_match,
            "decision_tree_version_match": decision_tree_version_match,
            "activation_snapshot_match": activation_snapshot_match,
            "statuses_match": status_match,
        }
        case_passed = all(
            [
                actual["failure_family"] == case["failure_family"],
                _negative_structure_matches(case, actual, checks_for_negative),
                audit_ids_match,
                validators_ok,
                overall_and_returncode_ok,
                actual["overall"] == expected["statuses"]["audit_status"],
                negative_returncode_ok,
            ]
        )

    return {
        "case_id": case["id"],
        "passed": case_passed,
        "expected": {
            "route": expected["primary_route"],
            "closest_alternative": expected["closest_alternative"],
            "secondary_routes": expected["secondary_routes"],
            "statuses": expected["statuses"],
            "verdict": expected["verdict"],
            "failure_family": case["failure_family"],
            "gap_class": gap_class_for_failure_family(case["failure_family"]),
            "evaluation_mode": evaluation_mode,
            "failure_stage": expected.get("failure_stage"),
        },
        "actual": {
            "route": actual["route"],
            "report_route": actual["report_route"],
            "activation_route": actual["activation_route"],
            "activation_secondary_routes": actual["activation_secondary_routes"],
            "activation_action_category": actual["activation_action_category"],
            "activation_weight_bearing_object": actual["activation_weight_bearing_object"],
            "activation_parallelization_decision": actual["activation_parallelization_decision"],
            "activation_prompt_sha256": actual["activation_prompt_sha256"],
            "activation_decision_tree_version": actual["activation_decision_tree_version"],
            "pack_decision_tree_version": actual["pack_decision_tree_version"],
            "activation_error": actual["activation_error"],
            "closest_alternative": actual["closest_alternative"],
            "secondary_routes": actual["secondary_routes"],
            "disciplines": actual["disciplines"],
            "audit_ids": actual["audit_ids"],
            "audits": actual["audits"],
            "validators": actual["validators"],
            "schema_version": actual["schema_version"],
            "blocking": actual["blocking"],
            "statuses": actual["statuses"],
            "overall": actual["overall"],
            "failure_family": actual["failure_family"],
            "gap_class": actual["gap_class"],
            "failure_stage": actual["failure_stage"],
            "evaluation_mode": actual["evaluation_mode"],
            "activation_snapshot_error": actual["activation_snapshot_error"],
            "activation_snapshot": actual["activation_snapshot"],
            "contract_activation_snapshot": actual["contract_activation_snapshot"],
            "pack_activation_snapshot": actual["pack_activation_snapshot"],
            "pack_missing_required_fields": actual["pack_missing_required_fields"],
            "returncode": returncode,
            "runner_error": runner_error,
        },
        "checks": {
            "activation_route_match": activation_route_match,
            "report_route_match": report_route_match,
            "activation_report_consistent": activation_report_consistent,
            "alternative_match": alternative_match,
            "activation_secondary_routes_match": activation_secondary_match,
            "report_secondary_routes_match": report_secondary_match,
            "secondary_routes_match": secondary_match,
            "disciplines_match": discipline_match,
            "required_audits_present": audit_ids_match,
            "audit_set_exact": audit_set_exact,
            "audits_consistent": audits_consistent,
            "audit_consistency_errors": audit_consistency_errors,
            "pack_fields_present": pack_fields_match,
            "statuses_match": status_match,
            "parallelization_match": parallelization_match,
            "prompt_identity_match": prompt_identity_match,
            "decision_tree_version_match": decision_tree_version_match,
            "activation_snapshot_match": activation_snapshot_match,
            "validators_ok": validators_ok,
            "overall_and_returncode_ok": overall_and_returncode_ok,
            "overall_consistency_errors": overall_consistency_errors,
        },
    }


def _metrics(cases: list[dict[str, Any]], results: list[dict[str, Any]]) -> dict[str, Any]:
    by_id = {result["case_id"]: result for result in results}
    positives = [case for case in cases if case["type"] == "positive"]
    negatives = [case for case in cases if case["type"] == "negative"]
    structured_positive_cases = [
        case
        for case in positives
        if case.get("evaluation_mode", "structured-decision-replay")
        == "structured-decision-replay"
    ]
    integration_positive_cases = [
        case
        for case in positives
        if case.get("evaluation_mode") == "activation-record-integration"
    ]
    integration_negative_cases = [
        case
        for case in negatives
        if case.get("evaluation_mode") == "activation-record-integration"
    ]
    oracle_mismatch_cases = [
        case
        for case in negatives
        if case.get("failure_family") == "route-misclassification"
    ]
    boundary_cases = [
        case
        for case in positives
        if case["expected"].get("closest_alternative") is not None
    ]
    boundary_resolved = sum(
        by_id[case["id"]]["checks"]["alternative_match"] for case in boundary_cases
    )
    structured_route_correct = sum(
        by_id[case["id"]]["checks"]["activation_route_match"]
        for case in structured_positive_cases
    )
    report_route_consistent = sum(
        by_id[case["id"]]["checks"]["activation_report_consistent"]
        for case in integration_positive_cases
    )
    secondary_cases = [
        case for case in negatives if case.get("failure_family") == "secondary-route-not-verified"
    ]
    secondary_recalled = sum(
        by_id[case["id"]]["actual"]["failure_family"] == "secondary-route-not-verified"
        for case in secondary_cases
    )
    declared_cases = [
        case for case in negatives if case.get("failure_family") == "declared-not-executed"
    ]
    declared_recalled = sum(
        by_id[case["id"]]["actual"]["failure_family"] == "declared-not-executed"
        for case in declared_cases
    )
    pack_complete = sum(
        result["checks"]["pack_fields_present"] for result in results
    )
    declared_not_executed_observed = sum(
        any(
            item.get("execution_type") in {"manual", "process"}
            and item.get("status") in {"not_run", "partial", "skipped"}
            for item in result["actual"].get("audits", [])
        )
        for result in results
    )
    integration_false_passed = sum(
        by_id[case["id"]]["actual"]["overall"] == "pass"
        for case in integration_negative_cases
    )
    oracle_mismatch_detected = sum(
        by_id[case["id"]]["actual"]["failure_family"]
        == "route-misclassification"
        for case in oracle_mismatch_cases
    )
    status_cases = [
        case
        for case in cases
        if case["expected"].get("statuses", {}).get("research_status") in {"blocked", "partial"}
        or case["expected"].get("statuses", {}).get("delivery_status") == "pdf_failed"
    ]
    status_correct = sum(
        by_id[case["id"]]["checks"]["statuses_match"] for case in status_cases
    )
    return {
        "case_count": len(cases),
        "positive_case_count": len(positives),
        "negative_case_count": len(negatives),
        "case_pass_count": sum(result["passed"] for result in results),
        "structured_route_resolution_rate": _ratio(
            structured_route_correct, len(structured_positive_cases)
        ),
        "activation_report_consistency": _ratio(
            report_route_consistent, len(integration_positive_cases)
        ),
        "parallelization_decision_consistency": _ratio(
            sum(result["checks"]["parallelization_match"] for result in results),
            len(results),
        ),
        "boundary_resolution_rate": _ratio(boundary_resolved, len(boundary_cases)),
        "pack_completeness": _ratio(pack_complete, len(results)),
        "secondary_hard_fail_recall": _ratio(secondary_recalled, len(secondary_cases)),
        "declared_not_executed_recall": _ratio(declared_recalled, len(declared_cases)),
        "declared_not_executed_rate": _ratio(declared_not_executed_observed, len(results)),
        "audit_false_pass_rate": _ratio(
            integration_false_passed, len(integration_negative_cases)
        ),
        "oracle_mismatch_detection_rate": _ratio(
            oracle_mismatch_detected, len(oracle_mismatch_cases)
        ),
        "negative_case_contract_pass_rate": _ratio(
            sum(by_id[case["id"]]["passed"] for case in negatives),
            len(negatives),
        ),
        "blocked_partial_and_pdf_failed_status_correctness": _ratio(
            status_correct, len(status_cases)
        ),
    }


def _check_baseline(metrics: dict[str, Any], baseline_path: Path) -> list[str]:
    if not baseline_path.is_file():
        return [f"metrics baseline not found: {baseline_path}"]
    try:
        baseline = _read_json(baseline_path)
    except (OSError, json.JSONDecodeError) as exc:
        return [f"metrics baseline is invalid: {exc}"]
    expected = baseline.get("metrics") if isinstance(baseline, dict) else None
    if not isinstance(expected, dict):
        return ["metrics baseline must contain an object field named 'metrics'"]
    mismatches = []
    for key, value in expected.items():
        if metrics.get(key) != value:
            mismatches.append(f"{key}: expected {value!r}, got {metrics.get(key)!r}")
    return mismatches


def run(registry_path: Path = DEFAULT_REGISTRY_PATH, *, check_baseline: bool = False) -> dict[str, Any]:
    registry = load_registry(registry_path)
    cases = active_cases(registry)
    results = [
        _evaluate_case(case, registry["decision_tree_version"])
        for case in cases
    ]
    metrics = _metrics(cases, results)
    baseline_errors = (
        _check_baseline(metrics, DEFAULT_BASELINE_PATH) if check_baseline else []
    )
    failed_cases = [result for result in results if not result["passed"]]
    return {
        "registry_version": registry["version"],
        "decision_tree_version": registry["decision_tree_version"],
        "offline": True,
        "evaluation_mode": "offline",
        "case_evaluation_modes": {
            mode: sum(
                case.get("evaluation_mode", "structured-decision-replay") == mode
                for case in cases
            )
            for mode in sorted(
                {
                    case.get("evaluation_mode", "structured-decision-replay")
                    for case in cases
                }
            )
        },
        "metrics": metrics,
        "baseline_errors": baseline_errors,
        "passed": not failed_cases and not baseline_errors,
        "failed_cases": failed_cases,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run offline route-sharp forward evals")
    parser.add_argument(
        "--registry",
        type=Path,
        default=DEFAULT_REGISTRY_PATH,
        help="path to the eval registry JSON",
    )
    parser.add_argument(
        "--offline",
        action="store_true",
        help="explicitly document the offline execution mode (the default)",
    )
    parser.add_argument(
        "--check-baseline",
        action="store_true",
        help="compare metrics with evals/forward-metrics-baseline.json",
    )
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = parser.parse_args(argv)

    try:
        report = run(args.registry, check_baseline=args.check_baseline)
    except EvalRegistryError as exc:
        report = {
            "registry_version": None,
            "offline": True,
            "metrics": {},
            "baseline_errors": [],
            "passed": False,
            "failed_cases": [],
            "gap_class": "fixture-reference-drift",
            "registry_error": str(exc),
        }

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        if report.get("registry_error"):
            print(f"Registry validation failed: {report['registry_error']}")
        else:
            status = "PASS" if report["passed"] else "FAIL"
            print(f"{status}: {report['metrics']['case_count']} offline forward cases")
            print(json.dumps(report["metrics"], ensure_ascii=False, indent=2, sort_keys=True))
            for result in report["failed_cases"]:
                print(f"- FAIL {result['case_id']}: {result['actual']}")
            for error in report["baseline_errors"]:
                print(f"- BASELINE {error}")
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
