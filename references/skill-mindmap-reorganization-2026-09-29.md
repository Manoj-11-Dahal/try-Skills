# Skill Mind-Map Reorganization

**Date:** 2026-09-29  
**Status:** Complete  
**Skills classified:** 6,500  
**Skill folders moved:** 6,500  
**Markdown links rebased:** 0

## Scope and method

All existing and newly added skills were moved under the nine top-level categories and the exact subfolder names in the user-approved mind map. Every skill was assigned to the closest listed subcategory; no extra `other` folder was created. Skill folder names and frontmatter were preserved; skill bodies were left intact except for narrowly scoped relative-link rebases if any were required. The top-level category of each skill was kept unchanged.

Assignments use the local skill slug and its existing task description in `INDEX.md`, with curated topic-prefix rules and narrowly scoped family rules for generated workflow batches. The implementation is in [`scripts/skill_taxonomy.py`](../scripts/skill_taxonomy.py); the read-only preflight and move/update routine is [`scripts/reorganize_skills_by_category.py`](../scripts/reorganize_skills_by_category.py). This is a classification heuristic, not a content rewrite or semantic guarantee; the per-skill CSV records each chosen subcategory and rule for review.

## Counts

| Top-level category | Total | Subcategory counts |
|---|---:|---|
| AI & Agent Systems (`ai-agent-systems`) | 606 | `agent-architecture-orchestration` 107; `prompts-context-memory` 36; `tools-integrations` 234; `evaluation-observability` 169; `safety-governance` 60 |
| Software & Development (`software-development`) | 816 | `languages-frameworks` 120; `frontend` 274; `backend-apis` 161; `architecture-devtools` 135; `testing-quality-release` 126 |
| Cloud, Infrastructure & Security (`cloud-infrastructure-security`) | 759 | `cloud-platforms` 94; `containers-kubernetes` 230; `networking-edge` 52; `devops-reliability` 77; `security-privacy` 306 |
| Data & Analytics (`data-analytics`) | 536 | `data-engineering` 170; `databases-storage` 92; `analytics-visualization` 80; `spreadsheets-geospatial` 119; `data-quality-governance` 75 |
| Business & Operations (`business-operations`) | 1,536 | `finance-accounting` 106; `product-growth` 509; `marketing-sales` 318; `people-operations` 101; `legal-compliance` 101; `retail-hospitality` 200; `supply-chain` 100; `insurance` 101 |
| Science, Health & Research (`science-health-research`) | 523 | `clinical-healthcare` 100; `trials-research-methods` 139; `life-sciences` 125; `physical-earth-sciences` 49; `statistics-evidence` 13; `medical-imaging` 97 |
| Engineering & Industry (`engineering-industry`) | 806 | `agriculture` 100; `construction-built-environment` 100; `energy-climate` 201; `manufacturing-quality` 102; `electronics-hardware` 298; `robotics-controls` 5 |
| Creative, Media & Design (`creative-media-design`) | 607 | `visual-graphic-design` 110; `ux-interaction-design` 32; `games-interactive` 221; `image-3d` 111; `audio-video` 130; `writing-publishing` 3 |
| Education & Public Service (`education-public-service`) | 311 | `curriculum-instruction` 171; `assessment-learning` 30; `civic-government` 40; `public-service-operations` 50; `nonprofit-community` 20 |
| **Total** | **6,500** | **51 subfolders; no uncategorized skills** |

## Validation

- All 6,500 skill paths have the canonical shape `skills/<category>/<subcategory>/<skill>/SKILL.md`.
- All skill names remain unique and every `INDEX.md` skill link resolves after the move.
- README, category guide, and INDEX counts are calculated from the actual moved files.
- No skill prose or frontmatter was rewritten; only local relative link targets, if present, were rebased for the additional directory level.
- `/home/user/uploads/skills.txt` remains unchanged with SHA-256 `d851ac5c2a77f0a17ea1e8e03c8a78c56622fbecb8e4299afb71b2b96fb290b4`.
- `.git/` remains absent.

## Files

- [`INDEX.md`](../INDEX.md) — every skill link now includes its subcategory path, and the router lists current category and subcategory counts.
- [`skills/README.md`](../skills/README.md) — full mind map, counts, and path format.
- [`README.md`](../README.md) — repository structure and quick-start path updated.
- [`skill-mindmap-assignments-2026-09-29.csv`](skill-mindmap-assignments-2026-09-29.csv) — per-skill rule and assignment ledger.
