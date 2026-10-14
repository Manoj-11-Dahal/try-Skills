"""Tree navigation, category mapping, and safe migration regression tests."""
from collections import Counter
import csv
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import migrate_category_tree as migration
import skill_categories
from skill_taxonomy import SUBCATEGORY_LABELS, LEGACY_SUBCATEGORY_LABELS, relative_skill_path
from skill_tree import CATEGORIES, destination_category
import sync_catalog
import tree_navigation
from topic_tree import build_topics, topic_paths
import validate_skills


class TreeTests(unittest.TestCase):
    def test_all_old_branches_have_one_current_destination(self):
        before = {(category, branch) for category, branches in LEGACY_SUBCATEGORY_LABELS.items() for branch in branches}
        after = {(category, branch) for category, branches in SUBCATEGORY_LABELS.items() for branch in branches}
        self.assertEqual(len(before), 65)
        self.assertEqual(len(after), 65)
        self.assertEqual({(destination_category(cat, branch), branch) for cat, branch in before}, after)
        self.assertEqual(len(CATEGORIES), 12)

    def test_classification_and_path_helpers_use_new_categories(self):
        examples = {
            "authorizedsec-test": ("cybersecurity", "authorized-security-testing"),
            "musiclab-test": ("music-audio", "music-and-audio-production"),
            "soundlab-test": ("music-audio", "sound-design-and-effects"),
            "deepresearch-test": ("science-research", "deep-research-and-evidence-synthesis"),
            "trial-ops-test": ("healthcare-medicine", "trials-research-methods"),
        }
        for slug, (category, branch) in examples.items():
            with self.subTest(slug=slug):
                self.assertEqual(skill_categories.category_for_skill(slug), category)
                self.assertEqual(relative_skill_path(category, slug), f"skills/{category}/{branch}/{slug}/SKILL.md")

    def test_old_category_path_helper_redirects_moved_branch(self):
        self.assertEqual(relative_skill_path("cloud-infrastructure-security", "authorizedsec-test"),
                         "skills/cybersecurity/authorized-security-testing/authorizedsec-test/SKILL.md")

    def test_tree_connector_at_last_category_is_closed(self):
        counts = Counter({"music-audio": 2, "education-public-service": 1})
        subcounts = Counter({("music-audio", "sound-design-and-effects"): 2,
                             ("education-public-service", "curriculum-instruction"): 1})
        self.assertEqual(tree_navigation.tree_lines(counts, subcounts), [
            "skills/", "├── music-audio/ (2)", "│   └── sound-design-and-effects/ (2)",
            "└── education-public-service/ (1)", "    └── curriculum-instruction/ (1)",
        ])

    def test_tree_summaries_escape_table_and_html_syntax(self):
        self.assertEqual(tree_navigation.compact(" A | <B>\n C "), "A &#124; &lt;B&gt; C")

    def test_navigation_is_split_into_small_pages(self):
        pages = [ROOT / "INDEX.md", ROOT / "skills/README.md"]
        pages += list((ROOT / "skills").glob("*/README.md"))
        pages += list((ROOT / "skills").glob("*/*/README.md"))
        records, _, _ = sync_catalog.inventory(ROOT)
        topic_indexes = topic_paths(ROOT, build_topics(ROOT, records))
        self.assertEqual(len(pages), 79)
        pages.extend(sorted(topic_indexes))
        self.assertGreater(len(topic_indexes), 0)
        for page in pages:
            with self.subTest(page=page):
                self.assertLess(page.stat().st_size, 500_000, "split the branch page before it becomes too large to browse")

    def test_migration_receipt_records_preserved_content(self):
        self.assertNotIn(b"\r\n", (ROOT / migration.RECEIPT).read_bytes())
        with (ROOT / migration.RECEIPT).open(encoding="utf-8", newline="") as stream:
            rows = list(csv.DictReader(stream))
        self.assertEqual(len(rows), 3677)
        for row in rows:
            with self.subTest(path=row["new_path"]):
                self.assertEqual(Path(row["old_path"]).parent.name, Path(row["new_path"]).parent.name)
                self.assertEqual(row["sha256_before"], row["sha256_after"])
                self.assertRegex(row["sha256_after"], r"^[0-9a-f]{64}$")


class MigrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.old = self.root / "skills/cloud-infrastructure-security/security-privacy/example-skill/SKILL.md"
        self.new = self.root / "skills/cybersecurity/security-privacy/example-skill/SKILL.md"
        self.old.parent.mkdir(parents=True)
        self.body = '---\nname: example-skill\ndescription: "Use when testing migration safety."\n---\n# Example\n'
        self.old.write_text(self.body, encoding="utf-8")
        (self.root / "README.md").write_text("Overview", encoding="utf-8")
        (self.root / "references").mkdir()

    def test_plan_is_read_only(self):
        changes = migration.plan(self.root)
        self.assertEqual(len(changes), 1)
        self.assertEqual(changes[0][:2], (self.old, self.new))
        self.assertTrue(self.old.exists())
        self.assertFalse(self.new.exists())

    def test_destination_collision_is_rejected(self):
        self.new.parent.mkdir(parents=True)
        with self.assertRaisesRegex(ValueError, "collision"):
            migration.plan(self.root)
        self.assertTrue(self.old.exists())

    def test_additional_resources_require_review(self):
        (self.old.parent / "notes.md").write_text("notes", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "additional resources"):
            migration.plan(self.root)

    def test_failed_navigation_update_rolls_back_package_moves(self):
        changes = migration.plan(self.root)
        with patch.object(sync_catalog, "planned_updates", side_effect=ValueError("simulated failure")):
            with self.assertRaisesRegex(ValueError, "simulated failure"):
                migration.apply(self.root, changes)
        self.assertEqual(self.old.read_text(encoding="utf-8"), self.body)
        self.assertFalse(self.new.exists())
        self.assertEqual((self.root / "README.md").read_text(encoding="utf-8"), "Overview")
        self.assertFalse((self.root / migration.RECEIPT).exists())

    def test_successful_move_is_idempotent_and_writes_receipt(self):
        changes = migration.plan(self.root)
        with patch.object(sync_catalog, "planned_updates", return_value={}):
            migration.apply(self.root, changes)
        self.assertFalse(self.old.exists())
        self.assertEqual(self.new.read_text(encoding="utf-8"), self.body)
        self.assertEqual(migration.plan(self.root), [])
        self.assertTrue((self.root / migration.RECEIPT).exists())
        self.assertNotIn(b"\r\n", (self.root / migration.RECEIPT).read_bytes())

    def test_rebase_cross_category_link(self):
        source = self.root / "skills/ai-agent-systems/tools-integrations/tool-skill/SKILL.md"
        source.parent.mkdir(parents=True)
        text = '[security](../../../cloud-infrastructure-security/security-privacy/example-skill/SKILL.md#scope "Scope")'
        self.assertEqual(migration.rebase_links(text, self.root, source, source),
                         '[security](../../../cybersecurity/security-privacy/example-skill/SKILL.md#scope "Scope")')

    def test_relative_reference_link_at_same_depth_is_unchanged(self):
        reference = self.root / "references/source.md"
        reference.write_text("source", encoding="utf-8")
        text = "[source](../../../../references/source.md)"
        self.assertEqual(migration.rebase_links(text, self.root, self.old, self.new), text)


class TreeValidationTests(unittest.TestCase):
    def test_missing_branch_page_and_broken_links_are_detected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            skill = root / "skills/music-audio/sound-design-and-effects/example/SKILL.md"
            skill.parent.mkdir(parents=True)
            skill.write_text("# Example", encoding="utf-8")
            (root / "README.md").write_text("# Home", encoding="utf-8")
            records = {"example": (skill.relative_to(root).as_posix(), "Use when testing the tree")}
            counts = Counter({"music-audio": 1})
            subcounts = Counter({("music-audio", "sound-design-and-effects"): 1})
            pages = tree_navigation.branch_pages(root, records, counts, subcounts)
            pages[root / "INDEX.md"] = tree_navigation.overview(counts, subcounts, from_root=True)
            pages[root / "skills/README.md"] = tree_navigation.overview(counts, subcounts)
            for path, text in pages.items():
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text, encoding="utf-8")
            self.assertEqual(validate_skills.validate_catalog(root, [skill]), [])
            orphan = root / "skills/retired-category/README.md"
            orphan.parent.mkdir()
            orphan.write_text(tree_navigation.MARKER, encoding="utf-8")
            self.assertTrue(any("orphaned navigation" in error for error in validate_skills.validate_catalog(root, [skill])))
            orphan.unlink()
            (skill.parent.parent / "README.md").unlink()
            errors = validate_skills.validate_catalog(root, [skill])
            self.assertTrue(any("cannot read navigation" in error for error in errors))
            self.assertTrue(any("stale navigation link" in error for error in errors))
            self.assertTrue(any("unreachable navigation" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
