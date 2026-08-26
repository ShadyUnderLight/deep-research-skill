# Claim–Source Alignment Audit

Use this checklist when the **opt-in** claim–source alignment audit is explicitly enabled for a delivery task. This audit is **default off** (issue #419).

## Scope

This audit checks whether **locator-bound excerpts** support specific claims — not whether citations exist, not whether sources are authentic, and not whether the overall research conclusion is correct.

**In scope**

- machine-readable evidence records bind `claim_id`, `source_id`, locator, retrieval status, excerpt hash, and evidence role
- bounded verdicts: `SUPPORTED`, `PARTIAL`, `UNSUPPORTED`, `AMBIGUOUS`, `RETRIEVAL_FAILED`, `NOT_RUN`
- offline rule-based evaluator + calibration gold set (CI only)

**Out of scope**

- proving sources are genuine or experiments were run
- replacing source-traceability, counter-evidence, quantitative-role, or route-specific audits
- LLM memory judgments without locator/excerpt evidence
- live search or paid-model calls in CI

## Default-off policy

- Do **not** enable this audit in routine delivery unless calibration has passed and the task carries an alignment bundle.
- Calibration passing **does not** mean production semantic correctness — only that the offline evaluator matches the gold set under declared thresholds.
- Re-evaluate default-off when: fixture coverage is stable, artifact/hash binding is proven in production paths, and per-class FNR/FPR meet thresholds on an updated gold set.

## Verdict discipline

- [ ] `RETRIEVAL_FAILED` is recorded as tool/access failure — **not** upgraded to `UNSUPPORTED`
- [ ] `NOT_RUN` / anchorless locators (`kind: none`) **cannot** aggregate to overall Pass
- [ ] `PARTIAL` includes non-empty subclaim decomposition; empty decomposition is not masked as plain `UNSUPPORTED` or `SUPPORTED`
- [ ] `AMBIGUOUS` is used when evidence–claim linkage cannot be reliably judged from the excerpt

## Structural binding

- [ ] every evidence record binds the correct `claim_id` and `source_id`
- [ ] `excerpt_hash` matches the retrieved excerpt bytes when `retrieval_status: fetched`
- [ ] section locators resolve against **visible** Markdown (hidden fence/HTML locators fail closed)
- [ ] route / artifact hash mismatches fail closed when bindings are declared
- [ ] an enabled audit result records and downstream consumers re-hash the exact claim-alignment bundle; changing that bundle invalidates the result

## Calibration (maintainers)

- [ ] gold keys live in an isolated file — not embedded in production bundles or candidate prompts
- [ ] calibration output records fixture version, sample counts, per-class FNR/FPR, and threshold
- [ ] CI runs `python3 scripts/validate_claim_alignment.py --calibrate …` on the gold set only

## Commands

```bash
python3 scripts/validate_claim_alignment.py tests/fixtures/claim-alignment/valid.json
python3 -m pytest -q tests/test_claim_alignment.py tests/test_claim_alignment_calibration.py
python3 scripts/audit_report.py report.md --enable-claim-alignment \
  --claim-alignment-bundle bundle.json --json
```
