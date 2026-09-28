#!/usr/bin/env python3
"""Issue #438 F1: validators must fail closed and readable on bad input.

Acceptance target: missing file / bad JSON / bad UTF-8 / unreadable input
must return a structured, non-zero result WITHOUT an unhandled traceback.

Run via: python3 -m pytest tests/test_validator_read_errors.py

Note: temp files are created under /tmp (not pytest tmp_path) because the
sandbox blocks mkdir under /private/var/folders/... used by pytest's default
base temp dir.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
SCRIPTS = REPO / "scripts"

_KIND_BAD_JSON = b"{not valid json"
_KIND_BAD_UTF8 = b"\xff\xfe\x00broken"


def _run_cli(script: str, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPTS / script), *args],
        capture_output=True,
        text=True,
        timeout=60,
    )


def _assert_clean_failure(proc: subprocess.CompletedProcess, label: str) -> None:
    assert proc.returncode != 0, f"{label}: expected non-zero exit, got 0"
    assert "Traceback" not in proc.stderr, (
        f"{label}: unhandled traceback in stderr:\n{proc.stderr}"
    )


def _run_loader(
    mod: str,
    func: str,
    kind: str,
    expected: str,
    *,
    arg_mode: str = "path",
    global_name: str | None = None,
) -> None:
    """Invoke `<mod>.<func>` on a bad input file inside an isolated subprocess
    and assert it raises the expected exception type (no raw read/json crash).

    arg_mode="path":   call ``m.func(Path(path))``
    arg_mode="global": set ``m.<global_name> = Path(path)`` then call ``m.func()``
                       (for loaders that read a module-level path constant
                       instead of taking a path argument)
    """
    payload = _KIND_BAD_JSON if kind == "bad_json" else _KIND_BAD_UTF8
    inner = (
        "import sys, os, tempfile\n"
        "from pathlib import Path\n"
        "sys.path.insert(0, {scripts!r})\n"
        "import {mod} as m\n"
        "data = {payload!r}\n"
        "with tempfile.NamedTemporaryFile('wb', suffix='.bin', delete=False, dir='/tmp') as f:\n"
        "    f.write(data); path = f.name\n"
        "try:\n"
        "    if {arg_mode!r} == 'global':\n"
        "        setattr(m, {global_name!r}, Path(path))\n"
        "        m.{func}()\n"
        "    else:\n"
        "        m.{func}(Path(path))\n"
        "    sys.stdout.write('NO_RAISE')\n"
        "except BaseException as e:\n"
        "    sys.stdout.write('RAISED:' + type(e).__name__)\n"
        "finally:\n"
        "    try: os.unlink(path)\n"
        "    except OSError: pass\n"
    ).format(
        scripts=str(SCRIPTS),
        mod=mod,
        func=func,
        payload=payload,
        arg_mode=arg_mode,
        global_name=global_name,
    )
    proc = subprocess.run(
        [sys.executable, "-c", inner],
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert proc.returncode == 0, (
        f"{mod}.{func} loader subprocess failed: {proc.stderr}"
    )
    assert proc.stdout.startswith("RAISED:"), (
        f"{mod}.{func} did not raise on bad input (got {proc.stdout!r})"
    )
    name = proc.stdout.split(":", 1)[1]
    assert name == expected, (
        f"{mod}.{func} raised {name}, expected {expected}"
    )


# ── CLI-level: research pack ────────────────────────────────────────────────


def test_research_pack_missing_file():
    proc = _run_cli("validate_research_pack.py", "/no/such/pack.md")
    _assert_clean_failure(proc, "research_pack missing file")


def test_research_pack_bad_utf8():
    with tempfile.NamedTemporaryFile(
        "wb", suffix=".md", delete=False, dir="/tmp"
    ) as f:
        f.write(_KIND_BAD_UTF8)
        path = f.name
    try:
        proc = _run_cli("validate_research_pack.py", path)
    finally:
        import os

        try:
            os.unlink(path)
        except OSError:
            pass
    _assert_clean_failure(proc, "research_pack bad utf8")


# ── Loader-level: data-flow registry ────────────────────────────────────────


def test_data_flows_load_registry_bad_json():
    _run_loader(
        "validate_data_flows",
        "load_registry",
        "bad_json",
        "ValueError",
        arg_mode="global",
        global_name="REGISTRY_PATH",
    )


def test_data_flows_load_registry_bad_utf8():
    _run_loader(
        "validate_data_flows",
        "load_registry",
        "bad_utf8",
        "ValueError",
        arg_mode="global",
        global_name="REGISTRY_PATH",
    )


# ── Loader-level: eval registry ─────────────────────────────────────────────


def test_eval_registry_load_registry_bad_utf8():
    _run_loader("eval_registry", "load_registry", "bad_utf8", "EvalRegistryError")


# ── Loader-level: track handoff ─────────────────────────────────────────────


def test_track_handoff_load_bad_json():
    _run_loader(
        "validate_track_handoff",
        "load_handoff_for_merge",
        "bad_json",
        "HandoffIncomplete",
    )


def test_track_handoff_load_bad_utf8():
    _run_loader(
        "validate_track_handoff",
        "load_handoff_for_merge",
        "bad_utf8",
        "HandoffIncomplete",
    )


# ── Loader-level: route manifest ────────────────────────────────────────────


def test_route_manifest_load_manifest_bad_utf8():
    _run_loader(
        "validate_route_manifest", "_load_manifest", "bad_utf8", "SystemExit"
    )


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
