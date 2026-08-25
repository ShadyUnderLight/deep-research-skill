#!/usr/bin/env python3
"""Validate data-flow documentation against the machine-readable registry.

Checks:
  1. docs/DATA_FLOWS.md and docs/RISK_REGISTER.md exist with required sections
  2. Every registry network touchpoint and local store appears in DATA_FLOWS.md
  3. Every registry risk_id appears in RISK_REGISTER.md
  4. Repo-owned network/write signal files match the registry (drift detection)
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

COMPONENT_TABLE_COLUMNS = 9
ALLOWED_VERIFICATION_STATUSES = {"measured", "asserted", "not_run", "unknown"}

NETWORK_SIGNAL_PATTERNS: dict[str, re.Pattern[str]] = {
    "async_playwright": re.compile(r"async_playwright"),
    "gh_cli": re.compile(
        r"subprocess\.run\(\s*\[\s*[\"']gh[\"']"
        r"|\bgh\s+api\b"
        r"|\bgh\s+issue\b"
        r"|\bgh\s+pr\b"
    ),
}

WRITE_SIGNAL_PATTERNS: dict[str, re.Pattern[str]] = {
    "delivery_temp_dir": re.compile(
        r'tempfile\.TemporaryDirectory\(\s*prefix\s*=\s*["\']deep-research-delivery-'
    ),
    "markdown_html_write": re.compile(r"out_path\.write_text\(\s*full_html"),
    "delivery_status_write": re.compile(r"write_delivery_status\("),
    "route_cards_write": re.compile(
        r"ROUTE_INDEX_PATH\.write_text|target\.write_text\(\s*content"
    ),
    "validator_named_tempfile": re.compile(r"tempfile\.NamedTemporaryFile\("),
    "test_tempfile": re.compile(
        r"tempfile\.(?:TemporaryDirectory|NamedTemporaryFile)\("
    ),
    "pdf_regression_temp": re.compile(
        r'tempfile\.TemporaryDirectory\(\s*prefix\s*=\s*["\']pdf-regression-'
    ),
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

SKIP_SCAN_FILES = {
    "scripts/validate_data_flows.py",
}


def load_registry() -> dict:
    if not REGISTRY_PATH.exists():
        raise FileNotFoundError(f"Registry not found: {REGISTRY_PATH}")
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def read_text(rel_path: str) -> str:
    path = REPO / rel_path
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")
    return path.read_text(encoding="utf-8")


def expand_source_files(store: dict) -> set[str]:
    files: set[str] = set(store.get("source_files", []))
    for pattern in store.get("source_globs", []):
        for path in REPO.glob(pattern):
            if path.is_file():
                files.add(path.relative_to(REPO).as_posix())
    return files


def iter_scan_paths(*, include_tests: bool) -> list[Path]:
    roots = [REPO / "scripts"]
    paths: list[Path] = []
    for root in roots:
        if not root.exists():
            continue
        for path in root.rglob("*.py"):
            rel = path.relative_to(REPO).as_posix()
            if rel in SKIP_SCAN_FILES:
                continue
            if rel.startswith("scripts/test_"):
                if include_tests:
                    paths.append(path)
                continue
            if not include_tests and rel.startswith("scripts/test_"):
                continue
            paths.append(path)
    return paths


def collect_signal_files(
    signal: str,
    patterns: dict[str, re.Pattern[str]],
    *,
    include_tests: bool,
    tests_only: bool = False,
) -> set[str]:
    pattern = patterns[signal]
    matches: set[str] = set()
    for path in iter_scan_paths(include_tests=include_tests):
        rel = path.relative_to(REPO).as_posix()
        if tests_only and not rel.startswith("scripts/test_"):
            continue
        content = path.read_text(encoding="utf-8", errors="replace")
        if pattern.search(content):
            matches.add(rel)
    return matches


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


def should_enforce_network_drift(touchpoint: dict) -> bool:
    if touchpoint.get("enforcement") == "out_of_repo":
        return False
    return bool(touchpoint.get("network_signals"))


def check_network_signal_drift(registry: dict) -> list[str]:
    failures: list[str] = []
    for touchpoint in registry.get("network_touchpoints", []):
        if not should_enforce_network_drift(touchpoint):
            continue
        component_id = touchpoint["id"]
        declared_files = set(touchpoint.get("source_files", []))
        for signal in touchpoint.get("network_signals", []):
            if signal not in NETWORK_SIGNAL_PATTERNS:
                failures.append(
                    f"Registry component `{component_id}` references unknown network signal: {signal}"
                )
                continue
            actual_files = collect_signal_files(
                signal, NETWORK_SIGNAL_PATTERNS, include_tests=False
            )
            extra = actual_files - declared_files
            for path in declared_files:
                full = REPO / path
                if not full.exists():
                    failures.append(
                        f"Registry component `{component_id}` lists missing file: {path}"
                    )
            if extra:
                failures.append(
                    f"Undocumented network signal `{signal}` in: {sorted(extra)} "
                    f"(expected only {sorted(declared_files)} for `{component_id}`)"
                )
    return failures


def check_local_store_write_drift(registry: dict) -> list[str]:
    failures: list[str] = []
    signal_owners: dict[str, tuple[str, set[str], bool, bool]] = {}

    for store in registry.get("local_stores", []):
        enforcement = store.get("enforcement", "registry_enforced")
        if enforcement == "documentation_only":
            continue

        store_id = store["id"]
        declared_files = expand_source_files(store)
        include_tests = store.get("kind") == "test_only"

        for path in declared_files:
            if not (REPO / path).exists():
                failures.append(
                    f"Registry local store `{store_id}` lists missing file: {path}"
                )

        for path_signal in store.get("path_signals", []):
            for path in declared_files:
                content = (REPO / path).read_text(encoding="utf-8", errors="replace")
                if path_signal not in content:
                    failures.append(
                        f"Registry local store `{store_id}` path_signal `{path_signal}` "
                        f"not found in {path}"
                    )

        for signal in store.get("write_signals", []):
            if signal not in WRITE_SIGNAL_PATTERNS:
                failures.append(
                    f"Registry local store `{store_id}` references unknown write signal: {signal}"
                )
                continue
            tests_only = signal == "test_tempfile"
            signal_owners[signal] = (store_id, declared_files, include_tests, tests_only)

    for signal, (store_id, declared_files, include_tests, tests_only) in signal_owners.items():
        actual_files = collect_signal_files(
            signal,
            WRITE_SIGNAL_PATTERNS,
            include_tests=include_tests,
            tests_only=tests_only,
        )
        extra = actual_files - declared_files
        if extra:
            failures.append(
                f"Undocumented write signal `{signal}` in: {sorted(extra)} "
                f"(expected only {sorted(declared_files)} for local store `{store_id}`)"
            )

    for signal in WRITE_SIGNAL_PATTERNS:
        if signal in signal_owners:
            continue
        actual_files = collect_signal_files(
            signal, WRITE_SIGNAL_PATTERNS, include_tests=False
        )
        if actual_files:
            failures.append(
                f"Write signal `{signal}` is not assigned to any local store but appears in: "
                f"{sorted(actual_files)}"
            )

    return failures


def parse_component_table_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def check_verification_status_tokens(data_flows_text: str) -> list[str]:
    failures: list[str] = []
    component_row_re = re.compile(r"^\|\s*`[^`]+`\s*\|")
    for line in data_flows_text.splitlines():
        if not component_row_re.match(line):
            continue
        cells = parse_component_table_row(line)
        if len(cells) != COMPONENT_TABLE_COLUMNS:
            failures.append(
                f"Component table row has {len(cells)} columns, expected "
                f"{COMPONENT_TABLE_COLUMNS}: {line[:120]}"
            )
            continue
        status = cells[-1].lower()
        if status not in ALLOWED_VERIFICATION_STATUSES:
            failures.append(
                f"Component table row has invalid verification_status `{cells[-1]}`: "
                f"{line[:120]}"
            )
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
    failures.extend(check_local_store_write_drift(registry))
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
