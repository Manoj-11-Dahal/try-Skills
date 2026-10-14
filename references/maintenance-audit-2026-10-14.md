# Repository maintenance audit — 2026-10-14

## Baseline findings

The checkout contained **15,860 `SKILL.md` files** across **nine categories and 65 populated subcategories**, but the current catalog and banner advertised 16,500 skills. `INDEX.md` contained 16,500 distinct skill links, **640 of which had no corresponding file**. The README also advertised 67 subcategories despite the taxonomy defining 65.

All seven baseline unit tests passed: they checked existing skill files but did not check index coverage or generated metadata drift. No third-party Python dependency manifest or application runtime was present to upgrade.

## Changes

- Reconciled the current index, category guide, README counts/tree/distribution, and SVG banner with the files actually present. Removed 640 stale index rows; no missing skill content was invented and no existing skill body was changed.
- Added a repeatable, read-only-by-default catalog synchronization tool with an explicit `--write` mode.
- Extended validation to check exact index coverage, stale/duplicate links and labels; added JSON reporting and graceful handling of unreadable files/malformed URLs. Fenced examples no longer produce false heading/link failures.
- Added focused regression tests, Python 3.10/3.14 CI, SHA-pinned GitHub Actions, weekly action update checks, cache ignores, and maintenance documentation.

## Current counts

| Category | Skills |
|---|---:|
| AI & Agent Systems | 2,027 |
| Software & Development | 2,514 |
| Cloud, Infrastructure & Security | 1,415 |
| Data & Analytics | 978 |
| Business & Operations | 2,302 |
| Science, Health & Research | 899 |
| Engineering & Industry | 2,146 |
| Creative, Media & Design | 3,268 |
| Education & Public Service | 311 |
| **Total** | **15,860** |

## Scope and limitations

This is a repository-integrity and maintenance-tooling update, not a claim that every domain workflow or external reference was refreshed against upstream sources. The cause of the 640 absent files was not established. Previous expansion reports, assignment ledgers, backups, and source research remain historical records; their totals are not the current inventory. Future intentional restoration of a missing package will be picked up by the synchronization tool.

## Verification

Local verification on Python 3.11.2:

- `python scripts/validate_skills.py --json`: 15,860 files scanned, zero issues.
- `python scripts/sync_catalog.py --check`: no metadata drift.
- `python -m unittest discover -s tests -v`: 34 tests passed.
- All scripts/tests also parse using Python 3.10 syntax rules; this is not a substitute for executing on that runtime.
- `git diff --check`: passed; no `SKILL.md` file changed.

The new Python 3.10/3.14 GitHub Actions matrix has been configured but was not executed in this local session.
