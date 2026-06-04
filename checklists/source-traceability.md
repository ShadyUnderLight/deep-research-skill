# Source Traceability Checklist

Use this checklist when the output includes confidence labels (confirmed / likely / uncertain) or is structured as a research memo.

Run through every item before delivering the final report.

## Inline citations

- [ ] every important claim in the body text has a source id in `[SN]` format (or functionally equivalent non-`[SN]` format — see format equivalence exemption in `references/source-traceability-and-claim-citation.md`)
- [ ] each `[SN]` maps to a single specific source, not a generic "multiple sources"
- [ ] inferred claims use `[IN]` with a documented reasoning chain in the register
- [ ] unconfirmable claims use `[UN]` and are listed in the uncertainty register
- [ ] **hard-fail gate**: see ternary severity below; a report with a bibliography but zero body-level references of any kind is not deliverable
- [ ] **conditional pass**: functionally equivalent non-`[SN]` inline format (Author-Year / arXiv ID / DOI / natural language uniquely identifying the source) + structured register exists → pass with recommendation to add `[SN]` references
- [ ] **full pass**: structured `[SN]` inline citations + complete register

## Source register

- [ ] source register is present and structured (not a loose bibliography)
- [ ] source register uses the 7-column template: ID / Source Name / Source Type / Date / DOI/URL / Reliability / Claims Supported
- [ ] every register entry has a DOI/URL where available; for offline sources, the limitation is noted explicitly
- [ ] every register entry has a `Claims Supported` column with § section references that match body citations
- [ ] Source Type is one of the simplified 5-class system (`primary` / `secondary` / `inferred` / `vendor-claim` / `unconfirmed`) or a compatible granular type (see `references/source-traceability-and-claim-citation.md`)
- [ ] Reliability consistency: if Source Type is `vendor-claim`, `inferred`, or `unconfirmed`, Reliability must be `low`
- [ ] no source id is listed but never cited in the body

## Source type discipline

- [ ] primary sources (official filings, company disclosures, primary documents) are distinguished from secondary (media, analyst reports)
- [ ] inferred claims are labeled `[IN]` and not presented as confirmed facts
- [ ] no source is given higher weight than its type warrants
- [ ] for load-bearing tier / positioning judgments, the body text makes visible which key claims are direct-evidence-backed vs inference-heavy rather than hiding the weighting inside a bibliography or source register
- [ ] self-tests, partner/customer marketing, roadmap reporting, and valuation signals are not allowed to silently carry the same weight as current primary evidence in the final classification

## Completeness

- [ ] no key claim is left without a traceable source
- [ ] the report reads as auditable — a reader can follow any claim back to a specific source entry
- [ ] if a reviewer highlighted the 3-5 sentences doing the most thesis work, each of those sentences would still be defendable without additional hidden notes

## Flags

If any item above is not satisfied, revise the report before delivery. A report without traceability is not a sufficient output of this skill.
