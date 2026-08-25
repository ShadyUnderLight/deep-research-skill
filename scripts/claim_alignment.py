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
VALIDATOR_VERSION = "claim-alignment-v1"

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

RETRIEVAL_STATUSES = frozenset({"fetched", "unavailable", "unreadable", "not_run"})

EVIDENCE_ROLES = frozenset({"primary", "secondary", "inferred", "unknown"})

BUNDLE_REQUIRED = frozenset(
    {
        "schema_version",
        "bundle_id",
        "audited_population",
        "sampling_rule",
        "entries",
    }
)

ENTRY_REQUIRED = frozenset({"claim_id", "claim_text", "evidence_record", "excerpt"})

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

_HEADING_RE = re.compile(r"^(#{1,6})[ \t]+(.+?)[ \t]*$")


def excerpt_sha256(text: str) -> str:
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return f"sha256:{digest}"


def artifact_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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
        return errors

    @property
    def aggregate_verdict(self) -> str:
        if self.structural_errors:
            return "fail"
        verdicts = {j.verdict for j in self.judgments}
        if any(v in {"UNSUPPORTED", "AMBIGUOUS"} for v in verdicts):
            return "fail"
        if any(v == "PARTIAL" for v in verdicts):
            return "conditional-pass"
        if verdicts <= {"SUPPORTED"}:
            return "pass"
        if verdicts <= {"NOT_RUN", "RETRIEVAL_FAILED"}:
            return "not_run"
        return "fail"


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


def validate_bundle_structure(
    data: dict[str, Any],
    *,
    artifact_path: Path | None = None,
    expected_route: str | None = None,
) -> list[str]:
    errors: list[str] = []
    missing = BUNDLE_REQUIRED - set(data)
    if missing:
        errors.append(f"missing required bundle fields: {sorted(missing)}")
    if data.get("schema_version") != SCHEMA_VERSION:
        errors.append(
            f"schema_version must be '{SCHEMA_VERSION}', got {data.get('schema_version')!r}"
        )
    unknown_top = set(data) - BUNDLE_REQUIRED - {
        "fixture_version",
        "source_artifact_path",
        "source_artifact_sha256",
        "route_id",
        "gold_labels",
    }
    if unknown_top:
        errors.append(f"unknown bundle fields: {sorted(unknown_top)}")

    if artifact_path is not None and data.get("source_artifact_path"):
        declared = str(data["source_artifact_path"])
        if declared != str(artifact_path):
            errors.append(
                f"source_artifact_path mismatch: bundle declares {declared!r}, "
                f"expected {artifact_path!r}"
            )
    if artifact_path is not None and data.get("source_artifact_sha256"):
        actual_hash = artifact_sha256(artifact_path)
        declared_hash = str(data["source_artifact_sha256"])
        if declared_hash != actual_hash:
            errors.append(
                f"source_artifact_sha256 mismatch: bundle declares {declared_hash}, "
                f"artifact bytes hash {actual_hash}"
            )
    if expected_route and data.get("route_id") and data["route_id"] != expected_route:
        errors.append(
            f"route_id mismatch: bundle declares {data['route_id']!r}, "
            f"expected {expected_route!r}"
        )

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
        claim_id = entry.get("claim_id")
        if isinstance(claim_id, str) and claim_id:
            if claim_id in seen_ids:
                errors.append(f"{prefix}: duplicate claim_id {claim_id}")
            seen_ids.add(claim_id)
        record = entry.get("evidence_record")
        if isinstance(record, dict):
            record_errors = _validate_evidence_record(record, prefix)
            errors.extend(record_errors)
            if isinstance(claim_id, str) and record.get("claim_id") != claim_id:
                errors.append(
                    f"{prefix}: evidence_record.claim_id {record.get('claim_id')!r} "
                    f"does not match entry claim_id {claim_id!r}"
                )
        else:
            errors.append(f"{prefix}: evidence_record must be an object")
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
        if not isinstance(locator.get("value"), str):
            errors.append(f"{prefix}.evidence_record.locator.value must be a string")
    else:
        errors.append(f"{prefix}.evidence_record.locator must be an object")
    status = record.get("retrieval_status")
    if status not in RETRIEVAL_STATUSES:
        errors.append(f"{prefix}.evidence_record.retrieval_status invalid: {status!r}")
    role = record.get("evidence_role")
    if role not in EVIDENCE_ROLES:
        errors.append(f"{prefix}.evidence_record.evidence_role invalid: {role!r}")
    excerpt_hash = record.get("excerpt_hash")
    if isinstance(excerpt_hash, str) and not excerpt_hash.startswith("sha256:"):
        errors.append(f"{prefix}.evidence_record.excerpt_hash must start with sha256:")
    return errors


def _section_visible(artifact_text: str, heading: str) -> bool:
    visible = _visible_markdown(artifact_text)
    target = _normalise_heading(heading)
    for line in visible.splitlines():
        match = _HEADING_RE.match(line)
        if match and _normalise_heading(match.group(2)) == target:
            return True
    return False


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


def judge_entry(entry: dict[str, Any]) -> EntryJudgment:
    """Rule-based alignment verdict for one bundle entry (no gold labels)."""
    claim_id = str(entry.get("claim_id", ""))
    claim_text = str(entry.get("claim_text", ""))
    excerpt = str(entry.get("excerpt", ""))
    record = entry.get("evidence_record")
    subclaims = entry.get("subclaims")
    errors: list[str] = []
    warnings: list[str] = []

    if not isinstance(record, dict):
        return EntryJudgment(
            claim_id=claim_id,
            verdict="NOT_RUN",
            errors=["evidence_record missing"],
        )

    retrieval_status = record.get("retrieval_status")
    locator = record.get("locator") if isinstance(record.get("locator"), dict) else {}
    locator_kind = locator.get("kind")
    locator_value = str(locator.get("value", ""))

    if retrieval_status == "not_run":
        return EntryJudgment(claim_id=claim_id, verdict="NOT_RUN")

    if retrieval_status in {"unavailable", "unreadable"}:
        return EntryJudgment(claim_id=claim_id, verdict="RETRIEVAL_FAILED")

    if locator_kind == "none":
        return EntryJudgment(
            claim_id=claim_id,
            verdict="NOT_RUN",
            warnings=["anchorless locator (kind=none) cannot produce support evidence"],
        )

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

    if locator_kind == "section" and entry.get("artifact_text"):
        artifact_text = str(entry["artifact_text"])
        if not _section_visible(artifact_text, locator_value):
            errors.append(
                f"section locator {locator_value!r} not found in visible artifact text"
            )
            return EntryJudgment(
                claim_id=claim_id,
                verdict="UNSUPPORTED",
                errors=errors,
            )

    if locator_kind == "quote":
        quote = locator_value.strip()
        if quote and quote.casefold() not in excerpt.casefold():
            return EntryJudgment(claim_id=claim_id, verdict="UNSUPPORTED")

    if "subclaims" in entry and isinstance(entry.get("subclaims"), list) and not entry.get("subclaims"):
        errors.append(f"{claim_id}: PARTIAL requires non-empty subclaim decomposition")
        return EntryJudgment(
            claim_id=claim_id,
            verdict="PARTIAL",
            errors=errors,
        )

    if isinstance(subclaims, list) and subclaims:
        normalised: list[dict[str, str]] = []
        for item in subclaims:
            if not isinstance(item, dict):
                errors.append(f"{claim_id}: subclaim entry must be an object")
                continue
            text = item.get("text")
            verdict = item.get("verdict")
            if not isinstance(text, str) or not text.strip():
                errors.append(f"{claim_id}: subclaim text required")
                continue
            if verdict not in VERDICTS:
                errors.append(f"{claim_id}: invalid subclaim verdict {verdict!r}")
                continue
            normalised.append({"text": text.strip(), "verdict": str(verdict)})
        if not normalised:
            errors.append(f"{claim_id}: PARTIAL requires non-empty subclaim decomposition")
            return EntryJudgment(
                claim_id=claim_id,
                verdict="PARTIAL",
                errors=errors,
            )
        sub_verdicts = {s["verdict"] for s in normalised}
        if sub_verdicts == {"SUPPORTED"}:
            verdict = "SUPPORTED"
        elif "UNSUPPORTED" in sub_verdicts and "SUPPORTED" in sub_verdicts:
            verdict = "PARTIAL"
        elif sub_verdicts <= {"UNSUPPORTED"}:
            verdict = "UNSUPPORTED"
        elif "AMBIGUOUS" in sub_verdicts:
            verdict = "AMBIGUOUS"
        else:
            verdict = "PARTIAL"
        return EntryJudgment(
            claim_id=claim_id,
            verdict=verdict,
            subclaims=normalised,
            errors=errors,
            warnings=warnings,
        )

    overlap = _token_overlap(claim_text, excerpt)
    if locator_kind == "quote" and locator_value.strip().casefold() in excerpt.casefold():
        return EntryJudgment(claim_id=claim_id, verdict="SUPPORTED", warnings=warnings)
    if overlap >= 0.45:
        return EntryJudgment(claim_id=claim_id, verdict="SUPPORTED", warnings=warnings)
    if overlap >= 0.2:
        return EntryJudgment(claim_id=claim_id, verdict="AMBIGUOUS", warnings=warnings)
    return EntryJudgment(claim_id=claim_id, verdict="UNSUPPORTED", warnings=warnings)


def run_bundle(
    data: dict[str, Any],
    *,
    artifact_path: Path | None = None,
    expected_route: str | None = None,
) -> BundleReport:
    structural = validate_bundle_structure(
        data,
        artifact_path=artifact_path,
        expected_route=expected_route,
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

    entries = data.get("entries", [])
    counts: dict[str, int] = {v: 0 for v in VERDICTS}
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        judgment = judge_entry(entry)
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
    artifact_path: Path | None = None,
    expected_route: str | None = None,
) -> BundleReport:
    data = _load_json(path)
    return run_bundle(
        data,
        artifact_path=artifact_path,
        expected_route=expected_route,
    )


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

    fixture_version = str(
        gold_data.get("fixture_version")
        or bundle_data.get("fixture_version")
        or "unknown"
    )
    report = run_bundle(bundle_data)
    predicted = {j.claim_id: j for j in report.judgments}

    per_class: dict[str, dict[str, float | int]] = {}
    mismatches: list[str] = []
    correct = 0
    total = 0
    positives = 0
    negatives = 0

    for claim_id, gold_entry in labels.items():
        if not isinstance(gold_entry, dict):
            continue
        expected = gold_entry.get("verdict")
        if expected not in VERDICTS:
            continue
        actual = predicted.get(claim_id)
        actual_verdict = actual.verdict if actual else "NOT_RUN"
        total += 1
        if expected in {"SUPPORTED", "PARTIAL"}:
            positives += 1
        else:
            negatives += 1
        if actual_verdict == expected:
            correct += 1
        else:
            mismatches.append(
                f"{claim_id}: expected {expected}, got {actual_verdict}"
            )
        bucket = per_class.setdefault(
            expected,
            {"tp": 0, "fp": 0, "fn": 0, "tn": 0, "support": 0},
        )
        bucket["support"] = int(bucket["support"]) + 1
        if actual_verdict == expected:
            if expected in {"SUPPORTED", "PARTIAL"}:
                bucket["tp"] = int(bucket["tp"]) + 1
            else:
                bucket["tn"] = int(bucket["tn"]) + 1
        else:
            if expected in {"SUPPORTED", "PARTIAL"}:
                bucket["fn"] = int(bucket["fn"]) + 1
            else:
                bucket["fp"] = int(bucket["fp"]) + 1

    for verdict, bucket in per_class.items():
        tp = int(bucket["tp"])
        fp = int(bucket["fp"])
        fn = int(bucket["fn"])
        bucket["fnr"] = fn / (tp + fn) if (tp + fn) else 0.0
        bucket["fpr"] = fp / (fp + int(bucket["tn"])) if (fp + int(bucket["tn"])) else 0.0

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
