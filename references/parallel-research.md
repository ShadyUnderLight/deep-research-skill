# Parallel Research

Use parallel research only when the topic naturally separates into mostly independent tracks.

## Good candidates

Parallelize when the task has 2-4 distinct tracks such as:

- company / product / market
- competitors / pricing / differentiation
- technical feasibility / implementation risk / compliance risk
- current status / historical context / forward-looking signals

Good parallel tracks should have:

- different source pools
- limited overlap
- a clear question for each track
- a clear merge point at the end

## Do not parallelize when

Avoid sub-agents when:

- the topic is narrow and linear
- the answer depends on one source chain
- the task is simple enough for one agent pass
- the overhead of coordination will exceed the research benefit

As a rule of thumb, do not parallelize a `briefing` unless the user explicitly asks for breadth.

## Track design

Define each track with:

- track name
- exact question
- preferred source types
- required outputs

Example:

- **Track: competitors**
  - Question: Who are the closest alternatives and how do they differ?
  - Preferred sources: official sites, pricing pages, comparison writeups
  - Required outputs: top competitors, differences, confidence notes, sources

## Sub-agent prompt shape

When spawning sub-agents, give each one:

1. the overall research goal
2. the specific track question
3. the preferred source types
4. the research mode
5. an instruction to return structured findings only
6. an instruction to separate confirmed facts from inference
7. an instruction to include source URLs

Keep sub-agent tasks narrow. Narrow tasks merge better.

## Expected sub-agent output

Ask each sub-agent to return:

- track summary
- key findings
- uncertainties or conflicts
- source list

If the topic is decision-oriented, also ask for:

- implications for the overall question

## Merge step

After sub-agents finish:

1. compare overlapping claims
2. resolve conflicts using stronger or more primary sources
3. note unresolved conflicts explicitly
4. remove duplicate evidence
5. synthesize one coherent report

Do not paste sub-agent outputs together without reconciliation.

## Batch parallelism (rate-limit safe)

To avoid triggering API rate limits when multiple tracks run simultaneously, use **batch parallelism** instead of full parallelism.

**Rule: run at most 2 tracks concurrently. Wait for both to finish before starting the next batch.**

If you have 4 tracks:
1. Spawn Track A + Track B in parallel → wait for both results
2. Spawn Track C + Track D in parallel → wait for both results
3. Merge all four results

If you have 3 tracks:
1. Spawn Track A + Track B in parallel → wait
2. Spawn Track C alone → wait
3. Merge all three

If you have 1 track: run it normally, no parallelism needed.

**Why 2:** Running 2 concurrent tracks is a conservative operational default that avoids rate-limit pressure in most environments. If the API clearly tolerates more in practice, you can adjust up—but default to safe.

**Spawning within a batch:** Use `sessions_spawn` for all tracks in the current batch simultaneously. The batch wait is handled by collecting their results before the next spawn call.

**Jitter (optional):** If you observe borderline rate-limit behavior, add a small random delay (0.5–1s) between spawning tracks within the same batch.

## Quality guardrails

During parallel runs:

- keep the number of tracks small
- prefer 2-3 strong tracks over 5 weak ones
- keep one synthesis pass at the end
- avoid recursive sub-agent spawning unless clearly justified
- stop parallel work once evidence saturates
- **never spawn all tracks at once** — always batch
