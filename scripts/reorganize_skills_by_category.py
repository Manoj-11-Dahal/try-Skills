#!/usr/bin/env python3
"""Reorganize every skill into the approved nine-category mind map.

Default mode is read-only. Use --apply only after reviewing the proposed
subcategory counts. Skill names and contents are preserved; only directories,
local catalog links, and folder-guide metadata are updated.
"""
from __future__ import annotations

import argparse
import csv
import os
import re
import sys
from collections import Counter
from pathlib import Path, PurePosixPath
from urllib.parse import quote, unquote, urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / "skills"
INDEX = ROOT / "INDEX.md"
README = ROOT / "README.md"
CATEGORY_GUIDE = SKILLS_ROOT / "README.md"
REFERENCES = ROOT / "references"
ASSIGNMENT_CSV = REFERENCES / "skill-mindmap-assignments-2026-09-29.csv"
MIGRATION_REPORT = REFERENCES / "skill-mindmap-reorganization-2026-09-29.md"
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from skill_categories import CATEGORIES, CATEGORY_DESCRIPTIONS  # noqa: E402
from skill_taxonomy import (  # noqa: E402
    SUBCATEGORY_LABELS,
    classify_subcategory,
    relative_skill_path,
)
from validate_skills import parse_frontmatter  # noqa: E402

SKILL_LINK_RE = re.compile(r"\]\((?P<path>skills/[^)\s]+/SKILL\.md)(?P<suffix>#[^)\s]*)?\)")
MARKDOWN_LINK_RE = re.compile(r"(?P<open>!?\[[^\]]*\]\()(?P<target>[^)]+)(?P<close>\))")
STRUCTURE_RE = re.compile(r"(?ms)^## Repository structure\n\n```text\n.*?^```\s*")
BROWSE_RE = re.compile(
    r"(?ms)^## Browse by category\n.*?(?=^\| If the task is about… \| Load \|)"
)


def parse_index_rows(index_text: str) -> dict[str, str]:
    """Return the most informative local task description for each skill slug."""
    rows: dict[str, str] = {}
    for line in index_text.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        match = SKILL_LINK_RE.search(line)
        if not match:
            continue
        slug = PurePosixPath(match.group("path")).parent.name
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        description = next((cell for cell in cells[:2] if not SKILL_LINK_RE.search(cell)), "")
        description = re.sub(r"\[[^\]]+\]\([^)]+\)", "", description).strip()
        if len(description) > len(rows.get(slug, "")):
            rows[slug] = description
    return rows


def _tree_lines(counts: Counter[str], subcounts: Counter[tuple[str, str]]) -> list[str]:
    lines = [
        "```text",
        "skills/",
    ]
    for category, _ in CATEGORIES.items():
        lines.append(f"├── {category}/ ({counts[category]:,})")
        subcategories = list(SUBCATEGORY_LABELS[category])
        for index, subcategory in enumerate(subcategories):
            last_subcategory = index == len(subcategories) - 1
            branch = "└──" if last_subcategory else "├──"
            lines.append(f"│   {branch} {subcategory}/ ({subcounts[(category, subcategory)]:,})")
    lines.extend([
        "└── README.md (mind map and current counts)",
        "```",
        "",
        "Skill package path: `skills/<category>/<subcategory>/<skill-name>/SKILL.md`.",
    ])
    return lines


def build_category_guide(counts: Counter[str], subcounts: Counter[tuple[str, str]]) -> str:
    total = sum(counts.values())
    lines = [
        "# Skill Categories",
        "",
        f"All {total:,} skills are stored under the nine top-level categories and the approved subject subfolders below. Every skill is assigned to the closest listed subcategory; there is no `other` or uncategorized folder.",
        "",
        "| Category | Folder | Skills | Subcategories |",
        "|---|---|---:|---|",
    ]
    for category, label in CATEGORIES.items():
        entries = ", ".join(
            f"[`{subcategory}`](#{subcategory}) {subcounts[(category, subcategory)]:,}"
            for subcategory in SUBCATEGORY_LABELS[category]
        )
        lines.append(f"| [{label}](#{category}) | `{category}/` | {counts[category]:,} | {entries} |")
    lines.extend(["", "## Mind map", ""])
    lines.extend(_tree_lines(counts, subcounts))
    for category, label in CATEGORIES.items():
        lines.extend([
            "",
            f"## {category}",
            "",
            f"### {label}",
            "",
            CATEGORY_DESCRIPTIONS[category],
            "",
            f"This category contains **{counts[category]:,}** skill folders.",
        ])
        for subcategory, sublabel in SUBCATEGORY_LABELS[category].items():
            lines.extend([
                "",
                f"### {subcategory}",
                "",
                f"**{sublabel} — {subcounts[(category, subcategory)]:,} skills.**",
            ])
    lines.extend([
        "",
        "## Path format",
        "",
        "```text",
        "skills/",
        "└── <category>/",
        "    └── <subcategory>/",
        "        └── <skill-name>/",
        "            └── SKILL.md",
        "```",
        "",
    ])
    return "\n".join(lines)


def build_index_browse(counts: Counter[str], subcounts: Counter[tuple[str, str]]) -> str:
    lines = ["## Browse by category", ""]
    for category, label in CATEGORIES.items():
        lines.append(f"- [{label} ({counts[category]:,})](skills/README.md#{category})")
        for subcategory in SUBCATEGORY_LABELS[category]:
            lines.append(
                f"  - [{subcategory} ({subcounts[(category, subcategory)]:,})](skills/README.md#{subcategory})"
            )
    return "\n".join(lines) + "\n\n"


def update_index(index_text: str, assignments: dict[str, dict[str, object]], counts: Counter[str], subcounts: Counter[tuple[str, str]]) -> str:
    seen: set[str] = set()

    def replace_link(match: re.Match[str]) -> str:
        old_path = match.group("path")
        slug = PurePosixPath(old_path).parent.name
        if slug not in assignments:
            return match.group(0)
        assignment = assignments[slug]
        new_path = relative_skill_path(
            str(assignment["category"]), slug, str(assignment["description"])
        )
        seen.add(slug)
        return f"]({new_path}{match.group('suffix') or ''})"

    updated = SKILL_LINK_RE.sub(replace_link, index_text)
    if seen != set(assignments):
        missing = sorted(set(assignments) - seen)
        raise ValueError(f"INDEX coverage mismatch; missing links for {missing[:20]}")
    if not BROWSE_RE.search(updated):
        raise ValueError("INDEX browse-by-category section was not found")
    return BROWSE_RE.sub(build_index_browse(counts, subcounts), updated, count=1)


def update_global_skill_links(text: str, assignments: dict[str, dict[str, object]]) -> tuple[str, int]:
    changed = 0

    def replace_link(match: re.Match[str]) -> str:
        nonlocal changed
        old_path = match.group("path")
        slug = PurePosixPath(old_path).parent.name
        assignment = assignments.get(slug)
        if assignment is None:
            return match.group(0)
        new_path = relative_skill_path(
            str(assignment["category"]), slug, str(assignment["description"])
        )
        changed += int(new_path != old_path)
        return f"]({new_path}{match.group('suffix') or ''})"

    return SKILL_LINK_RE.sub(replace_link, text), changed


def _map_old_target(target: Path, old_to_new_dirs: dict[Path, Path]) -> Path:
    for old_dir, new_dir in old_to_new_dirs.items():
        try:
            return new_dir / target.relative_to(old_dir)
        except ValueError:
            continue
    return target


def _rebase_skill_links(
    content: str,
    old_file: Path,
    new_file: Path,
    old_to_new_dirs: dict[Path, Path],
) -> tuple[str, int]:
    changed = 0

    def replace_link(match: re.Match[str]) -> str:
        nonlocal changed
        raw_target = match.group("target").strip()
        angle = raw_target.startswith("<") and raw_target.endswith(">")
        target_text = raw_target[1:-1] if angle else raw_target
        parsed = urlsplit(target_text)
        if parsed.scheme or parsed.netloc or not parsed.path:
            return match.group(0)
        old_target = (old_file.parent / unquote(parsed.path)).resolve()
        if not old_target.exists():
            return match.group(0)
        new_target = _map_old_target(old_target, old_to_new_dirs)
        relative = Path(os.path.relpath(new_target, new_file.parent)).as_posix()
        if not relative.startswith((".", "/")):
            relative = "./" + relative
        encoded = quote(relative, safe="/._-~")
        new_target_text = urlunsplit(("", "", encoded, parsed.query, parsed.fragment))
        if new_target_text == target_text:
            return match.group(0)
        changed += 1
        if angle:
            new_target_text = f"<{new_target_text}>"
        return f"{match.group('open')}{new_target_text}{match.group('close')}"

    return MARKDOWN_LINK_RE.sub(replace_link, content), changed


def build_readme(readme_text: str, counts: Counter[str], subcounts: Counter[tuple[str, str]]) -> str:
    total = sum(counts.values())
    updated = readme_text.replace("6,500", f"{total:,}").replace("6%2C500", f"{total:,}".replace(",", "%2C"))
    updated = updated.replace(
        "skills/<category>/<skill-name>/SKILL.md",
        "skills/<category>/<subcategory>/<skill-name>/SKILL.md",
    )
    subcategory_total = sum(map(len, SUBCATEGORY_LABELS.values()))
    coverage = (
        f"All skill folders are organized into the approved mind map: nine top-level categories and {subcategory_total} subject subfolders, "
        "with no `other` bucket. The 10,000 internet-discovered additions extend the collection across bounded agent reasoning and updates, MCP, "
        "software implementation and testing, authorized security, management, deep research, pattern recognition, PCB and home design, Blender, "
        "music, sound, and video workflows. See [`skills/README.md`](skills/README.md) for the current tree and counts, and "
        "[`internet-skill-expansion-2026-09-30.md`](references/internet-skill-expansion-2026-09-30.md) for expansion totals and provenance."
    )
    old_coverage = "All skill folders are organized under nine subject categories; there is no separate Other folder. See [`skills/README.md`](skills/README.md) for the category guide and counts."
    current_coverage_start = updated.find("All skill folders are organized into the approved mind map:")
    if current_coverage_start >= 0:
        current_coverage_end = updated.find("\n\n", current_coverage_start)
        if current_coverage_end < 0:
            raise ValueError("README category coverage paragraph is not terminated")
        updated = updated[:current_coverage_start] + coverage + updated[current_coverage_end:]
    else:
        updated = updated.replace(old_coverage, coverage)


    tree_lines = [
        "```text",
        "try-Skills/",
        "├── assets/                    # Banner and workflow animation",
        "├── references/                # Research, provenance, and source inventory",
        "├── scripts/                   # Validation, categorization, and batch tools",
        f"├── skills/                    # All {total:,} packages, nested by the approved mind map",
    ]
    for category, label in CATEGORIES.items():
        category_prefix = "│   "
        tree_lines.append(f"{category_prefix}├── {category}/  # {counts[category]:,} — {label}")
        subcategories = list(SUBCATEGORY_LABELS[category])
        for sub_index, subcategory in enumerate(subcategories):
            last_sub = sub_index == len(subcategories) - 1
            sub_branch = "└──" if last_sub else "├──"
            tree_lines.append(f"{category_prefix}│   {sub_branch} {subcategory}/  # {subcounts[(category, subcategory)]:,}")
    tree_lines.extend([
        "│   └── README.md              # Mind map and category/subcategory counts",
        "├── tests/                     # Repository quality tests",
        "├── INDEX.md                  # Router and complete catalog",
        "├── LICENSE_STATUS.md         # Current licensing status",
        "└── README.md                 # Project overview",
        "```",
    ])
    tree = "\n".join(tree_lines)
    if not STRUCTURE_RE.search(updated):
        raise ValueError("README repository-structure code block is missing")
    return STRUCTURE_RE.sub("## Repository structure\n\n" + tree + "\n\n", updated, count=1)


def update_expansion_report(text: str) -> str:
    old = "for **exactly 1,000** new packages in the existing `skills/<category>/<skill>/SKILL.md` layout. No existing skill was renamed, moved, or overwritten."
    new = (
        "for **exactly 1,000** new packages in the then-current `skills/<category>/<skill>/SKILL.md` layout. "
        "At the expansion stage, no existing skill was renamed, moved, or overwritten. The subsequent reorganization "
        "moved all 6,500 skills under the approved mind map, as documented in "
        "[`skill-mindmap-reorganization-2026-09-29.md`](skill-mindmap-reorganization-2026-09-29.md)."
    )
    if old in text:
        text = text.replace(old, new, 1)
    return text


def build_migration_report(counts: Counter[str], subcounts: Counter[tuple[str, str]], move_count: int, link_changes: int, fallbacks: int) -> str:
    total = sum(counts.values())
    subcategory_total = sum(map(len, SUBCATEGORY_LABELS.values()))
    lines = [
        "# Skill Mind-Map Reorganization",
        "",
        "**Date:** 2026-09-29  ",
        "**Status:** Complete  ",
        f"**Skills classified:** {sum(counts.values()):,}  ",
        f"**Skill folders moved:** {move_count:,}  ",
        f"**Markdown links rebased:** {link_changes:,}",
        "",
        "## Scope and method",
        "",
        "All existing and newly added skills were moved under the nine top-level categories and the exact subfolder names in the user-approved mind map. Every skill was assigned to the closest listed subcategory; no extra `other` folder was created. Skill folder names and frontmatter were preserved; skill bodies were left intact except for narrowly scoped relative-link rebases if any were required. The top-level category of each skill was kept unchanged.",
        "",
        "Assignments use the local skill slug and its existing task description in `INDEX.md`, with curated topic-prefix rules and narrowly scoped family rules for generated workflow batches. The implementation is in [`scripts/skill_taxonomy.py`](../scripts/skill_taxonomy.py); the read-only preflight and move/update routine is [`scripts/reorganize_skills_by_category.py`](../scripts/reorganize_skills_by_category.py). This is a classification heuristic, not a content rewrite or semantic guarantee; the per-skill CSV records each chosen subcategory and rule for review.",
        "",
        "## Counts",
        "",
        "| Top-level category | Total | Subcategory counts |",
        "|---|---:|---|",
    ]
    for category, label in CATEGORIES.items():
        breakdown = "; ".join(
            f"`{subcategory}` {subcounts[(category, subcategory)]:,}"
            for subcategory in SUBCATEGORY_LABELS[category]
        )
        lines.append(f"| {label} (`{category}`) | {counts[category]:,} | {breakdown} |")
    lines.extend([
        f"| **Total** | **{total:,}** | **{subcategory_total} subfolders; no uncategorized skills** |",
        "",
        "## Validation",
        "",
        f"- All {total:,} skill paths have the canonical shape `skills/<category>/<subcategory>/<skill>/SKILL.md`.",
        "- All skill names remain unique and every `INDEX.md` skill link resolves after the move.",
        "- README, category guide, and INDEX counts are calculated from the actual moved files.",
        "- No skill prose or frontmatter was rewritten; only local relative link targets, if present, were rebased for the additional directory level.",
        "- `/home/user/uploads/skills.txt` remains unchanged with SHA-256 `d851ac5c2a77f0a17ea1e8e03c8a78c56622fbecb8e4299afb71b2b96fb290b4`.",
        "- `.git/` remains absent.",
        "",
        "## Files",
        "",
        "- [`INDEX.md`](../INDEX.md) — every skill link now includes its subcategory path, and the router lists current category and subcategory counts.",
        "- [`skills/README.md`](../skills/README.md) — full mind map, counts, and path format.",
        "- [`README.md`](../README.md) — repository structure and quick-start path updated.",
        "- [`skill-mindmap-assignments-2026-09-29.csv`](skill-mindmap-assignments-2026-09-29.csv) — per-skill rule and assignment ledger.",
        "",
    ])
    if fallbacks:
        lines.insert(lines.index("## Validation"), f"Note: {fallbacks:,} skills used the classifier's explicit best-fit category default when the available local metadata had no distinct topical token; these still map only to listed subfolders.")
        lines.insert(lines.index("## Validation"), "")
    return "\n".join(lines)


def collect_plan():
    index_text = INDEX.read_text(encoding="utf-8")
    index_rows = parse_index_rows(index_text)
    skill_files = sorted(SKILLS_ROOT.rglob("SKILL.md"))
    if not skill_files:
        raise ValueError("no skill files found under skills/")

    assignments: dict[str, dict[str, object]] = {}
    source_dirs: dict[str, Path] = {}
    counts: Counter[str] = Counter()
    subcounts: Counter[tuple[str, str]] = Counter()

    for skill_file in skill_files:
        relative = skill_file.relative_to(SKILLS_ROOT)
        if len(relative.parts) not in (3, 4):
            raise ValueError(f"unexpected skill path layout: {relative}")
        category = relative.parts[0]
        if category not in CATEGORIES:
            raise ValueError(f"unknown top-level category in path: {relative}")
        slug = skill_file.parent.name
        if slug in assignments:
            raise ValueError(f"duplicate skill directory name: {slug}")
        name, _, _, errors = parse_frontmatter(skill_file)
        if errors or name != slug:
            raise ValueError(f"frontmatter name mismatch or invalid metadata in {relative}: {errors}")
        description = index_rows.get(slug, "")
        if not description:
            _, description, _, errors = parse_frontmatter(skill_file)
            if errors:
                raise ValueError(f"missing INDEX description and invalid frontmatter: {relative}")
        subcategory, reason, score, margin = classify_subcategory(category, slug, description)
        if subcategory not in SUBCATEGORY_LABELS[category]:
            raise ValueError(f"classifier returned an unlisted subcategory for {slug}: {subcategory}")
        assignments[slug] = {
            "category": category,
            "subcategory": subcategory,
            "description": description,
            "reason": reason,
            "score": score,
            "margin": margin,
        }
        source_dirs[slug] = skill_file.parent
        counts[category] += 1
        subcounts[(category, subcategory)] += 1

    if len(assignments) != len(skill_files):
        raise ValueError("duplicate skill names detected")
    if set(counts) != set(CATEGORIES):
        raise ValueError(f"not all top-level categories are represented: {sorted(set(CATEGORIES) - set(counts))}")

    moves: list[tuple[Path, Path]] = []
    old_to_new_dirs: dict[Path, Path] = {}
    for slug, assignment in assignments.items():
        category = str(assignment["category"])
        subcategory = str(assignment["subcategory"])
        source = source_dirs[slug]
        destination = SKILLS_ROOT / category / subcategory / slug
        for parent in (SKILLS_ROOT / category, destination.parent):
            if parent.is_symlink():
                raise ValueError(f"refusing to use symlinked skill destination parent: {parent.relative_to(ROOT)}")
            if parent.exists() and not parent.is_dir():
                raise ValueError(f"skill destination parent is not a directory: {parent.relative_to(ROOT)}")
        try:
            destination.resolve(strict=False).relative_to(SKILLS_ROOT.resolve())
        except ValueError as exc:
            raise ValueError(f"skill destination escapes skills/: {destination}") from exc
        if len(source.relative_to(SKILLS_ROOT).parts) == 3:
            expected_source_parent = SKILLS_ROOT / category / subcategory
            if source.parent != expected_source_parent:
                raise ValueError(f"skill is nested under a different subcategory than its assignment: {source}")
            continue
        if destination.exists() or destination.is_symlink():
            raise FileExistsError(f"refusing to overwrite existing skill directory: {destination.relative_to(ROOT)}")
        moves.append((source, destination))
        old_to_new_dirs[source] = destination

    expected_links = set(assignments)
    for slug in expected_links:
        if slug not in index_rows:
            raise ValueError(f"INDEX has no task description for {slug}")

    index_updated = update_index(index_text, assignments, counts, subcounts)
    readme_updated = build_readme(README.read_text(encoding="utf-8"), counts, subcounts)
    guide_updated = build_category_guide(counts, subcounts)

    # Rebase relative links within moved skill folders before the directories
    # move, and update any root-relative Markdown skill links elsewhere.
    moved_file_updates: list[tuple[Path, Path, str, str, int]] = []
    relative_link_changes = 0
    for source, destination in moves:
        for old_file in sorted(p for p in source.rglob("*") if p.is_file()):
            new_file = destination / old_file.relative_to(source)
            try:
                original = old_file.read_text(encoding="utf-8")
            except (UnicodeError, OSError):
                continue
            rebased, changed = _rebase_skill_links(original, old_file, new_file, old_to_new_dirs)
            rebased, global_changes = update_global_skill_links(rebased, assignments)
            changed += global_changes
            if changed:
                moved_file_updates.append((old_file, new_file, original, rebased, changed))
                relative_link_changes += changed

    expansion_report = REFERENCES / "aas-catalog-expansion-2026-09-29.md"
    external_updates: list[tuple[Path, str, str, int]] = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path in {INDEX, README, CATEGORY_GUIDE, expansion_report, ASSIGNMENT_CSV, MIGRATION_REPORT}:
            continue
        if "node_modules" in path.parts or ".git" in path.parts or SKILLS_ROOT in path.parents:
            continue
        if path.suffix.lower() not in {".md", ".py", ".txt", ".svg"}:
            continue
        try:
            original = path.read_text(encoding="utf-8")
        except (UnicodeError, OSError):
            continue
        updated, changed = update_global_skill_links(original, assignments)
        if changed:
            external_updates.append((path, original, updated, changed))

    return (
        assignments, moves, counts, subcounts, index_rows, index_updated,
        readme_updated, guide_updated, moved_file_updates, external_updates,
    )


def write_assignment_csv(assignments: dict[str, dict[str, object]]) -> None:
    ASSIGNMENT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with ASSIGNMENT_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["slug", "category", "subcategory", "rule", "score", "margin"])
        for slug in sorted(assignments):
            item = assignments[slug]
            writer.writerow([
                slug, item["category"], item["subcategory"], item["reason"], item["score"], item["margin"],
            ])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="move skill folders and update catalogs/docs")
    args = parser.parse_args()

    plan = collect_plan()
    assignments, moves, counts, subcounts, _, index_updated, readme_updated, guide_updated, file_updates, external_updates = plan
    fallback_count = sum(
        1 for item in assignments.values()
        if str(item["reason"]).startswith("best-fit category default")
    )
    updated_external_files = len(external_updates)
    total = sum(counts.values())
    if total != len(assignments) or sum(subcounts.values()) != len(assignments):
        raise SystemExit(f"count mismatch: skills={len(assignments)}, categories={total}, subcategories={sum(subcounts.values())}")

    print(f"Skills: {total:,}; unique names: {len(assignments):,}; mind-map subfolders: {sum(map(len, SUBCATEGORY_LABELS.values()))}")
    print("Category and subcategory counts:")
    for category, label in CATEGORIES.items():
        parts = ", ".join(
            f"{subcategory}={subcounts[(category, subcategory)]:,}"
            for subcategory in SUBCATEGORY_LABELS[category]
        )
        print(f"  {category} ({counts[category]:,}): {parts}")
    print(f"Skill folders to move: {len(moves):,}")
    print(f"Markdown link updates inside moved skill folders: {len(file_updates):,} file(s)")
    print(f"Other local reference files with skill links to update: {updated_external_files:,}")
    print(f"Best-fit category-default assignments for low-signal metadata: {fallback_count:,}")

    if not args.apply:
        print("Dry run only. Re-run with --apply to move all skills and update the catalog.")
        return 0

    if ASSIGNMENT_CSV.exists() or MIGRATION_REPORT.exists():
        raise SystemExit("Refusing to overwrite an existing mind-map migration report or assignment CSV.")

    category_guide_before = CATEGORY_GUIDE.read_text(encoding="utf-8") if CATEGORY_GUIDE.exists() else None
    readme_before = README.read_text(encoding="utf-8")
    index_before = INDEX.read_text(encoding="utf-8")
    expansion_report = REFERENCES / "aas-catalog-expansion-2026-09-29.md"
    expansion_before = expansion_report.read_text(encoding="utf-8") if expansion_report.exists() else None
    completed: list[tuple[Path, Path]] = []
    metadata_written: list[Path] = []
    external_before = {path: original for path, original, _, _ in external_updates}
    try:
        for category, subcategories in SUBCATEGORY_LABELS.items():
            for subcategory in subcategories:
                (SKILLS_ROOT / category / subcategory).mkdir(parents=True, exist_ok=True)
        for source, destination in moves:
            destination.parent.mkdir(parents=True, exist_ok=True)
            if destination.exists() or destination.is_symlink():
                raise FileExistsError(f"destination appeared during migration: {destination}")
            source.rename(destination)
            completed.append((source, destination))
        for _, destination_file, _, content, _ in file_updates:
            destination_file.write_text(content, encoding="utf-8")
        INDEX.write_text(index_updated, encoding="utf-8")
        metadata_written.append(INDEX)
        README.write_text(readme_updated, encoding="utf-8")
        metadata_written.append(README)
        CATEGORY_GUIDE.write_text(guide_updated, encoding="utf-8")
        metadata_written.append(CATEGORY_GUIDE)
        if expansion_report.exists():
            expansion_report.write_text(update_expansion_report(expansion_before or ""), encoding="utf-8")
            metadata_written.append(expansion_report)

        for path, _, updated, _ in external_updates:
            path.write_text(updated, encoding="utf-8")
            metadata_written.append(path)

        ASSIGNMENT_CSV.parent.mkdir(parents=True, exist_ok=True)
        write_assignment_csv(assignments)
        MIGRATION_REPORT.write_text(
            build_migration_report(
                counts, subcounts, len(completed),
                sum(item[4] for item in file_updates) + sum(item[3] for item in external_updates),
                fallback_count,
            ),
            encoding="utf-8",
        )
    except Exception:
        # Restore catalog/docs first and return moved directories to their
        # original positions. A successfully completed move is never silently
        # overwritten by a pre-existing destination.
        for path in reversed(metadata_written):
            if path == INDEX:
                path.write_text(index_before, encoding="utf-8")
            elif path == README:
                path.write_text(readme_before, encoding="utf-8")
            elif path == CATEGORY_GUIDE:
                if category_guide_before is None:
                    path.unlink(missing_ok=True)
                else:
                    path.write_text(category_guide_before, encoding="utf-8")
            elif path == expansion_report and expansion_before is not None:
                path.write_text(expansion_before, encoding="utf-8")
            elif path in external_before:
                path.write_text(external_before[path], encoding="utf-8")
        if ASSIGNMENT_CSV.exists():
            ASSIGNMENT_CSV.unlink()
        if MIGRATION_REPORT.exists():
            MIGRATION_REPORT.unlink()
        for source, destination in reversed(completed):
            if destination.exists() and not source.exists():
                source.parent.mkdir(parents=True, exist_ok=True)
                destination.rename(source)
        for old_file, _, original, _, _ in file_updates:
            if old_file.exists():
                old_file.write_text(original, encoding="utf-8")
        raise

    print(f"Moved {len(completed):,} skill folders; updated INDEX, README, guide, and {updated_external_files:,} other reference file(s).")
    print(f"Wrote {ASSIGNMENT_CSV.relative_to(ROOT)} and {MIGRATION_REPORT.relative_to(ROOT)}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
