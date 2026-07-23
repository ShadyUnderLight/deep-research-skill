#!/usr/bin/env python3
"""Validate that ROUTING-MATRIX.md contains the route selection decision tree,
and the old fixed-priority-only section has been replaced.

Property-based structural test suite.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def read_file(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _section_after_heading(content: str, heading: str) -> str:
    """Extract the section body following a ## heading, up to the next ## heading."""
    start = content.find(heading)
    if start == -1:
        return ""
    section = content[start:]
    # Skip the heading line itself
    rest = section[section.index("\n") + 1:]
    next_heading = re.search(r"\n## ", rest)
    if next_heading:
        rest = rest[:next_heading.start() + 1]
    return rest


def test_decision_tree_section_exists():
    """ROUTING-MATRIX.md MUST contain '## Route selection decision tree' section."""
    content = read_file(REPO_ROOT / "ROUTING-MATRIX.md")
    assert "## Route selection decision tree" in content, (
        "Missing '## Route selection decision tree' section in ROUTING-MATRIX.md"
    )
    _ = _section_after_heading(content, "## Route selection decision tree")


def test_old_routing_priority_replaced_or_demoted():
    """The old '## Routing priority' standalone section MUST be gone.

    It may only appear as a subsection heading (### Routing tie-breaker) or not at all."""
    content = read_file(REPO_ROOT / "ROUTING-MATRIX.md")
    # Count occurrences of '## Routing priority' as a standalone H2 heading
    # This matches only the old-style section header, not '### Routing ...' subsections
    count = len(re.findall(r"^## Routing priority$", content, re.MULTILINE))
    assert count == 0, (
        f"'## Routing priority' H2 section found {count} time(s) in ROUTING-MATRIX.md. "
        "It must be replaced with '## Route selection decision tree'."
    )


def test_decision_tree_has_four_steps():
    """The decision tree section MUST contain Step 1-4 markers."""
    content = read_file(REPO_ROOT / "ROUTING-MATRIX.md")
    section = _section_after_heading(content, "## Route selection decision tree")
    assert section, "Decision tree section not found (empty section body)"

    for step_num in range(1, 5):
        # Match patterns: "### Step 1", "**Step 1**", "Step 1 —", "Step 1:"
        pattern = rf"(?:###\s+|\\*\\*)?Step {step_num}\b"
        assert re.search(pattern, section), (
            f"Step {step_num} not found in decision tree section"
        )


def test_tie_breaker_retains_all_routes():
    """The tie-breaker table (step 4) MUST list all 11 specialized routes
    in the original priority order, within the Step 4 subsection only."""
    content = read_file(REPO_ROOT / "ROUTING-MATRIX.md")
    section = _section_after_heading(content, "## Route selection decision tree")
    assert section, "Decision tree section not found"

    # Narrow to the Step 4 subsection only
    step4_start = section.find("### Step 4")
    assert step4_start != -1, "Step 4 subsection not found in decision tree"
    step4_section = section[step4_start:]
    # Cut at next ### heading if any
    next_h3 = re.search(r"\n### ", step4_section[1:])
    if next_h3:
        step4_section = step4_section[:next_h3.start() + 1]

    expected_routes = [
        "listed-company",
        "startup-evaluation",
        "market-entry",
        "regulatory-analysis",
        "provider-selection",
        "competitive-positioning",
        "technical-deep-dive",
        "equipment-selection",
        "market-outlook",
        "constrained-choice",
        "academic-review",
    ]

    positions = {}
    for route_id in expected_routes:
        pos = step4_section.find(route_id)
        if pos != -1:
            positions[route_id] = pos

    sorted_by_pos = sorted(positions.items(), key=lambda x: x[1])
    found_ordered = [rid for rid, _ in sorted_by_pos]

    missing = set(expected_routes) - set(found_ordered)
    assert not missing, (
        f"Tie-breaker table missing routes: {missing}"
    )
    assert found_ordered == expected_routes, (
        f"Tie-breaker routes not in correct order.\n"
        f"Expected: {expected_routes}\n"
        f"Found:    {found_ordered}"
    )


def test_route_index_tie_breaker_annotation():
    """references/route-index.md MUST annotate priority as tie-breaker only."""
    content = read_file(REPO_ROOT / "references/route-index.md")

    has_tie_breaker = (
        "tie-break" in content.lower()
        or "tie break" in content.lower()
        or "decision tree" in content.lower()
    )
    assert has_tie_breaker, (
        "references/route-index.md must annotate the priority list as tie-breaker only "
        "or reference the decision tree"
    )

    # Must still contain the full priority line (as the tie-breaker list)
    assert "listed-company" in content, "listed-company missing from route-index.md"
    assert "academic-review" in content, "academic-review missing from route-index.md"


def test_route_activation_references_decision_tree():
    """references/route-activation-and-preflight.md MUST reference
    the decision tree (in any section — Preflight Step 1 is the expected location)."""
    content = read_file(REPO_ROOT / "references/route-activation-and-preflight.md")

    # Decision tree reference may be in Preflight Step 1 (after the "Do not use"
    # clause check), not necessarily in "How to choose the primary route" section.
    # Search the entire file.
    has_reference = (
        "decision tree" in content.lower()
        or "route selection decision tree" in content.lower()
    )
    assert has_reference, (
        "route-activation-and-preflight.md must reference the decision tree"
    )

    # Also verify ROUTING-MATRIX.md is mentioned (the decision tree lives there)
    assert "ROUTING-MATRIX.md" in content, (
        "route-activation-and-preflight.md must reference ROUTING-MATRIX.md"
    )


# ── Behavioral route fixtures ──────────────────────────────────────────────

def _decision_tree_section() -> str:
    """Return the full decision tree section from ROUTING-MATRIX.md."""
    content = read_file(REPO_ROOT / "ROUTING-MATRIX.md")
    return _section_after_heading(content, "## Route selection decision tree")


def _step1_section() -> str:
    """Return the Step 1 subsection."""
    section = _decision_tree_section()
    start = section.find("### Step 1")
    assert start != -1, "Step 1 not found"
    body = section[start:]
    next_h3 = re.search(r"\n### Step 2\b", body)
    if next_h3:
        body = body[:next_h3.start() + 1]
    return body


def _step2_section() -> str:
    """Return the Step 2 subsection."""
    section = _decision_tree_section()
    start = section.find("### Step 2")
    assert start != -1, "Step 2 not found"
    body = section[start:]
    next_h3 = re.search(r"\n### Step 3\b", body)
    if next_h3:
        body = body[:next_h3.start() + 1]
    return body


def _step2_object_routes() -> dict[str, list[str]]:
    """Parse Step 2 table: weight-bearing object → list of route candidate(s)."""
    section = _step2_section()
    mapping: dict[str, list[str]] = {}
    in_table = False
    for line in section.split("\n"):
        stripped = line.strip()
        if stripped.startswith("| Weight-bearing object"):
            in_table = True
            continue
        if not in_table:
            continue
        if stripped.startswith("|---"):
            continue
        if stripped.startswith("|") and "`" in stripped:
            cols = [c.strip() for c in stripped.strip("|").split("|")]
            if len(cols) >= 2:
                object_name = cols[0].strip()
                route_cell = cols[1].strip()
                # Extract all backtick-quoted route IDs
                route_ids = re.findall(r"`([a-z]+(?:-[a-z]+)*)`", route_cell)
                if route_ids and object_name:
                    mapping[object_name] = route_ids
        elif stripped.startswith("|") and not in_table:
            continue
        elif stripped.startswith("When an object matches"):
            break  # end of table
    return mapping


def test_step1_covers_all_action_categories():
    """Step 1 must define exactly the action categories that map to routes."""
    section = _step1_section()
    # Must list all 9 major action categories
    required = [
        "Select",
        "Enter",
        "Judge direction",
        "Judge regulation",
        "Judge listed-company",
        "Judge private-company",
        "Judge technical",
        "Judge academic",
        "Judge positioning",
    ]
    for keyword in required:
        assert keyword in section, f"Step 1 missing action category: {keyword}"


def test_step2_maps_to_known_route_ids():
    """Every route ID in Step 2 must exist in route-manifest.json."""
    import json
    manifest_path = REPO_ROOT / "schemas" / "route-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    valid_ids = {r["id"] for r in manifest["routes"]}

    mapping = _step2_object_routes()
    for obj_name, route_ids in mapping.items():
        for rid in route_ids:
            assert rid in valid_ids, (
                f"Step 2 object '{obj_name}' maps to unknown route '{rid}'"
            )


def test_step2_each_object_has_unique_candidate():
    """Each weight-bearing object row must map to 1-3 unique candidate routes."""
    mapping = _step2_object_routes()
    for obj_name, route_ids in mapping.items():
        assert 1 <= len(route_ids) <= 3, (
            f"Step 2 object '{obj_name}' has {len(route_ids)} candidates, "
            f"expected 1-3"
        )


def test_step2_disambiguation_rule_exists():
    """Step 2 must include a disambiguation rule for multi-match objects."""
    section = _step2_section()
    has_rule = (
        "most specific" in section.lower()
        or "more specific" in section.lower()
    )
    assert has_rule, (
        "Step 2 must include a 'most specific row wins' disambiguation rule "
        "for objects matching multiple rows"
    )


def test_step3_references_boundary_clauses():
    """Step 3 must reference per-route 'Do not use' and boundary resolution."""
    section = _decision_tree_section()
    step3_start = section.find("### Step 3")
    assert step3_start != -1
    step3 = section[step3_start:]
    next_h3 = re.search(r"\n### Step 4\b", step3)
    if next_h3:
        step3 = step3[:next_h3.start() + 1]

    assert "Do not use" in step3, "Step 3 must reference 'Do not use' clauses"
    assert "boundary" in step3.lower(), (
        "Step 3 must reference boundary resolution"
    )


def test_step4_is_explicitly_last_resort():
    """Step 4 tie-breaker must be labeled as last-resort, not default."""
    section = _decision_tree_section()
    step4_start = section.find("### Step 4")
    assert step4_start != -1
    step4 = section[step4_start:]
    next_h3 = re.search(r"\n### ", step4[1:])
    if next_h3:
        step4 = step4[:next_h3.start() + 1]

    # Must emphasize that Step 4 is only for unresolved cases
    keywords = ["only", "don't resolve", "did not produce", "exhausted"]
    found = any(kw in step4.lower() for kw in keywords)
    assert found, (
        "Step 4 must explicitly state it's only for cases Steps 1-3 don't resolve"
    )


def test_sports_prediction_routes_to_constrained_choice():
    """Sports prediction keywords in Step 1 must map to constrained-choice,
    not market-outlook or provider-selection. Regression test for the
    Blocker found in Round 1 cross-review."""
    step1 = _step1_section()
    mapping = _step2_object_routes()

    # Step 1 must have sports-related Chinese example
    assert "哪支球队" in step1 or "predict" in step1.lower(), (
        "Step 1 must include sports prediction example"
    )

    # "Defined options / teams" must map to constrained-choice (single candidate)
    teams_obj = None
    for obj_name in mapping:
        if "team" in obj_name.lower() or "defined options" in obj_name.lower():
            teams_obj = obj_name
            break
    assert teams_obj is not None, (
        "Step 2 must have a 'Defined options / teams' row"
    )
    candidates = mapping[teams_obj]
    assert "constrained-choice" in candidates, (
        f"'Defined options / teams' must map to constrained-choice, got {candidates}"
    )
    # constrained-choice must be the only or highest-specificity candidate for teams
    # (after the Blocker fix, it should be a single candidate row)
    assert len(candidates) == 1, (
        f"'Defined options / teams' should have 1 candidate after Blocker fix, "
        f"got {len(candidates)}: {candidates}"
    )


def test_market_outlook_guards_against_ranking_misuse_in_step1():
    """Step 1 must distinguish 'judge direction' from 'select/rank'.
    Step 2 must not map 'market trajectory' to constrained-choice."""
    step1 = _step1_section()
    mapping = _step2_object_routes()

    # Verify the action categories are distinct
    assert "Select / rank" in step1, "Step 1 must have Select/rank category"
    assert "Judge direction" in step1, "Step 1 must have Judge direction category"

    # Market trajectory must map to market-outlook only
    market_obj = None
    for obj_name in mapping:
        if "market" in obj_name.lower() and "trajectory" in obj_name.lower():
            market_obj = obj_name
            break
    assert market_obj is not None, "Step 2 must have a market trajectory row"
    candidates = mapping[market_obj]
    assert candidates == ["market-outlook"], (
        f"Market trajectory must map only to market-outlook, got {candidates}"
    )


def test_conflict_pairs_exist():
    """At least 5 action-object conflict pairs must be documented in Step 2."""
    section = _step2_section()
    # Count "→" arrows in the conflict examples section
    conflict_start = section.find("Conflict examples")
    assert conflict_start != -1, "Conflict examples section not found"
    conflict_section = section[conflict_start:]
    arrow_count = conflict_section.count("→")
    assert arrow_count >= 6, (
        f"Expected ≥6 conflict pairs, found {arrow_count} '→' arrows"
    )


def test_shared_workflow_not_misused():
    """The decision tree must not recommend shared-workflow as an escape hatch
    for tasks that have a clear action burden and weight-bearing object."""
    section = _decision_tree_section()
    mapping = _step2_object_routes()

    # Every weight-bearing object must map to at least one specialized route
    for obj_name, route_ids in mapping.items():
        for rid in route_ids:
            assert rid != "shared-workflow", (
                f"Step 2 object '{obj_name}' maps to shared-workflow — "
                f"specialized routes must be preferred"
            )


# ── Real action/object → route fixtures ──────────────────────────────────

def _parse_step1_phrasings() -> dict[str, list[str]]:
    """Parse Step 1 table: action category → example phrasings (EN + ZH).
    Returns mapping from action category bold text to list of example strings."""
    section = _step1_section()
    mapping: dict[str, list[str]] = {}
    in_table = False
    for line in section.split("\n"):
        stripped = line.strip()
        if not stripped:
            continue
        if "| Action category |" in stripped:
            in_table = True
            continue
        if not in_table:
            continue
        if stripped.startswith("|---"):
            continue
        if not stripped.startswith("|"):
            break
        cols = [c.strip() for c in stripped.strip("|").split("|")]
        if len(cols) < 3:
            continue
        action_match = re.search(r"\*\*(.+?)\*\*", cols[0])
        if not action_match:
            continue
        action_name = action_match.group(1).strip()
        # Example phrasings column: `"en1", "en2" / "zh1", "zh2"`
        examples_col = cols[2] if len(cols) > 2 else ""
        examples: list[str] = []
        # Split EN and ZH groups by " / " between the groups
        groups = re.split(r'\s+/\s+', examples_col)
        for group in groups:
            # Extract quoted strings within each group
            quoted = re.findall(r'"([^"]*)"', group)
            for q in quoted:
                q = q.strip()
                if q and len(q) >= 2:
                    examples.append(q)
        mapping[action_name] = examples
    return mapping


# Chinese → English keyword mapping for Step 2 object classification
_STEP2_ZH_KEYWORDS: dict[str, str] = {
    # Defined options / teams / ranking
    "球队": "team",
    "夺冠": "team",
    "选哪个": "option",
    "怎么选": "option",
    "比较": "option",
    # Providers / vendors / APIs / models
    "供应商": "provider",
    "API": "provider",
    "平台": "provider",
    # Devices / hardware / build
    "NAS": "device",
    "迷你主机": "device",
    "硬件": "device",
    "设备": "device",
    # Market / category trajectory
    "产业链": "market",
    "市场": "market",
    "演化": "market",
    "趋势": "market",
    "行业": "market",
    "展望": "market",
    # Regulation / rules / policy
    "法规": "regulation",
    "法案": "regulation",
    "政策": "regulation",
    "合规": "regulation",
    # Listed / public company
    "股票": "listed",
    "估值": "listed",
    "特斯拉": "listed",
    "英伟达": "listed",
    "Nvidia": "listed",
    # Private / startup company
    "创业": "private",
    "PMF": "private",
    "融资": "private",
    # Architecture / mechanism / patent
    "架构": "architecture",
    "GPU": "architecture",
    "Kubernetes": "architecture",
    "Docker": "architecture",
    "技术原理": "architecture",
    "可行性": "architecture",
    # Academic literature / research evidence
    "文献综述": "academic",
    "论文": "academic",
    "Transformer": "academic",
    "研究进展": "academic",
    # Positioning / tier label
    "第一梯队": "positioning",
    "竞争格局": "positioning",
    "竞争壁垒": "positioning",
    # Entry decision / sequencing / gates
    "进入": "entry",
    "扩张": "entry",
    "市场进入": "entry",
}


def _parse_step2_keywords() -> dict[str, str]:
    """Parse Step 2 table: weight-bearing object → route candidate(s).
    Returns mapping from object name to comma-separated route candidates."""
    mapping = _step2_object_routes()
    result: dict[str, str] = {}
    for obj_name, route_ids in mapping.items():
        result[obj_name] = route_ids[0] if len(route_ids) == 1 else ",".join(route_ids)
    return result


def _classify_action(description: str, phrasings: dict[str, list[str]]) -> str | None:
    """Classify a task description against Step 1 action categories.
    Returns the best-matching action category name, or None."""
    desc_lower = description.lower()

    # CJK action keyword mapping for fallback matching
    _action_zh_map: dict[str, str] = {
        "架构": "technical", "技术": "technical", "原理": "technical",
        "对比": "technical", "比较": "technical", "可行性": "technical",
        "股票": "listed-company", "估值": "listed-company", "投资": "listed-company",
        "文献": "academic", "论文": "academic", "综述": "academic",
        "球队": "select", "夺冠": "select", "选": "select",
        "市场": "direction", "演化": "direction", "趋势": "direction",
        "法规": "regulation", "法案": "regulation",
        "创业": "private-company", "PMF": "private-company",
        "第一梯队": "positioning", "竞争": "positioning",
        "进入": "enter", "扩张": "enter",
        "供应商": "select", "平台": "select",
    }

    best_match: str | None = None
    best_score = 0
    for action_name, examples in phrasings.items():
        score = 0
        for ex in examples:
            ex_lower = ex.lower()
            if ex_lower in desc_lower:
                score += 10
            # For CJK text (no spaces), use character n-gram overlap
            if re.search(r'[\u4e00-\u9fff]', ex_lower):
                ex_chars = list(ex_lower)
                desc_chars = list(desc_lower)
                ex_bigrams = set("".join(ex_chars[i:i+2]) for i in range(len(ex_chars)-1))
                desc_bigrams = set("".join(desc_chars[i:i+2]) for i in range(len(desc_chars)-1))
                score += len(ex_bigrams & desc_bigrams) * 2
            else:
                # For spaced text, use word overlap
                ex_words = set(ex_lower.split())
                desc_words = set(desc_lower.split())
                overlap = ex_words & desc_words
                score += len(overlap)
        # Fallback: match action name keywords against description
        action_words = set(re.split(r'\s+/\s+', action_name.lower()))
        for w in action_words:
            if len(w) >= 4 and w in desc_lower:
                score += 3
        # Fallback: CJK keyword → action category mapping
        for zh_kw, en_cat in _action_zh_map.items():
            if zh_kw.lower() in desc_lower:
                if en_cat in action_name.lower():
                    score += 5
        if score > best_score:
            best_score = score
            best_match = action_name
    return best_match


def _classify_object(description: str, mapping: dict[str, str]) -> str | None:
    """Classify a task description against Step 2 weight-bearing objects.
    Uses Chinese keyword mapping and English object name matching.
    Returns the best-matching object name, applying the 'most specific' rule."""
    desc_lower = description.lower()
    matches: list[tuple[str, int]] = []

    for obj_name in mapping:
        # Extract significant words from object name (≥3 chars, skip stop words)
        obj_words = [
            w for w in re.split(r"\s*/\s*", obj_name.lower())
            if len(w) >= 3 and w not in {"the", "or", "and"}
        ]
        score = 0
        for w in obj_words:
            if w in desc_lower:
                score += len(w)

        # Also check Chinese keyword mappings
        for zh_word, en_category in _STEP2_ZH_KEYWORDS.items():
            if zh_word.lower() in desc_lower:
                # Map Chinese keyword to the target object via English category
                for en_word in obj_words:
                    if en_category in en_word:
                        score += len(zh_word)

        if score > 0:
            matches.append((obj_name, score))

    if not matches:
        return None
    matches.sort(key=lambda x: (-x[1], -len(x[0])))
    return matches[0][0]


# ── Action+object → route conflict resolver ─────────────────────────────

# Conflict pairs extracted from Step 2 conflict examples:
# (action_name_substring, object_name_substring) → (primary_route, [secondary_routes])
# Substrings are slash-normalized (spaces around / removed) to match classifier output.
_CONFLICT_PAIRS: dict[tuple[str, str], tuple[str, list[str]]] = {
    ("select/rank", "market"): ("constrained-choice", []),
    ("enter/phase", "defined options"): ("market-entry", []),
    ("listed-company", "architecture"): ("listed-company", ["technical-deep-dive"]),
    ("academic evidence", "architecture"): ("academic-review", []),
    ("regulation", "market"): ("regulatory-analysis", ["market-outlook"]),
    # Reverse: action=technical + object=listed → technical primary
    ("technical", "listed"): ("technical-deep-dive", []),
    # Reverse: action=technical + object=academic → technical primary
    ("technical", "academic"): ("technical-deep-dive", []),
}


def _normalize_label(s: str) -> str:
    """Collapse spaces around slashes: 'Select / rank / predict' → 'select/rank/predict'."""
    return re.sub(r"\s*/\s*", "/", s.lower())


def _resolve_route(action_name: str, object_name: str) -> tuple[str, list[str]]:
    """Resolve primary route and secondary routes from action + object,
    applying conflict pair overrides when Step 1 action and Step 2 object
    point to different routes."""
    action_norm = _normalize_label(action_name)
    object_norm = _normalize_label(object_name)

    # Check if a conflict pair overrides the Step 2 mapping
    for (act_sub, obj_sub), (primary, secondary) in _CONFLICT_PAIRS.items():
        if act_sub in action_norm and obj_sub in object_norm:
            return (primary, secondary)

    # No conflict — use Step 2 object mapping directly
    step2 = _parse_step2_keywords()
    candidates_str = step2.get(object_name, "")
    candidates = candidates_str.split(",") if "," in candidates_str else [candidates_str]
    primary = candidates[0] if candidates else ""
    return (primary, [])


# Each fixture: (task_description, expected_action_name_substring,
#                 expected_primary_route, expected_secondary_routes)
ROUTE_FIXTURES = [
    # ── Positive cases ─────────────────────────────────────────────────
    (
        "哪支球队最可能夺冠",
        "Select",
        "constrained-choice",
        [],
    ),
    (
        "应该选哪个 AI 模型供应商",
        "Select",
        "provider-selection",
        [],
    ),
    (
        "NAS vs 迷你主机怎么选，预算 3000",
        "Select",
        "equipment-selection",
        [],
    ),
    (
        "人形机器人产业链未来 12 个月如何演化",
        "Judge direction",
        "market-outlook",
        [],
    ),
    (
        "特斯拉股票现在估值合理吗",
        "listed-company",
        "listed-company",
        [],
    ),
    (
        "分析 Nvidia GPU 架构及其对竞争壁垒的影响",
        "technical",
        "technical-deep-dive",
        [],
    ),
    (
        "英伟达股票估值分析——GPU 架构的竞争优势",
        "listed-company",
        "listed-company",
        [],
    ),
    (
        "Transformer 相关论文的文献综述",
        "academic",
        "academic-review",
        [],
    ),
    (
        "Transformer 注意力机制的技术原理——基于论文分析",
        "technical",
        "technical-deep-dive",
        [],
    ),
    (
        "Kubernetes 和 Docker Swarm 的架构对比",
        "technical",
        "technical-deep-dive",
        [],
    ),
    (
        "某创业公司的 PMF 分析",
        "private-company",
        "startup-evaluation",
        [],
    ),
    (
        "某公司是不是第一梯队",
        "positioning",
        "competitive-positioning",
        [],
    ),
    # ── Mixed cases — primary + secondary ──────────────────────────────
    (
        "欧盟 AI 法案对欧洲 AI 市场的影响（法规视角）",
        "regulation",
        "regulatory-analysis",
        [],
    ),
    (
        "是否应该进入中国市场，考虑数据本地化法规",
        "Enter",
        "market-entry",
        [],
    ),
    # ── Shared-workflow guard — must route to specialized ─────────────
    (
        "比较三个视频会议平台的功能和价格",
        "Select",
        "provider-selection",
        [],
    ),
    # ── Non-empty secondary fixtures — conflict pair secondary verification ──
    (
        "英伟达GPU架构对其估值的影响——投资视角分析架构优势",
        "listed-company",
        "listed-company",
        ["technical-deep-dive"],
    ),
    (
        "分析欧盟数据保护法规对美国科技市场的影响",
        "regulation",
        "regulatory-analysis",
        ["market-outlook"],
    ),
    # ── Conflict pair regression: select+market → constrained-choice ──
    (
        "predict which market will be more profitable",
        "Select",
        "constrained-choice",
        [],
    ),
]


def test_route_fixtures_classify_and_verify():
    """For each fixture: (a) classify task_description, (b) verify action
    classification matches expected, (c) resolve route via action+object
    with conflict pairs, (d) verify primary and secondary routes match."""
    phrasings = _parse_step1_phrasings()
    step2_keywords = _parse_step2_keywords()
    import json
    manifest_path = REPO_ROOT / "schemas" / "route-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    valid_ids = {r["id"] for r in manifest["routes"]}

    for desc, exp_action_sub, exp_route, exp_secondary in ROUTE_FIXTURES:
        # (a) Classify action
        action = _classify_action(desc, phrasings)
        assert action is not None, (
            f"Fixture '{desc}': could not classify action"
        )
        # (b) Verify action matches expected
        assert exp_action_sub.lower() in action.lower(), (
            f"Fixture '{desc}': action='{action}', expected contains '{exp_action_sub}'"
        )

        # (c) Classify object, then resolve route via conflict pairs
        obj_name = _classify_object(desc, step2_keywords)
        assert obj_name is not None, (
            f"Fixture '{desc}': could not classify object"
        )
        resolved_primary, resolved_secondary = _resolve_route(action, obj_name)

        # (d) Verify primary route
        assert resolved_primary == exp_route, (
            f"Fixture '{desc}': action='{action}', object='{obj_name}' "
            f"→ resolved primary='{resolved_primary}', expected='{exp_route}'"
        )

        # (e) Verify secondary routes (exact match — both directions)
        resolved_set = set(resolved_secondary)
        expected_set = set(exp_secondary)
        missing = expected_set - resolved_set
        extra = resolved_set - expected_set
        assert not missing, (
            f"Fixture '{desc}': missing secondary {missing}, "
            f"expected {exp_secondary}, got {resolved_secondary}"
        )
        assert not extra, (
            f"Fixture '{desc}': unexpected secondary {extra}, "
            f"expected {exp_secondary}, got {resolved_secondary}"
        )


def test_no_select_rank_fixture_routes_market_outlook():
    """Select/rank task descriptions must not resolve to market-outlook."""
    phrasings = _parse_step1_phrasings()
    step2_keywords = _parse_step2_keywords()

    for desc, exp_action_sub, _, _ in ROUTE_FIXTURES:
        if "select" not in exp_action_sub.lower():
            continue
        action = _classify_action(desc, phrasings)
        if action is None:
            continue
        obj_name = _classify_object(desc, step2_keywords)
        if obj_name is None:
            continue
        resolved_primary, _ = _resolve_route(action, obj_name)
        assert "market-outlook" != resolved_primary, (
            f"Fixture '{desc}': Select/rank, object='{obj_name}' "
            f"→ resolved '{resolved_primary}' (should not be market-outlook)"
        )


def test_market_outlook_fixtures_single_candidate():
    """Tasks classified as market outlook must resolve to market-outlook only."""
    phrasings = _parse_step1_phrasings()
    step2_keywords = _parse_step2_keywords()

    for desc, _, exp_route, _ in ROUTE_FIXTURES:
        if exp_route != "market-outlook":
            continue
        obj_name = _classify_object(desc, step2_keywords)
        assert obj_name is not None, f"Fixture '{desc}': could not classify object"
        resolved_primary, resolved_secondary = _resolve_route("Judge direction", obj_name)
        assert resolved_primary == "market-outlook", (
            f"Fixture '{desc}': expected market-outlook, got '{resolved_primary}'"
        )
        assert resolved_secondary == [], (
            f"Fixture '{desc}': market-outlook should have no secondary, got {resolved_secondary}"
        )


if __name__ == "__main__":
    failures: list[str] = []
    tests = [
        # Structural tests
        ("decision_tree_section_exists", test_decision_tree_section_exists),
        ("old_routing_priority_replaced", test_old_routing_priority_replaced_or_demoted),
        ("decision_tree_has_four_steps", test_decision_tree_has_four_steps),
        ("tie_breaker_retains_all_routes", test_tie_breaker_retains_all_routes),
        ("route_index_tie_breaker_annotation", test_route_index_tie_breaker_annotation),
        ("route_activation_references_decision_tree", test_route_activation_references_decision_tree),
        # Behavioral tests — action/object coverage
        ("step1_covers_all_action_categories", test_step1_covers_all_action_categories),
        ("step2_maps_to_known_route_ids", test_step2_maps_to_known_route_ids),
        ("step2_each_object_has_unique_candidate", test_step2_each_object_has_unique_candidate),
        ("step2_disambiguation_rule_exists", test_step2_disambiguation_rule_exists),
        # Behavioral tests — boundary/guard checks
        ("step3_references_boundary_clauses", test_step3_references_boundary_clauses),
        ("step4_is_explicitly_last_resort", test_step4_is_explicitly_last_resort),
        # Behavioral tests — routing correctness (positive)
        ("sports_prediction_routes_to_constrained_choice", test_sports_prediction_routes_to_constrained_choice),
        ("market_outlook_guards_against_ranking_misuse", test_market_outlook_guards_against_ranking_misuse_in_step1),
        ("conflict_pairs_exist", test_conflict_pairs_exist),
        # Behavioral tests — negative/misuse guard
        ("shared_workflow_not_misused", test_shared_workflow_not_misused),
        # Behavioral tests — action/object → route fixtures
        ("route_fixtures_classify_and_verify", test_route_fixtures_classify_and_verify),
        ("no_select_rank_fixture_routes_market_outlook", test_no_select_rank_fixture_routes_market_outlook),
        ("market_outlook_fixtures_single_candidate", test_market_outlook_fixtures_single_candidate),
    ]

    for name, fn in tests:
        try:
            fn()
            print(f"  PASS  {name}")
        except AssertionError as e:
            print(f"  FAIL  {name}: {e}")
            failures.append(name)

    if failures:
        print(f"\n{failures} test(s) failed")
        sys.exit(1)
    else:
        print("\nAll tests passed.")
        sys.exit(0)
