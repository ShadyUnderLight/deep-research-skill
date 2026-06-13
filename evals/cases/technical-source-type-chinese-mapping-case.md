# Eval: Technical Source Type Chinese Mapping — Uncalibrated Free Text Case

## Goal

Test that the `validate_source_label_consistency.py` validator correctly:
1. Maps common Chinese technical source types (官方技术文档, 技术博客, 行业研究报告) to canonical types
2. Fails reports that use these types to support [确认事实] without caveats
3. Reports unknown/unmapped source types as warnings (non-strict) or errors (--strict)

This eval is based on the pattern established by `agentic-rag-technical-deep-dive-compounded-case.md`: a well-structured technical report that still fails delivery because source type discipline is systematically noncompliant.

## Prompt

Produce a structured technical deep-dive report comparing two machine learning frameworks.

The Source Register must use Chinese free-text source types such as:
- "官方技术文档" for official framework documentation
- "技术博客" for community or official blog posts
- "行业研究报告" for industry analyst reports
- "学术综述（arXiv）" for academic survey papers

The body must label claims based on these source types, using [确认事实] for directly supported claims and [推断] for interpreted or secondary claims.

## What this eval is testing

- Whether the Chinese→canonical type mapping correctly routes 官方技术文档 → PRIMARY_DEV (needs caveat)
- Whether 行业研究报告 → SECONDARY_ANALYST triggers [确认事实] detection
- Whether 学术综述（arXiv）→ SECONDARY_MEDIA triggers [确认事实] detection
- Whether 技术博客 → SECONDARY_MEDIA triggers [确认事实] detection
- Whether an unmapped Chinese type triggers a warning in non-strict mode and error in --strict mode
- Whether known canonical types (PRIMARY_FILING, SECONDARY_MEDIA) continue to work correctly

## Pass criteria

A passing validator invocation should:

1. **Default mode (--strict not set):**
   - Mapped Chinese types: correct type-based checks fire
   - Unmapped types: warning output to stderr, exit code 0

2. **Strict mode (--strict set):**
   - Mapped Chinese types: correct type-based checks fire
   - Unmapped types: error, exit code 2

3. **Specific checks:**
   - 官方技术文档 supporting [确认事实] without caveat → detected as PRIMARY_DEV without caveat
   - 行业研究报告 supporting [确认事实] → detected as SECONDARY_ANALYST with confirmed label
   - 学术综述（arXiv）支持 [确认事实] → detected as SECONDARY_MEDIA with confirmed label
   - An unmapped Chinese free-text type → warning in default mode, error in strict mode

## Failure signs

- Validator silently passes Chinese free-text source types without mapping them to canonical types
- Validator treats unmapped types as valid (no warning or error output)
- Chinese type mapping causes false positives on known clean patterns (e.g., PRIMARY_FILING with [确认事实])
- Validator behavior changes for canonical types that were working before

## Current rule verdict

- Source type Chinese mapping: mandatory (unknown types must not silently pass)
- Unknown type handling: warning (default), error (--strict)
- Vendor/secondary docs as [确认事实] without caveat: hard fail

## Related evals

- `evals/cases/agentic-rag-technical-deep-dive-compounded-case.md` — same compounded-fail pattern, different route

## Reviewer checklist

- Does Chinese type mapping handle parenthetical variants (学术综述（arXiv）)?
- Does unmapped type produce at least a warning in default mode?
- Does --strict mode correctly escalate warnings to errors?
- Are all existing canonical types still working unchanged?
- Does the mapping table in `references/source-traceability-and-claim-citation.md` match the implementation in `scripts/validate_source_label_consistency.py`?

## Suggested scoring

- **Pass**: Chinese types mapped correctly, unknown types warned in default and errored in strict, existing types unchanged
- **Conditional pass**: Chinese mapping works but unknown-type handling has edge cases (e.g., some unmapped types silently pass)
- **Fail**: Chinese types not mapped (validator silently passes), or unknown types produce no warning/error
