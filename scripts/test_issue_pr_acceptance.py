#!/usr/bin/env python3
"""
Property-based contract tests for validate_issue_pr_acceptance.

Invariants tested:
  C1 (NO_OP_MERGE): identical merge/parent SHA → NO_OP_MERGE error
  C2 (MISSING_FILE): issue checklist path not in PR files → MISSING_FILE error
  C3 (PASS): no checklist paths + valid merge → empty findings
  C4 (NO_CRASH): empty/malformed input → no crash, graceful handling
  C5 (PATH_EXTRACTION): only checklist `- [ ] ` paths extracted, not body prose

Usage:
    python3 scripts/test_issue_pr_acceptance.py

Expected: ALL PASS
"""

from __future__ import annotations

import sys
import os
from pathlib import Path

# ── Ensure the sibling module is importable ────────────────────────────────
_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

# ── Import the validation module ───────────────────────────────────────────
# We import after path fix; if module doesn't exist yet, the test
# framework itself will fail (RED phase).
try:
    from validate_issue_pr_acceptance import (
        core_validate,
        extract_issue_paths,
        ValidationFinding,
        EXIT_UNAVAILABLE,
    )
except ImportError:
    # In RED phase before implementation exists, define stubs so tests
    # can at least be syntactically verified to fail for the right reason.
    from dataclasses import dataclass
    @dataclass
    class ValidationFinding:
        severity: str
        code: str
        message: str
        detail: str

    def core_validate(issue_body="", pr_files=None, pr_merge_tree_sha=None, pr_parent_tree_sha=None):
        raise NotImplementedError("RED phase — implement me")

    def extract_issue_paths(body: str) -> list[str]:
        raise NotImplementedError("RED phase — implement me")


# ═══════════════════════════════════════════════════════════════════════════
# C1: NO-OP MERGE DETECTION
# ═══════════════════════════════════════════════════════════════════════════

def test_c1_detects_no_op_merge():
    """C1: Identical merge/parent SHA MUST produce NO_OP_MERGE error."""
    findings = core_validate(
        issue_body="## Acceptance\n- [x] done",
        pr_files=["file1.py"],
        pr_merge_tree_sha="abc123",
        pr_parent_tree_sha="abc123",
    )
    codes = [f.code for f in findings]
    assert "NO_OP_MERGE" in codes, (
        f"Expected NO_OP_MERGE in findings, got {codes}"
    )


def test_c1_skips_when_different():
    """C1: Different merge/parent SHA MUST NOT produce NO_OP_MERGE."""
    findings = core_validate(
        issue_body="## Acceptance\n- [x] done",
        pr_files=["file1.py"],
        pr_merge_tree_sha="abc123",
        pr_parent_tree_sha="def456",
    )
    codes = [f.code for f in findings]
    assert "NO_OP_MERGE" not in codes, (
        f"Unexpected NO_OP_MERGE with different SHAs: {codes}"
    )


def test_c1_skips_when_none():
    """C1: None SHA MUST NOT produce NO_OP_MERGE (PR not merged yet)."""
    findings = core_validate(
        issue_body="## Acceptance\n- [x] done",
        pr_files=["file1.py"],
        pr_merge_tree_sha=None,
        pr_parent_tree_sha=None,
    )
    codes = [f.code for f in findings]
    assert "NO_OP_MERGE" not in codes, (
        f"Unexpected NO_OP_MERGE with None SHAs: {codes}"
    )


# ═══════════════════════════════════════════════════════════════════════════
# C2: MISSING FILE DETECTION
# ═══════════════════════════════════════════════════════════════════════════

SAMPLE_ISSUE_WITH_PATHS = """\
## Background
Some context.

## Acceptance Criteria
- [ ] `tests/test_issue_320_contracts.py` — verify contracts
- [ ] `references/report-template.md` — update template
- [ ] `checklists/market-outlook-audit.md` — add sections

## Notes
Additional details.
"""


def test_c2_detects_missing_file():
    """C2: Issue path not in PR files MUST produce MISSING_FILE for ALL."""
    findings = core_validate(
        issue_body=SAMPLE_ISSUE_WITH_PATHS,
        pr_files=["scripts/validate_report_quality.py"],
        pr_merge_tree_sha="abc123",
        pr_parent_tree_sha="def456",
    )
    missing = [f for f in findings if f.code == "MISSING_FILE"]
    flagged_paths = set(m.detail for m in missing)
    expected = {"tests/test_issue_320_contracts.py",
                "references/report-template.md",
                "checklists/market-outlook-audit.md"}
    # All three issue checklist paths must be flagged as missing
    assert expected.issubset(flagged_paths), (
        f"Expected ALL of {expected} flagged, got {flagged_paths}"
    )


def test_c2_all_files_present():
    """C2: All issue paths in PR files MUST NOT produce MISSING_FILE."""
    findings = core_validate(
        issue_body=SAMPLE_ISSUE_WITH_PATHS,
        pr_files=[
            "tests/test_issue_320_contracts.py",
            "references/report-template.md",
            "checklists/market-outlook-audit.md",
            "scripts/something_else.py",
        ],
        pr_merge_tree_sha="abc123",
        pr_parent_tree_sha="def456",
    )
    missing = [f for f in findings if f.code == "MISSING_FILE"]
    assert len(missing) == 0, (
        f"Expected no MISSING_FILE, got: {[(m.detail, m.message) for m in missing]}"
    )


def test_c2_empty_pr_files():
    """C2: Empty PR file list SHOULD flag ALL checklist paths."""
    findings = core_validate(
        issue_body=SAMPLE_ISSUE_WITH_PATHS,
        pr_files=[],
        pr_merge_tree_sha="abc123",
        pr_parent_tree_sha="def456",
    )
    missing = [f for f in findings if f.code == "MISSING_FILE"]
    flagged_paths = set(m.detail for m in missing)
    expected = {"tests/test_issue_320_contracts.py",
                "references/report-template.md",
                "checklists/market-outlook-audit.md"}
    assert expected.issubset(flagged_paths), (
        f"Expected ALL of {expected} flagged when PR files empty, got {flagged_paths}"
    )


# ═══════════════════════════════════════════════════════════════════════════
# C3: PASS — no checklist paths + valid merge
# ═══════════════════════════════════════════════════════════════════════════

ISSUE_NO_PATHS = """\
## Enhancement
Add a new validator.

## Acceptance Criteria
- [ ] Implement the feature
- [ ] All tests pass
"""


def test_c3_pass_no_checklist_paths():
    """C3: No checklist paths + valid merge → empty findings."""
    findings = core_validate(
        issue_body=ISSUE_NO_PATHS,
        pr_files=["scripts/new_validator.py"],
        pr_merge_tree_sha="abc123",
        pr_parent_tree_sha="def456",
    )
    assert len(findings) == 0, (
        f"Expected empty findings, got: {[(f.code, f.detail) for f in findings]}"
    )


# ═══════════════════════════════════════════════════════════════════════════
# C4: NO CRASH — graceful handling of edge inputs
# ═══════════════════════════════════════════════════════════════════════════

def test_c4_empty_issue_body():
    """C4: Empty issue body MUST NOT crash."""
    try:
        findings = core_validate(
            issue_body="",
            pr_files=["file.py"],
            pr_merge_tree_sha="abc",
            pr_parent_tree_sha="def",
        )
        assert isinstance(findings, list)
    except Exception as e:
        assert False, f"Empty issue body crashed: {e}"


def test_c4_none_issue_body():
    """C4: None issue body MUST NOT crash."""
    try:
        findings = core_validate(
            issue_body=None,  # type: ignore[arg-type]
            pr_files=["file.py"],
            pr_merge_tree_sha="abc",
            pr_parent_tree_sha="def",
        )
        assert isinstance(findings, list)
    except Exception as e:
        assert False, f"None issue body crashed: {e}"


def test_c4_none_pr_files():
    """C4: None pr_files MUST NOT crash."""
    try:
        findings = core_validate(
            issue_body="## Acceptance\n- [x] done",
            pr_files=None,  # type: ignore[arg-type]
            pr_merge_tree_sha="abc",
            pr_parent_tree_sha="def",
        )
        assert isinstance(findings, list)
    except Exception as e:
        assert False, f"None pr_files crashed: {e}"


# ═══════════════════════════════════════════════════════════════════════════
# C5: PATH EXTRACTION — only checklist paths, not prose
# ═══════════════════════════════════════════════════════════════════════════

ISSUE_WITH_PROSE_PATHS = """\
## Background

The file `scripts/validate_report_quality.py` needs updating.
Also see `references/report-template.md` for context.

## Acceptance Criteria
- [ ] `tests/test_issue_320_contracts.py` — new contract tests
- [ ] Implement the feature
"""


def test_c5_only_checklist_paths_extracted():
    """C5: Line-start paths extracted; prose paths ignored."""
    extracted = extract_issue_paths(ISSUE_WITH_PROSE_PATHS)
    # The checklist path should be extracted
    assert "tests/test_issue_320_contracts.py" in extracted, (
        "Checklist path not extracted"
    )
    # Prose paths (embedded in sentences, not at line start) should NOT be extracted
    assert "scripts/validate_report_quality.py" not in extracted, (
        "Prose path should NOT be extracted"
    )
    assert "references/report-template.md" not in extracted, (
        "Prose path should NOT be extracted"
    )


def test_c5_no_checklist_returns_empty():
    """C5: No checklist/bullet items → empty list."""
    extracted = extract_issue_paths("# Just a heading\nNo paths here.")
    assert extracted == [], f"Expected empty list, got {extracted}"


def test_c5_bullet_paths_extracted():
    """C5: Bullet list paths ARE extracted."""
    body = """\
## Scope
- `references/report-template.md`
- `references/decision-report-template.md`
"""
    extracted = extract_issue_paths(body)
    assert "references/report-template.md" in extracted, (
        "Bullet path not extracted"
    )
    assert "references/decision-report-template.md" in extracted, (
        "Bullet path not extracted"
    )


def test_c5_checklist_variants():
    """C5: Support `- [ ]`, `- [x]`, `* [ ]` checklist prefixes."""
    body = """\
- [ ] `file1.py` — unchecked
- [x] `file2.py` — checked
* [ ] `file3.py` — asterisk variant
"""
    extracted = extract_issue_paths(body)
    assert "file1.py" in extracted, "Missing unchecked item"
    assert "file2.py" in extracted, "Missing checked (x) item"
    assert "file3.py" in extracted, "Missing asterisk variant"


# ═══════════════════════════════════════════════════════════════════════════
# C6: DIRECTORY PREFIX MATCHING
# ═══════════════════════════════════════════════════════════════════════════

def test_c6_directory_prefix_matches():
    """C6: Directory `dir/` matches file `dir/foo.py` in PR files."""
    findings = core_validate(
        issue_body="- `mydir/` — all files in this dir",
        pr_files=["mydir/foo.py", "mydir/bar.py"],
        pr_merge_tree_sha="abc",
        pr_parent_tree_sha="def",
    )
    missing = [f for f in findings if f.code == "MISSING_FILE"]
    assert len(missing) == 0, (
        f"Directory prefix should match subfiles, got: "
        f"{[(m.detail, m.message) for m in missing]}"
    )


def test_c6_directory_prefix_no_match():
    """C6: Directory `dir/` with no matching PR file produces MISSING_FILE."""
    findings = core_validate(
        issue_body="- `mydir/` — all files in this dir",
        pr_files=["other/foo.py"],
        pr_merge_tree_sha="abc",
        pr_parent_tree_sha="def",
    )
    missing = [f for f in findings if f.code == "MISSING_FILE"]
    assert len(missing) >= 1, (
        "Directory prefix should produce MISSING_FILE when no file matches"
    )
    assert "mydir/" in {m.detail for m in missing}, (
        "Missing file detail should reference the directory path"
    )


# ═══════════════════════════════════════════════════════════════════════════
# REGRESSION FIXTURE: #320 / #324
# ═══════════════════════════════════════════════════════════════════════════

ISSUE_320_BODY_EXCERPT = """\
## 实现范围

建议更新：

- `references/report-template.md`
- `references/decision-report-template.md`
- `references/market-outlook-and-scenario-discipline.md`
- `checklists/market-outlook-audit.md`
- `evals/comparative-distillation/` 下增加或更新两组 GPT 对照的 distilled learning artifact
- `evals/templates/decision-utility-rubric.md`

## 验收标准

- [ ] 模板中出现 `Input boundary / 未指定项` 小节建议，且说明未指定项如何转 assumptions / uncertainty。
- [ ] market-outlook 产业链题默认建议 `Value-chain sensitivity map`。
- [ ] global scope 题默认建议 `Regional coverage matrix`，并要求 source role / data role。
- [ ] stakeholder implications 从"影响描述"升级为"decision/action/metric/trigger"结构。
- [ ] 文档明确说明：GPT 对照可学习结构，不继承 bibliography-only sourcing 或不可复查 citation。
- [ ] 至少新增一个 eval 或 comparative-distillation artifact，覆盖两组对照中的可迁移结构能力和不可迁移证据问题。
"""


PR_324_FILES = [
    "scripts/audit_report.py",
    "scripts/test_report_quality_validator.py",
    "scripts/validate_report_quality.py",
]


def test_regression_320_324_detects_no_op():
    """Regression: #324 was a no-op merge. Must detect NO_OP_MERGE + MISSING_FILE."""
    findings = core_validate(
        issue_body=ISSUE_320_BODY_EXCERPT,
        pr_files=PR_324_FILES,
        pr_merge_tree_sha="e8bfc976fbc40dfcab5833c824d95a0951a59716",
        pr_parent_tree_sha="e8bfc976fbc40dfcab5833c824d95a0951a59716",
    )
    codes = [f.code for f in findings]
    assert "NO_OP_MERGE" in codes, (
        f"Regression: #324 no-op merge not detected. Codes: {codes}"
    )
    assert "MISSING_FILE" in codes, (
        f"Regression: #324 missing templates not detected. Codes: {codes}"
    )


def test_regression_320_324_detects_missing_templates():
    """Regression: #324 claimed template changes but didn't touch them."""
    findings = core_validate(
        issue_body=ISSUE_320_BODY_EXCERPT,
        pr_files=PR_324_FILES,
        pr_merge_tree_sha="e8bfc",
        pr_parent_tree_sha="82b6ec",
    )
    missing = [f for f in findings if f.code == "MISSING_FILE"]
    missing_details = {m.detail for m in missing}

    # All specific template files from acceptance criteria must be flagged
    expected = {
        "references/report-template.md",
        "references/decision-report-template.md",
        "references/market-outlook-and-scenario-discipline.md",
        "checklists/market-outlook-audit.md",
        "evals/templates/decision-utility-rubric.md",
    }
    assert expected.issubset(missing_details), (
        f"Expected ALL template files flagged as missing. "
        f"Missing: {expected - missing_details}. "
        f"Flagged: {missing_details}"
    )


# ═══════════════════════════════════════════════════════════════════════════
# C7: COMBINED AND EDGE-CASE SCENARIOS
# ═══════════════════════════════════════════════════════════════════════════

def test_c7_combined_noop_and_missing():
    """C7: Both NO_OP_MERGE and MISSING_FILE can fire simultaneously."""
    findings = core_validate(
        issue_body="- [ ] `missing.py`",
        pr_files=["present.py"],
        pr_merge_tree_sha="same_sha",
        pr_parent_tree_sha="same_sha",
    )
    codes = [f.code for f in findings]
    assert "NO_OP_MERGE" in codes, f"NO_OP_MERGE missing: {codes}"
    assert "MISSING_FILE" in codes, f"MISSING_FILE missing: {codes}"


def test_c7_directory_prefix_no_overmatch():
    """C7: Directory prefix `mydir/` must NOT match `mydir-other/`."""
    findings = core_validate(
        issue_body="- `mydir/`",
        pr_files=["mydir-other/foo.py"],
        pr_merge_tree_sha="abc",
        pr_parent_tree_sha="def",
    )
    missing = [f for f in findings if f.code == "MISSING_FILE"]
    missing_paths = {m.detail for m in missing}
    assert "mydir/" in missing_paths, (
        f"Directory prefix must NOT match sibling dir. Got: {missing_paths}"
    )


def test_c7_deep_directory_prefix():
    """C7: Deep directory `a/b/c/` matches `a/b/c/d/e.py`."""
    findings = core_validate(
        issue_body="- `a/b/c/`",
        pr_files=["a/b/c/d/e.py", "a/b/c/f/g/h.py"],
        pr_merge_tree_sha="abc",
        pr_parent_tree_sha="def",
    )
    missing = [f for f in findings if f.code == "MISSING_FILE"]
    assert len(missing) == 0, (
        f"Deep directory prefix should match nested files: "
        f"{[(m.detail, m.message) for m in missing]}"
    )


def test_c7_uppercase_x_checkbox():
    """C7: `- [X]` (uppercase) MUST be treated same as `- [x]`."""
    body = "- [X] `uppercase.py`"
    extracted = extract_issue_paths(body)
    assert "uppercase.py" in extracted, (
        f"Uppercase [X] path not extracted: {extracted}"
    )


def test_c7_asymmetric_none_does_not_crash():
    """C7: `merge_tree=None, parent_tree='abc'` does not crash."""
    try:
        findings = core_validate(
            issue_body="- [ ] `file.py`",
            pr_files=["file.py"],
            pr_merge_tree_sha=None,
            pr_parent_tree_sha="abc",
        )
        assert isinstance(findings, list)
    except Exception as e:
        assert False, f"Asymmetric None crashed: {e}"


# ═══════════════════════════════════════════════════════════════════════════
# C8: REMOTE UNAVAILABLE SEMANTICS (issue #438 F3)
# ═══════════════════════════════════════════════════════════════════════════

def _run_cli_with_fake_gh_unavailable(allow_unavailable: bool) -> int:
    """Run the CLI with a fake `gh` that always exits 1 (unavailable)."""
    import subprocess as _sp
    import tempfile as _tf
    import stat as _st
    with _tf.TemporaryDirectory() as d:
        fake_gh = Path(d) / "gh"
        fake_gh.write_text("#!/bin/sh\nexit 1\n")
        fake_gh.chmod(fake_gh.stat().st_mode | _st.S_IEXEC)
        env = dict(os.environ)
        env["PATH"] = f"{d}:{env.get('PATH', '')}"
        cmd = [
            sys.executable,
            str(_SCRIPT_DIR / "validate_issue_pr_acceptance.py"),
            "1", "2",
        ]
        if allow_unavailable:
            cmd.append("--allow-unavailable")
        result = _sp.run(cmd, capture_output=True, text=True, env=env, timeout=30)
        return result.returncode


def test_c8_unavailable_returns_unavailable():
    """C8: gh unavailable MUST return EXIT_UNAVAILABLE (non-zero)."""
    rc = _run_cli_with_fake_gh_unavailable(allow_unavailable=False)
    assert rc == EXIT_UNAVAILABLE, (
        f"Expected EXIT_UNAVAILABLE ({EXIT_UNAVAILABLE}), got {rc}"
    )


def test_c8_allow_unavailable_returns_zero():
    """C8: --allow-unavailable downgrades unavailable to exit 0."""
    rc = _run_cli_with_fake_gh_unavailable(allow_unavailable=True)
    assert rc == 0, f"Expected 0 with --allow-unavailable, got {rc}"


# ═══════════════════════════════════════════════════════════════════════════
# C9: PARTIAL FETCH FAILURE MUST NOT REPORT PASS (issue #438 P1)
# ═══════════════════════════════════════════════════════════════════════════

def _run_cli_with_fake_gh(fail_request: str, allow_unavailable: bool) -> int:
    """Run the CLI with a fake `gh` that passes auth but can fail one data request.

    fail_request selects which data request fails: "issue", "files", "both",
    or "none". `gh auth status` always succeeds, so `_check_gh_available()`
    passes and execution reaches the fetch stage — unlike C8, which fails at
    the auth stage and never exercises the fetch functions.
    """
    import subprocess as _sp
    import tempfile as _tf
    import stat as _st
    script = """#!/bin/sh
case "$1" in
  auth)
    exit 0
    ;;
  issue)
    if [ "${FAIL_GH_REQUEST}" = "issue" ] || [ "${FAIL_GH_REQUEST}" = "both" ]; then
      exit 1
    fi
    echo '## Acceptance'
    echo '- [ ] `scripts/validate_issue_pr_acceptance.py`'
    exit 0
    ;;
  pr)
    if [ "${FAIL_GH_REQUEST}" = "files" ] || [ "${FAIL_GH_REQUEST}" = "both" ]; then
      exit 1
    fi
    echo 'scripts/validate_issue_pr_acceptance.py'
    exit 0
    ;;
  *)
    exit 1
    ;;
esac
"""
    with _tf.TemporaryDirectory() as d:
        fake_gh = Path(d) / "gh"
        fake_gh.write_text(script)
        fake_gh.chmod(fake_gh.stat().st_mode | _st.S_IEXEC)
        env = dict(os.environ)
        env["PATH"] = f"{d}:{env.get('PATH', '')}"
        env["FAIL_GH_REQUEST"] = fail_request
        cmd = [
            sys.executable,
            str(_SCRIPT_DIR / "validate_issue_pr_acceptance.py"),
            "1", "2",
        ]
        if allow_unavailable:
            cmd.append("--allow-unavailable")
        result = _sp.run(cmd, capture_output=True, text=True, env=env, timeout=30)
        return result.returncode


def test_c9_issue_fetch_fails_returns_unavailable():
    """C9 (P1): issue fetch fails (auth OK) MUST NOT be reported as pass."""
    rc = _run_cli_with_fake_gh("issue", allow_unavailable=False)
    assert rc == EXIT_UNAVAILABLE, (
        f"Expected EXIT_UNAVAILABLE ({EXIT_UNAVAILABLE}) when issue fetch "
        f"fails, got {rc}"
    )


def test_c9_files_fetch_fails_returns_unavailable():
    """C9 (P1): PR files fetch fails (auth OK) MUST NOT be reported as pass."""
    rc = _run_cli_with_fake_gh("files", allow_unavailable=False)
    assert rc == EXIT_UNAVAILABLE, (
        f"Expected EXIT_UNAVAILABLE ({EXIT_UNAVAILABLE}) when PR files fetch "
        f"fails, got {rc}"
    )


def test_c9_issue_fetch_fails_allow_unavailable_zero():
    """C9 (P1): --allow-unavailable downgrades a fetch failure to exit 0."""
    rc = _run_cli_with_fake_gh("issue", allow_unavailable=True)
    assert rc == 0, f"Expected 0 with --allow-unavailable, got {rc}"


def test_c9_all_fetches_ok_passes():
    """C9 (P1): both fetches succeed and the path is present → exit 0."""
    rc = _run_cli_with_fake_gh("none", allow_unavailable=False)
    assert rc == 0, f"Expected PASS (0) when fetches succeed, got {rc}"


# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import inspect

    # Collect all test functions
    tests = [
        obj for name, obj in globals().items()
        if name.startswith("test_") and inspect.isfunction(obj)
    ]
    tests.sort(key=lambda f: f.__name__)

    passed = 0
    failed = 0

    for test_fn in tests:
        try:
            test_fn()
            print(f"  ✅ {test_fn.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"  ❌ {test_fn.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"  💥 {test_fn.__name__}: {e}")
            failed += 1

    print(f"\n{'=' * 50}")
    print(f"  Total: {passed + failed}  |  Passed: {passed}  |  Failed: {failed}")
    if failed:
        sys.exit(1)
