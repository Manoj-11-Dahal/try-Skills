# Changelog

Notable changes to the Agentic Skills library are recorded here. Versions follow semantic versioning for the library layout and maintenance tooling. A version entry does not by itself mean a GitHub release has been published.

## [Unreleased]

No additional changes recorded beyond the release prepared below.

## [1.0.0] — Unreleased

Prepared on **2026-10-14** as the first versioned release. Publication is pending; no release tag has been created. See [release notes and publishing checklist](releases/v1.0.0.md).

### Added

- Multi-level navigation for all **15,860 existing skills**: **12 categories → 65 subjects → 724 topics → 1,629 context/workflow groups → skills**.
- **803 navigation pages** with expandable branches, breadcrumbs, and complete topic-level skill lists. Terminal lists contain at most 40 skills.
- Dedicated **Cybersecurity & Privacy**, **Healthcare & Medicine**, and **Music & Audio** categories.
- Read-only-by-default catalog synchronization, explicit category migration, and an old/new-path receipt with content hashes.
- Exact catalog coverage, link/anchor/reachability checks, machine-readable validation reports, and regression tests.
- Python 3.10/3.14 CI configuration, SHA-pinned GitHub Actions, and Dependabot configuration.
- Contributor documentation, maintenance reports, and a root `VERSION` file.

### Changed

- Replaced the oversized flat index with a navigable category/subject/topic tree.
- Moved **3,677 existing packages** to the redesigned category layout; preserved all skill names and instruction content.
- Redesigned the native SVG banner and README, with automatically synchronized inventory statistics.
- Centralized current taxonomy and generated navigation; retained historical authoring tools and provenance records as historical material.

### Fixed

- Removed **640 stale catalog entries** that referenced files absent from the checkout; corrected the advertised inventory from 16,500 to 15,860.
- Corrected subject counts from 67 to 65.
- Excluded fenced examples from heading/link checks and improved malformed-link and unreadable-file handling.
- Restricted count updates so unrelated limits such as “40 skills per list” are not overwritten.
- Normalized the migration receipt to LF line endings and made its writer produce LF consistently.

### Compatibility and upgrade notes

- **Moved package paths are a breaking change relative to the unversioned layout.** Use the current tree and [migration receipt](references/category-tree-migration-2026-10-14.csv) to update bookmarks, scripts, and installation references.
- `INDEX.md` is no longer a flat table containing every skill. Consumers of that format must be adapted.
- `_topics/*.md` files are navigation indexes, not installable skills. Actual packages remain at `skills/<category>/<subject>/<skill-name>/SKILL.md` after the category migration.
- Dated generators may assume the old layout. Use the current maintenance commands rather than running historical builders unchanged.
- Repository checks do not certify all domain-specific guidance, external URLs, or upstream compatibility. No new external skill collection was imported for this release.
