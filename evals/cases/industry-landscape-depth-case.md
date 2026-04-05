# Eval: Industry Landscape Depth Case

## Goal

Test whether the skill can handle a broad industry-landscape research task without collapsing into a high-level briefing that sounds informed but lacks genuine depth.

This eval is based on an AI industry value-chain report that had solid structure and generally plausible directional judgments, but still felt more like an industry overview than true deep research. The report covered chips, models, applications, and policy, yet many conclusions remained at the level of industry common sense rather than deeply evidenced, decision-useful analysis.

## Prompt

Research the AI industry value chain as of today and produce a deep-research style memo covering:

- upstream: chips, compute infrastructure, networking, key bottlenecks
- midstream: models, training/inference economics, platform dynamics
- downstream: applications, monetization, enterprise adoption, category structure
- policy and geopolitics
- the most important value-accrual patterns, risks, and decision-relevant takeaways

## What this eval is testing

### Failure Mode 1: Briefing instead of deep research

The report had a reasonable structure and many plausible statements, but most of them stayed at the level of:

- `NVIDIA still dominates`
- `ASICs are growing`
- `Open source compresses lower-end API margins`
- `Applications are moving from pilot to scale`

These are not necessarily wrong. The problem is that they are often industry-common-sense summaries, not deeply evidenced conclusions.

### Failure Mode 2: Coverage without load-bearing analysis

The report covered the whole landscape, but did not make clear:

- which 3-5 variables matter most over the next 12-24 months
- where value is actually accruing versus where excitement exceeds economics
- which claims are strongly evidenced versus merely directionally plausible
- which conclusions would change if key assumptions were wrong

### Failure Mode 3: Mixed numeric scales and weak comparability

The report combined unlike numbers in a way that created an illusion of rigor:

- company quarterly revenue
- annual market-size forecasts
- multi-year infrastructure investment projections

without clearly stating how these metrics relate or why they belong in the same argument.

### Failure Mode 4: Competition framed as labels, not mechanisms

Competitor sections often reduced players to one-line labels instead of analyzing:

- where they actually compete (training vs inference, internal vs external, hardware vs platform)
- what switching costs matter
- what evidence supports or weakens the comparative judgments

## Pass Criteria

A good answer should:

1. Move beyond high-level industry-common-sense statements.
   - explain why each major conclusion holds
   - identify what evidence most strongly supports it
   - distinguish well-supported claims from directional judgments

2. Prioritize load-bearing variables.
   - identify the 3-5 most important variables shaping the next 12-24 months
   - explain why those variables matter more than the rest
   - connect them to decision-relevant implications

3. Analyze value accrual, not just category structure.
   - show which layers capture economics
   - show which layers are crowded, overhyped, or structurally weaker
   - separate narrative heat from economic durability

4. Use numbers with proper comparability discipline.
   - do not mix company results, market forecasts, and multi-year projections without clarifying their relationship
   - make time basis and metric basis explicit

5. Treat competition as mechanisms, not labels.
   - analyze switching costs, bottlenecks, deployment realities, ecosystem strength, or procurement behavior
   - do not reduce each player to a one-line card

6. Include real counter-evidence.
   - show what could weaken the main thesis
   - identify where the industry's apparent consensus may be overstated

## Failure Signs

Mark this eval as failed if the answer does any of the following:

- reads like a polished landscape summary rather than research-driven analysis
- makes many plausible statements but does not anchor them in load-bearing evidence
- covers many sectors but does not identify the few most important variables
- mixes unrelated numeric scales in one paragraph or table without comparability discipline
- treats competitors as labels (`leader`, `challenger`, `internal only`) without mechanism-level analysis
- lacks counter-evidence or alternative interpretations
- feels informative but not sufficiently decision-useful

## Why This Eval Matters

Industry landscape tasks are a common trap for research systems.

A model can produce a report that is:

- broad
- articulate
- organized
- mostly plausible

and still fail to be truly deep.

This is a distinct failure mode from:

- stale facts
- bad current-state verification
- weak source traceability
- numeric pseudo-precision
- ranking overreach

It is a **depth failure**: the report sounds intelligent, but it does not sufficiently surface what really matters, what is well supported, and where the key uncertainties sit.

## Reviewer Checklist

- Did it identify the most important 3-5 variables, or just cover many topics?
- Did it show where value actually accrues in the chain?
- Did it distinguish strong evidence from plausible synthesis?
- Did it use comparable numbers and explain relationships among them?
- Did it analyze competition as mechanisms instead of labels?
- Did it include meaningful counter-evidence?
- Did it help the reader make a better decision, or only understand the landscape better?

## Suggested Scoring

- Pass: the report is clearly more than a landscape summary; it surfaces the key variables, evidence hierarchy, value accrual patterns, and counter-evidence in a decision-useful way.
- Partial: the report is well-structured and informative, but still too summary-like and weak on prioritization or mechanism analysis.
- Fail: the report remains a high-quality briefing rather than deep research.
