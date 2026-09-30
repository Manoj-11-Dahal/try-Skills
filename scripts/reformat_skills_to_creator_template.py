#!/usr/bin/env python3
"""Reformat the local skill corpus to the approved Creator Prompt structure.

Read-only by default. The original skill corpus is read from its verified
pre-template archive; --apply additionally verifies that the current corpus
matches its separate rollback archive before replacing any SKILL.md file.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import sys
import tarfile
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / "skills"
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import reformat_skills_to_template as source_parser  # noqa: E402
from validate_skills import content_units  # noqa: E402

SOURCE_BACKUP_DEFAULT = ROOT / "backups" / "before-template-reformat-2026-09-29.tar.gz"
ROLLBACK_BACKUP_DEFAULT = ROOT / "backups" / "before-creator-template-2026-09-29.tar.gz"

REQUIRED_SECTIONS = [
    "Overview",
    "When to Use",
    "Inputs",
    "Instructions",
    "Decision Rules",
    "Output Format",
    "Validation Checklist",
    "Examples",
    "Success Criteria",
]
OPTIONAL_ORDER = [
    "Scope",
    "Tools and Resources",
    "Edge Cases and Recovery",
    "Stop Conditions",
    "Common Pitfalls",
    "Related Skills",
]
SECTION_ORDER = [
    "Overview",
    "When to Use",
    "Scope",
    "Inputs",
    "Instructions",
    "Decision Rules",
    "Tools and Resources",
    "Output Format",
    "Validation Checklist",
    "Edge Cases and Recovery",
    "Stop Conditions",
    "Common Pitfalls",
    "Examples",
    "Success Criteria",
    "Related Skills",
]
MISSING = "Not specified in source skill."
MISSING_EXAMPLE = (
    "Not specified in source skill. The original provided no input/output example, "
    "and none has been invented."
)

SOURCE_ROUTES = {
    "overview": "overview",
    "purpose": "overview",
    "introduction": "overview",
    "when to use": "when",
    "inputs": "inputs",
    "inputs and boundaries": "inputs",
    "procedure": "instructions",
    "workflow": "instructions",
    "iterative workflow": "instructions",
    "focused procedure": "instructions",
    "maintenance rules": "instructions",
    "loop contract": "scope",
    "guardrails": "scope",
    "safety and privacy": "scope",
    "safety boundaries": "scope",
    "safety and respect": "scope",
    "review boundaries": "scope",
    "approval and safety boundaries": "scope",
    "audit guardrails": "scope",
    "context hygiene": "scope",
    "evaluation guardrails": "scope",
    "research guardrails": "scope",
    "planning guardrails": "scope",
    "safety rules": "scope",
    "safety and stop conditions": "stop",
    "stop conditions": "stop",
    "stopping rules": "stop",
    "red flags": "stop",
    "topic provenance": "tools",
    "tool map": "tools",
    "references": "tools",
    "acceptance": "success",
    "acceptance evidence": "success",
    "safety and acceptance": "success",
    "domain checks": "validation",
    "apple-platform checks": "validation",
    "game-specific checks": "validation",
    "kubernetes checks": "validation",
    "browser-specific checks": "validation",
    "platform-specific checks": "validation",
    "medical-imaging-specific checks": "validation",
    "security-specific checks": "validation",
    "safety and verification": "validation",
    "output": "output",
    "output and acceptance": "output",
    "adr shape": "output",
    "finding standard": "output",
    "go/no-go output": "output",
    "specification shape": "output",
    "finding format": "output",
    "checkpoint template": "output",
    "common failure modes": "pitfalls",
    "retry guardrails": "edge",
    "coordination risks": "edge",
    "examples": "examples",
    "test cases": "validation",
    "related skills": "related",
    "decision rules": "decisions",
    "edge cases and recovery": "edge",
    "tools and resources": "tools",
    "success criteria": "success",
    "validation checklist": "validation",
    "common pitfalls": "pitfalls",
}

BOUNDARY_RE = re.compile(
    r"\b(?:do\s+not|don['’]t|never|must\s+not|not\s+authorized|"
    r"without\s+explicit\s+(?:authorization|approval)|does\s+not\s+grant|"
    r"does\s+not\s+authorize|not\s+a\s+substitute|does\s+not\s+replace|cannot)\b",
    re.I,
)
STOP_RE = re.compile(
    r"\b(?:stop(?:ping)?|exit\s+conditions?|exit\s+when|halt|pause|"
    r"escalat(?:e|ion|ed)|ask\s+when|ask\s+rather\s+than|do\s+not\s+continue)\b",
    re.I,
)
EDGE_RE = re.compile(
    r"\b(?:boundary\s+cases?|fail(?:ure|ures|ed|ing)?|errors?|exceptions?|"
    r"recover(?:y|ies|ing)?|retries?|fallbacks?|malformed|partial\s+failure|"
    r"timeouts?|outages?|denied|invalid|missing\s+(?:data|inputs?)|regressions?|"
    r"repeated\s+(?:calls?|actions?|failures?))\b",
    re.I,
)
DECISION_RE = re.compile(r"\b(?:if|unless|otherwise|only\s+when|only\s+if|when)\b", re.I)
LINK_RE = re.compile(r"!??\[[^\]]*\]\(([^)]+)\)")


def _route(title: str) -> str | None:
    key = re.sub(r"\s+", " ", title.strip().rstrip(":")).casefold()
    if key in SOURCE_ROUTES:
        return SOURCE_ROUTES[key]
    if "related skill" in key:
        return "related"
    if "example" in key:
        return "examples"
    if "test" in key or "checklist" in key or "validation" in key:
        return "validation"
    if "decision" in key or "routing" in key:
        return "decisions"
    if "input" in key or "prerequisite" in key:
        return "inputs"
    if "stop" in key or "stopping" in key:
        return "stop"
    if "edge" in key or "recovery" in key or "retry" in key or "coordination risk" in key:
        return "edge"
    if "pitfall" in key or "failure mode" in key:
        return "pitfalls"
    if "tool" in key or "resource" in key or "reference" in key or "provenance" in key:
        return "tools"
    if "output" in key or "format" in key or "shape" in key or "template" in key or "finding" in key:
        return "output"
    if "acceptance" in key or "success" in key or "quality" in key:
        return "success"
    if "check" in key or "verification" in key:
        return "validation"
    if "scope" in key or "guardrail" in key or "boundary" in key or "safety" in key or "privacy" in key:
        return "scope"
    if "procedure" in key or "workflow" in key or "instruction" in key or "step" in key or "process" in key:
        return "instructions"
    if "when to use" in key or "activation" in key:
        return "when"
    if "overview" in key or "purpose" in key or "summary" in key:
        return "overview"
    return None


def _source_block(section) -> str:
    content = section.content.strip("\r\n")
    if not content:
        content = MISSING
    return f"### Preserved source section: {section.title}\n\n{content}"


def _source_blocks(sections: Iterable) -> str:
    return "\n\n".join(_source_block(section) for section in sections)


def _matched_lines(sections: Iterable, pattern: re.Pattern[str], *, excluded_titles: set[str] | None = None,
                   excluded_routes: set[str] | None = None) -> list[tuple[str, list[str]]]:
    excluded_titles = {item.casefold() for item in (excluded_titles or set())}
    excluded_routes = excluded_routes or set()
    result: list[tuple[str, list[str]]] = []
    for section in sections:
        if section.title.casefold() in excluded_titles or _route(section.title) in excluded_routes:
            continue
        lines: list[str] = []
        seen: set[str] = set()
        for line in section.content.splitlines():
            if pattern.search(line):
                key = re.sub(r"\s+", " ", line.strip()).casefold()
                if key and key not in seen:
                    seen.add(key)
                    lines.append(line.rstrip())
        if lines:
            result.append((section.title, lines))
    return result


def _derived_groups(groups: Iterable[tuple[str, list[str]]], label: str) -> str:
    return "\n\n".join(
        f"### {label}: {title}\n\n" + "\n".join(lines)
        for title, lines in groups
    )


def _loop_fields(sections: Iterable) -> tuple[str | None, str | None, str | None]:
    loop_text = "\n".join(
        section.content for section in sections if section.title.casefold() == "loop contract"
    )
    if not loop_text:
        return None, None, None
    return (
        source_parser._field(loop_text, "Artifact"),
        source_parser._field(loop_text, "Feedback signal"),
        source_parser._field(loop_text, "Exit"),
    )


def _check_items(sections: Iterable) -> list[str]:
    items: list[str] = []
    for section in sections:
        for line in section.content.splitlines():
            match = re.match(r"^\s*(?:[-*+]\s+|\d+[.)]\s+)(.+?)\s*$", line)
            if match:
                item = match.group(1).strip()
                if item.startswith(("[ ] ", "[x] ", "[X] ")):
                    item = item[4:].strip()
                if item:
                    items.append(item)
    unique: list[str] = []
    seen: set[str] = set()
    for item in items:
        key = re.sub(r"\s+", " ", item).casefold()
        if key not in seen:
            seen.add(key)
            unique.append(item)
    return unique


def _checkboxes(items: Iterable[str]) -> str:
    return "\n".join(f"- [ ] {item}" for item in items)


def _render(skill) -> tuple[str, set[str], list[str]]:
    trigger, action, description = source_parser._description_parts(skill.description, skill.title)
    groups: dict[str, list] = {
        key: [] for key in {
            "overview", "when", "inputs", "instructions", "decisions", "scope", "tools",
            "output", "validation", "edge", "stop", "pitfalls", "examples", "success", "related",
        }
    }
    unknown: set[str] = set()
    for section in skill.sections:
        target = _route(section.title)
        if target is None or target not in groups:
            unknown.add(section.title)
        else:
            groups[target].append(section)

    artifact, feedback, exit_condition = _loop_fields(skill.sections)

    overview_parts = [
        f"This skill applies when {trigger}. Its intended outcome is to {action.rstrip('.!? ')}."
    ]
    if groups["overview"]:
        overview_parts.append(_source_blocks(groups["overview"]))
    if skill.opening.strip():
        overview_parts.append("### Preserved opening content\n\n" + skill.opening.strip("\r\n"))

    when_content = _source_blocks(groups["when"]) if groups["when"] else MISSING

    # Keep source-defined rules in the required decision section without
    # synthesizing conditions or actions.
    decision_lines = _matched_lines(
        skill.sections,
        DECISION_RE,
        excluded_titles={"When to Use"},
        excluded_routes={"decisions"},
    )
    decision_parts: list[str] = []
    if groups["decisions"]:
        decision_parts.append(_source_blocks(groups["decisions"]))
    if decision_lines:
        decision_parts.append(
            "The following source conditional guidance is preserved verbatim; no unstated action is inferred."
        )
        decision_parts.append(_derived_groups(decision_lines, "Source conditional guidance from"))
    decisions_content = "\n\n".join(decision_parts) if decision_parts else MISSING

    if groups["inputs"]:
        inputs_parts = [
            "**Required:** See the preserved source input guidance below.\n\n"
            f"**Optional:** {MISSING}\n\n**Prerequisites:** {MISSING}",
            _source_blocks(groups["inputs"]),
        ]
    else:
        inputs_parts = [
            f"**Required:** {MISSING}\n\n**Optional:** {MISSING}\n\n**Prerequisites:** {MISSING}",
            "No dedicated input list was found in the source; check the preserved procedure for task-specific prerequisites.",
        ]
    inputs_content = "\n\n".join(inputs_parts)

    instructions_content = _source_blocks(groups["instructions"]) if groups["instructions"] else MISSING

    output_parts: list[str] = []
    if artifact:
        output_parts.append(f"**Artifact (from source Loop Contract):** {artifact}")
    if groups["output"]:
        output_parts.append(_source_blocks(groups["output"]))
    output_content = "\n\n".join(output_parts) if output_parts else MISSING

    output_acceptance = [
        section for section in groups["output"] if "acceptance" in section.title.casefold()
    ]
    success_parts: list[str] = []
    if feedback:
        success_parts.append(f"**Success signal (from source Loop Contract):** {feedback}")
    if groups["success"]:
        success_parts.append(_source_blocks(groups["success"]))
    if output_acceptance:
        success_parts.extend(
            f"### Acceptance criteria from source: {section.title}\n\n{section.content.strip()}"
            for section in output_acceptance
        )
    success_content = "\n\n".join(success_parts) if success_parts else MISSING

    validation_parts: list[str] = []
    if groups["validation"]:
        validation_parts.append(_source_blocks(groups["validation"]))
    check_sources = groups["validation"] + groups["success"] + output_acceptance
    items = _check_items(check_sources)
    if items:
        validation_parts.append(
            "**Unchecked checklist derived from source criteria (not test evidence):**\n\n"
            + _checkboxes(items)
        )
    elif check_sources or feedback:
        validation_parts.append("- [ ] Verify the source-defined success criteria above.")
    if not validation_parts:
        validation_parts.append(MISSING)
    validation_content = "\n\n".join(validation_parts)

    examples_content = (
        _source_blocks(groups["examples"])
        if groups["examples"]
        else MISSING_EXAMPLE
    )

    # Optional sections are included only where original sections or explicit
    # source statements support them.
    boundary_lines = _matched_lines(skill.sections, BOUNDARY_RE, excluded_routes={"scope"})
    boundary_source_titles = {
        section.title.casefold()
        for section in skill.sections
        if re.search(r"guardrail|safety|boundary|privacy|review", section.title, re.I)
    }
    scope_parts: list[str] = []
    if groups["scope"] or boundary_lines:
        if groups["scope"] or boundary_lines:
            has_boundaries = bool(boundary_lines or boundary_source_titles)
            does_not = (
                "See the preserved source boundaries below and under Stop Conditions."
                if has_boundaries
                else MISSING
            )
            scope_parts.append(
                "**Does:** Follow the task boundary stated under When to Use and Instructions.\n\n"
                f"**Does not:** {does_not}"
            )
        if groups["scope"]:
            scope_parts.append(_source_blocks(groups["scope"]))
        if boundary_lines:
            scope_parts.append(_derived_groups(boundary_lines, "Source boundary statements from"))

    tools_parts: list[str] = []
    if groups["tools"]:
        has_tool_map = any(section.title.casefold() == "tool map" for section in groups["tools"])
        if has_tool_map:
            tools_parts.append(
                "**Use:** See the preserved Tool Map below.\n\n"
                "**Do not use:** See source boundaries under Scope and Stop Conditions.\n\n"
                f"**Fallback:** {MISSING}"
            )
        tools_parts.append(_source_blocks(groups["tools"]))

    edge_lines = _matched_lines(
        skill.sections,
        EDGE_RE,
        excluded_titles={"When to Use"},
        excluded_routes={"edge"},
    )
    edge_parts: list[str] = []
    if groups["edge"]:
        edge_parts.append(_source_blocks(groups["edge"]))
    if edge_lines:
        edge_parts.append(_derived_groups(edge_lines, "Source edge/failure guidance from"))

    stop_lines = _matched_lines(
        skill.sections,
        STOP_RE,
        excluded_titles={"Loop Contract"},
        excluded_routes={"stop"},
    )
    stop_parts: list[str] = []
    if groups["stop"]:
        stop_parts.append(_source_blocks(groups["stop"]))
    if exit_condition:
        stop_parts.append(f"**Exit condition (from source Loop Contract):** {exit_condition}")
    if stop_lines:
        stop_parts.append(_derived_groups(stop_lines, "Source stop-related guidance from"))

    pitfalls_content = _source_blocks(groups["pitfalls"]) if groups["pitfalls"] else ""
    related_content = _source_blocks(groups["related"]) if groups["related"] else ""

    contents = {
        "Overview": "\n\n".join(overview_parts),
        "When to Use": when_content,
        "Inputs": inputs_content,
        "Instructions": instructions_content,
        "Decision Rules": decisions_content,
        "Output Format": output_content,
        "Validation Checklist": validation_content,
        "Examples": examples_content,
        "Success Criteria": success_content,
    }
    optional_content = {
        "Scope": "\n\n".join(scope_parts),
        "Tools and Resources": "\n\n".join(tools_parts),
        "Edge Cases and Recovery": "\n\n".join(edge_parts),
        "Stop Conditions": "\n\n".join(stop_parts),
        "Common Pitfalls": pitfalls_content,
        "Related Skills": related_content,
    }

    ordered_sections = ["Overview", "When to Use"]
    if optional_content["Scope"]:
        ordered_sections.append("Scope")
    ordered_sections.extend(["Inputs", "Instructions", "Decision Rules"])
    if optional_content["Tools and Resources"]:
        ordered_sections.append("Tools and Resources")
    ordered_sections.extend(["Output Format", "Validation Checklist"])
    for heading in ["Edge Cases and Recovery", "Stop Conditions", "Common Pitfalls"]:
        if optional_content[heading]:
            ordered_sections.append(heading)
    ordered_sections.extend(["Examples", "Success Criteria"])
    if optional_content["Related Skills"]:
        ordered_sections.append("Related Skills")

    body_lines = [f"# {skill.title}"]
    for heading in ordered_sections:
        content = contents.get(heading, optional_content.get(heading, "")).strip("\r\n")
        body_lines.extend(["", f"## {heading}", "", content])
    body = "\n".join(body_lines).rstrip() + "\n"
    frontmatter = (
        "---\n"
        f"name: {skill.name}\n"
        f"description: {json.dumps(description, ensure_ascii=False)}\n"
        "---\n"
    )
    return frontmatter + "\n" + body, unknown, ordered_sections


def _validate_output(path: Path, skill, rendered: str, unknown: set[str], headings: list[str]) -> list[str]:
    errors: list[str] = []
    try:
        name, description, body = source_parser._parse_frontmatter(rendered, path)
    except Exception as exc:
        return [f"frontmatter parse error: {exc}"]
    if name != skill.name:
        errors.append("frontmatter skill name changed")
    if len(description) > 1024:
        errors.append(f"description too long: {len(description)} characters")
    units = content_units(description)
    if units < 40:
        errors.append(f"description has {units} content units; minimum is 40")
    top = re.findall(r"^##\s+(.+?)\s*$", body, re.M)
    if top != headings:
        errors.append("rendered section headings differ from planned order")
    if any(heading not in top for heading in REQUIRED_SECTIONS):
        errors.append("one or more required sections are missing")
    if len([item for item in top if item == "Examples"]) != 1:
        errors.append("Examples section is missing or duplicated")
    all_headings = re.findall(r"^#{1,6}\s+(.+?)\s*#*\s*$", body, re.M)
    normalized = [item.strip().casefold() for item in all_headings]
    if len(normalized) != len(set(normalized)):
        dupes = sorted({item for item in normalized if normalized.count(item) > 1})
        errors.append(f"duplicate headings: {dupes[:8]}")
    if sum(1 for line in body.splitlines() if re.match(r"^#\s+\S", line)) != 1:
        errors.append("body must have exactly one H1 title")
    for section in skill.sections:
        original = section.content.strip("\r\n")
        if original and original not in body:
            errors.append(f"source content not preserved: {section.title}")
    if skill.opening.strip() and skill.opening.strip("\r\n") not in body:
        errors.append("opening content not preserved")
    if unknown:
        errors.append(f"unmapped source headings: {sorted(unknown)}")
    size = len(rendered.encode("utf-8"))
    if not 400 <= size <= 60_000:
        errors.append(f"file size outside 400..60000 bytes: {size}")
    return errors


def _manifest_path(archive: Path) -> Path:
    return archive.with_suffix("").with_suffix(".sha256")


def _load_archive(archive_path: Path, paths: list[Path]) -> dict[Path, str]:
    if not archive_path.is_file():
        raise ValueError(f"backup not found: {archive_path}")
    expected = {path.relative_to(ROOT).as_posix(): path for path in paths}
    manifest_path = _manifest_path(archive_path)
    if not manifest_path.is_file():
        raise ValueError(f"backup manifest not found: {manifest_path}")
    manifest: dict[str, str] = {}
    for line in manifest_path.read_text(encoding="utf-8").splitlines():
        digest, rel = line.split("  ", 1)
        manifest[rel] = digest
    if set(manifest) != set(expected):
        raise ValueError(f"manifest {manifest_path} does not list the current 5,500 skill paths")
    result: dict[Path, str] = {}
    try:
        with tarfile.open(archive_path, "r:gz") as archive:
            members = {
                item.name: item
                for item in archive.getmembers()
                if item.isfile() and item.name in expected
            }
            if set(members) != set(expected):
                raise ValueError(f"archive {archive_path} does not contain the current 5,500 skill paths")
            for rel, path in expected.items():
                stream = archive.extractfile(members[rel])
                if stream is None:
                    raise ValueError(f"cannot read archive member {rel}")
                data = stream.read()
                if hashlib.sha256(data).hexdigest() != manifest[rel]:
                    raise ValueError(f"backup hash mismatch for {rel} in {archive_path}")
                result[path] = data.decode("utf-8")
    except (OSError, tarfile.TarError, UnicodeError) as exc:
        raise ValueError(f"cannot read backup {archive_path}: {exc}") from exc
    return result


def _apply(outputs: dict[Path, str]) -> None:
    for path, rendered in outputs.items():
        temp = path.with_name(f".{path.name}.{os.getpid()}.tmp")
        mode = stat.S_IMODE(path.stat().st_mode)
        try:
            with temp.open("wb") as handle:
                handle.write(rendered.encode("utf-8"))
                handle.flush()
                os.fsync(handle.fileno())
            os.chmod(temp, mode)
            os.replace(temp, path)
        finally:
            if temp.exists():
                temp.unlink()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="replace all local SKILL.md files")
    parser.add_argument("--source-backup", type=Path, default=SOURCE_BACKUP_DEFAULT)
    parser.add_argument("--rollback-backup", type=Path, default=ROLLBACK_BACKUP_DEFAULT)
    args = parser.parse_args()
    source_backup = args.source_backup if args.source_backup.is_absolute() else ROOT / args.source_backup
    rollback_backup = args.rollback_backup if args.rollback_backup.is_absolute() else ROOT / args.rollback_backup

    paths = sorted(SKILLS_ROOT.rglob("SKILL.md"))
    if len(paths) != 5500:
        print(f"ERROR: expected 5,500 skills; found {len(paths)}", file=sys.stderr)
        return 2
    try:
        original_texts = _load_archive(source_backup, paths)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    outputs: dict[Path, str] = {}
    errors: list[str] = []
    source_headings: set[str] = set()
    desc_units: list[int] = []
    optional_counts = {heading: 0 for heading in OPTIONAL_ORDER}
    original_bytes = 0
    for path in paths:
        try:
            original_text = original_texts[path]
            skill = source_parser._parse_skill(path, original_text)
            rendered, unknown, headings = _render(skill)
            errors.extend(
                f"{path.relative_to(ROOT)}: {message}"
                for message in _validate_output(path, skill, rendered, unknown, headings)
            )
            outputs[path] = rendered
            original_bytes += len(original_text.encode("utf-8"))
            for section in skill.sections:
                source_headings.add(section.title)
            for heading in headings:
                if heading in optional_counts:
                    optional_counts[heading] += 1
            _, description, _ = source_parser._parse_frontmatter(rendered, path)
            desc_units.append(content_units(description))
        except Exception as exc:
            errors.append(f"{path.relative_to(ROOT)}: {exc}")

    rendered_bytes = sum(len(text.encode("utf-8")) for text in outputs.values())
    print(f"Scanned {len(paths):,} original local skills from the verified archive.")
    print(f"Required sections: {len(REQUIRED_SECTIONS)}; optional sections are included only when source-supported.")
    print(f"Distinct source section headings routed: {len(source_headings)}.")
    print(f"Optional-section coverage: " + ", ".join(f"{key} {value:,}" for key, value in optional_counts.items()) + ".")
    print(f"Original bytes: {original_bytes:,}; rendered bytes: {rendered_bytes:,}.")
    if desc_units:
        print(f"Description content units: {min(desc_units)}..{max(desc_units)}.")

    if errors:
        print(f"PREFLIGHT FAILED: {len(errors)} issue(s).", file=sys.stderr)
        for error in errors[:100]:
            print(f"- {error}", file=sys.stderr)
        if len(errors) > 100:
            print(f"- ... {len(errors) - 100} more", file=sys.stderr)
        return 1
    print("Preflight passed: required sections, metadata, source preservation, headings, and file-size limits are clean.")
    if not args.apply:
        print("Read-only mode: no SKILL.md files were changed.")
        return 0

    try:
        rollback_texts = _load_archive(rollback_backup, paths)
    except ValueError as exc:
        print(f"ERROR: rollback archive verification failed: {exc}", file=sys.stderr)
        return 2
    modified = [path.relative_to(ROOT).as_posix() for path in paths if path.read_text(encoding="utf-8") != rollback_texts[path]]
    if modified:
        print(
            f"ERROR: {len(modified)} current skill files differ from the verified pre-migration backup; nothing was changed. "
            f"First differences: {modified[:5]}",
            file=sys.stderr,
        )
        return 2

    _apply(outputs)
    print(f"Reformatted {len(outputs):,} local SKILL.md files in place.")
    print(f"Rollback archive: {rollback_backup}")
    print(f"Original-source archive: {source_backup}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
