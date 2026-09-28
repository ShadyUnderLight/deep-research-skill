#!/usr/bin/env python3
"""
Validate PR-issue acceptance consistency.

Detects:
  - NO_OP_MERGE:  merge commit with same tree SHA as parent (zero diff)
  - MISSING_FILE: issue acceptance checklist path not in PR changed files

Usage:
    python3 scripts/validate_issue_pr_acceptance.py <ISSUE_NUMBER> <PR_NUMBER>

Requires:
  - gh CLI (GitHub CLI) authenticated for the repository
  - git (for tree SHA comparison)

Exit codes:
    0 = all checks pass
    1 = warnings only
    2 = one or more blocking errors
    3 = remote dependency (gh) unavailable or data could not be fetched
        (unless --allow-unavailable is passed, which downgrades this to 0)
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from typing import Optional


# ═══════════════════════════════════════════════════════════════════════════
# Types
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class ValidationFinding:
    """A single validation finding from PR-issue acceptance checks."""

    severity: str  # "error" | "warning"
    code: str      # machine-readable code
    message: str   # human-readable summary
    detail: str    # additional context (e.g., the file path or SHA)


# ═══════════════════════════════════════════════════════════════════════════
# Constants
# ═══════════════════════════════════════════════════════════════════════════

EXIT_PASS = 0
EXIT_WARNINGS = 1
EXIT_BLOCKING = 2
EXIT_UNAVAILABLE = 3


class FetchError(RuntimeError):
    """Raised when a required gh data request fails.

    Distinct from a *successful but empty* result (empty issue body, or a
    PR that changes no files). Callers must treat a FetchError as
    "cannot validate", never as "validation passed".
    """

# Regex 1: checklist line `- [ ] ` / `- [x] ` / `* [ ] ` / `* [x] `
# followed by a backtick-enclosed path.
_CHECKLIST_PATH_RE = re.compile(
    r"^[\s]*[-*]\s+\[[\sxX]\]\s+`([^`]+)`",
    re.MULTILINE,
)

# Regex 2: prose bullet list `- `path`` / `* `path`` (no checkbox).
# This catches "实现范围" sections where paths are listed as plain bullets.
_BULLET_PATH_RE = re.compile(
    r"^[\s]*[-*]\s+`([^`]+)`",
    re.MULTILINE,
)


# ═══════════════════════════════════════════════════════════════════════════
# Core validation logic (pure, no side effects — fully testable)
# ═══════════════════════════════════════════════════════════════════════════

def extract_issue_paths(body: str) -> list[str]:
    r"""Extract file paths from issue body's path listings.

    Extracts from two formats:
      1. Checklist items: ``- [ ] `path` `` and ``- [x] `path` ``
      2. Bullet lists:   ``- `path` `` and ``* `path` `` (no checkbox)

    Paths embedded in running prose paragraphs are NOT extracted
    (they must be at the start of a bullet/checklist line).

    Args:
        body: Issue body markdown text.

    Returns:
        Sorted list of unique file paths found in checklist/bullet items.
    """
    if not body:
        return []
    matches = []
    matches.extend(_CHECKLIST_PATH_RE.findall(body))
    matches.extend(_BULLET_PATH_RE.findall(body))
    paths = sorted({p.strip() for p in matches if p.strip()})
    return paths


def core_validate(
    issue_body: Optional[str],
    pr_files: Optional[list[str]],
    pr_merge_tree_sha: Optional[str],
    pr_parent_tree_sha: Optional[str],
) -> list[ValidationFinding]:
    """Validate PR-issue acceptance consistency (pure function).

    Args:
        issue_body: Issue body markdown text. None/empty treated as no issue.
        pr_files: List of file paths changed in the PR. None treated as empty.
        pr_merge_tree_sha: Tree SHA of the PR merge commit (NOT the commit SHA).
                           None if PR not merged.
        pr_parent_tree_sha: Tree SHA of the first parent commit.
                            None if PR not merged.

    Returns:
        List of ValidationFinding. Empty = all checks pass.
    """
    findings: list[ValidationFinding] = []

    # Normalise inputs
    body = (issue_body or "").strip()
    files: set[str] = set(pr_files or [])

    # ── R1: No-op merge detection ──────────────────────────────────────
    if pr_merge_tree_sha is not None and pr_parent_tree_sha is not None:
        if pr_merge_tree_sha == pr_parent_tree_sha:
            findings.append(ValidationFinding(
                severity="error",
                code="NO_OP_MERGE",
                message="PR merge commit has the same tree SHA as its parent — "
                        "zero files changed (no-op merge).",
                detail=f"merge/parent tree SHA: {pr_merge_tree_sha}",
            ))

    # ── R2: Missing file / directory detection ─────────────────────────
    issue_paths = extract_issue_paths(body)
    for path in issue_paths:
        if path.endswith("/"):
            # Directory reference: check if any PR file starts with this prefix
            prefix = path.rstrip("/")
            if not any(f.startswith(prefix + "/") or f == prefix for f in files):
                findings.append(ValidationFinding(
                    severity="error",
                    code="MISSING_FILE",
                    message=f"Issue references directory `{path}` but no PR file "
                            f"falls under this directory.",
                    detail=path,
                ))
        else:
            # Exact file reference
            if path not in files:
                findings.append(ValidationFinding(
                    severity="error",
                    code="MISSING_FILE",
                    message=f"Issue acceptance checklist references `{path}` "
                            f"but it is not in the PR's changed files.",
                    detail=path,
                ))

    return findings


# ═══════════════════════════════════════════════════════════════════════════
# gh CLI helpers (side-effecting — isolated for testability)
# ═══════════════════════════════════════════════════════════════════════════

def _check_gh_available() -> bool:
    """Return True if gh CLI is available and authenticated."""
    try:
        result = subprocess.run(
            ["gh", "auth", "status"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def _gh_run(args: list[str], timeout: int = 30) -> str:
    """Run a gh CLI command and return stdout. Raises RuntimeError on failure."""
    try:
        result = subprocess.run(
            ["gh"] + args,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except FileNotFoundError:
        raise RuntimeError("gh CLI not found. Install GitHub CLI: https://cli.github.com/")
    except subprocess.TimeoutExpired:
        raise RuntimeError(f"gh command timed out after {timeout}s: gh {' '.join(args)}")

    if result.returncode != 0:
        raise RuntimeError(
            f"gh command failed (exit {result.returncode}): "
            f"gh {' '.join(args)}\n{result.stderr.strip()}"
        )
    return result.stdout.strip()


def fetch_issue_body(issue_number: int) -> str:
    """Fetch issue body via gh CLI.

    Returns:
        Issue body markdown. An issue that legitimately has no body returns
        "" (success). Raises FetchError if the data cannot be fetched (e.g.
        issue missing or gh error) so callers can distinguish a fetch
        failure from an empty-but-successful result.
    """
    try:
        return _gh_run([
            "issue", "view", str(issue_number),
            "--json", "body",
            "--jq", ".body",
        ])
    except RuntimeError as e:
        raise FetchError(
            f"could not fetch issue #{issue_number}: {e}"
        ) from e


def fetch_pr_files(pr_number: int) -> list[str]:
    """Fetch list of files changed in a PR via gh CLI.

    Returns:
        List of file paths. A PR that legitimately changes no files returns
        [] (success). Raises FetchError if the data cannot be fetched so
        callers can distinguish a fetch failure from an empty-but-successful
        result.
    """
    try:
        raw = _gh_run([
            "pr", "view", str(pr_number),
            "--json", "files",
            "--jq", ".files[].path",
        ])
        if not raw:
            return []
        return sorted(line.strip() for line in raw.splitlines() if line.strip())
    except RuntimeError as e:
        raise FetchError(
            f"could not fetch PR #{pr_number} files: {e}"
        ) from e


def fetch_pr_tree_shas(pr_number: int) -> tuple[Optional[str], Optional[str]]:
    """Fetch merge tree SHA and parent tree SHA for a merged PR.

    Returns (tree SHA of merge commit, tree SHA of first parent) when the PR
    is merged. Returns (None, None) when the PR is **not merged** — a
    legitimate "skip the no-op-merge check" result.

    Raises FetchError when the merge state cannot be determined, or when the
    PR is merged but its tree SHAs cannot be resolved (gh error, git error,
    timeout, shallow clone). That is *unavailable data*, not a clean skip:
    silently treating it as (None, None) would skip the NO_OP_MERGE check and
    could report PASS (issue #438 review).

    Note: returns tree SHAs, NOT commit SHAs — two different commits
    can produce the same tree (= no-op merge). Comparing tree SHAs
    catches this correctly.
    """
    try:
        raw = _gh_run([
            "pr", "view", str(pr_number),
            "--json", "mergeCommit",
            "--jq", ".mergeCommit.oid",
        ])
    except RuntimeError as e:
        raise FetchError(
            f"could not fetch PR #{pr_number} merge state: {e}"
        ) from e

    merge_sha = raw.strip()
    if not merge_sha or merge_sha == "null":
        return None, None  # PR not merged

    # Get trees via git plumbing. Any failure here means the PR is merged but
    # the tree data is unavailable → FetchError (never a silent skip).
    try:
        tree_result = subprocess.run(
            ["git", "rev-parse", f"{merge_sha}^{{tree}}"],
            capture_output=True, text=True, timeout=10,
        )
        if tree_result.returncode != 0:
            raise FetchError(
                f"could not resolve merge tree for PR #{pr_number} "
                f"({merge_sha}): {tree_result.stderr.strip()}"
            )
        merge_tree = tree_result.stdout.strip()

        parent_result = subprocess.run(
            ["git", "rev-parse", f"{merge_sha}^1^{{tree}}"],
            capture_output=True, text=True, timeout=10,
        )
        if parent_result.returncode != 0:
            raise FetchError(
                f"could not resolve parent tree for PR #{pr_number} "
                f"({merge_sha}): {parent_result.stderr.strip()}"
            )
        parent_tree = parent_result.stdout.strip()

        return merge_tree, parent_tree
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        raise FetchError(
            f"could not resolve trees for PR #{pr_number} ({merge_sha}): {exc}"
        ) from exc


# ═══════════════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════════════

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate PR-issue acceptance consistency",
    )
    parser.add_argument(
        "issue_number", type=int,
        help="GitHub issue number",
    )
    parser.add_argument(
        "pr_number", type=int,
        help="GitHub PR number",
    )
    parser.add_argument(
        "--allow-unavailable",
        action="store_true",
        help="When gh is unavailable or data cannot be fetched, exit 0 "
             "(advisory) instead of the default non-zero UNAVAILABLE code.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if not _check_gh_available():
        print(
            "warning: gh CLI is not available or not authenticated. "
            "Skipping validation. Install gh: https://cli.github.com/",
            file=sys.stderr,
        )
        return EXIT_PASS if args.allow_unavailable else EXIT_UNAVAILABLE

    # Fetch required data. A fetch FAILURE (vs. a legitimately empty result)
    # must not be silently treated as "validation passed": an unmerged PR with
    # an empty issue body would otherwise produce no findings and exit 0, and
    # an unresolvable merge tree would silently skip the NO_OP_MERGE check.
    try:
        issue_body = fetch_issue_body(args.issue_number)
        pr_files = fetch_pr_files(args.pr_number)
        merge_tree, parent_tree = fetch_pr_tree_shas(args.pr_number)
    except FetchError as exc:
        print(f"warning: {exc}", file=sys.stderr)
        return EXIT_PASS if args.allow_unavailable else EXIT_UNAVAILABLE

    # Run validation
    findings = core_validate(
        issue_body=issue_body,
        pr_files=pr_files,
        pr_merge_tree_sha=merge_tree,
        pr_parent_tree_sha=parent_tree,
    )

    if not findings:
        print("All PR-issue acceptance checks pass.")
        return EXIT_PASS

    # Report findings
    errors = [f for f in findings if f.severity == "error"]
    warnings = [f for f in findings if f.severity == "warning"]

    for f in findings:
        tag = "ERROR" if f.severity == "error" else "WARN"
        print(f"[{tag}] [{f.code}] {f.message}")
        if f.detail:
            print(f"       detail: {f.detail}")

    if errors:
        print(f"\n{len(errors)} error(s) found.", file=sys.stderr)
        return EXIT_BLOCKING
    if warnings:
        print(f"\n{len(warnings)} warning(s) found.", file=sys.stderr)
        return EXIT_WARNINGS

    return EXIT_PASS


if __name__ == "__main__":
    sys.exit(main())
