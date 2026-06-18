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
    0 = all checks pass (or gh unavailable — advisory only)
    1 = warnings only
    2 = one or more blocking errors
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
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

# Regex 1: checklist line `- [ ] ` / `- [x] ` / `* [ ] ` / `* [x] `
# followed by a backtick-enclosed path.
_CHECKLIST_PATH_RE = re.compile(
    r"^[\s]*[-*]\s+\[[\sx]\]\s+`([^`]+)`",
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
    pr_merge_sha: Optional[str],
    pr_parent_sha: Optional[str],
) -> list[ValidationFinding]:
    """Validate PR-issue acceptance consistency (pure function).

    Args:
        issue_body: Issue body markdown text. None/empty treated as no issue.
        pr_files: List of file paths changed in the PR. None treated as empty.
        pr_merge_sha: SHA of the PR merge commit. None if not merged.
        pr_parent_sha: SHA of the parent commit. None if not merged.

    Returns:
        List of ValidationFinding. Empty = all checks pass.
    """
    findings: list[ValidationFinding] = []

    # Normalise inputs
    body = (issue_body or "").strip()
    files: set[str] = set(pr_files or [])

    # ── R1: No-op merge detection ──────────────────────────────────────
    if pr_merge_sha is not None and pr_parent_sha is not None:
        if pr_merge_sha == pr_parent_sha:
            findings.append(ValidationFinding(
                severity="error",
                code="NO_OP_MERGE",
                message="PR merge commit has the same tree SHA as its parent — "
                        "zero files changed (no-op merge).",
                detail=f"merge/parent tree SHA: {pr_merge_sha}",
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
        Issue body markdown, or empty string on failure.
    """
    try:
        return _gh_run([
            "issue", "view", str(issue_number),
            "--json", "body",
            "--jq", ".body",
        ])
    except RuntimeError as e:
        print(f"warning: could not fetch issue #{issue_number}: {e}", file=sys.stderr)
        return ""


def fetch_pr_files(pr_number: int) -> list[str]:
    """Fetch list of files changed in a PR via gh CLI.

    Returns:
        List of file paths, or empty list on failure.
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
        print(f"warning: could not fetch PR #{pr_number} files: {e}", file=sys.stderr)
        return []


def fetch_pr_merge_sha(pr_number: int) -> tuple[Optional[str], Optional[str]]:
    """Fetch merge commit SHA and parent commit SHA for a merged PR.

    Returns:
        (merge_sha, parent_sha) or (None, None) if PR not merged / unavailable.
    """
    try:
        raw = _gh_run([
            "pr", "view", str(pr_number),
            "--json", "mergeCommit",
            "--jq", ".mergeCommit.oid",
        ])
        if not raw:
            return None, None  # not merged
        merge_sha = raw.strip()
    except RuntimeError:
        return None, None

    # Get tree of merge commit via git plumbing
    try:
        tree_result = subprocess.run(
            ["git", "rev-parse", f"{merge_sha}^{{tree}}"],
            capture_output=True, text=True, timeout=10,
        )
        if tree_result.returncode != 0:
            return None, None
        merge_tree = tree_result.stdout.strip()

        # Get tree of first parent
        parent_result = subprocess.run(
            ["git", "rev-parse", f"{merge_sha}^1^{{tree}}"],
            capture_output=True, text=True, timeout=10,
        )
        if parent_result.returncode != 0:
            return merge_tree, None
        parent_tree = parent_result.stdout.strip()

        # Return tree SHAs (not commit SHAs) for comparison
        return merge_tree, parent_tree
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None, None


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
        "--no-fetch", action="store_true",
        help="Skip gh CLI fetching (for testing with pre-supplied data)",
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
        return EXIT_PASS

    # Fetch data
    issue_body = fetch_issue_body(args.issue_number)
    pr_files = fetch_pr_files(args.pr_number)
    merge_sha, parent_sha = fetch_pr_merge_sha(args.pr_number)

    if not issue_body and not pr_files:
        print(
            "warning: could not fetch issue body or PR files — skipping validation.",
            file=sys.stderr,
        )
        return EXIT_PASS

    # Run validation
    findings = core_validate(
        issue_body=issue_body,
        pr_files=pr_files,
        pr_merge_sha=merge_sha,
        pr_parent_sha=parent_sha,
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
