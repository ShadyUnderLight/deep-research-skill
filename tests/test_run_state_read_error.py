#!/usr/bin/env python3
"""Issue #438 review: a run-state read failure is not "no declared state".

`load_declared_run_state` must not swallow read errors into ``None`` — that
would make "cannot read the Pack" indistinguishable from "the Pack declares
no Run State", silently skipping the audit delivery guard.  A read failure is
recorded as an explicit, blocking audit problem.
"""

from __future__ import annotations

import shutil
import sys
import tempfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_research_run_state import load_declared_run_state  # noqa: E402


def test_load_declared_run_state_raises_on_unreadable_pack():
    # A directory exists but cannot be read as UTF-8 text -> OSError
    # (IsADirectoryError). It must NOT be reported as "no declared state".
    tmp_dir = tempfile.mkdtemp(dir="/tmp")
    try:
        with pytest.raises(OSError):
            load_declared_run_state(tmp_dir)
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def test_delivery_guard_blocks_on_unreadable_pack():
    from audit_report import (  # noqa: E402
        EXIT_BLOCKING,
        AuditVerdict,
        _apply_run_state_delivery_guard,
    )

    tmp_dir = tempfile.mkdtemp(dir="/tmp")
    try:
        verdict = AuditVerdict(route=None, overall="pass")
        out = _apply_run_state_delivery_guard(verdict, Path(tmp_dir))
        assert out.blocking, "unreadable Pack must record a blocking issue"
        assert out.exit_code == EXIT_BLOCKING
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def _write_bad_utf8_pack() -> Path:
    with tempfile.NamedTemporaryFile(suffix=".md", dir="/tmp", delete=False) as f:
        f.write(b"\xff\xfe## Run State\n")  # invalid UTF-8
        return Path(f.name)


def test_load_declared_run_state_raises_on_bad_utf8_pack():
    # A file that is not valid UTF-8 raises UnicodeError — it must NOT be
    # reported as "no declared state".
    pack = _write_bad_utf8_pack()
    try:
        with pytest.raises(UnicodeError):
            load_declared_run_state(pack)
    finally:
        pack.unlink(missing_ok=True)


def test_delivery_guard_blocks_on_bad_utf8_pack():
    from audit_report import (  # noqa: E402
        EXIT_BLOCKING,
        AuditVerdict,
        _apply_run_state_delivery_guard,
    )

    pack = _write_bad_utf8_pack()
    try:
        verdict = AuditVerdict(route=None, overall="pass")
        out = _apply_run_state_delivery_guard(verdict, pack)
        assert out.blocking, "bad-UTF-8 Pack must record a blocking issue"
        assert out.exit_code == EXIT_BLOCKING
    finally:
        pack.unlink(missing_ok=True)


# ── issue #438 fourth review: a *declared* Run State that cannot be verified ──


def _pack_in_tmpdir(body: str) -> tuple[Path, Path]:
    """Create a temp dir under /tmp holding pack.md; return (dir, pack)."""
    d = Path(tempfile.mkdtemp(dir="/tmp"))
    pack = d / "pack.md"
    pack.write_text(body, encoding="utf-8")
    return d, pack


def test_load_declared_run_state_returns_none_when_section_absent():
    d, pack = _pack_in_tmpdir("# Pack\n\n## Objective\nok\n")
    try:
        assert load_declared_run_state(pack) is None
    finally:
        shutil.rmtree(d, ignore_errors=True)


def test_load_declared_run_state_raises_on_malformed_declaration():
    # Section present but missing `path` → declared, yet unverifiable.
    from validate_research_run_state import RunStateDeclarationError  # noqa: E402

    d, pack = _pack_in_tmpdir("## Run state\nrun_id: r1\n")
    try:
        with pytest.raises(RunStateDeclarationError):
            load_declared_run_state(pack)
    finally:
        shutil.rmtree(d, ignore_errors=True)


def test_load_declared_run_state_raises_on_missing_sidecar():
    from validate_research_run_state import RunStateDeclarationError  # noqa: E402

    d, pack = _pack_in_tmpdir("## Run state\nrun_id: r1\npath: nope.json\n")
    try:
        with pytest.raises(RunStateDeclarationError):
            load_declared_run_state(pack)
    finally:
        shutil.rmtree(d, ignore_errors=True)


def test_load_declared_run_state_raises_on_invalid_sidecar_json():
    from validate_research_run_state import RunStateDeclarationError  # noqa: E402

    d, pack = _pack_in_tmpdir("## Run state\nrun_id: r1\npath: run-state.json\n")
    try:
        (d / "run-state.json").write_text("{not json", encoding="utf-8")
        with pytest.raises(RunStateDeclarationError):
            load_declared_run_state(pack)
    finally:
        shutil.rmtree(d, ignore_errors=True)


def test_delivery_guard_blocks_on_unverifiable_declaration():
    from audit_report import (  # noqa: E402
        EXIT_BLOCKING,
        AuditVerdict,
        _apply_run_state_delivery_guard,
    )

    d, pack = _pack_in_tmpdir("## Run state\nrun_id: r1\npath: nope.json\n")
    try:
        verdict = AuditVerdict(route=None, overall="pass")
        out = _apply_run_state_delivery_guard(verdict, pack)
        assert out.blocking, "unverifiable declaration must record a blocking issue"
        assert out.exit_code == EXIT_BLOCKING
    finally:
        shutil.rmtree(d, ignore_errors=True)


def test_delivery_guard_does_not_block_when_no_declaration():
    from audit_report import (  # noqa: E402
        AuditVerdict,
        _apply_run_state_delivery_guard,
    )

    d, pack = _pack_in_tmpdir("# Pack\n\n## Objective\nok\n")
    try:
        verdict = AuditVerdict(route=None, overall="pass")
        out = _apply_run_state_delivery_guard(verdict, pack)
        assert not out.blocking, "a Pack with no Run State must keep the verdict"
    finally:
        shutil.rmtree(d, ignore_errors=True)



if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
