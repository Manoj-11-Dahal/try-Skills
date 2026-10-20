"""Content-quality audit: detection, grading, and CLI contract."""
import io
from contextlib import redirect_stdout
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import audit_skill_quality as audit


SHARED = (
    "This workflow requires the operator to record the target, the owner, the "
    "authorized scope, and the verification evidence before any action is taken."
)


def skill(body: str) -> str:
    description = (
        '"Use when a team needs to verify behaviour for a reviewable artifact. '
        'It records evidence and stops when authority is unclear. Use configured '
        'read and write capabilities only when authorized and relevant."'
    )
    return f"---\nname: temp-skill\ndescription: {description}\n---\n\n{body}"


class AuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self._root, self._skills = audit.ROOT, audit.SKILLS_ROOT
        audit.ROOT = self.root
        audit.SKILLS_ROOT = self.root / "skills"
        self.addCleanup(setattr, audit, "ROOT", self._root)
        self.addCleanup(setattr, audit, "SKILLS_ROOT", self._skills)

    def write(self, name: str, body: str) -> Path:
        path = self.root / "skills" / "software-development" / "backend-apis" / name / "SKILL.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(skill(body), encoding="utf-8")
        return path

    def test_repeated_paragraph_is_a_warning(self):
        path = self.write("demo", (
            "# Demo\n\n## Overview\n\n" + "Intro text. " * 20 + "\n\n"
            "## Instructions\n\n" + "Step text. " * 30 + "\n\n"
            "## Stop Conditions\n\n" + "Step text. " * 30 + "\n"
        ))
        findings, _ = audit.audit([path])
        codes = {finding.code for finding in findings}
        self.assertIn("duplicate_paragraph", codes)
        self.assertTrue(all(f.level == "WARN" for f in findings if f.code == "duplicate_paragraph"))

    def test_single_copy_is_not_flagged(self):
        path = self.write("clean", (
            "# Clean\n\n## Overview\n\n" + "Unique intro. " * 20 + "\n\n"
            "## Instructions\n\n" + "Unique steps. " * 30 + "\n"
        ))
        findings, _ = audit.audit([path])
        self.assertFalse([f for f in findings if f.code == "duplicate_paragraph"])

    def test_placeholder_sections_are_reported_as_info(self):
        path = self.write("placeholder", (
            "# Placeholder\n\n## Overview\n\n" + "Real overview. " * 20 + "\n\n"
            "## Inputs\n\n**Required:** Not specified in source skill.\n\n"
            "## Examples\n\nNot specified in source skill. The original provided no "
            "input/output example, and none has been invented.\n"
        ))
        findings, stats = audit.audit([path])
        placeholder = [f for f in findings if f.code == "placeholder_sections"]
        self.assertEqual(len(placeholder), 1)
        self.assertEqual(placeholder[0].level, "INFO")
        self.assertIn("Inputs", placeholder[0].detail["sections"])
        self.assertIn("Examples", placeholder[0].detail["sections"])
        self.assertEqual(stats["empty_sections"], 2)

    def test_active_markup_is_an_error(self):
        path = self.write("unsafe", (
            "# Unsafe\n\n## Overview\n\n" + "Text. " * 30 + "\n\n"
            "## Instructions\n\n<script>alert(1)</script>\n"
        ))
        findings, _ = audit.audit([path])
        errors = [f for f in findings if f.level == "ERROR"]
        self.assertEqual([f.code for f in errors], ["unsafe_embedded_markup"])

    def test_boilerplate_is_measured_across_the_corpus(self):
        for index in range(3):
            self.write(f"shared-{index}", (
                "# Shared\n\n## Overview\n\n" + SHARED + "\n\n"
                "## Instructions\n\n" + f"Distinct step set {index}. " * 20 + "\n"
            ))
        paths = sorted(audit.discover_skills(self.root / "skills"))
        findings, stats = audit.audit(paths, boilerplate_min_files=2)
        self.assertEqual(stats["skills"], 3)
        self.assertEqual(stats["boilerplate_paragraphs"], 1)
        self.assertGreater(stats["boilerplate_share"], 0)
        # Shared text across files is corpus boilerplate, not a within-file duplicate.
        self.assertFalse(any(f.code == "duplicate_paragraph" for f in findings))

    def test_fenced_code_is_ignored(self):
        block = "```text\n" + "echo repeated line\n" * 20 + "```\n"
        paragraphs = audit.paragraphs(f"# T\n\n## A\n\n{block}\n## B\n\n{block}\n")
        self.assertEqual(paragraphs, [])

    def test_cli_exit_zero_without_errors_and_strict_fails_on_warnings(self):
        self.write("demo", (
            "# Demo\n\n## Overview\n\n" + "Body. " * 40 + "\n\n"
            "## Instructions\n\n" + "Step text. " * 30 + "\n\n"
            "## Stop Conditions\n\n" + "Step text. " * 30 + "\n"
        ))
        original = sys.argv
        self.addCleanup(setattr, sys, "argv", original)
        for argv, expected in ((["audit"], 0), (["audit", "--strict"], 1)):
            sys.argv = argv
            stream = io.StringIO()
            with redirect_stdout(stream):
                self.assertEqual(audit.main(), expected)
            self.assertIn("skills scanned", stream.getvalue())


if __name__ == "__main__":
    unittest.main()
