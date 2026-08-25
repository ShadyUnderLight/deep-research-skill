#!/usr/bin/env python3
"""Tests for claim–source alignment validator (issue #419)."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
FIXTURES = ROOT / "tests" / "fixtures" / "claim-alignment"
AUDIT_FIXTURES = ROOT / "tests" / "fixtures" / "audit"
VALIDATE_CLI = [sys.executable, str(SCRIPTS / "validate_claim_alignment.py")]

if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from claim_alignment import (  # noqa: E402
    BindingContext,
    compute_per_class_one_vs_rest,
    judge_entry,
    load_and_run_bundle,
    run_bundle,
    validate_against_json_schema,
    validate_bundle_structure,
    EntryJudgment,
)

REPORT_PATH = AUDIT_FIXTURES / "market-outlook-pos.md"


def _run_cli(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [*VALIDATE_CLI, *args],
        capture_output=True,
        text=True,
    )


class TestValidateClaimAlignmentCli:
    def test_valid_supported_fixture_passes(self) -> None:
        result = _run_cli(str(FIXTURES / "valid.json"))
        assert result.returncode == 0, result.stdout + result.stderr

    def test_valid_supported_fixture_json(self) -> None:
        result = _run_cli(str(FIXTURES / "valid.json"), "--json")
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert data["aggregate_verdict"] == "pass"
        assert data["judgments"][0]["verdict"] == "SUPPORTED"


class TestSchemaConformance:
    def test_valid_fixture_matches_json_schema(self) -> None:
        data = json.loads((FIXTURES / "valid.json").read_text())
        errors = validate_against_json_schema(data)
        assert not errors, errors

    def test_calibration_bundle_matches_json_schema(self) -> None:
        data = json.loads((FIXTURES / "calibration-bundle.json").read_text())
        errors = validate_against_json_schema(data)
        assert not errors, errors

    def test_malformed_register_source_id_type_fails_schema(self) -> None:
        data = json.loads((FIXTURES / "valid.json").read_text())
        data["source_register"][0]["source_id"] = 123
        errors = validate_against_json_schema(data)
        assert errors
        struct_errors = validate_bundle_structure(data)
        assert any("source_id" in err for err in struct_errors)

    def test_unknown_source_id_with_empty_register_ids_fails(self) -> None:
        data = json.loads((FIXTURES / "valid.json").read_text())
        data["source_register"][0]["source_id"] = 123
        data["entries"][0]["evidence_record"]["source_id"] = "TOTALLY_FAKE"
        errors = validate_bundle_structure(data)
        assert any("not found in source_register" in err for err in errors)


class TestProductionBindingFailClosed:
    def test_missing_report_binding_fields_fail(self) -> None:
        data = json.loads((FIXTURES / "valid.json").read_text())
        data.pop("source_artifact_path")
        errors = validate_bundle_structure(
            data,
            binding=BindingContext(
                artifact_path=REPORT_PATH,
                expected_route="market-outlook",
                require_production_bindings=True,
            ),
        )
        assert any("source_artifact_path" in err for err in errors)

    def test_report_hash_mismatch_fails(self) -> None:
        data = json.loads((FIXTURES / "valid.json").read_text())
        data["source_artifact_sha256"] = "0000000000000000000000000000000000000000000000000000000000000000"
        errors = validate_bundle_structure(
            data,
            binding=BindingContext(
                artifact_path=REPORT_PATH,
                expected_route="market-outlook",
                require_production_bindings=True,
            ),
        )
        assert any("source_artifact_sha256 mismatch" in err for err in errors)

    def test_route_mismatch_fails_in_production_path(self) -> None:
        data = json.loads((FIXTURES / "route-mismatch.json").read_text())
        errors = validate_bundle_structure(
            data,
            binding=BindingContext(
                artifact_path=REPORT_PATH,
                expected_route="market-outlook",
                require_production_bindings=True,
            ),
        )
        assert any("route_id mismatch" in err for err in errors)

    def test_source_id_not_in_register_fails(self) -> None:
        data = json.loads((FIXTURES / "source-id-mismatch.json").read_text())
        errors = validate_bundle_structure(data)
        assert any("not found in source_register" in err for err in errors)

    def test_excerpt_not_from_source_artifact_fails(self) -> None:
        data = json.loads((FIXTURES / "excerpt-not-from-source.json").read_text())
        errors = validate_bundle_structure(data)
        assert any("excerpt not bound to source artifact" in err for err in errors)
        report = run_bundle(data)
        assert report.structural_errors
        assert report.aggregate_verdict == "fail"

    def test_claim_id_mismatch_fails(self) -> None:
        data = json.loads((FIXTURES / "claim-id-mismatch.json").read_text())
        errors = validate_bundle_structure(data)
        assert any("claim_id" in err for err in errors)

    def test_unbound_bundle_fails_against_report(self) -> None:
        bare = {
            "schema_version": "1",
            "bundle_id": "bare",
            "audited_population": "x",
            "sampling_rule": "x",
            "entries": json.loads((FIXTURES / "valid.json").read_text())["entries"],
        }
        errors = validate_bundle_structure(
            bare,
            binding=BindingContext(
                artifact_path=REPORT_PATH,
                expected_route="market-outlook",
                require_production_bindings=True,
            ),
        )
        assert any("production binding requires" in err for err in errors)


class TestVerdictSemantics:
    def test_retrieval_failed_not_upgraded_to_unsupported(self) -> None:
        report = load_and_run_bundle(FIXTURES / "calibration-bundle.json")
        by_id = {j.claim_id: j for j in report.judgments}
        assert by_id["C05"].verdict == "RETRIEVAL_FAILED"

    def test_not_run_stays_not_run(self) -> None:
        report = load_and_run_bundle(FIXTURES / "calibration-bundle.json")
        by_id = {j.claim_id: j for j in report.judgments}
        assert by_id["C06"].verdict == "NOT_RUN"

    def test_anchorless_locator_is_not_run(self) -> None:
        report = load_and_run_bundle(FIXTURES / "calibration-bundle.json")
        by_id = {j.claim_id: j for j in report.judgments}
        assert by_id["C07"].verdict == "NOT_RUN"

    def test_partial_requires_subclaim_decomposition(self) -> None:
        entry = {
            "claim_id": "PX",
            "claim_text": "A and B",
            "evidence_record": {
                "claim_id": "PX",
                "source_id": "S01",
                "locator": {"kind": "quote", "value": "A"},
                "retrieval_status": "fetched",
                "excerpt_hash": "sha256:112fb46a9479574d2a180970f5e456ce91c9dc3da9e76003dfc6853eaa7091df",
                "evidence_role": "primary",
            },
            "excerpt": "A only",
            "subclaim_candidates": [],
        }
        judgment = judge_entry(entry)
        assert judgment.verdict == "PARTIAL"
        assert any("non-empty subclaim" in err for err in judgment.errors)

    def test_partial_judges_subclaim_candidates_not_self_labels(self) -> None:
        report = load_and_run_bundle(FIXTURES / "calibration-bundle.json")
        partial = next(j for j in report.judgments if j.claim_id == "C02")
        assert partial.verdict == "PARTIAL"
        assert len(partial.subclaims) == 2
        assert partial.subclaims[0]["verdict"] == "UNSUPPORTED"
        assert partial.subclaims[1]["verdict"] == "SUPPORTED"

    def test_ambiguous_is_not_blocking_aggregate(self) -> None:
        data = json.loads((FIXTURES / "calibration-bundle.json").read_text())
        data["entries"] = [
            entry for entry in data["entries"] if entry["claim_id"] == "C04"
        ]
        report = run_bundle(data)
        assert report.judgments[0].verdict == "AMBIGUOUS"
        assert report.aggregate_verdict == "conditional-pass"

    def test_hash_mismatch_fail_closed(self) -> None:
        report = load_and_run_bundle(FIXTURES / "calibration-bundle.json")
        bad = next(j for j in report.judgments if j.claim_id == "C08")
        assert bad.verdict == "UNSUPPORTED"
        assert bad.errors

    def test_hidden_markdown_section_locator_fails(self) -> None:
        report = load_and_run_bundle(FIXTURES / "calibration-bundle.json")
        hidden = next(j for j in report.judgments if j.claim_id == "C09")
        assert hidden.verdict == "UNSUPPORTED"
        assert hidden.errors

    def test_quote_locator_does_not_short_circuit_contradictory_claim(self) -> None:
        data = json.loads((FIXTURES / "valid.json").read_text())
        entry = data["entries"][0]
        entry["claim_text"] = "Revenue collapsed 90% in FY2025"
        report = run_bundle(data)
        judgment = report.judgments[0]
        assert judgment.verdict != "SUPPORTED"
        assert judgment.verdict in {"UNSUPPORTED", "AMBIGUOUS"}


class TestAggregateVerdict:
    def test_not_run_does_not_aggregate_as_pass(self) -> None:
        data = json.loads((FIXTURES / "valid.json").read_text())
        data["entries"] = [
            {
                "claim_id": "N1",
                "claim_text": "pending verification",
                "evidence_record": {
                    "claim_id": "N1",
                    "source_id": "S01",
                    "locator": {"kind": "quote", "value": "pending"},
                    "retrieval_status": "not_run",
                    "excerpt_hash": "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
                    "evidence_role": "unknown",
                },
                "excerpt": "",
            }
        ]
        report = run_bundle(data)
        assert report.aggregate_verdict == "not_run"


class TestLocatorScopeBinding:
    def test_empty_quote_locator_fails_structurally(self) -> None:
        data = json.loads((FIXTURES / "valid.json").read_text())
        data["entries"][0]["evidence_record"]["locator"]["value"] = ""
        errors = validate_bundle_structure(data)
        assert any("locator.value required" in err for err in errors)

    def test_empty_quote_locator_does_not_support(self) -> None:
        data = json.loads((FIXTURES / "valid.json").read_text())
        data["entries"][0]["evidence_record"]["locator"]["value"] = ""
        report = run_bundle(data)
        assert report.structural_errors
        judgment = report.judgments[0] if report.judgments else None
        if judgment is not None:
            assert judgment.verdict != "SUPPORTED"

    def test_wrong_section_excerpt_not_in_locator_scope(self) -> None:
        report = load_and_run_bundle(FIXTURES / "wrong-section-locator.json")
        assert report.judgments[0].verdict == "UNSUPPORTED"
        assert any("locator scope" in err for err in report.judgments[0].errors)

    def test_bogus_paragraph_locator_is_not_run(self) -> None:
        data = json.loads((FIXTURES / "calibration-bundle.json").read_text())
        entry = next(e for e in data["entries"] if e["claim_id"] == "C02")
        entry["evidence_record"]["locator"] = {
            "kind": "paragraph",
            "value": "THIS_PARAGRAPH_DOES_NOT_EXIST",
        }
        report = run_bundle(data)
        c02 = next(j for j in report.judgments if j.claim_id == "C02")
        assert c02.verdict == "NOT_RUN"
        assert any("paragraph" in w for w in c02.warnings)

    def test_bogus_page_locator_is_not_run(self) -> None:
        data = json.loads((FIXTURES / "valid.json").read_text())
        data["entries"][0]["evidence_record"]["locator"] = {
            "kind": "page",
            "value": "banana",
        }
        report = run_bundle(data)
        assert report.judgments[0].verdict == "NOT_RUN"
        assert report.judgments[0].verdict != "SUPPORTED"


class TestLexicalJudgeAndProductionBundle:
    def test_production_bundle_rejects_embedded_gold_labels(self) -> None:
        data = json.loads((FIXTURES / "valid.json").read_text())
        data["gold_labels"] = {"C01": {"verdict": "UNSUPPORTED"}}
        errors = validate_bundle_structure(data)
        assert any("gold_labels" in err for err in errors)
        report = run_bundle(data)
        assert report.structural_errors

    def test_direction_conflict_not_supported(self) -> None:
        data = json.loads((FIXTURES / "valid.json").read_text())
        data["entries"][0]["claim_text"] = "Revenue declined 15% in FY2025"
        report = run_bundle(data)
        assert report.judgments[0].verdict == "UNSUPPORTED"

    def test_negation_conflict_not_supported(self) -> None:
        data = json.loads((FIXTURES / "valid.json").read_text())
        data["entries"][0]["claim_text"] = (
            "Revenue did not increase compared to the prior fiscal year"
        )
        report = run_bundle(data)
        assert report.judgments[0].verdict == "UNSUPPORTED"

    def test_numeric_percent_conflict_not_supported(self) -> None:
        data = json.loads((FIXTURES / "valid.json").read_text())
        data["entries"][0]["claim_text"] = "Revenue increased 50% in FY2025"
        report = run_bundle(data)
        assert report.judgments[0].verdict == "UNSUPPORTED"

    def test_cjk_negation_conflict_not_supported(self) -> None:
        import hashlib

        data = json.loads((FIXTURES / "valid.json").read_text())
        src = ROOT / "tests/fixtures/claim-alignment/sources/cjk-growth-source.txt"
        excerpt = "收入增长"
        data["source_register"] = [
            {
                "source_id": "S01",
                "source_artifact_path": (
                    "tests/fixtures/claim-alignment/sources/cjk-growth-source.txt"
                ),
                "source_artifact_sha256": hashlib.sha256(src.read_bytes()).hexdigest(),
            }
        ]
        data["entries"][0]["claim_text"] = "收入没有增长"
        data["entries"][0]["claim_id"] = "CJK1"
        data["entries"][0]["evidence_record"]["claim_id"] = "CJK1"
        data["entries"][0]["evidence_record"]["locator"] = {
            "kind": "quote",
            "value": "收入增长",
        }
        data["entries"][0]["excerpt"] = excerpt
        data["entries"][0]["evidence_record"]["excerpt_hash"] = (
            f"sha256:{hashlib.sha256(excerpt.encode()).hexdigest()}"
        )
        report = run_bundle(data)
        assert report.judgments[0].verdict == "UNSUPPORTED"

    def test_year_mismatch_not_supported(self) -> None:
        import hashlib

        data = json.loads((FIXTURES / "valid.json").read_text())
        src = ROOT / "tests/fixtures/claim-alignment/sources/year-mismatch-source.txt"
        data["source_register"] = [
            {
                "source_id": "S01",
                "source_artifact_path": (
                    "tests/fixtures/claim-alignment/sources/year-mismatch-source.txt"
                ),
                "source_artifact_sha256": hashlib.sha256(src.read_bytes()).hexdigest(),
            }
        ]
        excerpt = "Revenue grew 15% in FY2025."
        data["entries"][0]["claim_text"] = "Revenue grew 15% in FY2024"
        data["entries"][0]["excerpt"] = excerpt
        data["entries"][0]["evidence_record"]["excerpt_hash"] = (
            f"sha256:{hashlib.sha256(excerpt.encode()).hexdigest()}"
        )
        report = run_bundle(data)
        assert report.judgments[0].verdict == "UNSUPPORTED"

    def test_hidden_quote_in_fence_not_supported(self) -> None:
        import hashlib

        data = json.loads((FIXTURES / "valid.json").read_text())
        src = ROOT / "tests/fixtures/claim-alignment/sources/hidden-quote-source.txt"
        data["source_register"] = [
            {
                "source_id": "S01",
                "source_artifact_path": (
                    "tests/fixtures/claim-alignment/sources/hidden-quote-source.txt"
                ),
                "source_artifact_sha256": hashlib.sha256(src.read_bytes()).hexdigest(),
            }
        ]
        excerpt = "revenue increased 15%"
        data["entries"][0]["excerpt"] = excerpt
        data["entries"][0]["evidence_record"]["excerpt_hash"] = (
            f"sha256:{hashlib.sha256(excerpt.encode()).hexdigest()}"
        )
        report = run_bundle(data)
        assert report.judgments[0].verdict == "UNSUPPORTED"

    def test_judge_entry_never_reads_gold_labels(self) -> None:
        entry = json.loads((FIXTURES / "valid.json").read_text())["entries"][0]
        entry["gold_labels"] = {"verdict": "UNSUPPORTED"}
        judgment = judge_entry(entry)
        assert judgment.verdict == "SUPPORTED"


class TestPerClassMetrics:
    def test_supported_fpr_counts_misclassification(self) -> None:
        labels = {
            "X1": {"verdict": "UNSUPPORTED"},
        }
        predicted = {
            "X1": EntryJudgment(claim_id="X1", verdict="SUPPORTED"),
        }
        per_class = compute_per_class_one_vs_rest(labels, predicted)
        assert per_class["SUPPORTED"]["fp"] == 1
        assert per_class["SUPPORTED"]["fpr"] == 1.0
        assert per_class["UNSUPPORTED"]["fn"] == 1
