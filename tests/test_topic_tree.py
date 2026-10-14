"""Coverage, determinism, anchors, and safe maintenance for multi-level trees."""
from collections import Counter
from contextlib import redirect_stdout
import csv
import io
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import sync_catalog
import topic_tree
import tree_navigation
import validate_skills


class TopicGroupingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def records(self, names):
        return {name: (f"skills/software-development/backend-apis/{name}/SKILL.md", "Use when testing") for name in names}

    def write_hints(self, rows):
        path = self.root / "references/internet-topic-seeds-2026-09-30.csv"
        path.parent.mkdir(exist_ok=True)
        with path.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.writer(stream)
            writer.writerow(["topic_slug", "subject", "context"])
            writer.writerows(rows)

    def test_authoring_labels_form_subject_and_context_groups(self):
        self.write_hints([("codelab-python-api", "Python services", "API evolution"),
                          ("codelab-python-jobs", "Python services", "Background jobs")])
        names = ["codelab-python-api-design-blueprint", "codelab-python-jobs-design-blueprint"]
        topics = topic_tree.build_topics(self.root, self.records(names))["software-development", "backend-apis"]
        self.assertEqual(len(topics), 1)
        self.assertEqual(topics[0].label, "Python services")
        self.assertEqual(set(topics[0].groups), {"API evolution", "Background jobs"})
        self.assertEqual(topics[0].count, 2)

    def test_known_workflow_suffix_forms_older_family(self):
        names = ["example-api-scope-intake-gate", "example-api-source-provenance-ledger"]
        topics = topic_tree.build_topics(self.root, self.records(names))["software-development", "backend-apis"]
        self.assertEqual(len(topics), 1)
        self.assertEqual(topics[0].label, "Example api")
        self.assertEqual(topics[0].groups["Workflows"], sorted(names))

    def test_unknown_suffix_is_not_removed(self):
        self.assertEqual(topic_tree.workflow_base("example-security-review"), "example-security-review")
        self.assertEqual(topic_tree.workflow_base("example-failure-triage-and-recovery"), "example")

    def test_standalone_partition_is_bounded_complete_and_unique(self):
        names = [f"shared-prefix-task-{i}" for i in range(121)] + ["singleton"]
        topics = topic_tree.build_topics(self.root, self.records(names))
        actual = [name for items in topics.values() for item in items for group in item.groups.values() for name in group]
        self.assertEqual(Counter(actual), Counter(names))
        self.assertTrue(all(len(group) <= 40 for items in topics.values() for item in items for group in item.groups.values()))

    def test_input_order_does_not_change_output(self):
        names = [f"api-{i}-scope-intake-gate" for i in range(11)] + ["individual"]
        forward = topic_tree.build_topics(self.root, self.records(names))
        reverse = topic_tree.build_topics(self.root, self.records(reversed(names)))
        self.assertEqual(forward, reverse)

    def test_keys_disambiguate_normalization_and_bound_length(self):
        self.assertNotEqual(topic_tree.topic_key("subject", "C++"), topic_tree.topic_key("subject", "C#"))
        key = topic_tree.topic_key("subject", "long name " * 100)
        self.assertLess(len(key), 120)
        self.assertRegex(key, r"^[a-z0-9-]+$")

    def test_empty_inventory_has_no_topics(self):
        self.assertEqual(topic_tree.build_topics(self.root, {}), {})

    def test_duplicate_seed_is_rejected(self):
        self.write_hints([("one", "Subject", "Context"), ("one", "Another", "Context")])
        with self.assertRaisesRegex(ValueError, "duplicate"):
            topic_tree.load_hints(self.root)

    def test_invalid_hint_header_is_rejected(self):
        self.write_hints([])
        (self.root / "references/internet-topic-seeds-2026-09-30.csv").write_text("bad,header\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "invalid topic-label"):
            topic_tree.load_hints(self.root)

    def test_current_library_is_partitioned_once_with_bounded_lists(self):
        records, _, _ = sync_catalog.inventory(ROOT)
        topics = topic_tree.build_topics(ROOT, records)
        actual = [name for items in topics.values() for item in items for group in item.groups.values() for name in group]
        self.assertEqual(Counter(actual), Counter({name: 1 for name in records}))
        for (category, branch), items in topics.items():
            for item in items:
                for names in item.groups.values():
                    self.assertLessEqual(len(names), topic_tree.MAX_SECTION_SKILLS)
                    for name in names:
                        self.assertEqual(Path(records[name][0]).parts[1:3], (category, branch))


class TopicNavigationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "README.md").write_text("# Home", encoding="utf-8")
        names = ["demo-design-blueprint", "demo-option-comparison-matrix"]
        records = {name: (f"skills/software-development/backend-apis/{name}/SKILL.md", "Use when testing") for name in names}
        self.skills = [self.root / path for path, _ in records.values()]
        for path in self.skills:
            path.parent.mkdir(parents=True)
            path.write_text("# Skill content must not change", encoding="utf-8")
        counts = Counter({"software-development": 2})
        subcounts = Counter({("software-development", "backend-apis"): 2})
        topics = topic_tree.build_topics(self.root, records)
        self.pages = tree_navigation.branch_pages(self.root, records, counts, subcounts, topics)
        self.pages[self.root / "INDEX.md"] = tree_navigation.overview(counts, subcounts, from_root=True, topics=topics)
        self.pages[self.root / "skills/README.md"] = tree_navigation.overview(counts, subcounts, topics=topics)
        for path, text in self.pages.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
        self.topic = next(iter(topic_tree.topic_paths(self.root, topics)))
        self.subject = self.topic.parent.parent / "README.md"

    def errors(self):
        return validate_skills.validate_catalog(self.root, self.skills)

    def test_valid_nested_tree(self):
        self.assertEqual(self.errors(), [])

    def test_missing_anchor_is_detected(self):
        self.subject.write_text(self.subject.read_text().replace("#group-1", "#missing-group"), encoding="utf-8")
        self.assertTrue(any("missing navigation anchor" in error for error in self.errors()))

    def test_duplicate_skill_link_is_detected(self):
        with self.topic.open("a", encoding="utf-8") as stream:
            stream.write("\n[demo-design-blueprint](../demo-design-blueprint/SKILL.md)\n")
        self.assertTrue(any("duplicate skill link" in error for error in self.errors()))

    def test_missing_skill_listing_is_detected(self):
        self.topic.write_text(self.topic.read_text().replace("[demo-design-blueprint](../demo-design-blueprint/SKILL.md)", "removed"), encoding="utf-8")
        self.assertTrue(any("missing skill link" in error for error in self.errors()))

    def test_deleted_topic_is_detected(self):
        self.topic.unlink()
        self.assertTrue(any("cannot read navigation" in error for error in self.errors()))
        self.assertTrue(any("missing skill link" in error for error in self.errors()))

    def test_unreachable_topic_is_detected_even_when_skill_links_exist(self):
        for path in self.pages:
            if path != self.topic:
                path.write_text("\n".join(line for line in path.read_text().splitlines() if self.topic.name not in line), encoding="utf-8")
        self.assertTrue(any("unreachable navigation" in error for error in self.errors()))
        self.assertFalse(any("missing skill link" in error for error in self.errors()))

    def test_pruning_only_removes_obsolete_generated_topic_pages(self):
        obsolete = self.topic.parent / "obsolete.md"
        manual = self.topic.parent / "my-notes.md"
        obsolete.write_text(tree_navigation.MARKER, encoding="utf-8")
        manual.write_text("My own topic notes", encoding="utf-8")
        self.assertEqual(sync_catalog.obsolete_topic_pages(self.root, self.pages), [obsolete])
        with patch.object(sync_catalog, "ROOT", self.root), patch.object(sync_catalog, "planned_updates", return_value=self.pages), redirect_stdout(io.StringIO()):
            with patch.object(sys, "argv", ["sync_catalog.py", "--check"]):
                self.assertEqual(sync_catalog.main(), 1)
                self.assertTrue(obsolete.exists())
            with patch.object(sys, "argv", ["sync_catalog.py", "--write"]):
                self.assertEqual(sync_catalog.main(), 0)
        self.assertFalse(obsolete.exists())
        self.assertEqual(manual.read_text(), "My own topic notes")
        self.assertTrue(all(path.read_text() == "# Skill content must not change" for path in self.skills))

    def test_sync_refuses_user_authored_topic_path_collision(self):
        self.topic.write_text("User-owned page", encoding="utf-8")
        with patch.object(sync_catalog, "ROOT", self.root), patch.object(sync_catalog, "planned_updates", return_value=self.pages), redirect_stdout(io.StringIO()):
            with patch.object(sys, "argv", ["sync_catalog.py", "--write"]):
                self.assertEqual(sync_catalog.main(), 1)
        self.assertEqual(self.topic.read_text(), "User-owned page")


if __name__ == "__main__":
    unittest.main()
