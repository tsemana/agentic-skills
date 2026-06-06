# Delta Calculation

Use deltas to explain where effort went. Total usage is useful, but phase deltas are more operationally meaningful.

## Basic Formula

When two telemetry snapshots are available, compute field-by-field deltas:

```yaml
delta:
  api_calls: later.api_calls - earlier.api_calls
  tool_calls: later.tool_calls - earlier.tool_calls
  input_tokens: later.tokens.input - earlier.tokens.input
  output_tokens: later.tokens.output - earlier.tokens.output
  cache_read_tokens: later.tokens.cache_read - earlier.tokens.cache_read
  cache_write_tokens: later.tokens.cache_write - earlier.tokens.cache_write
  reasoning_tokens: later.tokens.reasoning - earlier.tokens.reasoning
  estimated_cost_usd: later.cost.estimated_usd - earlier.cost.estimated_usd
```

## Useful Deltas

| Delta | Formula | Meaning |
|---|---|---|
| Planning/research cost | `[TEL-1] - [TEL-0]` | Cost before side effects |
| Execution + verification cost | `[TEL-2] - [TEL-1]` | Cost to act and prove the work |
| Closeout cost | `[TEL-3] - [TEL-2]` | Cost after verification, usually reporting/state gathering |
| Whole-session cost | `[TEL-3] - [TEL-0]` | Total cost since baseline |
| Handoff delta | latest checkpoint - prior checkpoint | What changed since last handoff/compaction |

## Rules

- If either side is unavailable, mark the delta unavailable.
- If counters reset between snapshots, do not subtract; report both snapshots.
- If costs are estimates, label them as estimates.
- If costs come from different sources, do not combine them without noting source mismatch.
- If provider billing data differs from local estimates, prefer provider billing data and note the source.
- If child/subagent telemetry is separate from parent telemetry, do not silently merge them. Report separately or label the aggregation.

## Interpretation Guidance

Good interpretations:

- “Verification added 3 tool calls and caught no regressions.”
- “Most cost was in investigation before edits.”
- “Context is near limit; compaction is recommended.”
- “No telemetry source was available, but verification evidence is complete.”

Poor interpretations:

- “High token count means poor work.”
- “Low token count means high quality.”
- “Cost is exact” when it is only estimated.
- “Telemetry unavailable” as a reason to skip closeout.
