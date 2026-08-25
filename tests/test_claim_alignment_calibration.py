#!/usr/bin/env python3
"""Calibration tests for claim–source alignment gold set (issue #419)."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
FIXTURES = ROOT / "tests" / "fixtures" / "claim-alignment"
VALIDATE_CLI = [sys.executable, str(SCRIPTS / "validate_claim_alignment.py")]

if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from claim_alignment import run_calibration  # noqa: E402


class TestClaimAlignmentCalibration:
    def test_calibration_meets_threshold(self) -> None:
        result = run_calibration(
            FIXTURES / "calibration-bundle.json",
            FIXTURES / "calibration-gold.json",
            threshold=0.85,
        )
        assert result.aggregate_accuracy >= 0.85
        assert result.fixture_version == "claim-alignment-calibration-v1"
        assert result.positive_samples > 0
        assert result.negative_samples > 0
        supported = result.per_class["SUPPORTED"]
        assert supported["support"] == 1
        assert isinstance(supported["fpr"], float)

    def test_calibration_checks_partial_subclaims(self) -> None:
        result = run_calibration(
            FIXTURES / "calibration-bundle.json",
            FIXTURES / "calibration-gold.json",
        )
        assert not any("C02: subclaim" in m for m in result.mismatches)

    def test_calibration_cli_json(self) -> None:
        proc = subprocess.run(
            [
                *VALIDATE_CLI,
                str(FIXTURES / "calibration-bundle.json"),
                "--calibrate",
                str(FIXTURES / "calibration-gold.json"),
                "--json",
            ],
            capture_output=True,
            text=True,
        )
        assert proc.returncode == 0, proc.stdout + proc.stderr
        data = json.loads(proc.stdout)
        assert data["aggregate_accuracy"] >= 0.85
        assert data["per_class"]["SUPPORTED"]["fp"] == 0

    def test_bundle_with_embedded_gold_rejected(self) -> None:
        bundle = json.loads((FIXTURES / "calibration-bundle.json").read_text())
        bundle["gold_labels"] = {"C01": {"verdict": "SUPPORTED"}}
        import tempfile

        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tmp:
            json.dump(bundle, tmp)
            tmp_path = Path(tmp.name)
        try:
            try:
                run_calibration(tmp_path, FIXTURES / "calibration-gold.json")
                raised = False
            except ValueError:
                raised = True
            assert raised
        finally:
            tmp_path.unlink()

    def test_gold_keys_not_required_in_bundle(self) -> None:
        bundle_text = (FIXTURES / "calibration-bundle.json").read_text()
        assert "gold_labels" not in bundle_text

    def test_extra_gold_label_rejected(self) -> None:
        gold = json.loads((FIXTURES / "calibration-gold.json").read_text())
        gold["labels"]["NOT_IN_BUNDLE"] = {"verdict": "NOT_RUN"}
        import tempfile

        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tmp:
            json.dump(gold, tmp)
            tmp_path = Path(tmp.name)
        try:
            try:
                run_calibration(
                    FIXTURES / "calibration-bundle.json",
                    tmp_path,
                )
                raised = False
            except ValueError:
                raised = True
            assert raised
        finally:
            tmp_path.unlink()

    def test_bogus_gold_verdict_rejected(self) -> None:
        gold = json.loads((FIXTURES / "calibration-gold.json").read_text())
        gold["labels"]["C01"]["verdict"] = "BOGUS"
        import tempfile

        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tmp:
            json.dump(gold, tmp)
            tmp_path = Path(tmp.name)
        try:
            try:
                run_calibration(FIXTURES / "calibration-bundle.json", tmp_path)
                raised = False
            except ValueError:
                raised = True
            assert raised
        finally:
            tmp_path.unlink()

    def test_degenerate_all_not_run_gold_rejected(self) -> None:
        gold = json.loads((FIXTURES / "calibration-gold.json").read_text())
        for entry in gold["labels"].values():
            entry["verdict"] = "NOT_RUN"
            entry.pop("subclaims", None)
        import tempfile

        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tmp:
            json.dump(gold, tmp)
            tmp_path = Path(tmp.name)
        try:
            try:
                run_calibration(FIXTURES / "calibration-bundle.json", tmp_path)
                raised = False
            except ValueError:
                raised = True
            assert raised
        finally:
            tmp_path.unlink()

    def test_partial_gold_requires_subclaims(self) -> None:
        gold = json.loads((FIXTURES / "calibration-gold.json").read_text())
        gold["labels"]["C02"] = {"verdict": "PARTIAL"}
        import tempfile

        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tmp:
            json.dump(gold, tmp)
            tmp_path = Path(tmp.name)
        try:
            try:
                run_calibration(FIXTURES / "calibration-bundle.json", tmp_path)
                raised = False
            except ValueError:
                raised = True
            assert raised
        finally:
            tmp_path.unlink()

    def test_bundle_missing_fixture_version_rejected(self) -> None:
        bundle = json.loads((FIXTURES / "calibration-bundle.json").read_text())
        bundle.pop("fixture_version", None)
        import tempfile

        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tmp:
            json.dump(bundle, tmp)
            tmp_path = Path(tmp.name)
        try:
            try:
                run_calibration(tmp_path, FIXTURES / "calibration-gold.json")
                raised = False
            except ValueError:
                raised = True
            assert raised
        finally:
            tmp_path.unlink()
