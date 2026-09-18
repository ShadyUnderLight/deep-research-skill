"""Path-conflict checks and atomic writes for delivery artifacts.

The delivery pipeline must never treat the input Markdown, a hardlink alias,
or a non-PDF path as the output target.  These helpers keep that
file-lifecycle contract in one place so the pipeline and the
Markdown-to-HTML facade cannot drift apart (issue #435).
"""

from __future__ import annotations

import os
import secrets
import stat
from pathlib import Path


def paths_collide(left: Path, right: Path) -> bool:
    """Return True when two paths denote the same file.

    Resolved equality catches ``a/../b`` and symlinked directories; the
    ``samefile`` check additionally catches hardlink aliases, which resolve
    to different paths but share one inode.
    """

    left = Path(left)
    right = Path(right)
    if left.resolve() == right.resolve():
        return True
    if left.exists() and right.exists():
        try:
            return left.samefile(right)
        except OSError:
            return False
    return False


def pdf_output_reason(path: Path) -> str | None:
    """Return a diagnostic when *path* is not a case-insensitive ``.pdf`` target."""

    suffix = Path(path).suffix.lower()
    if suffix != ".pdf":
        return (
            f"refusing non-PDF output target {path}: expected a .pdf path"
        )
    return None


def _create_sibling_temp(target: Path) -> tuple[int, Path]:
    """Create a sibling temp file with umask-derived permissions.

    ``os.open(..., O_CREAT | O_EXCL, 0o666)`` lets the kernel apply the
    process umask at creation time, so nothing has to read or mutate the
    process-global umask (issue #435 review round 2).
    """

    for _ in range(10):
        candidate = target.parent / f".{target.stem}-{secrets.token_hex(8)}.tmp"
        try:
            descriptor = os.open(candidate, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o666)
        except FileExistsError:
            continue
        return descriptor, candidate
    raise RuntimeError(f"could not create a temporary file next to {target}")


def commit_staged_file(staged: Path, target: Path) -> None:
    """Atomically move *staged* onto *target*, preserving the target's mode.

    ``os.replace`` swaps inodes, so the staged file's permissions would
    otherwise win; an existing artifact must keep its mode (issue #435
    review round 3).
    """

    staged = Path(staged)
    target = Path(target)
    try:
        existing_mode: int | None = stat.S_IMODE(target.stat().st_mode)
    except OSError:
        existing_mode = None
    if existing_mode is not None:
        os.chmod(staged, existing_mode)
    os.replace(staged, target)


def atomic_write_text(target: Path, text: str) -> None:
    """Write *text* via a sibling temp file, then atomically replace target.

    The temporary file lives in the target directory so ``os.replace`` stays
    on one filesystem, and a failed write never truncates an existing file.
    The final file keeps the previous target mode when one existed; new
    files get the kernel-applied umask default instead of ``0600``
    (issue #435 review rounds 1-3).
    """

    target = Path(target)
    descriptor, temp_path = _create_sibling_temp(target)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            stream.write(text)
        commit_staged_file(temp_path, target)
    except BaseException:
        temp_path.unlink(missing_ok=True)
        raise
