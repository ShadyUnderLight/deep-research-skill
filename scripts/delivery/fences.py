"""Shared CommonMark fenced-code boundary tracking for delivery transforms.

Normalization and table repair both need to know which lines are code
fence content.  They share this single state machine so the boundary rule
cannot drift between the two transforms (issue #435), and its semantics
match the canonical fence handling used by the validators (issue #378):
backtick and tilde fences, an info string that must not contain backticks
for backtick fences, up to three leading spaces, and a closing fence that is
at least as long as the opener and carries nothing but spaces/tabs.
"""

from __future__ import annotations

import re
from collections.abc import Iterator

FENCE_OPEN_RE = re.compile(r"^[ ]{0,3}(`{3,}|~{3,})(.*)$")


def fence_open(line: str) -> tuple[str, int] | None:
    """Return ``(fence_char, fence_length)`` when *line* opens a fence."""

    match = FENCE_OPEN_RE.match(line)
    if match is None:
        return None
    marker = match.group(1)
    if marker[0] == "`" and "`" in match.group(2):
        return None
    return marker[0], len(marker)


def fence_close_re(fence_char: str, fence_length: int) -> re.Pattern[str]:
    """Closing fence: same char, >= opener length, trailing spaces/tabs only."""

    return re.compile(
        rf"^[ ]{{0,3}}{re.escape(fence_char)}{{{fence_length},}}[\t ]*$"
    )


def iter_fence_aware_lines(text: str) -> Iterator[tuple[str, bool]]:
    """Yield ``(line, in_fence)`` for every line in *text*.

    Fence opener, content, and closer lines are all reported as
    ``in_fence=True``.  An unclosed fence marks the rest of the text as code.
    A trailing carriage return is ignored for fence *detection* (so CRLF
    input is recognized) while the yielded line stays byte-identical.
    """

    close_re: re.Pattern[str] | None = None
    in_fence = False
    for raw in text.split("\n"):
        line = raw[:-1] if raw.endswith("\r") else raw
        if not in_fence:
            opener = fence_open(line)
            if opener is not None:
                close_re = fence_close_re(*opener)
                in_fence = True
            yield raw, in_fence
            continue
        yield raw, True
        if close_re is not None and close_re.match(line):
            in_fence = False
            close_re = None


def fence_aware_runs(text: str) -> list[tuple[list[str], bool]]:
    """Group lines into consecutive ``(lines, in_fence)`` runs."""

    runs: list[tuple[list[str], bool]] = []
    for line, in_fence in iter_fence_aware_lines(text):
        if runs and runs[-1][1] == in_fence:
            runs[-1][0].append(line)
        else:
            runs.append(([line], in_fence))
    return runs
