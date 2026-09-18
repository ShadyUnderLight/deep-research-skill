"""Path-conflict checks and atomic writes for delivery artifacts.

The delivery pipeline must never treat the input Markdown, a hardlink alias,
or an HTML intermediate as an output target for a different artifact.  These
helpers keep that file-lifecycle contract in one place so the pipeline and
the Markdown-to-HTML facade cannot drift apart (issue #435).
"""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

# Suffixes that denote source or intermediate artifacts.  Writing a PDF (or
# replacing the file with PDF bytes) over these paths is always a bug, even
# when the paths are not aliases of each other.
RESERVED_OUTPUT_SUFFIXES = frozenset({".md", ".markdown", ".html", ".htm"})


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


def reserved_output_reason(path: Path) -> str | None:
    """Return a diagnostic when *path* has a reserved source suffix."""

    suffix = Path(path).suffix.lower()
    if suffix in RESERVED_OUTPUT_SUFFIXES:
        return f"refusing to use reserved {suffix} path as a PDF output: {path}"
    return None


def atomic_write_text(target: Path, text: str) -> None:
    """Write *text* via a sibling temp file, then atomically replace target.

    The temporary file lives in the target directory so ``os.replace`` stays
    on one filesystem, and a failed write never truncates an existing file.
    """

    target = Path(target)
    descriptor, temp_name = tempfile.mkstemp(
        prefix=f".{target.stem}-", suffix=".tmp", dir=target.parent
    )
    temp_path = Path(temp_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            stream.write(text)
        os.replace(temp_path, target)
    except BaseException:
        temp_path.unlink(missing_ok=True)
        raise
