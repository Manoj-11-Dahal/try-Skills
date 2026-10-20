#!/usr/bin/env python3
"""skills — browse every package in the Agentic Skills library from a terminal.

Surfaces
--------
  skills                      overview of all 15,860 skills
  skills list                 every skill, paged (--page / --limit / --all)
  skills show <query>         one skill, in full
  skills find <query>         search names and descriptions
  skills stats                library statistics
  skills cmd                  command reference

Query forms accepted by `show` and `find`
-----------------------------------------
  aas-agent-quality-route-cost-threshold-rule-check
  /skills/aas-agent-quality-route-cost-threshold-rule-check
  skills/ai-agent-systems/evaluation-observability/<name>
  skills/ai-agent-systems/evaluation-observability/<name>/SKILL.md

  /skills/try-skills          the repository itself -> prints the overview

No third-party packages, no network access. Indexing all 15,860 packages takes
about 0.35s because only the frontmatter block of each file is read.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
import os
from pathlib import Path
import shutil
import sys
import textwrap

ROOT = Path(os.environ.get("SKILLS_ROOT") or Path(__file__).resolve().parents[1])
SKILLS = ROOT / "skills"
REPO_ALIASES = {"try-skills", "tryskills", "repo", "root", "skills", "library"}
FM_READ_BYTES = 8192

_CODES = {
    "bold": "1", "dim": "2", "red": "31", "green": "32", "yellow": "33",
    "blue": "34", "magenta": "35", "cyan": "36", "grey": "90",
}
COLOR = False
WIDTH = 100


def paint(style: str, text: str) -> str:
    if not COLOR:
        return text
    return f"\033[{_CODES[style]}m{text}\033[0m"


def rule() -> None:
    print(paint("grey", "─" * min(WIDTH, 100)))


@dataclass(frozen=True)
class Skill:
    name: str
    category: str
    subject: str
    path: Path
    description: str
    size: int

    @property
    def rel(self) -> str:
        return self.path.relative_to(ROOT).as_posix()


def _parse_frontmatter(raw: str) -> tuple[str, str]:
    lines = raw.splitlines()
    if not lines or lines[0].strip() != "---":
        return "", ""
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if end is None:
        return "", ""
    name = description = ""
    for line in lines[1:end]:
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key, value = key.strip(), value.strip()
        if key == "name":
            name = value
        elif key == "description":
            if value.startswith('"'):
                try:
                    description = json.loads(value)
                except json.JSONDecodeError:
                    description = value.strip('"')
            else:
                description = value
    return name, description


def load_skills() -> list[Skill]:
    """Index every skills/<category>/<subject>/<name>/SKILL.md package."""
    skills: list[Skill] = []
    for path in SKILLS.rglob("SKILL.md"):
        rel = path.relative_to(SKILLS)
        if len(rel.parts) != 4:
            continue  # _topics pages and anything outside the package layout
        try:
            with path.open("rb") as handle:
                raw = handle.read(FM_READ_BYTES).decode("utf-8", "replace")
            size = path.stat().st_size
        except OSError:
            continue
        name, description = _parse_frontmatter(raw)
        skills.append(
            Skill(
                name=name or rel.parts[2],
                category=rel.parts[0],
                subject=rel.parts[1],
                path=path,
                description=description,
                size=size,
            )
        )
    skills.sort(key=lambda s: s.name)
    return skills


def human(size: int) -> str:
    if size < 1024:
        return f"{size:,} B"
    kilobytes = size / 1024
    if kilobytes < 1024:
        return f"{kilobytes:,.1f} KB"
    return f"{kilobytes / 1024:,.1f} MB"


def field(label: str, text: str, column: int = 12) -> None:
    """Print `label  value`, wrapping the value with a hanging indent."""
    lines = textwrap.wrap(" ".join(text.split()), width=max(24, min(WIDTH, 100) - column)) or [""]
    print(f"  {paint('dim', f'{label:<9}')} {lines[0]}")
    for line in lines[1:]:
        print(" " * column + line)


# --------------------------------------------------------------------------- #
# discovery helpers
# --------------------------------------------------------------------------- #

def normalize_query(query: str) -> tuple[str, str]:
    """Return (leaf-name, normalized-path) for any accepted query form."""
    raw = query.strip().strip("`\"'")
    raw = raw.replace("\\", "/").lstrip("./")
    if raw.startswith("/"):
        raw = raw[1:]
    if raw.startswith("skills/"):
        raw = raw[len("skills/"):]
    for suffix in ("/SKILL.md", "SKILL.md"):
        if raw.endswith(suffix):
            raw = raw[: -len(suffix)]
            break
    raw = raw.strip("/")
    parts = [part for part in raw.split("/") if part]
    return (parts[-1] if parts else ""), "/".join(parts)


def resolve(skills: list[Skill], query: str) -> tuple[str, object]:
    """Resolve a query to ("skill", Skill) | ("repo", None) | ("candidates", [...])."""
    leaf, path = normalize_query(query)
    if not leaf or leaf.casefold() in REPO_ALIASES:
        return "repo", None
    exact = {skill.name: skill for skill in skills}
    if leaf in exact:
        return "skill", exact[leaf]
    if path:
        for skill in skills:
            if skill.rel.endswith(path + "/SKILL.md") or skill.rel == path:
                return "skill", skill
    lowered = leaf.casefold()
    scored: list[tuple[int, str, Skill]] = []
    for skill in skills:
        name = skill.name.casefold()
        if name.startswith(lowered):
            scored.append((0, name, skill))
        elif lowered in name:
            scored.append((1, name, skill))
    if len(scored) == 1:
        return "skill", scored[0][2]
    if scored:
        return "candidates", [item[2] for item in sorted(scored, key=lambda x: (x[0], x[1]))][:10]
    import difflib

    close = difflib.get_close_matches(leaf, list(exact), n=8, cutoff=0.6)
    return "candidates", [exact[name] for name in close]


# --------------------------------------------------------------------------- #
# views
# --------------------------------------------------------------------------- #

def overview(skills: list[Skill], note: str | None = None) -> None:
    if note:
        print(paint("yellow", "note") + " " + note)
        print()
    categories: dict[str, set[str]] = {}
    counts: dict[str, int] = {}
    for skill in skills:
        categories.setdefault(skill.category, set()).add(skill.subject)
        counts[skill.category] = counts.get(skill.category, 0) + 1
    subjects = sum(len(v) for v in categories.values())
    total = len(skills)
    print(paint("bold", "Agentic Skills"))
    print(
        paint("dim", f"{total:,} skills · {len(categories)} categories · {subjects} subjects")
    )
    print()
    print("  " + paint("dim", f"{'CATEGORY':<34}{'SUBJECTS':>9}{'SKILLS':>9}"))
    peak = max(counts.values()) if counts else 1
    for category, count in sorted(counts.items(), key=lambda item: -item[1]):
        bar = "█" * max(1, round(24 * count / peak))
        print(
            f"  {category:<34}{len(categories[category]):>9}{count:>9,}  "
            + paint("cyan", bar)
        )
    print("  " + paint("dim", f"{'Total':<34}{subjects:>9}{total:>9,}"))
    print()
    print(paint("bold", "Next"))
    for command, blurb in (
        ("skills list --page 1", f"browse all {total:,} skills, 40 at a time"),
        ("skills find <query>", "search names and descriptions"),
        ("skills show <name>", "read one skill in full"),
        ("skills cmd", "every command and flag"),
    ):
        print(f"  {paint('cyan', command):<34} {paint('dim', blurb)}")


def cmd_list(skills: list[Skill], args: argparse.Namespace) -> int:
    rows = skills
    if args.category:
        needle = args.category.casefold()
        rows = [s for s in rows if needle in s.category.casefold()]
    if args.subject:
        needle = args.subject.casefold()
        rows = [s for s in rows if needle in s.subject.casefold()]
    if args.sort == "category":
        rows = sorted(rows, key=lambda s: (s.category, s.subject, s.name))
    elif args.sort == "size":
        rows = sorted(rows, key=lambda s: -s.size)

    if args.json:
        payload = [{"name": s.name, "category": s.category, "subject": s.subject,
                    "path": s.rel, "description": s.description, "bytes": s.size} for s in rows]
        print(json.dumps(payload, indent=2))
        return 0

    limit = len(rows) if args.all else max(1, args.limit)
    pages = max(1, -(-len(rows) // limit))
    page = min(max(1, args.page), pages)
    start = (page - 1) * limit
    window = rows[start:start + limit]

    print(paint("bold", f"{len(rows):,} skills") + paint("dim", f" · page {page}/{pages}"))
    print()
    print("  " + paint("dim", f"{'#':>6}  {'SKILL':<52}{'CATEGORY':<26}{'SIZE':>9}"))
    for offset, skill in enumerate(window, start + 1):
        name = skill.name if len(skill.name) <= 50 else skill.name[:49] + "…"
        print(f"  {offset:>6}  {name:<52}{skill.category:<26}{human(skill.size):>9}")
    print()
    if pages > 1:
        hints = []
        if page > 1:
            hints.append(f"skills list --page {page - 1}")
        if page < pages:
            hints.append(f"skills list --page {page + 1}")
        print("  " + paint("dim", " · ".join(hints) + "   (or --all to print everything)"))
    print("  " + paint("dim", "skills show <name>   for the full instructions"))
    return 0


def cmd_find(skills: list[Skill], args: argparse.Namespace) -> int:
    query = " ".join(args.query).casefold()
    hits: list[tuple[int, Skill, str]] = []
    for skill in skills:
        name = skill.name.casefold()
        description = skill.description.casefold()
        if query in name:
            hits.append((0 if name.startswith(query) else 1, skill, "name"))
        elif query in description:
            hits.append((2, skill, "description"))
    hits.sort(key=lambda item: (item[0], item[1].name))
    if args.json:
        print(json.dumps([{"name": s.name, "matched": where, "path": s.rel,
                           "description": s.description} for _, s, where in hits[: args.limit]], indent=2))
        return 0 if hits else 3
    if not hits:
        print(paint("yellow", f"no match for {query!r}") + paint("dim", " · try skills find <broader term>"))
        return 3
    print(paint("bold", f"{len(hits):,} match{'es' if len(hits) != 1 else ''}")
          + paint("dim", f" for {query!r}"))
    print()
    for _, skill, where in hits[: args.limit]:
        tag = paint("dim", f"[{where[:4]}]")
        name = skill.name if len(skill.name) <= 54 else skill.name[:53] + "…"
        print(f"  {name:<56}{skill.category:<26}{tag}")
    if len(hits) > args.limit:
        print()
        print("  " + paint("dim", f"… {len(hits) - args.limit:,} more · raise --limit to see them"))
    print()
    print("  " + paint("dim", "skills show <name>   for the full instructions"))
    return 0


def _body(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="replace").splitlines()
    if text and text[0].strip() == "---":
        end = next((i for i in range(1, len(text)) if text[i].strip() == "---"), None)
        if end is not None:
            return "\n".join(text[end + 1:]).lstrip("\n")
    return "\n".join(text)


def cmd_show(skills: list[Skill], args: argparse.Namespace) -> int:
    query = " ".join(args.query)
    kind, value = resolve(skills, query)

    if kind == "repo":
        leaf, _ = normalize_query(query)
        overview(
            skills,
            note=(
                f"/skills/{leaf} is the repository, not a skill — showing the library overview.\n"
                f"  A single skill looks like: {paint('cyan', 'skills show aas-agent-quality-route-cost-threshold-rule-check')}"
            ),
        )
        return 0

    if kind == "candidates":
        print(paint("yellow", f"{query!r} does not resolve to a single skill"))
        print()
        if value:
            print("  " + paint("dim", "Closest matches"))
            for skill in value:
                print(f"  {paint('cyan', skill.name):<58}{skill.category}")
            print()
            print("  " + paint("dim", f"skills show {value[0].name}"))
        else:
            print("  " + paint("dim", "no close match · run skills find <query>"))
        return 4

    skill: Skill = value  # type: ignore[assignment]
    if args.json:
        print(json.dumps({
            "name": skill.name, "category": skill.category, "subject": skill.subject,
            "path": skill.rel, "description": skill.description, "bytes": skill.size,
            "body": _body(skill.path),
        }, indent=2))
        return 0

    print(paint("bold", skill.name))
    rule()
    description = " ".join(skill.description.split())
    trigger = description
    for marker in (". Success means", ". Use configured", " Success means"):
        if marker in description:
            trigger = description.split(marker)[0] + "."
            break
    if args.raw:
        print(skill.path.read_text(encoding="utf-8", errors="replace"), end="")
        return 0

    field("Category", f"{skill.category} › {skill.subject}")
    field("Package", skill.rel)
    field("Size", f"{human(skill.size)} · {len(description):,} character description")
    field("Trigger", trigger)
    print()
    body = _body(skill.path)
    if args.head:
        print("\n".join(body.splitlines()[: args.head]))
        print()
        print(paint("dim", f"… truncated at {args.head} lines · skills show {skill.name} --raw for the full file"))
    else:
        print(body.rstrip())
    return 0


def cmd_stats(skills: list[Skill]) -> int:
    categories: dict[str, int] = {}
    subjects: set[tuple[str, str]] = set()
    sizes = []
    for skill in skills:
        categories[skill.category] = categories.get(skill.category, 0) + 1
        subjects.add((skill.category, skill.subject))
        sizes.append(skill.size)
    sizes.sort()
    total_bytes = sum(sizes)
    print(paint("bold", "Library statistics"))
    rule()
    print(f"  {'skills':<18}{len(skills):>10,}")
    print(f"  {'categories':<18}{len(categories):>10,}")
    print(f"  {'subjects':<18}{len(subjects):>10,}")
    print(f"  {'library size':<18}{human(total_bytes):>10}")
    print(f"  {'median skill':<18}{human(sizes[len(sizes) // 2]):>10}")
    print(f"  {'largest skill':<18}{human(sizes[-1]):>10}")
    print(f"  {'smallest skill':<18}{human(sizes[0]):>10}")
    print()
    print("  " + paint("dim", f"{'CATEGORY':<34}{'SUBJECTS':>9}{'SKILLS':>9}{'SHARE':>8}"))
    per_category: dict[str, set[str]] = {}
    for skill in skills:
        per_category.setdefault(skill.category, set()).add(skill.subject)
    for category, count in sorted(categories.items(), key=lambda item: -item[1]):
        share = 100 * count / len(skills)
        print(f"  {category:<34}{len(per_category[category]):>9}{count:>9,}{share:>7.1f}%")
    return 0


def cmd_reference() -> int:
    print(paint("bold", "skills — command reference"))
    rule()
    rows = (
        ("/skills", "overview of all 15,860 skills"),
        ("/skills list", "every skill, paged (--page, --limit, --all)"),
        ("/skills show <query>", "one skill, in full"),
        ("/skills find <query>", "search names and descriptions"),
        ("/skills stats", "size and distribution statistics"),
        ("/skills cmd", "this reference"),
    )
    print("  " + paint("dim", f"{'COMMAND':<26}WHAT IT DOES"))
    for command, blurb in rows:
        print(f"  {paint('cyan', command):<26} {blurb}")
    print()
    print(paint("bold", "Query forms for show / find"))
    for form in (
        "aas-agent-quality-route-cost-threshold-rule-check",
        "/skills/<name>",
        "skills/<category>/<subject>/<name>",
        "skills/<category>/<subject>/<name>/SKILL.md",
        "/skills/try-skills            (repository alias → overview)",
    ):
        print("  " + paint("dim", form))
    print()
    print(paint("bold", "Global flags"))
    for flag, blurb in (
        ("--json", "machine-readable output (list, find, show)"),
        ("--no-color", "disable ANSI colour (honours NO_COLOR)"),
        ("--width N", "wrap width for descriptions"),
        ("-h, --help", "usage"),
        ("--version", "print the library version"),
    ):
        print(f"  {paint('cyan', flag):<26} {blurb}")
    print()
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip() if (ROOT / "VERSION").exists() else "unknown"
    print(paint("dim", f"  library v{version} · {SKILLS}"))
    return 0


# --------------------------------------------------------------------------- #
# entry point
# --------------------------------------------------------------------------- #

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="skills", add_help=False)
    sub = parser.add_subparsers(dest="cmd")
    listing = sub.add_parser("list", add_help=False)
    listing.add_argument("--page", type=int, default=1)
    listing.add_argument("--limit", type=int, default=40)
    listing.add_argument("--all", action="store_true")
    listing.add_argument("--category")
    listing.add_argument("--subject")
    listing.add_argument("--sort", choices=("name", "category", "size"), default="name")
    show = sub.add_parser("show", add_help=False)
    show.add_argument("query", nargs="+")
    show.add_argument("--head", type=int)
    show.add_argument("--raw", action="store_true")
    find = sub.add_parser("find", add_help=False)
    find.add_argument("query", nargs="+")
    find.add_argument("--limit", type=int, default=20)
    sub.add_parser("stats", add_help=False)
    sub.add_parser("cmd", add_help=False)
    return parser


def main(argv: list[str] | None = None) -> int:
    global COLOR, WIDTH
    argv = list(sys.argv[1:] if argv is None else argv)

    settings = {"json": False, "color": "auto", "width": None}
    rest: list[str] = []
    index = 0
    while index < len(argv):
        arg = argv[index]
        if arg == "--json":
            settings["json"] = True
        elif arg == "--no-color":
            settings["color"] = "never"
        elif arg.startswith("--color="):
            settings["color"] = arg.split("=", 1)[1]
        elif arg == "--color" and index + 1 < len(argv):
            index += 1
            settings["color"] = argv[index]
        elif arg.startswith("--width="):
            settings["width"] = arg.split("=", 1)[1]
        elif arg == "--width" and index + 1 < len(argv):
            index += 1
            settings["width"] = argv[index]
        elif arg in ("-h", "--help"):
            cmd_reference()
            return 0
        elif arg == "--version":
            version = (ROOT / "VERSION").read_text(encoding="utf-8").strip() if (ROOT / "VERSION").exists() else "unknown"
            print(f"skills {version}")
            return 0
        else:
            rest.append(arg)
        index += 1

    COLOR = sys.stdout.isatty() and os.environ.get("NO_COLOR") is None and settings["color"] != "never"
    if settings["color"] == "always":
        COLOR = True
    try:
        WIDTH = int(settings["width"]) if settings["width"] else (shutil.get_terminal_size((100, 24)).columns)
    except ValueError:
        WIDTH = 100
    WIDTH = max(60, min(WIDTH, 160))

    if not SKILLS.is_dir():
        print(paint("red", f"FAIL") + f" no skills directory at {SKILLS}")
        return 2

    skills = load_skills()
    if not skills:
        print(paint("red", "FAIL") + f" no SKILL.md packages found under {SKILLS}")
        return 2

    if not rest:
        if settings["json"]:
            print(json.dumps({"skills": len(skills), "path": str(SKILLS)}, indent=2))
            return 0
        overview(skills)
        return 0

    if rest[0] in ("cmd", "commands", "help"):
        return cmd_reference()

    # Slash-command friendly: `skills /skills/<name>` behaves like `show`.
    if rest[0].startswith("/"):
        args = build_parser().parse_known_args(["show", *rest])[0]
        args.json = settings["json"]
        return cmd_show(skills, args)

    parser = build_parser()
    args, extras = parser.parse_known_args(rest)
    if args.cmd is None:
        print(paint("red", "FAIL") + f" unknown command {rest[0]!r}")
        print("  " + paint("dim", "run skills cmd for the command reference"))
        return 2
    args.json = settings["json"]
    if extras:
        print("  " + paint("dim", f"ignored unknown argument(s): {' '.join(extras)}"))

    if args.cmd == "list":
        return cmd_list(skills, args)
    if args.cmd == "find":
        return cmd_find(skills, args)
    if args.cmd == "show":
        return cmd_show(skills, args)
    if args.cmd == "stats":
        return cmd_stats(skills)
    return 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BrokenPipeError:
        try:
            sys.stdout.close()
        finally:
            raise SystemExit(0)
