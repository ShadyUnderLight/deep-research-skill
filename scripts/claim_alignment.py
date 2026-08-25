#!/usr/bin/env python3
"""Claim–source alignment audit core (issue #419).

Offline, rule-based alignment between cited claims and retrieved excerpts.
Production judges never read calibration gold labels. Tool/retrieval failures
stay distinct from content failures.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "1"
VALIDATOR_VERSION = "claim-alignment-v2"
SCHEMA_PATH = Path(__file__).resolve().parents[1] / "schemas" / "claim-alignment-evidence.json"

VERDICTS = frozenset(
    {
        "SUPPORTED",
        "PARTIAL",
        "UNSUPPORTED",
        "AMBIGUOUS",
        "RETRIEVAL_FAILED",
        "NOT_RUN",
    }
)

LOCATOR_KINDS = frozenset(
    {"page", "section", "paragraph", "quote", "url_fragment", "none"}
)

# Locator kinds without a resolver cannot produce support evidence (issue #419).
UNRESOLVABLE_LOCATOR_KINDS = frozenset({"page", "paragraph", "url_fragment"})

RETRIEVAL_STATUSES = frozenset({"fetched", "unavailable", "unreadable", "not_run"})

EVIDENCE_ROLES = frozenset({"primary", "secondary", "inferred", "unknown"})

BUNDLE_REQUIRED = frozenset(
    {
        "schema_version",
        "bundle_id",
        "audited_population",
        "sampling_rule",
        "source_register",
        "entries",
    }
)

PRODUCTION_BINDING_FIELDS = frozenset(
    {"source_artifact_path", "source_artifact_sha256", "route_id"}
)

ENTRY_REQUIRED = frozenset(
    {"claim_id", "claim_text", "evidence_record", "excerpt"}
)

ENTRY_OPTIONAL = frozenset({"subclaim_candidates", "artifact_text"})

RECORD_REQUIRED = frozenset(
    {
        "claim_id",
        "source_id",
        "locator",
        "retrieval_status",
        "excerpt_hash",
        "evidence_role",
    }
)

SOURCE_REGISTER_REQUIRED = frozenset(
    {"source_id", "source_artifact_path", "source_artifact_sha256"}
)

_HEADING_RE = re.compile(r"^(#{1,6})[ \t]+(.+?)[ \t]*$")


@dataclass(frozen=True)
class ResolvedSource:
    """Resolved source_register entry: artifact bytes and text on disk."""

    source_id: str
    path: Path
    text: str
    sha256_hex: str


@dataclass(frozen=True)
class JudgmentContext:
    """Resolved sources for locator/excerpt binding during judging."""

    sources: dict[str, ResolvedSource]


@dataclass(frozen=True)
class BindingContext:
    """When provided, bundle must bind to the audited report artifact and route."""

    artifact_path: Path | None = None
    expected_route: str | None = None
    require_production_bindings: bool = False


@dataclass
class EntryJudgment:
    claim_id: str
    verdict: str
    subclaims: list[dict[str, str]] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


@dataclass
class BundleReport:
    bundle_id: str
    fixture_version: str | None
    audited_population: str
    sampling_rule: str
    judgments: list[EntryJudgment] = field(default_factory=list)
    structural_errors: list[str] = field(default_factory=list)
    counts: dict[str, int] = field(default_factory=dict)
    uncovered: list[str] = field(default_factory=list)
    tool_failures: list[str] = field(default_factory=list)
    unknowns: list[str] = field(default_factory=list)

    @property
    def blocking_errors(self) -> list[str]:
        errors = list(self.structural_errors)
        for j in self.judgments:
            errors.extend(j.errors)
            if j.verdict == "UNSUPPORTED":
                errors.append(f"{j.claim_id}: verdict UNSUPPORTED")
        return errors

    @property
    def advisory_warnings(self) -> list[str]:
        warnings: list[str] = []
        for j in self.judgments:
            warnings.extend(j.warnings)
            if j.verdict == "PARTIAL":
                warnings.append(
                    f"{j.claim_id}: verdict PARTIAL — review subclaim decomposition"
                )
            elif j.verdict == "AMBIGUOUS":
                warnings.append(f"{j.claim_id}: verdict AMBIGUOUS")
            elif j.verdict == "RETRIEVAL_FAILED":
                warnings.append(
                    f"{j.claim_id}: verdict RETRIEVAL_FAILED — "
                    "tool/access failure, not content unsupported"
                )
            elif j.verdict == "NOT_RUN":
                warnings.append(
                    f"{j.claim_id}: verdict NOT_RUN — audit did not produce support evidence"
                )
        return warnings

    @property
    def aggregate_verdict(self) -> str:
        """Frozen aggregation table (issue #419 review)."""
        if self.structural_errors:
            return "fail"
        verdicts = {j.verdict for j in self.judgments}
        if not verdicts:
            return "not_run"
        if "UNSUPPORTED" in verdicts:
            return "fail"
        if verdicts == {"SUPPORTED"}:
            return "pass"
        if verdicts <= {"NOT_RUN"}:
            return "not_run"
        if "PARTIAL" in verdicts:
            return "conditional-pass"
        if verdicts <= {"AMBIGUOUS"}:
            return "conditional-pass"
        if verdicts <= {"RETRIEVAL_FAILED"}:
            return "conditional-pass"
        if verdicts <= {"AMBIGUOUS", "RETRIEVAL_FAILED"}:
            return "conditional-pass"
        if verdicts <= {"SUPPORTED", "RETRIEVAL_FAILED"}:
            return "conditional-pass"
        if verdicts <= {"SUPPORTED", "AMBIGUOUS"}:
            return "conditional-pass"
        if verdicts <= {"SUPPORTED", "AMBIGUOUS", "RETRIEVAL_FAILED"}:
            return "conditional-pass"
        if "NOT_RUN" in verdicts:
            return "not_run"
        return "conditional-pass"


def excerpt_sha256(text: str) -> str:
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return f"sha256:{digest}"


def artifact_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _resolve_repo_path(path_value: str, base_dir: Path) -> Path | None:
    candidate = Path(path_value)
    if candidate.is_absolute():
        resolved = candidate.resolve()
    else:
        resolved = (base_dir / candidate).resolve()
    if not resolved.is_file():
        return None
    return resolved


def _paths_equal(declared: str, actual: Path, base_dir: Path | None = None) -> bool:
    try:
        declared_path = Path(declared)
        if not declared_path.is_absolute() and base_dir is not None:
            declared_resolved = (base_dir / declared_path).resolve()
        else:
            declared_resolved = declared_path.resolve()
        return declared_resolved == actual.resolve()
    except OSError:
        return str(declared) == str(actual)


def _normalise_heading(value: str) -> str:
    return " ".join(value.strip().split()).casefold()


def _visible_markdown(text: str) -> str:
    from validate_contract import sanitize_visible_markdown

    return sanitize_visible_markdown(text)


def _load_json(path: Path) -> dict[str, Any]:
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ValueError(f"{path}: cannot read bundle: {exc}") from exc
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path}: invalid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"{path}: bundle root must be a JSON object")
    return data


def validate_against_json_schema(data: dict[str, Any]) -> list[str]:
    """Validate bundle JSON against schemas/claim-alignment-evidence.json."""
    if not SCHEMA_PATH.is_file():
        return [f"schema file missing: {SCHEMA_PATH}"]
    try:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"cannot load claim-alignment schema: {exc}"]
    return _validate_json_schema_instance(data, schema, path="$")


def _resolve_schema_ref(ref: str, root_schema: dict[str, Any]) -> dict[str, Any]:
    if not ref.startswith("#/"):
        raise ValueError(f"unsupported $ref (only local refs): {ref!r}")
    node: Any = root_schema
    for part in ref[2:].split("/"):
        if not isinstance(node, dict) or part not in node:
            raise ValueError(f"invalid $ref {ref!r}")
        node = node[part]
    if not isinstance(node, dict):
        raise ValueError(f"$ref {ref!r} did not resolve to a schema object")
    return node


def _validate_json_schema_instance(
    value: Any,
    schema: dict[str, Any],
    *,
    path: str,
    root_schema: dict[str, Any] | None = None,
) -> list[str]:
    if root_schema is None:
        root_schema = schema
    if "$ref" in schema:
        try:
            resolved = _resolve_schema_ref(schema["$ref"], root_schema)
        except ValueError as exc:
            return [f"{path}: {exc}"]
        return _validate_json_schema_instance(
            value, resolved, path=path, root_schema=root_schema
        )
    errors: list[str] = []
    schema_type = schema.get("type")
    if schema_type == "object":
        if not isinstance(value, dict):
            return [f"{path}: expected object"]
        if schema.get("additionalProperties") is False:
            allowed = set(schema.get("properties", {}))
            extra = set(value) - allowed
            if extra:
                errors.append(f"{path}: unknown fields {sorted(extra)}")
        for key, subschema in schema.get("properties", {}).items():
            if key in value:
                errors.extend(
                    _validate_json_schema_instance(
                        value[key], subschema, path=f"{path}.{key}", root_schema=root_schema
                    )
                )
        required = schema.get("required", [])
        missing = [k for k in required if k not in value]
        if missing:
            errors.append(f"{path}: missing required fields {missing}")
    elif schema_type == "array":
        if not isinstance(value, list):
            return [f"{path}: expected array"]
        min_items = schema.get("minItems")
        if isinstance(min_items, int) and len(value) < min_items:
            errors.append(f"{path}: array shorter than minItems {min_items}")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(value):
                errors.extend(
                    _validate_json_schema_instance(
                        item, item_schema, path=f"{path}[{index}]", root_schema=root_schema
                    )
                )
    elif schema_type == "string":
        if not isinstance(value, str):
            return [f"{path}: expected string"]
        min_len = schema.get("minLength")
        if isinstance(min_len, int) and len(value) < min_len:
            errors.append(f"{path}: string shorter than minLength {min_len}")
        const = schema.get("const")
        if const is not None and value != const:
            errors.append(f"{path}: expected const {const!r}, got {value!r}")
        pattern = schema.get("pattern")
        if pattern and not re.fullmatch(pattern, value):
            errors.append(f"{path}: string does not match pattern {pattern}")
        enum = schema.get("enum")
        if isinstance(enum, list) and value not in enum:
            errors.append(f"{path}: value {value!r} not in enum {enum}")
    return errors


def build_resolved_source_register(
    register: list[Any],
    root: Path,
) -> tuple[dict[str, ResolvedSource], list[str]]:
    """Resolve source_register paths and load artifact text from disk."""
    resolved: dict[str, ResolvedSource] = {}
    errors: list[str] = []
    if not isinstance(register, list):
        return resolved, errors
    for index, source in enumerate(register):
        prefix = f"source_register[{index}]"
        if not isinstance(source, dict):
            continue
        source_id = source.get("source_id")
        if not isinstance(source_id, str) or not source_id.strip():
            continue
        src_path = source.get("source_artifact_path")
        src_hash = source.get("source_artifact_sha256")
        if not isinstance(src_path, str) or not src_path.strip():
            continue
        path = _resolve_repo_path(src_path, root)
        if path is None:
            continue
        if not isinstance(src_hash, str) or not re.fullmatch(r"[0-9a-f]{64}", src_hash):
            continue
        actual_hash = artifact_sha256(path)
        if src_hash != actual_hash:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            errors.append(f"{prefix}: cannot read source artifact: {exc}")
            continue
        resolved[source_id] = ResolvedSource(
            source_id=source_id,
            path=path,
            text=text,
            sha256_hex=actual_hash,
        )
    return resolved, errors


def _excerpt_digest_hex(excerpt_hash: str | None) -> str | None:
    if not isinstance(excerpt_hash, str):
        return None
    if excerpt_hash.startswith("sha256:"):
        digest = excerpt_hash[7:]
    else:
        digest = excerpt_hash
    if not re.fullmatch(r"[0-9a-f]{64}", digest):
        return None
    return digest


def _excerpt_bound_to_source(
    excerpt: str,
    excerpt_hash: str | None,
    source: ResolvedSource,
) -> bool:
    excerpt_digest = _excerpt_digest_hex(excerpt_hash)
    if excerpt_digest is None:
        return False
    if excerpt_digest == source.sha256_hex:
        return True
    if not excerpt.strip():
        return excerpt_digest == source.sha256_hex
    return excerpt in source.text or excerpt.casefold() in source.text.casefold()


def _validate_excerpt_source_binding(
    excerpt: str,
    excerpt_hash: str | None,
    source: ResolvedSource,
    prefix: str,
) -> list[str]:
    if _excerpt_bound_to_source(excerpt, excerpt_hash, source):
        return []
    return [
        f"{prefix}: excerpt not bound to source artifact {source.source_id!r} "
        f"({source.path})"
    ]


def validate_bundle_structure(
    data: dict[str, Any],
    *,
    binding: BindingContext | None = None,
    repo_root: Path | None = None,
) -> list[str]:
    errors = validate_against_json_schema(data)
    if "gold_labels" in data:
        errors.append("production bundle must not embed gold_labels")
    missing = BUNDLE_REQUIRED - set(data)
    if missing:
        errors.append(f"missing required bundle fields: {sorted(missing)}")
    if data.get("schema_version") != SCHEMA_VERSION:
        errors.append(
            f"schema_version must be '{SCHEMA_VERSION}', got {data.get('schema_version')!r}"
        )

    require_bindings = bool(binding and (
        binding.require_production_bindings or binding.artifact_path is not None
    ))
    if require_bindings:
        missing_binding = PRODUCTION_BINDING_FIELDS - set(data)
        if missing_binding:
            errors.append(
                f"production binding requires fields: {sorted(missing_binding)}"
            )

    root = repo_root or Path(__file__).resolve().parents[1]
    if binding and binding.artifact_path is not None:
        artifact_path = binding.artifact_path
        declared_path = data.get("source_artifact_path")
        if not isinstance(declared_path, str) or not declared_path.strip():
            errors.append("source_artifact_path required for report-bound validation")
        elif not _paths_equal(declared_path, artifact_path, base_dir=root):
            errors.append(
                f"source_artifact_path mismatch: bundle declares {declared_path!r}, "
                f"expected {artifact_path!r}"
            )
        declared_hash = data.get("source_artifact_sha256")
        if not isinstance(declared_hash, str) or not re.fullmatch(r"[0-9a-f]{64}", declared_hash):
            errors.append("source_artifact_sha256 must be a 64-char hex digest")
        else:
            actual_hash = artifact_sha256(artifact_path)
            if declared_hash != actual_hash:
                errors.append(
                    f"source_artifact_sha256 mismatch: bundle declares {declared_hash}, "
                    f"artifact bytes hash {actual_hash}"
                )
        if binding.expected_route:
            route_id = data.get("route_id")
            if not isinstance(route_id, str) or not route_id.strip():
                errors.append("route_id required for route-bound validation")
            elif route_id != binding.expected_route:
                errors.append(
                    f"route_id mismatch: bundle declares {route_id!r}, "
                    f"expected {binding.expected_route!r}"
                )

    register = data.get("source_register")
    register_ids: set[str] = set()
    if not isinstance(register, list) or not register:
        errors.append("source_register must be a non-empty array")
        register = []
    for index, source in enumerate(register):
        prefix = f"source_register[{index}]"
        if not isinstance(source, dict):
            errors.append(f"{prefix}: must be an object")
            continue
        src_missing = SOURCE_REGISTER_REQUIRED - set(source)
        if src_missing:
            errors.append(f"{prefix}: missing fields {sorted(src_missing)}")
        source_id = source.get("source_id")
        if not isinstance(source_id, str) or not source_id.strip():
            errors.append(f"{prefix}: source_id must be a non-empty string")
        else:
            if source_id in register_ids:
                errors.append(f"{prefix}: duplicate source_id {source_id}")
            register_ids.add(source_id)
        src_path = source.get("source_artifact_path")
        src_hash = source.get("source_artifact_sha256")
        if isinstance(src_path, str) and src_path.strip():
            resolved = _resolve_repo_path(src_path, root)
            if resolved is None:
                errors.append(f"{prefix}: source artifact not found: {src_path}")
            elif isinstance(src_hash, str) and re.fullmatch(r"[0-9a-f]{64}", src_hash):
                actual = artifact_sha256(resolved)
                if src_hash != actual:
                    errors.append(
                        f"{prefix}: source_artifact_sha256 mismatch for {src_path}"
                    )

    resolved_sources, resolve_errors = build_resolved_source_register(
        register if isinstance(register, list) else [], root
    )
    errors.extend(resolve_errors)

    entries = data.get("entries")
    if not isinstance(entries, list) or not entries:
        errors.append("entries must be a non-empty array")
        return errors

    seen_ids: set[str] = set()
    for index, entry in enumerate(entries):
        prefix = f"entries[{index}]"
        if not isinstance(entry, dict):
            errors.append(f"{prefix}: must be an object")
            continue
        entry_missing = ENTRY_REQUIRED - set(entry)
        if entry_missing:
            errors.append(f"{prefix}: missing fields {sorted(entry_missing)}")
        unknown_entry = set(entry) - ENTRY_REQUIRED - ENTRY_OPTIONAL
        if unknown_entry:
            errors.append(f"{prefix}: unknown fields {sorted(unknown_entry)}")
        claim_id = entry.get("claim_id")
        if isinstance(claim_id, str) and claim_id:
            if claim_id in seen_ids:
                errors.append(f"{prefix}: duplicate claim_id {claim_id}")
            seen_ids.add(claim_id)
        if not isinstance(entry.get("claim_text"), str) or not str(entry.get("claim_text")).strip():
            errors.append(f"{prefix}: claim_text must be a non-empty string")
        if not isinstance(entry.get("excerpt"), str):
            errors.append(f"{prefix}: excerpt must be a string")
        record = entry.get("evidence_record")
        if isinstance(record, dict):
            errors.extend(_validate_evidence_record(record, prefix))
            if isinstance(claim_id, str) and record.get("claim_id") != claim_id:
                errors.append(
                    f"{prefix}: evidence_record.claim_id {record.get('claim_id')!r} "
                    f"does not match entry claim_id {claim_id!r}"
                )
            source_id = record.get("source_id")
            if not isinstance(source_id, str) or not source_id.strip():
                errors.append(
                    f"{prefix}: evidence_record.source_id must be a non-empty string"
                )
            elif source_id not in register_ids:
                errors.append(
                    f"{prefix}: evidence_record.source_id {source_id!r} "
                    f"not found in source_register"
                )
            elif source_id in resolved_sources and record.get("retrieval_status") == "fetched":
                excerpt = entry.get("excerpt")
                if not isinstance(excerpt, str):
                    excerpt = ""
                errors.extend(
                    _validate_excerpt_source_binding(
                        excerpt,
                        record.get("excerpt_hash"),
                        resolved_sources[source_id],
                        prefix,
                    )
                )
        else:
            errors.append(f"{prefix}: evidence_record must be an object")
        candidates = entry.get("subclaim_candidates")
        if candidates is not None:
            if not isinstance(candidates, list):
                errors.append(f"{prefix}: subclaim_candidates must be an array")
            elif candidates and any(
                not isinstance(item, dict)
                or not isinstance(item.get("text"), str)
                or not item.get("text", "").strip()
                for item in candidates
            ):
                errors.append(f"{prefix}: subclaim_candidates require non-empty text")
            if "subclaims" in entry:
                errors.append(f"{prefix}: production entries must use subclaim_candidates, not subclaims")
    return errors


def _validate_evidence_record(record: dict[str, Any], prefix: str) -> list[str]:
    errors: list[str] = []
    missing = RECORD_REQUIRED - set(record)
    if missing:
        errors.append(f"{prefix}.evidence_record: missing fields {sorted(missing)}")
    unknown = set(record) - RECORD_REQUIRED
    if unknown:
        errors.append(f"{prefix}.evidence_record: unknown fields {sorted(unknown)}")
    locator = record.get("locator")
    if isinstance(locator, dict):
        kind = locator.get("kind")
        if kind not in LOCATOR_KINDS:
            errors.append(f"{prefix}.evidence_record.locator.kind invalid: {kind!r}")
        value = locator.get("value")
        if not isinstance(value, str):
            errors.append(f"{prefix}.evidence_record.locator.value must be a string")
        elif kind != "none" and not value.strip():
            errors.append(
                f"{prefix}.evidence_record.locator.value required when kind is {kind!r}"
            )
    else:
        errors.append(f"{prefix}.evidence_record.locator must be an object")
    status = record.get("retrieval_status")
    if status not in RETRIEVAL_STATUSES:
        errors.append(f"{prefix}.evidence_record.retrieval_status invalid: {status!r}")
    role = record.get("evidence_role")
    if role not in EVIDENCE_ROLES:
        errors.append(f"{prefix}.evidence_record.evidence_role invalid: {role!r}")
    excerpt_hash = record.get("excerpt_hash")
    if isinstance(excerpt_hash, str) and not re.fullmatch(
        r"sha256:[0-9a-f]{64}", excerpt_hash
    ):
        errors.append(f"{prefix}.evidence_record.excerpt_hash must match sha256:<hex>")
    source_id = record.get("source_id")
    if not isinstance(source_id, str) or not source_id.strip():
        errors.append(f"{prefix}.evidence_record.source_id must be a non-empty string")
    return errors


def _section_visible(artifact_text: str, heading: str) -> bool:
    return _extract_section_text(artifact_text, heading) is not None


def _extract_section_text(artifact_text: str, heading: str) -> str | None:
    """Visible markdown body from heading until next same/higher-level heading."""
    visible = _visible_markdown(artifact_text)
    target = _normalise_heading(heading)
    lines = visible.splitlines()
    start_idx: int | None = None
    start_level: int | None = None
    for index, line in enumerate(lines):
        match = _HEADING_RE.match(line)
        if match and _normalise_heading(match.group(2)) == target:
            start_idx = index + 1
            start_level = len(match.group(1))
            break
    if start_idx is None or start_level is None:
        return None
    body_lines: list[str] = []
    for line in lines[start_idx:]:
        match = _HEADING_RE.match(line)
        if match and len(match.group(1)) <= start_level:
            break
        body_lines.append(line)
    body = "\n".join(body_lines).strip()
    return body if body else None


def _resolve_quote_scope(source_text: str, quote: str) -> str | None:
    """Line scope in visible source text containing the quoted substring."""
    visible = _visible_markdown(source_text)
    quote_stripped = quote.strip()
    if not quote_stripped:
        return None
    idx = visible.find(quote_stripped)
    if idx < 0:
        return None
    line_start = visible.rfind("\n", 0, idx) + 1
    line_end = visible.find("\n", idx)
    if line_end < 0:
        line_end = len(visible)
    return visible[line_start:line_end]


_NEGATIVE_DIRECTION = frozenset({
    "decline", "declined", "decrease", "decreased", "fell", "fall", "fallen",
    "drop", "dropped", "down", "loss", "losses", "shrink", "contracted",
    "下降", "减少", "下跌", "降低", "萎缩", "回落", "下滑",
})
_POSITIVE_DIRECTION = frozenset({
    "grow", "grew", "growth", "increase", "increased", "rose", "rise", "risen",
    "up", "gain", "gains", "expand", "expanded", "surge", "surged",
    "增长", "增加", "上涨", "提高", "上升", "回升", "上升",
})


def _contains_direction_word(text: str, words: frozenset[str]) -> bool:
    text_cf = text.casefold()
    return any(word.casefold() in text_cf for word in words)


_NEGATION_PATTERNS_EN = (
    re.compile(r"\bnot\b", re.IGNORECASE),
    re.compile(r"\bno\b", re.IGNORECASE),
    re.compile(r"\bnever\b", re.IGNORECASE),
    re.compile(r"\bwithout\b", re.IGNORECASE),
    re.compile(r"\bdidn't\b", re.IGNORECASE),
    re.compile(r"\bdid not\b", re.IGNORECASE),
)
_NEGATION_MARKERS_CJK = ("没有", "未", "不再", "并非", "无")


def _has_negation(text: str) -> bool:
    if any(marker in text for marker in _NEGATION_MARKERS_CJK):
        return True
    return any(pattern.search(text) for pattern in _NEGATION_PATTERNS_EN)


def _direction_polarity_present(text: str) -> bool:
    return (
        _contains_direction_word(text, _NEGATIVE_DIRECTION)
        or _contains_direction_word(text, _POSITIVE_DIRECTION)
    )


def _negation_conflict(claim: str, excerpt: str) -> bool:
    claim_negated = _has_negation(claim)
    excerpt_negated = _has_negation(excerpt)
    if claim_negated == excerpt_negated:
        return False
    return _direction_polarity_present(claim) or _direction_polarity_present(excerpt)


def _extract_percentages(text: str) -> list[float]:
    return [float(value) for value in re.findall(r"(\d+(?:\.\d+)?)\s*%", text)]


def _numeric_percent_conflict(claim: str, excerpt: str) -> bool:
    claim_pcts = _extract_percentages(claim)
    excerpt_pcts = _extract_percentages(excerpt)
    if not claim_pcts or not excerpt_pcts:
        return False
    for claim_pct in claim_pcts:
        if not any(abs(claim_pct - excerpt_pct) < 0.01 for excerpt_pct in excerpt_pcts):
            return True
    return False


def _direction_conflict(claim: str, excerpt: str) -> bool:
    claim_neg = _contains_direction_word(claim, _NEGATIVE_DIRECTION)
    claim_pos = _contains_direction_word(claim, _POSITIVE_DIRECTION)
    excerpt_neg = _contains_direction_word(excerpt, _NEGATIVE_DIRECTION)
    excerpt_pos = _contains_direction_word(excerpt, _POSITIVE_DIRECTION)
    return (claim_neg and excerpt_pos) or (claim_pos and excerpt_neg)


def _year_mismatch(claim: str, excerpt: str) -> bool:
    claim_years = set(re.findall(r"(?:FY)?20\d{2}", claim, flags=re.IGNORECASE))
    excerpt_years = set(re.findall(r"(?:FY)?20\d{2}", excerpt, flags=re.IGNORECASE))
    if claim_years and excerpt_years and not (claim_years & excerpt_years):
        return True
    return False


def _cjk_char_overlap(claim: str, excerpt: str) -> float:
    claim_chars = {ch for ch in claim if "\u4e00" <= ch <= "\u9fff"}
    excerpt_chars = {ch for ch in excerpt if "\u4e00" <= ch <= "\u9fff"}
    if not claim_chars:
        return 0.0
    return len(claim_chars & excerpt_chars) / len(claim_chars)


def _lexical_overlap(claim: str, excerpt: str) -> float:
    return max(_token_overlap(claim, excerpt), _cjk_char_overlap(claim, excerpt))


def resolve_locator(
    source: ResolvedSource,
    locator_kind: str,
    locator_value: str,
) -> str | None:
    """Resolve locator to scope text within a source artifact, or None if unresolvable."""
    value = locator_value.strip()
    if locator_kind == "none" or not value:
        return None
    if locator_kind in UNRESOLVABLE_LOCATOR_KINDS:
        return None
    if locator_kind == "quote":
        return _resolve_quote_scope(source.text, value)
    if locator_kind == "section":
        return _extract_section_text(source.text, value)
    return None


def _locator_scope_blocks_support(
    claim_id: str,
    excerpt: str,
    locator_kind: str | None,
    locator_value: str,
    resolved_source: ResolvedSource | None,
    errors: list[str],
    warnings: list[str],
) -> EntryJudgment | None:
    """Return a terminal judgment when locator scope blocks support; else None."""
    if locator_kind == "none":
        return EntryJudgment(
            claim_id=claim_id,
            verdict="NOT_RUN",
            warnings=["anchorless locator (kind=none) cannot produce support evidence"],
        )
    if locator_kind != "none" and not locator_value.strip():
        errors.append(f"{claim_id}: locator value required when kind is {locator_kind!r}")
        return EntryJudgment(claim_id=claim_id, verdict="NOT_RUN", errors=errors)

    if resolved_source is None:
        return None

    if locator_kind in UNRESOLVABLE_LOCATOR_KINDS:
        return EntryJudgment(
            claim_id=claim_id,
            verdict="NOT_RUN",
            warnings=[
                f"locator kind {locator_kind!r} cannot be resolved for support evidence"
            ],
        )

    scope = resolve_locator(resolved_source, str(locator_kind), locator_value)
    if scope is None:
        errors.append(
            f"locator {locator_kind}:{locator_value!r} did not resolve in source "
            f"artifact {resolved_source.source_id!r}"
        )
        return EntryJudgment(claim_id=claim_id, verdict="UNSUPPORTED", errors=errors)

    if excerpt and excerpt not in scope:
        errors.append(
            f"excerpt not within resolved locator scope for "
            f"{locator_kind}:{locator_value!r}"
        )
        return EntryJudgment(claim_id=claim_id, verdict="UNSUPPORTED", errors=errors)

    return None


def _token_overlap(claim: str, excerpt: str) -> float:
    claim_tokens = {
        t.casefold()
        for t in re.findall(r"[A-Za-z0-9%]+", claim)
        if len(t) >= 3
    }
    excerpt_tokens = {
        t.casefold()
        for t in re.findall(r"[A-Za-z0-9%]+", excerpt)
        if len(t) >= 3
    }
    if not claim_tokens:
        return 0.0
    return len(claim_tokens & excerpt_tokens) / len(claim_tokens)


def _judge_claim_text(
    claim_text: str,
    excerpt: str,
    locator_kind: str | None,
    locator_value: str,
) -> str:
    if locator_kind == "quote":
        quote = locator_value.strip()
        if quote and quote not in excerpt:
            return "UNSUPPORTED"
    if _direction_conflict(claim_text, excerpt):
        return "UNSUPPORTED"
    if _negation_conflict(claim_text, excerpt):
        return "UNSUPPORTED"
    if _numeric_percent_conflict(claim_text, excerpt):
        return "UNSUPPORTED"
    if _year_mismatch(claim_text, excerpt):
        return "UNSUPPORTED"
    overlap = _lexical_overlap(claim_text, excerpt)
    if overlap >= 0.45:
        return "SUPPORTED"
    if overlap >= 0.2:
        return "AMBIGUOUS"
    return "UNSUPPORTED"


def _aggregate_subclaim_verdicts(sub_verdicts: set[str]) -> str:
    if not sub_verdicts:
        return "PARTIAL"
    if sub_verdicts == {"SUPPORTED"}:
        return "SUPPORTED"
    if "UNSUPPORTED" in sub_verdicts and "SUPPORTED" in sub_verdicts:
        return "PARTIAL"
    if sub_verdicts <= {"UNSUPPORTED"}:
        return "UNSUPPORTED"
    if "AMBIGUOUS" in sub_verdicts:
        return "AMBIGUOUS"
    return "PARTIAL"


def judge_entry(
    entry: dict[str, Any],
    *,
    context: JudgmentContext | None = None,
) -> EntryJudgment:
    """Rule-based alignment verdict for one bundle entry (no gold labels)."""
    claim_id = str(entry.get("claim_id", ""))
    claim_text = str(entry.get("claim_text", ""))
    excerpt = str(entry.get("excerpt", ""))
    record = entry.get("evidence_record")
    candidates = entry.get("subclaim_candidates")
    errors: list[str] = []
    warnings: list[str] = []

    if not isinstance(record, dict):
        return EntryJudgment(
            claim_id=claim_id,
            verdict="NOT_RUN",
            errors=["evidence_record missing"],
        )

    source_id = str(record.get("source_id", ""))
    resolved_source = (
        context.sources.get(source_id) if context and source_id else None
    )

    retrieval_status = record.get("retrieval_status")
    locator = record.get("locator") if isinstance(record.get("locator"), dict) else {}
    locator_kind = locator.get("kind")
    locator_value = str(locator.get("value", ""))

    if retrieval_status == "not_run":
        return EntryJudgment(claim_id=claim_id, verdict="NOT_RUN")

    if retrieval_status in {"unavailable", "unreadable"}:
        return EntryJudgment(claim_id=claim_id, verdict="RETRIEVAL_FAILED")

    if retrieval_status == "fetched":
        expected_hash = record.get("excerpt_hash")
        actual_hash = excerpt_sha256(excerpt)
        if expected_hash != actual_hash:
            errors.append(
                f"excerpt_hash mismatch for {claim_id}: record binds {expected_hash!r}, "
                f"excerpt bytes hash {actual_hash!r}"
            )
            return EntryJudgment(
                claim_id=claim_id,
                verdict="UNSUPPORTED",
                errors=errors,
            )
        if resolved_source is not None:
            if not _excerpt_bound_to_source(excerpt, expected_hash, resolved_source):
                errors.append(
                    f"excerpt not bound to source artifact {source_id!r} "
                    f"({resolved_source.path})"
                )
                return EntryJudgment(
                    claim_id=claim_id,
                    verdict="UNSUPPORTED",
                    errors=errors,
                )

    blocked = _locator_scope_blocks_support(
        claim_id,
        excerpt,
        str(locator_kind) if locator_kind is not None else None,
        locator_value,
        resolved_source,
        errors,
        warnings,
    )
    if blocked is not None:
        return blocked

    if isinstance(candidates, list):
        if not candidates:
            errors.append(f"{claim_id}: PARTIAL requires non-empty subclaim decomposition")
            return EntryJudgment(
                claim_id=claim_id,
                verdict="PARTIAL",
                errors=errors,
            )
        judged: list[dict[str, str]] = []
        for item in candidates:
            if not isinstance(item, dict):
                errors.append(f"{claim_id}: subclaim candidate must be an object")
                continue
            text = item.get("text")
            if not isinstance(text, str) or not text.strip():
                errors.append(f"{claim_id}: subclaim candidate text required")
                continue
            sub_verdict = _judge_claim_text(
                text.strip(), excerpt, locator_kind, locator_value
            )
            judged.append({"text": text.strip(), "verdict": sub_verdict})
        if not judged:
            errors.append(f"{claim_id}: PARTIAL requires non-empty subclaim decomposition")
            return EntryJudgment(
                claim_id=claim_id,
                verdict="PARTIAL",
                errors=errors,
            )
        verdict = _aggregate_subclaim_verdicts({j["verdict"] for j in judged})
        return EntryJudgment(
            claim_id=claim_id,
            verdict=verdict,
            subclaims=judged,
            errors=errors,
            warnings=warnings,
        )

    verdict = _judge_claim_text(claim_text, excerpt, locator_kind, locator_value)
    return EntryJudgment(claim_id=claim_id, verdict=verdict, warnings=warnings)


def run_bundle(
    data: dict[str, Any],
    *,
    binding: BindingContext | None = None,
    repo_root: Path | None = None,
) -> BundleReport:
    structural = validate_bundle_structure(
        data,
        binding=binding,
        repo_root=repo_root,
    )
    report = BundleReport(
        bundle_id=str(data.get("bundle_id", "")),
        fixture_version=(
            str(data["fixture_version"]) if data.get("fixture_version") else None
        ),
        audited_population=str(data.get("audited_population", "")),
        sampling_rule=str(data.get("sampling_rule", "")),
        structural_errors=structural,
    )
    if structural:
        return report

    root = repo_root or Path(__file__).resolve().parents[1]
    resolved_sources, resolve_errors = build_resolved_source_register(
        data.get("source_register", []) if isinstance(data.get("source_register"), list) else [],
        root,
    )
    if resolve_errors:
        report.structural_errors.extend(resolve_errors)
        return report
    context = JudgmentContext(sources=resolved_sources)

    entries = data.get("entries", [])
    counts: dict[str, int] = {v: 0 for v in VERDICTS}
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        judgment = judge_entry(entry, context=context)
        report.judgments.append(judgment)
        counts[judgment.verdict] = counts.get(judgment.verdict, 0) + 1
        if judgment.verdict == "NOT_RUN":
            report.uncovered.append(judgment.claim_id)
        if judgment.verdict == "RETRIEVAL_FAILED":
            report.tool_failures.append(judgment.claim_id)
        if judgment.verdict == "AMBIGUOUS":
            report.unknowns.append(judgment.claim_id)

    report.counts = counts
    return report


def load_and_run_bundle(
    path: Path,
    *,
    binding: BindingContext | None = None,
    repo_root: Path | None = None,
) -> BundleReport:
    data = _load_json(path)
    return run_bundle(data, binding=binding, repo_root=repo_root)


def report_to_dict(report: BundleReport) -> dict[str, Any]:
    return {
        "bundle_id": report.bundle_id,
        "fixture_version": report.fixture_version,
        "audited_population": report.audited_population,
        "sampling_rule": report.sampling_rule,
        "aggregate_verdict": report.aggregate_verdict,
        "counts": report.counts,
        "uncovered": report.uncovered,
        "tool_failures": report.tool_failures,
        "unknowns": report.unknowns,
        "structural_errors": report.structural_errors,
        "judgments": [
            {
                "claim_id": j.claim_id,
                "verdict": j.verdict,
                "subclaims": j.subclaims,
                "errors": j.errors,
                "warnings": j.warnings,
            }
            for j in report.judgments
        ],
    }


def compute_per_class_one_vs_rest(
    labels: dict[str, dict[str, Any]],
    predicted: dict[str, EntryJudgment],
) -> dict[str, dict[str, float | int]]:
    per_class: dict[str, dict[str, float | int]] = {
        cls: {"tp": 0, "fp": 0, "fn": 0, "tn": 0, "support": 0}
        for cls in VERDICTS
    }
    for claim_id, gold_entry in labels.items():
        if not isinstance(gold_entry, dict):
            continue
        gold_verdict = gold_entry.get("verdict")
        if gold_verdict not in VERDICTS:
            continue
        actual = predicted.get(claim_id)
        pred_verdict = actual.verdict if actual else "NOT_RUN"
        for cls in VERDICTS:
            if gold_verdict == cls:
                per_class[cls]["support"] = int(per_class[cls]["support"]) + 1
            if gold_verdict == cls and pred_verdict == cls:
                per_class[cls]["tp"] = int(per_class[cls]["tp"]) + 1
            elif gold_verdict != cls and pred_verdict == cls:
                per_class[cls]["fp"] = int(per_class[cls]["fp"]) + 1
            elif gold_verdict == cls and pred_verdict != cls:
                per_class[cls]["fn"] = int(per_class[cls]["fn"]) + 1
            else:
                per_class[cls]["tn"] = int(per_class[cls]["tn"]) + 1
    for cls, bucket in per_class.items():
        tp = int(bucket["tp"])
        fp = int(bucket["fp"])
        fn = int(bucket["fn"])
        tn = int(bucket["tn"])
        bucket["fnr"] = fn / (tp + fn) if (tp + fn) else 0.0
        bucket["fpr"] = fp / (fp + tn) if (fp + tn) else 0.0
    return per_class


def _validate_gold_label_entry(
    claim_id: str,
    gold_entry: Any,
    *,
    path_prefix: str,
) -> list[str]:
    errors: list[str] = []
    prefix = f"{path_prefix}[{claim_id}]"
    if not isinstance(gold_entry, dict):
        return [f"{prefix}: gold entry must be an object"]
    expected = gold_entry.get("verdict")
    if expected not in VERDICTS:
        errors.append(f"{prefix}: invalid verdict {expected!r}")
        return errors
    if expected == "PARTIAL":
        subclaims = gold_entry.get("subclaims")
        if not isinstance(subclaims, list) or not subclaims:
            errors.append(f"{prefix}: PARTIAL requires non-empty subclaims")
        else:
            for index, subclaim in enumerate(subclaims):
                sub_prefix = f"{prefix}.subclaims[{index}]"
                if not isinstance(subclaim, dict):
                    errors.append(f"{sub_prefix}: must be an object")
                    continue
                if not isinstance(subclaim.get("text"), str) or not str(subclaim.get("text")).strip():
                    errors.append(f"{sub_prefix}: text must be a non-empty string")
                sub_verdict = subclaim.get("verdict")
                if sub_verdict not in VERDICTS:
                    errors.append(f"{sub_prefix}: invalid verdict {sub_verdict!r}")
    return errors


def _subclaims_match(
    expected: list[dict[str, Any]] | None,
    actual: list[dict[str, str]],
) -> bool:
    if expected is None:
        return not actual
    if not expected:
        return False
    if len(expected) != len(actual):
        return False
    for exp, act in zip(expected, actual, strict=True):
        if not isinstance(exp, dict):
            return False
        if str(exp.get("text", "")).strip() != act.get("text", ""):
            return False
        if str(exp.get("verdict", "")) != act.get("verdict", ""):
            return False
    return True


@dataclass
class CalibrationReport:
    fixture_version: str
    threshold: float
    aggregate_accuracy: float
    per_class: dict[str, dict[str, float | int]]
    positive_samples: int
    negative_samples: int
    mismatches: list[str]


def run_calibration(
    bundle_path: Path,
    gold_path: Path,
    *,
    threshold: float = 0.85,
) -> CalibrationReport:
    """Compare judge output against an isolated gold-key file."""
    bundle_data = _load_json(bundle_path)
    gold_data = _load_json(gold_path)
    if bundle_data.get("gold_labels"):
        raise ValueError(
            f"{bundle_path}: production bundle must not embed gold_labels during calibration"
        )
    labels = gold_data.get("labels")
    if not isinstance(labels, dict):
        raise ValueError(f"{gold_path}: gold file must contain labels object")

    gold_fixture_version = gold_data.get("fixture_version")
    if not isinstance(gold_fixture_version, str) or not gold_fixture_version.strip():
        raise ValueError(f"{gold_path}: gold file must contain fixture_version")
    bundle_fixture_version = bundle_data.get("fixture_version")
    if isinstance(bundle_fixture_version, str) and bundle_fixture_version.strip():
        if bundle_fixture_version != gold_fixture_version:
            raise ValueError(
                f"{gold_path}: fixture_version {gold_fixture_version!r} does not match "
                f"bundle fixture_version {bundle_fixture_version!r}"
            )

    label_errors: list[str] = []
    for claim_id, gold_entry in labels.items():
        label_errors.extend(
            _validate_gold_label_entry(str(claim_id), gold_entry, path_prefix="labels")
        )
    if label_errors:
        raise ValueError(f"{gold_path}: invalid gold labels: {label_errors}")

    fixture_version = str(gold_fixture_version)
    report = run_bundle(bundle_data)
    if report.structural_errors:
        raise ValueError(
            f"{bundle_path}: bundle has structural errors: {report.structural_errors}"
        )
    predicted = {j.claim_id: j for j in report.judgments}
    bundle_claim_ids = {
        str(entry.get("claim_id"))
        for entry in bundle_data.get("entries", [])
        if isinstance(entry, dict) and entry.get("claim_id")
    }
    label_claim_ids = {str(key) for key in labels.keys()}
    missing_labels = sorted(bundle_claim_ids - label_claim_ids)
    extra_labels = sorted(label_claim_ids - bundle_claim_ids)
    if missing_labels:
        raise ValueError(
            f"{gold_path}: gold labels missing bundle entries: {missing_labels}"
        )
    if extra_labels:
        raise ValueError(
            f"{gold_path}: gold labels reference claims not in bundle: {extra_labels}"
        )
    per_class = compute_per_class_one_vs_rest(labels, predicted)

    mismatches: list[str] = []
    correct = 0
    total = 0
    positives = 0
    negatives = 0

    for claim_id, gold_entry in labels.items():
        expected = gold_entry.get("verdict")
        if claim_id not in bundle_claim_ids:
            continue
        actual = predicted.get(claim_id)
        actual_verdict = actual.verdict if actual else "NOT_RUN"
        total += 1
        if expected in {"SUPPORTED", "PARTIAL"}:
            positives += 1
        else:
            negatives += 1
        expected_subclaims = (
            gold_entry.get("subclaims") if expected == "PARTIAL" else None
        )
        subclaims_ok = _subclaims_match(
            expected_subclaims if isinstance(expected_subclaims, list) else None,
            actual.subclaims if actual else [],
        )
        if actual_verdict == expected and subclaims_ok:
            correct += 1
        else:
            if actual_verdict != expected:
                mismatches.append(
                    f"{claim_id}: expected {expected}, got {actual_verdict}"
                )
            elif not subclaims_ok:
                mismatches.append(f"{claim_id}: subclaim decomposition mismatch")

    if total == 0:
        raise ValueError(f"{gold_path}: gold labels contain no valid verdict entries")
    if positives == 0 or negatives == 0:
        raise ValueError(
            f"{gold_path}: calibration requires both positive and negative samples "
            f"(positives={positives}, negatives={negatives})"
        )

    accuracy = correct / total if total else 0.0
    return CalibrationReport(
        fixture_version=fixture_version,
        threshold=threshold,
        aggregate_accuracy=accuracy,
        per_class=per_class,
        positive_samples=positives,
        negative_samples=negatives,
        mismatches=mismatches,
    )
