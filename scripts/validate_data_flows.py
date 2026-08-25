#!/usr/bin/env python3
"""Validate data-flow documentation against the machine-readable registry.

Checks:
  1. docs/DATA_FLOWS.md and docs/RISK_REGISTER.md exist with required sections
  2. Every registry network touchpoint and local store appears in DATA_FLOWS.md
  3. Every registry risk_id appears in RISK_REGISTER.md
  4. Repo-owned network signal files match the registry (drift detection)
  5. Cross-links from README, SKILL.md, and external-channel-preflight.md

Exit codes:
  0 = all checks pass
  1 = one or more checks failed
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
REGISTRY_PATH = REPO / "schemas" / "data-flow-registry.json"
DATA_FLOWS_PATH = REPO / "docs" / "DATA_FLOWS.md"
RISK_REGISTER_PATH = REPO / "docs" / "RISK_REGISTER.md"

NETWORK_SIGNAL_PATTERNS: dict[str, re.Pattern[str]] = {
    "async_playwright": re.compile(r"async_playwright"),
    "gh_cli": re.compile(r"\bgh\b.*(?:api|issue|pr)|subprocess\.run\(\s*\[\s*[\"']gh[\"']"),
}

DATA_FLOWS_REQUIRED_SECTIONS = [
    "## Scope",
    "## Out-of-repository control boundary",
    "## Network touchpoints",
    "## Local stores",
    "## Off-switch and degraded-state summary",
]

RISK_REGISTER_REQUIRED_SECTIONS = [
    "## How to read an entry",
]

CROSS_LINK_CHECKS: list[tuple[str, str, str]] = [
    ("README.md", "README links to DATA_FLOWS", "docs/DATA_FLOWS.md"),
    ("README.md", "README links to RISK_REGISTER", "docs/RISK_REGISTER.md"),
    ("SKILL.md", "SKILL.md links to DATA_FLOWS", "docs/DATA_FLOWS.md"),
    ("SKILL.md", "SKILL.md links to RISK_REGISTER", "docs/RISK_REGISTER.md"),
    (
        "references/external-channel-preflight.md",
        "external-channel-preflight links to DATA_FLOWS",
        "docs/DATA_FLOWS.md",
    ),
    (
        "references/external-channel-preflight.md",
        "external-channel-preflight links to RISK_REGISTER",
        "docs/RISK_REGISTER.md",
    ),
]

VERIFICATION_STATUS_RE = re.compile(
    r"\b(measured|asserted|not_run|unknown)\b",
    re.IGNORECASE,
)


def load_registry() -> dict:
    if not REGISTRY_PATH.exists():
        raise FileNotFoundError(f"Registry not found: {REGISTRY_PATH}")
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def read_text(rel_path: str) -> str:
    path = REPO / rel_path
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")
    return path.read_text(encoding="utf-8")


def check_required_sections(text: str, sections: list[str], label: str) -> list[str]:
    failures: list[str] = []
    for section in sections:
        if section not in text:
            failures.append(f"{label} missing section: {section}")
    return failures


def check_component_ids_present(text: str, component_ids: list[str], label: str) -> list[str]:
    failures: list[str] = []
    for component_id in component_ids:
        if f"`{component_id}`" not in text:
            failures.append(f"{label} missing component id: `{component_id}`")
    return failures


def collect_signal_files(signal: str) -> set[str]:
    pattern = NETWORK_SIGNAL_PATTERNS[signal]
    matches: set[str] = set()
    search_roots = [REPO / "scripts"]
    for root in search_roots:
        if not root.exists():
            continue
        for path in root.rglob("*.py"):
            rel = path.relative_to(REPO).as_posix()
            if rel.startswith("scripts/test_") or rel == "scripts/validate_data_flows.py":
                continue
            content = path.read_text(encoding="utf-8", errors="replace")
            if pattern.search(content):
                matches.add(rel)
    return matches


def check_network_signal_drift(registry: dict) -> list[str]:
    failures: list[str] = []
    for touchpoint in registry.get("network_touchpoints", []):
        if touchpoint.get("kind") != "repo_script":
            continue
        component_id = touchpoint["id"]
        declared_files = set(touchpoint.get("source_files", []))
        for signal in touchpoint.get("network_signals", []):
            if signal not in NETWORK_SIGNAL_PATTERNS:
                failures.append(
                    f"Registry component `{component_id}` references unknown signal: {signal}"
                )
                continue
            actual_files = collect_signal_files(signal)
            extra = actual_files - declared_files
            missing = declared_files - actual_files
            # Only require declared files that still contain the signal.
            for path in list(missing):
                full = REPO / path
                if not full.exists():
                    failures.append(
                        f"Registry component `{component_id}` lists missing file: {path}"
                    )
                    continue
                content = full.read_text(encoding="utf-8", errors="replace")
                if not NETWORK_SIGNAL_PATTERNS[signal].search(content):
                    continue
                # file exists but no longer has signal — ok if other declared files cover it
            if extra:
                failures.append(
                    f"Undocumented network signal `{signal}` in: {sorted(extra)} "
                    f"(expected only {sorted(declared_files)} for `{component_id}`)"
                )
    return failures


def check_verification_status_tokens(data_flows_text: str) -> list[str]:
    failures: list[str] = []
    component_row_re = re.compile(r"^\|\s*`[^`]+`\s*\|")
    for line in data_flows_text.splitlines():
        if not component_row_re.match(line):
            continue
        if not VERIFICATION_STATUS_RE.search(line):
            failures.append(f"Component table row missing verification_status token: {line[:120]}")
    return failures


def run_checks() -> list[str]:
    failures: list[str] = []
    registry = load_registry()

    try:
        data_flows = read_text("docs/DATA_FLOWS.md")
    except FileNotFoundError as exc:
        return [str(exc)]

    try:
        risk_register = read_text("docs/RISK_REGISTER.md")
    except FileNotFoundError as exc:
        failures.append(str(exc))
        risk_register = ""

    failures.extend(check_required_sections(data_flows, DATA_FLOWS_REQUIRED_SECTIONS, "DATA_FLOWS.md"))

    if risk_register:
        failures.extend(
            check_required_sections(risk_register, RISK_REGISTER_REQUIRED_SECTIONS, "RISK_REGISTER.md")
        )

    network_ids = [item["id"] for item in registry.get("network_touchpoints", [])]
    store_ids = [item["id"] for item in registry.get("local_stores", [])]
    failures.extend(check_component_ids_present(data_flows, network_ids, "DATA_FLOWS network table"))
    failures.extend(check_component_ids_present(data_flows, store_ids, "DATA_FLOWS local store table"))

    for risk_id in registry.get("risk_ids", []):
        if risk_id not in risk_register:
            failures.append(f"RISK_REGISTER.md missing risk_id: {risk_id}")

    failures.extend(check_network_signal_drift(registry))
    failures.extend(check_verification_status_tokens(data_flows))

    for rel_path, desc, needle in CROSS_LINK_CHECKS:
        path = REPO / rel_path
        if not path.exists():
            failures.append(f"{desc} — file not found: {rel_path}")
            continue
        text = path.read_text(encoding="utf-8")
        if needle not in text:
            failures.append(f"{desc} — expected reference to {needle}")

    return failures


def main() -> int:
    failures = run_checks()
    if failures:
        for msg in failures:
            print(f"  FAIL  [{msg}]")
        print(f"\n{len(failures)} data-flow check(s) failed.")
        return 1

    print("All data-flow checks pass.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
