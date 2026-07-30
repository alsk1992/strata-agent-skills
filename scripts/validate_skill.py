#!/usr/bin/env python3

import re
import sys
from pathlib import Path


def fail(message: str) -> None:
    raise SystemExit(message)


def validate(path: Path) -> None:
    skill = path / "SKILL.md"
    if not skill.is_file():
        fail(f"{skill}: missing")
    content = skill.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
    if not match:
        fail(f"{skill}: invalid YAML frontmatter boundary")
    frontmatter = match.group(1)
    name = re.search(r"^name:\s*([a-z0-9-]+)\s*$", frontmatter, re.MULTILINE)
    description = re.search(r"^description:\s*(.+)\s*$", frontmatter, re.MULTILINE)
    if not name or name.group(1) != path.name:
        fail(f"{skill}: name must match directory")
    if not description or len(description.group(1).strip()) < 40:
        fail(f"{skill}: description is missing or too short")
    if "TODO" in content:
        fail(f"{skill}: unresolved TODO")
    if len(content.splitlines()) > 500:
        fail(f"{skill}: exceeds 500 lines")
    metadata = path / "agents" / "openai.yaml"
    if not metadata.is_file():
        fail(f"{metadata}: missing")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        fail("usage: validate_skill.py <skill-directory>")
    validate(Path(sys.argv[1]))
    print("skill is valid")
