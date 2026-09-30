# Skill Template Reformat Report

**Date:** 2026-09-29  
**Status:** Complete

## Scope

Reformatted all **5,500 local `SKILL.md` files** under `skills/` into the approved 19-section structure. The pinned upstream topic catalog count remains **2,478**; it was used only for topic discovery, and no upstream skill bodies were imported. This pass did not merge skills.

Every file now has these top-level sections, in this order:

1. Overview
2. When to Use
3. Trigger Examples
4. Scope
5. Inputs
6. Instructions
7. Decision Rules
8. Tools and Resources
9. Output Format
10. Quality Standards
11. Validation Checklist
12. Edge Cases and Recovery
13. Stop Conditions
14. Common Pitfalls
15. Examples
16. Test Cases
17. Success Criteria
18. Related Skills
19. Maintenance

Valid YAML frontmatter includes the required opening and closing `---` delimiters.

## Content handling

- Existing task-specific body text was preserved and moved under the closest applicable template section, labeled as preserved source content.
- Where source material directly supported it, artifact, feedback/acceptance criteria, stop guidance, boundaries, failure/recovery notes, and checklist items were also surfaced in their matching sections. These are source-derived reorganizations, not new task instructions.
- Unsupported items—including trigger examples, runnable test cases, related skills, and owner/version/review metadata—are explicitly marked **Not specified**. No examples, tests, ownership, or facts were invented.
- Existing descriptions were normalized to the `Use when … to …` form using their original trigger and outcome text.

## Recovery and audit artifacts

- Original-file backup: [`backups/before-template-reformat-2026-09-29.tar.gz`](../backups/before-template-reformat-2026-09-29.tar.gz)
- Backup SHA-256 manifest: [`backups/before-template-reformat-2026-09-29.sha256`](../backups/before-template-reformat-2026-09-29.sha256)
- Archive SHA-256: `3f6e0af7e2ccaa315b03b9f557b6e13e389261ef6edbe4a8ae61d8ffa122801f`
- Converter: [`scripts/reformat_skills_to_template.py`](../scripts/reformat_skills_to_template.py)

The archive contains all 5,500 original `SKILL.md` files. All 5,500 archived files matched their manifest hashes. A post-migration audit reproduced every current file byte-for-byte from the original archive and converter.

## Validation results

- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_skills.py` — **5,500 validated; all repository checks passed.**
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v` — **7 tests passed.**
- Full structural/source audit — **5,500/5,500** files have the required headings in order, valid metadata, and preserved source sections.
- Largest reformatted file: **14,237 bytes** (within the repository’s 60,000-byte limit).
- Description content units: **42–113** observed; every description is at least the 40-unit minimum and under the 1,024-character limit.

Only files inside `/home/user/skills` were changed. The `.git/` directory was not recreated.
