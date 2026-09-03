#!/usr/bin/env python3
"""Fail-closed validator for parallel-research Track Handoffs (issue #416).

A Track Handoff is the typed artifact one parallel research track returns to
the parent synthesizer.  Producers run this validation before handing off;
the parent re-runs it before merging.  Any structural problem — including a
missing file or unparseable JSON — is reported as ``HANDOFF_INCOMPLETE`` and
must never be interpretable as "no findings".

Single-track research does not create Track Handoffs and never invokes this
validator.

Exit codes:
    0 = handoff is schema-valid (and expected track id matched, if given)
    2 = fail closed: missing file, bad JSON, or any validation issue

Usage:
    python3 scripts/validate_track_handoff.py <handoff.json> \\
        [--expected-track-id <id>] [--expected-handoff-id <id>] \\
        [--expected-question <text>] [--expected-artifact-id <id>] \\
        [--expected-scope-file <dispatch-scope.json>]

Identity bindings: track_id only proves the track name; pass
--expected-handoff-id (dispatch/run identity) or --expected-question to
reject stale or misrouted handoffs from a previous run,
--expected-artifact-id to bind the handoff to the downstream artifact, and
--expected-scope-file to verify the track executed within its assigned
scope/timeframe boundary.
When --run-state is supplied, the handoff must bind to that Run State's
artifact_id and listed handoff_id (issue #417, #426: no sha256). Omitting
--run-state preserves the #416 single-handoff path.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

HANDOFF_INCOMPLETE = "HANDOFF_INCOMPLETE"

SCHEMA_VERSION = "1"
ALLOWED_STATUS = ("complete", "partial", "blocked")
ALLOWED_RESOLUTION_STATUS = ("resolved", "unresolved")
ALLOWED_EVIDENCE_ROLES = ("observed", "primary", "secondary", "inferred", "unknown")

REQUIRED_TOP_LEVEL = frozenset(
    {
        "schema_version",
        "handoff_id",
        "track_id",
        "question",
        "scope",
        "source_register",
        "findings",
        "conflicts",
        "unknowns",
        "implications",
        "status",
        "generated_at",
    }
)
# Optional top-level fields: conditional status explanations plus the
# Run State artifact_ref used when merging with --run-state (issue #417).
OPTIONAL_TOP_LEVEL = frozenset({"status_reason", "recovery_action", "artifact_ref"})
KNOWN_TOP_LEVEL = REQUIRED_TOP_LEVEL | OPTIONAL_TOP_LEVEL

SCOPE_REQUIRED = frozenset({"in_scope", "out_of_scope", "timeframe", "geography"})
SOURCE_REQUIRED = frozenset({"source_id", "title", "url"})
SOURCE_OPTIONAL = frozenset()
FINDING_REQUIRED = frozenset(
    {"finding_id", "claim", "evidence_refs", "evidence_role", "confidence"}
)
FINDING_OPTIONAL = frozenset({"limitations"})
CONFLICT_REQUIRED = frozenset(
    {"topic", "finding_refs", "resolution_status", "affects_overall_question"}
)
CONFLICT_OPTIONAL = frozenset({"resolution_note"})
UNKNOWN_REQUIRED = frozenset({"description", "reason", "impact", "next_action"})
ARTIFACT_REF_REQUIRED = frozenset({"artifact_id"})

# Shape gate for ISO-8601 date (2026-08-24) or RFC 3339 timestamp.  The
# regex only checks digit/separator shape; real calendar validity is checked
# separately via date/datetime.fromisoformat so impossible values such as
# 2026-02-31 fail closed.
_TIMESTAMP_RE = re.compile(
    r"^(\d{4}-\d{2}-\d{2})"
    r"(?:[Tt](\d{2}:\d{2}(?::\d{2}(?:\.\d+)?))([Zz]|[+-]\d{2}:\d{2})?)?$"
)


def _is_valid_timestamp(value: object) -> bool:
    """True for a real calendar date or a timezone-aware RFC 3339 datetime."""
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
        # Normalize RFC 3339's lowercase 'z' designator for fromisoformat.
        zone = (zone_part or "").replace("z", "Z").replace("Z", "+00:00")
        dt = datetime.fromisoformat(f"{date_part}T{time_part}{zone}")
    except ValueError:
        return False
    # RFC 3339 timestamps carry an explicit UTC offset; naive datetimes are
    # ambiguous about when the handoff was produced, so they fail closed.
    return dt.tzinfo is not None

EXIT_OK = 0
EXIT_FAIL_CLOSED = 2


class HandoffIncomplete(Exception):
    """Raised when a consumer receives a handoff that fails validation."""


def _is_non_empty_str(value: object) -> bool:
    return isinstance(value, str) and value.strip() != ""


def _is_string_list(value: object) -> bool:
    return isinstance(value, list) and all(isinstance(item, str) for item in value)


def validate_handoff_data(data: object) -> list[str]:
    """Validate an already-parsed handoff payload.

    Returns a list of blocking issues; an empty list means the payload is a
    schema-valid Track Handoff.  Never raises for invalid payloads — callers
    decide how to fail closed (see :func:`load_handoff_for_merge`).
    """
    errors: list[str] = []
    if not isinstance(data, dict):
        return [f"{HANDOFF_INCOMPLETE}: handoff must be a JSON object"]

    # ── Unknown / additional fields ──────────────────────────────────────
    unknown_keys = sorted(set(data) - KNOWN_TOP_LEVEL)
    if unknown_keys:
        errors.append(
            f"unknown additional top-level field(s): {unknown_keys}; "
            "handoffs must not smuggle free-form report content"
        )

    # ── Required fields ──────────────────────────────────────────────────
    missing = sorted(REQUIRED_TOP_LEVEL - set(data))
    for field in missing:
        errors.append(f"missing required field '{field}'")

    # ── Identity and version ─────────────────────────────────────────────
    if data.get("schema_version") != SCHEMA_VERSION:
        errors.append(
            f"schema_version must be {SCHEMA_VERSION!r}, got {data.get('schema_version')!r}"
        )
    for field in ("handoff_id", "track_id", "question"):
        if field in data and not _is_non_empty_str(data[field]):
            errors.append(f"'{field}' must be a non-empty string")

    # ── Status semantics ─────────────────────────────────────────────────
    status = data.get("status")
    # isinstance gate first: `in` on a set raises TypeError for unhashable
    # values such as dicts/lists.
    if not isinstance(status, str) or status not in ALLOWED_STATUS:
        errors.append(
            f"'status' must be one of {list(ALLOWED_STATUS)}, got {status!r}"
        )
    if (
        isinstance(status, str)
        and status in {"partial", "blocked"}
        and not _is_non_empty_str(data.get("status_reason"))
    ):
        errors.append(f"'{status}' status requires a non-empty 'status_reason'")
    if status == "blocked" and not _is_non_empty_str(data.get("recovery_action")):
        errors.append("'blocked' status requires a non-empty 'recovery_action'")

    # ── Timestamp ────────────────────────────────────────────────────────
    if "generated_at" in data and not _is_valid_timestamp(data["generated_at"]):
        errors.append(
            "'generated_at' must be an ISO-8601 date or a timezone-aware "
            "RFC 3339 timestamp (naive datetimes and impossible calendar "
            f"values are rejected), got {data['generated_at']!r}"
        )

    # ── Scope ────────────────────────────────────────────────────────────
    scope = data.get("scope")
    if "scope" in data:
        if not isinstance(scope, dict):
            errors.append("'scope' must be an object")
        else:
            extra_scope = sorted(set(scope) - SCOPE_REQUIRED)
            if extra_scope:
                errors.append(f"unknown additional 'scope' field(s): {extra_scope}")
            for field in sorted(SCOPE_REQUIRED - set(scope)):
                errors.append(f"'scope' is missing required field '{field}'")
            in_scope = scope.get("in_scope")
            if "in_scope" in scope:
                if not _is_string_list(in_scope) or not in_scope:
                    errors.append(
                        "'scope.in_scope' must be a non-empty list of strings"
                    )
                elif any(not item.strip() for item in in_scope):
                    errors.append("'scope.in_scope' items must be non-empty strings")
            out_of_scope = scope.get("out_of_scope")
            if "out_of_scope" in scope:
                if not _is_string_list(out_of_scope):
                    errors.append("'scope.out_of_scope' must be a list of strings")
                elif any(not item.strip() for item in out_of_scope):
                    errors.append(
                        "'scope.out_of_scope' items must be non-empty strings"
                    )
            for field in ("timeframe", "geography"):
                if field in scope and not _is_non_empty_str(scope[field]):
                    errors.append(f"'scope.{field}' must be a non-empty string")

    # ── Source register ──────────────────────────────────────────────────
    register = data.get("source_register")
    source_ids: set[str] = set()
    duplicate_source_ids: set[str] = set()
    if "source_register" in data:
        if not isinstance(register, list):
            errors.append("'source_register' must be a list")
        else:
            for entry in register:
                if not isinstance(entry, dict):
                    errors.append(
                        "each source_register entry must be an object; got "
                        f"{type(entry).__name__} ({str(entry)[:60]!r})"
                    )
                    continue
                extra = sorted(set(entry) - SOURCE_REQUIRED - SOURCE_OPTIONAL)
                if extra:
                    errors.append(
                        f"unknown additional 'source_register' field(s): {extra}"
                    )
                for field in sorted(SOURCE_REQUIRED - set(entry)):
                    errors.append(
                        f"source_register entry is missing required field '{field}'"
                    )
                sid = entry.get("source_id")
                if not _is_non_empty_str(sid):
                    errors.append("source_register 'source_id' must be a non-empty string")
                    continue
                if sid in source_ids:
                    duplicate_source_ids.add(sid)
                source_ids.add(sid)
                if "title" in entry and not _is_non_empty_str(entry.get("title")):
                    errors.append(
                        f"source_register '{sid}' title must be a non-empty string"
                    )
                if "url" in entry and not _is_non_empty_str(entry.get("url")):
                    errors.append(f"source_register '{sid}' url must be a non-empty string")
            for sid in sorted(duplicate_source_ids):
                errors.append(f"duplicate source_id '{sid}' in source_register")

    # ── Findings ─────────────────────────────────────────────────────────
    findings = data.get("findings")
    finding_ids: set[str] = set()
    duplicate_finding_ids: set[str] = set()
    if "findings" in data:
        if not isinstance(findings, list):
            errors.append("'findings' must be a list")
        else:
            if status == "complete" and not findings:
                errors.append(
                    "'complete' status requires at least one finding; use "
                    "'partial'/'blocked' with reasons instead of an empty array"
                )
            for finding in findings:
                if not isinstance(finding, dict):
                    errors.append("each finding must be an object")
                    continue
                extra = sorted(set(finding) - FINDING_REQUIRED - FINDING_OPTIONAL)
                if extra:
                    errors.append(f"unknown additional 'findings' field(s): {extra}")
                for field in sorted(FINDING_REQUIRED - set(finding)):
                    errors.append(f"finding is missing required field '{field}'")
                fid = finding.get("finding_id")
                if not _is_non_empty_str(fid):
                    errors.append("finding 'finding_id' must be a non-empty string")
                    fid = None
                elif fid in finding_ids:
                    duplicate_finding_ids.add(fid)
                else:
                    finding_ids.add(fid)
                if "claim" in finding and not _is_non_empty_str(finding.get("claim")):
                    errors.append(
                        f"finding {fid or '?'} 'claim' must be a non-empty string"
                    )
                refs = finding.get("evidence_refs")
                if "evidence_refs" in finding:
                    if not _is_string_list(refs) or not refs:
                        errors.append(
                            f"finding {fid or '?'} 'evidence_refs' must be a "
                            "non-empty list of source_ids"
                        )
                    else:
                        unresolved = [ref for ref in refs if ref not in source_ids]
                        for ref in unresolved:
                            errors.append(
                                f"finding {fid or '?'} 'evidence_refs' points to "
                                f"source id '{ref}' which is not in this "
                                "handoff's source_register"
                            )
                role = finding.get("evidence_role")
                if "evidence_role" in finding and (
                    not isinstance(role, str) or role not in ALLOWED_EVIDENCE_ROLES
                ):
                    errors.append(
                        f"finding {fid or '?'} 'evidence_role' must be one of "
                        f"{list(ALLOWED_EVIDENCE_ROLES)}, got {role!r}"
                    )
                confidence = finding.get("confidence")
                if "confidence" in finding and (
                    not isinstance(confidence, (int, float))
                    or isinstance(confidence, bool)
                    or not 0 <= confidence <= 1
                ):
                    errors.append(
                        f"finding {fid or '?'} 'confidence' must be a number "
                        f"between 0 and 1, got {confidence!r}"
                    )
                if "limitations" in finding and not _is_non_empty_str(
                    finding.get("limitations")
                ):
                    errors.append(
                        f"finding {fid or '?'} 'limitations' must be a "
                        "non-empty string when present"
                    )
            for fid in sorted(duplicate_finding_ids):
                errors.append(f"duplicate finding_id '{fid}' in findings")

    # ── Conflicts ────────────────────────────────────────────────────────
    conflicts = data.get("conflicts")
    if "conflicts" in data:
        if not isinstance(conflicts, list):
            errors.append("'conflicts' must be a list")
        else:
            for conflict in conflicts:
                if not isinstance(conflict, dict):
                    errors.append("each conflict must be an object")
                    continue
                extra = sorted(set(conflict) - CONFLICT_REQUIRED - CONFLICT_OPTIONAL)
                if extra:
                    errors.append(f"unknown additional 'conflicts' field(s): {extra}")
                for field in sorted(CONFLICT_REQUIRED - set(conflict)):
                    errors.append(f"conflict is missing required field '{field}'")
                topic = conflict.get("topic")
                if "topic" in conflict and not _is_non_empty_str(topic):
                    errors.append("conflict 'topic' must be a non-empty string")
                refs = conflict.get("finding_refs")
                if "finding_refs" in conflict:
                    if not _is_string_list(refs) or not refs:
                        errors.append(
                            "conflict 'finding_refs' must be a non-empty list "
                            "of finding_ids"
                        )
                    else:
                        unbound = [ref for ref in refs if ref not in finding_ids]
                        for ref in unbound:
                            errors.append(
                                f"conflict {topic or ''!r} 'finding_refs' points to "
                                f"finding id '{ref}' which does not exist in this "
                                "handoff's findings"
                            )
                resolution_status = conflict.get("resolution_status")
                if "resolution_status" in conflict and (
                    not isinstance(resolution_status, str)
                    or resolution_status not in ALLOWED_RESOLUTION_STATUS
                ):
                    errors.append(
                        "conflict 'resolution_status' must be one of "
                        f"{list(ALLOWED_RESOLUTION_STATUS)}, got {resolution_status!r}"
                    )
                # Type check applies whenever the field is present, regardless
                # of resolution status; the requirement below is status-bound.
                if "resolution_note" in conflict and not _is_non_empty_str(
                    conflict.get("resolution_note")
                ):
                    errors.append(
                        "conflict 'resolution_note' must be a non-empty string "
                        "when present"
                    )
                if resolution_status == "resolved" and not _is_non_empty_str(
                    conflict.get("resolution_note")
                ):
                    errors.append(
                        "resolved conflict requires a non-empty 'resolution_note'"
                    )
                affects = conflict.get("affects_overall_question")
                if (
                    "affects_overall_question" in conflict
                    and not isinstance(affects, bool)
                ):
                    errors.append(
                        "conflict 'affects_overall_question' must be a boolean"
                    )

    # ── Unknowns ─────────────────────────────────────────────────────────
    unknowns = data.get("unknowns")
    if "unknowns" in data:
        if not isinstance(unknowns, list):
            errors.append("'unknowns' must be a list")
        else:
            for unknown in unknowns:
                if not isinstance(unknown, dict):
                    errors.append("each unknown must be an object")
                    continue
                extra = sorted(set(unknown) - UNKNOWN_REQUIRED)
                if extra:
                    errors.append(f"unknown additional 'unknowns' field(s): {extra}")
                for field in sorted(UNKNOWN_REQUIRED):
                    if field not in unknown or not _is_non_empty_str(unknown[field]):
                        errors.append(
                            f"unknowns entry is missing required non-empty "
                            f"string field '{field}'"
                        )

    # ── Implications ─────────────────────────────────────────────────────
    implications = data.get("implications")
    if "implications" in data:
        if not _is_string_list(implications):
            errors.append("'implications' must be a list of strings")
        elif any(not item.strip() for item in implications):
            errors.append("'implications' items must be non-empty strings")

    # ── Optional string fields: null is never a lawful value ─────────────
    for field in ("status_reason", "recovery_action"):
        if field in data and not _is_non_empty_str(data[field]):
            errors.append(f"'{field}' must be a non-empty string when present")

    # ── Reserved artifact_ref shape (Run State, issue #417) ──────────────
    artifact_ref = data.get("artifact_ref")
    if "artifact_ref" in data:
        if not isinstance(artifact_ref, dict):
            errors.append("'artifact_ref' must be an object")
        else:
            extra = sorted(set(artifact_ref) - ARTIFACT_REF_REQUIRED)
            if extra:
                errors.append(f"unknown additional 'artifact_ref' field(s): {extra}")
            if not _is_non_empty_str(artifact_ref.get("artifact_id")):
                errors.append(
                    "'artifact_ref.artifact_id' must be a non-empty string"
                )

    return errors


def _normalized_scope_value(value: object) -> object:
    """Order-insensitive comparison key for string-list scope fields."""
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return sorted(value)
    return value


def _scope_binding_problems(
    actual_scope: object, expected_scope: object
) -> list[str]:
    """Compare a handoff's scope against the dispatched scope assignment.

    The dispatch identity (handoff_id/track_id/question) proves *which run*
    produced a handoff; only the scope binding proves the track executed
    within the assigned boundary (issue #416: machine-checkable scope /
    timeframe drift between tracks).
    """
    if not isinstance(expected_scope, dict) or set(expected_scope) != SCOPE_REQUIRED:
        got = (
            sorted(expected_scope)
            if isinstance(expected_scope, dict)
            else type(expected_scope).__name__
        )
        return [
            "invalid expected_scope binding: must contain exactly "
            f"{sorted(SCOPE_REQUIRED)}, got {got}"
        ]
    if not isinstance(actual_scope, dict):
        return ["scope binding failed: handoff has no valid scope object"]
    problems: list[str] = []
    for field in ("timeframe", "geography"):
        expected = expected_scope[field]
        actual = actual_scope.get(field)
        if actual != expected:
            problems.append(
                f"scope drift on '{field}': dispatch assigned {expected!r}, "
                f"handoff reports {actual!r}"
            )
    for field in ("in_scope", "out_of_scope"):
        expected = expected_scope[field]
        actual = actual_scope.get(field)
        if _normalized_scope_value(actual) != _normalized_scope_value(expected):
            problems.append(
                f"scope drift on '{field}': dispatch assigned {expected!r}, "
                f"handoff reports {actual!r}"
            )
    return problems


def load_handoff_for_merge(
    path: Path | str,
    *,
    expected_track_id: str | None = None,
    expected_handoff_id: str | None = None,
    expected_question: str | None = None,
    expected_artifact_id: str | None = None,
    expected_scope: dict | None = None,
) -> dict:
    """Consumer-side loader: parse + validate, raising instead of guessing.

    The parent synthesizer must call this before merging so that a missing,
    malformed, or incomplete handoff surfaces as :class:`HandoffIncomplete`
    rather than as an empty-but-plausible merge result.

    Identity bindings (all optional, each fails closed on mismatch):

    - ``expected_track_id`` proves which track produced the handoff — but a
      track id alone does NOT prove freshness: yesterday's handoff for the
      same track passes this check.
    - ``expected_handoff_id`` binds to one specific dispatch/run when the
      parent pre-assigns handoff ids; this is the strongest stale guard.
    - ``expected_question`` catches cross-task reuse when ids are not
      pre-assigned.
    - ``expected_artifact_id`` binds the handoff to the downstream artifact
      via its optional ``artifact_ref``; an absent artifact_ref fails.
    - ``expected_scope`` verifies the track executed within its assigned
      boundary (exact match on ``timeframe``/``geography``, order-insensitive
      match on ``in_scope``/``out_of_scope``).  This is a different axis from
      dispatch identity: a fresh handoff from the right run can still have
      drifted outside its assigned scope.
    """
    path = Path(path)
    problems: list[str] = []
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise HandoffIncomplete(
            f"{HANDOFF_INCOMPLETE}: cannot read handoff file {path}: {exc}"
        ) from exc
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise HandoffIncomplete(
            f"{HANDOFF_INCOMPLETE}: handoff file {path} is not valid JSON: {exc}"
        ) from exc
    if not isinstance(data, dict):
        # Identity bindings below use dict access; a non-object root (list,
        # string, number, null) must fail closed here instead of crashing.
        raise HandoffIncomplete(
            f"{HANDOFF_INCOMPLETE}: handoff file {path} must contain a single "
            f"JSON object, got {type(data).__name__}"
        )

    problems.extend(validate_handoff_data(data))
    if expected_track_id is not None and data.get("track_id") != expected_track_id:
        problems.append(
            f"track_id mismatch: expected {expected_track_id!r}, "
            f"got {data.get('track_id')!r}"
        )
    if (
        expected_handoff_id is not None
        and data.get("handoff_id") != expected_handoff_id
    ):
        problems.append(
            "handoff_id mismatch (stale or misrouted handoff?): expected "
            f"{expected_handoff_id!r}, got {data.get('handoff_id')!r}"
        )
    if expected_question is not None and data.get("question") != expected_question:
        problems.append(
            "question mismatch (handoff was not produced for this dispatch): "
            f"expected {expected_question!r}, got {data.get('question')!r}"
        )
    if expected_artifact_id is not None:
        artifact_ref = data.get("artifact_ref")
        actual = artifact_ref.get("artifact_id") if isinstance(artifact_ref, dict) else None
        if actual != expected_artifact_id:
            problems.append(
                "artifact binding mismatch: expected artifact_id "
                f"{expected_artifact_id!r}, got {actual!r} (a handoff without "
                "artifact_ref cannot satisfy an artifact-bound merge)"
            )
    if expected_scope is not None:
        problems.extend(_scope_binding_problems(data.get("scope"), expected_scope))
    if problems:
        detail = "\n".join(f"  - {problem}" for problem in problems)
        raise HandoffIncomplete(
            f"{HANDOFF_INCOMPLETE}: {path} failed Track Handoff validation:\n{detail}"
        )
    return data


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Fail-closed validator for parallel-research Track Handoffs",
    )
    parser.add_argument("handoff_file", type=str, help="Path to the handoff JSON file")
    parser.add_argument(
        "--expected-track-id",
        type=str,
        default=None,
        help="Consumer guard: reject unless track_id matches (proves track name only)",
    )
    parser.add_argument(
        "--expected-handoff-id",
        type=str,
        default=None,
        help="Consumer guard: reject unless handoff_id matches the dispatched run id "
        "(strongest guard against reusing a stale handoff from a previous run)",
    )
    parser.add_argument(
        "--expected-question",
        type=str,
        default=None,
        help="Consumer guard: reject unless question matches this dispatch's track question",
    )
    parser.add_argument(
        "--expected-artifact-id",
        type=str,
        default=None,
        help="Consumer guard: reject unless artifact_ref.artifact_id matches; a handoff "
        "without artifact_ref cannot pass an artifact-bound merge",
    )
    parser.add_argument(
        "--expected-scope-file",
        type=str,
        default=None,
        help="Consumer guard: path to a JSON file holding the dispatched scope object; "
        "reject unless the handoff scope matches (timeframe/geography exact, "
        "in_scope/out_of_scope order-insensitive)",
    )
    parser.add_argument(
        "--run-state",
        type=str,
        default=None,
        help="Optional issue #417 binding: reject unless this handoff matches the "
        "Run State's artifact_id and listed handoff_id. Omitting this "
        "flag leaves the #416 path unchanged.",
    )
    args = parser.parse_args(argv)

    expected_scope: dict | None = None
    if args.expected_scope_file is not None:
        try:
            expected_scope = json.loads(
                Path(args.expected_scope_file).read_text(encoding="utf-8")
            )
        except (OSError, json.JSONDecodeError) as exc:
            print(
                f"{HANDOFF_INCOMPLETE}: cannot read expected-scope file "
                f"{args.expected_scope_file}: {exc}"
            )
            print(
                "\nThis refusal is terminal: do not merge this handoff and do "
                "not interpret it as empty findings."
            )
            return EXIT_FAIL_CLOSED

    try:
        data = load_handoff_for_merge(
            args.handoff_file,
            expected_track_id=args.expected_track_id,
            expected_handoff_id=args.expected_handoff_id,
            expected_question=args.expected_question,
            expected_artifact_id=args.expected_artifact_id,
            expected_scope=expected_scope,
        )
    except HandoffIncomplete as exc:
        print(exc)
        print(
            "\nThis refusal is terminal: do not merge this handoff and do not "
            "interpret it as empty findings."
        )
        return EXIT_FAIL_CLOSED

    if args.run_state:
        from validate_research_run_state import (
            bind_handoff_to_run_state,
            load_run_state_file,
        )

        state, run_errors = load_run_state_file(args.run_state)
        bind_errors = list(run_errors)
        if state is not None:
            bind_errors.extend(
                bind_handoff_to_run_state(
                    data, state, handoff_path=args.handoff_file
                )
            )
        if bind_errors:
            detail = "\n".join(f"  - {item}" for item in bind_errors)
            print(
                f"{HANDOFF_INCOMPLETE}: {args.handoff_file} failed Run State "
                f"binding:\n{detail}"
            )
            print(
                "\nThis refusal is terminal: do not merge this handoff and do "
                "not interpret it as empty findings."
            )
            return EXIT_FAIL_CLOSED

    print("OK — Track Handoff is schema-valid")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
