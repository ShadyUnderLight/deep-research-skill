# Forward Eval: Company and Technical Mixed Case

## Route and audit status

**Primary route**: Technical Deep-dive

**Secondary routes**: Listed Company

| Audit | Status | 证据 | 数字角色 |
|---|---|---|---|
| technical-analysis-audit | ✅ Passed | report-section:Technical judgment | process |
| source-traceability | ✅ Passed | report-section:Source Register | process |
| final-audit | ✅ Passed | report-section:Executive summary | process |
| listed-company-secondary-hard-fail | ✅ Passed | report-section:Company boundary | process |

## Executive summary

**核心判断**：The technical mechanism is the primary decision burden; company
valuation is a bounded secondary route [S01].

- The architecture comparison drives the report structure.
- The company-level hard-fail conditions are independently recorded.

## Technical judgment

Architecture A is more viable for the stated workload because its failure
boundary is observable and its deployment assumptions are explicit [S01] [S02].

## Company boundary

The listed-company secondary route is limited to checking the company context;
it does not replace the technical comparison. The company data is treated as a
separate evidence layer [S02].

## Comparison table

| Dimension | Architecture A | Architecture B |
|---|---:|---:|
| Recovery coverage | 90 | 70 |
| Operational burden | 60 | 80 |

## Source Register

| ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
|---|---|---|---|---|---|---|
| S01 | Technical paper | peer-reviewed paper | 2026-05-01 | https://example.com/technical | high | architecture viability |
| S02 | Company filing | secondary | 2026-06-01 | https://example.com/company | medium | company context |

```contract
{
  "artifact_id": "forward-company-technical-mixed",
  "contract_version": "1",
  "created_at": "2026-08-17",
  "primary_route": "technical-deep-dive",
  "closest_alternative": "market-outlook",
  "boundary_judgment": {
    "checked_conditions": ["technical mechanism burden", "market overview boundary"],
    "why_not_alternative": "The report must judge architecture feasibility rather than describe market evolution.",
    "switch_conditions": "Switch to market-outlook if the technical mechanism is no longer load-bearing."
  },
  "secondary_routes": ["listed-company"],
  "disciplines": ["current-state", "source-traceability", "forward-looking", "quantitative-role"],
  "audits": [
    {"id": "technical-analysis-audit", "status": "passed", "evidence": "report-section:Technical judgment"},
    {"id": "source-traceability", "status": "passed", "evidence": "report-section:Source Register"},
    {"id": "final-audit", "status": "passed", "evidence": "report-section:Executive summary"},
    {"id": "listed-company-secondary-hard-fail", "status": "passed", "evidence": "report-section:Company boundary"}
  ]
}
```
