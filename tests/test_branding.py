"""README and native SVG integrity, accessibility, and synchronized counts."""
from collections import Counter
from pathlib import Path
import re
import sys
from types import SimpleNamespace
import unittest
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import sync_catalog
from topic_tree import build_topics


class BrandingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.banner = (ROOT / "assets/agentic-skills-banner.svg").read_text(encoding="utf-8")
        cls.svg = ET.fromstring(cls.banner)
        records, cls.counts, cls.subcounts = sync_catalog.inventory(ROOT)
        cls.topics = build_topics(ROOT, records)
        cls.values = sync_catalog.catalog_counts(cls.counts, cls.subcounts, cls.topics)

    def test_svg_is_accessible_and_scalable(self):
        self.assertEqual(self.svg.tag, "{http://www.w3.org/2000/svg}svg")
        self.assertEqual(self.svg.attrib["role"], "img")
        width, height = map(float, self.svg.attrib["viewBox"].split()[2:])
        self.assertGreater(width, height)
        by_id = {node.attrib["id"]: node for node in self.svg.iter() if "id" in node.attrib}
        for reference in self.svg.attrib["aria-labelledby"].split():
            self.assertIn(reference, by_id)
            self.assertTrue("".join(by_id[reference].itertext()).strip())

    def test_svg_is_self_contained_without_active_content(self):
        for node in self.svg.iter():
            self.assertNotIn(node.tag.split("}")[-1], {"script", "foreignObject", "image"})
            for attribute, value in node.attrib.items():
                self.assertFalse(attribute.lower().startswith("on"))
                if attribute.split("}")[-1] in {"href", "src"}:
                    self.assertTrue(value.startswith("#"))

    def test_banner_stats_match_the_current_inventory(self):
        nodes = [node for node in self.svg.iter() if "data-count" in node.attrib]
        self.assertEqual(len(nodes), 5)
        actual = {node.attrib["data-count"]: "".join(node.itertext()) for node in nodes}
        self.assertEqual(actual, {key: f"{value:,}" for key, value in self.values.items()})
        self.assertEqual(sync_catalog.update_banner(self.banner, self.counts, self.subcounts, self.topics), self.banner)

    def test_banner_stats_update_without_changing_geometry(self):
        counts = Counter({"example": 3})
        subcounts = Counter({("example", "one"): 3})
        topics = {("example", "one"): [SimpleNamespace(groups={"first": [], "second": []})]}
        changed = ET.fromstring(sync_catalog.update_banner(self.banner, counts, subcounts, topics))
        actual = {node.attrib["data-count"]: node.text for node in changed.iter() if "data-count" in node.attrib}
        self.assertEqual(actual, {"categories": "1", "subjects": "1", "topics": "1", "groups": "2", "skills": "3"})
        self.assertEqual(changed.attrib, self.svg.attrib)
        for before, after in zip(self.svg.iter(), changed.iter()):
            self.assertEqual(before.attrib, after.attrib)

    def test_malformed_banner_stat_contract_is_rejected(self):
        variants = [
            self.banner.replace('data-count="groups"', 'data-count="unknown"'),
            self.banner.replace('data-count="groups"', 'data-count="skills"'),
            self.banner.replace('</svg>', '<text data-count="skills">0</text></svg>'),
        ]
        for banner in variants:
            with self.subTest(banner=banner[-90:]):
                with self.assertRaises(ValueError):
                    sync_catalog.update_banner(banner, self.counts, self.subcounts, self.topics)

    def test_readme_summary_uses_the_same_statistics_as_banner(self):
        summary = sync_catalog.library_summary(self.counts, self.subcounts, self.topics)
        row = "| " + " | ".join(f"**{value:,}**" for value in self.values.values()) + " |"
        self.assertIn(row, summary)
        self.assertIn(summary.strip(), (ROOT / "README.md").read_text(encoding="utf-8"))

    def test_readme_local_links_and_images_exist(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        targets = re.findall(r"\[[^\]]*\]\(([^)]+)\)", text)
        targets += re.findall(r'(?:href|src)="([^"]+)"', text)
        for target in targets:
            parsed = urlsplit(target)
            if not parsed.scheme and not parsed.netloc and parsed.path:
                with self.subTest(target=target):
                    self.assertTrue((ROOT / unquote(parsed.path)).exists())
        self.assertIn('src="assets/agentic-skills-banner.svg"', text)
        self.assertIn("## Quick Start", text)
        self.assertIn("at most **40 skills**", text)


if __name__ == "__main__":
    unittest.main()
