# Runtime Telemetry Initialization

This reference describes how a harness initializes telemetry so closeout can report opening costs, phase deltas, and significant events without relying on transcript reconstruction.

## Design Principle

Telemetry should be captured by the runtime as the session runs. The closeout skill should read already-maintained state.

Do not wait until closeout to infer usage, opening cost, or significant events from the conversation transcript.

## Implementation Priority

If implementation capacity is limited, prioritize in this order:

1. **Robust raw usage accounting** — tokens in/out, cache/reasoning tokens where available, API/model calls, model/provider, elapsed time, context usage, and estimated cost.
2. **Agent-callable usage snapshot** — a low-friction tool/API that returns the current counters for closeout.
3. **Session-start baseline** — automatic `[TEL-0]` snapshot at agent/session creation.
4. **Named phase snapshots** — `[TEL-1]`, `[TEL-2]`, and `[TEL-3]` capture helpers.
5. **Significant event log** — compact metadata for work milestones, side effects, verification, subagents, and handoff.

Markers make usage interpretable, but they do not replace accurate usage accounting.

## Minimal Runtime State

```python
session_telemetry = {
    "started_at": iso_timestamp,
    "snapshots": {
        "TEL-0": usage_snapshot_at_session_start,
        "TEL-1": None,
        "TEL-2": None,
        "TEL-3": None,
    },
    "events": [],
    "counters": {
        "api_calls": 0,
        "tool_calls": 0,
        "tokens": {},
        "cost": {},
        "context": {},
    },
}
```

## Initialization Points

### Session/Agent Creation

Initialize:

- session start timestamp
- zeroed cumulative counters
- empty event list
- `[TEL-0]` snapshot if model/context metadata is available

In Hermes today, cumulative counters are initialized on the agent object during agent construction. This is enough for total closeout telemetry, but richer marker support needs named snapshots/events.

### Each Model Call

Update counters from provider usage metadata:

- API call count
- input/output/cache/reasoning tokens
- estimated cost if available
- context usage if available
- model/provider if changed by fallback routing

This is O(1) per model call and should be effectively negligible compared with the model call itself.

### Each Tool Call

Update:

- total tool call count
- count by tool name/category
- failure count
- significant event if the tool causes side effects or verification

Do not store full tool output by default. Store compact metadata: tool name, status, path/URL/ID if relevant, timestamp, and optional short label.

### Significant Events

Append an event for:

- objective accepted
- plan approved
- `[TEL-1]` pre-execution baseline captured
- first write/side effect
- subagent dispatch and return
- test/check/review starts and completes
- `[TEL-2]` verification snapshot captured
- context compaction/handoff preparation
- closeout requested and `[TEL-3]` captured

Suggested event shape:

```json
{
  "ts": "ISO-8601",
  "type": "objective | side_effect | verification | subagent | compaction | closeout | telemetry_marker",
  "marker": "TEL-1",
  "label": "focused tests passed",
  "tool": "terminal",
  "status": "ok | failed | skipped",
  "handle": "path/url/id if useful",
  "snapshot_ref": "TEL-2"
}
```

## Resource Budget

### Runtime CPU / Memory

Expected overhead is negligible when implemented as in-memory counters and compact events:

- model-call accounting: integer additions and one cost-estimation function
- tool-call accounting: one small event/count update per tool call
- marker snapshots: shallow dict copies of the current usage snapshot

Target budget:

- under 50 significant events per normal session
- under 200 significant events for long/debug sessions
- event object usually under 300 bytes if labels stay short
- do not store raw prompts, completions, or tool outputs in the telemetry event log

### Token Budget

Telemetry should not consume prompt tokens during normal execution if it stays in runtime state.

Token cost appears only when:

- a skill is loaded
- telemetry is requested by the model via a tool
- the closeout includes telemetry text

Current `operational-session-closeout` core skill is about 2.25k tokens. Reference files are loaded only on demand.

### Storage Budget

If persisted, use compact JSON and retention limits. For durable session history, store aggregate counters and compact events, not full trace payloads.

## Hermes Current State vs Target

Current Hermes state after the `session_usage` implementation:

- cumulative counters initialized at agent creation
- counters updated after each model call
- cost accumulator updated after each model call
- session DB token counts updated after each model call when available
- `session_usage` exposes a live closeout snapshot

Remaining target work for full marker support:

- automatic `[TEL-0]` named snapshot at session start
- event log for significant side effects/checks/subagents/compaction
- helper to capture named snapshots `[TEL-1]`, `[TEL-2]`, `[TEL-3]`
- closeout adapter that returns snapshots and event summary, not only total usage

## Recommended API Surface

A portable harness can expose:

```text
telemetry.snapshot(marker: "TEL-0" | "TEL-1" | "TEL-2" | "TEL-3", label?: string)
telemetry.event(type, label, metadata?)
telemetry.usage()
telemetry.closeout_summary()
```

Hermes could implement this as an extension of `session_usage`, or as a sibling `session_telemetry` tool if event history grows beyond simple usage counters.
