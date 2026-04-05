# Eval: Cambricon Evidence-Weighting and Traceability Case

## Goal

Test whether the skill can keep a multidimensional positioning memo auditable when the load-bearing judgment depends on mixed evidence types.

This eval is based on a real failure mode: the report used labels such as confirmed fact / inference / open uncertainty, but the key conclusion still blurred direct evidence, self-tested performance claims, media-reported roadmap material, market interpretation, and valuation signals into one polished narrative.

## Prompt

Assess Cambricon's current competitive position as of today and produce a structured memo that evaluates at least:

- technical capability
- product adoption / commercial traction
- ecosystem strength
- capital-markets or financing position when relevant

Requirements:
- use inline claim-level traceability
- distinguish confirmed facts, inference, and open uncertainty
- make clear which load-bearing claims are supported by direct evidence vs indirect evidence
- do not let self-tests, roadmap reports, valuation signals, or partner/customer marketing silently carry the same weight as current primary evidence
- if an overall positioning label is used, show why the evidence mix is still sufficient

## What this eval is testing

- whether the report is not only sourced, but auditable at the exact claims that matter most
- whether mixed evidence types are separated visibly in the body
- whether the model avoids confidence theater created by combining strong and weak evidence in one sentence or table
- whether the final classification reflects evidence quality instead of only report polish

## Pass criteria

A good answer should:

1. Make key claims traceable.
   - the main positioning claims in the body have visible source ids or claim markers
   - the source register distinguishes primary, secondary, inferred, and unconfirmed material

2. Make weighting visible.
   - current primary facts are visually or verbally separated from self-tests, media reporting, and inference
   - at least the load-bearing claims show what kind of evidence they rest on

3. Prevent silent evidence substitution.
   - valuation strength does not silently become product/ecosystem leadership
   - China-market traction does not silently become global first-tier status
   - roadmap reporting does not silently become current product competitiveness

4. Keep inference honest.
   - inferred claims are documented as such
   - the memo states the main limitation where an inference carries a crucial part of the conclusion

## Failure signs

Mark this eval as failed if the answer does any of the following:

- adds a source list but still leaves the key final judgment unauditable
- uses one confidence label for a sentence that mixes audited revenue, self-tested performance, and roadmap expectations
- cites sources but does not tell the reader which key judgment is direct vs inferred
- lets a weak or indirect evidence layer do too much work in the final classification without saying so
- presents a polished final ranking that sounds stronger than the underlying evidence mix

## Why this eval matters

Some reports fail even after adding sources, because the real problem is not missing URLs but missing evidence-role separation.

This eval catches a more subtle failure family:

- traceability theater instead of true auditability
- confidence labels without weighting discipline
- mixed evidence types collapsing into one neat bottom line

If the skill cannot pass this eval, it is still vulnerable to persuasive but weakly-auditable company-positioning memos.

## Reviewer checklist

- Are the load-bearing claims in the body visibly traceable?
- Can the reader tell which key claims are direct evidence vs inference-heavy?
- Are self-tests, roadmap reporting, valuation signals, and partner claims prevented from doing hidden work in the conclusion?
- Does the final judgment match the strength of the evidence mix?

## Suggested scoring

- Pass: the memo is auditable at the claim level and visibly separates strong evidence from inference-heavy judgment
- Partial: sourcing exists, but the main judgment still compresses mixed evidence too aggressively
- Fail: the report looks sourced but still obscures which evidence actually supports the bottom line
