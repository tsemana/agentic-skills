# Harness Adapters

These adapters map the portable telemetry markers in `operational-session-closeout` to common agent runtimes. The markers remain stable even when the telemetry source changes.

## Hermes Adapter

If running in Hermes:

- Use `session_usage` for callable usage telemetry when available.
- Map `session_usage` snapshots to `[TEL-0]`, `[TEL-1]`, `[TEL-2]`, and `[TEL-3]`.
- For `[TEL-4]`, subtract earlier snapshots from later snapshots when possible and combine with operational state.
- Use `todo` for current session task state when useful.
- Use `session_search` only when prior-session recall is needed.
- Use Obsidian tools only when durable task/note updates are required by user instruction or standing workflow.
- For code work, load and follow `requesting-code-review` before final signoff.

| Marker | Hermes source |
|---|---|
| `[TEL-0]` | `session_usage` at session start, if available |
| `[TEL-1]` | `session_usage` before execution |
| `[TEL-2]` | `session_usage` after verification |
| `[TEL-3]` | `session_usage` immediately before closeout |
| `[TEL-4]` | Delta between stored `session_usage` snapshots plus operational state |

Fallbacks:

1. If `session_usage` exists, use it.
2. If `session_usage` does not exist but `/usage` output is already available, use the provided `/usage` data.
3. Do not ask the user to manually run `/usage` unless telemetry is central to the request and no callable source exists.
4. If no source exists, preserve the marker and write `unavailable`.

## Claude Code / Claude-Style Harness Adapter

If running in Claude Code or a Claude-style coding harness:

- Use any built-in usage display, transcript metadata, or provider usage exposed by the harness.
- If no callable telemetry exists, do not interrupt closeout to ask for usage unless the user explicitly requested cost/token accounting.
- Use git status/diff and test outputs for artifact and verification state.
- Use project instructions such as `CLAUDE.md` for local closeout conventions.
- Preserve all telemetry markers even if unavailable.

| Marker | Possible source |
|---|---|
| `[TEL-0]` | Harness session metadata, if exposed |
| `[TEL-1]` | Usage metadata before edits/tool execution, if exposed |
| `[TEL-2]` | Usage metadata after tests/review, if exposed |
| `[TEL-3]` | Final usage metadata or unavailable |
| `[TEL-4]` | Operational delta from files/tests/tasks plus any available usage |

## OpenAI Codex / API Harness Adapter

If running in an OpenAI API-based harness:

- Use provider response `usage` objects when exposed.
- Aggregate usage across model calls if the harness provides per-call metadata.
- Include reasoning tokens if available.
- Include cached tokens if available.
- If tool-call counts are tracked separately from model usage, report both.

| Marker | Possible source |
|---|---|
| `[TEL-0]` | Initial aggregate usage counter |
| `[TEL-1]` | Aggregate usage before side effects |
| `[TEL-2]` | Aggregate usage after verification |
| `[TEL-3]` | Final aggregate usage |
| `[TEL-4]` | Aggregate delta plus artifacts and verification |

## Cursor / IDE Agent Adapter

If running in an IDE agent harness:

- Use workspace diff and diagnostics for artifact/verification state.
- Use any IDE agent usage/cost panel if programmatically available.
- Do not scrape UI panels unless explicitly allowed.
- Preserve markers with `unavailable` when telemetry is not exposed.

## Generic Harness Adapter

At each telemetry marker:

1. Check for a callable usage API.
2. Check for provider response usage metadata.
3. Check for tracing/logging span metadata.
4. Check for runtime counters such as tool calls or elapsed time.
5. Check whether context window usage is exposed.
6. If none are available, mark telemetry unavailable.

Never fabricate token counts, costs, or context usage.

Generic mapping:

```text
runtime telemetry available -> use it
provider usage available -> aggregate it
trace/log metadata available -> summarize it
only operational state available -> report operational state, telemetry unavailable
nothing available -> preserve marker, write unavailable
```
