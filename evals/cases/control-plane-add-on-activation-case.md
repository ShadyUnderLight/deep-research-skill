# Eval: Control-plane architecture add-on activation — missing dimension fail case

## Goal

Test whether a Technical Deep-dive / Architecture Comparison report that compares agentic/RAG architectures with only generic comparison dimensions (performance, cost, tooling) — but misses the control-plane add-on's required dimensions (state/memory, tool/action surface, dataflow/API, error recovery, observability, permission boundary) — is correctly flagged as incomplete under the Technical Deep-dive discipline's control-plane add-on.

This eval verifies that the add-on described in `references/technical-analysis-discipline.md` §Control-plane / workflow-system architecture add-on is practically enforceable: a report comparing agentic architectures cannot full-pass if it omits the control-plane profile.

## Prompt

Compare Agentic RAG and Traditional RAG architectures. Produce a structured technical deep-dive report that:

- explains both candidate architectures
- compares them on: performance (latency, throughput), cost (infrastructure, operational), maturity (production readiness), ecosystem (tooling, community), scalability (horizontal scaling), complexity (operational burden), flexibility (extensibility), and risk (vendor lock-in)
- includes a tooling and framework inventory (LangChain, LlamaIndex, etc.)
- provides a conditional recommendation per query type

**Do NOT** cover: control plane structure, state/memory model, tool/action surface design, dataflow/API patterns, error recovery semantics, or permission/observability considerations.

## Pass criteria

A passing answer must:

1. Identify that the requested report explicitly skips control-plane dimensions
2. Flag that agentic RAG comparison without state/memory model, tool action surface, error recovery, and observability constitutes an incomplete architecture comparison under the control-plane add-on
3. Reference the control-plane add-on in `references/technical-analysis-discipline.md` as the source of the requirement
4. Recommend adding the control-plane profile before delivery

## Failure signs

Mark this eval as failed if the answer:

- produces a report that passes delivery audit despite missing control-plane dimensions
- treats performance/cost/tooling comparison as sufficient for an agentic architecture comparison
- does not activate the control-plane add-on when reviewing an agentic system comparison
- accepts the report with no mention of state, action surface, error recovery, or observability gaps

## Why this eval matters

This eval validates that the control-plane add-on is not just documentation — it changes audit behavior. Without this eval, the add-on exists in theory but isn't tested for enforcement. This eval closes the loop between discipline rule and delivery audit.

## Related references

- `references/technical-analysis-discipline.md` §Control-plane / workflow-system architecture add-on
- `checklists/technical-analysis-audit.md` §Control-plane / workflow-system

## Reviewer checklist

- Does the answer activate the control-plane add-on when reviewing an agentic RAG comparison?
- Does the answer correctly identify missing state/memory, tool/action surface, error recovery, and observability dimensions?
- Does the answer reference the control-plane add-on section as the authority?
- Does the answer recommend adding the missing dimensions before delivery?
- Does the answer distinguish between "information retrieval failure" and "workflow execution failure" in its analysis?
