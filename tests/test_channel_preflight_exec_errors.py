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
    assert cp._validate_pack("## Objective\nok\n")[0] == cp.EXEC_ERROR


def test_validate_pack_launch_failure_returns_exec_error(monkeypatch):
    def _boom(*args, **kwargs):
        raise FileNotFoundError("no interpreter")

    monkeypatch.setattr(cp.subprocess, "run", _boom)
    assert cp._validate_pack("## Objective\nok\n")[0] == cp.EXEC_ERROR


def test_validate_pack_staging_failure_returns_exec_error(monkeypatch):
    def _boom(*args, **kwargs):
        raise OSError("cannot create temp file")

    monkeypatch.setattr(cp.tempfile, "NamedTemporaryFile", _boom)
    assert cp._validate_pack("## Objective\nok\n")[0] == cp.EXEC_ERROR


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
    rc, _ = cp._validate_pack("## Objective\nok\n")
    assert rc == cp.EXEC_ERROR
    name = created.get("name")
    assert name, "fixture file should have been created"
    assert not Path(name).exists(), (
        "temp file must be cleaned up after a write failure"
    )


# ─── issue #438 third review: crashes / unexpected codes are not rejections ──


class _FakeCompleted:
    def __init__(self, returncode: int, stdout: str = ""):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = ""


def test_validate_pack_signal_killed_returns_exec_error(monkeypatch):
    # A validator killed by a signal (SIGKILL) comes back as a negative code;
    # it must be an execution error, not a rejection.
    monkeypatch.setattr(
        cp.subprocess, "run", lambda *a, **k: _FakeCompleted(-9)
    )
    assert cp._validate_pack("## Objective\nok\n")[0] == cp.EXEC_ERROR


def test_validate_pack_segfault_returns_exec_error(monkeypatch):
    monkeypatch.setattr(
        cp.subprocess, "run", lambda *a, **k: _FakeCompleted(-11)
    )
    assert cp._validate_pack("## Objective\nok\n")[0] == cp.EXEC_ERROR


def _stub_validate_pack(monkeypatch, disco_result):
    """Stub `_validate_pack`: valid fixtures pass (0), the DISCOVERY fixture
    returns `disco_result`."""

    def _stub(text, strict=False):
        if "DISCOVERY https://example.com" in text:
            return disco_result
        return 0, ""

    monkeypatch.setattr(cp, "_validate_pack", _stub)


def test_behavior_checks_fail_on_signal_terminated_disco(monkeypatch):
    # rc == EXEC_ERROR (signal / timeout) is not a valid rejection.
    _stub_validate_pack(monkeypatch, (cp.EXEC_ERROR, ""))
    failures = cp.run_behavior_checks()
    assert any("DISCOVERY" in f for f in failures), failures


def test_behavior_checks_fail_on_unexpected_nonzero_disco(monkeypatch):
    # A non-zero code that is NOT the expected DISCOVERY rejection (e.g. exit 2
    # = structure error) must not be accepted.
    _stub_validate_pack(monkeypatch, (2, "Missing required headings:"))
    failures = cp.run_behavior_checks()
    assert any("DISCOVERY" in f for f in failures), failures


def test_behavior_checks_fail_when_discovery_diagnostic_missing(monkeypatch):
    # The expected code alone is not enough — the DISCOVERY diagnostic must be
    # present on stdout.
    _stub_validate_pack(
        monkeypatch, (cp.PACK_EXIT_STRICT, "Strict mode issues:\n  ✗ something else")
    )
    failures = cp.run_behavior_checks()
    assert any("DISCOVERY" in f for f in failures), failures


def test_behavior_checks_pass_on_expected_disco_rejection(monkeypatch):
    _stub_validate_pack(
        monkeypatch,
        (cp.PACK_EXIT_STRICT, f"  ✗ {cp.DISCOVERY_DIAGNOSTIC}: - [S01] DISCOVERY ..."),
    )
    failures = cp.run_behavior_checks()
    assert not any("DISCOVERY" in f for f in failures), failures


def test_real_disco_fixture_rejects_with_expected_code():
    # Integration guard: the real fixture must actually be rejected with the
    # expected code and diagnostic (pins the assumption the stub encodes).
    rc, out = cp._validate_pack(cp._BAD_PACK_DISCOVERY_IN_REGISTER, strict=True)
    assert rc == cp.PACK_EXIT_STRICT, f"unexpected rc={rc}"
    assert cp.DISCOVERY_DIAGNOSTIC in out, out


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
