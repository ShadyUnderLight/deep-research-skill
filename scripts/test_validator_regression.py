#!/usr/bin/env python3
"""Regression tests for validate_research_pack.py.

Each test creates a single-mutation fixture from a valid baseline,
runs the validator, and asserts the expected exit code.
"""

import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

VALID = """\
## Objective
ok

## Decision context
ok

## Primary route
ok

## Secondary disciplines
ok

## Core subquestions
ok

## Stop condition
ok

## Source register
ok

## Claim register
ok

## Uncertainty register
ok

## Artifact contract
ok

## Required audits
ok

## Final audit status
ok
"""

VALIDATOR = str(Path(__file__).resolve().parent / "validate_research_pack.py")


def write(path: str, content: str) -> str:
    Path(path).write_text(content)
    return path


def run_validator(path: str) -> int:
    return subprocess.run(
        [sys.executable, VALIDATOR, path],
        capture_output=True, text=True
    ).returncode


def test_valid_baseline(d: str) -> None:
    path = write(os.path.join(d, "valid.md"), VALID)
    rc = run_validator(path)
    assert rc == 0, f"valid baseline: expected 0, got {rc}"


def test_codeblock_heading(d: str) -> None:
    text = re.sub(
        r"^## Stop condition\nok",
        "```\n## Stop condition\n```",
        VALID, flags=re.MULTILINE
    )
    path = write(os.path.join(d, "codeblock.md"), text)
    rc = run_validator(path)
    assert rc == 2, f"code-block heading: expected exit 2 (missing heading), got {rc}"


def test_empty_section(d: str) -> None:
    text = re.sub(
        r"^## Stop condition\nok",
        "## Stop condition\n",
        VALID, flags=re.MULTILINE
    )
    path = write(os.path.join(d, "empty.md"), text)
    rc = run_validator(path)
    assert rc == 2, f"empty section: expected exit 2, got {rc}"


def test_h3_instead_of_h2(d: str) -> None:
    text = re.sub(
        r"^## Stop condition$",
        "### Stop condition",
        VALID, flags=re.MULTILINE
    )
    path = write(os.path.join(d, "h3.md"), text)
    rc = run_validator(path)
    assert rc == 2, f"H3 instead of H2: expected exit 2, got {rc}"


def test_blockquote_heading(d: str) -> None:
    text = re.sub(
        r"^## Stop condition$",
        "> ## Stop condition",
        VALID, flags=re.MULTILINE
    )
    path = write(os.path.join(d, "bq.md"), text)
    rc = run_validator(path)
    assert rc == 2, f"blockquote heading: expected exit 2, got {rc}"


def test_indented_fence(d: str) -> None:
    text = re.sub(
        r"^## Stop condition\nok",
        "   ```\n   ## Stop condition\n   hidden\n   ```",
        VALID, flags=re.MULTILINE
    )
    path = write(os.path.join(d, "ifence.md"), text)
    rc = run_validator(path)
    assert rc == 2, f"indented fence heading: expected exit 2, got {rc}"


def test_subheading_only_body(d: str) -> None:
    text = re.sub(
        r"^## Stop condition\nok",
        "## Stop condition\n### Placeholder subsection",
        VALID, flags=re.MULTILINE
    )
    path = write(os.path.join(d, "subonly.md"), text)
    rc = run_validator(path)
    assert rc == 2, f"sub-heading-only body: expected exit 2, got {rc}"


def test_partial_heading_match(d: str) -> None:
    text = re.sub(
        r"^## Stop condition$",
        "## Stop condition details",
        VALID, flags=re.MULTILINE
    )
    path = write(os.path.join(d, "partial.md"), text)
    rc = run_validator(path)
    assert rc == 2, f"partial heading match: expected exit 2, got {rc}"


# ─── Strict mode tests ────────────────────────────────────────────────────────

STRICT_BASELINE = """\
## Objective
ok

## Decision context
ok

## Primary route
Constrained choice / shortlist (alternative: market-outlook — rejected,
task asks for ranking not forecasting)

## Secondary disciplines
ok

## Core subquestions
ok

## Stop condition
ok

## Source register
- [S01] A relevant source
  - Supports: main claims

## Claim register
- Claim: main finding [S01]
  - Support: strong
  - Confidence: confirmed

## Uncertainty register
- Uncertainty: edge case
  - Why it matters: could weaken conclusion

## Artifact contract
ok

## Required audits
- final audit — passed
- quantitative role audit — passed

## Final audit status
Pass
"""


def run_strict(path: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, VALIDATOR, "--strict", path],
        capture_output=True, text=True
    )


def test_strict_valid_baseline(d: str) -> None:
    path = write(os.path.join(d, "strict_valid.md"), STRICT_BASELINE)
    result = run_strict(path)
    assert result.returncode == 0, (
        f"strict valid baseline: expected 0, got {result.returncode}\n"
        f"stdout: {result.stdout}"
    )


def test_strict_no_source_ids(d: str) -> None:
    text = re.sub(
        r"- \[S01\].*",
        "- A relevant source",
        STRICT_BASELINE, flags=re.MULTILINE
    )
    path = write(os.path.join(d, "no_ids.md"), text)
    result = run_strict(path)
    assert result.returncode == 4, (
        f"missing source IDs: expected exit 4, got {result.returncode}\n"
        f"stdout: {result.stdout}"
    )


def test_strict_undefined_source_ref(d: str) -> None:
    text = re.sub(
        r"main finding \[S01\]",
        "main finding [S99]",
        STRICT_BASELINE
    )
    path = write(os.path.join(d, "undefined.md"), text)
    result = run_strict(path)
    assert result.returncode == 4, (
        f"undefined source ref: expected exit 4, got {result.returncode}\n"
        f"stdout: {result.stdout}"
    )


def test_strict_unused_source_id(d: str) -> None:
    text = STRICT_BASELINE.replace(
        "main finding [S01]",
        "main finding (no ref)"
    )
    path = write(os.path.join(d, "unused.md"), text)
    result = run_strict(path)
    assert result.returncode == 0, (
        f"unused source IDs: expected exit 0 (warning), got {result.returncode}\n"
        f"stdout: {result.stdout}"
    )
    assert "Unused" in result.stdout, f"expected warning in output: {result.stdout}"


def test_strict_audit_status_partial(d: str) -> None:
    text = re.sub(
        r"^## Final audit status\nPass",
        "## Final audit status\nPartial",
        STRICT_BASELINE, flags=re.MULTILINE
    )
    path = write(os.path.join(d, "partial.md"), text)
    result = run_strict(path)
    assert result.returncode == 0, (
        f"Partial audit status: expected exit 0 (warning), got {result.returncode}\n"
        f"stdout: {result.stdout}"
    )
    assert "Partial" in result.stdout, f"expected warning in output: {result.stdout}"


def test_strict_audit_status_fail(d: str) -> None:
    text = re.sub(
        r"^## Final audit status\nPass",
        "## Final audit status\nFail",
        STRICT_BASELINE, flags=re.MULTILINE
    )
    path = write(os.path.join(d, "fail.md"), text)
    result = run_strict(path)
    assert result.returncode == 4, (
        f"Fail audit status: expected exit 4, got {result.returncode}\n"
        f"stdout: {result.stdout}"
    )


def test_strict_audit_status_invalid(d: str) -> None:
    text = re.sub(
        r"^## Final audit status\nPass",
        "## Final audit status\nPending",
        STRICT_BASELINE, flags=re.MULTILINE
    )
    path = write(os.path.join(d, "invalid.md"), text)
    result = run_strict(path)
    assert result.returncode == 4, (
        f"invalid audit status: expected exit 4, got {result.returncode}\n"
        f"stdout: {result.stdout}"
    )


def test_strict_claim_no_evidence(d: str) -> None:
    text = STRICT_BASELINE.replace("main finding [S01]", "main finding")
    path = write(os.path.join(d, "no_evidence.md"), text)
    result = run_strict(path)
    assert result.returncode == 0, (
        f"missing evidence tags: expected exit 0 (warning), got {result.returncode}\n"
        f"stdout: {result.stdout}"
    )
    assert "no evidence" in result.stdout.lower(), (
        f"expected warning about missing evidence: {result.stdout}"
    )


def test_strict_partial_claim_missing_evidence(d: str) -> None:
    text = re.sub(
        r"(- Claim: main finding.*?)(?=\n## )",
        r"\1\n- Claim: extra claim without evidence\n  - Support: guess\n  - Confidence: low",
        STRICT_BASELINE, flags=re.DOTALL
    )
    path = write(os.path.join(d, "partial_evidence.md"), text)
    result = run_strict(path)
    assert result.returncode == 0, (
        f"partial claim missing evidence: expected exit 0 (warning), got {result.returncode}\n"
        f"stdout: {result.stdout}"
    )
    assert "Claim #2" in result.stdout, (
        f"expected Claim #2 warning in output: {result.stdout}"
    )


def test_strict_claim_evidence_next_line(d: str) -> None:
    text = re.sub(
        r"- Claim: main finding \[S01\]\n  - Support: strong",
        "- Claim: main finding\n  - Evidence: [S01]\n  - Support: strong",
        STRICT_BASELINE
    )
    path = write(os.path.join(d, "evidence_next_line.md"), text)
    result = run_strict(path)
    assert result.returncode == 0, (
        f"claim evidence on next line: expected exit 0, got {result.returncode}\n"
        f"stdout: {result.stdout}"
    )


def test_strict_fenced_code_ignored(d: str) -> None:
    text = STRICT_BASELINE + "\n\n```\nExample [S99] in code block\n```\n"
    path = write(os.path.join(d, "fenced.md"), text)
    result = run_strict(path)
    assert result.returncode == 0, (
        f"fenced code [S99]: expected exit 0, got {result.returncode}\n"
        f"stdout: {result.stdout}"
    )


def test_strict_table_source_id(d: str) -> None:
    text = re.sub(
        r"- \[S01\].*",
        "| S01 | A relevant source |",
        STRICT_BASELINE
    )
    path = write(os.path.join(d, "table.md"), text)
    result = run_strict(path)
    assert result.returncode == 0, (
        f"table source ID: expected exit 0, got {result.returncode}\n"
        f"stdout: {result.stdout}"
    )


def test_strict_malformed_source_id_single_digit(d: str) -> None:
    text = STRICT_BASELINE.replace("[S01]", "[S1]")
    path = write(os.path.join(d, "malformed1.md"), text)
    result = run_strict(path)
    assert result.returncode == 4, (
        f"malformed [S1]: expected exit 4, got {result.returncode}\n"
        f"stdout: {result.stdout}"
    )


def test_strict_malformed_source_id_triple_digit(d: str) -> None:
    text = STRICT_BASELINE.replace("[S01]", "[S001]")
    path = write(os.path.join(d, "malformed3.md"), text)
    result = run_strict(path)
    assert result.returncode == 4, (
        f"malformed [S001]: expected exit 4, got {result.returncode}\n"
        f"stdout: {result.stdout}"
    )


def test_strict_duplicate_source_id(d: str) -> None:
    text = STRICT_BASELINE.replace(
        "- [S01] A relevant source",
        "- [S01] First source\n- [S01] Duplicate source"
    )
    path = write(os.path.join(d, "duplicate.md"), text)
    result = run_strict(path)
    assert result.returncode == 4, (
        f"duplicate source ID: expected exit 4, got {result.returncode}\n"
        f"stdout: {result.stdout}"
    )


def test_strict_undefined_u_id(d: str) -> None:
    text = STRICT_BASELINE.replace(
        "main finding [S01]",
        "main finding [U99]"
    )
    path = write(os.path.join(d, "undefined_u.md"), text)
    result = run_strict(path)
    assert result.returncode == 4, (
        f"undefined U99: expected exit 4, got {result.returncode}\n"
        f"stdout: {result.stdout}"
    )


def test_strict_claim_inference_id_warns_only(d: str) -> None:
    text = STRICT_BASELINE.replace(
        "main finding [S01]",
        "main finding [I01]"
    )
    path = write(os.path.join(d, "inference.md"), text)
    result = run_strict(path)
    assert result.returncode == 0, (
        f"I01 in claim: expected exit 0 (warning), got {result.returncode}\n"
        f"stdout: {result.stdout}"
    )
    assert "Inference IDs" in result.stdout, (
        f"expected Inference IDs warning in output: {result.stdout}"
    )


def test_strict_malformed_body_ref(d: str) -> None:
    text = STRICT_BASELINE.replace(
        "main finding [S01]",
        "main finding [S1]"
    )
    path = write(os.path.join(d, "malformed_body.md"), text)
    result = run_strict(path)
    assert result.returncode == 4, (
        f"malformed body ref [S1]: expected exit 4, got {result.returncode}\n"
        f"stdout: {result.stdout}"
    )


def test_strict_malformed_claim_ref(d: str) -> None:
    text = STRICT_BASELINE.replace(
        "main finding [S01]",
        "main finding"
    )
    text = text.replace(
        "- Claim: main finding",
        "- Claim: main finding [S001]"
    )
    path = write(os.path.join(d, "malformed_claim.md"), text)
    result = run_strict(path)
    assert result.returncode == 4, (
        f"malformed claim ref [S001]: expected exit 4, got {result.returncode}\n"
        f"stdout: {result.stdout}"
    )


def test_strict_non_strict_ignores_strict_checks(d: str) -> None:
    text = re.sub(
        r"- \[S01\].*",
        "- A relevant source",
        STRICT_BASELINE, flags=re.MULTILINE
    )
    path = write(os.path.join(d, "non_strict.md"), text)
    rc = run_validator(path)
    assert rc == 0, (
        f"non-strict mode should ignore source ID issues: expected 0, got {rc}"
    )


# ─── V4 behavior-level fixtures (closest alternative, per-audit, consistency) ───

V4_BASELINE = """\
## Objective
ok

## Decision context
ok

## Primary route
Constrained choice / shortlist
Closest alternative: market-outlook (rejected — task asks for ranking,
not forecasting). Boundary: if the question shifted to "how will the
travel market evolve," market-outlook would become the primary route.

## Secondary disciplines
ok

## Core subquestions
ok

## Stop condition
ok

## Source register
- [S01] A relevant source
  - Supports: main claims

## Claim register
- Claim: main finding [S01]
  - Support: strong
  - Confidence: confirmed

## Uncertainty register
ok

## Artifact contract
ok

## Required audits
- final audit — passed
- quantitative role audit — passed

## Final audit status
Pass
"""

V4_NO_ALTERNATIVE = re.sub(
    r"Constrained choice / shortlist\nClosest alternative.*?\n\n",
    "Constrained choice / shortlist\n\n",
    V4_BASELINE,
    flags=re.DOTALL,
)

V4_PASS_BUT_NOT_RUN = re.sub(
    r"- final audit — passed\n- quantitative role audit — passed",
    "- final audit — not-run\n- quantitative role audit — passed",
    V4_BASELINE,
)

V4_PASS_BUT_PARTIAL = re.sub(
    r"- final audit — passed\n- quantitative role audit — passed",
    "- final audit — partial: incomplete execution\n- quantitative role audit — passed",
    V4_BASELINE,
)

V4_PARTIAL_NOT_RUN_NO_REASON = re.sub(
    r"## Required audits\n- final audit — passed\n- quantitative role audit — passed\n\n## Final audit status\nPass",
    "## Required audits\n- final audit — not-run\n- quantitative role audit — passed\n\n## Final audit status\nPartial",
    V4_BASELINE,
)

V4_PARTIAL_VALID = re.sub(
    r"## Final audit status\nPass",
    "## Final audit status\nPartial",
    re.sub(
        r"- final audit — passed\n- quantitative role audit — passed",
        "- final audit — not-run: task completed before audit available\n"
        "- quantitative role audit — passed",
        V4_BASELINE,
    ),
)

V4_PASS_SKIPPED_NO_REASON = re.sub(
    r"- final audit — passed\n- quantitative role audit — passed",
    "- final audit — skipped\n- quantitative role audit — passed",
    V4_BASELINE,
)

V4_PASS_PARTIAL_NO_REASON = re.sub(
    r"- final audit — passed\n- quantitative role audit — passed",
    "- final audit — partial\n- quantitative role audit — passed",
    V4_BASELINE,
)


def test_strict_v4_valid_baseline(d: str) -> None:
    path = write(os.path.join(d, "v4_valid.md"), V4_BASELINE)
    result = run_strict(path)
    assert result.returncode == 0, (
        f"V4 valid baseline: expected exit 0, got {result.returncode}\n"
        f"stdout: {result.stdout}"
    )


def test_strict_v4_missing_closest_alternative(d: str) -> None:
    path = write(os.path.join(d, "v4_no_alt.md"), V4_NO_ALTERNATIVE)
    result = run_strict(path)
    assert result.returncode == 4, (
        f"V4 missing closest alternative: expected exit 4, got {result.returncode}\n"
        f"stdout: {result.stdout}"
    )
    assert "closest-alternative" in result.stdout.lower() or \
           "boundary" in result.stdout.lower(), (
        f"expected closest-alternative/boundary error in output: {result.stdout}"
    )


def test_strict_v4_pass_but_audit_not_run(d: str) -> None:
    path = write(os.path.join(d, "v4_not_run.md"), V4_PASS_BUT_NOT_RUN)
    result = run_strict(path)
    assert result.returncode == 4, (
        f"V4 Pass but audit not-run: expected exit 4, got {result.returncode}\n"
        f"stdout: {result.stdout}"
    )
    assert "not-run" in result.stdout.lower(), (
        f"expected not-run error in output: {result.stdout}"
    )


def test_strict_v4_pass_but_audit_partial(d: str) -> None:
    path = write(os.path.join(d, "v4_partial_audit.md"), V4_PASS_BUT_PARTIAL)
    result = run_strict(path)
    assert result.returncode == 4, (
        f"V4 Pass but audit partial: expected exit 4, got {result.returncode}\n"
        f"stdout: {result.stdout}"
    )
    assert "partial" in result.stdout.lower(), (
        f"expected partial error in output: {result.stdout}"
    )


def test_strict_v4_partial_not_run_no_reason(d: str) -> None:
    path = write(os.path.join(d, "v4_p_nr_nr.md"), V4_PARTIAL_NOT_RUN_NO_REASON)
    result = run_strict(path)
    assert result.returncode == 4, (
        f"V4 Partial + not-run no reason: expected exit 4, got {result.returncode}\n"
        f"stdout: {result.stdout}"
    )
    assert "should be Fail" in result.stdout.lower() or \
           "without" in result.stdout.lower(), (
        f"expected 'should be Fail' / 'without' error in output: {result.stdout}"
    )


def test_strict_v4_partial_valid(d: str) -> None:
    path = write(os.path.join(d, "v4_partial_valid.md"), V4_PARTIAL_VALID)
    result = run_strict(path)
    assert result.returncode == 0, (
        f"V4 Partial valid (not-run with reason): expected exit 0, got {result.returncode}\n"
        f"stdout: {result.stdout}"
    )


def test_strict_v4_pass_skipped_no_reason(d: str) -> None:
    path = write(os.path.join(d, "v4_skip_nr.md"), V4_PASS_SKIPPED_NO_REASON)
    result = run_strict(path)
    assert result.returncode == 4, (
        f"V4 Pass + skipped no reason: expected exit 4, got {result.returncode}\n"
        f"stdout: {result.stdout}"
    )
    assert "skipped" in result.stdout.lower(), (
        f"expected skipped error in output: {result.stdout}"
    )


def test_strict_v4_pass_partial_no_reason(d: str) -> None:
    path = write(os.path.join(d, "v4_part_nr.md"), V4_PASS_PARTIAL_NO_REASON)
    result = run_strict(path)
    assert result.returncode == 4, (
        f"V4 Pass + partial no reason: expected exit 4, got {result.returncode}\n"
        f"stdout: {result.stdout}"
    )
    assert "partial" in result.stdout.lower(), (
        f"expected partial error in output: {result.stdout}"
    )


def main() -> int:
    with tempfile.TemporaryDirectory() as d:
        tests = [
            ("valid baseline", test_valid_baseline),
            ("code-block heading", test_codeblock_heading),
            ("empty section", test_empty_section),
            ("H3 instead of H2", test_h3_instead_of_h2),
            ("blockquote heading", test_blockquote_heading),
            ("indented fence", test_indented_fence),
            ("sub-heading-only body", test_subheading_only_body),
            ("partial heading match", test_partial_heading_match),
            ("strict valid baseline", test_strict_valid_baseline),
            ("strict no source IDs", test_strict_no_source_ids),
            ("strict undefined source ref", test_strict_undefined_source_ref),
            ("strict unused source id (warning)", test_strict_unused_source_id),
            ("strict audit status Partial (warning)", test_strict_audit_status_partial),
            ("strict audit status Fail", test_strict_audit_status_fail),
            ("strict audit status invalid", test_strict_audit_status_invalid),
            ("strict claim no evidence (warning)", test_strict_claim_no_evidence),
            ("strict partial claim missing evidence (warning)", test_strict_partial_claim_missing_evidence),
            ("strict claim evidence on next line", test_strict_claim_evidence_next_line),
            ("strict fenced code ignores [S99]", test_strict_fenced_code_ignored),
            ("strict table S01 source ID", test_strict_table_source_id),
            ("strict malformed [S1] single digit", test_strict_malformed_source_id_single_digit),
            ("strict malformed [S001] triple digit", test_strict_malformed_source_id_triple_digit),
            ("strict duplicate source ID", test_strict_duplicate_source_id),
            ("strict undefined [U99] reference", test_strict_undefined_u_id),
            ("strict I01 claim warns only", test_strict_claim_inference_id_warns_only),
            ("strict malformed body ref [S1]", test_strict_malformed_body_ref),
            ("strict malformed claim ref [S001]", test_strict_malformed_claim_ref),
            ("non-strict ignores strict checks", test_strict_non_strict_ignores_strict_checks),
            ("V4 valid baseline (closest alt + per-audit)", test_strict_v4_valid_baseline),
            ("V4 missing closest alternative", test_strict_v4_missing_closest_alternative),
            ("V4 Pass but audit not-run", test_strict_v4_pass_but_audit_not_run),
            ("V4 Pass but audit partial", test_strict_v4_pass_but_audit_partial),
            ("V4 Partial + not-run no reason", test_strict_v4_partial_not_run_no_reason),
            ("V4 Partial valid (not-run with reason)", test_strict_v4_partial_valid),
            ("V4 Pass + skipped no reason", test_strict_v4_pass_skipped_no_reason),
            ("V4 Pass + partial no reason", test_strict_v4_pass_partial_no_reason),
        ]
        failures = []
        for name, fn in tests:
            try:
                fn(d)
                print(f"  PASS  {name}")
            except AssertionError as e:
                print(f"  FAIL  {name}: {e}")
                failures.append(name)
        if failures:
            print(f"\n{len(failures)} test(s) failed: {', '.join(failures)}")
            return 1
        print(f"\nAll {len(tests)} tests passed.")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
