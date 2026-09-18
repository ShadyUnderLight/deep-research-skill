"""Path-conflict checks and atomic writes for delivery artifacts.

The delivery pipeline must never treat the input Markdown, a hardlink alias,
or a non-PDF path as the output target.  These helpers keep that
file-lifecycle contract in one place so the pipeline and the
Markdown-to-HTML facade cannot drift apart (issue #435).
"""

from __future__ import annotations

import os
import stat
import tempfile
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


def _default_file_mode() -> int:
    """Mode for a brand-new artifact, respecting the process umask."""

    umask = os.umask(0)
    os.umask(umask)
    return 0o666 & ~umask


def atomic_write_text(target: Path, text: str) -> None:
    """Write *text* via a sibling temp file, then atomically replace target.

    The temporary file lives in the target directory so ``os.replace`` stays
    on one filesystem, and a failed write never truncates an existing file.
    The final file keeps the previous target mode when one existed; new
    files use the umask-derived default instead of ``mkstemp``'s ``0600``
    (issue #435 review round 1).
    """

    target = Path(target)
    try:
        existing_mode: int | None = stat.S_IMODE(target.stat().st_mode)
    except OSError:
        existing_mode = None

    descriptor, temp_name = tempfile.mkstemp(
        prefix=f".{target.stem}-", suffix=".tmp", dir=target.parent
    )
    temp_path = Path(temp_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            stream.write(text)
        os.chmod(
            temp_path,
            existing_mode if existing_mode is not None else _default_file_mode(),
        )
        os.replace(temp_path, target)
    except BaseException:
        temp_path.unlink(missing_ok=True)
        raise
