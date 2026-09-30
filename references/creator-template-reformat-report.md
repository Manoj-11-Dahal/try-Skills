# Creator Template Reformat Report

**Date:** 2026-09-29  
**Status:** Complete  
**Supersedes:** `skill-template-reformat-report.md` for the current on-disk `SKILL.md` structure.

## Scope

Reformatted all **5,500 local `SKILL.md` files** under `skills/` to the newer Skill Creator Prompt structure. Every file contains the nine required sections: Overview, When to Use, Inputs, Instructions, Decision Rules, Output Format, Validation Checklist, Examples, and Success Criteria. Optional sections are included only where the source supports them.

The pinned upstream catalog count remains **2,478** and was used for topic discovery only. No upstream skill bodies were imported, and this migration did not merge skills.

## Content handling

- Original task-specific section text was preserved and reorganized under the closest applicable section.
- Source-backed artifact, acceptance, decision, boundary, edge/failure, and stop guidance is surfaced where applicable; additional derived text is labeled as source guidance.
- Unsupported fields are marked **Not specified** or omitted when optional. No tools, permissions, facts, examples, or capabilities were invented.
- **Example policy:** The user chose source-supported examples only. An audit found no input/output example sections, labels, or fenced examples in the original corpus, so all 5,500 required `Examples` sections state that no source example was available; none was fabricated.
- Existing descriptions were normalized from their original trigger and outcome text. Frontmatter has valid opening and closing `---` delimiters.

## Backups and converter

- Original source archive: [`backups/before-template-reformat-2026-09-29.tar.gz`](../backups/before-template-reformat-2026-09-29.tar.gz)  
  SHA-256: `3f6e0af7e2ccaa315b03b9f557b6e13e389261ef6edbe4a8ae61d8ffa122801f`
- Pre-migration rollback archive: [`backups/before-creator-template-2026-09-29.tar.gz`](../backups/before-creator-template-2026-09-29.tar.gz)  
  SHA-256: `52ace6adabcbdfb99c1cfa3d4514daf51880b7048956a43984a2275be5043512`
- Each archive has an adjacent `.sha256` manifest containing 5,500 file hashes; both archives matched their manifests.
- Converter: [`scripts/reformat_skills_to_creator_template.py`](../scripts/reformat_skills_to_creator_template.py)

## Validation results

- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_skills.py` — **5,500 validated; all repository checks passed.**
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v` — **7 tests passed.**
- Backup-based reproduction audit — **5,500/5,500** current files exactly reproduce from the verified original source archive and converter.
- All nine required sections, valid metadata, source-text preservation, heading uniqueness, links, and repository size limits passed.
- Optional-section coverage: Scope 5,495; Tools and Resources 5,439; Edge Cases and Recovery 5,327; Stop Conditions 5,340; Common Pitfalls 1; Related Skills 0.
- Largest reformatted file: **15,918 bytes**. Description content units: **42–113**; every description meets the 40-unit minimum and 1,024-character maximum.

Only files inside `/home/user/skills` were changed. The `.git/` directory remains absent.
