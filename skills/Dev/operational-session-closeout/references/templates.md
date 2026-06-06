# Closeout Templates

Use these templates when the compact version in `SKILL.md` is not enough.

## Standard Closeout Template

```markdown
# Session Closeout

## Objective
- Primary:
- Secondary:

## Outcome
- Status: Completed / Partially completed / Blocked
- Summary:

## Work Completed
- ...

## Artifacts Changed
- Files:
- Notes:
- Tasks:
- External systems:
- Other:

## Verification
- Tests:
- Static checks:
- Review:
- Manual checks:
- Not run:

### [TEL-2] Verification Telemetry
- Source:
- Verification tool/API calls:
- Verification token delta:
- Verification cost delta:
- Verification elapsed time:
- Confidence gained:
- Notes:

## Open Loops
- ...

## Risks / Caveats
- ...

## [TEL-3] Closeout Telemetry
- Source:
- Model/provider:
- API calls:
- Tool calls:
- Input tokens:
- Output tokens:
- Cache read/write tokens:
- Reasoning tokens:
- Total tokens:
- Context usage:
- Estimated cost:
- Elapsed time:

## [TEL-4] Handoff Delta
- Work completed:
- Files/artifacts changed:
- Verification completed:
- Additional API/tool calls:
- Token/cost impact:
- Context pressure:
- Remaining risk:
- Recommended next action:

## Next Actions
1. ...
2. ...
3. ...
```

## Compact Closeout Template

```markdown
## Closeout

**Outcome**
- ...

**Completed**
- ...

**Verified**
- ...

**Open**
- ...

**[TEL-3] Telemetry**
- Source:
- Model/provider:
- API/tool calls:
- Tokens/cost:
- Context:

**Next**
1. ...
2. ...
3. ...
```

## Context Compaction Template

```markdown
# Context Handoff

## Active Task
- ...

## Goal
- ...

## Constraints
- ...

## Completed Actions
- ...

## Current State
- ...

## Files / Artifacts
- ...

## Verification
- ...

## Decisions Made
- ...

## Resolved Questions
- ...

## Pending User Asks
- ...

## Open Loops / Blockers
- ...

## [TEL-4] Handoff Delta
- Work completed since previous checkpoint:
- Verification completed:
- Tool/API-call delta:
- Token/cost delta:
- Context pressure:
- Remaining risk:

## Critical Context
- ...

## Recommended Resume Point
- ...
```
