# Roadmap

This file tracks likely next improvements and helps keep repo evolution intentional.

## Current priorities

### P1 — Done
- **Meta-evals for scope completeness and decision utility** ✅
  - `evals/meta/scope-completeness-discipline.md` (Family F diagnosis)
  - `evals/meta/decision-utility-discipline.md` (diagnosis, distinct from existing rubric)
  - `references/scope-completeness-discipline.md` (reusable minimum-coverage rule)
  - Wired into execution chain: SKILL.md, ROUTING-MATRIX.md route Attach, route-activation-audit.md, final-audit.md

### P1 — Remaining
- Use `SYSTEM-MAP.md` to tighten family-level coverage and identify where a dedicated family map, route-supporting reference, checklist hardening, or delivery note is still missing.
- Add more evals for freshness, counter-evidence, and decision-quality regressions.
- Test the skill against more real fast-moving company/product cases.
- Tighten current-state verification if stale facts still leak into reports.
- Continue testing whether the stale-anchor hard gate (added to `checklists/listed-company-report.md`) reliably triggers during real listed-company synthesis, and harden route activation if the gate keeps being skipped.
- Harden checklist-level gates for scope-completeness and decision-utility enforcement (final-audit recall discipline).
- Keep eval subtype formalization limited to naming conventions (`evals/README.md#naming-conventions`) unless eval volume justifies new folders.
- Run at least 2-3 more real comparative-distillation cases and promote only the recurring candidate rules.
- Validate the new market-outlook routing against 2-3 more real cases before hardening further wording or adding more specialized sub-checklists.
- **Validate the new technical deep-dive routing** against 2-3 real technical analysis cases (architecture comparison, feasibility assessment, patent analysis) and harden the route definition if activation or artifact contract execution is weak.

### P2
- Expand finance/investment-specific guidance for valuation, consensus, and reporting-period handling.
- Add more examples of good and bad outputs.
- Improve task-type guidance for company, vendor-selection, technical-feasibility, and market-outlook research.
- Continue separating rendering-layer PDF fixes from research-discipline commits so layout failures can be traced independently.
- **Validate whether recent CJK text-rhythm tweaks actually reduce the "broken export / OCR-like spacing" feel in Chinese-heavy PDFs before making larger visual changes.**
  - Validation uncovered two pipeline bugs that were fixed:
    - `normalize_text_for_pdf()` used `\s+` in CJK spacing regexes, which matched across newlines and merged headings with body paragraphs
    - `unicodedata.normalize('NFKC', ...)` degraded Chinese fullwidth punctuation (（）→(), ，→,) to ASCII equivalents
  - Both bugs fixed (`\s+` → `[ \t]+`; `NFKC` → `NFC`). Re-validated against 2 reports (5,000+ CJK chars each) — block structure preserved, CJK punctuation intact, no cross-paragraph merging.
  - See `evals/cases/cjk-pdf-validation-findings-case.md` for full results.
  - Remaining: testing against more report types (code-heavy, academic), adding CI gate for rendering regression.
- Add one more real-case pass on market-entry memo information design so recommendation, hard gates, shortlist, and phased-entry blocks become easier to scan in PDF output.
- **Validate the new private company / startup evaluation routing** against 2-3 real private company cases and harden the route definition if activation or artifact contract execution is weak. (Closes #121)

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
