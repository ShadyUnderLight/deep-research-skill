#!/usr/bin/env python3
"""
Tests for issue #378 — required-audit execution and fail-closed semantics.

Verifies that:
1. Every route's required_audits resolve to a registry binding; automated
   audits without a binding fail closed.
2. Required automated audits actually run and appear in structured results.
3. Manual/process audits not run in the report are recorded as ``not_run``
   and cannot aggregate to Pass (blocking in strict mode, warning otherwise).
4. Strict mode fails when route / contract / pack declarations are missing —
   no silent fallback to technical-deep-dive.
5. ``--json`` emits a machine-readable verdict with audit id, status,
   evidence, validator version and input artifact hash.
6. Markdown delivery, Research Pack (when provided) and route-specific
   audits run in a single command.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

SCRIPT = str(SCRIPTS_DIR / "audit_report.py")

# Contract template that satisfies all validate_contract rules (issue #376):
# every primary-route required audit declared, passed with non-empty
# evidence, plus stable artifact identity fields.
CONTRACT_TEMPLATE = {
    "primary_route": "market-outlook",
    "secondary_routes": [],
    "disciplines": [],
    "audits": [
        {"id": "market-outlook-audit", "status": "passed", "evidence": "§3"},
        {"id": "forward-looking-claims", "status": "passed", "evidence": "§4"},
        {"id": "source-traceability", "status": "passed", "evidence": "§5"},
        {"id": "final-audit", "status": "passed", "evidence": "§2"},
    ],
    "artifact_id": "fixture-market-outlook-pos",
    "contract_version": "1.0.0",
    "created_at": "2026-08-13",
}


def _contract(primary: str = "market-outlook", **overrides) -> str:
    data = json.dumps(CONTRACT_TEMPLATE, ensure_ascii=False)
    if primary != "market-outlook":
        data = json.dumps(
            {**CONTRACT_TEMPLATE, "primary_route": primary}, ensure_ascii=False
        )
    data = json.dumps(
        {**json.loads(data), **overrides}, ensure_ascii=False
    )
    return data


def _route_block(primary: str) -> str:
    """Route and audit status block declaring the primary route and audits."""
    audits = {
        "market-outlook": [
            ("market-outlook-audit", "§3"),
            ("forward-looking-claims", "§4"),
            ("source-traceability", "§5"),
            ("final-audit", "§2"),
            # quantitative-role-audit keeps the table role-annotated
            # (table-role-labels: 3+ row tables need a role keyword).
            ("quantitative-role-audit", "§6"),
        ],
        "technical-deep-dive": [
            ("technical-analysis-audit", "§4"),
            ("source-traceability", "§5"),
            ("final-audit", "§2"),
            ("quantitative-role-audit", "§6"),
        ],
        "shared-workflow": [
            ("workflow-spine-audit", "§3"),
            ("final-audit", "§2"),
            ("quantitative-role-audit", "§6"),
        ],
    }
    rows = audits.get(primary, audits["market-outlook"])
    body = "".join(
        f"| {aid} | ✅ Passed | {evidence} |\n" for aid, evidence in rows
    )
    display = {
        "market-outlook": "Market Outlook",
        "technical-deep-dive": "Technical Deep-dive",
        "shared-workflow": "Shared-workflow",
    }[primary]
    return (
        "## Route and audit status\n\n"
        f"**Primary route**: {display}\n\n"
        "| Audit | Status | 证据 |\n"
        "|-------|--------|------|\n" + body
    )


def _monitoring_section() -> str:
    """Monitoring section with 3 fully-defined signals (market-outlook)."""
    return """\
## Monitoring signals

| Signal | Threshold | Cadence | Source | Trigger-to-action | 数字角色 |
|--------|-----------|---------|--------|-------------------|---------|
| Signal A | ≥2.0 | monthly | [S01] | rebalance | observed |
| Signal B | ≤1.5 | weekly | [S02] | hedge | observed |
| Signal C | ≥10% | quarterly | [S03] | reallocate | observed |
"""


def _source_register() -> str:
    return """\
## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Example A | secondary | 2026-01-01 | https://example.com/a | medium | §3 |
| S02 | Example B | secondary | 2026-02-01 | https://example.com/b | high | §5 |
| S03 | Example C | secondary | 2026-03-01 | https://example.com/c | high | §4 |
"""


def _report(
    primary: str = "market-outlook",
    contract: str | None = None,
    include_monitoring: bool = True,
    route_block: str | None = None,
) -> str:
    """Build a report that passes all generic validators."""
    parts = [
        "# Test Report\n",
        route_block or _route_block(primary),
        "\n## Executive summary\n\n"
        "**核心判断**：the market will grow, backed by [S01].\n\n"
        "- Key bullet one\n"
        "- Key bullet two\n",
        "\n## Findings\n\nBody text with citations [S01], [S02], [S03].\n",
        "\n## Comparison Table\n\n"
        "| Metric | System A | System B | 数字角色 |\n"
        "|--------|----------|----------|---------|\n"
        "| Cost | 100 | 80 | observed |\n"
        "| Speed | 200 | 150 | observed |\n",
        "\n## Dimension conclusions\n\nBacked by [S01] and [S02].\n",
    ]
    if include_monitoring:
        parts.append("\n" + _monitoring_section())
    parts.append("\n" + _source_register())
    if contract is not None:
        parts.append(f"\n```contract\n{contract}\n```\n")
    return "".join(parts)


def _write(text: str) -> Path:
    f = tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", delete=False, encoding="utf-8"
    )
    f.write(text)
    f.close()
    return Path(f.name)


def _run_audit(
    path: Path,
    extra_args: list[str] | None = None,
    research_pack: Path | None = None,
) -> subprocess.CompletedProcess:
    args = [sys.executable, SCRIPT, str(path)]
    if research_pack is not None:
        args += ["--research-pack", str(research_pack)]
    args += extra_args or []
    return subprocess.run(args, capture_output=True, text=True)


class TestRequiredAuditExecution:
    """Required audits must actually execute and appear in results."""

    def test_required_automated_audits_executed(self) -> None:
        """forward-looking-claims (automated) must run for market-outlook."""
        report = _report(contract=_contract())
        path = _write(report)
        result = _run_audit(path, extra_args=["--json"])
        data = json.loads(result.stdout)
        audit_ids = {a["audit_id"] for a in data["audits"]}
        assert "forward-looking-claims" in audit_ids
        assert "source-traceability" in audit_ids
        assert "market-outlook-audit" in audit_ids  # manual, declared
        assert "markdown-delivery" in audit_ids  # global automated

    def test_forward_looking_failure_is_blocking(self) -> None:
        """A forward-looking numeric claim mislabeled as confirmed must fail."""
        report = _report(contract=_contract())
        report += (
            "\n## Outlook\n\n"
            "[Confirmed] Shipments will reach 100 units by 2027.\n"
        )
        path = _write(report)
        result = _run_audit(path)
        assert result.returncode == 2, result.stdout
        assert "forward-looking" in result.stdout.lower()


class TestManualAuditStatus:
    """Manual/process audits must have explicit not_run/skipped semantics."""

    def _report_missing_declaration(self) -> Path:
        block = (
            "## Route and audit status\n\n"
            "**Primary route**: Market Outlook\n\n"
            "| Audit | Status | 证据 |\n"
            "|-------|--------|------|\n"
            "| final-audit | ✅ Passed | §2 |\n"
        )
        return _write(_report(route_block=block, contract=_contract()))

    def _report_with_status(self, status_cell: str) -> Path:
        block = (
            "## Route and audit status\n\n"
            "**Primary route**: Market Outlook\n\n"
            "| Audit | Status | 证据 |\n"
            "|-------|--------|------|\n"
            f"| market-outlook-audit | {status_cell} | §3 |\n"
            "| forward-looking-claims | ✅ Passed | §4 |\n"
            "| source-traceability | ✅ Passed | §5 |\n"
            "| final-audit | ✅ Passed | §2 |\n"
            "| quantitative-role-audit | ✅ Passed | §6 |\n"
        )
        return _write(_report(route_block=block, contract=_contract()))

    def test_negative_status_not_parsed_as_pass(self) -> None:
        """'❌ Not passed' must not match the 'passed' substring (fail closed)."""
        path = self._report_with_status("❌ Not passed")
        result = _run_audit(path, extra_args=["--strict", "--require-contract", "--json"])
        data = json.loads(result.stdout)
        mo = next(
            a for a in data["audits"] if a["audit_id"] == "market-outlook-audit"
        )
        assert mo["status"] == "not_run", mo
        assert data["exit_code"] == 2, data["blocking"]

    def test_explicit_fail_status_is_not_pass(self) -> None:
        path = self._report_with_status("✗ Fail")
        result = _run_audit(path, extra_args=["--strict", "--require-contract", "--json"])
        data = json.loads(result.stdout)
        mo = next(
            a for a in data["audits"] if a["audit_id"] == "market-outlook-audit"
        )
        assert mo["status"] == "not_run", mo

    def test_passed_status_is_pass(self) -> None:
        path = self._report_with_status("✅ Passed")
        result = _run_audit(path, extra_args=["--strict", "--require-contract", "--json"])
        data = json.loads(result.stdout)
        mo = next(
            a for a in data["audits"] if a["audit_id"] == "market-outlook-audit"
        )
        assert mo["status"] == "pass", mo

    # Fail-open variants: the positive branch must only match canonical
    # status tokens at word boundaries, never 'pass'/'passed' substrings
    # inside negative or unknown wording.
    @pytest.mark.parametrize("cell", [
        "❌ Not passed",
        "✗ Fail",
        "not_passed",
        "did not pass",
        "unpassed",
        "not passing",
        "not-passed",
        "未通过",
        "pending",
        "in progress",
        "blocked",
        "unknown status",
        # Whole-cell canonical-token variants: a bare 'pass'/'passed'
        # substring anywhere in the cell must NOT count as pass.
        "passed-ish",
        "passed with caveats",
        "conditional-pass",
        "Status: Pass",
        "pass (manual)",
        "Passed ✅ with caveats",
    ])
    def test_negative_or_unknown_status_is_not_pass(self, cell: str) -> None:
        path = self._report_with_status(cell)
        result = _run_audit(path, extra_args=["--strict", "--require-contract", "--json"])
        data = json.loads(result.stdout)
        mo = next(
            a for a in data["audits"] if a["audit_id"] == "market-outlook-audit"
        )
        assert mo["status"] == "not_run", f"cell={cell!r} -> {mo['status']}"
        assert data["exit_code"] == 2, f"cell={cell!r} blocked: {data['blocking']}"

    @pytest.mark.parametrize("cell,expected", [
        ("skipped", "skipped"),
        ("已跳过", "skipped"),
        # Template-canonical form: references/report-template.md uses
        # ⚠️ Skipped / ⚠️ 已跳过 (with or without the FE0F variation
        # selector and surrounding whitespace).
        ("⚠️ Skipped", "skipped"),
        ("⚠️Skipped", "skipped"),
        ("⚠️ 已跳过", "skipped"),
        ("partial", "partial"),
        ("部分通过", "partial"),
    ])
    def test_canonical_skipped_partial_status(self, cell: str, expected: str) -> None:
        path = self._report_with_status(cell)
        result = _run_audit(path, extra_args=["--strict", "--require-contract", "--json"])
        data = json.loads(result.stdout)
        mo = next(
            a for a in data["audits"] if a["audit_id"] == "market-outlook-audit"
        )
        assert mo["status"] == expected, f"cell={cell!r} -> {mo['status']}"
        # skipped/partial are recorded but never aggregate to Pass.
        assert data["exit_code"] == 2, f"cell={cell!r} blocked: {data['blocking']}"

    def _report_with_duplicate_declaration(self, first: str, second: str) -> Path:
        block = (
            "## Route and audit status\n\n"
            "**Primary route**: Market Outlook\n\n"
            "| Audit | Status | 证据 |\n"
            "|-------|--------|------|\n"
            f"| market-outlook-audit | {first} | §3 |\n"
            f"| market-outlook-audit | {second} | §3 |\n"
            "| forward-looking-claims | ✅ Passed | §4 |\n"
            "| source-traceability | ✅ Passed | §5 |\n"
            "| final-audit | ✅ Passed | §2 |\n"
            "| quantitative-role-audit | ✅ Passed | §6 |\n"
        )
        return _write(_report(route_block=block, contract=_contract()))

    def test_duplicate_audit_declaration_is_not_run(self) -> None:
        """A duplicate audit id must not be last-write-wins: ❌ Not run then
        ✅ Passed must still fail closed (issue #378)."""
        path = self._report_with_duplicate_declaration("❌ Not run", "✅ Passed")
        result = _run_audit(path, extra_args=["--strict", "--require-contract", "--json"])
        data = json.loads(result.stdout)
        mo = next(
            a for a in data["audits"] if a["audit_id"] == "market-outlook-audit"
        )
        assert mo["status"] == "not_run", mo
        assert data["exit_code"] == 2, data["blocking"]
        assert "duplicate" in mo["reason"].lower(), mo

    def test_duplicate_audit_declaration_reversed_is_not_run(self) -> None:
        """Opposite order: ✅ Passed first, ❌ Not run second must also fail."""
        path = self._report_with_duplicate_declaration("✅ Passed", "❌ Not run")
        result = _run_audit(path, extra_args=["--strict", "--require-contract", "--json"])
        data = json.loads(result.stdout)
        mo = next(
            a for a in data["audits"] if a["audit_id"] == "market-outlook-audit"
        )
        assert mo["status"] == "not_run", mo
        assert data["exit_code"] == 2, data["blocking"]

    def _report_with_two_route_blocks(self, first: str, second: str) -> Path:
        block1 = (
            "## Route and audit status\n\n**Primary route**: Market Outlook\n\n"
            "| Audit | Status | 证据 |\n|-------|--------|------|\n"
            f"| market-outlook-audit | {first} | §3 |\n"
            "| forward-looking-claims | ✅ Passed | §4 |\n"
            "| source-traceability | ✅ Passed | §5 |\n"
            "| final-audit | ✅ Passed | §2 |\n"
            "| quantitative-role-audit | ✅ Passed | §6 |\n"
        )
        block2 = (
            "## Route and audit status\n\n**Primary route**: Market Outlook\n\n"
            "| Audit | Status | 证据 |\n|-------|--------|------|\n"
            f"| market-outlook-audit | {second} | §3 |\n"
        )
        return _write(_report(route_block=block1, contract=_contract()) + "\n" + block2)

    def test_multiple_route_blocks_fail_closed(self) -> None:
        """A second Route and audit status block hiding '❌ Not run' after a
        '✅ Passed' first block must not be silently ignored (issue #378)."""
        path = self._report_with_two_route_blocks("✅ Passed", "❌ Not run")
        result = _run_audit(path, extra_args=["--strict", "--require-contract", "--json"])
        data = json.loads(result.stdout)
        assert data["exit_code"] == 2, data["blocking"]
        assert any("multiple" in b.lower() for b in data["blocking"]), data["blocking"]

    def test_multiple_route_blocks_reversed_fail_closed(self) -> None:
        """Opposite order must fail the same way."""
        path = self._report_with_two_route_blocks("❌ Not run", "✅ Passed")
        result = _run_audit(path, extra_args=["--strict", "--require-contract", "--json"])
        data = json.loads(result.stdout)
        assert data["exit_code"] == 2, data["blocking"]
        assert any("multiple" in b.lower() for b in data["blocking"]), data["blocking"]

    def test_multiple_route_blocks_fail_closed_even_non_strict(self) -> None:
        """Multiple route blocks are structural malformation: blocking in
        every mode, not only strict."""
        path = self._report_with_two_route_blocks("✅ Passed", "❌ Not run")
        result = _run_audit(path, extra_args=["--json"])
        data = json.loads(result.stdout)
        assert data["exit_code"] == 2, data["blocking"]
        assert any("multiple" in b.lower() for b in data["blocking"]), data["blocking"]

    @pytest.mark.parametrize("cell", [
        "✅ Passed",
        "✅ passed",
        "Passed",
        "passed",
        "Pass",
        "已通过",
        "✔ Passed",
        "✓ Passed",
        "✅Passed",
    ])
    def test_canonical_pass_status_is_pass(self, cell: str) -> None:
        path = self._report_with_status(cell)
        result = _run_audit(path, extra_args=["--strict", "--require-contract", "--json"])
        data = json.loads(result.stdout)
        mo = next(
            a for a in data["audits"] if a["audit_id"] == "market-outlook-audit"
        )
        assert mo["status"] == "pass", f"cell={cell!r} -> {mo['status']}"

    def test_undeclared_manual_audit_is_not_run_non_strict(self) -> None:
        """Non-strict records not_run explicitly without changing exit code."""
        path = self._report_missing_declaration()
        result = _run_audit(path, extra_args=["--json"])
        data = json.loads(result.stdout)
        mo = next(
            a for a in data["audits"] if a["audit_id"] == "market-outlook-audit"
        )
        assert mo["status"] == "not_run"
        assert mo["reason"] == "not declared in Route and audit status block"

    def test_undeclared_manual_audit_is_blocking_in_strict(self) -> None:
        path = self._report_missing_declaration()
        result = _run_audit(path, extra_args=["--strict", "--require-contract"])
        assert result.returncode == 2, result.stdout
        assert "market-outlook-audit" in result.stdout


class TestFailClosed:
    """Strict mode must fail closed on missing declarations."""

    def test_strict_no_route_fails(self) -> None:
        """No route block and no --route: strict must fail, not fall back."""
        report = (
            "# Test Report\n\n"
            "## Findings\n\nBody [S01].\n\n"
            "## Source Register\n\n"
            "| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |\n"
            "|----|-------------|-------------|------|---------|-------------|------------------|\n"
            "| S01 | Example A | secondary | 2026-01-01 | https://example.com/a | medium | §3 |\n"
        )
        path = _write(report)
        result = _run_audit(path, extra_args=["--strict"])
        assert result.returncode == 2, result.stdout
        assert "route" in result.stdout.lower()

    def test_non_strict_no_route_still_falls_back(self) -> None:
        """Legacy compatibility: non-strict keeps the default-route fallback."""
        report = (
            "# Test Report\n\n"
            "## Findings\n\nBody [S01].\n\n"
            "## Source Register\n\n"
            "| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |\n"
            "|----|-------------|-------------|------|---------|-------------|------------------|\n"
            "| S01 | Example A | secondary | 2026-01-01 | https://example.com/a | medium | §3 |\n"
        )
        path = _write(report)
        result = _run_audit(path)
        assert "technical-deep-dive" in result.stdout.lower()

    def test_strict_missing_contract_fails(self) -> None:
        """Strict implies --require-contract: missing contract is blocking."""
        path = _write(_report(contract=None))
        result = _run_audit(path, extra_args=["--strict"])
        assert result.returncode == 2, result.stdout
        assert "contract" in result.stdout.lower()

    def test_missing_contract_non_strict_skips(self) -> None:
        """Migration opt-out preserved: non-strict without contract has no
        contract-related blocking."""
        path = _write(_report(contract=None))
        result = _run_audit(path, extra_args=["--route", "market-outlook", "--json"])
        data = json.loads(result.stdout)
        assert not any("contract" in b for b in data["blocking"]), data["blocking"]

    def test_research_pack_not_provided_is_skipped(self) -> None:
        """research-pack audit is explicitly skipped when no pack is given."""
        path = _write(_report(contract=_contract()))
        result = _run_audit(path, extra_args=["--json"])
        data = json.loads(result.stdout)
        pack = next(a for a in data["audits"] if a["audit_id"] == "research-pack")
        assert pack["status"] == "skipped"

    def test_strict_missing_pack_fails(self) -> None:
        """Issue #378 acceptance: a strict task without a pack fails closed."""
        path = _write(_report(contract=_contract()))
        result = _run_audit(path, extra_args=["--strict"])
        assert result.returncode == 2, result.stdout
        assert "research-pack" in result.stdout

    def test_pack_route_mismatch_fails(self) -> None:
        """Pack primary route must match the contract's primary route."""
        report = _write(_report(contract=_contract()))
        pack = _write(PACK_FIXTURE.replace(
            "## Primary route\n\nMarket Outlook\n",
            "## Primary route\n\nShared-workflow\n",
        ))
        result = _run_audit(
            report, research_pack=pack, extra_args=["--strict", "--require-contract"]
        )
        assert result.returncode == 2, result.stdout
        assert "route" in result.stdout.lower()

    def test_pack_artifact_id_mismatch_fails(self) -> None:
        """Pack artifact id must match the contract's artifact_id."""
        report = _write(_report(contract=_contract()))
        pack = _write(PACK_FIXTURE.replace(
            "fixture-market-outlook-pos", "fixture-someone-else"
        ))
        result = _run_audit(
            report, research_pack=pack, extra_args=["--strict", "--require-contract"]
        )
        assert result.returncode == 2, result.stdout
        assert "artifact" in result.stdout.lower()


class TestAutomatedAuditBinding:
    """Automated audits without a registry binding must fail closed."""

    def test_missing_binding_fails_closed(self, monkeypatch) -> None:
        import audit_report
        import registry_loader

        # Simulate an audit registry where forward-looking-claims lost its
        # validator binding (registry/code drift).
        class FakeAuditInfo:
            def __init__(self, aid, etype, binding):
                self.id = aid
                self.execution_type = etype
                self.validator_binding = binding
                self.checklist = "checklists/forward-looking-claims.md"
                self.description = ""
                self.automation_reference = None

        class FakeAuditRegistry:
            version = 1

            def __init__(self):
                self._audits = {
                    "market-outlook-audit": FakeAuditInfo(
                        "market-outlook-audit", "manual", None),
                    "forward-looking-claims": FakeAuditInfo(
                        "forward-looking-claims", "automated", None),
                    "source-traceability": FakeAuditInfo(
                        "source-traceability", "automated",
                        "source-label-consistency"),
                    "final-audit": FakeAuditInfo("final-audit", "manual", None),
                }

            def get_audit(self, aid):
                return self._audits.get(aid)

            def audit_ids(self):
                return set(self._audits)

        monkeypatch.setattr(audit_report, "_AUDIT_REGISTRY", FakeAuditRegistry())
        path = _write(_report(contract=_contract()))
        verdict = audit_report.audit_report(path, route="market-outlook")
        assert verdict.overall == "fail"
        assert any("forward-looking-claims" in e for e in verdict.blocking)


class TestJsonOutput:
    """--json must emit a machine-readable verdict."""

    def test_json_shape(self) -> None:
        path = _write(_report(contract=_contract()))
        result = _run_audit(path, extra_args=["--json"])
        assert result.returncode == 0, result.stdout
        data = json.loads(result.stdout)
        assert data["route"] == "market-outlook"
        assert data["overall"] == "pass"
        assert data["exit_code"] == 0
        assert data["input_sha256"]
        assert data["validator_version"]
        for audit in data["audits"]:
            assert audit["audit_id"]
            assert audit["status"]
            assert audit["execution_type"]
        # human-readable summary must not pollute stdout
        assert "Route:" not in result.stdout

    def test_json_with_failures(self) -> None:
        report = _report(contract=_contract())
        report += (
            "\n## Outlook\n\n"
            "[Confirmed] Shipments will reach 100 units by 2027.\n"
        )
        path = _write(report)
        result = _run_audit(path, extra_args=["--json"])
        assert result.returncode == 2
        data = json.loads(result.stdout)
        assert data["overall"] == "fail"
        fl = next(
            a for a in data["audits"] if a["audit_id"] == "forward-looking-claims"
        )
        assert fl["status"] == "fail"
        assert fl["errors"]

    def test_automated_success_has_evidence_location(self) -> None:
        """Successful automated audits carry an evidence location, not []."""
        path = _write(_report(contract=_contract()))
        result = _run_audit(path, extra_args=["--json"])
        data = json.loads(result.stdout)
        for audit in data["audits"]:
            if audit["audit_id"] == "research-pack":
                continue  # skipped by design without a pack
            if audit["status"] == "pass" and audit["execution_type"] == "automated":
                assert audit["evidence"], audit
                assert str(path) in audit["evidence"][0], audit

    def test_early_failure_json_has_provenance(self) -> None:
        """Even early-failure verdicts must carry input hash + version."""
        report = (
            "# Test Report\n\n"
            "## Findings\n\nBody [S01].\n\n"
            "## Source Register\n\n"
            "| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |\n"
            "|----|-------------|-------------|------|---------|-------------|------------------|\n"
            "| S01 | Example A | secondary | 2026-01-01 | https://example.com/a | medium | §3 |\n"
        )
        path = _write(report)
        result = _run_audit(path, extra_args=["--strict", "--json"])
        data = json.loads(result.stdout)
        assert data["overall"] == "fail"
        assert data["input_sha256"], data
        assert data["validator_version"], data

    def test_unknown_route_json_has_provenance(self) -> None:
        path = _write(_report(contract=_contract()))
        result = _run_audit(path, extra_args=["--route", "no-such-route", "--json"])
        data = json.loads(result.stdout)
        assert data["overall"] == "fail"
        assert data["input_sha256"], data
        assert data["validator_version"], data


class TestSingleCommandCoverage:
    """Markdown delivery + Research Pack + contract + route audits in one command."""

    def test_markdown_delivery_and_pack_run_together(self) -> None:
        report = _write(_report(contract=_contract()))
        pack = _write(PACK_FIXTURE)
        result = _run_audit(
            report, research_pack=pack, extra_args=["--strict", "--require-contract"]
        )
        assert result.returncode == 0, result.stdout

    def test_invalid_pack_fails(self) -> None:
        report = _write(_report(contract=_contract()))
        bad_pack = _write("# Not a pack\n")
        result = _run_audit(
            report, research_pack=bad_pack, extra_args=["--strict"]
        )
        assert result.returncode == 2, result.stdout
        assert "research-pack" in result.stdout.lower()


class TestSelfAssessmentCannotOverride:
    """A report claiming Passed must not override validator failures."""

    def test_report_claims_pass_but_validator_fails(self) -> None:
        # Report declares all audits Passed but body has no monitoring section.
        report = _report(
            contract=_contract(), include_monitoring=False, route_block=_route_block("market-outlook")
        )
        path = _write(report)
        result = _run_audit(path, extra_args=["--strict", "--require-contract"])
        assert result.returncode == 2, result.stdout
        assert "monitoring" in result.stdout.lower()


class TestDuplicateDeclarations:
    """User-writable declarations (contract / pack sections / route blocks)
    must be collected in full and reject cardinality != 1 (issue #378)."""

    def _run_with_pack(self, path: Path, pack: Path | None = None) -> dict:
        args = ["--strict", "--require-contract", "--json"]
        result = _run_audit(path, extra_args=args, research_pack=pack)
        return json.loads(result.stdout)

    def test_second_malformed_contract_block_fails(self) -> None:
        """A second ```contract block (malformed) must not be ignored."""
        report = _report(contract=_contract())
        report += '\n```contract\n{"this is": broken\n```\n'
        path = _write(report)
        data = self._run_with_pack(
            path, Path("tests/fixtures/audit/research-pack-pos.md").resolve()
            if False else None
        )
        # strict 缺 pack 也会 fail，这里直接断言 contract 相关阻断
        result = _run_audit(
            path, extra_args=["--strict", "--require-contract"],
            research_pack=Path("tests/fixtures/audit/research-pack-pos.md").resolve(),
        )
        assert result.returncode == 2, result.stdout
        assert "contract" in result.stdout.lower()

    def test_second_contract_block_conflicting_route_fails(self) -> None:
        """A second valid contract with a different route must not be ignored."""
        report = _report(contract=_contract())
        report += "\n```contract\n" + _contract("shared-workflow") + "\n```\n"
        path = _write(report)
        result = _run_audit(
            path, extra_args=["--strict", "--require-contract"],
            research_pack=Path("tests/fixtures/audit/research-pack-pos.md").resolve(),
        )
        assert result.returncode == 2, result.stdout
        assert "contract" in result.stdout.lower()

    def test_pack_duplicate_primary_route_fails(self) -> None:
        """A second '## Primary route' section in the pack must not be ignored."""
        pack_text = PACK_FIXTURE + "\n## Primary route\n\nShared-workflow\n"
        pack = _write(pack_text)
        path = _write(_report(contract=_contract()))
        result = _run_audit(
            path, extra_args=["--strict", "--require-contract"],
            research_pack=pack,
        )
        assert result.returncode == 2, result.stdout
        assert "primary route" in result.stdout.lower()

    def test_pack_duplicate_artifact_id_fails(self) -> None:
        """A second '## Artifact id' section in the pack must not be ignored."""
        pack_text = PACK_FIXTURE + "\n## Artifact id\n\nfixture-someone-else\n"
        pack = _write(pack_text)
        path = _write(_report(contract=_contract()))
        result = _run_audit(
            path, extra_args=["--strict", "--require-contract"],
            research_pack=pack,
        )
        assert result.returncode == 2, result.stdout
        assert "artifact" in result.stdout.lower()

    def test_fenced_fake_route_block_does_not_bypass_mismatch(self) -> None:
        """A route declaration inside a fenced code block must not count as
        the report's real route declaration."""
        visible_block = (
            "## Route and audit status\n\n**Primary route**: Shared-workflow\n\n"
            "| Audit | Status | 证据 |\n|-------|--------|------|\n"
            "| workflow-spine-audit | ✅ Passed | §3 |\n"
            "| final-audit | ✅ Passed | §2 |\n"
        )
        fake = (
            "```markdown\n## Route and audit status\n\n"
            "**Primary route**: Market Outlook\n\n"
            "| Audit | Status | 证据 |\n|-------|--------|------|\n"
            "| market-outlook-audit | ✅ Passed | §3 |\n```\n"
        )
        report = (
            "# Test Report\n\n" + fake + "\n" + visible_block +
            "\n## Executive summary\n\n**核心判断**：X is Y [S01].\n\n- a\n- b\n"
            "\n## Findings\n\nBody [S01] [S02].\n"
            "\n## Comparison Table\n\n| Metric | A | B | 数字角色 |\n"
            "|--------|---|---|---------|\n"
            "| Cost | 100 | 80 | observed |\n"
            "| Speed | 200 | 150 | observed |\n"
            "\n## Dimension conclusions\n\nBacked by [S01] and [S02].\n"
            "\n## Source Register\n\n"
            "| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |\n"
            "|----|-------------|-------------|------|---------|-------------|------------------|\n"
            "| S01 | Example A | secondary | 2026-01-01 | https://example.com/a | medium | §3 |\n"
            "| S02 | Example B | secondary | 2026-02-01 | https://example.com/b | high | §5 |\n"
            "\n```contract\n" + _contract() + "\n```\n"
        )
        path = _write(report)
        result = _run_audit(
            path, extra_args=["--strict", "--require-contract"],
            research_pack=Path("tests/fixtures/audit/research-pack-pos.md").resolve(),
        )
        assert result.returncode == 2, result.stdout

    def test_missing_route_block_is_structural_malformation(self) -> None:
        """Zero Route and audit status blocks is also cardinality != 1:
        the JSON verdict must report it as structural malformation."""
        report = (
            "# Test Report\n\n"
            "## Findings\n\nBody [S01].\n\n"
            "## Source Register\n\n"
            "| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |\n"
            "|----|-------------|-------------|------|---------|-------------|------------------|\n"
            "| S01 | Example A | secondary | 2026-01-01 | https://example.com/a | medium | §3 |\n"
        )
        path = _write(report)
        result = _run_audit(path, extra_args=["--route", "market-outlook", "--strict", "--json"])
        data = json.loads(result.stdout)
        assert data["exit_code"] == 2
        assert any(
            "route and audit status" in b.lower() for b in data["blocking"]
        ), data["blocking"]

    def test_nested_fenced_contract_example_is_ignored(self) -> None:
        """A ```contract example nested inside a `````markdown fence must
        not count as the real contract (fence-level parsing)."""
        full = _contract()
        nested = (
            "````markdown\nExample report contract:\n"
            "```contract\n" + full + "\n```\n````\n"
        )
        report = _report(contract=None) + "\n" + nested
        path = _write(report)
        result = _run_audit(
            path, extra_args=["--strict", "--require-contract"],
            research_pack=Path("tests/fixtures/audit/research-pack-pos.md").resolve(),
        )
        # No real top-level contract: strict must fail, not silently adopt
        # the nested example.
        assert result.returncode == 2, result.stdout
        assert "contract" in result.stdout.lower()

    def test_duplicate_json_key_in_contract_fails(self) -> None:
        """Duplicate object keys in the contract JSON are malformed —
        last-write-wins must not let a trailing good value win."""
        dup = (
            '{"primary_route": "shared-workflow", '
            '"primary_route": "market-outlook", '
            '"secondary_routes": [], "disciplines": [], '
            '"audits": [{"id": "market-outlook-audit", "status": "passed", '
            '"evidence": "§3"}, {"id": "forward-looking-claims", '
            '"status": "passed", "evidence": "§4"}, '
            '{"id": "source-traceability", "status": "passed", '
            '"evidence": "§5"}, {"id": "final-audit", "status": "passed", '
            '"evidence": "§2"}], '
            '"artifact_id": "fixture-market-outlook-pos", '
            '"contract_version": "1.0.0", "created_at": "2026-08-13"}'
        )
        path = _write(_report(contract=dup))
        result = _run_audit(
            path, extra_args=["--strict", "--require-contract"],
            research_pack=Path("tests/fixtures/audit/research-pack-pos.md").resolve(),
        )
        assert result.returncode == 2, result.stdout
        assert "duplicate" in result.stdout.lower() or "contract" in result.stdout.lower()

    def test_duplicate_route_declaration_in_block_fails(self) -> None:
        """Two '**Primary route**' lines in one status block are malformed —
        the first declaration must not win."""
        block = (
            "## Route and audit status\n\n"
            "**Primary route**: Market Outlook\n"
            "**Primary route**: Technical Deep-dive\n\n"
            "| Audit | Status | 证据 |\n|-------|--------|------|\n"
            "| market-outlook-audit | ✅ Passed | §3 |\n"
            "| forward-looking-claims | ✅ Passed | §4 |\n"
            "| source-traceability | ✅ Passed | §5 |\n"
            "| final-audit | ✅ Passed | §2 |\n"
            "| quantitative-role-audit | ✅ Passed | §6 |\n"
        )
        path = _write(_report(route_block=block, contract=_contract()))
        result = _run_audit(
            path, extra_args=["--strict", "--require-contract"],
            research_pack=Path("tests/fixtures/audit/research-pack-pos.md").resolve(),
        )
        assert result.returncode == 2, result.stdout
        assert "route" in result.stdout.lower()

    @pytest.mark.parametrize("label", ["notcontract", "contract-example", "contracts"])
    def test_non_contract_fence_label_is_ignored(self, label: str) -> None:
        """Only an exact 'contract' fence label counts as a contract
        declaration — substring matches like notcontract /
        contract-example must not satisfy --require-contract."""
        report = _report(contract=None)
        report += f"\n```{label}\n{_contract()}\n```\n"
        path = _write(report)
        result = _run_audit(
            path, extra_args=["--strict", "--require-contract"],
            research_pack=Path("tests/fixtures/audit/research-pack-pos.md").resolve(),
        )
        assert result.returncode == 2, result.stdout
        assert "contract" in result.stdout.lower()

    def test_fenced_pack_primary_route_fails(self) -> None:
        """A pack whose only '## Primary route' is inside a fenced block
        has no visible route declaration: audit_report must fail closed."""
        fenced = PACK_FIXTURE.replace(
            "## Primary route\n\nMarket Outlook\n",
            "~~~markdown\n## Primary route\n\nMarket Outlook\n~~~\n",
        )
        pack = _write(fenced)
        path = _write(_report(contract=_contract()))
        result = _run_audit(
            path, extra_args=["--strict", "--require-contract"], research_pack=pack
        )
        assert result.returncode == 2, result.stdout
        assert "route" in result.stdout.lower()

    def test_fenced_pack_primary_route_standalone_cli_fails(self) -> None:
        """The standalone validate_contract CLI must behave identically:
        a fenced-only Primary route must not resolve."""
        import sys as _sys
        _sys.path.insert(0, str(SCRIPTS_DIR))
        from validate_contract import main as vc_main

        fenced = PACK_FIXTURE.replace(
            "## Primary route\n\nMarket Outlook\n",
            "~~~markdown\n## Primary route\n\nMarket Outlook\n~~~\n",
        )
        pack = _write(fenced)
        report = _write(_report(contract=_contract()))
        code = vc_main([
            str(report), "--require-contract", "--strict",
            "--research-pack", str(pack),
        ])
        assert code == 2, f"standalone CLI must fail closed, got {code}"

    def test_unclosed_inner_fence_does_not_leak_pack_route(self) -> None:
        """A four-backtick fence containing an unclosed three-backtick fence
        must still hide its '## Primary route' (fence-length-aware parsing):
        both CLIs fail closed instead of leaking the section."""
        nested = (
            "````markdown\n"
            "```python\n"
            "# inner fence never closed\n"
            "## Primary route\n\n"
            "Market Outlook\n"
            "````\n"
        )
        pack = _write(PACK_FIXTURE.replace(
            "## Primary route\n\nMarket Outlook\n", nested
        ))
        report = _write(_report(contract=_contract()))

        # audit_report path
        result = _run_audit(
            report, extra_args=["--strict", "--require-contract"], research_pack=pack
        )
        assert result.returncode == 2, result.stdout
        assert "primary route" in result.stdout.lower()

        # standalone CLI path must behave identically
        import sys as _sys
        _sys.path.insert(0, str(SCRIPTS_DIR))
        from validate_contract import main as vc_main
        code = vc_main([
            str(report), "--require-contract", "--strict",
            "--research-pack", str(pack),
        ])
        assert code == 2, f"standalone CLI must fail closed, got {code}"

    def test_html_comment_route_block_is_not_a_declaration(self) -> None:
        """A whole 'Route and audit status' block inside <!-- --> is
        non-rendered content: strict audit must fail closed (issue #378)."""
        commented_block = (
            "<!--\n## Route and audit status\n\n"
            "**Primary route**: Market Outlook\n\n"
            "| Audit | Status | 证据 |\n|-------|--------|------|\n"
            "| market-outlook-audit | ✅ Passed | §3 |\n"
            "| forward-looking-claims | ✅ Passed | §4 |\n"
            "| source-traceability | ✅ Passed | §5 |\n"
            "| final-audit | ✅ Passed | §2 |\n"
            "| quantitative-role-audit | ✅ Passed | §6 |\n"
            "-->\n"
        )
        path = _write(_report(route_block=commented_block, contract=_contract()))
        result = _run_audit(
            path, extra_args=["--strict", "--require-contract"],
            research_pack=Path("tests/fixtures/audit/research-pack-pos.md").resolve(),
        )
        assert result.returncode == 2, result.stdout
        # Comment-hidden route block means no visible route declaration:
        # strict fails either on the missing declaration or the missing
        # audit-status block.
        assert "route" in result.stdout.lower()

    def test_html_comment_pack_primary_route_fails(self) -> None:
        """A pack '## Primary route' inside <!-- --> is not a visible
        declaration: both CLIs fail closed."""
        commented = PACK_FIXTURE.replace(
            "## Primary route\n\nMarket Outlook\n",
            "<!--\n## Primary route\n\nMarket Outlook\n-->\n",
        )
        pack = _write(commented)
        report = _write(_report(contract=_contract()))

        result = _run_audit(
            report, extra_args=["--strict", "--require-contract"], research_pack=pack
        )
        assert result.returncode == 2, result.stdout
        assert "primary route" in result.stdout.lower()

        import sys as _sys
        _sys.path.insert(0, str(SCRIPTS_DIR))
        from validate_contract import main as vc_main
        code = vc_main([
            str(report), "--require-contract", "--strict",
            "--research-pack", str(pack),
        ])
        assert code == 2, f"standalone CLI must fail closed, got {code}"

    def test_comment_monitoring_section_fails(self) -> None:
        """A '## Monitoring signals' section inside <!-- --> is not
        rendered content: the market-outlook monitoring audit must fail
        closed (issue #378)."""
        commented = "<!--\n" + _monitoring_section() + "-->\n"
        report = _report(contract=_contract(), include_monitoring=False)
        report = report.replace(
            "\n## Comparison Table",
            "\n" + commented + "\n## Comparison Table",
        )
        path = _write(report)
        result = _run_audit(
            path, extra_args=["--strict", "--require-contract"],
            research_pack=Path("tests/fixtures/audit/research-pack-pos.md").resolve(),
        )
        assert result.returncode == 2, result.stdout
        assert "monitoring" in result.stdout.lower()

    def test_comment_hidden_report_structure_fails_markdown_delivery(self) -> None:
        """A report whose entire visible structure lives inside <!-- -->
        has no rendered headings: the markdown-delivery audit must fail."""
        hidden = "<!--\n" + _report(contract=_contract()) + "\n-->\n"
        path = _write(hidden)
        result = _run_audit(
            path, extra_args=["--route", "market-outlook", "--strict", "--json"]
        )
        data = json.loads(result.stdout)
        assert data["exit_code"] == 2, data["blocking"]

    def test_comment_hidden_pack_section_fails(self) -> None:
        """Pack sections inside <!-- --> are not visible: the pack fails
        structure checks."""
        commented = PACK_FIXTURE.replace(
            "## Objective\n\nDetermine X, grounded on [S01].\n",
            "<!--\n## Objective\n\nDetermine X, grounded on [S01].\n-->\n",
        )
        pack = _write(commented)
        report = _write(_report(contract=_contract()))
        result = _run_audit(
            report, extra_args=["--strict", "--require-contract"], research_pack=pack
        )
        assert result.returncode == 2, result.stdout
        assert "objective" in result.stdout.lower()

    @pytest.mark.parametrize("tag", ["div", "pre", "script", "style"])
    def test_html_block_route_status_hidden_fails(self, tag: str) -> None:
        """A whole 'Route and audit status' block inside a raw HTML block
        (div/pre/script/style) is not rendered Markdown: strict audit must
        fail closed (issue #378, CommonMark HTML-block semantics)."""
        html_block = (
            f"<{tag}>\n## Route and audit status\n\n"
            "**Primary route**: Market Outlook\n\n"
            "| Audit | Status | 证据 |\n|-------|--------|------|\n"
            "| market-outlook-audit | ✅ Passed | §3 |\n"
            "| forward-looking-claims | ✅ Passed | §4 |\n"
            "| source-traceability | ✅ Passed | §5 |\n"
            "| final-audit | ✅ Passed | §2 |\n"
            "| quantitative-role-audit | ✅ Passed | §6 |\n"
            f"</{tag}>\n"
        )
        path = _write(_report(route_block=html_block, contract=_contract()))
        result = _run_audit(
            path, extra_args=["--strict", "--require-contract"],
            research_pack=Path("tests/fixtures/audit/research-pack-pos.md").resolve(),
        )
        assert result.returncode == 2, result.stdout

    def test_html_block_pack_primary_route_fails(self) -> None:
        """A pack '## Primary route' inside <div> is not a visible
        declaration: both CLIs fail closed."""
        div_pack = PACK_FIXTURE.replace(
            "## Primary route\n\nMarket Outlook\n",
            "<div>\n## Primary route\n\nMarket Outlook\n</div>\n",
        )
        pack = _write(div_pack)
        report = _write(_report(contract=_contract()))

        result = _run_audit(
            report, extra_args=["--strict", "--require-contract"], research_pack=pack
        )
        assert result.returncode == 2, result.stdout
        assert "primary route" in result.stdout.lower()

        import sys as _sys
        _sys.path.insert(0, str(SCRIPTS_DIR))
        from validate_contract import main as vc_main
        code = vc_main([
            str(report), "--require-contract", "--strict",
            "--research-pack", str(pack),
        ])
        assert code == 2, f"standalone CLI must fail closed, got {code}"

    def test_nested_html_block_route_status_hidden_fails(self) -> None:
        """Same-tag nesting: an inner </div> must not close the outer
        <div> and expose a forged route block (issue #378)."""
        route_block = (
            "## Route and audit status\n\n**Primary route**: Market Outlook\n\n"
            "| Audit | Status | 证据 |\n|-------|--------|------|\n"
            "| market-outlook-audit | ✅ Passed | §3 |\n"
            "| forward-looking-claims | ✅ Passed | §4 |\n"
            "| source-traceability | ✅ Passed | §5 |\n"
            "| final-audit | ✅ Passed | §2 |\n"
            "| quantitative-role-audit | ✅ Passed | §6 |\n"
        )
        nested = "<div>\n<div>\ninner\n</div>\n" + route_block + "\n</div>\n"
        path = _write(_report(route_block=nested, contract=_contract()))
        result = _run_audit(
            path, extra_args=["--strict", "--require-contract"],
            research_pack=Path("tests/fixtures/audit/research-pack-pos.md").resolve(),
        )
        assert result.returncode == 2, result.stdout

    @pytest.mark.parametrize("tag", [
        "h1", "h2", "h6", "head", "html", "iframe", "textarea", "template",
        "body", "title",
    ])
    def test_more_html_block_tags_hide_route_status(self, tag: str) -> None:
        """Additional CommonMark block tags must hide declarations."""
        route_block = (
            "## Route and audit status\n\n**Primary route**: Market Outlook\n\n"
            "| Audit | Status | 证据 |\n|-------|--------|------|\n"
            "| market-outlook-audit | ✅ Passed | §3 |\n"
            "| forward-looking-claims | ✅ Passed | §4 |\n"
            "| source-traceability | ✅ Passed | §5 |\n"
            "| final-audit | ✅ Passed | §2 |\n"
            "| quantitative-role-audit | ✅ Passed | §6 |\n"
        )
        html_block = f"<{tag}>\n" + route_block + f"\n</{tag}>\n"
        path = _write(_report(route_block=html_block, contract=_contract()))
        result = _run_audit(
            path, extra_args=["--strict", "--require-contract"],
            research_pack=Path("tests/fixtures/audit/research-pack-pos.md").resolve(),
        )
        assert result.returncode == 2, result.stdout

    def test_html_block_pack_objective_fails_both_clis(self) -> None:
        """A pack '## Objective' inside <div> must fail both the pack
        validator and audit_report (shared sanitizer, issue #378)."""
        div_pack = PACK_FIXTURE.replace(
            "## Objective\n\nDetermine X, grounded on [S01].\n",
            "<div>\n## Objective\n\nDetermine X, grounded on [S01].\n</div>\n",
        )
        pack = _write(div_pack)
        report = _write(_report(contract=_contract()))

        result = _run_audit(
            report, extra_args=["--strict", "--require-contract"], research_pack=pack
        )
        assert result.returncode == 2, result.stdout
        assert "objective" in result.stdout.lower()

        import sys as _sys
        _sys.path.insert(0, str(SCRIPTS_DIR))
        r = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / "validate_research_pack.py"),
             str(pack), "--strict"],
            capture_output=True, text=True,
        )
        assert r.returncode != 0, f"standalone pack validator must fail:\n{r.stdout}"


class TestSecondaryHardFail:
    """Secondary-route hard-fail verification needs its own audit result
    (issue #378 acceptance 6) — primary-route coverage is not enough."""

    def _secondary_report(self, contract_text: str) -> Path:
        block = _route_block("market-outlook")
        return _write(_report(contract=contract_text, route_block=block))

    def test_declared_secondary_hard_fail_present_passes(self) -> None:
        contract = _contract(
            secondary_routes=["constrained-choice"],
            audits=[
                {"id": "market-outlook-audit", "status": "passed", "evidence": "§3"},
                {"id": "forward-looking-claims", "status": "passed", "evidence": "§4"},
                {"id": "source-traceability", "status": "passed", "evidence": "§5"},
                {"id": "final-audit", "status": "passed", "evidence": "§2"},
                {"id": "constrained-choice-secondary-hard-fail", "status": "passed",
                 "evidence": "§6 verified hard-fail conditions"},
            ],
        )
        path = self._secondary_report(contract)
        result = _run_audit(path, extra_args=["--strict", "--require-contract", "--json"])
        data = json.loads(result.stdout)
        ids = {a["audit_id"]: a for a in data["audits"]}
        assert "constrained-choice-secondary-hard-fail" in ids
        assert ids["constrained-choice-secondary-hard-fail"]["status"] == "pass"

    def test_missing_secondary_hard_fail_is_not_run_blocking(self) -> None:
        """Secondary declared but no hard-fail audit entry: must not pass."""
        contract = _contract(
            secondary_routes=["constrained-choice"],
            audits=[
                {"id": "market-outlook-audit", "status": "passed", "evidence": "§3"},
                {"id": "forward-looking-claims", "status": "passed", "evidence": "§4"},
                {"id": "source-traceability", "status": "passed", "evidence": "§5"},
                {"id": "final-audit", "status": "passed", "evidence": "§2"},
            ],
        )
        path = self._secondary_report(contract)
        result = _run_audit(path, extra_args=["--strict", "--require-contract"])
        assert result.returncode == 2, result.stdout
        assert "constrained-choice-secondary-hard-fail" in result.stdout


# A minimal valid Research Pack satisfying validate_research_pack structure
# and strict semantic checks (see scripts/validate_research_pack.py).
PACK_FIXTURE = """\
## Objective

Determine X, grounded on [S01].

## Decision context

Context with boundary judgment: chosen over alternative Y, rejected because
scope mismatch; would become relevant if market conditions change.

## Primary route

Market Outlook

Market Outlook selected as primary route. The closest alternative,
shared-workflow, was rejected because this task needs scenario structure.
Boundary: if monitoring signals are not required, shared-workflow would apply.

## Secondary disciplines

- none

## Core subquestions

- Q1

## Stop condition

Stop when evidence saturated.

## Source register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Example A | secondary | 2026-01-01 | https://example.com/a | medium | §3 |

## Claim register

| Claim | Source ID |
|-------|-----------|
| C1 | S01 |

## Uncertainty register

| Uncertainty | Source ID |
|-------------|-----------|
| U01 | S01 |

## Artifact id

fixture-market-outlook-pos

## Artifact contract

| Field | Value |
|-------|-------|
| artifact_id | fixture-market-outlook-pos |

## Required audits

- market-outlook-audit — passed: executed by author
- forward-looking-claims — passed: no mislabeled claims
- source-traceability — passed: register complete
- final-audit — passed: all gates verified

## Final audit status

Pass
"""
