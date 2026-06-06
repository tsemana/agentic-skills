# Raw Usage Accounting Hardening

Use this reference when implementing or verifying usage telemetry before richer closeout markers/events. The core priority is: reliable raw usage first, lifecycle markers second.

## Priority Order

1. Capture raw usage counters reliably after every successful model call.
2. Expose a callable usage snapshot (`session_usage` or equivalent).
3. Ensure user-facing usage surfaces (`/usage`, dashboards, closeout tools) prefer the same accumulated counters.
4. Add lifecycle baselines/snapshots (`[TEL-0]` through `[TEL-3]`).
5. Add compact significant-event logging only after accounting is trustworthy.

## Counters to Normalize

Normalize provider usage into these buckets:

- input tokens, excluding cache read/write where provider totals include cache
- output tokens
- cache read tokens
- cache write tokens
- reasoning tokens, when provider exposes them
- API/model call count
- estimated cost
- cost status/source
- model/provider/base URL
- context usage, if available
- elapsed time, if available

Never reconstruct token usage from transcript text when provider/runtime counters are available. Transcript estimates are a fallback only.

## Provider Shape Checks

Test normalizers against at least these shapes:

### Anthropic Messages

```python
input_tokens
output_tokens
cache_read_input_tokens
cache_creation_input_tokens
```

### OpenAI Chat Completions

```python
prompt_tokens
completion_tokens
prompt_tokens_details.cached_tokens
prompt_tokens_details.cache_write_tokens  # when present via compatible gateways
completion_tokens_details.reasoning_tokens
```

Some OpenAI-compatible proxies route Anthropic models and expose Anthropic-style cache fields at top level. Fallback to:

```python
cache_read_input_tokens
cache_creation_input_tokens
```

### OpenAI Responses / Codex-style

```python
input_tokens
output_tokens
input_tokens_details.cached_tokens
input_tokens_details.cache_creation_tokens
output_tokens_details.reasoning_tokens
```

## Cost Parity Rule

When both per-call accumulated session cost and recomputed aggregate cost are available, user-facing usage should prefer the accumulated session cost.

Reason: accumulated cost is computed at the time each provider response is normalized, preserving provider route, pricing source, request-count pricing, included/subscription status, and cache/reasoning details. Recomputing from aggregate counters can drift.

Fallback recomputation should include request count:

```python
CanonicalUsage(..., request_count=session_api_calls or 1)
```

## Tests to Add

For any usage-accounting change, add focused tests for:

- each provider response shape touched
- reasoning token extraction from both `completion_tokens_details` and `output_tokens_details`
- cache read/write subtraction from prompt/input totals where applicable
- accumulated session cost preferred over recomputed cost in user-facing `/usage`-style output
- callable snapshot parity with other usage surfaces

## Verification Pattern

Run a focused suite covering:

```text
tests/agent/test_usage_pricing.py
tests/tools/test_session_usage_tool.py
tests/gateway/test_usage_command.py
tests/run_agent/test_context_token_tracking.py
```

Also run compile checks for changed source/test files.

## Pitfalls

- Do not build marker/event features on top of unverified raw counters.
- Do not let `/usage` and callable usage tools compute cost from different sources without an explicit reason.
- Do not count cache tokens twice: understand whether provider totals include cached tokens.
- Do not drop reasoning tokens because providers use different detail-field names.
- Do not inject raw event logs or usage snapshots into every model prompt; keep them in runtime state and read them only when needed.
