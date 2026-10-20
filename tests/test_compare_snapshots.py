"""Snapshot comparison: regression detection and content-loss classification."""
from contextlib import redirect_stdout
import io
from pathlib import Path
import sys
import tarfile
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import compare_snapshots as compare


DESCRIPTION = (
    'description: "Use when comparing snapshots to detect content regressions '
    'in a reproducible way for maintenance review."'
)


def package(name: str, body: str) -> str:
    return f"---\nname: {name}\n{DESCRIPTION}\n---\n\n# {name}\n\n{body}\n"


class CompareTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def write(self, root: Path, name: str, body: str) -> None:
        path = root / "software-development" / "backend-apis" / name / "SKILL.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(package(name, body), encoding="utf-8")

    def test_removed_package_is_a_regression(self):
        before, after = self.root / "before", self.root / "after"
        self.write(before, "kept", "## Overview\n\n" + "Real text. " * 30)
        self.write(before, "dropped", "## Overview\n\n" + "Real text. " * 30)
        self.write(after, "kept", "## Overview\n\n" + "Real text. " * 30)
        result = compare.compare(compare.load(before), compare.load(after))
        self.assertEqual(result["removed"], ["dropped"])
        self.assertTrue(any("missing" in issue for issue in compare.regressions(result)))

    def test_added_package_is_not_a_regression(self):
        before, after = self.root / "before", self.root / "after"
        self.write(before, "one", "## Overview\n\n" + "Text. " * 30)
        self.write(after, "one", "## Overview\n\n" + "Text. " * 30)
        self.write(after, "two", "## Overview\n\n" + "Text. " * 30)
        result = compare.compare(compare.load(before), compare.load(after))
        self.assertEqual(result["added"], ["two"])
        self.assertEqual(compare.regressions(result), [])

    def test_new_in_file_repetition_is_a_regression(self):
        before, after = self.root / "before", self.root / "after"
        paragraph = "A long substantive passage. " * 8
        self.write(before, "one", f"## Overview\n\n{paragraph}\n\n## Scope\n\n{paragraph}")
        self.write(before, "one", f"## Overview\n\n{paragraph}")
        self.write(after, "one", f"## Overview\n\n{paragraph}\n\n## Scope\n\n{paragraph}")
        result = compare.compare(compare.load(before), compare.load(after))
        self.assertGreater(result["after"]["duplicate_chars"], 0)
        self.assertTrue(any("repetition grew" in issue for issue in compare.regressions(result)))

    def test_placeholder_growth_is_a_regression(self):
        before, after = self.root / "before", self.root / "after"
        self.write(before, "one", "## Overview\n\n" + "Real text. " * 30)
        self.write(after, "one", "## Overview\n\n" + "Real text. " * 30
                   + "\n\n## Inputs\n\nNot specified in source skill.\n")
        result = compare.compare(compare.load(before), compare.load(after))
        self.assertEqual(result["after"]["placeholder_files"], 1)
        self.assertTrue(any("placeholder" in issue for issue in compare.regressions(result)))

    def test_renamed_section_is_not_reported_as_content_loss(self):
        before, after = self.root / "before", self.root / "after"
        prose = "Report the implemented subset, conventions, and declared tolerances. " * 2
        self.write(before, "one", f"## Acceptance Evidence\n\n{prose}")
        self.write(after, "one", f"## Success Criteria\n\n### Preserved source section: Acceptance\n\n{prose}")
        result = compare.compare(compare.load(before), compare.load(after))
        self.assertEqual(result["content_losses"], [])
        self.assertTrue(result["renamed_sections"])
        self.assertEqual(compare.regressions(result), [])

    def test_genuinely_removed_prose_is_reported(self):
        before, after = self.root / "before", self.root / "after"
        self.write(before, "one", "## Acceptance Evidence\n\n" + "Lost prose about tolerances. " * 5)
        self.write(after, "one", "## Success Criteria\n\nCompletely different wording here.\n")
        result = compare.compare(compare.load(before), compare.load(after))
        self.assertEqual(len(result["content_losses"]), 1)
        self.assertTrue(any("lost substantive content" in issue for issue in compare.regressions(result)))

    def test_dropped_placeholder_section_counts_as_improvement(self):
        before, after = self.root / "before", self.root / "after"
        self.write(before, "one", "## Overview\n\n" + "Real text. " * 30
                   + "\n\n## Related Skills\n\nNot specified in source skill.\n")
        self.write(after, "one", "## Overview\n\n" + "Real text. " * 30)
        result = compare.compare(compare.load(before), compare.load(after))
        self.assertEqual(result["content_losses"], [])
        self.assertEqual(compare.regressions(result), [])
        self.assertTrue(result["dropped_placeholder_sections"])

    def test_archive_and_directory_sources_agree(self):
        tree = self.root / "tree"
        self.write(tree, "one", "## Overview\n\n" + "Real text. " * 30)
        archive = self.root / "snapshot.tar.gz"
        with tarfile.open(archive, "w:gz") as handle:
            handle.add(tree, arcname="skills")
        from_archive = compare.load(archive)
        from_directory = compare.load(tree)
        self.assertEqual(sorted(from_archive), sorted(from_directory))
        self.assertEqual(from_archive["one"].text, from_directory["one"].text)

    def test_cli_exit_codes(self):
        before = self.root / "before"
        self.write(before, "one", "## Overview\n\n" + "Real text. " * 30)
        current = self.root / "current"
        self.write(current, "one", "## Overview\n\n" + "Real text. " * 30)
        self.write(current, "extra", "## Overview\n\n" + "Real text. " * 30)
        original = sys.argv
        self.addCleanup(setattr, sys, "argv", original)
        sys.argv = ["compare", str(before), "--new", str(current), "--quiet"]
        with redirect_stdout(io.StringIO()) as stream:
            self.assertEqual(compare.main(), 0)
        self.assertIn("no regression", stream.getvalue())

        sys.argv = ["compare", str(before), "--new", str(current),
                    "--fail-on-regression", "--json"]
        (current / "software-development/backend-apis/one/SKILL.md").unlink()
        with redirect_stdout(io.StringIO()):
            self.assertEqual(compare.main(), 1)


if __name__ == "__main__":
    unittest.main()
