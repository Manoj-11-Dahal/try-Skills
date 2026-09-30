#!/usr/bin/env python3
"""Validate the local agentic-skills repository without third-party packages."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

from skill_categories import CATEGORIES
from skill_taxonomy import SUBCATEGORY_LABELS

ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / "skills"
FRONTMATTER_KEYS = ("name", "description")
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_RE = re.compile(r"!??\[[^\]]*\]\(([^)]+)\)")
CJK_RANGES = (
    (0x3400, 0x4DBF), (0x4E00, 0x9FFF), (0xF900, 0xFAFF),
    (0x3040, 0x30FF), (0xAC00, 0xD7AF),
)


def content_units(text: str) -> int:
    """Count English-like words as one unit and CJK characters as three."""
    units = 0
    in_word = False
    for char in text:
        code = ord(char)
        if any(start <= code <= end for start, end in CJK_RANGES):
            if in_word:
                units += 1
                in_word = False
            units += 3
        elif char.isalnum() or char in "_'":
            in_word = True
        elif in_word:
            units += 1
            in_word = False
    if in_word:
        units += 1
    return units


def parse_frontmatter(path: Path) -> tuple[str, str, str, list[str]]:
    errors: list[str] = []
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return "", "", "", [f"cannot read UTF-8 content: {exc}"]
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return "", "", text, ["frontmatter must start with ---"]
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return "", "", text, ["frontmatter closing --- is missing"]
    meta_lines = [line for line in lines[1:end] if line.strip()]
    keys: list[str] = []
    values: dict[str, str] = {}
    for line in meta_lines:
        if ":" not in line:
            errors.append(f"invalid frontmatter line: {line}")
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        keys.append(key)
        values[key] = value.strip()
    if tuple(keys) != FRONTMATTER_KEYS:
        errors.append(f"frontmatter keys must be exactly {FRONTMATTER_KEYS}, got {tuple(keys)}")
    name = values.get("name", "")
    raw_description = values.get("description", "")
    description = ""
    if raw_description.startswith('"'):
        try:
            description = json.loads(raw_description)
            if not isinstance(description, str):
                errors.append("description must be a string")
                description = ""
        except json.JSONDecodeError as exc:
            errors.append(f"description must be valid double-quoted YAML/JSON text: {exc}")
    else:
        errors.append("description must be double-quoted")
    body = "\n".join(lines[end + 1:])
    return name, description, body, errors


def validate_skill(path: Path) -> list[str]:
    errors: list[str] = []
    name, description, body, parse_errors = parse_frontmatter(path)
    errors.extend(parse_errors)
    expected_name = path.parent.name
    if not NAME_RE.fullmatch(name):
        errors.append(f"name is not lowercase kebab-case: {name!r}")
    if name != expected_name:
        errors.append(f"frontmatter name {name!r} does not match directory {expected_name!r}")
    if len(description) > 1024:
        errors.append(f"description exceeds 1024 characters ({len(description)})")
    units = content_units(description)
    if units < 40:
        errors.append(f"description has {units} content units; minimum is 40")
    if not (re.search(r"\bUse when\b", description, re.I) or re.search(r"^##\s+When to Use\s*$", body, re.M | re.I)):
        errors.append("when-to-use condition is missing")
    headings = re.findall(r"^#{1,6}\s+(.+?)\s*#*\s*$", body, re.M)
    normalized = [h.strip().casefold() for h in headings]
    if len(headings) < 3:
        errors.append(f"needs at least 3 Markdown sections/headings; found {len(headings)}")
    if len(normalized) != len(set(normalized)):
        errors.append("duplicate Markdown heading detected")
    if sum(1 for line in body.splitlines() if re.match(r"^#\s+\S", line)) != 1:
        errors.append("body must contain exactly one level-one title")
    size = path.stat().st_size
    if not (400 <= size <= 60_000):
        errors.append(f"file size {size} bytes is outside 400..60000")
    for target in LINK_RE.findall(body):
        target = target.strip().strip("<>")
        parsed = urlsplit(target)
        if parsed.scheme or target.startswith("//") or not parsed.path:
            continue
        local = (path.parent / unquote(parsed.path)).resolve()
        if not local.exists():
            errors.append(f"relative link points to missing path: {target}")
    return errors


def discover_skills() -> list[Path]:
    if not SKILLS_ROOT.is_dir():
        return []
    return sorted(SKILLS_ROOT.rglob("SKILL.md"))


def validate_all() -> list[str]:
    paths = discover_skills()
    if not paths:
        return ["no skills found under skills/<category>/<subcategory>/<name>/SKILL.md"]
    errors: list[str] = []
    names: set[str] = set()
    expected_categories = set(CATEGORIES)
    actual_categories = {
        child.name for child in SKILLS_ROOT.iterdir()
        if child.is_dir() and any(child.rglob("SKILL.md"))
    }
    if actual_categories != expected_categories:
        missing = sorted(expected_categories - actual_categories)
        extra = sorted(actual_categories - expected_categories)
        errors.append(f"category folders mismatch; missing={missing}, extra={extra}")
    for path in paths:
        relative = path.relative_to(SKILLS_ROOT)
        if (
            len(relative.parts) != 4
            or relative.parts[0] not in expected_categories
            or relative.parts[1] not in SUBCATEGORY_LABELS.get(relative.parts[0], {})
        ):
            errors.append(f"skill must be stored under skills/<category>/<subcategory>/<name>/SKILL.md: {relative}")
        name, _, _, _ = parse_frontmatter(path)
        if name in names:
            errors.append(f"duplicate skill name: {name}")
        names.add(name)
        for issue in validate_skill(path):
            errors.append(f"{path.relative_to(ROOT)}: {issue}")
    return errors


def main() -> int:
    skill_paths = discover_skills()
    errors = validate_all()
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        print(f"Validation failed: {len(errors)} issue(s), {len(skill_paths)} skill(s) scanned.")
        return 1
    print(f"Validated {len(skill_paths)} skill(s): all repository checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
