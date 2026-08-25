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
VALIDATE_CLI = [sys.executable, str(SCRIPTS / "validate_claim_alignment.py")]

if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from claim_alignment import (  # noqa: E402
    judge_entry,
    load_and_run_bundle,
    run_bundle,
    validate_bundle_structure,
)


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
            "subclaims": [],
        }
        judgment = judge_entry(entry)
        assert judgment.verdict == "PARTIAL"
        assert any("non-empty subclaim" in err for err in judgment.errors)

    def test_partial_fixture_has_decomposition(self) -> None:
        report = load_and_run_bundle(FIXTURES / "calibration-bundle.json")
        partial = next(j for j in report.judgments if j.claim_id == "C02")
        assert partial.verdict == "PARTIAL"
        assert len(partial.subclaims) == 2

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

    def test_claim_id_mismatch_is_structural_error(self) -> None:
        data = json.loads((FIXTURES / "source-id-mismatch.json").read_text())
        errors = validate_bundle_structure(data)
        assert any("claim_id" in err for err in errors)

    def test_route_mismatch_when_expected_route_given(self) -> None:
        data = json.loads((FIXTURES / "route-mismatch.json").read_text())
        errors = validate_bundle_structure(
            data,
            expected_route="technical-deep-dive",
        )
        assert any("route_id mismatch" in err for err in errors)


class TestAggregateVerdict:
    def test_not_run_does_not_aggregate_as_pass(self) -> None:
        data = {
            "schema_version": "1",
            "bundle_id": "only-not-run",
            "audited_population": "x",
            "sampling_rule": "x",
            "entries": [
                {
                    "claim_id": "N1",
                    "claim_text": "pending",
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
            ],
        }
        report = run_bundle(data)
        assert report.aggregate_verdict == "not_run"


class TestGoldIsolation:
    def test_judge_entry_never_reads_gold_labels(self) -> None:
        entry = json.loads((FIXTURES / "valid.json").read_text())["entries"][0]
        entry["gold_labels"] = {"verdict": "UNSUPPORTED"}
        judgment = judge_entry(entry)
        assert judgment.verdict == "SUPPORTED"
