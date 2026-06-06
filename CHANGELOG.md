# Changelog

## 0.3.0

- Add `operational-session-closeout` under `Dev`: closes substantial agent sessions with objective state, verification evidence, raw usage telemetry priorities, lifecycle markers, open loops, and handoff-ready next actions.
- Include closeout references for harness adapters, telemetry contracts, templates, examples, delta calculation, runtime telemetry initialization, and raw usage accounting hardening.

## 0.2.0

- Add `story-map` skill under new `Dev/CLAUDE` category: facilitates Three Amigos story mapping sessions with a PO/Dev/QA agent team that debates via inter-agent messaging and incrementally builds a master story map. Requires Claude Code agent teams.
- Support nested category folders in `validate_skills.py` (discovers `SKILL.md` at any depth under `skills/`, skipping support directories).
- Document runtime-specific subcategories in the README.

## 0.1.0

- Initial repository scaffold for publishing agentic skills.
