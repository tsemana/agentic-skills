# Skills

Reusable agentic skills for AI agents.

This repository is organized as a small, publishable skill library. Each skill is a class-level workflow package with a rich `SKILL.md` and optional supporting files.

## Repository structure

```text
skills/
├── <category>/
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

For Hermes Agent, add this repository as a skills tap once it is published:

```bash
hermes skills tap add https://github.com/<owner>/skills
hermes skills install <skill-id>
```

For local/manual use, copy a skill directory into:

```bash
~/.hermes/skills/<category>/<skill-name>/
```

## License

MIT unless otherwise noted in an individual skill.
