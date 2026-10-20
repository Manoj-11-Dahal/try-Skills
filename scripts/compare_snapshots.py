#!/usr/bin/env python3
"""Compare the current skill library against an earlier snapshot.

The repository ships dated snapshots under `backups/`, and published reports
describe older states. Before changing the corpus, compare against one of them
so a regeneration cannot silently regress content quality.

A source may be a `.tar.gz` archive of a `skills/` tree or an unpacked
directory. Packages are matched by skill directory name, so a category or
subject migration does not count as a removal.

Reported per snapshot:

  packages    matched / added / removed
  size        bytes before and after, and the delta
  repetition  duplicate paragraphs inside a single package
  placeholders  packages carrying "Not specified" markers
  sections    H2 sections that existed before and are absent now

Exit status is 1 when `--fail-on-regression` is given and the snapshot regressed,
meaning packages were removed, or in-file repetition or placeholder sections
increased.

Usage
-----
  python scripts/compare_snapshots.py backups/before-template-reformat-2026-09-29.tar.gz
  python scripts/compare_snapshots.py backups/before-creator-template-2026-09-29.tar.gz --json
  python scripts/compare_snapshots.py /path/to/old/skills --fail-on-regression
"""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
import json
import re
import sys
import tarfile

from validate_skills import SKILLS_ROOT

MIN_PARAGRAPH_CHARS = 120
NOT_SPECIFIED = "Not specified in source skill"
BODY_SPLIT = "---"
HEADING = re.compile(r"^##\s+(.+?)\s*#*\s*$", re.M)
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})")


PLACEHOLDER = re.compile(r"not specified|none has been invented|no source example", re.I)
SECTION = re.compile(r"^##\s+(.+?)\s*$", re.M)


def section_map(body: str) -> dict[str, str]:
    """Heading -> normalised text beneath it, stopping at the next H2."""
    found: dict[str, str] = {}
    matches = list(SECTION.finditer(body))
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        # Keep line structure: collapsing it would merge a sub-heading into the
        # prose that follows, and the heading filter would then drop both.
        text = "\n".join(re.sub(r"[ \t]+", " ", line).strip()
                          for line in body[match.end():end].splitlines()).strip()
        found[match.group(1).strip()] = text
    return found


def normalize_section(text: str) -> str:
    """Section prose with markdown headings stripped, for cross-file comparison.

    Sub-headings are re-nested by reformatters, so comparing them produces false
    "content lost" reports. Only the prose is compared.
    """
    lines = [line for line in text.splitlines() if not line.lstrip().startswith("#")]
    return re.sub(r"\s+", " ", " ".join(lines)).strip()


def is_placeholder(text: str) -> bool:
    return not text or (len(text) < 240 and bool(PLACEHOLDER.search(text)))


@dataclass
class Package:
    name: str
    text: str

    @property
    def body(self) -> str:
        parts = self.text.split(BODY_SPLIT, 2)
        return parts[2] if len(parts) == 3 else self.text

    @property
    def paragraphs(self) -> list[str]:
        blocks, current, fence = [], [], False
        for line in self.body.splitlines():
            if FENCE.match(line):
                fence = not fence
                continue
            if fence:
                continue
            if not line.strip() or HEADING.match(line):
                if current:
                    blocks.append(re.sub(r"\s+", " ", " ".join(current)).strip())
                    current = []
                continue
            current.append(line.strip())
        if current:
            blocks.append(re.sub(r"\s+", " ", " ".join(current)).strip())
        return [block for block in blocks if len(block) >= MIN_PARAGRAPH_CHARS]

    @property
    def duplicate_chars(self) -> int:
        counts = Counter(self.paragraphs)
        return sum(len(text) * (n - 1) for text, n in counts.items() if n > 1)

    @property
    def sections(self) -> set[str]:
        return {match.strip() for match in HEADING.findall(self.body)}

    @property
    def section_text(self) -> dict[str, str]:
        return section_map(self.body)


def load_directory(root: Path) -> dict[str, Package]:
    packages: dict[str, Package] = {}
    for path in sorted(root.rglob("SKILL.md")):
        try:
            packages[path.parent.name] = Package(path.parent.name, path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError) as exc:
            print(f"WARN: cannot read {path}: {exc}", file=sys.stderr)
    return packages


def load_archive(path: Path) -> dict[str, Package]:
    packages: dict[str, Package] = {}
    try:
        with tarfile.open(path, "r:gz") as archive:
            for member in archive.getmembers():
                if not member.isfile() or not member.name.endswith("/SKILL.md"):
                    continue
                handle = archive.extractfile(member)
                if handle is None:
                    continue
                name = Path(member.name).parent.name
                packages[name] = Package(name, handle.read().decode("utf-8", "replace"))
    except (OSError, tarfile.TarError, UnicodeError) as exc:
        raise SystemExit(f"FAIL: cannot read archive {path}: {exc}") from exc
    return packages


def load(path: Path) -> dict[str, Package]:
    if path.is_file() and path.name.endswith((".tar.gz", ".tgz")):
        return load_archive(path)
    if path.is_dir():
        return load_directory(path)
    raise SystemExit(f"FAIL: {path} is neither a directory nor a .tar.gz snapshot")


def metrics(packages: dict[str, Package]) -> dict:
    duplicates = sum(package.duplicate_chars for package in packages.values())
    duplicated_files = sum(1 for package in packages.values() if package.duplicate_chars)
    return {
        "packages": len(packages),
        "bytes": sum(len(package.text) for package in packages.values()),
        "duplicate_chars": duplicates,
        "duplicated_files": duplicated_files,
        "placeholder_files": sum(1 for package in packages.values() if NOT_SPECIFIED in package.text),
    }


def compare(old: dict[str, Package], new: dict[str, Package]) -> dict:
    matched = sorted(set(old) & set(new))
    removed = sorted(set(old) - set(new))
    added = sorted(set(new) - set(old))

    lost_sections: Counter[str] = Counter()
    dropped_placeholders: Counter[str] = Counter()
    renamed_sections: Counter[str] = Counter()
    content_losses: list[dict] = []
    grew: list[tuple[int, str]] = []
    for name in matched:
        before, after = old[name], new[name]
        old_text, new_text = before.section_text, after.section_text
        flat_new = re.sub(r"\s+", " ", after.body)
        for heading in sorted(before.sections - after.sections):
            raw = old_text.get(heading, "")
            text = normalize_section(raw)
            if is_placeholder(raw):
                dropped_placeholders[heading] += 1
            elif text and (text[:100] in flat_new
                           or any(text[i:i + 60] in flat_new
                                  for i in range(0, max(1, len(text) - 60), 40))):
                renamed_sections[heading] += 1
            else:
                lost_sections[heading] += 1
                content_losses.append({"path": name, "heading": heading})
        delta = len(after.text) - len(before.text)
        if delta:
            grew.append((delta, name))

    before = metrics({name: old[name] for name in matched})
    after = metrics({name: new[name] for name in matched})
    return {
        "matched": len(matched),
        "added": added,
        "removed": removed,
        "before": before,
        "after": after,
        "lost_sections": lost_sections.most_common(10),
        "dropped_placeholder_sections": dropped_placeholders.most_common(10),
        "renamed_sections": renamed_sections.most_common(10),
        "content_losses": content_losses,
        "largest_growth": sorted(grew, reverse=True)[:5],
        "large_shrinks": sorted(grew)[:5],
    }


def regressions(result: dict) -> list[str]:
    """Changes that make the library worse than the snapshot it is compared to."""
    issues: list[str] = []
    before, after = result["before"], result["after"]
    if result["removed"]:
        issues.append(f"{len(result['removed'])} package(s) present before are missing now")
    if after["duplicate_chars"] > before["duplicate_chars"]:
        issues.append(
            f"in-file repetition grew by {after['duplicate_chars'] - before['duplicate_chars']:,} chars"
        )
    if after["placeholder_files"] > before["placeholder_files"]:
        issues.append(
            f"placeholder packages grew by {after['placeholder_files'] - before['placeholder_files']:,}"
        )
    if result.get("content_losses"):
        issues.append(f"{len(result['content_losses'])} section(s) lost substantive content")
    if after["bytes"] > before["bytes"] * 1.25 and before["bytes"]:
        issues.append(
            f"body bytes grew {(after['bytes'] / before['bytes'] - 1):.0%} with no coverage requirement"
        )
    return issues


def render(source: Path, result: dict) -> None:
    before, after = result["before"], result["after"]
    print(f"Snapshot compared: {source}")
    print("=" * 72)
    print(f"  matched packages        {result['matched']:>10,}")
    print(f"  added since snapshot    {len(result['added']):>10,}")
    print(f"  removed since snapshot  {len(result['removed']):>10,}")
    print()
    print(f"  {'':<26}{'SNAPSHOT':>12}{'CURRENT':>12}")
    rows = (
        ("body bytes", "bytes"),
        ("duplicate chars", "duplicate_chars"),
        ("files with repeats", "duplicated_files"),
        ("placeholder packages", "placeholder_files"),
    )
    for label, key in rows:
        print(f"  {label:<26}{before[key]:>12,}{after[key]:>12,}")
    if before["bytes"]:
        print(f"  {'body size change':<26}{'':>12}{(after['bytes'] / before['bytes'] - 1):>11.1%}")
    if before["duplicate_chars"] != after["duplicate_chars"]:
        delta = after["duplicate_chars"] - before["duplicate_chars"]
        print(f"  {'repetition change':<26}{'':>12}{delta:>+12,}")

    if result.get("content_losses"):
        print()
        print("Sections whose text is genuinely gone")
        for heading, count in result["lost_sections"]:
            print(f"  {count:>6,}  ## {heading}")
    if result.get("renamed_sections"):
        print()
        print("Sections re-titled or re-nested; text preserved")
        for heading, count in result["renamed_sections"][:6]:
            print(f"  {count:>6,}  ## {heading}")
    if result.get("dropped_placeholder_sections"):
        print()
        print("Empty placeholder sections removed (an improvement)")
        for heading, count in result["dropped_placeholder_sections"][:6]:
            print(f"  {count:>6,}  ## {heading}")

    if result["largest_growth"]:
        print()
        print("Largest single-package growth")
        for delta, name in result["largest_growth"][:3]:
            print(f"  {delta:>+8,} chars  {name}")

    issues = regressions(result)
    print()
    if issues:
        print("REGRESSIONS")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("No regression against this snapshot.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("snapshot", type=Path, help="archive (.tar.gz) or unpacked skills/ directory")
    parser.add_argument("--new", type=Path, default=SKILLS_ROOT, help="current tree (default: skills/)")
    parser.add_argument("--json", action="store_true", help="emit a machine-readable comparison")
    parser.add_argument("--fail-on-regression", action="store_true",
                        help="exit 1 when the current tree is worse than the snapshot")
    parser.add_argument("--quiet", action="store_true", help="only print the verdict")
    args = parser.parse_args()

    old = load(args.snapshot)
    new = load(args.new)
    if not old:
        raise SystemExit(f"FAIL: no SKILL.md packages in {args.snapshot}")

    result = compare(old, new)
    issues = regressions(result)
    if args.json:
        payload = {key: value for key, value in result.items()
                   if key not in ("lost_sections", "dropped_placeholder_sections",
                                  "renamed_sections", "content_losses")}
        for key in ("lost_sections", "dropped_placeholder_sections", "renamed_sections"):
            payload[key] = [{"heading": heading, "packages": count}
                            for heading, count in result[key]]
        payload["content_losses"] = result["content_losses"][:50]
        payload["regressions"] = issues
        payload["snapshot"] = str(args.snapshot)
        print(json.dumps(payload, indent=2))
    elif args.quiet:
        print(f"{len(issues)} regression(s)" if issues else "no regression")
    else:
        render(args.snapshot, result)

    if issues and args.fail_on_regression:
        if not args.json:
            print()
            print("Comparison failed: --fail-on-regression and the current tree regressed.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
