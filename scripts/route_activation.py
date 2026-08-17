#!/usr/bin/env python3
"""Deterministic offline adapter for the route-selection decision tree.

The production skill is still prose-driven, so this is deliberately a small
testable adapter rather than a claim that a keyword classifier replaces agent
reasoning.  It derives action examples and weight-bearing objects from the
canonical ``ROUTING-MATRIX.md`` decision tree, applies the documented conflict
pairs, and returns a structured activation snapshot for forward evals.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROUTING_MATRIX = ROOT / "ROUTING-MATRIX.md"
ALLOWED_PARALLELIZATION = {"single-track", "parallel", "not-needed"}


class RouteActivationError(ValueError):
    """Raised when an offline prompt cannot be classified safely."""


@dataclass(frozen=True)
class ActivationResult:
    primary_route: str
    secondary_routes: tuple[str, ...]
    action_category: str
    weight_bearing_object: str | None
    parallelization_decision: str
    mode: str = "offline-decision-tree"


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


def _decision_tree_section() -> str:
    try:
        content = ROUTING_MATRIX.read_text(encoding="utf-8")
    except OSError as exc:
        raise RouteActivationError(f"cannot read {ROUTING_MATRIX}: {exc}") from exc
    return _section_after_heading(content, "## Route selection decision tree")


def _step1_section() -> str:
    section = _decision_tree_section()
    start = section.find("### Step 1")
    if start == -1:
        raise RouteActivationError("ROUTING-MATRIX.md is missing Step 1")
    body = section[start:]
    next_h3 = re.search(r"\n### Step 2\b", body)
    if next_h3:
        body = body[:next_h3.start() + 1]
    return body


def _step2_section() -> str:
    section = _decision_tree_section()
    start = section.find("### Step 2")
    if start == -1:
        raise RouteActivationError("ROUTING-MATRIX.md is missing Step 2")
    body = section[start:]
    next_h3 = re.search(r"\n### Step 3\b", body)
    if next_h3:
        body = body[:next_h3.start() + 1]
    return body


def _parse_step1_phrasings() -> dict[str, list[str]]:
    mapping: dict[str, list[str]] = {}
    in_table = False
    for line in _step1_section().splitlines():
        stripped = line.strip()
        if "| Action category |" in stripped:
            in_table = True
            continue
        if not in_table:
            continue
        if stripped.startswith("|---"):
            continue
        if not stripped.startswith("|"):
            break
        columns = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(columns) < 3:
            continue
        action_match = re.search(r"\*\*(.+?)\*\*", columns[0])
        if not action_match:
            continue
        examples: list[str] = []
        for group in re.split(r"\s+/\s+", columns[2]):
            examples.extend(item.strip() for item in re.findall(r'"([^"]*)"', group) if item.strip())
        mapping[action_match.group(1).strip()] = examples
    return mapping


def _step2_object_routes() -> dict[str, list[str]]:
    mapping: dict[str, list[str]] = {}
    in_table = False
    for line in _step2_section().splitlines():
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


_STEP2_ZH_KEYWORDS: dict[str, str] = {
    "球队": "team", "夺冠": "team", "选哪个": "option", "哪一个": "option", "选项": "option", "定义好的": "option", "怎么选": "option", "比较": "option",
    "供应商": "provider", "API": "provider", "平台": "provider",
    "NAS": "device", "迷你主机": "device", "硬件": "device", "设备": "device",
    "产业链": "market", "市场": "market", "演化": "market", "趋势": "market", "行业": "market", "展望": "market",
    "法规": "regulation", "法案": "regulation", "政策": "regulation", "合规": "regulation",
    "股票": "listed", "估值": "listed", "特斯拉": "listed", "英伟达": "listed", "Nvidia": "listed",
    "创业": "private", "PMF": "private", "融资": "private",
    "架构": "architecture", "GPU": "architecture", "Kubernetes": "architecture", "Docker": "architecture", "技术原理": "architecture", "可行性": "architecture",
    "文献综述": "academic", "学术": "academic", "文献": "academic", "论文": "academic", "Transformer": "academic", "研究进展": "academic", "研究方向": "academic",
    "第一梯队": "positioning", "竞争格局": "positioning", "竞争壁垒": "positioning",
    "进入": "entry", "扩张": "entry", "市场进入": "entry",
}

_ACTION_ZH_MAP: dict[str, str] = {
    "架构": "technical", "技术": "technical", "原理": "technical", "对比": "technical", "比较": "technical", "可行性": "technical",
    "股票": "listed-company", "估值": "listed-company", "投资": "listed-company",
    "文献": "academic", "论文": "academic", "综述": "academic",
    "球队": "select", "夺冠": "select", "选": "select", "选择": "select", "哪一个": "select", "哪家": "select", "领先": "select", "排序": "select",
    "市场": "direction", "演化": "direction", "趋势": "direction",
    "法规": "regulation", "法案": "regulation",
    "创业": "private-company", "PMF": "private-company",
    "第一梯队": "positioning", "竞争": "positioning",
    "进入": "enter", "扩张": "enter", "供应商": "select", "平台": "select",
}

_CONFLICT_PAIRS: dict[tuple[str, str], tuple[str, tuple[str, ...]]] = {
    ("select/rank", "market"): ("constrained-choice", ()),
    ("enter/phase", "defined options"): ("market-entry", ()),
    ("listed-company", "architecture"): ("listed-company", ("technical-deep-dive",)),
    ("academic evidence", "architecture"): ("academic-review", ()),
    ("regulation", "market"): ("regulatory-analysis", ("market-outlook",)),
    ("technical", "listed"): ("technical-deep-dive", ()),
    ("technical", "academic"): ("technical-deep-dive", ()),
}


def _normalize_label(value: str) -> str:
    return re.sub(r"\s*/\s*", "/", value.lower())


def _classify_action(description: str) -> str | None:
    desc_lower = description.lower()
    best_match: str | None = None
    best_score = 0
    for action_name, examples in _parse_step1_phrasings().items():
        score = 0
        for example in examples:
            example_lower = example.lower()
            if example_lower in desc_lower:
                score += 10
            if re.search(r"[\u4e00-\u9fff]", example_lower):
                example_bigrams = {example_lower[i:i + 2] for i in range(len(example_lower) - 1)}
                desc_bigrams = {desc_lower[i:i + 2] for i in range(len(desc_lower) - 1)}
                score += len(example_bigrams & desc_bigrams) * 2
            else:
                score += len(set(example_lower.split()) & set(desc_lower.split()))
        for word in set(re.split(r"\s+/\s+", action_name.lower())):
            if len(word) >= 4 and word in desc_lower:
                score += 3
        for keyword, category in _ACTION_ZH_MAP.items():
            if keyword.lower() in desc_lower and category in action_name.lower():
                score += 5
        if score > best_score:
            best_score = score
            best_match = action_name
    return best_match


def _classify_object(description: str) -> str | None:
    desc_lower = description.lower()
    mapping = _step2_object_routes()
    matches: list[tuple[str, int]] = []
    for object_name in mapping:
        object_words = [
            word for word in re.split(r"\s*/\s*", object_name.lower())
            if len(word) >= 3 and word not in {"the", "or", "and"}
        ]
        score = sum(len(word) for word in object_words if word in desc_lower)
        for keyword, category in _STEP2_ZH_KEYWORDS.items():
            if keyword.lower() in desc_lower:
                score += sum(len(keyword) for word in object_words if category in word)
        if score > 0:
            matches.append((object_name, score))
    if not matches:
        return None
    matches.sort(key=lambda item: (-item[1], -len(item[0])))
    return matches[0][0]


def _resolve_route(action_name: str, object_name: str) -> tuple[str, tuple[str, ...]]:
    action_norm = _normalize_label(action_name)
    object_norm = _normalize_label(object_name)
    for (action_fragment, object_fragment), result in _CONFLICT_PAIRS.items():
        if action_fragment in action_norm and object_fragment in object_norm:
            return result
    candidates = _step2_object_routes().get(object_name, [])
    if not candidates:
        raise RouteActivationError(f"no route candidate for object '{object_name}'")
    return candidates[0], ()


def activate_prompt(prompt: str, parallelization_decision: str) -> ActivationResult:
    """Resolve one user prompt through the offline decision-tree adapter."""
    if not isinstance(prompt, str) or not prompt.strip():
        raise RouteActivationError("input.user_prompt must be a non-empty string")
    if parallelization_decision not in ALLOWED_PARALLELIZATION:
        raise RouteActivationError(
            "input.parallelization_decision must be one of "
            f"{sorted(ALLOWED_PARALLELIZATION)}"
        )

    action = _classify_action(prompt)
    object_name = _classify_object(prompt)
    if action is None or object_name is None:
        return ActivationResult(
            primary_route="shared-workflow",
            secondary_routes=(),
            action_category="shared-workflow",
            weight_bearing_object=object_name,
            parallelization_decision=parallelization_decision,
        )
    primary, secondary = _resolve_route(action, object_name)
    prompt_lower = prompt.lower()
    if (
        "次级" in prompt_lower
        and "市场" in prompt_lower
        and any(keyword in prompt_lower for keyword in ("选项", "选择", "比较"))
    ):
        primary, secondary = "market-outlook", ("constrained-choice",)
    elif (
        primary == "technical-deep-dive"
        and any(keyword in prompt_lower for keyword in ("上市公司", "股票", "估值", "公司"))
        and any(keyword in prompt_lower for keyword in ("架构", "技术", "可行性", "机制"))
    ):
        secondary = ("listed-company",)
    return ActivationResult(
        primary_route=primary,
        secondary_routes=secondary,
        action_category=action,
        weight_bearing_object=object_name,
        parallelization_decision=parallelization_decision,
    )
