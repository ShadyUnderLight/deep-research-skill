#!/usr/bin/env python3
"""Shared, fail-closed validation for audit evidence references.

Audit status is not execution evidence by itself.  This module defines the
small wire format shared by report status blocks, Research Packs, contracts,
and the JSON verdict emitted by ``audit_report.py``.

Typed references use one of these prefixes::

    report-section:<exact visible heading>
    report-table:<exact visible heading>
    pack-section:<exact visible heading>
    pack-table:<exact visible heading>
    checklist-item:<relative checklist path>#<item id>
    audit-record:<relative record path>#<record id>@<ISO-8601 timestamp>
    validator:<validator binding id>

Legacy free-form strings are accepted only outside strict mode and are
explicitly labelled ``legacy_self_attested`` by callers.
"""

from __future__ import annotations

import json
from collections.abc import Collection
from dataclasses import dataclass
from datetime import datetime, timezone
import re
from pathlib import Path


EXECUTION_SOURCES = frozenset(
    {
        "automated_validator",
        "manual_checklist_attestation",
        "process_node_evidence",
        "legacy_self_attested",
    }
)

_PREFIX_TO_KIND = {
    "report-section": "report_section",
    "report-table": "report_table",
    "pack-section": "pack_section",
    "pack-table": "pack_table",
    "checklist-item": "checklist_item",
    "audit-record": "audit_record",
    "validator": "automated_validator",
}
_KIND_TO_PREFIX = {value: key for key, value in _PREFIX_TO_KIND.items()}
_REFERENCE_RE = re.compile(r"^([a-z][a-z-]*):(.*)$", re.IGNORECASE)
_ITEM_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
_RECORD_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/-]*$")
_HEADING_RE = re.compile(r"^(#{1,6})[ \t]+(.+?)[ \t]*$")

# Removed audit-record byte-identity fields. New audit records bind through
# artifact_id, route, audit identity, execution state, and visible evidence;
# an old record carrying one of these fields must not be silently consumed.
REMOVED_AUDIT_RECORD_HASH_FIELDS = frozenset(
    {
        "input_sha256",
        "artifact_sha256",
        "artifact_hash",
        "sha256",
        "record_artifact_sha256",
        "claim_alignment_bundle_sha256",
    }
)


@dataclass(frozen=True)
class EvidenceValidation:
    """Result of validating one evidence reference."""

    provenance: dict[str, object] | None = None
    errors: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()
    legacy: bool = False

    @property
    def is_valid(self) -> bool:
        return not self.errors


def _normalise_heading(value: str) -> str:
    return " ".join(value.strip().split()).casefold()


def _normalise_kind(value: object) -> str | None:
    """Normalise a *dict-form* evidence kind (issue #402).

    The JSON Schema (schemas/route-activation-contract.json) declares an
    exact enum for a nested evidence object's ``kind``:
    report_section / report_table / pack_section / pack_table /
    checklist_item / audit_record / automated_validator.  Prefix vocabulary
    (``validator``, ``report-section``) and case/whitespace variants are
    string-reference forms and must NOT be accepted for objects — otherwise
    schema-rejected objects pass runtime validation.
    """
    if not isinstance(value, str):
        return None
    if value in _KIND_TO_PREFIX:
        return value
    return None


def is_typed_reference(value: object) -> bool:
    """Return whether *value* uses a recognised typed-reference prefix."""
    if isinstance(value, dict):
        return _normalise_kind(value.get("kind")) is not None
    if not isinstance(value, str):
        return False
    match = _REFERENCE_RE.match(value.strip())
    return bool(match and match.group(1).lower() in _PREFIX_TO_KIND)


def _safe_path(path_value: str, base_dir: Path) -> tuple[Path | None, str | None]:
    """Resolve a relative evidence path without allowing path traversal."""
    candidate = Path(path_value)
    if candidate.is_absolute():
        return None, "evidence path must be relative"
    root = base_dir.resolve()
    resolved = (root / candidate).resolve()
    try:
        resolved.relative_to(root)
    except ValueError:
        return None, "evidence path escapes the artifact directory"
    return resolved, None


def _headings(text: str) -> list[tuple[int, str, int]]:
    result: list[tuple[int, str, int]] = []
    for line_number, line in enumerate(text.splitlines(), 1):
        match = _HEADING_RE.match(line)
        if match:
            result.append((len(match.group(1)), match.group(2), line_number))
    return result


def _section_lines(text: str, heading_line: int) -> list[str]:
    lines = text.splitlines()
    start = heading_line
    for index in range(start, len(lines)):
        if index > start and _HEADING_RE.match(lines[index]):
            return lines[start:index]
    return lines[start:]


def _validate_artifact_heading(
    kind: str,
    locator: str,
    artifact_text: str | None,
    artifact_label: str,
) -> EvidenceValidation:
    if not locator.strip():
        return EvidenceValidation(errors=(f"{kind} evidence locator is empty",))

    if artifact_text is None:
        return EvidenceValidation(
            provenance={
                "kind": kind,
                "locator": locator,
                "verified": False,
            }
        )

    matches = [
        (level, title, line)
        for level, title, line in _headings(artifact_text)
        if _normalise_heading(title) == _normalise_heading(locator)
    ]
    if not matches:
        return EvidenceValidation(
            errors=(
                f"{kind} evidence locator {locator!r} was not found in "
                f"the visible {artifact_label}",
            )
        )
    if len(matches) > 1:
        return EvidenceValidation(
            errors=(
                f"{kind} evidence locator {locator!r} is ambiguous in "
                f"the visible {artifact_label} ({len(matches)} matches)",
            )
        )

    _, _, line = matches[0]
    return EvidenceValidation(
        provenance={
            "kind": kind,
            "locator": locator,
            "verified": True,
            "line": line,
        }
    )


def _validate_artifact_table(
    kind: str,
    locator: str,
    artifact_text: str | None,
    artifact_label: str,
) -> EvidenceValidation:
    heading_result = _validate_artifact_heading(
        kind,
        locator,
        artifact_text,
        artifact_label,
    )
    if heading_result.errors or artifact_text is None:
        if artifact_text is None and heading_result.provenance:
            heading_result = EvidenceValidation(
                provenance={
                    **heading_result.provenance,
                    "kind": kind,
                },
                errors=heading_result.errors,
                warnings=heading_result.warnings,
                legacy=heading_result.legacy,
            )
        return heading_result

    line = int(heading_result.provenance["line"])
    section = _section_lines(artifact_text, line)
    has_row = any("|" in current for current in section)
    has_separator = any(
        "|" in current and re.search(r"-{3,}", current)
        for current in section
    )
    if not has_row or not has_separator:
        return EvidenceValidation(
            errors=(
                f"{kind} evidence locator {locator!r} does not point "
                "to a visible Markdown table",
            )
        )
    return EvidenceValidation(
        provenance={
            **heading_result.provenance,
            "kind": kind,
        }
    )


def _validate_checklist_item(
    locator: str,
    base_dir: Path | None,
    *,
    strict: bool = False,
) -> EvidenceValidation:
    if "#" not in locator:
        return EvidenceValidation(
            errors=(
                "checklist-item evidence must use "
                "<relative checklist path>#<item id>",
            )
        )
    path_value, item_id = locator.rsplit("#", 1)
    if not path_value or not _ITEM_ID_RE.fullmatch(item_id):
        return EvidenceValidation(
            errors=(
                "checklist-item evidence has an invalid path or item id",
            )
        )

    provenance: dict[str, object] = {
        "kind": "checklist_item",
        "locator": locator,
        "checklist": path_value,
        "item_id": item_id,
        "verified": False,
    }
    if base_dir is None:
        return EvidenceValidation(provenance=provenance)

    path, path_error = _safe_path(path_value, base_dir)
    if path_error:
        return EvidenceValidation(errors=(path_error,))
    assert path is not None
    if not path.is_file():
        return EvidenceValidation(
            errors=(f"checklist file does not exist: {path_value}",)
        )
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return EvidenceValidation(
            errors=(f"cannot read checklist file {path_value}: {exc}",)
        )

    # Checklist markers are legitimate top-level HTML comments, but markers
    # inside fenced code or raw HTML containers are not visible evidence.
    # Use the checklist-specific sanitizer that shares the canonical
    # CommonMark state machine (issue #409).  Lazy import avoids a circular
    # import with validate_contract → audit_evidence.  On import failure fail
    # closed (do not fall back to raw text).
    try:
        from validate_contract import sanitize_checklist_visible_markdown

        visible_text = sanitize_checklist_visible_markdown(text)
    except Exception as exc:  # ImportError or any load failure → fail closed
        return EvidenceValidation(
            errors=(f"cannot load canonical fence sanitizer: {exc}",)
        )

    marker_patterns = (
        rf"^[ ]{{0,3}}<!--[ \t]*audit-item[ \t]*:[ \t]*{re.escape(item_id)}[ \t]*-->[ \t]*$",
        rf"^[ ]{{0,3}}\{{#{re.escape(item_id)}\}}[ \t]*$",
        rf"^[ ]{{0,3}}-[ \t]+\[[ xX]\][ \t]+\*\*{re.escape(item_id)}\*\*[ \t]*$",
    )
    if not any(re.search(pattern, visible_text, re.MULTILINE) for pattern in marker_patterns):
        return EvidenceValidation(
            errors=(
                f"checklist item {item_id!r} was not found in {path_value}",
            )
        )
    # In strict mode a checklist definition is not execution evidence (issue #401).
    # It must not be used alone to obtain a trusted Pass; callers must supply
    # an audit-record bound to the current artifact.
    if strict:
        provenance["definition_only"] = True
        provenance["verified"] = False
        return EvidenceValidation(
            provenance=provenance,
            errors=(
                "checklist-item is definition-only; strict requires "
                "audit-record with artifact binding (see issue #401)",
            ),
        )
    provenance["verified"] = True
    return EvidenceValidation(provenance=provenance)


def _validate_audit_record(
    locator: str,
    base_dir: Path | None,
    *,
    strict: bool = False,
    expected_audit_id: str | None = None,
    expected_artifact_id: str | None = None,
    expected_route: str | None = None,
    expected_validator_binding: str | None = None,
    execution_type: str | None = None,
    artifact_text: str | None = None,
    artifact_label: str = "report",
    report_text: str | None = None,
    pack_text: str | None = None,
) -> EvidenceValidation:
    match = re.fullmatch(r"([^#]+)#([^@]+)@(.+)", locator)
    if not match:
        return EvidenceValidation(
            errors=(
                "audit-record evidence must use "
                "<relative path>#<record id>@<ISO-8601 timestamp>",
            )
        )
    path_value, record_id, timestamp = match.groups()
    if not _RECORD_ID_RE.fullmatch(record_id):
        return EvidenceValidation(errors=("audit-record has an invalid record id",))
    try:
        datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError:
        return EvidenceValidation(
            errors=(f"audit-record timestamp is not ISO-8601: {timestamp!r}",)
        )

    provenance: dict[str, object] = {
        "kind": "audit_record",
        "locator": locator,
        "record_path": path_value,
        "record_id": record_id,
        "recorded_at": timestamp,
        "verified": False,
    }
    if base_dir is None:
        return EvidenceValidation(provenance=provenance)
    path, path_error = _safe_path(path_value, base_dir)
    if path_error:
        return EvidenceValidation(errors=(path_error,))
    assert path is not None
    if not path.is_file():
        return EvidenceValidation(
            errors=(f"audit record file does not exist: {path_value}",)
        )

    try:
        payload = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return EvidenceValidation(
            errors=(
                f"audit record file must contain JSON records: {path_value} "
                f"({exc})",
            )
        )

    if isinstance(payload, list):
        records = payload
    elif isinstance(payload, dict) and isinstance(payload.get("records"), list):
        records = payload["records"]
    elif isinstance(payload, dict):
        records = [payload]
    else:
        return EvidenceValidation(
            errors=(
                f"audit record file must contain a JSON object, array, or "
                f"records array: {path_value}",
            )
        )

    removed_hash_locations: list[str] = []
    if isinstance(payload, dict):
        envelope_hash_fields = sorted(
            REMOVED_AUDIT_RECORD_HASH_FIELDS & set(payload)
        )
        if envelope_hash_fields:
            removed_hash_locations.append(
                "envelope: " + ", ".join(envelope_hash_fields)
            )
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            continue
        record_hash_fields = sorted(
            REMOVED_AUDIT_RECORD_HASH_FIELDS & set(record)
        )
        if record_hash_fields:
            removed_hash_locations.append(
                f"records[{index}]: " + ", ".join(record_hash_fields)
            )
    if removed_hash_locations:
        return EvidenceValidation(
            provenance={**provenance, "verified": False},
            errors=(
                "audit record payload carries removed hash field(s): "
                + "; ".join(removed_hash_locations),
            ),
        )

    def _parse_timestamp(value: object) -> datetime | None:
        if not isinstance(value, str):
            return None
        try:
            parsed = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
        except ValueError:
            return None
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc)

    expected_time = _parse_timestamp(timestamp)
    # Collect all matching records to detect duplicates (P3: first-match-wins is fail-open)
    matching_records: list[dict] = []
    for record in records:
        if not isinstance(record, dict):
            continue
        candidate_id = record.get("record_id", record.get("id"))
        candidate_time = record.get(
            "recorded_at",
            record.get("timestamp", record.get("executed_at")),
        )
        if candidate_id != record_id or _parse_timestamp(candidate_time) != expected_time:
            continue
        matching_records.append(record)
    if not matching_records:
        return EvidenceValidation(
            errors=(
                f"audit record {record_id!r} with timestamp {timestamp!r} "
                f"was not found in {path_value}",
            )
        )
    if len(matching_records) > 1:
        return EvidenceValidation(
            provenance={
                **provenance,
                "verified": False,
                "duplicate_matches": len(matching_records),
            },
            errors=(
                f"audit record {record_id!r} with timestamp {timestamp!r} "
                f"is ambiguous ({len(matching_records)} matches) — duplicate/ambiguous record (see issue #401)",
            ),
        )
    matching_record = matching_records[0]

    # Strict artifact / audit binding (issue #401): an audit-record must be
    # provably bound to the current artifact, audit, execution state, and evidence.
    if strict:
        strict_errors: list[str] = []
        # audit_id must match the audit being validated when expected is known
        record_audit_id = (
            matching_record.get("audit_id")
            or matching_record.get("audit")
            or matching_record.get("auditId")
        )
        if expected_audit_id is not None:
            if not isinstance(record_audit_id, str) or record_audit_id.strip() != expected_audit_id:
                strict_errors.append(
                    f"audit record audit_id {record_audit_id!r} does not match expected audit {expected_audit_id!r}"
                )
        elif strict:
            # In strict mode without an explicit expected id, the record must at least declare one
            if not isinstance(record_audit_id, str) or not record_audit_id.strip():
                strict_errors.append("audit record is missing audit_id (strict requires it)")
        # status must be passed
        record_status = matching_record.get("status", "")
        if not isinstance(record_status, str) or record_status.strip().lower() not in {
            "passed",
            "pass",
            "已通过",
        }:
            strict_errors.append(
                f"audit record status {record_status!r} is not passed (strict requires passed)"
            )
        # artifact binding: fail closed on artifact_id mismatch (issue #401 P1,
        # #426: no byte-hash binding — binding is by explicit artifact_id).
        record_aid = matching_record.get("artifact_id") or matching_record.get("artifactId")
        if expected_artifact_id is not None:
            if not isinstance(record_aid, str) or record_aid.strip() != expected_artifact_id:
                strict_errors.append(
                    f"audit record artifact_id {record_aid!r} does not match expected {expected_artifact_id!r}"
                )
        if expected_artifact_id is None:
            if not (
                isinstance(record_aid, str) and record_aid.strip()
            ):
                strict_errors.append(
                    "audit record is missing artifact binding (strict requires artifact_id)"
                )
        # route binding (issue #401 #4): record should declare the route it was executed for
        if expected_route is not None:
            record_route = matching_record.get("route") or matching_record.get("primary_route")
            if not isinstance(record_route, str) or record_route.strip() != expected_route:
                strict_errors.append(
                    f"audit record route {record_route!r} does not match expected route {expected_route!r}"
                )
        # executed_at must be present and not in the future
        executed_at_value = matching_record.get("executed_at") or matching_record.get("recorded_at") or matching_record.get("timestamp")
        if not isinstance(executed_at_value, str) or not executed_at_value.strip():
            strict_errors.append("audit record is missing executed_at/recorded_at (strict requires it)")
        else:
            parsed_exec = _parse_timestamp(executed_at_value)
            if parsed_exec is None:
                strict_errors.append(
                    f"audit record executed_at is not ISO-8601: {executed_at_value!r}"
                )
            else:
                now = datetime.now(timezone.utc)
                # Allow small clock skew (60s) but reject clearly future timestamps
                if parsed_exec > now:
                    # Use 60s grace
                    try:
                        # compare with tolerance
                        if (parsed_exec - now).total_seconds() > 60:
                            strict_errors.append(
                                f"audit record executed_at {executed_at_value!r} is in the future"
                            )
                    except Exception:
                        strict_errors.append(
                            f"audit record executed_at {executed_at_value!r} is in the future"
                        )
        # execution_source must be explicitly declared and align with registry (issue #401 P2).
        # Missing source is now fail-closed; caller must not auto-fill.
        if execution_type == "automated":
            # Issue #402: an automated audit-record is a validator execution
            # record — it must declare the automated_validator source, never a
            # manual attestation.  Missing source is fail-closed too.
            src = matching_record.get("execution_source") or matching_record.get("source")
            if not isinstance(src, str) or src.strip() != "automated_validator":
                strict_errors.append(
                    "audit record execution_source must be 'automated_validator' "
                    "for an automated audit (strict requires it)"
                )
        elif execution_type in {"manual", "process"}:
            src = matching_record.get("execution_source") or matching_record.get("source")
            if not isinstance(src, str) or not src.strip():
                strict_errors.append(
                    "audit record is missing execution_source (strict requires manual_checklist_attestation or process_node_evidence)"
                )
            else:
                allowed = {
                    "manual": {"manual_checklist_attestation"},
                    "process": {"process_node_evidence"},
                }.get(execution_type, set())
                if src.strip() not in allowed:
                    strict_errors.append(
                        f"audit record execution_source {src!r} does not match {execution_type} audit (expected {sorted(allowed)})"
                    )
        # validator binding (issue #402): the record must not claim support
        # from a validator different from the audit's registry binding, and a
        # manual/process record must not declare any validator_binding at all.
        record_binding = matching_record.get("validator_binding")
        if expected_validator_binding is not None:
            # Automated audit: the registry binding is the execution identity —
            # missing / null / non-string / wrong string all fail closed.
            if not isinstance(record_binding, str) or (
                record_binding.strip() != expected_validator_binding
            ):
                strict_errors.append(
                    f"audit record validator_binding {record_binding!r} does not "
                    f"match expected binding {expected_validator_binding!r} "
                    "(automated audit requires the registry binding)"
                )
        elif strict:
            # Manual/process audit: null is the only allowed validator_binding —
            # any non-null value (string, empty string, or non-string) claims
            # automated support and must fail closed.
            if record_binding is not None:
                strict_errors.append(
                    "audit record declares validator_binding for a manual/process "
                    "audit (only automated audits execute a validator; null is "
                    "the only allowed value)"
                )
        # evidence binding (issue #401 P1): record must reference the actual checklist/section that was checked
        # This prevents JSON self-attestation: hash alone is not proof that a specific audit step was executed.
        # P1/P2 review (b1916b3): nested report-/pack- evidence must be validated against the correct artifact text.
        # Using a single artifact_text for both causes type confusion (e.g. report-section:Artifact contract
        # verified against pack text).  Dispatch strictly: report-* against report_text, pack-* against pack_text,
        # checklist against base_dir (both contexts allowed).
        evidence_value = (
            matching_record.get("evidence")
            or matching_record.get("evidence_locator")
            or matching_record.get("checklist_item")
            or matching_record.get("report_section")
            or matching_record.get("report_table")
            or matching_record.get("pack_section")
            or matching_record.get("pack_table")
        )
        if not isinstance(evidence_value, str) or not evidence_value.strip():
            strict_errors.append(
                "audit record is missing evidence (strict requires checklist-item or report-section/table reference that was verified, see issue #401)"
            )
        else:
            evidence_str = evidence_value.strip()
            m = _REFERENCE_RE.match(evidence_str)
            if not m or m.group(1).lower() not in _PREFIX_TO_KIND:
                strict_errors.append(
                    f"audit record evidence {evidence_value!r} must be a typed reference (checklist-item, report-section, etc.)"
                )
            else:
                kind = _PREFIX_TO_KIND[m.group(1).lower()]
                locator = m.group(2).strip()
                if kind not in {"checklist_item", "report_section", "report_table", "pack_section", "pack_table"}:
                    strict_errors.append(
                        f"audit record evidence kind {kind!r} is not allowed — use checklist-item or report/pack section/table"
                    )
                else:
                    nested_result: EvidenceValidation | None = None
                    if kind == "checklist_item":
                        nested_result = _validate_checklist_item(locator, base_dir, strict=False)
                        if nested_result.errors:
                            strict_errors.append(
                                f"audit record evidence {evidence_value!r} is not verifiable: {'; '.join(nested_result.errors)}"
                            )
                    elif kind in {"report_section", "report_table"}:
                        # Report evidence must be validated against report artifact, not pack
                        effective_report_text = report_text
                        if effective_report_text is None and artifact_label == "report":
                            effective_report_text = artifact_text
                        if effective_report_text is None:
                            strict_errors.append(
                                f"audit record evidence {evidence_value!r} is report-scoped but no report artifact text is available for verification"
                            )
                        else:
                            # Also enforce context: report context should not verify pack evidence via report text
                            # If this record is being validated in a pack-only context (e.g. research-pack without report_text), report evidence is allowed only if report_text was supplied
                            if report_text is None and artifact_label == "pack" and pack_text is not None:
                                # Pack context without report_text — report evidence is cross-artifact, require explicit report_text
                                strict_errors.append(
                                    f"audit record evidence {evidence_value!r} is report-scoped but current pack validation has no report text"
                                )
                            else:
                                if kind == "report_section":
                                    nested_result = _validate_artifact_heading(kind, locator, effective_report_text, "report")
                                else:
                                    nested_result = _validate_artifact_table(kind, locator, effective_report_text, "report")
                                if nested_result and nested_result.errors:
                                    strict_errors.append(
                                        f"audit record evidence {evidence_value!r} is not verifiable in report: {'; '.join(nested_result.errors)}"
                                    )
                    elif kind in {"pack_section", "pack_table"}:
                        effective_pack_text = pack_text
                        if effective_pack_text is None and artifact_label == "pack":
                            effective_pack_text = artifact_text
                        if effective_pack_text is None:
                            strict_errors.append(
                                f"audit record evidence {evidence_value!r} is pack-scoped but no pack artifact text is available — not allowed in report context (see issue #401)"
                            )
                        else:
                            if pack_text is None and artifact_label == "report":
                                strict_errors.append(
                                    f"audit record evidence {evidence_value!r} is pack-scoped but current report validation has no pack text — not allowed in report context"
                                )
                            else:
                                if kind == "pack_section":
                                    nested_result = _validate_artifact_heading(kind, locator, effective_pack_text, "pack")
                                else:
                                    nested_result = _validate_artifact_table(kind, locator, effective_pack_text, "pack")
                                if nested_result and nested_result.errors:
                                    strict_errors.append(
                                        f"audit record evidence {evidence_value!r} is not verifiable in pack: {'; '.join(nested_result.errors)}"
                                    )
                    if nested_result is not None and not nested_result.errors and nested_result.provenance:
                        provenance["record_evidence"] = evidence_value
                        provenance["record_evidence_provenance"] = nested_result.provenance

        if strict_errors:
            provenance["verified"] = False
            # expose what was found for debugging / provenance
            if record_audit_id is not None:
                provenance["record_audit_id"] = record_audit_id
            if record_status:
                provenance["record_status"] = record_status
            if record_aid is not None:
                provenance["record_artifact_id"] = record_aid
            # expose route / execution_source / evidence for debugging
            _r = matching_record.get("route") or matching_record.get("primary_route")
            if _r is not None:
                provenance["record_route"] = _r
            _src = matching_record.get("execution_source") or matching_record.get("source")
            if _src is not None:
                provenance["record_execution_source"] = _src
            _ev = matching_record.get("evidence") or matching_record.get("evidence_locator")
            if _ev is not None:
                provenance["record_evidence"] = _ev
            _binding = matching_record.get("validator_binding")
            if _binding is not None:
                provenance["record_validator_binding"] = _binding
            return EvidenceValidation(
                provenance=provenance,
                errors=tuple(strict_errors),
            )

    provenance["verified"] = True
    # enrich provenance with bound fields when present
    if matching_record.get("audit_id") is not None:
        provenance["record_audit_id"] = matching_record.get("audit_id")
    if matching_record.get("status") is not None:
        provenance["record_status"] = matching_record.get("status")
    if matching_record.get("artifact_id") is not None:
        provenance["record_artifact_id"] = matching_record.get("artifact_id")
    if matching_record.get("route") is not None:
        provenance["record_route"] = matching_record.get("route")
    elif matching_record.get("primary_route") is not None:
        provenance["record_route"] = matching_record.get("primary_route")
    if matching_record.get("execution_source") is not None:
        provenance["record_execution_source"] = matching_record.get("execution_source")
    elif matching_record.get("source") is not None:
        provenance["record_execution_source"] = matching_record.get("source")
    if matching_record.get("evidence") is not None:
        provenance["record_evidence"] = matching_record.get("evidence")
    elif matching_record.get("evidence_locator") is not None:
        provenance["record_evidence"] = matching_record.get("evidence_locator")
    if matching_record.get("executed_at") is not None:
        provenance["record_executed_at"] = matching_record.get("executed_at")
    elif matching_record.get("recorded_at") is not None:
        provenance["record_executed_at"] = matching_record.get("recorded_at")
    # Preserve nested evidence provenance if it was computed in strict mode
    if "record_evidence_provenance" not in provenance and matching_record.get("evidence") is not None:
        # For non-strict, still try to expose nested evidence verification (best-effort)
        try:
            ev = matching_record.get("evidence")
            if isinstance(ev, str) and ev.strip():
                m2 = _REFERENCE_RE.match(ev.strip())
                if m2 and _PREFIX_TO_KIND.get(m2.group(1).lower()) in {"checklist_item", "report_section", "report_table", "pack_section", "pack_table"}:
                    k2 = _PREFIX_TO_KIND[m2.group(1).lower()]
                    loc2 = m2.group(2).strip()
                    nr = None
                    if k2 == "checklist_item":
                        nr = _validate_checklist_item(loc2, base_dir, strict=False)
                    elif k2 in {"report_section", "pack_section"}:
                        lbl = "pack" if k2 == "pack_section" else artifact_label
                        nr = _validate_artifact_heading(k2, loc2, artifact_text, lbl)
                    elif k2 in {"report_table", "pack_table"}:
                        lbl = "pack" if k2 == "pack_table" else artifact_label
                        nr = _validate_artifact_table(k2, loc2, artifact_text, lbl)
                    if nr and nr.provenance:
                        provenance["record_evidence_provenance"] = nr.provenance
        except Exception:
            pass
    return EvidenceValidation(provenance=provenance)


def _default_validator_bindings() -> frozenset[str]:
    """Load the canonical validator binding set without importing audit_report."""
    try:
        from registry_loader import AUDIT_BINDING_IDS
    except (ImportError, AttributeError):
        return frozenset()
    return frozenset(AUDIT_BINDING_IDS)


def validate_evidence_reference(
    reference: object,
    *,
    artifact_text: str | None = None,
    base_dir: Path | None = None,
    strict: bool = False,
    artifact_label: str = "report",
    known_validator_bindings: Collection[str] | None = None,
    execution_type: str | None = None,
    expected_audit_id: str | None = None,
    expected_artifact_id: str | None = None,
    expected_route: str | None = None,
    expected_validator_binding: str | None = None,
    report_text: str | None = None,
    pack_text: str | None = None,
) -> EvidenceValidation:
    """Validate one typed evidence reference.

    ``artifact_text`` is optional because standalone contract/pack validators
    may only have the process artifact, not the final report.  When supplied,
    section/table references are resolved against visible content.  Legacy
    free-form strings are warnings outside strict mode and errors in strict
    mode; callers can still expose their provenance explicitly.

    ``expected_validator_binding`` (issue #402) is the audit's registry
    validator_binding.  An ``automated_validator`` reference must match it
    exactly; a registered-but-wrong binding fails closed.  Nested evidence
    objects must not carry unknown fields and their ``validator_binding``
    field (when present) must agree with ``locator`` — matching the JSON
    Schema in schemas/route-activation-contract.json.
    """
    kind: str | None = None
    locator: str | None = None
    declared_binding: object | None = None
    if isinstance(reference, dict):
        allowed_fields = {
            "kind", "locator", "record_path", "record_id", "recorded_at",
            "validator_binding",
        }
        extra = set(reference) - allowed_fields
        if extra:
            return EvidenceValidation(
                errors=(
                    "evidence object has unknown field(s): "
                    + ", ".join(sorted(extra)),
                )
            )
        # Issue #402 (review round 2): the JSON Schema declares every optional
        # field as {"type": "string"} when present.  Type-check them here, at
        # the dict layer, so a non-string value on ANY kind (e.g. a
        # report_section with validator_binding=123) is rejected before
        # dispatch — not only inside the automated_validator branch.
        for field in ("record_path", "record_id", "recorded_at", "validator_binding"):
            if field in reference and not isinstance(reference[field], str):
                return EvidenceValidation(
                    errors=(f"evidence {field} must be a string",),
                )
        kind = _normalise_kind(reference.get("kind"))
        raw_locator = reference.get("locator")
        if isinstance(raw_locator, str):
            locator = raw_locator.strip()
        declared_binding = reference.get("validator_binding")
    elif isinstance(reference, str):
        raw = reference.strip()
        match = _REFERENCE_RE.match(raw)
        if match:
            kind = _PREFIX_TO_KIND.get(match.group(1).lower())
            if kind is not None:
                locator = match.group(2).strip()
        if kind is None:
            provenance = {
                "kind": "legacy_self_attested",
                "locator": raw,
                "verified": False,
            }
            if strict:
                return EvidenceValidation(
                    provenance=provenance,
                    errors=(
                        "evidence must use a typed reference; free-form "
                        "evidence is legacy_self_attested",
                    ),
                    legacy=True,
                )
            return EvidenceValidation(
                provenance=provenance,
                warnings=(
                    "free-form evidence is legacy_self_attested and was "
                    "not independently verified",
                ),
                legacy=True,
            )
    else:
        return EvidenceValidation(
            errors=(
                "evidence must be a typed reference string or object",
            )
        )

    if kind is None:
        return EvidenceValidation(
            errors=(
                "evidence kind is unknown; use report-section, report-table, "
                "pack-section, pack-table, checklist-item, audit-record, "
                "or validator",
            )
        )
    if locator is None or not locator:
        return EvidenceValidation(errors=(f"{kind} evidence locator is empty",))

    if kind in {"report_section", "pack_section"}:
        label = "pack" if kind == "pack_section" else artifact_label
        return _validate_artifact_heading(kind, locator, artifact_text, label)
    if kind in {"report_table", "pack_table"}:
        label = "pack" if kind == "pack_table" else artifact_label
        return _validate_artifact_table(kind, locator, artifact_text, label)
    if kind == "checklist_item":
        return _validate_checklist_item(locator, base_dir, strict=strict)
    if kind == "audit_record":
        return _validate_audit_record(
            locator,
            base_dir,
            strict=strict,
            expected_audit_id=expected_audit_id,
            expected_artifact_id=expected_artifact_id,
            expected_route=expected_route,
            expected_validator_binding=expected_validator_binding,
            execution_type=execution_type,
            artifact_text=artifact_text,
            artifact_label=artifact_label,
            report_text=report_text,
            pack_text=pack_text,
        )
    if kind == "automated_validator":
        if execution_type in {"manual", "process"}:
            return EvidenceValidation(
                provenance={
                    "kind": "automated_validator",
                    "locator": locator,
                    "validator_binding": locator,
                    "verified": False,
                },
                errors=(
                    f"{execution_type} audits cannot use validator evidence; "
                    "use a checklist, artifact, or audit-record reference",
                ),
            )
        known_bindings = frozenset(
            known_validator_bindings
            if known_validator_bindings is not None
            else _default_validator_bindings()
        )
        if locator not in known_bindings:
            return EvidenceValidation(
                provenance={
                    "kind": "automated_validator",
                    "locator": locator,
                    "validator_binding": locator,
                    "verified": False,
                },
                errors=(
                    f"validator binding {locator!r} is not registered",
                ),
            )
        # Issue #402: a nested object's validator_binding field must agree with
        # its locator (declared support must name the referenced validator).
        # Non-string values were already rejected at the dict layer.
        if isinstance(declared_binding, str) and declared_binding.strip() != locator:
            return EvidenceValidation(
                provenance={
                    "kind": "automated_validator",
                    "locator": locator,
                    "validator_binding": locator,
                    "declared_binding": declared_binding,
                    "verified": False,
                },
                errors=(
                    f"evidence validator_binding {declared_binding!r} does "
                    f"not match locator {locator!r}",
                ),
            )
        # Issue #402: the binding must exactly match the audit's registry
        # validator_binding.  A registered-but-wrong binding (e.g.
        # validator:report-quality for the forward-looking-claims audit) fails
        # closed instead of borrowing another validator's success.
        if expected_validator_binding is not None and locator != expected_validator_binding:
            return EvidenceValidation(
                provenance={
                    "kind": "automated_validator",
                    "locator": locator,
                    "validator_binding": locator,
                    "expected_binding": expected_validator_binding,
                    "verified": False,
                },
                errors=(
                    f"validator binding {locator!r} does not match audit "
                    f"binding {expected_validator_binding!r}",
                ),
            )
        return EvidenceValidation(
            provenance={
                "kind": "automated_validator",
                "locator": locator,
                "validator_binding": locator,
                "verified": True,
            }
        )
    return EvidenceValidation(
        errors=(f"unsupported evidence kind: {kind}",)
    )


def typed_reference(kind: str, locator: str) -> str:
    """Render a canonical string reference for fixtures and templates."""
    prefix = _KIND_TO_PREFIX.get(kind, kind)
    return f"{prefix}:{locator}"
