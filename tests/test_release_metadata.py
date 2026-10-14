"""Keep the prepared version, changelog, README, and release notes consistent."""
from pathlib import Path
import re
import unittest
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


class ReleaseMetadataTests(unittest.TestCase):
    def test_version_and_release_documents_agree(self):
        raw = (ROOT / "VERSION").read_text(encoding="utf-8")
        version = raw.strip()
        self.assertEqual(raw, version + "\n")
        number = r"(?:0|[1-9][0-9]*)"
        self.assertRegex(version, rf"^{number}\.{number}\.{number}$")
        notes_path = ROOT / "releases" / f"v{version}.md"
        notes = notes_path.read_text(encoding="utf-8")
        self.assertTrue(notes.startswith(f"# Agentic Skills v{version} — "))
        self.assertIn(f"## [{version}]", (ROOT / "CHANGELOG.md").read_text(encoding="utf-8"))
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn(f"`v{version}`", readme)
        self.assertIn(f"(releases/v{version}.md)", readme)

    def test_release_document_local_links_resolve(self):
        documents = [ROOT / "CHANGELOG.md", *sorted((ROOT / "releases").glob("*.md"))]
        for document in documents:
            text = document.read_text(encoding="utf-8")
            for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
                parsed = urlsplit(target)
                if not parsed.scheme and not parsed.netloc and parsed.path:
                    with self.subTest(document=document.name, target=target):
                        self.assertTrue((document.parent / unquote(parsed.path)).exists())


if __name__ == "__main__":
    unittest.main()
