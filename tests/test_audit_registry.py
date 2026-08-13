#!/usr/bin/env python3
"""
Data-integrity tests for schemas/audit-registry.json (issue #374).

Verifies the audit registry is the canonical fact source for audit
identity: every checklist file is registered, every registered audit
maps to a real file, and every route required_audits reference is
defined in the registry.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from registry_loader import load_audit_registry, load_route_registry  # noqa: E402

AUDIT_REGISTRY_PATH = ROOT / "schemas" / "audit-registry.json"
CHECKLISTS_DIR = ROOT / "checklists"


class TestAuditRegistryDataIntegrity:
    def test_audit_registry_file_exists(self) -> None:
        assert AUDIT_REGISTRY_PATH.is_file(), f"Missing: {AUDIT_REGISTRY_PATH}"

    def test_every_checklist_file_is_registered(self) -> None:
        """No checklist file may exist without a registry entry."""
        registry = load_audit_registry()
        registered = {a.id for a in registry.audits}
        files_on_disk = {p.stem for p in CHECKLISTS_DIR.glob("*.md")}
        unregistered = files_on_disk - registered
        assert not unregistered, (
            f"Checklist files without registry entries: {sorted(unregistered)}"
        )

    def test_every_registered_audit_has_checklist_file(self) -> None:
        registry = load_audit_registry()
        files_on_disk = {p.stem for p in CHECKLISTS_DIR.glob("*.md")}
        for a in registry.audits:
            assert a.id in files_on_disk, (
                f"Audit '{a.id}' has no checklist file in checklists/"
            )

    def test_every_route_required_audit_is_registered(self) -> None:
        """All route required_audits must resolve to registry entries."""
        registry = load_audit_registry()
        known = {a.id for a in registry.audits}
        routes = load_route_registry()
        for route in routes.routes:
            unknown = set(route.required_audits) - known
            assert not unknown, (
                f"Route '{route.id}' required audits not in registry: "
                f"{sorted(unknown)}"
            )

    def test_automated_audits_have_automation_reference(self) -> None:
        registry = load_audit_registry()
        for a in registry.audits:
            if a.execution_type == "automated":
                assert a.automation_reference, (
                    f"Automated audit '{a.id}' missing automation_reference"
                )

    def test_manual_and_process_audits_have_no_automation_reference(self) -> None:
        registry = load_audit_registry()
        for a in registry.audits:
            if a.execution_type in ("manual", "process"):
                assert a.automation_reference is None, (
                    f"Audit '{a.id}' should not declare automation_reference "
                    f"for execution_type '{a.execution_type}'"
                )

    def test_automation_references_exist(self) -> None:
        registry = load_audit_registry()
        for a in registry.audits:
            if a.automation_reference:
                assert (ROOT / a.automation_reference).is_file(), (
                    f"Audit '{a.id}' automation_reference missing: "
                    f"{a.automation_reference}"
                )

    def test_route_manifest_version_is_current(self) -> None:
        """The route manifest this registry feeds must be version 2+."""
        data = json.loads((ROOT / "schemas" / "route-manifest.json").read_text())
        assert data["version"] >= 2, "route-manifest.json must be version >= 2"


if __name__ == "__main__":
    passed = 0
    failed = 0
    instance = TestAuditRegistryDataIntegrity()
    for name in dir(instance):
        if name.startswith("test_"):
            try:
                getattr(instance, name)()
                print(f"  PASS  {name}")
                passed += 1
            except Exception as e:
                print(f"  FAIL  {name}: {e}")
                failed += 1
    print(f"\n{passed} passed, {failed} failed")
    sys.exit(0 if failed == 0 else 1)
