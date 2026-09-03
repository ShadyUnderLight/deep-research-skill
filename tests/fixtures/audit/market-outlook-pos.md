# Market Outlook 2027 — Positive Fixture (issue #378)

## Route and audit status

**Primary route**: Market Outlook

| Audit | Status | 证据 |
|-------|--------|------|
| market-outlook-audit | ✅ Passed | report-section:Monitoring signals |
| forward-looking-claims | ✅ Passed | report-section:Monitoring signals |
| source-traceability | ✅ Passed | report-section:Findings |
| final-audit | ✅ Passed | report-section:Executive summary |
| quantitative-role-audit | ✅ Passed | report-table:Comparison Table |

## Executive summary

**核心判断**：market growth will continue through 2027 [S01].

- Demand keeps rising
- Supply remains constrained

## Findings

Body text with citations [S01], [S02] and [S03].

## Monitoring signals

| Signal | Threshold | Cadence | Source | Trigger-to-action | 数字角色 |
|--------|-----------|---------|--------|-------------------|---------|
| Signal A | ≥2.0 | monthly | [S01] | rebalance | observed |
| Signal B | ≤1.5 | weekly | [S02] | hedge | observed |
| Signal C | ≥10% | quarterly | [S03] | reallocate | observed |

## Comparison Table

| Metric | System A | System B | 数字角色 |
|--------|----------|----------|---------|
| Cost | 100 | 80 | observed |
| Speed | 200 | 150 | observed |

## Dimension conclusions

Each dimension conclusion is backed by [S01] and [S02].

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|----|-------------|-------------|------|---------|-------------|------------------|
| S01 | Example A | secondary | 2026-01-01 | https://example.com/a | medium | §3 |
| S02 | Example B | secondary | 2026-02-01 | https://example.com/b | high | §5 |
| S03 | Example C | secondary | 2026-03-01 | https://example.com/c | high | §4 |

```contract
{"primary_route": "market-outlook", "secondary_routes": [], "disciplines": [], "decision_tree_version": 1, "activation_snapshot": {"activation_id": "forward-market-outlook-baseline", "snapshot_version": 2, "decision_tree_version": 1}, "audits": [{"id": "market-outlook-audit", "status": "passed", "evidence": "report-section:Monitoring signals"}, {"id": "forward-looking-claims", "status": "passed", "evidence": "report-section:Monitoring signals"}, {"id": "source-traceability", "status": "passed", "evidence": "report-section:Findings"}, {"id": "final-audit", "status": "passed", "evidence": "report-section:Executive summary"}], "artifact_id": "fixture-market-outlook-pos", "contract_version": "1.0.0", "created_at": "2026-08-13"}
```
