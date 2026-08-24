"""Contract tests for the parallel-research Track Handoff contract (issue #416).

Covers:
1. Canonical schema doc exists and stays in sync with the validator.
2. Valid complete / partial / blocked fixtures pass.
3. Fail-closed negatives required by the issue acceptance checklist:
   missing required fields, dangling evidence refs, duplicate ids,
   unknown status, bad timestamps, unbound conflict refs,
   partial/blocked without reason or recovery action.
4. Command-level consumer behavior: the CLI rejects schema-invalid handoffs
   and a consumer loader raises instead of merging empty findings.
5. A mixed-defect handoff is rejected even when some fields are correct.
"""
import json
import copy
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
FIXTURES = ROOT / "tests" / "fixtures" / "track-handoff"
SCHEMA_DOC = ROOT / "schemas" / "track-handoff.json"

sys.path.insert(0, str(SCRIPTS))

import validate_track_handoff as vth  # noqa: E402


# ── Helpers ───────────────────────────────────────────────────────────────


def load_valid(name: str) -> dict:
    with open(FIXTURES / name, encoding="utf-8") as fh:
        return json.load(fh)


def mutate(base: dict, overlay: dict | None = None, drop: list[str] | None = None) -> dict:
    """Return a deep copy of *base* with keys added/overwritten and/or removed."""
    data = copy.deepcopy(base)
    if overlay:
        data.update(overlay)
    for key in drop or []:
        data.pop(key, None)
    return data


def write_tmp(tmp_path: Path, data: dict) -> Path:
    path = tmp_path / "handoff.json"
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return path


def run_cli(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPTS / "validate_track_handoff.py"), *args],
        capture_output=True,
        text=True,
    )


def cli_validates(data: dict, tmp_path: Path, *extra: str) -> subprocess.CompletedProcess:
    return run_cli(str(write_tmp(tmp_path, data)), *extra)


# ── Schema doc structural sync ────────────────────────────────────────────


def test_schema_doc_exists_with_version_1():
    assert SCHEMA_DOC.exists(), f"{SCHEMA_DOC} does not exist"
    doc = json.loads(SCHEMA_DOC.read_text(encoding="utf-8"))
    assert doc.get("version") == 1
    assert doc.get("schema_version") == "1"


def test_schema_doc_required_fields_match_validator():
    doc = json.loads(SCHEMA_DOC.read_text(encoding="utf-8"))
    assert set(doc["required"]) == set(vth.REQUIRED_TOP_LEVEL)


def test_validator_enforces_declared_status_enum():
    doc = json.loads(SCHEMA_DOC.read_text(encoding="utf-8"))
    assert sorted(doc["properties"]["status"]["enum"]) == sorted(vth.ALLOWED_STATUS)


# ── Valid fixtures pass ───────────────────────────────────────────────────


@pytest.mark.parametrize(
    "fixture_name",
    ["valid-complete.json", "valid-partial.json", "valid-blocked.json"],
)
def test_valid_fixtures_pass(fixture_name):
    errors = vth.validate_handoff_data(load_valid(fixture_name))
    assert errors == [], f"{fixture_name} unexpectedly invalid: {errors}"


def test_valid_complete_passes_cli(tmp_path):
    proc = run_cli(str(FIXTURES / "valid-complete.json"))
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_valid_blocked_passes_cli(tmp_path):
    proc = run_cli(str(FIXTURES / "valid-blocked.json"))
    assert proc.returncode == 0, proc.stdout + proc.stderr


# ── Missing required top-level fields fail closed ─────────────────────────


@pytest.mark.parametrize("field", sorted(vth.REQUIRED_TOP_LEVEL))
def test_missing_required_top_level_field_fails_closed(valid_complete, tmp_path, field):
    data = mutate(valid_complete, drop=[field])
    errors = vth.validate_handoff_data(data)
    assert any(field in err for err in errors), f"missing {field!r} not reported: {errors}"

    proc = cli_validates(data, tmp_path)
    assert proc.returncode != 0
    assert vth.HANDOFF_INCOMPLETE in proc.stdout + proc.stderr


# ── Status semantics ──────────────────────────────────────────────────────


def test_complete_with_empty_findings_fails(valid_complete):
    data = mutate(valid_complete, {"findings": []})
    assert any("findings" in err for err in vth.validate_handoff_data(data))


def test_partial_requires_reason(tmp_path):
    data = mutate(load_valid("valid-partial.json"), drop=["status_reason"])
    assert any("status_reason" in err for err in vth.validate_handoff_data(data))
    empty_reason = mutate(data, {"status_reason": "   "})
    assert any("status_reason" in err for err in vth.validate_handoff_data(empty_reason))


def test_blocked_requires_reason_and_recovery_action():
    base = load_valid("valid-blocked.json")
    no_recovery = mutate(base, drop=["recovery_action"])
    errs = vth.validate_handoff_data(no_recovery)
    assert any("recovery_action" in err for err in errs)

    empty_recovery = mutate(base, {"recovery_action": ""})
    assert any("recovery_action" in err for err in vth.validate_handoff_data(empty_recovery))


def test_unknown_status_rejected(valid_complete):
    data = mutate(valid_complete, {"status": "done"})
    assert any("status" in err for err in vth.validate_handoff_data(data))


# ── Referential integrity ─────────────────────────────────────────────────


def test_dangling_evidence_ref_fails(valid_complete):
    data = copy.deepcopy(valid_complete)
    data["findings"][0]["evidence_refs"] = ["S99"]
    assert any("S99" in err for err in vth.validate_handoff_data(data))


def test_empty_evidence_refs_on_finding_fails(valid_complete):
    data = copy.deepcopy(valid_complete)
    data["findings"][0]["evidence_refs"] = []
    assert any("evidence_refs" in err for err in vth.validate_handoff_data(data))


def test_duplicate_finding_id_fails(valid_complete):
    data = copy.deepcopy(valid_complete)
    data["findings"][1]["finding_id"] = data["findings"][0]["finding_id"]
    assert any("duplicate" in err.lower() for err in vth.validate_handoff_data(data))


def test_duplicate_source_id_fails(valid_complete):
    data = copy.deepcopy(valid_complete)
    data["source_register"][1]["source_id"] = data["source_register"][0]["source_id"]
    assert any("duplicate" in err.lower() for err in vth.validate_handoff_data(data))


def test_conflict_unbound_finding_ref_fails(valid_complete):
    data = copy.deepcopy(valid_complete)
    data["conflicts"][0]["finding_refs"] = ["F01", "F404"]
    assert any("F404" in err for err in vth.validate_handoff_data(data))


def test_resolved_conflict_requires_note(valid_complete):
    data = copy.deepcopy(valid_complete)
    data["conflicts"][0]["resolution_status"] = "resolved"
    data["conflicts"][0].pop("resolution_note")
    assert any("resolution_note" in err for err in vth.validate_handoff_data(data))


# ── Field formats and enums ───────────────────────────────────────────────


def test_bad_generated_at_format_rejected(valid_complete):
    data = mutate(valid_complete, {"generated_at": "yesterday"})
    assert any("generated_at" in err for err in vth.validate_handoff_data(data))


def test_bad_confidence_rejected(valid_complete):
    over = copy.deepcopy(valid_complete)
    over["findings"][0]["confidence"] = 1.5
    non_numeric = copy.deepcopy(valid_complete)
    non_numeric["findings"][0]["confidence"] = "high"
    assert any("confidence" in err for err in vth.validate_handoff_data(over))
    assert any("confidence" in err for err in vth.validate_handoff_data(non_numeric))


def test_unknown_evidence_role_rejected(valid_complete):
    data = copy.deepcopy(valid_complete)
    data["findings"][0]["evidence_role"] = "verified"
    assert any("evidence_role" in err for err in vth.validate_handoff_data(data))


def test_wrong_schema_version_rejected(valid_complete):
    data = mutate(valid_complete, {"schema_version": "2"})
    assert any("schema_version" in err for err in vth.validate_handoff_data(data))


def test_unknown_top_level_property_rejected(valid_complete):
    data = mutate(valid_complete, {"extra_polished_report": "looks like markdown"})
    assert any("additional" in err.lower() or "unknown" in err.lower()
               for err in vth.validate_handoff_data(data))


def test_unknown_scope_property_rejected(valid_complete):
    data = copy.deepcopy(valid_complete)
    data["scope"]["population"] = "mid-market SaaS teams"
    assert vth.validate_handoff_data(data) != []


# ── Consumer fail-closed semantics ────────────────────────────────────────


def test_consumer_loader_raises_on_invalid_instead_of_merging_empty(valid_complete, tmp_path):
    data = mutate(valid_complete, drop=["source_register"])
    path = write_tmp(tmp_path, data)
    with pytest.raises(vth.HandoffIncomplete) as excinfo:
        vth.load_handoff_for_merge(path)
    assert "source_register" in str(excinfo.value)


def test_consumer_loader_returns_payload_when_valid():
    payload = vth.load_handoff_for_merge(FIXTURES / "valid-complete.json")
    assert payload["track_id"] == "track-competitors"
    assert payload["findings"], "valid handoff must keep its findings"


def test_cli_reports_handoff_incomplete_and_nonzero_exit(valid_complete, tmp_path):
    data = mutate(valid_complete, drop=["status"])
    proc = cli_validates(data, tmp_path)
    assert proc.returncode == 2
    assert vth.HANDOFF_INCOMPLETE in proc.stdout
    # The refusal must not be interpretable as an empty-but-valid merge result.
    assert "0 findings" not in proc.stdout.split("HANDOFF_INCOMPLETE")[-1]


def test_expected_track_id_mismatch_fails(valid_complete, tmp_path):
    proc = cli_validates(valid_complete, tmp_path, "--expected-track-id", "track-other")
    assert proc.returncode == 2
    assert "track-other" in proc.stdout or "track-other" in proc.stderr

    ok = cli_validates(
        valid_complete, tmp_path, "--expected-track-id", "track-competitors"
    )
    assert ok.returncode == 0


def test_missing_file_fails_closed(tmp_path):
    proc = run_cli(str(tmp_path / "does-not-exist.json"))
    assert proc.returncode == 2
    assert vth.HANDOFF_INCOMPLETE in proc.stdout


def test_combined_defects_not_masked_by_correct_fields(valid_complete):
    """One correct field must not launder other illegal ones (issue #416)."""
    data = mutate(
        valid_complete,
        {
            "status": "done",                      # unknown status
            "schema_version": "9",                 # tampered version
        },
        drop=["scope"],                            # missing scope
    )
    data["findings"][0]["evidence_refs"] = ["S01", "GHOST"]   # dangling ref
    data["source_register"].append(dict(data["source_register"][0]))  # dup id

    errors = vth.validate_handoff_data(data)
    joined = "\n".join(errors)
    assert "status" in joined
    assert "schema_version" in joined
    assert "scope" in joined
    assert "GHOST" in joined
    assert any("duplicate" in err.lower() for err in errors)


# ── Fixtures ──────────────────────────────────────────────────────────────


@pytest.fixture
def valid_complete() -> dict:
    return load_valid("valid-complete.json")
