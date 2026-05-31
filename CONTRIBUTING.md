# Contributing

This repo publishes reusable, class-level agentic skills.

## Skill criteria

A skill should:

- Capture a repeatable class of work.
- Include enough procedure for an agent to execute without extra context.
- Include pitfalls and verification steps.
- Keep session-specific detail in `references/` rather than bloating `SKILL.md`.
- Avoid private, proprietary, credentialed, or personal data.

Avoid:

- One-off incident notes.
- Raw transcripts or session logs.
- API keys, OAuth tokens, internal URLs, or unredacted customer/company data.
- Skills that duplicate an existing class-level skill.

## Validation

Run before committing:

```bash
python3 scripts/validate_skills.py
```
