# Agentic Skills

Reusable agentic skills for AI agents.

This repository is organized as a small, publishable skill library. Each skill is a class-level workflow package with a rich `SKILL.md` and optional supporting files.

## Skill catalog

| Skill | Category | Purpose |
|---|---|---|
| `genai-platform-eval` | `Research` | Evaluate GenAI platforms, services, orchestration layers, and agent frameworks for adoption. |
| `story-map` | `Dev/CLAUDE` | Facilitate Three Amigos story mapping sessions with a PO/Dev/QA agent team that debates via messaging and builds a master story map incrementally. Requires Claude Code agent teams. |
| `youtube-transcript` | `Research` | Extract verbatim transcripts from public YouTube videos and Shorts using Gemini. |

## Repository structure

```text
skills/
├── <category>/            # categories may nest, e.g. Dev/CLAUDE/
│   └── <skill-name>/
│       ├── SKILL.md
│       ├── references/  # optional: long-form notes, examples, session-specific detail
│       ├── templates/   # optional: reusable starter files
│       ├── scripts/     # optional: deterministic helper scripts
│       └── assets/      # optional: images, diagrams, screenshots
├── scripts/
│   └── validate_skills.py
└── .github/workflows/
    └── validate-skills.yml
```

Skills that target a specific agent runtime live under a runtime subcategory (e.g. `skills/Dev/CLAUDE/` for skills that require Claude Code-specific tools such as agent teams). Each such skill must state its runtime requirements in a `## Requirements` section.

## Skill standard

Each skill should be a reusable class-level workflow, not a one-session note.

Minimum requirements:

- One `SKILL.md` per skill directory.
- YAML frontmatter starts at byte 0 with `---`.
- Frontmatter includes `name` and `description`.
- `description` is no more than 1024 characters.
- Body content is non-empty.
- Skill names are lowercase, hyphenated, and stable.
- Supporting details that are too long for `SKILL.md` belong in `references/`.

Recommended frontmatter:

```yaml
---
name: my-skill
description: Use when an agent needs to perform a reusable class of work. Provides a practical operating procedure, pitfalls, and verification steps.
version: 1.0.0
author: Tony Semana
license: MIT
metadata:
  hermes:
    tags: [agentic-ai, skills]
    related_skills: []
---
```

Runtime-specific skills (anything that cannot run on a generic agent) should declare the runtime instead of the `hermes` namespace, so they are not indexed as Hermes-installable:

```yaml
metadata:
  runtime: claude-code
  tags: [agent-teams]
  related_skills: []
```

Recommended body sections:

```markdown
# Skill Title

## Overview

## When to Use

## Procedure

## Common Pitfalls

## Verification Checklist
```

## Validate locally

```bash
python3 scripts/validate_skills.py
```

## Installation / use

See [`docs/agent-setup.md`](docs/agent-setup.md) for Hermes, Claude / Claude Code, Gemini, and generic agent consumption patterns.

For Hermes Agent, add this repository as a skills tap once it is published:

```bash
hermes skills tap add https://github.com/<owner>/agentic-skills
hermes skills install <skill-id>
```

For local/manual Hermes use, copy a skill directory into:

```bash
~/.hermes/skills/<category>/<skill-name>/
```

For Claude, Gemini, or other agents, clone the repo and point the agent at the relevant `skills/<category>/<skill-name>/SKILL.md` plus any referenced files under that skill's `references/` directory.

## License

MIT unless otherwise noted in an individual skill.
