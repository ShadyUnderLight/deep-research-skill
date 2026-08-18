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
    if not isinstance(value, str):
        return None
    value = value.strip().lower()
    if value in _PREFIX_TO_KIND:
        return _PREFIX_TO_KIND[value]
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

    marker_patterns = (
        rf"<!--\s*audit-item\s*:\s*{re.escape(item_id)}\s*-->",
        rf"\{{#{re.escape(item_id)}\}}",
        rf"^\s*-\s*\[[ xX]\]\s+\*\*{re.escape(item_id)}\*\*",
    )
    if not any(re.search(pattern, text, re.MULTILINE) for pattern in marker_patterns):
        return EvidenceValidation(
            errors=(
                f"checklist item {item_id!r} was not found in {path_value}",
            )
        )
    provenance["verified"] = True
    return EvidenceValidation(provenance=provenance)


def _validate_audit_record(
    locator: str,
    base_dir: Path | None,
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
    matching_record = None
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
        matching_record = record
        break
    if matching_record is None:
        return EvidenceValidation(
            errors=(
                f"audit record {record_id!r} with timestamp {timestamp!r} "
                f"was not found in {path_value}",
            )
        )
    provenance["verified"] = True
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
) -> EvidenceValidation:
    """Validate one typed evidence reference.

    ``artifact_text`` is optional because standalone contract/pack validators
    may only have the process artifact, not the final report.  When supplied,
    section/table references are resolved against visible content.  Legacy
    free-form strings are warnings outside strict mode and errors in strict
    mode; callers can still expose their provenance explicitly.
    """
    kind: str | None = None
    locator: str | None = None
    if isinstance(reference, dict):
        kind = _normalise_kind(reference.get("kind"))
        raw_locator = reference.get("locator")
        if isinstance(raw_locator, str):
            locator = raw_locator.strip()
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
        return _validate_checklist_item(locator, base_dir)
    if kind == "audit_record":
        return _validate_audit_record(locator, base_dir)
    if kind == "automated_validator":
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
