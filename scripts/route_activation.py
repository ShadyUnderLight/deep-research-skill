#!/usr/bin/env python3
"""Fail-closed offline adapter for the route-selection decision tree.

Forward evals provide canonical action/object classifications explicitly.  This
module resolves those structured values against ``ROUTING-MATRIX.md`` and keeps
the original user prompt as an identity-checked input.  It intentionally does
not guess from arbitrary prose or fall back to ``shared-workflow``.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path

try:
    from registry_loader import load_route_registry
except ImportError:  # pragma: no cover - package import fallback
    from .registry_loader import load_route_registry  # type: ignore[no-redef]


ROOT = Path(__file__).resolve().parents[1]
ROUTING_MATRIX = ROOT / "ROUTING-MATRIX.md"
ALLOWED_PARALLELIZATION = {"single-track", "parallel", "not-needed"}
ACTION_CATEGORIES = {
    "Select / rank / predict",
    "Enter / phase / sequence",
    "Judge direction / scenario",
    "Judge regulation / policy impact",
    "Judge listed-company value",
    "Judge private-company quality",
    "Judge technical mechanism / feasibility",
    "Judge academic evidence / research",
    "Judge positioning / tier",
    "shared-workflow",
}
OBJECT_CATEGORIES = {
    "Defined options / teams / ranking",
    "Providers / vendors / APIs / models",
    "Devices / hardware / build",
    "Market / category trajectory",
    "Regulation / rules / policy",
    "Listed / public company",
    "Private / startup company",
    "Architecture / mechanism / patent",
    "Academic literature / research evidence",
    "Positioning / tier label",
    "Entry decision / sequencing / gates",
    "shared-workflow",
}


class RouteActivationError(ValueError):
    """Raised when a structured activation input is incomplete or invalid."""


@dataclass(frozen=True)
class ActivationResult:
    primary_route: str
    secondary_routes: tuple[str, ...]
    action_category: str
    weight_bearing_object: str
    parallelization_decision: str
    prompt_sha256: str
    mode: str = "offline-decision-tree-structured"


def _section_after_heading(content: str, heading: str) -> str:
    start = content.find(heading)
    if start == -1:
        return ""
    section = content[start:]
    rest = section[section.index("\n") + 1:]
    next_heading = re.search(r"\n## ", rest)
    if next_heading:
        rest = rest[:next_heading.start() + 1]
    return rest


def _step2_object_routes() -> dict[str, list[str]]:
    try:
        content = ROUTING_MATRIX.read_text(encoding="utf-8")
    except OSError as exc:
        raise RouteActivationError(f"cannot read {ROUTING_MATRIX}: {exc}") from exc
    decision_tree = _section_after_heading(content, "## Route selection decision tree")
    start = decision_tree.find("### Step 2")
    if start == -1:
        raise RouteActivationError("ROUTING-MATRIX.md is missing Step 2")
    section = decision_tree[start:]
    next_h3 = re.search(r"\n### Step 3\b", section)
    if next_h3:
        section = section[:next_h3.start() + 1]

    mapping: dict[str, list[str]] = {}
    in_table = False
    for line in section.splitlines():
        stripped = line.strip()
        if stripped.startswith("| Weight-bearing object"):
            in_table = True
            continue
        if not in_table or stripped.startswith("|---"):
            continue
        if stripped.startswith("|") and "`" in stripped:
            columns = [cell.strip() for cell in stripped.strip("|").split("|")]
            if len(columns) >= 2:
                route_ids = re.findall(r"`([a-z]+(?:-[a-z]+)*)`", columns[1])
                if route_ids and columns[0]:
                    mapping[columns[0]] = route_ids
        elif stripped.startswith("When an object matches"):
            break
    return mapping


def _normalize_label(value: str) -> str:
    return re.sub(r"\s*/\s*", "/", value.lower())


_CONFLICT_PAIRS: dict[tuple[str, str], tuple[str, tuple[str, ...]]] = {
    ("select/rank", "market"): ("constrained-choice", ()),
    ("enter/phase", "defined options"): ("market-entry", ()),
    ("listed-company", "architecture"): ("listed-company", ("technical-deep-dive",)),
    ("academic evidence", "architecture"): ("academic-review", ()),
    ("regulation", "market"): ("regulatory-analysis", ("market-outlook",)),
    ("technical", "listed"): ("technical-deep-dive", ()),
    ("technical", "academic"): ("technical-deep-dive", ()),
}


def _resolve_route(action_category: str, weight_bearing_object: str) -> tuple[str, tuple[str, ...]]:
    action = _normalize_label(action_category)
    obj = _normalize_label(weight_bearing_object)
    for (action_fragment, object_fragment), result in _CONFLICT_PAIRS.items():
        if action_fragment in action and object_fragment in obj:
            return result
    candidates = _step2_object_routes().get(weight_bearing_object, [])
    if not candidates:
        raise RouteActivationError(
            f"no route candidate for structured object '{weight_bearing_object}'"
        )
    return candidates[0], ()


def activate_prompt(
    prompt: str,
    parallelization_decision: str,
    *,
    action_category: str | None = None,
    weight_bearing_object: str | None = None,
    secondary_routes: list[str] | tuple[str, ...] | None = None,
    expected_prompt_sha256: str | None = None,
) -> ActivationResult:
    """Resolve structured activation input and verify prompt identity.

    The prompt hash prevents a case from silently changing its natural-language
    input while retaining the old expected activation.  Route selection itself
    is based only on canonical action/object fields; an absent or unknown field
    is a hard error instead of an escape-hatch fallback.
    """
    if not isinstance(prompt, str) or not prompt.strip():
        raise RouteActivationError("input.user_prompt must be a non-empty string")
    if parallelization_decision not in ALLOWED_PARALLELIZATION:
        raise RouteActivationError(
            "input.parallelization_decision must be one of "
            f"{sorted(ALLOWED_PARALLELIZATION)}"
        )
    if not isinstance(action_category, str) or action_category not in ACTION_CATEGORIES:
        raise RouteActivationError(f"unknown structured action_burden: {action_category!r}")
    if not isinstance(weight_bearing_object, str) or weight_bearing_object not in OBJECT_CATEGORIES:
        raise RouteActivationError(
            f"unknown structured weight_bearing_object: {weight_bearing_object!r}"
        )
    if not isinstance(expected_prompt_sha256, str) or not re.fullmatch(r"[0-9a-f]{64}", expected_prompt_sha256):
        raise RouteActivationError("input.prompt_sha256 must be a 64-character lowercase SHA-256")
    prompt_sha256 = hashlib.sha256(prompt.encode("utf-8")).hexdigest()
    if prompt_sha256 != expected_prompt_sha256:
        raise RouteActivationError(
            "input.user_prompt does not match input.prompt_sha256; refusing stale activation"
        )
    if not isinstance(secondary_routes, (list, tuple)) or not all(
        isinstance(route, str) and route.strip() for route in secondary_routes
    ):
        raise RouteActivationError("input.secondary_routes must be a string list")
    route_ids = load_route_registry().route_ids()
    secondary = tuple(sorted(set(secondary_routes)))
    unknown_secondary = set(secondary) - route_ids
    if unknown_secondary:
        raise RouteActivationError(
            f"input.secondary_routes contains unknown route(s): {sorted(unknown_secondary)}"
        )

    if action_category == "shared-workflow" or weight_bearing_object == "shared-workflow":
        if action_category != "shared-workflow" or weight_bearing_object != "shared-workflow":
            raise RouteActivationError(
                "shared-workflow activation requires both action_burden and "
                "weight_bearing_object to be shared-workflow"
            )
        primary = "shared-workflow"
        derived_secondary: tuple[str, ...] = ()
    else:
        primary, derived_secondary = _resolve_route(action_category, weight_bearing_object)
    if set(secondary) != set(derived_secondary) and derived_secondary:
        raise RouteActivationError(
            "structured secondary routes do not match the route decision-tree conflict pair: "
            f"expected {sorted(derived_secondary)}, got {sorted(secondary)}"
        )
    return ActivationResult(
        primary_route=primary,
        secondary_routes=secondary,
        action_category=action_category,
        weight_bearing_object=weight_bearing_object,
        parallelization_decision=parallelization_decision,
        prompt_sha256=prompt_sha256,
    )
