#!/usr/bin/env python3
"""Audit skill *content* quality. Read-only; never edits a SKILL.md file.

`validate_skills.py` checks structure (frontmatter, headings, links, coverage).
This tool checks the things structure cannot see: how much of each package is
shared boilerplate, whether sections are actually filled in, and whether the
same paragraph is repeated inside one file.

Findings are graded so the tool can be adopted without failing a build on
day one:

  ERROR  Broken content that should block a merge.
  WARN   Real quality debt worth fixing.
  INFO   Context for maintainers; not a defect.

Exit status is 1 when any ERROR is found, else 0. Pass --strict to also fail
on WARN.

Usage
-----
  python scripts/audit_skill_quality.py
  python scripts/audit_skill_quality.py --json > quality.json
  python scripts/audit_skill_quality.py --top 20 --show boilerplate
  python scripts/audit_skill_quality.py --strict
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
import json
import re
import sys

from validate_skills import ROOT, SKILLS_ROOT, discover_skills, parse_frontmatter

MIN_PARAGRAPH_CHARS = 120
DUPLICATE_MIN_CHARS = 120
BOILERPLATE_MIN_FILES = 1000
NOT_SPECIFIED = "Not specified in source skill"

# A section is "empty" when the text under its heading is only a placeholder.
PLACEHOLDER_RE = re.compile(r"not specified|none has been invented|no source example", re.I)
HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*#*\s*$")
FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})")


@dataclass
class Finding:
    level: str
    code: str
    message: str
    path: str
    detail: dict = field(default_factory=dict)

    def as_dict(self) -> dict:
        return {"level": self.level, "code": self.code, "path": self.path,
                "message": self.message, **({"detail": self.detail} if self.detail else {})}


def paragraphs(body: str) -> list[str]:
    """Blank-line separated prose blocks, normalised, without headings or code."""
    blocks: list[str] = []
    current: list[str] = []
    fence = False
    for line in body.splitlines():
        if FENCE_RE.match(line):
            fence = not fence
            continue
        if fence:
            continue
        if not line.strip():
            if current:
                blocks.append(" ".join(current))
                current = []
            continue
        if HEADING_RE.match(line):
            if current:
                blocks.append(" ".join(current))
                current = []
            continue
        current.append(line.strip())
    if current:
        blocks.append(" ".join(current))
    return [re.sub(r"\s+", " ", block).strip() for block in blocks if block.strip()]


def empty_sections(body: str) -> list[str]:
    """Headings whose entire content is a placeholder sentence."""
    lines = body.splitlines()
    empty: list[str] = []
    index = 0
    while index < len(lines):
        match = HEADING_RE.match(lines[index])
        if not match:
            index += 1
            continue
        depth = len(lines[index]) - len(lines[index].lstrip("#"))
        if depth < 2:  # the level-one title is not a section
            index += 1
            continue
        content: list[str] = []
        cursor = index + 1
        while cursor < len(lines):
            nxt = HEADING_RE.match(lines[cursor])
            if nxt and (len(lines[cursor]) - len(lines[cursor].lstrip("#"))) <= depth:
                break
            if lines[cursor].strip():
                content.append(lines[cursor].strip())
            cursor += 1
        text = " ".join(content)
        if text and len(text) < 200 and PLACEHOLDER_RE.search(text):
            empty.append(match.group(1))
        index = cursor
    return empty


def audit(paths: list[Path], boilerplate_min_files: int | None = None) -> tuple[list[Finding], dict]:
    """Return findings plus corpus statistics.

    `boilerplate_min_files` overrides the corpus-wide threshold; tests use a
    small value because they build a synthetic two- or three-file library.
    """
    threshold = BOILERPLATE_MIN_FILES if boilerplate_min_files is None else boilerplate_min_files
    bodies: dict[str, str] = {}
    descriptions: dict[str, str] = {}
    for path in paths:
        name, description, body, _ = parse_frontmatter(path)
        key = path.relative_to(ROOT).as_posix()
        bodies[key] = body
        descriptions[key] = description

    blocks_by_file = {rel: paragraphs(body) for rel, body in bodies.items()}
    owners: dict[str, set[str]] = defaultdict(set)
    for rel, blocks in blocks_by_file.items():
        for block in blocks:
            if len(block) >= MIN_PARAGRAPH_CHARS:
                owners[block].add(rel)
    boilerplate = {block for block, files in owners.items() if len(files) >= threshold}

    findings: list[Finding] = []
    total_bytes = sum(len(body.encode()) for body in bodies.values())
    boilerplate_bytes = 0
    boilerplate_heavy: list[tuple[float, str]] = []
    not_specified_files = 0
    empty_section_total = 0
    duplicate_total = 0
    duplicate_files = 0
    per_file_share: dict[str, float] = {}

    for rel, blocks in blocks_by_file.items():
        body = bodies[rel]
        size = len(body.encode()) or 1
        shared = sum(len(block) for block in blocks if block in boilerplate)
        boilerplate_bytes += shared
        share = shared / size
        per_file_share[rel] = share
        if share > 0.6:
            boilerplate_heavy.append((share, rel))

        counts = Counter(block for block in blocks if len(block) >= DUPLICATE_MIN_CHARS)
        repeats = {block: n for block, n in counts.items() if n > 1}
        if repeats:
            duplicate_files += 1
            extra = sum(n - 1 for n in repeats.values())
            duplicate_total += extra
            worst = max(repeats.items(), key=lambda item: item[1])
            findings.append(Finding(
                "WARN", "duplicate_paragraph",
                f"{extra} paragraph(s) repeated inside the same file ({worst[1]}× maximum)",
                rel, {"repeats": extra, "sample": worst[0][:120]},
            ))

        if NOT_SPECIFIED in body:
            not_specified_files += 1
            empty = empty_sections(body)
            empty_section_total += len(empty)
            findings.append(Finding(
                "INFO", "placeholder_sections",
                f"{len(empty)} section(s) carry only a placeholder: {', '.join(empty) or 'none'}",
                rel, {"sections": empty},
            ))

        if "</" in body and re.search(r"</?(?:script|iframe|object|embed)\b", body, re.I):
            findings.append(Finding(
                "ERROR", "unsafe_embedded_markup",
                "skill body embeds active HTML content", rel,
            ))

        description = descriptions[rel]
        if description and description.rstrip()[-1:] not in ".!?":
            findings.append(Finding(
                "WARN", "description_punctuation",
                "frontmatter description does not end with sentence punctuation", rel,
            ))

    share = boilerplate_bytes / total_bytes if total_bytes else 0.0
    stats = {
        "skills": len(bodies),
        "body_bytes": total_bytes,
        "boilerplate_paragraphs": len(boilerplate),
        "boilerplate_threshold": threshold,
        "boilerplate_share": round(share, 4),
        "boilerplate_heavy_files": len(boilerplate_heavy),
        "not_specified_files": not_specified_files,
        "not_specified_share": round(not_specified_files / len(bodies), 4) if bodies else 0.0,
        "empty_sections": empty_section_total,
        "duplicate_paragraphs": duplicate_total,
        "duplicate_files": duplicate_files,
        "largest_boilerplate": [
            {"path": rel, "share": round(value, 3)}
            for value, rel in sorted(boilerplate_heavy, reverse=True)[:10]
        ],
    }
    return findings, stats


def render(findings: list[Finding], stats: dict, top: int, show: str | None) -> None:
    print("Content quality audit")
    print("=" * 72)
    print(f"  skills scanned          {stats['skills']:>10,}")
    print(f"  body bytes              {stats['body_bytes']:>10,}")
    print(f"  shared boilerplate      {stats['boilerplate_share']:>9.1%}   "
          f"({stats['boilerplate_paragraphs']} paragraphs in ≥{stats['boilerplate_threshold']:,} files)")
    print(f"  placeholder-only skills {stats['not_specified_files']:>10,}   "
          f"({stats['not_specified_share']:.1%}) · {stats['empty_sections']:,} empty sections")
    print(f"  duplicate paragraphs    {stats['duplicate_paragraphs']:>10,}   "
          f"across {stats['duplicate_files']:,} files")
    print(f"  files >60% boilerplate  {stats['boilerplate_heavy_files']:>10,}")

    levels = Counter(finding.level for finding in findings)
    print()
    print(f"Findings: {levels.get('ERROR', 0)} error · {levels.get('WARN', 0)} warn · "
          f"{levels.get('INFO', 0)} info")
    for level in ("ERROR", "WARN", "INFO"):
        selected = [finding for finding in findings if finding.level == level]
        if show and show.upper() != level:
            continue
        if not selected:
            continue
        print()
        print(f"{level}")
        for finding in selected[:top]:
            print(f"  {finding.path}")
            print(f"      {finding.message}")
        if len(selected) > top:
            print(f"  … {len(selected) - top:,} more {level.lower()} finding(s)")
    if stats["largest_boilerplate"]:
        print()
        print("Most boilerplate-heavy packages")
        for row in stats["largest_boilerplate"][:5]:
            print(f"  {row['share']:.0%}  {row['path']}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--json", action="store_true", help="emit machine-readable findings")
    parser.add_argument("--top", type=int, default=8, help="findings shown per level (default 8)")
    parser.add_argument("--show", choices=("error", "warn", "info"),
                        help="only print one finding level")
    parser.add_argument("--strict", action="store_true", help="also fail on WARN findings")
    parser.add_argument("--summary", action="store_true", help="statistics only, no findings")
    args = parser.parse_args()

    paths = discover_skills(SKILLS_ROOT)
    if not paths:
        print(f"FAIL: no skills found under {SKILLS_ROOT}")
        return 2
    findings, stats = audit(paths)

    if args.json:
        print(json.dumps({"stats": stats, "findings": [f.as_dict() for f in findings]}, indent=2))
    else:
        if not args.summary:
            render(findings, stats, args.top, args.show)
        else:
            print(json.dumps(stats, indent=2))

    has_error = any(f.level == "ERROR" for f in findings)
    has_warn = any(f.level == "WARN" for f in findings)
    if has_error or (args.strict and has_warn):
        if not args.json:
            print()
            print("Audit failed: resolve ERROR"
                  + ("/WARN" if args.strict else "") + " findings.")
        return 1
    if not args.json:
        print()
        print("Audit passed: no ERROR findings"
              + (" or WARN findings (--strict)." if args.strict else " (use --strict to fail on WARN)."))
    return 0


if __name__ == "__main__":
    sys.exit(main())
