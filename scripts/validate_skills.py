#!/usr/bin/env python3
"""Validate publishable Hermes-style agentic skills."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover - local fallback supports the repo's simple frontmatter
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
MAX_DESCRIPTION_CHARS = 1024
MAX_SKILL_CHARS = 100_000
ALLOWED_SUPPORT_DIRS = {"references", "templates", "scripts", "assets"}
NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
SECRET_PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*['\"]?[A-Za-z0-9_./+=-]{16,}"),
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
]


def simple_yaml_mapping(raw: str) -> dict[str, Any]:
    """Very small fallback parser for top-level scalar frontmatter fields.

    CI installs PyYAML. This fallback lets a fresh macOS checkout validate the
    basic required fields without adding dependencies first.
    """
    data: dict[str, Any] = {}
    for line in raw.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith(" "):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            data[key] = value
    return data


def load_frontmatter(raw: str) -> dict[str, Any]:
    if yaml is not None:
        parsed = yaml.safe_load(raw)
        if not isinstance(parsed, dict):
            raise ValueError("frontmatter must be a YAML mapping")
        return parsed
    return simple_yaml_mapping(raw)


def parse_skill(path: Path) -> tuple[dict[str, Any], str]:
    content = path.read_text(encoding="utf-8")
    if len(content) > MAX_SKILL_CHARS:
        raise ValueError(f"SKILL.md exceeds {MAX_SKILL_CHARS:,} characters")
    if not content.startswith("---"):
        raise ValueError("frontmatter must start at byte 0 with ---")
    match = re.search(r"\n---\s*\n", content[3:])
    if not match:
        raise ValueError("frontmatter closing --- not found")
    end = match.start() + 3
    frontmatter_raw = content[3:end]
    body = content[end + len(match.group(0)) - 1 :]
    try:
        frontmatter = load_frontmatter(frontmatter_raw)
    except Exception as exc:  # noqa: BLE001
        raise ValueError(f"frontmatter YAML does not parse: {exc}") from exc
    if not body.strip():
        raise ValueError("body must be non-empty")
    return frontmatter, body


def validate_skill(skill_md: Path) -> list[str]:
    errors: list[str] = []
    rel = skill_md.relative_to(ROOT)
    skill_dir = skill_md.parent

    try:
        frontmatter, body = parse_skill(skill_md)
    except ValueError as exc:
        return [f"{rel}: {exc}"]

    name = frontmatter.get("name")
    description = frontmatter.get("description")

    if not name or not isinstance(name, str):
        errors.append(f"{rel}: missing string field 'name'")
    elif not NAME_RE.fullmatch(name):
        errors.append(f"{rel}: name must be lowercase, hyphenated, and <=64 chars")
    elif skill_dir.name != name:
        errors.append(f"{rel}: directory name '{skill_dir.name}' does not match skill name '{name}'")

    if not description or not isinstance(description, str):
        errors.append(f"{rel}: missing string field 'description'")
    elif len(description) > MAX_DESCRIPTION_CHARS:
        errors.append(f"{rel}: description exceeds {MAX_DESCRIPTION_CHARS} characters")

    for child in skill_dir.iterdir():
        if child.name == "SKILL.md":
            continue
        if child.is_dir() and child.name in ALLOWED_SUPPORT_DIRS:
            continue
        errors.append(f"{rel}: unsupported item in skill directory: {child.name}")

    content = skill_md.read_text(encoding="utf-8")
    for pattern in SECRET_PATTERNS:
        if pattern.search(content):
            errors.append(f"{rel}: possible secret/token pattern detected")
            break

    required_sections = ["## Overview", "## When to Use", "## Common Pitfalls", "## Verification Checklist"]
    for section in required_sections:
        if section not in body:
            errors.append(f"{rel}: recommended section missing: {section}")

    return errors


def main() -> int:
    if not SKILLS_DIR.exists():
        print(f"ERROR: skills directory not found: {SKILLS_DIR}", file=sys.stderr)
        return 1

    skill_files = sorted(
        path
        for path in SKILLS_DIR.rglob("SKILL.md")
        if not ALLOWED_SUPPORT_DIRS.intersection(path.relative_to(SKILLS_DIR).parts)
    )
    if not skill_files:
        print("No SKILL.md files found yet. Scaffold is valid; add skills under skills/<category>[/<subcategory>]/<name>/SKILL.md.")
        return 0

    all_errors: list[str] = []
    for skill_md in skill_files:
        all_errors.extend(validate_skill(skill_md))

    if all_errors:
        print("Skill validation failed:", file=sys.stderr)
        for error in all_errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Validated {len(skill_files)} skill(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
