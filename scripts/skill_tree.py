"""Current category tree and explicit, non-heuristic migration from the old tree."""
from __future__ import annotations

CATEGORIES = {
    "ai-agent-systems": "AI & Agent Systems",
    "software-development": "Software & Development",
    "cloud-infrastructure": "Cloud & Infrastructure",
    "cybersecurity": "Cybersecurity & Privacy",
    "data-analytics": "Data & Analytics",
    "business-operations": "Business & Operations",
    "science-research": "Science & Research",
    "healthcare-medicine": "Healthcare & Medicine",
    "engineering-industry": "Engineering & Industry",
    "creative-media-design": "Creative, Media & Design",
    "music-audio": "Music & Audio",
    "education-public-service": "Education & Public Service",
}

CATEGORY_DESCRIPTIONS = {
    "ai-agent-systems": "Design, orchestrate, evaluate, and govern tool-using agents, memory, reasoning, and MCP integrations.",
    "software-development": "Build applications, interfaces, APIs, and developer tooling; test and release software.",
    "cloud-infrastructure": "Operate cloud platforms, containers, networks, and reliable delivery infrastructure.",
    "cybersecurity": "Protect systems and privacy; perform explicitly authorized security assessments. Skills never grant authorization.",
    "data-analytics": "Engineer, store, govern, analyze, and visualize data; work with geospatial information and machine learning.",
    "business-operations": "Plan and run finance, product, sales, people, legal, retail, supply-chain, and insurance operations.",
    "science-research": "Investigate life and physical sciences, evaluate evidence, and conduct reproducible research.",
    "healthcare-medicine": "Support clinical operations, medical imaging, and clinical-trial workflows. Not a substitute for qualified clinical judgment.",
    "engineering-industry": "Design and operate agriculture, buildings, energy systems, manufacturing, electronics, and robotics.",
    "creative-media-design": "Create visual design, user experiences, games, 3D assets, writing, and video; mixed audiovisual workflows stay here.",
    "music-audio": "Produce music and audio, design sound, and build effects workflows.",
    "education-public-service": "Develop learning and assessment, civic services, public operations, and community programs.",
}

CATEGORY_RENAMES = {
    "cloud-infrastructure-security": "cloud-infrastructure",
    "science-health-research": "science-research",
}
BRANCH_MOVES = {
    ("cloud-infrastructure-security", "security-privacy"): "cybersecurity",
    ("cloud-infrastructure-security", "authorized-security-testing"): "cybersecurity",
    ("science-health-research", "clinical-healthcare"): "healthcare-medicine",
    ("science-health-research", "trials-research-methods"): "healthcare-medicine",
    ("science-health-research", "medical-imaging"): "healthcare-medicine",
    ("creative-media-design", "music-and-audio-production"): "music-audio",
    ("creative-media-design", "sound-design-and-effects"): "music-audio",
}
LEGACY_PARENT = {
    "cloud-infrastructure": "cloud-infrastructure-security",
    "cybersecurity": "cloud-infrastructure-security",
    "science-research": "science-health-research",
    "healthcare-medicine": "science-health-research",
    "music-audio": "creative-media-design",
}


def destination_category(category: str, subcategory: str) -> str:
    return BRANCH_MOVES.get((category, subcategory), CATEGORY_RENAMES.get(category, category))


def migrate_labels(legacy: dict[str, dict[str, str]]) -> dict[str, dict[str, str]]:
    tree: dict[str, dict[str, str]] = {category: {} for category in CATEGORIES}
    for category, branches in legacy.items():
        for branch, label in branches.items():
            tree[destination_category(category, branch)][branch] = label
    return tree
