#!/usr/bin/env python3
"""Verify that md_to_pdf.py preflight catches missing dependencies with a clear error."""

import os
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = str(Path(__file__).resolve().parent / 'md_to_pdf.py')


def test_file_not_found_before_preflight() -> None:
    """File-not-found error should be reported even when deps are missing."""
    result = subprocess.run(
        [sys.executable, SCRIPT, '/nonexistent/input.md'],
        capture_output=True, text=True
    )
    assert result.returncode == 1, f"expected exit 1, got {result.returncode}"
    assert 'File not found' in result.stdout, (
        f"expected 'File not found' in stdout, got: {result.stdout}"
    )


def test_preflight_catches_missing_nh3() -> None:
    """Simulate missing nh3 via PYTHONPATH shim and verify clear error message."""
    with tempfile.TemporaryDirectory() as d:
        md_file = Path(d) / 'input.md'
        md_file.write_text('# Test\n\nHello.\n')

        shim_dir = Path(d) / '_shims'
        shim_dir.mkdir()
        (shim_dir / 'nh3.py').write_text('raise ImportError("simulated missing nh3")')

        env = os.environ.copy()
        pythonpath = str(shim_dir)
        if env.get('PYTHONPATH'):
            pythonpath += os.pathsep + env['PYTHONPATH']
        env['PYTHONPATH'] = pythonpath

        result = subprocess.run(
            [sys.executable, SCRIPT, str(md_file)],
            capture_output=True, text=True, env=env
        )
        assert result.returncode == 1, f"expected exit 1, got {result.returncode}"
        assert 'nh3' in result.stderr, f"'nh3' not in stderr: {result.stderr}"
        assert 'requirements.txt' in result.stderr, (
            f"'requirements.txt' not in stderr: {result.stderr}"
        )


def main() -> int:
    tests = [
        ('file-not-found before preflight', test_file_not_found_before_preflight),
        ('preflight catches missing nh3', test_preflight_catches_missing_nh3),
    ]
    failures = []
    for name, fn in tests:
        try:
            fn()
            print(f"  PASS  {name}")
        except AssertionError as e:
            print(f"  FAIL  {name}: {e}")
            failures.append(name)
    if failures:
        print(f"\n{len(failures)} test(s) failed: {', '.join(failures)}")
        return 1
    print(f"\nAll {len(tests)} tests passed.")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
