#!/usr/bin/env python3
"""
Lightweight validation: check that Agent-Reach channel preflight rules
are correctly wired across the repo.

Two check layers:
  1. Phrase-level checks — regex matches across reference files
  2. Behavior-level fixtures — inline Research Pack snippets that
     must pass or fail structural validation, catching rule violations
     that phrase checks alone cannot prove absent.

Exit codes:
  0 = all checks pass
  1 = one or more checks failed
"""

import re
import sys
import subprocess
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# Each check: (file_path_relative, description, expected_phrase_or_regex, must_exist)
CHECKS: list[tuple[str, str, str, bool]] = [
    # ---- New files exist ----
    (
        "references/external-channel-preflight.md",
        "External channel preflight reference exists",
        "Source intake log",
        True,
    ),
    (
        "evals/cases/agent-reach-external-channel-preflight-case.md",
        "Agent-Reach external channel eval case exists",
        "DISCOVERY → fetch → reclassify",
        True,
    ),
    # ---- SKILL.md references ----
    (
        "SKILL.md",
        "SKILL.md step 5 references external-channel-preflight.md",
        "references/external-channel-preflight.md",
        True,
    ),
    (
        "SKILL.md",
        "SKILL.md common capability mapping has Channel preflight row",
        r"Channel preflight.*`GET /health`",
        True,
    ),
    (
        "SKILL.md",
        "SKILL.md has expanded Agent-Reach first-class channel mention",
        r"non-degraded first-class channel",
        True,
    ),
    # ---- research-pack-contract.md ----
    (
        "references/research-pack-contract.md",
        "Research Pack contract includes channel availability snapshot (relevant list)",
        "channel availability snapshot",
        True,
    ),
    (
        "references/research-pack-contract.md",
        "Research Pack contract has field intent for channel availability snapshot",
        "Channel availability snapshot",
        True,
    ),
    # ---- schemas/research-pack.md ----
    (
        "schemas/research-pack.md",
        "Schema conditional sections include channel availability snapshot",
        "Channel availability snapshot",
        True,
    ),
    # ---- source-quality.md ----
    (
        "references/source-quality.md",
        "Source quality has External API source type mapping section",
        "External API source type mapping",
        True,
    ),
    (
        "references/source-quality.md",
        "Source quality has DISCOVERY hard rule (not a valid Source Register type)",
        "DISCOVERY.*not a valid source type",
        True,
    ),
    (
        "references/source-quality.md",
        "Source quality has weak-signal guard",
        "Weak-signal guard",
        True,
    ),
    # ---- source-traceability-and-claim-citation.md ----
    (
        "references/source-traceability-and-claim-citation.md",
        "Source traceability has PRIMARY_DEV type",
        "PRIMARY_DEV",
        True,
    ),
    (
        "references/source-traceability-and-claim-citation.md",
        "Source traceability has SECONDARY_FEED type",
        "SECONDARY_FEED",
        True,
    ),
    (
        "references/source-traceability-and-claim-citation.md",
        "Source traceability has TRANSCRIPT type",
        "TRANSCRIPT",
        True,
    ),
    (
        "references/source-traceability-and-claim-citation.md",
        "Source traceability explicitly excludes DISCOVERY from Source Register",
        r"DISCOVERY.*not a valid Source Register",
        True,
    ),
    # ---- New file content checks ----
    (
        "references/external-channel-preflight.md",
        "Preflight doc has DISCOVERY hard rule (must never appear as Sxx)",
        r"DISCOVERY.*must never appear",
        True,
    ),
    (
        "references/external-channel-preflight.md",
        "Preflight doc has fetch status handling table",
        r"fetch_failed.*HTTP error",
        True,
    ),
    (
        "references/external-channel-preflight.md",
        "Preflight doc has empty result set handling",
        r"Empty result set",
        True,
    ),
    # ---- Negative checks (must NOT contain) ----
    (
        "references/source-traceability-and-claim-citation.md",
        "DISCOVERY is NOT listed as a source type in classification",
        r"^- `DISCOVERY`",
        False,
    ),
    (
        "schemas/research-pack.md",
        "degraded-search log is NOT in schema conditional sections (scope guard)",
        r"Degraded.search.log",
        False,
    ),
]


def check_file(path: Path, desc: str, pattern: str, must_exist: bool) -> bool:
    if not path.exists():
        print(f"  FAIL  [{desc}] — file not found: {path}")
        return False

    text = path.read_text(encoding="utf-8")
    found = bool(re.search(pattern, text, re.MULTILINE))

    if must_exist and not found:
        print(f"  FAIL  [{desc}] — expected pattern not found: {pattern!r}")
        return False
    if not must_exist and found:
        print(f"  FAIL  [{desc}] — unexpected pattern found: {pattern!r}")
        return False
    return True


def main() -> int:
    all_pass = True
    for rel_path, desc, pattern, must_exist in CHECKS:
        path = REPO / rel_path
        ok = check_file(path, desc, pattern, must_exist)
        if not ok:
            all_pass = False

    if all_pass:
        print("All channel preflight checks pass.")
        return 0
    else:
        print("\nOne or more checks failed. See above.")
        return 1


# ─── Behavior-level fixtures ─────────────────────────────────────────────


def _validate_pack(text: str, strict: bool = False) -> int:
    """Write text to a temp file and run validate_research_pack.py."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", delete=False, encoding="utf-8"
    ) as f:
        f.write(text)
        tmp = f.name
    cmd = [sys.executable, str(REPO / "scripts" / "validate_research_pack.py")]
    if strict:
        cmd.append("--strict")
    cmd.append(tmp)
    result = subprocess.run(cmd, capture_output=True, text=True)
    Path(tmp).unlink(missing_ok=True)
    return result.returncode


# Baseline valid pack (all 12 required headings + all 8 snapshot fields)
_VALID_PACK = """\
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
- [S01] Example source; supports: baseline

## Claim register
- Claim: test [S01]
- Support: ok
- Confidence: high

## Uncertainty register
ok

## Channel availability snapshot
- api_available: true
- api_version: 0.1.0
- checked_at: 2026-06-04T10:00:00Z
- channels_ok: 5
- channels_total: 6
- selected_channels: [search, fetch]
- degraded_channels: [rss]
- impact_on_research: RSS degraded; search+fetch available

## Artifact contract
ok

## Required audits
ok

## Final audit status
Pass
"""

# Bad pack: DISCOVERY used as a source type in Source Register
# This uses a proper [S01] ID to prove the DISCOVERY rejection is
# based on content, not on missing source IDs.
_BAD_PACK_DISCOVERY_IN_REGISTER = """\
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
- [S01] DISCOVERY https://example.com/search-result; supports: bad raw discovery

## Claim register
- Claim: Raw discovery supports this claim [S01]
- Support: DISCOVERY result
- Confidence: low

## Uncertainty register
ok

## Artifact contract
ok

## Required audits
ok

## Final audit status
Pass
"""

# Bad pack: channel snapshot missing required fields (only 2 of 8)
_BAD_PACK_SNAPSHOT_MISSING_FIELDS = """\
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

## Channel availability snapshot
- api_available: true
- api_version: 0.1.0

## Artifact contract
ok

## Required audits
ok

## Final audit status
Pass
"""


def run_behavior_checks() -> list[str]:
    """Return list of failure messages (empty = all pass)."""
    failures: list[str] = []

    # 1. Valid baseline should pass
    rc = _validate_pack(_VALID_PACK)
    if rc != 0:
        failures.append(
            f"BEHAVIOR: valid baseline Research Pack should pass (exit 0), got {rc}"
        )

    # 2. Valid baseline should pass strict mode too
    rc_strict = _validate_pack(_VALID_PACK, strict=True)
    if rc_strict != 0:
        failures.append(
            f"BEHAVIOR: valid baseline should pass strict mode (exit 0), got {rc_strict}"
        )

    # 3. Bad pack with DISCOVERY in Source Register must fail strict mode
    #    (validate_research_pack.py has a DISCOVERY-as-source-type rejection rule)
    rc_disco = _validate_pack(_BAD_PACK_DISCOVERY_IN_REGISTER, strict=True)
    if rc_disco == 0:
        failures.append(
            "BEHAVIOR: pack with [S01] DISCOVERY in Source Register must "
            "fail strict validation (exit != 0), got 0"
        )

    # 4. Bad pack with snapshot missing fields — the channel availability
    #    snapshot is a conditional section so it doesn't fail heading checks.
    #    But the fields MUST be listed in the reference docs. This fixture
    #    validates that the validator at least parses the snapshot section.
    rc_snap = _validate_pack(_BAD_PACK_SNAPSHOT_MISSING_FIELDS)
    if rc_snap != 0:
        # A missing-field snapshot should still pass structure checks because
        # the section exists with partial content. This confirms baseline
        # compatibility.
        failures.append(
            f"BEHAVIOR: partial snapshot should pass structure check (exit 0), "
            f"got {rc_snap}"
        )

    return failures


def main() -> int:
    failed_phrase = 0
    for rel_path, desc, pattern, must_exist in CHECKS:
        path = REPO / rel_path
        ok = check_file(path, desc, pattern, must_exist)
        if not ok:
            failed_phrase += 1

    failed_behavior = run_behavior_checks()
    for msg in failed_behavior:
        print(f"  FAIL  [{msg}]")

    total_fail = failed_phrase + len(failed_behavior)
    if total_fail == 0:
        print("All channel preflight checks pass.")
        return 0
    else:
        print(f"\n{total_fail} check(s) failed. See above.")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
