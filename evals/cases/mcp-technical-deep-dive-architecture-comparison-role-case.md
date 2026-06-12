# Eval: MCP Protocol Technical Deep-Dive — Architecture Comparison Role and Load-Bearing Trade-off Case

## Goal

Test whether a Technical Deep-dive / Architecture Analysis report with explicit comparison dimensions and functional feature comparison can still **fail delivery** when:

- **comparator roles are absent** — alternatives are listed by name only (MCP vs A2A vs Function Calling) without explaining their comparative role (substitute, complement, ancestor, or unrelated approach)
- **comparison is a flat feature list** — dimensions are listed side-by-side but the table is a functional inventory rather than an architectural judgment tool
- **load-bearing dimensions are not identified** — the reader cannot tell which comparison dimensions drive the recommendation vs. which are background context
- **no exclusion rationale** — common comparators are omitted without explaining why
- **recommendation lacks reversal conditions** — the report says "choose MCP when..." but does not say what conditions would change the recommendation

This eval tests the **architecture comparison role** gap: reports that produce well-structured comparison tables can still fail to deliver architectural judgment if the table is a feature parity matrix rather than a role-aware, trade-off-driven comparison.

## Prompt

Analyze the MCP (Model Context Protocol) protocol's architecture and compare it to relevant alternatives. Produce a structured technical deep-dive report that:

- explains MCP's core mechanisms (participant model, transport layer, lifecycle, primitive system)
- identifies fundamental constraints and non-goals
- compares MCP to relevant alternatives with **explicit comparator roles**: each alternative should be classified as direct substitute, complement, design ancestor, or unsuitable comparator with exclusion rationale
- includes a comparison table that visibly distinguishes comparator roles (not just feature columns)
- explains which comparison dimensions are **load-bearing** vs. background information
- states **reversal conditions** — under what circumstances would the recommendation change
- includes counter-evidence (complexity, security model limitations, deprecation risk)
- provides actionable judgments for practitioners

## What this eval is testing

- whether comparator roles are present in an architecture comparison (substitute / complement / ancestor / excluded)
- whether the comparison table includes a role dimension beyond feature parity
- whether a trade-off interpretation follows the comparison table, identifying load-bearing dimensions
- whether exclusion reasons are stated for common but irrelevant comparators
- whether the recommendation states conditions that would reverse the judgment

## Pass criteria

A passing answer should:

### 1. Classify each comparator by role

Each compared alternative should have an explicit role, for example:

| 方案 | 比较角色 | 理由 |
|------|----------|------|
| LSP (Language Server Protocol) | Historical / design ancestor | JSON-RPC-based protocol pattern, same participant model ancestor |
| Google A2A (Agent-to-Agent) | Complement at application layer | Solves different problem (inter-agent vs. tool-access), can coexist |
| OpenAI Function Calling | Direct substitute in tool-calling scope | Overlapping capability for LLM tool execution, different architectural approach |
| REST/OpenAPI | API-description alternative | Addresses tool description but at different abstraction level; should be acknowledged and compared or excluded with reason |

### 2. Include a comparison table with role column

The comparison table should have a column for comparator role (not just name, features, pros/cons).
A 3-column table ("MCP / A2A / Function Calling" with features listed) without role column is **not sufficient**.

### 3. Provide after-table trade-off interpretation

The comparison table must be followed by a short interpretation block that:
- identifies which 2-3 dimensions are **load-bearing** (drive the recommendation)
- explains why the remaining dimensions are background only
- states what conditions would reverse the recommendation

### 4. State exclusion rationale (if applicable)

If common alternatives are excluded from the comparison (e.g., gRPC, WebSocket, REST), the report should briefly state why they are not the right comparison objects (different layer, different problem scope, etc.).

### 5. Make a conditional recommendation

The recommendation should state both:
- under what conditions MCP is preferred
- under what conditions an alternative would be preferred

## Failure signs

Mark this eval as failed if the answer does any of the following:

- lists alternatives without any comparator role classification
- provides a feature comparison table without a role column or role annotation
- the comparison is a functional feature list (MCP does X, A2A does Y) without architectural judgment
- the comparison table lacks after-table interpretation (load-bearing vs. background not distinguished)
- the recommendation is unconditional — no mention of what would change the conclusion
- common comparators (e.g., REST, gRPC) are silently excluded without rationale
- the report reads like a "which protocol to pick" choice memo rather than a role-aware architecture analysis

## Why this eval matters

This case adds an **architecture comparison role** failure mode not yet covered by existing technical-deep-dive cases:

| Case | Route | Level | Core failure |
|------|-------|-------|-------------|
| MCP timeline/roadmap | technical-deep-dive | Fail | Timeline inconsistency + roadmap state not separated |
| MCP opening baseline | technical-deep-dive | Fail | Opening lacks audience, decision scenario, version baseline |
| CPO inline citation | technical-deep-dive | Conditional pass | Body citations absent, vendor claims lack caveats |
| K8s vs Swarm | technical-deep-dive | Conditional pass | Self-assessment overconfident, benchmark method missing |
| **MCP comparator roles (this)** | technical-deep-dive | **Fail** | **Comparison is feature parity without comparator roles or load-bearing interpretation** |

Existing cases test whether comparison dimensions are explicit and load-bearing. This case goes further: it tests whether the **comparison structure itself** reveals the architectural relationships between alternatives, not just their feature differences.

A report with "MCP vs A2A vs Function Calling" listed side-by-side with dimensions can pass existing checks (dimensions are explicit, trade-offs are stated) but still fail the reader's need to understand *why these three are compared* and *what their relationship is*.

## Current rule verdict

The current rules would **not reliably catch** this failure:

- technical-analysis audit §Comparison structure: checks for explicit dimensions, criteria, trade-offs, 4+ dimensions — but does not check for comparator roles or after-table interpretation
- technical-analysis audit line 49: checks "recommendation explains which dimensions are load-bearing" — this is the closest existing rule, but it does not require after-table interpretation or exclusion rationale
- ROUTING-MATRIX visible artifact contract: requires "candidate architectures" but not comparator roles or role-based comparison structure

This eval case guards against **role-blind architecture comparison** — where the table is technically complete but structurally uninformative for architectural judgment.

## Related evals

- `evals/cases/mcp-technical-deep-dive-timeline-roadmap-case.md` — same route, timeline integrity and roadmap state
- `evals/cases/mcp-technical-deep-dive-opening-baseline-case.md` — same route, opening baseline
- `evals/cases/technical-analysis-kubernetes-vs-docker-case.md` — same route, architecture comparison route activation
- `evals/cases/cpo-technical-deep-dive-inline-citation-absent-case.md` — same route, self-assessment overconfidence
- `evals/cases/rag-technical-deep-dive-register-gap-case.md` — same route, register gaps

## Reviewer checklist

- Are comparator roles visible for each alternative (substitute / complement / ancestor / excluded)?
- Does the comparison table include a role column or equivalent role annotation?
- Is there an after-table interpretation identifying load-bearing dimensions?
- Are exclusion reasons stated for silently omitted common comparators?
- Does the recommendation state reversal conditions?
- Is the comparison an architectural judgment tool, not just a feature parity matrix?

## Suggested scoring

- **Pass**: comparator roles explicit, role column visible in table, after-table interpretation present, load-bearing dimensions identified, reversal conditions stated, exclusion rationale if applicable
- **Conditional pass**: comparator roles present but implicit in text rather than visible in table structure, or after-table interpretation present but thin (2-3 most important), or roles present but 1 omission — no architectural judgment failure
- **Fail**: no comparator roles (flat feature list), or no after-table interpretation, or recommendation unconditional, or common comparators silently excluded, or comparison reads as feature inventory rather than architectural analysis
