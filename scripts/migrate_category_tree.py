#!/usr/bin/env python3
"""Move legacy branches into the redesigned tree. Default: read-only plan.

Uses explicit branch mappings, not keyword reclassification. Preserves package
names and content except relative links that need rebasing. A CSV receipt records
old/new paths and hashes. Completed package moves are rolled back on failure.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import os
from pathlib import Path
import re
from urllib.parse import quote, unquote, urlsplit, urlunsplit

from skill_tree import CATEGORY_RENAMES, BRANCH_MOVES, destination_category
from validate_skills import ROOT, discover_skills, parse_frontmatter

RECEIPT = "references/category-tree-migration-2026-10-14.csv"
LINK = re.compile(r"(?P<open>!?\[[^\]]*\]\()(?P<target>[^)]+)(?P<close>\))")


def destination(root: Path, path: Path) -> Path:
    try:
        parts = path.relative_to(root / "skills").parts
    except ValueError:
        return path
    if len(parts) < 2:
        return path
    return root / "skills" / destination_category(parts[0], parts[1]) / Path(*parts[1:])


def rebase_links(text: str, root: Path, old: Path, new: Path) -> str:
    def replace(match):
        raw = match["target"].strip()
        title_match = re.search(r'''\s+(?:"[^"]*"|'[^']*')$''', raw)
        title = title_match[0] if title_match else ""
        raw = raw[:title_match.start()] if title_match else raw
        angle = raw.startswith("<") and raw.endswith(">")
        parsed = urlsplit(raw.strip("<>"))
        if parsed.scheme or parsed.netloc or not parsed.path:
            return match[0]
        old_target = (old.parent / unquote(parsed.path)).resolve()
        if not old_target.exists():
            return match[0]
        new_target = destination(root, old_target)
        if (new.parent / unquote(parsed.path)).resolve() == new_target:
            return match[0]
        path = quote(Path(os.path.relpath(new_target, new.parent)).as_posix(), safe="/._-~")
        target = urlunsplit(("", "", path, parsed.query, parsed.fragment))
        if angle:
            target = "<" + target + ">"
        return match["open"] + target + title + match["close"]
    return LINK.sub(replace, text)


def plan(root: Path):
    changes = []
    names = set()
    destinations = set()
    for old in discover_skills(root / "skills"):
        name, _, _, errors = parse_frontmatter(old)
        if errors or name != old.parent.name or name in names:
            raise ValueError(f"invalid or duplicate package: {old}: {errors}")
        names.add(name)
        new = destination(root, old)
        if new in destinations or (new != old and new.parent.exists()):
            raise ValueError(f"destination collision: {new.parent}")
        destinations.add(new)
        # All existing packages have a single file; refuse an unreviewed move
        # involving resource files rather than silently breaking their links.
        if old != new and list(old.parent.iterdir()) != [old]:
            raise ValueError(f"package has additional resources; review manually: {old.parent}")
        before = old.read_bytes()
        after_text = rebase_links(before.decode("utf-8"), root, old, new)
        after = after_text.encode("utf-8")
        if old != new or before != after:
            changes.append((old, new, before, after))
    if not names:
        raise ValueError("no skills found; refusing migration")
    return changes


def apply(root: Path, changes) -> None:
    from sync_catalog import planned_updates

    receipt = root / RECEIPT
    if receipt.exists():
        raise ValueError(f"migration receipt already exists; refusing to overwrite: {receipt}")
    moved = []
    saved = {}
    metadata = {}
    try:
        for old, new, before, after in changes:
            if old != new:
                new.parent.parent.mkdir(parents=True, exist_ok=True)
                old.parent.rename(new.parent)
            moved.append((old, new, before))
            if before != after:
                new.write_bytes(after)
        readme = root / "README.md"
        saved[readme] = readme.read_bytes()
        text = saved[readme].decode("utf-8")
        # Fix current overview links only; historical research is left intact.
        for (category, branch), target in BRANCH_MOVES.items():
            text = text.replace(f"skills/{category}/{branch}", f"skills/{target}/{branch}")
        for category, target in CATEGORY_RENAMES.items():
            text = text.replace(f"skills/{category}", f"skills/{target}")
        readme.write_text(text, encoding="utf-8")
        metadata = planned_updates(root)
        for path in metadata:
            if path not in saved:
                saved[path] = path.read_bytes() if path.exists() else None
        for path, text in metadata.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
        rows = io.StringIO(newline="")
        writer = csv.writer(rows, lineterminator="\n")
        writer.writerow(["old_path", "new_path", "sha256_before", "sha256_after"])
        for old, new, before, after in changes:
            writer.writerow([old.relative_to(root).as_posix(), new.relative_to(root).as_posix(), hashlib.sha256(before).hexdigest(), hashlib.sha256(after).hexdigest()])
        receipt.write_text(rows.getvalue(), encoding="utf-8")
    except Exception:
        receipt.unlink(missing_ok=True)
        for path, original in saved.items():
            if original is None:
                path.unlink(missing_ok=True)
            else:
                path.write_bytes(original)
        for old, new, before in reversed(moved):
            new.write_bytes(before)
            if old != new:
                new.parent.rename(old.parent)
        raise
    # Only remove empty directories; never recursively delete package contents.
    for directory in sorted((root / "skills").rglob("*"), key=lambda p: len(p.parts), reverse=True):
        if directory.is_dir() and not any(directory.iterdir()):
            directory.rmdir()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="move packages and regenerate navigation after reviewing the plan")
    args = parser.parse_args()
    try:
        changes = plan(ROOT)
        moves = sum(old != new for old, new, _, _ in changes)
        edits = sum(before != after for _, _, before, after in changes)
        print(f"Planned: {moves:,} package moves; {edits:,} relative-link edits.")
        if args.apply and changes:
            apply(ROOT, changes)
            print(f"Applied migration; receipt: {RECEIPT}")
        elif not changes:
            print("Already on the current category tree; nothing to move.")
        else:
            print("Read-only plan. Run with --apply to migrate.")
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"FAIL: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
