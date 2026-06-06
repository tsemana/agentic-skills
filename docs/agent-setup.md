# Agent Setup Guide

This repository is intentionally simple: each skill is a directory containing a `SKILL.md` file and optional support folders. Any capable agent can use the skills by reading the relevant `SKILL.md` and then loading any referenced files under `references/`, `templates/`, `scripts/`, or `assets/`.

## Repository Contract

Agents should treat the repo as a skill library with this shape:

```text
skills/<Category>/<skill-name>/
├── SKILL.md          # required: primary operating procedure
├── references/       # optional: longer guidance, domain notes, question banks
├── templates/        # optional: reusable starter files
├── scripts/          # optional: helper scripts used by the skill
└── assets/           # optional: images, diagrams, screenshots
```

A skill is ready to use when:

- `SKILL.md` starts with YAML frontmatter at byte 0.
- Frontmatter includes at least `name` and `description`.
- The body explains when to use the skill, how to execute it, pitfalls, and verification checks.
- Any referenced support file exists inside that skill directory.

## Hermes Agent

### Option A: Install from a published GitHub tap

Once the repository is published, add it as a Hermes skills tap:

```bash
hermes skills tap add https://github.com/<owner>/agentic-skills
hermes skills install <skill-id>
hermes skills list
```

Then load a skill explicitly in a session:

```bash
hermes -s genai-platform-eval
# or inside a running session:
/skill genai-platform-eval
```

If the installed skill does not appear immediately, start a fresh session. Hermes skill/tool changes are loaded at session start.

### Option B: Manual local install

Copy the skill directory into the local Hermes skills folder:

```bash
mkdir -p ~/.hermes/skills/Research
mkdir -p ~/.hermes/skills/Dev
cp -R skills/Research/genai-platform-eval ~/.hermes/skills/Research/
cp -R skills/Research/youtube-transcript ~/.hermes/skills/Research/
cp -R skills/Dev/operational-session-closeout ~/.hermes/skills/Dev/
hermes skills list
```

For a named Hermes profile, copy into that profile's skills folder instead:

```bash
mkdir -p ~/.hermes/profiles/<profile>/skills/Research
cp -R skills/Research/<skill-name> ~/.hermes/profiles/<profile>/skills/Research/
```

## Claude / Claude Code

Claude can use these skills without any special package manager.

Recommended approaches:

1. **Project context approach** — clone this repo into the project workspace and tell Claude:

   ```text
   Use the skill at skills/Research/genai-platform-eval/SKILL.md. Read any referenced files under that skill's references/ folder before acting.
   ```

2. **CLAUDE.md approach** — add a short pointer in the consuming project's `CLAUDE.md`:

   ```markdown
   ## Available external skills

   - GenAI platform evaluation: read `<path-to-agentic-skills>/skills/Research/genai-platform-eval/SKILL.md` before evaluating AI platforms. Also read its `references/evaluation-domains.md` and `references/question-bank.md` when doing research or drafting vendor questions.
   - Operational session closeout: read `<path-to-agentic-skills>/skills/Dev/operational-session-closeout/SKILL.md` before wrapping substantial sessions, preparing compaction, or producing handoff notes. Load references only when telemetry implementation details, templates, or examples are needed.
   - YouTube transcript: read `<path-to-agentic-skills>/skills/Research/youtube-transcript/SKILL.md` before extracting YouTube transcripts.
   ```

3. **Copy approach** — copy a skill directory into a project-local `skills/` or `.claude/skills/` folder if the consuming project prefers self-contained context.

For Claude, the critical requirement is not installation mechanics; it is a clear instruction to read `SKILL.md` and referenced support files before executing the task.

## Gemini / Gemini CLI

Gemini agents can also use the repo directly as file context.

Recommended approaches:

1. Clone the repo locally.
2. Include the relevant skill file and references in the prompt or working context.
3. Use a setup instruction like:

```text
Before evaluating a GenAI platform, read:
- skills/Research/genai-platform-eval/SKILL.md
- skills/Research/genai-platform-eval/references/evaluation-domains.md
- skills/Research/genai-platform-eval/references/question-bank.md

Follow the procedure, pitfalls, and verification checklist from the skill.
```

If the Gemini environment supports project instructions, add the same pointer there. If it supports file attachment or context inclusion, attach the relevant `SKILL.md` and referenced files.

## Agent Consumption Rules

For any agent family:

1. Select the skill by `name` and `description` in the frontmatter.
2. Read the entire `SKILL.md` before acting.
3. Read referenced support files when the skill tells you to.
4. Use scripts only after inspecting what they do and confirming prerequisites.
5. Do not assume local secrets, credentials, or paths exist unless the skill documents setup steps.
6. Run the skill's verification checklist before reporting completion.

## Validating the Repository

Run:

```bash
python3 scripts/validate_skills.py
```

The validator checks frontmatter, naming, supported directory structure, required/recommended sections, and basic secret patterns.
