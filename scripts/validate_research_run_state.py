#!/usr/bin/env python3
"""Fail-closed validator for the Research Run State contract (issue #417).

Run State records process phase, run overlay, artifact hash, and checkpoints
for long / multi-track / explicit-resume research. It is not a second
interpretation of Research Pack ``research_status``, Final audit status, or
``delivery_status``.

Single-track research does not create a Run State and never invokes this
validator unless the user explicitly resumes a previous ``run_id``.

Exit codes:
    0 = snapshot (and optional transition / resume / chain) is valid
    2 = fail closed

Usage:
    python3 scripts/validate_research_run_state.py <run-state.json> [--json]
    python3 scripts/validate_research_run_state.py --from prev.json --to next.json [--json]
    python3 scripts/validate_research_run_state.py <run-state.json> \\
        --resume --artifact <pack.md> [--activation-snapshot snap.json] [--json]
    python3 scripts/validate_research_run_state.py --chain \\
        --handoff h.json --run-state r.json --pack p.md [--audit-result a.json] [--json]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

from activation_snapshot import (
    ActivationSnapshotError,
    load_activation_snapshot,
    validate_activation_reference,
)

SCHEMA_VERSION = "1"
EXIT_OK = 0
EXIT_FAIL_CLOSED = 2

PHASES = (
    "intake",
    "route_locked",
    "collecting",
    "mid_review",
    "synthesizing",
    "auditing",
    "delivered",
)
STATUSES = (
    "in_progress",
    "paused",
    "partial",
    "blocked",
    "completed",
    "aborted",
)
ENABLED_REASONS = ("parallel", "explicit_resume")
TERMINAL_STATUSES = frozenset({"completed", "aborted"})
MID_REVIEW_DECISIONS = frozenset(
    {"continue", "narrow", "pivot", "stop-and-synthesize"}
)
PENDING_DECISIONS = MID_REVIEW_DECISIONS | {"confirm-boundary", "confirm-delivery"}
HANDOFF_REQUIRED_PHASES = frozenset({"synthesizing", "auditing", "delivered"})
PARTIAL_PHASES = frozenset({"collecting", "synthesizing"})
BLOCKED_PHASES = frozenset({"collecting", "auditing"})

LEGAL_COMBINATIONS = frozenset(
    {
        ("intake", "in_progress"),
        ("intake", "paused"),
        ("intake", "aborted"),
        ("route_locked", "in_progress"),
        ("route_locked", "paused"),
        ("route_locked", "aborted"),
        ("collecting", "in_progress"),
        ("collecting", "paused"),
        ("collecting", "partial"),
        ("collecting", "blocked"),
        ("collecting", "aborted"),
        ("mid_review", "in_progress"),
        ("mid_review", "paused"),
        ("mid_review", "aborted"),
        ("synthesizing", "in_progress"),
        ("synthesizing", "paused"),
        ("synthesizing", "partial"),
        ("synthesizing", "aborted"),
        ("auditing", "in_progress"),
        ("auditing", "paused"),
        ("auditing", "blocked"),
        ("auditing", "aborted"),
        ("delivered", "completed"),
    }
)

REQUIRED_TOP_LEVEL = frozenset(
    {
        "schema_version",
        "run_id",
        "artifact_id",
        "phase",
        "status",
        "current_artifact_sha256",
        "activation_reference",
        "pending_decision",
        "last_transition_reason",
        "updated_at",
        "enabled_reason",
    }
)
OPTIONAL_TOP_LEVEL = frozenset(
    {
        "parent_artifact_id",
        "status_reason",
        "recovery_action",
        "next_action",
        "handoff_refs",
    }
)
KNOWN_TOP_LEVEL = REQUIRED_TOP_LEVEL | OPTIONAL_TOP_LEVEL
HANDOFF_REF_REQUIRED = frozenset({"handoff_id", "sha256"})

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_TIMESTAMP_RE = re.compile(
    r"^(\d{4}-\d{2}-\d{2})"
    r"(?:[Tt](\d{2}:\d{2}(?::\d{2}(?:\.\d+)?))([Zz]|[+-]\d{2}:\d{2})?)?$"
)

STABLE_IDENTITY_FIELDS = (
    "run_id",
    "artifact_id",
    "enabled_reason",
    "schema_version",
)


def _is_non_empty_str(value: object) -> bool:
    return isinstance(value, str) and value.strip() != ""


def _is_valid_timestamp(value: object) -> bool:
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
        zone = (zone_part or "").replace("z", "Z").replace("Z", "+00:00")
        dt = datetime.fromisoformat(f"{date_part}T{time_part}{zone}")
    except ValueError:
        return False
    return dt.tzinfo is not None


def sha256_file(path: Path | str) -> str:
    """Return the lowercase SHA-256 of a file's bytes."""
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _phase_index(phase: str) -> int:
    return PHASES.index(phase)


def validate_run_state_data(data: object) -> list[str]:
    """校验单个 Run State 快照。空列表表示通过。"""
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["run state must be a JSON object"]

    unknown = sorted(set(data) - KNOWN_TOP_LEVEL)
    if unknown:
        errors.append(f"unknown additional top-level field(s): {unknown}")

    missing = sorted(REQUIRED_TOP_LEVEL - set(data))
    for field in missing:
        errors.append(f"missing required field '{field}'")

    if data.get("schema_version") != SCHEMA_VERSION:
        errors.append(
            f"schema_version must be {SCHEMA_VERSION!r}, got "
            f"{data.get('schema_version')!r}"
        )

    for field in ("run_id", "artifact_id", "last_transition_reason"):
        if field in data and not _is_non_empty_str(data[field]):
            errors.append(f"'{field}' must be a non-empty string")

    phase = data.get("phase")
    if not isinstance(phase, str) or phase not in PHASES:
        errors.append(f"'phase' must be one of {list(PHASES)}, got {phase!r}")
        phase = None
    status = data.get("status")
    if not isinstance(status, str) or status not in STATUSES:
        errors.append(f"'status' must be one of {list(STATUSES)}, got {status!r}")
        status = None
    if phase is not None and status is not None:
        if (phase, status) not in LEGAL_COMBINATIONS:
            errors.append(
                f"illegal (phase, status) combination: ({phase!r}, {status!r})"
            )

    digest = data.get("current_artifact_sha256")
    if not isinstance(digest, str) or not SHA256_RE.fullmatch(digest):
        errors.append(
            "'current_artifact_sha256' must be a 64-character lowercase SHA-256"
        )

    enabled = data.get("enabled_reason")
    if not isinstance(enabled, str) or enabled not in ENABLED_REASONS:
        errors.append(
            f"'enabled_reason' must be one of {list(ENABLED_REASONS)}, "
            f"got {enabled!r}"
        )

    if "parent_artifact_id" in data and not _is_non_empty_str(
        data.get("parent_artifact_id")
    ):
        errors.append("'parent_artifact_id' must be a non-empty string when present")
    if "next_action" in data and not _is_non_empty_str(data.get("next_action")):
        errors.append("'next_action' must be a non-empty string when present")

    if status in {"partial", "blocked"} and not _is_non_empty_str(
        data.get("status_reason")
    ):
        errors.append(f"'{status}' status requires a non-empty 'status_reason'")
    if status == "blocked" and not _is_non_empty_str(data.get("recovery_action")):
        errors.append("'blocked' status requires a non-empty 'recovery_action'")
    for field in ("status_reason", "recovery_action"):
        if field in data and not _is_non_empty_str(data[field]):
            errors.append(f"'{field}' must be a non-empty string when present")

    if "updated_at" in data and not _is_valid_timestamp(data["updated_at"]):
        errors.append(
            "'updated_at' must be an ISO-8601 date or a timezone-aware "
            f"RFC 3339 timestamp, got {data.get('updated_at')!r}"
        )

    pending = data.get("pending_decision")
    if pending is not None and pending not in PENDING_DECISIONS:
        errors.append(
            f"'pending_decision' must be null or one of {sorted(PENDING_DECISIONS)}, "
            f"got {pending!r}"
        )
    if (
        phase == "mid_review"
        and status in {"in_progress", "paused"}
        and pending not in MID_REVIEW_DECISIONS
    ):
        errors.append(
            "mid_review requires pending_decision in "
            f"{sorted(MID_REVIEW_DECISIONS)}"
        )
    if phase == "delivered" and pending is not None:
        errors.append("delivered requires pending_decision to be null (consumed)")
    if phase == "delivered" and status not in {None, "completed"}:
        errors.append("delivered requires status=completed")

    try:
        validate_activation_reference(
            data.get("activation_reference"),
            label="activation_reference",
        )
    except ActivationSnapshotError as exc:
        errors.append(str(exc))

    handoff_refs = data.get("handoff_refs")
    if "handoff_refs" in data:
        if not isinstance(handoff_refs, list):
            errors.append("'handoff_refs' must be a list")
            handoff_refs = None
        else:
            seen_ids: set[str] = set()
            for index, item in enumerate(handoff_refs):
                if not isinstance(item, dict):
                    errors.append(f"handoff_refs[{index}] must be an object")
                    continue
                extra = sorted(set(item) - HANDOFF_REF_REQUIRED)
                if extra:
                    errors.append(
                        f"unknown additional handoff_refs field(s): {extra}"
                    )
                hid = item.get("handoff_id")
                if not _is_non_empty_str(hid):
                    errors.append(
                        f"handoff_refs[{index}].handoff_id must be a non-empty string"
                    )
                elif hid in seen_ids:
                    errors.append(f"duplicate handoff_id in handoff_refs: {hid!r}")
                else:
                    seen_ids.add(hid)
                digest = item.get("sha256")
                if not isinstance(digest, str) or not SHA256_RE.fullmatch(digest):
                    errors.append(
                        f"handoff_refs[{index}].sha256 must be a 64-character "
                        "lowercase SHA-256"
                    )

    if (
        enabled == "parallel"
        and phase in HANDOFF_REQUIRED_PHASES
        and not (isinstance(handoff_refs, list) and handoff_refs)
    ):
        errors.append(
            "enabled_reason=parallel and phase "
            f"{phase!r} require a non-empty handoff_refs list"
        )
    if enabled == "explicit_resume" and handoff_refs:
        errors.append(
            "enabled_reason=explicit_resume must not carry handoff_refs "
            "(single-track creates no Track Handoffs)"
        )

    return errors


def validate_transition(before: object, after: object) -> list[str]:
    """校验一次合法/非法转移。两端都必须先是合法快照。"""
    errors = validate_run_state_data(before)
    errors.extend(
        f"after: {item}" for item in validate_run_state_data(after)
    )
    if errors:
        return errors
    assert isinstance(before, dict) and isinstance(after, dict)

    for field in STABLE_IDENTITY_FIELDS:
        if before.get(field) != after.get(field):
            errors.append(
                f"transition must not change {field}: "
                f"{before.get(field)!r} -> {after.get(field)!r}"
            )
    if before.get("activation_reference") != after.get("activation_reference"):
        errors.append(
            "transition must not change activation_reference; start a new run_id"
        )
    if before.get("parent_artifact_id") != after.get("parent_artifact_id"):
        errors.append("transition must not change parent_artifact_id")

    from_status = before["status"]
    to_status = after["status"]
    from_phase = before["phase"]
    to_phase = after["phase"]
    from_idx = _phase_index(from_phase)
    to_idx = _phase_index(to_phase)
    hash_changed = (
        before["current_artifact_sha256"] != after["current_artifact_sha256"]
    )

    if hash_changed:
        if to_phase == "delivered" or to_status == "completed":
            errors.append(
                "artifact hash change cannot keep or enter delivered/completed; "
                "stale audit/handoff bindings must be re-run"
            )
        if to_phase == "auditing" and to_status != "in_progress":
            errors.append(
                "artifact hash change during auditing requires status=in_progress "
                "(re-audit); old Pass must not be reused"
            )

    if from_status in TERMINAL_STATUSES:
        if before != after:
            errors.append(
                f"terminal status {from_status!r} cannot transition "
                f"to ({to_phase!r}, {to_status!r})"
            )
        return errors

    if to_idx == from_idx:
        allowed_same = _allowed_same_phase_status(from_phase, from_status, to_status)
        if not allowed_same:
            errors.append(
                f"illegal same-phase status transfer: "
                f"{from_status!r} -> {to_status!r} at phase {from_phase!r}"
            )
        return errors

    if from_phase == "auditing" and to_phase == "synthesizing":
        if to_status != "in_progress":
            errors.append("audit-fail repair must return to synthesizing/in_progress")
        if from_status not in {"in_progress", "blocked"}:
            errors.append(
                "only in_progress or blocked auditing may return to synthesizing"
            )
        return errors

    if to_idx != from_idx + 1:
        errors.append(
            f"illegal phase skip or regression: {from_phase!r} -> {to_phase!r}"
        )
        return errors

    if from_status == "paused":
        errors.append("paused runs must resume to in_progress before advancing phase")
    if from_status == "blocked":
        errors.append("blocked runs must recover to in_progress before advancing phase")
    if from_status not in {"in_progress", "partial"}:
        errors.append(
            f"cannot advance phase from status {from_status!r}"
        )
    if from_status == "partial" and from_phase not in PARTIAL_PHASES:
        errors.append(f"partial cannot advance from phase {from_phase!r}")

    expected_to_status = "completed" if to_phase == "delivered" else "in_progress"
    if to_status != expected_to_status:
        errors.append(
            f"advancing to {to_phase!r} requires status={expected_to_status!r}, "
            f"got {to_status!r}"
        )
    if to_phase == "delivered" and from_phase != "auditing":
        errors.append("delivered can only be entered from auditing")

    return errors


def _allowed_same_phase_status(phase: str, from_status: str, to_status: str) -> bool:
    if from_status == to_status:
        return True
    if to_status == "aborted":
        return from_status not in TERMINAL_STATUSES
    if from_status == "in_progress" and to_status == "paused":
        return True
    if from_status == "paused" and to_status == "in_progress":
        return True
    if from_status == "in_progress" and to_status == "partial":
        return phase in PARTIAL_PHASES
    if from_status == "in_progress" and to_status == "blocked":
        return phase in BLOCKED_PHASES
    if from_status == "partial" and to_status == "in_progress":
        return phase in PARTIAL_PHASES
    if from_status == "blocked" and to_status == "in_progress":
        return phase in BLOCKED_PHASES
    return False


def load_run_state_file(path: Path | str) -> tuple[dict | None, list[str]]:
    path = Path(path)
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return None, [f"cannot read run state file {path}: {exc}"]
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        return None, [f"run state file {path} is not valid JSON: {exc}"]
    errors = validate_run_state_data(data)
    if errors:
        return None, [f"{path}: {item}" for item in errors]
    assert isinstance(data, dict)
    return data, []


def check_audit_result_for_delivered(audit: object, run_state: dict) -> list[str]:
    """delivered 不能由未执行或失败的审计支撑。"""
    if not isinstance(audit, dict):
        return ["audit result must be a JSON object"]
    errors: list[str] = []
    overall = audit.get("overall")
    if overall == "fail":
        errors.append(
            "audit overall=fail cannot support phase=delivered; "
            "return to synthesizing and re-audit"
        )
    elif overall not in {"pass", "conditional-pass"}:
        errors.append(
            f"audit overall {overall!r} cannot support phase=delivered"
        )
    input_hash = audit.get("input_sha256")
    if not isinstance(input_hash, str) or not SHA256_RE.fullmatch(input_hash):
        errors.append("audit result requires a valid input_sha256")
    for entry in audit.get("audits") or []:
        if not isinstance(entry, dict):
            errors.append("audit result audits entries must be objects")
            continue
        if entry.get("status") == "not_run":
            errors.append(
                "audit not_run cannot support phase=delivered "
                f"({entry.get('audit_id')!r})"
            )
    if overall == "conditional-pass" and not _is_non_empty_str(
        run_state.get("last_transition_reason")
    ):
        errors.append(
            "conditional-pass delivery requires last_transition_reason "
            "recording explicit confirmation"
        )
    return errors


def _load_json_object(path: Path | str, label: str) -> tuple[dict | None, list[str]]:
    path = Path(path)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        return None, [f"cannot read {label} {path}: {exc}"]
    except json.JSONDecodeError as exc:
        return None, [f"{label} {path} is not valid JSON: {exc}"]
    if not isinstance(data, dict):
        return None, [f"{label} must be a JSON object"]
    return data, []


def check_resume(
    state: dict,
    *,
    artifact_path: Path | str | None = None,
    activation_snapshot_path: Path | str | None = None,
) -> list[str]:
    """恢复时重验 artifact hash、activation reference、未消费 pending_decision。"""
    errors: list[str] = []
    if artifact_path is not None:
        try:
            actual = sha256_file(artifact_path)
        except OSError as exc:
            return [f"cannot read resume artifact {artifact_path}: {exc}"]
        expected = state["current_artifact_sha256"]
        if actual != expected:
            errors.append(
                "resume artifact hash is stale: "
                f"run state has {expected}, file hashes to {actual}"
            )
    if activation_snapshot_path is not None:
        errors.extend(check_activation_alignment(state, activation_snapshot_path))
    if state["status"] in TERMINAL_STATUSES:
        errors.append(
            f"cannot resume a {state['status']} run; start a new run_id"
        )
    return errors


def check_activation_alignment(
    state: dict, activation_snapshot_path: Path | str
) -> list[str]:
    """核对 activation_reference 与启用门，不把 delivered 当成 resume。"""
    try:
        snapshot = load_activation_snapshot(Path(activation_snapshot_path))
    except (ActivationSnapshotError, OSError) as exc:
        return [f"cannot load activation snapshot: {exc}"]
    errors: list[str] = []
    ref = state["activation_reference"]
    if (
        snapshot.get("activation_id") != ref["activation_id"]
        or snapshot.get("snapshot_sha256") != ref["snapshot_sha256"]
        or snapshot.get("snapshot_version") != ref["snapshot_version"]
        or snapshot.get("decision_tree_version") != ref["decision_tree_version"]
    ):
        errors.append(
            "activation_reference does not match the supplied snapshot"
        )
    decision = snapshot.get("parallelization_decision")
    if state["enabled_reason"] == "parallel" and decision != "parallel":
        errors.append(
            "enabled_reason=parallel requires activation "
            f"parallelization_decision='parallel', got {decision!r}"
        )
    if state["enabled_reason"] == "explicit_resume" and decision == "parallel":
        errors.append(
            "enabled_reason=explicit_resume is for single-track resume; "
            "parallel runs must use enabled_reason=parallel"
        )
    return errors


def bind_handoff_to_run_state(
    handoff: dict,
    run_state: dict,
    *,
    handoff_path: Path | str | None = None,
) -> list[str]:
    """把 Track Handoff 绑到当前 Run State；不改 #416 无 --run-state 时的行为。"""
    errors: list[str] = []
    artifact_ref = handoff.get("artifact_ref")
    actual_id = (
        artifact_ref.get("artifact_id") if isinstance(artifact_ref, dict) else None
    )
    expected_id = run_state.get("artifact_id")
    if actual_id != expected_id:
        errors.append(
            "artifact binding mismatch under --run-state: expected artifact_id "
            f"{expected_id!r}, got {actual_id!r}"
        )
    hid = handoff.get("handoff_id")
    refs = run_state.get("handoff_refs") or []
    matching = [
        item
        for item in refs
        if isinstance(item, dict) and item.get("handoff_id") == hid
    ]
    if (
        run_state.get("enabled_reason") == "parallel"
        and run_state.get("phase") in HANDOFF_REQUIRED_PHASES
        and not matching
    ):
        errors.append(
            f"handoff_id {hid!r} is not listed in run state handoff_refs"
        )
    if matching and handoff_path is not None:
        expected = matching[0].get("sha256")
        try:
            actual = sha256_file(handoff_path)
        except OSError as exc:
            errors.append(f"cannot hash handoff {handoff_path}: {exc}")
            return errors
        if expected != actual:
            errors.append(
                f"handoff {hid!r} sha256 is stale: run state has {expected}, "
                f"file hashes to {actual}"
            )
    return errors


def parse_pack_run_state_section(cleaned: str) -> tuple[dict | None, list[str]]:
    """解析 Pack 的可选 ``## Run state``。缺省节返回 (None, [])。"""
    heading_re = re.compile(r"^## Run state\s*$", re.MULTILINE)
    count = len(heading_re.findall(cleaned))
    if count == 0:
        return None, []
    if count > 1:
        return None, [f"Duplicate section: '## Run state' appears {count} times"]
    lines = cleaned.split("\n")
    body: list[str] = []
    collecting = False
    for line in lines:
        if re.match(r"^## Run state\s*$", line):
            collecting = True
            continue
        if collecting:
            if re.match(r"^##\s", line):
                break
            body.append(line)
    text = "\n".join(body).strip()
    if not text:
        return None, ["Run state section is present but empty"]
    parsed: dict[str, str] = {}
    for raw in text.split("\n"):
        line = raw.strip()
        line = re.sub(r"^[-*>]+\s+", "", line)
        if not line:
            continue
        if ":" in line:
            key, _, value = line.partition(":")
            parsed[key.strip().lower().replace(" ", "_")] = value.strip()
        elif "run_id" not in parsed:
            parsed["run_id"] = line
    errors: list[str] = []
    if not parsed.get("run_id"):
        errors.append("Run state section missing run_id")
    if not parsed.get("path"):
        errors.append("Run state section missing path to the Run State JSON")
    if errors:
        return None, errors
    return parsed, []


def check_pack_run_state(pack_path: Path | str, cleaned: str | None = None) -> list[str]:
    """Pack 出现 ``## Run state`` 时 fail-closed；缺省节不增加负担。"""
    pack_path = Path(pack_path)
    try:
        text = pack_path.read_text(encoding="utf-8")
    except OSError as exc:
        return [f"cannot read Research Pack {pack_path}: {exc}"]
    if cleaned is None:
        cleaned = text
    ref, errors = parse_pack_run_state_section(cleaned)
    if errors:
        return errors
    if ref is None:
        return []
    sidecar = Path(ref["path"])
    if not sidecar.is_absolute():
        sidecar = pack_path.parent / sidecar
    state, load_errors = load_run_state_file(sidecar)
    if load_errors:
        return load_errors
    assert state is not None
    if state["run_id"] != ref["run_id"]:
        errors.append(
            f"Run state run_id mismatch: pack declares {ref['run_id']!r}, "
            f"file has {state['run_id']!r}"
        )
    try:
        actual = sha256_file(pack_path)
    except OSError as exc:
        return [f"cannot hash Research Pack {pack_path}: {exc}"]
    if actual != state["current_artifact_sha256"]:
        errors.append(
            "Research Pack hash does not match run state current_artifact_sha256 "
            f"(pack={actual}, run_state={state['current_artifact_sha256']}); "
            "stale process state cannot be reused"
        )
    pack_artifact = _first_pack_section_line(cleaned, "Artifact id")
    if pack_artifact and pack_artifact != state["artifact_id"]:
        errors.append(
            f"Research Pack artifact id {pack_artifact!r} does not match "
            f"run state artifact_id {state['artifact_id']!r}"
        )
    research_status = _first_pack_section_line(cleaned, "Research status")
    errors.extend(_check_status_mapping(state, research_status=research_status))
    return errors


def load_declared_run_state(pack_path: Path | str) -> dict | None:
    """读取 Pack 声明的 Run State 快照；缺节或无法解析时返回 None。"""
    pack_path = Path(pack_path)
    try:
        cleaned = pack_path.read_text(encoding="utf-8")
    except OSError:
        return None
    ref, errors = parse_pack_run_state_section(cleaned)
    if errors or ref is None:
        return None
    sidecar = Path(ref["path"])
    if not sidecar.is_absolute():
        sidecar = pack_path.parent / sidecar
    state, load_errors = load_run_state_file(sidecar)
    if load_errors or state is None:
        return None
    return state


def _first_pack_section_line(cleaned: str, heading: str) -> str | None:
    match = re.search(
        rf"^## {re.escape(heading)}\s*\n(.+?)(?=\n## |\Z)",
        cleaned,
        re.DOTALL | re.MULTILINE,
    )
    if not match:
        return None
    for line in match.group(1).split("\n"):
        line = line.strip()
        if not line:
            continue
        line = re.sub(r"^[-*>]+\s+", "", line)
        return line
    return None


def _check_status_mapping(state: dict, *, research_status: str | None) -> list[str]:
    """禁止 Run State 与 Pack 结果态互相冒充。不交叉强制三层独立性。"""
    errors: list[str] = []
    phase = state["phase"]
    status = state["status"]
    if research_status:
        token = research_status.split()[0].lower()
        if token in {"complete", "partial", "blocked"}:
            if status == "in_progress" and token == "complete" and phase != "delivered":
                errors.append(
                    "research_status=complete cannot pair with an in-progress "
                    f"run at phase {phase!r}"
                )
            if status == "paused" and token == "complete":
                errors.append(
                    "research_status=complete cannot pair with paused run state"
                )
            if (
                status == "completed"
                and token == "blocked"
                and phase == "delivered"
            ):
                errors.append(
                    "run state completed/delivered cannot pair with "
                    "research_status=blocked without an explicit blocked overlay"
                )
    return errors


def validate_chain(
    *,
    handoff_path: Path | str,
    run_state_path: Path | str,
    pack_path: Path | str,
    audit_result_path: Path | str | None = None,
) -> list[str]:
    """端到端：Handoff → Run State → Pack → 可选 audit result。"""
    from validate_track_handoff import load_handoff_for_merge, HandoffIncomplete

    errors: list[str] = []
    state, state_errors = load_run_state_file(run_state_path)
    errors.extend(state_errors)
    try:
        handoff = load_handoff_for_merge(handoff_path)
    except HandoffIncomplete as exc:
        errors.append(str(exc))
        handoff = None
    errors.extend(check_pack_run_state(pack_path))
    if state is not None and handoff is not None:
        errors.extend(
            bind_handoff_to_run_state(
                handoff, state, handoff_path=handoff_path
            )
        )
    if state is not None and state["phase"] == "delivered":
        if audit_result_path is None:
            errors.append(
                "phase=delivered requires --audit-result; "
                "unexecuted audit cannot enter delivered"
            )
        else:
            audit, audit_errors = _load_json_object(audit_result_path, "audit result")
            errors.extend(audit_errors)
            if audit is not None:
                errors.extend(check_audit_result_for_delivered(audit, state))
    elif audit_result_path is not None and state is not None:
        audit, audit_errors = _load_json_object(audit_result_path, "audit result")
        errors.extend(audit_errors)
        if audit is not None and audit.get("overall") == "fail" and state["phase"] == "delivered":
            errors.extend(check_audit_result_for_delivered(audit, state))
    return errors


def _emit(ok: bool, errors: list[str], *, as_json: bool, extra: dict | None = None) -> int:
    payload = {"ok": ok, "errors": errors}
    if extra:
        payload.update(extra)
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        if ok:
            print("OK — Research Run State is valid")
        else:
            print("Run State validation failed:")
            for item in errors:
                print(f"  - {item}")
    return EXIT_OK if ok else EXIT_FAIL_CLOSED


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Fail-closed validator for Research Run State (issue #417)",
    )
    parser.add_argument("run_state_file", nargs="?", help="Path to the Run State JSON")
    parser.add_argument("--from", dest="from_file", default=None, help="Previous snapshot")
    parser.add_argument("--to", dest="to_file", default=None, help="Next snapshot")
    parser.add_argument("--resume", action="store_true", help="Re-validate for resume")
    parser.add_argument("--artifact", default=None, help="Current process artifact to hash")
    parser.add_argument(
        "--activation-snapshot",
        default=None,
        help="Activation snapshot to re-check on resume",
    )
    parser.add_argument("--audit-result", default=None, help="audit_report --json payload")
    parser.add_argument("--chain", action="store_true", help="Validate the e2e artifact chain")
    parser.add_argument("--handoff", default=None, help="Track Handoff JSON for --chain / bind")
    parser.add_argument("--run-state", dest="chain_run_state", default=None)
    parser.add_argument("--pack", default=None, help="Research Pack markdown for --chain")
    parser.add_argument("--json", action="store_true", help="Machine-readable JSON output")
    args = parser.parse_args(argv)

    if args.chain:
        if not args.handoff or not (args.chain_run_state or args.run_state_file) or not args.pack:
            return _emit(
                False,
                ["--chain requires --handoff, --pack, and a run-state file"],
                as_json=args.json,
            )
        run_state_path = args.chain_run_state or args.run_state_file
        errors = validate_chain(
            handoff_path=args.handoff,
            run_state_path=run_state_path,
            pack_path=args.pack,
            audit_result_path=args.audit_result,
        )
        return _emit(not errors, errors, as_json=args.json)

    if (args.from_file is None) ^ (args.to_file is None):
        return _emit(
            False,
            ["--from and --to must be supplied together"],
            as_json=args.json,
        )

    if args.from_file and args.to_file:
        before, before_errors = load_run_state_file(args.from_file)
        after, after_errors = load_run_state_file(args.to_file)
        # load_run_state_file already schema-validates; still run transition
        errors = [*before_errors, *after_errors]
        if before is not None and after is not None:
            errors = validate_transition(before, after)
            if args.audit_result and after["phase"] == "delivered":
                audit, audit_errors = _load_json_object(
                    args.audit_result, "audit result"
                )
                errors.extend(audit_errors)
                if audit is not None:
                    errors.extend(check_audit_result_for_delivered(audit, after))
        extra = None
        if before is not None and after is not None:
            extra = {
                "from_phase": before["phase"],
                "to_phase": after["phase"],
                "from_status": before["status"],
                "to_status": after["status"],
            }
        return _emit(not errors, errors, as_json=args.json, extra=extra)

    if not args.run_state_file:
        return _emit(False, ["run state file is required"], as_json=args.json)

    state, errors = load_run_state_file(args.run_state_file)
    if state is None:
        return _emit(False, errors, as_json=args.json)

    extra = {
        "run_id": state["run_id"],
        "phase": state["phase"],
        "status": state["status"],
        "enabled_reason": state["enabled_reason"],
    }

    if args.resume:
        errors.extend(
            check_resume(
                state,
                artifact_path=args.artifact,
                activation_snapshot_path=args.activation_snapshot,
            )
        )
    elif args.artifact:
        try:
            actual = sha256_file(args.artifact)
            if actual != state["current_artifact_sha256"]:
                errors.append(
                    "artifact hash mismatch: "
                    f"run state has {state['current_artifact_sha256']}, "
                    f"file hashes to {actual}"
                )
        except OSError as exc:
            errors.append(f"cannot read --artifact {args.artifact}: {exc}")

    if args.activation_snapshot and not args.resume:
        errors.extend(
            check_activation_alignment(state, args.activation_snapshot)
        )

    if args.handoff:
        from validate_track_handoff import load_handoff_for_merge, HandoffIncomplete

        try:
            handoff = load_handoff_for_merge(args.handoff)
            errors.extend(
                bind_handoff_to_run_state(
                    handoff, state, handoff_path=args.handoff
                )
            )
        except HandoffIncomplete as exc:
            errors.append(str(exc))

    if state["phase"] == "delivered":
        if args.audit_result is None:
            errors.append(
                "phase=delivered requires --audit-result; "
                "unexecuted audit cannot enter delivered"
            )
        else:
            audit, audit_errors = _load_json_object(args.audit_result, "audit result")
            errors.extend(audit_errors)
            if audit is not None:
                errors.extend(check_audit_result_for_delivered(audit, state))
    elif args.audit_result:
        audit, audit_errors = _load_json_object(args.audit_result, "audit result")
        errors.extend(audit_errors)
        if audit is not None and audit.get("overall") == "fail" and state["phase"] == "delivered":
            errors.extend(check_audit_result_for_delivered(audit, state))

    return _emit(not errors, errors, as_json=args.json, extra=extra)


if __name__ == "__main__":
    raise SystemExit(main())
