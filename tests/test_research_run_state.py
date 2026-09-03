"""Contract tests for the Research Run State (issue #417).

Covers schema sync, valid snapshots, illegal transfers, pause/resume,
partial/blocked, audit-fail, artifact stale, terminal freeze, Pack mapping,
light-path (no Run State), CLI JSON/exit codes, and one e2e chain.
"""

from __future__ import annotations

import copy
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
FIXTURES = ROOT / "tests" / "fixtures" / "research-run-state"
AUDIT_POS_REPORT = ROOT / "tests" / "fixtures" / "audit" / "market-outlook-pos.md"
AUDIT_POS_PACK = ROOT / "tests" / "fixtures" / "audit" / "research-pack-pos.md"
HANDOFF_FIXTURES = ROOT / "tests" / "fixtures" / "track-handoff"
SCHEMA_DOC = ROOT / "schemas" / "research-run-state.json"
EXAMPLE_PACK = ROOT / "examples" / "research-pack-example.md"

sys.path.insert(0, str(SCRIPTS))

import validate_research_run_state as vrs  # noqa: E402

EMPTY_SHA = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"

PACK_BASELINE = """\
## Objective
Test task.

## Decision context
Testing run state validation.

## Primary route
Constrained choice / shortlist
Closest alternative: market-outlook (rejected — task asks "which" not "what will happen").
Boundary: if the question shifted to market trends, market-outlook would become primary.

## Secondary disciplines
source-traceability

## Core subquestions
Does the run-state sidecar bind to this pack?

## Stop condition
When tests pass.

## Source register
- [S01] Source: test source
  - Supports: test claim

## Claim register
- Claim: Status validation works. [S01]
  - Support: implementation
  - Confidence: medium

## Uncertainty register
- Uncertainty: edge cases
  - Why it matters: incorrect status could mislead

## Artifact id
research-2026-08-25-001

## Artifact contract
The report must validate correctly.

## Required audits
- final audit — passed — pack-section:Artifact contract

## Final audit status
Pass
"""


def load_valid(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def mutate(base: dict, overlay: dict | None = None, drop: list[str] | None = None) -> dict:
    data = copy.deepcopy(base)
    if overlay:
        data.update(overlay)
    for key in drop or []:
        data.pop(key, None)
    return data


def write_json(path: Path, data: dict) -> Path:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def empty_artifact(tmp_path: Path, name: str = "artifact.bin") -> Path:
    path = tmp_path / name
    path.write_bytes(b"")
    return path


def write_aligned_activation_snapshot(
    tmp_path: Path,
    state: dict,
    *,
    decision: str = "parallel",
) -> Path:
    """Bind a fixture state to a real activation snapshot for resume tests."""
    snapshot = json.loads(
        (
            ROOT
            / "tests"
            / "fixtures"
            / "forward"
            / "forward-market-outlook-baseline-activation.json"
        ).read_text(encoding="utf-8")
    )
    snapshot["parallelization_decision"] = decision
    state["activation_reference"] = {
        "activation_id": snapshot["activation_id"],
        "snapshot_version": snapshot["snapshot_version"],
        "decision_tree_version": snapshot["decision_tree_version"],
    }
    return write_json(tmp_path / "resume-activation.json", snapshot)


def write_real_pass_audit(
    tmp_path: Path,
    *,
    with_run_state: bool = False,
    run_id: str = "research-run-2026-08-25-001",
) -> tuple[Path, Path, Path]:
    """Generate a real audit_report --json Pass bound to copied report/pack files."""
    report = tmp_path / "report.md"
    report.write_text(AUDIT_POS_REPORT.read_text(encoding="utf-8"), encoding="utf-8")
    pack_text = AUDIT_POS_PACK.read_text(encoding="utf-8")
    if with_run_state:
        pack_text += (
            f"\n## Run state\nrun_id: {run_id}\npath: run-state.json\n"
        )
    pack = tmp_path / "pack.md"
    pack.write_text(pack_text, encoding="utf-8")
    if with_run_state:
        state = load_valid("valid-delivered.json")
        state["run_id"] = run_id
        state["artifact_id"] = "fixture-market-outlook-pos"
        state["current_artifact_sha256"] = vrs.sha256_file(pack)
        write_json(tmp_path / "run-state.json", state)
    proc = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "audit_report.py"),
            str(report),
            "--research-pack",
            str(pack),
            "--strict",
            "--require-contract",
            "--json",
        ],
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    audit_path = write_json(tmp_path / "audit.json", json.loads(proc.stdout))
    return report, pack, audit_path


def run_cli(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPTS / "validate_research_run_state.py"), *args],
        capture_output=True,
        text=True,
    )


def run_pack(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPTS / "validate_research_pack.py"), *args],
        capture_output=True,
        text=True,
    )


def run_handoff(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPTS / "validate_track_handoff.py"), *args],
        capture_output=True,
        text=True,
    )


def cli_state(data: dict, tmp_path: Path, *extra: str) -> subprocess.CompletedProcess:
    path = write_json(tmp_path / "run-state.json", data)
    return run_cli(str(path), *extra)


def test_schema_doc_exists_with_version_1():
    assert SCHEMA_DOC.exists()
    doc = json.loads(SCHEMA_DOC.read_text(encoding="utf-8"))
    assert doc.get("version") == 1
    assert doc.get("schema_version") == "1"


def test_schema_required_fields_match_validator():
    doc = json.loads(SCHEMA_DOC.read_text(encoding="utf-8"))
    assert set(doc["required"]) == set(vrs.REQUIRED_TOP_LEVEL)


def test_schema_phase_and_status_enums_match_validator():
    doc = json.loads(SCHEMA_DOC.read_text(encoding="utf-8"))
    assert doc["properties"]["phase"]["enum"] == list(vrs.PHASES)
    assert doc["properties"]["status"]["enum"] == list(vrs.STATUSES)
    assert doc["properties"]["enabled_reason"]["enum"] == list(vrs.ENABLED_REASONS)


@pytest.mark.parametrize(
    "name",
    [
        "valid-collecting.json",
        "valid-mid-review.json",
        "valid-paused.json",
        "valid-partial.json",
        "valid-blocked.json",
        "valid-explicit-resume.json",
    ],
)
def test_valid_snapshot_fixtures_pass_cli(name):
    proc = run_cli(str(FIXTURES / name), "--json")
    payload = json.loads(proc.stdout)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert payload["ok"] is True
    assert payload["errors"] == []


def test_valid_delivered_requires_audit_result_on_cli(tmp_path):
    missing = run_cli(str(FIXTURES / "valid-delivered.json"), "--json")
    payload = json.loads(missing.stdout)
    assert missing.returncode == 2
    assert payload["ok"] is False
    assert any("audit-result" in err for err in payload["errors"])

    report, pack, audit_path = write_real_pass_audit(tmp_path)
    state = load_valid("valid-delivered.json")
    state["current_artifact_sha256"] = vrs.sha256_file(pack)
    state_path = write_json(tmp_path / "delivered.json", state)

    no_artifact = run_cli(
        str(state_path),
        "--audit-result",
        str(audit_path),
        "--report",
        str(report),
        "--json",
    )
    payload = json.loads(no_artifact.stdout)
    assert no_artifact.returncode == 2
    assert any("artifact" in err for err in payload["errors"])

    no_report = run_cli(
        str(state_path),
        "--audit-result",
        str(audit_path),
        "--artifact",
        str(pack),
        "--json",
    )
    payload = json.loads(no_report.stdout)
    assert no_report.returncode == 2
    assert any("report" in err for err in payload["errors"])

    ok = run_cli(
        str(state_path),
        "--audit-result",
        str(audit_path),
        "--artifact",
        str(pack),
        "--report",
        str(report),
        "--json",
    )
    payload = json.loads(ok.stdout)
    assert ok.returncode == 0, ok.stdout + ok.stderr
    assert payload["ok"] is True


def test_validate_run_state_data_accepts_delivered_snapshot():
    assert vrs.validate_run_state_data(load_valid("valid-delivered.json")) == []


def _walk_states() -> list[dict]:
    collecting = load_valid("valid-collecting.json")
    handoff_refs = [
        {"handoff_id": "track-2026-08-24-competitors", "sha256": EMPTY_SHA}
    ]
    return [
        mutate(collecting, {"phase": "intake", "status": "in_progress",
                            "last_transition_reason": "run created"}),
        mutate(collecting, {"phase": "route_locked", "status": "in_progress",
                            "last_transition_reason": "route locked"}),
        collecting,
        load_valid("valid-mid-review.json"),
        mutate(collecting, {"phase": "synthesizing", "status": "in_progress",
                            "pending_decision": None,
                            "handoff_refs": handoff_refs,
                            "last_transition_reason": "search decision=continue"}),
        mutate(collecting, {"phase": "auditing", "status": "in_progress",
                            "handoff_refs": handoff_refs,
                            "last_transition_reason": "synthesis closed; audits running"}),
        load_valid("valid-delivered.json"),
    ]


def test_normal_path_transitions_are_legal():
    states = _walk_states()
    for before, after in zip(states, states[1:]):
        errors = vrs.validate_transition(before, after)
        assert errors == [], (before["phase"], after["phase"], errors)


def test_normal_path_transitions_pass_cli(tmp_path):
    states = _walk_states()
    report, pack, audit_path = write_real_pass_audit(tmp_path)
    pack_sha = vrs.sha256_file(pack)
    for before, after in zip(states, states[1:]):
        extra: list[str] = []
        if after["phase"] == "delivered":
            before = mutate(before, {"current_artifact_sha256": pack_sha})
            after = mutate(after, {"current_artifact_sha256": pack_sha})
            extra = [
                "--audit-result",
                str(audit_path),
                "--artifact",
                str(pack),
                "--report",
                str(report),
            ]
        prev = write_json(tmp_path / "from.json", before)
        nxt = write_json(tmp_path / "to.json", after)
        proc = run_cli("--from", str(prev), "--to", str(nxt), "--json", *extra)
        payload = json.loads(proc.stdout)
        assert proc.returncode == 0, (before["phase"], after["phase"], proc.stdout)
        assert payload["ok"] is True


def test_pause_and_resume_same_phase(tmp_path):
    collecting = load_valid("valid-collecting.json")
    paused = load_valid("valid-paused.json")
    assert vrs.validate_transition(collecting, paused) == []
    resumed = mutate(paused, {"status": "in_progress",
                              "last_transition_reason": "session resumed"})
    assert vrs.validate_transition(paused, resumed) == []

    artifact = tmp_path / "pack.md"
    artifact.write_bytes(b"")
    paused["current_artifact_sha256"] = vrs.sha256_file(artifact)
    snapshot_path = write_aligned_activation_snapshot(tmp_path, paused)
    paused_path = write_json(tmp_path / "paused.json", paused)
    proc = run_cli(
        str(paused_path),
        "--resume",
        "--artifact",
        str(artifact),
        "--activation-snapshot",
        str(snapshot_path),
        "--json",
    )
    assert json.loads(proc.stdout)["ok"] is True
    assert proc.returncode == 0


def test_resume_rechecks_unconsumed_pending_decision(tmp_path):
    mid = load_valid("valid-mid-review.json")
    artifact = tmp_path / "pack.md"
    artifact.write_bytes(b"")
    mid["current_artifact_sha256"] = vrs.sha256_file(artifact)
    snapshot_path = write_aligned_activation_snapshot(tmp_path, mid)
    path = write_json(tmp_path / "mid.json", mid)
    proc = run_cli(
        str(path),
        "--resume",
        "--artifact",
        str(artifact),
        "--activation-snapshot",
        str(snapshot_path),
        "--json",
    )
    payload = json.loads(proc.stdout)
    assert proc.returncode == 0
    assert payload["ok"] is True
    assert mid["pending_decision"] == "continue"


def test_resume_stale_artifact_fails(tmp_path):
    paused = load_valid("valid-paused.json")
    artifact = tmp_path / "pack.md"
    artifact.write_text("stale-body", encoding="utf-8")
    snapshot_path = write_aligned_activation_snapshot(tmp_path, paused)
    path = write_json(tmp_path / "paused.json", paused)
    proc = run_cli(
        str(path),
        "--resume",
        "--artifact",
        str(artifact),
        "--activation-snapshot",
        str(snapshot_path),
        "--json",
    )
    payload = json.loads(proc.stdout)
    assert proc.returncode == 2
    assert any("stale" in err for err in payload["errors"])


def test_resume_requires_artifact_and_activation_snapshot(tmp_path):
    state_path = write_json(tmp_path / "paused.json", load_valid("valid-paused.json"))
    proc = run_cli(str(state_path), "--resume", "--json")
    payload = json.loads(proc.stdout)
    assert proc.returncode == 2
    assert any("--artifact" in err for err in payload["errors"])
    assert any("--activation-snapshot" in err for err in payload["errors"])


def test_partial_and_blocked_require_reasons():
    collecting = load_valid("valid-collecting.json")
    partial = mutate(collecting, {"status": "partial"})
    assert any("status_reason" in err for err in vrs.validate_run_state_data(partial))
    blocked = mutate(collecting, {"status": "blocked", "status_reason": "provider down"})
    assert any("recovery_action" in err for err in vrs.validate_run_state_data(blocked))
    assert vrs.validate_run_state_data(load_valid("valid-partial.json")) == []
    assert vrs.validate_run_state_data(load_valid("valid-blocked.json")) == []


def test_partial_and_blocked_transitions_from_collecting():
    collecting = load_valid("valid-collecting.json")
    assert vrs.validate_transition(collecting, load_valid("valid-partial.json")) == []
    assert vrs.validate_transition(collecting, load_valid("valid-blocked.json")) == []


def test_skip_audit_to_delivered_fails():
    synthesizing = mutate(
        load_valid("valid-collecting.json"),
        {
            "phase": "synthesizing",
            "handoff_refs": [
                {"handoff_id": "track-2026-08-24-competitors", "sha256": EMPTY_SHA}
            ],
            "last_transition_reason": "search decision=continue",
        },
    )
    delivered = load_valid("valid-delivered.json")
    errors = vrs.validate_transition(synthesizing, delivered)
    assert errors
    assert any("skip" in err or "auditing" in err for err in errors)


def test_audit_fail_cannot_enter_delivered(tmp_path):
    auditing = mutate(
        load_valid("valid-collecting.json"),
        {
            "phase": "auditing",
            "handoff_refs": [
                {"handoff_id": "track-2026-08-24-competitors", "sha256": EMPTY_SHA}
            ],
            "last_transition_reason": "audits running",
        },
    )
    delivered = load_valid("valid-delivered.json")
    assert vrs.validate_transition(auditing, delivered) == []
    prev = write_json(tmp_path / "from.json", auditing)
    nxt = write_json(tmp_path / "to.json", delivered)
    proc = run_cli(
        "--from",
        str(prev),
        "--to",
        str(nxt),
        "--audit-result",
        str(FIXTURES / "valid-audit-fail.json"),
        "--artifact",
        str(empty_artifact(tmp_path, "pack.bin")),
        "--report",
        str(empty_artifact(tmp_path, "report.md")),
        "--json",
    )
    payload = json.loads(proc.stdout)
    assert proc.returncode == 2
    assert any("fail" in err for err in payload["errors"])


def test_audit_fail_repair_returns_to_synthesizing():
    auditing = mutate(
        load_valid("valid-collecting.json"),
        {
            "phase": "auditing",
            "status": "blocked",
            "status_reason": "required audit failed on source ids",
            "recovery_action": "fix claims and re-run final audit",
            "handoff_refs": [
                {"handoff_id": "track-2026-08-24-competitors", "sha256": EMPTY_SHA}
            ],
            "last_transition_reason": "audit failed",
        },
    )
    synthesizing = mutate(
        load_valid("valid-collecting.json"),
        {
            "phase": "synthesizing",
            "status": "in_progress",
            "handoff_refs": [
                {"handoff_id": "track-2026-08-24-competitors", "sha256": EMPTY_SHA}
            ],
            "last_transition_reason": "repairing after audit fail",
        },
    )
    assert vrs.validate_transition(auditing, synthesizing) == []


def test_stale_hash_cannot_stay_delivered():
    delivered = load_valid("valid-delivered.json")
    stale = mutate(delivered, {"current_artifact_sha256": "ab" * 32})
    errors = vrs.validate_transition(delivered, stale)
    assert errors
    assert any("hash" in err for err in errors)


def test_completed_cannot_return_to_in_progress():
    delivered = load_valid("valid-delivered.json")
    back = mutate(
        delivered,
        {"phase": "auditing", "status": "in_progress", "pending_decision": None},
    )
    errors = vrs.validate_transition(delivered, back)
    assert errors
    assert any("terminal" in err or "in_progress" in err for err in errors)


def test_paused_cannot_advance_phase_without_resume():
    paused = load_valid("valid-paused.json")
    mid = load_valid("valid-mid-review.json")
    errors = vrs.validate_transition(paused, mid)
    assert any("paused" in err for err in errors)


def test_blocked_without_reason_fails_cli(tmp_path):
    blocked = mutate(load_valid("valid-collecting.json"), {"status": "blocked"})
    proc = cli_state(blocked, tmp_path, "--json")
    payload = json.loads(proc.stdout)
    assert proc.returncode == 2
    assert any("status_reason" in err for err in payload["errors"])


def test_mid_review_without_pending_decision_fails():
    mid = mutate(load_valid("valid-mid-review.json"), {"pending_decision": None})
    errors = vrs.validate_run_state_data(mid)
    assert any("pending_decision" in err for err in errors)


def test_explicit_resume_rejects_handoff_refs():
    state = mutate(
        load_valid("valid-explicit-resume.json"),
        {"handoff_refs": [{"handoff_id": "x", "sha256": EMPTY_SHA}]},
    )
    errors = vrs.validate_run_state_data(state)
    assert any("handoff_refs" in err for err in errors)


def test_parallel_synthesizing_requires_handoff_refs():
    state = mutate(
        load_valid("valid-collecting.json"),
        {"phase": "synthesizing", "last_transition_reason": "continue"},
    )
    errors = vrs.validate_run_state_data(state)
    assert any("handoff_refs" in err for err in errors)


def test_illegal_phase_status_combination():
    delivered = mutate(load_valid("valid-delivered.json"), {"status": "in_progress"})
    errors = vrs.validate_run_state_data(delivered)
    assert any("combination" in err or "completed" in err for err in errors)


def _snapshot_with_parallelization(decision: str) -> dict:
    snapshot = json.loads(
        (ROOT / "tests/fixtures/forward/forward-market-outlook-baseline-activation.json")
        .read_text(encoding="utf-8")
    )
    snapshot["parallelization_decision"] = decision
    return snapshot


def test_resume_rejects_parallel_gate_on_single_track_snapshot(tmp_path):
    state = load_valid("valid-paused.json")
    snapshot = _snapshot_with_parallelization("single-track")
    snap_path = write_json(tmp_path / "snap.json", snapshot)
    state["activation_reference"] = {
        "activation_id": snapshot["activation_id"],
        "snapshot_version": snapshot["snapshot_version"],
        "decision_tree_version": snapshot["decision_tree_version"],
    }
    artifact = tmp_path / "pack.md"
    artifact.write_bytes(b"")
    state["current_artifact_sha256"] = vrs.sha256_file(artifact)
    path = write_json(tmp_path / "state.json", state)
    proc = run_cli(
        str(path),
        "--resume",
        "--artifact",
        str(artifact),
        "--activation-snapshot",
        str(snap_path),
        "--json",
    )
    payload = json.loads(proc.stdout)
    assert proc.returncode == 2
    assert any("parallel" in err for err in payload["errors"])


def test_resume_accepts_aligned_parallel_snapshot(tmp_path):
    state = load_valid("valid-paused.json")
    snapshot = _snapshot_with_parallelization("parallel")
    snap_path = write_json(tmp_path / "snap.json", snapshot)
    state["activation_reference"] = {
        "activation_id": snapshot["activation_id"],
        "snapshot_version": snapshot["snapshot_version"],
        "decision_tree_version": snapshot["decision_tree_version"],
    }
    artifact = tmp_path / "pack.md"
    artifact.write_bytes(b"")
    state["current_artifact_sha256"] = vrs.sha256_file(artifact)
    path = write_json(tmp_path / "state.json", state)
    proc = run_cli(
        str(path),
        "--resume",
        "--artifact",
        str(artifact),
        "--activation-snapshot",
        str(snap_path),
        "--json",
    )
    assert json.loads(proc.stdout)["ok"] is True


def test_cannot_resume_completed_run(tmp_path):
    delivered = load_valid("valid-delivered.json")
    artifact = tmp_path / "pack.md"
    artifact.write_bytes(b"")
    delivered["current_artifact_sha256"] = vrs.sha256_file(artifact)
    snapshot_path = write_aligned_activation_snapshot(tmp_path, delivered)
    path = write_json(tmp_path / "delivered.json", delivered)
    proc = run_cli(
        str(path),
        "--resume",
        "--artifact",
        str(artifact),
        "--audit-result",
        str(FIXTURES / "valid-audit-pass.json"),
        "--report",
        str(empty_artifact(tmp_path, "report.md")),
        "--activation-snapshot",
        str(snapshot_path),
        "--json",
    )
    payload = json.loads(proc.stdout)
    assert proc.returncode == 2
    assert any("completed" in err or "resume" in err for err in payload["errors"])


def test_example_pack_without_run_state_still_passes_strict():
    proc = run_pack(str(EXAMPLE_PACK), "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr


def _write_pack(tmp_path: Path, extra: str = "") -> Path:
    pack = tmp_path / "pack.md"
    pack.write_text(PACK_BASELINE + extra, encoding="utf-8")
    return pack


def test_pack_without_run_state_section_keeps_light_path(tmp_path):
    pack = _write_pack(tmp_path)
    proc = run_pack(str(pack), "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_pack_run_state_hash_mismatch_fails_strict(tmp_path):
    sidecar = tmp_path / "run-state.json"
    write_json(sidecar, load_valid("valid-collecting.json"))
    pack = _write_pack(
        tmp_path,
        "\n## Run state\n"
        "run_id: research-run-2026-08-25-001\n"
        "path: run-state.json\n",
    )
    proc = run_pack(str(pack), "--strict")
    assert proc.returncode == 4
    assert "current_artifact_sha256" in proc.stdout


def test_pack_run_state_matching_hash_passes(tmp_path):
    pack = _write_pack(
        tmp_path,
        "\n## Run state\n"
        "run_id: research-run-2026-08-25-001\n"
        "path: run-state.json\n",
    )
    state = load_valid("valid-collecting.json")
    state["current_artifact_sha256"] = vrs.sha256_file(pack)
    write_json(tmp_path / "run-state.json", state)
    proc = run_pack(str(pack), "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_pack_in_progress_cannot_claim_research_complete(tmp_path):
    pack = _write_pack(
        tmp_path,
        "\n## Research status\ncomplete\n"
        "\n## Run state\n"
        "run_id: research-run-2026-08-25-001\n"
        "path: run-state.json\n",
    )
    state = load_valid("valid-collecting.json")
    state["current_artifact_sha256"] = vrs.sha256_file(pack)
    write_json(tmp_path / "run-state.json", state)
    proc = run_pack(str(pack), "--strict")
    assert proc.returncode == 4
    assert "complete" in proc.stdout


def test_handoff_without_run_state_flag_unchanged():
    proc = run_handoff(str(HANDOFF_FIXTURES / "valid-complete.json"))
    assert proc.returncode == 0, proc.stdout


def test_handoff_run_state_binding_detects_stale_hash(tmp_path):
    handoff = json.loads((HANDOFF_FIXTURES / "valid-complete.json").read_text())
    handoff["artifact_ref"] = {"artifact_id": "research-2026-08-25-001"}
    handoff_path = write_json(tmp_path / "handoff.json", handoff)
    state = load_valid("valid-delivered.json")
    state["handoff_refs"] = [
        {"handoff_id": handoff["handoff_id"], "sha256": EMPTY_SHA}
    ]
    state_path = write_json(tmp_path / "run-state.json", state)
    proc = run_handoff(str(handoff_path), "--run-state", str(state_path))
    assert proc.returncode == 2
    assert "stale" in proc.stdout or "sha256" in proc.stdout


def test_handoff_run_state_binding_accepts_matching_hash(tmp_path):
    handoff = json.loads((HANDOFF_FIXTURES / "valid-complete.json").read_text())
    handoff["artifact_ref"] = {"artifact_id": "research-2026-08-25-001"}
    handoff_path = write_json(tmp_path / "handoff.json", handoff)
    state = load_valid("valid-delivered.json")
    state["handoff_refs"] = [
        {
            "handoff_id": handoff["handoff_id"],
            "sha256": vrs.sha256_file(handoff_path),
        }
    ]
    state_path = write_json(tmp_path / "run-state.json", state)
    proc = run_handoff(str(handoff_path), "--run-state", str(state_path))
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_e2e_chain_tamper_cannot_deliver(tmp_path):
    report, pack, audit_path = write_real_pass_audit(
        tmp_path, with_run_state=True
    )
    handoff = json.loads((HANDOFF_FIXTURES / "valid-complete.json").read_text())
    handoff["artifact_ref"] = {"artifact_id": "fixture-market-outlook-pos"}
    handoff_path = write_json(tmp_path / "handoff.json", handoff)
    state = json.loads((tmp_path / "run-state.json").read_text(encoding="utf-8"))
    state["handoff_refs"] = [
        {
            "handoff_id": handoff["handoff_id"],
            "sha256": vrs.sha256_file(handoff_path),
        }
    ]
    state_path = write_json(tmp_path / "run-state.json", state)
    chain_base = [
        "--chain",
        "--handoff",
        str(handoff_path),
        "--run-state",
        str(state_path),
        "--pack",
        str(pack),
        "--report",
        str(report),
        "--json",
    ]

    ok = run_cli(*chain_base, "--audit-result", str(audit_path))
    payload = json.loads(ok.stdout)
    assert ok.returncode == 0, ok.stdout + ok.stderr
    assert payload["ok"] is True

    tampered_handoff = mutate(handoff, {"question": "tampered question"})
    write_json(handoff_path, tampered_handoff)
    stale_handoff = run_cli(*chain_base, "--audit-result", str(audit_path))
    assert stale_handoff.returncode == 2
    write_json(handoff_path, handoff)

    pack.write_text(pack.read_text(encoding="utf-8") + "\n<!-- tamper -->\n", encoding="utf-8")
    stale_pack = run_cli(*chain_base, "--audit-result", str(audit_path))
    assert stale_pack.returncode == 2

    fail_audit = run_cli(
        *chain_base,
        "--audit-result",
        str(FIXTURES / "valid-audit-fail.json"),
    )
    payload = json.loads(fail_audit.stdout)
    assert fail_audit.returncode == 2
    assert any("fail" in err for err in payload["errors"])


def test_audit_report_delivery_guard_blocks_delivered_on_fail(tmp_path):
    from audit_report import AuditVerdict, _apply_run_state_delivery_guard

    pack = _write_pack(
        tmp_path,
        "\n## Run state\n"
        "run_id: research-run-2026-08-25-001\n"
        "path: run-state.json\n",
    )
    state = load_valid("valid-delivered.json")
    state["current_artifact_sha256"] = vrs.sha256_file(pack)
    write_json(tmp_path / "run-state.json", state)
    verdict = AuditVerdict(route="constrained-choice", overall="fail", blocking=["x"])
    guarded = _apply_run_state_delivery_guard(verdict, pack)
    assert any("delivered" in item for item in guarded.blocking)


def test_from_to_delivered_without_audit_result_fails(tmp_path):
    auditing = mutate(
        load_valid("valid-collecting.json"),
        {
            "phase": "auditing",
            "handoff_refs": [
                {"handoff_id": "track-2026-08-24-competitors", "sha256": EMPTY_SHA}
            ],
            "last_transition_reason": "audits running",
        },
    )
    delivered = load_valid("valid-delivered.json")
    prev = write_json(tmp_path / "from.json", auditing)
    nxt = write_json(tmp_path / "to.json", delivered)
    proc = run_cli(
        "--from",
        str(prev),
        "--to",
        str(nxt),
        "--artifact",
        str(empty_artifact(tmp_path)),
        "--json",
    )
    payload = json.loads(proc.stdout)
    assert proc.returncode == 2
    assert any("audit-result" in err for err in payload["errors"])


def test_mid_review_pending_decision_cannot_carry_into_synthesizing():
    mid = load_valid("valid-mid-review.json")
    carried = mutate(
        load_valid("valid-collecting.json"),
        {
            "phase": "synthesizing",
            "pending_decision": "continue",
            "handoff_refs": [
                {"handoff_id": "track-2026-08-24-competitors", "sha256": EMPTY_SHA}
            ],
            "last_transition_reason": "search decision=continue",
        },
    )
    errors = vrs.validate_transition(mid, carried)
    assert errors
    assert any("pending_decision" in err and "consumed" in err for err in errors)

    consumed = mutate(carried, {"pending_decision": None})
    assert vrs.validate_transition(mid, consumed) == []


def test_empty_or_skipped_audit_cannot_support_delivered():
    delivered = load_valid("valid-delivered.json")
    empty = json.loads((FIXTURES / "valid-audit-pass.json").read_text())
    empty["audits"] = []
    errors = vrs.check_audit_result_for_delivered(empty, delivered)
    assert any("non-empty" in err for err in errors)

    skipped = json.loads((FIXTURES / "valid-audit-pass.json").read_text())
    skipped["audits"][0]["status"] = "skipped"
    errors = vrs.check_audit_result_for_delivered(skipped, delivered)
    assert any("skipped" in err for err in errors)


def test_foreign_artifact_hash_cannot_support_delivered(tmp_path):
    delivered = load_valid("valid-delivered.json")
    foreign = tmp_path / "other.md"
    foreign.write_text("another artifact", encoding="utf-8")
    foreign_sha = vrs.sha256_file(foreign)
    audit = json.loads((FIXTURES / "valid-audit-pass.json").read_text())
    audit["input_sha256"] = foreign_sha
    for rec in audit["audits"][0]["evidence_provenance"]:
        rec["input_sha256"] = foreign_sha
    errors = vrs.check_audit_result_for_delivered(
        audit,
        delivered,
        expected_report_sha256=EMPTY_SHA,
        expected_pack_sha256=EMPTY_SHA,
    )
    assert any("input_sha256" in err for err in errors)

    actual = empty_artifact(tmp_path, "pack.bin")
    report = empty_artifact(tmp_path, "report.md")
    proc = run_cli(
        str(FIXTURES / "valid-delivered.json"),
        "--audit-result",
        str(write_json(tmp_path / "foreign-audit.json", audit)),
        "--artifact",
        str(actual),
        "--report",
        str(report),
        "--json",
    )
    payload = json.loads(proc.stdout)
    assert proc.returncode == 2
    assert any("input_sha256" in err for err in payload["errors"])


def test_chain_requires_pack_run_state_section(tmp_path):
    pack = _write_pack(tmp_path)
    handoff = json.loads((HANDOFF_FIXTURES / "valid-complete.json").read_text())
    handoff["artifact_ref"] = {"artifact_id": "research-2026-08-25-001"}
    handoff_path = write_json(tmp_path / "handoff.json", handoff)
    state = load_valid("valid-collecting.json")
    state["current_artifact_sha256"] = vrs.sha256_file(pack)
    state_path = write_json(tmp_path / "run-state.json", state)
    proc = run_cli(
        "--chain",
        "--handoff",
        str(handoff_path),
        "--run-state",
        str(state_path),
        "--pack",
        str(pack),
        "--json",
    )
    payload = json.loads(proc.stdout)
    assert proc.returncode == 2
    assert any("## Run state" in err for err in payload["errors"])


def test_chain_rejects_mismatched_sidecar_identity(tmp_path):
    pack = _write_pack(
        tmp_path,
        "\n## Run state\n"
        "run_id: research-run-2026-08-25-001\n"
        "path: run-state.json\n",
    )
    declared = load_valid("valid-collecting.json")
    declared["current_artifact_sha256"] = vrs.sha256_file(pack)
    write_json(tmp_path / "run-state.json", declared)
    other = mutate(declared, {"run_id": "research-run-other-sidecar"})
    other_path = write_json(tmp_path / "other-state.json", other)
    handoff = json.loads((HANDOFF_FIXTURES / "valid-complete.json").read_text())
    handoff["artifact_ref"] = {"artifact_id": "research-2026-08-25-001"}
    handoff_path = write_json(tmp_path / "handoff.json", handoff)
    proc = run_cli(
        "--chain",
        "--handoff",
        str(handoff_path),
        "--run-state",
        str(other_path),
        "--pack",
        str(pack),
        "--json",
    )
    payload = json.loads(proc.stdout)
    assert proc.returncode == 2
    assert any("Pack-declared sidecar" in err for err in payload["errors"])


def test_explicit_resume_rejects_aligned_handoff_bind(tmp_path):
    state = load_valid("valid-explicit-resume.json")
    handoff = json.loads((HANDOFF_FIXTURES / "valid-complete.json").read_text())
    handoff["artifact_ref"] = {"artifact_id": state["artifact_id"]}
    errors = vrs.bind_handoff_to_run_state(handoff, state)
    assert errors
    assert any("explicit_resume" in err for err in errors)

    handoff_path = write_json(tmp_path / "handoff.json", handoff)
    state_path = write_json(tmp_path / "run-state.json", state)
    proc = run_handoff(str(handoff_path), "--run-state", str(state_path))
    assert proc.returncode == 2
    assert "explicit_resume" in proc.stdout


def test_delivered_keeps_report_and_pack_hashes_distinct(tmp_path):
    report, pack, audit_path = write_real_pass_audit(tmp_path)
    pack_sha = vrs.sha256_file(pack)
    report_sha = vrs.sha256_file(report)
    assert pack_sha != report_sha
    state = load_valid("valid-delivered.json")
    state["current_artifact_sha256"] = pack_sha
    state_path = write_json(tmp_path / "run-state.json", state)
    ok = run_cli(
        str(state_path),
        "--audit-result",
        str(audit_path),
        "--artifact",
        str(pack),
        "--report",
        str(report),
        "--json",
    )
    payload = json.loads(ok.stdout)
    assert ok.returncode == 0, ok.stdout + ok.stderr
    assert payload["ok"] is True

    forged = json.loads(audit_path.read_text(encoding="utf-8"))
    forged["input_sha256"] = pack_sha
    pack_as_report = run_cli(
        str(state_path),
        "--audit-result",
        str(write_json(tmp_path / "pack-as-report.json", forged)),
        "--artifact",
        str(pack),
        "--report",
        str(report),
        "--json",
    )
    payload = json.loads(pack_as_report.stdout)
    assert pack_as_report.returncode == 2
    assert any("input_sha256" in err or "report" in err for err in payload["errors"])


def test_incomplete_audit_set_cannot_support_delivered():
    delivered = load_valid("valid-delivered.json")
    audit = json.loads((FIXTURES / "valid-audit-pass.json").read_text())
    assert [item["audit_id"] for item in audit["audits"]] == ["final-audit"]
    errors = vrs.check_audit_result_for_delivered(
        audit,
        delivered,
        expected_report_sha256=EMPTY_SHA,
        expected_pack_sha256=EMPTY_SHA,
    )
    assert errors
    assert any("missing required audit" in err for err in errors)


def test_malformed_audit_entries_cannot_support_delivered():
    delivered = load_valid("valid-delivered.json")
    base = json.loads((FIXTURES / "valid-audit-pass.json").read_text())

    unknown = copy.deepcopy(base)
    unknown["audits"][0]["status"] = "looks-good"
    errors = vrs.check_audit_result_for_delivered(
        unknown, delivered, expected_report_sha256=EMPTY_SHA, expected_pack_sha256=EMPTY_SHA
    )
    assert errors
    assert any("status" in err for err in errors)

    missing_status = copy.deepcopy(base)
    del missing_status["audits"][0]["status"]
    errors = vrs.check_audit_result_for_delivered(
        missing_status,
        delivered,
        expected_report_sha256=EMPTY_SHA,
        expected_pack_sha256=EMPTY_SHA,
    )
    assert errors
    assert any("status" in err for err in errors)

    missing_id = copy.deepcopy(base)
    del missing_id["audits"][0]["audit_id"]
    errors = vrs.check_audit_result_for_delivered(
        missing_id,
        delivered,
        expected_report_sha256=EMPTY_SHA,
        expected_pack_sha256=EMPTY_SHA,
    )
    assert errors
    assert any("audit_id" in err for err in errors)

    missing_hash = copy.deepcopy(base)
    del missing_hash["audits"][0]["evidence_provenance"][0]["input_sha256"]
    errors = vrs.check_audit_result_for_delivered(
        missing_hash,
        delivered,
        expected_report_sha256=EMPTY_SHA,
        expected_pack_sha256=EMPTY_SHA,
    )
    assert errors
    assert any("input_sha256" in err for err in errors)

    conditional = copy.deepcopy(base)
    conditional["overall"] = "conditional-pass"
    conditional["exit_code"] = 1
    conditional["audits"][0]["status"] = "conditional-pass"
    conditional["audits"][0]["warnings"] = []
    errors = vrs.check_audit_result_for_delivered(
        conditional,
        delivered,
        expected_report_sha256=EMPTY_SHA,
        expected_pack_sha256=EMPTY_SHA,
    )
    assert errors
    assert any("warning" in err for err in errors)


def test_omitted_validators_cannot_support_delivered(tmp_path):
    report, pack, audit_path = write_real_pass_audit(tmp_path)
    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    assert isinstance(audit.get("validators"), list) and audit["validators"]
    del audit["validators"]
    stripped = write_json(tmp_path / "no-validators.json", audit)
    state = load_valid("valid-delivered.json")
    state["current_artifact_sha256"] = vrs.sha256_file(pack)
    state_path = write_json(tmp_path / "delivered.json", state)
    proc = run_cli(
        str(state_path),
        "--audit-result",
        str(stripped),
        "--artifact",
        str(pack),
        "--report",
        str(report),
        "--json",
    )
    payload = json.loads(proc.stdout)
    assert proc.returncode == 2
    assert payload["ok"] is False
    assert any("validators" in err for err in payload["errors"])


def test_omitted_audit_route_cannot_support_delivered(tmp_path):
    report, pack, audit_path = write_real_pass_audit(tmp_path)
    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    del audit["route"]
    stripped = write_json(tmp_path / "no-route.json", audit)
    state = load_valid("valid-delivered.json")
    state["current_artifact_sha256"] = vrs.sha256_file(pack)
    state_path = write_json(tmp_path / "delivered.json", state)
    proc = run_cli(
        str(state_path),
        "--audit-result",
        str(stripped),
        "--artifact",
        str(pack),
        "--report",
        str(report),
        "--json",
    )
    payload = json.loads(proc.stdout)
    assert proc.returncode == 2
    assert payload["ok"] is False
    assert any("route" in err for err in payload["errors"])


def test_chain_rejects_unverified_second_handoff_ref(tmp_path):
    report, pack, audit_path = write_real_pass_audit(
        tmp_path, with_run_state=True
    )
    handoff = json.loads((HANDOFF_FIXTURES / "valid-complete.json").read_text())
    handoff["artifact_ref"] = {"artifact_id": "fixture-market-outlook-pos"}
    handoff_path = write_json(tmp_path / "handoff.json", handoff)
    state = json.loads((tmp_path / "run-state.json").read_text(encoding="utf-8"))
    state["handoff_refs"] = [
        {
            "handoff_id": handoff["handoff_id"],
            "sha256": vrs.sha256_file(handoff_path),
        },
        {
            "handoff_id": "track-ghost-unverified",
            "sha256": EMPTY_SHA,
        },
    ]
    state_path = write_json(tmp_path / "run-state.json", state)
    proc = run_cli(
        "--chain",
        "--handoff",
        str(handoff_path),
        "--run-state",
        str(state_path),
        "--pack",
        str(pack),
        "--report",
        str(report),
        "--audit-result",
        str(audit_path),
        "--json",
    )
    payload = json.loads(proc.stdout)
    assert proc.returncode == 2
    assert payload["ok"] is False
    assert any(
        "track-ghost-unverified" in err or "not supplied" in err
        for err in payload["errors"]
    )


def test_chain_accepts_every_listed_handoff(tmp_path):
    report, pack, audit_path = write_real_pass_audit(
        tmp_path, with_run_state=True
    )
    first = json.loads((HANDOFF_FIXTURES / "valid-complete.json").read_text())
    first["artifact_ref"] = {"artifact_id": "fixture-market-outlook-pos"}
    first_path = write_json(tmp_path / "handoff-a.json", first)
    second = copy.deepcopy(first)
    second["handoff_id"] = "track-2026-08-24-customers"
    second_path = write_json(tmp_path / "handoff-b.json", second)
    state = json.loads((tmp_path / "run-state.json").read_text(encoding="utf-8"))
    state["handoff_refs"] = [
        {
            "handoff_id": first["handoff_id"],
            "sha256": vrs.sha256_file(first_path),
        },
        {
            "handoff_id": second["handoff_id"],
            "sha256": vrs.sha256_file(second_path),
        },
    ]
    state_path = write_json(tmp_path / "run-state.json", state)
    proc = run_cli(
        "--chain",
        "--handoff",
        str(first_path),
        "--handoff",
        str(second_path),
        "--run-state",
        str(state_path),
        "--pack",
        str(pack),
        "--report",
        str(report),
        "--audit-result",
        str(audit_path),
        "--json",
    )
    payload = json.loads(proc.stdout)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert payload["ok"] is True
    assert payload["errors"] == []
