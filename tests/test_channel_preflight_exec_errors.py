#!/usr/bin/env python3
"""Issue #438 F2 review: preflight execution errors are not "rejections".

``_validate_pack`` must distinguish a validator that actually ran and rejected
a negative fixture from an execution error (timeout / launch failure / staging
failure).  An execution error must never satisfy a negative fixture, and the
staged temp file must be cleaned up even when writing fails.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import validate_channel_preflight as cp  # noqa: E402


def test_validate_pack_timeout_returns_exec_error(monkeypatch):
    def _boom(*args, **kwargs):
        raise subprocess.TimeoutExpired(cmd="validate_research_pack.py", timeout=30)

    monkeypatch.setattr(cp.subprocess, "run", _boom)
    assert cp._validate_pack("## Objective\nok\n") == cp.EXEC_ERROR


def test_validate_pack_launch_failure_returns_exec_error(monkeypatch):
    def _boom(*args, **kwargs):
        raise FileNotFoundError("no interpreter")

    monkeypatch.setattr(cp.subprocess, "run", _boom)
    assert cp._validate_pack("## Objective\nok\n") == cp.EXEC_ERROR


def test_validate_pack_staging_failure_returns_exec_error(monkeypatch):
    def _boom(*args, **kwargs):
        raise OSError("cannot create temp file")

    monkeypatch.setattr(cp.tempfile, "NamedTemporaryFile", _boom)
    assert cp._validate_pack("## Objective\nok\n") == cp.EXEC_ERROR


def test_validate_pack_write_failure_cleans_temp(monkeypatch):
    created: dict[str, str] = {}
    real = tempfile.NamedTemporaryFile

    def _factory(*args, **kwargs):
        inner = real(*args, **kwargs)
        created["name"] = inner.name

        class _WriteFails:
            def __enter__(self_):
                inner.__enter__()
                return self_

            def __exit__(self_, *exc):
                return inner.__exit__(*exc)

            def __getattr__(self_, name):
                return getattr(inner, name)

            def write(self_, *a, **k):
                raise OSError("disk full")

        return _WriteFails()

    monkeypatch.setattr(cp.tempfile, "NamedTemporaryFile", _factory)
    rc = cp._validate_pack("## Objective\nok\n")
    assert rc == cp.EXEC_ERROR
    name = created.get("name")
    assert name, "fixture file should have been created"
    assert not Path(name).exists(), (
        "temp file must be cleaned up after a write failure"
    )


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
