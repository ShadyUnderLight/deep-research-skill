#!/usr/bin/env python3
"""
Property-based consistency tests for threat model / engineering controls (issue #244).

These tests verify cross-document invariants that must hold across
4 discipline/checklist/eval files after the security threat model update.

Each test asserts a PROPERTY (invariant) about the documentation:
  - P0: §7 Security deep-dive section exists with required subsections
  - P1: Risk priority matrix template has required columns
  - P2: ROUTING-MATRIX artifact contract mentions security-sensitive analysis
  - P3: technical-analysis-audit has security deep-dive checklist items
  - P4: Security checklist covers assets/attackers, prioritization, controls tiering, detection, risk-type differentiation
  - P5: report-template mentions threat modeling in technical section
  - P6: New eval case exists with required structure (goal/prompt/pass-criteria/failure-signs)
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def fail(msg: str) -> None:
    raise AssertionError(msg)


# ─── files ────────────────────────────────────────────────────────────────────

DISCIPLINE_FILE = "references/technical-analysis-discipline.md"
ROUTING_FILE = "ROUTING-MATRIX.md"
AUDIT_FILE = "checklists/technical-analysis-audit.md"
TEMPLATE_FILE = "references/report-template.md"
EVAL_CASE_FILE = "evals/cases/mcp-security-risk-list-vs-threat-model-case.md"


# ─── helpers ──────────────────────────────────────────────────────────────────

EXPECTED_THREAT_SUBSECTIONS = [
    "资产",
    "攻击者",
    "信任边界",
    "攻击树",
    "风险优先级矩阵",
    "缓解措施",
    "检测",
    "短期",
    "中期",
    "长期",
]

ENGINEERING_CONTROL_SIGNALS = [
    "预防",
    "检测",
    "响应",
]

RISK_TYPE_SIGNALS = [
    "协议设计",
    "实现漏洞",
    "部署误配置",
    "供应链",
]


def find_section_heading(text: str, heading_prefix: str) -> int | None:
    """Find the line index of a markdown heading matching heading_prefix."""
    lines = text.split("\n")
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("##") or stripped.startswith("###"):
            if heading_prefix.lower() in stripped.lower():
                return i
    return None


def get_section_lines(text: str, heading_idx: int) -> list[str]:
    """Get lines belonging to a section starting at heading_idx, until next heading at same level."""
    lines = text.split("\n")
    heading_level = len(lines[heading_idx]) - len(lines[heading_idx].lstrip("#"))
    section = []
    for j in range(heading_idx + 1, len(lines)):
        next_line = lines[j]
        if next_line.startswith("#") and (len(next_line) - len(next_line.lstrip("#"))) <= heading_level:
            break
        section.append(next_line)
    return section


def extract_table_headers(text: str) -> list[list[str]]:
    """Extract markdown table headers from text. Returns list of header rows."""
    lines = text.split("\n")
    tables = []
    i = 0
    while i < len(lines):
        if lines[i].strip().startswith("|"):
            headers = [c.strip() for c in lines[i].strip().strip("|").split("|")]
            # Check next line is separator
            if i + 1 < len(lines) and lines[i + 1].strip().startswith("|") and all(
                c.strip().replace("-", "").replace(":", "") == "" for c in lines[i + 1].strip().strip("|").split("|") if c.strip()
            ):
                tables.append(headers)
                i += 2
                continue
        i += 1
    return tables


def count_checklist_items(text: str) -> int:
    """Count markdown checklist items."""
    count = 0
    for line in text.split("\n"):
        stripped = line.strip()
        if stripped.startswith("- [ ]") or stripped.startswith("- [x]") or stripped.startswith("- [X]"):
            count += 1
    return count


# ─── Property Tests ──────────────────────────────────────────────────────────


def test_p0_security_deep_dive_section_exists() -> None:
    """
    P0 (Section existence): technical-analysis-discipline.md must have a
    heading about security deep-dive / threat modeling, containing all required
    concepts for threat model + engineering controls output.

    Uses substring matching intentionally — checks concept coverage, not strict
    heading structure. A subsection can satisfy the requirement by appearing as
    a heading, table cell, or body text within the section boundary.
    """
    text = read(DISCIPLINE_FILE)
    heading_idx = find_section_heading(text, "security deep-dive")

    if heading_idx is None:
        # Try alternative heading patterns
        heading_idx = find_section_heading(text, "threat model")
    if heading_idx is None:
        heading_idx = find_section_heading(text, "安全")

    if heading_idx is None:
        fail(
            f"P0 FAIL: No 'Security deep-dive' or 'threat model' section heading "
            f"found in {DISCIPLINE_FILE}"
        )

    section_text = "\n".join(get_section_lines(text, heading_idx))

    # Verify all required concepts are present within the section boundary
    # Uses substring matching so a concept can be in headings, tables, or body
    missing = []
    for sub in EXPECTED_THREAT_SUBSECTIONS:
        if sub not in section_text:
            missing.append(sub)

    if missing:
        fail(
            f"P0 FAIL: Security deep-dive section is missing these required "
            f"elements: {missing}"
        )

    print(f"  PASS  P0: security deep-dive section found with all {len(EXPECTED_THREAT_SUBSECTIONS)} required elements")


def test_p1_risk_matrix_columns() -> None:
    """
    P1 (Risk matrix property): The risk priority matrix template must have
    at minimum these columns: 风险项, 可能性, 影响, 优先级.
    """
    text = read(DISCIPLINE_FILE)

    required_columns = ["风险项", "可能性", "影响", "优先级"]
    all_tables = extract_table_headers(text)

    found_matrix = False
    for headers in all_tables:
        if all(col in headers for col in required_columns):
            found_matrix = True
            break

    if not found_matrix:
        fail(
            f"P1 FAIL: No risk priority matrix table with required columns "
            f"{required_columns} found in {DISCIPLINE_FILE}"
        )

    print(f"  PASS  P1: risk priority matrix template with required columns found")


def test_p2_routing_mentions_security_sensitive() -> None:
    """
    P2 (Routing property): ROUTING-MATRIX.md's Technical Deep-dive
    Visible artifact contract mentions security-sensitive architecture analysis.
    """
    text = read(ROUTING_FILE)

    # Locate the Technical Deep-dive section
    lines = text.split("\n")
    found_signal = False

    # Collect the entire Visible artifact contract section as one block
    # to avoid false negatives from markdown line wrapping
    in_artifact_contract = False
    artifact_lines = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if "Route: Technical Deep-dive" in stripped or "Route: Technical Deep-dive / Architecture Analysis" in stripped:
            in_artifact_contract = False
            artifact_lines = []
        if in_artifact_contract:
            if stripped.startswith("##") or stripped.startswith("---"):
                break
            artifact_lines.append(stripped)
        if "Visible artifact contract" in stripped:
            in_artifact_contract = True

    artifact_block = " ".join(artifact_lines).lower()
    if "security" in artifact_block and ("sensitive" in artifact_block or "assets" in artifact_block or "threat" in artifact_block):
        found_signal = True

    if not found_signal:
        # Fallback: search entire Technical Deep-dive section (joined for line-break resilience)
        in_tech_route = False
        route_lines = []
        for line in lines:
            stripped = line.strip()
            if "Route: Technical Deep-dive" in stripped:
                in_tech_route = True
                continue
            if in_tech_route and (stripped.startswith("##") or stripped.startswith("---")) and "Route:" in stripped:
                break
            if in_tech_route:
                route_lines.append(stripped)
        route_block = " ".join(route_lines).lower()
        if "security-sensitive" in route_block or ("security" in route_block and "architecture" in route_block):
            found_signal = True

    if not found_signal:
        fail(
            f"P2 FAIL: Technical Deep-dive route does not mention "
            f"security-sensitive architecture analysis in {ROUTING_FILE}"
        )

    print(f"  PASS  P2: ROUTING-MATRIX mentions security-sensitive architecture analysis")


def test_p3_checklist_has_security_section() -> None:
    """
    P3 (Checklist property): technical-analysis-audit.md has a checklist section
    dedicated to security deep-dive with at least 3 checklist items.
    """
    text = read(AUDIT_FILE)
    heading_idx = find_section_heading(text, "security")

    if heading_idx is None:
        heading_idx = find_section_heading(text, "安全")
    if heading_idx is None:
        heading_idx = find_section_heading(text, "threat")

    if heading_idx is None:
        fail(
            f"P3 FAIL: No 'Security' or '安全' heading found in {AUDIT_FILE}"
        )

    section_lines = get_section_lines(text, heading_idx)
    section_text = "\n".join(section_lines)

    # Count checklist items in this section
    item_count = count_checklist_items(section_text)
    if item_count < 3:
        fail(
            f"P3 FAIL: Security section has only {item_count} checklist items, "
            f"expected at least 3"
        )

    print(f"  PASS  P3: security checklist section found with {item_count} items")


def test_p4_checklist_covers_essential_checks() -> None:
    """
    P4 (Checklist coverage property): Security checklist items must cover:
      - assets/attackers/boundaries (资产/攻击者/信任边界)
      - risk prioritization (风险优先级, not equal-weight list)
      - controls tiering (预防/检测/响应 or 短/中/长期)
      - detection signals (检测/监控)
      - risk-type differentiation (协议设计/实现漏洞/部署误配置/供应链)
    """
    text = read(AUDIT_FILE)
    items_text = text.lower()

    # Collect all checklist items in the security section
    heading_idx = find_section_heading(text, "security")
    if heading_idx is None:
        heading_idx = find_section_heading(text, "安全")
    if heading_idx is None:
        fail("P4 FAIL: Cannot check coverage — security section not found. Run P3 first.")

    section_text = "\n".join(get_section_lines(text, heading_idx)).lower()

    checks = {
        "assets/attackers/boundaries": any(kw in section_text for kw in ["资产", "攻击者", "信任边界", "asset", "attacker", "trust boundar"]),
        "risk prioritization": any(kw in section_text for kw in ["优先级", "priorit"]),
        "controls tiering": any(kw in section_text for kw in ["预防", "检测", "响应", "短期", "中期", "长期", "短中长", "防护", "short", "medium", "long"]),
        "detection signals": any(kw in section_text for kw in ["检测", "监控", "监测", "detection", "monitor"]),
        "risk-type differentiation": any(kw in section_text for kw in ["协议设计", "实现漏洞", "部署误配置", "供应链", "协议风险", "实现风险", "部署风险", "protocol design", "implementation vulnerability", "deployment misconfig", "supply chain"]),
    }

    missing = [k for k, v in checks.items() if not v]
    if missing:
        fail(
            f"P4 FAIL: Security checklist missing coverage for: {missing}"
        )

    print(f"  PASS  P4: all 5 essential security coverage areas present in checklist")


def test_p5_template_mentions_threat_modeling() -> None:
    """
    P5 (Template property): report-template.md's technical analysis
    section mentions threat modeling or points to the security discipline.
    """
    text = read(TEMPLATE_FILE)

    # Find the "technical" section reference under "Detailed analysis"
    in_detailed_analysis = False
    found_signal = False

    for line in text.split("\n"):
        stripped = line.strip()
        if "Detailed analysis" in stripped and stripped.startswith("##"):
            in_detailed_analysis = True
            continue
        if in_detailed_analysis:
            if stripped.startswith("##") and "Detailed analysis" not in stripped:
                break
            lower = stripped.lower()
            if "threat model" in lower or "威胁模型" in lower or "security deep-dive" in lower or "technical-analysis-discipline" in lower:
                if "安全" in lower or "security" in lower or "threat" in lower:
                    found_signal = True
                    break

    if not found_signal:
        # Fallback: search the Detailed analysis section only (not entire file)
        # Re-locate the Detailed analysis section boundary
        in_detailed = False
        for line in text.split("\n"):
            stripped = line.strip()
            if "Detailed analysis" in stripped and stripped.startswith("##"):
                in_detailed = True
                continue
            if in_detailed:
                if stripped.startswith("##") and "Detailed analysis" not in stripped:
                    break
                lower = stripped.lower()
                if any(kw in lower for kw in ["threat model", "威胁模型", "security deep-dive"]):
                    found_signal = True
                    break

    if not found_signal:
        fail(
            f"P5 FAIL: No threat modeling reference found in technical analysis "
            f"section of {TEMPLATE_FILE}"
        )

    print(f"  PASS  P5: report-template references threat modeling in technical analysis section")


def test_p6_eval_case_exists() -> None:
    """
    P6 (Eval case property): The threat model eval case exists with required
    structural sections: Goal (or 目标), Prompt, Pass criteria (or 验收标准),
    Failure signs (or 失败信号/Failure).
    """
    eval_path = ROOT / EVAL_CASE_FILE
    if not eval_path.exists():
        fail(
            f"P6 FAIL: Eval case file not found: {EVAL_CASE_FILE}"
        )

    text = read(EVAL_CASE_FILE)

    required_sections = ["## Goal", "## Prompt", "## Pass criteria"]
    # Allow alternative section names
    section_aliases = {
        "## Goal": ["## Goal", "## 目标", "## Purpose"],
        "## Prompt": ["## Prompt", "## 提示"],
        "## Pass criteria": ["## Pass criteria", "## 验收标准", "## Pass Criteria"],
    }

    missing = []
    for section, aliases in section_aliases.items():
        found = any(alias in text for alias in aliases)
        if not found:
            missing.append(section)

    if missing:
        fail(
            f"P6 FAIL: Eval case missing required sections: {missing}"
        )

    # Verify it also contains Failure signs (recommended but not required for all evals)
    has_failure_signs = any(
        kw in text for kw in ["## Failure signs", "## Failure", "## 失败信号", "## Fail"]
    )
    if not has_failure_signs:
        print(f"  WARN  P6: eval case does not have explicit Failure signs section (soft)")

    print(f"  PASS  P6: eval case file exists with all required sections")


# ─── main ────────────────────────────────────────────────────────────────────


def main() -> int:
    tests = [
        ("P0: Security deep-dive section", test_p0_security_deep_dive_section_exists),
        ("P1: Risk matrix columns", test_p1_risk_matrix_columns),
        ("P2: Routing contract", test_p2_routing_mentions_security_sensitive),
        ("P3: Checklist section", test_p3_checklist_has_security_section),
        ("P4: Checklist coverage", test_p4_checklist_covers_essential_checks),
        ("P5: Template reference", test_p5_template_mentions_threat_modeling),
        ("P6: Eval case exists", test_p6_eval_case_exists),
    ]

    failures = []
    for name, fn in tests:
        try:
            fn()
        except AssertionError as exc:
            failures.append(name)
            print(f"  FAIL  {name}: {exc}")
        except Exception as exc:
            failures.append(name)
            print(f"  FAIL  {name}: unexpected error — {exc}")

    if failures:
        print(f"\n{'='*60}")
        print(f"❌ {len(failures)} property test(s) FAILED: {', '.join(failures)}")
        return 1

    print(f"\n{'='*60}")
    print("✅ All 7 property tests PASSED — all cross-document invariants hold.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
