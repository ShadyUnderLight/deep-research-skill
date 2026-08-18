"""Production Research Pack validator coverage for Issue 391."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_research_pack.py"
PACK = ROOT / "tests" / "fixtures" / "forward" / "market-outlook-baseline-pack.md"


def _run(path: Path, *, strict: bool = False) -> subprocess.CompletedProcess[str]:
    args = [sys.executable, str(VALIDATOR), str(path)]
    if strict:
        args.append("--strict")
    return subprocess.run(
        args,
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def test_production_validator_accepts_current_decision_tree_version() -> None:
    result = _run(PACK, strict=True)
    assert result.returncode == 0, result.stdout + result.stderr


def test_production_validator_warns_and_strictly_rejects_stale_version(
    tmp_path: Path,
) -> None:
    stale = tmp_path / "stale-pack.md"
    text = PACK.read_text(encoding="utf-8")
    stale.write_text(text.replace("\n1\n\n## Secondary disciplines", "\n999\n\n## Secondary disciplines", 1), encoding="utf-8")

    normal = _run(stale)
    assert normal.returncode == 0
    assert "Decision tree version" in normal.stdout
    assert "canonical version" in normal.stdout

    strict = _run(stale, strict=True)
    assert strict.returncode != 0
    assert "Decision tree version 999" in strict.stdout
