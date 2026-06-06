# Examples

## Example: Code Session Closeout

```markdown
# Session Closeout

## Objective
- Add programmatic session telemetry to support closeout without manual `/usage` copy/paste.

## Outcome
- Status: Completed
- Summary: Implemented a callable session usage tool and wired it into the agent loop/toolset path.

## Work Completed
- Created `tools/session_usage_tool.py`.
- Wired direct agent dispatch.
- Registered the tool in relevant toolsets.
- Added focused tests.

## Artifacts Changed
- Files:
  - `tools/session_usage_tool.py` — created
  - `tests/tools/test_session_usage_tool.py` — created
  - `agent/tool_executor.py` — modified
  - `agent/agent_runtime_helpers.py` — modified
  - `model_tools.py` — modified
  - `toolsets.py` — modified

## Verification
- Tests: focused pytest suite passed.
- Static checks: compileall passed.
- Security scan: no added-line findings.
- Review: independent reviewer passed.
- Not run: full repository regression.

### [TEL-2] Verification Telemetry
- Source: session_usage
- Verification tool/API calls: unavailable
- Verification token delta: unavailable
- Verification cost delta: unavailable
- Confidence gained: focused feature path verified
- Notes: Full regression still pending.

## Open Loops
- Optional: add sequential execution-path integration test.
- Optional: run full regression before merge.

## Risks / Caveats
- Full repository regression was not run.
- Tool must be validated in a fresh runtime where the updated tool surface is loaded.

## [TEL-3] Closeout Telemetry
- Source: session_usage
- Model/provider: unavailable
- API calls: unavailable
- Tool calls: unavailable
- Tokens: unavailable
- Context usage: unavailable
- Estimated cost: unavailable
- Elapsed time: unavailable

## [TEL-4] Handoff Delta
- Work completed: implementation plus focused verification.
- Files/artifacts changed: listed above.
- Verification completed: focused tests, compile check, security scan, independent review.
- Additional API/tool calls: unavailable.
- Token/cost impact: unavailable.
- Context pressure: unavailable.
- Remaining risk: full regression pending.
- Recommended next action: run full regression or commit focused feature.

## Next Actions
1. Add optional sequential integration test if desired.
2. Run full regression if preparing for broad merge.
3. Commit the focused feature.
```

## Example: Harness Without Telemetry

```markdown
## [TEL-3] Closeout Telemetry
- Source: unavailable
- Reason: current harness does not expose callable usage, provider usage metadata, or context-window counters
```

## Correct vs Incorrect Marker Handling

Correct:

```markdown
## [TEL-3] Closeout Telemetry
- Source: unavailable
- Reason: this harness does not expose usage metadata
```

Incorrect:

```markdown
## Telemetry
- omitted
```

Correct:

```markdown
### [TEL-2] Verification Telemetry
- Source: provider usage metadata
- Verification token delta: unavailable
- Verification elapsed time: 84s
```

Incorrect:

```markdown
### Verification Telemetry
- Cost was probably low
```
