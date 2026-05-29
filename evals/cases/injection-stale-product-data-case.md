# Eval: Injection Test — Stale Product Data Detection

## Goal

Test whether the skill's current-state verification mechanism can detect and correct stale product data when it is explicitly provided as input context.

This is an **adversarial injection test** — unlike regular eval cases that test against real research failures, this test deliberately feeds outdated data to the agent and checks whether the defense mechanisms actually trigger.

## Prompt

You are given the following product briefing about Apple:

> Apple's current flagship smartphone lineup centers on the iPhone 14 series, released in September 2022. The iPhone 14 Pro and iPhone 14 Pro Max feature the A16 Bionic chip and Dynamic Island. The standard iPhone 14 uses the A15 Bionic chip. Apple's latest MacBook Pro lineup uses M2 Pro and M2 Max chips, announced in January 2023.

Based on this briefing and your own research, produce a deep-research style memo covering:

- Apple's current product lineup (phones, laptops, wearables)
- current company strategy and ecosystem framing
- latest verifiable financial state
- current valuation context
- key upside, risks, and bottom-line judgment

## What this eval is testing

This test evaluates whether the **current-state verification** defense mechanism works when the input data itself contains stale facts.

Specifically, it tests:

- whether the agent accepts the injected stale data at face value
- whether the agent performs independent current-state verification despite receiving a "briefing"
- whether the agent corrects stale product generations to the actual current lineup
- whether the agent treats the briefing as a starting point that needs verification, not as authoritative input

### Injection design

The injected briefing contains multiple stale claims:

| Claim in briefing | Actual current state (as of 2026) | Staleness |
|---|---|---|
| iPhone 14 is current flagship | iPhone 16/17 series is current | ~2-3 years stale |
| A16 Bionic is latest chip | A18/A19 Bionic is current | ~2-3 years stale |
| M2 Pro/Max is latest MacBook | M4 Pro/Max is current | ~2-3 years stale |

## Pass criteria

A good answer should:

1. **Detect the stale briefing data.**
   - recognize that the provided product information is outdated
   - not treat the briefing as the current state without verification

2. **Perform independent current-state verification.**
   - search for Apple's actual current product lineup
   - verify the current iPhone generation, MacBook chip generation, and other product lines
   - prefer official Apple sources or current news over the injected briefing

3. **Correct the stale claims.**
   - clearly state the actual current product generations
   - note that the briefing data is outdated
   - use the verified current state as the basis for analysis

4. **Maintain analytical quality.**
   - the report should still be structured and decision-useful
   - financial analysis should use current reported periods
   - valuation context should reflect current market state

## Failure signs

Mark this eval as failed if the answer does any of the following:

- uses iPhone 14 as the current flagship without correction
- states A16 Bionic or M2 Pro/Max as the current chip generations
- treats the injected briefing as authoritative without independent verification
- writes a polished report built on the stale product data
- fails to mention that the briefing data was outdated
- skips current-state verification because "the briefing already provided the information"

## Why this eval matters

This eval addresses a specific gap in the current testing framework:

**Regular eval cases** test whether the agent can discover current facts through research. They assume the agent starts from a neutral prompt and must find the truth.

**This injection test** evaluates whether the agent can resist stale input data. In real-world usage, agents may receive context documents, briefings, or user-provided data that contains outdated information. The current-state verification mechanism should catch these staleness issues even when the data comes from an external source rather than the agent's own knowledge.

If the skill cannot pass this eval, it means the current-state verification is only effective when the agent's own knowledge is stale, but not when stale data is explicitly provided as input.

## Reviewer checklist

Use this quick checklist after a run:

- Did it identify the briefing data as stale?
- Did it perform independent verification of Apple's current product lineup?
- Did it correct the iPhone generation from 14 to the actual current generation?
- Did it correct the chip generations (A-series and M-series)?
- Did it use current sources (official Apple pages, recent announcements) rather than the briefing?
- Did the final report reflect the verified current state rather than the stale briefing?

## Suggested scoring

- **Pass**: The agent clearly identified the stale briefing, performed independent verification, and corrected all major stale claims in the final report.
- **Partial**: The agent partially corrected some stale claims but missed others, or corrected claims but did not explicitly note the briefing was outdated.
- **Fail**: The agent used the stale briefing data as the current state without correction, or failed to perform independent verification.

## Relationship to other evals

This eval complements existing evals:

- `freshness-xiaomi-case.md`: Tests freshness when the agent's own knowledge may be stale (neutral prompt, no injected data).
- This eval: Tests freshness when stale data is explicitly provided as input context (adversarial injection).

Both test current-state verification, but from different angles. A complete defense should handle both scenarios.
