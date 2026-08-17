# Workflow Review 2026 — Negative Fixture (issue #378)

The final-audit manual audit is NOT declared in the Route and audit status
block: under strict mode the verdict must fail closed with `not_run`
instead of pretending the gate was executed.

## Route and audit status

**Primary route**: Shared-workflow

| Audit | Status | 证据 |
|-------|--------|------|
| workflow-spine-audit | ✅ Passed | §3 工作流脊柱可追溯 |
| quantitative-role-audit | ✅ Passed | §5 Comparison 表格含数字角色列 |

## Executive summary

**核心判断**：the workflow review concludes X is adequate [S01].

- Key bullet one
- Key bullet two

## Findings

Body text with citations [S01] and [S02].

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

```contract
{"primary_route": "shared-workflow", "secondary_routes": [], "disciplines": [], "audits": [{"id": "workflow-spine-audit", "status": "passed", "evidence": "§3"}, {"id": "final-audit", "status": "passed", "evidence": "§2"}], "artifact_id": "fixture-shared-workflow-neg", "contract_version": "1.0.0", "created_at": "2026-08-13"}
```
