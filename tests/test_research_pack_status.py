"""Property-based tests for research_status and delivery_status validation.

Tests the new two-layer status fields added to Research Pack for Issue #365.
Validates that the validate_research_pack.py script correctly handles:
- Valid status values
- Invalid status values (strict mode failures)
- Missing statuses (conditional — not an error)
- Cross-layer consistency (e.g., blocked research + Pass audit)
"""

import os
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

# ── Paths ──────────────────────────────────────────────────────────────────

ROOT = Path(__file__).resolve().parent.parent
VALIDATOR = ROOT / "scripts" / "validate_research_pack.py"

# Markers: skip tests until implementation exists
# ── Baseline Research Pack (valid, all 12 required sections present) ─────

BASELINE = """\
## Objective
Test task.

## Decision context
Testing status validation.

## Primary route
Constrained choice / shortlist
Closest alternative: market-outlook (rejected — task asks "which" not "what will happen").
Boundary: if the question shifted to market trends, market-outlook would become primary.

## Secondary disciplines
source-traceability

## Core subquestions
Does the validator correctly check status fields?

## Stop condition
When tests pass.

## Source register
- [S01] Source: test source
  - Supports: test claim

## Claim register
- Claim: Status validation works. [S01]
  - Support: implementation
  - Confidence: medium

## Uncertainty register
- Uncertainty: edge cases
  - Why it matters: incorrect status could mislead

## Artifact contract
The report must validate correctly.

## Required audits
- final audit — passed

## Final audit status
Pass
"""


# ── Helpers ────────────────────────────────────────────────────────────────

def _run_strict(md_content: str) -> subprocess.CompletedProcess:
    """Run validate_research_pack.py --strict on the given content."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", delete=False, encoding="utf-8"
    ) as f:
        f.write(md_content)
        path = f.name
    try:
        return subprocess.run(
            [sys.executable, str(VALIDATOR), path, "--strict"],
            capture_output=True,
            text=True,
        )
    finally:
        os.unlink(path)


def _run_nonstrict(md_content: str) -> subprocess.CompletedProcess:
    """Run validate_research_pack.py (non-strict) on the given content."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", delete=False, encoding="utf-8"
    ) as f:
        f.write(md_content)
        path = f.name
    try:
        return subprocess.run(
            [sys.executable, str(VALIDATOR), path],
            capture_output=True,
            text=True,
        )
    finally:
        os.unlink(path)


def _inject_section(base: str, heading: str, body: str, *, after: str | None = None) -> str:
    """Inject a new ## heading section into the baseline.

    If `after` is provided, insert after that entire heading section
    (i.e. after the next ## heading or end of file).
    Otherwise, insert before '## Required audits'.
    """
    if after:
        marker = f"## {after}\n"
    else:
        marker = "## Required audits\n"

    idx = base.find(marker)
    if idx == -1:
        # Fallback: insert before the last ## heading
        idx = base.rfind("\n## ")
        if idx == -1:
            idx = len(base)

    # Find start of next ## heading after the target section
    rest = base[idx + len(marker):]
    next_h2 = rest.find("\n## ")
    if next_h2 == -1:
        insert_pos = len(base)
    else:
        insert_pos = idx + len(marker) + next_h2

    section = f"\n## {heading}\n{body}\n"
    return base[:insert_pos] + section + base[insert_pos:]


# ── Fixtures ───────────────────────────────────────────────────────────────

@pytest.fixture
def baseline() -> str:
    return BASELINE


@pytest.fixture
def valid_baseline_md() -> str:
    """Baseline with no extra sections — should pass non-strict."""
    return BASELINE


@pytest.fixture
def research_complete_md(baseline) -> str:
    return _inject_section(baseline, "Research status", "complete",
                           after="Uncertainty register")


@pytest.fixture
def research_partial_md(baseline) -> str:
    return _inject_section(baseline, "Research status", "partial",
                           after="Uncertainty register")


@pytest.fixture
def research_blocked_md(baseline) -> str:
    return _inject_section(baseline, "Research status", "blocked",
                           after="Uncertainty register")


@pytest.fixture
def delivery_md_ready_md(baseline) -> str:
    return _inject_section(baseline, "Delivery status", "md_ready",
                           after="Uncertainty register")


@pytest.fixture
def delivery_pdf_failed_md(baseline) -> str:
    return _inject_section(baseline, "Delivery status", "pdf_failed",
                           after="Uncertainty register")


@pytest.fixture
def delivery_not_run_md(baseline) -> str:
    return _inject_section(baseline, "Delivery status", "not_run",
                           after="Uncertainty register")


@pytest.fixture
def both_statuses_valid_md(baseline) -> str:
    """Research status + Delivery status both valid."""
    md = _inject_section(baseline, "Research status", "complete",
                         after="Uncertainty register")
    return _inject_section(md, "Delivery status", "md_ready",
                           after="Research status")


@pytest.fixture
def research_invalid_md(baseline) -> str:
    return _inject_section(baseline, "Research status", "not-sure",
                           after="Uncertainty register")


@pytest.fixture
def delivery_invalid_md(baseline) -> str:
    return _inject_section(baseline, "Delivery status", "broken",
                           after="Uncertainty register")


@pytest.fixture
def research_empty_md(baseline) -> str:
    return _inject_section(baseline, "Research status", "",
                           after="Uncertainty register")


@pytest.fixture
def blocked_with_pass_audit_md(baseline) -> str:
    """research_status=blocked but Final audit status=Pass — potential inconsistency."""
    md = _inject_section(baseline, "Research status", "blocked",
                         after="Uncertainty register")
    # Keep Final audit status as Pass
    return md


@pytest.fixture
def pdf_failed_with_pass_audit_md(baseline) -> str:
    """delivery_status=pdf_failed but Final audit status=Pass."""
    md = _inject_section(baseline, "Delivery status", "pdf_failed",
                         after="Uncertainty register")
    return md


@pytest.fixture
def all_three_statuses_md(baseline) -> str:
    """Research status + (existing Final audit) + Delivery status — complete picture."""
    md = _inject_section(baseline, "Research status", "complete",
                         after="Uncertainty register")
    md = _inject_section(md, "Delivery status", "md_ready",
                         after="Research status")
    return md


# ── Property Tests: Non-strict mode (status sections are conditional) ────


class TestResearchStatusNonStrict:
    """In non-strict mode, research_status and delivery_status are conditional.
    Missing or invalid statuses should NOT cause failure."""

    def test_baseline_passes_nonstrict(self, valid_baseline_md):
        result = _run_nonstrict(valid_baseline_md)
        assert result.returncode == 0, f"expected exit 0, got {result.returncode}\n{result.stdout}"

    def test_research_complete_passes_nonstrict(self, research_complete_md):
        result = _run_nonstrict(research_complete_md)
        assert result.returncode == 0, f"expected exit 0, got {result.returncode}\n{result.stdout}"

    def test_delivery_md_ready_passes_nonstrict(self, delivery_md_ready_md):
        result = _run_nonstrict(delivery_md_ready_md)
        assert result.returncode == 0, f"expected exit 0, got {result.returncode}\n{result.stdout}"


# ── Property Tests: Strict mode — valid statuses ──────────────────────────



class TestResearchStatusValid:
    """Valid research_status values should pass strict mode."""

    def test_complete_passes_strict(self, research_complete_md):
        result = _run_strict(research_complete_md)
        assert result.returncode == 0, f"expected exit 0, got {result.returncode}\n{result.stdout}"

    def test_partial_passes_strict(self, research_partial_md):
        result = _run_strict(research_partial_md)
        assert result.returncode == 0, f"expected exit 0, got {result.returncode}\n{result.stdout}"

    def test_blocked_passes_strict(self, research_blocked_md):
        result = _run_strict(research_blocked_md)
        assert result.returncode == 0, f"expected exit 0, got {result.returncode}\n{result.stdout}"



class TestDeliveryStatusValid:
    """Valid delivery_status values should pass strict mode."""

    def test_md_ready_passes_strict(self, delivery_md_ready_md):
        result = _run_strict(delivery_md_ready_md)
        assert result.returncode == 0, f"expected exit 0, got {result.returncode}\n{result.stdout}"

    def test_pdf_ready_passes_strict(self, baseline):
        md = _inject_section(baseline, "Delivery status", "pdf_ready",
                             after="Uncertainty register")
        result = _run_strict(md)
        assert result.returncode == 0, f"expected exit 0, got {result.returncode}\n{result.stdout}"

    def test_pdf_failed_passes_strict(self, delivery_pdf_failed_md):
        result = _run_strict(delivery_pdf_failed_md)
        assert result.returncode == 0, f"expected exit 0, got {result.returncode}\n{result.stdout}"

    def test_not_run_passes_strict(self, delivery_not_run_md):
        result = _run_strict(delivery_not_run_md)
        assert result.returncode == 0, f"expected exit 0, got {result.returncode}\n{result.stdout}"

    def test_trailing_comment_accepted(self, baseline):
        """Status with trailing comment (matching audit_status word-boundary
        pattern) should pass."""
        md = _inject_section(baseline, "Research status",
                             "complete — verified by external review",
                             after="Uncertainty register")
        assert _run_strict(md).returncode == 0
        md2 = _inject_section(baseline, "Delivery status",
                              "md_ready — all checks passed",
                              after="Uncertainty register")
        assert _run_strict(md2).returncode == 0



class TestBothStatusesValid:
    """Both research_status and delivery_status valid simultaneously."""

    def test_both_valid_passes_strict(self, both_statuses_valid_md):
        result = _run_strict(both_statuses_valid_md)
        assert result.returncode == 0, f"expected exit 0, got {result.returncode}\n{result.stdout}"

    def test_all_three_layers_passes_strict(self, all_three_statuses_md):
        result = _run_strict(all_three_statuses_md)
        assert result.returncode == 0, f"expected exit 0, got {result.returncode}\n{result.stdout}"


# ── Property Tests: Strict mode — invalid statuses ──────────────────────



class TestResearchStatusInvalid:
    """Invalid research_status values should fail strict mode with exit 4."""

    def test_invalid_fails_strict(self, research_invalid_md):
        result = _run_strict(research_invalid_md)
        assert result.returncode == 4, (
            f"expected exit 4 for invalid research_status, got {result.returncode}\n{result.stdout}"
        )
        assert "research" in result.stdout.lower(), (
            f"expected 'research' in error output: {result.stdout}"
        )

    def test_empty_fails_strict(self, research_empty_md):
        result = _run_strict(research_empty_md)
        assert result.returncode == 4, (
            f"expected exit 4 for empty research_status, got {result.returncode}\n{result.stdout}"
        )



class TestDeliveryStatusInvalid:
    """Invalid delivery_status values should fail strict mode with exit 4."""

    def test_invalid_fails_strict(self, delivery_invalid_md):
        result = _run_strict(delivery_invalid_md)
        assert result.returncode == 4, (
            f"expected exit 4 for invalid delivery_status, got {result.returncode}\n{result.stdout}"
        )
        assert "delivery" in result.stdout.lower(), (
            f"expected 'delivery' in error output: {result.stdout}"
        )


# ── Property Tests: Cross-layer consistency ─────────────────────────────



class TestCrossLayerConsistency:
    """Cross-layer consistency checks between research/audit/delivery statuses."""

    def test_blocked_research_with_pass_audit_is_valid(self, blocked_with_pass_audit_md):
        """research_status=blocked + Final audit=Pass — valid state.
        Blocked research means external channels unavailable, but content audit
        checks the quality of what WAS produced. These are independent layers.
        Cross-layer consistency is NOT enforced (by design, per CoT vote C)."""
        result = _run_strict(blocked_with_pass_audit_md)
        assert result.returncode == 0, (
            f"blocked + Pass audit is valid (research ≠ quality), "
            f"got exit {result.returncode}: {result.stdout}"
        )

    def test_pdf_failed_with_pass_audit_is_valid(self, pdf_failed_with_pass_audit_md):
        """delivery_status=pdf_failed + Final audit=Pass — valid state.
        PDF rendering failure is a delivery concern, independent of content audit.
        Cross-layer consistency is NOT enforced (by design, per CoT vote C)."""
        result = _run_strict(pdf_failed_with_pass_audit_md)
        assert result.returncode == 0, (
            f"pdf_failed + Pass audit is valid (delivery ≠ quality), "
            f"got exit {result.returncode}: {result.stdout}"
        )


# ── Edge case: Missing status sections ─────────────────────────────────



class TestMissingStatusSections:
    """Missing research_status/delivery_status sections should NOT be errors.
    These are conditional sections — backward compatible."""

    def test_baseline_without_status_sections_passes_strict(self, valid_baseline_md):
        """Baseline without research_status or delivery_status should pass strict."""
        result = _run_strict(valid_baseline_md)
        assert result.returncode == 0, (
            f"baseline without status sections should pass strict, "
            f"got exit {result.returncode}: {result.stdout}"
        )

    def test_only_research_status_passes(self, research_complete_md):
        """Having only research_status (no delivery_status) should still pass."""
        result = _run_strict(research_complete_md)
        assert result.returncode == 0, f"expected exit 0, got {result.returncode}\n{result.stdout}"

    def test_only_delivery_status_passes(self, delivery_md_ready_md):
        """Having only delivery_status (no research_status) should still pass."""
        result = _run_strict(delivery_md_ready_md)
        assert result.returncode == 0, f"expected exit 0, got {result.returncode}\n{result.stdout}"
