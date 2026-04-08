# Eval: Final Delivery Cleanliness

Use this eval when the research may be solid, but the final user-facing artifact still feels unfinished, leaky, or export-shaped.

## Goal

Distinguish between:

1. reasoning quality
2. delivery quality

A report can succeed analytically and still fail as a delivered memo, markdown file, or PDF. This eval exists to prevent delivery failures from being excused as cosmetic issues.

---

## Typical failure patterns

- citation syntax, retrieval traces, or placeholder residue leak into the final body
- heading hierarchy is technically present but visually weak or confusing
- tables are too dense, too wide, or poorly broken for PDF readability
- markdown looks acceptable, but PDF output degrades spacing, structure, or scanability
- the report reads like a stitched analyst worksheet rather than a deliberate final memo
- internal process labels leak into user-facing sections without adding reader value

---

## What this eval is testing

### Failure Mode 1: Artifact leakage

The final report still exposes internal machinery.

Examples:
- unresolved placeholder text
- raw citation placeholders
- template markers
- retrieval syntax or parser debris

### Failure Mode 2: Export degradation

The source markdown may be reasonable, but the final delivered artifact is weak.

Examples:
- PDF hierarchy is flattened
- spacing becomes irregular or hard to scan
- a table dominates the page and becomes unreadable
- bullets collapse into dense text blocks

### Failure Mode 3: Delivery-shape mismatch

The artifact does not support the kind of reading the report is meant to enable.

Examples:
- decision memo reads like background notes
- key recommendation is visually buried
- hard gates and change conditions are hard to locate
- source appendix overwhelms the actual decision logic

---

## Pass criteria

A good final artifact should:

1. read like an intentional deliverable, not a draft export
2. avoid visible placeholders, citation residue, and parser leakage
3. preserve heading hierarchy and scanning structure in both markdown and PDF when PDF is produced
4. keep the main recommendation, ranking, or judgment visually easy to find
5. treat PDF degradation as a real delivery failure when it harms readability

---

## Scoring guide

Use a simple 0-2 scale.

### 0 = failed delivery
- the artifact visibly leaks internal residue or is hard to read as a final deliverable

### 1 = acceptable but unstable delivery
- the artifact is mostly usable, but noticeable cleanliness or rendering weaknesses remain

### 2 = polished delivery
- the artifact feels deliberate, clean, and readable in its delivered form

---

## Review questions

When using this eval, ask:

- Would a reader perceive this as a final memo or as an exported work file?
- Are there any unresolved placeholders, citation leaks, or internal labels that should not be visible?
- Does the heading, bullet, and table structure help scanning or hurt it?
- If PDF was generated, was the PDF actually reviewed as a deliverable?
- Does the final artifact preserve the route's decision readability, or does formatting bury it?

---

## Output format for reviewers

When you apply this eval, summarize the result as:

- **Artifact type reviewed:** markdown / PDF / both
- **Visible residue or leakage:**
- **Rendering or readability weaknesses:**
- **What still scans well:**
- **What feels unfinished or export-shaped:**
- **Diagnosis:** artifact leakage / export degradation / delivery-shape mismatch
- **Best next fix:** template hardening / checklist hardening / export-pipeline fix / route-specific formatting rule

---

## Why this eval exists

As the research system improves, more weak outputs will fail not because the analysis is wrong, but because the artifact is not ready for delivery. This eval makes final-delivery quality a first-class standard instead of a cosmetic afterthought.
