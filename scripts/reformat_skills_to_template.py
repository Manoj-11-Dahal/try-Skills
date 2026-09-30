#!/usr/bin/env python3
"""Reorganize every local SKILL.md into the approved 19-section template.

The converter preserves every existing body section as source content under a
new section, while deriving only fields directly supported by that content.
Missing fields are marked "Not specified in source skill." The script is
read-only by default; use --apply only after creating the required backup.
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
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / "skills"
DEFAULT_BACKUP = ROOT / "backups" / "before-template-reformat-2026-09-29.tar.gz"

TEMPLATE_SECTIONS = [
    "Overview",
    "When to Use",
    "Trigger Examples",
    "Scope",
    "Inputs",
    "Instructions",
    "Decision Rules",
    "Tools and Resources",
    "Output Format",
    "Quality Standards",
    "Validation Checklist",
    "Edge Cases and Recovery",
    "Stop Conditions",
    "Common Pitfalls",
    "Examples",
    "Test Cases",
    "Success Criteria",
    "Related Skills",
    "Maintenance",
]

TARGET_KEYS = {
    "Overview": "overview",
    "When to Use": "when",
    "Trigger Examples": "triggers",
    "Scope": "scope",
    "Inputs": "inputs",
    "Instructions": "instructions",
    "Decision Rules": "decisions",
    "Tools and Resources": "tools",
    "Output Format": "output",
    "Quality Standards": "quality",
    "Validation Checklist": "validation",
    "Edge Cases and Recovery": "edge",
    "Stop Conditions": "stop",
    "Common Pitfalls": "pitfalls",
    "Examples": "examples",
    "Test Cases": "tests",
    "Success Criteria": "success",
    "Related Skills": "related",
    "Maintenance": "maintenance",
}

# Current local heading inventory was inspected before conversion. Explicit
# mappings make routing auditable; the generic fallbacks below cover future
# skills without silently dropping their content.
EXACT_MAP = {
    "overview": "overview",
    "purpose": "overview",
    "introduction": "overview",
    "when to use": "when",
    "trigger examples": "triggers",
    "triggers": "triggers",
    "topic provenance": "tools",
    "acceptance evidence": "quality",
    "safety and stop conditions": "stop",
    "loop contract": "scope",
    "tool map": "tools",
    "iterative workflow": "instructions",
    "focused procedure": "instructions",
    "workflow": "instructions",
    "procedure": "instructions",
    "instructions": "instructions",
    "steps": "instructions",
    "guardrails": "scope",
    "acceptance": "quality",
    "inputs and boundaries": "inputs",
    "inputs": "inputs",
    "domain checks": "validation",
    "apple-platform checks": "validation",
    "game-specific checks": "validation",
    "kubernetes checks": "validation",
    "browser-specific checks": "validation",
    "platform-specific checks": "validation",
    "medical-imaging-specific checks": "validation",
    "security-specific checks": "validation",
    "output and acceptance": "output",
    "safety and acceptance": "quality",
    "stop conditions": "stop",
    "safety and privacy": "scope",
    "safety boundaries": "scope",
    "safety and respect": "scope",
    "adr shape": "output",
    "output": "output",
    "finding standard": "output",
    "review boundaries": "scope",
    "go/no-go output": "output",
    "approval and safety boundaries": "scope",
    "specification shape": "output",
    "safety and verification": "validation",
    "finding format": "output",
    "audit guardrails": "scope",
    "common failure modes": "pitfalls",
    "context hygiene": "scope",
    "evaluation guardrails": "scope",
    "retry guardrails": "edge",
    "references": "tools",
    "coordination risks": "edge",
    "maintenance rules": "maintenance",
    "research guardrails": "scope",
    "checkpoint template": "output",
    "planning guardrails": "scope",
    "safety rules": "scope",
    "red flags": "stop",
    "stopping rules": "stop",
    "examples": "examples",
    "test cases": "tests",
    "related skills": "related",
    "maintenance": "maintenance",
    "edge cases and recovery": "edge",
    "decision rules": "decisions",
    "tools and resources": "tools",
    "quality standards": "quality",
    "validation checklist": "validation",
    "success criteria": "success",
    "common pitfalls": "pitfalls",
}

MISSING = "Not specified in source skill."
STOP_LINE_RE = re.compile(
    r"\b(?:stop(?:ping)?|exit\s+conditions?|exit\s+when|halt|pause|"
    r"escalat(?:e|ion|ed)|ask\s+when|ask\s+rather\s+than|do\s+not\s+continue)\b",
    re.I,
)
EDGE_LINE_RE = re.compile(
    r"\b(?:boundary\s+cases?|fail(?:ure|ures|ed|ing)?|errors?|exceptions?|"
    r"recover(?:y|ies|ing)?|retries?|fallbacks?|malformed|partial\s+failure|"
    r"timeouts?|outages?|denied|invalid|missing\s+(?:data|inputs?)|regressions?|"
    r"repeated\s+(?:calls?|actions?|failures?))\b",
    re.I,
)
BOUNDARY_LINE_RE = re.compile(
    r"\b(?:do\s+not|don['’]t|never|must\s+not|not\s+authorized|"
    r"without\s+explicit\s+(?:authorization|approval)|does\s+not\s+grant|"
    r"does\s+not\s+authorize|not\s+a\s+substitute|does\s+not\s+replace|"
    r"cannot)\b",
    re.I,
)


@dataclass
class SourceSection:
    title: str
    content: str
    target: str


@dataclass
class ParsedSkill:
    name: str
    description: str
    body: str
    title: str
    opening: str
    sections: list[SourceSection]
    original_text: str


def _parse_frontmatter(text: str, path: Path) -> tuple[str, str, str]:
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        raise ValueError(f"{path}: frontmatter must start with ---")
    closing = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            closing = index
            break
    if closing is None:
        raise ValueError(f"{path}: frontmatter closing --- is missing")

    fields: dict[str, str] = {}
    keys: list[str] = []
    for line in lines[1:closing]:
        if not line.strip():
            continue
        if ":" not in line:
            raise ValueError(f"{path}: malformed frontmatter line {line.rstrip()!r}")
        key, value = line.split(":", 1)
        key = key.strip()
        keys.append(key)
        fields[key] = value.strip()
    if keys != ["name", "description"]:
        raise ValueError(f"{path}: unexpected frontmatter keys {keys!r}")
    name = fields.get("name", "")
    raw_description = fields.get("description", "")
    try:
        description = json.loads(raw_description)
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path}: description is not valid quoted YAML/JSON: {exc}") from exc
    if not isinstance(description, str):
        raise ValueError(f"{path}: description must be a string")
    body = "".join(lines[closing + 1 :])
    return name, description, body


def _heading(line: str) -> tuple[int, str] | None:
    content = line.rstrip("\r\n")
    match = re.match(r"^(#{1,6})\s+(.+?)\s*#*\s*$", content)
    if not match:
        return None
    return len(match.group(1)), match.group(2).strip()


def _split_body(body: str, name: str) -> tuple[str, str, list[tuple[str, str]]]:
    """Return title, pre-section opening text, and level-two source blocks."""
    lines = body.splitlines(keepends=True)
    title: str | None = None
    opening: list[str] = []
    sections: list[tuple[str, list[str]]] = []
    current: list[str] | None = None
    current_title: str | None = None
    fence_char: str | None = None
    fence_len = 0

    for line in lines:
        stripped = line.lstrip()
        fence = re.match(r"^(`{3,}|~{3,})", stripped)
        if fence_char is not None:
            if fence:
                marker = fence.group(1)
                if marker[0] == fence_char and len(marker) >= fence_len:
                    fence_char = None
                    fence_len = 0
            if current is not None:
                current.append(line)
            elif title is None:
                opening.append(line)
            else:
                opening.append(line)
            continue
        if fence:
            marker = fence.group(1)
            fence_char, fence_len = marker[0], len(marker)
            if current is not None:
                current.append(line)
            else:
                opening.append(line)
            continue

        parsed = _heading(line)
        if parsed and parsed[0] == 1 and title is None:
            title = parsed[1]
            continue
        if parsed and parsed[0] == 2:
            if current is not None and current_title is not None:
                sections.append((current_title, current))
            current_title = parsed[1]
            current = []
            continue
        if current is not None:
            current.append(line)
        else:
            opening.append(line)

    if current is not None and current_title is not None:
        sections.append((current_title, current))

    if not title:
        title = " ".join(part.capitalize() for part in name.split("-"))
    opening_text = "".join(opening).strip("\r\n")
    normalized_sections = [
        (heading, "".join(content).strip("\r\n"))
        for heading, content in sections
    ]
    return title, opening_text, normalized_sections


def _target_for_heading(title: str) -> str | None:
    key = re.sub(r"\s+", " ", title.strip().rstrip(":" )).casefold()
    if key in EXACT_MAP:
        return EXACT_MAP[key]
    if "related skill" in key:
        return "related"
    if "maintenance" in key or "version history" in key:
        return "maintenance"
    if "test case" in key or key.startswith("test"):
        return "tests"
    if "example" in key:
        return "examples"
    if "trigger" in key:
        return "triggers"
    if "decision" in key or "routing" in key:
        return "decisions"
    if "input" in key or "prerequisite" in key:
        return "inputs"
    if "stop" in key or "stopping" in key or "exit condition" in key:
        return "stop"
    if "edge case" in key or "recovery" in key or "retry" in key or "coordination risk" in key:
        return "edge"
    if "pitfall" in key or "failure mode" in key:
        return "pitfalls"
    if "tool" in key or "resource" in key or "reference" in key or "provenance" in key:
        return "tools"
    if "output" in key or "format" in key or "shape" in key or "template" in key or "finding" in key:
        return "output"
    if "acceptance" in key or "quality" in key:
        return "quality"
    if "validation" in key or "check" in key or "verification" in key:
        return "validation"
    if "scope" in key or "guardrail" in key or "boundary" in key or "safety" in key or "privacy" in key or "hygiene" in key:
        return "scope"
    if "procedure" in key or "workflow" in key or "instruction" in key or "step" in key or "process" in key or "method" in key:
        return "instructions"
    if "when to use" in key or "activation" in key:
        return "when"
    if "overview" in key or "purpose" in key or "summary" in key:
        return "overview"
    return None


def _sentence_boundary(text: str) -> int | None:
    """Find a likely sentence boundary, including punctuation other than dots."""
    for match in re.finditer(r"[.!?][ \t]+(?=[A-Z0-9])", text):
        prefix = text[: match.start() + 1].rstrip()
        last_word = re.search(r"([A-Za-z.]+)$", prefix)
        token = last_word.group(1).casefold() if last_word else ""
        if token in {"e.g.", "i.e.", "u.s.", "u.k.", "mr.", "mrs.", "dr.", "vs."}:
            continue
        return match.start() + 1
    return None


def _description_parts(description: str, title: str) -> tuple[str, str, str]:
    """Normalize the description to Use-when/trigger/to/outcome without dropping its detail."""
    original = re.sub(r"\s+", " ", description.strip())
    if not original.lower().startswith("use when "):
        trigger = f"a task needs {title.lower()}"
        action = f"apply the {title.lower()} guidance"
        return trigger, action, f"Use when {trigger} to {action}. {original}"

    rest = original[len("Use when ") :]
    first_boundary = _sentence_boundary(rest)
    if first_boundary is None:
        trigger = rest.rstrip(".!? ")
        action = f"apply the {title.lower()} guidance"
        normalized = f"Use when {trigger} to {action}."
        return trigger, action, normalized

    trigger = rest[:first_boundary].strip().rstrip(".!? ")
    after_trigger = rest[first_boundary:].lstrip()
    second_boundary = _sentence_boundary(after_trigger)
    if second_boundary is None:
        action_sentence = after_trigger.rstrip(".!? ")
        tail = ""
    else:
        action_sentence = after_trigger[:second_boundary].strip().rstrip(".!? ")
        tail = after_trigger[second_boundary:].strip()

    action_sentence = action_sentence.strip()
    first_token = action_sentence.split(None, 1)[0].strip(".,:;()[]{}") if action_sentence else ""
    non_action_openers = {"success", "trigger", "this", "that", "the", "a", "an", "because", "although"}
    if not action_sentence or first_token.casefold() in non_action_openers or action_sentence.casefold().startswith("do not "):
        action = f"follow the {title.lower()} workflow"
        retained = " ".join(part for part in (after_trigger, tail) if part).strip()
        normalized = f"Use when {trigger} to {action}."
        if retained:
            normalized += f" {retained}"
        return trigger, action, normalized

    action = action_sentence[0].lower() + action_sentence[1:]
    normalized = f"Use when {trigger} to {action}."
    if tail:
        normalized += f" {tail}"
    return trigger, action.rstrip(".!? "), normalized


def _field(section_text: str, label: str) -> str | None:
    pattern = re.compile(
        rf"(?im)^\s*(?:[-*+]\s*)?\*\*{re.escape(label)}:?\*\*\s*:?\s*(.+?)\s*$"
    )
    match = pattern.search(section_text)
    return match.group(1).strip() if match else None


def _source_block(section: SourceSection) -> str:
    content = section.content.strip("\r\n")
    heading = f"### Preserved source section: {section.title}"
    return f"{heading}\n\n{content}" if content else f"{heading}\n\n{MISSING}"


def _source_blocks(blocks: Iterable[SourceSection]) -> str:
    material = [_source_block(block) for block in blocks]
    return "\n\n".join(material)


def _matched_source_lines(
    sections: Iterable[SourceSection],
    pattern: re.Pattern[str],
    *,
    excluded_targets: set[str] | None = None,
    excluded_titles: set[str] | None = None,
) -> list[tuple[str, list[str]]]:
    excluded_targets = excluded_targets or set()
    excluded_titles = {title.casefold() for title in (excluded_titles or set())}
    grouped: list[tuple[str, list[str]]] = []
    for section in sections:
        if section.target in excluded_targets or section.title.casefold() in excluded_titles:
            continue
        matched: list[str] = []
        seen: set[str] = set()
        for line in section.content.splitlines():
            if pattern.search(line):
                normalized = re.sub(r"\s+", " ", line.strip()).casefold()
                if normalized and normalized not in seen:
                    seen.add(normalized)
                    matched.append(line.rstrip())
        if matched:
            grouped.append((section.title, matched))
    return grouped


def _render_derived_groups(groups: Iterable[tuple[str, list[str]]], label: str) -> str:
    rendered = [
        f"### {label}: {title}\n\n" + "\n".join(lines)
        for title, lines in groups
    ]
    return "\n\n".join(rendered)


def _list_items(text: str) -> list[str]:
    items: list[str] = []
    for line in text.splitlines():
        match = re.match(r"^\s*(?:[-*+]\s+|\d+[.)]\s+)(.+?)\s*$", line)
        if match:
            item = match.group(1).strip()
            if item.startswith("[ ] ") or item.startswith("[x] ") or item.startswith("[X] "):
                item = item[4:].strip()
            if item:
                items.append(item)
    return items


def _render_list_as_checkboxes(items: Iterable[str]) -> str:
    seen: set[str] = set()
    rendered: list[str] = []
    for item in items:
        key = re.sub(r"\s+", " ", item).casefold()
        if key in seen:
            continue
        seen.add(key)
        rendered.append(f"- [ ] {item}")
    return "\n".join(rendered)


def _render_sections(blocks: list[SourceSection], *, fallback: str = MISSING) -> str:
    if not blocks:
        return fallback
    return _source_blocks(blocks)


def _build_output(skill: ParsedSkill, old_description: str) -> tuple[str, set[str]]:
    trigger, action, new_description = _description_parts(old_description, skill.title)
    groups: dict[str, list[SourceSection]] = {key: [] for key in TARGET_KEYS.values()}
    unknown: set[str] = set()
    for section in skill.sections:
        if section.target not in groups:
            unknown.add(section.title)
        else:
            groups[section.target].append(section)

    # Source-derived loop-contract fields are repeated in the matching target
    # sections; the complete original section remains preserved under Scope.
    loop_text = "\n".join(
        section.content for section in skill.sections if section.title.casefold() == "loop contract"
    )
    artifact = _field(loop_text, "Artifact") if loop_text else None
    feedback = _field(loop_text, "Feedback signal") if loop_text else None
    exit_condition = _field(loop_text, "Exit") if loop_text else None

    overview_parts = [
        f"This skill applies when {trigger}. Its intended outcome is to {action.rstrip('.!? ')}."
    ]
    if groups["overview"]:
        overview_parts.append(_source_blocks(groups["overview"]))
    if skill.opening.strip():
        overview_parts.append(
            "### Preserved opening content\n\n" + skill.opening.strip("\r\n")
        )

    when_content = _render_sections(groups["when"])
    trigger_content = _render_sections(
        groups["triggers"],
        fallback="Not specified in source skill content; no sample trigger phrases were provided.",
    )
    if not groups["triggers"] and groups["examples"]:
        trigger_content = "See the preserved source examples below; separate trigger phrases are not specified."

    boundary_groups = _matched_source_lines(
        skill.sections,
        BOUNDARY_LINE_RE,
        excluded_targets={"scope", "stop"},
    )
    if groups["scope"] or groups["stop"] or boundary_groups:
        does_not = "See the preserved source boundaries below and under Stop Conditions."
    else:
        does_not = MISSING
    scope_intro = (
        "**Does:** Follow the task boundary stated under When to Use and the procedure below.\n\n"
        f"**Does not:** {does_not}"
    )
    scope_parts = [scope_intro]
    if groups["scope"]:
        scope_parts.append(_source_blocks(groups["scope"]))
    if boundary_groups:
        scope_parts.append(_render_derived_groups(boundary_groups, "Source boundary statements from"))
    if not groups["scope"] and not boundary_groups:
        scope_parts.append(
            "Source scope limits are preserved under Stop Conditions."
            if groups["stop"]
            else MISSING
        )

    if groups["inputs"]:
        inputs_intro = (
            "**Required:** See the preserved source input guidance below.\n\n"
            f"**Optional:** {MISSING}\n\n**If information is missing:** {MISSING}"
        )
        inputs_content = inputs_intro + "\n\n" + _source_blocks(groups["inputs"])
    else:
        inputs_content = (
            f"**Required:** {MISSING}\n\n**Optional:** {MISSING}\n\n"
            f"**If information is missing:** {MISSING}"
        )

    instructions_content = _render_sections(groups["instructions"])
    decisions_content = _render_sections(groups["decisions"])

    has_tool_map = any(section.title.casefold() == "tool map" for section in skill.sections)
    if has_tool_map:
        tools_intro = (
            "**Use:** See the preserved Tool Map below.\n\n"
            "**Do not use:** See preserved scope and stop-condition guidance for explicit restrictions; "
            f"additional tool-specific limits are {MISSING.lower()}\n\n"
            f"**Fallback:** {MISSING}"
        )
    else:
        tools_intro = (
            f"**Use:** {MISSING}\n\n**Do not use:** {MISSING}\n\n**Fallback:** {MISSING}"
        )
    tools_content = tools_intro
    if groups["tools"]:
        tools_content += "\n\n" + _source_blocks(groups["tools"])

    output_parts: list[str] = []
    if artifact:
        output_parts.append(f"**Artifact (from source Loop Contract):** {artifact}")
    if groups["output"]:
        output_parts.append(_source_blocks(groups["output"]))
    if not output_parts:
        output_parts.append(MISSING)
    output_content = "\n\n".join(output_parts)

    output_acceptance_blocks = [
        section for section in groups["output"] if "acceptance" in section.title.casefold()
    ]
    quality_parts: list[str] = []
    if groups["quality"]:
        quality_parts.append(_source_blocks(groups["quality"]))
    quality_parts.extend(
        f"### Acceptance standards from source: {section.title}\n\n{section.content.strip()}"
        for section in output_acceptance_blocks
    )
    quality_content = "\n\n".join(quality_parts) if quality_parts else MISSING

    # The original source check/acceptance text remains verbatim in its mapped
    # section. Separate unchecked items are derived from that text; they are not
    # evidence that anyone ran a test or completed a check.
    validation_parts: list[str] = []
    if groups["validation"]:
        validation_parts.append(_source_blocks(groups["validation"]))
    checklist_sources = groups["validation"] + groups["quality"] + output_acceptance_blocks
    check_items: list[str] = []
    for source_section in checklist_sources:
        check_items.extend(_list_items(source_section.content))
    if check_items:
        validation_parts.append(
            "**Unchecked checklist derived from source criteria (not test evidence):**\n\n"
            + _render_list_as_checkboxes(check_items)
        )
    elif groups["quality"] or groups["output"]:
        validation_parts.append(
            "- [ ] Confirm the source-defined acceptance standard preserved under Quality Standards or Output Format is met."
        )
    if not validation_parts:
        validation_parts.append(MISSING)
    validation_content = "\n\n".join(validation_parts)

    edge_related = _matched_source_lines(
        skill.sections,
        EDGE_LINE_RE,
        excluded_targets={"edge"},
        excluded_titles={"When to Use"},
    )
    edge_parts: list[str] = []
    if groups["edge"]:
        edge_parts.append(_source_blocks(groups["edge"]))
    if edge_related:
        edge_parts.append(_render_derived_groups(edge_related, "Source edge/failure guidance from"))
    edge_content = "\n\n".join(edge_parts) if edge_parts else MISSING

    stop_related = _matched_source_lines(
        skill.sections,
        STOP_LINE_RE,
        excluded_targets={"stop"},
        excluded_titles={"Loop Contract"},
    )
    stop_parts: list[str] = []
    if groups["stop"]:
        stop_parts.append(_source_blocks(groups["stop"]))
    if exit_condition:
        stop_parts.append(f"**Exit condition (from source Loop Contract):** {exit_condition}")
    if stop_related:
        stop_parts.append(_render_derived_groups(stop_related, "Source stop-related guidance from"))
    stop_content = "\n\n".join(stop_parts) if stop_parts else MISSING

    pitfalls_content = _render_sections(groups["pitfalls"])

    examples_parts: list[str] = []
    if groups["examples"]:
        examples_parts.append(_source_blocks(groups["examples"]))
    else:
        examples_parts.append(
            f"**Example input:** {MISSING}\n\n**Example output:** {MISSING}\n\n"
            f"**Anti-example:** {MISSING}\n\n**Why it fails:** {MISSING}"
        )
    examples_content = "\n\n".join(examples_parts)

    tests_content = _render_sections(
        groups["tests"],
        fallback="Not specified in source skill; no runnable test cases were supplied.",
    )

    success_parts: list[str] = []
    if feedback:
        success_parts.append(f"**Success signal (from source Loop Contract):** {feedback}")
    elif groups["quality"]:
        success_parts.extend(
            f"### Success criteria from source: {section.title}\n\n{section.content.strip()}"
            for section in groups["quality"]
        )
    elif groups["output"]:
        success_parts.extend(
            f"### Success criteria from source: {section.title}\n\n{section.content.strip()}"
            for section in groups["output"]
        )
    if groups["success"]:
        success_parts.append(_source_blocks(groups["success"]))
    if not success_parts:
        success_parts.append(MISSING)
    success_content = "\n\n".join(success_parts)

    related_content = _render_sections(groups["related"])

    maintenance_fields = (
        f"**Owner:** {MISSING}\n\n**Version:** {MISSING}\n\n"
        f"**Last reviewed:** {MISSING}\n\n**Review trigger:** {MISSING}"
    )
    maintenance_content = maintenance_fields
    if groups["maintenance"]:
        maintenance_content += "\n\n" + _source_blocks(groups["maintenance"])

    contents = {
        "Overview": "\n\n".join(overview_parts),
        "When to Use": when_content,
        "Trigger Examples": trigger_content,
        "Scope": "\n\n".join(scope_parts),
        "Inputs": inputs_content,
        "Instructions": instructions_content,
        "Decision Rules": decisions_content,
        "Tools and Resources": tools_content,
        "Output Format": output_content,
        "Quality Standards": quality_content,
        "Validation Checklist": validation_content,
        "Edge Cases and Recovery": edge_content,
        "Stop Conditions": stop_content,
        "Common Pitfalls": pitfalls_content,
        "Examples": examples_content,
        "Test Cases": tests_content,
        "Success Criteria": success_content,
        "Related Skills": related_content,
        "Maintenance": maintenance_content,
    }

    rendered_body = [f"# {skill.title}"]
    for heading in TEMPLATE_SECTIONS:
        rendered_body.extend(["", f"## {heading}", "", contents[heading].strip("\r\n")])
    body = "\n".join(rendered_body).rstrip() + "\n"
    frontmatter = (
        "---\n"
        f"name: {skill.name}\n"
        f"description: {json.dumps(new_description, ensure_ascii=False)}\n"
        "---\n"
    )
    return frontmatter + "\n" + body, unknown


def _parse_skill(path: Path, original_text: str | None = None) -> ParsedSkill:
    if original_text is None:
        original_text = path.read_text(encoding="utf-8")
    name, description, body = _parse_frontmatter(original_text, path)
    title, opening, raw_sections = _split_body(body, name)
    sections: list[SourceSection] = []
    for source_title, content in raw_sections:
        target = _target_for_heading(source_title)
        if target is None:
            target = "unmapped"
        sections.append(SourceSection(source_title, content, target))
    return ParsedSkill(name, description, body, title, opening, sections, original_text)


def _validate_rendered(path: Path, skill: ParsedSkill, rendered: str, unknown: set[str]) -> list[str]:
    errors: list[str] = []
    try:
        name, description, body = _parse_frontmatter(rendered, path)
    except ValueError as exc:
        return [str(exc)]
    if name != skill.name:
        errors.append("name changed during conversion")
    if len(description) > 1024:
        errors.append(f"description exceeds 1024 characters ({len(description)})")

    # Use the repository's validator for the same content-unit definition.
    scripts_dir = str(ROOT / "scripts")
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    try:
        from validate_skills import content_units
        units = content_units(description)
    except Exception as exc:  # pragma: no cover - import failure is reported below
        errors.append(f"could not load repository content-unit validator: {exc}")
        units = 0
    if units < 40:
        errors.append(f"description has {units} content units; minimum is 40")

    top_level = re.findall(r"^##\s+(.+?)\s*$", body, re.M)
    normalized = [value.strip().casefold() for value in top_level]
    expected = [value.casefold() for value in TEMPLATE_SECTIONS]
    if normalized != expected:
        errors.append("top-level headings do not exactly match the approved order")

    all_headings = re.findall(r"^#{1,6}\s+(.+?)\s*#*\s*$", body, re.M)
    normalized_all = [value.strip().casefold() for value in all_headings]
    if len(normalized_all) != len(set(normalized_all)):
        duplicates = sorted({value for value in normalized_all if normalized_all.count(value) > 1})
        errors.append(f"duplicate Markdown headings: {duplicates[:8]}")
    if sum(1 for line in body.splitlines() if re.match(r"^#\s+\S", line)) != 1:
        errors.append("body must contain exactly one level-one title")

    # Check that every source prose block survives as an exact substring (the
    # surrounding section headings and list-formatting copies may change).
    for source in skill.sections:
        source_text = source.content.strip("\r\n")
        if source_text and source_text not in body:
            errors.append(f"source content was not preserved for section {source.title!r}")
    if skill.opening.strip() and skill.opening.strip("\r\n") not in body:
        errors.append("opening body content was not preserved")

    if unknown:
        errors.append(f"unmapped source headings: {sorted(unknown)}")

    size = len(rendered.encode("utf-8"))
    if not (400 <= size <= 60_000):
        errors.append(f"rendered file size {size} bytes is outside 400..60000")
    return errors


def _backup_skill_count(backup: Path) -> int:
    if not backup.is_file():
        return 0
    try:
        with tarfile.open(backup, "r:gz") as archive:
            return sum(
                1
                for member in archive.getmembers()
                if member.isfile() and member.name.startswith("skills/") and member.name.endswith("/SKILL.md")
            )
    except (OSError, tarfile.TarError):
        return 0


def _load_backup_source_texts(backup: Path, paths: list[Path]) -> dict[Path, str]:
    if _backup_skill_count(backup) != len(paths):
        raise ValueError(f"backup {backup} does not contain exactly {len(paths)} SKILL.md files")
    expected = {path.relative_to(ROOT).as_posix(): path for path in paths}
    sources: dict[Path, str] = {}
    try:
        with tarfile.open(backup, "r:gz") as archive:
            for member in archive.getmembers():
                if not member.isfile() or member.name not in expected:
                    continue
                stream = archive.extractfile(member)
                if stream is None:
                    raise ValueError(f"cannot read backup member {member.name}")
                sources[expected[member.name]] = stream.read().decode("utf-8")
    except (OSError, tarfile.TarError, UnicodeError) as exc:
        raise ValueError(f"cannot read source backup {backup}: {exc}") from exc
    if set(sources) != set(paths):
        missing = sorted(path.relative_to(ROOT).as_posix() for path in set(paths) - set(sources))
        raise ValueError(f"backup is missing {len(missing)} expected files: {missing[:5]}")
    return sources


def _already_formatted(path: Path) -> bool:
    try:
        _, _, body = _parse_frontmatter(path.read_text(encoding="utf-8"), path)
    except Exception:
        return False
    headings = [item.strip() for item in re.findall(r"^##\s+(.+?)\s*$", body, re.M)]
    return [item.casefold() for item in headings] == [item.casefold() for item in TEMPLATE_SECTIONS]


def _load_and_render(
    paths: list[Path],
    source_texts: dict[Path, str] | None = None,
) -> tuple[dict[Path, str], list[str], dict[str, int], dict[str, int], int, int]:
    outputs: dict[Path, str] = {}
    errors: list[str] = []
    heading_counts: dict[str, int] = {}
    heading_set = set(TEMPLATE_SECTIONS)
    description_min = 10**9
    description_max = 0
    original_bytes = 0
    rendered_bytes = 0

    for path in paths:
        try:
            source_text = source_texts.get(path) if source_texts is not None else None
            skill = _parse_skill(path, source_text)
            rendered, unknown = _build_output(skill, skill.description)
            file_errors = _validate_rendered(path, skill, rendered, unknown)
            if file_errors:
                errors.extend(f"{path.relative_to(ROOT)}: {error}" for error in file_errors)
            outputs[path] = rendered
            original_bytes += len(skill.original_text.encode("utf-8"))
            rendered_bytes += len(rendered.encode("utf-8"))
            _, new_description, _ = _parse_frontmatter(rendered, path)
            if str(ROOT / "scripts") not in sys.path:
                sys.path.insert(0, str(ROOT / "scripts"))
            from validate_skills import content_units
            units = content_units(new_description)
            description_min = min(description_min, units)
            description_max = max(description_max, units)
            for section in skill.sections:
                heading_counts[section.title] = heading_counts.get(section.title, 0) + 1
        except Exception as exc:
            errors.append(f"{path.relative_to(ROOT)}: {exc}")

    return outputs, errors, heading_counts, {s: 1 for s in heading_set}, description_min, description_max


def _apply_outputs(outputs: dict[Path, str]) -> None:
    for path, content in outputs.items():
        data = content.encode("utf-8")
        mode = stat.S_IMODE(path.stat().st_mode)
        temp = path.with_name(f".{path.name}.{os.getpid()}.tmp")
        try:
            with temp.open("wb") as handle:
                handle.write(data)
                handle.flush()
                os.fsync(handle.fileno())
            os.chmod(temp, mode)
            os.replace(temp, path)
        finally:
            if temp.exists():
                temp.unlink()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="rewrite all local SKILL.md files in place")
    parser.add_argument("--backup", type=Path, default=DEFAULT_BACKUP, help="required pre-migration tar.gz backup")
    parser.add_argument("--from-backup", action="store_true", help="rebuild from the verified original backup")
    args = parser.parse_args()

    if not ROOT.is_dir() or not SKILLS_ROOT.is_dir():
        print(f"ERROR: expected repository at {ROOT}", file=sys.stderr)
        return 2
    paths = sorted(SKILLS_ROOT.rglob("SKILL.md"))
    if len(paths) != 5500:
        print(f"ERROR: expected 5,500 local SKILL.md files, found {len(paths)}", file=sys.stderr)
        return 2

    backup = args.backup if args.backup.is_absolute() else ROOT / args.backup
    if not args.from_backup and _already_formatted(paths[0]):
        print("ERROR: files already use the approved template; use --from-backup to rebuild safely.", file=sys.stderr)
        return 2
    source_texts = None
    if args.from_backup:
        try:
            source_texts = _load_backup_source_texts(backup, paths)
        except ValueError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 2

    outputs, errors, source_heading_counts, _, desc_min, desc_max = _load_and_render(paths, source_texts)
    print(f"Scanned {len(paths):,} SKILL.md files.")
    print(f"Required top-level sections: {len(TEMPLATE_SECTIONS)} in approved order.")
    print(f"Description content-unit range after normalization: {desc_min}..{desc_max}.")
    source_byte_count = sum(
        len((source_texts[path] if source_texts is not None else path.read_text(encoding="utf-8")).encode("utf-8"))
        for path in paths
    )
    print(f"Original bytes: {source_byte_count:,}; rendered bytes: {sum(len(v.encode('utf-8')) for v in outputs.values()):,}.")
    print(f"Distinct source section headings routed: {len(source_heading_counts)}.")

    if errors:
        print(f"PREFLIGHT FAILED: {len(errors)} issue(s).", file=sys.stderr)
        for error in errors[:100]:
            print(f"- {error}", file=sys.stderr)
        if len(errors) > 100:
            print(f"- ... {len(errors) - 100} more", file=sys.stderr)
        return 1

    print("Preflight passed: required structure, metadata, file-size bounds, source text preservation, and heading checks are clean.")
    if not args.apply:
        mode = " using the original backup" if args.from_backup else ""
        print(f"Read-only mode{mode}: no SKILL.md files were changed.")
        return 0

    backed_up = _backup_skill_count(backup)
    if backed_up != len(paths):
        print(
            f"ERROR: backup {backup} contains {backed_up} SKILL.md entries; expected {len(paths)}. Nothing was changed.",
            file=sys.stderr,
        )
        return 2
    if not args.from_backup:
        try:
            backup_texts = _load_backup_source_texts(backup, paths)
        except ValueError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 2
        mismatches = [
            path.relative_to(ROOT).as_posix()
            for path in paths
            if path.read_text(encoding="utf-8") != backup_texts[path]
        ]
        if mismatches:
            print(
                f"ERROR: {len(mismatches)} current files differ from the pre-migration backup; nothing was changed. "
                f"Use --from-backup only when intentionally rebuilding. First differences: {mismatches[:5]}",
                file=sys.stderr,
            )
            return 2

    _apply_outputs(outputs)
    print(f"Reformatted {len(outputs):,} local SKILL.md files in place.")
    print(f"Recovery backup: {backup}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
