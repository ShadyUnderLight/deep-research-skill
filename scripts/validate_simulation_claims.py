#!/usr/bin/env python3
"""Detect simulation/model-output claims without status disclosure.

Scans report text for keywords indicating statistical tests, simulations,
or model outputs (p-values, Monte Carlo, Poisson, Elo, confidence intervals,
significance claims, random seeds) and warns when the text does not disclose
whether the claim is:
  - conceptual / planned (method suggestion only)
  - executed (actually run with reproducible artifacts)
  - illustrative (example data, not supporting conclusions)

This validator produces conditional warnings (exit code 2), not hard-fails,
because the distinction between "executed" and "conceptual" cannot be
determined with high confidence by regex alone. Human review at final-audit
time is expected.

Related:
  - `references/model-output-and-simulation-discipline.md`
  - `checklists/quantitative-role-audit.md`
  - `scripts/test_simulation_claims.py`
"""

from __future__ import annotations

import argparse
import re
import sys
from collections.abc import Iterable
from pathlib import Path
from typing import NamedTuple


# ── Keyword definitions ──────────────────────────────────────────────
# Each entry: (keyword_type, compiled_regex)
# keyword_type is used in warning output for categorization.

class KeywordRule(NamedTuple):
    type: str
    pattern: re.Pattern[str]


KEYWORD_RULES: list[KeywordRule] = [
    # p-value variants (fullwidth/halfwidth) — requires non-letter prefix
    # to avoid matching TCP<0.01, ASP<1000, HTTP<1.0 etc.
    KeywordRule("p_value", re.compile(r"(?<![a-zA-Z])p\s*[<＜≪]\s*0?\.?\d+", re.IGNORECASE)),
    KeywordRule("p_value", re.compile(r"\bp[\-\s]?value\b", re.IGNORECASE)),
    # confidence intervals
    KeywordRule("confidence_interval", re.compile(r"置信区间|confidence\s+interval", re.IGNORECASE)),
    KeywordRule("confidence_interval", re.compile(r"\d+\s*%\s*CI\b")),
    # simulation methods
    KeywordRule("simulation", re.compile(r"(?i)\bMonte\s+Carlo\b")),
    KeywordRule("simulation", re.compile(r"模拟\d*次|仿真\d*次|simulation", re.IGNORECASE)),
    # model names
    KeywordRule("model_name", re.compile(r"\b[Pp]oisson\b")),
    KeywordRule("model_name", re.compile(r"\b[Ee]lo\b")),
    # statistical tests
    KeywordRule("statistical_test", re.compile(r"回归.*显著|显著.*回归|统计.*显著|statistically\s+significant", re.IGNORECASE)),
    KeywordRule("statistical_test", re.compile(r"t[\-\s]?test|T[\-\s]?检验|\banova\b", re.IGNORECASE)),
    KeywordRule("statistical_test", re.compile(r"[Cc]hi[\-\s]?square|卡方", re.IGNORECASE)),
    # random seed
    KeywordRule("random_seed", re.compile(r"random[\s\-]?seed|随机种子", re.IGNORECASE)),
    # Chinese simulation claims (bare + compound)
    KeywordRule("simulation", re.compile(r"(?:通过|使用|采用|进行|经过|借助).{0,8}模拟")),
    KeywordRule("simulation", re.compile(r"模拟(?:显示|表明|结果|得出|发现|预测|输出|了)")),
    # Bare "模拟" in context suggesting methodological use
    KeywordRule("simulation", re.compile(r"[(（]\s*模拟\s*[)）]")),
    KeywordRule("simulation", re.compile(r"\b模拟\s*(?:分析|方法|实验|预测|验证|建模|模型|评估|推断|过程)")),
]


# ── Status disclosure markers ────────────────────────────────────────

CONCEPTUAL_PATTERNS: list[re.Pattern[str]] = [
    re.compile(p, re.IGNORECASE) for p in [
        r"概念(?:性)?框架",
        r"伪代码",
        r"pseudocode",
        r"计划(?:使用|执行|进行|采用)",
        r"可用该框架",
        r"建议(?:使用|采用|通过|后续)?.{0,12}(?:验证|检验)",
        r"可供.*(?:验证|检验|参考)",
        r"conceptual",
        r"planned",
        r"未(?:实际)?执行",
        r"future\s+validation",
        r"尚未(?:运行|执行|实现|进行)",
        # Narrower: only match "future/后续/将来" + closely-followed action words
        r"(?:后续|将来).{0,10}(?:验证|执行|进行|测试)",
        r"potential\s+(?:approach|method)",
        r"不作为.*(?:结论|实际|证据)",
        # Add: negative disclosure ("模型未运行", "未实际模拟")
        r"(?:本报告|当前).{0,20}(?:未|不)(?:实际)?(?:运行|执行|模拟|仿真)",
    ]
]

EXECUTED_PATTERNS: list[re.Pattern[str]] = [
    re.compile(p, re.IGNORECASE) for p in [
        # Broader: match 运行了/执行了/实现了 + model/simulation context
        r"(?:已|已经|实际|我们)\s*(?:执行|运行|实现|完成)了?\s*(?:该|了|过)?",
        r"executed",
        r"ran\s+\d+",
        r"reproduced",
        r"运行了?\s*\d*\s*次",
        r"模拟了?\s*\d*\s*次",
        r"执行了?\s*\d*\s*次",
        r"输出.*结果",
        r"得到.*分布",
        r"recorded\s+output",
        # Model explicitly documented as run
        r"(?:运行|执行|实现)了\s*(?:该|上述|前述|以下)?(?:模型|模拟|仿真|分析|回归)",
    ]
]

ILLUSTRATIVE_PATTERNS: list[re.Pattern[str]] = [
    re.compile(p, re.IGNORECASE) for p in [
        r"示例",
        r"说明性",
        r"仅作(?:参考|示例|说明)",
        r"illustrative",
        r"示例数据",
        r"示例表(?:格)?",
        r"example\s+(?:data|table)",
        r"不应视为",
        r"不代表",
        r"仅为说明",
        r"for\s+illustration\s+only",
    ]
]

# ── False-positive exemptions ──────────────────────────────────────
# Patterns that should suppress SPECIFIC keyword types.
# Keyed by keyword_type; only exempts matches of that type, not all keywords on the line.
FALSE_POSITIVE_EXEMPTIONS: dict[str, list[re.Pattern[str]]] = {
    "simulation": [
        # "simulation software/platform/tool" is a product category, not a method claim
        re.compile(r"simulation\s+(software|platform|tool|engine|environment|system)", re.IGNORECASE),
    ],
    "statistical_test": [
        # Institutional names containing "统计" but not making statistical claims
        re.compile(r"国家统计局|统计局|统计年鉴|统计公报|统计部门"),
    ],
}

SOURCE_REF_PATTERN = re.compile(r"\[S\d+\]")
BLOCKQUOTE_NOTE_PATTERN = re.compile(r"^\s*>\s*(注|note|说明|disclaimer)[：:]", re.IGNORECASE)


def _is_false_positive_for_type(line: str, keyword_type: str) -> bool:
    """Check if a keyword match of *keyword_type* is a known false positive.

    Returns True only for the specific keyword_type, not all keywords on the line.
    """
    patterns = FALSE_POSITIVE_EXEMPTIONS.get(keyword_type, [])
    for pattern in patterns:
        if pattern.search(line):
            return True
    return False


# ── Core logic ────────────────────────────────────────────────────────

class Claim(NamedTuple):
    """A detected simulation/model-output claim needing review."""
    line_no: int
    keyword_type: str
    keyword: str
    sentence: str
    status: str  # "unknown" | "conceptual" | "executed" | "illustrative"


def strip_fenced_code_blocks(text: str) -> tuple[str, set[int]]:
    """Remove fenced code blocks, returning cleaned text + set of excluded line numbers."""
    lines = text.splitlines()
    out: list[str] = []
    excluded: set[int] = set()
    in_fence = False
    fence_char = ""
    fence_len = 0

    for i, line in enumerate(lines):
        stripped = line.rstrip()
        if not in_fence:
            m = re.match(r"^[ ]{0,3}(`{3,}|~{3,})", stripped)
            if m:
                fence_char = m.group(1)[0]
                fence_len = len(m.group(1))
                in_fence = True
                excluded.add(i)  # 0-indexed
                out.append("")
                continue
            out.append(line)
        else:
            excluded.add(i)
            closing = re.compile(
                r"^[ ]{0,3}" + re.escape(fence_char) + "{" + str(fence_len) + r",}\s*$"
            )
            if closing.match(stripped):
                in_fence = False
            out.append("")

    return "\n".join(out), excluded


def find_context_window(
    lines: list[str],
    line_idx: int,
    window_size: int = 3,
) -> str:
    """Extract a context window of *window_size* lines around *line_idx*."""
    start = max(0, line_idx - window_size)
    end = min(len(lines), line_idx + window_size + 1)
    return " ".join(lines[start:end])


def classify_status(context: str) -> str:
    """Classify disclosure status from context text.

    Returns one of: 'conceptual', 'executed', 'illustrative', 'unknown'.
    """
    # Check in priority order: executed > illustrative > conceptual > unknown
    for pattern in EXECUTED_PATTERNS:
        if pattern.search(context):
            return "executed"
    for pattern in ILLUSTRATIVE_PATTERNS:
        if pattern.search(context):
            return "illustrative"
    for pattern in CONCEPTUAL_PATTERNS:
        if pattern.search(context):
            return "conceptual"
    return "unknown"


def scan_text(text: str) -> list[Claim]:
    """Scan text for simulation/statistical claims without status disclosure."""
    cleaned, excluded_lines = strip_fenced_code_blocks(text)
    lines = cleaned.splitlines()
    claims: list[Claim] = []

    # Track which sentences we've already claimed to avoid duplicates
    # Key: (line_idx, keyword_type) — same type on same line is one claim
    seen_claims: set[tuple[int, str]] = set()

    for line_idx, line in enumerate(lines):
        if line_idx in excluded_lines:
            continue
        if not line.strip():
            continue

        # Skip source reference lines and blockquote notes
        if SOURCE_REF_PATTERN.search(line) and not any(
            rule.pattern.search(line) for rule in KEYWORD_RULES
            if rule.type not in ("source_reference",)
        ):
            # Line has [Sxx] but no simulation keywords → skip
            pass

        for rule in KEYWORD_RULES:
            match = rule.pattern.search(line)
            if not match:
                continue

            keyword = match.group(0)
            context = find_context_window(lines, line_idx)

            # Skip known false positives (e.g., "simulation software" for simulation type,
            # "统计局" for statistical_test type) — only exempts the specific keyword type
            if _is_false_positive_for_type(line, rule.type):
                continue

            # Check if this line+type already has a claim (dedup: same type on same line)
            claim_key = (line_idx, rule.type)
            if claim_key in seen_claims:
                continue

            # Check source reference exemption: if all keyword matches are
            # inside [Sxx] references (i.e. removing [Sxx] makes the keyword
            # disappear), exempt the claim.
            if SOURCE_REF_PATTERN.search(context):
                cleaned_context = SOURCE_REF_PATTERN.sub("", context)
                if not rule.pattern.search(cleaned_context):
                    continue

            status = classify_status(context)
            seen_claims.add(claim_key)
            claims.append(Claim(
                line_no=line_idx + 1,  # 1-indexed for user display
                keyword_type=rule.type,
                keyword=keyword,
                sentence=line.strip()[:200],
                status=status,
            ))
            # NOTE: no `break` — multiple keywords on the same line
            # may each represent independent claims that need individual
            # status disclosure (e.g. "Monte Carlo + p<0.01" in one line).

    return claims


def _has_keyword_outside_ref(context: str, pattern: re.Pattern[str]) -> bool:
    """Check if keyword appears outside of [Sxx] references."""
    # Remove [Sxx] blocks and check if keyword still matches
    cleaned = SOURCE_REF_PATTERN.sub("", context)
    return bool(pattern.search(cleaned))


# ── CLI ────────────────────────────────────────────────────────────────

def format_warnings(claims: list[Claim], path: str) -> list[str]:
    """Format claims with unknown status as warnings."""
    warnings: list[str] = []
    for c in claims:
        if c.status == "unknown":
            warnings.append(
                f"{path}:{c.line_no}: [{c.keyword_type}] "
                f"'{c.keyword}' without status disclosure — "
                f"verify if conceptual, executed, or illustrative"
            )
    return warnings


def format_info(claims: list[Claim], path: str) -> list[str]:
    """Format claims with known status as info (no action needed)."""
    info: list[str] = []
    for c in claims:
        if c.status != "unknown":
            info.append(
                f"{path}:{c.line_no}: [{c.keyword_type}] "
                f"'{c.keyword}' → {c.status} (auto-classified)"
            )
    return info


def validate_file(path: Path) -> tuple[list[str], list[str]]:
    """Validate a single file. Returns (warnings, info)."""
    text = path.read_text(encoding="utf-8", errors="replace")
    claims = scan_text(text)
    return format_warnings(claims, str(path)), format_info(claims, str(path))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Lint simulation/model-output claims without status disclosure."
    )
    parser.add_argument(
        "paths", nargs="+", help="Markdown/text files to validate"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="Also print auto-classified claims (conceptual/executed/illustrative)"
    )
    args = parser.parse_args(argv)

    all_warnings: list[str] = []
    all_info: list[str] = []
    errors: list[str] = []

    for raw_path in args.paths:
        path = Path(raw_path)
        if not path.exists():
            errors.append(f"{path}: file not found")
            continue
        w, i = validate_file(path)
        all_warnings.extend(w)
        all_info.extend(i)

    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        return 1

    if all_warnings:
        print(f"Simulation claims without status disclosure ({len(all_warnings)}):")
        for w in all_warnings:
            print(f"- {w}")
        if args.verbose and all_info:
            print(f"\nAuto-classified claims ({len(all_info)}):")
            for info_line in all_info:
                print(f"  {info_line}")
        return 2

    if all_info:
        total = len(all_info)
        print(f"All {total} simulation/stat claims have status disclosure.")
        if args.verbose:
            for info_line in all_info:
                print(f"  {info_line}")
    else:
        print(f"No simulation/statistical claims detected in {len(args.paths)} file(s).")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
