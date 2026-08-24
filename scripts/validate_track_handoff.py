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
    python3 scripts/validate_track_handoff.py <handoff.json> \
        [--expected-track-id <track-id>]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
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
# Optional top-level fields: conditional status explanations plus the Run
# State forward-reference reserved by issue #417.
OPTIONAL_TOP_LEVEL = frozenset({"status_reason", "recovery_action", "artifact_ref"})
KNOWN_TOP_LEVEL = REQUIRED_TOP_LEVEL | OPTIONAL_TOP_LEVEL

SCOPE_REQUIRED = frozenset({"in_scope", "out_of_scope", "timeframe", "geography"})
SOURCE_REQUIRED = frozenset({"source_id", "title"})
SOURCE_OPTIONAL = frozenset({"url"})
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

# ISO-8601 date (2026-08-24) or RFC 3339 timestamp with zone offset.
_TIMESTAMP_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}"
    r"(?:[Tt]\d{2}:\d{2}(?::\d{2}(?:\.\d+)?)?(?:[Zz]|[+-]\d{2}:\d{2})?)?$"
)

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
    if status not in ALLOWED_STATUS:
        errors.append(
            f"'status' must be one of {list(ALLOWED_STATUS)}, got {status!r}"
        )
    if status in {"partial", "blocked"} and not _is_non_empty_str(
        data.get("status_reason")
    ):
        errors.append(f"'{status}' status requires a non-empty 'status_reason'")
    if status == "blocked" and not _is_non_empty_str(data.get("recovery_action")):
        errors.append("'blocked' status requires a non-empty 'recovery_action'")

    # ── Timestamp ────────────────────────────────────────────────────────
    if "generated_at" in data and not (
        isinstance(data["generated_at"], str)
        and _TIMESTAMP_RE.match(data["generated_at"])
    ):
        errors.append(
            "'generated_at' must be an ISO-8601 date or RFC 3339 timestamp, "
            f"got {data['generated_at']!r}"
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
            if in_scope is not None:
                if not _is_string_list(in_scope) or not in_scope:
                    errors.append(
                        "'scope.in_scope' must be a non-empty list of strings"
                    )
                elif any(not item.strip() for item in in_scope):
                    errors.append("'scope.in_scope' items must be non-empty strings")
            out_of_scope = scope.get("out_of_scope")
            if out_of_scope is not None and not _is_string_list(out_of_scope):
                errors.append("'scope.out_of_scope' must be a list of strings")
            for field in ("timeframe", "geography"):
                if field in scope and not _is_non_empty_str(scope[field]):
                    errors.append(f"'scope.{field}' must be a non-empty string")

    # ── Source register ──────────────────────────────────────────────────
    register = data.get("source_register")
    source_ids: set[str] = set()
    duplicate_source_ids: set[str] = set()
    malformed_source_ids: list[str] = []
    if "source_register" in data:
        if not isinstance(register, list):
            errors.append("'source_register' must be a list")
        else:
            for entry in register:
                if not isinstance(entry, dict):
                    malformed_source_ids.append(str(entry))
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
                if refs is not None:
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
                if role is not None and role not in ALLOWED_EVIDENCE_ROLES:
                    errors.append(
                        f"finding {fid or '?'} 'evidence_role' must be one of "
                        f"{list(ALLOWED_EVIDENCE_ROLES)}, got {role!r}"
                    )
                confidence = finding.get("confidence")
                if confidence is not None and (
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
                if refs is not None:
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
                if resolution_status is not None and resolution_status not in (
                    ALLOWED_RESOLUTION_STATUS
                ):
                    errors.append(
                        "conflict 'resolution_status' must be one of "
                        f"{list(ALLOWED_RESOLUTION_STATUS)}, got {resolution_status!r}"
                    )
                if resolution_status == "resolved" and not _is_non_empty_str(
                    conflict.get("resolution_note")
                ):
                    errors.append(
                        "resolved conflict requires a non-empty 'resolution_note'"
                    )
                affects = conflict.get("affects_overall_question")
                if affects is not None and not isinstance(affects, bool):
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
    if implications is not None:
        if not _is_string_list(implications):
            errors.append("'implications' must be a list of strings")
        elif any(not item.strip() for item in implications):
            errors.append("'implications' items must be non-empty strings")

    # ── Reserved artifact_ref shape (Run State, issue #417) ──────────────
    artifact_ref = data.get("artifact_ref")
    if artifact_ref is not None:
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


def load_handoff_for_merge(path: Path | str, *, expected_track_id: str | None = None) -> dict:
    """Consumer-side loader: parse + validate, raising instead of guessing.

    The parent synthesizer must call this before merging so that a missing,
    malformed, or incomplete handoff surfaces as :class:`HandoffIncomplete`
    rather than as an empty-but-plausible merge result.
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

    problems.extend(validate_handoff_data(data))
    if expected_track_id is not None and data.get("track_id") != expected_track_id:
        problems.append(
            f"track_id mismatch: expected {expected_track_id!r}, "
            f"got {data.get('track_id')!r}"
        )
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
        help="Consumer guard: reject the handoff unless track_id matches",
    )
    args = parser.parse_args(argv)

    try:
        load_handoff_for_merge(args.handoff_file, expected_track_id=args.expected_track_id)
    except HandoffIncomplete as exc:
        print(exc)
        print(
            "\nThis refusal is terminal: do not merge this handoff and do not "
            "interpret it as empty findings."
        )
        return EXIT_FAIL_CLOSED

    print("OK — Track Handoff is schema-valid")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
