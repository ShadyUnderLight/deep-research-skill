"""Issue #433 A2/A3: contract evidence must bind to visible report content,
and secondary hard-fail must match the exact derived audit id.

A2: ``validate_contract.py --require-contract`` (without ``--strict``) must
still resolve ``report-section`` / ``report-table`` locators against the
visible report body.  The standalone ``validate_contract()`` API keeps its
syntax-only semantics when no artifact text is supplied.

A3: a plain registry audit whose id merely contains a secondary route name
(e.g. ``regulatory-analysis-audit``) must not satisfy the
``<secondary>-secondary-hard-fail`` requirement.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from validate_contract import validate_contract  # noqa: E402

SCRIPT = str(SCRIPTS / "validate_contract.py")


def _contract(
    primary: str = "technical-deep-dive",
    audits: list[dict] | None = None,
    secondary_routes: list[str] | None = None,
) -> dict:
    return {
        "primary_route": primary,
        "secondary_routes": secondary_routes or [],
        "disciplines": [],
        "audits": audits
        or [
            {"id": "technical-analysis-audit", "status": "passed",
             "evidence": "report-section:Findings"},
            {"id": "source-traceability", "status": "passed",
             "evidence": "report-section:Findings"},
            {"id": "final-audit", "status": "passed",
             "evidence": "report-section:Executive summary"},
        ],
        "artifact_id": "issue433-contract-evidence",
        "contract_version": "1.0.0",
        "created_at": "2026-09-16",
    }


def _report(contract: dict, extra_sections: str = "") -> str:
    return (
        "# Issue 433 report\n\n"
        "## Executive summary\n\nBody text with citation [S01].\n\n"
        "## Findings\n\nBody text with citation [S01].\n\n"
        f"{extra_sections}"
        "```contract\n"
        + json.dumps(contract, ensure_ascii=False)
        + "\n```\n"
    )


def _write(tmp_path: Path, text: str) -> Path:
    path = tmp_path / "report.md"
    path.write_text(text, encoding="utf-8")
    return path


def _run_cli(path: Path, *extra: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, SCRIPT, str(path), "--require-contract", *extra],
        capture_output=True,
        text=True,
    )


# ── A2: visible evidence binding in the CLI ────────────────────────────────


def test_non_strict_cli_rejects_phantom_report_section(tmp_path: Path) -> None:
    contract = _contract()
    contract["audits"][1]["evidence"] = "report-section:Missing section"
    path = _write(tmp_path, _report(contract))
    result = _run_cli(path)
    assert result.returncode == 2, result.stdout + result.stderr
    assert "Missing section" in result.stdout


def test_non_strict_cli_rejects_phantom_report_table(tmp_path: Path) -> None:
    contract = _contract()
    contract["audits"][1]["evidence"] = "report-table:Missing table"
    path = _write(tmp_path, _report(contract))
    result = _run_cli(path)
    assert result.returncode == 2, result.stdout + result.stderr
    assert "Missing table" in result.stdout


def test_non_strict_cli_accepts_visible_locators(tmp_path: Path) -> None:
    path = _write(tmp_path, _report(_contract()))
    result = _run_cli(path)
    assert result.returncode == 0, result.stdout + result.stderr


def test_non_strict_cli_rejects_ambiguous_heading(tmp_path: Path) -> None:
    contract = _contract()
    contract["audits"][1]["evidence"] = "report-section:Repeated heading"
    report = _report(
        contract,
        extra_sections="## Repeated heading\n\nA.\n\n## Repeated heading\n\nB.\n\n",
    )
    path = _write(tmp_path, report)
    result = _run_cli(path)
    assert result.returncode == 2, result.stdout + result.stderr
    assert "Repeated heading" in result.stdout


def test_api_without_artifact_text_keeps_syntax_semantics() -> None:
    """The standalone API stays usable for callers that only hold the
    contract artifact (no report body): typed syntax is validated, locator
    existence is not."""
    contract = _contract()
    contract["audits"][1]["evidence"] = "report-section:Missing section"
    result = validate_contract(contract)
    assert result.is_valid, result.errors


def test_strict_cli_still_rejects_phantom_locator(tmp_path: Path) -> None:
    contract = _contract()
    contract["audits"][1]["evidence"] = "report-section:Missing section"
    path = _write(tmp_path, _report(contract))
    result = _run_cli(path, "--strict")
    assert result.returncode == 2, result.stdout + result.stderr


# ── A3: exact secondary hard-fail id ───────────────────────────────────────


def _secondary_audits() -> list[dict]:
    return [
        {"id": "technical-analysis-audit", "status": "passed",
         "evidence": "report-section:Findings"},
        {"id": "source-traceability", "status": "passed",
         "evidence": "report-section:Findings"},
        {"id": "final-audit", "status": "passed",
         "evidence": "report-section:Executive summary"},
        {"id": "regulatory-analysis-audit", "status": "passed",
         "evidence": "report-section:Findings"},
    ]


def test_registry_audit_does_not_satisfy_secondary_hard_fail() -> None:
    contract = _contract(
        secondary_routes=["regulatory-analysis"],
        audits=_secondary_audits(),
    )
    result = validate_contract(contract)
    assert not result.is_valid
    assert any(
        "regulatory-analysis" in error and "hard-fail" in error.lower()
        for error in result.errors
    ), result.errors


def test_non_strict_cli_rejects_substring_secondary_hard_fail(tmp_path: Path) -> None:
    contract = _contract(
        secondary_routes=["regulatory-analysis"],
        audits=_secondary_audits(),
    )
    path = _write(tmp_path, _report(contract))
    result = _run_cli(path)
    assert result.returncode == 2, result.stdout + result.stderr
    assert "regulatory-analysis-secondary-hard-fail" in result.stdout


def test_exact_derived_hard_fail_is_accepted(tmp_path: Path) -> None:
    audits = _secondary_audits() + [
        {"id": "regulatory-analysis-secondary-hard-fail", "status": "passed",
         "evidence": "report-section:Findings"},
    ]
    contract = _contract(
        secondary_routes=["regulatory-analysis"],
        audits=audits,
    )
    path = _write(tmp_path, _report(contract))
    result = _run_cli(path)
    assert result.returncode == 0, result.stdout + result.stderr


# ── A5: contract-check sub-check failures keep the canonical id ────────────


def test_activation_snapshot_failure_keeps_contract_check_binding(
    tmp_path: Path,
) -> None:
    """Issue #433 A5: a failing activation-snapshot sub-check inside
    ``_run_contract_check`` must be reported under the canonical
    ``contract-check`` validator id, not misattributed as an unexpected
    result name or downgraded to ``incomplete``."""
    path = _write(tmp_path, _report(_contract()))
    bad_snapshot = tmp_path / "bad-snapshot.json"
    bad_snapshot.write_text("{not json", encoding="utf-8")
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "audit_report.py"),
            str(path),
            "--activation-snapshot",
            str(bad_snapshot),
            "--json",
        ],
        capture_output=True,
        text=True,
    )
    data = json.loads(result.stdout)
    by_id = {v["validator_id"]: v for v in data["validators"]}
    assert by_id["contract-check"]["status"] == "fail", by_id["contract-check"]
    assert by_id["contract-check"]["errors"], by_id["contract-check"]
    assert all(
        v["status"] != "incomplete" for v in data["validators"]
    ), data["validators"]
