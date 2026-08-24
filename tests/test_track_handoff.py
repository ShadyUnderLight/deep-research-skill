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


# ── Schema ↔ validator parity (review round 1, finding 4) ─────────────────


def test_schema_doc_nested_required_sets_match_validator():
    doc = json.loads(SCHEMA_DOC.read_text(encoding="utf-8"))
    props = doc["properties"]
    assert set(props["scope"]["required"]) == set(vth.SCOPE_REQUIRED)
    assert (
        set(props["source_register"]["items"]["required"]) == set(vth.SOURCE_REQUIRED)
    )
    assert set(props["findings"]["items"]["required"]) == set(vth.FINDING_REQUIRED)
    assert set(props["conflicts"]["items"]["required"]) == set(vth.CONFLICT_REQUIRED)
    assert set(props["unknowns"]["items"]["required"]) == set(vth.UNKNOWN_REQUIRED)


def test_schema_doc_declares_source_url_required():
    doc = json.loads(SCHEMA_DOC.read_text(encoding="utf-8"))
    source_items = doc["properties"]["source_register"]["items"]
    assert "url" in source_items["required"], (
        "SKILL.md requires explicit source URLs; the schema must not make "
        "url optional or url-less handoffs pass validation"
    )


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


# ── Fail-closed payload shapes (review round 1, findings 2/4/5) ───────────


def test_non_object_source_register_entry_fails_closed(valid_complete, tmp_path):
    """A schema-invalid register must never validate (fail-open regression)."""
    data = copy.deepcopy(valid_complete)
    data["source_register"].append("THIS SHOULD NEVER BE HERE")
    errors = vth.validate_handoff_data(data)
    assert any("source_register" in err and "object" in err.lower() for err in errors)

    proc = cli_validates(data, tmp_path)
    assert proc.returncode != 0


def test_non_object_finding_entry_fails_closed(valid_complete):
    data = copy.deepcopy(valid_complete)
    data["findings"].append("free-form prose masquerading as a finding")
    assert any(
        "finding" in err.lower() and "object" in err.lower()
        for err in vth.validate_handoff_data(data)
    )


def test_out_of_scope_empty_string_item_rejected(valid_complete):
    """Schema sets minLength 1 on out_of_scope items; runtime must match."""
    data = copy.deepcopy(valid_complete)
    data["scope"]["out_of_scope"] = [""]
    assert any("out_of_scope" in err for err in vth.validate_handoff_data(data))


def test_source_without_url_rejected():
    """Docs require explicit source URLs; url-less sources fail closed."""
    with open(FIXTURES / "valid-partial.json", encoding="utf-8") as fh:
        data = json.load(fh)
    data["source_register"][0].pop("url")
    errors = vth.validate_handoff_data(data)
    assert any("url" in err.lower() for err in errors)


# ── Consumer identity bindings (review round 1, finding 1) ────────────────


def test_expected_handoff_id_mismatch_fails(tmp_path):
    proc = cli_validates(load_valid("valid-complete.json"), tmp_path,
                         "--expected-handoff-id", "track-2099-01-01-other-run")
    assert proc.returncode == 2
    assert "HANDOFF_INCOMPLETE" in proc.stdout

    ok = cli_validates(load_valid("valid-complete.json"), tmp_path,
                       "--expected-handoff-id", "track-2026-08-24-competitors")
    assert ok.returncode == 0


def test_expected_question_mismatch_fails(tmp_path):
    stale = mutate(
        load_valid("valid-complete.json"),
        {"question": "Yesterday's different question about pricing tiers"},
    )
    # Same track_id, structurally valid — only the question binding catches it.
    assert vth.validate_handoff_data(stale) == []
    proc = cli_validates(stale, tmp_path,
                         "--expected-question",
                         "Who are the closest alternatives to Acme Analytics and how do they differ?")
    assert proc.returncode == 2

    ok = cli_validates(stale, tmp_path,
                       "--expected-question",
                       "Yesterday's different question about pricing tiers")
    assert ok.returncode == 0


def test_expected_artifact_id_requires_and_matches_artifact_ref(tmp_path):
    base = load_valid("valid-complete.json")  # no artifact_ref yet
    missing = cli_validates(base, tmp_path, "--expected-artifact-id", "artifact-001")
    assert missing.returncode == 2
    assert "artifact_ref" in missing.stdout

    bound = mutate(base, {"artifact_ref": {"artifact_id": "artifact-001"}})
    assert vth.validate_handoff_data(bound) == []
    ok = cli_validates(bound, tmp_path, "--expected-artifact-id", "artifact-001")
    assert ok.returncode == 0

    wrong = mutate(bound, {"artifact_ref": {"artifact_id": "artifact-002"}})
    bad = cli_validates(wrong, tmp_path, "--expected-artifact-id", "artifact-001")
    assert bad.returncode == 2


def test_loader_identity_bindings_fail_closed(valid_complete, tmp_path):
    path = write_tmp(tmp_path, valid_complete)
    with pytest.raises(vth.HandoffIncomplete):
        vth.load_handoff_for_merge(path, expected_question="unrelated question")
    payload = vth.load_handoff_for_merge(
        path,
        expected_question=valid_complete["question"],
        expected_handoff_id=valid_complete["handoff_id"],
    )
    assert payload["findings"]


# ── Field formats and enums ───────────────────────────────────────────────


def test_bad_generated_at_format_rejected(valid_complete):
    data = mutate(valid_complete, {"generated_at": "yesterday"})
    assert any("generated_at" in err for err in vth.validate_handoff_data(data))


@pytest.mark.parametrize(
    "bad_timestamp",
    [
        "2026-99-99",            # impossible month/day digits
        "2026-02-31",            # impossible calendar date
        "2026-13-01",            # impossible month
        "2026-08-24T99:88:77Z",  # impossible time digits
        "2026-08-24T09:30:00",   # naive datetime: RFC 3339 requires a zone
    ],
)
def test_impossible_or_naive_timestamps_rejected(valid_complete, bad_timestamp):
    data = mutate(valid_complete, {"generated_at": bad_timestamp})
    assert any(
        "generated_at" in err for err in vth.validate_handoff_data(data)
    ), f"{bad_timestamp!r} must be rejected"


@pytest.mark.parametrize(
    "good_timestamp",
    [
        "2026-08-24",
        "2026-08-24T09:30:00Z",
        "2026-08-24t09:30:00z",
        "2026-08-24T10:00:00+09:00",
        "2026-02-28T23:59:59Z",  # real calendar date, leap-year adjacent
    ],
)
def test_valid_timestamp_forms_accepted(valid_complete, good_timestamp):
    data = mutate(valid_complete, {"generated_at": good_timestamp})
    errors = [e for e in vth.validate_handoff_data(data) if "generated_at" in e]
    assert errors == [], f"{good_timestamp!r} must be accepted: {errors}"


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


# ── Single-track acceptance (issue #416) ──────────────────────────────────


def test_single_track_path_declares_no_handoff():
    """Acceptance: single-track research creates no handoff and keeps its
    current behavior. Nothing in the repo may wire handoff validation into
    the single-track path; the exemption must be documented and no eval case
    may require handoffs."""
    skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    assert "Single-track research creates no handoffs" in skill_text

    registry_text = (ROOT / "evals" / "registry.json").read_text(encoding="utf-8")
    assert "handoff" not in registry_text.lower(), (
        "no eval case may require a Track Handoff; the contract only binds "
        "the parallel path"
    )

    parallel_text = (ROOT / "references" / "parallel-research.md").read_text(
        encoding="utf-8"
    )
    assert "Single-track research does not create Track Handoffs" in parallel_text


# ── Fixtures ──────────────────────────────────────────────────────────────


@pytest.fixture
def valid_complete() -> dict:
    return load_valid("valid-complete.json")
