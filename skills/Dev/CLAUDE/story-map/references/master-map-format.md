# Master Map Format and Update Rules

Used in Step 6 of the procedure. One master map file per product, written to `story-maps/{product-name}.md` in the project directory. Product sessions create the file; Activity, Persona, and Feature sessions load it, update only their scoped sections, and write it back following the update rules at the bottom of this file.

---

## Master Map Template

```markdown
# Story Map: [Product Name]

**Last updated:** [date]
**Sessions log:**
- [date] — [session type]: [description of what was mapped]

---

## Personas

| Persona | Goal | Notes |
|---|---|---|
| [name] | [goal] | Primary / Secondary / Added [date] |

---

## Backbone

| | [Activity 1] | [Activity 2] | [Activity 3] | [Activity 4] |
|---|---|---|---|---|
| **Tasks** | Task A | Task D | Task G | Task J |
| | Task B | Task E | Task H | Task K |
| | Task C | Task F | Task I | Task L |

**Mapping status:**
| Activity | Status | Session date |
|---|---|---|
| [Activity 1] | Complete | [date] |
| [Activity 2] | Pending | — |

---

## Activity: [Activity 1 Name]

*Mapped: [date] | Session type: [type]*

### Task A — [task name]

| Story | Persona | Release | Definition of Done | BDD Status |
|---|---|---|---|---|
| As a [persona], I need to... | [persona] | Release 1 | [agreed DoD] | Ready / Pending |

### Task B — [task name]

[same format]

---

## Walking Skeleton

**Goal:** [technical validation goal]
**Path:** [list of tasks forming the thinnest end-to-end path]

---

## Release Slices

### Release 1 — [outcome-based goal]
**Goal:** [what a user can accomplish end-to-end]

| Story | Activity | Task | DoD | Acceptance Criteria | Confidence |
|---|---|---|---|---|---|
| [story] | | | [agreed] | [from QA] | Pass / Fail |

**Confidence test:**
- [ ] Can a real user accomplish this goal using only what is in this slice?
- [ ] Does the slice have a clear, testable outcome?
- [ ] Is every story necessary (no gold-plating)?
- [ ] Is everything necessary included (no hidden dependencies)?

### Release 2 — [outcome-based goal]
[same format]

### Backlog
[stories deferred beyond current slices]

---

## Risk & Gap Register

| Item | Type | Severity | Recommended Action | Status |
|---|---|---|---|---|
| [item] | Gap / Tech Risk / Scope Risk / Spike Needed | High / Med / Low | [action] | Open / Resolved |

---

## BDD Readiness

| Story | Activity | Task | Verdict | Rules for Example Mapping | Session |
|---|---|---|---|---|---|
| [story] | | | READY / NEEDS REFINEMENT / SPLIT / SPIKE | [rules] | [date] |

**Ready for Example Mapping:**
- [story]

**Needs refinement:**
- [story]: [gap]
```

---

## Update Rules for Additive Sessions

When updating an existing master map:

- **Sessions log**: append — never remove previous entries
- **Backbone table**: only modify if user approved a backbone change at checkpoint
- **Mapping status table**: update the row for the current activity; do not touch others
- **Activity sections**: add or update the scoped section; do not touch other activities
- **Personas table**: append new rows; do not modify existing ones
- **Release Slices**: add or update stories within relevant releases; preserve previous sessions' stories
- **Risk & Gap Register**: append new rows; update Status of resolved items only
- **BDD Readiness**: append new rows; do not modify rows from previous sessions
