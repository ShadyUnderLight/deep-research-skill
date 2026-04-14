# Roadmap

This file tracks likely next improvements and helps keep repo evolution intentional.

## Current priorities

### P1
- Use `SYSTEM-MAP.md` to tighten family-level coverage and identify where a dedicated family map, route-supporting reference, checklist hardening, or delivery note is still missing.
- Add more evals for freshness, counter-evidence, and decision-quality regressions.
- Test the skill against more real fast-moving company/product cases.
- Tighten current-state verification if stale facts still leak into reports.
- Treat **listed-company stale-anchor selection** as a distinct failure family rather than only a generic freshness issue: test whether older-but-plausible annual / quarterly / market snapshots are still silently becoming the memo baseline, and decide whether this needs a dedicated meta-eval or failure-taxonomy entry.
- Add meta-evals and trigger-routing improvements for failure families identified in `references/failure-taxonomy.md`, especially rule activation, scope completeness, decision utility, and market-outlook routing.
- Decide whether to formalize eval subtypes (`case`, `rubric`, `distillation`, `meta-eval`) in naming or folder structure.
- Run at least 2-3 more real comparative-distillation cases and promote only the recurring candidate rules.
- Validate the new market-outlook routing against 2-3 more real cases before hardening further wording or adding more specialized sub-checklists.

### P2
- Expand finance/investment-specific guidance for valuation, consensus, and reporting-period handling.
- Add more examples of good and bad outputs.
- Improve task-type guidance for company, vendor-selection, technical-feasibility, and market-outlook research.
- Continue separating rendering-layer PDF fixes from research-discipline commits so layout failures can be traced independently.
- Validate whether recent CJK text-rhythm tweaks actually reduce the "broken export / OCR-like spacing" feel in Chinese-heavy PDFs before making larger visual changes.
- Add one more real-case pass on market-entry memo information design so recommendation, hard gates, shortlist, and phased-entry blocks become easier to scan in PDF output.

### P3
- Consider scripts for normalizing evidence and claim records only after the protocol is stable.
- Consider lightweight release/version process once iteration settles.

## Operating rules

When making a meaningful change:

1. Record the problem first in an issue or roadmap note.
2. Make a focused change, not a grab-bag edit.
3. Update `CHANGELOG.md` if behavior meaningfully changes.
4. Add or update an eval when fixing a real failure mode.
5. Push the change with a specific commit message.

## Good next eval targets

- stale product-line detection
- current pricing verification
- historical vs current vs forward-looking financial layering
- weak counter-evidence in company/vendor research
- output that summarizes well but does not help decision-making
