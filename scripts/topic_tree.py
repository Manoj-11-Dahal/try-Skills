"""Deterministic navigation-only topic branches; package paths never change.

Existing authoring seeds supply subject/context labels where available. Older
matrix families use their stable name before a known workflow suffix. Remaining
standalone skills are grouped by shared name prefixes or explicit name lists.
These are browsing aids, not claims of new semantic classification.
"""
from __future__ import annotations

from collections import defaultdict
import csv
from dataclasses import dataclass
import hashlib
from pathlib import Path
import re

TOPIC_DIR = "_topics"
MAX_SECTION_SKILLS = 40
WORKFLOW_SUFFIXES = (
    "capability-surface-map", "version-compatibility", "input-output-contract",
    "permission-boundary-review", "integration-parity-trace", "failure-triage-record",
    "performance-envelope", "change-impact-assessment", "reproducibility-fixture-plan",
    "release-handoff-record", "scope-intake-gate", "source-provenance-ledger",
    "completeness-reconciliation", "exception-triage-queue", "change-impact-trace",
    "threshold-rule-check", "scenario-sensitivity-matrix", "approval-evidence-packet",
    "recovery-readiness-drill", "closeout-handoff-ledger", "scope-and-baseline-record",
    "source-research-and-provenance-ledger", "requirements-and-decision-brief",
    "design-blueprint", "option-comparison-matrix", "build-configuration-runbook",
    "verification-and-acceptance-test-plan", "failure-triage-and-recovery",
    "security-rights-and-safety-review", "measured-improvement-and-handoff",
)


@dataclass
class Topic:
    key: str
    label: str
    method: str
    groups: dict[str, list[str]]

    @property
    def count(self) -> int:
        return sum(len(names) for names in self.groups.values())


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.casefold()).strip("-")


def topic_key(kind: str, value: str) -> str:
    # A digest disambiguates punctuation/case folding and bounds path length.
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()[:10]
    return f"{kind}-{slugify(value)[:90].rstrip('-')}-{digest}"


def workflow_base(name: str) -> str:
    for suffix in sorted(WORKFLOW_SUFFIXES, key=len, reverse=True):
        if name.endswith("-" + suffix):
            return name[:-(len(suffix) + 1)]
    return name


def load_hints(root: Path) -> dict[str, tuple[str, str]]:
    path = root / "references/internet-topic-seeds-2026-09-30.csv"
    if not path.exists():
        return {}
    hints = {}
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        if not {"topic_slug", "subject", "context"}.issubset(reader.fieldnames or []):
            raise ValueError(f"invalid topic-label source: {path}")
        for row in reader:
            key, subject, context = (row.get(field, "").strip() for field in ("topic_slug", "subject", "context"))
            if not key or not subject or not context or key in hints:
                raise ValueError(f"empty or duplicate authoring topic: {key!r}")
            hints[key] = (subject, context)
    return hints


def title(name: str) -> str:
    if name.startswith("aas-"):
        name = name[4:]
    return name.replace("-", " ").capitalize()


def sections(groups: dict[str, list[str]]) -> dict[str, list[str]]:
    """Bound each terminal list without splitting or dropping skill names."""
    result = {}
    for label, names in sorted(groups.items()):
        names = sorted(names)
        for offset in range(0, len(names), MAX_SECTION_SKILLS):
            page = offset // MAX_SECTION_SKILLS + 1
            heading = label if len(names) <= MAX_SECTION_SKILLS else f"{label} — part {page}"
            if heading in result:
                raise ValueError(f"duplicate topic section label: {heading}")
            result[heading] = names[offset:offset + MAX_SECTION_SKILLS]
    return result


def standalone_groups(names: list[str], prefix: tuple[str, ...] = ()):
    """Split large name families along token boundaries, not guessed meanings."""
    if len(names) <= MAX_SECTION_SKILLS:
        yield prefix, names
        return
    buckets = defaultdict(list)
    for name in names:
        words = tuple(name.split("-"))
        key = words[len(prefix)] if len(words) > len(prefix) else ""
        buckets[key].append(name)
    small = []
    for token, group in sorted(buckets.items()):
        if len(group) >= 3 and token:
            yield from standalone_groups(group, prefix + (token,))
        else:
            small.extend(group)
    if small:
        yield prefix, sorted(small)


def build_topics(root: Path, records) -> dict[tuple[str, str], list[Topic]]:
    hints = load_hints(root)
    branches = defaultdict(dict)
    standalone = defaultdict(list)
    for name, (path, _) in sorted(records.items()):
        branch = tuple(Path(path).parts[1:3])
        base = workflow_base(name)
        if base in hints:
            label, context = hints[base]
            kind, identity, method = "subject", label, "Existing authoring subject and context labels"
        elif base != name:
            label, context = title(base), "Workflows"
            kind, identity, method = "family", base, "Shared skill-name family (known workflow suffix removed)"
        else:
            standalone[branch].append(name)
            continue
        key = topic_key(kind, identity)
        topic = branches[branch].setdefault(key, Topic(key, label, method, defaultdict(list)))
        if topic.label != label:
            raise ValueError(f"topic-key collision: {key}")
        topic.groups[context].append(name)
    for branch, names in standalone.items():
        for prefix, group in standalone_groups(names):
            identity = "-".join(prefix) or "named-workflows"
            key = topic_key("names", identity)
            label = title(identity) if prefix else "Named workflows"
            topic = Topic(key, label, "Name-prefix browsing group; not a semantic reassignment", {"Skill list": group})
            if key in branches[branch]:
                raise ValueError(f"duplicate standalone topic: {key}")
            branches[branch][key] = topic
    return {
        branch: [Topic(t.key, t.label, t.method, sections(t.groups)) for t in sorted(topics.values(), key=lambda t: (t.label.casefold(), t.key))]
        for branch, topics in sorted(branches.items())
    }


def topic_paths(root: Path, topics) -> set[Path]:
    return {root / "skills" / category / branch / TOPIC_DIR / f"{topic.key}.md"
            for (category, branch), items in topics.items() for topic in items}
