"""Regression tests for validation failures and non-destructive catalog updates."""
from collections import Counter
from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import sync_catalog  # noqa: E402
import validate_skills as validator  # noqa: E402


class ValidatorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.path = self.root / "skills/ai-agent-systems/tools-integrations/example-skill/SKILL.md"
        self.path.parent.mkdir(parents=True)
        description = "Use when " + " ".join(["evidence"] * 42)
        self.text = (f'---\nname: example-skill\ndescription: {json.dumps(description)}\n---\n'
                     '# Example\n\n## When to Use\n\nReview evidence.\n\n## Instructions\n\n'
                     'Inspect the task, verify the result, and report limitations.\n')
        self.path.write_text(self.text, encoding="utf-8")

    def append(self, text):
        self.path.write_text(self.text + text, encoding="utf-8")
        return validator.validate_skill(self.path)

    def test_valid_skill(self):
        self.assertEqual(validator.validate_skill(self.path), [])

    def test_missing_file_reports_instead_of_crashing(self):
        self.path.unlink()
        errors = validator.validate_skill(self.path)
        self.assertTrue(any("cannot read UTF-8" in error for error in errors))
        self.assertTrue(any("cannot stat" in error for error in errors))

    def test_non_utf8_reports_error(self):
        self.path.write_bytes(b"\xff\xfe")
        self.assertTrue(any("cannot read UTF-8" in error for error in validator.validate_skill(self.path)))

    def test_unclosed_frontmatter(self):
        self.path.write_text("---\nname: example-skill\n", encoding="utf-8")
        self.assertIn("frontmatter closing --- is missing", validator.validate_skill(self.path))

    def test_invalid_description_quotes(self):
        self.path.write_text(self.text.replace('description: "', 'description: ', 1), encoding="utf-8")
        self.assertIn("description must be double-quoted", validator.validate_skill(self.path))

    def test_duplicate_frontmatter_key(self):
        self.path.write_text(self.text.replace("name: example-skill", "name: example-skill\nname: example-skill"), encoding="utf-8")
        self.assertTrue(any("frontmatter keys" in error for error in validator.validate_skill(self.path)))

    def test_fenced_examples_do_not_count_as_headings_or_links(self):
        for fence in ("```", "~~~~"):
            with self.subTest(fence=fence):
                self.assertEqual(self.append(f'\n{fence}markdown\n# Example\n## Instructions\n[demo](missing.md)\n{fence}\n'), [])

    def test_shorter_or_different_fence_does_not_close_block(self):
        self.assertEqual(validator.prose_only("before\n````md\n```\n~~~\n# ignored\n````\nafter"), "before\nafter")

    def test_duplicate_real_heading_fails(self):
        self.assertIn("duplicate Markdown heading detected", self.append("\n## Instructions\n"))

    def test_missing_local_link(self):
        self.assertTrue(any("missing path" in error for error in self.append("\n[bad](missing.md)\n")))

    def test_malformed_url_does_not_crash(self):
        self.assertTrue(any("invalid link target" in error for error in self.append("\n[bad](https://[invalid)\n")))

    def test_encoded_local_link_and_title(self):
        (self.path.parent / "my notes.md").write_text("notes", encoding="utf-8")
        self.assertEqual(self.append('\n[notes](my%20notes.md#section "Notes")\n[notes](<my notes.md> "Notes")\n'), [])

    def test_remote_and_anchor_links_are_not_fetched(self):
        self.assertEqual(self.append("\n[web](https://example.invalid/path) [section](#instructions)\n"), [])

    def test_catalog_requires_exact_coverage(self):
        target = self.path.relative_to(self.root).as_posix()
        (self.root / "INDEX.md").write_text(f"| [example-skill]({target}) |\n", encoding="utf-8")
        self.assertEqual(validator.validate_catalog(self.root, [self.path]), [])
        (self.root / "INDEX.md").write_text(
            f"[wrong-name]({target})\n[example-skill]({target})\n[missing](skills/missing/SKILL.md)\n", encoding="utf-8")
        errors = validator.validate_catalog(self.root, [self.path])
        for expected in ("stale skill link", "duplicate skill link", "does not match"):
            self.assertTrue(any(expected in error for error in errors), errors)

    def test_catalog_missing_entry(self):
        (self.root / "INDEX.md").write_text("# Empty catalog\n", encoding="utf-8")
        self.assertTrue(any("missing skill link" in error for error in validator.validate_catalog(self.root, [self.path])))

    def test_missing_catalog_reports_error(self):
        self.assertTrue(any("cannot read INDEX.md" in error for error in validator.validate_catalog(self.root, [self.path])))

    def test_inventory_reads_actual_paths_without_mutating_skills(self):
        records, counts, subcounts = sync_catalog.inventory(self.root)
        self.assertEqual(set(records), {"example-skill"})
        self.assertEqual(counts, {"ai-agent-systems": 1})
        self.assertEqual(subcounts, {("ai-agent-systems", "tools-integrations"): 1})
        self.assertEqual(self.path.read_text(encoding="utf-8"), self.text)

    def test_sync_cli_defaults_to_read_only_and_write_is_idempotent(self):
        (self.root / "assets").mkdir()
        (self.root / "assets/agentic-skills-banner.svg").write_text("1 workflows for tool-using agents", encoding="utf-8")
        (self.root / "README.md").write_text("## Total Skills by Category\n\nStale\n\n## Repository Structure\n\nStale\n", encoding="utf-8")
        (self.root / "skills/README.md").write_text("Stale", encoding="utf-8")
        (self.root / "INDEX.md").write_text("# Skill router\n\n## Browse by category\n\nStale\n\n| If the task is about… | Load |\n|---|---|\n", encoding="utf-8")
        before = {path: path.read_bytes() for path in self.root.rglob("*") if path.is_file()}
        with patch.object(sync_catalog, "ROOT", self.root), redirect_stdout(io.StringIO()):
            with patch.object(sys, "argv", ["sync_catalog.py"]):
                self.assertEqual(sync_catalog.main(), 1)
            self.assertEqual(before, {path: path.read_bytes() for path in before})
            with patch.object(sys, "argv", ["sync_catalog.py", "--write"]):
                self.assertEqual(sync_catalog.main(), 0)
            with patch.object(sys, "argv", ["sync_catalog.py", "--check"]):
                self.assertEqual(sync_catalog.main(), 0)
        self.assertEqual(self.path.read_text(encoding="utf-8"), self.text)

    def test_json_cli_retains_failure_exit_code(self):
        output = io.StringIO()
        with patch.object(validator, "ROOT", self.root), patch.object(validator, "SKILLS_ROOT", self.root / "skills"):
            with patch.object(sys, "argv", ["validate_skills.py", "--json"]), redirect_stdout(output):
                self.assertEqual(validator.main(), 1)
        report = json.loads(output.getvalue())
        self.assertEqual(report["skills_scanned"], 1)
        self.assertGreater(report["issues"], 0)
        self.assertEqual(report["issues"], len(report["errors"]))

    def test_inventory_refuses_empty_collection(self):
        self.path.unlink()
        with self.assertRaisesRegex(ValueError, "no skill files"):
            sync_catalog.inventory(self.root)

    def test_inventory_refuses_duplicate_names(self):
        duplicate = self.root / "skills/ai-agent-systems/safety-governance/example-skill/SKILL.md"
        duplicate.parent.mkdir(parents=True)
        duplicate.write_text(self.text, encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "duplicate skill name"):
            sync_catalog.inventory(self.root)


class CatalogSyncTests(unittest.TestCase):
    def test_sync_repairs_drift_and_is_idempotent(self):
        text = ("# Skill router\n\n## Browse by category\n\nOld counts\n\n"
                "| If the task is about… | Load |\n|---|---|\n"
                "| Keep this custom routing description | [existing](skills/old/existing/SKILL.md) |\n"
                "| Duplicate | [existing](skills/old/existing/SKILL.md) |\n"
                "| Stale | [gone](skills/old/gone/SKILL.md) |\n")
        records = {"existing": ("skills/ai-agent-systems/tools-integrations/existing/SKILL.md", "unused"),
                   "new": ("skills/ai-agent-systems/tools-integrations/new/SKILL.md", "A | B")}
        counts = Counter({"ai-agent-systems": 2})
        subcounts = Counter({("ai-agent-systems", "tools-integrations"): 2})
        result = sync_catalog.sync_index(text, records, counts, subcounts)
        self.assertIn("Keep this custom routing description", result)
        self.assertNotIn("Duplicate", result)
        self.assertNotIn("gone/SKILL.md", result)
        self.assertIn("A &#124; B", result)
        self.assertEqual(len(sync_catalog.SKILL_LINK.findall(result)), 2)
        self.assertEqual(sync_catalog.sync_index(result, records, counts, subcounts), result)

    def test_sync_refuses_unrecognized_index_structure(self):
        with self.assertRaisesRegex(ValueError, "browse section"):
            sync_catalog.sync_index("# Not a router", {}, Counter(), Counter())

    def test_total_update_preserves_unrelated_numbers(self):
        text = 'alt="16,500+ skills"; 16,500+ task-focused workflows; 40 skills per list; 10,000 historical additions; badge/SKILLS-16%2C500%2B-color'
        self.assertEqual(sync_catalog.update_total(text, 15860),
                         'alt="15,860 skills"; 15,860 task-focused workflows; 40 skills per list; 10,000 historical additions; badge/SKILLS-15%2C860-color')

    def test_missing_readme_section_is_not_silently_ignored(self):
        with self.assertRaisesRegex(ValueError, "missing README section"):
            sync_catalog.replace_section("# README", "Repository Structure", "replacement")

    def test_current_metadata_has_no_drift(self):
        for path, expected in sync_catalog.planned_updates(ROOT).items():
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertEqual(path.read_text(encoding="utf-8"), expected)

    def test_current_catalog_covers_exactly_the_current_skills(self):
        self.assertEqual(validator.validate_catalog(ROOT, validator.discover_skills()), [])


if __name__ == "__main__":
    unittest.main()
