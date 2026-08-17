# Market Outlook 2027 with Secondary Route — Positive Fixture (issue #378)

Mixed-route report: primary market-outlook with secondary constrained-choice.
The secondary's hard-fail verification is tracked by an independent
`constrained-choice-secondary-hard-fail` audit entry.

## Route and audit status

**Primary route**: Market Outlook

**Secondary routes**: Constrained Choice / Shortlist

| Audit | Status | 证据 |
|-------|--------|------|
| market-outlook-audit | ✅ Passed | §3 监控信号完整 |
| forward-looking-claims | ✅ Passed | §4 前瞻数字均带标签 |
| source-traceability | ✅ Passed | §3-§5 正文使用 [S01]-[S03] 引用 |
| final-audit | ✅ Passed | §2-§6 各核心关卡可追溯 |
| quantitative-role-audit | ✅ Passed | §5 Comparison 表格含数字角色列 |
| constrained-choice-secondary-hard-fail | ✅ Passed | §6 独立验证 4 项 hard-fail 条件 |

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
{"primary_route": "market-outlook", "secondary_routes": ["constrained-choice"], "disciplines": [], "audits": [{"id": "market-outlook-audit", "status": "passed", "evidence": "§3"}, {"id": "forward-looking-claims", "status": "passed", "evidence": "§4"}, {"id": "source-traceability", "status": "passed", "evidence": "§5"}, {"id": "final-audit", "status": "passed", "evidence": "§2"}, {"id": "constrained-choice-secondary-hard-fail", "status": "passed", "evidence": "§6 verified 4 hard-fail conditions"}], "artifact_id": "fixture-market-outlook-mixed-pos", "contract_version": "1.0.0", "created_at": "2026-08-13"}
```
