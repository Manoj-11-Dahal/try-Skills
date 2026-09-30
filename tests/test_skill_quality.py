"""Repository-level tests for the agentic skill collection."""
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import validate_skills  # noqa: E402
import build_1000_skills_batches14_23 as industry_batch_builder  # noqa: E402


class CatalogIndexParserTests(unittest.TestCase):
    def test_parses_both_legacy_and_appended_catalog_row_layouts(self):
        text = """# Catalog
| Legacy task description | [legacy-skill](skills/legacy-skill/SKILL.md) |
| [appended-skill](skills/appended-skill/SKILL.md) | Appended task description |
| [nested-skill](skills/data-analytics/databases-storage/nested-skill/SKILL.md) | Nested task description |
"""
        self.assertEqual(
            industry_batch_builder.parse_index_rows(text),
            [
                ("appended-skill", "Appended task description"),
                ("legacy-skill", "Legacy task description"),
                ("nested-skill", "Nested task description"),
            ],
        )


class SkillQualityTests(unittest.TestCase):
    def test_repository_has_skills(self):
        self.assertGreaterEqual(len(validate_skills.discover_skills()), 1)

    def test_all_skills_pass_contract(self):
        for path in validate_skills.discover_skills():
            with self.subTest(skill=path.parent.name):
                self.assertEqual(validate_skills.validate_skill(path), [])

    def test_skills_are_nested_in_one_of_nine_categories(self):
        paths = validate_skills.discover_skills()
        self.assertEqual(set(path.relative_to(validate_skills.SKILLS_ROOT).parts[0] for path in paths), set(validate_skills.CATEGORIES))
        self.assertTrue(all(len(path.relative_to(validate_skills.SKILLS_ROOT).parts) == 4 for path in paths))
        for path in paths:
            parts = path.relative_to(validate_skills.SKILLS_ROOT).parts
            self.assertIn(parts[1], validate_skills.SUBCATEGORY_LABELS[parts[0]])

    def test_directory_and_frontmatter_names_match(self):
        for path in validate_skills.discover_skills():
            name, _, _, errors = validate_skills.parse_frontmatter(path)
            with self.subTest(skill=path.parent.name):
                self.assertEqual(errors, [])
                self.assertEqual(name, path.parent.name)

    def test_descriptions_have_use_conditions_and_minimum_units(self):
        for path in validate_skills.discover_skills():
            name, description, body, _ = validate_skills.parse_frontmatter(path)
            with self.subTest(skill=name):
                self.assertGreaterEqual(validate_skills.content_units(description), 40)
                self.assertRegex(description, r"(?i)\bUse when\b")
                self.assertIn("## When to Use", body)

    def test_internal_links_resolve(self):
        for path in validate_skills.discover_skills():
            with self.subTest(skill=path.parent.name):
                self.assertEqual(validate_skills.validate_skill(path), [])


if __name__ == "__main__":
    unittest.main()
