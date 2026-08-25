#!/usr/bin/env python3
"""Validate data-flow documentation against the machine-readable registry.

Checks:
  1. docs/DATA_FLOWS.md and docs/RISK_REGISTER.md exist with required sections
  2. Every registry network touchpoint and local store has a valid DATA_FLOWS table row
  3. Every registry risk_id has a structured RISK_REGISTER entry with required fields
  4. Repo-owned network/write signal files match the registry (bidirectional drift detection)
  5. Cross-links from README, SKILL.md, and external-channel-preflight.md

Automatic drift scanning is limited to `scripts/**/*.py` (excluding `scripts/validate_data_flows.py`
and, for production-network checks, `scripts/test_*.py`). It does not scan the whole repository.

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

RISK_REQUIRED_FIELDS = [
    "description",
    "affected_boundary",
    "existing_controls",
    "evidence_status",
    "residual_gap",
    "next_validation",
    "owner_layer",
]

COMPONENT_ROW_ID_RE = re.compile(r"^\|\s*`([^`]+)`\s*\|", re.MULTILINE)
RISK_ENTRY_RE = re.compile(
    r"^## (RISK-[^\s]+)\s*$([\s\S]*?)(?=^## |\Z)",
    re.MULTILINE,
)
RISK_FIELD_RE = re.compile(
    r"^-\s+\*\*(description|affected_boundary|existing_controls|evidence_status|residual_gap|next_validation|owner_layer):\*\*\s*(.+)$",
    re.MULTILINE,
)

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


def expand_glob_patterns(patterns: list[str]) -> set[str]:
    files: set[str] = set()
    for pattern in patterns:
        for path in REPO.glob(pattern):
            if path.is_file():
                files.add(path.relative_to(REPO).as_posix())
    return files


def expected_signal_files(entry: dict, signal: str) -> set[str]:
    signal_files = entry.get("signal_files", {})
    if signal in signal_files:
        return set(signal_files[signal])
    return set()


def allowed_signal_files(entry: dict, signal: str) -> set[str]:
    allowed = expected_signal_files(entry, signal)
    scan_globs = entry.get("signal_scan_globs", {})
    if signal in scan_globs:
        allowed |= expand_glob_patterns(scan_globs[signal])
    return allowed


def check_signal_file_drift(
    *,
    label: str,
    signal: str,
    patterns: dict[str, re.Pattern[str]],
    expected_files: set[str],
    allowed_files: set[str],
    include_tests: bool,
    tests_only: bool,
) -> list[str]:
    failures: list[str] = []
    if signal not in patterns:
        failures.append(f"{label} references unknown signal: {signal}")
        return failures

    actual_files = collect_signal_files(
        signal,
        patterns,
        include_tests=include_tests,
        tests_only=tests_only,
    )
    extra = actual_files - allowed_files
    missing = expected_files - actual_files

    if extra:
        failures.append(
            f"Undocumented signal `{signal}` in: {sorted(extra)} "
            f"(allowed only {sorted(allowed_files)} for {label})"
        )
    if missing:
        failures.append(
            f"Registered signal `{signal}` no longer present in: {sorted(missing)} "
            f"(still declared for {label})"
        )

    for path in sorted(expected_files):
        full = REPO / path
        if not full.exists():
            failures.append(f"{label} lists missing registered file: {path}")
            continue
        content = full.read_text(encoding="utf-8", errors="replace")
        if not patterns[signal].search(content):
            failures.append(
                f"Registered signal `{signal}` pattern missing from {path} ({label})"
            )

    return failures


def extract_section(text: str, heading: str) -> str:
    start = text.find(heading)
    if start == -1:
        return ""
    rest = text[start + len(heading) :]
    next_heading = re.search(r"\n## ", rest)
    if next_heading:
        return rest[: next_heading.start()]
    return rest


def parse_component_table_ids(section_text: str) -> set[str]:
    return set(COMPONENT_ROW_ID_RE.findall(section_text))


def check_data_flow_component_tables(data_flows_text: str, registry: dict) -> list[str]:
    failures: list[str] = []
    network_section = extract_section(data_flows_text, "## Network touchpoints")
    store_section = extract_section(data_flows_text, "## Local stores")

    network_table_ids = parse_component_table_ids(network_section)
    store_table_ids = parse_component_table_ids(store_section)

    expected_network = {item["id"] for item in registry.get("network_touchpoints", [])}
    expected_stores = {item["id"] for item in registry.get("local_stores", [])}

    missing_network = expected_network - network_table_ids
    missing_stores = expected_stores - store_table_ids
    extra_network = network_table_ids - expected_network
    extra_stores = store_table_ids - expected_stores
    if missing_network:
        failures.append(
            "DATA_FLOWS network table missing component rows: "
            f"{sorted(missing_network)}"
        )
    if missing_stores:
        failures.append(
            "DATA_FLOWS local store table missing component rows: "
            f"{sorted(missing_stores)}"
        )
    if extra_network:
        failures.append(
            "DATA_FLOWS network table has undeclared component rows: "
            f"{sorted(extra_network)}"
        )
    if extra_stores:
        failures.append(
            "DATA_FLOWS local store table has undeclared component rows: "
            f"{sorted(extra_stores)}"
        )

    failures.extend(check_verification_status_tokens(data_flows_text))
    return failures


def parse_risk_entry_fields(risk_text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for match in RISK_FIELD_RE.finditer(risk_text):
        fields[match.group(1)] = match.group(2).strip()
    return fields


def parse_risk_headings(risk_register: str) -> set[str]:
    return {match.group(1) for match in RISK_ENTRY_RE.finditer(risk_register)}


def check_risk_register_entries(risk_register: str, risk_ids: list[str]) -> list[str]:
    failures: list[str] = []
    expected_risk_ids = set(risk_ids)
    actual_risk_ids = parse_risk_headings(risk_register)

    missing_risk_ids = expected_risk_ids - actual_risk_ids
    extra_risk_ids = actual_risk_ids - expected_risk_ids
    if missing_risk_ids:
        failures.append(
            "RISK_REGISTER.md missing risk headings: " f"{sorted(missing_risk_ids)}"
        )
    if extra_risk_ids:
        failures.append(
            "RISK_REGISTER.md has undeclared risk headings: "
            f"{sorted(extra_risk_ids)}"
        )

    for risk_id in risk_ids:
        match = re.search(
            rf"^## {re.escape(risk_id)}\s*$([\s\S]*?)(?=^## |\Z)",
            risk_register,
            re.MULTILINE,
        )
        if not match:
            continue
        fields = parse_risk_entry_fields(match.group(1))
        for field in RISK_REQUIRED_FIELDS:
            if field not in fields or not fields[field]:
                failures.append(f"RISK_REGISTER.md `{risk_id}` missing field: {field}")
        status = fields.get("evidence_status", "").lower()
        if status and status not in ALLOWED_VERIFICATION_STATUSES:
            failures.append(
                f"RISK_REGISTER.md `{risk_id}` invalid evidence_status: "
                f"{fields.get('evidence_status')}"
            )
    return failures


def registered_network_signals(registry: dict) -> set[str]:
    registered: set[str] = set()
    for touchpoint in registry.get("network_touchpoints", []):
        if should_enforce_network_drift(touchpoint):
            registered.update(touchpoint.get("network_signals", []))
    return registered


def check_unassigned_network_signals(registry: dict) -> list[str]:
    failures: list[str] = []
    registered = registered_network_signals(registry)
    for signal in NETWORK_SIGNAL_PATTERNS:
        if signal in registered:
            continue
        actual_files = collect_signal_files(
            signal, NETWORK_SIGNAL_PATTERNS, include_tests=False
        )
        if actual_files:
            failures.append(
                f"Network signal `{signal}` is not assigned to any touchpoint but appears in: "
                f"{sorted(actual_files)}"
            )
    return failures


def check_required_sections(text: str, sections: list[str], label: str) -> list[str]:
    failures: list[str] = []
    for section in sections:
        if section not in text:
            failures.append(f"{label} missing section: {section}")
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
        label = f"network touchpoint `{component_id}`"
        for path in touchpoint.get("source_files", []):
            if not (REPO / path).exists():
                failures.append(f"Registry component `{component_id}` lists missing file: {path}")
        for signal in touchpoint.get("network_signals", []):
            failures.extend(
                check_signal_file_drift(
                    label=label,
                    signal=signal,
                    patterns=NETWORK_SIGNAL_PATTERNS,
                    expected_files=expected_signal_files(touchpoint, signal),
                    allowed_files=allowed_signal_files(touchpoint, signal),
                    include_tests=False,
                    tests_only=False,
                )
            )
    failures.extend(check_unassigned_network_signals(registry))
    return failures


def check_local_store_write_drift(registry: dict) -> list[str]:
    failures: list[str] = []
    assigned_write_signals: set[str] = set()

    for store in registry.get("local_stores", []):
        enforcement = store.get("enforcement", "registry_enforced")
        if enforcement == "documentation_only":
            continue

        store_id = store["id"]
        label = f"local store `{store_id}`"
        declared_files = expand_source_files(store)
        include_tests = store.get("kind") == "test_only"

        for path in declared_files:
            if not (REPO / path).exists():
                failures.append(f"Registry local store `{store_id}` lists missing file: {path}")

        for path_signal in store.get("path_signals", []):
            for path in store.get("source_files", []):
                content = (REPO / path).read_text(encoding="utf-8", errors="replace")
                if path_signal not in content:
                    failures.append(
                        f"Registry local store `{store_id}` path_signal `{path_signal}` "
                        f"not found in {path}"
                    )

        for signal in store.get("write_signals", []):
            assigned_write_signals.add(signal)
            failures.extend(
                check_signal_file_drift(
                    label=label,
                    signal=signal,
                    patterns=WRITE_SIGNAL_PATTERNS,
                    expected_files=expected_signal_files(store, signal),
                    allowed_files=allowed_signal_files(store, signal),
                    include_tests=include_tests,
                    tests_only=signal == "test_tempfile",
                )
            )

    for signal in WRITE_SIGNAL_PATTERNS:
        if signal in assigned_write_signals:
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

    if not risk_register.strip():
        failures.append("RISK_REGISTER.md is empty")
    else:
        failures.extend(
            check_required_sections(
                risk_register, RISK_REGISTER_REQUIRED_SECTIONS, "RISK_REGISTER.md"
            )
        )
        failures.extend(
            check_risk_register_entries(risk_register, registry.get("risk_ids", []))
        )

    failures.extend(check_data_flow_component_tables(data_flows, registry))

    failures.extend(check_network_signal_drift(registry))
    failures.extend(check_local_store_write_drift(registry))

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
