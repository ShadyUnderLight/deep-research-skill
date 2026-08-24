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
5. an instruction to return a Track Handoff (see below), not polished prose
6. an instruction to record confirmed facts vs inference via `evidence_role`
7. an instruction to put every used source into `source_register` with URLs

Keep sub-agent tasks narrow. Narrow tasks merge better.

## Track Handoff contract (required when parallelizing)

Each track does not return a free-form report. It returns one **Track Handoff** —
a schema-valid JSON artifact defined by `schemas/track-handoff.json`
(schema version `1`).

The canonical field vocabulary lives in the schema; do not redefine it here.
Minimum shape every track must produce:

- `schema_version`, `handoff_id`, `track_id`, `question`
- `scope` with explicit `in_scope`, `out_of_scope`, `timeframe`, `geography`
  so the parent can detect scope drift between tracks
- `source_register` — the sources this track actually used, each with a stable
  local `source_id`
- `findings[]` — load-bearing claims; each carries a stable `finding_id`,
  non-empty `evidence_refs` resolving into this handoff's `source_register`,
  an `evidence_role` (`observed | primary | secondary | inferred | unknown`),
  and a numeric `confidence`
- `conflicts[]` — disagreements between claims, bound to the involved
  `finding_refs`, with a resolution status
- `unknowns[]` — each with reason, impact, and next verification action
- `implications[]` for decision-oriented topics
- `status`: `complete | partial | blocked`; `partial` requires
  `status_reason`, `blocked` requires `status_reason` plus `recovery_action`

### Producer rules (the track)

1. Validate before handing off:

   ```bash
   python3 scripts/validate_track_handoff.py <handoff>.json
   ```

2. A track whose handoff fails validation is not complete — fix or mark it
   `partial`/`blocked` with reasons. Never downgrade a validation failure to
   an empty array.

### Consumer rules (the parent)

1. Re-validate every incoming handoff before merging (same validator).
2. A handoff that fails validation is reported as `HANDOFF_INCOMPLETE`.
   Refuse to merge it and **never interpret it as "no evidence for this
   direction"** — a missing or malformed handoff is not a finding.
3. Do not auto-fill missing claims, sources, conflicts, or unknowns; ask the
   track to re-run instead.
4. Preserve each track's `partial` / `blocked` / unknown states in the merged
   Research Pack's uncertainty and counter-evidence registers.
5. When dispatching, pass `--expected-track-id <id>` so a stale or misrouted
   handoff cannot be merged under the wrong track.

## Merge step

After all tracks return valid handoffs:

1. compare overlapping claims
2. resolve conflicts using stronger or more primary sources
3. note unresolved conflicts explicitly
4. remove duplicate evidence
5. synthesize one coherent report

Do not paste sub-agent outputs together without reconciliation. Do not merge
any track whose handoff did not pass validation (see consumer rules above).

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

**Spawning within a batch:** Use your environment's parallel-agent spawn capability for all tracks in the current batch simultaneously. The batch wait is handled by collecting their results before the next spawn call.

**Jitter (optional):** If you observe borderline rate-limit behavior, add a small random delay (0.5–1s) between spawning tracks within the same batch.

## Quality guardrails

During parallel runs:

- keep the number of tracks small
- prefer 2-3 strong tracks over 5 weak ones
- keep one synthesis pass at the end
- avoid recursive sub-agent spawning unless clearly justified
- stop parallel work once evidence saturates
- **never spawn all tracks at once** — always batch
