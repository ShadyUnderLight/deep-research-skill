# Code-heavy delivery regression

## Contract example

```contract
{
  "primary_route": "technical-deep-dive",
  "secondary_routes": [],
  "disciplines": ["source-traceability"],
  "audits": [{"id": "final-audit", "status": "passed", "evidence": "§1"}]
}
```

```python
def render_marker(value: str) -> str:
    return f"code-heavy-marker-{value}"
```
