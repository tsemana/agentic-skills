# Telemetry Contract

A harness that wants first-class support for `operational-session-closeout` should expose one callable or inspectable usage object. The shape below is recommended, not mandatory. Use the closest available equivalent and mark missing fields as `unavailable`.

## Telemetry Types

```yaml
telemetry_types:
  usage:
    description: Token, API-call, model-call, and cost data.
  context:
    description: Context window size, amount used, amount remaining, and compaction pressure.
  time:
    description: Wall-clock time, active execution time, or phase elapsed time.
  tools:
    description: Tool calls by category, status, and result.
  verification:
    description: Tests, checks, reviews, scans, and their outcomes.
  artifacts:
    description: Files, notes, tasks, URLs, messages, tickets, or records changed.
```

## Recommended Portable Shape

```json
{
  "source": "hermes.session_usage | runtime.usage | provider.usage | trace.span | manual | unavailable",
  "timestamp": "ISO-8601",
  "session_id": "optional",
  "turn_id": "optional",
  "model": "string",
  "provider": "string",
  "api_calls": 0,
  "tool_calls": 0,
  "tokens": {
    "input": 0,
    "output": 0,
    "cache_read": 0,
    "cache_write": 0,
    "reasoning": 0,
    "total": 0
  },
  "cost": {
    "estimated_usd": 0.0,
    "source": "provider | local_estimate | billing_api | unavailable"
  },
  "context": {
    "window": 0,
    "used": 0,
    "remaining": 0,
    "percent_used": 0.0
  },
  "elapsed": {
    "wall_seconds": 0,
    "active_seconds": 0
  },
  "tools": {
    "total": 0,
    "by_name": {},
    "failures": 0
  }
}
```

## Field Rules

- If a field is missing, write `unavailable`.
- Do not estimate unless the source and method are explicit.
- If cost data is estimated, label it as estimated.
- If billing data and local estimate differ, prefer billing data and name the source.
- If counters reset between snapshots, report both snapshots rather than subtracting.
- If parent and child/subagent telemetry are separate, report them separately.

## Minimal Useful Contract

A harness can still support the skill with only:

```json
{
  "source": "runtime.usage",
  "model": "string",
  "api_calls": 0,
  "tool_calls": 0,
  "tokens": "unavailable",
  "cost": "unavailable",
  "context": "unavailable"
}
```

The important requirement is that the source and unavailable fields are explicit.
