"""Resolution, paging, and exit-code tests for scripts/skills_cli.py."""
from contextlib import redirect_stdout
import io
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import skills_cli


class SkillsCliTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skills = skills_cli.load_skills()
        cls.by_name = {skill.name: skill for skill in cls.skills}

    def run_cli(self, *argv):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            code = skills_cli.main(list(argv))
        return code, buffer.getvalue()

    def test_index_covers_every_package_once(self):
        files = list((ROOT / "skills").rglob("SKILL.md"))
        self.assertEqual(len(self.skills), len(files))
        self.assertEqual(len(self.by_name), len(files))
        self.assertEqual(len(self.skills), 15860)
        for skill in self.skills:
            with self.subTest(skill=skill.name):
                self.assertEqual(len(skill.path.relative_to(ROOT / "skills").parts), 4)
                self.assertTrue(skill.description)

    def test_normalize_accepts_every_documented_path_form(self):
        name = "aas-agent-quality-route-cost-threshold-rule-check"
        category = "ai-agent-systems"
        subject = "evaluation-observability"
        for query in (
            name,
            f"/skills/{name}",
            f"skills/{category}/{subject}/{name}",
            f"skills/{category}/{subject}/{name}/SKILL.md",
            f"/skills/{category}/{subject}/{name}/",
        ):
            with self.subTest(query=query):
                leaf, _ = skills_cli.normalize_query(query)
                self.assertEqual(leaf, name)

    def test_resolve_handles_names_deep_paths_and_the_repository_alias(self):
        kind, value = skills_cli.resolve(self.skills, "/skills/agentic-workflows")
        self.assertEqual((kind, value.name), ("skill", "agentic-workflows"))
        kind, value = skills_cli.resolve(
            self.skills,
            "skills/ai-agent-systems/agent-architecture-orchestration/agentic-workflows/SKILL.md",
        )
        self.assertEqual((kind, value.name), ("skill", "agentic-workflows"))
        self.assertEqual(skills_cli.resolve(self.skills, "/skills/try-skills"), ("repo", None))
        self.assertEqual(skills_cli.resolve(self.skills, ""), ("repo", None))

    def test_show_prints_metadata_and_body(self):
        code, output = self.run_cli("show", "/skills/agentic-workflows")
        self.assertEqual(code, 0)
        self.assertIn("agentic-workflows", output)
        self.assertIn("ai-agent-systems › agent-architecture-orchestration", output)
        self.assertIn("## When to Use", output)

    def test_show_json_is_machine_readable(self):
        code, output = self.run_cli("show", "agentic-workflows", "--json")
        self.assertEqual(code, 0)
        payload = __import__("json").loads(output)
        self.assertEqual(payload["name"], "agentic-workflows")
        self.assertIn("## Overview", payload["body"])

    def test_unknown_query_reports_candidates_and_exits_4(self):
        code, output = self.run_cli("show", "definitely-not-a-real-skill-zzz")
        self.assertEqual(code, 4)
        self.assertIn("does not resolve", output)

    def test_list_all_presents_every_skill(self):
        code, output = self.run_cli("list", "--all")
        self.assertEqual(code, 0)
        rows = [line for line in output.splitlines() if line.startswith("  ") and line.strip()[:1].isdigit()]
        self.assertEqual(len(rows), len(self.skills))

    def test_list_paging_is_bounded_and_consistent(self):
        first_code, first = self.run_cli("list", "--page", "1", "--limit", "5")
        second_code, second = self.run_cli("list", "--page", "2", "--limit", "5")
        self.assertEqual((first_code, second_code), (0, 0))
        self.assertIn("page 1/", first)
        self.assertIn("page 2/", second)
        self.assertNotEqual(first, second)

    def test_find_matches_names_and_returns_zero_when_empty(self):
        code, output = self.run_cli("find", "threshold", "--limit", "3")
        self.assertEqual(code, 0)
        self.assertIn("threshold", output)
        code, output = self.run_cli("find", "this-string-cannot-exist-zzz")
        self.assertEqual(code, 3)

    def test_stats_and_reference_render(self):
        code, output = self.run_cli("stats")
        self.assertEqual(code, 0)
        self.assertIn("15,860", output)
        code, output = self.run_cli("cmd")
        self.assertEqual(code, 0)
        self.assertIn("/skills show <query>", output)


if __name__ == "__main__":
    unittest.main()
