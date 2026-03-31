# Eval: Source Traceability — Moore Threads Report

## Goal

Test whether the skill produces a report where every important claim can be traced to a specific source, with proper source-type classification, inline citations, and an auditable reasoning chain for inferred claims.

This eval is based on a Moore Threads report that showed improved structure and source awareness but still failed to provide claim-level traceability — sources were listed at the end, but no inline citations existed and key claims could not be audited.

## Prompt

Research Moore Threads as of today and produce a deep-research style memo covering:

- company identity and capital markets status
- current product lineup and positioning
- financial trajectory
- competitive position
- investment thesis and key risks
- bottom line

The output must use a two-layer traceability system:

1. Inline `[SN]` citations for every important claim in the body
2. A structured source register at the end mapping each source id to type, date, relevance, and notes

Inferred claims must be labeled `[IN]` with an explicit reasoning chain. Unconfirmable claims must be labeled `[UN]` with an uncertainty register entry.

## What this eval is testing

- whether the model uses inline citations, not just a bibliography
- whether each important claim can be traced to a specific source id
- whether source type is classified (primary filing / primary company / secondary media / inferred / unconfirmed)
- whether inferred claims have documented reasoning chains
- whether current-state claims are sourced to current or recent primary sources rather than stale filings
- whether the source register is structured and complete, not just a list of URLs
- whether the two-layer citation system makes the report auditable

## Pass criteria

A good answer should:

1. Use inline `[SN]` citations for every significant claim in the body.
2. Provide a structured source register at the end with at minimum:
   - source id
   - source title/description
   - source type (primary / secondary / inferred / unconfirmed)
   - date or version
   - relevance
   - reliability notes
3. Clearly label inferred claims with `[IN]` and document the reasoning chain.
4. Clearly label unconfirmable claims with `[UN]` and explain what would be needed to verify.
5. Avoid treating media reports, filings, and company disclosures as equivalent in weight.
6. Avoid presenting an inference as a confirmed fact.
7. Avoid over-citation where every sentence has five source ids.
8. Avoid using a stale filing as the sole source for a current-state claim.

## Failure signs

Mark this eval as failed if the answer does any of the following:

- has a long sources list but no inline `[SN]` citations in the body
- lists the same source repeatedly for unrelated claims without mapping which claim comes from which source
- treats a prospectus, a news article, and an analyst inference as equally reliable sources
- presents an inferred conclusion without `[IN]` notation or reasoning chain documentation
- presents a claim about the current state sourced only to a filing or article from many months earlier without noting the gap
- uses vague citations such as "来源：SCMP" at the end of a paragraph without specifying what in SCMP supports which claim
- produces a source register that is descriptive rather than structured (e.g., full URLs without ids, no type classification)

## Why this eval matters

A report can have good structure, correct facts, and even confidence labels — and still be unauditable.

This is a different failure mode from:

- stale facts (covered by freshness eval)
- pseudo-precision (covered by finance and market-share discipline eval)
- ranking overreach (covered by ranking/current-claims eval)

It is about **reasoning transparency**, not outcome correctness.

A well-traced report allows a reader to:

- verify specific claims
- challenge specific inferences
- understand why a conclusion was drawn
- see what remains unconfirmed

Without this, even a factually correct report leaves the reader unable to assess quality.

## Reviewer checklist

- Does each key claim have an inline `[SN]` citation?
- Does the source register map each id to a specific, classified source?
- Are inferred claims labeled `[IN]` with a documented reasoning chain?
- Are unconfirmable claims labeled `[UN]` with an uncertainty register?
- Is source type distinguished (primary vs secondary vs media vs inferred)?
- Is the bibliography replaced by a structured source register?
- Are current-state claims sourced to reasonably current evidence?
- Is the citation density appropriate (not under-cited, not over-cited)?

## Suggested scoring

- Pass: the two-layer citation system is fully operational; every key claim is traceable to a classified source; inferred claims are documented; the source register is structured and complete.
- Partial: some citations exist but the system is incomplete or inconsistent; some important claims lack inline citations; the source register exists but lacks type classification or reasoning chains for inferences.
- Fail: the report has a sources list but no meaningful claim-level traceability; or the report presents inferences as confirmed facts; or source types are not distinguished.
