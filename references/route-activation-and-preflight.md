# Route Activation and Preflight

## Purpose

Route activation exists to make task classification explicit before deep collection begins.

A route is not chosen because it sounds relevant.
It is chosen because it most strongly determines:

- report structure
- evidence burden
- audit burden
- visible artifact contract

If route selection stays implicit, research often drifts back into generic overview mode.

## Preflight questions

Before deep collection, decide:

- What is the primary route?
- What is the closest alternative route?
- Why does the chosen route win?
- What secondary disciplines are required?
- What visible artifact contract must the final report satisfy?
- What audits must run before delivery?

Do not treat generic research as automatically sufficient when a specialized route would materially change structure or audit burden.

## How to choose the primary route

Choose the route that most strongly determines:

- how the report must be structured
- what evidence burden the task carries
- what audit burden the final artifact must satisfy

If one route mainly changes wording while another changes structure and audit expectations, choose the latter.

## Preflight steps

After identifying candidate routes and before finalizing route selection, execute these verification steps.

### Step 1: Exclusion clause check

Before committing to a route, check the route's **"Do not use"** and **"Often confused with"** clauses in `ROUTING-MATRIX.md`.

- If the task matches a "Do not use" condition → do not use this route. Reconsider route selection.
- If the boundary is ambiguous (the task partially overlaps with "Often confused with" routes) → document the boundary judgment: why this route still wins despite the overlap, or switch to the more appropriate route.
- Do not skip this check because the route "feels right" for the topic — topic label is not the same as decision burden.

### Step 2: Secondary-route hard-fail verification

If the preflight identifies a secondary route (in addition to the primary route), its hard-fail conditions must be verified **at selection time**, not deferred to delivery.

- Read the secondary route's hard-fail conditions from `ROUTING-MATRIX.md`.
- If a condition is genuinely inapplicable to the task (e.g., "market snapshot hard-fail does not apply because the secondary route is listed-company but the task does not involve company-level market data"), document the inapplicability reason explicitly.
- Do not skip this step because the secondary route is "secondary" — the hard-fail conditions of all declared routes apply equally.

### Step 3: Execution contract

Before deep collection begins, write a compact execution contract that the final artifact must satisfy.

This contract must include at minimum:
- **mandatory sections** — which sections are non-negotiable because the route would fail without them
- **hard-fail conditions** — which route-specific failure patterns must be checked before delivery
- **minimize / move-later items** — which tempting generic sections should be compressed or placed after the primary decision logic

For tasks where the option set is small or obvious (e.g., binary choice), still state the selection boundary explicitly: "only these options are credible because…" rather than leaving it implicit.

The contract belongs in the research plan, not only in the final audit. A route is not fully selected until this contract exists in operational form.

## Common route confusions

### Market entry vs constrained choice
Use market entry when the task is really about whether to enter, when to enter, where to enter first, or how to sequence entry.

Use constrained choice when the task is mainly to choose among defined options with a visible comparison unit and ranking logic.

### First-tier positioning vs listed-company research
Use first-tier positioning when the real question is whether an entity reasonably belongs in a top group.

Use listed-company or investment-style research when the real burden is valuation, public-market judgment, or company-analysis framing.

### Provider selection vs market outlook
Use provider selection when the task is to choose.

Use market outlook when the task is to understand market direction, industry evolution, or future structure rather than select an option.

### Market outlook vs constrained choice
Use market outlook when the task is to understand **direction, evolution, or trajectory** of a market, industry, or category.

Use constrained choice when the task's core output is **ranking, prediction, or selection** among defined options — even if the topic sounds like a market or industry question.

Key test: does the task ask "how will this market evolve?" (market outlook) or "which option will win?" (constrained choice)?

Examples:
- "人形机器人产业链未来 12 个月如何演化" → market outlook (direction/trajectory)
- "哪支球队最可能夺冠" → constrained choice (ranking among defined options)
- "世界杯足球产业链的商业前景" → market outlook (market evolution)
- "AI 编程工具市场中哪家会领先" → constrained choice (selection/prediction)

### Regulatory / policy impact analysis vs market outlook
Use regulatory analysis when the core question is understanding the regulatory environment, assessing policy risk, or judging compliance impact. The report structure is organized around current regulations → business impact → scenarios → implications.

Use market outlook when the focus is market evolution with regulation as one driver among many (technology, demand, competition). The report structure is organized around current state → drivers → scenarios → stakeholder implications.

### Regulatory / policy impact analysis vs listed-company research
Use regulatory analysis when the primary burden is understanding regulatory impact on an industry or business. Company-specific analysis is secondary.

Use listed-company research when the primary burden is investment judgment. Regulation is one section within a broader thesis.

### Academic / literature review vs technical deep-dive
Use academic route when the core question is about understanding research evidence, evaluating research quality, or surveying field progress through academic literature.

Use technical deep-dive when the core question is about how technology works, comparing architectures, or evaluating feasibility — even if academic papers are used as sources.

**Borderline case**: "What are the key papers on Transformer architecture?" — use academic route if the goal is literature survey; use technical deep-dive if the goal is understanding how Transformers work for practical application.

### Academic / literature review vs market outlook
Use academic route when the focus is research progress, breakthroughs, and future directions in academic literature.

Use market outlook when the focus is market evolution, commercial applications, or industry trajectory.

**Borderline case**: "What is the current state of CRISPR research?" — use academic route if analyzing research progress; use market outlook if analyzing commercial applications.

## Minimal internal shape

A compact preflight may use this shape:

- Primary route:
- Closest alternative:
- Why chosen:
- Secondary disciplines:
- Required artifact contract:
- Required audits:

## Common failure modes

Common failures include:

- no route selected explicitly
- multiple routes named, none actually operationalized
- route chosen by topic label rather than decision burden
- route chosen too late, after report shape has already drifted
- route selected, but output still reads like generic overview
- required secondary disciplines named but not actually visible
- wrong route declared for the task type (e.g., Market Outlook used for ranking/prediction tasks; check "Do not use" clauses before committing)

## Scope

This file does not replace `ROUTING-MATRIX.md`.

It exists to make route choice explicit and auditable before a heavier execution layer exists.
